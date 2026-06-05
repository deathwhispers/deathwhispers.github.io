---
layout: post
title: 服务调用（五）之远程调用（WebService）
author: deathwhispers
date: 2022-05-04
slug: dubbo-invocation-webservice
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-05 11:51
updated: 2022-05-05 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文，我们分享 webservice:// 协议的远程调用，主要分成**三个部分**：

- 服务暴露
- 服务引用
- 服务调用

对应项目为 dubbo-rpc-webservice 。

对应文档为 [《Dubbo 用户指南 —— webservice://》](http://dubbo.apache.org/zh-cn/docs/user/references/protocol/webservice.html) 。定义如下：

基于 WebService 的远程调用协议，基于 [Apache CXF](http://cxf.apache.org/) 的 frontend-simple 和 transports-http 实现。

可以和原生 WebService 服务互操作，即：

- 提供者用 Dubbo 的 WebService 协议暴露服务，消费者直接用标准 WebService 接口调用，
- 或者提供方用标准 WebService 暴露服务，消费方用 Dubbo 的 WebService 协议调用。

本文涉及类图（红圈部分）如下：

![类图](/assets/images/learning/dubbo/dubbo-invocation-webservice/37ab7032cc3d71169218f05e54918c08.png)

旁白君：整体实现和 dubbo-rpc-http 一致，所以内容上和 [《精尽 Dubbo 源码分析 —— 服务调用（三）之远程调用（HTTP）》](http://svip.iocoder.cn/Dubbo/rpc-http/?self=) 差不多。

# 2. WebServiceProtocol

[com.alibaba.dubbo.rpc.protocol.webservice.WebServiceProtocol](https://github.com/YunaiV/dubbo/blob/master/dubbo-rpc/dubbo-rpc-webservice/src/main/java/com/alibaba/dubbo/rpc/protocol/webservice/WebServiceProtocol.java) ，实现 AbstractProxyProtocol 抽象类，webservice:// 协议实现类。

## 2.1 构造方法

```text
plain /**  * 默认服务器端口  */ public static final int DEFAULT_PORT = 80; /**  * Http 服务器集合  *  * key：ip:port  */ private final Map<String, HttpServer> serverMap = new ConcurrentHashMap<String, HttpServer>(); /**  * 《我眼中的CXF之Bus》http://jnn.iteye.com/blog/94746  * 《CXF BUS》https://blog.csdn.net/chen_fly2011/article/details/56664908  */ private final ExtensionManagerBus bus = new ExtensionManagerBus(); /**  *  */ private final HTTPTransportFactory transportFactory = new HTTPTransportFactory(); /**  * HttpBinder$Adaptive 对象  */ private HttpBinder httpBinder;  public WebServiceProtocol() {     super(Fault.class);     bus.setExtension(new ServletDestinationFactory(), HttpDestinationFactory.class); }  public void setHttpBinder(HttpBinder httpBinder) {     this.httpBinder = httpBinder; }
```

---

- serverMap
属性，HttpServer 集合。键为
ip:port
，通过
#getAddr(url)
方法，计算。代码如下：

```text
plain // AbstractProxyProtocol.java protected String getAddr(URL url) {     String bindIp = url.getParameter(Constants.BIND_IP_KEY, url.getHost());     if (url.getParameter(Constants.ANYHOST_KEY, false)) {         bindIp = Constants.ANYHOST_VALUE;     }     return NetUtils.getIpByHost(bindIp) + ":" + url.getParameter(Constants.BIND_PORT_KEY, url.getPort()); }
```

---

- skeletonMap
属性，
com.caucho.hessian.server.HessianSkeleton
集合。请求处理过程为
HttpServer => DispatcherServlet => WebServiceHandler => ServletController
。
- httpBinder
属性，HttpBinder$Adaptive 对象，通过
#setHttpBinder(httpBinder)
方法，Dubbo SPI 调用设置。
- rpcExceptions = Fault.class
。
- bus
和
transportFactory
属性，可以参看如下文章：
    - [《我眼中的CXF之Bus》](http://jnn.iteye.com/blog/94746)
    - [《CXF BUS》](https://blog.csdn.net/chen_fly2011/article/details/56664908)
- 艿艿对 Apache CXF 了解不多，所以本文更多梳理好整体脉络。

## 2.2 doExport

```text
plain 1: @Override  2: protected <T> Runnable doExport(T impl, Class<T> type, URL url) throws RpcException {  3:     // 获得服务器地址  4:     String addr = getAddr(url);  5:     // 获得 HttpServer 对象。若不存在，进行创建。  6:     HttpServer httpServer = serverMap.get(addr);  7:     if (httpServer == null) {  8:         httpServer = httpBinder.bind(url, new WebServiceHandler()); // WebServiceHandler  9:         serverMap.put(addr, httpServer); 10:     } 11:     // 创建 ServerFactoryBean 对象 12:     final ServerFactoryBean serverFactoryBean = new ServerFactoryBean(); 13:     serverFactoryBean.setAddress(url.getAbsolutePath()); 14:     serverFactoryBean.setServiceClass(type); 15:     serverFactoryBean.setServiceBean(impl); 16:     serverFactoryBean.setBus(bus); 17:     serverFactoryBean.setDestinationFactory(transportFactory); 18:     serverFactoryBean.create(); 19:     // 返回取消暴露的回调 Runnable 20:     return new Runnable() { 21:         public void run() { 22:             serverFactoryBean.destroy(); 23:         } 24:     }; 25: }
```

---

- 基于 **通信服务器**
dubbo-remoting-http
项目，作为
。
- 第 4 行：调用
#getAddr(url)
方法，获得服务器地址。
- 第 5 至 10 行：从
serverMap
中，获得 HttpServer 对象。若不存在，调用
HttpBinder#bind(url, handler)
方法，创建 HttpServer 对象。此处使用的 WebServiceHandler ，下文详细解析。
- 第 11 至 18 行：创建 ServerFactoryBean 对象。
- 第 19 至 24 行：返回取消暴露的回调 Runnable 对象。

### 2.2.1 WebServiceHandler

```text
plain private class WebServiceHandler implements HttpHandler {      private volatile ServletController servletController;      @Override     public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {         // 创建 ServletController 对象，设置使用 DispatcherServlet 。         if (servletController == null) {             HttpServlet httpServlet = DispatcherServlet.getInstance();             if (httpServlet == null) {                 response.sendError(500, "No such DispatcherServlet instance.");                 return;             }             synchronized (this) {                 if (servletController == null) {                     servletController = new ServletController(transportFactory.getRegistry(), httpServlet.getServletConfig(), httpServlet);                 }             }         }         // 设置调用方地址         RpcContext.getContext().setRemoteAddress(request.getRemoteAddr(), request.getRemotePort());         // 执行调用         servletController.invoke(request, response);     }  }
```

---

## 2.3 doRefer

```text
plain 1: @Override  2: @SuppressWarnings("unchecked")  3: protected <T> T doRefer(final Class<T> serviceType, final URL url) throws RpcException {  4:     // 创建 ClientProxyFactoryBean 对象  5:     ClientProxyFactoryBean proxyFactoryBean = new ClientProxyFactoryBean();  6:     proxyFactoryBean.setAddress(url.setProtocol("http").toIdentityString());  7:     proxyFactoryBean.setServiceClass(serviceType);  8:     proxyFactoryBean.setBus(bus);  9:     // 创建 Service Proxy 对象 10:     T ref = (T) proxyFactoryBean.create(); 11:     // 设置超时相关属性 12:     Client proxy = ClientProxy.getClient(ref); 13:     HTTPConduit conduit = (HTTPConduit) proxy.getConduit(); 14:     HTTPClientPolicy policy = new HTTPClientPolicy(); 15:     policy.setConnectionTimeout(url.getParameter(Constants.CONNECT_TIMEOUT_KEY, Constants.DEFAULT_CONNECT_TIMEOUT)); 16:     policy.setReceiveTimeout(url.getParameter(Constants.TIMEOUT_KEY, Constants.DEFAULT_TIMEOUT)); 17:     conduit.setClient(policy); 18:     return ref; 19: }
```

---

- 第 4 至 8 行：创建 ClientProxyFactoryBean 对象。
- 第 10 行：创建 Service Proxy 对象。
- 第 11 至 17 行：设置**超时相关**
属性。

### 2.3.1 getErrorCode

```text
plain @Override protected int getErrorCode(Throwable e) {     if (e instanceof Fault) {         e = e.getCause();     }     if (e instanceof SocketTimeoutException) {         return RpcException.TIMEOUT_EXCEPTION;     } else if (e instanceof IOException) {         return RpcException.NETWORK_EXCEPTION;     }     return super.getErrorCode(e); }
```

---

- 将异常，翻译成 Dubbo 异常码。

# 666. 彩蛋

![知识星球](/assets/images/learning/dubbo/dubbo-invocation-webservice/96ca62e95e06bbe2fa74153d2158bc13.png)

知识星球

水水的一篇更新，嘿嘿嘿。
