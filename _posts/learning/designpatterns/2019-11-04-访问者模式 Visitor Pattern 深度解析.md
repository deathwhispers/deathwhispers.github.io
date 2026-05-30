---
layout: post
title: 访问者模式 (Visitor Pattern) 深度解析
author: deathwhispers
date: 2019-11-04
slug: design-pattern-visitor-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🚶 访问者模式 (Visitor Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：分离操作与数据结构

在一个对象结构（如复杂的树形或列表）中，包含了很多不同类的对象。我们经常需要对这些对象执行各种**不相关的操作**（例如：计算成本、生成报表、执行类型检查）。

* **问题**：如果将所有操作都放在元素类内部，会导致：
    1.  元素类职责过多，违反**单一职责原则**。
    2.  每增加一个新操作，都需要修改所有元素类，违反**开闭原则**。
    3.  操作与数据结构高度耦合，难以扩展。
* **解决方案**：访问者模式将作用于数据结构中各元素的操作**封装**到一个独立的类（访问者）中。

> 访问者模式可以在**不改变数据结构**的前提下，定义作用于这些元素的新操作，实现了**数据结构与数据操作的分离**。

### 1.2. 模式定义

**访问者模式 (Visitor Pattern)**：

> **封装一些作用于某种数据结构中的各元素的操作，它可以在不改变数据结构的前提下定义作用于这些元素的新操作。**

访问者模式是一种**对象行为型模式**，主要用于解决**稳定的数据结构和易变的操作耦合**的问题。

## 2\. 模式结构与角色

访问者模式是少数使用**双重分派 (Double Dispatch)** 机制来实现的模式。

| 角色名称 | 职责描述 | 对应到计算机组件实例 |
| :--- | :--- | :--- |
| **Element** (抽象元素) | 定义一个**接受访问者**的抽象方法（`accept(Visitor visitor)`）。所有具体元素都必须实现此方法。 | `ComputerPart` 接口 |
| **ConcreteElement** (具体元素) | 实现了 `accept` 方法，该方法通常调用访问者的相应 `visit` 方法，并把自己（`this`）传递给访问者。 | `Mouse`, `Keyboard`, `Computer` |
| **Visitor** (抽象访问者) | 为所有具体元素类声明抽象的 `visit` 方法。每种元素类型都有一个对应的 `visit` 方法重载。 | `ComputerPartVisitor` 接口 |
| **ConcreteVisitor** (具体访问者) | 实现了抽象访问者中声明的每一个 `visit` 方法，用于实现针对不同元素的不同操作逻辑。 | `ComputerPartDisplayVisitor` |

### 2.1. 双重分派机制

访问者模式的关键在于 `Element.accept(Visitor)` 方法的实现，它体现了双重分派：

1.  **第一次分派（运行时确定）**：客户端调用 `element.accept(visitor)`，运行时确定了**具体元素 (ConcreteElement)** 的类型。
2.  **第二次分派（运行时确定）**：在 `accept` 方法内部，调用 `visitor.visit(this)`。由于 `this` 是一个具体的元素类型，并且 `visit` 方法在 `Visitor` 接口中有多个重载，编译器和运行时环境会根据 `this` 的实际类型选择调用**具体访问者**的对应 `visit` 方法。

这种机制使得操作（访问者）和数据结构（元素）能够松耦合地配合工作。

## 3\. 代码深度解析（计算机组件展示）

我们以一个计算机组件 (Computer, Mouse, Keyboard) 结构，并对其执行不同的操作（如 Display、CheckHealth）为例。

### 3.1. Java 代码示例

```java
// --- 1. 抽象元素 (Element) ---
public interface ComputerPart {
    // 接受访问者的方法，将自身引用传入
    public void accept(ComputerPartVisitor computerPartVisitor);
}

// --- 2. 具体元素 A: 鼠标 ---
public class Mouse  implements ComputerPart {
    @Override
    public void accept(ComputerPartVisitor computerPartVisitor) {
        // 双重分派的关键：调用访问者对应 Mouse 类型的 visit 方法
        computerPartVisitor.visit(this);
    }
}

// --- 3. 具体元素 B: 计算机 (组合结构) ---
public class Computer implements ComputerPart {
    ComputerPart[] parts;

    public Computer(){
        parts = new ComputerPart[]
        {
            new Mouse(), new Keyboard(), new Monitor();
        }
    ;
}

@Override
public void accept(ComputerPartVisitor computerPartVisitor) {
    // 遍历所有子元素，让它们都接受访问
    for (ComputerPart part : parts) {
        part.accept(computerPartVisitor);
    }
// 访问者访问 Computer 自身
computerPartVisitor.visit(this);
}
}
// (Keyboard 和 Monitor 类结构类似 Mouse，此处省略)

// --- 4. 抽象访问者 (Visitor) ---
public interface ComputerPartVisitor {
    // 为每一个 ConcreteElement 定义一个重载的 visit 方法
    public void visit(Computer computer);
    public void visit(Mouse mouse);
    public void visit(Keyboard keyboard);
    // ...
}

// --- 5. 具体访问者 A: 显示组件名称 ---
public class ComputerPartDisplayVisitor implements ComputerPartVisitor {
    @Override
    public void visit(Computer computer) {
        System.out.println("Displaying Computer.");
    }
@Override
public void visit(Mouse mouse) {
    System.out.println("Displaying Mouse.");
}
@Override
public void visit(Keyboard keyboard) {
    System.out.println("Displaying Keyboard.");
}
// ...
}

// --- 6. 客户端调用 (Client) ---
public class VisitorPatternDemo {
    public static void main(String[] args) {
        ComputerPart computer = new Computer(); // 这是一个组合结构

        // 客户端创建具体的访问者并将其传入元素结构
        System.out.println("--- 执行 Display 操作 ---");
        computer.accept(new ComputerPartDisplayVisitor());

        // 如果要新增一个 CheckHealth 操作，只需新增一个 ConcreteVisitor 即可：
        // System.out.println("\n--- 执行 CheckHealth 操作 ---");
        // computer.accept(new ComputerPartHealthCheckVisitor()); // 无需修改 Computer 或 Part 接口
    }
}

```

### 3.2. Python 代码示例

```python
from abc import ABC, abstractmethod

# --- 1. 抽象访问者 (Visitor) ---
class AssetVisitor(ABC):
    @abstractmethod
    def visit_stock(self, stock):
        pass

    @abstractmethod
    def visit_bond(self, bond):
        pass

    # ... 其他资产类型

# --- 2. 抽象元素 (Element) ---
class FinancialAsset(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def accept(self, visitor: AssetVisitor):
        pass

# --- 3. 具体元素 A: 股票 ---
class Stock(FinancialAsset):
    def accept(self, visitor: AssetVisitor):
        # 第一次分派确定 Stock，第二次分派调用 visit_stock
        visitor.visit_stock(self)

# --- 4. 具体元素 B: 债券 ---
class Bond(FinancialAsset):
    def accept(self, visitor: AssetVisitor):
        visitor.visit_bond(self)

# --- 5. 具体访问者 A: 净值计算器 ---
class NetWorthCalculator(AssetVisitor):
    def visit_stock(self, stock):
        # 针对股票的特有计算逻辑
        print(f"Calculating Stock Net Worth: {stock.value * 1.05:.2f} (5% buffer)")
        return stock.value * 1.05

    def visit_bond(self, bond):
        # 针对债券的特有计算逻辑
        print(f"Calculating Bond Net Worth: {bond.value:.2f} (Stable)")
        return bond.value

# --- 6. 客户端调用 (Client) ---
if __name__ == "__main__":

    portfolio = [
        Stock(10000),
        Bond(5000),
        Stock(2000)
    ]

    # 实例化一个操作：净值计算
    calculator = NetWorthCalculator()
    total_worth = 0

    print("--- Evaluating Portfolio ---")
    for asset in portfolio:
        # 客户端使用统一的 accept 接口
        total_worth += calculator.visit(asset) # Python 动态特性简化了这里的调用，但在类型系统中仍是双重分派

    # Python 习惯用法：在 Visitor 中集成调度
    # 实际在 Python 中，通常使用 `functools.singledispatch` 或自定义调度

    # 这里演示标准的 accept 调用
    # 注意：为了简化Python示例，我们通常直接在Visitor类中手动选择方法

    # Standard Dispatch (Manual Example):
    print("\n--- Standard Visitor Dispatch ---")
    for asset in portfolio:
        asset.accept(calculator)
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **符合单一职责原则**：将数据结构和操作分离，操作逻辑封装在访问者中，元素类只负责自身结构和接受访问。
2.  **优秀的扩展性**：增加新的操作（新的 `ConcreteVisitor`）非常容易，无需修改任何元素类，符合**开闭原则**。
3.  **操作集中化**：相关的操作逻辑被集中在一个访问者类中，便于管理和维护。

### 4.2. 缺点

1.  **具体元素变更困难**：如果数据结构本身不稳定（即经常增加新的 `ConcreteElement`），则需要修改所有 `Visitor` 接口和所有 `ConcreteVisitor` 类，扩展性极差。
2.  **违反依赖倒置原则**：`AbstractVisitor` 必须为每一个 `ConcreteElement` 定义 `visit` 方法，因此它**依赖了具体类**而非抽象。
3.  **暴露细节**：访问者需要访问元素类的内部状态才能执行操作，具体元素对访问者公布了部分细节，违反了迪米特原则。

## 5\. 适用环境

1.  **对象结构（Element Classes）中对象对应的类很少改变**，但经常需要在此对象结构上定义**新的操作**。
2.  **需要对一个对象结构中的对象进行很多不同并且不相关的操作**，且希望避免让这些操作“污染”这些对象的类。
3.  **一个对象结构包含很多类对象**，它们有不同的接口，但你想对它们实施依赖于其具体类型的操作（需要双重分派）。
4.  需要对功能进行统一（如报表生成、UI 渲染、拦截器与过滤器）。
