---
layout: post
title: Get Shit Done（GSD）实战使用文档：从安装到交付
slug: gsd-get-shit-done-usage-guide
status: Published
date: 2026-04-10
mermaid: true
tags:
- AI
categories:
- AI
- General
author: deathwhispers
---

如果你已经用过 Claude Code、Codex、OpenCode 这类 AI 编程工具，你大概率会遇到一个问题：

- 会话越长，质量越不稳定；
- 需求越复杂，越容易“上下文腐烂（context rot）”。

`get-shit-done`（简称 GSD）就是为这个问题设计的一层“工作流与上下文工程系统”。本文基于官方 README 和 User Guide，总结一份可以直接落地的使用文档。

## 1. GSD 是什么？适合谁？

GSD 的定位不是“另一个模型”，而是“编排层（orchestration layer）”：

- 把需求拆成阶段（phase）和原子计划（plan）；
- 用多代理并行执行；
- 每步都保留验证与状态文件；
- 通过流程减少上下文衰减。

适合人群：

- 个人开发者或小团队；
- 希望 AI 自动化更多开发流程，但不想引入重型流程平台；
- 需要“能持续交付”的 AI 辅助，而不只是一次性生成代码。

## 2. 一图看懂 GSD 工作流

```mermaid
flowchart LR
  A[gsd-new-project] --> B[gsd-discuss-phase N]
  B --> C[gsd-plan-phase N]
  C --> D[gsd-execute-phase N]
  D --> E[gsd-verify-work N]
  E --> F[gsd-ship N]
  F --> G[gsd-next / 下一阶段]
```

核心思想：

1. 先把上下文问清楚（discuss）；
2. 再做研究和计划（plan）；
3. 用新鲜上下文执行原子任务（execute）；
4. 最后做人类验收（verify）并发 PR（ship）。

## 3. 安装与初始化

## 3.1 一条命令安装

```bash
npx get-shit-done-cc@latest
```

安装器会让你选择：

- 运行时：Claude Code / OpenCode / Gemini / Kilo / Codex / Copilot / Cursor / Windsurf / Antigravity / Augment / Trae / Cline；
- 安装位置：全局（global）或当前项目（local）。

## 3.2 非交互安装（CI / 脚本）

例如 Codex 全局安装：

```bash
npx get-shit-done-cc --codex --global
```

Claude 本地安装：

```bash
npx get-shit-done-cc --claude --local
```

## 3.3 安装后验证

- Claude/OpenCode/Gemini 等：`/gsd-help`
- Codex：`$gsd-help`

## 4. 第一次跑通：推荐最小路径

假设你从零开始一个项目：

```bash
/gsd-new-project
/gsd-discuss-phase 1
/gsd-plan-phase 1
/gsd-execute-phase 1
/gsd-verify-work 1
/gsd-ship 1
```

如果是已有代码仓库，先跑：

```bash
/gsd-map-codebase
/gsd-new-project
```

这样后续规划会带上你的现有架构与约束。

## 5. GSD 关键产物（.planning）

GSD 的可控性来自“显式文件状态”，常见包括：

- `PROJECT.md`：项目目标与边界；
- `REQUIREMENTS.md`：需求拆解与范围；
- `ROADMAP.md`：阶段路线；
- `STATE.md`：当前进度与决策；
- `N-CONTEXT.md`：阶段上下文偏好；
- `N-RESEARCH.md`：阶段研究；
- `N-M-PLAN.md`：原子执行计划；
- `N-VERIFICATION.md`、`N-UAT.md`：验证与验收。

这些文件本质上就是“可审计的 AI 工作记忆”。

## 6. 命令分层：你最该记住哪些

## 6.1 主流程命令

- `/gsd-new-project`：项目初始化（问答→研究→需求→路线图）
- `/gsd-discuss-phase N`：锁定阶段实现偏好
- `/gsd-plan-phase N`：生成并校验原子计划
- `/gsd-execute-phase N`：按依赖波次并行执行
- `/gsd-verify-work N`：人工 UAT + 失败诊断
- `/gsd-ship N`：生成 PR

## 6.2 快速任务命令

- `/gsd-fast <text>`：极小任务，跳过规划
- `/gsd-quick`：小中型临时任务，保留 GSD 保障（支持 `--discuss`、`--research`、`--validate`、`--full`）

建议：

- 改一个错别字、常量、文案：`fast`
- 需要一点分析和验证的小改动：`quick`
- 涉及功能与结构演进：走完整 phase 流程

## 6.3 会话恢复与导航

- `/gsd-progress`：我现在在哪一步？
- `/gsd-next`：自动推进下一步
- `/gsd-resume-work`：断点恢复

## 7. 配置重点（.planning/config.json）

常用配置维度：

- `mode`: `interactive` / `yolo`
- `granularity`: `coarse` / `standard` / `fine`
- `model_profile`: `quality` / `balanced` / `budget` / `inherit`
- `workflow.research`, `workflow.plan_check`, `workflow.verifier`
- `parallelization.enabled`
- `git.branching_strategy`: `none` / `phase` / `milestone`

经验建议：

- 原型期：`yolo + coarse + budget`
- 正常开发：`interactive + standard + balanced`
- 生产上线前：`interactive + fine + quality`

## 8. 多运行时（尤其 Codex）注意点

User Guide 明确提到：非 Claude 运行时（Codex/OpenCode/Gemini/Kilo）安装时会自动设置 `resolve_model_ids: "omit"`，让模型选择交给运行时。

如果你要细粒度指定代理模型，可在 `model_overrides` 中显式配置（例如给 planner/executor/debugger 不同模型）。

## 9. 安全与权限建议

README 给了两套策略：

1. 追求流畅自动化：`claude --dangerously-skip-permissions`
2. 保守策略：在 `.claude/settings.json` 配置细粒度 allow/deny

另外，建议把敏感文件加入 deny（如 `.env`、`*.pem`、`*.key`），避免 codebase mapping 或分析阶段误读密钥。

## 10. 常见问题与排障

- 命令找不到：重启运行时，检查 skills/commands 是否安装到目标目录
- 行为异常：先跑 `/gsd-help`，再重装 `npx get-shit-done-cc`
- 执行后要改小问题：不要整阶段重跑，优先 `/gsd-quick`
- 成本过高：`/gsd-set-profile budget` 并关闭部分工作流代理
- 容器环境路径问题：按文档设置 `CLAUDE_CONFIG_DIR`

## 11. 我建议的落地打法（实战版）

1. 先在一个中小项目试跑完整 phase 流程。
2. 只保留你真正需要的代理开关（research/plan_check/verifier）。
3. 建立团队统一的 `granularity` 和 `branching_strategy` 约定。
4. 把 `/gsd-progress` 和 `/gsd-next` 作为每日主入口。
5. 用 `/gsd-quick` 承接“上线后小修小补”，避免流程过重。

## 12. 总结

GSD 的价值，不在“多加了多少命令”，而在于它把 AI 编程从一次性对话，转成了可恢复、可验证、可审计的工程流程。

如果你正被“上下文越聊越乱”困扰，GSD 值得至少在一个真实项目里完整跑一遍。

## 参考资料

1. GSD 官方仓库 README
   [https://github.com/gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
2. GSD User Guide
   [https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)
3. GSD CHANGELOG（版本变化）
   [https://github.com/gsd-build/get-shit-done/blob/main/CHANGELOG.md](https://github.com/gsd-build/get-shit-done/blob/main/CHANGELOG.md)
4. GSD 官方站
   [https://gsd.site/](https://gsd.site/)
