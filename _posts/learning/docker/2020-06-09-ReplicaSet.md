---
layout: post
title: ReplicaSet
author: deathwhispers
date: 2020-06-09
slug: replicaset
categories:
- Docker
tags:
- Docker
- Kubernetes
type: note
created: 2020-06-09 11:48
updated: 2020-06-09 11:48
---

# ReplicaSet

# **Kubernetes Replica Sets**

ReplicaSet（RS）是Replication Controller（RC）的升级版本。ReplicaSet 和 [Replication Controller](http://docs.kubernetes.org.cn/437.html)之间的唯一区别是对选择器的支持。ReplicaSet支持[labels user guide](http://docs.kubernetes.org.cn/247.html#Labels)中描述的set-based选择器要求， 而Replication Controller仅支持**equality-based**的选择器要求。

## **如何使用ReplicaSet**

大多数[kubectl](http://docs.kubernetes.org.cn/61.html) 支持Replication Controller 命令的也支持ReplicaSets。[rolling-update](https://kubernetes.io/docs/user-guide/kubectl/v1.7/#rolling-update)命令除外，**如果要使用rolling-update，请使用Deployments来实现**。

虽然ReplicaSets可以独立使用，但它主要被 [Deployments](http://docs.kubernetes.org.cn/317.html)用作pod 机制的创建、删除和更新。当使用Deployment时，你不必担心创建pod的ReplicaSets，因为可以通过Deployment实现管理ReplicaSets。

## **何时使用ReplicaSet**

ReplicaSet能确保运行指定数量的pod。然而，Deployment 是一个更高层次的概念，它能管理ReplicaSets，并提供对pod的更新等功能。因此，**我们建议你使用Deployment来管理ReplicaSets**，除非你需要自定义更新编排。

这意味着你可能永远不需要操作ReplicaSet对象，而是使用Deployment替代管理 。

## **示例**

[frontend.yaml](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/concepts/workloads/controllers/frontend.yaml)

```yaml
apiVersion: extensions/v1beta1
kind: ReplicaSet
metadata:
  name: frontend
  # these labels can be applied automatically
  # from the labels in the pod template if not set
  # labels:
    # app: guestbook
    # tier: frontend
spec:
  # this replicas value is default
  # modify it according to your case
  replicas: 3
  # selector can be applied automatically
  # from the labels in the pod template if not set,
  # but we are specifying the selector here to
  # demonstrate its usage.
  selector:
    matchLabels:
      tier: frontend
    matchExpressions:
      - {key: tier, operator: In, values: [frontend]}
  template:
    metadata:
      labels:
        app: guestbook
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        env:
        - name: GET_HOSTS_FROM
          value: dns
          # If your cluster config does not include a dns service, then to
          # instead access environment variables to find service host
          # info, comment out the 'value: dns' line above, and uncomment the
          # line below.
          # value: env
        ports:
        - containerPort: 80
```

将此配置保存到（frontend.yaml）并提交到Kubernetes集群时，将创建定义的ReplicaSet及其管理的pod。

```shell
$ kubectl create -f frontend.yaml
replicaset "frontend" created
```

```text
$ kubectl describe rs/frontend

Name:          frontend
Namespace:     default
Image(s):      gcr.io/google_samples/gb-frontend:v3
Selector:      tier=frontend,tier in (frontend)
Labels:        app=guestbook,tier=frontend
Replicas:      3 current / 3 desired
Pods Status:   3 Running / 0 Waiting / 0 Succeeded / 0 Failed
No volumes.
Events:
FirstSeen    LastSeen    Count    From                SubobjectPath    Type        Reason            Message
---------    --------    -----    ----                -------------    --------    ------            -------
1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-qhloh
1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-dnjpy
1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-9si5l
$ kubectl get pods
NAME             READY     STATUS    RESTARTS   AGE
frontend-9si5l   1/1       Running   0          1m
frontend-dnjpy   1/1       Running   0          1m
frontend-qhloh   1/1       Running   0          1m
```

## **ReplicaSet as an Horizontal Pod Autoscaler target**

ReplicaSet也可以作为 [Horizontal Pod Autoscalers (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)的目标 。也就是说，一个ReplicaSet可以由一个HPA来自动伸缩。以下是针对我们在上一个示例中创建的ReplicaSet的HPA示例。

[hpa-rs.yaml](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/concepts/workloads/controllers/hpa-rs.yaml)

![Horizontal Pod Autoscaler 示意图](../../../assets/images/learning/docker/replicaset/b6d54e217130858448902546cff85028.svg)

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-scaler
spec:
  scaleTargetRef:
    kind: ReplicaSet
    name: frontend
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```
