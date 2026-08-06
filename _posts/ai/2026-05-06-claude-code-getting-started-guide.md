---
layout: post
title: Claude Code 入门指南：从安装到日常使用
author: deathwhispers
date: 2026-05-06
slug: claude-code-getting-started-guide
categories:
- AI
- General
tags:
- AI
- ClaudeCode
- Tools
status: published
---

Claude Code 是 Anthropic 推出的终端 AI 编程助手。它不是一个独立 IDE，而是一个运行在终端里的代理工具——直接读取你的代码库、执行命令、编辑文件、管理 Git 提交，像一个坐在你旁边的资深工程师。

本文从零开始，带你完成安装、首次对话、理解核心概念，以及掌握日常高频命令。

## 1. Claude Code 是什么？

先用一句话定位：**Claude Code 是一款终端里的 AI 编程代理（agentic coding tool）**。

和 Copilot、Cursor 这类 IDE 插件不同，Claude Code 工作在终端，不需要你打开特定编辑器。它的几个核心特征：

- **直接在终端运行**：和 `vim`、`git`、`npm` 一样，是命令行工具
- **自主编辑和操作文件**：不只是给建议，它能直接写代码、改文件、执行命令
- **理解整个代码库**：自动索引项目结构，知道哪些文件在哪里
- **工具调用链**：读写文件、运行 shell 命令、搜索代码、发 PR 都能做
- **子代理系统**：可以派发独立代理并行做代码审查、探索代码库等任务

一句话总结：**把你用自然语言描述的需求，在终端里变成可以运行的代码。**

## 2. 安装与首次配置

### 2.1 安装

macOS / Linux 下一条命令：

```bash
npm install -g @anthropic-ai/claude-code
```

Windows 用户同样用 npm 全局安装：

```bash
npm install -g @anthropic-ai/claude-code
```

安装完成后验证：

```bash
claude --version
```

### 2.2 首次启动

进入你的项目目录，运行：

```bash
cd your-project
claude
```

首次运行会引导你完成几个配置项：

1. **认证**：通过浏览器登录 Anthropic 账号，或在终端输入 API Key
2. **权限模式**：选择默认权限策略。建议初学者选"按需确认"（Ask），每次操作都让你审批
3. **项目上下文**：Claude Code 会自动读取项目文件结构作为上下文

### 2.3 指定模型

你可以通过 `/model` 命令或启动参数切换模型：

```bash
# 启动时指定
claude --model opus

# 进入后切换
/model sonnet
```

可选的模型包括 `opus`（最强大）、`sonnet`（均衡）、`haiku`（最快）。

## 3. 第一次对话

进入 Claude Code 后，你会看到一个交互式终端界面。直接输入你的需求即可。

### 3.1 基本交互

```
> 帮我看看这个项目的目录结构，解释它是做什么的
```

Claude Code 会：
1. 读取项目文件（`package.json`、`README.md`、目录结构等）
2. 分析项目类型和技术栈
3. 给出清晰的解释

### 3.2 代码修改

```
> 把 src/utils/format.ts 里的日期格式化函数改成支持自定义格式字符串
```

Claude Code 会：
1. 读取目标文件
2. 理解现有代码逻辑
3. 通过 Edit 工具精确修改代码
4. 展示 diff 供你确认

### 3.3 运行命令

```
> 帮我跑一遍测试，看看有没有失败的用例
```

Claude Code 会执行 `npm test` 或项目对应的测试命令，分析输出，给出结果和修复建议。

### 3.4 理解权限弹窗

每次 Claude Code 执行操作前（比如编辑文件、运行命令），根据你的权限设置，可能会弹出一个确认框：

- **Allow** — 允许本次操作
- **Deny** — 拒绝本次操作
- **Always Allow** — 对这类操作不再询问（可后续修改）
- **Always Deny** — 永久拒绝这类操作

刚开始可以多看看每一步在做什么，熟悉后再逐步放开权限。

## 4. 核心概念

### 4.1 会话（Session）

每次运行 `claude` 就是一个新会话。会话有以下特性：

- 有独立的上下文窗口，会随着对话增长
- 默认保留在本地，下次可以 `claude --resume` 恢复最近的会话
- 上下文接近上限时，Claude Code 会自动提示你执行压缩（compact）

### 4.2 上下文窗口

每次对话，Claude Code 能"看到"的内容有上限（不同模型不同，通常 200K tokens）。这些内容消耗在：

- 对话历史
- 读取的文件内容
- 工具调用结果（如 `ls` 命令输出）

太长或太杂的对话会让模型"注意力分散"。管理上下文是高效使用 Claude Code 的关键技能。

### 4.3 CLAUDE.md — 项目级记忆

在项目根目录放一个 `CLAUDE.md` 文件，Claude Code 每次启动都会自动读取：

```markdown
# CLAUDE.md

## 项目简介
这是一个 Next.js 博客系统，使用 Tailwind CSS 做样式。

## 技术约定
- 使用 TypeScript 严格模式
- 组件放在 src/components/ 下
- 提交信息用中文
- 不要使用 any 类型
```

这个文件就像给 Claude 的"入职指南"，告诉它项目规范、约定和偏好，避免每次对话都重新解释。

### 4.4 记忆系统（Memory）

除了 `CLAUDE.md`，Claude Code 还有一个持久化记忆系统，存放在 `.claude/memory/` 目录下。它会在对话中自动学习你的偏好并保存：

- 你的角色和技术背景
- 你对代码风格的偏好
- 项目特定的上下文信息

你可以用 `/memory` 查看和编辑记忆。

### 4.5 权限系统

Claude Code 的权限是分层管理的，配置文件在 `~/.claude/settings.json`（用户级）和 `.claude/settings.json`（项目级）：

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(npm:*)",
      "Read(*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push:*)"
    ]
  }
}
```

权限粒度可以精确到"允许 npm 命令但不允许 `npm publish`"。

## 5. 常用基础命令

Claude Code 的斜杠命令（slash commands）是核心操作入口。输入 `/` 就能看到完整列表。

### 5.1 会话管理

| 命令 | 作用 | 使用场景 |
|------|------|----------|
| `/help` | 查看所有命令和说明 | 忘记命令时 |
| `/clear` | 清空当前对话上下文 | 话题跑偏了，想重新开始 |
| `/compact` | 压缩上下文，释放空间 | 对话很长，提示上下文接近上限时 |
| `/resume` | 恢复之前的会话 | 中断后继续上次的工作 |

### 5.2 上下文管理

| 命令 | 作用 | 使用场景 |
|------|------|----------|
| `/add-dir <path>` | 把目录加入工作上下文 | 需要跨多个目录协作时 |
| `/memory` | 查看和编辑持久化记忆 | 更新偏好或查看已知信息 |
| `/init` | 初始化或更新 CLAUDE.md | 为新项目或新阶段建立上下文 |

### 5.3 配置与信息

| 命令 | 作用 | 使用场景 |
|------|------|----------|
| `/model` | 查看或切换模型 | 简单任务换快模型，复杂任务换强模型 |
| `/config` | 查看和修改配置 | 调整主题、权限、默认模型等 |
| `/status` | 查看当前会话状态 | 了解上下文使用量、回话时长 |
| `/cost` | 查看 API 费用统计 | 关注 token 消耗 |

### 5.4 代码操作

| 命令 | 作用 | 使用场景 |
|------|------|----------|
| `/review` | 对当前 diff 做代码审查 | 提交前自查 |
| `/security-review` | 安全审查 | 检查代码中的安全隐患 |

### 5.5 高级入口

| 命令 | 作用 | 使用场景 |
|------|------|----------|
| `/agents` | 查看可用的子代理类型 | 需要并行处理多个任务 |
| `/workflows` | 查看和管理后台工作流 | 查看多代理编排的运行状态 |

## 6. 日常场景实战

### 场景一：阅读陌生代码库

```
> 我刚 clone 了这个项目，帮我梳理一下整体架构，重点说明数据是怎么从 API 流到 UI 的
```

### 场景二：修一个 bug

```
> 用户反馈登录后跳转回首页时 token 丢失，帮我排查 src/auth/ 目录下的登录逻辑
```

### 场景三：添加新功能

```
> 我需要加一个暗色模式切换功能，用 Tailwind 的 dark class 策略。请帮我：1) 调研现有的主题相关代码 2) 实现切换组件 3) 确保现有页面兼容
```

### 场景四：提交前自查

```
> 帮我 review 当前的改动，看看有没有遗漏的安全问题和边界情况
```

### 场景五：自动生成提交

```
> 帮我总结这次的改动，生成一条规范的 commit message，然后提交
```

## 7. 三个关键习惯

### 习惯一：先建立 CLAUDE.md

进入新项目的第一件事，额外花 3 分钟写一个 `CLAUDE.md`。长期收益远超投入：

```markdown
# CLAUDE.md
## 项目：电商后台管理系统
- Next.js 14 + TypeScript + Prisma + PostgreSQL
- 提交信息格式：feat:/fix:/refactor:/docs: + 中文描述
- 不要修改 package.json 的依赖版本号
- API 路由放在 src/app/api/ 下
```

### 习惯二：学会主动 compact

对话长了之后，Claude Code 会提示"上下文接近上限"。不要等到提示才压缩——在完成一个相对独立的任务后，主动 `/clear` 清空对话，开始新的话题。

### 习惯三：写清楚需求，而不是写步骤

给 Claude Code 描述"你想达成什么"，而不是"每一步怎么做"。好的提示：

```
> 用户下单后需要发邮件通知，帮我实现这个功能。先看看现有的邮件模板是怎么写的，保持风格一致。
```

不太好的提示：

```
> 打开 src/order.ts，在第 45 行加一个函数，调用 sendEmail，参数是 orderId 和 email
```

后者听起来很精确，但实际上你夺走了 Claude Code 分析问题和做判断的空间。

## 8. 安全注意事项

- **不要盲批 `Always Allow`**：先用一段时间保持手动确认，等熟悉了各类操作再逐渐放开。
- **敏感信息保护**：`CLAUDE.md` 和 `.claude/memory/` 可能随 git 提交。注意不要把 API Key、密码、内部 IP 等写入这些文件。
- **危险命令加 deny**：在 `.claude/settings.json` 中永久拒绝 `rm -rf`、`git push --force` 等高风险命令。
- **代码审查不可省略**：Claude Code 很聪明但也会犯错。所有 AI 生成的代码都应该人工审查后再合并。

## 9. 下一步

这篇入门指南覆盖了 Claude Code 的基本用法。当你熟悉了这些基础操作后，可以继续阅读：

- **《Claude Code 实战速查手册》**：命令速查表、权限管理最佳实践、MCP 工具使用、常见工作流
- **《Claude Code 深度进阶》**：Hooks 系统、自定义技能、Worktree 隔离、多代理编排、CI/CD 集成

## 参考资料

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic CLI 参考](https://docs.anthropic.com/en/docs/claude-code/cli-reference)
