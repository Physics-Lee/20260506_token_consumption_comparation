# r50k_base 与 p50k_base 的对比

两者词汇量相同（都是 50,000 个 token），但**词表内容完全不同**。容量上限一样，不代表内容一样。

---

## 对比

| | r50k_base | p50k_base |
|---|---|---|
| 全称 | raw 50k base | prompt 50k base |
| 用于 | GPT-3 基础模型 | Codex / text-davinci-003 |
| 训练语料 | 纯文本（网页、文章、书籍） | 文本 **+ 大量代码**（GitHub） |
| 诞生时间 | 2020 | 2021 |
| 典型模型 | davinci, curie, babbage, ada | text-davinci-002, text-davinci-003, code-davinci-002 |

## 为什么会多出一套

GPT-3 发布后，OpenAI 发现一个痛点：r50k 切代码切得太碎了。

```
输入: "import numpy as np"
              
r50k:  ["import", " num", "py", " as", " np"]
       → import 是常见单词 token，但 numpy 被拆成 num + py

p50k:  ["import", " num", "py", " as", " np"]  
       → 在这个例子里差不太多，但在更多代码模式中 p50k 显著更优
```

当 OpenAI 做 Codex（代码生成模型）时，如果继续用 r50k，代码里的大量关键字、函数名、变量模式都会被拆得很碎。于是他们用**含 GitHub 代码的混合语料**重新训练 BPE，产出 p50k。

## 实际差异示例

```
输入: "def __init__(self, x):\n    self.x = x"
```

| | r50k_base | p50k_base |
|---|---|---|
| `def` | 1 token（英文常见词，在纯文本语料里高频） | 1 token |
| `__init__` | 可能 3-4 tokens（双下划线模式在文本中罕见） | 2-3 tokens（代码中大量 __init__） |
| `self` | 1 token | 1 token |
| `self.x` | `self` + `.` + `x` = 3 tokens | 可能 `self.` + `x` = 2 tokens（点号附着模式在代码中高频） |

总体差异：对纯文本两者几乎一样，对代码 p50k 通常省 5-15% 的 token。

## 类比

两本 50 页的词典：

```
r50k 词典:  "hello" ✓  "world" ✓  "def" ✓  "import" ✓  "__init__" ✗
            → 文学词汇丰富

p50k 词典:  "hello" ✗  "world" ✓  "def" ✓  "import" ✓  "__init__" ✓
            → 编程词汇丰富（牺牲了一些低频文学词换代码 token）
```

页数一样（50K），但每页上写的东西不同。BPE 训练时的语料分布决定了哪些词对更频繁，也就决定了哪些 token 占用了这 50K 中的位置。

## 为什么 2024 年后不再分家了

o200k_base 的词汇量是 200K，比 r50k + p50k 加起来还大。它有足够空间**同时**收录文本和代码的高频 token，不需要做取舍。这就是为什么 GPT-4o 一个编码统一了文本和代码——大词表解决了 r50k/p50k 当年需要分家的根本矛盾。
