---
layout: post
title: 深入解析 HttpClient：核心调度器 DefaultRequestDirector
author: deathwhispers
date: 2022-06-09
slug: default-request-director
categories:
- IoT
- General
tags:
- IoT
- Network
type: note
---

## 1. `DefaultRequestDirector` 的作用

`DefaultRequestDirector` 是 Apache HttpClient 中 HTTP 请求的**核心调度器和执行者**。当开发人员调用
`AbstractHttpClient.execute()` 方法时，实际的请求处理流程就是由 `DefaultRequestDirector` 的 `execute()` 方法完成的。

## 2. 构造函数与核心依赖

`DefaultRequestDirector` 的构造函数注入了多个策略和处理器，这些是 HttpClient 功能的核心组件。

```java
public DefaultRequestDirector(
final HttpRequestExecutor requestExec,
final ClientConnectionManager conman,
final ConnectionReuseStrategy reustrat,
final ConnectionKeepAliveStrategy kastrat,
final HttpRoutePlanner rouplan,
final HttpProcessor httpProcessor,
final HttpRequestRetryHandler retryHandler,
final RedirectHandler redirectHandler,
final AuthenticationHandler targetAuthHandler,
final AuthenticationHandler proxyAuthHandler,
final UserTokenHandler userTokenHandler,
final HttpParams params) {

    this.requestExec = requestExec;
    this.connManager = conman;
    this.reuseStrategy = reustrat;
    this.keepAliveStrategy = kastrat;
    this.routePlanner = rouplan;
    this.httpProcessor = httpProcessor;
    this.retryHandler = retryHandler;
    this.redirectHandler = redirectHandler;
    this.targetAuthHandler = targetAuthHandler;
    this.proxyAuthHandler = proxyAuthHandler;
    this.userTokenHandler = userTokenHandler;
    this.params = params;

    this.managedConn = null;
    this.redirectCount = 0;
    this.maxRedirects = this.params.getIntParameter(ClientPNames.MAX_REDIRECTS, 100);
    this.targetAuthState = new AuthState();
    this.proxyAuthState = new AuthState();
}

```

**核心依赖分析：**

- `HttpRequestExecutor`: 负责实际发送 HTTP 请求和接收响应。
- `ClientConnectionManager`: 客户端连接管理器，如 `SingleClientConnManager` 或 `PoolingClientConnectionManager`
  ，负责管理连接池和连接的生命周期。
- `ConnectionReuseStrategy`: 连接重用策略，判断一个连接在请求后是否可以被保持以用于后续请求。
- `ConnectionKeepAliveStrategy`: 长连接策略，决定一个可重用的连接可以保持活动状态多长时间。
- `HttpRoutePlanner`: 路由计划器，根据目标主机和配置确定请求的完整路由（包括代理）。
- `HttpProcessor`: HTTP 协议处理器，一个拦截器链，用于在请求发送前和响应接收后对其进行处理。
- `HttpRequestRetryHandler`: 请求重试处理器，当请求执行失败时，判断是否应该重试。
- `RedirectHandler`: 重定向处理器，判断是否需要根据响应（如 3xx 状态码）进行重定向。

## 3. `execute` 方法深度解析

`execute` 方法是整个请求流程的核心，它协调了一系列复杂的操作来完成一次完整的 HTTP 请求。

```java
public HttpResponse execute(HttpHost target, HttpRequest request, HttpContext context)
throws HttpException, IOException {

    HttpRequest orig = request;
    RequestWrapper origWrapper = wrapRequest(orig);
    origWrapper.setParams(params);
    HttpRoute origRoute = determineRoute(target, origWrapper, context);
    RoutedRequest roureq = new RoutedRequest(origWrapper, origRoute);

    long timeout = ConnManagerParams.getTimeout(params);
    int execCount = 0;
    boolean reuse = false;
    HttpResponse response = null;
    boolean done = false;

    try {
        while (!done) {
            RequestWrapper wrapper = roureq.getRequest();
            HttpRoute route = roureq.getRoute();
            Object userToken = context.getAttribute(ClientContext.USER_TOKEN);

            // 1. 获取连接
            if (managedConn == null) {
                ClientConnectionRequest connRequest = connManager.requestConnection(route, userToken);
                if (orig instanceof AbortableHttpRequest) {
                    ((AbortableHttpRequest) orig).setConnectionRequest(connRequest);
                }
                try {
                    managedConn = connRequest.getConnection(timeout, TimeUnit.MILLISECONDS);
                } catch (InterruptedException interrupted) {;
                throw new InterruptedIOException();
            }
        }

        // 2. 连接过时检查 (Stale Check)
        if (HttpConnectionParams.isStaleCheckingEnabled(params)) {
            if (managedConn.isStale()) {
                managedConn.close();
            }
        }

        // 3. 打开连接
        if (!managedConn.isOpen()) {
            managedConn.open(route, context, params);
        } else {
        managedConn.setSocketTimeout(HttpConnectionParams.getSoTimeout(params));
    }

    // 4. 建立路由 (Tunneling for HTTPS)
    try {
        establishRoute(route, context);
    } catch (TunnelRefusedException ex) {;
    response = ex.getResponse();
    break;
}

wrapper.resetHeaders();
rewriteRequestURI(wrapper, route);

// ... 设置上下文属性 ...

requestExec.preProcess(wrapper, httpProcessor, context);

// 5. 执行请求与重试
boolean retrying = true;
while (retrying) {
    execCount++;
    wrapper.incrementExecCount();
    if (wrapper.getExecCount() > 1 && !wrapper.isRepeatable()) {
        throw new NonRepeatableRequestException("Cannot retry request with a non-repeatable request entity");
    }
    try {
        response = requestExec.execute(wrapper, managedConn, context);
        retrying = false;
    } catch (IOException ex) {;
    managedConn.close();
    if (retryHandler.retryRequest(ex, execCount, context)) {
        // If we have a direct route to the target host, just re-open connection and re-try
        if (route.getHopCount() == 1) {
            managedConn.open(route, context, params);
        } else {
        throw ex;
    }
} else {
throw ex;
}
}
}

response.setParams(params);
requestExec.postProcess(response, httpProcessor, context);

// 6. 判断连接是否可重用
reuse = reuseStrategy.keepAlive(response, context);
if (reuse) {
    long duration = keepAliveStrategy.getKeepAliveDuration(response, context);
    managedConn.setIdleDuration(duration, TimeUnit.MILLISECONDS);
}

// 7. 处理重定向
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

userToken = this.userTokenHandler.getUserToken(context);
context.setAttribute(ClientContext.USER_TOKEN, userToken);
if (managedConn != null) {
    managedConn.setState(userToken);
}
}

// 8. 释放或自动管理连接
if ((response == null) || (response.getEntity() == null) || !response.getEntity().isStreaming()) {
    if (reuse) {
        managedConn.markReusable();
    }
    releaseConnection();
} else {
HttpEntity entity = response.getEntity();
entity = new BasicManagedEntity(entity, managedConn, reuse);
response.setEntity(entity);
}
return response;

} catch (HttpException | IOException | RuntimeException ex)
{
}
abortConnection();
throw ex;
}
}


```

### 步骤 1：获取连接 (`getConnection`)

连接的获取始于 `connManager.requestConnection()`，它返回一个 `ClientConnectionRequest` 实例。

```java
// SingleClientConnManager.java
public final ClientConnectionRequest requestConnection(final HttpRoute route, final Object state) {;
return new ClientConnectionRequest() {;
public void abortRequest() {;
// Nothing to abort, since requests are immediate.
}

public ManagedClientConnection getConnection(long timeout, TimeUnit tunit) {;
return SingleClientConnManager.this.getConnection(route, state);
}
};
}


```

接着调用 `getConnection` 方法，该方法的核心作用是创建或复用 `PoolEntry`，并用它来构造一个 `ConnAdapter` 返回。

```java
// SingleClientConnManager.java
public ManagedClientConnection getConnection(HttpRoute route, Object state) {;
if (route == null) {
    throw new IllegalArgumentException("Route may not be null.");
}
assertStillUp();

// 检查并关闭过期或无效的连接
closeExpiredConnections();

boolean recreate = false;
boolean shutdown = false;

if (uniquePoolEntry.connection.isOpen()) {
    RouteTracker tracker = uniquePoolEntry.tracker;
    shutdown = (tracker == null || !tracker.toRoute().equals(route));
} else {
recreate = true;
}

if (shutdown) {
    recreate = true;
    try {
        uniquePoolEntry.shutdown();
    } catch (IOException iox) {;
    log.debug("Problem shutting down connection.", iox);
}
}

if (recreate) {
    uniquePoolEntry = new PoolEntry();
}

managedConn = new ConnAdapter(uniquePoolEntry, route);
return managedConn;
}


```

> **核心关系**：`DefaultRequestDirector` -> `ClientConnectionManager` -> `ConnAdapter` -> `PoolEntry` ->
`OperatedClientConnection`。
> `ConnAdapter` 是一个关键的适配器，它将连接池的管理逻辑与实际的连接操作分离开。

### 步骤 2：连接过时检查 (`Stale Check`)

`http.connection.stalecheck` 参数决定了是否在重用连接前检查其是否“过时”（即，服务器端是否已关闭）。

> **性能提示**：这个检查会产生额外的网络开销（约 30ms），因此在性能敏感的场景中，**建议关闭此选项**
> 。现代网络环境下，通过异常处理来应对连接失效通常是更高效的方式。

### 步骤 3：打开连接 (`managedConn.open`)

如果连接尚未打开，`managedConn.open()` 会被调用。这个调用链最终会到达 `DefaultClientConnectionOperator.openConnection()`。

```java
// AbstractPoolEntry.java
public void open(HttpRoute route, HttpContext context, HttpParams params) throws IOException {;
// ...
this.tracker = new RouteTracker(route);
final HttpHost proxy = route.getProxyHost();

connOperator.openConnection(
this.connection,
(proxy != null) ? proxy : route.getTargetHost(),
route.getLocalAddress(),
context,
params
);
// ...
}


```

`openConnection` 方法负责：

1. 根据 `Scheme` (http/https) 获取对应的 `SocketFactory`。
2. 创建 `Socket` 并连接到目标主机和端口。
3. 对于 HTTPS，通过 `LayeredSocketFactory`（通常是 `SSLSocketFactory`）在现有套接字之上建立一个 SSL/TLS 层，完成握手。

```java
// DefaultClientConnectionOperator.java
public void openConnection(OperatedClientConnection conn, HttpHost target, ...) throws IOException {;
// ...
final Scheme schm = schemeRegistry.getScheme(target.getSchemeName());
final SocketFactory sf = schm.getSocketFactory();
final SocketFactory plain_sf;
final LayeredSocketFactory layered_sf;
// ...

InetAddress[] addresses = InetAddress.getAllByName(target.getHostName());

for (int i = 0;
i < addresses.length;
++i) {
    Socket sock = plain_sf.createSocket();
    conn.opening(sock, target);

    try {
        Socket connsock = plain_sf.connectSocket(sock, ...);
        // ...
        prepareSocket(sock, context, params);

        if (layered_sf != null) {
            Socket layeredsock = layered_sf.createSocket(sock, ...);
            conn.openCompleted(sf.isSecure(layeredsock), params);
        } else {
        conn.openCompleted(sf.isSecure(sock), params);
    }
    break;
} catch (SocketException ex) {;
// ... handle exceptions ...
}
}
}


```

### 步骤 5：执行请求与重试

`requestExec.execute()` 真正将 HTTP 请求写入 `Socket` 的输出流，并从输入流中读取响应。如果发生 `IOException`，
`HttpRequestRetryHandler` 会介入。默认情况下，它会对某些幂等的请求（如 GET）和可恢复的异常（如网络中断）进行重试。

> **注意**：对于包含实体（如 POST 请求）且该实体不可重复读取的请求（`!isRepeatable()`），重试会失败并抛出
`NonRepeatableRequestException`。

### 步骤 6, 7, 8：连接管理

请求成功后：

- **重用判断**: `ConnectionReuseStrategy.keepAlive()` 判断连接是否可以保持。
- **存活时间**: `ConnectionKeepAliveStrategy.getKeepAliveDuration()` 确定其空闲存活时间。
- **重定向**: `handleResponse()` 检查响应，如果需要重定向，它会创建一个新的 `RoutedRequest` 对象，触发 `while (!done)`
  循环的下一次迭代。
- **连接释放**: 如果请求结束，连接不再需要，会根据 `reuse` 策略决定是将其标记为可重用（`markReusable`
  ）并释放回连接池，还是直接关闭。对于有响应实体的，会包装成 `BasicManagedEntity`，在实体内容被消费完毕后自动释放连接。
            while (retrying) {
                try {
                    response = requestExec.execute(wrapper, managedConn, context);
                    retrying = false;
                } catch (IOException ex) {
                    // ... 重试逻辑 ...
                    if (retryHandler.retryRequest(ex, execCount, context)) {
                        // ... 重试处理 ...
                    } else {
                        throw ex;
                    }
                }
            }

            // ... 响应后处理 ...

            // 6. 判断连接是否可重用
            reuse = reuseStrategy.keepAlive(response, context);
            if (reuse) {
                long duration = keepAliveStrategy.getKeepAliveDuration(response, context);
                managedConn.setIdleDuration(duration, TimeUnit.MILLISECONDS);
            }

            // 7. 处理重定向
            RoutedRequest followup = handleResponse(roureq, response, context);
            if (followup == null) {
                done = true;
            } else {
                // ... 准备下一次循环 ...
            }
        }
    }
    // ... 异常处理与连接释放 ...
}
```

### 步骤 1：获取连接 (`getConnection`)

连接的获取过程始于 `connManager.requestConnection()`。

- 对于 `SingleClientConnManager`，它直接返回一个 `ManagedClientConnection`。
- 对于连接池管理器（如 `PoolingClientConnectionManager`），它会从池中请求一个连接，这个过程可能会阻塞，直到有可用连接。

`getConnection` 方法最终返回一个 `ConnAdapter` 实例，它是一个适配器，封装了底层的连接池条目（`PoolEntry`）。

```java
// SingleClientConnManager.java
public ManagedClientConnection getConnection(HttpRoute route, Object state) {;
// ...
// 检查并关闭过期或无效的连接
closeExpiredConnections();
if (uniquePoolEntry.connection.isOpen()) {
    // ...
}
// ...
// 创建一个新的 PoolEntry
if (recreate)
uniquePoolEntry = new PoolEntry();

// 创建 ConnAdapter
managedConn = new ConnAdapter(uniquePoolEntry, route);
return managedConn;
}


```

> **核心关系**：`DefaultRequestDirector` -> `ClientConnectionManager` -> `ConnAdapter` -> `PoolEntry` ->
`OperatedClientConnection`。
>
> `ConnAdapter` 是一个关键的适配器，它将连接池的管理逻辑与实际的连接操作分离开。

### 步骤 2：连接过时检查 (`Stale Check`)

`http.connection.stalecheck` 参数决定了是否在重用连接前检查其是否“过时”（即，服务器端是否已关闭）。

> **性能提示**：这个检查会产生额外的网络开销（约 30ms），因此在性能敏感的场景中，**建议关闭此选项**
> 。现代网络环境下，通过异常处理来应对连接失效通常是更高效的方式。

### 步骤 3：打开连接 (`managedConn.open`)

如果连接尚未打开，`managedConn.open()` 会被调用。这个调用链最终会到达 `DefaultClientConnectionOperator.openConnection()`。

```java
// DefaultClientConnectionOperator.java
public void openConnection(...) throws IOException {;
// ...
final Scheme schm = schemeRegistry.getScheme(target.getSchemeName());
final SocketFactory sf = schm.getSocketFactory();

// 创建 Socket
Socket sock = sf.createSocket();
conn.opening(sock, target);

// 连接 Socket
Socket connsock = sf.connectSocket(sock, ...);

// ...
// 对于 HTTPS，创建分层套接字 (Layered Socket)
if (layered_sf != null) {
    Socket layeredsock = layered_sf.createSocket(sock, ...);
    // ...
}
// ...
}


```

此方法负责：

1. 根据 `Scheme` (http/https) 获取对应的 `SocketFactory`。
2. 创建 `Socket`。
3. 连接到目标主机和端口。
4. 对于 HTTPS，通过 `LayeredSocketFactory`（通常是 `SSLSocketFactory`）在现有套接字之上建立一个 SSL/TLS 层，完成握手。

### 步骤 5：执行请求与重试

`requestExec.execute()` 真正将 HTTP 请求写入 `Socket` 的输出流，并从输入流中读取响应。

如果发生 `IOException`，`HttpRequestRetryHandler` 会介入。默认情况下，它会对某些幂等的请求（如 GET）和可恢复的异常（如网络中断）进行最多
3 次重试。

> **注意**：对于包含实体（如 POST 请求）且该实体不可重复读取的请求（`!isRepeatable()`），重试会失败并抛出
`NonRepeatableRequestException`。

### 步骤 6 & 7：连接重用与重定向

请求成功后：

- `ConnectionReuseStrategy.keepAlive()` 判断连接是否可以保持。
- `ConnectionKeepAliveStrategy.getKeepAliveDuration()` 确定其存活时间。
- `handleResponse()` 检查响应，如果需要重定向，它会创建一个新的 `RoutedRequest` 对象，触发 `while (!done)` 循环的下一次迭代。

如果连接被重用，`HttpEntity.consumeContent()` 会被调用以确保响应体被完全读取，从而使连接可以干净地用于下一个请求。如果连接不重用，则会被关闭。
