---
layout: post
title: 调用特性（二）之泛化引用
slug: dubbo-invocation-generic-reference
type:
  - note
date: 2022-05-11
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-05-11 11:52
updated: 2022-05-11 18:33
---
本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享**泛化引用**。我们来看下 [《用户指南 —— 泛化引用》](http://dubbo.apache.org/zh-cn/docs/user/demos/generic-reference.html) 的定义：

泛化接口调用方式主要用于客户端没有 API 接口及模型类元的情况，参数及返回值中的所有 POJO 均用 Map 表示，通常用于框架集成，比如：实现一个通用的服务测试框架，可通过 GenericService 调用所有服务实现。

请注意，消费**消费者**没有 **API 接口** 及 **模型类元**。那就是说，Dubbo 在泛化引用中，需要做两件事情：

- 没有 **API 接口**[com.alibaba.dubbo.rpc.service.GenericService](https://github.com/YunaiV/dubbo/blob/f83e70b53389a064e49babe32e61a5648002a44a/dubbo-rpc/dubbo-rpc-api/src/main/java/com/alibaba/dubbo/rpc/service/GenericService.java)
，所以提供一个泛化服务接口，目前是
，代码如下：

```plain text
plain public interface GenericService {      /**      * Generic invocation      *      * 泛化调用      *      * @param method         Method name, e.g. findPerson. If there are overridden methods, parameter info is      *                       required, e.g. findPerson(java.lang.String)      *                       方法名      * @param parameterTypes Parameter types      *                       参数类型数组      * @param args           Arguments      *                       参数数组      * @return invocation return value 调用结果      * @throws Throwable potential exception thrown from the invocation      */     Object $invoke(String method, String[] parameterTypes, Object[] args) throws GenericException;  }
```

---

```plain text
- **<font style="color:rgb(51, 51, 51);">一个</font>**<font style="color:rgb(51, 51, 51);">泛化引用，只对应</font>**<font style="color:rgb(51, 51, 51);">一个</font>**<font style="color:rgb(51, 51, 51);">服务实现。</font>
- <font style="color:rgb(51, 51, 51);">通过 </font><font style="color:rgb(51, 51, 51);">$invoke(method, parameterTypes, args)</font><font style="color:rgb(51, 51, 51);"> 方法，可以实现服务的泛化调用。</font>
- <font style="color:rgb(51, 51, 51);">具体的使用方式，我们在 </font>[「2. 示例」](http://svip.iocoder.cn/Dubbo/rpc-feature-generic-reference/#)<font style="color:rgb(51, 51, 51);"> 中看。</font>
```

- 没有 **模型类元转换处理**
，所以方法参数和方法返回若是 POJO ( 例如 User 和 Order 等 ) ，需要
：
    - 服务消费者，将 POJO 转成 Map ，然后再调用服务提供者。
    - 服务提供者，接收到 Map ，转换成 POJO ，再调用 Service 方法。若返回值有 POJO ，则转换成 Map 再返回。
    - 此处的 Map 只是举例子，实际在下文中，我们会看到还有**两种**
转换方式。

整体流程如下：

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038374397-ff2c4a73-21a4-4174-a2ac-2a6981e30e46.png)

流程

# 2. 示例

**服务提供者**

在 [dubbo-generic-reference-demo-provider](https://github.com/YunaiV/dubbo/blob/3766a47c5e97ee86c29d765dc88ee11ab5225604/dubbo-demo/dubbo-generic-reference-demo-provider) ，我们提供了例子。普通的服务提供者，不需要做任何处理，胖友自己查看。

**服务消费者**

在 [dubbo-generic-reference-demo-consumer](https://github.com/YunaiV/dubbo/tree/3766a47c5e97ee86c29d765dc88ee11ab5225604/dubbo-demo/dubbo-generic-reference-demo-consumer) ，我们提供了例子。我们挑**重点**的地方说。

① 在 Spring 配置申明 generic=“true”：

```plain text
plain <dubbo:reference id="demoService"  interface="com.alibaba.dubbo.demo.DemoService" generic="true" />
```

---

- interface**该服务**
配置项，泛化引用的服务接口。通过该配置，可以从注册中心，获取到所有
的提供方的地址。
- generic**三种配置项的值**
配置项，默认为
false
，不使用配置项。目前有
，开启泛化引用的功能：
    - generic=true[com.alibaba.dubbo.common.utils.PojoUtils](https://github.com/YunaiV/dubbo/blob/f83e70b53389a064e49babe32e61a5648002a44a/dubbo-common/src/main/java/com/alibaba/dubbo/common/utils/PojoUtils.java)
，使用
，实现
POJO <=> Map
的互转。
    - generic=nativejava[com.alibaba.dubbo.common.serialize.support.nativejava.NativeJavaSerialization](https://github.com/YunaiV/dubbo/blob/master/dubbo-common/src/main/java/com/alibaba/dubbo/common/serialize/support/nativejava/NativeJavaSerialization.java)
，使用
，实现
POJO <=> byte[]
的互转。
    - generic=bean[com.alibaba.dubbo.common.beanutil.JavaBeanSerializeUtil](https://github.com/YunaiV/dubbo/blob/master/dubbo-common/src/main/java/com/alibaba/dubbo/common/beanutil/JavaBeanSerializeUtil.java)
，使用
，实现
POJO <=> JavaBeanDescriptor
的互转。
    - 总的来说，三种方式的差异，在于使用互转( **序列化和反序列化**
)的方式不同。未来如果我们有需要，完成可以实现
generic=json
，使用 FastJSON 来序列化和反序列化。

② 在 Java 代码获取 barService 并开始泛化调用：

```plain text
plain ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext(new String[]{"META-INF/spring/dubbo-demo-consumer.xml"});  GenericService genericService = (GenericService) context.getBean("demoService"); Object result = genericService.$invoke("say01", new String[]{"java.lang.String"}, new Object[]{"123"}); System.out.println("result: " + result);
```

---

- 那么问题就来了，为什么可以使用 GenericService 转换？答案在
ReferenceConfig#init()
方法中，代码如下：

```plain text
plain // ReferenceConfig.java if (ProtocolUtils.isGeneric(getGeneric())) {     interfaceClass = GenericService.class; }  // ProtocolUtils.java public static boolean isGeneric(String generic) {     return generic != null             && !"".equals(generic)             && (Constants.GENERIC_SERIALIZATION_DEFAULT.equalsIgnoreCase(generic)  /* Normal generalization cal */             || Constants.GENERIC_SERIALIZATION_NATIVE_JAVA.equalsIgnoreCase(generic) /* Streaming generalization call supporting jdk serialization */             || Constants.GENERIC_SERIALIZATION_BEAN.equalsIgnoreCase(generic)); }
```

---

## 2.1 有关泛化类型的进一步解释

本小节为引用 [《Dubbo 用户指南 —— 泛化引用》](http://dubbo.apache.org/zh-cn/docs/user/demos/generic-reference.html) 。

假设存在 POJO 如：

```plain text
plain package com.xxx;  public class PersonImpl implements Person {     private String name;     private String password;      public String getName() {         return name;     }      public void setName(String name) {         this.name = name;     }      public String getPassword() {         return password;     }      public void setPassword(String password) {         this.password = password;     } }
```

---

则 POJO 数据：

```plain text
plain Person person = new PersonImpl();  person.setName("xxx");  person.setPassword("yyy");
```

---

【服务消费者】可用下面 Map 表示：

```plain text
plain Map<String, Object> map = new HashMap<String, Object>();  // 注意：如果参数类型是接口，或者List等丢失泛型，可通过class属性指定类型。 map.put("class", "com.xxx.PersonImpl");  map.put("name", "xxx");  map.put("password", "yyy");
```

---

- Map 中的
class
属性，在 PojoUtils 中，会根据该属性，将 Map 转换成 POJO 对象。

# 3. 服务消费者 GenericImplFilter

[com.alibaba.dubbo.rpc.filter.GenericImplFilter](https://github.com/YunaiV/dubbo/blob/3766a47c5e97ee86c29d765dc88ee11ab5225604/dubbo-rpc/dubbo-rpc-api/src/main/java/com/alibaba/dubbo/rpc/filter/GenericImplFilter.java) ，实现 Filter 接口，服务消费者的泛化调用过滤器。代码如下：

```plain text
plain 1: @Activate(group = Constants.CONSUMER, value = Constants.GENERIC_KEY, order = 20000)  2: public class GenericImplFilter implements Filter {  3:   4:     // ... 省略无关属性  5:   6:     @Override  7:     public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {  8:         // 获得 `generic` 配置项  9:         String generic = invoker.getUrl().getParameter(Constants.GENERIC_KEY); 10:  11:         // 省略代码...泛化实现的调用 12:  13:         // 泛化引用的调用 14:         if (invocation.getMethodName().equals(Constants.$INVOKE) // 方法名为 `$invoke` 15:                 && invocation.getArguments() != null 16:                 && invocation.getArguments().length == 3 17:                 && ProtocolUtils.isGeneric(generic)) { 18:             Object[] args = (Object[]) invocation.getArguments()[2]; 19:             // `nativejava` ，校验方法参数都为 byte[] 20:             if (ProtocolUtils.isJavaGenericSerialization(generic)) { 21:                 for (Object arg : args) { 22:                     if (!(byte[].class == arg.getClass())) { 23:                         error(byte[].class.getName(), arg.getClass().getName()); 24:                     } 25:                 } 26:             // `bean` ，校验方法参数为 JavaBeanDescriptor 27:             } else if (ProtocolUtils.isBeanGenericSerialization(generic)) { 28:                 for (Object arg : args) { 29:                     if (!(arg instanceof JavaBeanDescriptor)) { 30:                         error(JavaBeanDescriptor.class.getName(), arg.getClass().getName()); 31:                     } 32:                 } 33:             } 34:  35:             // 通过隐式参数，传递 `generic` 配置项 36:             ((RpcInvocation) invocation).setAttachment(Constants.GENERIC_KEY, generic); 37:         } 38:         return invoker.invoke(invocation); 39:     } 40:  41:     // 省略 `#error(...)` 方法 42:  43: }
```

---

- 使用 Dubbo SPI Adaptive 机制，**自动加载服务消费者**
，仅限
，并且有
generic
配置项。
    - 此处笔者就产生了一个疑问，从注册中心，获得到的服务 URL ，并没有设置
generic
的配置项，那岂不是在 ProtocolFilterWrapper 中，使用 Dubbo SPI Adaptive 加载不到 GenericImplFilter 这个过滤器？
    - 于是，笔者就开始慢慢调试，直到发现 **覆盖**
RegistryDirectory#mergeUrl(providerUrl)
方法，它会将服务消费者的配置( URL )项，
到服务提供者的 URL 。
    - 又因为泛化引用时，我们会在服务消费者的配置
generic = true
，那么服务提供者 URL 自然就有了该配置项，所以便有了 GenericImplFilter 过滤器。
- 第 9 行：获得
generic
配置项。
- 第 11 行：省略用于调用**泛化实现服务**[《Dubbo 用户指南 —— 泛化实现》](http://dubbo.apache.org/zh-cn/docs/user/demos/generic-service.html)
的代码，对应文档为
，下一篇文章，我们详细分享。
- 第 13 至 37 行：**泛化引用**
的调用，通过方法( 包括方法名、参数 ) +
generic
配置项，进行判断。
    - 第 19 至 33 行：根据不同的 **序列化**
generic
配置项，校验方法参数是否已经正确
。若不合法，调用
#error(expected, actual)
方法，抛出 RpcException 异常。代码如下：

```plain text
plain private void error(String expected, String actual) throws RpcException {     throw new RpcException(             new StringBuilder(32)                     .append("Generic serialization [")                     .append(Constants.GENERIC_SERIALIZATION_NATIVE_JAVA)                     .append("] only support message type ")                     .append(expected)                     .append(" and your message type is ")                     .append(actual).toString()); }
```

---

```plain text
    * <font style="color:rgb(51, 51, 51);">x</font>
- <font style="color:rgb(51, 51, 51);">第 36 行：调用 </font><font style="color:rgb(51, 51, 51);">RpcInvocation#setAttachment(key, value)</font><font style="color:rgb(51, 51, 51);"> 通过隐式参数，传递 </font><font style="color:rgb(51, 51, 51);">generic</font><font style="color:rgb(51, 51, 51);"> 配置项。</font>
```

- 第 38 行：调用
Invoker#invoke(invocation)
方法，继续过滤链的调用，最终 RPC 调用。

# 4. 服务提供者 GenericFilter

[com.alibaba.dubbo.rpc.filter.GenericFilter](https://github.com/YunaiV/dubbo/blob/3766a47c5e97ee86c29d765dc88ee11ab5225604/dubbo-rpc/dubbo-rpc-api/src/main/java/com/alibaba/dubbo/rpc/filter/GenericFilter.java) ，实现 Filter 接口，服务消费者的泛化调用过滤器。代码如下：

```plain text
plain 1: @Activate(group = Constants.PROVIDER, order = -20000)  2: public class GenericFilter implements Filter {  3:   4:     @Override  5:     public Result invoke(Invoker<?> invoker, Invocation inv) throws RpcException {  6:         // 泛化引用的调用  7:         if (inv.getMethodName().equals(Constants.$INVOKE)  8:                 && inv.getArguments() != null  9:                 && inv.getArguments().length == 3 10:                 && !ProtocolUtils.isGeneric(invoker.getUrl().getParameter(Constants.GENERIC_KEY))) { // 非泛化实现的调用 11:             String name = ((String) inv.getArguments()[0]).trim(); 12:             String[] types = (String[]) inv.getArguments()[1]; 13:             Object[] args = (Object[]) inv.getArguments()[2]; 14:             try { 15:                 // 获得对应的方法 Method 对象 16:                 Method method = ReflectUtils.findMethodByMethodSignature(invoker.getInterface(), name, types); 17:                 // 获得方法参数类型和方法参数数组 18:                 Class<?>[] params = method.getParameterTypes(); 19:                 if (args == null) { 20:                     args = new Object[params.length]; 21:                 } 22:                 // 获得 `generic` 配置项 23:                 String generic = inv.getAttachment(Constants.GENERIC_KEY); 24:                 // 【第一步】`true` ，反序列化参数，仅有 Map => POJO 25:                 if (StringUtils.isEmpty(generic) || ProtocolUtils.isDefaultGenericSerialization(generic)) { 26:                     args = PojoUtils.realize(args, params, method.getGenericParameterTypes()); 27:                 // 【第一步】`nativejava` ，反序列化参数，byte[] => 方法参数 28:                 } else if (ProtocolUtils.isJavaGenericSerialization(generic)) { 29:                     for (int i = 0; i < args.length; i++) { 30:                         if (byte[].class == args[i].getClass()) { 31:                             try { 32:                                 UnsafeByteArrayInputStream is = new UnsafeByteArrayInputStream((byte[]) args[i]); 33:                                 args[i] = ExtensionLoader.getExtensionLoader(Serialization.class).getExtension(Constants.GENERIC_SERIALIZATION_NATIVE_JAVA) 34:                                         .deserialize(null, is).readObject(); 35:                             } catch (Exception e) { 36:                                 throw new RpcException("Deserialize argument [" + (i + 1) + "] failed.", e); 37:                             } 38:                         } else { 39:                             throw new RpcException( 40:                                     new StringBuilder(32).append("Generic serialization [") 41:                                             .append(Constants.GENERIC_SERIALIZATION_NATIVE_JAVA) 42:                                             .append("] only support message type ") 43:                                             .append(byte[].class) 44:                                             .append(" and your message type is ") 45:                                             .append(args[i].getClass()).toString()); 46:                         } 47:                     } 48:                 // 【第一步】`bean` ，反序列化参数，JavaBeanDescriptor => 方法参数 49:                 } else if (ProtocolUtils.isBeanGenericSerialization(generic)) { 50:                     for (int i = 0; i < args.length; i++) { 51:                         if (args[i] instanceof JavaBeanDescriptor) { 52:                             args[i] = JavaBeanSerializeUtil.deserialize((JavaBeanDescriptor) args[i]); 53:                         } else { 54:                             throw new RpcException( 55:                                     new StringBuilder(32) 56:                                             .append("Generic serialization [") 57:                                             .append(Constants.GENERIC_SERIALIZATION_BEAN) 58:                                             .append("] only support message type ") 59:                                             .append(JavaBeanDescriptor.class.getName()) 60:                                             .append(" and your message type is ") 61:                                             .append(args[i].getClass().getName()).toString()); 62:                         } 63:                     } 64:                 } 65:                 // 【第二步】方法调用 66:                 Result result = invoker.invoke(new RpcInvocation(method, args, inv.getAttachments())); 67:                 // 【第三步】若是异常结果，并且非 GenericException 异常，则使用 GenericException 包装 68:                 if (result.hasException() 69:                         && !(result.getException() instanceof GenericException)) { 70:                     return new RpcResult(new GenericException(result.getException())); 71:                 } 72:                 // 【第三步】`nativejava` ，序列化结果，结果 => byte[] 73:                 if (ProtocolUtils.isJavaGenericSerialization(generic)) { 74:                     try { 75:                         UnsafeByteArrayOutputStream os = new UnsafeByteArrayOutputStream(512); 76:                         ExtensionLoader.getExtensionLoader(Serialization.class).getExtension(Constants.GENERIC_SERIALIZATION_NATIVE_JAVA) 77:                                 .serialize(null, os).writeObject(result.getValue()); 78:                         return new RpcResult(os.toByteArray()); 79:                     } catch (IOException e) { 80:                         throw new RpcException("Serialize result failed.", e); 81:                     } 82:                 // 【第三步】`bean` ，序列化结果，结果 => JavaBeanDescriptor 83:                 } else if (ProtocolUtils.isBeanGenericSerialization(generic)) { 84:                     return new RpcResult(JavaBeanSerializeUtil.serialize(result.getValue(), JavaBeanAccessor.METHOD)); 85:                 // 【第三步】`true` ，序列化结果，仅有 POJO => Map 86:                 } else { 87:                     return new RpcResult(PojoUtils.generalize(result.getValue())); 88:                 } 89:             } catch (NoSuchMethodException e) { 90:                 throw new RpcException(e.getMessage(), e); 91:             } catch (ClassNotFoundException e) { 92:                 throw new RpcException(e.getMessage(), e); 93:             } 94:         } 95:         // 普通调用 96:         return invoker.invoke(inv); 97:     } 98:  99: }
```

---

- 使用 Dubbo SPI Adaptive 机制，**自动加载服务提供者**
，仅限
。
- 第 96 行：若是普通调用( **非泛化引用的调用**
)，调用
Invoker#invoke(invocation)
方法，继续过滤链的调用，最终调用 Service 服务。
- 第 6 至 95 行： 若是**泛化引用的调用注意泛化实现**
，通过方法( 包括方法名、参数 )判断。
，【第 10 行】非
的调用。
- 第 16 行：调用 [ReflectUtils#findMethodByMethodSignature(Class<?> clazz, String methodName, String[] parameterTypes)](https://github.com/YunaiV/dubbo/blob/f83e70b53389a064e49babe32e61a5648002a44a/dubbo-common/src/main/java/com/alibaba/dubbo/common/utils/ReflectUtils.java#L768-L814)**Method**
方法，通过反射，获得对应的方法
对象。具体的代码实现，胖友自己查看哈。
- 第 17 至 21 行：获得**方法参数类型和方法参数**
数组。
- 第 23 行：获得
generic
配置项。
- ========== 【第一步：反序列化参数】 ==========
- 第 24 至 26 行：[PojoUtils#realize(Object[] objs, Class<?>[] types, Type[] gtypes)](https://github.com/YunaiV/dubbo/blob/f83e70b53389a064e49babe32e61a5648002a44a/dubbo-common/src/main/java/com/alibaba/dubbo/common/utils/PojoUtils.java#L81-L89)**注意反序列化**
generic = true
，调用
方法，反序列化参数。
，在该方法中，只有带有
class
属性的 Map ，需要
成对应的 POJO 对象。
- 第 27 至 47 行：
generic = nativejava
，调用
NativeJavaSerialization#deserialize(url, input)
方法，反序列化参数，即
byte[] => 方法参数
。
- 第 48 至 64 行：
generic = bean
，调用
JavaBeanSerializeUtil#deserialize(JavaBeanDescriptor)
方法，反序列化参数，即
JavaBeanDescriptor => 方法参数
。
- ========== 【第二步：方法调用】 ==========
- 第 66 行：创建**新的非常关键具体**
RpcInvocation 对象。这是
的一步，
$invoke
的泛化调用，被转换成
的普通调用。
- 第 66 行：调用
Invoker#invoke(invocation)
方法，继续过滤链的调用，最终调用 Service 服务。
- ========== 【第三步：序列化结果】 ==========
- 第 68 至 71 行：若是异常结果，并且非 GenericException 异常，可能这个异常在服务消费端是**没有**[GenericException](https://github.com/YunaiV/dubbo/blob/f83e70b53389a064e49babe32e61a5648002a44a/dubbo-rpc/dubbo-rpc-api/src/main/java/com/alibaba/dubbo/rpc/service/GenericException.java)**包装后返回**
的，因此需要使用
。GenericException 的代码如下：

```plain text
plain public class GenericException extends RuntimeException {              private String exceptionClass;          private String exceptionMessage;          public GenericException() {     }          public GenericException(String exceptionClass, String exceptionMessage) {         super(exceptionMessage);         this.exceptionClass = exceptionClass;         this.exceptionMessage = exceptionMessage;     }          public GenericException(Throwable cause) {         super(StringUtils.toString(cause));         this.exceptionClass = cause.getClass().getName();         this.exceptionMessage = cause.getMessage();     }          // ... 省略 getting/setting 的方法 }
```

---

- 第 72 至 81 行：
generic = nativejava
，调用
NativeJavaSerialization#serialize(url, output)
方法，序列化结果，即
结果 => byte[]
。
- 第 82 至 84 行：
generic = bean
，调用
JavaBeanSerializeUtil#serialize(Object, JavaBeanAccessor)
方法，序列化结果，即
结果 => JavaBeanDescriptor
。
- 第 85 至 88 行：
generic = true
，调用
PojoUtils#generalize(Object)
方法，序列化结果，仅有
POJO => Map
。

# 666. 彩蛋

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038374487-282006d8-3a13-4358-84d4-f9e3fef6c172.png)

知识星球

艿艿在本文，并未解析 POJO 的序列化和反序列化的相关代码，感兴趣的胖友，可以自己研究。