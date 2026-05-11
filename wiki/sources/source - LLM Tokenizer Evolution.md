---
type: source
raw_file: "note/llama-qwen-deepseek-tokenizer-evolution.md"
date_ingested: 2026-05-10
tags: [llama, qwen, deepseek, glm, kimi, minimax, tokenizer-evolution, 2026]
---

# Source: LLM Tokenizer Evolution (May 2026)

**Author:** Yixuan Li
**Date:** 2026-05
**Type:** research synthesis

## Summary

This note tracks tokenizer evolution across major LLM families as of May 2026. Llama (Meta): 32K SentencePiece (1/2, 2023) → 128K tiktoken (3, 2024) → 200K tiktoken (4, 2025). Key转折: Llama 3 switched to OpenAI's tiktoken system due to poor multilingual performance in Llama 2; Llama 4 added reasoning and vision special tokens. Qwen (Alibaba): ~150K BBPE (1.0-3, 2023-2025) → 248K BBPE (3.5, 2026), a 63% jump driven by community complaints about poor token efficiency for Hindi, Italian, and German. DeepSeek: 32K (V2, 2024.05) → 128K (V3, 2024.12), the most dramatic single jump (4x), then unchanged through R1/V3.1/V3.2/V4.

GLM (Zhipu): unique approach of merging self-trained Chinese/multilingual BPE with OpenAI's cl100k_base as English base, creating a 150K hybrid vocabulary. Kimi (Moonshot): closed K1 (2023) → open K2 (2025.07) with 160K tiktoken-based vocabulary and explicit Chinese regex optimization. MiniMax: launched directly at 200K (2025.01), no changes since. ByteDance/Doubao: completely closed (algorithm, vocab size, special tokens all undisclosed).

Key patterns: (1) 32K is proven inadequate—no current model is below 128K; (2) each major jump correlates with training corpus diversification; (3) after jumping, vocabularies stabilize because changing tokenizer requires retraining all embedding layers; (4) the industry is converging on ~200K (Llama 4, Qwen 3.5, MiniMax, OpenAI o200k); (5) DeepSeek at 128K is the most conservative and may jump next.

## Key claims

- 32K vocabulary is proven inadequate for multilingual models; no current major model is below 128K
- Llama 3 switched from SentencePiece to tiktoken; Llama 4 reached 200K
- Qwen 3.5 jumped 63% to 248K, the largest proportional increase among established series
- DeepSeek's V2→V3 jump (32K→128K, 4x) was the most dramatic single change
- GLM uniquely merged self-trained Chinese BPE with OpenAI's cl100k_base English base
- Industry converging on ~200K vocabulary; Doubao is the only fully closed Chinese tokenizer

## Entities mentioned

- [[Meta]] — Llama series
- [[Alibaba]] — Qwen series
- [[DeepSeek]] — DeepSeek series
- [[Zhipu AI]] — GLM/ChatGLM series
- [[Moonshot AI]] — Kimi series
- [[MiniMax]] — MiniMax series
- [[ByteDance]] — Doubao (closed)
- [[OpenAI]] — cl100k_base (used by GLM), o200k_base
- [[HuggingFace]] — model repository and configuration source

## Concepts touched

- [[Tokenizer Evolution]] — how vocabularies change across model generations
- [[Vocabulary Size Convergence]] — industry trend toward ~200K vocabularies
- [[SentencePiece vs tiktoken]] — two major tokenizer frameworks
- [[Hybrid Vocabulary]] — GLM's unique merge of self-trained and OpenAI vocabularies
- [[Multilingual Token Efficiency]] — driving force behind vocabulary expansion

## Notes

This is the most up-to-date and comprehensive tokenizer evolution note in the collection. All claims are sourced to official repositories, papers, and documentation. The May 2026 timestamp makes this a current snapshot—the field evolves rapidly. The observation that DeepSeek (128K) is below the industry convergence point (~200K) suggests a potential future jump. The Doubao closure is a significant limitation for the project's comparison scope.