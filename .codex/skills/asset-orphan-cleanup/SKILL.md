# 技能：asset-orphan-cleanup（孤儿资源清理）

## 适用场景
- `assets` 膨胀明显，需要清理未被引用文件。

## 输入
- `.github/scripts/assets_cleaner.py` 的 `DRY_RUN` 配置

## 执行步骤
1. 先试运行（`DRY_RUN=True`）：
```bash
python3 .github/scripts/assets_cleaner.py
```
2. 人工确认后执行删除（`DRY_RUN=False`）。
3. 清理后复检：
```bash
python3 scripts/check_internal_links.py _posts --root .
```

## 输出结果
- 删除未引用资源，且文章链接不损坏。

## 失败回退
- 清理前先提交一次，必要时用提交回滚。
