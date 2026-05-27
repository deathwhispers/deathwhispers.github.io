---
layout: post
title: Optional 优雅处理 null（整合版）
slug: optional-elegant-use-of-null
type:
- note
date: 2022-12-10
week: 2025-W48
status: draft
tags:
- Java
categories:
- Learning
- Java
author: deathwhispers
created: 2022-12-10 15:25
updated: 2026-04-20 18:30
---

本文整合了 `Java8 Optional的使用详解` 与 `Optional 优雅的使用 null`，以 JDK Optional 为主线。

## 1. 为什么需要 Optional

`null` 本身语义模糊：

- 是“值不存在”？
- 是“查询失败”？
- 是“尚未初始化”？

`Optional<T>` 用类型系统显式表达“值可能不存在”，让调用方必须面对空值分支。

## 2. 常用创建方式

```java
Optional<String> a = Optional.of("hello");
Optional<String> b = Optional.ofNullable(possiblyNullValue);
Optional<String> c = Optional.empty();
```

- `of`：参数不能为 `null`
- `ofNullable`：可空
- `empty`：显式空

## 3. 读取与兜底

```java
String v1 = op.orElse("default");
String v2 = op.orElseGet(this::buildDefault);
String v3 = op.orElseThrow(() -> new IllegalStateException("missing"));
```

- `orElse`：即使有值也会先计算默认值
- `orElseGet`：懒加载默认值，更适合默认值构造成本高的场景

## 4. 转换链路

```java
Optional<String> name = userOpt
    .map(User::getProfile)
    .map(Profile::getName)
    .filter(n -> !n.isBlank());
```

- `map`：值存在时转换
- `flatMap`：避免 `Optional<Optional<T>>`
- `filter`：条件过滤

## 5. 使用边界（非常重要）

建议：

- 用作“方法返回值”表达可空结果。
- 在查询、解析、组装流程中替代多层 `if (x != null)`。

不建议：

- 作为实体字段（会增加序列化、ORM 复杂度）。
- 作为方法入参（直接传真实类型更清晰）。
- 盲目 `isPresent()+get()`（回到旧式判空写法）。

## 6. JDK Optional 与 Guava Optional

历史上 Guava 提供过 `Optional`；Java 8 以后优先使用 `java.util.Optional`，新项目建议统一到 JDK 版本，避免两套 Optional 混用。

## 相关阅读

- [Java8 新特性实战](/posts/java8-new-features-practice/)
- [Lambda介绍](/posts/lambda-introduction/)
- [Guava 常用功能](/posts/guava-common-features/)
