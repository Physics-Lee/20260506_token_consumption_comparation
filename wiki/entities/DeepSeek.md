---
type: entity
entity_type: organization
source_count: 6
last_updated: 2026-05-10
tags: [deepseek, chinese-llm, tokenizer, open-source]
---

# DeepSeek

Chinese AI company (深度求索) known for efficient open-source LLMs with industry-leading Chinese tokenization.

## Overview

DeepSeek produces open-source large language models with exceptional Chinese token efficiency (~1.3 chars/token, approaching English levels). The tokenizer underwent one dramatic change: DeepSeek-V2 (May 2024) used 32K Byte-level BPE, while DeepSeek-V3 (December 2024) jumped to 128K—a 4x increase, the most dramatic single jump among major LLM families.

The V3 technical report explicitly states the motivation: "The tokenizer for DeepSeek-V3 employs Byte-level BPE with an extended vocabulary of 128K tokens. The pretokenizer and training data are modified to optimize multilingual compression efficiency." This jump added more math, programming, and multilingual content to the training corpus. From V3 through R1, V3.1, V3.2, and V4, the tokenizer has remained unchanged at 128K.

## Key facts

- DeepSeek-V2 (2024.05): 32K Byte-level BPE
- DeepSeek-V3 (2024.12): 128K Byte-level BPE — 4x jump
- DeepSeek-R1 through V4: all use V3's 128K tokenizer unchanged
- Chinese token efficiency: ~1.3 chars/token (near English levels)
- transformers 5.x breaks DeepSeek Chinese tokenization; version 4.57 is required

## Mentioned in

- [[source - LLM Tokenizer Evolution]] — most dramatic single jump (4x)
- [[source - Tokenizer Iteration Ranking]] — 2 iterations, largest jump magnitude
- [[source - Plan vs Reality]] — transformers 5.x breaking change
- [[source - Tokenizer Browser Strategy]] — DeepSeek versions in timeline selector
- [[source - Project Overview and Logic]] — DeepSeek tokenizer used for testing

## Related

- [[DeepSeek-V3]] — model with 128K tokenizer
- [[DeepSeek-R1]] — reasoning model using V3's tokenizer
- [[Byte-level BPE]] — algorithm used by DeepSeek

## Open questions

- Will DeepSeek make the next jump to ~200K to match industry convergence, or stay at 128K?
- How does the transformers 5.x breaking change affect future DeepSeek tokenizer compatibility?