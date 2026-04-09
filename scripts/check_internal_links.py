#!/usr/bin/env python3
"""检查 Markdown 内部链接是否存在。

规则：
- 忽略外部链接（http/https/mailto/tel/data/javascript）
- 相对路径按当前文件目录解析
- 绝对路径（/xxx）按仓库根目录解析
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlsplit

LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|\[[^\]]*\]\(([^)]+)\)")
IGNORE_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}


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


def check_file(path: Path, root: Path) -> list[str]:
    issues: list[str] = []
    content = path.read_text(encoding="utf-8")
    for line_no, line in enumerate(content.splitlines(), start=1):
        for match in LINK_RE.finditer(line):
            raw = match.group(1) or match.group(2)
            target = strip_title_part(raw)
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

    issues: list[str] = []
    for f in files:
        issues.extend(check_file(f, root))

    for issue in issues:
        print(issue)

    print(f"检查文件数={len(files)} 问题数={len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
