#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notion → Markdown 同步脚本（增强版）
特点：
1. 支持段落、标题、列表、代码、图片、待办、引用、callout、toggle、公式、Mermaid
2. 自动下载图片到 assets/images
3. front matter 自动生成
4. 绝对路径保证 _posts/ 和 assets/images/ 在仓库根目录
5. 健壮性：网络重试、异常捕获、缺失字段容错
"""

import os
import requests
import yaml
import shutil
import time
from pathlib import Path
from datetime import datetime
import re

# ================== GitHub 仓库根目录 ==================
# 在 GitHub Actions 中，GITHUB_WORKSPACE 指向仓库根目录
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

# ================== 保存 Markdown ==================
def save_markdown(page):
    title = get_page_property(page, "Title", "Untitled")
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
        "tags": tags,
        "categories": categories,
        "comments": comments,
        "math": math,
        "mermaid": mermaid,
        "author": author,
        "images_dir": image_dir
    }

    mkdir_safe(save_dir)
    filename = f"{date}-{title.replace(' ', '-')}.md"
    file_path = os.path.join(save_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(fm, f, allow_unicode=True)
        f.write("---\n\n")
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
