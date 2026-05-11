---
type: entity
entity_type: organization
source_count: 17
last_updated: 2026-05-11
tags: [openai, gpt, tokenizer, api]
---

# OpenAI

Creator of the GPT model family and the most widely used LLM tokenizers.

## Overview

OpenAI is an AI research and deployment company founded in 2015. It created the GPT (Generative Pre-trained Transformer) model series starting with GPT-1 in 2018, and has released successive generations: GPT-2 (2019), GPT-3 (2020), GPT-3.5 (2022), GPT-4 (2023), GPT-4o (2024), and GPT-5.x (2025+). OpenAI also developed the tiktoken library, the official Python binding for its BPE tokenizers.

OpenAI is unique among LLM providers for having gone through all three major product paradigms: base text completion (GPT-3), instruction following (text-davinci-003), and conversational AI (ChatGPT/gpt-3.5-turbo). This progression is reflected in its tokenizer evolution: four encodings (r50k_base, p50k_base, cl100k_base, o200k_base) cover 60+ models, with each encoding corresponding to a product era.

## Key facts

- Released GPT-3 API in June 2020 with four model tiers named after scientists: ada (350M), babbage (1.3B), curie (6.7B), davinci (175B)
- Launched ChatGPT web interface in November 2022; API followed in March 2023
- GPT-4 released March 2023; GPT-4o released May 2024 with o200k_base encoding
- GPT-5 series (2025+) also uses o200k_base; gpt-oss-* uses experimental o200k_harmony
- tiktoken library permanently preserves all historical encodings even after models are deprecated
- Pricing strategy for gpt-3.5-turbo ($0.002/1K tokens) was deliberately set at 1/10 of davinci's price to capture developer market
- tiktoken uses prefix matching (MODEL_PREFIX_TO_ENCODING) for new model versions without requiring library updates

## Mentioned in

- [[source - OpenAI Encoder Naming]] — encoding naming conventions
- [[source - OpenAI API Timeline]] — chronological release history
- [[source - What is Davinci]] — three meanings of "davinci"
- [[source - GPT-1 vs Later Tokenizers]] — shift from spaCy to pure BPE
- [[source - GPT-2 vs r50k_base]] — encoding evolution from GPT-2 to GPT-3
- [[source - r50k_base vs p50k_base]] — code-focused encoding divergence
- [[source - text-davinci-003 vs ChatGPT]] — parallel product lines
- [[source - Instruct vs Chat]] — model paradigm evolution
- [[source - text-embedding-ada-002]] — embedding models
- [[source - Davinci-002 and Embedding Encoding]] — encoding reuse across product lines
- [[source - Why Deprecated Models Still Work]] — tiktoken's permanent encoding preservation
- [[source - LLM Tokenizer Evolution]] — OpenAI as the industry reference point
- [[source - Tokenizer Iteration Ranking]] — 5 tokenizer iterations, highest count
- [[source - Tokenizers Is All You Need]] — comprehensive tokenizer reference for the project
- [[source - Tiktoken Model.py Mapping]] — MODEL_TO_ENCODING and MODEL_PREFIX_TO_ENCODING tables

## Related

- [[GPT]] — OpenAI's generative pre-trained transformer model family
- [[tiktoken]] — OpenAI's official tokenizer library
- [[ChatGPT]] — conversational AI product
- [[Codex]] — code generation model family

## Open questions

- Will o200k_base remain the standard through GPT-5.x and beyond, or will a new encoding emerge?
- How does OpenAI's closed-source approach to model weights contrast with the open-source trend in Chinese LLMs?