---
layout: post
title: synchronized 关键字（整合版）
slug: java-synchronized-keyword
type:
  - note
date: 2019-07-18
week: 2025-W48
status: draft
tags:
  - Java并发
  - synchronized
categories:
  - Java
  - 并发
author: deathwhispers
created: 2019-07-18 16:37
updated: 2026-04-20 19:30
---

## 什么是 synchronized

`synchronized` 是 Java 内置同步关键字，本质是对象监视器（Monitor）锁。

## synchronized 锁的到底是什么

答案是“锁对象”。

- 实例方法：锁当前实例（`this`）。
- 静态方法：锁当前类对象（`Class`）。
- 同步代码块：锁 `synchronized(obj)` 中的 `obj`。

## 常见使用方式

1. 同步代码块：作用于大括号内临界区。  
2. 同步实例方法：作用于整个实例方法。  
3. 同步静态方法：作用于整个静态方法。  

```java
public class Demo {
    private final Object lock = new Object();

    public void methodA() {
        synchronized (lock) {
            // 临界区
        }
    }

    public synchronized void methodB() {
        // 锁 this
    }

    public static synchronized void methodC() {
        // 锁 Demo.class
    }
}
```

## 语义速记

- 可重入：同一线程可重复进入同一把锁。  
- 可见性：释放锁前的写，对后续获取同一锁的线程可见。  
- 互斥性：同一时刻仅有一个线程持有同一把对象锁。  

## 相关阅读

- [Java Lock 接口（整合版）](/posts/java-lock-interface/)
- [死磕Java并发：深入分析synchronized的实现原理](/posts/concurrent-source-code-synchronized/)
- [死磕Java并发：深入分析volatile的实现原理](/posts/concurrent-source-code-volatile/)
