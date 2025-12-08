import os
import re
from pathlib import Path
from typing import Set, Iterator
from urllib.parse import unquote

# --- 配置参数 ---

# ⚠ 关键安全开关：设置为 True 时，脚本只打印操作，不实际删除文件。
DRY_RUN = False

# 扫描的起始目录
SCAN_START_DIR = Path("_posts/")

# 资产存放目录前缀
IMAGE_ASSET_PREFIX = Path("assets/images")

# 标准 Markdown 链接的正则表达式
MD_LINK_REGEX = re.compile(r'(!?\[.*?\]\s*\((.*?)\))')
# Wiki Link 链接的正则表达式（仅用于提取路径，不替换）
WIKI_LINK_REGEX = re.compile(r'(!?\[\[(.*?)\]\])')

# 支持的文件类型（用于收集磁盘上的文件）
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}


# --- 辅助函数 ---

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


# --- 核心清理逻辑 ---

def extract_referenced_assets(project_root: Path) -> Set[Path]:
    """
    扫描所有 Markdown 文件，提取所有引用的 assets/images/... 路径。
    返回一个包含项目根目录绝对路径的集合。
    """
    print("1. 正在扫描 Markdown 文件并提取引用的附件路径...")
    referenced_paths: Set[Path] = set()
    md_files = list(find_markdown_files(project_root, SCAN_START_DIR))

    for md_file_relative in md_files:
        full_md_file_path = project_root / md_file_relative
        try:
            with open(full_md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  警告: 读取文件失败 {md_file_relative}: {e}")
            continue

        # 匹配标准 Markdown 链接
        for match in MD_LINK_REGEX.finditer(content):
            original_url = unquote(match.group(2))

            # 仅处理指向 assets/images/ 的链接 (标准化后的路径)
            if original_url.lstrip('/').startswith(str(IMAGE_ASSET_PREFIX)) and Path(
                    original_url).suffix.lower() in IMAGE_EXTENSIONS:
                referenced_paths.add((project_root / original_url.lstrip('/')).resolve())

        # 匹配 Wiki Links（标准化脚本会将它们转换为标准 MD 链接，这里是额外检查）
        for match in WIKI_LINK_REGEX.finditer(content):
            # 仅提取内容，不处理别名
            raw_content = match.group(2).split('|')[0].strip()
            path_part = unquote(raw_content)

            if path_part.lstrip('/').startswith(str(IMAGE_ASSET_PREFIX)) and Path(
                    path_part).suffix.lower() in IMAGE_EXTENSIONS:
                referenced_paths.add((project_root / path_part.lstrip('/')).resolve())

    print(f"  [完成] 发现 {len(referenced_paths)} 个被引用的附件。")
    return referenced_paths


def collect_all_image_paths(project_root: Path) -> Set[Path]:
    """
    扫描 IMAGE_ASSET_PREFIX 目录，收集所有实际存在的图片文件路径。
    返回一个包含项目根目录绝对路径的集合。
    """
    print("2. 正在扫描磁盘并收集所有实际存在的图片文件...")
    all_disk_paths: Set[Path] = set()
    asset_dir = project_root / IMAGE_ASSET_PREFIX

    if not asset_dir.is_dir():
        print("  警告: 资产目录不存在。跳过扫描。")
        return all_disk_paths

    for path in asset_dir.rglob('*'):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            all_disk_paths.add(path.resolve())

    print(f"  [完成] 磁盘上发现 {len(all_disk_paths)} 个图片文件。")
    return all_disk_paths


def clean_orphaned_assets(project_root: Path):
    """
    识别并删除孤立文件。
    """
    referenced = extract_referenced_assets(project_root)
    all_disk = collect_all_image_paths(project_root)

    # 孤立文件 = 实际存在的文件 - 被引用的文件
    orphans = all_disk - referenced

    if not orphans:
        print("\n3. 未发现孤立图片文件。无需删除。")
        return

    print(f"\n3. 发现 {len(orphans)} 个孤立图片文件。准备清理...")

    for orphan_path in orphans:
        relative_path = orphan_path.relative_to(project_root)

        if DRY_RUN:
            print(f"  [空运行] 待删除孤立文件: {relative_path}")
        else:
            try:
                os.remove(orphan_path)
                print(f"  [删除成功] 孤立文件已清理: {relative_path}")
            except Exception as e:
                print(f"  [删除失败] 无法清理 {relative_path}: {e}")


def clean_empty_dirs(project_root: Path):
    """
    递归删除 IMAGE_ASSET_PREFIX 目录下的空文件夹。
    """
    print("\n4. 正在清理留下的空目录...")
    asset_dir = project_root / IMAGE_ASSET_PREFIX
    if not asset_dir.is_dir():
        return

    removed_count = 0

    # 遍历目录，从深层向浅层删除空目录
    for dirpath, dirnames, filenames in os.walk(asset_dir, topdown=False):
        current_dir = Path(dirpath)

        # 跳过根目录本身
        if current_dir == asset_dir:
            continue

        # 如果目录为空（os.walk 从 topdown=False 确保了所有文件已被处理）
        if not os.listdir(current_dir):
            relative_path = current_dir.relative_to(project_root)

            if DRY_RUN:
                print(f"  [空运行] 待删除空目录: {relative_path}")
            else:
                try:
                    os.rmdir(current_dir)
                    print(f"  [删除成功] 空目录已清理: {relative_path}")
                    removed_count += 1
                except OSError as e:
                    # 只有在目录下仍有文件或权限问题时才会发生
                    print(f"  [删除失败] 目录非空或权限不足 {relative_path}: {e}")

    print(f"  [完成] 清理了 {removed_count} 个空目录。")


if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = find_project_root(SCRIPT_DIR)

    print("--- 资产清理脚本 ---")
    if DRY_RUN:
        print("!!! 当前处于 [空运行模式 (DRY_RUN=True)]。文件和目录将不会被实际删除 !!!")
        print("    要执行删除操作，请修改脚本中的 DRY_RUN = False。")
    else:
        print("!!! 当前处于 [实际删除模式 (DRY_RUN=False)]。请谨慎操作 !!!")

    # 步骤 1 & 2 & 3: 清理孤立文件
    clean_orphaned_assets(PROJECT_ROOT)

    # 步骤 4: 清理空目录
    clean_empty_dirs(PROJECT_ROOT)

    print("\n--- 脚本执行完毕 ---")
