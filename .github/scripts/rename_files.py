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

# 1. 默认扫描的目录路径
DEFAULT_DIR = Path("../../_posts/")

# 2. 是否真正执行重命名？
DEFAULT_APPLY = True  # False = 仅预览；True = 实际重命名

# 3. 是否递归扫描子目录？
DEFAULT_RECURSIVE = True

# 4. 目标文件后缀
DEFAULT_EXT = ".md"

# ==========================================
#                 脚本逻辑开始
# ==========================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


def slugify(text: str) -> str:
    """将标题转换为 URL/文件名友好的 slug"""
    text = str(text).strip()
    # 保留字母、数字、中文、空格、连字符，其余替换为空
    text = re.sub(r'[^\w\s\-]', '', text)
    # 将连续空白或连字符转为单个 '-'
    # text = re.sub(r'[\s\-]+', '-', text)
    return text.strip('-')


def get_frontmatter(file_path: Path) -> Tuple[Dict[str, Any], str | None]:
    """安全读取 YAML frontmatter"""
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
            data = yaml.safe_load("".join(yaml_lines))
            return data or {}, None
    except Exception as e:
        return {}, str(e)


def format_date(date_obj) -> str | None:
    """标准化日期为 YYYY-MM-DD"""
    if not date_obj:
        return None
    try:
        if isinstance(date_obj, (datetime, date)):
            return date_obj.strftime('%Y-%m-%d')
        # 尝试解析字符串日期
        str_date = str(date_obj).split('T')[0].split(' ')[0]
        # 验证是否为合法日期格式
        datetime.strptime(str_date, '%Y-%m-%d')
        return str_date
    except:
        return None


def parse_args():
    parser = argparse.ArgumentParser(description="Markdown 文件重命名脚本 (格式: date-title.md)")
    parser.add_argument("--dir", type=str, default=DEFAULT_DIR, help="指定扫描目录")
    parser.add_argument("--apply", action='store_true', dest='apply', default=DEFAULT_APPLY,
                        help="执行重命名操作（默认仅预览）")
    parser.add_argument("--preview", action='store_false', dest='apply', help="仅预览（不修改文件）")
    parser.add_argument("--recursive", action='store_true', dest='recursive', default=DEFAULT_RECURSIVE,
                        help="递归扫描子目录")
    parser.add_argument("--ext", type=str, default=DEFAULT_EXT, help="文件后缀过滤")
    return parser.parse_args()


def main():
    args = parse_args()
    root_dir = Path(args.dir).resolve()

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
            metadata, error = get_frontmatter(file_path)

            if error:
                logger.debug(f"跳过 {file_path.name}: {error}")
                stats['skip'] += 1
                continue

            # 必须有 date 和 title
            if 'date' not in metadata:
                logger.debug(f"跳过 {file_path.name}: 缺少 'date' 字段")
                stats['skip'] += 1
                continue

            if 'title' not in metadata:
                logger.warning(f"跳过 {file_path.name}: 缺少 'title' 字段")
                stats['skip'] += 1
                continue

            date_str = format_date(metadata['date'])
            title_slug = slugify(metadata['title'])

            if not date_str:
                logger.warning(f"跳过 {file_path.name}: 无效的日期格式")
                stats['skip'] += 1
                continue

            if not title_slug:
                logger.warning(f"跳过 {file_path.name}: 标题无法生成有效 slug")
                stats['skip'] += 1
                continue

            new_name = f"{date_str}-{title_slug}{file_path.suffix}"
            new_path = file_path.parent / new_name

            # 如果文件名已符合要求，跳过
            if file_path.name == new_name:
                stats['skip'] += 1
                continue

            # 检查目标文件是否已存在
            if new_path.exists():
                # 核心判断：如果 new_path 存在，但它指向的不是当前处理的 file_path，才是真正的冲突
                if not file_path.samefile(new_path):
                    logger.error(f"冲突: {file_path.name} -> {new_name} (被其他文件占用)")
                    stats['error'] += 1
                    continue
                else:
                    # 如果 samefile 为 True，说明只是大小写变了，在某些系统上直接 rename 会失败
                    # 此时可以继续往下走，或者根据系统环境做两步重命名
                    logger.warning(f"警告: {file_path.name} -> {new_name} (只是大小写变化，已跳过)")
                    pass

            # 执行或预览
            if args.apply:
                file_path.rename(new_path)
                logger.info(f"重命名: {file_path.name} -> {new_name}")
                stats['success'] += 1
            else:
                logger.info(f"[预览] {file_path.name} -> {new_name}")
                stats['success'] += 1

        except Exception as e:
            logger.error(f"处理 {file_path.name} 时出错: {e}")
            stats['error'] += 1

    logger.info("-" * 30)
    logger.info(f"处理结束: 成功/预览 {stats['success']} 个, 跳过 {stats['skip']} 个, 错误 {stats['error']} 个")


if __name__ == "__main__":
    main()