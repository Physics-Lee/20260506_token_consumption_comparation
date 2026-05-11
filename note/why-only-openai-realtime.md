# 为什么只有 OpenAI 的 tokenizer 能浏览器端实时计算

## 不是技术限制，是没人打包

OpenAI 和其他公司的 tokenizer 文件格式几乎一样——都是 BPE 词表 + merges 表。技术上，Qwen/DeepSeek 的 `tokenizer.json` 完全可以被编译成和 gpt-tokenizer 一样的 UMD JS 包。

但这件事需要有人做，而只有 OpenAI 的那四套有人做了。

## gpt-tokenizer 的来历

- 作者：Bazyli Brzoska（GitHub: niieani），**独立开发者，不是 OpenAI 员工**
- 做的事：把 OpenAI 开源的 tiktoken（Python/Rust）用纯 JS 重写，词表编译进 JS 文件，上传 npm 和 jsdelivr CDN
- 产物：4 个 UMD 文件（o200k_base.js / cl100k_base.js / p50k_base.js / r50k_base.js），每个 ~2MB
- 动机：让前端开发者不用 WASM、不用后端就能算 token 数

## OpenAI 官方提供什么

| 官方产物 | 语言 | 能浏览器端用吗 |
|----------|------|:---:|
| `tiktoken` | Python | ❌ |
| `tiktoken-rs` | Rust | ❌ |
| `tiktoken` WASM | Rust → WASM | ⚠️ 能，但有跨域限制 |
| 官方 JS 版 | — | ❌ 不存在 |

OpenAI 从来没有发布过浏览器端 JS tokenizer。gpt-tokenizer 是社区作品。

## 类比

```
OpenAI tiktoken (Python)  ──→  niieani 用 JS 重写  ──→  gpt-tokenizer CDN ✅

Qwen tokenizer.json       ──→  没人用 JS 重写        ──→  无 CDN ❌
DeepSeek tokenizer.json   ──→  没人用 JS 重写        ──→  无 CDN ❌
Llama tokenizer.json      ──→  没人用 JS 重写        ──→  无 CDN ❌
GLM tokenizer.model       ──→  没人用 JS 重写        ──→  无 CDN ❌
```

每套词表都能做，只是没人动手。
