#!/usr/bin/env python3
"""
批量格式化 markdown 文件中的 Java 代码块
格式化规则：
1. 挤在一行的代码分开
2. 添加4空格缩进
3. 花括号后换行
4. 分号后换行
"""

import re
import os
import glob

def format_java_code(code):
    """格式化 Java 代码块内容"""
    lines = code.split('\n')
    formatted_lines = []

    for line in lines:
        # 跳过空行和注释行
        stripped = line.strip()
        if stripped == '' or stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*') or stripped.startswith('*/'):
            formatted_lines.append(line)
            continue

        # 处理挤在一行的代码
        # 先处理花括号后换行和分号后换行
        new_parts = []

        # 处理行内多个语句的情况
        # 例如: "this.value = B return true;" -> 分成 "this.value = B;" 和 "return true;"

        # 先按花括号分开
        parts = split_by_braces_and_semicolons(stripped)

        for part in parts:
            part = part.strip()
            if part:
                # 添加4空格缩进
                new_parts.append('    ' + part)

        if new_parts:
            formatted_lines.extend(new_parts)
        else:
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)


def split_by_braces_and_semicolons(line):
    """按花括号和分号分割一行代码"""
    parts = []
    current = ''
    i = 0

    while i < len(line):
        char = line[i]

        if char == '{':
            # 花括号前的内容加上花括号，然后换行
            if current.strip():
                parts.append(current.strip() + ' {')
            else:
                parts.append('{')
            current = ''
        elif char == '}':
            # 先处理之前的内容
            if current.strip():
                parts.append(current.strip())
            parts.append('}')
            current = ''
        elif char == ';':
            # 分号结束当前语句
            current += char
            if current.strip():
                parts.append(current.strip())
            current = ''
        else:
            current += char

        i += 1

    # 处理剩余内容
    if current.strip():
        parts.append(current.strip())

    return parts


def process_markdown_file(filepath):
    """处理单个 markdown 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找所有 Java 代码块
    # 匹配 ```java ... ``` 格式
    pattern = r'```java\n(.*?)```'

    matches = list(re.finditer(pattern, content, re.DOTALL))
    code_block_count = len(matches)

    if code_block_count == 0:
        return 0

    # 替换每个代码块
    new_content = content
    for match in matches:
        old_code = match.group(1)
        formatted_code = format_java_code(old_code)
        # 替换时保持 ```java 和 ``` 标记
        replacement = '```java\n' + formatted_code + '\n```'
        new_content = new_content.replace(match.group(0), replacement)

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