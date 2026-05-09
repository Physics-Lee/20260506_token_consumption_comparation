# 分词器（Tokenizer）介绍

corpus_reader.html 内置了 10 种 OpenAI 分词器和 6 种开源分词器，用于对比词元消耗。

---

## OpenAI 分词器（实时计算）

所有 OpenAI 模型共用 4 种底层编码（BPE 词汇表）。`gpt-tokenizer` 库在浏览器端实时计算，无需服务器。

> **总览来源**：[OpenAI tiktoken 官方仓库](https://github.com/openai/tiktoken) · [OpenAI Tokenizer 在线工具](https://platform.openai.com/tokenizer) · [gpt-tokenizer（JS 实现）](https://github.com/niieani/gpt-tokenizer)

#### 关于 OpenAI 官方的 Tokenizer 工具

[platform.openai.com/tokenizer](https://platform.openai.com/tokenizer) 是 OpenAI 官方提供的在线分词可视化工具。它的本质和 tiktokenizer.vercel.app 一样，都是 `tiktoken` 库的前端封装：

- **默认展示的编码**：基于当前页面上选择的模型自动匹配对应编码。例如选择 "gpt-4o"，它就展示 `o200k_base` 的分词效果；选择 "gpt-4"，展示 `cl100k_base`。
- **功能**：输入文本 → 实时高亮显示每个 token 的边界 → 显示 token 总数和每个 token 的具体 ID。
- **和本项目的关系**：本项目对比表中的词元数，等价于 OpenAI Tokenizer 工具里看到的 "Tokens" 数值——所不同的是本项目可以**一键切换编码**，对比同一段文本在不同编码下的 token 消耗。

### o200k_base（GPT-4o / o 系列 / GPT-5.x 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| gpt-4o | GPT-4o / GPT-4o-mini |
| gpt-4.1 | GPT-4.1 / GPT-4.1-mini / GPT-4.1-nano |
| gpt-4.5 | GPT-4.5 |
| o200k_base | 直接使用编码 |

**o 系列推理模型和 GPT-5.x 也全部使用 o200k_base**：

| 系列 | 模型 | 编码 | 来源 |
|------|------|------|------|
| o 系列 | o1 / o1-mini / o1-pro / o3 / o3-mini / o4-mini | `o200k_base` | [tiktoken/model.py#L14-L18](https://github.com/openai/tiktoken/blob/main/tiktoken/model.py#L14-L18) |
| GPT-5.x | gpt-5 / gpt-5-mini / gpt-5-nano / gpt-5-pro / gpt-5.1 | `o200k_base` | [tiktoken/model.py#L20](https://github.com/openai/tiktoken/blob/main/tiktoken/model.py#L20) · [Issue #464](https://github.com/openai/tiktoken/issues/464) |

也就是说，自 2024 年 GPT-4o 发布以来，OpenAI 所有新模型（包括推理模型 o1/o3 和最新的 GPT-5 系列）**全部共用 o200k_base 这一种编码**。唯一的例外是 `gpt-oss-*` 系列（开源模型）使用了实验性的 `o200k_harmony` 编码。

**特点**：词汇表更大（~200K tokens），非英文语言（中日韩文）的压缩效率显著优于旧编码。例如中文文本在 o200k_base 下 token 数通常比 cl100k_base 少 30-50%。

> **来源**：[GPT-4o 模型文档](https://platform.openai.com/docs/models/gpt-4o) · [o1 模型文档](https://platform.openai.com/docs/models/o1) · [GPT-5 模型文档](https://platform.openai.com/docs/models/gpt-5) · [tiktoken 编码映射表](https://github.com/openai/tiktoken/blob/main/tiktoken/model.py)

### cl100k_base（GPT-4 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| gpt-4 | GPT-4 / GPT-4-turbo / GPT-4-32k |
| gpt-3.5-turbo | GPT-3.5-turbo |
| cl100k_base | 直接使用编码 |

**特点**：2022-2023 年的主流编码。词汇表 ~100K tokens。目前仍被 text-embedding-3 系列和旧版 GPT-4 使用。

> **来源**：[GPT-4 模型文档](https://platform.openai.com/docs/models/gpt-4) · [GPT-3.5 Turbo 模型文档](https://platform.openai.com/docs/models/gpt-3-5-turbo)

### p50k_base（Codex 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| text-davinci-003 | GPT-3.5 指令模型（2022 年） |
| p50k_base | 直接使用编码 |

**特点**：2021-2022 年使用的编码。词汇表 ~50K tokens。主要用于对比旧编码与新编码的差异。

> **来源**：[OpenAI Codex 论文 (arXiv)](https://arxiv.org/abs/2107.03374) · [tiktoken 编码列表](https://github.com/openai/tiktoken?tab=readme-ov-file#what-is-tiktoken)

### r50k_base（GPT-3 系）

| 选择器名称 | 对应模型 |
|-----------|---------|
| davinci | GPT-3 基础模型（2020 年） |
| r50k_base | 直接使用编码 |

**特点**：最早的 GPT-3 编码。词汇表 ~50K tokens。用于历史对比参考。

> **来源**：[GPT-3 论文 (arXiv)](https://arxiv.org/abs/2005.14165) · [GPT-3 模型文档](https://platform.openai.com/docs/models/gpt-3)

---

## 开源模型分词器（预计算）

通过 HuggingFace 的 tokenizer.json 预计算词元数，嵌入 HTML 中直接读取。需要先运行 `node code/precompute_tokens.js` 生成数据。

> **实现参考**：[transformers.js 文档](https://huggingface.co/docs/transformers.js) · [HuggingFace Tokenizers 库](https://github.com/huggingface/tokenizers)

| 选择器名称 | HuggingFace 模型 | 编码类型 | 词汇量 |
|-----------|-----------------|---------|--------|
| DeepSeek-R1 | [deepseek-ai/DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1) | BPE | ~100K |
| Llama-3-8B | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | BPE (SentencePiece) | ~128K |
| Llama-3-70B | [meta-llama/Meta-Llama-3-70B](https://huggingface.co/meta-llama/Meta-Llama-3-70B) | BPE (SentencePiece) | ~128K |
| Qwen2.5-72B | [Qwen/Qwen2.5-72B](https://huggingface.co/Qwen/Qwen2.5-72B) | BPE | ~152K |
| Phi-2 | [microsoft/phi-2](https://huggingface.co/microsoft/phi-2) | BPE | ~50K |
| Gemma-7B | [google/gemma-7b](https://huggingface.co/google/gemma-7b) | SentencePiece | ~256K |

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