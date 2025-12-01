---
layout: post
title: 项目结构一览
slug: dubbo-project-structure-overview
type:
  - note
date: 2022-03-11
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-03-11 11:53
updated: 2022-03-11 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文主要分享 **Dubbo 的项目结构**。希望通过本文能让胖友对 Dubbo 的整体项目有个简单的了解。

另外，笔者会相对大量引用 [《Dubbo 用户指南》](http://dubbo.apache.org/zh-cn/docs/user/) 和 [《Dubbo 开发指南》](http://dubbo.apache.org/zh-cn/docs/dev/) ，写的真的挺好的。ps：限于排版，部分地方引用会存在未标明的情况。

在拉取 Dubbo 项目后，我们会发现拆分了**好多** Maven 项目。是不是内心一紧，产生了恐惧感？不要方，我们就是继续怼。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038398517-b107bdd9-af3a-4e59-a983-52871d33592a.png)

项目结构

# 2. 代码统计

这里先分享一个小技巧。笔者在开始源码学习时，会首先了解项目的代码量。

**第一种方式**，使用 [IDEA Statistic](https://plugins.jetbrains.com/plugin/4509-statistic) 插件，统计整体代码量。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038398633-2c84f1d1-6490-41c3-8514-53dd42d53c02.png)

Statistic 统计代码量

我们可以粗略的看到，总的代码量在 98210 行。这其中还包括单元测试，示例等等代码。所以，不慌。

**第二种方式**，使用 [Shell 脚本命令逐个 Maven 模块统计](http://blog.csdn.net/yhhwatl/article/details/52623879) 。

一般情况下，笔者使用 find . -name “*.java”|xargs cat|grep -v -e ^$ -e ^//.*$|wc -l 。这个命令只过滤了**部分注释**，所以相比 [IDEA Statistic](https://plugins.jetbrains.com/plugin/4509-statistic) 会**偏多**。

当然，考虑到准确性，胖友需要手动 cd 到每个 Maven 项目的 src/main/java 目录下，以达到排除单元测试的代码量。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038398724-0bfd9112-a144-4f17-807b-277cbb33c9b6.png)

Shell 脚本统计代码量

# 3. 项目一览

如果胖友看过 [《Dubbo 框架设计》](http://dubbo.apache.org/zh-cn/docs/dev/design.html) ，就会发现有下面这张图。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038398806-0b976121-f2cb-45a0-bd50-c504e4aec862.png)

模块分包

通过这图，我们可以很清晰的知道几个 Maven 模块的依赖关系。

## 3.1 dubbo-common

[dubbo-common](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-common)**公共逻辑模块**：提供工具类和通用模型。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038398878-8a93803b-0e97-42a9-9e6e-f82df397321e.png)

dubbo-common 包结构

工具类比较好理解，**通用模型**是什么？举个例子，[com.alibaba.dubbo.common.URL](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-common/src/main/java/com/alibaba/dubbo/common/URL.java) ：

FROM [《Dubbo 开发指南 —— 公共契约》](http://dubbo.apache.org/zh-cn/docs/dev/contract.html)

- 所有扩展点参数都包含 URL 参数，URL 作为上下文信息贯穿整个扩展点设计体系。
- URL 采用标准格式：
protocol://username:password@host:port/path?key=value&key=value
。

那么 URL 有什么用呢？ 请见后续文章。

## 3.2 dubbo-remoting

[dubbo-remoting](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-remoting)**远程通信模块**：提供**通用**的客户端和服务端的通讯功能。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038398960-8d3dfe21-b056-4729-99d7-8eb0704c5f49.png)

dubbo-remoting 包结构

- dubbo-remoting-zookeeper
，相当于 Zookeeper Client ，和 Zookeeper Server 通信。
- dubbo-remoting-api**接口**
， 定义了 Dubbo Client 和 Dubbo Server 的
。
- **实现**
dubbo-remoting-api
    - dubbo-remoting-grizzly[Grizzly](https://javaee.github.io/grizzly/)
，基于
实现。
    - dubbo-remoting-http[Jetty](https://www.eclipse.org/jetty/)[Tomcat](http://tomcat.apache.org/)
，基于
或
实现。
    - dubbo-remoting-mina[Mina](https://mina.apache.org/)
，基于
实现。
    - dubbo-remoting-netty[Netty 3](https://netty.io/)
，基于
实现。
    - dubbo-remoting-netty4[Netty 4](https://netty.io/)
，基于
实现。
    - dubbo-remoting-p2p
，P2P 服务器。注册中心
dubbo-registry-multicast
项目的使用该项目。

从**最小化**的角度来看，我们只需要看：

- dubbo-remoting-api
+
dubbo-remoting-netty4
- dubbo-remoting-zookeeper

## 3.3 dubbo-rpc

[dubbo-rpc](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-rpc)**远程调用模块**：抽象各种协议，以及动态代理，只包含一对一的调用，**不关心集群的管理**。

- 集群相关的管理，由
dubbo-cluster
提供特性。

在回过头看上面的图，我们会发现，dubbo-rpc 是整个 Dubbo 的**中心**。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399039-a9ab7ff7-8ec7-4bcd-8973-e8c48aaa7012.png)

dubbo-rpc 包结构

- dubbo-rpc-api**抽象实现**
，
各种协议以及动态代理，
了一对一的调用。
- 其他模块，实现 [《用户指南 —— 协议参考手册》](http://dubbo.apache.org/zh-cn/docs/user/references/protocol/introduction.html)
dubbo-rpc-api
，提供对应的协议实现。在
中，可以看到每种协议的介绍。
- 另外，
dubbo-rpc-default
对应
dubbo://
协议。
- 拓展参见 [《Dubbo 开发指南 —— 协议扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/protocol.html)
文档。

进一步的拆解，见 [《精尽 Dubbo 源码分析 —— 核心流程一览》](http://svip.iocoder.cn/Dubbo/implementation-intro/?self=) 文章。

## 3.4 dubbo-cluster

[dubbo-cluster](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-cluster)**集群模块**：将多个服务提供方伪装为一个提供方，包括：负载均衡, 集群容错，路由，分组聚合等。集群的地址列表可以是静态配置的，也可以是由注册中心下发。

- 注册中心下发，由
dubbo-registry
提供特性。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399116-9699bc04-68ed-48d7-9db9-2accb3208d0d.png)

dubbo-cluster 包结构

- 容错
    - [com.alibaba.dubbo.rpc.cluster.Cluster](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-cluster/src/main/java/com/alibaba/dubbo/rpc/cluster/Cluster.java)
接口 +
com.alibaba.dubbo.rpc.cluster.support
包。
    - Cluster 将 Directory 中的多个 Invoker 伪装成一个 Invoker，对上层透明，伪装过程包含了容错逻辑，调用失败后，重试另一个。
    - 拓展参见 [《Dubbo 用户指南 —— 集群容错》](http://dubbo.apache.org/zh-cn/docs/user/demos/fault-tolerent-strategy.html)[《Dubbo 开发指南 —— 集群扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/cluster.html)
和
文档。
- 目录
    - [com.alibaba.dubbo.rpc.cluster.Directory](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-cluster/src/main/java/com/alibaba/dubbo/rpc/cluster/Directory.java)
接口 +
com.alibaba.dubbo.rpc.cluster.directory
包。
    - Directory 代表了多个 Invoker ，可以把它看成 List
，但与 List 不同的是，它的值可能是动态变化的，比如注册中心推送变更。
- 路由
    - [com.alibaba.dubbo.rpc.cluster.Router](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-cluster/src/main/java/com/alibaba/dubbo/rpc/cluster/Router.java)
接口 +
com.alibaba.dubbo.rpc.cluster.router
包。
    - 负责从多个
Invoker
中按路由规则选出子集，比如读写分离，应用隔离等。
    - 拓展参见 [《Dubbo 用户指南 —— 路由规则》](http://dubbo.apache.org/zh-cn/docs/user/demos/routing-rule.html)[《Dubbo 开发指南 —— 路由拓展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/router.html)
和
文档。
- 配置
    - [com.alibaba.dubbo.rpc.cluster.Configurator](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-cluster/src/main/java/com/alibaba/dubbo/rpc/cluster/Configurator.java)
接口 +
com.alibaba.dubbo.rpc.cluster.configurator
包。
    - 拓展参见 [《Dubbo 用户指南 —— 配置规则》](http://dubbo.apache.org/zh-cn/docs/user/demos/config-rule.html)
文档。
- 负载均衡
    - [com.alibaba.dubbo.rpc.cluster.LoadBalance](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-cluster/src/main/java/com/alibaba/dubbo/rpc/cluster/LoadBalance.java)
接口 +
com.alibaba.dubbo.rpc.cluster.loadbalance
包。
    - LoadBalance 负责从多个 Invoker 中选出具体的一个用于本次调用，选的过程包含了负载均衡算法，调用失败后，需要重选。
    - 拓展参见 [《Dubbo 用户指南 —— 负载均衡》](http://dubbo.apache.org/zh-cn/docs/user/demos/loadbalance.html)[《Dubbo 开发指南 —— 负载均衡拓展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/load-balance.html)
和
文档。
- 合并结果
    - [com.alibaba.dubbo.rpc.cluster.Merger](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-cluster/src/main/java/com/alibaba/dubbo/rpc/cluster/Merger.java)
接口 +
com.alibaba.dubbo.rpc.cluster.merger
包。
    - 合并返回结果，用于分组聚合。
    - 拓展参见 [《Dubbo 用户指南 —— 分组聚合》](http://dubbo.apache.org/zh-cn/docs/user/demos/group-merger.html)[《Dubbo 开发指南 —— 合并结果扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/merger.html)
和
文档。

整体流程如下：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399200-d3b045ce-edf9-4ffd-baf4-5be39143bf94.png)

集群容错

## 3.5 dubbo-registry

[dubbo-registry](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-registry)**注册中心模块**：基于注册中心下发地址的集群方式，以及对各种注册中心的抽象。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399289-02c4e944-02c7-43c3-865f-47f8c368a2b4.png)

dubbo-registry 包结构

- dubbo-registry-api**抽象**
，
注册中心的注册与发现接口。
- 其他模块，实现 [《用户指南 —— 注册中心参考手册》](http://dubbo.apache.org/zh-cn/docs/user/references/registry/introduction.html)
dubbo-registry-api
，提供对应的注册中心实现。在
中，可以看到每种注册中心的介绍。
- 另外，
dubbo-registry-default
对应 Simple 注册中心。
- 拓展参见 [《Dubbo 开发指南 —— 注册中心扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/registry.html)
文档。

## 3.6 dubbo-monitor

[dubbo-monitor](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-monitor)**监控模块**：统计服务调用次数，调用时间的，调用链跟踪的服务。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399404-7a9fcb00-fe62-412e-aeb3-3656f6f066b9.png)

dubbo-monitor 包结构

- 拓展参见 [《Dubbo 开发指南 —— 监控中心扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/monitor.html)
。

目前社区里，有对 Dubbo 监控中心进行重构的项目，例如 ：

- [https://github.com/handuyishe/dubbo-monitor](https://github.com/handuyishe/dubbo-monitor)
- [https://github.com/zhongxig/dubbo-d-monitor](https://github.com/zhongxig/dubbo-d-monitor)

## 3.7 dubbo-config

[dubbo-config](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-config)**配置模块**：是 Dubbo 对外的 API，用户通过 Config 使用Dubbo，隐藏 Dubbo 所有细节。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399470-0f9bd050-a784-46dd-91ac-57f097000b2e.png)

dubbo-config 包结构

- dubbo-config-api[API 配置](http://dubbo.apache.org/zh-cn/docs/user/configuration/api.html)[属性配置](http://dubbo.apache.org/zh-cn/docs/user/configuration/properties.html)
，实现了
和
功能。
- dubbo-config-spring[XML 配置](http://dubbo.apache.org/zh-cn/docs/user/configuration/xml.html)[注解配置](http://dubbo.apache.org/zh-cn/docs/user/configuration/annotation.html)
，实现了
和
功能。

推荐阅读 [《Dubbo 开发指南 —— 配置设计》](http://dubbo.apache.org/zh-cn/docs/dev/principals/configuration.html) 。

## 3.8 dubbo-container

[dubbo-container](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-container)**容器模块**：是一个 Standlone 的容器，以简单的 Main 加载 Spring 启动，因为服务通常不需要 Tomcat/JBoss 等 Web 容器的特性，没必要用 Web 容器去加载服务。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399540-7621a3ef-8439-4291-8c00-dd66bb682604.png)

dubbo-container 包结构

- dubbo-container-api[com.alibaba.dubbo.container.Container](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-container/dubbo-container-api/src/main/java/com/alibaba/dubbo/container/Container.java)
：定义了
接口，并提供 加载所有容器启动的 Main 类。
- 实现
dubbo-container-api
    - dubbo-container-spring
，提供了
com.alibaba.dubbo.container.spring.SpringContainer
。
    - dubbo-container-log4j
，提供了
com.alibaba.dubbo.container.log4j.Log4jContainer
。
    - dubbo-container-logback
，提供了
com.alibaba.dubbo.container.logback.LogbackContainer
。
- 拓展参考 [《Dubbo 用户指南 —— 服务容器》](http://dubbo.apache.org/zh-cn/docs/user/demos/service-container.html)[《Dubbo 开发指南 —— 容器扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/container.html)
和
文档。

## 3.9 dubbo-filter

[dubbo-filter](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-filter)**过滤器模块**：提供了**内置**的过滤器。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399604-10bbab65-b33b-4945-bd91-bd3eb7beabf2.png)

dubbo-filter 包结构

- dubbo-filter-cache
，缓存过滤器。
    - 拓展参考 [《Dubbo 用户指南 —— 结果缓存》](http://dubbo.apache.org/zh-cn/docs/user/demos/result-cache.html)[《Dubbo 开发指南 —— 缓存拓展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/cache.html)
和
文档。
- dubbo-filter-validation
，参数验证过滤器。
    - 拓展参考 [《Dubbo 用户指南 —— 参数验证》](http://dubbo.apache.org/zh-cn/docs/user/demos/parameter-validation.html)[《Dubbo 开发指南 —— 验证扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/validation.html)
和
文档。

## 3.10 dubbo-plugin

[dubbo-plugin](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-plugin)**插件模块**：提供了**内置**的插件。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399677-8e59bd68-371e-4a81-82aa-6806937c72c2.png)

dubbo-plugin 包结构

- dubbo-qos
，提供在线运维命令。
    - 拓展参考 [《Dubbo 用户指南 —— 新版本 telnet 命令使用说明》](http://dubbo.apache.org/zh-cn/docs/user/references/qos.html)[《Dubbo 开发指南 —— Telnet 命令扩展》](http://dubbo.apache.org/zh-cn/docs/dev/impls/telnet-handler.html)
和
文档。

## 3.11 hessian-lite

[hessian-lite](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/hessian-lite) ：Dubbo 对 [Hessian 2](http://hessian.caucho.com/) 的 **序列化** 部分的精简、改进、BugFix 。

提交历史如下：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399748-8dd03f58-d151-4c73-bd3e-b4daa15df25f.png)

hessian-lite 提交历史

## 3.12 dubbo-demo

[dubbo-demo](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-plugin)**快速启动示例**。

参见 [《Dubbo 用户指南 —— 快速启动》](http://dubbo.apache.org/zh-cn/docs/user/quick-start.html) 文档。

## 3.13 dubbo-test

[dubbo-test](https://github.com/alibaba/dubbo/tree/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dubbo-test)**测试模块**。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399826-55ede648-c8e7-4807-9fa8-3a14f886bb33.png)

dubbo-test 包结构

- dubbo-test-benchmark
，性能测试。
    - 参考 [《Dubbo 用户指南 —— 性能测试报告》](http://dubbo.apache.org/zh-cn/docs/user/perf-test.html)
文档。
- dubbo-test-compatibility
，兼容性测试。
    - dubbo-test-spring3
，测试对 Spring 3 的兼容性。
- dubbo-test-example**使用示例**
，
。

## 3.14 Maven POM

### 3.14.1 dubbo-dependencies-bom

[dubbo-dependencies-bom/pom.xml](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/dependencies-bom/pom.xml) ，Maven BOM(Bill Of Materials) ，**统一**定义了 Dubbo 依赖的三方库的版本号：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399893-803ab678-71c6-4b23-af06-0d35b0c93c45.png)

dubbo-dependencies-bom 文件

---

dubbo-parent 会引入该 BOM ：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038399968-27599a05-1da2-4a7b-a62d-80957ccc4fba.png)

引入 dubbo-dependencies-bom 文件

---

更多 Maven BOM 的知识，可以看下 [《Maven 与Spring BOM(Bill Of Materials)简化Spring版本控制》](http://blog.csdn.net/fanxiaobin577328725/article/details/66974896) 文档：

通俗解说：为了防止用 Maven 管理 Spring 项目时，不同的项目依赖了不同版本的 Spring ，可以使用 Maven BOM 来解决者一问题。

### 3.14.2 dubbo-bom

[dubbo-bom/pom.xml](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/bom/pom.xml) ，Maven BOM(Bill Of Materials) ，**统一**定义了 Dubbo 的版本号：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038400040-c4faa681-71c9-4f3e-8234-e0fb2fcc4cf2.png)

dubbo-bom 文件

---

dubbo-demo 和 dubbo-test 会引入该 BOM 。以 dubbo-demo 举例子：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038400127-1619b02e-5cd3-4dc7-a200-a3f5e76a474c.png)

引入 dubbo-bom 文件

### 3.14.3 dubbo-parent

[dubbo/pom.xml](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/pom.xml) ，Dubbo Parent Pom 。

Dubbo 的 Maven 模块，都会引入该 pom 文件。以 dubbo-cluster 举例子：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038400198-b10f2e2f-6b9c-4a59-bc35-ff53f8ffd862.png)

引入 dubbo-parent 文件

---

我们整理下上面的 pom 文件：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038400262-a0fff84d-fc8f-4cc3-a1f6-898ef91d3bb3.png)

引入关系

### 3.14.4 dubbo-all

[dubbo/all/pom.xml](https://github.com/alibaba/dubbo/blob/4bbc0ddddacc915ddc8ff292dd28745bbc0031fd/all/pom.xml) ，Dubbo All Pom ，定义了 Dubbo 的**打包脚本**。

我们在使用 Dubbo 库时，引入该 pom 文件。

笔者推荐，再详细阅读下 [《Dubbo 开发指南 —— 框架设计》](http://dubbo.apache.org/zh-cn/docs/dev/design.html) ，重新梳理下。

参考文章：

- [《Dubbo 用户指南》](http://dubbo.apache.org/zh-cn/docs/user/)
- [《Dubbo 开发指南》](http://dubbo.apache.org/zh-cn/docs/dev/)