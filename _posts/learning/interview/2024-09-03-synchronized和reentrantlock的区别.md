---
layout: post
title: Synchronized和ReentrantLock的区别
author: deathwhispers
date: 2024-09-03
slug: interview-synchronized-and-reentrantlock-differences
categories:
- Interview
tags:
- Java
- Redis
- Network
type: note
created: 2024-07-26 11:48
updated: 2024-07-26 11:48
---

1. synchronized是一个关键字，ReentrantLock是一个类
2. synchronized会自动的加锁与释放锁，ReentrantLock需要手动加锁与释放锁
3. synchronized的底层是JVM层面的锁，ReentrantLock是API层面的锁
4. synchronized是非公平锁，ReentrantLock在初始化时，可以选择是公平或非公平锁。
5. synchronized锁的是对象，锁信息保存在对象头中，ReentrantLock通过代码中int类型的state标识锁的状态
6. synchronized底层有一个锁升级的过程

### synchronized锁升级的过程

### synchronized的自旋锁、偏向锁、轻量级锁、重量级锁

7. 偏向锁：在锁对象的对象头中记录一下当前获取到该锁的线程ID，该线程下次如果又来获取该锁就可以直接获取到了
8. 轻量级锁：由偏向锁升级而来，当一个线程获取到锁后，此时这把锁是偏向锁，此时如果由第二个线程来竞争锁，偏向锁就会升级为轻量级锁，之所以叫轻量级锁，是为了和重量级锁区分开来，轻量级锁底层是通过自旋来实现的，并不会阻塞线程。
9. 如果自旋次数过多仍然没有获取到锁，则会升级为重量级锁，重量级锁会导致线程阻塞。
10. 自旋锁：自旋锁就是线程在获取锁的过程中，不会去阻塞线程，也就无所谓唤醒线程，阻塞和唤醒这两个步骤都是需要操作系统去进行的，比较消耗实际，自旋锁是线程通过CAS获取预期的一个标记，如果没有获取到，则继续循环获取，如果获取到了则表示获取到了锁，这个过程线程一直在运行中，相对而言没有使用太多的操作系统资源，比较轻量。
