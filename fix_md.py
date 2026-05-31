#!/usr/bin/env python3
import re
import sys

filepath = sys.argv[1]

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace curly quotes with straight quotes
content = content.replace('\u201c', '"').replace('\u201d', '"')
content = content.replace('\u2018', "'").replace('\u2019', "'")

# Remove extra blank lines at end of code blocks (2+ blank lines before ```)
content = re.sub(r'\n\n\n+(\n```)', r'\n```', content)

# Fix broken for loops: for (int i = 0;\n    i < ...;\n    i++) -> for (int i = 0; i < ...; i++)
content = re.sub(
    r'for \(int i = 0;\s*\n\s*i < ([^;]+);\s*\n\s*i\+\+\)',
    r'for (int i = 0; i < \1; i++)',
    content
)

# Fix other common broken loop patterns
content = re.sub(
    r'for \(int i = 0;\s*\n\s*i < ([^;]+);\s*\n\s*i \+= ([^)]+)\)',
    r'for (int i = 0; i < \1; i += \2)',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed: {filepath}')