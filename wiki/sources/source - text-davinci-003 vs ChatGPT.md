---
type: source
raw_file: "note/text-davinci-003-vs-chatgpt.md"
date_ingested: 2026-05-10
tags: [openai, text-davinci-003, chatgpt, instruct, comparison]
---

# Source: text-davinci-003 vs ChatGPT

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** comparison note

## Summary

This note compares text-davinci-003 and ChatGPT (gpt-3.5-turbo), two products launched in November 2022 that represented different paradigms. text-davinci-003 was an instruct model: instruction fine-tuned, prompt string input, weak refusal mechanism, tool-like output, $0.02/1K tokens, p50k_base encoding. ChatGPT was a chat model: RLHF-trained, messages array input, strong refusal, conversational output, $0.002/1K tokens (10x cheaper), cl100k_base encoding.

The training difference was crucial: text-davinci-003 stopped at supervised fine-tuning (SFT), while ChatGPT added human feedback scoring, reward model training, and PPO reinforcement learning. This RLHF step taught ChatGPT when to refuse, when to ask follow-up questions, and when to say "I don't know." The note clarifies that text-davinci-003 is not ChatGPT's predecessor—they were released simultaneously as different products. ChatGPT's true predecessor was the RLHF-naive base model before RLHF training.

The note also discusses davinci's remaining use cases: pure text completion (no "conversation" overhead), custom fine-tuning (before gpt-3.5-turbo fine-tuning opened in August 2023), and zero-shot reasoning (raw davinci sometimes outperformed RLHF models on pure intelligence tasks because alignment "dulled" reasoning sharpness). The evolution path from davinci → code-davinci-002 → SFT → RLHF → gpt-3.5-turbo is traced, with the key insight that code training on GitHub unexpectedly boosted general reasoning ability.

## Key claims

- text-davinci-003 and ChatGPT were launched simultaneously (Nov 2022) as different products, not predecessor-successor
- text-davinci-003: instruct model, SFT only, $0.02/1K, p50k_base
- ChatGPT: chat model, SFT + RLHF, $0.002/1K, cl100k_base
- RLHF added safety behavior, not conversation capability (SFT already had that)
- davinci was 10x more expensive than gpt-3.5-turbo; OpenAI priced ChatGPT aggressively to capture market
- code-davinci-002 was the common ancestor of both instruct and chat lineages

## Entities mentioned

- [[OpenAI]] — all models
- [[text-davinci-003]] — instruct model
- [[ChatGPT]] — chat model (gpt-3.5-turbo)
- [[Codex]] — code-davinci-002, common ancestor
- [[InstructGPT]] — research predecessor

## Concepts touched

- [[Instruct vs Chat]] — two different model paradigms
- [[RLHF]] — Reinforcement Learning from Human Feedback
- [[SFT]] — Supervised Fine-Tuning
- [[Model Distillation]] — how gpt-3.5-turbo achieved 10x lower pricing
- [[Code Training for Reasoning]] — unexpected generalization from code to reasoning

## Notes

This is one of the most detailed notes in the collection. The pricing analysis ($0.02 vs $0.002) and strategic explanation (OpenAI underpriced ChatGPT to lock in developers) is insightful. The observation that raw davinci sometimes outperforms RLHF models on pure reasoning tasks is a nuanced point about the tradeoffs of alignment. The traced evolution path (davinci → code-davinci-002 → text-davinci-003 / gpt-3.5-turbo) is historically accurate per the cited InstructGPT paper.