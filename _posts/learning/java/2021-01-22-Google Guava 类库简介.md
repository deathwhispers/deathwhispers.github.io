---
layout: post
title: Google Guava 类库简介
slug: guava-class-library-introduction
type:
  - note
date: 2021-01-22
week: 2025-W48
status: draft
tags:
  - guava
author: deathwhispers
created: 2021-01-22 14:36
updated: 2021-01-22 14:36
---


# 1. 项目相关信息

- 官方首页：[http://code.google.com/p/guava-libraries](http://code.google.com/p/guava-libraries)
- 官方下载：[http://code.google.com/p/guava-libraries/downloads/list](http://code.google.com/p/guava-libraries/downloads/list)
- 官方文档：
    - [http://docs.guava-libraries.googlecode.com/git/javadoc](http://docs.guava-libraries.googlecode.com/git/javadoc)
    - [http://www.ostools.net/apidocs/apidoc?api=guava](http://www.ostools.net/apidocs/apidoc?api=guava)

# 2. 源码包的简单说明

- com.google.common.annotations：普通注解类型。
- com.google.common.base：基本工具类库和接口。
- com.google.common.cache：缓存工具包，非常简单易用且功能强大的JVM内缓存。
- com.google.common.collect：带泛型的集合接口扩展和实现，以及工具类，这里你会发现很多好玩的集合。
- com.google.common.eventbus：发布订阅风格的事件总线。
- com.google.common.hash： 哈希工具包。
- com.google.common.io：I/O工具包。
- com.google.common.math：原始算术类型和超大数的运算工具包。
- com.google.common.net：网络工具包。
- com.google.common.primitives：八种原始类型和无符号类型的静态工具包。
- com.google.common.reflect：反射工具包。
- com.google.common.util.concurrent：多线程工具包。

# 3. 类库使用手册

## 3.1 基本工具类

让使用Java语言更令人愉悦。

1. 使用和避免 null：null 有语言歧义， 会产生令人费解的错误， 反正他总是让人不爽。很多 Guava 的工具类在遇到 null 时会直接拒绝或出错，而不是默默地接受他们。
2. 前提条件：更容易的对你的方法进行前提条件的测试。
3. 常见的对象方法： 简化了Object常用方法的实现， 如 hashCode() 和 toString()。
4. 排序： Guava 强大的 “fluent Comparator”比较器， 提供多关键字排序。
5. Throwable类： 简化了异常检查和错误传播。

## 3.2 集合类

集合类库是 Guava 对 JDK 集合类的扩展， 这是 Guava 项目最完善和为人所知的部分。

6. Immutable collections（不变的集合）： 防御性编程， 不可修改的集合，并且提高了效率。
7. New collection types(新集合类型)：JDK collections 没有的一些集合类型，主要有：multisets，multimaps，tables， bidirectional maps等等
8. Powerful collection utilities（强大的集合工具类）： java.util.Collections 中未包含的常用操作工具类
9. Extension utilities（扩展工具类）: 给 Collection 对象添加一个装饰器? 实现迭代器? 我们可以更容易使用这些方法。

## 3.3 缓存

本地缓存，可以很方便的操作缓存对象，并且支持各种缓存失效行为模式。

## 3.4 Functional idioms（函数式）

简洁, Guava实现了Java的函数式编程，可以显著简化代码。

## 3.5 Concurrency（并发）

强大,简单的抽象,让我们更容易实现简单正确的并发性代码。

10. ListenableFuture（可监听的Future）: Futures,用于异步完成的回调。
11. Service: 控制事件的启动和关闭，为你管理复杂的状态逻辑。

## 3.6 Strings

一个非常非常有用的字符串工具类: 提供 splitting，joining， padding 等操作。

## 3.7 Primitives

扩展 JDK 中未提供的对原生类型（如int、char等）的操作， 包括某些类型的无符号的变量。

## 3.8 Ranges

Guava 一个强大的 API，提供 Comparable 类型的范围处理， 包括连续和离散的情况。

## 3.9 I/O

简化 I/O 操作, 特别是对 I/O 流和文件的操作, for Java 5 and 6.

## 3.10 Hashing

提供比 Object.hashCode() 更复杂的 hash 方法, 提供 Bloom filters.

## 3.11 EventBus

基于发布-订阅模式的组件通信，但是不需要明确地注册在委托对象中。

## 3.12 Math

优化的 math 工具类，经过完整测试。

## 3.13 Reflection

Guava 的 Java 反射机制工具类。