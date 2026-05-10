# 主流 LLM 分词器演变史（截至 2026 年 5 月）

截至 2026 年 5 月，三家模型的分词器演化路径。

---

## Llama：两次大跳跃

```
2023.02  Llama 1    SentencePiece BPE    32K      基础
2023.07  Llama 2    SentencePiece BPE    32K      不变
         ─────────── 分水岭 ───────────
2024.04  Llama 3    改用 tiktoken BPE     128K     4 倍膨胀，多语言能力质变
2024.07  Llama 3.1  tiktoken BPE          128K
2024.12  Llama 3.3  tiktoken BPE          128K
         ─────────── 分水岭 ───────────
2025.04  Llama 4    tiktoken BPE          200K     再翻近一倍
                                                   用 o200k_base 的 regex 模式
                                                   2048 保留 token（Llama 3 仅 256）
                                                   支持 reasoning 专用 token
```

### 关键转折

**Llama 3（2024.04）**：从 SentencePiece 切换到 OpenAI 的 tiktoken 体系。直接原因是 Llama 2 的多语言 token 消耗太高——非英文语言常被拆成碎片。词汇量 4 倍膨胀后，多语言压缩率大幅改善。

**Llama 4（2025.04）**：词汇量再涨到 200K（202,048），和 OpenAI 的 o200k_base 直接对标。新加了大量 reasoning 和 vision 特殊 token，预训练覆盖 200+ 语言。

> **来源**：[meta-llama/llama-models](https://github.com/meta-llama/llama-models) 官方 README · [Llama 4 HuggingFace config](https://huggingface.co/docs/transformers/v5.4.0/en/model_doc/llama4) (vocab_size=202048)

---

## Qwen：保守三代后一次大膨胀

```
2023.??  Qwen 1.0    BBPE        ~150K    基础
2024.02  Qwen 1.5    BBPE        ~150K    不变
2024.06  Qwen 2      BBPE        ~150K    不变
2024.09  Qwen 2.5    BBPE        151,643  控制 token 从 3 个扩展到 22 个
2025.??  Qwen 3      BBPE        151,936  微调
         ─────────── 分水岭 ───────────
2026.??  Qwen 3.5    BBPE        248,320  首次大幅膨胀，63% 增幅
                                          首次改用 Gated RMSNorm + 混合注意力
                                          首次默认多模态 VLM 架构
```

### 关键转折

Qwen 前三代的词汇量极其稳定——一直在 150K 左右微调。但社区持续投诉部分语言（印地语、意大利语、德语）的 token 效率太低：[GitHub Issue #1400](https://github.com/QwenLM/Qwen3/issues/1400) 中用户反馈同一段印地语 Qwen 比 Gemma 多用 3 倍 token。

Qwen 3.5（2026 年最新版）做了一个迟到的大膨胀——从 152K 直跳 248K，增幅 63%。这是 Qwen 系列首次对 tokenizer 做重大架构变更。

> **来源**：[Qwen3.5 MNN 文档](https://github.com/alibaba/MNN/discussions/4354) (vocab_size=248320) · [Qwen3 Issue #1400](https://github.com/QwenLM/Qwen3/issues/1400) · [Qwen3 官方文档](https://github.com/QwenLM/Qwen3)

---

## DeepSeek：最剧烈的一次跳跃

```
2024.05  DeepSeek-V2       Byte-level BPE    32K      基础
         ───────────────── 分水岭 ─────────────────
2024.12  DeepSeek-V3       Byte-level BPE    128K     翻 4 倍
2025.01  DeepSeek-R1       同上              128K     同架构 fine-tune，未改 tokenizer
2025.08  DeepSeek-V3.1     同上              128K
2025.09  DeepSeek-V3.2-Exp 同上              128K     加稀疏注意力，未改 tokenizer
2025.12  DeepSeek-V3.2     同上              128K
2026.04  DeepSeek-V4       同上              128K
```

### 关键转折

**DeepSeek V2 → V3（2024.12）**：32K → 128K，4 倍增长。这是三家最剧烈的一次跃进。V3 技术报告明确写了原因：

> "The tokenizer for DeepSeek-V3 employs Byte-level BPE with an extended vocabulary of 128K tokens. The pretokenizer and training data are modified to optimize multilingual compression efficiency."

预训练语料中数学、编程、多语言内容的比例大幅增加，老 32K 编码无法有效压缩这些内容。V3 之后从 R1 到 V4，这个编码器一路沿用，没有再动过。

> **来源**：[DeepSeek-V3 技术报告](https://arxiv.org/abs/2412.19437) · [HuggingFace DeepSeek-V3 config](https://huggingface.co/docs/transformers/v5.6.2/model_doc/deepseek_v3) (vocab_size=129280) · [DeepSeek API 更新日志](https://api-docs.deepseek.com/updates)

---

## 全部并排（2026.05）

```
              2022     2023     2024          2025          2026

Llama           32K ── 32K ── 128K ──────── 200K ───────── 200K
Qwen                  150K ── 152K ──────── 152K ───────── 248K
DeepSeek                        32K → 128K ── 128K ──────── 128K
GLM              130K ── 130K ── 150K ──────── 150K ──────── 150K
Kimi                                         闭源 ───→ 160K（K2 开源）
MiniMax                                            200K ──→ 200K
豆包                                                                闭源

OpenAI     r50K ── p50K ── cl100K ───────── o200K ───────── o200K
             50K     50K     100K             200K             200K
```

### 共同规律

1. **32K 已被证明是严重瓶颈。** 没有任何一家当前模型低于 128K。

2. **每次大跳跃都和训练语料多样化同步。** Llama 3 跳 4 倍是为了多语言，DeepSeek V3 跳 4 倍是为了数学+编程+多语言，Qwen 3.5 跳 63% 是社区投诉推动的多语言优化。

3. **跳跃之后趋于稳定。** GLM 四代没动过 vocab，DeepSeek V3→V4 没动过，MiniMax 两代没动过——换 tokenizer 意味着所有 embedding 层要重训，代价太大。

4. **行业向 200K 收敛。** Llama 4（200K）、Qwen 3.5（248K）、MiniMax（200K）、OpenAI o200k（200K）都在 200K 这个量级。

5. **唯一全闭源的两家：Anthropic（Claude）和字节（豆包）。** 一个在旧金山，一个在北京。

### 共同规律

1. **32K 已被证明是严重瓶颈。** 三家当前的编码没有一家低于 128K。Llama 1/2 的 32K 和 DeepSeek-V2 的 32K 都被抛弃——到这个尺度，中文/代码/多语言文本会被切得太碎。

2. **每次大跳跃都和训练语料多样化同步。** Llama 3 跳 4 倍是为了多语言，DeepSeek V3 跳 4 倍是为了数学+编程+多语言，Qwen 3.5 跳 63% 是社区投诉推动的多语言优化。

3. **跳跃之后趋于稳定。** 一旦找到合适的词汇量，后续几代模型倾向于沿用同一个 tokenizer，因为换 tokenizer 意味着所有已训练的 embedding 层要重来。

4. **行业正在向 200K+ 收敛。** Llama 4（200K）、Qwen 3.5（248K）、OpenAI o200k_base（200K）都在 200K 这个量级。DeepSeek（128K）最保守，可能会在下一代做跳跃。

---

## GLM（智谱）：混合 tiktoken + 自训练

```
2022.08  GLM-130B       BPE               ~130K   基础，中英双语
2023.03  ChatGLM-6B     BPE               ~130K   开源，社区爆发
2023.06  ChatGLM2-6B    BPE               ~130K   上下文 2K → 32K
2023.10  ChatGLM3-6B    BPE               ~130K
         ─────────────── 分水岭 ───────────────
2024.01  GLM-4          混合 BPE           150K    首次大改
2024.06  GLM-4-9B       混合 BPE           151,552 开源版
```

### 关键转折

GLM-4 做了一个**全世界独一无二的操作**——它没有自己从头训 BPE，而是：

> "employ the byte-level BPE algorithm to separately learn Chinese and multilingual tokens, then merge them with the tokens of the cl100k_base tokenizer in tiktoken into a unified vocabulary with a size of 150,000"
> — ChatGLM 论文

意思就是：拿 OpenAI 的 cl100k_base 词表当底座，自己训练中文和多语言 BPE 合并进去。等于给英文用 OpenAI 的现成编码表，中文部分自己造——偷懒但聪明。

前三代 ChatGLM（6B → 6B2 → 6B3）词汇量稳定在 ~130K，GLM-4 才涨到 150K。之后没有再动过。

> **来源**：[ChatGLM 论文](https://openreview.net/forum?id=iEaNXS7cQd) (vocab_size=150,000) · [GLM-4 HuggingFace](https://huggingface.co/docs/transformers/main/model_doc/glm) (vocab_size=151,552) · [zai-org/glm-4-9b](https://huggingface.co/zai-org/glm-4-9b)

---

## Kimi（月之暗面）：突然转向开源

```
2023.10  Kimi K1        闭源           ？      完全不公开
         ─────────────── 分水岭 ───────────────
2025.07  Kimi K2        基于 tiktoken   160K    突然开源，1T 总参、32B 激活
```

### 关键转折

K1 时代完全闭源。K2 一口气全公开：权重、tokenizer、推理代码全部上 HuggingFace。

K2 的 tokenizer 完全基于 OpenAI 的 tiktoken 格式——直接用 `tiktoken.model` 文件，`load_tiktoken_bpe()` 函数加载，和 OpenAI 的编码表同一套 API。特殊之处是它的 `pat_str` regex 里加了 `[\p{Han}]+` 单独匹配中文字符段，对中文做了显式优化。

160K 词汇量，介于 OpenAI 的 cl100k_base（100K）和 o200k_base（200K）之间。

> **来源**：[moonshotai/Kimi-K2](https://github.com/moonshotai/kimi-k2) · [HuggingFace Kimi-K2-Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct) tokenization_kimi.py

---

## MiniMax：200K 开局，两代保持不变

```
2025.01  MiniMax-Text-01    BPE    200,064   456B 总参，45.9B 激活
2025.10  MiniMax-M2         BPE    200,064   230B 总参，10B 激活（同 tokenizer）
```

### 关键转折

没有转折。MiniMax 开局就定在 200K 词汇量——直接对标 OpenAI o200k_base 和 Llama 4 的量级。两代模型用了完全相同的 tokenizer，没有迭代。

> **来源**：[MiniMax-Text-01 Model Card](https://github.com/MiniMax-AI/MiniMax-01) (vocab=200,064) · [MiniMax-M2 HuggingFace](https://huggingface.co/docs/transformers/en/model_doc/minimax_m2) (vocab=200,064)

---

## 豆包（字节）：API 专供，全黑箱

```
2024.??  Doubao-pro       ？    ？    权重、tokenizer、训练数据一概不公开
```

国内七家主流 LLM 公司中唯一不开源的。和 Anthropic 一样——只能通过 API 使用，无法获取 tokenizer。要算豆包的 token 数，只能调 API 让服务端返回 usage 数据。

---

## 中国七家 tokenizer 公开情况总表

| 公司 | 模型 | 开源 | Tokenizer 公开 | 词汇量 |
|------|------|:---:|:---:|:---:|
| 阿里 | Qwen 1.0 ~ 3.5 | ✅ | ✅ HuggingFace | 152K → 248K |
| 智谱 | GLM-130B ~ GLM-4 | ✅ | ✅ HuggingFace | ~130K → 151K |
| DeepSeek | V2 ~ V4 | ✅ | ✅ HuggingFace | 32K → 128K |
| 月之暗面 | K2 | ✅ | ✅ HuggingFace (tiktoken) | 160K |
| MiniMax | Text-01 / M2 | ✅ | ✅ HuggingFace | 200K |
| 百川 | Baichuan | ✅ | ✅ HuggingFace | — |
| 字节 | 豆包 | ❌ | ❌ | 不公开 |
