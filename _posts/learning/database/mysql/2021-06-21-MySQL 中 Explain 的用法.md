---
layout: post
title: MySQL 中 Explain 的用法
slug: mysql-explain-usage
type:
  - note
date: 2021-06-21
tags:
  - mysql
categories:
  - mysql
author: deathwhispers
created: 2021-06-21 11:45
updated: 2021-06-21 22:17
---


## Explain中的列

### id

id列的编号是select的序列号，有几个select就有几个id，并且id的顺序是按照select出现的顺序增长的。id列越大执行优先级越高，id相同则从上往下执行，id为NULL最后执行。

### select_type

表示对应行是简单还是复杂查询。

1. simple：简单查询，查询不包含子查询和union
2. primary：复杂查询中最外层的select
3. subquery：包含在select中的子查询（不再from子句中的）
4. derived：包含在from子句中的子查询。Mysql会将结果存放在一个临时表中，也称为派生表

### table

这一列表示explain的一行正在访问哪个表当from子句中有子查询时，table列是格式，表示当前查询依赖id=N的查询，于是先执行id=N的查询。当有union时，UNION RESULT的table列的值为<union1,2>，1和2表示参与union的select行id

### type

表示关联类型或访问类型，即Mysql决定如何查找表中的行，查找数据行记录的大概范围。

依次从最优到最差分别为：**system > const > eq_ref > ref > range >index >ALL**一般来讲，得保证查询达到range级别，最好达到ref

NULL：mysql能够在优化阶段分解查询语句，在执行阶段用不着再访问表或索引。

const，system：Mysql能对查询的某部分进行优化并将其转化为一个常量

rq_ref：

### prossible_keys

显示查询可能使用哪些索引来查找

### key

显示Mysql实际采用哪个索引来优化对该表的访问如果没有使用索引，则该列时null，如果想强制Mysql使用或忽视prossible_keys中的索引，再查询中可以使用force index、ignore index

### key_len

显示Mysql在索引里使用的字节数，

### ref

显示了在key列记录的索引中，表查找值所用到的列或常量，常见的有：const，字段名

### rows

Mysql要读取并检测的行数，注意：这不是结果集里的行数

### Extra

显示的是额外信息

5. Using index：使用覆盖索引
6. Using where：使用where语句来处理结果，查询的列未被索引覆盖
7. Using index condition：查询的列不完全被索引覆盖，where条件中是一个前导列的范围
8. Using temporary：Mysql需要创建一张临时表来处理查询。出现这种情况一般是需要进行优化的，首先是想到用索引来优化
9. Using filesort：将用外部排序而不是索引排序
10. Select tables optimized away：使用某些聚合函数来访问存在索引的某个字段时
