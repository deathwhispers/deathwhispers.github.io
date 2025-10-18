#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notion → Markdown 同步脚本（优化版）
主要改进：
- 命名和注释优化
- 工具函数分组清晰
- Markdown/Front Matter 处理流程清晰
- 图片下载缓存逻辑清晰
- 不改变原先业务逻辑
"""
import os
import re
import shutil
import time
import unicodedata
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# ================== 全局配置 ==================
ROOT_DIR = os.environ.get("GITHUB_WORKSPACE", Path(__file__).resolve().parents[2])
DEFAULT_POSTS_DIR = "_posts"
DEFAULT_IMAGES_DIR = os.path.join("assets", "images")

# ================== 加载本地 .env ==================
# 仅在本地开发时使用，GitHub Actions 会使用 secrets
# env_path = ROOT_DIR / ".env"
# if env_path.exists():
#     load_dotenv(dotenv_path=env_path)
#     print(f"Loaded environment variables from {env_path}")

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

REQUEST_RETRY = 3
REQUEST_TIMEOUT = 20

# URL -> 本地绝对路径缓存，避免重复下载
_download_cache: dict[str, str] = {}


# ================== 工具函数 ==================
def safe_slugify(text: str) -> str:
    """生成 URL/文件安全 slug，保留中文、字母、数字，其余字符替换为 '-'"""
    if not text:
        return "untitled"
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^\w\s\u4e00-\u9fff\-]", " ", text)
    text = re.sub(r"[\s_]+", "-", text)
    slug = text.strip("-").lower()
    return slug if slug else "post"


def mkdir_safe(abs_path: str):
    """确保目录存在"""
    Path(abs_path).mkdir(parents=True, exist_ok=True)


def is_safe_subpath(base: str, target: str) -> bool:
    """检查 target 是否在 base 目录下"""
    try:
        return str(Path(target).resolve()).startswith(str(Path(base).resolve()))
    except Exception:
        return False


def normalize_path(user_path: str | None, default_base: str) -> str:
    """
    将用户提供路径转为绝对路径
    - 如果非法或为空，则返回 default_base 的绝对路径
    """
    base_abs = os.path.join(ROOT_DIR, default_base)
    if not user_path:
        mkdir_safe(base_abs)
        return base_abs

    p = user_path.strip().lstrip("/").rstrip("/")
    if ".." in p:
        mkdir_safe(base_abs)
        return base_abs

    if p.startswith(DEFAULT_IMAGES_DIR) or p.startswith(DEFAULT_POSTS_DIR):
        abs_path = os.path.join(ROOT_DIR, p)
    else:
        abs_path = os.path.join(ROOT_DIR, default_base, p)

    if not is_safe_subpath(ROOT_DIR, abs_path):
        mkdir_safe(base_abs)
        return base_abs

    mkdir_safe(abs_path)
    return abs_path


# ================== 图片下载 ==================
def download_image_to_dir(url: str, target_dir: str, slug: str) -> str | None:
    """
    下载图片到指定目录（子目录为 slug），返回绝对路径或 None
    - 使用全局缓存避免重复下载
    """
    if url in _download_cache and os.path.exists(_download_cache[url]):
        return _download_cache[url]

    slug_safe = safe_slugify(slug) if slug else "post"
    target_dir = os.path.join(target_dir, slug_safe)
    mkdir_safe(target_dir)

    # 提取文件扩展名
    ext = os.path.splitext(url.split("?")[0])[1] or ".png"
    if not re.match(r"^\.[A-Za-z0-9]+$", ext):
        ext = ".png"

    # 生成唯一文件名
    for _ in range(5):
        filename = uuid.uuid4().hex[:16] + ext
        abs_path = os.path.join(target_dir, filename)
        if not os.path.exists(abs_path):
            break

    headers = {}
    if "notion.so" in url and NOTION_API_KEY and "amazonaws.com" not in url:
        headers["Authorization"] = f"Bearer {NOTION_API_KEY}"

    for attempt in range(1, REQUEST_RETRY + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
            resp.raise_for_status()
            with open(abs_path, "wb") as f:
                shutil.copyfileobj(resp.raw, f)
            abs_path = abs_path.replace("\\", "/")
            _download_cache[url] = abs_path
            return abs_path
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed for {url}: {e}")
            time.sleep(1)

    # 下载失败
    try:
        if os.path.exists(abs_path) and os.path.getsize(abs_path) == 0:
            os.remove(abs_path)
    except Exception:
        pass

    print(f"❌ Failed to download image: {url}")
    return None


# ================== Notion 数据解析 ==================
def get_page_property(page: dict, prop_name: str, default: Any = None) -> Any:
    """解析 Notion 页面属性，按类型返回安全值"""
    prop = page.get("properties", {}).get(prop_name)
    if not prop:
        return default
    try:
        ptype = prop.get("type")
        val = prop.get(ptype)
        if ptype == "title":
            return "".join([t.get("plain_text", "") for t in val]) if val else default
        if ptype == "rich_text":
            return "".join([t.get("plain_text", "") for t in val]) if val else default
        if ptype == "select":
            return val.get("name") if val else default
        if ptype == "multi_select":
            return [v.get("name") for v in val] if val else []
        if ptype == "checkbox":
            return prop.get("checkbox", False)
        if ptype == "date":
            return val.get("start") if val else default
        if ptype == "number":
            return prop.get("number")
        if ptype == "people":
            return [p.get("name") for p in val] if val else []
        if ptype == "files":
            files = []
            for f in val:
                if f.get("file"):
                    files.append(f["file"].get("url"))
                elif f.get("external"):
                    files.append(f["external"].get("url"))
            return files
        return default
    except Exception as e:
        print(f"⚠️ Error parsing property '{prop_name}': {e}")
        return default


def get_property_with_aliases(page: dict, aliases: list[str], default: Any = None) -> Any:
    """尝试按多个别名获取 Notion 属性"""
    for name in aliases:
        if name in page.get("properties", {}):
            return get_page_property(page, name, default)
    return default


# ================== Notion API ==================
def query_database() -> list[dict]:
    """查询已发布页面"""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {"filter": {"property": "Status", "select": {"equals": "Published"}}}
    for i in range(REQUEST_RETRY):
        try:
            r = requests.post(url, headers=HEADERS, json=payload, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            return r.json().get("results", [])
        except Exception as e:
            print(f"⚠️ Retry {i + 1} failed: {e}")
            time.sleep(1)
    print("❌ Failed to query Notion database")
    return []


def get_block_children(page_id: str, page_size: int = 100) -> list[dict]:
    """获取页面所有 block"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size={page_size}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception as e:
        print(f"❌ Failed to fetch blocks for {page_id}: {e}")
        return []


# ================== Markdown 转换 ==================
def text_from_rich_text(rich_list: list[dict]) -> str:
    """富文本列表转换为 Markdown 文本"""
    if not rich_list:
        return ""
    parts = []
    for r in rich_list:
        ttype = r.get("type")
        if ttype == "text":
            parts.append(r.get("plain_text", ""))
        elif ttype == "equation":
            expr = r.get("equation", {}).get("expression", "").strip()
            if expr:
                parts.append(expr if "$" in expr else f"${expr}$")
    return "".join(parts)


def block_to_md(block: dict, indent: int = 0) -> str:
    """单个 block 转 Markdown"""
    t = block.get("type")
    space = "  " * indent
    rich = block.get(t, {}).get("rich_text", [])
    text = text_from_rich_text(rich)

    if t.startswith("heading_"):
        level = int(t[-1])
        return f"{'#' * level} {text}"
    if t == "paragraph":
        return text.strip()
    if t == "code":
        lang = block.get("code", {}).get("language", "")
        code_text = text_from_rich_text(block.get("code", {}).get("rich_text", []))
        return f"```{lang}\n{code_text}\n```"
    if t == "image":
        url = block.get("image", {}).get("file", {}).get("url") or block.get("image", {}).get("external", {}).get("url")
        return f"![]({url})" if url and not url.startswith("data:") else ""
    if t == "bulleted_list_item":
        return f"{space}- {text}"
    if t == "numbered_list_item":
        return f"{space}1. {text}"
    if t == "quote":
        return f"> {text}"
    if t == "to_do":
        checked = block.get("to_do", {}).get("checked", False)
        return f"- [{'x' if checked else ' '}] {text}"
    if t == "callout":
        emoji = block.get("callout", {}).get("icon", {}).get("emoji", "💡")
        children_md = ""
        if block.get("has_children"):
            children_md = "\n".join(block_to_md(c, indent + 1) for c in get_block_children(block.get("id")))
        return f"{emoji} {text}\n{children_md}"
    if t == "toggle":
        children_md = ""
        if block.get("has_children"):
            children_md = "\n\n".join(block_to_md(c, indent + 1) for c in get_block_children(block.get("id")))
        return f"<details>\n<summary>{text}</summary>\n\n{children_md}\n</details>"
    if t == "equation":
        expr = block.get("equation", {}).get("expression", "").strip()
        return f"$$\n{expr}\n$$" if expr else ""
    return text


def page_to_markdown(page_id: str) -> str:
    """将 Notion 页面所有 block 转为 Markdown 文本"""
    blocks = get_block_children(page_id)
    md_parts = [block_to_md(b) for b in blocks if b]
    md = "\n\n".join(md_parts)
    # 清理 data: 空图片和多余空行
    md = re.sub(r'!\[\]\(data:[^\)]*\)', '', md)
    md = re.sub(r'!\[\]\(\)', '', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


# ================== Front Matter ==================
def format_front_matter(fm: dict) -> str:
    """生成严格的 front matter"""
    lines = ["---"]
    lines.append(f'layout: {fm.get("layout", "post")}')
    lines.append(f'title: "{fm.get("title", "")}"')
    lines.append(f'date: {fm.get("date", "")}')

    for key in ["tags", "categories"]:
        vals = fm.get(key, [])
        if isinstance(vals, str):
            vals = [vals] if vals else []
        lines.append(f"{key}:")
        if vals:
            lines.extend([f"  - {v}" for v in vals])
        else:
            lines.append("  []")

    for key in ["comments", "math", "mermaid"]:
        lines.append(f"{key}: {str(fm.get(key, True)).lower()}")
    lines.append(f'author: {fm.get("author", "unknown")}')
    lines.append("---\n")
    return "\n".join(lines)


def normalize_md(content: str) -> str:
    """
    标准化 Markdown 内容，用于比较
    - 移除图片 URL，只保留 ![]()
    - 移除多余空行和空格
    """
    content = re.sub(r'!\[.*?\]\(.*?\)', '![]()', content)  # 忽略图片 URL
    content = re.sub(r'\s+', ' ', content)  # 合并空格
    content = re.sub(r'\n+', '\n', content)  # 合并空行
    return content.strip()


# ================== Markdown 保存 ==================
def save_page_markdown(page: dict) -> str:
    """
    保存页面为 Markdown
    - 删除时只清理当前文章图片目录（slug）
    - 若文章未变化则跳过覆盖
    """
    title = get_property_with_aliases(page, ["Title", "标题"], default="Untitled")
    slug_field = get_property_with_aliases(page, ["Slug", "slug"], default=None)
    slug = safe_slugify(slug_field) if slug_field else safe_slugify(title)

    date = get_property_with_aliases(page, ["Date", "日期"], default=datetime.today().strftime("%Y-%m-%d"))
    tags = get_property_with_aliases(page, ["Tags", "标签"], default=[])
    categories = get_property_with_aliases(page, ["Categories", "Category", "分类"], default=[])
    author = get_property_with_aliases(page, ["Author", "作者"], default="unknown")
    comments = get_property_with_aliases(page, ["Comments", "comments"], default=True)
    math = get_property_with_aliases(page, ["Math", "math"], default=True)
    mermaid = get_property_with_aliases(page, ["Mermaid", "mermaid"], default=True)

    save_dir_field = get_property_with_aliases(page, ["SaveDir", "保存目录", "Save Dir"], default=None)
    save_dir_abs = normalize_path(save_dir_field, DEFAULT_POSTS_DIR)
    mkdir_safe(save_dir_abs)

    page_id = page.get("id")
    md_content = page_to_markdown(page_id)

    # ========== 图片处理 ==========
    image_urls = re.findall(r'!\[.*?\]\((https?://[^\)\s]+)\)', md_content)
    has_images = bool(image_urls)
    image_dir_field = get_property_with_aliases(page, ["ImageDir", "Image Dir", "图片目录"], default=None)

    image_dir_abs = None
    if has_images:
        if image_dir_field:
            image_dir_abs = normalize_path(image_dir_field, DEFAULT_IMAGES_DIR)
        else:
            image_dir_abs = normalize_path(os.path.join(DEFAULT_IMAGES_DIR, slug), DEFAULT_IMAGES_DIR)

        # ✅ 只清理当前文章的图片子目录
        post_image_dir = os.path.join(image_dir_abs, slug)
        if os.path.exists(post_image_dir):
            shutil.rmtree(post_image_dir)
        mkdir_safe(post_image_dir)

        def repl_img(match):
            url = match.group(1)
            if not url or url.startswith("data:"):
                return match.group(0)
            local_path = download_image_to_dir(url, image_dir_abs, slug)
            if local_path:
                rel = os.path.relpath(local_path, ROOT_DIR).replace("\\", "/")
                return f"![](/" + rel + ")"
            return match.group(0)

        md_content = re.sub(r'!\[.*?\]\((https?://[^\)\s]+)\)', repl_img, md_content)

    # ========== Front Matter ==========
    images_dir_rel = os.path.relpath(image_dir_abs, ROOT_DIR).replace("\\", "/") if image_dir_abs else ""
    fm = {
        "layout": "post",
        "title": title,
        "date": date,
        "tags": tags,
        "categories": categories,
        "comments": comments,
        "math": math,
        "mermaid": mermaid,
        "author": author,
        "images_dir": images_dir_rel
    }

    file_path = os.path.join(save_dir_abs, f"{date}-{slug}.md")
    new_content = format_front_matter(fm) + "\n" + md_content

    # ========== 重复检测 ==========
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            old_normalized = normalize_md(f.read())
        new_normalized = normalize_md(new_content)
        if old_normalized == new_normalized:
            print(f"⚪ Skipped (no meaningful change): {file_path}")
            return file_path
        else:
            print(f"🟡 Updated: {file_path}")
    else:
        print(f"🟢 Created: {file_path}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return file_path


# ================== 主函数 ==================
def main():
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        print("❌ NOTION_API_KEY and NOTION_DATABASE_ID must be set.")
        return

    pages = query_database()
    if not pages:
        print("⚠️ No published pages found.")
        return

    saved_files = []
    for page in pages:
        try:
            saved_files.append(save_page_markdown(page))
        except Exception as e:
            print(f"❌ Error processing page {page.get('id')}: {e}")

    print(f"✅ Total saved: {len(saved_files)}")


if __name__ == "__main__":
    main()
