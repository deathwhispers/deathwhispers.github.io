# 仓库协作指南

## 1）项目结构
这是一个基于 Jekyll（Chirpy 主题）的博客仓库。
- `_posts/`：文章内容，文件名建议 `YYYY-MM-DD-title.md`
- `_tabs/`：顶部页面（about / tags / categories / archives / navigation）
- `_data/`：站点 YAML 元数据（authors / navigation / contact / links）
- `_plugins/`：Jekyll Ruby 插件（如 `posts-lastmod-hook.rb`）
- `assets/`：图片、附件、模板和工具页
- `.github/workflows/`：CI/CD 工作流
- `.github/scripts/`：已有同步与资源处理脚本
- `scripts/`：本地守护与内容自动化脚本
- `.codex/skills/`：本地技能说明（可重复执行流程）
- `_site/`：构建产物目录（禁止手改）

## 2）常用命令
- 安装依赖：`bundle install`
- 本地预览：`bundle exec jekyll s --livereload`
- 本地构建：`bundle exec jekyll b`
- 生产环境构建：`JEKYLL_ENV=production bundle exec jekyll b`
- Notion 同步：`pip install requests pyyaml pypinyin dotenv && python .github/scripts/sync_notion.py`
``
## 3）Agent 工作模型（Rules / Skills / Subagent）

### 3.1 Rules（硬约束）
P0（必须遵守）：
- 禁止手工修改 `_site/`。
- 禁止提交密钥、凭据、本机绝对路径等敏感信息。
- 文章文件命名必须符合 `YYYY-MM-DD-title.md`。
- 文章 Front Matter 必须包含：`layout`、`title`、`date`、`tags`、`categories`、`author`。

P1（质量门禁）：
- 合并前至少通过：`bash scripts/run_guardrails.sh`
- 发布前建议通过：`bash scripts/run_guardrails.sh --full`
- 涉及日期改写或重命名时，必须执行：`python3 scripts/check_post_filenames.py _posts`

P2（风格规范）：
- YAML 与 Markdown 列表缩进统一 2 空格。
- 资源路径使用 `/assets/images/...` 或 `/assets/files/...`。
- Python 脚本使用 UTF-8，遵循 PEP 8。

### 3.2 Skills（可复用流程）
技能索引见：`.codex/skills/README.md`

新笔记接入推荐顺序：
1. `frontmatter-normalize`（YAML 头标准化）
2. `markdown-cleanup`（Markdown 清理）
3. `post-filename-guard`（命名与日期一致性校验）
4. `internal-link-audit`（内部链接校验）
5. `jekyll-guardrails`（守护检查）

### 3.3 Subagent（子代理）使用策略
只在以下情况使用：
- 任务可并行（如一条线改内容，一条线做校验）。
- 需要风险隔离（如资源重命名与日期重排分开执行）。
- 批量迁移任务，需要明确评审边界。

小范围单文件修改，优先单代理直改。

## 4）内容规范
- Markdown 文章必须带 YAML 头。
- 推荐可选字段：`slug`、`status`、`updated`、`last_modified_at`。
- 中文标题可保留原文，重点保证日期前缀合法。

## 5）验证规范
仓库以“构建优先”验证为主：
- 快速检查：`bash scripts/run_guardrails.sh`
- 完整检查：`bash scripts/run_guardrails.sh --full`
- 可选链接检查：`bundle exec htmlproofer ./_site --disable-external`

## 6）提交与 PR 规范
- 提交信息：简短、祈使语气、建议带范围。
  - 示例：`posts: 规范 masterlearn 笔记 front matter`
- PR 建议包含：
  - 变更内容
  - 关键路径
  - 验证命令
  - 有界面变化时的截图

可用脚本生成 PR 草稿：
- `python3 scripts/generate_pr_summary.py --output /tmp/pr-summary.md`

## 7）安全与配置
- 本地密钥放 `.env`，CI 密钥放 GitHub Secrets。
- Notion 同步依赖：
  - `NOTION_API_KEY`
  - `NOTION_DATABASE_ID`

## 8）本地自动化入口
- `scripts/frontmatter_standardize.py`
- `scripts/check_frontmatter_required.py`
- `scripts/redistribute_post_dates.py`
- `scripts/markdown_cleanup.py`
- `scripts/check_post_filenames.py`
- `scripts/check_internal_links.py`
- `scripts/check_taxonomy_collisions.py`
- `scripts/check_changed_posts.py`
- `scripts/batch_note_intake.sh`
- `scripts/run_guardrails.sh`

## 9）CI 守门
工作流：`.github/workflows/agent-guardrails.yml`
- 在 PR / Push（内容相关路径）时触发。
- 执行完整守门检查并包含 Jekyll 构建。
