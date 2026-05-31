---
layout: post
title: 外观模式 (Facade Pattern) 深度解析
author: deathwhispers
date: 2019-11-03
slug: design-pattern-facade-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🏛️ 外观模式 (Facade Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：简化复杂子系统的访问

在复杂的软件系统中，通常会划分为多个子系统，每个子系统包含大量的类和复杂的交互逻辑。客户端如果需要调用一项功能，往往需要了解并操作多个子系统中的多个接口。

* **问题**：客户端与子系统内部的复杂性之间存在高度的耦合，导致代码复杂、难以维护和使用。
* **解决方案**：引入一个**外观对象 (Facade)**，它为子系统中的一组接口提供一个**统一、简单的高层界面**。客户端只需与外观对象通信，而无需直接处理子系统内部的复杂细节。

### 1.2. 模式定义

**外观模式 (Facade Pattern)**：

> **外部与一个子系统的通信必须通过一个统一的外观对象进行**，为子系统中的一组接口提供一个一致的界面，外观模式定义了一个高层接口，这个接口使得这一子系统更加容易使用。

外观模式又称为**门面模式**，它是一种**对象结构型模式**。

## 2\. 模式结构与角色

外观模式的目的是降低系统的复杂程度，它体现了**迪米特法则**，即减少类与类之间的相互依赖。

### 2.1. 模式角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Facade** (外观角色) | **客户端直接调用的角色**。它知道子系统中的功能和责任，负责将所有从客户端发来的请求委派到相应的子系统对象去处理。 |
| **SubSystem** (子系统角色) | 实现子系统的功能。它可以是一个单独的类，也可以是一个类的集合。**子系统之间不必知道外观的存在**。 |

### 2.2. 模式分析核心

* **统一入口**：外观模式要求一个子系统的外部与其内部的通信通过一个统一的外观对象进行。
* **客户端简化**：客户端只需要与外观对象打交道，而不需要与子系统内部的很多对象打交道，这极大地提高了客户端使用的便捷性。

## 3\. 代码深度解析（多语言实现）

我们以一个简单的**ShapeMaker**子系统为例，客户端通过**ShapeMaker Facade**来绘制各种图形，而无需直接调用各个图形类。

### 3.1. Java 代码示例

```java
// --- 子系统角色 (SubSystem) ---
public interface Shape {
    void draw();
}

public class Circle implements Shape {
    @Override
    public void draw() {
        System.out.println("SubSystem: Drawing Circle...");
    }
}

public class Rectangle implements Shape {
    @Override
    public void draw() {
        System.out.println("SubSystem: Drawing Rectangle...");
    }
}

// --- 外观角色 (Facade) ---
public class ShapeMaker {
    private Shape circle;
    private Shape rectangle;

    public ShapeMaker() {
        // 外观对象负责实例化子系统组件
        this.circle = new Circle();
        this.rectangle = new Rectangle();
    }

    // 提供统一的简化接口
    public void drawCircle() {
        // 外观对象负责协调子系统内部的调用顺序和逻辑
        circle.draw();
    }

    public void drawRectangle() {
        rectangle.draw();
    }

    // 复杂操作的简化接口：例如，绘制一个组合图形
    public void drawComplexShape() {
        System.out.println("Facade: Starting complex drawing sequence.");
        circle.draw();
        rectangle.draw();
        System.out.println("Facade: Complex drawing complete.");
    }
}

// --- 客户端调用 (Client) ---
public class FacadeDemo {
    public static void main(String[] args) {
        ShapeMaker shapeMaker = new ShapeMaker();

        // 客户端只需要调用外观对象，无需关心 Circle 和 Rectangle 的存在
        shapeMaker.drawCircle();
        shapeMaker.drawComplexShape();

        // 输出结果：
        // SubSystem: Drawing Circle...
        // Facade: Starting complex drawing sequence.
        // SubSystem: Drawing Circle...
        // SubSystem: Drawing Rectangle...
        // Facade: Complex drawing complete.
    }
}
```

### 3.2. Python 代码示例

Python 示例展示一个复杂的**家庭影院启动系统**。

```python
# --- 子系统角色 (SubSystem) ---
class Amplifier:
    def on(self):
        print("Amplifier: ON")
    def set_volume(self, level):
        print(f"Amplifier: Setting volume to {level}")

class DvdPlayer:
    def on(self):
        print("DvdPlayer: ON")
    def play(self, movie):
        print(f"DvdPlayer: Playing '{movie}'")

class Projector:
    def on(self):
        print("Projector: ON")
    def wide_screen_mode(self):
        print("Projector: Wide screen mode activated")

# --- 外观角色 (Facade) ---
class HomeTheaterFacade:
    def __init__(self, amp, dvd, proj):
        # 外观对象持有子系统的引用
        self.amp = amp
        self.dvd = dvd
        self.proj = proj

    # 简化接口：一键启动
    def watch_movie(self, movie):
        print("\n===== GET READY TO WATCH MOVIE =====")
        self.amp.on()
        self.amp.set_volume(5)
        self.proj.on()
        self.proj.wide_screen_mode()
        self.dvd.on()
        self.dvd.play(movie)

    # 简化接口：一键关闭
    def end_movie(self):
        print("\n===== SHUTTING DOWN HOME THEATER =====")
        self.dvd.off() # 假设子系统有 off 方法
        self.proj.off() # 假设子系统有 off 方法
        self.amp.off() # 假设子系统有 off 方法

# --- 客户端调用 (Client) ---
if __name__ == "__main__":
    amp = Amplifier()
    dvd = DvdPlayer()
    proj = Projector()

    # 客户端实例化外观对象
    home_theater = HomeTheaterFacade(amp, dvd, proj)

    # 客户端只需调用一个方法，隐藏了 7 步复杂操作
    home_theater.watch_movie("Inception")
    # home_theater.end_movie()
```

## 4\. 模式优点与扩展

### 4.1. 优点

1.  **降低系统耦合度**：实现了子系统与客户之间的松耦合关系。子系统的组件变化不会影响到调用它的客户类，只需要调整外观类即可。
2.  **简化客户端调用**：对客户屏蔽子系统组件，减少了客户处理的对象数目，使得子系统使用起来更加容易。
3.  **划分层次**：在层次化结构中，可以使用外观模式定义系统中每一层的入口，降低层之间的耦合度。
4.  **提高安全性**：可以限制客户只能通过外观访问子系统功能，提高了对子系统访问的安全性。

### 4.2. 缺点

1.  **不符合开闭原则**：在不引入抽象外观类的情况下，增加新的子系统可能需要修改外观类或客户端的源代码。
2.  **不能很好地限制客户**：外观模式只是提供了一个统一入口，但**并不影响用户直接使用子系统类**。如果需要严格限制客户访问子系统，则需要额外的控制。

### 4.3. 模式扩展与变体

1.  **抽象外观类**：为了解决违背"开闭原则"的问题，可以引入**抽象外观类**。客户端针对抽象外观类编程，新增业务需求时，增加一个新的具体外观类，而不修改原有外观类。
2.  **外观模式与单例模式**：在很多情况下，为了节约系统资源，一般将外观类设计为**单例类**，以确保整个系统中只有一个外观对象。
3.  **多个外观类**：在一个系统中可以设计多个外观类，每个外观类都负责和一些特定的子系统交互，向用户提供相应的业务功能。

### 4.4. 使用场景

* 当要为一个复杂子系统提供一个简单接口时。
* 客户程序与多个子系统之间存在很大的依赖性时，引入外观类进行解耦。
* 在层次化结构中，需要定义系统中每一层的入口，降低层与层之间的耦合度时。
