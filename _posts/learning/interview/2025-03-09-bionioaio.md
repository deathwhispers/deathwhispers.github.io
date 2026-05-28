---
layout: post
title: BIO、NIO、AIO
slug: interview-bio-nio-aio
date: '2025-03-09'
type:
- note
tags:
- Java
- Network
- NIO
categories:
- Learning
- Interview
author: deathwhispers
created: 2024-07-26 11:48
updated: 2024-07-26 11:48
---

# BIO是什么?

## 概念

BIO,又称Block-IO,是一种阻塞+同步的通信模式.

是一个比较传统的通信方式,模式简单,使用方便.但是并发处理能力低,通信耗时,依赖网速

## 原理

- 服务器通过一个Acceptor线程,负责监听客户端请求和为每个客户端创建一个新的线程进行链路处理.典型的一请求一应答模式
- 若客户端数量增多,频繁地创建和销毁线程会给服务器打开很大的压力.后改良为用线程池的方式代替新增线程,被称为伪异步IO

BIO模型中,通过Socket和ServerSocket实现套接字通道的通信. 阻塞,同步,简历连接耗时

# NIO是什么

## 概念

NIO,又称New IO,或Non-Block IO, 是一种非阻塞 + 同步的通信模式.

## 原理

- NIO相对于BIO来说一大进步.客户端和服务器之间通过Channel通信.NIO可以在Channel进行读写操作.这些Channel都会被注册在Selector多路复用器上. Selector通过一个线程不停的轮询这些Channel. 找出已经准备就绪的Channel执行IO操作.
- NIO通过一个线程轮询,实现千万个客户端的请求,这就是非阻塞NIO的特点.
    - 缓冲区Buffer: 它是NIO与BIO的一个重要区别.
        - BIO是将数据直接写入或读取到流Stream对象中.
        - NIO的数据操作都是在Buffer中进行的. Buffer实际上是一个数组. Buffer最常见的类型是ByteBuffer, 另外还有CharBuffer, ShortBuffer, IntBuffer, LongBuffer, FloatBuffer, DoubleBuffer.
    - 通道Channel: 和流Stream不同, 通道是双向的. NIO可以通过Channel进行数据的读,写和同时读写操作
        - 通道分为两大类：一类是网络读写（SelectableChannel），一类是用于文件操作（FileChannel）。我们使用的是前者 SocketChannel 和 ServerSocketChannel ，都是SelectableChannel 的子类。
    - 多路复用器Selector: NIO编程的基础. Selector会不断的轮询注册在其上的Channel, 如果某个通道处于就绪 状态, 会被Selector轮询出来, 然后通过SelectionKey可以取得就绪的Channel集合, 从而进行后续的IO操作.
        - 服务器端只要提供一个线程负责 Selector 的轮询, 就可以接入成千上万个客户端, 这就是 JDK NIO库的巨大进步.

## 小结

NIO 模型中通过 SocketChannel 和 ServerSocketChannel 实现套接字通信. 非阻塞, 同步, 避免了为每个TCP连接创建一个线程.

- 同步和异步的区别: 数据拷贝阶段是否需要完全由操作系统的处理.
- 阻塞和非阻塞操作: 是针对发起IO请求操作后, 是否有立刻返回一个标志信息, 而不让请求线程等待.

# AIO是什么

## 概念

AIO, 全程Asynchronous IO, 也叫NIO2, 是一种非阻塞 + 异步的通信模式. 在NIO的基础上, 引入了新的异步通道的概念, 并提供了异步文件通道和异步套接字通道的实现.

## 原理

AIO并没有采用NIO的多路复用器, 而是使用异步通道的概念. 其 read,write 方法的返回类型, 都是Future对象. 而Future模型是异步的, 其核心思想是: 去主函数等待时间.

AIO 模型中通过 AsynchronousSocketChannel 和 AsynchronousServerSocketChannel 实现套接字通道的通信. 非阻塞,异步

# BIO, NIO有什么区别

- 线程模型不同
    - BIO: 一个线程一个连接, 客户端有连接请求时服务器端就需要启动一个线程进行处理. 所以,线程开销大. 可改良为用线程池的方式代替新创建线程, 被称为伪异步IO.
    - NIO: 一个请求一个线程, 但客户端发送的连接请求都会注册到多路复用器上, 多路复用器轮询到连接有新的IO请求时, 才启动一个线程进行处理. 可改良为一个线程处理多个请求, 基于多 Reactor 模型.
- BIO是面向流(Stream)的, 而NIO是面向缓冲区(Buffer)的
- BIO的各种操作是阻塞的, 而NIO的各种操作是非阻塞的
- BIO的Socket是单向的, 而NIO的Channel是双向的.

![](/assets/images/learning/interview/interview-bio-nio-aio/13128cdd78c5cc4fb6826a0d4a8af69e.png)

有一点要注意, 虽然图中说NIO的性能一般, 但在绝大多数日常业务场景中, NIO和AIO的性能差距实际没这么大. 在Netty5中, 基于AIO改造和支持, 最后发现, 性能并没有想象中那么强悍, 所以Netty5被废弃, 而是继续保持Netty4为主版本, 使用NIO为主.

![](/assets/images/learning/interview/interview-bio-nio-aio/6de34a3a2497d8f02f416e658234ab64.png)
