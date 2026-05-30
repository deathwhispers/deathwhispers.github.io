---
layout: post
title: 组合模式 (Composite Pattern) 深度解析
author: deathwhispers
date: 2019-10-25
slug: design-pattern-composite-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🌳 组合模式 (Composite Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：统一处理部分和整体

在许多场景中，我们需要处理**树形结构**或**部分-整体 (Part-Whole)** 的层次结构。例如，文件系统中的文件和文件夹、组织结构中的员工和部门、GUI 框架中的组件和容器。

* **问题**：处理单个对象（叶子）和组合对象（树枝）的方式往往不同。如果客户端需要区分这两种类型并使用不同的 API，代码会变得复杂且僵硬。
* **解决方案**：组合模式将单个对象和组合对象都视为实现同一接口的**抽象构件**。这使得客户端可以忽略它们之间的差异，使用**一致的方式**处理组合结构中的所有对象。

### 1.2. 模式定义

**组合模式 (Composite Pattern)**：

> **将对象组合成树形结构以表示“部分-整体”的层次结构，使得用户对单个对象和组合对象的使用具有一致性。**

它是一种**对象结构型模式**，又叫**部分整体模式**。

## 2\. 模式结构与角色

组合模式的关键是定义一个抽象构件类，作为叶子和树枝的父类，并让树枝构件内部包含一组抽象构件。

| 角色名称 | 职责描述 | 对应到文件系统实例 |
| :--- | :--- | :--- |
| **Component** (抽象构件) | 定义了叶子构件和树枝构件的**公共接口**，通常包含操作方法以及管理子构件的方法（可选）。 | `FileComponent` (接口) |
| **Leaf** (叶子构件) | 组合中的**最小单位**，不能再包含其他构件。实现 Component 定义的操作。 | `File` (文件) |
| **Composite** (树枝构件/组合构件) | 代表有子节点的复杂对象。实现 Component 定义的操作，并维护一个**子构件的集合**，提供管理子构件的方法（`add()`, `remove()`, `getChildren()`）。 | `Directory` (文件夹) |

### 2.1. 模式分类

根据抽象构件接口中是否包含管理子构件的方法，组合模式通常分为两种形式：

1.  **透明式 (Transparent)**：
    * 在 `Component` 接口中声明所有管理子构件的方法 (`add()`, `remove()`, `getChildren()`)。
    * **优点**：客户端无需区分叶子和树枝，具有高度的**透明性**。
    * **缺点**：叶子构件无须管理子构件，但仍需要实现（或空实现）这些方法，牺牲了单一职责原则。
2.  **安全式 (Safe)**：
    * 在 `Component` 接口中**不**声明管理子构件的方法。
    * 管理方法只在 `Composite` 类中声明。
    * **优点**：叶子构件不需要实现不相关的方法，符合**单一职责原则**。
    * **缺点**：客户端在处理时必须区分 Leaf 和 Composite，失去了透明性。

> 实际应用中，通常采用**透明式**以简化客户端代码。

## 3\. 代码深度解析（组织结构）

我们以**员工组织结构**为例，员工可以是叶子（普通员工）也可以是树枝（经理）。

### 3.1. Java 代码示例（透明式）

```java
import java.util.ArrayList;
import java.util.List;

// --- 1. 抽象构件 (Component) ---
// 定义所有员工/经理的公共接口
public abstract class EmployeeComponent {
    protected String name;
    protected String role;

    public EmployeeComponent(String name, String role) {
        this.name = name;
        this.role = role;
    }

    public abstract void displayDetails();

    // 管理子构件的方法（透明式，Leaf 也需要实现）
    public void add(EmployeeComponent c) {
        throw new UnsupportedOperationException();
    }
    public void remove(EmployeeComponent c) {
        throw new UnsupportedOperationException();
    }
    public List<EmployeeComponent> getSubordinates() {
        return null;
    }
}

// --- 2. 叶子构件 (Leaf) ---
// 普通员工，不能再包含下属
public class BasicEmployee extends EmployeeComponent {
    public BasicEmployee(String name) {
        super(name, "Staff");
    }

    @Override
    public void displayDetails() {
        System.out.println(String.format("  -> Staff: %s", name));
    }
    // 不支持管理方法，保留空实现或抛出异常
}

// --- 3. 树枝构件 (Composite) ---
// 经理/部门主管，可以包含下属
public class Manager extends EmployeeComponent {
    private List<EmployeeComponent> subordinates = new ArrayList<>();

    public Manager(String name, String role) {
        super(name, role);
    }

    @Override
    public void add(EmployeeComponent c) {
        subordinates.add(c);
    }
    @Override
    public void remove(EmployeeComponent c) {
        subordinates.remove(c);
    }
    @Override
    public List<EmployeeComponent> getSubordinates() {
        return subordinates;
    }

    @Override
    public void displayDetails() {
        System.out.println(String.format("== Manager: %s (%s) ==", name, role));
        for (EmployeeComponent sub : subordinates) {
            sub.displayDetails(); // 递归调用
        }
    }
}

// --- 4. 客户端调用 (Client) ---
public class CompositePatternDemo {
    public static void main(String[] args) {
        // 创建组合结构
        Manager ceo = new Manager("John", "CEO");

        Manager salesHead = new Manager("Robert", "Head Sales");
        BasicEmployee salesStaff1 = new BasicEmployee("Richard");
        salesHead.add(salesStaff1);

        Manager marketingHead = new Manager("Michel", "Head Marketing");
        BasicEmployee marketingStaff1 = new BasicEmployee("Laura");
        marketingHead.add(marketingStaff1);

        ceo.add(salesHead);
        ceo.add(marketingHead);

        // 使用一致的接口处理整个结构
        ceo.displayDetails();
    }
}



```

### 3.2. Python 代码示例

```python
from abc import ABC, abstractmethod

# --- 1. 抽象构件 (Component) ---
class FileSystemComponent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def display(self, indent=""):
        pass

    # 管理操作（透明式）：Leaf会抛出异常或空实现
    def add(self, component):
        raise NotImplementedError("Cannot add to a Leaf.")

    def remove(self, component):
        raise NotImplementedError("Cannot remove from a Leaf.")

# --- 2. 叶子构件 (Leaf) ---
class File(FileSystemComponent):
    def display(self, indent=""):
        print(f"{indent}📄 {self.name}")
    # add/remove 方法继承自 Component 并抛出异常

# --- 3. 树枝构件 (Composite) ---
class Folder(FileSystemComponent):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def display(self, indent=""):
        print(f"{indent}📁 {self.name}")
        for child in self.children:
            child.display(indent + "  ") # 递归调用

# --- 4. 客户端调用 (Client) ---
if __name__ == "__main__":

    # 建立文件系统树
    root = Folder("Root")

    docs_folder = Folder("Documents")
    docs_folder.add(File("Resume.pdf"))
    docs_folder.add(File("Notes.txt"))

    images_folder = Folder("Images")
    images_folder.add(File("Sunset.jpg"))
    images_folder.add(File("Logo.png"))

    root.add(docs_folder)
    root.add(images_folder)
    root.add(File("README.md")) # 直接在根目录下添加文件

    # 客户端使用统一的 display 接口处理整个结构
    root.display()
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **高层模块调用简单**：客户端可以忽略组合对象和单个对象的差异，使用一致的方式处理结构中的所有对象，简化了高层模块的调用。
2.  **节点自由增加**：增加新的叶子构件或树枝构件时，无需修改原有代码，符合“开闭原则”。
3.  **清晰的层次结构**：有效地表示了自然界或业务中的“部分-整体”层次结构。

### 4.2. 缺点

1.  **类型检查复杂**：在透明式组合中，由于叶子构件实现了它不需要的方法（如 `add()`），可能会在运行时出现错误（如在叶子上调用 `add()`）。
2.  **违反依赖倒置原则（通常指实现层面）**：如果抽象构件定义为具体类而不是接口，或者如果 Leaf 和 Composite 的声明过于依赖具体实现，则可能违反该原则。

## 5\. 适用环境

1.  **您想表示对象的部分-整体层次结构（树形结构）**。
2.  **您希望用户忽略组合对象与单个对象的不同**，用户将统一地使用组合结构中的所有对象。
3.  需要维护和展示树形菜单、文件和文件夹管理等具有**递归结构**的场景。
4.  需要从一个整体中能够独立出部分模块或功能的场景。
