# 技能：pr-summary-generator（PR摘要生成）

## 适用场景
- 需要快速产出结构化 PR 描述。

## 输入
- 工作区 diff 或暂存区 diff

## 执行步骤
1. 基于当前工作区：
```bash
python3 scripts/generate_pr_summary.py --output /tmp/pr-summary.md
```
2. 基于暂存区：
```bash
python3 scripts/generate_pr_summary.py --staged --output /tmp/pr-summary.md
```

## 输出结果
- 自动生成：状态统计、路径统计、文件清单、验证清单。

## 失败回退
- 变更过大时先只按暂存区生成，分批提交。
