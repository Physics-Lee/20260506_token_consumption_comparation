---
type: entity
entity_type: organization
source_count: 2
last_updated: 2026-05-10
tags: [anthropic, claude, closed-source, safety]
---

# Anthropic

AI safety company founded by former OpenAI researchers, creator of the Claude LLM family.

## Overview

Anthropic is unique among major LLM providers for two reasons: it was chat-native from day one (no instruct phase), and its tokenizer has never been publicly disclosed. Claude models have only ever offered a messages API—no pure text completion endpoint.

Anthropic's training approach emphasizes "helpful, harmless, honest" (HHH) alignment from the start. The company was founded by Dario and Daniela Amodei and several other former OpenAI researchers who left due to disagreements about AI safety and commercialization.

## Key facts

- Founded by former OpenAI researchers (Dario Amodei, Daniela Amodei, et al.)
- Claude was chat-native from launch—no instruct-only product ever existed
- Tokenizer never publicly disclosed: algorithm, vocab size, and special tokens are all unknown
- API only offers messages format (no completions endpoint)
- Excluded from tokenizer iteration ranking due to complete opacity

## Mentioned in

- [[source - Instruct vs Chat]] — only chat-native from day one
- [[source - LLM Tokenizer Evolution]] — only fully closed tokenizer among Western major LLMs
- [[source - Tokenizer Iteration Ranking]] — excluded due to undisclosed tokenizer

## Related

- [[Claude]] — Anthropic's LLM family
- [[Constitutional AI]] — Anthropic's alignment approach

## Open questions

- Will Anthropic ever disclose its tokenizer, or will it remain permanently closed?
- How does Claude's undisclosed tokenizer compare to known tokenizers in multilingual efficiency?
