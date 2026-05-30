---
layout: post
title: 简单工厂模式 (Simple Factory Pattern) 深度解析
author: deathwhispers
date: 2019-07-05
slug: design-pattern-simple-factory-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🛠️ 简单工厂模式 (Simple Factory Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：集中管理对象创建

在软件应用中，当我们需要使用一组源自同一个基类的对象时（如不同外观的按钮、不同类型的图表等），如果客户端代码直接使用 `new` 关键字创建这些对象，会导致：

1.  客户端需要知道所有具体产品类的名字和创建细节。
2.  创建逻辑分散在客户端各处，难以维护。

**简单工厂模式**的动机在于：提供一个统一的、调用方便的方法，通过传入一个参数即可返回相应的对象，将对象的创建过程集中管理。

### 1.2. 模式定义

**简单工厂模式 (Simple Factory Pattern)**：

> 又称为**静态工厂方法 (Static Factory Method) 模式**，它专门定义一个类来负责创建其他类的实例，可以根据参数的不同返回不同类的实例。被创建的实例通常都具有共同的父类。

**注意**：简单工厂模式属于创建型模式，但它**不属于 GoF 提出的 23 种设计模式之一**，因为它缺乏足够的灵活性和抽象性。

## 2\. 模式结构与角色

简单工厂模式将对象的创建和对象本身的业务处理分离，它将产品对象的创建集中到一个工厂类中。

### 2.1. 模式角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Factory** (工厂角色) | **核心角色**。负责实现创建所有实例的内部逻辑，通常包含一个**静态的工厂方法**，根据传入的参数返回具体产品实例。 |
| **Product** (抽象产品角色) | 所创建的所有对象的父类（或接口），负责描述所有实例所共有的公共接口。 |
| **ConcreteProduct** (具体产品角色) | **创建目标**。是抽象产品角色的具体实现，所有创建的对象都充当这个角色的某个具体类的实例。 |

### 2.2. 模式分析核心

* **集中逻辑**：工厂类集中了所有产品创建逻辑，通过条件判断（如 `if-else` 或 `switch`）来决定创建哪一个具体产品类的实例。
* **客户端简化**：客户端免除直接创建产品对象的责任，只需知道传入工厂类的参数即可，无须知道其创建细节。

## 3\. 代码分析与实例（图形创建）

### 3.1. Java 简单工厂示例

以图形创建为例，客户端只需传入图形类型字符串即可获取对象。

```java
// --- 1. 抽象产品 (Product) ---
public interface Shape {
    void draw();
}

// --- 2. 具体产品 (ConcreteProduct) ---
public class Circle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing a Circle.");
    }
}

public class Rectangle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing a Rectangle.");
    }
}

// --- 3. 工厂角色 (Factory) ---
public class ShapeFactory {
    // 静态工厂方法是简单工厂模式的典型特征
    public static Shape createShape(String shapeType) {
        if (shapeType == null) {
            return null;
        }

    // 核心：集中了所有产品创建的判断逻辑
    if (shapeType.equalsIgnoreCase("CIRCLE")) {
        return new Circle();
    } else if (shapeType.equalsIgnoreCase("RECTANGLE"))
    {
    }
return new Rectangle();
}
// 增加新产品必须修改这里的逻辑！

throw new IllegalArgumentException("Unknown shape type: " + shapeType);
}
}

// --- 4. 客户端调用 (Client) ---
public class SimpleFactoryDemo {
    public static void main(String[] args) {
        // 客户端无需关心具体类名，只需传入参数
        Shape shape1 = ShapeFactory.createShape("CIRCLE");
        shape1.draw();

        Shape shape2 = ShapeFactory.createShape("rectangle");
        shape2.draw();
    }
}

```

### 3.2. Python 简单工厂示例

Python 中通常使用字典映射代替 `if-else` 链，但本质上仍然是简单工厂。

```python
# --- 1. 抽象产品 (Product) ---
class Product:
    def use(self):
        raise NotImplementedError

# --- 2. 具体产品 (ConcreteProduct) ---
class ConcreteProductA(Product):
    def use(self):
        print("ConcreteProduct A is being used.")

class ConcreteProductB(Product):
    def use(self):
        print("ConcreteProduct B is being used.")

# --- 3. 工厂角色 (Factory) ---
class SimpleFactory:

    # 使用字典映射集中创建逻辑
    _product_map = {
        "A": ConcreteProductA,
        "B": ConcreteProductB
    }

    @staticmethod
    def create_product(proname: str) -> Product:
        if proname in SimpleFactory._product_map:
            # 返回并实例化对应的类
            return SimpleFactory._product_map[proname]()
        return None

# --- 4. 客户端调用 (Client) ---
if __name__ == "__main__":
    prod_a = SimpleFactory.create_product("A")
    prod_a.use()

    prod_b = SimpleFactory.create_product("B")
    prod_b.use()
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **实现职责分割**：工厂类提供了专门的类用于创建对象，客户端可以免除直接创建产品对象的责任，而仅仅“消费”产品。
2.  **降低记忆量**：客户端无须知道所创建的具体产品类的类名，只需要知道具体产品类所对应的参数即可。
3.  **使用方便**：由于工厂方法通常是静态方法，可以直接通过类名调用。
4.  **提高灵活性（有限）**：通过引入配置文件来存储参数，可以在不修改任何客户端代码的情况下更换具体产品类。

### 4.2. 缺点

1.  **违背“开闭原则”**：这是简单工厂模式**最大的问题**。增加新的产品必须修改工厂类的判断逻辑代码，导致系统扩展困难。
2.  **职责过重**：工厂类集中了所有产品创建逻辑，一旦工厂类不能正常工作，整个系统都会受到影响。
3.  **无法形成等级结构**：由于使用了静态工厂方法，工厂角色无法形成基于继承的等级结构，限制了模式的进一步抽象和推广。
4.  **复杂度增加**：在一定程度上增加了系统的复杂度和理解难度。

## 5\. 适用环境与模式应用

### 5.1. 适用环境

1.  **工厂类负责创建的对象比较少**：由于创建的对象较少，不会造成工厂方法中的业务逻辑太过复杂。
2.  **客户端只知道传入工厂类的参数，对于如何创建对象不关心**：客户端既不需要关心创建细节，甚至连类名都不需要记住，只需要知道类型所对应的参数。

### 5.2. 模式应用实例

* **Java JDK 类库**：
    * `java.text.DateFormat`：通过 `getDateInstance()` 等静态方法根据参数返回不同风格的日期格式化实例。
    * `KeyGenerator.getInstance("DESede")` 和 `Cipher.getInstance("DESede")`：Java 加密技术中，通过传入算法名称来获取对应的密钥生成器或密码器实例。
