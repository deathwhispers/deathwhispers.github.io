---
layout: post
title: 桥接模式 (Bridge Pattern) 深度解析
author: deathwhispers
date: 2019-10-08
slug: design-pattern-bridge-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🌉 桥接模式 (Bridge Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：解决多维度变化的类爆炸问题

设想一个系统存在两个独立的变化维度：

1.  **形状 (Abstraction/抽象化)**：如圆形、矩形。
2.  **颜色 (Implementation/实现化)**：如红色、绿色、蓝色。

如果采用传统的**多继承**（方案一：为每种形状提供一套各种颜色的版本），则类的数量会是 $M \times N$ (M种形状 $\times$ N种颜色)。例如，4种形状和3种颜色，需要 $4 \times 3 = 12$ 个类。当增加一个形状或颜色时，需要修改或增加大量类，导致**类爆炸问题**，并且违背了单一职责原则。

**桥接模式**（方案二）通过将这两个维度分离，并使用**组合/关联关系**代替传统的**继承关系**，实现解耦。

### 1.2. 模式定义

**桥接模式 (Bridge Pattern)**：

> **将抽象部分与它的实现部分分离，使它们都可以独立地变化。**

它是一种**对象结构型模式**，又称为**柄体 (Handle and Body) 模式**或**接口 (Interface) 模式**。

### 1.3. 核心概念：脱耦

* **抽象化 (Abstraction)**：忽略一些信息，将对象的共同性质抽取出来形成类的过程。
* **实现化 (Implementation)**：针对抽象化给出的具体实现。
* **脱耦 (Decoupling)**：将抽象化和实现化之间的强关联（继承关系）改换成**弱关联（关联/组合/聚合关系）**，从而使两者可以相对独立地变化。

## 2\. 模式结构与角色

桥接模式通过在抽象类中引用实现类接口，建立抽象与实现之间的桥梁。

### 2.1. 模式角色

| 角色名称 | 职责描述 | 对应到实例 |
| :--- | :--- | :--- |
| **Abstraction** (抽象类) | 定义抽象接口，维护一个 `Implementor` 接口类型的对象，通常通过构造函数注入。 | `Shape` |
| **RefinedAbstraction** (扩充抽象类) | 扩充抽象类定义的接口，实现抽象类中的抽象业务方法。 | `Circle`, `Rectangle` |
| **Implementor** (实现类接口) | 定义实现类的接口，**仅提供基本操作**。 | `DrawAPI` |
| **ConcreteImplementor** (具体实现类) | 实现 `Implementor` 接口，提供基本操作的不同实现。 | `RedCircle`, `GreenCircle` |

### 2.2. 时序分析

客户端调用 `RefinedAbstraction` 的方法，`RefinedAbstraction` 通过其内部持有的 `Implementor` 对象的引用，调用 `Implementor` 的具体操作。

## 3\. 代码深度解析（形状与颜色）

我们以**形状 (Shape)** 和**绘图 API (DrawAPI)** 为例，演示两个独立维度的组合。

### 3.1. Java 代码示例

```java
// --- 1. 实现类接口 (Implementor) ---
// 维度 B：颜色/绘图API
public interface DrawAPI {
    void drawCircle(int radius, int x, int y);
}

// --- 2. 具体实现类 (ConcreteImplementor) ---
public class RedCircle implements DrawAPI {
    @Override
    public void drawCircle(int radius, int x, int y) {;
    System.out.println("Drawing Circle [Color: Red, Radius: " + radius + "]");
}
}
public class GreenCircle implements DrawAPI {
    @Override
    public void drawCircle(int radius, int x, int y) {;
    System.out.println("Drawing Circle [Color: Green, Radius: " + radius + "]");
}
}

// --- 3. 抽象类 (Abstraction) ---
// 维度 A：形状
public abstract class Shape {
    protected DrawAPI drawAPI; // 持有实现部分的引用，建立桥接

    // 通过构造函数注入实现部分
    protected Shape(DrawAPI drawAPI) {;
    this.drawAPI = drawAPI;
}

public abstract void draw();
}

// --- 4. 扩充抽象类 (RefinedAbstraction) ---
public class Circle extends Shape {
    private int x, y, radius;

    public Circle(int x, int y, int radius, DrawAPI drawAPI) {;
    super(drawAPI);
    this.x = x;
    this.y = y;
    this.radius = radius;
}

@Override
public void draw() {;
// 调用实现类的方法完成具体操作
drawAPI.drawCircle(radius, x, y);
}
}

// --- 5. 客户端 (Client) ---
public class BridgePatternDemo {
    public static void main(String[] args) {;
    // 红色圆形：形状(Circle) + 颜色(RedCircle)
    Shape redCircle = new Circle(100, 100, 10, new RedCircle());
    redCircle.draw();

    // 绿色圆形：形状(Circle) + 颜色(GreenCircle)
    Shape greenCircle = new Circle(100, 100, 10, new GreenCircle());
    greenCircle.draw();

    // 假设新增 Rectangle 形状和 BlueCircle 颜色，均不影响现有代码。
}
}


```

### 3.2. Python 代码示例

```python
# --- 1. 实现类接口 (Implementor) ---
class Implementor:
    def operation_imp(self):
        raise NotImplementedError

class ConcreteImplementorA(Implementor):
    def operation_imp(self):
        print("Concrete Implementor A is running.")

class ConcreteImplementorB(Implementor):
    def operation_imp(self):
        print("Concrete Implementor B is running.")

# --- 2. 抽象类 (Abstraction) ---
class Abstraction:
    def __init__(self, implementor: Implementor):
        self._implementor = implementor

    def operation(self):
        # 抽象类的高层操作委托给实现类完成
        self._implementor.operation_imp()

# --- 3. 扩充抽象类 (RefinedAbstraction) ---
class RefinedAbstraction(Abstraction):
    def __init__(self, implementor: Implementor):
        super().__init__(implementor)

    def operation(self):
        print("Refined Abstraction doing something extra...")
        self._implementor.operation_imp() # 委托给实现类

# --- 4. 客户端 (Client) ---
if __name__ == "__main__":
    # 抽象化角色与实现化角色可以独立变化并动态组合
    imp_a = ConcreteImplementorA()
    abs_a = RefinedAbstraction(imp_a)
    abs_a.operation()

    imp_b = ConcreteImplementorB()
    abs_b = RefinedAbstraction(imp_b)
    abs_b.operation()
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **分离抽象与实现**：将抽象接口及其实现部分分离，使得两者可以独立扩展，降低了耦合度。
2.  **优秀的扩展性**：在两个变化维度中**任意扩展一个维度**（增加形状或增加颜色），都**不需要修改原有系统**，符合“开闭原则”。
3.  **避免多继承**：是解决多维度变化导致的类爆炸问题的更好方法，比多继承方案复用性高，且类数量少。
4.  **隐藏实现细节**：实现细节对客户透明，可以对用户隐藏底层实现。

### 4.2. 缺点

1.  **增加设计难度**：桥接模式的引入会增加系统的理解与设计难度，要求开发者能够正确识别出系统中**两个独立变化的维度**。
2.  **局限性**：其使用范围具有一定的局限性，只有当存在两个或多个独立变化的维度时才适用。

## 5\. 适用环境

1.  **存在两个独立变化的维度**，且这两个维度都需要进行扩展。
2.  需要对抽象化角色和实现化角色进行**动态耦合**（程序运行时组合）。
3.  不希望使用继承或因为多层次继承导致系统类的个数急剧增加的系统。
4.  需要在构件的抽象化角色和具体化角色之间增加更多的灵活性，避免静态的继承联系。

## 6\. 模式应用与扩展

* **模式应用**：Java AWT 中的 Peer 架构就是使用了桥接模式。AWT 中的每一个 GUI 构件（抽象化）都对应一个 Peer 构件（实现化），Peer 构件根据不同的操作系统（不同实现）提供不同的视感。
* **与适配器模式的联用**：桥接模式用于**初步设计**，将两个独立变化的维度分离。适配器模式用于**设计完成之后**，当发现系统与已有类无法协同工作时，用于解决接口不兼容问题。
