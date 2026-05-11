---
type: source
raw_file: "note/instruct-vs-chat.md"
date_ingested: 2026-05-10
tags: [instruct, chat, rlhf, openai, model-paradigm]
---

# Source: Instruct vs Chat

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** conceptual comparison

## Summary

This note distinguishes instruct and chat models within OpenAI's ecosystem and explains why other companies never maintained this distinction. In OpenAI's system, instruct models (text-davinci-003) use SFT only, accept prompt strings, don't natively support multi-turn conversation, have weak refusal, and produce tool-like output. Chat models (gpt-3.5-turbo) add RLHF, use messages arrays, support roles natively, have strong refusal, and produce conversational output.

Other companies skipped the instruct phase entirely. Anthropic's Claude was chat-native from day one with only messages API. Google's Gemini was chat-native from launch (PaLM 2 had text-bison and chat-bison, but Gemini unified to chat). Meta's Llama releases base + "Instruct" versions, but the "Instruct" suffix actually means chat-finetuned (supports system/user/assistant roles, refuses unsafe requests). Chinese companies (DeepSeek, Qwen) are all chat-native with messages-format APIs.

The note explains that OpenAI was the first LLM API provider, so its evolution was natural growth: 2020 "text continuation" → 2021 "follow instructions" → 2022 "have conversations." Later companies stood on OpenAI's shoulders and jumped directly to chat. Today, "Instruct model" generally means "instruction-finetuned version" (vs base model), not the specific OpenAI instruct product paradigm.

## Key claims

- OpenAI is the only company that maintained separate instruct and chat product lines
- Instruct: SFT only, prompt strings, weak refusal, tool-like; Chat: SFT+RLHF, messages, strong refusal, conversational
- Anthropic, Google, Meta, and Chinese companies all launched chat-native products
- Meta's "Llama-Instruct" naming is misleading—these are chat-finetuned models
- Today's "Instruct" usually means "instruction-finetuned vs base," not OpenAI's specific paradigm

## Entities mentioned

- [[OpenAI]] — text-davinci-003, gpt-3.5-turbo
- [[Anthropic]] — Claude (chat-native from day one)
- [[Google]] — Gemini, PaLM 2 (text-bison/chat-bison)
- [[Meta]] — Llama ("Instruct" = chat-finetuned)
- [[DeepSeek]] — chat-native
- [[Alibaba]] — Qwen (chat-native)

## Concepts touched

- [[Instruct Model]] — model fine-tuned to follow instructions
- [[Chat Model]] — model trained for multi-turn conversation with roles
- [[RLHF]] — the key differentiator between instruct and chat
- [[Messages Format]] — system/user/assistant role structure
- [[Product Evolution]] — how OpenAI's first-mover status shaped its product path

## Notes

This note provides important context for why the project's tokenizer comparisons focus on chat-era encodings (cl100k_base, o200k_base) rather than instruct-era encodings (p50k_base). The distinction between "Instruct" as a product paradigm (OpenAI-specific) and "instruct-finetuned" as a general model type is a subtle but important terminological point.