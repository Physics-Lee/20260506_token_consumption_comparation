---
type: concept
source_count: 10
last_updated: 2026-05-10
tags: [algorithm, tokenization, bpe, subword]
---

# Byte Pair Encoding

A subword tokenization algorithm that iteratively merges the most frequent adjacent byte pairs to build a vocabulary.

## Overview

Byte Pair Encoding (BPE) is the dominant tokenization algorithm in modern LLMs. Originally developed by Philip Gage in 1994 for data compression, it was adapted for NLP by Sennrich et al. in 2016 and popularized by OpenAI's GPT-2 in 2019. BPE operates on bytes (0x00-0xFF) rather than characters, making it inherently multilingual and capable of encoding any Unicode text, including emoji, mathematical symbols, and code.

The algorithm has two phases. Training: start with 256 byte tokens, repeatedly scan corpus, find most frequent adjacent pair, merge into new token, add to vocabulary, until vocabulary reaches a preset size (typically 50K-200K). Inference: given input text, convert to bytes, repeatedly apply highest-priority merge from the trained merges table until no more merges are possible, then map resulting tokens to IDs via the vocabulary table.

BPE is a pure lookup-and-merge algorithm with no neural network inference. Tokenizers are 1-5MB static files (vocabulary + merges tables), while models are hundreds of gigabytes. This distinction is crucial: tokenizers can run in browsers without GPU; models cannot.

## Key perspectives

- **Training vs Inference**: Training is externally controlled (human sets vocabulary size limit); inference terminates naturally when no more merges are possible
- **Byte-level vs Character-level**: Modern BPE (BBPE) operates on bytes, eliminating out-of-vocabulary problems entirely
- **GPT-1 vs GPT-2+**: GPT-1 used spaCy word tokenization with BPE fallback; GPT-2 switched to pure byte-level BPE, enabling true multilingual support

## Evidence and data

- OpenAI vocabulary sizes: 50K (r50k/p50k), 100K (cl100k), 200K (o200k)
- Each vocabulary increase roughly halves the average tokens per word for common text
- o200k_base improves CJK efficiency by 30-50% over cl100k_base
- BPE inference is O(input length) with no matrix operations; hundreds of characters tokenize in milliseconds

## Contradictions and debates

- Larger vocabularies reduce token count but increase memory and loading time
- 50K-200K is empirically the sweet spot; theoretical unlimited vocabulary would be millions of tokens with diminishing returns
- Classical Chinese may not benefit from vocabulary expansion if the tokenizer was trained primarily on modern text

## Sources

- [[source - BPE Termination]] — training vs inference termination conditions
- [[source - Tokenizer Workflow Note]] — how BPE works step by step
- [[source - GPT-1 vs Later Tokenizers]] — evolution from word-level to byte-level BPE
- [[source - OpenAI Encoder Naming]] — vocabulary size progression
- [[source - Tokenizer Names]] — BPE vs WordPiece vs Unigram vs SentencePiece comparison
- [[source - LLM Tokenizer Evolution]] — how vocabulary sizes evolved across companies
- [[source - Tokenizer Iteration Ranking]] — iteration patterns related to vocabulary changes

## Related

- [[WordPiece]] — BERT's alternative merge algorithm (likelihood-based instead of frequency-based)
- [[SentencePiece]] — Google's language-agnostic wrapper that can use BPE or Unigram
- [[Unigram]] — top-down pruning alternative to BPE's bottom-up merging
- [[Tokenizer]] — the broader concept of text-to-token conversion
- [[Vocabulary Size]] — the limiting factor in BPE training