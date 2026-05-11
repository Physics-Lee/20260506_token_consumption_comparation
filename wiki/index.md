# Wiki Index

Content-oriented catalog of all wiki pages.

## Sources

Project notes and research materials from `note/`.

### Project Overview & Planning
- [[source - Project Overview and Logic]] — Core hypothesis: does Classical Chinese save tokens?
- [[source - Token Comparison Implementation Plan]] — Original plan for tokenizer selector UI
- [[source - Update Workflow]] — Build pipeline and deployment process
- [[source - Why Single Pipeline]] — Decision to consolidate json2html.py + build_index.py
- [[source - Plan vs Reality]] — Gap between planned JS-only path and actual Python implementation
- [[source - Pipeline Diagnosis and Fix]] — Fixing broken build pipeline

### Implementation Details
- [[source - Theme System Preference]] — Three-state (light/dark/system) CSS theme implementation
- [[source - How to Change Card Order]] — Fixed language card ordering (文言→现代汉语→English→Español)
- [[source - How Character Counting Works]] — Unicode code point counting in Python
- [[source - Language Choice]] — Why code/ stays pure Python
- [[source - Font Choice]] — Noto Sans/Noto Serif SC selection rationale
- [[source - Bug - Font Loading]] — github.io font inconsistency and fix
- [[source - Responsive Design]] — CSS media query breakpoints and mobile layout

### Tokenizer Fundamentals
- [[source - Tokenizer Workflow Note]] — How tokenizers work (merges + vocab tables)
- [[source - BPE Termination]] — Training vs inference termination conditions
- [[source - Tokenizer Names]] — Decoding tokenizer algorithm and Chinese LLM names
- [[source - Tokenizer Tools]] — Survey of 10+ tokenizer visualization tools
- [[source - Tiktokenizer Source Analysis]] — Architecture of tiktokenizer.vercel.app
- [[source - Tokenizer Browser Strategy]] — Precomputation strategy for browser display
- [[source - How to Implement Timeline Selector]] — Migration guide for version timeline UI

### OpenAI History & Encodings
- [[source - OpenAI Encoder Naming]] — r/p/cl/o prefix meanings and vocabulary progression
- [[source - OpenAI API Timeline]] — 2020-2024 chronological release history
- [[source - What is Davinci]] — Three meanings of "davinci" across OpenAI history
- [[source - GPT-1 vs Later Tokenizers]] — Evolution from spaCy to pure byte-level BPE
- [[source - GPT-2 vs r50k_base]] — Two eras, similar size, different corpora
- [[source - r50k_base vs p50k_base]] — Code corpus driving encoding divergence
- [[source - text-davinci-003 vs ChatGPT]] — Parallel product lines, different training
- [[source - Instruct vs Chat]] — Why only OpenAI had this distinction
- [[source - text-embedding-ada-002]] — Embedding model distinct from GPT-3 ada
- [[source - Davinci-002 and Embedding Encoding]] — Why "old" names use new encodings
- [[source - Why Deprecated Models Still Work]] — Tokenizer/model independence

### LLM Tokenizer Evolution
- [[source - LLM Tokenizer Evolution]] — Cross-family evolution as of May 2026
- [[source - Tokenizer Iteration Ranking]] — Companies ranked by tokenizer change frequency

---

## Entities

Pages about specific organizations, models, and tools.

### Companies
- [[OpenAI]] — GPT family creator, tiktoken library, 5 tokenizer iterations
- [[HuggingFace]] — Model hub and transformers library
- [[Meta]] — Llama family (32K→128K→200K)
- [[Alibaba]] — Qwen family (150K→248K)
- [[DeepSeek]] — DeepSeek family (32K→128K, most dramatic jump)
- [[Zhipu AI]] — GLM/ChatGLM (unique hybrid vocabulary)
- [[Moonshot AI]] — Kimi (closed K1→open K2)
- [[MiniMax]] — Started at 200K, no changes since
- [[ByteDance]] — Doubao (only fully closed Chinese tokenizer)
- [[Anthropic]] — Claude (chat-native, tokenizer never disclosed)

### Tools & Libraries
- [[tiktoken]] — OpenAI's fast BPE tokenizer (Python/Rust/WASM)
- [[Tiktokenizer]] — Browser visualization tool by dqbd

---

## Concepts

Pages about ideas, methods, and theories.

### Tokenization
- [[Byte Pair Encoding]] — Dominant subword tokenization algorithm
- [[Tokenization]] — Text-to-token conversion process
- [[Vocabulary Size]] — Vocabulary capacity and tradeoffs (50K→200K)
- [[Special Tokens]] — BOS, EOS, role markers, control signals
- [[Multilingual Token Efficiency]] — Cross-language compression rates
- [[OpenAI Encoding Timeline]] — r50k→p50k→cl100k→o200k evolution

### Model Paradigms
- [[RLHF]] — Reinforcement Learning from Human Feedback
- [[Instruct vs Chat Models]] — Two training/product paradigms

### Implementation
- [[CSS Custom Properties]] — Dynamic theming with CSS variables
- [[Precomputation]] — Ahead-of-time token counting for static data

---

*Index last updated: 2026-05-10*
