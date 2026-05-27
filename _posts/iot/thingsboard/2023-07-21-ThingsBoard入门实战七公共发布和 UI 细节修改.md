---
layout: post
title: ThingsBoard入门实战（七）：公共发布和 UI 细节修改
slug: thingsboard-common-publishing-ui-details-modification
type:
- note
date: 2023-07-21
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
created: 2023-06-08 11:45
updated: 2023-06-08 18:33
---

# ThingsBoard入门实战（七）：公共发布和 UI 细节修改

# 7.细节修改和公共发布

GET到新技能了，想给兄弟们演示，需要给他们每个人一个账号么？ 答案肯定是：**不需要！** ThingsBoard 用 **公共发布** 解决了这个问题。

## 一、公共发布

首先我们来看一下路灯设备现在在谁名下？

如下图，路灯都是customerA的，

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/97386415c034d0a872e07d7830b22bb7.jpg)

目前只有它和它的租户可以看到，其他人需要看就需要设为公有。

如图操作：

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/1717e11fe5175cd24984b9f32bce5094.jpg)

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/c43bd35c85a8e7e5c30d1cb4385de5fc.jpg)

对于设备详情[仪表盘](https://so.csdn.net/so/search?q=%E4%BB%AA%E8%A1%A8%E7%9B%98&spm=1001.2101.3001.7020)，我们也需要设为公有，这样他们才能自由跳转。 这时候是看不到界面的，我们需要设置公共用户的设备：

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/c27e92125b05bca757fc7d9be30ba283.jpg)

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/621a08ecf34ffb6bfabf7dd8b1b4627b.jpg)

搞定，现在路灯已经被公开了。

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/3b09d20dc6aafa151e7fe2295041e2d2.jpg)

复制仪表板的公有链接看一看：

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/0accad2ff4cb29ea048c3657f084e097.jpg)

![](/assets/images/iot/thingsboard/thingsboard-common-publishing-ui-details-modification/17dba0e95cee5bb22a8430ae50d1dd25.jpg)

不想公开了?

也简单，撤销公开就好，点一下按钮的事。

## 二、UI优化

在一些特殊情况下，需要去掉一些系统默认的标识， 下图中有三点看起来比较碍眼~

- 网页icon
- 网页标题
- 右下角标志

由于需要修改一点代码，这也可以算作简单的二次开发。 要二开，首先得下载源码~

### 下载

查看项目[https://github.com/thingsboard/thingsboard](https://github.com/thingsboard/thingsboard)

Git下载

复制地址

git@github.com:thingsboard/thingsboard.git

打开命令行下载

git clone git@github.com:thingsboard/thingsboard.git

单独复制ui-ngx文件夹

cp -r thingsboard/ui-ngx thingsboard-ui-ngx

### 运行

需要安装nodejs和yarn

下载依赖包

yarn

本地启动：

yarn start

**注意**： 由于前端默认的后端是localhost, 先改下地址

项目下找到文件proxy.conf.js

const forwardUrl = “http://IP:9090/”; const wsForwardUrl = “ws://IP:9090”; // const forwardUrl = “http://localhost:8080”; // const wsForwardUrl = “ws://localhost:8080”;

### 修改

1. logo

logo的文件地址是 src/assets/logo_title_white.svg

可以自己画一个 https://c.runoob.com/more/svgeditor/

2. icon

icon的文件地址是src/thingsboard.ico

3. title

title的文件地址是src/index.html 找到：

替换为：

找到源码目录src.ts和environment.prod.ts文件

修改appTitle = “主题名称”

修改defaultLang = “默认语言”

修改后效果如下：

export const environment = { appTitle: “主题名称”, production: false, // @ts-ignore tbVersion: TB_VERSION, // @ts-ignore supportedLangs: SUPPORTED_LANGS, defaultLang: “主题名称” };

4. powered by

找到 src/app/modules/home/components/dashboard-page/dashboard-page.component.html

直接删除有 power by的那行就可以了。

5. 修改程序主题颜色

找到源码src.scss文件:

修改$tb-primary-color: 主题颜色

修改$tb-secondary-color: 主题颜色

修改$tb-hue3-color: 主题颜色

可以参考目前国内流行的配色比如 [ElementUI](https://element-plus.gitee.io/zh-CN/component/color.html)。

6. 注释页面“帮助问号？”

找到文件：src.component.htmls

注释有问号的button源码

经过修改，UI界面已经基本符合我们的要求。

## 三、下一步还可以做什么？

现在我已经有了一个定制化的物联网平台。 下一步，我们还可以做什么？

### 更好的UI

现在要接甲方的项目, 界面这一块儿还是需要多下功夫，毕竟是整个系统的门面。想要更魔幻的界面UI，有两条路：

7. 基于ThingBoard部件库魔改 基本的思路是依然使用ThingBoard本身的可视化系统，通过修改ThingBoard部件库来达成该界面的优化。
8. 使用三方UI库对接ThingsBoard 如果已经有第三方的UI大屏，只需要数据对接ThingBoard就可以h把设备数据传到你的大屏上，同时还能实现设备遥测数据的实时更新。

### 更丰富的系统模块

9. 设备接入 除了三种默认的数据传输协议 HTTP / MQTT / COAP ，ThingBoard 官方还提供了对其他数据协议的支持，也就是网关项目。
10. 仪表盘 ThingBoard 仪表盘的功能非常强大，我们甚至可以基于仪表盘开发完整的基于物联网的应用系统。
11. 规则引擎 ThingBoard 内置规则引擎，可以接收设备的信息，还可以通过自定义的规则实现处理和转发。设备透传、设备关联控制也是小菜一碟。规则引擎是Thingsboard高级开发绕不开的话题。
