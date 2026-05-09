# 字体选择说明

## 当前字体栈

### 全局 UI
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", "Noto Serif SC", serif;
```

### 正文内容（卡片内）
```css
font-family: "Noto Sans SC", "Noto Serif SC", serif;
```

## 选择理由

### 1. 系统字体优先（英文/数字）
- `-apple-system`、`BlinkMacSystemFont`：macOS / iOS 原生字体，在不同设备上自动匹配 San Francisco 或 PingFang
- `"Segoe UI"`：Windows 默认无衬线字体，与系统界面风格一致
- `Roboto`：Android / Material Design 标准字体

**为什么**：英文和数字用系统字体渲染效果最好，无需额外加载，首屏更快。

### 2. 中文回退：Noto Sans SC + Noto Serif SC
- **Noto Sans SC**：思源黑体，Google Fonts 提供，支持简体中文、繁体中文、日文、韩文（CJK）统一表意文字
- **Noto Serif SC**：思源宋体，同一字族的有衬线版本，字形更古典，适合长文阅读

**为什么**：
- 免费、开源（SIL Open Font License）
- 通过 Google Fonts CDN 加载，全球访问速度快
- CJK 字符覆盖全面（Unicode 基本区和扩展区 A/B）
- 包含文言文常用字（如「之」「乎」「者」「也」的繁体/异体字形）

### 3. 为什么没有用专用古籍字体？
本项目语料包含现代汉语、英语、西班牙语，以及文言文。专用古籍字体（如「文征明体」「方正清刻本悦宋」）虽然对古典字形还原更好，但：
- 多为商业字体，授权复杂
- 西文字形通常不配套，混排效果差
- 文件体积大（一个中文字体通常 5–20MB），影响加载速度

`Noto Serif SC` 的宋体风格已经足够古典，且西文部分（衬线）与之协调，是性价比最高的选择。

### 4. 为什么不全部用无衬线？
长文本（尤其是文言文）用衬线字体（宋体/明朝体）更易读：
- 笔画粗细对比明显，帮助眼睛追踪行距
- 古典文本与传统印刷字形气质更匹配
- 现代汉语、英语、西班牙语在宋体下的表现也优于预期（Noto Serif SC 的西文部分经过专门设计）

UI 元素（导航栏、按钮、标签）仍使用无衬线，保证界面现代感和清晰度。

## 加载方式

### 当前实现

通过 Google Fonts CDN 在 HTML `<head>` 中引入：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
```

- `preconnect`：提前与字体服务器建立 TCP/TLS 连接，减少加载延迟约 100–300ms
- `display=swap`：字体加载期间先用系统 fallback 字体渲染，避免 FOIT（Flash of Invisible Text）

### 曾遇到的 bug

早期版本只在 CSS 中声明了 `font-family: "Noto Sans SC", "Noto Serif SC", serif;`，但**没有在 HTML 中加载字体文件**。导致：
- 本地开发环境（已安装 Noto 字体）显示正常
- 部署到 github.io 后，大部分用户系统没有这些字体，回退到微软雅黑/苹方，视觉效果不一致

**教训**：声明 `font-family` 不等于加载字体，必须通过 `@font-face` 或 CDN 引入实际字体文件。

## 未来可能调整

- 如需更严格的古籍排版（竖排、从右到左、异体字），可引入 `Source Han Serif` 的特定子集
- 如需优化屏幕阅读体验，可考虑加载 `Noto Sans SC` 的 Variable Font 版本，减少文件体积
- 如需支持更多罕见汉字（扩展区 C/D/E），需评估字体子集是否覆盖
