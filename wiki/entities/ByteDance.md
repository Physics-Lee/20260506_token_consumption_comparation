---
type: entity
entity_type: organization
source_count: 3
last_updated: 2026-05-10
tags: [bytedance, doubao, closed-source, chinese-llm]
---

# ByteDance

Chinese technology company behind TikTok/Douyin and the Doubao (豆包) LLM service.

## Overview

ByteDance operates the Doubao LLM service, which has the highest daily token call volume among Chinese LLM providers (4 trillion tokens/day). However, Doubao is unique among major Chinese LLMs in having a completely closed tokenizer—algorithm, vocabulary size, and special token naming are all undisclosed.

The only ByteDance model with any tokenizer disclosure is Seed-OSS-36B (August 2025), which uses BPE with 155K vocabulary. It is unknown whether this is the same tokenizer used by the commercial Doubao API.

## Key facts

- Doubao: 4 trillion daily token calls, highest market share in China
- Completely closed: algorithm, vocab size, special tokens all undisclosed
- API is OpenAI-compatible but only exposes /v1/chat/completions
- Cannot analyze Doubao tokenization without API usage data
- Seed-OSS-36B (2025): 155K vocab — only open glimpse into ByteDance tokenizer

## Mentioned in

- [[source - Tokenizer Names]] — only fully black-box tokenizer among major Chinese LLMs
- [[source - LLM Tokenizer Evolution]] — closed vs open comparison
- [[source - Tokenizer Iteration Ranking]] — 1 iteration (Seed-OSS)

## Related

- [[Doubao]] — ByteDance's commercial LLM service
- [[Seed-OSS-36B]] — ByteDance's only open-sourced model
- [[Volces]] — ByteDance's cloud platform (火山方舟)

## Open questions

- Does Doubao use the same tokenizer as Seed-OSS-36B, or a different one?
- Will ByteDance ever open its tokenizer, or will it remain permanently closed?
- How does Doubao's token efficiency compare to open Chinese models?