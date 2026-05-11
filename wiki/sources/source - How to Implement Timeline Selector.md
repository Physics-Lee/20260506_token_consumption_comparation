---
type: source
raw_file: "note/how-to-implement-timeline-selector.md"
date_ingested: 2026-05-10
tags: [implementation, timeline-selector, build-index, token-counts]
---

# Source: How to Implement Timeline Selector

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** implementation guide

## Summary

This note is a step-by-step migration guide from the current flat tokenizer selector to a company-grouped timeline selector. Current state: single dropdown with OpenAI + a few open-source models; token_counts.json uses {"open_source": {"Qwen2.5-72B": {...}}}; JS lookup uses pre.open_source[name][article][lang]. Target state: company-grouped dropdown (Llama evolution, Qwen evolution, DeepSeek evolution); token_counts.json uses {"qwen": {"1.0-150K": {...}}, "deepseek": {...}}; JS lookup splits "qwen/3.5-248K" into company/version.

The note provides concrete code changes for four files: token_counts.json structure (top-level keys change from "open_source" to company names), build_index.py selector HTML (~30 lines, optgroup per company with version options using company/version value format), build_index.py JS logic (~15 lines, split by '/' instead of isOpenSource() check), and precompute_tokens.js (multi-version download loop with output structure adjustment). Special cases: GLM uses tokenizer.model (SentencePiece format), Kimi uses tiktoken.model, requiring separate loading logic.

The total estimated change is ~100 lines across all files. No CSS or table generation logic needs modification. The migration is recommended in two steps: first restructure token_counts.json + JS lookup (without adding new versions), then add historical versions one by one.

## Key claims

- Timeline selector requires restructuring token_counts.json from flat "open_source" to nested company/version
- Option values use "company/version" format, split by JS on selection change
- GLM and Kimi require special handling (tokenizer.model and tiktoken.model formats)
- Total change is ~100 lines; no CSS or table logic needs modification
- Two-step migration recommended: restructure first, then add versions incrementally

## Entities mentioned

- (none)

## Concepts touched

- [[Timeline Selector UI]] — grouped dropdown showing version evolution per company
- [[Data Structure Migration]] — changing nested JSON structure
- [[Tokenizer Format Variants]] — tokenizer.json vs tokenizer.model vs tiktoken.model

## Notes

This is the most detailed implementation note in the collection. The two-step migration strategy (restructure first, add versions second) is good risk management. The special handling for GLM (SentencePiece) and Kimi (tiktoken format) is an important detail that could cause bugs if overlooked. The note predates some actual implementation that may have already occurred in build_index.py.