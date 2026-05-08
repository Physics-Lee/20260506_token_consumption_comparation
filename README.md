# 用文言，可省词元乎？

A multilingual parallel corpus for comparing token consumption across languages and tokenizer models.

## 语料库概况

- **12 篇文章** × **4 种语言** = 48 个文本
- 四种语言：文言、现代汉语、English、Español
- 每篇文章均含 1 个原文 + 3 个译文
- 导航栏与页面主标题统一使用**文言标题**

## 目录结构

```
.
├── code/                          # 构建脚本（纯 Python）
│   ├── extract_originals.py       # 从 JSON 提取原文到 resource/
│   ├── json2html.py               # 从 JSON 生成主题化 HTML
│   └── md2json.py                 # 将 Markdown 原文转为 JSON 骨架
├── corpus_reader.html             # 主阅读器（自动生成）
├── data/                          # 规范语料数据（JSON）
│   ├── allende.json               # 阿连德最后的演讲
│   ├── assassination_qin.json     # 荆轲刺秦王
│   ├── bird_migration.json        # 夜间鸟类迁徙监测网络
│   ├── dark_matter_galaxies.json  # 暗物质缺失星系
│   ├── duke_huan_qi.json          # 齐桓公葵丘会盟
│   ├── duke_xi_28th_year.json     # 春秋·僖公二十八年
│   ├── exile_of_duke_wen_of_jin.json  # 左传·晋文公流亡
│   ├── ju_lu_battle.json          # 钜鹿之战
│   ├── paulgraham.json            # 会写的人与不会写的人
│   ├── science_revolution_dl.json # 深度学习与科学革命
│   ├── yangzhenning.json          # 谏罢建造超大对撞机疏
│   └── yau_collider_opinions.json # 丘成桐议中国建高能对撞机
├── note/                          # 文档
│   ├── how-to-change-card-order.md      # 如何更改卡片顺序
│   ├── how-character-counting-works.md  # 字符统计机制
│   └── theme-system-preference.md       # 三态主题切换原理
└── resource/                      # 原文 Markdown
    ├── Last_Speech_of_Salvador_Allende.md
    ├── The_Assassination_Attempt_on_the_King_of_Qin.md
    ├── Bird_Migration.md
    ├── Dark_Matter_Deficient_Galaxies.md
    ├── Duke_Huan_of_Qi_Accepts_the_Sacrificial_Meat_at_Kuiqiu_Without_Breaching_Ritual_Propriety.md
    ├── Ju_Lu_Battle.md
    ├── Science_Revolution_by_DL.md
    ├── Several_Opinions_on_Chinas_Construction_of_a_High_Energy_Collider_and_Responses_to_Media_Questions.md
    ├── The_Exile_of_Duke_Wen_of_Jin.md
    ├── The_Twenty_Eighth_Year_of_Duke_Xi_of_Lu_in_the_Spring_and_Autumn_Annals.md
    ├── Why_China_Should_Not_Build_a_Super_Collider_Today.md
    └── Writes_and_Write_Nots.md
```

## 快速开始

```bash
# 生成阅读器
python code/json2html.py

# 在浏览器中打开
corpus_reader.html
```

## 如何添加新文章

### 方式一：使用 md2json.py 生成骨架

```bash
# 将 Markdown 原文放入 resource/
python code/md2json.py resource/My_Article.md --lang modern_chinese
```

这会生成 `data/my_article.json`，其中包含待填写的 metadata 和 3 个占位译文。

### 方式二：手动创建 JSON

```json
{
  "id": "unique_id",
  "metadata": {
    "title_zh": "中文标题",
    "title_en": "English Title",
    "title_es": "Título en Español",
    "author": "作者名",
    "source": "出处",
    "period": "时代",
    "genre": "体裁",
    "original_language": "modern_chinese"
  },
  "texts": [
    {
      "language": "classical_chinese",
      "role": "translation",
      "title": "文言标题",
      "content": "全文..."
    },
    {
      "language": "modern_chinese",
      "role": "original",
      "title": "现代汉语标题",
      "content": "全文..."
    },
    {
      "language": "english",
      "role": "translation",
      "title": "English Title",
      "content": "Full text..."
    },
    {
      "language": "spanish",
      "role": "translation",
      "title": "Título en Español",
      "content": "Texto completo..."
    }
  ]
}
```

**重要**：请使用 Python `json.dump()` 生成 JSON，不要手动拼接字符串，否则引号不会自动转义。

### 最后一步

```bash
python code/json2html.py
```

## 阅读器特性

- **三态主题**：浅色 / 深色 / 跟随系统（默认）
- **固定卡片顺序**：文言 → 现代汉语 → English → Español
- **文言标题**：导航栏与页面主标题统一使用文言标题
- **Unicode 字符数统计**：每篇文章附字符对比表
- **Sticky 导航**：顶部导航栏始终可见
- **响应式布局**：窄屏自动折叠为单列

## 技术细节

### 字符统计

采用 Python `len(str)`，统计 Unicode code points：
- 每个汉字 = 1 字符
- 每个英文字母 = 1 字符
- 换行符、空格均计入

### 语言标识

| 标识 | 语言 | CSS 类 |
|---|---|---|
| `classical_chinese` | 文言 | `lang-classical` |
| `modern_chinese` | 现代汉语 | `lang-modern` |
| `english` | English | `lang-english` |
| `spanish` | Español | `lang-spanish` |

## 文档

- [`note/theme-system-preference.md`](note/theme-system-preference.md) — 三态主题切换实现
- [`note/how-to-change-card-order.md`](note/how-to-change-card-order.md) — 如何修改卡片显示顺序
- [`note/how-character-counting-works.md`](note/how-character-counting-works.md) — 字符统计机制

## Token 分析管线（计划中）

- OpenAI `tiktoken` for GPT token counts
- DeepSeek / HuggingFace tokenizers for comparison
- Statistical summary tables

## License

Created for token consumption research. Texts are translations of public-domain or widely published works.
