---
layout: post
title: Master-Worker模式
slug: master-worker-pattern
type:
- note
date: 2021-04-11
week: 2021-W19
status: draft
tags:
- SystemDesign
author: deathwhispers
created: 2021-04-11 10:00
updated: 2021-04-11 10:00
categories:
- Learning
- SystemDesign
---

# Master-Worker模式

Master-Worker模式是常用的并行计算模式。

它的核心思想是系统由两类进程协作工作：Master进程和Worker进程。

Master进程负责接收和分配任务，Worker负责处理子任务。当各个Worker子进程处理完成后，会将结果返回给Master，由Master做归纳和总结。

其好处是能将一个大任务分解若干个小任务，并行执行，从而提高系统的吞吐量。

![](/assets/images/learning/sysdesign/master-worker-pattern/8723ac595edd1de7f232714af5322c03.png)

![](/assets/images/learning/sysdesign/master-worker-pattern/3b75d5ccc0c986fa369ba0c336d0af95.png)

示例demo：

![](/assets/images/learning/sysdesign/master-worker-pattern/bfc6d86460a47bd884309f946e43b8a1.png)

![](/assets/images/learning/sysdesign/master-worker-pattern/96c943d8396680e58ecf045e0ff4f9bb.png)

![](/assets/images/learning/sysdesign/master-worker-pattern/94575b7e77416252fef7b38d96ecf109.png)

![](/assets/images/learning/sysdesign/master-worker-pattern/2659e06494105036934a43df867a8684.png)

![](/assets/images/learning/sysdesign/master-worker-pattern/339a6c06fc99df547cb4c902ab73d1ef.png)
