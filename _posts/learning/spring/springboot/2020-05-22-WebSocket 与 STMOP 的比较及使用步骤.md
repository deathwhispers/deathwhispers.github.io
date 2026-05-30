---
layout: post
title: WebSocket 与 STMOP 的比较及使用步骤
author: deathwhispers
date: 2020-05-22
slug: websocket-stmop-comparison-and-usage-steps
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2025-01-09 11:46
updated: 2025-03-12 18:41
---

# **前言**

介绍了websocket与STMOP以及SockJs使用代码，基本上拿来即可使用。也介绍了2者的区别及个人推荐使用websocket方式。

websocket在Html5里使用，主要目标还是解决服务器能主动向客户端发送消息的功能。也就是全双工的通信方式。

Spring提供了对Websocket的支持，WebSocket API是比较低级的API,但恰恰是我比较中意的方式。因为接近底层，能控制的逻辑比较多。

[文章源码](https://gitee.com/chenyuan122912/gs-messaging-stomp-websocket-master.git)

源码是"webSocket+sockJs+STOMP 包括spring-websocket官方源码(STOMP方式)和自己实现的源码(webSocket)"。

WebSocket 是底层协议，SockJS 是WebSocket 的备选方案，也是底层协议，而 STOMP 是基于 WebSocket（SockJS） 的上层协议。

我个人更喜欢使用WebSocket 是底层协议。，WebSocket将发送的对象相对比较集中，对代码的侵入比较少，而STOMP会有大量的@SendTo侵入式编程。

# **WebSocket和Socket结合一起使用**

下面的SockJs和STMOP引入同样的依赖即可

## **引入依赖**

gradle

```groovy
dependencies {
    compile("org.springframework.boot:spring-boot-starter-websocket")
    compile("org.webjars:stomp-websocket:2.3.3")
}
```

maven

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-websocket</artifactId>
    </dependency>
    <dependency>
        <groupId>org.webjars</groupId>
        <artifactId>stomp-websocket</artifactId>
        <version>2.3.3</version>
    </dependency>
</dependencies>
```

## **java-config配置**

拿来即可。

WebSockt使用起来比较简单，只要配置handler处理数据逻辑，Config接收数据，拦截器处理前置或后置情况下逻辑即可。配置前端。

```java

```

注册配置表，其实不难，拿来即用。有一个端点路径，是客户端连接地址。相当于统一入口，在接收或分发消息时，使用拦截器增加了前置和后置处理程序，同时真正的业务逻辑交给handler处理。

## **处理器handler**

处理器ChatWebSocketHandler.java，继承TextWebSocketHandler类,使TextMessage，BinaryMessage，PongMessage

```java
package webSocketSockJs;

import org.springframework.stereotype.Service;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class MyHandler extends TextWebSocketHandler {
    // 在线用户列表
    private static final Map<Integer, WebSocketSession> users;
    // 用户标识
    private static final String CLIENT_ID = "clientId";

    static {
        users = new HashMap<>();
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        System.out.println("成功建立连接");
        Integer userId = getClientId(session);
        System.out.println(userId);
        if (userId != null) {
            users.put(userId, session);
            session.sendMessage(new TextMessage("成功建立socket连接"));
            System.out.println(userId);
            System.out.println(session);
        }
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) {
        System.out.println(message.getPayload());
        WebSocketMessage message1 = new TextMessage("hi " + message.getPayload());
        try {
            session.sendMessage(message1);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
    * 发送信息给指定用户
    *
    * @param clientId
    * @param message
    * @return
    */
    public boolean sendMessageToUser(Integer clientId, TextMessage message) {
        if (users.get(clientId) == null) return false;
        WebSocketSession session = users.get(clientId);
        System.out.println("sendMessage:" + session);
        if (!session.isOpen()) return false;
        try {
            session.sendMessage(message);
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    /**
    * 广播信息
    *
    * @param message
    * @return
    */
    public boolean sendMessageToAllUsers(TextMessage message) {
        boolean allSendSuccess = true;
        Set<Integer> clientIds = users.keySet();
        WebSocketSession session = null;
        for (Integer clientId : clientIds) {
            try {
                session = users.get(clientId);
                if (session.isOpen()) {
                    session.sendMessage(message);
                }
            } catch (IOException e) {
                e.printStackTrace();
                allSendSuccess = false;
            }
        }
        return allSendSuccess;
    }

    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
        if (session.isOpen()) {
            session.close();
        }
        System.out.println("连接出错");
        users.remove(getClientId(session));
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        System.out.println("连接已关闭：" + status);
        users.remove(getClientId(session));
    }

    @Override
    public boolean supportsPartialMessages() {
        return false;
    }

    /**
    * 获取用户标识
    *
    * @param session
    * @return
    */
    private Integer getClientId(WebSocketSession session) {
        try {
            Integer clientId = Integer.valueOf(String.valueOf(session.getAttributes().get(CLIENT_ID)));
            return clientId;
        } catch (Exception e) {
            return null;
        }
    }
}



```

对每个函数功能不作解释，有二点要注意

我们也可以通过H5在new WebSocket(url)中，在url传入标识参数，比如ws:hocalhost:8080/webSocketIMServer?userId=用户id值。在handler里拿到数据。

在TextWebSocketHandler类里有handleMessage方法，如下

```java
@Override
public void handleMessage(WebSocketSession session, WebSocketMessage<?> message) throws Exception {
    if(message instanceof TextMessage) {
        handleTextMessage(session, (TextMessage) message);
    } else if(message instanceof BinaryMessage) {
        handleBinaryMessage(session, (BinaryMessage) message);
    } else if(message instanceof PongMessage) {
        handlePongMessage(session, (PongMessage) message);
    } else {
        throw new IllegalStateException("Unexpected WebSocket message type: " + message);
    }
}


```

可以处理3种类型数据。支持TextMessage，BinaryMessage，PongMessage。实现不同方法即可。

## **拦截器Interceptor**

WebSocketInterceptor.java

```java
package webSocketSockJs;

import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.http.server.ServletServerHttpRequest;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.HandshakeInterceptor;

import javax.servlet.http.HttpSession;
import java.util.Map;

public class WebSocketInterceptor implements HandshakeInterceptor {
    // handler处理前调用,attributes属性最终在WebSocketSession里,可能通过webSocketSession.getAttributes().get(key值)获得
    @Override
    public boolean beforeHandshake(ServerHttpRequest request, ServerHttpResponse response,
    WebSocketHandler wsHandler, Map<String, Object> attributes) throws Exception {
        if(request instanceof ServletServerHttpRequest) {
            ServletServerHttpRequest serverHttpRequest = (ServletServerHttpRequest) request;
            Object clientId = serverHttpRequest.getServletRequest().getParameter("clientId");
            System.out.println(clientId);
            attributes.put("clientId", clientId);
        }
        return true;
    }

    // handler处理后调用
    @Override
    public void afterHandshake(ServerHttpRequest serverHttpRequest, ServerHttpResponse serverHttpResponse, WebSocketHandler webSocketHandler, Exception e) {
    }
}



```

attributes属性最终在WebSocketSession里,可能通过webSocketSession.getAttributes().get(key值)获得。

## **SockJs是什么**

一些浏览器中缺少对WebSocket的支持，SocketJS是一种备选解决方案。SockJS优先使用原生WebSocket，如果在不支持websocket的浏览器中，会自动降级为轮询的方式。 它在浏览器和web服务器之间创建了一个低延迟、全双工、跨域通信通道。

SockJS所处理的URL是"http://"或"https://"模式，而不是"ws://"和"wss://"

服务器通过withSockJS()方法来使用SockJS作为备用方法

## **客户端实现，SockJS与WebSocket一起使用**

前端引入SockJS模块。

```javascript
// 建立连接
function connect() {
    var host = window.location.host;
    if ('WebSocket' in window) {
        websocket = new WebSocket("ws://" + host + "/webSocketIMServer?clientId=6");
    } else if ('MozWebSocket' in window) {
        websocket = new MozWebSocket("ws://" + host + "/webSocketIMServer?clientId=6");
    } else {
        websocket = new SockJS("http://" + host + "/sockjs/webSocketIMServer?clientId=6");
    }
    websocket.onopen = function(evnt) {
        console.log("websocket连接上");
        setConnected(true);
    };
    websocket.onmessage = function(evnt) {
        console.log("接收到的消息：" + evnt.data);
        showGreeting(evnt.data);
    };
    websocket.onerror = function(evnt) {
        console.log("websocket错误");
    };
    websocket.onclose = function(evnt) {
        console.log("websocket关闭");
    }
}
// 向服务器发送消息
function sendName() {
    websocket.send(JSON.stringify({'name': $("#name").val()}));
}
```

上面判断浏览器支持WebSocket则使用原生WebSocket，否则使用SockJS，SockJS所处理的URL是"http://"或"https://"模式，而不是"ws://"和"wss://"。上面客户端代码拿来即用。

上面源码在git上。前言里有地址。

## **总结客户端与服务端交互方式**

建议连接后

- 客户端向服务端发送消息：websocket.send(JSON.stringify({'name': $("#name").val()}));，数据最终进入handler里的handleTextMessage(WebSocketSession session, TextMessage message)方法里。
- 服务端向客户端发送消息。

任意类里使用

```java
@Autowired
MyHandler handler;

// 调用方法，发送消息
boolean hasSend = handler.sendMessageToUser(6, new TextMessage("发送一条小xi"));
```

# **STMOP协议**

spring-web-socket官网上的源码为例

[源码](https://github.com/spring-guides/gs-messaging-stomp-websocket.git).

[英文文档](http://spring.io/guides/gs/messaging-stomp-websocket/)

官网使用的是STMOP协议。

WebSocketConfig类，继承WebSocketMessageBrokerConfigurer

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic6");
        config.setApplicationDestinationPrefixes("/app");
        // 点对点使用的订阅前缀（客户端订阅路径上会体现出来），不设置的话，默认也是/user/
        // registry.setUserDestinationPrefix("/user/");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/gs-guide-websocket")
        .setAllowedOrigins("*")
        .withSockJS();
    }
}



```

登录后复制

@Configuration注解用于定义配置类，使用java-config方式配置。@EnableWebSocketMessageBroker用于开启STMOP。

基本上继承WebSocketMessageBrokerConfigurer类即可，也可以继承AbstractWebSocketMessageBrokerConfigurer，它是WebSocketMessageBrokerConfigurer接口的空实现类。

enableSimpleBroker这个方法用于配置主题，内容可以任意写，支持可变参数。可以把它理解为不同的业务定义不同的主题，每个主题下有多个子主题。这里的/topic6是随意写的。

setApplicationDestinationPrefixes方法定义了请求的前缀是/app，可被controller拦截，能进入controller层，否则不能进入controller层。

addEndpoint定义了端点，可以理解为客户端连接地址，连接成功即可使用webSocket的API,setAllowedOrigins("*")定义了可以跨域，可以限制域名，比如 .setAllowedOrigins({"http://www.localhost.com"})，withSockJS()方法定义了支持SockJS连接，优先使用原生的WebSockt，如果浏览器不支持，则降级使用SockJs。

Greeting.java和HelloMessage.java是2个纯java类，没啥介绍的。

## **控制层**

GreetingController.java

```java
package hello;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.simp.annotation.SubscribeMapping;
import org.springframework.stereotype.Controller;
import org.springframework.web.util.HtmlUtils;

@Controller
public class GreetingController {
    private Logger logger = LoggerFactory.getLogger(this.getClass());

    @MessageMapping("/hello")
    @SendTo("/topic6/greetings")
    public Greeting greeting(HelloMessage message) throws Exception {
        Thread.sleep(1000); // simulated delay
        return new Greeting("Hello, " + HtmlUtils.htmlEscape(message.getName()) + "!");
    }

    @SubscribeMapping("/topic6/greetings")
    @SendTo("/topic6/greetings")
    public Greeting sub() {
        logger.info("XXX用户订阅了我。。。");
        return new Greeting("感谢你订阅了我。。。");
    }
}



```

@MessageMapping是接收客户端发送的消息映射，看名字也知道。由于上面定义了controll层拦截请求的前缀，所以请求/app/hello才能进入controller层。

@SendTo("/topic6/greetings")定义了向哪个主题发送消息。如果不定义，/app/hello不会向任意主题发送消息，同时该接口也不会返回任意数据。/app/hello接口的目的是接收消息，同时广播或定向发送给其它用户。

我添加了@SubscribeMapping注解的方法，它是拦截订阅请求的，其实它的作用并不大，它也是必需接收/app/topic6/greetings形势接口(注意有/app前缀)，如果该注解下面没有@SendTo，则会向订阅了/app/topic6/greetings主题的用户发送消息。如果指定了@SendTo，则使用它。

网上一图很方便于理解

这些配置已经完整的构成的使用STMOP协议的服务器了，只需要修改主题名，controller即可。

下面的重点是客户端。

```javascript
// 建议连接
function connect() {
    var socket = new SockJS('/gs-guide-websocket');
    stompClient = Stomp.over(socket);
    stompClient.connect({}, function(frame) {
        setConnected(true);
        console.log('Connected: ' + frame);
        stompClient.subscribe('/topic6/greetings', function(greeting) {
            showGreeting(JSON.parse(greeting.body).content);
        });
    });
}
// 发送消息
function sendName() {
    stompClient.send("/app/hello", {}, JSON.stringify({'name': $("#name").val()}));
}
```

当客户端与服务端连接成功后，可以调用send()来发送STOMP消息。这个方法必须有一个参数，用来描述对应的STOMP的目的地。另外可以有两个可选的参数：headers，object类型包含额外的信息头部；body，一个String类型的参数。

## **总结客户端与服务端交互方式**

建立连接后

客户端向服务端发送消息：stompClient.send("/app/hello", {}, JSON.stringify({'name': $("#name").val()}));，进入controller层，接收消息。

服务端向客户端发送消息

一种情况，有客户端向服务端发送消息，可以使用@SendTo跳转

另一种情况，服务端主动发送消息

任意类中都可以

```java
public class 任意类 {
    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    // 客户端只要订阅了/topic/subscribeTest主题，调用这个方法即可
    public void templateTest() {
        messagingTemplate.convertAndSend("/topic/subscribeTest", new ServerMessage("服务器主动推的数据"));
    }
}


```

# **STMOP参考**

客户端js使用请参数[STOMP-WebSocket中文文档](https://blog.csdn.net/quanyuejie/article/details/53896140)