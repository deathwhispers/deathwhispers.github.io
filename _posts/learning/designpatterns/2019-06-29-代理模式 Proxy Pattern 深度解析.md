---
layout: post
title: 代理模式 (Proxy Pattern) 深度解析
author: deathwhispers
date: 2019-06-29
slug: design-pattern-proxy-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🛡️ 代理模式 (Proxy Pattern) 深度解析

## 1\. 模式动机

### 1.1. 模式动机：实现间接引用与控制

在某些情况下，一个客户端不想或者不能直接引用一个目标对象（真实主题）。此时可以通过一个称之为\*\*"代理"\*\*的第三者来实现间接引用。

通过引入代理对象，可以在客户端和目标对象之间起到**中介**的作用，并实现以下目标：

1.  **控制访问**：通过代理对象去掉客户不能看到的内容和服务，或者控制用户对真实对象的使用权限（保护代理）。
2.  **增强功能**：通过代理对象添加客户需要的额外服务（如预处理、日志、缓存）。
3.  **性能优化**：通过小对象（代理）代表大对象（真实对象），减少资源消耗（虚拟代理）。
4.  **处理远程对象**：为远程对象提供一个本地代表（远程代理）。

这种通过引入代理对象来间接访问一个对象的实现机制，即为代理模式的模式动机。

## 2\. 模式定义与结构

### 2.1. 模式定义

**代理模式 (Proxy Pattern)**：

> 给某一个对象提供一个**代理**，并由代理对象**控制对原对象的引用**。

代理模式的英文是 Proxy 或 Surrogate，它是一种**对象结构型模式**。

### 2.2. 模式结构与角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Subject** (抽象主题角色) | 抽象基类或接口，声明了真实主题和代理主题的**共同接口**。客户端针对此接口进行编程。 |
| **RealSubject** (真实主题角色) | 定义了代理角色所代表的**真实对象**，实现了真实的业务操作。 |
| **Proxy** (代理主题角色) | 内部包含对真实主题的**引用**，从而可以在任何时候操作真实主题对象。它负责**控制**对真实主题的访问，并在调用真实主题前后执行额外的服务。 |

### 2.3. 时序图逻辑

1.  **Client** 调用 **Proxy** 的 `request()` 方法。
2.  **Proxy** 执行 `preRequest()` (预处理)。
3.  **Proxy** 调用 **RealSubject** 的 `request()` 方法。
4.  **RealSubject** 执行核心业务。
5.  **Proxy** 执行 `afterRequest()` (后处理)。
6.  结果返回给 **Client**。

## 3\. 代理模式的类型与适用环境

根据代理模式的使用目的，常见的代理模式有多种类型：

| 代理类型 | 目的 / 功能 | 优势 |
| :--- | :--- | :--- |
| **远程 (Remote) 代理** | 为位于不同地址空间的对象提供本地代表（桩）。 | 隐藏网络的细节，客户端无需考虑网络通信。 |
| **虚拟 (Virtual) 代理** | 用一个消耗相对较小的对象代表一个资源消耗较大的对象，真实对象只在需要时才会被创建。 | 减少系统资源消耗，对系统进行优化并提高启动速度。 |
| **保护 (Protection/Access) 代理** | 控制对一个对象的访问，可以给不同的用户提供不同级别的使用权限。 | 控制访问权限，降低系统耦合度。 |
| **缓冲 (Cache) 代理** | 为目标操作的结果提供临时的存储空间。 | 多个客户端可以共享结果，提高性能。 |
| **Copy-on-Write 代理** | 虚拟代理的一种，将昂贵的复制操作延迟到只有客户端真正需要时才执行。 | 节省开销较大的深克隆操作。 |
| **智能引用 (Smart Reference) 代理** | 在对象被引用时，提供一些额外的操作，如计数、加锁等。 | 增加额外的操作（如记录调用次数），增强引用安全性。 |

## 4\. 代码深度解析（多语言实现）

我们以\*\*虚拟代理（Virtual Proxy）\*\*为例，实现大图的延迟加载。

### 4.1. Java 代码示例 (虚拟代理)

`ProxyImage` 延迟加载资源消耗较大的 `RealImage` 对象。

```java
// 1. 抽象主题 (Subject)
public interface Image {
    void display();
}

// 2. 真实主题 (RealSubject)
public class RealImage implements Image {
    private String fileName;

    public RealImage(String fileName){
        this.fileName = fileName;
        loadFromDisk(fileName); // 模拟耗时操作：真正加载大图
    }

    @Override
    public void display() {
        System.out.println("Displaying " + fileName);
    }

    private void loadFromDisk(String fileName){
        System.out.println("Loading " + fileName + " from disk...");
    }
}

// 3. 代理主题 (Proxy)
public class ProxyImage implements Image{
    private RealImage realImage; // 代理持有真实主题的引用
    private String fileName;

    public ProxyImage(String fileName){
        this.fileName = fileName;
        // 注意：构造函数中不加载 RealImage，实现了延迟加载 (Virtual Proxy)
    }

    @Override
    public void display() {
        // 只有在第一次调用 display() 时，才创建并加载 RealImage
        if(realImage == null){
            System.out.println("Proxy: Real image not created yet. Creating now.");
            realImage = new RealImage(fileName);
        }
        realImage.display();
    }
}
```

### 4.2. C++ 代码示例 (预处理与后处理)

原文中的 C++ 代码展示了代理对象在调用真实对象前后添加服务的经典模式。

```cpp
// Proxy.cpp 核心实现 (基于原文逻辑)
#include "Proxy.h"
#include "RealSubject.h"
#include <iostream>
using namespace std;

// 构造函数：代理负责创建真实对象，对用户透明
Proxy::Proxy(){
    m_pRealSubject = new RealSubject();
}

Proxy::~Proxy(){
    delete m_pRealSubject;
}

void Proxy::preRequest(){
    cout << "Proxy::preRequest: [Adding Pre-Check/Security Log]" << endl;
}

void Proxy::afterRequest(){
    cout << "Proxy::afterRequest: [Adding Post-Processing/Statistics]" << endl;
}

void Proxy::request(){
    // 1. 执行预处理
    preRequest();

    // 2. 调用真实对象的核心方法
    m_pRealSubject->request();

    // 3. 执行后处理
    afterRequest();
}
```

### 4.3. Python 代码示例 (保护代理)

此示例实现一个简单的保护代理，控制对敏感方法的访问权限。

```python
# 1. 抽象主题 (Conceptually)
class BankAccount:
    def deposit(self, amount):
        raise NotImplementedError
    def withdraw(self, amount):
        raise NotImplementedError

# 2. 真实主题 (RealSubject)
class RealBankAccount(BankAccount):
    def __init__(self, balance=0):
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount
        print(f"Deposited {amount}. New Balance: {self._balance}")

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            print(f"Withdrew {amount}. New Balance: {self._balance}")
            return True
        print("Withdrawal failed: Insufficient funds.")
        return False

# 3. 代理主题 (Proxy)
class ProtectionProxy(BankAccount):
    def __init__(self, real_account):
        self._real_account = real_account

    # 存钱无需权限
    def deposit(self, amount):
        self._real_account.deposit(amount)

    # 取钱需要特殊权限（或密码验证）
    def withdraw(self, amount, password):
        if password == "SECRET123":
            return self._real_account.withdraw(amount)
        else:
            print("Access Denied: Invalid password for withdrawal.")
            return False

# 客户端调用
real_acc = RealBankAccount(500)
proxy_acc = ProtectionProxy(real_acc)

# 存款 (代理直接委托给真实对象)
proxy_acc.deposit(100)

# 取款 (代理进行控制/权限检查)
proxy_acc.withdraw(50, "WRONGPASS")
proxy_acc.withdraw(150, "SECRET123")
```

## 5\. 模式分析与总结

### 5.1. 优点

1.  **职责分离**：代理模式能够协调调用者和被调用者，在一定程度上降低了系统的耦合度。真实主题只关注核心业务。
2.  **功能增强**：可以在不修改真实主题的情况下，通过代理添加额外的功能和服务。
3.  **系统优化**：远程代理、虚拟代理等可以提升系统性能或隐藏底层复杂性。
4.  **控制访问**：保护代理可以控制对真实对象的使用权限。

### 5.2. 缺点

1.  **性能开销**：由于在客户端和真实主题之间增加了代理对象，有些类型的代理模式可能会造成请求的处理速度变慢。
2.  **实现复杂**：实现某些复杂的代理模式（如远程代理、动态代理）需要额外的工作，且实现可能非常复杂。

### 5.3. 模式扩展：动态代理

* **静态代理**：需要事先为每个真实主题手动编写或生成一个代理类。
* **动态代理**：是一种较为高级的代理模式，它能够在**运行时**自动生成代理类。
* **典型应用**：Java 中的 **Spring AOP (面向切面编程)** 和 **JDK Dynamic Proxy** 都是动态代理的典型应用，它解决了静态代理中类数量急剧增加的问题。

### 5.4. 注意事项

* **与适配器模式的区别**：适配器模式主要目的是**改变接口**，而代理模式**不能改变**所代理类的接口。
* **与装饰器模式的区别**：装饰器模式目的是**增强功能**，而代理模式的目的是**控制访问**。
