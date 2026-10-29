# 《整机需要准备的工作》编写计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 基于R3交付面向DUV设备、可讨论分工和验证的具体准备工作报告。

**Architecture:** 保留R3作为研究基线，新报告按工作、依赖、交付物和验收组织；四个独立资料域并行定向复核，主编整合正文及图示。用户明确要求直接撰写，不另设组织结构审批轮。

**Tech Stack:** Markdown、已有原PDF与MinerU、Matplotlib SVG、Pandoc／Chromium预览及仓库现有检查。

**Spec:** [用户范围及组织判断](../specs/2026-10-29-whole-machine-preparation-design.md)。

## Global Constraints

- 基线`bf495f886ba027941721dd754b8f82be96d14abe`；原始资料和R3不改。
- 报告为`reports/whole-machine-preparation/report.md`，V1，独立于架构报告R3；Markdown交付，无PDF。
- 直接披露、工程建议、采用条件及待补设备资料分别说明；不预设浸没式、不编造nm指标和工期。
- 不为可逆文档改写添加模仿实现的单元测试；使用既有18项测试、仓库校验、证据审查、显示及哈希检查。

## Review Focus

1. 用户示例是否被错误写成必装硬件，RTS是否被误当成FF效果的唯一证据。
2. dHDM的公开名称／维护用途是否被扩成未证实的波前模式、带宽或套刻性能。
3. Wafer table、晶圆与镜块的对象和任务是否混淆，浸没措施是否错误普适化。
4. 每项是否有具体动作、依赖、产物与验证，建议是否冒充专利原文或已完成试验。
5. 数据、坐标、已用校正和残差的职责是否闭合；图表、来源及版本链接是否可追溯。

## Task 1：证据与工作分解

- [x] 核对最新main，建立短期分支和独立报告；复制R3为改写起点并记录继承关系。
- [x] 四域定向复核，将证据与建议写入`review/thermal.md`、`mechanics.md`、`optics.md`、`control.md`，不改主稿或原件。
- [x] 确定任务ID、启动条件、共同数据及验收口径。

## Task 2：正文及路线图

- [x] 以具体工作为主线重写正文，保留三类热前馈、传感器路线、平台改造、光学能力和闭环整合的因果关系。
- [x] 绘制工作依赖图，检查节点尺寸、文字边距、连线和网页显示；关键决策结合原专利图。
- [x] 汇总首批行动、阶段出口、R3覆盖及未知参数；明确责任角色为建议分工。

## Task 3：记录与核验

- [x] 写sources.json、delivery.json；新增REQ-007并同步README、报告入口、STATUS、CHANGELOG。
- [x] 运行`.venv/bin/python -m unittest discover -s tests -v`及`.venv/bin/python tools/validate_repository.py --base bf495f886ba027941721dd754b8f82be96d14abe`。
- [x] 独立审阅任务可执行性与证据边界，整合修正；检查旧资料不变、图像、链接和最终哈希。

## Task 4：保存

- [ ] 提交、快进合并推送main并删除本轮短期分支；远端回读关键文件和对应Actions，记录实际结果。

实际证据：[报告交付记录](../../../reports/whole-machine-preparation/delivery.json)。工作清单撰写完成不代表设备研发任务已经完成。
