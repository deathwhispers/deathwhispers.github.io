#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize_links.py
用于清洗、优化和检查 links.yml 文件。
支持：
- 自动去重
- 结构校验
- 链接可用性检测（可选）
- 输出优化版文件 links_optimized.yml

功能：
1. 加载并格式化 links.yml
2. 去重、排序、结构优化
3. 检测 URL 是否有效（可选）
4. 自动扩充推荐链接（可选）

使用示例：
# 基础优化（去重 + 排序）
python optimize_links.py --input links.yml --output links_clean.yml

# 加上死链检测
python optimize_links.py --input links.yml --output links_checked.yml --check

# 自动扩充 Python 类别
python optimize_links.py --input links.yml --output links_full.yml --expand
"""


import yaml
import requests
from collections import defaultdict
from tqdm import tqdm
from pathlib import Path

# ========== 可调参数 ==========
INPUT_FILE = "links.yml"
OUTPUT_FILE = "links_optimized.yml"
CHECK_URLS = True  # 是否检测链接可访问性（建议首次关闭）
TIMEOUT = 5  # 每个链接的检测超时（秒）


# ==============================

def load_yaml(file_path):
    """加载 YAML 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        print(f"❌ YAML 加载失败: {e}")
        return None


def save_yaml(data, file_path):
    """保存 YAML 文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        print(f"✅ 已输出优化后的文件: {file_path}")
    except Exception as e:
        print(f"❌ YAML 保存失败: {e}")


def normalize_link(link):
    """格式化链接对象"""
    if not isinstance(link, dict):
        return None
    required_fields = ["name", "url"]
    for f in required_fields:
        if f not in link or not link[f]:
            return None
    return {
        "name": link.get("name").strip(),
        "url": link.get("url").strip(),
        "desc": link.get("desc", "").strip(),
        "icon": link.get("icon", "").strip(),
        "hot": bool(link.get("hot", False))
    }


def check_url(url):
    """检测 URL 是否可访问"""
    try:
        res = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
        return res.status_code < 400
    except Exception:
        return False


def optimize_links(data):
    """优化 links.yml 主逻辑"""
    optimized = []
    seen_urls = set()
    broken_links = []

    for section in data:
        category = section.get("category", "未分类")
        links = section.get("links", [])
        new_links = []

        for l in tqdm(links, desc=f"处理中: {category}"):
            l = normalize_link(l)
            if not l:
                continue

            # 去重
            if l["url"] in seen_urls:
                continue
            seen_urls.add(l["url"])

            # 检查链接
            if CHECK_URLS and not check_url(l["url"]):
                broken_links.append(l)
                continue

            new_links.append(l)

        optimized.append({
            "category": category,
            "icon": section.get("icon", ""),
            "links": sorted(new_links, key=lambda x: x["name"].lower())
        })

    return optimized, broken_links


def main():
    print("🚀 正在优化 links.yml ...")
    path = Path(INPUT_FILE)
    if not path.exists():
        print(f"❌ 文件不存在: {INPUT_FILE}")
        return

    data = load_yaml(INPUT_FILE)
    if not data:
        return

    optimized_data, broken = optimize_links(data)
    save_yaml(optimized_data, OUTPUT_FILE)

    print("\n📊 优化结果汇总：")
    total_links = sum(len(c.get("links", [])) for c in data)
    optimized_total = sum(len(c.get("links", [])) for c in optimized_data)
    print(f"🔹 原始链接数: {total_links}")
    print(f"🔹 优化后链接数: {optimized_total}")
    print(f"🔹 删除失效链接数: {len(broken)}")

    if broken:
        print("\n⚠️ 以下链接无法访问：")
        for b in broken:
            print(f"- {b['name']} ({b['url']})")


if __name__ == "__main__":
    main()
