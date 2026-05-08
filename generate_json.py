import json
import re
from pathlib import Path

def extract_sections(filepath):
    """Extract sections from a translation file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by section markers like 【原文·文言】, 【现代汉语】, etc.
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('【') and line.endswith('】'):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            # Start new section
            current_section = line.strip('【】')
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def clean_text(text):
    """Clean text by removing extra whitespace."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

# Process each file
files_data = []

# Row 1: Classical Chinese (左传)
sections = extract_sections('row_1_classical_chinese_translations.txt')
files_data.append({
    "id": "zuozhuan",
    "title": {
        "zh": "左传·晋文公流亡",
        "en": "Zuo Zhuan: The Exile of Duke Wen of Jin",
        "es": "Zuo Zhuan: El Exilio del Duque Wen de Jin"
    },
    "original_language": "classical_chinese",
    "author": "左丘明",
    "source": "《左传·僖公二十三年、二十四年》",
    "period": "春秋时期 (公元前7世纪)",
    "genre": "历史叙事",
    "texts": {
        "classical_chinese": {
            "role": "original",
            "content": clean_text(sections.get('原文·文言', '')),
            "title": "左传·晋文公流亡"
        },
        "modern_chinese": {
            "role": "translation",
            "content": clean_text(sections.get('现代汉语', '')),
            "title": "晋文公流亡记（白话译文）",
            "translator": "现代汉语翻译"
        },
        "english": {
            "role": "translation", 
            "content": clean_text(sections.get('English', '')),
            "title": "The Exile of Duke Wen of Jin",
            "translator": "English Translation"
        },
        "spanish": {
            "role": "translation",
            "content": clean_text(sections.get('Español', '')),
            "title": "El Exilio del Duque Wen de Jin",
            "translator": "Traducción al Español"
        }
    }
})

# Row 2: English (Paul Graham)
sections = extract_sections('row_2_english_translations.txt')
files_data.append({
    "id": "paulgraham",
    "title": {
        "zh": "会写的人与不会写的人",
        "en": "Writes and Write-Nots",
        "es": "Los que escriben y los que no"
    },
    "original_language": "english",
    "author": "Paul Graham",
    "source": "paulgraham.com, October 2024",
    "period": "当代 (2024年)",
    "genre": "科技评论/散文",
    "texts": {
        "classical_chinese": {
            "role": "translation",
            "content": clean_text(sections.get('文言', '')),
            "title": "能书者与不能书者",
            "translator": "文言翻译"
        },
        "modern_chinese": {
            "role": "translation",
            "content": clean_text(sections.get('现代汉语', '')),
            "title": "会写的人与不会写的人",
            "translator": "现代汉语翻译"
        },
        "english": {
            "role": "original",
            "content": clean_text(sections.get('原文·English', '')),
            "title": "Writes and Write-Nots"
        },
        "spanish": {
            "role": "translation",
            "content": clean_text(sections.get('Español', '')),
            "title": "Los que escriben y los que no",
            "translator": "Traducción al Español"
        }
    }
})

# Row 3: Spanish (Allende)
sections = extract_sections('row_3_spanish_translations.txt')
files_data.append({
    "id": "allende",
    "title": {
        "zh": "阿连德最后的演讲",
        "en": "Last Speech of Salvador Allende",
        "es": "Último discurso de Salvador Allende"
    },
    "original_language": "spanish",
    "author": "Salvador Allende Gossens",
    "source": "Radio Magallanes, 11 de septiembre de 1973",
    "period": "当代 (1973年)",
    "genre": "政治演讲/绝命书",
    "texts": {
        "classical_chinese": {
            "role": "translation",
            "content": clean_text(sections.get('文言', '')),
            "title": "阿连德绝命书",
            "translator": "文言翻译"
        },
        "modern_chinese": {
            "role": "translation",
            "content": clean_text(sections.get('现代汉语', '')),
            "title": "萨尔瓦多·阿连德的最后一次演讲",
            "translator": "现代汉语翻译"
        },
        "english": {
            "role": "translation",
            "content": clean_text(sections.get('English', '')),
            "title": "Last Speech of Salvador Allende",
            "translator": "English Translation"
        },
        "spanish": {
            "role": "original",
            "content": clean_text(sections.get('原文·Español', '')),
            "title": "Último discurso de Salvador Allende"
        }
    }
})

# Row 4: Modern Chinese (杨振宁)
sections = extract_sections('row_4_modern_chinese_translations.txt')
files_data.append({
    "id": "yangzhenning",
    "title": {
        "zh": "中国今天不宜建造超大对撞机",
        "en": "Why China Should Not Build a Super Collider Today",
        "es": "Por qué China no debería construir un supercolisionador hoy"
    },
    "original_language": "modern_chinese",
    "author": "杨振宁 (Chen-Ning Yang)",
    "source": "《知识分子》微信公众号, 2016年9月4日",
    "period": "当代 (2016年)",
    "genre": "科学评论/议论文",
    "texts": {
        "classical_chinese": {
            "role": "translation",
            "content": clean_text(sections.get('文言', '')),
            "title": "谏罢建造超大对撞机疏",
            "translator": "文言翻译"
        },
        "modern_chinese": {
            "role": "original",
            "content": clean_text(sections.get('原文·现代汉语', '')),
            "title": "中国今天不宜建造超大对撞机"
        },
        "english": {
            "role": "translation",
            "content": clean_text(sections.get('English', '')),
            "title": "Why China Should Not Build a Super Collider Today",
            "translator": "English Translation"
        },
        "spanish": {
            "role": "translation",
            "content": clean_text(sections.get('Español', '')),
            "title": "Por qué China no debería construir un supercolisionador hoy",
            "translator": "Traducción al Español"
        }
    }
})

# Generate individual JSON files
for data in files_data:
    filename = f"{data['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Created: {filename}")
    
    # Calculate character counts
    print(f"  Title: {data['title']['en']}")
    for lang, text_data in data['texts'].items():
        char_count = len(text_data['content'])
        role = text_data['role']
        print(f"    {lang:20s}: {char_count:5d} chars ({role})")
    print()

# Also create a combined manifest
manifest = {
    "project": "Token Consumption Comparison Corpus",
    "description": "4×4 multilingual parallel corpus for tokenizer efficiency analysis",
    "created": "2026-05-06",
    "languages": ["classical_chinese", "modern_chinese", "english", "spanish"],
    "articles": [
        {
            "id": d["id"],
            "title": d["title"],
            "original_language": d["original_language"],
            "author": d["author"],
            "genre": d["genre"],
            "period": d["period"]
        }
        for d in files_data
    ]
}

with open('manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("Created: manifest.json")

print("\nDone! All JSON files generated successfully.")
