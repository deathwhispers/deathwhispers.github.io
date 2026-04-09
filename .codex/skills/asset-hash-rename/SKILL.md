# 技能：asset-hash-rename（资源哈希化重命名）

## 适用场景
- 资源命名混乱，想统一为哈希名并便于去重。

## 输入
- `.github/scripts/batch_rename_tool.py` 配置

## 执行步骤
1. 先把脚本中的 `DRY_RUN=True`。
2. 试运行：
```bash
python3 .github/scripts/batch_rename_tool.py
```
3. 确认后改为 `DRY_RUN=False` 再执行。

## 输出结果
- 资源文件名标准化，Markdown 链接同步更新。

## 失败回退
- 先按单目录执行，确认安全后再放大范围。
