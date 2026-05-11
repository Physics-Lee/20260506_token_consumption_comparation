---
type: concept
source_count: 4
last_updated: 2026-05-10
tags: [tokenizer, special-tokens, bos, eos, role-markers]
---

# Special Tokens

Non-text tokens injected by tokenizers to mark boundaries, roles, and control signals in model inputs.

## Overview

Special tokens are reserved token IDs that don't correspond to regular text fragments. They serve structural purposes: marking the beginning/end of sequences (BOS/EOS), delimiting conversation roles (user, assistant, system), and signaling control operations (masking, tool calls, reasoning steps).

Different model families use different special token conventions. OpenAI GPT-4o+ uses `<|endoftext|>` and `<|endofprompt|>`. ChatGLM uses `[MASK]`, `[gMASK]`, `[sMASK]`, plus `<|user|>`, `<|assistant|>`. Qwen uses `<|im_start|>`, `<|im_end|>` for role boundaries. DeepSeek uses full-width vertical bars: `<｜end▁of▁sentence｜>`, `<｜User｜>`, `<｜Assistant｜>`. Yi follows LLaMA conventions with `</s>` and `Human:`/`Assistant:` prefixes.

The handling of special tokens is a key reason why simply downloading tokenizer.json is insufficient for correct tokenization—tokenizer_config.json is also needed to map special token strings to their IDs. The plan to implement pure-JS tokenization was blocked by this realization.

## Key perspectives

- **Config-dependent**: Special token mappings are stored in tokenizer_config.json, not the vocabulary itself
- **Model-specific**: Each model family has its own convention, making cross-model comparison more complex
- **Injection timing**: Special tokens are added before/after the BPE merge process, not derived from it

## Evidence and data

| Model | EOS | Role Markers | Other |
|-------|-----|-------------|-------|
| OpenAI GPT-4o+ | `<|endoftext|>` | None (ChatML uses JSON role field) | `<|endofprompt|>` |
| ChatGLM | `<|endoftext|>` | `<|user|>` `<|assistant|>` `<|system|>` `<|observation|>` | `[MASK]` `[gMASK]` `[sMASK]` |
| Qwen | `<|endoftext|>` | `<|im_start|>` user `<|im_end|>` | `<|extra_0|>` to `<|extra_204|>` |
| DeepSeek | `<｜end▁of▁sentence｜>` | `<｜User｜>` `<｜Assistant｜>` | Full-width `｜` instead of `|` |
| Yi | `</s>` | `Human:` `Assistant:` | LLaMA-style |
| Baichuan | `</s>` | `<reserved_106>` `<reserved_107>` | Numeric role IDs |

## Contradictions and debates

- Some models (Doubao) keep all special token details completely hidden
- The diversity of conventions complicates building universal tokenizer tools
- JS-only tokenization requires parsing tokenizer_config.json, not just tokenizer.json

## Sources

- [[source - Plan vs Reality]] — special token handling as blocker for JS-only path
- [[source - Tokenizer Names]] — special token naming comparison table
- [[source - Tiktokenizer Source Analysis]] — tiktoken's special token injection mechanism

## Related

- [[Tokenizer Config]] — tokenizer_config.json metadata file
- [[BPE]] — the merge algorithm that operates on regular text tokens
- [[ChatML]] — OpenAI's messages format that uses JSON roles instead of special tokens
