# 技能：internal-link-audit（内部链接校验）

## 适用场景
- 移动/重命名了文章或资源。
- 发布前检查本地链接是否失效。

## 输入
- 目标 Markdown 路径
- 仓库根路径

## 执行步骤
```bash
python3 scripts/check_internal_links.py _posts --root .
```

## 输出结果
- 无缺失本地链接（文章/图片/附件）。

## 失败回退
- 对已知占位链接先标记处理，再复跑校验。
