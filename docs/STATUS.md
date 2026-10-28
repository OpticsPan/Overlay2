# 仓库维护状态

更新：2026-10-28（Asia/Shanghai） · [需求台账](REQUIREMENTS.md) · [变更日志](../CHANGELOG.md)

## 报告结构与排版规范（2026-10-28）

- 本次框图检查：最终SVG经CairoSVG栅格化至560px宽目视核查，六个节点和两条反馈标签完整、无重叠；18项单元测试及以`b264152ba98220ecd24f6365606437fbb53aa63f`为基线的资料/链接校验通过。未更新PDF，故本次未执行最终报告PDF版式检查。
- L0—L4骨架图改为自动尺寸、显式分行的SVG，字形固化以避免查看端字体替换导致裁切；保留可编辑源文件，并补充逐节点检查要求。此次仅修订骨架图和规范，既有报告PDF未更新。

- REQ-006已确认：[L0—L4结构](../reports/STRUCTURE.md)为后续报告默认骨架，已同步报告维护规范及代理约定。本次仅将骨架入库；全部45件专利的通读、归纳和报告修订尚待后续执行。

- REQ-005已确认并记录到[报告维护规范](../reports/README.md)：后续PDF参考中文学术论文国标格式，正文两端对齐、首行缩进两个汉字宽度。
- 本次仅记录规范；现有PDF未重排，CSS的首行缩进需在下一次PDF任务落实并验证。

## 报告工作进展（2026-10-28）

- REQ-004新增[《先进光刻机套刻管理架构》](../reports/advanced-overlay-management/report.md)R1及PDF，待内容审阅。
- 报告任务基线：`dd7ee03acec72b6db251f59b2bcf798aa1ff2aed`；原报告分支`docs/overlay-management-report`已合并并删除。
- 六件核心专利、八幅原图；原始资料保持字节。检查结果见[交付记录](../reports/advanced-overlay-management/delivery.json)。
- 报告已随`f7cb1a0a8812ce4b7964e5a647e2c2e2b98927c8`纳入main；[Repository checks #5](https://github.com/OpticsPan/Overlay2/actions/runs/40615082936)已成功（通过Actions网页核对）。报告内容仍待审阅，未作产品发布。

## 当前基线与资料

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
