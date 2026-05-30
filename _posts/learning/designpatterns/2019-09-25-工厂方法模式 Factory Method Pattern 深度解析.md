---
layout: post
title: 工厂方法模式 (Factory Method Pattern) 深度解析
author: deathwhispers
date: 2019-09-25
slug: design-pattern-factory-method-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🏭 工厂方法模式 (Factory Method Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：符合“开闭原则”的工厂

在简单工厂模式中，一个工厂类负责所有产品的创建。当需要引入新产品时，必须修改工厂类的创建逻辑（例如添加新的 `if-else` 分支），这违背了“开闭原则” (对扩展开放，对修改关闭)。

**工厂方法模式**的动机在于：不再设计一个单一的工厂类来负责所有产品的创建，而是将**具体产品的创建过程交给专门的工厂子类去完成**。

* 定义一个**抽象工厂类**。
* 定义具体的**工厂子类**来生成具体的产品。

这种抽象化的结果是，如果出现新的产品类型，只需要为这种新产品创建一个**具体的工厂类**，而无需修改原有的抽象工厂和现有工厂类，使得系统具有极好的可扩展性。

### 1.2. 模式定义

**工厂方法模式 (Factory Method Pattern)**：

> 定义一个创建对象的**接口**，但让实现这个接口的**子类**来决定实例化哪个类。工厂方法模式将产品类的实例化操作**延迟**到工厂子类中完成，即通过工厂子类来确定究竟应该实例化哪一个具体产品类。

工厂方法模式又称为**工厂模式**、**虚拟构造器 (Virtual Constructor) 模式**或**多态工厂 (Polymorphic Factory) 模式**，它属于**类创建型模式**。

## 2\. 模式结构与角色

工厂方法模式是简单工厂模式的进一步抽象和推广。

### 2.1. 模式角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Product** (抽象产品) | 定义产品的接口，是工厂方法模式所创建对象的超类型。 |
| **ConcreteProduct** (具体产品) | 实现了抽象产品接口，是工厂创建的目标对象。 |
| **Factory** (抽象工厂) | **声明了工厂方法**，用于返回一个产品。它是工厂方法模式的核心，任何创建对象的工厂类都必须实现该接口。 |
| **ConcreteFactory** (具体工厂) | **抽象工厂类的子类**，实现了抽象工厂中定义的工厂方法，负责返回一个具体的**产品实例**。 |

### 2.2. 产品等级结构与产品族

* **产品等级结构**：指抽象产品下所有具体产品类的继承结构（例如，`Shape` 下有 `Circle` 和 `Rectangle`）。
* **产品族**：指由同一个工厂生产出来的，位于不同产品等级结构的一组产品（例如，A工厂生产鼠标和键盘，B工厂也生产鼠标和键盘）。**（注意：产品族是抽象工厂模式的核心概念，在工厂方法模式中通常只关注产品等级结构。）**

## 3\. 代码分析与实例（日志记录器）

我们使用**日志记录器**的例子来体现工厂方法模式的结构。系统要求支持文件记录、数据库记录等多种日志记录方式。

### 3.1. Java 核心代码结构

```java
// --- 1. 抽象产品 (Product) ---
public interface Logger {
    void writeLog(String message);
}

// --- 2. 具体产品 (ConcreteProduct) ---
public class FileLogger implements Logger {
    @Override
    public void writeLog(String message) {;
    System.out.println("LOG to File: " + message);
}
}

public class DatabaseLogger implements Logger {
    @Override
    public void writeLog(String message) {;
    System.out.println("LOG to Database: " + message);
}
}

// --- 3. 抽象工厂 (Factory) ---
public interface LoggerFactory {
    // 声明工厂方法，返回抽象产品类型
    Logger createLogger();
}

// --- 4. 具体工厂 (ConcreteFactory) ---
public class FileLoggerFactory implements LoggerFactory {
    @Override
    public Logger createLogger() {;
    // 负责创建具体产品
    return new FileLogger();
}
}

public class DatabaseLoggerFactory implements LoggerFactory {
    @Override
    public Logger createLogger() {;
    return new DatabaseLogger();
}
}

// --- 5. 客户端 (Client) ---
public class FactoryMethodDemo {
    public static void main(String[] args) {;
    // 客户端只需要关心所需的工厂，并使用抽象类型进行操作
    LoggerFactory factory = new FileLoggerFactory();
    Logger logger = factory.createLogger();
    logger.writeLog("System started.");
    // Output: LOG to File: System started.

    // 切换到数据库记录，只需要更改具体工厂类的实例化
    LoggerFactory dbFactory = new DatabaseLoggerFactory();
    Logger dbLogger = dbFactory.createLogger();
    dbLogger.writeLog("User logged in.");
    // Output: LOG to Database: User logged in.
}
}

```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **符合“开闭原则”**：引入新产品时，只需增加新的具体产品类和新的具体工厂类，**无须修改抽象工厂和现有工厂**，系统的可扩展性非常好。
2.  **封装创建细节**：向客户隐藏了哪种具体产品类将被实例化这一细节，用户只需关心所需产品对应的工厂。
3.  **多态性设计**：基于工厂和产品的多态性设计是关键，所有的具体工厂类都具有同一抽象父类。

### 4.2. 缺点

1.  **系统复杂度增加**：在添加新产品时，需要编写新的具体产品类，而且还要提供与之对应的具体工厂类。系统中类的个数将**成对增加**，增加了系统的抽象性和理解难度，并带来额外的开销。
2.  **抽象层引入**：在客户端代码中均使用抽象层进行定义，增加了系统的抽象性和理解难度。

## 5\. 适用环境与模式扩展

### 5.1. 适用环境

1.  **一个类不知道它所需要的对象的类**：客户端只需要知道所对应的工厂即可，具体的产品对象由具体工厂类创建。
2.  **一个类通过其子类来指定创建哪个对象**：利用多态性和里氏代换原则，在程序运行时，子类对象将覆盖父类对象，使得系统更容易扩展。
3.  **需要动态指定工厂**：将创建对象的任务委托给多个工厂子类中的某一个，客户端在使用时可以无须关心是哪一个工厂子类创建产品子类，需要时再动态指定（如通过配置文件）。

### 5.2. 模式扩展与退化

* **使用多个工厂方法**：抽象工厂角色中可以定义多个工厂方法，以满足对不同的产品对象的需求。
* **模式的退化**：
    * 如果工厂仅仅返回一个具体产品对象（即没有抽象产品或只有唯一的具体产品），工厂方法模式就发生了退化。
    * 当工厂等级结构中只有一个具体工厂类，且工厂方法被设计为**静态方法**时，工厂方法模式就**退化成简单工厂模式**。

### 5.3. 模式应用实例

* **JDBC (Java Database Connectivity)**：在 JDBC 中，`DriverManager` 类的 `getConnection()` 方法就是工厂方法模式的应用。它根据传入的 URL 动态选择并创建对应的 `Connection` 对象（具体产品）。
* **日志记录器**：如上例所示，用户可以动态选择记录到文件、数据库或远程服务器。
