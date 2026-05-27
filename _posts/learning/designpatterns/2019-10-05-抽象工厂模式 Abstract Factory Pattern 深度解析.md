---
layout: post
title: 抽象工厂模式 (Abstract Factory Pattern) 深度解析
slug: design-pattern-abstract-factory-pattern
type:
- note
date: 2019-10-05
tags:
- DesignPatterns
categories:
- Learning
- DesignPatterns
author: deathwhispers
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🔩 抽象工厂模式 (Abstract Factory Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：面对多个产品等级结构

在工厂方法模式中，一个具体工厂只负责生产**一个产品等级结构**中的**一种具体产品**。但有时候，一个工厂需要提供**多个产品对象**，这些产品位于**不同的产品等级结构**中，但它们之间是**相关或相互依赖**的。

为了更清晰地理解抽象工厂模式，我们先回顾两个核心概念：

* **产品等级结构 (Product Hierarchy)**：产品的继承结构。例如：`抽象电视机` $\rightarrow$ (`海尔电视机`, `TCL电视机`)。
* **产品族 (Product Family)**：由**同一个工厂**生产的，位于**不同产品等级结构**中的一组相关产品。例如：`海尔工厂`生产的 (`海尔电视机`, `海尔电冰箱`)。

**抽象工厂模式**适用于：当系统所提供的工厂所需生产的具体产品是**多个位于不同产品等级结构中属于不同类型**的具体产品时。它是所有工厂模式中最为抽象和最具一般性的一种形态。

### 1.2. 模式定义

**抽象工厂模式 (Abstract Factory Pattern)**：

> 提供一个**创建一系列相关或相互依赖对象的接口**，而无须指定它们具体的类。

抽象工厂模式又称为 **Kit 模式**，属于**对象创建型模式**。

### 1.3. 区别：工厂方法 vs. 抽象工厂

| 特点 | 工厂方法模式 | 抽象工厂模式 |
| :--- | :--- | :--- |
| **产品数量** | 针对**一个**产品等级结构中的单一产品。 | 针对**多个**产品等级结构中的一组**产品族**。 |
| **抽象度** | 较低。 | 最高，最具一般性。 |
| **工厂方法** | 抽象工厂中通常只有一个 `factoryMethod()`。 | 抽象工厂中通常有多个 `createProductX()` 方法。 |

## 2\. 模式结构与角色

抽象工厂模式的关键在于，一个具体工厂可以创建分属于不同产品等级结构的一个产品族中的所有对象。

### 2.1. 模式角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **AbstractFactory** (抽象工厂) | 声明**生成抽象产品**的方法，用于创建不同等级结构的产品。 |
| **ConcreteFactory** (具体工厂) | 实现了抽象工厂声明的方法，**生成一组具体产品**，这些产品构成了一个**产品族**。 |
| **AbstractProduct** (抽象产品) | 为每种产品等级结构声明接口（例如：`电视机`、`电冰箱`）。 |
| **ConcreteProduct** (具体产品) | 定义具体工厂生产的具体产品对象，实现抽象产品接口（例如：`海尔电视机`）。 |

## 3\. 代码深度解析（多产品族创建）

我们以**跨平台 UI 组件**为例，创建两个产品等级结构：`Button` 和 `TextField`。

* **产品等级结构 1**：`AbstractButton` $\rightarrow$ (`WinButton`, `MacButton`)
* **产品等级结构 2**：`AbstractTextField` $\rightarrow$ (`WinTextField`, `MacTextField`)
* **产品族 1**：`WinFactory` 生产 (`WinButton`, `WinTextField`)
* **产品族 2**：`MacFactory` 生产 (`MacButton`, `MacTextField`)

### 3.1. Java 代码示例

```java
// --- 1. 抽象产品等级结构 ---
// 产品等级结构 A: Button
interface AbstractButton {
    void paint();
}
// 产品等级结构 B: TextField
interface AbstractTextField {
    void display();
}

// --- 2. 具体产品 ---
class WinButton implements AbstractButton {
    @Override public void paint() { System.out.println("Win Button painted."); }
}
class MacButton implements AbstractButton {
    @Override public void paint() { System.out.println("Mac Button painted."); }
}
class WinTextField implements AbstractTextField {
    @Override public void display() { System.out.println("Win TextField displayed."); }
}
class MacTextField implements AbstractTextField {
    @Override public void display() { System.out.println("Mac TextField displayed."); }
}

// --- 3. 抽象工厂 (声明创建产品族的方法) ---
interface AbstractFactory {
    AbstractButton createButton();
    AbstractTextField createTextField();
}

// --- 4. 具体工厂 (创建某一产品族) ---
class WinFactory implements AbstractFactory {
    @Override
    public AbstractButton createButton() { return new WinButton(); }
    @Override
    public AbstractTextField createTextField() { return new WinTextField(); }
}
class MacFactory implements AbstractFactory {
    @Override
    public AbstractButton createButton() { return new MacButton(); }
    @Override
    public AbstractTextField createTextField() { return new MacTextField(); }
}

// --- 5. 客户端 (Client) ---
public class AbstractFactoryDemo {
    public static void main(String[] args) {
        // 客户端只需要切换具体的工厂实例，即可切换整个产品族（界面主题）
        AbstractFactory factory = new WinFactory();
        AbstractButton btn = factory.createButton();
        AbstractTextField txt = factory.createTextField();

        System.out.println("--- Using Windows Theme ---");
        btn.paint();   // Win Button painted.
        txt.display(); // Win TextField displayed.

        factory = new MacFactory(); // 切换产品族
        btn = factory.createButton();
        txt = factory.createTextField();

        System.out.println("\n--- Using macOS Theme ---");
        btn.paint();   // Mac Button painted.
        txt.display(); // Mac TextField displayed.
    }
}
```

## 4\. 模式优点、缺点与扩展

### 4.1. 优点

1.  **保证产品族一致性**：能够保证客户端始终只使用同一个产品族中的对象，产品族中的多个对象被设计成一起工作。
2.  **隔离具体类**：隔离了具体类的生成，客户并不需要知道什么被创建，更换一个具体工厂就变得相对容易。
3.  **增加产品族方便**：增加新的具体工厂和产品族非常方便，无须修改抽象工厂或客户端代码，符合“开闭原则”。

### 4.2. 缺点：开闭原则的倾斜性

抽象工厂模式的最大的缺点在于**增加新的产品等级结构非常困难**。

* **增加产品族**：只需增加新的 `ConcreteFactory`，系统对扩展**开放**。
* **增加产品等级结构**：如果要增加一个新的产品（例如 `Checkbox`）到所有主题中，则需要：
    1.  修改 `AbstractFactory` 接口，增加 `createCheckbox()` 方法。
    2.  修改所有的 `ConcreteFactory` 子类，实现新的 `createCheckbox()` 方法。

这种性质称为\*\*“开闭原则”的倾斜性\*\*：它为新产品族的增加提供方便，但不能为新的产品等级结构的增加提供方便。

### 4.3. 模式扩展与退化

* **工厂模式的退化**：
    * 当抽象工厂模式中每一个具体工厂类只创建一个产品对象（只存在一个产品等级结构）时，抽象工厂模式退化成**工厂方法模式**。
    * 当工厂方法模式退化时（只有一个具体工厂且方法静态），则退化成**简单工厂模式**。

### 4.4. 适用环境

1.  **系统中有多于一个的产品族**，而每次只使用其中某一产品族（如不同皮肤、不同操作系统组件）。
2.  **属于同一个产品族的产品将在一起使用**，这一约束必须在系统的设计中体现出来。
3.  系统不应当依赖于产品类实例如何被创建、组合和表达的细节。
