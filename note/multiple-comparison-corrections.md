# 多重比较校正方法对比

## 问题背景

`build_index.py` 的统计分析部分，每个分词器在同一组内同时进行 3 次单边检验（文言 vs 现代汉语、vs English、vs Español）。如果不做校正，"族错误率"（Family-Wise Error Rate, FWER）会膨胀——即使零假设全部为真，纯凭运气也会有约 $3 \times 0.05 = 15\%$ 的概率至少出现一次"显著"。

本文档对比三种常用校正方法，并给出本项目的选择建议。

---

## 三种方法

### 1. Bonferroni（最简单、最保守）

**原理**：将显著性阈值除以比较次数 $m$。

$$
\text{拒绝 } H_0 \iff p \leq \frac{\alpha}{m}
$$

等价于报告校正后 p 值：$p_{\text{adj}} = \min(m \cdot p,\; 1)$。

**特点**：
- 控制 FWER（族错误率），即"至少犯一次假阳性"的概率 $\leq \alpha$。
- 假设所有检验相互独立，即使不独立也仍然保守地控制 FWER。
- **过于保守**：检验之间往往存在正相关（同一分词器下三种语言的 p 值不是独立的），Bonferroni 会浪费功效。

**本项目**：$m=3$，校正后阈值 $0.05/3 \approx 0.0167$。

---

### 2. Holm-Bonferroni（逐步校正，推荐用于 FWER 控制）

**原理**：逐步下降校正，比 Bonferroni 更有功效（power），但仍严格控制 FWER。

将 $m$ 个原始 p 值从小到大排序：$p_{(1)} \leq p_{(2)} \leq \dots \leq p_{(m)}$。

对每个 $p_{(i)}$ 计算：

$$
p_{\text{adj},(i)} = \max_{j \leq i} \left\{ \min\left( p_{(j)} \times (m - j + 1),\; 1 \right) \right\}
$$

**决策规则**：找到最大的 $k$，使得 $p_{(i)} \leq \alpha / (m - i + 1)$ 对所有 $i \leq k$ 成立，则拒绝前 $k$ 个假设。

**特点**：
- 同样控制 FWER。
- **永远不比 Bonferroni 更保守**，通常更宽松（更有功效）。
- 不假设检验独立性。

**本项目**：$m=3$，三个 p 值分别乘以 3、2、1，再取逐步最大值。

---

### 3. Benjamini-Hochberg（控制 FDR，推荐用于探索性分析）

**原理**：控制**假发现率**（False Discovery Rate），即"被拒绝的假设中假阳性的期望比例" $\leq \alpha$。

将 p 值从大到小处理（或等价地，从小到大找临界值）：

$$
p_{\text{adj},(i)} = \min_{j \geq i} \left\{ \min\left( p_{(j)} \times \frac{m}{j},\; 1 \right) \right\}
$$

等价决策规则：找到最大的 $k$，使得 $p_{(k)} \leq \alpha \cdot \frac{k}{m}$，则拒绝前 $k$ 个假设。

**特点**：
- 控制 FDR，而非 FWER。允许一定比例的假阳性，换得更高的真实发现率。
- 在检验相互独立或满足正相关条件下成立（本项目的三种语言比较基本满足）。
- **比 Holm 更宽松**，特别适合探索性研究和筛选假设。

**本项目**：$m=3$，乘数分别为 $3/3=1$、$3/2=1.5$、$3/1=3$（从小到大时）。

---

## 数值对比示例

假设某分词器在"原文为文言"组（$n=5$）得到三个原始 p 值：

| 比较 | 原始 $p$ |
|------|---------|
| 文言 vs 现代汉语 | 0.031 |
| 文言 vs English | 0.062 |
| 文言 vs Español | 0.125 |

三种方法的校正后 p 值（q 值）：

| 比较 | Bonferroni | Holm | BH-FDR |
|------|-----------|------|--------|
| 文言 vs 现代汉语 | $0.031 \times 3 = \mathbf{0.093}$ | $\max(0.093) = \mathbf{0.093}$ | $0.031 \times 3/3 = \mathbf{0.031}$ |
| 文言 vs English | $0.062 \times 3 = 0.186$ | $\max(0.093, 0.124) = \mathbf{0.124}$ | $0.062 \times 3/2 = 0.093$ → 取 min 得 $\mathbf{0.031}$ |
| 文言 vs Español | $0.125 \times 3 = 0.375$ | $\max(0.124, 0.125) = \mathbf{0.125}$ | $0.125 \times 3/1 = 0.375$ → 取 min 得 $\mathbf{0.031}$ |

**结论差异**：
- **Bonferroni / Holm**：只有"vs 现代汉语"在校正后接近显著（0.093），其余不显著。严格，但几乎扼杀了所有信号。
- **BH-FDR**："vs 现代汉语"保持 0.031 显著（$<0.05$），其余两个跟随调整后被前项拉低到 0.031。

> 注意：BH 的"跟随调整"（monotonicity）在本例中表现为后两项被第一项拉低，这是算法的正常性质。

---

## 另一个关键场景：$n=5$ 的最小可能 p 值

精确配对置换检验的最小非零 p 值 = $1/2^5 = 0.03125$。

| 方法 | 校正后最小 p | 能否 $<0.05$ |
|------|------------|------------|
| 不做校正 | 0.031 | ✅ 能 |
| Bonferroni | $0.031 \times 3 = 0.094$ | ❌ 不能 |
| Holm | $0.031 \times 3 = 0.094$ | ❌ 不能 |
| BH-FDR | $0.031 \times 3/3 = 0.031$ | ✅ 能（若为该分词器内最小 p 值）|

**这意味着**：如果要求控制 FWER（Holm 或 Bonferroni），$n=5$ 组无论文言领先幅度多大，都**不可能显著**。这是功效（power）灾难，不是方法错误。

---

## 方法选择建议

| 你的目标 | 推荐方法 | 理由 |
|---------|---------|------|
| **保守确认"绝对可靠"的结论** | Holm | 严格控制 FWER，适合验证性研究 |
| **在有限数据中发现值得关注的模式** | **BH-FDR（推荐）** | 本项目是探索性语料库分析，假阳性代价低，需要保留检出能力 |
| 快速心算 / 口头报告 | Bonferroni | 最简单，$\alpha/m$ 口算即可 |

### 本项目的选择

建议采用 **Benjamini-Hochberg（FDR）**，校正粒度为**每个分词器 × 每个原文语言组内部**（$m=3$）。

**理由**：
1. **探索性研究**：这不是药理学试验，假阳性不会导致人身伤害或资源错配。
2. **样本量极小**：$n=5$ 时 Holm 会彻底消除所有显著性，使"原文为文言"组（核心样本）在统计表格中失声。
3. **现代 NLP 惯例**：计算语言学和多语言对比研究通常报告 FDR 校正后的 q 值。
4. **有明确先验方向**：研究问题"文言能否省 token"是定向假设，不是盲目 fishing。

---

## 代码参考

### BH-FDR 校正（纯 Python，无额外依赖）

```python
def bh_adjust(values):
    """Benjamini-Hochberg FDR control. Returns q-values."""
    valid = [(i, v) for i, v in enumerate(values) if v == v]  # 排除 NaN
    if not valid:
        return list(values)
    
    # 从大到小遍历
    indexed = sorted(valid, key=lambda x: x[1], reverse=True)
    m = len(valid)
    adjusted_map = {}
    prev = 1.0
    for rank, (orig_idx, p) in enumerate(indexed):
        k = m - rank          # 当前是第 k 大（从 1 计数）
        raw = p * m / k
        adj = min(raw, prev)
        adjusted_map[orig_idx] = adj
        prev = adj
    
    result = list(values)
    for i, v in enumerate(values):
        result[i] = adjusted_map.get(i, float('nan'))
    return result


def apply_fdr_correction(pvalue_data):
    """在每个 (group, model) 组合内部对 3 种语言做 BH-FDR 校正。"""
    for group in pvalue_data:
        for model_name, lang_results in pvalue_data[group].items():
            langs = ['modern_chinese', 'english', 'spanish']
            fisher_ps, wilcox_ps, valid_langs = [], [], []
            
            for lang in langs:
                if lang in lang_results:
                    fisher_ps.append(lang_results[lang]['fisher_p'])
                    wilcox_ps.append(lang_results[lang].get('wilcoxon_p', float('nan')))
                    valid_langs.append(lang)
            
            if len(fisher_ps) > 1:
                adj_fisher = bh_adjust(fisher_ps)
                adj_wilcox = bh_adjust(wilcox_ps)
                for i, lang in enumerate(valid_langs):
                    lang_results[lang]['fisher_p_adj'] = adj_fisher[i]
                    lang_results[lang]['wilcoxon_p_adj'] = adj_wilcox[i]
    
    return pvalue_data
```

调用位置（`build_index.py` 生成 `pvalue_json` 之前）：

```python
pvalue_data = apply_fdr_correction(pvalue_data)
pvalue_json = json.dumps(pvalue_data, ensure_ascii=False)
```

---

## 脚注建议

若在前端展示，建议在方法论说明中加入：

> **多重比较控制**：每个分词器在同一组内同时进行 3 次单边检验。本研究采用 Benjamini-Hochberg 方法控制假发现率（FDR）。理由：(1) 本研究为探索性语料库分析，假阳性代价低；(2) $n=5$ 时 Holm 校正将彻底消除所有检出功效；(3) 计算语言学领域惯例报告 FDR 校正后的 q 值。鼠标悬停表格可查看原始 p 值。
