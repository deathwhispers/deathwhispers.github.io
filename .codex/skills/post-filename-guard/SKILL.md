# 技能：post-filename-guard（命名与日期守护）

## 适用场景
- 合并前检查
- 批量重命名或日期改写后复核

## 输入
- 目标路径（默认 `_posts`）

## 执行步骤
```bash
python3 scripts/check_post_filenames.py _posts
```

## 输出结果
- 文件名符合 `YYYY-MM-DD-title.md`
- front matter `date` 与文件名前缀一致

## 失败回退
- 若缺失 YAML 头，先执行 `frontmatter-normalize`。
