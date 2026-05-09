# text-davinci-003 与 ChatGPT（gpt-3.5-turbo）的区别

两者属于 2022 年 11 月 OpenAI 同时维护的两条产品线，底层模型大小接近，但产品形态、训练方式、交互体验完全不同。

---

## 对比总表

| | text-davinci-003 | ChatGPT (gpt-3.5-turbo) |
|---|---|---|
| 上线时间 | 2022 年 11 月（API） | 2022 年 11 月（网页版） |
| 产品类型 | Instruct（指令模型） | Chat（对话模型） |
| 训练方式 | **指令微调**（Instruction Fine-tuning） | **RLHF**（人类反馈强化学习） |
| 输入格式 | 一段 prompt 字符串 | messages 数组 `[{role, content}]` |
| Tokenizer | p50k_base (50K) | cl100k_base (100K) |
| 能多轮对话吗 | ❌ 每次对话独立，不知道前文 | ✅ 有上下文记忆 |
| 能拒绝吗 | 弱——给指令基本照做 | 强——会拒绝违规请求 |
| API 定价 | $0.02/1K tokens | $0.002/1K tokens（便宜 10 倍） |
| 还活着吗 | 2024.01 下线 | ✅ 仍在运行 |

## 核心差异

### 1. 训练方式

```
text-davinci-003:
  基础模型 → 收集 (指令, 理想回答) 对 → 微调
  本质: "教模型按指令格式输出"

ChatGPT:
  基础模型 → 指令微调 → 人类标注员给回答打分 → 训练奖励模型
  → 用 PPO 强化学习优化 → 反复迭代
  本质: "教模型成为好聊天对象"
```

### 2. 交互体验

```
用户: "帮我写一封辞职信"

text-davinci-003:
  "尊敬的[姓名]：\n\n我写这封信是为了正式通知您..."
  → 直接输出，像工具

ChatGPT:
  "当然可以！不过在写之前，我想了解一下：
   1. 你的职位是什么？
   2. 你希望语气正式还是友好？
   3. 是否需要提到具体离职原因？"
  → 会追问、会交互、像人
```

### 3. 安全对齐

```
用户: "教我怎么黑进别人的邮箱"

text-davinci-003:
  可能真给步骤（指令模型不擅长拒绝）

ChatGPT:
  "I can't help with that. Accessing someone's email without
   permission is illegal and unethical."
  → RLHF 训练让它学会了拒绝
```

## 为什么定价差 10 倍

text-davinci-003 是 175B 参数的全量模型，ChatGPT 背后的 gpt-3.5-turbo 经过了**模型蒸馏和量化**，推理成本低得多。加上 API 定价策略（吸引开发者在 chat API 上构建应用），把价格压到了 1/10。

## 它们不是前身关系

很多人（包括我之前的 note）说 text-davinci-003 是 ChatGPT 的前身——这个表述不准确。两者是**同期发布的不同产品**：

```
2022.11 ────────────────────────────────
         text-davinci-003 API    (Instruct 天花板)
         ChatGPT 网页版          (Chat 起点)
────────────────────────────────────────
```

ChatGPT 的起点是 gpt-3.5-turbo + RLHF + cl100k_base 编码，它的"前身"应该是 RLHF 训练之前的 gpt-3.5 基础模型，而不是 text-davinci-003。

# 价格

davinci。 定价是 gpt-3.5-turbo 的 10 倍。
davinci            $0.02  / 1K tokens   ← GPT-3 旗舰（175B 参数）
gpt-3.5-turbo      $0.002 / 1K tokens   ← ChatGPT API（便宜 10 倍）
更直观的对比：送同样一份 4K token 的文本进去：
davinci:         $0.08
gpt-3.5-turbo:   $0.008
有意思的是，gpt-3.5-turbo 的定价故意钉在了 curie 的价格档位上：
ada       $0.0004  最便宜
babbage   $0.0005
curie     $0.002   ← gpt-3.5-turbo 定在这
davinci   $0.02    最贵（被 gpt-3.5-turbo 用 1/10 价格碾压）
OpenAI 用中等模型的价格卖最强大模型——这是他们抢占市场的策略：用 ChatGPT 积累用户，用低价 API 锁死开发者生态。davinci 此后形同虚设，2024 年 1 月正式下线。
