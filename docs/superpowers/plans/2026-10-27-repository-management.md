# Overlay2资料库管理实施计划

> **For agentic workers:** 使用 superpowers:executing-plans 在当前任务内执行；不启动子代理。各步以实际检查结果验收。

**Goal:** 把已入库的专利资料纳入可追溯、可重复核验的仓库维护流程。

**Architecture:** 保留现有main／短期分支／PR流程。以资料manifest作为原件和转换文件清单，在本地与GitHub Actions运行同一校验器；管理文档负责需求、版本、变更和实际状态。

**Tech Stack:** Python 3.12+、标准库unittest、pypdfium2 5.14.0、GitHub Actions；这些仅为管理校验依赖，不确定未来业务技术栈。

**Spec:** 用户要求“做好@github/overlay2仓库的管理”，承接[现有协作约定](../../../AGENTS.md)和[管理决策](../../DECISIONS.md)。以下具体组织方式为助手实施选择。

## Global Constraints

- 原件、既有Markdown和图片保持原字节；本轮只补管理与校验。
- 正式资料通过GitHub交付，本机工作数据位于D盘。
- 后续专利转换使用MinerU；报告PDF只在用户明确要求时生成。
- 不创建产品版本、Release、许可证，不改仓库可见性或访问权限。
- 不把页覆盖、哈希或CI通过称为全文语义准确；如实记录当前main分支保护状态。

## Review Focus

- 清单与实际文件同时被改写：以Git基线额外保护已存在原件。
- 页数看似相同但锚点重复或错序：检查完整有序序列。
- 目录穿越、绝对路径和失效图像链接：只接受仓库内可解析目标。
- 原件存在但无法解析、空清单或非预期字段类型：报告明确错误并返回非零退出码。
- 新增合法专利：由清单推导数量，不把45件或1,114页永久写死在校验器。

## Task 1：资料和文档校验

**Files:** `tools/validate_repository.py`、`tests/test_validate_repository.py`、`requirements-validation.txt`。

**Interfaces:** `validate(root: Path, base: str | None = None) -> dict`；CLI `python tools/validate_repository.py --base <SHA>`，错误时退出1，成功退出0。

- [x] 编写真实小PDF fixture及损坏／缺页／重复锚点／哈希／图片／越界／断链／基线原件修改测试。
- [x] 运行测试确认缺失功能导致失败，再实现可移植校验器；不依赖本机绝对路径或旧Overlay仓库。
- [x] 18项测试及全45件真实资料校验通过；确认原件、MD与图片相对基线无变化。

## Task 2：管理入口与持续维护

**Files:** README、AGENTS、CONTRIBUTING、CHANGELOG、`docs/REQUIREMENTS.md`、`docs/DECISIONS.md`、`docs/SOURCES.md`、`docs/STATUS.md`、PR与资料Issue模板。

- [x] 补齐资料入口、当前状态、REQ-002资料入库和REQ-003管理完善；历史已验收状态与证据对应。
- [x] 明确来源版本、原件保护、转换／人工说明区分、链接和校验命令；记录现存识别问题入口。
- [x] 更新Unreleased、维护交接和模板；保留未发布状态。

## Task 3：自动校验与发布核验

**Files:** `.github/workflows/repository-checks.yml`。

- [x] 配置只读权限、固定依赖版本和固定checkout提交；在PR、main推送及手动触发时运行相同测试与校验。
- [x] 自审差异，提交PR，等待实际Actions结果；通过后按仓库流程合并。
- [x] 回读main及对应Actions，记录验证证据和仍未启用的GitHub分支保护，不虚构平台设置。
