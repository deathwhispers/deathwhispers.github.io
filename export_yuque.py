import os
import time
import re
import argparse
from datetime import datetime

# 尝试导入依赖库，如果没有则提示安装
try:
    import requests
    from markdownify import markdownify as md
except ImportError:
    print("错误: 缺少必要的依赖库。请先运行以下命令安装:")
    print("pip install requests markdownify")
    exit(1)

# 配置区域
# 建议通过环境变量或命令行参数传递 TOKEN，避免硬编码
# export YUQUE_TOKEN="your_token_here"
YUQUE_TOKEN = os.getenv("YUQUE_TOKEN", "") 
BASE_URL = "https://www.yuque.com/api/v2"
USER_AGENT = "YuqueExportScript/1.0"

def get_headers():
    if not YUQUE_TOKEN:
        print("错误: 未找到 YUQUE_TOKEN。")
        print("请在脚本中设置 TOKEN，或使用环境变量: export YUQUE_TOKEN='你的Token'")
        exit(1)
    return {
        "X-Auth-Token": YUQUE_TOKEN,
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }

def sanitize_filename(name):
    """清理文件名，移除非法字符"""
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()

def get_user_info():
    """获取当前用户信息"""
    url = f"{BASE_URL}/user"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code != 200:
        print(f"获取用户信息失败: {resp.text}")
        exit(1)
    return resp.json()['data']

def get_repos(user_id):
    """获取用户的知识库列表"""
    # 获取属于用户的知识库
    url = f"{BASE_URL}/users/{user_id}/repos"
    repos = []
    offset = 0
    
    while True:
        # 语雀 API 分页默认 20，最大 100? 这里不做复杂分页，假设用户知识库不过百
        # 若需完整支持分页需检查 headers['X-Total']
        resp = requests.get(url, headers=get_headers(), params={"offset": offset})
        if resp.status_code != 200:
            print(f"获取知识库列表失败: {resp.text}")
            break
            
        data = resp.json().get('data', [])
        if not data:
            break
            
        repos.extend(data)
        if len(data) < 20: 
            break
        offset += 20
        
    return repos

def get_repo_docs(namespace):
    """获取知识库下的文档列表"""
    url = f"{BASE_URL}/repos/{namespace}/docs"
    docs = []
    offset = 0
    limit = 100 
    
    while True:
        resp = requests.get(url, headers=get_headers(), params={"offset": offset, "limit": limit})
        if resp.status_code != 200:
            print(f"获取文档列表失败 [{namespace}]: {resp.text}")
            break
            
        data = resp.json().get('data', [])
        if not data:
            break
            
        docs.extend(data)
        if len(data) < limit:
            break
        offset += limit
        
    return docs

def get_doc_detail(namespace, slug):
    """获取文档详情（包含 Markdown 内容）"""
    url = f"{BASE_URL}/repos/{namespace}/docs/{slug}"
    # raw=1 试图获取 markdown，但语雀湖畔文档通常返回 HTML
    resp = requests.get(url, headers=get_headers(), params={"raw": 1})
    if resp.status_code != 200:
        print(f"获取文档详情失败 [{slug}]: {resp.text}")
        return None
    return resp.json()['data']

def save_doc(repo_name, doc, output_dir):
    """保存文档为 Markdown"""
    title = sanitize_filename(doc['title'])
    slug = doc['slug']
    
    # 获取详情
    # 列表接口不包含正文，必须调详情接口
    detail = get_doc_detail(doc['book']['namespace'], slug)
    if not detail:
        return

    body = detail.get('body', '')
    
    # 转换 HTML 到 Markdown
    # 语雀新版文档(Lake)返回的是 HTML，旧版可能是 Markdown
    # 不管怎样，先尝试用 markdownify 转换
    # 如果已经是 markdown (format='markdown')，则不需要转换太重
    
    content = ""
    if detail.get('format') == 'markdown':
        content = body
    else:
        # 使用 markdownify 转换 HTML
        # heading_style="atx" 使用 # 标题
        content = md(body, heading_style="atx")

    # 处理 YAML Front Matter
    created_at = detail.get('created_at', '')
    updated_at = detail.get('updated_at', '')
    
    # 尝试格式化日期
    try:
        # 语雀返回 ISO8601: 2020-01-01T00:00:00.000Z
        ctime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        utime = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_str = ctime.strftime("%Y-%m-%d")
        created_str = ctime.strftime("%Y-%m-%d %H:%M:%S")
        updated_str = utime.strftime("%Y-%m-%d %H:%M:%S")
    except:
        date_str = created_at
        created_str = created_at
        updated_str = updated_at

    front_matter = f"""---
title: {title}
slug: {slug}
date: {date_str}
created: {created_str}
updated: {updated_str}
author: {detail.get('user', {}).get('name', 'Unknown')}
---

"""
    
    full_content = front_matter + content
    
    # 创建目录
    repo_path = os.path.join(output_dir, sanitize_filename(repo_name))
    os.makedirs(repo_path, exist_ok=True)
    
    file_path = os.path.join(repo_path, f"{date_str}-{title}.md")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"已保存: {file_path}")
    
    # 避免触发 API 速率限制
    time.sleep(0.5)

def main():
    parser = argparse.ArgumentParser(description="语雀知识库批量导出工具")
    parser.add_argument("--token", help="语雀 Access Token", default="")
    parser.add_argument("--output", help="输出目录", default="yuque_export")
    args = parser.parse_args()
    
    global YUQUE_TOKEN
    if args.token:
        YUQUE_TOKEN = args.token
        
    # 检查 Token
    if not YUQUE_TOKEN:
         # 交互式输入
         YUQUE_TOKEN = input("请输入您的语雀 Token: ").strip()
         
    if not YUQUE_TOKEN:
        print("错误: Token 不能为空")
        return

    print("正在验证 Token...")
    user = get_user_info()
    print(f"登录成功: {user['name']} (ID: {user['id']})")
    
    print("正在获取知识库列表...")
    repos = get_repos(user['id'])
    print(f"找到 {len(repos)} 个知识库")
    
    for i, repo in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] 正在处理知识库: {repo['name']} ...")
        
        # 排除私有且不属于自己的 (如果需要的话，这里暂时全部导出)
        
        docs = get_repo_docs(repo['namespace'])
        print(f"  - 发现 {len(docs)} 篇文档")
        
        for j, doc in enumerate(docs):
            print(f"  -> [{j+1}/{len(docs)}] 下载文档: {doc['title']}")
            save_doc(repo['name'], doc, args.output)
            
    print("\n✅ 所有导出完成！")
    print(f"文件保存在: {os.path.abspath(args.output)}")

if __name__ == "__main__":
    main()
