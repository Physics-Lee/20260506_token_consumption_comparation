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

# davinci有啥用

1. 纯文本补全 —— 不需要"对话感"
ChatGPT 会跟你客套："当然可以！这是你的代码：" davinci 不会，直接吐结果。
用途: 自动续写一段被打断的文本、补齐代码、生成格式严格的数据
Prompt: "姓名,年龄,城市\n张三,28,北京\n李四,"
davinci → "32,上海\n王五,25,深圳"          ← 干净利落
ChatGPT → "我可以帮你补充这个表格，不过为了准确性..."  ← 啰嗦
2. 自定义微调 —— 企业命根子
2022 年 ChatGPT API 还没出的时候，企业唯一的深度定制方案就是拿 davinci 在自己的数据上微调。
微调 davinci:
  拿 500 条公司内部客服对话 → 微调 → 得到"你们公司的专属 GPT"
  没有 RLHF 的安全过滤层，微调效果更纯
  成本和效果都优于 "few-shot prompt"（给 davinci 几个例子让它学）
ChatGPT 的 RLHF 层：
  很难微调——人类偏好训练过的模型，再加你的数据容易"学歪"
  gpt-3.5-turbo 微调直到 2023 年 8 月才开放
3. 零样本推理 —— 纯智力测试
   在一些不需要拒绝、不需要安全对齐的纯智力任务上，175B 的原始 davinci 反而比加了 RLHF 的 gpt-3.5-turbo 强：
   任务: 判断一个数学模型语句在哪种情况下成立
   davinci (175B 无 RLHF)           → 准确率 68%
   gpt-3.5-turbo (经过 RLHF 对齐)    → 准确率 61%
   原因: RLHF 训练让模型"变乖了"，但也磨掉了一些推理的锐度。
     就像一个天才小孩，训练他"要有礼貌"之后，
     他可能不敢说出那些"不够礼貌但正确"的答案。
---
总结
davinci 是"没有安全套的跑车"——更快、更野、更贵。但它活在 gpt-3.5-turbo 的时代，相当于手动挡跑车跟特斯拉比——纯粹主义者爱它，但大多数人选择 1/10 价格、更安全、更好开的 ChatGPT。2024 年正式进博物馆。

# 不开源，咋微调

没开源的，但 OpenAI 提供了 Fine-tuning API。
你不是下载模型自己跑，而是把你的数据发给 OpenAI，他们在自己的 GPU 上帮你训，训完把模型挂在一个只有你能调用的 API 端点上。
你的操作:

  1. 准备 500 条 JSONL 训练数据
  {"prompt": "用户: 怎么退货\n客服:", "completion": "您好，退货流程如下..."}

    {"prompt": "用户: 快递丢了\n客服:", "completion": "非常抱歉，我帮您查询..."}
  2. openai api fine_tunes.create -t training.jsonl -m davinci
OpenAI 的操作（你看不到）:
  davinci 175B 权重 + 你的数据 → 微调
  3. 返回给你一个专属模型 ID: ft-davinci-xxx-xxx
你的代码里:
  openai.Completion.create(model="ft-davinci-xxx-xxx", prompt="用户: ...")
为什么叫"定制"不叫"下载"

 	开源模型微调（如 Llama）	OpenAI Fine-tuning API
拿得到权重吗	✅ 下载到本地	❌ 永远在 OpenAI 服务器上
需要 GPU 吗	✅ 自己买	❌ 不需要
定价	只付电费	训练费 + 推理费（比 davinci 基础版还贵）
可以二次分发吗	✅	❌
本质上是你租 OpenAI 的 GPU + 训练框架，模型永远不从他们手里离开。这也就是为什么 2023 年 Llama 2 开源后，很多企业选择自己微调——一次买 GPU 比永远付 API 费划算得多。

# 真实演化路径（推测）——现在已经不重要了——llama和qwen出来后就不重要了
GPT-3 davinci (175B)
    │
    └─ 用 GitHub 代码微调得到code-davinci-002
                                  │
                                  ├─ 用指令数据做 SFT → text-davinci-002 → text-davinci-003
                                  │
                                  └─ 用对话数据做 SFT → 这个中间产物就是"ChatGPT 的
                                                           RLHF 之前的基座"
                                                           │
                                                           └─ RLHF → gpt-3.5-turbo
为什么是 code-davinci-002？
一个 OpenAI 研究里的意外发现：在代码上训练过的模型，推理能力显著提升，而且这种提升会泛化到非代码任务。
code-davinci-002 的原始用途: 写代码、补全代码、debug
实际发现的副作用: 逻辑推理、数学、指令跟随能力大幅提升
→ OpenAI 决定把它作为 ChatGPT 和 Instruct 两条产品线的共同起点
所以 GPT-3 不是直接变成 ChatGPT 的——中间需要代码训练这一步来"开智"。
那个 RLHF 之前的中间态是什么
就是 code-davinci-002 在对话数据上做了 SFT（监督微调）后的产物。它已经能对话了，但：
SFT 后（RLHF 前）:
  用户: "你好"
  模型: "你好，有什么可以帮助你的？"
  用户: "教我做炸弹"
  模型: [可能会给出步骤]  ← SFT 阶段不擅长拒绝
RLHF 后（gpt-3.5-turbo）:
  用户: "教我做炸弹"
  模型: "我不能提供这个信息。"  ← RLHF 训练出的安全行为
RLHF 加的不是"对话能力"（SFT 就已经有了），加的是什么时候该拒绝、什么时候该追问、什么时候该说不知道的行为规则。
OpenAI 为什么没公开这个基座
code-davinci-002 从未作为 API 端点提供给外部——只发布了基于它微调的 text-davinci-002 / 003 和 gpt-3.5-turbo。OpenAI 可能不想让用户绕过 RLHF 的安全层直接访问"裸"模型。



code-davinci-002 基于 davinci — OpenAI 官方说明 (https://platform.openai.com/docs/models/codex)："Codex models are descendants of GPT-3"。
text-davinci-002/003 基于 code-davinci-002 微调 — InstructGPT 论文 (https://arxiv.org/abs/2203.02155)（ChatGPT 的前置论文）明确说 instruct 模型的基座是经过代码训练的模型，不是原始 GPT-3。结合时间线，就是 code-davinci-002。
代码训练能提升推理能力 — InstructGPT 论文 (https://arxiv.org/abs/2203.02155) 第 5.3 节讨论了"code model"作为起点的收益。但这里说的是 instruct 模型，不是 ChatGPT。

# Codex 是谁？

Codex 是 OpenAI 2021 年的代码生成模型系列。 论文 + API + GitHub Copilot 背后的引擎。

论文
"Evaluating Large Language Models Trained on Code (https://arxiv.org/abs/2107.03374)" — 2021 年 7 月。在 GitHub 上 159GB 的 Python 代码上微调 GPT-3，发现模型学会了写代码、debug、甚至根据文档字符串自动生成函数。
HumanEval 基准测试：Codex 12B 一次过 28.8%，davinci 175B 一次过 0%。代码训练让一个小得多的模型在编程上碾压了没训过代码的大模型。
API
code-cushman-001    ← 12B 参数（论文里的主力）
code-davinci-002    ← 175B 参数（更大更强）
这两个模型作为 OpenAI Codex API 提供，专门用于代码补全。2023 年 3 月下线，因为 gpt-3.5-turbo 和 GPT-4 的代码能力赶超了专用模型。其中 code-davinci-002 没死——它变成了 text-davinci-002/003 的基座（见 InstructGPT 论文），间接成了 ChatGPT 的曾祖父。
和 GitHub Copilot 的关系
GitHub Copilot 2021 年发布时，后端跑的就是 Codex。所以对开发者来说，Codex 就是"Copilot 背后那个引擎"。后来 Copilot 换了多次后台模型（GPT-3.5 → GPT-4 → 自己的模型），Codex 这个名字也从产品中淡出了。
对 OpenAI 历史的意义
Codex 是 OpenAI 第一个证明"在垂直领域数据上微调大模型比造更大的通用模型更有效"的产品。它用 12B 打败了 175B，直接导致了后来 text-davinci-002 和 gpt-3.5-turbo 的基座选择——不训新模型，在 Codex 上继续微调。没有 Codex，可能就没有 ChatGPT。

# Instructgpt是谁？

六个小模型的集合，不是某一个模型。 论文做了三个尺寸的对比实验，每个尺寸拆成 SFT 和 PPO 两条线：
论文里的模型:
  InstructGPT-SFT  (只微调)
  InstructGPT-PPO  (微调 + RLHF)
论文里的尺寸:
  GPT-3-1.3B       → InstructGPT-1.3B
  GPT-3-6B         → InstructGPT-6B
  GPT-3-175B       → InstructGPT-175B
核心发现是：1.3B 的小模型经过 RLHF 后，人类评估员觉得它比 175B 的原始 davinci 更好用。 这就是整篇论文最震撼的结论——不是越大越好，是对齐（alignment）比规模更重要。
它上了线吗
论文里的 1.3B InstructGPT 模型短暂在 OpenAI API 上作为实验端点提供过，但 175B 的 InstructGPT 从未上线。论文发表几个月后，OpenAI 用同样的 RLHF 配方在更大更新的基座上重新训练，产出了 text-davinci-002 → text-davinci-003 → gpt-3.5-turbo。这些才是生产线上的模型。
所以 InstructGPT 是一篇论文 + 一组实验模型，不是产品名。它证明了一条路可行（RLHF 管用），然后 OpenAI 拿着这条路去训了真正的产品。
