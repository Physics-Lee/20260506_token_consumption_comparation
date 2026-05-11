---
type: entity
entity_type: organization
source_count: 3
last_updated: 2026-05-10
tags: [zhipu, glm, chatglm, chinese-llm, hybrid-tokenizer]
---

# Zhipu AI

Chinese AI company (智谱AI) from Tsinghua University, creator of the GLM and ChatGLM model families.

## Overview

Zhipu AI developed the GLM (General Language Model) series, notable for a unique tokenizer approach: GLM-4 merged self-trained Chinese/multilingual BPE vocabulary with OpenAI's cl100k_base English vocabulary into a 150K unified vocabulary. The ChatGLM paper explicitly describes this: "employ the byte-level BPE algorithm to separately learn Chinese and multilingual tokens, then merge them with the tokens of the cl100k_base tokenizer."

This hybrid approach is unique among major LLMs—no other company uses a competitor's vocabulary as a base component. GLM's vocabulary changed only once (from ~130K to 150K) across four generations (GLM-130B, ChatGLM-6B, ChatGLM2-6B, ChatGLM3-6B, GLM-4).

## Key facts

- GLM-130B (2022): ~130K vocab, BPE
- ChatGLM-6B/2/3 (2023): ~130K vocab, unchanged
- GLM-4 (2024): 150K vocab, hybrid BPE + cl100k_base merge
- Unique approach: using OpenAI's cl100k_base as English base, self-trained Chinese on top
- Three special MASK tokens: [MASK] (bidirectional), [gMASK] (autoregressive), [sMASK] (shared)

## Mentioned in

- [[source - LLM Tokenizer Evolution]] — hybrid vocabulary approach
- [[source - Tokenizer Iteration Ranking]] — 2 iterations
- [[source - Tokenizer Names]] — special token naming conventions

## Related

- [[GLM]] — General Language Model family
- [[ChatGLM]] — conversational variant
- [[cl100k_base]] — OpenAI encoding used as GLM-4's English base

## Open questions

- How does the hybrid vocabulary affect tokenization of mixed Chinese-English text?
- Will future GLM versions continue the hybrid approach or train entirely self-sufficient vocabularies?
