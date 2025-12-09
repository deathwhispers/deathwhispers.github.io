---
layout: post
title: SQL Server CDC 数据迁移和数据抽取功能介绍
slug: sql-server-cdc-data-migration-and-extraction-features-introduction
type:
  - note
date: 2023-11-01
tags:
  - Sql Server
categories:
  - Database
author: deathwhispers
created: 2023-11-01 22:08
updated: 2023-11-01 22:08
---


简介：CDC介绍 cdc.png 为了满足数据迁移和数据抽取的业务需要，使得有机会在数据库层面上直接实现增量抽取功能，ORACLE综合性能和场景需要，在数据库引擎层面直接集成了CDC功能，由于提供了类似API的功能接口，变更数据捕获和更改跟踪均不要求在源中进行任何架构更改或使用触发器，所以比第三方工具具有一定的优势。

# CDC介绍

![953aa7f22bd8ee7f9db7b6501c7bbf7e](/assets/images/learning/database/sql-server-cdc-data-migration-and-extraction-features-introduction/953aa7f22bd8ee7f9db7b6501c7bbf7e.png)

为了满足数据迁移和数据抽取的业务需要，使得有机会在数据库层面上直接实现增量抽取功能，ORACLE综合性能和场景需要，在数据库引擎层面直接集成了CDC功能，由于提供了类似API的功能接口，变更数据捕获和更改跟踪均不要求在源中进行任何架构更改或使用触发器，所以比第三方工具具有一定的优势。利用CDC捕获变更有以下特点：

1. 性能影响小。使用异步进程捕获，通过进程读取事务日志，对系统造成的影响很小，不对业务系统造成太大的压力，影响现有业务。
2. 监控范围大。对该表的所有DML和DDL操作都会被记录，有助于跟踪表的变化，实现表操作的追根溯源。
3. 操作简单 。CDC是在数据库引擎中添加的功能，封装在数据库中，类似于API接口调用，不需要复杂的业务处理逻辑就可以实现DML和DDL的操作监控。
4. 有一定时延性。由于捕获进程从事务日志中提取更改数据，因此，向源表提交更改的时间与更改出现在其关联更改表中的时间之间存在内在的延迟。 虽然这种延迟通常很小，但务必记住，在捕获进程处理相关日志项之前无法使用更改数据。

# CDC注意事项

```plain text
1. SQL Server的版本必须是2008或以上；
2. 不能同时使用内存优化表（SQL Server2014或以上版本才有的功能）。否则会出现以下错误：
```

![6f244bebf6be3082d786071db0455d44](/assets/images/learning/database/sql-server-cdc-data-migration-and-extraction-features-introduction/6f244bebf6be3082d786071db0455d44.png)

5. @SERVERNAME、serverproperty(‘servername’)两者（本地服务器名和服务器实例的属性必须一致）必须一致。下面脚本可将两者调整成一致。如果执行后两者仍不一致，需要重启SQL Server服务。

if serverproperty(‘servername’) <> @@servername

begin

declare @server sysname

set @server = @@servername

exec sp_dropserver@server =@server

set @server = cast(serverproperty(‘servername’) as sysname)

exec sp_addserver@server = @server , @local = ‘LOCAL’

PRINT ‘ok’

end

select @@SERVERNAME,serverproperty(‘servername’)

```plain text
1. 必须开启SQL Sever代理服务。CDC功能必须通过作业来实现。
2. 开启CDC功能的表，无法使用 TRUNCATE TABLE 。可以先禁用，执行完truncate再启用cdc。
3. 如果表结构发生变化，则捕获实例表中：新增列无法捕获到、删除列保持NULL、修改列类型会发生强制转换。为保险起见，应禁用捕获实例，然后再启用。
```

6. 在查询CDC相关表时，建议加上With(NOLOCK)，否则易产生阻塞或死锁。
    1. 一个表最多只能有两个捕获实例。