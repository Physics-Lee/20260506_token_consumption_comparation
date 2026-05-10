# Llama / Qwen / DeepSeek 分词器演变史

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

## 三家并排

```
        2023    2024         2025         2026
Llama:   32K ── 128K ────── 200K ──────── 200K
Qwen:   150K ── 152K ────── 152K ──────── 248K
DeepSeek:       32K → 128K ── 128K ─────── 128K
```

### 共同规律

1. **32K 已被证明是严重瓶颈。** 三家当前的编码没有一家低于 128K。Llama 1/2 的 32K 和 DeepSeek-V2 的 32K 都被抛弃——到这个尺度，中文/代码/多语言文本会被切得太碎。

2. **每次大跳跃都和训练语料多样化同步。** Llama 3 跳 4 倍是为了多语言，DeepSeek V3 跳 4 倍是为了数学+编程+多语言，Qwen 3.5 跳 63% 是社区投诉推动的多语言优化。

3. **跳跃之后趋于稳定。** 一旦找到合适的词汇量，后续几代模型倾向于沿用同一个 tokenizer，因为换 tokenizer 意味着所有已训练的 embedding 层要重来。

4. **行业正在向 200K+ 收敛。** Llama 4（200K）、Qwen 3.5（248K）、OpenAI o200k_base（200K）都在 200K 这个量级。DeepSeek（128K）最保守，可能会在下一代做跳跃。
