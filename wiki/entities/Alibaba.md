---
type: entity
entity_type: organization
source_count: 5
last_updated: 2026-05-10
tags: [alibaba, qwen, chinese-llm, tokenizer]
---

# Alibaba

Chinese technology company that created the Qwen (通义千问) LLM family.

## Overview

Alibaba developed the Qwen series of large language models. Qwen uses BBPE (Byte-level BPE) with UTF-8 byte-level processing. The tokenizer vocabulary was remarkably stable across the first five generations (Qwen 1.0 through Qwen 3), staying around 150K with only minor adjustments. Qwen 2.5 (2024) expanded control tokens from 3 to 22 while keeping vocabulary at ~151K.

The major change came with Qwen 3.5 (2026), which jumped to 248K vocabulary—a 63% increase. This was driven by community complaints about poor token efficiency for Hindi, Italian, and German. Qwen is considered the most conservative established player in terms of tokenizer changes (6 model generations, only 2 tokenizer changes).

## Key facts

- Qwen name: "Question + answer" (Q + wen), Chinese name "通义千问"
- Uses tiktoken-style BPE but with self-trained vocabulary
- Qwen 1.0-3: ~150K vocab (stable for ~2 years)
- Qwen 2.5: 151,643 vocab (expanded control tokens)
- Qwen 3.5: 248,320 vocab (+63%, first major expansion)
- Highest Chinese compression rate among domestic Chinese models (C-Eval: 60.8% token efficiency)

## Mentioned in

- [[source - LLM Tokenizer Evolution]] — detailed Qwen evolution
- [[source - Tokenizer Iteration Ranking]] — most conservative established player
- [[source - Tokenizer Names]] — naming and vocabulary progression
- [[source - Tokenizer Browser Strategy]] — Qwen versions in timeline selector
- [[source - Plan vs Reality]] — Qwen 3.5 tokenizer.json unavailable due to firewall

## Related

- [[Qwen]] — Alibaba's LLM family
- [[BBPE]] — Byte-level BPE used by Qwen
- [[C-Eval]] — Chinese evaluation benchmark

## Open questions

- How does Qwen 3.5's 248K vocabulary affect Classical Chinese tokenization specifically?
- Will Qwen maintain BBPE or switch to standard tiktoken format in future versions?