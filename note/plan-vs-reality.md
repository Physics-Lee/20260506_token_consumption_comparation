# 方案 vs 实现：差异分析

## 文档方案（`tokenizer-browser-strategy.md`）

- **编码方式**：纯 JS，直接下载 `tokenizer.json`，手写 BPE 算法编码
- **依赖**：零。不需要 transformers、不需要 Python、不需要 conda
- **数据格式**：按家族分组嵌套（`qwen/1.0-150K`、`deepseek/V2-32K`）
- **UI**：时间线选择器，家族内切换版本
- **覆盖**：Qwen 3 代、DeepSeek 2 代、Llama 3 代、GLM 2 代

## 当前实现

- **编码方式**：Python `precompute_tokens.py`，走 `AutoTokenizer.from_pretrained()`，加载完整 HuggingFace 模型
- **依赖**：transformers 4.57 + tiktoken，锁定 conda 环境 `token_analysis`（Python 3.11）。已踩坑：transformers 5.x 干废 DeepSeek 中文
- **数据格式**：扁平 key（`"Qwen-7B (2023)"`、`"DeepSeek-V3/R1 (2024.12)"`），不按家族嵌套
- **UI**：`<optgroup>` 分组下拉框，接近时间线但还不是
- **覆盖**：Qwen 2 代（3.5 因 HF 被墙缺 `tokenizer.json`）、DeepSeek 2 代、Phi-2、GPT-2

## 差异根源

文档的 JS 路径假设"下载一个 JSON 文件就够了"，但实际上 `AutoTokenizer` 还需要 `tokenizer_config.json` 处理特殊 token 映射、BOS/EOS 标签等。JS 路径的手写 BPE 只处理了基础合并，没处理特殊 token 注入——两者的 token 数可能对不齐。

当前 Python 路径踩了 transformers 版本的坑，但它处理特殊 token 是正确的。JS 路径如果能补齐特殊 token 处理，就可以彻底扔掉 transformers。

## 结论

两条路对齐需要做：让 `precompute_tokens.js` 读取 `tokenizer_config.json` 并正确注入 special tokens，验证产出和 Python 路径一致。做完这一步，"不需要 transformers"那条才成立。
