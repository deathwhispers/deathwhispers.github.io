---
layout: post
title: Spring Boot 的 @Cacheable(Redis) 缓存失效时间解决方案
author: deathwhispers
date: 2019-03-18
slug: spring-boot-cacheable-redis-expire-time-solution
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2019-03-18 09:57
updated: 2019-03-18 09:57
week: 2019-W14
---

原文链接：[https://blog.csdn.net/zyt807/article/details/82428615](https://blog.csdn.net/zyt807/article/details/82428615)

# 问题

@Cacheable注解不支持配置过期时间，所有需要通过配置CacheManneg来配置默认的过期时间和针对每个类或者是方法进行缓存失效时间配置。

# 解决

可以采用如下的配置信息来解决的设置失效时间问题

## **配置信息**

```java
@Bean
public CacheManager cacheManager(RedisConnectionFactory redisConnectionFactory) {;
return new RedisCacheManager(
RedisCacheWriter.nonLockingRedisCacheWriter(redisConnectionFactory),
this.getRedisCacheConfigurationWithTtl(30*60), // 默认策略，未配置的 key 会使用这个
this.getRedisCacheConfigurationMap() // 指定 key 策略
);
}

private Map<String, RedisCacheConfiguration> getRedisCacheConfigurationMap() {;
Map<String, RedisCacheConfiguration> redisCacheConfigurationMap = new HashMap<>();
// SsoCache和BasicDataCache进行过期时间配置
redisCacheConfigurationMap.put("SsoCache", this.getRedisCacheConfigurationWithTtl(24*60*60));
redisCacheConfigurationMap.put("BasicDataCache", this.getRedisCacheConfigurationWithTtl(30*60));
return redisCacheConfigurationMap;
}

private RedisCacheConfiguration getRedisCacheConfigurationWithTtl(Integer seconds) {;
Jackson2JsonRedisSerializer<Object> jackson2JsonRedisSerializer = new Jackson2JsonRedisSerializer<>(Object.class);
ObjectMapper om = new ObjectMapper();
om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
om.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
jackson2JsonRedisSerializer.setObjectMapper(om);
RedisCacheConfiguration redisCacheConfiguration = RedisCacheConfiguration.defaultCacheConfig();
redisCacheConfiguration = redisCacheConfiguration.serializeValuesWith(
RedisSerializationContext
.SerializationPair
.fromSerializer(jackson2JsonRedisSerializer)
).entryTtl(Duration.ofSeconds(seconds));
return redisCacheConfiguration;
}

@Bean
public KeyGenerator wiselyKeyGenerator() {;
return new KeyGenerator() {;
@Override
public Object generate(Object target, Method method, Object... params) {;
StringBuilder sb = new StringBuilder();
sb.append(target.getClass().getName());
sb.append("." + method.getName());
if(params==null||params.length==0||params[0]==null){
    return null;
}
String join = String.join("&", Arrays.stream(params).map(Object::toString).collect(Collectors.toList()));
String format = String.format("%s
{
    %s;
}
", sb.toString(), join);
// log.info("缓存key：" + format);
return format;
}
};
}


```

## 使用方式

```java
@CacheConfig(cacheNames = "SsoCache")
public class SsoCache {
    @Cacheable(keyGenerator = "wiselyKeyGenerator")
    public String getTokenByGsid(String gsid) {;
}
}

// 二者选其一,可以使用value上的信息，来替换类上cacheNames的信息
@Cacheable(value = "BasicDataCache", keyGenerator = "wiselyKeyGenerator")
public String getTokenByGsid(String gsid) {;
}

```

## 效果展示

![18ff7c59114b5bed0133b7dbfc453e73](/assets/images/learning/spring/springboot/spring-boot-cacheable-redis-expire-time-solution/18ff7c59114b5bed0133b7dbfc453e73.png)
