---
layout: post
title: ThingsBoard入门实战（六）：设备列表和带状态跳转
slug: thingsboard-device-list-and-status-jump
type:
  - note
date: 2023-07-17
status: draft
tags:
  - ThingsBoard
categories:
  - IoT
  - ThingsBoard
mood:
weather:
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

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038812777-348dc525-8b23-488b-9b0c-8e9a1fc816e1.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038812881-ab210fc8-c451-47ba-a3a0-991d057992fe.jpg)

进入编辑模式，选择**Entity admin widgets**实体管理部件库

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038812997-1b735805-7a81-41cf-a367-699fccc7ba1d.jpg)

选择**Device admin table**设备管理部件：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813101-3b7a4a6f-f17e-4bee-bb03-b08528238c76.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813207-1b17827b-0f7e-444c-8699-d45f1fe42f13.jpg)

可见需要一个别名

### 别名

添加别名，注意筛选器类型要是设备类型：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813309-78edd2e5-1520-4552-b51d-b1af6670cef6.jpg)

设备类型选路灯：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813414-e34e8731-a320-4611-aa6c-affcc44e64ad.jpg)

选好要导入的遥测值：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813519-a41adaaf-4623-47a9-a7c8-5b8dc1d2a5c7.jpg)

点击添加，大功告成：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813626-7469b7fb-3b81-4864-b988-05a7142c826b.jpg)

仔细看看，增删改一应俱全，简直比低代码还低代码！

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813739-ce475b98-5e87-41e6-8269-53e5f408260e.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813840-92a763b1-7fed-4795-ae4d-44eff8f684ae.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038813949-33b38570-d44c-4d3c-ac1b-52b9a40bc681.jpg)

看起来不错，不过我觉得跳转我们自己的详情页会更美丽。

### 列表Action到详情

进入部件编辑模式，选择Action这个Tab，可以发现刚我们看到的增删改三大操作都是在这定义的，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814058-e379c994-f965-405f-8200-6cd8232b6aa0.jpg)

我们在这里定义一个新的按钮，它可以有四个位置，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814164-0a1b8d11-82bf-4bc0-8e20-9370b8841970.jpg)

对应到列表页面：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814274-a56ddcee-76a0-4702-8567-b1dab31e60a9.jpg)

我们需要跳转详情，自然是在单元格之内比较直观

设置一下

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814376-45e9b38e-b786-4bc6-bf45-aa296b13ea69.jpg)

注意这两层都需要保存

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814485-7b00f2e3-e294-4e94-b097-1ca1e4a93d9f.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814604-79dcd0b1-c34e-467b-af7d-aef8ba093328.jpg)

点击查看详情

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814708-0f935230-2a88-4c8f-b5f1-8c9cfe120f81.jpg)

看起来不错的样子，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814818-3db2b75c-dcaf-4d3a-93ac-31e4688b9a9a.jpg)

可是，数据对么？

记得我们详情里选的别名是 路灯1，现在有两个路灯了，路灯2也得有姓名，我们得让别名随着设备走。

## 三、设备详情升级

### 设备详情的别名修改

进入 路灯详情 仪表板的 编辑模式，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038814954-669addb2-ad97-4924-9779-e215b4e6e5c6.jpg)

点击别名图标

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815079-b794bbd0-e32a-4394-9c2e-cf62afc30d37.jpg)

现在别名叫路灯1已经不合适了，我们叫它单路灯, 最重要的是，要把筛选器改成仪表板实体状态，这样他就能获取跳转之前这个实体的状态了。

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815182-43a966ad-3d8d-4ea2-8ad3-100722f4bf75.jpg)

切记，每次修改一定要记得保存！

现在用路灯2验证一下：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815287-e0e69726-5a27-4460-af60-2929469abc5a.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815389-ff3730cb-9ab2-475e-9b66-c392c338ccee.jpg)

跳转成功！

再来点小优化，我们怎么跳回列表呢？用Action！

### 跳回列表

进入 路灯详情 仪表板的 编辑模式，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815493-36420dfd-a817-4041-92ad-d57a12131ab5.jpg)

点击地图面板的编辑图标：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815620-f80e4e3d-195d-4276-9519-fb316dbd1e6f.jpg)

给地图新增一个Action：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815739-56356888-04a6-4e40-b5a7-e9ba0f5f8371.jpg)

保存，然后发现 路灯详情 仪表板 右上角 多了个跳转的图标：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038815904-7a8f518c-bd82-43e4-a846-c129a4fc8ccf.jpg)

点击直接跳到列表，完美！

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038816049-f6dde350-d808-463a-98a2-1b492903f1ea.jpg)

## 四、下一步

通过这节的练习，我们几乎只用配置就实现了一个基于路灯的管理模块，下一节我们把它修改完善一下，然后发布出去。