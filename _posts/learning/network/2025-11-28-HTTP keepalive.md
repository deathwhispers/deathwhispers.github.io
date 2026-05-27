---
layout: post
title: HTTP keepalive
slug: http-keepalive
type:
- note
date: 2025-11-28
week: 2025-W48
status: draft
tags:
- Network
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
categories:
- Learning
- Network
---

# HttpRequestRetryHandler

## 1. 类的作用

- **请求计数**：当发生异常时，如果重试次数大于设定值，则结束重连
- **异常判断**：当且仅当是可恢复的异常时，才进行重连

## 2. 具体实现

HttpRequestRetryHandler 的实现者为 `DefaultHttpRequestRetryHandler`，可通过 `DefaultHttpClient` 进行配置和使用。

## 3. 默认构造函数

```java
public DefaultHttpRequestRetryHandler(int retryCount, boolean requestSentRetryEnabled) {
    super();
    this.retryCount = retryCount;
    this.requestSentRetryEnabled = requestSentRetryEnabled;
}
```

## 4. 重连机制工作原理

在 `DefaultRequestDirector` 的 `execute` 方法中，通过 `while (retrying) {}` 循环不断发送请求：
- 当连接正常响应后，`retrying` 被重置为 `false`，退出循环
- 当请求过程中发生异常时，使用 `HttpRequestRetryHandler` 判断是否进行重连

## 5. 重连判断逻辑

`retryRequest` 方法用于判断是否应该重试请求：

```java
/**
 * Used `retryCount` and `requestSentRetryEnabled` to determine
 * if the given method should be retried.
 */
public boolean retryRequest(
    final IOException exception,
    int executionCount,
    final HttpContext context) {
    if (exception == null) {
        throw new IllegalArgumentException("Exception parameter may not be null");
    }
    if (context == null) {
        throw new IllegalArgumentException("HTTP context may not be null");
    }

    // 如果重试次数大于 retryCount（默认为3次），则返回false，execute方法会抛出对应异常
    if (executionCount > this.retryCount) {
        // Do not retry if over max retry count
        return false;
    }

    // NoHttpResponseException 是一种可以重试的异常
    if (exception instanceof NoHttpResponseException) {
        // Retry if the server dropped connection on us
        return true;
    }

    // InterruptedIOException 是一种不可以重试的异常
    if (exception instanceof InterruptedIOException) {
        // Timeout
        return false;
    }

    // UnknownHostException 是一种不可以重试的异常
    if (exception instanceof UnknownHostException) {
        // Unknown host
        return false;
    }

    // SSLHandshakeException 是一种不可以重试的异常
    if (exception instanceof SSLHandshakeException) {
        // SSL handshake exception
        return false;
    }

    Boolean b = (Boolean)
        context.getAttribute(ExecutionContext.HTTP_REQ_SENT);
    boolean sent = (b != null && b.booleanValue());

    if (!sent || this.requestSentRetryEnabled) {
        // Retry if the request has not been sent fully or
        // if it's OK to retry methods that have been sent
        return true;
    }

    // otherwise do not retry
    return false;
}
```

## 6. 可重试与不可重试的异常

### 可重试的异常
- `NoHttpResponseException`：服务器断开连接时
- `ConnectTimeoutException`：连接超时
- `SocketTimeoutException`：套接字超时
- 其他未完全发送的请求

### 不可重试的异常
- `InterruptedIOException`：超时
- `UnknownHostException`：未知主机
- `SSLHandshakeException`：SSL握手异常
- 已完全发送且 `requestSentRetryEnabled` 为 `false` 的请求

## 7. 总结

`HttpRequestRetryHandler` 是 HttpClient 中用于控制请求重试逻辑的核心组件，它通过判断异常类型、重试次数和请求发送状态来决定是否进行重连，从而提高网络请求的可靠性。
