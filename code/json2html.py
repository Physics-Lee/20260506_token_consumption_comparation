import json
from pathlib import Path

def json_to_html():
    """Convert all JSON corpus files to a single themed HTML reader."""
    
    json_files = sorted(Path('./data').glob('*.json'))
    articles = []
    
    for filepath in json_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            articles.append(json.load(f))
    
    if not articles:
        print("No JSON files found in ../data/!")
        return
    
    # Language configuration
    LANG_CONFIG = {
        'classical_chinese': {'label': '文言', 'css': 'lang-classical', 'dot': '#ffd700', 'dot_light': '#b8860b'},
        'modern_chinese': {'label': '现代汉语', 'css': 'lang-modern', 'dot': '#4ecdc4', 'dot_light': '#2a9d8f'},
        'english': {'label': 'English', 'css': 'lang-english', 'dot': '#a5d6ff', 'dot_light': '#3b82f6'},
        'spanish': {'label': 'Español', 'css': 'lang-spanish', 'dot': '#ff7b72', 'dot_light': '#dc2626'},
    }
    
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
        
        # Sort: original first, then by language order
        lang_order = {'classical_chinese': 0, 'modern_chinese': 1, 'english': 2, 'spanish': 3}
        texts_sorted = sorted(texts, key=lambda x: (0 if x['role'] == 'original' else 1, lang_order.get(x['language'], 99)))
        
        # Build text cards
        cards = []
        for text in texts_sorted:
            cfg = LANG_CONFIG.get(text['language'], {'label': text['language'], 'css': '', 'dot': '#fff'})
            role_text = '原文' if text['role'] == 'original' else '译文'
            char_count = len(text['content'])
            
            cards.append(f'''
                <div class="text-card {cfg['css']}">
                    <div class="card-header"><span class="lang-name">{cfg['label']}</span><span class="role-badge {'original' if text['role'] == 'original' else 'translation'}">{role_text}</span></div>
                    <div class="card-body"><h4>{text['title']}</h4><pre>{text['content']}</pre></div>
                    <div class="card-footer">{char_count:,} 字符</div>
                </div>
            ''')
        
        # Build comparison table rows
        rows = []
        for text in texts_sorted:
            cfg = LANG_CONFIG.get(text['language'], {'label': text['language'], 'dot': '#fff'})
            role_text = '原文' if text['role'] == 'original' else '译文'
            rows.append(f'''
                <tr><td><span class="dot" style="background:{cfg['dot']}"></span>{cfg['label']}</td><td>{role_text}</td><td>{text['title']}</td><td>{len(text['content']):,}</td></tr>
            ''')
        
        sections.append(f'''
        <section id="{article['id']}" class="article-section {active}">
            <div class="metadata">
                <h2>{meta['title_zh']}</h2>
                <div class="meta-grid">
                    <div><span class="meta-label">English Title</span><span class="meta-value">{meta.get('title_en', '')}</span></div>
                    <div><span class="meta-label">Título en Español</span><span class="meta-value">{meta.get('title_es', '')}</span></div>
                    <div><span class="meta-label">作者 / Author</span><span class="meta-value">{meta.get('author', '')}</span></div>
                    <div><span class="meta-label">来源 / Source</span><span class="meta-value">{meta.get('source', '')}</span></div>
                    <div><span class="meta-label">时代 / Period</span><span class="meta-value">{meta.get('period', '')}</span></div>
                    <div><span class="meta-label">体裁 / Genre</span><span class="meta-value">{meta.get('genre', '')}</span></div>
                    <div><span class="meta-label">原文语言</span><span class="meta-value">{meta.get('original_language', '')}</span></div>
                </div>
            </div>
            
            <div class="comparison">
                <table>
                    <thead><tr><th>语言</th><th>角色</th><th>标题</th><th>字符数</th></tr></thead>
                    <tbody>{''.join(rows)}</tbody>
                </table>
            </div>
            
            <div class="text-grid">{''.join(cards)}</div>
        </section>
        ''')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{len(articles)}×4 多语言语料库阅读器</title>
    <style>
        :root {{
            --bg-body: #f8f9fa;
            --bg-card: #ffffff;
            --bg-card-inner: #f9fafb;
            --text-primary: #374151;
            --text-secondary: #6b7280;
            --text-heading: #111827;
            --accent: #2563eb;
            --border: #e5e7eb;
            --shadow: rgba(0,0,0,0.08);
            --hover-bg: rgba(37, 99, 235, 0.04);
            --btn-active-text: #fff;
        }}
        [data-theme="dark"] {{
            --bg-body: #0d1117;
            --bg-card: #161b22;
            --bg-card-inner: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --text-heading: #f0f6fc;
            --accent: #58a6ff;
            --border: #30363d;
            --shadow: rgba(0,0,0,0.3);
            --hover-bg: rgba(88, 166, 255, 0.05);
            --btn-active-text: #fff;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", "Noto Serif SC", serif;
            background: var(--bg-body);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background 0.3s, color 0.3s;
        }}
        header {{
            background: var(--bg-card);
            padding: 2rem;
            text-align: center;
            border-bottom: 3px solid var(--accent);
            position: relative;
            transition: background 0.3s;
        }}
        header h1 {{
            font-size: 2rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }}
        header p {{ color: var(--text-secondary); }}
        
        .theme-toggle {{
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            padding: 0.5rem 1rem;
            border: 2px solid var(--border);
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            border-radius: 8px;
            font-size: 0.9rem;
            transition: all 0.3s;
        }}
        .theme-toggle:hover {{ border-color: var(--accent); color: var(--accent); }}
        
        nav {{
            background: var(--bg-card);
            padding: 1rem;
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border);
            transition: background 0.3s;
        }}
        .nav-btn {{
            padding: 0.75rem 1.5rem;
            border: 2px solid var(--border);
            background: transparent;
            color: var(--text-secondary);
            cursor: pointer;
            border-radius: 8px;
            font-size: 0.95rem;
            transition: all 0.3s;
        }}
        .nav-btn:hover {{ border-color: var(--accent); color: var(--text-primary); }}
        .nav-btn.active {{ background: var(--accent); border-color: var(--accent); color: var(--btn-active-text); }}
        
        main {{ max-width: 1600px; margin: 0 auto; padding: 2rem; }}
        
        .article-section {{ display: none; }}
        .article-section.active {{ display: block; animation: fadeIn 0.5s; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        .metadata {{
            background: var(--bg-card);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
            transition: background 0.3s;
        }}
        .metadata h2 {{ color: var(--accent); margin-bottom: 1rem; }}
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }}
        .meta-label {{ display: block; color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; margin-bottom: 0.25rem; }}
        .meta-value {{ font-size: 1rem; font-weight: 500; color: var(--text-primary); }}
        
        .comparison {{
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
            transition: background 0.3s;
        }}
        .comparison table {{ width: 100%; border-collapse: collapse; }}
        .comparison th {{
            background: var(--bg-card-inner);
            padding: 1rem;
            text-align: left;
            color: var(--accent);
            font-weight: 600;
            border-bottom: 2px solid var(--border);
            transition: background 0.3s;
        }}
        .comparison td {{ padding: 1rem; border-bottom: 1px solid var(--border); }}
        .comparison tr:hover td {{ background: var(--hover-bg); }}
        .dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; }}
        
        .text-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }}
        @media (max-width: 1200px) {{ .text-grid {{ grid-template-columns: 1fr; }} }}
        
        .text-card {{
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
            transition: transform 0.3s, box-shadow 0.3s, background 0.3s;
        }}
        .text-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px var(--shadow);
        }}
        .card-header {{
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            border-top: 4px solid;
        }}
        .lang-name {{ font-weight: 700; font-size: 0.9rem; letter-spacing: 1px; }}
        .role-badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .role-badge.original {{ background: var(--accent); color: var(--bg-body); }}
        .role-badge.translation {{ background: var(--bg-card-inner); color: var(--text-secondary); border: 1px solid var(--border); }}
        
        .card-body {{
            padding: 1.5rem;
            max-height: 600px;
            overflow-y: auto;
        }}
        .card-body h4 {{ margin-bottom: 1rem; color: var(--text-heading); font-size: 1.1rem; }}
        .card-body pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: "Noto Sans SC", "Noto Serif SC", serif;
            line-height: 1.8;
            font-size: 0.95rem;
            color: var(--text-primary);
            background: transparent;
            border: none;
            padding: 0;
        }}
        
        .card-footer {{
            padding: 1rem 1.5rem;
            background: var(--bg-card-inner);
            border-top: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-align: right;
            transition: background 0.3s;
        }}
        
        footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
            margin-top: 3rem;
            background: var(--bg-card);
            transition: background 0.3s;
        }}
        
        /* Language colors */
        .lang-classical {{ border-top-color: #ffd700 !important; }}
        .lang-classical .lang-name {{ color: #ffd700; }}
        [data-theme="light"] .lang-classical .lang-name {{ color: #b8860b; }}
        .lang-modern {{ border-top-color: #4ecdc4 !important; }}
        .lang-modern .lang-name {{ color: #4ecdc4; }}
        [data-theme="light"] .lang-modern .lang-name {{ color: #2a9d8f; }}
        .lang-english {{ border-top-color: #a5d6ff !important; }}
        .lang-english .lang-name {{ color: #a5d6ff; }}
        [data-theme="light"] .lang-english .lang-name {{ color: #3b82f6; }}
        .lang-spanish {{ border-top-color: #ff7b72 !important; }}
        .lang-spanish .lang-name {{ color: #ff7b72; }}
        [data-theme="light"] .lang-spanish .lang-name {{ color: #dc2626; }}
    </style>
</head>
<body>
    <header>
        <button class="theme-toggle" onclick="toggleTheme()" title="切换主题"></button>
        <h1>{len(articles)}×4 多语言语料库阅读器</h1>
        <p>Token Consumption Analysis Corpus | 四种语言 · {len(articles)}篇文章 · 平行对照</p>
    </header>
    
    <nav>
        {' '.join(nav_items)}
    </nav>
    
    <main>
        {' '.join(sections)}
    </main>
    
    <footer>
        <p>{len(articles)}×4 Multilingual Corpus | Generated for Token Consumption Analysis</p>
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

        const themeBtn = document.querySelector('.theme-toggle');
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        function getEffectiveTheme() {{
            const attr = document.documentElement.getAttribute('data-theme');
            if (attr === 'light' || attr === 'dark') return attr;
            return mediaQuery.matches ? 'dark' : 'light';
        }}

        function applyTheme(mode) {{
            if (mode === 'system') {{
                document.documentElement.removeAttribute('data-theme');
            }} else {{
                document.documentElement.setAttribute('data-theme', mode);
            }}
            updateThemeBtn();
        }}

        function updateThemeBtn() {{
            const attr = document.documentElement.getAttribute('data-theme');
            let label, icon;
            if (attr === 'light') {{ icon = '☀️'; label = '浅色'; }}
            else if (attr === 'dark') {{ icon = '🌙'; label = '深色'; }}
            else {{ icon = '💻'; label = '跟随系统'; }}
            themeBtn.textContent = `${{icon}} ${{label}}`;
            const effective = getEffectiveTheme();
            themeBtn.title = `当前模式: ${{label}} (实际: ${{effective === 'dark' ? '深色' : '浅色'}}) — 点击切换`;
        }}

        function toggleTheme() {{
            const current = document.documentElement.getAttribute('data-theme');
            const modes = ['light', 'dark', 'system'];
            const idx = modes.indexOf(current || 'system');
            const next = modes[(idx + 1) % modes.length];
            applyTheme(next);
        }}

        mediaQuery.addEventListener('change', () => {{
            if (!document.documentElement.hasAttribute('data-theme')) {{
                updateThemeBtn();
            }}
        }});

        applyTheme('system');
    </script>
</body>
</html>'''
    
    output = './corpus_reader.html'
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated: {output}")
    print(f"Articles: {len(articles)}")
    print(f"Open in browser to read")
    return output

if __name__ == '__main__':
    json_to_html()
