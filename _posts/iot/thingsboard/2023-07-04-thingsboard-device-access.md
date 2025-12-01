---
layout: post
title: ThingsBoard入门实战（二）：ThingsBoard 设备接入
slug: thingsboard-device-access
type:
  - note
date: 2023-07-04
status: draft
tags:
  - ThingsBoard
categories:
  - IoT
  - ThingsBoard
mood:
weather:
author: deathwhispers
created: 2023-06-04 11:45
updated: 2023-06-04 18:33
---
# ThingsBoard入门实战（二）：ThingsBoard 设备接入

# ThingsBoard 设备接入

设备接入并不一定需要真正的设备，我们可以通过程序。或者命令来模拟设备，向平台发送信息。 这节我们先为用户分配一个设备，然后通过模拟设备命令更新设备的状态(遥测值)。

## 一、设备配置/设备类型

添加一个叫”路灯”的设备配置。

**设备配置**听起来比较抽象，可以认为是设备类型或者是设备类型的配置。实际上，ThingsBoard 中很多时候让选择设备类型，就是选的这个。

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038807603-b6c13385-3675-4396-bd24-82b9c91278fb.jpg)

按照提示填写待添加设备类型的信息，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038807707-4e8e4532-2a7b-445e-969e-1a851a19b1b8.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038807808-3e622985-ec9a-4685-bf63-c941e619ac71.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038807920-e31ff4c7-bf4a-4230-b80e-75b008978682.jpg)

设备类型路灯添加成功：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038808058-a443b0a4-9a71-445e-a701-8f8189177f88.jpg)

## 二、设备

接下来添加一个叫”路灯1”的设备：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038808196-54b9e658-b535-4a3d-b430-f6bbc5b8a96d.jpg)

按照提示填写待添加设备的信息，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038808329-aaca4923-726b-4f7f-a061-feb4a314f7c3.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038808441-fd758d9d-4c0a-4065-8cca-c26cac6c0675.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038808553-95d05f7f-2628-4df1-8edf-1644bf86f7b3.jpg)

设备**路灯1**添加成功：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038808653-d137556f-441b-4671-be4e-7935ae4672a6.jpg)

## 三、设备接入

ThingsBoard支持使用HTTP,COAP,MQTT三种方式直接接入平台，我们就使用3种命令行分别模拟路灯的5个状态。

### HTTP

使用[curl](https://so.csdn.net/so/search?q=curl&spm=1001.2101.3001.7020)发送开关和亮度信息：

curl -v -X POST -d ‘{“turn”:“1”,“light”:“90”}’ http://{SERVER_IP}:9090/api/v1/A1_TEST_TOKEN/telemetry –header “Content-Type:application/json”

### COAP

mqtt命令需要安装npm库mqtt，安装指令npm install coap-cli -g 使用coap发送电量信息：

coap post coap://{SERVER_IP}:5683/api/v1/A1_TEST_TOKEN/telemetry -p ‘{“battery”:“90”}’

### MQTT

mqtt命令需要安装npm库mqtt，安装指令npm install mqtt -g 使用mqtt发送经纬度信息：

mqtt pub -v -h “{SERVER_IP}” -p 1883 -t “v1/devices/me/telemetry” -u ‘A1_TEST_TOKEN’ -m ‘{“latitude”:“22.54845664”,“longitude”:“114.06455184”}’

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038808782-2e80ddd7-a842-4d3e-aaa8-9a9551f3d2c4.jpg)

**在实际工作中，选择一种协议就可以了。** 由于MQTT协议已经成为事实上的物联网标准，我们后面的操作都使用**MQTT协议**来进行。

## 四、下一步

三种常见协议之外的接入会麻烦点，需要使用官方的另一个项目tb-gateway了，我们以后会专门开个专题来讲他。 下一节我们围绕刚分配的路灯设备做一个小的接入-管理-展示闭环。