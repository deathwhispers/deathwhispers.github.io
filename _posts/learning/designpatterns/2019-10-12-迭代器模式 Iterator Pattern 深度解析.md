---
layout: post
title: 迭代器模式 (Iterator Pattern) 深度解析
author: deathwhispers
date: 2019-10-12
slug: design-pattern-iterator-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🔁 迭代器模式 (Iterator Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：分离遍历行为与集合结构

在面向对象编程中，集合对象（如数组、列表、树等）通常包含一组元素。如果客户端需要访问这些元素，通常需要了解集合的底层数据结构（例如是数组索引、链表节点还是树的遍历算法）。

* **问题**：将遍历操作放在集合类中会导致：
    1.  暴露集合的**内部表示**（如索引、节点指针），违反信息隐藏原则。
    2.  如果需要多种遍历方式（如正序、倒序），集合类会变得臃肿。
* **解决方案**：迭代器模式将集合对象的遍历行为**分离**出来，封装到一个独立的**迭代器 (Iterator)** 对象中。

> **核心思想**：提供一种方法访问一个容器对象中各个元素，而又**不需要暴露该对象的内部细节**。

### 1.2. 模式定义

**迭代器模式 (Iterator Pattern)**：

> **提供一种方法顺序访问一个聚合对象中各个元素，而又无须暴露该对象的内部表示。**

迭代器模式是一种**对象行为型模式**，主要用于解决**不同的方式来遍历整个聚合对象**的问题。

-----

> **💡 注意**：如您笔记中所述，在现代编程语言如 Java (`java.util.Iterator`) 和 Python (迭代协议) 中，迭代器已是核心语言特性，因此在实际应用中通常直接使用语言自带的迭代器，而非手动从头实现该模式。

-----

## 2\. 模式结构与角色

迭代器模式通过抽象将遍历的职责从聚合对象中转移出来。

| 角色名称 | 职责描述 | 对应到名称列表实例 |
| :--- | :--- | :--- |
| **Iterator** (抽象迭代器) | 定义了访问和遍历元素的接口，通常包含 `hasNext()` (判断是否还有元素) 和 `next()` (获取下一个元素) 等方法。 | `Iterator` 接口 |
| **ConcreteIterator** (具体迭代器) | 实现了抽象迭代器接口，负责**记录遍历的当前位置**，并实现特定的遍历算法。 | `NameIterator` 内部类 |
| **Aggregate** (抽象聚合器/容器) | 定义创建相应迭代器对象的接口 (`getIterator()`)。 | `Container` 接口 |
| **ConcreteAggregate** (具体聚合器/容器) | 实现了创建具体迭代器的工厂方法，返回一个 `ConcreteIterator` 实例，它持有对该聚合对象的引用。 | `NameRepository` |

### 2.1. 模式分析核心

* **职责分离**：聚合对象负责存储数据，迭代器对象负责遍历数据。
* **多重遍历**：可以在同一个聚合对象上创建多个迭代器，实现多个独立的、同步或异步的遍历过程。
* **统一接口**：为遍历不同的聚合结构（如数组、链表、哈希表）提供一个统一的接口 (`Iterator`)。

## 3\. 代码深度解析（名称列表遍历）

我们以一个简单的名称列表 `NameRepository` 为例，实现对其内部元素的遍历。

### 3.1. Java 代码示例

```java
// --- 1. 抽象迭代器 (Iterator) ---
public interface Iterator {
    public boolean hasNext();
    public Object next();
}

// --- 2. 抽象聚合器 (Container/Aggregate) ---
public interface Container {
    public Iterator getIterator();
}

// --- 3. 具体聚合器 (NameRepository) ---
public class NameRepository implements Container {
    public String[] names =
    {
        "Robert" , "John" ,"Julie" , "Lora";
    }
    ;

    @Override
    public Iterator getIterator() {
        // 聚合器负责创建并返回一个具体迭代器
        return new NameIterator();
    }

    // --- 4. 具体迭代器 (NameIterator) ---
    // 通常作为具体聚合器的内部类，以便访问其内部数据
    private class NameIterator implements Iterator {
        int index;

        @Override
        public boolean hasNext() {
            if(index < names.length){
                return true;
            }
            return false;
        }

        @Override
        public Object next() {
            if(this.hasNext()){
                // 返回元素，并更新游标位置
                return names[index++];
            }
            return null;
        }
    }
}

// --- 5. 客户端调用 (Client) ---
public class IteratorPatternDemo {
    public static void main(String[] args) {
        NameRepository namesRepository = new NameRepository();

        // 客户端通过统一的 getIterator() 方法获取迭代器
        for(Iterator iter = namesRepository.getIterator();
        iter.hasNext();
        ){
            String name = (String)iter.next();
            System.out.println("Name : " + name);
        }
    }
}
```

### 3.2. Python 代码示例 (Pythonic Iterator Pattern)

在 Python 中，迭代器模式通过实现 **迭代器协议**（`__iter__` 和 `__next__`）来实现，这是其语言核心特性。

```python
# --- 1. Pythonic 聚合器 (Aggregate) ---
# 实现 __iter__ 方法，返回一个迭代器对象
class NameRepository:
    def __init__(self, names):
        self._names = names

    def __iter__(self):
        # 返回一个迭代器对象
        return NameIterator(self._names)

# --- 2. Pythonic 迭代器 (Iterator) ---
# 实现 __next__ 和 __iter__ 方法
class NameIterator:
    def __init__(self, names):
        self._names = names
        self._index = 0

    def __next__(self):
        # next() 方法：返回下一个元素，并在到达末尾时抛出 StopIteration
        if self._index < len(self._names):
            item = self._names[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration

    def __iter__(self):
        # 迭代器对象通常返回自身
        return self

# --- 3. 客户端调用 (Client) ---
if __name__ == "__main__":

    namesRepository = NameRepository(["Robert" , "John" ,"Julie" , "Lora"])

    # 客户端使用标准的 for...in 循环，底层调用 __iter__ 和 __next__
    print("--- Standard Iteration ---")
    for name in namesRepository:
        print("Name : " + name)

    # Python 推荐的另一种简单实现方式 (使用生成器)
    class SimpleRepository:
        def __init__(self, items):
            self._items = items

        def __iter__(self):
            # 这是一个更简洁的实现，直接返回一个生成器迭代器
            for item in self._items:
                yield item

    print("\n--- Generator Iteration ---")
    simpleRepo = SimpleRepository([10, 20, 30])
    for num in simpleRepo:
        print(f"Number: {num}")
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **支持多种遍历方式**：可以轻松创建不同的具体迭代器来实现正序、倒序、跳跃等各种遍历方式。
2.  **简化聚合类**：将遍历职责从聚合类中分离，聚合类专注于数据存储，符合单一职责原则。
3.  **信息隐藏**：客户端无须知道聚合对象的内部数据结构，只通过统一的 `Iterator` 接口访问元素。
4.  **易于扩展**：增加新的聚合类和迭代器类都很方便，无须修改原有代码。

### 4.2. 缺点

1.  **类数量增加**：每增加一个新的聚合类，就需要对应增加一个新的迭代器类，类的个数成对增加，增加了系统的复杂性。
2.  **不适用于复杂操作**：迭代器主要用于**顺序访问**，如果需要复杂的依赖于元素类型或集合结构的操作，则可能需要考虑**访问者模式**。

## 5\. 适用环境

1.  **访问一个聚合对象的内容而无须暴露它的内部表示。**
2.  **需要为聚合对象提供多种遍历方式**（例如，需要实现正向和反向两种遍历）。
3.  **为遍历不同的聚合结构提供一个统一的接口**（例如，无论底层是数组还是哈希表，都使用 `hasNext()` 和 `next()` 访问）。
