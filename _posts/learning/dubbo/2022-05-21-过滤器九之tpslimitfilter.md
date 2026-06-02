---
layout: post
title: 过滤器（九）之TpsLimitFilter
author: deathwhispers
date: 2022-05-21
slug: dubbo-filter-tps-limit
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-21 11:52
updated: 2022-05-21 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享 TpsLimitFilter 过滤器，用于服务**提供者**中，提供 **限流** 的功能。

**配置方式**

① 通过 配置项，添加到 或 或 中开启，例如：

```xml
<dubbo:service interface="com.alibaba.dubbo.demo.DemoService" ref="demoServiceImpl" protocol="injvm" >
    <dubbo:parameter key="tps" value="100" />
</dubbo:service>
```

---

② 通过 配置项，设置 TPS **周期**。

**注意**

笔者阅读的 Dubbo 版本，目前暂未配置 TpsLimitFilter 到 Dubbo SPI 文件里，所以我们需要添加到 com.alibaba.dubbo.rpc.Filter 中，例如：

```properties
tps=com.alibaba.dubbo.rpc.filter.TpsLimitFilter
```

---

# 2. TpsLimitFilter

com.alibaba.dubbo.rpc.filter.TpsLimitFilter ，实现 Filter 接口，TPS 限流过滤器实现类。代码如下：

```java
@Activate(group = Constants.PROVIDER, value = Constants.TPS_LIMIT_RATE_KEY)
public class TpsLimitFilter implements Filter {

    private final TPSLimiter tpsLimiter = new DefaultTPSLimiter();

    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
        if (!tpsLimiter.isAllowable(invoker.getUrl(), invocation)) {
            throw new RpcException(
                    new StringBuilder(64)
                            .append("Failed to invoke service ")
                            .append(invoker.getInterface().getName())
                            .append(".")
                            .append(invocation.getMethodName())
                            .append(" because exceed max service tps.")
                            .toString());
        }
        // 服务调用
        return invoker.invoke(invocation);
    }

}
```

---

- 第 8 至 17 行：调用 `TPSLimiter#isAllowable(url, invocation)` 方法，根据 tps 限流规则判断是否限制此次调用。若是，抛出 RpcException 异常。目前使用 TPSLimiter 作为限流器的实现类。
- 第 19 行：调用 `Invoker#invoke(invocation)` 方法，服务调用。

# 3. TPSLimiter

com.alibaba.dubbo.rpc.filter.tps.TPSLimiter ，TPS 限制器接口。代码如下：

```java
public interface TPSLimiter {

    /**
     * judge if the current invocation is allowed by TPS rule
     *
     * 根据 tps 限流规则判断是否限制此次调用.
     *
     * @param url        url
     * @param invocation invocation
     * @return true allow the current invocation, otherwise, return false
     */
    boolean isAllowable(URL url, Invocation invocation);
}
```

---

## 3.1 DefaultTPSLimiter

com.alibaba.dubbo.rpc.filter.tps.DefaultTPSLimiter ，实现 TPSLimiter 接口，**默认** TPS 限制器实现类，**以服务为维度**。代码如下：

```java
public class DefaultTPSLimiter implements TPSLimiter {

    /**
     * StatItem 集合
     *
     * key：服务名
     */
    private final ConcurrentMap<String, StatItem> stats = new ConcurrentHashMap<String, StatItem>();

    @Override
    public boolean isAllowable(URL url, Invocation invocation) {
        // 获得 TPS 大小配置项
        int rate = url.getParameter(Constants.TPS_LIMIT_RATE_KEY, -1);
        // 获得 TPS 周期配置项，默认 60 秒
        long interval = url.getParameter(Constants.TPS_LIMIT_INTERVAL_KEY, Constants.DEFAULT_TPS_LIMIT_INTERVAL);
        String serviceKey = url.getServiceKey();
        // 要限流
        if (rate > 0) {
            // 获得 StatItem 对象
            StatItem statItem = stats.get(serviceKey);
            // 不存在，则进行创建
            if (statItem == null) {
                stats.putIfAbsent(serviceKey, new StatItem(serviceKey, rate, interval));
                statItem = stats.get(serviceKey);
            }
            // 根据 TPS 限流规则判断是否限制此次调用.
            return statItem.isAllowable(url, invocation);
        // 不限流
        } else {
            // 移除 StatItem
            StatItem statItem = stats.get(serviceKey);
            if (statItem != null) {
                stats.remove(serviceKey);
            }
            // 返回通过
            return true;
        }
    }

}
```

---

- stats**即以服务为维度**属性，StatItem 集合，Key 为 服务名。
- 第 13 行：获得 TPS 大小配置项 `tps`。
- 第 15 行：获得 TPS 周期配置项 `tps.interval`，默认 60 * 1000 毫秒。
- 第 17 至 27 行：若要限流，调用 `StatItem#isAllowable(url, invocation)` 方法，根据 TPS 限流规则判断是否限制此次调用。
- 第 28 至 37 行：若不限流，移除 StatItem 对象。

## 3.2 StatItem

com.alibaba.dubbo.rpc.filter.tps.StatItem ，统计项。

### 3.2.1 构造方法

```java
/**
 * 统计名，目前使用服务名
 */
private String name;
/**
 * 周期
 */
private long interval;
/**
 * 限制大小
 */
private int rate;
/**
 * 最后重置时间
 */
private long lastResetTime;
/**
 * 当前周期，剩余种子数
 */
private AtomicInteger token;

StatItem(String name, int rate, long interval) {
    this.name = name;
    this.rate = rate;
    this.interval = interval;
    this.lastResetTime = System.currentTimeMillis();
    this.token = new AtomicInteger(rate);
}
```

---

### 3.2.2 isAllowable

```java
public boolean isAllowable(URL url, Invocation invocation) {
    // 若到达下一个周期，恢复可用种子数，设置最后重置时间。
    long now = System.currentTimeMillis();
    if (now > lastResetTime + interval) {
        token.set(rate); // 回复可用种子数
        lastResetTime = now; // 最后重置时间
    }

    // CAS ，直到或得到一个种子，或者没有足够种子
    int value = token.get();
    boolean flag = false;
    while (value > 0 && !flag) {
        flag = token.compareAndSet(value, value - 1);
        value = token.get();
    }

    // 是否成功
    return flag;
}
```

---

# 666. 彩蛋

实际在服务的限流时，更推荐使用 **令牌桶算法** ，在 [《Eureka 源码解析 —— 基于令牌桶算法的 RateLimiter》](http://www.iocoder.cn/Eureka/rate-limiter/?self=) 中，我们有详细分享。