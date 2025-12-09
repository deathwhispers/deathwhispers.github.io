---
layout: post
title: db2完全卸载
slug: db2-uninstall
type:
  - note
date: 2018-05-11
tags:
  - db2
categories:
  - db2
author: deathwhispers
created: 2018-05-11 11:45
updated: 2018-05-11 22:17
---
# db2完全卸载

如果你是已经成功安装过db2，在/.profile中进行了配置，那么在再次安装的时候可能会不成功，需要到/.profile配置进行还原。您必须具有 root 权限才能卸载DB2。

1、删除数据库

su - db2inst1 (这里db2inst1为实例用户)

db2 list db directory (查看所有数据库列表)

db2 connect to db_name (连接数据库)

db2 drop db db_name (删除数据库)

注：如果在删除数据库时提示数据库正在使用（The database is currently using），得先停止数据库，然后再删除。

2、删除实例

su - db2inst1 (切换到实例用户)

db2inst1 stop (停止管理服务，db2inst1为实例名)

su - root (切换为root用户)

cd /opt/IBM/db2/V9.5/instance (切换到实例目录)

./dasdrop db2inst1 (删除管理服务)

./db2idrop db2inst1 (删除实例)

注：如果删除实例时提示实例正在运行（There are applications that are still running that are using the specified instance.），则先停止实例，再删除。

su - db2inst1 (切换到实例用户)

./db2stop (停止实例)

su - root

cd /opt/IBM/db2/V9.5/instance

./db2idrop db2inst1

3、卸载DB2

cd /opt/IBM/db2/V9.5/install (切换到安装目录)

./db2_deinstall -a (卸载)

cd /opt/IBM/db2 (如果db2下没有任何文件，则卸载成功)

cd /opt

rm -rf IBM (强制删除IBM文件夹)

4、删除用户

su - root

smit user (然后根据提示删除相关的用户)

cd /home

rm -rf db2inst1 (删除用户的宿主目录)

至此，DB2卸载成功。卸载过程中，需注意用户的权限。