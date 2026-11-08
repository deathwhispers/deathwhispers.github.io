#!/usr/bin/env python3
"""检查 Markdown 内部链接是否存在。

规则：
- 忽略外部链接（http/https/mailto/tel/data/javascript）
- 相对路径按当前文件目录解析
- 绝对路径（/xxx）按仓库根目录解析
- 文章永久链接（/posts/年/月/日/slug/）按文章 front matter 的 slug 与 date 校验
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlsplit

LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|\[[^\]]*\]\(([^)]+)\)")
IGNORE_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
POST_PERMALINK_RE = re.compile(r"^/posts/(\d{4})/(\d{2})/(\d{2})/([^/]+)/?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查文章内部链接是否失效")
    parser.add_argument("paths", nargs="*", default=["_posts"], help="待检查文件或目录")
    parser.add_argument("--root", default=".", help="仓库根目录")
    return parser.parse_args()


def iter_md(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix.lower() == ".md":
            out.append(p)
        elif p.is_dir():
            out.extend(sorted(p.rglob("*.md")))
    return out


def parse_frontmatter(text: str) -> dict[str, str]:
    """提取 front matter 中的 slug 与 date（仅保留 YYYY-MM-DD 部分）。"""
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for key in ("slug", "date"):
        mm = re.search(rf"^{key}:\s*(.+)$", m.group(1), re.M)
        if mm:
            fm[key] = mm.group(1).strip().strip("\"'")
    return fm


def build_permalink_index(root: Path) -> dict[str, set[str]]:
    """建立 slug -> 日期前缀集合，用于校验 /posts/... 永久链接。"""
    index: dict[str, set[str]] = {}
    posts_dir = root / "_posts"
    if not posts_dir.is_dir():
        return index
    for md in posts_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        slug = fm.get("slug")
        date = fm.get("date", "")
        if slug:
            index.setdefault(slug, set()).add(date[:10])
    return index


def strip_title_part(raw_target: str) -> str:
    target = raw_target.strip().strip("<>")
    if " " in target and '"' in target:
        target = target.split(" ", 1)[0]
    return target


def resolve_target(md_file: Path, target: str, root: Path) -> Path | None:
    if target.startswith("#"):
        return None

    parsed = urlsplit(target)
    if parsed.scheme in IGNORE_SCHEMES:
        return None
    if parsed.scheme:
        # 例如 en-resource:// 这种非本地协议，直接跳过
        return None

    path_part = parsed.path
    if not path_part:
        return None

    if path_part.startswith("/"):
        return (root / path_part.lstrip("/")).resolve()
    return (md_file.parent / path_part).resolve()


def check_file(path: Path, root: Path, permalink_index: dict[str, set[str]]) -> list[str]:
    issues: list[str] = []
    content = path.read_text(encoding="utf-8")
    for line_no, line in enumerate(content.splitlines(), start=1):
        for match in LINK_RE.finditer(line):
            raw = match.group(1) or match.group(2)
            target = strip_title_part(raw)

            permalink = POST_PERMALINK_RE.match(target)
            if permalink:
                year, month, day, slug = permalink.groups()
                if f"{year}-{month}-{day}" not in permalink_index.get(slug, set()):
                    issues.append(f"缺失链接: {path}:{line_no} -> {target}")
                continue

            resolved = resolve_target(path, target, root)
            if resolved is None:
                continue
            if not resolved.exists():
                issues.append(f"缺失链接: {path}:{line_no} -> {target}")
    return issues


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    files = iter_md(args.paths)
    permalink_index = build_permalink_index(root)

    issues: list[str] = []
    for f in files:
        issues.extend(check_file(f, root, permalink_index))

    for issue in issues:
        print(issue)

    print(f"检查文件数={len(files)} 问题数={len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
