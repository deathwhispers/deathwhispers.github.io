---
layout: post
title: Disruptor 术语说明
slug: disruptor-terminology
type:
  - note
date: 2021-09-16
week: 2025-W48
status: draft
tags:
  - 并发编程
  - Java并发系列
categories:
  - Java
author: deathwhispers
created: 2021-09-16 19:45
updated: 2021-09-16 19:45
---
# Disruptor

Disruptor 术语说明：

RingBuffer： 被看做Disruptor最主要的组件，然而从3.0开始RingBuffer 仅仅负责存储和更新在Disruptor中流通的数据。对一些特殊的使用场景能够被用户（使用其他数据结构）完全替代

> **Sequence：Disruptor 使用 Sequence 来表示一个特殊组件处理的序号，和 Disruptor 一样，每一个消费者（EventProcessor）都维持着一个Sequence。大部分的并发代码依赖这些Sequence 值得运转，因此Sequence 支持多种当前为 AtomicLong 类的特性**

> **Sequencer： 这是 Disruptor 真正的核心，实现了这个接口的两种生产者（单生产者和多生产者）均实现了所有的并发算法，为了在生产者和消费者之间进行准确快速的数据传递**

SequenceBarrier： 由 Sequencer 生成，并且包含了已经发布的 Sequence 的引用，这些 Sequencer 和一些独立的消费者的 Sequence。它包含了决定是否有供消费者来消费的Event的逻辑

WaitStrategy：决定一个消费者将如何等待生产者将Event 置入 Disruptor。

Event：从生产者到消费者过程中所处理的数据单元。Disruptor 中没有代码表示Event，因此它完全是由用户定义的

EventProcessor：主要时间循环，处理Disruptor 中的Event，并且拥有消费者的Sequence。它有一个实现类是BatchEventProcessor。包含了event loop有效的实现，并且将回调到一个EventHandler 接口的实现对象。

EventHandler：由用户实现并且代表了Disruptor 中的一个消费者的接口。

Producer：由用户实现，它调用 RingBuffer 来插入事件（Event），在Disrupter 中没有相应的实现代码，

WorkProcessor：确保每个Sequence 只被一个 processor消费，在同一个WorkPool 中的处理多个 WorkProcessor 不会消费同样的 Sequence

WorkerPool：一个WorkProcess 池，其中 WorkProcess 将消费 Sequence ，所以任务可以在实现WorkHandler 接口的 worker 之间移交

LifecycleAware：当BatchEventProcessor 启动和停止时，于实现这个接口用于接收通知

**理解RingBuffer**

场景使用：

可以直接使用RingBuffer，而不用Disruptor
