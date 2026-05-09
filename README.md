# 用文言，可省词元乎？

A multilingual parallel corpus for comparing token consumption across languages and tokenizer models.

## 目录结构

```
.
├── code/                          # 构建脚本
│   ├── build_index.py             # 生成 index.html
│   ├── precompute_tokens.py       # Python 版：HuggingFace 预计算开源模型 token 数
│   └── precompute_tokens.js       # JS 版：纯 JS BPE 预计算，零 Python 依赖
├── index.html                     # 产物：Token 消耗对比页 + 阅读器
├── data/                          # 规范语料数据
│   ├── *.json                     # 文章数据（每篇含 4 种语言）
│   └── token_counts.json          # 预计算的开源模型 token 数
├── note/                          # 文档
└── resource/                      # 原文 Markdown
```

## 更新流程

```
改 data/*.json          →  python code/precompute_tokens.py  →  data/token_counts.json
（加文章/改文本）            （重新编码所有文本）                  ↓
                                                         python code/build_index.py  →  index.html
                                                         （构建页面）                    （浏览器打开）
```

> `precompute_tokens.py` 需要 `pip install transformers`。不想装 Python 依赖可用 `node code/precompute_tokens.js`，纯 JS BPE 实现，零依赖。

### 如果只改样式/代码（不改数据）

```
改 build_index.py 模板   →  python code/build_index.py    →  index.html
```

### 如果增删分词器

1. 改 `build_index.py` 里 `<optgroup>` 那段的 `<option>` 列表
2. 开源模型增删需同步改 `precompute_tokens.py` 的 `OPEN_SOURCE_MODELS` 字典
3. 重新跑 `precompute_tokens.py` → `build_index.py`

> 如果 token_counts.json 还没生成过（或不需要开源模型数据），直接跑 `build_index.py` 也行——开源模型那列会显示"需预计算"。

## 如何添加新文章

1. 创建 JSON 文件放入 `data/`，遵循此 schema：

```json
{
  "id": "unique_id",
  "metadata": {
    "title_zh": "中文标题",
    "title_en": "English Title",
    "title_es": "Título en Español",
    "author": "作者名",
    "source": "出处",
    "period": "时代",
    "genre": "体裁",
    "original_language": "modern_chinese"
  },
  "texts": [
    {
      "language": "classical_chinese",
      "role": "translation",
      "title": "文言标题",
      "content": "全文..."
    },
    {
      "language": "modern_chinese",
      "role": "original",
      "title": "现代汉语标题",
      "content": "全文..."
    },
    {
      "language": "english",
      "role": "translation",
      "title": "English Title",
      "content": "Full text..."
    },
    {
      "language": "spanish",
      "role": "translation",
      "title": "Título en Español",
      "content": "Texto completo..."
    }
  ]
}
```

2. 按需要跑上面「更新流程」中的对应命令。

## 阅读器特性

- **三态主题**：浅色 / 深色 / 跟随系统
- **分词器切换**：OpenAI 4 种编码 + 6 种开源模型，实时对比 token 消耗
- **预计算 + 实时**：开源模型 token 数预计算，OpenAI 编码浏览器端实时跑
- **响应式布局**：窄屏自动折叠

## 语言标识

| 标识 | 语言 |
|------|------|
| `classical_chinese` | 文言 |
| `modern_chinese` | 现代汉语 |
| `english` | English |
| `spanish` | Español |
