---
layout: post
title: 使用MQTT服务网关接入设备
slug: jetlinks-mqtt-connection
type:
  - note
date: 2023-05-29
status: draft
tags:
  - JetLinks
categories:
  - IoT
mood:
weather:
author: deathwhispers
created: 2023-05-29 11:45
updated: 2023-05-29 18:33
---

# 使用MQTT服务网关接入设备

本文档以MQTTX为例，介绍使用第三方软件以MQTT协议接入物联网平台。

## [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%88%9B%E5%BB%BA%E5%8D%8F%E8%AE%AE) 创建协议

自定义消息协议创建，请参考[消息协议定义](http://doc.jetlinks.cn/basics-guide/protocol-support.html)。

**例**

i. 选择 设备接入–>协议管理–> 点击新建按钮

![](/assets/img/new-protocol.878fbbf2.png)

ii.输入协议ID

iii. 输入型号名称

iv. 选择型号类型为 jar

v. 输入类名org.jetlinks.protocol.official.JetLinksProtocolSupportProvider

vi. 上传jar包jetlinks-official-protocol-2.0-SNAPSHOT.jar， 请检出[jetlinks-official-protocol (opens new window)](https://github.com/jetlinks/jetlinks-official-protocol)自行打包。

vii. 点击确认，完成协议新增。

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%88%9B%E5%BB%BA%E5%AE%8C%E6%88%90%E4%BF%A1%E6%81%AF%E5%B1%95%E7%A4%BA) 创建完成信息展示

![](/assets/img/product-protocol.c07eaa2e.png)

viii. 在操作列表中将协议发布。

![](/assets/img/protocol-release.3ad7301e.png)

## [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%88%9B%E5%BB%BA%E4%BA%A7%E5%93%81) 创建产品

**例**

i.下载型号文件[配置JSON](http://doc.jetlinks.cn/basics-guide/files/device-connection/%E8%AE%BE%E5%A4%87%E5%9E%8B%E5%8F%B7-%E6%99%BA%E8%83%BD%E6%B8%A9%E6%8E%A7.json)

ii. 选择 设备管理–>产品–> 点击导入配置按钮

![](/assets/img/import-product.cf7b01cb.png)

iii. 选择[配置JSON](http://doc.jetlinks.cn/basics-guide/files/device-connection/%E8%AE%BE%E5%A4%87%E5%9E%8B%E5%8F%B7-%E6%99%BA%E8%83%BD%E6%B8%A9%E6%8E%A7.json)文件

注意：

上传文件需要将standalone/src/main/resources/application.yml中的static-location修改为http://后台服务ip:8848/upload，参考[协议上传问题](http://doc.jetlinks.cn/common-problems/install.html#%E5%8D%8F%E8%AE%AE%E5%8F%91%E5%B8%83%E5%A4%B1%E8%B4%A5%E6%88%96%E5%87%BA%E7%8E%B0%E4%B8%8D%E6%94%AF%E6%8C%81%E7%9A%84%E5%8D%8F%E8%AE%AE%EF%BC%9Axxx)

iv.产品导入完成后，产品状态为未发布,效果如下图

![](/assets/img/device-product-unpublished.95fe628c.png)

v.点击刚导入产品中的…按钮会出现发布按钮，点击发布按钮完成产品发布，导航栏中发布状态变为已发布代表发布成功。

![](/assets/img/device-product-published.8f504bd8.png)

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%88%9B%E5%BB%BA%E6%88%90%E5%8A%9F%E7%9A%84%E4%BA%A7%E5%93%81%E4%BF%A1%E6%81%AF%E5%B1%95%E7%A4%BA) 创建成功的产品信息展示

i. 点击产品中

编辑

链接查看和编辑产品的基本信息

![](/assets/img/compile.0f2e9cf0.png)

ii. 点击产品中

查看

→

物模型

,对产品设备定义

![](/assets/img/check.05c164a5.png)

![](/assets/img/Physical-model.be1ee9ca.png)

iii. 点击属性定义信、事件定义对应操作下的编辑按钮查看更详细的型号息

属性定义参数：

![](/assets/img/device-product-info1.287b6211.png)

功能定义参数：

![](/assets/img/device-product-info2.65db5b19.png)

事件定义参数：

![](/assets/img/device-product-info3.79ae8c33.png)

## [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%88%9B%E5%BB%BA%E8%AE%BE%E5%A4%87) 创建设备

自定义创建设备，请参考[添加设备](http://doc.jetlinks.cn/basics-guide/device-manager.html#%E6%B7%BB%E5%8A%A0%E8%AE%BE%E5%A4%87)。

**例**

i. 下载设备Excel文件[设备Excel](http://doc.jetlinks.cn/basics-guide/files/device-connection/%E6%99%BA%E8%83%BD%E6%B8%A9%E6%8E%A7%E6%B5%8B%E8%AF%95%E8%AE%BE%E5%A4%87.xlsx)

ii. 选择 设备管理–>设备–> 其他批量操作–>批量导入设备

![](/assets/img/import-device.893fc4ee.png)

iii. 选择需要导入的产品,点击文件上传

![](/assets/img/choose-device-product.874329f6.png)

iv. 设备导入完成效果如下图

![](/assets/img/device-instance-not-active.afd4cd8b.png)

v. 点击上图中启用链接完成设备激活，状态栏中发布状态变为离线代表设备激活成功。

![](/assets/img/device-instance-offline.319ae76a.png)

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%88%9B%E5%BB%BA%E6%88%90%E5%8A%9F%E7%9A%84%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF%E5%B1%95%E7%A4%BA) 创建成功的设备信息展示

i. 点击查看链接可以看到设备基本信息（实例信息）

![](/assets/img/device-instance-general-check.9e847db5.png)

![](/assets/img/device-instance-general-info.b43d753a.png)

ii. 设备运行状态信息（运行状态）

![](/assets/img/device-instance-run-info.27ada8c3.png)

iii.设备功能信息（设备功能）

![](/assets/img/device-instance-function.d795c3a5.png)

iv. 设备日志（日志管理）

![](/assets/img/device-instance-log.550e4be7.png)

v.告警设置

![](/assets/img/device-instance-alarm.de9fe90b.png)

vi.可视化

![](/assets/img/device-instance-visual.4dcbc8bf.png)

vii.设备影子

![](/assets/img/device-instance-sign.bff329fd.png)

## [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%88%9B%E5%BB%BA%E7%BD%91%E5%85%B3%E9%85%8D%E7%BD%AE) 创建网关配置

参照[启动设备网关服务](http://doc.jetlinks.cn/basics-guide/course/device-gateway.html)

**例**

i.创建MQTT服务网络组件以及MQTT服务组件配置

![](/assets/img/mqtt-config.342954a5.png)

注意：

此处使用的端口为1889，docker启动时没有默认开启，使用docker启动jetlinks时请映射1889端口或者使用1883端口。

ii.启动MQTT服务组件（灰色为未启动，蓝色为启动）

![](/assets/img/mqtt-start.ceebf2f4.png)

iii.创建MQTT服务设备网关以及MQTT服务设备网关配置

![](/assets/img/mqtt-gateway-info.5bcea38d.png)

警告

大部分情况，请勿勾选认证协议,认证协议的作用是: 使用指定的协议来进行统一的认证。不勾选时，则使用产品里选择的协议来进行认证， 这2种认证方式在协议包内的实现方式是不同的。大部分情况下不需要选择。

iv.启动MQTT服务设备网关，点击

启动

，

状态

变为

已启动

![](/assets/img/mqtt-gateway-start1.0d7fa79e.png)

![](/assets/img/mqtt-gateway-start2.f6130070.png)

注意：

大部分情况无需选择认证协议.

## [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E4%BD%BF%E7%94%A8mqttx%E6%8E%A5%E5%85%A5) 使用MQTTX接入

1.下载并安装MQTTX软件。请访问[MQTTX官网 (opens new window)](https://mqttx.app/zh)。

2.打开MQTTX软件，点击New Connection创建一个连接。

![](/assets/img/mqttx-index.1cf3213f.png)

3.设置连接参数。

注意

设置参数时，请确保参数值中或参数值的前后均没有空格。

i. 设置基本信息

![](/assets/img/mqtt-connection-general.c7d17922.png)

| 参数 | 说明 |
| --- | --- |
| Name | 输入您的自定义名称。 |
| Client ID | 设备Id。本文档中为演示设备test001 |
| Host | 连接域名。本地连接可直接填写 127.0.0.1,如为远程连接，请填写远程连接地址 |
| Port | 设置为1889 |
| Username | 接入账号 |
| Password | 接入密码 |

提示

username和password

[自动生成器 (opens new window)](http://doc.jetlinks.cn/basics-guide/mqtt-auth-generator.html)

![](/assets/img/mqtt-connection-user.4eae0dcb.png)

4.设置完成后，单击右下角的**OK**。

## [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF) 设备消息

设备连接上平台，并进行一些基本的事件收发、属性读取操作。

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E8%AE%BE%E5%A4%87%E4%B8%8A%E4%B8%8B%E7%BA%BF) 设备上下线

单击 MqttX 中Connect进行连接

![](/assets/img/mqtt-connection.818f3cf8.png)

平台中设备状态变为上线即为连接成功

![](/assets/img/device-online.dc3d00bf.png)

点击该设备的查看→日志管理，在设备日志模块可以看到设备上线日志

![](/assets/img/device-online-log.f5bca109.png)

单击 MqttX 中Disconnect断开连接

![](/assets/img/mqtt-connection-stop.4fe1307d.png)

平台中设备状态变为离线即为断开连接成功

![](/assets/img/device-offline.def91fef.png)

点击该设备的查看→日志管理，在设备日志模块可以看到设备离线日志

![](/assets/img/device-offline-log.c9e5adf4.png)

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E8%AF%BB%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7) 读取设备属性

注意

第2步中回复平台属性值需要在第1步平台发送订阅以后的十秒钟内完成，否则平台会视为该次操作超时，导致读取属性值失败。

1.平台告知设备（MQTTX）需要设备返回设备属性

单击设备页面中test001设备对应的查看链接

选择弹出框中运行状态板块

单击属性刷新

![](/assets/img/device-property-refresh.f7cf28bd.png)

MQTTX会收到平台下发的订阅

![](/assets/img/mqttfx-sub-read-property.47aa94fe.png)

注意:

复制好订阅该topic收到的消息中的messageId。此messageId将作为回复与平台设备属性的凭据之一

2.设备（MQTTX）回复平台设备属性值

在MQTTX上发送消息，发送平台所需要的设备属性值。

i 输入一个回复平台属性值消息Topic(这里的为/{productId}/{deviceId}/properties/read/reply)和要发送的消息内容， 单击Publish，向平台推送该消息。

![](/assets/img/mqttfx-replay-device-property.b18d73a8.png)

| 参数 | 说明 |
| --- | --- |
| messageId | 平台所下发的messageId值 |
| deviceId | 设备Id |
| timestamp | 当前时间戳 |
| success | 成功标识 |
| properties | 设备属性值对象。例如： { “temperature”:“50”} |

该文档所使用的回复内容

```plain text
{
 "timestamp":1601196762389,
 "messageId":"第一次平台订阅设备,MQTTX所收到的messageId值",
 "properties":{"temperature":"50"},
 "deviceId":"test001",
 "success":true
}
```

iii. 平台收到MqttX推送的属性值

![](/assets/img/mqttfx-replyed-property-value.831c167c.png)

iv. 读取设备属性回复的日志

![](/assets/img/read-device-property-reply-log.2b6867c1.png)

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%80%BC%E5%AE%8C%E6%95%B4%E6%BC%94%E7%A4%BA) 获取设备属性值完整演示

注意：在下图中，从在界面上刷新属性开始直到动图结束的所有操作，需要在十秒钟内完成。否则平台会视为该次操作超时，导致读取属性值失败。

![](/assets/img/read-device-property.f7cac8f9.gif)

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E8%AE%BE%E5%A4%87%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5) 设备事件上报

MQTTX 推送设备事件消息到平台

以火灾报警事件为例。

1.在MQTTX上，订阅topic/{productId}/{deviceId}/event/{eventId}。

2.输入事件上报Topic和要发送的事件内容，单击Publish按钮，向平台推送该事件消息。

![](/assets/img/mqttfx-device-event-report.e51158c1.png)

该文档所使用的回复内容

```plain text
{
 "timestamp":1627960319,
 "messageId":"1422143789942595584",
 "data":{"a_name":"未来科技城",
  "b_name":"C2 栋",
  "l_name":"12-05-2012"}
}
```

| 参数 | 说明 |
| --- | --- |
| timestamp | 毫秒时间戳 |
| messageId | 随机消息ID |
| data | 上报数据，类型与物模型事件中定义的类型一致 |

3.事件上报设备日志

![](/assets/img/device-event-report-log.5a4b2cf4.png)

4.事件上报内容

![](/assets/img/device-event-info.b88615f8.png)

![](/assets/img/device-event-info1.8a1374cc.png)

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E4%B8%8A%E6%8A%A5) 地理位置上报

1. 物模型中添加地理位置。通过属性定义添加地理位置类型属性。

![](/assets/img/insert-geo-property.17bb75e5.png)

2. 在设备产品详情页面点击
应用配置
按钮。
![](/assets/img/start-model.a46d1501.png)
3. 使用mqttX连接到平台，设备上线后推送地理位置消息到平台， 此处使用topic为
/{productId}/{deviceId}/properties/report
。

![](/assets/img/push-geo.2516c8c7.png)

此处使用的报文为：

```plain text
{
 "timestamp":1601196762389,
 "messageId":"ddddd",
 "properties":{
  "geoPoint": "102.321,36.523"
 }
}
```

注意：

上报geo地理位置类型数据有三种格式，一是字符串以逗号分隔，如：“102.321,36.523”;二是数组类型，如:[102.321,36.523];三是map类型，如：{“lat”:102.321,“lon”:36.523}。

4. 上报成功后将在设备的运行状态中显示。

![](/assets/img/device-info-geo.22f94d2d.png)

也可查看上报历史消息。

![](/assets/img/geo-history.9d62c615.png)

注意：

物模型中的标签也可创建geo类型，但不可通过标签上报地理位置信息，只能通过属性上报。地理位置标签将主要运用在地图查询中。

### [#](http://doc.jetlinks.cn/advancement-guide/mqtt-connection.html#%E8%B0%83%E7%94%A8%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD) 调用设备功能

5. MqttX连接上平台

2.选择设备功能模块,点击执行,向设备发送topic

![](/assets/img/device-function.30195827.png)

3.在MqttX订阅topic为

/{productId}/{deviceId}/function/invoke/reply

。

![](/assets/img/mqttx-device-function-replay.304ac535.png)

此处使用的报文为：

```plain text
{
 "timestamp":1601196762389,
 "messageId":"1422497215780651008",
 "output":"success",
 "success":true
}
```

| 参数 | 说明 |
| --- | --- |
| timestamp | 毫秒时间戳 |
| messageId | 与设备下发中的messageId相同” |
| output | 返回执行结果,具体类型与物模型中功能输出类型一致 |
| success | 成功状态 |

4.设备功能调用成功

![](/assets/img/mqttx-device-function-success.5dcd6cd7.png)

%23%20%E4%BD%BF%E7%94%A8MQTT%E6%9C%8D%E5%8A%A1%E7%BD%91%E5%85%B3%E6%8E%A5%E5%85%A5%E8%AE%BE%E5%A4%87%0A%0A%E6%9C%AC%E6%96%87%E6%A1%A3%E4%BB%A5MQTTX%E4%B8%BA%E4%BE%8B%EF%BC%8C%E4%BB%8B%E7%BB%8D%E4%BD%BF%E7%94%A8%E7%AC%AC%E4%B8%89%E6%96%B9%E8%BD%AF%E4%BB%B6%E4%BB%A5MQTT%E5%8D%8F%E8%AE%AE%E6%8E%A5%E5%85%A5%E7%89%A9%E8%81%94%E7%BD%91%E5%B9%B3%E5%8F%B0%E3%80%82%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%2588%259B%25E5%25BB%25BA%25E5%258D%258F%25E8%25AE%25AE)%20%E5%88%9B%E5%BB%BA%E5%8D%8F%E8%AE%AE%0A%0A%3E%20%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B6%88%E6%81%AF%E5%8D%8F%E8%AE%AE%E5%88%9B%E5%BB%BA%EF%BC%8C%E8%AF%B7%E5%8F%82%E8%80%83%5B%E6%B6%88%E6%81%AF%E5%8D%8F%E8%AE%AE%E5%AE%9A%E4%B9%89%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Fprotocol-support.html)%E3%80%82%0A%0A**%E4%BE%8B**%0A%0Ai.%20%E9%80%89%E6%8B%A9%20%60%E8%AE%BE%E5%A4%87%E6%8E%A5%E5%85%A5%60%5C–%3E%60%E5%8D%8F%E8%AE%AE%E7%AE%A1%E7%90%86%60%5C–%3E%20%E7%82%B9%E5%87%BB%60%E6%96%B0%E5%BB%BA%60%E6%8C%89%E9%92%AE%0A%0A!%5B%E6%96%B0%E5%BB%BA%E5%8D%8F%E8%AE%AE%E5%AF%BC%E8%88%AA%5D(%2Fassets%2Fimg%2Fnew-protocol.878fbbf2.png)%0A%0Aii.%E8%BE%93%E5%85%A5%E5%8D%8F%E8%AE%AEID%0A%0Aiii.%20%E8%BE%93%E5%85%A5%E5%9E%8B%E5%8F%B7%E5%90%8D%E7%A7%B0%0A%0Aiv.%20%E9%80%89%E6%8B%A9%E5%9E%8B%E5%8F%B7%E7%B1%BB%E5%9E%8B%E4%B8%BA%20%60jar%60%0A%0Av.%20%E8%BE%93%E5%85%A5%E7%B1%BB%E5%90%8D%60org.jetlinks.protocol.official.JetLinksProtocolSupportProvider%60%0A%0Avi.%20%E4%B8%8A%E4%BC%A0jar%E5%8C%85%60jetlinks-official-protocol-2.0-SNAPSHOT.jar%60%EF%BC%8C%20%E8%AF%B7%E6%A3%80%E5%87%BA%5Bjetlinks-official-protocol%20(opens%20new%20window)%5D(https%3A%2F%2Fgithub.com%2Fjetlinks%2Fjetlinks-official-protocol)%E8%87%AA%E8%A1%8C%E6%89%93%E5%8C%85%E3%80%82%0A%0Avii.%20%E7%82%B9%E5%87%BB%E7%A1%AE%E8%AE%A4%EF%BC%8C%E5%AE%8C%E6%88%90%E5%8D%8F%E8%AE%AE%E6%96%B0%E5%A2%9E%E3%80%82%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%2588%259B%25E5%25BB%25BA%25E5%25AE%258C%25E6%2588%2590%25E4%25BF%25A1%25E6%2581%25AF%25E5%25B1%2595%25E7%25A4%25BA)%20%E5%88%9B%E5%BB%BA%E5%AE%8C%E6%88%90%E4%BF%A1%E6%81%AF%E5%B1%95%E7%A4%BA%0A%0A!%5B%E6%96%B0%E5%BB%BA%E5%9E%8B%E5%8F%B7%E5%8D%8F%E8%AE%AE%5D(%2Fassets%2Fimg%2Fproduct-protocol.c07eaa2e.png)%0A%0Aviii.%20%E5%9C%A8%E6%93%8D%E4%BD%9C%E5%88%97%E8%A1%A8%E4%B8%AD%E5%B0%86%E5%8D%8F%E8%AE%AE%E5%8F%91%E5%B8%83%E3%80%82%20!%5B%E6%96%B0%E5%BB%BA%E5%9E%8B%E5%8F%B7%E5%8D%8F%E8%AE%AE%5D(%2Fassets%2Fimg%2Fprotocol-release.3ad7301e.png)%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%2588%259B%25E5%25BB%25BA%25E4%25BA%25A7%25E5%2593%2581)%20%E5%88%9B%E5%BB%BA%E4%BA%A7%E5%93%81%0A%0A**%E4%BE%8B**%0A%0Ai.%E4%B8%8B%E8%BD%BD%E5%9E%8B%E5%8F%B7%E6%96%87%E4%BB%B6%5B%E9%85%8D%E7%BD%AEJSON%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Ffiles%2Fdevice-connection%2F%25E8%25AE%25BE%25E5%25A4%2587%25E5%259E%258B%25E5%258F%25B7-%25E6%2599%25BA%25E8%2583%25BD%25E6%25B8%25A9%25E6%258E%25A7.json)%0A%0Aii.%20%E9%80%89%E6%8B%A9%20%60%E8%AE%BE%E5%A4%87%E7%AE%A1%E7%90%86%60%5C–%3E%60%E4%BA%A7%E5%93%81%60%5C–%3E%20%E7%82%B9%E5%87%BB%60%E5%AF%BC%E5%85%A5%E9%85%8D%E7%BD%AE%60%E6%8C%89%E9%92%AE%0A%0A!%5B%E5%AF%BC%E5%85%A5%E5%9E%8B%E5%8F%B7%E5%AF%BC%E8%88%AA%5D(%2Fassets%2Fimg%2Fimport-product.cf7b01cb.png)%0A%0Aiii.%20%E9%80%89%E6%8B%A9%5B%E9%85%8D%E7%BD%AEJSON%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Ffiles%2Fdevice-connection%2F%25E8%25AE%25BE%25E5%25A4%2587%25E5%259E%258B%25E5%258F%25B7-%25E6%2599%25BA%25E8%2583%25BD%25E6%25B8%25A9%25E6%258E%25A7.json)%E6%96%87%E4%BB%B6%0A%0A%E6%B3%A8%E6%84%8F%EF%BC%9A%0A%0A%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6%E9%9C%80%E8%A6%81%E5%B0%86standalone%2Fsrc%2Fmain%2Fresources%2Fapplication.yml%E4%B8%AD%E7%9A%84static-location%E4%BF%AE%E6%94%B9%E4%B8%BA%20%20%0Ahttp%3A%2F%2F%E5%90%8E%E5%8F%B0%E6%9C%8D%E5%8A%A1ip%3A8848%2Fupload%EF%BC%8C%E5%8F%82%E8%80%83%5B%E5%8D%8F%E8%AE%AE%E4%B8%8A%E4%BC%A0%E9%97%AE%E9%A2%98%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fcommon-problems%2Finstall.html%23%25E5%258D%258F%25E8%25AE%25AE%25E5%258F%2591%25E5%25B8%2583%25E5%25A4%25B1%25E8%25B4%25A5%25E6%2588%2596%25E5%2587%25BA%25E7%258E%25B0%25E4%25B8%258D%25E6%2594%25AF%25E6%258C%2581%25E7%259A%2584%25E5%258D%258F%25E8%25AE%25AE%25EF%25BC%259Axxx)%0A%0Aiv.%E4%BA%A7%E5%93%81%E5%AF%BC%E5%85%A5%E5%AE%8C%E6%88%90%E5%90%8E%EF%BC%8C%E4%BA%A7%E5%93%81%E7%8A%B6%E6%80%81%E4%B8%BA%60%E6%9C%AA%E5%8F%91%E5%B8%83%60%2C%E6%95%88%E6%9E%9C%E5%A6%82%E4%B8%8B%E5%9B%BE%0A%0A!%5B%E6%9C%AA%E5%8F%91%E5%B8%83%E4%BA%A7%E5%93%81%5D(%2Fassets%2Fimg%2Fdevice-product-unpublished.95fe628c.png)%0A%0Av.%E7%82%B9%E5%87%BB%E5%88%9A%E5%AF%BC%E5%85%A5%E4%BA%A7%E5%93%81%E4%B8%AD%E7%9A%84%60…%60%E6%8C%89%E9%92%AE%E4%BC%9A%E5%87%BA%E7%8E%B0%60%E5%8F%91%E5%B8%83%60%E6%8C%89%E9%92%AE%EF%BC%8C%E7%82%B9%E5%87%BB%60%E5%8F%91%E5%B8%83%60%E6%8C%89%E9%92%AE%E5%AE%8C%E6%88%90%E4%BA%A7%E5%93%81%E5%8F%91%E5%B8%83%EF%BC%8C%E5%AF%BC%E8%88%AA%E6%A0%8F%E4%B8%AD%E5%8F%91%E5%B8%83%E7%8A%B6%E6%80%81%E5%8F%98%E4%B8%BA%60%E5%B7%B2%E5%8F%91%E5%B8%83%60%E4%BB%A3%E8%A1%A8%E5%8F%91%E5%B8%83%E6%88%90%E5%8A%9F%E3%80%82%0A%0A!%5B%E5%B7%B2%E5%8F%91%E5%B8%83%E4%BA%A7%E5%93%81%5D(%2Fassets%2Fimg%2Fdevice-product-published.8f504bd8.png)%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%2588%259B%25E5%25BB%25BA%25E6%2588%2590%25E5%258A%259F%25E7%259A%2584%25E4%25BA%25A7%25E5%2593%2581%25E4%25BF%25A1%25E6%2581%25AF%25E5%25B1%2595%25E7%25A4%25BA)%20%E5%88%9B%E5%BB%BA%E6%88%90%E5%8A%9F%E7%9A%84%E4%BA%A7%E5%93%81%E4%BF%A1%E6%81%AF%E5%B1%95%E7%A4%BA%0A%0Ai.%20%E7%82%B9%E5%87%BB%E4%BA%A7%E5%93%81%E4%B8%AD%60%E7%BC%96%E8%BE%91%60%E9%93%BE%E6%8E%A5%E6%9F%A5%E7%9C%8B%E5%92%8C%E7%BC%96%E8%BE%91%E4%BA%A7%E5%93%81%E7%9A%84%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF%20!%5B%E4%BA%A7%E5%93%81%E7%BC%96%E8%BE%91%E6%8C%89%E9%92%AE%5D(%2Fassets%2Fimg%2Fcompile.0f2e9cf0.png)%0A%0Aii.%20%E7%82%B9%E5%87%BB%E4%BA%A7%E5%93%81%E4%B8%AD%60%E6%9F%A5%E7%9C%8B%60%E2%86%92%60%E7%89%A9%E6%A8%A1%E5%9E%8B%60%2C%E5%AF%B9%E4%BA%A7%E5%93%81%E8%AE%BE%E5%A4%87%E5%AE%9A%E4%B9%89%20!%5B%E4%BA%A7%E5%93%81%E6%9F%A5%E7%9C%8B%E6%8C%89%E9%92%AE%5D(%2Fassets%2Fimg%2Fcheck.05c164a5.png)%20!%5B%E7%89%A9%E6%A8%A1%E5%9E%8B%E6%8C%89%E9%92%AE%5D(%2Fassets%2Fimg%2FPhysical-model.be1ee9ca.png)%0A%0Aiii.%20%E7%82%B9%E5%87%BB%E5%B1%9E%E6%80%A7%E5%AE%9A%E4%B9%89%E4%BF%A1%E3%80%81%E4%BA%8B%E4%BB%B6%E5%AE%9A%E4%B9%89%E5%AF%B9%E5%BA%94%E6%93%8D%E4%BD%9C%E4%B8%8B%E7%9A%84%E7%BC%96%E8%BE%91%E6%8C%89%E9%92%AE%E6%9F%A5%E7%9C%8B%E6%9B%B4%E8%AF%A6%E7%BB%86%E7%9A%84%E5%9E%8B%E5%8F%B7%E6%81%AF%0A%0A%E5%B1%9E%E6%80%A7%E5%AE%9A%E4%B9%89%E5%8F%82%E6%95%B0%EF%BC%9A%20%20%0A!%5B%E5%9E%8B%E5%8F%B7%E4%BF%A1%E6%81%AF1%5D(%2Fassets%2Fimg%2Fdevice-product-info1.287b6211.png)%0A%0A%E5%8A%9F%E8%83%BD%E5%AE%9A%E4%B9%89%E5%8F%82%E6%95%B0%EF%BC%9A%20%20%0A!%5B%E5%9E%8B%E5%8F%B7%E4%BF%A1%E6%81%AF2%5D(%2Fassets%2Fimg%2Fdevice-product-info2.65db5b19.png)%0A%0A%E4%BA%8B%E4%BB%B6%E5%AE%9A%E4%B9%89%E5%8F%82%E6%95%B0%EF%BC%9A%20%20%0A!%5B%E5%9E%8B%E5%8F%B7%E4%BF%A1%E6%81%AF3%5D(%2Fassets%2Fimg%2Fdevice-product-info3.79ae8c33.png)%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%2588%259B%25E5%25BB%25BA%25E8%25AE%25BE%25E5%25A4%2587)%20%E5%88%9B%E5%BB%BA%E8%AE%BE%E5%A4%87%0A%0A%3E%20%E8%87%AA%E5%AE%9A%E4%B9%89%E5%88%9B%E5%BB%BA%E8%AE%BE%E5%A4%87%EF%BC%8C%E8%AF%B7%E5%8F%82%E8%80%83%5B%E6%B7%BB%E5%8A%A0%E8%AE%BE%E5%A4%87%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Fdevice-manager.html%23%25E6%25B7%25BB%25E5%258A%25A0%25E8%25AE%25BE%25E5%25A4%2587)%E3%80%82%0A%0A**%E4%BE%8B**%0A%0Ai.%20%E4%B8%8B%E8%BD%BD%E8%AE%BE%E5%A4%87Excel%E6%96%87%E4%BB%B6%5B%E8%AE%BE%E5%A4%87Excel%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Ffiles%2Fdevice-connection%2F%25E6%2599%25BA%25E8%2583%25BD%25E6%25B8%25A9%25E6%258E%25A7%25E6%25B5%258B%25E8%25AF%2595%25E8%25AE%25BE%25E5%25A4%2587.xlsx)%0A%0Aii.%20%E9%80%89%E6%8B%A9%20%60%E8%AE%BE%E5%A4%87%E7%AE%A1%E7%90%86%60%5C–%3E%60%E8%AE%BE%E5%A4%87%60%5C–%3E%20%60%E5%85%B6%E4%BB%96%E6%89%B9%E9%87%8F%E6%93%8D%E4%BD%9C%60%5C–%3E%60%E6%89%B9%E9%87%8F%E5%AF%BC%E5%85%A5%E8%AE%BE%E5%A4%87%60%0A%0A!%5B%E5%AF%BC%E5%85%A5%E8%AE%BE%E5%A4%87%E5%AF%BC%E8%88%AA%5D(%2Fassets%2Fimg%2Fimport-device.893fc4ee.png)%0A%0Aiii.%20%E9%80%89%E6%8B%A9%E9%9C%80%E8%A6%81%E5%AF%BC%E5%85%A5%E7%9A%84%E4%BA%A7%E5%93%81%2C%E7%82%B9%E5%87%BB%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%0A%0A!%5B%E9%80%89%E6%8B%A9%E4%BA%A7%E5%93%81%5D(%2Fassets%2Fimg%2Fchoose-device-product.874329f6.png)%0A%0Aiv.%20%E8%AE%BE%E5%A4%87%E5%AF%BC%E5%85%A5%E5%AE%8C%E6%88%90%E6%95%88%E6%9E%9C%E5%A6%82%E4%B8%8B%E5%9B%BE%0A%0A!%5B%E6%9C%AA%E6%BF%80%E6%B4%BB%E7%9A%84%E8%AE%BE%E5%A4%87%5D(%2Fassets%2Fimg%2Fdevice-instance-not-active.afd4cd8b.png)%0A%0Av.%20%E7%82%B9%E5%87%BB%E4%B8%8A%E5%9B%BE%E4%B8%AD%60%E5%90%AF%E7%94%A8%60%E9%93%BE%E6%8E%A5%E5%AE%8C%E6%88%90%E8%AE%BE%E5%A4%87%E6%BF%80%E6%B4%BB%EF%BC%8C%E7%8A%B6%E6%80%81%E6%A0%8F%E4%B8%AD%E5%8F%91%E5%B8%83%E7%8A%B6%E6%80%81%E5%8F%98%E4%B8%BA%60%E7%A6%BB%E7%BA%BF%60%E4%BB%A3%E8%A1%A8%E8%AE%BE%E5%A4%87%E6%BF%80%E6%B4%BB%E6%88%90%E5%8A%9F%E3%80%82%0A%0A!%5B%E5%B7%B2%E6%BF%80%E6%B4%BB%E7%9A%84%E8%AE%BE%E5%A4%87%5D(%2Fassets%2Fimg%2Fdevice-instance-offline.319ae76a.png)%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%2588%259B%25E5%25BB%25BA%25E6%2588%2590%25E5%258A%259F%25E7%259A%2584%25E8%25AE%25BE%25E5%25A4%2587%25E4%25BF%25A1%25E6%2581%25AF%25E5%25B1%2595%25E7%25A4%25BA)%20%E5%88%9B%E5%BB%BA%E6%88%90%E5%8A%9F%E7%9A%84%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF%E5%B1%95%E7%A4%BA%0A%0Ai.%20%E7%82%B9%E5%87%BB%E6%9F%A5%E7%9C%8B%E9%93%BE%E6%8E%A5%E5%8F%AF%E4%BB%A5%E7%9C%8B%E5%88%B0%E8%AE%BE%E5%A4%87%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF%EF%BC%88%E5%AE%9E%E4%BE%8B%E4%BF%A1%E6%81%AF%EF%BC%89%20!%5B%E7%82%B9%E5%87%BB%E6%9F%A5%E7%9C%8B%E6%8C%89%E9%92%AE%5D(%2Fassets%2Fimg%2Fdevice-instance-general-check.9e847db5.png)%20!%5B%E8%AE%BE%E5%A4%87%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF%5D(%2Fassets%2Fimg%2Fdevice-instance-general-info.b43d753a.png)%0A%0Aii.%20%E8%AE%BE%E5%A4%87%E8%BF%90%E8%A1%8C%E7%8A%B6%E6%80%81%E4%BF%A1%E6%81%AF%EF%BC%88%E8%BF%90%E8%A1%8C%E7%8A%B6%E6%80%81%EF%BC%89%0A%0A!%5B%E8%AE%BE%E5%A4%87%E8%BF%90%E8%A1%8C%E7%8A%B6%E6%80%81%E4%BF%A1%E6%81%AF%5D(%2Fassets%2Fimg%2Fdevice-instance-run-info.27ada8c3.png)%0A%0Aiii.%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E4%BF%A1%E6%81%AF%EF%BC%88%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%EF%BC%89%0A%0A!%5B%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E4%BF%A1%E6%81%AF%5D(%2Fassets%2Fimg%2Fdevice-instance-function.d795c3a5.png)%0A%0Aiv.%20%E8%AE%BE%E5%A4%87%E6%97%A5%E5%BF%97%EF%BC%88%E6%97%A5%E5%BF%97%E7%AE%A1%E7%90%86%EF%BC%89%0A%0A!%5B%E8%AE%BE%E5%A4%87%E6%97%A5%E5%BF%97%5D(%2Fassets%2Fimg%2Fdevice-instance-log.550e4be7.png)%0A%0Av.%E5%91%8A%E8%AD%A6%E8%AE%BE%E7%BD%AE%0A%0A!%5B%E5%91%8A%E8%AD%A6%E8%AE%BE%E7%BD%AE%5D(%2Fassets%2Fimg%2Fdevice-instance-alarm.de9fe90b.png)%0A%0Avi.%E5%8F%AF%E8%A7%86%E5%8C%96%0A%0A!%5B%E5%8F%AF%E8%A7%86%E5%8C%96%5D(%2Fassets%2Fimg%2Fdevice-instance-visual.4dcbc8bf.png)%0A%0Avii.%E8%AE%BE%E5%A4%87%E5%BD%B1%E5%AD%90%0A%0A!%5B%E8%AE%BE%E5%A4%87%E5%BD%B1%E5%AD%90%5D(%2Fassets%2Fimg%2Fdevice-instance-sign.bff329fd.png)%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%2588%259B%25E5%25BB%25BA%25E7%25BD%2591%25E5%2585%25B3%25E9%2585%258D%25E7%25BD%25AE)%20%E5%88%9B%E5%BB%BA%E7%BD%91%E5%85%B3%E9%85%8D%E7%BD%AE%0A%0A%E5%8F%82%E7%85%A7%5B%E5%90%AF%E5%8A%A8%E8%AE%BE%E5%A4%87%E7%BD%91%E5%85%B3%E6%9C%8D%E5%8A%A1%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Fcourse%2Fdevice-gateway.html)%0A%0A**%E4%BE%8B**%20i.%E5%88%9B%E5%BB%BAMQTT%E6%9C%8D%E5%8A%A1%E7%BD%91%E7%BB%9C%E7%BB%84%E4%BB%B6%E4%BB%A5%E5%8F%8AMQTT%E6%9C%8D%E5%8A%A1%E7%BB%84%E4%BB%B6%E9%85%8D%E7%BD%AE%20!%5BMQTT%E6%9C%8D%E5%8A%A1%E7%BB%84%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E9%85%8D%E7%BD%AE%5D(%2Fassets%2Fimg%2Fmqtt-config.342954a5.png)%0A%0A%E6%B3%A8%E6%84%8F%EF%BC%9A%0A%0A%E6%AD%A4%E5%A4%84%E4%BD%BF%E7%94%A8%E7%9A%84%E7%AB%AF%E5%8F%A3%E4%B8%BA1889%EF%BC%8Cdocker%E5%90%AF%E5%8A%A8%E6%97%B6%E6%B2%A1%E6%9C%89%E9%BB%98%E8%AE%A4%E5%BC%80%E5%90%AF%EF%BC%8C%E4%BD%BF%E7%94%A8docker%E5%90%AF%E5%8A%A8jetlinks%E6%97%B6%E8%AF%B7%E6%98%A0%E5%B0%841889%E7%AB%AF%E5%8F%A3%E6%88%96%E8%80%85%E4%BD%BF%E7%94%A81883%E7%AB%AF%E5%8F%A3%E3%80%82%0A%0Aii.%E5%90%AF%E5%8A%A8MQTT%E6%9C%8D%E5%8A%A1%E7%BB%84%E4%BB%B6%EF%BC%88%E7%81%B0%E8%89%B2%E4%B8%BA%E6%9C%AA%E5%90%AF%E5%8A%A8%EF%BC%8C%E8%93%9D%E8%89%B2%E4%B8%BA%E5%90%AF%E5%8A%A8%EF%BC%89%20!%5BMQTT%E6%9C%8D%E5%8A%A1%E7%BB%84%E4%BB%B6%E5%90%AF%E5%8A%A8%5D(%2Fassets%2Fimg%2Fmqtt-start.ceebf2f4.png)%0A%0Aiii.%E5%88%9B%E5%BB%BAMQTT%E6%9C%8D%E5%8A%A1%E8%AE%BE%E5%A4%87%E7%BD%91%E5%85%B3%E4%BB%A5%E5%8F%8AMQTT%E6%9C%8D%E5%8A%A1%E8%AE%BE%E5%A4%87%E7%BD%91%E5%85%B3%E9%85%8D%E7%BD%AE%20%20%0A!%5BMQTT%E6%9C%8D%E5%8A%A1%E8%AE%BE%E5%A4%87%E7%BD%91%E5%85%B3%E5%88%9B%E5%BB%BA%E5%92%8C%E9%85%8D%E7%BD%AE%5D(%2Fassets%2Fimg%2Fmqtt-gateway-info.5bcea38d.png)%0A%0A%E8%AD%A6%E5%91%8A%0A%0A%E5%A4%A7%E9%83%A8%E5%88%86%E6%83%85%E5%86%B5%EF%BC%8C%E8%AF%B7%E5%8B%BF%E5%8B%BE%E9%80%89%60%E8%AE%A4%E8%AF%81%E5%8D%8F%E8%AE%AE%60%2C%E8%AE%A4%E8%AF%81%E5%8D%8F%E8%AE%AE%E7%9A%84%E4%BD%9C%E7%94%A8%E6%98%AF%3A%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%AE%9A%E7%9A%84%E5%8D%8F%E8%AE%AE%E6%9D%A5%E8%BF%9B%E8%A1%8C%E7%BB%9F%E4%B8%80%E7%9A%84%E8%AE%A4%E8%AF%81%E3%80%82%E4%B8%8D%E5%8B%BE%E9%80%89%E6%97%B6%EF%BC%8C%E5%88%99%E4%BD%BF%E7%94%A8%E4%BA%A7%E5%93%81%E9%87%8C%E9%80%89%E6%8B%A9%E7%9A%84%E5%8D%8F%E8%AE%AE%E6%9D%A5%E8%BF%9B%E8%A1%8C%E8%AE%A4%E8%AF%81%EF%BC%8C%20%E8%BF%992%E7%A7%8D%E8%AE%A4%E8%AF%81%E6%96%B9%E5%BC%8F%E5%9C%A8%E5%8D%8F%E8%AE%AE%E5%8C%85%E5%86%85%E7%9A%84%E5%AE%9E%E7%8E%B0%E6%96%B9%E5%BC%8F%E6%98%AF%E4%B8%8D%E5%90%8C%E7%9A%84%E3%80%82%E5%A4%A7%E9%83%A8%E5%88%86%E6%83%85%E5%86%B5%E4%B8%8B%E4%B8%8D%E9%9C%80%E8%A6%81%E9%80%89%E6%8B%A9%E3%80%82%0A%0Aiv.%E5%90%AF%E5%8A%A8MQTT%E6%9C%8D%E5%8A%A1%E8%AE%BE%E5%A4%87%E7%BD%91%E5%85%B3%EF%BC%8C%E7%82%B9%E5%87%BB%20%60%E5%90%AF%E5%8A%A8%60%EF%BC%8C%60%E7%8A%B6%E6%80%81%60%E5%8F%98%E4%B8%BA%60%E5%B7%B2%E5%90%AF%E5%8A%A8%60%20!%5BMQTT%E5%90%AF%E5%8A%A8%5D(%2Fassets%2Fimg%2Fmqtt-gateway-start1.0d7fa79e.png)%20!%5BMQTT%E5%90%AF%E5%8A%A8%5D(%2Fassets%2Fimg%2Fmqtt-gateway-start2.f6130070.png)%0A%0A%E6%B3%A8%E6%84%8F%EF%BC%9A%0A%0A%E5%A4%A7%E9%83%A8%E5%88%86%E6%83%85%E5%86%B5%E6%97%A0%E9%9C%80%E9%80%89%E6%8B%A9%E8%AE%A4%E8%AF%81%E5%8D%8F%E8%AE%AE.%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E4%25BD%25BF%25E7%2594%25A8mqttx%25E6%258E%25A5%25E5%2585%25A5)%20%E4%BD%BF%E7%94%A8MQTTX%E6%8E%A5%E5%85%A5%0A%0A1.%E4%B8%8B%E8%BD%BD%E5%B9%B6%E5%AE%89%E8%A3%85MQTTX%E8%BD%AF%E4%BB%B6%E3%80%82%E8%AF%B7%E8%AE%BF%E9%97%AE%5BMQTTX%E5%AE%98%E7%BD%91%20(opens%20new%20window)%5D(https%3A%2F%2Fmqttx.app%2Fzh)%E3%80%82%0A%0A2.%E6%89%93%E5%BC%80MQTTX%E8%BD%AF%E4%BB%B6%EF%BC%8C%E7%82%B9%E5%87%BB%60New%20Connection%60%E5%88%9B%E5%BB%BA%E4%B8%80%E4%B8%AA%E8%BF%9E%E6%8E%A5%E3%80%82%0A%0A!%5Bmqttx%E9%A6%96%E9%A1%B5%5D(%2Fassets%2Fimg%2Fmqttx-index.1cf3213f.png)%0A%0A3.%E8%AE%BE%E7%BD%AE%E8%BF%9E%E6%8E%A5%E5%8F%82%E6%95%B0%E3%80%82%0A%0A%E6%B3%A8%E6%84%8F%0A%0A%E8%AE%BE%E7%BD%AE%E5%8F%82%E6%95%B0%E6%97%B6%EF%BC%8C%E8%AF%B7%E7%A1%AE%E4%BF%9D%E5%8F%82%E6%95%B0%E5%80%BC%E4%B8%AD%E6%88%96%E5%8F%82%E6%95%B0%E5%80%BC%E7%9A%84%E5%89%8D%E5%90%8E%E5%9D%87%E6%B2%A1%E6%9C%89%E7%A9%BA%E6%A0%BC%E3%80%82%0A%0Ai.%20%E8%AE%BE%E7%BD%AE%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF%0A%0A!%5Bmqtt%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF%E8%AE%BE%E7%BD%AE%5D(%2Fassets%2Fimg%2Fmqtt-connection-general.c7d17922.png)%0A%0A%7C%20%E5%8F%82%E6%95%B0%20%7C%20%E8%AF%B4%E6%98%8E%20%7C%0A%7C%20—%20%7C%20—%20%7C%0A%7C%20Name%20%7C%20%E8%BE%93%E5%85%A5%E6%82%A8%E7%9A%84%E8%87%AA%E5%AE%9A%E4%B9%89%E5%90%8D%E7%A7%B0%E3%80%82%20%7C%0A%7C%20Client%20ID%20%7C%20%E8%AE%BE%E5%A4%87Id%E3%80%82%E6%9C%AC%E6%96%87%E6%A1%A3%E4%B8%AD%E4%B8%BA%E6%BC%94%E7%A4%BA%E8%AE%BE%E5%A4%87%60test001%60%20%7C%0A%7C%20Host%20%7C%20%E8%BF%9E%E6%8E%A5%E5%9F%9F%E5%90%8D%E3%80%82%E6%9C%AC%E5%9C%B0%E8%BF%9E%E6%8E%A5%E5%8F%AF%E7%9B%B4%E6%8E%A5%E5%A1%AB%E5%86%99%20%60127.0.0.1%60%2C%E5%A6%82%E4%B8%BA%E8%BF%9C%E7%A8%8B%E8%BF%9E%E6%8E%A5%EF%BC%8C%E8%AF%B7%E5%A1%AB%E5%86%99%E8%BF%9C%E7%A8%8B%E8%BF%9E%E6%8E%A5%E5%9C%B0%E5%9D%80%20%7C%0A%7C%20Port%20%7C%20%E8%AE%BE%E7%BD%AE%E4%B8%BA%601889%60%20%7C%0A%7C%20Username%20%7C%20%E6%8E%A5%E5%85%A5%E8%B4%A6%E5%8F%B7%20%7C%0A%7C%20Password%20%7C%20%E6%8E%A5%E5%85%A5%E5%AF%86%E7%A0%81%20%7C%0A%0A%E6%8F%90%E7%A4%BA%0A%0Ausername%E5%92%8Cpassword%5B%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E5%99%A8%20(opens%20new%20window)%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Fmqtt-auth-generator.html)%20!%5Bmqtt%E7%94%A8%E6%88%B7%E5%90%8D%E5%90%8D%E5%AF%86%E7%A0%81%E8%AE%BE%E7%BD%AE%5D(%2Fassets%2Fimg%2Fmqtt-connection-user.4eae0dcb.png)%0A%0A4.%E8%AE%BE%E7%BD%AE%E5%AE%8C%E6%88%90%E5%90%8E%EF%BC%8C%E5%8D%95%E5%87%BB%E5%8F%B3%E4%B8%8B%E8%A7%92%E7%9A%84**OK**%E3%80%82%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E8%25AE%25BE%25E5%25A4%2587%25E6%25B6%2588%25E6%2581%25AF)%20%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%0A%0A%E8%AE%BE%E5%A4%87%E8%BF%9E%E6%8E%A5%E4%B8%8A%E5%B9%B3%E5%8F%B0%EF%BC%8C%E5%B9%B6%E8%BF%9B%E8%A1%8C%E4%B8%80%E4%BA%9B%E5%9F%BA%E6%9C%AC%E7%9A%84%E4%BA%8B%E4%BB%B6%E6%94%B6%E5%8F%91%E3%80%81%E5%B1%9E%E6%80%A7%E8%AF%BB%E5%8F%96%E6%93%8D%E4%BD%9C%E3%80%82%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E8%25AE%25BE%25E5%25A4%2587%25E4%25B8%258A%25E4%25B8%258B%25E7%25BA%25BF)%20%E8%AE%BE%E5%A4%87%E4%B8%8A%E4%B8%8B%E7%BA%BF%0A%0A%E5%8D%95%E5%87%BB%20MqttX%20%E4%B8%AD%60Connect%60%E8%BF%9B%E8%A1%8C%E8%BF%9E%E6%8E%A5%0A%0A!%5Bmqtt%E8%BF%9E%E6%8E%A5%5D(%2Fassets%2Fimg%2Fmqtt-connection.818f3cf8.png)%0A%0A%E5%B9%B3%E5%8F%B0%E4%B8%AD%E8%AE%BE%E5%A4%87%E7%8A%B6%E6%80%81%E5%8F%98%E4%B8%BA%E4%B8%8A%E7%BA%BF%E5%8D%B3%E4%B8%BA%E8%BF%9E%E6%8E%A5%E6%88%90%E5%8A%9F%0A%0A!%5B%E8%AE%BE%E5%A4%87%E4%B8%8A%E7%BA%BF%5D(%2Fassets%2Fimg%2Fdevice-online.dc3d00bf.png)%0A%0A%E7%82%B9%E5%87%BB%E8%AF%A5%E8%AE%BE%E5%A4%87%E7%9A%84%60%E6%9F%A5%E7%9C%8B%60%E2%86%92%60%E6%97%A5%E5%BF%97%E7%AE%A1%E7%90%86%60%EF%BC%8C%E5%9C%A8%E8%AE%BE%E5%A4%87%E6%97%A5%E5%BF%97%E6%A8%A1%E5%9D%97%E5%8F%AF%E4%BB%A5%E7%9C%8B%E5%88%B0%E8%AE%BE%E5%A4%87%E4%B8%8A%E7%BA%BF%E6%97%A5%E5%BF%97%0A%0A!%5B%E8%AE%BE%E5%A4%87%E4%B8%8A%E7%BA%BF%E6%97%A5%E5%BF%97%5D(%2Fassets%2Fimg%2Fdevice-online-log.f5bca109.png)%0A%0A%E5%8D%95%E5%87%BB%20MqttX%20%E4%B8%AD%60Disconnect%60%E6%96%AD%E5%BC%80%E8%BF%9E%E6%8E%A5%0A%0A!%5Bmqtt%E6%96%AD%E5%BC%80%E8%BF%9E%E6%8E%A5%5D(%2Fassets%2Fimg%2Fmqtt-connection-stop.4fe1307d.png)%0A%0A%E5%B9%B3%E5%8F%B0%E4%B8%AD%E8%AE%BE%E5%A4%87%E7%8A%B6%E6%80%81%E5%8F%98%E4%B8%BA%E7%A6%BB%E7%BA%BF%E5%8D%B3%E4%B8%BA%E6%96%AD%E5%BC%80%E8%BF%9E%E6%8E%A5%E6%88%90%E5%8A%9F%0A%0A!%5B%E8%AE%BE%E5%A4%87%E7%A6%BB%E7%BA%BF%5D(%2Fassets%2Fimg%2Fdevice-offline.def91fef.png)%0A%0A%E7%82%B9%E5%87%BB%E8%AF%A5%E8%AE%BE%E5%A4%87%E7%9A%84%60%E6%9F%A5%E7%9C%8B%60%E2%86%92%60%E6%97%A5%E5%BF%97%E7%AE%A1%E7%90%86%60%EF%BC%8C%E5%9C%A8%E8%AE%BE%E5%A4%87%E6%97%A5%E5%BF%97%E6%A8%A1%E5%9D%97%E5%8F%AF%E4%BB%A5%E7%9C%8B%E5%88%B0%E8%AE%BE%E5%A4%87%E7%A6%BB%E7%BA%BF%E6%97%A5%E5%BF%97%0A%0A!%5B%E8%AE%BE%E5%A4%87%E7%A6%BB%E7%BA%BF%E6%97%A5%E5%BF%97%5D(%2Fassets%2Fimg%2Fdevice-offline-log.c9e5adf4.png)%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E8%25AF%25BB%25E5%258F%2596%25E8%25AE%25BE%25E5%25A4%2587%25E5%25B1%259E%25E6%2580%25A7)%20%E8%AF%BB%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%0A%0A%E6%B3%A8%E6%84%8F%0A%0A%E7%AC%AC2%E6%AD%A5%E4%B8%AD%E5%9B%9E%E5%A4%8D%E5%B9%B3%E5%8F%B0%E5%B1%9E%E6%80%A7%E5%80%BC%E9%9C%80%E8%A6%81%E5%9C%A8%E7%AC%AC1%E6%AD%A5%E5%B9%B3%E5%8F%B0%E5%8F%91%E9%80%81%E8%AE%A2%E9%98%85%E4%BB%A5%E5%90%8E%E7%9A%84%E5%8D%81%E7%A7%92%E9%92%9F%E5%86%85%E5%AE%8C%E6%88%90%EF%BC%8C%E5%90%A6%E5%88%99%E5%B9%B3%E5%8F%B0%E4%BC%9A%E8%A7%86%E4%B8%BA%E8%AF%A5%E6%AC%A1%E6%93%8D%E4%BD%9C%E8%B6%85%E6%97%B6%EF%BC%8C%E5%AF%BC%E8%87%B4%E8%AF%BB%E5%8F%96%E5%B1%9E%E6%80%A7%E5%80%BC%E5%A4%B1%E8%B4%A5%E3%80%82%0A%0A1.%E5%B9%B3%E5%8F%B0%E5%91%8A%E7%9F%A5%E8%AE%BE%E5%A4%87%EF%BC%88MQTTX%EF%BC%89%E9%9C%80%E8%A6%81%E8%AE%BE%E5%A4%87%E8%BF%94%E5%9B%9E%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%0A%0A%E5%8D%95%E5%87%BB%E8%AE%BE%E5%A4%87%E9%A1%B5%E9%9D%A2%E4%B8%AD%60test001%60%E8%AE%BE%E5%A4%87%E5%AF%B9%E5%BA%94%E7%9A%84%60%E6%9F%A5%E7%9C%8B%60%E9%93%BE%E6%8E%A5%0A%0A%E9%80%89%E6%8B%A9%E5%BC%B9%E5%87%BA%E6%A1%86%E4%B8%AD%60%E8%BF%90%E8%A1%8C%E7%8A%B6%E6%80%81%E6%9D%BF%E5%9D%97%60%0A%0A%E5%8D%95%E5%87%BB%E5%B1%9E%E6%80%A7%E5%88%B7%E6%96%B0%0A%0A!%5B%E5%B9%B3%E5%8F%B0%E5%B1%9E%E6%80%A7%E8%AE%A2%E9%98%85%E6%93%8D%E4%BD%9C%5D(%2Fassets%2Fimg%2Fdevice-property-refresh.f7cf28bd.png)%0A%0AMQTTX%E4%BC%9A%E6%94%B6%E5%88%B0%E5%B9%B3%E5%8F%B0%E4%B8%8B%E5%8F%91%E7%9A%84%E8%AE%A2%E9%98%85%0A%0A!%5B%E8%AE%A2%E9%98%85topic%5D(%2Fassets%2Fimg%2Fmqttfx-sub-read-property.47aa94fe.png)%0A%0A%E6%B3%A8%E6%84%8F%3A%0A%0A%E5%A4%8D%E5%88%B6%E5%A5%BD%E8%AE%A2%E9%98%85%E8%AF%A5topic%E6%94%B6%E5%88%B0%E7%9A%84%E6%B6%88%E6%81%AF%E4%B8%AD%E7%9A%84messageId%E3%80%82%E6%AD%A4messageId%E5%B0%86%E4%BD%9C%E4%B8%BA%E5%9B%9E%E5%A4%8D%E4%B8%8E%E5%B9%B3%E5%8F%B0%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E7%9A%84%E5%87%AD%E6%8D%AE%E4%B9%8B%E4%B8%80%0A%0A2.%E8%AE%BE%E5%A4%87%EF%BC%88MQTTX%EF%BC%89%E5%9B%9E%E5%A4%8D%E5%B9%B3%E5%8F%B0%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%80%BC%0A%0A%E5%9C%A8MQTTX%E4%B8%8A%E5%8F%91%E9%80%81%E6%B6%88%E6%81%AF%EF%BC%8C%E5%8F%91%E9%80%81%E5%B9%B3%E5%8F%B0%E6%89%80%E9%9C%80%E8%A6%81%E7%9A%84%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%80%BC%E3%80%82%0A%0Ai%20%E8%BE%93%E5%85%A5%E4%B8%80%E4%B8%AA%E5%9B%9E%E5%A4%8D%E5%B9%B3%E5%8F%B0%E5%B1%9E%E6%80%A7%E5%80%BC%E6%B6%88%E6%81%AFTopic(%E8%BF%99%E9%87%8C%E7%9A%84%E4%B8%BA%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fread%2Freply%60)%E5%92%8C%E8%A6%81%E5%8F%91%E9%80%81%E7%9A%84%E6%B6%88%E6%81%AF%E5%86%85%E5%AE%B9%EF%BC%8C%20%E5%8D%95%E5%87%BBPublish%EF%BC%8C%E5%90%91%E5%B9%B3%E5%8F%B0%E6%8E%A8%E9%80%81%E8%AF%A5%E6%B6%88%E6%81%AF%E3%80%82%0A%0A!%5B%E5%9B%9E%E5%A4%8D%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%5D(%2Fassets%2Fimg%2Fmqttfx-replay-device-property.b18d73a8.png)%0A%0A%7C%20%E5%8F%82%E6%95%B0%20%7C%20%E8%AF%B4%E6%98%8E%20%7C%0A%7C%20—%20%7C%20—%20%7C%0A%7C%20messageId%20%7C%20%E5%B9%B3%E5%8F%B0%E6%89%80%E4%B8%8B%E5%8F%91%E7%9A%84messageId%E5%80%BC%20%7C%0A%7C%20deviceId%20%7C%20%E8%AE%BE%E5%A4%87Id%20%7C%0A%7C%20timestamp%20%7C%20%E5%BD%93%E5%89%8D%E6%97%B6%E9%97%B4%E6%88%B3%20%7C%0A%7C%20success%20%7C%20%E6%88%90%E5%8A%9F%E6%A0%87%E8%AF%86%20%7C%0A%7C%20properties%20%7C%20%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%80%BC%E5%AF%B9%E8%B1%A1%E3%80%82%E4%BE%8B%E5%A6%82%EF%BC%9A%20%7B%20%22temperature%22%3A%2250%22%7D%20%7C%0A%0A%E8%AF%A5%E6%96%87%E6%A1%A3%E6%89%80%E4%BD%BF%E7%94%A8%E7%9A%84%E5%9B%9E%E5%A4%8D%E5%86%85%E5%AE%B9%0A%0A%60%60%60%0A%7B%0A%20%22timestamp%22%3A1601196762389%2C%0A%20%22messageId%22%3A%22%E7%AC%AC%E4%B8%80%E6%AC%A1%E5%B9%B3%E5%8F%B0%E8%AE%A2%E9%98%85%E8%AE%BE%E5%A4%87%2CMQTTX%E6%89%80%E6%94%B6%E5%88%B0%E7%9A%84messageId%E5%80%BC%22%2C%0A%20%22properties%22%3A%7B%22temperature%22%3A%2250%22%7D%2C%0A%20%22deviceId%22%3A%22test001%22%2C%0A%20%22success%22%3Atrue%0A%7D%0A%60%60%60%0A%0Aiii.%20%E5%B9%B3%E5%8F%B0%E6%94%B6%E5%88%B0MqttX%E6%8E%A8%E9%80%81%E7%9A%84%E5%B1%9E%E6%80%A7%E5%80%BC%0A%0A!%5B%E5%B9%B3%E5%8F%B0%E6%94%B6%E5%88%B0%E5%B1%9E%E6%80%A7%E5%80%BC%5D(%2Fassets%2Fimg%2Fmqttfx-replyed-property-value.831c167c.png)%0A%0Aiv.%20%E8%AF%BB%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%9B%9E%E5%A4%8D%E7%9A%84%E6%97%A5%E5%BF%97%0A%0A!%5B%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E8%AF%BB%E5%8F%96%E6%97%A5%E5%BF%97%5D(%2Fassets%2Fimg%2Fread-device-property-reply-log.2b6867c1.png)%0A%0A%23%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E8%258E%25B7%25E5%258F%2596%25E8%25AE%25BE%25E5%25A4%2587%25E5%25B1%259E%25E6%2580%25A7%25E5%2580%25BC%25E5%25AE%258C%25E6%2595%25B4%25E6%25BC%2594%25E7%25A4%25BA)%20%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%80%BC%E5%AE%8C%E6%95%B4%E6%BC%94%E7%A4%BA%0A%0A%E6%B3%A8%E6%84%8F%EF%BC%9A%E5%9C%A8%E4%B8%8B%E5%9B%BE%E4%B8%AD%EF%BC%8C%E4%BB%8E%E5%9C%A8%E7%95%8C%E9%9D%A2%E4%B8%8A%E5%88%B7%E6%96%B0%E5%B1%9E%E6%80%A7%E5%BC%80%E5%A7%8B%E7%9B%B4%E5%88%B0%E5%8A%A8%E5%9B%BE%E7%BB%93%E6%9D%9F%E7%9A%84%E6%89%80%E6%9C%89%E6%93%8D%E4%BD%9C%EF%BC%8C%E9%9C%80%E8%A6%81%E5%9C%A8%E5%8D%81%E7%A7%92%E9%92%9F%E5%86%85%E5%AE%8C%E6%88%90%E3%80%82%E5%90%A6%E5%88%99%E5%B9%B3%E5%8F%B0%E4%BC%9A%E8%A7%86%E4%B8%BA%E8%AF%A5%E6%AC%A1%E6%93%8D%E4%BD%9C%E8%B6%85%E6%97%B6%EF%BC%8C%E5%AF%BC%E8%87%B4%E8%AF%BB%E5%8F%96%E5%B1%9E%E6%80%A7%E5%80%BC%E5%A4%B1%E8%B4%A5%E3%80%82%0A%0A!%5B%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%80%BC%5D(%2Fassets%2Fimg%2Fread-device-property.f7cac8f9.gif)%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E8%25AE%25BE%25E5%25A4%2587%25E4%25BA%258B%25E4%25BB%25B6%25E4%25B8%258A%25E6%258A%25A5)%20%E8%AE%BE%E5%A4%87%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%0A%0AMQTTX%20%E6%8E%A8%E9%80%81%E8%AE%BE%E5%A4%87%E4%BA%8B%E4%BB%B6%E6%B6%88%E6%81%AF%E5%88%B0%E5%B9%B3%E5%8F%B0%0A%0A%E4%BB%A5%E7%81%AB%E7%81%BE%E6%8A%A5%E8%AD%A6%E4%BA%8B%E4%BB%B6%E4%B8%BA%E4%BE%8B%E3%80%82%0A%0A1.%E5%9C%A8MQTTX%E4%B8%8A%EF%BC%8C%E8%AE%A2%E9%98%85topic%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fevent%2F%7BeventId%7D%60%E3%80%82%0A%0A2.%E8%BE%93%E5%85%A5%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5Topic%E5%92%8C%E8%A6%81%E5%8F%91%E9%80%81%E7%9A%84%E4%BA%8B%E4%BB%B6%E5%86%85%E5%AE%B9%EF%BC%8C%E5%8D%95%E5%87%BBPublish%E6%8C%89%E9%92%AE%EF%BC%8C%E5%90%91%E5%B9%B3%E5%8F%B0%E6%8E%A8%E9%80%81%E8%AF%A5%E4%BA%8B%E4%BB%B6%E6%B6%88%E6%81%AF%E3%80%82%0A%0A!%5B%E8%AE%BE%E5%A4%87%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%5D(%2Fassets%2Fimg%2Fmqttfx-device-event-report.e51158c1.png)%0A%0A%E8%AF%A5%E6%96%87%E6%A1%A3%E6%89%80%E4%BD%BF%E7%94%A8%E7%9A%84%E5%9B%9E%E5%A4%8D%E5%86%85%E5%AE%B9%0A%0A%60%60%60%0A%7B%0A%20%22timestamp%22%3A1627960319%2C%0A%20%22messageId%22%3A%221422143789942595584%22%2C%0A%20%22data%22%3A%7B%22a_name%22%3A%22%E6%9C%AA%E6%9D%A5%E7%A7%91%E6%8A%80%E5%9F%8E%22%2C%0A%20%20%22b_name%22%3A%22C2%20%E6%A0%8B%22%2C%0A%20%20%22l_name%22%3A%2212-05-2012%22%7D%0A%7D%0A%60%60%60%0A%0A%7C%20%E5%8F%82%E6%95%B0%20%7C%20%E8%AF%B4%E6%98%8E%20%7C%0A%7C%20—%20%7C%20—%20%7C%0A%7C%20timestamp%20%7C%20%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%20%7C%0A%7C%20messageId%20%7C%20%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%20%7C%0A%7C%20data%20%7C%20%E4%B8%8A%E6%8A%A5%E6%95%B0%E6%8D%AE%EF%BC%8C%E7%B1%BB%E5%9E%8B%E4%B8%8E%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%BA%8B%E4%BB%B6%E4%B8%AD%E5%AE%9A%E4%B9%89%E7%9A%84%E7%B1%BB%E5%9E%8B%E4%B8%80%E8%87%B4%20%7C%0A%0A3.%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%E8%AE%BE%E5%A4%87%E6%97%A5%E5%BF%97%0A%0A!%5B%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%E8%AE%BE%E5%A4%87%E6%97%A5%E5%BF%97%5D(%2Fassets%2Fimg%2Fdevice-event-report-log.5a4b2cf4.png)%0A%0A4.%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%E5%86%85%E5%AE%B9%0A%0A!%5B%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%E5%86%85%E5%AE%B9%5D(%2Fassets%2Fimg%2Fdevice-event-info.b88615f8.png)%20!%5B%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%E5%86%85%E5%AE%B91%5D(%2Fassets%2Fimg%2Fdevice-event-info1.8a1374cc.png)%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E5%259C%25B0%25E7%2590%2586%25E4%25BD%258D%25E7%25BD%25AE%25E4%25B8%258A%25E6%258A%25A5)%20%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E4%B8%8A%E6%8A%A5%0A%0A1.%20%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%B8%AD%E6%B7%BB%E5%8A%A0%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E3%80%82%E9%80%9A%E8%BF%87%E5%B1%9E%E6%80%A7%E5%AE%9A%E4%B9%89%E6%B7%BB%E5%8A%A0%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E7%B1%BB%E5%9E%8B%E5%B1%9E%E6%80%A7%E3%80%82%0A%0A!%5B%E6%B7%BB%E5%8A%A0%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E5%B1%9E%E6%80%A7%5D(%2Fassets%2Fimg%2Finsert-geo-property.17bb75e5.png)%0A%0A2.%20%E5%9C%A8%E8%AE%BE%E5%A4%87%E4%BA%A7%E5%93%81%E8%AF%A6%E6%83%85%E9%A1%B5%E9%9D%A2%E7%82%B9%E5%87%BB%60%E5%BA%94%E7%94%A8%E9%85%8D%E7%BD%AE%60%E6%8C%89%E9%92%AE%E3%80%82%20%20%0A%20%20%20%20!%5B%E5%BA%94%E7%94%A8%E9%85%8D%E7%BD%AE%5D(%2Fassets%2Fimg%2Fstart-model.a46d1501.png)%0A%20%20%20%20%0A3.%20%E4%BD%BF%E7%94%A8mqttX%E8%BF%9E%E6%8E%A5%E5%88%B0%E5%B9%B3%E5%8F%B0%EF%BC%8C%E8%AE%BE%E5%A4%87%E4%B8%8A%E7%BA%BF%E5%90%8E%E6%8E%A8%E9%80%81%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E6%B6%88%E6%81%AF%E5%88%B0%E5%B9%B3%E5%8F%B0%EF%BC%8C%20%E6%AD%A4%E5%A4%84%E4%BD%BF%E7%94%A8topic%E4%B8%BA%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Freport%60%E3%80%82%0A%20%20%20%20%0A%0A!%5B%E6%8E%A8%E9%80%81%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E6%B6%88%E6%81%AF%5D(%2Fassets%2Fimg%2Fpush-geo.2516c8c7.png)%0A%0A%E6%AD%A4%E5%A4%84%E4%BD%BF%E7%94%A8%E7%9A%84%E6%8A%A5%E6%96%87%E4%B8%BA%EF%BC%9A%0A%0A%60%60%60%0A%7B%0A%20%22timestamp%22%3A1601196762389%2C%0A%20%22messageId%22%3A%22ddddd%22%2C%0A%20%22properties%22%3A%7B%0A%20%20%22geoPoint%22%3A%20%22102.321%2C36.523%22%0A%20%7D%0A%7D%0A%60%60%60%0A%0A%E6%B3%A8%E6%84%8F%EF%BC%9A%0A%0A%E4%B8%8A%E6%8A%A5geo%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E7%B1%BB%E5%9E%8B%E6%95%B0%E6%8D%AE%E6%9C%89%E4%B8%89%E7%A7%8D%E6%A0%BC%E5%BC%8F%EF%BC%8C%E4%B8%80%E6%98%AF%E5%AD%97%E7%AC%A6%E4%B8%B2%E4%BB%A5%E9%80%97%E5%8F%B7%E5%88%86%E9%9A%94%EF%BC%8C%E5%A6%82%EF%BC%9A%60%22102.321%2C36.523%22%60%3B%20%20%0A%E4%BA%8C%E6%98%AF%E6%95%B0%E7%BB%84%E7%B1%BB%E5%9E%8B%EF%BC%8C%E5%A6%82%3A%60%5B102.321%2C36.523%5D%60%3B%20%20%0A%E4%B8%89%E6%98%AFmap%E7%B1%BB%E5%9E%8B%EF%BC%8C%E5%A6%82%EF%BC%9A%60%7B%22lat%22%3A102.321%2C%22lon%22%3A36.523%7D%60%E3%80%82%0A%0A4.%20%E4%B8%8A%E6%8A%A5%E6%88%90%E5%8A%9F%E5%90%8E%E5%B0%86%E5%9C%A8%E8%AE%BE%E5%A4%87%E7%9A%84%E8%BF%90%E8%A1%8C%E7%8A%B6%E6%80%81%E4%B8%AD%E6%98%BE%E7%A4%BA%E3%80%82%0A%0A!%5B%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E5%B1%95%E7%A4%BA%5D(%2Fassets%2Fimg%2Fdevice-info-geo.22f94d2d.png)%0A%0A%E4%B9%9F%E5%8F%AF%E6%9F%A5%E7%9C%8B%E4%B8%8A%E6%8A%A5%E5%8E%86%E5%8F%B2%E6%B6%88%E6%81%AF%E3%80%82%0A%0A!%5B%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E5%8E%86%E5%8F%B2%E8%AE%B0%E5%BD%95%5D(%2Fassets%2Fimg%2Fgeo-history.9d62c615.png)%0A%0A%E6%B3%A8%E6%84%8F%EF%BC%9A%0A%0A%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%B8%AD%E7%9A%84%E6%A0%87%E7%AD%BE%E4%B9%9F%E5%8F%AF%E5%88%9B%E5%BB%BAgeo%E7%B1%BB%E5%9E%8B%EF%BC%8C%E4%BD%86%E4%B8%8D%E5%8F%AF%E9%80%9A%E8%BF%87%E6%A0%87%E7%AD%BE%E4%B8%8A%E6%8A%A5%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E4%BF%A1%E6%81%AF%EF%BC%8C%E5%8F%AA%E8%83%BD%E9%80%9A%E8%BF%87%E5%B1%9E%E6%80%A7%E4%B8%8A%E6%8A%A5%E3%80%82%20%20%0A%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE%E6%A0%87%E7%AD%BE%E5%B0%86%E4%B8%BB%E8%A6%81%E8%BF%90%E7%94%A8%E5%9C%A8%E5%9C%B0%E5%9B%BE%E6%9F%A5%E8%AF%A2%E4%B8%AD%E3%80%82%0A%0A%23%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fmqtt-connection.html%23%25E8%25B0%2583%25E7%2594%25A8%25E8%25AE%25BE%25E5%25A4%2587%25E5%258A%259F%25E8%2583%25BD)%20%E8%B0%83%E7%94%A8%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%0A%0A1.%20MqttX%E8%BF%9E%E6%8E%A5%E4%B8%8A%E5%B9%B3%E5%8F%B0%0A%0A2.%E9%80%89%E6%8B%A9%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97%2C%E7%82%B9%E5%87%BB%E6%89%A7%E8%A1%8C%2C%E5%90%91%E8%AE%BE%E5%A4%87%E5%8F%91%E9%80%81topic%20!%5B%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97%5D(%2Fassets%2Fimg%2Fdevice-function.30195827.png)%0A%0A3.%E5%9C%A8MqttX%E8%AE%A2%E9%98%85topic%E4%B8%BA%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffunction%2Finvoke%2Freply%60%E3%80%82%20!%5B%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97%5D(%2Fassets%2Fimg%2Fmqttx-device-function-replay.304ac535.png)%20%E6%AD%A4%E5%A4%84%E4%BD%BF%E7%94%A8%E7%9A%84%E6%8A%A5%E6%96%87%E4%B8%BA%EF%BC%9A%0A%0A%60%60%60%0A%7B%0A%20%22timestamp%22%3A1601196762389%2C%0A%20%22messageId%22%3A%221422497215780651008%22%2C%0A%20%22output%22%3A%22success%22%2C%0A%20%22success%22%3Atrue%0A%7D%0A%60%60%60%0A%0A%7C%20%E5%8F%82%E6%95%B0%20%7C%20%E8%AF%B4%E6%98%8E%20%7C%0A%7C%20—%20%7C%20—%20%7C%0A%7C%20timestamp%20%7C%20%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%20%7C%0A%7C%20messageId%20%7C%20%E4%B8%8E%E8%AE%BE%E5%A4%87%E4%B8%8B%E5%8F%91%E4%B8%AD%E7%9A%84messageId%E7%9B%B8%E5%90%8C%22%20%7C%0A%7C%20output%20%7C%20%E8%BF%94%E5%9B%9E%E6%89%A7%E8%A1%8C%E7%BB%93%E6%9E%9C%2C%E5%85%B7%E4%BD%93%E7%B1%BB%E5%9E%8B%E4%B8%8E%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%B8%AD%E5%8A%9F%E8%83%BD%E8%BE%93%E5%87%BA%E7%B1%BB%E5%9E%8B%E4%B8%80%E8%87%B4%20%7C%0A%7C%20success%20%7C%20%E6%88%90%E5%8A%9F%E7%8A%B6%E6%80%81%20%7C%0A%0A4.%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E8%B0%83%E7%94%A8%E6%88%90%E5%8A%9F%20%0A!%5B%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97%5D(%2Fassets%2Fimg%2Fmqttx-device-function-success.5dcd6cd7.png)