# 技能：jekyll-guardrails（守门检查）

## 适用场景
- 提交前快速质量检查。
- 发布前完整检查（含 Jekyll 构建）。

## 输入
- 检查模式：`quick` 或 `full`

## 执行步骤
1. 快速检查：
```bash
bash scripts/run_guardrails.sh
```
2. 完整检查（含构建）：
```bash
bash scripts/run_guardrails.sh --full
```
3. 全量严格模式（内容治理专项）：
```bash
bash scripts/run_guardrails.sh --all --strict-taxonomy --full
```

## 输出结果
- Python 脚本可编译
- 变更文章的 YAML/命名/链接检查通过
- `--full` 时站点可构建

## 失败回退
- 若失败源于历史存量问题，先定位具体文件再分批修复。
