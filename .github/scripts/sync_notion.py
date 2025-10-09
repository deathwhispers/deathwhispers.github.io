#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notion → Markdown 同步脚本（增强版）
特点：
1. 支持段落、标题、列表、代码、图片、待办、引用、callout、toggle、公式、Mermaid
2. 自动下载图片到 assets/images
3. front matter 自动生成，严格符合 Jekyll 博客格式
4. 绝对路径保证 _posts/ 和 assets/images/ 在仓库根目录
5. 健壮性：网络重试、异常捕获、缺失字段容错
"""

import os
import requests
import shutil
import time
from pathlib import Path
from datetime import datetime
import re
import unicodedata
from pypinyin import lazy_pinyin, Style

# ================== GitHub 仓库根目录 ==================
ROOT_DIR = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
POSTS_DIR = os.path.join(ROOT_DIR, "_posts")
IMAGES_BASE_DIR = os.path.join(ROOT_DIR, "assets/images")

# ================== 配置 ==================
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

REQUEST_RETRY = 3
REQUEST_TIMEOUT = 20

# ================== 工具函数 ==================
# ================== Slug 生成（无网络、无 API） ==================

def slugify_safe(text: str) -> str:
    """通用 slug 化：只保留字母数字和连字符"""
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')  # 移除重音
    text = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\s\-]', ' ', text)  # 保留中英文、数字、空格、连字符
    text = re.sub(r'[\s\-]+', '-', text)
    return text.strip('-').lower()

def mixed_slug(title: str) -> str:
    """
    智能混合 slug：
    - 英文/数字/符号 → 保留并 slugify
    - 中文 → 转拼音
    示例：
      "安装 FFmpeg 教程！" → "an-zhuang-ffmpeg-jiao-cheng"
      "Hello 世界" → "hello-shi-jie"
    """
    if not title:
        return "untitled"

    # 分段处理：逐字符判断
    parts = []
    current_en = []
    current_zh = []

    for char in title:
        if '\u4e00' <= char <= '\u9fff':  # 中文字符
            if current_en:
                parts.append(slugify_safe(''.join(current_en)))
                current_en = []
            current_zh.append(char)
        else:
            if current_zh:
                # 中文转拼音
                pinyin = lazy_pinyin(''.join(current_zh), style=Style.NORMAL, errors='ignore')
                parts.append('-'.join(pinyin))
                current_zh = []
            current_en.append(char)

    # 处理剩余
    if current_en:
        parts.append(slugify_safe(''.join(current_en)))
    if current_zh:
        pinyin = lazy_pinyin(''.join(current_zh), style=Style.NORMAL, errors='ignore')
        parts.append('-'.join(pinyin))

    slug = '-'.join([p for p in parts if p])
    # 再次清理
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-') or "post"

def generate_slug_from_title(title: str) -> str:
    return mixed_slug(title)

def mkdir_safe(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    mkdir_safe(path)

def download_image(url, save_dir):
    mkdir_safe(save_dir)
    filename = url.split("/")[-1].split("?")[0] or "image.png"
    file_path = os.path.join(save_dir, filename)
    for i in range(REQUEST_RETRY):
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(resp.content)
            return file_path.replace("\\", "/")
        except Exception as e:
            print(f"⚠️ Retry {i+1} download image {url} failed: {e}")
            time.sleep(1)
    print(f"❌ Failed to download image {url} after {REQUEST_RETRY} retries")
    return None

# ================== Notion API ==================
def query_database():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Status",
            "select": {"equals": "Published"}
        }
    }
    for i in range(REQUEST_RETRY):
        try:
            resp = requests.post(url, headers=HEADERS, json=payload, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except Exception as e:
            print(f"⚠️ Retry {i+1} query database failed: {e}")
            time.sleep(1)
    print("❌ Failed to query Notion database after retries")
    return []

def get_page_property(page, prop_name, default=None):
    prop = page.get("properties", {}).get(prop_name, {})
    type_map = {
        "title": lambda p: "".join([t["plain_text"] for t in p.get("title", [])]) if p.get("title") else default,
        "rich_text": lambda p: "".join([t["plain_text"] for t in p.get("rich_text", [])]) if p.get("rich_text") else default,
        "multi_select": lambda p: [t["name"] for t in p.get("multi_select", [])] if p.get("multi_select") else [],
        "checkbox": lambda p: p.get("checkbox", False),
        "select": lambda p: p.get("select", {}).get("name", default),
        "date": lambda p: p.get("date", {}).get("start", default)
    }
    return type_map.get(prop.get("type", ""), lambda x: default)(prop)

# ================== Markdown 转换 ==================
def get_block_children_md(block_id, indent=0):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        blocks = resp.json().get("results", [])
        md_list = [block_to_md(b, indent) for b in blocks]
        return "\n\n".join(md_list)
    except Exception as e:
        print(f"❌ Failed to fetch children for block {block_id}: {e}")
        return ""

def block_to_md(block, indent=0):
    t = block.get("type")
    space = "  " * indent
    if t == "paragraph":
        text = "".join([r.get("plain_text","") for r in block.get("paragraph", {}).get("rich_text",[])])
        return f"{space}{text}"
    elif t == "heading_1":
        text = "".join([r.get("plain_text","") for r in block.get("heading_1", {}).get("rich_text",[])])
        return f"# {text}"
    elif t == "heading_2":
        text = "".join([r.get("plain_text","") for r in block.get("heading_2", {}).get("rich_text",[])])
        return f"## {text}"
    elif t == "heading_3":
        text = "".join([r.get("plain_text","") for r in block.get("heading_3", {}).get("rich_text",[])])
        return f"### {text}"
    elif t == "code":
        code = "".join([r.get("plain_text","") for r in block.get("code", {}).get("rich_text",[])])
        lang = block.get("code", {}).get("language","")
        return f"```{lang}\n{code}\n```"
    elif t == "image":
        url = block.get("image", {}).get("file", {}).get("url") or block.get("image", {}).get("external", {}).get("url")
        return f"![]({url})" if url else ""
    elif t == "bulleted_list_item":
        text = "".join([r.get("plain_text","") for r in block.get("bulleted_list_item", {}).get("rich_text",[])])
        return f"{space}- {text}"
    elif t == "numbered_list_item":
        text = "".join([r.get("plain_text","") for r in block.get("numbered_list_item", {}).get("rich_text",[])])
        return f"{space}1. {text}"
    elif t == "quote":
        text = "".join([r.get("plain_text","") for r in block.get("quote", {}).get("rich_text",[])])
        return f"{space}> {text}"
    elif t == "to_do":
        checked = block.get("to_do", {}).get("checked", False)
        text = "".join([r.get("plain_text","") for r in block.get("to_do", {}).get("rich_text",[])])
        mark = "x" if checked else " "
        return f"{space}- [{mark}] {text}"
    elif t == "callout":
        text = "".join([r.get("plain_text","") for r in block.get("callout", {}).get("rich_text",[])])
        emoji = block.get("callout", {}).get("icon", {}).get("emoji", "💡")
        children_md = ""
        if block.get("has_children"):
            children_md = get_block_children_md(block.get("id"), indent+1)
        return f"{space}{emoji} {text}\n{children_md}"
    elif t == "toggle":
        text = "".join([r.get("plain_text","") for r in block.get("toggle", {}).get("rich_text",[])])
        children_md = ""
        if block.get("has_children"):
            children_md = get_block_children_md(block.get("id"), indent+1)
        return f"{space}<details>\n{space}<summary>{text}</summary>\n\n{children_md}\n{space}</details>"
    elif t == "equation":
        eq = block.get("equation", {}).get("expression","")
        return f"${eq}$"
    else:
        return ""

def get_page_blocks(page_id):
    return get_block_children_md(page_id)

# ================== Front Matter 格式化 ==================
def format_front_matter(fm: dict) -> str:
    """
    严格生成 front matter:
    - title 用双引号
    - date 不加引号
    - tags 和 categories 保留列表格式，即使为空
    - 字段顺序固定
    """
    lines = ["---"]
    lines.append(f'layout: {fm.get("layout", "post")}')
    lines.append(f'title: "{fm.get("title","")}"')
    lines.append(f'date: {fm.get("date","")}')

    # tags
    tags = fm.get("tags", [])
    lines.append("tags:")
    if tags:
        for t in tags:
            lines.append(f"  - {t}")
    else:
        lines.append("  []")

    # categories
    categories = fm.get("categories", [])
    lines.append("categories:")
    if categories:
        for c in categories:
            lines.append(f"  - {c}")
    else:
        lines.append("  []")

    # 其他字段
    lines.append(f'comments: {str(fm.get("comments", True)).lower()}')
    lines.append(f'math: {str(fm.get("math", True)).lower()}')
    lines.append(f'mermaid: {str(fm.get("mermaid", True)).lower()}')
    lines.append(f'author: {fm.get("author","unknown")}')
    lines.append("---\n")
    return "\n".join(lines)

# ================== 保存 Markdown ==================
def save_markdown(page):
    title = get_page_property(page, "Title", "Untitled")

    custom_slug = get_page_property(page, "Slug", None)
    if custom_slug:
        slug = slugify_safe(custom_slug)
    else:
        slug = generate_slug_from_title(title)

    date = get_page_property(page, "Date", datetime.today().strftime("%Y-%m-%d"))
    tags = get_page_property(page, "Tags", [])
    categories = get_page_property(page, "Categories", [])
    author = get_page_property(page, "Author", "unknown")
    comments = get_page_property(page, "Comments", True)
    math = get_page_property(page, "Math", True)
    mermaid = get_page_property(page, "Mermaid", True)

    # 路径基于仓库根目录
    save_dir = POSTS_DIR
    image_dir = os.path.join(IMAGES_BASE_DIR, title.replace(" ", "-"))

    clean_dir(image_dir)
    page_id = page.get("id")
    md_content = get_page_blocks(page_id)

    # 图片替换为本地路径
    def repl_image(match):
        url = match.group(1)
        local_path = download_image(url, image_dir)
        return f"![]({local_path})" if local_path else match.group(0)

    md_content = re.sub(r'!\[.*?\]\((https://[^\)]+)\)', repl_image, md_content)

    # front matter
    fm = {
        "layout": "post",
        "title": title,
        "date": date,
        "slug": slug,
        "tags": tags,
        "categories": categories,
        "comments": comments,
        "math": math,
        "mermaid": mermaid,
        "author": author,
        "images_dir": image_dir
    }

    mkdir_safe(save_dir)
    # 使用 slug 生成文件名
    filename = f"{date}-{slug}.md"

    file_path = os.path.join(save_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(format_front_matter(fm))
        f.write(md_content)

    print(f"✅ Saved: {file_path}")
    return file_path

# ================== 主函数 ==================
def main():
    pages = query_database()
    if not pages:
        print("⚠️ No published pages found")
        return

    saved_files = []
    for page in pages:
        try:
            saved_file = save_markdown(page)
            saved_files.append(saved_file)
        except Exception as e:
            print(f"❌ Failed to process page: {e}")

    print(f"✅ Total saved files: {len(saved_files)}")
    return saved_files

if __name__ == "__main__":
    main()
