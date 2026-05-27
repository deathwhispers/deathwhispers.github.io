---
layout: post
title: Cassandra框架
slug: cassandra-framework
type:
- note
date: 2019-03-11
status: draft
tags:
- Database
- Cassandra
categories:
- Learning
- Database
author: deathwhispers
created: 2019-03-22 11:46
updated: 2019-03-22 18:34
---

# Cassandra框架

Cassandra框架

Cassandra是社交网络理想的数据库，适合于实时事务处理和提供交互型数据。以Amazon的完全分布式的Dynamo为基础，结合了Google BigTable基于列族（Column Family）的数据模型，P2P去中心化的存储，目前twitter和digg中都有使用。

在CAP特性上，HBase选择了CP，Cassandra更倾向于AP，而在一致性上有所减弱。

Cassandra的类Dynamo特性有以下几点：

l 对称的，P2P架构

n 无特殊节点，无单点故障

l 基于Gossip的分布式管理

l 通过分布式hash表放置数据

n 可插拔的分区

n 可插拔的拓扑发现

n 可配置的放置策略

l 可配置的，最终一致性

类BigTable特性：

l 列族数据模型

n 可配置，2级maps，Super Colum Family

l SSTable磁盘存储

n Append-only commit log

n Mentable (buffer and sort)

n 不可修改的SSTable文件

l 集成Hadoop
