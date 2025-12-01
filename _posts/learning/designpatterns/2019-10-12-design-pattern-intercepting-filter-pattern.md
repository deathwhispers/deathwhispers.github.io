---
layout: post
title: 拦截过滤器模式 (Intercepting Filter Pattern) 深度解析
slug: design-pattern-intercepting-filter-pattern
type:
  - note
date: 2019-10-12
tags:
  - designPatterns
  - interceptingFilterPattern
categories:
  - designPatterns
author: deathwhispers
created: 2019-01-09 11:45
updated: 2019-03-12 22:17
---


# 📝 拦截过滤器模式 (Intercepting Filter Pattern) 深度解析

## 🚀 1. 模式目的与动机

### 意图

> **拦截过滤器模式：** 用于对应用程序的请求或响应做一些预处理/后处理。定义过滤器，并在把请求传给实际目标应用程序之前或之后应用在请求上。

### 动机

在基于 Web 或分布式应用的架构中，客户端请求在到达核心处理逻辑之前，通常需要经过一系列的通用处理，如：**身份验证 (Authentication)**、**授权 (Authorization)**、**日志记录 (Logging)**、**数据压缩 (Compression)** 等。

如果将这些交叉关注点（Cross-cutting Concerns）直接硬编码到目标处理器中，会导致代码重复和耦合。拦截过滤器模式通过建立一个**可配置的过滤器链 (Filter Chain)**，将这些通用任务从核心业务逻辑中剥离出来，实现了：

1.  **模块化:** 将预处理任务封装在独立的过滤器中。
2.  **可插拔:** 可以动态添加、移除或重新排序过滤器。
3.  **解耦:** 客户端和目标对象只与过滤器管理器交互。

## 🏗️ 2. 模式核心实体与结构

拦截过滤器模式的核心思想与**责任链模式**非常相似，但其目的是预处理和后处理请求，最终目标是执行一个 **Target**。

| 角色 | 英文名称 | 职责描述 |
| :--- | :--- | :--- |
| **过滤器** | Filter | 接口，定义了执行任务的方法（`execute(request)`）。具体的认证、日志逻辑都封装在这里。 |
| **目标** | Target | 实际处理业务请求的对象。在过滤器链执行完毕后，请求最终由它处理。 |
| **过滤器链** | Filter Chain | 持有多个 **过滤器** 实例，并知道 **目标 (Target)**。它负责按照定义的顺序执行链中的所有过滤器，最后将请求传递给 **Target**。 |
| **过滤管理器** | Filter Manager | 管理 **过滤器链** 的创建和配置。客户端通过它来发送请求。 |
| **客户端** | Client | 向 **过滤管理器** 发送请求，并最终触发整个处理流程。 |

### 关键代码 (Java)

#### 1\. 过滤器接口 (Filter)

```java
public interface Filter {
   public void execute(String request);
}
```

#### 2\. 过滤器链 (Filter Chain)

```java
import java.util.ArrayList;
import java.util.List;
// 负责顺序执行过滤器，最后执行 Target
public class FilterChain {
   private List<Filter> filters = new ArrayList<Filter>();
   private Target target;
   
   public void addFilter(Filter filter){
      filters.add(filter);
   }
   
   public void execute(String request){
      for (Filter filter : filters) {
         filter.execute(request); // 依次执行过滤器
      }
      target.execute(request); // 最后执行 Target
   }
   
   public void setTarget(Target target){
      this.target = target;
   }
}
```

#### 3\. 过滤管理器 (Filter Manager)

```java
public class FilterManager {
   FilterChain filterChain;
   
   public FilterManager(Target target){
      filterChain = new FilterChain();
      filterChain.setTarget(target);
   }
   
   public void setFilter(Filter filter){
      filterChain.addFilter(filter);
   }
   
   public void filterRequest(String request){
      filterChain.execute(request); // 客户端通过 Manager 触发链的执行
   }
}
```

## 🌐 3. 模式应用

拦截过滤器模式是 **Java EE Servlet 规范** 中的 **Filter** 机制的基础。

* **应用实例:** Web 应用中的身份验证、日志、压缩、缓存等。
* **优点:** 实现了请求处理逻辑的模块化和可配置性，易于扩展和维护。

-----

# 📝 过滤器模式 / 标准模式 (Filter/Criteria Pattern) 深度解析

## 🚀 1. 模式意图与动机

### 意图

> **过滤器模式（或标准模式）：** 允许开发人员使用不同的标准来过滤一组对象，通过逻辑运算（如 AND, OR）以解耦的方式把它们连接起来，结合多个标准来获得单一标准。

### 动机

当需要从一个集合（列表）中根据多种属性（标准）筛选对象时，如果直接在客户端代码中硬编码所有筛选逻辑，会导致代码僵硬、难以维护，并且无法灵活地组合查询条件。

过滤器模式通过以下方式解决问题：

1.  **抽象标准:** 将每个筛选条件抽象为一个独立的 `Criteria` 对象。
2.  **组合查询:** 使用 `AndCriteria` 和 `OrCriteria` 等组合标准类，灵活地将基本标准连接起来，形成复杂的查询规则。

## 🏗️ 2. 模式核心角色与结构

该模式是一种**结构型模式**，其结构类似于**组合模式**，将单个标准和复合标准统一处理。

| 角色 | 英文名称 | 职责描述 |
| :--- | :--- | :--- |
| **待筛选对象** | Person (或其他实体) | 存储数据的对象，如列表中的单个元素。 |
| **标准接口** | Criteria | 接口，定义了筛选方法（`meetCriteria(List<Person> persons)`），返回满足条件的子列表。 |
| **具体标准** | Concrete Criteria | 实现 **标准接口**，封装单一的筛选逻辑 (如 `CriteriaMale`, `CriteriaSingle`)。 |
| **组合标准** | Composite Criteria | 实现 **标准接口**，但其内部持有并组合其他 **标准接口** 实例，用于实现复杂的逻辑组合 (如 `AndCriteria`, `OrCriteria`)。 |

### 关键代码 (Java)

#### 1\. 待筛选对象 (Person)

```java
public class Person {
    private String name;
    private String gender;
    private String maritalStatus;
    // ... 构造函数和 Getter 方法 ...
}
```

#### 2\. 标准接口 (Criteria)

```java
import java.util.List;
public interface Criteria {
   public List<Person> meetCriteria(List<Person> persons);
}
```

#### 3\. 具体标准 (CriteriaSingle)

```java
import java.util.ArrayList;
import java.util.List;
public class CriteriaSingle implements Criteria {
   @Override
   public List<Person> meetCriteria(List<Person> persons) {
      List<Person> singlePersons = new ArrayList<Person>();
      for (Person person : persons) {
         if(person.getMaritalStatus().equalsIgnoreCase("SINGLE")){
            singlePersons.add(person);
         }
      }
      return singlePersons;
   }
}
```

#### 4\. 组合标准 (AndCriteria)

```java
import java.util.List;
public class AndCriteria implements Criteria {
   private Criteria criteria;
   private Criteria otherCriteria;
   
   public AndCriteria(Criteria criteria, Criteria otherCriteria) {
      this.criteria = criteria;
      this.otherCriteria = otherCriteria;
   }
   
   @Override
   public List<Person> meetCriteria(List<Person> persons) {
      // 链式执行第一个标准
      List<Person> firstCriteriaPersons = criteria.meetCriteria(persons);
      // 在第一个标准的结果上执行第二个标准（即逻辑 AND）
      return otherCriteria.meetCriteria(firstCriteriaPersons); 
   }
}
```

## 🌐 3. 模式应用

* **应用实例:** 数据库查询语言 (SQL) 的 WHERE 子句逻辑、报表系统中的数据过滤、Java 集合框架中的 **Stream API 过滤**（概念相似）。
* **优点:** 实现了过滤逻辑与数据集合的分离，极大地提高了筛选条件的灵活性和可重用性。

-----

## 总结：两种“过滤器”模式的对比

虽然名字相似，但两者目的和实现方式有本质区别：

| 特性 | 拦截过滤器模式 (Intercepting Filter) | 过滤器/标准模式 (Filter/Criteria) |
| :--- | :--- | :--- |
| **模式类型** | J2EE 模式 (行为/结构混合) | 结构型模式 |
| **解决问题** | 请求/响应的**预处理和后处理**（交叉关注点）。 | 根据**多个标准**筛选集合中的对象。 |
| **核心机制** | **责任链**（依次执行，最终到达 Target）。 | **组合**（逻辑组合，返回子集）。 |
| **数据流** | 请求/响应在链中**传递和修改**。 | 集合数据在标准中**筛选和缩减**。 |



