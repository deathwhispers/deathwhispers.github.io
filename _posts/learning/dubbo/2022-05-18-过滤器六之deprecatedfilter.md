---
layout: post
title: 过滤器（六）之DeprecatedFilter
author: deathwhispers
date: 2022-05-18
slug: dubbo-filter-deprecated
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-18 11:52
updated: 2022-05-18 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享过滤器 DeprecatedFilter ，用于服务**消费者**中，通过 <dubbo: service /> 或  或  的 "deprecated" 配置项为 true 来开启。

# 2. DeprecatedFilter

com.alibaba.dubbo.rpc.filter.DeprecatedFilter ，实现 Filter 接口，废弃调用的过滤器实现类。当调用废弃的服务方法时，打印错误日志提醒。代码如下：

```java
@Activate(group = Constants.CONSUMER, value = Constants.DEPRECATED_KEY)
public class DeprecatedFilter implements Filter {

    private static final Logger LOGGER = LoggerFactory.getLogger(DeprecatedFilter.class);

    /**
     * 已经打印日志的方法集合
     */
    private static final Set<String> logged = new ConcurrentHashSet<String>();

    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
        // 获得方法名
        String key = invoker.getInterface().getName() + "." + invocation.getMethodName();
        // 打印告警日志
        if (!logged.contains(key)) {
            logged.add(key);
            if (invoker.getUrl().getMethodParameter(invocation.getMethodName(), Constants.DEPRECATED_KEY, false)) {
                LOGGER.error("The service method " + invoker.getInterface().getName() + "." + getMethodSignature(invocation) + " is DEPRECATED! Declare from " + invoker.getUrl());
            }
        }
        return invoker.invoke(invocation);
    }

    // 省略 getMethodSignature 方法

}
```

---

- logged**静态**属性，已经打印日志的方法集合。
- 第 14 行：获得方法名。
- 第 16 至 21 行：打印告警日志。一个服务的方法，**有且仅有**打印一次。例如：

```text
[14/04/18 11:51:35:035 CST] main ERROR filter.DeprecatedFilter:  [DUBBO] The service method com.alibaba.dubbo.demo.DemoService.say01(String) is DEPRECATED! Declare from dubbo://192.168.3.17:20880/com.alibaba.dubbo.demo.DemoService?accesslog=true&anyhost=true&application=demo-consumer&callbacks=1000&check=false&client=netty4&default.delay=-1&default.retries=0&delay=-1&deprecated=false&dubbo=2.0.0&generic=false&interface=com.alibaba.dubbo.demo.DemoService&methods=sayHello,callbackParam,say03,say04,say01,bye,say02&payload=1000&pid=16820&qos.port=33333&register.ip=192.168.3.17&remote.timestamp=1523720843597&say01.deprecated=true&sayHello.async=true&server=netty4&service.filter=demo&side=consumer&timeout=100000&timestamp=1523721049491, dubbo version: 2.0.0, current host: 192.168.3.17
```

---

- 注意，【第 18 行】会根据方法在判断。因为，一个服务里，可能只有**部分**方法废弃。

- 第 22 行：调用 `Invoker#invoke(invocation)` 方法，服务调用。

# 3. DeprecatedInvokerListener

功能**类似**，在 [《精尽 Dubbo 源码分析 —— 服务引用（一）之本地引用（Injvm）》「5.2 DeprecatedInvokerListener」](http://svip.iocoder.cn/Dubbo/reference-refer-local/?self=) 中，已经有详细解析。