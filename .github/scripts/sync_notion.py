#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notion → Markdown 同步脚本（修正版）
主要修复：
- SaveDir（文章保存目录）优先从 Notion 字段读取并安全处理
- ImageDir（图片保存目录）优先从 Notion 字段读取并安全处理
- 图片下载并替换为仓库相对路径
- Slug 优先使用 Notion 的 Slug 字段
"""

import os
import re
import time
import shutil
import unicodedata
import requests
from pathlib import Path
from datetime import datetime

# ================== 仓库根目录（保证无论 working-directory 为何都写到 repo 根） ==================
ROOT_DIR = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
# ROOT_DIR = Path(__file__).resolve().parents[2]

# 默认基础目录（相对于 ROOT_DIR）
DEFAULT_POSTS_BASE = "_posts"
DEFAULT_IMAGES_BASE = os.path.join("assets", "images")

# 全局配置
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

REQUEST_RETRY = 3
REQUEST_TIMEOUT = 20

# ================== 工具：slug、安全路径、文件夹 ==================
def safe_slugify(text: str) -> str:
    """生成安全 slug：保留中文、字母、数字，其他字符转换为连字符"""
    if not text:
        return "untitled"
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    # 保留中文 \u4e00-\u9fff、字母数字、连字符、空格
    text = re.sub(r'[^\w\s\u4e00-\u9fff\-]', ' ', text)
    text = re.sub(r'[\s\_]+', '-', text)
    slug = text.strip('-').lower()
    if not slug:
        return "post"
    return slug


# ================== 图片下载函数（支持 Notion 私有文件，返回绝对路径） ==================
def download_image(url: str, save_dir_abs: str) -> str | None:
    """
    下载 image 到 save_dir_abs，返回本地绝对路径，失败返回 None。
    - 如果 URL 来自 notion（包含 's3.us-west-2.amazonaws.com' 或 'www.notion.so' 等），
      我们也带上 Notion API KEY 头部尝试访问（有些 Notion file 需要）。
    - 如果文件已存在且大小>0，直接返回（避免重复下载）。
    """
    try:
        mkdir_safe_abs(save_dir_abs)
    except Exception as e:
        print(f"❌ cannot create image dir {save_dir_abs}: {e}")
        return None

    # 解析文件名（去掉 query）
    try:
        filename = url.split("/")[-1].split("?")[0] or "image.png"
        filename = re.sub(r'[\\/:*?"<>|]+', '_', filename)
    except Exception:
        filename = "image.png"

    abs_path = os.path.join(save_dir_abs, filename)

    # 已存在则直接返回
    if os.path.exists(abs_path) and os.path.getsize(abs_path) > 0:
        return abs_path.replace("\\", "/")

    # 准备 headers：对于 Notion 托管的文件，带 Authorization 可以避免 403
    req_headers = {}
    if "notion" in url or "amazonaws.com" in url:
        # 只在可能是 Notion 托管的 URL 上附带 Authorization
        req_headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}"
        }

    for attempt in range(1, REQUEST_RETRY + 1):
        try:
            resp = requests.get(url, headers=req_headers, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            with open(abs_path, "wb") as fw:
                fw.write(resp.content)
            return abs_path.replace("\\", "/")
        except Exception as e:
            print(f"⚠️ download_image attempt {attempt} failed for {url}: {e}")
            time.sleep(1)
    print(f"❌ download_image: failed to download {url} after {REQUEST_RETRY} attempts")
    # 清理可能的空文件
    try:
        if os.path.exists(abs_path) and os.path.getsize(abs_path) == 0:
            os.remove(abs_path)
    except Exception:
        pass
    return None


# ---------- 路径 & 目录工具 ----------
def mkdir_safe_abs(abs_path: str):
    Path(abs_path).mkdir(parents=True, exist_ok=True)

def clean_dir_abs(abs_path: str):
    if os.path.exists(abs_path):
        shutil.rmtree(abs_path)
    mkdir_safe_abs(abs_path)

def is_safe_subpath(base_abs: str, target_abs: str) -> bool:
    try:
        base = Path(base_abs).resolve()
        target = Path(target_abs).resolve()
        return str(target).startswith(str(base))
    except Exception:
        return False

def normalize_user_path_to_abs(user_path: str, default_base_rel: str) -> str:
    """
    将用户提供的路径（可能为 'assets/images/deepseek' 或 '/assets/images/deepseek' 或 'ai/deepseek' 等）
    转为基于 ROOT_DIR 的绝对路径。
    如果 user_path 为空或非法，则返回 ROOT_DIR/default_base_rel 的绝对路径。
    """
    base_abs = os.path.join(ROOT_DIR, default_base_rel)
    if not user_path:
        mkdir_safe_abs(base_abs)
        return base_abs

    p = str(user_path).strip()
    p = p.lstrip("/").rstrip("/")
    if ".." in p:
        mkdir_safe_abs(base_abs)
        return base_abs

    # 若用户已包含默认基路径段，则直接拼接
    if p.startswith(DEFAULT_IMAGES_BASE) or p.startswith(DEFAULT_POSTS_BASE):
        abs_path = os.path.join(ROOT_DIR, p)
    else:
        abs_path = os.path.join(ROOT_DIR, default_base_rel, p)

    if not is_safe_subpath(ROOT_DIR, abs_path):
        mkdir_safe_abs(base_abs)
        return base_abs

    mkdir_safe_abs(abs_path)
    return abs_path



# ---------- 下载图片（返回绝对路径或 None） ----------
def download_image_safe(url: str, save_dir_abs: str) -> str | None:
    """
    下载图片到 save_dir_abs，返回文件绝对路径（字符串），失败返回 None。
    - 兼容 Notion file.url (S3 临时链接) 与 external.url
    - 自动携带 Authorization header 以访问私有资源
    """
    mkdir_safe_abs(save_dir_abs)

    try:
        filename = url.split("/")[-1].split("?")[0] or "image.png"
        filename = re.sub(r'[\\/:*?"<>|]+', '_', filename)
    except Exception:
        filename = f"image_{int(time.time())}.png"

    abs_path = os.path.join(save_dir_abs, filename)
    if os.path.exists(abs_path) and os.path.getsize(abs_path) > 0:
        return abs_path.replace("\\", "/")

    # 检查是否是 Notion 托管的 S3 链接
    is_notion_file = "amazonaws.com" in url or "notion.so" in url

    headers = {}
    if is_notion_file and NOTION_API_KEY:
        headers["Authorization"] = f"Bearer {NOTION_API_KEY}"

    # ✅ 重试下载
    for attempt in range(1, REQUEST_RETRY + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
            if resp.status_code == 403:
                print(f"⚠️ 403 Forbidden for {url} — retrying with headers...")
            resp.raise_for_status()

            with open(abs_path, "wb") as fw:
                shutil.copyfileobj(resp.raw, fw)
            return abs_path.replace("\\", "/")
        except Exception as e:
            print(f"⚠️ download_image attempt {attempt} failed for {url}: {e}")
            time.sleep(1)

    print(f"❌ download_image: failed to download {url}")
    return None


# ================== Notion 读取与类型化处理 ==================
def get_page_property(page, prop_name, default=None):
    """
    精确按 Notion 字段类型解析属性值
    返回值类型依据字段类型：
      - title / rich_text / select -> str (或 None)
      - multi_select -> list[str]
      - checkbox -> bool
      - date -> str (ISO date)
    """
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
            # 返回文件名或 url 列表
            files = []
            for f in val:
                if f.get("file"):
                    files.append(f["file"].get("url"))
                elif f.get("external"):
                    files.append(f["external"].get("url"))
            return files
        # 默认兜底
        return default
    except Exception as e:
        print(f"⚠️ Error parsing property '{prop_name}': {e}")
        return default

def get_property_with_aliases(page, aliases, default=None):
    """
    尝试按多个别名查找属性，例如 ["Categories","Category","分类"]
    返回 get_page_property 解析后的值（类型安全）
    """
    for name in aliases:
        if name in page.get("properties", {}):
            return get_page_property(page, name, default)
    return default

# ================== Notion API：查询数据库 & 页面块 ==================
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
            r = requests.post(url, headers=HEADERS, json=payload, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            return r.json().get("results", [])
        except Exception as e:
            print(f"⚠️ Retry {i+1} query database failed: {e}")
            time.sleep(1)
    print("❌ Failed to query Notion database after retries")
    return []

def get_block_children(page_id, page_size=100):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size={page_size}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception as e:
        print(f"❌ Failed to fetch blocks for {page_id}: {e}")
        return []

# ================== Markdown 转换（支持常见块） ==================
def text_from_rich_text(rich_list):
    return "".join([r.get("plain_text", "") for r in rich_list]) if rich_list else ""

def block_to_md(block, indent=0):
    t = block.get("type")
    space = "  " * indent
    if t == "paragraph":
        return space + text_from_rich_text(block.get("paragraph", {}).get("rich_text", []))
    if t == "heading_1":
        return "# " + text_from_rich_text(block.get("heading_1", {}).get("rich_text", []))
    if t == "heading_2":
        return "## " + text_from_rich_text(block.get("heading_2", {}).get("rich_text", []))
    if t == "heading_3":
        return "### " + text_from_rich_text(block.get("heading_3", {}).get("rich_text", []))
    if t == "code":
        code_text = text_from_rich_text(block.get("code", {}).get("rich_text", []))
        lang = block.get("code", {}).get("language", "")
        return f"```{lang}\n{code_text}\n```"
    if t == "image":


        # Notion image may be file or external
        url = block.get("image", {}).get("file", {}).get("url") or block.get("image", {}).get("external", {}).get("url")
        return f"![]({url})" if url else ""
    if t == "bulleted_list_item":
        return f"{space}- " + text_from_rich_text(block.get("bulleted_list_item", {}).get("rich_text", []))
    if t == "numbered_list_item":
        return f"{space}1. " + text_from_rich_text(block.get("numbered_list_item", {}).get("rich_text", []))
    if t == "quote":
        return f"{space}> " + text_from_rich_text(block.get("quote", {}).get("rich_text", []))
    if t == "to_do":
        checked = block.get("to_do", {}).get("checked", False)
        mark = "x" if checked else " "
        return f"{space}- [{mark}] " + text_from_rich_text(block.get("to_do", {}).get("rich_text", []))
    if t == "callout":
        icon = block.get("callout", {}).get("icon", {}).get("emoji", "💡")
        text = text_from_rich_text(block.get("callout", {}).get("rich_text", []))
        children_md = ""
        if block.get("has_children"):
            children = get_block_children(block.get("id"))
            children_md = "\n\n".join([block_to_md(c, indent+1) for c in children])
        return f"{space}{icon} {text}\n\n{children_md}"
    if t == "toggle":
        text = text_from_rich_text(block.get("toggle", {}).get("rich_text", []))
        children_md = ""
        if block.get("has_children"):
            children = get_block_children(block.get("id"))
            children_md = "\n\n".join([block_to_md(c, indent+1) for c in children])
        return f"{space}<details>\n{space}<summary>{text}</summary>\n\n{children_md}\n{space}</details>"
    if t == "equation":
        expr = block.get("equation", {}).get("expression", "")
        # return inline math by default; the caller can choose how to render
        return f"${expr}$"
    # unknown/unsupported -> try to grab text if exists
    return text_from_rich_text(block.get(block.get("type", ""), {}).get("rich_text", [])) if block.get(block.get("type", ""), {}).get("rich_text") else ""

def page_blocks_to_md(page_id):
    # iterate first-level blocks and join; recursively handled in block_to_md where needed
    blocks = get_block_children(page_id)
    md_lines = []
    for b in blocks:
        md = block_to_md(b, indent=0)
        if md is not None:
            md_lines.append(md)
    return "\n\n".join(md_lines)

# ================== Front matter 格式化（与你的严格格式兼容） ==================
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
    lines.append(f'title: "{fm.get("title", "")}"')
    lines.append(f'date: {fm.get("date", "")}')

    # tags: support str or list
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [tags] if tags else []
    lines.append("tags:")
    if tags:
        for t in tags:
            lines.append(f"  - {t}")
    else:
        lines.append("  []")

    # categories: support str or list
    categories = fm.get("categories", [])
    if isinstance(categories, str):
        categories = [categories] if categories else []
    lines.append("categories:")
    if categories:
        for c in categories:
            lines.append(f"  - {c}")
    else:
        lines.append("  []")

    # other fields
    lines.append(f'comments: {str(fm.get("comments", True)).lower()}')
    lines.append(f'math: {str(fm.get("math", True)).lower()}')
    lines.append(f'mermaid: {str(fm.get("mermaid", True)).lower()}')
    lines.append(f'author: {fm.get("author", "unknown")}')
    lines.append("---\n")
    return "\n".join(lines)


# ================== 主保存逻辑（SaveDir + ImageDir 修复） ==================
def save_markdown(page):
    """
    保存页面为 Markdown（按 SaveDir/ImageDir 优先逻辑）
    - 仅在文章确实包含图片时才创建/清理 image dir 并下载图片
    - 图片在 markdown 中替换为以 / 开头的相对路径（基于仓库根）
    """
    # 元数据
    title = get_property_with_aliases(page, ["Title", "标题"], default="Untitled")
    slug_field = get_property_with_aliases(page, ["Slug", "slug"], default=None)
    slug = safe_slugify(slug_field) if (isinstance(slug_field, str) and slug_field.strip()) else safe_slugify(title)

    date = get_property_with_aliases(page, ["Date", "日期"], default=datetime.today().strftime("%Y-%m-%d"))
    tags = get_property_with_aliases(page, ["Tags", "标签"], default=[])
    categories = get_property_with_aliases(page, ["Categories", "Category", "分类"], default=[])
    author = get_property_with_aliases(page, ["Author", "作者"], default="unknown")
    comments = get_property_with_aliases(page, ["Comments", "comments"], default=True)
    math = get_property_with_aliases(page, ["Math", "math"], default=True)
    mermaid = get_property_with_aliases(page, ["Mermaid", "mermaid"], default=True)

    # SaveDir
    save_dir_field = get_property_with_aliases(page, ["SaveDir", "保存目录", "Save Dir"], default=None)
    save_dir_abs = normalize_user_path_to_abs(save_dir_field, DEFAULT_POSTS_BASE)

    # 先将页面内容转为 Markdown 文本（此处会产生 ![](url) 的占位）
    page_id = page.get("id")
    md_content = page_blocks_to_md(page_id)

    # 查找所有图片 URL（常见 markdown img 语法），不包括 data:, 空链等
    image_urls = re.findall(r'!\[.*?\]\((https?://[^\)\s]+)\)', md_content)
    has_images = len(image_urls) > 0

    # ImageDir 优先使用 Notion 配置，否则使用 DEFAULT_IMAGES_BASE/<slug>
    image_dir_field = get_property_with_aliases(page, ["ImageDir", "Image Dir", "图片目录"], default=None)
    image_dir_abs = None
    if has_images:
        if image_dir_field:
            image_dir_abs = normalize_user_path_to_abs(image_dir_field, DEFAULT_IMAGES_BASE)
        else:
            image_dir_abs = normalize_user_path_to_abs(os.path.join(DEFAULT_IMAGES_BASE, slug), DEFAULT_IMAGES_BASE)
        # 清理旧图片（仅当前文章目录）
        clean_dir_abs(image_dir_abs)

    # 替换 markdown 中的图片 URL -> 下载并替换为 /rel/path
    def repl_image(match):
        url = match.group(1)
        if not image_dir_abs:
            return match.group(0)  # 不处理
        local_abs = download_image_safe(url, image_dir_abs)
        if local_abs:
            rel = os.path.relpath(local_abs, ROOT_DIR).replace("\\", "/")
            return f"![](/" + rel + ")"
        else:
            return match.group(0)

    if has_images:
        md_content = re.sub(r'!\[.*?\]\((https?://[^\)\s]+)\)', repl_image, md_content)

    # front matter（images_dir 输出为相对路径，无前导斜杠；若无 images 则输出为空字符串）
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

    # 写入 Markdown
    mkdir_safe_abs(save_dir_abs)
    filename = f"{date}-{slug}.md"
    file_path = os.path.join(save_dir_abs, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(format_front_matter(fm))
        f.write("\n")
        f.write(md_content)

    print(f"✅ Saved: {file_path}  (images: {'yes' if has_images else 'no'})")
    return file_path


# ================== 入口 ==================
def main():
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        print("❌ NOTION_API_KEY and NOTION_DATABASE_ID must be set in environment.")
        return

    pages = query_database()
    if not pages:
        print("⚠️ No published pages found.")
        return

    out = []
    for p in pages:
        try:
            out.append(save_markdown(p))
        except Exception as e:
            print(f"❌ Error processing page {p.get('id')}: {e}")

    print(f"✅ Total saved: {len(out)}")

if __name__ == "__main__":
    main()
