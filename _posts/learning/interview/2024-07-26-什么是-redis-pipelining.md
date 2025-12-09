---
layout: post
title: 什么是 Redis Pipelining ？
slug: interview-what-is-redis-pipelining
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

# 什么是 Redis Pipelining ？

一次请求/响应服务器能实现处理新的请求即使旧的请求还未被响应。这样就可以将多个命令发送到服务器，而不用等待回复，最后在一个步骤中读取该答复。

注意，Redis Pipelining 是 Redis Client 实现的功能，而不是 Redis Server 提供的特性。假设我们有 3 个请求进行下举例子。

- 未使用 Pipeline 时，那么整个执行的顺序是，req1->resp1->req2->resp2->req3->resp3 。
- 在使用 Pipeline 时，那么整个执行的顺序是，[req1,req2,req3] 一起发给 Redis Server ，而 Redis Server 收到请求后，一个一个请求进行执行，然后响应，不会进行什么特殊处理。而 Client 在收到 resp1,resp2,resp3 后，进行响应给业务上层。

所以，Pipeline 的作用，是避免每发一个请求，就阻塞等待这个请求的结果。

这就是管道（pipelining），是一种几十年来广泛使用的技术。例如许多 POP3 协议已经实现支持这个功能，大大加快了从服务器下载新邮件的过程。

Redis 很早就支持管道（pipelining）技术，因此无论你运行的是什么版本，你都可以使用管道（pipelining）操作 Redis。

🦅 **Redis 如何做大量数据插入？**

Redis 2.6 开始，Redis-cli 支持一种新的被称之为 pipe mode 的新模式用于执行大量数据插入工作。

具体可见 [《Redis 大量数据插入》](http://www.redis.cn/topics/mass-insert.html) 文章。