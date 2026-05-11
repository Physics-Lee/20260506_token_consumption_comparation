---
type: source
raw_file: "note/plan-vs-reality.md"
date_ingested: 2026-05-10
tags: [plan-vs-reality, implementation-gap, js-vs-python]
---

# Source: Plan vs Reality

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** gap analysis note

## Summary

This note documents the divergence between the documented strategy (in tokenizer-browser-strategy.md) and the actual implementation. The planned approach was pure JavaScript: download tokenizer.json files directly, implement BPE algorithm by hand, zero dependencies (no transformers, no Python, no conda). The planned data format was nested by family (qwen/1.0-150K, deepseek/V2-32K) with a timeline selector for switching versions within a family. The planned coverage was Qwen 3 generations, DeepSeek 2 generations, Llama 3 generations, and GLM 2 generations.

The actual implementation uses Python precompute_tokens.py with AutoTokenizer.from_pretrained(), loading full HuggingFace models. Dependencies include transformers 4.57 + tiktoken, locked in a conda environment token_analysis (Python 3.11). A discovered pitfall: transformers 5.x breaks DeepSeek Chinese tokenization. The actual data format uses flat keys ("Qwen-7B (2023)", "DeepSeek-V3/R1 (2024.12)") without family nesting. The actual UI uses optgroup-based dropdowns, approximating a timeline but not fully implementing it. Actual coverage includes Qwen 2 generations (Qwen 3.5 missing due to HF firewall blocking tokenizer.json downloads), DeepSeek 2 generations, Phi-2, and GPT-2.

The root cause of the divergence: the JS path assumed downloading a single JSON file would suffice, but AutoTokenizer actually needs tokenizer_config.json to handle special token mappings and BOS/EOS tags. A hand-written BPE in JS would only handle basic merges, not special token injection—leading to mismatched token counts between JS and Python paths. The Python path correctly handles special tokens but has transformers version pitfalls. To align the two paths, precompute_tokens.js would need to read tokenizer_config.json and correctly inject special tokens, with output verified against the Python path.

## Key claims

- The documented JS-only path underestimated the complexity of special token handling
- AutoTokenizer requires both tokenizer.json and tokenizer_config.json for correct special token mapping
- transformers 5.x breaks DeepSeek Chinese tokenization, requiring version locking at 4.57
- Qwen 3.5 tokenizer.json is unavailable due to HuggingFace being firewalled in the user's region
- Aligning JS and Python paths requires implementing special token injection in JS

## Entities mentioned

- [[HuggingFace]] — AutoTokenizer and transformers library provider
- [[DeepSeek]] — model affected by transformers 5.x breaking change
- [[Alibaba]] — Qwen models affected by HF download firewall

## Concepts touched

- [[Special Tokens]] — BOS, EOS, and other non-vocabulary tokens requiring config
- [[BPE Algorithm]] — the core tokenization algorithm
- [[Tokenizer Config]] — tokenizer_config.json metadata file
- [[Implementation Gap]] — divergence between planned and actual approaches

## Notes

This is a valuable reality-check document. The JS path is not impossible but requires more work than initially assumed. The transformers version pitfall (5.x breaking DeepSeek) is a notable finding worth documenting for others working with these tools.