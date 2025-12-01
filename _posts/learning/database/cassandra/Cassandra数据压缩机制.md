---
layout: post
title: Cassandra数据压缩机制
slug: cassandra-data-compression-mechanism
type:
  - note
date: 2019-06-22
status: draft
tags:
  - cassandra
  - compression
categories: 
  - cassandra
author: deathwhispers
created: 2019-06-22 11:46
updated: 2019-06-22 18:34
---


# Cassandra数据压缩机制

压缩数据的步骤：

1. 判断是否符合压缩条件
2. 如果SSTable 的数量足够，就将需要压缩的 SSTable 文件按照大小进行分组
3. 对于已经分组的SSTable文件，如果数量满足压缩的要求，取分组中的前max_compaction_threshold 个SSTable文件执行压缩

Cassandra在对SSTable执行数据压缩的过程如下：

判断是否需要在压缩前对需要压缩的文件做快照，同时判断需要压缩的磁盘空间是否满足，如果不满足，减少压缩文件的个数。

判断本次压缩操作是否属于主压缩（即该Column Family下面的所有SSTable文件都被压缩），构建遍历需要压缩的SSTable文件的迭代器，创建

SSTableWriter，开始遍历需要压缩的SSTable文件，将压缩后的值通过SSTableWriter写入新的SSTable文件中。