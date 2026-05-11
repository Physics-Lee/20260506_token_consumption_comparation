---
type: entity
entity_type: product
source_count: 10
last_updated: 2026-05-10
tags: [tiktoken, openai, tokenizer-library, python, wasm]
---

# tiktoken

OpenAI's official fast BPE tokenizer library, available in Python and as a Rust/WASM build.

## Overview

tiktoken is OpenAI's official tokenizer library, providing fast BPE tokenization for all OpenAI models. The Python version is a thin wrapper around a Rust core. The Rust implementation can also be compiled to WASM (~2-3MB) for browser use, as demonstrated by tiktokenizer.vercel.app.

tiktoken encodes all OpenAI model names to their corresponding encodings via a lookup table (MODEL_TO_ENCODING). Since 60+ models reuse only 4 encodings (gpt2, r50k_base, p50k_base, cl100k_base, o200k_base), this mapping is simple and compact.

A key design principle: all historical encodings are permanently preserved, even after their corresponding models are deprecated. This ensures historical token sequences remain decodable and enables cross-era comparison.

## Key facts

- Python binding wraps Rust core for performance
- WASM build (~2-3MB) enables browser tokenization
- 4 main encodings: r50k_base, p50k_base, cl100k_base, o200k_base
- 60+ models map to these 4 encodings via MODEL_TO_ENCODING table
- Deprecated models marked in code but never removed from mappings
- encoding_for_model() does model name → encoding name lookup
- get_encoding() loads encoding directly by name

## Mentioned in

- [[source - Tiktokenizer Source Analysis]] — WASM build and architecture
- [[source - Tokenizer Workflow Note]] — how BPE runs inside tiktoken
- [[source - OpenAI Encoder Naming]] — encoding naming conventions
- [[source - What is Davinci]] — MODEL_TO_ENCODING mapping
- [[source - Why Deprecated Models Still Work]] — permanent encoding preservation
- [[source - Tokenizer Tools]] — tiktoken in various tools
- [[source - text-davinci-003 vs ChatGPT]] — different encodings for different models

## Related

- [[OpenAI]] — tiktoken's creator
- [[Tiktokenizer]] — browser tool using tiktoken WASM
- [[BPE]] — algorithm implemented by tiktoken
- [[WASM]] — WebAssembly target for browser use

## Open questions

- Will tiktoken add support for non-OpenAI encodings in the future?
- How does tiktoken's Rust implementation compare in performance to pure Python BPE?
