---
base: "[[_posts/learning/文档中心/文档中心.base]]"
created: 2025-01-09T11:49:00
categories: []
author: deathwhispers
---
# DefaultRequestDirector

1：该类的作用

Http请求的直接发起者，开发人员通过调用AbstractHttpClient类的execute方法，实际上就是由DefaultRequestDirector的execute完成的

2：构造函数以及属性分析

//构造函数参数以及该类成员的具体实现者分析

//第一个参数实现者HttpRequestExecutor,表示发送一个请求和接收一个请求,该类也可以插入拦截器

//第二个参数实现者SingleClientConnManager,表示客户端的链接管理，就像总管一样，管理者客户端的http连接

//第三个参数实现者DefaultConnectionReuseStrategy,表示客户端链接的重用策略，开发过程中用的比较少

//第四个参数实现者DefaultConnectionKeepAliveStrategy，表示客户端的长连接策略,

//第五个参数实现者ProxySelectorRoutePlanner:表示路由寻址功能的类

//第六个参数实现者BasicHttpProcessor：http拦截器

//第七个参数实现者DefaultHttpRequestRetryHandler：http请求的重试

//第八个参数实现者DefaultRedirectHandler：http重定向类

public DefaultRequestDirector(

final HttpRequestExecutor requestExec,

final ClientConnectionManager conman,

final ConnectionReuseStrategy reustrat,

final ConnectionKeepAliveStrategy kastrat,

final HttpRoutePlanner rouplan,

final HttpProcessor httpProcessor,

final HttpRequestRetryHandler retryHandler,

final RedirectHandler redirectHandler,

final AuthenticationHandler targetAuthHandler,

final AuthenticationHandler proxyAuthHandler,

final UserTokenHandler userTokenHandler,

final HttpParams params) {

/*省略代码*/

this.requestExec = requestExec;

this.connManager = conman;

this.reuseStrategy = reustrat;

this.keepAliveStrategy = kastrat;

this.routePlanner = rouplan;

this.httpProcessor = httpProcessor;

this.retryHandler = retryHandler;

this.redirectHandler = redirectHandler;

this.targetAuthHandler = targetAuthHandler;

this.proxyAuthHandler = proxyAuthHandler;

this.userTokenHandler = userTokenHandler;

this.params = params;

//managedConn表示一个适配器，通过managedConn可以获得里面PoolEntry,而PoolEntry封装这具体的请求发送类和发送的请求，即客户端的socket的创建都是由managedConn来管理和控制的

this.managedConn = null;

this.redirectCount = 0;

this.maxRedirects = this.params.getIntParameter(ClientPNames.MAX_REDIRECTS, 100);

this.targetAuthState = new AuthState();

this.proxyAuthState = new AuthState();

}

接下来我们看下http请求的最终执行方法execute(HttpHost target, HttpRequest request,HttpContext context)

//此处的context为BasicHttpContext

public HttpResponse execute(HttpHost target, HttpRequest request,HttpContext context)throws HttpException, IOException {

HttpRequest orig = request;

//RequestWrapper为一个请求的包装类,当发送post请求的时候,其实现者为EntityEnclosingRequestWrapper

//当为其他请求的时候,其实现者RequestWrapper

RequestWrapper origWrapper = wrapRequest(orig);

origWrapper.setParams(params);

HttpRoute origRoute = determineRoute(target, origWrapper, context);

//http请求必将使用路由,这里构建RoutedRequest,表示一个路由请求

RoutedRequest roureq = new RoutedRequest(origWrapper, origRoute);

long timeout = ConnManagerParams.getTimeout(params);

int execCount = 0;

boolean reuse = false;

HttpResponse response = null;

boolean done = false;

try {

while (!done) {

RequestWrapper wrapper = roureq.getRequest();

HttpRoute route = roureq.getRoute();

//如果上下文中有token

Object userToken = context.getAttribute(ClientContext.USER_TOKEN);

//开始执行http请求的时候,managedConn为null

if (managedConn == null) {

//此处的connManager的实现者为SingleClientConnManager,

//requestConnection只是使用匿名内部类的方式返回一个ClientConnectionRequest接口实例

ClientConnectionRequest connRequest = connManager.requestConnection(route, userToken);

if (orig instanceof AbortableHttpRequest) {

((AbortableHttpRequest) orig).setConnectionRequest(connRequest);

}

try {

//getConnection方法返回一个连接,其实例为ConnAdapter,在getConnection方法中关键作用是传入创建的PoolEntry

//PoolEntry里面封装了ClientConnectionOperator connOperator请求操着者，通过connOperator我们可以获得具体的http请求

//这样后续的http的打开，发送都可以使用ConnAdapter来进行管理和控制

managedConn = connRequest.getConnection(timeout, TimeUnit.MILLISECONDS);

} catch(InterruptedException interrupted) {

InterruptedIOException iox = new InterruptedIOException();

iox.initCause(interrupted);

throw iox;

}

//如果一个http请求中，httpparams做了如下设置

//httpParams.setBooleanParameter(“http.connection.stalecheck”, true);

//则HttpConnectionParams.isStaleCheckingEnabled(params)返回true

//stalecheck，决定了是否使用旧的连接检查。

//关闭旧的连接检查检查时间可以达到30毫秒,所以一般通过禁用该属性，可以提高性能

//这个参数期望得到一个java.lang.Boolean类型的值。出于性能的关键操作，检查应该被关闭。

if (HttpConnectionParams.isStaleCheckingEnabled(params)) {

// validate connection

this.log.debug(“Stale connection check”);

if (managedConn.isStale()) {

this.log.debug(“Stale connection detected”);

// BEGIN android-changed

try {

//关闭连接，通过managedConn中的PoolEntry将connect关闭

managedConn.close();

} catch (IOException ignored) {

// SSLSocket’s will throw IOException

// because they can’t send a “close

// notify” protocol message to the

// server. Just supresss any

// exceptions related to closing the

// stale connection.

}

// END android-changed

}

}

}

if (orig instanceof AbortableHttpRequest) {

((AbortableHttpRequest) orig).setReleaseTrigger(managedConn);

}

//该类是调用父类AbstractClientConnAdapter的isOpen方法,返回连接是否打开

if (!managedConn.isOpen()) {

//调用AbstractPoolEntry的open方法,open方法调用connOperator.openConnection完成socket的创建和连接

managedConn.open(route, context, params);

}

// BEGIN android-added

else {

// b/3241899 set the per request timeout parameter on reused connections

//默认超时时间为0

managedConn.setSocketTimeout(HttpConnectionParams.getSoTimeout(params));

}

// END android-added

try {

establishRoute(route, context);

} catch (TunnelRefusedException ex) {

if (this.log.isDebugEnabled()) {

this.log.debug(ex.getMessage());

}

response = ex.getResponse();

break;

}

// Reset headers on the request wrapper

wrapper.resetHeaders();

// Re-write request URI if needed

rewriteRequestURI(wrapper, route);

// Use virtual host if set

target = (HttpHost) wrapper.getParams().getParameter(

ClientPNames.VIRTUAL_HOST);

if (target == null) {

target = route.getTargetHost();

}

HttpHost proxy = route.getProxyHost();

// Populate the execution context

context.setAttribute(ExecutionContext.HTTP_TARGET_HOST,

target);

context.setAttribute(ExecutionContext.HTTP_PROXY_HOST,

proxy);

context.setAttribute(ExecutionContext.HTTP_CONNECTION,

managedConn);

context.setAttribute(ClientContext.TARGET_AUTH_STATE,

targetAuthState);

context.setAttribute(ClientContext.PROXY_AUTH_STATE,

proxyAuthState);

// Run request protocol interceptors

requestExec.preProcess(wrapper, httpProcessor, context);

context.setAttribute(ExecutionContext.HTTP_REQUEST,

wrapper);

//从establishRoute到这里都是做一些路由，上线文的事，这里就不重点关注了

boolean retrying = true;

//在这里进行一个死循环，当一次http请求完成之后，retrying设置为false,退出循环

//当出现异常的时候，根据retryHandler.retryRequest返回值来决定是否退出循环

//retryHandler默认重试三次，而且仅当是可恢复的异常才能正常循环

while (retrying) {

// Increment total exec count (with redirects)

execCount++;

// Increment exec count for this particular request

wrapper.incrementExecCount();

if (wrapper.getExecCount() > 1 && !wrapper.isRepeatable()) {

throw new NonRepeatableRequestException(“Cannot retry request” +

“with a non-repeatable request entity”);

}

try {

if (this.log.isDebugEnabled()) {

this.log.debug(“Attempt” + execCount + ” to execute request”);

}

// BEGIN android-added

if ((!route.isSecure())

&& (!isCleartextTrafficPermitted(

route.getTargetHost().getHostName()))) {

throw new IOException(

“Cleartext traffic not permitted:” + route.getTargetHost());

}

// END android-added

//执行请求获得响应

response = requestExec.execute(wrapper, managedConn, context);

retrying = false;

} catch (IOException ex) {

this.log.debug(“Closing the connection.”);

managedConn.close();

if (retryHandler.retryRequest(ex, execCount, context)) {

if (this.log.isInfoEnabled()) {

this.log.info(“I/O exception (”+ ex.getClass().getName() +

“) caught when processing request:”

+ ex.getMessage());

}

if (this.log.isDebugEnabled()) {

this.log.debug(ex.getMessage(), ex);

}

this.log.info(“Retrying request”);

} else {

throw ex;

}

// If we have a direct route to the target host

// just re-open connection and re-try the request

if (route.getHopCount() == 1) {

this.log.debug(“Reopening the direct connection.”);

managedConn.open(route, context, params);

} else {

// otherwise give up

throw ex;

}

}

}

// Run response protocol interceptors

//开始运行响应拦截器

response.setParams(params);

requestExec.postProcess(response, httpProcessor, context);

// The connection is in or can be brought to a re-usable state.

reuse = reuseStrategy.keepAlive(response, context);

if(reuse) {

// Set the idle duration of this connection

long duration = keepAliveStrategy.getKeepAliveDuration(response, context);

managedConn.setIdleDuration(duration, TimeUnit.MILLISECONDS);

}

//根据response来决定是否需要进一步请求，即重定向

RoutedRequest followup = handleResponse(roureq, response, context);

if (followup == null) {

done = true;

} else {

if (reuse) {

this.log.debug(“Connection kept alive”);

// Make sure the response body is fully consumed, if present

HttpEntity entity = response.getEntity();

if (entity != null) {

entity.consumeContent();

}

// entity consumed above is not an auto-release entity,

// need to mark the connection re-usable explicitly

managedConn.markReusable();

} else {

managedConn.close();

}

// check if we can use the same connection for the followup

if (!followup.getRoute().equals(roureq.getRoute())) {

releaseConnection();

}

roureq = followup;

}

userToken = this.userTokenHandler.getUserToken(context);

context.setAttribute(ClientContext.USER_TOKEN, userToken);

if (managedConn != null) {

managedConn.setState(userToken);

}

} // while not done

// check for entity, release connection if possible

if ((response == null) || (response.getEntity() == null) ||

!response.getEntity().isStreaming()) {

// connection not needed and (assumed to be) in re-usable state

if (reuse)

managedConn.markReusable();

releaseConnection();

} else {

// install an auto-release entity

HttpEntity entity = response.getEntity();

entity = new BasicManagedEntity(entity, managedConn, reuse);

response.setEntity(entity);

}

return response;

} catch (HttpException ex) {

abortConnection();

throw ex;

} catch (IOException ex) {

abortConnection();

throw ex;

} catch (RuntimeException ex) {

abortConnection();

throw ex;

}

} // execute

Http的请求过程是及其复杂的，这里我们重点关注下几个地方

第26行，connManager的实现者为SingleClientConnManager，通过调用SingleClientConnManager的requestConnection方法我们可以获得一个匿名内部类connRequest

第34行，通过调用connRequest.getConnection的方法，返回ManagedClientConnection的对象managedConn ，其实现为ConnAdapter，我们看下connRequest.getConnection的具体实现

```plain text
public final ClientConnectionRequest requestConnection(
            final HttpRoute route,
            final Object state) {


        return new ClientConnectionRequest() {


            public void abortRequest() {
                // Nothing to abort, since requests are immediate.
            }


            public ManagedClientConnection getConnection(
                    long timeout, TimeUnit tunit) {
                return SingleClientConnManager.this.getConnection(
                        route, state);
            }
        };
    }
```

可见其调用了SingleClientConnManager.this.getConnection方法

```plain text
public ManagedClientConnection getConnection(HttpRoute route, Object state) {


        if (route == null) {
            throw new IllegalArgumentException("Route may not be null.");
        }
        assertStillUp();


        if (log.isDebugEnabled()) {
            log.debug("Get connection for route " + route);
        }
        //在构建SingleClientConnManager的时候,managedConn为null;
        if (managedConn != null)
            revokeConnection();


        // check re-usability of the connection
        boolean recreate = false;
        boolean shutdown = false;


        // Kill the connection if it expired.
        //建立连接的预处理,关闭超时连接
        closeExpiredConnections();


        if (uniquePoolEntry.connection.isOpen()) {
            RouteTracker tracker = uniquePoolEntry.tracker;
            shutdown = (tracker == null || // can happen if method is aborted
                        !tracker.toRoute().equals(route));
        } else {
            // If the connection is not open, create a new PoolEntry,
            // as the connection may have been marked not reusable,
            // due to aborts -- and the PoolEntry should not be reused
            // either.  There's no harm in recreating an entry if
            // the connection is closed.
            recreate = true;
        }


        if (shutdown) {
            recreate = true;
            try {
                uniquePoolEntry.shutdown();
            } catch (IOException iox) {
                log.debug("Problem shutting down connection.", iox);
            }
        }


        if (recreate)
            uniquePoolEntry = new PoolEntry();


        // BEGIN android-changed
        // When using a recycled Socket, we need to re-tag it with any
        // updated statistics options.
        try {
            final Socket socket = uniquePoolEntry.connection.getSocket();
            if (socket != null) {
                TrafficStats.tagSocket(socket);
            }
        } catch (IOException iox) {
            log.debug("Problem tagging socket.", iox);
        }
        // END android-changed


        managedConn = new ConnAdapter(uniquePoolEntry, route);


        return managedConn;
    }
```

这个方法的主要作用有两点

1：因为该方法不是线程安全的，故需要在建立socket前，做一些预处理

2：通过传入的PoolEntry，创建ConnAdapter，这样就可以通过ConnAdapter来获得PoolEntry的ClientConnectionOperator连接操作者，通过ClientConnectionOperator操作者便可以获得OperatedClientConnection connection被操作的链接；以后http的操作都是通过ConnAdapter适配器来完成

第46行，告诉我们一般不要在httpparams设置stalecheck过时检查

第74行，通过managedConn.open方法完成socket的建立，绑定至目标host managedConn.open调用了父类AbstractPooledConnAdapter的open方法

```plain text
public void open(HttpRoute route, HttpContext context, HttpParams params)
        throws IOException {
        assertAttached();
        poolEntry.open(route, context, params);
    }
```

可见managedConn是通过父类AbstractPooledConnAdapter来操作poolEntry来实现各种操作，我们在接着看poolEntry.open，其会调用到AbstractPoolEntry的open方法

```plain text
public void open(HttpRoute route,
                     HttpContext context, HttpParams params)
        throws IOException {
/*省略部分代码*/
        this.tracker = new RouteTracker(route);
        final HttpHost proxy  = route.getProxyHost();
        connOperator.openConnection
            (this.connection,
             (proxy != null) ? proxy : route.getTargetHost(),
             route.getLocalAddress(),
             context, params);
        RouteTracker localTracker = tracker; // capture volatile
        if (proxy == null) {
            localTracker.connectTarget(this.connection.isSecure());
        } else {
            localTracker.connectProxy(proxy, this.connection.isSecure());
        }
    }
```

在这里主要调用了connOperator的openConnection来完成socket的创建和绑定，其中connOperator默认实现为DefaultClientConnectionOperator

```plain text
public void openConnection(OperatedClientConnection conn,
                               HttpHost target,
                               InetAddress local,
                               HttpContext context,
                               HttpParams params)
        throws IOException {




       /*省略部分代码*/




        final Scheme schm = schemeRegistry.getScheme(target.getSchemeName());
        final SocketFactory sf = schm.getSocketFactory();
        final SocketFactory plain_sf;
        final LayeredSocketFactory layered_sf;
        if (sf instanceof LayeredSocketFactory) {
            plain_sf = staticPlainSocketFactory;
            layered_sf = (LayeredSocketFactory)sf;
        } else {
            plain_sf = sf;
            layered_sf = null;
        }
        InetAddress[] addresses = InetAddress.getAllByName(target.getHostName());




        for (int i = 0; i < addresses.length; ++i) {
            Socket sock = plain_sf.createSocket();
            conn.opening(sock, target);




            try {
                Socket connsock = plain_sf.connectSocket(sock,
                    addresses[i].getHostAddress(),
                    schm.resolvePort(target.getPort()),
                    local, 0, params);
                if (sock != connsock) {
                    sock = connsock;
                    conn.opening(sock, target);
                }
                /*
                 * prepareSocket is called on the just connected
                 * socket before the creation of the layered socket to
                 * ensure that desired socket options such as
                 * TCP_NODELAY, SO_RCVTIMEO, SO_LINGER will be set
                 * before any I/O is performed on the socket. This
                 * happens in the common case as
                 * SSLSocketFactory.createSocket performs hostname
                 * verification which requires that SSL handshaking be
                 * performed.
                 */
                prepareSocket(sock, context, params);
                if (layered_sf != null) {
                    Socket layeredsock = layered_sf.createSocket(sock,
                        target.getHostName(),
                        schm.resolvePort(target.getPort()),
                        true);
                    if (layeredsock != sock) {
                        conn.opening(layeredsock, target);
                    }
                    conn.openCompleted(sf.isSecure(layeredsock), params);
                } else {
                    conn.openCompleted(sf.isSecure(sock), params);
                }
                break;
            // BEGIN android-changed
            //       catch SocketException to cover any kind of connect failure
            } catch (SocketException ex) {
                if (i == addresses.length - 1) {
                    final ConnectException cause;
                    if (ex instanceof ConnectException) {
                        cause = (ConnectException) ex;
                    } else {
                        cause = new ConnectException(ex.getMessage());
                        cause.initCause(ex);
                    }
                    throw new HttpHostConnectException(target, cause);
                }
            // END android-changed
            } catch (ConnectTimeoutException ex) {
                if (i == addresses.length - 1) {
                    throw ex;
                }
            }
        }
    }
```

第145行，就是执行请求获得响应的过程