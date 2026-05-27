---
layout: post
title: ThingsBoard入门实战（五）：设备详情面板
slug: thingsboard-device-details-panel
type:
- note
date: 2023-07-15
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

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/2ececd8246552380293909c0d9b134c4.jpg)

ThingsBoard提供的地图控件比较丰富，我们先选个鹅厂的腾讯地图：

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/f4e1d5f7894b4c0a556aea2cc919e35d.jpg)

选择实体做数据源：

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/cc05a0589f62e8756d6d4d863896002f.jpg)

好了，看看图？

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/c9e7f93e103fff5ede60e22ff3b0c80b.jpg)

### 修改Marker图标

这个**路灯**几乎看不见啊，亲先别差评，看我来改一改，加上个Marker图标：

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/7b027914b72264a5780314bee7e8c936.png)

现在看一看，

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/dd8f0aa15f4f71f106aac6b4292907c3.jpg)

不好看没关系，我们可以换自己的图：

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/527228bd94a3a68cf563694cd7004ef0.jpg)

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/69ca3b5800dd79fcc4417c1fb825b491.jpg)

找图标，认准 [iconfont 阿里巴巴矢量图标库](https://www.iconfont.cn/)

### 修改弹框

既然有了Marker，少不得要点一下，等等这个是啥？

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/6c33381785fbc8a274d000d3b5419cf2.jpg)

进入修改模式，看看设置，

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/f16e1e4d00949029232ed59374289b50.jpg)

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

![](/assets/images/iot/thingsboard/thingsboard-device-details-panel/9e6ec5a76b41590c0e7630c211894772.jpg)
