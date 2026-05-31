---
layout: post
title: 建造者模式 (Builder Pattern) 深度解析
author: deathwhispers
date: 2019-11-30
slug: design-pattern-builder-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🏗️ 建造者模式 (Builder Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：分离复杂对象的构建与表示

在现实世界和软件系统中，存在许多**复杂的对象**，它们由多个组成部分构成（例如一辆汽车包含车轮、发动机、方向盘等）。

* **问题**：对于大多数用户而言，他们只需要一个**完整的对象**（一辆汽车），而**不需要知道这些部件的装配细节**，也不能随意更改组装顺序，因为某些属性的赋值可能相互依赖。
* **解决方案**：将复杂对象的**部件**和**组装过程**分开，将部件的组合过程"外部化"到一个称作**建造者 (Builder)** 的对象里。用户只需指定对象类型，即可一步一步构建完整的对象。

**建造者模式**正是为了解决这种复杂对象的创建和装配逻辑问题。

### 1.2. 模式定义

**建造者模式 (Builder Pattern)**：

> **将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。**

建造者模式允许用户只通过指定复杂对象的类型和内容就可以构建它们，用户不需要知道内部的具体构建细节。它属于**对象创建型模式**。根据中文翻译的不同，建造者模式又可以称为**生成器模式**。

## 2\. 模式结构与角色

建造者模式的核心是将产品的构建过程封装在 `Director` 中，并利用多态性实现不同产品的构建。

### 2.1. 模式角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Product** (产品角色) | 被构建的复杂对象，包含多个组成部件。 |
| **Builder** (抽象建造者) | 为创建产品对象的**各个部件指定抽象接口**，并提供一个方法返回创建好的复杂产品对象 (`getResult()`)。 |
| **ConcreteBuilder** (具体建造者) | 实现抽象建造者接口，实现各个部件的**构造和装配方法**，定义并明确它所创建的复杂对象。 |
| **Director** (指挥者) | **负责安排复杂对象的建造次序**。它针对抽象建造者编程，隔离了客户与生产过程，控制产品的生成过程。 |

### 2.2. 模式分析核心

* **解耦构建与表示**：同样的构建过程（例如指挥者中的 `construct()` 方法）可以创建出不同的表示（不同的具体建造者返回不同的产品对象）。
* **隔离装配过程**：`Director` 类是关键，它封装了产品对象的组装顺序和细节，客户端只需要知道具体的 `ConcreteBuilder` 类型，即可通过 `Director` 获得一个完整的对象。

## 3\. 代码深度解析（KFC 套餐）

我们以 **KFC 套餐**为例。套餐 (`Meal`) 是复杂对象，包含 `Burger` 和 `ColdDrink` 等部件。`MealBuilder` 负责具体的装配。

### 3.1. Java 代码示例（简化 GoF 结构）

在这个例子中，`MealBuilder` 充当了 Builder 和 Director 的双重角色（简化结构）。

```java
// --- 1. 产品角色 (Product) ---
import java.util.ArrayList;
import java.util.List;

class Meal {
    private List<String> parts = new ArrayList<>();

    public void addPart(String part) {
        parts.add(part);
    }
    public void show() {
        System.out.println("--- Meal Constructed ---");
        for (String part : parts) {
            System.out.println(part);
        }
    }
}

// --- 2. 抽象建造者 (Builder) ---
abstract class MealBuilder {
    protected Meal meal = new Meal();

    public abstract void buildBurger();
    public abstract void buildDrink();

    // 返回结果的方法
    public Meal getMeal() {
        return meal;
    }
}

// --- 3. 具体建造者 (ConcreteBuilder) ---
class VegMealBuilder extends MealBuilder {
    @Override
    public void buildBurger()
    {
        meal.addPart("Veg Burger");
    }
    @Override
    public void buildDrink() {
        meal.addPart("Coke");
    }
}

class NonVegMealBuilder extends MealBuilder {
    @Override
    public void buildBurger()
    {
        meal.addPart("Chicken Burger");
    }
    @Override
    public void buildDrink()
    {
        meal.addPart("Pepsi");
    }
}

// --- 4. 指挥者 (Director) ---
class Director {
    private MealBuilder builder;

    public void setBuilder(MealBuilder builder) {
        this.builder = builder;
    }

    // 负责控制产品的生成次序 (不变的构建过程)
    public Meal construct() {
        // 装配顺序：先装汉堡，再装饮料
        builder.buildBurger();
        builder.buildDrink();
        return builder.getMeal();
    }
}

// --- 5. 客户端调用 (Client) ---
public class BuilderPatternDemo {
    public static void main(String[] args) {
        Director director = new Director();

        // 建造者 1: 素食套餐
        MealBuilder vegBuilder = new VegMealBuilder();
        director.setBuilder(vegBuilder);
        Meal vegMeal = director.construct();
        vegMeal.show();

        // 建造者 2: 非素食套餐
        MealBuilder nonVegBuilder = new NonVegMealBuilder();
        director.setBuilder(nonVegBuilder);
        Meal nonVegMeal = director.construct();
        nonVegMeal.show();
    }
}
```

### 3.2. Python 代码示例（链式调用 - 流畅接口）

在 Python 和 Java 中，建造者模式常常被简化，通过**链式调用 (Fluent Interface)** 来代替 `Director` 类，这也是 `StringBuilder` 等类采用的方式。

```python
# --- 1. 产品角色 (Product) ---
class Car:
    def __init__(self):
        self.parts = []
    def add(self, part):
        self.parts.append(part)
    def show(self):
        print(f"Car construction complete. Parts: {', '.join(self.parts)}")

# --- 2. 建造者 (Builder) - 扮演指挥者角色 ---
class CarBuilder:
    def __init__(self):
        self.car = Car()

    # 构建部件的方法，并返回自身 (链式调用)
    def build_engine(self, type="Standard"):
        self.car.add(f"{type} Engine")
        return self

    def build_wheels(self, count=4):
        self.car.add(f"{count} Wheels")
        return self

    def build_frame(self, color="Black"):
        self.car.add(f"{color} Frame")
        return self

    # 结果获取方法
    def get_result(self):
        return self.car

# --- 3. 客户端调用 (Client) ---
if __name__ == "__main__":
    builder = CarBuilder()

    # 构建产品 1: 经济型轿车 (使用链式调用定义构建过程)
    economy_car = builder.build_frame("Grey").build_wheels(4).build_engine("Economy").get_result()
    economy_car.show()
    # Output: Car construction complete. Parts: Grey Frame, 4 Wheels, Economy Engine

    # 构建产品 2: 跑车 (同样的构建方法，不同的调用次序和参数)
    sport_builder = CarBuilder()
    sport_car = sport_builder.build_engine("V8").build_wheels(5).build_frame("Red").get_result()
    sport_car.show()
    # Output: Car construction complete. Parts: V8 Engine, 5 Wheels, Red Frame
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **产品与创建过程解耦**：将产品本身与产品的创建过程分离，使得相同的创建过程可以创建不同的产品对象。
2.  **精细化控制创建**：将复杂产品的创建步骤分解在不同的方法中，使得创建过程更加清晰，方便控制创建次序。
3.  **系统扩展方便**：增加新的具体建造者无须修改原有类库的代码，`Director` 针对抽象建造者编程，符合"开闭原则"。
4.  **客户端简化**：客户端不必知道产品内部组成的细节，只需要指定具体的建造者类型。

### 4.2. 缺点

1.  **使用范围限制**：建造者模式所创建的产品一般具有较多的共同点，其组成部分相似。如果产品之间的差异性很大，则不适合使用。
2.  **类膨胀**：如果产品的内部变化复杂，可能需要定义很多具体建造者类来实现这种变化，导致系统变得很庞大。

## 5\. 比较：建造者模式 vs. 抽象工厂模式

| 特点 | 建造者模式 (Builder) | 抽象工厂模式 (Abstract Factory) |
| :--- | :--- | :--- |
| **关注点** | **一步一步构造一个完整复杂的对象**。关注**装配过程和顺序**。 | **创建一系列相关或相互依赖的产品族**。关注**产品族的横向切换**。 |
| **返回对象** | 返回一个**组装好的完整产品**（通常是一个对象）。 | 返回一系列**相关的产品**（通常是多个对象）。 |
| **客户端交互** | 客户端通过**指挥者**指导装配次序，或通过链式调用控制。 | 客户端直接实例化工厂类，调用工厂方法获取所需产品对象。 |
| **比喻** | **汽车组装工厂**，通过对部件的装配返回一辆完整的汽车。 | **汽车配件生产工厂**，生产一个产品族的产品。 |
