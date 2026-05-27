---
layout: post
title: ThingsBoard入门实战（六）：设备列表和带状态跳转
slug: thingsboard-device-list-and-status-jump
type:
- note
date: 2023-07-17
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
created: 2023-06-07 11:45
updated: 2023-06-07 18:33
---

# ThingsBoard入门实战（六）：设备列表和带状态跳转

# 设备列表和带状态跳转

**上节有提到，这节就是仪表盘甚至整个专题的精髓，信息量很大，请反复阅读体会。。理解透了，甚至可以用仪表盘开发基于设备的应用系统**

## 一、多个设备

为了实现设备的跳转，我们至少需要两个设备。 按照之前添加设备的方式添加 第二个设备路灯2。

## 二、列表部件

### 路灯列表

添加路灯列表

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/bbe83e507bdf2367bbd9bb319eba55d5.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/4de8da7de9c09931cc65d7d0286a6ed0.jpg)

进入编辑模式，选择**Entity admin widgets**实体管理部件库

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/08d19fae3673e2694edb8e83c06474cf.jpg)

选择**Device admin table**设备管理部件：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/d79244873167643d5cb487d041faa439.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/fb00cee5fa564e20ea50b278ae563e61.jpg)

可见需要一个别名

### 别名

添加别名，注意筛选器类型要是设备类型：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/20485740ea8b0fe774dca0d426e03747.jpg)

设备类型选路灯：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/21285a68d2e73010a5b4bc2ca174b6e0.jpg)

选好要导入的遥测值：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/93eb60139e2ad75ed1f9dd3dd3c9000a.jpg)

点击添加，大功告成：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/91a2f916961ca576043cee26fda18279.jpg)

仔细看看，增删改一应俱全，简直比低代码还低代码！

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/dac4a089b6c2f2815d754cc6ff61b32c.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/a9df827d8c24130dcf735b0add695c76.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/7f1fba39859be37a411103d3e86b28fe.jpg)

看起来不错，不过我觉得跳转我们自己的详情页会更美丽。

### 列表Action到详情

进入部件编辑模式，选择Action这个Tab，可以发现刚我们看到的增删改三大操作都是在这定义的，

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/a49914bffe63483125599e881b6f8e1b.jpg)

我们在这里定义一个新的按钮，它可以有四个位置，

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/ba8dcb37be26e8a458a54d5a6e84d0bc.jpg)

对应到列表页面：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/5db7dd3be54dcc25bc62ebefc31e1b89.jpg)

我们需要跳转详情，自然是在单元格之内比较直观

设置一下

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/15b04e2c53600f1337e09e84b6f57baa.jpg)

注意这两层都需要保存

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/1a142c1a53fa5688949c19a4e5cf1ca3.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/c77f080a78f720b02c1c2fe74fb4afc7.jpg)

点击查看详情

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/91c6e7809cdbb03010a0311537fd7671.jpg)

看起来不错的样子，

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/bbe49916988815e5a004d071705da216.jpg)

可是，数据对么？

记得我们详情里选的别名是 路灯1，现在有两个路灯了，路灯2也得有姓名，我们得让别名随着设备走。

## 三、设备详情升级

### 设备详情的别名修改

进入 路灯详情 仪表板的 编辑模式，

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/9973efb1ba80d1a5998892a38b6f5c87.jpg)

点击别名图标

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/50bff79c2ec001809c7a62d13d90363c.jpg)

现在别名叫路灯1已经不合适了，我们叫它单路灯, 最重要的是，要把筛选器改成仪表板实体状态，这样他就能获取跳转之前这个实体的状态了。

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/7932adff577d4a7e5b922d65b9d9296a.jpg)

切记，每次修改一定要记得保存！

现在用路灯2验证一下：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/8058b188328d6229c56b002a010670f5.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/9c3e464cfb1d094c0cb39f418597dc24.jpg)

跳转成功！

再来点小优化，我们怎么跳回列表呢？用Action！

### 跳回列表

进入 路灯详情 仪表板的 编辑模式，

![](assets/images/iot/thingsboard/2023-07-17-thingsboard-device-list-and-status-jump/9973efb1ba80d1a5998892a38b6f5c87.jpg)

点击地图面板的编辑图标：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/8f3bc277d5cc3545c0151af8068b6695.jpg)

给地图新增一个Action：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/5e8903e8e0f5311d27612a1ae7ca24e5.jpg)

保存，然后发现 路灯详情 仪表板 右上角 多了个跳转的图标：

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/50299180a1a205126e69fc1f4f12c04a.jpg)

点击直接跳到列表，完美！

![](/assets/images/iot/thingsboard/thingsboard-device-list-and-status-jump/f8b08581959bd2728bd7b0fba0735fea.jpg)

## 四、下一步

通过这节的练习，我们几乎只用配置就实现了一个基于路灯的管理模块，下一节我们把它修改完善一下，然后发布出去。
