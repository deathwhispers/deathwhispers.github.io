---
layout: post
title: ThreadLocal 的底层原理（整合版）
slug: threadlocal-underlying-principle
type:
  - note
date: 2020-06-22
week: 2025-W48
status: draft
tags:
  - Java并发
  - ThreadLocal
categories:
  - Java
  - 并发
author: deathwhispers
created: 2020-06-22 22:58
updated: 2026-04-20 18:30
---

本文整合了 `ThreadLocal的底层原理` 与 `threadlocal` 两篇笔记。

## 1. ThreadLocal 是什么

`ThreadLocal` 提供“线程本地变量”能力：同一个 `ThreadLocal` 对象，在不同线程里读到的是各自独立的数据副本。

它的目标不是线程共享，而是线程隔离。

## 2. 底层结构

很多同学容易误解为：`ThreadLocal -> Map<Thread, Value>`。

更准确是：

- 每个 `Thread` 对象内部有一个 `ThreadLocalMap`。
- `ThreadLocalMap` 的 key 是 `ThreadLocal`（弱引用）。
- value 是线程保存的业务数据。

## 3. 为什么可能内存泄漏

在线程池场景，线程会复用且长期存活：

- `ThreadLocal` key 可能被回收（弱引用失效）。
- value 仍可能挂在 `ThreadLocalMap` 里，直到后续清理逻辑触发。
- 如果不手动 `remove()`，脏数据和内存占用会累积。

## 4. 正确使用姿势

```java
private static final ThreadLocal<String> TRACE_ID = new ThreadLocal<>();

public void handle() {
    try {
        TRACE_ID.set(generateTraceId());
        // 业务逻辑
    } finally {
        TRACE_ID.remove();
    }
}
```

关键点：`set` 和 `remove` 成对出现，尤其在 web 容器线程池、MQ 消费线程池中。

## 5. 常见应用场景

- 请求链路追踪（TraceId）
- 数据库连接/事务上下文绑定
- 用户上下文、租户上下文
- 非线程安全对象的线程封闭缓存

## 6. 不建议的场景

- 在线程间传递业务数据（应使用参数传递或上下文对象）
- 异步线程池链路中直接依赖父线程 `ThreadLocal`（可能丢失）

## 相关阅读

- [Java 并发学习索引](/posts/java-concurrency-study-index/)
- [线程通信-等待通知机制（整合版）](/posts/thread-communication-wait-notify/)
- [第3章：Java并发包中的ThreadLocalRandom类原理剖析](/posts/java-thread-local-random-principle-analysis/)
