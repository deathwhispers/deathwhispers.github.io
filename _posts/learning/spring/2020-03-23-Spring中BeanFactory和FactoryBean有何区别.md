---
layout: post
title: Spring中BeanFactory和FactoryBean有何区别
author: deathwhispers
date: 2020-03-23
slug: spring-beanfactory-factorybean-difference
categories:
- Spring
tags:
- Spring
type: note
status: draft
created: 2020-03-23 10:00
updated: 2020-03-23 10:00
week: 2020-W13
---

其实从名字上就能看出来个一二

- BeanFactory 是 Factory
- 而 FactoryBean 是一个 Bean

我们先来看下总结：

- BeanFactory 是 Spring 框架的核心接口之一，用于管理和获取应用程序中的 Bean 实例。它是一个工厂模式的实现，负责创建、配置和管理 Bean 对象。BeanFactory 是 Spring IoC 容器的基础，它可以从配置元数据（如 XML 文件）中读取 Bean 的定义，并在需要时实例化和提供这些 Bean。
- FactoryBean 是一个特殊的 Bean，它是一个工厂对象，用于创建和管理其他 Bean 的实例。FactoryBean 接口定义了一种创建 Bean 的方式，它允许开发人员在 Bean 的创建过程中进行更多的自定义操作。通过实现 FactoryBean 接口，开发人员可以创建复杂的 Bean 实例，或者在 Bean 实例化之前进行一些额外的逻辑处理。

区别在于，BeanFactory 是 Spring 框架的核心接口，用于管理和提供 Bean 实例，而 FactoryBean 是一个特殊的 Bean，用于创建和管理其他 Bean 的实例。FactoryBean 在 Bean 的创建过程中提供更多的自定义能力，允许进行额外的逻辑处理。

可能有的小伙伴看的还不是很清楚，我们再来详细看下。

## BeanFactory

BeanFactory 看名字就知道这是一个 Bean 工厂，小伙伴们知道，Spring IoC 容器帮我们完成了 Bean 的创建、管理等操作，那么这些操作都离不开 BeanFactory。

我们来简单看下 BeanFactory 的代码：

```java
public interface BeanFactory
{
    String FACTORY_BEAN_PREFIX = "&" ;
    Object getBean(String name) throws BeansException ;
    <T> T getBean(String name, Class<T> requiredType) throws BeansException ;
    Object getBean(String name, Object... args) throws BeansException ;
    <T> T getBean(Class<T> requiredType) throws BeansException ;
    <T> T getBean(Class<T> requiredType, Object... args) throws BeansException ;
    <T> ObjectProvider<T> getBeanProvider(Class<T> requiredType) ;
    <T> ObjectProvider<T> getBeanProvider(ResolvableType requiredType) ;
    boolean containsBean(String name) ;
    boolean isSingleton(String name) throws NoSuchBeanDefinitionException ;
    boolean isPrototype(String name) throws NoSuchBeanDefinitionException ;
    boolean isTypeMatch(String name, ResolvableType typeToMatch) throws NoSuchBeanDefinitionException ;
    boolean isTypeMatch(String name, Class<?> typeToMatch) throws NoSuchBeanDefinitionException ;
    @Nullable Class<?> getType(String name) throws NoSuchBeanDefinitionException ;
    @Nullable Class<?> getType(String name, boolean allowFactoryBeanInit) throws NoSuchBeanDefinitionException ;
    String[] getAliases(String name) ;
}
```

这些方法基本上都见名知义：

- FACTORY_BEAN_PREFIX：这个变量其实是说，如果当前 Bean 不是像 User、Book 这种普通 Bean，而是一个 FactoryBean，就给这个 Bean 名字加一个 & 前缀，这个我在第二小节和小伙伴们演示。
- getBean：这个方法就是根据 Bean 的名字、类型等去查询 Bean。
- getBeanProvider：这个方法可以获取一个 ObjectProvider，ObjectProvider 是 Spring 框架中的一个接口，用于获取 Bean 对象的实例。它提供了一种延迟加载 Bean 的方式，可以在需要时动态地获取 Bean 实例（懒加载）。
- containsBean：判断是否包含某个 Bean。
- isSingleton：判断某个 Bean 是否是单例的。
- isPrototype：判断某个 Bean 是否是多例的。
- isTypeMatch：判断某一个 Bean 的类型是否是给定类型。
- getType：获取 Bean 的类型。
- getAliases：获取 Bean 的别名。

可以看到，很多都是大家日常开发中常见常用的方法。

很多小伙伴刚开始接触 Spring 的时候，都会用到一个对象 ClassPathXmlApplicationContext，这其实就是 BeanFactory 的一个子类。我们来看下 BeanFactory 的继承图：

![](/assets/images/learning/spring/spring-beanfactory-factorybean-difference/b9f4da8e7f260233dbf6e1e0b9ed8b97.png)

继承类比较多，我说几个大家可能比较熟悉的：

1. ClassPathXmlApplicationContext：这个是 Spring 容器启动时，从当前类路径下去加载 XML 配置文件，参数就是 classpath 下 XML 的文件路径。
2. FileSystemXmlApplicationContext：这个是 Spring 容器启动时，从文件系统中去加载 XML 配置文件，参数一个绝对路径。
3. AnnotationConfigApplicationContext：这个是如果我们使用 Java 代码去做 Spring 容器的配置的话，通过这个配置类去加载 Java 配置类。
4. DefaultListableBeanFactory：这个默认实现了 ListableBeanFactory 和 BeanDefinitionRegistry 接口，是一个比较成熟的 BeanFactory。

好啦，这就是 BeanFactory 的特点，大家明白了吧～

## FactoryBean

### 分析

FactoryBean 其实很多小伙伴可能都见过，只是可能没去总结归纳。我给小伙伴们举几个例子。

在 SSM 项目中，如果我们要配置 MyBatis 到项目中，一般需要配置下面这个 Bean：

```xml
<bean class="org.mybatis.spring.SqlSessionFactoryBean" id="sqlSessionFactoryBean">
  <property name="dataSource" ref="dataSource"/>
  <property name="typeAliasesPackage" value="org.javaboy.shirodemo.model"/>
  <property name="mapperLocations">
    <list>
      <value>classpath*:org/javaboy/shirodemo/mapper/*.xml</value>
    </list>
  </property>
</bean>
```

我们在配置 Shiro 的时候，一般都要配置如下 Bean：

```xml
<bean class="org.apache.shiro.spring.web.ShiroFilterFactoryBean" id="shiroFilter">
  <property name="securityManager" ref="securityManager"/>
  <property name="loginUrl" value="/login"/>
  <property name="successUrl" value="/index"/>
  <property name="unauthorizedUrl" value="/unauthorizedUrl"/>
  <property name="filterChainDefinitions">
    <value>
      /index=anon
      /doLogin=anon
      /hello=user
      /**=authc
    </value>
  </property>
</bean>
```

如果我们前端传递的参数是 key-value 格式，并且有一个日期，那么小伙伴们知道，服务端 SpringMVC 默认无法处理这个日期，需要配置一个日期转换器，一般我们在 Spring 容器中添加如下 Bean：

```xml
<bean class="org.springframework.format.support.FormattingConversionServiceFactoryBean" id="conversionService">
  <property name="converters">
    <set>
      <ref bean="myDateConverter"/>
    </set>
  </property>
</bean>
<mvc:annotation-driven conversion-service="conversionService"/>
```

小伙伴们观察上面三个 Bean 有一个共同的特点，**那就是 Bean 的名字都是 xxxFactoryBean**。

为什么要用 xxxFactoryBean 而不直接把需要的 Bean 注入到 Spring 容器中去呢？以 MyBatis 为例：

手动配置过 MyBatis 的小伙伴应该都知道，MyBatis 有两个重要的类，一个是 SqlSessionFactory，还有一个是 SqlSession，通过 SqlSessionFactory 可以获取到一个 SqlSession。但是不知道小伙伴们是否还记得配置代码，手动配置代码如下：

```java
public class SqlSessionFactoryUtils
{
    private static SqlSessionFactory SQLSESSIONFACTORY = null ;
    public static SqlSessionFactory getInstance()
    {
        if (SQLSESSIONFACTORY == null)
        {
            try
            {
                SQLSESSIONFACTORY = new SqlSessionFactoryBuilder().build(Resources.getResourceAsStream("mybatis-config.xml")) ;
            }
            catch (IOException e)
            {
                e.printStackTrace() ;
            }
        }
        return SQLSESSIONFACTORY ;
    }
}
public class Main
{
    public static void main(String[] args)
    {
        SqlSessionFactory factory = SqlSessionFactoryUtils.getInstance() ;
        SqlSession sqlSession = factory.openSession() ;
        List<User> list = sqlSession.selectList("org.javaboy.mybatis01.mapper.UserMapper.getAllUser") ;
        for (User user : list)
        {
            System.out.println("user = " + user) ;
        }
        sqlSession.close() ;
    }
}


```

小伙伴们看到，无论是 SqlSessionFactory 还是 SqlSession，都不是正经 new 出来的，其实这两个都是接口，显然不可能 new 出来，前者通过建造者模式去配置各种属性，最后生成一个 SqlSessionFactory 的实例，后者则通过前者这个工厂去生成，最终拿到的都是这两个接口的子类的对象。

所以，对于 SqlSessionFactory 和 SqlSession 就没法在 Spring 容器中直接进行配置，那么对于这样的 Bean，就可以通过 xxxFactoryBean 来进行配置。

我们来看下 SqlSessionFactoryBean 类，源码很长，我挑了重要的出来：

```java
public class SqlSessionFactoryBean implements FactoryBean<SqlSessionFactory>, InitializingBean, ApplicationListener<ApplicationEvent>
{
    private SqlSessionFactory sqlSessionFactory ;
    @Override public SqlSessionFactory getObject() throws Exception
    {
        if (this.sqlSessionFactory == null)
        {
            afterPropertiesSet() ;
        }
        return this.sqlSessionFactory ;
    }
    @Override public Class<? extends SqlSessionFactory> getObjectType()
    {
        return this.sqlSessionFactory == null ? SqlSessionFactory.class : this.sqlSessionFactory.getClass() ;
    }
    @Override public boolean isSingleton()
    {
        return true ;
    }
}


```

大家看一下，SqlSessionFactoryBean 需要实现 FactoryBean 接口，并且在实现接口的时候指定泛型是 SqlSessionFactory，也就是 SqlSessionFactoryBean 最终产出的 Bean 是 SqlSessionFactory。实现了 FactoryBean 接口之后，就需要实现接口中的三个方法：

- getObject：这个方法返回的对象，就是真正要注册到 Spring 容器中的对象，在这个方法中，我们就可以按照各种方式对 Bean 进行各种配置了。
- getObjectType：这个方法返回注册到 Spring 容器中的对象类型。
- isSingleton：这个方法用来返回注册到 Spring 容器中的 Bean 是否是单例的。

这就是 FactoryBean 的特点，由于某一个 Bean 的初始化过于复杂，那么就可以通过 FactoryBean 来帮助注册到 Spring 容器中去。

### 实践

松哥再写一个简单的例子给小伙伴们体验一把 FactoryBean。

假设我有如下类：

```java
public class Author
{
    private String name ;
    private Integer age ;
    private Author()
    {
    }
    public static Author init(String name, Integer age)
    {
        Author author = new Author() ;
        author.setAge(age) ;
        author.setName(name) ;
        return author ;
    }
    //省略 getter/setter/toString
}


```

这个类的特点就是构造方法是私有的，你没法从外面去 new，现在我想将这个类的对象注册到 Spring 容器中，那么我可以提供一个 AuthorFactoryBean：

```java
public class AuthorFactoryBean implements FactoryBean<Author>
{
    @Override public Author getObject() throws Exception
    {
        return Author.init("javaboy", 99) ;
    }
    @Override public Class<?> getObjectType()
    {
        return Author.class ;
    }
    @Override public boolean isSingleton()
    {
        return true ;
    }
}


```

然后在 Spring 容器中配置 AuthorFactoryBean 即可：

```xml
<bean class="org.javaboy.bean.AuthorFactoryBean" id="author"/>
```

接下来我们就可以从容器中去获取 Author 对象了，但是要注意，通过 author 这个名字拿到的是 Author 对象，而不是 AuthorFactoryBean 对象，如果想要获取到 AuthorFactoryBean 对象，那么要通过 &author 这个名字去获取（回顾第一小节所讲内容）。

```java
public class Main
{
    public static void main(String[] args)
    {
        ClassPathXmlApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml") ;
        Object author = ctx.getBean("author") ;
        Object authorFactoryBean = ctx.getBean("&author") ;
        System.out.println("author.getClass() = " + author.getClass()) ;
        System.out.println("authorFactoryBean.getClass() = " + authorFactoryBean.getClass()) ;
    }
}
```

来看下最终运行结果：

![](/assets/images/learning/spring/spring-beanfactory-factorybean-difference/b083a7104d1088dec6c89a6edfde7db9.png)

跟我们所想的一致吧～

## 小结

经过前面的介绍，相信小伙伴们已经能够区分 BeanFactory 和 FactoryBean 了，再来回顾一下本文开头的内容：

- BeanFactory 是 Spring 框架的核心接口之一，用于管理和获取应用程序中的 Bean 实例。它是一个工厂模式的实现，负责创建、配置和管理 Bean 对象。BeanFactory 是 Spring IoC 容器的基础，它可以从配置元数据（如 XML 文件）中读取 Bean 的定义，并在需要时实例化和提供这些 Bean。
- FactoryBean 是一个特殊的 Bean，它是一个工厂对象，用于创建和管理其他 Bean 的实例。FactoryBean 接口定义了一种创建 Bean 的方式，它允许开发人员在 Bean 的创建过程中进行更多的自定义操作。通过实现 FactoryBean 接口，开发人员可以创建复杂的 Bean 实例，或者在 Bean 实例化之前进行一些额外的逻辑处理。
