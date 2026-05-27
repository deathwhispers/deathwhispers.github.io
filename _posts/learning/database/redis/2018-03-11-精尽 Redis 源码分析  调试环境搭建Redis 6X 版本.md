---
layout: post
title: 精尽 Redis 源码分析 —— 调试环境搭建（Redis 6.X 版本）
slug: redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x
type:
- note
date: 2018-03-11
tags:
- Concurrency
- Redis
- Database
categories:
- Learning
- Database
author: deathwhispers
created: 2019-05-11 11:45
updated: 2019-05-11 22:17
---

今儿，我们来搭建一个 Redis 调试环境，目标是：

- 启动 Redis Server ，成功断点调试 Server 的启动过程。
- 使用 redis-cli 启动一个 Client 连接上 Server，并使用 get key 指令，发起一次 key 的读取。

视频可见 B 站：[https://www.bilibili.com/video/BV12X4y1c79z](https://www.bilibili.com/video/BV12X4y1c79z)

艿艿比较腼腆，大家给个三连支持一下，感恩 1024~

# 1. 依赖工具

## 1.1 CLion

下载地址：[https://www.jetbrains.com/clion](https://www.jetbrains.com/clion)

CLion 是 Jetbrains 团队提供的 C/C++ 开发工具。所以，所以和我们平时使用的 [IDEA](https://www.iocoder.cn/IDEA/idea-2020-reset-eval/) 差别不大。

这里，艿艿使用的是 CLion 版本是 **2021.1.3** 。

## ~~1.2 CMake~~

从 CLion [2020.2](https://blog.jetbrains.com/zh-hans/2020/07/08/clion-makefile/) 版本开始，可以支持 Makefile 类型的项目，而 Redis 就是使用 Makefile 构建的项目，所以我们**无需**再安装 CMake 啦！！！

可能胖友对 Makefile 或是 CMake 不太了解？！没关系，这个小节主要是给，之前尝试搭建 Redis 调试环境，结果被 CMake 的胖友。

**不影响后续的内容的学习**！

# 2. 源码拉取

使用 CLion 从官方仓库 [https://github.com/antirez/redis](https://github.com/antirez/redis) 克隆项目。操作如下图所示：

友情提示：如果网络不是很好的胖友，可以选择和艿艿一样，使用 Gitee 提供的镜像仓库 [https://gitee.com/mirrors/redis.git](https://gitee.com/mirrors/redis.git)

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037822980-699581b7-8924-4dd9-87d6-37f74512e73b.gif)

克隆 Redis 仓库

这里，我们使用的 Redis 版本是 **6.2.5**。

友情提示：胖友可以考虑 Fork 下[官方仓库](https://github.com/antirez/redis)，为什么呢？

既然开始阅读、调试源码，我们可能会写一些注释，有了自己的仓库，可以进行自由的提交。

# 3. 导入项目

克隆完项目后，CLion 会进行 Importing 导入项目，耐心等待一下。如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823086-63f3c181-655d-4bd5-a28e-5c876b0de953.png)

导入项目

# 4. 编译项目

导入完成后，打开 Makefile 文件，点击 default:all 绿色箭头，开始项目的编译。如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823230-9c9f7c20-99e1-4bfc-baac-7c9d6cc98940.png)

编译项目

# 5. 运行 Redis Server

① 配置 Redis Server 的启动项，操作如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823333-5da44521-c060-4358-b55f-75bd73a418ab.png)

配置 Redis Server 启动项

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823428-72c472e9-febb-4c24-a44b-d8aec1eabed7.png)

配置 Redis Server 启动项

② 打开 server.c 文件，在 #main(…) 方法上，添加一个**方法断点**，它是 Redis Server 的启动入口。如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823509-417e27c6-a12b-44e2-b520-ae873bc13a1b.png)

设置 Redis Server main 断点

③ **Debug** 右上方的 redis-server 启动项，成功进入 #main(…) 方法的断点。如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823594-df63fea3-8c72-49b5-9148-6364fbc09df2.png)

进入 Redis Server main 断点

---

至此，我们已经完成了我们的第一个小目标“*启动 Redis Server ，成功断点调试 Server 的启动过程*”。

点击左下方的**绿色**小箭头，恢复 Redis Server 的启动，不然等会 Redis Client 都连接不上来。在 CLion 的控制台，我们会看到 Redis Server 启动成功的日志如下：

```plain text
plain 22315:M 28 Jul 2021 01:23:37.535 # Server initialized 22315:M 28 Jul 2021 01:23:37.535 * Ready to accept connections
```

---

# 6. 运行 Redis Client

① 打开 ae.c 文件，在 #aeProcessEvents(…) 方法的如图处，打上一个**端点**，用于调试 Redis Server 处理各种来自 Redis Client 的 IO 事件。如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823707-5e2ee55f-432a-4d00-8b16-f8d9819dd2a1.png)

设置 Redis Server ae 断点

② 打开 IDE Terminal，运行 redis-cli 启动一个 Redis Client，连接上 Redis Server。如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823819-f7ecf42c-8afe-4872-a4f0-641c9c975e3e.png)

启动 Redis Client

此时，我们在 ae.c 的 #aeProcessEvents(…) 的断点成功进入，Redis Server 收到 Redis Client 的**连接事件**。

打开 Debug 窗口，点击左下方的**绿色**小箭头，恢复 Redis Server 的执行。

③ 回到 redis-cli 命令行，输入 get key 指令，向 Redis Server 发起一次 get 请求。效果如下图所示：

![](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/1698037823928-0ddd80d1-25df-4629-ac27-d4344581fa09.png)

Redis Client 读取 key

此时，我们在 ae.c 的 #aeProcessEvents(…) 的断点又一次进入，Redis Server 收到 Redis Client 的 get 请求。

---

至此，我们已经完成了我们的第二个小目标“*使用 ****redis-cli**** 启动一个 Client 连接上 Server，并使用 ****get key**** 指令，发起一次 key 的读取*”。

# 7. 源码解析

Redis 源码是使用 C 实现的，对于 Java 程序员的我们来说，还是有一定“门槛”的，所以最好借助下市面上 Redis 相关的书籍。

① [《Redis 设计与实现》](https://github.com/YunaiV/books)，针对 Redis 3.X 版本，豆瓣评分 8.6 分，对应详细注释的 Redis 仓库 [https://github.com/YunaiV/redis-3.0-annotated.git](https://github.com/YunaiV/redis-3.0-annotated.git) 。

这本书艿艿和蛮多朋友都看过，虽然针对的 Redis 版本比较老，考虑到 Redis 核心代码变动其实不多，还是非常不错的选择。

② [《Redis5设计与源码分析》](https://github.com/YunaiV/books)，针对 Redis 5.X 版本，豆瓣评分 6.8 分。

主要优点是针对 Redis 5.X 版本，比较新。具体内容如何，艿艿也不是很确定。可以备一本，在看到源码卡壳的时候，作为字典查一查，也是不错的选择哈~

③ [《Redis源码剖析与实战》](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/184d59981e2b62d539ae6e4732a8badb.jpg)，针对 Redis 版本不详，极客时间 2021 年出的，可能是 Redis 6.X 版本。

这个专栏，目前还在更新，艿艿准备养肥之后，花 1-2 周撸一撸，嘿嘿！作者（蒋德钧）之前出的[《Redis核心技术与实战》](assets/images/learning/database/redis/redisson-redlock-source-code-analysis-debug-environment-setup-redis-6-x/bc2c20a873b8d016029fb615f96fcd1e.jpg) 非常不错，我大飞哥好评连连！
