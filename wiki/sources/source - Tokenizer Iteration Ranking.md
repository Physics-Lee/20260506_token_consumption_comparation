---
type: source
raw_file: "note/tokenizer-iteration-ranking.md"
date_ingested: 2026-05-10
tags: [ranking, tokenizer, iteration, comparison]
---

# Source: Tokenizer Iteration Ranking

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** analysis note

## Summary

This note ranks major LLM companies by how many times they've substantially changed their tokenizer (algorithm change, vocabulary size change, or encoding change), excluding versions that merely reused the previous tokenizer.

Rankings: #1 OpenAI (5 times: gpt2→r50k→p50k→cl100k→o200k, 2019-2024), #2 Llama/Meta (3 times: 32K→128K→200K, 2023-2025), #3 Qwen/Alibaba (2 times: ~150K→151K→248K, 2023-2026), #4 GLM/Zhipu (2 times: ~130K→150K, 2022-2024), #5 DeepSeek (2 times: 32K→128K, 2024), #6 Kimi/Moonshot (1 time: closed→160K, 2023-2025), #7 MiniMax (1 time: 200K, 2025), #8 ByteDance/Seed (1 time: 155K, 2025). Anthropic is excluded—tokenizer never publicly disclosed.

Patterns observed: (1) longer-lived companies have more iterations, but annualized rate shows Llama (1.5/year) is more aggressive than OpenAI (0.83/year); (2) iteration count and jump magnitude are inversely correlated—DeepSeek changed once but jumped 4x, Qwen changed twice but the second jump was 63%; (3) 2025 entrants started at ≥160K, skipping the 32K trial-and-error phase; (4) non-iteration can mean maturity (MiniMax at 200K from day one) or conservatism (Qwen waited for community complaints before jumping).

## Key claims

- OpenAI has the most tokenizer iterations (5) but Llama has the highest annualized rate (1.5/year)
- Iteration count and jump magnitude are inversely correlated
- 2025 entrants (MiniMax, Kimi, ByteDance Seed) skipped the 32K phase, starting at 155K-200K
- Non-iteration can indicate either maturity (optimal from launch) or conservatism (resistant to change)
- Qwen is the most conservative established player (6 model generations, only 2 tokenizer changes)

## Entities mentioned

- [[OpenAI]] — 5 iterations
- [[Meta]] — Llama, 3 iterations
- [[Alibaba]] — Qwen, 2 iterations
- [[Zhipu AI]] — GLM, 2 iterations
- [[DeepSeek]] — 2 iterations
- [[Moonshot AI]] — Kimi, 1 iteration
- [[MiniMax]] — 1 iteration
- [[ByteDance]] — Seed, 1 iteration
- [[Anthropic]] — excluded (closed tokenizer)

## Concepts touched

- [[Tokenizer Iteration Rate]] — frequency of vocabulary/algorithm changes
- [[Jump Magnitude]] — proportional change in vocabulary size
- [[Market Entry Timing]] — later entrants can skip early evolutionary stages
- [[Conservatism vs Maturity]] — interpreting lack of tokenizer changes

## Notes

This ranking provides a useful meta-perspective on the tokenizer evolution data. The inverse correlation between iteration count and jump magnitude is an interesting finding that suggests different company strategies: frequent small adjustments vs rare large leaps. The distinction between "mature" (MiniMax at 200K from launch) and "conservative" (Qwen delaying change until community pressure) is a nuanced interpretation worth tracking as the field evolves.