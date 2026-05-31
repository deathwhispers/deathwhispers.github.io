---
layout: post
title: 适配器模式 (Adapter Pattern) 深度解析
author: deathwhispers
date: 2019-11-09
slug: design-pattern-adapter-pattern
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 📝 适配器模式 (Adapter Pattern) 深度解析

## 🚀 1. 模式动机 (Motivation)

在软件开发中，我们常常遇到这样的情况：**现有的类**已经实现了所需的功能，但它提供的**接口**（方法名、参数等）与**客户端期望的接口**不兼容，导致客户端无法直接使用。

**适配器模式**的设计灵感来源于现实中的**电源适配器**或**读卡器**：

* 它定义一个**包装类（适配器 Adapter）**，去包装那个接口不兼容的**现有类（适配配者 Adaptee）**。
* 适配器对外提供客户端期望的**目标接口 (Target)**。
* 在适配器内部，将客户端的请求**转换**为对适配者相应方法的调用。

这一过程对客户端是透明的，从而使得原本接口不兼容的类能够一起工作，实现了对现有代码的**重用**，同时遵循\*\*"开放-封闭原则"\*\*（对修改关闭，对扩展开放）。

## 💡 2. 模式定义 (Definition)

> **适配器模式 (Adapter Pattern)：** 将一个类的接口转换成客户希望的另一个接口，使原本接口不兼容的那些类可以一起工作。其别名为**包装器 (Wrapper)**。

适配器模式是一种**结构型模式**，主要用于解决新环境与现有对象接口不匹配的问题。

## 🏗️ 3. 模式结构 (Structure)

适配器模式包含以下四个核心角色：

1.  **Target (目标抽象类/接口):** 定义客户端期望使用的接口。
2.  **Adaptee (适配者类):** 已经存在的、需要被适配的类。它的接口与目标接口不兼容。
3.  **Adapter (适配器类):** 模式的核心。它实现 **Target** 接口，并持有或继承 **Adaptee**，将 **Target** 接口的调用转换为对 **Adaptee** 相应方法的调用。
4.  **Client (客户类):** 直接与 **Target** 接口交互的类。

适配器模式主要有两种实现方式：**对象适配器**和**类适配器**。

| 特性 | 对象适配器 | 类适配器 |
| :--- | :--- | :--- |
| **实现方式** | **组合/委派** (Adapter 包含 Adaptee 实例) | **多重继承** (Adapter 继承 Adaptee 和 Target) |
| **关系** | Adapter 与 Adaptee 是**组合**关系。 | Adapter 与 Adaptee 是**继承**关系。 |
| **灵活性** | 更灵活，一个 Adapter 可适配 Adaptee 及其子类。 | 局限于不支持多重继承的语言（如 Java）。 |
| **适用性** | 更常用，推荐使用。 | 使用受限，但可以直接覆盖 Adaptee 的方法。 |

本笔记后续示例将主要采用**对象适配器**（组合/依赖）方式，因为它更灵活且被主流语言推荐。

## 💻 4. 代码示例：媒体播放器 (Java/Python)

以**媒体播放器**为例：现有的 `AudioPlayer` 只能播放 `mp3` 文件。我们有高级播放器 `VlcPlayer` 和 `Mp4Player`，它们接口不兼容。我们通过一个 `MediaAdapter` 来实现播放 `vlc` 和 `mp4` 的功能。

### 📌 Java 对象适配器实现

我们将使用 Java 语言来实现**对象适配器**。

#### 1\. 目标接口 (Target)

```java
// 1. Target：媒体播放器接口
public interface MediaPlayer {
    void play(String audioType, String fileName);
}
```

#### 2\. 适配者接口与实现 (Adaptee)

```java
// 2A. AdvancedMediaPlayer 接口 (Adaptee 的接口)
public interface AdvancedMediaPlayer {
    void playVlc(String fileName);
    void playMp4(String fileName);
}

// 2B. Adaptee 实体类 VlcPlayer
public class VlcPlayer implements AdvancedMediaPlayer {
    @Override
    public void playVlc(String fileName) {
        System.out.println("Playing vlc file. Name: " + fileName);
    }
    @Override
    public void playMp4(String fileName) {
        // 什么也不做
    }
}
// 2C. Adaptee 实体类 Mp4Player
public class Mp4Player implements AdvancedMediaPlayer {
    @Override
    public void playVlc(String fileName) {
        // 什么也不做
    }
    @Override
    public void playMp4(String fileName) {
        System.out.println("Playing mp4 file. Name: " + fileName);
    }
}
```

#### 3\. 适配器 (Adapter)

```java
// 3. Adapter：媒体适配器
public class MediaAdapter implements MediaPlayer {
    private AdvancedMediaPlayer advancedMusicPlayer;

    public MediaAdapter(String audioType) {
        if (audioType.equalsIgnoreCase("vlc")) {
            this.advancedMusicPlayer = new VlcPlayer();
        } else if (audioType.equalsIgnoreCase("mp4")) {
            this.advancedMusicPlayer = new Mp4Player();
        }
    }

    // 核心：实现 Target 接口，并在内部调用 Adaptee 的方法
    @Override
    public void play(String audioType, String fileName) {
        if (audioType.equalsIgnoreCase("vlc")) {
            advancedMusicPlayer.playVlc(fileName); // 委托给 Adaptee
        } else if (audioType.equalsIgnoreCase("mp4")) {
            advancedMusicPlayer.playMp4(fileName); // 委托给 Adaptee
        }
    }
}
```

#### 4\. 客户端实现 (Client)

```java
// 4. Client：AudioPlayer (内置 mp3 支持，通过 Adapter 支持 vlc/mp4)
public class AudioPlayer implements MediaPlayer {
    private MediaAdapter mediaAdapter;

    @Override
    public void play(String audioType, String fileName) {
        if (audioType.equalsIgnoreCase("mp3")) {
            System.out.println("Playing mp3 file. Name: " + fileName);
        }
        // 使用适配器支持其他格式
        else if (audioType.equalsIgnoreCase("vlc") || audioType.equalsIgnoreCase("mp4")) {
            mediaAdapter = new MediaAdapter(audioType); // 创建或获取适配器
            mediaAdapter.play(audioType, fileName);
        } else {
            System.out.println("Invalid media. " + audioType + " format not supported");
        }
    }
}

// 5. 客户端调用
public class AdapterPatternDemo {
    public static void main(String[] args) {
        AudioPlayer audioPlayer = new AudioPlayer();

        audioPlayer.play("mp3", "beyond the horizon.mp3");
        audioPlayer.play("mp4", "alone.mp4");
        audioPlayer.play("vlc", "far far away.vlc");
        audioPlayer.play("avi", "mind me.avi");
    }
}
```

**运行结果:**

```
Playing mp3 file. Name: beyond the horizon.mp3
Playing mp4 file. Name: alone.mp4
Playing vlc file. Name: far far away.vlc
Invalid media. avi format not supported
```

### 📌 Python 对象适配器实现

Python 没有接口的概念，通常使用**抽象基类 (ABC)** 模拟 Target 接口，并通过**组合**实现对象适配器。

```python
from abc import ABC, abstractmethod

# 1. Target：媒体播放器接口
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, audioType, fileName):
        pass

# 2A. AdvancedMediaPlayer 接口 (Adaptee 的接口 - 隐式接口)
class AdvancedMediaPlayer(ABC):
    @abstractmethod
    def play_vlc(self, fileName):
        pass

    @abstractmethod
    def play_mp4(self, fileName):
        pass

# 2B. Adaptee 实体类 VlcPlayer
class VlcPlayer(AdvancedMediaPlayer):
    def play_vlc(self, fileName):
        print(f"Playing vlc file. Name: {fileName}")

    def play_mp4(self, fileName):
        pass # 不实现

# 2C. Adaptee 实体类 Mp4Player
class Mp4Player(AdvancedMediaPlayer):
    def play_vlc(self, fileName):
        pass # 不实现

    def play_mp4(self, fileName):
        print(f"Playing mp4 file. Name: {fileName}")

# 3. Adapter：媒体适配器
class MediaAdapter(MediaPlayer):
    def __init__(self, audioType):
        if audioType.lower() == "vlc":
            self.advanced_player = VlcPlayer()
        elif audioType.lower() == "mp4":
            self.advanced_player = Mp4Player()
        else:
            self.advanced_player = None

    # 核心：实现 Target 接口，并在内部调用 Adaptee 的方法
    def play(self, audioType, fileName):
        if self.advanced_player:
            if audioType.lower() == "vlc":
                self.advanced_player.play_vlc(fileName)
            elif audioType.lower() == "mp4":
                self.advanced_player.play_mp4(fileName)

# 4. Client：AudioPlayer
class AudioPlayer(MediaPlayer):
    def play(self, audioType, fileName):
        if audioType.lower() == "mp3":
            print(f"Playing mp3 file. Name: {fileName}")
        elif audioType.lower() in ("vlc", "mp4"):
            # 使用适配器支持其他格式
            media_adapter = MediaAdapter(audioType)
            media_adapter.play(audioType, fileName)
        else:
            print(f"Invalid media. {audioType} format not supported")

# 5. 客户端调用
if __name__ == "__main__":
    audioPlayer = AudioPlayer()

    audioPlayer.play("mp3", "beyond the horizon.mp3")
    audioPlayer.play("mp4", "alone.mp4")
    audioPlayer.play("vlc", "far far away.vlc")
    audioPlayer.play("avi", "mind me.avi")
```

## ✅ 5. 优点与缺点

### 👍 优点

* **解耦和重用:** 将目标类和适配者类解耦，无需修改原有适配者类的代码即可重用。
* **透明性和复用性:** 客户端只面向目标接口编程，不关心内部适配者实现，提高了适配者的复用性。
* **灵活性和扩展性:** 引入新的适配者或更换适配器非常方便，符合\*\*"开闭原则"\*\*。
* **对象适配器优势:** 一个对象适配器可以适配多个不同的适配者类及其子类到同一个目标接口。

### 👎 缺点

* **类适配器局限性:** 对于 Java、C\# 等不支持多重继承的语言，类适配器只能适配一个适配者类。
* **对象适配器局限性:** 想要置换适配者类的方法相对复杂，需要通过继承适配者来解决。
* **系统凌乱:** 过多地使用适配器可能使系统结构变得零乱，难以一眼看出实际调用逻辑（例如：调用 A 接口，内部被适配成 B 接口的实现）。

## 🌐 6. 适用环境 (Applicability)

在以下情况下可以考虑使用适配器模式：

1.  系统需要使用**现有的类**，但这些类的接口与系统需要的接口不兼容时。
2.  想要建立一个可以**重复使用**的类，用于与一些彼此没有太大关联的类一起工作时。
3.  想要通过**接口转换**，将一个类无缝地插入到另一个类体系中时（例如 JDBC 驱动）。

-----

如果您希望了解更多关于**类适配器**的实现细节，或者需要查看其他**结构型设计模式**的笔记，请告诉我！
