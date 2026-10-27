# 开发与维护约定

## 分支与变更

- main 保存可审阅的当前基线；本次空仓库初始化完成后，日常改动优先通过 PR 合并。
- 从最新 main 建立短期分支：feat/<主题>、fix/<主题>、docs/<主题>、chore/<主题>。
- 不为尚不存在的团队和发布周期引入长期 develop 分支。
- 不直接改写 main 历史；不要强制推送共享分支。
- 推荐聚焦的提交说明：feat:、fix:、docs:、test:、refactor:、chore:，例如 docs: 完善发布验收清单。
- 有不兼容变更时，在 PR 和更新日志明确写出影响及迁移办法。

## 需求与缺陷

- 功能需求使用需求模板，缺陷使用缺陷模板。
- docs/REQUIREMENTS.md 是编号、范围和验收状态的基准；Issue 记录执行讨论，PR 记录实现与验证。
- 不重复维护长篇内容；在台账中保留摘要和对应链接即可。
- 简单文档修正可不建 Issue；涉及行为、接口、数据或数值结果的变更应具有明确验收标准。

## PR 与验证

PR 应说明问题、变化、关联需求、验证证据、风险和必要的回退方法。

提交前：

- 检查差异，确保仅包含本次范围。
- 运行适合改动的现有检查；只有文档时检查链接、模板和内容一致性。
- 涉及功能或缺陷时，执行有针对性的测试；涉及算法时提供定量比较和容差。
- 更新受影响的 README、需求状态和 CHANGELOG。
- 删除或忽略临时输出，确认无凭据及不适合公开的内容。

至少由维护者完成审阅后合并；单人维护时可自审并记录检查结果。`Repository checks / validate`会运行单元测试及资料、链接、原件保护检查；流程上应等待这些检查通过再合并。GitHub平台是否强制要求检查由分支保护设置决定，见[实际状态](docs/STATUS.md#platform-state)。

本地执行：

```bash
python -m pip install -r requirements-validation.txt
python -m unittest discover -s tests -v
python tools/validate_repository.py --base <变更前SHA>
```

`--base`使用本次任务开始或PR目标基线的提交SHA；不传时只验证当前文件，不能声称验证了原件历史保护。文档性状态更新也要检查链接；新的错误修复需要能复现该错误的测试。完整命令和边界见[资料规则](docs/SOURCES.md)。

## 文件与依赖

- 通用文本使用 UTF-8 和 LF；Windows 命令脚本按 .gitattributes 处理。
- 生成物放在 work/ 或 outputs/，默认不进入 Git；需保留的小型基准结果应明确存入版本管理目录并说明来源。
- 正式参考资料是明确例外，存入 `references/patents/`，包含原件、全文与其图像依赖。OCR缓存、模型、虚拟环境和运行日志不入库。
- 依赖变更记录用途、版本影响和验证结果；接入技术栈后维护对应锁文件。
- `requirements-validation.txt`固定PDF页数校验依赖；仅服务于管理工具，不确定后续业务技术栈。
- 许可证由仓库所有者明确选择；当前不代为决定授权条款。
