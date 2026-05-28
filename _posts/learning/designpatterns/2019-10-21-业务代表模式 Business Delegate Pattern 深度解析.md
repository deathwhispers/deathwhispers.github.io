---
layout: post
title: 业务代表模式 (Business Delegate Pattern) 深度解析
author: deathwhispers
date: 2019-10-21
slug: design-pattern-business-delegate-pattern-tutorial
categories:
- DesignPatterns
tags:
- DesignPatterns
type: note
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---

# 📝 业务代表模式 (Business Delegate Pattern) 深度解析

## 🚀 1. 模式目的与动机

业务代表模式（Business Delegate Pattern）是一种**J2EE 核心设计模式**，其主要目的是：

1.  **解耦 (Decoupling):** 对表示层（如 Web 页面、UI 客户端）和业务层（实际处理逻辑）进行解耦。
2.  **简化 (Simplification):** 隐藏复杂的业务服务查找（LookUp）和访问细节。
3.  **减少通信 (Optimization):** 减少表示层代码中的远程查询功能和业务层代码的调用次数，提高性能。

简而言之，业务代表充当客户端（表示层）和业务服务（业务层）之间的**中介或门面**。客户端通过这个代表对象调用业务功能，而无需关心业务层服务是如何定位、创建和执行的。

## 🏗️ 2. 模式核心实体与结构

业务代表模式涉及以下四个主要实体：

| 角色 | 英文名称 | 职责描述 |
| :--- | :--- | :--- |
| **客户端** | Client | 表示层代码 (JSP, Servlet, UI)。它使用 **业务代表** 来访问业务层功能。 |
| **业务服务** | Business Service | 业务层的抽象接口。定义了实际的业务处理方法。 |
| **具体服务** | Concrete Service | 实现 **业务服务** 接口的实体类，包含实际的业务逻辑 (例如 EJBService, JMSService)。 |
| **查询服务** | LookUp Service | 负责获取和定位具体的业务服务实现，并将业务对象提供给 **业务代表**。它隐藏了查找服务的复杂性。 |
| **业务代表** | Business Delegate | **核心角色。** 它为客户端提供一个统一的入口，负责**委托**请求给 **查询服务** 获得的具体业务服务。 |

### 模式结构图

该模式的结构可以清晰地展示业务代表如何作为中介连接客户端与业务层：

## 💻 3. Java 代码实现

本实现使用 Java 语言模拟了一个客户端通过业务代表访问 EJB 或 JMS 业务服务的场景。

### 步骤 1: 业务服务接口 (Business Service)

定义业务层功能的抽象接口。

```java
public interface BusinessService {
   public void doProcessing();
}
```

### 步骤 2: 实体服务类 (Concrete Service)

实现业务服务接口，提供具体的业务逻辑。

```java
// EJB 业务服务实现
public class EJBService implements BusinessService {
   @Override
   public void doProcessing() {
      System.out.println("Processing task by invoking EJB Service");
   }
}

// JMS 业务服务实现
public class JMSService implements BusinessService {
   @Override
   public void doProcessing() {
      System.out.println("Processing task by invoking JMS Service");
   }
}
```

### 步骤 3: 业务查询服务 (LookUp Service)

负责查找和实例化正确的业务服务对象。

```java
public class BusinessLookUp {

   /**
    * 根据服务类型获取具体的业务服务实例
    */
   public BusinessService getBusinessService(String serviceType){
      if(serviceType.equalsIgnoreCase("EJB")){
         return new EJBService();
      }else if (serviceType.equalsIgnoreCase("JMS")) {
         return new JMSService();
      } else {
         System.out.println("Unknown Service Type.");
         return null;
      }
   }
}
```

### 步骤 4: 业务代表 (Business Delegate)

作为客户端和业务层之间的中介，负责服务类型的配置和业务调用委托。

```java
public class BusinessDelegate {
   private BusinessLookUp lookupService = new BusinessLookUp();
   private BusinessService businessService;
   private String serviceType;

   /**
    * 设置客户端想要使用的服务类型
    */
   public void setServiceType(String serviceType){
      this.serviceType = serviceType;
   }

   /**
    * 客户端调用的统一入口方法
    */
   public void doTask(){
      // 1. 使用 LookUp Service 查找具体的业务服务
      businessService = lookupService.getBusinessService(serviceType);

      // 2. 委托给具体的业务服务进行处理
      if (businessService != null) {
          businessService.doProcessing();
      }
   }
}
```

### 步骤 5: 客户端 (Client)

表示层代码，它只与业务代表交互。

```java
public class Client {
   BusinessDelegate businessService;

   public Client(BusinessDelegate businessService){
      this.businessService  = businessService;
   }

   /**
    * 客户端执行任务，通过业务代表进行委托
    */
   public void doTask(){
      businessService.doTask();
   }
}
```

### 步骤 6: 演示 (Demo)

```java
public class BusinessDelegatePatternDemo {
   public static void main(String[] args) {
      BusinessDelegate businessDelegate = new BusinessDelegate();
      Client client = new Client(businessDelegate);

      // 客户端要求使用 EJB 服务
      businessDelegate.setServiceType("EJB");
      client.doTask();

      // 客户端要求使用 JMS 服务
      businessDelegate.setServiceType("JMS");
      client.doTask();
   }
}
```

**运行结果：**

```
Processing task by invoking EJB Service
Processing task by invoking JMS Service
```

## ✅ 4. 模式总结

业务代表模式通过引入一个中介对象，将客户端代码从复杂的业务查找和实现细节中解脱出来。它提供了一个**抽象层**，使表示层和业务层之间的交互更加简洁、灵活和解耦。

* **核心优势:** 隐藏复杂性，解耦分层，提高性能（尤其是在处理远程调用时）。
* **应用场景:** 典型的 J2EE 分层架构（如 EJB/Spring MVC + Service 层）中，业务代表模式的思想被广泛应用，用于将 Web 层代码与 Service 层代码隔离。

-----

如果需要将此模式与另一个模式（如**门面模式**或**代理模式**）进行比较，或者想了解其在现代框架中的体现，请告诉我！
