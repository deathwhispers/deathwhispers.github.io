---
layout: post
title: 装饰模式 (Decorator Pattern) 深度解析
author: deathwhispers
date: 2019-10-31
slug: design-pattern-decorator-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🎁 装饰模式 (Decorator Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：灵活地扩展对象功能

给一个类或对象增加行为，通常有两种主要方式：

1.  **继承机制**：通过继承现有类来添加功能。这是**静态**的，功能在编译时确定，且会随着扩展功能增多导致**子类数量爆炸性增长**。
2.  **关联机制 (装饰模式)**：将一个类的对象**嵌入**另一个对象中（即使用组合/聚合），由外部对象（装饰器）来决定是否调用嵌入对象的行为，从而扩展功能。

<!-- end list -->

* **核心目的**：用**组合 (Composition)** 替代**继承 (Inheritance)** 来实现功能扩展，解决继承的静态性和子类膨胀问题。

> 装饰模式以对客户**透明**的方式动态地给一个对象附加上更多的责任，客户端不会觉得对象在装饰前和装饰后有什么不同。

### 1.2. 模式定义

**装饰模式 (Decorator Pattern)**：

> **动态地给一个对象增加一些额外的职责 (Responsibility)。就增加对象功能来说，装饰模式比生成子类实现更为灵活。**

其别名也称为**包装器 (Wrapper)**，是一种**对象结构型模式**。

## 2\. 模式结构与角色

装饰模式通过组合关系，将新的功能（装饰器）层层包装在原始对象之上。

| 角色名称 | 职责描述 | 对应到实例 |
| :--- | :--- | :--- |
| **Component** (抽象构件) | 定义了原始对象和装饰器对象的**公共接口或抽象类**，可以给这些对象动态增加职责。 | `Shape` 接口 |
| **ConcreteComponent** (具体构件) | **被装饰的原始对象**，实现了抽象构件中声明的方法，是需要被增强的核心对象。 | `Circle`, `Rectangle` |
| **Decorator** (抽象装饰类) | **抽象构件的子类**，用于给具体构件增加职责。它内部必须包含一个**抽象构件对象的引用**（用于组合），并定义了与抽象构件相同的接口。 | `ShapeDecorator` |
| **ConcreteDecorator** (具体装饰类) | 抽象装饰类的子类，**负责向构件添加新的具体职责**（如在调用原方法前/后执行自身的操作）。 | `RedShapeDecorator` |

### 2.1. 模式分析核心

* **透明性**：装饰器和被装饰对象实现相同的接口 (`Component`)，使得客户端对装饰过程无感知，可以对装饰前后的对象一致对待。
* **链式扩展**：装饰器可以相互嵌套，形成一个功能链，实现灵活的、多层次的功能叠加。
* **组合优于继承**：它将功能扩展从**静态的继承**（增加子类）转变为**动态的组合**（增加装饰器对象）。

## 3\. 代码深度解析（形状加边框）

我们以给 `Shape`（形状）对象动态增加 `Red Border`（红色边框）功能为例。

### 3.1. Java 代码示例

```java
// --- 1. 抽象构件 (Component) ---
public interface Shape {
   void draw();
}

// --- 2. 具体构件 (ConcreteComponent) ---
public class Circle implements Shape {
   @Override
   public void draw() {
      System.out.println("Base Shape: Circle");
   }
}

// --- 3. 抽象装饰类 (Decorator) ---
public abstract class ShapeDecorator implements Shape {
   // 组合关系：持有抽象构件的引用
   protected Shape decoratedShape;

   public ShapeDecorator(Shape decoratedShape){
      this.decoratedShape = decoratedShape;
   }

   // 默认实现：委托给被包装的对象
   @Override
   public void draw(){
      decoratedShape.draw();
   }
}

// --- 4. 具体装饰类 (ConcreteDecorator) ---
public class RedShapeDecorator extends ShapeDecorator {

   public RedShapeDecorator(Shape decoratedShape) {
      super(decoratedShape);
   }

   @Override
   public void draw() {
      // 1. 委托给原有构件执行核心功能
      decoratedShape.draw();

      // 2. 增加额外职责
      setRedBorder(decoratedShape);
   }

   private void setRedBorder(Shape decoratedShape){
      System.out.println("Decoration: Border Color set to Red");
   }
}

// --- 5. 客户端调用 (Client) ---
public class DecoratorPatternDemo {
   public static void main(String[] args) {
      // 原始对象
      Shape circle = new Circle();

      // 动态地增加职责：用装饰器包装原始对象
      Shape redCircle = new RedShapeDecorator(circle);

      System.out.println("--- Normal Circle ---");
      circle.draw();

      System.out.println("\n--- Decorated Red Circle ---");
      redCircle.draw(); // 客户端使用一致的接口

      // 链式装饰：可以在外部再套一层，例如：
      Shape doubleDecoratedCircle = new RedShapeDecorator(redCircle);
      System.out.println("\n--- Double Decorated Circle (Red + Red) ---");
      doubleDecoratedCircle.draw();
   }
}
```

### 3.2. Python 代码示例

Python 的装饰器模式常常利用类来实现，或利用语言原生的 `@decorator` 语法糖（虽然底层机制不同，但思想一致）。这里我们使用类实现标准模式。

```python
from abc import ABC, abstractmethod

# --- 1. 抽象构件 (Component) ---
class Coffee(ABC):
    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def get_ingredients(self):
        pass

# --- 2. 具体构件 (ConcreteComponent) ---
class SimpleCoffee(Coffee):
    def get_cost(self):
        return 5.0

    def get_ingredients(self):
        return "Coffee"

# --- 3. 抽象装饰类 (Decorator) ---
class CoffeeDecorator(Coffee):
    def __init__(self, decorated_coffee):
        # 组合：持有被装饰对象的引用
        self._decorated_coffee = decorated_coffee

    # 默认委托给被包装对象
    def get_cost(self):
        return self._decorated_coffee.get_cost()

    def get_ingredients(self):
        return self._decorated_coffee.get_ingredients()

# --- 4. 具体装饰类 A: 牛奶 ---
class MilkDecorator(CoffeeDecorator):
    def get_cost(self):
        return super().get_cost() + 1.5 # 增加成本

    def get_ingredients(self):
        return super().get_ingredients() + ", Milk" # 增加职责

# --- 5. 具体装饰类 B: 糖 ---
class SugarDecorator(CoffeeDecorator):
    def get_cost(self):
        return super().get_cost() + 0.5 # 增加成本

    def get_ingredients(self):
        return super().get_ingredients() + ", Sugar" # 增加职责

# --- 6. 客户端调用 (Client) ---
if __name__ == "__main__":

    # 原始咖啡
    coffee = SimpleCoffee()
    print(f"Base: {coffee.get_ingredients()} | Cost: ${coffee.get_cost()}")

    # 装饰 1: 加牛奶 (MilkDecorator 包装 SimpleCoffee)
    coffee_with_milk = MilkDecorator(coffee)
    print(f"With Milk: {coffee_with_milk.get_ingredients()} | Cost: ${coffee_with_milk.get_cost()}")

    # 装饰 2: 再加糖 (SugarDecorator 包装 MilkDecorator)
    coffee_with_milk_sugar = SugarDecorator(coffee_with_milk)
    print(f"Full: {coffee_with_milk_sugar.get_ingredients()} | Cost: ${coffee_with_milk_sugar.get_cost()}")
```

## 5\. 模式优点与缺点

### 5.1. 优点

1.  **比继承更灵活**：实现了功能扩展的动态性和运行时可配置性，避免了继承体系的僵硬和静态特性。
2.  **符合“开闭原则”**：可以增加新的具体装饰类和具体构件类，而无需修改原有代码。
3.  **可组合性强**：可以通过不同的具体装饰类的排列组合，创造出功能更为强大、行为各异的对象，支持多层装饰。
4.  **对客户端透明**：客户端可以一致地对待被装饰的对象和装饰后的对象。

### 5.2. 缺点

1.  **对象数量增加**：设计时会产生许多小对象（构件和装饰器），增加了系统的复杂度和学习理解难度。
2.  **排错困难**：对于多次装饰的对象，调试时寻找错误可能需要逐级排查，较为繁琐。

## 6\. 适用环境

1.  **在不影响其他对象的情况下，以动态、透明的方式给单个对象添加职责。**
2.  **需要动态地给一个对象增加功能，且这些功能也可以动态地被撤销。**
3.  当不能采用继承的方式对系统进行扩充时（例如，存在大量独立的扩展导致子类爆炸，或基类是 `final` 类）。
