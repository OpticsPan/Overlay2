# Overlay2

Overlay2 项目仓库。当前处于管理基础初始化阶段，尚未接入业务代码或确认产品需求。

## 当前状态

- 发布状态：未发布；尚无产品版本号。
- 管理基础建立日期：2026-10-27（Asia/Shanghai）。
- 项目用途、技术栈、运行环境和首个版本范围：待确认。
- 本仓库当前为公开仓库；提交前确认代码、数据和文档适合公开。

## 管理入口

| 内容 | 入口 |
| --- | --- |
| 开发、分支、提交与评审约定 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 代理工作约定 | [AGENTS.md](AGENTS.md) |
| 变更记录 | [CHANGELOG.md](CHANGELOG.md) |
| 需求、验收与待确认事项 | [需求台账](docs/REQUIREMENTS.md) |
| 版本策略与发布清单 | [发布管理](docs/RELEASE.md) |
| 管理决策记录 | [决策记录](docs/DECISIONS.md) |
| 新建需求或缺陷 | [Issues](https://github.com/OpticsPan/Overlay2/issues) |
| 代码和文档评审 | [Pull requests](https://github.com/OpticsPan/Overlay2/pulls) |

## 日常流程

1. 用 Issue 或需求台账记录目标、范围、验收标准及优先级。
2. 从最新 main 创建短期工作分支，完成修改及适当验证。
3. 在 PR 中关联需求、说明变更和验证证据，并更新 Unreleased。
4. 合并后更新需求状态；发布时整理版本记录、标签和 Release。

小型文档修正可直接在 PR 中说明，无需额外创建 Issue。完整规则见上方文档。

## 首次接入代码

接入时补充项目简介、目录结构、安装/运行/测试命令、依赖及许可证选择；以真实运行结果为依据。当前没有可运行程序、测试命令或自动化 CI，不代表验证已经通过。
