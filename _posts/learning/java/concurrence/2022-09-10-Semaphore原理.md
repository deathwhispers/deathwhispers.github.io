---
layout: post
title: Semaphore 原理
slug: concurrent-source-code-semaphore
type:
  - note
date: 2022-09-10
week: 2025-W48
status: draft
tags:
  - Java并发源码分析
  - Java并发系列
categories:
  - Java
author: deathwhispers
created: 2022-09-10 09:10
updated: 2022-09-10 09:10
---

[https://www.iocoder.cn/JUC/sike/Semaphore/](https://www.iocoder.cn/JUC/sike/Semaphore/)

# 1. 简介

信号量 Semaphore 是一个控制访问多个共享资源的计数器，和 CountDownLatch 一样，其本质上是一个“**共享锁**”。

Semaphore，在 API 是这么介绍的：

一个计数信号量。从概念上讲，信号量维护了一个许可集。

如有必要，在许可可用前会阻塞每一个 acquire，然后再获取该许可。

每个 release 添加一个许可，从而可能释放一个正在阻塞的获取者。

但是，不使用实际的许可对象，Semaphore 只对可用许可的号码进行计数，并采取相应的行动。

Semaphore 通常用于限制可以访问某些资源（物理或逻辑的）的线程数目。

下面我们就一个停车场的简单例子来阐述 Semaphore ：

- 为了简单起见我们假设停车场仅有 5 个停车位。一开始停车场没有车辆所有车位全部空着，然后先后到来三辆车，停车场车位够，安排进去停车，然后又来三辆，这个时候由于只有两个停车位，所有只能停两辆，其余一辆必须在外面候着，直到停车场有空车位。当然，以后每来一辆都需要在外面候着。当停车场有车开出去，里面有空位了，则安排一辆车进去（至于是哪辆，要看选择的机制是公平还是非公平）。
- 从程序角度看，停车场就相当于信号量 Semaphore ，其中许可数为 5 ，车辆就相对线程。当来一辆车时，许可数就会减 1 。当停车场没有车位了（许可数 == 0 ），其他来的车辆需要在外面等候着。如果有一辆车开出停车场，许可数 + 1，然后放进来一辆车。
- 信号量 Semaphore 是一个非负整数（ >=1 ）。当一个线程想要访问某个共享资源时，它必须要先获取 Semaphore。当 Semaphore > 0 时，获取该资源并使 Semaphore – 1 。如果S emaphore 值 = 0，则表示全部的共享资源已经被其他线程全部占用，线程必须要等待其他线程释放资源。当线程释放资源时，Semaphore 则 +1 。

# 2. 实现分析

java.util.concurrent.Semaphore 结构如下图：

![](/assets/images/learning/java/concurrencecode/concurrent-source-code-semaphore/cd3ff930253e651fa67708be2dfaf807.jpg)

从上图可以看出，Semaphore 内部包含公平锁（FairSync）和非公平锁（NonfairSync），继承内部类 Sync ，其中 Sync 继承 AQS（再一次阐述 AQS 的重要性）。

Semaphore 提供了两个构造函数：

1. Semaphore(int permits) ：创建具有给定的许可数和**非公平**的公平设置的 Semaphore 。
2. Semaphore(int permits, boolean fair) ：创建具有给定的许可数和给定的公平设置的 Semaphore 。

实现如下：

```java
public Semaphore(int permits) {
  sync = new NonfairSync(permits);
}
public Semaphore(int permits, boolean fair) {
  sync = fair ? new FairSync(permits) : new NonfairSync(permits);
}
```

- Semaphore 默认选择**非公平锁**。
- 当信号量 Semaphore = 1 时，它可以当作互斥锁使用。其中 0、1 就相当于它的状态：1）当 =1 时表示，其他线程可以获取；2）当 =0 时，排他，即其他线程必须要等待。
- 🙂 Semaphore 的代码实现结构，和 ReentrantLock 类似。

## 2.1 信号量获取

Semaphore 提供了 #acquire() 方法，来获取一个许可。

```java
public void acquire() throws InterruptedException {
  sync.acquireSharedInterruptibly(1);
}
```

- 内部调用 AQS 的 #acquireSharedInterruptibly(int arg) 方法，该方法以**共享模式**获取同步状态。代码如下：

```java
public final void acquireSharedInterruptibly(int arg) throws InterruptedException {
  if (Thread.interrupted()) throw new InterruptedException();
  if (tryAcquireShared(arg) < 0) doAcquireSharedInterruptibly(arg);
}
```

在 #acquireSharedInterruptibly(int arg) 方法中，会调用 #tryAcquireShared(int arg) 方法。而 #tryAcquireShared(int arg) 方法，由子类来实现。对于 Semaphore 而言，如果我们选择非公平模式，则调用 NonfairSync 的#tryAcquireShared(int arg) 方法，否则调用 FairSync 的 #tryAcquireShared(int arg) 方法。若 #tryAcquireShared(int arg) 方法返回 < 0 时，则会**阻塞**等待，从而实现 Semaphore 信号量不足时的阻塞，代码如下：

```java
// AQS.java
private void doAcquireSharedInterruptibly(int arg) throws InterruptedException {
  final Node node = addWaiter(Node.SHARED);
  boolean failed = true;
  try {
    for (;;) {
      final Node p = node.predecessor();
      if (p == head) {
        int r = tryAcquireShared(arg);
        if (r >= 0) {
          setHeadAndPropagate(node, r);
          p.next = null;
          // help GC
          failed = false;
          return;
        }
      }
      if (shouldParkAfterFailedAcquire(p, node) && parkAndCheckInterrupt()) {
        throw new InterruptedException();
      }
    }
  } finally {
    if (failed) {
      cancelAcquire(node);
    }
  }
}
```

- 老艿艿：另外，这也是为什么 Semaphore 在使用 AQS 时，state 代表的是，剩余可获取的许可数，而不是已经使用的许可数。我们假设 state 代表的是已经使用的许可数，那么 #tryAcquireShared(int arg) 返回的结果 = 原始许可数 - state ，这个操作在并发情况下，会存在线程不安全的问题。所以，**state 代表的是，剩余可获取的许可数，而不是已经使用的许可数**。

**公平**情况的 FairSync 的方法实现，代码如下：

```java
// FairSync.java
@Override protected int tryAcquireShared(int acquires) {
  for (;;) {
    //判断该线程是否位于CLH队列的列头，从而实现公平锁
    if (hasQueuedPredecessors()) return -1;
    //获取当前的信号量许可
    int available = getState();
    //设置“获得acquires个信号量许可之后，剩余的信号量许可数”
    int remaining = available - acquires;
    //CAS设置信号量
    if (remaining < 0 || compareAndSetState(available, remaining)) return remaining;
  }
}
```

- 通过 #hasQueuedPredecessors() 方法，判断该线程是否位于 CLH 队列的**列头**，从而实现公平锁。

**非公平**情况的 NonfairSync 的方法实现，代码如下：

```java
// NonfairSync.java
protected int tryAcquireShared(int acquires) {
  return nonfairTryAcquireShared(acquires);
}
// Sync.java
final int nonfairTryAcquireShared(int acquires) {
  for (;;) {
    int available = getState();
    int remaining = available - acquires;
    if (remaining < 0 || compareAndSetState(available, remaining)) return remaining;
  }
}
```

- 对于非公平而言，因为它**不需要**判断当前线程是否位于 CLH 同步队列列头，所以相对而言会简单些。

## 2.2 信号量释放

获取了许可，当用完之后就需要释放，Semaphore 提供 #release() 方法，来释放许可。代码如下：

```java
public void release() {
  sync.releaseShared(1);
}
```

- 内部调用 AQS 的 #releaseShared(int arg) 方法，释放同步状态。

```java
// AQS.java
public final boolean releaseShared(int arg) {
  if (tryReleaseShared(arg)) {
    doReleaseShared();
    return true;
  }
  return false;
}
```

```text
- releaseShared(int arg) 方法，会调用 Semaphore 内部类 Sync 的 #tryReleaseShared(int arg) 方法，释放同步状态。
```

```java
// Sync.java
protected final boolean tryReleaseShared(int releases) {
  for (;;) {
    int current = getState();
    //信号量的许可数 = 当前信号许可数 + 待释放的信号许可数
    int next = current + releases;
    if (next < current) {
      throw new Error(“Maximum permit count exceeded”);
    }
    //设置可获取的信号许可数为next
    if (compareAndSetState(current, next)) return true;
  }
}
```

```text
    * 如该方法返回 **true** 时，代表释放同步状态成功，从而在 #releaseShared(int args) 方法中，调用 #doReleaseShared() 方法，**可唤醒阻塞等待 Semaphore 的许可的线程**。
    * 对于信号量的获取释放详细过程，请参考如下博客：
        + [《【死磕 Java 并发】—– J.U.C 之 AQS：同步状态的获取与释放》](http://www.iocoder.cn/JUC/sike/aqs-2)
        + [《【死磕 Java 并发】—– J.U.C 之 AQS：阻塞和唤醒线程》](http://www.iocoder.cn/JUC/sike/aqs-3)
```

## 2.3 其他方法

本文有部分方法并未解析，因为比较简单，胖友可以自己研究。

Semaphore ：

- #acquireUninterruptibly()
- #tryAcquire()
- #tryAcquire(long timeout, TimeUnit unit)
- #acquire(int permits)
- #acquireUninterruptibly(int permits)
- #tryAcquire(int permits)
- #tryAcquire(int permits, long timeout, TimeUnit unit)
- #availablePermits()
- #drainPermits()
- #reducePermits(int reduction)
- #isFair()
- #hasQueuedThreads()
- #getQueueLength()
- #getQueuedThreads()

Sync ：

- #reducePermits(int reductions)
- #drainPermits()

# 3. 应用示例

我们已停车为示例：

```java
public class SemaphoreTest {
  static class Parking {
    private final Semaphore semaphore;

    Parking(int count) {
      semaphore = new Semaphore(count);
    }

    public void park() {
      try {
        semaphore.acquire();
        long time = (long) (Math.random() * 10);
        System.out.println(Thread.currentThread().getName() + “进入停车场，停车” + time + “秒…”);
        Thread.sleep(time * 1000);
        System.out.println(Thread.currentThread().getName() + “开出停车场…”);
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
      } finally {
        semaphore.release();
      }
    }
  }

  static class Car extends Thread {
    private final Parking parking;

    Car(Parking parking) {
      this.parking = parking;
    }

    @Override
    public void run() {
      parking.park();
    }
  }

  public static void main(String[] args) {
    Parking parking = new Parking(3);
    for (int i = 0; i < 5; i++) {
      new Car(parking).start();
    }
  }
}
```

运行结果如下：

![](/assets/images/learning/java/concurrencecode/concurrent-source-code-semaphore/f576e88ac1baa96291f99e2c815c93f4.jpg)
