---
layout: post
title: Spring Boot 启动的时候初始化的线程池默认配置
slug: spring-boot-tomcat-thread-pool-default-config
type:
- note
date: 2018-10-05
week: 2018-W40
status: draft
tags:
- Spring
- SpringBoot
author: deathwhispers
created: 2018-10-05 09:57
updated: 2018-10-05 09:57
categories:
- Learning
- Spring
---

[参考文献：http://tomcat.apache.org/tomcat-8.0-doc/config/http.html#HTTP/1.1_and_HTTP/1.0_Support](http://tomcat.apache.org/tomcat-8.0-doc/config/http.html#HTTP/1.1_and_HTTP/1.0_Support)

整理一下springboot中的tomcat默认线程池配置

server:

port: xxxx

tomcat:

uri-encoding: UTF-8

max-threads: 1000 #最大并发数

max-connections: 20000 #接受和处理的最大连接数

min-SpareThreads: 20 #初始化时创建的线程数

acceptCount: 700 #可以放到处理队列中的请求数

maxThreads=1000 最大并发数

minSpareThreads=100 // 初始化时创建的线程数

maxSpareThreads=500 // 一旦创建的线程超过这个值，Tomcat就会关闭不再需要的socket线程。

acceptCount=700 // 指定当所有可以使用的处理请求的线程数都被使用时，可以放到处理队列中的请求数，超过这个数的请求将不予处理

maxThreads: 客户请求最大线程数

minSpareThreads: Tomcat初始化时创建的 socket 线程数

maxSpareThreads: Tomcat连接器的最大空闲 socket 线程数

enableLookups: 若设为true, 则支持域名解析，可把 ip 地址解析为主机名

redirectPort: 在需要基于安全通道的场合，把客户请求转发到基于SSL 的 redirectPort 端口

acceptAccount: 监听端口队列最大数，满了之后客户请求会被拒绝（不能小于maxSpareThreads ）

connectionTimeout: 连接超时时间

minProcessors 服务器创建时的最小处理线程数

maxProcessors 服务器同时最大处理线程数

URIEncoding URL统一编码

maxThreads：处理的最大并发请求数，默认值200

minSpareThreads：最小线程数始终保持运行，默认值10

maxConnections：在给定时间接受和处理的最大连接数，默认值10000
