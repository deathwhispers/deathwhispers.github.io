---
layout: post
title: Netty 自己实现的 ByteBuf 有什么优点？
slug: interview-netty-bytebuf-advantages
date: 2024-07-26
type:
  - note
tags:
  - Redis
categories:
  - interview
author: deathwhispers
created: 2024-07-26 11:48
updated: 2024-07-26 11:48
---

## Netty 自己实现的 ByteBuf 有什么优点？

- A01. 它可以被用户自定义的缓冲区类型扩展
- A02. 通过内置的符合缓冲区类型实现了透明的零拷贝
- A03. 容量可以按需增长
- A04. 在读和写这两种模式之间切换不需要调用 #flip() 方法
- A05. 读和写使用了不同的索引
- A06. 支持方法的链式调用
- A07. 支持引用计数
- A08. 支持池化
- 特别是第 A04 这点，相信很多胖友都被 NIO ByteBuffer 反人类的读模式和写模式给坑哭了。在 《精尽 Netty 源码分析 —— NIO 基础（三）之 Buffer》 中，我们也吐槽过了。😈