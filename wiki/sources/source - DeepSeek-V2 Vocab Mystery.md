---
type: source
raw_file: "note/deepseek-v2-vocab-mystery.md"
date_ingested: 2026-05-11
tags: [deepseek, vocabulary, huggingface, configuration]
---

# Source: DeepSeek-V2 Vocab Mystery

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** investigation note

## Summary

This note resolves an apparent contradiction in DeepSeek-V2's vocabulary size. HuggingFace's `DeepseekV2Config` class shows `vocab_size: int = 32000`, while the V2 paper states "vocabulary size of 100K." The investigation reveals that 32000 is merely a Python class default value (placeholder), not the actual model parameter. When loading the real model, `config.json` overrides this to 100K.

The root cause: HuggingFace automatically generates documentation from Config class defaults, causing search engines and doc pages to display 32000 as if it were the model's actual vocabulary. DeepSeek-V2's actual vocabulary is 100K—same as V1, unchanged.

## Key claims

- HuggingFace `Config` class default values (32000) are placeholders, not model parameters
- DeepSeek-V2's actual vocabulary is 100K, matching the paper and config.json override
- Auto-generated documentation from Config classes can mislead by showing placeholder defaults
- DeepSeek-V2 did NOT change vocabulary from V1

## Entities mentioned

- [[DeepSeek]] — DeepSeek-V2 model
- [[HuggingFace]] — transformers library Config class

## Concepts touched

- [[Config Class Defaults]] — placeholder values in ML library code
- [[Vocabulary Size]] — actual vs documented values
- [[Auto-Generated Documentation]] — pitfalls of deriving docs from code defaults

## Notes

This finding corrects an error in [[source - Tokenizers Is All You Need]] which lists DeepSeek-R1 as "~100K BPE." If DeepSeek-V2 was 100K (not 32K as some sources claim), then the V2→V3 jump (to 128K) was smaller than initially thought—28% rather than 4x. This substantially changes the narrative of "most dramatic single jump." The V3 technical report's claim of "extended vocabulary of 128K tokens" should be re-examined in light of V2 actually being 100K, not 32K.

This contradicts [[source - LLM Tokenizer Evolution]] and [[source - Tokenizer Iteration Ranking]] which both describe the V2→V3 jump as "32K → 128K, 4x." The true progression may be 100K → 128K (28% increase), which is far less dramatic. However, the note author states "DeepSeek-V2 词表 = 100K，和 V1 同一套，完全没改"—this raises the question of what V1's vocabulary was.
