---
layout: post
title: 原生的 NIO 存在 Epoll Bug 是什么？Netty 是怎么解决的？
slug: interview-why-epoll-bug-in-java-nio-and-how-netty-solve-it
date: 2024-07-26
type:
  - note
tags:
  - NIO
categories:
  - interview
author: deathwhispers
created: 2024-07-26 11:48
updated: 2024-07-26 11:48
---

🦅 Java NIO Epoll BUG

Java NIO Epoll 会导致 Selector 空轮询，最终导致 CPU 100% 。

官方声称在 JDK 1.6 版本的 update18 修复了该问题，但是直到 JDK 1.7 版本该问题仍旧存在，只不过该 BUG 发生概率降低了一些而已，它并没有得到根本性解决。

🦅 Netty 解决方案

对 Selector 的 select 操作周期进行统计，每完成一次空的 select 操作进行一次计数，若在某个周期内连续发生 N 次空轮询，则判断触发了 Epoll 死循环 Bug 。

艿艿：此处空的 select 操作的定义是，select 操作执行了 0 毫秒。

此时，Netty 重建 Selector 来解决。判断是否是其他线程发起的重建请求，若不是则将原 SocketChannel 从旧的 Selector 上取消注册，然后重新注册到新的 Selector 上，最后将原来的 Selector 关闭。