---
layout: post
title: MySQL MVCC实现机制
author: deathwhispers
date: 2021-06-10
slug: mysql-mvcc-implementation-mechanism
categories:
- Database
tags:
- MySQL
- Database
type: note
created: 2021-06-10 11:45
updated: 2021-06-10 22:17
---

# MySQL MVCC实现机制

## 什么是MVC## 什么是MVCC

MVCC是一种多版本并发控制机制

## MVCC是为了解决什么问题

## MVCC实现

MVCC是通过保存数据在某个时间点的快照来实现的

## MVCC具体实现分析

InnoDB的MVCC是通过在每行记录后面保存两个隐藏列来实现的**一个保存了行的事务ID（DB_TRX_ID），一个保存了行的回滚指针（DB_ROLL_PT）**每开始一个新事物，都会自动递增产生一个新的事务id，事务开始时刻会把事务id放到当前事务影响的行事务id中，当查询时需要用当前事务id和每行记录的事务id进行比较
