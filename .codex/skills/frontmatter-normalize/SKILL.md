# 技能：frontmatter-normalize（YAML头标准化）

## 适用场景
- 从 Notion / Obsidian / 其他平台导入了新 Markdown。
- YAML 头字段缺失、顺序混乱、格式不一致。

## 输入
- 目标路径（默认 `_posts`）

## 执行步骤
1. 检查模式：
```bash
python3 scripts/frontmatter_standardize.py --check _posts
```
2. 应用修复：
```bash
python3 scripts/frontmatter_standardize.py _posts
```
3. 校验命名日期一致性：
```bash
python3 scripts/check_post_filenames.py _posts
```

## 输出结果
- 每篇文章都具备 `layout/title/date/tags/categories/author`。
- YAML 使用统一 2 空格缩进。

## 失败回退
- 遇到异常 YAML 时，不破坏正文，输出错误后手工处理。
