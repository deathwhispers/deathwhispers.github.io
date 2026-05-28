---
layout: post
title: Redis 支持的 Java 客户端都有哪些？
author: deathwhispers
date: 2018-03-11
slug: redis-java-clients
categories:
- Database
tags:
- Redis
- Database
type: note
created: 2019-05-11 11:45
updated: 2019-05-11 22:17
---

# Redis 支持的 Java 客户端都有哪些？

使用比较广泛的有三个 Java 客户端：

- Redisson

Redisson ，是一个高级的分布式协调 Redis 客服端，能帮助用户在分布式环境中轻松实现一些 Java 的对象 (Bloom filter, BitSet, Set, SetMultimap, ScoredSortedSet, SortedSet, Map, ConcurrentMap, List, ListMultimap, Queue, BlockingQueue, Deque, BlockingDeque, Semaphore, Lock, ReadWriteLock, AtomicLong, CountDownLatch, Publish / Subscribe, HyperLogLog)。

- Jedis

Jedis 是 Redis 的 Java 实现的客户端，其 API 提供了比较全面的 Redis 命令的支持。

Redisson 实现了分布式和可扩展的 Java 数据结构，和 Jedis 相比，Jedis 功能较为简单。

Redisson 的宗旨是促进使用者对 Redis 的关注分离，从而让使用者能够将精力更集中地放在处理业务逻辑上。

- Lettuce

Lettuce 是一个可伸缩线程安全的 Redis 客户端。多个线程可以共享同一个 RedisConnection 。它利用优秀 Netty NIO 框架来高效地管理多个连接。

Redis 官方推荐使用 Redisson 或 Jedis 。

Spring Boot 2.x 内置支持 Jedis 和 Lettuce 。一般情况下，建议：

- 使用 Spring Data Redis ，提供了透明使用 Jedis 和 Lettuce 的封装。也就是说，大多数时候，我们可以通过配置使用 Jedis 或 Lettuce 进行 Redis 的操作，而上层使用 Spring Data Redis 提供的统一 API 。
- 从目前来说，Jedis 会比 Lettuce 更加流行，并且更加稳定。虽然说 Jedis 有一段时间，不再进行更新，但是突然又开始更新，可能是诈尸了。
- 如果想要更加丰富的特性，例如说分布式锁，布隆过滤器，可以考虑研究下 Redisson 。
