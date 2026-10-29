# Overlay2

Overlay2 用于整机套刻调研资料的保存和持续维护。当前已收录45件专利的原始PDF、MinerU全文Markdown及其图像资料，共1,114个物理页。研究报告和业务程序的后续范围由具体任务确定。

## 研究报告

- [先进光刻机套刻管理架构 · R3（Markdown，当前稿）](reports/advanced-overlay-management/r3/report.md)
- [R2历史Markdown](reports/advanced-overlay-management/r2/report.md)
- [R1历史Markdown](reports/advanced-overlay-management/report.md) · [R1历史PDF](reports/advanced-overlay-management/report.pdf)（仅对应R1）
- [R3撰写逻辑v0.2（组织逻辑已批准）](reports/advanced-overlay-management/planning/r3-logic-review.md)
- [报告维护与修订规范](reports/README.md)

## 资料入口

| 内容 | 入口 |
| --- | --- |
| 45件专利原件与全文 | [专利资料目录](references/patents/README.md) |
| 公开号、页数、文件SHA-256 | [机器清单](references/patents/manifest.json) |
| 机器转换质量与已知识别问题 | [质量记录](references/patents/QUALITY.md) |
| 新资料入库、修订与引用规范 | [资料维护规则](docs/SOURCES.md) |
| 当前进度、验证和交接 | [维护状态](docs/STATUS.md) |

## 当前状态

- 发布状态：未发布；尚无产品版本号。
- 管理基础建立日期：2026-10-27（Asia/Shanghai）。
- 当前用途：整机套刻调研资料库；已完成的资料入库见[REQ-002](docs/REQUIREMENTS.md#req-002)。
- Python仅用于仓库校验；未来业务程序的技术栈和首个产品版本范围仍待确认。
- 本仓库当前为公开仓库；提交前确认代码、数据和文档适合公开。
- 自动检查：[Repository checks](https://github.com/OpticsPan/Overlay2/actions/workflows/repository-checks.yml)。实际通过与否以对应提交的工作流结果为准。
- main分支保护状态及管理检查边界见[维护状态](docs/STATUS.md#platform-state)。

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

## 本地验收

需要Python 3.12及以上版本。在独立环境内安装校验依赖后执行：

```bash
python -m pip install -r requirements-validation.txt
python -m unittest discover -s tests -v
python tools/validate_repository.py --base <变更前的提交SHA>
```

校验原件与派生文件哈希、实际PDF页数、逐页锚点、仓库内链接及原件历史保护。Windows本机的环境、缓存和输出按用户偏好放在D盘；脚本不依赖特定盘符。自动校验不判断OCR语义、专利技术结论或法律状态。

首次接入业务代码时，再按实际代码补充运行方式、依赖和功能验证，不因资料入库或管理工具产生产品版本号。
