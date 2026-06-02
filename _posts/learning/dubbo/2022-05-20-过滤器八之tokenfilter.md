---
layout: post
title: 过滤器（八）之TokenFilter
author: deathwhispers
date: 2022-05-20
slug: dubbo-filter-token
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-20 11:52
updated: 2022-05-20 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享 TokenFilter 过滤器，用于服务**提供者**中，提供 **令牌验证** 的功能。在 [《Dubbo 用户指南 —— 令牌验证》](http://dubbo.apache.org/zh-cn/docs/user/demos/token-authorization.html) 定义如下：

通过令牌验证在**注册中心**控制权限，以决定要不要下发令牌给消费者，可以防止消费者绕过注册中心访问提供者。

另外通过注册中心可灵活改变授权方式，而不需修改或升级提供者。

![认证流程](/assets/images/learning/dubbo/dubbo-filter-token/b8b5e1985b34f89b62a2e499df5694d8.png)

- 官方文档写的很全，胖友请点击链接看完哈。

So ，可能和大多数胖友（包括我），一开始理解和期望的不太一样 。

# 2.【服务消费者】随机 Token

在 ServiceConfig 的 #doExportUrlsFor1Protocol(protocolConfig, registryURLs) 方法中，随机生成 Token ：

```java
// token ，参见《令牌校验》http://dubbo.apache.org/zh-cn/docs/user/demos/token-authorization.html
if (!ConfigUtils.isEmpty(token)) {
    if (ConfigUtils.isDefault(token)) { // true || default 时，UUID 随机生成
        map.put("token", UUID.randomUUID().toString());
    } else {
        map.put("token", token);
    }
}
```

---

# 3.【服务消费者】接收 Token

服务**消费者**，从注册中心，获取服务提供者的 **URL** ，从而获得该服务着的 Token 。所以，即使服务提供者随机生成 Token ，消费者一样可以拿到。

# 3.【服务消费者】发送 Token

RpcInvocation 在创建时，"**自动**"带上 Token ，如下图所示：

![RpcInvocation](/assets/images/learning/dubbo/dubbo-filter-token/51c7e2508e80c68647ca1eb34398d566.png)

# 4.【服务提供者】认证 Token

com.alibaba.dubbo.rpc.filter.TokenFilter ，实现 Filter 接口，**令牌验证** Filter 实现类。代码如下：

```java
@Activate(group = Constants.PROVIDER, value = Constants.TOKEN_KEY)
public class TokenFilter implements Filter {

    @Override
    public Result invoke(Invoker<?> invoker, Invocation inv) throws RpcException {
        // 获得服务提供者配置的 Token 值
        String token = invoker.getUrl().getParameter(Constants.TOKEN_KEY);
        if (ConfigUtils.isNotEmpty(token)) {
            // 从隐式参数中，获得 Token 值。
            Class<?> serviceType = invoker.getInterface();
            Map<String, String> attachments = inv.getAttachments();
            String remoteToken = attachments == null ? null : attachments.get(Constants.TOKEN_KEY);
            // 对比，若不一致，抛出 RpcException 异常
            if (!token.equals(remoteToken)) {
                throw new RpcException("Invalid token! Forbid invoke remote service " + serviceType + " method " + inv.getMethodName() + "() from consumer " + RpcContext.getContext().getRemoteHost() + " to provider " + RpcContext.getContext().getLocalHost());
            }
        }
        // 服务调用
        return invoker.invoke(inv);
    }
}
```

---