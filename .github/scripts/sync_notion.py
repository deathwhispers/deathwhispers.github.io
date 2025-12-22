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
IMAGE_ASSET_PREFIX = os.path.join("assets", "images")  # /assets/images
FILE_ASSET_PREFIX = os.path.join("assets", "files")  # /assets/files

# ================== 加载本地 .env ==================
# 1. 判断是否在 GitHub Actions 环境中
# GITHUB_ACTIONS 环境变量在 GitHub Actions 运行时会自动设置为 'true'
is_github_actions = os.environ.get("GITHUB_ACTIONS") == "true"
if is_github_actions:
    # GitHub Actions 环境：
    # - 环境变量（如 secrets）已由 Action 自动注入
    # - 无需加载本地 .env 文件，避免不必要的磁盘操作或错误
    print("Running in GitHub Actions environment. Using injected secrets/variables.")
else:
    # 本地开发环境：
    # - 尝试加载本地的 .env 文件
    env_path = ROOT_DIR / ".env"

    if env_path.exists():
        # override=True 可确保本地 .env 覆盖系统变量
        load_dotenv(dotenv_path=env_path)
        print(f"Loaded environment variables from local {env_path}")
    else:
        print(
            f"Not running in GitHub Actions and local {env_path} not found. Proceeding with existing environment variables.")

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
    """将标题转换为 URL/文件名友好的 slug"""
    if not text:
        return "untitled"
    text = str(text).strip()
    # 保留字母、数字、中文、空格、连字符，其余替换为空
    text = re.sub(r'[^\w\s\-]', '', text)
    # 将连续空白或连字符转为单个 '-'
    # text = re.sub(r'[\s\-]+', '-', text)
    return text.strip('-')



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
    # 确保没有上级目录穿越
    if ".." in p:
        mkdir_safe(base_abs)
        return base_abs

    # 尝试构建绝对路径，如果用户路径以标准目录开头，则直接拼接
    if p.startswith(IMAGE_ASSET_PREFIX) or p.startswith(DEFAULT_POSTS_DIR):
        abs_path = os.path.join(ROOT_DIR, p)
    # 否则，相对于 default_base 拼接
    else:
        abs_path = os.path.join(ROOT_DIR, default_base, p)

    if not is_safe_subpath(ROOT_DIR, abs_path):
        mkdir_safe(base_abs)
        return base_abs

    mkdir_safe(abs_path)
    return abs_path


# ================== 图片下载 ==================
def download_image_to_dir(url: str, target_dir_abs: str) -> str | None:
    """
    下载图片到指定绝对目录，返回绝对路径或 None
    - target_dir_abs 已经是最终的 assets/images/{dir_structure}/{slug} 路径
    - 使用全局缓存避免重复下载
    """
    if url in _download_cache and os.path.exists(_download_cache[url]):
        return _download_cache[url]

    mkdir_safe(target_dir_abs)

    # 提取文件扩展名
    ext = os.path.splitext(url.split("?")[0])[1] or ".png"
    if not re.match(r"^\.[A-Za-z0-9]+$", ext):
        ext = ".png"

    # 生成唯一文件名
    abs_path = ""
    for _ in range(5):
        filename = uuid.uuid4().hex[:16] + ext
        abs_path = os.path.join(target_dir_abs, filename)
        if not os.path.exists(abs_path):
            break

    # 添加默认的伪装浏览器头部
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Referer': 'https://www.bilibili.com/'  # 针对 bilibili 的图片，最好伪造一个 Referer
    }

    headers = default_headers.copy()

    # 如果是 Notion 托管的图片，添加授权头
    if "notion.so" in url and NOTION_API_KEY and "amazonaws.com" not in url:
        headers["Authorization"] = f"Bearer {NOTION_API_KEY}"
        # 注意：对于 notion.so 的图片，可能不需要 default_headers 中的 Referer

    for attempt in range(1, REQUEST_RETRY + 1):
        try:
            # 使用合并后的 headers 发送请求
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
    """查询已发布或需要重新发布的页面"""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {
        "filter": {
            "or": [
                {"property": "Status", "select": {"equals": "Published"}},
                {"property": "Status", "select": {"equals": "Republish"}}
            ]
        }
    }
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
    """递归获取页面所有 block，支持分页"""
    results = []
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size={page_size}"
    has_more = True
    start_cursor = None

    while has_more:
        params = {}
        if start_cursor:
            params["start_cursor"] = start_cursor

        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            data = r.json()
            results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        except Exception as e:
            print(f"❌ Failed to fetch blocks for {page_id}: {e}")
            break

    return results


# ================== Markdown 转换 ==================
def _escape_liquid(s: str) -> str:
    """
    避免触发 Liquid 的 {{ ... }}，把 '{{' -> '{ {'，'}}' -> '} }'
    保持视觉上几乎相同但不被 Liquid 解析。
    """
    return s.replace("{{", "{ {").replace("}}", "} }")


def _normalize_equation_for_inline(expr: str) -> str:
    """
    把公式适配为行内形式：
    - 删除首尾多余空白和换行
    - 把内部换行换成空格
    - 转义可能与 Liquid 冲突的花括号
    - 最终用 $...$ 包裹（如果已包含 $ 则只清理）
    """
    if not expr:
        return ""
    # 清理首尾空白并把多行合并为单行（表格单元格应为行内）
    expr = expr.strip()
    expr = re.sub(r'\s*\n\s*', ' ', expr)
    # 避免 Liquid 解析
    # expr = _escape_liquid(expr)
    # 如果已经包含 $，则直接返回（保护原貌），否则包 $...$
    if "$" in expr:
        return expr
    return f"${expr}$"


def text_from_rich_text(rich_list: list[dict]) -> str:
    """
    富文本列表转换为 Markdown 文本，正确处理链接、注释、公式。
    行内公式( rich item of type 'equation' ) 会生成 $...$。
    """
    if not rich_list:
        return ""

    parts = []
    for r in rich_list:
        ttype = r.get("type")
        # 基础文本
        content = r.get("plain_text", "")

        # ============ Equation (inline) ============
        if ttype == "equation":
            expr = r.get("equation", {}).get("expression", "").strip()
            content = _normalize_equation_for_inline(expr)
            if not content:
                continue

        # ============ Text ============
        elif ttype == "text":
            href = r.get("href")
            if href:
                content = f"[{content}]({href})"

            # 注释（annotations）
            ann = r.get("annotations", {}) or {}
            # code highest priority
            if ann.get("code"):
                content = f"`{content}`"
            if ann.get("bold"):
                content = f"**{content}**"
            if ann.get("italic"):
                content = f"*{content}*"
            if ann.get("strikethrough"):
                content = f"~~{content}~~"
            if ann.get("underline"):
                content = f"<ins>{content}</ins>"

        # 其他类型（mention、date 等）— 使用 plain_text
        else:
            content = r.get("plain_text", "")

        if content:
            # 最后统一做 Liquid 保护（对普通文本我们通常不修改花括号，但为安全在公式以外也保护可能的 '{{' 出现）
            # content = _escape_liquid(content)
            parts.append(content)

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
        if expr:
            # 避免触发 Liquid
            expr = expr.replace("{{", "{ {").replace("}}", "} }")
            return f"\n$$\n{expr}\n$$\n"
        return ""
    # ========== table ==========
    if t == "table":
        # 获取表格行（Notion 的 table block 子节点是 table_row）
        rows = get_block_children(block.get("id"))
        if not rows:
            return ""

        # helper: sanitize cell content for markdown table
        def _sanitize_cell(cell_text: str) -> str:
            if cell_text is None:
                return ""
            # 把行内的 $$...$$ 或块级 $$...$$ 转为单行行内 $...$（表格内不适合多行块级）
            # 先去掉首尾空白
            s = str(cell_text).strip()
            # 把块级 $$...$$ -> $...$
            s = re.sub(r'\$\$\s*(.*?)\s*\$\$', lambda m: _normalize_equation_for_inline(m.group(1)), s, flags=re.S)
            # 把单行内可能包含换行的内容换成 <br>，避免破坏表格布局
            s = s.replace("\n", "<br>")
            # 转义竖线 '|'（以防分栏错误）
            s = s.replace("|", "&#124;")
            return s

        table_lines = []
        # First row will be header if table has header row (Notion tables usually first row is header)
        # We'll treat the first row as header always (user can control in Notion)
        for idx, row in enumerate(rows):
            if row.get("type") != "table_row":
                continue
            cells = row.get("table_row", {}).get("cells", [])
            # cells is list of rich_text arrays per cell
            cell_texts = []
            for cell in cells:
                # each cell is a rich_text array
                cell_md = text_from_rich_text(cell)
                cell_md = _sanitize_cell(cell_md)
                cell_texts.append(cell_md)
            # ensure consistent column count by padding with empty cells
            col_count = max(len(r.get("table_row", {}).get("cells", [])) for r in rows if r.get("type") == "table_row")
            if len(cell_texts) < col_count:
                cell_texts.extend([""] * (col_count - len(cell_texts)))
            line = "| " + " | ".join(cell_texts) + " |"
            table_lines.append(line)
            # insert header separator after first row
            if idx == 0:
                table_lines.append("| " + " | ".join(["---"] * len(cell_texts)) + " |")
        # add blank line before and after table to be safe in Markdown rendering
        return "\n\n" + "\n".join(table_lines) + "\n\n"

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
    """
    根据输入字典 (fm) 的键顺序动态生成 front matter，格式化规则基于值类型。
    fm: 传入的字典，键的顺序即为输出的顺序。
    """
    lines = ["---"]

    # 定义特殊字段的默认值（仅用于值为 None 或空字符串时填充）
    default_values = {
        "layout": "post",
        "author": "deathwhispers"
    }

    # 遍历输入的字典，使用其顺序
    for key, val in fm.items():
        if val is None:
            val = default_values.get(key)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            continue
        if isinstance(val, (list, tuple)):
            vals = val
            lines.append(f"{key}:")
            if vals:
                for v in vals:
                    # 列表元素如果包含空格或特殊字符，最好用引号包裹
                    if isinstance(v, str) and (' ' in v or ':' in v):
                        lines.append(f"  - \"{v}\"")
                    else:
                        lines.append(f"  - {v}")
            else:
                lines.append("  []")
        # 布尔值处理 (Boolean)
        elif isinstance(val, bool):
            # YAML 约定布尔值应小写
            lines.append(f"{key}: {str(val).lower()}")

        # 字符串/数字/日期处理 (String, Number, Date)
        else:
            output_val = val

            # 对于字符串值，如果包含空格或 YAML 特殊字符 (如:冒号)，最好用双引号包裹
            if isinstance(val, str) and (' ' in val or ':' in val):
                output_val = f'"{val}"'
            lines.append(f"{key}: {output_val}")
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
    title = get_property_with_aliases(page, ["Title", "标题"], default="Untitled")
    slug_field = get_property_with_aliases(page, ["Slug", "slug"], default=None)
    slug = safe_slugify(slug_field) if slug_field else safe_slugify(title)
    date = get_property_with_aliases(page, ["Date", "日期"], default=datetime.today().strftime("%Y-%m-%d"))
    status = get_property_with_aliases(page, ["Status", "状态"], default="Draft")

    if status == "Draft":
        print(f"⚪ Skipped (Draft): {title}")
        return ""

    # 1. 获取文章保存的绝对目录
    save_dir_field = get_property_with_aliases(page, ["SaveDir", "保存目录", "Save Dir"], default=None)
    save_dir_abs = normalize_path(save_dir_field, DEFAULT_POSTS_DIR)
    mkdir_safe(save_dir_abs)

    # 2. 提取文章目录结构 (例如 'ai/deepseek')
    # a. 获取 save_dir_abs 相对于 ROOT_DIR 的相对路径
    save_dir_rel = os.path.relpath(save_dir_abs, ROOT_DIR).replace("\\", "/")
    # b. 移除默认的 _posts/ 前缀（如果存在）
    posts_prefix = DEFAULT_POSTS_DIR.replace("\\", "/") + "/"
    if save_dir_rel.startswith(posts_prefix):
        # 提取出用户定义的目录部分（例如 'ai/deepseek'）
        article_dir_structure = save_dir_rel[len(posts_prefix):].rstrip("/")
    else:
        # 如果 save_dir_rel 不是以 _posts 开头 (非常规情况)，则用空字符串
        article_dir_structure = ""

    # 3. 构造标准化图片目录路径
    # 路径结构: ROOT_DIR / assets/images / {article_dir_structure} / {slug}
    # 确保使用 / 分隔符，以便在路径拼接时与 os.path.join 配合
    image_base_abs = os.path.join(ROOT_DIR, IMAGE_ASSET_PREFIX)
    # post_image_dir 是图片的最终绝对路径
    post_image_dir = os.path.join(image_base_abs, article_dir_structure, slug)

    # 文件名使用 date-title 格式 (根据您上一个请求的修改)
    file_title_safe = safe_slugify(title)
    file_path = os.path.join(save_dir_abs, f"{date}-{file_title_safe}.md")

    # Republish 逻辑
    if status == "Republish":
        print(f"⚪ Update (Republish): {title}")

        # 尝试删除旧文件（date-slug 和 date-title 两种格式）
        old_slug_file_path = os.path.join(save_dir_abs, f"{date}-{slug}.md")

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑 Deleted existing file: {file_path}")
        if os.path.exists(old_slug_file_path) and old_slug_file_path != file_path:
            os.remove(old_slug_file_path)
            print(f"🗑 Deleted old slug-based file: {old_slug_file_path}")

        # 删除旧图片目录
        if os.path.exists(post_image_dir):
            shutil.rmtree(post_image_dir)
            print(f"🗑 Deleted old images: {post_image_dir}")

    if os.path.exists(file_path):
        print(f"⚪ Skipped (file exists): {file_path}")
        return file_path

    page_id = page.get("id")
    md_content = page_to_markdown(page_id)

    fm = {
        "layout": "post",
        "title": title,
        "slug": slug,
        "status": status,
        "date": date,
        "tags": get_property_with_aliases(page, ["Tags", "标签"], default=[]),
        "categories": get_property_with_aliases(page, ["Categories", "Category", "分类"], default=[]),
        "author": get_property_with_aliases(page, ["Author", "作者"], default="unknown")
    }
    new_content = format_front_matter(fm) + "\n" + md_content

    # 图片处理逻辑 - 下载到新的标准化路径
    image_urls = re.findall(r'!\[.*?\]\((https?://[^\)\s]+)\)', md_content)
    if image_urls:
        mkdir_safe(post_image_dir)

        def repl_img(match):
            url = match.group(1)
            if not url or url.startswith("data:"):
                return match.group(0)

            # download_image_to_dir 使用 post_image_dir (已包含 article_dir_structure)
            local_path = download_image_to_dir(url, post_image_dir)

            if local_path:
                # 构造相对路径：/assets/images/{article_dir_structure}/{slug}/filename.ext
                rel = os.path.relpath(local_path, ROOT_DIR).replace("\\", "/")
                return f"![](/" + rel + ")"
            return match.group(0)

        new_content = re.sub(r'!\[.*?\]\((https?://[^\)\s]+)\)', repl_img, new_content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"🟢 Created: {file_path}")
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
            status = get_property_with_aliases(page, ["Status", "状态"], default="Draft")
            if status == "Draft":
                print(f"⚪ Skipped (Draft): {get_property_with_aliases(page, ['Title', '标题'], 'Untitled')}")
                continue
            saved_file = save_page_markdown(page)
            if saved_file:
                saved_files.append(saved_file)
        except Exception as e:
            print(f"❌ Error processing page {page.get('id')}: {e}")

    print(f"✅ Total saved: {len(saved_files)}")


if __name__ == "__main__":
    main()
