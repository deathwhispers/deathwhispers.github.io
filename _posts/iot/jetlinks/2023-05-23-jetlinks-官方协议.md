---
layout: post
title: JetLinks 官方协议
slug: jetlinks-official-protocol
type:
  - note
date: 2023-05-23
status: draft
tags:
  - JetLinks
categories:
  - IoT
  - JetLinks
mood:
weather:
author: deathwhispers
created: 2023-05-23 11:45
updated: 2023-05-23 18:33
---


# JetLinks 官方协议

除了使用自定义协议以外,jetlinks提供了默认的协议支持. 设备可以使用此协议接入平台. 设备协议已经确定并且无法修改协议的时候,建议使用[自定义协议接入](http://doc.jetlinks.cn/basics-guide/protocol-support.html)

[查看源码 (opens new window)](https://github.com/jetlinks/jetlinks-official-protocol)

## 官方协议topic主题说明

| 名词 | 解释 |
| --- | --- |
| 上行topic | 设备端向平台发送 |
| 下行topic | 平台向设备端发送 |

## Topic列表

### 下行Topic

```plain text
读取设备属性: /{productId}/{deviceId}/properties/read
     修改设备属性: /{productId}/{deviceId}/properties/write
     调用设备功能: /{productId}/{deviceId}/function/invoke
```

### 网关设备

```plain text
读取子设备属性: /{productId}/{deviceId}/child/{childDeviceId}/properties/read
      修改子设备属性: /{productId}/{deviceId}/child/{childDeviceId}/properties/write
      调用子设备功能: /{productId}/{deviceId}/child/{childDeviceId}/function/invoke
```

### 上行Topic

```plain text
读取属性回复: /{productId}/{deviceId}/properties/read/reply
      修改属性回复: /{productId}/{deviceId}/properties/write/reply
      调用设备功能: /{productId}/{deviceId}/function/invoke/reply
      上报设备事件: /{productId}/{deviceId}/event/{eventId}
      上报设备属性: /{productId}/{deviceId}/properties/report
      上报设备派生物模型: /{productId}/{deviceId}/metadata/derived
```

### 网关设备

```plain text
子设备上线消息: /{productId}/{deviceId}/child/{childDeviceId}/connected
      子设备下线消息: /{productId}/{deviceId}/child/{childDeviceId}/disconnect
      读取子设备属性回复: /{productId}/{deviceId}/child/{childDeviceId}/properties/read/reply
      修改子设备属性回复: /{productId}/{deviceId}/child/{childDeviceId}/properties/write/reply
      调用子设备功能回复: /{productId}/{deviceId}/child/{childDeviceId}/function/invoke/reply
      上报子设备事件: /{productId}/{deviceId}/child/{childDeviceId}/event/{eventId}
      上报子设备派生物模型: /{productId}/{deviceId}/child/{childDeviceId}/metadata/derived
```

## MQTT接入

目前支持MQTT3.1.1和3.1版本协议.

### 认证

CONNECT报文:

```plain text
clientId: 设备实例ID
username: secureId+"|"+timestamp
password: md5(secureId+"|"+timestamp+"|"+secureKey)
```

[在线生成工具](http://doc.jetlinks.cn/basics-guide/mqtt-auth-generator.html)

说明: secureId以及secureKey在创建设备产品和设备实例时进行配置. timestamp为当前系统时间戳(毫秒),与系统时间不能相差5分钟.

### 读取设备属性

topic: /{productId}/{deviceId}/properties/read

方向: 下行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"消息ID",
    "deviceId":"设备ID",
    "properties":["sn","model"] //要读取到属性列表
}
```

回复Topic: /{productId}/{deviceId}/properties/read/reply

回复消息格式:

```plain text
//成功
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"与下行消息中的messageId相同",
    "properties":{"sn":"test","model":"test"}, //key与设备模型中定义的属性id一致
    "deviceId":"设备ID",
    "success":true
}
//失败. 下同
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"与下行消息中的messageId相同",
    "success":false,
    "code":"error_code",
    "message":"失败原因"
}
```

### 修改设备属性

topic: /{productId}/{deviceId}/properties/write

方向: 下行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"消息ID",
    "deviceId":"设备ID",
    "properties":{"color":"red"} //要设置的属性
}
```

回复Topic: /{productId}/{deviceId}/properties/write/reply

方向: 上行

回复消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"与下行消息中的messageId相同",
    "properties":{"color":"red"}, //设置成功后的属性,可不返回
    "success":true
}
```

### 设备属性上报

topic: /{productId}/{deviceId}/properties/report

方向: 上行

消息格式:

```plain text
{
    "deviceId":"设备id",
    "properties":{"temp":36.8} //上报数据
}
```

### 调用设备功能

topic: /{productId}/{deviceId}/function/invoke

方向: 下行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"消息ID",
    "deviceId":"设备ID",
    "function":"playVoice",//功能ID
    "inputs":[{"name":"text","value":"播放声音"}] //参数
}
```

回复Topic: /{productId}/{deviceId}/function/invoke/reply

方向: 上行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"与下行消息中的messageId相同",
    "output":"success", //返回执行结果,具体类型与物模型中功能输出类型一致
    "success":true,
}
```

### 设备事件上报

topic: /{productId}/{deviceId}/event/{eventId}

方向: 上行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"随机消息ID",
    "data":100 //上报数据,类型与物模型事件中定义的类型一致
}
```

### 子设备注册

与子设备消息配合使用,实现设备与网关设备进行自动绑定.

topic: /{productId}/{deviceId}/child/{childDeviceId}/register

方向: 上行

消息格式:

```plain text
{
"timestamp":1601196762389, //毫秒时间戳
"messageId":"随机消息ID",
"deviceId":"子设备ID",
"headers":{
    "productId":"子设备在平台的产品ID",
    "deviceName":"子设备名称",
    "configuration":{
        "selfManageState":true //子设备自己管理状态(默认false).为true时,平台将发送DeviceCheckMessage到网关来检查子设备状态
    }
 }
}
```

### 子设备注销

与子设备消息配合使用,实现设备与网关设备进行自动解绑.

topic: /{productId}/{deviceId}/child/{childDeviceId}/unregister

方向: 上行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"随机消息ID",
    "deviceId":"子设备ID"
}
```

### 子设备上线

与子设备消息配合使用,实现关联到网关的子设备上线.(默认情况下,网关上线,子设备也会全部自动上线.)

topic: /{productId}/{deviceId}/child/{childDeviceId}/online

方向: 上行

消息格式:

```plain text
{
    "deviceId":"子设备ID", //毫秒时间戳
    "messageId":"随机消息ID",
    "timestamp":1584331469964//时间戳
}
```

### 子设备离线

与子设备消息配合使用,实现关联到网关的子设备离线.(默认情况下,网关离线,子设备也会全部自动离线.)

topic: /{productId}/{deviceId}/child/{childDeviceId}/offline

方向: 上行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"随机消息ID"
}
```

### 断开子设备连接

平台主动断开设备连接时，会发送此指令到网关

topic: /{productId}/{deviceId}/child/{childDeviceId}/disconnect

方向: 下行

消息格式:

```plain text
{
    "deviceId":"子设备ID", //子设备ID
    "messageId":"随机消息ID",
    "timestamp":1584331469964//时间戳
}
```

### 断开子设备连接回复

平台主动断开设备连接时，会发送此指令到网关

topic: /{productId}/{deviceId}/child-reply/{childDeviceId}/disconnect/reply

方向: 上行

消息格式:

```plain text
{
    "deviceId":"子设备ID", //子设备ID
    "messageId":"断开连接指令的ID",
    "timestamp":1584331469964//时间戳
}
```

### 子设备状态检查

在查看子设备详情或者检查设备状态时，将会收到此消息

topic: /{productId}/{deviceId}/child/{childDeviceId}/state-check

方向: 下行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "deviceId":"子设备ID", //子设备ID
    "messageId":"随机消息ID",
}
```

### 子设备状态检查回复

在查看子设备详情或者检查设备状态时，将会收到此消息

topic: /{productId}/{deviceId}/child-reply/{childDeviceId}/state-check/reply

方向: 上行

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "deviceId":"子设备ID", //子设备ID
    "messageId":"状态检查指令的消息ID",
    "state":1 // 1在线，-1离线
}
```

### 子设备消息

topic: /{productId}/{deviceId}/child/{childDeviceId}/{topic}

方向: 上行或下行, 根据{topic}决定.

TIP

{topic} 以及数据格式与设备topic定义一致. 如: 获取子设备属性: /1/d1/child/c1/properties/read,

### 子设备指令回复消息

topic: /{productId}/{deviceId}/child-reply/{childDeviceId}/{topic}

方向: 上行, 根据{topic}决定.

TIP

{topic} 以及数据格式与设备topic定义一致. 如: 获取子设备属性回复: /1/d1/child-reply/c1/properties/read/reply,

### 更新标签消息

topic: /{productId}/{deviceId}/tags

方向上行,更新平台中的设备标签数据

消息格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "tags":{
        "key":"value",
        "key2":"value2"
    }
}
```

### 更新固件消息

topic: /{productId}/{deviceId}/firmware/upgrade

方向下行,更新设备固件.

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "url":"固件文件下载地址",
    "version":"版本号",
    "parameters":{},//其他参数
    "sign":"文件签名值",
    "signMethod":"签名方式",
    "firmwareId":"固件ID",
    "size":100000//文件大小,字节
}
```

### 上报更新固件进度

topic: /{productId}/{deviceId}/firmware/upgrade/progress

方向上行,上报更新固件进度.

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "progress":50,//进度,0-100
    "complete":false, //是否完成更新
    "version":"升级的版本号",
    "success":true,//是否更新成功,complete为true时有效
    "errorReason":"失败原因",
    "firmwareId":"固件ID"
}
```

### 拉取固件更新

topic: /{productId}/{deviceId}/firmware/pull

方向上行,拉取平台的最新固件信息.

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"消息ID",//回复的时候会回复相同的ID
    "currentVersion":"",//当前版本,可以为null
    "requestVersion":"", //请求更新版本,为null或者空字符则为最新版本
}
```

### 拉取固件更新回复

topic: /{productId}/{deviceId}/firmware/pull/reply

方向下行,平台回复拉取的固件信息.

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"请求的ID",
    "url":"固件文件下载地址",
    "version":"版本号",
    "parameters":{},//其他参数
    "sign":"文件签名值",
    "signMethod":"签名方式",
    "firmwareId":"固件ID",
    "size":100000//文件大小,字节
}
```

### 上报固件版本

topic: /{productId}/{deviceId}/firmware/report

方向下行,设备向平台上报固件版本.

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "version":"版本号"
}
```

### 获取固件版本

topic: /{productId}/{deviceId}/firmware/read

方向下行,平台读取设备固件版本

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"消息ID"
}
```

### 获取固件版本回复

topic: /{productId}/{deviceId}/firmware/read

方向上行,设备回复平台读取设备固件版本指令

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "messageId":"读取指令中的消息ID",
    "version":""//版本号
}
```

### 派生物模型上报

topic: /{productId}/{deviceId}/metadata/derived

方向上行,设备上报新的物模型信息

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "metadata":"物模型json字符",
    "all":false//是否全量更新
}
```

### 设备日志上报

topic: /{productId}/{deviceId}/log

方向上行,设备上报新的物模型信息

详细格式:

```plain text
{
    "timestamp":1601196762389, //毫秒时间戳
    "log":"日志内容"
}
```

[查看物模型格式 (opens new window)](http://doc.jetlinks.cn/advancement-guide/jetlinks-protocol.html)

### 透传消息

topic: /{productId}/{deviceId}/direct

方向上行,透传设备消息,将报文传入mqtt payload中

### 时间同步

topic: /{productId}/{deviceId}/time-sync

方向上行,用于同步服务器的时间.格式:

```plain text
{
    "messageId":"消息ID"
}
```

平台回复:

topic: /{productId}/{deviceId}/time-sync/reply

方向下行,同步服务器的时间回复.格式:

```plain text
{
    "messageId":"消息ID",
    "timestamp":1601196762389 //UTC毫秒时间戳
}
```

## CoAP接入

使用CoAP协议接入仅需要对数据进行加密即可.加密算法: AES/ECB/PKCS5Padding.

将请求体进行加密,密钥为在创建设备产品和设备实例时进行配置的(secureKey).

请求地址(URI)与MQTT Topic相同.消息体(payload)与MQTT相同(只支持上行消息).

## DTLS接入

使用CoAP DTLS 协议接入时需要先进行认证:

发送认证请求:

```plain text
POST /{productId}/{deviceId}/request-token
Accept: application/json
Content-Format: application/json
2110: 签名 md5(payload+secureKey)
payload: {"timestamp":"时间戳"}
```

响应结果:

```plain text
2.05 (Content)
payload: {"token":"令牌"}
```

之后的请求中需要将返回的令牌携带到自定义Option:2111

例如:

```plain text
POST /{productId}/{deviceId}/{topic}
2111: 令牌
...其他Option
payload: json数据
```

%23%20JetLinks%20%E5%AE%98%E6%96%B9%E5%8D%8F%E8%AE%AE%0A%0A%5Btoc%5D%0A%0A%E9%99%A4%E4%BA%86%E4%BD%BF%E7%94%A8%E8%87%AA%E5%AE%9A%E4%B9%89%E5%8D%8F%E8%AE%AE%E4%BB%A5%E5%A4%96%2Cjetlinks%E6%8F%90%E4%BE%9B%E4%BA%86%E9%BB%98%E8%AE%A4%E7%9A%84%E5%8D%8F%E8%AE%AE%E6%94%AF%E6%8C%81.%20%E8%AE%BE%E5%A4%87%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E6%AD%A4%E5%8D%8F%E8%AE%AE%E6%8E%A5%E5%85%A5%E5%B9%B3%E5%8F%B0.%20%E8%AE%BE%E5%A4%87%E5%8D%8F%E8%AE%AE%E5%B7%B2%E7%BB%8F%E7%A1%AE%E5%AE%9A%E5%B9%B6%E4%B8%94%E6%97%A0%E6%B3%95%E4%BF%AE%E6%94%B9%E5%8D%8F%E8%AE%AE%E7%9A%84%E6%97%B6%E5%80%99%2C%E5%BB%BA%E8%AE%AE%E4%BD%BF%E7%94%A8%5B%E8%87%AA%E5%AE%9A%E4%B9%89%E5%8D%8F%E8%AE%AE%E6%8E%A5%E5%85%A5%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Fprotocol-support.html)%0A%0A%5B%E6%9F%A5%E7%9C%8B%E6%BA%90%E7%A0%81%20(opens%20new%20window)%5D(https%3A%2F%2Fgithub.com%2Fjetlinks%2Fjetlinks-official-protocol)%0A%0A%23%23%20%E5%AE%98%E6%96%B9%E5%8D%8F%E8%AE%AEtopic%E4%B8%BB%E9%A2%98%E8%AF%B4%E6%98%8E%0A%0A%7C%20%E5%90%8D%E8%AF%8D%20%7C%20%E8%A7%A3%E9%87%8A%20%7C%0A%7C%20—%20%7C%20—%20%7C%0A%7C%20%E4%B8%8A%E8%A1%8Ctopic%20%7C%20%E8%AE%BE%E5%A4%87%E7%AB%AF%E5%90%91%E5%B9%B3%E5%8F%B0%E5%8F%91%E9%80%81%20%7C%0A%7C%20%E4%B8%8B%E8%A1%8Ctopic%20%7C%20%E5%B9%B3%E5%8F%B0%E5%90%91%E8%AE%BE%E5%A4%87%E7%AB%AF%E5%8F%91%E9%80%81%20%7C%0A%0A%23%23%20Topic%E5%88%97%E8%A1%A8%0A%0A%23%23%23%20%E4%B8%8B%E8%A1%8CTopic%0A%0A%60%60%60tex%0A%20%20%20%20%20%E8%AF%BB%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fread%0A%20%20%20%20%20%E4%BF%AE%E6%94%B9%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fwrite%0A%20%20%20%20%20%E8%B0%83%E7%94%A8%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffunction%2Finvoke%0A%60%60%60%0A%0A%23%23%23%20%E7%BD%91%E5%85%B3%E8%AE%BE%E5%A4%87%0A%0A%60%60%60tex%0A%20%20%20%20%20%20%E8%AF%BB%E5%8F%96%E5%AD%90%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fproperties%2Fread%0A%20%20%20%20%20%20%E4%BF%AE%E6%94%B9%E5%AD%90%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fproperties%2Fwrite%0A%20%20%20%20%20%20%E8%B0%83%E7%94%A8%E5%AD%90%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Ffunction%2Finvoke%0A%60%60%60%0A%0A%23%23%23%20%E4%B8%8A%E8%A1%8CTopic%0A%0A%60%60%60tex%0A%20%20%20%20%20%20%E8%AF%BB%E5%8F%96%E5%B1%9E%E6%80%A7%E5%9B%9E%E5%A4%8D%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fread%2Freply%0A%20%20%20%20%20%20%E4%BF%AE%E6%94%B9%E5%B1%9E%E6%80%A7%E5%9B%9E%E5%A4%8D%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fwrite%2Freply%0A%20%20%20%20%20%20%E8%B0%83%E7%94%A8%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffunction%2Finvoke%2Freply%0A%20%20%20%20%20%20%E4%B8%8A%E6%8A%A5%E8%AE%BE%E5%A4%87%E4%BA%8B%E4%BB%B6%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fevent%2F%7BeventId%7D%0A%20%20%20%20%20%20%E4%B8%8A%E6%8A%A5%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Freport%0A%20%20%20%20%20%20%E4%B8%8A%E6%8A%A5%E8%AE%BE%E5%A4%87%E6%B4%BE%E7%94%9F%E7%89%A9%E6%A8%A1%E5%9E%8B%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fmetadata%2Fderived%0A%60%60%60%0A%0A%23%23%23%20%E7%BD%91%E5%85%B3%E8%AE%BE%E5%A4%87%0A%0A%60%60%60tex%0A%20%20%20%20%20%20%E5%AD%90%E8%AE%BE%E5%A4%87%E4%B8%8A%E7%BA%BF%E6%B6%88%E6%81%AF%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fconnected%0A%20%20%20%20%20%20%E5%AD%90%E8%AE%BE%E5%A4%87%E4%B8%8B%E7%BA%BF%E6%B6%88%E6%81%AF%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fdisconnect%0A%20%20%20%20%20%20%E8%AF%BB%E5%8F%96%E5%AD%90%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%9B%9E%E5%A4%8D%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fproperties%2Fread%2Freply%0A%20%20%20%20%20%20%E4%BF%AE%E6%94%B9%E5%AD%90%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%9B%9E%E5%A4%8D%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fproperties%2Fwrite%2Freply%0A%20%20%20%20%20%20%E8%B0%83%E7%94%A8%E5%AD%90%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%E5%9B%9E%E5%A4%8D%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Ffunction%2Finvoke%2Freply%0A%20%20%20%20%20%20%E4%B8%8A%E6%8A%A5%E5%AD%90%E8%AE%BE%E5%A4%87%E4%BA%8B%E4%BB%B6%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fevent%2F%7BeventId%7D%0A%20%20%20%20%20%20%E4%B8%8A%E6%8A%A5%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B4%BE%E7%94%9F%E7%89%A9%E6%A8%A1%E5%9E%8B%3A%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fmetadata%2Fderived%0A%60%60%60%0A%0A%23%23%20MQTT%E6%8E%A5%E5%85%A5%0A%0A%E7%9B%AE%E5%89%8D%E6%94%AF%E6%8C%81MQTT3.1.1%E5%92%8C3.1%E7%89%88%E6%9C%AC%E5%8D%8F%E8%AE%AE.%0A%0A%23%23%23%20%E8%AE%A4%E8%AF%81%0A%0ACONNECT%E6%8A%A5%E6%96%87%3A%0A%0A%60%60%60tex%0AclientId%3A%20%E8%AE%BE%E5%A4%87%E5%AE%9E%E4%BE%8BID%0Ausername%3A%20secureId%2B%22%7C%22%2Btimestamp%0Apassword%3A%20md5(secureId%2B%22%7C%22%2Btimestamp%2B%22%7C%22%2BsecureKey)%0A%60%60%60%0A%0A%5B%E5%9C%A8%E7%BA%BF%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbasics-guide%2Fmqtt-auth-generator.html)%0A%0A%E8%AF%B4%E6%98%8E%3A%20%60secureId%60%E4%BB%A5%E5%8F%8A%60secureKey%60%E5%9C%A8%E5%88%9B%E5%BB%BA%E8%AE%BE%E5%A4%87%E4%BA%A7%E5%93%81%E5%92%8C%E8%AE%BE%E5%A4%87%E5%AE%9E%E4%BE%8B%E6%97%B6%E8%BF%9B%E8%A1%8C%E9%85%8D%E7%BD%AE.%20%60timestamp%60%E4%B8%BA%E5%BD%93%E5%89%8D%E7%B3%BB%E7%BB%9F%E6%97%B6%E9%97%B4%E6%88%B3(%E6%AF%AB%E7%A7%92)%2C%E4%B8%8E%E7%B3%BB%E7%BB%9F%E6%97%B6%E9%97%B4%E4%B8%8D%E8%83%BD%E7%9B%B8%E5%B7%AE5%E5%88%86%E9%92%9F.%0A%0A%23%23%23%20%E8%AF%BB%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fread%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8B%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22deviceId%22%3A%22%E8%AE%BE%E5%A4%87ID%22%2C%0A%20%20%20%20%22properties%22%3A%5B%22sn%22%2C%22model%22%5D%20%2F%2F%E8%A6%81%E8%AF%BB%E5%8F%96%E5%88%B0%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8%0A%7D%0A%60%60%60%0A%0A%E5%9B%9E%E5%A4%8DTopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fread%2Freply%60%0A%0A%E5%9B%9E%E5%A4%8D%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%2F%2F%E6%88%90%E5%8A%9F%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E4%B8%8E%E4%B8%8B%E8%A1%8C%E6%B6%88%E6%81%AF%E4%B8%AD%E7%9A%84messageId%E7%9B%B8%E5%90%8C%22%2C%0A%20%20%20%20%22properties%22%3A%7B%22sn%22%3A%22test%22%2C%22model%22%3A%22test%22%7D%2C%20%2F%2Fkey%E4%B8%8E%E8%AE%BE%E5%A4%87%E6%A8%A1%E5%9E%8B%E4%B8%AD%E5%AE%9A%E4%B9%89%E7%9A%84%E5%B1%9E%E6%80%A7id%E4%B8%80%E8%87%B4%0A%20%20%20%20%22deviceId%22%3A%22%E8%AE%BE%E5%A4%87ID%22%2C%0A%20%20%20%20%22success%22%3Atrue%0A%7D%0A%2F%2F%E5%A4%B1%E8%B4%A5.%20%E4%B8%8B%E5%90%8C%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E4%B8%8E%E4%B8%8B%E8%A1%8C%E6%B6%88%E6%81%AF%E4%B8%AD%E7%9A%84messageId%E7%9B%B8%E5%90%8C%22%2C%0A%20%20%20%20%22success%22%3Afalse%2C%0A%20%20%20%20%22code%22%3A%22error_code%22%2C%0A%20%20%20%20%22message%22%3A%22%E5%A4%B1%E8%B4%A5%E5%8E%9F%E5%9B%A0%22%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E4%BF%AE%E6%94%B9%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fwrite%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8B%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22deviceId%22%3A%22%E8%AE%BE%E5%A4%87ID%22%2C%0A%20%20%20%20%22properties%22%3A%7B%22color%22%3A%22red%22%7D%20%2F%2F%E8%A6%81%E8%AE%BE%E7%BD%AE%E7%9A%84%E5%B1%9E%E6%80%A7%0A%7D%0A%60%60%60%0A%0A%E5%9B%9E%E5%A4%8DTopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Fwrite%2Freply%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E5%9B%9E%E5%A4%8D%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E4%B8%8E%E4%B8%8B%E8%A1%8C%E6%B6%88%E6%81%AF%E4%B8%AD%E7%9A%84messageId%E7%9B%B8%E5%90%8C%22%2C%0A%20%20%20%20%22properties%22%3A%7B%22color%22%3A%22red%22%7D%2C%20%2F%2F%E8%AE%BE%E7%BD%AE%E6%88%90%E5%8A%9F%E5%90%8E%E7%9A%84%E5%B1%9E%E6%80%A7%2C%E5%8F%AF%E4%B8%8D%E8%BF%94%E5%9B%9E%0A%20%20%20%20%22success%22%3Atrue%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E4%B8%8A%E6%8A%A5%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fproperties%2Freport%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22deviceId%22%3A%22%E8%AE%BE%E5%A4%87id%22%2C%0A%20%20%20%20%22properties%22%3A%7B%22temp%22%3A36.8%7D%20%2F%2F%E4%B8%8A%E6%8A%A5%E6%95%B0%E6%8D%AE%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E8%B0%83%E7%94%A8%E8%AE%BE%E5%A4%87%E5%8A%9F%E8%83%BD%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffunction%2Finvoke%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8B%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22deviceId%22%3A%22%E8%AE%BE%E5%A4%87ID%22%2C%0A%20%20%20%20%22function%22%3A%22playVoice%22%2C%2F%2F%E5%8A%9F%E8%83%BDID%0A%20%20%20%20%22inputs%22%3A%5B%7B%22name%22%3A%22text%22%2C%22value%22%3A%22%E6%92%AD%E6%94%BE%E5%A3%B0%E9%9F%B3%22%7D%5D%20%2F%2F%E5%8F%82%E6%95%B0%0A%7D%0A%60%60%60%0A%0A%E5%9B%9E%E5%A4%8DTopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffunction%2Finvoke%2Freply%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E4%B8%8E%E4%B8%8B%E8%A1%8C%E6%B6%88%E6%81%AF%E4%B8%AD%E7%9A%84messageId%E7%9B%B8%E5%90%8C%22%2C%0A%20%20%20%20%22output%22%3A%22success%22%2C%20%2F%2F%E8%BF%94%E5%9B%9E%E6%89%A7%E8%A1%8C%E7%BB%93%E6%9E%9C%2C%E5%85%B7%E4%BD%93%E7%B1%BB%E5%9E%8B%E4%B8%8E%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%B8%AD%E5%8A%9F%E8%83%BD%E8%BE%93%E5%87%BA%E7%B1%BB%E5%9E%8B%E4%B8%80%E8%87%B4%0A%20%20%20%20%22success%22%3Atrue%2C%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E8%AE%BE%E5%A4%87%E4%BA%8B%E4%BB%B6%E4%B8%8A%E6%8A%A5%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fevent%2F%7BeventId%7D%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22data%22%3A100%20%2F%2F%E4%B8%8A%E6%8A%A5%E6%95%B0%E6%8D%AE%2C%E7%B1%BB%E5%9E%8B%E4%B8%8E%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%BA%8B%E4%BB%B6%E4%B8%AD%E5%AE%9A%E4%B9%89%E7%9A%84%E7%B1%BB%E5%9E%8B%E4%B8%80%E8%87%B4%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B3%A8%E5%86%8C%0A%0A%E4%B8%8E%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%E9%85%8D%E5%90%88%E4%BD%BF%E7%94%A8%2C%E5%AE%9E%E7%8E%B0%E8%AE%BE%E5%A4%87%E4%B8%8E%E7%BD%91%E5%85%B3%E8%AE%BE%E5%A4%87%E8%BF%9B%E8%A1%8C%E8%87%AA%E5%8A%A8%E7%BB%91%E5%AE%9A.%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fregister%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%22messageId%22%3A%22%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%22%2C%0A%22deviceId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87ID%22%2C%0A%22headers%22%3A%7B%0A%20%20%20%20%22productId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87%E5%9C%A8%E5%B9%B3%E5%8F%B0%E7%9A%84%E4%BA%A7%E5%93%81ID%22%2C%0A%20%20%20%20%22deviceName%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87%E5%90%8D%E7%A7%B0%22%2C%0A%20%20%20%20%22configuration%22%3A%7B%0A%20%20%20%20%20%20%20%20%22selfManageState%22%3Atrue%20%2F%2F%E5%AD%90%E8%AE%BE%E5%A4%87%E8%87%AA%E5%B7%B1%E7%AE%A1%E7%90%86%E7%8A%B6%E6%80%81(%E9%BB%98%E8%AE%A4false).%E4%B8%BAtrue%E6%97%B6%2C%E5%B9%B3%E5%8F%B0%E5%B0%86%E5%8F%91%E9%80%81DeviceCheckMessage%E5%88%B0%E7%BD%91%E5%85%B3%E6%9D%A5%E6%A3%80%E6%9F%A5%E5%AD%90%E8%AE%BE%E5%A4%87%E7%8A%B6%E6%80%81%0A%20%20%20%20%7D%0A%20%7D%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B3%A8%E9%94%80%0A%0A%E4%B8%8E%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%E9%85%8D%E5%90%88%E4%BD%BF%E7%94%A8%2C%E5%AE%9E%E7%8E%B0%E8%AE%BE%E5%A4%87%E4%B8%8E%E7%BD%91%E5%85%B3%E8%AE%BE%E5%A4%87%E8%BF%9B%E8%A1%8C%E8%87%AA%E5%8A%A8%E8%A7%A3%E7%BB%91.%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Funregister%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22deviceId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87ID%22%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E4%B8%8A%E7%BA%BF%0A%0A%E4%B8%8E%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%E9%85%8D%E5%90%88%E4%BD%BF%E7%94%A8%2C%E5%AE%9E%E7%8E%B0%E5%85%B3%E8%81%94%E5%88%B0%E7%BD%91%E5%85%B3%E7%9A%84%E5%AD%90%E8%AE%BE%E5%A4%87%E4%B8%8A%E7%BA%BF.(%E9%BB%98%E8%AE%A4%E6%83%85%E5%86%B5%E4%B8%8B%2C%E7%BD%91%E5%85%B3%E4%B8%8A%E7%BA%BF%2C%E5%AD%90%E8%AE%BE%E5%A4%87%E4%B9%9F%E4%BC%9A%E5%85%A8%E9%83%A8%E8%87%AA%E5%8A%A8%E4%B8%8A%E7%BA%BF.)%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fonline%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22deviceId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87ID%22%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22timestamp%22%3A1584331469964%2F%2F%E6%97%B6%E9%97%B4%E6%88%B3%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E7%A6%BB%E7%BA%BF%0A%0A%E4%B8%8E%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%E9%85%8D%E5%90%88%E4%BD%BF%E7%94%A8%2C%E5%AE%9E%E7%8E%B0%E5%85%B3%E8%81%94%E5%88%B0%E7%BD%91%E5%85%B3%E7%9A%84%E5%AD%90%E8%AE%BE%E5%A4%87%E7%A6%BB%E7%BA%BF.(%E9%BB%98%E8%AE%A4%E6%83%85%E5%86%B5%E4%B8%8B%2C%E7%BD%91%E5%85%B3%E7%A6%BB%E7%BA%BF%2C%E5%AD%90%E8%AE%BE%E5%A4%87%E4%B9%9F%E4%BC%9A%E5%85%A8%E9%83%A8%E8%87%AA%E5%8A%A8%E7%A6%BB%E7%BA%BF.)%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Foffline%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%22%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%96%AD%E5%BC%80%E5%AD%90%E8%AE%BE%E5%A4%87%E8%BF%9E%E6%8E%A5%0A%0A%E5%B9%B3%E5%8F%B0%E4%B8%BB%E5%8A%A8%E6%96%AD%E5%BC%80%E8%AE%BE%E5%A4%87%E8%BF%9E%E6%8E%A5%E6%97%B6%EF%BC%8C%E4%BC%9A%E5%8F%91%E9%80%81%E6%AD%A4%E6%8C%87%E4%BB%A4%E5%88%B0%E7%BD%91%E5%85%B3%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fdisconnect%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8B%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22deviceId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87ID%22%2C%20%2F%2F%E5%AD%90%E8%AE%BE%E5%A4%87ID%0A%20%20%20%20%22messageId%22%3A%22%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22timestamp%22%3A1584331469964%2F%2F%E6%97%B6%E9%97%B4%E6%88%B3%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%96%AD%E5%BC%80%E5%AD%90%E8%AE%BE%E5%A4%87%E8%BF%9E%E6%8E%A5%E5%9B%9E%E5%A4%8D%0A%0A%E5%B9%B3%E5%8F%B0%E4%B8%BB%E5%8A%A8%E6%96%AD%E5%BC%80%E8%AE%BE%E5%A4%87%E8%BF%9E%E6%8E%A5%E6%97%B6%EF%BC%8C%E4%BC%9A%E5%8F%91%E9%80%81%E6%AD%A4%E6%8C%87%E4%BB%A4%E5%88%B0%E7%BD%91%E5%85%B3%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild-reply%2F%7BchildDeviceId%7D%2Fdisconnect%2Freply%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22deviceId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87ID%22%2C%20%2F%2F%E5%AD%90%E8%AE%BE%E5%A4%87ID%0A%20%20%20%20%22messageId%22%3A%22%E6%96%AD%E5%BC%80%E8%BF%9E%E6%8E%A5%E6%8C%87%E4%BB%A4%E7%9A%84ID%22%2C%0A%20%20%20%20%22timestamp%22%3A1584331469964%2F%2F%E6%97%B6%E9%97%B4%E6%88%B3%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5%0A%0A%E5%9C%A8%E6%9F%A5%E7%9C%8B%E5%AD%90%E8%AE%BE%E5%A4%87%E8%AF%A6%E6%83%85%E6%88%96%E8%80%85%E6%A3%80%E6%9F%A5%E8%AE%BE%E5%A4%87%E7%8A%B6%E6%80%81%E6%97%B6%EF%BC%8C%E5%B0%86%E4%BC%9A%E6%94%B6%E5%88%B0%E6%AD%A4%E6%B6%88%E6%81%AF%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2Fstate-check%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8B%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22deviceId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87ID%22%2C%20%2F%2F%E5%AD%90%E8%AE%BE%E5%A4%87ID%0A%20%20%20%20%22messageId%22%3A%22%E9%9A%8F%E6%9C%BA%E6%B6%88%E6%81%AFID%22%2C%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5%E5%9B%9E%E5%A4%8D%0A%0A%E5%9C%A8%E6%9F%A5%E7%9C%8B%E5%AD%90%E8%AE%BE%E5%A4%87%E8%AF%A6%E6%83%85%E6%88%96%E8%80%85%E6%A3%80%E6%9F%A5%E8%AE%BE%E5%A4%87%E7%8A%B6%E6%80%81%E6%97%B6%EF%BC%8C%E5%B0%86%E4%BC%9A%E6%94%B6%E5%88%B0%E6%AD%A4%E6%B6%88%E6%81%AF%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild-reply%2F%7BchildDeviceId%7D%2Fstate-check%2Freply%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22deviceId%22%3A%22%E5%AD%90%E8%AE%BE%E5%A4%87ID%22%2C%20%2F%2F%E5%AD%90%E8%AE%BE%E5%A4%87ID%0A%20%20%20%20%22messageId%22%3A%22%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5%E6%8C%87%E4%BB%A4%E7%9A%84%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22state%22%3A1%20%2F%2F%201%E5%9C%A8%E7%BA%BF%EF%BC%8C-1%E7%A6%BB%E7%BA%BF%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild%2F%7BchildDeviceId%7D%2F%7Btopic%7D%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%E6%88%96%E4%B8%8B%E8%A1%8C%60%2C%20%E6%A0%B9%E6%8D%AE%7Btopic%7D%E5%86%B3%E5%AE%9A.%0A%0ATIP%0A%0A%7Btopic%7D%20%E4%BB%A5%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E4%B8%8E%E8%AE%BE%E5%A4%87topic%E5%AE%9A%E4%B9%89%E4%B8%80%E8%87%B4.%20%E5%A6%82%3A%20%E8%8E%B7%E5%8F%96%E5%AD%90%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%3A%20%60%2F1%2Fd1%2Fchild%2Fc1%2Fproperties%2Fread%60%2C%0A%0A%23%23%23%20%E5%AD%90%E8%AE%BE%E5%A4%87%E6%8C%87%E4%BB%A4%E5%9B%9E%E5%A4%8D%E6%B6%88%E6%81%AF%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fchild-reply%2F%7BchildDeviceId%7D%2F%7Btopic%7D%60%0A%0A%E6%96%B9%E5%90%91%3A%20%60%E4%B8%8A%E8%A1%8C%60%2C%20%E6%A0%B9%E6%8D%AE%7Btopic%7D%E5%86%B3%E5%AE%9A.%0A%0ATIP%0A%0A%7Btopic%7D%20%E4%BB%A5%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E4%B8%8E%E8%AE%BE%E5%A4%87topic%E5%AE%9A%E4%B9%89%E4%B8%80%E8%87%B4.%20%E5%A6%82%3A%20%E8%8E%B7%E5%8F%96%E5%AD%90%E8%AE%BE%E5%A4%87%E5%B1%9E%E6%80%A7%E5%9B%9E%E5%A4%8D%3A%20%60%2F1%2Fd1%2Fchild-reply%2Fc1%2Fproperties%2Fread%2Freply%60%2C%0A%0A%23%23%23%20%E6%9B%B4%E6%96%B0%E6%A0%87%E7%AD%BE%E6%B6%88%E6%81%AF%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ftags%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E6%9B%B4%E6%96%B0%E5%B9%B3%E5%8F%B0%E4%B8%AD%E7%9A%84%E8%AE%BE%E5%A4%87%E6%A0%87%E7%AD%BE%E6%95%B0%E6%8D%AE%0A%0A%E6%B6%88%E6%81%AF%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22tags%22%3A%7B%0A%20%20%20%20%20%20%20%20%22key%22%3A%22value%22%2C%0A%20%20%20%20%20%20%20%20%22key2%22%3A%22value2%22%0A%20%20%20%20%7D%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%9B%B4%E6%96%B0%E5%9B%BA%E4%BB%B6%E6%B6%88%E6%81%AF%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffirmware%2Fupgrade%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8B%E8%A1%8C%60%2C%E6%9B%B4%E6%96%B0%E8%AE%BE%E5%A4%87%E5%9B%BA%E4%BB%B6.%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22url%22%3A%22%E5%9B%BA%E4%BB%B6%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD%E5%9C%B0%E5%9D%80%22%2C%0A%20%20%20%20%22version%22%3A%22%E7%89%88%E6%9C%AC%E5%8F%B7%22%2C%0A%20%20%20%20%22parameters%22%3A%7B%7D%2C%2F%2F%E5%85%B6%E4%BB%96%E5%8F%82%E6%95%B0%0A%20%20%20%20%22sign%22%3A%22%E6%96%87%E4%BB%B6%E7%AD%BE%E5%90%8D%E5%80%BC%22%2C%0A%20%20%20%20%22signMethod%22%3A%22%E7%AD%BE%E5%90%8D%E6%96%B9%E5%BC%8F%22%2C%0A%20%20%20%20%22firmwareId%22%3A%22%E5%9B%BA%E4%BB%B6ID%22%2C%0A%20%20%20%20%22size%22%3A100000%2F%2F%E6%96%87%E4%BB%B6%E5%A4%A7%E5%B0%8F%2C%E5%AD%97%E8%8A%82%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E4%B8%8A%E6%8A%A5%E6%9B%B4%E6%96%B0%E5%9B%BA%E4%BB%B6%E8%BF%9B%E5%BA%A6%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffirmware%2Fupgrade%2Fprogress%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E4%B8%8A%E6%8A%A5%E6%9B%B4%E6%96%B0%E5%9B%BA%E4%BB%B6%E8%BF%9B%E5%BA%A6.%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22progress%22%3A50%2C%2F%2F%E8%BF%9B%E5%BA%A6%2C0-100%0A%20%20%20%20%22complete%22%3Afalse%2C%20%2F%2F%E6%98%AF%E5%90%A6%E5%AE%8C%E6%88%90%E6%9B%B4%E6%96%B0%0A%20%20%20%20%22version%22%3A%22%E5%8D%87%E7%BA%A7%E7%9A%84%E7%89%88%E6%9C%AC%E5%8F%B7%22%2C%0A%20%20%20%20%22success%22%3Atrue%2C%2F%2F%E6%98%AF%E5%90%A6%E6%9B%B4%E6%96%B0%E6%88%90%E5%8A%9F%2Ccomplete%E4%B8%BAtrue%E6%97%B6%E6%9C%89%E6%95%88%0A%20%20%20%20%22errorReason%22%3A%22%E5%A4%B1%E8%B4%A5%E5%8E%9F%E5%9B%A0%22%2C%0A%20%20%20%20%22firmwareId%22%3A%22%E5%9B%BA%E4%BB%B6ID%22%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%8B%89%E5%8F%96%E5%9B%BA%E4%BB%B6%E6%9B%B4%E6%96%B0%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffirmware%2Fpull%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E6%8B%89%E5%8F%96%E5%B9%B3%E5%8F%B0%E7%9A%84%E6%9C%80%E6%96%B0%E5%9B%BA%E4%BB%B6%E4%BF%A1%E6%81%AF.%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E6%B6%88%E6%81%AFID%22%2C%2F%2F%E5%9B%9E%E5%A4%8D%E7%9A%84%E6%97%B6%E5%80%99%E4%BC%9A%E5%9B%9E%E5%A4%8D%E7%9B%B8%E5%90%8C%E7%9A%84ID%0A%20%20%20%20%22currentVersion%22%3A%22%22%2C%2F%2F%E5%BD%93%E5%89%8D%E7%89%88%E6%9C%AC%2C%E5%8F%AF%E4%BB%A5%E4%B8%BAnull%0A%20%20%20%20%22requestVersion%22%3A%22%22%2C%20%2F%2F%E8%AF%B7%E6%B1%82%E6%9B%B4%E6%96%B0%E7%89%88%E6%9C%AC%2C%E4%B8%BAnull%E6%88%96%E8%80%85%E7%A9%BA%E5%AD%97%E7%AC%A6%E5%88%99%E4%B8%BA%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%8B%89%E5%8F%96%E5%9B%BA%E4%BB%B6%E6%9B%B4%E6%96%B0%E5%9B%9E%E5%A4%8D%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffirmware%2Fpull%2Freply%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8B%E8%A1%8C%60%2C%E5%B9%B3%E5%8F%B0%E5%9B%9E%E5%A4%8D%E6%8B%89%E5%8F%96%E7%9A%84%E5%9B%BA%E4%BB%B6%E4%BF%A1%E6%81%AF.%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E8%AF%B7%E6%B1%82%E7%9A%84ID%22%2C%0A%20%20%20%20%22url%22%3A%22%E5%9B%BA%E4%BB%B6%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD%E5%9C%B0%E5%9D%80%22%2C%0A%20%20%20%20%22version%22%3A%22%E7%89%88%E6%9C%AC%E5%8F%B7%22%2C%0A%20%20%20%20%22parameters%22%3A%7B%7D%2C%2F%2F%E5%85%B6%E4%BB%96%E5%8F%82%E6%95%B0%0A%20%20%20%20%22sign%22%3A%22%E6%96%87%E4%BB%B6%E7%AD%BE%E5%90%8D%E5%80%BC%22%2C%0A%20%20%20%20%22signMethod%22%3A%22%E7%AD%BE%E5%90%8D%E6%96%B9%E5%BC%8F%22%2C%0A%20%20%20%20%22firmwareId%22%3A%22%E5%9B%BA%E4%BB%B6ID%22%2C%0A%20%20%20%20%22size%22%3A100000%2F%2F%E6%96%87%E4%BB%B6%E5%A4%A7%E5%B0%8F%2C%E5%AD%97%E8%8A%82%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E4%B8%8A%E6%8A%A5%E5%9B%BA%E4%BB%B6%E7%89%88%E6%9C%AC%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffirmware%2Freport%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8B%E8%A1%8C%60%2C%E8%AE%BE%E5%A4%87%E5%90%91%E5%B9%B3%E5%8F%B0%E4%B8%8A%E6%8A%A5%E5%9B%BA%E4%BB%B6%E7%89%88%E6%9C%AC.%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22version%22%3A%22%E7%89%88%E6%9C%AC%E5%8F%B7%22%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E8%8E%B7%E5%8F%96%E5%9B%BA%E4%BB%B6%E7%89%88%E6%9C%AC%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffirmware%2Fread%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8B%E8%A1%8C%60%2C%E5%B9%B3%E5%8F%B0%E8%AF%BB%E5%8F%96%E8%AE%BE%E5%A4%87%E5%9B%BA%E4%BB%B6%E7%89%88%E6%9C%AC%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E6%B6%88%E6%81%AFID%22%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E8%8E%B7%E5%8F%96%E5%9B%BA%E4%BB%B6%E7%89%88%E6%9C%AC%E5%9B%9E%E5%A4%8D%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ffirmware%2Fread%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E8%AE%BE%E5%A4%87%E5%9B%9E%E5%A4%8D%E5%B9%B3%E5%8F%B0%E8%AF%BB%E5%8F%96%E8%AE%BE%E5%A4%87%E5%9B%BA%E4%BB%B6%E7%89%88%E6%9C%AC%E6%8C%87%E4%BB%A4%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22messageId%22%3A%22%E8%AF%BB%E5%8F%96%E6%8C%87%E4%BB%A4%E4%B8%AD%E7%9A%84%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22version%22%3A%22%22%2F%2F%E7%89%88%E6%9C%AC%E5%8F%B7%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%B4%BE%E7%94%9F%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%B8%8A%E6%8A%A5%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fmetadata%2Fderived%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E8%AE%BE%E5%A4%87%E4%B8%8A%E6%8A%A5%E6%96%B0%E7%9A%84%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%BF%A1%E6%81%AF%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22metadata%22%3A%22%E7%89%A9%E6%A8%A1%E5%9E%8Bjson%E5%AD%97%E7%AC%A6%22%2C%0A%20%20%20%20%22all%22%3Afalse%2F%2F%E6%98%AF%E5%90%A6%E5%85%A8%E9%87%8F%E6%9B%B4%E6%96%B0%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E8%AE%BE%E5%A4%87%E6%97%A5%E5%BF%97%E4%B8%8A%E6%8A%A5%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Flog%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E8%AE%BE%E5%A4%87%E4%B8%8A%E6%8A%A5%E6%96%B0%E7%9A%84%E7%89%A9%E6%A8%A1%E5%9E%8B%E4%BF%A1%E6%81%AF%0A%0A%E8%AF%A6%E7%BB%86%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22timestamp%22%3A1601196762389%2C%20%2F%2F%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%20%20%20%20%22log%22%3A%22%E6%97%A5%E5%BF%97%E5%86%85%E5%AE%B9%22%0A%7D%0A%60%60%60%0A%0A%5B%E6%9F%A5%E7%9C%8B%E7%89%A9%E6%A8%A1%E5%9E%8B%E6%A0%BC%E5%BC%8F%20(opens%20new%20window)%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fadvancement-guide%2Fjetlinks-protocol.html)%0A%0A%23%23%23%20%E9%80%8F%E4%BC%A0%E6%B6%88%E6%81%AF%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Fdirect%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E9%80%8F%E4%BC%A0%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%2C%E5%B0%86%E6%8A%A5%E6%96%87%E4%BC%A0%E5%85%A5%60mqtt%20payload%60%E4%B8%AD%0A%0A%23%23%23%20%E6%97%B6%E9%97%B4%E5%90%8C%E6%AD%A5%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ftime-sync%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8A%E8%A1%8C%60%2C%E7%94%A8%E4%BA%8E%E5%90%8C%E6%AD%A5%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%9A%84%E6%97%B6%E9%97%B4.%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22messageId%22%3A%22%E6%B6%88%E6%81%AFID%22%0A%7D%0A%60%60%60%0A%0A%E5%B9%B3%E5%8F%B0%E5%9B%9E%E5%A4%8D%3A%0A%0Atopic%3A%20%60%2F%7BproductId%7D%2F%7BdeviceId%7D%2Ftime-sync%2Freply%60%0A%0A%E6%96%B9%E5%90%91%60%E4%B8%8B%E8%A1%8C%60%2C%E5%90%8C%E6%AD%A5%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%9A%84%E6%97%B6%E9%97%B4%E5%9B%9E%E5%A4%8D.%E6%A0%BC%E5%BC%8F%3A%0A%0A%60%60%60json%0A%7B%0A%20%20%20%20%22messageId%22%3A%22%E6%B6%88%E6%81%AFID%22%2C%0A%20%20%20%20%22timestamp%22%3A1601196762389%20%2F%2FUTC%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3%0A%7D%0A%60%60%60%0A%0A%23%23%20CoAP%E6%8E%A5%E5%85%A5%0A%0A%E4%BD%BF%E7%94%A8CoAP%E5%8D%8F%E8%AE%AE%E6%8E%A5%E5%85%A5%E4%BB%85%E9%9C%80%E8%A6%81%E5%AF%B9%E6%95%B0%E6%8D%AE%E8%BF%9B%E8%A1%8C%E5%8A%A0%E5%AF%86%E5%8D%B3%E5%8F%AF.%E5%8A%A0%E5%AF%86%E7%AE%97%E6%B3%95%3A%20AES%2FECB%2FPKCS5Padding.%0A%0A%E5%B0%86%E8%AF%B7%E6%B1%82%E4%BD%93%E8%BF%9B%E8%A1%8C%E5%8A%A0%E5%AF%86%2C%E5%AF%86%E9%92%A5%E4%B8%BA%E5%9C%A8%E5%88%9B%E5%BB%BA%E8%AE%BE%E5%A4%87%E4%BA%A7%E5%93%81%E5%92%8C%E8%AE%BE%E5%A4%87%E5%AE%9E%E4%BE%8B%E6%97%B6%E8%BF%9B%E8%A1%8C%E9%85%8D%E7%BD%AE%E7%9A%84(%60secureKey%60).%0A%0A%E8%AF%B7%E6%B1%82%E5%9C%B0%E5%9D%80(%60URI%60)%E4%B8%8EMQTT%20%60Topic%60%E7%9B%B8%E5%90%8C.%E6%B6%88%E6%81%AF%E4%BD%93(%60payload%60)%E4%B8%8EMQTT%E7%9B%B8%E5%90%8C(%E5%8F%AA%E6%94%AF%E6%8C%81%E4%B8%8A%E8%A1%8C%E6%B6%88%E6%81%AF).%0A%0A%23%23%20DTLS%E6%8E%A5%E5%85%A5%0A%0A%E4%BD%BF%E7%94%A8CoAP%20DTLS%20%E5%8D%8F%E8%AE%AE%E6%8E%A5%E5%85%A5%E6%97%B6%E9%9C%80%E8%A6%81%E5%85%88%E8%BF%9B%E8%A1%8C%E8%AE%A4%E8%AF%81%3A%0A%0A%E5%8F%91%E9%80%81%E8%AE%A4%E8%AF%81%E8%AF%B7%E6%B1%82%3A%0A%0A%60%60%60http%0APOST%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2Frequest-token%0AAccept%3A%20application%2Fjson%0AContent-Format%3A%20application%2Fjson%0A2110%3A%20%E7%AD%BE%E5%90%8D%20md5(payload%2BsecureKey)%0Apayload%3A%20%7B%22timestamp%22%3A%22%E6%97%B6%E9%97%B4%E6%88%B3%22%7D%0A%60%60%60%0A%0A%E5%93%8D%E5%BA%94%E7%BB%93%E6%9E%9C%3A%0A%0A%60%60%60tex%0A2.05%20(Content)%0Apayload%3A%20%7B%22token%22%3A%22%E4%BB%A4%E7%89%8C%22%7D%0A%60%60%60%0A%0A%E4%B9%8B%E5%90%8E%E7%9A%84%E8%AF%B7%E6%B1%82%E4%B8%AD%E9%9C%80%E8%A6%81%E5%B0%86%E8%BF%94%E5%9B%9E%E7%9A%84%E4%BB%A4%E7%89%8C%E6%90%BA%E5%B8%A6%E5%88%B0%E8%87%AA%E5%AE%9A%E4%B9%89Option%3A2111%0A%0A%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60http%0APOST%20%2F%7BproductId%7D%2F%7BdeviceId%7D%2F%7Btopic%7D%0A2111%3A%20%E4%BB%A4%E7%89%8C%0A…%E5%85%B6%E4%BB%96Option%0Apayload%3A%20json%E6%95%B0%E6%8D%AE%0A%60%60%60