---
type: concept
source_count: 8
last_updated: 2026-05-10
tags: [multilingual, token-efficiency, cjk, chinese, compression]
---

# Multilingual Token Efficiency

How effectively different languages are compressed by LLM tokenizers, measured in characters or bytes per token.

## Overview

Token efficiency varies dramatically across languages due to training corpus composition and vocabulary design. English, being the dominant language in most training data, typically achieves the best compression (~1.3 chars/token). Chinese historically fared worse (~0.6 chars/token) because tokenizers were trained primarily on English text, causing Chinese characters to be split into subword fragments.

The project's central hypothesis concerns Classical Chinese (文言文): despite having the highest information density among natural languages, it may actually be less token-efficient than Modern Chinese or English. Modern tokenizers are trained on contemporary text; Classical Chinese characters and grammatical patterns are treated as rare Unicode sequences, causing excessive subword splitting.

Vocabulary expansion has improved multilingual efficiency over time. OpenAI's o200k_base (200K) improved CJK efficiency by 30-50% over cl100k_base (100K). Chinese models like DeepSeek (~1.3 chars/token) and Qwen (C-Eval: 60.8% efficiency) have narrowed the gap significantly by training tokenizers on Chinese-centric corpora.

## Key perspectives

- **Information density ≠ Token density**: A language can pack more meaning per character while requiring more tokens per character
- **Training corpus bias**: Tokenizers reflect their training data. English-heavy training produces English-efficient tokenizers.
- **Vocabulary expansion helps**: Larger vocabularies (100K→200K) can encode more multilingual patterns as single tokens

## Evidence and data

| Language | Typical chars/token | Notes |
|----------|-------------------|-------|
| English | ~1.3 | Baseline efficiency |
| Spanish | ~1.2 | Slightly less efficient than English |
| Modern Chinese | ~0.6 | Historical baseline for non-English-centric tokenizers |
| Classical Chinese | ~0.8-1.0 (theoretical) | May be worse in practice due to subword splitting |
| DeepSeek Chinese | ~1.3 | Near-English efficiency with Chinese-trained tokenizer |
| Qwen Chinese | 60.8% (C-Eval) | Best among domestic Chinese models |

- o200k_base CJK improvement: 30-50% over cl100k_base
- Qwen 3.5's 248K vocab (+63%) driven by community complaints about Hindi/Italian/German efficiency
- Llama 3's switch to tiktoken was motivated by poor multilingual performance in Llama 2 (32K SentencePiece)

## Contradictions and debates

- Classical Chinese may be split into more tokens than Modern Chinese despite higher information density
- "Optimal" efficiency depends on corpus alignment, not just vocabulary size
- Some languages (Hindi, Italian, German) remain underrepresented even in 200K vocabularies
- Community pressure (Qwen Issue #1400) can drive vocabulary expansion

## Sources

- [[source - Project Overview and Logic]] — core hypothesis about Classical Chinese
- [[source - LLM Tokenizer Evolution]] — vocabulary expansion driven by multilingual needs
- [[source - Tokenizer Names]] — Chinese model efficiency claims
- [[source - OpenAI Encoder Naming]] — o200k_base CJK improvement
- [[source - Plan vs Reality]] — JS vs Python path alignment for correct token counts

## Related

- [[Tokenization]] — the process of converting text to tokens
- [[Vocabulary Size]] — how vocabulary scale affects multilingual compression
- [[Byte Pair Encoding]] — the algorithm whose training corpus determines efficiency
- [[Classical Chinese]] — the specific language variant at the center of the project's hypothesis