---
layout: post
title: ThingsBoard入门实战（四）：设备RPC命令下发
slug: thingsboard-device-rpc-command
type:
- note
date: 2023-07-14
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

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/c85acd56424b2395a9bad1a9033ce459.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/5f3c1a6bf2e70303228ec8c9ec629827.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/6544b2a713c2262797d94f5bda4ba195.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/a5267472bdf06392a015e08b3866c968.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/5d1586085983ec268646b505e056211f.jpg)

控件是有了，但是Request Timeout.是什么鬼？

别着急，我们需要设备响应刚才的RPC请求 编写响应程序：

# -*- coding:utf-8 -*- import time,random,sys from tb_device_mqtt import TBDeviceMqttClient telemetry = {} def on_server_side_rpc_request(client, request_id, request_body): print(request_id, request_body,telemetry) elif request_body[“method”] == “getTurn”: turn = 0 if “turn” not in telemetry else telemetry[‘turn’] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: turn}) elif request_body[“method”] == “setTurn”: turn = request_body[“params”] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: 1 if turn else 0}) client.send花钱的_telemetry(telemetry) def mock_telemetry(): t = { “battery”:random.choice(range(10,50)), return t def run(token): client = TBDeviceMqttClient(“103.44.238.67”, token) client.set_server_side_rpc_request_handler(on_server_side_rpc_request) client.connect() while True: time.sleep(3) tc = mock_telemetry() client.send_telemetry(tc) if **name** == ‘**main**’: idx = sys.argv[1] token = “token_lamp_1” run(token)

这个程序的作用就是模拟设备响应RPC请求，我们先把它跑起来~

刷新页面：

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/20510e0b35f3a14bc60d93e58d2a73cf.jpg)

警告神奇的消失了！

还可以点击开关，完成设备开关灯操作。完美！

### 2.2 亮度

用同样的方法，选择亮度控件：

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/4aa8c3944a29a4d040924c36a3479374.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/4d3c9a2e501efaabdaff1343326a25b6.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/1fb6ce5de2a9ca86a4d2afae53c99162.jpg)

在程序里加入RPC方法的实现：

# -*- coding:utf-8 -*- import time,random,sys from tb_device_mqtt import TBDeviceMqttClient telemetry = {} def on_server_side_rpc_request(client, request_id, request_body): print(request_id, request_body,telemetry) if request_body[“method”] == “getLight”: light = random.choice(range(20,60)) if “light” not in telemetry else telemetry[‘light’] client.send_rpc_reply(request_id, light) telemetry.update({“light”: light}) elif request_body[“method”] == “setLight”: light = request_body[“params”] client.send_rpc_reply(request_id, light) telemetry.update({“light”: light}) elif request_body[“method”] == “getTurn”: turn = 0 if “turn” not in telemetry else telemetry[‘turn’] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: turn}) elif request_body[“method”] == “setTurn”: turn = request_body[“params”] client.send_rpc_reply(request_id, turn) telemetry.update({“turn”: 1 if turn else 0}) client.send_telemetry(telemetry) def mock_telemetry(): t = { “battery”:random.choice(range(10,50)), } return t def run(token): client = TBDeviceMqttClient(“103.44.238.67”, token) client.set_server_side_rpc_request_handler(on_server_side_rpc_request) client.connect() while True: time.sleep(3) tc = mock_telemetry() client.send_telemetry(tc) if **name** == ‘**main**’: idx = sys.argv[1] token = “token_lamp_1” run(token)

成功对接，点击亮度条可调亮度，完美*2！

![](/assets/images/iot/thingsboard/thingsboard-device-rpc-command/8b7f562bd82def75d8f11e2fcd8068df.jpg)

## 三、下一步

本节在详情面板中使用RPC控件完成对远程设备的操控，下节我们继续完善详情面板。
