---
layout: post
title: 享元模式 (Flyweight Pattern) 深度解析
author: deathwhispers
date: 2019-10-03
slug: design-pattern-flyweight-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

没问题，我完全理解了。之前的处理确实在整合时丢失了部分深度，且没有严格遵循“一篇一篇输出”的节奏。

现在，我将严格按照您的要求：**保持原文深度、优化排版结构、增加 Java/Python 代码示例**，为您重新输出**享元模式 (Flyweight Pattern)** 的完整深度解析笔记。

-----

# 🚀 享元模式 (Flyweight Pattern) 深度解析

## 1\. 模式动机与背景

面向对象技术可以很好地解决一些灵活性或可扩展性问题，但在很多情况下需要在系统中增加类和对象的个数。

* **问题场景**：当系统中存在**大量相同或相似的细粒度对象**时，如果为每个实例都创建独立的对象，将导致内存占用极高，运行代价过大，甚至导致性能急剧下降（例如：文档编辑器中的字符对象、游戏中的粒子效果）。
* **解决方案**：**享元模式**通过**共享技术**实现相同或相似对象的重用。
* **核心思想**：
    * **内部状态 (Intrinsic State)**：存储在享元对象内部，**不会随环境改变而改变**，因此可以共享（例如：字符的字体、颜色）。
    * **外部状态 (Extrinsic State)**：**随环境改变而改变**，不可以共享，必须由客户端保存，并在使用时传入享元对象（例如：字符在文档中的位置）。

通过区分这两种状态，我们可以将大量细粒度对象的内部状态剥离出来共享，从而将内存中对象的数量从“百万级”降低到“几十个”。

## 2\. 模式定义

**享元模式 (Flyweight Pattern)**：

> 运用**共享技术**有效地支持**大量细粒度对象的复用**。系统只使用少量的对象，而这些对象都很相似，状态变化很小，可以实现对象的多次复用。

由于享元模式要求能够共享的对象必须是**细粒度对象**，因此它又称为**轻量级模式**，它是一种**对象结构型模式**。

## 3\. 模式结构与角色

享元模式的核心在于**享元工厂**和**享元池**。

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Flyweight** (抽象享元类) | 通常是一个接口或抽象类，声明了具体享元类的公共方法，这些方法可以向外界提供对象的内部状态，同时也可以通过这些方法设置外部状态。 |
| **ConcreteFlyweight** (具体享元类) | 实现了抽象享元接口，为内部状态增加存储空间。**ConcreteFlyweight 对象必须是可共享的**。它所存储的状态必须是内部的，即它不随环境的改变而改变。 |
| **UnsharedConcreteFlyweight** (非共享具体享元类) | 并非所有的抽象享元类的子类都需要被共享。不能被共享的子类通常设计为非共享具体享元类（例如，复合享元模式中的组合对象）。 |
| **FlyweightFactory** (享元工厂类) | 负责创建和管理享元对象。它主要用来确保合理地共享享元，当用户请求一个享元时，工厂提供一个已创建的实例或者创建一个（如果不存在的话）。 |

### 时序图逻辑

1.  Client 请求 FlyweightFactory。
2.  Factory 检查享元池（Pool）。
3.  如果有对应的 Key，直接返回 Pool 中的对象。
4.  如果没有，创建一个新的 ConcreteFlyweight，存入 Pool，然后返回。

## 4\. 代码深度解析（多语言实现）

为了更好地理解“内部状态”和“外部状态”的分离，我们以**绘制圆形**为例。

* **内部状态（共享）**：圆的颜色（Color）。
* **外部状态（不共享）**：圆的坐标（X, Y）和半径（Radius）。

### 4.1. Java 代码示例

```java
import java.util.HashMap;

// 1. 抽象享元类 (Flyweight)
public interface Shape {
    // draw 方法接收外部状态作为参数
    void draw(int x, int y, int radius);
}

// 2. 具体享元类 (ConcreteFlyweight)
public class Circle implements Shape {
    // 内部状态：颜色 (在对象创建后不再改变，可共享)
    private String color;

    public Circle(String color){
        this.color = color;
    }

    @Override
    public void draw(int x, int y, int radius) {
        // 这里的 x, y, radius 是外部状态，由客户端在运行时传入
        System.out.println("Circle: Draw() [Color : " + color
        + ", x : " + x + ", y :" + y + ", radius :" + radius + "]");
    }
}

// 3. 享元工厂类 (FlyweightFactory)
public class ShapeFactory {
    // 享元池：使用 HashMap 存储已创建的 Shape 对象
    private static final HashMap<String, Shape> circleMap = new HashMap<>();

    public static Shape getCircle(String color) {
        // 尝试从缓存池获取
        Circle circle = (Circle)circleMap.get(color);

        if(circle == null) {
            // 如果不存在，则创建新对象并放入池中
            circle = new Circle(color);
            circleMap.put(color, circle);
            System.out.println("Creating circle of color : " + color);
        } else {
            System.out.println("Reusing existing circle of color : " + color);
        }
        return circle;
    }
}

// 4. 客户端调用
public class FlyweightPatternDemo {
    private static final String colors[] =
    {
        "Red", "Green", "Blue";
    }
    ;

    public static void main(String[] args) {
        // 模拟绘制 10 个圆，但实际上只会创建 3 个对象 (Red, Green, Blue)
        for(int i=0; i < 10; ++i) {
            String color = colors[(int)(Math.random()*colors.length)];
            // 获取享元对象
            Circle circle = (Circle)ShapeFactory.getCircle(color);
            // 传入外部状态 (随机坐标)
            circle.draw(getRandomX(), getRandomY(), 100);
        }
    }

    private static int getRandomX()
    {
        return (int)(Math.random()*100 );
    }
    private static int getRandomY()
    {
        return (int)(Math.random()*100);
    }
}



```

### 4.2. Python 代码示例

Python 中利用字典来实现享元池非常直观。

```python
import random

# 1. 抽象享元类 (Conceptually)
class Flyweight:
    def operation(self, extrinsic_state):
        pass

# 2. 具体享元类
class ConcreteFlyweight(Flyweight):
    def __init__(self, intrinsic_state):
        # 内部状态：可共享
        self.intrinsic_state = intrinsic_state

    def operation(self, extrinsic_state):
        # 外部状态：由客户端传入
        print(f"Flyweight [{self.intrinsic_state}] executing with external state: {extrinsic_state}")

# 3. 享元工厂类
class FlyweightFactory:
    _flyweights = {}

    @staticmethod
    def get_flyweight(key):
        if key not in FlyweightFactory._flyweights:
            print(f"--> Creating new Flyweight for key: {key}")
            FlyweightFactory._flyweights[key] = ConcreteFlyweight(key)
        else:
            print(f"--> Reusing existing Flyweight for key: {key}")
        return FlyweightFactory._flyweights[key]

    @staticmethod
    def get_count():
        return len(FlyweightFactory._flyweights)

# 4. 客户端代码
if __name__ == "__main__":
    factory = FlyweightFactory()

    # 模拟请求多个对象
    keys = ["A", "B", "A", "C", "B", "A"]

    for key in keys:
        flyweight = factory.get_flyweight(key)
        # 传入外部状态 (例如随机数)
        flyweight.operation(random.randint(1, 100))

    print(f"\nTotal objects created in memory: {factory.get_count()}")
    # 输出结果将显示实际内存中只有 3 个对象 (A, B, C)
```

### 4.3. C++ 代码逻辑分析 (基于原文)

原文中的 C++ 代码展示了标准的指针管理和 Map 容器使用。

* **`FlyweightFactory`**: 内部维护 `map<string, Flyweight*> m_mpFlyweight`。`getFlyweight(string str)` 方法先查找 iterator，如果 `itr == end()` 则 `new ConcreteFlyweight`，否则直接返回 `itr->second`。
* **`ConcreteFlyweight`**: 构造函数接收 `intrinsicState`。`operation()` 方法执行具体逻辑。
* **内存管理注意**: 在 C++ 中使用享元模式，需要特别注意享元工厂析构时对池中所有对象的内存释放，防止内存泄漏。

## 5\. 模式分析与优缺点

### 5.1. 优点

1.  **极大减少内存中对象的数量**：使得相同对象或相似对象在内存中只保存一份。
2.  **外部状态独立**：外部状态相对独立，而且不会影响其内部状态，从而使得享元对象可以在不同的环境中被共享。

### 5.2. 缺点

1.  **系统复杂度增加**：需要分离出内部状态和外部状态，这使得程序的逻辑复杂化。
2.  **运行时间变长**：为了使对象可以共享，享元模式需要将享元对象的状态外部化，而读取外部状态使得运行时间变长（时间换空间）。
3.  **线程安全问题**：如果多个线程同时修改共享对象的外部状态注入过程，需要注意并发控制（虽然内部状态通常是不可变的）。

## 6\. 适用环境

在以下情况下强烈建议使用享元模式：

* 一个系统有**大量相同或者相似的对象**，由于这类对象的大量使用，造成内存的大量耗费。
* 对象的大部分状态都可以**外部化**，可以将这些外部状态传入对象中。
* 系统**不依赖于这些对象的身份**，这些对象是不可分辨的（即 `obj1 == obj2` 对逻辑无影响）。
* 需要缓冲池的场景。

## 7\. 模式应用实例

1.  **Java String 常量池**：Java 中的字符串如果内容相同，通常指向常量池中的同一个对象。
2.  **文本编辑器**：文档中包含成千上万个字符对象（如 'a', 'b', 'c'），每个字符对象的内部状态（字形、编码）是共享的，而外部状态（位置、大小、颜色）由文档结构维护。
3.  **数据库连接池**：虽然连接池更侧重于复用连接资源（避免频繁握手），但其核心思想也是减少重对象的创建，通过池化技术实现复用，与享元模式有异曲同工之妙。

## 8\. 模式扩展：单纯享元 vs 复合享元

* **单纯享元模式**：
    * 所有的享元对象都是可以共享的。
    * 即所有抽象享元类的子类都可共享，不存在非共享具体享元类。
* **复合享元模式 (Composite Flyweight)**：
    * 将一些单纯享元使用**组合模式 (Composite Pattern)** 加以组合。
    * 形成的**复合享元对象**本身不能共享，但是它们可以分解成单纯享元对象，而后者则可以共享。
    * 例如：一个“单词”对象可以由多个“字母”享元对象组合而成。

-----

**总结**：享元模式是**用时间换空间**的经典模式。它通过复杂的工厂逻辑和状态分离，换取了内存占用的极大降低。在处理大规模细粒度对象的系统中，它是必不可少的优化手段。
