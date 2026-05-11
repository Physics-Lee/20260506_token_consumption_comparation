---
type: source
raw_file: "note/tiktokenizer-source-analysis.md"
date_ingested: 2026-05-10
tags: [tiktokenizer, source-analysis, architecture, wasm]
---

# Source: Tiktokenizer Source Analysis

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** source code analysis

## Summary

This note dissects the tiktokenizer.vercel.app implementation (by dqbd), a Next.js + T3 Stack + TypeScript project. It has two tokenizer paths. Path one (OpenAI): TiktokenTokenizer class imports get_encoding / encoding_for_model from "tiktoken", which loads a ~2-3MB WASM binary compiled from Rust. The WASM contains all encoding tables (cl100k_base, o200k_base, p50k_base, r50k_base) embedded as logic, not JSON. 30+ OpenAI models are supported because they all reuse 4 encodings; encoding_for_model() only does model name → encoding name mapping.

Path two (Open Source): OpenSourceTokenizer class uses @xenova/transformers. At build time (src/scripts/download.ts), tokenizer.json + tokenizer_config.json are downloaded from HuggingFace into public/hf/{org}/{model}/. At runtime, PreTrainedTokenizer.from_pretrained(model) loads the tokenizer, with env.remotePathTemplate pointing to "/hf/{model}" (served via Vercel to avoid CORS).

The visualization layer takes token ID arrays, decodes each token back to text bytes, uses graphemer library to split by visual character boundaries (handling emoji and multi-byte characters), then renders with colored highlighting per token boundary.

## Key claims

- tiktokenizer has two independent tokenizer paths: OpenAI (WASM) and open-source (transformers.js)
- OpenAI's 30+ models reuse only 4 encodings; model name → encoding mapping is a simple lookup
- Open-source tokenizers download tokenizer.json (1-5MB) at build time and serve via static hosting
- All computation happens in the browser (WASM or JS); zero backend API calls, zero cost
- graphemer library handles visual character boundaries for accurate token-to-text mapping

## Entities mentioned

- [[dqbd]] — author of tiktokenizer
- [[OpenAI]] — tiktoken library
- [[HuggingFace]] — @xenova/transformers, model repositories
- [[Vercel]] — hosting platform for tiktokenizer
- [[Xenova]] — creator of transformers.js

## Concepts touched

- [[WASM]] — WebAssembly for running Rust tiktoken in browser
- [[transformers.js]] — browser-compatible HuggingFace transformers
- [[Build-Time Download]] — downloading assets during build rather than runtime
- [[CORS Proxy]] — using same-origin paths to avoid cross-origin restrictions
- [[Grapheme Splitting]] — dividing text by visual character boundaries

## Notes

This analysis directly informed the project's architecture decisions. The observation that all computation is client-side (no API calls, no cost) validates the browser-side approach. The build-time download strategy for open-source tokenizers is a pattern the project could adopt if HuggingFace downloads were not firewalled in the user's region. The graphemer visualization technique could enhance the project's UI in the future.