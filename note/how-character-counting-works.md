# 如何统计字符数

## 统计位置

字符数统计在 `code/json2html.py` 的第48行：

```python
char_count = len(text['content'])
```

## 统计逻辑

非常简单——直接计算 `content` 字符串的 **Python 字符长度**。

```python
text['content']  # 这是一个 Python str
len(text['content'])  # 返回 Unicode 字符数量
```

## 什么是 "字符"

在 Python 3 中，`len()` 对字符串返回的是 **Unicode code points 数量**:

| 内容 | len() 结果 | 说明 |
|---|---|---|
| `"hello"` | 5 | 5 个 ASCII 字母 |
| `"你好"` | 2 | 2 个汉字 |
| `"こんにちは"` | 5 | 5 个假名 |
| `"🙂"` | 1 | 1 个 emoji |
| `"\n"` | 1 | 换行符也算 1 个字符 |
| `"  "` | 2 | 空格也算字符 |

## 实际应用

### 在 Comparison Table 中显示
```python
rows.append(f'''
    <tr>
        <td><span class="dot" style="background:{cfg['dot']}"></span>{cfg['label']}</td>
        <td>{role_text}</td>
        <td>{text['title']}</td>
        <td>{len(text['content']):,}</td>  <!-- 这里统计字符数 -->
    </tr>
''')
```

### 在 Card Footer 中显示
```python
cards.append(f'''
    <div class="text-card {cfg['css']}">
        ...
        <div class="card-footer">{char_count:,} 字符</div>  <!-- 这里 -->
    </div>
''')
```

## 为什么不用字节数

| 指标 | 适用场景 | 本仓库选择 |
|---|---|---|
| **字符数** (`len(str)`) | 人类阅读体验、排版长度 | 采用 |
| **字节数** (`len(str.encode('utf-8'))`) | 存储空间、网络传输 | 未采用 |

理由：
- 本仓库目的是 **token 消耗分析**，字符数是直观的文本长度指标
- 一个汉字 = 1 字符，一个英文字母 = 1 字符，便于跨语言比较
- 如果使用字节数，英文 1 字节/字符 vs 中文 3 字节/字符，会扭曲对比

## 格式美化

使用 Python 的 `:,` 格式符添加千分位分隔符：

```python
f"{len(text['content']):,}"
# 1742  -> "1,742"
# 4288  -> "4,288"
```

## 验证

可以在 Python 中直接验证：

```python
text = "荆轲捧着装有樊於期头颅的匣子"
print(len(text))  # 输出: 14
```

对应 HTML 中显示为：`14 字符`
