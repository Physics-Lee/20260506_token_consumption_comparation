---
type: concept
source_count: 5
last_updated: 2026-05-10
tags: [precomputation, tokenization, browser, performance]
---

# Precomputation

Computing token counts ahead of time for static data, embedding the results directly into the application rather than calculating at runtime.

## Overview

The project uses precomputation as a core strategy for displaying open-source model token counts in the browser. Since most open-source tokenizer models lack browser-ready CDNs (unlike OpenAI's gpt-tokenizer at 50KB), downloading 1-5MB tokenizer.json files per model at runtime would be impractical. Instead, the project precomputes token counts for all 48 text segments (12 articles × 4 languages) using Python scripts, stores results in data/token_counts.json, and embeds this data as a JavaScript variable in the generated HTML.

This hybrid approach—real-time calculation for OpenAI models (small CDN) and precomputed lookup for open-source models—provides instant token display without loading large tokenizer libraries in the browser.

## Key perspectives

- **Static data advantage**: The corpus is fixed (12 articles, 4 languages each), so precomputing is a one-time cost
- **Performance**: Precomputed lookups are microseconds; real-time BPE is milliseconds
- **Scalability**: Adding new articles requires re-running the precomputation script

## Evidence and data

Precomputation flow:
1. Download tokenizer.json from HuggingFace (1-5MB per model)
2. Run BPE on all 48 text segments
3. Store results in nested JSON: {company: {version: {article: {language: count}}}}
4. build_index.py embeds as JS variable PRECOMPUTED_TOKENS
5. Browser lookup: PRECOMPUTED_TOKENS[company][version][article][language] → instant result

## Contradictions and debates

- Precomputation cannot support user-provided text; only works for fixed corpus
- HuggingFace downloads are blocked in some regions, complicating the precomputation workflow
- The original flat data structure (open_source → model name) was replaced with nested company/version hierarchy for the timeline selector

## Sources

- [[source - Token Comparison Implementation Plan]] — original precomputation design
- [[source - Tokenizer Browser Strategy]] — precomputation as solution for non-OpenAI models
- [[source - How to Implement Timeline Selector]] — data structure migration for timeline support
- [[source - Update Workflow]] — precomputation as optional but recommended step

## Related

- [[Hybrid Tokenization Strategy]] — combining real-time and precomputed approaches
- [[Tokenization]] — the process being precomputed
- [[Browser Tokenization]] — alternative of running tokenizers directly in browser
