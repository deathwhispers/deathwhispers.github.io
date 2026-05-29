#!/usr/bin/env python3
"""
批量格式化 markdown 文件中的 Java 代码块
格式化规则：
1. 挤在一行的代码分开（处理缺少分号的多语句）
2. 添加4空格缩进
3. 花括号后换行
4. 分号后换行
"""

import re
import os
import glob

# 需要在其前面分割的关键字（语句开始关键字）
STATEMENT_START_KEYWORDS = [
    'return', 'throw', 'break', 'continue', 'if', 'else', 'for', 'while',
    'do', 'switch', 'case', 'default', 'try', 'catch', 'finally', 'class',
    'interface', 'enum', 'assert', 'synchronized', 'public', 'private',
    'protected', 'static', 'final', 'abstract', 'volatile', 'transient',
    'native', 'strictfp', 'void', 'int', 'long', 'short', 'byte', 'char',
    'float', 'double', 'boolean'
]


def normalize_indentation(code):
    """统一缩进为4空格"""
    lines = code.split('\n')
    normalized_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped == '':
            normalized_lines.append('')
        else:
            normalized_lines.append('    ' + stripped)

    return '\n'.join(normalized_lines)


def split_multi_statement_line(line):
    """
    处理一行中多个挤在一起的语句
    例如: "this.value = B return true;" -> ["this.value = B;", "return true;"]
    """
    stripped = line.strip()
    if stripped == '':
        return [line]

    # 跳过注释行
    if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*') or stripped.startswith('*/'):
        return [line]

    # 检查是否有缺少分号的多语句情况
    # 模式: 在某个语句开始关键字前分割
    result_parts = []

    # 首先按分号分割
    parts = []
    current = ''
    i = 0
    while i < len(stripped):
        char = stripped[i]
        if char == ';':
            current += char
            parts.append(current.strip())
            current = ''
        elif char == '{':
            if current.strip():
                parts.append(current.strip())
            parts.append('{')
            current = ''
        elif char == '}':
            if current.strip():
                parts.append(current.strip())
            parts.append('}')
            current = ''
        else:
            current += char
        i += 1

    if current.strip():
        parts.append(current.strip())

    # 对每个部分检查是否包含多个挤在一起的语句
    for part in parts:
        part = part.strip()
        if part == '{' or part == '}':
            result_parts.append(part)
            continue

        # 检查是否有缺少分号分隔的多语句
        # 模式: "... return ..." 或 "... throw ..." 等
        sub_parts = []
        current_sub = ''
        words = part.split()

        j = 0
        while j < len(words):
            word = words[j]
            # 检查是否遇到语句开始关键字
            if word in STATEMENT_START_KEYWORDS:
                # 如果当前累积的内容不为空，保存并加分号（如果需要）
                if current_sub.strip():
                    # 检查是否已经有分号
                    if not current_sub.strip().endswith(';'):
                        # 判断是否是完整语句（如赋值语句）
                        # 如果是赋值语句，需要加分号
                        if '=' in current_sub or current_sub.strip().startswith('new') or current_sub.strip().startswith('('):
                            current_sub = current_sub.strip() + ';'
                    sub_parts.append(current_sub.strip())
                    current_sub = ''

            current_sub += ' ' + word if current_sub else word
            j += 1

        # 处理剩余内容
        if current_sub.strip():
            sub_parts.append(current_sub.strip())

        result_parts.extend(sub_parts)

    return result_parts


def format_java_code(code):
    """格式化 Java 代码块"""
    # 首先统一缩进
    code = normalize_indentation(code)

    lines = code.split('\n')
    formatted_lines = []

    for line in lines:
        # 处理挤在一行的多个语句
        split_parts = split_multi_statement_line(line)

        for part in split_parts:
            part = part.strip()
            if part:
                # 花括号和普通语句的处理
                if part == '{':
                    formatted_lines.append('    ' + part)
                elif part == '}':
                    formatted_lines.append('    ' + part)
                else:
                    formatted_lines.append('    ' + part)

    return '\n'.join(formatted_lines)


def process_markdown_file(filepath):
    """处理单个 markdown 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找所有 Java 代码块
    pattern = r'```java\s*\n(.*?)\n```'

    matches = list(re.finditer(pattern, content, re.DOTALL))
    code_block_count = len(matches)

    if code_block_count == 0:
        return 0

    # 替换每个代码块
    def replace_code_block(match):
        old_code = match.group(1)
        formatted_code = format_java_code(old_code)
        return '```java\n' + formatted_code + '\n```'

    new_content = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)

    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return code_block_count


def main():
    directory = '/Users/whisper/IdeaProjects/github/deathwhispers.github.io/_posts/learning/java/concurrence'
    md_files = glob.glob(os.path.join(directory, '*.md'))

    total_files = 0
    total_code_blocks = 0

    for filepath in md_files:
        count = process_markdown_file(filepath)
        if count > 0:
            total_files += 1
            total_code_blocks += count
            print(f"处理文件: {os.path.basename(filepath)}, 代码块数: {count}")

    print(f"\n总结:")
    print(f"处理文件数: {total_files}")
    print(f"处理代码块数: {total_code_blocks}")


if __name__ == '__main__':
    main()