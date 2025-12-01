---
layout: post
title: db2安装手册
slug: db2-installation-manual
type:
  - note
date: 2018-03-17
tags:
  - db2
categories:
  - db2
author: deathwhispers
created: 2018-03-17 11:45
updated: 2018-03-17 22:17
---
# db2安装手册

linux下安装db2

**准备工作**

先检查应用用户/实力用户是否存在，目录是否正确，相关软件是否安装，如db2/cd/mqctm等，如果缺少必须软件，请联系系统部安装

**安装db2**

1.解压db2压缩包

tar -zxvf DB2_v11.1.2fp_linuxx64_server_t.tar.gz

2.安装db2

cd server_t

./db2prereqcheck>>installchk.log

./db2_install

- yes
- yes
- SERVER
- no

3.安装license

cd /opt/ibm/db2/v11.1/adm

./db2licm -a /home/xxx/xxxx/xxxx

**创建用户组和用户**

1.创建用户和组

```plain text
创建用户组   groupadd  用户组名

创建用户  useradd -s  /bin/bash -d 用户目录 -m 用户名 -g 主用户组名 -G 从用户组名 -e 用户期限日
```

创建实例（切换为root用户创建实例对象 ）

su -root

cd /opt/ibm/db2/vxx.x/instance –db2安装目录

./db2icrt -u db2inst1 db2inst1

- *

**

**创建数据库**

1.登陆实力用户修改相关参数

```plain text
    db2 get dbm cfg         --查看相关参数


    db2 set DB2COMM=TCPIP         --设置协议


    db2set DB2CODEPAGE=1208        --设置斌吗格式为UTF-8（GBK为1386）


    db2 update dbm cfg using SVCENAME 60000         --修改登陆端口号





    db2stop force


    db2start


    db2 create db xxxx  using  utf-8 territory cn;


    connect to xxxx
```

创建缓冲池