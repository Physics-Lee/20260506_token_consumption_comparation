---
type: source
raw_file: "note/This_code_is_all_you_need_for_openai_tokenzier.md"
date_ingested: 2026-05-11
tags: [tiktoken, source-code, model-mapping, prefix-matching]
---

# Source: Tiktoken model.py Mapping

**Author:** Yixuan Li
**Date:** ~2026-05
**Type:** source code analysis

## Summary

This note contains the complete MODEL_PREFIX_TO_ENCODING and MODEL_TO_ENCODING dictionaries from tiktoken's model.py, with Chinese annotations explaining the prefix matching logic.

MODEL_PREFIX_TO_ENCODING handles model families by prefix: o1-/o3-/o4-mini- → o200k_base; gpt-5-/gpt-4.5-/gpt-4.1-/chatgpt-4o-/gpt-4o- → o200k_base; gpt-4-/gpt-3.5-turbo-/gpt-35-turbo- → cl100k_base; gpt-oss- → o200k_harmony; ft:gpt-4o → o200k_base; ft:gpt-4 → cl100k_base.

MODEL_TO_ENCODING handles exact model names: o1/o3/o4-mini → o200k_base; gpt-5/gpt-4.1/gpt-4o → o200k_base; gpt-4/gpt-3.5-turbo → cl100k_base; davinci-002/babbage-002 → cl100k_base; text-embedding-ada-002/text-embedding-3-* → cl100k_base; text-davinci-003/002 → p50k_base; text-davinci-001/davinci/curie/babbage/ada → r50k_base; code-davinci-002/001/cushman → p50k_base; text-davinci-edit-001 → p50k_edit; gpt2/gpt-2 → gpt2.

The prefix matching resolves questions about why gpt-5.4/gpt-5.5 aren't in MODEL_TO_ENCODING: they are handled by "gpt-5-" prefix. gpt-oss-* uses "gpt-oss-" prefix → o200k_harmony. The note clarifies that the matching logic depends on actual API naming conventions—if OpenAI uses "gpt-5.4-2025-xx-xx" format, the prefix hits; if "gpt-5.4" without hyphen, it depends on implementation details.

## Key claims

- tiktoken uses two lookup tables: exact match (MODEL_TO_ENCODING) and prefix match (MODEL_PREFIX_TO_ENCODING)
- All gpt-5.* models map to o200k_base via "gpt-5-" prefix
- gpt-oss-* uses experimental o200k_harmony encoding
- Fine-tuned models (ft:) map to their base model's encoding
- Deprecated models remain in the mapping table permanently for backward compatibility

## Entities mentioned

- [[OpenAI]] — tiktoken library
- [[tiktoken]] — model.py source code

## Concepts touched

- [[Model-to-Encoding Mapping]] — how model names resolve to tokenizer encodings
- [[Prefix Matching]] — handling model families without listing every version
- [[Backward Compatibility]] — deprecated models kept in mapping tables

## Notes

This is a primary source—the actual tiktoken/model.py code with annotations. It provides definitive answers about which encoding any OpenAI model uses. The note's explanation of prefix matching is particularly valuable for understanding how new model versions are handled without library updates.
