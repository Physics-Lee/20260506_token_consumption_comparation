"""
Pre-compute token counts for open-source models via HuggingFace tokenizers.

Reads all data/*.json corpus files and encodes each text segment
using HuggingFace tokenizers, then saves token counts to data/token_counts.json.

Usage:
    python code/precompute_tokens.py

Requires:
    pip install transformers
    pip install huggingface_hub  # for token-based access to gated models

Environment (optional):
    HF_TOKEN=<your_huggingface_token>  # for gated models like Llama, DeepSeek
"""
import json
import sys
from pathlib import Path

# --- Configuration ---
# Models needing non-default tokenizer loading
MODEL_LOAD_KWARGS = {
}

OPEN_SOURCE_MODELS = {
    # Qwen timeline: vocab grew from 150K → 151K → 248K
    "Qwen-7B (2023-)": "Qwen/Qwen-7B",
    "Qwen2.5-72B (2024-)": "Qwen/Qwen2.5-72B",
    "Qwen3.5-27B (2026-)": "Qwen/Qwen3.5-27B",
    # DeepSeek timeline: vocab jumped from 32K → 128K
    "DeepSeek-V2 (2024.05-)": "deepseek-ai/DeepSeek-V2-Lite",
    "DeepSeek-V3/R1/V4 (2024.12-)": "deepseek-ai/DeepSeek-V3",
    "Phi-2": "microsoft/phi-2",
}

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "token_counts.json"


def load_corpus():
    """Load all corpus JSON files and return {article_id: [text_records]}."""
    corpus = {}
    for f in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                article = json.load(fh)
            corpus[article["id"]] = article
        except Exception as e:
            print(f"  [WARN] Failed to read {f.name}: {e}")
    return corpus


def compute_token_counts(corpus):
    """Compute token counts for all models × articles × languages."""
    from transformers import AutoTokenizer

    result = {"open_source": {}}

    for display_name, model_id in OPEN_SOURCE_MODELS.items():
        print(f"\n{'='*60}")
        print(f"  Loading: {display_name} ({model_id})")
        print(f"{'='*60}")

        try:
            kwargs = {"trust_remote_code": True}
            kwargs.update(MODEL_LOAD_KWARGS.get(model_id, {}))
            tokenizer = AutoTokenizer.from_pretrained(model_id, **kwargs)
        except Exception as e:
            print(f"  [SKIP] Failed to load {model_id}: {e}")
            continue

        # Quick sanity check on first Chinese text
        first_article = next(iter(corpus.values()))
        first_cn = next((t['content'][:20] for t in first_article['texts'] if t['language'] == 'classical_chinese'), '')
        if first_cn:
            test_tokens = tokenizer.encode(first_cn)
            print(f"  Sanity: '{first_cn[:20]}' → {len(test_tokens)} tokens (expect 10-20 for Chinese)")

        model_counts = {}
        for article_id, article in corpus.items():
            text_counts = {}
            for text in article["texts"]:
                lang = text["language"]
                content = text["content"]
                try:
                    # DeepSeek tokenizer has issues with `tokenizer(text)` for Chinese;
                    # fallback to .encode() which handles it correctly
                    if "DeepSeek" in display_name:
                        tokens = tokenizer.encode(content)
                        text_counts[lang] = len(tokens) if isinstance(tokens, list) else len(tokens.ids)
                    else:
                        tok_out = tokenizer(content, add_special_tokens=False)
                        text_counts[lang] = len(tok_out["input_ids"])
                except Exception as e:
                    print(f"  [ERR] {article_id}/{lang}: {e}")
                    text_counts[lang] = -1

            model_counts[article_id] = text_counts
            print(
                f"  {article_id:30s}  "
                + "  ".join(
                    f"{lang}: {count:>5}"
                    for lang, count in text_counts.items()
                )
            )

        result["open_source"][display_name] = model_counts

    return result


def compute_gpt2(corpus):
    """Compute token counts for GPT-2 using tiktoken."""
    import tiktoken

    print(f"\n{'='*60}")
    print(f"  Loading: GPT-2 (tiktoken-gpt2)")
    print(f"{'='*60}")

    try:
        enc = tiktoken.get_encoding("gpt2")
    except Exception as e:
        print(f"  [SKIP] Failed to load GPT-2 encoding: {e}")
        print("  Install: pip install tiktoken")
        return {}

    model_counts = {}
    for article_id, article in corpus.items():
        text_counts = {}
        for text in article["texts"]:
            lang = text["language"]
            content = text["content"]
            try:
                tokens = enc.encode(content)
                text_counts[lang] = len(tokens)
            except Exception as e:
                print(f"  [ERR] {article_id}/{lang}: {e}")
                text_counts[lang] = -1

        model_counts[article_id] = text_counts
        print(
            f"  {article_id:30s}  "
            + "  ".join(
                f"{lang}: {count:>5}"
                for lang, count in text_counts.items()
            )
        )

    return {"GPT-2": model_counts}


def main():
    print("Loading corpus data...")
    corpus = load_corpus()
    if not corpus:
        print("No corpus data found in data/")
        sys.exit(1)
    print(f"  Loaded {len(corpus)} articles")

    print("\nComputing token counts...")
    result = compute_token_counts(corpus)

    # Compute GPT-2 tokens via tiktoken
    print("\nComputing GPT-2 token counts...")
    gpt2_result = compute_gpt2(corpus)
    if gpt2_result:
        result["open_source"].update(gpt2_result)

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved to {OUTPUT_FILE}")

    # Summary
    print("\n--- Summary ---")
    for model in result["open_source"]:
        total = sum(
            sum(counts.values())
            for counts in result["open_source"][model].values()
        )
        print(f"  {model}: {total:,} total tokens")


if __name__ == "__main__":
    main()
