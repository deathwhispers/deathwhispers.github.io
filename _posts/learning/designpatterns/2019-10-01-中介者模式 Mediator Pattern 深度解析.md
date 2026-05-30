---
layout: post
title: 中介者模式 (Mediator Pattern) 深度解析
author: deathwhispers
date: 2019-10-01
slug: design-pattern-mediator-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 🧑‍🤝‍🧑 中介者模式 (Mediator Pattern) 深度解析

## 1\. 模式动机：解决“蜘蛛网”式的复杂交互

在用户直接聊天的设计方案中，用户对象之间存在很强的关联性，将导致系统出现“蜘蛛网”式的复杂耦合结构。

* **系统结构复杂：** 对象间存在大量的相互关联和直接调用。若有一个对象发生变化，需要跟踪所有关联对象进行处理。
* **对象可重用性差：** 由于强关联，一个对象很难被另一个系统或模块重用，表现得像一个不可分割的整体。
* **系统扩展性低：** 增加新的对象需要调整原有相关对象上的引用，系统耦合度很高，扩展性差。

根据“单一职责原则”，对象应尽量细化。中介者模式正是为了解决这种**对象两两之间复杂的引用关系**，使系统成为一个**松耦合**
的星形结构。

## 2\. 模式定义

**中介者模式 (Mediator Pattern)** 定义：

> 用一个**中介对象**来封装一系列的**对象交互**。中介者使各对象不需要显式地相互引用，从而使其**耦合松散**，而且可以*
*独立地改变它们之间的交互**。

中介者模式又称为**调停者模式**，它是一种对象行为型模式。

## 3\. 模式结构与角色

| 角色名称                          | 职责描述                                            |
|:------------------------------|:------------------------------------------------|
| **Mediator** (抽象中介者)          | 定义一个接口，用于各同事对象之间的通信。                            |
| **ConcreteMediator** (具体中介者)  | 实现抽象接口，通过协调和封装同事对象的交互来实现协作行为。它了解并维护所有同事对象的引用。   |
| **Colleague** (抽象同事类)         | 定义同事对象的公有方法，并通常会引用一个中介者对象。                      |
| **ConcreteColleague** (具体同事类) | 抽象同事类的子类，是需要通过中介者进行通信的具体对象。它通过中介者间接完成与其他同事类的通信。 |

## 4\. 中介者的职责与原理分析

中介者承担了两个核心职责：

1. **中转作用（结构性）：** 各同事对象只需通过中介者即可通信，避免了显式引用其他同事。
2. **协调作用（行为性）：** 中介者封装了同事之间的协调逻辑，对同事的请求进行进一步处理。

通过引入中介者对象，可以将系统的网状结构变成以中介者为中心的**星形结构**。

### 时序图

## 5\. 代码示例（多语言）

### 5.1. C++ 示例 (聊天消息转发)

此示例展示了 `ConcreteColleagueA` 和 `ConcreteColleagueB` 如何通过 `ConcreteMediator` 进行消息转发，从而实现解耦。

**`main.cpp`**

```cpp
#include <iostream>
#include "ConcreteColleagueA.h"
#include "ConcreteMediator.h"
#include "ConcreteColleagueB.h"

using namespace std;

int main(int argc, char *argv[])
{
    ConcreteColleagueA * pa = new ConcreteColleagueA();
    ConcreteColleagueB * pb = new ConcreteColleagueB();
    ConcreteMediator * pm = new ConcreteMediator();

    // 注册同事对象
    pm->registered(1,pa);
    pm->registered(2,pb);

    // sendmsg from a to b
    pa->sendmsg(2,"hello,i am a");
    // sendmsg from b to a
    pb->sendmsg(1,"hello,i am b");

    delete pa;
    delete pb;
    delete pm; // 注意：实际应用中需要确保map中的Colleague对象也被正确管理和释放
    return 0;
}
```

**`ConcreteMediator.cpp` (核心实现)**

```cpp
// 引入必要的头文件...
#include "ConcreteMediator.h"
#include <map>
#include <iostream>
using namespace std;

// ... 构造函数和析构函数省略 ...

/**
 * @brief 中介者的核心操作：根据 nWho 查找同事并转发消息
 * @param nWho 目标同事的ID
 * @param str 要发送的消息
 */
void ConcreteMediator::operation(int nWho,string str){
    map<int,Colleague*>::const_iterator itr = m_mpColleague.find(nWho);
    if(itr == m_mpColleague.end())
    {
        cout << "not found this colleague!" << endl;
        return;
    }

    Colleague* pc = itr->second;
    pc->receivemsg(str); // 转发消息给目标同事
}

void ConcreteMediator::registered(int nWho,Colleague * aColleague){
    m_mpColleague.insert(make_pair(nWho,aColleague));
    // 同时将中介类暴露给colleague，建立双向引用（Colleague需知晓Mediator才能发送消息）
    aColleague->setMediator(this);
}
```

**`ConcreteColleagueA.cpp` (发送方实现)**

```cpp
// 引入必要的头文件...
#include "ConcreteColleagueA.h"
#include <iostream>
using namespace std;

// ... 构造函数和析构函数省略 ...

/**
 * @brief 发送消息，不直接引用其他同事，而是委托给中介者
 */
void ConcreteColleagueA::sendmsg(int toWho,string str){
    cout << "send msg from colleagueA,to:" << toWho << endl;
    // 核心：通过中介者进行操作
    m_pMediator->operation(toWho,str);
}

void ConcreteColleagueA::receivemsg(string str){
    cout << "ConcreteColleagueA reveivemsg:" << str <<endl;
}
```

### 5.2. Java 示例 (聊天室)

此示例使用 Java 语言实现一个虚拟聊天室，`ChatRoom` 作为具体中介者。

**`ChatRoom.java` (ConcreteMediator)**

```java
import java.util.Date;

public class ChatRoom {
    /**
    * 静态方法模拟消息转发和协调行为
    */
    public static void showMessage(User user, String message) {
        // 协调行为：增加时间戳、过滤等逻辑可以在此处实现
        String filteredMessage = message.replace("日", "*"); // 示例：过滤不雅字符
        System.out.println(new Date().toString()
        + " [" + user.getName() + "] : " + filteredMessage);
    }
}

```

**`User.java` (ConcreteColleague)**

```java
public class User {
    private String name;

    public User(String name) {
        this.name = name;
    }

public String getName() {
    return name;
}

public void sendMessage(String message) {
    // 核心：将消息发送（委托）给中介者
    ChatRoom.showMessage(this, message);
}
}

```

**`MediatorPatternDemo.java`**

```java
public class MediatorPatternDemo {
    public static void main(String[] args) {
        User robert = new User("Robert");
        User john = new User("John");

        robert.sendMessage("Hi! John!");
        john.sendMessage("Hello! Robert!");
        robert.sendMessage("今天天气真好日"); // 包含被过滤的字符
    }
}
```

### 5.3. Python 示例

此示例使用 Python 语言实现，结构清晰地展示了中介者和同事类的关系。

**`mediator_pattern.py`**

```python
class Mediator:
    """抽象中介者"""

    def notify(self, sender, event):
        pass

class ConcreteMediator(Mediator):
    """具体中介者：协调同事之间的交互"""

    def __init__(self, c1, c2):
        self.colleague1 = c1
        self.colleague1.mediator = self
        self.colleague2 = c2
        self.colleague2.mediator = self

    def notify(self, sender, event):
        if sender == self.colleague1 and event == "A":
            print("Mediator reacts to A and triggers B's action.")
            self.colleague2.do_b()
        elif sender == self.colleague2 and event == "D":
            print("Mediator reacts to D and triggers A's action.")
            self.colleague1.do_c()

class Colleague:
    """抽象同事类"""

    def __init__(self, mediator=None):
        self.mediator = mediator

class ConcreteColleague1(Colleague):
    """具体同事类 1"""

    def do_a(self):
        print("Colleague 1 does A.")
        # 委托给中介者
        self.mediator.notify(self, "A")

    def do_c(self):
        print("Colleague 1 does C.")

class ConcreteColleague2(Colleague):
    """具体同事类 2"""

    def do_b(self):
        print("Colleague 2 does B.")

    def do_d(self):
        print("Colleague 2 does D.")
        # 委托给中介者
        self.mediator.notify(self, "D")

# 客户端代码
c1 = ConcreteColleague1()
c2 = ConcreteColleague2()
mediator = ConcreteMediator(c1, c2)

print("Client triggers Colleague 1's action:")
c1.do_a()

print("\nClient triggers Colleague 2's action:")
c2.do_d()
```

## 6\. 模式应用、优缺点与总结

### 6.1. 模式应用

* **MVC 架构：** Controller（控制器）作为 Model（模型）和 View（视图）之间的中介者。
* **机场调度系统：** 塔台充当各飞机之间的中介者。
* **GUI 开发：** 在复杂的界面中，中介者类负责协调多个界面组件（同事类）之间的交互关系。

### 6.2. 优缺点

| 优点 (Benefits)                                     | 缺点 (Drawbacks)                                    |
|:--------------------------------------------------|:--------------------------------------------------|
| **简化交互与解耦：** 将复杂的网状引用关系转化为星形结构，各同事对象彼此解耦，只依赖于中介者。 | **中介者复杂化：** 所有的交互逻辑都集中在具体中介者类中，可能导致它非常庞大和复杂，难以维护。 |
| **符合迪米特法则：** 减少了对象之间直接引用的数目。                      |                                                   |
| **提高复用性/扩展性：** 改变交互行为只需修改或增加中介者类。                 |                                                   |

### 6.3. 适用环境

* 系统中对象之间存在**复杂的引用关系**，相互依赖关系结构混乱且难以理解。
* 一个对象直接引用并与其他**很多对象通信**，导致难以复用该对象。
* 想通过一个**中间类来封装多个类中的行为**，从而集中管理和控制这些交互。

**总结：** 中介者模式通过引入一个中介者对象，成功地将同事对象之间的网状耦合关系解开，转化为以中介者为中心的松耦合星形结构，简化了对象间的交互，是迪米特法则的典型应用。
