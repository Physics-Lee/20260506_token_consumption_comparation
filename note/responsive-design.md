# 响应式设计：如何检测屏幕尺寸

## 核心机制：CSS 媒体查询（Media Query）

浏览器在渲染页面时，会自动获取当前设备的**视口（viewport）宽度**，CSS 媒体查询根据这个宽度应用不同的样式规则。

```css
/* 默认样式（桌面端） */
.text-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;  /* 两列 */
    gap: 2rem;
}

/* 平板/大手机：屏幕宽度 ≤ 768px */
@media (max-width: 768px) {
    .text-grid {
        grid-template-columns: 1fr;  /* 单列 */
        gap: 1rem;
    }
}
```

**不是服务器检测，不是 JavaScript，纯 CSS 机制。**

---

## 浏览器如何获取视口宽度

### 桌面端

视口宽度 = 浏览器窗口的 CSS 像素宽度。拖动窗口大小时，宽度实时变化，媒体查询即时响应。

### 移动端

手机浏览器有一个虚拟的"布局视口"（layout viewport），通常宽 980px（Safari）或 980-1024px（Chrome）。这样桌面版网页不会挤爆小屏幕。

但通过 meta viewport 标签，可以告诉浏览器：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

这行代码的含义：
- `width=device-width`：把布局视口宽度设为设备物理屏幕宽度（如 iPhone 14 是 390px）
- `initial-scale=1.0`：初始缩放比例为 1，不放大也不缩小

于是媒体查询 `max-width: 768px` 在手机上会**立即匹配**。

---

## 断点（Breakpoints）的选择

本项目用了两个断点：

| 断点 | 目标设备 | 关键改动 |
|---|---|---|
| `max-width: 1200px` | 窄桌面 / 横屏平板 | 2×2 卡片网格 → 单列 |
| `max-width: 768px` | 平板 / 大手机 | 全面缩减 padding、字号、导航栏重组 |
| `max-width: 480px` | 小手机 | 进一步压缩，主题按钮改为内联 |

这些数字不是拍脑袋定的：
- **768px**：iPad 竖屏宽度（768 CSS 像素）
- **480px**：iPhone SE / 类似小屏手机的宽度
- **1200px**：常见笔记本屏幕宽度的一半左右

---

## 与服务器端检测的区别

| | CSS 媒体查询（本项目） | 服务器端检测 |
|---|---|---|
| **检测什么** | 视口宽度（CSS 像素） | User-Agent 字符串 |
| **响应时机** | 实时（拖动窗口、旋转手机立即生效） | 页面加载时一次 |
| **准确度** | 高，反映真实显示区域 | 低，UA 字符串可被伪造 |
| **代码复杂度** | 纯 CSS，零额外代码 | 需要 UA 解析库 |
| **旋转支持** | 自动（宽度变了媒体查询重算） | 需要页面重载 |

**本项目用 CSS 媒体查询，不用服务器检测。**

---

## 为什么不用 JavaScript 检测

可以用 `window.innerWidth` 做 JS 检测，但没必要：

```javascript
// JS 能做到，但没必要
if (window.innerWidth <= 768) {
    // 改样式
}
```

CSS 媒体查询的优势：
1. **零 JS 依赖**：即使 JS 被禁用，响应式依然工作
2. **性能更好**：浏览器原生优化，不需要 JS 引擎介入
3. **实时响应**：窗口拖动、手机旋转时自动重算，不需要监听 resize 事件
4. **代码更少**：CSS 一行搞定，JS 需要事件监听 + DOM 操作

---

## 实际工作中的调试方法

### Chrome DevTools

1. F12 打开开发者工具
2. 点击左上角设备图标（Toggle device toolbar）
3. 选择预设设备（iPhone 14, iPad, Pixel 5 等）
4. 直接拖动边框测试任意宽度

### Safari

1. 开发菜单 → 进入响应式设计模式
2. 可以旋转设备、切换分辨率

### 真实设备

把 `index.html` 部署到 github.io 或本地局域网，手机浏览器打开。这是唯一可靠的测试方式（DevTools 模拟有局限）。

---

## 常见坑

### 坑 1：忘记 viewport meta 标签

没有这行代码，手机浏览器会把网页当成 980px 宽的桌面页面缩小显示，媒体查询永远不会触发。

```html
<!-- 必须要有 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 坑 2：物理像素 vs CSS 像素

iPhone 14 Pro 物理分辨率是 1179×2556，但 CSS 像素是 393×852。媒体查询用的是 **CSS 像素**，不是物理像素。

```css
/* 在 iPhone 14 Pro 上，这个会匹配 */
@media (max-width: 480px) { }

/* 这个不会匹配 */
@media (max-width: 1200px) { }
```

### 坑 3：min-width 和 max-width 搞反

```css
/* 正确：从小到大 */
/* 默认（桌面）→ 768px（平板）→ 480px（手机） */

/* 错误：max-width 越大越先生效 */
@media (max-width: 1200px) { }  /* 包含 768px 和 480px */
@media (max-width: 768px) { }   /* 包含 480px */
```

CSS 的层叠规则：后写的覆盖先写的。所以要把小屏幕规则写在后面。

---

## 参考

- [MDN: Using media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries/Using_media_queries)
- [MDN: Viewport meta tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Viewport_meta_tag)
