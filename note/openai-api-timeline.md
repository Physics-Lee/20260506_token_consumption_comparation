# OpenAI API 上线时间线

---

## 完整时间线

```
2020.06  GPT-3 API 上线
         ├─ 模型: davinci, curie, babbage, ada
         ├─ 类型: 纯文本补全（text completion）
         ├─ 编码: r50k_base (50K)
         └─ 格式: 一个字符串 prompt → 模型续写

2022.01  Instruct 模型上线
         ├─ 模型: text-davinci-002, text-davinci-003
         ├─ 类型: 指令微调后的文本补全（更听话）
         ├─ 编码: p50k_base (50K)
         └─ 格式: 仍是一个字符串 prompt → 续写

2022.11  ChatGPT 上线
         ├─ 模型: gpt-3.5-turbo + RLHF
         ├─ 类型: 对话（Conversation）
         ├─ 编码: cl100k_base (100K)
         ├─ 格式: messages 数组 [{role:"user", content:"..."}]
         └─ API: ❌ 未开放，仅有聊天界面

2023.03  gpt-3.5-turbo API 上线（ChatGPT API）
         ├─ 比 ChatGPT 晚了 4 个月
         ├─ 原因: RLHF 模型的安全测试 + chat format 协议设计
         └─ 首次引入 messages 格式到 API

2023.03  GPT-4 发布（网页版 + API 同日）
         ├─ 网页版: ChatGPT Plus 用户当天即可切换 GPT-4 模型
         ├─ API: 同天开放，但仅限 waitlist 用户
         ├─ 编码: cl100k_base (100K)

2023.07  GPT-4 API 结束 waitlist，面向全部付费开发者开放

2024.05  GPT-4o 上线
         ├─ 模型: gpt-4o, gpt-4o-mini
         ├─ 编码: o200k_base (200K)
         └─ 多模态（文本+图片+音频）
```

## 编码和 API 时代的对应

```
2020 ───────── r50k_base ───────── GPT-3 纯文本补全 API
2021 ───────── p50k_base ───────── Instruct 模型
2022 ───────  cl100k_base ─────── ChatGPT + GPT-4
2024 ───────  o200k_base ──────── GPT-4o + GPT-5.x
```

## ChatGPT 上线时为什么没开 API

1. **RLHF 模型安全测试不够**：instruct 模型只做了指令微调，行为较可预测。RLHF 加了人类偏好训练，模型会"拒绝回答"、"主动纠错"、"带有语气"——这些行为在 API 场景下需要额外安全评估。

2. **Chat Format 是全新协议**：之前的 API 输入是一个字符串，输出是续写。ChatGPT 引入了 `messages` 数组（system/user/assistant 角色），API 协议需要重新设计、做 backward compatibility。

3. **容量不足**：ChatGPT 上线一周用户破百万，OpenAI 需要先保证聊天界面的稳定性，再考虑分算力给 API。

## 关键句式

> ChatGPT 上线时没有 API。gpt-3.5-turbo API 比 ChatGPT 晚了 4 个月（2023 年 3 月）。在那之前，开发者只能通过 text-davinci-003 API 调用——那是 instruct 模型，不是 chat 模型。
