---
layout: post
title: Spring Boot 防抖动
author: deathwhispers
date: 2019-07-11
slug: spring-boot-debounce
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2019-07-11 09:57
updated: 2019-07-11 09:57
week: 2019-W29
---

## [前言](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

作为一名老码农，在开发后端Java业务系统，包括各种管理后台和小程序等。在这些项目中，我设计过单/多租户体系系统，对接过许多开放平台，也搞过消息中心这类较为复杂的应用，但幸运的是，我至今还没有遇到过线上系统由于代码崩溃导致资损的情况。这其中的原因有三点：一是业务系统本身并不复杂；二是我一直遵循某大厂代码规约，在开发过程中尽可能按规约编写代码；三是经过多年的开发经验积累，我成为了一名熟练工，掌握了一些实用的技巧。

## [啥是防抖](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

![防抖概念示意图](/assets/images/learning/spring/springboot/spring-boot-debounce/cd8cdbcfc0a2fb7c9ad497f98d4bbaea.jpeg)

> ❝
> 所谓防抖，一是防用户手抖，二是防网络抖动。在Web系统中，表单提交是一个非常常见的功能，如果不加控制，容易因为用户的误操作或网络延迟导致同一请求被发送多次，进而生成重复的数据记录。要针对用户的误操作，前端通常会实现按钮的loading状态，阻止用户进行多次点击。而对于网络波动造成的请求重发问题，仅靠前端是不行的。为此，后端也应实施相应的防抖逻辑，确保在网络波动的情况下不会接收并处理同一请求多次。

一个理想的防抖组件或机制，我觉得应该具备以下特点：

1. 逻辑正确，也就是不能误判；
2. 响应迅速，不能太慢；
3. 易于集成，逻辑与业务解耦；
4. 良好的用户反馈机制，比如提示"您点击的太快了"

## [思路解析](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

前面讲了那么多，我们已经知道接口的防抖是很有必要的了，但是在开发之前，我们需要捋清楚几个问题。

### [哪一类接口需要防抖?](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

接口防抖也不是每个接口都需要加，一般需要加防抖的接口有这几类：

- 用户输入类接口：比如搜索框输入、表单输入等，用户输入往往会频繁触发接口请求，但是每次触发并不一定需要立即发送请求，可以等待用户完成输入一段时间后再发送请求。
- 按钮点击类接口：比如提交表单、保存设置等，用户可能会频繁点击按钮，但是每次点击并不一定需要立即发送请求，可以等待用户停止点击一段时间后再发送请求。
- 滚动加载类接口：比如下拉刷新、上拉加载更多等，用户可能在滚动过程中频繁触发接口请求，但是每次触发并不一定需要立即发送请求，可以等待用户停止滚动一段时间后再发送请求。

### [如何确定接口是重复的？](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

防抖也即防重复提交，那么如何确定两次接口就是重复的呢？首先，我们需要给这两次接口的调用加一个时间间隔，大于这个时间间隔的一定不是重复提交；其次，两次请求提交的参数比对，不一定要全部参数，选择标识性强的参数即可；最后，如果想做的更好一点，还可以加一个请求地址的对比。

## [分布式部署下如何做接口防抖？](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

有两个方案：

### [使用共享缓存](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

流程图如下：

![使用共享缓存流程图](/assets/images/learning/spring/springboot/spring-boot-debounce/632ad6e66036b525efaf12f8b7e0a195.jpeg)

### [使用分布式锁](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

流程图如下：

![使用分布式锁流程图](/assets/images/learning/spring/springboot/spring-boot-debounce/05ae04729ca0efb7a15ac3cb5e21126e.jpeg)

> ❝
> 常见的分布式组件有Redis、Zookeeper等，但结合实际业务来看，一般都会选择Redis，因为Redis一般都是Web系统必备的组件，不需要额外搭建。

## [具体实现](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

现在有一个保存用户的接口

```java
@PostMapping("/add")
@RequiresPermissions(value = "add")
@Log(methodDesc = "添加用户")
public ResponseEntity<String> add(@RequestBody AddReq addReq) {
    return userService.add(addReq);
}


```

AddReq.java

```java
package com.summo.demo.model.request;

import java.util.List;

import lombok.Data;

@Data
public class AddReq {
    /**
    * 用户名称
    */
    private String userName;
    /**
    * 用户手机号
    */
    private String userPhone;
    /**
    * 角色ID列表
    */
    private List<Long> roleIdList;
}

```

> ❝
> 目前数据库表中没有对userPhone字段做UK索引，这就会导致每调用一次add就会创建一个用户，即使userPhone相同。

## [请求锁](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

根据上面的要求，我定了一个注解`@RequestLock`，使用方式很简单，把这个注解打在接口方法上即可。**RequestLock.java**

```java
package com.summo.demo.model.request;

import java.util.List;

import lombok.Data;

@Data
public class AddReq {
    /**
    * 用户名称
    */
    private String userName;
    /**
    * 用户手机号
    */
    private String userPhone;
    /**
    * 角色ID列表
    */
    private List<Long> roleIdList;
}

```

> ❝
> `@RequestLock`注解定义了几个基础的属性，redis锁前缀、redis锁时间、redis锁时间单位、key分隔符。其中前面三个参数比较好理解，都是一个锁的基本信息。key分隔符是用来将多个参数合并在一起的，比如userName是张三，userPhone是123456，那么完整的key就是"张三&123456"，最后再加上redis锁前缀，就组成了一个唯一key。

## [唯一key生成](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

要做到参数可选，那么用注解的方式最好了，注解如下**RequestKeyParam.java**

```java
package com.example.requestlock.lock.annotation;

import java.lang.annotation.*;

/**
* @description 加上这个注解可以将参数设置为key
*/
@Target(
{
    ElementType.METHOD, ElementType.PARAMETER, ElementType.FIELD;
}
)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
public @interface RequestKeyParam {}

```

> ❝
> 这个注解加到参数上就行，没有多余的属性。

接下来就是lockKey的生成了，代码如下**RequestKeyGenerator.java**

```java
import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Parameter;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.util.ReflectionUtils;
import org.springframework.util.StringUtils;

public class RequestKeyGenerator {
    /**
    * 获取LockKey
    *
    * @param joinPoint 切入点
    * @return
    */
    public static String getLockKey(ProceedingJoinPoint joinPoint) {
        // 获取连接点的方法签名对象
        MethodSignature methodSignature = (MethodSignature) joinPoint.getSignature();
        // Method对象
        Method method = methodSignature.getMethod();
        // 获取Method对象上的注解对象
        RequestLock requestLock = method.getAnnotation(RequestLock.class);
        // 获取方法参数
        final Object[] args = joinPoint.getArgs();
        // 获取Method对象上所有的注解
        final Parameter[] parameters = method.getParameters();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < parameters.length; i++) {
            final RequestKeyParam keyParam = parameters[i].getAnnotation(RequestKeyParam.class);
            // 如果属性不是RequestKeyParam注解，则不处理
            if (keyParam == null) {
                continue;
            }
            // 如果属性是RequestKeyParam注解，则拼接 连接符 "& + RequestKeyParam"
            sb.append(requestLock.delimiter()).append(args[i]);
        }
        // 如果方法上没有加RequestKeyParam注解
        if (StringUtils.isEmpty(sb.toString())) {
            // 获取方法上的多个注解（为什么是两层数组：因为第二层数组是只有一个元素的数组）
            final Annotation[][] parameterAnnotations = method.getParameterAnnotations();
            // 循环注解
            for (int i = 0; i < parameterAnnotations.length; i++) {
                final Object object = args[i];
                // 获取注解类中所有的属性字段
                final Field[] fields = object.getClass().getDeclaredFields();
                for (Field field : fields) {
                    // 判断字段上是否有RequestKeyParam注解
                    final RequestKeyParam annotation = field.getAnnotation(RequestKeyParam.class);
                    // 如果没有，跳过
                    if (annotation == null) {
                        continue;
                    }
                    // 如果有，设置Accessible为true（为true时可以使用反射访问私有变量，否则不能访问私有变量）
                    field.setAccessible(true);
                    // 如果属性是RequestKeyParam注解，则拼接 连接符" & + RequestKeyParam"
                    sb.append(requestLock.delimiter()).append(ReflectionUtils.getField(field, object));
                }
            }
        }
        // 返回指定前缀的key
        return requestLock.prefix() + sb;
    }
}
```

> 由于`@RequestKeyParam`可以放在方法的参数上，也可以放在对象的属性上，所以这里需要进行两次判断，一次是获取方法上的注解，一次是获取对象里面属性上的注解。

## [重复提交判断](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

### [Redis缓存方式](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

**RedisRequestLockAspect.java**

```java
import java.lang.reflect.Method;

import com.summo.demo.exception.biz.BizException;
import com.summo.demo.model.response.ResponseCodeEnum;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.data.redis.connection.RedisStringCommands;
import org.springframework.data.redis.core.RedisCallback;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.types.Expiration;
import org.springframework.util.StringUtils;

/**
* @description 缓存实现
*/
@Aspect
@Configuration
@Order(2)
public class RedisRequestLockAspect {
    private final StringRedisTemplate stringRedisTemplate;

    @Autowired
    public RedisRequestLockAspect(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Around("execution(public * * (..)) && @annotation(com.summo.demo.config.requestlock.RequestLock)")
    public Object interceptor(ProceedingJoinPoint joinPoint) {
        MethodSignature methodSignature = (MethodSignature) joinPoint.getSignature();
        Method method = methodSignature.getMethod();
        RequestLock requestLock = method.getAnnotation(RequestLock.class);
        if (StringUtils.isEmpty(requestLock.prefix())) {
            throw new BizException(ResponseCodeEnum.BIZ_CHECK_FAIL, "重复提交前缀不能为空");
        }
        // 获取自定义key
        final String lockKey = RequestKeyGenerator.getLockKey(joinPoint);
        // 使用RedisCallback接口执行set命令，设置锁键；设置额外选项：过期时间和SET_IF_ABSENT选项
        final Boolean success = stringRedisTemplate.execute(
        (RedisCallback<Boolean>) connection -> connection.set(lockKey.getBytes(), new byte[0],
        Expiration.from(requestLock.expire(), requestLock.timeUnit()),
        RedisStringCommands.SetOption.SET_IF_ABSENT));
        if (!success) {
            throw new BizException(ResponseCodeEnum.BIZ_CHECK_FAIL, "您的操作太快了,请稍后重试");
        }
        try {
            return joinPoint.proceed();
        } catch (Throwable throwable) {
            throw new BizException(ResponseCodeEnum.BIZ_CHECK_FAIL, "系统异常");
        }
    }
}
```

> ❝
> 这里的核心代码是stringRedisTemplate.execute里面的内容，正如注释里面说的"使用RedisCallback接口执行set命令，设置锁键；设置额外选项：过期时间和SET_IF_ABSENT选项"，有些同学可能不太清楚`SET_IF_ABSENT`是个啥,这里我解释一下：`SET_IF_ABSENT`是 RedisStringCommands.SetOption 枚举类中的一个选项，用于在执行 SET 命令时设置键值对的时候，如果键不存在则进行设置，如果键已经存在，则不进行设置。

### [Redisson分布式方式](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng%3D%3D&mid=2247576728&idx=1&sn=1298645b025eb51d9078e8c3de7b3c17&scene=21#wechat_redirect)

Redisson分布式需要一个额外依赖，引入方式

```xml
<dependency>
  <groupId>org.redisson</groupId>
  <artifactId>redisson-spring-boot-starter</artifactId>
  <version>3.10.6</version>
</dependency>
```

由于我之前的代码有一个RedisConfig，引入Redisson之后也需要单独配置一下，不然会和RedisConfig冲突**RedissonConfig.java**

```java
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RedissonConfig {
    @Bean
    public RedissonClient redissonClient() {
        Config config = new Config();
        // 这里假设你使用单节点的Redis服务器
        config.useSingleServer()
        // 使用与Spring Data Redis相同的地址
        .setAddress("redis://127.0.0.1:6379");
        // 如果有密码
        //.setPassword("xxxx");
        // 其他配置参数
        //.setDatabase(0)
        //.setConnectionPoolSize(10)
        //.setConnectionMinimumIdleSize(2);
        // 创建RedissonClient实例
        return Redisson.create(config);
    }
}


```

配好之后，核心代码如下**RedissonRequestLockAspect.java**

```java
import java.lang.reflect.Method;

import com.summo.demo.exception.biz.BizException;
import com.summo.demo.model.response.ResponseCodeEnum;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.util.StringUtils;

/**
* @description 分布式锁实现
*/
@Aspect
@Configuration
@Order(2)
public class RedissonRequestLockAspect {
    private RedissonClient redissonClient;

    @Autowired
    public RedissonRequestLockAspect(RedissonClient redissonClient) {
        this.redissonClient = redissonClient;
    }

    @Around("execution(public * * (..)) && @annotation(com.summo.demo.config.requestlock.RequestLock)")
    public Object interceptor(ProceedingJoinPoint joinPoint) {
        MethodSignature methodSignature = (MethodSignature) joinPoint.getSignature();
        Method method = methodSignature.getMethod();
        RequestLock requestLock = method.getAnnotation(RequestLock.class);
        if (StringUtils.isEmpty(requestLock.prefix())) {
            throw new BizException(ResponseCodeEnum.BIZ_CHECK_FAIL, "重复提交前缀不能为空");
        }
        // 获取自定义key
        final String lockKey = RequestKeyGenerator.getLockKey(joinPoint);
        // 使用Redisson分布式锁的方式判断是否重复提交
        RLock lock = redissonClient.getLock(lockKey);
        boolean isLocked = false;
        try {
            // 尝试抢占锁
            isLocked = lock.tryLock();
            // 没有拿到锁说明已经有了请求了
            if (!isLocked) {
                throw new BizException(ResponseCodeEnum.BIZ_CHECK_FAIL, "您的操作太快了,请稍后重试");
            }
            // 拿到锁后设置过期时间
            lock.lock(requestLock.expire(), requestLock.timeUnit());
            try {
                return joinPoint.proceed();
            } catch (Throwable throwable) {
                throw new BizException(ResponseCodeEnum.BIZ_CHECK_FAIL, "系统异常");
            }
        } catch (Exception e) {
            throw new BizException(ResponseCodeEnum.BIZ_CHECK_FAIL, "您的操作太快了,请稍后重试");
        } finally {
            // 释放锁
            if (isLocked && lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}
```

> ❝
> Redisson的核心思路就是抢锁，当一次请求抢到锁之后，对锁加一个过期时间，在这个时间段内重复的请求是无法获得这个锁，也不难理解。

测试一下。

- **第一次提交，"添加用户成功"**

![第一次提交成功](/assets/images/learning/spring/springboot/spring-boot-debounce/d83a72fe220c105756705c06d058ff38.jpeg)

- **短时间内重复提交，"BIZ-0001:您的操作太快了,请稍后重试"**

![短时间内重复提交失败](/assets/images/learning/spring/springboot/spring-boot-debounce/e94dd441b421cefc097243ba5aa07563.jpeg)

- **过几秒后再次提交，"添加用户成功"**

![过几秒后再次提交成功](/assets/images/learning/spring/springboot/spring-boot-debounce/ebeb516566ec5fd089b1ae60f8655195.jpeg)

> ❝
> 从测试的结果上看，防抖是做到了，但是随着缓存消失、锁失效，还是可以发起同样的请求，所以要真正做到接口幂等性，还需要业务代码的判断、设置数据库表的UK索引等操作。我在文章里面说到生成唯一key的时候没有加用户相关的信息，比如用户ID、IP属地等，真实生产环境建议加上这些，可以更好地减少误判。

---