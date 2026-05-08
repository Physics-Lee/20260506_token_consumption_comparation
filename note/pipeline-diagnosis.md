# 流水线诊断与修复方案

## 现状

原始设计：

```
翻译文本 (.txt)
    ↓  generate_json.py
结构化数据 (data/*.json)
    ↓  json2html.py
交互式阅读器 (corpus_reader.html)
    ↓  浏览器查看
4 语言平行对照展示
```

## 断点

### 断点 1：翻译源文件已删除

- 所有 `.txt` 翻译源文件已被删除
- `generate_json.py` 无法运行（读取不存在的 txt）

### 断点 2：json2html.py 路径错误 + 样式过时

- 第 11 行 `if Path(filename).exists()` 在当前目录查找 JSON，但数据在 `data/` 子目录 → 脚本不可运行
- 模板样式是旧版暗色主题，缺少：
  - CSS 变量（`:root` / `[data-theme="dark"]`）
  - 三态主题切换 JS（浅色 / 深色 / 跟随系统）
  - `theme-toggle` 按钮

### 断点 3：HTML 是硬编码产物

- `corpus_reader.html` 四篇文章全部硬编码在 HTML 中
- 加新文章必须手动改 1000+ 行 HTML
- 样式更新也必须手改 HTML

## 修复方案

**一步到位**：重写 `json2html.py`，从 `data/*.json` 直接生成新版 HTML。

### 改动点

1. **读取路径**：`data/*.json` 替代当前目录
2. **模板升级**：移植 `corpus_reader.html` 中的新版样式：
   - CSS 自定义属性（`:root` 浅色 + `[data-theme="dark"]` 深色）
   - 语言颜色适配（`[data-theme="light"]` 下的覆写）
   - 三态主题切换按钮 + JS 逻辑
3. **保持纯静态**：不在 HTML 中引入运行时 JSON 动态加载（零依赖，直接生成完整 HTML）
4. **反向生成**：因为 .txt 已丢，`generate_json.py` 不再使用；如有需要可从现有 HTML 提取内容补充 JSON

### 效果

- 加新文章 → 扔一个 JSON 进 `data/` → 跑一次脚本 → 生成完整 HTML
- 样式更新 → 改脚本模板 → 重新生成
- 主题系统与 HTML 保持一致
