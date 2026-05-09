# 为什么抛弃 json2html.py

## 结论

删除 `json2html.py` 和 `corpus_reader.html`，只保留 `build_index.py` → `index.html` 一条线。

## 理由

1. **build_index.py 是 json2html.py 的超集。** 主题切换、四语言平行阅读、字符数统计——json2html 有的 build_index 全有，外加：分词器切换、实时 token 计算、预计算开源模型 token 数、页脚友链。没有 json2html 能做而 build_index 不能做的事。

2. **不想看 token 的人不受影响。** 分词器下拉框多看一眼不会怎样。忽略它，index.html 就是 corpus_reader.html。

3. **维护两套 HTML 模板必然漂移。** 同样的 CSS 变量、同样的 class 名、同样的三态主题 JS，分两个文件写两遍。改一边的 padding 忘改另一边，或者这边加了 copy 按钮那边没加——这种事情迟早发生。

4. **多条线增加认知负担。** 新来的人看 README 要理解两条流水线的区别、两个 HTML 产物的关系。一条线，一个脚本，一个产物，零歧义。
