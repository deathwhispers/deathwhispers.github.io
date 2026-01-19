---
layout: post
title: 死磕Java并发：Java内存模型之happens-before
slug: concurrent-source-code-happens-before
type:
  - note
date: 2020-05-25
week: 2025-W48
status: draft
tags:
  - Java并发源码分析
categories:
  - Java
author: deathwhispers
created: 2020-05-25 11:55
updated: 2020-05-25 11:55
---
[https://www.iocoder.cn/JUC/sike/happens-before/](https://www.iocoder.cn/JUC/sike/happens-before/)

在上篇博客（《【死磕 Java 并发】—– 深入分析 volatile 的实现原理》）中，LZ 提到过由于存在线程本地内存和主内存的原因，再加上重排序，会导致多线程环境下存在可见性的问题。那么我们正确使用同步、锁的情况下，线程 A 修改了变量 a ，何时对线程 B 可见？

我们无法就所有场景来规定，某个线程修改的变量何时对其他线程可见，但是我们可以指定某些规则，这规则就是 happens-before 。从 JDK 5 开始，JMM 就使用 happens-before 的概念，来阐述多线程之间的内存可见性。

在 JMM 中，如果一个操作执行的结果需要对另一个操作可见，那么这两个操作之间必须存在 happens-before 关系。

happens-before 原则非常重要，它是判断数据是否存在竞争、线程是否安全的主要依据，依靠这个原则，我们解决在并发环境下两操作之间是否可能存在冲突的所有问题。下面我们就一个简单的例子稍微了解下happens-before ；

i = 1; // 线程 A 执行 j = i; //线程 B 执行

j 是否等于 1 呢？假定线程 A 的操作（i = 1）happens-before 线程 B 的操作（j = i），那么可以确定，线程 B 执行后 j = 1 一定成立。如果他们不存在 happens-before 原则，那么 j = 1 不一定成立。这就是happens-before原则的威力。

# 1. 定义

happens-before 原则【定义】如下：

```plain text
1. 如果一个操作 happens-before 另一个操作，那么第一个操作的执行结果，将对第二个操作可见，而且第一个操作的执行顺序，排在第二个操作之前。
1. 两个操作之间存在 happens-before 关系，并不意味着一定要按照 happens-before 原则制定的顺序来执行。如果重排序之后的执行结果与按照 happens-before 关系来执行的结果一致，那么这种重排序并不非法。
```

# 2. 规则

happens-before 原则【规则】如下：

FROM 《深入理解 Java 虚拟机》

程序次序规则：一个线程内，按照代码顺序，书写在前面的操作，happens-before 于书写在后面的操作。锁定规则：一个 unLock 操作，happens-before 于后面对同一个锁的 lock 操作。volatile 变量规则：对一个变量的写操作，happens-before 于后面对这个变量的读操作。传递规则：如果操作 A happens-before 操作 B，而操作 B happens-before 操作C，则可以得出，操作 A happens-before 操作C线程启动规则：Thread 对象的 start 方法，happens-before 此线程的每个一个动作。线程中断规则：对线程 interrupt 方法的调用，happens-before 被中断线程的代码检测到中断事件的发生。线程终结规则：线程中所有的操作，都 happens-before 线程的终止检测，我们可以通过Thread.join() 方法结束、Thread.isAlive() 的返回值手段，检测到线程已经终止执行。对象终结规则：一个对象的初始化完成，happens-before 它的 finalize() 方法的开始

上面八条是原生 Java 满足 happens-before 关系的规则，但是我们可以对他们进行推导出其他满足 happens-before 的规则：

1. 将一个元素放入一个线程安全的队列的操作，happens-before 从队列中取出这个元素的操作。
2. 将一个元素放入一个线程安全容器的操作，happens-before 从容器中取出这个元素的操作。
3. 在 CountDownLatch 上的 countDown 操作，happens-before CountDownLatch 上的 await 操作。
4. 释放 Semaphore 上的 release 的操作，happens-before 上的 acquire 操作。
5. Future 表示的任务的所有操作，happens-before Future 上的 get 操作。
6. 向 Executor 提交一个 Runnable 或 Callable 的操作，happens-before 任务开始执行操作。

这里再说一遍 happens-before 的概念：如果两个操作不存在上述（前面8条 + 后面6条）任一一个 happens-before 规则，那么这两个操作就没有顺序的保障，JVM 可以对这两个操作进行重排序。如果操作 A happens-before 操作 B，那么操作A在内存上所做的操作对操作B都是可见的。

下面就用一个简单的例子，来描述下 happens-before 的原则：

private int i = 0; public void write(int j ) { i = j; } public int read() { return i; }

我们约定线程 A 执行 #write(int j)，线程 B 执行 #read()，且线程 A 优先于线程 B 执行，那么线程 B 获得结果是什么？

就这段简单的代码，我们来基于 happens-before 的规则做一次分析：

7. 由于两个方法是由不同的线程调用，所以肯定不满足程序次序规则。
8. 两个方法都没有使用锁，所以不满足锁定规则。
9. 变量 i 不是用volatile修饰的，所以 volatile 变量规则不满足。
10. 传递规则肯定不满足。
11. 规则 5、6、7、8 + 推导的 6 条可以忽略，因为他们和这段代码毫无关系。

所以，我们无法通过 happens-before 原则，推导出线程 A happens-before 线程 B 。虽然，可以确认在时间上，线程 A 优先于线程 B 执行，但是就是无法确认线程B获得的结果是什么，所以这段代码不是线程安全的。

那么怎么修复这段代码呢？满足规则 2、3 任一即可。

---

happen-before原则是JMM中非常重要的原则，它是判断数据是否存在竞争、线程是否安全的主要依据，保证了多线程环境下的可见性。

下图是 happens-before 与 JMM 的关系图：

FROM 《Java并发编程的艺术》

![](/assets/images/learning/java/concurrencecode/concurrent-source-code-happens-before/3980ff20799e41ead84e6efd2bee64c1.jpg)

# 参考资料

12. 周志明：《深入理解Java虚拟机》
13. 方腾飞：《Java并发编程的艺术》

# 666. 彩蛋

整理本小节，简单脑图如下：

![](/assets/images/learning/java/concurrencecode/concurrent-source-code-happens-before/020a0135b5ac53f71f8cd3d2f1cfac3e.png)

如果你对 Java 并发感兴趣，欢迎加入我的知识星球一起交流。