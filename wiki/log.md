# Wiki Log

Chronological record of all wiki operations.

---

## [2026-05-10] ingest | Ingest all 33 note/ files into wiki

Bulk ingestion of the complete note/ directory. Created the full wiki structure from scratch.

### Source pages created (33)
- source - Project Overview and Logic
- source - Token Comparison Implementation Plan
- source - Update Workflow
- source - Why Single Pipeline
- source - Plan vs Reality
- source - Pipeline Diagnosis and Fix
- source - Theme System Preference
- source - How to Change Card Order
- source - How Character Counting Works
- source - Language Choice
- source - Font Choice
- source - Bug - Font Loading
- source - Responsive Design
- source - Tokenizer Workflow Note
- source - BPE Termination
- source - Tokenizer Names
- source - Tokenizer Tools
- source - Tiktokenizer Source Analysis
- source - Tokenizer Browser Strategy
- source - How to Implement Timeline Selector
- source - OpenAI Encoder Naming
- source - OpenAI API Timeline
- source - What is Davinci
- source - GPT-1 vs Later Tokenizers
- source - GPT-2 vs r50k_base
- source - r50k_base vs p50k_base
- source - text-davinci-003 vs ChatGPT
- source - Instruct vs Chat
- source - text-embedding-ada-002
- source - Davinci-002 and Embedding Encoding
- source - Why Deprecated Models Still Work
- source - LLM Tokenizer Evolution
- source - Tokenizer Iteration Ranking

### Entity pages created (12)
- OpenAI
- HuggingFace
- Meta
- Alibaba
- DeepSeek
- Zhipu AI
- Moonshot AI
- MiniMax
- ByteDance
- Anthropic
- tiktoken
- Tiktokenizer

### Concept pages created (10)
- Byte Pair Encoding
- Tokenization
- Vocabulary Size
- RLHF
- Instruct vs Chat Models
- Multilingual Token Efficiency
- Special Tokens
- CSS Custom Properties
- Precomputation
- OpenAI Encoding Timeline

### Key findings from ingestion
- Core hypothesis: Classical Chinese may NOT save tokens despite highest information density
- Plan vs Reality gap: JS-only path blocked by special token handling complexity
- Industry converging on ~200K vocabulary (Llama 4, Qwen 3.5, MiniMax, OpenAI o200k)
- DeepSeek has most dramatic single jump (32K→128K, 4x); Qwen most conservative (6 gens, 2 changes)
- Doubao (ByteDance) is only fully closed tokenizer among major Chinese LLMs
- OpenAI's 4 encodings cover 60+ models; encoding names outlive products

---

## [2026-05-11] ingest | Ingest 4 new note/ files + update existing pages

### New source pages created (4)
- source - Tokenizers Is All You Need — Complete tokenizer reference with UMD loading details
- source - Tiktoken Model.py Mapping — Full encoding mapping tables with prefix matching explanation
- source - Tokenizer Cache Locations — HuggingFace cache on user's Windows machine
- source - DeepSeek-V2 Vocab Mystery — V2 vocabulary may be 100K not 32K

### Entity pages updated
- [[DeepSeek]] — Added contradiction: V2 vocab is 100K (paper) vs 32K (HuggingFace Config default). Changes V2→V3 jump narrative from 4x to ~28%.
- [[OpenAI]] — Added gpt-oss-* using o200k_harmony, prefix matching system
- [[HuggingFace]] — Added cache locations and Config class default value pitfall

### Concept pages updated
- [[OpenAI Encoding Timeline]] — Added o200k_harmony for gpt-oss open-source models

### Key findings
- DeepSeek-V2 vocabulary contradiction: paper says 100K, HuggingFace DeepseekV2Config shows placeholder 32000
- If V2 was 100K, the "most dramatic jump" narrative (32K→128K, 4x) is incorrect—actual jump may be ~28%
- UMD builds of gpt-tokenizer are pure JS (not WASM), ~2MB per encoding, cached by browser
- tiktoken uses prefix matching (MODEL_PREFIX_TO_ENCODING) so new model versions don't require library updates
- All OpenAI models since GPT-4o share o200k_base; only exception is gpt-oss-* with o200k_harmony

### Contradictions found
- [[source - LLM Tokenizer Evolution]] and [[source - Tokenizer Iteration Ranking]] both claim DeepSeek V2→V3 was "32K→128K, 4x" — but [[source - DeepSeek-V2 Vocab Mystery]] shows V2 was likely 100K all along
- This affects the "most dramatic single jump" claim attributed to DeepSeek

### Suggested follow-ups
- Verify DeepSeek-V1 vocabulary size to confirm V1→V2→V3 progression
- Update project documentation if V2 was indeed 100K (not 32K)
- Monitor for new tokenizer versions (especially DeepSeek potential jump to 200K)
- Resolve HuggingFace firewall issue for precomputation
- Consider adding output page comparing tokenizer efficiency across all covered models
- Periodically lint for dead wikilinks as project evolves
