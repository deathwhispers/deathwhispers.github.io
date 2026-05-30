---
layout: post
title: ReentrantLock 原理
author: deathwhispers
date: 2021-11-07
slug: concurrent-source-code-reentrantlock
categories:
- Java
tags:
- Java
- Concurrency
type: note
created: 2021-11-07 21:48
updated: 2021-11-07 21:48
---

[https://www.iocoder.cn/JUC/sike/ReentrantLock/](https://www.iocoder.cn/JUC/sike/ReentrantLock/)

# 1. 简介

ReentrantLock，可重入锁，是一种递归无阻塞的同步机制。它可以等同于 synchronized 的使用，但是 ReentrantLock 提供了比 synchronized 更强大、灵活的锁机制，可以减少死锁发生的概率。

API 介绍如下：

一个可重入的互斥锁定 Lock，它具有与使用 synchronized 方法和语句所访问的隐式监视器锁定相同的一些基本行为和语义，但功能更强大。

ReentrantLock 将由最近成功获得锁定，并且还没有释放该锁定的线程所拥有。当锁定没有被另一个线程所拥有时，调用 lock 的线程将成功获取该锁定并返回。如果当前线程已经拥有该锁定，此方法将立即返回。可以使用 #isHeldByCurrentThread() 和 #getHoldCount() 方法来检查此情况是否发生。

ReentrantLock 还提供了公平锁和非公平锁的选择，通过构造方法接受一个可选的 fair 参数（默认非公平锁）：当设置为 true 时，表示公平锁；否则为非公平锁。

公平锁与非公平锁的区别在于，公平锁的锁获取是有顺序的。但是公平锁的效率往往没有非公平锁的效率高，在许多线程访问的情况下，公平锁表现出较低的吞吐量。

ReentrantLock 整体结构如下图：

![](/assets/images/learning/java/concurrencecode/死磕java并发juc之重入锁reentrantlock/d63affa82d13f197547a6253b7c361cb.jpg)

- ReentrantLock 实现 Lock 接口，基于内部的 Sync 实现。
- Sync 实现 AQS ，提供了 FairSync 和 NonFairSync 两种实现。

# 2. Sync 抽象类

Sync 是 ReentrantLock 的内部静态类，实现 AbstractQueuedSynchronizer 抽象类，同步器抽象类。它使用 AQS 的 state 字段，来表示当前锁的持有数量，从而实现可重入的特性。

## 2.1 lock

```java
/**
* Performs {@link Lock#lock}.
* The main reason for subclassing is to allow fast path for nonfair version.
*/
abstract void lock();

```

- 执行锁。抽象了该方法的原因是，允许子类实现快速获得非公平锁的逻辑。

## 2.2 nonfairTryAcquire

#nonfairTryAcquire(int acquires) 方法，非公平锁的方式获得锁。代码如下：

```java
final boolean nonfairTryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    int c = getState();
    if (c == 0) {
        if (compareAndSetState(0, acquires)) {
            setExclusiveOwnerThread(current);
            return true;
        }
    } else if (current == getExclusiveOwnerThread()) {
        int nextc = c + acquires;
        if (nextc < 0) {
            throw new Error(“Maximum lock count exceeded”);
        }
        setState(nextc);
        return true;
    }
    return false;
}



```

- 该方法主要逻辑：首先判断同步状态 state == 0 ?
- 理论来说，这个方法应该在子类 FairSync 中实现，但是为什么会在这里呢？在下文的 ReentrantLock.tryLock() 中，详细解析。

## 2.3 tryRelease

#tryRelease(int releases) 实现方法，释放锁。代码如下：

```java
protected final boolean tryRelease(int releases) {
    int c = getState() - releases;
    if (Thread.currentThread() != getExclusiveOwnerThread()) {
        throw new IllegalMonitorStateException();
    }
    boolean free = false;
    if (c == 0) {
        free = true;
        setExclusiveOwnerThread(null);
    }
    setState(c);
    return free;
}



```

- 通过判断判断是否为获得到锁的线程，保证该方法线程安全。
- 只有当同步状态彻底释放后，该方法才会返回 true 。当 state == 0 时，则将锁持有线程设置为 null ，free= true，表示释放成功。

## 2.4 其他实现方法

其他实现方法比较简单，胖友自己看。

```java
// 是否当前线程独占
@Override protected final boolean isHeldExclusively() {
    // While we must in general read state before owner,
    // we don't need to do so to check if current thread is owner.
    return getExclusiveOwnerThread() == Thread.currentThread();
}
// 新生成条件
final ConditionObject newCondition() {
    return new ConditionObject();
}
// Methods relayed from outer class
final Thread getOwner() {
    return getState() == 0 ? null : getExclusiveOwnerThread();
}
// 获得当前线程持有锁的数量
final int getHoldCount() {
    return isHeldExclusively() ? getState() : 0;
}
// 是否被锁定
final boolean isLocked() {
    return getState() != 0;
}
/**
* Reconstitutes the instance from a stream (that is, deserializes it).
*/
private void readObject(java.io.ObjectInputStream s)
throws java.io.IOException, ClassNotFoundException {
    s.defaultReadObject();
    setState(0);
}



```

- 从这些方法中，我们可以看到，ReentrantLock 是独占获取同步状态的模式。

# 3. Sync 实现类

## 3.1 NonfairSync

NonfairSync 是 ReentrantLock 的内部静态类，实现 Sync 抽象类，非公平锁实现类。

### 3.1.1 lock

#lock() 实现方法，首先基于 AQS state 进行 CAS 操作，将 0 => 1 。若成功，则获取锁成功。若失败，执行 AQS 的正常的同步状态获取逻辑。代码如下：

```java
@Override final void lock() {
    if (compareAndSetState(0, 1)) setExclusiveOwnerThread(Thread.currentThread());
    else acquire(1);
}



```

- 优先基于 AQS state 进行 CAS 操作，已经能体现出非公平锁的特点。因为，此时有可能有 N + 1 个线程正在获得锁，其中 1 个线程已经获得到锁，释放的瞬间，恰好被新的线程抢夺到，而不是排队的 N 个线程。

### 3.1.2 tryAcquire

#tryAcquire(int acquires) 实现方法，非公平的方式，获得同步状态。代码如下：

```java
protected final boolean tryAcquire(int acquires) {
    return nonfairTryAcquire(acquires);
}



```

- 用 #nonfairTryAcquire(int acquires) 方法，非公平锁的方式获得锁。

## 3.2 FairSync

FairSync 是 ReentrantLock 的内部静态类，实现 Sync 抽象类，公平锁实现类。

### 3.2.1 lock

#lock() 实现方法，代码如下：

```java
final void lock() {
    acquire(1);
}



```

- 直接执行 AQS 的正常的同步状态获取逻辑。

### 3.2.2 tryAcquire

#tryAcquire(int acquires) 实现方法，公平的方式，获得同步状态。代码如下：

```java
protected final boolean tryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    int c = getState();
    if (c == 0) {
        if (!hasQueuedPredecessors() &&
        // <1>
        compareAndSetState(0, acquires)) {
            setExclusiveOwnerThread(current);
            return true;
        }
    }
    else if (current == getExclusiveOwnerThread()) {
        int nextc = c + acquires;
        if (nextc < 0) throw new Error(“Maximum lock count exceeded”);
        setState(nextc);
        return true;
    }
    return false;
}



```

比较非公平锁和公平锁获取同步状态的过程，会发现两者唯一的区别就在于，公平锁在获取同步状态时多了一个限制条件 <1> 处的 #hasQueuedPredecessors() 方法，是否有前序节点，即自己不是首个等待获取同步状态的节点。代码如下：

```java
// AbstractQueuedSynchronizer.java
public final boolean hasQueuedPredecessors() {
    Node t = tail;
    //尾节点
    Node h = head;

    //头节点
    Node s;
    //头节点 != 尾节点 //同步队列第一个节点不为null //当前线程是同步队列第一个节点
    return h != t && ((s = h.next) == null || s.thread != Thread.currentThread());
}



```

- 该方法主要做一件事情：主要是判断当前线程是否位于 CLH 同步队列中的第一个。如果是则返回 true ，否则返回 false 。

# 3. Lock 接口

java.util.concurrent.locks.Lock 接口，定义方法如下：

```java
void lock();
void lockInterruptibly() throws InterruptedException;
boolean tryLock();
boolean tryLock(long time, TimeUnit unit) throws InterruptedException;
void unlock();
Condition newCondition();
```

- 每个方法解释如下图：FROM 《Java并发编程的艺术》的 「5.1 Lock 接口」 章节。

![](/assets/images/learning/java/concurrencecode/死磕java并发juc之重入锁reentrantlock/0fa440407492b43e0781b5b014fef158.png)

# 4. ReentrantLock

java.util.concurrent.locks.ReentrantLock ，实现 Lock 接口，重入锁。

ReentrantLock 的实现方法，基本是对 Sync 的调用。

## 4.1 构造方法

```java
public ReentrantLock() {
    sync = new NonfairSync();
}
public ReentrantLock(boolean fair) {
    sync = fair ? new FairSync() : new NonfairSync();
}



```

- 基于 fair 参数，创建 FairSync 还是 NonfairSync 对象。

## 4.2 lock

```java
@Override public void lock() {
    sync.lock();
}



```

## 4.3 lockInterruptibly

```java
@Override public void lockInterruptibly() throws InterruptedException {
    sync.acquireInterruptibly(1);
}



```

**4.4 tryLock**

/** * Acquires the lock only if it is not held by another thread at the time * of invocation. * *

Acquires the lock if it is not held by another thread and * returns immediately with the value {@code true}, setting the * lock hold count to one. Even when this lock has been set to use a * fair ordering policy, a call to {@code tryLock()} *will* * immediately acquire the lock if it is available, whether or not * other threads are currently waiting for the lock. * This "barging" behavior can be useful in certain * circumstances, even though it breaks fairness. If you want to honor * the fairness setting for this lock, then use * {@link #tryLock(long, TimeUnit) tryLock(0, TimeUnit.SECONDS) } * which is almost equivalent (it also detects interruption). * *

If the current thread already holds this lock then the hold * count is incremented by one and the method returns {@code true}. * *

If the lock is held by another thread then this method will return * immediately with the value {@code false}. * * @return {@code true} if the lock was free and was acquired by the * current thread, or the lock was already held by the current * thread; and {@code false} otherwise */ @Override public boolean tryLock() { return sync.nonfairTryAcquire(1); }

- 详细的说明，胖友可以看上面的英文注释。
- 老艿艿的简单理解是：

## 4.5 tryLock

```java
@Override public boolean tryLock(long timeout, TimeUnit unit) throws InterruptedException {
    return sync.tryAcquireNanos(1, unit.toNanos(timeout));
}



```

## 4.6 unlock

```java
@Override public void unlock() {
    sync.release(1);
}



```

## 4.7 newCondition

```java
@Override public Condition newCondition() {
    return sync.newCondition();
}



```

## 4.8 其他实现方法

其他实现方法比较简单，胖友自己看。

```java
public int getHoldCount() {
    return sync.getHoldCount();
}
public boolean isHeldByCurrentThread() {
    return sync.isHeldExclusively();
}
public boolean isLocked() {
    return sync.isLocked();
}
public final boolean isFair() {
    return sync instanceof FairSync;
}
protected Thread getOwner() {
    return sync.getOwner();
}
public final boolean hasQueuedThreads() {
    return sync.hasQueuedThreads();
}
public final boolean hasQueuedThread(Thread thread) {
    return sync.isQueued(thread);
}
public final int getQueueLength() {
    return sync.getQueueLength();
}
protected Collection getQueuedThreads() {
    return sync.getQueuedThreads();
}
public boolean hasWaiters(Condition condition) {
    if (condition == null) throw new NullPointerException();
    if (!(condition instanceof AbstractQueuedSynchronizer.ConditionObject)) throw new IllegalArgumentException(“not owner”);
    return sync.hasWaiters((AbstractQueuedSynchronizer.ConditionObject)condition);
}
public int getWaitQueueLength(Condition condition) {
    if (condition == null) throw new NullPointerException();
    if (!(condition instanceof AbstractQueuedSynchronizer.ConditionObject)) throw new IllegalArgumentException(“not owner”);
    return sync.getWaitQueueLength((AbstractQueuedSynchronizer.ConditionObject)condition);
}
protected Collection getWaitingThreads(Condition condition) {
    if (condition == null) throw new NullPointerException();
    if (!(condition instanceof AbstractQueuedSynchronizer.ConditionObject)) throw new IllegalArgumentException(“not owner”);
    return sync.getWaitingThreads((AbstractQueuedSynchronizer.ConditionObject)condition);
}



```

# 5. ReentrantLock 与 synchronized 的区别

前面提到 ReentrantLock 提供了比 synchronized 更加灵活和强大的锁机制，那么它的灵活和强大之处在哪里呢？他们之间又有什么相异之处呢？

首先他们肯定具有相同的功能和内存语义。

1. 与 synchronized 相比，ReentrantLock提供了更多，更加全面的功能，具备更强的扩展性。例如：时间锁等候，可中断锁等候，锁投票。
2. ReentrantLock 还提供了条件 Condition ，对线程的等待、唤醒操作更加详细和灵活，所以在多个条件变量和高度竞争锁的地方，ReentrantLock 更加适合（以后会阐述Condition）。
3. ReentrantLock 提供了可轮询的锁请求。它会尝试着去获取锁，如果成功则继续，否则可以等到下次运行时处理，而 synchronized 则一旦进入锁请求要么成功要么阻塞，所以相比 synchronized 而言，ReentrantLock会不容易产生死锁些。
4. ReentrantLock 支持更加灵活的同步代码块，但是使用 synchronized 时，只能在同一个 synchronized 块结构中获取和释放。注意，ReentrantLock 的锁释放一定要在 finally 中处理，否则可能会产生严重的后果。
5. ReentrantLock 支持中断处理，且性能较 synchronized 会好些。

# 参考资料

1. Doug Lea：《Java并发编程实战》
2. 方腾飞：《Java并发编程的艺术》的 「5.1 Lock 接口」 和 「5.3 重入锁」 章节
3. 《【JUC】JDK 1.8 源码分析之 ReentrantLock（三）》
