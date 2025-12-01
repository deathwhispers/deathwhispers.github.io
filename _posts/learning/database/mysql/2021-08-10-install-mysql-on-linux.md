---
layout: post
title: Linux下安装MySQL
slug: install-mysql-on-linux
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
## **yum安装**

```bash
yum -y list mysql*
```

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037425664-8e52a506-6aee-4fdf-b653-be339f62048b.png)

```bash
yum install mariadb-devel.x86_64
```

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037425748-8848fbe1-7597-4522-972d-bacfca13b517.png)

**若安装错误，可使用yum命令讲mysql（mariadb卸载）**

```bash
yum remove mysql mysql-server mysql-libs mysql-server
```

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037425832-a26d80a7-231a-4642-93cb-088cb80bfe00.png)

## **方法二 下载tar包进行安装**

### **1、找到对应的下载链接**

```plain text
官网下载地址： [https://dev.mysql.com/downloads/mysql/5.6.html#downloads](https://dev.mysql.com/downloads/mysql/5.6.html#downloads)
```

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037425920-067cce0b-2cf0-46cb-b1dd-7c13112c04d4.png)

## **2、使用wget命令将压缩包下载到服务器**

选择5.7的最后一个版本

```bash
wget https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
```

## **3、解压安装包**

```bash
tar –zxvf mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
```

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037426009-8f8050cd-9d95-47be-b1ba-ddfa97fb9d7a.png)

## **4、将解压后的文件夹复制到安装目**

```plain text
我们选择安装到/usr/local/mysql 下
```

## **5、添加mysql用户组和用户并修改对应权限**

```bash
groupadd mysql
useradd -g mysql mysql
```

**更改/usr/local/mysql 文件夹所有者属性和对应权限**

```bash
chown -R mysql:mysql /usr/local/mysql/
chown -R mysql /usr/local/mysql
chmod -R 755 /usr/local/mysql
```

## **6、安装libaio依赖包**

- *

**

**直接使用yum命令来安装**

```bash
yum install libaio
```

### **7、初始化安装**

在当前目录（/usr/local/mysql）创建一个data目录 用于存放数据库数据文件（可自定义）

mkdir data

注意修改data目录权限

**chown -R mysql:mysql /usr/local/mysql/**data

**chown -R mysql /usr/local/mysql/data**

**chmod -R 755 /usr/local/mysql/data**

**bin/mysqld –user=mysql –basedir=/usr/local/mysql –datadir=/usr/local/mysql/data –initialize**

***mysqld ****在数据库软件目录的bin下面；我当前在/usr/local/mysql根目录所以执行mysqld时前面要加上bin目录。*

_**basedir**__:数据库软件根目录，即解压后复制到的地方_

_**datadir**__:数据库数据存储目录，这个就是前面mkdir data前面建立的_

*记住最后几个字符生成的临时数据库登录密码记住是冒号后面的都是密码（如下图）*

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037426087-aab8c93e-653d-49ce-ae41-c56ae45bae61.png)

*如果出现:****initialize specified but the data directory has files in it. Aborting****错误，请将data目录下的所有文件都删除，再进行初始化安装命令。*

## **开启mysql服务**

./support-files/mysql.server start （sevice mysql start）

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698037426165-5b9d2e7d-05fe-466a-9a54-69bc48312afc.png)

**配置mysql的环境变量**

```bash
echo‘PATH=/usr/local/mysql/bin:$PATH’>>/etc/profile
```

```bash
source/etc/profile
```

# 修改密码alteruser‘root’@‘localhost’ identified by ‘root’;

# 刷新权限flushprivileges;

退出后，重新登录就可以使用自己修改好的密码了。

**设置开机自启**

```bash
# 先将/usr/local/mysql/mysql/support-files/ 文件夹下的mysql.server文件复制到 /etc/rc.d/init.d/ 目录下mysqld
cp /usr/local/mysql/mysql/support-files/mysql.server /etc/rc.d/init.d/mysqld
# 赋予可执行权限
chmod +x /etc/rc.d/init.d/mysqld
# 添加为服务
chkconfig --add mysqld
# 查看服务列表
chkconfig --list
```

设置mysql远程连接

```bash
# 修改权限 grant all privileges on *.* to 'root'@'%' identified by 'root' with grant option;
# 刷新 flush privileges;
```

以下为Linux防火墙的一些操作，这里我们就添加放行端口即可放行端口命令：firewall-cmd –zone=public –add-port=3306/tcp –permanen。添加后，记得重启防火墙，重启后就可以进行远程访问mysql了。

```bash
# 查看防火墙状态
firewall-cmd --state
# 开启防火墙
systemctl start firewalld.service
# 关闭防火墙
systemctl stop firewalld.service
# 重启防火墙
systemctl restart firewalld.service
# 添加防火墙放行端口
firewall-cmd --zone=public --add-port=3306/tcp --permanen
# 关闭防火墙放行端口
firewall-cmd --zone=public --add-port=80/tcp --permanen
# 查看防火墙放行端口
firewall-cmd --zone=public --list-ports
```

**8、修改配置文件**

修改datadir、basedir等对应的目录

配置文件里所有配置的文件位置必须真实存在，不存在的需要手动创建；并且赋予对应的文件权限

```bash
vim /etc/my.cnf
```
