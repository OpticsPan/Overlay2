# 研究报告维护规范

本目录保存用户要求交付和持续维护的正式研究报告。报告Markdown、交付PDF、来源清单、交付记录及排版模板是版本管理对象；中间HTML、公式SVG、缓存和日志放入忽略的`work/`。这是对一般生成物不入库规则的特定报告交付例外，不扩大到任意临时输出。

## 当前报告

- [先进光刻机套刻管理架构 · R1 Markdown](advanced-overlay-management/report.md)
- [对应PDF](advanced-overlay-management/report.pdf)
- [来源与图像清单](advanced-overlay-management/sources.json)
- [交付与验证记录](advanced-overlay-management/delivery.json)

R1是报告修订标识，不是产品版本。待用户审阅不写成已验收。

## 继承与修订

1. 未明确要求从零撰写时，先复制适用旧报告的Markdown。新主题使用新目录；同一报告修订通过Git保存旧版。若无适用旧报告，记录新建理由。
2. 记录父报告路径、父报告提交或哈希、资料基线与本次范围。复制不等于重新验证。
3. 重新检查题名、摘要、适用对象、图表编号、相对引用路径、权利要求版本、数字、公式、结论与外推标记。删除不适用于新主题的旧内容。
4. 每项关键判断定位至公开号、原PDF物理页、图号及段落/权利要求；关键公式与权利要求回看原件。来源PDF与机器全文保持原字节。
5. 同步来源清单、REQ、CHANGELOG、状态和交付记录。仅在用户要求PDF时生成/更新PDF；未更新时明确PDF过期，不声称与新MD一致。
6. 执行现有仓库测试和基线校验；检查PDF文字、图片、表格、公式与分页，再进行内容审阅。未运行的远端CI不得标为通过。

## PDF生成

构建脚本为[build_report.py](build_report.py)，样式为[report.css](templates/report.css)。当前脚本面向本报告，其他报告可据此调整输入路径。使用Pandoc生成HTML、Matplotlib将数学公式排版为SVG、WeasyPrint导出PDF；需要Noto Serif/Sans CJK SC中文字体以及WeasyPrint系统字体/排版依赖。

本次环境：系统Python提供Matplotlib，独立工具环境`/workspace/report-tools`提供WeasyPrint 68.1。在仓库根目录执行：

```bash
python3 reports/build_report.py --weasyprint /workspace/report-tools/bin/weasyprint
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/validate_repository.py --base dd7ee03acec72b6db251f59b2bcf798aa1ff2aed
```

上面的SHA只适用于R1任务；后续用各自真实变更前基线。工具路径是本次环境示例，不要求其他机器采用相同目录。构建不下载专利、不修改原始资料。公式SVG只用于排版，Markdown中的公式是文字源；数学图形需目视核查。来源图片引用仓库现有文件，单独分发Markdown时需一并提供这些相对路径的图像。
