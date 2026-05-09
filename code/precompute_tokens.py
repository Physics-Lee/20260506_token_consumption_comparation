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
OPEN_SOURCE_MODELS = {
    "DeepSeek-R1": "deepseek-ai/DeepSeek-R1",
    "Llama-3-8B": "meta-llama/Meta-Llama-3-8B",
    "Llama-3-70B": "meta-llama/Meta-Llama-3-70B",
    "Qwen2.5-72B": "Qwen/Qwen2.5-72B",
    "Phi-2": "microsoft/phi-2",
    "Gemma-7B": "google/gemma-7b",
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
            tokenizer = AutoTokenizer.from_pretrained(
                model_id, trust_remote_code=True
            )
        except Exception as e:
            print(f"  [SKIP] Failed to load {model_id}: {e}")
            continue

        model_counts = {}
        for article_id, article in corpus.items():
            text_counts = {}
            for text in article["texts"]:
                lang = text["language"]
                content = text["content"]
                try:
                    tokens = tokenizer.encode(content)
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
