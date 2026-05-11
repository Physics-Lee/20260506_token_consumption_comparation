---
type: source
raw_file: "note/r50k-vs-p50k.md"
date_ingested: 2026-05-10
tags: [r50k, p50k, openai, encoding, code]
---

# Source: r50k_base vs p50k_base

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** technical comparison

## Summary

This note compares r50k_base and p50k_base, which share the same 50,000 vocabulary size but have completely different contents. r50k (raw, 2020) was trained on pure text (webpages, articles, books) for GPT-3 base models (davinci, curie, babbage, ada). p50k (prompt, 2021) added massive GitHub code to the training corpus for Codex and text-davinci-003.

The divergence arose because r50k split code poorly—keywords and function names were fragmented. Example: "import numpy as np" produced similar but suboptimal tokenization in r50k. p50k's code-augmented vocabulary improved code tokenization by 5-15%. The analogy is two 50-page dictionaries with different contents: r50k is rich in literary vocabulary, p50k is rich in programming vocabulary (sacrificing some low-frequency literary terms).

The note observes that this split became unnecessary with o200k_base (200K vocabulary), which has enough space for both text and code tokens. GPT-4o unified text and code in a single encoding.

## Key claims

- r50k_base and p50k_base have identical vocabulary sizes (50K) but completely different contents
- r50k was trained on pure text; p50k added GitHub code for Codex
- p50k improves code tokenization by 5-15% over r50k
- The split was necessary because 50K was too small to accommodate both text and code
- o200k_base (200K) eliminated this split by having enough capacity for both domains

## Entities mentioned

- [[OpenAI]] — creator of both encodings
- [[Codex]] — code generation model that motivated p50k_base
- [[GitHub]] — source of code training data for p50k
- [[GPT-4o]] — model using o200k_base, which unified text and code

## Concepts touched

- [[Domain-Specific Vocabulary]] — training corpus composition affecting vocabulary content
- [[Code Tokenization]] — how programming text is split into tokens
- [[Vocabulary Capacity]] — tradeoff between vocabulary size and coverage
- [[Token Efficiency for Code]] — measuring code compression across encodings

## Notes

This comparison is directly relevant to the project's tokenizer selector, which includes both r50k_base and p50k_base options. The 5-15% code efficiency improvement is a concrete metric that users can verify with the tool. The observation that o200k_base made the split unnecessary is a good example of how vocabulary scaling solves domain-specific problems.