# DeepSeek-V2 词表大小迷案

## 两个矛盾的说法

| 来源 | 数字 |
|------|:---:|
| HuggingFace `DeepseekV2Config` | `vocab_size = 32000` |
| V2 论文原文 | "vocabulary size of 100K" |

## 真凶

```python
# transformers/src/transformers/models/deepseek_v2/configuration_deepseek_v2.py
class DeepseekV2Config(PreTrainedConfig):
    vocab_size: int = 32000   # ← Python 类默认值，不是模型真实词表
```

这是 HuggingFace 代码里的占位默认值。加载真实模型时会被 `config.json` 覆盖为 100K。但搜索引擎和文档自动生成的页面都把这个 32000 当成模型参数展示了出来。

## 真相

DeepSeek-V2 词表 = **100K**，和 V1 同一套，完全没改。

## 教训

HuggingFace `Config` 类的 Python 默认值 ≠ 模型真实参数。信论文，别信类构造函数的占位符。
