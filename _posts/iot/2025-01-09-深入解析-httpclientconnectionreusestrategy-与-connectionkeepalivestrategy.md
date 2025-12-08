---
layout: post
title: "深入解析 HttpClient：ConnectionReuseStrategy 与 ConnectionKeepAliveStrategy"
slug: connection-reuse-strategy-connection-keep-alive-strategy
date: 2025-01-09
type:
  - note
tags:
  - httpclient
  - keep-alive
  - http
categories:
  - IoT
author: deathwhispers
---

## 1. 基础介绍

### 1.1 Keep-Alive 解析

HTTP 协议作为应用层协议，构建于 TCP/IP 或 UDP 等传输层协议之上，通过 Socket 实现客户端与服务端的通信。HTTP/1.0 和 HTTP/1.1 是两个主要版本，它们都是无状态协议。

-   **HTTP/1.0**: 每一次请求-响应周期结束后，TCP 连接会断开，下一次请求需要重新建立连接。
-   **HTTP/1.1**: 引入了 **Keep-Alive** 机制，允许在一次 TCP 连接中持续发送多份数据而无需断开。

**Keep-Alive** 机制通过减少 TCP 连接的建立次数，降低了 `TIME_WAIT` 状态的连接数量，从而提高了服务器的性能和吞吐量（更少的 TCP 连接意味着更少的系统内核调用，如 `accept()` 和 `close()`）。

![短链接与长连接示意图](/assets/images/iot/connection-reuse-strategy-connection-keep-alive-strategy/1698038930834-6e0244e9-e865-4d1a-867c-0d11f9c0e006.png)

#### 连接管理

-   **HTTP/1.0** 默认关闭 Keep-Alive。要启用它，需要在 HTTP 请求头中加入 `Connection: Keep-Alive`。服务器收到该请求后，也会在响应头中添加相同字段以确认使用 Keep-Alive。
-   **HTTP/1.1** 默认启用 Keep-Alive。若要关闭，需明确在请求头中加入 `Connection: close`。

> **Keep-Alive** 连接并非永久保持，它有一个可配置的保持时间。一个 HTTP 请求能否保持长连接，也取决于服务端是否支持并开启了 Keep-Alive 功能。

### 1.2 如何判断数据接收完整

在传统的 Socket 编程中，我们通常通过检查 `read()` 方法是否返回 `EOF`（-1）来判断数据流是否结束。

```java
Socket socket = new Socket("localhost", 10086);
InputStream is = socket.getInputStream();
BufferedReader br = new BufferedReader(new InputStreamReader(is));
String info = null;
while ((info = br.readLine()) != -1) {
    // process data
}
```

这种方式在非 Keep-Alive 的 HTTP 请求中是有效的，因为服务器在响应后会关闭连接，客户端自然会收到 `EOF`。

然而，在 Keep-Alive 模式下，连接在一次请求后保持打开状态，因此客户端无法通过 `EOF` 来判断响应是否结束。为了解决这个问题，HTTP 协议引入了 `Content-Length` 和 `Transfer-Encoding: chunked`。

-   **HTTP/1.0**: `Content-Length` 字段是可选的。
-   **HTTP/1.1**:
    -   如果启用了 Keep-Alive，则响应头中必须包含 `Content-Length` 或 `Transfer-Encoding: chunked` 之一。
    -   如果未启用 Keep-Alive，则 `Content-Length` 行为与 HTTP/1.0 相同，为可选字段。

## 2. `ConnectionReuseStrategy` 解析

在 Apache HttpClient 的 `DefaultRequestDirector.execute` 方法中，有如下逻辑：

```java
// The connection is in or can be brought to a re-usable state.
reuse = reuseStrategy.keepAlive(response, context);
if (reuse) {
    // Set the idle duration of this connection
    final long duration = keepAliveStrategy.getKeepAliveDuration(response, context);
    if (this.log.isDebugEnabled()) {
        final String s;
        if (duration > 0) {
            s = "for " + duration + " " + TimeUnit.MILLISECONDS;
        } else {
            s = "indefinitely";
        }
        this.log.debug("Connection can be kept alive " + s);
    }
    managedConn.setIdleDuration(duration, TimeUnit.MILLISECONDS);
}
```

这段代码表明，在一次 HTTP 请求完成后，连接不会立即关闭，而是通过一个**可重用策略（`ConnectionReuseStrategy`）**来判断连接是否可以保持以及可以保持多长时间。

`reuseStrategy` 的默认实现是 `DefaultConnectionReuseStrategy`。其核心方法 `keepAlive` 的逻辑如下：

```java
@Override
public boolean keepAlive(final HttpResponse response, final HttpContext context) {
    // ... 参数校验 ...

    // 1. 对于 HTTP 204 No Content 响应，如果包含 Content-Length > 0 或 Transfer-Encoding，则不重用连接。
    // 这是为了防止行为异常的服务器在 204 响应中返回内容体，导致连接状态不同步。
    if (response.getStatusLine().getStatusCode() == HttpStatus.SC_NO_CONTENT) {
        Header clh = response.getFirstHeader(HTTP.CONTENT_LEN);
        if (clh != null) {
            // ... 检查 Content-Length 是否大于 0 ...
        }
        Header teh = response.getFirstHeader(HTTP.TRANSFER_ENCODING);
        if (teh != null) {
            return false;
        }
    }

    // 2. 检查请求头中是否包含 "Connection: close"，如果包含，则不重用。
    HttpRequest request = (HttpRequest) context.getAttribute(HttpCoreContext.HTTP_REQUEST);
    if (request != null) {
        // ... 遍历 Connection 头 ...
        if (HTTP.CONN_CLOSE.equalsIgnoreCase(token)) {
            return false;
        }
    }

    // 3. 检查响应实体是否是自终止的。如果实体结束的标志是关闭连接，则无法保持 Keep-Alive。
    // - Transfer-Encoding 存在但值不是 "chunked"，则不重用。
    // - 如果响应可以有实体，但 Content-Length 头不合法（不存在、多于一个或值为负），则不重用。
    final ProtocolVersion ver = response.getStatusLine().getProtocolVersion();
    final Header teh = response.getFirstHeader(HTTP.TRANSFER_ENCODING);
    if (teh != null) {
        if (!HTTP.CHUNK_CODING.equalsIgnoreCase(teh.getValue())) {
            return false;
        }
    } else {
        if (canResponseHaveBody(request, response)) {
            // ... 校验 Content-Length ...
        }
    }

    // 4. 检查响应头中的 "Connection" 或 "Proxy-Connection"。
    HeaderIterator headerIterator = response.headerIterator(HTTP.CONN_DIRECTIVE);
    if (!headerIterator.hasNext()) {
        headerIterator = response.headerIterator("Proxy-Connection");
    }
    if (headerIterator.hasNext()) {
        // ... 遍历头信息 ...
        // 如果存在 "close"，则返回 false。
        // 如果存在 "keep-alive"，则标记为 true。
    }

    // 5. 默认策略：HTTP/1.1 及以上版本默认为持久连接，HTTP/1.0 及以下版本默认为非持久连接。
    return !ver.lessEquals(HttpVersion.HTTP_1_0);
}
```

#### `Proxy-Connection` 说明

`Proxy-Connection` 是 HTTP/1.0 时代的产物。当时一些老旧的代理服务器不完全支持 `Connection: keep-alive`。如果客户端直接发送此头，代理会原样转发给服务器，服务器会误认为要建立长连接，但代理本身不支持，导致问题。

为了解决这个问题，客户端转而发送 `Proxy-Connection: keep-alive`。
-   **新代理**：识别此头，并将其转换为 `Connection: keep-alive` 后再转发给服务器，成功建立持久连接。
-   **老代理**：不识别此头，原样转发，服务器也不认识，因此不会建立持久连接，避免了错误。

#### 总结

`keepAlive` 方法的核心判断逻辑：
1.  **返回 `false`（关闭连接）** 的情况：
    -   响应状态码为 `204` 但包含 `Content-Length > 0` 或 `Transfer-Encoding`。
    -   请求或响应头中明确包含 `Connection: close`。
    -   响应体长度无法确定（例如，没有 `Content-Length` 或 `Transfer-Encoding: chunked`）。
    -   HTTP 协议版本低于 `1.1` 且未明确指定 `Keep-Alive`。
2.  **返回 `true`（保持连接）** 的情况：
    -   响应头中明确包含 `Connection: keep-alive`。
    -   HTTP/1.1 及以上版本，且没有明确的关闭指令。

## 3. `ConnectionKeepAliveStrategy` 解析

当一个连接被 `ConnectionReuseStrategy` 判断为可重用后，它的存活时间由 `ConnectionKeepAliveStrategy` 决定。默认实现是 `DefaultConnectionKeepAliveStrategy`。

其核心方法 `getKeepAliveDuration` 用于获取连接的存活时间。

```java
@Override
public long getKeepAliveDuration(final HttpResponse response, final HttpContext context) {
    Args.notNull(response, "HTTP response");
    final HeaderElementIterator it = new BasicHeaderElementIterator(
            response.headerIterator(HTTP.CONN_KEEP_ALIVE));
    while (it.hasNext()) {
        final HeaderElement he = it.nextElement();
        final String param = he.getName();
        final String value = he.getValue();
        if (value != null && param.equalsIgnoreCase("timeout")) {
            try {
                return Long.parseLong(value) * 1000;
            } catch(final NumberFormatException ignore) {
            }
        }
    }
    return -1;
}
```

该方法解析响应头中的 `Keep-Alive` 字段。例如，如果响应头为 `Keep-Alive: timeout=5, max=100`，该方法会提取 `timeout` 的值 `5`，并将其转换为毫秒（5000ms）作为连接的空闲超时时间。

如果响应头中没有 `Keep-Alive` 字段或该字段中没有 `timeout` 参数，则此方法返回 `-1`，表示连接可以一直保持活动状态（除非被连接池的其他策略管理）。