#!/usr/bin/env python3
"""检查文章文件名日期前缀与 Front Matter 日期一致性。"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)
NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查文章命名规范与日期一致性")
    parser.add_argument("paths", nargs="*", default=["_posts"], help="待检查文件或目录")
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


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    data = yaml.safe_load(m.group(1)) or {}
    if not isinstance(data, dict):
        return {}
    return data


def normalize_date(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()

    raw = str(value).strip()
    if not raw:
        return None
    raw = raw.split("T", 1)[0].split(" ", 1)[0]
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        return None


def main() -> int:
    args = parse_args()
    files = iter_md(args.paths)
    if not files:
        print("未找到 Markdown 文件。")
        return 0

    errors = 0
    for path in files:
        m = NAME_RE.match(path.name)
        if not m:
            print(f"文件名不合规: {path}")
            errors += 1
            continue

        filename_date = m.group(1)
        fm = read_frontmatter(path)
        if not fm:
            print(f"缺少YAML头: {path}")
            errors += 1
            continue

        fm_date = normalize_date(fm.get("date"))
        if not fm_date:
            print(f"YAML日期不合法: {path} -> {fm.get('date')}")
            errors += 1
            continue

        if fm_date != filename_date:
            print(f"日期不一致: {path} 文件名={filename_date} YAML={fm_date}")
            errors += 1

    print(f"检查文件数={len(files)} 错误数={errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
