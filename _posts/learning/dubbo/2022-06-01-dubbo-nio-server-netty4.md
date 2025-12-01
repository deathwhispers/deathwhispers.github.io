---
layout: post
title: NIO服务器（六）之Netty4实现
slug: dubbo-nio-server-netty4
type:
  - note
date: 2022-06-01
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-06-01 11:49
updated: 2022-06-01 18:33
---
本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

在前面的文章，我们已经了解了 dubbo-remoting-api 如何实现 NIO 服务器的抽象 API 层。那么本文来看看，dubbo-remoting-netty4 ，如何将 Netty4 接入实现。

涉及如下类：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038307508-2a1fd8f2-be16-4e5b-86c8-40c65e63a163.png)

类图

友情提示：在当前版本，默认情况下，使用 Netty3 ，如果想配置成 Netty4 ，请参考文档：[《Dubbo 用户指南 —— Netty4》](http://dubbo.apache.org/zh-cn/docs/user/demos/netty4.html)

# 2. NettyTransporter

com.alibaba.dubbo.remoting.transport.netty4.NettyTransporter ，实现 Transporter 接口，基于 **Netty4** 的网络传输实现类。代码如下：

```plain text
plain public class NettyTransporter implements Transporter {      /**      * 拓展名      */     public static final String NAME = "netty4";      public Server bind(URL url, ChannelHandler listener) throws RemotingException {         return new NettyServer(url, listener);     }      public Client connect(URL url, ChannelHandler listener) throws RemotingException {         return new NettyClient(url, listener);     }  }
```

---

- NAME**静态**
属性，拓展名。
- NettyTransporter 基于 Dubbo SPI 机制加载。
- 创建 NettyServer 和 NettyClient 对象。

# 3. NettyChannel

io.netty.channel.ChannelFuture.NettyChannel ，实现 AbstractChannel 抽象类，**封装 Netty Channel** 的通道实现类。

NettyChannel 和 HeaderExchangeChannel 很类似。

**构造方法**

```plain text
plain /**  * 通道集合  */ private static final ConcurrentMap<io.netty.channel.Channel, NettyChannel> channelMap = new ConcurrentHashMap<Channel, NettyChannel>();  /**  * 通道  */ private final io.netty.channel.Channel channel; /**  * 属性集合  */ private final Map<String, Object> attributes = new ConcurrentHashMap<String, Object>();  private NettyChannel(io.netty.channel.Channel channel, URL url, ChannelHandler handler) {     super(url, handler);     if (channel == null) {         throw new IllegalArgumentException("netty channel == null;");     }     this.channel = channel; }
```

---

- channel**装饰器**
属性，通道。NettyChannel 是传入
channel
属性的
，每个实现的方法，都会调用
channel
。
- attributes**注意**
属性，属性集合。
，
setAttribute(…)
等方法，使用的是该属性，而不是
io.netty.channel.Channel
的。
- channelMap**静态**
属性，通道集合。在实际 Netty Handler 里（例如下面我们会看到的 NettyServerHandler 和 NettyClientHandler），每个方法参数里，传递的是
io.netty.channel.Channel
对象。通过
NettyChannel.channelMap
中，获得对应的 NettyChannel 对象。
    - #getOrAddChannel(ch, url, handler)**静态**
方法，创建 NettyChannel 对象。代码如下：

```plain text
plain static NettyChannel getOrAddChannel(io.netty.channel.Channel ch, URL url, ChannelHandler handler) {     if (ch == null) {         return null;     }     NettyChannel ret = channelMap.get(ch);     if (ret == null) {         NettyChannel nettyChannel = new NettyChannel(ch, url, handler);         if (ch.isActive()) { // 连接中             ret = channelMap.putIfAbsent(ch, nettyChannel); // 添加到 channelMap         }         if (ret == null) {             ret = nettyChannel;         }     }     return ret; }
```

---

```plain text
    * <font style="color:rgb(51, 51, 51);">x</font>
- <font style="color:rgb(51, 51, 51);">#removeChannelIfDisconnected(ch)</font>**<font style="color:rgb(51, 51, 51);">静态</font>**<font style="color:rgb(51, 51, 51);">方法，移除 NettyChannel 对象。代码如下：</font>
```

```plain text
plain static void removeChannelIfDisconnected(io.netty.channel.Channel ch) {     if (ch != null && !ch.isActive()) { // 未连接         channelMap.remove(ch); // 移除出channelMap     } }
```

---

```plain text
    * <font style="color:rgb(51, 51, 51);">x</font>
```

**发送消息**

```plain text
plain 1: @Override  2: public void send(Object message, boolean sent) throws RemotingException {  3:     // 检查连接状态  4:     super.send(message, sent);  5:   6:     boolean success = true; // 如果没有等待发送成功，默认成功。  7:     int timeout = 0;  8:     try {  9:         // 发送消息 10:         ChannelFuture future = channel.writeAndFlush(message); 11:         // 等待发送成功 12:         if (sent) { 13:             timeout = getUrl().getPositiveParameter(Constants.TIMEOUT_KEY, Constants.DEFAULT_TIMEOUT); 14:             success = future.await(timeout); 15:         } 16:         // 若发生异常，抛出 17:         Throwable cause = future.cause(); 18:         if (cause != null) { 19:             throw cause; 20:         } 21:     } catch (Throwable e) { 22:         throw new RemotingException(this, "Failed to send message " + message + " to " + getRemoteAddress() + ", cause: " + e.getMessage(), e); 23:     } 24:  25:     // 发送失败，抛出异常 26:     if (!success) { 27:         throw new RemotingException(this, "Failed to send message " + message + " to " + getRemoteAddress() 28:                 + "in timeout(" + timeout + "ms) limit"); 29:     } 30: }
```

---

- 第 4 行：调用
#send(message, sent)
方法，检查连接状态。
- 第 6 行：
success
，是否执行成功。若不需要等待发送成功(
sent = false
) ，默认成功。
- 第 10 行：调用**真正的**
io.netty.channel.Channel#writeAndFlush(message)
方法，发送消息。
- 第 11 至 15 行：若需要等待发送成功(
sent = true
)，等待直到成功或超时。
- 第 16 至 20 行：若发生异常，抛出异常。
- 第 26 至 29 行：若发送失败，抛出异常。

**关闭通道**

```plain text
plain @Override @SuppressWarnings("Duplicates") public void close() {     // 标记关闭     try {         super.close();     } catch (Exception e) {         logger.warn(e.getMessage(), e);     }     // 移除连接     try {         removeChannelIfDisconnected(channel);     } catch (Exception e) {         logger.warn(e.getMessage(), e);     }     // 清空属性 attributes     try {         attributes.clear();     } catch (Exception e) {         logger.warn(e.getMessage(), e);     }     // 关闭真正的通道 channel     try {         if (logger.isInfoEnabled()) {             logger.info("Close netty channel " + channel);         }         channel.close();     } catch (Exception e) {         logger.warn(e.getMessage(), e);     } }
```

---

- **注意**
，最后一步才关闭真正的通道，避免中间状态。

**其它方法**

其它实现方法，比较简单，胖友自己瞅瞅。例如：

```plain text
plain @Override public boolean isConnected() {     return !isClosed() && channel.isActive(); }
```

---

# 4. Server

## 4.1 NettyServer

[com.alibaba.dubbo.remoting.transport.netty4.NettyServer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyServer.java) ，实现 Server 接口，继承 AbstractServer 抽象类，Netty 服务器实现类。

**构造方法**

```plain text
plain /**  * 通道集合  */ private Map<String, Channel> channels; // <ip:port, channel>  private ServerBootstrap bootstrap;  private io.netty.channel.Channel channel;  private EventLoopGroup bossGroup; private EventLoopGroup workerGroup;  public NettyServer(URL url, ChannelHandler handler) throws RemotingException {     super(url, ChannelHandlers.wrap(handler, ExecutorUtil.setThreadName(url, SERVER_THREAD_POOL_NAME) /* 设置线程名到 URL 上 */)); }
```

---

- channels**指定地址**
属性，连接到服务器的客户端通道集合。笔者在看 NettyChannel 时，在有
NettyChannel.channels
，那么此处的
channels
不是重复了么？答案在
#getChannel(remoteAddress)
方法，获得
的 Channel 对象。代码如下：

```plain text
plain @Override public Channel getChannel(InetSocketAddress remoteAddress) {     return channels.get(NetUtils.toAddressString(remoteAddress)); }
```

---

- bootstrap
channel
bossGroup
workerGroup
属性， 不熟悉这几个的胖友，请 Google 一下 Netty 入门噶。
- ChannelHandlers.wrap(handler, ExecutorUtil.setThreadName(url, SERVER_THREAD_POOL_NAME)
代码段，包装 ChannelHandler ，实现 Dubbo 线程模型的功能。
    - [《精尽 Dubbo 源码分析 —— NIO 服务器（二）之 Transport 层》「8. Dispacher」](http://svip.iocoder.cn/Dubbo/remoting-api-transport/?self=)
有详细解析。
    - [《Dubbo 用户指南 —— 线程模型》](http://dubbo.apache.org/zh-cn/docs/user/demos/thread-model.html)

**启动服务器**

```plain text
plain 1: @Override  2: protected void doOpen() {  3:     // 设置日志工厂  4:     NettyHelper.setNettyLoggerFactory();  5:   6:     // 实例化 ServerBootstrap  7:     bootstrap = new ServerBootstrap();  8:   9:     // 创建线程组 10:     bossGroup = new NioEventLoopGroup(1, new DefaultThreadFactory("NettyServerBoss", true)); 11:     workerGroup = new NioEventLoopGroup(getUrl().getPositiveParameter(Constants.IO_THREADS_KEY, Constants.DEFAULT_IO_THREADS), 12:             new DefaultThreadFactory("NettyServerWorker", true)); 13:  14:     // 创建 NettyServerHandler 对象 15:     final NettyServerHandler nettyServerHandler = new NettyServerHandler(getUrl(), this); 16:     // 设置 `channels` 属性 17:     channels = nettyServerHandler.getChannels(); 18:  19:     bootstrap 20:             // 设置它的线程组 21:             .group(bossGroup, workerGroup) 22:             // 设置 Channel类型 23:             .channel(NioServerSocketChannel.class) // Server 24:             // 设置可选项 25:             .childOption(ChannelOption.TCP_NODELAY, Boolean.TRUE) 26:             .childOption(ChannelOption.SO_REUSEADDR, Boolean.TRUE) 27:             .childOption(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT) 28:             // 设置责任链路 29:             .childHandler(new ChannelInitializer<NioSocketChannel>() { 30:                 @Override 31:                 protected void initChannel(NioSocketChannel ch) { 32:                     // 创建 NettyCodecAdapter 对象 33:                     NettyCodecAdapter adapter = new NettyCodecAdapter(getCodec(), getUrl(), NettyServer.this); 34:                     ch.pipeline()//.addLast("logging",new LoggingHandler(LogLevel.INFO))//for debug 35:                             .addLast("decoder", adapter.getDecoder()) // 解码 36:                             .addLast("encoder", adapter.getEncoder())  // 解码 37:                             .addLast("handler", nettyServerHandler); // 处理器 38:                 } 39:             }); 40:  41:     // 服务器绑定端口监听 42:     // bind 43:     ChannelFuture channelFuture = bootstrap.bind(getBindAddress()); 44:     channelFuture.syncUninterruptibly(); 45:     channel = channelFuture.channel(); 46: }
```

---

- 参考：[《Netty4.x中文教程系列(六) 从头开始Bootstrap》](https://tinyzzh.github.io/netty/2014/08/12/Netty4.x_6.html)
- 第 4 行：设置 Netty 的日志工厂，在 [「7. 日志处理」](http://svip.iocoder.cn/Dubbo/remoting-impl-netty4/#)
详细解析。
- 第 7 行：实例化 ServerBootstrap 对象。
- 第 9 至 12 行：创建
bossGroup
workerGroup
线程组。
- 第 15 行：创建 NettyServerHandler 对象。
- 第 17 行：设置
channels
属性，指向
NettyServerHandler.channels
属性。
- 第 21 行：设置线程组。
- 第 23 行：设置 Channel 类型为 NioServerSocketChannel 。
- 第 24 至 27 行：设置可选项。
    - PooledByteBufAllocator.DEFAULT[《Netty 调优》](http://huangdongrong.github.io/2016/05/24/netty-jvm/)
，对象池，重用缓冲区。参见
。
- 第 29 至 39 行：设置责任链。
    - 第 33 行：创建 NettyCodecAdapter 对象。NettyCodecAdapter 在 [「6. 2 NettyCodecAdapter」](http://svip.iocoder.cn/Dubbo/remoting-impl-netty4/#)
详细解析。
    - 第 35 行：调用
NettyCodecAdapter#getDecoder()
方法，获得解码器，并设置。
    - 第 37 行：调用
NettyCodecAdapter#getEncoder()
方法，获得编码器，并设置。
    - 第 37 行：设置处理器
handler
。
- 第 41 至 45 行：服务器绑定端口监听，**正式启动**
啦。

**获得所有通道**

```plain text
plain public Collection<Channel> getChannels() {     Collection<Channel> chs = new HashSet<Channel>();     for (Channel channel : this.channels.values()) {         if (channel.isConnected()) { // 已连接，返回             chs.add(channel);         } else { // 未连接，移除             channels.remove(NetUtils.toAddressString(channel.getRemoteAddress()));         }     }     return chs; }
```

---

**关闭服务器**

```plain text
plain 1: @Override  2: protected void doClose() {  3:     // 关闭服务器通道  4:     try {  5:         if (channel != null) {  6:             // unbind.  7:             channel.close();  8:         }  9:     } catch (Throwable e) { 10:         logger.warn(e.getMessage(), e); 11:     } 12:     // 关闭连接到服务器的客户端通道 13:     try { 14:         Collection<com.alibaba.dubbo.remoting.Channel> channels = getChannels(); 15:         if (channels != null && channels.size() > 0) { 16:             for (com.alibaba.dubbo.remoting.Channel channel : channels) { 17:                 try { 18:                     channel.close(); 19:                 } catch (Throwable e) { 20:                     logger.warn(e.getMessage(), e); 21:                 } 22:             } 23:         } 24:     } catch (Throwable e) { 25:         logger.warn(e.getMessage(), e); 26:     } 27:     // 优雅关闭工作组 28:     try { 29:         if (bootstrap != null) { 30:             bossGroup.shutdownGracefully(); 31:             workerGroup.shutdownGracefully(); 32:         } 33:     } catch (Throwable e) { 34:         logger.warn(e.getMessage(), e); 35:     } 36:     // 清空连接到服务器的客户端通道 37:     try { 38:         if (channels != null) { 39:             channels.clear(); 40:         } 41:     } catch (Throwable e) { 42:         logger.warn(e.getMessage(), e); 43:     } 44: }
```

---

- 第 3 至 11 行：关闭服务器通道(
io.netty.channel.Channel
)。
- 第 12 至 26 行：关闭连接到服务器的客户端通道(
com.alibaba.dubbo.remoting.Channel
) 。
- 第 27 至 35 行：优雅关闭工作组。
- 第 36 至 43 行：清空连接到服务器的客户端通道。

## 4.2 NettyServerHandler

[com.alibaba.dubbo.remoting.transport.netty4.NettyServerHandler](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyServerHandler.java) ，实现 io.netty.channel.ChannelDuplexHandler 类，NettyServer 的处理器。

NettyServerHandler 和 HeaderExchangeHandler 类似。

**构造方法**

```plain text
plain @io.netty.channel.ChannelHandler.Sharable public class NettyServerHandler extends ChannelDuplexHandler {      /**      * Dubbo Channel 集合      */     private final Map<String, Channel> channels = new ConcurrentHashMap<String, Channel>(); // <ip:port, channel>     /**      * URL      */     private final URL url;     /**      * Dubbo ChannelHandler      */     private final ChannelHandler handler;      public NettyServerHandler(URL url, ChannelHandler handler) {         if (url == null) {             throw new IllegalArgumentException("url == null");         }         if (handler == null) {             throw new IllegalArgumentException("handler == null");         }         this.url = url;         this.handler = handler;     }          // ... 省略实现方法      }
```

---

- [`@io.netty.channel.ChannelHandler.Sharable](http://svip.iocoder.cn/Dubbo/remoting-impl-netty4/mailto:%60@io.netty.channel.ChannelHandler.Sharable)<font style="color:rgb(51, 51, 51);">` 注解：[《netty4中注解Sharable的使用场景？》](https://www.zhihu.com/question/50198921)
FROM
Sharable 注解主要是用来标示一个 ChannelHandler 可以被安全地共享，即可以在多个Channel 的 ChannelPipeline 中使用同一个ChannelHandler ，而不必每一个ChannelPipeline 都重新 new 一个新的 ChannelHandler 。
- channels
属性，连接到服务器的 Dubbo Channel 集合。
- handler
属性，Dubbo ChannelHandler。NettyServerHandler 对每个事件的处理，会调用
handler
对应的方法。

**实现方法**

每个实现的方法，处理都比较类似，一般是提交给 handler 做相应的处理。艿艿已经添加了代码注释，胖友可以自己看看。下面以 #channelActive(ChannelHandlerContext) 方法举例子，代码如下：

```plain text
plain 1: @Override  2: public void channelActive(ChannelHandlerContext ctx) throws Exception {  3:     // 交给下一个节点处理  4:     // 芋艿：实际此处不要调用也没关系，因为 NettyServerHandler 没下一个节点。  5:     ctx.fireChannelActive();  6:   7:     // 创建 NettyChannel 对象  8:     NettyChannel channel = NettyChannel.getOrAddChannel(ctx.channel(), url, handler);  9:     try { 10:         // 添加到 `channels` 中 11:         if (channel != null) { 12:             channels.put(NetUtils.toAddressString((InetSocketAddress) ctx.channel().remoteAddress()), channel); 13:         } 14:         // 提交给 `handler` 处理器。 15:         handler.connected(channel); 16:     } finally { 17:         // 移除 NettyChannel 对象，若已断开 18:         NettyChannel.removeChannelIfDisconnected(ctx.channel()); 19:     } 20: }
```

---

- [《Netty 框架总结「ChannelHandler 及 EventLoop」》](https://www.jianshu.com/p/88ffafa23221)
- 第 5 行：调用 **此处不要调用也没关系**
ChannelHandlerContext#fireChannelActive()
方法，交给下一个节点处理。实际上，
，因为 NettyServerHandler 没下一个节点。
- 第 8 行：调用
NettyChannel#getOrAddChannel(channel, url, handler)
方法，创建 NettyChannel 对象。
- 第 10 至 13 行：添加到
channels
中。
- 第 15 行：调用
ChannelHandler#connected(channel)
方法，处理连接事件。
- 第 16 至 19 行：调用 **已断开**
NettyChannel#removeChannelIfDisconnected(channel)
方法，移除 NettyChannel 对象，若
。

# 5. Client

## 5.1 NettyClient

[com.alibaba.dubbo.remoting.transport.netty4.NettyClient](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyClient.java) ，继承 AbstractNettyClient 抽象类，Netty 客户端实现类。

**构造方法**

```plain text
plain // 【TODO 8027】为啥公用 private static final NioEventLoopGroup nioEventLoopGroup = new NioEventLoopGroup(Constants.DEFAULT_IO_THREADS, new DefaultThreadFactory("NettyClientWorker", true));  private Bootstrap bootstrap;  private volatile io.netty.channel.Channel channel; // volatile, please copy reference to use  public NettyClient(final URL url, final ChannelHandler handler) throws RemotingException {     super(url, wrapChannelHandler(url, handler)); }
```

---

- nioEventLoopGroup
属性，【TODO 8027】为啥公用
- channel**volatile多线程**
属性，通道，有
修饰符。因为客户端可能会断开重连，需要保证
的可见性。
- #wrapChannelHandler(url, handler)
代码段，包装 ChannelHandler ，实现 Dubbo 线程模型的功能。
    - [《精尽 Dubbo 源码分析 —— NIO 服务器（二）之 Transport 层》「8. Dispacher」](http://svip.iocoder.cn/Dubbo/remoting-api-transport/?self=)
有详细解析。
    - [《Dubbo 用户指南 —— 线程模型》](http://dubbo.apache.org/zh-cn/docs/user/demos/thread-model.html)

**启动客户端**

```plain text
plain 1: @Override  2: protected void doOpen() {  3:     // 设置日志工厂  4:     NettyHelper.setNettyLoggerFactory();  5:   6:     // 创建 NettyClientHandler 对象  7:     final NettyClientHandler nettyClientHandler = new NettyClientHandler(getUrl(), this);  8:   9:     // 实例化 ServerBootstrap 10:     bootstrap = new Bootstrap(); 11:     bootstrap 12:             // 设置它的线程组 13:             .group(nioEventLoopGroup) 14:             // 设置可选项 15:             .option(ChannelOption.SO_KEEPALIVE, true) 16:             .option(ChannelOption.TCP_NODELAY, true) 17:             .option(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT) 18:             //.option(ChannelOption.CONNECT_TIMEOUT_MILLIS, getTimeout()) 19:             // 设置 Channel类型 20:             .channel(NioSocketChannel.class); 21:  22:     // 设置连接超时时间 23:     if (getTimeout() < 3000) { 24:         bootstrap.option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 3000); 25:     } else { 26:         bootstrap.option(ChannelOption.CONNECT_TIMEOUT_MILLIS, getTimeout()); 27:     } 28:  29:     // 设置责任链路 30:     bootstrap.handler(new ChannelInitializer() { 31:         @Override 32:         protected void initChannel(Channel ch) { 33:             // 创建 NettyCodecAdapter 对象 34:             NettyCodecAdapter adapter = new NettyCodecAdapter(getCodec(), getUrl(), NettyClient.this); 35:             ch.pipeline()//.addLast("logging",new LoggingHandler(LogLevel.INFO))//for debug 36:                     .addLast("decoder", adapter.getDecoder()) // 解码 37:                     .addLast("encoder", adapter.getEncoder()) // 解码 38:                     .addLast("handler", nettyClientHandler); // 处理器 39:         } 40:     }); 41: }
```

---

- 和
NettyClient#doOpen()
方法类似。我们仅仅说一些差异点。
- 第 7 行：创建 NettyClientHandler 对象。
- 第 13 行：设置线程组，没有
bossGroup
。
- 第 20 行：设置 Channel 类型为 NioSocketChannel 。
- 第 22 至 27 行：设置连接超时时间。

**连接服务器**

```plain text
plain 1: @Override  2: @SuppressWarnings("Duplicates")  3: protected void doConnect() throws Throwable {  4:     long start = System.currentTimeMillis();  5:     // 连接服务器  6:     ChannelFuture future = bootstrap.connect(getConnectAddress());  7:     try {  8:         // 等待连接成功或者超时  9:         boolean ret = future.awaitUninterruptibly(3000, TimeUnit.MILLISECONDS); 10:         // 连接成功 11:         if (ret && future.isSuccess()) { 12:             Channel newChannel = future.channel(); 13:             try { 14:                 // 关闭老的连接 15:                 // Close old channel 16:                 Channel oldChannel = NettyClient.this.channel; // copy reference 17:                 if (oldChannel != null) { 18:                     try { 19:                         if (logger.isInfoEnabled()) { 20:                             logger.info("Close old netty channel " + oldChannel + " on create new netty channel " + newChannel); 21:                         } 22:                         oldChannel.close(); 23:                     } finally { 24:                         NettyChannel.removeChannelIfDisconnected(oldChannel); 25:                     } 26:                 } 27:             } finally { 28:                 // 若 NettyClient 被关闭，关闭连接 29:                 if (NettyClient.this.isClosed()) { 30:                     try { 31:                         if (logger.isInfoEnabled()) { 32:                             logger.info("Close new netty channel " + newChannel + ", because the client closed."); 33:                         } 34:                         newChannel.close(); 35:                     } finally { 36:                         NettyClient.this.channel = null; 37:                         NettyChannel.removeChannelIfDisconnected(newChannel); 38:                     } 39:                 // 设置新连接 40:                 } else { 41:                     NettyClient.this.channel = newChannel; 42:                 } 43:             } 44:         // 发生异常，抛出 RemotingException 异常 45:         } else if (future.cause() != null) { 46:             throw new RemotingException(this, "client(url: " + getUrl() + ") failed to connect to server " 47:                     + getRemoteAddress() + ", error message is:" + future.cause().getMessage(), future.cause()); 48:         // 无结果（连接超时），抛出 RemotingException 异常 49:         } else { 50:             throw new RemotingException(this, "client(url: " + getUrl() + ") failed to connect to server " 51:                     + getRemoteAddress() + " client-side timeout " 52:                     + getConnectTimeout() + "ms (elapsed: " + (System.currentTimeMillis() - start) + "ms) from netty client " 53:                     + NetUtils.getLocalHost() + " using dubbo version " + Version.getVersion()); 54:         } 55:     } finally { 56:         if (!isConnected()) { 57:             //future.cancel(true); 58:         } 59:     } 60: }
```

---

- 第 6 行：调用
Bootstrap#connect(remoteAddress)
方法，连接服务器。
- 第 9 行：调用
ChannelFuture#awaitUninterruptibly(3000, TimeUnit)
方法，等待连接成功或超时。这里传入
3000
貌似不太正确，应该传入
ChannelOption.CONNECT_TIMEOUT_MILLIS
的实际值。
- 第 10 至 43 行：连接成功。
    - 第 14 至 26 行：若存在**老的**
连接，调用
Channel#close()
方法，进行关闭。
    - 第 29 至 38 行：若 NettyClient 被关闭，调用 **新的连接**
Channel#close()
方法，关闭
。
    - 第 39 至 42 行：设置**新的连接**
到
channel
。
- 第 44 至 47 行：发生异常，抛出 **Server**
RemotingException 异常。
- 第 48 至 54 行：无结果（连接超时），抛出 **Client**
RemotingException 异常。
- 第 55 至 59 行：// 【TODO 8028】为什么不取消 future TODO 可能，和 3000 有关系。< 3000 强制 3000 。以及等待 3000

**断开连接**

```plain text
plain @Override protected void doDisConnect() {     try {         NettyChannel.removeChannelIfDisconnected(channel);     } catch (Throwable t) {         logger.warn(t.getMessage());     } }
```

---

**关闭连接**

```plain text
plain @Override protected void doClose() throws Throwable {     //can't shutdown nioEventLoopGroup     //nioEventLoopGroup.shutdownGracefully(); }
```

---

## 5.2 NettyClientHandler

[com.alibaba.dubbo.remoting.transport.netty4.NettyClientHandler](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyClientHandler.java) ，实现 io.netty.channel.ChannelDuplexHandler 类，NettyClient 的处理器。

NettyServerHandler 和 HeaderExchangeHandler 类似。

**构造方法**

```plain text
plain @io.netty.channel.ChannelHandler.Sharable public class NettyClientHandler extends ChannelDuplexHandler {      /**      * Dubbo URL      */     private final URL url;     /**      * Dubbo ChannelHandler      */     private final ChannelHandler handler;      public NettyClientHandler(URL url, ChannelHandler handler) {         if (url == null) {             throw new IllegalArgumentException("url == null");         }         if (handler == null) {             throw new IllegalArgumentException("handler == null");         }         this.url = url;         this.handler = handler;     }          // ... 省略实现方法 }
```

---

**实现方法**

NettyClientHandler 的**处理方式**，和 NettyServerHandler 大体一致，但是也存在**一定的差异**，以 #channelActive(ChannelHandlerContext) 方法举例子，代码如下：

```plain text
plain @Override public void channelActive(ChannelHandlerContext ctx) {     ctx.fireChannelActive(); }
```

---

- 不同于 NettyServerHandler 的该方法，会提交给
handler
继续处理。因为，客户端不会被连接，无需做连入 Channel 的管理。

其他方法，胖友自己查看。

# 6. NettyBackedChannelBuffer

[com.alibaba.dubbo.remoting.transport.netty4.NettyBackedChannelBuffer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyBackedChannelBuffer.java) ，实现 ChannelBuffer 接口，基于 **Netty ByteBuf** 的 ChannelBuffer 实现类。

**构造方法**

```plain text
plain private ByteBuf buffer;  public NettyBackedChannelBuffer(ByteBuf buffer) {     Assert.notNull(buffer, "buffer == null");     this.buffer = buffer; }
```

---

- [《ByteBuf - 字节数据的容器》](https://waylau.gitbooks.io/essential-netty-in-action/CORE%20FUNCTIONS/ByteBuf%20-%20The%20byte%20data%20container.html)

**工厂**

```plain text
plain @Override //has nothing use public ChannelBufferFactory factory() {     return null; }
```

---

- 无使用工厂的地方。
- 另外，ByteBuf 默认情况下，容量为 Integer.MAX_VALUE 。

**实现方法**

每个方法，直接调用 ByteBuf 对应的方法。 ChannelBuffer 是以 ByteBuf 为**原型**，设计的接口 API 。

# 7. NettyCodecAdapter

[com.alibaba.dubbo.remoting.transport.netty4.NettyCodecAdapter](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyCodecAdapter.java) ，Netty 编解码**适配器**，将 **Dubbo 编解码器** 适配成 Netty4 的编码器和解码器。

**构造方法**

```plain text
plain /**  * Netty 编码器  */ private final ChannelHandler encoder = new InternalEncoder(); /**  * Netty 解码器  */ private final ChannelHandler decoder = new InternalDecoder();  /**  * Dubbo 编解码器  */ private final Codec2 codec; /**  * Dubbo URL  */ private final URL url; /**  * Dubbo ChannelHandler  */ private final com.alibaba.dubbo.remoting.ChannelHandler handler;  public NettyCodecAdapter(Codec2 codec, URL url, com.alibaba.dubbo.remoting.ChannelHandler handler) {     this.codec = codec;     this.url = url;     this.handler = handler; }
```

---

## 7.1 InternalEncoder

```plain text
plain private class InternalEncoder extends MessageToByteEncoder {      @Override     protected void encode(ChannelHandlerContext ctx, Object msg, ByteBuf out) throws Exception {         // 创建 NettyBackedChannelBuffer 对象         com.alibaba.dubbo.remoting.buffer.ChannelBuffer buffer = new NettyBackedChannelBuffer(out);         // 获得 NettyChannel 对象         Channel ch = ctx.channel();         NettyChannel channel = NettyChannel.getOrAddChannel(ch, url, handler);         try {             // 编码             codec.encode(channel, buffer, msg);         } finally {             // 移除 NettyChannel 对象，若断开连接             NettyChannel.removeChannelIfDisconnected(ch);         }     }  }
```

---

- io.netty.handler.codec.MessageToByteEncoder**抽象类**
，Netty4 编码器
。
- 代码比较简单，胖友自己看注释。

## 7.2 InternalDecoder

```plain text
plain private class InternalDecoder extends ByteToMessageDecoder {      @Override     protected void decode(ChannelHandlerContext ctx, ByteBuf input, List<Object> out) throws Exception {         // 创建 NettyBackedChannelBuffer 对象         ChannelBuffer message = new NettyBackedChannelBuffer(input);         // 获得 NettyChannel 对象         NettyChannel channel = NettyChannel.getOrAddChannel(ctx.channel(), url, handler);         // 循环解析，直到结束         Object msg;         int saveReaderIndex;         try {             // decode object.             do {                 // 记录当前读进度                 saveReaderIndex = message.readerIndex();                 // 解码                 try {                     msg = codec.decode(channel, message);                 } catch (IOException e) {                     throw e;                 }                 // 需要更多输入，即消息不完整，标记回原有读进度，并结束                 if (msg == Codec2.DecodeResult.NEED_MORE_INPUT) {                     message.readerIndex(saveReaderIndex);                     break;                 // 解码到消息，添加到 `out`                 } else {                     //is it possible to go here ? 芋艿：不可能，哈哈哈                     if (saveReaderIndex == message.readerIndex()) {                         throw new IOException("Decode without read data.");                     }                     if (msg != null) {                         out.add(msg);                     }                 }             } while (message.readable());         } finally {             // 移除 NettyChannel 对象，若断开连接             NettyChannel.removeChannelIfDisconnected(ctx.channel());         }     } }
```

---

- io.netty.handler.codec.ByteToMessageDecoder**抽象类**
，Netty4 解码器
。
- 代码比较简单，胖友自己看注释。

# 8. 日志工厂

在 [《Dubbo 用户指南 —— 日志适配》](http://dubbo.apache.org/zh-cn/docs/user/demos/logger-strategy.html) 文档，提到：

自 2.2.1 开始，dubbo 开始内置 log4j、slf4j、jcl、jdk 这些日志框架的适配。

在 [《Netty源码笔记 —— Netty日志处理》](https://www.kancloud.cn/ssj234/netty-source/433218) 文档，我们可以看到 Netty 支持实现自定义的**日志工厂**。通过这样的方式，我们可以接入 Dubbo 的**日志适配**。

下面，我们来看看具体的代码实现。

调用 NettyHelper#setNettyLoggerFactory() 方法，设置日志工厂，基于 Dubbo Logger 组件。代码如下：

```plain text
plain public static void setNettyLoggerFactory() {     InternalLoggerFactory factory = InternalLoggerFactory.getDefaultFactory();     if (factory == null || !(factory instanceof DubboLoggerFactory)) {         InternalLoggerFactory.setDefaultFactory(new DubboLoggerFactory());     } }
```

---

- 设置 Netty 日志工厂为 DubboLoggerFactory 。

---

[DubboLoggerFactory](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/logging/NettyHelper.java#L27-L32) ，代码如下：

```plain text
plain static class DubboLoggerFactory extends InternalLoggerFactory {      @Override     public InternalLogger newInstance(String name) {         return new DubboLogger(LoggerFactory.getLogger(name));     }  }
```

---

- 创建 DubboLogger 对象，并传入 [Logger](https://github.com/YunaiV/dubbo/blob/master/dubbo-common/src/main/java/com/alibaba/dubbo/common/logger/Logger.java)
name
对应的 Dubbo
对象，而 Dubbo Logger 的对象，基于 Dubbo SPI 机制加载。

---

[DubboLogger](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/logging/NettyHelper.java#L42-L236) ，代码如下：

```plain text
plain static class DubboLogger extends AbstractInternalLogger {      /**      * 日志组件      */     private com.alibaba.dubbo.common.logger.Logger logger;      DubboLogger(Logger logger) {         super(logger.getClass().getName());         this.logger = logger;     }          @Override     public void info(String msg) {         if (isInfoEnabled()) {             logger.info(msg);         }     }          // ... 省略类似代码 }
```

---

- 在实现的每个方法中，直接调用
logger
对应的方法。
- 在类似
#info(String format, Object… arguments)
方法中，需要对日志内容进行格式化，代码如下：

```plain text
plain @Override public void info(String format, Object... arguments) {     if (isInfoEnabled()) {         FormattingTuple ft = MessageFormatter.arrayFormat(format, arguments);         logger.info(ft.getMessage(), ft.getThrowable());     } }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">我们看到需要 </font>[FormattingTuple](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/logging/MessageFormatter.java)<font style="color:rgb(51, 51, 51);"> 和 </font>[MessageFormatter](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/logging/MessageFormatter.java)<font style="color:rgb(51, 51, 51);"> 这两个类，用于格式化。实际上，这两个类是直接从 Netty4 中拷贝出来的两个类，因为它们是 </font><font style="color:rgb(51, 51, 51);">package</font><font style="color:rgb(51, 51, 51);"> 修饰的类，在 DubboLogger 中，无法访问到它们，所以进行复制解决。</font>
```