# Tiktokenizer 源码实现拆解

> 源码: https://github.com/dqbd/tiktokenizer
> 技术栈: Next.js + T3 Stack + TypeScript
> 关键依赖: `tiktoken` (WASM) + `@xenova/transformers` (浏览器端 HuggingFace) + `graphemer` (字符边界)

---

## 两条 Tokenizer 路径

### 路径一：OpenAI 系列 → `tiktoken` npm 包（WASM）

```
选择模型 "gpt-4o" 或编码 "cl100k_base"
        ↓
TiktokenTokenizer 类
        ↓
import { get_encoding, encoding_for_model } from "tiktoken"
        ↓
WASM 二进制（~2-3MB，编译自 Rust 版 tiktoken）
  内含所有编码表（逻辑内嵌，不是 JSON 文件）:
    · cl100k_base  → GPT-4 / GPT-3.5 / text-embedding-3
    · o200k_base   → GPT-4o / GPT-4.1
    · p50k_base    → Codex / Davinci
    · r50k_base    → GPT-3
        ↓
this.enc.encode(text) → token IDs
```

**支持 30+ OpenAI 模型的原因**: 全部复用 4 种编码，`encoding_for_model()` 只做模型名→编码名的映射。

关键源码 (`src/models/tokenizer.ts`):
```typescript
export class TiktokenTokenizer implements Tokenizer {
  private enc: Tiktoken;

  constructor(model) {
    // gpt-3.5-turbo / gpt-4 → cl100k_base + 特殊 token 注入
    // gpt-4o → o200k_base + 特殊 token 注入
    // 其他 → encoding_for_model(model) 自动映射
    this.enc = get_encoding("cl100k_base", {
      "<|im_start|>": 100264,
      "<|im_end|>": 100265,
      "<|im_sep|>": 100266,
    });
  }

  tokenize(text: string): TokenizerResult {
    const tokens = [...(this.enc?.encode(text, "all") ?? [])];
    return { name: this.name, tokens, count: tokens.length };
  }
}
```

### 路径二：开源模型 → `@xenova/transformers`（词汇表文件）

```
选择模型 "deepseek-ai/DeepSeek-R1" 等
        ↓
OpenSourceTokenizer 类
        ↓
构建时（src/scripts/download.ts）:
  从 HuggingFace 下载 tokenizer.json + tokenizer_config.json
  → 存入 public/hf/{org}/{model}/
        ↓
运行时:
  PreTrainedTokenizer.from_pretrained(model)  ← transformers.js
  env.remotePathTemplate = "/hf/{model}"      ← 走 Vercel 代理避免 CORS
  tokenizer.json (1-5MB) → 浏览器内存
        ↓
this.tokenizer.encode(text) → token IDs
```

关键源码 (`src/models/tokenizer.ts`):
```typescript
export class OpenSourceTokenizer implements Tokenizer {
  static async load(model): Promise<PreTrainedTokenizer> {
    if (typeof window !== "undefined") {
      env.remoteHost = window.location.origin;       // localhost / vercel
    }
    env.remotePathTemplate = "/hf/{model}";           // 代理路径
    return await PreTrainedTokenizer.from_pretrained(model);
  }

  tokenize(text: string): TokenizerResult {
    const tokens = this.tokenizer.encode(text);
    return { name: this.name, tokens, count: tokens.length };
  }
}
```

### 构建时下载脚本 (`src/scripts/download.ts`)

```typescript
// 遍历所有开源模型，从 HuggingFace 下载词汇表文件
for (const modelName of openSourceModels) {
  const [orgId, modelId] = modelName.split("/");
  for (const file of ["tokenizer.json", "tokenizer_config.json"]) {
    // → public/hf/codellama/CodeLlama-7b-hf/tokenizer.json
    await fetch(`https://huggingface.co/${orgId}/${modelId}/resolve/main/${file}`);
    await fs.writeFile(targetPath, response);
  }
}
// 部署时 打包进 Vercel 静态资源
```

---

## 可视化层

```
分词结果: [15496, 995, 13, 220, ...]
        ↓
逐个 token → decode_single_token_bytes() → 拼回文本字节
        ↓
graphemer 按视觉字符边界切分（处理 emoji、多字节字符）
        ↓
输出: [
  { text: "hello", tokens: [{id:15496, idx:0}] },
  { text: " world", tokens: [{id:995, idx:1}] },
  ...
]
        ↓
前端按 token 边界着色高亮渲染
```

---

## 架构一览

```
                    用户选择模型
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
    OpenAI 模型                      开源模型
         │                               │
    tiktoken npm                    download.ts
    (WASM, ~2-3MB)                构建时下载词汇表
    · cl100k_base                  tokenizer.json (1-5MB)
    · o200k_base                         │
    · p50k_base                   PreTrainedTokenizer
    · r50k_base                   (transformers.js)
         │                               │
         ▼                               ▼
   encode(text)                    encode(text)
         │                               │
         └───────────────┬───────────────┘
                         ▼
                  token ID 数组
                         │
               getTiktokenSegments()
            或 getHuggingfaceSegments()
                  (graphemer 切分)
                         │
                    着色渲染
```

---

## 关键结论

| 问题 | 答案 |
|------|------|
| 数据存在哪 | OpenAI: WASM 二进制内嵌；开源的: 构建时下载 JSON 到 public/ |
| 运算在哪跑 | **全部在浏览器**（WASM 或 JS），0 后端调用 |
| 花钱吗 | **不花钱**，不需要任何 API key，纯静态站点 |
| 为什么支持几十种 | OpenAI 30+ 模型复用 4 种编码；开源的每个只需一个 tokenizer.json |
| 每次输入要重跑吗 | **是的**，但 BPE 算法 O(n)，几百字只需几毫秒 |
| 词汇表多大 | OpenAI WASM ~2-3MB；开源 tokenizer.json 每个 1-5MB |
