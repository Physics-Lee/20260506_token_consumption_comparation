# davinci-002、babbage-002 和 embedding 模型为什么都用 cl100k_base

在 tiktoken 的映射表里，几个名字上看起来属于"老时代"的模型全部用了 cl100k_base（100K）编码。原因是：**名字是旧品牌，模型是全新的。**

---

## dripped-002 和 babbage-002：借名的全新模型

```
davinci       2020, r50k_base (50K)  ← GPT-3 原版，现已下线
davinci-002   2023, cl100k_base      ← 全新模型，全新训练，"davinci"只是品牌名

babbage       2020, r50k_base (50K)  ← GPT-3 原版，现已下线
babbage-002   2023, cl100k_base      ← 全新模型，全新训练
```

怎么区分：**挂 `-002` 后缀的都不是 GPT-3 原版。**

OpenAI 在 2023 年重新训练了一套"基础模型"（base models），沿用了科学家命名体系作为品牌档位——davinci 代表最强档，babbage 代表便宜档——但训练时 cl100k_base 已经是内部标准编码，没有理由回头用旧的 r50k。

类比：iPhone SE 叫 SE，不代表它用的是 2016 年第一代 SE 的芯片。名字是定位，硬件是当代的。

---

## embedding 模型：发布时间决定编码

| 模型 | 发布时间 | 编码 | 当时 OpenAI 的标准编码 |
|------|------|------|------|
| text-embedding-ada-002 | 2022.12 | cl100k_base | cl100k_base（ChatGPT 上线后） |
| text-embedding-3-small | 2024.01 | cl100k_base | o200k_base（GPT-4o 尚未发布） |
| text-embedding-3-large | 2024.01 | cl100k_base | o200k_base |

发布时间全部在 cl100k_base 成为标准之后。

### 为什么 text-embedding-3 没用最新的 o200k_base

text-embedding-3 2024 年 1 月发布，当时 o200k_base 还没出现（o200k 是 2024 年 5 月随 GPT-4o 发布的）。而且 embedding 模型的 tokenizer 如果改编码，会导致**所有已向量化的文档全部失效**——向量和 tokenizer 绑定，换 tokenizer 等于废掉整个向量数据库。所以 text-embedding-3 选择了向下兼容，延续 cl100k_base。

### 为什么 embedding 和生成模型要用同一套编码

```
开发者需要知道: 我的 prompt 用了多少 token → API 才按 token 收费

如果 embedding 用 r50k 编码:
  "hello world" → r50k 切出来 3 个 token
  生成模型用 cl100k:
  "hello world" → cl100k 切出来 2 个 token
  → 两边 token 数对不上 → 计费和估算是两套 → 添乱

统一用 cl100k_base:
  "hello world" → 2 个 token ← 生成和 embedding 一个数字
  → 开发者只需要维护一套 token 计算逻辑
```

---

## 总结

```
davinci-002, babbage-002      → 全新的 2023 模型，借旧品牌名，用新编码
text-embedding-ada-002        → 2022.12 发布，cl100k 已是标准
text-embedding-3-small/large  → 2024.01 发布，为了向下兼容沿用 cl100k
```

和 GPT-3 的 davinci/babbage/ada 共享的只有名字，没有一行权重代码。编码统一到 cl100k_base 也不是巧合——它是 OpenAI 产品矩阵中覆盖范围最广的编码，连接了生成、嵌入、微调三条产品线。
