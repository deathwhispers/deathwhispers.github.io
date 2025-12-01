---
layout: post
title: 服务调用（七）之远程调用（WebService）
slug: dubbo-invocation-webservice
type:
  - note
date: 2022-05-07
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-05-07 11:51
updated: 2022-05-07 18:33
---
本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文，我们分享 rmi:// 协议的远程调用，主要分成**三个部分**：

- 服务暴露
- 服务引用
- 服务调用

对应项目为 dubbo-rpc-rmi 。

对应文档为 [《Dubbo 用户指南 —— rmi://》](http://dubbo.apache.org/zh-cn/docs/user/references/protocol/rmi.html) 。定义如下：

RMI 协议采用 JDK 标准的 java.rmi.* 实现，采用阻塞式短连接和 JDK 标准序列化方式。

本文涉及类图（红圈部分）如下：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038345044-dadf8ece-1444-4702-8120-366aeaf98c9f.png)

类图

旁白君：整体实现和 dubbo-rpc-http 一致，所以内容上和 [《精尽 Dubbo 源码分析 —— 服务调用（三）之远程调用（HTTP）》](http://svip.iocoder.cn/Dubbo/rpc-http/?self=) 差不多。

# 2. RmiRemoteInvocation

```plain text
plain public class RmiRemoteInvocation extends RemoteInvocation {      private static final long serialVersionUID = 1L;      private static final String dubboAttachmentsAttrName = "dubbo.attachments";      /**      * executed on consumer side      *      * 构造将在消费端执行      */     public RmiRemoteInvocation(MethodInvocation methodInvocation) {         super(methodInvocation);         addAttribute(dubboAttachmentsAttrName, new HashMap<String, String>(RpcContext.getContext().getAttachments()));     }      /**      * Need to restore context on provider side (Though context will be overridden by Invocation's attachment      * when ContextFilter gets executed, we will restore the attachment when Invocation is constructed, check more      * from {@link com.alibaba.dubbo.rpc.proxy.InvokerInvocationHandler}      *      * 服务端执行时，重新放入上下文（虽然这时上下文在ContextFilter执行时将被Invocation的attachments覆盖，我们在Invocation构造时还原attachments, see InvokerInvocationHandler）      */     @SuppressWarnings("unchecked")     @Override     public Object invoke(Object targetObject) throws NoSuchMethodException, IllegalAccessException,             InvocationTargetException {         RpcContext context = RpcContext.getContext();         context.setAttachments((Map<String, String>) getAttribute(dubboAttachmentsAttrName));         try {             return super.invoke(targetObject);         } finally {             context.setAttachments(null);         }     } }
```

---

# 3. RmiProtocol

[com.alibaba.dubbo.rpc.protocol.rmi.RmiProtocol](https://github.com/YunaiV/dubbo/blob/master/dubbo-rpc/dubbo-rpc-rmi/src/main/java/com/alibaba/dubbo/rpc/protocol/rmi/RmiProtocol.java) ，实现 AbstractProxyProtocol 抽象类，rmi:// 协议实现类。

## 3.1 构造方法

```plain text
plain /**  * 默认端口  */ public static final int DEFAULT_PORT = 1099;  public RmiProtocol() {     super(RemoteAccessException.class, RemoteException.class); }  public int getDefaultPort() {     return DEFAULT_PORT; }
```

---

- rpcExceptions = RemoteAccessException.class, RemoteException.class
。
- 艿艿对 RMI了解不多，所以本文更多梳理好整体脉络。

## 3.2 doExport

```plain text
plain 1: @Override  2: protected <T> Runnable doExport(final T impl, Class<T> type, URL url) throws RpcException {  3:     // 创建 RmiServiceExporter 对象  4:     final RmiServiceExporter rmiServiceExporter = new RmiServiceExporter();  5:     rmiServiceExporter.setRegistryPort(url.getPort());  6:     rmiServiceExporter.setServiceName(url.getPath());  7:     rmiServiceExporter.setServiceInterface(type);  8:     rmiServiceExporter.setService(impl);  9:     try { 10:         rmiServiceExporter.afterPropertiesSet(); 11:     } catch (RemoteException e) { 12:         throw new RpcException(e.getMessage(), e); 13:     } 14:     // 返回取消暴露的回调 Runnable 15:     return new Runnable() { 16:         public void run() { 17:             try { 18:                 rmiServiceExporter.destroy(); 19:             } catch (Throwable e) { 20:                 logger.warn(e.getMessage(), e); 21:             } 22:         } 23:     }; 24: }
```

---

- 第 3 至 13 行：创建 RmiServiceExporter 对象。
- 第 14 至 23 行：返回取消暴露的回调 Runnable。

## 3.3 doRefer

```plain text
plain 1: @Override  2: @SuppressWarnings("unchecked")  3: protected <T> T doRefer(final Class<T> serviceType, final URL url) throws RpcException {  4:     // 创建 RmiProxyFactoryBean 对象  5:     final RmiProxyFactoryBean rmiProxyFactoryBean = new RmiProxyFactoryBean();  6:     // RMI needs extra parameter since it uses customized remote invocation object  7:     // RMI传输时使用自定义的远程执行对象，从而传递额外的参数  8:     if (url.getParameter(Constants.DUBBO_VERSION_KEY, Version.getVersion()).equals(Version.getVersion())) {  9:         // Check dubbo version on provider, this feature only support 10:         rmiProxyFactoryBean.setRemoteInvocationFactory(new RemoteInvocationFactory() { 11:             public RemoteInvocation createRemoteInvocation(MethodInvocation methodInvocation) { 12:                 return new RmiRemoteInvocation(methodInvocation); 13:             } 14:         }); 15:     } 16:     // 设置相关参数 17:     rmiProxyFactoryBean.setServiceUrl(url.toIdentityString()); 18:     rmiProxyFactoryBean.setServiceInterface(serviceType); 19:     rmiProxyFactoryBean.setCacheStub(true); 20:     rmiProxyFactoryBean.setLookupStubOnStartup(true); 21:     rmiProxyFactoryBean.setRefreshStubOnConnectFailure(true); 22:     rmiProxyFactoryBean.afterPropertiesSet(); 23:     // 创建 Service Proxy 对象 24:     return (T) rmiProxyFactoryBean.getObject(); 25: }
```

---

- 第 5 行：创建 RmiProxyFactoryBean 对象。
- 第 8 至 15 行：若远程服务是 Dubbo RMI 服务时，RMI 传输时使用自定义的远程执行对象，从而传递额外的参数。
- 第 16 至 22 行：设置相关参数。另外，dubbo 配置中的超时时间对 RMI 无效，需使用 java 启动参数设置
    - Dsun.rmi.transport.tcp.responseTimeout=3000
，参见下面的 RMI 配置
- 第 24 行：创建 Service Proxy 对象。

### 3.3.1 getErrorCode

```plain text
plain @Override protected int getErrorCode(Throwable e) {     if (e instanceof RemoteAccessException) {         e = e.getCause();     }     if (e != null && e.getCause() != null) {         Class<?> cls = e.getCause().getClass();         if (SocketTimeoutException.class.equals(cls)) {             return RpcException.TIMEOUT_EXCEPTION;         } else if (IOException.class.isAssignableFrom(cls)) {             return RpcException.NETWORK_EXCEPTION;         } else if (ClassNotFoundException.class.isAssignableFrom(cls)) {             return RpcException.SERIALIZATION_EXCEPTION;         }     }     return super.getErrorCode(e); }
```

---

- 将异常，翻译成 Dubbo 异常码。

# 666. 彩蛋

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038345162-a45a8f74-c102-4545-863a-080c237bfbdd.png)

知识星球

水水的一篇更新，嘿嘿嘿。