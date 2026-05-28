---
layout: post
title: Srping Boot Cache 本地缓存
author: deathwhispers
date: 2020-05-22
slug: srping-boot-cache-local-cache
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2025-01-09 11:46
updated: 2025-03-12 18:41
---

针对某些读写比很高的场景，使用本地缓存可以极大提高访问效率。

springboot中对cache做了很好的支持

添加依赖

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

通过注解启动缓存

```java
//启动缓存@EnableCaching@SpringBootApplicationpublic class BootCacheApplication {    public static void main(String[] args) {        SpringApplication.run(BootCacheApplication.class, args);    }}
```

使用

```java
@Slf4j@Servicepublic class PersonService {    @Resource    private PersonMapper personMapper;    @Cacheable("person")    public Person getOne(int id) {        log.info("load one person");        return personMapper.selectOne(id);    }    @CacheEvict(value = "person", key = "#person.id")    public void update(Person person) {        personMapper.updateById(person);    }}
```

- @Cacheable是最主要的注解，它指定了被注解方法的返回值是可被缓存的
- @CacheEvict注解是@Cacheable注解的反向操作，它负责从给定的缓存中移除一个值

Spring Boot Cache默认使用ConcurrentHashMap作为缓存的实现，只提供了最基础的功能，实际项目中往往需要更加专业的缓存实现。比如Caffeine，EhCache，Redis等

使用Caffeine作为缓存实现

使用Spring Boot Cache框架，其中一个很大的好处，就是可以很方便的更换缓存实现

### 添加依赖

```xml
<dependency>
  <groupId>com.github.ben-manes.caffeine</groupId>
  <artifactId>caffeine</artifactId>
</dependency>
```

Spring Boot会检查class path里的类，发现合适的（比如caffeine）就会生成对应的CacheManager

### 添加特定配置

application.properties

```yaml
spring:  cache:    type: mqttTokenCache    cache-names: mqttTokenCache    caffeine:        spec: maximumSize=1,expireAfterAccess=15s
```

Spring Boot 2已经不支持Guava作为Cache（用户代码内部还是可以使用，只是Spring框架的Cache不支持），代替Guava是的Caffeine，用法跟Guava类似，迁移成本很低

### 其他

- 如果classpath有多个缓存组件，可以通过配置指定使用的缓存组件

spring.cache.type=caffeine
