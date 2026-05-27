---
layout: post
title: NIO服务器（四）之Exchange层
slug: dubbo-nio-server-exchange
type:
- note
date: 2022-05-29
status: draft
tags:
- Dubbo
categories:
- Learning
- Dubbo
mood: null
weather: null
author: deathwhispers
created: 2022-05-29 11:49
updated: 2022-05-29 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文接 [《精尽 Dubbo 源码分析 —— NIO 服务器（三）之 Telnet 层》](http://svip.iocoder.cn/Dubbo/remoting-api-telnet//?self=) 一文，分享 dubbo-remoting-api 模块， exchange 包，**信息交换层**。

**exchange** 信息交换层：封装请求响应模式，同步转异步，以 Request, Response 为中心，扩展接口为 Exchanger, ExchangeChannel, ExchangeClient, ExchangeServer。

在一次 RPC 调用，每个**请求**( Request )，是关注对应的**响应**( Response )。那么 **transport 层** 提供的**网络传输** 功能，是无法满足 RPC 的诉求的。因此，**exchange 层**，在其 **Message** 之上，构造了**Request-Response** 的模型。

实现上，也非常简单，将 Message 分成 Request 和 Response 两种类型，并增加**编号**属性，将 Request 和 Response 能够**一一映射**。

实际上，RPC 调用，会有更多特性的需求：1）**异步**处理返回结果；2）内置事件；3）等等。因此，Request 和 Response 上会有类似**编号**的**系统字段**。

一条消息，我们分成两段：

- 协议头( Header ) ： 系统字段，例如编号等。
- 内容( Body ) ：具体请求的参数和响应的结果等。

胖友在看下面这张图，是否就亲切多了 ：

![](/assets/images/learning/dubbo/dubbo-nio-server-exchange/560ea52f313f12fe4d284b496572df56.png)

类图

所以，exchange 包，很多的代码，是在 Header 的处理。OK ，下面我们来看下这个包的**类图**：

![](/assets/images/learning/dubbo/dubbo-nio-server-exchange/52573eca8be7ed14452ca33b22b94ad1.png)

类图

- 白色部分，为通用接口和
transport
包下的类。
- 蓝色部分，为
exchange
包下的类。

在 [《精尽 Dubbo 源码分析 —— NIO 服务器（二）之 Transport 层》](http://svip.iocoder.cn/Dubbo/remoting-api-transport/?self=) 中，我们提到，**装饰器设计模式**，是 dubbo-remoting 项目，最核心的实现方式，所以，exchange 其实是在 transport 上的**装饰**，提供给 dubbo-rpc 项目使用。

下面，我们来看具体代码实现。

# 2. ExchangeChannel

com.alibaba.dubbo.remoting.exchange.ExchangeChannel ，继承 Channel 接口，**信息交换通道**接口。方法如下：

```plain text
plain // 发送请求 ResponseFuture request(Object request) throws RemotingException; ResponseFuture request(Object request, int timeout) throws RemotingException;  // 获得信息交换处理器 ExchangeHandler getExchangeHandler();  // 优雅关闭 void close(int timeout);
```

---

## 2.1 HeaderExchangeChannel

com.alibaba.dubbo.remoting.exchange.support.header.HeaderExchangeChannel ，实现 ExchangeChannel 接口，基于**消息头部( Header )**的信息交换通道实现类。

### 2.1.1 构造方法

```plain text
plain private static final String CHANNEL_KEY = HeaderExchangeChannel.class.getName() + ".CHANNEL";  /**  * 通道  */ private final Channel channel; /**  * 是否关闭  */ private volatile boolean closed = false;  HeaderExchangeChannel(Channel channel) {     if (channel == null) {         throw new IllegalArgumentException("channel == null");     }     this.channel = channel; }
```

---

- channel**装饰器**
属性，通道。HeaderExchangeChannel 是传入
channel
属性的
，每个实现的方法，都会调用
channel
。如下是该属性的一个例子：
![](/assets/images/learning/dubbo/dubbo-nio-server-exchange/e6b64a0a49f676cf5460fb565cdf57ae.png)
`channel`
- #getOrAddChannel(Channel)**静态**
方法，创建 HeaderExchangeChannel 对象。代码如下：

```plain text
plain static HeaderExchangeChannel getOrAddChannel(Channel ch) {     if (ch == null) {         return null;     }     HeaderExchangeChannel ret = (HeaderExchangeChannel) ch.getAttribute(CHANNEL_KEY);     if (ret == null) {         ret = new HeaderExchangeChannel(ch);         if (ch.isConnected()) { // 已连接             ch.setAttribute(CHANNEL_KEY, ret);         }     }     return ret; }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">传入的 </font><font style="color:rgb(51, 51, 51);">ch</font><font style="color:rgb(51, 51, 51);"> 属性，实际就是 </font><font style="color:rgb(51, 51, 51);">HeaderExchangeChanel.channel</font><font style="color:rgb(51, 51, 51);"> 属性。</font>
- <font style="color:rgb(51, 51, 51);">通过 </font><font style="color:rgb(51, 51, 51);">ch.attribute</font><font style="color:rgb(51, 51, 51);"> 的 </font><font style="color:rgb(51, 51, 51);">CHANNEL_KEY</font><font style="color:rgb(51, 51, 51);"> 键值，保证有且仅有为 </font><font style="color:rgb(51, 51, 51);">ch</font><font style="color:rgb(51, 51, 51);"> 属性，创建唯一的 HeaderExchangeChannel 对象。</font>
- <font style="color:rgb(51, 51, 51);">要求</font>**<font style="color:rgb(51, 51, 51);">已连接</font>**<font style="color:rgb(51, 51, 51);">。</font>
```

- #removeChannelIfDisconnected(ch)**静态方法**
，移除 HeaderExchangeChannel 对象。代码如下：

```plain text
plain static void removeChannelIfDisconnected(Channel ch) {     if (ch != null && !ch.isConnected()) { // 未连接         ch.removeAttribute(CHANNEL_KEY);     } }
```

---

### 2.1.2 发送请求

```plain text
plain 1: @Override  2: public ResponseFuture request(Object request, int timeout) throws RemotingException {  3:     if (closed) {  4:         throw new RemotingException(this.getLocalAddress(), null, "Failed to send request " + request + ", cause: The channel " + this + " is closed!");  5:     }  6:     // create request. 创建请求  7:     Request req = new Request();  8:     req.setVersion("2.0.0");  9:     req.setTwoWay(true); // 需要响应 10:     req.setData(request); 11:     // 创建 DefaultFuture 对象 12:     DefaultFuture future = new DefaultFuture(channel, req, timeout); 13:     try { 14:         // 发送请求 15:         channel.send(req); 16:     } catch (RemotingException e) { // 发生异常，取消 DefaultFuture 17:         future.cancel(); 18:         throw e; 19:     } 20:     // 返回 DefaultFuture 对象 21:     return future; 22: }
```

---

- 第 3 至 5 行：若已经关闭，不再允许发起新的请求。
- 第 6 至 10 行：创建 Request 对象。其中，
twoWay = true
需要响应；
data = request
具体数据。
- 第 12 行：创建 DefaultFuture 对象。
- 第 13 至 15 行：调用
Channel#send(req)
方法，发送请求。
- 第 16 至 19 行：发生 RemotingException 异常，调用
DefaultFuture#cancel()
方法，取消。
- 第 21 行：返回 DefaultFuture 对象。从代码的形式上来说，有点类似线程池提交任务，返回 Future 对象。 看到 DefaultFuture 的具体代码，我们就会更加理解了。

### 2.1.3 优雅关闭

```plain text
plain 1: @Override  2: public void close(int timeout) {  3:     if (closed) {  4:         return;  5:     }  6:     closed = true;  7:     // 等待请求完成  8:     if (timeout > 0) {  9:         long start = System.currentTimeMillis(); 10:         while (DefaultFuture.hasFuture(channel) && System.currentTimeMillis() - start < timeout) { 11:             try { 12:                 Thread.sleep(10); 13:             } catch (InterruptedException e) { 14:                 logger.warn(e.getMessage(), e); 15:             } 16:         } 17:     } 18:     // 关闭通道 19:     close(); 20: }
```

---

- 第 3 至 6 行：标记 **新**
closed = true
，避免发起
的请求。
- 第 7 至 17 行：调用
DefaultFuture#hasFuture(channel)
方法，判断已发起的已经是否已经都响应了。若否，等待完成或超时。
- 第 19 行：关闭**通道**
。

**其它方法**

其它**实现**方法，主要是直接调用 channel 的方法，点击 [传送门](https://github.com/YunaiV/dubbo/blob/2a0484941defceb9a600c7f7914ada335e3186af/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/header/HeaderExchangeChannel.java) 查看代码。

# 3. ExchangeClient

com.alibaba.dubbo.remoting.exchange.ExchangeClient ，实现 Client ，ExchangeChannel 接口，**信息交换客户端**接口。

无自定义方法。

## 3.1 HeaderExchangeClient

com.alibaba.dubbo.remoting.exchange.support.header.HeaderExchangeClient ，实现 ExchangeClient 接口，基于**消息头部( Header )**的信息交换客户端实现类。

**构造方法**

```plain text
plain 1: /**  2:  * 定时器线程池  3:  */  4: private static final ScheduledThreadPoolExecutor scheduled = new ScheduledThreadPoolExecutor(2, new NamedThreadFactory("dubbo-remoting-client-heartbeat", true));  5: /**  6:  * 客户端  7:  */  8: private final Client client;  9: /** 10:  * 信息交换通道 11:  */ 12: private final ExchangeChannel channel; 13: // heartbeat timer 14: /** 15:  * 心跳定时器 16:  */ 17: private ScheduledFuture<?> heartbeatTimer; 18: /** 19:  * 是否心跳 20:  */ 21: private int heartbeat; 22: // heartbeat timeout (ms), default value is 0 , won't execute a heartbeat. 23: /** 24:  * 心跳间隔，单位：毫秒 25:  */ 26: private int heartbeatTimeout; 27:  28: public HeaderExchangeClient(Client client, boolean needHeartbeat) { 29:     if (client == null) { 30:         throw new IllegalArgumentException("client == null"); 31:     } 32:     this.client = client; 33:     // 创建 HeaderExchangeChannel 对象 34:     this.channel = new HeaderExchangeChannel(client); 35:     // 读取心跳相关配置 36:     String dubbo = client.getUrl().getParameter(Constants.DUBBO_VERSION_KEY); 37:     this.heartbeat = client.getUrl().getParameter(Constants.HEARTBEAT_KEY, dubbo != null && dubbo.startsWith("1.0.") ? Constants.DEFAULT_HEARTBEAT : 0); 38:     this.heartbeatTimeout = client.getUrl().getParameter(Constants.HEARTBEAT_TIMEOUT_KEY, heartbeat * 3); 39:     if (heartbeatTimeout < heartbeat * 2) { // 避免间隔太短 40:         throw new IllegalStateException("heartbeatTimeout < heartbeatInterval * 2"); 41:     } 42:     // 发起心跳定时器 43:     if (needHeartbeat) { 44:         startHeatbeatTimer(); 45:     } 46: }
```

---

- client
属性，客户端。如下是该属性的一个例子：
![](/assets/images/learning/dubbo/dubbo-nio-server-exchange/f0d59c0fc01a3415f9f1f02a1434dcd2.png)
`client`
- 第 34 行：使用传入的
client
属性，创建 HeaderExchangeChannel 对象。
- 第 35 至 41 行：读取心跳相关配置。**默认，开启心跳功能**[《Dubbo 用户指南 —— dubbo:protocol》](http://dubbo.apache.org/zh-cn/docs/user/references/xml/dubbo-protocol.html)
。为什么需要有心跳功能呢？
FROM
心跳间隔，对于长连接，当物理层断开时，比如拔网线，TCP的FIN消息来不及发送，对方收不到断开事件，此时需要心跳来帮助检查连接是否已断开
- 第 42 至 45 行：调用
#startHeatbeatTimer()
方法，发起心跳定时器。

**发起心跳定时器**

```plain text
plain 1: private void startHeatbeatTimer() {  2:     // 停止原有定时任务  3:     stopHeartbeatTimer();  4:     // 发起新的定时任务  5:     if (heartbeat > 0) {  6:         heartbeatTimer = scheduled.scheduleWithFixedDelay(  7:                 new HeartBeatTask(new HeartBeatTask.ChannelProvider() {  8:                     public Collection<Channel> getChannels() {  9:                         return Collections.<Channel>singletonList(HeaderExchangeClient.this); 10:                     } 11:                 }, heartbeat, heartbeatTimeout), 12:                 heartbeat, heartbeat, TimeUnit.MILLISECONDS); 13:     } 14: }
```

---

- 第 3 行：调用 [#stopHeartbeatTimer()](https://github.com/YunaiV/dubbo/blob/0f933100ad0ea81d3760d42169318904f91a45bb/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/header/HeaderExchangeClient.java#L176-L188)
方法，停止原有定时任务。
- 第 5 至 13 行：发起新的定时任务。
    - 第 7 至 11 行：创建定时任务 HeartBeatTask 对象。具体实现见下文。

**其它方法**

其它**实现**方法，主要是直接调用 channel 或 client 的方法，点击 [传送门](https://github.com/YunaiV/dubbo/blob/0f933100ad0ea81d3760d42169318904f91a45bb/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/header/HeaderExchangeClient.java) 查看代码。

# 4. ExchangeServer

com.alibaba.dubbo.remoting.exchange.ExchangeServer ，继承 Server 接口，**信息交换服务器**接口。方法如下：

```plain text
plain // 获得通道数组 Collection<ExchangeChannel> getExchangeChannels(); ExchangeChannel getExchangeChannel(InetSocketAddress remoteAddress);
```

---

## 4.1 HeaderExchangeServer

com.alibaba.dubbo.remoting.exchange.support.header.HeaderExchangeServer ，实现 ExchangeServer 接口，基于**消息头部( Header )**的信息交换服务器实现类。

代码实现上，和 HeaderExchangeChannel + HeaderExchangeClient 的综合。

### 4.1.1 构造方法

代码实现上，和 HeaderExchangeClient 的类似。

```plain text
plain /**  * 定时器线程池  */ private final ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(1, new NamedThreadFactory("dubbo-remoting-server-heartbeat", true)); /**  * 服务器  */ private final Server server; // heartbeat timer /**  * 心跳定时器  */ private ScheduledFuture<?> heatbeatTimer; /**  * 是否心跳  */ // heartbeat timeout (ms), default value is 0 , won't execute a heartbeat. private int heartbeat; /**  * 心跳间隔，单位：毫秒  */ private int heartbeatTimeout; /**  * 是否关闭  */ private AtomicBoolean closed = new AtomicBoolean(false);  public HeaderExchangeServer(Server server) {     if (server == null) {         throw new IllegalArgumentException("server == null");     }     // 读取心跳相关配置     this.server = server;     this.heartbeat = server.getUrl().getParameter(Constants.HEARTBEAT_KEY, 0);     this.heartbeatTimeout = server.getUrl().getParameter(Constants.HEARTBEAT_TIMEOUT_KEY, heartbeat * 3);     if (heartbeatTimeout < heartbeat * 2) {         throw new IllegalStateException("heartbeatTimeout < heartbeatInterval * 2");     }     // 发起心跳定时器     startHeatbeatTimer(); }
```

---

### 4.1.2 发起心跳定时器

代码实现上，和 HeaderExchangeClient 的类似。

```plain text
plain private void startHeatbeatTimer() {     // 停止原有定时任务     stopHeartbeatTimer();     // 发起新的定时任务     if (heartbeat > 0) {         heatbeatTimer = scheduled.scheduleWithFixedDelay(                 new HeartBeatTask(new HeartBeatTask.ChannelProvider() {                     public Collection<Channel> getChannels() {                         return Collections.unmodifiableCollection(HeaderExchangeServer.this.getChannels());                     }                 }, heartbeat, heartbeatTimeout),                 heartbeat, heartbeat, TimeUnit.MILLISECONDS);     } }
```

---

- 差异，Server 持有**多条多条**
Client 连接的 Channel ，所以通过 ChannelProvider 返回的是
。

### 4.1.3 重置属性

```plain text
plain @Override public void reset(URL url) {     // 重置服务器     server.reset(url);     try {         if (url.hasParameter(Constants.HEARTBEAT_KEY)                 || url.hasParameter(Constants.HEARTBEAT_TIMEOUT_KEY)) {             int h = url.getParameter(Constants.HEARTBEAT_KEY, heartbeat);             int t = url.getParameter(Constants.HEARTBEAT_TIMEOUT_KEY, h * 3);             if (t < h * 2) {                 throw new IllegalStateException("heartbeatTimeout < heartbeatInterval * 2");             }             // 重置定时任务             if (h != heartbeat || t != heartbeatTimeout) {                 heartbeat = h;                 heartbeatTimeout = t;                 startHeatbeatTimer();             }         }     } catch (Throwable t) {         logger.error(t.getMessage(), t);     } }
```

---

### 4.1.4 优雅关闭

代码实现上，和 HeaderExchangeChannel 的类似，且复杂一些。

```plain text
plain 1: @Override  2: public void close(final int timeout) {  3:     // 关闭  4:     startClose();  5:     if (timeout > 0) {  6:         final long max = (long) timeout;  7:         final long start = System.currentTimeMillis();  8:         // 发送 READONLY 事件给所有 Client ，表示 Server 不可读了。  9:         if (getUrl().getParameter(Constants.CHANNEL_SEND_READONLYEVENT_KEY, true)) { 10:             sendChannelReadOnlyEvent(); 11:         } 12:         // 等待请求完成 13:         while (HeaderExchangeServer.this.isRunning() && System.currentTimeMillis() - start < max) { 14:             try { 15:                 Thread.sleep(10); 16:             } catch (InterruptedException e) { 17:                 logger.warn(e.getMessage(), e); 18:             } 19:         } 20:     } 21:     // 关闭心跳定时器 22:     doClose(); 23:     // 关闭服务器 24:     server.close(timeout); 25: }
```

---

- Server 关闭的过程，分成**两个阶段**
：正在关闭和已经关闭。
- 第 4 行：调用
#startClose()
方法，标记正在关闭。代码如下：

```plain text
plain @Override public void startClose() {     server.startClose(); }  // AbstractPeer.java @Override public void startClose() {     if (isClosed()) {         return;     }     closing = true; }
```

---

- 第 8 至 11 行：发送 **READONLY新的消息**
事件给所有 Client ，表示 Server 不再接收新的消息，避免不断有
接收到。杂实现的呢？以 DubboInvoker 举例子，
#isAvailable()
方法，代码如下：

```plain text
plain @Override public boolean isAvailable() {     if (!super.isAvailable())         return false;     for (ExchangeClient client : clients) {         if (client.isConnected() && !client.hasAttribute(Constants.CHANNEL_ATTRIBUTE_READONLY_KEY)) { // 只读判断             //cannot write == not Available ?             return true;         }     }     return false; }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">即使 </font><font style="color:rgb(51, 51, 51);">client</font><font style="color:rgb(51, 51, 51);"> 处于</font>**<font style="color:rgb(51, 51, 51);">连接中</font>**<font style="color:rgb(51, 51, 51);">，但是 Server 处于</font>**<font style="color:rgb(51, 51, 51);">正在关闭中</font>**<font style="color:rgb(51, 51, 51);">，也算</font>**<font style="color:rgb(51, 51, 51);">不可用</font>**<font style="color:rgb(51, 51, 51);">，不进行发送请求( 消息 )。</font>
```

- #sendChannelReadOnlyEvent()
方法，广播客户端，READONLY_EVENT 事件。代码如下：

```plain text
plain private void sendChannelReadOnlyEvent() {     // 创建 READONLY_EVENT 请求     Request request = new Request();     request.setEvent(Request.READONLY_EVENT);     request.setTwoWay(false); // 无需响应     request.setVersion(Version.getVersion());      // 发送给所有 Client     Collection<Channel> channels = getChannels();     for (Channel channel : channels) {         try {             if (channel.isConnected())                 channel.send(request, getUrl().getParameter(Constants.CHANNEL_READONLYEVENT_SENT_KEY, true));         } catch (RemotingException e) {             logger.warn("send connot write messge error.", e);         }     } }
```

---

- 第 22 行：调用
#oClose()
方法，关闭心跳定时器。代码如下：

```plain text
plain private void doClose() {     if (!closed.compareAndSet(false, true)) {         return;     }     stopHeartbeatTimer();     try {         scheduled.shutdown();     } catch (Throwable t) {         logger.warn(t.getMessage(), t);     } }
```

---

- 第 24 行：**真正**
关闭服务器。

## 4.2 ExchangeServerDelegate

[com.alibaba.dubbo.remoting.exchange.support.ExchangeServerDelegate](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/ExchangeServerDelegate.java) ，实现 ExchangeServer 接口，信息交换服务器装饰者。在每个实现的方法里，直接调用被装饰的 [server](https://github.com/YunaiV/dubbo/blob/31b3f1e868ed2d62c97a26b5cd233a921ce2205a/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/ExchangeServerDelegate.java#L34) 属性的方法。

目前 dubbo-remoting-p2p 模块中，ExchangeServerPeer 会继承该类，后续再看。

# 5. 请求/响应模型

## 5.1 Request

com.alibaba.dubbo.remoting.exchange.Request ，请求。代码如下：

```plain text
plain /**  * 事件 - 心跳  */ public static final String HEARTBEAT_EVENT = null; /**  * 事件 - 只读  */ public static final String READONLY_EVENT = "R";  /**  * 请求编号自增序列  */ private static final AtomicLong INVOKE_ID = new AtomicLong(0);  /**  * 请求编号  */ private final long mId; /**  * Dubbo 版本  */ private String mVersion; /**  * 是否需要响应  *  * true-需要  * false-不需要  */ private boolean mTwoWay = true; /**  * 是否是事件。例如，心跳事件。  */ private boolean mEvent = false; /**  * 是否异常的请求。  *  * 在消息解析的时候，会出现。  */ private boolean mBroken = false; /**  * 数据  */ private Object mData;
```

---

- 内置两种事件：
    - HEARTBEAT_EVENT
：心跳。因为心跳比较常用，所以在事件上时候了
null
。
    - READONLY_EVENT
：只读。上文已经解释。
- mId
属性：编号。使用
INVOKE_ID
属性生成，JVM 进程内唯一。生成代码如下：

```plain text
plain private static long newId() {     // getAndIncrement() When it grows to MAX_VALUE, it will grow to MIN_VALUE, and the negative can be used as ID     return INVOKE_ID.getAndIncrement(); }
```

---

- version
属性，版本号。目前使用 Dubbo 大版本，
“2.0.0”
。
- mTwoWay**需要**
属性，标记请求是否响应( Response )，默认
。
- mBroken
属性，是否异常的请求。在消息解析的时候，会出现。
- mData
属性，请求具体数据。

## 5.2 Response

com.alibaba.dubbo.remoting.exchange.Response ，响应。代码如下：

```plain text
plain /**  * 响应编号  *  * 一个 {@link Request#mId} 和 {@link Response#mId} 一一对应。  */ private long mId = 0; /**  * 版本  */ private String mVersion; /**  * 状态  */ private byte mStatus = OK; /**  * 是否事件  */ private boolean mEvent = false; /**  * 错误消息  */ private String mErrorMsg; /**  * 结果  */ private Object mResult;
```

---

- mId
属性，响应编号，和请求编号一致。
- mStatus[https://github.com/apache/incubator-dubbo/blob/9deadadea3b1342345fed77c87a3d24ea026d7e6/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/Response.java)。](https://github.com/apache/incubator-dubbo/blob/9deadadea3b1342345fed77c87a3d24ea026d7e6/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/Response.java)%E3%80%82)
属性，状态。有多种状态：[状态码] (
- mEvent**一样**
属性，是否事件。和 Request 内置了
的事件，但是
READONLY_EVENT
并未使用。因为目前，只读事件，无需响应。
- mErrorMsg
属性，错误消息。
- mResult
属性，结果。

## 5.3 ResponseFuture

com.alibaba.dubbo.remoting.exchange.ResponseFuture ，响应 Future **接口**。方法如下：

```plain text
plain // 获得值 Object get() throws RemotingException; Object get(int timeoutInMillis) throws RemotingException;  // 设置回调 void setCallback(ResponseCallback callback);  // 是否完成 boolean isDone();
```

---

和 [java.util.concurrent.Future](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/Future.html) 很类似。

### 5.3.1 ResponseCallback

com.alibaba.dubbo.remoting.exchange.ResponseCallback ，响应回调**接口**。方法如下：

```plain text
plain // 处理执行完成 void done(Object response);  // 处理发生异常 void caught(Throwable exception);
```

---

ResponseCallback 在 com.alibaba.dubbo.rpc.protocol.dubbo.filter.FutureFilter 中有使用，后面我们会有文章来分享 FutureFilter 。

### 5.3.2 DefaultFuture

com.alibaba.dubbo.remoting.exchange.support.DefaultFuture ，实现 ResponseFuture 接口，**默认**响应 Future 实现类。同时，它也是所有 DefaultFuture 的管理容器。

**构造方法**

```plain text
plain /**  * 通道集合  *  * key：请求编号  */ private static final Map<Long, Channel> CHANNELS = new ConcurrentHashMap<Long, Channel>(); /**  * Future 集合  *  * key：请求编号  */ private static final Map<Long, DefaultFuture> FUTURES = new ConcurrentHashMap<Long, DefaultFuture>();  /**  * 请求编号  */ // invoke id. private final long id; /**  * 通道  */ private final Channel channel; /**  * 请求  */ private final Request request; /**  * 超时  */ private final int timeout; /**  * 创建开始时间  */ private final long start = System.currentTimeMillis(); /**  * 发送请求时间  */ private volatile long sent; /**  * 响应  */ private volatile Response response; /**  * 回调  */ private volatile ResponseCallback callback;  public DefaultFuture(Channel channel, Request request, int timeout) {     this.channel = channel;     this.request = request;     this.id = request.getId();     this.timeout = timeout > 0 ? timeout : channel.getUrl().getPositiveParameter(Constants.TIMEOUT_KEY, Constants.DEFAULT_TIMEOUT);     // put into waiting map.     FUTURES.put(id, this);     CHANNELS.put(id, channel); }
```

---

- CHANNELS**静态**
属性，通道集合。通过
#hasFuture(channel)
方法，判断通道是否有未结束的请求。代码如下：

```plain text
plain public static boolean hasFuture(Channel channel) {     return CHANNELS.containsValue(channel); }
```

---

- FUTURES**静态**
属性，Future 集合。
- sent**静态方法**
属性，发送请求时间。因为在目前 Netty Mina 等通信框架中，发送请求一般是异步的，因此在
ChannelHandler#sent(channel, message)
方法中，调用
DefaultFuture#sent(channel, request)
，代码如下：

```plain text
plain public static void sent(Channel channel, Request request) {     DefaultFuture future = FUTURES.get(request.getId());     if (future != null) {         future.doSent();     } }  private void doSent() {     sent = System.currentTimeMillis(); }
```

---

- callback
属性，回调，适用于异步请求。通过
#setCallback(callback)
方法设置。

**获得值**

```plain text
plain /**  * 锁  */ private final Lock lock = new ReentrantLock(); /**  * 完成 Condition  */ private final Condition done = lock.newCondition();    1: @Override   2: public Object get(int timeout) throws RemotingException {   3:     if (timeout <= 0) {   4:         timeout = Constants.DEFAULT_TIMEOUT;   5:     }   6:     // 若未完成，等待   7:     if (!isDone()) {   8:         long start = System.currentTimeMillis();   9:         lock.lock();  10:         try {  11:             // 等待完成或超时  12:             while (!isDone()) {  13:                 done.await(timeout, TimeUnit.MILLISECONDS);  14:                 if (isDone() || System.currentTimeMillis() - start > timeout) {  15:                     break;  16:                 }  17:             }  18:         } catch (InterruptedException e) {  19:             throw new RuntimeException(e);  20:         } finally {  21:             lock.unlock();  22:         }  23:         // 未完成，抛出超时异常 TimeoutException  24:         if (!isDone()) {  25:             throw new TimeoutException(sent > 0, channel, getTimeoutMessage(false));  26:         }  27:     }  28:     // 返回响应  29:     return returnFromResponse();  30: }
```

---

- 第 7 行：调用
#isDone()
方法，判断是否完成。若未完成，基于 Lock + Condition 的方式，实现等待。而等待的唤醒，通过
ChannelHandler#received(channel, message)
方法，接收到请求时执行
DefaultFuture#received(channel, response)
方法。 下文详细解析。
    - [《 Java线程(九)：Condition-线程通信更高效的方式》](https://blog.csdn.net/ghsau/article/details/7481142)
    - [《怎么理解Condition》](http://www.importnew.com/9281.html)
    - 第 8 行：获得开始时间。**注意重新后台扫描调用超时任务等待超时后台扫描调用超时任务先调用**
，此处使用的不是
start
属性。后面我们会看到，
#get(…)
方法中，使用的是
获取开始时间；
，使用的是
start
属性。也就是说，
#get(timeout)
方法的
timeout
参数，指的是从当前时刻开始的
时间。当然，这不影响最终的结果，最终 Response 是什么，由是
ChannelHandler#received(channel, message)
还是
，谁
DefaultFuture#received(channel, response)
方法决定。 有点绕，胖友细看下。
    - 第 9 行：获得锁。
    - 第 11 至 17 行：等待**完成超时**
或
。
    - 第 21 行：释放锁。
    - 第 24 至 26 行：若未完成，抛出超时异常 TimeoutException 。
        - TimeoutException.phase
的阶段，由
sent > 0
来决定，即 Client 是否发送给 Server 。
        - [#getTimeoutMessage(scan)](https://github.com/apache/incubator-dubbo/blob/9deadadea3b1342345fed77c87a3d24ea026d7e6/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/DefaultFuture.java#L264-L275)
方法，获得超时异常提示信息。 胖友自己看哈。
- 第 29 行：调用
#returnFromResponse()
方法，返回响应( Response )。代码如下：

```plain text
plain private Object returnFromResponse() throws RemotingException {     Response res = response;     if (res == null) {         throw new IllegalStateException("response cannot be null");     }     // 正常，返回结果     if (res.getStatus() == Response.OK) {         return res.getResult();     }     // 超时，抛出 TimeoutException 异常     if (res.getStatus() == Response.CLIENT_TIMEOUT || res.getStatus() == Response.SERVER_TIMEOUT) {         throw new TimeoutException(res.getStatus() == Response.SERVER_TIMEOUT, channel, res.getErrorMessage());     }     // 其他，抛出 RemotingException 异常     throw new RemotingException(channel, res.getErrorMessage()); }
```

---

**响应结果**

```plain text
plain 1: public static void received(Channel channel, Response response) {  2:     try {  3:         // 移除 FUTURES  4:         DefaultFuture future = FUTURES.remove(response.getId());  5:         // 接收结果  6:         if (future != null) {  7:             future.doReceived(response);  8:         } else {  9:             logger.warn("The timeout response finally returned at " 10:                     + (new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS").format(new Date())) 11:                     + ", response " + response 12:                     + (channel == null ? "" : ", channel: " + channel.getLocalAddress() 13:                     + " -> " + channel.getRemoteAddress())); 14:         } 15:     // 移除 CHANNELS 16:     } finally { 17:         CHANNELS.remove(response.getId()); 18:     } 19: }
```

---

- 该方法有两处被调用，如下图所示：
![](/assets/images/learning/dubbo/dubbo-nio-server-exchange/03fdf57816e34daed595731c43e3507c.png)
调用
- 第 4 行：移除
FUTURES
。
- 第 6 至 7 行：调用
DefaultFuture#doReceived(response)
方法，响应结果。代码如下：

```plain text
plain 1: private void doReceived(Response res) {  2:     // 锁定  3:     lock.lock();  4:     try {  5:         // 设置结果  6:         response = res;  7:         // 通知，唤醒等待  8:         if (done != null) {  9:             done.signal(); 10:         } 11:     } finally { 12:         // 释放锁定 13:         lock.unlock(); 14:     } 15:     // 调用回调 16:     if (callback != null) { 17:         invokeCallback(callback); 18:     } 19: }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">第 3 行：获得锁。</font>
- <font style="color:rgb(51, 51, 51);">第 6 行：设置响应 </font><font style="color:rgb(51, 51, 51);">response</font><font style="color:rgb(51, 51, 51);"> 。</font>
- <font style="color:rgb(51, 51, 51);">第 8 至 10 行：调用 </font><font style="color:rgb(51, 51, 51);">Condition#signal()</font><font style="color:rgb(51, 51, 51);"> 方法，通知，</font>**<font style="color:rgb(51, 51, 51);">唤醒</font>**<font style="color:rgb(51, 51, 51);">DefaultFuture#get(..)</font><font style="color:rgb(51, 51, 51);"> 方法的等待。</font>
- <font style="color:rgb(51, 51, 51);">第 13 行：释放锁。</font>
- <font style="color:rgb(51, 51, 51);">第 16 至 18 行：调用 </font><font style="color:rgb(51, 51, 51);">#invokeCallback(callback)</font><font style="color:rgb(51, 51, 51);"> 方法，执行回调方法。</font>
```

- 第 8 至 14 行：超时情况，打印**告警**
日志。
- 第 15 至 18 行：移除
CHANNELS
。

**设置回调**

```plain text
plain 1: @Override  2: public void setCallback(ResponseCallback callback) {  3:     // 已完成，调用回调  4:     if (isDone()) {  5:         invokeCallback(callback);  6:     } else {  7:         boolean isdone = false;  8:         // 获得锁  9:         lock.lock(); 10:         try { 11:             // 未完成，设置回调 12:             if (!isDone()) { 13:                 this.callback = callback; 14:             } else { 15:                 isdone = true; 16:             } 17:         // 释放锁 18:         } finally { 19:             lock.unlock(); 20:         } 21:         // 已完成，调用回调 22:         if (isdone) { 23:             invokeCallback(callback); 24:         } 25:     } 26: }
```

---

- 第 3 至 5 行：若**已完成**
，调用
#invokeCallback(callback)
方法，执行回调方法。
- 第 9 行：获得锁。
- 第 12 至 13 行：若**未完成再回调**
，设置回调
callback
属性，等在
#doReceived(response)
方法中
。
- 第 14 至 16 行：标记已完成。在【第 22 至 24 行】，调用
#invokeCallback(callback)
方法，执行回调方法。
- 第 18 至 20 行：释放锁。

**调用回调**

```plain text
plain 1: private void invokeCallback(ResponseCallback c) {  2:     ResponseCallback callbackCopy = c;  3:     if (callbackCopy == null) {  4:         throw new NullPointerException("callback cannot be null.");  5:     }  6:     Response res = response;  7:     if (res == null) {  8:         throw new IllegalStateException("response cannot be null. url:" + channel.getUrl());  9:     } 10:  11:     // 正常，处理结果 12:     if (res.getStatus() == Response.OK) { 13:         try { 14:             callbackCopy.done(res.getResult()); 15:         } catch (Exception e) { 16:             logger.error("callback invoke error .reasult:" + res.getResult() + ",url:" + channel.getUrl(), e); 17:         } 18:     // 超时，处理 TimeoutException 异常 19:     } else if (res.getStatus() == Response.CLIENT_TIMEOUT || res.getStatus() == Response.SERVER_TIMEOUT) { 20:         try { 21:             TimeoutException te = new TimeoutException(res.getStatus() == Response.SERVER_TIMEOUT, channel, res.getErrorMessage()); 22:             callbackCopy.caught(te); 23:         } catch (Exception e) { 24:             logger.error("callback invoke error ,url:" + channel.getUrl(), e); 25:         } 26:     // 其他，处理 RemotingException 异常 27:     } else { 28:         try { 29:             RuntimeException re = new RuntimeException(res.getErrorMessage()); 30:             callbackCopy.caught(re); 31:         } catch (Exception e) { 32:             logger.error("callback invoke error ,url:" + channel.getUrl(), e); 33:         } 34:     } 35: }
```

---

- 和
#returnFromResponse()
方法，情况一致。
- 第 11 至 17 行：正常返回，调用
ResponseCallback#done(result)
方法，处理结果。
- 第 18 至 25 行：超时异常，调用
ResponseCallback#caught(e)
方法，处理 TimeoutException 异常。
- 第 26 至 34 行：其他异常，调用 ResponseCallback#caught(e)` 方法，处理 RuntimeException 异常。

**后台扫描调用超时任务**

```plain text
plain static {     Thread th = new Thread(new RemotingInvocationTimeoutScan(), "DubboResponseTimeoutScanTimer");     th.setDaemon(true);     th.start(); }  private static class RemotingInvocationTimeoutScan implements Runnable {      public void run() {         while (true) {             try {                 for (DefaultFuture future : FUTURES.values()) {                     // 已完成，跳过                     if (future == null || future.isDone()) {                         continue;                     }                     // 超时                     if (System.currentTimeMillis() - future.getStartTimestamp() > future.getTimeout()) {                         // 创建超时 Response                         // create exception response.                         Response timeoutResponse = new Response(future.getId());                         // set timeout status.                         timeoutResponse.setStatus(future.isSent() ? Response.SERVER_TIMEOUT : Response.CLIENT_TIMEOUT);                         timeoutResponse.setErrorMessage(future.getTimeoutMessage(true));                         // 响应结果                         // handle response.                         DefaultFuture.received(future.getChannel(), timeoutResponse);                     }                 }                 // 30 ms                 Thread.sleep(30);             } catch (Throwable e) {                 logger.error("Exception when scan the timeout invocation of remoting.", e);             }         }     } }
```

---

- 代码比较简单，胖友自己看下代码和注释嘿。

---

代码略多，胖友自己在梳理梳理，也可以多多调试。

### 5.3.3 SimpleFuture

[com.alibaba.dubbo.remoting.exchange.support.SimpleFuture](https://github.com/apache/incubator-dubbo/blob/9deadadea3b1342345fed77c87a3d24ea026d7e6/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/SimpleFuture.java) ，实现 ResponseFuture 接口，简单的 Future 实现。

目前暂未使用。

## 5.4 MultiMessage

com.alibaba.dubbo.remoting.exchange.support.MultiMessage ，实现 Iterable 接口，多消息的封装。代码如下：

```plain text
plain public final class MultiMessage implements Iterable {      private final List messages = new ArrayList();          // ... 省略方法 }
```

---

# 6. Handler

在文初的，我们在类图可以看到，有多种处理器，统一在本小节分享。

## 6.1 HeartbeatHandler

[com.alibaba.dubbo.remoting.exchange.support.header.HeartbeatHandler](https://github.com/YunaiV/dubbo/blob/619cbe46350c8d0b97b84631c6518e4603a89aee/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/header/HeartbeatHandler.java) ，实现 AbstractChannelHandlerDelegate 抽象类，**心跳处理器**，处理心跳事件。

旁白君，注意，它是一个 AbstractChannelHandlerDelegate ！！！

代码比较简单，胖友自己查看。

### 6.1.1 HeartBeatTask

com.alibaba.dubbo.remoting.exchange.support.header.HeartBeatTask ，实现 Runnable 接口，心跳任务。

**构造方法**

```plain text
plain private ChannelProvider channelProvider; /**  * 心跳间隔，单位：毫秒  */ private int heartbeat; /**  * 心跳超时时间，单位：毫秒  */ private int heartbeatTimeout;
```

---

- channelProvider
属性，用于查询获得需要心跳的通道数组。ChannelProvider 接口，代码如下：

```plain text
plain interface ChannelProvider {     Collection<Channel> getChannels(); }
```

---

**执行任务**

```plain text
plain 1: @Override  2: public void run() {  3:     try {  4:         long now = System.currentTimeMillis();  5:         for (Channel channel : channelProvider.getChannels()) {  6:             if (channel.isClosed()) {  7:                 continue;  8:             }  9:             try { 10:                 Long lastRead = (Long) channel.getAttribute(HeaderExchangeHandler.KEY_READ_TIMESTAMP); 11:                 Long lastWrite = (Long) channel.getAttribute(HeaderExchangeHandler.KEY_WRITE_TIMESTAMP); 12:                 // 最后读写的时间，任一超过心跳间隔，发送心跳 13:                 if ((lastRead != null && now - lastRead > heartbeat) 14:                         || (lastWrite != null && now - lastWrite > heartbeat)) { 15:                     Request req = new Request(); 16:                     req.setVersion("2.0.0"); 17:                     req.setTwoWay(true); // 需要响应 18:                     req.setEvent(Request.HEARTBEAT_EVENT); 19:                     channel.send(req); 20:                     if (logger.isDebugEnabled()) { 21:                         logger.debug("Send heartbeat to remote channel " + channel.getRemoteAddress() 22:                                 + ", cause: The channel has no data-transmission exceeds a heartbeat period: " + heartbeat + "ms"); 23:                     } 24:                 } 25:                 // 最后读的时间，超过心跳超时时间 26:                 if (lastRead != null && now - lastRead > heartbeatTimeout) { 27:                     logger.warn("Close channel " + channel 28:                             + ", because heartbeat read idle time out: " + heartbeatTimeout + "ms"); 29:                     // 客户端侧，重新连接服务端 30:                     if (channel instanceof Client) { 31:                         try { 32:                             ((Client) channel).reconnect(); 33:                         } catch (Exception e) { 34:                             //do nothing 35:                         } 36:                     // 服务端侧，关闭客户端连接 37:                     } else { 38:                         channel.close(); 39:                     } 40:                 } 41:             } catch (Throwable t) { 42:                 logger.warn("Exception when heartbeat to remote channel " + channel.getRemoteAddress(), t); 43:             } 44:         } 45:     } catch (Throwable t) { 46:         logger.warn("Unhandled exception when heartbeat, cause: " + t.getMessage(), t); 47:     } 48: }
```

---

- 【任务一】第 13 至 24 行：最后读或写的时间，**任一发送心跳**
超过心跳间隔
heartbeat
，
。
- 【任务二】第 25 至 40 行：最后读的时间，超过心跳超时时间
heartbeatTimeout
，分成两种情况：
    - 第 29 至 35 行：**客户端侧**
，重连连接服务端。
    - 第 36 至 39 行：**服务端侧**
，关闭客户端连接。

## 6.2 HeaderExchangeHandler

[com.alibaba.dubbo.remoting.exchange.support.header.HeaderExchangeHandler](https://github.com/YunaiV/dubbo/blob/e24730a1dcfe8d5f1329377e80b1577724a85aac/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/header/HeaderExchangeHandler.java)，实现 ChannelHandlerDelegate 接口，**基于消息头部( Header )**的信息交换处理器实现类。

旁白君，注意，它是一个 ChannelHandlerDelegate ！！！

代码比较简单，胖友自己查看，我们挑几个比较重要的来讲讲。

**接收消息**

```plain text
plain 1: @Override  2: public void received(Channel channel, Object message) throws RemotingException {  3:     // 设置最后的读时间  4:     channel.setAttribute(KEY_READ_TIMESTAMP, System.currentTimeMillis());  5:     // 创建 ExchangeChannel 对象  6:     ExchangeChannel exchangeChannel = HeaderExchangeChannel.getOrAddChannel(channel);  7:     try {  8:         // 处理请求( Request )  9:         if (message instanceof Request) { 10:             // handle request. 11:             Request request = (Request) message; 12:             // 处理事件请求 13:             if (request.isEvent()) { 14:                 handlerEvent(channel, request); 15:             } else { 16:                 // 处理普通请求 17:                 if (request.isTwoWay()) { 18:                     Response response = handleRequest(exchangeChannel, request); 19:                     channel.send(response); 20:                 // 提交给装饰的 `handler`，继续处理 21:                 } else { 22:                     handler.received(exchangeChannel, request.getData()); 23:                 } 24:             } 25:         // 处理响应( Response ) 26:         } else if (message instanceof Response) { 27:             handleResponse(channel, (Response) message); 28:         // 处理 String 29:         } else if (message instanceof String) { 30:             // 客户端侧，不支持 String 31:             if (isClientSide(channel)) { 32:                 Exception e = new Exception("Dubbo client can not supported string message: " + message + " in channel: " + channel + ", url: " + channel.getUrl()); 33:                 logger.error(e.getMessage(), e); 34:             // 服务端侧，目前是 telnet 命令 35:             } else { 36:                 String echo = handler.telnet(channel, (String) message); 37:                 if (echo != null && echo.length() > 0) { 38:                     channel.send(echo); 39:                 } 40:             } 41:             // 提交给装饰的 `handler`，继续处理 42:         } else { 43:             handler.received(exchangeChannel, message); 44:         } 45:     } finally { 46:         // 移除 ExchangeChannel 对象，若已断开 47:         HeaderExchangeChannel.removeChannelIfDisconnected(channel); 48:     } 49: }
```

---

- 第 4 行：设置最后的**读时间**
。
- 第 6 行：创建 ExchangeChannel 对象。
- 第 8 至 24 行：处理请求( Request)
    - 第 13 至 14 行：调用
#handlerEvent(channel, request)
方法，处理事件请求。
    - 第 17 至 19 行：调用
#handleRequest(channel, request)
方法，处理普通请求（需要响应），并将响应写回请求方。
    - 第 21 至 23 行：调用
ChannelHandler#received(channel, message)
方法，处理普通请求（无需响应）。
- 第 25 至 27 行：调用
#handleResponse(channel, message)
方法，处理响应。
- 第 29 至 41 行：处理 String 的情况
    - 第 30 至 33 行：客户端侧，不支持 String 的情况。
    - 第 34 至 40 行：服务端侧，目前仅有 telnet 命令的情况，调用 [《精尽 Dubbo 源码分析 —— NIO 服务器（三）之 Telnet 层》](http://svip.iocoder.cn/Dubbo/remoting-api-telnet/?self=)
TelnetHandler#telnet(channel, message)
方法，获得 telnet 命令的结果，并响应给 telnet 客户端。在
有详细分享。
- 第 42 至 44 行：剩余的情况，调用
ChannelHandler#received(channel, message)
方法，处理。
- 第 45 至 48 行：移除 ExchangeChannel 对象，若已断开。
- #handlerEvent(channel, request)
方法，代码如下：

```plain text
plain void handlerEvent(Channel channel, Request req) {     if (req.getData() != null && req.getData().equals(Request.READONLY_EVENT)) {         channel.setAttribute(Constants.CHANNEL_ATTRIBUTE_READONLY_KEY, Boolean.TRUE);     } }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">客户端接收到 READONLY_EVENT 事件请求，进行记录到通道。后续，不再向该服务器，</font>**<font style="color:rgb(51, 51, 51);">发送新的请求</font>**<font style="color:rgb(51, 51, 51);">。</font>
```

- #handleRequest(channel, request)
方法，代码如下：

```plain text
plain 1: Response handleRequest(ExchangeChannel channel, Request req) {  2:     Response res = new Response(req.getId(), req.getVersion());  3:     // 请求无法解析，返回 BAD_REQUEST 响应  4:     if (req.isBroken()) {  5:         Object data = req.getData();  6:         String msg; // 请求数据，转成 msg  7:         if (data == null) {  8:             msg = null;  9:         } else if (data instanceof Throwable) { 10:             msg = StringUtils.toString((Throwable) data); 11:         } else { 12:             msg = data.toString(); 13:         } 14:         res.setErrorMessage("Fail to decode request due to: " + msg); 15:         res.setStatus(Response.BAD_REQUEST); 16:         return res; 17:     } 18:     // 使用 ExchangeHandler 处理，并返回响应 19:     // find handler by message class. 20:     Object msg = req.getData(); 21:     try { 22:         // handle data. 23:         Object result = handler.reply(channel, msg); 24:         res.setStatus(Response.OK); 25:         res.setResult(result); 26:     } catch (Throwable e) { 27:         res.setStatus(Response.SERVICE_ERROR); 28:         res.setErrorMessage(StringUtils.toString(e)); 29:     } 30:     return res; 31: }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">第 3 至 17 行：请求</font>**<font style="color:rgb(51, 51, 51);">无法解析</font>**<font style="color:rgb(51, 51, 51);">，返回 BAD_REQUEST 响应。下面 ExchangeCodec ，我们将看到具体发生的代码。</font>
- <font style="color:rgb(51, 51, 51);">第 18 至 30 行：调用 </font><font style="color:rgb(51, 51, 51);">ExchangeHandler#reply(channel, message)</font><font style="color:rgb(51, 51, 51);"> 方法，返回结果，并设置到响应( Response) 最终返回。</font>
```

- #handleResponse(channel, response)
方法，代码如下：

```plain text
plain static void handleResponse(Channel channel, Response response) {     if (response != null && !response.isHeartbeat()) {         DefaultFuture.received(channel, response);     } }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">非心跳事件响应，调用 </font><font style="color:rgb(51, 51, 51);">DefaultFuture#received(channel, response)</font><font style="color:rgb(51, 51, 51);"> 方法，唤醒等待请求结果的线程。</font>
```

比较繁杂，胖友耐心的看一看哟。

**发生异常**

```plain text
plain 1: @Override  2: public void caught(Channel channel, Throwable exception) throws RemotingException {  3:     // 当发生 ExecutionException 异常，返回异常响应( Response )  4:     if (exception instanceof ExecutionException) {  5:         ExecutionException e = (ExecutionException) exception;  6:         Object msg = e.getRequest();  7:         if (msg instanceof Request) {  8:             Request req = (Request) msg;  9:             if (req.isTwoWay() && !req.isHeartbeat()) { // 需要响应，并且非心跳时间 10:                 Response res = new Response(req.getId(), req.getVersion()); 11:                 res.setStatus(Response.SERVER_ERROR); 12:                 res.setErrorMessage(StringUtils.toString(e)); 13:                 channel.send(res); 14:                 return; 15:             } 16:         } 17:     } 18:     // 创建 ExchangeChannel 对象 19:     ExchangeChannel exchangeChannel = HeaderExchangeChannel.getOrAddChannel(channel); 20:     try { 21:         // 提交给装饰的 `handler`，继续处理 22:         handler.caught(exchangeChannel, exception); 23:     } finally { 24:         // 移除 ExchangeChannel 对象，若已断开 25:         HeaderExchangeChannel.removeChannelIfDisconnected(channel); 26:     } 27: }
```

---

- 第 3 至 17 行：当发生 ExecutionException 异常，返回异常响应( Response )。目前会发生 ExecutionException 的情况，并且符合提交，如下图所示：
![](/assets/images/learning/dubbo/dubbo-nio-server-exchange/37db3a91094dc90d601faf3ea1a78884.png)
ExecutionException
- 第 18 至 26 行：见注释。

## 6.3 ExchangeHandler

com.alibaba.dubbo.remoting.exchange.ExchangeHandler ，继承 ChannelHandler 和 TelnetHandler 接口，信息交换处理器**接口**。方法如下：

```plain text
plain // 回复请求结果 Object reply(ExchangeChannel channel, Object request) throws RemotingException;
```

---

- **注意请求结果**
，返回的是
。正如我们在上文看到的，将请求结果，设置到
Response.mResult
属性中。

ExchangeHandler 是一个非常关键的接口。为什么这么说呢，点击 [DubboProtocol. requestHandler](https://github.com/YunaiV/dubbo/blob/619cbe46350c8d0b97b84631c6518e4603a89aee/dubbo-rpc/dubbo-rpc-default/src/main/java/com/alibaba/dubbo/rpc/protocol/dubbo/DubboProtocol.java#L82-L112) ！胖友，领悟到了么？如果没有，淡定，后面我们会有文章分享。

### 6.3.1 ExchangeHandlerAdapter

com.alibaba.dubbo.remoting.exchange.support.ExchangeHandlerAdapter ，实现 ExchangeHandler 接口，继承 TelnetHandlerAdapter 抽象类，信息交换处理器适配器**抽象类**。代码如下：

```plain text
plain @Override public Object reply(ExchangeChannel channel, Object msg) throws RemotingException {     return null; }
```

---

在 DubboProtocol 、ThirftProtocol 中，都会基于 ExchangeHandlerAdapter **实现自己的处理器**，处理请求，返回结果。

## 6.4 Replier

友情提示：这个小节，胖友可以选择性来看，目前仅用于 dubbo-remoting-p2p 模块中。

在 ExchangeHandler 中，我们看到的是，Request 对应统一的 ExchangeHandler 实现的对象。但是在一些场景下，我们希望实现，不同的数据类型，对应不同的处理器。Replier 就是来处理这种情况的。一个数据类型，对应一个 Replier 对象。

com.alibaba.dubbo.remoting.exchange.support.Replier ，回复者接口。代码如下：

```plain text
plain public interface Replier<T> {      // 回复请求结果     Object reply(ExchangeChannel channel, T request) throws RemotingException;  }
```

---

- 和 ExchangeHandler 最大的不同是，使用的是**泛型 T**
，而不是固定的 Request 。

### 6.4.1 ReplierDispatcher

com.alibaba.dubbo.remoting.exchange.support.ReplierDispatcher ，实现 Replier 接口，回复者**调度器**实现类。

**构造方法**

```plain text
plain /**  * 默认回复者  */ private final Replier<?> defaultReplier; /**  * 回复者集合  *  * key：类  */ private final Map<Class<?>, Replier<?>> repliers = new ConcurrentHashMap<Class<?>, Replier<?>>();  public ReplierDispatcher() {     this(null, null); }  public ReplierDispatcher(Replier<?> defaultReplier) {     this(defaultReplier, null); }  public ReplierDispatcher(Replier<?> defaultReplier, Map<Class<?>, Replier<?>> repliers) {     // ... 省略 }
```

---

- repliers[#addReplier(Class type, Replier replier)](https://github.com/YunaiV/dubbo/blob/c63ec335b776a386a215fa3662b575ece7d32c5e/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/ReplierDispatcher.java#L49-L52)[#removeReplier(Class type)](https://github.com/YunaiV/dubbo/blob/c63ec335b776a386a215fa3662b575ece7d32c5e/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/ReplierDispatcher.java#L54-L57)
属性，回复者集合。可通过
或
方法，添加或移除回复者。

**回复请求结果**

```plain text
plain @Override @SuppressWarnings({"unchecked", "rawtypes"}) public Object reply(ExchangeChannel channel, Object request) throws RemotingException {     return ((Replier) getReplier(request.getClass())).reply(channel, request); }
```

---

- 调用 [#getReplier(Class<?> type)](https://github.com/YunaiV/dubbo/blob/c63ec335b776a386a215fa3662b575ece7d32c5e/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/support/ReplierDispatcher.java#L59-L69)
方法，获得回复者对象。
- 调用
Repiler#reply(channel, request)
方法，回复请求结果。

### 6.4.2 ExchangeHandlerDispatcher

com.alibaba.dubbo.remoting.exchange.support.ExchangeHandlerDispatcher ，实现 ExchangeHandler 接口，信息交换处理器**调度器**实现类。代码如下：

```plain text
plain /**  * 回复者调度器  */ private final ReplierDispatcher replierDispatcher; /**  * 通道处理器集合  */ private final ChannelHandlerDispatcher handlerDispatcher; /**  * Telnet 命令处理器  */ private final TelnetHandler telnetHandler;  // ... 省略方法
```

---

- 通过 ExchangeHandlerDispatcher ，将 ReplierDispatcher + ChannelHandlerDispatcher + TelnetHandler 三者结合在一起，将对应的事件，调度到**合适的**
处理器。以
#reply(…)
#received(…)
#telnet(…)
方法，举例子，代码如下：

```plain text
plain @Override @SuppressWarnings({"unchecked", "rawtypes"}) public Object reply(ExchangeChannel channel, Object request) throws RemotingException {     return replierDispatcher.reply(channel, request); }  @Override public void received(Channel channel, Object message) {     handlerDispatcher.received(channel, message); }  @Override public String telnet(Channel channel, String message) throws RemotingException {     return telnetHandler.telnet(channel, message); }
```

---

# 7. Exchanger

com.alibaba.dubbo.remoting.exchange.Exchanger ，**数据交换者**接口。方法如下：

Exchanger 和 Transporter 类似。

```plain text
plain @SPI(HeaderExchanger.NAME) public interface Exchanger {      /**      * bind.      *      * 绑定一个服务器      *      * @param url server url      * @param handler 数据交换处理器      * @return message server 服务器      */     @Adaptive({Constants.EXCHANGER_KEY})     ExchangeServer bind(URL url, ExchangeHandler handler) throws RemotingException;      /**      * connect.      *      * 连接一个服务器，即创建一个客户端      *      * @param url server url 服务器地址      * @param handler 数据交换处理器      * @return message channel 客户端      */     @Adaptive({Constants.EXCHANGER_KEY})     ExchangeClient connect(URL url, ExchangeHandler handler) throws RemotingException;  }
```

---

- @SPI(HeaderExchanger.NAME)**拓展点**
注解，Dubbo SPI
，默认为
“header”
，即 HeaderExchanger 。
- @Adaptive({Constants.EXCHANGER_KEY})
注解，基于 Dubbo SPI Adaptive 机制，加载对应的 Server 实现，使用
URL.exchanger
属性。
- @Adaptive({Constants.EXCHANGER_KEY})
注解，基于 Dubbo SPI Adaptive 机制，加载对应的 Client 实现，使用
URL.exchanger
属性。

## 7.1 HeaderExchanger

com.alibaba.dubbo.remoting.exchange.support.header.HeaderExchanger ，实现 Exchanger 接口，基于消息头部( Header )的**信息交换者**实现类。代码如下：

```plain text
plain public class HeaderExchanger implements Exchanger {      public static final String NAME = "header";      @Override     public ExchangeClient connect(URL url, ExchangeHandler handler) throws RemotingException {         return new HeaderExchangeClient(Transporters.connect(url, new DecodeHandler(new HeaderExchangeHandler(handler))), true);     }      @Override     public ExchangeServer bind(URL url, ExchangeHandler handler) throws RemotingException {         return new HeaderExchangeServer(Transporters.bind(url, new DecodeHandler(new HeaderExchangeHandler(handler))));     }  }
```

---

- 以
#connect(…)
方法举例子。
    - 通过
Transporters#connect(url, handler)
方法，创建通信 Client ，内嵌到 HeaderExchangeClient 中。
    - 传入的
handler
处理器，内嵌到 HeaderExchangeHandler ，再进一步内嵌到 DecodeHandler 中。所以，处理器的顺序是：DecodeHandler => HeaderExchangeHandler => ExchangeHandler(
handler
) 。

## 7.2 Exchangers

Exchangers 和 Transporters 类似。

[com.alibaba.dubbo.remoting.Transporters](https://github.com/YunaiV/dubbo/blob/e24730a1dcfe8d5f1329377e80b1577724a85aac/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/Exchangers.java) ，数据交换者门面类，参见 Facade 设计模式。

代码比较简单，胖友自己查看列。

# 8. ExchangeCodec

胖友，打起精神，ExchangeCodec 非常重要。

com.alibaba.dubbo.remoting.exchange.codec.ExchangeCodec ，继承 TelnetCodec 类，信息交换编解码器。

在看具体的编解码方法的代码时，我们来先看一幅图：

![](/assets/images/learning/dubbo/dubbo-nio-server-exchange/9bc8327c20bb17075e0991a24bc32d25.png)

协议

- 基于**消息长度粘包拆包**[《精尽 Dubbo 源码分析 —— NIO 服务器（二）之 Transport 层》](http://svip.iocoder.cn/Dubbo/remoting-api-transport/?self=)**特定字符粘包拆包不同**
的方式，做每条消息的
处理。和我们在
中，看到 Telnet 协议，基于
的方式，做每条命令的
处理
。
- Header 部分，协议头，通过 Codec 编解码。Bits 位如下：
    - [0, 15]
：Magic Number
    - [16, 20]
：Serialization 编号。
    - [21]
：
event
是否为事件。
    - [22]
：
twoWay
是否需要响应。
    - [23]
：是请求还是响应。
    - [24 - 31]
：
status
状态。
    - [32 - 95]
：
id
编号，Long 型。
    - [96 - 127]**长度**
：Body 的
。通过该长度，读取 Body 。
- Body 部分，协议体，通过 Serialization 序列化/反序列化。

**属性**

```plain text
plain // header length. protected static final int HEADER_LENGTH = 16; // magic header. protected static final short MAGIC = (short) 0xdabb; protected static final byte MAGIC_HIGH = Bytes.short2bytes(MAGIC)[0]; protected static final byte MAGIC_LOW = Bytes.short2bytes(MAGIC)[1]; // message flag. protected static final byte FLAG_REQUEST = (byte) 0x80; // 128 protected static final byte FLAG_TWOWAY = (byte) 0x40; // 64 protected static final byte FLAG_EVENT = (byte) 0x20; // 32 protected static final int SERIALIZATION_MASK = 0x1f; // 31
```

---

- HEADER_LENGTH**静态**
属性，Header 总长度，16 Bytes = 128 Bits 。
- 其它**静态**
属性，胖友对照上面的 Bits 位。

**编码**

```plain text
plain 1: @Override  2: public void encode(Channel channel, ChannelBuffer buffer, Object msg) throws IOException {  3:     if (msg instanceof Request) { // 请求  4:         encodeRequest(channel, buffer, (Request) msg);  5:     } else if (msg instanceof Response) { // 响应  6:         encodeResponse(channel, buffer, (Response) msg);  7:     } else { // 提交给父类( Telnet ) 处理，目前是 Telnet 命令的结果。  8:         super.encode(channel, buffer, msg);  9:     } 10: }
```

---

- 第 3 至 4 行：调用
#encodeRequest(channel, buffer, request)
方法，编码请求。
- 第 5 至 6 行：调用
#encodeResponse(channel, buffer, response)
方法，编码响应。
- 第 7 至 9 行：调用
TelnetCodec#encode(channel, buffer, msg)
方法，编码 Telnet 命令的结果。
- #encodeRequest(channel, buffer, request)
方法，代码如下：

```plain text
plain 1: protected void encodeRequest(Channel channel, ChannelBuffer buffer, Request req) throws IOException {  2:     Serialization serialization = getSerialization(channel);  3:     // `[0, 15]`：Magic Number  4:     // header.  5:     byte[] header = new byte[HEADER_LENGTH];  6:     // set magic number.  7:     Bytes.short2bytes(MAGIC, header);  8:   9:     // `[16, 20]`：Serialization 编号 && `[23]`：请求。 10:     // set request and serialization flag. 11:     header[2] = (byte) (FLAG_REQUEST | serialization.getContentTypeId()); 12:  13:     // `[21]`：`event` 是否为事件。 14:     if (req.isTwoWay()) header[2] |= FLAG_TWOWAY; 15:     // `[22]`：`twoWay` 是否需要响应。 16:     if (req.isEvent()) header[2] |= FLAG_EVENT; 17:  18:     // `[32 - 95]`：`id` 编号，Long 型。 19:     // set request id. 20:     Bytes.long2bytes(req.getId(), header, 4); 21:  22:     // 编码 `Request.data` 到 Body ，并写入到 Buffer 23:     // encode request data. 24:     int savedWriteIndex = buffer.writerIndex(); 25:     buffer.writerIndex(savedWriteIndex + HEADER_LENGTH); 26:     ChannelBufferOutputStream bos = new ChannelBufferOutputStream(buffer); 27:     ObjectOutput out = serialization.serialize(channel.getUrl(), bos); // 序列化 Output 28:     if (req.isEvent()) { 29:         encodeEventData(channel, out, req.getData()); 30:     } else { 31:         encodeRequestData(channel, out, req.getData()); 32:     } 33:     // 释放资源 34:     out.flushBuffer(); 35:     if (out instanceof Cleanable) { 36:         ((Cleanable) out).cleanup(); 37:     } 38:     bos.flush(); 39:     bos.close(); 40:     // 检查 Body 长度，是否超过消息上限。 41:     int len = bos.writtenBytes(); 42:     checkPayload(channel, len); 43:     // `[96 - 127]`：Body 的**长度**。 44:     Bytes.int2bytes(len, header, 12); 45:  46:     // 写入 Header 到 Buffer 47:     // write 48:     buffer.writerIndex(savedWriteIndex); 49:     buffer.writeBytes(header); // write header. 50:     buffer.writerIndex(savedWriteIndex + HEADER_LENGTH + len); 51: }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">Header 部分，先写入 </font><font style="color:rgb(51, 51, 51);">header</font><font style="color:rgb(51, 51, 51);"> 数组，再写入 Buffer 中。</font>
- <font style="color:rgb(51, 51, 51);">Body 部分，使用 Serialization 序列化 </font><font style="color:rgb(51, 51, 51);">Request.data</font><font style="color:rgb(51, 51, 51);"> ，写入到 Buffer 中。</font>
    * <font style="color:rgb(51, 51, 51);">#encodeEventData(Channel channel, ObjectOutput out, Object data)</font><font style="color:rgb(51, 51, 51);"> 方法，代码如下：</font>
```

```plain text
plain private void encodeEventData(Channel channel, ObjectOutput out, Object data) throws IOException {     encodeEventData(out, data); }  private void encodeEventData(ObjectOutput out, Object data) throws IOException {     out.writeObject(data); }
```

---

```plain text
        + <font style="color:rgb(51, 51, 51);">x</font>
    * <font style="color:rgb(51, 51, 51);">#encodeRequestData(Channel channel, ObjectOutput out, Object data)</font><font style="color:rgb(51, 51, 51);"> 方法，代码如下：</font>
```

```plain text
plain protected void encodeRequestData(Channel channel, ObjectOutput out, Object data) throws IOException {     encodeRequestData(out, data); }  protected void encodeRequestData(ObjectOutput out, Object data) throws IOException {     out.writeObject(data); }
```

---

```plain text
        + <font style="color:rgb(51, 51, 51);">#encodeEventData(...)</font><font style="color:rgb(51, 51, 51);"> 和 </font><font style="color:rgb(51, 51, 51);">#encodeRequestData(...)</font><font style="color:rgb(51, 51, 51);"> 两个方法是一致的。</font>
- <font style="color:rgb(51, 51, 51);">第 42 行：会调用 </font><font style="color:rgb(51, 51, 51);">#checkPayload(channel, len)</font><font style="color:rgb(51, 51, 51);"> 方法，校验 Body 内容的长度。笔者在这块纠结了很久，如果过长而抛出 ExceedPayloadLimitException 异常，那么 ChannelBuffer 是否重置下写入位置。后来发现自己煞笔了，每次 ChannelBuffer 都是新创建的，所以无需重置。</font>
- <font style="color:rgb(51, 51, 51);">为什么 Buffer 先写入了 Body ，再写入 Header 呢？因为 Header 中，里面 </font><font style="color:rgb(51, 51, 51);">[96 - 127]</font><font style="color:rgb(51, 51, 51);"> 的 Body 长度，需要序列化后才得到。</font>
```

- [#encodeResponse(channel, buffer, response)](https://github.com/YunaiV/dubbo/blob/a89a569e608ee1282d1bce3fc2540860873629db/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/codec/ExchangeCodec.java#L292-L404)
方法，和
#encodeRequest(chanel, buffer, request)
方法，基本一致，胖友自己瞅瞅列。主要差异点如下：
    - [24 - 31]
：
status
状态。这是 Request 没有，而 Response 有的部分。
    - 当响应的内容过长而抛出 ExceedPayloadLimitException 异常，根据条件，发送一条 Response (
status = BAD_RESPONSE
) 给请求方。

**解码**

```plain text
plain 1: @Override  2: public Object decode(Channel channel, ChannelBuffer buffer) throws IOException {  3:     // 读取 Header 数组  4:     int readable = buffer.readableBytes();  5:     byte[] header = new byte[Math.min(readable, HEADER_LENGTH)];  6:     buffer.readBytes(header);  7:     // 解码  8:     return decode(channel, buffer, readable, header);  9: } 10:  11: @Override 12: protected Object decode(Channel channel, ChannelBuffer buffer, int readable, byte[] header) throws IOException { 13:     // 非 Dubbo 协议，目前是 Telnet 命令。 14:     // check magic number. 15:     if (readable > 0 && header[0] != MAGIC_HIGH || readable > 1 && header[1] != MAGIC_LOW) { 16:         // 将 buffer 完全复制到 `header` 数组中。因为，上面的 `#decode(channel, buffer)` 方法，可能未读全 17:         int length = header.length; 18:         if (header.length < readable) { 19:             header = Bytes.copyOf(header, readable); 20:             buffer.readBytes(header, length, readable - length); 21:         } 22:         // 【TODO 8026 】header[i] == MAGIC_HIGH && header[i + 1] == MAGIC_LOW ？ 23:         for (int i = 1; i < header.length - 1; i++) { 24:             if (header[i] == MAGIC_HIGH && header[i + 1] == MAGIC_LOW) { 25:                 buffer.readerIndex(buffer.readerIndex() - header.length + i); 26:                 header = Bytes.copyOf(header, i); 27:                 break; 28:             } 29:         } 30:         // 提交给父类( Telnet ) 处理，目前是 Telnet 命令。 31:         return super.decode(channel, buffer, readable, header); 32:     } 33:     // Header 长度不够，返回需要更多的输入 34:     // check length. 35:     if (readable < HEADER_LENGTH) { 36:         return DecodeResult.NEED_MORE_INPUT; 37:     } 38:  39:     // `[96 - 127]`：Body 的**长度**。通过该长度，读取 Body 。 40:     // get data length. 41:     int len = Bytes.bytes2int(header, 12); 42:     checkPayload(channel, len); 43:  44:     // 总长度不够，返回需要更多的输入 45:     int tt = len + HEADER_LENGTH; 46:     if (readable < tt) { 47:         return DecodeResult.NEED_MORE_INPUT; 48:     } 49:  50:     // 解析 Header + Body 51:     // limit input stream. 52:     ChannelBufferInputStream is = new ChannelBufferInputStream(buffer, len); 53:     try { 54:         return decodeBody(channel, is, header); 55:     } finally { 56:         // skip 未读完的流，并打印错误日志 57:         if (is.available() > 0) { 58:             try { 59:                 if (logger.isWarnEnabled()) { 60:                     logger.warn("Skip input stream " + is.available()); 61:                 } 62:                 StreamUtils.skipUnusedStream(is); 63:             } catch (IOException e) { 64:                 logger.warn(e.getMessage(), e); 65:             } 66:         } 67:     } 68: }
```

---

- 第 3 至 6 行：读取 **注意**
header
数组。
，这里的
Math.min(readable, HEADER_LENGTH)
，优先考虑解析 Dubbo 协议。
- 第 8 行：调用
#decode(channel, buffer, readable, header)
方法，解码。
- ========== 分隔线 ==========
- 第 13 至 32 行：非 Dubbo 协议，目前是 Telnet 协议。
    - 第 17 至 21 行：将 Buffer 完全复制到 **Dubbo 协议**
header
数组中。因为，上面的
#decode(channel, buffer)
方法，可能未读全。因为，【第 3 至 6 行】，是以
为优先考虑解码的。
    - 第 22 至 29 行：【TODO 8026 】header[i] == MAGIC_HIGH && header[i + 1] == MAGIC_LOW ？搞不懂？
    - 第 31 行：调用 [《精尽 Dubbo 源码分析 —— NIO 服务器（三）之 Telnet 层》](http://svip.iocoder.cn/Dubbo/remoting-api-telnet/?self=)
Telnet#decode(channel, buffer, readable, header)
方法，解码 Telnet 。在
有详细解析。
- 第 33 至 48 行：基于**消息长度**
的方式，拆包。
- 第 50 至 54 行：调用 [#decodeBody(channel, is, header)](https://github.com/YunaiV/dubbo/blob/a89a569e608ee1282d1bce3fc2540860873629db/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/exchange/codec/ExchangeCodec.java#L148-L218)
方法，解析 Header + Body ，根据情况，返回 Request 或 Reponse 。 逻辑上，是
#encodeRequest(…)
和
#encodeResponse(…)
方法的反向，所以，胖友就自己看啦。
- 第 55 至 67 行：skip **未读完的流**
，并打印告警日志。
