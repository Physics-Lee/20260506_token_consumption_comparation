# Tokenizer 名字含义

> 机器学习领域的命名往往揭示设计哲学。以下是主流 tokenizer 的名字及其含义。

| Tokenizer | 出产方 / 使用者 | 类型 | 词表大小 | 名字含义 |
|-----------|------------|------|---------|----------|
| **BPE** | Gage (1994), GPT-2, RoBERTa, DeepSeek | 自底向上合并 | 取决于训练 | **Byte Pair Encoding**。反复合并最频繁出现的字节对（byte pair）。名字直述算法：把字节两两配对编码 |
| **BBPE** | GPT-2 实际使用 | 字节级 BPE | — | **Byte-level BPE**。在字节而非字符上做 BPE，前缀"B"强调与字符级 BPE 的区别 |
| **WordPiece** | BERT, DistilBERT | 自底向上合并 | 30k~120k | 直译"词的碎片"。与 BPE 的区别：选择使训练语料似然提升最大的 pair，而非频率最高的 pair |
| **SentencePiece** | Google, T5, LLaMA, Gemma, ChatGLM, Baichuan | 封装器（含 BPE/Unigram） | 取决于底层 | 双关：把句子切成碎片，同时暗示"判刑切碎"。核心哲学：一切文本当字节流处理，无需按语言预分词 |
| **Unigram** | XLNet, ALBERT | 自顶向下剪枝 | — | 一元语法模型。算法与 BPE 相反：从大词表逐步删减，保留概率最高的子词。名字暗示基于单个子词概率独立建模 |
| **tiktoken** | OpenAI（库名） | BPE 库 | — | **Tik** = Token 谐音简化，"tic"→"tik"，加"token"读起来轻快。命名套路和 TikTok 一样——短、响、好记 |
| **cl100k_base** | GPT-4 / GPT-3.5 | tiktoken BPE | 100,256 | **c**hat **l**anguage **100k** **base**。ChatGPT 系列基础 tokenizer，100k 为近似值 |
| **o200k_base** | GPT-4o / GPT-5 / o1 / o3 | tiktoken BPE | ~200,000 | **o** 系列 **200k** **base**。o1 先用的编码，词表翻倍，中文/多语言效率提升。名字说明出身 |
| **o200k_harmony** | GPT-OSS（开源） | tiktoken BPE | ~200,000 | o200k 变体，多了 `<\|start\|>` `<\|call\|>` 等结构化 token。"harmony"暗示与开源社区的和谐 |
| **ChatGLM** | 智谱AI / 清华 | SentencePiece BBPE | 130k→65k→151k | **G**eneral **L**anguage **M**odel。三个 MASK：`[MASK]` 双向注意力、`[gMASK]` 自回归生成、`[sMASK]` 共享注意力——tokenizer 和训练目标深度耦合 |
| **Qwen** | 阿里巴巴 | tiktoken BPE（UTF-8 字节级） | 151,851 | **Q**uestion + ans**wen**。中文名"通义千问"。用 tiktoken 但词表自训，中文压缩率国产最高（C-Eval 基准 token 效率 60.8） |
| **Baichuan** | 百川智能 | SentencePiece BPE | 64k→125,696 | **百川** = hundreds of rivers。化用"海纳百川"，暗示数据多样性。v2 词表翻倍只为降低中文压缩比（0.570→0.498） |
| **DeepSeek** | 深度求索 | BPE | — | **Deep Seek**。中文 tokenizer 效率极高，chars/token 约 1.3，接近英文水平 |
| **Yi** | 零一万物（李开复） | 扩展 LLaMA tokenizer | 64,000 | **一** = one。取自"一即是全"——一个模型覆盖所有语言。在 LLaMA 词表上扩充中文，避免重训 embedding |
| **YAYI** | 中科闻歌 | BPE | 81,920 | **雅意** = refined insight。词表设为 81,920（非 80,000），确保被 128 整除以适配 GPU tensor parallelism |
| **InternLM** | 上海AI实验室 | SentencePiece | — | **Intern** Language Model。书生——暗示学术出身 |
| **XVERSE** | 元象科技 | — | 100,534 | **Universe** 变体拼写（X = 未知，Verse = 宇宙），暗示多语言覆盖 |
| **ERNIE** | 百度 | WordPiece | — | **E**nhanced **R**epresentation through K**n**owledge I**nt**e**g**ration。"知识增强"融入 tokenizer/embedding |
| **Doubao / 豆包** | 字节跳动 | 未公开 | 未公开 | 原名云雀模型（Skylark），后改名豆包。日均 4 万亿 token 调用量，国内市占率第一。tokenizer 细节（算法、词表大小、特殊 token 命名）均未公开，API 仅暴露 OpenAI 兼容接口，无法直接获取 tokenize 结果 |

## 算法对比

| 维度 | BPE | WordPiece | Unigram | SentencePiece |
|------|-----|-----------|---------|---------------|
| 方向 | 自底向上（合并） | 自底向上（合并） | 自顶向下（剪枝） | 封装器（BPE 或 Unigram） |
| 合并依据 | 频率 | 似然增益 | 概率损失最小 | 取决于底层算法 |
| 语言假设 | 有空格分词 | 有空格分词 | 有空格分词 | **无假设，字节流处理** |

## 特殊 Token 命名对比

| 模型 | EOS | 对话角色 | 其他特色 |
|------|-----|---------|---------|
| OpenAI (GPT-4o+) | `<\|endoftext\|>` | 无（ChatML 用 role 字段） | `<\|endofprompt\|>` |
| ChatGLM | `<\|endoftext\|>` | `<\|user\|>` `<\|assistant\|>` `<\|system\|>` `<\|observation\|>` | `[MASK]` `[gMASK]` `[sMASK]` `<sop>` `<eop>` |
| Qwen | `<\|endoftext\|>` | `<\|im_start\|>`user `<\|im_end\|>` | `<\|extra_0\|>` ~ `<\|extra_204\|>` 保留 |
| DeepSeek | `<｜end▁of▁sentence｜>` | ` <｜User｜>` ` <｜Assistant｜>` | 用全角竖线 `｜` 替代 `|` |
| Yi | `</s>` | `Human:` `Assistant:` | 沿袭 LLaMA 风格 |
| Baichuan | `</s>` | `<reserved_106>` `<reserved_107>` | 用保留 ID 代替具名 token |

## 黑盒

国产主流模型中，Doubao 是唯一 tokenizer 完全黑盒的——算法、词表大小、特殊 token 均未公开。

对比一下就知道差在哪：

- **Qwen / DeepSeek / ChatGLM / Baichuan**：模型开源，tokenizer 可直接加载。本地跑 `tokenizer.encode("你好")` 就能看到每个 token 的 ID 和边界，完全透明。
- **Doubao**：不开源，只提供 OpenAI 兼容的 `/v1/chat/completions` API。这个接口只接受文本、返回文本，中间 token 化过程全部藏在后端，用户永远看不到。想分析 Doubao 的中文 token 压缩率？没门。
   - 按量付费：`https://ark.cn-beijing.volces.com/api/v3`
   - Coding Plan：`https://ark.cn-beijing.volces.com/api/coding/v3`
   - 须先在火山方舟控制台创建推理接入点，拿到 Endpoint ID（`ep-xxx`），用这个 ID 当模型名调用。
