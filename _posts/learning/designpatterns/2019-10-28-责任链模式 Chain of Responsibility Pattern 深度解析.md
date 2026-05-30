---
layout: post
title: 责任链模式 (Chain of Responsibility Pattern) 深度解析
author: deathwhispers
date: 2019-10-28
slug: design-pattern-chain-of-responsibility-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 📝 责任链模式 (Chain of Responsibility Pattern) 深度解析

## 🚀 1. 模式意图与动机 (Intention & Motivation)

### 意图

> **责任链模式 (Chain of Responsibility Pattern)：** 使多个对象都有机会处理请求，从而避免了请求的发送者和接收者之间的耦合关系。将这些对象连成一条链，并沿着这条链传递该请求，直到有对象处理它为止。

### 动机

在软件设计中，有时一个请求可能有多种处理方式，或者需要经过一系列的预处理才能最终完成。如果直接让发送者知道所有可能的接收者，会导致发送者与接收者之间的**紧密耦合**。

责任链模式通过建立一个**处理者对象链 (Chain)**，将请求发送给链上的第一个处理者。每个处理者要么处理请求，要么将其转发给链上的下一个处理者，从而实现：

1.  **解耦:** 请求的发送者不需要知道哪个对象将处理其请求，也不需要知道链的结构。
2.  **灵活性:** 责任链的成员和顺序可以动态调整。

## 🏗️ 2. 模式结构与角色 (Structure & Roles)

责任链模式包含以下核心角色：

1.  **Handler (抽象处理者):**
    * 定义一个处理请求的接口。
    * 实现/聚合一个指向链中下一个处理者的引用（`nextHandler`）。
    * 通常包含处理请求的抽象方法和转发请求的模板方法。
2.  **ConcreteHandler (具体处理者):**
    * 实现抽象处理者的处理方法。
    * 判断自己是否能处理该请求。如果能，则处理；如果不能，则转发给下一个处理者。
3.  **Client (客户端):**
    * 创建并配置责任链（设置第一个处理者和后续链接）。
    * 将请求发送给链上的第一个处理者。

### 核心机制

在抽象处理者（`Handler`）中，通常包含一个核心的模板方法：

```java
// 抽象处理者中的核心逻辑（伪代码）
public final Response handleMessage(Request request){
    Response response = null;
    if(this.canHandle(request)){ // 1. 判断是否是自己的处理级别/条件
    response = this.echo(request);
}else{
    if(this.nextHandler != null){ // 2. 转发给下一个处理者
    response = this.nextHandler.handleMessage(request);
}else{
    // 3. 链尾处理（如抛出异常或默认处理）
}
}
return response;
}



```

## 💻 3. 代码示例：日志记录链 (Java/Python)

我们将使用**日志记录系统**作为示例，其中不同级别的消息（INFO, DEBUG, ERROR）由不同的处理者（控制台、文件、错误日志）负责记录。

### 📌 Java 实现

```java
// 1. 抽象处理者：AbstractLogger
public abstract class AbstractLogger {
    public static int INFO = 1;
    public static int DEBUG = 2;
    public static int ERROR = 3;

    protected int level; // 本处理者能处理的最低级别
    protected AbstractLogger nextLogger; // 责任链中的下一个元素

    // 设置下一个处理者
    public void setNextLogger(AbstractLogger nextLogger){
        this.nextLogger = nextLogger;
    }

    // 核心的请求处理/转发方法
    public void logMessage(int level, String message){
        if(this.level <= level){
            // 如果当前处理者能够处理该级别的消息
            write(message);
        }
        // 不管当前处理者是否处理，都传递给下一个处理者
        if(nextLogger !=null){
            nextLogger.logMessage(level, message);
        }
    }

    // 具体处理任务的抽象方法
    abstract protected void write(String message);
}

// 2. 具体处理者：ConsoleLogger
public class ConsoleLogger extends AbstractLogger {
    public ConsoleLogger(int level){
        this.level = level;
    }
    @Override
    protected void write(String message) {
        System.out.println("Standard Console::Logger: " + message);
    }
}

// 3. 具体处理者：ErrorLogger
public class ErrorLogger extends AbstractLogger {
    // ... 构造函数类似 ConsoleLogger ...
    public ErrorLogger(int level){
        this.level = level;
    }
    @Override
    protected void write(String message) {
        System.out.println("Error Console::Logger: " + message);
    }
}

// 4. 客户端配置与调用
public class ChainPatternDemo {
    private static AbstractLogger getChainOfLoggers(){
        // ERRORLogger (3) -> FileLogger (2) -> ConsoleLogger (1)
        AbstractLogger errorLogger = new ErrorLogger(AbstractLogger.ERROR);
        AbstractLogger fileLogger = new FileLogger(AbstractLogger.DEBUG);
        AbstractLogger consoleLogger = new ConsoleLogger(AbstractLogger.INFO);

        errorLogger.setNextLogger(fileLogger);
        fileLogger.setNextLogger(consoleLogger);
        // 从链头开始
        return errorLogger;
    }

    public static void main(String[] args) {
        AbstractLogger loggerChain = getChainOfLoggers();

        // 消息级别：INFO (1)
        loggerChain.logMessage(AbstractLogger.INFO, "This is an information.");
        // 消息级别：DEBUG (2)
        loggerChain.logMessage(AbstractLogger.DEBUG, "This is a debug level information.");
        // 消息级别：ERROR (3)
        loggerChain.logMessage(AbstractLogger.ERROR, "This is an error information.");
    }
}



```

**运行结果分析:**
在本实现中，由于每个处理者在处理完请求后，**都会**继续将请求传递给下一个（`if(nextLogger !=null)`），所以消息会被所有满足条件的日志器处理：

1.  INFO (1): 被 ConsoleLogger (1) 处理。
2.  DEBUG (2): 被 FileLogger (2) 和 ConsoleLogger (1) 处理。
3.  ERROR (3): 被 ErrorLogger (3), FileLogger (2), 和 ConsoleLogger (1) 处理。

<!-- end list -->

```
Standard Console::Logger: This is an information.
File::Logger: This is a debug level information.
Standard Console::Logger: This is a debug level information.
Error Console::Logger: This is an error information.
File::Logger: This is an error information.
Standard Console::Logger: This is an error information.
```

### 📌 Python 实现

Python 中使用**抽象基类 (ABC)** 定义抽象处理者，并利用组合实现责任链。

```python
from abc import ABC, abstractmethod

# 级别常量
INFO, DEBUG, ERROR = 1, 2, 3

# 1. 抽象处理者：AbstractLogger
class AbstractLogger(ABC):
    def __init__(self, level):
        self.level = level
        self.next_logger = None

    def set_next_logger(self, next_logger):
        self.next_logger = next_logger

    def log_message(self, level, message):
        if self.level <= level:
            self.write(message)

        # 转发请求
        if self.next_logger is not None:
            self.next_logger.log_message(level, message)

    @abstractmethod
    def write(self, message):
        pass

# 2. 具体处理者：ConsoleLogger
class ConsoleLogger(AbstractLogger):
    def write(self, message):
        print(f"Standard Console::Logger: {message}")

# 3. 具体处理者：FileLogger
class FileLogger(AbstractLogger):
    def write(self, message):
        print(f"File::Logger: {message}")

# 4. 具体处理者：ErrorLogger
class ErrorLogger(AbstractLogger):
    def write(self, message):
        print(f"Error Console::Logger: {message}")

# 5. 客户端配置与调用
def get_chain_of_loggers():
    error_logger = ErrorLogger(ERROR)
    file_logger = FileLogger(DEBUG)
    console_logger = ConsoleLogger(INFO)

    error_logger.set_next_logger(file_logger)
    file_logger.set_next_logger(console_logger)
    return error_logger # 返回链头

if __name__ == "__main__":
    logger_chain = get_chain_of_loggers()

    print("--- INFO Message (1) ---")
    logger_chain.log_message(INFO, "This is an information.")

    print("\n--- DEBUG Message (2) ---")
    logger_chain.log_message(DEBUG, "This is a debug level information.")

    print("\n--- ERROR Message (3) ---")
    logger_chain.log_message(ERROR, "This is an error information.")
```

## ✅ 4. 优点与缺点

### 👍 优点

* **降低耦合度:** 请求的发送者和接收者完全解耦。发送者只需将请求发送到链上，不关心具体由谁处理。
* **简化对象:** 接收者对象只需知道链中的下一个处理者，不需要知道整个链的结构。
* **增强灵活性:** 可以通过改变链内的成员或调动它们的次序，**动态地**新增或删除责任。
* **符合开闭原则:** 增加新的处理者类非常方便，只需继承抽象处理者并插入链中，无需修改现有代码。

### 👎 缺点

* **性能影响:** 请求在链中传递，性能会受到一定影响，尤其当链条过长时。
* **不保证接收:** 无法保证请求一定会被链中的某个处理者接收和处理。如果设计不当，请求可能到达链尾仍未被处理。
* **调试不便:** 运行时特征不容易观察，在进行代码调试时，跟踪请求的流动路径可能比较复杂。

## 🌐 5. 适用场景 (Applicability)

在以下情况下可以考虑使用责任链模式：

1.  有**多个对象**可以处理同一个请求，但具体哪个对象处理应由**运行时刻**自动确定。
2.  想要在**不明确指定接收者**的情况下，向多个对象中的一个提交一个请求（解耦发送者和接收者）。
3.  需要**动态地指定**一组对象处理请求，或者希望请求按特定顺序通过一系列预处理步骤。

-----

责任链模式在实际应用中非常广泛，例如 Web 框架中的**过滤器 (Filter)**、**拦截器 (Interceptor)**，以及像 Java Servlet 规范中的 `Filter` 链、日志框架（如 Log4j/Slf4j）中的 `Appender` 链等。

如果您对如何在特定应用场景（如审批流程或事件处理）中应用责任链模式感兴趣，请告诉我！
