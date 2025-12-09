---
layout: post
title: synchronized关键字的基本语义
slug: java-synchronized-keyword-semantics
type:
  - note
date: 2025-11-28
week: 2025-W48
status: draft
tags:
  - 并发编程
categories:
  - Java
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---
# synchronized关键字的基本语义

synchronized锁什么？

锁对象。是一个对象锁

可能锁的对象包括: this，临界资源对象，Class类对象