---
layout: post
title: C/C++配置环境变量
slug: c_c++-config-env-variable
type:
  - note
date: 2023-06-12
status: draft
tags:
  - C_C++
categories:
  - C_C++
author: deathwhispers
created: 2025-06-12 10:34
updated: 2025-06-12 10:34
---

# C/C++配置环境变量

一、安装GNU的C++编译器

为了在 Windows 上安装 GCC，您需要安装 MinGW。为了安装 MinGW，请访问 MinGW 的主页 [www.mingw.org](http://www.mingw.org/)，进入 MinGW 下载页面，然后进行安装，

![Image.png](/assets/images/learning/c_c%2B%2B/Image.png)

![Image [1].png](/assets/images/learning/c_c%2B%2B/Image%20%5B1%5D.png)

![Image [2].png](/assets/images/learning/c_c%2B%2B/Image%20%5B2%5D.png)


添加你安装的 MinGW 的 bin 子目录到您的 **PATH** 环境变量中，这样您就可以在命令行中通过简单的名称来指定这些工具。

1、在命令行（cmd）输入g++ –version查看g++版本，确认path是否生效。

2、用cmd命令提示符输入: gcc -v。如果出现如下信息说明MinGW安装正确