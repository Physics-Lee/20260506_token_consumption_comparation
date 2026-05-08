import json
from pathlib import Path

def json_to_html():
    """Convert all JSON corpus files to a single HTML reader."""
    
    json_files = ['zuozhuan.json', 'paulgraham.json', 'allende.json', 'yangzhenning.json']
    articles = []
    
    for filename in json_files:
        if Path(filename).exists():
            with open(filename, 'r', encoding='utf-8') as f:
                articles.append(json.load(f))
    
    if not articles:
        print("No JSON files found!")
        return
    
    # Build navigation
    nav_items = []
    for i, article in enumerate(articles):
        active = 'active' if i == 0 else ''
        nav_items.append(f'<button class="nav-btn {active}" data-id="{article["id"]}">{article["metadata"]["title_zh"]}</button>')
    
    # Build article sections
    sections = []
    for i, article in enumerate(articles):
        active = 'active' if i == 0 else ''
        meta = article['metadata']
        texts = article['texts']
        
        # Sort: translations first, then by language order
        lang_order = {'classical_chinese': 0, 'modern_chinese': 1, 'english': 2, 'spanish': 3}
        texts.sort(key=lambda x: (0 if x['role'] == 'translation' else 1, lang_order.get(x['language'], 99)))
        
        # Build text cards
        cards = []
        for text in texts:
            lang_map = {
                'classical_chinese': ('文言', 'classical', '#ffd700'),
                'modern_chinese': ('现代汉语', 'modern', '#4ecdc4'),
                'english': ('English', 'english', '#95e1d3'),
                'spanish': ('Español', 'spanish', '#f38181')
            }
            label, css_class, color = lang_map.get(text['language'], (text['language'], text['language'], '#fff'))
            role_text = '原文' if text['role'] == 'original' else '译文'
            char_count = len(text['content'])
            
            cards.append(f'''
            <div class="text-card">
                <div class="card-header" style="border-top-color: {color}">
                    <span class="lang-name" style="color: {color}">{label}</span>
                    <span class="role-badge {'original' if text['role'] == 'original' else 'translation'}">{role_text}</span>
                </div>
                <div class="card-body">
                    <h4>{text['title']}</h4>
                    <pre>{text['content']}</pre>
                </div>
                <div class="card-footer">
                    <span>{char_count:,} 字符</span>
                </div>
            </div>
            ''')
        
        # Build comparison table
        rows = []
        for text in texts:
            label, _, color = lang_map.get(text['language'], (text['language'], '', '#fff'))
            role_text = '原文' if text['role'] == 'original' else '译文'
            rows.append(f'''
            <tr>
                <td><span class="dot" style="background: {color}"></span>{label}</td>
                <td>{role_text}</td>
                <td>{text['title']}</td>
                <td>{len(text['content']):,}</td>
            </tr>
            ''')
        
        sections.append(f'''
        <section id="{article['id']}" class="article-section {active}">
            <div class="metadata">
                <h2>{meta['title_zh']}</h2>
                <div class="meta-grid">
                    <div><span class="meta-label">英文标题</span><span class="meta-value">{meta['title_en']}</span></div>
                    <div><span class="meta-label">西班牙文标题</span><span class="meta-value">{meta['title_es']}</span></div>
                    <div><span class="meta-label">作者</span><span class="meta-value">{meta['author']}</span></div>
                    <div><span class="meta-label">来源</span><span class="meta-value">{meta['source']}</span></div>
                    <div><span class="meta-label">时代</span><span class="meta-value">{meta['period']}</span></div>
                    <div><span class="meta-label">体裁</span><span class="meta-value">{meta['genre']}</span></div>
                    <div><span class="meta-label">原文语言</span><span class="meta-value">{meta['original_language']}</span></div>
                </div>
            </div>
            
            <div class="comparison">
                <table>
                    <thead>
                        <tr><th>语言</th><th>角色</th><th>标题</th><th>字符数</th></tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
            
            <div class="text-grid">
                {''.join(cards)}
            </div>
        </section>
        ''')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4×4 多语言语料库阅读器</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", "Noto Serif SC", serif;
            background: #1a1a2e;
            color: #eaeaea;
            line-height: 1.6;
        }}
        header {{
            background: #16213e;
            padding: 2rem;
            text-align: center;
            border-bottom: 3px solid #e94560;
        }}
        header h1 {{
            font-size: 2rem;
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        header p {{ color: #a0a0a0; }}
        
        nav {{
            background: #16213e;
            padding: 1rem;
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid #2a2a4a;
        }}
        .nav-btn {{
            padding: 0.75rem 1.5rem;
            border: 2px solid #2a2a4a;
            background: transparent;
            color: #a0a0a0;
            cursor: pointer;
            border-radius: 8px;
            font-size: 0.95rem;
            transition: all 0.3s;
        }}
        .nav-btn:hover {{ border-color: #e94560; color: #fff; }}
        .nav-btn.active {{ background: #e94560; border-color: #e94560; color: #fff; }}
        
        main {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}
        
        .article-section {{ display: none; }}
        .article-section.active {{ display: block; animation: fadeIn 0.5s; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        .metadata {{
            background: #16213e;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid #2a2a4a;
        }}
        .metadata h2 {{ color: #e94560; margin-bottom: 1rem; }}
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }}
        .meta-label {{ display: block; color: #a0a0a0; font-size: 0.8rem; text-transform: uppercase; }}
        .meta-value {{ font-size: 1rem; font-weight: 500; }}
        
        .comparison {{
            background: #16213e;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 2rem;
            border: 1px solid #2a2a4a;
        }}
        .comparison table {{ width: 100%; border-collapse: collapse; }}
        .comparison th {{
            background: #0f3460;
            padding: 1rem;
            text-align: left;
            color: #e94560;
            font-weight: 600;
        }}
        .comparison td {{ padding: 1rem; border-bottom: 1px solid #2a2a4a; }}
        .comparison tr:hover td {{ background: rgba(233, 69, 96, 0.05); }}
        .dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; }}
        
        .text-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 2rem;
        }}
        @media (max-width: 1300px) {{ .text-grid {{ grid-template-columns: 1fr; }} }}
        
        .text-card {{
            background: #0f3460;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #2a2a4a;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .text-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }}
        .card-header {{
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #2a2a4a;
            border-top: 4px solid;
        }}
        .lang-name {{ font-weight: 700; font-size: 0.9rem; letter-spacing: 1px; }}
        .role-badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .role-badge.original {{ background: #e94560; color: white; }}
        .role-badge.translation {{ background: #16213e; color: #a0a0a0; border: 1px solid #2a2a4a; }}
        
        .card-body {{
            padding: 1.5rem;
            max-height: 500px;
            overflow-y: auto;
        }}
        .card-body h4 {{ margin-bottom: 1rem; color: #fff; font-size: 1.1rem; }}
        .card-body pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: inherit;
            line-height: 1.8;
            font-size: 0.95rem;
            color: #eaeaea;
            background: transparent;
            border: none;
            padding: 0;
        }}
        
        .card-footer {{
            padding: 1rem 1.5rem;
            background: #16213e;
            border-top: 1px solid #2a2a4a;
            color: #a0a0a0;
            font-size: 0.85rem;
            text-align: right;
        }}
        
        footer {{
            text-align: center;
            padding: 2rem;
            color: #a0a0a0;
            border-top: 1px solid #2a2a4a;
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1>4×4 多语言语料库</h1>
        <p>Token Consumption Analysis Corpus | 四种语言 · 四篇文章 · 平行对照</p>
    </header>
    
    <nav>
        {' '.join(nav_items)}
    </nav>
    
    <main>
        {' '.join(sections)}
    </main>
    
    <footer>
        <p>Generated for Token Consumption Comparison | 用于 Token 消耗比较实验</p>
    </footer>
    
    <script>
        document.querySelectorAll('.nav-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.article-section').forEach(s => s.classList.remove('active'));
                this.classList.add('active');
                document.getElementById(this.dataset.id).classList.add('active');
            }});
        }});
    </script>
</body>
</html>'''
    
    output = 'corpus_reader.html'
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {output}")
    print(f"  Articles: {len(articles)}")
    print(f"  Open in browser to read")
    return output

if __name__ == '__main__':
    json_to_html()
