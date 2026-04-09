#!/usr/bin/env python3
"""根据 Git 变更生成中文 PR 摘要。"""

from __future__ import annotations

import argparse
import subprocess
from collections import Counter
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 PR 摘要 Markdown")
    parser.add_argument("--staged", action="store_true", help="仅统计暂存区变更")
    parser.add_argument("--output", help="输出文件路径")
    return parser.parse_args()


def git_diff_name_status(staged: bool) -> list[tuple[str, str]]:
    cmd = ["git", "diff", "--name-status"]
    if staged:
        cmd.append("--cached")
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()

    rows: list[tuple[str, str]] = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 2:
            status = parts[0]
            path = parts[-1]
            rows.append((status, path))
    return rows


def build_summary(rows: list[tuple[str, str]]) -> str:
    if not rows:
        return "## 变更摘要\n\n当前没有检测到文件变更。\n"

    status_counter = Counter(status for status, _ in rows)
    dir_counter = Counter()

    for _, path in rows:
        p = Path(path)
        top = p.parts[0] if p.parts else "(root)"
        dir_counter[top] += 1

    lines: list[str] = []
    lines.append("## 变更摘要")
    lines.append("")
    lines.append("### 按状态统计")
    for status, count in sorted(status_counter.items()):
        lines.append(f"- {status}: {count}")

    lines.append("")
    lines.append("### 按顶层目录统计")
    for directory, count in sorted(dir_counter.items()):
        lines.append(f"- `{directory}`: {count}")

    lines.append("")
    lines.append("### 文件清单")
    for status, path in rows:
        lines.append(f"- `{status}` {path}")

    lines.append("")
    lines.append("### 验证清单")
    lines.append("- [ ] `bash scripts/run_guardrails.sh`")
    lines.append("- [ ] `bundle exec jekyll b`")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    rows = git_diff_name_status(staged=args.staged)
    text = build_summary(rows)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"已写入: {args.output}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
