# 仓库维护状态

更新：2026-10-29（Asia/Shanghai） · [需求台账](REQUIREMENTS.md) · [变更日志](../CHANGELOG.md)

## 待审阅：R3撰写逻辑临时参考

- 2026-10-29按用户要求，将[L0—L3脉络与章节安排](../reports/advanced-overlay-management/planning/r3-logic-review.md)保存为审阅稿v0.1，包含L0整机关系、L1章节导航、章内L2／L3模板和三对象热管理结构。
- 用户审阅通过后才开始R3正文；当前保存不表示结构已获批准。R2及已确认的默认骨架保持原样，当前报告仍为R2。
- 本轮基线为`e42db35592ad78ff7d7311f3138e60c5fde8cb7e`；检查范围与结果见[临时稿验证记录](validation/2026-10-29-r3-logic-review.json)。

## 当前报告：R2（初稿2026-10-28；最近修订2026-10-29）

- [R2网页Markdown](../reports/advanced-overlay-management/r2/report.md)已从零撰写，未以R1为基底；按L0—L4组织，正文展开L0—L3，L4保留后续专题接口，待用户内容审阅。
- 全部45件MinerU文本分组通读，关键说明、权利要求和原图回看原PDF；[六组阅读记录](../reports/advanced-overlay-management/r2/report.md#references)保存实际范围与边界。通读不等于1,114页逐字校勘。
- 资料与任务基线：`edd7a4e13fdddc994befcbc22147a7ac59013385`。来源、产物哈希及验证范围见[R2交付记录](../reports/advanced-overlay-management/r2/delivery.json)。原PDF、机器全文和原图不改；新发现的提取／原文差异已补入QUALITY。
- 2026-10-29根据用户阅读反馈，基于R2提交`b0168c3`重写[8.2节](../reports/advanced-overlay-management/r2/report.md#section-8-2)：先交代问题背景与空间层级，再结合原Fig. 2、Fig. 3说明两条解决策略及L3能力；其他章节正文保持原样，L4仍仅为接口。来源及交付记录同步更新，待用户内容审阅。
- 2026-10-29根据用户确认的复核方向，基于`c511be6`重绘[图1](../reports/advanced-overlay-management/r2/report.md#architecture)，分开参考／模型支撑、源头措施和两类反馈；同步图注、表2和可编辑图源，并检查文字边界、连线及网页显示尺寸。
- 2026-10-29基于`85a3b87`补充[6.6节物镜专题](../reports/advanced-overlay-management/r2/report.md#objective-thermal)，串联热效应来源、校准预测、补偿执行、量测解释和前馈更新；明确校正器设计／升级与生产运行的区别，补入原图和T10接口。本次定向复核相关原页，未重复宣称通读全部45件；待用户内容审阅。
- 当前默认：报告保存并推送GitHub，维护版本；无特殊要求为适合网页阅读的Markdown。流程框图必须美观且文字完整；规范、骨架及代理约定已同步。
- 本次未生成R2 PDF。R1 Markdown/PDF作为历史版本保留，其PDF不对应R2；后续PDF仍须落实中文学术排版、正文两端对齐和首行2em缩进，并重新核对标准版本及实际版式。
- R1仅解读六件核心专利；R2是重新研究和组织后的独立稿。两稿均未作产品发布或商业机型性能认证。

## 资料入库与管理建设历史

- 本轮开始基线：`f4ca7fd71199a27c47b45d94bfe3609bc7bcf18e`。
- [资料入库PR #1](https://github.com/OpticsPan/Overlay2/pull/1)已合并并回读main确认：45份原始PDF、45份MinerU全文、1,114个物理页、624个图像裁切。
- 既有717个资料文件本轮保持原字节；本轮完善管理文档与校验工具。
- 当前仍为未发布状态；不因资料入库或Python校验工具创建产品版本。

## 验证与交接

- 本地18项测试已通过，覆盖原件改写、PDF页数、重复／缺失锚点、缺图、清单错误、越界路径、坏PDF、文档锚点、CLI退出码和Git基线保护。Windows不能创建符号链接时，该项只模拟操作系统路径解析；Linux CI已使用实际符号链接并通过。
- 全45件资料的文件哈希、实际页数和页锚点检查通过，既有资料目录相对基线无变化。命令与结果见[本地验收记录](validation/2026-10-27-management.json)。
- [管理PR #2](https://github.com/OpticsPan/Overlay2/pull/2)已合并；[PR检查](https://github.com/OpticsPan/Overlay2/actions/runs/40527885523)与[main检查](https://github.com/OpticsPan/Overlay2/actions/runs/40528504056)实际成功。已回读main提交`1aae1b57039c05d7415b5fa2ecc42d01eae6aec0`，内容树与已核验分支一致。本记录针对该已验证快照，后续提交结果以对应Actions为准。
- 后续任务先读取本文件、需求台账和资料规则，核对远端最新main，再从短期分支修改；合并前检查对应PR的Actions结果。

<a id="platform-state"></a>

## GitHub平台实际状态

| 项目 | 已核对状态 | 依据与边界 |
| --- | --- | --- |
| 默认分支 | main | 仓库元数据 |
| 仓库可见性 | 公开 | 本轮没有修改可见性或访问权限 |
| main分支保护 | 未启用 | 2026-10-27读取branches/main得到protected=false；CI文件不等于平台强制保护 |
| 合并后自动删分支 | 未启用 | 仓库元数据delete_branch_on_merge=false；本轮没有修改该设置 |
| 自动检查 | 已运行：PR及main均成功 | [Repository checks](https://github.com/OpticsPan/Overlay2/actions/workflows/repository-checks.yml) |
| 许可证、产品Release | 未设置／未发布 | 不代用户选择许可证或创建产品版本 |

如需将PR检查变成平台强制条件，可另行明确main保护策略及单人维护者的合并方式；当前协作流程要求先通过检查，但不宣称已经强制执行。
