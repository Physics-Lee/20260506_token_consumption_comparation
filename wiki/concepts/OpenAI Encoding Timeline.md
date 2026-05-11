---
type: concept
source_count: 8
last_updated: 2026-05-10
tags: [openai, encoding, history, r50k, p50k, cl100k, o200k]
---

# OpenAI Encoding Timeline

The evolution of OpenAI's tokenizer encodings from 2019 to 2024, reflecting changes in product focus and training corpus.

## Overview

OpenAI has released five major encodings across six years, each corresponding to a product era. The progression tells the story of LLM evolution: from raw text completion to code generation to chat to multimodal AI.

## Key perspectives

**Feature-based naming**: OpenAI chose encoding-feature names (r50k, p50k, cl100k, o200k) over product names because encodings outlive products. GPT-3 was deprecated, but r50k_base remains in tiktoken for historical data decoding.

**Training corpus drives encoding**: Each encoding reflects its training data. r50k used pure text; p50k added GitHub code; cl100k optimized for chat; o200k expanded multilingual coverage.

**Vocabulary doubling strategy**: Each major product shift roughly doubled vocabulary: 50K → 100K → 200K. This wasn't coincidence—it reflects the engineering judgment that new use cases required more token capacity.

## Evidence and data

| Encoding | Year | Prefix | Vocab | Training Focus | Key Models |
|----------|------|--------|-------|---------------|------------|
| gpt2 | 2019 | — | ~50K | WebText (Reddit) | GPT-2 |
| r50k_base | 2020 | r=raw | 50K | Common Crawl + Books + Wikipedia | davinci, curie, babbage, ada |
| p50k_base | 2021 | p=prompt | 50K | Text + GitHub code | text-davinci-003, Codex |
| cl100k_base | 2022 | cl=Chat Language | 100K | Chat-optimized | GPT-3.5, GPT-4, text-embedding-3 |
| o200k_base | 2024 | o=omni | 200K | Multimodal + multilingual | GPT-4o, GPT-5.x, o1, o3 |

Encoding-to-model mapping (not one-to-one):
- o200k_base ← GPT-4o, GPT-4.1, o1, o3, GPT-5.x
- cl100k_base ← GPT-4, GPT-3.5-turbo, text-embedding-3, davinci-002
- p50k_base ← text-davinci-003, Codex, code-davinci-002
- r50k_base ← davinci, curie, babbage, ada (GPT-3 base)

## Contradictions and debates

- p50k_base had a variant (p50k_edit) for the deprecated Edit API, demonstrating why _base suffix exists
- gpt2 encoding remains in tiktoken purely for backward compatibility despite no active models
- davinci has three meanings with three different encodings, causing confusion

## Sources

- [[source - OpenAI Encoder Naming]] — naming format and prefix meanings
- [[source - OpenAI API Timeline]] — chronological release history
- [[source - What is Davinci]] — three davinci variants with different encodings
- [[source - GPT-2 vs r50k_base]] — evolution from GPT-2 to GPT-3 encoding
- [[source - r50k_base vs p50k_base]] — code corpus addition driving new encoding
- [[source - Davinci-002 and Embedding Encoding]] — why "old" names use new encodings
- [[source - Why Deprecated Models Still Work]] — encoding preservation after model deprecation

## Related

- [[Byte Pair Encoding]] — the algorithm underlying all OpenAI encodings
- [[Vocabulary Size]] — how vocabulary capacity changed across encodings
- [[Multilingual Token Efficiency]] — o200k's 30-50% CJK improvement over cl100k
- [[OpenAI]] — the organization behind these encodings
