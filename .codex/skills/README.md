# 本地技能目录（中文）

本仓库提供了可直接执行的本地技能，目的是把高频操作固化为稳定流程。

## 一、内容治理类
- `frontmatter-normalize`：统一 YAML 头字段与格式。
- `post-date-redistribute`：按给定时间窗口重排日期并重命名文件。
- `markdown-cleanup`：清理空行、行尾空格与 Front Matter 后空行。
- `post-filename-guard`：校验 `YYYY-MM-DD-title.md` 与 `date` 一致性。
- `internal-link-audit`：检查本地链接与资源引用是否存在。
- `taxonomy-collision-check`：检查标签/分类 slug 冲突。

## 二、流程编排类
- `batch-note-intake`：一条命令处理新导入笔记（标准化 + 校验）。
- `changed-post-scope-check`：快速定位当前分支变更的文章范围。
- `jekyll-guardrails`：执行守门检查，可选完整构建。
- `pr-summary-generator`：自动生成 PR 变更摘要模板。

## 三、同步与资产类
- `notion-sync-pipeline`：Notion 同步后的规范化与验证流水线。
- `remote-asset-download`：下载远程资源并替换为本地链接。
- `asset-hash-rename`：资产哈希化重命名并回写引用。
- `asset-orphan-cleanup`：清理未引用资产。

## 约定
每个技能目录下都有 `SKILL.md`，统一包含：
- 适用场景
- 输入参数
- 执行步骤
- 输出结果
- 失败回退
