# 项目更新流程

## 概述

本项目采用**数据驱动生成**模式：

```
resource/*.md（原文Markdown）
    ↓ 手动翻译/编辑
        ↓ 方式一：md2json.py 生成骨架
        ↓ 方式二：手动填充翻译
    data/*.json（规范数据）
        ↓ precompute_tokens.py（可选）
    data/token_counts.json（预计算token数）
        ↓ json2html.py / build_index.py
    corpus_reader.html（阅读器）
    index.html（token对比工具）
        ↓ git push
    github.io 线上部署
```

**黄金法则**：
- `corpus_reader.html` 和 `index.html` **永远不要手动编辑**
- 所有改动都应在 `data/*.json` 或 Python 脚本中完成，然后重新生成

---

## 场景一：新增一篇文章

### 步骤 1：准备原文 Markdown

将原文放入 `resource/`，文件名用英文，格式：

```markdown
# 标题

正文...
```

示例：`resource/My_Article.md`

### 步骤 2A：自动生成 JSON 骨架（推荐）

```bash
python code/md2json.py resource/My_Article.md --lang modern_chinese
```

这会生成 `data/my_article.json`，包含：
- 从 Markdown 提取的 metadata（需手动补充 title_en, title_es 等）
- 原文内容放在 `modern_chinese` 语言槽
- 其他 3 个语言槽为占位符 `"[待翻译]"`

### 步骤 2B：手动创建 JSON

如果骨架生成器不适用，直接创建 JSON 文件：

```json
{
  "id": "my_article",
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
    {"language": "classical_chinese", "role": "translation", "title": "文言标题", "content": "..."},
    {"language": "modern_chinese", "role": "original", "title": "现代汉语标题", "content": "..."},
    {"language": "english", "role": "translation", "title": "English Title", "content": "..."},
    {"language": "spanish", "role": "translation", "title": "Título en Español", "content": "..."}
  ]
}
```

**重要**：用 Python `json.dump()` 生成，不要手动拼接字符串，否则引号不会自动转义。

### 步骤 3：翻译填充

编辑 `data/my_article.json`，将 `classical_chinese`、`english`、`spanish` 的内容从占位符替换为实际译文。

### 步骤 4：重新生成 HTML

```bash
# 生成阅读器（面向人类读者）
python code/json2html.py

# 生成 token 对比页面（面向研究者）
python code/build_index.py
```

### 步骤 5：预计算 token（可选但推荐）

如果新增了文章，且希望 `index.html` 中的开源模型 token 数正确：

```bash
python code/precompute_tokens.py
```

这需要：
- `pip install transformers huggingface_hub`
- HuggingFace 账号（部分模型如 Llama、DeepSeek 需要 token 访问权限）
- 足够磁盘空间（tokenizer 模型文件约 1-5MB/个，但下载过程需要临时空间）

### 步骤 6：提交部署

```bash
git add data/my_article.json resource/My_Article.md corpus_reader.html index.html data/token_counts.json
git commit -m "add article: My Article"
git push
```

github.io 会自动更新（通常 1-2 分钟内生效）。

---

## 场景二：修改现有文章

如果只是修改某篇文章的译文或 metadata：

```bash
# 1. 编辑 data/xxx.json
# 2. 重新生成 HTML
python code/json2html.py
python code/build_index.py

# 3. 如果修改了内容长度，建议重新预计算 token
python code/precompute_tokens.py

# 4. 提交
git add data/xxx.json corpus_reader.html index.html data/token_counts.json
git commit -m "update article xxx: fix translation"
git push
```

---

## 场景三：更新页面样式或功能

如果需要修改 UI（如新增按钮、调整颜色、修改布局）：

```bash
# 1. 修改 code/json2html.py 中的 HTML/CSS/JS 模板
# 2. 同步修改 code/build_index.py（两个页面共用大部分样式）
# 3. 重新生成
python code/json2html.py
python code/build_index.py

# 4. 提交
git add code/json2html.py code/build_index.py corpus_reader.html index.html
git commit -m "feat: add new UI feature"
git push
```

**注意**：两个生成脚本的模板代码高度重复（约 80% CSS 相同），未来可考虑提取公共模板。

---

## 场景四：仅更新 token 预计算数据

当 HuggingFace 新增模型或现有模型更新时：

```bash
# 1. 修改 precompute_tokens.py 中的 OPEN_SOURCE_MODELS 字典
# 2. 运行预计算
python code/precompute_tokens.py

# 3. 重新生成 index.html（因为 token_counts.json 变了）
python code/build_index.py

# 4. 提交
git add code/precompute_tokens.py data/token_counts.json index.html
git commit -m "feat: add tokenizer for XXX"
git push
```

---

## 场景五：更新 README 或文档

```bash
# 直接编辑 markdown 文件
git add README.md note/xxx.md
git commit -m "docs: update ..."
git push
```

文档不需要重新生成 HTML。

---

## 快速检查清单

每次提交前确认：

- [ ] `data/*.json` 格式合法（可用 `python -m json.tool data/xxx.json` 验证）
- [ ] 重新运行了 `json2html.py` 和 `build_index.py`
- [ ] 如果新增/修改了文章内容，运行了 `precompute_tokens.py`
- [ ] `corpus_reader.html` 和 `index.html` 已更新
- [ ] 本地浏览器打开确认无报错

---

## 常见错误

### 错误 1：JSON 里包含未转义的引号

```json
// ❌ 错误
"content": "他说："你好""

// ✅ 正确
"content": "他说：\"你好\""
```

**解决**：始终用 `json.dump()` 生成 JSON，不要手写。

### 错误 2：忘运行 precompute_tokens.py

现象：`index.html` 中新增文章的 token 数显示 "需预计算"

**解决**：运行 `python code/precompute_tokens.py` 后重新生成 `index.html`。

### 错误 3：忘同步修改两个生成脚本

现象：`corpus_reader.html` 有新功能但 `index.html` 没有

**解决**：两个脚本修改后都要重新运行。未来建议提取公共模板减少重复。

### 错误 4：git push 后 github.io 没更新

**解决**：
1. 确认推送到的是 `gh-pages` 或 `main` 分支（取决于仓库设置）
2. 等待 1-2 分钟
3. 强制刷新浏览器（Ctrl+F5 / Cmd+Shift+R）
4. 检查 GitHub 仓库 Settings → Pages 的部署状态

---

## 文件变更矩阵

| 你修改了 | 必须运行 | 生成的文件 |
|---|---|---|
| `resource/*.md` | — | 仅作为备份，不直接参与构建 |
| `data/*.json` | `json2html.py` + `build_index.py` | `corpus_reader.html`, `index.html` |
| `data/*.json` 内容 | `precompute_tokens.py` | `data/token_counts.json` |
| `code/json2html.py` | `json2html.py` | `corpus_reader.html` |
| `code/build_index.py` | `build_index.py` | `index.html` |
| `code/precompute_tokens.py` | `precompute_tokens.py` + `build_index.py` | `data/token_counts.json`, `index.html` |
| `README.md`, `note/*.md` | 无需运行 | — |
