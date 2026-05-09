# 为什么废弃的模型还能在 Tiktokenizer 上看到

Tiktokenizer.vercel.app 上有一堆已下线的模型选项（code-davinci-002、text-davinci-003、各种带 `-001` 后缀的老模型），但它们仍然可以正常使用。原因在于：**分词器和模型是两个完全独立的东西。**

---

## 模型和编码表是分离的

```
模型 code-davinci-002:
  ├─ 权重文件 (175B 参数)    → 2023 年 3 月下线，GPU 释放，不再服务
  └─ BPE 编码表 (p50k_base)  → 开源，永远在 tiktoken 库里，随时可用
```

Tiktokenizer 加载的是**编码表**，不是模型权重。

```
Tiktokenizer 的运行流程:
  1. 加载 p50k_base 编码表（一个几 MB 的静态文件）
  2. 对用户输入的文本跑 BPE 算法
  3. 输出 token 个数和可视化

全程没有调用任何 OpenAI API，没有加载任何模型权重，
不需要 GPU，不需要模型还在线。
```

---

## 类比

| | 模型 | 编码表 |
|---|---|---|
| 类比 | 一台汽车 | 一本汽车零件目录 |
| 能开吗 | 模型在线才能用 | 不需要"在线" |
| 下线后 | 车报废了 | 零件目录还在书架上 |
| 用途 | 生成文本 | 告诉你"这台车的发动机由哪些零件组成" |

查零件目录不需要车还在线。同样的，查"hello world"在 p50k_base 编码下会切成几个 token，不需要 text-davinci-003 还在提供服务。

---

## tiktoken 库的设计哲学

tiktoken 是 OpenAI 的官方分词器库，它的设计原则是**所有历史编码永久可用**：

```python
tiktoken.encoding_for_model("text-davinci-003")  # ✅ 模型下线了，但编码表还能加载
tiktoken.get_encoding("p50k_base")               # ✅ 直接按编码名加载
```

### 为什么要永久保留

1. **历史数据复盘**：你在 2022 年用 text-davinci-003 API 跑了一百万条请求，每条都记录了 token 消耗。2024 年模型下线，你仍然需要把当时的 token 序列 decode 回文本，或者复盘成本，这都需要原始编码表。

2. **跨编码对比**：你要比较"同一段中文在 2020 年的 GPT-3 编码下消耗多少 token vs 2024 年的 GPT-4o 编码下消耗多少"。删掉旧编码表，这种对比就无法完成。

3. **编码表就是数据的钥匙**：所有经某个编码切割过的 token 序列，都是这个编码的产物。删掉它 = 历史数据变成不可解读的乱码——就像删掉字典后，你手上那堆 token ID 永远不知道对应什么文字。

---

## Tiktokenizer 的项目选择

Tiktokenizer 选择展示所有可用的编码，并不是因为那些模型还在运行，而是它提供的价值在于"你可以用任何历史编码切分你的文本，看看 token 消耗如何变化"。

OpenAI 官方虽然将旧模型标记为 "DEPRECATED"，但从未将它们从编码映射表中移除，也从未删除对应的编码文件。

```python
# tiktoken/model.py 中的注释
"text-davinci-003": "p50k_base",  # DEPRECATED
"text-davinci-002": "p50k_base",  # DEPRECATED
"text-davinci-001": "r50k_base",  # DEPRECATED
"davinci":          "r50k_base",  # DEPRECATED
# 标记 DEPRECATED，但编码映射和数据依然保留
```

---

## 和本项目的对应

本项目 `index.html` 也做了同样的事——4 种 OpenAI 编码（r50k_base、p50k_base、cl100k_base、o200k_base）全部加载，即使其中两种对应的模型早已下线。目的不是让你用那些模型，而是让你**对比同一段文本在不同历史时期的编码效率**。
