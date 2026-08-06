---
layout: post
title: Claude Code 深度进阶：Hooks、技能与多代理编排
author: deathwhispers
date: 2026-06-12
slug: claude-code-advanced-hooks-skills-workflows
categories:
- AI
- General
tags:
- AI
- ClaudeCode
- Tools
status: published
---

前两篇文章覆盖了入门和日常实战。这一篇面向想把 Claude Code 深度集成到开发体系中的进阶用户——你将学会用 Hooks 自动化流程、编写自定义技能、实现并行多代理编排、以及把 Claude Code 嵌入 CI/CD 管线。

## 1. Hooks 系统：把 Claude Code 变成可编程平台

Hooks 是 Claude Code 最强大的扩展机制。它让你在 Claude Code 的生命周期事件中插入自定义脚本——相当于给你的 AI 助手装上传感器和触发器。

### 1.1 可用事件类型

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `PreToolUse` | 任何工具调用**之前** | 校验参数、阻止危险操作、日志记录 |
| `PostToolUse` | 任何工具调用**之后** | 结果二次处理、自动格式化、告警 |
| `Notification` | Claude Code 发出通知时 | 桌面通知转发、IM 消息推送 |
| `SessionStart` | 会话启动时 | 加载环境变量、预热缓存、检查更新 |
| `SessionEnd` | 会话结束时 | 自动提交、清理临时文件、发送摘要 |
| `PreCompact` | 上下文压缩**之前** | 保存压缩前的关键信息 |
| `PrePromptSubmit` | 用户提交 prompt **之前** | 自动补充上下文、注入环境信息 |
| `PostPromptSubmit` | Claude 回复**之后** | 自动格式化输出、提取关键结论 |

### 1.2 配置文件结构

在 `.claude/settings.json` 中配置 hooks：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(*rm*)",
        "command": "echo '⚠️ 警告：即将执行删除命令' && exit 0"
      },
      {
        "matcher": "Bash(git push*)",
        "command": "./.claude/hooks/pre-push-check.sh"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts)",
        "command": "npx prettier --write ${CLAUDE_TOOL_FILE_PATH}"
      }
    ],
    "SessionStart": [
      {
        "command": "./.claude/hooks/session-start.sh"
      }
    ]
  }
}
```

Hook 脚本的退出码决定行为：
- `exit 0` — 继续执行
- `exit 2` — 阻止当前操作（仅 PreToolUse）
- 其他非零 — 显示警告但继续

### 1.3 实战案例

#### 案例一：阻止危险命令

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(*rm -rf*)",
        "command": "echo '此操作被 hook 阻止' && exit 2"
      },
      {
        "matcher": "Bash(*git push --force*)",
        "command": "echo '禁止 force push 到 main/master' && exit 2"
      }
    ]
  }
}
```

#### 案例二：自动格式化编辑过的文件

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts)",
        "command": "npx prettier --write ${CLAUDE_TOOL_FILE_PATH} > /dev/null 2>&1"
      },
      {
        "matcher": "Edit(*.py)",
        "command": "black ${CLAUDE_TOOL_FILE_PATH} > /dev/null 2>&1"
      }
    ]
  }
}
```

每次 Claude Code 编辑 TypeScript 文件后，prettier 自动格式化，不需要在对话里反复提醒。

#### 案例三：会话启动时注入动态上下文

```bash
#!/bin/bash
# .claude/hooks/session-start.sh

echo "## 当前环境"
echo "- 分支: $(git branch --show-current)"
echo "- 最近提交: $(git log -1 --oneline)"
echo "- 未提交文件: $(git diff --name-only | head -5)"
echo "- Node: $(node -v)"
echo "- 当前时间: $(date)"
```

每次会话启动，Claude Code 自动获得当前环境快照。

#### 案例四：提交前自动检查

```bash
#!/bin/bash
# .claude/hooks/pre-commit-check.sh

# 只有 main 分支需要额外检查
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
  echo "✅ 非 main 分支，跳过检查"
  exit 0
fi

# 检查是否包含 TODO
if git diff --cached | grep -q "TODO"; then
  echo "⚠️ 提交包含 TODO，请确认是否继续"
  exit 1
fi

echo "✅ 提交检查通过"
```

### 1.4 Hook 环境变量

Hook 脚本中可以访问以下环境变量：

| 变量 | 含义 | 示例 |
|------|------|------|
| `CLAUDE_TOOL_NAME` | 被调用的工具名 | `Edit`, `Bash`, `Read` |
| `CLAUDE_TOOL_FILE_PATH` | 操作的文件路径 | `/Users/me/project/src/app.ts` |
| `CLAUDE_TOOL_INPUT` | 工具调用参数（JSON） | `{"command": "npm test"}` |
| `CLAUDE_SESSION_ID` | 当前会话 ID | `abc123-def456` |

利用这些变量可以写出精确匹配的 hook 逻辑。

## 2. 自定义 Slash Commands

除了内置命令，你还可以创建自己的 `/` 命令。

### 2.1 快速创建

在 `.claude/commands/` 目录下添加 `.md` 文件，文件名就是命令名：

```markdown
<!-- .claude/commands/deploy-staging.md -->

## 部署到 Staging

1. 先跑一遍完整的测试套件
2. 如果通过，构建并部署到 staging 环境：
   ```bash
   npm run build
   npm run deploy:staging
   ```
3. 部署完成后，运行 staging 环境的冒烟测试
4. 把部署结果总结成一条 Slack 消息（用 MCP slack 工具）
```

使用：`/deploy-staging`

### 2.2 带参数的命令

命令文件可以通过 `$ARGUMENTS` 接收参数：

```markdown
<!-- .claude/commands/release.md -->

## 发布版本 $ARGUMENTS

$ARGUMENTS 是用户传入的版本号。请执行以下步骤：

1. 更新 package.json 版本号为 $ARGUMENTS
2. 更新 CHANGELOG.md（基于最近的提交自动生成）
3. 创建 tag: v$ARGUMENTS
4. 推送到远程仓库
```

使用：`/release 1.5.0`

## 3. 技能体系（Skills）

Skill 是比 slash command 更强大的扩展——它是一套完整的行为规则，可以改变 Claude Code 对特定任务的处理方式。

### 3.1 什么是 Skill

Skill 本质是一个 Markdown 文件，放在 `.claude/skills/` 目录下，包含：
- **指令**：告诉 Claude 遇到什么情况时使用这个 skill
- **工作流**：处理这类任务的步骤和方法
- **约束**：硬性规则和边界

### 3.2 编写一个自定义 Skill

```markdown
<!-- .claude/skills/database-migration.md -->

---
name: database-migration
description: 数据库迁移操作的专用技能，确保安全性
---

## 触发条件
当用户提到以下关键词时自动激活：
- "数据库迁移"、"schema 变更"、"prisma migrate"
- "添加表"、"添加字段"、"修改字段类型"

## 工作流

### 第一步：分析影响范围
1. 读取 prisma/schema.prisma，理解现有结构
2. 确定变更是否涉及数据丢失（如删除列、修改类型）
3. 列出所有受影响的查询和 API 端点

### 第二步：生成迁移计划
1. 写出完整的 schema 变更
2. 如果有数据迁移需求，写出数据迁移脚本
3. 评估回滚方案

### 第三步：安全检查
1. 确认变更不违反数据保护策略
2. 确认迁移不会锁表导致生产中断
3. 如有风险项，必须显式标注并要求人工确认

## 硬性规则
- 永远不要直接修改生产数据库
- 迁移前必须在 staging 环境验证
- 必须生成 rollback 方案
- 涉及数据删除的操作必须二次确认
```

### 3.3 Skill 的触发机制

Skill 可以通过三种方式触发：

1. **自动触发**：Claude Code 扫描 skill 的 `description` 和触发条件，匹配上下文时自动激活
2. **手动调用**：`/skill database-migration` 或通过 Skill 工具调用
3. **关键词匹配**：当用户在对话中提到 skill 描述的关键词

### 3.4 Skill vs Hook vs Slash Command

| 维度 | Hook | Slash Command | Skill |
|------|------|--------------|-------|
| 触发方式 | 事件驱动（自动） | 用户手动 | 自动/手动 |
| 执行内容 | Shell 脚本 | Markdown 指令 | 完整工作流规则 |
| 改变 Claude 行为 | 间接（通过拦截） | 一次性指令 | 持续性行为修改 |
| 适用场景 | 自动化、安全检查 | 重复性操作流程 | 领域专精任务 |

三者可以组合使用：用 Skill 定义数据库迁移规范，用 Hook 在每次 schema 变更时自动校验，用 Slash Command 一键触发标准迁移流程。

## 4. Worktree 隔离：并行任务互不干扰

### 4.1 什么是 Worktree

Git Worktree 允许同一个仓库同时存在多个工作目录，每个对应一个独立分支。Claude Code 的 worktree 功能基于此实现"任务隔离"——每个子代理在独立的工作目录中运行，互不干扰。

### 4.2 使用场景

- **并行开发多个功能**：每个功能给一个子代理，各自在独立 worktree 里操作
- **尝试高风险重构**：不确定是否可行？在 worktree 中尝试，坏了不污染主工作区
- **代码审查**：子代理在 worktree 中检出 PR 分支做审查，不影响你的工作

### 4.3 启用 Worktree 隔离

在对话中直接要求：

```
> 在 worktree 中尝试把 express 替换成 fastify，先别动我的主工作区
```

或在 `Agent` 工具调用中指定：

```
> 派一个子代理在隔离环境中审查 src/auth/ 模块的安全性
```

Claude Code 会自动创建临时的 git worktree，代理在其中操作。完成后：
- 如果代理有改动：worktree 保留，你可以检查并合并
- 如果代理只读分析：worktree 自动清理

### 4.4 手动管理 Worktree

```
> 创建一个 worktree 分支叫 experiment/new-router
> 切换到 worktree

# 完成后
> 退出 worktree，保留改动
> 退出 worktree，删除（抛弃实验）
```

## 5. 多代理编排

当任务量超出单次对话能力时，多代理编排可以让多个 Claude Code 实例并行工作。

### 5.1 基础并行

派发多个独立子代理同时执行：

```
> 同时做三件事：
> 1) 审查 src/auth/ 的安全性
> 2) 审查 src/api/ 的性能
> 3) 审查 src/ui/ 的代码风格
```

Claude Code 会同时启动三个子代理，各自阅读不同代码区域，互不等待。

### 5.2 子代理类型选择

| 代理类型 | 适合任务 | 特点 |
|----------|----------|------|
| `general-purpose` | 通用编程任务 | 全面但可能不够聚焦 |
| `Explore` | 代码探索和研究 | 只读、快速，适合"找东西" |
| `Plan` | 方案设计 | 只设计不实现，先出方案再讨论 |
| `claude-code-guide` | 回答 Claude Code 本身的问题 | "这个配置能怎么优化" |

### 5.3 管道式编排

复杂任务拆成多个阶段，每个阶段的输出是下一阶段的输入：

```
> 执行一个三阶段开发流程：
> 阶段一：全面分析 src/ 当前架构，输出架构分析报告
> 阶段二：基于报告设计重构方案
> 阶段三：评审方案并给出改进建议
```

Claude Code 会依次执行，每个阶段独立上下文，后续阶段只需阅读前阶段的输出摘要即可。

### 5.4 Workflow 脚本：批量处理

对于大规模批量任务（如迁移、审计、全面梳理），可以用 Workflow 脚本：

```
> 使用 workflow，遍历 src/ 下所有超过 200 行的 TypeScript 文件，
> 每个文件分析：职责是否单一、是否存在循环依赖、是否有未覆盖的边界情况
```

Workflow 的 `pipeline` 模式让每个文件走完"分析→修→验证"全流程再处理下一个，不需要等所有文件都分析完才开始修。

## 6. settings.json 完整参考

### 6.1 三层配置互补

```
~/.claude/settings.json            # 用户全局默认
project/.claude/settings.json      # 项目级，提交 git，团队共享
project/.claude/settings.local.json # 本地覆盖，不提交 git
```

合并规则：高优先级覆盖低优先级，数组字段是替换而非合并。

### 6.2 完整配置示例

```json
{
  "model": "sonnet",
  "theme": "dark",
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Write(*)",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(npx:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(*rm*)",
        "command": "./.claude/hooks/warn-delete.sh"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts)",
        "command": "npx prettier --write ${CLAUDE_TOOL_FILE_PATH}"
      }
    ],
    "SessionStart": [
      {
        "command": "./.claude/hooks/inject-context.sh"
      }
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  },
  "env": {
    "NODE_ENV": "development",
    "VERBOSE": "false"
  }
}
```

### 6.3 关键配置项

| 配置 | 说明 | 建议值 |
|------|------|--------|
| `model` | 默认模型 | `"sonnet"` 日常，`"opus"` 复杂任务 |
| `theme` | 主题 | `"dark"` / `"light"` |
| `promptCaching` | 启用 prompt 缓存 | `true`（省钱，默认开启） |
| `sandbox` | Bash 命令沙箱模式 | 默认开启，不要关 |

## 7. CI/CD 集成

### 7.1 非交互模式

Claude Code 支持在 CI 中无头运行：

```bash
# 单次任务模式（-p print，输出后退出）
claude -p "审查这次 PR 的改动，按严重性列出安全问题" --model opus

# 带文件的上下文
claude -p "检查 package.json 依赖是否有已知漏洞" --allowedTools "Bash(npm audit)"

# 完全非交互
claude -p "..." --output-format json --model sonnet
```

### 7.2 GitHub Actions 集成

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          DIFF=$(git diff origin/${{ github.base_ref }}...HEAD)
          claude -p "审查以下代码改动，按安全、性能、可维护性分类输出建议：

          $DIFF" --model opus > review.md

      - name: Post Review Comment
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body-file review.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 7.3 Git Hook 集成

在 `.git/hooks/pre-commit` 中调用 Claude Code 做提交前检查：

```bash
#!/bin/bash
# 只检查暂存区的文件
STAGED=$(git diff --cached --name-only | grep -E '\.(ts|tsx)$' | tr '\n' ' ')

if [ -z "$STAGED" ]; then
  exit 0
fi

claude -p "检查这些文件的暂存改动有没有明显的安全问题和逻辑错误：$STAGED。只需要输出有问题的部分，没问题就说 'PASS'" --model haiku
```

## 8. 团队级配置管理

### 8.1 推荐的团队配置结构

```
project/
├── .claude/
│   ├── settings.json           # 团队共享配置（提交 git）
│   ├── settings.local.json     # 个人覆盖（.gitignore）
│   ├── hooks/
│   │   ├── pre-push-check.sh
│   │   └── inject-context.sh
│   ├── commands/
│   │   ├── deploy-staging.md
│   │   └── release.md
│   └── skills/
│       ├── database-migration.md
│       └── code-review.md
├── CLAUDE.md                   # 项目上下文（提交 git）
└── .gitignore                  # 包含 .claude/settings.local.json
```

### 8.2 团队配置策略

- **`CLAUDE.md`**：提交 git，记录项目技术栈、编码约定、目录结构。全团队共享。
- **`settings.json`**：提交 git，定义共享的权限基线、hooks、MCP 服务器。不含敏感信息。
- **`settings.local.json`**：不提交，个人敏感路径、本地特殊配置。
- **`hooks/` 和 `commands/`**：提交 git，团队共享的自动化流程。

### 8.3 安全隔离

高风险项目可以配置严格限制：

```json
{
  "permissions": {
    "allow": [
      "Read(*)"
    ],
    "deny": [
      "Bash(*)",
      "Edit(*.env*)",
      "Write(*.env*)",
      "WebFetch(*)"
    ]
  }
}
```

只允许读取，任何写入和执行都需要手动确认。适合做代码审查和安全审计场景。

## 9. 一个完整的进阶工作流示例

把上面所有能力串起来，这是一个"需求到上线的全自动流"：

```
Session 1: 需求分析
> 用 CLAUDE.md 里的项目上下文，帮我分析这个需求的技术方案

Session 2: 并行实现
> 派 3 个子代理：
> 1) 在 worktree 中实现 API 层
> 2) 在 worktree 中实现 UI 组件
> 3) 写集成测试
> 三者都完成后，把结果合并到当前分支

Session 3: 质量门禁
> 对合并后的代码执行：
> 1) /review --effort high
> 2) /security-review
> 3) Hook 自动格式化所有编辑过的文件
> 把发现的问题全部修复

Session 4: 发布
> 1) 生成 CHANGELOG
> 2) 走 /release 命令发布版本
> 3) CI 中的 Claude Code review 自动通过后合并

Post-Release:
> ProcessNotification hook 把部署结果推送到 Slack #deployments 频道
```

## 10. 小结

Claude Code 的进阶能力本质上是在做三件事：

1. **自动化**（Hooks）— 把重复的检查、格式化、环境注入交给事件驱动脚本
2. **专业化**（Skills + Slash Commands）— 把领域知识和流程固化，让 AI 的行为更精准
3. **规模化**（Worktree + 多代理 + CI/CD）— 突破单会话的限制，让 AI 能力融入开发管线

这三层能力逐级叠加，最终把 Claude Code 从一个"终端对话工具"变成"团队开发基础设施"。

## 参考资料

- [Claude Code Hooks 文档](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Claude Code Settings 参考](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Claude Code CI/CD 集成](https://docs.anthropic.com/en/docs/claude-code/headless)
- [Model Context Protocol](https://modelcontextprotocol.io)
