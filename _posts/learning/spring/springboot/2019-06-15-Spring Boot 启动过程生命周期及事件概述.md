---
layout: post
title: Spring Boot 启动过程（生命周期及事件）概述
author: deathwhispers
date: 2019-06-15
slug: spring-boot-startup-lifecycle-events
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2019-06-15 09:57
updated: 2019-06-15 09:57
week: 2019-W24
---

总结：

![f95fb74df31df5925fd9a14f57eac631](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/f95fb74df31df5925fd9a14f57eac631.png)

========================

详见正文：[SpringBoot生命周期事件——BAT的乌托邦](https://mp.weixin.qq.com/s?__biz=MzI0MTUwOTgyOQ%3D%3D&mid=2247483786&idx=1&sn=a5b22ff8a41d4f445e58214d20c83a8a&chksm=e90b3520de7cbc36ff213cc1a35e2717fe3db7973bd1a723ddcb37e15e690e04c4566e7e2c46&scene=178&cur_album_id=1914508501259730944#rd)

## 前言

本文将以SpringApplication的启动流程/生命周期各时期发出的Event事件为主线，结合每个生命周期内**完成的大事记**介绍，真正实现一文让你总览Spring Boot的全貌，这对你**深入理解Spring Boot，以及整合进Spring Cloud都将非常重要**。

为表诚意，本文一开始便把SpringApplication生命周期事件流程图附上，然后再精细化讲解各个事件的详情。

话外音：赶时间的小伙伴可以拿图走人?，但不建议白嫖哟

---

## 生命周期事件流程图

![7de8e3c5b020a2a6133d886718fbe5f0](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/7de8e3c5b020a2a6133d886718fbe5f0.png)

---

### 版本说明：

由于不同版本、类路径下存在不同包时结果会存在差异，不指明版本的文章都是不够负责任的。因此对导包/版本情况作出如下说明：

- Spring Boot
：2.2.2.RELEASE。有且仅导入
spring-boot-starter-web
和
spring-boot-starter-actuator
- Spring Cloud
：Hoxton.SR1。有且仅导入
spring-cloud-context
（注意：并非spring-cloud-starter，并不含有spring-cloud-commons哦）

总的来说：本例导包是非常非常“干净”的，这样在流程上才更有说服力嘛~

---

## SpringApplicationEvent

它是和SpringApplication生命周期有关的**所有事件**的父类，@since 1.0.0。

```java
public abstract class SpringApplicationEvent extends ApplicationEvent {
    private final String[] args;

    public SpringApplicationEvent(SpringApplication application, String[] args) {
        super(application);
        this.args = args;
    }

    public SpringApplication getSpringApplication() {
        return (SpringApplication) getSource();
    }

    public final String[] getArgs() {
        return this.args;
    }
}



```

它是抽象类，扩展自Spring Framwork的ApplicationEvent，确保了事件和应用实体SpringApplication产生关联（当然还有String[] args）。它有如下实现子类（7个）：

![fb3c041df978421ec6568e469dceff27](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/fb3c041df978421ec6568e469dceff27.png)

每个事件都代表着SpringApplication不同生命周期所处的位置，下面分别进行讲解。

---

### ApplicationStartingEvent：开始启动中

@since 1.5.0，并非1.0.0就有的哦。不过现在几乎没有人用1.5以下的版本了，所以可当它是标准事件。

---

### 完成的大事记

- SpringApplication
实例已实例化：
new SpringApplication(primarySources)
    - 它在实例化阶段完成了如下几件“大”事：
        - 推断出应用类型
webApplicationType
、main方法所在类
        - 给字段initializers赋值：拿到SPI方式配置的
ApplicationContextInitializer
上下文初始化器
            -
![d5af3fb8c6d1cedf3dc7cf1eb8582f3b](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/d5af3fb8c6d1cedf3dc7cf1eb8582f3b.png)
        - 给字段listeners赋值：拿到SPI方式配置的
ApplicationListener
应用监听器
            -
![d5e8fc8b0226ce66530dd4bc198c01fd](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/d5e8fc8b0226ce66530dd4bc198c01fd.png)
    - 注意：在此阶段(早期阶段)不要过多地使用它的内部状态，因为它可能在生命周期的后期被修改（话外音：使用时需谨慎）
- 此时，
SpringApplicationRunListener
已实例化：它通过SPI方式指定
org.springframework.boot.SpringApplicationRunListener=org.springframework.boot.context.event.EventPublishingRunListener
    - 若你有自己的运行时应用监听器，使用相同方式配置上即可，均会生效
- 由于
EventPublishingRunListener
已经实例化了，因此在后续的事件发送中，均能够触发对应的监听器的执行
- 发送ApplicationStartingEvent事件，触发对应的监听器的执行

---

### 监听此事件的监听器们

默认情况下，有4个监听器监听

ApplicationStartingEvent

事件：

![d4ca86e89d06350786a4570137482fcc](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/d4ca86e89d06350786a4570137482fcc.png)

1. LoggingApplicationListener
：@since 2.0.0。对日志系统抽象
LoggingSystem
执行实例化以及初始化之前的操作，默认使用的是基于Logback的
LogbackLoggingSystem
2. BackgroundPreinitializer**预热**
：启动一个后台进行对一些类进行
。如
ValidationInitializer、JacksonInitializer…
，因为这些组件有第一次惩罚的特点（并且首次初始化均还比较耗时），所以使用后台线程先预热效果更佳
3. DelegatingApplicationListener
：它监听的是
ApplicationEvent
，而实际上只会
ApplicationEnvironmentPreparedEvent
到达时生效，所以此处忽略
4. LiquibaseServiceLocatorApplicationListener
：略

总结：此事件节点结束时， SpringApplication完成了一些实例化相关的动作：本实例实例化、本实例属性赋值、日志系统实例化等。

---

### ApplicationEnvironmentPreparedEvent：环境已准备好

@since 1.0.0。该事件节点是最为重要的一个节点之一，因为对于Spring应用来说，环境抽象Enviroment简直太重要了，它是最为基础的**元数据**，决定着程序的构建和走向，所以构建的时机是比较早的。

---

### 完成的大事记

- 封装命令行参数（main方法的args）到
ApplicationArguments
里面
- 创建出一个环境抽象实例
ConfigurableEnvironment
的实现类，并且填入值：Profiles配置和Properties属性，默认内容如下（注意，这只是初始状态，后面还会改变、添加属性源，实际见最后的截图）：

![5611003df0ba4001c71f4017af549b9f](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/5611003df0ba4001c71f4017af549b9f.png)

- 发送ApplicationEnvironmentPreparedEvent事件，触发对应的监听器的执行
    - 对环境抽象Enviroment的**填值**
，均是由监听此事件的监听器去完成，见下面的监听器详解
- bindToSpringApplication(environment)
：把环境属性中
spring.main.xxx = xxx
绑定到当前的SpringApplication实例属性上，如常用的
spring.main.allow-bean-definition-overriding=true
会被绑定到当前
SpringApplication
实例的对应属性上

---

### 监听此事件的监听器们

默认情况下，有9个监听器监听 ApplicationEnvironmentPreparedEvent 事件：

![c3025ebaf4e5afa92e8ff6e10b9907cf](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/c3025ebaf4e5afa92e8ff6e10b9907cf.png)

5. BootstrapApplicationListener
：来自SC。优先级最高，用于启动/创建Spring Cloud的应用上下文。需要注意的是：到此时SB的上下文
ApplicationContext
还并没有创建哦。这个流程“嵌套”特别像Bean初始化流程：初始化Bean A时，遇到了Bean B，就需要先去完成Bean B的初始化，再回头来继续完成Bean A的步骤。
- 说明：在创建SC的应用的时候，使用的也是
SpringApplication#run()
完成的（非web），因此也会走下一整套SpringApplication的生命周期逻辑，所以请你务必区分。
    - 特别是这种case会让“绝大多数”初始化器、监听器等执行多次，若你有那种只需要执行一次的需求（比如只想让SB容器生命周期内执行，SC生命周期不执行），**请务必自行处理**
，否则会被执行多次而带来不可预知的结果
- SC应用上下文读取的外部化配置文件名默认是：
bootstrap
，使用的也是
ConfigFileApplicationListener
完成的加载/解析
6. LoggingSystemShutdownListener
：来自SC。对
LogbackLoggingSystem
先清理，再重新初始化一次，效果同上个事件，相当于重新来了一次，毕竟现在有Enviroment环境里嘛
7. ConfigFileApplicationListener**它也许是最重要的一个监听器**
：@since 1.0.0。
。做了如下事情：
- 加载SPI配置的所有的
EnvironmentPostProcessor
实例，并且排好序。需要注意的是：
ConfigFileApplicationListener
也是个
EnvironmentPostProcessor
，会参与排序哦

![130438f1ca3da2e23920ea2fa67ac73c](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/130438f1ca3da2e23920ea2fa67ac73c.png)

- **排好序后**
，分别一个个的执行
EnvironmentPostProcessor
（@since 1.3.0，并非一开始就有），介绍如下：
    - SystemEnvironmentPropertySourceEnvironmentPostProcessor
：@since 2.0.0。把
SystemEnvironmentPropertySource
替换为其子类
OriginAwareSystemEnvironmentPropertySource
（属性值带有Origin来源），仅此而已
    - SpringApplicationJsonEnvironmentPostProcessor
：@since 1.3.0。把环境中
spring.application.json=xxx
值解析成为一个
MapPropertySource
属性源，然后放进环境里面去（属性源的位置是做了处理的，一般不用太关心）
    - 可以看到，SB是直接支持JSON串配置的哦。Json解析参见：
JsonParser
    - CloudFoundryVcapEnvironmentPostProcessor
：@since 1.3.0。略
    - ConfigFileApplicationListener
：@since 1.0.0（它比EnvironmentPostProcessor先出现的哦）。加载
application.properties/yaml
等外部化配置，解析好后放进环境里（这应该是最为重要的）。
    - 外部化配置默认的优先级为：
“classpath:/,classpath:/config/,file:./,file:./config/”
。当前工程下的config目录里的application.properties优先级最高，当前工程类路径下的application.properties优先级最低
    - 值得强调的是：bootstrap.xxx也是由它负责加载的，处理规则一样
    - DebugAgentEnvironmentPostProcessor
：@since 2.2.0。处理和
reactor
测试相关，略
8. AnsiOutputApplicationListener
：@since 1.2.0。让你的终端（可以是控制台、可以是日志文件）支持Ansi彩色输出，使其更具可读性。当然前提是你的终端支持ANSI显示。参考类：
AnsiOutput
。你可通过
spring.output.ansi.enabled = xxx
配置，可选值是：
DETECT/ALWAYS/NEVER
，一般不动即可。另外，针对控制台可以单独配置：
spring.output.ansi.console-available = true/false
9. LoggingApplicationListener
：@since 2.0.0。根据Enviroment环境完成
initialize()
初始化动作：日志等级、日志格式模版等
- 值得注意的是：它这步相当于在ApplicationStartingEvent事件基础上进一步完成了初始化（上一步只是实例化）
10. ClasspathLoggingApplicationListener
：@since 2.0.0。用于把classpath路径以
log.debug()
输出，略
11. 值得注意的是：classpath类路径是有N多个的
Arrays.toString(((URLClassLoader) classLoader).getURLs())
，也就是说每个.jar里都属于classpath的范畴
12. 当然喽，你需要注意Spring在处理类路径时：**
classpath和classpath*的区别
~，这属于基础知识
13. BackgroundPreinitializer
：本事件达到时无动作
14. DelegatingApplicationListener
：执行通过外部化配置
context.listener.classes = xxx,xxx
的监听器们，然后把该事件广播给他们，关心此事件的监听器执行
- 这麽做的好处：可以通过属性文件外部化配置监听器，而不一定必须写在
spring.factories
里，更具弹性
- 外部化配置的执行优先级，还是相对较低的，到这里才给与执行嘛
15. FileEncodingApplicationListener
：检测当前系统环境的file.encoding和spring.mandatory-file-encoding设置的值是否一样,如果不一样则抛出异常如果不配置spring.mandatory-file-encoding则不检查

总结：此事件节点结束时，Spring Boot的环境抽象Enviroment已经准备完毕，但此时其上下文ApplicationContext还**没有创建**，但是Spring Cloud的应用上下文（引导上下文）已经**全部初始化完毕哦**，所以SC管理的外部化配置也应该都进入到了SB里面。如下图所示（这是基本上算是Enviroment的最终态了）：

![dfcdc7939e1078fb4fba2ac143fb7542](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/dfcdc7939e1078fb4fba2ac143fb7542.png)

小提示：SC配置的优先级是高于SB管理的外部化配置的。例如针对spring.application.name这个属性，若bootstrap里已配置了值，再在application.yaml里配置其实就无效了，因此生产上建议不要写两处。

---

### ApplicationContextInitializedEvent：上下文已实例化

@since 2.1.0，非常新的一个事件。当SpringApplication的上下文ApplicationContext准备好**后**，对单例Bean们实例化之**前**，发送此事件。所以此事件又可称为：contextPrepared事件。

---

### 完成的大事记

- printBanner(environment)
：打印Banner图，默认打印的是Spring Boot字样
- spring.main.banner-mode = xxx
来控制Banner的输出，可选值为
CONSOLE/LOG/OFF
，一般默认就好
- 默认在类路径下放置一个
banner.txt
文件，可实现自定义Banner。关于更多自定义方式，如使用图片、gif等，本处不做过多介绍
    - 小建议：别花里胡哨搞个佛祖在那。让它能自动打印输出**当前应用名**
，这样才是最为实用，最高级的（但需要你定制化开发，并且支持可配置，最好对使用者无感，属于一个common组件）
- 根据是否是web环境、是否是REACTIVE等，用空构造器创建出一个
ConfigurableApplicationContext
上下文实例（因为使用的是空构造器，所以不会立马“启动”上下文）
    - SERVLET -> AnnotationConfigServletWebServerApplicationContext
    - REACTIVE -> AnnotationConfigReactiveWebServerApplicationContext
    - 非web环境 -> AnnotationConfigApplicationContext（SC应用的容器就是使用的它）
- 既然上下文实例已经有了，那么就开始对它进行一些参数的设置：
    - 首先**最重要的**
便是把已经准备好的环境Enviroment环境设置给它
    - 设置些beanNameGenerator、resourceLoader、ConversionService等组件
    - 实例化所有的
ApplicationContextInitializer
上下文初始化器，并且排序好后挨个执行它（这个很重要），默认有如下截图这些初始化器此时要执行：

![18f2191040c0116969d194cc0c66394d](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/18f2191040c0116969d194cc0c66394d.png)

下面对这些初始化器分别做出简单介绍：

16. BootstrapApplicationListener.AncestorInitializer
：来自SC。用于把SC容器设置为SB容器的父容器。当然实际操作委托给了此方法：
new ParentContextApplicationContextInitializer(this.parent).initialize(context)
去完成
17. BootstrapApplicationListener.DelegatingEnvironmentDecryptApplicationInitializer
：来自SC。代理了下面会提到的
EnvironmentDecryptApplicationInitializer
，也就是说在此处就会先执行，用于提前解密Enviroment环境里面的属性，如相关URL等
18. PropertySourceBootstrapConfiguration**若想自定义配置中心必须了解它**
：来自SC。重要，和配置中心相关，
。主要作用是
PropertySourceLocator
属性源定位器，我会把它放在配置中心章节详解
19. EnvironmentDecryptApplicationInitializer
：来自SC。属性源头通过上面加载回来了，通过它来实现解密
- 值得注意的是：它被执行了两次哦~
5.
DelegatingApplicationContextInitializer
：和上面的
DelegatingApplicationListener
功能类似，支持外部化配置
context.initializer.classes = xxx,xxx
6.
SharedMetadataReaderFactoryContextInitializer
：略
7.
ContextIdApplicationContextInitializer
：@since 1.0.0。设置应用ID ->
applicationContext.setId()
。默认取值为
spring.application.name
，再为application，再为自动生成
8.
ConfigurationWarningsApplicationContextInitializer
：@since 1.2.0。对错误的配置进行警告（不会终止程序），以warn()日志输出在控制台。默认内置的只有对包名的检查：若你扫包含有
“org.springframework”/“org”
这种包名就警告
    - 若你想自定义检查规则，请实现
Check
接口，然后…
9.
RSocketPortInfoApplicationContextInitializer
：@since 2.2.0。暂略
10.
ServerPortInfoApplicationContextInitializer
：@since 2.0.0。将自己作为一个监听器注册到上下文
ConfigurableApplicationContext
里，专门用于监听
WebServerInitializedEvent
事件（非SpringApplication的生命周期事件）
    - 该事件有两个实现类：
ServletWebServerInitializedEvent
和
ReactiveWebServerInitializedEvent
。发送此事件的时机是
WebServer
已启动完成，所以已经有了监听的端口号
    - 该监听器做的事有两个：
    -
“local.” + getName(context.getServerNamespace()) + “.port”
作为key（默认值是
local.server.port
），value是端口值。这样可以通过@Value来获取到本机端口了（但貌似端口写0的时候，SB在显示上有个小bug）
    - 作为一个属性源
MapPropertySource
放进环境里，属性源名称为：
server.ports
（因为一个server是可以监听多个端口的，所以这里用复数）
- ConditionEvaluationReportLoggingListener
：将
ConditionEvaluationReport
报告（自动配置中哪些匹配了，哪些没匹配上）写入日志，当然只有
LogLevel#DEBUG
时才会输出（注意：这不是日志级别哦，应该叫报告级别）。如你配置
debug=true
就开启了此自动配置类报告
- 槽点：它明明是个初始化器，为毛命名为Listener？
- 发送ApplicationContextInitializedEvent事件，触发对应的监听器的执行

---

### 监听此事件的监听器们

默认情况下，有2个监听器监听ApplicationContextInitializedEvent事件：

![61c2418d85a0380c1332337bd92ed9ec](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/61c2418d85a0380c1332337bd92ed9ec.png)

20. BackgroundPreinitializer
：本事件达到时无动作
21. DelegatingApplicationListener
：本事件达到时无动作

总结：此事件节点结束时，完成了应用上下文ApplicationContext的准备工作，**并且执行所有注册的上下文初始化器ApplicationContextInitializer**。但是此时，单例Bean是仍旧还没有初始化，并且WebServer也还没有启动

---

### ApplicationPreparedEvent：上下文已准备好

@since 1.0.0。截止到上个事件ApplicationContextInitializedEvent，应用上下文ApplicationContext充其量叫**实例化**好了，但是还剩下很重要的事没做，这便是本周期的内容。

---

### 完成的大事记

- 把applicationArguments、printedBanner等都作为一个Bean放进Bean工厂里（因此你就可以@Autowired注入的哦）
    - 比如：有了Banner这个Bean，你可以在你任何想要输出的地方输出一个Banner，而不仅仅是启动时只会输出一次了
- 若
lazyInitialization = true
延迟初始化，那就向Bean工厂放一个：
new LazyInitializationBeanFactoryPostProcessor()
    - 该处理器@since 2.2.0。该处理器的作用是：对所有的Bean（通过
LazyInitializationExcludeFilter
接口指定的排除在外）全部
.setLazyInit(true);
延迟初始化
- 根据primarySources和allSources，交给
BeanDefinitionLoader
（SB提供的实现）实现加载Bean的定义信息，它支持4种加载方式（4种源）：
    - AnnotatedBeanDefinitionReader
-> 基于注解
    - XmlBeanDefinitionReader
-> 基于xml配置
    - GroovyBeanDefinitionReader
-> Groovy文件
    - ClassPathBeanDefinitionScanner
-> classpath中加载
    - (不同的源使用了不同的load加载方式)
- 发送ApplicationPreparedEvent事件，触发对应的监听器的执行

---

### 监听此事件的监听器们

默认情况下，有6个监听器监听ApplicationContextInitializedEvent事件：

![3e9433cdc6e43af7f8badc0c68935ac8](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/3e9433cdc6e43af7f8badc0c68935ac8.png)

22. CloudFoundryVcapEnvironmentPostProcessor
：略
23. ConfigFileApplicationListener
：向上下文注册一个
new PropertySourceOrderingPostProcessor(context)
。它的作用是：Bean工厂结束后对环境里的属性源进行重排序 -> 把名字叫
defaultProperties
的属性源放在最末位
- 该属性源是通过
SpringApplication#setDefaultProperties
API方式放进来的，一般不会使用到，留个印象即可
24. LoggingApplicationListener
：因为这时已经有Bean工厂了嘛，所以它做的事是：向工厂内放入Bean
- “springBootLoggingSystem” -> loggingSystem
- “springBootLogFile” -> logFile
- “springBootLoggerGroups” -> loggerGroups
25. BackgroundPreinitializer
：本事件达到时无动作
26. RestartListener
：SC提供。把当前最新的上下文缓存起来而已，目前并未发现有实质性作用，可忽略
27. DelegatingApplicationListener
：本事件达到时无动作

总结：此事件节点结束时，应用上下文ApplicationContext**初始化**完成，该赋值的赋值了，Bean定义信息也已全部加载完成。但是，单例Bean还没有被实例化，web容器依旧还没启动。

---

### ApplicationStartedEvent：应用成功启动

@since 2.0.0。截止到此，应用已经**准备就绪**，并且通过监听器、初始化器等完成了非常多的工作了，但仍旧剩下**被认为最为重要的**初始化单例Bean动作还没做、web容器（如Tomcat）还没启动，这便是这个周期所要做的事。

---

### 完成的大事记

- 启动Spring容器：
AbstractApplicationContext#refresh()
，这个步骤会做很多事，比如会实例化单例Bean
    - 该步骤属于Spring Framework的核心内容范畴，做了很多事，请参考Spring核心技术内容章节
    - 在Spring容器refresh()启动完成后，**成功监听到对应端口(们)**
WebServer
也随之完成启动，
- 输出启动成功的日志：
Started Application in xxx seconds (JVM running for xxx)
- 发送ApplicationStartedEvent事件，触发对应的监听器的执行
- callRunners()
：依次执行容器内配置的
ApplicationRunner/CommandLineRunner
的Bean实现类，支持sort排序
- ApplicationRunner
：@since 1.3.0，入参是
ApplicationArguments
，先执行（推荐使用）
- CommandLineRunner
：@since 1.0.0，入参是
String… args
，后执行（不推荐使用）

---

### 监听此事件的监听器们

默认情况下，有3个监听器监听ApplicationStartedEvent事件：

![422f4f8c25e901af1e3d456fcc0a688e](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/422f4f8c25e901af1e3d456fcc0a688e.png)

28. 前两个不用再解释了吧：本事件达到时无动作
29. TomcatMetricsBinder
：@since 2.1.0。和监控相关：将你的tomcat指标信息
TomcatMetrics
绑定到
MeterRegistry
，从而就能收集到相关指标了

总结：此事件节点结束时，SpringApplication的生命周期到这一步，**正常的启动流程**就全部完成了。也就说Spring Boot应用可以正常对对外提供服务了。

---

### ApplicationReadyEvent：应用已准备好

@since 1.3.0。该事件所处的生命周期可认为基本同ApplicationStartedEvent，仅是在其后执行而已，两者中间并无其它特别的动作，但是监听此事件的监听器们还是**蛮重要的**。

---

### 完成的大事记

同上。

---

### 监听此事件的监听器们

默认情况下，有4个监听器监听ApplicationStartedEvent事件：

![4b88876b85aebf6e254f05f538c79ee2](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/4b88876b85aebf6e254f05f538c79ee2.png)

30. SpringApplicationAdminMXBeanRegistrar
：当此事件到达时，告诉Admin Spring应用已经ready，可以使用啦。
31. 中间这两个不用再解释了吧：本事件达到时无动作
32. RefreshEventListener
：当此事件到达时，告诉Spring应用已经ready了，接下来便可以执行
ContextRefresher.refresh()
喽

总结：此事件节点结束时，应用已经完完全全的准备好了，并且也已经完成了相关组件的周知工作。

---

### 异常情况

SpringApplication是有可能在启动的时候失败（如端口号已被占用），当然任何一步骤遇到异常时交给SpringApplication#handleRunFailure()方法来处理，这时候也会有对应的事件发出。

---

### ApplicationFailedEvent：应用启动失败

当SpringApplication在启动时抛出异常：可能是端口绑定、也可能是你自定义的监听器你写了个bug等，就会“可能”发送此事件。

---

### 完成的大事记

- 得到异常的退出码ExitCode，然后发送
ExitCodeEvent
事件（非生命周期事件）
- 发送
ApplicationFailedEvent
事件，触发对应的监听器的执行

---

### 监听此事件的监听器们

默认情况下，有6个监听器监听ApplicationStartedEvent事件：

![0c2750122cf92a2f2bb99c5dfcde42ef](/assets/images/learning/spring/springboot/spring-boot-startup-lifecycle-events/0c2750122cf92a2f2bb99c5dfcde42ef.png)

33. LoggingApplicationListener
：执行
loggingSystem.cleanUp()
清理资源
34. ClasspathLoggingApplicationListener
：输出一句debug日志：
Application failed to start with classpath: …
35. 中间这两个不用再解释了吧：本事件达到时无动作
36. ConditionEvaluationReportLoggingListener
：自动配置输出报告，输出错误日志呗：特别方便你查看和错误定位
- 不得不夸：SB对错误定位这块才真叫智能，比Spring Framework好用太多了
37. BootstrapApplicationListener.CloseContextOnFailureApplicationListener
：执行context.close()

总结：此事件节点结束时，会做一些释放资源的操作。一般情况下：我们并不需要监听到此事件

---

# 总结

关于SpringApplication的生命周期体系的介绍就到这了，相信通过此“万字长文”你能体会到A哥的用心。翻了翻市面上的相关文章，本文Almost可以保证是总结得最到位的，让你通过一文便可从大的方面基本掌握Spring Boot，这不管是你使用SB，还是后续自行扩展、精雕细琢SB，以及去深入了解Spring Cloud均由非常重要的意义，希望对你有帮助，谢谢你的三连。
