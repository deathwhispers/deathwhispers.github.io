---
layout: post
title: 过滤器（十一）之ValidationFilter
slug: dubbo-filter-validation
type:
  - note
date: 2022-05-23
status: draft
tags:
  - Dubbo
categories:
  - Dubbo
mood:
weather:
author: deathwhispers
created: 2022-05-23 11:52
updated: 2022-05-23 18:33
---
本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

本文分享 dubbo-filter-validation 项目的 ValidationFilter 过滤器，用于服务**消费者**和**提供者**中，提供 **参数验证** 的功能。在 [《Dubbo 用户指南 —— 参数验证》](http://dubbo.apache.org/zh-cn/docs/user/demos/parameter-validation.html) 定义如下：

参数验证功能，是基于 [JSR303](https://jcp.org/en/jsr/detail?id=303) Bean Validation 实现的，用户只需标识 JSR303 标准的验证 annotation，并通过声明 filter 来实现验证。

- **配置示例**
和
，官方文档已经写的很齐全，笔者就不多哔哔了。
- 如下是新版本的 Maven 依赖的例子：

```plain text
plain <!-- JSR 303 - Bean Validation begin --> <dependency>     <groupId>javax.validation</groupId>     <artifactId>validation-api</artifactId>     <version>1.1.0.Final</version> </dependency> <dependency>     <groupId>org.hibernate</groupId>     <artifactId>hibernate-validator</artifactId>     <version>5.3.4.Final</version> </dependency> <dependency>     <groupId>javax.el</groupId>     <artifactId>javax.el-api</artifactId>     <version>2.2.4</version> </dependency> <dependency>     <groupId>org.glassfish.web</groupId>     <artifactId>javax.el</artifactId>     <version>2.2.4</version> </dependency> <!-- JSR 303 - Bean Validation end -->
```

---

本文涉及的类，如下图所示：

![](/assets/images/learning/dubbo/dubbo-filter-validation/062d60c0ed2878e236c95e926d655c64.png)

类图

# 2. ValidationFilter

com.alibaba.dubbo.validation.filter.ValidationFilter ，实现 Filter 接口，参数验证过滤器实现类。代码如下：

```plain text
plain 1: @Activate(group = {Constants.CONSUMER, Constants.PROVIDER}, value = Constants.VALIDATION_KEY, order = 10000)  2: public class ValidationFilter implements Filter {  3:   4:     /**  5:      * Validation$Adaptive 对象  6:      *  7:      * 通过 Dubbo SPI 机制，调用 {@link #setValidation(Validation)} 方法，进行注入  8:      */  9:     private Validation validation; 10:  11:     public void setValidation(Validation validation) { 12:         this.validation = validation; 13:     } 14:  15:     @Override 16:     public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException { 17:         if (validation != null && !invocation.getMethodName().startsWith("$") // 非泛化调用和回音调用等方法 18:                 && ConfigUtils.isNotEmpty(invoker.getUrl().getMethodParameter(invocation.getMethodName(), Constants.VALIDATION_KEY))) { // 方法开启 Validation 功能 19:             try { 20:                 // 获得 Validator 对象 21:                 Validator validator = validation.getValidator(invoker.getUrl()); 22:                 // 使用 Validator ，验证方法参数。若不合法，抛出异常。 23:                 if (validator != null) { 24:                     validator.validate(invocation.getMethodName(), invocation.getParameterTypes(), invocation.getArguments()); 25:                 } 26:             } catch (RpcException e) { 27:                 throw e; 28:             } catch (Throwable t) { 29:                 return new RpcResult(t); 30:             } 31:         } 32:         // 服务调用 33:         return invoker.invoke(invocation); 34:     } 35:  36: }
```

---

- 第 17 行：非泛化调用和回音调用等方法。
- 第 18 行：判断方法**开启部分**
Validation 功能。因为，一个服务里，可能只有
方法开启了 Validation 功能。
- 第 21 行：调用 **URL**
Validation$Adaptive#getValidator(url)
方法，基于
为维度，获得 Validator 对象。
- 第 22 至 25 行：调用
Validator#validate(String methodName, Class<?>[] parameterTypes, Object[] arguments)
方法，方法参数验证。若不合法，抛出异常。
- 第 33 行：调用
Invoker#invoke(invocation)
方法，服务调用。

# 3. API 定义

## 3.1 Validator

com.alibaba.dubbo.validation.Validator ，验证器接口。代码如下：

```plain text
plain public interface Validator {      /**      * 方法参数验证      *      * @param methodName 方法名      * @param parameterTypes 参数类型数组      * @param arguments 参数值数组      * @throws Exception 当发生异常时      */     void validate(String methodName, Class<?>[] parameterTypes, Object[] arguments) throws Exception;  }
```

---

## 3.2 Validation

com.alibaba.dubbo.validation.Validation ，Validator 工厂**接口**。代码如下：

```plain text
plain @SPI("jvalidation") public interface Validation {      /**      * 获得 Validator 对象      *      * @param url URL      * @return Validator      */     @Adaptive(Constants.VALIDATION_KEY)     Validator getValidator(URL url);  }
```

---

- @SPI(“jvalidation”)**拓展点**
注解，Dubbo SPI
，默认为
“jvalidation”
。
- @Adaptive(“validation”)
注解，基于 Dubbo SPI Adaptive 机制，加载对应的 Validator 实现，使用
URL.validation
属性。

### 3.2.1 AbstractValidation

com.alibaba.dubbo.validation.support.AbstractValidation ，实现 Validation 接口，Validator 工厂**抽象类**。代码如下：

```plain text
plain public abstract class AbstractValidation implements Validation {      /**      * Validator 集合      *      * key：URL      */     private final ConcurrentMap<String, Validator> validators = new ConcurrentHashMap<String, Validator>();      @Override     public Validator getValidator(URL url) {         // 获得 Validator 对象         String key = url.toFullString();         Validator validator = validators.get(key);         // 不存在，创建 Validator 对象，并缓存         if (validator == null) {             validators.put(key, createValidator(url));             validator = validators.get(key);         }         return validator;     }      /**      * 创建 Validator 对象      *      * @param url URL      * @return Validator 对象      */     protected abstract Validator createValidator(URL url);  }
```

---

# 3.3 @MethodValidated

com.alibaba.dubbo.validation.@MethodValidated ，方法分组验证**注解**。代码如下：

```plain text
plain @Target({ElementType.METHOD}) @Retention(RetentionPolicy.RUNTIME) @Documented public @interface MethodValidated {      /**      * @return 分组集合      */     Class<?>[] value() default {};  }
```

---

- 使用场景：当调用某个方法时，需要检查多个分组，可以在接口方法上加上该注解。
- 用法：

```plain text
plain @MethodValidated({Save.class, Update.class}) void relatedQuery(ValidationParameter parameter);
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">在接口方法上增加注解，表示 </font><font style="color:rgb(51, 51, 51);">#relatedQuery(ValidationParameter)</font><font style="color:rgb(51, 51, 51);"> 这个方法，需要同时检查 Save 和 Update 这两个分组。</font>
- <font style="color:rgb(51, 51, 51);">如果胖友对 Java Bean Validation 分组不熟悉，可以理解起来比较绕。可以跑下官方提供的 </font>[com.alibaba.dubbo.config.validation](https://github.com/YunaiV/dubbo/tree/f4216485f5641ea5cf406d1e58503c5651f86432/dubbo-config/dubbo-config-api/src/test/java/com/alibaba/dubbo/config/validation)<font style="color:rgb(51, 51, 51);"> 的立足。</font>![](/assets/images/learning/dubbo/dubbo-filter-validation/87098c48e6e043e381a2505c69d58f3b.png)<font style="color:rgb(153, 153, 153);">relatedQuery</font>
```

# 4. JSR303 实现

基于 [JSR303](https://jcp.org/en/jsr/detail?id=303) Bean Validation 实现的，用户只需标识 JSR303 标准的验证 annotation 。

## 4.1 JValidator

com.alibaba.dubbo.validation.support.jvalidation.JValidator ，实现 Validator 接口，基于 [JSR303](https://jcp.org/en/jsr/detail?id=303) 的验证器实现类。

### 4.1.1 构造方法

```plain text
plain /**  * 服务接口类  */ private final Class<?> clazz; /**  * Validator 对象  */ private final javax.validation.Validator validator;  @SuppressWarnings({"unchecked", "rawtypes"}) public JValidator(URL url) {     // 获得服务接口类     this.clazz = ReflectUtils.forName(url.getServiceInterface());     // 获得 `"jvalidation"` 配置项     String jvalidation = url.getParameter("jvalidation");     // 获得 ValidatorFactory 对象     ValidatorFactory factory;     if (jvalidation != null && jvalidation.length() > 0) { // 指定实现         factory = Validation.byProvider((Class) ReflectUtils.forName(jvalidation)).configure().buildValidatorFactory();     } else { // 默认         factory = Validation.buildDefaultValidatorFactory();     }     // 获得 javax Validator 对象     this.validator = factory.getValidator(); }
```

---

- “jvalidation”**指定**
配置项，可
具体的 JSR303 的实现类。
- 如果我们**未配置**
，并且引入 Hibernate Validator ，则使用的是 HibernateValidatorFactory 。

### 4.1.2 validate

```plain text
plain 1: @Override  2: public void validate(String methodName, Class<?>[] parameterTypes, Object[] arguments) throws Exception {  3:     // 验证分组集合  4:     List<Class<?>> groups = new ArrayList<Class<?>>();  5:     // 【第一种】添加以方法命名的内部接口，作为验证分组。例如 `ValidationService#save(...)` 方法，对应 `ValidationService.Save` 接口。  6:     String methodClassName = clazz.getName() + "$" + toUpperMethodName(methodName);  7:     Class<?> methodClass;  8:     try {  9:         methodClass = Class.forName(methodClassName, false, Thread.currentThread().getContextClassLoader()); 10:         groups.add(methodClass); 11:     } catch (ClassNotFoundException e) { 12:     } 13:     // 【第二种】添加方法的 @MethodValidated 注解的值对应的类，作为验证分组。 14:     Method method = clazz.getMethod(methodName, parameterTypes); 15:     Class<?>[] methodClasses; 16:     if (method.isAnnotationPresent(MethodValidated.class)){ 17:         methodClasses = method.getAnnotation(MethodValidated.class).value(); 18:         groups.addAll(Arrays.asList(methodClasses)); 19:     } 20:     // 【第三种】添加 Default.class 类，作为验证分组。在 JSR 303 中，未设置分组的验证注解，使用 Default.class 。 21:     // add into default group 22:     groups.add(0, Default.class); 23:     // 【第四种】添加服务接口类，作为验证分组。 24:     groups.add(1, clazz); 25:     // convert list to array 26:     Class<?>[] classGroups = groups.toArray(new Class[0]); 27:  28:     // 验证错误集合 29:     Set<ConstraintViolation<?>> violations = new HashSet<ConstraintViolation<?>>(); 30:     // 【第一步】获得方法参数的 Bean 对象。因为，JSR 303 是 Java Bean Validation ，以 Bean 为维度。 31:     Object parameterBean = getMethodParameterBean(clazz, method, arguments); 32:     // 【第一步】验证 Bean 对象。 33:     if (parameterBean != null) { 34:         violations.addAll(validator.validate(parameterBean, classGroups)); 35:     } 36:     // 【第二步】验证集合参数 37:     for (Object arg : arguments) { 38:         validate(violations, arg, classGroups); 39:     } 40:     // 若有错误，抛出 ConstraintViolationException 异常。 41:     if (!violations.isEmpty()) { 42:         logger.error("Failed to validate service: " + clazz.getName() + ", method: " + methodName + ", cause: " + violations); 43:         throw new ConstraintViolationException("Failed to validate service: " + clazz.getName() + ", method: " + methodName + ", cause: " + violations, violations); 44:     } 45: }
```

---

- ============ 【第一步】获得验证分组集合 ============
- 第 4 行：验证分组集合
group
，目前有四种来源。
- 【第一种】第 5 至 12 行：添加以方法命名的内部接口，作为验证分组。例如
ValidationService#save(…)
方法，对应
ValidationService.Save
接口。
- 【第二种】第 13 至 19 行：添加方法的
@MethodValidated
注解的值对应的类，作为验证分组。
- 【第三种】第 22 行：添加 Default.class 类，作为验证分组。在 JSR 303 中，未设置分组的验证注解，使用 Default.class 。
- 【第四种】第 24 行：添加服务接口类
clazz
，作为验证分组。
- 最终生成的验证分组集合的顺序为：【第三种】》【第四种】》【第一种】》【第二种】。
- ============ 【第二步】验证方法参数 ============
- 第 29 行：验证错误集合
violations
。
- 【第一步】调用 [「4.1.3 getMethodParameterBean」](http://svip.iocoder.cn/Dubbo/filter-validation-filter/#)
#getMethodParameterBean(Class<?> clazz, Method method, Object[] args)
方法，获得方法参数的 Bean 对象。因为，JSR 303 是 Java Bean Validation ，以 Bean 为维度。具体的实现，我们在
中，详细解析。
- 【第一步】调用 **Bean**
Validator#validate(T object, Class<?>… groups)
方法，验证
对象。
- 【第二步】循环方法参数，调用 **集合为什么会有这一步不会校验集合中的每个元素**
#validate(violations, arg, classGroups)
方法，验证
参数。
？因为，在【第一步】中，校验的是 Constraint 注解的参数( 例如
@NotNull
) ，但是呢，若是集合参数，
。我们来举个例子：

```plain text
plain void saves(@NotNull(message = "至少需要保存一个用户") User[] users);
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">【第一步】校验 </font><font style="color:rgb(51, 51, 51);">users</font><font style="color:rgb(51, 51, 51);"> 参数的 </font><font style="color:rgb(51, 51, 51);">@NotNull</font><font style="color:rgb(51, 51, 51);"> 约束。</font>
- <font style="color:rgb(51, 51, 51);">【第二步】校验 </font><font style="color:rgb(51, 51, 51);">users</font><font style="color:rgb(51, 51, 51);"> 参数中的</font>**<font style="color:rgb(51, 51, 51);">每个 User</font>**<font style="color:rgb(51, 51, 51);"> 的约束。</font>
```

- 第 40 至 44 行：若有验证错误，抛出 ConstraintViolationException 异常。

---

#validate(Set<ConstraintViolation<?>> violations, Object arg, Class<?>… groups) 方法，代码如下：

```plain text
plain 1: /**  2:  * 验证集合参数  3:  *  4:  * @param violations 验证错误集合  5:  * @param arg 参数  6:  * @param groups 验证分组集合  7:  */  8: private void validate(Set<ConstraintViolation<?>> violations, Object arg, Class<?>... groups) {  9:     if (arg != null && !isPrimitives(arg.getClass())) { 10:         // [] 数组 11:         if (Object[].class.isInstance(arg)) { 12:             for (Object item : (Object[]) arg) { 13:                 validate(violations, item, groups); // 单个元素 14:             } 15:         // Collection 16:         } else if (Collection.class.isInstance(arg)) { 17:             for (Object item : (Collection<?>) arg) { 18:                 validate(violations, item, groups); // 单个元素 19:             } 20:         // Map 21:         } else if (Map.class.isInstance(arg)) { 22:             for (Map.Entry<?, ?> entry : ((Map<?, ?>) arg).entrySet()) { 23:                 validate(violations, entry.getKey(), groups); // 单个元素 24:                 validate(violations, entry.getValue(), groups); // 单个元素 25:             } 26:         // 单个元素 27:         } else { 28:             violations.addAll(validator.validate(arg, groups)); 29:         } 30:     } 31: }
```

---

- 第 9 行：调用 **基本类型第一步**
#isPrimitives(Class<?> cls)
方法，判断是否为
。若是基本类型，已经被【
】给验证了，避免重复验证。代码如下：

```plain text
plain private static boolean isPrimitives(Class<?> cls) {     // [] 数组，使用内部的类来判断     if (cls.isArray()) {         return isPrimitive(cls.getComponentType());     }     // 直接判断     return isPrimitive(cls); }  private static boolean isPrimitive(Class<?> cls) {     return cls.isPrimitive() || cls == String.class || cls == Boolean.class || cls == Character.class             || Number.class.isAssignableFrom(cls) || Date.class.isAssignableFrom(cls); }
```

---

- 第 10 至 14 行：验证
    - [ ] [ ]
数组参数，循环调用【第 26 至 29】的验证。
- 第 15 至 19 行：验证 Collection 参数，循环调用【第 26 至 29】的验证。
- 第 20 至 25 行：验证 Map 参数，循环调用【第 26 至 29】的验证。
- **第 26 至 29 行单个**
：验证
参数。

### 4.1.3 getMethodParameterBean

在看 #getMethodParameterBean(Class<?> clazz, Method method, Object[] args) 的具体实现代码之前，我们来看下它，根据方法，**自动生成** Bean 类的例子。

- 接口方法，代码如下：

```plain text
plain void demo(@NotNull(message = "名字不能为空") @Min(value = 6, message = "昵称不能太短") String name,           String password, // 不校验           @NotNull(message = "至少需要保存一个用户") User user);
```

---

- 生成 Bean 类，代码如下：

```plain text
plain package com.alibaba.dubbo.demo.DemoService_DemoParameter_java.lang.String_java.lang.String_com.alibaba.dubbo.demo.entity;  public class User {      @NotNull(message = "名字不能为空")      @Min(value = 6, message = "昵称不能太短")     public java.lang.String name;          public java.lang.String password;          @NotNull(message = "至少需要保存一个用户")     public com.alibaba.dubbo.demo.entity.User user;          public User() {}  }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);"> Javassist 生成的类，使用 JD-GUI 反编译一直报错。所以，该类是笔者，</font>**<font style="color:rgb(51, 51, 51);">手工</font>**<font style="color:rgb(51, 51, 51);">生成的。哈哈哈，意思能达到就好。</font>
```

---

#getMethodParameterBean(Class<?> clazz, Method method, Object[] args) 方法，代码如下：

```plain text
plain 1: /**  2:  * 使用方法参数，创建 Bean 对象。  3:  *  4:  * 因为该 Bean 对象，实际不存在对应类，使用 Javassist 动态编译生成。  5:  *  6:  * @param clazz 服务接口类  7:  * @param method 方法  8:  * @param args 参数数组  9:  * @return Bean 对象 10:  */ 11: private static Object getMethodParameterBean(Class<?> clazz, Method method, Object[] args) { 12:     // 无 Constraint 注解的方法参数，无需创建 Bean 对象。 13:     if (!hasConstraintParameter(method)) { 14:         return null; 15:     } 16:     try { 17:         // 获得 Bean 类名 18:         String parameterClassName = generateMethodParameterClassName(clazz, method); 19:         Class<?> parameterClass; 20:         try { 21:             // 获得 Bean 类 22:             parameterClass = Class.forName(parameterClassName, true, clazz.getClassLoader()); 23:         } catch (ClassNotFoundException e) { // 类不存在，使用 Javassist 动态编译生成 24:             // 创建 ClassPool 对象 25:             ClassPool pool = ClassGenerator.getClassPool(clazz.getClassLoader()); 26:             // 创建 CtClass 对象 27:             CtClass ctClass = pool.makeClass(parameterClassName); 28:             // 设置 Java 版本为 5 29:             ClassFile classFile = ctClass.getClassFile(); 30:             classFile.setVersionToJava5(); 31:             // 添加默认构造方法 32:             ctClass.addConstructor(CtNewConstructor.defaultConstructor(pool.getCtClass(parameterClassName))); 33:             // 循环每个方法参数，生成对应的类的属性 34:             // parameter fields 35:             Class<?>[] parameterTypes = method.getParameterTypes(); 36:             Annotation[][] parameterAnnotations = method.getParameterAnnotations(); 37:             for (int i = 0; i < parameterTypes.length; i++) { 38:                 Class<?> type = parameterTypes[i]; 39:                 Annotation[] annotations = parameterAnnotations[i]; 40:                 // 创建注解属性 41:                 AnnotationsAttribute attribute = new AnnotationsAttribute(classFile.getConstPool(), AnnotationsAttribute.visibleTag); 42:                 // 循环每个方法参数的每个注解 43:                 for (Annotation annotation : annotations) { 44:                     if (annotation.annotationType().isAnnotationPresent(Constraint.class)) { // 约束条件的注解，例如 @NotNull 45:                         javassist.bytecode.annotation.Annotation ja = new javassist.bytecode.annotation.Annotation( 46:                                 classFile.getConstPool(), pool.getCtClass(annotation.annotationType().getName())); 47:                         // 循环注解的每个方法 48:                         Method[] members = annotation.annotationType().getMethods(); 49:                         for (Method member : members) { 50:                             if (Modifier.isPublic(member.getModifiers()) 51:                                     && member.getParameterTypes().length == 0 52:                                     && member.getDeclaringClass() == annotation.annotationType()) { 53:                                 // 将注解，添加到类的属性上 54:                                 Object value = member.invoke(annotation); 55:                                 if (null != value) { 56:                                     MemberValue memberValue = createMemberValue( 57:                                             classFile.getConstPool(), pool.get(member.getReturnType().getName()), value); 58:                                     ja.addMemberValue(member.getName(), memberValue); 59:                                 } 60:                             } 61:                         } 62:                         attribute.addAnnotation(ja); 63:                     } 64:                 } 65:                 // 创建属性 66:                 String fieldName = method.getName() + "Argument" + i; 67:                 CtField ctField = CtField.make("public " + type.getCanonicalName() + " " + fieldName + ";", pool.getCtClass(parameterClassName)); 68:                 ctField.getFieldInfo().addAttribute(attribute); 69:                 // 添加属性 70:                 ctClass.addField(ctField); 71:             } 72:             // 生成类 73:             parameterClass = ctClass.toClass(clazz.getClassLoader(), null); 74:         } 75:         // 创建 Bean 对象 76:         Object parameterBean = parameterClass.newInstance(); 77:         // 设置 Bean 对象的每个属性的值 78:         for (int i = 0; i < args.length; i++) { 79:             Field field = parameterClass.getField(method.getName() + "Argument" + i); 80:             field.set(parameterBean, args[i]); 81:         } 82:         return parameterBean; 83:     } catch (Throwable e) { 84:         logger.warn(e.getMessage(), e); 85:         return null; 86:     } 87: }
```

---

- 第 13 至 15 行：调用 **Constraint**
#hasConstraintParameter(method)
方法，判断是否有
注解( 例如，
@NotNull
)的方法参数。若没有，则无需创建 Bean 对象。代码如下：

```plain text
plain private static boolean hasConstraintParameter(Method method) {     Annotation[][] parameterAnnotations = method.getParameterAnnotations();     // 循环所有方法参数的注解     if (parameterAnnotations != null && parameterAnnotations.length > 0) {         // 循环每个方法参数的注解数组         for (Annotation[] annotations : parameterAnnotations) {             // 是否有 Constraint 注解             for (Annotation annotation : annotations) {                 if (annotation.annotationType().isAnnotationPresent(Constraint.class)) {                     return true;                 }             }         }     }     return false; }
```

---

- 第 17 至 22 行：获得 Bean 类。
- 第 23 至 73 行：若 Bean 类**不存在每个属性的值**
，使用 Javassist 动态编译生成。 代码比较简单，已经添加详细注释，胖友耐心看看哈。其中，
#createMemberValue(ConstPool cp, CtClass type, Object value)
方法，获得注解
，代码如下：

```plain text
plain // Copy from javassist.bytecode.annotation.Annotation.createMemberValue(ConstPool, CtClass); private static MemberValue createMemberValue(ConstPool cp, CtClass type, Object value) throws NotFoundException {     MemberValue memberValue = javassist.bytecode.annotation.Annotation.createMemberValue(cp, type);     if (memberValue instanceof BooleanMemberValue) // Boolean         ((BooleanMemberValue) memberValue).setValue((Boolean) value);     else if (memberValue instanceof ByteMemberValue) // Byte         ((ByteMemberValue) memberValue).setValue((Byte) value);     else if (memberValue instanceof CharMemberValue) // Char         ((CharMemberValue) memberValue).setValue((Character) value);     else if (memberValue instanceof ShortMemberValue) // Short         ((ShortMemberValue) memberValue).setValue((Short) value);     else if (memberValue instanceof IntegerMemberValue) // Integer         ((IntegerMemberValue) memberValue).setValue((Integer) value);     else if (memberValue instanceof LongMemberValue) // Long         ((LongMemberValue) memberValue).setValue((Long) value);     else if (memberValue instanceof FloatMemberValue) // Float         ((FloatMemberValue) memberValue).setValue((Float) value);     else if (memberValue instanceof DoubleMemberValue)         ((DoubleMemberValue) memberValue).setValue((Double) value);     else if (memberValue instanceof ClassMemberValue) // Class         ((ClassMemberValue) memberValue).setValue(((Class<?>) value).getName());     else if (memberValue instanceof StringMemberValue) // String         ((StringMemberValue) memberValue).setValue((String) value);     else if (memberValue instanceof EnumMemberValue) // Enum         ((EnumMemberValue) memberValue).setValue(((Enum<?>) value).name());     /* else if (memberValue instanceof AnnotationMemberValue) */     else if (memberValue instanceof ArrayMemberValue) { // 数组         CtClass arrayType = type.getComponentType();         int len = Array.getLength(value);         // 循环，递归         MemberValue[] members = new MemberValue[len];         for (int i = 0; i < len; i++) {             members[i] = createMemberValue(cp, arrayType, Array.get(value, i));         }         ((ArrayMemberValue) memberValue).setValue(members);     }     return memberValue; }
```

---

- 第 75 至 81 行：创建 Bean 对象，**设置 Bean 对象的每个属性的值**
。

又是一处，使用 Javassist 动态编译类的代码。好用！！！

## 4.2 JValidation

com.alibaba.dubbo.validation.support.jvalidation.JValidation ，实现 AbstractValidation 抽象类，代码如下：

```plain text
plain public class JValidation extends AbstractValidation {      @Override     protected Validator createValidator(URL url) {         return new JValidator(url);     }  }
```

---

# 666. 彩蛋

美滋滋，终于弄懂，为什么 JSR303 是 Java Bean Validation ，结果接口方法上，每个参数都添加 Constraint 的注解，结果也可以做校验。

推荐两篇文章：

- [《JSR 303 - Bean Validation 介绍及最佳实践》](https://www.ibm.com/developerworks/cn/java/j-lo-jsr303/)
- [《Spring4新特性——集成Bean Validation 1.1(JSR-349)到SpringMVC》](http://jinnianshilongnian.iteye.com/blog/1990081)