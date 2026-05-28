---
layout: post
title: 策略模式 (Strategy Pattern) 深度解析
author: deathwhispers
date: 2019-08-16
slug: design-pattern-strategy-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🎯 策略模式 (Strategy Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：灵活选择和替换算法

在完成一项任务时，往往可以有多种不同的方法或算法来实现同一功能（如查找、排序、计算等）。

* **问题**：如果将所有算法硬编码在一个类中，并通过 `if...else...` 或 `switch` 语句选择执行，会导致：
    1.  封装算法的类将**十分复杂且难以维护**。
    2.  增加新的算法需要**修改原有类**的源代码，违反“开闭原则”。
    3.  客户端需要理解并选择复杂的条件逻辑。
* **解决方案**：定义独立的类来封装不同的算法，每一个类封装一个具体的算法（策略）。通过将客户端与具体算法解耦，实现算法的灵活选择和替换。

### 1.2. 模式定义

**策略模式 (Strategy Pattern)**：

> **定义一系列算法，将每一个算法封装起来，并让它们可以相互替换。策略模式让算法独立于使用它的客户而变化。**

策略模式属于**对象行为型模式**，也称为**政策模式 (Policy)**。

## 2\. 模式结构与角色

策略模式的核心是**环境类 (Context)** 持有**抽象策略 (Strategy)** 的引用，并委托给具体的策略执行。

| 角色名称 | 职责描述 | 对应到实例 |
| :--- | :--- | :--- |
| **Strategy** (抽象策略类) | 为所支持的算法声明了抽象方法，是所有具体策略类的父类（接口或抽象类），定义了所有算法的公共接口。 | `Strategy` (e.g., 计算接口) |
| **ConcreteStrategy** (具体策略类) | 实现了抽象策略中定义的算法，包含了具体的业务逻辑实现。 | `OperationAdd`, `OperationSubtract` |
| **Context** (环境类) | 维护一个对抽象策略类的引用实例，负责将客户端请求委派给具体的策略对象执行。它不知道具体的策略实现细节。 | `Context` |

### 2.1. 模式分析核心

* **封装算法族**：策略模式将一族相关的算法封装在独立的类中。
* **客户端选择**：应当由**客户端**自己决定在什么情况下使用什么具体策略角色，并通过 Context 注入。
* **解耦**：Context 类针对抽象策略类编程，实现与具体算法的解耦。

## 3\. 代码深度解析（数学运算）

我们以一个简单的数学运算为例，实现加法、减法和乘法三种策略。

### 3.1. Java 代码示例

```java
// --- 1. 抽象策略类 (Strategy) ---
public interface Strategy {
    int execute(int num1, int num2);
}

// --- 2. 具体策略类 A: 加法 ---
public class OperationAdd implements Strategy {
    @Override
    public int execute(int num1, int num2) {
        return num1 + num2;
    }
}

// --- 3. 具体策略类 B: 乘法 ---
public class OperationMultiply implements Strategy {
    @Override
    public int execute(int num1, int num2) {
        return num1 * num2;
    }
}

// --- 4. 环境类 (Context) ---
public class Context {
    private Strategy strategy;

    // 客户端通过构造函数或 Setter 注入策略
    public Context(Strategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    // 算法执行：将请求委托给当前策略对象
    public int executeStrategy(int num1, int num2) {
        System.out.println("Executing strategy: " + strategy.getClass().getSimpleName());
        return strategy.execute(num1, num2);
    }
}

// --- 5. 客户端调用 (Client) ---
public class StrategyPatternDemo {
    public static void main(String[] args) {
        // 客户端选择并注入策略
        Context context = new Context(new OperationAdd());
        int resultAdd = context.executeStrategy(10, 5);
        System.out.println("Result: 10 + 5 = " + resultAdd); // 15

        // 运行时切换策略
        context.setStrategy(new OperationMultiply());
        int resultMultiply = context.executeStrategy(10, 5);
        System.out.println("Result: 10 * 5 = " + resultMultiply); // 50
    }
}
```

### 3.2. Python 代码示例

在 Python 中，策略模式常使用**函数**或**可调用对象**作为策略，简化了类结构。

```python
from abc import ABC, abstractmethod

# --- 1. 抽象策略类 (Strategy) ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# --- 2. 具体策略类 A: 信用卡支付 ---
class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying {amount:.2f} using Credit Card.")

# --- 3. 具体策略类 B: 支付宝支付 ---
class AlipayPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying {amount:.2f} using Alipay.")

# --- 4. 环境类 (Context) ---
class ShoppingCart:
    def __init__(self, payment_strategy: PaymentStrategy):
        self._payment_strategy = payment_strategy
        self.amount = 0.0

    def set_amount(self, amount):
        self.amount = amount

    def checkout(self):
        print(f"Cart total is {self.amount:.2f}")
        # 委托给当前策略对象
        self._payment_strategy.pay(self.amount)

# --- 5. 客户端调用 (Client) ---
if __name__ == "__main__":

    # 客户端选择策略 A
    cart = ShoppingCart(CreditCardPayment())
    cart.set_amount(150.75)
    cart.checkout()

    print("\n--- Switching Strategy ---")

    # 客户端选择策略 B (运行时切换)
    cart._payment_strategy = AlipayPayment()
    cart.set_amount(99.00)
    cart.checkout()
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **完美支持“开闭原则”**：用户可以在不修改原有系统代码的基础上，灵活地增加新的算法或行为。
2.  **避免多重条件转移语句**：使用多态替代了复杂的 `if...else...` 结构，简化了环境类 (Context) 的代码。
3.  **管理相关算法族**：提供了一种结构化的方式来组织和管理一系列相关的算法。
4.  **提高算法安全性**：具体策略类中封装算法和相关的数据结构，提高算法的保密性与安全性。

### 4.2. 缺点

1.  **客户端负担**：客户端必须**知道所有的策略类**，并自行决定使用哪一个策略类，增加了客户端的使用难度和复杂性。
2.  **策略类膨胀**：策略模式将造成产生很多策略类。如果算法过多，系统的类数量会急剧增加。

## 5\. 适用环境

1.  在一个系统里，有许多类，它们之间的**区别仅在于它们的行为/算法**，且这些行为可以互换。
2.  **一个系统需要动态地在几种算法中选择一种**。
3.  如果一个对象有很多行为，且这些行为原本会使用多重条件选择语句来实现。
4.  需要将复杂的、与算法相关的数据结构对客户端隐藏。

## 6\. 策略模式与状态模式的比较

策略模式和状态模式的结构（Context + 抽象接口 + 具体实现）非常相似，但它们的目的和转换逻辑截然不同：

| 特点 | 策略模式 (Strategy) | 状态模式 (State) |
| :--- | :--- | :--- |
| **目的** | 封装**可互换**的算法，实现算法之间的**互换**。 | 封装**状态相关**的行为，实现对象**行为随状态而变**。 |
| **谁来切换** | **客户端**（或配置类）负责选择和注入具体的策略。 | **具体状态类**内部封装了状态转换逻辑，环境类状态自动转换。 |
| **关注点** | 行为的**不同实现方式**（可互换）。 | 对象的**生命周期状态**以及不同状态下的行为差异。 |
| **关系** | **策略类无需关心环境类。** | **状态类需要引用环境类**，以便回调 `setState()` 方法实现状态切换（双向关联）。 |
