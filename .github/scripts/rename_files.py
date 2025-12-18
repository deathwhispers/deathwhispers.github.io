import argparse
import logging
import re
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Tuple

import yaml

# ==========================================
#              用户配置区域 (可直接修改)
# ==========================================

# 1. 默认扫描的目录路径 (可以是相对路径或绝对路径)
DEFAULT_DIR = Path("../../_posts/")

# 2. 是否真正执行重命名？
DEFAULT_APPLY = False  # 默认安全模式 (False = 仅预览 / True = 实际修改文件)

# 3. 是否递归扫描子目录？
DEFAULT_RECURSIVE = True

# 4. 目标文件后缀
DEFAULT_EXT = ".md"

# ==========================================
#                 脚本逻辑开始
# ==========================================

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


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


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Markdown 文件重命名脚本 (date-slug)")
    parser.add_argument("--dir", type=str, default=DEFAULT_DIR, help="指定扫描目录")
    parser.add_argument("--apply", action='store_true', dest='apply', default=DEFAULT_APPLY, help="执行重命名操作")
    parser.add_argument("--preview", action='store_false', dest='apply', help="仅预览（不修改文件）")
    parser.add_argument("--recursive", action='store_true', dest='recursive', default=DEFAULT_RECURSIVE,
                        help="递归扫描子目录")
    parser.add_argument("--ext", type=str, default=DEFAULT_EXT, help="文件后缀过滤")
    return parser.parse_args()


def main():
    args = parse_args()
    root_dir = Path(args.dir)

    if not root_dir.exists():
        logger.error(f"目录不存在: {root_dir}")
        return

    mode_str = "【执行模式】" if args.apply else "【预览模式 - 不会修改文件】"
    logger.info(f"{mode_str} 正在扫描: {root_dir}")

    pattern = f"**/*{args.ext}" if args.recursive else f"*{args.ext}"
    files = list(root_dir.glob(pattern))

    stats = {'success': 0, 'skip': 0, 'error': 0}

    for file_path in files:
        try:
            metadata, _ = get_frontmatter(file_path)

            # 检查 Date 和 Slug/Title
            if 'date' not in metadata:
                logger.debug(f"跳过 {file_path.name}: 无日期字段")
                stats['skip'] += 1
                continue

            date_str = format_date(metadata['date'])

            # 优先使用 slug，其次使用 title 并进行 slugify
            raw_slug = metadata.get('slug') or metadata.get('title')
            if not raw_slug:
                logger.warning(f"跳过 {file_path.name}: 无 slug 或 title 字段")
                stats['skip'] += 1
                continue

            slug = slugify(str(raw_slug))

            if not date_str or not slug:
                logger.warning(f"跳过 {file_path.name}: 日期或 Slug 无效")
                stats['skip'] += 1
                continue

            # --- 计算新路径 ---
            new_name = f"{date_str}-{slug}{file_path.suffix}"
            new_path = file_path.parent / new_name

            if file_path.name == new_name:
                stats['skip'] += 1
                continue  # 名称已经正确

            if new_path.exists():
                logger.error(f"冲突: {file_path.name} -> {new_name} (目标文件已存在)")
                stats['error'] += 1
                continue

            # --- 执行重命名 ---
            arrow = "->"
            if args.apply:
                file_path.rename(new_path)
                logger.info(f"重命名: {file_path.name} {arrow} {new_name}")
                stats['success'] += 1
            else:
                logger.info(f"[预览] {file_path.name} {arrow} {new_name}")
                stats['success'] += 1

        except Exception as e:
            logger.error(f"处理 {file_path.name} 时出错: {e}")
            stats['error'] += 1

    logger.info("-" * 30)
    logger.info(f"处理结束: 成功/预览 {stats['success']} 个, 跳过 {stats['skip']} 个, 错误 {stats['error']} 个")


if __name__ == "__main__":
    main()
