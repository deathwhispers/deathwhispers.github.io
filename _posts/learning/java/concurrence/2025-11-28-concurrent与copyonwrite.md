---
layout: post
title: concurrent与CopyOnWrite
slug: java-concurrent-copyonwrite
type:
  - note
date: 2025-11-28
week: 2025-W48
status: draft
tags:
  - 分布式事物
categories:
  - Java
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---


# concurrent与CopyOnWrite

## **1.1 ConcurrentHashMap/ConcurrentHashSet**

```plain text
    segment：段

    将一个HashTable分为很多段，每一个小段相当于一个小的HashTable

    最高支持16个段

    设计思想：减小锁粒度

    底层哈希实现的同步 Map(Set)。效率高，线程安全。使用系统底层技术实现线程安全。
```

- * 量级较 synchronized 低。key 和 value 不能为 null。**

```plain text
    key和value都不能为空，当value为null时，会抛出NullPointerException；
   
```

## 1.2 ConcurrentSkipListMap/ConcurrentSkipList

    底层是跳表（SkipList）实现同步（Map/Set），是有序的，效率比ConcurrentHashMap稍低。

![](/assets/images/learning/java/concurrence/java-concurrent-copyonwrite/80c8898bfb074b3431fa5002272706e9.png)

跳表的底层逻辑：

每次存入数据时，都会进行一次比较

```plain text
如： 
第一次插入数据 10
第二次插入数据为 18，此时比较10<18，因此生成一个由10指向18的引用
第三次插入数据为15，此时发现15>10，且15<18, 因此生成一条由10指向15的引用
第四次插入数据为20，发现 20>15,20>18，此时，分别生成一个由15指向20和一个18指向20的引用
第五次插入数据为19，发现 19>15,19>18, 此时，分别生成一个由15指向19和一个18指向19的引用
```

**CopyOnWriteArrayList**

适用场景：读多写少。

如： 黑名单，白名单

当执行写操作时，将原容器copy一份快照，写操作在副本执行，
若此时有读操作并发进行，读操作直接读取原容器，
当写操作执行完后，将指针指向新的容器，并将原容器清空。
