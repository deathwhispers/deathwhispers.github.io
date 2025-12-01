---
layout: post
title: NIO服务器（七）之Netty3实现
slug: dubbo-nio-server-netty3
type:
  - note
date: 2022-06-02
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-06-02 11:49
updated: 2022-06-02 18:33
---
本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文接 [《精尽 Dubbo 源码分析 —— NIO 服务器（六）之 Netty4 实现》](http://svip.iocoder.cn/Dubbo/remoting-impl-netty4/?self=) 一文，分享在 dubbo-remoting-netty 中，Netty3 如何接入实现。

因为 Netty3 的接入代码，和 Netty4 基本是一致，主要是一些 Netty 不同版本的 API 差异，所以本文，会相对简介，只重点分享一些差异的地方。

涉及如下类：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038299499-85473855-ddd8-4833-8a3e-13df6de7d838.png)

类图

友情提示：在当前版本，默认情况下，使用 Netty3 ，如果想配置成 Netty4 ，请参考文档：[《Dubbo 用户指南 —— Netty4》](http://dubbo.apache.org/zh-cn/docs/user/demos/netty4.html)

# 2. NettyTransporter

[com.alibaba.dubbo.remoting.transport.netty.NettyTransporter](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyTransporter.java) ，和 dubbo-remoting-netty4 一致，省略。

# 3. NettyChannel

[com.alibaba.dubbo.remoting.transport.netty.NettyChannel](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyChannel.java) ，和 dubbo-remoting-netty4 一致，省略。

# 4. NettyHandler

[com.alibaba.dubbo.remoting.transport.netty.NettyHandler](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyHandler.java) ，实现 io.netty.channel.ChannelDuplexHandler 类，NettyServer 和 NettyClient 的处理器，**统一使用**。这一点，不同于 dubbo-remoting-netty4 ，服务端和服务器使用不同的两个处理器。相比来说，dubbo-remoting-netty4 控制更精细，影响不大。

当然也有一个原因，Dubbo ChannelHandler 基于 **Netty3 的 SimpleChannelHandler** 为设计原型。因此，在 dubbo-remoting-netty4 中，需要将 DubboHandler 的方法，适配到 **Netty4 的 ChannelDuplexHandler** 的方法。

NettyHandler 和 HeaderExchangeHandler 类似。

**构造方法**

```plain text
plain @Sharable public class NettyHandler extends SimpleChannelHandler {      /**      * Dubbo Channel 集合      */     private final Map<String, Channel> channels = new ConcurrentHashMap<String, Channel>(); // <ip:port, channel>     /**      * URL      */     private final URL url;     /**      * Dubbo ChannelHandler      */     private final ChannelHandler handler;      public NettyHandler(URL url, ChannelHandler handler) {         if (url == null) {             throw new IllegalArgumentException("url == null");         }         if (handler == null) {             throw new IllegalArgumentException("handler == null");         }         this.url = url;         this.handler = handler;     }          // ... 省略实现方法 }
```

---

**实现方法**

每个实现的方法，调用 handler 对应的方法。以 #channelActive(ChannelHandlerContext) 方法举例子，代码如下：

```plain text
plain @Override public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e) throws Exception {     // 创建 NettyChannel 对象     NettyChannel channel = NettyChannel.getOrAddChannel(ctx.getChannel(), url, handler);     try {         // 添加到 `channels` 中         if (channel != null) {             channels.put(NetUtils.toAddressString((InetSocketAddress) ctx.getChannel().getRemoteAddress()), channel);         }         // 提交给 `handler` 处理器。         handler.connected(channel);     } finally {         // 移除 NettyChannel 对象，若已断开         NettyChannel.removeChannelIfDisconnected(ctx.getChannel());     } }
```

---

其他方法，胖友自己查看。

# 5. NettyServer

[com.alibaba.dubbo.remoting.transport.netty.NettyServer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyServer.java) ，实现 Server 接口，继承 AbstractServer 抽象类，Netty 服务器实现类。

**构造方法**

```plain text
plain /**  * 通道集合  */ private Map<String, Channel> channels; // <ip:port, channel>  private ServerBootstrap bootstrap;  private org.jboss.netty.channel.Channel channel;  public NettyServer(URL url, ChannelHandler handler) throws RemotingException {     super(url, ChannelHandlers.wrap(handler, ExecutorUtil.setThreadName(url, SERVER_THREAD_POOL_NAME))); }
```

---

- 和
dubbo-remoting-netty4
基本一致。

**启动服务器**

```plain text
plain 1: @Override  2: protected void doOpen() {  3:     // 设置日志工厂  4:     NettyHelper.setNettyLoggerFactory();  5:   6:     // 创建线程池  7:     ExecutorService boss = Executors.newCachedThreadPool(new NamedThreadFactory("NettyServerBoss", true));  8:     ExecutorService worker = Executors.newCachedThreadPool(new NamedThreadFactory("NettyServerWorker", true));  9:  10:     // 创建 ChannelFactory 对象 11:     ChannelFactory channelFactory = new NioServerSocketChannelFactory(boss, worker, getUrl().getPositiveParameter(Constants.IO_THREADS_KEY, Constants.DEFAULT_IO_THREADS)); 12:     // 实例化 ServerBootstrap 13:     bootstrap = new ServerBootstrap(channelFactory); 14:  15:     // 创建 NettyHandler 对象 16:     final NettyHandler nettyHandler = new NettyHandler(getUrl(), this); 17:     // 设置 `channels` 属性 18:     channels = nettyHandler.getChannels(); 19:     // https://issues.jboss.org/browse/NETTY-365 20:     // https://issues.jboss.org/browse/NETTY-379 21:     // final Timer timer = new HashedWheelTimer(new NamedThreadFactory("NettyIdleTimer", true)); 22:     bootstrap.setPipelineFactory(new ChannelPipelineFactory() { 23:         @Override 24:         public ChannelPipeline getPipeline() { 25:             // 创建 NettyCodecAdapter 对象 26:             NettyCodecAdapter adapter = new NettyCodecAdapter(getCodec(), getUrl(), NettyServer.this); 27:             ChannelPipeline pipeline = Channels.pipeline(); 28:             /*int idleTimeout = getIdleTimeout(); 29:             if (idleTimeout > 10000) { 30:                 pipeline.addLast("timer", new IdleStateHandler(timer, idleTimeout / 1000, 0, 0)); 31:             }*/ 32:             pipeline.addLast("decoder", adapter.getDecoder()); // 解码 33:             pipeline.addLast("encoder", adapter.getEncoder()); // 解码 34:             pipeline.addLast("handler", nettyHandler); // 处理器 35:             return pipeline; 36:         } 37:     }); 38:     // 服务器绑定端口监听 39:     // bind 40:     channel = bootstrap.bind(getBindAddress()); 41: }
```

---

- 和
dubbo-remoting-netty4
基本一致，下面只说一些差异的地方。
- 第 6 至 8 行：创建线程池，不同于
dubbo-remoting-netty4
中，创建线程组 NioEventLoopGroup 。
- 第 11 行：基于
boss
worker
，创建 ChannelFactory 对象。
- **并未设置**
ServerBootstrap 的可选项。

**关闭服务器**

```plain text
plain 1: @Override  2: protected void doClose() {  3:     // 关闭服务器通道  4:     try {  5:         if (channel != null) {  6:             // unbind.  7:             channel.close();  8:         }  9:     } catch (Throwable e) { 10:         logger.warn(e.getMessage(), e); 11:     } 12:     // 关闭连接到服务器的客户端通道 13:     try { 14:         Collection<com.alibaba.dubbo.remoting.Channel> channels = getChannels(); 15:         if (channels != null && !channels.isEmpty()) { 16:             for (com.alibaba.dubbo.remoting.Channel channel : channels) { 17:                 try { 18:                     channel.close(); 19:                 } catch (Throwable e) { 20:                     logger.warn(e.getMessage(), e); 21:                 } 22:             } 23:         } 24:     } catch (Throwable e) { 25:         logger.warn(e.getMessage(), e); 26:     } 27:     // 优雅关闭 ServerBootstrap 28:     try { 29:         if (bootstrap != null) { 30:             // release external resource. 31:             bootstrap.releaseExternalResources(); 32:         } 33:     } catch (Throwable e) { 34:         logger.warn(e.getMessage(), e); 35:     } 36:     // 清空连接到服务器的客户端通道 37:     try { 38:         if (channels != null) { 39:             channels.clear(); 40:         } 41:     } catch (Throwable e) { 42:         logger.warn(e.getMessage(), e); 43:     } 44: }
```

---

- 和
dubbo-remoting-netty4
基本一致，下面只说一些差异的地方。
- 第 27 至 35 行：调用
Bootstrap#releaseExternalResources()
方法，释放 ServerBootstrap 相关的资源。

# 6. NettyClient

[com.alibaba.dubbo.remoting.transport.netty.NettyClient](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyClient.java) ，继承 AbstractNettyClient 抽象类，Netty 客户端实现类。

**构造方法**

```plain text
plain // ChannelFactory's closure has a DirectMemory leak, using static to avoid // https://issues.jboss.org/browse/NETTY-424 private static final ChannelFactory channelFactory = new NioClientSocketChannelFactory(Executors.newCachedThreadPool(new NamedThreadFactory("NettyClientBoss", true)),         Executors.newCachedThreadPool(new NamedThreadFactory("NettyClientWorker", true)),         Constants.DEFAULT_IO_THREADS);  private ClientBootstrap bootstrap;  private volatile org.jboss.netty.channel.Channel channel; // volatile, please copy reference to use  public NettyClient(final URL url, final ChannelHandler handler) throws RemotingException {     super(url, wrapChannelHandler(url, handler)); }
```

---

- channelFactory
属性，【TODO 8027】为啥公用

**启动客户端**

```plain text
plain 1: @Override  2: protected void doOpen() {  3:     // 设置日志工厂  4:     NettyHelper.setNettyLoggerFactory();  5:   6:     // 实例化 ServerBootstrap  7:     bootstrap = new ClientBootstrap(channelFactory);  8:     // 设置可选项  9:     // config 10:     // @see org.jboss.netty.channel.socket.SocketChannelConfig 11:     bootstrap.setOption("keepAlive", true); 12:     bootstrap.setOption("tcpNoDelay", true); 13:     bootstrap.setOption("connectTimeoutMillis", getTimeout()); 14:  15:     // 创建 NettyHandler 对象 16:     final NettyHandler nettyHandler = new NettyHandler(getUrl(), this); 17:  18:     // 设置责任链路 19:     bootstrap.setPipelineFactory(new ChannelPipelineFactory() { 20:         public ChannelPipeline getPipeline() { 21:             // 创建 NettyCodecAdapter 对象 22:             NettyCodecAdapter adapter = new NettyCodecAdapter(getCodec(), getUrl(), NettyClient.this); 23:             ChannelPipeline pipeline = Channels.pipeline(); 24:             pipeline.addLast("decoder", adapter.getDecoder()); // 解码 25:             pipeline.addLast("encoder", adapter.getEncoder()); // 编码 26:             pipeline.addLast("handler", nettyHandler); // 处理器 27:             return pipeline; 28:         } 29:     }); 30: }
```

---

- 和
dubbo-remoting-netty4
基本一致。

**连接服务器**

```plain text
plain 1: @Override  2: protected void doConnect() throws Throwable {  3:     long start = System.currentTimeMillis();  4:     // 连接服务器  5:     ChannelFuture future = bootstrap.connect(getConnectAddress());  6:     try {  7:         // 等待连接成功或者超时  8:         boolean ret = future.awaitUninterruptibly(getConnectTimeout(), TimeUnit.MILLISECONDS);  9:         // 连接成功 10:         if (ret && future.isSuccess()) { 11:             Channel newChannel = future.getChannel(); 12:             newChannel.setInterestOps(Channel.OP_READ_WRITE); 13:             try { 14:                 // 关闭老的连接 15:                 // Close old channel 16:                 Channel oldChannel = NettyClient.this.channel; // copy reference 17:                 if (oldChannel != null) { 18:                     try { 19:                         if (logger.isInfoEnabled()) { 20:                             logger.info("Close old netty channel " + oldChannel + " on create new netty channel " + newChannel); 21:                         } 22:                         oldChannel.close(); 23:                     } finally { 24:                         NettyChannel.removeChannelIfDisconnected(oldChannel); 25:                     } 26:                 } 27:             } finally { 28:                 // 若 NettyClient 被关闭，关闭连接 29:                 if (NettyClient.this.isClosed()) { 30:                     try { 31:                         if (logger.isInfoEnabled()) { 32:                             logger.info("Close new netty channel " + newChannel + ", because the client closed."); 33:                         } 34:                         newChannel.close(); 35:                     } finally { 36:                         NettyClient.this.channel = null; 37:                         NettyChannel.removeChannelIfDisconnected(newChannel); 38:                     } 39:                 // 设置新连接 40:                 } else { 41:                     NettyClient.this.channel = newChannel; 42:                 } 43:             } 44:         // 发生异常，抛出 RemotingException 异常 45:         } else if (future.getCause() != null) { 46:             throw new RemotingException(this, "client(url: " + getUrl() + ") failed to connect to server " 47:                     + getRemoteAddress() + ", error message is:" + future.getCause().getMessage(), future.getCause()); 48:         // 无结果（连接超时），抛出 RemotingException 异常 49:         } else { 50:             throw new RemotingException(this, "client(url: " + getUrl() + ") failed to connect to server " 51:                     + getRemoteAddress() + " client-side timeout " 52:                     + getConnectTimeout() + "ms (elapsed: " + (System.currentTimeMillis() - start) + "ms) from netty client " 53:                     + NetUtils.getLocalHost() + " using dubbo version " + Version.getVersion()); 54:         } 55:     } finally { 56:         // 未连接，取消任务 57:         if (!isConnected()) { 58:             future.cancel(); 59:         } 60:     } 61: }
```

---

- 和
dubbo-remoting-netty4
基本一致，下面只说一些差异的地方。
- 第 9 行：调用
ChannelFuture#awaitUninterruptibly(timeout, TimeUnit)
方法，等待连接成功或超时。这里传入的不是
3000
。
- 第 55 至 60 行：最终结果为未连接，调用
ChannelFuture#cancel(true)
方法，取消任务。

**关闭连接**

```plain text
plain @Override protected void doClose() throws Throwable {     /*try {             bootstrap.releaseExternalResources();         } catch (Throwable t) {             logger.warn(t.getMessage());         }*/ }
```

---

- 因为 **静态**
channelFactory
是
属性，被多个 NettyClient 共用。

# 7. Buffer

## 7.1 NettyBackedChannelBuffer

[com.alibaba.dubbo.remoting.transport.netty.NettyBackedChannelBuffer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyBackedChannelBuffer.java) ，实现 ChannelBuffer 接口，基于 **Netty3 ChannelBuffer** 的 ChannelBuffer 实现类。

**构造方法**

```plain text
plain private org.jboss.netty.buffer.ChannelBuffer buffer;  public NettyBackedChannelBuffer(org.jboss.netty.buffer.ChannelBuffer buffer) {     Assert.notNull(buffer, "buffer == null");     this.buffer = buffer; }
```

---

**工厂**

```plain text
plain @Override public ChannelBufferFactory factory() {     return NettyBackedChannelBufferFactory.getInstance(); }
```

---

- 对应的工厂是 NettyBackedChannelBufferFactory

**实现方法**

每个方法，直接调用 Netty3 ChannelBuffer 对应的方法。

## 7.2 NettyBackedChannelBufferFactory

[com.alibaba.dubbo.remoting.transport.netty.NettyBackedChannelBufferFactory](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyBackedChannelBufferFactory.java) ，实现 ChannelBufferFactory 接口，创建 NettyBackedChannelBuffer 的工厂。代码如下：

```plain text
plain @Override public ChannelBuffer getBuffer(int capacity) {     return new NettyBackedChannelBuffer(ChannelBuffers.dynamicBuffer(capacity)); // ChannelBuffers 为 `org.jboss.netty.buffer` 包下 }  @Override public ChannelBuffer getBuffer(byte[] array, int offset, int length) {     // 创建 Netty3 ChannelBuffer 对象     org.jboss.netty.buffer.ChannelBuffer buffer = ChannelBuffers.dynamicBuffer(length); // ChannelBuffers 为 `org.jboss.netty.buffer` 包下     // 写入数据     buffer.writeBytes(array, offset, length);     // 创建 NettyBackedChannelBuffer 对象     return new NettyBackedChannelBuffer(buffer); }  @Override public ChannelBuffer getBuffer(ByteBuffer nioBuffer) {     return new NettyBackedChannelBuffer(ChannelBuffers.wrappedBuffer(nioBuffer)); // ChannelBuffers 为 `org.jboss.netty.buffer` 包下 }
```

---

- **注意**
，此处的 ChannelBuffers 是
org.jboss.netty.buffer
包下的。

# 8. NettyCodecAdapter

[com.alibaba.dubbo.remoting.transport.netty.NettyCodecAdapter](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyCodecAdapter.java) ，Netty 编解码**适配器**，将 **Dubbo 编解码器** 适配成 Netty3 的编码器和解码器。

**构造方法**

```plain text
plain /**  * Netty 编码器  */ private final ChannelHandler encoder = new InternalEncoder(); /**  * Netty 解码器  */ private final ChannelHandler decoder = new InternalDecoder();  /**  * Dubbo 编解码器  */ private final Codec2 codec; /**  * Dubbo URL  */ private final URL url; /**  * 网络读写缓冲区大小  */ private final int bufferSize; /**  * Dubbo ChannelHandler  */ private final com.alibaba.dubbo.remoting.ChannelHandler handler;  public NettyCodecAdapter(Codec2 codec, URL url, com.alibaba.dubbo.remoting.ChannelHandler handler) {     this.codec = codec;     this.url = url;     this.handler = handler;     // 设置 `bufferSize`     int b = url.getPositiveParameter(Constants.BUFFER_KEY, Constants.DEFAULT_BUFFER_SIZE);     this.bufferSize = b >= Constants.MIN_BUFFER_SIZE && b <= Constants.MAX_BUFFER_SIZE ? b : Constants.DEFAULT_BUFFER_SIZE; }
```

---

- bufferSize**不需要**[「8.2 InternalDecoder」](http://svip.iocoder.cn/Dubbo/remoting-impl-netty3/#)
属性，网络读写缓冲区大小，默认 8K 。这是
dubbo-remoting-netty4
的 NettyCodecAdapter 所
的。用于下面
，消息解码时使用。

## 8.1 InternalEncoder

```plain text
plain @Sharable private class InternalEncoder extends OneToOneEncoder {      @Override     protected Object encode(ChannelHandlerContext ctx, Channel ch, Object msg) throws Exception {         // 创建 HeapChannelBuffer 对象         com.alibaba.dubbo.remoting.buffer.ChannelBuffer buffer = com.alibaba.dubbo.remoting.buffer.ChannelBuffers.dynamicBuffer(1024);         // 获得 NettyChannel 对象         NettyChannel channel = NettyChannel.getOrAddChannel(ch, url, handler);         try {             // 编码             codec.encode(channel, buffer, msg);         } finally {             // 移除 NettyChannel 对象，若断开连接             NettyChannel.removeChannelIfDisconnected(ch);         }         // 返回 Netty ChannelBuffer 对象         return ChannelBuffers.wrappedBuffer(buffer.toByteBuffer());     }  }
```

---

- org.jboss.netty.handler.codec.oneone.OneToOneEncoder**抽象类**
，Netty3 编码器
。
- 代码比较简单，胖友自己看注释。

## 8.2 InternalDecoder

```plain text
plain 1: private class InternalDecoder extends SimpleChannelUpstreamHandler {  2:   3:     /**  4:      * 未读完的消息 Buffer  5:      */  6:     private com.alibaba.dubbo.remoting.buffer.ChannelBuffer buffer = com.alibaba.dubbo.remoting.buffer.ChannelBuffers.EMPTY_BUFFER;  7:   8:     @Override  9:     public void messageReceived(ChannelHandlerContext ctx, MessageEvent event) throws Exception { 10:         // 跳过非 ChannelBuffer 11:         Object o = event.getMessage(); 12:         if (!(o instanceof ChannelBuffer)) { 13:             ctx.sendUpstream(event); 14:             return; 15:         } 16:  17:         // 无可读，跳过 18:         ChannelBuffer input = (ChannelBuffer) o; 19:         int readable = input.readableBytes(); 20:         if (readable <= 0) { 21:             return; 22:         } 23:  24:         // 合并 `buffer` + `input` 成 `message` 25:         com.alibaba.dubbo.remoting.buffer.ChannelBuffer message; 26:         if (buffer.readable()) { // 有未读完的，需要拼接 27:             if (buffer instanceof DynamicChannelBuffer) { 28:                 buffer.writeBytes(input.toByteBuffer()); 29:                 message = buffer; 30:             } else { // Netty3 ChannelBuffer ，转成 DynamicChannelBuffer 。 31:                 int size = buffer.readableBytes() + input.readableBytes(); 32:                 message = com.alibaba.dubbo.remoting.buffer.ChannelBuffers.dynamicBuffer(size > bufferSize ? size : bufferSize); 33:                 message.writeBytes(buffer, buffer.readableBytes()); 34:                 message.writeBytes(input.toByteBuffer()); 35:             } 36:         } else { // 无未读完的，直接创建 37:             message = com.alibaba.dubbo.remoting.buffer.ChannelBuffers.wrappedBuffer(input.toByteBuffer()); 38:         } 39:  40:         // 获得 NettyChannel 对象 41:         NettyChannel channel = NettyChannel.getOrAddChannel(ctx.getChannel(), url, handler); 42:         // 循环解析，直到结束 43:         Object msg; 44:         int saveReaderIndex; 45:         try { 46:             // decode object. 47:             do { 48:                 saveReaderIndex = message.readerIndex(); 49:                 try { 50:                     msg = codec.decode(channel, message); 51:                 } catch (IOException e) { 52:                     buffer = com.alibaba.dubbo.remoting.buffer.ChannelBuffers.EMPTY_BUFFER; 53:                     throw e; 54:                 } 55:                 if (msg == Codec2.DecodeResult.NEED_MORE_INPUT) { 56:                     message.readerIndex(saveReaderIndex); 57:                     break; 58:                 // 解码到消息，触发一条消息 59:                 } else { 60:                     //is it possible to go here ? 芋艿：不可能，哈哈哈 61:                     if (saveReaderIndex == message.readerIndex()) { 62:                         buffer = com.alibaba.dubbo.remoting.buffer.ChannelBuffers.EMPTY_BUFFER; 63:                         throw new IOException("Decode without read data."); 64:                     } 65:                     if (msg != null) { 66:                         Channels.fireMessageReceived(ctx, msg, event.getRemoteAddress()); 67:                     } 68:                 } 69:             } while (message.readable()); 70:         } finally { 71:             // 有剩余可读的，压缩并缓存 72:             if (message.readable()) { 73:                 message.discardReadBytes(); 74:                 buffer = message; 75:             // 无剩余的，设置空 Buffer 76:             } else { 77:                 buffer = com.alibaba.dubbo.remoting.buffer.ChannelBuffers.EMPTY_BUFFER; 78:             } 79:             // 移除 NettyChannel 对象，若断开连接 80:             NettyChannel.removeChannelIfDisconnected(ctx.getChannel()); 81:         } 82:     } 83:  84:     @Override 85:     public void exceptionCaught(ChannelHandlerContext ctx, ExceptionEvent e) { 86:         ctx.sendUpstream(e); 87:     } 88: }
```

---

- 继承
org.jboss.netty.channel.SimpleChannelUpstreamHandler
类。
- buffer
属性，未读完的消息 Buffer 。在
#messageReceived(ctx, event)
方法中，我们在做拆包粘包的处理过程中，可能收到数据是不完整的。例如，不足以解析成一条 Dubbo Request 。那么，我们就需要将收到的，缓存到
buffer
中。
- 第 10 至 15 行：跳过非 ChannelBuffer 。
- 第 17 至 22 行：跳过无可读的。
- 第 24 至 38 行：合并 **两类三种**
buffer
+
input
成
message
。有
情况，胖友看下注释。
- 第 41 行：获得 NettyChannel 对象。
- 第 42 至 69 行：循环解析，直到结束。此处，和
dubbo-remoting-netty4
的解码流程，就是一致的了。
- 第 71 至 75 行：有剩余的部分，压缩并缓存到
buffer
中。
- 第 75 至 78 行：完全读完，设置
buffer
为空(
EMPTY_BUFFER
)。
- 第 80 行：移除 NettyChannel 对象，若断开连接。

# 9. 日志工厂

和 netty-remoting-netty4 的**日志工厂**，基本一致。差异点是 [DubboLogger](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-netty/src/main/java/com/alibaba/dubbo/remoting/transport/netty/NettyHelper.java#L43-L103) ，无需实现类似 #log(format, arguments) 等需要格式化的方法。因此，无需复制 FormattingTuple 、MessageFormatter 类。