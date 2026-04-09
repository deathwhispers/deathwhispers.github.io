# 技能：batch-note-intake（新笔记批量接入）

## 适用场景
- 新导入一批笔记，需要一次性标准化并校验。

## 输入
- 目标路径（默认 `_posts`）
- 可选：`--with-date`（启用日期重排）
- 可选：`--seed=...`（日期分布种子）

## 执行步骤
1. 标准接入：
```bash
bash scripts/batch_note_intake.sh _posts
```
2. 接入 + 日期重排：
```bash
bash scripts/batch_note_intake.sh _posts --with-date --seed=notes-v1
```

## 输出结果
- YAML 头标准化
- Markdown 基础格式清理
- 可选日期重分布后命名一致性通过

## 失败回退
- 先按子目录执行，缩小影响面后再全量。
