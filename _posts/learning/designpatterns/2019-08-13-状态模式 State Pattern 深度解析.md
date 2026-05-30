---
layout: post
title: 状态模式 (State Pattern) 深度解析
author: deathwhispers
date: 2019-08-13
slug: design-pattern-state-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🚦 状态模式 (State Pattern) 深度解析

## 1\. 模式动机与定义

### 1.1. 模式动机：对象的行为依赖于动态变化的状态

在许多软件系统中，一个对象的行为取决于其内部的**一个或多个动态变化的属性**，这些属性被称为**状态 (State)**。当对象与外部事件互动时，其内部状态会改变，从而导致系统的行为也随之发生变化。

* **问题**：传统的做法是使用大量的 `if...else` 或 `switch` 条件语句来判断当前状态，并在语句块中实现相应的行为和状态转换逻辑。
    * 随着状态和行为的增加，条件语句块会变得**巨大且难以维护**。
    * 难以方便地增加或删除状态，违背“开闭原则”。
    * 客户类与类库之间的耦合增强。
* **解决方案**：将**所有与某个状态有关的行为**封装到一个独立的类中（具体状态类），环境类（Context）持有当前状态的引用。当状态改变时，环境类切换其内部引用的状态对象，从而改变其行为。

### 1.2. 模式定义

**状态模式 (State Pattern)**：

> **允许一个对象在其内部状态改变时改变它的行为，对象看起来似乎修改了它的类。**

其别名为**状态对象 (Objects for States)**，属于**对象行为型模式**。

## 2\. 模式结构与角色

状态模式将状态相关的行为委托给具体的状态对象处理。

| 角色名称 | 职责描述 | 对应到实例 |
| :--- | :--- | :--- |
| **Context** (环境类/上下文) | 拥有状态的对象，维护一个 `State` 抽象状态的实例，这个实例定义当前状态。它将与状态相关的行为委托给当前状态对象处理。 | `TCPConnection`, `Player` |
| **State** (抽象状态类) | 定义一个接口，用于**封装与环境类的一个特定状态相关的行为**。 | `TCPState`, `PlayerState` |
| **ConcreteState** (具体状态类) | 抽象状态类的子类，**实现一个与环境类的一个状态相关的行为**。负责处理该状态下的行为，并决定是否以及如何进行状态转换。 | `ListeningState`, `StartState` |

### 2.1. 模式分析核心

* **状态行为封装**：将与某个状态相关的行为和状态转换逻辑都封装到对应的 `ConcreteState` 类中。
* **消除条件语句**：状态模式用**多态**代替了客户端或环境类中**巨大的条件语句块**。
* **状态切换**：状态的切换逻辑通常发生在 `ConcreteState` 类的 `handle()` 方法内部，通过调用 `Context` 的 `changeState()` 或 `setState()` 方法实现。

## 3\. 代码深度解析（音乐播放器）

我们以一个简单的**音乐播放器**为例，其状态可以从 `Stopped` 切换到 `Playing`。

### 3.1. Java 代码示例

```java
// --- 1. 抽象状态类 (State) ---
public interface PlayerState {
    void handlePlayPause(Context context);
    void handleStop(Context context);
}

// --- 2. 具体状态类 A: 停止状态 (StoppedState) ---
public class StoppedState implements PlayerState {
    @Override
    public void handlePlayPause(Context context) {
        System.out.println("-> 播放中。");
        // 状态转换：从 Stopped -> Playing
        context.setState(new PlayingState());
    }
    @Override
    public void handleStop(Context context) {
        System.out.println("已经停止，无需操作。");
    }
    @Override
    public String toString() {
        return "Stopped";
    }
}

// --- 3. 具体状态类 B: 播放状态 (PlayingState) ---
public class PlayingState implements PlayerState {
    @Override
    public void handlePlayPause(Context context) {
        System.out.println("-> 暂停。");
        // 状态转换：从 Playing -> Stopped
        context.setState(new StoppedState());
    }
    @Override
    public void handleStop(Context context) {
        System.out.println("-> 停止播放。");
        // 状态转换：从 Playing -> Stopped
        context.setState(new StoppedState());
    }
    @Override
    public String toString() {
        return "Playing";
    }
}

// --- 4. 环境类 (Context) ---
public class Context {
    private PlayerState currentState;

    public Context() {
        // 设置初始状态
        this.currentState = new StoppedState();
        System.out.println("Initial State: " + currentState);
    }

    public void setState(PlayerState newState) {
        this.currentState = newState;
        System.out.println("State Changed to: " + newState);
    }

    // 委托给当前状态对象处理
    public void pressPlayPause() {
        System.out.print("Current State [" + currentState + "]: ");
        currentState.handlePlayPause(this);
    }
    public void pressStop() {
        System.out.print("Current State [" + currentState + "]: ");
        currentState.handleStop(this);
    }
}

// --- 5. 客户端调用 (Client) ---
public class StatePatternDemo {
    public static void main(String[] args) {
        Context player = new Context();

        player.pressPlayPause(); // Stopped -> Playing
        player.pressPlayPause(); // Playing -> Stopped (Pause)
        player.pressPlayPause(); // Stopped -> Playing
        player.pressStop();      // Playing -> Stopped
    }
}



```

### 3.2. Python 代码示例

```python
from abc import ABC, abstractmethod

# --- 1. 抽象状态类 (State) ---
class PlayerState(ABC):
    @abstractmethod
    def play_pause(self, context):
        pass

    @abstractmethod
    def stop(self, context):
        pass

# --- 2. 具体状态类 (ConcreteState) ---
class StoppedState(PlayerState):
    def play_pause(self, context):
        print("-> 播放音乐。")
        context.state = PlayingState()
        context.log_state_change()

    def stop(self, context):
        print("已经停止。")

class PlayingState(PlayerState):
    def play_pause(self, context):
        print("-> 暂停播放。")
        context.state = StoppedState()
        context.log_state_change()

    def stop(self, context):
        print("-> 停止播放。")
        context.state = StoppedState()
        context.log_state_change()

# --- 3. 环境类 (Context) ---
class Context:
    def __init__(self):
        # 初始状态
        self._state = StoppedState()
        self.log_state_change()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def log_state_change(self):
        print(f"[Context]: State changed to {self._state.__class__.__name__}")

    # 委托方法
    def press_play_pause(self):
        self._state.play_pause(self)

    def press_stop(self):
        self._state.stop(self)

# --- 4. 客户端调用 (Client) ---
if __name__ == "__main__":
    player = Context()

    print("\n--- Interaction 1 ---")
    player.press_play_pause() # Stopped -> Playing

    print("\n--- Interaction 2 ---")
    player.press_play_pause() # Playing -> Stopped

    print("\n--- Interaction 3 ---")
    player.press_stop()       # Already Stopped, no change.
```

## 4\. 模式优点与缺点

### 4.1. 优点

1.  **封装转换规则**：将所有与某个状态有关的行为和转换逻辑封装到一个类中，使得环境类（Context）的代码更简洁。
2.  **消除条件语句**：用**多态**代替了庞大的 `if/else` 或 `switch` 语句块，提高了代码的可维护性和可读性。
3.  **方便增加新状态**：只需增加新的具体状态类即可增加新的状态行为。
4.  **状态共享**：可以让多个环境对象共享一个状态对象（如果状态对象是无状态的，可设计为单例），减少系统中对象的个数。

### 4.2. 缺点

1.  **类数量增加**：状态模式的使用必然会增加系统类和对象的个数，使系统结构更加复杂。
2.  **“开闭原则”支持不佳（针对可切换状态）**：对于**可切换状态**的状态模式，增加新的状态类通常需要修改**其他**负责状态转换的源代码（即在现有状态类中增加指向新状态的转换逻辑），因此对“开闭原则”的支持并不理想。

## 5\. 适用环境

1.  **对象的行为依赖于它的状态**（属性），并且可以根据它的状态改变而改变它的相关行为（例如权限管理、工作流、TCP连接状态）。
2.  **代码中包含大量与对象状态有关的条件语句**，导致代码的可维护性和灵活性变差，需要用多态结构替换。
3.  行为随状态改变而改变的场景，它是**条件、分支判断语句的替代者**。
