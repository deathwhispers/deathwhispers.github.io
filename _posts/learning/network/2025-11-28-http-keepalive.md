---
layout: post
title: HTTP keepalive
slug: http-keepalive
type:
  - note
date: 2025-11-28
week: 2025-W48
status: draft
tags:
  - 计算机网络
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---


# HTTP keepalive

**问题:**

1. keepalive 是否开启服务端控制还是客户端控制？
2. keepalive的时间是由服务端控制还是客户端控制？
3. keepalive时间一到，是由客户端主动关闭还是服务端主动关闭？
4. 如果客户端不是httpclient，使用telnet连接服务端？

http请求示意图:

![](/assets/images/learning/network/http-keepalive/8cf9825323be5b736b1e84f9ab89fa2d.png)

场景一

- 1.httpclient连续两次请求，间隔10秒，服务端设置keealive时间为5秒
- 2.client代码：

```plain text
closeableHttpClient.execute(httpGet);
Thread.sleep(10000);
closeableHttpClient.execute(httpGet);
Thread.sleep(10000);
```

- 3.服务端设置keepalive：

```plain text
((AbstractProtocol) connector.getProtocolHandler())
.setKeepAliveTimeout(5000);
```

- 4.使用wireshark抓包

![](/assets/images/learning/network/http-keepalive/3b81ec7ad17f47c8e8b1ce06bd5195fe.png)

```plain text
从图中可以看到：第一次请求的端口是64360，并且在5秒之后，由服务端主动发送fin包关闭连接。而第二次请求显然已经不能复用连接了，使用的新的端口64361重新连接服务器，后续的行为基本和第一次请求一样。
```

![](/assets/images/learning/network/http-keepalive/382e083a1b3e847cfbfb4fe05924266b.png)

```plain text
请求中带有keepalive头，HTTP1.1之后默认都是开启keepalive，即使是不带keepalive参数。后面将通过close头关闭keepalive看看效果。
```

- 5.查看本地的端口状态

![](/assets/images/learning/network/http-keepalive/af616d95233b83f763c2ad0df51953cc.png)

```plain text
可以看到服务端8080端口进入了FIN_WAIT_2状态，参照文中刚开始的第一张图，这显然是主动关闭方才会有的状态，同样64360进入了CLOSE_WAIT状态，说明client端是被动关闭的。
```

这里比较奇怪的是，没能看到服务端进入TIME_WAIT状态(可能是环境问题，即使是客户端主动关闭也没看到)。

**场景二**

1.改造场景一，httpclient请求头加上Connection: Close，请求时间间隔改为1秒 –

httpGet.addHeader(“Connection”, “Close”);

2.wireshark抓包

![](/assets/images/learning/network/http-keepalive/9799c440611fe63e33ca72d2eb044fe8.png)

可以看到，主动关闭方还是服务器端，并且立刻关闭，并没有等待keepalive时间到达。

**场景三**

1.httpclient默认keealive，服务端响应头加上Connection: Close –

response.setHeader(“Connection”, “Close”);

2.wireshark抓包

![](/assets/images/learning/network/http-keepalive/24ca0fb465f5a8510af4299a062383ce.png)

从图中看出，主动关闭方是客户端。如果客户端不是httpclient，是telnet，客户端会主动关闭？后面实验一下。

如果客户端和服务端都加上Connection: Close，那么主动关闭方是客户端（已经抓包查看过）。

**场景四**

- *

**

跟场景四一样，client有httpclient改成telnet，服务端返回Connection: Close 以及keepalive时间为 5秒。

虽然服务端返回Connection: Close ，但是telnet客户端并不理会，而是等到服务端keepalive时间到了（5秒），才由服务端关闭。

服务端keepalive改成30秒，同样是30秒后由服务端主动关闭。

**场景五**

客户端设置keepalive的时间，设置为3秒，比服务端小（5秒）。– httpGet.addHeader(“Keep-alive”, “3000”);

wireshark 抓包

服务端5秒后主动关闭，而不是期望的客户端主动关闭。估计客户端主动关闭只有在浏览器端才能实现，或者需要合适的参数和客户端实现。

**答疑**

**基于文中开头的疑问做一个解答**

1.keepalive 是否开启服务端控制还是客户端控制？

keepalive可以由双方共同控制，需要双方都开启才能生效，HTTP1.1客户端默认开启，客户端想关闭可以通过设置Connection: Close，服务端同样想关闭可以设置Connection: Close。双方哪方先收到Connection: Close 则由收到方关闭（前提是双方的实现都支持，比如telnet就不支持）

2.keepalive的时间是由服务端控制还是客户端控制？

时间主要还是由服务端控制，时间一到由服务端主动关闭，当然客户端如果有实现设置一定时间后，由客户端主动关闭也可以。一般的httpclient库都有提供相应的配置，设置关闭长期不使用的连接，如connectionManager.closeIdleConnections(readTimeout * 2, TimeUnit.MILLISECONDS);

[https://my.oschina.net/greki/blog/83350](https://my.oschina.net/greki/blog/83350)

3.keepalive时间一到，是由客户端主动关闭还是服务端主动关闭？

根据上述的分析，哪方的时间短，由哪一方来关闭，除非双方的实现有更明确的协议

4.如果客户端不是httpclient，使用telnet连接服务端？

telnet客户端除了连接时进行三次握手，用来发送数据接收数据，基本无其他实现逻辑。即接收到服务器的响应之后，不会有相关HTTP协议的处理。

- *

**

**总结**

HTTP是应用层协议，具体的表现行为取决于HTTP服务器以及HTTP client的实现。本文的分析使用tomcat服务器，apache httpclient。