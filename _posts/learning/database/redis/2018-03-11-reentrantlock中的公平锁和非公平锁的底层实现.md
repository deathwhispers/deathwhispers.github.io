---
layout: post
title: ReentrantLock中的公平锁和非公平锁的底层实现
slug: reentrantlock-fair-lock-and-non-fair-lock-implementation
type:
- note
date: 2018-03-11
tags:
- Redis
- Database
categories:
- Learning
- Database
author: deathwhispers
created: 2019-05-11 11:45
updated: 2019-05-11 22:17
---

# ReentrantLock中的公平锁和非公平锁的底层实现

首先不管是公平锁和非公平锁，它们的底层实现都会使用AQS来进行排队，它们的区别在于：线程在使用lock()方法加锁时，如果是公平锁，会先检查AQS队列中是否存在线程在排队，如果有线程在排队，则当前线程也进行排队，如果是非公平锁，则不会去检查是否有线程在排队，而是直接竞争锁。

不管是公平锁还是非公平锁，一旦没有竞争到锁，都会进行排队，当锁释放时，都是唤醒排在最前面的线程，所以非公平锁只是体现在了线程加锁阶段，而没有体现在线程被唤醒阶段。

另外，ReentrantLock是可重入锁，不管是公平锁还是非公平锁都是可重入的。

![](assets/images/learning/database/redis/reentrantlock-fair-lock-and-non-fair-lock-implementation/1698218796239-d924bbf1-ce42-40fd-bace-5a5443652fd7.png)

![](assets/images/learning/database/redis/reentrantlock-fair-lock-and-non-fair-lock-implementation/1698218796332-61744097-34a4-4178-bdd6-70b17df74296.png)

### ReentrantLock中tryLock()和lock()方法的区别

1. tryLock()表示尝试加锁，可能加到，也可能加不到，该方法不会阻塞线程，如果加到锁则返回true，没有加到则返回false
2. lock()表示阻塞加速，线程会阻塞直到加上锁，方法也没有返回值。
