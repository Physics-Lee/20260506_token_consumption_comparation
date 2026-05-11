---
type: concept
source_count: 8
last_updated: 2026-05-10
tags: [vocabulary, tokenizer, bpe, scaling]
---

# Vocabulary Size

The number of distinct tokens in a tokenizer's vocabulary, typically set during BPE training as the stopping criterion.

## Overview

Vocabulary size is one of the most consequential hyperparameters in tokenizer design. It determines the tradeoff between sequence length (fewer tokens = cheaper API calls) and memory/load time (larger vocabulary = more storage). During BPE training, the algorithm starts with 256 byte tokens and repeatedly merges the most frequent adjacent pairs. Training stops when the vocabulary reaches the preset size.

OpenAI's progression illustrates this tradeoff: 50K (r50k/p50k, 2020-2021) → 100K (cl100k, 2022) → 200K (o200k, 2024). Each doubling roughly halves token count for common text patterns. For Chinese specifically, the jump from cl100k to o200k improved efficiency by 30-50%.

The industry has converged on ~200K as the current standard. Llama 4 (200K), Qwen 3.5 (248K), MiniMax (200K), and OpenAI o200k_base all cluster in this range. DeepSeek remains at 128K, the most conservative among current major models.

## Key perspectives

- **Capacity vs Efficiency**: Larger vocabularies can encode more common phrases as single tokens, reducing sequence length and API cost
- **Memory Cost**: Each token has an associated embedding vector. 200K vocabulary × hidden dimension × precision = significant memory overhead
- **Training Data Alignment**: Vocabulary should match the model's training corpus distribution. Mismatches cause inefficiency.

## Evidence and data

| Encoding | Vocab Size | Year | Typical Use |
|----------|-----------|------|-------------|
| gpt2 | ~50K | 2019 | GPT-2 |
| r50k_base | 50,000 | 2020 | GPT-3 base |
| p50k_base | 50,000 | 2021 | Codex, text-davinci-003 |
| cl100k_base | 100,000 | 2022 | GPT-3.5, GPT-4 |
| o200k_base | 200,000 | 2024 | GPT-4o, GPT-5.x |
| Llama 1/2 | 32K | 2023 | SentencePiece |
| Llama 3 | 128K | 2024 | tiktoken |
| Llama 4 | 200K | 2025 | tiktoken |
| Qwen 1.0-3 | ~150K | 2023-2025 | BBPE |
| Qwen 3.5 | 248K | 2026 | BBPE |
| DeepSeek V2 | 32K | 2024 | Byte-level BPE |
| DeepSeek V3+ | 128K | 2024+ | Byte-level BPE |

## Contradictions and debates

- 32K has been proven inadequate for multilingual models; no current major model is below 128K
- Qwen's conservative 150K for 3+ years was criticized for poor non-Chinese efficiency
- The "optimal" vocabulary size depends on training corpus composition, not just language count
- Once trained, vocabulary cannot change without retraining all embedding layers

## Sources

- [[source - BPE Termination]] — vocabulary size as training stopping condition
- [[source - OpenAI Encoder Naming]] — vocabulary size in encoding names
- [[source - LLM Tokenizer Evolution]] — cross-company vocabulary progression
- [[source - Tokenizer Iteration Ranking]] — iteration patterns and jump magnitudes
- [[source - r50k_base vs p50k_base]] — same size, different contents

## Related

- [[Byte Pair Encoding]] — algorithm whose training is controlled by vocabulary size
- [[Tokenization]] — the broader process of text-to-token conversion
- [[Multilingual Token Efficiency]] — how vocabulary size affects non-English compression