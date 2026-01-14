---
layout: post
title: 死磕 Spring4 张图带你读懂 Spring IoC 的世界
slug: dead-dive-spring4-understand-spring-ioc-with-this-picture
type:
  - note
date: 2020-04-07
status: draft
tags:
  - Spring 源码解析
mood:
weather:
author: deathwhispers
created: 2020-04-07 09:00
updated: 2020-04-07 18:00
---
# 1. Bean 的转换过程

下面这张图演示了一个可用的 bean 是如何从 xml 配置文件中演变过来的。

![365d4142eb23822dcaddba6d1f59ccbc](/assets/images/learning/spring/springsourcecode/dead-dive-spring4-understand-spring-ioc-with-this-picture/365d4142eb23822dcaddba6d1f59ccbc.jpeg)

# 2. ApplicationContext 的架构图

![dde0bf4ae9014ec73c80f4c45045850a](/assets/images/learning/spring/springsourcecode/dead-dive-spring4-understand-spring-ioc-with-this-picture/dde0bf4ae9014ec73c80f4c45045850a.jpeg)

# 3. load BeanDefinition 的全流程

![38419d23d29c83a4758f73f85281e076](/assets/images/learning/spring/springsourcecode/dead-dive-spring4-understand-spring-ioc-with-this-picture/38419d23d29c83a4758f73f85281e076.png)

# 4. get Bean 的全流程

![3a5b28a2d3bd435ca94ea5c8752609d5](/assets/images/learning/spring/springsourcecode/dead-dive-spring4-understand-spring-ioc-with-this-picture/3a5b28a2d3bd435ca94ea5c8752609d5.png)