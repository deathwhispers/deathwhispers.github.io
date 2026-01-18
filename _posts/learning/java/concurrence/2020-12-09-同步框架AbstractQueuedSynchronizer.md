---
layout: post
title: 同步框架AbstractQueuedSynchronizer
slug: java-abstractqueuedsynchronizer
type:
  - note
date: 2020-12-09
week: 2025-W48
status: draft
tags:
  - 并发编程
categories:
  - Java
author: deathwhispers
created: 2020-12-09 22:51
updated: 2020-12-09 22:51
---


# 同步框架AbstractQueuedSynchronizer

java并发核心在于 java.concurrent.util 当中同步器的实现

同步容器

解决并发情况下的容器线程安全问题。给多线程环境准备一个线程安全的容器对象

线程安全的容器对象L Vector，Hashtable；它们时通过synchronized方法实现的。

concurrent 包中的同步容器，大多数是使用系统底层技术实现的线程安全，类似于native。java8中是通过 CAS

1.Map/Set