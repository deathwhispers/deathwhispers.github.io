#!/usr/bin/env python3
"""检查 Front Matter 必填字段与日期格式。"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)
REQUIRED = ["layout", "title", "date", "tags", "categories", "author"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查文章 YAML 头是否满足必填字段")
    parser.add_argument("paths", nargs="+", help="待检查的 Markdown 文件或目录")
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


def parse_date(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (date, datetime)):
        return True
    text = str(value).strip()
    if not text:
        return False
    text = text.split("T", 1)[0].split(" ", 1)[0]
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def check(path: Path) -> list[str]:
    issues: list[str] = []
    content = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(content)
    if not m:
        return [f"缺少YAML头: {path}"]

    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception as exc:
        return [f"YAML解析失败: {path} -> {exc}"]

    if not isinstance(data, dict):
        return [f"YAML头不是对象结构: {path}"]

    for key in REQUIRED:
        if key not in data:
            issues.append(f"缺少字段: {path} -> {key}")

    if "date" in data and not parse_date(data.get("date")):
        issues.append(f"日期格式非法: {path} -> {data.get('date')}")

    return issues


def main() -> int:
    args = parse_args()
    files = iter_md(args.paths)
    if not files:
        print("未找到 Markdown 文件。")
        return 0

    issues: list[str] = []
    for f in files:
        issues.extend(check(f))

    for item in issues:
        print(item)

    print(f"检查文件数={len(files)} 问题数={len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
