# gpt2 编码与 r50k_base 的对比

两者词汇量相近（约 50K），但属于**不同时代、不同语料、不同算法细节**的产物。GPT-2 是第 1 代收录的 BPE 编码，r50k 是第 2 代。

---

## 对比

| | gpt2 | r50k_base |
|---|---|---|
| 用于 | GPT-2 全系列 | GPT-3 基础模型（davinci, curie, babbage, ada） |
| 训练语料 | WebText（Reddit 3 点赞以上的外链网页） | GPT-3 训练语料（Common Crawl + WebText2 + Books + Wikipedia，总量大得多） |
| 词汇量 | ~50,000 | 50,000 |
| 诞生时间 | 2019 | 2020 |
| 现状 | 无在役模型使用 | 无在役模型使用（已被 cl100k / o200k 替代） |

## 为什么会重新训练

GPT-3 的训练语料比 GPT-2 大了两个数量级，而且语料构成完全不同（GPT-2 只有 WebText，GPT-3 加了代码、书籍、多语言数据）。用老编码器处理新数据，很多高频模式会成为罕见模式，导致 token 切得过碎。

重新跑一遍 BPE 训练，让词表更匹配 GPT-3 的实际输入分布，是最直接的做法。

## 实际差异

两者差异不大，因为都是 50K 量级且都是纯文本主导：

```
输入: "The quick brown fox jumps over the lazy dog"

gpt2:     10 tokens（常见英文短句，两种编码表现几乎一致）
r50k_base: 10 tokens

输入: "Machine learning is a subset of artificial intelligence"

gpt2:     13 tokens
r50k_base: 13 tokens（类似）
```

主要差异出现在 GPT-3 训练语料中新增的内容类型上：

- **代码片段**：r50k 略微优于 gpt2（GPT-3 语料含少量代码）
- **多语言**：r50k 略微优于 gpt2（GPT-3 语料含更多非英语文本）
- **数学/科学符号**：r50k 更好（GPT-3 语料含 arXiv 论文）

但总体上，gpt2 和 r50k 的差异远小于 r50k 和 p50k 的差异——因为 gpt2 → r50k 是同质升级（文本→更多文本），r50k → p50k 是跨界（文本→文本+代码）。

## 为什么 gpt2 还在 tiktoken 里

```python
# tiktoken/model.py
"gpt2": "gpt2",    # 保留
"gpt-2": "gpt2",   # 别名
```

纯粹是为了兼容性——确保 `tiktoken.encoding_for_model("gpt-2")` 不会报错。没有在役模型用这个编码，但 tiktoken 作为一个库，承诺对所有历史模型名都能返回正确的编码。

## 类比

GPT-1 的 tokenizer 用了一个词级方案（依赖 spaCy），但 GPT-2 和后续版本统一采用了纯 BPE。而 GPT-2 的 BPE 编码最终被 GPT-3 的 r50k 取代。

GPT-2 和 r50k 的关系，就像 iPhone 4 和 iPhone 5——都是手机，都叫 iPhone，但内部已经换了一代。token 数看起来差不多，词表结构已经不同。
