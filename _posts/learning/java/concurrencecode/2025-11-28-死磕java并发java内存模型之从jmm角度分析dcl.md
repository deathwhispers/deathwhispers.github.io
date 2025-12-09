---
layout: post
title: 死磕Java并发：Java内存模型之从JMM角度分析DCL
slug: concurrent-source-code-dcl
type:
  - note
date: 2025-11-28
week: 2025-W48
status: draft
tags:
  - Java并发源码分析
categories:
  - Java
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---
# 1. 问题分析

我们先看单例模式里面的**懒汉式**：

我们都知道这种写法是**错误的**，因为**它无法保证线程的安全性**。优化如下：

优化非常简单，就是在#getInstance()方法上面做了**同步**，但是synchronized就会导致这个方法比较低效，导致程序性能下降，那么怎么解决呢？聪明的人们想到了双重检查 DCL：

就如上面所示，这个代码看起来很完美，理由如下：

如果检查第一个singleton不为 null ，则不需要执行下面的加锁动作，极大提高了程序的性能。

如果第一个singleton为 null ，即使有多个线程同一时间判断，但是由于synchronized的存在，只会有一个线程能够创建对象。

当第一个获取锁的线程创建完成后singleton对象后，其他的在第二次判断singleton一定不会为 null ，则直接返回已经创建好的singleton对象。

通过上面的分析，DCL 看起确实是非常完美，但是可以明确地告诉你，这个**错误的**。上面的逻辑确实是没有问题，分析也对，但是就是有问题，那么问题出在哪里呢？在回答这个问题之前，我们先来复习一下创建对象过程，实例化一个对象要分为三个步骤：

但是由于**重排序**的原因，步骤 2、3 可能会发生重排序，其过程如下：

如果 2、3 发生了重排序，就会导致第二个判断会出错，singleton != null，但是它其实仅仅只是一个地址而已，此时对象还没有被初始化，所以return的singleton对象是一个没有被初始化的对象，如下：

![](/assets/images/learning/java/concurrencecode/concurrent-source-code-dcl/d7d208870993dec9a9bd9c313e807b0b.jpg)

按照上面图例所示，线程 B 访问的是一个没有被初始化的singleton对象。

通过上面的阐述，我们可以判断 DCL 的错误根源在于**步骤 4**：

知道问题根源所在，那么怎么解决呢？有两个解决办法：

不允许初始化阶段步骤 2、3 发生重排序。

允许初始化阶段步骤 2、3 发生重排序，但是不允许其他线程“看到”这个重排序。

# 2. 解决方案

解决方案依据上面两个解决办法即可。

## **2.1 基于 volatile 解决方案**

对于上面的DCL其实只需要做一点点修改即可：将变量singleton生命为volatile即可：

当singleton声明为volatile后，步骤 2、3 就不会被重排序了，也就可以解决上面那问题了。

## **2.2 基于类初始化的解决方案**

该解决方案的根本就在于：**利用 ClassLoder 的机制，保证初始化 instance 时只有一个线程。JVM 在类初始化阶段会获取一个锁，这个锁可以同步多个线程对同一个类的初始化**。

这种解决方案的实质是：运行步骤 2 和步骤 3 重排序，但是不允许其他线程看见。

*Java 语言规定，对于每一个类或者接口 C ，都有一个唯一的初始化锁 LC 与之相对应。从C 到 LC 的映射，由 JVM 的具体实现去自由实现。JVM 在类初始化阶段期间会获取这个初始化锁，并且每一个线程至少获取一次锁来确保这个类已经被初始化过了。*

![](/assets/images/learning/java/concurrencecode/concurrent-source-code-dcl/aa0739ad8dd3d11aa179b5b04c9dbfc9.jpg)

*老艿艿：因为****基于类初始化的解决方案****，涉及到类加载机制，本文就不拓展开来，感兴趣的胖友，可以看看*[《双重检查锁定与延迟初始化》](http://www.infoq.com/cn/articles/double-checked-locking-with-delay-initialization#%E5%9F%BA%E4%BA%8E%E7%B1%BB%E5%88%9D%E5%A7%8B%E5%8C%96%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88)*的*[「基于类初始化的解决方案」](https://www.iocoder.cn/JUC/sike/jmm-3-dcl/#)*小节。*

# 3. 总结

*延迟初始化降低了初始化类或创建实例的开销，但增加了访问被延迟初始化的字段的开销。****在大多数时候，正常的初始化要优于延迟初始化****。*

*如果确实需要对****实例字段****使用线程安全的延迟初始化，请使用上面介绍的基于****volatile****的延迟初始化的方案。*

*如果确实需要对****静态字段****使用线程安全的延迟初始化，请使用上面介绍的基于类初始化的方案。*

```java
public class Singleton {
    private static Singleton singleton;
    private Singleton() {}

    public static Singleton getInstance() {
        if (singleton == null) {
            singleton = new Singleton();
        }
        return singleton;
    }
}
```

```java
public class Singleton {
    private static Singleton singleton;
    private Singleton() {}

    public static synchronized Singleton getInstance() {
        if (singleton == null) {
            singleton = new Singleton();
        }
        return singleton;
    }
}
```

```java
public class Singleton {
    private static Singleton singleton;
    private Singleton() {}
    public static Singleton getInstance() {
        if(singleton == null) { // 1
            synchronized (Singleton.class) { // 2
                if(singleton == null) { // 3
                    singleton = new Singleton(); // 4
                }
            }
        }
        return singleton;
    }
}
```

```java
memory = allocate(); //1：分配内存空间
ctorInstance(memory); //2：初始化对象
instance = memory; //3：将内存空间的地址赋值给对应的引用
```

```java
memory = allocate(); // 1：分配内存空间
instance = memory; // 3：将内存空间的地址赋值给对应的引用
// 注意，此时对象还没有被初始化！
ctorInstance(memory); // 2：初始化对象
```

```java
singleton = new Singleton();
```

```java
public class Singleton {
    // 通过volatile关键字来确保安全
    private volatile static Singleton singleton;
    private Singleton() {} public static Singleton getInstance() {
        if(singleton == null) {
            synchronized (Singleton.class) {
                if(singleton == null) {
                    singleton = new Singleton();
                }
            }
        }
        return singleton;
    }
}
```

```java
public class Singleton {

    private static class SingletonHolder {
        public static Singleton singleton = new Singleton();
    }

    public static Singleton getInstance() {
        return SingletonHolder.singleton;
    }
}
```
