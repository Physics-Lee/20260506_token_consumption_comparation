---
type: source
raw_file: "note/gpt1-vs-later-tokenizers.md"
date_ingested: 2026-05-10
tags: [gpt-1, gpt-2, bpe, history, tokenization]
---

# Source: GPT-1 vs Later Tokenizers

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** historical comparison

## Summary

This note compares GPT-1's tokenizer with GPT-2 and later. GPT-1 (2018) used a hybrid approach: spaCy for word-level tokenization first, with BPE as a fallback for out-of-vocabulary words. GPT-2+ uses pure byte-level BPE with no external dependencies. The consequences were severe: GPT-1 had OOV (out-of-vocabulary) problems, poor multilingual support (spaCy is English-centric), weak Unicode/emoji handling, and required spaCy as a preprocessing dependency.

GPT-2's pure BPE solved all of these: no OOV (all characters are in 256-byte range), natural multilingual support (bytes are language-agnostic), strong Unicode/emoji handling, and zero external dependencies. The core shift was from "words are the base unit, BPE is a patch" to "bytes are the base unit, BPE is everything." This made the tokenizer a pure mathematical algorithm capable of handling code, math, emoji, and any symbol system.

## Key claims

- GPT-1 used spaCy word-level tokenization + BPE fallback; GPT-2+ uses pure byte-level BPE
- GPT-1 had OOV problems, poor multilingual support, and required spaCy dependency
- GPT-2's byte-level approach eliminated OOV, enabled multilingual, and removed dependencies
- The shift was fundamental: word-based → byte-based base unit
- Pure BPE can handle code, math, emoji, and any byte-representable symbol system

## Entities mentioned

- [[OpenAI]] — GPT-1, GPT-2, and subsequent models
- [[spaCy]] — NLP library used by GPT-1 for word tokenization

## Concepts touched

- [[Word-Level Tokenization]] — splitting text into words before subword processing
- [[Byte-Level BPE]] — operating on bytes rather than characters or words
- [[OOV Problem]] — out-of-vocabulary words that cannot be directly encoded
- [[Language-Agnostic Tokenization]] — tokenization independent of specific language features

## Notes

This historical note contextualizes why modern tokenizers (including those used in this project) all use byte-level approaches. The GPT-1 → GPT-2 transition was a paradigm shift that influenced all subsequent LLM tokenization. The note's conclusion that pure BPE "can handle any human-invented symbol system" is particularly relevant for the project's Classical Chinese corpus.