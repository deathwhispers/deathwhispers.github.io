#!/usr/bin/env python3
"""输出 Git Diff 中变更的文章 Markdown 文件。"""

from __future__ import annotations

import argparse
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="列出当前变更涉及的文章文件")
    parser.add_argument("--staged", action="store_true", help="仅查看暂存区变更")
    parser.add_argument("--base", default="", help="可选：指定对比基线，如 origin/main")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    cmd = ["git", "diff", "--name-only", "--diff-filter=ACMR"]
    if args.staged:
        cmd.append("--cached")
    if args.base:
        cmd.append(args.base)

    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    posts = [p for p in paths if p.startswith("_posts/") and p.endswith(".md")]

    for p in posts:
        print(p)

    print(f"变更文章数量={len(posts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
