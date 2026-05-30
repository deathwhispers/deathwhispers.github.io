---
layout: post
title: 模板方法模式 (Template Method Pattern) 深度解析
author: deathwhispers
date: 2019-08-27
slug: design-pattern-template-method-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 模板方法模式 (Template Method Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：封装不变的算法骨架

在面向对象编程中，经常会遇到多个子类拥有**基本相同的方法和逻辑**，只是其中**少数几个步骤的实现细节不同**的情况。

* **问题**：如果每个子类都重复编写这些通用方法，会导致代码冗余，难以维护。
* **解决方案**：将这些公有的方法和算法流程提取到**父类（抽象类）中，形成一个固定的“骨架”，而将那些易变的、特定的步骤延迟**到子类中去实现。

### 1.2. 模式定义

**模板方法模式 (Template Method Pattern)**：

> **定义一个操作中的算法的框架（骨架），而将一些步骤延迟到子类中。**
>
> 使得子类可以**不改变一个算法的结构**即可重定义该算法的某些特定步骤。

它属于**行为型模式**，核心思想是**封装不变部分，扩展可变部分**。

## 2\. 模式结构与角色

模板方法模式通过**继承**实现算法的复用和差异化。

| 角色名称 | 职责描述 |
| :--- | :--- |
| **AbstractClass** (抽象类) | 定义**模板方法**（算法骨架），该方法调用一系列基本方法。它定义并实现了一些基本方法，并声明了抽象方法或钩子方法。 |
| **ConcreteClass** (具体子类) | 实现父类中的**抽象方法**，以完成算法中特定的、可变的步骤。 |
| **Template Method** (模板方法) | 定义在抽象类中，是算法的固定流程，通常使用 `final` 关键字防止被重写。 |
| **Primitive Method** (基本方法) | 算法中的基本步骤，可以是抽象方法（强制子类实现）、具体方法（公共代码）或钩子方法（可选重写）。 |

## 3\. 核心机制：基本方法分类

在抽象类中，用于实现算法骨架的基本方法通常分为三类：

1.  **抽象方法 (Abstract Methods)**：强制子类必须实现的方法，是算法中**最核心的差异点**。
2.  **具体方法 (Concrete Methods)**：已经实现的方法，包含多个子类共有的**公共代码**。
3.  **钩子方法 (Hook Methods)**：在抽象类中给出**空实现或默认实现**的方法。子类可以选择性地重写，从而影响算法的流程（例如控制是否执行某一步骤）。

## 4\. 代码深度解析（游戏流程）

我们以**游戏流程**为例，所有游戏都有 `initialize` $\rightarrow$ `startPlay` $\rightarrow$ `endPlay` 的固定顺序。

### 4.1. Java 代码示例

```java
// --- 1. 抽象类 (AbstractClass) ---
public abstract class Game {

    // 抽象方法：必须由子类实现
    protected abstract void initialize();
    protected abstract void startPlay();
    protected abstract void endPlay();

    // 模板方法：定义算法骨架，使用 final 关键字防止结构被修改
    public final void play(){
        // 1. 初始化游戏
        this.initialize();

        // 2. 开始游戏 (钩子方法示例：可以在这里加入条件判断)
        if (this.shouldStart()) {
            this.startPlay();
        }

        // 3. 结束游戏
        this.endPlay();
    }

    // 钩子方法 (Hook Method)：提供默认实现，子类可选重写
    protected boolean shouldStart() {
        // 默认总是开始
        return true;
    }
}

// --- 2. 具体子类 (ConcreteClass) ---
public class Cricket extends Game {
    @Override
    protected void initialize() {
        System.out.println("Cricket Game Initialized!");
    }
    @Override
    protected void startPlay() {
        System.out.println("Cricket Game Started. (Toss coin, Bat first)");
    }
    @Override
    protected void endPlay() {
        System.out.println("Cricket Game Finished!");
    }
}

public class Football extends Game {
    @Override
    protected void initialize() {
        System.out.println("Football Game Initialized!");
    }
    @Override
    protected void startPlay() {
        System.out.println("Football Game Started. (Kick off)");
    }
    @Override
    protected void endPlay() {
        System.out.println("Football Game Finished!");
    }

    // 重写钩子方法，改变了默认行为
    @Override
    protected boolean shouldStart() {
        System.out.println("Checking weather conditions...");
        return true;
    }
}

// --- 3. 客户端调用 (Client) ---
public class TemplatePatternDemo {
    public static void main(String[] args) {
        Game cricket = new Cricket();
        System.out.println("--- Playing Cricket ---");
        cricket.play();

        System.out.println("\n--- Playing Football ---");
        Game football = new Football();
        football.play();
    }
}



```

### 4.2. Python 代码示例

```python
from abc import ABC, abstractmethod

# --- 1. 抽象类 (AbstractClass) ---
class Game(ABC):
    """定义游戏的抽象流程骨架"""

    # 抽象方法：强制子类实现
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def start_play(self):
        pass

    @abstractmethod
    def end_play(self):
        pass

    # 钩子方法：默认实现
    def hook_log(self):
        print("Standard game log initialized.")

    # 模板方法：定义固定算法骨架
    def play(self):
        self.initialize()
        self.hook_log() # 钩子方法在子类重写前运行默认实现
        self.start_play()
        self.end_play()

# --- 2. 具体子类 (ConcreteClass) ---
class Chess(Game):
    def initialize(self):
        print("Chess game setup: Board ready.")

    def start_play(self):
        print("Chess game started: White moves first.")

    def end_play(self):
        print("Chess game finished: King checked.")

    # 重写钩子方法
    def hook_log(self):
        print("Chess tournament log started.")

# --- 3. 客户端调用 (Client) ---
if __name__ == "__main__":
    chess = Chess()
    print("--- Playing Chess ---")
    chess.play()

# Output:
# --- Playing Chess ---
# Chess game setup: Board ready.
# Chess tournament log started.
# Chess game started: White moves first.
# Chess game finished: King checked.
```

## 5\. 模式优点与缺点

### 5.1. 优点

1.  **封装不变部分**：将算法的不变结构封装在模板方法中，提高了代码复用性和可维护性。
2.  **提取公共代码**：将子类共有的方法提取到父类，便于维护。
3.  **行为由父类控制**：算法的执行顺序由父类严格控制，子类只负责实现细节，实现了**控制反转**（即父类调用子类的方法）。
4.  **符合“开闭原则”**：通过增加新的子类，可以轻松扩展新的实现，而无需修改模板方法。

### 5.2. 缺点

1.  **类数量增加**：每一个不同的实现都需要一个子类来实现，导致类的个数增加，使得系统更加庞大。
2.  **系统抽象度高**：在编写具体子类时，需要充分理解父类模板方法的执行逻辑和抽象方法的约束。

## 6\. 适用环境

1.  **有多个子类共有的方法，且逻辑基本相同**（算法骨架一致）。
2.  **重要的、复杂的算法**，可以将核心的算法设计为模板方法，周边的相关细节功能则由各个子类实现。
3.  **重构时**，模板方法模式是一个经常使用的模式，用于把相同的代码抽取到父类中。

**注意事项**：为防止恶意操作或意外修改，一般模板方法都应加上 `final` 关键词（Java）。
