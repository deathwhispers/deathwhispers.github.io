---
layout: post
title: Codex 深度进阶：Hooks、自定义命令与自动化流水线
author: deathwhispers
date: 2026-07-13
slug: codex-advanced-hooks-custom-commands-automation
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

前两篇文章覆盖了入门和日常实战。这一篇写给想把 Codex 深度集成到开发体系中的进阶用户——你将学会用 Hooks 自动化工作流、编写自定义命令、配置沙箱策略、将 Codex 嵌入 CI/CD 管线。

## 1. Hooks 系统

Hooks 是 Codex 的事件驱动扩展机制。在 Codex 的生命周期关键节点插入自定义脚本，实现自动化检查和操作。

### 1.1 可用事件

| 事件 | 触发时机 | 典型用途 |
|------|----------|---------|
| `pre_tool_use` | 工具调用**之前** | 校验参数、阻止危险操作 |
| `post_tool_use` | 工具调用**之后** | 结果后处理、自动格式化 |
| `session_start` | 会话启动 | 加载环境、注入上下文 |
| `session_end` | 会话结束 | 自动清理、发送摘要 |
| `pre_compact` | 上下文压缩前 | 保存关键信息 |
| `post_message` | Codex 回复后 | 格式化输出、触发通知 |
| `pre_command` | 用户提交消息前 | 自动补充上下文 |

### 1.2 配置方式

在 `.codex/config.yaml` 中配置：

```yaml
hooks:
  pre_tool_use:
    - matcher: "Bash(*rm*)"
      command: ".codex/hooks/warn-delete.sh"
      on_failure: block    # block | warn | ignore

    - matcher: "Bash(*git push*)"
      command: ".codex/hooks/pre-push-check.sh"
      on_failure: warn

  post_tool_use:
    - matcher: "Edit(*.py)"
      command: "ruff format ${CODEX_TOOL_FILE} > /dev/null 2>&1"

    - matcher: "Edit(*.ts)"
      command: "npx prettier --write ${CODEX_TOOL_FILE} > /dev/null 2>&1"

  session_start:
    - command: ".codex/hooks/session-start.sh"

  session_end:
    - command: ".codex/hooks/session-end.sh"
```

Hook 返回值语义：
- `exit 0` — 成功，继续执行
- `exit 1` — 警告但继续（当 `on_failure: warn` 时）
- `exit 2` — 阻止操作（当 `on_failure: block` 时）

### 1.3 Hook 环境变量

| 变量 | 含义 | 示例 |
|------|------|------|
| `CODEX_TOOL_NAME` | 工具名 | `Edit`, `Bash`, `Read` |
| `CODEX_TOOL_FILE` | 操作的文件路径 | `/project/src/app.py` |
| `CODEX_TOOL_ARGS` | 工具参数（JSON） | `{"command": "npm test"}` |
| `CODEX_SESSION_ID` | 会话 ID | `sess_abc123` |
| `CODEX_PROJECT_DIR` | 项目根目录 | `/Users/me/project` |

### 1.4 实战案例

#### 案例一：拦截危险命令

```bash
#!/bin/bash
# .codex/hooks/warn-delete.sh

COMMAND=$(echo "$CODEX_TOOL_ARGS" | jq -r '.command')

if echo "$COMMAND" | grep -qE 'rm -rf /|rm -rf ~|rm -rf \*'; then
  echo "⛔ 绝对禁止此操作"
  exit 2
fi

if echo "$COMMAND" | grep -q 'rm -rf'; then
  echo "⚠️  检测到递归删除命令：$COMMAND"
  echo "请确认这不会误删重要文件"
fi

exit 0
```

#### 案例二：自动格式化

```yaml
hooks:
  post_tool_use:
    # Python 文件用 ruff 格式化
    - matcher: "Edit(*.py)"
      command: "ruff format ${CODEX_TOOL_FILE} && ruff check --fix ${CODEX_TOOL_FILE}"

    # TypeScript 文件用 prettier
    - matcher: "Edit(*.ts)"
      command: "npx prettier --write ${CODEX_TOOL_FILE}"

    # Go 文件用 gofmt
    - matcher: "Edit(*.go)"
      command: "gofmt -w ${CODEX_TOOL_FILE}"
```

Codex 每编辑一个文件，自动用对应工具格式化，无需在对话中反复提醒。

#### 案例三：会话启动注入动态上下文

```bash
#!/bin/bash
# .codex/hooks/session-start.sh

cat <<EOF
## 当前环境快照
- 分支: $(git branch --show-current 2>/dev/null || echo 'N/A')
- 最新提交: $(git log -1 --oneline 2>/dev/null || echo 'N/A')
- 未暂存改动: $(git diff --name-only 2>/dev/null | wc -l | tr -d ' ') 个文件
- 操作系统: $(uname -s)
- Python: $(python --version 2>&1)
- Node: $(node -v 2>/dev/null || echo 'N/A')
- 时间: $(date '+%Y-%m-%d %H:%M')
EOF
```

每次启动 Codex，自动获得当前环境的完整快照。

#### 案例四：防止敏感文件被读取

```bash
#!/bin/bash
# .codex/hooks/check-sensitive-read.sh

FILE=$(echo "$CODEX_TOOL_ARGS" | jq -r '.file_path // empty')
if [ -z "$FILE" ]; then
  FILE=$(echo "$CODEX_TOOL_ARGS" | jq -r '.paths[0] // empty')
fi

SENSITIVE_PATTERNS="\.env$|\.env\.|credentials|secrets|\.pem$|id_rsa"

if echo "$FILE" | grep -qE "$SENSITIVE_PATTERNS"; then
  echo "⚠️  尝试读取敏感文件: $FILE"
  echo "如果确实需要读取，请在配置中显式允许此文件"
  exit 2
fi

exit 0
```

```yaml
hooks:
  pre_tool_use:
    - matcher: "Read(*)"
      command: ".codex/hooks/check-sensitive-read.sh"
      on_failure: block
```

## 2. 自定义命令

### 2.1 创建自定义命令

在 `.codex/commands/` 目录下创建 `.md` 文件，文件名即命令名：

```markdown
<!-- .codex/commands/deploy-staging.md -->

# 部署到 Staging

执行以下步骤将当前分支部署到 staging 环境：

1. 确认所有测试通过：
   ```bash
   npm test
   ```
2. 构建生产包：
   ```bash
   npm run build
   ```
3. 部署到 staging：
   ```bash
   npm run deploy:staging
   ```
4. 等待部署完成后，运行 smoketest：
   ```bash
   npm run smoketest:staging
   ```
5. 如果 smoketest 通过，输出部署摘要。
   如果失败，立即回滚并报告错误。
```

使用：`/deploy-staging`

### 2.2 带参数的命令

```markdown
<!-- .codex/commands/release.md -->

# 发布版本 $ARGUMENTS

发布版本 $ARGUMENTS，执行以下步骤：

1. 验证参数格式（应为 semver 如 1.2.3）
2. 从最近的提交生成 CHANGELOG
3. 更新 package.json 中的版本号
4. 创建 git tag: v$ARGUMENTS
5. 构建并发布到 npm
6. 推送 tag 到 origin

完成后输出发布摘要。
```

使用：`/release 2.1.0`

### 2.3 多步骤编排命令

```markdown
<!-- .codex/commands/publish-docs.md -->

# 发布文档

执行文档构建和发布的完整流程：

## 步骤一：检查
- 确认 docs/ 目录下有改动
- 确认没有 broken links

## 步骤二：构建
```bash
npm run docs:build
```

## 步骤三：部署
```bash
npm run docs:deploy
```

## 步骤四：验证
- 检查部署后的页面是否可访问
- 抽样检查 3 个页面的内容完整性
```

### 2.4 条件执行命令

```markdown
<!-- .codex/commands/smart-commit.md -->

# 智能提交

基于当前改动自动生成 commit：

1. 如果只有文档改动：使用 `docs:` 前缀
2. 如果有测试文件改动：使用 `test:` 前缀
3. 如果修改了 src/ 下代码：分析改动类型
   - 新功能 → `feat:`
   - Bug 修复 → `fix:`
   - 重构 → `refactor:`
   - 性能 → `perf:`
4. 如果涉及 breaking change：在 body 中标注
5. 提交并显示 commit message 供确认
```

## 3. 沙箱深度配置

### 3.1 沙箱策略精细化

```yaml
sandbox:
  enabled: true

  # 文件系统：只允许写入特定目录
  writable_paths:
    - node_modules/
    - dist/
    - build/
    - .cache/
    - __pycache__/
    - .pytest_cache/

  # 只读路径：只能读不能写
  readonly_paths:
    - ~/.ssh/
    - ~/.aws/
    - ~/.config/

  # 网络：精细化出站规则
  network:
    allow_outbound: true
    allowed_hosts:
      - "*.npmjs.org"
      - "*.pypi.org"
      - "*.github.com"
      - "*.docker.com"
      - "localhost:*"
    blocked_hosts:
      - "*internal.corp.com"   # 阻止内网地址

  # 环境变量：沙箱中可用的变量
  env:
    allow:
      - NODE_ENV
      - PYTHONPATH
      - PATH
      - HOME
    block:
      - AWS_*
      - DATABASE_URL
      - REDIS_URL
      - SECRET_*

  # 资源限制
  resources:
    max_memory_mb: 2048
    max_cpu_seconds: 300
    max_disk_mb: 1024
```

### 3.2 按场景切换沙箱策略

```yaml
# .codex/config.yaml

# 使用 profiles 定义多套配置
profiles:
  # 默认：安全优先
  default:
    sandbox:
      enabled: true
      network:
        allow_outbound: false

  # 前端开发：需要 npm install
  frontend:
    sandbox:
      enabled: true
      writable_paths: [node_modules/, .next/, dist/]
      network:
        allow_outbound: true
        allowed_hosts: ["*.npmjs.org", "*.github.com"]

  # 后端开发：需要数据库连接
  backend:
    sandbox:
      enabled: true
      network:
        allow_outbound: true
        allowed_hosts: ["localhost:*", "*.pypi.org"]

  # CI：完全信任
  ci:
    sandbox:
      enabled: false
```

切换命令：

```bash
codex --profile frontend
codex --profile ci
```

## 4. 多代理编排

### 4.1 子代理类型

| 代理类型 | 特征 | 适用场景 |
|----------|------|---------|
| `explore` | 只读，快速 | 代码探索、搜索、定位 |
| `review` | 只读，深度分析 | 代码审查、安全审计 |
| `implement` | 可读写 | 实现功能、修复 bug |
| `test` | 可读写，聚焦测试 | 写单元测试、集成测试 |
| `general` | 全能 | 复杂多步骤任务 |

### 4.2 并行审查

```
> 同时审查三个模块：
> 1) src/auth/ — 安全审查
> 2) src/api/ — 性能审查
> 3) src/ui/ — 代码质量审查
```

Codex 会同时启动三个子代理，各自独立分析。结果汇总后统一展示。

### 4.3 管道式开发

```
> 按以下流程处理：
> 阶段一：深度分析 src/ 当前架构，输出分析报告
> 阶段二：基于报告，设计模块拆分方案
> 阶段三：评审方案可行性，输出修改建议
> 阶段四：根据评审结果逐模块执行拆分
```

每个阶段独立上下文，干净高效。

### 4.4 用 `/delegate` 派发任务

```
/delegate 全面扫描 src/ 下所有超过 300 行的 Python 文件
/delegate 检查是否有循环依赖，输出依赖图和风险点
/delegate 分析数据库查询是否有 N+1 问题
```

## 5. CI/CD 集成

### 5.1 非交互模式

```bash
# 单次任务
codex -p "审查 PR #42 的改动，列出安全问题" --model gpt-5

# 输出 JSON 用于后续处理
codex -p "分析代码复杂度" --output json

# 限制可用工具
codex -p "跑测试并总结失败原因" \
  --allowed-tools "Bash(npm:test),Bash(npm:run),Read"
```

### 5.2 GitHub Actions 集成

```yaml
# .github/workflows/codex-review.yml
name: Codex PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Codex Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > /tmp/diff.patch

          codex -p "审查以下代码变更。分类输出问题（安全/性能/可维护性），
          每个问题标注严重程度（高/中/低）和具体文件行号：

          $(cat /tmp/diff.patch)" \
            --model gpt-5 \
            --profile ci \
            > review.md

      - name: Post Review
        run: |
          gh pr review ${{ github.event.pull_request.number }} \
            --body-file review.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 5.3 自动修复 CI 失败

```yaml
# .github/workflows/codex-fix.yml
name: Codex Auto-Fix
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  auto-fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Codex Auto Fix
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex -p "CI 失败了。查看最近的测试失败和 lint 错误，自动修复。
          只修复明显的错误（类型错误、lint 违规、测试断言错误），
          不要改变业务逻辑。每个修复一个 commit。" \
            --model gpt-5 \
            --profile ci
```

### 5.4 Git Hook 集成

```bash
#!/bin/bash
# .git/hooks/pre-commit

STAGED=$(git diff --cached --name-only | grep -E '\.(py|ts|tsx|go)$' | tr '\n' ' ')

if [ -z "$STAGED" ]; then
  exit 0
fi

echo "Codex 正在检查暂存文件..."

RESULT=$(codex -p "检查这些暂存文件的改动，只输出有问题的部分：
$STAGED。如果没有明显问题，输出 'PASS'" \
  --model gpt-5-mini \
  --profile ci 2>&1)

if [ "$RESULT" != "PASS" ] && ! echo "$RESULT" | grep -q "PASS"; then
  echo "⚠️  Codex 发现以下问题："
  echo "$RESULT"
  echo ""
  read -p "是否继续提交？(y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

exit 0
```

### 5.5 Docker 化运行

```dockerfile
FROM node:20-slim

RUN npm install -g @openai/codex

WORKDIR /workspace

ENTRYPOINT ["codex"]
```

```bash
# 构建
docker build -t codex-runner -f Dockerfile.codex .

# 运行
docker run --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd):/workspace \
  -v ~/.codex/config.yaml:/root/.codex/config.yaml \
  codex-runner -p "审查代码安全性" --profile ci
```

## 6. 完整配置参考

```yaml
# ~/.codex/config.yaml — 用户全局配置

model: gpt-5
theme: dark

permissions:
  auto_approve:
    - Read
    - Bash(git:status,git:diff,git:log)
  require_approval:
    - Edit
    - Write
    - Bash(*)
    - WebFetch

sandbox:
  enabled: true

hooks:
  session_start:
    - command: "echo 'Codex Ready'"

context:
  max_file_size_mb: 2
  exclude_patterns:
    - "node_modules/**"
    - "dist/**"
    - ".git/**"
    - "*.min.js"
    - "*.lock"

ui:
  show_tool_calls: true
  compact_on_idle_minutes: 30
```

```yaml
# .codex/config.yaml — 项目级配置（提交 git）

model: gpt-5

permissions:
  auto_approve:
    - Read
    - Edit(src/**)
    - Write(src/**)
    - Bash(git:status,git:diff,git:log,git:branch,git:add)
    - Bash(npm:*,npx:*,node:*)
    - Bash(ls:*,find:*,grep:*)
  require_approval:
    - Bash(git:push,git:commit)
    - Bash(rm:*,mv:*)
    - WebFetch

hooks:
  post_tool_use:
    - matcher: "Edit(*.ts)"
      command: "npx prettier --write ${CODEX_TOOL_FILE}"
    - matcher: "Edit(*.tsx)"
      command: "npx prettier --write ${CODEX_TOOL_FILE}"

sandbox:
  enabled: true
  writable_paths:
    - node_modules/
    - dist/
    - .next/
  network:
    allowed_hosts: ["*.npmjs.org"]

context:
  auto_read:
    - package.json
    - tsconfig.json
    - CODEX.md
```

## 7. Codex vs Claude Code 进阶能力对比

| 能力 | Codex | Claude Code |
|------|-------|-------------|
| 配置文件格式 | YAML | JSON |
| 项目上下文文件 | `CODEX.md` | `CLAUDE.md` |
| Hooks 事件数 | 7 种 | 8 种 |
| 沙箱执行 | 默认开启，可精细配置 | 可选，通过 settings 控制 |
| 子代理类型 | explore/review/implement/test | explore/review/plan/general-purpose |
| 自定义命令 | `.codex/commands/*.md` | `.claude/commands/*.md` |
| Skills | 不支持独立 skill 体系 | 支持 `.claude/skills/*.md` |
| Worktree 隔离 | 通过沙箱实现 | 原生 git worktree 支持 |
| Workflow 脚本 | 不支持 | 支持 JS 编排脚本 |
| 记忆系统 | `.codex/memory/` | `.claude/memory/` |
| 多代理编排 | `/delegate` + 子代理 | Agent/Workflow + 子代理 |
| CI 模式 | `--profile ci` + 非交互 | `-p` + 非交互 |

## 8. 小结

Codex 的进阶能力围绕三个核心：

1. **Hooks** — 事件驱动的自动化检查、格式化、安全拦截
2. **自定义命令** — 把重复性操作流程固化为 `/` 命令
3. **沙箱 + 多代理 + CI/CD** — 从本地工具升级为团队基础设施

这三个维度叠加，Codex 不再只是"对话写代码"，而是融入了你整个软件开发的生命周期。

## 参考资料

- [Codex 官方文档](https://platform.openai.com/docs/guides/codex)
- [OpenAI API 参考](https://platform.openai.com/docs/api-reference)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
