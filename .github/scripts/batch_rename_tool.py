import hashlib
import os
import re
import shutil
from pathlib import Path
from typing import List, Set, Literal, Dict, Iterator
from urllib.parse import unquote

# --- 配置区 ---

# 1. 要扫描的目录列表 (相对于项目根目录)。
#    这些是包含附件的目录，附件将被重命名。
SCAN_DIRS: List[Path] = [
    Path("assets/images/"),
    # Path("assets/files"),
    # Path("其他需要扫描的目录")
]

# 1B. 要扫描的笔记目录列表 (相对于项目根目录)。
#     这些是包含 Markdown 笔记的目录，附件链接将在这些文件中更新。
SCAN_NOTE_DIRS: List[Path] = [
    Path("_posts"),
    # Path("docs"),
]

# 2. 文件过滤配置
#    - 如果设置了 INCLUDE_EXTENSIONS，则只处理这些文件类型。
#    - 如果 INCLUDE_EXTENSIONS 为空集，则处理所有文件类型，除了 EXCLUDE_EXTENSIONS 中的。
INCLUDE_EXTENSIONS: Set[str] = {
    # '.png', '.jpg', '.pdf'  # 例如：只处理这三种类型的文件
}

#    - 要排除的文件扩展名（只有在 INCLUDE_EXTENSIONS 为空时生效）
EXCLUDE_EXTENSIONS: Set[str] = {
    '.md', '.gitignore', '.gitattributes', '.py', '.txt', '.json', '.yml'
}

# 3. 重命名策略
#    - 'hash': (推荐) 使用文件内容的 MD5 哈希作为文件名。确保全局唯一且能去重。
#    - 'sequence': 使用递增数字序列 (例如: 0001.png, 0002.jpg)。
RENAME_STRATEGY: Literal['hash', 'sequence'] = 'hash'

# 4. 运行模式
#    - True: 只打印将要执行的操作，不实际移动、重命名或更新文件。
#    - False: 实际执行重命名和链接更新操作。
DRY_RUN: bool = False

# --- 全局状态 ---
# 记录已处理文件的哈希值，用于避免对相同内容的文件的重复重命名
HASH_TO_NEW_NAME: Dict[str, Path] = {}

# 记录旧文件绝对路径到新文件相对项目根目录路径的映射，用于更新 Markdown 链接
OLD_PATH_TO_NEW_PATH: Dict[Path, Path] = {}

# --- 链接处理正则 ---
# Wiki Link 链接的正则表达式：匹配 [[...]] 或 ![[...]]
WIKI_LINK_REGEX = re.compile(r'(!?\[\[(.*?)\]\])')

# 标准 Markdown 链接的正则表达式
MD_LINK_REGEX = re.compile(r'(!?\[.*?\]\s*\((.*?)\))')


# --- 辅助函数 ---

def find_project_root(start_dir: Path, marker_file: str = ".git") -> Path:
    """尝试查找项目根目录（通常是包含 .git 文件的目录）"""
    current = start_dir
    while current.parent != current:
        if (current / marker_file).exists():
            return current
        current = current.parent
    return start_dir


def get_file_hash_name(file_path: Path) -> str:
    """计算文件内容的 MD5 哈希值。"""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"  [错误] 无法读取文件 {file_path} 进行哈希计算: {e}")
        return ""


def filter_file(file_path: Path) -> bool:
    """根据配置检查文件是否应该被处理。"""
    ext = file_path.suffix.lower()

    if INCLUDE_EXTENSIONS:
        return ext in INCLUDE_EXTENSIONS

    return ext and ext not in EXCLUDE_EXTENSIONS


def find_note_files(project_root: Path) -> Iterator[Path]:
    """迭代器，返回所有 Markdown 笔记文件的相对路径。"""
    for scan_dir in SCAN_NOTE_DIRS:
        full_scan_path = project_root / scan_dir
        if not full_scan_path.is_dir(): continue
        for path in full_scan_path.rglob('*.md'):
            yield path.relative_to(project_root)


# --- 重命名策略实现 ---

def rename_with_hash(file_path: Path, project_root: Path) -> Path | None:
    """根据文件内容哈希重命名文件，并记录路径映射。"""
    file_hash = get_file_hash_name(file_path)
    if not file_hash:
        return None

    new_filename = f"{file_hash}{file_path.suffix.lower()}"

    # 保持文件在原目录，只改变文件名
    new_full_path = file_path.parent / new_filename
    new_full_path_relative = new_full_path.relative_to(project_root)

    # 检查是否是重复文件（内容哈希相同）
    if file_hash in HASH_TO_NEW_NAME:
        existing_path_relative = HASH_TO_NEW_NAME[file_hash]
        existing_path = project_root / existing_path_relative
        if existing_path.exists():
            print(f"  [跳过] 文件内容重复，已存在于: {existing_path_relative}")

            # 记录映射：旧文件指向已存在的哈希文件
            OLD_PATH_TO_NEW_PATH[file_path.resolve()] = existing_path_relative

            # 如果是重复文件，且不在目标位置，则删除原文件
            if file_path.resolve() != existing_path.resolve():
                print(f"  [清理] 删除重复文件: {file_path.name}")
                if not DRY_RUN:
                    os.remove(file_path)
            return existing_path_relative

    # 记录新的哈希和路径
    HASH_TO_NEW_NAME[file_hash] = new_full_path_relative
    OLD_PATH_TO_NEW_PATH[file_path.resolve()] = new_full_path_relative

    if file_path.resolve() == new_full_path.resolve():
        print(f"  [匹配] 文件名已是哈希格式: {file_path.name}")
        return new_full_path_relative

    if DRY_RUN:
        print(f"  [哈希重命名] {file_path.name} -> {new_filename}")
        return new_full_path_relative

    try:
        # 重命名文件
        shutil.move(file_path, new_full_path)
        print(f"  [成功] {file_path.name} -> {new_filename}")
        return new_full_path_relative
    except Exception as e:
        print(f"  [失败] 重命名 {file_path.name} 失败: {e}")
        return None


def rename_with_sequence(file_path: Path, project_root: Path, counter: List[int]) -> Path | None:
    """根据序列号重命名文件，并记录路径映射。"""
    counter[0] += 1
    new_filename = f"{counter[0]:04d}{file_path.suffix.lower()}"
    new_full_path = file_path.parent / new_filename
    new_full_path_relative = new_full_path.relative_to(project_root)

    OLD_PATH_TO_NEW_PATH[file_path.resolve()] = new_full_path_relative

    if DRY_RUN:
        print(f"  [序列重命名] {file_path.name} -> {new_filename}")
        return new_full_path_relative

    try:
        shutil.move(file_path, new_full_path)
        print(f"  [成功] {file_path.name} -> {new_filename}")
        return new_full_path_relative
    except Exception as e:
        print(f"  [失败] 重命名 {file_path.name} 失败: {e}")
        return None


# --- 链接更新函数 ---

def get_link_replacement(link_content: str, is_wiki_link: bool, note_path: Path, project_root: Path) -> str | None:
    """
    根据 OLD_PATH_TO_NEW_PATH 字典查找链接的替换目标，并计算相对于笔记的路径。
    """
    # 1. 预处理链接内容
    if is_wiki_link:
        link_content = link_content.split('|')[0]

    link_content = unquote(link_content)

    # 2. 尝试解析为绝对路径
    note_dir = (project_root / note_path).parent

    if link_content.startswith('/'):
        # 绝对路径 (相对于项目根目录)
        full_original_path = (project_root / link_content.lstrip('/')).resolve()
    elif is_wiki_link and link_content.find('/') == -1 and link_content.find('\\') == -1:
        # 纯文件名 Wiki Link (如 [[image.png]])
        # 这种链接在 Markdown 中是模棱两可的，我们依赖 OLD_PATH_TO_NEW_PATH 中的文件名匹配。

        target_filename = Path(link_content).name

        # 遍历映射，查找旧文件名匹配项
        for old_abs_path, new_rel_path in OLD_PATH_TO_NEW_PATH.items():
            if old_abs_path.name == target_filename:
                # 找到匹配项，计算新相对路径并返回
                new_abs_path = project_root / new_rel_path
                try:
                    new_link = os.path.relpath(new_abs_path, note_dir)
                    return Path(new_link).as_posix()  # 转换为 POSIX 风格 /
                except ValueError:
                    # 路径计算错误
                    print(f"  [DEBUG] 链接替换失败 (路径计算错误): Note='{note_path}', Target='{link_content}'")
                    return None
        # 纯文件名 Wiki Link 没有被重命名
        print(f"  [DEBUG] Wiki Link: '{link_content}' (文件名匹配) NOT found in map.")
        return None
    else:
        # 相对路径或复杂 Wiki Link (e.g. [[../images/file.png]])
        full_original_path = (note_dir / link_content).resolve()

    # 3. 查找映射
    if full_original_path in OLD_PATH_TO_NEW_PATH:
        new_rel_path = OLD_PATH_TO_NEW_PATH[full_original_path]

        # 计算新链接相对于当前笔记的路径
        new_abs_path = project_root / new_rel_path

        try:
            new_link = os.path.relpath(new_abs_path, note_dir)
            return Path(new_link).as_posix()
        except ValueError:
            print(f"  [DEBUG] 链接替换失败 (路径计算错误): Note='{note_path}', Target='{link_content}'")
            return None

    # 如果找不到，打印调试信息
    if is_wiki_link:
        print(f"  [DEBUG] Wiki Link: '{link_content}' resolved to '{full_original_path}' NOT found in map.")
    else:
        print(f"  [DEBUG] MD Link: '{link_content}' resolved to '{full_original_path}' NOT found in map.")

    return None  # 未找到需要替换的链接


def replace_link_in_content(match: re.Match, note_path: Path, project_root: Path) -> str:
    """替换找到的链接：Wiki Link 转换为标准 MD 链接，标准 MD 链接替换路径。"""
    full_match = match.group(0)

    # 确定链接类型和捕获组
    if full_match.startswith('!['):  # 可能是 ![[...]] 或 ![...]
        link_content_group = 2
        is_wiki_link = full_match.startswith('![[')
    elif full_match.startswith('['):  # 可能是 [[...]] 或 [...]
        link_content_group = 2
        is_wiki_link = full_match.startswith('[[')
    else:
        # 不支持的格式
        return full_match

    raw_content = match.group(link_content_group)

    if is_wiki_link:
        # 处理 Wiki Link
        parts = raw_content.split('|', 1)
        link_target = parts[0]
        alt_text = parts[1] if len(parts) > 1 else None

        new_link_target = get_link_replacement(link_target, True, note_path, project_root)

        if new_link_target:
            print(f"  [更新Wiki] 找到替换: {link_target} -> {new_link_target}")
            # Wiki Link 转换为标准 Markdown Link
            prefix = '!' if full_match.startswith('!') else ''
            alt = alt_text or Path(new_link_target).stem
            # 确保 alt text 不为空，并进行简单清理
            alt = alt.replace(')', '').replace('[', '')
            return f'{prefix}[{alt}]({new_link_target})'
        return full_match

    else:
        # 处理 Standard Markdown Link
        link_target = raw_content

        # 检查是否是笔记链接，跳过
        if Path(link_target).suffix.lower() in ('.md', '.markdown'):
            return full_match

        new_link_target = get_link_replacement(link_target, False, note_path, project_root)

        if new_link_target:
            print(f"  [更新MD] 找到替换: {link_target} -> {new_link_target}")
            return full_match.replace(link_target, new_link_target)
        return full_match


def update_links_in_markdown(project_root: Path):
    """
    遍历Markdown文件，更新重命名后的附件链接。
    """
    if not OLD_PATH_TO_NEW_PATH:
        print("\n没有文件被重命名，跳过链接更新。")
        return

    print("\n--- 正在更新 Markdown 笔记中的附件链接 ---")

    for note_path_relative in find_note_files(project_root):
        note_path_full = project_root / note_path_relative

        print(f"  [扫描] {note_path_relative}")

        try:
            with open(note_path_full, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  [错误] 无法读取文件 {note_path_full}: {e}")
            continue

        original_content = content

        # 1. 更新 Wiki Links (并转换为标准 MD 链接)
        # 先处理 Wiki Link 正则，因为它捕获的链接内容和 MD Link 不同
        partial_wiki = lambda m: replace_link_in_content(m, note_path_relative, project_root)
        content = WIKI_LINK_REGEX.sub(partial_wiki, content)

        # 2. 更新 Standard MD Links
        partial_md = lambda m: replace_link_in_content(m, note_path_relative, project_root)
        content = MD_LINK_REGEX.sub(partial_md, content)

        if content != original_content:
            if DRY_RUN:
                print(f"  [更新] {note_path_relative} 需要更新 (测试运行跳过写入)")
            else:
                try:
                    with open(note_path_full, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  [写入] {note_path_relative} 链接已更新。")
                except Exception as e:
                    print(f"  [错误] 写入文件失败: {note_path_full}: {e}")
        else:
            print(f"  [跳过] {note_path_relative} 无需更新。")


# --- 主程序执行流程 ---

def execute_renaming_and_link_update(project_root: Path):
    """
    执行整个流程：重命名文件，然后更新Markdown链接。
    """
    print("--- 批量重命名和链接更新工具启动 ---")

    # 1. 执行重命名操作 (会填充 OLD_PATH_TO_NEW_PATH)
    print(f"当前模式: {'【测试运行】不实际修改文件' if DRY_RUN else '【实际执行】将修改文件'}")
    print(f"重命名策略: {RENAME_STRATEGY}")

    # 序列命名需要一个可变的计数器
    sequence_counter = [0]

    for scan_dir in SCAN_DIRS:
        full_scan_path = project_root / scan_dir

        if not full_scan_path.is_dir():
            print(f"\n[警告] 扫描目录不存在: {scan_dir}")
            continue

        print(f"\n--- 正在扫描附件目录: {scan_dir} ---")

        # 递归扫描所有文件
        for file_path in full_scan_path.rglob('*'):
            if file_path.is_file() and filter_file(file_path):

                # 执行重命名操作
                if RENAME_STRATEGY == 'hash':
                    rename_with_hash(file_path, project_root)
                elif RENAME_STRATEGY == 'sequence':
                    rename_with_sequence(file_path, project_root, sequence_counter)
                else:
                    print(f"  [错误] 未知的重命名策略: {RENAME_STRATEGY}")
                    return  # 退出

    print("\n--- 附件批量重命名阶段完成 ---")

    # 2. 更新链接
    update_links_in_markdown(project_root)

    print("\n--- 批量重命名和链接更新完成 ---")
    if DRY_RUN:
        print("【提示】您正在运行测试模式 (DRY_RUN=True)。要实际执行操作，请修改脚本中的 DRY_RUN 为 False。")


if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = find_project_root(SCRIPT_DIR)

    execute_renaming_and_link_update(PROJECT_ROOT)
