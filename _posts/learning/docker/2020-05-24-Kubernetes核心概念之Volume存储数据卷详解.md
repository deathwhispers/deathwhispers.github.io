---
layout: post
title: Kubernetes核心概念之Volume存储数据卷详解
slug: kubernetes-volume
date: 2020-05-24
type:
  - note
tags:
  - Kubernetes
categories:
  - Kubernetes
author: deathwhispers
created: 2020-05-24 11:48
updated: 2020-05-24 11:48
---


# Kubernetes核心概念之Volume存储数据卷详解

在Docker中就有数据卷的概念，当容器删除时，数据也一起会被删除，想要持久化使用数据，需要把主机上的目录挂载到Docker中去，在K8S中，数据卷是通过Pod实现持久化的，如果Pod删除，数据卷也会一起删除，k8s的数据卷是docker数据卷的扩展，K8S适配各种存储系统，包括本地存储EmptyDir,HostPath,网络存储NFS,GlusterFS,PV/PVC等，下面就详细介绍下K8S的存储如何实现。

一.本地存储

1，EmptyDir

①编辑EmptyDir配置文件

vim emptydir.yaml

```yaml
apiVersion: v1kind: Pod#类型是Podmetadata:labels:name: redisrole: master#定义为主redisname: redis-masterspec:containers:- name: masterimage: redis:latestenv:#定义环境变量- name: MASTERvalue:"true"ports:#容器内端口- containerPort: 6379volumeMounts:#容器内挂载点- mountPath: /dataname: redis-data#必须有名称volumes:- name: redis-data#跟上面的名称对应emptyDir:{}#宿主机挂载点
```

②创建Pod

```plain text
kubectl create -f emptydir.yaml
```