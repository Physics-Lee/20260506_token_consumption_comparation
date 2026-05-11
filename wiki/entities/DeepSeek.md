---
type: entity
entity_type: organization
source_count: 7
last_updated: 2026-05-11
tags: [deepseek, chinese-llm, tokenizer, open-source]
---

# DeepSeek

Chinese AI company (深度求索) known for efficient open-source LLMs with industry-leading Chinese tokenization.

## Overview

DeepSeek produces open-source large language models with exceptional Chinese token efficiency (~1.3 chars/token, approaching English levels). The tokenizer underwent one change: DeepSeek-V2 (May 2024) used 100K Byte-level BPE (not 32K—HuggingFace's DeepseekV2Config shows a placeholder default of 32000 that is overridden by config.json), while DeepSeek-V3 (December 2024) expanded to 128K. If V2 was indeed 100K, the V2→V3 jump was ~28%, not the 4x previously assumed. However, some sources continue to describe V2 as 32K, creating ambiguity.

The V3 technical report explicitly states the motivation: "The tokenizer for DeepSeek-V3 employs Byte-level BPE with an extended vocabulary of 128K tokens. The pretokenizer and training data are modified to optimize multilingual compression efficiency." This jump added more math, programming, and multilingual content to the training corpus. From V3 through R1, V3.1, V3.2, and V4, the tokenizer has remained unchanged at 128K.

## Key facts

- DeepSeek-V2 (2024.05): 100K Byte-level BPE (paper claim; HuggingFace config shows placeholder 32000)
- DeepSeek-V3 (2024.12): 128K Byte-level BPE — 28% increase if V2 was 100K
- DeepSeek-R1 through V4: all use V3's 128K tokenizer unchanged
- Chinese token efficiency: ~1.3 chars/token (near English levels)
- transformers 5.x breaks DeepSeek Chinese tokenization; version 4.57 is required

## Mentioned in

- [[source - LLM Tokenizer Evolution]] — most dramatic single jump (4x)
- [[source - Tokenizer Iteration Ranking]] — 2 iterations, largest jump magnitude
- [[source - Plan vs Reality]] — transformers 5.x breaking change
- [[source - Tokenizer Browser Strategy]] — DeepSeek versions in timeline selector
- [[source - DeepSeek-V2 Vocab Mystery]] — investigation revealing V2 vocab may be 100K not 32K
- [[source - Project Overview and Logic]] — DeepSeek tokenizer used for testing

## Related

- [[DeepSeek-V3]] — model with 128K tokenizer
- [[DeepSeek-R1]] — reasoning model using V3's tokenizer
- [[Byte-level BPE]] — algorithm used by DeepSeek

## Open questions

- Was DeepSeek-V2 actually 100K or 32K? The paper says 100K but many sources repeat 32K
- Will DeepSeek make the next jump to ~200K to match industry convergence, or stay at 128K?
- How does the transformers 5.x breaking change affect future DeepSeek tokenizer compatibility?