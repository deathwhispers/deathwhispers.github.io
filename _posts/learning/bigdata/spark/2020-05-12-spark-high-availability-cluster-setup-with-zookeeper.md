---
layout: post
title: 基于ZooKeeper搭建Spark高可用集群
slug: spark-high-availability-cluster-setup-with-zookeeper
type:
  - note
date: 2020-05-12
status: draft
tags:
  - Spark
categories:
  - BigData
mood:
weather:
author: deathwhispers
created: 2025-01-09 11:45
updated: 2025-03-12 18:26
---

## 一、集群规划

这里搭建一个 3 节点的 Spark 集群，其中三台主机上均部署 Worker 服务。同时为了保证高可用，除了在 hadoop001 上部署主 Master 服务外，还在 hadoop002 和 hadoop003 上分别部署备用的 Master 服务，Master 服务由 Zookeeper 集群进行协调管理，如果主 Master 不可用，则备用 Master 会成为新的主 Master。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698029095065-7f7aede9-7f90-40bc-a3cd-ad16b1dc38d7.png)

## 二、前置条件

搭建 Spark 集群前，需要保证 JDK 环境、Zookeeper 集群和 Hadoop 集群已经搭建，相关步骤可以参阅：

- [Linux 环境下 JDK 安装](https://github.com/heibaiying/BigData-Notes/blob/master/notes/installation/Linux%E4%B8%8BJDK%E5%AE%89%E8%A3%85.md)
- [Zookeeper 单机环境和集群环境搭建](https://github.com/heibaiying/BigData-Notes/blob/master/notes/installation/Zookeeper%E5%8D%95%E6%9C%BA%E7%8E%AF%E5%A2%83%E5%92%8C%E9%9B%86%E7%BE%A4%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA.md)
- [Hadoop 集群环境搭建](https://github.com/heibaiying/BigData-Notes/blob/master/notes/installation/Hadoop%E9%9B%86%E7%BE%A4%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA.md)

## 三、Spark集群搭建

### 3.1 下载解压

下载所需版本的 Spark，官网下载地址：http://spark.apache.org/downloads.html

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698029095159-5761bbff-9643-4337-8477-3eabae1e9843.png)

下载后进行解压：

```plain text
# tar -zxvf  spark-2.2.3-bin-hadoop2.6.tgz
```

### 3.2 配置环境变量

```plain text
# vim /etc/profile
```

添加环境变量：

```plain text
export SPARK_HOME=/usr/app/spark-2.2.3-bin-hadoop2.6
export  PATH=${SPARK_HOME}/bin:$PATH
```

使得配置的环境变量立即生效：

```plain text
source /etc/profile
```

### 3.3 集群配置

进入 ${SPARK_HOME}/conf 目录，拷贝配置样本进行修改：

### 1. spark-env.sh

```plain text
cp spark-env.sh.template spark-env.sh
```

```plain text
# 配置JDK安装位置
JAVA_HOME=/usr/java/jdk1.8.0_201
# 配置hadoop配置文件的位置
HADOOP_CONF_DIR=/usr/app/hadoop-2.6.0-cdh5.15.2/etc/hadoop
# 配置zookeeper地址
SPARK_DAEMON_JAVA_OPTS="-Dspark.deploy.recoveryMode=ZOOKEEPER -Dspark.deploy.zookeeper.url=hadoop001:2181,hadoop002:2181,hadoop003:2181 -Dspark.deploy.zookeeper.dir=/spark"
```

### 2. slaves

```plain text
cp slaves.template slaves
```

配置所有 Woker 节点的位置：

```plain text
hadoop001
hadoop002
hadoop003
```

### 3.4 安装包分发

将 Spark 的安装包分发到其他服务器，分发后建议在这两台服务器上也配置一下 Spark 的环境变量。

```plain text
scp -r /usr/app/spark-2.4.0-bin-hadoop2.6/   hadoop002:usr/app/
scp -r /usr/app/spark-2.4.0-bin-hadoop2.6/   hadoop003:usr/app/
```

## 四、启动集群

### 4.1 启动ZooKeeper集群

分别到三台服务器上启动 ZooKeeper 服务：

```plain text
zkServer.sh start
```

### 4.2 启动Hadoop集群

```plain text
# 启动dfs服务
start-dfs.sh
# 启动yarn服务
start-yarn.sh
```

### 4.3 启动Spark集群

进入 hadoop001 的 ${SPARK_HOME}/sbin 目录下，执行下面命令启动集群。执行命令后，会在 hadoop001 上启动 Maser 服务，会在 slaves 配置文件中配置的所有节点上启动 Worker 服务。

```plain text
start-all.sh
```

分别在 hadoop002 和 hadoop003 上执行下面的命令，启动备用的 Master 服务：

```plain text
# ${SPARK_HOME}/sbin 下执行
start-master.sh
```

### 4.4 查看服务

查看 Spark 的 Web-UI 页面，端口为 8080。此时可以看到 hadoop001 上的 Master 节点处于 ALIVE 状态，并有 3 个可用的 Worker 节点。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698029095239-53d73a5f-f565-44e2-a237-71137dcd3a4f.png)

而 hadoop002 和 hadoop003 上的 Master 节点均处于 STANDBY 状态，没有可用的 Worker 节点。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698029095316-a8e5b5cb-f0af-49f6-b2fb-daf2328dea50.png)

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698029095405-cfa0ef66-ed57-483f-918c-fb3a2a95fd60.png)

## 五、验证集群高可用

此时可以使用 kill 命令杀死 hadoop001 上的 Master 进程，此时备用 Master 会中会有一个再次成为 主 Master，我这里是 hadoop002，可以看到 hadoop2 上的 Master 经过 RECOVERING 后成为了新的主 Master，并且获得了全部可以用的 Workers。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698029095486-874e4bfc-cbc0-4a2a-a665-a9f739713fd8.png)

Hadoop002 上的 Master 成为主 Master，并获得了全部可以用的 Workers。

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698029095563-c825db72-6e26-4258-8eba-0cfbad419237.png)

此时如果你再在 hadoop001 上使用 start-master.sh 启动 Master 服务，那么其会作为备用 Master 存在。

## 六、提交作业

和单机环境下的提交到 Yarn 上的命令完全一致，这里以 Spark 内置的计算 Pi 的样例程序为例，提交命令如下：

```plain text
spark-submit \
--class org.apache.spark.examples.SparkPi \
--master yarn \
--deploy-mode client \
--executor-memory 1G \
--num-executors 10 \
/usr/app/spark-2.4.0-bin-hadoop2.6/examples/jars/spark-examples_2.11-2.4.0.jar \
100
```