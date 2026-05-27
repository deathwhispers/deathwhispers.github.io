---
layout: post
title: ThingsBoard入门实战（一）：物联网平台 ThingsBoard 简介
slug: thingsboard-introduction
type:
- note
date: 2023-07-03
status: draft
tags:
- IoT
- ThingsBoard
categories:
- IoT
- ThingsBoard
mood: null
weather: null
author: deathwhispers
created: 2023-06-03 11:45
updated: 2023-06-03 18:33
---

# ThingsBoard入门实战（一）：物联网平台 ThingsBoard 简介_莽就对了的博客-CSDN博客_thingsboard

# 物联网平台 ThingsBoard 简介

## 一、简介

### 1. 背景

最近很多做设备的朋友和我说，设备接入物联网并进行[可视化](https://so.csdn.net/so/search?q=%E5%8F%AF%E8%A7%86%E5%8C%96&spm=1001.2101.3001.7020)管理存在困难，主要是以下两点：

1. 一方面，接入物联网平台需要花费大量的时间精力金钱。而且适用性不强，也就是说如果加入新的设备，就需要大量的改动。同时由于没有专业的可视化人员，可视化方面更是一塌糊涂。
2. 另一方面，目前各大厂的物联网平台产品生态封闭。物联网平台之间无法互通，难以满足自由互联的需求。在可视化方面大厂则是各玩各的，无法形成软件资产的有效沉淀。

有没有一种几乎不花钱，还功能强大、扩展性强、使用方便的物联网平台呢？

答案就是Thingsboard。

### 2. 物联网平台 ThingsBoard

ThingsBoard 作为目前 Github 上最流行的开源物联网平台，可以实现物联网项目的快速开发、管理和扩展, 是中小微企业物联网平台的不二之选。

ThingBoard可以分为四个核心模块：

- 设备管理
- 数据接入
- 规则引擎
- 部件面板

![](/assets/images/iot/thingsboard/thingsboard-introduction/a1f93f1cbf66c72a2aacd50523213f00.png)

也就是说，ThingsBoard可用于:

- 设备管理，资产和客户并定义他们之间的关系。
- 基于设备和资产收集数据并进行可视化。
- 采集遥测数据并进行相关的事件处理进行警报响应。
- 基于远程RPC调用进行设备控制。
- 基于生命周期事件、REST API事件、RPC请求构建工作流。
- 基于动态设计和响应仪表板向你的客户提供设备或资产的遥测数据。
- 基于规则链自定义特定功能。
- 发布设备数据至第三方系统。
- …

涵盖了各种常见的物联网需求，不常见的也可以通过配置和二次开发完美完成。

三个必须了解的网站：

3. [官网](https://thingsboard.io/)

![](/assets/images/iot/thingsboard/thingsboard-introduction/253b9106dfa13544308c066c7a7df171.jpg)

4. [GitHub](https://github.com/thingsboard/thingsboard)
5. [中文网](http://xn--thingsboard-b28qs24v2pyd/%20(ithingsboard.com))

![](/assets/images/iot/thingsboard/thingsboard-introduction/109cbf1a19c53bac17061ea77a73d3ce.jpg)

## 二、安装

方便起见，使用Docker安装ThingsBoard。

6. 安装Docker和Docker-compose

参考Docker官网和Docker-compose官网安装即可。

7. 新建docker-compose.yml用于定义安装环境:

vi docker-compose.yml

8. 编写docker-compose.yml:

由于 docker 搭建环境非常方便，我们直接使用兼容性最好的thingsboard/tb-postgres镜像。

version: ‘2.2’ services: zookeeper: restart: always image: “zookeeper:3.5” ports: - “2181:2181” environment: ZOO_MY_ID: 1 ZOO_SERVERS: server.1=zookeeper:2888:3888;zookeeper:2181 kafka: restart: always image: wurstmeister/kafka depends_on: - zookeeper ports: - “9092:9092” environment: KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181 KAFKA_LISTENERS: INSIDE://:9093,OUTSIDE://:9092 KAFKA_ADVERTISED_LISTENERS: INSIDE://:9093,OUTSIDE://kafka:9092 KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE volumes: - /var/run/docker.sock:/var/run/docker.sock mytb: restart: always image: “thingsboard/tb-postgres” depends_on: - kafka ports: - “9090:9090” - “1883:1883” - “5683:5683/udp” environment: TB_QUEUE_TYPE: kafka TB_KAFKA_SERVERS: kafka:9092 volumes: - /data/.mytb-data:/data - /data/.mytb-logs:/var/log/thingsboard

**说明：**

- mytb - ThingsBoard服务名称
- restart: always - 在系统重新启动的情况下自动启动ThingsBoard在出现故障的情况下自动重新启动ThingsBoard。
- image: thingsboard/tb-postgres - docker镜像也可以是thingsboard/tb-cassandra或thingsboard/tb
- “PORT:PORT” 顺序是 “本地端口:Docker容器内端口”

8080:9090 - 将本地端口9090转发至Docker容器内的HTTP端口9090

1883:1883 - 将本地端口1883转发至Docker容器内的MQTT端口1883

5683:5683 - 将本地端口5683转发至Docker容器内的COAP端口5683

- “DIR:DIR” 顺序是 “本地主机目录:Docker容器内目录”

/data/.mytb-data:/data - 将主机的目录/data/.mytb-data挂载到ThingsBoard数据目录

/data/.mytb-logs:/var/log/thingsboard - 将主机的目录/data/.mytb-logs挂载到ThingsBoard日志目录

9. 授予目录权限 在启动Docker容器之前请运行以下命令以创建用于存储数据和日志的目录然后将其所有者更改为Docker容器用户，以便能够更改用户使用chown命令该命令需要sudo权限（该命令将要求sudo访问的密码）：

mkdir -p /data/.mytb-data && sudo chown -R 799:799 /data/.mytb-data mkdir -p /data/.mytb-logs && sudo chown -R 799:799 /data/.mytb-logs

10. 使用 docker-compose 启动容器

在包含docker-compose.yml文件的目录打开终端执行docker compose命令：

docker-compose pull docker-compose up

如果需要后台启动，就使用：

docker-compose up -d

执行完命令后等待启动， 可以先看看 docker容器的状态

docker ps

11. 查看ThingsBoard平台并修改密码 然后在浏览器中打开(例如http://localhost:9090)。

![](/assets/images/iot/thingsboard/thingsboard-introduction/6da7ebab4917b4d2d228d2f8609c95ba.jpg)

默认用户名/密码如下：

系统管理员: sysadmin@thingsboard.org / sysadmin

租户管理员: tenant@thingsboard.org / tenant

客户: customer@thingsboard.org / customer

安全起见，修改下密码： 主页右上角三个点 – 属性 – 更改密码

![](/assets/images/iot/thingsboard/thingsboard-introduction/26f7f46a27c41960eea9dfe56cd41fc1.jpg)

![](/assets/images/iot/thingsboard/thingsboard-introduction/29c94be87155ff93900736990984e37c.jpg)

![](/assets/images/iot/thingsboard/thingsboard-introduction/f34d079dccc65ff2d3b373637ae15868.jpg)

## 三、探索

### 1. 用户

先简单看下三类用户的面板，

**系统管理员**

![](/assets/images/iot/thingsboard/thingsboard-introduction/789f7c67527051d1487edb4cc9b33715.jpg)

**租户**

![](/assets/images/iot/thingsboard/thingsboard-introduction/d4698cc32fccaaf7c8397a4774ee2ecf.jpg)

**客户**

![](/assets/images/iot/thingsboard/thingsboard-introduction/483a16ea6a60be4822cda2b2b70e5dc8.jpg)

显然租户才是实际上的掌控者~

三者关系如下：

![](/assets/images/iot/thingsboard/thingsboard-introduction/d2b76b83dff124a9d31bc0625dfd7d15.jpg)

可以看到，默认租户下面有三个客户

![](/assets/images/iot/thingsboard/thingsboard-introduction/c26dde87599e089344a429fdf48e2174.jpg)

客户A的用户有两个，我们刚使用的是这个叫customer的用户

![](/assets/images/iot/thingsboard/thingsboard-introduction/746b8d590bf2e1d0a25a74e49949a0d1.jpg)

可见客户是一个抽象概念，也就是说客户用户才是真用户。

### 2. 设备

设备主要分属性和遥测，我们下一节会详细讲解，这里先看下最核心的遥测：

![](/assets/images/iot/thingsboard/thingsboard-introduction/e03e37eef1abad60aa3295a9a75e6a51.jpg)

遥测也就是我们常说的设备测量状态，比如温度计的温度，灯的亮度等等， 由于是新设备，所以是没有遥测值的，我们可以用http协议发一个。

### 3. 模拟发送遥测值

3.1 获取对接设备的访问令牌

![](/assets/images/iot/thingsboard/thingsboard-introduction/f6e54aa53f9ee4e5d13f431fe833b2ed.jpg)

这里使用默认的A1_TEST_TOKEN。

3.2 使用curl发送HTTP请求

curl -v -X POST -d ‘{“turn”:“1”,“light”:“90”}’ http://103.44.238.67:9090/api/v1/A1_TEST_TOKEN/telemetry –header “Content-Type:application/json”

3.3 查看更新后的遥测值

![](/assets/images/iot/thingsboard/thingsboard-introduction/f9cd8b38048596f751cc11558bea0977.jpg)

## 四、下一步

我们在这节简单了解了 ThingsBoard 这个物联网平台大杀器，后面的主要工作就是通过在 ThingsBoard 上开发一个路灯的项目，帮助大家熟悉 ThingsBoard 的基本使用。

下节课，就从为用户分配第一台设备开始。
