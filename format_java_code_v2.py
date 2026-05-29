#!/usr/bin/env python3
"""
批量格式化 markdown 文件中的 Java 代码块
格式化规则：
1. 挤在一行的代码分开（分号后换行）
2. 添加4空格缩进
3. 花括号后换行
4. 分号后换行
"""

import re
import os
import glob


def format_java_line(line):
    """格式化单行 Java 代码，按分号和花括号分开"""
    stripped = line.strip()
    if stripped == '':
        return []

    # 跳过注释行（保持原样）
    if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*') or stripped.startswith('*/'):
        return ['    ' + stripped]

    # 处理行内多个语句的情况
    result_lines = []

    # 按花括号和分号分割
    segments = []
    current = ''
    brace_depth = 0

    i = 0
    while i < len(stripped):
        char = stripped[i]

        if char == '{':
            brace_depth += 1
            current += char
            # 花括号后换行
            segments.append(current.strip())
            current = ''
        elif char == '}':
            brace_depth -= 1
            # 花括号前如果有内容，先处理
            if current.strip():
                segments.append(current.strip())
            segments.append(char)
            current = ''
        elif char == ';':
            current += char
            # 分号后换行
            segments.append(current.strip())
            current = ''
        else:
            current += char

        i += 1

    # 处理剩余内容
    if current.strip():
        segments.append(current.strip())

    # 为每个段添加4空格缩进
    for seg in segments:
        seg = seg.strip()
        if seg:
            # 特殊处理花括号
            if seg == '{' or seg == '}':
                result_lines.append('    ' + seg)
            else:
                result_lines.append('    ' + seg)

    return result_lines


def format_java_code(code):
    """格式化 Java 代码块内容"""
    lines = code.split('\n')
    formatted_lines = []

    for line in lines:
        new_lines = format_java_line(line)
        formatted_lines.extend(new_lines)

    return '\n'.join(formatted_lines)


def process_markdown_file(filepath):
    """处理单个 markdown 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找所有 Java 代码块
    # 匹配 ```java ... ``` 格式
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
    # 目录路径
    directory = '/Users/whisper/IdeaProjects/github/deathwhispers.github.io/_posts/learning/java/concurrence'

    # 获取所有 .md 文件
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