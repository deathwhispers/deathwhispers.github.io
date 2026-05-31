#!/usr/bin/env python3
"""
修复 Markdown 文件中 Java 代码块格式的脚本
"""
import os
import re
import sys

def fix_java_code_block(content):
    """修复单个Java代码块的格式"""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 检测代码块开始
        if line.strip().startswith('```java'):
            code_lines = [line]
            i += 1

            # 收集代码块内容
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1

            # 添加结束的 ```
            if i < len(lines):
                code_lines.append(lines[i])
                i += 1

            # 修复代码块内的格式
            fixed_code = fix_code_content(code_lines)
            result.extend(fixed_code)
        else:
            result.append(line)
            i += 1

    return '\n'.join(result)

def fix_code_content(code_lines):
    """修复代码块内容的格式"""
    if len(code_lines) <= 2:
        return code_lines

    # 获取代码内容（去掉首尾的 ```java 和 ```）
    start_marker = code_lines[0]
    end_marker = code_lines[-1]
    content_lines = code_lines[1:-1]

    # 移除末尾的空行
    while content_lines and content_lines[-1].strip() == '':
        content_lines.pop()

    if not content_lines:
        return [start_marker, end_marker]

    # 修复代码内容
    fixed_lines = []
    i = 0
    while i < len(content_lines):
        line = content_lines[i]

        # 修复错误的引号字符
        line = line.replace('"', '"').replace('"', '"')
        line = line.replace(''', "'").replace(''', "'")

        # 检查是否是 if/else/for/while/try/catch 等语句后的花括号问题
        # 例如: } else { 需要保持
        # 例如: if (xxx) { 需要检查下一行

        fixed_lines.append(line)
        i += 1

    # 确保代码块结束标记前只有一个空行
    result = [start_marker] + fixed_lines + [end_marker]
    return result

def process_file(filepath):
    """处理单个文件"""
    print(f"处理文件: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否包含 java 代码块
        if '```java' not in content:
            print(f"  跳过: 没有 Java 代码块")
            return False

        fixed_content = fix_java_code_block(content)

        if content != fixed_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"  已修复")
            return True
        else:
            print(f"  无需修改")
            return False
    except Exception as e:
        print(f"  错误: {e}")
        return False

def main():
    # 要处理的目录
    base_dir = '_posts/learning/java'

    if not os.path.exists(base_dir):
        print(f"目录不存在: {base_dir}")
        sys.exit(1)

    modified_count = 0

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    modified_count += 1

    print(f"\n总计修改 {modified_count} 个文件")

if __name__ == '__main__':
    main()
