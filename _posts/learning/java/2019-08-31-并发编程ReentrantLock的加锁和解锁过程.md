---
layout: post
title: 并发编程：ReentrantLock的加锁和解锁过程
slug: reentrantlock-lock-unlock-process
type:
  - note
date: 2019-08-31
week: 2025-W48
status: draft
tags:
  - Java8
author: deathwhispers
created: 2019-08-31 14:55
updated: 2019-08-31 14:55
---
# 并发编程：ReentrantLock的加锁和解锁过程

# ReentrantLock

- 和Aqs的关系
- 加锁流程
- 解锁流程

## 1. 和Aqs的关系

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/75e5dafa81d881061d90e7ef8e49eeaf.jpg)

## 2. 加锁流程

第一个线程t1，第一次加锁，没有加锁之前 aqs（NonfairSync）的状态

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/39995750be08e0b4c855027e23f5ab35.jpg)

t1加锁成功后

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/9ae27a9b80c1c4f0c5c8f6da280042c6.jpg)

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/174ea32fa6b44bade62b75d26e413530.jpg)

第二个线程t2尝试加锁，如果加锁成功

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/a333e7c500b8aa21ab1a7bc41502a38f.jpg)

t2加锁失败，会创建队列

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/32c44f850a3d790e01d3c24631e038d9.jpg)

private Node addWaiter(Node mode) { // 1. 创建t2节点 Node node = newNode(Thread.currentThread(), mode); // Try the fast path of enq; backup to full enq on failure // 2. 还不存在队列，故队尾node为null，不进入if Node pred = tail; if (pred != null) { node.prev = pred; if (compareAndSetTail(pred, node)) { pred.next = node; return node; } } // 3. 创建队列 enq(node); return node; } private Node enq(final Node node) { for (; ; ) { // 1. 循环第一次进来，队列不存在，就初始化队列，所以走if Node t = tail; if (t == null) {// Must initialize // 2. 把new出来的node设置为第一个节点，这个node的Thread、prev、next都是null，waitStatus=0 //再把head节点赋给tail节点 if (compareAndSetHead(newNode())) tail = head; } else { // 3. 循环第二次进来，队列存在，走else // t2节点的前一个节点指向第一次进循环new出来的那个node node.prev = t; // 4. 如果队尾是new出来的node，就替换成t2节点 if (compareAndSetTail(t, node)) { // 5.把new出来的节点的next指向t2节点，返回new出来的node，跳出循环 t.next = node; return t; } } } }

t == null队列还没有创建；

compareAndSetHead(new Node())创建一个Thread=null的head；

node.prev = t; t2节点的prev指向head；

t.next = node; head的next节点指向t2；

final boolean acquireQueued(final Node node, int arg) { boolean failed = true; try { boolean interrupted = false; for (; ; ) { // 1. 取出t2节点的上一个节点 final Node p = node.predecessor(); // 2. p是head节点，但是t2重新加锁失败，不会进if if (p == head && tryAcquire(arg)) { setHead(node); p.next = null;// help GC failed = false; return interrupted; } // 3. 修改上一节点的waitStatus && park当前线程 if (shouldParkAfterFailedAcquire(p, node) && parkAndCheckInterrupt()) interrupted = true; } } finally { if (failed) cancelAcquire(node); } }

后加入队列的node会将前一个node的waitStatus置为-1（标记为-1的节点有责任唤醒下一个节点），尾部waitStatus默认值是0。

private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) { //1. 此时t2上一个节点的waitStatus=0 int ws = pred.waitStatus; if (ws == Node.SIGNAL) returntrue; if (ws > 0) { do { node.prev = pred = pred.prev; } while (pred.waitStatus > 0); pred.next = node; } else { //2. 通过cas将t2上一个节点的ws置为-1 compareAndSetWaitStatus(pred, ws, Node.SIGNAL); } returnfalse; }

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/2a844ab407d96bb217113f9ce4efce67.jpg)

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/9bd46bb75cb6c269a4e6fc6726b3fe1f.jpg)

.第三个线程t3尝试加锁，并且t1没有释放锁，t2还在队列中

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/a2a7fa9ac71abd9e1c6734e769ae4d88.jpg)

## 3. 解锁流程

1. 解锁前

![](assets/images/learning/java/2025-11-28-reentrantlock-lock-unlock-process/9bd46bb75cb6c269a4e6fc6726b3fe1f.jpg)

2. 解锁中
- t1解锁，进入tryRealse方法

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/f9888134252cb3ab3e9796a56f888fcc.jpg)

protected final boolean tryRelease(int releases){ //1-1，c=0 int c =getState()- releases; if(Thread.currentThread()!=getExclusiveOwnerThread()) throw new IllegalMonitorStateException(); boolean free =false; if(c ==0){ free =true; // aqs的当前线程变为null setExclusiveOwnerThread(null); } // 当前aqs的state变为0 setState(c); return free; }

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/8509ce97e31797d831c28715f79632e7.jpg)

3.解锁后

头节点存在, 状态为-1, 走unparkSuccessor方法

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/15edc6324e330f08e3213c389d049962.jpg)

private void unparkSuccessor(Node node){ // 1. ws=-1 int ws = node.waitStatus; // 2. 先将第一个节点的ws置为0，防止其他线程使用第一个节点重复唤醒下一个节点（只有ws=-1的节点才有资格唤醒下一个节点） if(ws <0){ compareAndSetWaitStatus(node, ws,0); } Node s = node.next; if(s == null || s.waitStatus >0){ s = null; for(Node t = tail; t != null && t != node; t = t.prev){ if(t.waitStatus <=0){ s = t; } } } //3.第二个节点是t2不等于null，unpark唤醒t2 if(s != null){ LockSupport.unpark(s.thread); } }

- t2被unpark唤醒，代码会走到t2被排队等待的代码，parkAndCheckInterrupt()返回false

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/16579e5a7a3403feb79db7df1e0d5fe4.jpg)

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/304a6dc75b2891183d531b85a127dd9c.jpg)

t2被唤醒，则if判断不成立，代码继续执行，再循环一次

final boolean acquireQueued(final Node node, int arg) { boolean failed = true; try { boolean interrupted = false; for (; ; ) { // 1. 定义t2的前一个节点 final Node p = node.predecessor(); // 2. t2的前一个节点是head，t2重新加锁成功，会进入if if (p == head && tryAcquire(arg)) { // 3. 设置head节点为t2，断开aqs指向旧head的链接；同时将t2节点的thread和prev都设置为null setHead(node); // 4. t2的前一个节点断开指向t2的链接，至此旧head节点所有与外部的引用和被引用全都断开，等待下一次jvm的垃圾回收 p.next = null;// help GC failed = false; // 5. 返回false，跳出循环 return interrupted; } if (shouldParkAfterFailedAcquire(p, node) && parkAndCheckInterrupt()) { interrupted = true; } } } finally { if (failed){ cancelAcquire(node); } } }

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/bd787522e7416dad9a0e25f3bd03e0f2.jpg)

![](/assets/images/learning/java/reentrantlock-lock-unlock-process/af087ff8938cd2689bfb1e2de0ea39e1.jpg)