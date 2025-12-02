---
base: "[[_posts/learning/文档中心/文档中心.base]]"
created: 2025-01-09T11:49:00
categories: []
author: deathwhispers
---
# ConnectionReuseStrategy，ConnectionKeepAliveStrategy解析

1：基础介绍

1.1）Keep-Alive解析

http协议作为上层应用协议,其是基于TCP/IP协议,UDP协议传输层上进行的;http协议通过socket这个套接字完成客户端和服务端的通信;

http协议目前主要有两个版本HTTP1.0和HTTP1.1,他们都是无状态协议

在HTTP1.0中,每一次请求响应之后,下一次的请求需要断开之前的连接,再重新开始;

再HTTP1.1中,使用keep-alive在一次TCP连接中可以持续发送多份数据而不会断开连接,通过kttp-alive机制,可以减少tcp连接建立次数,也意味着可以减少TIME_WAIT状态连接,以此提高性能和提高http的服务器的吞吐量(更少的tcp连接意味着更少的系统内核调用,socket的accept()和close()调用).

因此便出现了Connection: keep-alive的设置,用于建立长连接,即我们所说的Keep-Alive模式

![](https://cdn.nlark.com/yuque/0/2023/png/29230873/1698038930834-6e0244e9-e865-4d1a-867c-0d11f9c0e006.png)

短链接与长连接示意

http1.0中默认是关闭的,需要在http头中加入”Connection: Keep-Alive” ,才能启用Keep-Alive,当服务器收到附带有Connection: Keep-Alive的请求时,它也会在响应头中添加一个同样的字段来使用Keep-Alive,这样一来,客户端和服务器之间的HTTP连接就会被保持,不会断开(超过Keep-Alive规定的时间, 意外断电等情况除外),当客户端发送另外一个请求时,就使用这条已经建立的连接

http1.1中默认启用Keep-Alive,如果假如”Connection: close“,才关闭.

Keep-Alive不会永久保持连接,它有一个保持时间,可以在不同的服务器软件中设定这个时间;

一次完成的额http请求是否能够保持,同时也是靠服务端是否具备Keep-Alive能力;

1.2 如何判断客户端已经完整的接收服务端的数据,针对HTTP1.0 和HTTP1.1

在java中, 使用socket编程的时候,我们经常看到如下代码

```plain text
Socket socket = new Socket("localhost",10086);
InputStream is = socket.getInputStream();
BufferedReader br = new BufferedReader(new InputStreamReader(is));
String info = null;
while((info=br.readLine()) != -1){


}
```

所以在普通的socket编程中,我们可以使用EOF(-1)来判断是否完整的接收到服务端的返回的数据;

这是因为在一次普通的http请求中,即没有添加Connection: Keep-Alive属性的http请求中,服务端响应之后,会断开连接,故使用EOF判断是准确的;

但是这种方式针对添加的Connection: Keep-Alive属性的http请求来说,就无法生效了;

因此,在http1.0及之前的版本中, content-length字段可有可无

在http1.1及之后的版本,如果是keep alive,则content-length和chunk必然是二选一,若是非keep alive,则和Hhttp1.0一样.content-length可有可无.

2.在DefaultRequestDirector.execute 方法中有如下代码

```plain text
// The connection is in or can be brought to a re-usable state.
reuse = reuseStrategy.keepAlive(response, context);
if (reuse) {
    // Set the idle duration of this connection
    final long duration = keepAliveStrategy.getKeepAliveDuration(response, context);
    if (this.log.isDebugEnabled()) {
        final String s;
        if (duration > 0) {
            s = "for " + duration + " " + TimeUnit.MILLISECONDS;
        } else {
            s = "indefinitely";
        }
        this.log.debug("Connection can be kept alive " + s);
    }
    managedConn.setIdleDuration(duration, TimeUnit.MILLISECONDS);
}
```

从这段代码中可以看出,当完成一次http请求之后,并没有立即关闭这个tcp连接和释放资源;而是通过可重用策略来判断这个连接能否保持,以及保持多长时间;

我们先分析下:

如何判断连接是可重用的??

我们可以通过上面的keepAlive()方法来进行具体分析,reuseStrategy的默认实现者为DefaultConnectionReuseStrategy

我们看一下keep Alive方法:

```plain text
// 该方法的作用就是在一次请求之后,这个连接能够被保持
// 如果返回false,则调用者应该立即关闭连接
// 如果返回true,则调用者应该保持这个连接从而可以应用于其他请求
@Override
public boolean keepAlive(final HttpResponse response,
                         final HttpContext context) {
    Args.notNull(response, "HTTP response");
    Args.notNull(context, "HTTP context");


    // If a HTTP 204 No Content response contains a Content-length with value > 0 or Transfer-Encoding,
    // don't reuse the connection. This is to avoid getting out-of-sync if a misbehaved HTTP server
    // returns content as part of a HTTP 204 response.
    if (response.getStatusLine().getStatusCode() == HttpStatus.SC_NO_CONTENT) {
        final Header clh = response.getFirstHeader(HTTP.CONTENT_LEN);
        if (clh != null) {
            try {
                final int contentLen = Integer.parseInt(clh.getValue());
                if (contentLen > 0) {
                    return false;
                }
            } catch (final NumberFormatException ex) {
                // fall through
            }
        }




        final Header teh = response.getFirstHeader(HTTP.TRANSFER_ENCODING);
        if (teh != null) {
            return false;
        }
    }




    final HttpRequest request = (HttpRequest) context.getAttribute(HttpCoreContext.HTTP_REQUEST);
    if (request != null) {
        try {
            final TokenIterator ti = new BasicTokenIterator(request.headerIterator(HttpHeaders.CONNECTION));
            while (ti.hasNext()) {
                final String token = ti.nextToken();
                if (HTTP.CONN_CLOSE.equalsIgnoreCase(token)) {
                    return false;
                }
            }
        } catch (final ParseException px) {
            // invalid connection header. do not re-use
            return false;
        }
    }




    // Check for a self-terminating entity. If the end of the entity will
    // be indicated by closing the connection, there is no keep-alive.
    final ProtocolVersion ver = response.getStatusLine().getProtocolVersion();
    final Header teh = response.getFirstHeader(HTTP.TRANSFER_ENCODING);
    if (teh != null) {
        if (!HTTP.CHUNK_CODING.equalsIgnoreCase(teh.getValue())) {
            return false;
        }
    } else {
        if (canResponseHaveBody(request, response)) {
            final Header[] clhs = response.getHeaders(HTTP.CONTENT_LEN);
            // Do not reuse if not properly content-length delimited
            if (clhs.length == 1) {
                final Header clh = clhs[0];
                try {
                    final int contentLen = Integer.parseInt(clh.getValue());
                    if (contentLen < 0) {
                        return false;
                    }
                } catch (final NumberFormatException ex) {
                    return false;
                }
            } else {
                return false;
            }
        }
    }




    // Check for the "Connection" header. If that is absent, check for
    // the "Proxy-Connection" header. The latter is an unspecified and
    // broken but unfortunately common extension of HTTP.
    HeaderIterator headerIterator = response.headerIterator(HTTP.CONN_DIRECTIVE);
    if (!headerIterator.hasNext()) {
//Proxy-Connection是http1.0 时代的产物。老旧的代理，如果设置 connection: keepalive，
        // 代理原样转发给服务器，服务器会以为要建立长久连接，但是代理并不支持，这样就出问题了。
        // 所以改为设置 proxy-connection: keepalive，如果是新的代理，
        // 支持 keepalive，它会认得这个头，并改成 connection: keepalive 转发给服务器，
        // 顺利建立持久连接；如果是老的代理，它不认识，会原样转发，这时候服务器也不会建立持久连接
        headerIterator = response.headerIterator("Proxy-Connection");
    }




    if (headerIterator.hasNext()) {
        try {
            final TokenIterator ti = new BasicTokenIterator(headerIterator);
            boolean keepalive = false;
            while (ti.hasNext()) {
                final String token = ti.nextToken();
                // 如果connection:close则返回false
                if (HTTP.CONN_CLOSE.equalsIgnoreCase(token)) {
                    return false;
                // 如果connection:keep-allive则返回true
                } else if (HTTP.CONN_KEEP_ALIVE.equalsIgnoreCase(token)) {
                    // continue the loop, there may be a "close" afterwards
                    keepalive = true;
                }
            }
            if (keepalive) {
                return true;
            // neither "close" nor "keep-alive", use default policy
            }




        } catch (final ParseException px) {
            // invalid connection header. do not re-use
            return false;
        }
    }




    // default since HTTP/1.1 is persistent, before it was non-persistent
    return !ver.lessEquals(HttpVersion.HTTP_1_0);
}
```

总结:

1.该方法的作用就是在一次请求之后,这个连接能否被保持,如果返回false,则调用者应该立即关闭连接;如果返回true,则调用者应该保持这个连接从而可以应用于其他请求

2.由于HTTP1.0时代,还不能有效支持connection,故多了一个Proxy-Connection头信息,该字段出现的原因是:在HTTP1.0中老旧的代理,如果设置connection: keepalive,代理原样转发给服务端,服务端会以为要建立长久连接,但是代理并不支持,这样就出问题了,所以改为设置Proxy-connection: keepalive, 如果是新的代理,支持keepalive,他会认得这个头,并改成connection:keepalive 转发给服务器,顺利建立持久连接;如果是老的代理,他不认识,会原样转发,这时候服务器也不会建立持久连接

---

当一个请求视为可重用之后,那么链接是否能一直保持连接状态?会不会超过一定时间,连接就断开了?

答案是会的,当链接超过预设时间,会自动断开:

如何获取连接的存货时间,和哪些设置有关

keepAliveStrategy.getKeepAliveDuration

keepAliveStrategy的实现为DefaultConnectionKeepAliveStrategy

DefaultConnectionKeepAliveStrategy.java

```plain text
@Override
public long getKeepAliveDuration(final HttpResponse response, final HttpContext context) {
    Args.notNull(response, "HTTP response");
    final HeaderElementIterator it = new BasicHeaderElementIterator(
            response.headerIterator(HTTP.CONN_KEEP_ALIVE));
    while (it.hasNext()) {
        final HeaderElement he = it.nextElement();
        final String param = he.getName();
        final String value = he.getValue();
        if (value != null && param.equalsIgnoreCase("timeout")) {
            try {
                return Long.parseLong(value) * 1000;
            } catch(final NumberFormatException ignore) {
            }
        }
    }
    return -1;
}
```

通过Keep-Alive头信息,获取到timeout的值.作为超时时间;单位毫秒

如: Keep-Alive: timeout=5, max=100,则超时时间为5000ms

若无keep-Alive头信息, 则默认连接一直存活(默认-1)