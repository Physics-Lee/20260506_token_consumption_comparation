---
type: source
raw_file: "note/openai-encoder-naming.md"
date_ingested: 2026-05-10
tags: [openai, encoding, naming, history]
---

# Source: OpenAI Encoder Naming Explained

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** reference note

## Summary

This note decodes OpenAI's four encoder naming format: {prefix}{number}_base. Prefixes indicate product era: r = raw (GPT-3 early, davinci/curie/babbage/ada), p = prompt (instruct era, text-davinci-003/Codex), cl = Chat Language (ChatGPT era, GPT-3.5/GPT-4), o = omni (GPT-4o era, 2024+). Numbers indicate vocabulary size in thousands: 50K for r50k/p50k, 100K for cl100k, 200K for o200k.

The _base suffix indicates the general-purpose version, distinguishing from variants like p50k_edit (for the deprecated Edit API). OpenAI chose encoding-feature naming over product naming because encodings outlive products—GPT-3 may be deprecated but r50k_base remains understandable.

The timeline shows: 2020 r50k_base (davinci series), 2021 p50k_base (text-davinci-003/Codex, added GitHub code to training corpus), 2022 cl100k_base (GPT-3.5/GPT-4, chat-optimized), 2024 o200k_base (GPT-4o/GPT-5.x, multimodal + multilingual, CJK efficiency improved 30-50% over cl100k). Notably, 4 encodings cover all 60+ OpenAI models—encoding_for_model() is just a name-to-encoding lookup.

## Key claims

- OpenAI encoder names follow {prefix}{vocab_size}_base format
- Prefixes mark product eras: r=raw, p=prompt, cl=Chat Language, o=omni
- Vocabulary sizes doubled twice: 50K → 100K → 200K
- o200k_base improves CJK token efficiency by 30-50% over cl100k_base
- Encoding names use feature-based naming because encodings outlive products
- 4 encodings cover 60+ models; model-to-encoding is a simple lookup table

## Entities mentioned

- [[OpenAI]] — creator of all encodings
- [[GPT-3]] — r50k_base era
- [[Codex]] — p50k_base era
- [[ChatGPT]] — cl100k_base era
- [[GPT-4o]] — o200k_base era

## Concepts touched

- [[Encoder Naming]] — how tokenizer encodings are named
- [[Vocabulary Size]] — number of tokens in an encoding's vocabulary
- [[Product Era]] — how encoding prefixes map to OpenAI product generations
- [[CJK Token Efficiency]] — token compression for Chinese/Japanese/Korean text

## Notes

This is the clearest explanation of OpenAI encoder naming in the notes. The CJK efficiency improvement claim (30-50% for o200k over cl100k) is significant for the project's core hypothesis about Classical Chinese tokenization. The observation that encoding names outlive products is a good insight into OpenAI's API design philosophy.