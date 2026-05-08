# 语言选择：Python vs JavaScript

## 判断

**`code/` 目录保持纯 Python。** HTML 内嵌的浏览器 JS 不参与此决策。

## 理由

核心工作是 **token 分析**（`analyze_tokens.py`、`test_tokenizer.py`），这必须用 Python：

- `tiktoken`（OpenAI tokenizer）只有 Python 绑定
- `transformers`（HuggingFace tokenizer）只有 Python 绑定
- HTML 生成（`json2html.py`）只是辅助构建步骤，没必要为此引入 Node.js 运行时

## 什么时候用 JS？

如果未来采用"浏览器端动态渲染"方案（即 HTML 只是一个壳，运行时 fetch `data/*.json` 动态构建 DOM），那么 JS 是自然选择。但即使如此：

- 那是 HTML 内嵌的 `<script>` 标签里的浏览器 JS
- 和 `code/` 目录里的构建脚本是两层不同的东西
- 不会因为 HTML 里有 JS 就把 `code/` 里的 Python 换成 Node.js

## 结论

不要制造不必要的多语言混用。`code/` = Python，HTML `<script>` = JS（本来就是），各司其职。
