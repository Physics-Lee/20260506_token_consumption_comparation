# 分词器（Tokenizer）介绍

corpus_reader.html 内置了 10 种 OpenAI 分词器和 6 种开源分词器，用于对比词元消耗。

---

## OpenAI 分词器（实时计算）

所有 OpenAI 模型共用 4 种底层编码（BPE 词汇表）。`gpt-tokenizer` 库在浏览器端实时计算，无需服务器。

### o200k_base（GPT-4o 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| gpt-4o | GPT-4o / GPT-4o-mini |
| gpt-4.1 | GPT-4.1 / GPT-4.1-mini / GPT-4.1-nano |
| o200k_base | 直接使用编码 |

**特点**：2024 年后 OpenAI 的新编码。词汇表更大（~200K tokens），非英文语言（中日韩文）的压缩效率显著优于旧编码。例如中文文本在 o200k_base 下 token 数通常比 cl100k_base 少 30-50%。

### cl100k_base（GPT-4 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| gpt-4 | GPT-4 / GPT-4-turbo / GPT-4-32k |
| gpt-3.5-turbo | GPT-3.5-turbo |
| cl100k_base | 直接使用编码 |

**特点**：2022-2023 年的主流编码。词汇表 ~100K tokens。目前仍被 text-embedding-3 系列和旧版 GPT-4 使用。

### p50k_base（Codex 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| text-davinci-003 | GPT-3.5 指令模型（2022 年） |
| p50k_base | 直接使用编码 |

**特点**：2021-2022 年使用的编码。词汇表 ~50K tokens。主要用于对比旧编码与新编码的差异。

### r50k_base（GPT-3 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| davinci | GPT-3 基础模型（2020 年） |
| r50k_base | 直接使用编码 |

**特点**：最早的 GPT-3 编码。词汇表 ~50K tokens。用于历史对比参考。

---

## 开源模型分词器（预计算）

通过 HuggingFace 的 tokenizer.json 预计算词元数，嵌入 HTML 中直接读取。需要先运行 `node code/precompute_tokens.js` 生成数据。

| 选择器名称 | HuggingFace 模型 | 编码类型 | 词汇量 |
|-----------|-----------------|---------|--------|
| DeepSeek-R1 | deepseek-ai/DeepSeek-R1 | BPE | ~100K |
| Llama-3-8B | meta-llama/Meta-Llama-3-8B | BPE (SentencePiece) | ~128K |
| Llama-3-70B | meta-llama/Meta-Llama-3-70B | BPE (SentencePiece) | ~128K |
| Qwen2.5-72B | Qwen/Qwen2.5-72B | BPE | ~152K |
| Phi-2 | microsoft/phi-2 | BPE | ~50K |
| Gemma-7B | google/gemma-7b | SentencePiece | ~256K |

### 编码对比意义

不同分词器的核心差异在于**词汇表的构造方式**：

| 对比维度 | 说明 |
|---------|------|
| **词汇量大小** | 词汇表越大，常见词越可能作为单 token，token 数越少 |
| **多语言支持** | o200k_base 对中文的压缩率显著优于 cl100k_base（中文 token 更少） |
| **代码支持** | p50k_base 对代码的 tokenization 效率较好（Codex 训练时优化） |
| **文言文** | 各编码对文言文的处理差异显著——文言文字符数虽少，但 token 数未必更省 |

### 加载方式：CDN + UMD 全局变量

#### OpenAI 分词器：jsDelivr CDN → UMD 构建

`gpt-tokenizer` npm 包为每种编码单独构建了 UMD 文件，可以直接用 `<script>` 标签加载：

```html
<!-- 4 个独立的 UMD 构建，各 ~2MB -->
<script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/o200k_base.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/cl100k_base.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/p50k_base.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/r50k_base.js"></script>
```

每个文件加载后，在 `window`（`globalThis`）上注册一个全局变量：

| 文件 | 全局变量 | 内含函数 |
|------|---------|---------|
| `o200k_base.js` | `GPTTokenizer_o200k_base` | `.encode(text)` → `number[]` |
| `cl100k_base.js` | `GPTTokenizer_cl100k_base` | `.encode(text)` → `number[]` |
| `p50k_base.js` | `GPTTokenizer_p50k_base` | `.encode(text)` → `number[]` |
| `r50k_base.js` | `GPTTokenizer_r50k_base` | `.encode(text)` → `number[]` |

这些 UMD 文件是 **纯 JavaScript**（非 WASM），内含完整的 BPE 编码表。每个文件约 2MB，首次访问后浏览器自动缓存到 disk cache，之后秒开。

#### 调用方式

```javascript
// 编码映射表：选择器值 → 全局编码器对象
const ENCODERS = {
    'gpt-4o':    GPTTokenizer_o200k_base,
    'gpt-4':     GPTTokenizer_cl100k_base,
    'davinci':   GPTTokenizer_r50k_base,
    // ...
};

// 计算 token 数
function countTokens(text, tokenizerName) {
    const encoder = ENCODERS[tokenizerName];
    return encoder.encode(text).length;  // 返回 token 个数
}
```

#### 为什么用 UMD 而不是 ES Module？

第一版尝试用 `<script type="importmap">` + `import { encode } from 'gpt-tokenizer'`，但 `gpt-tokenizer` 的默认导出只包含一种编码（o200k_base），无法切换。而 npm 包的 UMD 构建目录下，每种编码都有独立文件且暴露不同的全局变量，正好解决编码切换问题。

#### 开源模型分词器：预计算嵌入 JSON

```html
<script>
    window.PRECOMPUTED_TOKENS = {
        "open_source": {
            "DeepSeek-R1": {
                "allende": { "spanish": 523, "classical_chinese": 412, ... },
                ...
            }
        }
    };
</script>
```

无需额外下载，直接读取内存中的预计算数据。数据由 `code/precompute_tokens.js` 在构建时生成。

### 计算原理

所有上述分词器都使用 **BPE（Byte Pair Encoding）** 算法，本质是：
1. 将文本拆为字节序列
2. 反复查找最高频的相邻字节对并合并
3. 直到无法再合并为止
4. 查 vocab 表得到 token ID

整个过程是**确定性查表操作**，不涉及 AI 推理，所以在浏览器端可以毫秒级完成。
