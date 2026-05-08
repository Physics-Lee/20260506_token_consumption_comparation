# 类似 tiktokenizer 的 Token 可视化工具

## 同类工具

| 工具 | 在线版 | 仓库 | 特点 |
|------|--------|------|------|
| **tiktokenizer** | https://tiktokenizer.vercel.app | https://github.com/dqbd/tiktokenizer | React + tiktoken (wasm)，直观的可视化拆分 |
| **GPT Tokenizer Playground** | https://gpt-tokenizer.dev/ | https://github.com/niieani/gpt-tokenizer | 全系列 OpenAI 模型（含 GPT-5.5），token 数 + 成本估算 + 上下文窗口占比。TypeScript 纯 JS 实现，无 wasm 依赖 |
| **LLM Tokenizer** | https://www.danieldemmel.me/tokenizer | — | 纯浏览器端（transformers.js），从 HuggingFace 动态加载任意 tokenizer，多模型并列对比，ruby annotation 显示 token ID |
| **HappyTokenizer** | https://happytokenizer.com/ | — | 面向开发者，侧重成本优化和上下文窗口管理 |
| **Tokenizer Visualizer** (Netlify) | https://tokenization-visualization.netlify.app/ | — | 支持 OpenAI、LLaMA、Mistral、BERT 等 tokenizer 切换 |
| **Interactive Tokenization Visualizer** | https://context-lab.com/llm-course/demos/tokenization/ | — | 教学向，GPT-2/BERT/T5 三栏并列对比，含 BPE 步骤动画 |
| **Tokenize It!** (HuggingFace) | https://orion-zhen-tokenize-it.hf.space/ | — | Gradio 搭建，显示 vocab size、special tokens |
| **BPE Tokenizer** (ExplainLLM) | https://explainllm.ru/en/playground/tokenizer | — | BPE 算法逐步可视化 |
| **Tokenizere** | https://tswira.com/playground/tokenizer | — | 轻量级，显示 token ID |
| **Himjoe's** | https://himjoe.github.io/tokenization_visualization/ | — | 简单直观的 token 拆分对比 |
| **OpenAI 官方** | https://platform.openai.com/tokenizer | — | 官方页面 |

## 分类

- **工程向**：gpt-tokenizer.dev、LLM Tokenizer、tiktokenizer（成本估算、多模型对比）
- **教学向**：context-lab（BPE 步骤动画）、ExplainLLM（算法可视化）
- **极简向**：Himjoe's、Tokenizere（轻量直观）

## 私货

- `gpt-tokenizer.dev` 最全，全系列 OpenAI 模型 + 实时成本估算
- `danieldemmel.me/tokenizer` 最灵活，从 HuggingFace 动态加载任意 tokenizer，多模型并列对比
- `context-lab.com` 最适合理解 BPE 算法本身
