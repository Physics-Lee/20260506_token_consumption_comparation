---
type: source
raw_file: "note/tokenizers_is_all_you_need_yixuan.md"
date_ingested: 2026-05-11
tags: [tokenizer-reference, openai, open-source, corpus-reader, umd]
---

# Source: Tokenizers Is All You Need

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** reference documentation

## Summary

This is the definitive reference for all tokenizers used in corpus_reader.html: 10 OpenAI tokenizers (real-time browser calculation) and 6 open-source tokenizers (precomputed). All OpenAI models share 4 underlying BPE encodings; gpt-tokenizer computes them in browser without a server.

For o200k_base (GPT-4o / o-series / GPT-5.x): since GPT-4o's 2024 release, all new OpenAI models including o1/o3 and GPT-5 series share o200k_base. The only exception is gpt-oss-* using experimental o200k_harmony. CJK compression is 30-50% better than cl100k_base. For cl100k_base (GPT-4 / GPT-3.5): the 2022-2023 mainstream encoding, still used by text-embedding-3. For p50k_base (Codex): 2021-2022, ~50K vocab. For r50k_base (GPT-3): earliest, ~50K vocab.

Open-source models use precomputed token counts from HuggingFace tokenizer.json: DeepSeek-R1 (~100K BPE), Llama-3-8B/70B (~128K SentencePiece BPE), Qwen2.5-72B (~152K BPE), Phi-2 (~50K BPE), Gemma-7B (~256K SentencePiece).

The UMD loading approach is key: gpt-tokenizer npm provides separate UMD builds per encoding (~2MB each) that register global variables (GPTTokenizer_o200k_base, etc.). UMD was chosen over ES modules because the default export only includes o200k_base—separate UMD files enable encoding switching. Files are cached by browser after first load.

## Key claims

- All OpenAI models since GPT-4o (2024) share o200k_base; the only exception is gpt-oss-* with o200k_harmony
- gpt-tokenizer UMD builds (~2MB each) are pure JavaScript (not WASM), containing complete BPE encoding tables
- UMD chosen over ES modules because separate files per encoding enable runtime switching
- Open-source tokenizer counts are precomputed by node code/precompute_tokens.js and embedded as PRECOMPUTED_TOKENS
- Classical Chinese token efficiency varies significantly across encoders—this is a core comparison dimension

## Entities mentioned

- [[OpenAI]] — all OpenAI models and encodings
- [[DeepSeek]] — DeepSeek-R1 tokenizer
- [[Meta]] — Llama-3 tokenizers
- [[Alibaba]] — Qwen2.5 tokenizer
- [[Microsoft]] — Phi-2 tokenizer
- [[Google]] — Gemma tokenizer
- [[HuggingFace]] — tokenizer.json source
- [[gpt-tokenizer]] — JS implementation of OpenAI encodings

## Concepts touched

- [[OpenAI Encoding Timeline]] — mapping of models to encodings
- [[UMD]] — Universal Module Definition for browser script loading
- [[Precomputation]] — embedding precomputed token counts in HTML
- [[BPE]] — algorithm used by all listed tokenizers
- [[CJK Token Efficiency]] — o200k_base 30-50% improvement over cl100k_base

## Notes

This is the most current and comprehensive tokenizer reference in the project. It supersedes some details in earlier notes. The vocabulary sizes listed for open-source models should be cross-checked against [[source - DeepSeek-V2 Vocab Mystery]] for accuracy. The UMD global variable naming convention (GPTTokenizer_{encoding}) is the actual API used in the project.
