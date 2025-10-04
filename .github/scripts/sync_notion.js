import fs from "fs";
import path from "path";
import fetch from "node-fetch";
import { Client } from "@notionhq/client";
import { NotionToMarkdown } from "notion-to-md";

// 环境变量
const NOTION_API_KEY = process.env.NOTION_API_KEY;
const NOTION_DATABASE_ID = process.env.NOTION_DATABASE_ID;

// 初始化客户端
const notion = new Client({ auth: NOTION_API_KEY });
const n2m = new NotionToMarkdown({ notionClient: notion });

/**
 * 获取已发布文章
 */
async function fetchArticles() {
    const response = await notion.databases.query({
        database_id: NOTION_DATABASE_ID,
        filter: {
            property: "Status",
            select: { equals: "Published" },
        },
    });
    return response.results;
}

/**
 * 删除目录（递归）
 */
function removeDirRecursive(dirPath) {
    if (fs.existsSync(dirPath)) {
        fs.readdirSync(dirPath).forEach((file) => {
            const curPath = path.join(dirPath, file);
            if (fs.lstatSync(curPath).isDirectory()) {
                removeDirRecursive(curPath);
            } else {
                fs.unlinkSync(curPath);
            }
        });
        fs.rmdirSync(dirPath);
    }
}

/**
 * 下载图片到本地
 */
async function downloadImage(url, imageDir, filename) {
    if (!fs.existsSync(imageDir)) {
        fs.mkdirSync(imageDir, { recursive: true });
    }

    const res = await fetch(url);
    if (!res.ok) throw new Error(`❌ Failed to download ${url}`);

    const filePath = path.join(imageDir, filename);
    const buffer = await res.arrayBuffer();
    fs.writeFileSync(filePath, Buffer.from(buffer));

    // 返回 Markdown 引用路径（相对仓库根目录）
    return `/${path.join(imageDir, filename)}`;
}

/**
 * 异步替换字符串
 */
async function replaceAsync(str, regex, asyncFn) {
    const promises = [];
    str.replace(regex, (match, ...args) => {
        const promise = asyncFn(match, ...args);
        promises.push(promise);
    });
    const data = await Promise.all(promises);
    return str.replace(regex, () => data.shift());
}

/**
 * 保存 Markdown
 */
async function saveAsMarkdown(page) {
    const title = page.properties.Title?.title[0]?.plain_text || "Untitled";
    const date = page.properties.Date?.date?.start || new Date().toISOString().split("T")[0];
    const tags = page.properties.Tags?.multi_select?.map((t) => t.name) || [];
    const categories = page.properties.Categories?.multi_select?.map((c) => c.name) || [];
    const saveDir = page.properties.SaveDir?.rich_text[0]?.plain_text || "_posts";
    const imageDir = page.properties.ImageDir?.rich_text[0]?.plain_text || `assets/images/${title.replace(/\s+/g, "-")}`;
    const author = page.properties.Author?.rich_text[0]?.plain_text || "unknown";
    const comments = page.properties.Comments?.checkbox ?? true;
    const math = page.properties.Math?.checkbox ?? true;
    const mermaid = page.properties.Mermaid?.checkbox ?? true;

    // 清理旧图片
    if (fs.existsSync(imageDir)) {
        console.log(`🧹 Cleaning old images for "${title}" ...`);
        removeDirRecursive(imageDir);
    }

    // 转 Markdown
    const mdBlocks = await n2m.pageToMarkdown(page.id);
    let mdString = n2m.toMarkdownString(mdBlocks);

    // 替换 Notion 图片为本地路径
    const imageRegex = /!\[.*?\]\((https:\/\/www.notion.so\/.*?\/.*?\?v=.*?)\)/g;
    mdString = await replaceAsync(mdString, imageRegex, async (match, url) => {
        const filename = url.split("/").pop().split("?")[0] || "image.png";
        const localUrl = await downloadImage(url, imageDir, filename);
        return `![image](${localUrl})`;
    });

    // 构建 front matter
    const frontMatter = `---
layout: post
title: "${title}"
date: ${date}
tags:
${tags.map((t) => `  - ${t}`).join("\n")}
categories:
${categories.map((c) => `  - ${c}`).join("\n")}
comments: ${comments}
math: ${math}
mermaid: ${mermaid}
author: ${author}
images_dir: ${imageDir}
---
`;

    // 保存 Markdown
    if (!fs.existsSync(saveDir)) {
        fs.mkdirSync(saveDir, { recursive: true });
    }
    const filename = `${date}-${title.replace(/\s+/g, "-")}.md`;
    const filePath = path.join(saveDir, filename);

    fs.writeFileSync(filePath, frontMatter + "\n" + mdString, "utf-8");
    console.log(`✅ Saved: ${filePath}`);
}

/**
 * 主函数
 */
async function main() {
    const articles = await fetchArticles();
    for (const page of articles) {
        await saveAsMarkdown(page);
    }
}

main().catch((err) => console.error(err));
