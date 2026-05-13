# 结论表格的实现原理

## 需求

在【统计分析】页末尾添加一张极简结论表：

- 每一行是一个 tokenizer
- 只有两列：原文为文言组（文言 vs 某语言）、原文为非文言组（文言 vs 某语言）
- 不显示原始 p 值，只显示判断结果：BH-FDR 校正后 p < 0.10 为 ✓，否则为 ✗

目前已实现两张：文言文 vs 现代汉语、文言文 vs 英语。

---

## 数据基础

结论表格依赖 `pvalue_data`——在 `build_index.py` 中预先计算并存储了三种校正方法的结果：

| 字段 | 含义 |
|------|------|
| `fisher_p` | 精确配对置换检验原始 p 值 |
| `fisher_bh` | Benjamini-Hochberg FDR 校正后 p 值（q 值） |
| `fisher_holm` | Holm-Bonferroni 校正后 p 值 |
| `fisher_bonf` | Bonferroni 校正后 p 值 |
| `wilcoxon_*` | Wilcoxon 符号秩检验对应版本 |

结论表格选用 `fisher_bh`（BH-FDR 校正后的置换检验 p 值），理由见 `note/multiple-comparison-corrections.md`。

---

## 实现方案

### 1. 为什么不在浏览器端用 JavaScript 动态渲染？

p 值和校正结果全部在 Python 端（`build_index.py`）完成计算，通过 `pvalue_json` 注入前端。理论上可以用 JS 在浏览器里动态画这张表。但选择**静态生成**的原因：

- 结论表格不需要随 tokenizer 切换而改变（本身就是对所有 tokenizer 的汇总）
- 静态 HTML 更简单，无额外 JS 逻辑，页面加载即呈现
- 避免和已有 `updatePvalues`/`updateEffects` 的动态更新逻辑纠缠

### 2. 代码位置和逻辑

`code/build_index.py`，在 `pvalue_data` 完成 BH 校正之后、`sections` 列表组装之前：

```python
# Build conclusion table for stats section
conclusion_rows = []
for name in sorted(pvalue_data['cc'].keys()):
    cc_bh = pvalue_data['cc'][name].get('modern_chinese', {}).get('fisher_bh', float('nan'))
    other_bh = pvalue_data['other'][name].get('modern_chinese', {}).get('fisher_bh', float('nan'))
    cc_mark = '✓' if cc_bh < 0.10 else '✗'
    other_mark = '✓' if other_bh < 0.10 else '✗'
    conclusion_rows.append(
        f'<tr><td class="summary-article-name">{name}</td>'
        f'<td>{cc_mark}</td><td>{other_mark}</td></tr>'
    )

conclusion_html = f"""<div class="summary-table-wrap" ...>...</div>"""

# 把结论表格插入到 stats_section 的 </section> 之前
stats_section = stats_section.replace(
    '        </section>',
    conclusion_html + '\n        </section>'
)
```

### 3. 关键细节：字符串替换

`stats_section` 是一个 f-string，在 Python 执行到该行时就已经被求值为一个普通字符串。它的末尾是：

```html
            </div>
        </section>
```

**注意**：f-string 的闭合定界符 `'''` **不属于**字符串内容，所以不能用 `"        </section>\n    '''"` 做匹配。实际匹配的是 `'        </section>'`——这在整个 `stats_section` 中只出现一次（最外层 `<section id="stats">` 的结束标签），所以替换是安全的。

### 4. 英语表格的复用

第二张表格（vs English）完全复用同一套逻辑，只是把 `.get('modern_chinese', ...)` 改为 `.get('english', ...)`，然后把两张表格的 HTML 拼接后一次性插入：

```python
stats_section = stats_section.replace(
    '        </section>',
    conclusion_html + conclusion_html_en + '\n        </section>'
)
```

---

## 为什么不显示原始 p 值数字？

这是需求层面的选择。结论表格的设计目标是**让读者一眼看到"哪些 tokenizer 支持文言文更省 token 这一命题"**，而不是展示精确的统计量。

如果未来需要同时显示数字，可以改为：

```python
cc_mark = f'{cc_bh:.3f} ✓' if cc_bh < 0.10 else f'{cc_bh:.3f} ✗'
```

---

## 相关文件

- `code/build_index.py`：生成逻辑（搜索 "Build conclusion table"）
- `note/multiple-comparison-corrections.md`：BH-FDR 校正方法说明
- `index.html`：产物（搜索 "结论：文言文是否比"）
