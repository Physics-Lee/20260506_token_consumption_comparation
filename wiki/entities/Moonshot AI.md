---
type: entity
entity_type: organization
source_count: 2
last_updated: 2026-05-10
tags: [moonshot, kimi, chinese-llm, open-source]
---

# Moonshot AI

Chinese AI company (月之暗面) that created the Kimi LLM family, known for its sudden pivot to open-source with Kimi K2.

## Overview

Moonshot AI operated Kimi K1 (2023) as a completely closed model—tokenizer, weights, and training data were all undisclosed. In a dramatic reversal, Kimi K2 (July 2025) was fully open-sourced: weights, tokenizer, and inference code all released on HuggingFace.

K2's tokenizer is based on OpenAI's tiktoken format (using tiktoken.model files and load_tiktoken_bpe() function), with a vocabulary of 160K. A notable optimization: the regex pattern includes [\p{Han}]+ for explicit Chinese character matching, optimizing Chinese tokenization. At 160K, K2 sits between OpenAI's cl100k_base (100K) and o200k_base (200K).

## Key facts

- K1 (2023): fully closed, tokenizer unknown
- K2 (2025.07): fully open-source, 160K vocab, tiktoken-based
- K2: 1T total parameters, 32B active parameters
- Explicit Chinese optimization in regex: [\p{Han}]+ pattern
- Only 1 tokenizer iteration (closed → open)

## Mentioned in

- [[source - LLM Tokenizer Evolution]] — closed-to-open pivot
- [[source - Tokenizer Iteration Ranking]] — 1 iteration

## Related

- [[Kimi]] — Moonshot AI's LLM family
- [[tiktoken]] — format used by Kimi K2's tokenizer

## Open questions

- Will Moonshot continue the open-source approach for K3 and beyond?
- How does K2's explicit Chinese regex optimization compare to other models' implicit handling?
