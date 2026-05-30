---
layout: post
title: 一文看透 Apache HttpClient 的底层请求执行与 Socket 连接建立流程（源码级解析）
author: deathwhispers
date: 2022-01-09
slug: apache-httpclient-under-the-hood
categories:
- IoT
- General
tags:
- IoT
- Network
type: note
---

# ✅ 一文看透 Apache HttpClient 的底层请求执行与 Socket 连接建立流程（源码级解析）

> HttpClient 的请求过程非常复杂，但本质上可以拆解为五个关键阶段：
>
> **请求执行 → 连接获取 → Socket 建立 → 响应处理 → 连接复用**
>
> 本文将从 `request.execute()` 一路向下，带你完整走完这条调用链。

---

# 一、整体执行流程总览（大局观）

一条完整请求的生命周期如下：

```text
request.execute()
    ↓
获取连接 requestConnection()
    ↓
ConnManager.getConnection()
    ↓
ConnAdapter.open()
    ↓
Socket.connect()
    ↓
发送请求 → 接收响应
    ↓
响应拦截器
    ↓
连接是否复用
```

后面的所有源码分析，都是围绕这条主线展开。

---

# 二、请求失败后的重试与直连重建

当请求发送异常时，HttpClient 并不是立即失败，而是分情况处理：

```java
this.log.debug(ex.getMessage(), ex);
this.log.info("Retrying request");

if (route.getHopCount() == 1) {
    this.log.debug("Reopening the direct connection.");
    managedConn.open(route, context, params);
} else {
    throw ex;
}
```

✅ 核心逻辑：

| 情况        | 是否重试     |
| --------- | -------- |
| 直连（无代理）   | ✅ 允许重新建连 |
| 多跳路由（含代理） | ❌ 直接抛异常  |

---

# 三、响应拦截器执行阶段

在成功收到响应后，进入协议级拦截器处理阶段：

```java
response.setParams(params);
requestExec.postProcess(response, httpProcessor, context);
```

这里会执行：

* gzip 解压
* header 处理
* 重定向相关处理

---

# 四、连接是否进入复用池（KeepAlive）

```java
reuse = reuseStrategy.keepAlive(response, context);

if (reuse) {
    long duration = keepAliveStrategy.getKeepAliveDuration(response, context);
    managedConn.setIdleDuration(duration, TimeUnit.MILLISECONDS);
}
```

✅ 这一步决定：

* 该连接是 **被复用**
* 还是 **请求结束后直接关闭**

---

# 五、是否触发重定向（follow-up request）

```java
RoutedRequest followup = handleResponse(roureq, response, context);

if (followup == null) {
    done = true;
} else {
    if (reuse) {
        HttpEntity entity = response.getEntity();
        if (entity != null) {
            entity.consumeContent();
        }
    managedConn.markReusable();
} else {
    managedConn.close();
}

if (!followup.getRoute().equals(roureq.getRoute())) {
    releaseConnection();
}

roureq = followup;
}

```

✅ 触发场景：

* 301 / 302
* 认证跳转
* 协议跳转

---

# 六、响应完成后的最终连接处理

```java
if ((response == null)
|| (response.getEntity() == null)
|| !response.getEntity().isStreaming()) {

    if (reuse) managedConn.markReusable();
    releaseConnection();

} else {
    HttpEntity entity = response.getEntity();
    entity = new BasicManagedEntity(entity, managedConn, reuse);
    response.setEntity(entity);
}

```

✅ 这一段的核心目的只有一个：

> **防止连接泄漏**

---

# 七、获取连接的真正入口：SingleClientConnManager

真正获取连接是从这里开始的：

```java
public final ClientConnectionRequest requestConnection(
final HttpRoute route,
final Object state) {

    return new ClientConnectionRequest() {

        public void abortRequest() {}

    public ManagedClientConnection getConnection(
    long timeout, TimeUnit tunit) {

        return SingleClientConnManager.this.getConnection(route, state);
    }
};
}

```

✅ 这里做了两件事：

* 返回一个 **连接请求对象**
* 真正获取连接在 `getConnection()` 里

---

# 八、核心连接获取逻辑：getConnection()

```java
public ManagedClientConnection getConnection(HttpRoute route, Object state) {

    if (managedConn != null)
    revokeConnection();

    closeExpiredConnections();

    boolean recreate = false;

    if (!uniquePoolEntry.connection.isOpen()) {
        recreate = true;
    }

if (recreate)
uniquePoolEntry = new PoolEntry();

managedConn = new ConnAdapter(uniquePoolEntry, route);
return managedConn;
}

```

✅ 核心职责总结：

| 功能             | 作用       |
| -------------- | -------- |
| 回收旧连接          | 防止污染     |
| 清理超时连接         | 避免假活跃    |
| 创建 PoolEntry   | 承载真实连接   |
| 创建 ConnAdapter | 对外暴露操作接口 |

> **真正干活的是 PoolEntry + OperatedClientConnection**

---

# 九、真正建立 TCP 连接：managedConn.open()

```java
public void open(HttpRoute route,
HttpContext context,
HttpParams params) throws IOException {

    this.tracker = new RouteTracker(route);

    connOperator.openConnection(
    this.connection,
    route.getTargetHost(),
    route.getLocalAddress(),
    context, params
    );
}

```

这里第一次真正触发 **网络通信级别的操作**。

---

# 十、最终 Socket 创建与连接（最底层）

最终调用落在：

```java
DefaultClientConnectionOperator.openConnection(...)
```

核心简化逻辑如下：

```java
InetAddress[] addresses = InetAddress.getAllByName(target.getHostName());

for (int i = 0;
i < addresses.length;
++i) {

    Socket sock = socketFactory.createSocket();
    conn.opening(sock, target);

    try {
        Socket connsock = socketFactory.connectSocket(
        sock,
        addresses[i].getHostAddress(),
        target.getPort(),
        local,
        0,
        params
        );

        prepareSocket(connsock, context, params);
        conn.openCompleted(isSecure, params);
        break;

    } catch (Exception ex) {
        if (i == addresses.length - 1) {
            throw new HttpHostConnectException(target, ex);
        }
}
}

```

✅ 这一段完成了真正的底层动作：

| 步骤        | 说明                |
| --------- | ----------------- |
| DNS 解析    | `getAllByName`    |
| 创建 Socket | `createSocket()`  |
| TCP 连接    | `connectSocket()` |
| SSL 握手    | HTTPS 时           |
| 连接完成回调    | `openCompleted()` |

> **从这一刻开始，HTTP 请求才真正拥有了底层网络通道。**

---

# ✅ 结语：你真正该记住的 5 层核心结构

```text
HttpClient 请求五层结构：

[1] RequestExecutor      → 请求调度
[2] ConnManager          → 连接管理
[3] ConnAdapter          → 连接适配
[4] PoolEntry            → 物理连接池
[5] Socket               → 真实网络通信
```
