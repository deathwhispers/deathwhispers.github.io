import os
import requests
from notion_client import Client
from notion2md.exporter.block import NotionToMarkdown

# 🔑 从环境变量读取
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# 初始化客户端
notion = Client(auth=NOTION_API_KEY)
n2m = NotionToMarkdown(notion)

# 拉取数据库中的文章
def fetch_articles():
    results = notion.databases.query(
        **{
            "database_id": NOTION_DATABASE_ID,
            "filter": {
                "property": "Status",
                "select": {"equals": "Published"}
            }
        }
    )
    return results["results"]

# 转换为 Markdown 文件并写入本地
def save_as_markdown(page):
    page_id = page["id"]
    title = page["properties"]["Title"]["title"][0]["text"]["content"]
    date = page["properties"]["Date"]["date"]["start"]

    # 转换 Notion 块 → Markdown
    md_blocks = n2m.page_to_markdown(page_id)
    md_string = n2m.to_markdown(md_blocks)

    # Jekyll 需要 YAML front matter
    front_matter = f"""---
title: "{title}"
date: {date}
layout: post
---
"""

    filename = f"_posts/{date}-{title.replace(' ', '-')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter + "\n" + md_string)

    print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    articles = fetch_articles()
    for page in articles:
        save_as_markdown(page)
