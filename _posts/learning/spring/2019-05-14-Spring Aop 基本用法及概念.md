---
layout: post
title: Spring Aop 基本用法及概念
author: deathwhispers
date: 2019-05-14
slug: spring-aop-basic-usage-concept
categories:
- Spring
tags:
- Spring
type: note
status: draft
created: 2019-05-14 10:00
updated: 2019-05-14 10:00
week: 2019-W21
---

参考文章：

Spring AOP切面表达式详解： [https://blog.csdn.net/xubo_ob/article/details/78182014](https://blog.csdn.net/xubo_ob/article/details/78182014)

Spring AOP中pointcut 表达式详解： [https://www.cnblogs.com/rainy-shurun/p/5195439.html](https://www.cnblogs.com/rainy-shurun/p/5195439.html)

说说 Spring AOP 中 @Aspect 的高级用法： [https://blog.csdn.net/deniro_li/article/details/81838197](https://blog.csdn.net/deniro_li/article/details/81838197)

**AOP的一些注意事项：**

**1.对于切入点中的类，必须要有公有的构造方法，否则会抛出异常 ***************** **

**2.使用aop时，需添加配置spring.aop.auto = true (默认为true) 是否开启aop动态代理**

**proxy-target-class: true (默认为false) 是否启用cglib代理**

**··········**

spring Aop的八个概念：

1. 通知(advice):通知定义了在切入点代码执行时间点附近需要做的工作
2. 连接点(joinPoint)：程序能够应用通知的一个“时机”，这些“时机”就是连接点，例如：方法调用时、异常抛出时、方法返回后等
3. 切入点(pointcut)：通知定义了切面要发生的“故事”，连接点定义了“故事”发生的时机，那么切入点就定义了“故事”发生”的地点“，例如某个类或方法的名称，Spring中允许我们使用正则表达式来定义。
4. 切面(Aspect)：通知、连接点和切入点共同组成了切面：时间、地点和要发生的故事
5. 引入(Introduction)：引入允许我们向现有的类添加新的方法和属性（Spring提供了一个方法注入的功能）
6. 目标对象(target)：即被通知对象，解耦和，通知的逻辑从具体的业务类分离到aop切面中
7. 代理(proxy)：应用通知的对象，
8. 织入(Weaving)：把切面应用到目标对象来创建新的代理对象的过程，织入一般发生在以下几个时机
    1. 编译时：当一个类文件被编译时进行织入，这需要特殊的编译器才可以做到，例如AspectJ的织入编译器
    2. 类加载时：使用特殊的 ClassLoader 在目标类被加载到程序之前增强类的字节代码
    3. 运行时：切面在运行的某个时刻被织入，SpringAop 就是以这种方式织入切面的，原理应该是使用了 JDK 的动态代理

使用AOP的几种方式

9. 经典的基于代理的AOP
10. @AspectJ注解驱动的切面
11. 纯POJO切面
12. 注入式AspectJ切面

**aop切入点表达式：**

1、切入点表达式：对指定的方法进行拦截，并且生成代理表达式。

2、拦截所有public方法

```xml
<aop:pointcut expression="execution(public * *(..))"
```

3、拦截所有save开头的方法

```xml
<aop:pointcut expression="execution(* save*(..))" id="pt"/>
```

4、拦截指定类的指定方法

```xml
<aop:pointcut expression="execution(public * 包名.类名.方法名(..))" id="pt"/>
```

5、拦截指定类的所有方法

```xml
<aop:pointcut expression="execution(* 包名.类名.*(..))" id="pt"/>
```

6、拦截指定包，以及其自包下所有类的所有方法

```xml
<aop:pointcut expression="execution(* cn..*.*(..))" id="pt"/>
```

7、多个表达式

```xml
<aop:pointcut expression="execution(* 包名.类名.方法名()) || execution(* 包名.类名（不同的类）.方法名())" id="pt"/>
<aop:pointcut expression="execution(* 包名.类名.方法名()) or execution(* 包名.类名（不同的类）.方法名())" id="pt"/>
```

8、取非值

```xml
<aop:pointcut expression="!execution(* 包名.类名.方法名())" id="pt"/>
<aop:pointcut expression=" not execution(* 包名.类名.方法名())" id="pt"/>
```

@Around注解

使用环绕通知的注意事项:

13. 环绕通知是所有通知类型中功能最为强大的,能够全面的控制连接点,甚至可以控制是否执行连接点
14. 使用@Around时:连接点的**参数必须是 ProceedingJoinPoint**
.它是 JoinPoint 的子接口,允许控制何时执行,是否执行连接点
15. 在使用@Around时,**需要明确调用 ProceedingJoinPoint 的 proceed() 方法**来执行被代理的方法,如果没有调用 proceed() 方法,会导致通知执行了,但是目标方法没有被执行.
16. 注意：@Around 环绕通知需要返回目标方法执行之后的结果，即调用 **ProceedingJoinPoint .proceed()**的返回值；**否则，会出现空指针异常**

**示例代码：**

```java
@Around("execution(* com..Spring4.AOP.*.*(..))")
public Object aroundMethod(ProceedingJoinPoint pjd)
{
    Object result = null;
    String methodName = pjd.getSignature().getName();
    try
    {
        //前置通知    System.out.println("The method " + methodName + " begins with " + Arrays.asList(pjd.getArgs()));
        //执行目标方法    result = pjd.proceed();
        //返回通知    System.out.println("The method " + methodName + " ends with " + result);
        } catch (Throwable e) {
        //异常通知    System.out.println("The method " + methodName + " occurs exception:" + e);
        throw new RuntimeException(e);
    }
    //后置通知System.out.println("The method " + methodName + " ends");
    return result;
```
