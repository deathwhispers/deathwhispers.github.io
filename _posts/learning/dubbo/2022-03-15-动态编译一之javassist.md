---
layout: post
title: 动态编译（一）之Javassist
author: deathwhispers
date: 2022-03-15
slug: dubbo-compiler-javassist
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-04-25 11:50
updated: 2022-04-25 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

在 Java 语言中，大多数情况下，我们已经编写好 Java 类，并编译成 Class 文件进行运行。但是在一些场景下，例如动态代理，需要运用到**动态编译**的技术。虽然我们也可以用反射的技术实现，但是相比来说，还是有一定的性能差距。

例如，在 [《精尽 Dubbo 源码分析 —— 拓展机制 SPI》](http://svip.iocoder.cn/Dubbo/spi/?self=) 的 [「4.5.4 createAdaptiveExtensionClassCode」](http://svip.iocoder.cn/Dubbo/compiler-javassist/#) 小节中，我们可以看到如下代码：

```plain text
plain 1: /**  2:  * 自动生成自适应拓展的代码实现，并编译后返回该类。  3:  *  4:  * @return 类  5:  */  6: private Class<?> createAdaptiveExtensionClass() {  7:     // 自动生成自适应拓展的代码实现的字符串  8:     String code = createAdaptiveExtensionClassCode();  9:     // 编译代码，并返回该类 10:     ClassLoader classLoader = findClassLoader(); 11:     com.alibaba.dubbo.common.compiler.Compiler compiler = ExtensionLoader.getExtensionLoader(com.alibaba.dubbo.common.compiler.Compiler.class).getAdaptiveExtension(); 12:     return compiler.compile(code, classLoader); 13: }
```

---

调用 Compiler#compile(code, classLoader) 方法，编译代码，并返回该类。Compiler 基于 Dubbo SPI 机制进行加载，目前有两种实现：

- JdkCompiler

```plain text
plain <dubbo:application compiler="jdk" />
```

---

- JavassistCompiler

```plain text
plain <dubbo:application compiler="javassist" />
```

---

**缺省**使用 JavassistCompiler 。

本文仅分享 JavassistCompiler 的实现。

---

动态编译，在 dubbo-common 模块的 [compiler](https://github.com/YunaiV/dubbo/tree/ded892cb2f31e2847c18f773e16b16a6fbaf53d2/dubbo-common/src/main/java/com/alibaba/dubbo/common/compiler) 包下实现，整体类结构如下图：

![](/assets/images/learning/dubbo/dubbo-compiler-javassist/50eb8eebc17381529d607b22e92f2d4d.png)

类图

# 2. Compiler

com.alibaba.dubbo.common.compiler.Compiler ，编辑器接口。代码如下：

```plain text
plain @SPI("javassist") public interface Compiler {      /**      * Compile java source code.      *      * 编译 Java 代码字符串      *      * @param code        Java source code      *                    Java 代码字符串      * @param classLoader classloader      *                    类加载器      * @return Compiled class      *                    编译后的类      */     Class<?> compile(String code, ClassLoader classLoader);  }
```

---

- @SPI("javassist")
注解，使用 Dubbo SPI 机制，默认拓展为 Javassist 。
- code**例子**
参数，Java 代码字符串。如下是 ProxyFactory$Adaptive 的自适应拓展的代码实现的字符串生成
：
![](/assets/images/learning/dubbo/dubbo-compiler-javassist/c73cb291227ae3a3c7e5d0b0f8e6f5b6.png)
自适应拓展的代码实现的字符串生成例子

# 3. AdaptiveCompiler

com.alibaba.dubbo.common.compiler.support.AdaptiveCompiler ，实现 Compiler 接口，自适应 Compiler 实现类。

```plain text
plain 1: @Adaptive  2: public class AdaptiveCompiler implements Compiler {  3:   4:     /**  5:      * 默认编辑器的拓展名  6:      */  7:     private static volatile String DEFAULT_COMPILER;  8:   9:     public static void setDefaultCompiler(String compiler) { 10:         DEFAULT_COMPILER = compiler; 11:     } 12:  13:     @Override public Class<?> compile(String code, ClassLoader classLoader) { 14:         Compiler compiler; 15:         // 获得 Compiler 的 ExtensionLoader 对象。 16:         ExtensionLoader<Compiler> loader = ExtensionLoader.getExtensionLoader(Compiler.class); 17:         String name = DEFAULT_COMPILER; // copy reference 18:         // 使用设置的拓展名，获得 Compiler 拓展对象 19:         if (name != null && name.length() > 0) { 20:             compiler = loader.getExtension(name); 21:         // 获得默认的 Compiler 拓展对象 22:         } else { 23:             compiler = loader.getDefaultExtension(); 24:         } 25:         // 26:         return compiler.compile(code, classLoader); 27:     } 28:  29: }
```

---

- #setDefaultCompiler(compiler)**静态**
方法，设置默认编辑器的拓展名(
DEFAULT_COMPILER
)。该方法被
ApplicationConfig#setCompiler(compiler)
方法调用，代码如下：

```plain text
plain // ApplicationConfig.java public void setCompiler(String compiler) {     this.compiler = compiler;     AdaptiveCompiler.setDefaultCompiler(compiler); }
```

---

```plain text
- <font style="color:rgb(51, 51, 51);">在 </font><font style="color:rgb(51, 51, 51);"><dubbo:application compiler="" /></font><font style="color:rgb(51, 51, 51);"> 配置下，可触发该方法。</font>
```

- #compile(code, classLoader)**实现**
方法：
    - 第 16 行：调用
ExtensionLoader#getExtensionLoader(Class<?> type)
方法，获得 Compiler 的 ExtensionLoader 对象。
    - 第 17 行：声明
name
变量，引用
DEFAULT_COMPILER
的值。避免在【第 19 至 20 行】的代码过程中，值变了。
    - 第 19 至 20 行：使用**设置**
的拓展名，获得 Compiler 拓展对象。
    - 第 22 至 24 行：获得默认的 Compiler 拓展对象。
    - 第 26 行：调用真正的 Compiler 对象，动态编译代码。

# 4. AbstractCompiler

com.alibaba.dubbo.common.compiler.support.AbstractCompiler ，实现 Compiler 接口，Compiler **抽象类**。代码如下：

```plain text
plain public abstract class AbstractCompiler implements Compiler {      /**      * 正则 - 包名      */     private static final Pattern PACKAGE_PATTERN = Pattern.compile("package\\s+([$_a-zA-Z][$_a-zA-Z0-9\\.]*);");     /**      * 正则 - 类名      */     private static final Pattern CLASS_PATTERN = Pattern.compile("class\\s+([$_a-zA-Z][$_a-zA-Z0-9]*)\\s+");      public Class<?> compile(String code, ClassLoader classLoader) {         // 获得包名         code = code.trim();         Matcher matcher = PACKAGE_PATTERN.matcher(code);         String pkg;         if (matcher.find()) {             pkg = matcher.group(1);         } else {             pkg = "";         }         // 获得类名         matcher = CLASS_PATTERN.matcher(code);         String cls;         if (matcher.find()) {             cls = matcher.group(1);         } else {             throw new IllegalArgumentException("No such class name in " + code);         }         // 获得完整类名         String className = pkg != null && pkg.length() > 0 ? pkg + "." + cls : cls;         // 加载类，若已经存在         try {             // 加载成功，说明已存在             return Class.forName(className, true, ClassHelper.getCallerClassLoader(getClass())); // classloader 为调用方的         } catch (ClassNotFoundException e) { // 类不存在，说明可能未编译过，进行编译             // 代码格式不正确             if (!code.endsWith("}")) {                 throw new IllegalStateException("The java code not endsWith \"}\", code: \n" + code + "\n");             }             // 编译代码             try {                 return doCompile(className, code);             } catch (RuntimeException t) {                 throw t;             } catch (Throwable t) {                 throw new IllegalStateException("Failed to compile class, cause: " + t.getMessage() + ", class: " + className + ", code: \n" + code + "\n, stack: " + ClassUtils.toString(t));             }         }     }      /**      * 编译代码      *      * @param name 类名      * @param source 代码      * @return 编译后的类      * @throws Throwable 发生异常      */     protected abstract Class<?> doCompile(String name, String source) throws Throwable;  }
```

---

- 首先获得完整类名，后使用类加载器加载该类：
    - 若成功，说明已经存在（可能已经编译过）。
    - 若失败，进行编译。
- 代码比较简单，胖友可以在看下注释。

# 5. JavassistCompiler

Javassist 是一个开源的分析、编辑和创建 Java 字节码的类库。通过使用Javassist 对字节码操作可以实现动态 "AOP" 框架。

关于 Java 字节码的处理，目前有很多工具，如 bcel，asm( cglib只是对asm又封装了一层 )。不过这些都需要直接跟虚拟机指令打交道。

Javassist 的主要的优点，在于简单，而且快速，直接使用 Java 编码的形式，而不需要了解虚拟机指令，就能动态改变类的结构，或者动态生成类。

- 粗略一看，可能不够形象，下面我们通过看 JavassistCompiler 如何使用来理解理解。
- [《Java学习之javassist》](http://www.cnblogs.com/sunfie/p/5154246.html)
- [《Javassist 字节码操作》](http://blog.csdn.net/qbg19881206/article/details/8993562)

com.alibaba.dubbo.common.compiler.support.JavassistCompiler ，实现 AbstractCompiler 抽象类，基于 Javassist 实现的 Compiler 。代码如下：

```plain text
plain 1: public class JavassistCompiler extends AbstractCompiler {   2:    3:     /**   4:      * 正则 - 匹配 import   5:      */   6:     private static final Pattern IMPORT_PATTERN = Pattern.compile("import\\s+([\\w\\.\\*]+);\n");   7:     /**   8:      * 正则 - 匹配 extends   9:      */  10:     private static final Pattern EXTENDS_PATTERN = Pattern.compile("\\s+extends\\s+([\\w\\.]+)[^\\{]*\\{\n");  11:     /**  12:      * 正则 - 匹配 implements  13:      */  14:     private static final Pattern IMPLEMENTS_PATTERN = Pattern.compile("\\s+implements\\s+([\\w\\.]+)\\s*\\{\n");  15:     /**  16:      * 正则 - 匹配方法  17:      */  18:     private static final Pattern METHODS_PATTERN = Pattern.compile("\n(private|public|protected)\\s+");  19:     /**  20:      * 正则 - 匹配变量  21:      */  22:     private static final Pattern FIELD_PATTERN = Pattern.compile("[^\n]+=[^\n]+;");  23:   24:     @Override  25:     public Class<?> doCompile(String name, String source) throws Throwable {  26:         // 获得类名  27:         int i = name.lastIndexOf('.');  28:         String className = i < 0 ? name : name.substring(i + 1);  29:         // 创建 ClassPool 对象  30:         ClassPool pool = new ClassPool(true);  31:         // 设置类搜索路径  32:         pool.appendClassPath(new LoaderClassPath(ClassHelper.getCallerClassLoader(getClass())));  33:         // 匹配 import  34:         Matcher matcher = IMPORT_PATTERN.matcher(source);  35:         List<String> importPackages = new ArrayList<String>(); // 引用的包名  36:         Map<String, String> fullNames = new HashMap<String, String>(); // 引用的类名  37:         while (matcher.find()) {  38:             String pkg = matcher.group(1);  39:             if (pkg.endsWith(".*")) { // 引用整个包下的类/接口  40:                 String pkgName = pkg.substring(0, pkg.length() - 2);  41:                 pool.importPackage(pkgName);  42:                 importPackages.add(pkgName);  43:             } else { // 引用指定类/接口  44:                 int pi = pkg.lastIndexOf('.');  45:                 if (pi > 0) {  46:                     String pkgName = pkg.substring(0, pi);  47:                     pool.importPackage(pkgName);  48:                     importPackages.add(pkgName);  49:                     fullNames.put(pkg.substring(pi + 1), pkg); // 类名  50:                 }  51:             }  52:         }  53:         String[] packages = importPackages.toArray(new String[0]);  54:         // 匹配 extends  55:         matcher = EXTENDS_PATTERN.matcher(source);  56:         CtClass cls;  57:         if (matcher.find()) {  58:             String extend = matcher.group(1).trim();  59:             String extendClass;  60:             if (extend.contains(".")) { // 内嵌的类，例如：extends A.B  61:                 extendClass = extend;  62:             } else if (fullNames.containsKey(extend)) { // 指定引用的类  63:                 extendClass = fullNames.get(extend);  64:             } else { // 引用整个包下的类  65:                 extendClass = ClassUtils.forName(packages, extend).getName();  66:             }  67:             // 创建 CtClass 对象  68:             cls = pool.makeClass(name, pool.get(extendClass));  69:         } else {  70:             // 创建 CtClass 对象  71:             cls = pool.makeClass(name);  72:         }  73:         // 匹配 implements  74:         matcher = IMPLEMENTS_PATTERN.matcher(source);  75:         if (matcher.find()) {  76:             String[] ifaces = matcher.group(1).trim().split("\\,");  77:             for (String iface : ifaces) {  78:                 iface = iface.trim();  79:                 String ifaceClass;  80:                 if (iface.contains(".")) { // 内嵌的接口，例如：extends A.B  81:                     ifaceClass = iface;  82:                 } else if (fullNames.containsKey(iface)) { // 指定引用的接口  83:                     ifaceClass = fullNames.get(iface);  84:                 } else { // 引用整个包下的接口  85:                     ifaceClass = ClassUtils.forName(packages, iface).getName();  86:                 }  87:                 // 添加接口  88:                 cls.addInterface(pool.get(ifaceClass));  89:             }  90:         }  91:         // 获得类中的内容，即首末 {} 的内容。  92:         String body = source.substring(source.indexOf("{") + 1, source.length() - 1);  93:         // 匹配 method 。使用分隔的方式，实际上，分隔出来的不仅仅有方法。  94:         String[] methods = METHODS_PATTERN.split(body);  95:         for (String method : methods) {  96:             method = method.trim();  97:             if (method.length() > 0) {  98:                 if (method.startsWith(className)) { // 构造方法  99:                     cls.addConstructor(CtNewConstructor.make("public " + method, cls)); 100:                 } else if (FIELD_PATTERN.matcher(method).matches()) { // 变量 101:                     cls.addField(CtField.make("private " + method, cls)); 102:                 } else { // 方法 103:                     cls.addMethod(CtNewMethod.make("public " + method, cls)); 104:                 } 105:             } 106:         } 107:         // 生成类 108:         // JavassistCompiler.class.getProtectionDomain() =》 设置保护域和 JavassistCompiler 一致，即 `#getClass()` 方法。深入见 《Java安全——安全管理器、访问控制器和类装载器》https://www.zybuluo.com/changedi/note/417132 109:         return cls.toClass(ClassHelper.getCallerClassLoader(getClass()), JavassistCompiler.class.getProtectionDomain()); 110:     } 111:  112: }
```

---

- 因为传入的是 Java 源代码
source
，需要通过正则匹配出
import
、
extends
、
implements
、方法、变量，传递给 Javassist API ，进行类生成。 如果胖友对 Javassist 的 API 不是很了解，可以看完整体逻辑，回看下上面提供的文档。挺有趣的。
- 第 27 至 28 行：获得类名。
- 第 30 行：创建 ClassPool 对象。**ClassPool**
是一个 CtClass 对象的 hash 表，类名做为 key 。ClassPool 的
#get(key)
搜索 hash 表找到与指定 key 关联的 CtClass 对象。如果没有找到 CtClass 对象，
#get(key)
读一个类文件构建新的 CtClass 对象，它是被记录在 hash 表中然后返回这个对象。
- 第 32 行：调用
ClassPool#appendClassPath(ClassPath)
方法，设置类搜索路径。
- 第 33 至 52 行：匹配
import
。
    - ClassPool#importPackage(packageName)
方法，引用包。
- 第 54 至 72 行：匹配
extends
。
    - ClassPool#makeClass(name, extendClass)**带继承的**
方法，创建
类。
    - ClassPool#makeClass(name)
方法，创建类。
- 第 74 至 90 行：匹配
implements
，整体逻辑和
extends
类似。
    - CtClass#addInterface(anInterface)
方法，添加类的接口。
- 第 92 行：获得类中的内容，即首末
{
}
中的内容体。
- 第 94 至 106 行：匹配方法和变量。使用
METHODS_PATTERN
分隔的方式。
    - CtClass#addConstructor(CtConstructor)
方法，添加类的构造方法。
    - CtClass#addMethod(CtMethod)
方法，添加类的方法。
    - CtClass#addField(CtField)
方法，添加类的属性。
- 第 109 行：调用
CtClass#toClass(ClassLoader, ProtectionDomain)
方法，生成类。

# 666. 彩蛋

![](/assets/images/learning/dubbo/dubbo-compiler-javassist/96ca62e95e06bbe2fa74153d2158bc13.png)

知识星球

今天状态略差。

推荐文章：[《Java-JDK代理、CGLIB、AspectJ代理分析比较》](http://xiezhaodong.me/2017/03/31/Java-JDK%E4%BB%A3%E7%90%86%E3%80%81CGLIB%E3%80%81AspectJ%E4%BB%A3%E7%90%86%E5%88%86%E6%9E%90%E6%AF%94%E8%BE%83/)
