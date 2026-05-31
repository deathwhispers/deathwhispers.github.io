#!/usr/bin/env python3
import re
import sys

filepath = sys.argv[1] if len(sys.argv) > 1 else '_posts/learning/java/concurrence/2022-04-04-CountDownLatch原理.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace curly quotes with straight quotes
content = content.replace('\u201c', '"').replace('\u201d', '"')
content = content.replace('\u2018', "'").replace('\u2019', "'")

# Remove extra blank lines at end of code blocks (pattern: 2+ blank lines followed by ```)
content = re.sub(r'\n\n\n+(\n```)', r'\n```', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed: {filepath}')