---
layout: post
title: threadlocal
slug: threadlocal
type:
  - note
date: 2020-08-03
week: 2025-W48
status: draft
tags:
  - threadlocal
author: deathwhispers
created: 2020-08-03 15:31
updated: 2020-08-03 15:31
---
# threadlocal

ThreadLocal 就是一个map

key -> Thread.getCurrentThread()

value -> 线程需要保存的变量

![](/assets/images/learning/java/threadlocal/310db01107c906e65aaa8298209c90e8.jpg)

内存问题： 在并发量高的时候，可能有内存溢出

使用ThreadLocalde shihou ,一定注意回收资源问题，每一个线程结束之前，将当前线程保存的线程变量一定要删除。

ThreadLocal。remove();

不是线程回收了，ThreadLocal就回收了

线程结束，回收的知识线程中的数据；