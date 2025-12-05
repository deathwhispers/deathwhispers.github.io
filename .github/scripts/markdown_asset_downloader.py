import os
import re
import shutil
from pathlib import Path
from typing import Iterator
from urllib.parse import urlparse, unquote

import requests

# --- 配置参数 ---

# 扫描的起始目录（相对于项目根目录）。脚本将递归查找该目录下的所有 .md 文件。
SCAN_START_DIR = Path("_posts/learning/database/redis")

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


# --- 辅助函数：文件查找与路径计算 (与上一版保持一致) ---

def find_project_root(start_dir: Path, marker_file: str = ".git") -> Path:
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
    search_dir = root_dir / scan_path
    if not search_dir.is_dir():
        print(f"错误：扫描目录不存在或不是目录: {search_dir}")
        return

    print(f"开始扫描目录: {search_dir.relative_to(root_dir)} ...")
    for path in search_dir.rglob('*.md'):
        yield path.relative_to(root_dir)


def get_asset_base_path(md_file_path: Path) -> Path:
    filename_parts = md_file_path.stem.split('-')

    if len(filename_parts) > 3 and all(part.isdigit() for part in filename_parts[:3]):
        final_stem = "-".join(filename_parts[3:])
    else:
        final_stem = md_file_path.stem

    # 移除第一个目录（如_posts）
    asset_base_parts = md_file_path.parent.parts[1:]

    base_dir_relative = Path(*asset_base_parts) / final_stem
    return base_dir_relative


# --- 核心函数：下载 (与上一版保持一致) ---

def download_asset_and_get_new_path(
        link_url: str,
        asset_type_dir: Path,
        base_dir_relative: Path,
        project_root: Path
) -> str | None:
    # ... (下载逻辑，略去代码，与 V2/V1 版本保持一致)

    try:
        parsed_url = urlparse(link_url)
        path_decoded = unquote(parsed_url.path)
        path_parts = Path(path_decoded).parts
        relative_url_path = Path(*path_parts[1:])

        filename = relative_url_path.name

        # 构造本地存储路径：<asset_type_dir>/<base_dir_relative>/<文件名>
        new_local_path_relative = asset_type_dir / base_dir_relative / relative_url_path.name
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


# --- 核心函数：处理单个文件 (重点修改) ---

def process_single_markdown_file(md_file_path: Path, project_root: Path, overwrite: bool):
    """
    处理单个 Markdown 文件的核心逻辑，包括远程下载和本地路径标准化。
    """
    base_dir_relative = get_asset_base_path(md_file_path)
    full_md_file_path = project_root / md_file_path

    # 确定输出路径
    output_file_path = full_md_file_path if overwrite else full_md_file_path.with_name(
        full_md_file_path.stem + "_local" + full_md_file_path.suffix)

    print(f"\n--- 正在处理文件: {md_file_path} ---")
    print(f"--- 资产子目录: {base_dir_relative} ---")

    try:
        with open(full_md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        def replace_link(match: re.Match) -> str:
            full_link = match.group(0)
            original_url = match.group(2)

            # 1. 预检查：确保链接不是空或锚点
            if not original_url or original_url.startswith('#'):
                return full_link

            # 2. 确定链接类型和资产目录
            parsed_url = urlparse(original_url)

            ext = Path(unquote(parsed_url.path)).suffix.lower()
            if ext in IMAGE_EXTENSIONS:
                asset_type_dir = IMAGE_ASSET_PREFIX
            elif ext in FILE_EXTENSIONS:
                asset_type_dir = FILE_ASSET_PREFIX
            else:
                return full_link  # 不支持的扩展名，保留原链接

            new_relative_path_str = None

            # --- A. 远程链接处理 (包含 http/https) ---
            if parsed_url.scheme in EXCLUDE_SCHEMES:
                # 远程链接：执行下载和替换逻辑 (与 V2 版本一致)
                new_relative_path_str = download_asset_and_get_new_path(
                    original_url,
                    asset_type_dir,
                    base_dir_relative,
                    project_root
                )

            # 本地链接处理 (不包含 scheme 或 scheme 为空)
            else:
                # 1. 尝试解析出本地文件的绝对路径
                original_url_path = Path(original_url)

                # 启发式判断：如果链接以 '/' 开头，或者以 'assets/' (或 'files/') 开头
                # 我们就将其视为相对于项目根目录的绝对路径引用。
                is_root_relative = original_url.startswith('/') or \
                                   original_url.startswith(str(IMAGE_ASSET_PREFIX.parts[0])) or \
                                   original_url.startswith(str(FILE_ASSET_PREFIX.parts[0]))

                if is_root_relative:
                    # 链接被视为相对于项目根目录（无论是否带 /）
                    full_original_path = (project_root / original_url.lstrip('/')).resolve()
                else:
                    # 链接是相对于 Markdown 文件所在目录的相对路径（如 ../img.png）
                    full_original_path = (full_md_file_path.parent / original_url).resolve()

                # 2. 确保文件存在
                if not full_original_path.exists() or not full_original_path.is_file():
                    print(f"  [警告] 本地链接文件不存在或非文件，跳过标准化: {full_original_path}")
                    return full_link

                # 3. 构造标准化后的新路径 (相对于项目根目录)
                # ... (后续逻辑保持不变，确保移动和替换操作正确执行) ...

                # 构造目标新路径: <asset_type_dir>/<base_dir_relative>/<文件名>
                new_local_path_relative = asset_type_dir / base_dir_relative / full_original_path.name
                full_new_path = project_root / new_local_path_relative

                # 4. 如果原文件不在新标准路径，则进行移动
                if full_original_path != full_new_path.resolve():
                    print(
                        f"  [移动] 移动本地资产: {full_original_path.relative_to(project_root)} -> {new_local_path_relative}")
                    full_new_path.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.move(full_original_path, full_new_path)
                    except Exception as e:
                        print(f"  [移动失败] 无法移动文件 {full_original_path}: {e}")
                        return full_link

                # 5. 返回标准化后的引用路径
                new_relative_path_str = str(new_local_path_relative).replace(os.path.sep, '/')
                print(f"  [标准化] {original_url} -> {new_relative_path_str}")

            if new_relative_path_str:
                new_link = full_link.replace(original_url, new_relative_path_str)
                return new_link
            else:
                return full_link

        new_content = MD_LINK_REGEX.sub(replace_link, content)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

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
