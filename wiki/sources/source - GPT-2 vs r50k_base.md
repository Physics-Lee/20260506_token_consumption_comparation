---
type: source
raw_file: "note/gpt2-vs-r50k.md"
date_ingested: 2026-05-10
tags: [gpt-2, r50k, openai, encoding, history]
---

# Source: GPT-2 vs r50k_base

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** historical comparison

## Summary

This note compares the gpt2 encoding with r50k_base. Both have ~50K vocabulary but belong to different eras with different training corpora. gpt2 (2019) was trained on WebText (Reddit posts with 3+ upvotes), while r50k_base (2020) was trained on GPT-3's much larger corpus (Common Crawl + WebText2 + Books + Wikipedia). The difference is small for common English text but noticeable for GPT-3's new content types: code snippets, multilingual text, and math/scientific symbols.

gpt2 remains in tiktoken purely for backward compatibility—no in-service models use it, but tiktoken promises that all historical model names return correct encodings. The relationship is likened to iPhone 4 vs iPhone 5: same brand, different internals, token counts look similar but vocabulary structure differs.

## Key claims

- gpt2 and r50k_base both have ~50K vocabulary but different training corpora
- gpt2: WebText (Reddit); r50k: Common Crawl + WebText2 + Books + Wikipedia
- Differences are small for common English but visible for code, multilingual, and scientific text
- gpt2 remains in tiktoken only for backward compatibility; no active models use it
- The upgrade from gpt2 to r50k was "homogeneous" (more text), unlike r50k→p50k which was "cross-domain" (text+code)

## Entities mentioned

- [[OpenAI]] — GPT-2, GPT-3
- [[Reddit]] — source of WebText corpus
- [[Common Crawl]] — part of GPT-3 training data

## Concepts touched

- [[Training Corpus]] — the data used to train BPE vocabulary
- [[Backward Compatibility]] — keeping old encodings available in libraries
- [[Vocabulary Evolution]] — how vocabularies change across model generations

## Notes

This note clarifies a subtle point: gpt2 and r50k_base are not the same encoding despite similar vocabulary sizes. For the project's purposes, both are included in the tokenizer selector to show historical progression. The distinction between "homogeneous" (gpt2→r50k) and "cross-domain" (r50k→p50k) upgrades is a useful framework for understanding encoding evolution.