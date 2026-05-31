---
layout: post
title: ThingsBoard入门实战（二）：ThingsBoard 设备接入
author: deathwhispers
date: 2023-07-04
slug: thingsboard-device-access
categories:
- IoT
- ThingsBoard
tags:
- IoT
- ThingsBoard
type: note
status: draft
created: 2023-06-04 11:45
updated: 2023-06-04 18:33
---

# ThingsBoard入门实战（二）：ThingsBoard 设备接入

# ThingsBoard 设备接入

设备接入并不一定需要真正的设备，我们可以通过程序。或者命令来模拟设备，向平台发送信息。 这节我们先为用户分配一个设备，然后通过模拟设备命令更新设备的状态(遥测值)。

## 一、设备配置/设备类型

添加一个叫"路灯"的设备配置。

**设备配置**听起来比较抽象，可以认为是设备类型或者是设备类型的配置。实际上，ThingsBoard 中很多时候让选择设备类型，就是选的这个。

![](/assets/images/iot/thingsboard/thingsboard-device-access/4a7acdb16585621ee0c5b9e7a9e19982.jpg)

按照提示填写待添加设备类型的信息，

![](/assets/images/iot/thingsboard/thingsboard-device-access/5bb4ba2d38f34a8bc96a4db4e6b88acb.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-access/a8d255e022644a5210a89db3019e53c2.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-access/d061aff3594bde1660dce186dc18775e.jpg)

设备类型路灯添加成功：

![](/assets/images/iot/thingsboard/thingsboard-device-access/e7a393851ee6e622744dc8498a6abeba.jpg)

## 二、设备

接下来添加一个叫"路灯1"的设备：

![](/assets/images/iot/thingsboard/thingsboard-device-access/c55096403bb5b3781d6bcc6c6f53fa00.jpg)

按照提示填写待添加设备的信息，

![](/assets/images/iot/thingsboard/thingsboard-device-access/06360013861e1f45a426fbef7aa117aa.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-access/5be94bd5224a3c2a321fb2f6ea490e18.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-access/162903b1173ca73a7b904f68b9aca23d.jpg)

设备**路灯1**添加成功：

![](/assets/images/iot/thingsboard/thingsboard-device-access/7709c424d1ecb6e2e002e641bf250cd9.jpg)

## 三、设备接入

ThingsBoard支持使用HTTP,COAP,MQTT三种方式直接接入平台，我们就使用3种命令行分别模拟路灯的5个状态。

### HTTP

使用[curl](https://so.csdn.net/so/search?q=curl&spm=1001.2101.3001.7020)发送开关和亮度信息：

curl -v -X POST -d '{"turn":"1","light":"90"}' http://{SERVER_IP}:9090/api/v1/A1_TEST_TOKEN/telemetry –header "Content-Type:application/json"

### COAP

mqtt命令需要安装npm库mqtt，安装指令npm install coap-cli -g 使用coap发送电量信息：

coap post coap://{SERVER_IP}:5683/api/v1/A1_TEST_TOKEN/telemetry -p '{"battery":"90"}'

### MQTT

mqtt命令需要安装npm库mqtt，安装指令npm install mqtt -g 使用mqtt发送经纬度信息：

mqtt pub -v -h "{SERVER_IP}" -p 1883 -t "v1/devices/me/telemetry" -u 'A1_TEST_TOKEN' -m '{"latitude":"22.54845664","longitude":"114.06455184"}'

![](/assets/images/iot/thingsboard/thingsboard-device-access/278222561ca4d54d6c56078d1feabd3d.jpg)

**在实际工作中，选择一种协议就可以了。** 由于MQTT协议已经成为事实上的物联网标准，我们后面的操作都使用**MQTT协议**来进行。

## 四、下一步

三种常见协议之外的接入会麻烦点，需要使用官方的另一个项目tb-gateway了，我们以后会专门开个专题来讲他。 下一节我们围绕刚分配的路灯设备做一个小的接入-管理-展示闭环。
