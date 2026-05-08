# 4×4 Multilingual Corpus for Token Consumption Analysis

A parallel corpus of 4 articles translated into 4 languages (Classical Chinese, Modern Chinese, English, Spanish) for comparing token consumption across languages and tokenizer models.

## Directory Structure

```
.
├── code/                          # Build scripts (Python)
│   ├── extract_originals.py       # Extract original texts from JSON to resource/
│   └── json2html.py               # Generate themed HTML from JSON
├── corpus_reader.html             # Main interactive reader (generated)
├── data/                          # Canonical corpus data (JSON)
│   ├── allende.json               # Salvador Allende's last speech
│   ├── paulgraham.json            # Paul Graham: Writes and Write-Nots
│   ├── yangzhenning.json          # Yang Zhenning on super colliders
│   └── zuozhuan.json              # Zuo Zhuan: Exile of Duke Wen of Jin
├── note/                          # Documentation
│   └── theme-system-preference.md # How the 3-state theme toggle works
└── resource/                      # Source texts in Markdown
    ├── Last_Speech_of_Salvador_Allende.md
    ├── The_Exile_of_Duke_Wen_of_Jin.md
    ├── Why_China_Should_Not_Build_a_Super_Collider_Today.md
    └── Writes_and_Write_Nots.md
```

## How to Add a New Article

1. **Write translations**: Create the article in all 4 languages. Identify which is the original.

2. **Create a JSON file** in `data/` following this schema:

```json
{
  "id": "unique_id",
  "metadata": {
    "title_zh": "中文标题",
    "title_en": "English Title",
    "title_es": "Título en Español",
    "author": "Author Name",
    "source": "Publication Source",
    "period": "Historical Period",
    "genre": "Genre/Type",
    "original_language": "english"
  },
  "texts": [
    {
      "language": "classical_chinese",
      "role": "translation",
      "title": "文言标题",
      "content": "Full text..."
    },
    {
      "language": "modern_chinese",
      "role": "translation",
      "title": "现代汉语标题",
      "content": "Full text..."
    },
    {
      "language": "english",
      "role": "original",
      "title": "English Title",
      "content": "Full text..."
    },
    {
      "language": "spanish",
      "role": "translation",
      "title": "Título en Español",
      "content": "Full text..."
    }
  ]
}
```

3. **Add the original source** to `resource/` as a Markdown file with an English filename:
   ```bash
   # Example
   resource/My_New_Article.md
   ```

4. **Regenerate the HTML**:
   ```bash
   python code/json2html.py
   ```

5. Open `corpus_reader.html` in a browser.

## Theme System

The reader supports three display modes:
- ☀️ **Light** — Fixed light theme
- 🌙 **Dark** — Fixed dark theme  
- 💻 **Follow System** — Automatically matches OS preference (default)

Click the theme button in the top-right corner to cycle through modes.

## Features

- **Sticky navigation** — Switch between articles without scrolling
- **Metadata panel** — Author, source, period, genre for each article
- **Comparison table** — Character counts per language/translation
- **2×2 parallel grid** — Side-by-side reading of all 4 versions
- **Language highlighting** — Color-coded borders for each language
- **Responsive design** — Collapses to single column on narrow screens

## Token Analysis Pipeline (Planned)

Future scripts may integrate:
- OpenAI `tiktoken` for GPT token counts
- DeepSeek/HuggingFace tokenizers for comparison
- Statistical summary tables

## License

Created for token consumption research. Texts are translations of public-domain or widely published works.
