# 各公司 Tokenizer 的浏览器端展示策略

---

## 现状总表

| 公司 | 浏览器实时 | 原因 |
|------|:---:|------|
| OpenAI | ✅ | gpt-tokenizer UMD CDN，4 个编码包现成的 |
| 其他全部 | ❌ | tokenizer.json 在 HuggingFace，无浏览器 CDN |

唯一的可行策略：**全部预计算，嵌入 JSON。**

---

## 为什么不需要管 transformers 版本

每个模型版本的 tokenizer 是独立的静态文件，和 transformers 库版本无关：

```
Qwen 演化（3 个关键版本）:

Qwen/Qwen-7B                    → tokenizer.json  (~150K 词表)
  └─ Qwen 1.0 / 1.5 / 2 共用这套

Qwen/Qwen2.5-72B                → tokenizer.json  (151,643 词表)
  └─ 控制 token 从 3 扩展到 22，词汇量微调

Qwen/Qwen3.5-xxx                → tokenizer.json  (248,320 词表)
  └─ 首次大幅膨胀 63%

DeepSeek 演化（2 个关键版本）:

deepseek-ai/DeepSeek-V2-Lite    → tokenizer.json  (32K 词表)
  └─ DeepSeek-V2 时代

deepseek-ai/DeepSeek-V3         → tokenizer.json  (128K 词表)
  └─ V3 / R1 / V3.1 / V3.2 / V4 全部沿用
```

每个 `tokenizer.json` 是独立的 JSON 文件（1-5MB），内含完整的 `vocab` 和 `merges` 表。下载后直接用 BPE 算法编码文本即可——**和用什么版本的 Python、装没装 transformers、用 pip 还是 conda 完全无关。**

---

## 预计算流程

```
步骤 1: 下载 tokenizer.json
  https://huggingface.co/Qwen/Qwen-7B/resolve/main/tokenizer.json
  https://huggingface.co/Qwen/Qwen2.5-72B/resolve/main/tokenizer.json
  https://huggingface.co/deepseek-ai/DeepSeek-V2-Lite/resolve/main/tokenizer.json
  https://huggingface.co/deepseek-ai/DeepSeek-V3/resolve/main/tokenizer.json

步骤 2: 用 BPE 算法对 48 段文本编码
  输入: 词表 JSON + 文本
  输出: token 数量

步骤 3: 写入 data/token_counts.json
  {
    "qwen": {
      "1.0-150K": { "allende": {...}, ... },
      "2.5-151K": { "allende": {...}, ... },
      "3.5-248K": { "allende": {...}, ... }
    },
    "deepseek": {
      "V2-32K":  { "allende": {...}, ... },
      "V3-128K": { "allende": {...}, ... }
    }
  }

步骤 4: build_index.py 嵌入 HTML
  构建时读取 token_counts.json → 嵌入为 JS 变量
  运行时切换版本 → 秒读预计算数据
```

---

## 网页展示方案：时间线选择器

替换当前单一模型的下拉菜单，改成按时间线排列：

```
分词器变迁对比：

Qwen 系列:
  ○ 2023 Qwen 1.0 (150K 词表)
  ○ 2024 Qwen 2.5 (151K 词表)
  ● 2026 Qwen 3.5 (248K 词表)

DeepSeek 系列:
  ○ 2024.05 V2 (32K 词表)
  ● 2024.12 V3 (128K 词表) → 沿用至今

Llama 系列:
  ○ 2023 Llama 1/2 (32K SentencePiece)
  ● 2024 Llama 3 (128K tiktoken)
  ○ 2025 Llama 4 (200K tiktoken)
```

用户在同一系列内切换版本，对比表实时更新该版本对应的 token 数。可以直接看到"同一段文言文，Qwen 1.0 切了 500 个 token，Qwen 3.5 降到 300 个"。

---

## 唯一阻塞点

**HuggingFace 下载被墙。** 当前运行 `precompute_tokens.js` 时所有 `fetch()` 到 `huggingface.co` 全部超时。tokenizer.json 文件本身完全公开、无需认证，纯网络问题。

### 绕过方案

1. **换网络**：在其他机器/VPN 下跑一次脚本，生成 `token_counts.json` 后拷回来
2. **镜像站**：使用 `hf-mirror.com` 等国内 HuggingFace 镜像下载
3. **手动下载**：浏览器直接打开 HuggingFace 页面下载 tokenizer.json，放到本地目录，脚本从本地读
4. **CDN**：部分模型 tokenizer.json 在 jsDelivr 上有缓存（`cdn.jsdelivr.net/npm/@huggingface/...`），但覆盖不全

---

## 投入产出分析

| 能做的事 | 需要克服什么 | 产出 |
|----------|-------------|------|
| OpenAI 4 种编码 | ✅ CDN 已通 | 全模型家族的 token 消耗对比 |
| Qwen 3 代 | 💡 下载 3 个 tokenizer.json | 看到 Qwen 6 年 3 次改编码的实际效果 |
| DeepSeek 2 代 | 💡 下载 2 个 tokenizer.json | 看到 32K→128K 跳跃对中文的冲击 |
| GLM 2 代 | 💡 下载 2 个 tokenizer.json | 看到混血 tokenizer 的效率 |
| 其余各家 | 💡 各 1-2 个文件 | 横向对比生态位 |

核心价值：**让用户看到同一段文本在不同历史时期的 token 消耗曲线，证明"文言文省 token"这个假说是否成立。**
