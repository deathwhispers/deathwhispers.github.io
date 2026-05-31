---
layout: post
title: 单例模式 (Singleton Pattern) 深度解析
author: deathwhispers
date: 2019-02-15
slug: design-pattern-singleton-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🏭 单例模式 (Singleton Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：保证唯一实例与全局访问

对于系统中的某些类来说，**只有一个实例**至关重要，例如：

* 一个系统只能有一个**窗口管理器**、**文件系统**或**ID（序号）生成器**。
* 一个系统可以有多个打印任务，但只能有一个**正在工作的打印任务**。

如果使用全局变量，虽然可以确保对象随时被访问，但不能阻止用户实例化多个对象。

**单例模式**的模式动机在于：让类自身负责保存它的唯一实例，保证没有其他实例被创建，并且提供一个访问该实例的全局方法。

### 1.2. 模式定义

**单例模式 (Singleton Pattern)**：

> **确保某一个类只有一个实例**，而且**自行实例化**并向整个系统**提供这个实例**。这个类称为单例类，它提供全局访问的方法。

**单例模式的要点有三**：

1.  某个类**只能有一个实例**。
2.  它必须**自行创建**这个实例。
3.  它必须**自行向整个系统提供**这个实例。

单例模式是一种**对象创建型模式**，又名单件模式或单态模式。

## 2\. 模式结构与实现要点

### 2.1. 模式结构角色

单例模式只包含一个角色：**单例类 (Singleton)**。

### 2.2. 实现要点

在实现单例模式时，需要注意如下三点：

1.  **私有化构造函数**：确保用户无法通过 `new` 关键字直接实例化它，从而保证实例的唯一性。
2.  **提供自身的静态私有成员变量**：用于存储单例的唯一实例。
3.  **提供一个公有的静态工厂方法（`getInstance()`）**：该方法负责检验实例的存在性并实例化自己，然后存储在静态成员变量中，提供全局访问点。

## 3\. 单例模式的实现方式（Java 核心）

单例模式的实现方式多种多样，主要区别在于**是否支持 Lazy 初始化**（延迟加载）以及**是否支持多线程安全**。

| 实现方式 | Lazy 初始化 | 线程安全 | 性能/描述 | 适用性推荐 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 懒汉式** (不安全) | 是 | 否 | 最基本，多线程下会创建多个实例。 | **不推荐**（非单例） |
| **2. 懒汉式** (加锁) | 是 | 是 | 效率低，99%情况下不需要同步，加锁影响性能。 | **不推荐**（性能差） |
| **3. 饿汉式** | 否 | 是 | 类加载时初始化，无锁，效率高；但非延迟加载，易产生垃圾对象。 | **推荐**（简单高效） |
| **4. 双检锁 (DCL)** | 是 | 是 | 复杂但高效，兼顾 Lazy Loading 和线程安全。**JDK 1.5+ 需加 `volatile`**。 | **推荐**（需要延迟加载时） |
| **5. 静态内部类** | 是 | 是 | 利用 ClassLoader 机制实现延迟加载和线程安全，简洁高效。 | **最佳实践**（推荐） |
| **6. 枚举** | 否 | 是 | 最简洁，自动支持序列化和防止反射攻击。 | **推荐**（最佳方法之一） |

### 3.1. 饿汉式 (Eager Initialization)

在第一次引用该类的时候就创建对象实例，保证了线程安全和执行效率，但无法延迟创建。

```java
public class SingletonEager {
    // 静态成员变量在类加载时即被初始化
    private static SingletonEager instance = new SingletonEager();

    // 私有构造函数
    private SingletonEager () {
    }

    public static SingletonEager getInstance() {
        return instance;
    }
}
```

### 3.2. 懒汉式 - 双重校验锁 (DCL)

兼顾线程安全和效率的写法，实现了延迟加载。

```java
public class SingletonDCL {
    // 必须使用 volatile 关键字，防止指令重排序
    private volatile static SingletonDCL instance;

    private SingletonDCL () {
    }

    public static SingletonDCL getInstance() {
        // 第一次检查：若已创建，则无需进入同步块
        if (instance == null) {
            // 同步块：保证同一时间只有一个线程实例化
            synchronized (SingletonDCL.class) {
                // 第二次检查：在同步块内再次检查，防止多线程竞争时重复创建
                if (instance == null) {
                    instance = new SingletonDCL();
                }
            }
        }
        return instance;
    }
}
// 注意：该方法在 JDK 1.5 之前的版本，即使加了 volatile 也无法完全保证线程安全。
```

### 3.3. 登记式 / 静态内部类 (Singleton Holder)

这种方式是实现延迟加载和线程安全的**推荐方式**，实现简单且高效。

```java
public class SingletonHolder {
    private SingletonHolder() {
    }

    // 静态内部类：只有显式调用 getInstance() 时，才会被虚拟机装载
    private static class SingletonHolderInner {
        private static final SingletonHolder INSTANCE = new SingletonHolder();
    }

    public static final SingletonHolder getInstance() {
        // 利用 ClassLoader 机制保证初始化 INSTANCE 时只有一个线程
        return SingletonHolderInner.INSTANCE;
    }
}
```

### 3.4. 枚举 (Enum)

实现单例模式的**最佳方法**，它更简洁，自动支持序列化机制，绝对防止反射和反序列化攻击。

```java
public enum SingletonEnum {
    INSTANCE;

    public void whateverMethod() {
        // ... 业务方法
    }
}
// 使用方式：SingletonEnum.INSTANCE.whateverMethod();


```

## 4\. C++ 与 Python 实现

### 4.1. C++ 代码示例

C++ 中需要手动管理静态变量的初始化和内存释放。

```c
// Singleton.cpp 核心实现 (基于原文)
#include "Singleton.h"
#include <iostream>

Singleton * Singleton::instance = NULL; // 静态成员变量的定义和初始化

Singleton::Singleton(){} // 私有构造函数

// 析构函数中释放资源 (需要注意 Singleton 类的生命周期管理)
Singleton::~Singleton(){
    delete instance;
}

Singleton* Singleton::getInstance(){
    if (instance == NULL) // 检查实例是否存在
    {
        instance = new Singleton(); // 懒汉式实例化
    }
    return  instance;
}
```

### 4.2. Python 代码示例

Python 中实现单例通常通过**装饰器 (Decorator)** 或修改类的 **`__new__` 方法**。

**使用 `__new__` 方法实现单例**：

```python
class SingletonPython:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # 覆盖默认的 __new__ 方法
        if cls._instance is None:
            # 只有在实例不存在时，才调用父类的 __new__ 来创建实例
            cls._instance = super().__new__(cls)
        return cls._instance

# 客户端调用
s1 = SingletonPython()
s2 = SingletonPython()

print(f"s1 is s2: {s1 is s2}") # 输出: s1 is s2: True (证明是同一个实例)
```

## 5\. 模式分析与总结

### 5.1. 优点

1.  **提供了对唯一实例的受控访问**：可以严格控制客户怎样以及何时访问它。
2.  **节约系统资源**：在系统内存中只存在一个对象，对于需要频繁创建和销毁的对象，可以提高系统性能。
3.  **允许可变数目的实例**：可以基于单例模式进行扩展，使用相似的方法来获得指定个数的多例对象。

### 5.2. 缺点

1.  **扩展困难**：由于单例模式中没有抽象层（接口），单例类的扩展（如创建子类）有很大的困难。
2.  **职责过重**：单例类既充当了工厂角色（提供 `getInstance()`），又充当了产品角色（包含业务方法），在一定程度上**违背了"单一职责原则"**。
3.  **滥用问题**：滥用单例可能导致资源池溢出（如数据库连接池），或在具有垃圾回收的语言中导致对象状态丢失（如果实例被回收）。

### 5.3. 适用环境

* 系统只需要一个实例对象（如序列号生成器、文件系统）。
* 客户调用类的单个实例只允许使用一个公共访问点，不能通过其他途径访问该实例。
* 创建对象需要消耗的资源过多（如访问 I/O 和数据库）。
* 需要定义大量的静态常量和静态方法（如工具类）。
