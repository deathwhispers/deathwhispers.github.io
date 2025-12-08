import logging
import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Tuple
from urllib.parse import urlparse, unquote

import requests
import yaml

# ==========================================
#              用户配置区域 (可直接修改)
# ==========================================
SCAN_START_DIR = Path("_posts")  # 默认扫描路径
PROJECT_ROOT = Path(".").resolve()  # 假设脚本运行在项目根目录
IMAGE_ASSET_PREFIX = Path("assets/images")
FILE_ASSET_PREFIX = Path("assets/files")

# --- 脚本设置 ---
OVERWRITE_ORIGINAL = True
EXCLUDE_SCHEMES = {'http', 'https', 'ftp'}  # 仅处理这些外部链接
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
FILE_EXTENSIONS = {'.pdf', '.zip', '.rar', '.docx', '.pptx', '.xlsx', '.mp4', '.mp3', '.mov'}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | FILE_EXTENSIONS
MD_LINK_REGEX = re.compile(r'(!?\[.*?\]\s*\((.*?)\))')
WIKI_LINK_REGEX = re.compile(r'(!?\[\[(.*?)\]\])')  # 仅用来排除 Wiki Link

# ==========================================
#                 辅助函数
# ==========================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


def find_project_root(start_dir: Path, marker_file: str = ".git") -> Path:
    current = start_dir
    while current.parent != current:
        if (current / marker_file).exists():
            return current
        current = current.parent
    return start_dir


def slugify(text: str) -> str:
    """将文本转换为 URL 和文件名友好的 slug。"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'[-]+', '-', text)
    return text.strip('-')


def get_frontmatter(file_path: Path) -> Tuple[Dict[str, Any], str | None]:
    """鲁棒的 Frontmatter 读取函数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if not first_line.startswith('---'): return {}, "无 YAML 头部"
            yaml_lines = []
            for line in f:
                if line.strip() == '---': break
                yaml_lines.append(line)
            else:
                return {}, "YAML 头部未闭合"
            return yaml.safe_load("".join(yaml_lines)) or {}, None
    except Exception as e:
        return {}, str(e)


def format_date(date_obj) -> str | None:
    """标准化日期格式为 YYYY-MM-DD"""
    if not date_obj: return None
    try:
        if isinstance(date_obj, (datetime, date)):
            return date_obj.strftime('%Y-%m-%d')
        return str(date_obj).split(' ')[0]
    except:
        return None


def get_asset_base_path(md_file_path: Path, date_str: str | None = None, slug: str | None = None) -> Path:
    """根据 Markdown 文件路径和 Front Matter 信息计算资产存放的子目录 (例如: docker/2025-01-01-my-post)"""
    asset_base_parts = md_file_path.parent.parts[1:]

    if date_str and slug:
        final_stem = f"{date_str}-{slug}"
    else:
        final_stem = slugify(md_file_path.stem)

    return Path(*asset_base_parts) / final_stem


def download_asset_and_get_new_path(link_url: str, asset_type_dir: Path, base_dir_relative: Path,
                                    project_root: Path) -> str | None:
    """下载远程链接资源，并返回新的本地相对路径"""
    try:
        parsed_url = urlparse(link_url)
        path_decoded = unquote(parsed_url.path)

        # 尝试从 URL 路径中提取文件名，或使用通用名
        filename = Path(path_decoded).name
        if not filename or '.' not in filename:
            # 如果文件名不明确，尝试从链接中提取一个安全的命名
            ext = Path(path_decoded).suffix.lower() or '.dat'
            hash_part = hashlib.md5(link_url.encode()).hexdigest()[:8]
            filename = f"remote_asset_{hash_part}{ext}"

        new_local_path_relative = asset_type_dir / base_dir_relative / filename
        new_local_path_full = project_root / new_local_path_relative
        new_local_path_full.parent.mkdir(parents=True, exist_ok=True)

        if new_local_path_full.exists():
            logger.info(f"  [重用] 文件已存在，跳过下载: {new_local_path_relative}")
            return str(new_local_path_relative).replace(os.path.sep, '/')

        logger.info(f"  [下载] {link_url} -> {new_local_path_relative}")
        response = requests.get(link_url, stream=True, timeout=30)
        response.raise_for_status()
        with open(new_local_path_full, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return str(new_local_path_relative).replace(os.path.sep, '/')
    except Exception as e:
        logger.error(f"  [下载失败] {link_url}: {e}")
        return None


def remote_link_replacer(match: re.Match, md_file_path: Path, project_root: Path, base_dir_relative: Path) -> str:
    """处理 Markdown 链接匹配，执行下载和路径替换"""
    full_link = match.group(0)
    original_url = match.group(2)

    if not original_url or original_url.startswith('#'): return full_link

    parsed_url = urlparse(original_url)

    # 仅处理远程链接
    if parsed_url.scheme not in EXCLUDE_SCHEMES: return full_link

    path_suffix = Path(unquote(parsed_url.path)).suffix.lower()

    if path_suffix in IMAGE_EXTENSIONS:
        asset_type_dir = IMAGE_ASSET_PREFIX
    elif path_suffix in FILE_EXTENSIONS:
        asset_type_dir = FILE_ASSET_PREFIX
    else:
        logger.debug(f"  [跳过] 不支持的远程资源类型: {original_url}")
        return full_link

    new_path = download_asset_and_get_new_path(original_url, asset_type_dir, base_dir_relative, project_root)

    # 将链接从原始 URL 替换为新的本地相对路径
    if new_path:
        return full_link.replace(original_url, new_path)
    return full_link


# ==========================================
#                 主程序
# ==========================================

def process_single_markdown_file(md_file_path: Path, project_root: Path, overwrite: bool):
    """处理单个 Markdown 文件中的远程链接"""
    full_md_file_path = project_root / md_file_path

    metadata, _ = get_frontmatter(full_md_file_path)
    date_str = format_date(metadata.get('date'))
    slug = slugify(metadata.get('slug') or metadata.get('title') or md_file_path.stem)

    # 计算新的资产基础目录 (e.g., assets/images/docker/2025-01-01-my-post)
    base_dir_relative = get_asset_base_path(md_file_path, date_str, slug)

    output_file_path = full_md_file_path if overwrite else full_md_file_path.with_name(
        full_md_file_path.stem + "_remote_fixed" + full_md_file_path.suffix)

    logger.info(f"\n--- 处理远程链接: {md_file_path} ---")

    with open(full_md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 忽略 Wiki Links
    # 2. 处理标准 Markdown Links
    partial_md = lambda m: remote_link_replacer(m, md_file_path, project_root, base_dir_relative)

    # 替换前先确保内容中没有 Wiki Link，避免误替换
    if WIKI_LINK_REGEX.search(content):
        logger.warning("  [注意] 文件中包含 Wiki Links，本脚本将忽略它们。")

    new_content = MD_LINK_REGEX.sub(partial_md, content)

    if new_content != content:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        logger.info(f"  [完成] 文件已保存到: {output_file_path.name}")
    else:
        logger.info("  [跳过] 未发现需要下载或替换的远程链接。")


if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = find_project_root(SCRIPT_DIR)

    md_files = list(PROJECT_ROOT.glob(str(SCAN_START_DIR / "**/*.md")))
    logger.info(f"\n准备处理 {len(md_files)} 个 Markdown 文件中的远程链接...")

    for md_file in md_files:
        try:
            # 获取相对于项目根目录的路径
            relative_md_path = md_file.relative_to(PROJECT_ROOT)
            process_single_markdown_file(relative_md_path, PROJECT_ROOT, OVERWRITE_ORIGINAL)
        except Exception as e:
            logger.error(f"处理失败 {md_file}: {e}")
