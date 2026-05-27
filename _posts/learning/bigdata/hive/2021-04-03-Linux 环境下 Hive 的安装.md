---
layout: post
title: Linux 环境下 Hive 的安装
slug: hive-installation-on-linux
type:
- note
date: 2021-04-03
status: draft
tags:
- Hive
- BigData
categories:
- Learning
- BigData
mood: null
weather: null
author: deathwhispers
created: 2025-01-09 11:45
updated: 2025-03-12 18:26
---

## 一、安装Hive

### 1.1 下载并解压

下载所需版本的 Hive，这里我下载版本为 cdh5.15.2。下载地址：http://archive.cloudera.com/cdh5/cdh/5/

```plain text
# 下载后进行解压
 tar -zxvf hive-1.1.0-cdh5.15.2.tar.gz
```

### 1.2 配置环境变量

```plain text
# vim /etc/profile
```

添加环境变量：

```plain text
export HIVE_HOME=/usr/app/hive-1.1.0-cdh5.15.2
export PATH=$HIVE_HOME/bin:$PATH
```

使得配置的环境变量立即生效：

```plain text
# source /etc/profile
```

### 1.3 修改配置

**1. hive-env.sh**

进入安装目录下的 conf/ 目录，拷贝 Hive 的环境配置模板 hive-env.sh.template

```plain text
cp hive-env.sh.template hive-env.sh
```

修改 hive-env.sh，指定 Hadoop 的安装路径：

```plain text
HADOOP_HOME=/usr/app/hadoop-2.6.0-cdh5.15.2
```

**2. hive-site.xml**

新建 hive-site.xml 文件，内容如下，主要是配置存放元数据的 MySQL 的地址、驱动、用户名和密码等信息：

```xml
<?xml version="1.0"?><?xml-stylesheet type="text/xsl"  ?><configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://hadoop001:3306/hadoop_hive?createDatabaseIfNotExist=true</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.jdbc.Driver</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>root</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>root</value>
  </property>
</configuration>
```

### 1.4 拷贝数据库驱动

将 MySQL 驱动包拷贝到 Hive 安装目录的 lib 目录下, MySQL 驱动的下载地址为：https://dev.mysql.com/downloads/connector/j/ , 在本仓库的[resources](https://github.com/heibaiying/BigData-Notes/tree/master/resources) 目录下我也上传了一份，有需要的可以自行下载。

![](/assets/images/learning/bigdata/hive/hive-installation-on-linux/6ee8a6378e66a54273908308772ad78f.png)

### 1.5 初始化元数据库

- 当使用的 hive 是 1.x 版本时，可以不进行初始化操作，Hive 会在第一次启动的时候会自动进行初始化，但不会生成所有的元数据信息表，只会初始化必要的一部分，在之后的使用中用到其余表时会自动创建；
- 当使用的 hive 是 2.x 版本时，必须手动初始化元数据库。初始化命令：

```plain text
# schematool 命令在安装目录的 bin 目录下，由于上面已经配置过环境变量，在任意位置执行即可
  schematool -dbType mysql -initSchema
```

这里我使用的是 CDH 的 hive-1.1.0-cdh5.15.2.tar.gz，对应 Hive 1.1.0 版本，可以跳过这一步。

### 1.6 启动

由于已经将 Hive 的 bin 目录配置到环境变量，直接使用以下命令启动，成功进入交互式命令行后执行 show databases 命令，无异常则代表搭建成功。

```plain text
hive
```

![](/assets/images/learning/bigdata/hive/hive-installation-on-linux/126b6a49774baceb8532be7f880cf3e4.png)

在 Mysql 中也能看到 Hive 创建的库和存放元数据信息的表

![](/assets/images/learning/bigdata/hive/hive-installation-on-linux/b7e9e61d1ae38cde7e871bd969cbf978.png)

## 二、HiveServer2/beeline

Hive 内置了 HiveServer 和 HiveServer2 服务，两者都允许客户端使用多种编程语言进行连接，但是 HiveServer 不能处理多个客户端的并发请求，因此产生了 HiveServer2。HiveServer2（HS2）允许远程客户端可以使用各种编程语言向 Hive 提交请求并检索结果，支持多客户端并发访问和身份验证。HS2 是由多个服务组成的单个进程，其包括基于 Thrift 的 Hive 服务（TCP 或 HTTP）和用于 Web UI 的 Jetty Web 服务。

HiveServer2 拥有自己的 CLI 工具——Beeline。Beeline 是一个基于 SQLLine 的 JDBC 客户端。由于目前 HiveServer2 是 Hive 开发维护的重点，所以官方更加推荐使用 Beeline 而不是 Hive CLI。以下主要讲解 Beeline 的配置方式。

### 2.1 修改Hadoop配置

修改 hadoop 集群的 core-site.xml 配置文件，增加如下配置，指定 hadoop 的 root 用户可以代理本机上所有的用户。

```xml
<property>
  <name>hadoop.proxyuser.root.hosts</name>
  <value>*</value>
</property>
<property>
  <name>hadoop.proxyuser.root.groups</name>
  <value>*</value>
</property>
```

之所以要配置这一步，是因为 hadoop 2.0 以后引入了安全伪装机制，使得 hadoop 不允许上层系统（如 hive）直接将实际用户传递到 hadoop 层，而应该将实际用户传递给一个超级代理，由该代理在 hadoop 上执行操作，以避免任意客户端随意操作 hadoop。如果不配置这一步，在之后的连接中可能会抛出 AuthorizationException 异常。

关于 Hadoop 的用户代理机制，可以参考：[hadoop 的用户代理机制](https://blog.csdn.net/u012948976/article/details/49904675#%E5%AE%98%E6%96%B9%E6%96%87%E6%A1%A3%E8%A7%A3%E8%AF%BB) 或 [Superusers Acting On Behalf Of Other Users](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/Superusers.html)

### 2.2 启动hiveserver2

由于上面已经配置过环境变量，这里直接启动即可：

```plain text
# nohup hiveserver2 &
```

### 2.3 使用beeline

可以使用以下命令进入 beeline 交互式命令行，出现 Connected 则代表连接成功。

```plain text
# beeline -u jdbc:hive2://hadoop001:10000 -n root
```

![](/assets/images/learning/bigdata/hive/hive-installation-on-linux/c29358eb62d1dfea36ad6132b7d0b978.png)
