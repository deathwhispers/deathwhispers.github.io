---
layout: post
title: SPI机制在JDK与SpringBoot中的应用
author: deathwhispers
date: 2023-05-24
slug: spi-mechanism-in-jdk-and-springboot
categories:
- Java
tags:
- Java
type: note
status: draft
created: 2023-05-24 10:25
updated: 2023-05-24 10:25
week: 2025-W48
---

Spring Boot 不仅是简化 Spring 应用开发的工具，它还融合了许多先进的机制。本文深入探讨了 Spring Boot 中与 Java 的标准 SPI 相似的机制，揭示了它的工作原理、应用场景及与标准 SPI 的异同。文章通过实际代码示例为你展示了如何在 Spring Boot 中使用这一机制，并以形象的比喻帮助你理解其背后的思想。

## 1. SPI 解读：什么是 SPI?

SPI (Service Provider Interface) 是一种服务发现机制，它允许第三方提供者为核心库或主框架提供实现或扩展。这种设计允许核心库 / 框架在不修改自身代码的情况下，通过第三方实现来增强功能。

**JDK 原生的 SPI**：

- **定义和发现**
：
JDK
的
SPI
主要通过在
META-INF/services/
目录下放置特定的文件来指定哪些类实现了给定的服务接口。这些文件的名称应为接口的全限定名，内容为实现该接口的全限定类名。
- **加载机制**
：
ServiceLoader
类使用
Java
的类加载器机制从
META-INF/services/
目录下加载和实例化服务提供者。例如，
ServiceLoader.load(MyServiceInterface.class)
会返回一个实现了
MyServiceInterface
的实例迭代器。
- **缺点**
：
JDK
原生的
SPI
每次通过
ServiceLoader
加载时都会初始化一个新的实例，没有实现类的缓存，也没有考虑单例等高级功能。

**Spring 的 SPI**：

- **更加灵活**
：
Spring
的
SPI
不仅仅是服务发现，它提供了一套完整的插件机制。例如，可以为
Spring
定义新的
PropertySource
，
ApplicationContextInitializer
等。
- **与 IoC 集成**
：与
JDK
的
SPI
不同，
Spring
的
SPI
与其
IoC
(
Inversion of Control
) 容器集成，使得在
SPI
实现中可以利用
Spring
的全部功能，如依赖注入。
- **条件匹配**
：
Spring
提供了基于条件的匹配机制，这允许在某些条件下只加载特定的
SPI
实现，例如，可以基于当前运行环境的不同来选择加载哪个数据库驱动。
- **配置**
：
Spring
允许通过
spring.factories
文件在
META-INF
目录下进行配置，这与
JDK
的
SPI
很相似，但它提供了更多的功能和灵活性。

举个类比的例子：

想象我们正在建造一个电视机，SPI 就像电视机上的一个 USB 插口。这个插口可以插入各种设备（例如 U 盘、游戏手柄、电视棒等），但我们并不关心这些设备的内部工作方式。这样只需要提供一个标准的接口，其他公司（例如 U 盘制造商）可以为此接口提供实现。这样，电视机可以在不更改自己内部代码的情况下使用各种新设备，而设备制造商也可以为各种电视机制造兼容的设备。

总之，SPI 是一种将接口定义与实现分离的设计模式，它鼓励第三方为一个核心产品或框架提供插件或实现，从而使核心产品能够轻松地扩展功能。

## 2. SPI 在 JDK 中的应用示例

在 Java 的生态系统中，SPI 是一个核心概念，允许开发者提供扩展和替代的实现，而核心库或应用不必更改，下面举出一个例子来说明。

全部代码和步骤如下：

**步骤 1**：定义一个服务接口，文件名: MessageService.java

```java
package com.example.demo.service;

public interface MessageService {
    String getMessage();
}
```

**步骤 2**：为服务接口提供实现，这里会提供两个简单的实现类。

HelloMessageService.java

```java
package com.example.demo.service;

public class HelloMessageService implements MessageService {
    @Override
    public String getMessage() {
        return "Hello from HelloMessageService!";
    }
}
```

HiMessageService.java

```java
package com.example.demo.service;

public class HiMessageService implements MessageService {
    @Override
    public String getMessage() {
        return "Hi from HiMessageService!";
    }
}
```

这些实现就像不同品牌或型号的 U 盘或其他 USB 设备。每个设备都有自己的功能和特性，但都遵循相同的 USB 标准。

**步骤 3**：注册服务提供者

在资源目录（通常是 src/main/resources/）下创建一个名为 META-INF/services/ 的文件夹。在这个文件夹中，创建一个名为 com.example.demo.service.MessageService 的文件（这是我们**接口的全限定名**），这个文件没有任何文件扩展名，所以不要加上.txt 这样的后缀。文件的内容应为我们的两个实现类的全限定名，每个名字占一行：

```java
com.example.demo.service.HelloMessageService
com.example.demo.service.HiMessageService
```

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/f5bb50ebf675af1189675b70eb5fa5b1.png)

META-INF/services/ 是 Java SPI (Service Provider Interface) 机制中约定俗成的特定目录。它不是随意选择的，而是 SPI 规范中明确定义的。

因此，当使用 JDK 的 ServiceLoader 类来加载服务提供者时，它会特意去查找这个路径下的文件。

请确保文件的每一行只有一个名称，并且没有额外的空格或隐藏的字符，文件使用 UTF-8 编码。

**步骤 4**：使用 ServiceLoader 加载和使用服务

```java
package com.example.demo;

import com.example.demo.service.MessageService;
import java.util.ServiceLoader;

public class DemoApplication {
    public static void main(String[] args) {
        ServiceLoader<MessageService> loaders = ServiceLoader.load(MessageService.class);
        for (MessageService service : loaders) {
            System.out.println(service.getMessage());
        }
}
}

```

运行结果如下：

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/5e5817bf8e3c6f109a714fdf14dd6bf2.png)

这说明 ServiceLoader 成功地加载了我们为 MessageService 接口提供的两个实现，并且我们可以在不修改 Main 类的代码的情况下，通过添加更多的实现类和更新 META-INF/services/com.example.MessageService 文件来扩展我们的服务。

想象一下买了一台高端的智能电视，这台电视上有一个或多个 HDMI 端口，这就是它与外部设备连接的接口。

- **定义服务接口**
：这就像电视定义了
HDMI
端口的标准。在上面的代码中，
MessageService
接口就是这个“
HDMI
端口”，定义了如何与外部设备交流。
- **为服务接口提供实现**
：这类似于制造商为
HDMI
接口生产各种设备，如游戏机、蓝光播放器或流媒体棒。在代码中，
HelloMessageService
和
HiMessageService
就是这些 “
HDMI
设备”。每个设备/实现 都有其独特的输出，但都遵循了统一的
HDMI
标准（
MessageService
接口）。
- **注册服务提供者**
：当我们购买了一个
HDMI
设备，它通常都会在包装盒上明确标明 “适用于
HDMI
”。这就像一个标识，告诉用户它可以连接到任何带有
HDMI
接口的电视。在
SPI
的例子中，
META-INF/services/
目录和其中的文件就像这个 “标签”，告诉
JDK
哪些类是
MessageService
的实现。
- **使用 ServiceLoader 加载和使用服务**
：当插入一个
HDMI
设备到电视上，并切换到正确的输入频道，电视就会显示该设备的内容。类似地，在代码的这个步骤中，
ServiceLoader
就像电视的输入选择功能，能够发现和使用所有已连接的
HDMI
设备（即
MessageService
的所有实现）。

## 3. SPI 在 Spring 框架中的应用

Spring 官方在其文档和源代码中多次提到了 SPI（Service Provider Interface）的概念。但是，当我们说 “Spring 的 SPI” 时，通常指的是 Spring 框架为开发者提供的一套可扩展的接口和抽象类，开发者可以基于这些接口和抽象类实现自己的版本。

在 Spring 中，SPI 的概念与 Spring Boot 使用的 spring.factories 文件的机制不完全一样，但是它们都体现了可插拔、可扩展的思想。

**Spring 的 SPI**

- Spring
的核心框架提供了很多接口和抽象类，如
BeanPostProcessor
,
PropertySource
,
ApplicationContextInitializer
等，这些都可以看作是
Spring
的
SPI
。开发者可以实现这些接口来扩展
Spring
的功能。这些接口允许开发者在
Spring
容器的生命周期的不同阶段介入，实现自己的逻辑。

**Spring Boot 的 spring.factories 机制**

- spring.factories
是
Spring Boot
的一个特性，允许开发者自定义自动配置。通过
spring.factories
文件，开发者可以定义自己的自动配置类，这些类在
Spring Boot
启动时会被自动加载。
- 在这种情况下，
SpringFactoriesLoader
的使用，尤其是通过
spring.factories
文件来加载和实例化定义的类，可以看作是一种特定的
SPI
实现方式，但它特定于
Spring Boot
。

### 3.1 传统 Spring 框架中的 SPI 思想

在传统的 Spring 框架中，虽然没有直接使用名为 “SPI” 的术语，但其核心思想仍然存在。Spring 提供了多个扩展点，其中最具代表性的就是 BeanPostProcessor。在本节中，我们将通过一个简单的 MessageService 接口及其实现来探讨如何利用 Spring 的 BeanPostProcessor 扩展点体现 SPI 的思想。

提供两个简单的实现类。

HelloMessageService.java

```java
package com.example.demo.service;

public class HelloMessageService implements MessageService {
    @Override
    public String getMessage() {
        return "Hello from HelloMessageService!";
    }
}
```

HiMessageService.java

```java
package com.example.demo.service;

public class HiMessageService implements MessageService {
    @Override
    public String getMessage() {
        return "Hi from HiMessageService!";
    }
}
```

定义 BeanPostProcessor

```java
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;

public class MessageServicePostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        if (bean instanceof MessageService) {
            return new MessageService() {
                @Override
                public String getMessage() {
                    return ((MessageService) bean).getMessage() + " [Processed by Spring SPI]";
                }
        };
    }
return bean;
}

@Override
public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
    return bean;
}
}

```

修改 Spring 配置

将 MessageServicePostProcessor 添加到 Spring 配置中：

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MessageServiceConfig {
    @Bean
    public MessageService helloMessageService() {
        return new HelloMessageService();
    }

@Bean
public MessageService hiMessageService() {
    return new HiMessageService();
}

@Bean
public MessageServicePostProcessor messageServicePostProcessor() {
    return new MessageServicePostProcessor();
}
}

```

执行程序

使用之前提供的 DemoApplication 示例类：

```java
package com.example.demo;

import com.example.demo.configuration.MessageServiceConfig;
import com.example.demo.service.MessageService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class DemoApplication {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(MessageServiceConfig.class);
        MessageService helloMessageService = context.getBean("helloMessageService", MessageService.class);
        MessageService hiMessageService = context.getBean("hiMessageService", MessageService.class);
        System.out.println(helloMessageService.getMessage());
        System.out.println(hiMessageService.getMessage());
    }
}
```

运行结果：

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/f9eb1ec3cd179454a6e567557aa13037.png)

现在，每一个 MessageService 实现都被 BeanPostProcessor 处理了，添加了额外的消息 “[Processed by Spring SPI]”。这演示了 Spring 的 SPI 概念，通过 BeanPostProcessor 来扩展或修改 Spring 容器中的 bean。

有人可能留意到这里红色的警告，这个之前在讲 BeanPostProcessor 的时候也提到过，当 BeanPostProcessor 自身被一个或多个 BeanPostProcessor 处理时，就会出现这种情况。简单地说，由于 BeanPostProcessor 需要在其他 bean 之前初始化，所以某些 BeanPostProcessor 无法处理早期初始化的 bean，包括配置类和其他 BeanPostProcessor。解决办法就是不要把 MessageServicePostProcessor 放在配置类初始化，在配置类删掉，再把 MessageServicePostProcessor 加上 @Component 注解。

类比文章开头的电视机的例子：

- **电视机与 USB 插口: 在这个新的示例中，电视机仍然是核心的 Spring 应用程序，具体来说是 DemoApplication 类。这个核心应用程序需要从某个服务（即 MessageService）获取并打印一条消息。**
- **USB 插口: 与之前一样，MessageService 接口就是这个 “***USB*** 插口”。它为电视机提供了一个标准化的接口，即 getMessage() 方法，但没有规定具体怎么实现。**
- **设备制造商与他们的产品: 在这里，我们有两种设备制造商或第三方提供者：HelloMessageService 和 HiMessageService。它们为 “***USB*** 插口”（即 MessageService 接口）提供了不同的设备或实现。一个显示 “Hello from HelloMessageService!”，另一个显示 “Hi from HiMessageService!”。**
- **BeanPostProcessor: 这是一个特殊的 “魔法盒子”，可以将其视为一个能够拦截并修改电视机显示内容的智能设备。当插入 USB 设备（即 MessageService 的实现）并尝试从中获取消息时，这个 “魔法盒子” 会介入，并为每条消息添加 “[Processed by Spring SPI]”。**
- **Spring 上下文配置: 这依然是电视机的使用说明书，但现在是使用了基于 Java 的配置方式，即 MessageServiceConfig 类。这个 “使用说明书” 指导 Spring 容器如何创建并管理 MessageService 的实例，并且还指导它如何使用 “魔法盒子”（即 MessageServicePostProcessor）来处理消息。**

总的来说，与之前的例子相比，这个新示例提供了一个更加动态的场景，其中 Spring 的 BeanPostProcessor 扩展点允许我们拦截并修改 bean 的行为，就像一个能够干预并改变电视机显示内容的智能设备。

### 3.2 Spring Boot 中的 SPI 思想

Spring Boot 有一个与 SPI 相似的机制，但它并不完全等同于 Java 的标准 SPI。

Spring Boot 的自动配置机制主要依赖于 spring.factories 文件。这个文件可以在多个 jar 中存在，并且 Spring Boot 会加载所有可见的 spring.factories 文件。我们可以在这个文件中声明一系列的自动配置类，这样当满足某些条件时，这些配置类会自动被 Spring Boot 应用。

接下来会展示 Spring SPI 思想的好例子，但是它与 Spring Boot 紧密相关。

定义接口

```java
package com.example.demo.service;

public interface MessageService {
    String getMessage();
}
```

这里会提供两个简单的实现类。

HelloMessageService.java

```java
package com.example.demo.service;

public class HelloMessageService implements MessageService {
    @Override
    public String getMessage() {
        return "Hello from HelloMessageService!";
    }
}
```

HiMessageService.java

```java
package com.example.demo.service;

public class HiMessageService implements MessageService {
    @Override
    public String getMessage() {
        return "Hi from HiMessageService!";
    }
}
```

注册服务

在 resources/META-INF 下创建一个文件名为 spring.factories。这个文件里，可以注册 MessageService 实现类。

```java
com.example.demo.service.MessageService=com.example.demo.service.HelloMessageService,com.example.demo.service.HiMessageService
```

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/7bd4c0e1419d065e398e92dba8c106e4.png)

注意这里 com.example.demo.service.MessageService 是接口的全路径，而 com.example.demo.service.HelloMessageService,com.example.demo.service.HiMessageService 是实现类的全路径。如果有多个实现类，它们应当用逗号分隔。

spring.factories 文件中的条目键和值之间不能有换行，即 key=value 形式的结构必须在同一行开始。但是，如果有多个值需要列出（如多个实现类），并且这些值是逗号分隔的，那么可以使用反斜杠（““）来换行。spring.factories 的名称是约定俗成的。如果试图使用一个不同的文件名，那么 Spring Boot 的自动配置机制将不会识别它。

这里 spring.factories 又可以写为

```plain text
com.example.demo.service.MessageService=com.example.demo.service.HelloMessageService,\
com.example.demo.service.HiMessageService
```

直接在逗号后面回车 IDEA 会自动补全反斜杠，保证键和值之间不能有换行即可。

使用 SpringFactoriesLoader 来加载服务

```java
package com.example.demo;

import com.example.demo.service.MessageService;
import org.springframework.core.io.support.SpringFactoriesLoader;
import java.util.List;

public class DemoApplication {
    public static void main(String[] args) {
        List<MessageService> services = SpringFactoriesLoader.loadFactories(MessageService.class, null);
        for (MessageService service : services) {
            System.out.println(service.getMessage());
        }
}
}

```

SpringFactoriesLoader.loadFactories 的第二个参数是类加载器，此处我们使用默认的类加载器，所以传递 null。

运行结果：

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/2ebeefc24a93904f8edc27d151a0ae68.png)

这种方式利用了 Spring 的 SpringFactoriesLoader，它允许开发者提供接口的多种实现，并通过 spring.factories 文件来注册它们。这与 JDK 的 SPI 思想非常相似，只是在实现细节上有所不同。这也是 Spring Boot 如何自动配置的基础，它会查找各种 spring.factories 文件，根据其中定义的类来初始化和配置 bean。

我们继续使用电视机的例子来解释：

- **电视机: 这是我们的 Spring 应用，就像 DemoApplication。电视机是查看不同信号源或通道的设备，我们的应用程序是为了运行并使用不同的服务实现。**
- **USB 插口: 这代表我们的 MessageService 接口。USB 插口是一个标准的接口，它允许连接各种设备，就像 MessageService 接口允许有多种实现方式。**
- ***USB 设备（如 U 盘或移动硬盘）**: 这代表我们的服务实现，例如 HelloMessageService 和 HiMessageService。每个 USB 设备在插入电视机后都有特定的内容或功能，这就像我们的每个服务实现返回不同的消息。**
- **电视机的 USB 设备目录: 这是 spring.factories 文件。当我们将 USB 设备插入电视机时，电视机会检查设备的信息或内容，spring.factories 文件告诉 Spring Boot 哪些服务实现是可用的，就像电视机知道有哪些 USB 设备被插入。**
- **电视机的 USB 扫描功能: 这就是 SpringFactoriesLoader。当我们要从电视机上查看 USB 内容时，电视机会扫描并显示内容。同样，当 DemoApplication 运行时，SpringFactoriesLoader 会查找并加载在 spring.factories 文件中列出的服务实现。**

简化解释:

- 当插入
USB
设备到电视机，期望电视机能够识别并显示该设备的内容。
- 在我们的例子中，
USB
设备的内容就是从
MessageService
实现类返回的消息。
- spring.factories
文件就像电视机的内置目录，告诉电视机哪些
USB
设备是已知的和可以使用的。
- 当我们的
DemoApplication
（电视机）运行时，它使用
SpringFactoriesLoader
（
USB
扫描功能）来检查哪些服务（
USB
设备）是可用的，并输出相应的消息（显示
USB
内容）。

总结：在这个 Spring Boot 的 SPI 例子中，我们展示了核心 Spring 应用如何自动地识别和使用 spring.factories 文件中注册的实现，这与电视机自动地识别和使用所有插入的 USB 设备有相似之处。

## 4. SPI 在 JDBC 驱动加载中的应用

数据库驱动的 SPI 主要体现在 JDBC 驱动的自动发现机制中。JDBC 4.0 引入了一个特性，允许驱动自动注册到 DriverManager。这是通过使用 Java 的 SPI 来实现的。驱动 jar 包内会有一个 META-INF/services/java.sql.Driver 文件，此文件中包含了该驱动的 Driver 实现类的全类名。这样，当类路径中有 JDBC 驱动的 jar 文件时，Java 应用程序可以自动发现并加载 JDBC 驱动，而无需明确地加载驱动类。

这意味着任何数据库供应商都可以编写其自己的 JDBC 驱动程序，只要它遵循 JDBC 驱动程序的 SPI，它就可以被任何使用 JDBC 的 Java 应用程序所使用。

当我们使用 DriverManager.getConnection() 获取数据库连接时，背后正是利用 SPI 机制加载合适的驱动程序。

以下是 SPI 机制的具体工作方式：

**定义服务接口**：

在这里，接口已经由 Java 平台定义，即 java.sql.Driver。

**为接口提供实现**：

各大数据库厂商（如 Oracle, MySQL, PostgreSQL 等）为其数据库提供了 JDBC 驱动程序，它们都实现了 java.sql.Driver 接口。例如，MySQL 的驱动程序中有一个类似于以下的类：

```java
public class com.mysql.cj.jdbc.Driver implements java.sql.Driver {
    // 实现接口方法...
}
```

直接上图：

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/77c4ac898a3c441fa128a7a0cab34a64.png)

**注册服务提供者**：

对于 MySQL 的驱动程序，可以在其 JAR 文件的 META-INF/services 目录下找到一个名为 java.sql.Driver 的文件，文件内容如下：

```java
com.mysql.cj.jdbc.Driver
```

直接上图：

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/2a8fcfdfb8be4569fcb0025fd958aa14.png)

看到这里是不是发现和第 2 节举的 JDK SPI 的例子一样？体会一下。

**使用 SPI 来加载和使用服务**：

当我们调用 DriverManager.getConnection(jdbcUrl, username, password) 时，DriverManager 会使用 ServiceLoader 来查找所有已注册的 java.sql.Driver 实现。然后，它会尝试每一个驱动程序，直到找到一个可以处理给定 jdbcUrl 的驱动程序。

以下是一个简单的示例，展示如何使用 JDBC SPI 获取数据库连接：

```java
import java.sql.Connection;
import java.sql.DriverManager;

public class JdbcExample {
    public static void main(String[] args) {
        String jdbcUrl = "jdbc:mysql://localhost:3306/mydatabase";
        String username = "root";
        String password = "password";
        try {
            Connection connection = DriverManager.getConnection(jdbcUrl, username, password);
            System.out.println("Connected to the database!");
            connection.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
}
}

```

在上述代码中，我们没有明确指定使用哪个 JDBC 驱动程序，因为 DriverManager 会自动为我们选择合适的驱动程序。

这种模块化和插件化的机制使得我们可以轻松地为不同的数据库切换驱动程序，只需要更改 JDBC URL 并确保相应的驱动程序 JAR 在类路径上即可。

在 Spring Boot 中，开发者通常不会直接与 JDBC 的 SPI 机制交互来获取数据库连接。Spring Boot 的自动配置机制隐藏了许多底层细节，使得配置和使用数据库变得更加简单。

一般会在 application.properties 或 application.yml 中配置数据库连接信息。

例如：

```plain text
spring.datasource.url=jdbc:mysql://localhost:3306/mydatabase
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
```

在上述步骤中，Spring Boot 的自动配置机制会根据提供的依赖和配置信息来初始化和配置 DataSource 对象，这个对象管理数据库连接。实际上，添加 JDBC 驱动依赖时，Spring Boot 会使用 JDK 的 SPI 机制（在 JDBC 规范中应用）来找到并加载相应的数据库驱动。开发者虽然不直接与 JDK 的 SPI 交互，但在背后 Spring Boot 确实利用了 JDK SPI 机制来获取数据库连接。

## 5. 如何通过 Spring Boot 自动配置理解 SPI 思想

这种机制有点类似于 Java 的 SPI，因为它允许第三方库提供一些默认的配置。但它比 Java 的 SPI 更为强大和灵活，因为 Spring Boot 提供了大量的注解（如 @ConditionalOnClass、@ConditionalOnProperty、@ConditionalOnMissingBean 等）来控制自动配置类是否应该被加载和应用。

总的来说，Spring Boot 的 spring.factories 机制和 Java 的 SPI 在概念上是相似的，但它们在实现细节和用途上有所不同。

让我们创建一个简化的实际例子，假设我们要为不同的消息服务（如 SMS 和 Email）创建自动配置。

**MessageService 接口**：

```java
package com.example.demo.service;

public interface MessageService {
    void send(String message);
}
```

**SMS 服务实现**：

```java
package com.example.demo.service.impl;

import com.example.demo.service.MessageService;

public class SmsService implements MessageService {
    @Override
    public void send(String message) {
        System.out.println("Sending SMS: " + message);
    }
}
```

**Email 服务实现**：

```java
package com.example.demo.service.impl;

import com.example.demo.service.MessageService;

public class EmailService implements MessageService {
    @Override
    public void send(String message) {
        System.out.println("Sending Email: " + message);
    }
}
```

**自动配置类**：

```java
package com.example.demo.configuration;

import com.example.demo.service.EmailService;
import com.example.demo.service.MessageService;
import com.example.demo.service.SmsService;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MessageAutoConfiguration {
    @Bean
    @ConditionalOnProperty(name = "message.type", havingValue = "sms")
    public MessageService smsService() {
        return new SmsService();
    }

@Bean
@ConditionalOnProperty(name = "message.type", havingValue = "email")
public MessageService emailService() {
    return new EmailService();
}
}

```

这个类提供两个条件性的 beans（组件），分别是 SmsService 和 EmailService。这些 beans 的创建取决于 application.properties 文件中特定的属性值。

- **@ConditionalOnProperty(name = “message.type”, havingValue = “sms”)**

当 application.properties 或 application.yml 中定义的属性 message.type 的值为 sms 时，此条件为 true。此时，smsService() 方法将被调用，从而创建一个 SmsService 的 bean。

- **@ConditionalOnProperty(name = “message.type”, havingValue = “email”)**

当 application.properties 或 application.yml 中定义的属性 message.type 的值为 email 时，此条件为 true。此时，emailService() 方法将被调用，从而创建一个 EmailService 的 bean。

**spring.factories 文件**：

在 src/main/resources/META-INF 目录下创建一个 spring.factories 文件，内容如下：

```plain text
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
com.example.demo.configuration.MessageAutoConfiguration
```

**application.properties 文件**：

```plain text
message.type=sms
```

**MessageTester 组件**：

```java
package com.example.demo;

import com.example.demo.service.MessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import javax.annotation.PostConstruct;

@Component
public class MessageTester {
    @Autowired
    private MessageService messageService;

    @PostConstruct
    public void init() {
        messageService.send("Hello World");
    }
}
```

**DemoApplication 主程序**：

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

运行结果：

![](/assets/images/learning/java/spi-mechanism-in-jdk-and-springboot/16fa9a9c6c9a2256c49505ebcc4c563f.png)

在上述例子中，我们创建了一个 MessageService 接口和两个实现（SmsService 和 EmailService）。然后，我们创建了一个自动配置类，其中包含两个 bean 定义，这两个 bean 定义分别基于 application.properties 中的属性值条件性地创建。在 spring.factories 文件中，我们声明了这个自动配置类，以便 Spring Boot 在启动时能够自动加载它。

在此，继续用电视机的例子升华理解下

**电视机类比**

**总体概念：**

- 假设电视机（
TV
）是一个
Java
应用。
- 电视机的各种插槽，如
HDMI
、
USB
、
VGA
等，可以视为应用中的
SPI
接口。
- 插入这些插槽的设备（如
DVD
播放器、游戏机、
USB
驱动器等）可以视为
SPI
的实现。

**Java 的 SPI：**

- 当我们购买电视机时，不知道将会连接哪种设备，可能是
DVD
播放器，也可能是游戏机。
- 但是，只要这些设备遵循了插槽的标准（例如，
HDMI
标准），就可以将其插入电视机并使其工作。
- 这就像
Java
的
SPI
机制：为了能让多个供应商提供实现，
Java
定义了一个接口，供应商提供具体的实现。

**Spring Boot 的自动配置**：

- 现在，想象一下现代的智能电视。当插入一个设备，电视机不仅可以识别它，还可能根据所连接的设备类型自动调整设置，例如选择正确的输入源、优化图像质量等。
- 这就像
Spring Boot
的自动配置：当
Spring Boot
应用启动时，它会检查
classpath
上的库，并根据存在的库自动配置应用。
- 电视机的自动设置可以类比为
Spring Boot
中的
spring.factories
和各种
@Conditional
… 注解。它们决定在什么条件下进行哪种配置。

**扩展性**：

- 如果电视制造商想为新型的插槽或连接技术开发电视，它可以很容易地在其电视机型中添加新的插槽。
- 同样地，使用
Spring Boot
，如果要为应用添加新功能或库，只需添加相关的依赖，然后
Spring Boot
会自动识别并配置这些新功能。

通过这种类比，电视机的插槽和自动设置功能为我们提供了一个直观的方式来理解 Java 的 SPI 机制和 Spring Boot 的自动配置如何工作，以及它们如何为应用开发者提供便利。

## 6. SPI（Service Provider Interface）总结

SPI，即服务提供者接口，是一种特定的设计模式。它允许框架或核心库为第三方开发者提供一个预定义的接口，从而使他们能够为框架提供自定义的实现或扩展。

**核心目标**:

- 解耦：
SPI
机制让框架的核心与其扩展部分保持解耦，使核心代码不依赖于具体的实现。
- 动态加载：系统能够通过特定的机制（如
Java
的
ServiceLoader
）动态地发现和加载所需的实现。
- 灵活性：框架用户可以根据自己的需求选择、更换或增加新的实现，而无需修改核心代码。
- 可插拔：第三方提供的服务或实现可以轻松地添加到或从系统中移除，无需更改现有的代码结构。

**价值**:

- 为框架或库的用户提供更多的自定义选项和灵活性。
- 允许框架的核心部分保持稳定，同时能够容纳新的功能和扩展。

**SPI 与 “开闭原则”**：

“开闭原则” 提倡软件实体应该对扩展开放，但对修改封闭。即在不改变现有代码的前提下，通过扩展来增加新的功能。

**SPI 如何体现 “开闭原则”**:

- 对扩展开放：
SPI
提供了一种标准化的方式，使第三方开发者可以为现有系统提供新的实现或功能。
- 对修改封闭：添加新的功能或特性时，原始框架或库的代码不需要进行修改。
- 独立发展：框架与其
SPI
实现可以独立地进化和发展，互不影响。

总之，SPI 是一种使软件框架或库更加模块化、可扩展和可维护的有效方法。通过遵循 “开闭原则”，SPI 确保了系统的稳定性和灵活性，从而满足了不断变化的业务需求。
