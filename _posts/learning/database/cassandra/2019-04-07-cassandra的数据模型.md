---
layout: post
title: Cassandra的数据模型
slug: cassandra-data-model
type:
- note
date: 2019-04-07
status: draft
tags:
- Database
- Cassandra
categories:
- Learning
- Database
author: deathwhispers
created: 2019-04-07 11:46
updated: 2019-04-07 18:34
---

# Cassandra的数据模型

Cassandra 的数据模型是基于列族 （Column Family）的思维或五维模型

它借鉴了 Amazon 的 Dynamo 和 Goggle’s Big Table 的数据结构和功能特点，采用 Memtable 的方式进行存储。

在 Cassandra 写入数据之前，需要先记录日志 （CommitLog），然后数据开始写入到 Column Family 对应的 Memtalbe 中， Memtable 是一种按照 key 排序数据的内存结构，在满足一定条件时，再把 Memtable 的数据批量的刷新到磁盘上，存储为 SSTable.

**1.Cassandra 的数据模型**

![](assets/images/learning/database/cassandra/cassandra-data-model/1698037632741-353e3545-acb9-4ff4-95a5-6279062de694.png)

**2.Cassandra 数据模型的基本概念**

| 名称 | 说明 |
| --- | --- |
| Cluster | Cassandra 的节点实例，它可以包含多个Keyspace |
| Keyspace | 用于存放 ColumnFamily 的容器，相当于关系型数据库中的 Schema 或 database |
| ColumnFamily | 用于存放 Column 的容器，类似于关系型数据库中的 table |
| SuperColumn | 一个特殊的 Column， 他的 Value 值可以包涵多个 Column |
| Column | Cassandra 的最基本单位，由 name, value, timestamp组成 |

**3.Cassandra 中数据存放规则**

| 名称 | 说明 |
| --- | --- |
| data | 存储真正的数据文件，即SSTable文件，可以指定多个目录 |
| commitLog | 存储未写入SSTable 中的数据（在每次写入前先记录日志文件） |
| cache(saved_caches) | 存储系统中的缓存数据（在服务重启的时候，从这个目录中加载缓存数据）,可以在cassandra.yaml文件中自定义ColumnFamily的属性中定义缓存相关的信息，如：缓存数据的大小（keys_cahed和rows_cached）、持久化缓存数据的时间间隔（row_cache_save_period_in_seconds 和key_cache_save_period_in_seconds） |

- *

**

在data目录下，Cassandra会将每一个keyspace中的数据存储在不同的目录下，并且keyspace文件目录的名称于keyspace名称相同

system目录时Cassandra系统默认的一个Keyspace，叫做system，它用来存储Cassandra系统的相关元数据信息以及HINT数据信息

- *

**

- *

**

**4.Cassandra 的特点**

1. 灵活的schema：不需要像关系数据库那样预先设计schema，增加或删除字段非常方便
2. 支持range查询：可以对key进行范围查询
3. 高可用，可扩展：单点故障不影响集群服务，可线性扩展

**5.Cassandra 内部数据的排序**

```plain text
有一点需要明确，我们使用 Cassandra 的时候，数据在写入的时候就已经排好顺序了。在某一个 key 内的所有 Column都是按照它的 name来排序的，我们可以在storage-conf.xml 文件中指定排序类型，目前 Cassandra 提供的排序类型有: Bytes, UTF8Type, LexicalUUIDType, TimeUUIDType, AsciiType，和LongType。Cassandra的排序功能是允许我们自己实现的，只要你继承org.apache.cassandra.db.marshal.IType就可以了。
```

[https://www.ibm.com/developerworks/cn/opensource/os-cn-cassandra/](https://www.ibm.com/developerworks/cn/opensource/os-cn-cassandra/)

[https://blog.csdn.net/qq_32523587/article/details/54356557](https://blog.csdn.net/qq_32523587/article/details/54356557)

# 虽然Cassandra不是CP但Cassandra是安全的

[https://blog.csdn.net/cadem/article/details/79933186](https://blog.csdn.net/cadem/article/details/79933186)

# Tunable Consistency不能让Cassandra成为CP系统

[https://blog.csdn.net/cadem/article/details/79932046](https://blog.csdn.net/cadem/article/details/79932046)

# Cassandra的副本策略

[https://blog.csdn.net/cadem/article/details/79931478](https://blog.csdn.net/cadem/article/details/79931478)

# 线性一致性(Linearizability)是并发控制的基础

[https://blog.csdn.net/cadem/article/details/79932574](https://blog.csdn.net/cadem/article/details/79932574)

# Cassandra 3.x官方文档_数据库内部

[https://blog.csdn.net/qq_32523587/article/details/54356557](https://blog.csdn.net/qq_32523587/article/details/54356557)

# cassandra 3.x官方文档(7)—内部原理之如何读写数据

[https://blog.csdn.net/fs1360472174/article/details/55005335](https://blog.csdn.net/fs1360472174/article/details/55005335)

# Cassandra源代码分析：数据写入流程

[http://www.voidcn.com/article/p-smevpecn-ws.html](http://www.voidcn.com/article/p-smevpecn-ws.html)

# Cassandra源代码分析（一）Table和ColumnFamilyStore

[http://www.voidcn.com/article/p-fenjudtz-hv.html](http://www.voidcn.com/article/p-fenjudtz-hv.html)

# Cassandra源代码分析（二）动态变更Keyspace和ColumnFamily定义

[http://www.voidcn.com/article/p-pvepdddf-se.html](http://www.voidcn.com/article/p-pvepdddf-se.html)

# 分布式 Key-Value 存储系统：Cassandra 入门

[https://www.ibm.com/developerworks/cn/opensource/os-cn-cassandra/](https://www.ibm.com/developerworks/cn/opensource/os-cn-cassandra/)

# Cassandra 分布式数据库详解，第 2 部分：数据结构与数据读写

[https://www.ibm.com/developerworks/cn/opensource/os-cn-cassandraxu2/](https://www.ibm.com/developerworks/cn/opensource/os-cn-cassandraxu2/)

# Using a composite partition key

A composite partition key is a partition key consisting of multiple columns. You use an extra set of parentheses to enclose columns that make up the composite partition key. The columns within the primary key definition but outside the nested parentheses are clustering columns. These columns form logical sets inside a partition to facilitate retrieval.

**CREATETABLE**Cats (

block_iduuid,

breedtext,

colortext,

short_hairboolean,

**PRIMARYKEY**((block_id, breed), color, short_hair)

);

For example, the composite partition key consists of block_id and breed. The clustering columns, color and short_hair, determine the clustering order of the data. Generally, Apache Cassandra™ will store columns having the same block_id but a different breed on different nodes, and columns having the same block_id and breed on the same node.
