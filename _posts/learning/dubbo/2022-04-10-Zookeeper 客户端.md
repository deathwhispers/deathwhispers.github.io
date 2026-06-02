---
layout: post
title: Zookeeper 客户端
author: deathwhispers
date: 2022-04-10
slug: dubbo-zookeeper-client
categories:
- Dubbo
tags:
- Dubbo
type: note
status: draft
created: 2022-04-21 11:50
updated: 2022-04-21 18:33
---

本文基于 Dubbo 2.6.1 版本，望知悉。

# 1. 概述

在 dubbo-remoting-zookeeper 模块，实现了 Dubbo 对 Zookeeper 客户端的封装。在该模块中，抽象了**通用**的 Zookeeper Client API 接口，实现了**两种** Zookeeper Client 库的接入：

- 基于 [Apache Curator](https://curator.apache.org/)
实现。

```xml
<dubbo:registry address="zookeeper://127.0.0.1:2181" client="curator" />
```

---

- 基于 [ZkClient](https://github.com/sgroschupf/zkclient)
实现。

```xml
<dubbo:registry address="zookeeper://127.0.0.1:2181" client="zkclient" />
```

---

默认不配置 client 的情况下，使用 Curator 。

---

dubbo-remoting-zookeeper 的整体类图如下：

![类图](/assets/images/learning/dubbo/dubbo-zookeeper-client/04f5580b651cc4cea1f0e4d7992b5be5.png)

下面，我们按照接口到实现的顺序，往下看。

# 2. 接口

## 2.1 StateListener

com.alibaba.dubbo.remoting.zookeeper.StateListener ，状态监听器接口，代码如下：

```java
public interface StateListener {
    /**
     * 状态 - 已断开
     */
    int DISCONNECTED = 0;
    /**
     * 状态 - 已连接
     */
    int CONNECTED = 1;
    /**
     * 状态 - 已重连
     */
    int RECONNECTED = 2;

    /**
     * 状态变更回调
     *
     * @param connected 状态
     */
    void stateChanged(int connected);
}
```

---

## 2.2 ChildListener

com.alibaba.dubbo.remoting.zookeeper.StateListener ，节点监听器接口，代码如下：

```java
public interface ChildListener {
    /**
     * 子节点发生变化的回调
     *
     * @param path 节点
     * @param children 最新的子节点列表
     */
    void childChanged(String path, List<String> children);
}
```

---

## 2.3 ZookeeperClient

com.alibaba.dubbo.remoting.zookeeper.ZookeeperClient ，Zookeeper 客户端接口，代码如下：

```java
public interface ZookeeperClient {
    /**
     * 创建节点
     *
     * @param path 节点路径
     * @param ephemeral 是否临时节点
     */
    void create(String path, boolean ephemeral);

    /**
     * 删除节点
     *
     * @param path 节点路径
     */
    void delete(String path);

    List<String> getChildren(String path);

    /**
     * 添加 ChildListener
     *
     * @param path 节点路径
     * @param listener 监听器
     * @return 子节点列表
     */
    List<String> addChildListener(String path, ChildListener listener);

    /**
     * 移除 ChildListener
     *
     * @param path 节点路径
     * @param listener 监听器
     */
    void removeChildListener(String path, ChildListener listener);

    /**
     * 添加 StateListener
     *
     * @param listener 监听器
     */
    void addStateListener(StateListener listener);

    /**
     * 移除 StateListener
     *
     * @param listener 监听器
     */
    void removeStateListener(StateListener listener);

    /**
     * @return 是否连接
     */
    boolean isConnected();

    /**
     * 关闭
     */
    void close();

    /**
     * @return 获得注册中心 URL
     */
    URL getUrl();
}
```

---

- 状态相关方法
    - #isConnected()
    - #close()
    - #getUrl()
- 数据相关方法
    - #create(path, ephemeral)
    - #getChildren(path)
    - 从 API 上，Dubbo 只使用节点的路径，而不使用节点的值（内容）。
- 监听相关方法
    - #addChildListener(path, listener)
    - #removeChildListener(path, listener)
    - #addStateListener(listener)
    - #removeStateListener(listener)

## 2.4 AbstractZookeeperClient

com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient ，实现 ZookeeperClient 接口，Zookeeper 客户端**抽象类**，实现通用的逻辑。

### 2.4.1 属性

```java
public abstract class AbstractZookeeperClient<TargetChildListener> implements ZookeeperClient {

    /**
     * 注册中心 URL
     */
    private final URL url;
    /**
     * StateListener 集合
     */
    private final Set<StateListener> stateListeners = new CopyOnWriteArraySet<StateListener>();
    /**
     * ChildListener 集合
     *
     * key1：节点路径
     * key2：ChildListener 对象
     * value ：监听器具体对象。不同 Zookeeper 客户端，实现会不同。
     */
    private final ConcurrentMap<String, ConcurrentMap<ChildListener, TargetChildListener>> childListeners = new ConcurrentHashMap<String, ConcurrentMap<ChildListener, TargetChildListener>>();
    /**
     * 是否关闭
     */
    private volatile boolean closed = false;

    public AbstractZookeeperClient(URL url) {
        this.url = url;
    }

    @Override
    public URL getUrl() {
        return url;
    }

    // ... 省略其他方法
}
```

---

见代码注释。

### 2.4.2 create

```java
@Override
public void create(String path, boolean ephemeral) {
    // 循环创建父路径
    int i = path.lastIndexOf('/');
    if (i > 0) {
        String parentPath = path.substring(0, i);
        if (!checkExists(parentPath)) {
            create(parentPath, false);
        }
    }
    // 创建临时节点
    if (ephemeral) {
        createEphemeral(path);
    // 创建持久节点
    } else {
        createPersistent(path);
    }
}
```

---

- #checkExists(path)**抽象**
方法，节点是否存在。代码如下：

```java
protected abstract boolean checkExists(String path);
```

---

- #createEphemeral(path)**抽象**
方法，创建临时节点。代码如下：

```java
protected abstract void createPersistent(String path);
```

---

- #createPersistent(path)**抽象**
方法，创建持久节点。代码如下：

```java
protected abstract void createEphemeral(String path);
```

---

### 2.4.3 StateListener 相关方法

```java
@Override
public void addStateListener(StateListener listener) {
    stateListeners.add(listener);
}

@Override
public void removeStateListener(StateListener listener) {
    stateListeners.remove(listener);
}

public Set<StateListener> getSessionListeners() {
    return stateListeners;
}

/**
 * StateListener 数组，回调
 *
 * @param state 状态
 */
protected void stateChanged(int state) {
    for (StateListener sessionListener : getSessionListeners()) {
        sessionListener.stateChanged(state);
    }
}
```

---

### 2.4.4 ChildListener 相关方法

```java
@Override
public List<String> addChildListener(String path, final ChildListener listener) {
    // 获得路径下的监听器数组
    ConcurrentMap<ChildListener, TargetChildListener> listeners = childListeners.get(path);
    if (listeners == null) {
        childListeners.putIfAbsent(path, new ConcurrentHashMap<ChildListener, TargetChildListener>());
        listeners = childListeners.get(path);
    }
    // 获得是否已经有该监听器
    TargetChildListener targetListener = listeners.get(listener);
    // 监听器不存在，进行创建
    if (targetListener == null) {
        listeners.putIfAbsent(listener, createTargetChildListener(path, listener));
        targetListener = listeners.get(listener);
    }
    // 向 Zookeeper ，真正发起订阅
    return addTargetChildListener(path, targetListener);
}

@Override
public void removeChildListener(String path, ChildListener listener) {
    ConcurrentMap<ChildListener, TargetChildListener> listeners = childListeners.get(path);
    if (listeners != null) {
        TargetChildListener targetListener = listeners.remove(listener);
        if (targetListener != null) {
            // 向 Zookeeper ，真正发起取消订阅
            removeTargetChildListener(path, targetListener);
        }
    }
}
```

---

- #createTargetChildListener(path, listener)**抽象**
方法，创建真正的 ChildListener 对象。因为，每个 Zookeeper 的库，实现不同。代码如下：

```java
protected abstract TargetChildListener createTargetChildListener(String path, ChildListener listener);
```

---

- #addTargetChildListener(path, targetListener)**抽象**
方法，向 Zookeeper ，真正发起订阅。代码如下：

```java
protected abstract List<String> addTargetChildListener(String path, TargetChildListener listener);
```

---

- #removeTargetChildListener(path, targetListener)**抽象**
方法，向 Zookeeper ，真正发起取消订阅。代码如下：

```java
protected abstract void removeTargetChildListener(String path, TargetChildListener listener);
```

---

### 2.4.5 close

```java
@Override
public void close() {
    if (closed) {
        return;
    }
    closed = true;
    try {
        doClose();
    } catch (Throwable t) {
        logger.warn(t.getMessage(), t);
    }
}
```

---

- #doClose()**抽象**
方法，关闭 Zookeeper 连接。代码如下：

```java
protected abstract void doClose();
```

---

## 2.5 ZookeeperTransporter

com.alibaba.dubbo.remoting.zookeeper.ZookeeperTransporter ，Zookeeper 工厂接口，代码如下：

```java
@SPI("curator")
public interface ZookeeperTransporter {

    /**
     * 连接创建 ZookeeperClient 对象
     *
     * @param url 注册中心地址
     * @return ZookeeperClient 对象
     */
    @Adaptive({Constants.CLIENT_KEY, Constants.TRANSPORTER_KEY})
    ZookeeperClient connect(URL url);

}
```

---

- #connect(url)
方法，连接创建 ZookeeperClient 对象。
- @SPI("curator")
注解，使用 Dubbo SPI 机制，默认使用 Curator 实现。
- @Adaptive({Constants.CLIENT_KEY, Constants.TRANSPORTER_KEY})
注解，使用 Dubbo SPI Adaptive 机制，根据
url
参数，加载对应的 ZookeeperTransporter 拓展实现类。

# 3. 基于 Curator 实现

Apache Curator ，作为 Zookeeper 客户端的库，基本是**最佳**的选择，在 Sharding-JDBC、Elastic-Job 等等中间都选择了 Curator 连接 Zookeeper 。

友情提示，如果对 Curator 的 API 不熟悉的胖友，推荐看下官方文档，进行下学习。本文不会写 Curator 使用方法。

## 3.1 CuratorZookeeperClient

com.alibaba.dubbo.remoting.zookeeper.curator.CuratorZookeeperClient ，实现 ZookeeperTransporter 抽象类，基于 Curator 的 Zookeeper 客户端实现类。

### 3.1.1 属性

```java
/**
 * client 对象
 */
private final CuratorFramework client;

public CuratorZookeeperClient(URL url) {
    super(url);
    try {
        // 创建 client 对象
        CuratorFrameworkFactory.Builder builder = CuratorFrameworkFactory.builder()
                .connectString(url.getBackupAddress()) // 连接地址
                .retryPolicy(new RetryNTimes(1, 1000)) // 重试策略，1 次，间隔 1000 ms
                .connectionTimeoutMs(5000); // 连接超时时间
        String authority = url.getAuthority();
        if (authority != null && authority.length() > 0) {
            builder = builder.authorization("digest", authority.getBytes());
        }
        client = builder.build();
        // 添加连接监听器
        client.getConnectionStateListenable().addListener(new ConnectionStateListener() {
            public void stateChanged(CuratorFramework client, ConnectionState state) {
                if (state == ConnectionState.LOST) {
                    CuratorZookeeperClient.this.stateChanged(StateListener.DISCONNECTED);
                } else if (state == ConnectionState.CONNECTED) {
                    CuratorZookeeperClient.this.stateChanged(StateListener.CONNECTED);
                } else if (state == ConnectionState.RECONNECTED) {
                    CuratorZookeeperClient.this.stateChanged(StateListener.RECONNECTED);
                }
            }
        });
        // 启动 client
        client.start();
    } catch (Exception e) {
        throw new IllegalStateException(e.getMessage(), e);
    }
}
```

---

- 在连接状态发生变化时，调用
#stateChange(state)
方法，进行 StateListener 的回调。

### 3.1.2 create 相关方法

- [#createPersistent(path)](https://github.com/YunaiV/dubbo/blob/414a4799cef08f0b5263d838eeaf8d8f169f2cdc/dubbo-remoting/dubbo-remoting-zookeeper/src/main/java/com/alibaba/dubbo/remoting/zookeeper/curator/CuratorZookeeperClient.java#L72-L79)
- [#createEphemeral(path)](https://github.com/YunaiV/dubbo/blob/414a4799cef08f0b5263d838eeaf8d8f169f2cdc/dubbo-remoting/dubbo-remoting-zookeeper/src/main/java/com/alibaba/dubbo/remoting/zookeeper/curator/CuratorZookeeperClient.java#L81-L88)
- [#checkExists(path)](https://github.com/YunaiV/dubbo/blob/414a4799cef08f0b5263d838eeaf8d8f169f2cdc/dubbo-remoting/dubbo-remoting-zookeeper/src/main/java/com/alibaba/dubbo/remoting/zookeeper/curator/CuratorZookeeperClient.java#L109-L117)

### 3.1.3 ChildListener 相关方法

```java
public CuratorWatcher createTargetChildListener(String path, ChildListener listener) {
    return new CuratorWatcherImpl(listener);
}

public List<String> addTargetChildListener(String path, CuratorWatcher listener) {
    try {
        return client.getChildren().usingWatcher(listener).forPath(path);
    } catch (NoNodeException e) {
        return null;
    } catch (Exception e) {
        throw new IllegalStateException(e.getMessage(), e);
    }
}

public void removeTargetChildListener(String path, CuratorWatcher listener) {
    ((CuratorWatcherImpl) listener).unwatch();
}

private class CuratorWatcherImpl implements CuratorWatcher {

    private volatile ChildListener listener;

    public CuratorWatcherImpl(ChildListener listener) {
        this.listener = listener;
    }

    public void unwatch() {
        this.listener = null;
    }

    @Override
    public void process(WatchedEvent event) throws Exception {
        if (listener != null) {
            String path = event.getPath() == null ? "" : event.getPath();
            listener.childChanged(path,
                    // if path is null, curator using watcher will throw NullPointerException.
                    // if client connect or disconnect to server, zookeeper will queue
                    // watched event(Watcher.Event.EventType.None, .., path = null).
                    StringUtils.isNotEmpty(path)
                            ? client.getChildren().usingWatcher(this).forPath(path) // 重新发起连接，并传入最新的子节点列表
                            : Collections.<String>emptyList()); //
        }
    }
}
```

---

### 3.1.4 close 相关方法

- [#doClose()](https://github.com/YunaiV/dubbo/blob/414a4799cef08f0b5263d838eeaf8d8f169f2cdc/dubbo-remoting/dubbo-remoting-zookeeper/src/main/java/com/alibaba/dubbo/remoting/zookeeper/curator/CuratorZookeeperClient.java#L122-L124)

### 3.1.5 delete

```java
@Override
public void delete(String path) {
    try {
        client.delete().forPath(path);
    } catch (NoNodeException e) {
    } catch (Exception e) {
        throw new IllegalStateException(e.getMessage(), e);
    }
}
```

---

无法通用，所以子类实现。

### 3.1.6 getChildren

```java
@Override
public List<String> getChildren(String path) {
    try {
        return client.getChildren().forPath(path);
    } catch (NoNodeException e) {
        return null;
    } catch (Exception e) {
        throw new IllegalStateException(e.getMessage(), e);
    }
}
```

---

## 3.2 CuratorZookeeperTransporter

com.alibaba.dubbo.remoting.zookeeper.curator.CuratorZookeeperTransporter ，实现 ZookeeperTransporter 接口，CuratorZookeeper 工厂实现类。

```java
public class CuratorZookeeperTransporter implements ZookeeperTransporter {

    public ZookeeperClient connect(URL url) {
        return new CuratorZookeeperClient(url);
    }

}
```

---

# 4. 基于 ZkClient 实现

基于 ZkClient 的实现，本文仅列出标题。感兴趣的胖友，可以自己去看。

当然，良心如笔者，已经添加了中文注释。

## 4.1 ZkclientZookeeperClient

[com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient](https://github.com/YunaiV/dubbo/blob/66a1e1b0ef4b01175be148d27fdcf519f4f01b15/dubbo-remoting/dubbo-remoting-zookeeper/src/main/java/com/alibaba/dubbo/remoting/zookeeper/zkclient/ZkclientZookeeperClient.java)

### 4.1.1 ZkClientWrapper

[com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper](https://github.com/YunaiV/dubbo/blob/66a1e1b0ef4b01175be148d27fdcf519f4f01b15/dubbo-remoting/dubbo-remoting-zookeeper/src/main/java/com/alibaba/dubbo/remoting/zookeeper/zkclient/ZkClientWrapper.java)

## 4.2 ZkclientZookeeperTransporter

[com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperTransporter](https://github.com/YunaiV/dubbo/blob/66a1e1b0ef4b01175be148d27fdcf519f4f01b15/dubbo-remoting/dubbo-remoting-zookeeper/src/main/java/com/alibaba/dubbo/remoting/zookeeper/zkclient/ZkclientZookeeperTransporter.java)

# 666. 彩蛋

![知识星球](/assets/images/learning/dubbo/dubbo-zookeeper-client/96ca62e95e06bbe2fa74153d2158bc13.png)

小文一篇。

发现，即使很简单的文章，例如本文，也要写 3 小时左右。
