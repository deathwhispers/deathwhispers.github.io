---
layout: post
title: ThingsBoard入门实战（四）：设备RPC命令下发
slug: thingsboard-device-rpc-command
type:
  - note
date: 2023-07-14
status: draft
tags:
  - ThingsBoard
categories:
  - IoT
  - ThingsBoard
mood:
weather:
author: deathwhispers
created: 2023-06-06 11:45
updated: 2023-06-06 18:33
---

# ThingsBoard入门实战（四）：设备RPC命令下发

# 设备RPC命令下发

路灯遥测状态我们可以获取了，怎么控制路灯呢？

## 一、分析

对于出现的遥测数据进行一个分析:

- 电量 不可控制
- 开关 可开关
- 亮度 可调

电量的显示比较简单，没什么花俏。 开关和亮度，我们很想操作一下，怎么进行交互呢？

ThingsBoard提供了RPC部件来帮助我们实现。

## 二、RPC部件

### 2.1 开关

选择一个可以用来开关的RPC控件

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038817356-81da4c22-be11-4952-aad0-6bde3eae6ee6.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038817529-8977c8e3-2045-490e-bc58-add02b73e212.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038817659-0b14147c-6d26-4ba7-87f6-9f4deb350e21.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038817754-582b4279-865a-42f6-a189-76a588e3c02d.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038817874-70a8f4a9-90b4-4f56-a0bf-2e2288119967.jpg)

控件是有了，但是Request Timeout.是什么鬼？

别着急，我们需要设备响应刚才的RPC请求 编写响应程序：

# -*- coding:utf-8 -*- import time,random,sys from tb_device_mqtt import TBDeviceMqttClient telemetry = {} def on_server_side_rpc_request(client, request_id, request_body): print(request_id, request_body,telemetry) elif request_body[“method”] == “getTurn”: turn = 0 if “turn” not in telemetry else telemetry[‘turn’] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: turn}) elif request_body[“method”] == “setTurn”: turn = request_body[“params”] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: 1 if turn else 0}) client.send花钱的_telemetry(telemetry) def mock_telemetry(): t = { “battery”:random.choice(range(10,50)), return t def run(token): client = TBDeviceMqttClient(“103.44.238.67”, token) client.set_server_side_rpc_request_handler(on_server_side_rpc_request) client.connect() while True: time.sleep(3) tc = mock_telemetry() client.send_telemetry(tc) if **name** == ‘**main**’: idx = sys.argv[1] token = “token_lamp_1” run(token)

这个程序的作用就是模拟设备响应RPC请求，我们先把它跑起来~

刷新页面：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038817968-93d1c9cc-4183-4bb6-81d9-95cdc4ac9232.jpg)

警告神奇的消失了！

还可以点击开关，完成设备开关灯操作。完美！

### 2.2 亮度

用同样的方法，选择亮度控件：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038818059-fb6e9042-0e3b-4166-98aa-4e5f0b4c91ca.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038818176-e5bd5388-92f3-482b-a0fc-952a9e1247ff.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038818266-14a4cc94-7935-46e9-a945-f5aa087f2dd4.jpg)

在程序里加入RPC方法的实现：

# -*- coding:utf-8 -*- import time,random,sys from tb_device_mqtt import TBDeviceMqttClient telemetry = {} def on_server_side_rpc_request(client, request_id, request_body): print(request_id, request_body,telemetry) if request_body[“method”] == “getLight”: light = random.choice(range(20,60)) if “light” not in telemetry else telemetry[‘light’] client.send_rpc_reply(request_id, light) telemetry.update({“light”: light}) elif request_body[“method”] == “setLight”: light = request_body[“params”] client.send_rpc_reply(request_id, light) telemetry.update({“light”: light}) elif request_body[“method”] == “getTurn”: turn = 0 if “turn” not in telemetry else telemetry[‘turn’] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: turn}) elif request_body[“method”] == “setTurn”: turn = request_body[“params”] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: 1 if turn else 0}) client.send_telemetry(telemetry) def mock_telemetry(): t = { “battery”:random.choice(range(10,50)), } return t def run(token): client = TBDeviceMqttClient(“103.44.238.67”, token) client.set_server_side_rpc_request_handler(on_server_side_rpc_request) client.connect() while True: time.sleep(3) tc = mock_telemetry() client.send_telemetry(tc) if **name** == ‘**main**’: idx = sys.argv[1] token = “token_lamp_1” run(token)

成功对接，点击亮度条可调亮度，完美*2！

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038818356-4610b3d8-b461-4895-a030-48d2e19177df.jpg)

## 三、下一步

本节在详情面板中使用RPC控件完成对远程设备的操控，下节我们继续完善详情面板。