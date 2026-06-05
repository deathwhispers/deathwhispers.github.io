---
layout: post
title: 基于Kafka+Debezium+Flink的SQLServer实时增量同步方案
author: deathwhispers
date: 2024-01-09
slug: sqlserver-real-time-incremental-synchronization-using-kafka-debezium-flink
categories:
- BigData
tags:
- Flink
- BigData
type: note
status: draft
created: 2024-01-09 11:45
updated: 2024-03-12 18:33
---

### 安装Connector

下载链接

```shell
http://client.hub.confluent.io/confluent-hub-client-latest.tar.gz?_ga=2.215682399.93673590.1629776859-1065619546.1629776859
```

解压

```shell
tar confluent-hub-client-latest.tar -C /opt/module/confluent-hub
```

配置环境变量

```properties
export CONN_HOME=/opt/module/confluent-hub
export PATH=$CONN_HOME/bin:$PATH
```

验证安装

```shell
source /etc/profile
confluent-hub
```

### 安装Debezium的SQLServer连接器

```shell
confluent-hub install debezium/debezium-connector-sqlserver:0.9.4 \
 --component-dir /opt/module/kafka2/connect/ \
 --worker-configs /opt/module/kafka2/config/connect-distributed.properties

 一直选y即可
```

- component-dir 连接器存放路径
- worker-configs connect-distributed.properties路径

### 配置Kafka Connent

```shell
vi $KAFKA_HOME/config/connect-distributed.properties

##
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

# This file contains some of the configurations for the Kafka Connect distributed worker. This file is intended
# to be used with the examples, and some settings may differ from those used in a production system, especially
# the `bootstrap.servers` and those specifying replication factors.

# A list of host/port pairs to use for establishing the initial connection to the Kafka cluster.
#  kafka集群
bootstrap.servers=sc1:9092,sc2:9092,sc3:9092

# unique name for the cluster, used in forming the Connect cluster group. Note that this must not conflict with consumer group IDs
group.id=connect-cluster

# The converters specify the format of data in Kafka and how to translate it into Connect data. Every Connect user will
# need to configure these based on the format they want their data in when loaded from or stored into Kafka
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
# Converter-specific settings can be passed in by prefixing the Converter's setting with the converter we want to apply
# it to
key.converter.schemas.enable=true
value.converter.schemas.enable=true

# Topic to use for storing offsets. This topic should have many partitions and be replicated and compacted.
# Kafka Connect will attempt to create the topic automatically when needed, but you can always manually create
# the topic before starting Kafka Connect if a specific topic configuration is needed.
# Most users will want to use the built-in default replication factor of 3 or in some cases even specify a larger value.
# Since this means there must be at least as many brokers as the maximum replication factor used, we'd like to be able
# to run this example on a single-broker cluster and so here we instead set the replication factor to 1.
offset.storage.topic=connect-offsets
offset.storage.replication.factor=1
#offset.storage.partitions=25

# Topic to use for storing connector and task configurations; note that this should be a single partition, highly replicated,
# and compacted topic. Kafka Connect will attempt to create the topic automatically when needed, but you can always manually create
# the topic before starting Kafka Connect if a specific topic configuration is needed.
# Most users will want to use the built-in default replication factor of 3 or in some cases even specify a larger value.
# Since this means there must be at least as many brokers as the maximum replication factor used, we'd like to be able
# to run this example on a single-broker cluster and so here we instead set the replication factor to 1.
config.storage.topic=connect-configs
config.storage.replication.factor=1

# Topic to use for storing statuses. This topic can have multiple partitions and should be replicated and compacted.
# Kafka Connect will attempt to create the topic automatically when needed, but you can always manually create
# the topic before starting Kafka Connect if a specific topic configuration is needed.
# Most users will want to use the built-in default replication factor of 3 or in some cases even specify a larger value.
# Since this means there must be at least as many brokers as the maximum replication factor used, we'd like to be able
# to run this example on a single-broker cluster and so here we instead set the replication factor to 1.
status.storage.topic=connect-status
status.storage.replication.factor=1
#status.storage.partitions=5

# Flush much faster than normal, which is useful for testing/debugging
offset.flush.interval.ms=10000

# These are provided to inform the user about the presence of the REST host and port configs
# Hostname & Port for the REST API to listen on. If this is set, it will bind to the interface used to listen to requests.
#rest.host.name=
# 通信端口
rest.port=18083

# The Hostname & Port that will be given out to other workers to connect to i.e. URLs that are routable from other servers.
rest.advertised.host.name=sc1
rest.advertised.port=9093

# Set to a list of filesystem paths separated by commas (,) to enable class loading isolation for plugins
# (connectors, converters, transformations). The list should consist of top level directories that include
# any combination of:
# a) directories immediately containing jars with plugins and their dependencies
# b) uber-jars with plugins and their dependencies
# c) directories immediately containing the package directory structure of classes of plugins and their dependencies
# Examples:
# plugin.path=/usr/local/share/java,/usr/local/share/kafka/plugins,/opt/connectors,
# 连接器路径
plugin.path=/opt/module/kafka2/connect
```

启动

```plain text
connect-distributed.sh $KAFKA_HOME/config/connect-distributed.properties
```

查看通信端口

```plain text
netstat -tanp |grep 18083
```

查看Worker

```plain text
curl -s sc1:18083
```

获取Worker上已经安装的Connector

```plain text
curl -s sc1:18083/connector-plugins
```

### **提交Connector用户配置**

```plain text
- debezium文档中连接sqlserver的例子
curl -s -X POST -H "Content-Type: application/json" --data '{
    "name": "inventory-connector",
    "config": {
        "connector.class": "io.debezium.connector.sqlserver.SqlServerConnector",
        "database.hostname": "192.168.110.220",
        "database.port": "1433",
        "database.user": "sa",
        "database.password": "passwd",
        "database.dbname": "DebeziumTest",
        "database.server.name": "fullfillment",
        "database.history.kafka.bootstrap.servers": "sc1:9092,sc2:9092,sc3:9092",
        "database.history.kafka.topic": "dbhistory.fullfillment"
    }
}' http://sc1:18083/connectors

```

查看connector当前状态,确保状态是RUNNING

```plain text
curl -s sc1:18083/connectors/inventory-connector/status

{"name":"inventory-connector",
"connector":{"state":"RUNNING","worker_id":"192.168.110.220:8083"},
"tasks":[{"id":0,"state":"RUNNING","worker_id":"192.168.110.220:8083"}],
"type":"source"}

```

其他常用操作

```plain text
- 列出运行的connector
curl -s sc1:18083/connectors
- 查看connector的信息
curl -s sc1:18083/connectors/inventory-connector
- 查看connector下运行的task信息
curl -s sc1:18083/connectors/inventory-connector/tasks
- 暂停 Connector
curl -s -X PUT sc1:18083/connectors/inventory-connector/pause
- 重启 Connector
curl -s -X PUT sc1:18083/connectors/inventory-connector/resume
- 删除 Connector
curl -s -X DELETE sc1:18083/connectors/inventory-connector

```

```plain text
kafka-console-consumer.sh --bootstrap-server sc1:9092,sc2:9092,sc3:9092 --topic dbhistory.cs --from-beginning

```

一张表就是一个topic，直接对接topic就可以获取对应的数据。

```plain text
package com.flinkcdc;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;

import java.util.Properties;

public class SourceTest {
    public static void main(String[] args) throws Exception{
        // 创建执行环境
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        //checkpoint配置
        env.enableCheckpointing(5000);
        env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
        env.getCheckpointConfig().setCheckpointTimeout(60000);
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(500);
        env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);

        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "sc1:9092,sc2:9092,sc3:9092");
        properties.setProperty("group.id", "connect-cluster");
        properties.setProperty("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        properties.setProperty("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        properties.setProperty("auto.offset.reset", "earliest");

        // 从文件读取数据  管道名称  连接方法  配置信息
        DataStream<String> dataStream = env.addSource( new FlinkKafkaConsumer<String>("cs.dbo.tableName", new SimpleStringSchema(), properties));

        // 打印输出
        dataStream.print();

        // 执行
        env.execute();
    }
}

```
