---
type: source
raw_file: "note/tokenizer-workflow-note.md"
date_ingested: 2026-05-10
tags: [tokenizer, bpe, algorithm, browser]
---

# Source: Tokenizer Workflow

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** technical explanation

## Summary

This note explains tokenizer internals in accessible terms. A tokenizer consists of two static lookup tables: a merges table (tens of thousands of rows mapping byte pairs to merge priorities) and a vocab table (mapping token strings to token IDs). The total size is 1-5 MB per tokenizer. Crucially, a tokenizer is not an AI model—it is a dictionary plus splitting rules, while the AI model is a massive neural network. Tokenizers run in browsers without GPU; models require GPU.

The BPE process is described step by step: regex matching splits input into initial chunks, byte encoding converts to raw bytes, then a BPE loop repeatedly looks up the highest-priority merge from the merges table until no more merges are possible, finally mapping to token IDs via the vocab table. The entire process is "repeated lookup + merging" with no "inference" occurring.

Two browser implementation strategies are described: WASM compilation (tiktoken, ~2MB Rust-compiled WASM) and dynamic vocabulary loading (HuggingFace, 1-5MB tokenizer.json per model). The note addresses the question of whether BPE must be re-executed every time: yes, but this is not a problem because BPE is extremely fast (milliseconds for hundreds of characters), inputs are almost always different (cache hit rate near zero), and tables are loaded once per page and stay resident in memory.

## Key claims

- Tokenizers are lookup tables (merges + vocab), not neural networks
- BPE tokenization is pure algorithmic lookup and merge, with no machine learning inference
- Browser implementations use either WASM (tiktoken) or dynamic JSON loading (HuggingFace)
- BPE runs from scratch each time but completes in milliseconds; caching would not help
- Tokenizers are free and run locally; only the AI model usage is charged

## Entities mentioned

- [[OpenAI]] — tiktoken library
- [[HuggingFace]] — transformers.js for browser tokenization

## Concepts touched

- [[BPE]] — Byte Pair Encoding algorithm
- [[Tokenizer]] — text-to-token conversion system
- [[Merges Table]] — priority-ordered list of byte pair merges
- [[Vocabulary Table]] — token string to ID mapping
- [[WASM]] — WebAssembly for running native-code tokenizers in browser

## Notes

This is one of the most foundational notes in the collection. It correctly distinguishes between tokenizers (static dictionaries) and models (neural networks), a distinction that many users conflate. The performance argument (BPE is O(input length), no matrix operations) is a key justification for browser-side tokenization.