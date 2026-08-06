---
layout: post
title: Claude Code 实战速查手册：每天都要用的命令与技巧
author: deathwhispers
date: 2026-05-23
slug: claude-code-practical-quick-reference
categories:
- AI
- General
tags:
- AI
- ClaudeCode
- Tools
status: published
---

本文面向已经上手 Claude Code 的开发者，聚焦日常高频场景的可复制方案。你可以把它当速查表——需要时直接搜关键词，找到命令复制就用。

## 1. 命令速查表

### 1.1 全命令分类索引

#### 会话控制

| 命令 | 用途 | 典型用法 |
|------|------|----------|
| `/clear` | 清空上下文，开始新话题 | 一个独立任务完成后 |
| `/compact` | 压缩上下文，释放窗口空间 | 对话长、开始变慢时 |
| `/resume` | 恢复最近一次会话 | 终端关了、中断了 |
| `/resume <id>` | 恢复指定会话 | 切到之前的某次对话 |
| `/doctor` | 诊断配置和连接问题 | 启动报错、连不上 API |

#### 上下文与项目信息

| 命令 | 用途 | 典型用法 |
|------|------|----------|
| `/add-dir <path>` | 添加目录到工作上下文 | 需要同时操作多个模块 |
| `/init` | 创建或更新 CLAUDE.md | 新项目启动 / 规范有变 |
| `/memory` | 查看和编辑持久化记忆 | 更新偏好、清理过时记忆 |
| `/status` | 查看会话状态和 token 用量 | 监控上下文消耗 |
| `/cost` | 查看本次和累计费用 | 关注 API 开销 |

#### 代码操作

| 命令 | 用途 | 典型用法 |
|------|------|----------|
| `/review` | 代码审查当前 diff | 提交前自查 |
| `/security-review` | 安全漏洞审查 | 上线前检查 |
| `/simplify` | 简化/重构当前改动 | 代码能跑但觉得不够干净 |
| `/run` | 运行项目并验证改动 | 改完后确认能正常工作 |
| `/verify` | 端到端验证改动行为 | 不只是跑测试，还要看效果 |

#### 配置与模型

| 命令 | 用途 | 典型用法 |
|------|------|----------|
| `/model` | 查看或切换模型 | 快速任务切 haiku，复杂任务切 opus |
| `/model <name>` | 直接切换到指定模型 | `/model opus` |
| `/config` | 打开配置面板 | 调整主题、权限、通知 |
| `/permissions` | 管理权限规则 | 新增 allow/deny 规则 |

#### 子代理与编排

| 命令 | 用途 | 典型用法 |
|------|------|----------|
| `/agents` | 列出可用子代理类型 | 需要派发探索、审查任务 |
| `/workflows` | 查看工作流运行状态 | 调试多代理编排 |

#### 外部集成

| 命令 | 用途 | 典型用法 |
|------|------|----------|
| `/login` | 登录 Anthropic 账号 | 首次使用或 token 过期 |
| `/logout` | 登出 | 切换账号 |
| `/mcp` | 管理 MCP 服务器连接 | 添加/移除外部工具源 |
| `/terminal-setup` | 设置终端集成（快捷键绑定） | 配置 `Ctrl+K` 等快捷呼出 |

#### Bash 快捷方式

在对话中输入 `!<command>` 可以直接在终端执行而不通过 Claude Code：

```
> !git diff --stat
```

这在需要快速查看状态又不想让 Claude 分析时特别有用。

### 1.2 启动参数速查

```bash
# 基础启动
claude                                          # 进入交互模式

# 模型选择
claude --model opus                              # 用最强模型启动
claude --model haiku                             # 快速轻量任务

# 一次性任务（非交互）
claude -p "解释这个项目的架构"                    # print 模式，输出即退出
claude -p "审查 src/auth/ 的安全性" --model opus
claude -c "帮我修 src/login.ts 的第 45 行 bug"    # 带上下文执行

# 会话管理
claude --resume                                  # 恢复最近会话
claude --resume <session-id>                     # 恢复指定会话

# 配置
claude --config                                  # 打开配置面板
claude --update                                  # 更新到最新版本
```

## 2. 权限管理实战

### 2.1 权限类型速查

| 权限 | 覆盖范围 | 示例 |
|------|----------|------|
| `Read` | 读取文件/目录 | `Read(*)` — 读取所有文件 |
| `Edit` | 编辑文件 | `Edit(src/**)` — 允许编辑 src 下所有文件 |
| `Write` | 创建新文件 | `Write(src/**)` — 允许在 src 下创建文件 |
| `Bash` | 执行 shell 命令 | `Bash(git:*)` — 允许所有 git 命令 |
| `WebFetch` | 获取网页内容 | `WebFetch(*)` — 允许访问任何网页 |
| `WebSearch` | 搜索网页 | `WebSearch(*)` — 允许网页搜索 |
| `MCP.*` | MCP 工具调用 | `MCP.github:*` — 允许 GitHub MCP 所有操作 |
| `NotebookEdit` | 编辑 Jupyter | `NotebookEdit(*)` — 允许编辑所有 notebook |
| `Agent` | 派发子代理 | 控制是否能使用子代理 |

### 2.2 常用权限配置模板

#### 日常开发（推荐起点）

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Write(*)",
      "Bash(git:status)",
      "Bash(git:diff)",
      "Bash(git:log)",
      "Bash(npm:*)",
      "Bash(ls:*)",
      "Bash(find:*)",
      "Bash(grep:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(git push:*)",
      "Bash(git reset --hard:*)",
      "Bash(curl:*)",
      "WebFetch(*)"
    ]
  }
}
```

#### 信任的本地项目（宽松）

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Write(*)",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(ls:*)",
      "Bash(find:*)",
      "Bash(grep:*)",
      "Bash(node:*)",
      "WebFetch(*)",
      "WebSearch(*)"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(rm -rf:*)",
      "Bash(curl:*)"
    ]
  }
}
```

#### CI / 自动化场景（最宽松）

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Write(*)",
      "Bash(*)",
      "WebFetch(*)",
      "WebSearch(*)"
    ],
    "deny": []
  }
}
```

### 2.3 权限配置层级

Claude Code 权限有三个层级，优先级从高到低：

```
项目本地 (.claude/settings.local.json)   ← 最高优先级，不提交 git
项目级   (.claude/settings.json)          ← 团队共享，提交 git
用户级   (~/.claude/settings.json)        ← 全局默认
```

建议策略：
- **用户级**：保守策略，deny 所有高风险命令
- **项目级**：开放日常操作（Read/Edit/Bash git/npm）
- **本地级**：放敏感路径或本项目特殊需求

### 2.4 一键添加权限

遇到反复弹出的权限确认？终端里直接回复：

```
# 当前操作永远允许
Always Allow

# 或通过命令直接添加
/permissions allow Bash(git:status)
/permissions deny Bash(rm:*)
```

## 3. 上下文管理技巧

### 3.1 何时 compact

观察这几个信号：

- Claude Code 主动提示"上下文接近上限"
- 回复速度明显变慢
- 模型开始"忘记"你前面说过的话
- 同样的约束需要重复提醒

compact 的本质是把当前对话摘要成更短的形式，释放窗口空间。**在独立任务完成后立刻 compact，而不是等到提示弹出来。**

### 3.2 主动 clear 的节奏

一次对话不要试图做完一整个功能。最佳实践是"主题式对话"：

```
Session 1: 理解现有代码 → /clear
Session 2: 设计方案 → /clear
Session 3: 实现核心逻辑 → /clear
Session 4: 写测试 → /clear
Session 5: Review 和优化 → /clear
```

每次 `/clear` 之前，让 Claude Code 总结当前进度（你可以复制保存），这样下一个会话可以直接引用。

### 3.3 CLAUDE.md 最佳实践

CLAUDE.md 不需要长篇大论。一个高效的结构：

```markdown
# CLAUDE.md

## 技术栈
Next.js 14 App Router + TypeScript + Tailwind + Prisma

## 项目结构
- src/app/      → 页面路由
- src/components/ → 共享组件
- src/lib/      → 工具函数和业务逻辑
- prisma/       → 数据库 schema 和迁移

## 编码约定
- 组件用函数式 + hooks，不用 class
- 错误处理：API 层 try-catch，UI 层 ErrorBoundary
- 命名：文件名 kebab-case，组件 PascalCase，函数 camelCase
- 不要使用 any 类型
- 提交格式：type(scope): 中文描述

## 当前重点关注
- 正在做用户权限重构，涉及 src/auth/ 和 middleware.ts
- 性能优化阶段，关注 bundle size 和 LCP

## 不要做的事
- 不要改 package.json 的依赖版本
- 不要改 .eslintrc 和 prettier.config 的规则
- 不要直接操作 production 数据库
```

### 3.4 memory 体系运用

除了 CLAUDE.md（每次启动必读），还有持久化记忆：

```
/memory                    # 查看所有记忆
```

记忆会在对话中自动积累。主动管理：

- 完成一个重要项目后：`/memory` → 检查新增记忆是否准确
- 发现记忆过时：直接在界面里删除或编辑
- 不需要的记忆：宁可删掉，不要堆积过期信息

### 3.5 图片和 PDF 的直接使用

Claude Code 能直接"看"图片和 PDF：

```
> 分析这张截图里的报错信息 @/path/to/screenshot.png
> 阅读这个 PDF 文档的技术方案 @/path/to/design.pdf，帮我实现第三章的接口
```

比手动描述效率高很多，尤其适合做 UI 对照和文档解析。

## 4. MCP 工具日常使用

MCP（Model Context Protocol）让 Claude Code 可以连接外部数据源和工具。

### 4.1 常用 MCP 场景

| MCP 工具 | 用途 | 连接后的效果 |
|----------|------|------------|
| GitHub MCP | 操作 issues/PRs | 直接说"帮我创建一个 PR" |
| Postgres MCP | 查询数据库 | "查一下 users 表最近注册的用户" |
| Filesystem MCP | 跨项目文件访问 | 读写项目目录外的文件 |
| Slack MCP | 发消息 | "把这次构建结果发到 #dev 频道" |
| Jira/Linear MCP | 任务管理 | "根据这个 issue 描述写代码" |
| Context7 MCP | 查阅最新文档 | "查一下 Next.js 15 的 caching 变化" |

### 4.2 配置示例

在 `.claude/settings.json` 中添加 MCP 服务器：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/mcp-server-context7"]
    }
  }
}
```

### 4.3 在对话中确认 MCP 可用

```
> 你有哪些 MCP 工具可用？
```

Claude Code 会列出当前连接的所有 MCP 工具及它们的能力。

## 5. 高效工作流

### 5.1 代码审查流程

```
# 步骤一：查看改动
> 帮我看看当前分支的 diff，做一个完整的代码审查

# 步骤二：针对性深化
> 重点看看 src/auth/ 里的安全处理，有没有 token 泄漏或注入风险

# 步骤三：修复发现的问题
> 把刚才提到的 3 个问题都修了，每个修一个 commit
```

也可以用内置命令快速启动：

```
/review              # 启动代码审查，可选 effort 参数
/review --effort high
```

### 5.2 调试工作流

```
# 步骤一：描述症状
> 提交订单接口返回 500，帮我排查 src/app/api/orders/route.ts

# 步骤二：添加日志和定位
> 先别改逻辑，帮我加一些关键节点的日志，先定位问题

# 步骤三：修复
> 找到了，是 Prisma 查询时缺少了 include。帮我修，并加一个对应的测试

# 步骤四：验证
/verify              # 端到端验证修复是否生效
```

### 5.3 重构工作流

```
# 步骤一：理解现有代码
> 梳理 src/services/payment.ts 的整体逻辑，画成流程图

# 步骤二：设计方案
> 我要把这个文件拆成 3 个模块：支付创建、支付回调、退款处理。先给我拆分方案，不要直接改

# 步骤三：执行重构
> 方案可以，开始执行。每次只改一个模块，改完停一下让我确认

# 步骤四：质量检查
/simplify            # 复查重构后的代码是否可以进一步精简
/review              # 做一次审查确保没有引入 bug
```

### 5.4 TDD 工作流

最节能的方式是利用子代理：

```
> 帮我写单元测试覆盖 src/utils/validator.ts，用 vitest，先跑一遍看覆盖率缺口，再补全
```

### 5.5 发 PR 前最后检查

```
# 一键检查清单
> 帮我做上线前的全面检查：1) diff 安全审查 2) 确认没漏掉测试 3) 检查有没有 console.log/debugger 残留 4) 写 PR description
```

## 6. 常见问题

### Q: 上下文满了怎么办？

A: `/compact`。如果 compact 后还是不够，先 `> 总结一下我们目前完成了什么，还有哪些待办` 保存笔记，然后 `/clear`，在新会话中把笔记贴回去继续。

### Q: Claude Code 开始"犯糊涂"，同一个问题问了好几遍？

A: 上下文太长导致模型注意力分散。立刻 `/compact` 或 `/clear`。

### Q: 权限弹窗太多影响效率？

A: 跑一遍 `/permissions`，把每天要做的事情一次性加白名单。参考 2.2 节的配置模板。

### Q: 怎么知道它有没有在读懂我的代码？

A: 先问开放式问题测试——"这段代码你觉得哪个地方最可能出问题？" 如果 Claude 能指出具体的变量、函数、边界情况，说明它真在"读"。

### Q: 如何查看花了多少钱？

A: `/cost`。会显示当前会话和累计的 API 费用。

### Q: 一个复杂需求应该在一个会话里完成还是拆开？

A: 拆开。一个会话一个核心任务。大需求会耗尽上下文窗口，后半段质量下降明显。

## 7. 速查清单：每天启动的 5 件事

1. **`/status`** — 看看上下文用了多少，是否需要 fresh start
2. **`claude.md` 是否更新** — 昨天有没有新约定、新发现需要写入
3. **`/model` 是否合适** — 简单任务别用大模型，省钱又快
4. **权限是否顺手** — 如果昨天频繁点 Allow，今天直接加白名单
5. **一个会话一个主题** — 别在同一个会话里既修 bug 又写新功能又做 code review

把这几件事做顺了，Claude Code 会从"偶尔用的助手"变成"离不开的工具"。

## 参考资料

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code CLI 参考](https://docs.anthropic.com/en/docs/claude-code/cli-reference)
- [Model Context Protocol](https://modelcontextprotocol.io)
