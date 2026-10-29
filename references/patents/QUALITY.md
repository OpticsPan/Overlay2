# 转换质量与已知问题

日期：2026-10-27 · [资料目录](README.md) · [文件校验清单](manifest.json)

<div align="justify">

　　本目录提供原件与机器提取全文。全部物理页进入处理、页码可追溯和文件哈希一致，不等于全部文字、公式、表格或图示语义已经人工校勘。44件沿用已校验的MinerU结果；新增CN120344910A使用本地MinerU 4.0.12的standard／auto模式处理26页，实际为txt模式，保留原语言和14个原图裁切。

</div>

## 实际抽查范围

| 专利／物理页 | 核对内容 | 观察与限制 |
| --- | --- | --- |
| [CN117234040A · 第5页](CN117234040A/mineru.md#p0005) | 说明书[0011]、[0015]的HDM／dHDM名称与可选限定 | 目视原PDF并对照MinerU文本，所查段落保留名称和“可以／优选”等限定；不据此认证整篇逐字无误。 |
| [DE102016205618A1 · 第2页](DE102016205618A1/mineru.md#p0002) | [0001]波长λ < 260 nm及[0002]换行处 | MinerU保留所查波长及德文变音符；原件跨行Photo-lithographie在输出中出现Photo lithographie空格，说明分词／断词处理仍需校核。 |
| [JP5809458B2 · 第2页](JP5809458B2/mineru.md#p0002) | 請求項5–8，サポート／テーブル／クランプ与下划线段 | 所查词语及权利要求顺序在MinerU原生文本模式中保留，下划线段也有对应标记；页眉J P存在额外空格。此处只核对所列范围。 |
| [US8947630B2 · 第18页](US8947630B2/mineru.md#p0018) | 双栏权利要求17–27的阅读顺序 | 目视原页并核对MinerU输出，先左栏17–20再右栏21–27；输出仍夹有边栏行号5／10／15，不能把这些数字当作权利要求正文。 |
| [US20090207511A1 · 第5页](US20090207511A1/mineru.md#p0005) | Fig. 3图像及22、21、20、10、19部件编号 | 已对照原页与MinerU坐标裁切图。Markdown保留Fig. 3图题和原图裁切，所列部件编号、线条与引线可在图片中辨认；这些编号未单独转写为可搜索正文，不能用全文搜索替代读图。裁切图附完整原PDF第5页链接。 |
| [US6961116B2 · 第24页](US6961116B2/mineru.md#p0024) | 式(45)的18 nm、后文18 nm/4=4.5 nm，以及式(46)求和下限 | 目视原PDF后核对：本次MinerU在式(45)和所查正文正确输出nm，未重现旧转换的18 mm错误。但式(46)原件求和下限为n=-N，MinerU输出n=N，漏了负号；输出还夹有边栏行号。原始机器文本保持原样，引用该公式必须回看原件并使用正确下限，不能据单位抽查通过推断整页公式准确。 |
| [CN120344910A · 第1页](CN120344910A/mineru.md#p0001) | 公开号、中文题名与原件组成 | 目视原页确认CN120344910A及所给中文题名；1页首页、2页权利要求、14页说明书、9页附图合计26页。 |
| [CN120344910A · 第2页](CN120344910A/mineru.md#p0002) | 权利要求1、2、7及页面排版 | 所查照射路径、检测路径、控制器、负载温度与平台／透镜补偿文字有对应提取。部分普通段落被识别为Markdown标题，页脚2重复为22；机器输出保留原样，不据标题级别推断权利要求层级。仅核对所列范围。 |
| [CN120344910A · 第26页](CN120344910A/mineru.md#p0026) | 图8的810–840步骤与连接箭头 | 已对照原页及裁切图，图中四个步骤、编号与箭头可辨认；Markdown保留图8图题及原页链接。图中文字未单独转写为可搜索正文，页脚26重复为2626。 |

## 使用提示

- 关键引文、技术参数、权利要求与公式以同目录原始PDF为核对依据；物理页从封面计1。
- 原始PDF字节保持不变，Markdown保留机器正文。为适配本仓库，只调整资料页眉说明和原件／质量链接；既有图像字节保持不变。
- 已知US6961116B2第24页式(46)求和下限应为`n=-N`，机器输出漏负号；该全文入口也有提示。
- 图片文件用于保留图纸与流程图；裁切不能代替完整原页上下文，图内文字不保证可通过Markdown全文搜索检索。
- 未进行45份原件的全文逐字校勘，不提供机器识别准确率承诺。

## R2研究中新增的原页核对记录（2026-10-28）

以下为人工校核说明，机器全文及原件保持不变。各条的原页、核验方式与详细语境保存在R2逐篇记录中；不得将原文内部差异统一当作OCR错误修改。

| 资料与位置 | 类型与处理要求 | 详细记录 |
| --- | --- | --- |
| CN120344910A p12，[0086]—[0087] | OCR温度和再现性数字有误，如原页约0.6 K不应引作10.6 K；引用以原页为准 | [热管理记录](../../reports/advanced-overlay-management/r2/review/thermal.md) |
| CN120344910A p13／WO2024132326A1 p14 | 形变参数命名在原文不同段落间有差异；不静默统一成新的物理定义 | [热管理记录](../../reports/advanced-overlay-management/r2/review/thermal.md) |
| US8184265B2 p12、p15；US12663725B2 p26 | 表1并非所有场尺寸都更优；更正证书与授权权利要求须分别核对，不能用同申请A1或示例clauses代替正式权利要求 | [热管理记录](../../reports/advanced-overlay-management/r2/review/thermal.md) |
| US20240184221A1 p12；US10884345B2 p15；US11703772B2 Fig.15 | 前者机器权利要求重复steps B)；后两者原图／原文编号有不一致，按功能及上下文解释，不改原图 | [量测记录](../../reports/advanced-overlay-management/r2/review/measurement.md) |
| US8208120B2 p22；US8269949B2 p8 | 前者机器权利要求1有原页不存在的重复片段；后者原文increase与示例刚度及权利要求13相冲突，属于原文瑕疵 | [机械记录](../../reports/advanced-overlay-management/r2/review/mechanics.md) |
| CN117234040A p12 [0109]／US20230400772A1 p20 [0111] | 对后续测量／调整能否省略存在原件表达差异，不能以同源关系抹平 | [机械记录](../../reports/advanced-overlay-management/r2/review/mechanics.md) |
| US8947630B2 p19；US6961116B2 p29—32 | 原件包含正式更正／勘误，引用权利要求时须一并阅读 | [机械记录](../../reports/advanced-overlay-management/r2/review/mechanics.md) · [执行记录](../../reports/advanced-overlay-management/r2/review/execution.md) |
| US20130188160A1 p3／p18；US20230077090A1 p21—22 | 仿真单元图文编号70/72不同；后者100 pm与上下文ppm存在单位疑点，且小于1 nm仅为排除物镜其他误差及制造误差的设计例 | [光学记录](../../reports/advanced-overlay-management/r2/review/optics.md) |
| WO2017108453A1 Fig.7及[0094]—[0096]；US11886124B2 p36 | 前者图文信号编号有歧义；后者存在132nm/16.5nm相关单位疑点，本报告不据此引用数值 | [控制记录](../../reports/advanced-overlay-management/r2/review/control.md) |

上述阅读不等于45份PDF全文逐字校勘；仿真、示意图、设计残差、部件指标与整机实测仍须分开。R2保留了US7423725B2仿真性质、US9772561B2不同测试组不能混用等证据边界，详见相应阅读记录。

## R2第8.2节修订中的图片校核（2026-10-29）

US20210096472A1的Fig. 2位于原PDF物理第3页。既有MinerU裁切`figures/p0003-0003.png`右缘使编号220的末位不完整；回看原PDF可见完整220。原PDF、机器全文及既有裁切保持原字节，R2[第8.2节](../../reports/advanced-overlay-management/r2/report.md#section-8-2)改用从原PDF整页渲染的PNG，未重绘或补写文字；渲染命令、来源与产物哈希见[R2来源清单](../../reports/advanced-overlay-management/r2/sources.json)。

## R2物镜专题修订中的图片校核（2026-10-29）

US8659745B2的Fig. 4位于原PDF物理第6页。既有MinerU裁切`figures/p0006-0006.png`左缘未完整保留Fig. 4图号及装置编号1；原PDF中两者完整。原PDF、机器全文及既有裁切保持原字节，R2[第6.6节](../../reports/advanced-overlay-management/r2/report.md#objective-thermal)采用完整原页渲染图，不重绘或补写原图标注；命令及哈希见[R2来源清单](../../reports/advanced-overlay-management/r2/sources.json)。


## R3全文复核补记（2026-10-29）

本节仅补充人工校核说明，原PDF、MinerU及原裁切保持原字节。继承的R2阅读记录中的解释性错误与原件／转写差异分开处理；前者由R3复核记录订正，不改写历史稿。

| 资料与位置 | 核对结果与引用边界 | 记录 |
| --- | --- | --- |
| DE102016205618A1 p18 [0148]、p21表235a | 晶圆位移正文+0.433 µm与表中−0.433 µm符号不一致，DEZ／DCZ标识也不一致，均存在于原PDF；不裁决正确命令或摘录为控制向量 | [R3光学复核](../../reports/advanced-overlay-management/r3/review/recheck-optics.md) |
| US20250021017A1 p26权利要求7、11 | MinerU漏失预定温度限定的引导文字，权利要求11在sub-截断；原件完整至“substrates until a convergence of at least 90% is reached” | [R3热管理复核](../../reports/advanced-overlay-management/r3/review/recheck-thermal.md) |
| US12663725B2 p26权利要求13 | “to a zero to a zero dose”重复存在于原件，不是转写新增；须结合上下文且保留原件身份 | [R3热管理复核](../../reports/advanced-overlay-management/r3/review/recheck-thermal.md) |
| US11175593B2 p27表1前后 | 编程套刻例中−30 nm与表后30 nm符号不一致，原PDF即如此；R3不从该例提取数值收益 | [R3量测复核](../../reports/advanced-overlay-management/r3/review/recheck-measurement.md) |
| US7423725B2 Fig. 8—10，p5 | 既有裁切上缘未完整保留图号；R3采用完整原PDF页渲染图，未重绘或修改原件 | [R3来源清单](../../reports/advanced-overlay-management/r3/sources.json) |
