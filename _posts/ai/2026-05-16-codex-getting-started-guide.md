---
layout: post
title: Codex 入门指南：OpenAI 的终端 AI 编程助手
author: deathwhispers
date: 2026-05-16
slug: codex-getting-started-guide
categories:
- AI
- General
tags:
- AI
- Codex
- OpenAI
- Tools
status: published
---

Codex 是 OpenAI 推出的终端 AI 编程代理。和 Claude Code 类似，它直接在终端中运行，能读代码、编辑文件、执行命令、管理 Git，像一个不需要休息的结对编程伙伴。

本文从零开始，带你完成安装、首次使用、理解核心概念，以及掌握日常高频命令。

## 1. Codex 是什么？

Codex 的定位是**终端里的自主编程代理（agentic coding agent）**。它和 Copilot（IDE 补全插件）的区别在于：

- **Copilot**：在你编辑器中补全代码，偏"辅助"
- **Codex**：在终端中自主规划和执行任务，偏"代理"

核心特征：

- **终端原生**：在 shell 中运行，和 git、npm、docker 等工具天然协作
- **全自主执行**：不只是给建议，能直接修改代码、运行测试、提交 PR
- **沙箱执行**：危险命令在沙箱中运行，保护你的系统和数据
- **多模型支持**：底层使用 OpenAI GPT 系列模型，可选不同能力级别
- **Git 深度集成**：自动创建分支、提交、发 PR
- **扩展生态**：支持 MCP 工具、自定义命令、hooks

## 2. 安装与首次配置

### 2.1 安装

macOS / Linux：

```bash
# 通过 Homebrew（macOS）
brew install openai/chatgpt/codex

# 或通过 npm
npm install -g @openai/codex
```

Windows：

```bash
npm install -g @openai/codex
```

验证安装：

```bash
codex --version
```

### 2.2 首次启动

进入项目目录，运行：

```bash
cd your-project
codex
```

首次运行会引导你完成配置：

1. **认证**：通过浏览器登录 OpenAI 账号，或设置 `OPENAI_API_KEY` 环境变量
2. **模型选择**：选择默认模型（如 `gpt-5`、`gpt-5-mini` 等）
3. **权限策略**：选择默认权限模式
4. **项目上下文**：Codex 自动索引项目结构

### 2.3 切换到 Codex

如果你从 Claude Code 迁移过来，主要差异：

| 维度 | Claude Code | Codex |
|------|------------|-------|
| 启动命令 | `claude` | `codex` |
| 底层模型 | Claude 系列 | GPT 系列 |
| 配置文件 | `.claude/settings.json` | `.codex/config.yaml` |
| 项目上下文 | `CLAUDE.md` | `CODEX.md` 或 `.codex/instructions.md` |
| 记忆系统 | `.claude/memory/` | `.codex/memory/` |
| 沙箱执行 | 可选 | 默认开启 |

## 3. 第一次对话

进入 Codex 后，直接输入需求：

### 3.1 基本交互

```
> 这个项目是做什么的？帮我梳理一下整体架构
```

Codex 会读取项目文件，分析技术栈，给出结构化解释。

### 3.2 代码修改

```
> 帮我把 src/utils/date.ts 中的日期格式化函数增加时区参数支持
```

Codex 会读取文件、分析现有逻辑、精确编辑，展示 diff 供你确认。

### 3.3 运行命令

```
> 跑一遍测试，看看有没有失败的用例，有的话帮我分析原因
```

### 3.4 理解权限机制

Codex 在每次执行操作前，根据权限策略有不同的行为：

- **默认模式**（推荐）：每个危险操作都会弹出确认框
- **自动模式**：可配置哪些操作自动通过
- **严格模式**：所有写操作都需要人工确认

确认框选项：
- **Approve** — 允许本次
- **Deny** — 拒绝本次
- **Always approve** — 以后类似操作自动允许
- **Always deny** — 以后类似操作自动拒绝

建议刚开始不要轻易用 "Always approve"，保持对操作的可视性。

## 4. 核心概念

### 4.1 会话（Session）

每次 `codex` 启动就是一次新会话。会话特点：

- 独立上下文窗口，不同模型有不同上限
- 自动保存，可用 `codex --resume` 恢复
- 上下文接近上限时会提示压缩

### 4.2 上下文窗口

Codex 能"看到"的内容包括：对话历史、读取的文件、工具调用结果、项目索引信息。

管理要点：
- 避免一次会话塞入太多不相关的任务
- 及时清理已完成话题
- 善用 `CODEX.md` 减少重复解释

### 4.3 CODEX.md — 项目说明书

在项目根目录创建 `CODEX.md`，Codex 每次启动自动读取：

```markdown
# CODEX.md

## 项目概述
一个基于 FastAPI 的微服务框架，支持 gRPC 和 REST 双协议。

## 技术栈
- Python 3.12 + FastAPI + SQLAlchemy + PostgreSQL
- Redis 做缓存，RabbitMQ 做消息队列

## 编码约定
- 使用 ruff 做格式化和 lint
- 类型注解覆盖率要求 100%
- 测试用 pytest + pytest-asyncio
- API 端点文档用 FastAPI 自动生成的 OpenAPI

## 不要做的事
- 不要修改 alembic 迁移文件的历史记录
- 不要升级 requirements.txt 中的主版本号
```

### 4.4 记忆系统

Codex 在 `.codex/memory/` 下维护持久化记忆，自动学习你的偏好。你可以：

- `/memory` 查看所有记忆
- 在对话中说"记住：我们的 API 端口是 8080"
- 过时的记忆手动删除

### 4.5 沙箱执行

Codex 默认在沙箱中运行 Bash 命令，隔离效果：

- 文件系统操作在沙箱中进行
- 网络访问受限
- 敏感目录（如 `~/.ssh`）不可访问

信任的项目可以放宽沙箱限制，在配置文件中设置。

## 5. 常用命令

### 5.1 会话控制

| 命令 | 作用 |
|------|------|
| `/help` | 查看所有命令 |
| `/clear` | 清空上下文 |
| `/compact` | 压缩上下文释放空间 |
| `/resume` | 恢复之前的会话 |
| `/status` | 查看会话状态和 token 用量 |
| `/cost` | 查看 API 费用 |

### 5.2 上下文管理

| 命令 | 作用 |
|------|------|
| `/init` | 创建或更新 CODEX.md |
| `/memory` | 查看和编辑持久化记忆 |
| `/add-dir <path>` | 添加目录到工作上下文 |

### 5.3 代码操作

| 命令 | 作用 |
|------|------|
| `/review` | 代码审查当前改动 |
| `/fix` | 自动修复 lint/类型错误 |
| `/test` | 运行测试并分析结果 |
| `/pr` | 创建 Pull Request |

### 5.4 配置与模型

| 命令 | 作用 |
|------|------|
| `/model` | 查看或切换模型 |
| `/config` | 打开配置菜单 |
| `/sandbox` | 管理沙箱设置 |

### 5.5 子代理

| 命令 | 作用 |
|------|------|
| `/agents` | 查看可用的子代理类型 |
| `/delegate` | 派发任务给子代理 |

### 5.6 常用启动参数

```bash
codex                                   # 交互模式
codex -p "解释这个项目"                   # 一次性任务，输出后退出
codex --model gpt-5                     # 指定模型
codex --resume                          # 恢复最近会话
codex --sandbox off                     # 关闭沙箱（信任项目）
codex --no-sandbox                      # 同上
codex --config                          # 打开配置面板
```

## 6. 日常场景实战

### 场景一：快速上手陌生项目

```
> 我刚 clone 这个项目，帮我：
> 1) 梳理目录结构和各模块职责
> 2) 找到入口文件和核心路由
> 3) 告诉我怎么在本地跑起来
```

### 场景二：修 Bug

```
> 用户反馈登录后刷新页面会丢失登录状态，定位一下 src/auth/ 里的 token 持久化逻辑
```

### 场景三：添加新功能

```
> 我要给用户表加一个 avatar_url 字段，做完整的迁移链路：
> 1) 修改数据库 schema
> 2) 更新 API 接口的上传处理
> 3) 前端显示头像
> 先给我方案，确认后再动手。
```

### 场景四：自动发 PR

```
> 帮我：
> 1) 看一遍改动总结
> 2) 写 commit message
> 3) 创建分支并提交
> 4) 发 PR，PR 描述写清楚改动内容和测试情况
```

Codex 的 `/pr` 命令可以一键完成上述流程。

### 场景五：写测试

```
> 检查 src/services/user.py 的测试覆盖率，给没覆盖的地方补上单元测试
```

## 7. 三个好习惯

### 习惯一：写好 CODEX.md

每次进入新项目，花 5 分钟写一个 `CODEX.md`。它不是一次性文档——随着项目演进持续更新。内容不需要长，但一定要精准。

### 习惯二：任务分离，主动清上下文

不要在一个会话里试图完成一整个大功能。做完一个独立任务后 `/clear`，在新的上下文中开始下一个任务。

### 习惯三：先审方案再动手

对复杂的改动，先让 Codex 给出方案而不是直接改代码：

```
> 我要重构支付模块，先给我重构方案和影响范围分析，不要直接改
```

确认方案后再让它在干净的会话中执行——这时上下文里只有"方案"和"执行"两层，注意力最集中。

## 8. 安全注意事项

- **沙箱不要全关**：保持默认沙箱开启，只在充分信任的项目中放宽
- **审查 AI 生成的代码**：Codex 很聪明但不是万能的，所有改动都应该人工审查
- **敏感信息不进 CODEX.md**：API Key、密码、内部 IP 等信息不要写入 CODEX.md
- **`.gitignore` 配置**：确保 `.codex/memory/` 和 `.codex/sandbox/` 不会意外提交敏感数据
- **权限最小化**：日常开发用默认权限模式，只在 CI 中放开更多权限

## 9. 下一步

这篇入门指南覆盖了 Codex 的基本用法。当你熟悉了日常操作后：

- **《Codex 实战速查手册》**：命令速查表、权限配置模板、工作流模板、常见问题
- **《Codex 深度进阶》**：Hooks 系统、自定义命令、沙箱策略、多代理编排、CI/CD 集成

## 参考资料

- [Codex 官方文档](https://platform.openai.com/docs/guides/codex)
- [OpenAI API 参考](https://platform.openai.com/docs/api-reference)
