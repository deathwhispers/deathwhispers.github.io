---
layout: post
title: Replication Controller
author: deathwhispers
date: 2020-06-09
slug: replication-controller
categories:
- Docker
tags:
- Docker
- Kubernetes
type: note
created: 2020-06-09 11:48
updated: 2020-06-09 11:48
---

# Replication Controller

# **Kubernetes Replication Controller**

注意：建议使用[Deployment](http://docs.kubernetes.org.cn/317.html) 配置 [ReplicaSet](http://docs.kubernetes.org.cn/314.html) （简称RS）方法来控制副本数。

ReplicationController（简称RC）是确保用户定义的Pod副本数保持不变。

## **ReplicationController 工作原理**

在用户定义范围内，如果pod增多，则ReplicationController会终止额外的pod，如果减少，RC会创建新的pod，始终保持在定义范围。例如，RC会在Pod维护（例如内核升级）后在节点上重新创建新Pod。

**注：**

- ReplicationController会替换由于某些原因而被删除或终止的pod，例如在节点故障或中断节点维护（例如内核升级）的情况下。因此，即使应用只需要一个pod，我们也建议使用ReplicationController。
- RC跨多个Node节点监视多个pod。

### **示例：**

replication.yaml

```yaml
apiVersion: v1kind: ReplicationControllermetadata:  name: nginxspec:  replicas: 3  selector:    app: nginx  template:    metadata:      name: nginx      labels:        app: nginx    spec:      containers:      - name: nginx        image: nginx        ports:        - containerPort: 80
```

下载示例文件然后运行：

```plain text
$ kubectl create -f ./replication.yaml
replicationcontroller "nginx" created
```

检查ReplicationController状态：

```plain text
$ kubectl describe replicationcontrollers/nginx
Name:        nginx
Namespace:   default
Image(s):    nginx
Selector:    app=nginx
Labels:      app=nginx
Replicas:    3 current / 3 desired
Pods Status: 0 Running / 3 Waiting / 0 Succeeded / 0 Failed
Events:
  FirstSeen       LastSeen     Count    From                        SubobjectPath    Type      Reason              Message
  ---------       --------     -----    ----                        -------------    ----      ------              -------
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-qrm3m
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-3ntk0
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-4ok8v
```

创建了三个pod

```plain text
Pods Status:    3 Running / 0 Waiting / 0 Succeeded / 0 Failed
```

列出属于ReplicationController的所有pod：

```plain text
$ pods=$(kubectl get pods --selector=app=nginx --output=jsonpath={.items..metadata.name})
echo $pods
nginx-3ntk0 nginx-4ok8v nginx-qrm3m
```

### **删除ReplicationController及其Pods**

使用kubectl delete命令删除ReplicationController及其所有pod。

当使用REST API或客户端库时，需要明确地执行这些步骤（将副本缩放为0，等待pod删除，然后删除ReplicationController）。

### **只删除 ReplicationController**

在删除ReplicationController时，可以不影响任何pod。

使用kubectl，为kubectl delete指定- cascade = false选项。

使用REST API或go客户端库时，只需删除ReplicationController对象即可。

原始文件被删除后，你可以创建一个新的ReplicationController来替换它。只要旧的和新.spec.selector 相匹配，那么新的将会采用旧的Pod。

### **ReplicationController隔离pod**

可以通过更改标签来从ReplicationController的目标集中删除Pod。

## **RC常用方式**

- Rescheduling（重新规划）
- 扩展
- 滚动更新
- 多版本跟踪
- 使用ReplicationControllers与关联的Services

## **API对象**

Replication controller是Kubernetes REST API中的顶级资源。有关API对象更多详细信息，请参见：[ReplicationController API对象](https://kubernetes.io/docs/api-reference/v1.7/#replicationcontroller-v1-core)。

## **RC 替代方法**

### **ReplicaSet**

[ReplicaSet](http://docs.kubernetes.org.cn/314.html)是支持新的set-based选择器要求的下一代ReplicationController 。它主要用作[Deployment](http://docs.kubernetes.org.cn/317.html)协调pod创建、删除和更新。请注意，除非需要自定义更新编排或根本不需要更新，否则建议使用Deployment而不是直接使用ReplicaSets。

### **Deployment（推荐）**

[Deployment](http://docs.kubernetes.org.cn/317.html)是一个高级的API对象，以类似的方式更新其底层的副本集和它们的Pods kubectl rolling-update。如果您希望使用这种滚动更新功能，建议您进行部署，因为kubectl rolling-update它们是声明式的，服务器端的，并具有其他功能。

### **Bare Pods**

与用户直接创建pod的情况不同，ReplicationController会替换由于某些原因而被删除或终止的pod，例如在节点故障或中断节点维护（例如内核升级）的情况下。因此，即使应用只需要一个pod，我们也建议使用ReplicationController。

其他：[Job](https://kubernetes.io/docs/concepts/jobs/run-to-completion-finite-workloads/)、[DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
