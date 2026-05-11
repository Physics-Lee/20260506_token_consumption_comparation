---
type: source
raw_file: "note/token-comparison-plan.md"
date_ingested: 2026-05-10
tags: [implementation-plan, tokenizer-ui, precomputation]
---

# Source: Token Comparison Implementation Plan

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** implementation plan

## Summary

This note outlines the original implementation plan for adding tokenizer selection and token consumption comparison to corpus_reader.html. The core strategy is a hybrid computation approach: OpenAI models use real-time calculation via the gpt-tokenizer CDN (50KB, loads instantly in browser), while open-source models (DeepSeek, Llama, Qwen, etc.) use precomputed token counts embedded in the HTML. This avoids loading 30MB of transformers.js at runtime.

The data flow involves: data/*.json (12 articles x 4 languages = 48 text segments) → code/precompute_tokens.py (downloads HuggingFace tokenizer.json, encodes all texts) → data/token_counts.json → code/json2html.py (reads token data, injects into HTML, adds tokenizer selector UI). The precomputed result format nests by model name, then article ID, then language.

The UI design places a tokenizer selector dropdown in the navigation bar, organized by provider (OpenAI vs open-source). For OpenAI models, the JavaScript uses gpt-tokenizer from CDN to encode text on the fly. For open-source models, it reads from the precomputed PRECOMPUTED_TOKENS object. The plan lists supported models including GPT-4o, GPT-4, GPT-3.5-turbo, text-davinci-003, davinci, o1, o3 for OpenAI; and DeepSeek-R1, Llama-3-8B/70B, Qwen2.5-72B, Phi-2, Gemma-7B for open-source.

## Key claims

- A hybrid approach (real-time for OpenAI, precomputed for open-source) is optimal for browser performance
- Precomputing token counts for static corpus eliminates the need to load large tokenizer libraries in browser
- gpt-tokenizer CDN at 50KB is negligible overhead for real-time OpenAI token counting
- The comparison table should add a "Token count for selected tokenizer" column alongside Unicode character count

## Entities mentioned

- [[OpenAI]] — GPT-4o, GPT-4, GPT-3.5-turbo models
- [[DeepSeek]] — DeepSeek-R1 tokenizer
- [[Meta]] — Llama-3 series tokenizers
- [[Alibaba]] — Qwen2.5 tokenizer
- [[Microsoft]] — Phi-2 tokenizer
- [[Google]] — Gemma tokenizer

## Concepts touched

- [[Precomputation]] — computing token counts ahead of time for static data
- [[Hybrid Tokenization Strategy]] — combining real-time and precomputed approaches
- [[Tokenizer Selection UI]] — dropdown interface for switching between tokenizers
- [[CDN]] — Content Delivery Network for loading gpt-tokenizer

## Notes

This plan was written before the project pivoted to a single-pipeline approach (build_index.py only, dropping json2html.py and corpus_reader.html). See [[source - Why Single Pipeline]] and [[source - Plan vs Reality]] for the evolution. The precomputed data structure described here (`open_source` key) was later replaced by a company/version hierarchy.