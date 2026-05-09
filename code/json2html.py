import json
from pathlib import Path

def json_to_html():
    """Convert all JSON corpus files to a single themed HTML reader."""
    
    json_files = sorted(Path('./data').glob('*.json'))
    articles = []
    
    for filepath in json_files:
        if filepath.name == 'token_counts.json':
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            articles.append(json.load(f))
    
    if not articles:
        print("No JSON files found in ../data/!")
        return
    
    # Load precomputed token counts (if available) for embedding as JS variable
    token_counts_json = "{}"
    try:
        with open('./data/token_counts.json', 'r', encoding='utf-8') as f:
            token_counts_json = json.dumps(json.load(f), ensure_ascii=False)
        print("Loaded precomputed token counts from token_counts.json")
    except FileNotFoundError:
        print("No token_counts.json found — open-source tokenizers will show placeholder")
    
    # Language configuration
    LANG_CONFIG = {
        'classical_chinese': {'label': '文言', 'css': 'lang-classical', 'dot': '#ffd700', 'dot_light': '#b8860b'},
        'modern_chinese': {'label': '现代汉语', 'css': 'lang-modern', 'dot': '#4ecdc4', 'dot_light': '#2a9d8f'},
        'english': {'label': 'English', 'css': 'lang-english', 'dot': '#a5d6ff', 'dot_light': '#3b82f6'},
        'spanish': {'label': 'Español', 'css': 'lang-spanish', 'dot': '#ff7b72', 'dot_light': '#dc2626'},
    }
    
    # Build navigation - use classical Chinese title for nav buttons
    nav_items = []
    for i, article in enumerate(articles):
        active = 'active' if i == 0 else ''
        classical_title = next((t['title'] for t in article['texts'] if t['language'] == 'classical_chinese'), article['metadata']['title_zh'])
        nav_items.append(f'<button class="nav-btn {active}" data-id="{article["id"]}">{classical_title}</button>')
    
    # Build article sections
    sections = []
    for i, article in enumerate(articles):
        active = 'active' if i == 0 else ''
        meta = article['metadata']
        texts = article['texts']
        
        # Use classical Chinese title as the main page title
        classical_title = next((t['title'] for t in texts if t['language'] == 'classical_chinese'), meta['title_zh'])
        
        # Sort by fixed language order: 文言, 现代汉语, English, Español
        lang_order = {'classical_chinese': 0, 'modern_chinese': 1, 'english': 2, 'spanish': 3}
        texts_sorted = sorted(texts, key=lambda x: lang_order.get(x['language'], 99))
        
        # Build text cards
        cards = []
        for text in texts_sorted:
            cfg = LANG_CONFIG.get(text['language'], {'label': text['language'], 'css': '', 'dot': '#fff'})
            role_text = '原文' if text['role'] == 'original' else '译文'
            char_count = len(text['content'])
            
            # Fix: some JSON files contain literal \n sequences instead of actual newlines
            content_fixed = text['content'].replace('\\n', '\n')
            
            cards.append(f'''
                <div class="text-card {cfg['css']}">
                    <div class="card-header"><span class="lang-name">{cfg['label']}</span><span class="role-badge {'original' if text['role'] == 'original' else 'translation'}">{role_text}</span></div>
                    <div class="card-body">
                        <button class="copy-btn" data-content="{content_fixed.replace(chr(34), '&quot;').replace(chr(39), '&#39;')}" title="复制全文">📋</button>
                        <h4>{text['title']}</h4><pre>{content_fixed}</pre>
                    </div>
                    <div class="card-footer">{char_count:,} 字符</div>
                </div>
            ''')
        
        # Build comparison table rows
        rows = []
        for text in texts_sorted:
            cfg = LANG_CONFIG.get(text['language'], {'label': text['language'], 'dot': '#fff'})
            role_text = '原文' if text['role'] == 'original' else '译文'
            rows.append(f'''
                <tr><td><span class="dot" style="background:{cfg['dot']}"></span>{cfg['label']}</td><td>{role_text}</td><td>{text['title']}</td><td>{len(text['content']):,}</td><td class="token-count" data-article="{article['id']}" data-lang="{text['language']}">—</td></tr>
            ''')
        
        sections.append(f'''
        <section id="{article['id']}" class="article-section {active}">
            <div class="metadata">
                <h2>{classical_title}</h2>
                <div class="meta-grid">
                    <div><span class="meta-label">English Title</span><span class="meta-value">{meta.get('title_en', '')}</span></div>
                    <div><span class="meta-label">Título en Español</span><span class="meta-value">{meta.get('title_es', '')}</span></div>
                    <div><span class="meta-label">作者 / Author</span><span class="meta-value">{meta.get('author', '')}</span></div>
                    <div><span class="meta-label">来源 / Source</span><span class="meta-value">{meta.get('source', '')}</span></div>
                    <div><span class="meta-label">时代 / Period</span><span class="meta-value">{meta.get('period', '')}</span></div>
                    <div><span class="meta-label">体裁 / Genre</span><span class="meta-value">{meta.get('genre', '')}</span></div>
                     <div><span class="meta-label">原文语言 / ORIGINAL LANGUAGE</span><span class="meta-value">{meta.get('original_language', '')}</span></div>
                </div>
            </div>
            
            <div class="comparison">
                <table>
                    <thead><tr><th>语言</th><th>角色</th><th>标题</th><th>Unicode 字符数</th><th class="token-col-header">词元数 <span class="tokenizer-name"></span></th></tr></thead>
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
    <title>用文言，可省词元乎？</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
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
        .copy-btn {{
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            width: 2rem;
            height: 2rem;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--bg-card-inner);
            color: var(--text-secondary);
            font-size: 0.9rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0.5;
            transition: opacity 0.2s, background 0.2s, border-color 0.2s;
            z-index: 2;
        }}
        .text-card:hover .copy-btn {{
            opacity: 1;
        }}
        .copy-btn:hover {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--bg-body);
        }}
        .copy-btn.copied {{
            background: #2ecc71;
            border-color: #2ecc71;
            color: white;
        }}
        .card-body {{
            position: relative;
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
        .footer-links {{
            margin-top: 1rem;
            font-size: 0.85rem;
        }}
        .footer-links a {{
            color: var(--accent);
            text-decoration: none;
            margin: 0 0.6rem;
            transition: opacity 0.2s;
        }}
        .footer-links a:hover {{
            text-decoration: underline;
            opacity: 0.8;
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
        
        /* Tokenizer selector */
        .tokenizer-bar {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-left: auto;
            padding-left: 1.5rem;
            border-left: 1px solid var(--border);
        }}
        .tokenizer-bar label {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            white-space: nowrap;
        }}
        .tokenizer-select {{
            padding: 0.5rem 1rem;
            border: 2px solid var(--border);
            background: var(--bg-card);
            color: var(--text-primary);
            border-radius: 8px;
            font-size: 0.9rem;
            cursor: pointer;
            outline: none;
            transition: border-color 0.3s;
        }}
        .tokenizer-select:hover, .tokenizer-select:focus {{
            border-color: var(--accent);
        }}
        .token-col-header .tokenizer-name {{
            font-weight: 400;
            color: var(--text-secondary);
            font-size: 0.8rem;
        }}
        .token-count {{
            font-variant-numeric: tabular-nums;
            transition: color 0.2s;
        }}
        .token-count.loading {{
            color: var(--text-secondary);
            font-style: italic;
        }}
    </style>
</head>
<body>
    <header>
        <button class="theme-toggle" onclick="toggleTheme()" title="切换主题"></button>
        <h1>用文言，可省词元乎？</h1>
        <p>Token Consumption Analysis Corpus | 四种语言 · {len(articles)}篇文章</p>
    </header>
    
    <nav>
        {' '.join(nav_items)}
        <div class="tokenizer-bar">
            <label for="tokenizer-select">分词器：</label>
            <select id="tokenizer-select" class="tokenizer-select">
                <optgroup label="OpenAI（实时）">
                    <option value="gpt-4o" selected>gpt-4o (o200k_base)</option>
                    <option value="gpt-4.1">gpt-4.1</option>
                    <option value="gpt-4">gpt-4 / gpt-3.5-turbo (cl100k_base)</option>
                    <option value="text-davinci-003">text-davinci-003 (p50k_base)</option>
                    <option value="davinci">davinci (r50k_base)</option>
                    <option value="o200k_base">o200k_base (编码)</option>
                    <option value="cl100k_base">cl100k_base (编码)</option>
                    <option value="p50k_base">p50k_base (编码)</option>
                    <option value="r50k_base">r50k_base (编码)</option>
                </optgroup>
                <optgroup label="开源模型（预计算）">
                    <option value="Qwen2.5-72B">Qwen2.5-72B</option>
                    <option value="Phi-2">Phi-2</option>
                    <option value="Gemma-7B">Gemma-7B</option>
                    <option value="DeepSeek-R1">DeepSeek-R1</option>
                    <option value="Llama-3-8B">Llama-3-8B</option>
                    <option value="Llama-3-70B">Llama-3-70B</option>
                </optgroup>
            </select>
        </div>
    </nav>
    
    <main>
        {' '.join(sections)}
    </main>
    
    <footer>
        <p>{len(articles)}×4 Multilingual Corpus | Generated for Token Consumption Analysis</p>
        <div class="footer-links">
            <span>友情链接 / Friendly Links:</span>
            <a href="https://gpt-tokenizer.dev/" target="_blank" rel="noopener">GPT Tokenizer</a>
            <a href="https://www.danieldemmel.me/tokenizer" target="_blank" rel="noopener">LLM Tokenizer</a>
            <a href="https://tiktokenizer.vercel.app/" target="_blank" rel="noopener">tiktokenizer</a>
            <a href="https://platform.openai.com/tokenizer" target="_blank" rel="noopener">OpenAI Tokenizer</a>
        </div>
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

        // Copy button logic
        document.querySelectorAll('.copy-btn').forEach(btn => {{
            btn.addEventListener('click', async function(e) {{
                e.stopPropagation();
                const content = this.getAttribute('data-content');
                try {{
                    await navigator.clipboard.writeText(content);
                    this.textContent = '✓';
                    this.classList.add('copied');
                    this.title = '已复制';
                    setTimeout(() => {{
                        this.textContent = '📋';
                        this.classList.remove('copied');
                        this.title = '复制全文';
                    }}, 1500);
                }} catch (err) {{
                    console.error('Copy failed:', err);
                    this.title = '复制失败';
                }}
            }});
        }});
    </script>
    <script>
        // Precomputed token counts for open-source models (generated at build time)
        window.PRECOMPUTED_TOKENS = {token_counts_json};
    </script>
    
    <!-- gpt-tokenizer encoding-specific UMD bundles -->
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/o200k_base.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/cl100k_base.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/p50k_base.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/r50k_base.js"></script>
    
    <script>
        // ── Encoder map: tokenizer name → UMD global ──
        const ENCODERS = {{
            'gpt-4o':             GPTTokenizer_o200k_base,
            'gpt-4.1':            GPTTokenizer_o200k_base,
            'gpt-4':              GPTTokenizer_cl100k_base,
            'gpt-3.5-turbo':      GPTTokenizer_cl100k_base,
            'text-davinci-003':   GPTTokenizer_p50k_base,
            'davinci':            GPTTokenizer_r50k_base,
            'o200k_base':         GPTTokenizer_o200k_base,
            'cl100k_base':        GPTTokenizer_cl100k_base,
            'p50k_base':          GPTTokenizer_p50k_base,
            'r50k_base':          GPTTokenizer_r50k_base,
        }};

        const OPEN_SOURCE_MODELS = [
            'Qwen2.5-72B', 'Phi-2', 'Gemma-7B',
            'DeepSeek-R1', 'Llama-3-8B', 'Llama-3-70B'
        ];

        function isOpenSource(name) {{
            return OPEN_SOURCE_MODELS.includes(name);
        }}

        // ── Text cache: extract all <pre> texts once ──
        const textCache = new Map();
        function getTextKey(articleId, lang) {{
            return `${{articleId}}::${{lang}}`;
        }}
        function getText(articleId, lang) {{
            const key = getTextKey(articleId, lang);
            if (textCache.has(key)) return textCache.get(key);
            const section = document.getElementById(articleId);
            if (!section) return '';
            const cards = section.querySelectorAll('.text-card');
            for (const card of cards) {{
                const langClass = Array.from(card.classList).find(c =>
                    c.startsWith('lang-') && !c.endsWith('-name'));
                if (!langClass) continue;
                const pre = card.querySelector('pre');
                if (!pre) continue;
                let cardLang = null;
                if (langClass === 'lang-classical') cardLang = 'classical_chinese';
                else if (langClass === 'lang-modern') cardLang = 'modern_chinese';
                else if (langClass === 'lang-english') cardLang = 'english';
                else if (langClass === 'lang-spanish') cardLang = 'spanish';
                if (cardLang && cardLang === lang) {{
                    textCache.set(key, pre.textContent);
                    return pre.textContent;
                }}
            }}
            return '';
        }}

        // ── Count tokens ──
        function countTokens(text, tokenizerName) {{
            const encoder = ENCODERS[tokenizerName];
            if (!encoder || typeof encoder.encode !== 'function') return -1;
            try {{
                return encoder.encode(text).length;
            }} catch(e) {{
                return -1;
            }}
        }}

        // ── Update all token cells ──
        let currentTokenizer = 'gpt-4o';

        function updateAllTokenCounts() {{
            const name = currentTokenizer;
            document.querySelectorAll('.tokenizer-name').forEach(el => {{
                el.textContent = `(${{name}})`;
            }});

            const cells = document.querySelectorAll('.token-count');
            cells.forEach(cell => {{ cell.classList.add('loading'); cell.textContent = '...'; }});

            setTimeout(() => {{
                cells.forEach(cell => {{
                    const articleId = cell.dataset.article;
                    const lang = cell.dataset.lang;
                    cell.classList.remove('loading');

                    if (isOpenSource(name)) {{
                        const pre = window.PRECOMPUTED_TOKENS;
                        if (pre && pre.open_source && pre.open_source[name] &&
                            pre.open_source[name][articleId] &&
                            pre.open_source[name][articleId][lang] !== undefined) {{
                            cell.textContent = pre.open_source[name][articleId][lang].toLocaleString();
                        }} else {{
                            cell.textContent = '需预计算';
                            cell.title = '运行 code/precompute_tokens.js 生成数据';
                        }}
                        return;
                    }}

                    const text = getText(articleId, lang);
                    if (!text) {{ cell.textContent = '—'; return; }}

                    const count = countTokens(text, name);
                    cell.textContent = count > 0 ? count.toLocaleString() : '—';
                }});
            }}, 10);
        }}

        // ── Init ──
        document.getElementById('tokenizer-select').addEventListener('change', function() {{
            currentTokenizer = this.value;
            updateAllTokenCounts();
        }});

        document.addEventListener('DOMContentLoaded', updateAllTokenCounts);
        if (document.readyState !== 'loading') updateAllTokenCounts();
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
