#!/usr/bin/env python3
"""标准化 Jekyll 文章 YAML 头。

功能：
- 保证必填字段：layout/title/date/tags/categories/author
- 默认保留额外字段（可关闭）
- YAML 输出统一为 2 空格缩进
- 支持检查模式（仅提示，不写文件）
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")


@dataclass
class Result:
    changed: int = 0
    scanned: int = 0
    errors: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="标准化文章 YAML 头")
    parser.add_argument("paths", nargs="*", default=["_posts"], help="待扫描文件或目录")
    parser.add_argument("--check", action="store_true", help="仅检查，不写入")
    parser.add_argument("--author", default="deathwhispers", help="默认作者")
    parser.add_argument("--layout", default="post", help="默认 layout")
    parser.add_argument("--no-preserve-extra", action="store_true", help="不保留非标准字段")
    return parser.parse_args()


def iter_markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
            continue
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return files


def split_front_matter(text: str) -> tuple[dict[str, Any], str, str]:
    if not text.startswith("---\n"):
        return {}, "", text

    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, "", text

    raw_fm = match.group(1)
    body = text[match.end() :]
    try:
        data = yaml.safe_load(raw_fm) or {}
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    return data, raw_fm, body


def parse_date(value: Any) -> str | None:
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


def derive_title(path: Path, meta: dict[str, Any], body: str) -> str:
    title = str(meta.get("title") or "").strip()
    if title:
        return title

    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", s)
        if heading:
            return heading.group(1).strip().strip("*")
        break

    name = path.stem
    m = DATE_PREFIX_RE.match(path.name)
    if m:
        name = m.group(2)
    return name or "未命名"


def derive_date(path: Path, meta: dict[str, Any]) -> str:
    normalized = parse_date(meta.get("date"))
    if normalized:
        return normalized

    m = DATE_PREFIX_RE.match(path.name)
    if m:
        return m.group(1)

    return date.today().isoformat()


def normalize_list(value: Any, fallback: str) -> list[str]:
    if value is None:
        return [fallback]
    if isinstance(value, list):
        items = [str(v).strip() for v in value if str(v).strip()]
        return items if items else [fallback]

    v = str(value).strip()
    return [v] if v else [fallback]


def derive_categories(path: Path, value: Any) -> list[str]:
    if value is not None:
        return normalize_list(value, "未分类")

    parts = path.parts
    if len(parts) >= 3 and parts[0] == "_posts":
        categories = [p for p in parts[1:-1] if p]
        return categories or ["未分类"]
    return ["未分类"]


def build_front_matter(
    path: Path,
    meta: dict[str, Any],
    body: str,
    default_author: str,
    default_layout: str,
    preserve_extra: bool,
) -> dict[str, Any]:
    standardized: dict[str, Any] = {
        "layout": str(meta.get("layout") or default_layout),
        "title": derive_title(path, meta, body),
        "date": derive_date(path, meta),
        "tags": normalize_list(meta.get("tags"), "笔记"),
        "categories": derive_categories(path, meta.get("categories")),
        "author": str(meta.get("author") or default_author),
    }

    if preserve_extra:
        for key, value in meta.items():
            if key in standardized:
                continue
            standardized[key] = value

    return standardized


def render(meta: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(
        meta,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        indent=2,
    )
    normalized_body = body.lstrip("\n").rstrip("\n")
    return f"---\n{yaml_text}---\n\n{normalized_body}\n"


def process_file(path: Path, args: argparse.Namespace, result: Result) -> None:
    result.scanned += 1
    text = path.read_text(encoding="utf-8")
    meta, _, body = split_front_matter(text)

    new_meta = build_front_matter(
        path=path,
        meta=meta,
        body=body,
        default_author=args.author,
        default_layout=args.layout,
        preserve_extra=not args.no_preserve_extra,
    )
    new_text = render(new_meta, body)

    if new_text != text:
        result.changed += 1
        if args.check:
            print(f"需要规范化: {path}")
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"已更新: {path}")


def main() -> int:
    args = parse_args()
    files = iter_markdown_files(args.paths)
    if not files:
        print("未找到 Markdown 文件。")
        return 0

    result = Result()
    for path in files:
        try:
            process_file(path, args, result)
        except Exception as exc:
            result.errors += 1
            print(f"处理失败: {path} -> {exc}")

    mode = "检查模式" if args.check else "执行模式"
    print(f"[{mode}] 扫描={result.scanned} 变更={result.changed} 错误={result.errors}")

    if result.errors:
        return 2
    if args.check and result.changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
