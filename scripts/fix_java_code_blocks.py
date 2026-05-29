#!/usr/bin/env python3
"""
修复 Markdown 文件中 Java 代码块的超长行
将花括号内容过长的代码块分行处理
"""
import re
import sys
import os

def fix_java_code_block(content):
    """修复 Java 代码块中的超长行"""
    lines = content.split('\n')
    result = []
    in_java_block = False

    for line in lines:
        if line.strip() == '```java':
            in_java_block = True
            result.append(line)
            continue
        elif line.strip() == '```' and in_java_block:
            in_java_block = False
            result.append(line)
            continue

        if in_java_block and len(line) > 100:
            # 处理超长行
            fixed_lines = fix_long_java_line(line)
            result.extend(fixed_lines)
        else:
            result.append(line)

    return '\n'.join(result)

def fix_long_java_line(line):
    """修复单个超长的 Java 代码行"""
    # 处理注释格式问题: // xxx 或 /** xxx */ 被合并
    if line.strip().startswith('//') and len(line) > 100:
        # 处理 // 注释后被合并的代码
        parts = re.split(r'\s*//\s*', line)
        if len(parts) > 1:
            result = []
            for i, part in enumerate(parts):
                if i == 0:
                    if part.strip():
                        result.append(part)
                else:
                    result.append('// ' + part.strip())
            return result

    # 处理多行注释格式问题: /** xxx */ 被合并
    if '/**' in line and '*/' in line and len(line) > 150:
        # 拆分 Javadoc 注释
        line = line.replace('{@link', '{@link ')
        line = line.replace('}', ' }')
        # 按合理长度拆分
        result = []
        if line.strip().startswith('/**'):
            # 提取注释内容
            match = re.match(r'(\s*/\*\*)(.*)(\*/)', line)
            if match:
                prefix = match.group(1)
                content = match.group(2)
                suffix = match.group(3)
                # 拆分内容
                result.append(prefix)
                # 按 @see, @since 等标签拆分
                tags = re.split(r'(\*?\s*@see|\*?\s*@since|\*?\s*@param|\*?\s*@return)', content)
                for tag in tags:
                    if tag.strip():
                        if tag.strip().startswith('@'):
                            result.append(' * ' + tag.strip())
                        else:
                            result.append(' * ' + tag.strip())
                result.append(' ' + suffix)
                return result

    # 处理包含多个语句的行（以分号分隔）
    if ';' in line and not line.strip().startswith('//') and not line.strip().startswith('*'):
        statements = []
        current = ""
        for char in line:
            current += char
            if char == ';':
                statements.append(current.strip())
                current = ""
        if current.strip():
            statements.append(current.strip())
        if len(statements) > 1:
            return statements

    # 处理包含花括号的超长行
    if '{' in line or '}' in line:
        # 尝试按花括号拆分
        parts = []
        depth = 0
        current = ""
        for char in line:
            current += char
            if char == '{':
                depth += 1
                if depth == 1 and len(current.strip()) > 80:
                    parts.append(current.strip())
                    current = ""
            elif char == '}':
                depth -= 1
                if depth == 0 and current.strip():
                    parts.append(current.strip())
                    current = ""
        if current.strip():
            parts.append(current.strip())
        if len(parts) > 1:
            return parts

    return [line]

def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fixed_content = fix_java_code_block(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"已处理: {filepath}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python fix_java_code_blocks.py <文件路径>")
        sys.exit(1)

    filepath = sys.argv[1]
    if os.path.isfile(filepath):
        process_file(filepath)
    else:
        print(f"文件不存在: {filepath}")
        sys.exit(1)

if __name__ == '__main__':
    main()