#!/usr/bin/env python3
"""
批量格式化 markdown 文件中的 Java 代码块
格式化规则：
1. 挤在一行的代码分开（识别 Java 关键字分割）
2. 添加4空格缩进
3. 花括号后换行
4. 分号后换行
"""

import re
import os
import glob

# Java 关键字列表（用于识别语句边界）
JAVA_KEYWORDS = [
    'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
    'break', 'continue', 'return', 'throw', 'try', 'catch', 'finally',
    'class', 'interface', 'enum', 'extends', 'implements', 'import',
    'package', 'public', 'private', 'protected', 'static', 'final',
    'abstract', 'synchronized', 'volatile', 'transient', 'native',
    'void', 'int', 'long', 'short', 'byte', 'char', 'float', 'double',
    'boolean', 'true', 'false', 'null', 'new', 'this', 'super',
    'instanceof', 'assert', 'const', 'goto', 'throws', 'strictfp'
]


def split_java_statements(line):
    """将一行中的多个 Java 语句分开"""
    stripped = line.strip()
    if stripped == '':
        return []

    # 跳过纯注释行
    if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*') or stripped.startswith('*/'):
        return [stripped]

    # 处理行内多个语句的情况
    statements = []
    current = ''
    i = 0

    while i < len(stripped):
        char = stripped[i]

        if char == '{':
            # 花括号前如果有内容，保存
            if current.strip():
                statements.append(current.strip())
            statements.append('{')
            current = ''
        elif char == '}':
            # 花括号前如果有内容，保存
            if current.strip():
                statements.append(current.strip())
            statements.append('}')
            current = ''
        elif char == ';':
            current += char
            # 分号结束当前语句
            statements.append(current.strip())
            current = ''
        elif char == ' ' or char == '\t':
            # 检查是否遇到关键字（可能需要分割）
            current += char
            # 检查当前累积的内容是否以某个关键字结束，且下一个词是另一个关键字
            current_stripped = current.strip()
            for kw in JAVA_KEYWORDS:
                # 如果当前内容以关键字结束
                if current_stripped.endswith(kw):
                    # 检查是否有下一个关键字开始
                    remaining = stripped[i+1:].strip()
                    for next_kw in JAVA_KEYWORDS:
                        if remaining.startswith(next_kw):
                            # 在关键字处分割
                            statements.append(current_stripped)
                            current = ''
                            break
                    break
        else:
            current += char

        i += 1

    # 处理剩余内容
    if current.strip():
        statements.append(current.strip())

    return statements


def format_java_code(code):
    """格式化 Java 代码块内容"""
    lines = code.split('\n')
    formatted_lines = []

    for line in lines:
        statements = split_java_statements(line)
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                # 特殊处理花括号缩进
                if stmt == '{':
                    # 花括号通常和前一行一起，单独处理
                    formatted_lines.append('    ' + stmt)
                elif stmt == '}':
                    formatted_lines.append('    ' + stmt)
                else:
                    formatted_lines.append('    ' + stmt)

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