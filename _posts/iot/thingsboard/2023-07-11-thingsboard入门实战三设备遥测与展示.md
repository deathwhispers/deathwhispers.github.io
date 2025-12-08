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

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/cb21fd165a4ea843f3f48dff7bdf3021.jpg)

其中属性是**基础**，遥测是**核心**。

## 二、属性

ThingsBoard能够给实体分配自定义属性并进行管理。

**属性** 代表设备基本信息, 以key-value格式存在, 可以与IoT设备无缝兼容。

属性分客户端属性，服务端属性和共享属性, 使用官方的图示比较容易理解。

- 客户端属性

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/92d77bc13cf45fe4b8561a771a711a5b.png)

- 服务端属性

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/ba563555ced97871036d70fc7b0554c5.png)

- 共享属性

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/24e81f0c287b21a72dd4f10a070ef9a6.png)

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

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/e4d6cbf1353abe4e4471da85af0ea8fd.png)

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

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/cbd631228e52fd4a5efdf52d6782d437.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/0636a1a80d06b760374ccb12abdcb87b.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/a352e3c6aa98a3b2e2c1a5f34ea7ba5a.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/f721ec5ef64d237397d21065d7764528.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/6fea6fccd9a171ca62934a39e6624539.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/099aa38b2046a46de6738be2b4175d4a.jpg)

### 部件：电量展示

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/f0401a745c62577631b0c4eb6d061664.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/1e171e03bdd33d3d731d752ace57397b.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/c7bfb44643ba97b0de7a05812e59cdfa.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/ea0434677ec956280aaa0d0bd9ca307b.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/51ec25701137d78a90d67597466b1523.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/8e6b8e281cc9a598f37ffd086b652e9c.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/739833c8172aaefab6a5a519e0070701.jpg)

按图操作就好。

### 设为首页

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/91b5d6f6a9a6dcfe4a4bb0a207b70ebc.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/ed9fb0abb647b939fc1f7f3faa866d08.jpg)

可以看到, 首页已经变成了设备的电量图示。

![](/assets/images/iot/thingsboard/thingsboard-device-telemetry-and-display/e05a6e4e76b5106448c2e783564777ce.jpg)

## 七、下一步

这节我们主要讲解了设备遥测的模拟和展示，下节是另一个核心功能：命令下发