# 技能：changed-post-scope-check（变更范围识别）

## 适用场景
- 希望快速知道当前分支改了哪些文章。
- 想做“只针对变更文件”的检查。

## 输入
- 工作区变更或暂存区变更

## 执行步骤
1. 查看工作区变更文章：
```bash
python3 scripts/check_changed_posts.py
```
2. 仅看暂存区：
```bash
python3 scripts/check_changed_posts.py --staged
```
3. 按变更范围跑守门：
```bash
bash scripts/run_guardrails.sh
```

## 输出结果
- 快速列出变更文章清单。

## 失败回退
- 若输出为空但你确认有改动，使用 `--base origin/main` 显式对比。
