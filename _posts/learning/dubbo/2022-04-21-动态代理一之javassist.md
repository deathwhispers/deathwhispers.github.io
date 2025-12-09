---
layout: post
title: 动态代理（一）之Javassist
slug: dubbo-proxy-javassist
type:
  - note
date: 2022-04-21
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-04-26 11:50
updated: 2022-04-26 18:33
---
本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享 Dubbo **动态代理**的实现。

在 [《Dubbo 用户指南 —— schema 配置参考手册》](http://dubbo.apache.org/zh-cn/docs/user/references/xml/introduction.html) 中，我们可以看到  和  标签中，可以通过 “proxy” 属性，可以配置动态代理的生成方式：

生成动态代理方式，可选：jdk / javassist

从说明中，我们可以看到，Dubbo 实现了**两种**方式生成代理：

- Javassit
- JDK

本文分享 Javassist 实现动态代理的源码；涉及代码如下：

- dubbo-common
模块的
bytecode
包。
- dubbo-rpc-api
模块的
proxy
包。

下一篇文章分享 JDK 实现动态代理的源码。

# 2. 性能

在分享具体实现之前，可能有胖友对性能方面感兴趣，可以看看如下的内容：

- [《动态代理方案性能对比》](http://javatar.iteye.com/blog/814426)
- 来自老徐的某篇文章
![](/assets/images/learning/dubbo/dubbo-proxy-javassist/e9441892fb76cb2ed55fc158fead14fb.png)
菜逼老徐

# 3. 整体流程

瞎比比了这么多，我们开始进入正题了。相信很多胖友对**动态代理**的概念已经理解（如果暂时不理解，请 Google 下），那么 Dubbo 对它们使用在哪呢？见下图：

![](/assets/images/learning/dubbo/dubbo-proxy-javassist/3fef1864364a3d1de123abc101d5b313.png)

菜逼老王

旁白君：本图暂不考虑集群容错、网络调用、序列化反序列等。

- 在 Dubbo 中，我们使用 **Service 接口**
，作为服务 API 的契约。
- 在 Consumer 中，我们调用 Service 接口的方法时，实际调用的是 Dubbo 动态代理。下面先一起来看一个生成的 **proxy**
代码的示例：

```plain text
plain 1: package com.alibaba.dubbo.common.bytecode;  2:   3: import com.alibaba.dubbo.demo.DemoService;  4: import com.alibaba.dubbo.rpc.service.EchoService;  5: import java.lang.reflect.InvocationHandler;  6: import java.lang.reflect.Method;  7:   8: public class proxy0  9:   implements ClassGenerator.DC, EchoService, DemoService 10: { 11:   public static Method[] methods; 12:   private InvocationHandler handler; 13:    14:   public void bye(Object paramObject) 15:   { 16:     Object[] arrayOfObject = new Object[1]; 17:     arrayOfObject[0] = paramObject; 18:     Object localObject = this.handler.invoke(this, methods[0], arrayOfObject); 19:   } 20:    21:   public String sayHello(String paramString) 22:   { 23:     Object[] arrayOfObject = new Object[1]; 24:     arrayOfObject[0] = paramString; 25:     Object localObject = this.handler.invoke(this, methods[1], arrayOfObject); 26:     return (String)localObject; 27:   } 28:    29:   public Object $echo(Object paramObject) 30:   { 31:     Object[] arrayOfObject = new Object[1]; 32:     arrayOfObject[0] = paramObject; 33:     Object localObject = this.handler.invoke(this, methods[2], arrayOfObject); 34:     return (Object)localObject; 35:   } 36:    37:   public proxy0() {} 38:    39:   public proxy0(InvocationHandler paramInvocationHandler) 40:   { 41:     this.handler = paramInvocationHandler; 42:   } 43: }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">该类通过 </font><font style="color:rgb(51, 51, 51);">dubbo-common</font><font style="color:rgb(51, 51, 51);"> 模块的 </font><font style="color:rgb(51, 51, 51);">bytecode</font><font style="color:rgb(51, 51, 51);"> 模块的 </font>**<font style="color:rgb(51, 51, 51);">Proxy</font>**<font style="color:rgb(51, 51, 51);"> 类，</font>**<font style="color:rgb(51, 51, 51);">自动生成</font>**<font style="color:rgb(51, 51, 51);">，使用 Javassist 技术。</font>
- <font style="color:rgb(51, 51, 51);">生成的 </font>**<font style="color:rgb(51, 51, 51);">proxy</font>**<font style="color:rgb(51, 51, 51);"> 类会</font>**<font style="color:rgb(51, 51, 51);">实现</font>**<font style="color:rgb(51, 51, 51);">我们定义的 Service 接口( 例如，此处是 DemoService )。</font>
- <font style="color:rgb(51, 51, 51);">#bye(Object)</font><font style="color:rgb(51, 51, 51);"> 和 </font><font style="color:rgb(51, 51, 51);">#sayHello(Object)</font><font style="color:rgb(51, 51, 51);"> 方法，是我们定义在 DemoService 的</font>**<font style="color:rgb(51, 51, 51);">接口方法</font>**<font style="color:rgb(51, 51, 51);">，在生成的 </font>**<font style="color:rgb(51, 51, 51);">proxy</font>**<font style="color:rgb(51, 51, 51);"> 类中，实现这些定义在接口中的方法，收拢统一调用 </font><font style="color:rgb(51, 51, 51);">java.lang.reflect.InvocationHandler#invoke(proxy, method, args)</font><font style="color:rgb(51, 51, 51);"> 方法。通过这样的方式，可以调用到最终的 </font><font style="color:rgb(51, 51, 51);">Invoker#invoke(Invocation)</font><font style="color:rgb(51, 51, 51);"> 方法，实现 RPC 调用。</font>
- <font style="color:rgb(51, 51, 51);">注意，此处我们一直用的 </font>**<font style="color:rgb(51, 51, 51);">proxy</font>**<font style="color:rgb(51, 51, 51);"> 一直是小写的，这是为什么呢？请见下文大写的 </font>**<font style="color:rgb(51, 51, 51);">Proxy</font>**<font style="color:rgb(51, 51, 51);"> 类。</font>
```

- 在 Provider 中，XXXProtocol 会获得被调用的 Exporter 对象，从而获得到 Invoker 对象。但是呢，Invoker 对象实际和 Service 实现对象，是无法直接调用，需要有中间的一层 Wrapper 来**代理分发**
到 Service 对应的方法。下面我们来看一个生成的 Wrapper 代码的示例：

```plain text
plain 1: package com.alibaba.dubbo.common.bytecode;   2:    3: import com.alibaba.dubbo.demo.provider.DemoDAO;   4: import com.alibaba.dubbo.demo.provider.DemoServiceImpl;   5: import java.lang.reflect.InvocationTargetException;   6: import java.util.Map;   7:    8: public class Wrapper1   9:   extends Wrapper  10:   implements ClassGenerator.DC  11: {  12:   public static String[] pns;  13:   public static Map pts;  14:   public static String[] mns;  15:   public static String[] dmns;  16:   public static Class[] mts0;  17:   public static Class[] mts1;  18:   public static Class[] mts2;  19:     20:   public String[] getPropertyNames()  21:   {  22:     return pns;  23:   }  24:     25:   public boolean hasProperty(String paramString)  26:   {  27:     return pts.containsKey(paramString);  28:   }  29:     30:   public Class getPropertyType(String paramString)  31:   {  32:     return (Class)pts.get(paramString);  33:   }  34:     35:   public String[] getMethodNames()  36:   {  37:     return mns;  38:   }  39:     40:   public String[] getDeclaredMethodNames()  41:   {  42:     return dmns;  43:   }  44:     45:   public void setPropertyValue(Object paramObject1, String paramString, Object paramObject2)  46:   {  47:     DemoServiceImpl w;  48:     try  49:     {  50:       w = (DemoServiceImpl)paramObject1;  51:     }  52:     catch (Throwable localThrowable)  53:     {  54:       throw new IllegalArgumentException(localThrowable);  55:     }  56:     if (paramString.equals("test01"))  57:     {  58:       w.test01 = ((String)paramObject2);  59:       return;  60:     }  61:     if (paramString.equals("demoDAO"))  62:     {  63:       localDemoServiceImpl.setDemoDAO((DemoDAO)paramObject2);  64:       return;  65:     }  66:     throw new NoSuchPropertyException("Not found property \"" + paramString + "\" filed or setter method in class com.alibaba.dubbo.demo.provider.DemoServiceImpl.");  67:   }  68:     69:   public Object getPropertyValue(Object paramObject, String paramString)  70:   {  71:     DemoServiceImpl w;  72:     try  73:     {  74:       w = (DemoServiceImpl)paramObject;  75:     }  76:     catch (Throwable localThrowable)  77:     {  78:       throw new IllegalArgumentException(localThrowable);  79:     }  80:     if (paramString.equals("test01")) {  81:       return localDemoServiceImpl.test01;  82:     }  83:     throw new NoSuchPropertyException("Not found property \"" + paramString + "\" filed or setter method in class com.alibaba.dubbo.demo.provider.DemoServiceImpl.");  84:   }  85:     86:   public Object invokeMethod(Object paramObject, String paramString, Class[] paramArrayOfClass, Object[] paramArrayOfObject)  87:     throws InvocationTargetException  88:   {  89:     DemoServiceImpl w;  90:     try  91:     {  92:       w = (DemoServiceImpl)paramObject;  93:     }  94:     catch (Throwable localThrowable1)  95:     {  96:       throw new IllegalArgumentException(localThrowable1);  97:     }  98:     try  99:     { 100:       if ("sayHello".equals(paramString) && paramArrayOfClass.length == 1) { 101:         return w.sayHello((String)paramArrayOfObject[0]); 102:       } 103:       if ("bye".equals(paramString) && paramArrayOfClass.length == 1) 104:       { 105:         w.bye((Object)paramArrayOfObject[0]); 106:         return null; 107:       } 108:       if ("setDemoDAO".equals(paramString) && paramArrayOfClass.length == 1) 109:       { 110:         w.setDemoDAO((DemoDAO)paramArrayOfObject[0]); 111:         return null; 112:       } 113:     } 114:     catch (Throwable localThrowable2) 115:     { 116:       throw new InvocationTargetException(localThrowable2); 117:     } 118:     throw new NoSuchMethodException("Not found method \"" + paramString + "\" in class com.alibaba.dubbo.demo.provider.DemoServiceImpl."); 119:   } 120: }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">该类通过 </font><font style="color:rgb(51, 51, 51);">dubbo-common</font><font style="color:rgb(51, 51, 51);"> 模块的 </font><font style="color:rgb(51, 51, 51);">bytecode</font><font style="color:rgb(51, 51, 51);"> 模块的 Wrapper 类，</font>**<font style="color:rgb(51, 51, 51);">自动生成</font>**<font style="color:rgb(51, 51, 51);">，使用 Javassist 技术。</font>
- <font style="color:rgb(51, 51, 51);">不同于生成的 </font>**<font style="color:rgb(51, 51, 51);">proxy</font>**<font style="color:rgb(51, 51, 51);">类，不实现 Service 接口类，而是在 </font><font style="color:rgb(51, 51, 51);">#invokeMethod(paramObject, paramString, paramArrayOfClass, paramArrayOfObject)</font><font style="color:rgb(51, 51, 51);"> 方法，提供给 </font><font style="color:rgb(51, 51, 51);">Invoker#invoke(invocation)</font><font style="color:rgb(51, 51, 51);"> 中调用，统一分发请求到 Service 对应的方法。从职能上来看，有一点像硬编码的 Controller 。</font>
- <font style="color:rgb(51, 51, 51);">一个生成的 </font>**<font style="color:rgb(51, 51, 51);">Wrapper</font>**<font style="color:rgb(51, 51, 51);">类，只对应一个 Service ，从第 75 行的代码，我们也可以看出。</font>
```

# 4. ProxyFactory

[com.alibaba.dubbo.rpc.ProxyFactory](https://github.com/YunaiV/dubbo/blob/6de0a069fcc870894e64ffd54a24e334b19dcb36/dubbo-rpc/dubbo-rpc-api/src/main/java/com/alibaba/dubbo/rpc/ProxyFactory.java) ，代理工厂接口。

在 [《精尽 Dubbo 源码分析 —— 核心流程一览》](http://svip.iocoder.cn/Dubbo/implementation-intro/) 的 [「4.5 ProxyFactory」](http://svip.iocoder.cn/Dubbo/proxy-javassist/#)，已经分享，胖友点击查看。

![](/assets/images/learning/dubbo/dubbo-proxy-javassist/ba26b5cb5afa1805cd4acd0a2ea8785a.png)

ProxyFactory 子类

## 4.1 AbstractProxyFactory

com.alibaba.dubbo.rpc.proxy.AbstractProxyFactory ，实现 ProxyFactory 接口，代理工厂抽象类。代码如下：

```plain text
plain 1: public abstract class AbstractProxyFactory implements ProxyFactory {  2:   3:     public <T> T getProxy(Invoker<T> invoker) throws RpcException {  4:         Class<?>[] interfaces = null;  5:         // TODO 8022 芋艿  6:         String config = invoker.getUrl().getParameter("interfaces");  7:         if (config != null && config.length() > 0) {  8:             String[] types = Constants.COMMA_SPLIT_PATTERN.split(config);  9:             if (types != null && types.length > 0) { 10:                 interfaces = new Class<?>[types.length + 2]; 11:                 interfaces[0] = invoker.getInterface(); 12:                 interfaces[1] = EchoService.class; 13:                 for (int i = 0; i < types.length; i++) { 14:                     interfaces[i + 1] = ReflectUtils.forName(types[i]); 15:                 } 16:             } 17:         } 18:         // 增加 EchoService 接口，用于回生测试。参见文档《回声测试》http://dubbo.apache.org/zh-cn/docs/user/demos/echo-service.html 19:         if (interfaces == null) { 20:             interfaces = new Class<?>[]{invoker.getInterface(), EchoService.class}; 21:         } 22:         return getProxy(invoker, interfaces); 23:     } 24:  25:     public abstract <T> T getProxy(Invoker<T> invoker, Class<?>[] types); 26:  27: }
```

---

- 可以看到，该抽象类，主要是实现了
#getProxy(invoker)
方法，获得需要生成代理的接口们。
    - 第 5 至 17 行： TODO 8022 芋艿
    - 第 18 至 21 行：在原有 Invoker 对应**关联**[《Dubbo 用户指南 —— 回声测试》](http://dubbo.apache.org/zh-cn/docs/user/demos/echo-service.html)
的 Service 接口之上，增加 EchoService 接口。
FROM
回声测试用于检测服务是否可用，回声测试按照正常请求流程执行，能够测试整个调用是否通畅，可用于监控。
所有服务自动实现 EchoService 接口，只需将任意服务引用强制转型为 EchoService，即可使用。
    - 第 22 行：调用 **抽象**
#getProxy(invoker, types)
方法，获得 Proxy 对象。

## 4.2 StubProxyFactoryWrapper

[com.alibaba.dubbo.rpc.proxy.wrapper.StubProxyFactoryWrapper](https://github.com/YunaiV/dubbo/blob/afb312f7dce997f5f90ba686345f4354e786534d/dubbo-rpc/dubbo-rpc-api/src/main/java/com/alibaba/dubbo/rpc/proxy/wrapper/StubProxyFactoryWrapper.java) ，实现 ProxyFactory 接口，Stub 代理工厂 Wrapper 实现类，基于 Dubbo SPI Wrapper 机制加载。

该类，不在本文的范畴内，感兴趣的胖友可以先看下 [《Dubbo 用户指南 —— 本地存根》](http://dubbo.apache.org/zh-cn/docs/user/demos/local-stub.html) 。后续，我们单独开文章分享。

## 4.3 JavassistProxyFactory

com.alibaba.dubbo.rpc.proxy.javassist.JavassistProxyFactory ，实现 AbstractProxyFactory 抽象类，基于 Javassist 代理工厂实现类。代码如下：

```plain text
plain 1: public class JavassistProxyFactory extends AbstractProxyFactory {  2:   3:     @SuppressWarnings("unchecked")  4:     public <T> T getProxy(Invoker<T> invoker, Class<?>[] interfaces) {  5:         return (T) Proxy.getProxy(interfaces).newInstance(new InvokerInvocationHandler(invoker));  6:     }  7:   8:     public <T> Invoker<T> getInvoker(T proxy, Class<T> type, URL url) {  9:         // TODO Wrapper cannot handle this scenario correctly: the classname contains '$' 10:         // TODO Wrapper类不能正确处理带$的类名 11:         final Wrapper wrapper = Wrapper.getWrapper(proxy.getClass().getName().indexOf('$') < 0 ? proxy.getClass() : type); 12:         return new AbstractProxyInvoker<T>(proxy, type, url) { 13:             @Override 14:             protected Object doInvoke(T proxy, String methodName, 15:                                       Class<?>[] parameterTypes, 16:                                       Object[] arguments) throws Throwable { 17:                 return wrapper.invokeMethod(proxy, methodName, parameterTypes, arguments); 18:             } 19:         }; 20:     } 21:  22: }
```

---

- #getProxy(invoker, interfaces)
方法
    - 第 5 行：调用 **Proxy**
Proxy#getProxy(interface)
方法，获得
对象。
    - 第 5 行：调用 **proxy**
Proxy#newInstance(InvocationHandler)
方法，获得
对象。其中传入的参数是 InvokerInvocationHandler 类，通过这样的方式，让 proxy 和真正的逻辑代码解耦。
        - Proxy 和 proxy ，在 [「7.3 Proxy」](http://svip.iocoder.cn/Dubbo/proxy-javassist/#)
中，详细解析。
        - InvokerInvocationHandler ，在 [「5. InvokerInvocationHandler」](http://svip.iocoder.cn/Dubbo/proxy-javassist/#)
中，详细解析。
- #getInvoker(proxy, type, url)
方法
    - 第 11 行：调用 **Wrapper**
Wrapper#getWrapper(Class<?>)
方法，获得
对象。
        - Wrapper ，在 [「7.4 Wrapper」](http://svip.iocoder.cn/Dubbo/proxy-javassist/#)
中，详细解析。
    - 第 12 至 19 行：创建 AbstractProxyInvoker 对象，实现
#doInvoke(…)
方法。在该方法中，调用
Wrapper#invokeMethod(…)
方法，从而调用 Service 的方法。
        - AbstractProxyInvoker ，在 [「6. AbstractProxyInvoker」](http://svip.iocoder.cn/Dubbo/proxy-javassist/#)
中，详细解析。

# 5. InvokerInvocationHandler

com.alibaba.dubbo.rpc.proxy.InvokerInvocationHandler ，实现 [java.lang.reflect.InvocationHandler](https://docs.oracle.com/javase/7/docs/api/java/lang/reflect/InvocationHandler.html) 接口，代码如下：

```plain text
plain 1: public class InvokerInvocationHandler implements InvocationHandler {  2:   3:     /**  4:      * Invoker 对象  5:      */  6:     private final Invoker<?> invoker;  7:   8:     public InvokerInvocationHandler(Invoker<?> handler) {  9:         this.invoker = handler; 10:     } 11:  12:     @Override public Object invoke(Object proxy, Method method, Object[] args) throws Throwable { 13:         String methodName = method.getName(); 14:         Class<?>[] parameterTypes = method.getParameterTypes(); 15:         // wait 等方法，直接反射调用 16:         if (method.getDeclaringClass() == Object.class) { 17:             return method.invoke(invoker, args); 18:         } 19:         // 基础方法，不使用 RPC 调用 20:         if ("toString".equals(methodName) && parameterTypes.length == 0) { 21:             return invoker.toString(); 22:         } 23:         if ("hashCode".equals(methodName) && parameterTypes.length == 0) { 24:             return invoker.hashCode(); 25:         } 26:         if ("equals".equals(methodName) && parameterTypes.length == 1) { 27:             return invoker.equals(args[0]); 28:         } 29:         // RPC 调用 30:         return invoker.invoke(new RpcInvocation(method, args)).recreate(); 31:     } 32:  33: }
```

---

- invoker
属性，Invoker 对象，用于在
#invoke()
方法调用。
- #invoke(proxy, method, args)**实现**
方法，核心逻辑是调用
Invoker#invoke(invocation)
方法，进行 RPC 调用。
    - 第 16 至 18 行：处理
#wait()
#notify()
等方法，进行反射调用。
    - 第 20 至 28 行：处理
#toString()
#hashCode()
等方法，使用 Invoker 对象的方法，不进行 RPC 调用。
    - 第 30 行：调用 **核心逻辑**
Invoker#invoke(invocation)
方法，
，进行 RPC 调用。
    - 第 30 行：调用
Result#recreate()
方法，回放调用结果。代码如下：

```plain text
plain // RpcResult.java public Object recreate() throws Throwable {     // 有异常，抛出异常     if (exception != null) {         throw exception;     }     // 无异常，返回结果     return result; }
```

---

```plain text
    * <font style="color:rgb(51, 51, 51);">x </font>
```

通过 InvokerInvocationHandler ，可以实现 Proxy 和真正的逻辑解耦。

# 6. AbstractProxyInvoker

com.alibaba.dubbo.rpc.proxy.AbstractProxyInvoker ，实现 Invoker 接口，**代理** Invoker 对象的抽象类。

## 6.1 属性

```plain text
plain /**  * 代理的对象，一般是 Service 实现对象  */ private final T proxy; /**  * 接口类型，一般是 Service 接口  */ private final Class<T> type; /**  * URL 对象，一般是暴露服务的 URL 对象  */ private final URL url;  public AbstractProxyInvoker(T proxy, Class<T> type, URL url) {     if (proxy == null) {         throw new IllegalArgumentException("proxy == null");     }     if (type == null) {         throw new IllegalArgumentException("interface == null");     }     if (!type.isInstance(proxy)) { //         throw new IllegalArgumentException(proxy.getClass().getName() + " not implement interface " + type);     }     this.proxy = proxy;     this.type = type;     this.url = url; }
```

---

胖友，请看代码上的注释。

## 6.2 invoke

```plain text
plain 1: public Result invoke(Invocation invocation) throws RpcException { 2:     try { 3:         return new RpcResult(doInvoke(proxy, invocation.getMethodName(), invocation.getParameterTypes(), invocation.getArguments())); 4:     } catch (InvocationTargetException e) { 5:         return new RpcResult(e.getTargetException()); 6:     } catch (Throwable e) { 7:         throw new RpcException("Failed to invoke remote proxy method " + invocation.getMethodName() + " to " + getUrl() + ", cause: " + e.getMessage(), e); 8:     } 9: }
```

---

- 第 3 行：调用 **抽象**
#doInvoke(..)
方法，执行调用，返回调用结果。
#doInvoke(…)
方法，代码如下：

```plain text
plain /**  * 执行调用  *  * @param proxy 代理的对象  * @param methodName 方法名  * @param parameterTypes 方法参数类型数组  * @param arguments 方法参数数组  * @return 调用结果  * @throws Throwable 发生异常  */ protected abstract Object doInvoke(T proxy, String methodName, Class<?>[] parameterTypes, Object[] arguments) throws Throwable;
```

---

- 第 3 行：创建 RpcResult 对象，将结果包装返回。
- 第 5 行：发生 InvocationTargetException 异常，创建 RpcResult 对象包装。
    - [《 Java反射异常处理之InvocationTargetException》](https://blog.csdn.net/zhangzeyuaaa/article/details/39611467)

# 7. bytecode

在 dubbo-common 模块的 bytecode 包，基于 Javassit 库，**动态编译**，实现提供了**通用的**的动态代理实现。所以本小节，从**动态编译**的角度上来看，在内容上，和 [《精尽 Dubbo 源码分析 —— 动态编译（一）之 Javassist》](http://svip.iocoder.cn/Dubbo/compiler-javassist/?self=) 有一定的相似。

## 7.1 ClassGenerator

[com.alibaba.dubbo.common.bytecode.ClassGenerator](https://github.com/YunaiV/dubbo/blob/b5a5adcd965393b374a4f58ecea90264251c3cdb/dubbo-common/src/main/java/com/alibaba/dubbo/common/bytecode/ClassGenerator.java) ，类生成器，基于 **Javassist** 实现。

笔者在 [《TCC-Transaction 源码分析 —— Dubbo 支持》](http://www.iocoder.cn/TCC-Transaction/dubbo-support/?self=) 的 [「2.1.3 TccProxy & TccClassGenerator」](http://svip.iocoder.cn/Dubbo/proxy-javassist/#) 已经详细分享，基本类似，胖友瞅瞅噢。

## 7.3 Proxy

[com.alibaba.dubbo.common.bytecode.Proxy](https://github.com/YunaiV/dubbo/blob/b5a5adcd965393b374a4f58ecea90264251c3cdb/dubbo-common/src/main/java/com/alibaba/dubbo/common/bytecode/Proxy.java) ，代理抽象类，用于创建 Proxy 和 proxy 对象。

笔者在 [《TCC-Transaction 源码分析 —— Dubbo 支持》](http://www.iocoder.cn/TCC-Transaction/dubbo-support/?self=) 的 [「2.1.3 TccProxy & TccClassGenerator」](http://svip.iocoder.cn/Dubbo/proxy-javassist/#) 已经详细分享，基本类似，胖友瞅瞅噢。

---

如下是一个生成的 **Proxy** 代码的示例，代码如下：

```plain text
plain public class Proxy0 extends Proxy implements ClassGenerator.DC {          public Object newInstance(InvocationHandler paramInvocationHandler) {         return new proxy0(paramInvocationHandler);     }      }
```

---

- **生成的Proxy生成的proxy**
实现 Proxy 抽象类，是创建
的工厂（一一对应）。例如，Proxy0 创建 proxy0 对象。
- #newInstance(InvocationHandler)**生成的proxy**
方法，创建
的方法。

## 7.4 Wrapper

[com.alibaba.dubbo.common.bytecode.Wrapper](http://svip.iocoder.cn/Dubbo/proxy-javassist/TODO) ，Wrapper 抽象类，用于**创建某个对象的方法调用**的包装器，以避免**反射**调用，提高性能。即：

```plain text
plain // 反射 Method#invoke(Object instance, Object[] args)  // 优化成===>  // Wrapper Wrapper#invokeMethod(Object instance, String mn, Class<?>[] types, Object[] args)
```

---

- 为什么会提高性能呢？看到上文的 Wrapper 代理的示例，相信胖友已经明白。

### 7.4.1 抽象方法

在自动生成 Wrapper 类时，需要实现如下**抽象**方法：

```plain text
plain abstract public String[] getPropertyNames(); abstract public Class<?> getPropertyType(String pn);  abstract public boolean hasProperty(String name); abstract public Object getPropertyValue(Object instance, String pn) throws NoSuchPropertyException, IllegalArgumentException; abstract public void setPropertyValue(Object instance, String pn, Object pv) throws NoSuchPropertyException, IllegalArgumentException;  abstract public String[] getMethodNames(); abstract public String[] getDeclaredMethodNames();  /**  * invoke method.  *  * 调用方法  *  * @param instance instance.  *                 被调用的对象  * @param mn       method name.  *                 方法名  * @param types 参数类型数组  * @param args     argument array.  *                 参数数组  * @return return value.  *                  返回值  */ abstract public Object invokeMethod(Object instance, String mn, Class<?>[] types, Object[] args) throws NoSuchMethodException, InvocationTargetException;
```

---

### 7.4.2 getWrapper

#getWrapper(c) 方法，根据指定类，获得 Wrapper 对象。代码如下：

```plain text
plain 1: public static Wrapper getWrapper(Class<?> c) {  2:     // 判断是否继承 ClassGenerator.DC.class ，如果是，拿到父类，避免重复包装  3:     while (ClassGenerator.isDynamicClass(c)) // can not wrapper on dynamic class.  4:         c = c.getSuperclass();  5:   6:     // 指定类为 Object.class  7:     if (c == Object.class)  8:         return OBJECT_WRAPPER;  9:  10:     // 从缓存中获得 Wrapper 对象 11:     Wrapper ret = WRAPPER_MAP.get(c); 12:     // 创建 Wrapper 对象，并添加到缓存 13:     if (ret == null) { 14:         ret = makeWrapper(c); 15:         WRAPPER_MAP.put(c, ret); 16:     } 17:     return ret; 18: }
```

---

- 第 3 至 4 行：判断是否已经继承了 [ClassGenerator.DC.class](https://github.com/YunaiV/dubbo/blob/91b4862d4aed0f984015b132c3cb426f9c3b0c76/dubbo-common/src/main/java/com/alibaba/dubbo/common/bytecode/ClassGenerator.java#L382-L386)**重复包装**
，如果是，拿到父类，避免
。
- 第 7 至 8 行：若指定类为 Object.class ，返回 [OBJECT_WRAPPER](https://github.com/YunaiV/dubbo/blob/91b4862d4aed0f984015b132c3cb426f9c3b0c76/dubbo-common/src/main/java/com/alibaba/dubbo/common/bytecode/Wrapper.java#L43-L95)
对象。
- 第 11 行：从缓存
WRAPPER_MAP
中，获得 Wrapper 对象。
WRAPPER_MAP
代码如下：

```plain text
plain /**  * Wrapper 对象缓存  * key ：Wrapper 类。  * value ：Proxy 对象  */ private static final Map<Class<?>, Wrapper> WRAPPER_MAP = new ConcurrentHashMap<Class<?>, Wrapper>(); //class wrapper map
```

---

- 第 13 至 16 行：调用
#makeWrapper(Class<?>)
方法，创建 Wrapper 对象，并添加到缓存。

### 7.4.3 makeWrapper

#makeWrapper(Class<?>) 方法，创建 Wrapper 对象。代码如下：

旁白君：实现上，和 Proxy 差不过的，只生成**一个** Wrapper 类。

```plain text
plain 1: private static Wrapper makeWrapper(Class<?> c) {   2:     // 非私有类   3:     if (c.isPrimitive())   4:         throw new IllegalArgumentException("Can not create wrapper for primitive type: " + c);   5:    6:     // 类名   7:     String name = c.getName();   8:     // 类加载器   9:     ClassLoader cl = ClassHelper.getClassLoader(c);  10:   11:     // 设置属性方法 `#setPropertyValue(o, n, v)` 的开头的代码  12:     StringBuilder c1 = new StringBuilder("public void setPropertyValue(Object o, String n, Object v){ ");  13:     // 获得属性方法 `#getPropertyValue(o, n)` 的开头的代码  14:     StringBuilder c2 = new StringBuilder("public Object getPropertyValue(Object o, String n){ ");  15:     // 调用方法 `#invokeMethod(o, n, p, v)` 的开头的代码  16:     StringBuilder c3 = new StringBuilder("public Object invokeMethod(Object o, String n, Class[] p, Object[] v) throws " + InvocationTargetException.class.getName() + "{ ");  17:   18:     // 添加每个方法的，被调用对象的类型转换的代码  19:     c1.append(name).append(" w; try{ w = ((").append(name).append(")$1); }catch(Throwable e){ throw new IllegalArgumentException(e); }");  20:     c2.append(name).append(" w; try{ w = ((").append(name).append(")$1); }catch(Throwable e){ throw new IllegalArgumentException(e); }");  21:     c3.append(name).append(" w; try{ w = ((").append(name).append(")$1); }catch(Throwable e){ throw new IllegalArgumentException(e); }");  22:   23:     // 属性名与属性名的集合，用于 `#hasProperty(...)` `#setPropertyValue(...)` `getPropertyValue(...)` 方法。  24:     Map<String, Class<?>> pts = new HashMap<String, Class<?>>(); // <property name, property types>  25:     // 方法签名与方法对象的集合，用于 `#invokeMethod(..)` 方法。  26:     Map<String, Method> ms = new LinkedHashMap<String, Method>(); // <method desc, Method instance>  27:     // 方法名数组用于 `#getMethodNames()` 方法。  28:     List<String> mns = new ArrayList<String>(); // method names.  29:     // 定义的方法名数组，用于 `#getDeclaredMethodNames()` 方法。  30:     List<String> dmns = new ArrayList<String>(); // declaring method names.  31:   32:     // 循环 public 属性，添加每个属性的设置和获得分别到 `#setPropertyValue(o, n, v)` 和 `#getPropertyValue(o, n)` 的代码  33:     // get all public field.  34:     for (Field f : c.getFields()) {  35:         String fn = f.getName();  36:         Class<?> ft = f.getType();  37:         if (Modifier.isStatic(f.getModifiers()) || Modifier.isTransient(f.getModifiers())) // 排除 static 和 transient  38:             continue;  39:   40:         c1.append(" if( $2.equals(\"").append(fn).append("\") ){ w.").append(fn).append("=").append(arg(ft, "$3")).append("; return; }");  41:         c2.append(" if( $2.equals(\"").append(fn).append("\") ){ return ($w)w.").append(fn).append("; }");  42:         // 添加到 `pts` 中  43:         pts.put(fn, ft);  44:     }  45:   46:     Method[] methods = c.getMethods();  47:     // 如果有方法，添加 `#invokeMethod(o, n, p, v)` 的 try 的代码  48:     // get all public method.  49:     boolean hasMethod = hasMethods(methods);  50:     if (hasMethod) {  51:         c3.append(" try{");  52:     }  53:     for (Method m : methods) {  54:         // 跳过来自 Object 的内置方法  55:         if (m.getDeclaringClass() == Object.class) //ignore Object's method.  56:             continue;  57:   58:         String mn = m.getName(); // 方法名  59:         // 使用方法名 + 方法参数长度来判断  60:         c3.append(" if( \"").append(mn).append("\".equals( $2 ) ");  61:         int len = m.getParameterTypes().length;  62:         c3.append(" && ").append(" $3.length == ").append(len);  63:   64:         // 若相同方法名存在多个，增加参数类型数组的比较判断  65:         boolean override = false;  66:         for (Method m2 : methods) {  67:             if (m != m2 && m.getName().equals(m2.getName())) {  68:                 override = true;  69:                 break;  70:             }  71:         }  72:         if (override) {  73:             if (len > 0) {  74:                 for (int l = 0; l < len; l++) {  75:                     c3.append(" && ").append(" $3[").append(l).append("].getName().equals(\"")  76:                             .append(m.getParameterTypes()[l].getName()).append("\")");  77:                 }  78:             }  79:         }  80:   81:         c3.append(" ) { ");  82:   83:         // 添加调用对象的对应方法的代码  84:         if (m.getReturnType() == Void.TYPE)  85:             c3.append(" w.").append(mn).append('(').append(args(m.getParameterTypes(), "$4")).append(");").append(" return null;");  86:         else  87:             c3.append(" return ($w)w.").append(mn).append('(').append(args(m.getParameterTypes(), "$4")).append(");");  88:   89:         c3.append(" }");  90:   91:         // 添加到 `mns` 中  92:         mns.add(mn);  93:         // 添加到 `dmns` 中  94:         if (m.getDeclaringClass() == c)  95:             dmns.add(mn);  96:         // 添加到 `ms` 中  97:         ms.put(ReflectUtils.getDesc(m), m);  98:     }  99:     // 如果有方法，添加 `#invokeMethod(o, n, p, v)` 的 catch 的代码 100:     if (hasMethod) { 101:         c3.append(" } catch(Throwable e) { "); 102:         c3.append("     throw new java.lang.reflect.InvocationTargetException(e); "); 103:         c3.append(" }"); 104:     } 105:     // 添加 `#invokeMethod(o, n, p, v)` 的未匹配到方法的代码 106:     c3.append(" throw new " + NoSuchMethodException.class.getName() + "(\"Not found method \\\"\"+$2+\"\\\" in class " + c.getName() + ".\"); }"); 107:  108:     // 循环 setting/getting 方法，添加每个属性的设置和获得分别到 `#setPropertyValue(o, n, v)` 和 `#getPropertyValue(o, n)` 的代码 109:     // deal with get/set method. 110:     Matcher matcher; 111:     for (Map.Entry<String, Method> entry : ms.entrySet()) { 112:         String md = entry.getKey(); 113:         Method method = entry.getValue(); 114:         if ((matcher = ReflectUtils.GETTER_METHOD_DESC_PATTERN.matcher(md)).matches()) { 115:             String pn = propertyName(matcher.group(1)); 116:             c2.append(" if( $2.equals(\"").append(pn).append("\") ){ return ($w)w.").append(method.getName()).append("(); }"); 117:             // 添加到 `pts` 中 118:             pts.put(pn, method.getReturnType()); 119:         } else if ((matcher = ReflectUtils.IS_HAS_CAN_METHOD_DESC_PATTERN.matcher(md)).matches()) { 120:             String pn = propertyName(matcher.group(1)); 121:             c2.append(" if( $2.equals(\"").append(pn).append("\") ){ return ($w)w.").append(method.getName()).append("(); }"); 122:             // 添加到 `pts` 中 123:             pts.put(pn, method.getReturnType()); 124:         } else if ((matcher = ReflectUtils.SETTER_METHOD_DESC_PATTERN.matcher(md)).matches()) { // 不支持 public T setName(String name) { this.name = name; return this;} 这种返回 this 的形式。 125:             Class<?> pt = method.getParameterTypes()[0]; 126:             String pn = propertyName(matcher.group(1)); 127:             c1.append(" if( $2.equals(\"").append(pn).append("\") ){ w.").append(method.getName()).append("(").append(arg(pt, "$3")).append("); return; }"); 128:             // 添加到 `pts` 中 129:             pts.put(pn, pt); 130:         } 131:     } 132:     c1.append(" throw new " + NoSuchPropertyException.class.getName() + "(\"Not found property \\\"\"+$2+\"\\\" filed or setter method in class " + c.getName() + ".\"); }"); 133:     c2.append(" throw new " + NoSuchPropertyException.class.getName() + "(\"Not found property \\\"\"+$2+\"\\\" filed or setter method in class " + c.getName() + ".\"); }"); 134:  135:     // make class 136:     long id = WRAPPER_CLASS_COUNTER.getAndIncrement(); 137:     // 创建 ClassGenerator 对象 138:     ClassGenerator cc = ClassGenerator.newInstance(cl); 139:     // 设置类名 140:     cc.setClassName((Modifier.isPublic(c.getModifiers()) ? Wrapper.class.getName() : c.getName() + "$sw") + id); 141:     // 设置父类为 Wrapper.class 142:     cc.setSuperClass(Wrapper.class); 143:  144:     // 添加构造方法，参数 空 145:     cc.addDefaultConstructor(); 146:     // 添加静态属性 `pns` 的代码 147:     cc.addField("public static String[] pns;"); // property name array. 148:     // 添加静态属性 `pts` 的代码 149:     cc.addField("public static " + Map.class.getName() + " pts;"); // property type map. 150:     // 添加静态属性 `pts` 的代码 151:     cc.addField("public static String[] mns;"); // all method name array. 152:     // 添加静态属性 `dmns` 的代码 153:     cc.addField("public static String[] dmns;"); // declared method name array. 154:     // 添加静态属性 `mts` 的代码。每个方法的参数数组。 155:     for (int i = 0, len = ms.size(); i < len; i++) 156:         cc.addField("public static Class[] mts" + i + ";"); 157:  158:     // ======= 添加抽象方法的实现，到 `cc` 中 159:     // 添加 `#getPropertyNames()` 的代码到 `cc` 160:     cc.addMethod("public String[] getPropertyNames(){ return pns; }"); 161:     // 添加 `#hasProperty(n)` 的代码到 `cc` 162:     cc.addMethod("public boolean hasProperty(String n){ return pts.containsKey($1); }"); 163:     // 添加 `#getPropertyType(n)` 的代码到 `cc` 164:     cc.addMethod("public Class getPropertyType(String n){ return (Class)pts.get($1); }"); 165:     // 添加 `#getMethodNames()` 的代码到 `cc` 166:     cc.addMethod("public String[] getMethodNames(){ return mns; }"); 167:     // 添加 `#getDeclaredMethodNames()` 的代码到 `cc` 168:     cc.addMethod("public String[] getDeclaredMethodNames(){ return dmns; }"); 169:     // 添加 `#setPropertyValue(o, n, v)` 的代码到 `cc` 170:     cc.addMethod(c1.toString()); 171:     // 添加 `#getPropertyValue(o, n)` 的代码到 `cc` 172:     cc.addMethod(c2.toString()); 173:     // 添加 `#invokeMethod(o, n, p, v)` 的代码到 `cc` 174:     cc.addMethod(c3.toString()); 175:  176:     try { 177:         // 生成类 178:         Class<?> wc = cc.toClass(); 179:         // 反射，设置静态变量的值 180:         // setup static field. 181:         wc.getField("pts").set(null, pts); 182:         wc.getField("pns").set(null, pts.keySet().toArray(new String[0])); 183:         wc.getField("mns").set(null, mns.toArray(new String[0])); 184:         wc.getField("dmns").set(null, dmns.toArray(new String[0])); 185:         int ix = 0; 186:         for (Method m : ms.values()) 187:             wc.getField("mts" + ix++).set(null, m.getParameterTypes()); 188:         // 创建对象 189:         return (Wrapper) wc.newInstance(); 190:     } catch (RuntimeException e) { 191:         throw e; 192:     } catch (Throwable e) { 193:         throw new RuntimeException(e.getMessage(), e); 194:     } finally { 195:         // 释放资源 196:         cc.release(); 197:         ms.clear(); 198:         mns.clear(); 199:         dmns.clear(); 200:     } 201: }
```

---

- 上文生成的 Wrapper1 的代码，对应的 DempServiceImpl 的代码如下：

```plain text
plain 1: public class DemoServiceImpl implements DemoService {  2:   3:     /**  4:      * 测试属性，{@link com.alibaba.dubbo.common.bytecode.Wrapper}  5:      */  6:     public String test01;  7:   8:     private DemoDAO demoDAO;  9:  10:     public String sayHello(String name) { 11:         System.out.println("[" + new SimpleDateFormat("HH:mm:ss").format(new Date()) + "] Hello " + name + ", request from consumer: " + RpcContext.getContext().getRemoteAddress()); 12:         return "Hello " + name + ", response form provider: " + RpcContext.getContext().getLocalAddress(); 13:     } 14:  15:     @Override 16:     public void bye(Object o) { 17:         System.out.println(JSON.toJSONString(o)); 18:         System.out.println(o.getClass()); 19:     } 20:  21:     public void setDemoDAO(DemoDAO demoDAO) { 22:         this.demoDAO = demoDAO; 23:     } 24:  25: }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">下面，我们的解析，会结合这个类一起讲。</font>
- <font style="color:rgb(51, 51, 51);">========== 生成代码 ==========</font>
```

- 第 11 至 16 行：创建方法的**开头**
的代码：
    - #setPropertyValue(o, n, v)
的【Wrapper1 第 45 至 46 行】
    - #getPropertyValue(o, n)
的【Wrapper1 第 69 至 70 行】
    - #invokeMethod(o, n, p, v)
的【Wrapper1 第 86 至 88 行】
- 第 19 至 21 行：设置方法的**被调用对象的类型转换**
的代码：
    - #setPropertyValue(o, n, v)
的【Wrapper1 第 47 至 55 行】
        - #getPropertyValue(o, n)
的【Wrapper1 第 71 至 79 行】
        - #invokeMethod(o, n, p, v)
的【Wrapper1 第 89 至 97 行】
- 第 23 至 30 行：声明
pts
ms
mn
dmns
变量。 每个变量的用途，已经添加到代码的注释上。
- 第 32 至 44 行：循环 **public**
属性，添加每个属性的设置和获得分别代码：
    - 【DemoServiceImpl 第 6 行】
    - #setPropertyValue(o, n, v)
的【Wrapper1 第 56 至 60 行】
    - #getPropertyValue(o, n)
的【Wrapper1 第 80 至 62 行】
- 第 46 至 106 行：设置方法
#invokeMethod(o, n, p, v)
的调用代码：
    - 【DemoServiceImpl 第 10 至 23 行】
    - 【Wrapper1 第 98 至 119 行】
- 第 108 至 131 行：循环 **setting / getting**
属性，添加每个属性的设置和获得分别代码：
    - #setPropertyValue(o, n, v)
        - 【DemoServiceImpl 第 21 至 23 行】【DemoServiceImpl 第 8 行】
        - 【Wrapper1 第 61 至 62 行】
    - #getPropertyValue(o, n)
没举例子，胖友自己看代码脑补。
- ========== 生成类 ==========
- 第 138 行：创建 ClassGenerator 对象。
- 第 140 行：设置类名。
- 第 142 行：设置父类为 Wrapper.class
- 第 145 行：添加构造方法，参数为空
- 第 146 至 156 行：添加**静态属性**
pns
pts
mns
dmns
mts
。
- 第 158 至 174 行：添加**抽象方法**
的实现。
- 第 178 行：生成类。
- ========== 创建对象 ==========
- 第 179 至 187 行：反射，设置**静态属性**
的值。
- 第 189 行：创建 Wrapper 对象。
- ========== 释放 ==========
- 第 195 至 199 行：释放资源。

# 666. 彩蛋

![](/assets/images/learning/dubbo/dubbo-proxy-javassist/96ca62e95e06bbe2fa74153d2158bc13.png)

知识星球

趁着我球结婚的日子，写完了小文一篇。

祝福我球。

感慨我们离张牙舞爪的中二少年越来越远，身旁站着妻子或未婚妻，手上抱着一脸懵逼的孩子。