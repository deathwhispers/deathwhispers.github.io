# 自动提交文章到github.py
import os
import requests
import json
from datetime import datetime
from notion2md.exporter import StringExporter

# 获取环境变量
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

# Notion API 端点
NOTION_API_URL = 'https://api.notion.com/v1'

# 查询 Notion 文章
headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

def query_notion_articles():
    url = f'{NOTION_API_URL}/databases/{NOTION_DATABASE_ID}/query'
    data = {
        'filter': {
            'and': [
                {
                    'property': 'IsPublish',
                    'checkbox': {
                        'equals': False
                    }
                },
                {
                    'property': 'NeedUpdate',
                    'checkbox': {
                        'equals': True
                    }
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

# 将 Notion 文章转换为 Markdown 格式

def convert_to_markdown(article_id):
    exporter = StringExporter(token=NOTION_TOKEN)
    markdown_content = exporter.export(article_id)
    return markdown_content

# 提交 Markdown 文件到 GitHub

def commit_to_github(markdown_content, file_name):
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{file_name}'
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'message': 'Auto commit from Notion',
        'content': markdown_content.encode('utf-8').hex()
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        return True
    return False

# 更新 Notion 文章状态为已发布

def update_notion_article_status(article_id):
    url = f'{NOTION_API_URL}/pages/{article_id}'
    data = {
        'properties': {
            'IsPublish': {
                'checkbox': True
            },
            'NeedUpdate': {
                'checkbox': False
            }
        }
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    return False

# 主函数

def main():
    articles = query_notion_articles()
    for article in articles:
        article_id = article.get('id')
        markdown_content = convert_to_markdown(article_id)
        file_name = article.get('properties', {}).get('MDFilename', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '') + '.md'
        if commit_to_github(markdown_content, file_name):
            update_notion_article_status(article_id)

if __name__ == '__main__':
    main()
