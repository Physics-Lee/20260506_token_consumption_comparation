---
type: source
raw_file: "note/why-deprecated-models-still-work.md"
date_ingested: 2026-05-10
tags: [deprecated, tiktoken, encoding, backward-compatibility]
---

# Source: Why Deprecated Models Still Work

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** explanation note

## Summary

This note explains why tiktokenizer.vercel.app and the project's tokenizer selector can still use deprecated models (code-davinci-002, text-davinci-003, etc.) even though the models themselves are offline. The reason: tokenizers and models are completely separate. A model's weights (175B parameters) may be decommissioned, but its BPE encoding table (a few MB static file) remains available in the tiktoken library forever.

Tiktokenizer loads encoding tables, not model weights. Its workflow is: load encoding table (static file) → run BPE algorithm on user text → output token count and visualization. No OpenAI API call, no model weights, no GPU needed. OpenAI's tiktoken library design principle is "all historical encodings permanently available" for three reasons: historical data复盘 (decoding old token sequences), cross-encoding comparison (same text across different eras), and data integrity (token sequences are meaningless without their encoding dictionary).

The note emphasizes that Tiktokenizer and the project include deprecated models not to encourage their use, but to enable comparison of token efficiency across historical encodings.

## Key claims

- Tokenizers and models are completely independent; a model can be offline while its encoding remains usable
- tiktoken loads encoding tables (MB-scale static files), not model weights (GB-scale neural networks)
- OpenAI permanently preserves all historical encodings in tiktoken for data integrity and comparison
- Deprecated models in the tokenizer selector enable historical token efficiency comparison
- Encoding tables are the "key" to interpreting token sequences; losing them makes historical data unreadable

## Entities mentioned

- [[OpenAI]] — tiktoken library
- [[Tiktokenizer]] — dqbd's tokenizer visualization tool

## Concepts touched

- [[Model vs Encoding Separation]] — the independence of tokenizers from trained models
- [[Backward Compatibility]] — preserving historical encodings for data integrity
- [[Historical Data Analysis]] — comparing tokenization across model generations
- [[Encoding as Data Key]] — token sequences require their encoding to be interpretable

## Notes

This note provides the philosophical justification for including deprecated models in the project's tokenizer selector. The analogy of "encoding table = car parts catalog, model = the car itself" is particularly effective. The observation that OpenAI marks models as DEPRECATED in code comments but never removes their encoding mappings is a subtle but important detail about their library maintenance policy.