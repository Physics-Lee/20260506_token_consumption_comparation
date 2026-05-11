---
type: concept
source_count: 5
last_updated: 2026-05-10
tags: [model-paradigm, instruct, chat, openai, training]
---

# Instruct vs Chat Models

Two distinct product paradigms for language models: instruct models follow single-turn commands; chat models engage in multi-turn conversations with role awareness.

## Overview

In OpenAI's ecosystem, instruct and chat represent genuinely different products. Instruct models (text-davinci-003) were instruction-fine-tuned only, accepted prompt strings, had weak refusal mechanisms, and produced tool-like output. Chat models (gpt-3.5-turbo) added RLHF, used messages arrays with system/user/assistant roles, had strong refusal, and produced conversational output.

The distinction originated from OpenAI's first-mover status: they evolved naturally from text completion (2020) → instruction following (2021) → conversation (2022). Later companies (Anthropic, Google, Meta, DeepSeek, Qwen) jumped directly to chat-native models.

Today, the terminology has blurred. Meta's "Llama-Instruct" models are actually chat-finetuned (support roles, refuse unsafe requests). When the industry says "Instruct model" now, it generally means "instruction-finetuned version" as opposed to a raw base model—not the specific OpenAI instruct product paradigm.

## Key perspectives

- **OpenAI's unique path**: Only OpenAI maintained separate instruct and chat product lines simultaneously
- **Training difference**: Instruct = SFT only; Chat = SFT + RLHF
- **API format**: Instruct = prompt string; Chat = messages array
- **Behavior**: Instruct = tool-like, direct; Chat = conversational, may ask follow-up questions

## Evidence and data

| Feature | text-davinci-003 | gpt-3.5-turbo |
|---------|-----------------|---------------|
| Training | SFT | SFT + RLHF |
| Input | Prompt string | Messages array |
| Multi-turn | Manual | Native |
| Refusal | Weak | Strong |
| Tone | Tool-like | Conversational |
| Price | $0.02/1K | $0.002/1K |
| Encoding | p50k_base | cl100k_base |
| Status | Deprecated 2024 | Active |

## Contradictions and debates

- text-davinci-003 was not ChatGPT's "predecessor"—they launched simultaneously as different products
- Raw davinci (without RLHF) sometimes outperforms RLHF models on pure reasoning tasks
- OpenAI's pricing strategy ($0.002 for gpt-3.5-turbo, 10x cheaper than davinci) effectively killed the instruct product line before official deprecation

## Sources

- [[source - Instruct vs Chat]] — cross-company comparison
- [[source - text-davinci-003 vs ChatGPT]] — detailed product comparison
- [[source - OpenAI API Timeline]] — chronological evolution
- [[source - What is Davinci]] — model naming and lineage

## Related

- [[RLHF]] — the key differentiator between instruct and chat
- [[Supervised Fine-Tuning]] — common prerequisite for both
- [[Messages Format]] — system/user/assistant role structure
- [[text-davinci-003]] — the canonical instruct model
- [[ChatGPT]] — the canonical chat model