---
layout: post
title: Java 中的 Queue
slug: java-queue
type:
- note
date: 2018-02-13
week: 2025-W48
status: draft
tags:
- Java
author: deathwhispers
created: 2018-02-13 11:32
updated: 2018-02-13 11:32
categories:
- Learning
- Java
---

# Queue

queue容器：

![](/assets/images/learning/java/java-queue/8d6f56121c8ebd06f9519f8e2d246360.png)

1.ConcurrentLinkedQueue：基础链表同步队列

适用于高并发场景下的队列、无锁，实现高并发状态下的高性能

**高性能无阻塞无界队列**

**先进先出原则。**

add()和offer()都是加入元素的方法（在ConcurrentLinkedQueue中，这两个方法没有任何区别）

poll()和peek()：都是取头部元素节点。区别在于前者会删除元素（先取出元素再将该元素删除），后者不会

2.BlockingQueue接口：阻塞队列

ReentrantLock & Condition(只能在独占模式下使用)

2.1ArrayBlockingQueue：

- 基于**数组**阻塞队列实现，在 ArrayBlockingQueue内部，**维护了一个定长数组，不可扩容**
- 可以指定先进先出或者先进后出
- 是一个**有界**
队列
- 生产者和消费者并不能完全并行
- put方法在容量不足时，阻塞能力，等待消费
- add() - 容量不足时，抛出异常
- 底层是数组实现的有界队列。自动阻塞。根据API(add/put/offer)不同，有不同的特性

offer():

```plain text
1. 单参数offer方法，不阻塞。容量不足时，返回false。<font style="background-color:rgb(255, 250, 165);">当前新增数据操作放弃</font>
2. 三参数offer方法（offer(value,times,timeunit)），容量不足时，阻塞times时长（单位为timeunit），如果在阻塞时长内，有容量空闲，新增数据返回true。如果阻塞时长范围内，无容量空闲，放弃新增数据，返回false
```

2.2LinkedBlockingQueue：

- 基于链表的的阻塞队列，内部维持了一个数据缓冲队列（由链表组成）
- put自动阻塞：队列容量满后，自动阻塞
- take自动阻塞：队列容量为0时，自动阻塞
- 是一个**无界队列**
- 其内部
采用分离锁（读写分离两个锁）生产者和消费者操作完全并行运行

2.3PriorityBlockingQueue：阻塞队列

由优先级堆支持的无界优先级队列，（为什么是无界，每次数组容量达到最大值时，会进行自动扩容）

- **必须实现comparator接口 – 通过该**
Compator来确定大小
- 每次调用take方法时，取出队列中优先
- 级最高的元素（取出后，该元素从原容器中移除）

transient：表示当前的属性不需要序列化

3.DelayQueue:**必须实现Delay接口**

有点类似定时任务

延时队列。根据比较机制，实现自定义处理顺序的队列。常用于定时任务。

如：定时关机。

通过ReentrantLock实现线程安全

4.TransferQueue

```plain text
并发容器 － LinkedTransferQueue

转移队列，使用 transfer 方法，实现数据的即时处理。没有消费者，就阻塞。

add - 队列会保存数据，不做阻塞等待

transfer - 是TransferQueue的特有方法。必须有消费者

如果线程去消费数据，transfer方法阻塞。一般用于处理即时消息
```

4.1SynchronousQueue:

一个没有缓冲的队列，生产者数据直接被消费者获取并消费

- **同步队列，是一个容量为 0 的队列。是一个特殊的 TransferQueue。**
- **必须现有消费线程等待，才能使用的队列。**
- add 方法，**无阻塞**
。若没有消费线程阻塞等待数据，则抛出异常。
- put 方法，**有阻塞**
。若没有消费线程阻塞等待数据，则阻塞。

![](/assets/images/learning/java/java-queue/14045b7547dc41257f7d209dbb0c8136.png)
