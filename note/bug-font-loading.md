# Bug：github.io 上字体显示不一致

## 现象

- **本地打开** `corpus_reader.html`：字体显示正常，长文阅读舒适
- **github.io 上打开**：字体明显变了，中文显示为系统默认字体（Windows 微软雅黑 / macOS 苹方），阅读体验下降

## 根本原因

### CSS 只声明了字体名，没有加载字体文件

`json2html.py` 生成的 CSS 中有：

```css
font-family: "Noto Sans SC", "Noto Serif SC", serif;
```

但这行代码只是告诉浏览器：**"如果你系统里有这两个字体，就用它们；没有的话，用 serif 回退"**。

它并没有把字体文件下载到用户的浏览器里。

### 为什么本地正常，线上不正常

| 环境 | 是否安装了 Noto 字体 | 实际渲染字体 | 效果 |
|---|---|---|---|
| 本地开发机 | ✅ 已安装（可能通过其他项目/系统自带） | Noto Sans/Noto Serif | 正常 |
| github.io 访问者 | ❌ 99% 未安装 | 微软雅黑 / 苹方 / 宋体 | 不一致 |

## 教训

**声明 `font-family` ≠ 加载字体文件**

要让所有用户看到一致的字体，必须通过以下方式之一实际引入字体：

1. **CDN 加载**（本项目采用）
2. **@font-face 自托管**
3. **npm 包 + 构建工具处理**

只写 `font-family` 是"尽力而为"，不是"保证送达"。

## 修复过程

### 修复前（问题代码）

```html
<head>
    <meta charset="UTF-8">
    <title>用文言，可省词元乎？</title>
    <style>
        /* 只声明了名字，没有加载文件 */
        body { font-family: "Noto Sans SC", "Noto Serif SC", serif; }
    </style>
</head>
```

### 修复后（正确代码）

```html
<head>
    <meta charset="UTF-8">
    <title>用文言，可省词元乎？</title>
    <!-- 1. 预连接字体服务器，减少加载延迟 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <!-- 2. 实际加载字体文件 -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* 现在浏览器真的有这些字体了 */
        body { font-family: "Noto Sans SC", "Noto Serif SC", serif; }
    </style>
</head>
```

### 关键改进点

1. **`preconnect`**
   - 提前与 `fonts.googleapis.com` 和 `fonts.gstatic.com` 建立 TCP + TLS 连接
   - 节省 100–300ms 的握手时间

2. **`crossorigin`**
   - `fonts.gstatic.com` 需要 CORS，必须加这个属性
   - 否则浏览器可能拒绝加载字体

3. **`display=swap`**
   - 字体加载期间先用系统 fallback 字体显示文字
   - 避免 FOIT（Flash of Invisible Text，文字空白闪烁）
   - 加载完成后无缝切换到目标字体

### 修改的文件

- `code/json2html.py`：在 HTML 模板 `<head>` 中加入字体加载链接
- `corpus_reader.html`：重新生成

## 验证方法

修复后，在浏览器开发者工具中检查：

1. **Network 面板**：应该能看到对 `fonts.googleapis.com/css2` 和 `fonts.gstatic.com/s/noto...` 的请求
2. **Elements → Computed → font-family**：应该显示 `Noto Sans SC` 或 `Noto Serif SC`，而不是 `Microsoft YaHei` / `PingFang SC`
3. **不同设备测试**：Windows、macOS、Android、iOS 上显示一致

## 相关文档

- [font-choice.md](font-choice.md) — 字体选择的整体策略
- Google Fonts 官方文档：https://developers.google.com/fonts/docs/getting_started