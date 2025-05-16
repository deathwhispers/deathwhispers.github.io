---
layout: post
title: "修改服务器时间"
date: 2024-08-29
tags: [hwclock]
comments: true
author: deathwhispers
---

## 前言
甲方自建机房，系统均在内网运行，因为该项目仅用到一台服务器，也没有做时钟同步。

某天突然收到消息，说系统中出现了很多2000-xx-xx的时间，故留此记录。

<!-- more -->

## 修改时间
1. date 查看系统时间
2. 临时修改Linux时间：date -s 时间
3. 查看硬件时间
    1. hwclock --show
4. 修改硬件的时间 也是永久性修改Linux的时间
    1. hwclock --set --date '2021-08-16 17:17:00' 设置硬件时间为2021年8月16日17点17分00秒
5. 设置系统时间和硬件时间同步
    1. hwclock --hctosys
6. 保存时钟
    1. clock -w

## 后记

有很多项目并没有那么高大上，运用前沿的技术手段来实现，反而很原始，因此，需要留意的地方也更多。

