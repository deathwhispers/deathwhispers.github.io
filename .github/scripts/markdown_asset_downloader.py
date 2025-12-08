import os
import re
import shutil
from pathlib import Path
from typing import Iterator, Dict, List
from urllib.parse import unquote

import yaml
from datetime import date, datetime

# --- 配置参数 ---

# Wiki Link 链接的正则表达式：匹配 [[...]] 或 ![[...]]
WIKI_LINK_REGEX = re.compile(r'(!?\[\[(.*?)\]\])')

# 标准 Markdown 链接的正则表达式
MD_LINK_REGEX = re.compile(r'(!?\[.*?\]\s*\((.*?)\))')

# 笔记文件的扩展名（用于识别非附件链接）
NOTE_EXTENSIONS = {'.md', '.markdown'}

# 扫描的起始目录
SCAN_START_DIR = Path("_posts")

# 资产存放目录前缀
IMAGE_ASSET_PREFIX = Path("assets/images")
FILE_ASSET_PREFIX = Path("assets/files")

# 是否直接覆盖原 Markdown 文件
OVERWRITE_ORIGINAL = True

# --- 支持的文件类型 ---
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
FILE_EXTENSIONS = {'.pdf', '.zip', '.rar', '.docx', '.pptx', '.xlsx', '.mp4', '.mp3'}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | FILE_EXTENSIONS

# 全局索引：文件名 -> [文件路径列表]
ATTACHMENT_INDEX: Dict[str, List[Path]] = {}

# --- 辅助函数 ---

def slugify(text: str) -> str:
    """
    将文本转换为 URL 和文件名友好的 slug。
    """
    text = str(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'[-]+', '-', text)
    return text.strip('-')

def find_project_root(start_dir: Path, marker_file: str = ".git") -> Path:
    """查找项目根目录（包含 .git 文件）。"""
    current = start_dir
    while current.parent != current:
        if (current / marker_file).exists():
            return current
        current = current.parent
    return start_dir

def find_markdown_files(root_dir: Path, scan_path: Path) -> Iterator[Path]:
    """查找所有 Markdown 文件。"""
    search_dir = root_dir / scan_path
    if not search_dir.is_dir():
        print(f"错误：扫描目录不存在: {search_dir}")
        return
    for path in search_dir.rglob('*.md'):
        yield path.relative_to(root_dir)

def get_frontmatter(file_path: Path):
    """鲁棒的 Frontmatter 读取函数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if not first_line.startswith('---'):
                return {}, "无 YAML 头部"
            yaml_lines = []
            for line in f:
                if line.strip() == '---':
                    break
                yaml_lines.append(line)
            else:
                return {}, "YAML 头部未闭合"
            return yaml.safe_load("".join(yaml_lines)) or {}, None
    except Exception as e:
        return {}, str(e)

def format_date(date_obj):
    """标准化日期格式为 YYYY-MM-DD (保留以防 Front Matter 处理需要)"""
    if not date_obj: return None
    try:
        if isinstance(date_obj, (datetime, date)):
            return date_obj.strftime('%Y-%m-%d')
        return str(date_obj).split(' ')[0]
    except:
        return None

def get_asset_base_path(md_file_path: Path, slug: str | None = None) -> Path:
    """
    根据 Markdown 文件路径和 slug 计算资产存放的子目录。
    目录结构为：(原始目录路径 - 排除第一个组件，如 _posts) / (slug)
    """
    # 1. 获取基础目录（排除项目根目录和集合名，例如从 _posts/a/b/file.md 得到 a/b）
    asset_base_parts = md_file_path.parent.parts[1:]

    # 2. 确定最终的目录名 (仅使用 Slug)
    if slug:
        final_stem = slug
    else:
        # 降级处理：使用文件名（并尝试移除 Jekyll 默认的日期前缀）
        filename_parts = md_file_path.stem.split('-')
        if len(filename_parts) > 3 and all(part.isdigit() for part in filename_parts[:3]):
            final_stem = "-".join(filename_parts[3:])
        else:
            final_stem = md_file_path.stem
        final_stem = slugify(final_stem)

    # 3. 组合：相对路径 + Slug (例如：a/b/my-post-slug)
    return Path(*asset_base_parts) / final_stem

def get_file_final_name(file_path: Path) -> str:
    """
    根据用户的要求，不再计算哈希，直接返回原始文件名。
    """
    return file_path.name

# --- 关键：构建全局索引 (用于路径解析) ---

def build_attachment_index(project_root: Path):
    """
    遍历整个项目，为所有支持的附件建立索引。
    """
    print("正在构建全局附件索引 (用于解析文件名链接)...")
    count = 0
    for path in project_root.rglob('*'):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            filename = path.name
            if filename not in ATTACHMENT_INDEX:
                ATTACHMENT_INDEX[filename] = []
            ATTACHMENT_INDEX[filename].append(path)
            count += 1
    print(f"索引构建完成。共索引 {count} 个附件。")

# --- 核心函数：本地资产标准化 (保持原名, 移动, 修正路径) ---

def standardize_local_asset(full_original_path: Path, asset_type_dir: Path, base_dir_relative: Path, project_root: Path) -> str | None:
    """
    对本地附件进行标准化处理：保持原名，移动到目标目录，返回项目根目录绝对链接。

    返回的链接格式为：/assets/[type]/[path]/[slug]/[filename]
    """
    # 1. 确定最终文件名（保持原名）
    final_filename = get_file_final_name(full_original_path)

    # 2. 构造新的相对路径和完整路径 (注意：目标路径包含文件名)
    new_local_path_relative = asset_type_dir / base_dir_relative / final_filename
    full_new_path = project_root / new_local_path_relative

    # 3. 执行移动/复制和清理操作

    # 明确使用 resolve() 确保比较的是绝对路径
    full_original_path_resolved = full_original_path.resolve()
    full_new_path_resolved = full_new_path.resolve()

    # 新增的调试日志
    print(f"  [原始路径]: {full_original_path_resolved.relative_to(project_root) if full_original_path_resolved.is_relative_to(project_root.resolve()) else full_original_path_resolved}")
    print(f"  [目标路径]: {full_new_path_resolved.relative_to(project_root)}")

    # 只有当源文件路径和目标文件路径不同时才需要执行文件操作
    if full_original_path_resolved != full_new_path_resolved:
        full_new_path.parent.mkdir(parents=True, exist_ok=True)

        try:

            if full_new_path.exists():
                # Case 1: 目标文件已存在（去重）。我们假设目标文件是正确的，仅需删除源文件。
                print(f"  [去重/清理] 目标位置已存在同名文件: {final_filename}.")

            else:
                # Case 2: 目标文件不存在。执行复制操作。
                shutil.copy2(full_original_path, full_new_path)
                print(f"  [复制成功] {full_original_path.name} -> {full_new_path.relative_to(project_root)}")

            # Final step: Remove the original file if it still exists (it should if we just copied it, or if we deduped).
            if full_original_path.exists():
                os.remove(full_original_path)
                print(f"  [删除成功] 源文件已清理: {full_original_path.relative_to(project_root)}")
            else:
                # This path is hit if the original path was somehow a bad link or already gone
                print(f"  [跳过删除] 源文件 {full_original_path.name} 已不存在.")

        except Exception as e:
            # 这里的异常会捕获复制失败或删除失败
            # 这里的失败意味着文件没有移动成功，所以不应该替换链接
            print(f"  [文件操作失败] 在处理 {full_original_path.name} 时发生错误: {e}. 请检查文件权限。")
            return None
    else:
        # Case 3: 源文件已经在正确位置，无需移动或复制
        print(f"  [跳过] 文件已在正确位置: {final_filename}. 链接路径: /{new_local_path_relative}")


    # 4. 返回项目根目录绝对链接 (以 / 开头)
    # 例如：/assets/images/ai/llm/abc/original_name.png
    return f'/{str(new_local_path_relative).replace(os.path.sep, "/")}'

# --- 核心函数：处理 Wiki Links ---

def replace_wiki_link(match: re.Match, md_file_path: Path, project_root: Path, base_dir_relative: Path) -> str:
    """处理 [[链接]] 格式，解析本地附件并标准化。"""
    full_link = match.group(0)
    raw_content = match.group(2).strip()

    if not raw_content: return full_link

    # 解析别名和文件名
    parts = raw_content.split('|')
    link_content = unquote(parts[0].strip())
    alt_text = parts[1].strip() if len(parts) > 1 else None

    # 检查链接是否指向附件
    link_path = Path(link_content)
    ext = link_path.suffix.lower()

    if ext in NOTE_EXTENSIONS:
        return full_link # 忽略内部笔记链接

    if ext in IMAGE_EXTENSIONS:
        asset_type_dir = IMAGE_ASSET_PREFIX
    elif ext in FILE_EXTENSIONS:
        asset_type_dir = FILE_ASSET_PREFIX
    else:
        return full_link # 忽略不支持的附件类型

    # 1. 查找本地文件
    full_original_path = None

    # --- 关键修改点：判断是否为项目根目录相对路径 ---
    is_project_root_relative = (
            '/' in link_content or
            '\\' in link_content or
            link_content.lower().startswith(str(IMAGE_ASSET_PREFIX).lower()) or
            link_content.lower().startswith(str(FILE_ASSET_PREFIX).lower())
    )

    if is_project_root_relative:
        # 路径查找（相对或绝对） - 尝试相对于项目根目录
        safe_path = link_content.lstrip('/')
        candidate = (project_root / safe_path).resolve()
        if candidate.exists():
            full_original_path = candidate
        else:
            # 尝试相对于 MD 文件目录
            candidate = ((project_root / md_file_path).parent / link_content).resolve()
            if candidate.exists():
                full_original_path = candidate
    else:
        # 索引查找（仅通过文件名）
        candidates = ATTACHMENT_INDEX.get(link_content)
        if not candidates:
            # 尝试不带扩展名的文件名查找 (如 [[image]])
            stem_match = next((p for n, paths in ATTACHMENT_INDEX.items() if n.split('.')[0] == link_content for p in paths), None)
            if stem_match:
                full_original_path = stem_match
            else:
                print(f"  [未找到] 索引中未找到文件: {link_content}")
                return full_link
        elif len(candidates) == 1:
            full_original_path = candidates[0]
        else:
            # 歧义处理：选择离 Markdown 文件最近的文件
            print(f"  [歧义] 文件名 '{link_content}' 存在 {len(candidates)} 个副本。")
            md_abs_path = (project_root / md_file_path).parent
            best_candidate = candidates[0]
            for cand in candidates:
                # 检查候选文件是否在 Markdown 文件的父路径下
                if md_abs_path in cand.parents:
                    best_candidate = cand
                    break
            print(f"  [解决] 自动选择: {best_candidate.relative_to(project_root)}")
            full_original_path = best_candidate

    if not full_original_path or not full_original_path.exists():
        return full_link

    # 2. 标准化处理 (移动/复制到新路径, 返回绝对链接)
    new_absolute_path_str = standardize_local_asset(
        full_original_path, asset_type_dir, base_dir_relative, project_root
    )

    if not new_absolute_path_str:
        return full_link

    # 3. 构造新的 Markdown 链接
    final_alt_text = alt_text if alt_text else full_original_path.stem

    # new_absolute_path_str 已经包含 / 开头
    if full_link.startswith('!'):
        return f'![{final_alt_text}]({new_absolute_path_str})'
    else:
        return f'[{final_alt_text}]({new_absolute_path_str})'

# --- 核心函数：处理标准 Markdown 链接 ---

def markdown_link_replacer(match: re.Match, md_file_path: Path, project_root: Path, base_dir_relative: Path) -> str:
    """处理 [文本](链接) 格式，解析本地附件并标准化。"""
    full_link = match.group(0)
    original_url = match.group(2)
    # 使用 unquote 解析 URL 编码，以确保查找路径正确
    original_url_unquoted = unquote(original_url)

    if not original_url_unquoted or original_url_unquoted.startswith(('#', 'http', 'https', 'ftp')):
        return full_link # 忽略锚点链接和远程链接

    # 检查链接是否指向附件
    ext = Path(original_url_unquoted).suffix.lower()

    if ext in IMAGE_EXTENSIONS: asset_type_dir = IMAGE_ASSET_PREFIX
    elif ext in FILE_EXTENSIONS: asset_type_dir = FILE_ASSET_PREFIX
    else: return full_link

    # 1. 查找本地文件

    # --- 关键修改点：判断是否为项目根目录相对路径 ---
    is_project_root_relative = (
            original_url_unquoted.startswith('/') or
            original_url_unquoted.lower().startswith(str(IMAGE_ASSET_PREFIX).lower().split('/')[0]) # 检查是否以 assets/ 开头
    )

    if is_project_root_relative:
        # 绝对路径 (相对于项目根目录)
        safe_path = original_url_unquoted.lstrip('/')
        full_original_path = (project_root / safe_path).resolve()
    else:
        # 相对路径 (相对于当前 Markdown 文件目录)
        full_original_path = ((project_root / md_file_path).parent / original_url_unquoted).resolve()

    if not full_original_path.exists():
        # 索引容错查找（应对路径错误但文件名正确的情况）
        filename = Path(original_url_unquoted).name
        if filename in ATTACHMENT_INDEX and len(ATTACHMENT_INDEX[filename]) == 1:
            full_original_path = ATTACHMENT_INDEX[filename][0]
            print(f"  [修正] 标准链接路径错误，通过索引找到文件: {filename}")
        else:
            return full_link

    # 2. 标准化处理 (移动/复制到新路径, 返回绝对链接)
    new_absolute_path_str = standardize_local_asset(
        full_original_path, asset_type_dir, base_dir_relative, project_root
    )

    if not new_absolute_path_str:
        return full_link

    # 3. 构造新的 Markdown 链接
    # 替换原始的 URL 部分为新的绝对路径
    return full_link.replace(original_url, new_absolute_path_str)

# --- 主程序 ---

def process_single_markdown_file(md_file_path: Path, project_root: Path, overwrite: bool):
    full_md_file_path = project_root / md_file_path

    # 读取 Front Matter 获取 slug
    metadata, _ = get_frontmatter(full_md_file_path)
    slug = metadata.get('slug') if metadata and 'slug' in metadata else None
    if not slug and metadata and 'title' in metadata:
        slug = slugify(metadata.get('title'))

    # 使用 slug 计算基础目录
    base_dir_relative = get_asset_base_path(md_file_path, slug)
    output_file_path = full_md_file_path if overwrite else full_md_file_path.with_name(full_md_file_path.stem + "_local" + full_md_file_path.suffix)

    print(f"\n--- 处理: {md_file_path} ---")
    if slug:
        print(f"  [标准化目录]: {IMAGE_ASSET_PREFIX / base_dir_relative} (基于文件路径和 slug: {slug})")
    else:
        print("  [警告]: 缺少 slug/title，资产目录将基于文件名和相对路径。")

    try:
        with open(full_md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件内容失败: {e}")
        return

    # 1. 处理 Wiki Links
    partial_wiki = lambda m: replace_wiki_link(m, md_file_path, project_root, base_dir_relative)
    content = WIKI_LINK_REGEX.sub(partial_wiki, content)

    # 2. 处理标准 Markdown Links
    partial_md = lambda m: markdown_link_replacer(m, md_file_path, project_root, base_dir_relative)
    content = MD_LINK_REGEX.sub(partial_md, content)

    # 写入文件
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"写入文件内容失败: {e}")

if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = find_project_root(SCRIPT_DIR)

    build_attachment_index(PROJECT_ROOT)

    md_files = list(find_markdown_files(PROJECT_ROOT, SCAN_START_DIR))
    print(f"\n准备处理 {len(md_files)} 个文件...")

    for md_file in md_files:
        try:
            process_single_markdown_file(md_file, PROJECT_ROOT, OVERWRITE_ORIGINAL)
        except Exception as e:
            print(f"处理失败 {md_file}: {e}")