# 技能：notion-sync-pipeline（Notion 同步流水线）

## 适用场景
- 从 Notion 同步到 `_posts` 与 `assets` 后，需要自动规范化与校验。

## 输入
- 环境变量：`NOTION_API_KEY`、`NOTION_DATABASE_ID`

## 执行步骤
1. 安装依赖：
```bash
pip install requests pyyaml pypinyin dotenv
```
2. 执行同步：
```bash
python3 .github/scripts/sync_notion.py
```
3. 规范化与守门：
```bash
python3 scripts/frontmatter_standardize.py _posts
bash scripts/run_guardrails.sh
```

## 输出结果
- 同步后的内容可直接用于站点构建。

## 失败回退
- 遇到 API 限流/网络问题，重试一次并保留未暂存结果人工检查。
