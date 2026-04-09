# 技能：markdown-cleanup（Markdown 清理）

## 适用场景
- 文本有行尾空格、空行不稳定、front matter 后空行不统一。

## 输入
- 目标路径（默认 `_posts`）

## 执行步骤
1. 检查模式：
```bash
python3 scripts/markdown_cleanup.py --check _posts
```
2. 应用修复：
```bash
python3 scripts/markdown_cleanup.py _posts
```

## 输出结果
- 统一换行符 `\n`
- 去除行尾空格
- 连续空行最多两行
- front matter 后固定一个空行

## 失败回退
- 对表格/代码块敏感目录可分目录逐步执行。
