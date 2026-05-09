# OpenAI 分词器编码命名解释

OpenAI 的四套编码遵循统一的命名格式：`{前缀}{数字}_base`

```
 r50k_base
 │ │   │
 │ │   └─ 后缀：基础版本（区别于特化变体）
 │ └───── 数字：词汇表 token 总数（单位 K = 千）
 └─────── 前缀：表示诞生的产品时代
```

---

## 前缀

| 前缀 | 全称 | 含义 |
|------|------|------|
| **r** | raw | 原始的 BPE 编码，GPT-3 早期（davinci / curie / babbage / ada 时代）直接在大规模文本上训练，没有针对特定任务优化 |
| **p** | prompt | GPT-3 指令微调时代（text-davinci-003 / Codex）。针对 prompt-instruct 范式做了优化，"prompt" 指的就是当时 OpenAI API 的 prompt 字段 |
| **cl** | Chat Language | ChatGPT 时代（GPT-3.5-turbo / GPT-4）。为聊天场景重新训练，`cl` = Chat + Language。也是目前 text-embedding-3 系列使用的编码 |
| **o** | omni | GPT-4o 时代（2024 至今）。`o` 取自 GPT-4o 的 "o"——官方说 "o" 代表 "omni"（全能），暗示多模态。o1 / o3 / GPT-5.x 全部沿用此编码 |

### 未在主项目中使用但存在的前缀

| 前缀 | 编码名 | 说明 |
|------|--------|------|
| — | gpt2 | GPT-2 时代的编码，最早的 BPE 实现，词汇量最小。tiktoken 库中仍可手动调用 |
| — | o200k_harmony | gpt-oss（OpenAI 开源模型系列）使用的实验性编码，基于 o200k 修改 |

---

## 数字：词汇表大小

| 编码 | 词汇量 | 说明 |
|------|:---:|------|
| r**50k** | 50,000 | 最早的规模，够用但中文切得碎 |
| p**50k** | 50,000 | 和 r50k 不同，训练语料更新（加了代码），大小相同 |
| cl**100k** | 100,000 | 翻倍，开始覆盖更多常见组合 |
| o**200k** | 200,000 | 再翻倍，大幅扩展 CJK（中日韩）多字词组 |

数字越大，BPE 训练时允许的合并次数越多，词表里就能存更多常见词组。对于中文用户，o200k_base 在 API 费用上通常比 cl100k_base 省 30-50%。

---

## 后缀 _base：基础版本

所有编码统一加上 `_base` 后缀，表示"通用基础版本"。

### 为什么有 _base

p50k 编码存在两个变体：

| 编码 | 用途 |
|------|------|
| `p50k_base` | 通用版本，被 text-davinci-003、Codex 等主模型使用 |
| `p50k_edit` | 为已废弃的 Edit API 特化，能识别 `[insert]`、`[replace]` 等编辑指令标记 |

其他编码（r50k、cl100k、o200k）只有一个版本，但为保持一致，全加 `_base` 后缀——就像内部代码规范，有特例的才加第二个，没特例的也不能省略后缀。

### 如果命名是另一种设计

OpenAI 完全可以命名为：

```
GPT3Tokenizer          ← 不用 r50k_base
InstructTokenizer      ← 不用 p50k_base
ChatTokenizer          ← 不用 cl100k_base
OmniTokenizer          ← 不用 o200k_base
```

但他们选择了**编码特征**命名而非**产品名**命名，因为编码的生命周期比产品长——GPT-3 下线了，r50k 编码的格式仍可被理解。

---

## 时间线

```
2020  r50k_base     davinci / curie / babbage / ada
      └─ 纯文本 BPE，词汇量 50K

2021  p50k_base     text-davinci-003 / Codex
      └─ 加了代码语料训练，词汇量 50K

2022  cl100k_base   gpt-3.5-turbo / gpt-4
      └─ 聊天场景优化，词汇量翻倍到 100K

2024  o200k_base    gpt-4o / gpt-4.1 / o1 / o3 / gpt-5.x
      └─ 多模态 + 多语言，词汇量再翻倍到 200K
```

---

## 编码和模型的对应关系

不是一一对应。4 种编码覆盖了 OpenAI 全部 60+ 个模型：

```
o200k_base ← gpt-4o / GPT-4.1 / o1 / o3 / GPT-5.x / GPT-4.5
cl100k_base ← GPT-4 / GPT-3.5-turbo / text-embedding-3 / davinci-002
p50k_base   ← text-davinci-003 / Codex / code-davinci-002
r50k_base   ← davinci / curie / babbage / ada (GPT-3 基础模型)
```

模型可以下架，但编码是永久的——只要知道文本是用哪种编码切的，就能还原出 token 序列。
