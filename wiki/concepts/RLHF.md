---
type: concept
source_count: 4
last_updated: 2026-05-10
tags: [rlhf, alignment, training, safety]
---

# RLHF

Reinforcement Learning from Human Feedback, a training technique that shapes model behavior to align with human preferences.

## Overview

RLHF is the key differentiator between instruct models and chat models. While both undergo supervised fine-tuning (SFT) on instruction-following data, chat models add an RLHF phase where human annotators rate model outputs, a reward model is trained to predict these ratings, and the base model is optimized via reinforcement learning (typically PPO) to maximize predicted human preference.

RLHF teaches models behaviors that SFT alone cannot: when to refuse harmful requests, when to ask clarifying questions, when to express uncertainty, and how to adopt a conversational tone. The InstructGPT paper (2022) demonstrated that a 1.3B parameter model with RLHF could outperform a 175B parameter base model in human evaluations—showing that alignment matters more than scale.

OpenAI is unique among major LLM providers for having maintained separate instruct and chat product lines. Other companies (Anthropic, Google, Meta, Chinese providers) launched chat-native models directly, skipping the instruct-only phase.

## Key perspectives

- **RLHF adds safety, not capability**: The base model already knows how to converse after SFT; RLHF adds the judgment of when to refuse, hedge, or ask questions
- **Tradeoff**: Some studies suggest RLHF can slightly reduce raw reasoning performance (model becomes "too careful")
- **InstructGPT legacy**: OpenAI's research proved RLHF works, then applied it to production models (text-davinci-003 → gpt-3.5-turbo)

## Evidence and data

- InstructGPT 1.3B with RLHF > davinci 175B without RLHF (human preference)
- ChatGPT launched November 2022; API delayed until March 2023 due to RLHF safety testing
- text-davinci-003 (instruct, no RLHF): $0.02/1K tokens
- gpt-3.5-turbo (chat, with RLHF): $0.002/1K tokens (10x cheaper)

## Contradictions and debates

- RLHF may reduce performance on pure reasoning tasks (model becomes "too aligned" to give direct answers)
- The "intermediate" model (SFT after code training, before RLHF) was never publicly released—OpenAI may have wanted to prevent bypassing safety layers
- Today's "Instruct" models (e.g., Llama-Instruct) are actually chat-finetuned, not OpenAI-style instruct models

## Sources

- [[source - Instruct vs Chat]] — RLHF as the key differentiator
- [[source - text-davinci-003 vs ChatGPT]] — parallel products, different training
- [[source - text-davinci-003 vs ChatGPT]] — code-davinci-002 as common ancestor

## Related

- [[Instruct vs Chat Models]] — two paradigms separated by RLHF
- [[Supervised Fine-Tuning]] — the prerequisite step before RLHF
- [[PPO]] — Proximal Policy Optimization, the RL algorithm typically used
- [[Alignment]] — the broader goal of making models behave according to human values