---
layout: post
title: 空对象模式 (Null Object Pattern) 深度解析
author: deathwhispers
date: 2019-10-12
slug: design-pattern-null-object-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 📜 设计模式：空对象模式 (Null Object Pattern)

## 概念与动机

### 定义

**空对象模式 (Null Object Pattern)** 是一种行为型设计模式，它用一个\*\*不执行任何操作（no-op）\*\*的对象来代替程序中的
`null` 引用。

这个"空对象"实现了与实际对象相同的接口或继承相同的抽象类，从而可以在客户端代码中**透明地使用**。

### 动机

在传统的编程中，为了防止访问空引用时抛出 `NullPointerException` (Java) 或类似错误，我们经常需要编写大量的条件判断语句（如
`if (object != null)`）来进行检查。

空对象模式的核心价值在于：**消除条件检查，简化客户端代码。**

* **消除条件逻辑：** 客户端代码可以直接调用方法，而无需关心它拿到的是一个真实对象还是一个空对象。
* **提供默认行为：** 空对象可以提供默认的、安全且"无害"的行为，例如返回一个空字符串，或者执行一个空操作。

## 结构

在空对象模式中，主要角色包括：

1. **抽象实体 (Abstract Entity)：** 定义了真实对象和空对象都必须实现或继承的接口或抽象类。
2. **真实实体 (Real Entity)：** 实现了抽象实体，并提供实际的业务逻辑。
3. **空对象 (Null Object)：** 实现了抽象实体，但其方法实现为空操作或返回默认值。
4. **工厂/客户端 (Factory/Client)：** 根据条件判断，返回真实实体或空对象。

-----

## 💻 实现示例：客户查找服务

我们将创建一个客户查找服务。如果客户存在，返回 $RealCustomer$；如果客户不存在，返回 $NullCustomer$。

### 1\. Java 实现

#### 步骤 1: 抽象类 $AbstractCustomer$ (修正原笔记中的类名错误)

定义了客户的通用接口。

```java
// AbstractCustomer.java
public abstract class AbstractCustomer {
    protected String name;

    // 检查对象是否为空对象
    public abstract boolean isNil();

    // 获取客户名称
    public abstract String getName();
}
```

#### 步骤 2: 实体类 $RealCustomer$ 和 $NullCustomer$

* **RealCustomer:** 包含真实的客户信息。
* **NullCustomer:** 不包含信息，返回默认的"不可用"字符串。

<!-- end list -->

```java
// RealCustomer.java
public class RealCustomer extends AbstractCustomer {
    public RealCustomer(String name) {
        this.name = name;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public boolean isNil() {
        return false;
    }
}

// NullCustomer.java
public class NullCustomer extends AbstractCustomer {
    @Override
    public String getName() {
        return "Not Available in Customer Database"; // 默认行为
    }

    @Override
    public boolean isNil() {
        return true;
    }
}
```

#### 步骤 3: 工厂类 $CustomerFactory$

负责根据名字决定返回 $RealCustomer$ 还是 $NullCustomer$。

```java
// CustomerFactory.java
public class CustomerFactory {
    public static final String[] names =
    {
        "Rob", "Joe", "Julie";
    }
    ;

    public static AbstractCustomer getCustomer(String name) {
        for (int i = 0; i < names.length; i++) {
            if (names[i].equalsIgnoreCase(name)) {
                return new RealCustomer(name);
            }
        }
        // 如果未找到，返回 NullCustomer
        return new NullCustomer();
    }
}
```

#### 4\. 客户端演示 $NullPatternDemo$

**注意：** 客户端代码无需任何 `if (customer != null)` 检查。

```java
// NullPatternDemo.java
public class NullPatternDemo {
    public static void main(String[] args) {
        AbstractCustomer customer1 = CustomerFactory.getCustomer("Rob");
        AbstractCustomer customer2 = CustomerFactory.getCustomer("Bob");
        AbstractCustomer customer3 = CustomerFactory.getCustomer("Julie");
        AbstractCustomer customer4 = CustomerFactory.getCustomer("Laura");

        System.out.println("Customers");
        System.out.println(customer1.getName()); // Rob
        System.out.println(customer2.getName()); // Not Available...
        System.out.println(customer3.getName()); // Julie
        System.out.println(customer4.getName()); // Not Available...
    }
}


```

##### 执行结果：

```
Customers
Rob
Not Available in Customer Database
Julie
Not Available in Customer Database
```

### 2\. Python 实现

在 Python 中，我们使用 `abc` 模块来定义抽象基类。

#### 步骤 1: 抽象基类 $AbstractCustomer$

```python
# abstract_customer.py
from abc import ABC, abstractmethod

class AbstractCustomer(ABC):
    def __init__(self, name: str = None):
        self._name = name

    @abstractmethod
    def is_nil(self) -> bool:
        """检查是否为空对象"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取客户名称"""
        pass
```

#### 步骤 2: 实体类 $RealCustomer$ 和 $NullCustomer$

```python
# real_customer.py
class RealCustomer(AbstractCustomer):
    def is_nil(self) -> bool:
        return False

    def get_name(self) -> str:
        return self._name

# null_customer.py
class NullCustomer(AbstractCustomer):
    def is_nil(self) -> bool:
        return True

    def get_name(self) -> str:
        # 提供默认的、无害的返回
        return "Not Available in Customer Database"
```

#### 步骤 3: 工厂类 $CustomerFactory$

```python
# customer_factory.py
class CustomerFactory:
    NAMES = ["Rob", "Joe", "Julie"]

    @staticmethod
    def get_customer(name: str) -> AbstractCustomer:
        if name in CustomerFactory.NAMES:
            return RealCustomer(name)
        # 返回 Null Object
        return NullCustomer()
```

#### 4\. 客户端演示

```python
# null_pattern_demo.py
if __name__ == '__main__':
    customer1 = CustomerFactory.get_customer("Rob")
    customer2 = CustomerFactory.get_customer("Bob")
    customer3 = CustomerFactory.get_customer("Julie")
    customer4 = CustomerFactory.get_customer("Laura")

    print("Customers")
    print(customer1.get_name())
    print(customer2.get_name())
    print(customer3.get_name())
    print(customer4.get_name())

    # 客户端代码始终可以安全地调用 .get_name()
```

##### 执行结果：

```
Customers
Rob
Not Available in Customer Database
Julie
Not Available in Customer Database
```

-----

## 🌟 优缺点分析

| 方面        | 优点 (Pros)                                    | 缺点 (Cons)                                             |
|:----------|:---------------------------------------------|:------------------------------------------------------|
| **代码可读性** | 极大地简化了客户端代码，消除了大量的 $if (obj != null)$ 检查。    | 增加了新的类（Null Object），可能导致类数量增多，增加维护负担。                 |
| **错误处理**  | 将检查 $null$ 的逻辑集中到工厂，客户端无需关心。                 | 如果业务逻辑要求区分"不存在"和"存在但为空"，可能会引入额外的复杂性（例如 $isNil()$ 方法）。 |
| **健壮性**   | 保证了程序执行的流程，消除了潜在的 $NullPointerException$ 风险。 | 该模式必须基于一个稳定的、被所有真实对象和空对象实现的接口。                        |
| **耦合性**   | 客户端对真实对象和空对象解耦，只依赖于抽象接口。                     | 只能用于可以预知 $null$ 检查的场景。如果 $null$ 出现的位置不确定，该模式无效。       |
