---
layout: post
title: NIO服务器（一）之抽象API
slug: dubbo-nio-server-abstract-api
type:
  - note
date: 2022-05-25
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-05-25 11:49
updated: 2022-05-25 18:33
---


本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

从本小节开始，我们来分享 Dubbo **自己**实现的 NIO 服务器，使用在 [dubbo://](http://dubbo.apache.org/zh-cn/docs/user/references/protocol/dubbo.html) 和 [thrift://](http://dubbo.apache.org/zh-cn/docs/user/references/protocol/thrift.html) 协议上。

在 NIO 框架的选型上，强大的 Java 社区里有 mina、netty、grizzly 等，甚至 netty 提供了 3.x 和 4.x 的版本。那么该咋办呢？

Dubbo 开发团队的选择是：

- API 层：
    - dubbo-remoting-api
- 实现层：
    - dubbo-remoting-netty3
    - dubbo-remoting-netty4
    - dubbo-remoting-mina
    - dubbo-remoting-grizzly
    - dubbo-remoting-p2p

再配合上 Dubbo SPI 的机制，使用者可以自定义使用哪一种具体的实现。美滋滋。

# 2. 一览

还是老样子，笔者习惯性对代码量进行下统计，dubbo-remoting 的**代码量**如下图：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038297480-6e68b023-e2af-45e5-b436-a48b18ddcbe5.png)

代码量

WTF ！！！ dubbo-remoting-api 的代码量竟然近**万行**？

{__/}( • - •)/つ淡定 @胖友

我们来首先看一张图：

FROM [《Dubbo 开发指南 —— 框架设计》](http://dubbo.apache.org/zh-cn/docs/dev/design.html)

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038297561-52001ca4-f9e0-437c-87bd-0ecc83b5d477.png)

整体设计

**红框部分**，Protocol => Exchange => Transport => Serialize 的调用顺序。

- **exchange**
信息交换层：封装请求响应模式，同步转异步，以 Request, Response 为中心，扩展接口为 Exchanger, ExchangeChannel, ExchangeClient, ExchangeServer。
- **transport**
网络传输层：抽象 mina 和 netty 为统一接口，以 Message 为中心，扩展接口为 Channel, Transporter, Client, Server, Codec
- **serialize**
数据序列化层：可复用的一些工具，扩展接口为 Serialization, ObjectInput, ObjectOutput, ThreadPool

在笔者初看 dubbo-remoting-api 的代码时，对 **exchange** 和 **transport** 的理解是比较模糊的。简单来说，**exchange** 在 **transport** 之上，构造了 Request，Response 模型，**一个请求对应一个响应**。这样的方式，才符合我们实际业务开发的需要。当然，即使是 Request，Response 也分成**同步和异步**返回，重要的是，能够**一一映射**。

胖友如果有兴趣，可以看看：

- [《Request–response》](https://en.wikipedia.org/wiki/Request%E2%80%93response)
- [《Client–server model》](https://en.wikipedia.org/wiki/Client%E2%80%93server_model)

看完以上知识，我们在回过头看 dubbo-remoting-api 的项目结构就清晰了：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038297644-dbb78ccf-4530-4380-945f-269485c8b3a8.png)

dubbo-remoting-api

- 最外层：通用接口。
- buffer
包：缓冲区。
- exchange
包：信息交换层
- transporter
包：网络传输层
- telnet[Telnet 命令](http://dubbo.apache.org/zh-cn/docs/dev/impls/telnet-handler.html)
包：

如上的每一层/包，我们都会独立一篇文章，进行分享。当然，dubbo-remoting-api 模块，只负责 API 层抽象和部分实现，最终能够**真正通信**，需要 dubbo-remoting-netty 等等模块来实现。对应的每一个实现模块，我们也是独立一篇文章。

是不是很清晰，美滋滋？

# 3. 最外层：通用接口

胖友先看看 [《Netty4.0学习笔记系列之一：Server与Client的通讯》](https://blog.csdn.net/u013252773/article/details/21046697?self=)**教程文章**。在该文章中，我们可以看到使用 Netty 在四个类：

- 1、HelloServer ：server类，启动Netty server
- 2、HelloServerInHandler：server的handler，接收客户端消息，并向客户端发送消息
- 3、HelloClient：client类，建立于Netty server的连接
- 4、HelloClientIntHandler：client的handler，接收server端的消息，并向服务端发送消息

恰好，和 dubbo-remoting-api 模块，定义的 Server、Client、ChannelHandler **接口**对应。我们以 dubbo-remoting-netty4 模块的，举例子。整理如下：

| **上文** | **dubbo-remoting-api** | **dubbo-remoting-netty4** |
| --- | --- | --- |
| HelloServer | Server 接口 | [NettyServer](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyServer.java) 实现类 |
| HelloServerInHandler：server | ChannelHandler 接口 | [NettyServerHandler](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyServerHandler.java) 实现类 |
| HelloClient | Client 接口 | [NettyClient](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyClient.java) 实现类 |
| HelloServerInHandler | ChannelHandler 接口 | [NettyClientHandler](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyClientHandler.java) 实现类 |

因为**教程文章**，以教程 Demo 为准，实际会有更多需要抽象的，例如：Codec 协议编解码，Dispatcher 消息等分发。胖友再来看看 dubbo:// 的处理流程：

FROM [《Dubbo 用户指南 —— dubbo://》](http://dubbo.apache.org/zh-cn/docs/user/references/protocol/dubbo.html)

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038297718-29ef1e80-58e5-4534-8e0b-0af3636360f1.png)

dubbo://

- Transporter: mina, netty, grizzy
- Serialization: dubbo, hessian2, java, json
- Dispatcher: all, direct, message, execution, connection
- ThreadPool: fixed, cached

如果这个图读不懂，没关系，下面我们来看看每个接口。后面，胖友可以回过头来理解这个图。

**本文涉及的类图如下**：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038297796-33782fa4-ca33-488f-a976-756ac7ab0f85.png)

类图

# 4. Endpoint

com.alibaba.dubbo.remoting.Endpoint ，**端点**接口。方法如下：

- 属性相关

```plain text
plain URL getUrl();  InetSocketAddress getLocalAddress();  ChannelHandler getChannelHandler();
```

---

- 发送消息

```plain text
plain void send(Object message) throws RemotingException; void send(Object message, boolean sent) throws RemotingException;
```

---

- 关系相关

```plain text
plain void close(); void close(int timeout);  void startClose();  boolean isClosed();
```

---

Endpoint ，从中文上解释来说是，“**端点**”。从字面上来看，不太容易理解。在 dubbo-remoting-api 中，一个 Client 或 Server ，都是一个 Endpoint 。 不同系统的，Endpoint 代表的会略有差距，例如 SpringMVC 中，一个请求 Restful URL 也可以是一个 Endpoint ，胖友可以 Google 查询，理解更多。

## 4.1 Channel

com.alibaba.dubbo.remoting.Channel ，继承 Endpoint 接口，**通道**接口。方法如下：

- 连接相关

```plain text
plain InetSocketAddress getRemoteAddress();  boolean isConnected();
```

---

- 属性相关

```plain text
plain boolean hasAttribute(String key); Object getAttribute(String key); void setAttribute(String key, Object value); void removeAttribute(String key);
```

---

和 Netty Channel 一致，**通讯的载体**。在后面的文章，我们会看到在 dubbo-remoting-netty4 项目中，[NettyChannel](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyChannel.java) 是 Dubbo Channel 的实现，内部有**真正的** Netty Channel 属性，用于**通讯**。

## 4.2 Client

com.alibaba.dubbo.remoting.Client ，实现 Endpoint 和 Channel 和 Resetable 接口，**客户端**接口。方法如下：

```plain text
plain // 重连 void reconnect() throws RemotingException;
```

---

## 4.3 Server

com.alibaba.dubbo.remoting.Server ，继承 Endpoint 和 Resetable 接口，**服务器**接口。方法如下：

```plain text
plain // 是否绑定本地端口，提供服务。即，是否启动成功，可连接，接收消息等。 boolean isBound();  // 获得连接上服务器的通道（客户端）们 Collection<Channel> getChannels(); Channel getChannel(InetSocketAddress remoteAddress);
```

---

### 4.3.1 Resetable

com.alibaba.dubbo.common.Resetable ，**可重置**接口。方法如下：

```plain text
plain void reset(URL url);
```

---

Server 实现 Resetable 接口，在实现 #reset(url) 方法，用于根据新传入的 url 属性，重置自己内部的一些属性，例如 [AbstractServer#reset(url)](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/AbstractServer.java#L80-L129) 方法。

# 5. ChannelHandler

com.alibaba.dubbo.remoting.ChannelHandler ，**通道处理器**接口。方法如下：

```plain text
plain void connected(Channel channel) throws RemotingException; void disconnected(Channel channel) throws RemotingException;  void sent(Channel channel, Object message) throws RemotingException; void received(Channel channel, Object message) throws RemotingException;  void caught(Channel channel, Throwable exception) throws RemotingException;
```

---

和 Netty ChannelHandler 一致，**负责 Channel 中的逻辑处理**。在后面的文章，我们会看到在 dubbo-remoting-netty4 项目中，[NettyServerHandler](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyServerHandler.java) 是 Netty ChannelHandler 的实现，内部调用 Netty ChannelHandler 的方法，进行逻辑处理。

# 6. Transporter

com.alibaba.dubbo.remoting.Transporter ，**网络传输**接口。方法如下：

```plain text
plain @SPI("netty") public interface Transporter {      /**      * Bind a server.      *      * 绑定一个服务器      *      * @param url     server url      * @param handler 通道处理器      * @return server 服务器      * @throws RemotingException 当绑定发生异常时      * @see com.alibaba.dubbo.remoting.Transporters#bind(URL, Receiver, ChannelHandler)      */     @Adaptive({Constants.SERVER_KEY, Constants.TRANSPORTER_KEY})     Server bind(URL url, ChannelHandler handler) throws RemotingException;      /**      * Connect to a server.      *      * 连接一个服务器，即创建一个客户端      *      * @param url     server url 服务器地址      * @param handler 通道处理器      * @return client 客户端      * @throws RemotingException 当连接发生异常时      * @see com.alibaba.dubbo.remoting.Transporters#connect(URL, Receiver, ChannelListener)      */     @Adaptive({Constants.CLIENT_KEY, Constants.TRANSPORTER_KEY})     Client connect(URL url, ChannelHandler handler) throws RemotingException;  }
```

---

- @SPI(“netty”)**拓展点**[《Dubbo 用户指南 —— Netty4》](http://dubbo.apache.org/zh-cn/docs/user/demos/netty4.html)
注解，Dubbo SPI
，默认为
“netty”
。注意，此处的
netty
对应的是 netty3 ，因为 Dubbo 项目在开发时，netty4 并未发布。配置方式见
文档。
- @Adaptive({Constants.SERVER_KEY, Constants.TRANSPORTER_KEY})
注解，基于 Dubbo SPI Adaptive 机制，加载对应的 Server 实现，使用
URL.server
或
URL.transporter
属性。
- @Adaptive({Constants.CLIENT_KEY, Constants.TRANSPORTER_KEY})
注解，基于 Dubbo SPI Adaptive 机制，加载对应的 Client 实现，使用
URL.client
或
URL.transporter
属性。

## 6.1 Transporters

[com.alibaba.dubbo.remoting.Transporters](https://github.com/YunaiV/dubbo/blob/7fad710c2dbf66356d5e7b7995e843b8f6225652/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/Transporters.java) ，Transporter 门面类。

友情提示：Facade 设计模式，参见 [《 设计模式（九）外观模式Facade（结构型）》](https://blog.csdn.net/hguisu/article/details/7533759) 文章。

#bind(String url, ChannelHandler… handler)**静态**方法，绑定一个服务器。代码如下：

```plain text
plain 1: public static Server bind(String url, ChannelHandler... handler) throws RemotingException {  2:     return bind(URL.valueOf(url), handler);  3: }  4:   5: public static Server bind(URL url, ChannelHandler... handlers) throws RemotingException {  6:     if (url == null) {  7:         throw new IllegalArgumentException("url == null");  8:     }  9:     if (handlers == null || handlers.length == 0) { 10:         throw new IllegalArgumentException("handlers == null"); 11:     } 12:     // 创建 handler 13:     ChannelHandler handler; 14:     if (handlers.length == 1) { 15:         handler = handlers[0]; 16:     } else { 17:         handler = new ChannelHandlerDispatcher(handlers); 18:     } 19:     // 创建 Server 对象 20:     return getTransporter().bind(url, handler); 21: }
```

---

- 和
Transporter#bind(url, handler)
方法，对应。
- 第 12 至 18 行：创建 [ChannelHandlerDispatcher](https://github.com/YunaiV/dubbo/blob/7fad710c2dbf66356d5e7b7995e843b8f6225652/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/ChannelHandlerDispatcher.java)
handler
。若
handlers
是多个，使用
进行封装。在 ChannelHandlerDispatcher 中，会循环调用
handlers
，对应的方法。
- 第 20 行：调用
#getTransporter()
方法，基于 Dubbo SPI 机制，获得 Transporter$Adaptive 对象。代码如下：

```plain text
plain public static Transporter getTransporter() {     return ExtensionLoader.getExtensionLoader(Transporter.class).getAdaptiveExtension(); }
```

---

- 第 20 行：调用 **Transporter 实现对象**[NettyTransporter](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyTransporter.java)[NettyServer](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-netty4/src/main/java/com/alibaba/dubbo/remoting/transport/netty4/NettyServer.java)
Transporter#bind(url, handler)
方法，在 Transporter$Adaptive 对象中，会根据
url
参数，获得对应的
（例如，
），从而创建对应的 Server 对象（例如，
）。

另外，还有一个 [#connect(url, handler)](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/Transporters.java#L59-L76)**静态**方法，连接一个服务器，即创建一个客户端。 和上面方法类似，胖友自己看咯。

# 7. Codec2

com.alibaba.dubbo.remoting.Codec2 ，**编解码器**接口。代码如下：

```plain text
plain /**  * 编码  *  * @param channel 通道  * @param buffer Buffer  * @param message 消息  * @throws IOException 当编码发生异常时  */ @Adaptive({Constants.CODEC_KEY}) void encode(Channel channel, ChannelBuffer buffer, Object message) throws IOException;  /**  * 解码  *  * @param channel 通道  * @param buffer Buffer  * @return 消息  * @throws IOException 当解码发生异常时  */ @Adaptive({Constants.CODEC_KEY}) Object decode(Channel channel, ChannelBuffer buffer) throws IOException;
```

---

- @SPI(“netty”)**拓展点**
注解，Dubbo SPI
。
- @Adaptive({Constants.CODEC_KEY})
注解，基于 Dubbo SPI Adaptive 机制，加载对应的 Codec2 实现，使用
URL.codec
属性。

另外，解码过程中，需要解决 TCP 拆包、粘包的场景，因此解码结果如下：

```plain text
plain // Codec2.java enum DecodeResult {     /**      * 需要更多输入      */     NEED_MORE_INPUT,     /**      * 忽略一些输入      */     SKIP_SOME_INPUT }
```

---

- 目前
SKIP_SOME_INPUT
，暂未使用。
- 感兴趣的胖友，可以提前看下 [《高性能网络框架Netty的TCP拆包、粘包解决方案》](http://chen-tao.github.io/2015/10/03/nettytcp/)**长度界定符**
文章。在后续的文章中，我们既会看到基于
的方案，也会看到基于
的方案。

## 7.1 Codec

[com.alibaba.dubbo.remoting.Codec](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/Codec.java) ，**老的**编解码器接口，被 Codec2 取代。

通过 [CodecAdapter](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/codec/CodecAdapter.java) ，将 Codec 适配成 Codec2 。

## 7.2 Decodeable

com.alibaba.dubbo.remoting.Decodeable ，**可解码**的接口。方法如下：

```plain text
plain // 解码 void decode() throws Exception;
```

---

# 8. Dispatcher

com.alibaba.dubbo.remoting.Dispatcher ，**调度器**接口。方法如下：

```plain text
plain @SPI(AllDispatcher.NAME) public interface Dispatcher {      @Adaptive({Constants.DISPATCHER_KEY, "dispather", "channel.handler"})     // The last two parameters are reserved for compatibility with the old configuration     ChannelHandler dispatch(ChannelHandler handler, URL url);  }
```

---

- @SPI(AllDispatcher.NAME)**拓展点**
注解，Dubbo SPI
，默认为
“all”
。
- @Adaptive({Constants.DISPATCHER_KEY, “dispather”, “channel.handler”})
注解，基于 Dubbo SPI Adaptive 机制，加载对应的 ChanelHander 实现，使用
URL.dispatcher
属性。
- 为什么传入的 [AllChannelHandler](https://github.com/apache/incubator-dubbo/blob/bb8884e04433677d6abc6f05c6ad9d39e3dcf236/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/transport/dispatcher/all/AllChannelHandler.java)[《Dubbo 用户指南 —— 线程模型》](http://dubbo.apache.org/zh-cn/docs/user/demos/thread-model.html)
handler
参数，创建返回的还是 ChannelHandler 对象呢？感兴趣的胖友，可以提前看下
和
。 文章，后面见。

# 9. RemotingException

com.alibaba.dubbo.remoting.RemotingException ，实现 Exception 类，dubbo-remoting-api 的**基础**异常。代码如下：

```plain text
plain public class RemotingException extends Exception {      /**      * 本地地址      */     private InetSocketAddress localAddress;     /**      * 远程地址      */     private InetSocketAddress remoteAddress;          // ... 省略方法 }
```

---

## 9.1 ExecutionException

com.alibaba.dubbo.remoting.ExecutionException ，实现 RemotingException 类，执行异常。代码如下：

```plain text
plain public class ExecutionException extends RemotingException {      /**      * 请求      */     private final Object request;      // ... 省略方法 }
```

---

## 9.2 TimeoutException

com.alibaba.dubbo.remoting.TimeoutException ，实现 RemotingException 类，超时异常。代码如下：

```plain text
plain public class TimeoutException extends RemotingException {      /**      * 客户端      */     public static final int CLIENT_SIDE = 0;     /**      * 服务端      */     public static final int SERVER_SIDE = 1;      /**      * 阶段      */     private final int phase;          // ... 省略方法 }
```

---

# 666. 彩蛋

dubbo-remoting-api 模块，涉及到大量的封装，如果不太理解的胖友，建议多多调试。

毕业那年，也尝试过想，封装一个通用的 API 层，屏蔽 Netty、Mina 差异的细节，写的比较戳。现在看到 Dubbo 实现的方式，Get 新姿势了。