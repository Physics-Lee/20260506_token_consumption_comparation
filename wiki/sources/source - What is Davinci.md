---
type: source
raw_file: "note/what-is-davinci.md"
date_ingested: 2026-05-10
tags: [openai, davinci, gpt-3, history]
---

# Source: What is Davinci

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** reference note

## Summary

This note explains that "davinci" has three distinct meanings in OpenAI's ecosystem. First, GPT-3 base model (2020): the largest of four scientist-named models (ada 350M, babbage 1.3B, curie 6.7B, davinci 175B). The naming logic orders scientists by perceived complexity of contribution: Ada Lovelace → Charles Babbage → Marie Curie → Leonardo da Vinci. This davinci used r50k_base encoding.

Second, GPT-3.5 instruct model (2022): text-davinci-001/002/003 were instruction-fine-tuned versions. text-davinci-003 was the most mature and is considered ChatGPT's immediate predecessor. These used p50k_base encoding, not r50k—an easily confused point.

Third, post-2023 reuse: davinci-002 (2023) is a completely different model using cl100k_base encoding, not the original GPT-3 davinci. The note shows tiktoken's MODEL_TO_ENCODING mapping, demonstrating that models sharing the "davinci" name use three different encodings.

## Key claims

- "davinci" has three distinct meanings across OpenAI's history
- Original davinci (2020): 175B GPT-3 base model, r50k_base
- text-davinci-003 (2022): instruct model, p50k_base, ChatGPT predecessor
- davinci-002 (2023): entirely new model, cl100k_base
- Scientists were named in order of contribution "complexity": ada → babbage → curie → davinci

## Entities mentioned

- [[OpenAI]] — all davinci variants
- [[Ada Lovelace]] — namesake of ada model
- [[Charles Babbage]] — namesake of babbage model
- [[Marie Curie]] — namesake of curie model
- [[Leonardo da Vinci]] — namesake of davinci model

## Concepts touched

- [[Model Naming]] — how OpenAI named its model tiers
- [[Encoding Mapping]] — model name to tokenizer encoding lookup
- [[Model Lineage]] — evolution from base to instruct to chat models

## Notes

This note is essential for understanding the tokenizer selector in index.html. The project includes "davinci" as an option representing the earliest GPT-3 era (r50k_base), allowing comparison of token efficiency from 2020 to 2024. The confusion between davinci variants is a common pitfall when analyzing OpenAI's historical APIs.