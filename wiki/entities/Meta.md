---
type: entity
entity_type: organization
source_count: 5
last_updated: 2026-05-10
tags: [meta, llama, open-source, tokenizer]
---

# Meta

Technology company that created the Llama open-source LLM family.

## Overview

Meta (formerly Facebook) released the Llama model series, one of the most influential open-source LLM families. Llama 1 and 2 (2023) used SentencePiece BPE with 32K vocabulary. Llama 3 (2024) made a watershed change: switching from SentencePiece to OpenAI's tiktoken BPE format with 128K vocabulary. Llama 4 (2025) expanded further to 200K vocabulary, matching OpenAI's o200k_base scale.

The switch to tiktoken in Llama 3 was driven by poor multilingual tokenization in Llama 2—non-English text was frequently split into fragments. The 4x vocabulary expansion dramatically improved multilingual compression rates.

## Key facts

- Llama 1/2 (2023): 32K vocab, SentencePiece BPE
- Llama 3 (2024): 128K vocab, tiktoken BPE — algorithm switch
- Llama 4 (2025): 200K vocab, tiktoken BPE — added reasoning and vision special tokens
- Llama has the highest annualized tokenizer iteration rate (1.5/year) among major families
- "Llama-Instruct" models are chat-finetuned, despite the "Instruct" name

## Mentioned in

- [[source - LLM Tokenizer Evolution]] — detailed evolution timeline
- [[source - Tokenizer Iteration Ranking]] — 3 iterations, highest annualized rate
- [[source - Tokenizer Browser Strategy]] — Llama versions in timeline selector
- [[source - Tokenizer Names]] — SentencePiece to tiktoken transition

## Related

- [[Llama]] — Meta's open-source LLM family
- [[SentencePiece]] — Google's tokenizer framework used by early Llama
- [[tiktoken]] — OpenAI's tokenizer format adopted by Llama 3+

## Open questions

- Will Llama maintain tiktoken compatibility or diverge in future versions?
- How does Llama 4's 200K vocabulary compare to OpenAI's o200k_base in CJK efficiency?