import os
import re
import shutil
from pathlib import Path
from typing import Iterator
from urllib.parse import urlparse, unquote

import requests

# --- 配置参数 ---

# Wiki Link 链接的正则表达式：匹配 [[...]] 或 ![[...]]
# 捕获组 1: 完整的 Wiki Link (e.g., [[image.png]] 或 ![[image.png]])
# 捕获组 2: 链接内容 (image.png)
WIKI_LINK_REGEX = re.compile(r'(!?\[\[(.*?)\]\])')

# 笔记文件的扩展名（用于判断是否保留 Wiki Link）
NOTE_EXTENSIONS = ('.md', '.markdown')

# 扫描的起始目录（相对于项目根目录）。脚本将递归查找该目录下的所有 .md 文件。
SCAN_START_DIR = Path("_posts/ai/llm")

# 项目根目录路径。脚本将尝试自动查找。
PROJECT_ROOT = Path(__file__).resolve().parent

# 下载的图片和文件存放的目录前缀（相对于项目根目录）
IMAGE_ASSET_PREFIX = Path("assets/images")
FILE_ASSET_PREFIX = Path("assets/files")

# 是否直接覆盖原 Markdown 文件。设置为 True 则不会生成 _local 文件。
OVERWRITE_ORIGINAL = True

# --- 通用设置 ---
EXCLUDE_SCHEMES = ('http', 'https', 'ftp', 'mailto', 'tel')
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')
FILE_EXTENSIONS = ('.pdf', '.zip', '.rar', '.docx', '.pptx', '.xlsx')
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS + FILE_EXTENSIONS
MD_LINK_REGEX = re.compile(r'(!?\[.*?\]\s*\((.*?)\))')


# --- 辅助函数：文件查找与路径计算 ---

def find_project_root(start_dir: Path, marker_file: str = ".git") -> Path:
    """尝试向上查找项目根目录（通过 .git 或其他标识）。"""
    current = start_dir
    print(f"尝试从 {current} 向上查找项目根目录...")
    while current.parent != current:
        if (current / marker_file).exists():
            print(f"找到项目根目录标识 {marker_file}，确定根目录为: {current}")
            return current
        current = current.parent
    print(f"警告：未找到项目根目录标识文件 {marker_file}。将使用脚本所在目录作为根目录: {start_dir}")
    return start_dir


def find_markdown_files(root_dir: Path, scan_path: Path) -> Iterator[Path]:
    """递归查找指定路径下的所有 Markdown 文件。"""
    search_dir = root_dir / scan_path
    if not search_dir.is_dir():
        print(f"错误：扫描目录不存在或不是目录: {search_dir}")
        return
    print(f"开始扫描目录: {search_dir.relative_to(root_dir)} ...")
    for path in search_dir.rglob('*.md'):
        yield path.relative_to(root_dir)


def get_asset_base_path(md_file_path: Path) -> Path:
    """根据 Markdown 文件的路径生成资产存储的子目录名称。"""
    # 移除第一个目录（如_posts）
    asset_base_parts = md_file_path.parent.parts[1:]

    # 尝试处理 Jekyll 格式的文件名 (YYYY-MM-DD-title.md)
    filename_parts = md_file_path.stem.split('-')
    if len(filename_parts) > 3 and all(part.isdigit() for part in filename_parts[:3]):
        final_stem = "-".join(filename_parts[3:])
    else:
        final_stem = md_file_path.stem

    base_dir_relative = Path(*asset_base_parts) / final_stem
    return base_dir_relative


# --- 核心函数：下载 ---

def download_asset_and_get_new_path(
        link_url: str,
        asset_type_dir: Path,
        base_dir_relative: Path,
        project_root: Path
) -> str | None:
    """下载远程链接资源，并返回其新的相对路径。"""
    try:
        parsed_url = urlparse(link_url)
        path_decoded = unquote(parsed_url.path)
        path_parts = Path(path_decoded).parts

        if not path_parts:
            filename = "downloaded_asset"
            ext = ""
        else:
            filename = Path(path_decoded).name
            ext = Path(path_decoded).suffix

        # 确保文件名中包含扩展名
        if not ext and asset_type_dir == IMAGE_ASSET_PREFIX:
            filename += ".png"
        elif not ext and asset_type_dir == FILE_ASSET_PREFIX:
            filename += ".bin"

            # 构造本地存储路径：<asset_type_dir>/<base_dir_relative>/<文件名>
        new_local_path_relative = asset_type_dir / base_dir_relative / filename
        new_local_path_full = project_root / new_local_path_relative

        new_local_path_full.parent.mkdir(parents=True, exist_ok=True)

        if new_local_path_full.exists():
            return str(new_local_path_relative).replace(os.path.sep, '/')

        print(f"  [下载] 正在下载 {link_url} -> {new_local_path_full.relative_to(project_root)}")

        response = requests.get(link_url, stream=True, timeout=30)
        response.raise_for_status()

        with open(new_local_path_full, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return str(new_local_path_relative).replace(os.path.sep, '/')

    except requests.exceptions.RequestException as e:
        print(f"  [错误] 下载失败 {link_url}: {e}")
        return None
    except Exception as e:
        print(f"  [致命错误] 处理链接时发生异常 {link_url}: {e}")
        return None


def replace_wiki_link(match: re.Match, md_file_path: Path, project_root: Path, base_dir_relative: Path) -> str:
    """
    处理 Wiki Link 格式的引用，将图片/文件标准化，保留 Markdown 笔记链接。

    Args:
        md_file_path: Markdown 文件的相对路径 (相对于 project_root)。
    """
    full_link = match.group(0)
    link_content = match.group(2).strip()

    if not link_content:
        return full_link

    link_path = Path(link_content)
    ext = link_path.suffix.lower()

    # 【修复 NameError 关键步骤】构造 MD 文件的绝对路径
    full_md_file_path = project_root / md_file_path

    # 1. 【修正保留逻辑】如果引用的是笔记文件（.md/.markdown），则保留 Wiki Link 格式
    if ext in NOTE_EXTENSIONS:
        print(f"  [保留] 笔记链接 Wiki Link (MD): {full_link}")
        return full_link

    # 2. 确定资产类型目录
    if ext in IMAGE_EXTENSIONS:
        asset_type_dir = IMAGE_ASSET_PREFIX
    elif ext in FILE_EXTENSIONS:
        asset_type_dir = FILE_ASSET_PREFIX
    else:
        # 如果不是图片也不是已配置的文件附件，则保留原样
        print(f"  [警告] Wiki Link 扩展名不在配置列表中，跳过: {ext}")
        return full_link

    # 3. 找到原始文件路径 (Wiki Link 默认是相对于项目根目录的)
    full_original_path = (project_root / link_content).resolve()

    # 检查文件是否存在 (兼容某些笔记软件可能在 MD 文件父目录)
    if not full_original_path.exists() or not full_original_path.is_file():
        # 现在 full_md_file_path 已经被正确定义
        full_original_path = (full_md_file_path.parent / link_content).resolve()

        if not full_original_path.exists() or not full_original_path.is_file():
            print(f"  [警告] Wiki Link 文件不存在，跳过标准化: {link_content}")
            return full_link

    # 4. 构造标准化后的新路径 (移动目标)
    new_local_path_relative = asset_type_dir / base_dir_relative / full_original_path.name
    full_new_path = project_root / new_local_path_relative

    # 5. 移动文件
    if full_original_path.resolve() != full_new_path.resolve():
        print(f"  [移动 Wiki] 移动本地资产: {full_original_path.relative_to(project_root)} -> {new_local_path_relative}")
        full_new_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(full_original_path, full_new_path)
        except Exception as e:
            print(f"  [移动失败] 无法移动 Wiki 文件 {full_original_path}: {e}")
            return full_link

    # 6. 构造标准的 Markdown 引用格式
    new_relative_path_str = str(new_local_path_relative).replace(os.path.sep, '/')

    # 【修正输出逻辑】根据是否带 '!' 来决定是图片嵌入还是普通链接
    if full_link.startswith('!'):
        # 原始链接带 !，转换为嵌入式图片/文件
        new_markdown_link = f'![{full_original_path.stem}]({new_relative_path_str})'
    else:
        # 原始链接不带 !，转换为标准链接（附件）
        new_markdown_link = f'[{full_original_path.stem}]({new_relative_path_str})'

    print(f"  [转换] Wiki Link {full_link} -> {new_markdown_link}")
    return new_markdown_link

# --- 核心函数：处理单个文件 (重点修改) ---
def process_single_markdown_file(md_file_path: Path, project_root: Path, overwrite: bool):
    """
    处理单个 Markdown 文件，包括：
    1. 标准化 Wiki Links (图片/文件，保留笔记链接)。
    2. 下载远程链接资产。
    3. 标准化所有不符合规范的本地链接。
    """
    # 确定资产存储的基目录
    base_dir_relative = get_asset_base_path(md_file_path)

    full_md_file_path = project_root / md_file_path

    # 确定输出路径
    if overwrite:
        output_file_path = full_md_file_path
    else:
        output_file_path = full_md_file_path.with_name(full_md_file_path.stem + "_local" + full_md_file_path.suffix)

    print(f"\n--- 正在处理文件: {md_file_path} ---")
    print(f"--- 资产子目录: {base_dir_relative} ---")

    # --- 嵌套替换函数：处理标准 Markdown Links ---
    def markdown_link_replacer(match: re.Match) -> str:
        full_link = match.group(0)
        original_url = match.group(2)

        if not original_url or original_url.startswith('#'):
            return full_link

        parsed_url = urlparse(original_url)

        # 确定文件扩展名和资产类型目录
        ext = Path(unquote(parsed_url.path)).suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            asset_type_dir = IMAGE_ASSET_PREFIX
        elif ext in FILE_EXTENSIONS:
            asset_type_dir = FILE_ASSET_PREFIX
        else:
            return full_link

        new_relative_path_str = None

        # --- A. 远程链接处理 (包含 http/https) ---
        if parsed_url.scheme in EXCLUDE_SCHEMES:
            # 远程链接：执行下载和替换逻辑
            new_relative_path_str = download_asset_and_get_new_path(
                original_url,
                asset_type_dir,
                base_dir_relative,
                project_root
            )

        # --- B. 本地链接处理 (标准化不符合规范的引用) ---
        else:
            original_url_path = Path(original_url)

            # 【修正本地路径逻辑】启发式判断：以 '/' 开头，或以 'assets/'/'files/' 开头，视为项目根目录相对路径
            is_root_relative = original_url.startswith('/') or \
                               original_url.startswith(str(IMAGE_ASSET_PREFIX.parts[0])) or \
                               original_url.startswith(str(FILE_ASSET_PREFIX.parts[0]))

            if is_root_relative:
                # 根目录相对路径：从项目根目录开始计算
                full_original_path = (project_root / original_url.lstrip('/')).resolve()
            else:
                # 相对路径：从 MD 文件所在目录开始计算
                full_original_path = (full_md_file_path.parent / original_url).resolve()

            # 确保文件存在
            if not full_original_path.exists() or not full_original_path.is_file():
                print(f"  [警告] 本地链接文件不存在或非文件，跳过标准化: {full_original_path}")
                return full_link

            # 构造标准化后的新路径
            new_local_path_relative = asset_type_dir / base_dir_relative / full_original_path.name
            full_new_path = project_root / new_local_path_relative

            # 如果原文件不在新标准路径，则进行移动
            if full_original_path.resolve() != full_new_path.resolve():
                print(
                    f"  [移动 MD] 移动本地资产: {full_original_path.relative_to(project_root)} -> {new_local_path_relative}")
                full_new_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(full_original_path, full_new_path)
                except Exception as e:
                    print(f"  [移动失败] 无法移动文件 {full_original_path}: {e}")
                    return full_link

            # 返回标准化后的引用路径
            new_relative_path_str = str(new_local_path_relative).replace(os.path.sep, '/')
            # print(f"  [标准化] {original_url} -> {new_relative_path_str}")

        if new_relative_path_str:
            new_link = full_link.replace(original_url, new_relative_path_str)
            return new_link
        else:
            return full_link

    # --- 执行替换 ---
    try:
        # 1. 读取文件内容
        with open(full_md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 2. 替换 WIKI LINKS (首先处理，将 ![[...]] 和 [[附件.ext]] 转换为标准 MD 链接)
        wiki_link_replacer_partial = lambda match: replace_wiki_link(match, full_md_file_path.relative_to(project_root), project_root, base_dir_relative)
        content_after_wiki = WIKI_LINK_REGEX.sub(wiki_link_replacer_partial, content)

        # 3. 替换标准 MD LINKS (处理远程链接和剩余的本地链接)
        final_content = MD_LINK_REGEX.sub(markdown_link_replacer, content_after_wiki)

        # 4. 将修改后的内容写入文件
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"--- 写入成功: {output_file_path.relative_to(project_root)} ---")

    except FileNotFoundError:
        print(f"错误：文件未找到 {full_md_file_path}")
    except Exception as e:
        print(f"处理文件 {md_file_path} 时发生错误: {e}")



# --- 主程序入口 ---
if __name__ == "__main__":

    # 1. 确定项目根目录
    PROJECT_ROOT = find_project_root(Path(__file__).resolve().parent)

    # 2. 创建所有必要的顶级目录
    (PROJECT_ROOT / IMAGE_ASSET_PREFIX).mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / FILE_ASSET_PREFIX).mkdir(parents=True, exist_ok=True)

    # 3. 扫描并批量处理文件
    processed_count = 0
    md_files_to_process = list(find_markdown_files(PROJECT_ROOT, SCAN_START_DIR))

    if not md_files_to_process:
        print(f"\n没有在 {SCAN_START_DIR} 目录下找到任何 .md 文件，请检查配置。")
    else:
        print(f"\n--- 准备处理 {len(md_files_to_process)} 个文件 ---")

        for md_file_path in md_files_to_process:
            try:
                # 调用单个文件处理函数
                process_single_markdown_file(
                    md_file_path=md_file_path,
                    project_root=PROJECT_ROOT,
                    overwrite=OVERWRITE_ORIGINAL
                )
                processed_count += 1
            except Exception as e:
                print(f"主循环中处理 {md_file_path} 失败: {e}")
                continue

        print(f"\n==========================================")
        print(f"批量处理完成。成功处理了 {processed_count} 个文件。")
        print(f"==========================================")
