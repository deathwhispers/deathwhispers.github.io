---
layout: post
title: 关于Mac使用IDEA的设置和小tip
slug: mac-idea-setup-tips
type:
- note
status: published
date: 2022-08-27
tags:
- Tooling
author: deathwhispers
categories:
- Other
- General
---

## 操作环境

- 电脑：MacBook Pro M1 Pro 16GB
- macOS：Sequoia 15.4
- IDE：IntelliJ IDEA 2024.2.4(Ultimate Edition)

## 通用设置

### 主题&字体设置

Setting - Appearance & Behavior - Appearance

- 主题：Atom One Dark
- 字体：Andale Mono

这里的字体主要是整个页面的字体 不包括编辑区域内代码中的字体

- 字体大小：12

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ad54c5a2e43b4ebea071ea6c5e859b2e~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

## 编辑区域设置

### 自动导包设置

Setting - Editor - General - Auto Import

这里主要对于导入项目后的自动导包设置

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/012b9334e12942038748941a23c5639a~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

### 字体设置

Setting - Editor - Font

这里主要对于编辑区域内 (代码区域) 字体进行设置

- 字体：Andale Mono
- 大小：13
- 行高：2

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/da14765c743e48319d2b947700dcd4e0~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

### 主题设置

- 主题样式：Atom One Dark

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ee97dfa018454506bc338cc40082d5b8~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

### 新建文件模版设置

- 模版设置目的：新建文件时 自动填充作者、文件描述、创建日期注释
若需新增其余可按照官方描述进行添加即可
```perl
/**
 @author: bobochang
 @description:
 @date: ${DATE} ${TIME}
*/
```
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3c243ea73f1a452488832f64008e043a~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

### 快捷键模版设置

- 自定义快捷键模板：该功能主要用于自定义快捷键输出自定义的代码，如 psvm

```java
public static void main(String[] args){
 $END$
}
```

- 自定义关于日志输出的快捷键模版：
    1. 点击右上方 ➕ 选择第二点 创建新的模板组 并从弹出框中为新的模板组命名
    2. 选择新创建好的模板组 继续点击右上方 ➕ 选择第一天 创建新的模板
    3. 选择新创建好的模板 在 **Abbreviation** 输入框中填入触发该自定义模板的快捷键
    4. 在 **Template text** 文本框中输入模板内容
    5. 最后在左下方 **Change** 选择框中勾选可触发该模板的语言类型
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f5607234340645ef935db6f647488a67~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)
其中：关于模版文本框中的变量名和对应值可以到 **Edit variables** 自行添加和修改

### 隐藏文件设置

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/93b60e321ef74a6b8f935db6d08c9fae~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

## 构建&执行&部署环境设置

### 构建工具设置

Setting - Build,Execution,Deployment - Build Tools - Maven

这里主要Maven工具进行环境设置

- 选择本机对应的Maven文件夹 以及 对应的配置文件 和 本地仓库位置

选择完本机对应Maven文件夹后 加载出对应Maven版本则表示选择正确并加载完成

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/373ce3caa6a34a8db775a3a9b0b66bb7~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

## 插件设置

这边主要分享几款个人觉得比较好用 也一直在使用的插件分享

### 图标插件设置

Setting - Plugins - Marketplace

进入插件市场后搜索关键字 Atom Material Icons

这款插件作用主要是美化系统自带的大部分图标 也是为枯燥的代码生化加点颜色

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/16019154e31b4ac2bb344b78f260aa48~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

### 主题插件设置

Setting - Plugins - Marketplace

进入插件市场后搜索关键字 Atom OneDark Theme

这款主题插件是夜间主题插件 配合上面的图标插件使用个人还是挺喜欢的 效果也如上图

### MyBatis增强插件设置

Setting - Plugins - Marketplace

进入插件市场后搜索关键字 MyBatisX

关于MyBatisX这款插件的优秀之处相信也不用我多介绍了 安装时 其作者也进行了介绍

我最喜欢这款插件的一点就是可以快速的按照数据库中的表 创建对应的基础mapper和xml文件

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c92d092e3eae49c5aa81544f66a998e3~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

### 彩虹括号插件设置

Setting - Plugins - Marketplace

进入插件市场后搜索关键字 Rainbow Brackets

这款插件主要作用是让我们每一个括号都颜色对应起来

个人觉得有了颜色的照应 找出对应所包括的内容就简单许多了

## 写在最后

这一次的分享可能做得不到位 也希望各位体谅 如果有其他更好的设置也可以一起交流分享

最后我还整理出了一份使用比较频繁的 java springboot [后台开发通用模板](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fbobochangzzz%2FSpringBoot-Init)

可以在此基础上快速开发新项目
