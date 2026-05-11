---
type: concept
source_count: 15
last_updated: 2026-05-10
tags: [tokenization, tokenizer, nlp, llm]
---

# Tokenization

The process of converting raw text into sequences of tokens (integer IDs) that language models can process.

## Overview

Tokenization is the first step in any LLM pipeline. Every model has an associated tokenizer that defines how text is split into discrete units. The same text tokenized by different models can produce dramatically different token counts—this is the central phenomenon the project investigates.

A tokenizer consists of two static lookup tables: a merges table (tens of thousands of rows mapping byte pairs to merge priorities) and a vocabulary table (mapping token strings to integer IDs). The total size is 1-5 MB. This is fundamentally different from the model itself, which is a neural network of hundreds of gigabytes. Tokenizers run locally in browsers without GPU; models require GPU servers.

The project's core hypothesis tests whether Classical Chinese, despite having the highest information density, actually consumes fewer tokens than Modern Chinese or English. Modern tokenizers are trained primarily on contemporary text, so Classical Chinese may be treated as rare Unicode sequences and split into multiple subword tokens.

## Key perspectives

- **Tokenizer ≠ Model**: Tokenizers are static dictionaries; models are neural networks. Tokenizers can be used indefinitely even after models are deprecated.
- **Precomputation vs Real-time**: OpenAI tokenizers can run in browser via CDN (50KB); open-source tokenizers require downloading 1-5MB tokenizer.json files, making precomputation preferable for static corpora.
- **Cross-era Comparison**: Comparing the same text across different historical encodings (r50k→p50k→cl100k→o200k) reveals how tokenizer evolution affects cost and efficiency.

## Evidence and data

- English: ~1.3 chars/token
- Spanish: ~1.2 chars/token
- Modern Chinese: ~0.6 chars/token
- Classical Chinese: ~0.8-1.0 chars/token (but tokenizer may split into subwords, increasing actual count)
- OpenAI o200k_base: 30-50% more efficient for CJK than cl100k_base
- DeepSeek: ~1.3 chars/token for Chinese (approaching English efficiency)

## Contradictions and debates

- **Information density vs Token density**: High information density does not necessarily translate to high token density. Classical Chinese may be information-dense but token-inefficient if the tokenizer hasn't learned its patterns.
- **Vocabulary size tradeoff**: Larger vocabularies improve compression for common patterns but increase memory. The 50K→200K progression reflects evolving tradeoff calculations.
- **Training corpus bias**: Tokenizers reflect their training data. Models trained predominantly on modern text may underperform on Classical Chinese, ancient languages, or domain-specific jargon.

## Sources

- [[source - Project Overview and Logic]] — core hypothesis about Classical Chinese
- [[source - Tokenizer Workflow Note]] — tokenizer internals explained
- [[source - Token Comparison Implementation Plan]] — hybrid real-time/precomputed strategy
- [[source - Tokenizer Browser Strategy]] — browser tokenization approaches
- [[source - Why Deprecated Models Still Work]] — tokenizer/model independence
- [[source - LLM Tokenizer Evolution]] — cross-family evolution data
- [[source - Tokenizer Names]] — algorithm comparison

## Related

- [[Byte Pair Encoding]] — dominant tokenization algorithm
- [[Vocabulary Size]] — number of tokens in a tokenizer's dictionary
- [[Special Tokens]] — non-text tokens (BOS, EOS, role markers)
- [[Multilingual Token Efficiency]] — how different languages compress across tokenizers