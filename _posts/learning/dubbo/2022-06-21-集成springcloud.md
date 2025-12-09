---
layout: post
title: 集成SpringCloud
slug: dubbo-integration-spring-cloud
type:
  - note
date: 2022-06-21
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-06-21 11:52
updated: 2022-06-21 18:33
---

# 1. 概述

本文，我们来分享 [Spring Cloud Alibaba Dubbo](https://github.com/spring-cloud-incubator/spring-cloud-alibaba/tree/master/spring-cloud-alibaba-dubbo) 项目的源码解析，看看 Dubbo 是如何集成到 Spring Cloud 中的。

Spring Cloud 和 Dubbo 一直不是竞争的关系，胖友要好好理解哟。

目前 Spring Cloud Alibaba Dubbo 暂时没有文档，不过不用担心，艿艿会先教你搭建一个示例，同时它也是我们后面用来调试的示例。

# 2. 调试环境搭建

在读源码之前，我们当然是先把调试环境搭建起来。

## 2.1 依赖工具

- JDK ：1.8+
- Maven
- IntelliJ IDEA

## 2.2 源码拉取

从官方仓库 [https://github.com/spring-cloud-incubator/spring-cloud-alibaba](https://github.com/spring-cloud-incubator/spring-cloud-alibaba)Fork 出属于自己的仓库。为什么要 Fork ？既然开始阅读、调试源码，我们可能会写一些注释，有了自己的仓库，可以进行自由的提交。

使用 IntelliJ IDEA 从 Fork 出来的仓库拉取代码。拉取完成后，Maven 会下载依赖包，可能会花费一些时间，耐心等待下。

---

考虑到方便，我们直接使用

spring-cloud-alibaba-dubbo

项目提供的示例，就在它的

test

测试目录下，如下图所示：

![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/436c928a486b1c09e7325f33e361add3.jpg)

示例项目

另外，本文使用的 spring-cloud-alibaba 版本是 0.2.2.BUILD-SNAPSHOT 。

## 2.3 启动 Nacos

因为后面我们会使用 Nacos 作为注册中心和配置中心，所以需要启动它。具体的，参考艿艿在 [《Nacos 实现原理与源码解析系统 —— 精品合集》](http://www.iocoder.cn/Nacos/the-tutorial/) 的 [「2. 快速开始」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#) 小节。

## 2.4 启动示例

右键 DubboSpringCloudBootstrap 类的 #main(String[] args) 方法，直接运行即可。 如果你没有看到任何异常输出，说明就已经成功了。

另外，这个示例，即做了服务消费者，又做了服务提供者。

下面，让我们让我们逐步解释示例中的每个类和配置文件。

### 2.4.1 bootstrap.yaml

```plain text
plain spring:   application:     name: spring-cloud-alibaba-dubbo   cloud:     nacos:       discovery:         server-addr: 127.0.0.1:8848       config:         server-addr: 127.0.0.1:8848  eureka:   client:     enabled: false  --- spring:   profiles: eureka   cloud:     nacos:       discovery:         enabled: false         register-enabled: false  eureka:   client:     enabled: true     service-url:       defaultZone: http://127.0.0.1:8761/eureka/
```

---

- Eureka 相关的配置，可以无视，因为我们使用的是 Nacos 作为注册中心。
- spring.application.name
，配置了应用名。
- spring.cloud.nacos.discovery.server-addr
，配置了 Nacos 作为注册中心。
- spring.cloud.nacos.config.server-addr
，配置了 Nacos 作为配置中心。

### 2.4.2 application.yaml

```plain text
plain dubbo:   scan:     base-packages: org.springframework.cloud.alibaba.dubbo.service # 扫描指定包，生成对应的 @Service 和 @Reference Bean 对象   protocols:     dubbo:       name: dubbo # Dubbo 协议       port: 12345 # Dubbo 协议的端口     rest:       name: rest # REST 协议       port: 9090 # REST 协议的端口       server: netty # 使用 Netty 作为 HTTP Server   registry:     address: spring-cloud://nacos # Dubbo 注册中心  feign:   hystrix:     enabled: true # 开启 Hystrix 功能，可以熔断落  server:   port: 8080 # HTTP API 端口
```

---

- 每个配置，看看其后的配置文件。

### 2.4.3 EchoService

org.springframework.cloud.alibaba.dubbo.service.EchoService ，EchoService 接口。代码如下：

```plain text
plain // EchoService.java  public interface EchoService {      String echo(String message);      String plus(int a, int b);  }
```

---

- 熟悉不能在熟悉的 Dubbo Service 接口的代码~

### 2.4.4 DefaultEchoService

org.springframework.cloud.alibaba.dubbo.service.DefaultEchoService ，实现 EchoService 接口，默认的 EchoService 实现者，服务提供者。代码如下：

```plain text
plain // DefaultEchoService.java  @Service(version = "1.0.0", protocol = {"dubbo", "rest"}) @RestController @Path("/") public class DefaultEchoService implements EchoService {      @Override     @GetMapping(value = "/echo" //            consumes = MediaType.APPLICATION_JSON_VALUE, //            produces = MediaType.APPLICATION_JSON_UTF8_VALUE     )     @Path("/echo")     @GET //    @Consumes("application/json") //    @Produces("application/json;charset=UTF-8")     public String echo(@RequestParam @QueryParam("message") String message) {         System.out.println(message);         return RpcContext.getContext().getUrl() + " [echo] : " + message;     }      @Override     @PostMapping("/plus")     @Path("/plus")     @POST     public String plus(@RequestParam @QueryParam("a") int a, @RequestParam @QueryParam("b") int b) {         return null;     }  }
```

---

- @Service(version = “1.0.0”, protocol = {“dubbo”, “rest”})
注解，提供 Dubbo 和 Rest 两种协议的服务。

### 2.4.5 DubboSpringCloudBootstrap

org.springframework.cloud.alibaba.dubbo.bootstrap.DubboSpringCloudBootstrap ，示例的 Spring Boot 启动器。代码如下：

```plain text
plain // DubboSpringCloudBootstrap.java  @EnableDiscoveryClient // 开启注册发现 @EnableAutoConfiguration // 开启自动配置 @EnableFeignClients // 开启 Feign Client @RestController public class DubboSpringCloudBootstrap {      @Reference(version = "1.0.0")     private EchoService echoService;      @Autowired     @Lazy     private FeignEchoService feignEchoService;      @Autowired     @Lazy     private DubboFeignEchoService dubboFeignEchoService;      public static void main(String[] args) {         new SpringApplicationBuilder(DubboSpringCloudBootstrap.class)                 .run(args);     }  }
```

---

- @EnableDiscoveryClient
注解，用于开启注册发现 Client 的功能。
- @EnableAutoConfiguration
注解，用于开启自动配置。
- @EnableFeignClients
注解，开启 Feign Client 。在
spring-cloud-alibaba-dubbo
项目中，使用 Feign 作为服务消费者。
- @RestController
注解，后续我们会看到这个类中会提供基于 Spring MVC 的 HTTP API 接口。
- echoService
属性，使用
@Reference(version = “1.0.0”)
注解，引入 Dubbo 服务。这个方式，就是我们原先在 Dubbo 中就使用的。
- feignEchoService
属性，使用标准的 Feign Client 作为服务消费者，它使用 RestTemplate 调用的是 Dubbo 提供的 Rest 接口。代码如下：

```plain text
plain // DubboSpringCloudBootstrap.java  @FeignClient("spring-cloud-alibaba-dubbo") public interface FeignEchoService {      @GetMapping(value = "/echo")     String echo(@RequestParam("message") String message);  }
```

---

- dubboFeignEchoService
属性，也使用标准的 Feign Client 作为服务消费者，它调用 Dubbo 调用的是 Dubbo 提供的 Dubbo 接口。代码如下：

```plain text
plain // DubboSpringCloudBootstrap.java  @FeignClient("spring-cloud-alibaba-dubbo") public interface DubboFeignEchoService {      @GetMapping(value = "/echo")     @DubboTransported     String echo(@RequestParam("message") String message);  }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">相比 </font><font style="color:rgb(51, 51, 51);">echoService</font><font style="color:rgb(51, 51, 51);"> 属性，它在方法上，增加了 </font><font style="color:rgb(51, 51, 51);">org.springframework.cloud.alibaba.dubbo.annotation.@DubboTransported</font><font style="color:rgb(51, 51, 51);"> 注解。</font>
- <font style="color:rgb(51, 51, 51);">可能会有胖友好奇，具体是如何实现的呢？本文我们一起来揭晓~</font>
```

---

```plain text
plain // DubboSpringCloudBootstrap.java  @Bean public ApplicationRunner applicationRunner() {     return arguments -> {         // Dubbo Service call         System.out.println(echoService.echo("mercyblitz"));         // Spring Cloud Open Feign REST Call         System.out.println(feignEchoService.echo("mercyblitz"));         // Spring Cloud Open Feign REST Call (Dubbo Transported)         System.out.println(dubboFeignEchoService.echo("mercyblitz"));     }; }
```

---

- 声明了 ApplicationRunner Bean 对象，在 Spring Boot 启动完成，直接发起相应的调用。它的目的是，看看三种调用方式，是否都正常。如果没有报错，说明都是 OK 的。

---

```plain text
plain // DubboSpringCloudBootstrap.java  @GetMapping(value = "/dubbo/call/echo") public String dubboEcho(@RequestParam("message") String message) {     return echoService.echo(message); }  @GetMapping(value = "/feign/call/echo") public String feignEcho(@RequestParam("message") String message) {     return feignEchoService.echo(message); }  @GetMapping(value = "/feign-dubbo/call/echo") public String feignDubboEcho(@RequestParam("message") String message) {     return dubboFeignEchoService.echo(message); }
```

---

- 声明了三个 Spring MVC HTTP API ，分别调用三个不同的服务消费者。
- 这就是为什么 DubboSpringCloudBootstrap 有
@RestController
注解，且配置文件中配置了
server.port=8080
。

至此，我们已经完整看过了 Spring Cloud Alibaba Dubbo 的示例，可以愉快的开始调试了。

# 3. 项目结构一览

本文主要分享 spring-cloud-alibaba-dubbo 的 **项目结构**。希望通过本文能让胖友对 spring-cloud-alibaba-dubbo 的整体项目有个简单的了解。

![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/8f4ff33aa74bfa4767ceb36ba7fdabd0.jpg)

项目结构一览

## 3.1 代码统计

这里先分享一个小技巧。笔者在开始源码学习时，会首先了解项目的代码量。

**第一种方式**，使用 [IDEA Statistic](https://plugins.jetbrains.com/plugin/4509-statistic) 插件，统计整体代码量。

![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/4bda762c7cf4cb78f049ecdd94b67abd.jpg)

Statistic 统计代码量

- 我们可以粗略的看到，整个 Spring Cloud Alibaba 的代码量在 16000 行。这其中还包括单元测试，示例等等代码。
- /(ㄒoㄒ)/~~ 显然，目前这个插件没办法很方便的统计出，我们想要看到的
spring-cloud-alibaba-dubbo
的代码量。

**第二种方式**，使用 [Shell 脚本命令逐个 Maven 模块统计](http://blog.csdn.net/yhhwatl/article/details/52623879) 。

一般情况下，笔者使用 find . -name “*.java”|xargs cat|grep -v -e ^$ -e ^//.*$|wc -l 。这个命令只过滤了**部分注释**，所以相比 [IDEA Statistic](https://plugins.jetbrains.com/plugin/4509-statistic) 会**偏多**。

当然，考虑到准确性，胖友需要手动 cd 到每个 Maven 项目的 src/main/java 目录下，以达到排除单元测试的代码量。

![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/efd42e35fa614326851f15781807add3.jpg)

Shell 脚本统计代码量

统计完后，发现代码量是不多的。

## 3.2 annotation 包

annotation 包，62 行代码，提供 @EnableFeignClients 注解。

## 3.3 autoconfigure 包

autoconfigure 包，172 行代码，提供 Spring Boot 自动配置 Spring Cloud Alibaba Dubbo 。

## 3.4 context 包

context 包，35 行代码，目前仅有 DubboServiceRegistrationApplicationContextInitializer 类，先不解释哈~

## 3.5 metadata 包

metadata 包，904 行代码，实现将 Spring Cloud Alibaba Dubbo 的服务的元数据，存储到配置中心。这样，后续使用 @DubboTransported 注解的 Dubbo 调用时，因为会使用到 [Dubbo的泛化调用](http://dubbo.apache.org/zh-cn/blog/dubbo-generic-invoke.html) ，有了服务的元数据，就可以愉快的调用了。

## 3.6 openfeign 包

openfeign 包，305 行代码，实现将 Dubbo 集成到 OpenFeign 中。

## 3.7 registry 包

registry 包，478 行代码，实现 Dubbo 使用 Spring Cloud Service 注册中心体系。可能这么说有点抽象，我们可以回过头看看 [「2.4.2 application.yaml」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#) 中看到，有个神奇的 dubbo.protocols.registry.address=spring-cloud://nacos 配置。

emm~哈哈哈，等会看具体代码，会更加明白。

# 4. annotation 包

## 4.1 @DubboTransported

org.springframework.cloud.alibaba.dubbo.annotation.@DubboTransported 注解，表名调用时，使用 Dubbo 作为底层 RPC 调用。代码如下：

```plain text
plain // DubboTransported.java  /**  * {@link DubboTransported @DubboTransported} annotation indicates that the traditional Spring Cloud Service-to-Service call is transported  * by Dubbo under the hood, there are two main scenarios:  * <ol>  * <li>{@link FeignClient @FeignClient} annotated classes:  * <ul>  * If {@link DubboTransported @DubboTransported} annotated classes, the invocation of all methods of  * {@link FeignClient @FeignClient} annotated classes.  * </ul>  * <ul>  * If {@link DubboTransported @DubboTransported} annotated methods of {@link FeignClient @FeignClient} annotated classes.  * </ul>  * </li>  * <li>{@link LoadBalanced @LoadBalanced} {@link RestTemplate} annotated field, method and parameters</li>  * </ol>  * <p>  *  * @see FeignClient  * @see LoadBalanced  */ @Retention(RetentionPolicy.RUNTIME) @Target(value = {ElementType.TYPE, ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER}) // 支持类、方法 @Documented public @interface DubboTransported {      /**      * The protocol of Dubbo transport whose value could be used the placeholder "dubbo.transport.protocol"      *      * 使用的 Dubbo 协议，默认为 "dubbo"      *      * @return the default protocol is "dubbo"      */     String protocol() default "${dubbo.transport.protocol:dubbo}";      /**      * The cluster of Dubbo transport whose value could be used the placeholder "dubbo.transport.cluster"      *      * 使用的集群容错方式，默认为 "failover"      *      * @return the default protocol is "failover"      */     String cluster() default "${dubbo.transport.cluster:failover}";  }
```

---

- protocol
属性，使用的 Dubbo 协议，默认为
“dubbo”
。
- cluster
属性，使用 使用的集群容错方式，默认为
“failover”
。
- 可标记在类或者方法上。

# 5. autoconfigure 包

在 META-INF/spring.factories 文件中，声明了三个自动配置类。代码如下：

```plain text
plain org.springframework.boot.autoconfigure.EnableAutoConfiguration=\   org.springframework.cloud.alibaba.dubbo.autoconfigure.DubboMetadataAutoConfiguration,\   org.springframework.cloud.alibaba.dubbo.autoconfigure.DubboOpenFeignAutoConfiguration,\   org.springframework.cloud.alibaba.dubbo.autoconfigure.DubboRestMetadataRegistrationAutoConfiguration
```

---

- 下面，我们逐个来瞅瞅。

## 5.1 DubboMetadataAutoConfiguration

org.springframework.cloud.alibaba.dubbo.autoconfigure.DubboMetadataAutoConfiguration ，Dubbo 元数据（Metadata）相关 Bean 的自动配置类。代码如下：

```plain text
plain // DubboMetadataAutoConfiguration.java  @Configuration @Import(DubboServiceMetadataRepository.class) // 创建了 DubboServiceMetadataRepository Bean 对象 public class DubboMetadataAutoConfiguration {      @Bean // 创建了 NacosMetadataConfigService Bean 对象     @ConditionalOnBean(NacosConfigProperties.class)     public MetadataConfigService metadataConfigService() {         return new NacosMetadataConfigService();     }  }
```

---

- 通过 [「7.5 DubboServiceMetadataRepository」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
@Import(DubboServiceMetadataRepository.class)
，创建了 DubboServiceMetadataRepository 对象。详细解析，见
。
- #metadataConfigService()[「7.4.1 NacosMetadataConfigService」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
方法，创建了 NacosMetadataConfigService Bean 对象。详细解析，见
。

## 5.2 DubboOpenFeignAutoConfiguration

org.springframework.cloud.alibaba.dubbo.autoconfigure.DubboOpenFeignAutoConfiguration ，Dubbo OpenFeign 相关 Bean 的自动配置类。代码如下：

```plain text
plain // DubboOpenFeignAutoConfiguration.java  @ConditionalOnClass(value = Feign.class) // 存在 Feign 类的时候，即存在 feign 依赖 @AutoConfigureAfter(FeignAutoConfiguration.class) // 在 FeignAutoConfiguration 配置类之后初始化 @Configuration public class DubboOpenFeignAutoConfiguration {      @Value("${spring.application.name}")     private String currentApplicationName;      @Bean // 创建 DubboServiceBeanMetadataResolver 对象     @ConditionalOnMissingBean     public MetadataResolver metadataJsonResolver(ObjectProvider<Contract> contract) {         return new DubboServiceBeanMetadataResolver(currentApplicationName, contract);     }      @Bean // 创建 TargeterBeanPostProcessor 对象     public TargeterBeanPostProcessor targeterBeanPostProcessor(Environment environment,                                                                DubboServiceMetadataRepository dubboServiceMetadataRepository) {         return new TargeterBeanPostProcessor(environment, dubboServiceMetadataRepository);     }  }
```

---

- #metadataJsonResolver(…)[「7.2 MetadataResolver」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
方法，创建 DubboServiceBeanMetadataResolver Bean 对象。详细解析，见
。
- #targeterBeanPostProcessor(…)[「8.1 TargeterBeanPostProcessor」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
方法，创建 TargeterBeanPostProcessor Bean 对象。详细解析，见
。

## 5.3 DubboRestMetadataRegistrationAutoConfiguration

org.springframework.cloud.alibaba.dubbo.autoconfigure.DubboRestMetadataRegistrationAutoConfiguration ，自动配置两个 Spring 事件监听器，将 Dubbo Rest 元数据（Metadata）注册到配置中心。代码如下：

```plain text
plain // DubboRestMetadataRegistrationAutoConfiguration.java  @ConditionalOnProperty(value = "spring.cloud.service-registry.auto-registration.enabled", matchIfMissing = true) // 要求有 "spring.cloud.service-registry.auto-registration.enabled=true" ，或者不配置。 @ConditionalOnBean(value = { // 要求存在 MetadataResolver、MetadataConfigService Bean 对象         MetadataResolver.class,         MetadataConfigService.class }) @AutoConfigureAfter(value = {DubboMetadataAutoConfiguration.class}) // 在 DubboMetadataAutoConfiguration 配置类之后初始化 @Configuration public class DubboRestMetadataRegistrationAutoConfiguration {      /**      * A Map to store REST metadata temporary, its' key is the special service name for a Dubbo service,      * the value is a JSON content of JAX-RS or Spring MVC REST metadata from the annotated methods.      *      * Dubbo Rest Service 方法的元数据（Metadata）集合      */     private final Set<ServiceRestMetadata> serviceRestMetadata = new LinkedHashSet<>();      @Autowired // 默认情况下，来自 DubboOpenFeignAutoConfiguration 注册的 DubboServiceBeanMetadataResolver Bean 对象     private MetadataResolver metadataResolver;      @Autowired // 默认情况下，来自 DubboMetadataAutoConfiguration 注册的 NacosMetadataConfigService Bean 对象     private MetadataConfigService metadataConfigService;      @EventListener(ServiceBeanExportedEvent.class)     public void recordRestMetadata(ServiceBeanExportedEvent event) throws JsonProcessingException {         ServiceBean serviceBean = event.getServiceBean();         serviceRestMetadata.addAll(metadataResolver.resolveServiceRestMetadata(serviceBean));     }      /**      * Pre-handle Spring Cloud application service registered:      * <p>      * Put <code>restMetadata</code> with the JSON format into      * {@link Registration#getMetadata() service instances' metadata}      * <p>      *      * @param event {@link InstancePreRegisteredEvent} instance      */     @EventListener(InstancePreRegisteredEvent.class)     public void registerRestMetadata(InstancePreRegisteredEvent event) throws Exception {         Registration registration = event.getRegistration();         metadataConfigService.publishServiceRestMetadata(registration.getServiceId(), serviceRestMetadata);     }  }
```

---

- serviceRestMetadata
属性，Dubbo Rest Service 方法的元数据（Metadata）集合。
- #recordRestMetadata(ServiceBeanExportedEvent)
方法，监听 ServiceBeanExportedEvent 事件。
    - 在每个 Dubbo 服务暴露后，会发布 ServiceBeanExportedEvent 事件。在 [《精尽 Dubbo 源码分析 —— 注解配置》](http://www.iocoder.cn/Dubbo/good-collection/)[「5.3.3 onApplicationEvent」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
的
中，我们有过详细解析。
    - 在接收到 ServiceBeanExportedEvent 事件，该方法会调用 [「7.5 DubboServiceBeanMetadataResolver」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
MetadataResolver#resolveServiceRestMetadata(ServiceBean serviceBean)
方法，获得该 ServiceBean 的 ServiceRestMetadata 集合，添加到
serviceRestMetadata
中。详细解析，见
。
- #registerRestMetadata(InstancePreRegisteredEvent)
方法，监听 InstancePreRegisteredEvent 事件。
    - InstancePreRegisteredEvent 事件，在 Spring Cloud 应用注册到注册中心之前，会触发该事件。详细的，可以看看 [《spring-cloud-commons reference》](https://www.jianshu.com/p/a8b255c9feae)[「2.2.1 ServiceRegistry Auto-Registration」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
文章的
小节。现在，可以不看~
    - 在接收到 InstancePreRegisteredEvent 事件，该方法会调用
MetadataConfigService#publishServiceRestMetadata(String serviceName, Set serviceRestMetadata)
方法，将每个 Dubbo 服务的 ServiceRestMetadata 元数据集合，发布（存储）到配置中心。
- 这样，后续的 Dubbo 泛化调用，就有 Dubbo 服务的元数据咧。

因为本小节讲的都是自动配置类，胖友可能会略有懵逼。不要慌，我们继续往下撸。

对咧，最好一边调试，一边看。

# 6. context 包

在 META-INF/spring.factories 文件中，声明了三个自动配置类。代码如下：

```plain text
plain org.springframework.context.ApplicationContextInitializer=\   org.springframework.cloud.alibaba.dubbo.context.DubboServiceRegistrationApplicationContextInitializer
```

---

## 6.1 DubboServiceRegistrationApplicationContextInitializer

org.springframework.cloud.alibaba.dubbo.context.DubboServiceRegistrationApplicationContextInitializer ，实现 ApplicationContextInitializer 接口，将 applicationContext 设置到 SpringCloudRegistryFactory.applicationContext 静态属性。代码如下：

```plain text
plain // SpringCloudRegistryFactory.java  /**  * The Dubbo services will be registered as the specified Spring cloud applications that will not be considered  * normal ones, but only are used to Dubbo's service discovery even if it is based on Spring Cloud Commons abstraction.  * However, current application will be registered by other DiscoveryClientAutoConfiguration.  *  */ public class DubboServiceRegistrationApplicationContextInitializer implements ApplicationContextInitializer<ConfigurableApplicationContext> {      @Override     public void initialize(ConfigurableApplicationContext applicationContext) {         // Set ApplicationContext into SpringCloudRegistryFactory before Dubbo Service Register         SpringCloudRegistryFactory.setApplicationContext(applicationContext);     }  }
```

---

# 7. metadata 包

在看具体代码之前，我们先在 Nacos 的配置中心界面，看看什么是 Dubbo Metadata 。如下图所示：

![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/3a506fda54fc3b7a7f2687b3aaf407b8.jpg)

Dubbo Metadata

可能这样还是不够清理，我们来看一个 Dubbo Service Metadata 更具体的示例，如下 JSON 串：

```plain text
plain {   "name" : "providers:dubbo:org.springframework.cloud.alibaba.dubbo.service.EchoService:1.0.0", // dubbo 协议   "meta" : [ { // 一个 Dubbo 方法     "method" : { // 方法信息       "name" : "echo",       "returnType" : "java.lang.String",       "params" : [ {         "index" : 0,         "name" : "message",         "type" : "java.lang.String"       } ]     },     "request" : { // 请求信息       "method" : "GET",       "url" : "/echo",       "queries" : {         "message" : [ "{message}" ]       },       "headers" : { }     },     "indexToName" : {       "0" : [ "message" ]     }   }, { // 一个 Dubbo 方法     "method" : { // 方法信息       "name" : "plus",       "returnType" : "java.lang.String",       "params" : [ {         "index" : 0,         "name" : "a",         "type" : "int"       }, {         "index" : 1,         "name" : "b",         "type" : "int"       } ]     },     "request" : { // 请求信息       "method" : "POST",       "url" : "/plus",       "queries" : {         "a" : [ "{a}" ],         "b" : [ "{b}" ]       },       "headers" : { }     },     "indexToName" : {       "0" : [ "a" ],       "1" : [ "b" ]     }   } ] }
```

---

- 

## 7.1 Metadata 类

在 metadata 包的根目录，一共有 6 个 Metadata 类。如下：

- ServiceRestMetadata
- RestMethodMetadata
- MethodMetadata
- MethodParameterMetadata
- RequestMetadata
- DubboTransportedMethodMetadata

### 7.1.1 ServiceRestMetadata

org.springframework.cloud.alibaba.dubbo.metadata.ServiceRestMetadata ，Service Rest Metadata 。代码如下：

```plain text
plain // ServiceRestMetadata.java  public class ServiceRestMetadata {      /**      * 服务名      */     private String name;     /**      * Rest 方法元数据      */     private Set<RestMethodMetadata> meta;      // ... 省略 setting/getting 方法 }
```

---

### 7.1.2 RestMethodMetadata

org.springframework.cloud.alibaba.dubbo.metadata.RestMethodMetadata ，Rest Method Metadata 。代码如下：

```plain text
plain // RestMethodMetadata.java  public class RestMethodMetadata {      /**      * 方法元数据      */     private MethodMetadata method;     /**      * 请求元数据      */     private RequestMetadata request;     /**      * TODO      */     private Map<Integer, Collection<String>> indexToName;      // ... 省略 setting/getting 方法 }
```

---

### 7.1.2.1 MethodMetadata

org.springframework.cloud.alibaba.dubbo.metadata.MethodMetadata ，Method Metadata 。代码如下：

```plain text
plain // ServiceRestMetadata.java  public class MethodMetadata {      /**      * 方法名      */     private String name;     /**      * 返回类型      */     private String returnType;     /**      * 方法参数元数据的数组      */     private List<MethodParameterMetadata> params;     /**      * 方法      */     @JsonIgnore // 不存储到配置中心     private Method method;      public MethodMetadata() {         this.params = new LinkedList<>();     }      public MethodMetadata(Method method) {         this.name = method.getName();         // 获得返回类型         this.returnType = ClassUtils.getName(method.getReturnType());         // 初始化 params         this.params = initParameters(method);         this.method = method;     }      private List<MethodParameterMetadata> initParameters(Method method) {         // 获得参数数量         int parameterCount = method.getParameterCount();         // 如果参数不存在，则返回空数组         if (parameterCount < 1) {             return Collections.emptyList();         }         // 创建 MethodParameterMetadata 数组         List<MethodParameterMetadata> params = new ArrayList<>(parameterCount);         Parameter[] parameters = method.getParameters();         for (int i = 0; i < parameterCount; i++) {             // 获得 Parameter 对象             Parameter parameter = parameters[i];             // 转换成 MethodParameterMetadata 对象             MethodParameterMetadata param = toMethodParameterMetadata(i, parameter);             // 添加到 params 中             params.add(param);         }         return params;     }      private MethodParameterMetadata toMethodParameterMetadata(int index, Parameter parameter) {         // 创建 MethodParameterMetadata 对象         MethodParameterMetadata metadata = new MethodParameterMetadata();         metadata.setIndex(index); // 方法参数的位置         metadata.setName(parameter.getName()); // 方法参数的名字         metadata.setType(parameter.getType().getTypeName()); // 方法参数的类型         return metadata;     }      // ... 省略 setting/getting 方法 }
```

---

### 7.1.2.1.1 MethodParameterMetadata

org.springframework.cloud.alibaba.dubbo.metadata.MethodParameterMetadata ，Method Parameter Metadata 。代码如下：

```plain text
plain // MethodParameterMetadata.java  public class MethodParameterMetadata {      /**      * 方法参数的位置      */     private int index;     /**      * 方法参数的名字      */     private String name;     /**      * 方法参数的类型      */     private String type;      // ... 省略 setting/getting 方法 }
```

---

### 7.1.2.2 RequestMetadata

org.springframework.cloud.alibaba.dubbo.metadata.RequestMetadata ，Request Metadata 。代码如下：

```plain text
plain // RequestMetadata.java  public class RequestMetadata {      /**      * 方法名      */     private String method;     /**      * URL 路径      */     private String url;      private Map<String, Collection<String>> queries;      private Map<String, Collection<String>> headers;      public RequestMetadata() {     }      // 将 RequestTemplate 对象，转换成 RequestMetadata 对象     public RequestMetadata(RequestTemplate requestTemplate) {         this.method = requestTemplate.method();         this.url = requestTemplate.url();         this.queries = requestTemplate.queries();         this.headers = requestTemplate.headers();     }      // ... 省略 setting/getting 方法 }
```

---

### 7.1.2.3 DubboTransportedMethodMetadata

org.springframework.cloud.alibaba.dubbo.metadata.DubboTransportedMethodMetadata ，继承 MethodMetadata 类， @DubboTransported 注解对应的 MethodMetadata 对象。代码如下：

```plain text
plain // DubboTransportedMethodMetadata.java  public class DubboTransportedMethodMetadata extends MethodMetadata {      /**      * Dubbo 协议      */     private String protocol;     /**      * Dubbo 容错策略      */     private String cluster;      // ... 省略 setting/getting 方法 }
```

---

## 7.2 MetadataResolver

org.springframework.cloud.alibaba.dubbo.metadata.resolver.MetadataResolver ，Metadata Resolver 元数据解析器接口。代码如下：

```plain text
plain // MetadataResolver.java  /**  * The REST metadata resolver  */ public interface MetadataResolver {      /**      * Resolve the {@link ServiceRestMetadata} {@link Set set} from {@link ServiceBean}      *      * 解析指定 ServiceBean 的 ServiceRestMetadata 集合      *      * @param serviceBean {@link ServiceBean}      * @return non-null {@link Set}      */     Set<ServiceRestMetadata> resolveServiceRestMetadata(ServiceBean serviceBean);      /**      * Resolve {@link RestMethodMetadata} {@link Set set} from {@link Class target type}      *      * 解析指定类的 ServiceRestMetadata 集合      *      * @param targetType {@link Class target type}      * @return non-null {@link Set}      */     Set<RestMethodMetadata> resolveMethodRestMetadata(Class<?> targetType);  }
```

---

### 7.2.1 DubboServiceBeanMetadataResolver

DubboServiceBeanMetadataResolver Bean 对象，在 [「5.2 DubboOpenFeignAutoConfiguration」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#) 中被创建。

org.springframework.cloud.alibaba.dubbo.metadata.resolver.DubboServiceBeanMetadataResolver ，实现 MetadataResolver、BeanClassLoaderAware、SmartInitializingSingleton 接口，基于 Dubbo ServiceBean 的 MetadataResolver 实现类。

```plain text
plain // DubboServiceBeanMetadataResolver.java  /**  * The metadata resolver for {@link Feign} for {@link ServiceBean Dubbo Service Bean} in the provider side.  */
```

---

### 7.2.1.1 构造方法

```plain text
plain // DubboServiceBeanMetadataResolver.java  private static final String[] CONTRACT_CLASS_NAMES = {         "feign.jaxrs2.JAXRS2Contract",         "org.springframework.cloud.openfeign.support.SpringMvcContract", };  /**  * 当前应用名  *  * 不过，目前暂时并未用该参数  */ private final String currentApplicationName; /**  * 当前类加载器  */ private ClassLoader classLoader; private final ObjectProvider<Contract> contract;  /**  * Feign Contract 数组  *  * https://www.jianshu.com/p/6582f8319f72  */ private Collection<Contract> contracts;  public DubboServiceBeanMetadataResolver(String currentApplicationName, ObjectProvider<Contract> contract) {     this.currentApplicationName = currentApplicationName;     this.contract = contract; }
```

---

- 具体的每个属性，我们下面一个一个来看。

### 7.2.1.2 afterSingletonsInstantiated

实现 #afterSingletonsInstantiated() 方法，初始化 contracts 属性。代码如下：

```plain text
plain // DubboServiceBeanMetadataResolver.java  @Override public void afterSingletonsInstantiated() {     // <1> 创建 Feign Contract 数组     LinkedList<Contract> contracts = new LinkedList<>();      // Add injected Contract if available, for example SpringMvcContract Bean under Spring Cloud Open Feign     // <2.1> 如果 contract 存在，则添加到 contracts 中     contract.ifAvailable(contracts::add);      // <2.2> 遍历 CONTRACT_CLASS_NAMES 数组，创建对应的 Contract 对象，添加到 contracts 中     Stream.of(CONTRACT_CLASS_NAMES)             .filter(this::isClassPresent) // filter the existed classes             .map(this::loadContractClass) // load Contract Class             .map(this::createContract)    // create instance by the specified class             .forEach(contracts::add);     // add the Contract instance into contracts      // <3> 赋值给 contracts 中     this.contracts = Collections.unmodifiableCollection(contracts); }
```

---

- <1>
处，创建 Feign Contract 数组
contracts
。
- <2.1>
处，如果
contract
存在，则添加到
contracts
中。一般情况下，
contract
不存在，所以可以暂时无视。
- <2.2>
处，遍历
CONTRACT_CLASS_NAMES
数组，创建对应的 Contract 对象，添加到
contracts
中。一般来说，都会存在。涉及代码如下：

```plain text
plain // DubboServiceBeanMetadataResolver.java  // 判断指定 className 类是否存在 private boolean isClassPresent(String className) {     return ClassUtils.isPresent(className, classLoader); }  // 加载 contractClassName 对应的 Contract 实现类 private Class<?> loadContractClass(String contractClassName) {     return ClassUtils.resolveClassName(contractClassName, classLoader); }  // 创建 Contract 对象 private Contract createContract(Class<?> contractClassName) {     return (Contract) BeanUtils.instantiateClass(contractClassName); }
```

---

- <3>
处，赋值给
this.contracts
中。

### 7.2.1.3 resolveMethodRestMetadata

实现 #resolveMethodRestMetadata(Class<?> targetType) 方法，解析指定类的 ServiceRestMetadata 集合。代码如下：

```plain text
plain // DubboServiceBeanMetadataResolver.java  @Override public Set<RestMethodMetadata> resolveMethodRestMetadata(Class<?> targetType) {     // <1> 获得 Method 集合     List<Method> feignContractMethods = selectFeignContractMethods(targetType);     // <2> 转换成 RestMethodMetadata 集合     return contracts.stream() // 遍历 contracts 数组             .map(contract -> contract.parseAndValidatateMetadata(targetType)) // <2.1> 返回目标类型的 Feign MethodMetadata 数组             .flatMap(Collection::stream)             .map(methodMetadata -> resolveMethodRestMetadata(methodMetadata, targetType, feignContractMethods)) // <2.2> 将 Feign MethodMetadata 转换成 RestMethodMetadata 对象             .collect(Collectors.toSet()); // 转换成 Set }
```

---

- <1>
处，调用
#selectFeignContractMethods(Class<?> targetType)
方法，获得 Method 集合。代码如下：

```plain text
plain // DubboServiceBeanMetadataResolver.java  /**  * Select feign contract methods  * <p>  * extract some code from {@link Contract.BaseContract#parseAndValidatateMetadata(java.lang.Class)}  *  * @param targetType  * @return non-null  */ private List<Method> selectFeignContractMethods(Class<?> targetType) {     List<Method> methods = new LinkedList<>();     // 遍历目标的方法     for (Method method : targetType.getMethods()) {         // 忽略         if (method.getDeclaringClass() == Object.class || // Object 声明的方法，例如说 equals 方法                 (method.getModifiers() & Modifier.STATIC) != 0 || // 静态方法                 Util.isDefault(method)) { // Feign 默认方法             continue;         }         methods.add(method);     }     return methods; }
```

---

- <2>
处，转换成 RestMethodMetadata 集合。
- <2.1>
处，调用
Contract#parseAndValidatateMetadata()
方法，返回目标类型的 Feign MethodMetadata 数组。这块代码属于 Feign 的，我们先不细调，看一个结果的示例。如下图：
![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/2f1a20456b2528e21b5e00b6d8f19c97.jpg)
结果
    - 这里有一点要注意，因为
CONTRACT_CLASS_NAMES
中，即有 JAXRS2Contract 类，又有 SpringMvcContract 类，所以要求添加 JSR311 的注解，也要添加 Spring MVC 的注解。举个例子：

```plain text
plain // DefaultEchoService.java  @Service(version = "1.0.0", protocol = {"dubbo", "rest"}) @RestController // Spring MVC 注解 @Path("/") // JSR311 注解 public class DefaultEchoService implements EchoService {      @Override     @GetMapping(value = "/echo" //            consumes = MediaType.APPLICATION_JSON_VALUE, //            produces = MediaType.APPLICATION_JSON_UTF8_VALUE     ) // Spring MVC 注解     @Path("/echo") // JSR311 注解     @GET // JSR311 注解 //    @Consumes("application/json") //    @Produces("application/json;charset=UTF-8")     public String echo(@RequestParam // Spring MVC 注解                        @QueryParam("message") String message) { // JSR311 注解         System.out.println(message);         return RpcContext.getContext().getUrl() + " [echo] : " + message;     } }
```

---

```plain text
    * <font style="color:rgb(51, 51, 51);">不过艿艿暂时不太理解，为什么这么设计。有知道的胖友，麻烦教育下，嘻嘻~</font>
```

- <2.2>
处，调用
#resolveMethodRestMetadata(MethodMetadata methodMetadata, Class<?> targetType, List feignContractMethods)
方法，将 Feign MethodMetadata 转换成 RestMethodMetadata 对象。代码如下：

```plain text
plain // DubboServiceBeanMetadataResolver.java  protected RestMethodMetadata resolveMethodRestMetadata(MethodMetadata methodMetadata, // Feign MethodMetadata                                                        Class<?> targetType,                                                        List<Method> feignContractMethods) {     // 获得 configKey 。例如说：DefaultEchoService#echo(String)     String configKey = methodMetadata.configKey();     // 获得匹配的 Method     Method feignContractMethod = getMatchedFeignContractMethod(targetType, feignContractMethods, configKey);     // 创建 RestMethodMetadata 对象，并设置其属性     RestMethodMetadata metadata = new RestMethodMetadata();     metadata.setRequest(new RequestMetadata(methodMetadata.template()));     metadata.setMethod(new org.springframework.cloud.alibaba.dubbo.metadata.MethodMetadata(feignContractMethod));     metadata.setIndexToName(methodMetadata.indexToName());     return metadata; }  private Method getMatchedFeignContractMethod(Class<?> targetType, List<Method> methods, String expectedConfigKey) {     Method matchedMethod = null;     // 遍历 Method 集合     for (Method method : methods) {         // 获得该方法的 configKey         String configKey = Feign.configKey(targetType, method);         // 如果相等，则进行返回。         if (expectedConfigKey.equals(configKey)) {             matchedMethod = method;             break;         }     }     return matchedMethod; }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">对象转换的代码，简单瞅瞅即可明白。</font>
```

### 7.2.1.4 resolveServiceRestMetadata

实现 #resolveServiceRestMetadata(ServiceBean serviceBean) 方法，解析指定 ServiceBean 的 ServiceRestMetadata 集合。代码如下：

```plain text
plain // DubboServiceBeanMetadataResolver.java  @Override public Set<ServiceRestMetadata> resolveServiceRestMetadata(ServiceBean serviceBean) {     // <1.1> 获得应用的 Bean 对象     Object bean = serviceBean.getRef();     // <1.2> 获得 Bean 类型     Class<?> beanType = bean.getClass();     // <1.3> 解析 Bean 类型对应的 RestMethodMetadata 集合     Set<RestMethodMetadata> methodRestMetadata = resolveMethodRestMetadata(beanType);      // <2.1> 创建 ServiceRestMetadata 数组     Set<ServiceRestMetadata> serviceRestMetadata = new LinkedHashSet<>();     // <2.2> 获得 ServiceBean 暴露的 URL 集合     List<URL> urls = serviceBean.getExportedUrls();     // <2.3> 遍历 URL 集合，将 RestMethodMetadata 集合，封装成 ServiceRestMetadata 对象，然后添加到 serviceRestMetadata 中，最后返回。     urls.stream()             .map(SpringCloudRegistry::getServiceName)             .forEach(serviceName -> {                 ServiceRestMetadata metadata = new ServiceRestMetadata();                 metadata.setName(serviceName);                 metadata.setMeta(methodRestMetadata);                 serviceRestMetadata.add(metadata);             });     return serviceRestMetadata; }
```

---

- <1.3>[「7.2.1.3 resolveMethodRestMetadata」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
处，调用
#resolveMethodRestMetadata(Class<?> targetType)
方法，解析 Bean 类型对应的 RestMethodMetadata 集合。即，我们在
解析的方法。
- <2.1>
处，获得 ServiceBean 暴露的 URL 集合。例如说，本文的 DefaultEchoService 示例，就暴露了
dubbo://
和
rest://
两种协议的 URL 。
- <2.3>
处，遍历 URL 集合，将 RestMethodMetadata 集合，封装成 ServiceRestMetadata 对象，然后添加到 serviceRestMetadata 中，最后返回。此处的
SpringCloudRegistry::getServiceName
代码段，就是调用
SpringCloudRegistry#getServiceName(URL url)
方法，获得 Dubbo 服务名。例如说：
providers:dubbo:org.springframework.cloud.alibaba.dubbo.service.EchoService:1.0.0
。

至此，Dubbo Service 元数据的解析，就已经完成了。后续，我们会看到两个方面的内容：

- 1、将元数据存储到配置中心。这样，服务消费者才能共享到该部分的数据。
- 2、服务消费者基于 Dubbo Service 元数据，可以使用 Dubbo 发起泛化调用。

当然，如果不使用 Dubbo 发起泛化调用，是不需要这部分 Dubbo Service 元数据的。为什么呢？胖友好好思考一波~

## 7.3 DubboTransportedMethodMetadataResolver

org.springframework.cloud.alibaba.dubbo.metadata.resolver.DubboTransportedMethodMetadataResolver ，解析 @DubboTransported 注解的 MethodMetadata 数据。代码如下：

```plain text
plain // DubboTransportedMethodMetadataResolver.java  public Map<DubboTransportedMethodMetadata, RequestMetadata> resolve(Class<?> targetType) {     // <1> 获得指定类的 DubboTransportedMethodMetadata 集合     Set<DubboTransportedMethodMetadata> dubboTransportedMethodMetadataSet = resolveDubboTransportedMethodMetadataSet(targetType);     // <2> 获得指定类的 RequestMetadata 映射。其中，KEY 为 configKey     Map<String, RequestMetadata> requestMetadataMap = resolveRequestMetadataMap(targetType);     // <3> 转换成 DubboTransportedMethodMetadata 和 RequestMetadata 的映射     return dubboTransportedMethodMetadataSet             .stream()             .collect(Collectors.toMap(methodMetadata -> methodMetadata, methodMetadata ->                     requestMetadataMap.get(Feign.configKey(targetType, methodMetadata.getMethod()))             )); }
```

---

- <1>
处，调用
#resolveDubboTransportedMethodMetadataSet(Class<?> targetType)
方法，获得指定类的 DubboTransportedMethodMetadata 集合。代码如下：

```plain text
plain // DubboTransportedMethodMetadataResolver.java  protected Set<DubboTransportedMethodMetadata> resolveDubboTransportedMethodMetadataSet(Class<?> targetType) {     // The public methods of target interface     Method[] methods = targetType.getMethods();     // 创建 DubboTransportedMethodMetadata 数组     Set<DubboTransportedMethodMetadata> methodMetadataSet = new LinkedHashSet<>();     // 遍历方法     for (Method method : methods) {         // 如果有 @DubboTransported 注解         DubboTransported dubboTransported = resolveDubboTransported(method); // ①         // 如果有，则创建成  DubboTransportedMethodMetadata 对象，并添加到 methodMetadataSet 中         if (dubboTransported != null) {             // 创建 ②             DubboTransportedMethodMetadata methodMetadata = createDubboTransportedMethodMetadata(method, dubboTransported);             // 添加             methodMetadataSet.add(methodMetadata);         }     }     return methodMetadataSet; }  // ① private DubboTransported resolveDubboTransported(Method method) {     // 先从方法上，获得 @DubboTransported 注解     DubboTransported dubboTransported = AnnotationUtils.findAnnotation(method, DUBBO_TRANSPORTED_CLASS);     // 如果获得不到，则从类上，获得 @DubboTransported 注解     if (dubboTransported == null) { // Attempt to find @DubboTransported in the declaring class         Class<?> declaringClass = method.getDeclaringClass();         dubboTransported = AnnotationUtils.findAnnotation(declaringClass, DUBBO_TRANSPORTED_CLASS);     }     return dubboTransported; }  // ② private DubboTransportedMethodMetadata createDubboTransportedMethodMetadata(Method method, DubboTransported dubboTransported) {     // 创建 DubboTransportedMethodMetadata 对象     DubboTransportedMethodMetadata methodMetadata = new DubboTransportedMethodMetadata(method);    // 解析属性，并设置到 methodMetadata 中     String protocol = propertyResolver.resolvePlaceholders(dubboTransported.protocol());     String cluster = propertyResolver.resolvePlaceholders(dubboTransported.cluster());     methodMetadata.setProtocol(protocol);     methodMetadata.setCluster(cluster);     return methodMetadata; }
```

---

- <2>
处，调用
#resolveRequestMetadataMap(Class<?> targetType)
方法，获得指定类的 RequestMetadata 映射。其中，KEY 为
configKey
。代码如下：

```plain text
plain // DubboTransportedMethodMetadataResolver.java  private Map<String, RequestMetadata> resolveRequestMetadataMap(Class<?> targetType) {     return contract.parseAndValidatateMetadata(targetType) // 获得指定类的 Feign MethodMetadata 集合             .stream().collect(Collectors.toMap(feign.MethodMetadata::configKey, this::requestMetadata)); // 创建 RequestMetadata 对象 }  private RequestMetadata requestMetadata(feign.MethodMetadata methodMetadata) {     return new RequestMetadata(methodMetadata.template()); }
```

---

- <3>
处，转换成 DubboTransportedMethodMetadata 和 RequestMetadata 的映射。

后续，这个类会被 [「8.1 TargeterInvocationHandler」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#) 所调用 。

## 7.4 MetadataConfigService

给服务提供者使用。

org.springframework.cloud.alibaba.dubbo.metadata.service.MetadataConfigService ，元数据配置服务接口，即可以从配置中心，读取和写入元数据。代码如下：

```plain text
plain // MetadataConfigService.java  public interface MetadataConfigService {      /**      * 发布指定服务的 Rest 元数据      *      * @param serviceName 服务名      * @param serviceRestMetadata ServiceRestMetadata 集合      */     void publishServiceRestMetadata(String serviceName, Set<ServiceRestMetadata> serviceRestMetadata);      /**      * 获得指定服务的 Rest 元数据      *      * @param serviceName 服务名      * @return ServiceRestMetadata 集合      */     Set<ServiceRestMetadata> getServiceRestMetadata(String serviceName);  }
```

---

### 7.4.1 NacosMetadataConfigService

org.springframework.cloud.alibaba.dubbo.metadata.service.NacosMetadataConfigService ，实现 MetadataConfigService 接口，基于 Nacos 作为配置中心的实现类。

### 7.4.1.1 构造方法

```plain text
plain // NacosMetadataConfigService.java  /**  * ObjectMapper ，使用 Jackson 序列化和反序列化  */ private final ObjectMapper objectMapper = new ObjectMapper();  /**  * NacosConfigProperties 对象，用于获得 {@link #configService}  */ @Autowired private NacosConfigProperties nacosConfigProperties;  private ConfigService configService;  @PostConstruct public void init() {     // 初始化 configService 属性     this.configService = nacosConfigProperties.configServiceInstance();     // 开启 JSON 格式化     this.objectMapper.enable(SerializationFeature.INDENT_OUTPUT); }
```

---

### 7.4.1.2 publishServiceRestMetadata

实现 #publishServiceRestMetadata(String serviceName, Set serviceRestMetadata) 方法，代码如下：

```plain text
plain // NacosMetadataConfigService.java  @Override public void publishServiceRestMetadata(String serviceName, Set<ServiceRestMetadata> serviceRestMetadata) {     // 获得 Nacos dataId ①     String dataId = getServiceRestMetadataDataId(serviceName);     // 将 ServiceRestMetadata 集合序列化成 json 字符串 ②     String json = writeValueAsString(serviceRestMetadata);     // 写入到 Nacos 配置中心     try {         configService.publishConfig(dataId, DEFAULT_GROUP, json);     } catch (NacosException e) {         throw new RuntimeException(e);     } }  /**  * Get the data Id of service rest metadata  */ private static String getServiceRestMetadataDataId(String serviceName) { // ①     return "metadata:rest:" + serviceName + ".json"; }  private String writeValueAsString(Object object) { // ②     String content;     try {         content = objectMapper.writeValueAsString(object);     } catch (JsonProcessingException e) {         throw new IllegalArgumentException(e);     }     return content; }
```

---

### 7.4.1.3 getServiceRestMetadata

实现 #getServiceRestMetadata(String serviceName) 方法，代码如下：

```plain text
plain // NacosMetadataConfigService.java  @Override public Set<ServiceRestMetadata> getServiceRestMetadata(String serviceName) {     Set<ServiceRestMetadata> metadata;     // 获得 Nacos dataId     String dataId = getServiceRestMetadataDataId(serviceName);     try {         // 从 Nacos 配置中心，读取 json 字符串         String json = configService.getConfig(dataId, DEFAULT_GROUP, 1000 * 3);         // 将 json 字符串，反序列化成 ServiceRestMetadata 集合         metadata = objectMapper.readValue(json, TypeFactory.defaultInstance().constructCollectionType(LinkedHashSet.class, ServiceRestMetadata.class));     } catch (Exception e) {         throw new RuntimeException(e);     }     return metadata; }
```

---

## 7.5 DubboServiceMetadataRepository

给服务消费者使用。

org.springframework.cloud.alibaba.dubbo.metadata.repository.DubboServiceMetadataRepository ，Dubbo Service Metadata 仓库。通过该类，服务消费者就可以获得每个对应 Dubbo 服务的 ReferenceBean 对象~

### 7.5.1 构造方法

```plain text
plain // DubboServiceMetadataRepository.java  /**  * RequestMetadata 和 ReferenceBean 的映射  *  * Key is application name  * Value is  Map<RequestMetadata, ReferenceBean<GenericService>>  */ private Map<String, Map<RequestMetadata, ReferenceBean<GenericService>>> referenceBeansRepository = new HashMap<>();  /**  * RequestMetadata 和 MethodMetadata 的映射  *  * Key is application name  */ private Map<String, Map<RequestMetadata, MethodMetadata>> methodMetadataRepository = new HashMap<>();  @Autowired private MetadataConfigService metadataConfigService;
```

---

- 看看每个属性上的注释哟。
- 有一点要注意，
Key is application name
，表示首个 KEY 是 Spring Cloud（Spring Boot）应用名。
    - 但是，一个 Dubbo 应用中，可以有多个 Dubbo Service ，所以，就有了第二个 Map ，例如
Map<RequestMetadata, ReferenceBean
。
    - 当然，此处是按照 RequestMetadata 为维度，即每个 Dubbo Service 方法对应的请求信息。因为，每个请求路径的 URL 是唯一的，所以这么做是 OK 的。相当于说，把每个 Dubbo Service 的方法，平铺开。

### 7.5.2 updateMetadata

#updateMetadata(String serviceName) 方法，初始化指定 serviceName 的元数据。代码如下：

```plain text
plain // DubboServiceMetadataRepository.java  public void updateMetadata(String serviceName) {     // <1.1> 获得 serviceName 对应的 RequestMetadata 和 ReferenceBean 的映射     Map<RequestMetadata, ReferenceBean<GenericService>> genericServicesMap = referenceBeansRepository.computeIfAbsent(serviceName, k -> new HashMap<>());     // <1.2> 获得 serviceName 对应的 RequestMetadata 和 MethodMetadata 的映射     Map<RequestMetadata, MethodMetadata> methodMetadataMap = methodMetadataRepository.computeIfAbsent(serviceName, k -> new HashMap<>());     // <1.3> 获得 serviceName 对应的  ServiceRestMetadata 集合     Set<ServiceRestMetadata> serviceRestMetadataSet = metadataConfigService.getServiceRestMetadata(serviceName);      // <2> 遍历 ServiceRestMetadata 集合，创建对应的 ReferenceBean ，获得对应的 MethodMetadata 对象     for (ServiceRestMetadata serviceRestMetadata : serviceRestMetadataSet) {         // <2.1> 创建对应的 ReferenceBean         ReferenceBean<GenericService> referenceBean = adaptReferenceBean(serviceRestMetadata);         // <2.2> 遍历 RestMethodMetadata 集合，添加到 genericServicesMap 和 methodMetadataMap 中，进行缓存         serviceRestMetadata.getMeta().forEach(restMethodMetadata -> {             RequestMetadata requestMetadata = restMethodMetadata.getRequest();             genericServicesMap.put(requestMetadata, referenceBean);             methodMetadataMap.put(requestMetadata, restMethodMetadata.getMethod());         });     } }
```

---

- <1.3>[「7.4 MetadataConfigService」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
处，调用
MetadataConfigService#getServiceRestMetadata(String serviceName)
方法，获得指定
serviceName
的 ServiceRestMetadata 集合。此处，我们就使用上了
。
- <2>
处，遍历 ServiceRestMetadata 集合，创建对应的 ReferenceBean ，获得对应的 MethodMetadata 对象。
    - <2.1>
处，调用
#adaptReferenceBean(ServiceRestMetadata serviceRestMetadata)
方法，创建 ReferenceBean 对象。代码如下：

```plain text
plain // DubboServiceMetadataRepository.java  private ReferenceBean<GenericService> adaptReferenceBean(ServiceRestMetadata serviceRestMetadata) {     // 获得相应的属性     String dubboServiceName = serviceRestMetadata.getName();     String[] segments = SpringCloudRegistry.getServiceSegments(dubboServiceName);     String interfaceName = SpringCloudRegistry.getServiceInterface(segments);     String version = SpringCloudRegistry.getServiceVersion(segments);     String group = SpringCloudRegistry.getServiceGroup(segments);      // 创建 ReferenceBean 对象，并设置相关属性     ReferenceBean<GenericService> referenceBean = new ReferenceBean<GenericService>();     referenceBean.setGeneric(true);     referenceBean.setInterface(interfaceName);     referenceBean.setVersion(version);     referenceBean.setGroup(group);     return referenceBean; }
```

---

```plain text
    * <font style="color:rgb(51, 51, 51);">注意哦，此时创建的 ReferenceBean 是 Dubbo 的泛化引用。</font>
- <font style="color:rgb(51, 51, 51);"><2.2></font><font style="color:rgb(51, 51, 51);"> 处，遍历 RestMethodMetadata 集合，添加到 </font><font style="color:rgb(51, 51, 51);">genericServicesMap</font><font style="color:rgb(51, 51, 51);"> 和 </font><font style="color:rgb(51, 51, 51);">methodMetadataMap</font><font style="color:rgb(51, 51, 51);"> 中，进行缓存。</font>
```

### 7.5.3 getReferenceBean

#getReferenceBean(String serviceName, RequestMetadata requestMetadata) 方法，获得指定应用的指定 RequestMetadata 对应的 ReferenceBean 对象。代码如下：

```plain text
plain public ReferenceBean<GenericService> getReferenceBean(String serviceName, RequestMetadata requestMetadata) {     return getReferenceBeansMap(serviceName).get(requestMetadata); }  private Map<RequestMetadata, ReferenceBean<GenericService>> getReferenceBeansMap(String serviceName) {     return referenceBeansRepository.getOrDefault(serviceName, Collections.emptyMap()); }
```

---

### 7.5.4 getMethodMetadata

#getMethodMetadata(String serviceName, RequestMetadata requestMetadata) 方法，获得指定应用的指定 RequestMetadata 对应的 MethodMetadata 对象。代码如下：

```plain text
plain // DubboServiceMetadataRepository.java  public MethodMetadata getMethodMetadata(String serviceName, RequestMetadata requestMetadata) {     return getMethodMetadataMap(serviceName).get(requestMetadata); }  private Map<RequestMetadata, MethodMetadata> getMethodMetadataMap(String serviceName) {     return methodMetadataRepository.getOrDefault(serviceName, Collections.emptyMap()); }
```

---

## 7.6 小结

至此，我们看完了 metadata 包下的所有代码。因为本小节更多是元数据的解析、存储、读取，不涉及到具体的使用，所以会略微有点懵逼。但是，到下一节 openfeign 后，Feign 通过泛化调用对应的 Dubbo 服务，就会使用上元数据了。此时，我们就可以把整个流程打通。

# 8. openfeign 包

本小节，我们来瞅瞅，Dubbo 是如何和 Feign 进行集成的。

## 8.1 TargeterBeanPostProcessor

org.springframework.cloud.alibaba.dubbo.openfeign.TargeterBeanPostProcessor ，实现 BeanPostProcessor、BeanClassLoaderAware 接口，处理类型为 openfeign Targeter 的 Bean ，创建其动态代理，从而能够将 Dubbo 集成到 Openfeign 中。代码如下：

```plain text
plain // TargeterBeanPostProcessor.java  public class TargeterBeanPostProcessor implements BeanPostProcessor, BeanClassLoaderAware {      private static final String TARGETER_CLASS_NAME = "org.springframework.cloud.openfeign.Targeter";      private final Environment environment;      private final DubboServiceMetadataRepository dubboServiceMetadataRepository;      private ClassLoader classLoader;      public TargeterBeanPostProcessor(Environment environment, DubboServiceMetadataRepository dubboServiceMetadataRepository) {         this.environment = environment;         this.dubboServiceMetadataRepository = dubboServiceMetadataRepository;     }      @Override     public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {         return bean;     }      @Override     public Object postProcessAfterInitialization(final Object bean, String beanName) throws BeansException {         // <1> 获得 Bean 的类         Class<?> beanClass = ClassUtils.getUserClass(bean.getClass());         // <2> 获得 openfeign Targeter 接口         Class<?> targetClass = ClassUtils.resolveClassName(TARGETER_CLASS_NAME, classLoader);         // <3> 如果实现 openfeign Targeter 接口，则创建动态代理         if (targetClass.isAssignableFrom(beanClass)) {             return Proxy.newProxyInstance(classLoader, new Class[]{targetClass},                     new TargeterInvocationHandler(bean, environment, dubboServiceMetadataRepository));         }         return bean;     }      @Override     public void setBeanClassLoader(ClassLoader classLoader) {         this.classLoader = classLoader;     }  }
```

---

- 在分析具体代码之前，胖友先看下 [《Spring Cloud Alibaba Sentinel 整合 Feign 的设计实现》](https://cloud.tencent.com/developer/article/1378733)[「Feign 的执行过程」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
的
小节。因为艿艿看的时候也不是很了解 Feign 的内部运转机制，也是参考这个小节读懂这部分代码的。
- <1>
处，获得 Bean 的类。根据上面推荐的文章，我们可以知道，此时返回的是 HystrixTargeter 或 DefaultTargeter 类。
- <2>
处，获得 openfeign Targeter 接口。
- <3>[「8.2 TargeterInvocationHandler」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
处，如果实现 openfeign Targeter 接口，则创建动态代理。其中，传入的处理器是 TargeterInvocationHandler 对象。详细解析，见
。

## 8.2 TargeterInvocationHandler

org.springframework.cloud.alibaba.dubbo.openfeign.TargeterInvocationHandler ，会拦截 Targeter 的 #target(FeignClientFactoryBean factory, Builder feign, FeignContext context, HardCodedTarget target) 方法，根据条件，创建不同的代理对象。代码如下：

如果不理解 Targeter 的话，请再看下 [《Spring Cloud Alibaba Sentinel 整合 Feign 的设计实现》](https://cloud.tencent.com/developer/article/1378733) 的 [「Feign 的执行过程」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#) 小节。

```plain text
plain // TargeterInvocationHandler.java  class TargeterInvocationHandler implements InvocationHandler {      private final Object bean;      private final Environment environment;      private final DubboServiceMetadataRepository dubboServiceMetadataRepository;      TargeterInvocationHandler(Object bean, Environment environment,                               DubboServiceMetadataRepository dubboServiceMetadataRepository) {         this.bean = bean;         this.environment = environment;         this.dubboServiceMetadataRepository = dubboServiceMetadataRepository;     }      @Override     public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {         /**          * args[0]: FeignClientFactoryBean factory          * args[1]: Feign.Builder feign          * args[2]: FeignContext context          * args[3]: Target.HardCodedTarget<T> target          */         FeignContext feignContext = cast(args[2]);         Target.HardCodedTarget<?> target = cast(args[3]);          // <1> 先调用原有 target 方法，返回默认的代理对象         // Execute Targeter#target method first         method.setAccessible(true);         // Get the default proxy object         Object defaultProxy = method.invoke(bean, args);         // Create Dubbo Proxy if required         // 如果符合创建 Dubbo 代理对象，则创建 Dubbo 代理对象。         // 否则，使用默认的 defaultProxy 代理         return createDubboProxyIfRequired(feignContext, target, defaultProxy);     }      // ... 省略下面要讲解的方法 }
```

---

- 为了让胖友更加好理解，我们来看下这个方法被调用时的截图：
![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/1261f836abcb3afa56682544552de7b7.jpg)
调用图
- <1>
处，先调用原有
target
方法，返回默认的代理对象。
- <2>
处，调用
#createDubboProxyIfRequired(FeignContext feignContext, Target target, Object defaultProxy)
方法，如果符合创建 Dubbo 代理对象，则创建 Dubbo 代理对象。否则，使用默认的 defaultProxy 代理。那么问题就来了，条件是什么呢？有
@DubboTransported
注解，且从配置中心拉取不到服务提供者的元数据。 因为，没有服务提供者的元数据，我们也无法使用 Dubbo 的泛化调用呀。
- so ，我们继续往下看。

### 8.2.1 createDubboProxyIfRequired

#createDubboProxyIfRequiredcreateDubboProxyIfRequired(FeignContext feignContext, Target target, Object defaultProxy) 方法，根据条件，创建对应的代理对象。代码如下：

```plain text
plain // TargeterInvocationHandler.java  private Object createDubboProxyIfRequired(FeignContext feignContext, Target target, Object defaultProxy) {     // <1> 尝试创建 DubboInvocationHandler     DubboInvocationHandler dubboInvocationHandler = createDubboInvocationHandler(feignContext, target, defaultProxy);     // <2.1> 如果未创建成功，说明不符合条件，则返回默认的 defaultProxy 代理     if (dubboInvocationHandler == null) {         return defaultProxy;     }     // <2.2> 如果创建成功，说明符合条件，则创建使用 dubboInvocationHandler 的动态代理     return Proxy.newProxyInstance(target.type().getClassLoader(), new Class<?>[]{target.type()}, dubboInvocationHandler); }
```

---

- <1>
处，调用
#createDubboInvocationHandler(FeignContext feignContext, Target target, Object defaultFeignClientProxy)
方法，尝试创建 DubboInvocationHandler。
- <2.1>
处，如果未创建成功，说明不符合条件，则返回默认的
defaultProxy
代理。
- <2.2>
处，如果创建成功，说明符合条件，则创建使用
dubboInvocationHandler
的动态代理。

### 8.2.2 createDubboInvocationHandler

#createDubboInvocationHandler(FeignContext feignContext, Target target, Object defaultFeignClientProxy) 方法，创建 DubboInvocationHandler 对象。代码如下：

未来这块的逻辑，会被抽取到 org.springframework.cloud.alibaba.dubbo.openfeign.DubboInvocationHandlerFactory 类中。

```plain text
plain // TargeterInvocationHandler.java  private DubboInvocationHandler createDubboInvocationHandler(FeignContext feignContext, Target target, Object defaultFeignClientProxy) {     // Service name equals @FeignClient.name()     String serviceName = target.name();     Class<?> targetType = target.type();      // Get Contract Bean from FeignContext     // <1.1> 获得 Feign Contract     Contract contract = feignContext.getInstance(serviceName, Contract.class);     // <1.2> 创建 DubboTransportedMethodMetadataResolver 对象     DubboTransportedMethodMetadataResolver resolver = new DubboTransportedMethodMetadataResolver(environment, contract);     // <1.3> 解析指定类，获得其 DubboTransportedMethodMetadata 和 RequestMetadata 的映射     Map<DubboTransportedMethodMetadata, RequestMetadata> methodRequestMetadataMap = resolver.resolve(targetType);     // <1.4> 如果为空，则返回，说明不符合条件     if (methodRequestMetadataMap.isEmpty()) { // @DubboTransported method was not found         return null;     }      // Update Metadata     // <2> 初始化指定 `serviceName` 的元数据。此处，会从配置中心，获得元数据     dubboServiceMetadataRepository.updateMetadata(serviceName);      Map<Method, org.springframework.cloud.alibaba.dubbo.metadata.MethodMetadata> methodMetadataMap = new HashMap<>();     Map<Method, GenericService> genericServicesMap = new HashMap<>();     // <3> 遍历 methodRequestMetadataMap 集合，初始化其 GenericService     methodRequestMetadataMap.forEach((dubboTransportedMethodMetadata, requestMetadata) -> {         // <3.1.1> 获得 ReferenceBean 对象，并初始化其属性         ReferenceBean<GenericService> referenceBean = dubboServiceMetadataRepository.getReferenceBean(serviceName, requestMetadata);         referenceBean.setProtocol(dubboTransportedMethodMetadata.getProtocol());         referenceBean.setCluster(dubboTransportedMethodMetadata.getCluster());         // <3.1.2> 添加到 genericServicesMap 中         genericServicesMap.put(dubboTransportedMethodMetadata.getMethod(), referenceBean.get());         // <3.2.1> 获得 MethodMetadata 对象         org.springframework.cloud.alibaba.dubbo.metadata.MethodMetadata methodMetadata = dubboServiceMetadataRepository.getMethodMetadata(serviceName, requestMetadata);         // <3.2.2> 添加到 methodMetadataMap 中         methodMetadataMap.put(dubboTransportedMethodMetadata.getMethod(), methodMetadata);     });      // <4.1> 获得默认的 defaultFeignClientProxy 中，默认的 InvocationHandler 对象     InvocationHandler defaultFeignClientInvocationHandler = Proxy.getInvocationHandler(defaultFeignClientProxy);     // <4.2> 创建 DubboInvocationHandler 对象     return new DubboInvocationHandler(genericServicesMap, methodMetadataMap, defaultFeignClientInvocationHandler); }
```

---

- <1.1>
处，获得 Feign Contract 。
- <1.2>
处，创建 DubboTransportedMethodMetadataResolver 对象。
- <1.3>[「7.3 DubboTransportedMethodMetadata」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
处，调用
DubboTransportedMethodMetadataResolver#resolve(Class<?> targetType)
解析指定类，获得其 DubboTransportedMethodMetadata 和 RequestMetadata 的映射。此处，我们就把
给串起来了。
- <1.4>
处，如果为空，则返回，说明不符合条件。此处，我们来抛一个问题，如果一个类里，多个方法中，有部分方法没有
@DubboTransported
注解，那么会不会创建 DubboInvocationHandler 呢？答案是肯定的。那么此时，就会有
@DubboTransported
注解的方法，使用 Dubbo 进行调用，没有
@DubboTransported
注解的方法，还是选择原有 Feign 提供的方式（例如说 RestTemplate）进行调用。
- <2>[「7.5 DubboServiceMetadataRepository」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
处，调用
DubboServiceMetadataRepository#updateMetadata(String serviceName)
方法，初始化指定
serviceName
的元数据（此时，会从配置中心，获得元数据）。此处，我们就把
给串起来了。
- <3>
处，遍历
methodRequestMetadataMap
集合，初始化其 GenericService 。
    - <3.1.1>
处，获得 ReferenceBean 对象，并初始化其属性。
    - <3.1.2>
处，添加到
genericServicesMap
中。
    - <3.2.1>
处，获得 MethodMetadata 对象。
    - <3.2.2>
处，添加到
methodMetadataMap
中。
- <4.1>
处，获得默认的
defaultFeignClientProxy
中，默认的 InvocationHandler 对象。为什么需要它呢？因为，一个类中，可能有没有
@DubboTransported
注解的方法。
- <4.2>
处，创建 DubboInvocationHandler 对象。

## 8.3 DubboInvocationHandler

org.springframework.cloud.alibaba.dubbo.openfeign.DubboInvocationHandler ，实现 InvocationHandler 接口，Dubbo InvocationHandler 实现类。代码如下：

```plain text
plain // DubboInvocationHandler.java  public class DubboInvocationHandler implements InvocationHandler {      private final Map<Method, GenericService> genericServicesMap;      private final Map<Method, MethodMetadata> methodMetadata;      private final InvocationHandler defaultInvocationHandler;      public DubboInvocationHandler(Map<Method, GenericService> genericServicesMap,                                   Map<Method, MethodMetadata> methodMetadata,                                   InvocationHandler defaultInvocationHandler) {         this.genericServicesMap = genericServicesMap;         this.methodMetadata = methodMetadata;         this.defaultInvocationHandler = defaultInvocationHandler;     }      @Override     public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {         // 获得 GenericService 对象         GenericService genericService = genericServicesMap.get(method);         // 获得 MethodMetadata 对象         MethodMetadata methodMetadata = this.methodMetadata.get(method);          // <1> 情况一，如果任一不存在，使用默认的 defaultInvocationHandler         if (genericService == null || methodMetadata == null) {             return defaultInvocationHandler.invoke(proxy, method, args);         }          // 情况二，执行泛化调用         String methodName = methodMetadata.getName(); // 方法名         String[] parameterTypes = methodMetadata                 .getParams()                 .stream()                 .map(MethodParameterMetadata::getType)                 .toArray(String[]::new); // 参数类型         return genericService.$invoke(methodName, parameterTypes, args);     }  }
```

---

- <1>
处，如果任一不存在，使用默认的
defaultInvocationHandler
，即无
@DubboTransported
注解的方法。
- <2>
处，执行泛化调用，即有
@DubboTransported
注解的方法。

## 8.4 小结

至此，整个服务消费者调用的流程，我们已经串联起来了。因为本文是按照 package 包分层来写，所以连贯性会相对比较差。因此，需要胖友自己在调试一下哈。

# 9. registry 包

本小节，我们来瞅瞅，Dubbo 是如何和 Spring Cloud 注册中心进行集成的。

在 [2.4.2 application.yaml](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#) 中，我们可以看到，注册中心使用的是 dubbo.registry.address: spring-cloud://nacos 。

## 9.1 Registration

org.springframework.cloud.alibaba.dubbo.registry.DubboRegistration ，实现 Spring Cloud Registration 接口，Dubbo Registration 实现类。代码如下：

```plain text
plain // DubboRegistration.java  /**  * The {@link Registration} of Dubbo uses an external of {@link ServiceInstance} instance as the delegate.  */ class DubboRegistration implements Registration {      /**      * Spring Cloud ServiceInstance      */     private final ServiceInstance delegate;      public DubboRegistration(ServiceInstance delegate) {         this.delegate = delegate;     }      @Override     public String getServiceId() {         return delegate.getServiceId();     }      @Override     public String getHost() {         return delegate.getHost();     }      @Override     public int getPort() {         return delegate.getPort();     }      @Override     public boolean isSecure() {         return delegate.isSecure();     }      @Override     public URI getUri() {         return delegate.getUri();     }      @Override     public Map<String, String> getMetadata() {         return delegate.getMetadata();     }      @Override     public String getScheme() {         return delegate.getScheme();     }  }
```

---

## 9.2 SpringCloudRegistryFactory

在 com.alibaba.dubbo.registry.RegistryFactory 中，声明了一个 SpringCloudRegistryFactory 拓展。如下：

```plain text
plain spring-cloud=org.springframework.cloud.alibaba.dubbo.registry.SpringCloudRegistryFactory
```

---

- 前缀为
“spring-cloud”
。即，和我们配置的
dubbo.registry.address: spring-cloud://nacos
能够对应上。

org.springframework.cloud.alibaba.dubbo.registry.SpringCloudRegistryFactory ，实现 Dubbo RegistryFactory 接口，创建对 SpringCloudRegistry 注册中心。代码如下：

```plain text
plain // SpringCloudRegistryFactory.java  public class SpringCloudRegistryFactory implements RegistryFactory {      private static ApplicationContext applicationContext;      @Override     public Registry getRegistry(URL url) {         // <1> 获得 ServiceRegistry 对象         ServiceRegistry<Registration> serviceRegistry = applicationContext.getBean(ServiceRegistry.class);         // <2> 获得 DiscoveryClient 对象         DiscoveryClient discoveryClient = applicationContext.getBean(DiscoveryClient.class);         // <3> 创建 SpringCloudRegistry 对象         return new SpringCloudRegistry(url, serviceRegistry, discoveryClient);     }      public static void setApplicationContext(ApplicationContext applicationContext) {         SpringCloudRegistryFactory.applicationContext = applicationContext;     }  }
```

---

- <1>
处，获得 ServiceRegistry 对象。此处，如果我们使用 Nacos 作为注册中心，那么返回的就是
org.springframework.cloud.alibaba.nacos.registry.NacosServiceRegistry
对象。
- <2>
处，获得 DiscoveryClient 对象。此处，如果我们使用 Nacos 作为注册中心，那么返回的 Composite DiscoveryClient 对象，包含
org.springframework.cloud.alibaba.nacos.NacosDiscoveryClient
对象。
- 上述两个变量，如下图所示：
![](/assets/images/learning/dubbo/dubbo-integration-spring-cloud/60f5da7bb593bde85b6b884d8136b4a7.jpg)
变量
- <3>[「9.3 SpringCloudRegistry」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)
处，创建 SpringCloudRegistry 对象。详细解析，见
。

## 9.3 SpringCloudRegistry

本小节，建立在胖友看过 [《精尽 Dubbo 源码分析 —— 注册中心（一）之抽象 API》](http://www.iocoder.cn/Dubbo/good-collection/) 文章。

org.springframework.cloud.alibaba.dubbo.registry.SpringCloudRegistry ，继承 Dubbo FailbackRegistry 抽象类，基于 Spring Cloud DiscoveryClient、SpringCloudRegistry 的 API ，封装出 Spring Cloud Registry 实现类。

### 9.3.1 构造方法

```plain text
plain // SpringCloudRegistry.java  /**  * ServiceRegistry 对象  */ private final ServiceRegistry<Registration> serviceRegistry;  /**  * DiscoveryClient 对象  */ private final DiscoveryClient discoveryClient;  public SpringCloudRegistry(URL url, ServiceRegistry<Registration> serviceRegistry,                            DiscoveryClient discoveryClient) {     super(url);     this.serviceRegistry = serviceRegistry;     this.discoveryClient = discoveryClient; }
```

---

### 9.3.2 doRegister

实现 #doRegister(URL ur) 方法，执行注册。代码如下：

```plain text
plain // SpringCloudRegistry.java  @Override protected void doRegister(URL url) {     // <1> 获得 serviceName     final String serviceName = getServiceName(url);     // <2> 创建 Registration 对象     final Registration registration = createRegistration(serviceName, url);     // <3> 注册到 serviceRegistry 中     serviceRegistry.register(registration); }
```

---

- <1>
处，获得
serviceName
。例如：
providers:dubbo:org.springframework.cloud.alibaba.dubbo.service.EchoService:1.0.0
。代码如下：

```plain text
plain // SpringCloudRegistry.java  public static String getServiceName(URL url) {     // 获得分类     String category = url.getParameter(Constants.CATEGORY_KEY, Constants.DEFAULT_CATEGORY);     // 获得 ServiceName     return getServiceName(url, category); }  private static void appendIfPresent(StringBuilder target, URL url, String parameterName) {     String parameterValue = url.getParameter(parameterName);     appendIfPresent(target, parameterValue); }  private static final String SERVICE_NAME_SEPARATOR = ":"; private static void appendIfPresent(StringBuilder target, String parameterValue) {     if (StringUtils.hasText(parameterValue)) {         target.append(SERVICE_NAME_SEPARATOR).append(parameterValue);     } }
```

---

- <2>
处，创建 DubboRegistration 对象。代码如下：

```plain text
plain // SpringCloudRegistry.java  private Registration createRegistration(String serviceName, URL url) {     return new DubboRegistration(createServiceInstance(serviceName, url)); }  private ServiceInstance createServiceInstance(String serviceName, URL url) {     // Append default category if absent     // 获得属性     String category = url.getParameter(Constants.CATEGORY_KEY, Constants.DEFAULT_CATEGORY);     URL newURL = url.addParameter(Constants.CATEGORY_KEY, category);     newURL = newURL.addParameter(Constants.PROTOCOL_KEY, url.getProtocol());     String ip = NetUtils.getLocalHost(); // IP     int port = newURL.getParameter(Constants.BIND_PORT_KEY, url.getPort()); // 端口     // 创建 DefaultServiceInstance 对象     DefaultServiceInstance serviceInstance = new DefaultServiceInstance(serviceName, ip, port, false);     serviceInstance.getMetadata().putAll(new LinkedHashMap<>(newURL.getParameters()));     return serviceInstance; }
```

---

- <3>
处，调用
ServiceRegistry#register(R registration)
方法，注册到
serviceRegistry
中。这样，Dubbo 就注册到 Spring Cloud Registry 中。

### 9.3.3 doUnregister

实现 #doUnregister(URL url) 方法，取消注册。代码如下：

```plain text
plain // SpringCloudRegistry.java  @Override protected void doUnregister(URL url) {     // 获得 serviceName     final String serviceName = getServiceName(url);     // 创建 Registration 对象     final Registration registration = createRegistration(serviceName, url);     // 取消注册从 serviceRegistry 中     this.serviceRegistry.deregister(registration); }
```

---

### 9.3.4 doSubscribe

实现 #doSubscribe(URL url, NotifyListener listener) 方法，执行订阅。代码如下：

```plain text
plain // SpringCloudRegistry.java  @Override protected void doSubscribe(URL url, NotifyListener listener) {     // <1> 获得 serviceName 数组     List<String> serviceNames = getServiceNames(url, listener);     // <2> 执行订阅     doSubscribe(url, listener, serviceNames); }
```

---

- <1>
处，获得 serviceName 数组。代码如下：

```plain text
plain // SpringCloudRegistry.java  private List<String> getServiceNames(URL url, NotifyListener listener) {     // 管理端，暂时无视     if (isAdminProtocol(url)) {         scheduleServiceNamesLookup(url, listener);         return getServiceNamesForOps(url);     } else {         return doGetServiceNames(url);     } }  private List<String> doGetServiceNames(URL url) {     // 获得 category 数组     String[] categories = getCategories(url);     // 创建 serviceName 数组，并进行获得     List<String> serviceNames = new ArrayList<String>(categories.length);     for (String category : categories) {         final String serviceName = getServiceName(url, category);         serviceNames.add(serviceName);     }     return serviceNames; }
```

---

- <2>
处，调用
#doSubscribe(final URL url, final NotifyListener listener, final List serviceNames)
方法，执行订阅。代码如下：

```plain text
plain // SpringCloudRegistry.java  private void doSubscribe(final URL url, final NotifyListener listener, final List<String> serviceNames) {     for (String serviceName : serviceNames) {         // <2.1> 获得 ServiceInstance 数组         List<ServiceInstance> serviceInstances = discoveryClient.getInstances(serviceName);         // <2.2> 通知订阅者         notifySubscriber(url, listener, serviceInstances);         // TODO Support Update notification event     } }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">遍历 </font><font style="color:rgb(51, 51, 51);">serviceNames</font><font style="color:rgb(51, 51, 51);"> 数组，逐个处理。</font>
- <font style="color:rgb(51, 51, 51);"><2.1></font><font style="color:rgb(51, 51, 51);"> 处，调用 </font><font style="color:rgb(51, 51, 51);">DiscoveryClient#getInstances(String serviceId)</font><font style="color:rgb(51, 51, 51);"> 方法，获得 ServiceInstance 数组。</font>
- <font style="color:rgb(51, 51, 51);"><2.2></font><font style="color:rgb(51, 51, 51);"> 处，调用 </font><font style="color:rgb(51, 51, 51);">#notifySubscriber(URL url, NotifyListener listener, List<ServiceInstance> serviceInstances)</font><font style="color:rgb(51, 51, 51);"> 方法，通知订阅者。详细解析，见 </font>[「notifySubscriber」](http://svip.iocoder.cn/Dubbo/spring-cloud-integration/#)<font style="color:rgb(51, 51, 51);"> 。</font>
```

### 9.3.4.1 notifySubscriber

#notifySubscriber(URL url, NotifyListener listener, List serviceInstances) 方法，通知订阅者。代码如下：

```plain text
plain // SpringCloudRegistry.java  private void notifySubscriber(URL url, NotifyListener listener, List<ServiceInstance> serviceInstances) {     // <1> 过滤掉非健康的 Dubbo 服务     List<ServiceInstance> healthyInstances = new LinkedList<ServiceInstance>(serviceInstances);     // <1> Healthy Instances     filterHealthyInstances(healthyInstances);     // <2> 创建 URL 数组     List<URL> urls = buildURLs(url, healthyInstances);     // <3> 通知订阅者     this.notify(url, listener, urls); }
```

---

- <1>
处，调用
#filterHealthyInstances(Collection instances)
方法，过滤掉非健康的 Dubbo 服务。代码如下：

```plain text
plain // SpringCloudRegistry.java  private void filterHealthyInstances(Collection<ServiceInstance> instances) {     filter(instances, new Filter<ServiceInstance>() {         @Override         public boolean accept(ServiceInstance data) {             // TODO check the details of status //                return serviceRegistry.getStatus(new DubboRegistration(data)) != null;             return true;         }     }); }  private <T> void filter(Collection<T> collection, Filter<T> filter) {     // remove if not accept     collection.removeIf(data -> !filter.accept(data)); }  private interface Filter<T> {      /**      * Tests whether or not the specified data should be accepted.      *      * @param data The data to be tested      * @return <code>true</code> if and only if <code>data</code>      * should be accepted      */     boolean accept(T data);  }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">从 </font><font style="color:rgb(51, 51, 51);">TODO check the details of status</font><font style="color:rgb(51, 51, 51);"> 可以看出，目前暂时未实现。后续，可能会根据状态进行过滤。</font>
```

- <2>
处，调用
#buildURLs(URL consumerURL, Collection serviceInstances)
方法，将 ServiceInstance 数组，转换成 URL 数组。代码如下：

```plain text
plain // SpringCloudRegistry.java  private List<URL> buildURLs(URL consumerURL, Collection<ServiceInstance> serviceInstances) {     // serviceInstances 为空，返回空数组     if (serviceInstances.isEmpty()) {         return Collections.emptyList();     }     // serviceInstances 非空，则逐个构建对应的 URL 对象，添加到 urls 中进行返回     List<URL> urls = new LinkedList<>();     for (ServiceInstance serviceInstance : serviceInstances) {         // 构建 URL 对象         URL url = buildURL(serviceInstance);         if (UrlUtils.isMatch(consumerURL, url)) {             urls.add(url);         }     }     return urls; }  private URL buildURL(ServiceInstance serviceInstance) {     return new URL(serviceInstance.getMetadata().get(Constants.PROTOCOL_KEY),             serviceInstance.getHost(),             serviceInstance.getPort(),             serviceInstance.getMetadata()); }
```

---

- <3>
处，调用父
#notify(URL url, NotifyListener listener, List urls)
方法，通知订阅者。

### 9.3.5 doUnsubscribe

实现 #doUnsubscribe(URL url, NotifyListener listener) 方法，取消订阅。代码如下：

```plain text
plain // SpringCloudRegistry.java  @Override protected void doUnsubscribe(URL url, NotifyListener listener) {     // 忽略管理端     if (isAdminProtocol(url)) {         shutdownServiceNamesLookup();     } }
```

---

# 666. 彩蛋

大体是这样，如果有些细节没写到位，欢迎知识星球留言。

比较有趣的，还是泛化调用那一块。