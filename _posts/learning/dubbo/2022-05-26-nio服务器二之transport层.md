---
layout: post
title: NIO服务器（二）之Transport层
author: deathwhispers
date: 2022-05-26
slug: dubbo-nio-server-transport
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-05-26 11:49
updated: 2022-05-26 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文接 [《精尽 Dubbo 源码分析 —— NIO 服务器（一）之抽象 API》](http://svip.iocoder.cn/Dubbo/remoting-api-interface/?self=) 一文，分享 dubbo-remoting-api 模块， transport 包，**网络传输层**。

**transport** 网络传输层：抽象 mina 和 netty 为统一接口，以 Message 为中心，扩展接口为 Channel, Transporter, Client, Server, Codec

涉及的类图如下：

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/773e08aa9257ced848b427d8f982ea06.png)

类图

- 白色部分，为通用接口。
- 蓝色部分，为
transport
包下的类。
- 整个类图，我们分成**六个**
部分：
    - Client
    - Server
    - Channel
    - ChannelHandler
    - Codec
    - Dispacher
- 从流程上来说，我们分成：
    - Server
        - 启动
        - 关闭
    - Client
        - 启动
        - 关闭
    - ChannelHandler
        - 处理连接
        - 处理断开
        - 发送消息
        - 接收消息
        - 处理异常

艿艿的旁白：涉及较多类和流程，内容不是很线性，可能分享的比较凌乱，还望胖友谅解。建议，读 2-3 遍，并且做一些调试。

# 2. AbstractPeer

[com.alibaba.dubbo.remoting.transport.AbstractPeer](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractPeer.java) ，实现 Endpoint、ChannelHandler 接口，**Peer** 抽象类。

**构造方法**

```plain text
plain 1: /**  2:  * 通道处理器  3:  */  4: private final ChannelHandler handler;  5: /**  6:  * URL  7:  */  8: private volatile URL url;  9: /** 10:  * 正在关闭 11:  * 12:  * {@link #startClose()} 13:  */ 14: // closing closed means the process is being closed and close is finished 15: private volatile boolean closing; 16: /** 17:  * 关闭完成 18:  * 19:  * {@link #close()} 20:  */ 21: private volatile boolean closed; 22:  23: public AbstractPeer(URL url, ChannelHandler handler) { 24:     if (url == null) { 25:         throw new IllegalArgumentException("url == null"); 26:     } 27:     if (handler == null) { 28:         throw new IllegalArgumentException("handler == null"); 29:     } 30:     this.url = url; 31:     this.handler = handler; 32: }
```

---

- handler
属性，通道处理器，通过构造方法传入。实现的 ChannelHandler 的接口方法，直接调用
handler
的方法，进行执行逻辑处理。
    - 参见代码：[传送门](https://github.com/YunaiV/dubbo/blob/7fad710c2dbf66356d5e7b7995e843b8f6225652/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractPeer.java#L114-L141)
    - 这种方式在设计模式中被称作 “[装饰模式](https://www.cnblogs.com/java-my-life/archive/2012/04/20/2455726.html)**大量的**
“ 。在下文中，我们会看到
装饰模式的使用。实际上，这也是
dubbo-remoting
抽象 API + 实现最核心的方式之一。
- url**配置项**
属性，URL ，通过构造方法传入。通过该属性，传递 Dubbo 服务引用和服务暴露的
。
- closing
属性，正在关闭，调用
#startClose()
方法，变更。
- close
属性，关闭完成，调用
#close()
方法，变更。

**发送消息**

```plain text
plain @Override public void send(Object message) throws RemotingException {     send(message, url.getParameter(Constants.SENT_KEY, false)); }
```

---

- sent
配置项：
    - true
等待消息发出，消息发送失败将抛出异常。
    - false
不等待消息发出，将消息放入 IO 队列，即刻返回。
    - 详细参见：[《Dubbo 用户指南 —— 异步调用》](http://dubbo.apache.org/zh-cn/docs/user/demos/async-call.html)

**其他方法**

胖友点击 [AbstractPeer](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractPeer.java) ，再看看**所有**的方法。

## 2.1 AbstractEndpint

[com.alibaba.dubbo.remoting.transport.AbstractPeer.AbstractEndpint](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractEndpoint.java) ，实现 Resetable 接口，继承 AbstractPeer 抽象类，**端点**抽象类。

**构造方法**

```plain text
plain 1: /**  2:  * 编解码器  3:  */  4: private Codec2 codec;  5: /**  6:  * 超时时间  7:  */  8: private int timeout;  9: /** 10:  * 连接超时时间 11:  */ 12: private int connectTimeout; 13:  14: public AbstractEndpoint(URL url, ChannelHandler handler) { 15:     super(url, handler); 16:     this.codec = getChannelCodec(url); 17:     this.timeout = url.getPositiveParameter(Constants.TIMEOUT_KEY, Constants.DEFAULT_TIMEOUT); 18:     this.connectTimeout = url.getPositiveParameter(Constants.CONNECT_TIMEOUT_KEY, Constants.DEFAULT_CONNECT_TIMEOUT); 19: }
```

---

- codec
属性，编解码器。在构造方法中，可以看到调用
#getChannelCodec(url)
方法，基于
url
参数，加载对应的 Codec 实现对象。代码如下：

```plain text
plain 1: protected static Codec2 getChannelCodec(URL url) { 2:     String codecName = url.getParameter(Constants.CODEC_KEY, "telnet"); 3:     if (ExtensionLoader.getExtensionLoader(Codec2.class).hasExtension(codecName)) { // 例如，在 DubboProtocol 中，会获得 DubboCodec 4:         return ExtensionLoader.getExtensionLoader(Codec2.class).getExtension(codecName); 5:     } else { 6:         return new CodecAdapter(ExtensionLoader.getExtensionLoader(Codec.class).getExtension(codecName)); 7:     } 8: }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">第 3 行：基于 Dubbo SPI 机制，加载对应的 Codec 实现对象。例如，在 DubboProtocol 中，会获得 </font>[DubboCodec](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/com/alibaba/dubbo/rpc/protocol/dubbo/DubboCodec.java)<font style="color:rgb(51, 51, 51);"> 对象。</font>
- <font style="color:rgb(51, 51, 51);">第 6 行：Codec 接口，已经废弃了，目前 Dubbo 项目里，也没有它的拓展实现。</font>
```

**重置属性**

[#reset(url)](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractEndpoint.java#L60-L92)**实现**方法，使用新的 url 属性，可重置 codectimeoutconnectTimeout 属性。 已经添加了谅解，胖友点击可看。

# 3. Client

## 3.1 AbstractClient

[com.alibaba.dubbo.remoting.transport.AbstractClient](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractClient.java) ，实现 Client 接口，继承 AbstractEndpoint 抽象类，**客户端**抽象类，**重点**实现了公用的重连逻辑，同时抽象了连接等模板方法，供子类实现。抽象方法如下：

```plain text
plain protected abstract void doOpen() throws Throwable; protected abstract void doClose() throws Throwable;  protected abstract void doConnect() throws Throwable; protected abstract void doDisConnect() throws Throwable;  protected abstract Channel getChannel();
```

---

**构造方法**

```plain text
plain 1: /**  2:  * 重连定时任务执行器  3:  */  4: private static final ScheduledThreadPoolExecutor reconnectExecutorService = new ScheduledThreadPoolExecutor(2, new NamedThreadFactory("DubboClientReconnectTimer", true));  5: /**  6:  * 发送消息时，若断开，是否重连  7:  */  8: private final boolean send_reconnect;  9: /** 10:  * 重连 warning 的间隔.(waring多少次之后，warning一次) //for test 11:  */ 12: // reconnect warning period. Reconnect warning interval (log warning after how many times) //for test 13: private final int reconnect_warning_period; 14: /** 15:  * 关闭超时时间 16:  */ 17: private final long shutdown_timeout; 18: /** 19:  * 线程池 20:  * 21:  * 在调用 {@link #wrapChannelHandler(URL, ChannelHandler)} 时，会调用 {@link com.alibaba.dubbo.remoting.transport.dispatcher.WrappedChannelHandler} 创建 22:  */ 23: protected volatile ExecutorService executor; 24:  25: public AbstractClient(URL url, ChannelHandler handler) throws RemotingException { 26:     super(url, handler); 27:     // 从 URL 中，获得重连相关配置项 28:     send_reconnect = url.getParameter(Constants.SEND_RECONNECT_KEY, false); 29:     shutdown_timeout = url.getParameter(Constants.SHUTDOWN_TIMEOUT_KEY, Constants.DEFAULT_SHUTDOWN_TIMEOUT); 30:     // The default reconnection interval is 2s, 1800 means warning interval is 1 hour. 31:     reconnect_warning_period = url.getParameter("reconnect.waring.period", 1800); 32:  33:     // 初始化客户端 34:     try { 35:         doOpen(); 36:     } catch (Throwable t) { 37:         close(); // 失败，则关闭 38:         throw new RemotingException(url.toInetSocketAddress(), null, 39:                 "Failed to start " + getClass().getSimpleName() + " " + NetUtils.getLocalAddress() 40:                         + " connect to the server " + getRemoteAddress() + ", cause: " + t.getMessage(), t); 41:     } 42:  43:     // 连接服务器 44:     try { 45:         // connect. 46:         connect(); 47:         if (logger.isInfoEnabled()) { 48:             logger.info("Start " + getClass().getSimpleName() + " " + NetUtils.getLocalAddress() + " connect to the server " + getRemoteAddress()); 49:         } 50:     } catch (RemotingException t) { 51:         if (url.getParameter(Constants.CHECK_KEY, true)) { 52:             close(); // 失败，则关闭 53:             throw t; 54:         } else { 55:             logger.warn("Failed to start " + getClass().getSimpleName() + " " + NetUtils.getLocalAddress() 56:                     + " connect to the server " + getRemoteAddress() + " (check == false, ignore and retry later!), cause: " + t.getMessage(), t); 57:         } 58:     } catch (Throwable t) { 59:         close(); // 失败，则关闭 60:         throw new RemotingException(url.toInetSocketAddress(), null, 61:                 "Failed to start " + getClass().getSimpleName() + " " + NetUtils.getLocalAddress() 62:                         + " connect to the server " + getRemoteAddress() + ", cause: " + t.getMessage(), t); 63:     } 64:  65:     // 获得线程池 66:     executor = (ExecutorService) ExtensionLoader.getExtensionLoader(DataStore.class).getDefaultExtension() 67:             .get(Constants.CONSUMER_SIDE, Integer.toString(url.getPort())); 68:     ExtensionLoader.getExtensionLoader(DataStore.class).getDefaultExtension() 69:             .remove(Constants.CONSUMER_SIDE, Integer.toString(url.getPort())); 70: }
```

---

- reconnectExecutorService
属性，重连定时任务执行器。在客户端连接服务端时，会创建后台任务，定时检查连接，若断开，会进行重连。
- 第 27 至 31 行：从 URL 中，获得重连相关**配置项**
。
- 第 33 至 41 行：调用 **抽象**
#doOpen()
方法，初始化客户端。若异常，调用
#close()
方法，进行关闭。
- 第 43 至 63 行：调用 **实现**
#connect()
方法，连接服务器。若异常，调用
#close()
方法，进行关闭。
    - 第 51 至 57 行：若是连接失败 RemotingException ，若开启了 [启动时检查](http://dubbo.apache.org/zh-cn/docs/user/demos/preflight-check.html)
，则调用
#close()
方法，进行关闭。
- 第 66 至 69 行：从 [DataStore](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-common/src/main/java/com/alibaba/dubbo/common/store/DataStore.java)
中，获得线程池。
    - DataStore 在 [store](https://github.com/YunaiV/dubbo/tree/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-common/src/main/java/com/alibaba/dubbo/common/store)
dubbo-common
模块，
包下实现。目前的实现比较简单，可以认为是
ConcurrentMap<String, ConcurrentMap<String, Object>>
的集合。胖友可以自己看相关实现。
    - 此处的线程池，实际就是 [《Dubbo 用户指南 —— 线程模型》](http://dubbo.apache.org/zh-cn/docs/user/demos/thread-model.html)**线程池**[「8. Dispacher」](http://svip.iocoder.cn/Dubbo/remoting-api-transport/#)
中说的
。在
中，详细解析。

**连接服务器**

```plain text
plain /**  * 连接锁，用于实现发起连接和断开连接互斥，避免并发。  */ private final Lock connectLock = new ReentrantLock();    1: protected void connect() throws RemotingException {   2:     // 获得锁   3:     connectLock.lock();   4:     try {   5:         // 已连接，   6:         if (isConnected()) {   7:             return;   8:         }   9:         // 初始化重连线程  10:         initConnectStatusCheckCommand();  11:         // 执行连接  12:         doConnect();  13:         // 连接失败，抛出异常  14:         if (!isConnected()) {  15:             throw new RemotingException(this, "Failed connect to server " + getRemoteAddress() + " from " + getClass().getSimpleName() + " "  16:                     + NetUtils.getLocalHost() + " using dubbo version " + Version.getVersion()  17:                     + ", cause: Connect wait timeout: " + getTimeout() + "ms.");  18:         // 连接成功，打印日志  19:         } else {  20:             if (logger.isInfoEnabled()) {  21:                 logger.info("Successed connect to server " + getRemoteAddress() + " from " + getClass().getSimpleName() + " "  22:                         + NetUtils.getLocalHost() + " using dubbo version " + Version.getVersion()  23:                         + ", channel is " + this.getChannel());  24:             }  25:         }  26:         // 设置重连次数归零  27:         reconnect_count.set(0);  28:         // 设置未打印过错误日志  29:         reconnect_error_log_flag.set(false);  30:     } catch (RemotingException e) {  31:         throw e;  32:     } catch (Throwable e) {  33:         throw new RemotingException(this, "Failed connect to server " + getRemoteAddress() + " from " + getClass().getSimpleName() + " "  34:                 + NetUtils.getLocalHost() + " using dubbo version " + Version.getVersion()  35:                 + ", cause: " + e.getMessage(), e);  36:     } finally {  37:         // 释放锁  38:         connectLock.unlock();  39:     }  40: }
```

---

- 第 3 行：获得锁。在连接和断开连接时，通过锁，避免并发冲突。
- 第 5 至 8 行：调用
#isConnected()
方法，判断连接状态。若已经连接，就不重复连接。代码如下：

```plain text
plain @Override public boolean isConnected() {     Channel channel = getChannel();     return channel != null && channel.isConnected(); }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">该方法，是因为实现 Channel 接口( Client 实现 Channel 接口 )，所以需要实现的。我们可以看到，实际方法内部，调用的是 </font><font style="color:rgb(51, 51, 51);">channel</font><font style="color:rgb(51, 51, 51);"> 对象，进行判断。其它实现 Channel 的方法，也是这么处理的，例如 </font>[#getAttribute(key)](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractClient.java#L194-L245)<font style="color:rgb(51, 51, 51);"> 等方法。</font>
```

- 第 10 行：调用 **线程**
#initConnectStatusCheckCommand()
方法，初始化重连
。
    - 方法会复杂一些，不杂糅在这里讲。
- 第 14 至 17 行：连接失败，抛出异常 RemotingException 。
- 第 18 至 25 行：连接成功，打印日志。
- 第 26 至 29 行：设置重连次数归零，打印过错误日志状态为否。下面，我们会看到这些状态字段的变更。
- 第 38 行：释放锁。

**初始化重连线程**

```plain text
plain /**  * 重连次数  */ private final AtomicInteger reconnect_count = new AtomicInteger(0); /**  * 重连时，是否已经打印过错误日志。  */ // Reconnection error log has been called before? private final AtomicBoolean reconnect_error_log_flag = new AtomicBoolean(false); /**  * 重连执行任务 Future  */ private volatile ScheduledFuture<?> reconnectExecutorFuture = null; /**  * 最后成功连接时间  */ // the last successed connected time private long lastConnectedTime = System.currentTimeMillis();        1: private synchronized void initConnectStatusCheckCommand() {   2:     //reconnect=false to close reconnect   3:     // 获得获得重连频率，默认开启。   4:     int reconnect = getReconnectParam(getUrl());   5:     // 若开启重连功能，创建重连线程   6:     if (reconnect > 0 && (reconnectExecutorFuture == null || reconnectExecutorFuture.isCancelled())) {   7:         // 创建 Runnable 对象   8:         Runnable connectStatusCheckCommand = new Runnable() {   9:             public void run() {  10:                 try {  11:                     // 未连接，重连  12:                     if (!isConnected()) {  13:                         connect();  14:                     // 已连接，记录最后连接时间  15:                     } else {  16:                         lastConnectedTime = System.currentTimeMillis();  17:                     }  18:                 } catch (Throwable t) {  19:                     // 超过一定时间未连接上，才打印异常日志。并且，仅打印一次。默认，15 分钟。  20:                     String errorMsg = "client reconnect to " + getUrl().getAddress() + " find error . url: " + getUrl();  21:                     // wait registry sync provider list  22:                     if (System.currentTimeMillis() - lastConnectedTime > shutdown_timeout) {  23:                         if (!reconnect_error_log_flag.get()) {  24:                             reconnect_error_log_flag.set(true);  25:                             logger.error(errorMsg, t);  26:                             return;  27:                         }  28:                     }  29:                     // 每一定次发现未重连，才打印告警日志。默认，1800 次，1 小时。  30:                     if (reconnect_count.getAndIncrement() % reconnect_warning_period == 0) {  31:                         logger.warn(errorMsg, t);  32:                     }  33:                 }  34:             }  35:         };  36:         // 发起定时任务  37:         reconnectExecutorFuture = reconnectExecutorService.scheduleWithFixedDelay(connectStatusCheckCommand, reconnect, reconnect, TimeUnit.MILLISECONDS);  38:     }  39: }
```

---

- 第 4 行：调用 [#getReconnectParam(url)](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractClient.java#L120-L142)
方法，获得重连频率。默认开启，2000 毫秒。
    - 代码比较简单，胖友自己点击方法查看。
- 第 6 至 38 行：若**开启**
重连功能， 创建重连线程。
    - 第 8 至 35 行：创建 Runnable 对象。
        - 第 11 至 13 行：未连接时，调用
#connect()
方法，进行重连。
        - 第 14 至 17 行：已连接时，记录最后连接时间。
        - 第 18 至 33 行：**符合错误告警**
条件时，打印
或
日志。为什么要符合条件才打印呢？之前也和朋友聊起来过，线上因为中间件组件，打印了太多的日志，结果整个 JVM 崩了。特别在网络场景 + 大量“无限”重试的场景，特别容易打出满屏的日志。这块，我们可以学习下。另外，Eureka 在集群同步，也有类似处理。
    - 第 36 行：发起任务，**定时**
检查，是否需要重连。
- reconnect=false to close reconnect
，从目前代码上来看，未实现
#reset(url)
方法，在 URL 的
reconnect=false
配置项时，关闭重连线程。

**发送消息**

```plain text
plain @Override public void send(Object message, boolean sent) throws RemotingException {     // 未连接时，开启重连功能，则先发起连接     if (send_reconnect && !isConnected()) {         connect();     }     // 发送消息     Channel channel = getChannel();     //TODO Can the value returned by getChannel() be null? need improvement.     if (channel == null || !channel.isConnected()) {         throw new RemotingException(this, "message can not send, because channel is closed . url:" + getUrl());     }     channel.send(message, sent); }
```

---

**包装通道处理器**

```plain text
plain // Constants.java public static final String DEFAULT_CLIENT_THREADPOOL = "cached";  protected static final String CLIENT_THREAD_POOL_NAME = "DubboClientHandler";    1: /**   2:  * 包装通道处理器   3:  *   4:  * @param url URL   5:  * @param handler 被包装的通道处理器   6:  * @return 包装后的通道处理器   7:  */   8: protected static ChannelHandler wrapChannelHandler(URL url, ChannelHandler handler) {   9:     // 设置线程名  10:     url = ExecutorUtil.setThreadName(url, CLIENT_THREAD_POOL_NAME);  11:     // 设置使用的线程池类型  12:     url = url.addParameterIfAbsent(Constants.THREADPOOL_KEY, Constants.DEFAULT_CLIENT_THREADPOOL);  13:     // 包装通道处理器  14:     return ChannelHandlers.wrap(handler, url);  15: }
```

---

- 第 10 行：调用 **线程名**
ExecutorUtil#setThreadName(url, CLIENT_THREAD_POOL_NAME)
方法，设置
，即
URL.threadname=xxx
。代码如下：

```plain text
plain public static URL setThreadName(URL url, String defaultName) {     String name = url.getParameter(Constants.THREAD_NAME_KEY, defaultName);     name = new StringBuilder(32).append(name).append("-").append(url.getAddress()).toString();     url = url.addParameter(Constants.THREAD_NAME_KEY, name);     return url; }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">注意，线程名中，包含 </font>**<font style="color:rgb(51, 51, 51);">URL 的地址信息</font>**<font style="color:rgb(51, 51, 51);">。</font>
```

- 第 12 行：设置**线程类型**
，即
URL.threadpool=xxx
。默认情况下，使用
“cached”
类型，这个和 Server 是不同的，下面我们会看到。
    - [《精尽 Dubbo 源码分析 —— 线程池》](http://svip.iocoder.cn/Dubbo/thread-pool/?self=)
- 第 14 行：调用 [「8. Dispacher」](http://svip.iocoder.cn/Dubbo/remoting-api-transport/#)
ChannelHandlers#wrap(handler, url)
方法，包装通道处理器。这里我们不细说，在
中，结合解析。
- 这是一个非常关键的方法，在例如 NettyClient 等里，都会调用该方法。

**其他方法**

如下方法比较简单，艿艿就不重复啰嗦了。

- [#disconnect()](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractClient.java#L291-L311)
方法，断开连接。
- [#reconnect()](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractClient.java#L313-L316)
方法，主动重连。
- [#close()](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractClient.java#L318-L341)
方法，强制关闭。
- [#close(timeout)](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractClient.java#L343-L346)
方法，优雅关闭。

**子类类图**

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/bffacd2603a103238426b398ed38afd9.png)

类图

## 3.2 ClientDelegate

[com.alibaba.dubbo.remoting.transport.ClientDelegate](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ClientDelegate.java) ，实现 Client 接口，客户端装饰者实现类。在每个实现的方法里，直接调用被装饰的 [client](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ClientDelegate.java#L31) 属性的方法。

目前 dubbo-rpc-default 模块中，[ChannelWrapper](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-rpc/dubbo-rpc-default/src/main/java/com/alibaba/dubbo/rpc/protocol/dubbo/ChannelWrappedInvoker.java#L91-L160) 继承了 ClientDelegate 类。但实际上，ChannelWrapper **重新实现了所有的方法**，并且，并未复用任何方法。所以，ClientDelegate 目前用途不大。

# 4. Server

## 4.1 AbstractServer

[com.alibaba.dubbo.remoting.transport.AbstractServer](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractServer.java) ，实现 Server 接口，继承 AbstractEndpoint 抽象类，**服务器**抽象类，**重点**实现了公用的逻辑，同时抽象了开启、关闭等模板方法，供子类实现。抽象方法如下：

```plain text
plain protected abstract void doOpen() throws Throwable;  protected abstract void doClose() throws Throwable;
```

---

**构造方法**

```plain text
plain 1: /**  2:  * 线程池  3:  */  4: ExecutorService executor;  5: /**  6:  * 服务地址  7:  */  8: private InetSocketAddress localAddress;  9: /** 10:  * 绑定地址 11:  */ 12: private InetSocketAddress bindAddress; 13: /** 14:  * 服务器最大可接受连接数 15:  */ 16: private int accepts; 17: /** 18:  * 空闲超时时间，单位：毫秒 19:  */ 20: private int idleTimeout; //600 seconds 21:  22: public AbstractServer(URL url, ChannelHandler handler) throws RemotingException { 23:     super(url, handler); 24:     // 服务地址 25:     localAddress = getUrl().toInetSocketAddress(); 26:     // 绑定地址 27:     String bindIp = getUrl().getParameter(Constants.BIND_IP_KEY, getUrl().getHost()); 28:     int bindPort = getUrl().getParameter(Constants.BIND_PORT_KEY, getUrl().getPort()); 29:     if (url.getParameter(Constants.ANYHOST_KEY, false) || NetUtils.isInvalidLocalHost(bindIp)) { 30:         bindIp = NetUtils.ANYHOST; 31:     } 32:     bindAddress = new InetSocketAddress(bindIp, bindPort); 33:     // 服务器最大可接受连接数 34:     this.accepts = url.getParameter(Constants.ACCEPTS_KEY, Constants.DEFAULT_ACCEPTS); 35:     // 空闲超时时间 36:     this.idleTimeout = url.getParameter(Constants.IDLE_TIMEOUT_KEY, Constants.DEFAULT_IDLE_TIMEOUT); 37:  38:     // 开启服务器 39:     try { 40:         doOpen(); 41:         if (logger.isInfoEnabled()) { 42:             logger.info("Start " + getClass().getSimpleName() + " bind " + getBindAddress() + ", export " + getLocalAddress()); 43:         } 44:     } catch (Throwable t) { 45:         throw new RemotingException(url.toInetSocketAddress(), null, "Failed to bind " + getClass().getSimpleName() 46:                 + " on " + getLocalAddress() + ", cause: " + t.getMessage(), t); 47:     } 48:  49:     // 获得线程池 50:     //fixme replace this with better method 51:     DataStore dataStore = ExtensionLoader.getExtensionLoader(DataStore.class).getDefaultExtension(); 52:     executor = (ExecutorService) dataStore.get(Constants.EXECUTOR_SERVICE_COMPONENT_KEY, Integer.toString(url.getPort())); 53: }
```

---

- 第 24 至 36 行：从 URL 中，加载
localAddress
bindAddress
accepts
idleTimeout
配置项。比较难理解的，可能是两个地址属性，如下是比例提供的一个例子：
![](/assets/images/learning/dubbo/dubbo-nio-server-transport/2fdd09a2501dea83c3aa5de34cf4d482.png)
例子
    - 配置项可在 [#reset(url)](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractServer.java#L80-L129)
方法中，重置属性。
- 第 38 至 47 行：调用
#doOpen()
方法，开启服务器。
- 第 49 至 52 行：从 [DataStore](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-common/src/main/java/com/alibaba/dubbo/common/store/DataStore.java)
中，获得线程池。
    - fixme replace this with better method**官方**
，说明
在这块实现上，也不是很满意，后面会优化掉。

**被客户端连接**

```plain text
plain @Override public void connected(Channel ch) throws RemotingException {     // If the server has entered the shutdown process, reject any new connection     if (this.isClosing() || this.isClosed()) {         logger.warn("Close new channel " + ch + ", cause: server is closing or has been closed. For example, receive a new connect request while in shutdown process.");         ch.close();         return;     }      // 超过上限，关闭新的链接     Collection<Channel> channels = getChannels();     if (accepts > 0 && channels.size() > accepts) {         logger.error("Close channel " + ch + ", cause: The server " + ch.getLocalAddress() + " connections greater than max config " + accepts);         ch.close(); // 关闭新的链接         return;     }     // 连接     super.connected(ch); }
```

---

**发送消息**

```plain text
plain @Override public void send(Object message, boolean sent) throws RemotingException {     // 获得所有的客户端的通道     Collection<Channel> channels = getChannels();     // 群发消息     for (Channel channel : channels) {         if (channel.isConnected()) {             channel.send(message, sent);         }     } }
```

---

**其他方法**

如下方法比较简单，艿艿就不重复啰嗦了。

- [#disconnect()](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractServer.java#L196-L203)
方法，断开连接。
- [#close()](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractServer.java#L140-L155)
方法，强制关闭。
- [#close(timeout)](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractServer.java#L157-L160)
方法，优雅关闭。

**子类类图**

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/9f1105bb5b20d5b0830f89e5575ba799.png)

类图

## 4.2 ServerDelegate

[com.alibaba.dubbo.remoting.transport.ServerDelegate](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ServerDelegate.java) ，实现 Client 接口，客户端装饰者实现类。在每个实现的方法里，直接调用被装饰的 [server](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ServerDelegate.java#L35) 属性的方法。

目前 dubbo-remoting-p2p 模块中，PeerServer 会继承该类，后续再看。

# 5. Channel

## 5.1 AbstractChannel

[com.alibaba.dubbo.remoting.transport.AbstractChannel](https://github.com/YunaiV/dubbo/blob/4fa80f25673c4e7060847a711a87ea37ed152d91/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractChannel.java) ，实现 Channel 接口，实现 AbstractPeer 抽象类，**通道**抽象类。

**发送消息**

```plain text
plain @Override public void send(Object message, boolean sent) throws RemotingException {     if (isClosed()) {         throw new RemotingException(this, "Failed to send message "                 + (message == null ? "" : message.getClass().getName()) + ":" + message                 + ", cause: Channel closed. channel: " + getLocalAddress() + " -> " + getRemoteAddress());     } }
```

---

- 具体的发送方法，子类实现。在 AbstractChannel 中，目前只做状态检查。

**子类类图**

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/c97c05aca83b5eb2e04929bcbb4b9b44.png)

类图

## 5.2 ChannelDelegate

[com.alibaba.dubbo.remoting.transport.ChannelDelegate](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ChannelDelegate.java) ，实现 Channel 接口，通道装饰者实现类。在每个实现的方法里，直接调用被装饰的 [channel](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ChannelDelegate.java#L31) 属性的方法。

目前 Dubbo 中，暂未用到。

# 7. ChannelHandler

## 7.1 ChannelHandlerAdapter

com.alibaba.dubbo.remoting.transport.ChannelHandlerAdapter ，实现 ChannelHandler 接口，通道处理器**适配器**，每个方法为空实现。代码如下：

```plain text
plain @Override public void connected(Channel channel) throws RemotingException { }  @Override public void disconnected(Channel channel) throws RemotingException { }  @Override public void sent(Channel channel, Object message) { }  @Override public void received(Channel channel, Object message) throws RemotingException { }  @Override public void caught(Channel channel, Throwable exception) throws RemotingException { }
```

---

子类，可继承它，**仅实现**想要的方法。

## 7.2 ChannelHandlerDispatcher

com.alibaba.dubbo.remoting.transport.ChannelHandlerDispatcher ，实现 ChannelHandler 接口，通道处理器**调度器**。在它内部，有一个通道处理器数组 [channelHandlers](https://github.com/YunaiV/dubbo/blob/4fa80f25673c4e7060847a711a87ea37ed152d91/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ChannelHandlerDispatcher.java#L35) 属性。

每个实现的方法，都会循环调用 channelHandlers 的方法，例如：

```plain text
plain public void received(Channel channel, Object message) {     for (ChannelHandler listener : channelHandlers) {         try {             listener.received(channel, message);         } catch (Throwable t) {             logger.error(t.getMessage(), t);         }     } }
```

---

搜索了下 ChannelHandlerDispatcher 的使用情况，主要用在 dubbo-remoting-p2p 的 AbstractGroup 中。

## 7.3 ChannelHandlerDelegate

com.alibaba.dubbo.remoting.transport.ChannelHandlerDelegate ，实现 ChannelHandler 接口，通道处理器**装饰者**接口。方法如下：

```plain text
plain ChannelHandler getHandler();
```

---

正如，我们在上文中说道，**装饰器模式**，在 dubbo-remoting-api 扮演了非常重要的角色，那么最佳演员就是 ChannelHandlerDelegate 们。下面，开始他们的表演。

### 7.3.1 AbstractChannelHandlerDelegate

[com.alibaba.dubbo.remoting.transport.AbstractChannelHandlerDelegate](https://github.com/YunaiV/dubbo/blob/4fa80f25673c4e7060847a711a87ea37ed152d91/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractChannelHandlerDelegate.java) ，实现 ChannelHandlerDelegate 接口，通道处理器装饰者**抽象实现类**。在每个实现的方法里，直接调用被装饰的 [handler](https://github.com/YunaiV/dubbo/blob/4fa80f25673c4e7060847a711a87ea37ed152d91/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractChannelHandlerDelegate.java#L26) 属性的方法。

### 7.3.2 DecodeHandler

com.alibaba.dubbo.remoting.transport.DecodeHandler ，实现 AbstractChannelHandlerDelegate 抽象类，**解码处理器**，处理接收到的消息，实现了 Decodeable 接口的情况。

**覆写了 #received(channel, message) 方法**

```plain text
plain 1: @Override  2: public void received(Channel channel, Object message) throws RemotingException {  3:     if (message instanceof Decodeable) {  4:         decode(message);  5:     }  6:   7:     if (message instanceof Request) {  8:         decode(((Request) message).getData());  9:     } 10:  11:     if (message instanceof Response) { 12:         decode(((Response) message).getResult()); 13:     } 14:  15:     handler.received(channel, message); 16: }
```

---

- 第 3 至 5 行：当消息是 Decodeable 类型时，调用
#decode(message)
方法，解析消息。
- 第 7 至 9 行：当消息是 Request 类型时，调用
#decode(message)
方法，解析
data
属性。
- 第 11 至 13 行：当消息是 Response 类型时，调用
#decode(message)
方法，解析
result
属性。
- 第 15 行：调用
ChannelHandler#received(channel, message)
方法，将消息交给委托的
handler
，继续处理。 胖友是否感受到，装饰器模式的好处：通过组合的方式，实现功能的叠加。

**解析消息**

```plain text
plain 1: private void decode(Object message) {  2:     if (message != null && message instanceof Decodeable) {  3:         try {  4:             ((Decodeable) message).decode(); // 解析消息  5:             if (log.isDebugEnabled()) {  6:                 log.debug(new StringBuilder(32).append("Decode decodeable message ").append(message.getClass().getName()).toString());  7:             }  8:         } catch (Throwable e) {  9:             if (log.isWarnEnabled()) { 10:                 log.warn(new StringBuilder(32).append("Call Decodeable.decode failed: ").append(e.getMessage()).toString(), e); 11:             } 12:         } // ~ end of catch 13:     } // ~ end of if 14: } // ~ end of method decode
```

---

- 第 2 至 4 行：当类型是 Decodeable 时，调用
Decodeable#decode()
方法，进一步解析。
- 在
dubbo-rpc-default
项目中，DecodeableRpcInvocation 和 DecodeableRpcResult 实现 Decodeable 接口，后面我们来分享。

### 7.3.3 MultiMessageHandler

`com.alibaba.dubbo.remoting.transport.MultiMessageHandler ，实现 AbstractChannelHandlerDelegate 抽象类，**多消息处理器**，处理一次性接收到多条消息的情况。

**覆写了 #received(channel, message) 方法**

```plain text
plain 1: @Override  2: public void received(Channel channel, Object message) throws RemotingException {  3:     if (message instanceof MultiMessage) { // 多消息  4:         MultiMessage list = (MultiMessage) message;  5:         for (Object obj : list) {  6:             handler.received(channel, obj);  7:         }  8:     } else {  9:         handler.received(channel, message); 10:     } 11: }
```

---

- 第 3 至 7 行：当消息是 MultiMessage 类型，即**多消息循环**
，
提交给
handler
处理。
- 第 8 至 10 行：当**单消息直接**
时，
提交给
handler
处理。

---

在下面的文章，我们可以看到 ChannelHandlerDelegate 的**组合使用的例子**。

# 8. Dispacher

本小节内容，对应 [《Dubbo 用户指南 —— 线程模型》](http://dubbo.apache.org/zh-cn/docs/user/demos/thread-model.html) 。

简单概括这节，以**接收消息**举例子，代码如下：

```plain text
plain executor.execute(new Runnable() {     handler.received(channel, message) });
```

---

将 ChannelHandler 的具体操作，调度到线程池中，这也是为什么这个模块叫 dispacher 的原因。

## 8.1 ChannelHandlers

com.alibaba.dubbo.remoting.transport.dispatcher.ChannelHandlers ，通道处理器**工厂**。在上文 [「3.1 AbstractClient」](http://svip.iocoder.cn/Dubbo/remoting-api-transport/#) ，我们看到 AbstractClient#wrapChannelHandler(url, handler) 方法中，会调用 ChannelHandlers#wrap(url, handler) 方法。实际上，Server 部分也会有这样类似的逻辑，只是代码实现上暂未统一。以 dubbo-remoting-netty4 来举例子：

- NettyClient ：

```plain text
plain public NettyClient(final URL url, final ChannelHandler handler) throws RemotingException {     super(url, wrapChannelHandler(url, handler)); }
```

---

- NettyServer ：

```plain text
plain public NettyServer(URL url, ChannelHandler handler) throws RemotingException {     super(url, ChannelHandlers.wrap(handler, ExecutorUtil.setThreadName(url, SERVER_THREAD_POOL_NAME) /* 设置线程名到 URL 上 */)); }
```

---

无论 Client 还是 Server ，都是类似的，将传入的 handler ，最终使用 ChannelHandlers 进行一次包装。OK ，我们来看看包装通道处理器的具体代码：

```plain text
plain 1: /**  2:  * 单例  3:  */  4: private static ChannelHandlers INSTANCE = new ChannelHandlers();  5:   6: public static ChannelHandler wrap(ChannelHandler handler, URL url) {  7:     return ChannelHandlers.getInstance().wrapInternal(handler, url);  8: }  9:  10: protected ChannelHandler wrapInternal(ChannelHandler handler, URL url) { 11:     return new MultiMessageHandler( 12:             new HeartbeatHandler( 13:                     ExtensionLoader.getExtensionLoader(Dispatcher.class).getAdaptiveExtension().dispatch(handler, url) 14:             ) 15:     ); 16: }
```

---

- 第 11 至 15 行：在这里，我们就看到了多个 ChannelHandlerDelegate 的组合。包括，第 15 行的，**返回**
Dispatcher#dispatch(handler, url)
方法，实际上也是
一个 ChannelHandlerDelegate 对象。

## 8.2 Dispatcher 实现类

在 Dubbo 中，有多种 Dispatcher 的实现，如下：

FROM [《Dubbo 用户指南 —— 线程模型》](http://dubbo.apache.org/zh-cn/docs/user/demos/thread-model.html)

- all
所有消息都派发到线程池，包括请求，响应，连接事件，断开事件，心跳等。
- direct
所有消息都不派发到线程池，全部在 IO 线程上直接执行。
- message
只有请求响应消息派发到线程池，其它连接断开事件，心跳等消息，直接在 IO 线程上执行。
- execution
只请求消息派发到线程池，不含响应，响应和其它连接断开事件，心跳等消息，直接在 IO 线程上执行。
- connection
在 IO 线程上，将连接断开事件放入队列，有序逐个执行，其它消息派发到线程池。

**子类类图**

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/a683269f616c18e47c202302f7aaaf15.png)

类图

### 8.2.1 AllDispatcher

我们以 all 对应的 AllDispatcher 举例子，代码如下：

```plain text
plain public class AllDispatcher implements Dispatcher {      public static final String NAME = "all";      public ChannelHandler dispatch(ChannelHandler handler, URL url) {         return new AllChannelHandler(handler, url);     }  }
```

---

在该类的 #dispatch(…) 的方法中，我们可以看到创建 AllChannelHandler 对象，并传入 handler 属性。 聪慧如你，已经猜到 AllChannelHandler 也是 ChannelHandlerDelegate 类型。也就是说“**线程模型**”，也是通过**装饰器模式**，组合而成。

每个 Dispatcher 实现类，都对应一个 ChannelHandler 实现类。默认**未配置**的情况下，使用 AllDispatcher 调度。

### 8.2.2 AllChannelHandler

[com.alibaba.dubbo.remoting.transport.dispatcher.all.AllChannelHandler](http://svip.iocoder.cn/Dubbo/remoting-api-transport/com.alibaba.dubbo.remoting.transport.dispatcher.all) ，实现 WrappedChannelHandler 抽象类。覆写 #connected(channel) 方法如下：

WrappedChannelHandler 是实现 ChannelHandlerDelegate 的抽象类，下文再看。

```plain text
plain @Override public void connected(Channel channel) throws RemotingException {     ExecutorService cexecutor = getExecutorService();     try {         cexecutor.execute(new ChannelEventRunnable(channel, handler, ChannelState.CONNECTED));     } catch (Throwable t) {         throw new ExecutionException("connect event", channel, getClass() + " error when process connected event .", t);     } }
```

---

- 创建 ChannelEventRunnable 对象，提交给线程池执行。
- 注意，传入的状态为
ChannelState.CONNECTED
。不同的实现方法，对应不同的状态。

## 8.3 ChannelEventRunnable

[com.alibaba.dubbo.remoting.transport.dispatcher.ChannelEventRunnable](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/dispatcher/ChannelEventRunnable.java) ，实现 Runnable 接口。代码比较简单，胖友自己看噢。主要分成三部分：

- [构造方法](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/dispatcher/ChannelEventRunnable.java#L27-L51)
- [ChannelState](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/dispatcher/ChannelEventRunnable.java#L98-L129)
- [#run()](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/dispatcher/ChannelEventRunnable.java#L53-L96)
方法，简化代码如下：

```plain text
plain @Override public void run() {     switch (state) {         case CONNECTED: handler.connected(channel); break;         case DISCONNECTED:handler.disconnected(channel); break;         case SENT:handler.sent(channel, message);break;         case RECEIVED:handler.received(channel, message);break;         case CAUGHT:handler.caught(channel, exception);break;         default: logger.warn("unknown state: " + state + ", message is " + message);     } }
```

---

## 8.4 WrappedChannelHandler

com.alibaba.dubbo.remoting.transport.dispatcher.WrappedChannelHandler ，实现 ChannelHandlerDelegate 接口，**包装的** WrappedChannelHandler 实现类。

从目前的实现来看，WrappedChannelHandler 继承 AbstractChannelHandlerDelegate 更合适，因为 #connected(channel) 等，实现的方法都是相同的。

**构造方法**

```plain text
plain 1: /**  2:  * 线程池  3:  */  4: protected final ExecutorService executor;  5: /**  6:  * 通道处理器  7:  */  8: protected final ChannelHandler handler;  9: /** 10:  * URL 11:  */ 12: protected final URL url; 13:  14: public WrappedChannelHandler(ChannelHandler handler, URL url) { 15:     this.handler = handler; 16:     this.url = url; 17:  18:     // 创建线程池 19:     executor = (ExecutorService) ExtensionLoader.getExtensionLoader(ThreadPool.class).getAdaptiveExtension().getExecutor(url); 20:  21:     // 添加线程池到 DataStore 中 22:     String componentKey = Constants.EXECUTOR_SERVICE_COMPONENT_KEY; 23:     if (Constants.CONSUMER_SIDE.equalsIgnoreCase(url.getParameter(Constants.SIDE_KEY))) { 24:         componentKey = Constants.CONSUMER_SIDE; 25:     } 26:     DataStore dataStore = ExtensionLoader.getExtensionLoader(DataStore.class).getDefaultExtension(); 27:     dataStore.put(componentKey, Integer.toString(url.getPort()), executor); 28: }
```

---

- 第 19 行：基于 Dubbo SPI Adaptive 机制，创建线程池。
- 第 21 至 27 行：添加线程池到 DataStore 中。 这就是上文 AbstractClient 或 AbstractServer 从 DataStore 获得线程池的**方式**
。当然，官方也说了，这种方式不是很优雅，有点奇淫技巧，未来会优化掉。

**共享线程池**

在 WrappedChannelHandler 中，有一个内置的共享线程池，如下：

```plain text
plain protected static final ExecutorService SHARED_EXECUTOR = Executors.newCachedThreadPool(new NamedThreadFactory("DubboSharedHandler", true));
```

---

【TODO 8024】搞不懂，这个设计的意图，先mark留着。

**子类类图**

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/00752335eee5e78bc61ea1d2c4e24819.png)

类图

# 9. Codec

## 9.1 CodecSupport

com.alibaba.dubbo.remoting.transport.CodecSupport ，编解码工具类，提供查询 Serialization 的功能。

**初始化**

```plain text
plain /**  * 序列化对象集合  * key：序列化类型编号 {@link Serialization#getContentTypeId()}  */ private static Map<Byte, Serialization> ID_SERIALIZATION_MAP = new HashMap<Byte, Serialization>(); /**  * 序列化名集合  * key：序列化类型编号 {@link Serialization#getContentTypeId()}  * value: 序列化拓展名  */ private static Map<Byte, String> ID_SERIALIZATIONNAME_MAP = new HashMap<Byte, String>();  static {     // 基于 Dubbo SPI ，初始化     Set<String> supportedExtensions = ExtensionLoader.getExtensionLoader(Serialization.class).getSupportedExtensions();     for (String name : supportedExtensions) {         Serialization serialization = ExtensionLoader.getExtensionLoader(Serialization.class).getExtension(name);         byte idByte = serialization.getContentTypeId();         if (ID_SERIALIZATION_MAP.containsKey(idByte)) {             logger.error("Serialization extension " + serialization.getClass().getName()                     + " has duplicate id to Serialization extension "                     + ID_SERIALIZATION_MAP.get(idByte).getClass().getName()                     + ", ignore this Serialization extension");             continue;         }         ID_SERIALIZATION_MAP.put(idByte, serialization);         ID_SERIALIZATIONNAME_MAP.put(idByte, name);     } }
```

---

Dubbo 提供了多种序列化方式，此处初始化结果，如下图：

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/b14d716ce7dc08c9c6bb22002d039b06.png)

SERIALIZATION 集合

**查找 Serialization 对象**

```plain text
plain public static Serialization getSerialization(URL url, Byte id) throws IOException {     Serialization serialization = getSerializationById(id);     String serializationName = url.getParameter(Constants.SERIALIZATION_KEY, Constants.DEFAULT_REMOTING_SERIALIZATION); // 默认，hessian2     // 出于安全的目的，针对 JDK 的序列化方式（对应编号为 3、4、7），检查连接到服务器的 URL 和实际传输的数据，协议是否一致。     // https://github.com/apache/incubator-dubbo/issues/1138     // Check if "serialization id" passed from network matches the id on this side(only take effect for JDK serialization), for security purpose.     if (serialization == null             || ((id == 3 || id == 7 || id == 4) && !(serializationName.equals(ID_SERIALIZATIONNAME_MAP.get(id))))) {         throw new IOException("Unexpected serialization id:" + id + " received from network, please check if the peer send the right id.");     }     return serialization; }
```

---

在最新的 Dubbo 版本中，已经将 serialization 模块，从 dubbo-common 中，独立成 [dubbo-serialization](https://github.com/apache/incubator-dubbo/blob/HEAD/dubbo-serialization/pom.xml) 。So ，我们后面开一个系列来分享。

## 9.2 AbstractCodec

com.alibaba.dubbo.remoting.transport.AbstractCodec ，实现 Codec**2** 接口，提供如下公用方法：

- [#checkPayload(channel, size)](https://github.com/apache/incubator-dubbo/blob/05da8040e88ef5c9a544cb9dddf4c6abee6bd61a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractCodec.java#L38-L48)**静态**
方法，校验消息长度。
- [#getSerialization(channel)](https://github.com/apache/incubator-dubbo/blob/05da8040e88ef5c9a544cb9dddf4c6abee6bd61a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractCodec.java#L50-L52)
方法，获得 Serialization 对象。
- [#isClientSide(channel)](https://github.com/apache/incubator-dubbo/blob/05da8040e88ef5c9a544cb9dddf4c6abee6bd61a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractCodec.java#L54-L71)
方法，是否为客户端侧的通道。
- [#isServerSide(channel)](https://github.com/apache/incubator-dubbo/blob/05da8040e88ef5c9a544cb9dddf4c6abee6bd61a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractCodec.java#L73-L75)
方法，是否为服务端侧的通道。

**子类类图**

![](/assets/images/learning/dubbo/dubbo-nio-server-transport/250514e16a70e81b3b14644c447ec4de.png)

类图

编解码器的实现，通过**继承**的方式，获得更多的功能。每一个 Codec2 类实现对不同消息的编解码。通过**协议头**来判断，具体使用哪个编解码逻辑。听起来有点绕，我们来看一段简化 ExchangeCodec 的 #decode(…) 例子：

```plain text
plain 1: protected Object decode(Channel channel, ChannelBuffer buffer, int readable, byte[] header) throws IOException { 2:     // check magic number. 3:     if (readable > 0 && header[0] != MAGIC_HIGH 4:             || readable > 1 && header[1] != MAGIC_LOW) { 5:         // ... 省略 6:         return super.decode(channel, buffer, readable, header); 7:     } 8:     9:      // ... 省略 10:     11:     return decodeBody(channel, is, header); 12: }
```

---

- 第 2 至 7 行：通过 magic number 判断到，**并非信息交易的协议头**
Dubbo Exchange
，转交给父类 TelnetCodec 处理，一般此时是 Telnet 消息。
- 第 8 至 11 行：通过 magic number 判断到，**符合信息交易的协议头**
Dubbo Exchange
，ExchangeCodec 自己处理。

### 9.2.1 TransportCodec

com.alibaba.dubbo.remoting.transport.codec.TransportCodec ，传输编解码器，使用 Serialization 进行序列化/反序列化，直接编解码。

**编码消息**

```plain text
plain 1: @Override  2: public void encode(Channel channel, ChannelBuffer buffer, Object message) throws IOException {  3:     // 获得反序列化的 ObjectOutput 对象  4:     OutputStream output = new ChannelBufferOutputStream(buffer);  5:     ObjectOutput objectOutput = getSerialization(channel).serialize(channel.getUrl(), output);  6:     // 写入 ObjectOutput  7:     encodeData(channel, objectOutput, message);  8:     objectOutput.flushBuffer();  9:     // 释放 10:     if (objectOutput instanceof Cleanable) { 11:         ((Cleanable) objectOutput).cleanup(); 12:     } 13: }
```

---

- 第 3 至 5 行：获得对应的 Serialization 对象，并创建用于反序列化的 ObjectOutput 对象。不同的 Serialization 实现，对应不同的 ObjectOutput 实现类。 这里，我们只要读懂大体流程，详细的，我们后面文章见。
- 第 7 行：调用
#encodeData(channel, objectOutput, message)
方法，写入 ObjectOutput。代码如下：

```plain text
plain protected void encodeData(Channel channel, ObjectOutput output, Object message) throws IOException {     encodeData(output, message); }  protected void encodeData(ObjectOutput output, Object message) throws IOException {     output.writeObject(message); }
```

---

- 第 9 至 12 行：释放资源。目前，仅有
kryo
的 KryoObjectInput 、KryoObjectOutput 实现了 Cleanable 接口，需要释放资源。

**解码消息**

[#decode(channel, buffer)](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/codec/TransportCodec.java#L48-L56)**实现**方法，和解码消息基本一致，胖友自己查看。

## 9.3 CodecAdapter

[com.alibaba.dubbo.remoting.transport.codec.CodecAdapter](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/codec/CodecAdapter.java) ，实现 Code2 **接口**，Codec **适配器**，将 Codec 适配成 Codec2 。

代码比较简单，胖友自己查看。

# 666. 彩蛋

代码比较多，如果不熟悉 Netty 等框架的胖友，可能会一脸懵逼的看到文末。建议胖友结合如下的代码：

```plain text
plain // Netty.java new ChannelInitializer<NioSocketChannel>() {     @Override     protected void initChannel(NioSocketChannel ch) {         NettyCodecAdapter adapter = new NettyCodecAdapter(getCodec(), getUrl(), NettyServer.this);         ch.pipeline().addLast("decoder", adapter.getDecoder()) // 解码                     .addLast("encoder", adapter.getEncoder())  // 解码                     .addLast("handler", nettyServerHandler); // 处理器     } }
```

---

在脑补 Debug + IDE Debug ，多考虑下。

推荐阅读：

- [《Dubbo源代码实现六：线程池模型与提供者》](http://manzhizhen.iteye.com/blog/2380055)
- [《Dubbo源代码分析八：再说Provider线程池被EXHAUSTED》](http://manzhizhen.iteye.com/blog/2391177)
