# 懿轩注

https://github.com/openai/tiktoken/blob/main/tiktoken/model.py

```python
# TODO: these will likely be replaced by an API endpoint
MODEL_PREFIX_TO_ENCODING: dict[str, str] = {
    "o1-": "o200k_base",
    "o3-": "o200k_base",
    "o4-mini-": "o200k_base",
    # chat
    "gpt-5-": "o200k_base",
    "gpt-4.5-": "o200k_base",
    "gpt-4.1-": "o200k_base",
    "chatgpt-4o-": "o200k_base",
    "gpt-4o-": "o200k_base",  # e.g., gpt-4o-2024-05-13
    "gpt-4-": "cl100k_base",  # e.g., gpt-4-0314, etc., plus gpt-4-32k
    "gpt-3.5-turbo-": "cl100k_base",  # e.g, gpt-3.5-turbo-0301, -0401, etc.
    "gpt-35-turbo-": "cl100k_base",  # Azure deployment name
    "gpt-oss-": "o200k_harmony",
    # fine-tuned
    "ft:gpt-4o": "o200k_base",
    "ft:gpt-4": "cl100k_base",
    "ft:gpt-3.5-turbo": "cl100k_base",
    "ft:davinci-002": "cl100k_base",
    "ft:babbage-002": "cl100k_base",
}

MODEL_TO_ENCODING: dict[str, str] = {
    # reasoning
    "o1": "o200k_base",
    "o3": "o200k_base",
    "o4-mini": "o200k_base",
    # chat
    "gpt-5": "o200k_base",
    "gpt-4.1": "o200k_base",
    "gpt-4o": "o200k_base",
    "gpt-4": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
    "gpt-3.5": "cl100k_base",  # Common shorthand
    "gpt-35-turbo": "cl100k_base",  # Azure deployment name
    # base
    "davinci-002": "cl100k_base",
    "babbage-002": "cl100k_base",
    # embeddings
    "text-embedding-ada-002": "cl100k_base",
    "text-embedding-3-small": "cl100k_base",
    "text-embedding-3-large": "cl100k_base",
    # DEPRECATED MODELS
    # text (DEPRECATED)
    "text-davinci-003": "p50k_base",
    "text-davinci-002": "p50k_base",
    "text-davinci-001": "r50k_base",
    "text-curie-001": "r50k_base",
    "text-babbage-001": "r50k_base",
    "text-ada-001": "r50k_base",
    "davinci": "r50k_base",
    "curie": "r50k_base",
    "babbage": "r50k_base",
    "ada": "r50k_base",
    # code (DEPRECATED)
    "code-davinci-002": "p50k_base",
    "code-davinci-001": "p50k_base",
    "code-cushman-002": "p50k_base",
    "code-cushman-001": "p50k_base",
    "davinci-codex": "p50k_base",
    "cushman-codex": "p50k_base",
    # edit (DEPRECATED)
    "text-davinci-edit-001": "p50k_edit",
    "code-davinci-edit-001": "p50k_edit",
    # old embeddings (DEPRECATED)
    "text-similarity-davinci-001": "r50k_base",
    "text-similarity-curie-001": "r50k_base",
    "text-similarity-babbage-001": "r50k_base",
    "text-similarity-ada-001": "r50k_base",
    "text-search-davinci-doc-001": "r50k_base",
    "text-search-curie-doc-001": "r50k_base",
    "text-search-babbage-doc-001": "r50k_base",
    "text-search-ada-doc-001": "r50k_base",
    "code-search-babbage-code-001": "r50k_base",
    "code-search-ada-code-001": "r50k_base",
    # open source
    "gpt2": "gpt2",
    "gpt-2": "gpt2",  # Maintains consistency with gpt-4
}

```

这俩文件里怎么没有5.4 5.5，也没有oss？

> 1. gpt-5.4 / gpt-5.5 没出现在 MODEL_TO_ENCODING
> 不需要。它们走的是前缀匹配：
> MODEL_PREFIX_TO_ENCODING = {
>     "gpt-5-": "o200k_base",   # ← 这一行就够了
> }
> 当代码收到 "gpt-5.4" 时：
> ① 先查 MODEL_TO_ENCODING → 没有精确匹配
> ② 再遍历 PREFIX 表 → "gpt-5.4" 以 "gpt-5-" 开头？不是
>    "gpt-5.4-" 以 "gpt-5-" 开头？是的！→ o200k_base ✓
> 所以只要模型名以 gpt-5 开头，自动匹配，不需要逐一手动添加。但注意这个匹配逻辑：实际调用时如果是 "gpt-5.4"（不带横杠），前缀 "gpt-5-" 不会命中，因为 "gpt-5.4" 不以 "gpt-5-" 开头（差一个点 vs 横杠）。这就看 tiktoken 库的发布时间点和 OpenAI 的实际命名——如果 gpt-5.4 发布时用的是 "gpt-5.4-2025-xx-xx" 这种格式，前缀就能命中。
> 2. gpt-oss 没出现在 MODEL_TO_ENCODING
> 它出现在 PREFIX 表里了：
> "gpt-oss-": "o200k_harmony",
> 不放进 MODEL_TO_ENCODING 是因为没有 "gpt-oss" 这个不带版本号的简称——用户调 API 时用的都是 gpt-oss-20b、gpt-oss-120b 这种带参数的全名，前缀匹配就够了。