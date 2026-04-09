#!/usr/bin/env python3
"""检查 tag/category 的 slug 冲突，避免 Jekyll 生成重复页面。"""

from __future__ import annotations

import argparse
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查标签/分类 slug 冲突")
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


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def read_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    data = yaml.safe_load(m.group(1)) or {}
    if isinstance(data, dict):
        return data
    return {}


def slugify(value: str) -> str:
    x = unicodedata.normalize("NFKD", value).lower()
    x = re.sub(r"[^\w\s-]", "", x)
    x = re.sub(r"[\s_]+", "-", x)
    x = re.sub(r"-+", "-", x)
    return x.strip("-")


def find_collisions(files: list[Path], key: str) -> dict[str, set[str]]:
    slug_map: dict[str, set[str]] = defaultdict(set)
    for p in files:
        fm = read_front_matter(p)
        for value in normalize_list(fm.get(key)):
            slug = slugify(value)
            if slug:
                slug_map[slug].add(value)

    collisions: dict[str, set[str]] = {}
    for slug, originals in slug_map.items():
        if len(originals) > 1:
            collisions[slug] = originals
    return collisions


def main() -> int:
    args = parse_args()
    files = iter_md(args.paths)

    tag_collisions = find_collisions(files, "tags")
    cat_collisions = find_collisions(files, "categories")

    for slug, originals in sorted(tag_collisions.items()):
        values = ", ".join(sorted(originals))
        print(f"标签冲突: slug={slug} 值=[{values}]")

    for slug, originals in sorted(cat_collisions.items()):
        values = ", ".join(sorted(originals))
        print(f"分类冲突: slug={slug} 值=[{values}]")

    issue_count = len(tag_collisions) + len(cat_collisions)
    print(f"检查文件数={len(files)} 冲突组数={issue_count}")
    return 1 if issue_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
