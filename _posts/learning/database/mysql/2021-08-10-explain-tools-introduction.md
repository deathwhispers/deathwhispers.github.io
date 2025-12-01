---
layout: post
title: Explain工具介绍
slug: explain-tools-introduction
type:
  - note
date: 2021-08-10
tags:
  - mysql
categories:
  - mysql
author: deathwhispers
created: 2021-08-10 11:45
updated: 2021-08-10 22:17
---
# Explain工具介绍

使用 explain 关键字可以模拟优化器制行sql语句，分析你的查询语句或是结构的性能瓶颈

在 select 语句之前增加explain关键字，Mysql会在查询设置一个标记，执行查询会返回执行计划的信息，而不是执行这条sql

注意：如果from中包含子查询，仍会执行该子查询，将结果放入临时表中

Explain分析示例：

explain select * from actor;

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037422833-ee57b44d-42f6-457c-ad86-cd725bdd2d57.png)

在查询中的每个表会输出一行，如果有两个表通过join连接查询，那么会输出两行

**Explain两个变种**

**1.explain extended**：会在 explain 的基础上额外提供一些查询优化的信息，紧随其后通过 show warnings 命令可以得到优化后的查询语句，从而看出优化器优化了什么，额外还有 filtered 列，是一个半分比的值，rows * filtered/100 可以估算出将要和 explain 中前一个进行连接的行数（前一个表指 explain 中的 id 值比当前表id值小的表）

explain extended select * from film where id = 1；

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037422912-3f2a66dc-1dd2-4ccc-a2e6-fefacb0f6ac5.png)

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037422992-e649e2fe-b360-4da1-9970-c5778864d420.png)

**2.explain partitions**：相比 explain 多了个 partitions 字段，如果查询是基于分区表的话，会显示铲鲟将访问的分区

**explain中的列**

**1.id列**

id列的编号是 select 的序列号，有几个select 就有几个id，并且id的顺序是按 select 出现的顺序增长的。

id列越大执行优先级越高，id相同则从上往下执行，id为 null 最后执行

**2.select_type 列**

select_type表示对应行是简单还是复杂的查询

1.simple：简单查询。查询不包含子查询和 union

explain select * from film where id =2；

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037423081-58261588-e586-4e3e-a764-0dadc616c8a2.png)

2.primary：复杂查询中最外层的 select

3.subquery：包含在 select 中的子查询（不在 from 子句中）

4.derived：包含在 from 子句中的子查询。mysql会将结果存放在一个临时表中，也称为派生表（derived 的英文含义）

用这个例子来了解 primary、subquery 和 derived 类型

5.union：在 union 中的第二个和随后的 select

explain select 1 union all select 1；

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037423162-daecadc0-f955-4565-9edb-2f122836f14d.png)

**3.table列**

这一列表示 explain 的一行正在访问哪个表

当 from 子句中有子查询时，table 列是格式，表示当前查询依赖id = N 的查询，于是先执行 id = N 的查询

当有 union 时，UNION RESULT 的 table 列的值为<union1,2>，1和2表示参与 union 的 select 行id。

**4. type列**

这一列表示关联类型或访问类型，即MySQL决定如何查找表中的行，查找数据行记录的大概范围。

依次从最优到最差分别为：**system > const > eq_ref > ref > range > index > ALL**

一般来说，得保证查询达到range级别，最好达到ref

**NULL**：mysql能够在优化阶段分解查询语句，在执行阶段用不着再访问表或索引。

例如：在索引列中选取最小值，可以单独查找索引来完成，不需要在执行时访问表