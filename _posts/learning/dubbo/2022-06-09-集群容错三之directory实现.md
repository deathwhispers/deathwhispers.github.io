---
layout: post
title: 集群容错（三）之Directory实现
author: deathwhispers
date: 2022-06-09
slug: dubbo-cluster-fault-tolerance-directory-impl
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-06-06 11:52
updated: 2022-06-06 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文接 [《精尽 Dubbo 源码解析 —— 集群容错（二）之 Cluster 实现》](http://svip.iocoder.cn/Dubbo/cluster-2-impl-cluster/?self=) 一文，分享 dubbo-cluster 模块， directory 包，**各种 Directory 实现类**。

Directory ，中文直译为**目录**，代表了**多个** Invoker ，可以把它看成 List 。但与 List 不同的是，它的值可能是动态变化的，比如注册中心推送变更。

Directory 子类如下图：

![Directory子类](/assets/images/learning/dubbo/dubbo-cluster-fault-tolerance-directory-impl/96cfccdf0da2317fa880f4eb48ec7099.png)

我们看到有两个实现类：

- StaticDirectory ，**静态静态**
Directory 实现类，从命名上看出它是
的
List
。
- RegistryDirectory ，基于**注册中心动态动态**
的
Directory 实现类，从命名上看出它是
的，会根据注册中心的推送变更
List
。

# 2. Directory

com.alibaba.dubbo.rpc.cluster.Directory ，继承 Node 接口，Directory 接口。代码如下：

```java
public interface Directory<T> extends Node {

    /**
     * get service type.
     *
     * 获得服务类型，例如：com.alibaba.dubbo.demo.DemoService
     *
     * @return service type.
     */
    Class<T> getInterface();

    /**
     * list invokers.
     *
     * 获得所有服务 Invoker 集合
     *
     * @return invokers
     */
    List<Invoker<T>> list(Invocation invocation) throws RpcException;

}
```

---

- 定义了**两个类型Invoker 集合**
接口方法，分别返回服务的
和
。
- 一个 Directory **只对应**
一个服务类型。

# 3. AbstractDirectory

com.alibaba.dubbo.rpc.cluster.directory.AbstractDirectory ，实现 Directory 接口，Directory 抽象实现类，实现了公用的**路由规则( Router )**的逻辑。

## 3.1 构造方法

```java
/**
 * 是否已经销毁
 */
private volatile boolean destroyed = false;
/**
 * 注册中心 URL
 */
private final URL url;
/**
 * 消费者 URL
 *
 * 若未显示调用 {@link #AbstractDirectory(URL, URL, List)} 构造方法，consumerUrl 等于 {@link #url}
 */
private volatile URL consumerUrl;
/**
 * Router 数组
 */
private volatile List<Router> routers;

public AbstractDirectory(URL url) {
    this(url, null);
}

public AbstractDirectory(URL url, List<Router> routers) {
    this(url, url, routers);
}

public AbstractDirectory(URL url, URL consumerUrl, List<Router> routers) {
    if (url == null) {
        throw new IllegalArgumentException("url == null");
    }
    this.url = url;
    this.consumerUrl = consumerUrl;
    // 设置 Router 数组
    setRouters(routers);
}
```

---

- consumerUrl
字段，认真看下注释和构造方法。
- 调用
#setRouters(routers)
方法，初始化并设置 Router 数组。

## 3.2 setRouters

#setRouters(routers) 方法，初始化并设置 Router 数组。详细解析，见 [《精尽 Dubbo 源码解析 —— 集群容错（七）之 Router 实现》](http://svip.iocoder.cn/Dubbo/cluster-7-impl-router?self=) 中。

## 3.3 list

#list(Invocation)**实现**方法，获得所有服务 Invoker 集合。代码如下：

```java
@Override
public List<Invoker<T>> list(Invocation invocation) throws RpcException {
    if (destroyed) {
        throw new RpcException("Directory already destroyed .url: " + getUrl());
    }
    // 获得所有 Invoker 集合
    List<Invoker<T>> invokers = doList(invocation);
    // 根据路由规则，筛选 Invoker 集合
    List<Router> localRouters = this.routers; // local reference 本地引用，避免并发问题
    if (localRouters != null && !localRouters.isEmpty()) {
        for (Router router : localRouters) {
            try {
                if (router.getUrl() == null || router.getUrl().getParameter(Constants.RUNTIME_KEY, false)) {
                    invokers = router.route(invokers, getConsumerUrl(), invocation);
                }
            } catch (Throwable t) {
                logger.error("Failed to execute router: " + getUrl() + ", cause: " + t.getMessage(), t);
            }
        }
    }
    return invokers;
}
```

---

- 第 7 行：调用 **抽象**#doList(invocation)方法，获得所有 Invoker 集合。代码如下：

```java
protected abstract List<Invoker<T>> doList(Invocation invocation) throws RpcException;
```

---

- 第 9 至 20 行：根据**路由规则( Router )**[《精尽 Dubbo 源码解析 —— 集群容错（七）之 Router 实现》](http://svip.iocoder.cn/Dubbo/cluster-7-impl-router/?self=)
，进一步筛选合适的 Invoker 集合。详细解析，见
。

# 4. RegistryDirectory

com.alibaba.dubbo.registry.integration.RegistryDirectory ，实现 NotifyListener 接口，实现 AbstractDirectory 抽象类，基于**注册中心**的 Directory 实现类。

1. RegistryDirectory 在
dubbo-registry
模块，
integration
包下，是 Dubbo 注册中心模块集成 Directory 的实现类。
2. RegistryDirectory 作为一个 NotifyListener ，**订阅监听**
注册中心( Registry ) 的数据，实现对变更的
。

## 4.1 构造方法

RegistryDirectory 的字段有 **17** 个，比较多，所以胖友请耐心。

```java // ========== Dubbo SPI Adaptive 对象 BEGIN ==========  /**  * Cluster$Adaptive 对象  */ private static final Cluster cluster = ExtensionLoader.getExtensionLoader(Cluster.class).getAdaptiveExtension(); /**  * RouterFactory$Adaptive 对象  */ private static final RouterFactory routerFactory = ExtensionLoader.getExtensionLoader(RouterFactory.class).getAdaptiveExtension(); /**  * ConfiguratorFactory$Adaptive 对象  */ private static final ConfiguratorFactory configuratorFactory = ExtensionLoader.getExtensionLoader(ConfiguratorFactory.class).getAdaptiveExtension();  // ========== 服务消费者相关 BEGIN ==========  /**  * 服务类型，例如：com.alibaba.dubbo.demo.DemoService  */ private final Class<T> serviceType; // Initialization at construction time, assertion not null /**  * Consumer URL 的配置项 Map  */ private final Map<String, String> queryMap; // Initialization at construction time, assertion not null /**  * 服务方法数组  */ private final String[] serviceMethods; /**  * 是否引用多分组  *  * 服务分组：http://dubbo.apache.org/zh-cn/docs/user/demos/service-group.html  */ private final boolean multiGroup;  // ========== 注册中心相关 BEGIN ==========  /**  * 注册中心的 Protocol 对象  */ private Protocol protocol; // Initialization at the time of injection, the assertion is not null /**  * 注册中心  */ private Registry registry; // Initialization at the time of injection, the assertion is not null /**  * 注册中心的服务类，目前是 com.alibaba.dubbo.registry.RegistryService  *  * 通过 {@link #url} 的 {@link URL#getServiceKey()} 获得  */ private final String serviceKey; // Initialization at construction time, assertion not null /**  * 是否禁止访问。  *  * 有两种情况会导致：  *  * 1. 没有服务提供者  * 2. 服务提供者被禁用  */ private volatile boolean forbidden = false;  // ========== 配置规则相关 BEGIN ==========  /**  * 原始的目录 URL  *  * 例如：zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=demo-consumer&callbacks=1000&check=false&client=netty4&cluster=failback&dubbo=2.0.0&interface=com.alibaba.dubbo.demo.DemoService&methods=sayHello,callbackParam,save,update,say03,delete,say04,demo,say01,bye,say02,saves&payload=1000&pid=63400&qos.port=33333&register.ip=192.168.16.23&sayHello.async=true&side=consumer&timeout=10000&timestamp=1527056491064  */ private final URL directoryUrl; // Initialization at construction time, assertion not null, and always assign non null value /**  * 覆写的目录 URL ，结合配置规则  */ private volatile URL overrideDirectoryUrl; // Initialization at construction time, assertion not null, and always assign non null value /**  * 配置规则数组  *  * override rules  * Priority: override>-D>consumer>provider  * Rule one: for a certain provider <ip:port,timeout=100>  * Rule two: for all providers <* ,timeout=5000>  */ private volatile List<Configurator> configurators; // The initial value is null and the midway may be assigned to null, please use the local variable reference  // ========== 服务提供者相关 BEGIN ==========  /**  * [url]与[服务提供者 Invoker 集合]的映射缓存  */ // Map<url, Invoker> cache service url to invoker mapping. private volatile Map<String, Invoker<T>> urlInvokerMap; // The initial value is null and the midway may be assigned to null, please use the local variable reference /**  * [方法名]与[服务提供者 Invoker 集合]的映射缓存  */ // Map<methodName, Invoker> cache service method to invokers mapping. private volatile Map<String, List<Invoker<T>>> methodInvokerMap; // The initial value is null and the midway may be assigned to null, please use the local variable reference /**  * [服务提供者 Invoker 集合]缓存  */ // Set<invokerUrls> cache invokeUrls to invokers mapping. private volatile Set<URL> cachedInvokerUrls; // The initial value is null and the midway may be assigned to null, please use the local variable reference  public RegistryDirectory(Class<T> serviceType, URL url) {     super(url);     if (serviceType == null) {         throw new IllegalArgumentException("service type is null.");     }     if (url.getServiceKey() == null || url.getServiceKey().length() == 0) {         throw new IllegalArgumentException("registry serviceKey is null.");     }     this.serviceType = serviceType;     this.serviceKey = url.getServiceKey();     // 获得 queryMap     this.queryMap = StringUtils.parseQueryString(url.getParameterAndDecoded(Constants.REFER_KEY));     // 获得 overrideDirectoryUrl 和 directoryUrl     this.overrideDirectoryUrl = this.directoryUrl = url.setPath(url.getServiceInterface()).clearParameters().addParameters(queryMap).removeParameter(Constants.MONITOR_KEY);     // 初始化 multiGroup     String group = directoryUrl.getParameter(Constants.GROUP_KEY, "");     this.multiGroup = group != null && ("*".equals(group) || group.contains(","));     // 初始化 serviceMethods     String methods = queryMap.get(Constants.METHODS_KEY);     this.serviceMethods = methods == null ? null : Constants.COMMA_SPLIT_PATTERN.split(methods); }
```

---

- 分成**五类**
变量。胖友自己看注释。
- 如果不理解，可以结合下面的具体方法的使用。 当然也可以给我留言，因为确实变量有点多和复杂。

## 4.2 subscribe

#subscribe(URL) 方法，向**注册中心**发起订阅。代码如下：

```java public void subscribe(URL url) {     // 设置消费者 URL     setConsumerUrl(url);     // 向注册中心，发起订阅     registry.subscribe(url, this); }
```

---

- 调用**父**
#setConsumerUrl(url)
方法，设置
consumerUrl
消费者 URL 。
- 调用
Registry#subscribe(url, NotifyListener)
方法，向注册中心，发起订阅。


服务消费者，再引用服务时，会创建 RegistryDirectory 对象，并发起**1）服务提供者 + 2）路由规则 + 3）配置规则**的数据订阅。如下图：

![doRefer流程](/assets/images/learning/dubbo/dubbo-cluster-fault-tolerance-directory-impl/b84a2bb52e510e78cb88f33e8019e3a7.png)

- 对应为
RegistryProtocol#doRefer(Cluster, Registry, Class type, URL url)
方法。

## 4.3 notify

在注册中心( Registry )发现数据发生变化时，会通知对应的 NotifyListener 们。如下图：

![notify流程](/assets/images/learning/dubbo/dubbo-cluster-fault-tolerance-directory-impl/fbc0f29179e205b29f2ee52d26c78fea.png)

- 对应为
AbstractRegistry#notify(URL url, NotifyListener, List urls)
方法。
- 因为 RegistryDirectory 作为一个 NotifyListener ，向注册中心( Registry )发起了订阅，所以此时会被通知。**注意，是按照分类循环通知的一次只有一类 URL**
，也就是说，
。

#notify(List urls)**实现**方法，代码如下：

```java
@Override
public synchronized void notify(List<URL> urls) {
    // 根据 URL 的分类或协议，分组成三个集合。
    List<URL> invokerUrls = new ArrayList<URL>(); // 服务提供者 URL 集合
    List<URL> routerUrls = new ArrayList<URL>();
    List<URL> configuratorUrls = new ArrayList<URL>();
    for (URL url : urls) {
        String protocol = url.getProtocol();
        String category = url.getParameter(Constants.CATEGORY_KEY, Constants.DEFAULT_CATEGORY);
        if (Constants.ROUTERS_CATEGORY.equals(category) || Constants.ROUTE_PROTOCOL.equals(protocol)) {
            routerUrls.add(url);
        } else if (Constants.CONFIGURATORS_CATEGORY.equals(category) || Constants.OVERRIDE_PROTOCOL.equals(protocol)) {
            configuratorUrls.add(url);
        } else if (Constants.PROVIDERS_CATEGORY.equals(category)) {
            invokerUrls.add(url);
        } else {
            logger.warn("Unsupported category " + category + " in notified url: " + url + " from registry " + getUrl().getAddress() + " to consumer " + NetUtils.getLocalHost());
        }
    }
    // 处理配置规则 URL 集合
    // configurators
    if (!configuratorUrls.isEmpty()) {
        this.configurators = toConfigurators(configuratorUrls);
    }
    // 处理路由规则 URL 集合
    // routers
    if (!routerUrls.isEmpty()) {
        List<Router> routers = toRouters(routerUrls);
        if (routers != null) { // null - do nothing
            setRouters(routers);
        }
    }
    // 合并配置规则，到 `directoryUrl` 中，形成 `overrideDirectoryUrl` 变量。
    List<Configurator> localConfigurators = this.configurators; // local reference
    // merge override parameters
    this.overrideDirectoryUrl = directoryUrl;
    if (localConfigurators != null && !localConfigurators.isEmpty()) {
        for (Configurator configurator : localConfigurators) {
            this.overrideDirectoryUrl = configurator.configure(overrideDirectoryUrl);
        }
    }
    // 处理服务提供者 URL 集合
    refreshInvoker(invokerUrls);
}
```

---

- **注意同步**
，这是一个
的方法。
- 第 3 至 19 行：根据 URL 的**分类三个1）服务提供者 + 2）路由规则 + 3）配置规则**
或协议，分成组
集合：
。
- 第 20 至 24 行：非空，调用 **配置规则**[「4.3.1 toConfigurators」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#toConfigurators(configuratorUrls)
方法，处理
URL 集合。详细解析，见
。
- 第 25 至 32 行：非空，调用 **路由规则**[「4.3.2 toRouters」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#toRouters(routerUrls)
方法，处理
URL 集合。详细解析，见
。
    - 若转换到 **父**
routers
非空，调用
#setRouters(routers)
方法，设置路由规则。
- 第 33 至 41 行：合并配置规则，到 directoryUrl 中，形成详见 [《精尽 Dubbo 源码解析 —— 集群容错（六）之 Configurator 实现》](http://svip.iocoder.cn/Dubbo/cluster-6-impl-configurator?self=) 的 [「4.1.2 mergeUrl」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)。
overrideDirectoryUrl
变量。详细解析，见
的
。
- 第 43 行：调用 **服务提供者**[「4.3.3 refreshInvoker」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#refreshInvoker(invokerUrls)
方法，处理
URL 集合。详细解析，见
。

### 4.3.1 toConfigurators

详细解析，见 [《精尽 Dubbo 源码解析 —— 集群容错（六）之 Configurator 实现》](http://svip.iocoder.cn/Dubbo/cluster-6-impl-configurator?self=) 的 [「4.1.1 toConfigurators」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#) 。

### 4.3.2 toRouters

详细解析，见 [《精尽 Dubbo 源码解析 —— 集群容错（七）之 Router 实现》](http://svip.iocoder.cn/Dubbo/cluster-7-impl-router/?self=) 。

## 4.7 内部类

### 4.7.1 InvokerDelegate

InvokerDelegate ，实现 com.alibaba.dubbo.rpc.protocol.InvokerWrapper 类，Invoker 代理类，主要用于存储**注册中心下发的 url 地址**( providerUrl )，用于重新重新 refer 时能够根据 providerURL queryMap overrideMap 重新组装。 代码如下：

老艿艿：目前貌似没看到这块逻辑噢

```java private static class InvokerDelegate<T> extends InvokerWrapper<T> {      /**      * 服务提供者 URL      *      * 未经过配置合并      */     private URL providerUrl;      public InvokerDelegate(Invoker<T> invoker, URL url, URL providerUrl) {         super(invoker, url);         this.providerUrl = providerUrl;     }      public URL getProviderUrl() {         return providerUrl;     }  }
```

---

### 4.7.2 InvokerComparator

InvokerComparator ，实现 Comparator 接口，Invoker 排序器实现类，**根据 URL 升序** 。代码如下：

```java private static class InvokerComparator implements Comparator<Invoker<?>> {      /**      * 单例      */     private static final InvokerComparator comparator = new InvokerComparator();      private InvokerComparator() {     }      public static InvokerComparator getComparator() {         return comparator;     }      @Override     public int compare(Invoker<?> o1, Invoker<?> o2) {         return o1.getUrl().toString().compareTo(o2.getUrl().toString());     }  }
```

---

### 4.3.3 refreshInvoker

#refreshInvoker(List invokerUrls) 方法，官方注释其如下：

根据 invokerURL 列表转换为 invoker 列表。转换规则如下：

3. 如果 url 已经被转换为 invoker ，则不在重新引用，直接从缓存中获取，注意如果 url 中任何一个参数变更也会重新引用
4. 如果传入的 invoker 列表不为空，则表示最新的 invoker 列表
5. 如果传入的 invokerUrl 列表是空，则表示只是下发的 override 规则或 route 规则，需要重新交叉对比，决定是否需要重新引用。
- 是不是看起来有点点懵逼？淡定，我们来看看代码。

```java
private void refreshInvoker(List<URL> invokerUrls) {
    if (invokerUrls != null && invokerUrls.size() == 1 && invokerUrls.get(0) != null
            && Constants.EMPTY_PROTOCOL.equals(invokerUrls.get(0).getProtocol())) {
        // 设置禁止访问
        this.forbidden = true; // Forbid to access
        // methodInvokerMap 置空
        this.methodInvokerMap = null; // Set the method invoker map to null
        // 销毁所有 Invoker 集合
        destroyAllInvokers(); // Close all invokers
    } else {
        // 设置允许访问
        this.forbidden = false; // Allow to access
        // 引用老的 urlInvokerMap
        Map<String, Invoker<T>> oldUrlInvokerMap = this.urlInvokerMap; // local reference
        // 传入的 invokerUrls 为空，说明是路由规则或配置规则发生改变，此时 invokerUrls 是空的，直接使用 cachedInvokerUrls。
        if (invokerUrls.isEmpty() && this.cachedInvokerUrls != null) {
            invokerUrls.addAll(this.cachedInvokerUrls);
        // 传入的 invokerUrls 非空，更新 cachedInvokerUrls。
        } else {
            this.cachedInvokerUrls = new HashSet<URL>();
            this.cachedInvokerUrls.addAll(invokerUrls); //Cached invoker urls, convenient for comparison //缓存invokerUrls列表，便于交叉对比
        }
        // 忽略，若无 invokerUrls
        if (invokerUrls.isEmpty()) {
            return;
        }
        // 将传入的 invokerUrls ，转成新的 urlInvokerMap
        Map<String, Invoker<T>> newUrlInvokerMap = toInvokers(invokerUrls);// Translate url list to Invoker map
        // 转换出新的 methodInvokerMap
        Map<String, List<Invoker<T>>> newMethodInvokerMap = toMethodInvokers(newUrlInvokerMap); // Change method name to map Invoker Map
        // state change
        // If the calculation is wrong, it is not processed. 如果计算错误，则不进行处理.
        if (newUrlInvokerMap == null || newUrlInvokerMap.size() == 0) {
            logger.error(new IllegalStateException("urls to invokers error .invokerUrls.size :" + invokerUrls.size() + ", invoker.size :0. urls :" + invokerUrls.toString()));
            return;
        }
        // 若服务引用多 group ，则按照 method + group 聚合 Invoker 集合
        this.methodInvokerMap = multiGroup ? toMergeMethodInvokerMap(newMethodInvokerMap) : newMethodInvokerMap;
        this.urlInvokerMap = newUrlInvokerMap;
        // 销毁不再使用的 Invoker 集合
        try {
            destroyUnusedInvokers(oldUrlInvokerMap, newUrlInvokerMap); // Close the unused Invoker
        } catch (Exception e) {
            logger.warn("destroyUnusedInvokers error. ", e);
        }
    }
}
```

---

- ========== 第一部分 ==========
- 第 2 至 3 行：当 **1下线**
invokerUrls
集合大小为
，并且协议为
empty://
，说明所有服务提供者都已经
。若注册中心为 Zookeeper ，可参见
ZookeeperRegistry#toUrlsWithEmpty(URL consumer, String path, List providers)
方法。
- 第 5 行：设置**禁止**
访问，因为没有服务提供者了。
- 第 7 行：
methodInvokerMap
置空。
- 第 9 行：调用 [「4.3.3.5 destroyAllInvokers」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#destroyAllInvokers()
方法，销毁所有服务提供者 Invoker 集合。详细解析，见
。
- ========== 第二部分 ==========
- 第 12 行：设置**允许**
访问，因为有服务提供者了。
- 第 15 至 17 行：传入的 **说明是路由规则或配置规则发生改变**
invokerUrls
为空，
，此时
invokerUrls
是空的，直接使用
cachedInvokerUrls
。对应官方注释【第 3 点】（部分，不包括"需要重新交叉对比，决定是否需要重新引用"）。
- 第 18 至 22 行：传入的 **新的**
invokerUrls
非空，更新
cachedInvokerUrls
。考虑到并发的问题，更新的方式为创建
HashSet 。对应官方注释【第 2 点】。
    - 为什么【第 15 至 17 行】**不需要更新**
呢？因为
invokerUrls
为空，直接使用
cachedInvokerUrls
，相当于进行了"更新"。
- 第 23 至 26 行：忽略，若无
invokerUrls
。出现情况为，初始是按照
configurators => routers => providers
，所以前两个会出现这个情况。关于这一点，胖友可以调试感受下。
- 第 28 行：调用 **新的**[「4.3.3.1 toInvokers」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#toInvokers(List urls)
方法，将传入的
invokerUrls
，转换成
urlInvokerMap
。详细解析，见
。
- 第 30 行：调用 **新的**[「4.3.3.2 toMethodInvokers」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#toMethodInvokers(newUrlInvokerMap)
方法，将
urlInvokerMap
转成与方法的映射关系，即
methodInvokerMap
。详细解析，见
。
- 第 31 至 36 行：如果计算错误，则不进行处理。一般来说，是防御性编程。
- 第 38 行：若服务引用**多method + group**[「4.3.3.3 toMethodInvokers」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
group ，则调用
#toMergeMethodInvokerMap(newMethodInvokerMap)
方法，按照
聚合 Invoker 集合。详细解析，见
。
- 第 39 行：赋值
urlInvokerMap
属性。
- 第 40 至 45 行：调用 **销毁**[「4.3.3.4 toMethodInvokers」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#destroyUnusedInvokers(oldUrlInvokerMap, newUrlInvokerMap)
方法，
不再使用的 Invoker 集合。详细解析，见
。

### 4.3.3.1 toInvokers

#toInvokers(List urls) 方法，

```java
private Map<String, Invoker<T>> toInvokers(List<URL> urls) {
    // 新的 `newUrlInvokerMap`
    Map<String, Invoker<T>> newUrlInvokerMap = new HashMap<String, Invoker<T>>();
    // 若为空，直接返回
    if (urls == null || urls.isEmpty()) {
        return newUrlInvokerMap;
    }
    // 已初始化的服务器提供 URL 集合
    Set<String> keys = new HashSet<String>();
    // 获得引用服务的协议
    String queryProtocols = this.queryMap.get(Constants.PROTOCOL_KEY);
    // 循环服务提供者 URL 集合，转成 Invoker 集合
    for (URL providerUrl : urls) {
        // If protocol is configured at the reference side, only the matching protocol is selected
        // 如果 reference 端配置了 protocol ，则只选择匹配的 protocol
        if (queryProtocols != null && queryProtocols.length() > 0) {
            boolean accept = false;
            String[] acceptProtocols = queryProtocols.split(","); // 可配置多个协议
            for (String acceptProtocol : acceptProtocols) {
                if (providerUrl.getProtocol().equals(acceptProtocol)) {
                    accept = true;
                    break;
                }
            }
            if (!accept) {
                continue;
            }
        }
        // 忽略，若为 `empty://` 协议
        if (Constants.EMPTY_PROTOCOL.equals(providerUrl.getProtocol())) {
            continue;
        }
        // 忽略，若应用程序不支持该协议
        if (!ExtensionLoader.getExtensionLoader(Protocol.class).hasExtension(providerUrl.getProtocol())) {
            logger.error(new IllegalStateException("Unsupported protocol " + providerUrl.getProtocol() + " in notified url: " + providerUrl + " from registry " + getUrl().getAddress() + " to consumer " + NetUtils.getLocalHost()
                    + ", supported protocol: " + ExtensionLoader.getExtensionLoader(Protocol.class).getSupportedExtensions()));
            continue;
        }
        // 合并 URL 参数
        URL url = mergeUrl(providerUrl);
        // 忽略，若已经初始化
        String key = url.toFullString(); // The parameter urls are sorted
        if (keys.contains(key)) { // Repeated url
            continue;
        }
        // 添加到 `keys` 中
        keys.add(key);
        // Cache key is url that does not merge with consumer side parameters, regardless of how the consumer combines parameters, if the server url changes, then refer again
        // 如果服务端 URL 发生变化，则重新 refer 引用
        Map<String, Invoker<T>> localUrlInvokerMap = this.urlInvokerMap; // local reference
        Invoker<T> invoker = localUrlInvokerMap == null ? null : localUrlInvokerMap.get(key);
        if (invoker == null) { // Not in the cache, refer again 未在缓存中，重新引用
            try {
                // 判断是否开启
                boolean enabled;
                if (url.hasParameter(Constants.DISABLED_KEY)) {
                    enabled = !url.getParameter(Constants.DISABLED_KEY, false);
                } else {
                    enabled = url.getParameter(Constants.ENABLED_KEY, true);
                }
                // 若开启，创建 Invoker 对象
                if (enabled) {
                    // 注意，引用服务
                    invoker = new InvokerDelegate<T>(protocol.refer(serviceType, url), url, providerUrl);
                }
            } catch (Throwable t) {
                logger.error("Failed to refer invoker for interface:" + serviceType + ",url:(" + url + ")" + t.getMessage(), t);
            }
            // 添加到 newUrlInvokerMap 中
            if (invoker != null) { // Put new invoker in cache
                newUrlInvokerMap.put(key, invoker);
            }
        } else { // 在缓存中，直接使用缓存的 Invoker 对象，添加到 newUrlInvokerMap 中
            newUrlInvokerMap.put(key, invoker);
        }
    }
    // 清空 keys
    keys.clear();
    return newUrlInvokerMap;
}
```

---

- 第 3 行：
newUrlInvokerMap
变量，新的
urlInvokerMap
字段，后面会赋值给它。
- 第 4 至 7 行：若
urls
为空，直接返回，防御性编程。
- 第 9 行：**已初始化**
keys
变量，
的服务器提供 URL 集合，即服务提供者 URL 已经处理。
- 第 11 行：获得引用服务的协议。一般情况下，我们不会设置
配置项。
- 第 13 行：**循环**
urls
集合，转成 Invoker 集合。
- 协议处理相关
    - 第 14 至 28 行：如果 reference 端配置了 protocol ，则**只选择匹配**
的 protocol 。
    - 第 29 至 32 行：**忽略**
，若为
empty://
协议。
    - 第 33 至 38 行：**忽略**
，若应用程序不支持该协议。
- 第 40 行：调用 **合并**[「4.3.3.1 mergeUrl」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
#mergeUrl(providerUrl)
方法，
URL 参数。详细解析，见
。
- 第 41 至 47 行：**忽略**
，通过
keys
判断已经初始化。
    - 若未初始化，添加到
keys
中。
- 第 48 至 75 行："创建"服务 Invoker 对象。
    - 第 50 至 51 行：获得
url
对应在
localUrlInvokerMap
缓存的 Invoker 对象。
    - 第 52 至 72 行：不在缓存中，需要重新 refer 引用，创建 Invoker 对象。
        - 第 54 至 60 行：通过配置项
enable
和
disable
判断，服务是否开启。
        - 第 61 至 65 行： 若开启，创建 Invoker 对象。
            - 【重要】**第 64 行：调用 Protocol$Adaptive#refer(serviceType, url) 方法，引用服务，创建服务提供者 Invoker 对象**[《精尽 Dubbo 源码解析 —— 服务引用》](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
。详细解析，在
已经有了。
            - 第 64 行：创建 InvokerDelegate 对象。详细解析，见 [「4.7.1 InvokerDelegate」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
。
    - 第 73 至 75 行：在缓存中，直接使用缓存的 Invoker 对象，添加到
newUrlInvokerMap
中。
- 第 78 行：清空
keys
。
- 第 79 行：返回结果
newUrlInvokerMap
。

### 4.3.3.1.1 mergeUrl

#mergeUrl(providerUrl) 方法，合并 URL 参数，**优先级**为配置规则 > 服务消费者配置 > 服务提供者配置。代码如下：

```java 1: private URL mergeUrl(URL providerUrl) {  2:     // 合并消费端参数  3:     providerUrl = ClusterUtils.mergeUrl(providerUrl, queryMap); // Merge the consumer side parameters  4:   5:     // 合并配置规则  6:     List<Configurator> localConfigurators = this.configurators; // local reference  7:     if (localConfigurators != null && !localConfigurators.isEmpty()) {  8:         for (Configurator configurator : localConfigurators) {  9:             providerUrl = configurator.configure(providerUrl); 10:         } 11:     } 12:  13:     // 不检查连接是否成功，总是创建 Invoker ！ 14:     providerUrl = providerUrl.addParameter(Constants.CHECK_KEY, String.valueOf(false)); // Do not check whether the connection is successful or not, always create Invoker! 15:  16:     // The combination of directoryUrl and override is at the end of notify, which can't be handled here 17:     // 仅合并提供者参数，因为 directoryUrl 与 override 合并是在 notify 的最后，这里不能够处理 18:     this.overrideDirectoryUrl = this.overrideDirectoryUrl.addParametersIfAbsent(providerUrl.getParameters()); // Merge the provider side parameters // 合并提供者参数 19:  20:     // 【忽略】因为是对 1.0 版本的兼容 21:     if ((providerUrl.getPath() == null || providerUrl.getPath().length() == 0) 22:             && "dubbo".equals(providerUrl.getProtocol())) { // Compatible version 1.0 23:         //fix by tony.chenl DUBBO-44 24:         String path = directoryUrl.getParameter(Constants.INTERFACE_KEY); 25:         if (path != null) { 26:             int i = path.indexOf('/'); 27:             if (i >= 0) { 28:                 path = path.substring(i + 1); 29:             } 30:             i = path.lastIndexOf(':'); 31:             if (i >= 0) { 32:                 path = path.substring(0, i); 33:             } 34:             providerUrl = providerUrl.setPath(path); 35:         } 36:     } 37:  38:     // 返回服务提供者 URL 39:     return providerUrl; 40: }
```

---

- 【**重要**[「6. ClusterUtils」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
】第 3 行：调用
ClusterUtils#mergeUrl(providerUrl, queryMap)
方法，合并服务消费者配置到
providerUrl
。详细解析，见
。
- 第 5 至 11 行：合并**配置规则**[《精尽 Dubbo 源码解析 —— 集群容错（六）之 Configurator 实现》](http://svip.iocoder.cn/Dubbo/cluster-6-impl-configurator/?self=)
到
providerUrl
中。详细解析，见
- 第 14 行：设置
providerUrl
不检查连接是否成功，总是创建 Invoker ！
- 第 18 行：仅合并提供者参数。详细解析，见 [《精尽 Dubbo 源码解析 —— 集群容错（六）之 Configurator 实现》](http://svip.iocoder.cn/Dubbo/cluster-6-impl-configurator/?self=)
- 第 20 至 36 行：【**忽略**
】因为是对 1.0 版本的兼容。

### 4.3.3.2 toMethodInvokers

#toMethodInvokers(Map<String, Invoker> invokersMap) 方法，将 invokersMap 转成**与方法**的映射关系。代码如下：

```java 1: private Map<String, List<Invoker<T>>> toMethodInvokers(Map<String, Invoker<T>> invokersMap) {  2:     // 创建新的 `methodInvokerMap`  3:     Map<String, List<Invoker<T>>> newMethodInvokerMap = new HashMap<String, List<Invoker<T>>>();  4:     // 创建 Invoker 集合  5:     List<Invoker<T>> invokersList = new ArrayList<Invoker<T>>();  6:     // According to the methods classification declared by the provider URL, the methods is compatible with the registry to execute the filtered methods  7:     // 按服务提供者 URL 所声明的 methods 分类，兼容注册中心执行路由过滤掉的 methods  8:     if (invokersMap != null && invokersMap.size() > 0) {  9:         // 循环每个服务提供者 Invoker 10:         for (Invoker<T> invoker : invokersMap.values()) { 11:             String parameter = invoker.getUrl().getParameter(Constants.METHODS_KEY); // methods 12:             if (parameter != null && parameter.length() > 0) { 13:                 String[] methods = Constants.COMMA_SPLIT_PATTERN.split(parameter); 14:                 if (methods != null && methods.length > 0) { 15:                     // 循环每个方法，按照方法名为维度，聚合到 `methodInvokerMap` 中 16:                     for (String method : methods) { 17:                         if (method != null && method.length() > 0 && !Constants.ANY_VALUE.equals(method)) { // 当服务提供者的方法为 "*" ，代表泛化调用 18:                             List<Invoker<T>> methodInvokers = newMethodInvokerMap.get(method); 19:                             if (methodInvokers == null) { 20:                                 methodInvokers = new ArrayList<Invoker<T>>(); 21:                                 newMethodInvokerMap.put(method, methodInvokers); 22:                             } 23:                             methodInvokers.add(invoker); 24:                         } 25:                     } 26:                 } 27:             } 28:             // 添加到 `invokersList` 中 29:             invokersList.add(invoker); 30:         } 31:     } 32:     // 路由全 `invokersList` ，匹配合适的 Invoker 集合。 33:     List<Invoker<T>> newInvokersList = route(invokersList, null); 34:     // 添加 `newInvokersList` 到 `newMethodInvokerMap` 中，表示该服务提供者的全量 Invoker 集合 35:     newMethodInvokerMap.put(Constants.ANY_VALUE, newInvokersList); 36:     // 循环，基于每个方法路由，匹配合适的 Invoker 集合 37:     if (serviceMethods != null && serviceMethods.length > 0) { 38:         for (String method : serviceMethods) { 39:             List<Invoker<T>> methodInvokers = newMethodInvokerMap.get(method); 40:             if (methodInvokers == null || methodInvokers.isEmpty()) { 41:                 methodInvokers = newInvokersList; 42:             } 43:             newMethodInvokerMap.put(method, route(methodInvokers, method)); 44:         } 45:     } 46:     // 循环排序每个方法的 Invoker 集合，并设置为不可变 47:     // sort and unmodifiable 48:     for (String method : new HashSet<String>(newMethodInvokerMap.keySet())) { 49:         List<Invoker<T>> methodInvokers = newMethodInvokerMap.get(method); 50:         Collections.sort(methodInvokers, InvokerComparator.getComparator()); 51:         newMethodInvokerMap.put(method, Collections.unmodifiableList(methodInvokers)); 52:     } 53:     return Collections.unmodifiableMap(newMethodInvokerMap); 54: }
```

---

- 第 3 行：
newMethodInvokerMap
变量，新的
methodInvokerMap
字段，后面会赋值给它。
- 第 5 行：创建 Invoker 集合。在【第 29 行】，我们可以看到，实际就是
invokersMap
的值的集合。
- 第 8 至 31 行：按照方法名为**维度对应的 Invoker 集合**
( KEY ) ，聚合
到
newMethodInvokerMap
中。
- 第 33 行：路由全 [《精尽 Dubbo 源码解析 —— 集群容错（七）之 Router 实现》](http://svip.iocoder.cn/Dubbo/cluster-7-impl-router/?self=)
invokersList
，匹配合适的 Invoker 集合。详细解析，见
。
- 第 35 行：添加 **全量**
newInvokersList
到
newMethodInvokerMap
中，表示该服务提供者的
Invoker 集合。
- 第 36 至 45 行：**循环**[《精尽 Dubbo 源码解析 —— 集群容错（七）之 Router 实现》](http://svip.iocoder.cn/Dubbo/cluster-7-impl-router/?self=)
，基于每个方法路由，匹配合适的 Invoker 集合。详细解析，见
。
- 第 46 至 53 行：循环**排序不可变**
每个方法的 Invoker 集合，并设置为
。

### 4.3.3.3 toMergeMethodInvokerMap

#toMergeMethodInvokerMap(Map<String, List<Invoker>> methodMap) ，按照 **method + group** 聚合 Invoker 集合。代码如下：

```java 1: private Map<String, List<Invoker<T>>> toMergeMethodInvokerMap(Map<String, List<Invoker<T>>> methodMap) {  2:     Map<String, List<Invoker<T>>> result = new HashMap<String, List<Invoker<T>>>();  3:     // 循环方法，按照 method + group 聚合 Invoker 集合  4:     for (Map.Entry<String, List<Invoker<T>>> entry : methodMap.entrySet()) {  5:         String method = entry.getKey();  6:         List<Invoker<T>> invokers = entry.getValue();  7:         // 按照 Group 聚合 Invoker 集合的结果。其中，KEY：group VALUE：Invoker 集合。  8:         Map<String, List<Invoker<T>>> groupMap = new HashMap<String, List<Invoker<T>>>();  9:         // 循环 Invoker 集合，按照 group 聚合 Invoker 集合 10:         for (Invoker<T> invoker : invokers) { 11:             String group = invoker.getUrl().getParameter(Constants.GROUP_KEY, ""); 12:             List<Invoker<T>> groupInvokers = groupMap.get(group); 13:             if (groupInvokers == null) { 14:                 groupInvokers = new ArrayList<Invoker<T>>(); 15:                 groupMap.put(group, groupInvokers); 16:             } 17:             groupInvokers.add(invoker); 18:         } 19:         // 大小为 1，使用第一个 20:         if (groupMap.size() == 1) { 21:             result.put(method, groupMap.values().iterator().next()); 22:         // 大于 1，将每个 Group 的 Invoker 集合，创建成 Cluster Invoker 对象。 23:         } else if (groupMap.size() > 1) { 24:             List<Invoker<T>> groupInvokers = new ArrayList<Invoker<T>>(); 25:             for (List<Invoker<T>> groupList : groupMap.values()) { 26:                 groupInvokers.add(cluster.join(new StaticDirectory<T>(groupList))); 27:             } 28:             result.put(method, groupInvokers); 29:         // 大小为 0 ，使用原有值 30:         } else { 31:             result.put(method, invokers); 32:         } 33:     } 34:     return result; 35: }
```

---

- 第 2 行：**新的**
result
属性，
methodInvokerMap
字段，后面会赋值给它。
- 第 3 终 33 行：**循环method + group**
，按照
聚合 Invoker 集合。
    - 第 8 行： 按照 Group 聚合 Invoker 集合的结果。其中，**KEYVALUE**
：group ，
：Invoker 集合。
    - 第 9 至 18 行：**循环group**
Invoker 集合，按照
聚合 Invoker 集合。
    - ========== 结果
groupMap
处理 ==========
    - 第 19 至 21 行：若数量为 1 ，使用第一个。
    - 第 29 至 32 行：若数量为 0 ，使用原有值 **等价**
invokers
。实际上，和【第 19 至 21 行】
。
    - 第 22 至 28 行：若数量**大于每个**
1 ，循环
Group 的 Invoker 集合，调用
Cluster$Adaptive#join(Directory)
方法，创建对应的 Cluster Invoker 对象。
        - 我们发现，此处创建 **StaticDirectory**[「5. StaticDirectory」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#)
对象。详细解析，见
。

那么，引用多个服务分组有什么用呢？为什么要按照 **group** 进行聚合，直接调用不可以么？让我们来打开 ProtocolRegistry#refer(Class type, URL url) 方法，如下图所示：

![refer流程](/assets/images/learning/dubbo/dubbo-cluster-fault-tolerance-directory-impl/325dc718b4dca8f5753059a01185c48d.png)

- 当引用多个服务分组时，会**自动分组聚合**
使用到
的特性。那么之后 MergeableCluster 会怎么做呢？详细解析，见后文 。

### 4.3.3.4 destroyUnusedInvokers

#destroyUnusedInvokers(oldUrlInvokerMap, newUrlInvokerMap) 方法，**销毁**不再使用的 Invoker 集合。代码如下：

```java private void destroyUnusedInvokers(Map<String, Invoker<T>> oldUrlInvokerMap, Map<String, Invoker<T>> newUrlInvokerMap) {     // 防御性编程，目前不存在这个情况     if (newUrlInvokerMap == null || newUrlInvokerMap.size() == 0) {         // 销毁所有服务提供者 Invoker         destroyAllInvokers();         return;     }     // check deleted invoker     // 对比新老集合，计算需要销毁的 Invoker 集合     List<String> deleted = null;     if (oldUrlInvokerMap != null) {         Collection<Invoker<T>> newInvokers = newUrlInvokerMap.values();         for (Map.Entry<String, Invoker<T>> entry : oldUrlInvokerMap.entrySet()) {             // 若不存在，添加到 `deleted` 中             if (!newInvokers.contains(entry.getValue())) {                 if (deleted == null) {                     deleted = new ArrayList<String>();                 }                 deleted.add(entry.getKey());             }         }     }      // 若有需要销毁的 Invoker ，则进行销毁     if (deleted != null) {         for (String url : deleted) {             if (url != null) {                 // 移除出 `urlInvokerMap`                 Invoker<T> invoker = oldUrlInvokerMap.remove(url);                 if (invoker != null) {                     try {                         // 销毁 Invoker                         invoker.destroy();                         if (logger.isDebugEnabled()) {                             logger.debug("destroy invoker[" + invoker.getUrl() + "] success. ");                         }                     } catch (Exception e) {                         logger.warn("destroy invoker[" + invoker.getUrl() + "] failed. " + e.getMessage(), e);                     }                 }             }         }     } }
```

---

### 4.3.3.5 destroyAllInvokers

#destroyAllInvokers() 方法，销毁所有服务提供者 Invoker 。代码如下：

```java private void destroyAllInvokers() {     Map<String, Invoker<T>> localUrlInvokerMap = this.urlInvokerMap; // local reference 本地引用，避免并发问题     if (localUrlInvokerMap != null) {         // 循环 urlInvokerMap ，销毁所有服务提供者 Invoker         for (Invoker<T> invoker : new ArrayList<Invoker<T>>(localUrlInvokerMap.values())) {             try {                 invoker.destroy();             } catch (Throwable t) {                 logger.warn("Failed to destroy service " + serviceKey + " to provider " + invoker.getUrl(), t);             }         }         // urlInvokerMap 清空         localUrlInvokerMap.clear();     }     // methodInvokerMap 置空     methodInvokerMap = null; }
```

---

## 4.4 doList

#doList(Invocation)**实现**方法，获得对应的 Invoker 集合。代码如下：

```java 1: @Override  2: public List<Invoker<T>> doList(Invocation invocation) {  3:     if (forbidden) {  4:         // 1. No service provider 2. Service providers are disabled  5:         throw new RpcException(RpcException.FORBIDDEN_EXCEPTION,  6:             "No provider available from registry " + getUrl().getAddress() + " for service " + getConsumerUrl().getServiceKey() + " on consumer " +  NetUtils.getLocalHost()  7:                     + " use dubbo version " + Version.getVersion() + ", please check status of providers(disabled, not registered or in blacklist).");  8:     }  9:     List<Invoker<T>> invokers = null; 10:     Map<String, List<Invoker<T>>> localMethodInvokerMap = this.methodInvokerMap; // local reference 11:     // 获得 Invoker 集合 12:     if (localMethodInvokerMap != null && localMethodInvokerMap.size() > 0) { 13:         // 获得方法名、方法参数 14:         String methodName = RpcUtils.getMethodName(invocation); 15:         Object[] args = RpcUtils.getArguments(invocation); 16:         // 【第一】可根据第一个参数枚举路由 17:         if (args != null && args.length > 0 && args[0] != null 18:                 && (args[0] instanceof String || args[0].getClass().isEnum())) { 19: //            invokers = localMethodInvokerMap.get(methodName + "." + args[0]); // The routing can be enumerated according to the first parameter 20:             invokers = localMethodInvokerMap.get(methodName + args[0]); // The routing can be enumerated according to the first parameter 21:         } 22:         // 【第二】根据方法名获得 Invoker 集合 23:         if (invokers == null) { 24:             invokers = localMethodInvokerMap.get(methodName); 25:         } 26:         // 【第三】使用全量 Invoker 集合。例如，`#$echo(name)` ，回声方法 27:         if (invokers == null) { 28:             invokers = localMethodInvokerMap.get(Constants.ANY_VALUE); 29:         } 30:         // 【第四】使用 `methodInvokerMap` 第一个 Invoker 集合。防御性编程。 31:         if (invokers == null) { 32:             Iterator<List<Invoker<T>>> iterator = localMethodInvokerMap.values().iterator(); 33:             if (iterator.hasNext()) { 34:                 invokers = iterator.next(); 35:             } 36:         } 37:     } 38:     return invokers == null ? new ArrayList<Invoker<T>>(0) : invokers; 39: }
```

---

- 通过四种方式，从
methodInvokerMap
中，获得对应的 Invoker 集合。
- 第一种，可根据**第一个参数**
枚举路由。这是个非常小众的场景，胖友不必理解。例子如下：

```java // DemoService 接口定义 public interface DemoService {     void hello(String name);      void hello01(String name);      void hello02(String name); }  // 消费者调用 DemoService demoService = (DemoService) context.getBean("demoService"); demoService.hello("01");
```

---

```java
- 通过这样的方式，调用到的服务提供者的 </font>DemoServiceImpl#hello01(name)</font> 方法。- 如果使用该</font>**特性</font>**，注意避免出现</font>**无关</font>**的几个方法，例如 </font>#hello(name)</font> 和 </font>#hello01(name)</font> 是毫无关系的两个方法，而我真的想调用 </font>#hello(name)</font> 方法，结果调用到了 </font>#hello01(name)</font> 方法。- 如下是 Dubbo Commiter </font>**诣极</font>** 的解惑，非常感谢。</font>动态的方法名本身就是接口中已经定义的</font>举个例子吧借口定义了 method, method1,method2， 如果我发起rpc调用method(1, 2, 3), 这个时候会去查找方法method1的invokers， 如果我这个时候发起rpc method(2, 1, 3), 这个时候会去查找方法method2的invokers， 然后调用invokers的method方法    * 另外，经过沟通，【第 19 行】的 </font>"."</font> 是个 BUG ，方法里不能包含该字符，因此，笔者改成了【第 20 行】，去掉了 </font>"."</font> 进行测试。```

- 第二种，根据**方法名**
获得 Invoker 集合。一般情况下，都能匹配到。
- 第三种，使用全量 Invoker 集合。例如，
#$echo(name)
回声方法。
- 第四种，使用
methodInvokerMap
第一个 Invoker 集合。防御性编程。

## 4.5 isAvailable

```java @Override public boolean isAvailable() {     // 若已销毁，返回不可用     if (isDestroyed()) {         return false;     }     // 任意一个 Invoker 可用，则返回可用     Map<String, Invoker<T>> localUrlInvokerMap = urlInvokerMap;     if (localUrlInvokerMap != null && localUrlInvokerMap.size() > 0) {         for (Invoker<T> invoker : new ArrayList<Invoker<T>>(localUrlInvokerMap.values())) {             if (invoker.isAvailable()) {                 return true;             }         }     }     return false; }
```

---

## 4.6 destroy

```java @Override public void destroy() {     if (isDestroyed()) {         return;     }     // 取消订阅     // unsubscribe.     try {         if (getConsumerUrl() != null && registry != null && registry.isAvailable()) {             registry.unsubscribe(getConsumerUrl(), this);         }     } catch (Throwable t) {         logger.warn("unexpeced error when unsubscribe service " + serviceKey + "from registry" + registry.getUrl(), t);     }     // 标记已经销毁     super.destroy(); // must be executed after unsubscribing     // 销毁所有 Invoker      try {         destroyAllInvokers();     } catch (Throwable t) {         logger.warn("Failed to destroy service " + serviceKey, t);     } }
```

---

# 5. StaticDirectory

com.alibaba.dubbo.rpc.cluster.directory.StaticDirectory ，实现 AbstractDirectory 抽象类，**静态** Directory 实现类。逻辑比较简单，将传入的 invokers 集合，封装成静态的 Directory 对象。代码如下：

```java public class StaticDirectory<T> extends AbstractDirectory<T> {      /**      * Invoker 集合      */     private final List<Invoker<T>> invokers;      public StaticDirectory(List<Invoker<T>> invokers) {         this(null, invokers, null);     }      public StaticDirectory(List<Invoker<T>> invokers, List<Router> routers) {         this(null, invokers, routers);     }      public StaticDirectory(URL url, List<Invoker<T>> invokers) {         this(url, invokers, null);     }      public StaticDirectory(URL url, List<Invoker<T>> invokers, List<Router> routers) {         // 默认使用 `url` 参数。当它为空时，使用 `invokers[0].url` 。         super(url == null && invokers != null && !invokers.isEmpty() ? invokers.get(0).getUrl() : url, routers);         if (invokers == null || invokers.isEmpty()) {             throw new IllegalArgumentException("invokers == null");         }         this.invokers = invokers;     }      @Override     public Class<T> getInterface() {         return invokers.get(0).getInterface();     }      @Override     public boolean isAvailable() {         // 若已经销毁，则不可用         if (isDestroyed()) {             return false;         }         // 任一一个 Invoker 可用，则为可用         for (Invoker<T> invoker : invokers) {             if (invoker.isAvailable()) {                 return true;             }         }         return false;     }      @Override     public void destroy() {         // 若已经销毁， 跳过         if (isDestroyed()) {             return;         }         // 销毁         super.destroy();         // 销毁每个 Invoker         for (Invoker<T> invoker : invokers) {             invoker.destroy();         }         // 清空 Invoker 集合         invokers.clear();     }      @Override     protected List<Invoker<T>> doList(Invocation invocation) throws RpcException {         return invokers;     }  }
```

---

- 代码比较易懂，胖友自己看下。

---

除了在 [「4.3.3.3 toMergeMethodInvokerMap」](http://svip.iocoder.cn/Dubbo/cluster-3-impl-directory/#) 方法中，使用到了 StaticDirectory 对象。我们来看看 ReferenceConfig#createProxy(Map<String, String> map) 的使用，代码如下图：

![createProxy流程](/assets/images/learning/dubbo/dubbo-cluster-fault-tolerance-directory-impl/2fc2ba339c0e57e1ac30a9ea7c5b376c.png)

- 第 522 至 527 行：当 **有注册中心仅调用第一个可用的 Invoker 对象**
registryURL
非空时，意味着
，使用
cluster=available
集群方式，并调用
Cluster$Adaptive#join(StaticDirectory)
方法，创建对应的 Cluster Invoker 对象。这意味着，服务调用时，因为使用的是
cluster=available
，
。下面，我们来做一个 YY ：
    - 目前我们有 A , B 两个机房，分别对应 zk01 集群，zk02 集群。这两个 zk 集群**不互通**
。
    - A , B 机房，分别部署了 **User 服务提供者**
，仅注册到自己机房的 zk 集群。
    - A , B 机房，部署了对应的 **User 服务消费User 服务提供者**
，那么如果我们希望优先调用本机房。当本机房
全挂的情况下，使用另外一个机房，该如何配置呢？

```java // A 机房 <dubbo:reference interface="com.alibaba.dubbo.demo.UserService" registry="zk01,zk02" /> // B 机房 <dubbo:reference interface="com.alibaba.dubbo.demo.UserService" registry="zk02,zk01" />
```

---

```java
    * 即在 </font>"registry"</font> 配置项中，将自己的 zk 集群放在前面。    * 当然，大多数情况下，很少会出现一个机房服务提供者全挂，zk 集群还存活着。```

# 6. ClusterUtils

com.alibaba.dubbo.rpc.cluster.support.ClusterUtils ，Cluster 工具类。代码如下：

```java 1: public class ClusterUtils {  2:  3:     private ClusterUtils() {  4:     }  5:  6:     public static URL mergeUrl(URL remoteUrl, Map<String, String> localMap) {  7:         // 合并配置 Map 结果  8:         Map<String, String> map = new HashMap<String, String>();  9:         // 远程配置 Map 结果 10:         Map<String, String> remoteMap = remoteUrl.getParameters(); 11: 12:         // 添加 `remoteMap` 到 `map` 中，并移除不必要的配置 13:         if (remoteMap != null && remoteMap.size() > 0) { 14:             map.putAll(remoteMap); 15: 16:             // Remove configurations from provider, some items should be affected by provider. 线程池配置不使用提供者的 17:             map.remove(Constants.THREAD_NAME_KEY); 18:             map.remove(Constants.DEFAULT_KEY_PREFIX + Constants.THREAD_NAME_KEY); 19: 20:             map.remove(Constants.THREADPOOL_KEY); 21:             map.remove(Constants.DEFAULT_KEY_PREFIX + Constants.THREADPOOL_KEY); 22: 23:             map.remove(Constants.CORE_THREADS_KEY); 24:             map.remove(Constants.DEFAULT_KEY_PREFIX + Constants.CORE_THREADS_KEY); 25: 26:             map.remove(Constants.THREADS_KEY); 27:             map.remove(Constants.DEFAULT_KEY_PREFIX + Constants.THREADS_KEY); 28: 29:             map.remove(Constants.QUEUES_KEY); 30:             map.remove(Constants.DEFAULT_KEY_PREFIX + Constants.QUEUES_KEY); 31: 32:             map.remove(Constants.ALIVE_KEY); 33:             map.remove(Constants.DEFAULT_KEY_PREFIX + Constants.ALIVE_KEY); 34: 35:             map.remove(Constants.TRANSPORTER_KEY); 36:             map.remove(Constants.DEFAULT_KEY_PREFIX + Constants.TRANSPORTER_KEY); 37:         } 38:         // 添加 `localMap` 到 `map` 中 39:         if (localMap != null && localMap.size() > 0) { 40:             map.putAll(localMap); 41:         } 42: 43:         // 添加指定的 `remoteMap` 的配置项到 `map` 中，因为上面被 `localMap` 覆盖了。 44:         if (remoteMap != null && remoteMap.size() > 0) { 45:             // Use version passed from provider side 46:             String dubbo = remoteMap.get(Constants.DUBBO_VERSION_KEY); 47:             if (dubbo != null && dubbo.length() > 0) { 48:                 map.put(Constants.DUBBO_VERSION_KEY, dubbo); 49:             } 50:             String version = remoteMap.get(Constants.VERSION_KEY); 51:             if (version != null && version.length() > 0) { 52:                 map.put(Constants.VERSION_KEY, version); 53:             } 54:             String group = remoteMap.get(Constants.GROUP_KEY); 55:             if (group != null && group.length() > 0) { 56:                 map.put(Constants.GROUP_KEY, group); 57:             } 58:             String methods = remoteMap.get(Constants.METHODS_KEY); 59:             if (methods != null && methods.length() > 0) { 60:                 map.put(Constants.METHODS_KEY, methods); 61:             } 62:             // Reserve timestamp of provider url. 保留 provider 的启动 timestamp 63:             String remoteTimestamp = remoteMap.get(Constants.TIMESTAMP_KEY); 64:             if (remoteTimestamp != null && remoteTimestamp.length() > 0) { 65:                 map.put(Constants.REMOTE_TIMESTAMP_KEY, remoteMap.get(Constants.TIMESTAMP_KEY)); 66:             } 67:             // Combine filters and listeners on Provider and Consumer 合并 filter 和 listener 68:             String remoteFilter = remoteMap.get(Constants.REFERENCE_FILTER_KEY); 69:             String localFilter = localMap.get(Constants.REFERENCE_FILTER_KEY); 70:             if (remoteFilter != null && remoteFilter.length() > 0 71:                     && localFilter != null && localFilter.length() > 0) { 72:                 localMap.put(Constants.REFERENCE_FILTER_KEY, remoteFilter + "," + localFilter); 73:             } 74:             String remoteListener = remoteMap.get(Constants.INVOKER_LISTENER_KEY); 75:             String localListener = localMap.get(Constants.INVOKER_LISTENER_KEY); 76:             if (remoteListener != null && remoteListener.length() > 0 77:                     && localListener != null && localListener.length() > 0) { 78:                 localMap.put(Constants.INVOKER_LISTENER_KEY, remoteListener + "," + localListener); 79:             } 80:         } 81: 82:         // 清空原有配置，使用合并的配置覆盖 83:         return remoteUrl.clearParameters().addParameters(map); 84:     } 85: 86: }
```

---

- 将 **合并前者指定**
localMap
和
remoteUrl.parameters
成
map
，大多数以
为主【第 12 至 41 行】，部分
以后者为主【第 43 至 80 行】。
- 将合并的 **覆盖**
map
的结果，
设置到
remoteUrl
中。

# 666. 彩蛋

比想象中，长好多的一篇博客，原本预期会短蛮多的。

顺便吐槽下，中间碰到一些困惑，网络上搜了一圈，都没解释到很多细节的点的源码解析文章，真的是。哎~~~
