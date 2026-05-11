---
type: source
raw_file: "note/tokenizer-names.md"
date_ingested: 2026-05-10
tags: [tokenizer, naming, chinese-llm]
---

# Source: Tokenizer Names and Meanings

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** reference note

## Summary

This note decodes the names and philosophies behind major tokenizer algorithms and Chinese LLM tokenizers. Algorithm names reveal design philosophy: BPE (Byte Pair Encoding, bottom-up frequency merge), BBPE (byte-level variant), WordPiece (likelihood-gain merge, used by BERT), SentencePiece (Google's language-agnostic wrapper treating all text as byte stream), Unigram (top-down pruning, probability-based), and tiktoken (OpenAI's library, "Tik" = token谐音).

Chinese LLM tokenizer names and their vocabularies: Qwen (阿里巴巴, BBPE, 151K→248K, "Question + answer"), ChatGLM (智谱AI, SentencePiece BBPE, 130K→151K, with unique MASK tokens), Baichuan (百川智能, 64K→125K, "hundreds of rivers"暗示 data diversity), DeepSeek (深度求索, BPE, ~1.3 chars/token Chinese efficiency), Yi (零一万物, 64K, "一" = one,暗示 "one model for all languages"), YAYI (中科闻歌, 81,920, "refined insight", sized to be divisible by 128 for GPU tensor parallelism), InternLM (上海AI实验室, "intern"暗示 academic origin), XVERSE (元象科技, 100K, "universe" variant), ERNIE (百度, WordPiece, "Enhanced Representation through Knowledge Integration").

The note also covers special token naming conventions across models, highlighting DeepSeek's use of full-width vertical bars (｜) instead of pipes (|), and the fact that Doubao (字节跳动) is the only major Chinese model with a completely closed tokenizer—algorithm, vocab size, and special tokens are all undisclosed.

## Key claims

- Machine learning naming often reveals design philosophy; tokenizer names are no exception
- Chinese LLM tokenizers have culturally embedded naming (Qwen = 千问, Baichuan = 海纳百川)
- Doubao is the only major Chinese LLM with a completely closed/black-box tokenizer
- Special token conventions vary significantly across model families
- Algorithm comparison: BPE merges by frequency, WordPiece by likelihood gain, Unigram prunes by probability

## Entities mentioned

- [[OpenAI]] — tiktoken, cl100k_base, o200k_base
- [[Meta]] — Llama, SentencePiece
- [[Alibaba]] — Qwen
- [[Zhipu AI]] — ChatGLM/GLM
- [[DeepSeek]] — DeepSeek tokenizer
- [[01.AI]] — Yi (李开复)
- [[ByteDance]] — Doubao (唯一闭源 tokenizer)
- [[Baidu]] — ERNIE
- [[MiniMax]] — MiniMax tokenizer
- [[Moonshot AI]] — Kimi tokenizer
- [[Baichuan]] — Baichuan tokenizer

## Concepts touched

- [[BPE]] — Byte Pair Encoding
- [[BBPE]] — Byte-level BPE
- [[WordPiece]] — BERT's likelihood-based merge algorithm
- [[SentencePiece]] — Google's language-agnostic tokenizer wrapper
- [[Unigram]] — Top-down pruning algorithm
- [[Special Tokens]] — EOS, role markers, and model-specific tokens
- [[Tokenizer Naming Conventions]] — how names encode design intent

## Notes

This is a remarkably comprehensive reference note. The observation that Doubao is the only fully closed tokenizer among major Chinese LLMs is significant for the project's scope—Doubao cannot be included in tokenization comparisons. The vocabulary size progression (150K→248K for Qwen, 32K→128K for DeepSeek) is tracked in more detail in [[source - LLM Tokenizer Evolution]].