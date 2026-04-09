#!/usr/bin/env python3
"""Markdown 基础格式清理脚本。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n?", re.S)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="清理 Markdown 基础格式")
    parser.add_argument("paths", nargs="*", default=["_posts"], help="待处理文件或目录")
    parser.add_argument("--check", action="store_true", help="仅检查，不写入")
    return parser.parse_args()


def iter_md(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix.lower() == ".md":
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
    return files


def cleanup_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = [ln.rstrip() for ln in text.split("\n")]
    cleaned = "\n".join(lines)

    # 最多保留连续两行空行
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # front matter 后固定留一个空行
    fm = FRONT_MATTER_RE.match(cleaned)
    if fm:
        start = fm.group(0)
        rest = cleaned[fm.end() :].lstrip("\n")
        cleaned = start.rstrip("\n") + "\n\n" + rest

    cleaned = cleaned.rstrip("\n") + "\n"
    return cleaned


def main() -> int:
    args = parse_args()
    files = iter_md(args.paths)
    changed = 0

    for p in files:
        old = p.read_text(encoding="utf-8")
        new = cleanup_text(old)
        if new != old:
            changed += 1
            if args.check:
                print(f"需要清理: {p}")
            else:
                p.write_text(new, encoding="utf-8")
                print(f"已更新: {p}")

    mode = "检查模式" if args.check else "执行模式"
    print(f"[{mode}] 扫描={len(files)} 变更={changed}")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
