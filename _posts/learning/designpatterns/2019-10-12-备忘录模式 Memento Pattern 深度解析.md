---
layout: post
title: 备忘录模式 (Memento Pattern) 深度解析
author: deathwhispers
date: 2019-10-12
slug: design-pattern-memento-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 📝 备忘录模式 (Memento Pattern) 深度解析

## 🚀 1. 模式意图与动机 (Intention & Motivation)

### 意图

> **备忘录模式 (Memento Pattern)：** 在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态。这样以后就可以将该对象恢复到原先保存的状态。

### 动机

在软件应用中，我们经常需要提供“撤销 (Undo)”、“回滚 (Rollback)”或“存档 (Save)”等功能。这意味着我们需要在特定时间点**保存对象的状态**，并在需要时**恢复**到该状态。

如果直接访问对象内部状态并保存，会**破坏对象的封装性**。备忘录模式通过引入一个**备忘录对象 (Memento)** 来专门存储状态，将状态的保存细节隐藏在发起人内部，从而实现状态的捕获和恢复，同时保持了良好的封装性。

## 🏗️ 2. 模式核心角色与结构

备忘录模式涉及以下三个核心角色：

| 角色 | 英文名称 | 职责描述 |
| :--- | :--- | :--- |
| **发起人** | Originator | 需要保存自身状态的对象。它负责创建**备忘录**来保存当前状态，并使用**备忘录**来恢复到以前的状态。 |
| **备忘录** | Memento | 存储发起人某一时刻的内部状态。它是一个被动的数据容器，**不应该暴露给外部**（即管理者）。 |
| **管理者** | CareTaker | 负责保存和管理**备忘录**对象。它永远不会检查备忘录的内容，只负责存储和按需提供备忘录。 |

### 模式结构图

## 💻 3. 代码示例：游戏存档/状态回滚 (Java/Python)

我们将使用一个简单的**状态机 (Originator)** 来演示如何通过**备忘录模式**实现状态的保存和恢复。

### 📌 Java 实现

```java
// 1. 备忘录 (Memento)：存储发起人的状态
public class Memento {
   private String state; // 内部状态

   public Memento(String state){
      this.state = state;
   }

   // 供发起人恢复状态时使用
   public String getState(){
      return state;
   }
   // 注意：备忘录通常只有发起人可以完全访问其状态
}

// 2. 发起人 (Originator)：创建和使用备忘录
public class Originator {
   private String state; // 需要保存的内部状态

   public void setState(String state){
      this.state = state;
   }
   public String getState(){
      return state;
   }

   // 创建备忘录：保存当前状态
   public Memento saveStateToMemento(){
      return new Memento(state);
   }

   // 恢复状态：从备忘录中获取状态
   public void getStateFromMemento(Memento Memento){
      state = Memento.getState();
   }
}

// 3. 管理者 (CareTaker)：管理备忘录列表
import java.util.ArrayList;
import java.util.List;

public class CareTaker {
   private List<Memento> mementoList = new ArrayList<Memento>();

   // 保存备忘录
   public void add(Memento state){
      mementoList.add(state);
   }

   // 获取备忘录
   public Memento get(int index){
      return mementoList.get(index);
   }
}

// 4. 客户端演示
public class MementoPatternDemo {
   public static void main(String[] args) {
      Originator originator = new Originator();
      CareTaker careTaker = new CareTaker();

      originator.setState("State #1");
      originator.setState("State #2");
      // 第一次存档：保存 State #2
      careTaker.add(originator.saveStateToMemento());

      originator.setState("State #3");
      // 第二次存档：保存 State #3
      careTaker.add(originator.saveStateToMemento());

      originator.setState("State #4");
      System.out.println("Current State: " + originator.getState()); // State #4

      // 恢复到第一次存档 (State #2)
      originator.getStateFromMemento(careTaker.get(0));
      System.out.println("First saved State: " + originator.getState()); // State #2

      // 恢复到第二次存档 (State #3)
      originator.getStateFromMemento(careTaker.get(1));
      System.out.println("Second saved State: " + originator.getState()); // State #3
   }
}
```

### 📌 Python 实现

Python 中通常使用**内部类**或**命名元组**来实现备忘录，以限制对状态的访问。

```python
# 1. 发起人 (Originator)
class Originator:
    def __init__(self):
        self._state = ""

    def set_state(self, state):
        print(f"Originator: Setting state to {state}")
        self._state = state

    def get_state(self):
        return self._state

    # 内部类作为 Memento，确保只有 Originator 知道 Memento 的结构
    class Memento:
        def __init__(self, state):
            self._state = state

        # 仅供 Originator 内部恢复时访问
        def get_saved_state(self):
            return self._state

    # 创建备忘录
    def save_state_to_memento(self):
        return self.Memento(self._state)

    # 恢复状态
    def get_state_from_memento(self, memento):
        self._state = memento.get_saved_state()

# 2. 管理者 (CareTaker)
class CareTaker:
    def __init__(self):
        self._memento_list = []

    def add(self, memento):
        self._memento_list.append(memento)

    def get(self, index):
        return self._memento_list[index]

# 3. 客户端演示
if __name__ == "__main__":
    originator = Originator()
    caretaker = CareTaker()

    originator.set_state("State #1")
    originator.set_state("State #2")
    caretaker.add(originator.save_state_to_memento()) # 存档 0: State #2

    originator.set_state("State #3")
    caretaker.add(originator.save_state_to_memento()) # 存档 1: State #3

    originator.set_state("State #4")
    print(f"\nCurrent State: {originator.get_state()}") # State #4

    # 恢复到存档 0
    originator.get_state_from_memento(caretaker.get(0))
    print(f"First saved State: {originator.get_state()}") # State #2

    # 恢复到存档 1
    originator.get_state_from_memento(caretaker.get(1))
    print(f"Second saved State: {originator.get_state()}") # State #3
```

## ✅ 4. 优点与缺点

### 👍 优点

* **状态恢复机制:** 提供了一种方便的机制，使用户能够比较方便地回到某个历史状态（“后悔药”）。
* **封装性保护:** 发起人将状态封装在备忘录对象中，外部（管理者）不知道发起人内部的细节，符合**迪米特原则**。
* **简化发起人:** 管理者负责备忘录的存储和生命周期，减轻了发起人的责任。

### 👎 缺点

* **资源消耗:** 如果需要保存的状态信息过多（即发起人包含的成员变量过多），或者保存的频率很高，会占用大量的内存和资源。
* **性能影响:** 创建和存储备忘录对象本身需要时间，可能对系统性能造成一定影响。

## 🌐 5. 适用场景 (Applicability)

在以下情况下可以使用备忘录模式：

1.  需要提供**保存和恢复**数据的相关状态的场景（如编辑器的 **Ctrl+Z** 撤销功能、游戏存档）。
2.  需要提供一个**可回滚 (rollback)** 的操作，允许用户取消不确定或错误的操作。
3.  涉及到**事务管理**的场景，例如数据库连接的事务，可以在执行操作前保存状态，失败时回滚。

### 注意事项

* 为了节约内存，如果状态对象非常庞大，可以考虑结合**原型模式**来创建状态副本，或者只存储**增量变化**而不是完整的状态。
