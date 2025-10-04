#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notion → Markdown 同步脚本
功能：
1. 获取 Notion 数据库文章（Status=Published）
2. 转换文章块为 Markdown
3. 下载文章中图片到指定目录
4. 生成 front matter YAML
5. 支持自定义 SaveDir、ImageDir、tags、categories、author、comments、math、mermaid
"""

import os
import requests
import yaml
import shutil
import time
from pathlib import Path
from datetime import datetime

# ================== 配置 ==================
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
REQUEST_RETRY = 3      # 网络请求重试次数
REQUEST_TIMEOUT = 20   # 网络请求超时秒数

# ================== 工具函数 ==================

def mkdir_safe(path):
    """安全创建目录"""
    Path(path).mkdir(parents=True, exist_ok=True)

def clean_dir(path):
    """清理目录"""
    if os.path.exists(path):
        shutil.rmtree(path)
    mkdir_safe(path)

def download_image(url, save_dir):
    """下载图片并返回本地路径"""
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
    """查询 Notion 数据库，返回已发布文章列表"""
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
    """获取页面属性，自动适配字段类型"""
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

def get_page_blocks(page_id):
    """获取页面块内容并转成 Markdown"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    md_lines = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        blocks = resp.json().get("results", [])
        for block in blocks:
            t = block.get("type")
            if t == "paragraph":
                text = "".join([r.get("plain_text","") for r in block.get("paragraph", {}).get("rich_text",[])])
                md_lines.append(text)
            elif t == "heading_1":
                text = "".join([r.get("plain_text","") for r in block.get("heading_1", {}).get("rich_text",[])])
                md_lines.append(f"# {text}")
            elif t == "heading_2":
                text = "".join([r.get("plain_text","") for r in block.get("heading_2", {}).get("rich_text",[])])
                md_lines.append(f"## {text}")
            elif t == "heading_3":
                text = "".join([r.get("plain_text","") for r in block.get("heading_3", {}).get("rich_text",[])])
                md_lines.append(f"### {text}")
            elif t == "code":
                code = "".join([r.get("plain_text","") for r in block.get("code", {}).get("rich_text",[])])
                lang = block.get("code", {}).get("language","")
                md_lines.append(f"```{lang}\n{code}\n```")
            elif t == "image":
                url = block.get("image", {}).get("file", {}).get("url") or block.get("image", {}).get("external", {}).get("url")
                if url:
                    md_lines.append(f"![]({url})")
            elif t == "bulleted_list_item":
                text = "".join([r.get("plain_text","") for r in block.get("bulleted_list_item", {}).get("rich_text",[])])
                md_lines.append(f"- {text}")
            elif t == "numbered_list_item":
                text = "".join([r.get("plain_text","") for r in block.get("numbered_list_item", {}).get("rich_text",[])])
                md_lines.append(f"1. {text}")
            # TODO: 可扩展更多块类型（todo, quote, toggle, callout等）
    except Exception as e:
        print(f"❌ Failed to fetch blocks for page {page_id}: {e}")
    return "\n\n".join(md_lines)

# ================== Markdown 保存 ==================

def save_markdown(page):
    """生成 Markdown 文件"""
    title = get_page_property(page, "Title", "Untitled")
    date = get_page_property(page, "Date", datetime.today().strftime("%Y-%m-%d"))
    tags = get_page_property(page, "Tags", [])
    categories = get_page_property(page, "Categories", [])
    save_dir = get_page_property(page, "SaveDir", "_posts")
    image_dir = get_page_property(page, "ImageDir", f"assets/images/{title.replace(' ', '-')}")
    author = get_page_property(page, "Author", "unknown")
    comments = get_page_property(page, "Comments", True)
    math = get_page_property(page, "Math", True)
    mermaid = get_page_property(page, "Mermaid", True)

    # 清理旧图片
    clean_dir(image_dir)

    # 获取页面 Markdown 内容
    page_id = page.get("id")
    md_content = get_page_blocks(page_id)

    # 替换图片链接为本地路径
    import re
    def repl_image(match):
        url = match.group(1)
        local_path = download_image(url, image_dir)
        if local_path:
            return f"![]({local_path})"
        else:
            return match.group(0)
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
