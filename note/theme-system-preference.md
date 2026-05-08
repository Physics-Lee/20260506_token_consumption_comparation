# 跟随系统主题（System Preference Theme）实现笔记

## 原理

利用 CSS 自定义属性（CSS Variables）+ `prefers-color-scheme` Media Query + JavaScript 三者配合，实现"浅色 / 深色 / 跟随系统"三态切换。

---

## 1. CSS 架构

### 1.1 定义两套颜色变量

```css
/* 默认（浅色） */
:root {
  --bg-body: #f8f9fa;
  --bg-card: #ffffff;
  --text-primary: #374151;
  --text-secondary: #6b7280;
  --accent: #2563eb;
  --border: #e5e7eb;
}

/* 深色模式覆盖 */
[data-theme="dark"] {
  --bg-body: #0d1117;
  --bg-card: #161b22;
  --text-primary: #c9d1d9;
  --text-secondary: #8b949e;
  --accent: #58a6ff;
  --border: #30363d;
}
```

所有元素的颜色都使用这些变量，而不是硬编码。切换主题时，只需要改变根元素的 `data-theme` 属性，整个页面颜色自动更新。

### 1.2 关键设计

- **默认 `:root`** = 浅色主题
- **`[data-theme="dark"]`** = 强制深色
- **没有 `data-theme` 时** = 跟随系统（由 JS 通过 `prefers-color-scheme` 决定实际生效哪套颜色）

---

## 2. JavaScript 控制逻辑

### 2.1 读取系统偏好

```js
const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

function getEffectiveTheme() {
  const attr = document.documentElement.getAttribute('data-theme');
  // 如果用户明确指定了 light/dark，就按用户的选择
  if (attr === 'light' || attr === 'dark') return attr;
  // 否则，读取系统偏好
  return mediaQuery.matches ? 'dark' : 'light';
}
```

### 2.2 三态切换

```js
function applyTheme(mode) {
  if (mode === 'system') {
    // 移除 data-theme，让页面回到 :root 默认状态
    // 实际颜色由系统偏好决定（因为 :root 是浅色，但系统设为深色时
    // 我们通过 JS 监听来更新 UI，而不是用 CSS media query）
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', mode);
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const modes = ['light', 'dark', 'system'];
  const idx = modes.indexOf(current || 'system');
  const next = modes[(idx + 1) % modes.length];
  applyTheme(next);
}
```

### 2.3 监听系统变化

```js
mediaQuery.addEventListener('change', () => {
  // 只有在"跟随系统"模式下才响应系统变化
  if (!document.documentElement.hasAttribute('data-theme')) {
    updateThemeBtn(); // 更新按钮提示
  }
});
```

当用户切换 OS 主题（如 macOS 自动日夜切换、Windows 深色模式），浏览器会触发 `change` 事件。如果当前处于"跟随系统"模式，页面会自动适配。

---

## 3. 为什么不用 CSS `@media (prefers-color-scheme)`？

可以这样做，但复杂：

```css
@media (prefers-color-scheme: dark) {
  :root { --bg-body: #0d1117; ... }
}
```

**问题**：一旦用了 `@media`，CSS 会强制跟随系统，用户无法手动覆盖。要实现"三态"（浅色/深色/跟随），必须在 CSS 层面留出"手动覆盖"的口子。

**我们的方案**：
- CSS 只定义 `:root`（浅色）和 `[data-theme="dark"]`（深色）
- "跟随系统"时，JS 检测系统偏好，**动态设置/移除 `data-theme`**
- 用户手动选择时，**JS 接管控制权**，系统偏好不再生效

这样实现最干净，不需要在 CSS 里写 `@media` 规则。

---

## 4. 状态机

```
┌─────────────────────────────────────────┐
│  页面加载                                │
│  默认: applyTheme('system')             │
│  → 无 data-theme，读取系统偏好           │
└─────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────┐
        │   用户点击按钮     │
        └───────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    ☀️ 浅色     🌙 深色      💻 跟随系统
    data-theme   data-theme   移除 data-theme
    ="light"    ="dark"      读取 prefers-color-scheme
```

---

## 5. 持久化（可选增强）

如果需要记住用户选择，可以加一行：

```js
function applyTheme(mode) {
  localStorage.setItem('theme', mode);
  // ... 现有逻辑
}

// 页面加载时恢复
const saved = localStorage.getItem('theme') || 'system';
applyTheme(saved);
```

当前实现未加持久化，每次刷新回到"跟随系统"。

---

## 6. 浏览器兼容性

| 特性 | 兼容性 |
|------|--------|
| CSS Custom Properties | 所有现代浏览器 |
| `prefers-color-scheme` | Chrome 76+, Firefox 67+, Safari 12.1+, Edge 79+ |
| `matchMedia().addEventListener` | 所有现代浏览器 |

IE 不支持，但本项目不需要支持 IE。

---

## 7. 文件位置

- HTML 文件：`corpus_reader.html`
- 主题切换按钮：`<button class="theme-toggle">`
- JS 逻辑：文件末尾 `<script>` 标签内
