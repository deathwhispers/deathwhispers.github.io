---
layout: post
title: Codex 实战速查手册：日常命令、工作流与排错
author: deathwhispers
date: 2026-06-03
slug: codex-practical-quick-reference
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

本文面向已经上手 Codex 的开发者，聚焦日常高频操作和可复制的实战方案。收藏这篇，需要时直接搜索关键词找到对应命令。

## 1. 命令速查表

### 1.1 全命令分类

#### 会话控制

| 命令 | 用途 | 常见用法 |
|------|------|---------|
| `/clear` | 清空上下文 | 任务完成后开启新话题 |
| `/compact` | 压缩上下文 | 对话变长、速度变慢 |
| `/resume` | 恢复最近会话 | 终端闪退、主动中断 |
| `/resume <id>` | 恢复指定会话 | 切回之前某次对话 |
| `/status` | 查看会话状态 | 监控 token 消耗 |
| `/cost` | API 费用统计 | 关注开销 |

#### 项目与上下文

| 命令 | 用途 | 常见用法 |
|------|------|---------|
| `/init` | 创建/更新 CODEX.md | 新项目启动 |
| `/add-dir <path>` | 加目录到上下文 | 跨模块操作 |
| `/memory` | 管理持久化记忆 | 查看/编辑/删除记忆 |
| `/context` | 查看当前上下文详情 | 了解窗口使用情况 |
| `/env` | 查看环境信息 | node 版本、Python 路径等 |

#### 代码操作

| 命令 | 用途 | 常见用法 |
|------|------|---------|
| `/review` | 审查当前 diff | 提交前自查 |
| `/fix` | 自动修复问题 | lint/类型/格式错误 |
| `/test` | 运行测试并分析 | "跑测试看看有没有问题" |
| `/lint` | 运行 linter | 代码风格检查 |
| `/format` | 格式化代码 | 统一代码风格 |

#### Git 与协作

| 命令 | 用途 | 常见用法 |
|------|------|---------|
| `/pr` | 创建 Pull Request | 自动分支→提交→发 PR |
| `/commit` | 生成 commit 并提交 | 自动写 commit message |
| `/branch <name>` | 创建并切换到新分支 | 在分支上开发新功能 |
| `/diff` | 查看当前改动 | 快速看改了什么 |

#### 配置与模型

| 命令 | 用途 | 常见用法 |
|------|------|---------|
| `/model` | 查看/切换模型 | 轻任务换小模型 |
| `/model gpt-5` | 直接切换到指定模型 | 重任务切强模型 |
| `/config` | 打开配置面板 | 调整权限、沙箱、通知 |
| `/sandbox` | 管理沙箱设置 | 开/关/查看沙箱状态 |

#### 子代理与工具

| 命令 | 用途 | 常见用法 |
|------|------|---------|
| `/agents` | 列出可用子代理 | 了解可派发的代理类型 |
| `/delegate <描述>` | 派发任务给子代理 | 并行处理独立任务 |
| `/tools` | 列出可用 MCP 工具 | 查看已连接的扩展工具 |
| `/mcp` | 管理 MCP 服务器 | 添加/移除/查看 |

#### Bash 快捷方式

在对话中用 `!` 前缀直接执行终端命令，不经过 Codex 分析：

```
> !git diff --stat
> !npm ls --depth=0
> !docker ps
```

这在你只想快速查看状态、不需要 AI 分析时非常高效。

### 1.2 启动参数速查

```bash
# 基础
codex                                    # 交互模式
codex .                                  # 指定工作目录

# 一次性任务
codex -p "审查安全性"                    # print 模式，输出后退出
codex -c "修复 lint 错误"               # 带项目上下文执行
codex --command "分析架构"               # 同 -c

# 模型
codex --model gpt-5                      # 指定模型
codex --model gpt-5-mini                 # 轻量模型

# 会话
codex --resume                           # 恢复最近
codex --resume <session-id>              # 恢复指定

# 沙箱
codex --sandbox off                      # 关闭沙箱
codex --no-sandbox                       # 同上

# 配置和更新
codex --config                           # 打开配置面板
codex --update                           # 更新到最新版
codex --version                          # 版本信息
```

## 2. 配置管理实战

### 2.1 配置文件层级

Codex 使用 YAML 格式的配置文件，三层优先级：

```
.codex/config.local.yaml    # 本地覆盖（不提交 git）  最高优先级
.codex/config.yaml          # 项目级（提交 git）      次优先级
~/.codex/config.yaml        # 用户全局                 默认值
```

### 2.2 项目配置模板

#### 日常 Web 开发

```yaml
# .codex/config.yaml
model: gpt-5

permissions:
  auto_approve:
    - Read
    - Bash(git:status,git:diff,git:log,git:branch)
    - Bash(npm:*,npx:*,node:*)
    - Bash(ls:*,find:*,grep:*,cat:*,head:*,tail:*)
    - Bash(docker:ps,docker:logs)
  require_approval:
    - Edit
    - Write
    - Bash(git:push,git:commit,git:merge)
    - Bash(rm:*,mv:*)
    - Bash(curl:*,wget:*)
    - WebFetch

sandbox:
  enabled: true
  auto_approve_in_sandbox:
    - Bash(npm:install,npm:run,npm:test)
    - Bash(npx:*)
    - Bash(node:*)
    - Bash(python:*)
    - Bash(pip:*)

context:
  auto_read:
    - package.json
    - tsconfig.json
    - README.md
    - "src/**/*.ts"
```

#### 信任的本地项目（更宽松）

```yaml
# .codex/config.yaml
model: gpt-5

permissions:
  auto_approve:
    - Read
    - Edit
    - Write
    - Bash(git:*)
    - Bash(npm:*,npx:*,node:*)
    - Bash(ls:*,find:*,grep:*)
    - Bash(docker:*)
    - WebFetch
    - WebSearch
  require_approval:
    - Bash(rm -rf:*)
    - Bash(git push --force:*)
    - Bash(curl:*,wget:*)

sandbox:
  enabled: false  # 信任项目关闭沙箱

context:
  auto_read:
    - package.json
    - tsconfig.json
    - CLAUDE.md
    - CODEX.md
```

#### CI / 自动化（全自动）

```yaml
# .codex/config.yaml
model: gpt-5

permissions:
  auto_approve:
    - Read
    - Edit
    - Write
    - Bash(*)

sandbox:
  enabled: true

execution:
  mode: non-interactive  # 无头模式
  auto_confirm: true      # 自动确认所有操作
```

### 2.3 权限类型速查

| 权限 | 覆盖范围 | 示例配置 |
|------|----------|---------|
| `Read` | 读文件 | `Read(*)` |
| `Edit` | 编辑已有文件 | `Edit(src/**)` |
| `Write` | 创建新文件 | `Write(src/**)` |
| `Bash` | 执行命令 | `Bash(git:*)` |
| `WebFetch` | 抓取网页 | `WebFetch(docs.*)` |
| `WebSearch` | 搜索网页 | `WebSearch(*)` |
| `MCP.*` | MCP 工具 | `MCP.github:*` |

### 2.4 沙箱配置

```yaml
sandbox:
  enabled: true

  # 沙箱中自动批准的 shell 命令
  auto_approve_in_sandbox:
    - Bash(npm:*)     # npm 相关操作自动通过
    - Bash(npx:*)
    - Bash(node:*)
    - Bash(python:*)

  # 沙箱中的文件系统访问
  writable_paths:
    - node_modules/
    - dist/
    - .cache/

  # 网络策略
  network:
    allow_outbound: true
    allowed_hosts:
      - registry.npmjs.org
      - pypi.org
```

## 3. 上下文管理技巧

### 3.1 何时 compact

观察信号：

- Codex 提示"上下文接近上限"
- 回答质量明显下降
- 开始遗漏你前面说过的重要信息
- 相同约束需要反复提醒

**最佳时机**：每完成一个独立任务后立刻 compact，而不是等系统提示。

### 3.2 任务拆分原则

```
Session 1: 探索代码库 → /clear
Session 2: 设计方案 → /clear
Session 3: 实现逻辑 → /clear /compact
Session 4: 补充测试 → /clear
Session 5: Review 修复 → /clear
Session 6: 文档和 PR → /clear
```

每个会话结束时让 Codex 总结进度，把摘要复制保存。下一个会话开始时贴回去即可。

### 3.3 CODEX.md 编写技巧

高效 CODEX.md 的三个原则：**具体、简短、可执行**。

```markdown
# CODEX.md

## 技术栈
FastAPI + SQLAlchemy + PostgreSQL + Redis

## 项目约定
- Python 3.12，用 ruff 格式化
- 所有 public 函数必须有 docstring
- 数据库迁移用 Alembic，不要手动改 schema
- 测试用 pytest + pytest-asyncio

## 当前关注
- 正在从 Flask 迁移到 FastAPI，src/flask_routes/ 是旧代码
- 新代码全部写在 src/api/

## 禁止
- 不要改 alembic/versions/ 下的历史迁移文件
- 不要改 Dockerfile 和 docker-compose.yml
- 不要引入新的 PyPI 依赖，除非必要
```

### 3.4 记忆管理

```bash
# 查看现有记忆
/memory

# 在对话中主动记录
> 记住：我们 API 默认分页是 page_size=20

# 清理过时记忆
> 删除关于 Flask 迁移的记忆，迁移已经完成了
```

### 3.5 图片和文件引用

Codex 支持直接引用图片和文件作为上下文：

```
> 分析这张 UI 截图的问题 @./screenshots/bug.png
> 根据这个设计稿的 PDF @./docs/api-design.pdf 帮我实现 API
```

比纯文本描述高效得多。

## 4. 高效工作流

### 4.1 Code Review 流程

```
# 快速审查
/review                          # 对当前 diff 做审查

# 深度审查
> 对当前改动做一个全面的 code review，重点看：
> 1) 安全漏洞
> 2) 性能隐患
> 3) 边界情况处理
> 4) 是否破坏了现有 API 契约

# 修复发现的问题
> 把刚才提到的所有问题都修了，每个独立问题一个 commit
```

### 4.2 调试工作流

```
# 定位问题
> 订单创建接口返回 500，帮我查看相关日志和代码，逐步定位根因

# 不要直接改逻辑，先加日志
> 先在关键路径上加 debug 日志，复现后分析输出

# 定位后修复
> 根因是 SQLAlchemy session 未正确关闭。帮我修复，并补充对应的测试用例

# 验证
> 跑一遍 order 相关的测试，确认修复有效且没有回归
```

### 4.3 自动修复工作流

```
/fix                             # 一键修复 lint 和类型错误
/lint                            # 只跑 lint 看有哪些问题
/format                          # 统一格式化
```

### 4.4 TDD 工作流

```
> 我要用 TDD 方式给 src/services/payment.py 添加退款功能：
> 1) 先写测试用例
> 2) 确认测试失败
> 3) 实现退款逻辑
> 4) 确认测试通过
> 5) 重构优化
> 每个步骤做完停一下让我确认
```

### 4.5 发 PR 完整流程

```
# 方式一：一键
/pr

# 方式二：分步控制
> 帮我：
> 1) 总结这次所有改动的要点
> 2) 生成规范的 commit message
> 3) 创建 feature/refund-api 分支
> 4) 提交并推送
> 5) 创建 PR，标题和描述写清楚改动内容和测试结果
```

## 5. 常见问题

### Q: Codex 和 Claude Code 选哪个？

A: 两者定位相似，核心差异在底层模型和生态。如果你的团队用 OpenAI API 更多，Codex 集成更顺；如果偏好 Anthropic 生态，Claude Code 更合适。实际很多团队两个都在用，不同任务选不同工具。

### Q: 上下文满了怎么办？

A: 先 `> 总结当前进度和待办` 复制内容，然后 `/compact` 或 `/clear`，新会话贴上摘要继续。

### Q: Codex 开始"犯糊涂"，质量明显下降？

A: 上下文太长导致注意力分散。立即 `/compact`。如果 compact 后还是不行，说明这个任务本身太大了——拆成更小的任务独立处理。

### Q: 沙箱里不能访问某些文件/网络怎么办？

A: 检查 `.codex/config.yaml` 中的 `sandbox.writable_paths` 和 `sandbox.network.allowed_hosts` 配置。也可以用 `/sandbox` 命令临时调整。

### Q: 怎么评估花了多少钱？

A: `/cost` 显示当前会话和累计费用。

### Q: 如何让 Codex 更好地理解我的私有框架？

A: 在 `CODEX.md` 中详细描述框架约定，把核心代码路径加入 `context.auto_read`。

## 6. 速查：每天启动的 5 件事

1. **`/status`** — 上下文是否需要 fresh start
2. **CODEX.md 更新** — 昨天有没有新约定需要记录
3. **`/model` 检查** — 当前任务是否需要更强/更快的模型
4. **权限检查** — 频繁遇到的权限弹窗，今天直接加白名单
5. **一个会话一个主题** — 别混着做

这五件事养成习惯，Codex 会从"可用"变成"高效"。

## 参考资料

- [Codex 官方文档](https://platform.openai.com/docs/guides/codex)
- [OpenAI API 参考](https://platform.openai.com/docs/api-reference)
