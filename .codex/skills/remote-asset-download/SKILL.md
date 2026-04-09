# 技能：remote-asset-download（远程资源本地化）

## 适用场景
- 文章里有大量远程图片/附件链接，需要改为本地托管。

## 输入
- `.github/scripts/download_remotes.py` 的配置项

## 执行步骤
1. 确认扫描目录和支持后缀。
2. 执行下载与替换：
```bash
python3 .github/scripts/download_remotes.py
```
3. 校验本地链接：
```bash
python3 scripts/check_internal_links.py _posts --root .
```

## 输出结果
- 远程资源下载到 `assets/`，Markdown 引用替换为本地路径。

## 失败回退
- 对无法下载的域名保留远程链接，并输出待处理清单。
