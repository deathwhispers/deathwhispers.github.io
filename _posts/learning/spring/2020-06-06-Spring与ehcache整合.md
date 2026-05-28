---
layout: post
title: Spring与ehcache整合
author: deathwhispers
date: 2020-06-06
slug: spring-ehcache-integration
categories:
- Spring
tags:
- Spring
type: note
status: draft
created: 2020-06-06 10:00
updated: 2020-06-06 10:00
week: 2020-W23
---

1.添加依赖：

```xml
<!-- ehcache缓存 --><dependency>
   <groupId>net.sf.ehcache</groupId>
   <artifactId>ehcache</artifactId>
   <version>2.10.1</version>
</dependency>
<dependency>
   <groupId>org.springframework</groupId>
   <artifactId>spring-context-support</artifactId>
   <version>4.3.8.RELEASE</version>
</dependency>
```

2.ehcahce.xml:

```xml
<ehcache>
  <diskStorepath="java.io.tmpdir"/>    <defaultCache      maxEntriesLocalHeap="10000"      eternal="false"      timeToIdleSeconds="120"      timeToLiveSeconds="120"      maxEntriesLocalDisk="10000000"      diskExpiryThreadIntervalSeconds="120"      memoryStoreEvictionPolicy="LRU">
      <persistencestrategy="localTempSwap"/>      </defaultCache>    <!-- 缓存键 -->    <cachename="exams"      maxElementsInMemory="1000"      eternal="false"      overflowToDisk="true"      timeToIdleSeconds="10"      timeToLiveSeconds="20"/>
</ehcache>
```

3.spring-ehcache.xml

```xml
<?xml version="1.0"encoding="UTF-8"?><beansxmlns="http://www.springframework.org/schema/beans";      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance";      xmlns:cache="http://www.springframework.org/schema/cache";      xsi:schemaLocation="http://www.springframework.org/schema/beanshttp://www.springframework.org/schema/beans/spring-beans.xsdhttp://www.springframework.org/schema/cachehttp://www.springframework.org/schema/cache/spring-cache.xsd   ">
   <!-- 配置缓存管理器 -->   <beanid="cacheManager"class="org.springframework.cache.ehcache.EhCacheCacheManager">
        <propertyname="cacheManager"ref="ehcache"></property>
   </bean>
   <beanid="ehcache"          class="org.springframework.cache.ehcache.EhCacheManagerFactoryBean">
            <!-- 指定ehcache配置文件 -->            <propertyname="configLocation"value="classpath:ehcache.xml"></property>
   </bean>
   <cache:annotation-drivencache-manager="cacheManager"></cache:annotation-driven></beans>
```

4.业务层方法：

```java
@Cacheable("exams")publicList<Exam> list() {    returnexamDao.findAll();}@CachePut("exams")//清空缓存@Transactional//当前方法受事务管理public voidadd(Exam exam)throwsTipException {    examDao.insert(exam);}
```
