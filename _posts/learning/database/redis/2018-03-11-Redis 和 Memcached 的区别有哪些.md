---
layout: post
title: Redis 和 Memcached 的区别有哪些？
author: deathwhispers
date: 2018-03-11
slug: redis-and-memcached-difference
categories:
- Database
tags:
- Redis
- Database
type: note
created: 2019-05-11 11:45
updated: 2019-05-11 22:17
---

# Redis 和 Memcached 的区别有哪些？

艿艿：随着 Memcached 日渐没落，这个问题问的越来越少了。

🦅 **1. Redis 支持复杂的数据结构**

- Memcached 仅提供简单的字符串。
- Redis 提供复杂的数据结构，丰富的数据操作。

也因为 Redis 支持复杂的数据结构，Redis 即使晚于 Memcached 推出，却获得更多开发者的青睐。

Redis 相比 Memcached 来说，拥有更多的数据结构，能支持更丰富的数据操作。如果需要缓存能够支持更复杂的结构和操作，Redis 会是不错的选择。

🦅 **2. Redis 原生支持集群模式**

- 在 Redis3.x 版本中，官方便能支持 Cluster 模式。
- Memcached 没有原生的集群模式，需要依靠客户端来实现往集群中分片写入数据。

🦅 **3. 性能对比**

- Redis 只使用单核，而 Memcached 可以使用多核，所以平均每一个核上 Redis在存储小数据时比 Memcached 性能更高。
- 在 100k 以上的数据中，Memcached 性能要高于 Redis 。虽然 Redis 最近也在存储大数据的性能上进行优化，但是比起 Memcached，还是稍有逊色。

更多关于性能的对比，可以看看 [《Memcached 与 Redis 的关键性能指标比较》](https://www.jianshu.com/p/34f90813d7c9) 。

🦅 **4. 内存管理机制不同**

相比来说，Redis 的内存管理机制，会更加简单。

- Redis 采用的是包装的 malloc/free ，使用时现场申请的方式。
- Memcached 采用的是 Slab Allocation 机制管理内存，预分配的内存池的方式。

如果对比两者的内存使用效率：

- 简单的 Key-Value 存储的话，Memcached 的内存利用率更高，可以使用类似内存池。
- 如果 Redis 采用 hash 结构来做 key-value 存储，由于其组合式的压缩， 其内存利用率会高于 Memcached 。

🦅 **5. 网络 IO 模型**

- Memcached 是多线程，非阻塞 IO 复用的网络模型，原型上接近 Nignx 。
- Redis 使用单线程的 IO 复用模型，自己封装了一个简单的 AeEvent 事件处理框架，主要实现了 epoll ， kqueue 和 select ，更接近 Apache 早期的模式。

🦅 **6. 持久化存储**

- Memcached 不支持持久化存储，重启时，数据被清空。
- Redis 支持持久化存储，重启时，可以恢复已持久化的数据。
