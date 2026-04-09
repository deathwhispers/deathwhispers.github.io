# 技能：post-date-redistribute（日期重分布）

## 适用场景
- 需要把一批文章日期分散到固定时间区间。
- 需要同时改 `front matter date` 和文件名前缀日期。

## 输入
- 目标目录
- 起止月份（`YYYY-MM`）
- 随机种子 `--seed`
- 可选窗口映射 `scripts/config/date_windows.yml`

## 执行步骤
1. 预览计划：
```bash
python3 scripts/redistribute_post_dates.py _posts \
  --start 2021-09 --end 2024-04 \
  --seed notes-v1 \
  --window-map scripts/config/date_windows.yml
```
2. 真正执行：
```bash
python3 scripts/redistribute_post_dates.py _posts \
  --start 2021-09 --end 2024-04 \
  --seed notes-v1 \
  --window-map scripts/config/date_windows.yml \
  --apply
```
3. 结果校验：
```bash
python3 scripts/check_post_filenames.py _posts
```

## 输出结果
- 文件名前缀日期与 `date` 字段一致。
- 同一 seed 下结果稳定可复现。

## 失败回退
- 重名冲突时自动追加 `-2`、`-3` 后缀。
