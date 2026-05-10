# Agent Knowledge Base

## build_index.py

### What it does
Reads all `data/*.json` files and generates `index.html` — the main Token Consumption Comparison page.

### Key behavior
- Reads `data/*.json` alphabetically by filename (excludes `token_counts.json`)
- Navigation buttons use each article's classical Chinese title
- Embeds precomputed token counts from `data/token_counts.json` for open-source models
- Includes gpt-tokenizer UMD bundles (r50k/p50k/cl100k/o200k) for real-time OpenAI token counting
- Supports three-state theme toggle (light / dark / follow system)

### Runtime
```bash
conda run -n token_analysis python code/build_index.py
```

---

## precompute_tokens.py

### What it does
Computes token counts for all articles × all languages, across multiple tokenizers, and writes to `data/token_counts.json`.

### Tokenizers computed
| Tokenizer | Source | Method |
|-----------|--------|--------|
| DeepSeek-R1 | deepseek-ai/DeepSeek-V3 | HuggingFace AutoTokenizer |
| Qwen2.5-72B | Qwen/Qwen2.5-72B | HuggingFace AutoTokenizer |
| Phi-2 | microsoft/phi-2 | HuggingFace AutoTokenizer |
| GPT-2 | tiktoken `gpt2` encoding | tiktoken.get_encoding |

### Requirements
```bash
pip install transformers tiktoken
# Python 3.11 + transformers<5 (5.x breaks DeepSeek tokenizer)
```

### Runtime
```bash
conda run -n token_analysis python code/precompute_tokens.py
```

---

## precompute_tokens.js

### What it does
Same as precompute_tokens.py, but pure JavaScript — downloads `tokenizer.json` from HuggingFace and implements byte-level BPE encoding without any Python dependencies.

### Requirements
Node.js. No npm packages needed.

### Runtime
```bash
node code/precompute_tokens.js
```

---

## Data Schema

### JSON structure
```json
{
  "id": "unique_snake_case_id",
  "metadata": {
    "title_zh": "Chinese title",
    "title_en": "English title",
    "title_es": "Spanish title",
    "author": "Author name",
    "source": "Source/publication",
    "period": "Historical period",
    "genre": "Genre",
    "original_language": "classical_chinese|modern_chinese|english|spanish"
  },
  "texts": [
    {"language": "classical_chinese", "role": "original|translation", "title": "...", "content": "..."},
    {"language": "modern_chinese", "role": "original|translation", "title": "...", "content": "..."},
    {"language": "english", "role": "original|translation", "title": "...", "content": "..."},
    {"language": "spanish", "role": "original|translation", "title": "...", "content": "..."}
  ]
}
```

### Critical Rules
1. `texts` array order must be: classical_chinese → modern_chinese → english → spanish
2. `role` must be `"original"` for one language, `"translation"` for the other three
3. `content` inside JSON uses `\n` for line breaks; `build_index.py` converts them to real newlines for HTML display
4. Always generate via `json.dump(ensure_ascii=False, indent=2)` — never hand-write JSON strings

### How to add a new article
1. Create a JSON file in `data/` following the schema above
2. Run `conda run -n token_analysis python code/precompute_tokens.py` to recompute token counts
3. Run `conda run -n token_analysis python code/build_index.py` to regenerate `index.html`
