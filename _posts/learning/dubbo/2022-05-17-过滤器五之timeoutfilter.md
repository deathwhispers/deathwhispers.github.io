---
layout: post
title: 过滤器（五）之TimeoutFilter
author: deathwhispers
date: 2022-05-17
slug: dubbo-filter-timeout
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-17 11:52
updated: 2022-05-17 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享过滤器 TimeoutFilter ，用于服务**提供者**中。

# 2. TimeoutFilter

com.alibaba.dubbo.rpc.filter.TimeoutFilter ，实现 Filter 接口，超时过滤器。如果服务调用**超时**，记录**告警**日志，**不干涉**服务的运行。代码如下：

```plain text
plain 1: @Activate(group = Constants.PROVIDER)  2: public class TimeoutFilter implements Filter {  3:   4:     private static final Logger logger = LoggerFactory.getLogger(TimeoutFilter.class);  5:   6:     @Override  7:     public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {  8:         long start = System.currentTimeMillis();  9:         // 服务调用 10:         Result result = invoker.invoke(invocation); 11:         // 计算调用时长 12:         long elapsed = System.currentTimeMillis() - start; 13:         // 超过时长，打印告警日志 14:         if (invoker.getUrl() != null 15:                 && elapsed > invoker.getUrl().getMethodParameter(invocation.getMethodName(), "timeout", Integer.MAX_VALUE)) { 16:             if (logger.isWarnEnabled()) { 17:                 logger.warn("invoke time out. method: " + invocation.getMethodName() 18:                         + " arguments: " + Arrays.toString(invocation.getArguments()) + " , url is " 19:                         + invoker.getUrl() + ", invoke elapsed " + elapsed + " ms."); 20:             } 21:         } 22:         return result; 23:     } 24:  25: }
```

---

- 第 10 行：调用
Invoker#invoke(invocation)
方法，服务调用。
- 第 12 行：计算调用时长。
- 第 13 至 21 行：超过时长，打印**告警提供者消费者**
日志。注意，此处的
"timeout"
取得的是服务
的配置，不同于服务
的配置。
- 第 22 行：返回调用结果。
- 再注意，在服务**提供者超过了超时时间消费者**
，执行服务调用时，即使
，也不会取消执行。虽然，服务
，已经结束调用，返回调用超时。
