---
layout: post
title: 命令模式 (Command Pattern) 深度解析
author: deathwhispers
date: 2019-10-25
slug: design-pattern-command-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 命令模式 (Command Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：解耦请求的发送者与接收者

在软件设计中，我们经常需要向某些对象发送请求，但并**不清楚请求的接收者是谁**，也**不知道被请求的具体操作是哪个**。我们只需要在运行时指定具体的请求接收者即可。

命令模式的引入，使得**请求发送者与请求接收者消除彼此之间的耦合**，让对象之间的调用关系更加灵活。发送请求的对象只需要知道如何发送请求，而不必知道如何完成请求。

### 1.2. 模式定义

**命令模式 (Command Pattern)**：

> 将一个**请求封装为一个对象**，从而使我们可用不同的请求对客户进行参数化；对请求排队或者记录请求日志，以及支持可撤销的操作。

命令模式是一种**对象行为型模式**，其别名为**动作 (Action) 模式**或**事务 (Transaction) 模式**。

## 2\. 模式结构与角色

命令模式的本质是对命令进行封装，将发出命令的责任和执行命令的责任分割开。

### 2.1. 模式角色

| 角色名称 | 职责描述 |
| :--- | :--- |
| **Command** (抽象命令类) | 定义一个抽象接口，用于声明执行请求的 `execute()` 等方法。 |
| **ConcreteCommand** (具体命令类) | 实现了抽象命令接口，**持有对 Receiver 对象的引用**，负责调用接收者对象的对应动作，将接收者对象的动作绑定其中。 |
| **Receiver** (接收者角色) | **执行与请求相关的操作**，它具体实现对请求的业务处理（干活的角色）。 |
| **Invoker** (调用者/请求者角色) | **请求的发送者**，它通过命令对象来执行请求。它不知道哪个具体命令被执行，只针对抽象命令接口编程。 |
| **Client** (客户类) | 负责创建具体命令对象，并指定其接收者，然后将具体命令对象设置给调用者。 |

### 2.2. 模式结构图

### 2.3. 模式分析核心

* **解耦**：发送者 (`Invoker`) 只针对**抽象命令接口** (`Command`) 编程，不关心具体的**接收者** (`Receiver`) 或执行细节。
* **请求对象化**：命令模式使请求本身成为一个对象，这个对象可以像其他对象一样被**存储**（例如放入队列）、**传递**和**操作**（例如 `Undo` 和 `Redo`）。

## 3\. 代码深度解析（多语言实现）

我们以**电视机遥控器**为例（**Invoker** 是遥控器，**Receiver** 是电视机，**Command** 是按钮操作）。

### 3.1. Java 代码示例 (电视机遥控器)

```java
// 1. 接收者 (Receiver)
public class Television {
    public void turnOn() {;
    System.out.println("Television: The TV is ON!");
}
public void turnOff() {;
System.out.println("Television: The TV is OFF!");
}
public void changeChannel() {;
System.out.println("Television: Channel switched.");
}
}

// 2. 抽象命令类 (Command)
public interface Command {
    void execute();
    // 可选：void undo(); // 用于支持撤销操作
}

// 3. 具体命令类 (ConcreteCommand) - 打开电视
public class TurnOnCommand implements Command {
    private Television tv; // 包含对接收者的引用

    public TurnOnCommand(Television tv) {;
    this.tv = tv;
}

@Override
public void execute() {;
tv.turnOn(); // 将请求转发给接收者
}
}
// 更多命令类如 TurnOffCommand, ChangeChannelCommand 略

// 4. 调用者 (Invoker) - 遥控器
public class RemoteControl {
    private Command command;

    public void setCommand(Command command) {;
    this.command = command;
}

public void pressButton() {;
System.out.println("RemoteControl: Button pressed.");
command.execute();
}
}

// 5. 客户端 (Client)
public class CommandDemo {
    public static void main(String[] args) {;
    // 创建接收者
    Television myTV = new Television();

    // 创建具体命令，并将接收者绑定到命令上
    Command onCommand = new TurnOnCommand(myTV);

    // 创建调用者
    RemoteControl remote = new RemoteControl();

    // 将命令设置给调用者
    remote.setCommand(onCommand);

    // 发送请求，实际执行的动作由命令对象封装
    remote.pressButton();

    // 动态更换命令
    Command offCommand = new TurnOffCommand(myTV); // 略去 TurnOffCommand 实现
    remote.setCommand(offCommand);
    remote.pressButton();
}
}


```

### 3.2. Python 代码示例 (队列和宏命令)

此示例展示了如何将命令放入队列，并实现一个**宏命令** (MacroCommand)。

```python
# 1. 接收者 (Receiver)
class Light:
    def on(self):
        print("Light is ON")
    def off(self):
        print("Light is OFF")

# 2. 抽象命令类 (Command)
class Command:
    def execute(self):
        raise NotImplementedError

# 3. 具体命令类 (ConcreteCommand)
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.on()

class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.off()

# 4. 调用者 (Invoker) - 支持排队 (宏命令)
class MacroCommand(Command):
    """一个包含多个命令的宏命令（组合命令）"""
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute(self):
        print("\n--- Executing Macro Command ---")
        for command in self.commands:
            command.execute()
        print("--- Macro Command Finished ---")

# 5. 客户端
if __name__ == "__main__":
    kitchen_light = Light()

    # 单独命令
    cmd_on = LightOnCommand(kitchen_light)
    cmd_off = LightOffCommand(kitchen_light)

    # 创建宏命令
    party_macro = MacroCommand()
    party_macro.add_command(cmd_on)
    party_macro.add_command(cmd_off)
    party_macro.add_command(cmd_on)

    # Invoker (MacroCommand 自身就是一个 Invoker)
    party_macro.execute()
```

## 4\. 模式分析与扩展

### 4.1. 优点

1.  **降低系统耦合度**：请求调用者和请求接收者解耦，彼此不直接交互。
2.  **易于扩展**：新的命令可以很容易地加入到系统中，符合“开放-封闭原则”。
3.  **易于实现复杂功能**：可以比较容易地设计一个**命令队列**和**宏命令**（组合命令）。
4.  **支持可撤销操作 (Undo/Redo)**：通过在命令对象中保存执行前的状态，并实现 `undo()` 方法，可以方便地实现撤销和恢复功能。

### 4.2. 缺点

* **过多的具体命令类**：针对每一个命令都需要设计一个具体命令类，因此某些系统可能需要大量具体命令类，这将影响命令模式的使用。

### 4.3. 模式扩展：宏命令 (组合命令)

* **宏命令**：又称为组合命令，它是**命令模式**和**组合模式**联用的产物。
* **实现原理**：宏命令本身也是一个**具体命令**，但它内部包含了对其他命令对象的引用（列表）。在调用宏命令的 `execute()` 方法时，将递归调用它所包含的每个成员命令的 `execute()` 方法，实现对命令的批处理。

### 4.4. 适用环境

1.  系统需要将请求调用者和请求接收者解耦。
2.  系统需要在不同的时间指定请求、将请求排队和执行请求（如任务调度、消息队列）。
3.  系统需要支持命令的**撤销 (Undo)** 和**恢复 (Redo)** 操作（如文本编辑器）。
4.  系统需要将一组操作组合在一起，即支持**宏命令**（如 Shell 脚本、游戏连招）。
