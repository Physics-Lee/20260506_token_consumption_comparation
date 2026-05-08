# 如何更改卡片显示顺序

## 问题
用户要求将语料库阅读器中的四张语言卡片固定按 **文言 → 现代汉语 → English → Español** 的顺序排列，而不是根据 "原文优先" 来动态排序。

## 修改位置

**文件**: `code/json2html.py`

**原代码** (第39-41行):
```python
# Sort: original first, then by language order
lang_order = {'classical_chinese': 0, 'modern_chinese': 1, 'english': 2, 'spanish': 3}
texts_sorted = sorted(texts, key=lambda x: (0 if x['role'] == 'original' else 1, lang_order.get(x['language'], 99)))
```

**修改后**:
```python
# Sort by fixed language order: 文言, 现代汉语, English, Español
lang_order = {'classical_chinese': 0, 'modern_chinese': 1, 'english': 2, 'spanish': 3}
texts_sorted = sorted(texts, key=lambda x: lang_order.get(x['language'], 99))
```

## 关键区别

| | 原逻辑 | 新逻辑 |
|---|---|---|
| 排序键 | `(role_priority, lang_order)` | `(lang_order)` |
| role_priority | `0 if original else 1` | 无 |
| 效果 | 原文语言的卡片总是排第一 | 固定按语言顺序排列 |

## 示例

以"荆轲刺秦王"（原文为文言）为例：

**修改前**:
1. 文言 (原文)
2. 现代汉语 (译文)
3. English (译文)
4. Español (译文)

→ 看起来刚好一样，是因为原文恰好是文言。

**修改后**:
1. 文言
2. 现代汉语
3. English
4. Español

→ 无论原文是哪种语言，顺序永远固定。

以"阿连德最后的演讲"（原文为 Spanish）为例：

**修改前**:
1. Español (原文)
2. 文言 (译文)
3. 现代汉语 (译文)
4. English (译文)

**修改后**:
1. 文言
2. 现代汉语
3. English
4. Español

## 影响范围

此修改同时影响：
- **Comparison table**（比较表格）的行顺序
- **Text cards**（2×2 网格中的四张卡片）的排列顺序

## 重新生成

修改后运行：
```bash
python code/json2html.py
```

即可生成新的 `corpus_reader.html`。
