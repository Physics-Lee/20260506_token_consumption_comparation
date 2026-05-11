---
type: source
raw_file: "note/tokenizer-browser-strategy.md"
date_ingested: 2026-05-10
tags: [browser, precomputation, huggingface, timeline-selector]
---

# Source: Tokenizer Browser Strategy

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** strategy note

## Summary

This note outlines the browser-side tokenizer display strategy. Currently only OpenAI models can do real-time browser tokenization (via gpt-tokenizer UMD CDN). All other companies lack browser CDNs for their tokenizer.json files. The proposed solution: precompute all token counts and embed them as JSON in the HTML.

The precomputation flow: download tokenizer.json from HuggingFace (each model version has a unique static file), run BPE algorithm on all 48 text segments (12 articles × 4 languages), write results to data/token_counts.json with nested structure by company and version, then build_index.py embeds this as a JS variable. The proposed UI is a timeline selector: within each company (Qwen, DeepSeek, Llama, GLM, etc.), users can switch between historical versions to see how token counts evolved.

The note documents tokenizer evolution per company: Qwen has 3 key versions (~150K, 151K, 248K), DeepSeek has 2 (32K, 128K), Llama has 3 (32K SentencePiece, 128K tiktoken, 200K tiktoken). The only blocker is HuggingFace being firewalled in the user's region, requiring workarounds (VPN, hf-mirror.com, manual download, or jsDelivr CDN).

The core value proposition: letting users see the same text's token consumption curve across different historical encodings, testing whether "Classical Chinese saves tokens" holds across tokenizer generations.

## Key claims

- Only OpenAI has browser-ready tokenizer CDN; all others require precomputation
- Each model version's tokenizer.json is an independent static file (1-5MB)
- Precomputed token counts enable instant version switching without downloading tokenizers
- Timeline selector UI lets users compare tokenization across historical versions within each company
- HuggingFace downloads are blocked in the user's region, requiring mirror/workaround

## Entities mentioned

- [[OpenAI]] — gpt-tokenizer CDN
- [[HuggingFace]] — source for tokenizer.json files
- [[Alibaba]] — Qwen versions
- [[DeepSeek]] — DeepSeek versions
- [[Meta]] — Llama versions
- [[Zhipu AI]] — GLM versions
- [[Moonshot AI]] — Kimi versions
- [[MiniMax]] — MiniMax versions

## Concepts touched

- [[Precomputation Strategy]] — computing token counts ahead of time
- [[Timeline Selector]] — UI for switching between historical tokenizer versions
- [[HuggingFace Firewall]] — network access issues for HF downloads
- [[Browser Tokenization]] — running tokenizers client-side in web browsers

## Notes

This note is the strategic complement to [[source - Token Comparison Implementation Plan]]. It focuses on the open-source/historical-version aspect rather than the OpenAI real-time aspect. The timeline selector concept is the project's most distinctive UI feature compared to other tokenizer tools. The firewall issue is a practical blocker documented further in [[source - Plan vs Reality]].