---
layout: post
title: 对线面试官 AQS ReentrantLock
author: deathwhispers
date: 2022-11-14
slug: solo-interviewer-aqs-reentrantlock
categories:
- Interview
tags:
- Concurrency
- Java
- Network
type: note
created: 2024-07-26 11:48
updated: 2024-07-26 11:48
---

![AQS ReentrantLock面试漫画对话01](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/df387c7ecf1f031ef1c09d00a060c7d1.png)

![AQS ReentrantLock面试漫画对话02](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/a0ef31eaad85789a289e582cfed09a4d.png)

![AQS ReentrantLock面试漫画对话03](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/23af878e5d58bcaca47a1b1013f6d06b.png)

![AQS ReentrantLock面试漫画对话04](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/be277f169375d4a4794475c6a4cdd338.png)

![AQS ReentrantLock面试漫画对话05](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/514d30f5b403bc8e24a08e128e07419b.png)

![AQS ReentrantLock面试漫画对话06](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/ff2319a6fc3c01f1f8b5fc6bc64d2768.png)

![AQS ReentrantLock面试漫画对话07](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/942c968d5cf84bca9dd012d66cb8f7a7.png)

![AQS ReentrantLock面试漫画对话08](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/38b18ad93316579d042cf5ca7709202e.png)

![AQS ReentrantLock面试漫画对话09](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/c8117b03ff23b18e6387ed7829e1cc23.png)

![AQS ReentrantLock面试漫画对话10](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/b3e53d44422181ef9a5be5a6fd512b57.png)

![AQS ReentrantLock面试漫画对话11](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/27c38b4195eda5411c4af601d86e239f.png)

![AQS ReentrantLock面试漫画对话12](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/ea1a60b592f2f362bac9796e0a801376.png)

![AQS ReentrantLock面试漫画对话13](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/332d1cb08e745d18fd49aa601908f94d.png)

![AQS ReentrantLock面试漫画对话14](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/7a2f741eab521fc508f974416cf376d0.png)

![AQS ReentrantLock面试漫画对话15](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/31c9cce443b62181bd2942213886dc27.png)

![AQS ReentrantLock面试漫画对话16](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/646dc11f954847b2abd0da3f8e9eb6b9.png)

![AQS ReentrantLock面试漫画对话17](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/222fa0e691ed6e057f70b2a01c0ddbca.png)

![AQS ReentrantLock面试漫画对话18](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/fd91fc7e92777e92cd1083db0c803a62.png)

![AQS ReentrantLock面试漫画对话19](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/1d75bb449f5437c8a3d918cd3b23cd23.png)

![AQS ReentrantLock面试漫画对话20](/assets/images/learning/interview/solo/solo-interviewer-aqs-reentrantlock/f31d8bb9fa88b9f2d786ed6fd0a3908c.png)

文章以纯面试的角度去讲解，所以有很多的细节是未曾铺垫的。

单纯通过一篇文章来想要在面试中答出AQS、公平锁&&非公平锁以及ReentrantLock的加解锁🔐流程是很难的，强烈建议看完之后自己去**翻下源码**。

鉴于很多同学反馈没看懂【对线面试官】系列，基础相关的知识我确实写过文章讲解过啦，但有的同学就是不爱去翻。
