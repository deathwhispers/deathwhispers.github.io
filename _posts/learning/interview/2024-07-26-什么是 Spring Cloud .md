---
layout: post
title: 什么是 Spring Cloud ？
slug: interview-what-is-spring-cloud
date: 2024-07-26
type:
  - note
tags:
  - Spring Cloud
categories:
  - interview
author: deathwhispers
created: 2024-07-26 11:48
updated: 2024-07-26 11:48
---

---
# 什么是 Spring Cloud ？

# 什么是 Spring Cloud ？

- <u>什么是 Spring Cloud ？</u>
    - <u>Spring Cloud 核心功能是什么？</u>
    - <u>Spring Cloud 有哪些组件？</u>
    - <u>Spring Cloud 和 Spring Boot 的区别和关系？</u>
    - <u>Spring Cloud 和 Dubbo 的区别？</u>

Spring Cloud 是构建在 Spring Boot 基础之上，用于快速构建分布式系统的通用模式的工具集。或者说，换成大家更为熟知的，用于构建微服务的技术栈。

## Spring Cloud 核心功能是什么？

毫无疑问，Spring Cloud 可以说是目前微服务架构的最好的选择，涵盖了基本我们需要的所有组件，所以也被称为全家桶。Spring Cloud 主要提供了如下核心的功能：

- Distributed/versioned configuration 分布式/版本化的配置管理
- Service registration and discovery 服务注册与服务发现
- Routing 路由
- Service-to-service calls 端到端的调用
- Load balancing 负载均衡
- Circuit Breakers 断路器
- Global locks 全局锁
- Leadership election and cluster state 选举与集群状态管理
- Distributed messaging 分布式消息

## Spring Cloud 有哪些组件？

Spring Cloud的 组件相当繁杂，拥有诸多子项目。如下脑图所示：

![](/assets/images/learning/interview/interview-what-is-spring-cloud/34216b7c4395db15b96eec623b8dc989.png)

Spring Cloud的 组件

我们最为熟知的，可能就是 Spring Cloud Netflix ，它是 Netflix 公司基于它们自己的 Eureka、Hystrix、Zuul、Ribbon 等组件，构建的一个 Spring Cloud 实现技术栈。

当然，可能关心 Spring Cloud 体系的胖友，已经知道 Spring Cloud Netflix 要进入维护模式，可能会略感担心。实际上，目前已经开始有新的基于 Spring Cloud 实现，可以作为新的选择。如下表格：

《Spring Cloud Netflix 项目进入维护模式》 ，感兴趣的胖友，可以看看新闻。

|   | Netflix | 阿里 | 其它 |
| --- | --- | --- | --- |
| 注册中心 | Eureka | Nacos | Zookeeper、Consul、Etcd |
| 熔断器 | Hystrix | Sentinel | Resilience4j |
| 网关 | Zuul1 | 暂无 | Spring Cloud Gateway |
| 负载均衡 | Ribbon | Dubbo(未来) | spring-cloud-loadbalancer |

其它组件，例如配置中心、链路追踪、服务引用等等，都有相应其它的实现。妥妥的~

## Spring Cloud 和 Spring Boot 的区别和关系？

1. Spring Boot 专注于快速方便的开发单个个体微服务。
2. Spring Cloud 是关注全局的微服务协调整理治理框架以及一整套的落地解决方案，它将 Spring Boot 开发的一个个单体微服务整合并管理起来，为各个微服务之间提供：配置管理，服务发现，断路器，路由，微代理，事件总线等的集成服务。
3. Spring Boot 可以离开 Spring Cloud 独立使用，但是 Spring Cloud 离不开 Spring Boot ，属于依赖的关系。

**总结**：

- Spring Boot ，专注于快速，方便的开发单个微服务个体。
- Spring Cloud ，关注全局的服务治理框架。

## Spring Cloud 和 Dubbo 的区别？

参见 [《精尽 Dubbo 面试题》](http://svip.iocoder.cn/Dubbo/Interview) 文章的 [「Spring Cloud 与 Dubbo 怎么选择？」](http://svip.iocoder.cn/Spring-Cloud/Interview/#) 问题的解答。

%23%20%E4%BB%80%E4%B9%88%E6%98%AF%20Spring%20Cloud%20%EF%BC%9F%0A%5BTOC%5D%0A%0ASpring%20Cloud%20%E6%98%AF%E6%9E%84%E5%BB%BA%E5%9C%A8%20Spring%20Boot%20%E5%9F%BA%E7%A1%80%E4%B9%8B%E4%B8%8A%EF%BC%8C%E7%94%A8%E4%BA%8E%E5%BF%AB%E9%80%9F%E6%9E%84%E5%BB%BA%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F%E7%9A%84%E9%80%9A%E7%94%A8%E6%A8%A1%E5%BC%8F%E7%9A%84%E5%B7%A5%E5%85%B7%E9%9B%86%E3%80%82%E6%88%96%E8%80%85%E8%AF%B4%EF%BC%8C%E6%8D%A2%E6%88%90%E5%A4%A7%E5%AE%B6%E6%9B%B4%E4%B8%BA%E7%86%9F%E7%9F%A5%E7%9A%84%EF%BC%8C%E7%94%A8%E4%BA%8E%E6%9E%84%E5%BB%BA%E5%BE%AE%E6%9C%8D%E5%8A%A1%E7%9A%84%E6%8A%80%E6%9C%AF%E6%A0%88%E3%80%82%0A%0A%23%23%20Spring%20Cloud%20%E6%A0%B8%E5%BF%83%E5%8A%9F%E8%83%BD%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F%0A%E6%AF%AB%E6%97%A0%E7%96%91%E9%97%AE%EF%BC%8CSpring%20Cloud%20%E5%8F%AF%E4%BB%A5%E8%AF%B4%E6%98%AF%E7%9B%AE%E5%89%8D%E5%BE%AE%E6%9C%8D%E5%8A%A1%E6%9E%B6%E6%9E%84%E7%9A%84%E6%9C%80%E5%A5%BD%E7%9A%84%E9%80%89%E6%8B%A9%EF%BC%8C%E6%B6%B5%E7%9B%96%E4%BA%86%E5%9F%BA%E6%9C%AC%E6%88%91%E4%BB%AC%E9%9C%80%E8%A6%81%E7%9A%84%E6%89%80%E6%9C%89%E7%BB%84%E4%BB%B6%EF%BC%8C%E6%89%80%E4%BB%A5%E4%B9%9F%E8%A2%AB%E7%A7%B0%E4%B8%BA%E5%85%A8%E5%AE%B6%E6%A1%B6%E3%80%82Spring%20Cloud%20%E4%B8%BB%E8%A6%81%E6%8F%90%E4%BE%9B%E4%BA%86%E5%A6%82%E4%B8%8B%E6%A0%B8%E5%BF%83%E7%9A%84%E5%8A%9F%E8%83%BD%EF%BC%9A%0A%0A*%20Distributed%2Fversioned%20configuration%20%E5%88%86%E5%B8%83%E5%BC%8F%2F%E7%89%88%E6%9C%AC%E5%8C%96%E7%9A%84%E9%85%8D%E7%BD%AE%E7%AE%A1%E7%90%86%0A*%20Service%20registration%20and%20discovery%20%E6%9C%8D%E5%8A%A1%E6%B3%A8%E5%86%8C%E4%B8%8E%E6%9C%8D%E5%8A%A1%E5%8F%91%E7%8E%B0%0A*%20Routing%20%E8%B7%AF%E7%94%B1%0A*%20Service-to-service%20calls%20%E7%AB%AF%E5%88%B0%E7%AB%AF%E7%9A%84%E8%B0%83%E7%94%A8%0A*%20Load%20balancing%20%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%0A*%20Circuit%20Breakers%20%E6%96%AD%E8%B7%AF%E5%99%A8%0A*%20Global%20locks%20%E5%85%A8%E5%B1%80%E9%94%81%0A*%20Leadership%20election%20and%20cluster%20state%20%E9%80%89%E4%B8%BE%E4%B8%8E%E9%9B%86%E7%BE%A4%E7%8A%B6%E6%80%81%E7%AE%A1%E7%90%86%0A*%20Distributed%20messaging%20%E5%88%86%E5%B8%83%E5%BC%8F%E6%B6%88%E6%81%AF%0A%0A%23%23%20Spring%20Cloud%20%E6%9C%89%E5%93%AA%E4%BA%9B%E7%BB%84%E4%BB%B6%EF%BC%9F%0ASpring%20Cloud%E7%9A%84%20%E7%BB%84%E4%BB%B6%E7%9B%B8%E5%BD%93%E7%B9%81%E6%9D%82%EF%BC%8C%E6%8B%A5%E6%9C%89%E8%AF%B8%E5%A4%9A%E5%AD%90%E9%A1%B9%E7%9B%AE%E3%80%82%E5%A6%82%E4%B8%8B%E8%84%91%E5%9B%BE%E6%89%80%E7%A4%BA%EF%BC%9A%0A!%5B34216b7c4395db15b96eec623b8dc989.png%5D(en-resource%3A%2F%2Fdatabase%2F5578%3A1)%0A%0ASpring%20Cloud%E7%9A%84%20%E7%BB%84%E4%BB%B6%0A%0A%E6%88%91%E4%BB%AC%E6%9C%80%E4%B8%BA%E7%86%9F%E7%9F%A5%E7%9A%84%EF%BC%8C%E5%8F%AF%E8%83%BD%E5%B0%B1%E6%98%AF%20Spring%20Cloud%20Netflix%20%EF%BC%8C%E5%AE%83%E6%98%AF%20Netflix%20%E5%85%AC%E5%8F%B8%E5%9F%BA%E4%BA%8E%E5%AE%83%E4%BB%AC%E8%87%AA%E5%B7%B1%E7%9A%84%20Eureka%E3%80%81Hystrix%E3%80%81Zuul%E3%80%81Ribbon%20%E7%AD%89%E7%BB%84%E4%BB%B6%EF%BC%8C%E6%9E%84%E5%BB%BA%E7%9A%84%E4%B8%80%E4%B8%AA%20Spring%20Cloud%20%E5%AE%9E%E7%8E%B0%E6%8A%80%E6%9C%AF%E6%A0%88%E3%80%82%0A%0A%E5%BD%93%E7%84%B6%EF%BC%8C%E5%8F%AF%E8%83%BD%E5%85%B3%E5%BF%83%20Spring%20Cloud%20%E4%BD%93%E7%B3%BB%E7%9A%84%E8%83%96%E5%8F%8B%EF%BC%8C%E5%B7%B2%E7%BB%8F%E7%9F%A5%E9%81%93%20Spring%20Cloud%20Netflix%20%E8%A6%81%E8%BF%9B%E5%85%A5%E7%BB%B4%E6%8A%A4%E6%A8%A1%E5%BC%8F%EF%BC%8C%E5%8F%AF%E8%83%BD%E4%BC%9A%E7%95%A5%E6%84%9F%E6%8B%85%E5%BF%83%E3%80%82%E5%AE%9E%E9%99%85%E4%B8%8A%EF%BC%8C%E7%9B%AE%E5%89%8D%E5%B7%B2%E7%BB%8F%E5%BC%80%E5%A7%8B%E6%9C%89%E6%96%B0%E7%9A%84%E5%9F%BA%E4%BA%8E%20Spring%20Cloud%20%E5%AE%9E%E7%8E%B0%EF%BC%8C%E5%8F%AF%E4%BB%A5%E4%BD%9C%E4%B8%BA%E6%96%B0%E7%9A%84%E9%80%89%E6%8B%A9%E3%80%82%E5%A6%82%E4%B8%8B%E8%A1%A8%E6%A0%BC%EF%BC%9A%0A%0A%3E%20%E3%80%8ASpring%20Cloud%20Netflix%20%E9%A1%B9%E7%9B%AE%E8%BF%9B%E5%85%A5%E7%BB%B4%E6%8A%A4%E6%A8%A1%E5%BC%8F%E3%80%8B%20%EF%BC%8C%E6%84%9F%E5%85%B4%E8%B6%A3%E7%9A%84%E8%83%96%E5%8F%8B%EF%BC%8C%E5%8F%AF%E4%BB%A5%E7%9C%8B%E7%9C%8B%E6%96%B0%E9%97%BB%E3%80%82%0A%0A%0A%7C%20%20%7C%20Netflix%20%7C%20%E9%98%BF%E9%87%8C%20%7C%20%E5%85%B6%E5%AE%83%20%7C%0A%7C%20—%20%7C%20—%20%7C%20—%20%7C%20—%20%7C%0A%7C%20%E6%B3%A8%E5%86%8C%E4%B8%AD%E5%BF%83%20%7C%20Eureka%20%7C%20Nacos%20%7C%20Zookeeper%E3%80%81Consul%E3%80%81Etcd%20%7C%0A%7C%20%E7%86%94%E6%96%AD%E5%99%A8%20%7C%20Hystrix%20%7C%20Sentinel%20%7C%20Resilience4j%20%7C%0A%7C%20%E7%BD%91%E5%85%B3%20%7C%20Zuul1%20%7C%20%E6%9A%82%E6%97%A0%20%7C%20Spring%20Cloud%20Gateway%20%7C%0A%7C%20%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%20%7C%20Ribbon%20%7C%20Dubbo(%E6%9C%AA%E6%9D%A5)%20%7C%20spring-cloud-loadbalancer%20%7C%0A%0A%0A%E5%85%B6%E5%AE%83%E7%BB%84%E4%BB%B6%EF%BC%8C%E4%BE%8B%E5%A6%82%E9%85%8D%E7%BD%AE%E4%B8%AD%E5%BF%83%E3%80%81%E9%93%BE%E8%B7%AF%E8%BF%BD%E8%B8%AA%E3%80%81%E6%9C%8D%E5%8A%A1%E5%BC%95%E7%94%A8%E7%AD%89%E7%AD%89%EF%BC%8C%E9%83%BD%E6%9C%89%E7%9B%B8%E5%BA%94%E5%85%B6%E5%AE%83%E7%9A%84%E5%AE%9E%E7%8E%B0%E3%80%82%E5%A6%A5%E5%A6%A5%E7%9A%84~%0A%0A%23%23%20Spring%20Cloud%20%E5%92%8C%20Spring%20Boot%20%E7%9A%84%E5%8C%BA%E5%88%AB%E5%92%8C%E5%85%B3%E7%B3%BB%EF%BC%9F%0A%0A1.%20Spring%20Boot%20%E4%B8%93%E6%B3%A8%E4%BA%8E%E5%BF%AB%E9%80%9F%E6%96%B9%E4%BE%BF%E7%9A%84%E5%BC%80%E5%8F%91%E5%8D%95%E4%B8%AA%E4%B8%AA%E4%BD%93%E5%BE%AE%E6%9C%8D%E5%8A%A1%E3%80%82%0A2.%20Spring%20Cloud%20%E6%98%AF%E5%85%B3%E6%B3%A8%E5%85%A8%E5%B1%80%E7%9A%84%E5%BE%AE%E6%9C%8D%E5%8A%A1%E5%8D%8F%E8%B0%83%E6%95%B4%E7%90%86%E6%B2%BB%E7%90%86%E6%A1%86%E6%9E%B6%E4%BB%A5%E5%8F%8A%E4%B8%80%E6%95%B4%E5%A5%97%E7%9A%84%E8%90%BD%E5%9C%B0%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%EF%BC%8C%E5%AE%83%E5%B0%86%20Spring%20Boot%20%E5%BC%80%E5%8F%91%E7%9A%84%E4%B8%80%E4%B8%AA%E4%B8%AA%E5%8D%95%E4%BD%93%E5%BE%AE%E6%9C%8D%E5%8A%A1%E6%95%B4%E5%90%88%E5%B9%B6%E7%AE%A1%E7%90%86%E8%B5%B7%E6%9D%A5%EF%BC%8C%E4%B8%BA%E5%90%84%E4%B8%AA%E5%BE%AE%E6%9C%8D%E5%8A%A1%E4%B9%8B%E9%97%B4%E6%8F%90%E4%BE%9B%EF%BC%9A%E9%85%8D%E7%BD%AE%E7%AE%A1%E7%90%86%EF%BC%8C%E6%9C%8D%E5%8A%A1%E5%8F%91%E7%8E%B0%EF%BC%8C%E6%96%AD%E8%B7%AF%E5%99%A8%EF%BC%8C%E8%B7%AF%E7%94%B1%EF%BC%8C%E5%BE%AE%E4%BB%A3%E7%90%86%EF%BC%8C%E4%BA%8B%E4%BB%B6%E6%80%BB%E7%BA%BF%E7%AD%89%E7%9A%84%E9%9B%86%E6%88%90%E6%9C%8D%E5%8A%A1%E3%80%82%0A3.%20Spring%20Boot%20%E5%8F%AF%E4%BB%A5%E7%A6%BB%E5%BC%80%20Spring%20Cloud%20%E7%8B%AC%E7%AB%8B%E4%BD%BF%E7%94%A8%EF%BC%8C%E4%BD%86%E6%98%AF%20Spring%20Cloud%20%E7%A6%BB%E4%B8%8D%E5%BC%80%20Spring%20Boot%20%EF%BC%8C%E5%B1%9E%E4%BA%8E%E4%BE%9D%E8%B5%96%E7%9A%84%E5%85%B3%E7%B3%BB%E3%80%82%0A%0A****%E6%80%BB%E7%BB%93****%EF%BC%9A%0A%0A*%20Spring%20Boot%20%EF%BC%8C%E4%B8%93%E6%B3%A8%E4%BA%8E%E5%BF%AB%E9%80%9F%EF%BC%8C%E6%96%B9%E4%BE%BF%E7%9A%84%E5%BC%80%E5%8F%91%E5%8D%95%E4%B8%AA%E5%BE%AE%E6%9C%8D%E5%8A%A1%E4%B8%AA%E4%BD%93%E3%80%82%0A*%20Spring%20Cloud%20%EF%BC%8C%E5%85%B3%E6%B3%A8%E5%85%A8%E5%B1%80%E7%9A%84%E6%9C%8D%E5%8A%A1%E6%B2%BB%E7%90%86%E6%A1%86%E6%9E%B6%E3%80%82%0A%0A%23%23%20Spring%20Cloud%20%E5%92%8C%20Dubbo%20%E7%9A%84%E5%8C%BA%E5%88%AB%EF%BC%9F%0A%E5%8F%82%E8%A7%81%20%5B%E3%80%8A%E7%B2%BE%E5%B0%BD%20Dubbo%20%E9%9D%A2%E8%AF%95%E9%A2%98%E3%80%8B%5D(http%3A%2F%2Fsvip.iocoder.cn%2FDubbo%2FInterview)%20%E6%96%87%E7%AB%A0%E7%9A%84%20%5B%E3%80%8CSpring%20Cloud%20%E4%B8%8E%20Dubbo%20%E6%80%8E%E4%B9%88%E9%80%89%E6%8B%A9%EF%BC%9F%E3%80%8D%5D(http%3A%2F%2Fsvip.iocoder.cn%2FSpring-Cloud%2FInterview%2F%23)%20%E9%97%AE%E9%A2%98%E7%9A%84%E8%A7%A3%E7%AD%94%E3%80%82%0A