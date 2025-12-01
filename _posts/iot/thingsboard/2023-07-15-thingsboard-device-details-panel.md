---
layout: post
title: ThingsBoard入门实战（五）：设备详情面板
slug: thingsboard-device-details-panel
type:
  - note
date: 2023-07-15
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


# ThingsBoard入门实战（五）：设备详情面板

# 设备面板:详情

一个炫酷的详情页怎么能少得了地图呢？ Thingsboard很贴心的为我们内置了地图的部件库。

## 一、地图

地图显示的核心是位置信息，也就是我们常听到的坐标，

**坐标系**是坐标产生的参考背景，常见坐标系如下：

- GCJ-02 高德地图、腾讯地图以及谷歌中国区地图使用的是GCJ-02坐标系
- BD-09 百度地图使用的是BD-09坐标系
- WGS-84 底层接口 (HTML5 Geolocation或ios、安卓API)通过GPS设备获取的坐标使用的是WGS-84坐标系

**坐标**是在坐标系上的位置点，一般用经纬度表示：

- longitude 经度
- latitude 纬度

可以搜索经纬度查询定位查询地址的经纬度。

## 二、地图部件

### 添加部件

像往常一样，我们先找到地图部件包：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038810131-fd323480-fb0d-4c94-aaef-2f637fcfecf1.jpg)

ThingsBoard提供的地图控件比较丰富，我们先选个鹅厂的腾讯地图：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038810257-ca54fa96-7934-417c-bfdd-74e251126b3c.jpg)

选择实体做数据源：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038810391-ef0c297d-3d8b-4980-a890-4c07b4c6a270.jpg)

好了，看看图？

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038810507-2533a523-24fa-470d-a5da-a2d0e461c567.jpg)

### 修改Marker图标

这个**路灯**几乎看不见啊，亲先别差评，看我来改一改，加上个Marker图标：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038810640-e30164ca-b973-4b78-bbbe-34f9750ac4fb.png)

现在看一看，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038810774-44ff16d3-35c8-43ab-a74f-a1603382cd18.jpg)

不好看没关系，我们可以换自己的图：

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038810898-9d316760-f021-4484-ae68-9be8450f8f9a.jpg)

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038811068-00c6d7ed-810f-44f5-9318-f0e9ad43d4f6.jpg)

找图标，认准 [iconfont 阿里巴巴矢量图标库](https://www.iconfont.cn/)

### 修改弹框

既然有了Marker，少不得要点一下，等等这个是啥？

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038811188-a11dc2de-e952-4c6a-91d7-2a658915563d.jpg)

进入修改模式，看看设置，

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038811320-317b33c9-ad42-4ef3-9b04-b6b0bcd5a622.jpg)

发现代码

` <b>${entityName}</b><br /><br />     <b>Latitude:</b> ${latitude:7}<br />     <b>Longitude:</b> ${longitude:7}<br />     <b>Temperature:</b> ${temperature} °C<br />     <small>See advanced settings for details</small> </div></font>`
原来是默认设置，修改成：

` <b>${entityName}</b><br />     <b>纬度:</b> ${latitude:7}<br />     <b>经度:</b> ${longitude:7}<br />     <b>电量:</b> ${battery} %<br /> </div></font>`
如果样式还不符合你的审美，请Web前端修改就好。 只要前端用html/css/js可以实现的，在这里都可以通过自定义的方式做到，发挥想象力~
详情页当然不止这些内容，这里建议大家好好学习一下部件库，相信你很快就会有适合自己项目的炫酷详情页~**
三、下一步**
大家应该发现这个问题了：
一个设备我写一个详情页，10个设备写10个？这个不能通用么？
当然不是这样，ThingsBoard的操作太魔幻，下节课我们就直接放个大招解决这个问题~

![](https://cdn.nlark.com/yuque/0/2023/jpg/29230873/1698038811450-2f54ff20-a71b-418d-a0f4-23cf7ddd62db.jpg)