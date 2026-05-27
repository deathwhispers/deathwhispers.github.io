---
layout: post
title: Spring事务-@Transactional使用
slug: spring-transactional-usage
type:
- note
date: 2017-12-01
week: 2017-W48
status: draft
tags:
- Spring
author: deathwhispers
created: 2017-12-01 10:00
updated: 2017-12-01 10:00
categories:
- Learning
- Spring
---

事务是指逻辑上的一组操作,组成这组操作的各个单元,要么全部成功,要么全部失败

事务的基本要素

- 原子性: 事务是原子的,即事务开始后所有的操作,要么全部做完,要么全部不做,不能停滞在中间的某个环节.事务执行过程中出错,会回滚到事务开始前的状态,所有的操作就像没有发生一样.也就是说事务是一个不可分割的整体
- 隔离性: 同一时间,只允许一个事务请求同一数据,不同的事务之间彼此没有任何干扰.比如A正在一张银行卡中取钱,在A取钱结束前,B不能向这张卡转账
- 一致性: 事务开始前和结束后,数据库的完整性约束没有被破坏.比如A向B转账,不可能A扣了钱而B却没有收到
- 持久性; 事务完成后,事务对数据库的所有更新将被保存到数据库,不能回滚.
