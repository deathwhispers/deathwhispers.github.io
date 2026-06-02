---
layout: post
title: 服务调用（九）之远程调用（Memcached）
author: deathwhispers
date: 2022-05-09
slug: dubbo-invocation-memcached
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-09 11:51
updated: 2022-05-09 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文接 [《精尽 Dubbo 源码分析 —— 服务调用（八）之远程调用（Redis）》](http://svip.iocoder.cn/Dubbo/rpc-redis/?self=) ，我们分享 memcached:// 协议的远程调用，主要分成**两个个部分**：

- ~~服务暴露~~
- 服务引用
- 服务调用

对应项目为 dubbo-rpc-memcached 。

对应文档为 [《Dubbo 用户指南 —— memcached://》](http://dubbo.apache.org/zh-cn/docs/user/references/protocol/memcached.html) 。定义如下：

基于 Memcached 实现的 RPC 协议。

# 2. MemcachedProtocol

[com.alibaba.dubbo.rpc.protocol.memcached.MemcachedProtocol](https://github.com/YunaiV/dubbo/blob/master/dubbo-rpc/dubbo-rpc-memcached/src/main/java/com/alibaba/dubbo/rpc/protocol/memcached/MemcachedProtocol.java) ，实现 AbstractProtocol 抽象类，memcached:// 协议实现类。

## 2.1 export

```java
@Override
public <T> Exporter<T> export(final Invoker<T> invoker) throws RpcException {
    throw new UnsupportedOperationException("Unsupported export redis service. url: " + invoker.getUrl());
}
```

实际访问的就是 Memcached Server 实例，因此无需进行 Dubbo 服务暴露。客户端配置引用方式如下：

在客户端使用，注册中心读取：

或者，点对点直连：

```xml
<dubbo:reference id="store" interface="java.util.Map" url="memcached://10.20.153.10:11211" />
```

## 2.2 refer

```java
@Override
public <T> Invoker<T> refer(final Class<T> type, final URL url) throws RpcException {
    try {
        // 创建 MemcachedClient 对象
        String address = url.getAddress();
        String backup = url.getParameter(Constants.BACKUP_KEY);
        if (backup != null && backup.length() > 0) {
            address += "," + backup;
        }
        MemcachedClientBuilder builder = new XMemcachedClientBuilder(AddrUtil.getAddresses(address));
        final MemcachedClient memcachedClient = builder.build();

        // 处理方法名的映射
        final int expiry = url.getParameter("expiry", 0);
        final String get = url.getParameter("get", "get");
        final String set = url.getParameter("set", Map.class.equals(type) ? "put" : "set");
        final String delete = url.getParameter("delete", Map.class.equals(type) ? "remove" : "delete");
        return new AbstractInvoker<T>(type, url) {

            @Override
            protected Result doInvoke(Invocation invocation) throws Throwable {
                try {
                    // Memcached get 指令
                    if (get.equals(invocation.getMethodName())) {
                        if (invocation.getArguments().length != 1) {
                            throw new IllegalArgumentException("The memcached get method arguments mismatch, must only one arguments. interface: " + type.getName() + ", method: " + invocation.getMethodName() + ", url: " + url);
                        }
                        return new RpcResult(memcachedClient.get(String.valueOf(invocation.getArguments()[0])));
                    // Memcached set 指令
                    } else if (set.equals(invocation.getMethodName())) {
                        if (invocation.getArguments().length != 2) {
                            throw new IllegalArgumentException("The memcached set method arguments mismatch, must be two arguments. interface: " + type.getName() + ", method: " + invocation.getMethodName() + ", url: " + url);
                        }
                        memcachedClient.set(String.valueOf(invocation.getArguments()[0]), expiry, invocation.getArguments()[1]);
                        return new RpcResult();
                    // Memcached delele 指令
                    } else if (delete.equals(invocation.getMethodName())) {
                        if (invocation.getArguments().length != 1) {
                            throw new IllegalArgumentException("The memcached delete method arguments mismatch, must only one arguments. interface: " + type.getName() + ", method: " + invocation.getMethodName() + ", url: " + url);
                        }
                        memcachedClient.delete(String.valueOf(invocation.getArguments()[0]));
                        return new RpcResult();
                    // 不支持的指令，抛出异常
                    } else {
                        throw new UnsupportedOperationException("Unsupported method " + invocation.getMethodName() + " in memcached service.");
                    }
                } catch (Throwable t) {
                    RpcException re = new RpcException("Failed to invoke memcached service method. interface: " + type.getName() + ", method: " + invocation.getMethodName() + ", url: " + url + ", cause: " + t.getMessage(), t);
                    if (t instanceof TimeoutException || t instanceof SocketTimeoutException) {
                        re.setCode(RpcException.TIMEOUT_EXCEPTION);
                    } else if (t instanceof MemcachedException || t instanceof IOException) {
                        re.setCode(RpcException.NETWORK_EXCEPTION);
                    }
                    throw re;
                }
            }

            @Override
            public void destroy() {
                // 标记销毁
                super.destroy();
                // 关闭 MemcachedClient
                try {
                    memcachedClient.shutdown();
                } catch (Throwable e) {
                    logger.warn(e.getMessage(), e);
                }
            }

        };
    } catch (Throwable t) {
        throw new RpcException("Failed to refer memcached service. interface: " + type.getName() + ", url: " + url + ", cause: " + t.getMessage(), t);
    }
}
```

- 第 4 至 11 行：创建 MemcachedClient 对象。
- 第 13 至 17 行：处理方法名的映射。此处有个问题，Memcached 不存在 Map 数据结构，因此不存在 put 和 remove 指令。
- 第 18 至 73 行：创建 Invoker 对象。

### 2.2.1 doInvoke

- 第 23 至 28 行：Memcached **get** 指令。
- 第 29 至 35 行：Memcached **set** 指令。
- 第 36 至 42 行：Memcached **delete** 指令。
- 第 43 至 46 行：目前其他命令，暂时不支持。
- 第 47 至 55 行：翻译异常成 Dubbo 错误码。

### 2.2.2 destroy

- 第 61 行：调用 `super#destroy()` 方法，标记销毁。
- 第 63 至 67 行：调用 `Memcached#shutdown()` 方法，关闭 MemcachedClient 。

# 666. 彩蛋

![](/assets/images/learning/dubbo/dubbo-invocation-memcached/96ca62e95e06bbe2fa74153d2158bc13.png)

没有彩蛋~