---
layout: post
title: Cassandra日常运维
slug: cassandra-daily-ops
type:
  - note
date: 2019-03-22
status: draft
tags:
  - cassandra
  - compression
categories: 
  - cassandra
author: deathwhispers
created: 2019-03-22 11:46
updated: 2019-03-22 18:34
---


# Cassandra 日常运维

Cassandra 日常运维: OpsCenter

- Cassandra 日常运维
    - 线上应急
    - 机器预估
    - 准备工作
    - 文件操作
    - 进程
- Cassandra 使用
    - CQL 查询端
- 集群维护

删除/下线节点

```plain text
- 集群拷贝数据
- 节点上线, 扩容
    * 初始化一个新的集群
    * 添加新节点
    * 替换节点
        + 旧节点宕机
        + 旧节点正在运行
- Streaming
```

- 疑难问题
    - GC
- 升级
    - 2.0升级到2,1
    - 2.1升级到2.2
    - 2.2升级到3.10
    - 授权访问
- 监控
    - 安装 opsCenter
    - 创建集群和安装 agent
    - 修改 agent 配置
    - 堡垒机无法查看 opsCenter
    - 手动安装 agent
    - rolling restart
- nodetool 常用工具 (cfstats, cfhistograms, compactionstats, tpstats)
- 日志分析
    - GC 长时间
    - ParNew 统计
    - tombstone 与 GC 的比较
    - cfstats 和 cfhistograms 统计
    - large partition
        - 2.2
        - 3.10
- 性能调优
    - 服务端配置指南
        - 读写配置
        - JVM配置
        - 从CMS更改为 G1 GC
            - G1 GC LOG
        - Mentable
        - KeyCache
        - RowCache
        - compaction
    - commit log
    - JavaDriver 配置
        - Partitioner
    - Internal
        - Partitioner
        - Memory
    - Ref

## **Cassandra日常运维**

### **线上应急**

**[日志]超过10s的GC:**

```plain text
读取压缩文件：zgrep 'Unlogged batch covering [0-9][0-9][0-9] partitions' cassandra/logs/system.log*


查看当前文件：
cat cassandra/logs/system.log | grep `date +%Y-%m-%d` | grep 'GC in [0-9][0-9][0-9][0-9][0-9]'


cat cassandra/logs/system.log | grep `date +%Y-%m-%d` | grep 'Unlogged batch covering [0-9][0-9][0-9] partitions'


cat cassandra/logs/system.log | grep `date +%Y-%m-%d` | grep 'live and [0-9][0-9][0-9][0-9] tombstone cells'




#按照小时统计长时间GC的次数
grep 'GC' /usr/install/cassandra/logs/system.log | awk '{print $4":"substr($5,0,2)}' | sort | uniq -c | awk '{print $2" "$1}'


zgrep 'GC in [0-9][0-9][0-9][0-9][0-9]ms' /usr/install/cassandra/logs/system.log.1.zip | awk '{print $4":"substr($5,0,2)}' | sort | uniq -c | awk '{print $2" "$1}'


zgrep 'GC in [0-9][0-9][0-9][0-9][0-9]ms' /usr/install/cassandra/logs/system.log.1.zip | awk '{print $4}' | sort | uniq -c | awk '{print $2" "$1}'
```

不需要pssh也可以执行多台机器的命令（仅限于nodetool可以指定-h的命令），下面是一些常用的nodetool命令

```plain text
setcompactionthroughput 256
compactionstats | grep "pending tasks"
cfhistograms forseti velocity_global
cfstats forseti.velocity_app | grep "SSTable count"
proxyhistograms
snapshot forseti_fp
clearsnapshot forseti_fp
ssh $ip 'ps -ef|grep cassandra'
flush
cleanup
disablebackup
proxyhistograms | grep 99%
info | grep "Key Cache"
info |grep Key
compactionstats -H | grep "Tombstone"
tablehistograms forseti velocity_global
tablehistograms forseti velocity_global | grep "95%"
tablestats forseti.velocity_global -H|grep "level:"
compactionstats -H|grep sstables
cfstats forseti.ip_account | grep memory
```

通过nodetool批量执行脚本

```plain text
#sh nodecluster.sh "getcompactionthroughput | awk '{print $4}'"
#sh nodecluster.sh "tablestats forseti.velocity_global -H|grep level:"
home=`echo $CASSANDRA_HOME` #Cassandra安装路径
() {
  ip=`ifconfig | grep "192.168" | awk '/inet/{sub("addr:",""); print $2}'`
  if [ "$ip" == "" ] ;then
    ip=`ifconfig | grep "10.21" | awk '/inet/{sub("addr:",""); print $2}'`
  fi
  echo "$ip"
}
host=$(getIP)
command=$1




nodetoolCMD=`echo $command|cut -d"|" -f1`
otherCMD=`echo $command|cut -d"|" -s -f2-`




if [ "$otherCMD" == "" ]; then
  $home/bin/nodetool -h $host status|grep UN|awk '{print $2}'| while read ip; do echo $ip; $home/bin/nodetool -h $ip $command; done
else
  $home/bin/nodetool -h $host status|grep UN|awk '{print $2}'| while read ip; do echo $ip; $home/bin/nodetool -h $ip $nodetoolCMD | eval "$otherCMD"; done
fi
```

**[JVM]查看GC:**

```plain text
jstat -gc -h 10 `jps | grep CassandraDaemon |awk '{print $1}'` 1000 |
awk '{printf("%10st%10st%10st%10st%10st%10st%10st%10st%10st%10stn",$1,$5,$3,$4,$6,$8,$11,$12,$13,$14)}'




jstat -gcutil `jps | grep CassandraDaemon |awk '{print $1}'` 1000
jstat -gc -h 10 `jps | grep CassandraDaemon |awk '{print $1}'` 500




jstat -gc -h 10 `jps | grep CassandraDaemon |awk '{print $1}'` 500 |
awk '{printf("%10st%10st%10st%10st%10st%10st%10st%10st%10st%10st%10stn",$1,$3,$4,$5,$6,$7,$8,$11,$12,$13,$14)}'




jmap -dump:format=b,file=/home/qihuang.zheng/0428.dat `jps | grep CassandraDaemon |awk '{print $1}'`




S0C S0U S1U EC EU OC OU YGC YGCT FGC FGCT
419392.0 419392.0 419392.0 3355520.0 3355520.0 12582912.0 11641724.1 995186 39005.793 1951 810.868
```

**[进程]重启Cassandra进程:**

```plain text
ps -ef|grep cassandra | grep -v grep | awk '{print $2}'




/usr/install/cassandra/bin/nodetool flush &&
kill -9 `jps | grep CassandraDaemon |awk '{print $1}'`
ps -ef|grep cassandra
/usr/install/cassandra/bin/cassandra
/usr/install/cassandra/bin/nodetool setstreamthroughput -- 4
```

**[日志]查询tombstone:**

```plain text
./pssh.sh ip_forseti.txt "cat /var/log/cassandra/system.log | grep '2015-11-05' | grep 'tombstone'"


./pssh.sh ip_forseti.txt "cat /var/log/cassandra/system.log | grep '2015-11-05' | grep 'messages dropped in last 5000ms'"
```

**[网络]查看网卡流量和限制Streams流量:**

```plain text
./pssh.sh ip_all.txt '/usr/install/cassandra/bin/nodetool getstreamthroughput'




iftop
./pssh.sh ip_all.txt '/usr/install/cassandra/bin/nodetool setstreamthroughput -- 200'
```

**[进程]查看最耗费CPU的线程:**

```plain text
cid=166766
top -Hp $cid | head -8 | tail -1 | awk '{print $1}'






top -Hp `jps | grep CassandraDaemon |awk '{print $1}'` | head -8 | tail -1 | awk '{print $1}'
id1=`printf '%xn' 23518`
jstack `jps | grep CassandraDaemon |awk '{print $1}'` | grep $id1
```

**[统计]查看表的读写延迟:**

```plain text
./pssh.sh ip_forseti.txt '/usr/install/cassandra/bin/nodetool cfstats forseti.velocity | head -3'




./pssh.sh ip_fp.txt '/usr/install/cassandra/bin/nodetool cfstats forseti_fp.android_device_session_temp | head -3'
./pssh.sh ip_fp.txt '/usr/install/cassandra/bin/nodetool cfstats forseti_fp.ios_device_session | head -3'
```

**[统计]KeyCache命中率:**

```plain text
./pssh.sh ip_all.txt '/usr/install/cassandra/bin/nodetool info | tail -2 | head -1'
```

**[应用]CQL查询示例**

```plain text
select * from velocity where attribute='111111' and partner_code='koudai' and app_name='weidian_cross' and type='accountLogin'
order by partner_code desc, app_name desc, type desc, timestamp desc limit 1000;




/usr/install/cassandra/bin/cqlsh -e "desc table forseti_fp.android_device_session_temp;" 192.168.47.227
```

**清空表数据:**

```plain text
/usr/install/cassandra/bin/cqlsh -e "truncate forseti_fp.android_device_session_temp;" 192.168.47.227
nodetool -h 192.168.47.227 status |grep RAC|awk '{print $2}' | while read ip; do echo $ip; nodetool -h $ip clearsnapshot forseti_fp; done




nodetool -h 192.168.47.202 status |grep RAC|awk '{print $2}' | while read ip; do echo $ip; nodetool -h $ip clearsnapshot md5; done




/usr/install/cassandra/bin/cqlsh -e "truncate forseti.velocity;" 192.168.47.202
nodetool -h 192.168.47.202 status |grep RAC|awk '{print $2}' | while read ip; do echo $ip; nodetool -h $ip clearsnapshot forseti; done
```

### **机器预估**

1.每天的调用量有5000万, 预估需要多少容量

```plain text
Cassandra配置: SSD, 8CPU, 32G内存, 3.5T
一个节点, 2.5亿keys, ttl=3M, 占用500G.
ttl=1Y, 需要2T. 182亿条keys, 需要145.6T
一条activity会有大概十几条velocity. 182亿的activity,对应velocity需要1456T.




10Nodes, 3M 25亿velocity 2.5亿activity 500G*10=5T
         6M                            5T*2=10T
         182亿activity, 10*(182/2.5)=3600T=728T
```

2.velocity新的三张表保存半年数据的容量

```plain text
4Nodes - 1Week - 1T
4Nodes - 1Month - 4T
4Nodes - 6Month - 24T
8Nodes - 6Month - 12T
```

### **准备工作**

1.统一使用admin用户安装启动软件, 方便管理和其他用户的使用:

```plain text
chown admin:admin -R /usr/install/apache-cassandra-2.0.15
```

2.建立软链接,方便升级. 如果有升级, 只要替换软链接, 启动命令不需要改变:

```plain text
ln -s /usr/install/apache-cassandra-2.0.15 /usr/install/cassandra
```

3.关闭swap

```plain text
swapoff -a
vi /etc/fstab




sed -i 's/^(.*swap)/#1/' /etc/fstab
echo "vm.swappiness = 1" > /etc/sysctl.d/swappiness.conf
sysctl -p /etc/sysctl.d/swappiness.conf
```

4.jna

下载jna.jar并加入Cassandra的lib下（2.2以上不需要做，因为默认已经有了）

修改/etc/security/limits.conf：

```plain text
* soft memlock unlimited
* hard memlock unlimited
```

### **文件操作**

1.递归查看磁盘的容量或者Cassandra每个keyspace/table占用的大小(第三个按照大小排序取前10个):

```plain text
ll /home/admin/cassandra/data/forseti_fp/android_device_session -rSh|grep Data|tail




du --max-depth=1 /home/admin/cassandra/data/forseti -h
du /home/admin/cassandra/data/forseti/* -sh *
cd /home/admin/cassandra/data/forseti && for i in $(ls -l |grep '^d' |du -s * |sort -nr|awk '{print $2}');do du -sh $i;done | head -10




cd /home/admin/cassandra/data/forseti_fp && for i in $(ls -l |grep '^d' |du -s * |sort -nr|awk '{print $2}');do du -sh $i;done
```

2.找出修改时间在三个月前的文件(第二个命令会删除这些文件):

```plain text
find /home/admin/cassandra/data/forseti/activity_detail -type f -mtime +90 -exec ls -lrth {} ; | grep Data


find /home/admin/cassandra/data/forseti/activity_detail -type f -mtime +90 -exec rm {} ;


find /home/admin/cassandra/data/forseti_fp/android_device_session -type f -mtime +30 -exec rm {} ;






find /home/admin/data/data/forseti_fp/android_device_session* -type f -mtime +25 -exec ls -lrth {} ; | grep Data


find /home/admin/data/data/forseti_fp/android_device_session* -type f -mtime +20 -exec rm {} ;
```

3.查看是否有快照文件, 如果没有文件夹会报错No such file or directory:

```plain text
ls /home/admin/cassandra/data/forseti/velocity/snapshots
```

4.查看所有节点/home目录(数据目录)的磁盘剩余空间:

```plain text
pssh -A -h ip.txt -i 'df -h | grep /home'
./pssh.sh "df -h | grep /home"
```

5.重建数据目录:

```plain text
rm -rf /home/admin/cassandra && mkdir /home/admin/cassandra && chown admin:admin -R /home/admin/cassandra && ll /home/admin/cassandra
```

6.统计每天的Data文件数量:

```plain text
ll /home/admin/cassandra/data/forseti/velocity_app -rth | grep Data |
awk '{count[$6$7]++;}END{for (i in count) {print i"t"count[i]}}' | sort -k 2 -t t


for filename in /home/admin/cassandra/data/forseti/velocity_app/*; do if [ `date -r $filename +%m` == "12" ];then mv $filename ~/12_m; fi done
```

7.compaction时会生成临时文件：

```plain text
[qihuang.zheng@cass048169 ~]$ nodetool compactionstats | grep velocity_global | wc -l
2
[qihuang.zheng@cass048169 ~]$ ll /home/admin/cassandra/data/forseti/velocity_global/ | grep tmp | grep Data | wc -l
2
[qihuang.zheng@cass048169 ~]$ ll /home/admin/cassandra/data/forseti/velocity_partner/ | grep tmp | grep Data | wc -l
4
[qihuang.zheng@cass048169 ~]$ nodetool compactionstats | grep velocity_partner | wc -l
4
```

8.升级时，计算未完成和已完成的文件数量

```plain text
查看la(2.2.6)开头的总文件大小，mc是3.10




find data/data/forseti/velocity_global*/ -name "la*Data.db" -print0 | du --files0-from=- -hc | tail -n1 &&
find data/data/forseti/velocity_global*/ -name "mc*Data.db" -print0 | du --files0-from=- -hc | tail -n1




find data/data/forseti/velocity*/ -name "la*Data.db" -print0 | du --files0-from=- -hc | tail -n1 &&
find data/data/forseti/velocity*/ -name "mc*Data.db" -print0 | du --files0-from=- -hc | tail -n1




ll data/data/forseti/velocity* -rth |grep la |grep Data
```

### **进程**

**进程启停**

1.启动Cassandra进程: /usr/install/cassandra/bin/cassandra

2.查看Cassandra进程: jps -lm 或 ps -ef | grep cassandra

3.杀死Cassandra进程: 下面的命令不需要先用ps查看pid,再kill -9 pid, 直接使用一条命令就可以搞定.

```plain text
kill -9 `jps | grep CassandraDaemon |awk '{print $1}'`
jps | grep CassandraDaemon |awk '{print $1}' | xargs kill -9
```

4.启动Cassandra进程如果报错找不到java:

```plain text
[5] 15:35:54 [FAILURE] 192.168.47.224 Exited with error code 1
Cassandra 2.0 and later require Java 7 or later.
Stderr: which: no java in (/usr/local/bin:/bin:/usr/bin)
```

解决方式:

```plain text
update-alternatives  --install  /usr/bin/java java /usr/install/jdk1.8.0_60/bin/java 1888
update-alternatives  --install  /usr/bin/javac javac /usr/install/jdk1.8.0_60/bin/javac 1888
update-alternatives --config java
update-alternatives --config javac
```

默认java命令链接的是/usr/bin/java，修改成自己安装的路径

```plain text
export JAVA_HOME=/home/admin/zulu8.15.0.1-jdk8.0.92-linux_x64
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$PATH
```

**查询进程**

5.找出Cassandra进程内最耗费CPU的线程(假设Cassandra的进程PID=20893):

A.查看进程相关的所有线程: 使用ps -Lfp pid或者ps -mp pid -o THREAD, tid, time或者top -Hp pid

```plain text
[qihuang.zheng@192-168-47-227 ~]$ top -Hp 20893
  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
44755 admin     24   4  158g  31g  11g R 85.4 50.2 639:34.07 java
44728 admin     24   4  158g  31g  11g R 84.1 50.2 608:12.93 java
44730 admin     24   4  158g  31g  11g R 83.1 50.2 691:32.11 java
44958 admin     20   0  158g  31g  11g R 82.1 50.2   1028:58 java
```

B.TIME列就是各个Java线程耗费的CPU时间, 计算进程ID对应的16进制

```plain text
[qihuang.zheng@192-168-47-227 ~]$ printf "%xn" 44958
af9e
```

C.输出Cassandra进程的堆栈信息，然后根据线程ID的十六进制值grep, 下面表示Cassandra进程耗费的CPU主要在于传输数据.

```plain text
[qihuang.zheng@192-168-47-227 ~]$ jstack 20893 | grep af9e
"STREAM-IN-/192.168.47.225" daemon prio=10 tid=0x00007ff1229ec000 nid=0xaf9e runnable [0x00007ff12c7e9000]
```

6.查看GC信息(第二条格式化输出美观的格式):

```plain text
jstat -gc `jps | grep CassandraDaemon |awk '{print $1}'` 1000




jstat -gc -h 20 `jps | grep CassandraDaemon |awk '{print $1}'` 1000 |
awk '{printf("%10st%10st%10st%10st%10st%10st%10st%10st%10st%10stn",$1,$5,$3,$4,$6,$8,$11,$12,$13,$14)}'
```

## **Cassandra使用**

### **CQL查询客户端**

```plain text
wget https://archive.apache.org/dist/cassandra/2.1.13/apache-cassandra-2.1.13-bin.tar.gz
tar zxf apache-cassandra-2.1.13-bin.tar.gz
apache-cassandra-2.1.13/bin/cqlsh 192.168.6.70
```

1.不进入客户端,直接在终端执行脚本: 第二个命令查看forseti的ks, 会打印很多信息, 如果只是看ks的拓扑信息,使用head.

```plain text
/usr/install/cassandra/bin/cqlsh -e 'desc keyspaces' 192.168.47.202
/usr/install/cassandra/bin/cqlsh -e 'desc keyspace forseti' 192.168.47.202 | head
```

2.创建keyspace,并指定副本数:

```plain text
CREATE KEYSPACE forseti WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
CREATE TABLE velocity_app (
  attribute text,
  partner_code text,
  app_name text,
  type text,
  "timestamp" bigint,
  event text,
  sequence_id text,
  PRIMARY KEY ((attribute, partner_code, app_name, type), sequence_id)
) WITH CLUSTERING ORDER BY (sequence_id DESC);




CREATE KEYSPACE demo WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };




insert into velocity_app(attribute,partner_code,app_name,type,timestamp,event,sequence_id)
values('192.168.0.1','tongdun','tongdun_app','ipAddress',1473427497000,
'{"accountLogin":"zqhxuyuan","ipAddress":"192.168.0.1"}','1473427497000-0001');




for i in `seq 100`;do bin/cqlsh -e "insert into forseti.velocity_app(attribute,partner_code,app_name,type,timestamp,event,sequence_id) values('192.168.0.2','tongdun','tongdun_app','ipAddress',1473427497000$i, '{"accountLogin":"zqhxuyuan","ipAddress":"192.168.0.2"}','1473427497000-000$i');";done
bin/nodetool tablestats forseti.velocity_app




select max(timestamp) from forseti.velocity_app where attribute='192.168.0.2' and partner_code='tongdun' and app_name='tongdun_app' and type='ipAddress';




for i in `seq 1000`;do bin/cqlsh -e "insert into demo.velocity_app(attribute,partner_code,app_name,type,timestamp,event,sequence_id) values('192.168.0.3','tongdun','tongdun_app','ipAddress',1473427497000,'{"accountLogin":"zqhxuyuan","ipAddress":"192.168.0.2"}','1473427497000-000$i');";done
select * from demo.velocity_app where attribute='192.168.0.3' and
partner_code='tongdun' and app_name='tongdun_app' and type='ipAddress';
```

3.导出csv文件(数据文件太大,COPY TO实际也需要查询):

```plain text
cqlsh 192.168.6.52 -e "copy forseti.historical_prices (ticker,date,adj_close,close,high,low,open,volume) to 'historical.csv';"
cqlsh 192.168.47.202 -e "copy cill.channel_device to 'channel_device.csv';"
cqlsh 10.21.21.133 -e "copy cill.channel_device from 'channel_device.csv';"




copy forseti.velocity (attribute,partner_code,app_name,type,"timestamp",event,sequence_id) to '217.csv';
Request did not complete within rpc_timeout.




cqlsh 192.168.47.242 -e "copy forseti.velocity (attribute,partner_code,app_name,type,timestamp,event,sequence_id) to 'test1.csv';"
cqlsh 192.168.47.242 -e "copy forseti.velocity to 'test1.csv';"
cqlsh 192.168.47.202 -e "copy model_result.ip_category to 'ip_category_20161107.csv';"
cqlsh 192.168.47.202 -e "copy model_result.credit_id_labels to 'credit_id_labels.csv';"
cqlsh 10.21.21.19 -e "copy forseti_fp.android_device_time (device_id,gmt_create,device_info,emulator) to 'android_device_time.csv';"
cqlsh 192.168.48.161 -e "copy forseti_fp.device_session_map to 'device_session_map.csv';"




cat /tmp/unitedModeling_id_online_labels.csv |head -1 > id_tbl.cql
sed -i -e "s/,/" text,"/g" id_tbl.cql
echo -e "create table model_resesult.id_online_label("" >> id_tbl.cql
```

4.🙅跳板机直接访问线上数据库

```plain text
在跳板机上生成建表语句:
/usr/install/cassandra/bin/cqlsh -e 'desc keyspace forseti_fp' 192.168.50.20 > forseti_fp.cql




创建keyspace:
CREATE KEYSPACE forseti_fp WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };




修改副本数:
ALTER KEYSPACE forseti_fp WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
ALTER KEYSPACE forseti WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'DC1' : 3};
ALTER KEYSPACE model_result WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'DC1' : 1};
ALTER KEYSPACE realtime WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': '3'}  AND durable_writes = true;
ALTER KEYSPACE gaea WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'dc1' : 3};




https://docs.datastax.com/en/cql/3.1/cql/cql_reference/compactSubprop.html?scroll=compactSubprop__compactionSubpropertiesSTCS




ALTER TABLE device WITH compaction = {'class' : 'SizeTieredCompactionStrategy', 'min_threshold' : 6 };




在跳板机上执行建表语句:
/usr/install/cassandra/bin/cqlsh 192.168.47.227 -f forseti_fp.cql




在跳板机上查询:
[qihuang.zheng@fd047022 ~]$ /usr/install/cassandra/bin/cqlsh 192.168.47.227
cqlsh> desc KEYSPACES ;
system  forseti_fp  system_traces




cqlsh> use forseti_fp ;
cqlsh:forseti_fp> desc TABLES ;
analysis                device              ios_device_info     tcp_stack_ua
```

## **集群维护**

### **删除/下线节点**

A.正在运行的节点: nodetool decommission

B.挂掉的节点:

```plain text
nohup nodetool removenode host-id &
nodetool removenode force




nodetool removenode status
```

### **集群拷贝数据**

```plain text
sstableloader -d 10.21.21.133 -t 1 model_result/mobile_score
```

### **节点上线、扩容**

### **初始化一个新的集群**

**auto_bootstrap**：默认该选项在cassandra.yaml中不存在，表示auto_bootstrap=true

[http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/initialize/initSingleDS.html](http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/initialize/initSingleDS.html)

```plain text
auto_bootstrap: false (Add this setting only when initializing a fresh cluster with no data.)
```

创建一个新的集群，没有任何数据，可以设置auto_bootstrap=false。

**但是设置为true也没有影响，因为对于新集群，没有数据需要同步。**

```plain text
Seed nodes do not bootstrap, which is the process of a new node joining an existing cluster.
For new clusters, the bootstrap process on seed nodes is skipped.
```

对于新的集群，种子节点上的bootstrap过程会被省略。

### **添加新节点**

[http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsAddNodeToCluster.html](http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsAddNodeToCluster.html)

auto_bootstrap - If this option has been set to false, you must set it to true.

This option is not listed in the default cassandra.yaml configuration file and defaults to true.

seed_provider - Make sure that the new node lists at least one node in the existing cluster.

The -seeds list determines which nodes the new node should contact to learn about the cluster and establish the gossip process.

Note: Seed nodes cannot bootstrap. Make sure the new node is not listed in the -seeds list.

Do not make all nodes seed nodes. Please read Internode communications (gossip).

种子节点的目的是：新节点加入集群时，新节点和种子节点联系，学习整个集群，并建立gossip通信。

种子节点不会bootstrap，确保新节点不在-seeds中（针对添加节点到已有的集群，如果是新集群，不存在该限制）。

After all new nodes are running, run nodetool cleanup on each of the previously existing nodes

to remove the keys that no longer belong to those nodes.

Wait for cleanup to complete on one node before running nodetool cleanup on the next node.

Cleanup can be safely postponed for low-usage hours.

所有新节点都运行后，在每个老节点上执行cleanup，删除不属于它们的数据。

### **替换节点**

替换节点，新的节点也需要设置auto_bootstrap=true

### **旧节点当掉**

[http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsReplaceNode.html](http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsReplaceNode.html)

假设要用10.21.38.102替换10.21.38.106，先“当掉”被替换的节点10.21.38.106，然后在新节点10.21.38.102中修改配置

```plain text
2.2.6 在cassandra-env.sh中
JVM_OPTS="$JVM_OPTS -Dcassandra.replace_address=10.21.38.106




3.10在jvm.options中
-Dcassandra.replace_address=10.21.38.106




#cassandra/bin/cassandra -Dcassandra.replace_address=10.21.38.106
```

替换的节点10.21.38.102启动后，需要删除被替换的节点10.21.38.106

### **旧节点正在运行**

[http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsReplaceLiveNode.html](http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsReplaceLiveNode.html)

1. 加入新节点，使用bootstrap加入后，对旧的需要替换的节点执行decommission
2. 停掉旧节点，采用“旧节点当掉”的方式替换

### **Streaming**

[https://support.datastax.com/hc/en-us/articles/206502913-FAQ-How-to-reduce-the-impact-of-streaming-errors-or-failures](https://support.datastax.com/hc/en-us/articles/206502913-FAQ-How-to-reduce-the-impact-of-streaming-errors-or-failures)

## **疑难问题**

### **GC**

[http://docs.datastax.com/en/landing_page/doc/landing_page/troubleshooting/cassandra/gcPauses.html](http://docs.datastax.com/en/landing_page/doc/landing_page/troubleshooting/cassandra/gcPauses.html)

The basic cause of the problem is that the rate of data stored in memory outpaces the rate at which data can be removed.

## **升级**

### **2.0升级到2.1**

[http://zhaoyanblog.com/archives/815.html](http://zhaoyanblog.com/archives/815.html)

[https://docs.datastax.com/en/upgrade/doc/upgrade/cassandra/upgradeCassandraDetails.html](https://docs.datastax.com/en/upgrade/doc/upgrade/cassandra/upgradeCassandraDetails.html)

```plain text
第一步：更改配置文件
把Cassandra 2.0的配置通过比对, 把你原来cassandra.yaml配置文件里的参数移植到新版本的cassandra.yaml配置文件中。
因为cassandra2.1增加了一些配置，也减少了一些配置。所以你不能直接复制过来。你只要把新版的配置文件中有的配置项，从老的配置文件中挪过来就可以了。




第二步：创建快照，防止升级失败
nodetool snapshot keyspace -t snapshot_20150828 创建快照。如果你使用了JNA，快照是通过硬链接实现的，并不会增加磁盘空间，创建快照时间很短。




apache-cassandra-2.0.16/bin/nodetool snapshot forseti -t snapshot_20160420




第三步：停节点
先执行apache-cassandra-2.0.16/bin/nodetool drain关闭写入，同时把数据写入文件。
执行bin/nodetool stodaemon停掉本节点。 --> kill xxx




第四步: 启动新节点
apache-cassandra-2.1.13/bin/cassandra




第五步：重复一到四步把集群所有机器都升级为新版本。这时候如果查询forseti的表应该是能查到数据的。 如果没有，说明有问题！




第六步：在所有节点执行升级sstable文件操作
apache-cassandra-2.1.13/bin/nodetool upgradesstables
```

### **2.1升级到2.2**

```plain text
wget http://192.168.47.211:8000/apache-cassandra-2.2.6_hz.tar.gz
tar zxf apache-cassandra-2.2.6_hz.tar.gz && mv apache-cassandra-2.2.6_hz apache-cassandra-2.2.6




##执行上面的脚本




/usr/install/apache-cassandra-2.1.13/bin/nodetool flush
/usr/install/apache-cassandra-2.1.13/bin/nodetool drain
/usr/install/apache-cassandra-2.1.13/bin/nodetool stopdaemon
/usr/install/apache-cassandra-2.2.6/bin/cassandra




nohup /usr/install/apache-cassandra-2.2.6/bin/nodetool upgradesstables &
```

### **2.2升级到3.10**

3. 修改配置

```plain text
wget 192.168.64.134:8000/apache-cassandra-3.10_sh.tar.gz &&
wget 192.168.64.134:8000/check_cassandra.sh && tar zxf apache-cassandra-3.10_sh.tar.gz
sh check_cassandra.sh 10.21.38.106 apache-cassandra-3.10 sh_credit true
```

4. 确认数据目录

```plain text
cat apache-cassandra-2.2.6/conf/cassandra.yaml |grep -v "#" |grep /home/admin
cat apache-cassandra-3.10/conf/cassandra.yaml |grep -v "#" |grep /home/admin
```

5. 停止每个节点，并重启

```plain text
apache-cassandra-2.2.6/bin/nodetool drain
apache-cassandra-2.2.6/bin/nodetool stopdaemon
apache-cassandra-3.10/bin/cassandra
```

6. 所有节点都重启后，每个节点执行升级

```plain text
nohup apache-cassandra-3.10/bin/nodetool upgradesstables &
```

7. 重做软连接

```plain text
rm -rf cassandra
ln -s apache-cassandra-3.10 cassandra




#检查压缩状态，升级的文件
cassandra/bin/nodetool compactionstats -H
ll data/data/forseti/velocity* -rthh |grep Data
```

升级总结：

8. 杭州credit集群，3个节点，每个节点700G，花了10个小时，每秒钟大概19MB

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624188-313bf300-d8d1-46ec-b423-566c37edca48.png)

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624282-ddce1aac-a192-4f4b-a437-62f5b6378ec5.png)

9. 上海credit集群，4个节点，每个节点700G，花了8个小时

升级时间

```plain text
beginTime=`cat cassandra/logs/system.log |grep upgrade |awk '{print $3" "$4}'|cut -d"," -f1`
endTime=`cat cassandra/logs/system.log |grep UPGRADE |grep events |awk '{print $5" "$6}'|cut -d"," -f1`
timeMs=$(($(date +%s -d "$endTime") - $(date +%s -d "$beginTime")))
#timeHour=`expr $timeMs / 3600`
timeHour=`awk 'BEGIN{printf "%.2fn",('$timeMs'/'3600')}'`
echo "开始时间：$beginTime，结束时间：$endTime，花费时间：$timeHour 小时"
```

### **授权访问**

[http://docs.datastax.com/en/cassandra/2.0/cassandra/security/security_config_native_authenticate_t.html](http://docs.datastax.com/en/cassandra/2.0/cassandra/security/security_config_native_authenticate_t.html)

A.将cassandra.yaml的authenticator从AllowAllAuthenticator修改成密码方式

```plain text
authenticator: PasswordAuthenticator
```

B.增大system_auth keyspace的副本数等于集群中每个数据中心的节点数量

```plain text
ALTER KEYSPACE "Excalibur" WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
ALTER KEYSPACE system_auth WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'dc1' : 3, 'dc2' : 2};
```

在每个节点依次执行nodetool repair, 这样会将副本数据拷贝到其他节点. 不至于一个节点当掉, 导致无法访问C.

….TODO

## **监控**

### **安装opscenter**

opscenter只需要安装server端即可, 启动方式: /usr/install/opscenter-5.2.2/bin/opscenter

启动后会在opscenter下生成一个twistd.pid代表server的进程id.

```plain text
[qihuang.zheng@cass047222 opscenter-5.2.0]$ ps -ef | grep opscenter
admin     6344     1 39 11:22 ?        00:00:01 /usr/bin/python2.6 ./bin/twistd -r epoll -oy bin/start_opscenter.py
```

杀掉opscenter进程的方式:

```plain text
kill -9 `cat /usr/install/opscenter-5.2.2/twistd.pid`
```

### **创建集群和安装agent**

[https://downloads.datastax.com/community/](https://downloads.datastax.com/community/)

访问localhost:8888端口, 初始时没有任何集群, 选择管理已经存在的Cassandra集群. 填写上Cassandra集群的部分地址即可.

会提示: 没有安装Agent: OpsCenter is having trouble connecting with the agents. Click here for more details Fix Now

点击Fix Now, 输入自己能访问这台机器的用户名密码, 完成每个Agent节点的安装.

正常在页面上安装完Agent后, 监控图是没有问题的. 但是经过一段时间有时候会没有数据. 需要修改每个agent的配置.

### **修改agent配置**

agent安装完后, 需要更改各个agent节点的配置信息: 更改local_interface的地址. stomp_interface是opscenter的地址.

vi /var/lib/datastax-agent/conf/address.yaml:

```plain text
stomp_interface: 192.168.47.222
use_ssl: 0
async_pool_size: 200
thrift_max_cons: 200
async_queue_size: 20000
hosts : ["192.168.47.202","192.168.47.203"....]
local_interface: 192.168.47.227
cassandra_conf: /usr/install/cassandra/conf/cassandra.yaml
```

修改完配置, 需要把agent进程杀掉

```plain text
kill -9 `ps -ef|grep datastax_agent_monitor | head -1 |awk '{print $2}'` &&
kill -9 `cat /var/run/datastax-agent/datastax-agent.pid`
```

注意并不需要重启Agent(因为agent节点并没有启动的命令). 启动Agent的方式只能通过web页面的提示点击Fix now重新修复.

彻底删除agent(当opscenter修改配置完并重装还是没有起作用时):

```plain text
kill -9 `ps -ef|grep datastax_agent_monitor | head -1 |awk '{print $2}'` &&
kill -9 `cat /var/run/datastax-agent/datastax-agent.pid` &&
rm -rf /var/lib/datastax-agent &&
rm -rf /usr/share/datastax-agent
```

### **堡垒机无法查看opscenter**

[https://docs.datastax.com/en/opscenter/5.1/opsc/troubleshooting/opscTroubleshootingZeroNodes.html](https://docs.datastax.com/en/opscenter/5.1/opsc/troubleshooting/opscTroubleshootingZeroNodes.html)

### **Loading OpsCenter..**

[https://docs.datastax.com/en/latest-opscenter/opsc/troubleshooting/opscTroubleshootingZeroNodes.html](https://docs.datastax.com/en/latest-opscenter/opsc/troubleshooting/opscTroubleshootingZeroNodes.html)

### **手动安装agent**

[http://docs.datastax.com/en//opscenter/5.0/opsc/install/opsc-agentInstallManual_t.html](http://docs.datastax.com/en//opscenter/5.0/opsc/install/opsc-agentInstallManual_t.html)

```plain text
sftp sftp@192.168.47.13
wget http://192.168.47.211:8000/datastax-agent-5.2.2.tar.gz
wget http://10.21.21.11:8000/datastax-agent-5.2.2.tar.gz




tar zxf datastax-agent-5.2.2.tar.gz
rm datastax-agent-5.2.2/conf/address.yaml
rm datastax-agent-5.2.2/log/agent.log
touch datastax-agent-5.2.2/conf/address.yaml
host=`ifconfig | grep "10.21" | awk '/inet addr/{sub("addr:",""); print $2}'`
echo "stomp_interface: 10.21.21.10" >> datastax-agent-5.2.2/conf/address.yaml
echo "local_interface: $host" >> datastax-agent-5.2.2/conf/address.yaml
echo 'hosts: ["localhost"]' >> datastax-agent-5.2.2/conf/address.yaml
echo "use_ssl: 0" >> datastax-agent-5.2.2/conf/address.yaml
echo "async_pool_size: 200" >> datastax-agent-5.2.2/conf/address.yaml
echo "thrift_max_cons: 200" >> datastax-agent-5.2.2/conf/address.yaml
echo "async_queue_size: 20000" >> datastax-agent-5.2.2/conf/address.yaml
echo "cassandra_conf: /home/admin/cassandra/conf/cassandra.yaml" >> datastax-agent-5.2.2/conf/address.yaml
sed -i -e "s#localhost#$host#g" datastax-agent-5.2.2/conf/address.yaml
echo "alias: $host" >> datastax-agent-5.2.2/conf/address.yaml




datastax-agent-5.2.2/bin/datastax-agent
```

注意：这里的cassandra配置文件cassandra_conf，必须是完整路径！

日志：tail -f datastax-agent-5.2.2/log/agent.log

```plain text
ERROR [clojure-agent-send-off-pool-0] 2016-07-02 18:54:10,272 Can't connect to Cassandra (All host(s) tried for query failed (tried: /10.21.21.10:9042 (com.datastax.driver.core.TransportException: [/10.21.21.10:9042] Cannot connect))), retrying soon.
```

**安装agent超时**

前台Opscenter报错：

```plain text
Error creating cluster: Timeout while adding cluster. Please check the log for details on the problem.
```

后台日志文件：

```plain text
2016-07-07 09:54:32+0800 []  INFO: Adding new cluster 'sh_fp': {u'jmx': {u'username': u'', u'password': '*****', u'port': u'7199'}, u'agents': None, u'cassandra': {u'username': u'', u'seed_hosts': u'10.21.21.19', u'password': '*****', u'cql_port': u'9042'}}
2016-07-07 09:54:32+0800 []  INFO: Starting new cluster services for sh_fp
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Starting services for cluster sh_fp
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Loading event plugins
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Loading event plugin conf ./conf/event-plugins/posturl.conf
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Successfully loaded event plugin conf ./conf/event-plugins/posturl.conf
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Loading event plugin conf ./conf/event-plugins/email.conf
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Successfully loaded event plugin conf ./conf/event-plugins/email.conf
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Done loading event plugins
2016-07-07 09:54:32+0800 []  INFO: Metric caching enabled with 50 points and 1000 metrics cached
2016-07-07 09:54:32+0800 []  INFO: Starting PushService
2016-07-07 09:54:32+0800 [sh_fp]  INFO: Starting CassandraCluster service
2016-07-07 09:54:32+0800 [sh_fp]  INFO: agent_config items: {'restore_req_update_period': 1, 'cassandra_log_location': '/var/log/cassandra/system.log', 'thrift_port': 9160, 'jmx_pass': '*****', 'rollups86400_ttl': -1, 'max_pending_repairs': 5, 'api_port': '61621', 'use_ssl': 0, 'monitored_thrift_port': 9160, 'rollups7200_ttl': 31536000, 'storage_keyspace': 'OpsCenter', 'jmx_operations_pool_size': 4, 'backup_staging_dir': '', 'provisioning': 0, 'metrics_ignored_column_families': '', 'metrics_ignored_keyspaces': 'system, system_traces, system_auth, dse_auth, OpsCenter', 'jmx_user': '', 'cassandra_install_location': '', 'rollups300_ttl': 2419200, 'jmx_port': 7199, 'monitored_cassandra_pass': '', 'monitored_cassandra_port': 9042, 'cassandra_port': 9042, 'metrics_enabled': 1, 'cassandra_pass': '*****', 'rollups60_ttl': 604800, 'monitored_cassandra_user': '', 'ec2_metadata_api_host': '169.254.169.254', 'cassandra_user': '', 'metrics_ignored_solr_cores': ''}
2016-07-07 09:54:32+0800 []  INFO: Starting factory <cassandra.io.twistedreactor.TwistedConnectionClientFactory instance at 0x1c00d3638>
2016-07-07 09:54:32+0800 [sh_fp]  INFO: New Cassandra host 10.21.21.20 discovered
2016-07-07 09:54:32+0800 [sh_fp]  INFO: New Cassandra host 10.21.21.23 discovered
2016-07-07 09:54:32+0800 [sh_fp]  INFO: New Cassandra host 10.21.21.25 discovered
2016-07-07 09:54:32+0800 [sh_fp]  INFO: New Cassandra host 10.21.21.21 discovered
2016-07-07 09:54:32+0800 [sh_fp]  INFO: New Cassandra host 10.21.21.26 discovered
2016-07-07 09:54:32+0800 [sh_fp]  INFO: New Cassandra host 10.21.21.24 discovered
2016-07-07 09:55:01+0800 []  WARN: Error attempting to reconnect to 192.168.50.21, scheduling retry in 60 seconds: errors=Timed out creating connection, last_host=None
2016-07-07 09:55:01+0800 []  WARN: Error attempting to reconnect to 10.21.21.22, scheduling retry in 60 seconds: errors=Timed out creating connection, last_host=None
2016-07-07 09:55:01+0800 []  WARN: Error attempting to reconnect to 10.21.21.22, scheduling retry in 60 seconds: errors=Timed out creating connection, last_host=None
2016-07-07 09:55:01+0800 []  WARN: Error attempting to reconnect to 192.168.50.23, scheduling retry in 60 seconds: errors=Timed out creating connection, last_host=None
2016-07-07 09:55:01+0800 []  WARN: Error attempting to reconnect to 192.168.50.20, scheduling retry in 60 seconds: errors=Timed out creating connection, last_host=None
2016-07-07 09:55:01+0800 []  INFO: Starting factory <cassandra.io.twistedreactor.TwistedConnectionClientFactory instance at 0x7f30a8a756c8>
2016-07-07 09:55:01+0800 []  WARN: Error attempting to reconnect to 192.168.50.24, scheduling retry in 60 seconds: errors=Timed out creating connection, last_host=None
```

### **rolling restart**

统一修改配置文件，并依次重启每个节点，可以使用OpsCenter的Cluster Actions功能。

## **nodetool常用工具(cfstats,cfhistograms,compactionstats,tpstats)**

1.查看数据库所有的表(适合脚本方式获取并批量处理):

```plain text
/usr/install/cassandra/bin/nodetool cfstats forseti_fp.android_device_session
/usr/install/cassandra/bin/nodetool cfstats forseti_fp | grep "Table: " | sed -e 's+^.*: ++'
```

2.查看CF的统计直方图:

```plain text
/usr/install/cassandra/bin/nodetool cfhistograms forseti velocity -h 192.168.47.225
/usr/install/cassandra/bin/nodetool cfhistograms forseti velocity_app -h 192.168.48.162




#2.2版本用proxyhistograms代替cfhistograms
cassandra/bin/nodetool proxyhistograms
```

结果(micros表示微秒)：

```plain text
[admin@cass047202 ~]$ nodetool -h 192.168.48.162 cfhistograms forseti velocity_app
forseti/velocity_app histograms
Percentile SSTables Write Latency Read Latency Partition Size Cell Count
(micros) (micros) (bytes)
50% 1.00 14.00 924.00 770 3
75% 1.00 17.00 1916.00 1597 6
95% 1.00 24.00 3311.00 6866 35
98% 2.00 29.00 4768.00 14237 72
99% 3.00 42.00 6866.00 24601 124
Min 0.00 2.00 30.00 150 0
Max 42.00 263210.00 943127.00 158683580810 962624926
```

3.做/清理keyspace的快照:

```plain text
nodetool status |grep RAC|awk '{print $2}' | while read ip; do echo $ip; nodetool -h $ip snapshot forseti_fp; done
192.168.48.159
Requested creating snapshot(s) for [forseti_fp] with snapshot name [1467716815575]




以159为例：
[admin@fp-cass048159 ~]$ ll /home/admin/cassandra/data/forseti_fp/android_device_session/snapshots/
总用量 4
drwxr-xr-x. 2 admin admin 4096 7月 5 19:07 1467716815575




pssh -A -h ip.txt -i '/usr/install/apache-cassandra-2.0.15/bin/nodetool clearsnapshot forseti_fp'
pssh -A -H 192.168.47.203 -i '/usr/install/apache-cassandra-2.0.15/bin/nodetool clearsnapshot forseti_fp'
```

4.修复集群的每个节点(谨慎使用):

```plain text
nohup nodetool repair -par -pr -- forseti &
```

5.线程统计

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624370-2bd6bbcf-4d79-45a5-9695-4bfd9f862b96.png)

## **日志分析**

Data文件按照日期分组统计大小：

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624450-64eb2afa-d504-4ffd-abb2-082e4cbf0dd2.png)

### **GC长时间**

```plain text
#测试环境查看单节点GC日志
cat /home/admin/output/cassandra/system.log | grep `date +%Y-%m-%d` | grep 'GC for .*: [0-9][0-9][0-9][0-9][0-9]'
#2.0.15查看单节点GC日志
cat /var/log/cassandra/system.log | grep `date +%Y-%m-%d` | grep 'GC for .*: [0-9][0-9][0-9][0-9][0-9]'
cat /var/log/cassandra/system.log | grep 'GC for ConcurrentMarkSweep' | grep `date +%Y-%m-%d`
#202上查看所有节点的GC日志, pssh脚本内容： pssh -A -h ip.txt -i "CMD"
./pssh.sh ip_forseti.txt "cat /var/log/cassandra/system.log | grep `date +%Y-%m-%d` | grep 'GC for .*: [0-9][0-9][0-9][0-9][0-9]'"
./pssh.sh ip_forseti.txt "cat /var/log/cassandra/system.log | grep 2016-04-28 | grep 'GC for .*: [0-9][0-9][0-9][0-9][0-9]'"




#2.1.13查看单节点GC日志
cat /usr/install/cassandra/logs/system.log | grep `date +%Y-%m-%d` | grep 'GC'
cat /usr/install/cassandra/logs/system.log | grep `date +%Y-%m-%d` | grep 'GC in [0-9][0-9][0-9][0-9][0-9]'
```

### **ParNew统计**

```plain text
INFO [ScheduledTasks:1] 2016-03-02 23:05:42,594 GCInspector.java (line 116) GC for ParNew: 406 ms for 2 collections, 8366932456 used; max is 16750411776
INFO [ScheduledTasks:1] 2016-03-02 23:06:57,084 GCInspector.java (line 116) GC for ParNew: 520 ms for 1 collections, 4986064208 used; max is 16750411776
1          2                  3         4           5               6   7    8  9   10      11 12  13 14  15
统计所有的ParNew
cat /var/log/cassandra/system.log | grep "GC for ParNew" | awk '{print $3}' | uniq -c
cat /var/log/cassandra/system.log | grep "GC for ParNew" | awk '{if($11>200) print $3}' | uniq -c
按照时间排序：
cat /var/log/cassandra/system.log* | grep "GC for ParNew" | awk '{print $3}' | uniq -c | awk '{print $2" "$1}' | sort | tail -30
    126 2016-03-01
    153 2016-03-02
    146 2016-03-03




按天统计超过500ms的ParNew
cat /var/log/cassandra/system.log | grep "GC for ParNew" | awk '{if($11>500) print $3}' | uniq -c
     57 2016-03-01
     73 2016-03-02
     89 2016-03-03




按天-小时统计超过500ms的ParNew
cat /var/log/cassandra/system.log | grep "GC for ParNew" | awk '{if($11>500) print $3" "substr($4,0,2)}' | uniq -c | tail
     14 2016-03-14 18
      3 2016-03-14 19
      7 2016-03-14 20
      7 2016-03-14 21
      2 2016-03-14 23
      1 2016-03-15 00
     10 2016-03-15 08
     20 2016-03-15 09
     41 2016-03-15 10
     15 2016-03-15 11
```

CMS GC

```plain text
cat gc.log | grep 'GC in [0-9][0-9][0-9][0-9][0-9]ms' | awk '{print $4":"substr($5,0,2)}' | uniq -c | awk '{print $2" "$1}' | sort
cat /usr/install/cassandra/logs/system.log | grep 'GC in [0-9][0-9][0-9][0-9][0-9]ms' | awk '{print $4":"substr($5,0,2)}' | uniq -c | awk '{print $2" "$1}' | sort




1 2 3 4 5 6 7 8 9 10 11
2016-06-16 03:45:46,213 - ConcurrentMarkSweep GC in 41559ms. CMS Old Gen: 12278864496 -> 11729068408;
2016-06-16 04:07:41,335 - ConcurrentMarkSweep GC in 45019ms. CMS Old Gen: 12658987080 -> 12655359880;
2016-06-16 04:14:15,050 - ConcurrentMarkSweep GC in 41167ms. CMS Old Gen: 12790815136 -> 12784530856; Par Eden Space: 200304 -> 0; Par Survivor Space: 5916848 -> 0
```

### **tombstone与GC的比较**

```plain text
WARN [ReadStage:69] 2016-03-02 07:52:55,238 SliceQueryFilter.java (line 231) Read 1002 live and 5112 tombstone cells in forseti.velocity (see tombstone_warn_threshold). 1001 columns was requested, slices=[dhgate:dh_web_seller:ip3:1453780552156:sequence_id-dhgate:!]




统计多个文件，要加sort
[qihuang.zheng@cass047202 cassandra]$ cat system.log* | grep "tombstone cells in forseti.velocity" | awk '{print substr($3,0,7)}' | sort |  uniq -c | head
  10155 2015-07
192148 2015-08
257728 2015-09
  59041 2015-10
   3499 2015-11
   3189 2015-12
  18997 2016-01
  12411 2016-02
   7466 2016-03
```

### **cfstats和cfhistograms统计**

```plain text
KEYSPACE="forseti"
COLUMN_FAMILY="velocity"
exec >/home/admin/stats/${KEYSPACE}_${COLUMN_FAMILY}_$(date +%s).log 2>&1
function stat_node {
    local host=$1
    /usr/install/cassandra/bin/nodetool -h $host cfstats ${KEYSPACE}.${COLUMN_FAMILY}
    /usr/install/cassandra/bin/nodetool -h $host cfhistograms ${KEYSPACE} ${COLUMN_FAMILY}
}
/usr/install/cassandra/bin/nodetool status forseti |
awk '/192.168/{print $2;}' |
while read ip
do
    echo "On $ip"
    stat_node $ip
done
```

### **large partition**

### **2.2**

日志中打印出超过100MB的分区（2.2版本的格式是(711831539 bytes)）

```plain text
WARN  [CompactionExecutor:11] 2016-06-21 08:58:19,103 SSTableWriter.java:241 - Compacting large partition
forseti/velocity_partner:烟台市:jd-bbs_com:ipAddressCity (711831539 bytes)
```

通过CQLSH查询超时：

```plain text
select count(*) from velocity_partner where attribute='烟台市' and partner_code='jd-bbs_com' and type='ipAddressCity'
OperationTimedOut: errors={}, last_host=192.168.48.162
```

查询其他节点，获取key所在的SSTable文件：

```plain text
$ nodetool -h 192.168.48.162 status |grep RAC|awk '{print $2}' | while read ip; do echo $ip; nodetool -h $ip getsstables forseti velocity_partner 烟台市:jd-bbs_com:ipAddressCity; done
192.168.48.163
/home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-487812-Data.db
/home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-476475-Data.db
192.168.48.162
/home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-459121-Data.db
/home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-tmplink-ka-459182-Data.db
192.168.48.174
192.168.48.173
192.168.48.172
192.168.48.171
192.168.48.170
/home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-361798-Data.db
/home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-237778-Data.db
/home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-360942-Data.db
192.168.48.169
```

验证数据文件大小

```plain text
[admin@fp-cass048163 ~]$ ll /home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-487812-Data.db -h
-rw-r--r--. 1 admin admin 162M 6月 21 08:58 /home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-487812-Data.db
[admin@fp-cass048163 ~]$ ll /home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-476475-Data.db -h
-rw-r--r--. 1 admin admin 161M 6月 18 09:22 /home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-476475-Data.db
```

查询sstable的所有key（大文件时不要这么做）

```plain text
/usr/install/cassandra/bin/sstablekeys /home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-ka-487812-Data.db
```

超过100G的分区

```plain text
cat cassandra/logs/system.log |grep 'large partition'|awk '{if(substr($(NF-1),2,length($(NF-1)))/1000000000 > 100) print $0}'
zgrep 'large partition' cassandra/logs/system.log.* | awk '{if(substr($(NF-1),2,length($(NF-1)))/1000000000 > 100) print $10 " " substr($(NF-1),2,length($(NF-1)))/1000000000"G"}' | sort -rnk2 | awk '{if (!keys[$1]) print $0; keys[$1] = 1;}'
zgrep 'large partition' cassandra/logs/system.log.* | awk '{print $10 " " substr($(NF-1),2,length($(NF-1)))/1000000000"G"}' | sort -rnk2 | awk '{if (!keys[$1]) print $0; keys[$1] = 1;}'
grep "BatchStatement" cassandra/logs/system.log | grep "velocity" | awk '{print $3 ":" substr($4,0,2) " " substr($18,0,length($18)-1)}' | awk '{s[$1] += $2}END{ for(i in s){ print i, s[i]/1000000 } }'
```

### **3.10**

大key报表：

```plain text
cat cassandra/logs/system.log|grep large|grep CompactionExecutor |
awk '{if(NF==14){print $3" "$4" "$10" "$(NF-3);}
else if(NF!=14){printf $3" "$4" ";for(i=10;i<NF-2;i++)printf $i" ";printf "n"}}'




2017-1-1 10:00:00 forset/velocity_global:122:idNumber (111MiB)
#cat largekey.log |sort -k3




zgrep 2017-3-20 cassandra/logs/system.log* |zgrep large|zgrep CompactionExecutor |
awk '{if(NF==14){print $3" "$4" "$10" "$(NF-3);}
else if(NF!=14){printf $3" "$4" ";for(i=10;i<NF-2;i++)printf $i" ";printf "n"}}' |head




#今天、昨天，定时生成报表：时间 大key 大小
#0 1 * * * /home/admin/cassandra_large.sh
day=`date -d 'yesterday' +"%Y-%m-%d"`
#day=`date +%Y-%m-%d`
cat cassandra/logs/system.log|grep large|grep CompactionExecutor|grep "$day" |
awk '{if(NF==14){print $3" "$4" "$10" "$(NF-3);}
else if(NF!=14){printf $3" "$4" ";for(i=10;i<NF-2;i++)printf $i" ";printf "n"}}' > cassandra_large_$day.log




#awk '{max[$3]=max[$3]>$1?max[$3]:$1;}END{for (i in max) print max[i],i}' OFS="t" largekey.log




#(123MiB) to sstable /home/admin/11-Data.db
cat cassandra/logs/system.log |grep 'large partition' | awk '{print $(NF-3)}'
cat cassandra/logs/system.log |grep 'large partition' | awk '{print length($(NF-3))}'
cat cassandra/logs/system.log |grep 'large partition' | awk '{print substr($(NF-3),1,length($(NF-3)))}'
cat cassandra/logs/system.log |grep 'large partition' | awk '{print substr($(NF-3),2,length($(NF-3))-5)}'  #去掉()和MiB,GiB




cat cassandra/logs/system.log |grep 'large partition' | awk '{
if(match($(NF-3),"MiB")) {print substr($(NF-3),2,length($(NF-3))-5)}
else if(match($(NF-3),"GiB")) {print substr($(NF-3),2,length($(NF-3))-5)*1024}}'  # 统一转换为MB




cat cassandra/logs/system.log |grep 'large partition' | awk '
function getMB() {
  if(match($(NF-3),"MiB")) {return substr($(NF-3),2,length($(NF-3))-5)}
  else if(match($(NF-3),"GiB")) {return substr($(NF-3),2,length($(NF-3))-5)*1024}
}
{print getMB()}
'  #用awk的函数来做，$(NF-3)表示倒数第四列，$NF是倒数第一列




cat cassandra/logs/system.log|grep large|grep CompactionExecutor |
awk '{if(NF==14){print $3" "$4" "$10" "$(NF-3);}
else if(NF!=14){printf $3" "$4" ";for(i=10;i<NF-3;i++)printf $i" ";printf $(NF-3);printf "n"}}'




#将(123MiB)转为123，(1.1GiB)转为1024
cat cassandra/logs/system.log|grep large|grep CompactionExecutor |
awk '
function getPartitionKeyMB() {
  if(match($(NF-3),"MiB")) {return substr($(NF-3),2,length($(NF-3))-5)}
  else if(match($(NF-3),"GiB")) {return substr($(NF-3),2,length($(NF-3))-5)*1024}
}
{if(NF==14){print $3" "$4" "$10" "getPartitionKeyMB();}
else if(NF!=14){printf $3" "$4" ";for(i=10;i<NF-3;i++)printf $i" ";printf getPartitionKeyMB();printf "n"}}' |
awk '{print $NF" "$0}' | sort -rn | awk '{$1="";print $0}' |sed 's/.//' |head
#分区大小在最后一列，根据最后一列排序。或者输出的时候把大小放在第一列，就可以sort -n -k1排序.（-n表示按照数值，否则按照字母）




#超过100G的大key
cat cassandra/logs/system.log|grep large|grep CompactionExecutor |
awk '
function printLargeKeyGB(limit) {
  partitionMB=""
  if(match($(NF-3),"MiB")) {
    partitionMB=substr($(NF-3),2,length($(NF-3))-5)
  } else if(match($(NF-3),"GiB")) {
    partitionMB=substr($(NF-3),2,length($(NF-3))-5)*1024
  }
  limitMB=limit*1024
  if(int(partitionMB) > limitMB){
    if(NF==14){
      print $3" "$4" "$10" "partitionMB
    } else if(NF!=14){
      printf $3" "$4" ";
      for(i=10;i<NF-3;i++)printf $i" ";
      printf partitionMB;printf "n"
    }
  }
}
{printLargeKeyGB(100)}'








#使用函数打印时间、key、大小
cat cassandra/logs/system.log|grep large|grep CompactionExecutor | wc -l
cat cassandra/logs/system.log|grep large|grep CompactionExecutor | awk '{if(NF==14){print $3" "$4" "$10" "$(NF-3);}}' |wc -l




#注意%转义字符的处理：grep -v "%"  报错：相对格式来说参数个数不足，跑出范围
cat cassandra/logs/system.log|grep large|grep CompactionExecutor|
awk '
function getKey(){
  partitionKey=""
  if(NF==14){
    partitionKey=$10
  } else if(NF!=14){
    for(i=10;i<NF-3;i++) partitionKey=(partitionKey" "$i)
    partitionKey=substr(partitionKey,2,length(partitionKey))
  }
  return partitionKey
}
function getPartitionKeyMB() {
  if(match($(NF-3),"MiB")) {return substr($(NF-3),2,length($(NF-3))-5)}
  else if(match($(NF-3),"GiB")) {return substr($(NF-3),2,length($(NF-3))-5)*1024}
}
{printf $3" "$4" "getKey()" "getPartitionKeyMB()" n"}
'




#分组求最大值，最后的输出是大小和key，大小放在前面，是为了方便排序
#awk '{max[$1]=max[$1]>$2?max[$1]:$2;}END{for (i in max) print i,max[i]}' OFS="t" url.txt
#awk '{print $NF" "$0}' | sort -rn | awk '{$1="";print $0}' |sed 's/.//' |head
#2017-1-1 10:00:00 forseti/velocity_app:xxx :type 1999
#2017-1-1 10:00:00 forseti/velocity_app:xxx :type 2000 选这个，做法：
#1999 2017-1-1 10:00:00 forseti/velocity_app:xxx :type 1999
#2000 2017-1-1 10:00:00 forseti/velocity_app:xxx :type 2000
cat cassandra/logs/system.log|grep large|grep CompactionExecutor |grep -v "%"|
awk '
function getKey(){
  partitionKey=""
  if(NF==14){
    partitionKey=$10
  } else if(NF!=14){
    for(i=10;i<NF-3;i++) partitionKey=(partitionKey" "$i)
    partitionKey=substr(partitionKey,2,length(partitionKey))
  }
  return partitionKey
}
function getPartitionKeyMB() {
  if(match($(NF-3),"MiB")) {return substr($(NF-3),2,length($(NF-3))-5)}
  else if(match($(NF-3),"GiB")) {return substr($(NF-3),2,length($(NF-3))-5)*1024}
}
{max[getKey()]=max[getKey()]>int(getPartitionKeyMB())?max[getKey()]:int(getPartitionKeyMB());}
END{for (i in max) print int(max[i]),i}
' | sort -rn > largekey.log




#只需要输出type
```

## **性能调优**

### **服务端配置指南**

基础配置项：

```plain text
endpoint_snitch: GossipingPropertyFileSnitch


使用cassandra-rackdc.properties配置文件，可以配置默认的RAC名称，适用于多个机架方式部署


seed_provider：种子节点


同一个集群的每个节点的种子节点必须一致，配置2-3个种子就可以了


compaction_large_partition_warning_threshold_mb: 100


很大的partition实际上就说明了PK的数据很大


commitlog_segment_size_in_mb: 32
commitlog_total_space_in_mb: 30720


每个commit log的大小为32M，文件夹保留30G
```

### **读写配置**

```plain text
memtable_total_space_in_mb


(Default: 1/4 of heap) Specifies the total memory used for all memtables on a node. This replaces the per-table storage settings memtable_operations_in_millions and memtable_throughput_in_mb.


# For workloads with more data than can fit in memory, Cassandra's
# bottleneck will be reads that need to fetch data from
# disk. "concurrent_reads" should be set to (16 * number_of_drives) in
# order to allow the operations to enqueue low enough in the stack
# that the OS and drives can reorder them.
#
# On the other hand, since writes are almost never IO bound, the ideal
# number of "concurrent_writes" is dependent on the number of cores in
# your system; (8 * number_of_cores) is a good rule of thumb.
concurrent_reads: 32
concurrent_writes: 64


datastax documentation:


concurrent_reads: 32
(Default: 32) For workloads（工作负载） with more data than can fit in memory（内存中的数据放不下更多的数据）, the bottleneck is reads fetching data from disk（瓶颈在于从磁盘读取文件的速度）. Setting to (16 × number_of_drives) allows operations（请求） to queue low enough in the stack（进入队列的时间足够短） so that the OS and drives can reorder them（操作系统和磁盘会重新排序，指令重排？）. The default setting applies to both logical volume managed (LVM) and RAID drives. 对于LVM(?)和RAID都适用这个设置。


假设硬盘数量=8，datastax建议的concurrent_reads=8drive*16=128
当前集群硬盘数量=24个，所以concurrent_reads=16*24=384....


concurrent_writes: 64
(Default: 32)note Writes in Cassandra are rarely I/O bound, so the ideal number of concurrent writes depends on the number of CPU cores in your system. The recommended value is 8 × number_of_cpu_cores.


假设CPU数量为24个，datastax建议的concurrent_writes=24cpu*8=128


Cassandra High Performance Book:


It is common to calculate the number of Concurrent Readers by taking the number of cores and multiplying it by two.
Concurrent Writers should be set equal to or higher then Concurrent Readers


假设CPU数量为16个，concurrent_reads=16*2=32， concurrent_writes>=32
```

RAID0的硬盘数量：

```plain text
[admin@cass021026 bin]$ dmesg |grep -i raid
dracut: rd_NO_MD: removing MD RAID activation
megaraid_sas 0000:02:00.0: PCI INT A -> GSI 26 (level, low) -> IRQ 26
megaraid_sas 0000:02:00.0: setting latency timer to 64
megaraid_sas 0000:02:00.0: irq 86 for MSI/MSI-X
megaraid_sas 0000:02:00.0: irq 87 for MSI/MSI-X
megaraid_sas 0000:02:00.0: irq 88 for MSI/MSI-X
....一共24行
megaraid_sas 0000:02:00.0: [scsi0]: FW supports<96> MSIX vector,Online CPUs: <24>,Current MSIX <24>
megaraid_sas 0000:02:00.0: Controller type: MR,Memory size is: 1024MB
megaraid_sas 0000:02:00.0: FW supports: UnevenSpanSupport=1
scsi0 : LSI SAS based MegaRAID driver




[admin@cass021026 bin]$ cat /proc/scsi/scsi
Attached devices:
Host: scsi0 Channel: 02 Id: 00 Lun: 00
  Vendor: DELL     Model: PERC H730 Mini   Rev: 4.26
  Type:   Direct-Access                    ANSI  SCSI revision: 05




[admin@cass021026 bin]$ cat /var/log/dmesg | grep raid
megaraid_sas 0000:02:00.0: PCI INT A -> GSI 26 (level, low) -> IRQ 26
megaraid_sas 0000:02:00.0: setting latency timer to 64
megaraid_sas 0000:02:00.0: irq 86 for MSI/MSI-X
megaraid_sas 0000:02:00.0: irq 87 for MSI/MSI-X
....
megaraid_sas 0000:02:00.0: [scsi0]: FW supports<96> MSIX vector,Online CPUs: <24>,Current MSIX <24>
megaraid_sas 0000:02:00.0: Controller type: MR,Memory size is: 1024MB
megaraid_sas 0000:02:00.0: FW supports: UnevenSpanSupport=1




[admin@cass021026 bin]$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       8.6T  2.1G  8.2T   1% /
tmpfs            32G   12K   32G   1% /dev/shm
/dev/sda1       190M   30M  151M  17% /boot
```

### **JVM配置**

[http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsTuneJVM.html](http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsTuneJVM.html)

[https://docs.datastax.com/en/cassandra/3.0/cassandra/operations/opsTuneJVM.html](https://docs.datastax.com/en/cassandra/3.0/cassandra/operations/opsTuneJVM.html)

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624529-45d0ad24-83b5-42fd-a605-b663bbae070b.png)

基于java的Cassandra,一般为堆分配8G内存，现代机器的内存一般超过8G，Cassandra可以使用额外的内存（分配给堆剩余的内存，即物理内存-JVM堆内存）作为page cache，

当磁盘上的文件(sstable)被访问时会被放入page cache, 所以访问的sstable文件并不是在堆内存里，而是在page cache里，因此也有内存级的访问速度！

如果堆内存很大超过8G，不仅带来了不可预料的GC问题，PageCache占用的内存减少，导致能缓存在PageCache里的文件变少，所以读取磁盘文件时访问速度也将变慢。

总结下堆内存带来的问题：GC变慢，PageCache减少，访问磁盘文件速度变慢。而如果把堆内存控制在不引起太严重的GC，PageCache变多，访问磁盘文件也加快！

为什么堆内存太大会有问题？因为Cassandra的sstable文件保存在本地，内存变大，关于sstable数据的元数据数量也变多，而元数据一般保存在内存中，它的占比和总的数据规模有关。

有一些组件（跟读取流程的一些组件有关）的增长比例和总的内存有关，如果堆内存变大，这些组件也占用更多的内存。

**MAX_HEAP_SIZE&HEAP_NEWSIZE**

Xms和Xmx对应MAX_HEAP_SIZE，-Xmn对应HEAP_NEWSIZE

而MAX_HEAP_SIZE建议为系统内存的1/4,但不超过8G。Java的堆内存不宜过高的原因是：

默认堆1/4大小。我们集群机器内存32G，cassandra-env.sh关于堆内存的配置：-Xms16G，-Xmx16G，-Xmn4G

堆1/4=4G(和Xmn新生代大小一样)。那么堆内存是由什么决定的呢？看下面的两个配置：

HEAP_NEWSIZE为100M*Core(不过有些文章说为Heap的1/4)：

- NEW越大，GC暂停的时间越长，因为在内存中的数据越多 -> GC时间长，次数少；
- NEW越小，GC的代价越大，因为内存很容易满，越容易发生GC -> GC时间短，次数多。

| **config** | **old value** | **suggest value** | **explain** |
| --- | --- | --- | --- |
| MAX_HEAP_SIZE(Xmx) | 16G | 8G | 物理内存的1/4,最多8G |
| HEAP_NEWSIZE(Xms) | 4G | 800M/2G | 100*8cores,堆内存的1/4 |
| memtable_total_space_in_mb | 1G | 2G | 堆内存的1/4 |

超过8G时，Java处理GC回收的能力会有所减弱

现代操作系统对频繁访问的数据会放到PageCache里（内存中），如果JVM堆内存过大，PageCache内存就减少，这部分的工作也不是很好

物理内存32G， 分配给JVM的16G， 新生代=1/4的堆内存

JVM_OPTS=“$JVM_OPTS -Xms16G”

JVM_OPTS=“$JVM_OPTS -Xmx16G”

JVM_OPTS=“$JVM_OPTS -Xmn4G”

大内存

- 会降低GC执行次数(一次可以容纳的东西较多，不需要经常打扫)
- 相应的会增加GC执行耗时(东西太多了，整理的慢)

小内存

- 会缩小单次GC耗时（东西本来就很少，整理的也很快）
- 相应的会增加GC执行次数（进来的数据量不变，每次只整理一小批，就要不停地打扫）

GC中年轻代和老年代大小变化的影响：

| **generation** | **decrement:too small** | **increment:too large** |
| --- | --- | --- |
| Old | 降低FGC执行时间，可能面临OOM，更频繁的FGC | 减少FGC执行次数，单次FGC耗时将会增加 |
| Yung | Minor GC就会频繁执行,转移到老年代的对象增多，也会引起FGC的频繁执行 |   |

[https://segmentfault.com/a/1190000004303843](https://segmentfault.com/a/1190000004303843)

并发模式失败:CMS GC执行中并不会伴随内存压缩，因此GC速度相比Parallel GC会更快一些，

GC清理过程中释放的内存便会成为空闲空间。因为空间不连续，可能会导致在创建大对象时空间不足。

如果老年代尚有300M空闲，却不能为10MB的对象分配足够的连续空间,就会触发内存压缩。

结论：**当内存压缩时，CMS将会变慢**

如果GC执行时间满足以下判断条件，那么GC调优并没那么必须。

- Minor GC执行迅速(50毫秒以内)
- Minor GC执行不频繁(间隔10秒左右一次)
- Full GC执行迅速(1秒以内)
- Full GC执行不频繁(间隔10分钟左右一次)

| 123456789101112 | [qihuang.zheng@fp-cass048162 cassandra]$ jstat -gcutil 31596 1sS0 S1 E O P YGC YGCT FGC FGCT GCT0.99 0.00 61.69 15.02 59.74 12044 546.120 48 20.094 566.2142.56 0.00 3.27 15.21 59.74 12046 546.197 48 20.094 566.2912.56 0.00 49.09 15.21 59.74 12046 546.197 48 20.094 566.2910.00 12.90 30.43 15.21 59.74 12047 546.219 48 20.094 566.3140.00 12.90 84.14 15.21 59.74 12047 546.219 48 20.094 566.3148.59 0.00 39.23 15.43 59.74 12048 546.252 48 20.094 566.3478.59 0.00 83.73 15.43 59.74 12048 546.252 48 20.094 566.3470.00 9.15 40.61 15.57 59.74 12049 546.282 48 20.094 566.3760.00 9.15 87.59 15.57 59.74 12049 546.282 48 20.094 566.3767.39 0.00 43.98 15.73 59.74 12050 546.310 48 20.094 566.404 |
| --- | --- |

MinorGC的平均时间=546/12044=0.04s=40ms，上面统计了10s中，发生了12050-12044=6次MinorGC

FGC的平均时间=20/48=0.41s=410ms，看起来也没有太长时间的FGC。

| 1234567 | [qihuang.zheng@fp-cass048162 cassandra]$ jstat -gccapacity 31596 10sNGCMN NGCMX NGC S0C S1C EC OGCMN OGCMX OGC OC PGCMN PGCMX PGC PC YGC FGC4194304.0 4194304.0 4194304.0 419392.0 419392.0 3355520.0 12582912.0 12582912.0 12582912.0 12582912.0 21248.0 83968.0 45824.0 45824.0 126883 6914194304.0 4194304.0 4194304.0 419392.0 419392.0 3355520.0 12582912.0 12582912.0 12582912.0 12582912.0 21248.0 83968.0 45824.0 45824.0 126887 6914194304.0 4194304.0 4194304.0 419392.0 419392.0 3355520.0 12582912.0 12582912.0 12582912.0 12582912.0 21248.0 83968.0 45824.0 45824.0 126891 6914194304.0 4194304.0 4194304.0 419392.0 419392.0 3355520.0 12582912.0 12582912.0 12582912.0 12582912.0 21248.0 83968.0 45824.0 45824.0 126898 6924194304.0 4194304.0 4194304.0 419392.0 419392.0 3355520.0 12582912.0 12582912.0 12582912.0 12582912.0 21248.0 83968.0 45824.0 45824.0 126902 693 |
| --- | --- |

New : 4,194,304=4G

Old : 12,582,912=12G

New : Old = 4G : 12G = 1 : 3

这是通过-Xms16G -Xmx16G -Xmn4G指定的。

问题：HEAP_NEWSIZE和memtable_total_space_in_mb大小都是堆内存的1/4,两者有关联吗？

几种GC的发生：

- Eden满了，发生minor gc，将eden中存活的移动到Survivor
- Survivor满了，会将eden中存活的和survivor中存活的移动到另一个survivor
- 对象在survivor中超过指定年龄，被promot到old
- old满了，发生FullGC

if you see long ParNew GC pauses it’s because many objects are being promoted.

If you have long ParNew pauses, it means that a lot of the objects in eden are not (yet) garbage, and they’re being copied around to the survivor space, or into the old gen.

通常来说大部分的对象存活周期都很短(short lived objects)。找出并移除要被回收的对象是很快的。

但是将没有被回收的对象从eden移动到survivor，或者从survivor移动到old，则很慢。

长时间的ParNew GC停顿，表示新生代的很多对象没有被回收，需要移动的对象很多，因此耗时较长。

哪些对象会被提升：在新生代存活超过MaxTenuringThreshold(默认为1，因为大部分对象都是short live)

By increasing the young generation space it decreases the frequency at which we have to run GC because more objects can accumulate before we reach 75% capacity. By increasing the young generation and the MaxTenuringThreshold you give the short lived objects more time to die, and dead objects don’t get promoted.

As of Cassandra 2.0, there are two major pieces of the storage engine that still depend on the JVM heap: memtables and the key cache.

The only thing that should live in tenured space is the key cache and memtables.

Although no random I/O occurs, compaction can still be a fairly heavyweight operation. During compaction, there is a temporary spike in disk space usage and disk I/O because the old and new SSTables co-exist. To minimize deteriorating read speed, compaction runs in the background.

To lessen the impact of compaction on application requests, Cassandra performs these operations:

- Throttles compaction I/O to compaction_throughput_mb_per_sec (default 16MB/s).
- Requests that the operating system pull newly compacted partitions into the page cache when the key cache indicates that the compacted partition is hot for recent reads.

off-heap保存的是什么? [http://noflex.org/cassandra-component-on-heap-or-off-heap/](http://noflex.org/cassandra-component-on-heap-or-off-heap/)

cassandra 2.0 and later use offheap for

- bloom filter
- compression offset map
- partition summary
- index samples
- row cache

### **从CMS更改为G1 GC**

### **G1 GC LOG**

| 123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167 | 2016-07-07T09:49:22.341+0800: 942859.604: Total time for which application threads were stopped: 0.0814731 seconds, Stopping threads took: 0.0002340 seconds2016-07-07T09:49:29.213+0800: 942866.476: Total time for which application threads were stopped: 0.0012369 seconds, Stopping threads took: 0.0002430 seconds{Heap before GC invocations=159966 (full 2):garbage-first heap total 16777216K, used 14876451K [0x00000003c0000000, 0x00000003c0804000, 0x00000007c0000000)region size 8192K, 1074 young (8798208K), 15 survivors (122880K)Metaspace used 35401K, capacity 35916K, committed 36224K, reserved 1081344Kclass space used 3719K, capacity 3839K, committed 3968K, reserved 1048576K2016-07-07T09:49:29.213+0800: 942866.477: [GC pause (GCLocker Initiated GC) (young)Desired survivor size 566231040 bytes, new threshold 15 (max 15)- age 1: 16845608 bytes, 16845608 total- age 2: 6895480 bytes, 23741088 total- age 3: 7210040 bytes, 30951128 total- age 4: 6712376 bytes, 37663504 total- age 5: 6050320 bytes, 43713824 total- age 6: 5356392 bytes, 49070216 total- age 7: 5514552 bytes, 54584768 total- age 8: 5607616 bytes, 60192384 total- age 9: 5430416 bytes, 65622800 total- age 10: 5450352 bytes, 71073152 total- age 11: 5550480 bytes, 76623632 total- age 12: 5110560 bytes, 81734192 total- age 13: 5440256 bytes, 87174448 total- age 14: 5565200 bytes, 92739648 total- age 15: 5550672 bytes, 98290320 total(to-space exhausted), 17.8874292 secs][Parallel Time: 16666.1 ms, GC Workers: 13][GC Worker Start (ms): Min: 942866476.9, Avg: 942866477.0, Max: 942866477.1, Diff: 0.2][Ext Root Scanning (ms): Min: 2.9, Avg: 3.0, Max: 3.1, Diff: 0.2, Sum: 39.0][Update RS (ms): Min: 71.8, Avg: 72.2, Max: 72.7, Diff: 0.9, Sum: 938.2][Processed Buffers: Min: 52, Avg: 75.5, Max: 102, Diff: 50, Sum: 982][Scan RS (ms): Min: 0.1, Avg: 0.2, Max: 0.4, Diff: 0.3, Sum: 2.1][Code Root Scanning (ms): Min: 0.0, Avg: 0.0, Max: 0.0, Diff: 0.0, Sum: 0.1][Object Copy (ms): Min: 16589.9, Avg: 16590.4, Max: 16590.6, Diff: 0.7, Sum: 215675.3][Termination (ms): Min: 0.0, Avg: 0.1, Max: 0.2, Diff: 0.2, Sum: 1.3][Termination Attempts: Min: 1, Avg: 1.0, Max: 1, Diff: 0, Sum: 13][GC Worker Other (ms): Min: 0.0, Avg: 0.1, Max: 0.1, Diff: 0.1, Sum: 0.7][GC Worker Total (ms): Min: 16665.8, Avg: 16665.9, Max: 16666.0, Diff: 0.2, Sum: 216656.7][GC Worker End (ms): Min: 942883142.9, Avg: 942883142.9, Max: 942883142.9, Diff: 0.1][Code Root Fixup: 0.1 ms][Code Root Purge: 0.0 ms][Clear CT: 2.0 ms][Other: 1219.2 ms][Evacuation Failure: 1212.5 ms][Choose CSet: 0.0 ms][Ref Proc: 0.7 ms][Ref Enq: 0.0 ms][Redirty Cards: 4.4 ms][Humongous Register: 0.1 ms][Humongous Reclaim: 0.1 ms][Free CSet: 0.7 ms][Eden: 8472.0M(8464.0M)->0.0B(1184.0M) Survivors: 120.0M->1080.0M Heap: 14.2G(16.0G)->12.0G(16.0G)]Heap after GC invocations=159967 (full 2):garbage-first heap total 16777216K, used 12625455K [0x00000003c0000000, 0x00000003c0804000, 0x00000007c0000000)region size 8192K, 135 young (1105920K), 135 survivors (1105920K)Metaspace used 35401K, capacity 35916K, committed 36224K, reserved 1081344Kclass space used 3719K, capacity 3839K, committed 3968K, reserved 1048576K}[Times: user=41.47 sys=3.94, real=17.88 secs]2016-07-07T09:49:47.101+0800: 942884.364: Total time for which application threads were stopped: 17.8884392 seconds, Stopping threads took: 0.0001048 seconds2016-07-07T09:49:48.103+0800: 942885.366: Total time for which application threads were stopped: 0.0013006 seconds, Stopping threads took: 0.0002328 seconds{Heap before GC invocations=159967 (full 2):garbage-first heap total 16777216K, used 13837871K [0x00000003c0000000, 0x00000003c0804000, 0x00000007c0000000)region size 8192K, 283 young (2318336K), 135 survivors (1105920K)Metaspace used 35401K, capacity 35916K, committed 36224K, reserved 1081344Kclass space used 3719K, capacity 3839K, committed 3968K, reserved 1048576K2016-07-07T09:49:48.248+0800: 942885.511: [GC pause (G1 Evacuation Pause) (young) (initial-mark)Desired survivor size 150994944 bytes, new threshold 1 (max 15)- age 1: 1132372544 bytes, 1132372544 total- age 2: 18088 bytes, 1132390632 total- age 3: 6072 bytes, 1132396704 total- age 4: 7760 bytes, 1132404464 total- age 5: 8248 bytes, 1132412712 total- age 6: 6376 bytes, 1132419088 total- age 7: 4384 bytes, 1132423472 total- age 8: 5496 bytes, 1132428968 total- age 9: 3088 bytes, 1132432056 total- age 10: 4136 bytes, 1132436192 total- age 11: 3048 bytes, 1132439240 total- age 12: 3728 bytes, 1132442968 total- age 13: 1944 bytes, 1132444912 total- age 14: 3136 bytes, 1132448048 total- age 15: 2440 bytes, 1132450488 total, 0.5353097 secs][Parallel Time: 528.2 ms, GC Workers: 13][GC Worker Start (ms): Min: 942885512.0, Avg: 942885512.1, Max: 942885512.2, Diff: 0.2][Ext Root Scanning (ms): Min: 2.9, Avg: 3.0, Max: 3.1, Diff: 0.2, Sum: 38.7][Update RS (ms): Min: 28.9, Avg: 29.2, Max: 30.6, Diff: 1.8, Sum: 379.2][Processed Buffers: Min: 54, Avg: 84.8, Max: 133, Diff: 79, Sum: 1103][Scan RS (ms): Min: 14.6, Avg: 16.2, Max: 16.5, Diff: 1.9, Sum: 210.2][Code Root Scanning (ms): Min: 0.0, Avg: 0.0, Max: 0.0, Diff: 0.0, Sum: 0.1][Object Copy (ms): Min: 479.2, Avg: 479.4, Max: 479.5, Diff: 0.3, Sum: 6231.7][Termination (ms): Min: 0.0, Avg: 0.2, Max: 0.3, Diff: 0.3, Sum: 3.1][Termination Attempts: Min: 1, Avg: 395.1, Max: 486, Diff: 485, Sum: 5136][GC Worker Other (ms): Min: 0.0, Avg: 0.1, Max: 0.1, Diff: 0.1, Sum: 0.8][GC Worker Total (ms): Min: 527.9, Avg: 528.0, Max: 528.1, Diff: 0.2, Sum: 6863.7][GC Worker End (ms): Min: 942886040.0, Avg: 942886040.0, Max: 942886040.1, Diff: 0.1][Code Root Fixup: 0.1 ms][Code Root Purge: 0.0 ms][Clear CT: 1.4 ms][Other: 5.6 ms][Choose CSet: 0.0 ms][Ref Proc: 0.4 ms][Ref Enq: 0.0 ms][Redirty Cards: 3.1 ms][Humongous Register: 0.0 ms][Humongous Reclaim: 0.1 ms][Free CSet: 0.7 ms][Eden: 1184.0M(1184.0M)->0.0B(1544.0M) Survivors: 1080.0M->288.0M Heap: 13.2G(16.0G)->12.4G(16.0G)]Heap after GC invocations=159968 (full 2):garbage-first heap total 16777216K, used 13010479K [0x00000003c0000000, 0x00000003c0804000, 0x00000007c0000000)region size 8192K, 36 young (294912K), 36 survivors (294912K)Metaspace used 35401K, capacity 35916K, committed 36224K, reserved 1081344Kclass space used 3719K, capacity 3839K, committed 3968K, reserved 1048576K}[Times: user=6.90 sys=0.01, real=0.54 secs]2016-07-07T09:49:48.784+0800: 942886.047: [GC concurrent-root-region-scan-start]2016-07-07T09:49:48.784+0800: 942886.047: Total time for which application threads were stopped: 0.5368812 seconds, Stopping threads took: 0.0002119 seconds2016-07-07T09:49:48.973+0800: 942886.236: [GC concurrent-root-region-scan-end, 0.1896420 secs]2016-07-07T09:49:48.973+0800: 942886.236: [GC concurrent-mark-start]{Heap before GC invocations=159968 (full 2):garbage-first heap total 16777216K, used 14591535K [0x00000003c0000000, 0x00000003c0804000, 0x00000007c0000000)region size 8192K, 229 young (1875968K), 36 survivors (294912K)Metaspace used 35401K, capacity 35916K, committed 36224K, reserved 1081344Kclass space used 3719K, capacity 3839K, committed 3968K, reserved 1048576K2016-07-07T09:49:51.216+0800: 942888.479: [GC pause (G1 Evacuation Pause) (young)Desired survivor size 121634816 bytes, new threshold 1 (max 15)- age 1: 277632680 bytes, 277632680 total, 0.4639409 secs][Parallel Time: 455.9 ms, GC Workers: 13][GC Worker Start (ms): Min: 942888479.3, Avg: 942888479.4, Max: 942888479.5, Diff: 0.3][Ext Root Scanning (ms): Min: 2.8, Avg: 3.0, Max: 3.1, Diff: 0.2, Sum: 38.4][Update RS (ms): Min: 166.4, Avg: 167.6, Max: 168.7, Diff: 2.4, Sum: 2178.7][Processed Buffers: Min: 59, Avg: 81.7, Max: 109, Diff: 50, Sum: 1062][Scan RS (ms): Min: 6.8, Avg: 7.9, Max: 8.2, Diff: 1.4, Sum: 102.4][Code Root Scanning (ms): Min: 0.0, Avg: 0.0, Max: 0.0, Diff: 0.0, Sum: 0.0][Object Copy (ms): Min: 277.0, Avg: 277.0, Max: 277.1, Diff: 0.2, Sum: 3601.5][Termination (ms): Min: 0.0, Avg: 0.0, Max: 0.0, Diff: 0.0, Sum: 0.0][Termination Attempts: Min: 1, Avg: 1.0, Max: 1, Diff: 0, Sum: 13][GC Worker Other (ms): Min: 0.0, Avg: 0.1, Max: 0.1, Diff: 0.1, Sum: 0.8][GC Worker Total (ms): Min: 455.5, Avg: 455.6, Max: 455.7, Diff: 0.2, Sum: 5923.0][GC Worker End (ms): Min: 942888935.0, Avg: 942888935.0, Max: 942888935.1, Diff: 0.1][Code Root Fixup: 0.3 ms][Code Root Purge: 0.0 ms][Clear CT: 1.2 ms][Other: 6.6 ms][Choose CSet: 0.0 ms][Ref Proc: 3.6 ms][Ref Enq: 0.0 ms][Redirty Cards: 1.7 ms][Humongous Register: 0.1 ms][Humongous Reclaim: 0.1 ms][Free CSet: 0.5 ms][Eden: 1544.0M(1544.0M)->0.0B(960.0M) Survivors: 288.0M->232.0M Heap: 13.9G(16.0G)->13.0G(16.0G)]Heap after GC invocations=159969 (full 2):garbage-first heap total 16777216K, used 13616687K [0x00000003c0000000, 0x00000003c0804000, 0x00000007c0000000)region size 8192K, 29 young (237568K), 29 survivors (237568K)Metaspace used 35401K, capacity 35916K, committed 36224K, reserved 1081344Kclass space used 3719K, capacity 3839K, committed 3968K, reserved 1048576K}[Times: user=5.99 sys=0.00, real=0.46 secs]2016-07-07T09:49:51.680+0800: 942888.943: Total time for which application threads were stopped: 0.4655046 seconds, Stopping threads took: 0.0001802 seconds2016-07-07T09:49:51.680+0800: 942888.943: [GC concurrent-mark-reset-for-overflow]{Heap before GC invocations=159969 (full 2):garbage-first heap total 16777216K, used 14599727K [0x00000003c0000000, 0x00000003c0804000, 0x00000007c0000000)region size 8192K, 149 young (1220608K), 29 survivors (237568K)Metaspace used 35401K, capacity 35916K, committed 36224K, reserved 1081344Kclass space used 3719K, capacity 3839K, committed 3968K, reserved 1048576K |
| --- | --- |

### **Memtable**

[http://www.datastax.com/dev/blog/off-heap-memtables-in-Cassandra-2-1](http://www.datastax.com/dev/blog/off-heap-memtables-in-Cassandra-2-1)

观察线上某台机器的内存总是比其他机器要大，用jvisualvm连接机器，发现堆内存使用基本上1s增加1G，然后回到10G左右，继续

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624609-f4d0fc1e-a759-445e-b666-e994286765ff.png)

左图中CPU很高的部分，以及右图比较平滑的部分，是在做内存抽样操作。这时候内存中的数据不会被YGC释放，所以一直上升

Zabbix观察老年代的占用从10G到15G差不多20分钟一次（红色），而黄色部分是新生代，则很频繁

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624700-b8ff6732-0a86-47a5-bcdd-9a644241f727.png)

通过jstat观察，Eden基本上一秒增长1G，和jvisualvm的观察结果一致

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624786-57c852c8-a63d-47f3-a514-bfcd12f7f32e.png)

grafana的观察结果，162机器与其他机器Old的变化也比较频繁，而且跟zabbix的波浪状态类似

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624888-418ed5be-f3c5-4d91-b9d1-889624816fcd.png)

对应的YoungGC也比其他机器的耗时要高（最上面的绿色曲线）

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037624973-e4e0ecaf-ca28-4fe0-8f2b-bbae9b1a7a28.png)

Cassandra的Memtable在2.2之后，支持Offheap的存储，默认heap_buffers时，写入Memtable的数据直接分配在堆内，

堆内的大部分对象会在YGC时被回收，所以你可以看到堆内存一上一下，变得很快，这是因为数据不断写入到Memtable，

然后在YGC回收时释放内存。

```plain text
# Specify the way Cassandra allocates and manages memtable memory.
# Options are:
#   heap_buffers:    on heap nio buffers
#   offheap_buffers: off heap (direct) nio buffers
#   offheap_objects: native memory, eliminating nio buffer heap overhead
memtable_allocation_type: heap_buffers
```

将memtable_allocation_type配置改为：offheap_buffers后，上面的几张图中可以看到Old变化不再那么快，YGC的时间也降下来了。

这是因为将Memtable的对象放在堆外之后，这部分内存不会被GC管理，当然YGC就没有压力。而且堆外内存的是否是通过native方式分配和释放，

而Memtable在不用了之后，堆外占用的内存会自动释放。

如果再用jvisualvm查看的话，会发现堆内存还是一上一下变得很快，这是因为堆内存包括堆内和堆外，并不是说堆外内存不属于堆，

实际上它还是Java进程的一部分。而一上一下很快，YGC仍然很频繁，只不过这部分内存不是在堆内释放，而是在堆外释放。

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037625069-511cc713-554b-4b11-9376-882ff3a72485.png)

上图中右侧部分，也是在做抽样，CPU中间部分几乎为0的是在做heap dump

如果用jstat看的话，其实Eden的变化还是几乎1s1G，不过Eden实际上是分配在堆外的，jstat无法反映内存分配在堆内还是堆外

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037625149-646176d5-dd60-4143-a3f4-771bc80da44b.png)

下面是内存的抽样，有三种类型占用很大，byte[],HeapByteBuffer,int[]

![](assets/images/learning/database/cassandra/cassandra-daily-ops/1698037625235-a7eee5eb-f412-4366-987f-0d74ffc0590e.png)

**Memtable存储类型**

| 123456 | # Specify the way Cassandra allocates and manages memtable memory.# Options are:# heap_buffers: on heap nio buffers (defaults)# offheap_buffers: off heap (direct) nio buffers# offheap_objects: native memory, eliminating nio buffer heap overheadmemtable_allocation_type: offheap_objects |
| --- | --- |

2.0之前Memtable和KeyCache都在Heap中，如果能把这部分数据从Java的Heap移动到native内存，这样吞吐量就可以跟上来了。

Memtable不归Java的堆管理后，可以使用剩余的物理内存，OffHeap指的是在Java中直接将对象直接分配到堆外内存，这部分内存不归JVM管理。

flush frequently -> small sstable -> more sstable -> more compaction

flush infrequence -> bigger sstable -> less sstable -> less compaction

Memtable很小->数据一下子就写满了Memtable->越容易发生flush->生成的sstable和Memtable大小有关，所以很小->因为很容易flush，所以sstable数量很多->sstable越多，越容易发生compaction

Memtable越大->不容易写满Memtabel->不容易发生flush->即使发生flush生成的sstable文件也比较大->不容易flush，sstable数量不多->不容易compaction

堆外内存、OffHeap、DirectorBuffer、Native Memory的关系：堆外内存=OffHeap，通常Java使用DirectBuffer操作堆外内存.

offheap_buffers: moves the cell name and value to DirectBuffer objects. This has the lowest impact on reads — the values are still “live” Java buffers — but only reduces heap significantly when you are storing large strings or blobs.

offheap_objects: moves the entire cell off heap, leaving only the NativeCell reference containing a pointer to the native (off-heap) data. This makes it effective for small values like ints or uuids as well, at the cost of having to copy it back on-heap temporarily when reading from it.

cell指的是column，offheap_buffers仅仅是列名和列值移动到offheap的DirectBuffer对象中。

offheap_objects的适用场景是：most of reads are coming from sstables on disk, not unflushed data in memtables。

因为如果要读取的数据还是OffHeap的memtables中，则必须从off-heap拷贝到on-heap，才能返回给客户端。

tobert:Offheap memtables can improve write-heavy workloads by reducing the amount of data stored on the Java heap. 1-2GB of offheap memory should be sufficient for most workloads. The memtable size whould be left at 25% of the heap as well, since it is still in use when offheap is in play.

An additional performance boost can be realized by installing and enabling jemalloc. On common distros(通常的linux发行版) this is usually a yum/apt-get install away. Worst case you can simply install the .so file in /usr/local/lib or similar. Instructions for configuring it are in cassandra-env.sh.

**Memtable清理时机**

[http://docs.datastax.com/en/cassandra/3.0/cassandra/operations/opsMemtableThruput.html](http://docs.datastax.com/en/cassandra/3.0/cassandra/operations/opsMemtableThruput.html)

10. commitlog_total_space_in_mb：提交日志超过总大小，由于没有剩余空间，需要将提交日志刷写到磁盘，才能释放提交日志的空间。将memtable刷写到磁盘的sstable后，对应的提交日志文件就可以删除，释放提交日志的空间。
11. memtable_cleanup_threshold：清理memtable的阈值=1/(memtable_flush_writers + 1)，默认memtable_flush_writers等于2。

memtable_flush_writers表示刷写memtable的线程数，写线程会阻塞磁盘IO，每个写线程在阻塞期间都在内存中持有一个memtable。

memtable_offheap_space_in_mb

| 1234567891011121314151617181920212223242526 | # Total permitted memory to use for memtables. Cassandra will stop# accepting writes when the limit is exceeded until a flush completes,# and will trigger a flush based on memtable_cleanup_threshold# If omitted, Cassandra will set both to 1/4 the size of the heap.# memtable_heap_space_in_mb: 2048memtable_offheap_space_in_mb: 2048# Ratio of occupied（占用） non-flushing memtable size to total permitted size# that will trigger a flush of the largest memtable. Larger mct will# mean larger flushes and hence less compaction, but also less concurrent# flush activity which can make it difficult to keep your disks fed# under heavy write load.## memtable_cleanup_threshold defaults to 1 / (memtable_flush_writers + 1)# memtable_cleanup_threshold: 0.11# This sets the amount of memtable flush writer threads. These will# be blocked by disk io, and each one will hold a memtable in memory# while blocked.## memtable_flush_writers defaults to the smaller of (number of disks,# number of cores), with a minimum of 2 and a maximum of 8.## If your data directories are backed by SSD, you should increase this# to the number of cores.#memtable_flush_writers: 8 |
| --- | --- |

memtable的flush writer线程数量，将memtable刷写成sstable。通常每个表都对应一个memtable，如果只用一个刷写线程，在多个表

memtable刷写成sstable，并不是memtable大小刚好满足配置的大小时才flush。比如上面分配了2G堆外内存作为Memtable的总大小(total permitted size)，

当剩余0.11*2G=225M(non-flushing memtable size)时，才会触发flush。

默认的memtable_flush_writers=8，清理阈值=1/9=0.11，如果设置memtable_flush_writers=CPU核数=24，则清理阈值=1/25=0.04，比率从0.11减少到0.04。

因为总大小不变，所以剩余0.04*2048=81M的时候才会触发flush。

tobert: if you have a lot of flush writers, your cleanup threshold is going to be very low and cause frequent flushing for no good reason. A safe starting value for a cluster with few tables is 0.15 (15% of memtable space). If you have lots of active tables, a smaller value may be better, but watch out for compaction cost.

**memtable_cleanup_threshold**

(Default: 1/(memtable_flush_writers + 1))note. Ratio used for automatic memtable flush. Casssandra adds memtable_heap_space_in_mb to memtable_offheap_space_in_mb and multiplies the total by memtable_cleanup_threshold to get a space amount in MB. When the total amount of memory being used by all non-flushing memtables exceeds this amount, Casandra flushes the largest memtable to disk.

For example, consider a system in which the total of memtable_heap_space_in_mb and memtable_offheap_space_in_mb is 1000, and memtable_cleanup_threshold is 0.50. The “memtable_cleanup” amount is 500MB. This system has two memtables: Memtable A (150MB) and Memtable B (350MB) . When either memtable increases, the total space they use exceeds 500MB. When this happens, Cassandra flushes the Memtable B to disk.

A larger value for memtable_cleanup_threshold means larger flushes, less frequent flushes and potentially less compaction activities, but also less concurrent flush activity, which can make it difficult to keep the disks saturated under heavy write load.

This section documents the formula used to calculate the ratio based on the number of memtable_flush_writers. The default value in cassandra.yaml is 0.11, which works if the node has many disks or if you set the node’s memtable_flush_writers to 8. As another example, if the node uses a single SSD, the value for memttable_cleanup_threshold computes to 0.33, based on the minimum memtable_flush_writers value of 2

### **KeyCache**

| 12345678910 | [admin@cass048171 ~]$ ll cassandra/saved_caches/-rw-r–r–. 1 admin admin 180 4月 27 06:06 forseti-velocity_app-KeyCache-b.db-rw-r–r–. 1 admin admin 219847918 4月 27 06:06 forseti-velocity_global-KeyCache-b.db-rw-rw-r–. 1 admin admin 296004448 8月 2 06:08 KeyCache-ba.db-rw-r–r–. 1 admin admin 26095 4月 27 06:06 OpsCenter-rollups60-KeyCache-b.db-rw-r–r–. 1 admin admin 52 4月 27 06:06 system-local-KeyCache-b.db-rw-r–r–. 1 admin admin 175 4月 27 06:06 system-peers-KeyCache-b.dbINFO 00:42:40 reading saved cache /home/admin/cassandra/saved_caches/KeyCache-ba.dbINFO 00:43:31 Completed loading (51327 ms; 931872 keys) KeyCache cache |
| --- | --- |

KeyCache大小≈280M，keys的数量有931872个，平均每个key的大小=296004448/931872=317.6449 byte

### **RowCache**

[http://blog.nosqlfan.com/html/3932.html](http://blog.nosqlfan.com/html/3932.html) Ori: [http://www.datastax.com/dev/blog/caching-in-cassandra-1-1](http://www.datastax.com/dev/blog/caching-in-cassandra-1-1)

主键缓存就是对Cassandra表的主键的缓存，主键缓存能够节约内存和CPU时间。但是，如果仅仅是开启主键缓存的话，我们在取具体每一行数据时还是可能会导致磁盘操作。

行缓存类似于传统的Memcached缓存，其机制是，**当某一行数据被访问时，将其加载到内存中，这样后续的访问只需要通过内存访问就能拿到这一行数据**。

在一般的场景下，你可能会选择开启主键缓存或者行缓存，这样会提高读性能。但是对那种不经常读的表，就可以完全不开启缓存了。

OpsCenter通过查看缓存的效率，通过来说，缓存达到90％以上的命中率是比较正常的。

如果你某个表的行缓存达不到这个数，那么建议你将这个表的行缓存去掉，仅保留主键缓存。

这样它原本用在行缓存上的内存就可以被其它命中率更高的表更高效地使用了。

| 1234567 | row_cache_save_period: 0key_cache_save_period: 14400preheat_kernel_page_cache: falsekey_cache_size_in_mb: 512row_cache_size_in_mb: 0saved_caches_directory: /home/admin/cassandra/saved_cachescompaction_preheat_key_cache: true |
| --- | --- |

[http://www.datastax.com/dev/blog/row-caching-in-cassandra-2-1](http://www.datastax.com/dev/blog/row-caching-in-cassandra-2-1)

when data needs to be read from disk, it works best when it is performed as a single sequential operation.

In order to design an effective data model in Cassandra, it’s good to keep these best practices in mind:

Use clustering columns in your tables so that your rows are ordered on disk in the same order you want them in when read.

Use the built-in caching mechanisms to limit the amount of reads from disk.

谨慎使用Cassandra-2.0的RowCache. 所以上面的配置中row_cache_size=0.

### **compaction**

| 12345678910111213141516 | compaction_throughput_mb_per_sec: 128(Default: 16) Throttles compaction to the specified total throughput across the entire system. The faster you insert data, the faster you need to compact in order to keep the SSTable count down. The recommended value is 16 to 32 times the rate of write throughput (in MB/second). Setting the value to 0 disables compaction throttling.compaction的速度限制，使用nodetool compactionstats查看如果发现append task很多，可以设置为0不限速即throughput大小越大，compaction越快完成，否则compaction很慢的话，任务会堆积越来越多concurrent_compactors: 4(Default: Smaller of number of disks or number of cores, with a minimum of 2 and a maximum of 8 per CPU core)note Sets the number of concurrent compaction processes allowed to run simultaneously on a node, not including validation compactions for anti-entropy repair. Simultaneous compactions help preserve read performance in a mixed read-write workload by mitigating the tendency of small SSTables to accumulate during a single long-running compaction.If your data directories are backed by SSD, increase this value to the number of cores. If compaction running too slowly or too fast, adjust compaction_throughput_mb_per_sec first.SSD硬盘，可以增加为CPU的数量，如果compaction太慢或太快，可以调整compaction_throughput_mb_per_sec。不过实际中，如果把compaction并行的线程数占满了CPU，会有影响， 以8核CPU为例，最好设置为4-6个。 |
| --- | --- |

提高compaction流量，对于大的partition让compaction尽快完成。已完成

修改内存配置（堆内存，New大小，memtable大小）为官方建议的配置。未完成

修改compaction策略。待评估

**compaction_throughput_mb_per_sec**

插入速度越快，就应该更快地compact便于减少sstable的数量。

如果没有及时compact，sstable数量变多，查询分布在多个sstable会变慢。

默认值为16M. 建议的值是每秒写入量(MB/s)的16-32倍，这个值是针对整个集群而言。

目前的值是128M,对应的写入量大概是8M/s.

因为要求尽快地compact,所以应该提升compact的流量。

提高到200M: nodetool setcompactionthroughput 200

为什么是提高而不是减少？降低后本来应该快速被compaction完成的对象现在由于流量限制，compaction完成的慢了，对象存活时间越长。

Throttling compaction can even make it worse by forcing Cassandra to keep objects in memory longer than necessary, causing promotion which leads to memory compaction which is bound by memory bandwidth of the system.

该配置主要针对大的partitions(partition指的是partition key对应的记录)

**LeveledCompactionStrategy**

Row Fragmentation行碎片，相同行多个列分散在多个sstable文件中，增加读延迟，因为要读取多个文件

相同partition key的数据写入包括两种情况：列被覆盖（比如最近的访问时间，则每次更新同一列），

添加新列（比如以sequenceId作为cluster key，则对于相同attribtue,都是添加新列，这种叫做wide rows）。

层级压缩策略：在compaction时花费更多的IO（代价）来确保一行记录分布在尽量少的sstable上（读延迟低）。

使用该配置，在90%的情况下读取一行记录只需要读取一个sstable文件。

Leveled compaction essentially treats more disk IO for a guarantee of how many SSTables a row may be spread. Below are the cases where Leveled Compaction can be a good option.

Low latency read is required

High read/write ratio

Rows are frequently updated. If size-tiered compaction is used, a row will spread across multiple SSTables.

Below are the cases where size-tiered compaction can be a good option.

Disk I/O is expensive

Write heavy workloads.

Rows are write once. If the rows are written once and then never updated, they will be contained in a single SSTable naturally. There’s no point to use the more I/O intensive leveled compaction.

| **Leveled** | **velocity** |
| --- | --- |
| Low latency read | +(20ms) |
| High read/write ratio | -(写多读少) |
| Rows frequently updated | +(attribute) |

| **Size-tiered** | **velocity** |
| --- | --- |
| Disk I/O is expensive | -(SSD) |
| Write heavy workloads | +(20倍于读) |
| Rows are write once | - |

Leveled has many small and fixed sized SSTables grouped into levels. Within a level, the SSTables do not have any overlap.

Consider SizeTiered Compaction when:

There is uncertainty of which compaction strategy is best; SizeTiered Compaction provides a good set of tradeoffs for acceptable performance under most workloads.

Mixed workload of reads, updates, and deletes; avoiding updates to existing rows helps avoid fragmentation.

Read latency is not important; the upper bound to fragmentation is the number of SSTables representing the column family.

Tombstones make up a substantial portion of at rest data, and are reaped via manual compaction.

There is sufficient free space to store 100% growth of the largest column family.

Consider Leveled Compaction when:

Read-heavy workload; many reads, some updates

Workloads which frequently update existing rows

Read latency is important; the upper bound to fragmentation is reduced as the number of SSTables in the column family grows (due to the leveled compaction process)

Tombstone space recovery is not important; tombstones will not be reaped until an SSTable moves to the next compaction tier (i.e. moves from L1 to L2).

There is not sufficient free space to store 100% growth of the largest column family. Leveled compaction requires 10 times available storage space of the largest SSTable in a column family.

Notice: Very wide rows are bad for compaction performance; wide rows fragmented across multiple SSTables (especially with partial updates) seem to result in lazy compaction.

### **commit log**

| 1234567891011121314151617181920212223242526272829 | INFO 00:43:34 G1 Young Generation GC in 665ms. G1 Eden Space: 746586112 -> 0; G1 Old Gen: 863097376 -> 1077936160;INFO 00:43:34 Finished reading /home/admin/cassandra/commitlog/CommitLog-4-1469253255114.logINFO 00:43:34 Replaying /home/admin/cassandra/commitlog/CommitLog-4-1469253255115.logINFO 00:43:34 Replaying /home/admin/cassandra/commitlog/CommitLog-4-1469253255115.log (CL version 4, messaging version 8)INFO 00:43:34 Finished reading /home/admin/cassandra/commitlog/CommitLog-4-1469253255115.logINFO 00:43:34 Replaying /home/admin/cassandra/commitlog/CommitLog-4-1469253255116.logINFO 00:43:34 Replaying /home/admin/cassandra/commitlog/CommitLog-4-1469253255116.log (CL version 4, messaging version 8)INFO 00:43:34 Finished reading /home/admin/cassandra/commitlog/CommitLog-4-1469253255116.logINFO 00:43:34 Enqueuing flush of velocity_app: 4533700 (0%) on-heap, 19619446 (1%) off-heapINFO 00:43:34 Enqueuing flush of velocity_partner: 7053660 (0%) on-heap, 30525922 (1%) off-heapINFO 00:43:34 Enqueuing flush of velocity_global: 7209692 (0%) on-heap, 31952864 (1%) off-heapINFO 00:43:34 Enqueuing flush of compaction_history: 348 (0%) on-heap, 337 (0%) off-heapINFO 00:43:34 Enqueuing flush of peers: 8100 (0%) on-heap, 12961 (0%) off-heapINFO 00:43:34 Enqueuing flush of sstable_activity: 1672004 (0%) on-heap, 1090645 (0%) off-heapINFO 00:43:34 Writing Memtable-velocity_app@267505537(17.287MiB serialized bytes, 80241 ops, 0%/1% of on/off-heap limit)INFO 00:43:34 Writing Memtable-velocity_partner@1289868454(27.246MiB serialized bytes, 151660 ops, 0%/1% of on/off-heap limit)INFO 00:43:35 Writing Memtable-velocity_global@1372197833(28.741MiB serialized bytes, 184395 ops, 0%/1% of on/off-heap limit)INFO 00:43:35 Completed flushing /home/admin/cassandra/data/forseti/velocity_app/forseti-velocity_app-tmp-ka-1638169-Data.db (6.254MiB) for commitlog position ReplayPosition(segmentId=1470098454897, position=1076701)INFO 00:43:35 Completed flushing /home/admin/cassandra/data/forseti/velocity_partner/forseti-velocity_partner-tmp-ka-696949-Data.db (9.154MiB) for commitlog position ReplayPosition(segmentId=1470098454897, position=1076701)INFO 00:43:36 Completed flushing /home/admin/cassandra/data/forseti/velocity_global/forseti-velocity_global-tmp-ka-632911-Data.db (9.456MiB) for commitlog position ReplayPosition(segmentId=1470098454897, position=1076701)INFO 00:43:36 Writing Memtable-peers@200973128(10.031KiB serialized bytes, 284 ops, 0%/0% of on/off-heap limit)INFO 00:43:36 Writing Memtable-sstable_activity@1268561550(677.721KiB serialized bytes, 23511 ops, 0%/0% of on/off-heap limit)INFO 00:43:36 Completed flushing /home/admin/cassandra/data/system/peers/system-peers-tmp-ka-139-Data.db (0.000KiB) for commitlog position ReplayPosition(segmentId=1470098454897, position=1076903)INFO 00:43:36 Completed flushing /home/admin/cassandra/data/system/sstable_activity/system-sstable_activity-tmp-ka-11818-Data.db (316.776KiB) for commitlog position ReplayPosition(segmentId=1470098454897, position=1076903)INFO 00:43:36 Enqueuing flush of compactions_in_progress: 3008 (0%) on-heap, 3018 (0%) off-heapINFO 00:43:36 Writing Memtable-compactions_in_progress@1320271332(2.269KiB serialized bytes, 99 ops, 0%/0% of on/off-heap limit)INFO 00:43:36 Completed flushing /home/admin/cassandra/data/system/compactions_in_progress/system-compactions_in_progress-tmp-ka-1248876-Data.db (0.000KiB) for commitlog position ReplayPosition(segmentId=1470098454897, position=1125106) |
| --- | --- |

CommitLog -> MemTable -> flush

选择一个tmp data.db查看：

| 12 | [admin@cass048171 ~]$ ll /home/admin/cassandra/data/forseti/velocity_app/forseti-velocity_app-ka-1638169-Data.db -h-rw-rw-r–. 1 admin admin 6.3M 8月 2 08:43 /home/admin/cassandra/data/forseti/velocity_app/forseti-velocity_app-ka-1638169-Data.db |
| --- | --- |

### **JavaDriver配置**

连接池配置：[http://zhaoyanblog.com/archives/547.html](http://zhaoyanblog.com/archives/547.html)

连接选项： [http://docs.datastax.com/en/latest-java-driver/common/drivers/reference/connectionsOptions_c.html](http://docs.datastax.com/en/latest-java-driver/common/drivers/reference/connectionsOptions_c.html)

| 123 | WARN [SharedPool-Worker-1] 2016-07-07 09:31:20,371 BatchStatement.java:272 -Batch of prepared statements for [forseti_fp.ios_device_info] is of size 17287,exceeding specified threshold of 5120 by 12167. |
| --- | --- |

### **Partitioner**

| 123456 | Opening sstables and calculating sections to streamERROR 06:31:40 Cannot open md5_id_20160705/md5_id_2/md5s/md5_id_2/md5s-md5_id_2-ka-7978;partitioner org.apache.cassandra.dht.ByteOrderedPartitionerdoes not match system partitioner org.apache.cassandra.dht.Murmur3Partitioner.Note that the default partitioner starting with Cassandra 1.2 is Murmur3Partitioner,so you will need to edit that to match your old partitioner if upgrading. |
| --- | --- |

Partitioner是在cassandra.yaml中配置的！不是在表级别！

| 1 | partitioner: org.apache.cassandra.dht.Murmur3Partitioner |
| --- | --- |

### **Internal**

### **Partitioner**

[http://www.geroba.com/cassandra/cassandra-token-calculator/](http://www.geroba.com/cassandra/cassandra-token-calculator/)

8个节点，Murmur3Partitioner

| 12345678 | -9223372036854775808n-6917529027641081856n-4611686018427387904n-2305843009213693952n0n2305843009213693952n4611686018427387904n6917529027641081856 |
| --- | --- |

RandomPartitioner

| 12345678 | 0n21267647932558653966460912964485513216n42535295865117307932921825928971026432n63802943797675961899382738893456539648n85070591730234615865843651857942052864n106338239662793269832304564822427566080n127605887595351923798765477786913079296n148873535527910577765226390751398592512 |
| --- | --- |

### **Memory**

| 123456789101112131415161718192021222324252627282930313233343536373839404142434445 | [admin@cass047202 data]$ nodetool cfstats forseti.ip_account |
| --- | --- |

OffHeap总共占用6G。md5_id_x每张表占用400M，16张表=16*400=6400=6G.

### **Ref**

[https://docs.datastax.com/en/cassandra/2.0/cassandra/dml/dml_write_path_c.html](https://docs.datastax.com/en/cassandra/2.0/cassandra/dml/dml_write_path_c.html)

[https://docs.datastax.com/en/cassandra/2.0/cassandra/operations/ops_tune_jvm_c.html](https://docs.datastax.com/en/cassandra/2.0/cassandra/operations/ops_tune_jvm_c.html)

[https://tobert.github.io/pages/als-cassandra-21-tuning-guide.html](https://tobert.github.io/pages/als-cassandra-21-tuning-guide.html)

[http://www.datastax.com/dev/blog/when-to-use-leveled-compaction](http://www.datastax.com/dev/blog/when-to-use-leveled-compaction)

[http://www.datastax.com/dev/blog/leveled-compaction-in-apache-cassandra](http://www.datastax.com/dev/blog/leveled-compaction-in-apache-cassandra)

[http://www.roman10.net/2012/08/24/apache-cassandra-how-compaction-works/](http://www.roman10.net/2012/08/24/apache-cassandra-how-compaction-works/)

[http://engblog.polyvore.com/2015/03/cassandra-compaction-and-tombstone.html](http://engblog.polyvore.com/2015/03/cassandra-compaction-and-tombstone.html)