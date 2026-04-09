#!/usr/bin/env python3
"""在指定时间窗口内重分布文章日期。

会同时更新：
- front matter 的 `date`
- 文件名前缀日期 `YYYY-MM-DD-...`

日期分配使用“路径 + seed”的确定性伪随机算法。
"""

from __future__ import annotations

import argparse
import calendar
import hashlib
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)
DATE_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")


@dataclass
class Window:
    pattern: str
    start: date
    end: date


@dataclass
class Item:
    path: Path
    title: str
    new_date: date
    new_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按时间区间重排文章日期")
    parser.add_argument("paths", nargs="*", default=["_posts"], help="待处理 Markdown 文件或目录")
    parser.add_argument("--start", default="2021-09", help="全局开始月份，格式 YYYY-MM")
    parser.add_argument("--end", default="2024-04", help="全局结束月份，格式 YYYY-MM")
    parser.add_argument("--seed", default="default", help="分布种子")
    parser.add_argument("--window-map", help="窗口映射 YAML 配置文件")
    parser.add_argument("--apply", action="store_true", help="执行写入；不传则仅预览")
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


def month_start_end(month_str: str) -> tuple[date, date]:
    year, month = [int(x) for x in month_str.split("-", 1)]
    first = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    last = date(year, month, last_day)
    return first, last


def load_windows(path: str | None) -> list[Window]:
    if not path:
        return []

    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    raw_windows = cfg.get("windows", [])
    windows: list[Window] = []
    for item in raw_windows:
        if not isinstance(item, dict):
            continue
        pattern = str(item.get("pattern") or "").strip()
        start = str(item.get("start") or "").strip()
        end = str(item.get("end") or "").strip()
        if not (pattern and start and end):
            continue
        s, _ = month_start_end(start)
        _, e = month_start_end(end)
        windows.append(Window(pattern=pattern, start=s, end=e))
    return windows


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text

    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    body = text[m.end() :]
    return data, body


def extract_title(path: Path, meta: dict[str, Any], body: str) -> str:
    title = str(meta.get("title") or "").strip()
    if title:
        return title

    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        h = re.match(r"^#{1,6}\s+(.+)$", s)
        if h:
            return h.group(1).strip().strip("*")
        break

    m = DATE_NAME_RE.match(path.name)
    return m.group(2) if m else path.stem


def pick_window(path: Path, title: str, global_start: date, global_end: date, windows: list[Window]) -> tuple[date, date]:
    text = f"{path.as_posix()} {title}"
    for w in windows:
        if re.search(w.pattern, text):
            return w.start, w.end
    return global_start, global_end


def deterministic_date(path: Path, seed: str, start: date, end: date) -> date:
    span = (end - start).days
    if span < 0:
        start, end = end, start
        span = (end - start).days
    key = f"{seed}|{path.as_posix()}"
    n = int(hashlib.sha1(key.encode("utf-8")).hexdigest(), 16)
    return start + timedelta(days=(n % (span + 1)))


def render(meta: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(
        meta,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        indent=2,
    )
    return f"---\n{yaml_text}---\n\n{body.lstrip().rstrip()}\n"


def rename_target(path: Path, d: date, reserved: set[Path]) -> Path:
    date_str = d.isoformat()
    m = DATE_NAME_RE.match(path.name)
    rest = m.group(2) if m else path.stem
    candidate = path.with_name(f"{date_str}-{rest}.md")
    idx = 2
    while candidate in reserved or (candidate.exists() and candidate != path):
        candidate = path.with_name(f"{date_str}-{rest}-{idx}.md")
        idx += 1
    return candidate


def main() -> int:
    args = parse_args()

    files = iter_md(args.paths)
    if not files:
        print("未找到 Markdown 文件。")
        return 0

    global_start, _ = month_start_end(args.start)
    _, global_end = month_start_end(args.end)
    windows = load_windows(args.window_map)

    plan: list[Item] = []
    reserved: set[Path] = set()

    for path in files:
        text = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        title = extract_title(path, meta, body)
        win_start, win_end = pick_window(path, title, global_start, global_end, windows)
        d = deterministic_date(path, args.seed, win_start, win_end)
        new_path = rename_target(path, d, reserved)
        reserved.add(new_path)
        plan.append(Item(path=path, title=title, new_date=d, new_path=new_path))

    for item in plan:
        old = item.path
        text = old.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        meta["date"] = item.new_date.isoformat()
        new_text = render(meta, body)

        if args.apply:
            old.write_text(new_text, encoding="utf-8")
            if item.new_path != old:
                item.new_path.parent.mkdir(parents=True, exist_ok=True)
                old.rename(item.new_path)

        op = "执行" if args.apply else "预览"
        print(f"{op}: {old} -> {item.new_path} 日期={item.new_date.isoformat()}")

    mode = "执行模式" if args.apply else "预览模式"
    print(f"处理文件数={len(plan)} 模式={mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
