# davinci 是什么

"davinci" 在 OpenAI 生态里有三种含义，取决于上下文。

---

## 1. GPT-3 基础模型（davinci）

2020 年，OpenAI 发布了 GPT-3 系列，用四位科学家/数学家命名四个规模的基础模型：

| 模型名 | 全名 | 参数量 | 能力 |
|--------|------|:---:|------|
| **ada** | Ada Lovelace（第一位程序员） | 350M | 最轻量，最快 |
| **babbage** | Charles Babbage（差分机发明者） | 1.3B | 轻量 |
| **curie** | Marie Curie（放射性研究先驱） | 6.7B | 中等 |
| **davinci** | Leonardo da Vinci（达芬奇） | 175B | 最强，最贵 |

davinci 是当时参数最大、能力最强的 GPT-3 模型。它在 API 里叫 `davinci`，用的编码是 `r50k_base`。

### 命名逻辑

Ada → Babbage → Curie → Davinci，按科学家所处时代和贡献的"复杂程度"递增排列，对应模型从小到大。

---

## 2. GPT-3.5 指令模型（text-davinci-003）

2022 年，OpenAI 对 davinci 基础模型做指令微调（instruct fine-tuning），发布了：

| 模型 | 说明 |
|------|------|
| `text-davinci-001` | 第一批指令微调尝试 |
| `text-davinci-002` | 改进版，用了 p50k_base 编码 |
| **`text-davinci-003`** | 最成熟的指令版 davinci，**就是 ChatGPT 的前身** |

`text-davinci-003` 用的编码是 `p50k_base`——它虽然名字还带 davinci，但 tokenizer 已经不是基础版的 r50k 了，而是为指令模型优化的 p50k。

这是经常被混淆的点：

```
davinci               → r50k_base 编码
text-davinci-003       → p50k_base 编码（名字带 davinci，但 tokenizer 不同！）
```

---

## 3. 后续使用 davinci 名字的模型

2023 年，OpenAI 停止在 API 中提供原始的 davinci 模型，但 "davinci" 这个品牌名被延续：

| 模型 | 编码 | 说明 |
|------|------|------|
| `davinci-002` | cl100k_base | 不是 GPT-3 的 davinci！是后来重新训练的基础模型，用 cl100k 编码 |

所以 `davinci`（2020）和 `davinci-002`（2023）是完全不同的模型，连编码都不一样。

---

## 在 tiktoken/model.py 中的体现

```python
MODEL_TO_ENCODING = {
    "davinci":             "r50k_base",    # GPT-3 基础模型 (2020)
    "text-davinci-003":    "p50k_base",    # GPT-3.5 指令模型 (2022)
    "text-davinci-002":    "p50k_base",    # 同上
    "text-davinci-001":    "r50k_base",    # GPT-3 第一次指令微调 (仍用 r50k)
    "davinci-002":         "cl100k_base",   # GPT-4 时代的基础模型代号 (2023)
}
```

**名字都带 davinci，编码各不相同。** 这就是为什么 tiktoken 需要一个完整的映射表——靠名字根本猜不出编码。

---

## 在本项目中的体现

index.html 的选择器里，"davinci" 对应 `r50k_base`（GPT-3 基础版的编码），用来代表最早的 GPT-3 时代 token 消耗水平——和 o200k_base 对比，能看到 2020→2024 编码效率的提升幅度。
