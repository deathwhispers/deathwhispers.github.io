---
layout: post
title: 过滤器（三）之AccessLogFilter
author: deathwhispers
date: 2022-05-15
slug: dubbo-filter-accesslog
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-15 11:52
updated: 2022-05-15 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享记录访问日志的过滤器 AccessLogFilter ，需要在 `<dubbo:service>` 或 `<dubbo:reference>` 或 `<dubbo:method>` 中，设置 "accesslog" 配置项开启。有两种配置项选择：

- 【配置方式一】true：将向日志组件 logger 中输出访问日志。
- 【配置方式二】访问日志文件路径：直接把访问日志输出到指定文件。

# 2. AccessLogFilter

com.alibaba.dubbo.rpc.filter.AccessLogFilter ，实现 Filter 接口，记录服务的访问日志的过滤器实现类。

## 2.1 构造方法

```java
/**
 * 访问日志在 {@link LoggerFactory} 中的日志名
 */
private static final String ACCESS_LOG_KEY = "dubbo.accesslog";

/**
 * 访问日志的文件后缀
 */
private static final String FILE_DATE_FORMAT = "yyyyMMdd";
/**
 * 日历的时间格式化
 */
private static final String MESSAGE_DATE_FORMAT = "yyyy-MM-dd HH:mm:ss";
/**
 * 队列大小，即 {@link #logQueue} 值的大小
 */
private static final int LOG_MAX_BUFFER = 5000;
/**
 * 日志输出频率，单位：毫秒。仅适用于 {@link #logFuture}
 */
private static final long LOG_OUTPUT_INTERVAL = 5000;

/**
 * 日志队列
 *
 * key：访问日志名
 * value：日志集合
 */
private final ConcurrentMap<String, Set<String>> logQueue = new ConcurrentHashMap<String, Set<String>>();
/**
 * 定时任务线程池
 */
private final ScheduledExecutorService logScheduled = Executors.newScheduledThreadPool(2, new NamedThreadFactory("Dubbo-Access-Log", true));
/**
 * 记录日志任务
 */
private volatile ScheduledFuture<?> logFuture = null;
```

---

- 【配置方式一】
    - ACCESS_LOG_KEY
- 【配置方式二】
    - 文件相关：
        - FILE_DATE_FORMAT
        - MESSAGE_DATE_FORMAT
    - 队列相关：
        - logQueue
        - LOG_MAX_BUFFER
    - 任务相关：
        - logScheduled
        - LOG_OUTPUT_INTERVAL
        - logFuture
    - 日志流向为：**logMessage** => 队列 => 任务 => 文件。

## 2.2 invoke

```java
@Override
@SuppressWarnings("Duplicates")
public Result invoke(Invoker<?> invoker, Invocation inv) throws RpcException {
    try {
        // 记录访问日志的文件名
        String accesslog = invoker.getUrl().getParameter(Constants.ACCESS_LOG_KEY);
        if (ConfigUtils.isNotEmpty(accesslog)) {
            // 服务的名字、版本、分组信息
            RpcContext context = RpcContext.getContext();
            String serviceName = invoker.getInterface().getName();
            String version = invoker.getUrl().getParameter(Constants.VERSION_KEY);
            String group = invoker.getUrl().getParameter(Constants.GROUP_KEY);
            // 拼接日志内容
            StringBuilder sn = new StringBuilder();
            sn.append("[").append(new SimpleDateFormat(MESSAGE_DATE_FORMAT).format(new Date())).append("] ") // 时间
                    .append(context.getRemoteHost()).append(":").append(context.getRemotePort()) // 调用方地址
                    .append(" -> ").append(context.getLocalHost()).append(":").append(context.getLocalPort()) // 本地地址
                    .append(" - ");
            if (null != group && group.length() > 0) { // 分组
                sn.append(group).append("/");
            }
            sn.append(serviceName); // 服务名
            if (null != version && version.length() > 0) { // 版本
                sn.append(":").append(version);
            }
            sn.append(" ");
            sn.append(inv.getMethodName()); // 方法名
            sn.append("(");
            Class<?>[] types = inv.getParameterTypes(); // 参数类型
            if (types != null && types.length > 0) {
                boolean first = true;
                for (Class<?> type : types) {
                    if (first) {
                        first = false;
                    } else {
                        sn.append(",");
                    }
                    sn.append(type.getName());
                }
            }
            sn.append(") ");
            Object[] args = inv.getArguments(); // 参数值
            if (args != null && args.length > 0) {
                sn.append(JSON.toJSONString(args));
            }
            String msg = sn.toString();
            // 【方式一】使用日志组件，例如 Log4j 等写
            if (ConfigUtils.isDefault(accesslog)) {
                LoggerFactory.getLogger(ACCESS_LOG_KEY + "." + invoker.getInterface().getName()).info(msg);
            // 【方式二】异步输出到指定文件
            } else {
                log(accesslog, msg);
            }
        }
    } catch (Throwable t) {
        logger.warn("Exception in AcessLogFilter of service(" + invoker + " -> " + inv + ")", t);
    }
    // 服务调用
    return invoker.invoke(inv);
}
```

---

- 第 6 行：获得访问日志的配置项。
- 第 8 至 12 行：获得服务的名字、版本、分组信息。
- 第 13 至 46 行：拼接日志的内容。例子如下：

```text
[2018-04-14 11:57:58] 192.168.3.17:57207 -> 192.168.3.17:20880 - com.alibaba.dubbo.demo.DemoService say01(java.lang.String) [null]
```

---

- 第 47 至 49 行：调用 [《Dubbo 用户指南 —— 日志适配》](http://dubbo.apache.org/zh-cn/docs/user/demos/logger-strategy.html) ConfigUtils#isDefault(value) 方法，判断是否使用日志组件记录日志。例如 Log4J 等等。详细参见。
- 第 50 至 53 行：调用 #log(accesslog, logMessage) 方法，添加日志内容到日志队列。代码如下：

```java
/**
 * 初始化任务
 */
private void init() {
    if (logFuture == null) {
        synchronized (logScheduled) {
            if (logFuture == null) { // 双重锁，避免重复初始化
                logFuture = logScheduled.scheduleWithFixedDelay(new LogTask(), LOG_OUTPUT_INTERVAL, LOG_OUTPUT_INTERVAL, TimeUnit.MILLISECONDS);
            }
        }
    }
}

/**
 * 添加日志内容到日志队列
 *
 * @param accesslog 日志文件
 * @param logmessage 日志内容
 */
private void log(String accesslog, String logmessage) {
    // 初始化
    init();
    // 获得队列，以文件名为 Key
    Set<String> logSet = logQueue.get(accesslog);
    if (logSet == null) {
        logQueue.putIfAbsent(accesslog, new ConcurrentHashSet<String>());
        logSet = logQueue.get(accesslog);
    }
    // 若未超过队列大小，添加到队列中
    if (logSet.size() < LOG_MAX_BUFFER) {
        logSet.add(logmessage);
    }
}
```

---

## 2.3 LogTask

LogTask 是 AccessLogFilter 的内部类

```java
/**
 * 日志任务
 */
private class LogTask implements Runnable {

    @Override
    public void run() {
        try {
            if (logQueue.size() > 0) {
                for (Map.Entry<String, Set<String>> entry : logQueue.entrySet()) {
                    try {
                        String accesslog = entry.getKey();
                        Set<String> logSet = entry.getValue();
                        // 获得日志文件
                        File file = new File(accesslog);
                        File dir = file.getParentFile();
                        if (null != dir && !dir.exists()) {
                            dir.mkdirs();
                        }
                        if (logger.isDebugEnabled()) {
                            logger.debug("Append log to " + accesslog);
                        }
                        // 归档历史日志文件，例如： `accesslog` => `access.20181023`
                        if (file.exists()) {
                            String now = new SimpleDateFormat(FILE_DATE_FORMAT).format(new Date());
                            String last = new SimpleDateFormat(FILE_DATE_FORMAT).format(new Date(file.lastModified())); // 最后修改时间
                            if (!now.equals(last)) {
                                File archive = new File(file.getAbsolutePath() + "." + last);
                                file.renameTo(archive);
                            }
                        }
                        // 输出日志到指定文件
                        FileWriter writer = new FileWriter(file, true);
                        try {
                            for (Iterator<String> iterator = logSet.iterator(); iterator.hasNext(); iterator.remove()) {
                                writer.write(iterator.next()); // 写入一行日志
                                writer.write("\r\n"); // 换行
                            }
                            writer.flush(); // 刷盘
                        } finally {
                            writer.close(); // 关闭
                        }
                    } catch (Exception e) {
                        logger.error(e.getMessage(), e);
                    }
                }
            }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
    }

}
```

---

- 从 #init() 方法，我们可以看到，LogTask 每 5000 (LOG_OUTPUT_INTERVAL) 毫秒，执行一次。
- 第 9 至 10 行：循环日志队列 logQueue。注意乱序，日志集合使用了 ConcurrentHashSet ，所以会有一定的，在最终输出到指定文件后。
- 第 14 至 22 行：获得日志文件。
- 第 23 至 31 行：归档历史日志文件，例如：accesslog => access.20181023。
    - 注意文件最后修改时间第二天，因为是按照，所以极端情况（写着写着到了），那么就不会归档了。
- 第 32 至 42 行：输出日志到指定文件。

# 666. 彩蛋

实际使用时，推荐使用 accesslog="true" 配置项。

![知识星球](/assets/images/learning/dubbo/dubbo-filter-accesslog/96ca62e95e06bbe2fa74153d2158bc13.png)