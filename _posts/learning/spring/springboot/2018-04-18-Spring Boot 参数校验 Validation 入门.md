---
layout: post
title: Spring Boot 参数校验 Validation 入门
author: deathwhispers
date: 2018-04-18
slug: spring-boot-validation-getting-started
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2018-04-18 09:57
updated: 2018-04-18 09:57
week: 2018-W16
---

# 1. 概述

在想标题的时候，到底应该叫**数据**校验，还是**参数**校验时，我纠结了，而且非常。

最后，考虑**参数**校验更贴近我们的理解，就选择了它。实际更合适的叫法，还是**数据校验**。

文头艿艿瞎哔哔了一些碎碎念，嫌弃的胖友，可以跳往 [「3. 快速入门」](https://www.iocoder.cn/Spring-Boot/Validation/#) 。

当我们想提供可靠的 API 接口，对参数的校验，以保证最终数据入库的正确性，是**必不可少**的活。例如说，用户注册时，会校验手机格式的正确性，密码非弱密码。

可惜的是，在翻开自己的项目的时候，会发现大量的 API 接口，我们并没有添加相应的参数校验，而是把这个活交给调用方（例如说前端）来完成。😈 甚至在艿艿接触过的后端开发中，认为这是前端的活，简直了！

世界比我们想象中的不安全，可能有"黑客"会绕过浏览器，直接使用 HTTP 工具，模拟请求向后端 API 接口传入违法的参数，以达到它们"不可告人"的目的。

又或者前端开发小哥，不小心漏做了一些 API 接口调用时的参数校验，结果导致用户提交了大量不正确的数据到后端 API 接口，并且这些数据**成功**入库了。这个时候，你是会甩锅给前端小哥，还是怒喷测试小姐姐验收不到位呢？

我相信，很多时候并不是我们不想添加，而是没有统一方便的方式，让我们快速的添加实现参数校验的功能。毕竟，比起枯燥的 CRUD 来说，它更枯燥。例如说，还是拿用户注册的接口，校验手机和密码这两个参数，可能就要消耗掉小 10 行的代码。更不要说，管理后台创建商品这种参数贼多的接口。

😈 世界上大多数碰到的困难，大多已经有了解决方案，特别是软件开发。实际上，Java 早在 2009 年就提出了 [Bean Validation](https://beanvalidation.org/specification/) 规范，并且已经历经 JSR303、JSR349、JSR380 三次标准的置顶，发展到了 **2.0** 。

FROM [https://beanvalidation.org/specification/](https://beanvalidation.org/specification/)

**Bean Validation 1.0** ：Bean Validation 1.0 (JSR [303](https://www.jcp.org/en/jsr/detail?id=303)) was the first version of Java's standard for object validation. It was released in 2009 and is part of Java EE 6. You can learn more about Bean Validation 1.0 [here](https://beanvalidation.org/1.0/) (specification text, API docs etc).

**Bean Validation 1.1** ：Bean Validation 1.1 ([JSR 349](https://www.jcp.org/en/jsr/detail?id=349)) was finished in 2013 and is part of Java EE 7. Its main contributions are method-level validation, integration with CDI, group conversion and some more. You can learn more about Bean Validation 1.1 [here](https://beanvalidation.org/1.1/) (specification text, full change log, API docs etc).

**Bean Validation 2.0** ：Bean Validation 2.0 ([JSR 380](https://www.jcp.org/en/jsr/detail?id=380)) was finished in August 2017.

It's part of Java EE 8 (but can of course be used with plain Java SE as the previous releases).

You can learn more about Bean Validation 2.0 [here](https://beanvalidation.org/2.0/) (specification text, full change log, API docs etc).

Bean Validation 和我们很久以前学习过的 JPA 一样，只提供规范，不提供具体的实现。

艿艿：对 JPA 不了的胖友，可以看看 [《芋道 Spring Boot JPA 入门》](http://www.iocoder.cn/Spring-Boot/JPA/?self=) 一文。

- 在 [Bean Validation API](https://mvnrepository.com/artifact/javax.validation/validation-api) 中，定义了 Bean Validation 相关的接口，并没有具体实现。
- 在 [javax.validation.constraints](https://github.com/eclipse-ee4j/beanvalidation-api/tree/master/src/main/java/javax/validation/constraints) 包下，定义了一系列的校验注解。例如说，[@NotNull](https://github.com/eclipse-ee4j/beanvalidation-api/blob/master/src/main/java/javax/validation/constraints/NotNull.java)、[@NotEmpty](https://github.com/eclipse-ee4j/beanvalidation-api/blob/master/src/main/java/javax/validation/constraints/NotEmpty.java) 。

实现 Bean Validation 规范的数据校验框架，主要有：

- [Hibernate Validator](https://hibernate.org/validator/)不要以为 Hibernate 仅仅是一个 ORM 框架，这只是它的 [Hibernate ORM](https://hibernate.org/orm) 所提供的。Hibernate 可是打着"Everything data"口号的，它还提供了 [Hibernate Search](https://hibernate.org/)、[Hibernate OGM](https://hibernate.org/ogm) 等等解决方案的。😈所以，女朋友也是 data ，我们来 new 一个就好，不需要找。
- [Apache BVal](https://bval.apache.org/)

**绝大多数情况下，也就 99.99% 吧，我们采用 Hibernate Validator 。**

但是，我们在使用 Spring 的项目中，因为 [Spring Validation](https://github.com/spring-projects/spring-framework/tree/master/spring-context/src/main/java/org/springframework/validation) 提供了对 Bean Validation 的内置封装支持，可以使用 [@Validated](https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/validation/annotation/Validated.java) 注解，实现**声明式校验**，而无需直接调用 Bean Validation 提供的 API 方法。而在实现原理上，也是基于 Spring AOP 拦截，实现校验相关的操作。

友情提示：这一点，类似 Spring Transaction 事务，通过 @Transactional 注解，实现声明式事务。

而在 Spring Validation 内部，最终还是调用不同的 Bean Validation 的实现框架。例如说，Hibernate Validator 。

下面，让我们开始遨游，在 Spring Boot 中，如何实现参数校验。

# 2. 注解

在开始入门之前，我们先了解下本文可能会涉及到的注解。

## 2.1 Bean Validation 定义的约束注解

[javax.validation.constraints](https://github.com/eclipse-ee4j/beanvalidation-api/tree/master/src/main/java/javax/validation/constraints) 包下，定义了一系列的约束( constraint )注解。如下：

参考 [《JSR 303 - Bean Validation 介绍及最佳实践》](https://www.ibm.com/developerworks/cn/java/j-lo-jsr303/index.html) 博客。

一共 22 个注解，快速略过即可。

- 空和非空检查
    - @NotBlank ：只能用于字符串不为 null ，并且字符串 #trim() 以后 length 要大于 0 。
    - @NotEmpty ：集合对象的元素不为 0 ，即集合不为空，也可以用于字符串不为 null 。
    - @NotNull ：不能为 null 。
    - @Null ：必须为 null 。
- 数值检查
    - @DecimalMax(value) ：被注释的元素必须是一个数字，其值必须小于等于指定的最大值。
    - @DecimalMin(value) ：被注释的元素必须是一个数字，其值必须大于等于指定的最小值。
    - @Digits(integer, fraction) ：被注释的元素必须是一个数字，其值必须在可接受的范围内。
    - @Positive ：判断正数。
    - @PositiveOrZero ：判断正数或 0 。
    - @Max(value) ：该字段的值只能小于或等于该值。
    - @Min(value) ：该字段的值只能大于或等于该值。
    - @Negative ：判断负数。
    - @NegativeOrZero ：判断负数或 0 。
- Boolean 值检查
    - @AssertFalse ：被注释的元素必须为 true 。
    - @AssertTrue ：被注释的元素必须为 false 。
- 长度检查
    - @Size(max, min) ：检查该字段的 size 是否在 min 和 max 之间，可以是字符串、数组、集合、Map 等。
- 日期检查
    - @Future ：被注释的元素必须是一个将来的日期。
    - @FutureOrPresent ：判断日期是否是将来或现在日期。
    - @Past ：检查该字段的日期是在过去。
    - @PastOrPresent ：判断日期是否是过去或现在日期。
- 其它检查
    - @Email ：被注释的元素必须是电子邮箱地址。
    - @Pattern(value) ：被注释的元素必须符合指定的正则表达式。

## 2.2 Hibernate Validator 附加的约束注解

[org.hibernate.validator.constraints](https://github.com/hibernate/hibernate-validator/tree/master/engine/src/main/java/org/hibernate/validator/constraints) 包下，定义了一系列的约束( constraint )注解。如下：

- @Range(min=, max=) ：被注释的元素必须在合适的范围内。
- @Length(min=, max=) ：被注释的字符串的大小必须在指定的范围内。
- @URL(protocol=,host=,port=,regexp=,flags=) ：被注释的字符串必须是一个有效的 URL 。
- @SafeHtml ：判断提交的 HTML 是否安全。例如说，不能包含 javascript 脚本等等。
- … 等等，就不一一列举了。

## 2.3 @Valid 和 @Validated

[@Valid](https://docs.oracle.com/javaee/7/api/javax/validation/Valid.html) 注解，是 Bean Validation 所定义，可以添加在普通方法、构造方法、方法参数、方法返回、成员变量上，表示它们需要进行约束校验。

[@Validated](https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/validation/annotation/Validated.java) 注解，是 Spring Validation 锁定义，可以添加在类、方法参数、普通方法上，表示它们需要进行约束校验。同时，@Validated 有 value 属性，支持分组校验。属性如下：

// Validated.java Class<?>[] value() default {};

对于初学的胖友来说，很容易搞混 @Valid 和 @Validated 注解。

**① 声明式校验**

Spring Validation **仅**对 @Validated 注解，实现声明式校验。

**② 分组校验**

Bean Validation 提供的 @Valid 注解，因为没有分组校验的属性，所以无法提供分组校验。此时，我们只能使用 ``@Validated` 注解。

**③ 嵌套校验**

相比来说，@Valid 注解的地方，多了【成员变量】。这就导致，如果有嵌套对象的时候，只能使用 @Valid 注解。例如说：

// User.java public class User { private String id; @Valid private UserProfile profile; } // UserProfile.java public class UserProfile { @NotBlank private String nickname; }

- 如果不在 User.profile 属性上，添加 @Valid 注解，就会导致 UserProfile.nickname 属性，不会进行校验。

当然，@Valid 注解的地方，也多了【构造方法】和【方法返回】，所以在有这方面的诉求的时候，也只能使用 @Valid 注解。

**🔥**** 总结**

总的来说，绝大多数场景下，我们使用 @Validated 注解即可。

而在有嵌套校验的场景，我们使用 @Valid 注解添加到成员属性上。

# 3. 快速入门

示例代码对应仓库：[lab-22-validation-01](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01) 。

本小节，我们会实现在 Spring Boot 中，对 SpringMVC 的 Controller 的 API 接口参数，实现参数校验。

同时，因为我们在 Service 也会有参数校验的诉求，所以我们也会提供示例。

## 3.1 引入依赖

在 [pom.xml](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/pom.xml) 文件中，引入相关依赖。

  org.springframework.boot spring-boot-starter-parent 2.1.3.RELEASE    4.0.0 lab-22-validation-01    org.springframework.boot spring-boot-starter-web    org.springframework spring-aspects    org.springframework.boot spring-boot-starter-test test

- [spring-boot-starter-web](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-web) 依赖里，已经默认引入 [hibernate-validator](https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator) 依赖，所以本示例使用的是 Hibernate Validator 作为 Bean Validation 的实现框架。

在 Spring Boot 体系中，也提供了 [spring-boot-starter-validation](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-validation) 依赖。在这里，我们并没有引入。为什么呢？该依赖的目的，重点也是引入 hibernate-validator 依赖，这在 spring-boot-starter-web 已经引入，所以无需重复引入。

## 3.2 Application

创建 [Application.java](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/Application.java) 类，配置 @SpringBootApplication 注解即可。代码如下：

@SpringBootApplication @EnableAspectJAutoProxy(exposeProxy = true) // http://www.voidcn.com/article/p-zddcuyii-bpt.html public class Application { public static void main(String[] args) { SpringApplication.run(Application.class, args); } }

- 添加 @EnableAspectJAutoProxy 注解，重点是配置 exposeProxy = true ，因为我们希望 Spring AOP 能将当前代理对象设置到 [AopContext](https://github.com/spring-projects/spring-framework/blob/master/spring-aop/src/main/java/org/springframework/aop/framework/AopContext.java) 中。具体用途，我们会在下文看到。想要提前看的胖友，可以看看 [《Spring AOP 通过获取代理对象实现事务切换》](http://www.voidcn.com/article/p-zddcuyii-bpt.html) 文章。

先暂时不启动项目。等我们添加好 Controller 。

## 3.3 UserAddDTO

在 [cn.iocoder.springboot.lab22.validation.dto](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto) 包路径下，创建 [UserAddDTO](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto/UserAddDTO.java) 类，为用户添加 DTO 类。代码如下：

// UserAddDTO.java public class UserAddDTO { /** * 账号 */ @NotEmpty(message = "登录账号不能为空") @Length(min = 5, max = 16, message = "账号长度为 5-16 位") @Pattern(regexp = "[1](about:blank#fn1)+$", message = "账号格式为数字以及字母") private String username; /** * 密码 */ @NotEmpty(message = "密码不能为空") @Length(min = 4, max = 16, message = "密码长度为 4-16 位") private String password; // … 省略 setting/getting 方法 }

每个字段上的约束注解，胖友仔细瞅瞅。

## 3.4 UserController

在 [cn.iocoder.springboot.lab22.validation.controller](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/controller) 包路径下，创建 [UserController](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/controller/UserController.java) 类，提供用户 API 接口。代码如下：

// UserController.java @RestController @RequestMapping("/users") @Validated public class UserController { private Logger logger = LoggerFactory.getLogger(getClass()); @GetMapping("/get") public void get(@RequestParam("id") @Min(value = 1L, message = "编号必须大于 0") Integer id) { logger.info("[get][id: {}]", id); } @PostMapping("/add") public void add(@Valid UserAddDTO addDTO) { logger.info("[add][addDTO: {}]", addDTO); } }

- 在类上，添加 @Validated 注解，表示 UserController 是所有接口都需要进行参数校验。
- 对于 #get(id) 方法，我们在 id 参数上，添加了 @Min 注解，校验 id 必须大于 0 。校验不通过示例如下图：

![参数校验失败示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/e7fd65851475f136210de5050ff420bd.jpg)

- 对于 #add(addDTO) 方法，我们在 addDTO 参数上，添加了 @Valid 注解，实现对该参数的校验。校验不通过示例如下图：

![用户添加参数校验失败示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/1c0491f5b97d513a39c30475d1979d11.jpg)

```text
- errors 字段，参数错误明细**数组**。每一个数组元素，对应一个参数错误明细。这里，username 违背了长度不满足 [5, 16] 。
```

示例我们是已经成功跑通了，但是呢，这里有几点差异性，我们要来理解下。

艿艿：解释起来，信息量有点大，胖友保持耐心。

也可以不理解，就按照这么使用即可。

**第一点**，#get(id) 方法上，我们并没有给 id 添加 @Valid 注解，而 #add(addDTO) 方法上，我们给 addDTO 添加 @Valid 注解。这个差异，是为什么呢？

因为 UserController 使用了 @Validated 注解，那么 Spring Validation 就会使用 AOP 进行切面，进行参数校验。而该切面的拦截器，使用的是 [MethodValidationInterceptor](https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/validation/beanvalidation/MethodValidationInterceptor.java) 。

- 对于 #get(id) 方法，需要校验的参数 id ，是**平铺**开的，所以无需添加 @Valid 注解。
- 对于 #add(addDTO) 方法，需要校验的参数 addDTO ，实际相当于**嵌套校验**，要校验的参数的都在 addDTO 里面，所以需要添加 @Valid 注解。

**第二点**，#get(id) 方法的返回的结果是 status = 500 ，而 #add(addDTO) 方法的返回的结果是 status = 400 。

- 对于 #get(id) 方法，在 MethodValidationInterceptor 拦截器中，校验到参数不正确，会抛出 [ConstraintViolationException](https://github.com/eclipse-ee4j/beanvalidation-api/blob/master/src/main/java/javax/validation/ConstraintViolationException.java) 异常。
- 对于 #add(addDTO) 方法，因为 addDTO 是个 POJO 对象，所以会走 SpringMVC 的 [DataBinder](https://docs.spring.io/spring/docs/3.2.x/spring-framework-reference/html/validation.html#validation-binder) 机制，它会调用 DataBinder#validate(Object… validationHints) 方法，进行校验。在校验不通过时，会抛出 [BindException](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/validation/BindException.html) 。

在 SpringMVC 中，默认使用 [DefaultHandlerExceptionResolver](https://hyrepo.com/tech/spring-mvc-error-handling/) 处理异常。

- 对于 BindException 异常，处理成 400 的状态码。
- 对于 ConstraintViolationException 异常，没有特殊处理，所以处理成 500 的状态码。

这里，我们在抛个问题，如果 #add(addDTO 方法，如果参数正确，在走完 DataBinder 中的参数校验后，会不会在走一遍 MethodValidationInterceptor 的拦截器呢？思考 100 毫秒…

答案是会。这样，就会导致浪费。所以 Controller 类里，如果**只有**类似的 #add(addDTO) 方法的**嵌套校验**，那么我可以不在 Controller 类上添加 @Validated 注解。从而实现，仅使用 DataBinder 中来做参数校验。

**第三点**，无论是 #get(id) 方法，还是 #add(addDTO) 方法，它们的返回提示都非常不友好，那么该怎么办呢？

参考 [《芋道 Spring Boot SpringMVC 入门》](http://www.iocoder.cn/Spring-Boot/SpringMVC/?self=) 的 [「5. 全局异常处理」](https://www.iocoder.cn/Spring-Boot/Validation/#) ，使用 @ExceptionHandler 注解，实现自定义的异常处理。这个，我们在本文的 [4. 处理校验异常](https://www.iocoder.cn/Spring-Boot/Validation/#) 小节中，来提供具体示例。

## 3.5 UserService

相比在 Controller 添加参数校验来说，在 Service 进行参数校验，会更加安全可靠。艿艿个人建议的话，Controller 的参数校验可以不做，**Service 的参数校验一定要做**。

在 [cn.iocoder.springboot.lab22.validation.service](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/service) 包路径下，创建 [UserService](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/service/UserService.java) 类，提供用户 Service 逻辑。代码如下：

// UserService.java @Service @Validated public class UserService { private Logger logger = LoggerFactory.getLogger(getClass()); public void get(@Min(value = 1L, message = "编号必须大于 0") Integer id) { logger.info("[get][id: {}]", id); } public void add(@Valid UserAddDTO addDTO) { logger.info("[add][addDTO: {}]", addDTO); } public void add01(UserAddDTO addDTO) { this.add(addDTO); } public void add02(UserAddDTO addDTO) { self().add(addDTO); } private UserService self() { return (UserService) AopContext.currentProxy(); } }

- 和 UserController 的方法是一致的，包括注解。
- 额外添加了 #add01(addDTO) 和 #add02(addDTO) 方法，用于演示方法内部调用。

创建 [UserServiceTest](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/test/java/cn/iocoder/springboot/lab22/validation/service/UserServiceTest.java) 测试类，我们来测试一下简单的 UserService 的每个操作。代码如下：

// UserService.java @RunWith(SpringRunner.class) @SpringBootTest(classes = Application.class) public class UserServiceTest { @Autowired private UserService userService; @Test public void testGet() { userService.get(-1); } @Test public void testAdd() { UserAddDTO addDTO = new UserAddDTO(); userService.add(addDTO); } @Test public void testAdd01() { UserAddDTO addDTO = new UserAddDTO(); userService.add01(addDTO); } @Test public void testAdd02() { UserAddDTO addDTO = new UserAddDTO(); userService.add02(addDTO); } }

**① #testGet() 测试方法**

执行，抛出 ConstraintViolationException 异常。日志如下：

javax.validation.ConstraintViolationException: get.id: 编号必须大于 0 at org.springframework.validation.beanvalidation.MethodValidationInterceptor.invoke(MethodValidationInterceptor.java:116)

- 符合期望。

**② #testAdd() 测试方法**

执行，抛出 ConstraintViolationException 异常。日志如下：

javax.validation.ConstraintViolationException: add.addDTO.username: 登录账号不能为空, add.addDTO.password: 密码不能为空 at org.springframework.validation.beanvalidation.MethodValidationInterceptor.invoke(MethodValidationInterceptor.java:116)

- 符合期望。不同于我们在调用 UserController#add(addDTO) 方法，这里被 MethodValidationInterceptor 拦截，进行参数校验，而不是 DataBinder 当中。

**③ #testAdd01() 测试方法**

执行，正常结束。因为进行 this.add(addDTO) 调用时，this 并不是 Spring AOP 代理对象，所以并不会被 MethodValidationInterceptor 所拦截。

**④ #testAdd02() 测试方法**

执行，抛出 IllegalStateException 异常。日志如下：

java.lang.IllegalStateException: Cannot find current proxy: Set 'exposeProxy' property on Advised to 'true' to make it available. at org.springframework.aop.framework.AopContext.currentProxy(AopContext.java:69)

- 理论来说，因为我们配置了 @EnableAspectJAutoProxy(exposeProxy = true) 注解，在 Spring AOP 拦截时，通过调用 AopContext.currentProxy() 方法，是可以获取到当前的代理对象。结果，此处抛出 IllegalStateException 异常。
- 显然，这里并没有将当前的代理对象，设置到 AopContext 中，所以抛出 IllegalStateException 异常。目前猜测，可能是 BUG 。😈 暂时木有心情去调试，嘿嘿。

# 4. 处理校验异常

示例代码对应仓库：[lab-22-validation-01](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01) 。

在 [「3. 快速入门」](https://www.iocoder.cn/Spring-Boot/Validation/#) 中，我们可以看到，如果直接将校验的结果返回给前端，提示内容的可阅读性是比较差的，所以我们需要对校验抛出的异常进行处理。

在 [《芋道 Spring Boot SpringMVC 入门》](http://www.iocoder.cn/Spring-Boot/SpringMVC/?self=) 的 [「5. 全局异常处理」](https://www.iocoder.cn/Spring-Boot/Validation/#) 小节中，使用 @ExceptionHandler 注解，实现自定义的异常处理。所以本小节，我们在 [「3. 快速入门」](https://www.iocoder.cn/Spring-Boot/Validation/#) 小节的 [lab-22-validation-01](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01) 示例，进一步处理校验异常。

## 4.1 复制粘贴

我们先把 [《芋道 Spring Boot SpringMVC 入门》](http://www.iocoder.cn/Spring-Boot/SpringMVC/?self=) 的 [「5. 全局异常处理」](https://www.iocoder.cn/Spring-Boot/Validation/#) 小节中，需要用到的类，全部复制过来。

- 在 [cn.iocoder.springboot.lab22.validation.constants](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/constants) 包路径下，复制 [ServiceExceptionEnum](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/constants/ServiceExceptionEnum.java) 类。
- 在 [cn.iocoder.springboot.lab22.validation.core.exception](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/exception) 包路径下，复制 [ServiceException](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/exception/ServiceException.java) 类。
- 在 [cn.iocoder.springboot.lab22.validation.core.vo](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/vo) 包路径下，复制 [CommonResult](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/vo/CommonResult.java) 类。
- 在 [cn.iocoder.springboot.lab22.validation.core.web](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/web) 包路径下，复制 [GlobalExceptionHandler](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/web/GlobalExceptionHandler.java) 和 [GlobalResponseBodyHandler](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/web/GlobalResponseBodyHandler.java) 类。

## 4.2 ServiceExceptionEnum

修改 [ServiceExceptionEnum](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/constants/ServiceExceptionEnum.java) 枚举类，增加校验参数不通过的错误码枚举。代码如下：

// ServiceExceptionEnum.java INVALID_REQUEST_PARAM_ERROR(2001001002, "请求参数不合法"),

## 4.3 GlobalExceptionHandler

修改 [GlobalExceptionHandler](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/web/GlobalExceptionHandler.java) 类，增加 #constraintViolationExceptionHandler(…) 方法，处理 ConstraintViolationException 异常。代码如下：

// GlobalExceptionHandler.java @ResponseBody @ExceptionHandler(value = ConstraintViolationException.class) public CommonResult constraintViolationExceptionHandler(HttpServletRequest req, ConstraintViolationException ex) { logger.debug("[constraintViolationExceptionHandler]", ex); // 拼接错误 StringBuilder detailMessage = new StringBuilder(); for (ConstraintViolation<?> constraintViolation : ex.getConstraintViolations()) { // 使用 ; 分隔多个错误 if (detailMessage.length() > 0) { detailMessage.append(";"); } // 拼接内容到其中 detailMessage.append(constraintViolation.getMessage()); } // 包装 CommonResult 结果 return CommonResult.error(ServiceExceptionEnum.INVALID_REQUEST_PARAM_ERROR.getCode(), ServiceExceptionEnum.INVALID_REQUEST_PARAM_ERROR.getMessage() + ":" + detailMessage.toString()); }

- 将每个约束的错误内容提示，拼接起来，使用 ; 分隔。
- 重新请求 UserController#get(id) 对应的接口，响应结果如下：

![ConstraintViolationException异常处理结果](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/d3ec1b5a4735e371f33021306eb48b59.png)

修改 [GlobalExceptionHandler](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/web/GlobalExceptionHandler.java) 类，增加 #bindExceptionHandler(…) 方法，处理 BindException 异常。代码如下：

// GlobalExceptionHandler.java @ResponseBody @ExceptionHandler(value = BindException.class) public CommonResult bindExceptionHandler(HttpServletRequest req, BindException ex) { logger.debug("[bindExceptionHandler]", ex); // 拼接错误 StringBuilder detailMessage = new StringBuilder(); for (ObjectError objectError : ex.getAllErrors()) { // 使用 ; 分隔多个错误 if (detailMessage.length() > 0) { detailMessage.append(";"); } // 拼接内容到其中 detailMessage.append(objectError.getDefaultMessage()); } // 包装 CommonResult 结果 return CommonResult.error(ServiceExceptionEnum.INVALID_REQUEST_PARAM_ERROR.getCode(), ServiceExceptionEnum.INVALID_REQUEST_PARAM_ERROR.getMessage() + ":" + detailMessage.toString()); }

- 将每个约束的错误内容提示，拼接起来，使用 ; 分隔。
- 重新请求 UserController#add(addDTO) 对应的接口，响应结果如下：

![BindException异常处理结果](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/81fa0969f0cb07ae43eccceee303cd3a.png)

# 5. 自定义约束

示例代码对应仓库：[lab-22-validation-01](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01) 。

在大多数项目中，无论是 Bean Validation 定义的约束，还是 Hibernate Validator 附加的约束，都是无法满足我们复杂的业务场景。所以，我们需要自定义约束。

开发自定义约束一共只要**两步**：1）编写自定义约束的**注解**；2）编写自定义的**校验器 ConstraintValidator** 。

下面，就让我们一起来实现一个自定义约束，用于校验参数必须在枚举值的范围内。

## 5.1 IntArrayValuable

在 [cn.iocoder.springboot.lab22.validation.core.validator](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/validator) 包路径下，创建 IntArrayValuable 接口，用于返回值数组。代码如下：

// IntArrayValuable.java public interface IntArrayValuable { /** * @return int 数组 */ int[] array(); }

## 5.2 GenderEnum

在 [cn.iocoder.springboot.lab22.validation.constants](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/constants) 包路径下，创建 [GenderEnum](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/constants/GenderEnum.java) 枚举类，枚举性别。代码如下：

// GenderEnum.java public enum GenderEnum implements IntArrayValuable { MALE(1, "男"), FEMALE(2, "女"); /** * 值数组 */ public static final int[] ARRAYS = Arrays.stream(values()).mapToInt(GenderEnum::getValue).toArray(); /** * 性别值 */ private final Integer value; /** * 性别名 */ private final String name; GenderEnum(Integer value, String name) { this.value = value; this.name = name; } public Integer getValue() { return value; } public String getName() { return name; } @Override public int[] array() { return ARRAYS; } }

- 实现 IntArrayValuable 接口，返回值数组 ARRAYS 。

## 5.3 @InEnum

在 [cn.iocoder.springboot.lab22.validation.core.validator](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/validator) 包路径下，创建 [@InEnum](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/validator/InEnum.java) **自定义约束的注解**。代码如下：

// InEnum.java @Target({METHOD, FIELD, ANNOTATION_TYPE, CONSTRUCTOR, PARAMETER, TYPE_USE}) @Retention(RetentionPolicy.RUNTIME) @Documented @Constraint(validatedBy = InEnumValidator.class) public @interface InEnum { /** * @return 实现 IntArrayValuable 接口的 */ Class<? extends IntArrayValuable> value(); /** * @return 提示内容 */ String message() default "必须在指定范围 {value}"; /** * @return 分组 */ Class<?>[] groups() default {}; /** * @return Payload 数组 */ Class<? extends Payload>[] payload() default {}; /** * Defines several {@code @InEnum} constraints on the same element. */ @Target({METHOD, FIELD, ANNOTATION_TYPE, CONSTRUCTOR, PARAMETER, TYPE_USE}) @Retention(RetentionPolicy.RUNTIME) @Documented @interface List { InEnum[] value(); } }

- 在类上，添加 @@Constraint(validatedBy = InEnumValidator.class) 注解，设置使用的**自定义约束的校验器**。
- value() 属性，设置实现 IntArrayValuable 接口的类。这样，我们就能获得参数需要校验的值数组。
- message() 属性，设置提示内容。默认为 "必须在指定范围 {value}" 。
- 其它属性，复制粘贴即可，都可以忽略不用理解。

## 5.4 InEnumValidator

在 [cn.iocoder.springboot.lab22.validation.core.validator](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/validator) 包路径下，创建 [InEnumValidator](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/core/validator/InEnumValidator.java) **自定义约束的校验器**。代码如下：

// InEnumValidator.java public class InEnumValidator implements ConstraintValidator<InEnum, Integer> { /** * 值数组 */ private Set values; @Override public void initialize(InEnum annotation) { IntArrayValuable[] values = annotation.value().getEnumConstants(); if (values.length == 0) { this.values = Collections.emptySet(); } else { this.values = Arrays.stream(values[0].array()).boxed().collect(Collectors.toSet()); } } @Override public boolean isValid(Integer value, ConstraintValidatorContext context) { // <2.1> 校验通过 if (values.contains(value)) { return true; } // <2.2.1>校验不通过，自定义提示语句（因为，注解上的 value 是枚举类，无法获得枚举类的实际值） context.disableDefaultConstraintViolation(); // 禁用默认的 message 的值 context.buildConstraintViolationWithTemplate(context.getDefaultConstraintMessageTemplate() .replaceAll("\{value}", values.toString())).addConstraintViolation(); // 重新添加错误提示语句 return false; // <2.2.2.> } }

- 实现 [ConstraintValidator](https://github.com/beanvalidation/beanvalidation-api/blob/master/src/main/java/javax/validation/ConstraintValidator.java) 接口。
    - 第一个泛型为 A extends Annotation ，设置对应的自定义约束的注解。例如说，这里我们设置了 @InEnum 注解。
    - 第二个泛型为 T ，设置对应的参数值的类型。例如说，这里我们设置了 Integer 类型。
- 实现 #initialize(annotation) 方法，获得 @InEnum 注解的 values() 属性，获得值数组，设置到 values 属性种。
- 实现 #isValid(value, context) 方法，实现校验参数值，是否在 values 范围内。
    - <2.1> 处，校验参数值在范围内，直接返回 true ，校验通过。
    - <2.2.1> 处，校验不通过，自定义提示语句。
    - <2.2.2> 处，校验不通过，所以返回 false 。

至此，我们已经完成了自定义约束的实现。下面，我们来进行下测试。

## 5.5 UserUpdateGenderDTO

在 [cn.iocoder.springboot.lab22.validation.dto](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto) 包路径下，创建 [UserUpdateGenderDTO](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto/UserUpdateGenderDTO.java) 类，为用户更新性别 DTO。代码如下：

// UserUpdateGenderDTO.java public class UserUpdateGenderDTO { /** * 用户编号 */ @NotNull(message = "用户编号不能为空") private Integer id; /** * 性别 */ @NotNull(message = "性别不能为空") @InEnum(value = GenderEnum.class, message = "性别必须是 {value}") private Integer gender; // … 省略 set/get 方法 }

- 在 gender 字段上，添加 @InEnum(value = GenderEnum.class, message = "性别必须是 {value}") 注解，限制传入的参数值，必须在 GenderEnum 枚举范围内。

## 5.6 UserController

修改 [UserController](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/controller/UserController.java) 类，增加修改性别 API 接口。代码如下：

// UserController.java @PostMapping("/update_gender") public void updateGender(@Valid UserUpdateGenderDTO updateGenderDTO) { logger.info("[updateGender][updateGenderDTO: {}]", updateGenderDTO); }

模拟请求该 API 接口，响应结果如下：

![自定义约束校验失败示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/b7ce5d660b9051bf77d32ee438e15986.png)

因为我们传入的请求参数 gender 的值为 null ，显然不在 GenderEnum 范围内，所以校验不通过，输出 "性别必须是 [1, 2]" 。

# 6. 分组校验

示例代码对应仓库：[lab-22-validation-01](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01) 。

在一些业务场景下，我们需要使用**分组**校验，即相同的 Bean 对象，根据校验分组，使用不同的校验规则。咳咳咳，貌似我们暂时没有这方面的诉求。即使有，也是拆分不同的 Bean 类。当然，作为一篇入门的文章，艿艿还是提供下分组校验的示例。

## 6.1 UserUpdateStatusDTO

在 [cn.iocoder.springboot.lab22.validation.dto](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto) 包路径下，创建 [UserUpdateStatusDTO](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto/UserUpdateStatusDTO.java) 类，为用户更新状态 DTO 。代码如下：

// UserUpdateStatusDTO.java public class UserUpdateStatusDTO { /** * 分组 01 ，要求状态必须为 true */ public interface Group01 {} /** * 状态 02 ，要求状态必须为 false */ public interface Group02 {} /** * 状态 */ @AssertTrue(message = "状态必须为 true", groups = Group01.class) @AssertFalse(message = "状态必须为 false", groups = Group02.class) private Boolean status; // … 省略 set/get 方法 }

- 创建了 Group01 和 Group02 接口，作为两个校验分组。不一定要定义在 UserUpdateStatusDTO 类中，这里仅仅是为了方便。
- status 字段，在 Group01 校验分组时，必须为 true ；在 Group02 校验分组时，必须为 false 。

## 6.2 UserController

修改 [UserController](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/controller/UserController.java) 类，增加两个修改状态的 API 接口。代码如下：

// UserController.java @PostMapping("/update_status_true") public void updateStatusTrue(@Validated(UserUpdateStatusDTO.Group01.class) UserUpdateStatusDTO updateStatusDTO) { logger.info("[updateStatusTrue][updateStatusDTO: {}]", updateStatusDTO); } @PostMapping("/update_status_false") public void updateStatusFalse(@Validated(UserUpdateStatusDTO.Group02.class) UserUpdateStatusDTO updateStatusDTO) { logger.info("[updateStatusFalse][updateStatusDTO: {}]", updateStatusDTO); }

- 对于 #updateStatusTrue(updateStatusDTO) 方法，我们在 updateStatusDTO 参数上，添加了 @Validated 注解，并且设置校验分组为 Group01 。校验不通过示例如下图：

![分组校验Group01失败示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/71b5a2243617902f4da2328e58ba757b.jpg)

- 对于 #updateStatusFalse(updateStatusDTO) 方法，我们在 updateStatusDTO 参数上，添加了 @Validated 注解，并且设置校验分组为 Group02 。校验不通过示例如下图：

![分组校验Group02失败示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/b57dbdd4f60e30df9d104faa52cab40b.jpg)

所以，使用分组校验，核心在于添加上 @Validated 注解，并设置对应的校验分组。

# 7. 手动校验

示例代码对应仓库：[lab-22-validation-01](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01) 。

在上面的示例中，我们使用的主要是 Spring Validation 的声明式注解。然而在少数业务场景下，我们可能需要手动使用 Bean Validation API ，进行参数校验。

修改 [UserServiceTest](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/test/java/cn/iocoder/springboot/lab22/validation/service/UserServiceTest.java) 测试类，增加手动参数校验的示例。代码如下：

// UserServiceTest.java @Autowired // <1.1> private Validator validator; @Test public void testValidator() { // 打印，查看 validator 的类型 // <1.2> System.out.println(validator); // 创建 UserAddDTO 对象 // <2> UserAddDTO addDTO = new UserAddDTO(); // 校验 // <3> Set<ConstraintViolation> result = validator.validate(addDTO); // 打印校验结果 // <4> for (ConstraintViolation constraintViolation : result) { // 属性:消息 System.out.println(constraintViolation.getPropertyPath() + ":" + constraintViolation.getMessage()); } }

- <1.1> 处，注入 Validator Bean 对象。
- <1.2> 处，打印 validator 的类型。输出如下：

org.springframework.validation.beanvalidation.LocalValidatorFactoryBean@48c3205a

```text
- validator 的类型为 [LocalValidatorFactoryBean](https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/validation/beanvalidation/LocalValidatorFactoryBean.java) 。LocalValidatorFactoryBean 提供 JSR-303、JSR-349 的支持，同时兼容 Hibernate Validator 。
- 在 Spring Boot 体系中，使用 [ValidationAutoConfiguration](https://github.com/spring-projects/spring-boot/blob/master/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/validation/ValidationAutoConfiguration.java) 自动化配置类，默认创建 LocalValidatorFactoryBean 作为 Validator Bean 。
```

- <2> 处，创建 UserAddDTO 对象，即 [「3.3 UserAddDTO」](https://www.iocoder.cn/Spring-Boot/Validation/#) ，已经添加相应的约束注解。
- <3> 处，调用 Validator#validate(T object, Class<?>… groups) 方法，进行参数校验。
- <4> 处，打印校验结果。输出如下：

username:登录账号不能为空password:密码不能为空

```text
- 如果校验通过，则返回的 Set<ConstraintViolation<?>> 集合为空。
```

# 8. 国际化 i18n

示例代码对应仓库：[lab-22-validation-01](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01) 。

在一些项目中，我们会有国际化的需求，特别是我们在做 TOB 的 SASS 化服务的时候。那么，显然我们在使用 Bean Validator 做参数校验的时候，也需要提供国际化的错误提示。

给力的是，Hibernate Validator 已经内置了国际化的支持，所以我们只需要简单的配置，就可以实现国际化的错误提示。

## 8.1 应用配置文件

在 [resources](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/resources) 目录下，创建 [application.yaml](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/resources/application.yaml) 配置文件。配置如下：

spring: # i18 message 配置，对应 MessageSourceProperties 配置类 messages: basename: i18n/messages # 文件路径基础名 encoding: UTF-8 # 使用 UTF-8 编码

然后，我们在 [resources/i18](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/resources/i18n) 目录下，创建不同语言的 messages 文件。如下：

- [messages.properties](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/resources/i18n/messages.properties) ：默认的 i18 配置文件。

UserUpdateDTO.id.NotNull=用户编号不能为空

- [messages_en.properties](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/resources/i18n/messages_en.properties) ：英文的 i18 配置文件。

UserUpdateDTO.id.NotNull=userId cannot be empty

- [messages_ja.properties](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-22/lab-22-validation-01/src/main/resources/i18n/messages_ja.properties) ：日文的 i18 配置文件。

UserUpdateDTO.id.NotNull=ユーザー番号は空にできません

## 8.2 ValidationConfiguration

在 [cn.iocoder.springboot.lab22.validation.config](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/config) 包路径下，创建 ValidationConfiguration 配置类，用于创建一个支持 i18 国际化的 Validator Bean 对象。代码如下：

// ValidationConfiguration.java @Configuration public class ValidationConfiguration { /** * 参考 {@link ValidationAutoConfiguration#defaultValidator()} 方法，构建 Validator Bean * * @return Validator 对象 */ @Bean public Validator validator(MessageSource messageSource) { // 创建 LocalValidatorFactoryBean 对象 LocalValidatorFactoryBean validator = ValidationAutoConfiguration.defaultValidator(); // 设置 messageSource 属性，实现 i18 国际化 validator.setValidationMessageSource(messageSource); // 返回 return validator; } }

## 8.3 UserUpdateDTO

在 [cn.iocoder.springboot.lab22.validation.dto](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto) 包路径下，创建 [UserUpdateDTO](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/dto/UserUpdateDTO.java) 类，为用户更新 DTO 。代码如下：

// UserUpdateDTO.java public class UserUpdateDTO { /** * 用户编号 */ @NotNull(message = "{UserUpdateDTO.id.NotNull}") private Integer id; // … 省略 get/set 方法 }

- 不同于我们上面看到的约束注解的 message 属性的设置，这里我们使用了 {} 占位符。

## 8.4 UserController

修改 [UserController](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-22/lab-22-validation-01/src/main/java/cn/iocoder/springboot/lab22/validation/controller/UserController.java) 类，增加用户更新的 API 接口。代码如下：

// UserController.java @PostMapping("/update") public void update(@Valid UserUpdateDTO updateDTO) { logger.info("[update][updateDTO: {}]", updateDTO); }

下面，我们来进行下 API 接口测试。有一点要注意，SpringMVC 通过 Accept-Language 请求头，实现 i18n 国际化。

- Accept-Language = zh 的情况，响应结果如下：

![国际化中文提示示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/620819b83f927d39428044a8beb7e595.jpg)

- Accept-Language = en 的情况，响应结果如下：

![国际化英文提示示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/ac7aa78e850c84fd0b9148995620a7a0.jpg)

- Accept-Language = ja 的情况，响应结果如下：

![国际化日文提示示例](/assets/images/learning/spring/springboot/spring-boot-validation-getting-started/21b512a70f231207844ea2c76208614f.jpg)

至此，我们的 Validator 的 i18n 国际化已经完成了。

不过细心的胖友，会发现 "请求参数不合法" 并没有国际化处理。是的~实际上，国际化是个大工程，涉及到方方面面。例如说，业务信息表的国际化，商品同时支持中文、英文、韩文等多种语言。😈 最近艿艿手头有个新项目，需要做国际化，有这方面需求的胖友，可以一起多多交流呀。

# 666. 彩蛋

希望阅读完本文，能够让胖友更加舒适且优雅的完成各种需要参数校验的地方。😈 不说了，艿艿赶紧给自己的系统去把参数校验给补全，嘿嘿。

当然，有一点要注意，Bean Validation 更多做的是，无状态的参数校验。怎么理解呢？

- 例如说，参数的大小长度等等，是**适合**通过 Bean Validation 中完成。
- 例如说，校验用户名唯一等等，依赖外部数据源的，是**不适合**通过 Bean Validation 中完成。

当然，如果胖友有不同意见，欢迎留言讨论。

受限于篇幅，艿艿偷懒了下，还有一些内容其实可以补充：

- [《Intro to Apache BVal》](https://www.baeldung.com/apache-bval) 使用 Apache BVal 实现参数校验。
- [《使用 Spring 的 Validator 接口进行校验》](http://www.shouce.ren/api/spring2.5/ch05s02.html) ，通过实现 Validator 接口，提供对应 Bean 的参数校验器。

---

1. A-Za-z0-9[↩︎](about:blank#fnref1)
