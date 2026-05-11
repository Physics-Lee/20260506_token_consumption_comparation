import json
from pathlib import Path

def build_index():
    """Generate index.html with token consumption comparison across tokenizers."""
    
    json_files = list(Path('./data').glob('*.json'))
    articles = []
    
    for filepath in json_files:
        if 'token_counts' in filepath.name:
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            articles.append(json.load(f))
    
    # Sort articles by pinyin of classical Chinese title
    def get_pinyin_key(article):
        classical_title = next((t['title'] for t in article['texts'] if t['language'] == 'classical_chinese'), article['metadata']['title_zh'])
        first_char = classical_title[0]
        try:
            from pypinyin import pinyin, Style
            py = pinyin(first_char, style=Style.NORMAL)
            return py[0][0] if py else first_char
        except ImportError:
            # Fallback: hardcoded mapping for common characters
            pinyin_map = {
                '阿': 'a', '暗': 'an', '春': 'chun', '谏': 'jian',
                '能': 'neng', '丘': 'qiu', '深': 'shen', '史': 'shi',
                '夜': 'ye', '战': 'zhan', '左': 'zuo'
            }
            return pinyin_map.get(first_char, first_char)
    
    articles.sort(key=get_pinyin_key)
    
    if not articles:
        print("No JSON files found in ../data/!")
        return
    
    # Load precomputed token counts for open-source models
    token_counts_json = "{}"
    try:
        with open('./data/token_counts.json', 'r', encoding='utf-8') as f:
            tc_data = json.load(f)
            token_counts_json = json.dumps(tc_data, ensure_ascii=False)
        print("Loaded precomputed token counts")
    except FileNotFoundError:
        tc_data = {}
        print("No token_counts.json — open-source tokenizers will show placeholder")
    
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
        classical_title = next((t['title'] for t in article['texts'] if t['language'] == 'classical_chinese'), article['metadata']['title_zh'])
        nav_items.append(f'<button class="nav-btn" data-id="{article["id"]}">{classical_title}</button>')
    # Totals and summary buttons at end
    nav_items.append(f'<button class="nav-btn" data-id="stats">统计分析</button>')
    nav_items.append(f'<button class="nav-btn" data-id="totals">词元总数</button>')
    nav_items.append(f'<button class="nav-btn active" data-id="summary">总结</button>')
    
    # Build summary section (cross-table: articles × languages)
    lang_order = ['classical_chinese', 'modern_chinese', 'english', 'spanish']
    summary_rows = []
    ratio_rows = []
    for article in articles:
        classical_title = next((t['title'] for t in article['texts'] if t['language'] == 'classical_chinese'), article['metadata']['title_zh'])
        cells = []
        ratio_cells = []
        for lang in lang_order:
            cells.append(f'<td class="token-count" data-article="{article["id"]}" data-lang="{lang}">—</td>')
            if lang == 'classical_chinese':
                ratio_cells.append(f'<td class="ratio-cell" data-ratio-article="{article["id"]}">1</td>')
            else:
                ratio_cells.append(f'<td class="ratio-cell" data-ratio-article="{article["id"]}" data-ratio-lang="{lang}">—</td>')
        summary_rows.append(f'<tr><td class="summary-article-name">{classical_title}</td>{"".join(cells)}</tr>')
        ratio_rows.append(f'<tr><td class="summary-article-name">{classical_title}</td>{"".join(ratio_cells)}</tr>')
    
    summary_section = f'''
        <section id="summary" class="article-section active">
            <div class="summary-intro">
                <h2>Token 消耗总览</h2>
                <p>12 篇文章 × 4 种语言的 token 消耗对比。右上角切换分词器，查看不同模型对同一批文本的编码效率。</p>
            </div>
            <div class="summary-table-wrap">
                <table class="summary-table">
                    <thead>
                        <tr><th>文章</th><th class="token-col-header">文言</th><th class="token-col-header">现代汉语</th><th class="token-col-header">English</th><th class="token-col-header">Español</th></tr>
                    </thead>
                    <tbody>{"".join(summary_rows)}</tbody>
                </table>
            </div>
            <div class="summary-intro" style="margin-top:2rem">
                <h2>相对比例（文言=1）</h2>
                <p>各语言 token 数 ÷ 文言 token 数。比例 >1 表示比文言费 token，<1 表示比文言省。</p>
            </div>
            <div class="summary-table-wrap">
                <table class="summary-table ratio-table">
                    <thead>
                        <tr><th>文章</th><th class="token-col-header">文言</th><th class="token-col-header">现代汉语</th><th class="token-col-header">English</th><th class="token-col-header">Español</th></tr>
                    </thead>
                    <tbody>{"".join(ratio_rows)}</tbody>
                </table>
            </div>
            <div style="text-align:center; margin-top:2rem">
                <button class="nav-btn" data-id="stats">详细统计分析（假设检验等） →</button>
            </div>
        </section>
    '''
    
    # Build totals section (per-model token totals from precomputed data)
    totals_rows = []
    os_data = tc_data.get("open_source", {})
    model_totals = {}
    for model_name, articles_data in os_data.items():
        total = 0
        for aid, langs in articles_data.items():
            for count in langs.values():
                if isinstance(count, (int, float)) and count > 0:
                    total += count
        model_totals[model_name] = total
    
    # Labels for display
    OPENAI_LABELS = {
        'r50k_base': 'r50k_base (2020-)',
        'p50k_base': 'p50k_base (2021-)',
        'cl100k_base': 'cl100k_base (2022-)',
        'o200k_base': 'o200k_base (2024-)',
    }
    def totals_label(key):
        if key == 'GPT-2': return 'GPT-2 (2019-)'
        if key == 'Phi-2': return 'Phi-2 (2023-)'
        return key
    
    # Second table baseline (same as precomputed, just exclude classical_chinese)
    no_cc_totals = {}
    exclude_lang = 'classical_chinese'
    for model_name, articles_data in os_data.items():
        total = 0
        for aid, langs in articles_data.items():
            for lang, count in langs.items():
                if lang != exclude_lang and isinstance(count, (int, float)) and count > 0:
                    total += count
        no_cc_totals[model_name] = total
    
    # Compute OpenAI tokenizer totals (for both tables at once)
    try:
        import tiktoken
        for enc_name in ['r50k_base', 'p50k_base', 'cl100k_base', 'o200k_base']:
            enc = tiktoken.get_encoding(enc_name)
            total_all = 0
            total_no_cc = 0
            for article in articles:
                for text in article['texts']:
                    n = len(enc.encode(text['content']))
                    total_all += n
                    if text['language'] != exclude_lang:
                        total_no_cc += n
            label = OPENAI_LABELS[enc_name]
            model_totals[label] = total_all
            no_cc_totals[label] = total_no_cc
    except ImportError:
        pass
    
    for key, total in sorted(model_totals.items(), key=lambda x: x[1]):
        totals_rows.append(f'<tr><td class="summary-article-name">{totals_label(key)}</td><td>{total:,}</td></tr>')
    
    no_cc_rows = []
    for key, total in sorted(no_cc_totals.items(), key=lambda x: x[1]):
        no_cc_rows.append(f'<tr><td class="summary-article-name">{totals_label(key)}</td><td>{total:,}</td></tr>')
    
    totals_section = f'''
        <section id="totals" class="article-section">
            <div class="summary-intro">
                <h2>词元总数</h2>
                <p>各分词器对全部 48 段文本（12 篇 × 4 语言）编码后的 token 总数。在 token 单价相同的情况下，数字越小 = 编码越紧凑 = 越省钱。</p>
            </div>
            <div class="summary-table-wrap" style="max-width:600px; margin:0 auto;">
                <table class="summary-table">
                    <thead><tr><th>分词器</th><th>Token 总数</th></tr></thead>
                    <tbody>{"".join(totals_rows)}</tbody>
                </table>
            </div>
            <div class="summary-intro" style="margin-top:2rem">
                <h2>词元总数（不含文言）</h2>
                <p>仅统计现代汉语、English、Español 三种语言。排除文言后，观察各分词器对日常语言的编码效率。</p>
            </div>
            <div class="summary-table-wrap" style="max-width:600px; margin:0 auto;">
                <table class="summary-table">
                    <thead><tr><th>分词器</th><th>Token 总数（不含文言）</th></tr></thead>
                    <tbody>{"".join(no_cc_rows)}</tbody>
                </table>
            </div>
        </section>
    '''
    
    # Build stats section (split by original language)
    cc_articles = [a for a in articles if a['metadata'].get('original_language') == 'classical_chinese']
    other_articles = [a for a in articles if a['metadata'].get('original_language') != 'classical_chinese']
    
    def build_ratio_table(article_list, title, desc):
        ratio_rows = []
        for article in article_list:
            classical_title = next((t['title'] for t in article['texts'] if t['language'] == 'classical_chinese'), article['metadata']['title_zh'])
            cells = [f'<td class="summary-article-name">{classical_title}</td>']
            for lang in ['classical_chinese', 'modern_chinese', 'english', 'spanish']:
                if lang == 'classical_chinese':
                    cells.append(f'<td class="ratio-cell" data-ratio-article="{article["id"]}">1</td>')
                else:
                    cells.append(f'<td class="ratio-cell" data-ratio-article="{article["id"]}" data-ratio-lang="{lang}">—</td>')
            ratio_rows.append('<tr>{}</tr>'.format(''.join(cells)))
        return f'''
            <div class="summary-intro">
                <h3>{title}（{len(article_list)} 篇）</h3>
                <p>{desc}</p>
            </div>
            <div class="summary-table-wrap">
                <table class="summary-table ratio-table">
                    <thead><tr><th>文章</th><th>文言</th><th>现代汉语</th><th>English</th><th>Español</th></tr></thead>
                    <tbody>{"".join(ratio_rows)}</tbody>
                </table>
            </div>
        '''
    
    stats_section = f'''
        <section id="stats" class="article-section">
            <div class="summary-intro">
                <h2>详细统计分析</h2>
                <p>按原文语言分组，观察"原文→译文"方向的 token 膨胀。切换右上角分词器查看不同模型表现。</p>
            </div>
            {build_ratio_table(cc_articles, "原文为文言", f"这 {len(cc_articles)} 篇文章的原文是文言，现代汉语/英语/西班牙语为译文。比例 = 译文 token ÷ 文言 token。")}
            <div style="margin-top:2rem"></div>
            {build_ratio_table(other_articles, "原文为非文言", f"这 {len(other_articles)} 篇文章的原文是现代汉语/英语/西班牙语之一，文言为译文。比例 = 各语言 token ÷ 文言 token。")}
            <div style="text-align:center; margin-top:2rem">
                <p style="color:var(--text-secondary); font-size:0.8rem; line-height:1.8">
                <b>方法论说明</b><br><br>

                <b>1. 为何用单边检验？</b><br>
                研究问题是"文言能否省 token"，不是"文言 token 数是否等同于其他语言"。前者是单边（H₀：文言 ≥ 某语言，H₁：文言 &lt; 某语言），后者是双边。<br><br>

                <b>2. α=0.05 是超参数</b><br>
                α=0.05 是 Fisher 在 1925 年《研究工作者的统计方法》中建议的一个"便利参考线"。它不是来自数学推导，也不是来自实际需求——纯粹是一个约定俗成的超参数。n 太小时即便真实效应存在，p 值也很难跨过 0.05，此时不应纠结"是否显著"，而应关注效应量和 p 值本身。<br><br>

                <b>3. 四种检验方法的取舍</b><br>
                (a) t 检验：假设差值正态分布。n<10 时 Shapiro-Wilk 检验功效太低，无法验证正态性——"测不出来偏离"不等于"真的正态"。中心极限定理在 n&lt;30 不起作用。不可用。<br>
                (b) Fisher 精确检验（置换检验）：不假设任何分布。穷举所有 2<sup>n</sup> 种符号排列，计算观察到同样或更极端均值的排列比例 = p 值。n=5 仅 2<sup>5</sup>=32 种排列，信息量有限但不假设分布。选用。<br>
                (c) Wilcoxon 符号秩检验：也不假设分布。把差值排秩（1~n），看正号秩和落在哪。比 Fisher 多一层"秩加权"——对差值大小更敏感，但对符号方向同样受限。选用。<br>
                (d) Bootstrap：有放回重抽样做置信区间，n=5 时反复抽来抽去就 5 个点，宽到没有参考价值；若用于打乱标签做置换检验则与 Fisher 完全等价——Fisher 已穷举全部 2<sup>n</sup> 种排列，再抽样是画蛇添足。不用。<br><br>

                <b>4. 这里的 Fisher 精确检验就是女士品茶吗？</b><br>
                是。
                </p>
            </div>
            
            <div class="summary-table-wrap" style="margin-top:2rem">
                <h3 style="text-align:center;color:var(--accent);margin-bottom:0.5rem">假设检验 — 原文为文言（n={len(cc_articles)}）</h3>
                <table class="summary-table">
                    <thead><tr><th>分词器</th><th colspan="2" style="text-align:center">vs 现代汉语<br><small style="color:var(--text-secondary);font-weight:400">H₀：文言 ≥ 现代汉语<br>H₁：文言 &lt; 现代汉语</small></th><th colspan="2" style="text-align:center">vs English<br><small style="color:var(--text-secondary);font-weight:400">H₀：文言 ≥ English<br>H₁：文言 &lt; English</small></th><th colspan="2" style="text-align:center">vs Español<br><small style="color:var(--text-secondary);font-weight:400">H₀：文言 ≥ Español<br>H₁：文言 &lt; Español</small></th></tr>
                    <tr><th></th><th>Fisher 精确检验 p</th><th>Wilcoxon 符号秩 p</th><th>Fisher 精确检验 p</th><th>Wilcoxon 符号秩 p</th><th>Fisher 精确检验 p</th><th>Wilcoxon 符号秩 p</th></tr></thead>
                    <tbody id="pv-cc"><tr><td colspan="7" style="text-align:center;color:var(--text-secondary)">—</td></tr></tbody>
                </table>
            </div>
            <div class="summary-table-wrap" style="margin-top:2rem">
                <h3 style="text-align:center;color:var(--accent);margin-bottom:0.5rem">效应量 — 原文为文言（n={len(cc_articles)}）</h3>
                <table class="summary-table">
                    <thead><tr><th>分词器</th><th colspan="2" style="text-align:center">vs 现代汉语</th><th colspan="2" style="text-align:center">vs English</th><th colspan="2" style="text-align:center">vs Español</th></tr>
                    <tr><th></th><th>Cohen's d</th><th>Hedge's g</th><th>Cohen's d</th><th>Hedge's g</th><th>Cohen's d</th><th>Hedge's g</th></tr></thead>
                    <tbody id="ef-cc"><tr><td colspan="7" style="text-align:center;color:var(--text-secondary)">—</td></tr></tbody>
                </table>
                <p style="text-align:center;color:var(--text-secondary);font-size:0.7rem;margin-top:0.3rem">d / g ≥ 0.2 小，≥ 0.5 中，≥ 0.8 大。Hedge's g 对小样本做偏差修正。</p>
            </div>
            <div class="summary-table-wrap" style="margin-top:2rem">
                <h3 style="text-align:center;color:var(--accent);margin-bottom:0.5rem">假设检验 — 原文为非文言（n={len(other_articles)}）</h3>
                <table class="summary-table">
                    <thead><tr><th>分词器</th><th colspan="2" style="text-align:center">vs 现代汉语<br><small style="color:var(--text-secondary);font-weight:400">H₀：文言 ≥ 现代汉语<br>H₁：文言 &lt; 现代汉语</small></th><th colspan="2" style="text-align:center">vs English<br><small style="color:var(--text-secondary);font-weight:400">H₀：文言 ≥ English<br>H₁：文言 &lt; English</small></th><th colspan="2" style="text-align:center">vs Español<br><small style="color:var(--text-secondary);font-weight:400">H₀：文言 ≥ Español<br>H₁：文言 &lt; Español</small></th></tr>
                    <tr><th></th><th>Fisher 精确检验 p</th><th>Wilcoxon 符号秩 p</th><th>Fisher 精确检验 p</th><th>Wilcoxon 符号秩 p</th><th>Fisher 精确检验 p</th><th>Wilcoxon 符号秩 p</th></tr></thead>
                    <tbody id="pv-other"><tr><td colspan="7" style="text-align:center;color:var(--text-secondary)">—</td></tr></tbody>
                </table>
            </div>
            <div class="summary-table-wrap" style="margin-top:2rem">
                <h3 style="text-align:center;color:var(--accent);margin-bottom:0.5rem">效应量 — 原文为非文言（n={len(other_articles)}）</h3>
                <table class="summary-table">
                    <thead><tr><th>分词器</th><th colspan="2" style="text-align:center">vs 现代汉语</th><th colspan="2" style="text-align:center">vs English</th><th colspan="2" style="text-align:center">vs Español</th></tr>
                    <tr><th></th><th>Cohen's d</th><th>Hedge's g</th><th>Cohen's d</th><th>Hedge's g</th><th>Cohen's d</th><th>Hedge's g</th></tr></thead>
                    <tbody id="ef-other"><tr><td colspan="7" style="text-align:center;color:var(--text-secondary)">—</td></tr></tbody>
                </table>
            </div>
        </section>
    '''
    
    # Compute p-values for all tokenizers, split by original language
    import itertools
    from scipy.stats import wilcoxon
    
    def compute_pvalues(token_counts_by_lang, aids):
        """Compute paired permutation and Wilcoxon p-values for classical vs other."""
        results = {}
        classical = [token_counts_by_lang[aid]['classical_chinese'] for aid in aids if aid in token_counts_by_lang]
        n = len(classical)
        for compare_lang in ['modern_chinese', 'english', 'spanish']:
            compare = [token_counts_by_lang[aid][compare_lang] for aid in aids if aid in token_counts_by_lang]
            diffs = [c - cp for c, cp in zip(classical, compare)]
            obs_mean = sum(diffs) / n if n > 0 else 0
            
            # Exhaustive Fisher exact (permutation) test — one-sided: H₁: 文言 < X
            count_extreme = 0
            total = 0
            for signs in itertools.product([1, -1], repeat=n):
                perm_mean = sum(s * d for s, d in zip(signs, diffs)) / n
                if perm_mean <= obs_mean:
                    count_extreme += 1
                total += 1
            fisher_p = count_extreme / total
            
            # Wilcoxon signed-rank — one-sided: H₁: 文言 < X
            diffs_nz = [d for d in diffs if d != 0]
            wp = float('nan')
            if len(diffs_nz) >= 3:
                try:
                    _, wp = wilcoxon(diffs_nz, method='exact', alternative='less')
                except Exception:
                    _, wp = wilcoxon(diffs_nz, alternative='less')
            results[compare_lang] = {'fisher_p': fisher_p, 'wilcoxon_p': wp, 'n': n}
            
            # Effect size (Cohen's d, Hedge's g) — paired
            mean_d = sum(diffs) / n
            sd_d = (sum((d - mean_d)**2 for d in diffs) / (n - 1)) ** 0.5 if n > 1 else 1
            d_val = abs(mean_d / sd_d) if sd_d > 0 else 0
            g_val = d_val * (1 - 3/(4*n - 9)) if n > 2 else d_val
            results[compare_lang]['cohens_d'] = d_val
            results[compare_lang]['hedges_g'] = g_val
        return results
    
    article_ids = [a['id'] for a in articles]
    cc_ids = [a['id'] for a in cc_articles]
    ot_ids = [a['id'] for a in other_articles]
    
    pvalue_data = {'cc': {}, 'other': {}}
    
    # Precomputed models
    for name, articles_data in tc_data.get('open_source', {}).items():
        pvalue_data['cc'][name] = compute_pvalues(articles_data, cc_ids)
        pvalue_data['other'][name] = compute_pvalues(articles_data, ot_ids)
    
    # OpenAI encodings
    try:
        import tiktoken
        for enc_name in ['r50k_base', 'p50k_base', 'cl100k_base', 'o200k_base']:
            enc = tiktoken.get_encoding(enc_name)
            counts = {}
            for article in articles:
                aid = article['id']
                counts[aid] = {}
                for text in article['texts']:
                    counts[aid][text['language']] = len(enc.encode(text['content']))
            pvalue_data['cc'][enc_name] = compute_pvalues(counts, cc_ids)
            pvalue_data['other'][enc_name] = compute_pvalues(counts, ot_ids)
    except Exception as e:
        print(f"  [WARN] OpenAI p-value computation failed: {e}")
    
    pvalue_json = json.dumps(pvalue_data, ensure_ascii=False)
    
    # Build article sections
    sections = [summary_section, totals_section, stats_section]
    for i, article in enumerate(articles):
        meta = article['metadata']
        texts = article['texts']
        
        classical_title = next((t['title'] for t in texts if t['language'] == 'classical_chinese'), meta['title_zh'])
        lang_order = {'classical_chinese': 0, 'modern_chinese': 1, 'english': 2, 'spanish': 3}
        texts_sorted = sorted(texts, key=lambda x: lang_order.get(x['language'], 99))
        
        # Build text cards
        cards = []
        for text in texts_sorted:
            cfg = LANG_CONFIG.get(text['language'], {'label': text['language'], 'css': '', 'dot': '#fff'})
            role_text = '原文' if text['role'] == 'original' else '译文'
            char_count = len(text['content'])
            content_fixed = text['content'].replace('\\n', '\n')
            
            cards.append(f'''
                <div class="text-card {cfg['css']}">
                    <div class="card-header"><span class="lang-name">{cfg['label']}</span><span class="role-badge {'original' if text['role'] == 'original' else 'translation'}">{role_text}</span></div>
                    <div class="card-body"><h4>{text['title']}</h4><pre>{content_fixed}</pre></div>
                    <div class="card-footer">{char_count:,} 字符</div>
                </div>
            ''')
        
        # Build comparison table rows (with token column)
        rows = []
        for text in texts_sorted:
            cfg = LANG_CONFIG.get(text['language'], {'label': text['language'], 'dot': '#fff'})
            role_text = '原文' if text['role'] == 'original' else '译文'
            rows.append(f'''
                <tr><td><span class="dot" style="background:{cfg['dot']}"></span>{cfg['label']}</td><td>{role_text}</td><td>{text['title']}</td><td>{len(text['content']):,}</td><td class="token-count" data-article="{article['id']}" data-lang="{text['language']}">—</td></tr>
            ''')
        
        sections.append(f'''
        <section id="{article['id']}" class="article-section">
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
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border);
            transition: background 0.3s, transform 0.35s ease;
        }}
        nav.nav-hidden {{
            transform: translateY(-100%);
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
        
        /* Summary page */
        .summary-intro {{
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
            text-align: center;
        }}
        .summary-intro h2 {{ color: var(--accent); font-size: 1.5rem; margin-bottom: 0.5rem; }}
        .summary-intro p {{ color: var(--text-secondary); }}
        .summary-table-wrap {{
            background: var(--bg-card);
            border-radius: 12px;
            overflow-x: auto;
            border: 1px solid var(--border);
        }}
        .summary-table {{ width: 100%; border-collapse: collapse; }}
        .summary-table th {{
            background: var(--bg-card-inner);
            padding: 1rem;
            text-align: center;
            color: var(--accent);
            font-weight: 600;
            border-bottom: 2px solid var(--border);
        }}
        .summary-table td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
            text-align: center;
            transition: background 0.2s;
        }}
        .summary-table tr:hover td {{ background: var(--hover-bg); }}
        .summary-article-name {{
            text-align: center !important;
            font-weight: 500;
            white-space: nowrap;
        }}
        .ratio-cell {{ font-variant-numeric: tabular-nums; }}
        /* ========== Mobile Responsive ========== */
        @media (max-width: 768px) {{
            header {{ padding: 1.5rem 1rem; }}
            header h1 {{ font-size: 1.5rem; }}
            .theme-toggle {{ top: 1rem; right: 1rem; padding: 0.4rem 0.8rem; font-size: 0.8rem; }}
            
            nav {{ padding: 0.5rem; gap: 0.4rem; }}
            .nav-btn {{ padding: 0.5rem 0.75rem; font-size: 0.85rem; }}
            .tokenizer-bar {{ 
                width: 100%; 
                margin-left: 0; 
                padding-left: 0; 
                padding-top: 0.5rem;
                border-left: none; 
                border-top: 1px solid var(--border);
                justify-content: center;
            }}
            
            main {{ padding: 1rem; }}
            
            .metadata {{ padding: 1rem; }}
            .metadata h2 {{ font-size: 1.25rem; }}
            .meta-grid {{ grid-template-columns: 1fr; gap: 0.75rem; }}
            
            .comparison {{ overflow-x: auto; -webkit-overflow-scrolling: touch; }}
            .comparison table {{ min-width: 600px; font-size: 0.9rem; }}
            .comparison th, .comparison td {{ padding: 0.75rem 0.5rem; }}
            
            .text-grid {{ gap: 1rem; }}
            .card-header {{ padding: 0.75rem 1rem; }}
            .card-body {{ padding: 1rem; max-height: 400px; }}
            .card-body h4 {{ font-size: 1rem; }}
            .card-body pre {{ font-size: 0.9rem; line-height: 1.7; }}
            .card-footer {{ padding: 0.75rem 1rem; }}
            
            footer {{ padding: 1.5rem 1rem; }}
            .footer-links {{ display: flex; flex-direction: column; gap: 0.5rem; align-items: center; }}
            .footer-links a {{ margin: 0; }}
        }}
        
        @media (max-width: 480px) {{
            header h1 {{ font-size: 1.25rem; }}
            header p {{ font-size: 0.85rem; }}
            .theme-toggle {{ position: static; margin-top: 0.5rem; display: inline-block; }}
            
            .nav-btn {{ padding: 0.4rem 0.6rem; font-size: 0.8rem; border-radius: 6px; }}
            .tokenizer-select {{ font-size: 0.85rem; padding: 0.4rem 0.75rem; }}
            
            .comparison table {{ min-width: 500px; font-size: 0.85rem; }}
            .comparison th, .comparison td {{ padding: 0.6rem 0.4rem; }}
            
            .card-body {{ max-height: 350px; }}
            .card-body pre {{ font-size: 0.85rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <button class="theme-toggle" onclick="toggleTheme()" title="切换主题"></button>
        <h1>用文言，可省词元乎？</h1>
        <p>Token Consumption Comparison · 四种语言 · {len(articles)}篇文章 · 多分词器对比</p>
    </header>
    
    <nav>
        {' '.join(nav_items)}
        <div class="tokenizer-bar">
            <label for="tokenizer-select">分词器：</label>
            <select id="tokenizer-select" class="tokenizer-select">
                <optgroup label="OpenAI（实时）">
<option value="r50k_base">r50k_base — gpt-3 / text-davinci-001（2020-）</option>
<option value="p50k_base">p50k_base — code-davinci-002 / text-davinci-003（2021-）</option>
<option value="cl100k_base">cl100k_base — gpt-3.5-turbo / gpt-4（2022-）</option>
<option value="o200k_base">o200k_base — gpt-4o / gpt-4.1 / o1 / o3 / gpt-5.x（2024-）</option>
                </optgroup>
                <optgroup label="开源预计算 — Qwen 词表演变">
<option value="Qwen-7B (2023-)">Qwen 1.0 / 1.5 / 2.0 — 150K 词表 (2023-)</option>
<option value="Qwen2.5-72B (2024-)">Qwen 2.5 / 3.0 — 151K 词表 (2024-)</option>
<option value="Qwen3.5-27B (2026-)">Qwen 3.5 — 248K 词表 (2026-)</option>
                </optgroup>
                <optgroup label="开源预计算 — DeepSeek 词表演变">
                    <option value="DeepSeek LLM (2023.11-)">DeepSeek LLM — 100K 词表 (2023.11-)</option>
                    <option value="DeepSeek-V2 (2024.05-)">DeepSeek-V2 — 100K 词表 (2024.05-)</option>
                    <option value="DeepSeek-V3/R1/V4 (2024.12-)" selected>DeepSeek-V3/R1/V4 — 128K 词表 (2024.12-)</option>
                </optgroup>
                <optgroup label="开源预计算 — 其它">
<option value="GPT-2">GPT-2 (2019-)</option>
<option value="Phi-2">Phi-2 (2023-)</option>
                </optgroup>
            </select>
        </div>
    </nav>
    
    <main>
        {' '.join(sections)}
    </main>
    
    <footer>
        <p>{len(articles)}×4 Multilingual Corpus | Token Consumption Comparison</p>
        <div class="footer-links">
            <span>友情链接 / Friendly Links:</span>
            <a href="https://gpt-tokenizer.dev/" target="_blank" rel="noopener">GPT Tokenizer</a>
            <a href="https://www.danieldemmel.me/tokenizer" target="_blank" rel="noopener">LLM Tokenizer</a>
            <a href="https://tiktokenizer.vercel.app/" target="_blank" rel="noopener">tiktokenizer</a>
            <a href="https://platform.openai.com/tokenizer" target="_blank" rel="noopener">OpenAI Tokenizer</a>
        </div>
    </footer>
    
    <script>
        let lastScrollY = window.scrollY;
        const nav = document.querySelector('nav');
        const NAV_HIDE_THRESHOLD = 80;

        window.addEventListener('scroll', () => {{
            const currentScrollY = window.scrollY;
            if (currentScrollY < NAV_HIDE_THRESHOLD) {{
                nav.classList.remove('nav-hidden');
            }} else if (currentScrollY > lastScrollY) {{
                nav.classList.add('nav-hidden');
            }} else {{
                nav.classList.remove('nav-hidden');
            }}
            lastScrollY = currentScrollY;
        }}, {{ passive: true }});

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
            if (attr === 'light') {{ icon = '\\u2600\\ufe0f'; label = '\u6d45\u8272'; }}
            else if (attr === 'dark') {{ icon = '\\ud83c\\udf19'; label = '\u6df1\u8272'; }}
            else {{ icon = '\\ud83d\\udcbb'; label = '\u8ddf\u968f\u7cfb\u7edf'; }}
            themeBtn.textContent = `${{icon}} ${{label}}`;
            const effective = getEffectiveTheme();
            themeBtn.title = `\u5f53\u524d\u6a21\u5f0f: ${{label}} (\u5b9e\u9645: ${{effective === 'dark' ? '\u6df1\u8272' : '\u6d45\u8272'}}) \u2014 \u70b9\u51fb\u5207\u6362`;
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
    <script>
        window.PRECOMPUTED_TOKENS = {token_counts_json};
        window.PVALUES = {pvalue_json};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/o200k_base.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/cl100k_base.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/p50k_base.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer@2.9.0/dist/r50k_base.js"></script>
    <script>
        const ENCODERS = {{
            'r50k_base':  GPTTokenizer_r50k_base,
            'p50k_base':  GPTTokenizer_p50k_base,
            'cl100k_base': GPTTokenizer_cl100k_base,
            'o200k_base': GPTTokenizer_o200k_base,
        }};

        const OPEN_SOURCE_MODELS = [
            'Qwen-7B (2023-)', 'Qwen2.5-72B (2024-)', 'Qwen3.5-27B (2026-)',
            'DeepSeek LLM (2023.11-)', 'DeepSeek-V2 (2024.05-)', 'DeepSeek-V3/R1/V4 (2024.12-)',
            'GPT-2', 'Phi-2'
        ];

        function isOpenSource(name) {{ return OPEN_SOURCE_MODELS.includes(name); }}

        const textCache = new Map();
        function getText(articleId, lang) {{
            const key = `${{articleId}}::${{lang}}`;
            if (textCache.has(key)) return textCache.get(key);
            const section = document.getElementById(articleId);
            if (!section) return '';
            const cards = section.querySelectorAll('.text-card');
            for (const card of cards) {{
                const langClass = Array.from(card.classList).find(c => c.startsWith('lang-') && !c.endsWith('-name'));
                if (!langClass) continue;
                const pre = card.querySelector('pre');
                if (!pre) continue;
                let cardLang = null;
                if (langClass === 'lang-classical') cardLang = 'classical_chinese';
                else if (langClass === 'lang-modern') cardLang = 'modern_chinese';
                else if (langClass === 'lang-english') cardLang = 'english';
                else if (langClass === 'lang-spanish') cardLang = 'spanish';
                if (cardLang === lang) {{ textCache.set(key, pre.textContent); return pre.textContent; }}
            }}
            return '';
        }}

        function countTokens(text, tokenizerName) {{
            const encoder = ENCODERS[tokenizerName];
            if (!encoder || typeof encoder.encode !== 'function') return -1;
            try {{ return encoder.encode(text).length; }} catch(e) {{ return -1; }}
        }}

        let currentTokenizer = 'DeepSeek-V3/R1/V4 (2024.12-)';

        function updateAllTokenCounts() {{
            const name = currentTokenizer;
            document.querySelectorAll('.tokenizer-name').forEach(el => {{ el.textContent = `(${{name}})`; }});
            const cells = document.querySelectorAll('.token-count');
            cells.forEach(cell => {{ cell.classList.add('loading'); cell.textContent = '...'; }});
            setTimeout(() => {{
                cells.forEach(cell => {{
                    const articleId = cell.dataset.article;
                    const lang = cell.dataset.lang;
                    cell.classList.remove('loading');
                    if (isOpenSource(name)) {{
                        const pre = window.PRECOMPUTED_TOKENS;
                        if (pre && pre.open_source && pre.open_source[name] && pre.open_source[name][articleId] && pre.open_source[name][articleId][lang] !== undefined) {{
                            cell.textContent = pre.open_source[name][articleId][lang].toLocaleString();
                        }} else {{
                            cell.textContent = '\u9700\u9884\u8ba1\u7b97';
                            cell.title = '\u8fd0\u884c code/precompute_tokens.js \u751f\u6210\u6570\u636e';
                        }}
                        return;
                    }}
                    const text = getText(articleId, lang);
                    if (!text) {{ cell.textContent = '\u2014'; return; }}
                    const count = countTokens(text, name);
                    cell.textContent = count > 0 ? count.toLocaleString() : '\u2014';
                }});
                // Update ratio table
                document.querySelectorAll('.ratio-cell[data-ratio-lang]').forEach(cell => {{
                    const articleId = cell.dataset.ratioArticle;
                    const lang = cell.dataset.ratioLang;
                    const classicalText = getText(articleId, 'classical_chinese');
                    const langText = getText(articleId, lang);
                    if (!classicalText || !langText) {{ cell.textContent = '\u2014'; return; }}
                    let classicalCount, langCount;
                    if (isOpenSource(name)) {{
                        const pre = window.PRECOMPUTED_TOKENS;
                        classicalCount = pre?.open_source?.[name]?.[articleId]?.['classical_chinese'];
                        langCount = pre?.open_source?.[name]?.[articleId]?.[lang];
                    }} else {{
                        classicalCount = countTokens(classicalText, name);
                        langCount = countTokens(langText, name);
                    }}
                    if (classicalCount > 0 && langCount > 0) {{
                        cell.textContent = (langCount / classicalCount).toFixed(2);
                    }} else {{
                        cell.textContent = '\u2014';
                    }}
                }});
            }}, 10);

            // Update p-value + effect size tables
            updatePvalues(name);
            updateEffects(name);
        }}

        function updatePvalues(name) {{
            ['cc', 'other'].forEach(group => {{
                const body = document.getElementById('pv-' + group);
                if (!body) return;
                const gd = window.PVALUES?.[group];
                if (!gd || !gd[name]) {{ body.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-secondary)">—</td></tr>'; return; }}
                const d = gd[name];
                const langs = ['modern_chinese', 'english', 'spanish'];
                let html = '<tr><td class="summary-article-name">' + name + '</td>';
                for (const l of langs) {{
                    const fp = d[l].fisher_p < 0.0001 ? '&lt;0.0001' : d[l].fisher_p.toFixed(4);
                    const wp = isNaN(d[l].wilcoxon_p) ? '—' : (d[l].wilcoxon_p < 0.0001 ? '&lt;0.0001' : d[l].wilcoxon_p.toFixed(4));
                    html += '<td>' + fp + '</td><td>' + wp + '</td>';
                }}
                body.innerHTML = html + '</tr>';
            }});
        }}

        function updateEffects(name) {{
            ['cc', 'other'].forEach(group => {{
                const body = document.getElementById('ef-' + group);
                if (!body) return;
                const gd = window.PVALUES?.[group];
                if (!gd || !gd[name]) {{ body.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-secondary)">—</td></tr>'; return; }}
                const d = gd[name];
                const langs = ['modern_chinese', 'english', 'spanish'];
                let html = '<tr><td class="summary-article-name">' + name + '</td>';
                for (const l of langs) {{
                    html += '<td>' + d[l].cohens_d.toFixed(2) + '</td><td>' + d[l].hedges_g.toFixed(2) + '</td>';
                }}
                body.innerHTML = html + '</tr>';
            }});
        }}

        document.getElementById('tokenizer-select').addEventListener('change', function() {{
            currentTokenizer = this.value;
            updateAllTokenCounts();
        }});

        document.addEventListener('DOMContentLoaded', updateAllTokenCounts);
        if (document.readyState !== 'loading') updateAllTokenCounts();
    </script>
</body>
</html>'''
    
    output = './index.html'
    with open(output, 'w', encoding='utf-8', errors='replace') as f:
        f.write(html)
    
    print(f"Generated: {output}")
    print(f"Articles: {len(articles)}")
    print(f"Open in browser to compare token consumption")
    return output

if __name__ == '__main__':
    build_index()
