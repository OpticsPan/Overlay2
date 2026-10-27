# 仓库维护状态

更新：2026-10-27（Asia/Shanghai） · [需求台账](REQUIREMENTS.md) · [变更日志](../CHANGELOG.md)

## 当前基线与资料

- 本轮开始基线：`f4ca7fd71199a27c47b45d94bfe3609bc7bcf18e`。
- [资料入库PR #1](https://github.com/OpticsPan/Overlay2/pull/1)已合并并回读main确认：45份原始PDF、45份MinerU全文、1,114个物理页、624个图像裁切。
- 既有717个资料文件本轮保持原字节；本轮完善管理文档与校验工具。
- 当前仍为未发布状态；不因资料入库或Python校验工具创建产品版本。

## 验证与交接

- 本地18项测试已通过，覆盖原件改写、PDF页数、重复／缺失锚点、缺图、清单错误、越界路径、坏PDF、文档锚点、CLI退出码和Git基线保护。Windows不能创建符号链接时，该项只模拟操作系统路径解析；Linux CI将使用实际符号链接。
- 全45件资料的文件哈希、实际页数和页锚点检查通过，既有资料目录相对基线无变化。命令与结果见[本地验收记录](validation/2026-10-27-management.json)。
- GitHub Actions远端验证待执行；未执行的检查不记为通过。
- 后续任务先读取本文件、需求台账和资料规则，核对远端最新main，再从短期分支修改；合并前检查对应PR的Actions结果。

<a id="platform-state"></a>

## GitHub平台实际状态

| 项目 | 已核对状态 | 依据与边界 |
| --- | --- | --- |
| 默认分支 | main | 仓库元数据 |
| 仓库可见性 | 公开 | 本轮没有修改可见性或访问权限 |
| main分支保护 | 未启用 | 2026-10-27读取branches/main得到protected=false；CI文件不等于平台强制保护 |
| 合并后自动删分支 | 未启用 | 仓库元数据delete_branch_on_merge=false；本轮没有修改该设置 |
| 自动检查 | 本轮新增，待实际运行验收 | [Repository checks](https://github.com/OpticsPan/Overlay2/actions/workflows/repository-checks.yml) |
| 许可证、产品Release | 未设置／未发布 | 不代用户选择许可证或创建产品版本 |

如需将PR检查变成平台强制条件，可另行明确main保护策略及单人维护者的合并方式；当前协作流程要求先通过检查，但不宣称已经强制执行。
