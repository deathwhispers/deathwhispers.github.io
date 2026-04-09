# 技能：taxonomy-collision-check（分类标签冲突检查）

## 适用场景
- Jekyll 构建提示 `tags/...` 或 `categories/...` 重复输出冲突。
- 你调整了 tags / categories 命名规则。

## 输入
- 目标 Markdown 路径

## 执行步骤
```bash
python3 scripts/check_taxonomy_collisions.py _posts
```

## 输出结果
- 识别 slug 冲突分组，便于统一命名。

## 失败回退
- 将同义词合并或统一大小写（如 `MySQL` / `mysql`）。
