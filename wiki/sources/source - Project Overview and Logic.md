---
type: source
raw_file: "note/20260508_1915_logic.md"
date_ingested: 2026-05-10
tags: [project-overview, tokenization, multilingual]
---

# Source: Project Overview and Logic

**Author:** Yixuan Li
**Date:** 2026-05-08
**Type:** project note

## Summary

This note provides the overarching rationale for the token consumption comparison project. The core hypothesis being tested is whether Classical Chinese (文言文), as the language with the highest information density, actually consumes fewer tokens during LLM tokenization. The project is structured around a 4x4 matrix: four articles, each translated into four language versions (Classical Chinese, Modern Chinese, English, and Spanish).

The four articles are: "Zuo Zhuan: Duke Wen of Jin's Exile" (originally Classical Chinese), Paul Graham's "Writers and Non-Writers" (originally English), Allende's Last Speech (originally Spanish), and Chen-Ning Yang's argument against building a super collider (originally Modern Chinese). This design ensures each article has one "original" language and three translations, enabling cross-language comparison while controlling for content.

The data pipeline flows from translation text files (.txt) through generate_json.py to structured JSON data, then through json2html.py to an interactive HTML reader (corpus_reader.html). Two analysis scripts support the project: analyze_tokens.py provides theoretical estimates of compression efficiency across languages, while test_tokenizer.py performs actual encoding using tiktoken (OpenAI) and transformers (DeepSeek) to measure real token counts.

The project's working assumption, captured in code comments, is that while Classical Chinese has high information density, this does not necessarily translate to high token density. Modern tokenizers are trained primarily on modern text, so Classical Chinese may be split into multiple subword tokens, potentially making English or Modern Chinese more token-efficient in practice.

## Key claims

- Classical Chinese has the highest information density among the four languages tested
- Modern tokenizers are trained primarily on modern text, causing Classical Chinese to be treated as rare Unicode and split into subword tokens
- English or Modern Chinese may be more token-efficient than Classical Chinese in practice, despite lower information density
- The 4x4 article matrix design controls for content while enabling cross-language comparison

## Entities mentioned

- [[Paul Graham]] — author of one of the test articles
- [[Salvador Allende]] — subject of one of the test articles
- [[Chen-Ning Yang]] — author of one of the test articles
- [[OpenAI]] — provider of GPT tokenizers
- [[DeepSeek]] — provider of open-source tokenizers tested

## Concepts touched

- [[Tokenization]] — the process of converting text into token sequences
- [[Information Density]] — the amount of meaning per unit of text
- [[BPE]] — Byte Pair Encoding, the algorithm used by modern tokenizers
- [[Subword Tokenization]] — splitting words into smaller units

## Notes

This note serves as the project's foundational document. The hypothesis about Classical Chinese token efficiency remains the central research question. The note predates the more detailed implementation plans in other notes.