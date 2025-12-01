---
layout: post
title: db2备份与恢复
slug: db2-backup-restore
type:
  - note
date: 2018-05-06
tags:
  - db2
categories:
  - db2
author: deathwhispers
created: 2018-05-06 11:45
updated: 2018-05-06 22:17
---


# db2备份与恢复

**db2备份与恢复**

1.1离线备份

db2离线备份必须先stop

#断开所有连接，关闭数据库

db2 db2stop force

#启动数据库

db2 db2start 

#显示所有数据库及其路径列表

db2 list database directory

#显示所有活动的数据库

db2 list active databases

#释放一个数据库

db2 deactivate database db_test

#数据库的备份和恢复，注意：不能跨平台恢复

#离线备份

db2 backup database dbname to “/data/DB2/db2idb/dbback”

1.2 离线备份恢复

#断开所有连接，关闭数据库

db2stop fouce

#启动数据库

db2 start

#恢复到相同数据库

–db2 restore database db_dev from “/data/DB2/db2idb/dbback”

#恢复到不同数据库

db2 restore database dbname from “/data/DB2/db2idb/dbback” into db_dev

#

db2 restore database dbname from backdir(/home/db2inst1/backup..) without rolling forward whitout prompting

离线备份可以不用rollforward

2.1在线备份

#启用日志归档模式

db2 update db cfg **for** db_db using LOGRETAIN ON

#设置日志归档目录

db2 update db cfg **for** db_db using LOGARCHMETH1 DISK:/data/db2data/logs/db_db

#做一次离线备份，否则数据库会登录不了[如果提示有连接无法备份，请参考db2离线备份]

db2 backup db db_db to “/data/db2data/backup/db_db”

#在线备份–备份日志（首个活动日志到当前日志会一同备份到备份文件里）

db2 backup db db_db online to “/data/db2data/backup/db_db” include logs

#从包含日志的备份集恢复[恢复同一个数据库 into db_db 可省略]

db2 RESTORE db db_db FROM /data/db2data/backup/db_test/ taken at 20130618142149 into db_test LOGTARGET /data/db2data/logs/db_test

#前滚

#或者直接从归档日志目录进行前滚，同”从不包含日志的备份集恢复”中的”前滚”

db2 “rollforward db db_test to end of logs and stop overflow log path(/data/db2data/logs/db_test)”

#在线备份，恢复数据库时必须前滚。