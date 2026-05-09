# GPT-1 与后续 tokenizer 的对比

## GPT-1（2018）

GPT-1 用的**不是纯 BPE**，是一个混合方案：

```
1. 先用 spaCy 做词级分割（word-level tokenization）
   "The cat sat on the mat."
    → ["The", "cat", "sat", "on", "the", "mat", "."]

2. 对于不在词表里的词，再用 BPE 做子词拆分
   "unhappiness"（不在词表里）
    → ["un", "happi", "ness"]
```

| | GPT-1 | GPT-2 及以后 |
|---|---|---|
| Tokenization 方式 | 词级为主 + BPE fallback | 纯 BPE（字节级） |
| 依赖 | 需要 spaCy 做词分割，依赖语言模型 | 无外部依赖，只看字节 |
| 未登录词（OOV） | 有——词表外的词触发 fallback，但部分罕见词仍可能丢失 | **无**——所有字符都在 256 字节范围内，不可能出现 OOV |
| 多语言 | 差——spaCy 主要针对英文，中文日文支持有限 | 天然多语言——字节是所有语言的最小公分母 |
| Unicode/Emoji | 弱——emoji、特殊符号可能无法处理 | 强——emoji 也是字节序列，必然能编码 |

## 为什么 GPT-2 之后全改纯 BPE

GPT-1 的词级方案有三个致命问题：

### 1. OOV 问题

```
输入: "I love GPT-4o"
GPT-1: "GPT-4o" 不在词表 → fallback BPE → "GPT" + "-" + "4" + "o"
GPT-2: 所有字符都能编码，不存 OOV 概念
```

### 2. 多语言天然差

```
输入: "日本語を勉強する"
GPT-1: spaCy 日文支持有限 → 切词混乱
GPT-2: 字节级 BPE → 每个日文字符作为字节处理 → 保证了完整性
```

### 3. 预处理依赖

GPT-1 需要 spaCy + 语言特定规则，不能作为一个独立模块。GPT-2 的 BPE tokenizer 是一个无依赖的纯算法模块，任何语言的文本扔进去都能输出 token。

## 核心转变

```
GPT-1:  词是基本单位，BPE 是补丁
GPT-2+: 字节是基本单位，BPE 是全部
```

这个转变让 tokenizer 从"需要理解语言"变成"纯粹的数学算法"——也让它能处理代码、数学公式、emoji、任何人类尚未发明的符号系统。
