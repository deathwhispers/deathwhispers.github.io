---
layout: post
title: 观察者模式 (Observer Pattern) 深度解析
slug: observer-pattern
type:
- note
date: 2019-11-18
tags:
- DesignPatterns
categories:
- Learning
- DesignPatterns
author: deathwhispers
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 📢 观察者模式 (Observer Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：建立松耦合的一对多依赖

在软件系统中，经常需要建立一种对象与对象之间的依赖关系：当一个对象（**观察目标/Subject**）发生改变时，需要自动通知其他一个或多个对象（**观察者/Observer**），并让它们做出相应的反应。

* **核心需求**：
    * **低耦合**：观察目标不应该知道具体有多少个观察者，也不应该知道它们的具体类型。
    * **动态增删**：可以根据需要随时增加或删除观察者，系统易于扩展。
* **解决方案**：观察者模式将这种依赖关系抽象化。目标对象维护一个观察者列表，并在状态改变时遍历列表，通知所有观察者。

### 1.2. 模式定义

**观察者模式 (Observer Pattern)**：

> **定义对象间的一种一对多依赖关系，使得每当一个对象状态发生改变时，其相关依赖对象皆得到通知并被自动更新。**

观察者模式是一种**对象行为型模式**，其别名众多，包括：

* 发布-订阅（Publish/Subscribe）模式
* 模型-视图（Model/View）模式（MVC模式的核心）
* 源-监听器（Source/Listener）模式

## 2\. 模式结构与角色

观察者模式通过将通知机制抽象化，实现了目标与观察者的解耦。

| 角色名称 | 职责描述 | 对应到股票交易实例 |
| :--- | :--- | :--- |
| **Subject** (目标/主题) | 定义了管理观察者的方法（`attach`, `detach`）和通知观察者的方法（`notify`）。它维护了一个抽象观察者列表。 | `Stock` (抽象股票) |
| **ConcreteSubject** (具体目标) | 存储与其状态相关的具体数据。当状态发生改变时，调用父类的 `notify` 方法通知所有注册的观察者。 | `SpecificStock` (具体股票) |
| **Observer** (抽象观察者) | 定义一个更新接口 (`update`)，以便在接收到目标通知时更新自己。 | `Trader` (抽象交易员) |
| **ConcreteObserver** (具体观察者) | 实现抽象观察者的更新接口，根据具体目标的状态变化执行相应的业务逻辑。 | `BinaryTrader`, `OctalTrader` |

### 2.1. 模式分析核心

* **抽象耦合**：目标和观察者都依赖于抽象接口，而不是具体实现，实现了两者之间的松耦合。
* **广播通信**：目标对象无需知道观察者的细节，可以向所有注册的观察者发送广播通知。
* **更新机制**：当目标状态改变时，它调用 `notify()`，然后遍历观察者列表，依次调用每个观察者的 `update()` 方法。

## 3\. 代码深度解析（状态更新与同步）

我们以一个简单的**状态同步系统**为例，目标状态改变时，观察者以不同格式（二进制、八进制）显示该状态。

### 3.1. Java 代码示例

```java
import java.util.ArrayList;
import java.util.List;

// --- 1. 抽象观察者 (Observer) ---
public abstract class Observer {
    protected Subject subject;
    // 抽象更新方法，通常包含对 Subject 的引用以获取最新状态
    public abstract void update();
}

// --- 2. 具体目标 (ConcreteSubject) ---
public class Subject {
    private List<Observer> observers = new ArrayList<>();
    private int state;

    public int getState() {
        return state;
    }

    // 状态改变时，通知所有观察者
    public void setState(int state) {
        System.out.println("\nSubject: State changed from " + this.state + " to " + state);
        this.state = state;
        notifyAllObservers();
    }

    public void attach(Observer observer) {
        observers.add(observer);
        // 通常在 attach 时执行一次初始化更新
        observer.update();
    }

    public void detach(Observer observer) {
        observers.remove(observer);
    }

    public void notifyAllObservers() {
        for (Observer observer : observers) {
            observer.update();
        }
    }
}

// --- 3. 具体观察者 A: 二进制观察者 ---
public class BinaryObserver extends Observer {
    public BinaryObserver(Subject subject) {
        this.subject = subject;
        this.subject.attach(this);
    }

    @Override
    public void update() {
        System.out.println("Binary Observer: " + Integer.toBinaryString(subject.getState()));
    }
}

// --- 4. 具体观察者 B: 十六进制观察者 ---
public class HexaObserver extends Observer {
    public HexaObserver(Subject subject) {
        this.subject = subject;
        this.subject.attach(this);
    }

    @Override
    public void update() {
        System.out.println("Hexa Observer: " + Integer.toHexString(subject.getState()).toUpperCase());
    }
}

// --- 5. 客户端调用 (Client) ---
public class ObserverPatternDemo {
    public static void main(String[] args) {
        Subject subject = new Subject();

        // 注册观察者
        new BinaryObserver(subject);
        new HexaObserver(subject);

        // 第一次状态改变
        subject.setState(15);

        // 第二次状态改变
        subject.setState(10);
    }
}
```

### 3.2. Python 代码示例 (使用抽象基类实现标准模式)

```python
from abc import ABC, abstractmethod

# --- 1. 抽象观察者 (Observer) ---
class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

# --- 2. 具体目标 (ConcreteSubject) ---
class ConcreteSubject:
    def __init__(self):
        self._observers = []
        self._state = 0

    def attach(self, observer):
        print(f"[Subject] Attached {observer.__class__.__name__}")
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)
        print(f"[Subject] Detached {observer.__class__.__name__}")

    def set_state(self, new_state):
        print(f"\n[Subject] Setting state to: {new_state}")
        self._state = new_state
        self.notify()

    def get_state(self):
        return self._state

    def notify(self):
        for observer in self._observers:
            observer.update(self)

# --- 3. 具体观察者 A: 终端日志 ---
class ConsoleLogger(Observer):
    def update(self, subject: ConcreteSubject):
        current_state = subject.get_state()
        print(f"Logger: State updated to {current_state}")

# --- 4. 具体观察者 B: 数据库同步 ---
class DBSyncer(Observer):
    def update(self, subject: ConcreteSubject):
        current_state = subject.get_state()
        print(f"DBSyncer: Persisting state {current_state} to DB...")
        # 实际业务逻辑：执行数据库写入等操作

# --- 5. 客户端调用 (Client) ---
if __name__ == "__main__":

    publisher = ConcreteSubject()

    # 创建并注册观察者
    logger = ConsoleLogger()
    syncer = DBSyncer()

    publisher.attach(logger)
    publisher.attach(syncer)

    # 状态改变，自动触发通知
    publisher.set_state(42)

    # 移除一个观察者
    publisher.detach(logger)

    # 状态再次改变，只有剩下的观察者收到通知
    publisher.set_state(100)
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **松耦合**：目标和观察者之间是抽象耦合，它们可以独立变化和复用。目标不知道观察者的具体类型，只知道它们实现了 `update` 接口。
2.  **支持广播通信**：目标状态改变时，所有已注册的观察者都能得到通知。
3.  **符合“开闭原则”**：增加新的观察者或目标子类，无需修改原有目标或观察者的代码。
4.  **动态可配置**：可以根据需要动态地增加或删除观察者。

### 4.2. 缺点

1.  **通知耗时**：如果观察者数量庞大，通知所有观察者可能会花费较长时间，影响响应速度。
2.  **循环依赖**：如果在观察者和观察目标之间存在复杂的循环依赖，可能导致循环调用，造成系统崩溃。
3.  **信息有限**：观察者通常只知道目标发生了变化，但没有机制让观察者知道**目标具体是如何发生变化**的（例如变化前后的值对比）。

## 5\. 适用环境

1.  **一个对象的改变将导致其他一个或多个对象也发生改变**，且不知道具体有多少对象将发生改变，需要降低对象之间的耦合度。
2.  **一个对象必须通知其他对象，而并不知道这些对象是谁**（实现高度的解耦）。
3.  **需要实现表示层和数据逻辑层的分离**，例如 MVC 模式中 Model 对 View 的通知。
4.  需要在系统中创建一个**触发链**（A 影响 B，B 影响 C），建立一种链式触发机制。
