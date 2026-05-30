---
layout: post
title: 原型模式 (Prototype Pattern) 深度解析
author: deathwhispers
date: 2019-09-29
slug: design-pattern-prototype-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🧬 原型模式 (Prototype Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：高性能创建重复对象

当直接创建对象的代价比较大时（例如，需要进行高代价的数据库操作、繁琐的数据准备或权限校验），频繁使用 `new` 关键字会影响性能。

**原型模式**通过**拷贝**一个现有对象来生成新对象，避免了传统的对象创建过程，从而实现了**性能优化**和**资源节约**。

### 1.2. 模式定义

**原型模式 (Prototype Pattern)**：

> 用**原型实例**指定创建对象的种类，并且通过**拷贝**这些原型创建新的对象。

原型模式是一种**创建型模式**，它提供了一种创建对象的最佳方式之一。

## 2\. 模式结构与实现要点

### 2.1. 关键代码：实现克隆操作

实现原型模式的核心在于**实现克隆操作**。

* **在 Java 中**：实现 `Cloneable` 接口，并重写 `Object` 类的 `clone()` 方法。
* **在其他语言中**：实现一个 `Clone()` 或 `Copy()` 方法，提供复制自身的能力。

### 2.2. 模式角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Prototype** (抽象原型角色) | 声明克隆自身的操作接口（例如 Java 中的 `Cloneable` 接口）。 |
| **ConcretePrototype** (具体原型角色) | 实现克隆操作，可以返回自身的一个克隆实例。 |
| **Client** (客户端角色) | 使用抽象原型中的 `clone()` 方法来创建新的对象。 |

## 3\. 浅拷贝与深拷贝的深度分析

原型模式中，拷贝操作可以分为**浅拷贝**和**深拷贝**，理解它们的区别至关重要。

### 3.1. 浅拷贝 (Shallow Copy)

* **实现方式**：Java 中默认的 `Object.clone()` 方法实现的就是浅拷贝。
* **拷贝内容**：
    * **值类型/基本类型** (`int`, `char`, `long`, 等) 会被**完全拷贝**。
    * **引用类型** (对象、数组) **只拷贝引用地址**，而不是对象本身。新对象和原始对象内部的引用成员变量仍然指向**同一块内存地址**。
* **影响**：当客户端修改新对象内部的引用成员时，原始对象的该成员也会被修改，因此存在**数据污染**的风险。

### 3.2. 深拷贝 (Deep Copy)

* **实现方式**：需要手动编写代码，对对象内部的**所有引用类型的成员变量进行独立的拷贝**（递归克隆）。在 Java 中，通常通过**序列化**（读取二进制流）或**递归调用 `clone()`** 方法来实现。
* **拷贝内容**：对象本身及其内部所有引用的对象都会被**完全复制**，新对象和原始对象完全独立。
* **示例**：对私有的类变量进行独立的拷贝，如 `this.arrayList = (ArrayList) this.arrayList.clone();`

### 3.3. 浅拷贝的约束条件（Java）

使用原型模式时，引用的成员变量必须满足以下两个条件才需要考虑**拷贝**（否则浅拷贝即可）：

1.  是类的成员变量，而不是方法内的局部变量。
2.  必须是一个**可变的引用对象**（Mutable Reference），而不是一个原始类型或**不可变对象**（Immutable Object，如 Java 中的 `String`）。

## 4\. 模式应用场景与优缺点

### 4.1. 优点

1.  **性能优良**：原型模式是在内存二进制流中进行拷贝，性能通常比直接 `new` 一个对象要好，特别是在循环体内需要产生大量对象时。
2.  **逃避构造函数的约束**：直接在内存中拷贝，**构造函数不会被执行**。这既是优点也是缺点（如果构造函数中有必要的初始化逻辑，则需要注意）。

### 4.2. 缺点

1.  **克隆方法实现复杂**：特别是对于已有复杂的类，如果类引用了不支持串行化的间接对象，或者引用含有**循环结构**时，实现深拷贝会非常困难。
2.  **必须实现克隆接口**：所有需要支持拷贝的类都必须实现 `Cloneable` 接口。

### 4.3. 适用场景

1.  **资源优化场景**：类初始化需要消耗非常多的资源（数据、硬件资源等），通过缓存原型并克隆可以节省资源。
2.  **性能和安全要求的场景**：通过 `new` 产生对象需要非常繁琐的数据准备或访问权限时。
3.  **一个对象多个修改者的场景**：一个对象需要提供给多个调用者访问，且每个调用者都可能需要独立修改其值时，可以拷贝多个独立对象供调用者使用。
4.  **与工厂模式联用**：原型模式很少单独出现，通常和工厂模式一起出现，通过 `clone()` 方法创建对象，然后由工厂方法提供给调用者。

## 5\. 代码示例（多语言实现）

### 5.1. Java 代码示例 (Shape 缓存与克隆)

此示例展示了如何使用 `ShapeCache` 缓存原型对象，并在请求时返回其克隆。

```java
import java.util.Hashtable;

// 1. 抽象原型类 (Prototype)
public abstract class Shape implements Cloneable {
    private String id;
    protected String type;

    abstract void draw();

    // 实现克隆操作（默认是浅拷贝）
    public Object clone() {;
    Object clone = null;
    try {
        // 调用 Object 类的原生 clone 方法
        clone = super.clone();
    } catch (CloneNotSupportedException e) {;
    e.printStackTrace();
}
return clone;
}

// 省略 Getter/Setter
}

// 2. 具体原型类 (ConcretePrototype)
public class Rectangle extends Shape {
    public Rectangle(){;
    type = "Rectangle";
}
@Override
public void draw() {;
System.out.println("Inside Rectangle::draw() method.");
}
}

// 3. 原型缓存/工厂类 (ShapeCache)
public class ShapeCache {
    private static Hashtable<String, Shape> shapeMap = new Hashtable<>();

    // 核心方法：获取并返回克隆对象
    public static Shape getShape(String shapeId) {;
    Shape cachedShape = shapeMap.get(shapeId);
    // 返回对象的克隆，而不是原始对象
    return (Shape) cachedShape.clone();
}

// 加载原型缓存（模拟从数据库加载）
public static void loadCache() {;
Rectangle rectangle = new Rectangle();
rectangle.setId("3");
shapeMap.put(rectangle.getId(), rectangle);
System.out.println("Cache loaded with Rectangle ID 3.");
}
}


```

### 5.2. Python 代码示例 (深浅拷贝)

Python 的 `copy` 模块提供了 `copy()`（浅拷贝）和 `deepcopy()`（深拷贝）。

```python
import copy

# 引用类型成员
class Detail:
    def __init__(self, value):
        self.value = value

# 具体原型类 (实现了克隆能力)
class PrototypePython:
    def __init__(self, name, data_list):
        self.name = name                 # 原始类型/不可变类型
        self.data_list = data_list       # 可变的引用类型
        self.detail = Detail(name)       # 另一个引用对象

    # Python 浅拷贝：使用 copy.copy()
    def shallow_copy(self):
        return copy.copy(self)

    # Python 深拷贝：使用 copy.deepcopy()
    def deep_copy(self):
        return copy.deepcopy(self)

# 客户端测试
prototype = PrototypePython("Original", [1, 2])

# --- 浅拷贝测试 ---
shallow = prototype.shallow_copy()
shallow.name = "Shallow Copy"
shallow.data_list.append(3) # 修改引用成员

print(f"Original List ID: {id(prototype.data_list)}")
print(f"Shallow List ID:  {id(shallow.data_list)}")
print(f"Original List: {prototype.data_list}") # 浅拷贝导致原对象也被修改
# Output: Original List: [1, 2, 3]

# --- 深拷贝测试 ---
deep = prototype.deep_copy()
deep.data_list.append(4)

print(f"\nOriginal List ID: {id(prototype.data_list)}") # 此时已经带了 [3]
print(f"Deep List ID:     {id(deep.data_list)}") # ID 不同，独立了
print(f"Original List: {prototype.data_list}")
# Output: Original List: [1, 2, 3] (未被深拷贝修改)
```

### 5.3. C++ 代码示例 (克隆抽象类)

C++ 中通过定义虚函数 `clone()` 来实现抽象原型接口。

```cpp
// 1. 抽象原型类 (Abstract Prototype)
class Shape {
public:
    virtual ~Shape() {}
    // 关键：声明虚函数 clone，返回自身的指针
    virtual Shape* clone() const = 0;
    virtual void draw() = 0;
};

// 2. 具体原型类 (Concrete Prototype)
class Circle : public Shape {
private:
    int radius;
public:
    Circle(int r) : radius(r) {}

    // 实现克隆操作：返回一个新创建的、与自身状态相同的对象
    Circle* clone() const override {
        return new Circle(*this); // 使用拷贝构造函数实现浅拷贝
    }

    void draw() override {
        std::cout << "Drawing Circle with radius " << radius << std::endl;
    }
};

// 客户端使用
Circle* original = new Circle(10);
// 通过克隆方法创建新对象
Circle* cloned = original->clone();

// 原始对象和克隆对象是不同的实例
// if (original != cloned) // True
```
