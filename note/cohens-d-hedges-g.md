# Cohen's d 与 Hedge's g 计算方式

## 背景

配对设计：同一篇文章，用文言和现代汉语分别 tokenize，得到一对 token 数。

## 配对 Cohen's d

对于 n 对差值 $d_i = x_i^{\text{文言}} - x_i^{\text{现代汉语}}$：

$$
d = \frac{\bar{d}}{s_d}
$$

其中 $\bar{d}$ 是差值均值，$s_d$ 是差值的样本标准差：

$$
s_d = \sqrt{\frac{\sum(d_i - \bar{d})^2}{n-1}}
$$

> 配对设计的 d 用差值标准差做分母，不是合并标准差。这是配对 t 检验对应的效应量。

## Hedge's g（小样本修正）

Cohen's d 在小样本下有偏（轻微高估），Hedge's g 用修正因子：

$$
g = d \times \left(1 - \frac{3}{4n - 9}\right)
$$

n = 5 时修正因子 ≈ 0.727，n = 7 时 ≈ 0.842，n → ∞ 时 → 1。

## 解释

| |d| 或 |g| | 含义 |
|---|---|---|
| 0.2 | 小 |
| 0.5 | 中 |
| 0.8 | 大 |

> 本项目中 d 和 g 恒为非负——代码在 `abs(mean_d / sd_d)` 已取绝对值，不关心方向（方向由单边假设检验 H₁ 决定）。

## 代码位置

`code/build_index.py` 中 `compute_pvalues` 函数末尾：

```python
mean_d = sum(diffs) / n
sd_d = (sum((d - mean_d)**2 for d in diffs) / (n - 1)) ** 0.5
d_val = abs(mean_d / sd_d) if sd_d > 0 else 0
g_val = d_val * (1 - 3/(4*n - 9)) if n > 2 else d_val
```
