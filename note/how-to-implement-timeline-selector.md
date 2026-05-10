# 实施改造指南：从当前方案到时间线选择器

当前 `build_index.py` 已经初步改了选择器 UI（Qwen/DeepSeek 版本分组），但**数据结构和 JS 逻辑还没跟上**。本 note 记录从现状到完整方案的改动点。

---

## 现状 vs 目标

| | 现状 | 目标 |
|---|---|---|
| 选择器 | 单个下拉，OpenAI + 几个开源模型 | 按公司分组的时间线选择器，每个版本独立可选 |
| token_counts.json | `{ "open_source": { "Qwen2.5-72B": {...} } }` | `{ "qwen": { "1.0-150K": {...}, "2.5-151K": {...}, "3.5-248K": {...} }, "deepseek": {...} }` |
| JS 查找逻辑 | `pre.open_source[name][articleId][lang]` | `pre[company][version][articleId][lang]` |
| 预计算 | 单版本 GPT-2 / Phi-2 | 每家公司多版本，从 HuggingFace 逐个下载 |

---

## 改动清单

### 改动 1：token_counts.json 新结构

```json
{
  "openai": {
    "r50k_base":  { ... },   // OpenAI 仍走 CDN 实时计算，此项可选
    "cl100k_base": { ... }
  },
  "qwen": {
    "1.0-150K": {
      "allende": {
        "classical_chinese": 523,
        "modern_chinese": 680,
        "english": 1150,
        "spanish": 1178
      },
      "paulgraham": { ... }
    },
    "2.5-151K": { ... },
    "3.5-248K": { ... }
  },
  "deepseek": {
    "V2-32K":  { ... },
    "V3-128K": { ... }
  },
  "llama": {
    "1-32K":   { ... },
    "3-128K":  { ... },
    "4-200K":  { ... }
  },
  "glm": {
    "GLM-4-150K": { ... }
  },
  "kimi": {
    "K2-160K": { ... }
  },
  "minimax": {
    "M1-200K": { ... }
  }
}
```

**改动**：顶层 key 从 `"open_source"` 改为按公司名分组。版本名作为二级 key。

这只影响预计算脚本的输出和 JS 读取路径，不影响 Python 生成器。

---

### 改动 2：build_index.py — 选择器 HTML

当前在 `build_index.py` 行 486-506。改成：

```html
<select id="tokenizer-select" class="tokenizer-select">
    <optgroup label="OpenAI（实时）">
        <option value="r50k_base">r50k_base — GPT-3 / davinci（2020）</option>
        <option value="p50k_base">p50k_base — Codex / text-davinci-003（2021）</option>
        <option value="cl100k_base">cl100k_base — GPT-3.5 / GPT-4（2022）</option>
        <option value="o200k_base" selected>o200k_base — GPT-4o / GPT-5.x（2024+）</option>
    </optgroup>

    <optgroup label="Llama 词表演变">
        <option value="llama/1-32K">Llama 1/2 — 32K SentencePiece（2023）</option>
        <option value="llama/3-128K">Llama 3 — 128K tiktoken（2024）</option>
        <option value="llama/4-200K">Llama 4 — 200K tiktoken（2025）</option>
    </optgroup>

    <optgroup label="Qwen 词表演变">
        <option value="qwen/1.0-150K">Qwen 1.0/1.5/2 — 150K（2023）</option>
        <option value="qwen/2.5-151K">Qwen 2.5 — 151K（2024）</option>
        <option value="qwen/3.5-248K">Qwen 3.5 — 248K（2026）</option>
    </optgroup>

    <optgroup label="DeepSeek 词表演变">
        <option value="deepseek/V2-32K">DeepSeek-V2 — 32K（2024.05）</option>
        <option value="deepseek/V3-128K">DeepSeek-V3/R1/V4 — 128K（2024.12+）</option>
    </optgroup>

    <optgroup label="其他开源">
        <option value="glm/GLM-4-150K">GLM（智谱）— 150K 混血词表</option>
        <option value="kimi/K2-160K">Kimi K2 — 160K tiktoken</option>
        <option value="minimax/M1-200K">MiniMax — 200K</option>
    </optgroup>
</select>
```

**关键**：value 用 `company/version` 斜杠分隔，JS 端拆分后查找。

---

### 改动 3：build_index.py — JS 逻辑

当前在行 604-684。核心改动点：

```javascript
// OpenAI 编码 → CDN 全局变量（不变）
const ENCODERS = {
    'r50k_base':  GPTTokenizer_r50k_base,
    'p50k_base':  GPTTokenizer_p50k_base,
    'cl100k_base': GPTTokenizer_cl100k_base,
    'o200k_base': GPTTokenizer_o200k_base,
};

function updateAllTokenCounts() {
    const name = currentTokenizer;  // 如 "qwen/3.5-248K" 或 "o200k_base"
    // ...

    cells.forEach(cell => {
        // ...
        const isOpenAI = !!ENCODERS[name];  // OpenAI 值在 ENCODERS 表中

        if (!isOpenAI) {
            // 解析 company/version： "qwen/3.5-248K" → ["qwen", "3.5-248K"]
            const [company, version] = name.split('/');
            const pre = window.PRECOMPUTED_TOKENS;
            if (pre && pre[company] && pre[company][version] &&
                pre[company][version][articleId] &&
                pre[company][version][articleId][lang] !== undefined) {
                cell.textContent = pre[company][version][articleId][lang].toLocaleString();
            } else {
                cell.textContent = '需预计算';
            }
            return;
        }

        // OpenAI：实时计算
        const text = getText(articleId, lang);
        const count = countTokens(text, name);
        cell.textContent = count > 0 ? count.toLocaleString() : '—';
    });
}
```

**改动点**：
1. 删除 `OPEN_SOURCE_MODELS` 数组和 `isOpenSource()` 函数
2. 用 `!!ENCODERS[name]` 判断是否 OpenAI（在 ENCODERS 表里 = OpenAI，不在 = 预计算）
3. 用 `name.split('/')` 从 `"qwen/3.5-248K"` 拆出公司和版本，按 `pre[company][version]` 路径查找

---

### 改动 4：precompute_tokens.js — 多版本下载

当前脚本只下载每个模型的**最新版**。改为循环下载每个**历史版本**：

```javascript
const MODELS = [
    // Qwen 三个时间点
    { key: "qwen/1.0-150K",     repo: "Qwen/Qwen-7B",             file: "tokenizer.json" },
    { key: "qwen/2.5-151K",     repo: "Qwen/Qwen2.5-72B",         file: "tokenizer.json" },
    { key: "qwen/3.5-248K",     repo: "Qwen/Qwen3.5-27B",         file: "tokenizer.json" },
    // DeepSeek 两个时间点
    { key: "deepseek/V2-32K",   repo: "deepseek-ai/DeepSeek-V2-Lite", file: "tokenizer.json" },
    { key: "deepseek/V3-128K",  repo: "deepseek-ai/DeepSeek-V3",     file: "tokenizer.json" },
    // Llama 三个时间点
    { key: "llama/1-32K",       repo: "meta-llama/Llama-2-7b-hf",  file: "tokenizer.json" },
    { key: "llama/3-128K",      repo: "meta-llama/Meta-Llama-3-8B", file: "tokenizer.json" },
    { key: "llama/4-200K",      repo: "meta-llama/Llama-4-Scout-17B-16E-Instruct", file: "tokenizer.json" },
    // GLM
    { key: "glm/GLM-4-150K",    repo: "zai-org/glm-4-9b",         file: "tokenizer.model" },
    // Kimi（tiktoken 格式）
    { key: "kimi/K2-160K",      repo: "moonshotai/Kimi-K2-Instruct", file: "tiktoken.model" },
    // MiniMax
    { key: "minimax/M1-200K",   repo: "MiniMaxAI/MiniMax-Text-01", file: "tokenizer.json" },
];
```

输出结构也要调整：

```javascript
// 旧：{ "open_source": { "Qwen2.5-72B": { allende: {...} } } }
// 新：{ "qwen": { "2.5-151K": { allende: {...} } }, "deepseek": {...} }
const result = {};
for (const model of MODELS) {
    const [company, version] = model.key.split('/');
    if (!result[company]) result[company] = {};
    result[company][version] = computeAllArticles(model);
}
```

**注意**：GLM 的 tokenizer.model 和 Kimi 的 tiktoken.model 不是标准 tokenizer.json 格式，需要单独处理（GLM 用 SentencePiece 加载，Kimi 用 tiktoken 加载）。

---

## 改动总览

| 文件 | 改动量 | 说明 |
|------|:---:|------|
| `data/token_counts.json` | 结构重构 | 顶层按公司分组，二级按版本 |
| `code/build_index.py` 选择器 HTML | ~30 行 | 替换 optgroup，加公司/版本分组 |
| `code/build_index.py` JS 逻辑 | ~15 行 | 用 split('/') 替代 isOpenSource |
| `code/precompute_tokens.js` | ~50 行 | 多版本循环，输出结构调整 |

总改动量约 100 行。不需要动 CSS、不需要动表格生成逻辑、不需要动 gpt-tokenizer CDN。

---

## 迁移建议

分两步走，降低风险：

**第一步**：改 token_counts.json 结构 + JS 查找逻辑（不新增任何模型版本）
- 验证现有开源模型在新结构下能正常显示
- 确认 OpenAI CDN 模型不受影响

**第二步**：改 precompute_tokens.js + 选择器 HTML，加 Qwen/DeepSeek/Llama 的全部历史版本
- 逐个下载验证，每个版本确认 token 数合理后再加下一个
- 最后打开 index.html，切换版本看时间线效果
