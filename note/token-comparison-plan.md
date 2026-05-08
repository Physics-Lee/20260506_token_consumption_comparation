# Token 对比功能实现方案

## 目标

在 corpus_reader.html 中新增 tokenizer 选择器，允许用户切换不同分词器，对比各语言版本的 token 消耗量。

## 整体数据流

```
data/*.json（12篇语料）
        │
        ├──→ code/precompute_tokens.py  ← 新建
        │    下载 HuggingFace tokenizer.json
        │    对所有文本预计算 token 数
        │    输出 data/token_counts.json
        │
        └──→ code/json2html.py  ← 修改
             读取 token_counts.json
             注入预计算数据到 HTML
             添加 tokenizer 选择器 UI
             添加 gpt-tokenizer CDN
             输出 corpus_reader.html
```

## 文件清单

| 文件 | 动作 | 用途 |
|------|------|------|
| `code/precompute_tokens.py` | **新建** | 用 HuggingFace tokenizer 对所有语料预计算 token 数 |
| `data/token_counts.json` | **新建（生成）** | 预计算结果，提交到仓库 |
| `code/json2html.py` | **修改** | ① 读 token_counts.json ② 注入数据到对比表 ③ 嵌入 JS 逻辑 |
| `corpus_reader.html` | **重新生成** | 最终产物，包含实时 token 对比 |

## 核心方案：混合计算

| 模型来源 | 实现方式 | 原因 |
|----------|----------|------|
| OpenAI（GPT-4o/4/3.5 等） | `gpt-tokenizer` CDN 实时计算 | 50KB 纯 JS，浏览器秒加载 |
| 开源（DeepSeek/Llama/Qwen） | **预计算**，嵌入 HTML | 语料是静态的，无需运行时加载 30MB 的 transformers.js |

### 预计算原理

```
data/*.json（12篇 × 4语言 = 48段文本）
        ↓
对每个开源模型:
  下载 tokenizer.json（1-5MB，一次性的）
  对 48 段文本逐段 encode → 记录 token 数
        ↓
data/token_counts.json
```

### 预计算结果格式

```json
{
  "open_source": {
    "DeepSeek-R1": {
      "allende": {
        "spanish": 523,
        "classical_chinese": 412,
        "modern_chinese": 380,
        "english": 510
      },
      "paulgraham": { ... }
    },
    "Llama-3-8B": { ... },
    "Qwen2.5-72B": { ... }
  }
}
```

## json2html.py 修改点

### 1. 读取预计算数据

```python
# 构建时读入
with open("data/token_counts.json") as f:
    token_data = json.load(f)
# 嵌入为 JS 变量
PRECOMPUTED_TOKENS = {...}
```

### 2. 对比表加 Token 列

表头从：
```
语言 | 角色 | 标题 | Unicode 字符数
```
变为：
```
语言 | 角色 | 标题 | Unicode 字符数 | 所选分词器的词元数
```

每行新增：
```html
<td class="token-count" data-article="allende" data-lang="spanish">—</td>
```

### 3. Tokenizer 选择器 UI

在 nav 栏右侧或独立一行：

```
┌──────────────────────────────────────────────────────┐
│  [文章1] [文章2] ...    │  分词器: [🔽 gpt-4o     ]  │
└──────────────────────────────────────────────────────┘
```

下拉菜单结构：
```
── OpenAI ──
  gpt-4o / o200k_base
  gpt-4.1
  gpt-4 / gpt-3.5-turbo / cl100k_base
  text-davinci-003 / p50k_base
  davinci / r50k_base
  o1 / o3
── 开源（预计算）──
  DeepSeek-R1
  Llama-3-8B
  Llama-3-70B
  Qwen2.5-72B
  Phi-2
  Gemma-7B
```

### 4. JavaScript 逻辑（嵌入 HTML）

```javascript
// gpt-tokenizer 从 CDN 加载（50KB）
import { encode, modelNames } from 'https://cdn.jsdelivr.net/npm/gpt-tokenizer/+esm';

// 预计算数据（构建时注入）
const PRECOMPUTED_TOKENS = { ... };

// 当前选择的 tokenizer
let currentTokenizer = 'gpt-4o';

// tokenizer 切换时
function onTokenizerChange(name) {
    currentTokenizer = name;
    updateAllTokenCounts();
}

// 更新所有表格
function updateAllTokenCounts() {
    document.querySelectorAll('.token-count').forEach(cell => {
        const text = getTextForCell(cell);  // 从对应 <pre> 取文本
        if (isOpenAIModel(currentTokenizer)) {
            cell.textContent = encode(text).length.toLocaleString();
        } else {
            // 读预计算数据
            const article = cell.dataset.article;
            const lang = cell.dataset.lang;
            cell.textContent = PRECOMPUTED_TOKENS.open_source[currentTokenizer][article][lang];
        }
    });
}
```

## 运行时行为

```
用户选择 tokenizer "gpt-4o"
    ↓
js: isOpenAIModel("gpt-4o") → true
    ↓
遍历所有 <pre> → encode(text) → token 数
    ↓
更新所有 .token-count 单元格（毫秒级）

用户选择 "DeepSeek-R1"
    ↓
js: isOpenAIModel("DeepSeek-R1") → false
    ↓
读取 PRECOMPUTED_TOKENS["open_source"]["DeepSeek-R1"][article][lang]
    ↓
更新所有 .token-count 单元格（微秒级）
```

## 支持的 Tokenizer 列表

### OpenAI（实时计算，gpt-tokenizer）

| 显示名 | 编码 | 说明 |
|--------|------|------|
| gpt-4o | o200k_base | GPT-4o / GPT-4.1 |
| gpt-4 | cl100k_base | GPT-4 / GPT-3.5-turbo |
| gpt-3.5-turbo | cl100k_base | 同上编码 |
| text-davinci-003 | p50k_base | Codex / Davinci 系 |
| davinci | r50k_base | GPT-3 早期 |
| o1 | o200k_base | o 系列推理模型 |
| o3 | o200k_base | 同上 |

### 开源（预计算，HuggingFace tokenizer.json）

| 显示名 | 模型 |
|--------|------|
| DeepSeek-R1 | deepseek-ai/DeepSeek-R1 |
| Llama-3-8B | meta-llama/Meta-Llama-3-8B |
| Llama-3-70B | meta-llama/Meta-Llama-3-70B |
| Qwen2.5-72B | Qwen/Qwen2.5-72B |
| Phi-2 | microsoft/phi-2 |
| Gemma-7B | google/gemma-7b |
