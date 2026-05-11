---
type: entity
entity_type: organization
source_count: 2
last_updated: 2026-05-10
tags: [minimax, chinese-llm, open-source]
---

# MiniMax

Chinese AI company that launched with a 200K vocabulary tokenizer, skipping the small-vocab evolutionary phase entirely.

## Overview

MiniMax entered the open-source LLM space in 2025 with MiniMax-Text-01, featuring a 200,064 vocabulary BPE tokenizer and 456B total parameters (45.9B active). Their second model, MiniMax-M2 (October 2025), reduced to 230B total / 10B active parameters but kept the exact same tokenizer.

MiniMax is notable for starting at the industry convergence point (200K) without going through the 32K→128K→200K evolution that other companies experienced. This "starting at the finish line" approach reflects the maturation of the field by 2025.

## Key facts

- MiniMax-Text-01 (2025.01): 200,064 vocab, BPE, 456B total / 45.9B active params
- MiniMax-M2 (2025.10): same tokenizer (200,064 vocab), 230B total / 10B active params
- Only 1 tokenizer iteration (never changed since launch)
- Vocabulary size directly matches OpenAI o200k_base and Llama 4 scale

## Mentioned in

- [[source - LLM Tokenizer Evolution]] — started at 200K
- [[source - Tokenizer Iteration Ranking]] — 1 iteration, "starting at finish line"

## Related

- [[MiniMax-Text-01]] — first open-source model
- [[MiniMax-M2]] — second model with same tokenizer

## Open questions

- Will MiniMax eventually increase vocabulary beyond 200K, or is this their long-term standard?
- How does MiniMax's tokenizer compare in multilingual efficiency to OpenAI's o200k_base?
