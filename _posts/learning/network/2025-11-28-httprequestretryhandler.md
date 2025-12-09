---
layout: post
title: HttpRequestRetryHandler
slug: http-request-retry-handler
type:
  - note
date: 2025-11-28
week: 2025-W48
status: draft
tags:
  - 计算机网络
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---


# HttpRequestRetryHandler

HttpRequestRetryHandler类

1：该类的作用

1）请求计数，当发生异常的时候，如果重试次数大于某个值，则重连结束

2）当且仅当是可恢复的异常，才能进行重连

2：该类的具体实现

我们通过DefaultHttpClient可以知道，HttpRequestRetryHandler的实现者为DefaultHttpRequestRetryHandler

3：该类的默认构造函数

```plain text

```

public DefaultHttpRequestRetryHandler(int retryCount, boolean requestSentRetryEnabled) {

super();

this.retryCount = retryCount;

this.requestSentRetryEnabled = requestSentRetryEnabled;

}

我们知道，在DefaultRequestDirector的execute方法中，是通过while (retrying) {}的方式来不断的循环发送的，当且仅当一次连接正常响应后，retrying会被重置为false，退出循环；如果在一次请求过程中，发生异常，我们就会使用到HttpRequestRetryHandler来判断如何进行重连，我们看下判断是否重连的逻辑

/**

* Used `retryCount` and `requestSentRetryEnabled` to determine

* if the given method should be retried.

*/

public boolean retryRequest(

final IOException exception,

int executionCount,

final HttpContext context) {

if (exception == null) {

throw new IllegalArgumentException(“Exception parameter may not be null”);

}

if (context == null) {

throw new IllegalArgumentException(“HTTP context may not be null”);

}

//如果重试次数大于retryCount，默认为3此，则返回false，则execute方法会抛出对应异常

if (executionCount > this.retryCount) {

// Do not retry if over max retry count

return false;

}

//NoHttpResponseException也是一种可以重试的异常，return true则打印下异常日志

if (exception instanceof NoHttpResponseException) {

// Retry if the server dropped connection on us

return true;

}

//InterruptedIOException也是一种不可以重试的异常，return false则抛出异常

if (exception instanceof InterruptedIOException) {

// Timeout

return false;

}

//UnknownHostException也是一种不可以重试的异常，return false则抛出异常

if (exception instanceof UnknownHostException) {

// Unknown host

return false;

}

//SSLHandshakeException也是一种不可以重试的异常，return false则抛出异常

if (exception instanceof SSLHandshakeException) {

// SSL handshake exception

return false;

}

Boolean b = (Boolean)

context.getAttribute(ExecutionContext.HTTP_REQ_SENT);

boolean sent = (b != null && b.booleanValue());

if (!sent || this.requestSentRetryEnabled) {

// Retry if the request has not been sent fully or

// if it’s OK to retry methods that have been sent

return true;

}

// otherwise do not retry

return false;

}

故并不是所有的异常我们都建议或者可以重试的，可以重连的异常有NoHttpResponseException，ConnectTimeoutException ，SocketTimeoutException等