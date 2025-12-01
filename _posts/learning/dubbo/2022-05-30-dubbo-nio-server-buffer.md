---
layout: post
title: NIO服务器（五）之Buffer层
slug: dubbo-nio-server-buffer
type:
  - note
date: 2022-05-30
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-05-30 11:49
updated: 2022-05-30 18:33
---


本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文接 [《精尽 Dubbo 源码分析 —— NIO 服务器（四）之 Exchange 层》](http://svip.iocoder.cn/Dubbo/remoting-api-exchange//?self=) 一文，分享 dubbo-remoting-api 模块， buffer 包，**Buffer 层**。

Buffer 在 NIO 框架中，扮演非常重要的角色，基本每个库都提供了自己的 Buffer 实现，例如：

- Java NIO 的
java.nio.ByteBuffer
- Mina 的
org.apache.mina.core.buffer.IoBuffer
- Netty4 的
io.netty.buffer.ByteBuf

在 dubbo-remoting-api 的 buffer 包中，一方面定义了 ChannelBuffer 和 ChannelBufferFactory 的接口，同时提供了多种默认的实现。整体类图如下：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038305622-fd6c15fb-8f1b-4c2c-b563-1eb1353bec26.png)

类图

- 其中，红框部分，是 Netty3 和 Netty4 ，实现的自定义的 ChannelBuffer 和 ChannelBufferFactory 类。

# 2. ChannelBuffer

[com.alibaba.dubbo.remoting.buffer.ChannelBuffer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/ChannelBuffer.java) ，实现 Comparable 接口，**通道 Buffer** 接口。

ChannelBuffer 在接口方法的定义上，主要参考了 Netty 的 ByteBuf 进行设计，所以接口和注释基本一致，本文就不一个一个细讲过去，胖友可以看：

- 英文：[《Netty4.1 ByteBuf API》](https://netty.io/4.1/api/io/netty/buffer/ByteBuf.html)
- 中文：[《深入研究Netty框架之ByteBuf功能原理及源码分析》](https://my.oschina.net/7001/blog/742236)

独有的接口方法 #factory() 方法，用于逻辑中，需要创建 ChannelBuffer 的情况。

- 代码如下：

```plain text
plain /**  * Returns the factory which creates a {@link ChannelBuffer} whose type and  * default {@link java.nio.ByteOrder} are same with this buffer.  */ ChannelBufferFactory factory()
```

---

- 调用方如下：
![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038305692-40d238a8-136b-46f6-aa61-a888d0524cb4.png)
调用方

## 2.1 AbstractChannelBuffer

[com.alibaba.dubbo.remoting.buffer.AbstractChannelBuffer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/AbstractChannelBuffer.java) ，实现 ChannelBuffer 接口，通道 Buffer **抽象类**。

**构造方法**

```plain text
plain /**  * 读取位置  */ private int readerIndex; /**  * 写入位置  */ private int writerIndex; /**  * 标记的读取位置  */ private int markedReaderIndex; /**  * 标记的写入位置  */ private int markedWriterIndex;
```

---

FROM [《netty的ByteBuf》](https://blog.csdn.net/zhxdick/article/details/51187362)

writerIndex 和 readerIndex

- 初始状态：
![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038305757-5f748e29-095b-4a9b-8f34-c3f516dc29a5.png)
- 当写入5个字节后：
![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038305818-b4a21bde-41aa-4342-ad71-0584ecf2e28d.png)

这时，writerIndex 为 5，这时如果开始读取，那么这个 writerIndex 可以作为上面ByteBuffer flip 之后的 limit。

- 当读取3个字节后：
![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038305876-c70fa5b5-0890-4036-b999-968e44b7419b.png)

**实现方法**

在 AbstractChannelBuffer 实现的方法，都是**重载**的方法，真正**实质**的方法，需要子类来实现。以 #getBytes(…) 方法，举例子：

```plain text
plain @Override public void getBytes(int index, ChannelBuffer dst, int length) {     if (length > dst.writableBytes()) {         throw new IndexOutOfBoundsException();     }     getBytes(index, dst, dst.writerIndex(), length);     dst.writerIndex(dst.writerIndex() + length); }
```

---

- 方法中调用的 **为啥呢实质实现形式**
#getBytes(index, ds, dstIndex, length)
方法，并未实现。
？
的方法，涉及到字节数组的
。

如下是所有

**未实现**

的方法：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038305976-12b3f413-3526-4311-bfbb-532fca13d739.png)

未实现方法

## 2.2 ByteBufferBackedChannelBuffer

[com.alibaba.dubbo.remoting.buffer.ByteBufferBackedChannelBuffer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/ByteBufferBackedChannelBuffer.java) ，实现 AbstractChannelBuffer 抽象类，基于 **java.nio.ByteBuffer** 的 Buffer 实现类。

**构造方法**

```plain text
plain /**  * buffer  * java.nio.ByteBuffer  */ private final ByteBuffer buffer; /**  * 容量  */ private final int capacity;  public ByteBufferBackedChannelBuffer(ByteBuffer buffer) {     if (buffer == null) {         throw new NullPointerException("buffer");     }     // buffer     this.buffer = buffer.slice();     // 容量     capacity = buffer.remaining();     // 设置 `writerIndex`     writerIndex(capacity); }  public ByteBufferBackedChannelBuffer(ByteBufferBackedChannelBuffer buffer) {     // buffer     this.buffer = buffer.buffer;     // 容量     capacity = buffer.capacity;     // 设置 `writerIndex` `readerIndex`     setIndex(buffer.readerIndex(), buffer.writerIndex()); }
```

---

**工厂**

```plain text
plain @Override public ChannelBufferFactory factory() {     if (buffer.isDirect()) {         return DirectChannelBufferFactory.getInstance();     } else {         return HeapChannelBufferFactory.getInstance();     } }
```

---

- 对应的工厂是 DirectChannelBufferFactory 或 HeapChannelBufferFactory 。

**实现方法**

胖友，自己查看。

## 2.3 HeapChannelBuffer

[com.alibaba.dubbo.remoting.buffer.HeapChannelBuffer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/HeapChannelBuffer.java) ，实现 AbstractChannelBuffer 抽象类，基于**字节数组**的 Buffer 实现类。

**构造方法**

```plain text
plain /**  * The underlying heap byte array that this buffer is wrapping.  * 字节数组  */ protected final byte[] array;  public HeapChannelBuffer(int length) {     this(new byte[length], 0, 0); }  public HeapChannelBuffer(byte[] array) {     this(array, 0, array.length); }  protected HeapChannelBuffer(byte[] array, int readerIndex, int writerIndex) {     if (array == null) {         throw new NullPointerException("array");     }     this.array = array;     setIndex(readerIndex, writerIndex); }
```

---

**工厂**

```plain text
plain @Override public ChannelBufferFactory factory() {     return HeapChannelBufferFactory.getInstance(); }
```

---

- 对应的工厂是 HeapChannelBufferFactory 。

**实现方法**

胖友，自己查看。

## 2.4 DynamicChannelBuffer

[com.alibaba.dubbo.remoting.buffer.DynamicChannelBuffer](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/DynamicChannelBuffer.java) ，实现 AbstractChannelBuffer 抽象类，基于**动态**的 Buffer 实现类。或者说，基于传入的 ChannelBufferFactory 的 Buffer 实现类。

**构造方法**

```plain text
plain /**  * 工厂  */ private final ChannelBufferFactory factory; /**  * Buffer  */ private ChannelBuffer buffer;  public DynamicChannelBuffer(int estimatedLength) {     this(estimatedLength, HeapChannelBufferFactory.getInstance()); // 默认 HeapChannelBufferFactory }  public DynamicChannelBuffer(int estimatedLength, ChannelBufferFactory factory) {     if (estimatedLength < 0) {         throw new IllegalArgumentException("estimatedLength: " + estimatedLength);     }     if (factory == null) {         throw new NullPointerException("factory");     }     // 设置 `factory`     this.factory = factory;     // 创建 `buffer`     buffer = factory.getBuffer(estimatedLength); }
```

---

**工厂**

```plain text
plain @Override public ChannelBufferFactory factory() {     return factory; }
```

---

**实现方法**

每个方法，直接调用 buffer 对应的方法。

# 3. ChannelBuffers

[com.alibaba.dubbo.remoting.buffer.ChannelBuffers](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/ChannelBuffers.java)

，Buffer

**工具类**

，提供创建、比较 ChannelBuffer 等公用方法。如下图所示：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038306043-b0a2f154-d0a8-4eaf-b846-8a5a28e650d5.png)

ChannelBuffers

# 4. ChannelBufferFactory

com.alibaba.dubbo.remoting.buffer.ChannelBufferFactory ，**通道 Buffer 工厂**接口。方法如下：

```plain text
plain ChannelBuffer getBuffer(int capacity); ChannelBuffer getBuffer(byte[] array, int offset, int length); ChannelBuffer getBuffer(ByteBuffer nioBuffer); // java.nio.ByteBuffer
```

---

## 4.1 DirectChannelBufferFactory

[com.alibaba.dubbo.remoting.buffer.DirectChannelBufferFactory](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/DirectChannelBufferFactory.java) ，实现 ChannelBufferFactory 接口，创建 DirectChannelBuffer 的工厂。

实现比较简单，代码已经加注释，胖友自己查看。

## 4.2 HeapChannelBufferFactory

[com.alibaba.dubbo.remoting.buffer.HeapChannelBufferFactory](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/HeapChannelBufferFactory.java) ，实现 ChannelBufferFactory 接口，创建 HeapChannelBufferFactory 的工厂。

实现比较简单，代码已经加注释，胖友自己查看。

# 5. IO

实际 IO 操作，是基于 InputStream 和 OutputStream ，例如我们在前文看到的 Serialization 序列化和反序列化，方法如下：

```plain text
plain // ... 省略其他方法 ObjectOutput serialize(URL url, OutputStream output) throws IOException;  ObjectInput deserialize(URL url, InputStream input) throws IOException;
```

---

所以，我们需要将 ChannelBuffer 进行装饰。

---

另外，我们在回过头来看看 Codec 和 Codec2 接口，方法如下：

```plain text
plain // Codec.java void encode(Channel channel, OutputStream output, Object message) throws IOException; // Codec2.java void encode(Channel channel, ChannelBuffer buffer, Object message) throws IOException;  // Codec.java Object decode(Channel channel, InputStream input) throws IOException; // Codec2.java Object decode(Channel channel, ChannelBuffer buffer) throws IOException
```

---

一个变化点，就是将 OutputStream 和 InputStream ，替换成了 ChannelBuffer ，更好的以 ChannelBuffer 为核心，与其他框架整合。

## 5.1 ChannelBufferInputStream

[com.alibaba.dubbo.remoting.buffer.ChannelBufferInputStream](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/ChannelBufferInputStream.java) ，实现 InputStream 接口，代码如下：

```plain text
plain public class ChannelBufferInputStream extends InputStream {      private final ChannelBuffer buffer;     /**      * 开始位置      */     private final int startIndex;     /**      * 结束位置      */     private final int endIndex;      public ChannelBufferInputStream(ChannelBuffer buffer) {         this(buffer, buffer.readableBytes());     }      public ChannelBufferInputStream(ChannelBuffer buffer, int length) {         if (buffer == null) {             throw new NullPointerException("buffer");         }         if (length < 0) {             throw new IllegalArgumentException("length: " + length);         }         if (length > buffer.readableBytes()) {             throw new IndexOutOfBoundsException();         }          this.buffer = buffer;         startIndex = buffer.readerIndex();         endIndex = startIndex + length;         buffer.markReaderIndex();     }          // ... 省略从 buffer 读取的方法，胖友，自己查看。 }
```

---

## 5.2 ChannelBufferOutputStream

[com.alibaba.dubbo.remoting.buffer.ChannelBufferOutputStream](https://github.com/YunaiV/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/com/alibaba/dubbo/remoting/buffer/ChannelBufferOutputStream.java) ，实现 OutputStream 接口，代码如下：

```plain text
plain public class ChannelBufferOutputStream extends OutputStream {      private final ChannelBuffer buffer;     /**      * 开始位置      */     private final int startIndex;      public ChannelBufferOutputStream(ChannelBuffer buffer) {         if (buffer == null) {             throw new NullPointerException("buffer");         }         this.buffer = buffer;         startIndex = buffer.writerIndex();     }      // ... 省略向 buffer 写入的方法，胖友，自己查看。  }
```

---