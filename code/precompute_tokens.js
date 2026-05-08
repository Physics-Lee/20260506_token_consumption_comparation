/**
 * Pre-compute token counts for open-source models.
 *
 * Downloads tokenizer.json from HuggingFace and uses pure-JS BPE to encode.
 *
 * Usage: node code/precompute_tokens.js
 *   HF_TOKEN=xxx node code/precompute_tokens.js  # for gated models
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "url";
import fs from "fs";

// Fix Windows path: /D:/... → D:/...
const __dirname = new URL(".", import.meta.url).pathname.replace(/^\/+/, "");
const ROOT = join(__dirname, "..");
const DATA_DIR = join(ROOT, "data");
const CACHE_DIR = join(ROOT, "node_modules", ".tokenizer_cache");

const HF_TOKEN = process.env.HF_TOKEN || "";

// --- Configuration ---
const MODELS = [
  { id: "Qwen2.5-72B", repo: "Qwen/Qwen2.5-72B", gated: false },
  { id: "Phi-2", repo: "microsoft/phi-2", gated: false },
  { id: "Gemma-7B", repo: "google/gemma-7b", gated: true },
  { id: "DeepSeek-R1", repo: "deepseek-ai/DeepSeek-R1", gated: true },
  { id: "Llama-3-8B", repo: "meta-llama/Meta-Llama-3-8B", gated: true },
  { id: "Llama-3-70B", repo: "meta-llama/Meta-Llama-3-70B", gated: true },
];

// --- Download tokenizer.json ---
async function downloadTokenizer(model) {
  if (!existsSync(CACHE_DIR)) mkdirSync(CACHE_DIR, { recursive: true });
  const cachePath = join(CACHE_DIR, `${model.id}.json`);

  if (existsSync(cachePath)) {
    console.log(`  [CACHE] ${model.id}`);
    return JSON.parse(readFileSync(cachePath, "utf-8"));
  }

  const url = `https://huggingface.co/${model.repo}/resolve/main/tokenizer.json`;
  console.log(`  [FETCH] ${url}`);
  const headers = {};
  if (HF_TOKEN) headers["Authorization"] = `Bearer ${HF_TOKEN}`;

  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

  const data = await res.json();
  writeFileSync(cachePath, JSON.stringify(data));
  return data;
}

// --- Build merge rank map ---
function buildMergeRanks(merges) {
  const ranks = {};
  merges.forEach((m, i) => (ranks[m] = i));
  return ranks;
}

// --- Get pre-tokenization regex pattern from tokenizer config ---
function getPreTokenPattern(tokenizerData) {
  const pt = tokenizerData.pre_tokenizer;

  // GPT-2 style ByteLevel pattern (used by many models)
  const gpt2Pattern =
    /'(?i:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+/gu;

  if (!pt) return gpt2Pattern;

  // Unwrap Metaspace if present
  const inner = pt.type === "Metaspace" ? pt.pre_tokenizer : pt;

  if (inner?.type === "ByteLevel") return gpt2Pattern;
  if (inner?.pattern?.String) return new RegExp(inner.pattern.String, "gu");

  // Check pretokenizers array
  const list = pt.pretokenizers;
  if (list) {
    for (const p of list) {
      if (p.type === "ByteLevel") return gpt2Pattern;
      if (p.pattern?.String) return new RegExp(p.pattern.String, "gu");
    }
  }

  return gpt2Pattern;
}

// --- Byte-level BPE encoding ---
function encode(text, tokenizerData) {
  const merges = tokenizerData.model?.merges;
  if (!merges || merges.length === 0) return -1;

  const mergeRanks = buildMergeRanks(merges);
  const pattern = getPreTokenPattern(tokenizerData);

  const words = text.match(pattern) || [];
  let total = 0;

  for (const word of words) {
    // Byte-level encoding: each byte → Unicode char (code point 256 + byte)
    const encoder = new TextEncoder();
    const bytes = encoder.encode(word);
    let tokens = [...bytes].map((b) => String.fromCodePoint(256 + b));

    // BPE merge loop
    while (tokens.length >= 2) {
      let bestRank = Infinity;
      let bestI = -1;

      for (let i = 0; i < tokens.length - 1; i++) {
        const rank = mergeRanks[tokens[i] + " " + tokens[i + 1]];
        if (rank !== undefined && rank < bestRank) {
          bestRank = rank;
          bestI = i;
        }
      }

      if (bestI === -1) break;

      tokens[bestI] = tokens[bestI] + tokens[bestI + 1];
      tokens.splice(bestI + 1, 1);
    }

    total += tokens.length;
  }

  return total;
}

// --- Main ---
async function main() {
  // Load corpus
  const corpus = {};
  for (const f of fs.readdirSync(DATA_DIR).filter((f) => f.endsWith(".json"))) {
    const article = JSON.parse(readFileSync(join(DATA_DIR, f), "utf-8"));
    corpus[article.id] = article;
  }
  console.log(`Loaded ${Object.keys(corpus).length} articles\n`);

  const result = { open_source: {} };

  for (const model of MODELS) {
    console.log(`\n${"=".repeat(50)}`);
    console.log(`${model.id}  [gated: ${model.gated}]`);
    console.log(`${"=".repeat(50)}`);

    let td;
    try {
      td = await downloadTokenizer(model);
    } catch (e) {
      console.log(`  [SKIP] ${e.message}`);
      continue;
    }

    const mc = {};
    let totalT = 0;

    for (const [aid, article] of Object.entries(corpus)) {
      const tc = {};
      for (const text of article.texts) {
        const c = encode(text.content, td);
        tc[text.language] = c;
        totalT += c;
      }
      mc[aid] = tc;
      console.log(
        `  ${aid.padEnd(30)} ` +
          Object.entries(tc)
            .map(([l, c]) => `${l}: ${String(c).padStart(5)}`)
            .join("  ")
      );
    }

    result.open_source[model.id] = mc;
    console.log(`  TOTAL: ${totalT.toLocaleString()} tokens`);
  }

  // Save
  const outPath = join(DATA_DIR, "token_counts.json");
  writeFileSync(outPath, JSON.stringify(result, null, 2));
  console.log(`\n✅ Saved to ${outPath}`);

  // Summary
  console.log("\n--- Summary ---");
  for (const mid of Object.keys(result.open_source)) {
    const m = result.open_source[mid];
    const t = Object.values(m).reduce(
      (s, a) => s + Object.values(a).reduce((ss, c) => ss + (c > 0 ? c : 0), 0),
      0
    );
    console.log(`  ${mid.padEnd(18)} ${t.toLocaleString()} tokens`);
  }
}

main().catch(console.error);
