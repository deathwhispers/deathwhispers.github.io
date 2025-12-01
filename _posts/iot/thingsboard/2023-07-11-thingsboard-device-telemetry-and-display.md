---
layout: post
title: ThingsBoard入门实战（三）：设备遥测与展示
slug: thingsboard-device-telemetry-and-display
type:
  - note
date: 2023-07-11
status: draft
tags:
  - ThingsBoard
categories:
  - IoT
  - ThingsBoard
mood:
weather:
author: deathwhispers
created: 2023-06-05 11:45
updated: 2023-06-05 18:33
---
# ThingsBoard入门实战（三）：设备遥测与展示

# 设备遥测与展示

## 一、设备基础概念

观察下设备面板，有以下几部分构成：

- 属性：基础信息，比较稳定
- 遥测：需要测量的状态信息
- 警告：设备或者设备监控的状态出现问题
- 事件：发生在设备上的事件
- 关联：设备属于谁，在哪个资产上等等
- 审计日志：谁在平台上对设备做了什么操作

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038804200-5adf0caf-754f-4f3a-9f75-58f0a1df845a.jpg)

其中属性是**基础**，遥测是**核心**。

## 二、属性

ThingsBoard能够给实体分配自定义属性并进行管理。

**属性** 代表设备基本信息, 以key-value格式存在, 可以与IoT设备无缝兼容。

属性分客户端属性，服务端属性和共享属性, 使用官方的图示比较容易理解。

- 客户端属性

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038804307-52b6a473-6896-4af0-b394-aacc4a711ff4.png)

- 服务端属性

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038804394-59341dd1-73d8-420a-be3b-fe2647391d58.png)

- 共享属性

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038804475-3528759a-294d-4892-9b21-3810a5db3f50.png)

## 三、遥测

物联网的核心目的之一就是通过传感器采集相应的遥测数据上传。对此，ThingsBoard 提供了大量与遥测数据操作相关的功能：

- **采集** 使用MQTT, CoAP或者HTTP协议采集设备数据。
- **存储** 在Cassandra（高效、可扩展、能容错的NoSQL数据库）中存储时序数据。
- **查询** 查询最新时序数据值，或查询特定时间段内的所有数据。
- **订阅** 使用websockets订阅数据更新(用于可视化或实时分析)。
- **可视化** 使用可配置和可配置的小部件以及仪表盘可视化时序数据。
- **过滤和分析** 使用灵活的规则引擎过滤和分析数据(/docs/user-guide/rule-engine/)。
- **事件警报** 根据采集的数据触发事件警报。
- **数据传输** 过规则引擎节点实现与外部数据交互（例如Kafka或RabbitMQ规则节点）

官方有个说明蓝图，一目了然：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038804561-36be732f-f126-466e-8d1f-f552cf6565d8.png)

## 四、路灯设备定义

先定义一个简单的路灯设备，具有4个遥测状态：

- 开关
- 亮度
- 电量
- 位置信息

通过章节的进行，逐步将这几个遥测状态进行处理和展示。

## 五、设备模拟

想要连接设备，首先要搞清楚下载上传数据的[API](https://so.csdn.net/so/search?q=API&spm=1001.2101.3001.7020) 以及 设备和平台连接的API。

### 设备API

和云平台进行通信的主要api是device api, 部署好平台就直接可以在浏览器中访问

http://IP:9090/swagger-ui/#/device-api-controller

### 遥测模拟

从Github下载有设备信息上传功能的设备客户端的sdk。

https://github.com/thingsboard/thingsboard-python-client-sdk

或者直接使用pip3安装：

pip3 install tb-mqtt-client

通过mqtt链接，向设备平台上传模拟设备的遥测数据：

# -*- coding:utf-8 -*- import random from time import sleep from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo def send_to(token,telemetry): client = TBDeviceMqttClient(“IP”, token) # Connect to ThingsBoard client.connect() # Sending telemetry without checking the delivery status client.send_telemetry(telemetry) # Sending telemetry and checking the delivery status (QoS = 1 by default) result = client.send_telemetry(telemetry) # get is a blocking call that awaits delivery status success = result.get() == TBPublishInfo.TB_ERR_SUCCESS print(success) # Disconnect from ThingsBoard client.disconnect() def mock_telemetry(): t = { “turn”: 1, “light”: random.choice(range(0,100)), “battery”:random.choice(range(10,60)), } return t if **name** == ‘**main**’: while True: sleep(3) tokens = [“token_lamp_1”] for token in tokens: telemetry = mock_telemetry() send_to(token,telemetry)

**请注意!** pip上并不是最新版本,如果需要使用http,需要下载然后直接本地安装

git clone git@github.com:thingsboard/thingsboard-python-client-sdk.git

## 六、电量展示

### [仪表盘](https://so.csdn.net/so/search?q=%E4%BB%AA%E8%A1%A8%E7%9B%98&spm=1001.2101.3001.7020)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038804642-a589e306-acae-4f6f-b6c1-019ddac5edcc.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038804752-35c97ffc-9ed7-4049-8063-204138d67f14.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038804859-e18dd2f1-6fe7-471e-bf10-1d3f12787362.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038804959-657e7985-40d1-4887-8f1c-d637029189ef.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805116-31bc6bbd-6925-45af-9788-c22cb85e5967.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805229-d13ad5e5-bc86-4624-9683-a124d8b46462.jpg)

### 部件：电量展示

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805332-0db3e433-8b82-48ee-ae28-827660e343f2.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805440-06668920-8c92-49a5-8d2c-c3e3c5e602b4.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805544-298896b2-7dbf-4019-960d-67ceb8d025e5.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805643-e0d2547a-d887-4071-8bd6-49c99f5ee083.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805764-937adfad-de41-4aee-a086-0bf4815cf448.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805866-d9d4db5c-4979-4e27-9e46-1394287c8a84.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038805978-b1592193-7264-45cb-918a-eff2c24d95d3.jpg)

按图操作就好。

### 设为首页

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038806090-bab26e23-1cd3-4437-8ea7-385b0096bdc2.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038806189-e9bf5a9d-b1c2-4726-b395-5e969afa4368.jpg)

可以看到, 首页已经变成了设备的电量图示。

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038806287-6df3dcf0-606e-42cf-b26f-41fda477317b.jpg)

## 七、下一步

这节我们主要讲解了设备遥测的模拟和展示，下节是另一个核心功能：命令下发