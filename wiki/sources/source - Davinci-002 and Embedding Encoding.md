---
type: source
raw_file: "note/davinci-002-and-embedding-encoding.md"
date_ingested: 2026-05-10
tags: [davinci-002, embedding, cl100k, openai, encoding]
---

# Source: Davinci-002, Babbage-002, and Embedding Encoding

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** reference note

## Summary

This note explains why several "old-era" sounding OpenAI models all use cl100k_base (100K) encoding. The rule: any model with "-002" suffix is not the GPT-3 original. davinci-002 and babbage-002 (2023) are completely new models trained when cl100k_base was already the internal standard—there was no reason to use old r50k. They borrow the scientist names as brand tiers (davinci = strongest, babbage = budget) but use contemporary encodings.

Embedding models also use cl100k_base because: (1) they were all released after cl100k became standard (text-embedding-ada-002 in Dec 2022, text-embedding-3 in Jan 2024), and (2) changing embedding tokenizer would invalidate all previously vectorized documents. The note explains the practical reason for unified encoding: developers need consistent token counts for billing and estimation. If embedding used r50k and generation used cl100k, the same text would produce different token counts on different APIs.

## Key claims

- Models with "-002" suffix are new models using contemporary encodings, not GPT-3 originals
- davinci-002 and babbage-002 (2023) use cl100k_base, not r50k_base
- All embedding models use cl100k_base for release-timing and backward-compatibility reasons
- text-embedding-3 (Jan 2024) kept cl100k_base because o200k_base didn't exist yet (May 2024)
- Unified encoding across product lines simplifies developer token counting

## Entities mentioned

- [[OpenAI]] — davinci-002, babbage-002, text-embedding series

## Concepts touched

- [[Model Naming Conventions]] — how suffixes indicate model generations
- [[Embedding Tokenizer Stability]] — why embedding models don't change encodings
- [[Cross-Product Encoding Consistency]] — unified token counting across APIs
- [[Brand Tier Naming]] — using scientist names as price/performance indicators

## Notes

This note resolves a common confusion: seeing "davinci" in the tokenizer selector and assuming it means the 2020 GPT-3 model. The note clarifies that davinci-002 is a different model with a different encoding. For the project's historical comparison purposes, the "davinci" option represents the earliest era (r50k_base), while davinci-002 represents a later era (cl100k_base).