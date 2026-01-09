---
layout: post
title: Spring Boot API 接口文档 JApiDocs 入门
slug: spring-boot-apidoc-japidocs-getting-started
type:
  - note
date: 2019-03-28
week: 2019-W21
status: draft
tags:
  - Spring Boot
author: deathwhispers
created: 2019-03-28 09:57
updated: 2019-03-28 09:57
---
![8b8ef94463c45fad1bbd047731f3b67d](/assets/images/learning/spring/springboot/spring-boot-apidoc-japidocs-getting-started/8b8ef94463c45fad1bbd047731f3b67d.png)

## 2.1 引入依赖

在 [pom.xml](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-24/lab-24-apidoc-japidocs/pom.xml) 文件中，引入 japidocs 的依赖。

io.github.yedaxia japidocs 1.4.4

## 2.2 创建 JApiDocs 配置

创建 [TestJApiDocs](https://github.com/YunaiV/SpringBoot-Labs/blob/master/lab-24/lab-24-apidoc-japidocs/src/main/java/cn/iocoder/springboot/lab24/TestJApiDocs.java) 类，作为 JApiDocs 的配置，生成接口文档。代码如下：

public class TestJApiDocs { public static void main(String[] args) { // 1. 创建生成文档的配置 DocsConfig config = new DocsConfig(); config.setProjectPath(“/Users/yunai/Java/SpringBoot-Labs/lab-24/lab-24-apidoc-japidocs”); // 项目所在目录 config.setDocsPath(“/Users/yunai/Downloads/”); // 生成 HTML 接口文档的目标目录 config.setAutoGenerate(true); // 是否给所有 Controller 生成接口文档 config.setProjectName(“示例项目”); // 项目名 config.setApiVersion(“V1.0”); // API 版本号 config.addPlugin(new MarkdownDocPlugin()); // 使用 MD 插件，额外生成 MD 格式的接口文档 // 2. 执行生成 HTML 接口文档 Docs.buildHtmlDocs(config); } }

稍后，我们执行 #main(…) 方法，就可以使用 JApiDocs 生成**接口文档**。

## 2.3 代码注释

JApiDocs 是通过解析 *Controller* 源码上的 **Java 注释**，所以我们需要在相关的**类**、**方法**、**属性**上，进行添加。示例代码如下图：

![](/assets/images/learning/spring/springboot/spring-boot-apidoc-japidocs-getting-started/12.png)

## 2.4 简单测试

示例项目搭建完成，我们来简单测试下。

① 执行 TestJApiDocs 类，生成 JApiDocs 接口文档。结果如下图所示：

![](/assets/images/learning/spring/springboot/spring-boot-apidoc-japidocs-getting-started/13.png)

② 点击 index.html 文件，查看 HTML 接口文档。如下图所示：

![](/assets/images/learning/spring/springboot/spring-boot-apidoc-japidocs-getting-started/fc4236f94c65ab07d0fb4b382494def4.png)

后续，我们可以部署到 Nginx 下，提供给前端小伙伴查看接口文档。

③ 点击 *-api-docs.md 文件，查看 Markdown 接口文档。如下图所示：

![](/assets/images/learning/spring/springboot/spring-boot-apidoc-japidocs-getting-started/8cee16f2e70c98dae97ca809d6b1436d.png)

# 3. 高级用法

本小节，我们来学习下 JApiDocs 的高级用法。

友情提示：在 99.99% 的场景下，不会使用到，所以胖友可以选择忽略不看。

如果使用到，请胖友直接去锤死狗芳。

JApiDocs 自定义了 @ApiDoc 和 @Ignore 注解，用于针对指定接口，进行自定义的配置。下面，我们来瞅一瞅哦。

良心艿：可能会有胖友说，JApiDocs 的注解不是和 Swagger 的注解一样，也对代码有入侵吗？确实是的，但是比 Swagger 的注解入侵性会低一些，并且基本不需要使用到。

## 3.1 @ApiDoc 注解

[@ApiDoc](https://github.com/YeDaxia/JApiDocs/blob/master/library/src/main/java/io/github/yedaxia/apidocs/ApiDoc.java) 注解，声明在**接口方法**上，通过它的四个属性，进行灵活配置。

- result 属性：直接声明**返回结果**的类型。如果你声明了，将会覆盖方法返回结果的类型。
- stringResult 属性：返回字符串。在**返回结果**比较简单，而不想创建一个专门的返回类，则可以考虑使用这个属性。友情提示：建议返回结果是否简单，还是创建一个对应的返回类，可维护性更好。
- url 属性：请求 **URL**。扩展字段，用于支持非 SpringMVC 的项目。友情提示：JApiDocs 提供了 [SpringControllerParser](https://github.com/YeDaxia/JApiDocs/blob/master/library/src/main/java/io/github/yedaxia/apidocs/parser/SpringControllerParser.java) 类，支持解析 SpringMVC 的注解。对于一些老项目，例如说使用 [Struts](https://www.oschina.net/p/struts) 框架，则需要通过 url 属性来声明。当然，更加推荐自定义一个针对 Struts 的 Parser 解析器，每个接口都手写，挺麻烦的。
- method 属性：请求 **Method**。扩展字段，用于支持非 SpringMVC 项目。

@ApiDoc 注解还有一个作用，声明该接口需要导出文档。不过因为一般我们会设置 DocsConfig 的 autoGenerate 属性为 true，默认导出所有 Controller 的接口文档，所以无需使用它。

具体的使用**示例**如下：

// 示例一 @ApiDoc(result = AdminVO.class, url = “/api/v1/admin/login2”, method = “post”) // 示例二：针对 `stringResult` 属性 @ApiDoc(stringResult = “{code: 0, data: ‘success’}”) @GetMapping(value = “custom-json”) public Map customJsonResult() {}

## 3.2 @Ignore 注解

[@Ignore](https://github.com/YeDaxia/JApiDocs/blob/master/library/src/main/java/io/github/yedaxia/apidocs/Ignore.java) 注解，比较好理解，实现**接口**或**字段**的忽略。

具体的使用**示例**如下：

// 示例一：声明在 Controller 类上，忽略该 Controller 的所有接口 @Ignore public class UserController {} // 示例二：声明在接口方法上，忽略该接口 @Ignore @PostMapping(“save”) public ApiResult saveUser() {} // 示例三：声明在接口使用到的对象的属性上，忽略该属性 public class UserCreateReqVO { @Ignore private Integer age; }

## 3.3 @description 注释

通过 @description 注释，主要有两种使用场景。

友情提示：由于 @description 注释不是 Java 注释中自带的标签，所以 IDEA 会存在黄色报警的情况，需要手动添加下，去除告警。

① 在 *Controller* 类上使用 @description 注释，将会作为该 *Controller* 在接口文档上的**导航标题**，而不会使用上面的注释内容。示例代码如下：

/** * 用户 Controller，提供用户基本信息的 CRUD 的功能 * * @description 用户 API */ @Controller public class UserController {}

② 在**接口方法**上使用 @description 注释，则可以在接口方法下面额外添加一行说明。示例代码如下：

/** * 获得用户列表 * * @param listReqVO 列表筛选条件 * @return 用户列表 * @description 不同的前端界面，可能有不同的查询诉求，通过该接口统一满足。 */ @GetMapping(“list”) public List list(UserListReqVO listReqVO){ return null; }

# 666. 彩蛋

至此，我们已经**“精通”** JApiDocs 的入门使用，通过在接口上添加 Java 注释，即可生成 HTTP API 的**接口文档**，非常的便捷。更多内容，胖友可以阅读[《JApiDocs 官方文档》](https://github.com/YeDaxia/JApiDocs/blob/master/docs/zh-cn/README.md)。

不过真正在团队中使用的话，艿艿还是会选择 Swagger，而不是 JApiDocs 作为接口文档的工具。主要有如下原因：

① JApiDocs 界面不提供**接口调试**功能，这个在日常开发中，还是非常高频使用的一个功能。

② JApiDocs 支持对接 [RAP](https://github.com/thx/RAP) 接口平台，不支持我们使用的 [YApi](https://github.com/YMFE/yapi) 接口平台，需要进行二次的[插件](https://github.com/YeDaxia/JApiDocs/blob/master/docs/zh-cn/README.md#%E6%B7%BB%E5%8A%A0%E6%9B%B4%E5%A4%9A%E5%8A%9F%E8%83%BD)开发。而 YApi 默认提供对 Swagger 的集成，可以直接采集接口信息。

良心艿：随着公司项目越来越多，我们会引入**接口平台**，提供统一的入口，查看所有项目的接口文档。

同时，接口平台往往提供接口的 **mock** 能力，可以更好的实现前后端的**并行开发**，提升开发效率和体验。

想要进一步了解的胖友，可以阅读[《芋道 Spring Boot API 接口文档 Swagger 入门》](http://www.iocoder.cn/Spring-Boot/Swagger/?self=)文章的[「4. 更强大的 YApi」](https://www.iocoder.cn/Spring-Boot/JApiDocs/?self=#)小节。

③ JApiDocs 是基于 **注释** 作为接口信息的数据来源，而 Java 注释的**定制化**能力是**弱**于 **注解** 的。

例如说，Swagger 的 @ApiImplicitParam 注解，可以使用 required 属性声明是否必填，使用 example 属性声明参数示例，这个在 Java 注释是非常难以实现的。

很多时候，我们会认为 Swagger 使用注解的**侵入性**很强，是因为在参数较多的接口方法上，会写一大片的 @ApiImplicitParam 注解，导致看起来会乱糟糟的。这个其实非常好解决，艿艿推荐对于复杂参数的接口，统一定义 [POJO](https://baike.baidu.com/item/POJO) 类。示例如下：

![](/assets/images/learning/spring/springboot/spring-boot-apidoc-japidocs-getting-started/bb4b334a11c1edc42f8ca8045e1e312e.png)