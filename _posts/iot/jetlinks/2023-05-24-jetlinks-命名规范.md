---
layout: post
title: JetLinks 命名规范
slug: jetlinks-naming-convention
type:
  - note
date: 2023-05-24
status: draft
tags:
  - JetLinks
categories:
  - IoT
  - JetLinks
mood:
weather:
author: deathwhispers
created: 2023-05-24 11:45
updated: 2023-05-24 18:33
---


# 命名

## [#](http://doc.jetlinks.cn/dev-guide/specification.html#java%E5%91%BD%E5%90%8D) java命名

1. maven模块名小写,多个单词使用
    - 
连接
正确: device-manager 错误: deviceManager
2. 包名全部小写,多个单词使用多个目录层级.
正确: org.jetlinks.pro.device.instance 错误: org.jetlinks.pro.deviceInstance
3. 类名首字母大写,使用驼峰命名.
正确: DeviceInstance 错误: Deviceinstance , Device_Instance
4. 方法名首字母小写,使用驼峰命名. 名称要见名知义.
正确: findById(String id), deployDeviceInstance(ListdeviceInstanceIdList) 错误: getData(String arg)
5. 局部变量首字母小写,使用驼峰命名. 名称要见名知义.
正确: String deviceId = device.getId(); 错误: String str = device.getId();
6. 常量使用大写,多个单词使用
_
分割.
正确: static String DEFAULT_CONFIG = “1”; 错误: static String DEFAULTCONFIG = “1”;

## [#](http://doc.jetlinks.cn/dev-guide/specification.html#java-%E6%8E%A5%E5%8F%A3) java 接口

一个模块在需要提供给其他模块使用时,应该面向接口编程,对外提供相应的接口.并在当前模块提供默认的实现.

当一个模块是具体的业务功能实现时,大部分情况不需要写接口,如一个增删改查功能 不需要针对 Service 写一个接口.

## [#](http://doc.jetlinks.cn/dev-guide/specification.html#restful-%E6%8E%A5%E5%8F%A3%E5%91%BD%E5%90%8D) Restful 接口命名

URL使用小写,多个单词使用-或者/分割,如:device-info,logger/system.通常情况下应该使用URL来描述资源, 使用HTTP METHOD(GET 查询,POST 新增,PUT 修改,PATCH 修改不存在则新增,DELETE 删除)来描述对资源的操作. 在一些特殊操作无法使用HTTP METHOD来描述操作的时候,使用_开头加动词来描述,如: device/_query

```plain text
正确: GET /device-info/1
错误: GET /deviceInfo/1  GET /device_info/1

正确: GET /device/1
错误: GET /getDevice?id=1 ,  GET /getDevice/1

正确: GET /device/_query , POST /device/_query
错误: GET /queryDevice , POST /queryDevice
```

# [#](http://doc.jetlinks.cn/dev-guide/specification.html#%E5%93%8D%E5%BA%94%E5%BC%8F) 响应式

JetLinks 使用全响应式([reactor](https://projectreactor.io/))编程.

约定:

7. 所有可能涉及到IO或者异步操作(
网络请求
,
数据库操作
,
文件操作
)的方法,返回值全部为
Mono
或者
Flux
.
8. 所有代码不允许出现阻塞操作,如:
Thread.sleep
,
Mono.block
,
Flux.block
.
9. 响应式方法间调用,应该组装为同一个
Publisher
.
正确:
return deviceService .findById(id) .flatMap(device->this.syncDeviceState(device));
错误:
deviceService .findById(id) .subscribe(device->this.syncDeviceState(device).subscribe())
错误:
this.syncDeviceState(deviceService.findById(id).block()).subscribe();

相关资料:

10. [reactive-streams](http://www.reactive-streams.org/)
11. [project-reactor](https://projectreactor.io/)
12. [使用 Reactor 进行反应式编程](https://www.ibm.com/developerworks/cn/java/j-cn-with-reactor-response-encode/index.html?lnk=hmhm)
13. [simviso视频教程](https://space.bilibili.com/2494318)

%23%20%E5%91%BD%E5%90%8D%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fdev-guide%2Fspecification.html%23java%25E5%2591%25BD%25E5%2590%258D)%20java%E5%91%BD%E5%90%8D%0A%0A1.%20maven%E6%A8%A1%E5%9D%97%E5%90%8D%E5%B0%8F%E5%86%99%2C%E5%A4%9A%E4%B8%AA%E5%8D%95%E8%AF%8D%E4%BD%BF%E7%94%A8%60-%60%E8%BF%9E%E6%8E%A5%0A%20%20%20%20%0A%20%20%20%20%E6%AD%A3%E7%A1%AE%3A%20device-manager%20%E9%94%99%E8%AF%AF%3A%20deviceManager%0A%20%20%20%20%0A2.%20%E5%8C%85%E5%90%8D%E5%85%A8%E9%83%A8%E5%B0%8F%E5%86%99%2C%E5%A4%9A%E4%B8%AA%E5%8D%95%E8%AF%8D%E4%BD%BF%E7%94%A8%E5%A4%9A%E4%B8%AA%E7%9B%AE%E5%BD%95%E5%B1%82%E7%BA%A7.%0A%20%20%20%20%0A%20%20%20%20%E6%AD%A3%E7%A1%AE%3A%20org.jetlinks.pro.device.instance%20%E9%94%99%E8%AF%AF%3A%20org.jetlinks.pro.deviceInstance%0A%20%20%20%20%0A3.%20%E7%B1%BB%E5%90%8D%E9%A6%96%E5%AD%97%E6%AF%8D%E5%A4%A7%E5%86%99%2C%E4%BD%BF%E7%94%A8%E9%A9%BC%E5%B3%B0%E5%91%BD%E5%90%8D.%0A%20%20%20%20%0A%20%20%20%20%E6%AD%A3%E7%A1%AE%3A%20DeviceInstance%20%E9%94%99%E8%AF%AF%3A%20Deviceinstance%20%2C%20Device%5C_Instance%0A%20%20%20%20%0A4.%20%E6%96%B9%E6%B3%95%E5%90%8D%E9%A6%96%E5%AD%97%E6%AF%8D%E5%B0%8F%E5%86%99%2C%E4%BD%BF%E7%94%A8%E9%A9%BC%E5%B3%B0%E5%91%BD%E5%90%8D.%20%E5%90%8D%E7%A7%B0%E8%A6%81%E8%A7%81%E5%90%8D%E7%9F%A5%E4%B9%89.%0A%20%20%20%20%0A%20%20%20%20%E6%AD%A3%E7%A1%AE%3A%20findById(String%20id)%2C%20deployDeviceInstance(List%3CString%3EdeviceInstanceIdList)%20%E9%94%99%E8%AF%AF%3A%20getData(String%20arg)%0A%20%20%20%20%0A5.%20%E5%B1%80%E9%83%A8%E5%8F%98%E9%87%8F%E9%A6%96%E5%AD%97%E6%AF%8D%E5%B0%8F%E5%86%99%2C%E4%BD%BF%E7%94%A8%E9%A9%BC%E5%B3%B0%E5%91%BD%E5%90%8D.%20%E5%90%8D%E7%A7%B0%E8%A6%81%E8%A7%81%E5%90%8D%E7%9F%A5%E4%B9%89.%0A%20%20%20%20%0A%20%20%20%20%E6%AD%A3%E7%A1%AE%3A%20String%20deviceId%20%3D%20device.getId()%3B%20%E9%94%99%E8%AF%AF%3A%20String%20str%20%3D%20device.getId()%3B%0A%20%20%20%20%0A6.%20%E5%B8%B8%E9%87%8F%E4%BD%BF%E7%94%A8%E5%A4%A7%E5%86%99%2C%E5%A4%9A%E4%B8%AA%E5%8D%95%E8%AF%8D%E4%BD%BF%E7%94%A8%60_%60%E5%88%86%E5%89%B2.%0A%20%20%20%20%0A%20%20%20%20%E6%AD%A3%E7%A1%AE%3A%20static%20String%20DEFAULT%5C_CONFIG%20%3D%20%221%22%3B%20%E9%94%99%E8%AF%AF%3A%20static%20String%20DEFAULTCONFIG%20%3D%20%221%22%3B%0A%20%20%20%20%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fdev-guide%2Fspecification.html%23java-%25E6%258E%25A5%25E5%258F%25A3)%20java%20%E6%8E%A5%E5%8F%A3%0A%0A%E4%B8%80%E4%B8%AA%E6%A8%A1%E5%9D%97%E5%9C%A8%E9%9C%80%E8%A6%81%E6%8F%90%E4%BE%9B%E7%BB%99%E5%85%B6%E4%BB%96%E6%A8%A1%E5%9D%97%E4%BD%BF%E7%94%A8%E6%97%B6%2C%E5%BA%94%E8%AF%A5%E9%9D%A2%E5%90%91%E6%8E%A5%E5%8F%A3%E7%BC%96%E7%A8%8B%2C%E5%AF%B9%E5%A4%96%E6%8F%90%E4%BE%9B%E7%9B%B8%E5%BA%94%E7%9A%84%E6%8E%A5%E5%8F%A3.%E5%B9%B6%E5%9C%A8%E5%BD%93%E5%89%8D%E6%A8%A1%E5%9D%97%E6%8F%90%E4%BE%9B%E9%BB%98%E8%AE%A4%E7%9A%84%E5%AE%9E%E7%8E%B0.%0A%0A%E5%BD%93%E4%B8%80%E4%B8%AA%E6%A8%A1%E5%9D%97%E6%98%AF%E5%85%B7%E4%BD%93%E7%9A%84%E4%B8%9A%E5%8A%A1%E5%8A%9F%E8%83%BD%E5%AE%9E%E7%8E%B0%E6%97%B6%2C%E5%A4%A7%E9%83%A8%E5%88%86%E6%83%85%E5%86%B5%E4%B8%8D%E9%9C%80%E8%A6%81%E5%86%99%E6%8E%A5%E5%8F%A3%2C%E5%A6%82%E4%B8%80%E4%B8%AA%E5%A2%9E%E5%88%A0%E6%94%B9%E6%9F%A5%E5%8A%9F%E8%83%BD%20%E4%B8%8D%E9%9C%80%E8%A6%81%E9%92%88%E5%AF%B9%20%60Service%60%20%E5%86%99%E4%B8%80%E4%B8%AA%E6%8E%A5%E5%8F%A3.%0A%0A%23%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fdev-guide%2Fspecification.html%23restful-%25E6%258E%25A5%25E5%258F%25A3%25E5%2591%25BD%25E5%2590%258D)%20Restful%20%E6%8E%A5%E5%8F%A3%E5%91%BD%E5%90%8D%0A%0AURL%E4%BD%BF%E7%94%A8%E5%B0%8F%E5%86%99%2C%E5%A4%9A%E4%B8%AA%E5%8D%95%E8%AF%8D%E4%BD%BF%E7%94%A8%60-%60%E6%88%96%E8%80%85%60%2F%60%E5%88%86%E5%89%B2%2C%E5%A6%82%3A%60device-info%60%2C%60logger%2Fsystem%60.%E9%80%9A%E5%B8%B8%E6%83%85%E5%86%B5%E4%B8%8B%E5%BA%94%E8%AF%A5%E4%BD%BF%E7%94%A8URL%E6%9D%A5%E6%8F%8F%E8%BF%B0%E8%B5%84%E6%BA%90%2C%20%E4%BD%BF%E7%94%A8HTTP%20METHOD(%60GET%20%E6%9F%A5%E8%AF%A2%60%2C%60POST%20%E6%96%B0%E5%A2%9E%60%2C%60PUT%20%E4%BF%AE%E6%94%B9%60%2C%60PATCH%20%E4%BF%AE%E6%94%B9%E4%B8%8D%E5%AD%98%E5%9C%A8%E5%88%99%E6%96%B0%E5%A2%9E%60%2C%60DELETE%20%E5%88%A0%E9%99%A4%60)%E6%9D%A5%E6%8F%8F%E8%BF%B0%E5%AF%B9%E8%B5%84%E6%BA%90%E7%9A%84%E6%93%8D%E4%BD%9C.%20%E5%9C%A8%E4%B8%80%E4%BA%9B%E7%89%B9%E6%AE%8A%E6%93%8D%E4%BD%9C%E6%97%A0%E6%B3%95%E4%BD%BF%E7%94%A8%60HTTP%20METHOD%60%E6%9D%A5%E6%8F%8F%E8%BF%B0%E6%93%8D%E4%BD%9C%E7%9A%84%E6%97%B6%E5%80%99%2C%E4%BD%BF%E7%94%A8%60_%60%E5%BC%80%E5%A4%B4%E5%8A%A0%E5%8A%A8%E8%AF%8D%E6%9D%A5%E6%8F%8F%E8%BF%B0%2C%E5%A6%82%3A%20device%2F%5C_query%0A%0A%60%60%60tex%0A%E6%AD%A3%E7%A1%AE%3A%20GET%20%2Fdevice-info%2F1%0A%E9%94%99%E8%AF%AF%3A%20GET%20%2FdeviceInfo%2F1%20%20GET%20%2Fdevice_info%2F1%0A%0A%E6%AD%A3%E7%A1%AE%3A%20GET%20%2Fdevice%2F1%0A%E9%94%99%E8%AF%AF%3A%20GET%20%2FgetDevice%3Fid%3D1%20%2C%20%20GET%20%2FgetDevice%2F1%0A%0A%E6%AD%A3%E7%A1%AE%3A%20GET%20%2Fdevice%2F_query%20%2C%20POST%20%2Fdevice%2F_query%0A%E9%94%99%E8%AF%AF%3A%20GET%20%2FqueryDevice%20%2C%20POST%20%2FqueryDevice%0A%60%60%60%0A%0A%23%20%5B%23%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fdev-guide%2Fspecification.html%23%25E5%2593%258D%25E5%25BA%2594%25E5%25BC%258F)%20%E5%93%8D%E5%BA%94%E5%BC%8F%0A%0AJetLinks%20%E4%BD%BF%E7%94%A8%E5%85%A8%E5%93%8D%E5%BA%94%E5%BC%8F(%5Breactor%5D(https%3A%2F%2Fprojectreactor.io%2F))%E7%BC%96%E7%A8%8B.%0A%0A%E7%BA%A6%E5%AE%9A%3A%0A%0A1.%20%E6%89%80%E6%9C%89%E5%8F%AF%E8%83%BD%E6%B6%89%E5%8F%8A%E5%88%B0IO%E6%88%96%E8%80%85%E5%BC%82%E6%AD%A5%E6%93%8D%E4%BD%9C(%60%E7%BD%91%E7%BB%9C%E8%AF%B7%E6%B1%82%60%2C%60%E6%95%B0%E6%8D%AE%E5%BA%93%E6%93%8D%E4%BD%9C%60%2C%60%E6%96%87%E4%BB%B6%E6%93%8D%E4%BD%9C%60)%E7%9A%84%E6%96%B9%E6%B3%95%2C%E8%BF%94%E5%9B%9E%E5%80%BC%E5%85%A8%E9%83%A8%E4%B8%BA%60Mono%60%E6%88%96%E8%80%85%60Flux%60.%0A%20%20%20%20%0A2.%20%E6%89%80%E6%9C%89%E4%BB%A3%E7%A0%81%E4%B8%8D%E5%85%81%E8%AE%B8%E5%87%BA%E7%8E%B0%E9%98%BB%E5%A1%9E%E6%93%8D%E4%BD%9C%2C%E5%A6%82%3A%20%60Thread.sleep%60%2C%60Mono.block%60%2C%60Flux.block%60.%0A%20%20%20%20%0A3.%20%E5%93%8D%E5%BA%94%E5%BC%8F%E6%96%B9%E6%B3%95%E9%97%B4%E8%B0%83%E7%94%A8%2C%E5%BA%94%E8%AF%A5%E7%BB%84%E8%A3%85%E4%B8%BA%E5%90%8C%E4%B8%80%E4%B8%AA%60Publisher%60.%0A%20%20%20%20%0A%20%20%20%20%E6%AD%A3%E7%A1%AE%3A%20%60return%20deviceService%20.findById(id)%20.flatMap(device-%3Ethis.syncDeviceState(device))%3B%60%0A%20%20%20%20%0A%20%20%20%20%E9%94%99%E8%AF%AF%3A%20%60deviceService%20.findById(id)%20.subscribe(device-%3Ethis.syncDeviceState(device).subscribe())%60%0A%20%20%20%20%0A%20%20%20%20%E9%94%99%E8%AF%AF%3A%20%60this.syncDeviceState(deviceService.findById(id).block()).subscribe()%3B%60%0A%20%20%20%20%0A%0A%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99%3A%0A%0A1.%20%5Breactive-streams%5D(http%3A%2F%2Fwww.reactive-streams.org%2F)%0A2.%20%5Bproject-reactor%5D(https%3A%2F%2Fprojectreactor.io%2F)%0A3.%20%5B%E4%BD%BF%E7%94%A8%20Reactor%20%E8%BF%9B%E8%A1%8C%E5%8F%8D%E5%BA%94%E5%BC%8F%E7%BC%96%E7%A8%8B%5D(https%3A%2F%2Fwww.ibm.com%2Fdeveloperworks%2Fcn%2Fjava%2Fj-cn-with-reactor-response-encode%2Findex.html%3Flnk%3Dhmhm)%0A4.%20%5Bsimviso%E8%A7%86%E9%A2%91%E6%95%99%E7%A8%8B%5D(https%3A%2F%2Fspace.bilibili.com%2F2494318)