---
layout: post
title: 乐观锁重试导致 Lock Wait Timeout
author: deathwhispers
date: 2020-09-30
slug: java-optimistic-lock-retry-lock-wait-timeout-exceeded
categories:
- Java
tags:
- Java
- Concurrency
type: note
status: draft
created: 2020-09-30 12:19
updated: 2020-09-30 12:19
week: 2025-W48
---

# 乐观锁加重试，并发更新数据库一条记录导致：Lock wait timeout exceeded

## 背景：

mysql数据库，用户余额表有一个version（版本号）字段，作为乐观锁。 更新方法有事务控制：
```java
@Transactional(rollbackFor = Exception.class)
```

- 更新时，比对版本号，如果版本号不一致，则更新失败。
- 有重试机制，如果更新失败，则查询最新版本号，再次更新，重试超过5次，报错退出。
- 更新的核心方法：
```java
public boolean updateUserAccount(Long userId, int amount) {
    boolean retryable;
    int attemptNumber = 0;
    do {
        // 查询最新版本号
        UserAccount userAccount = accountMapper.selectByPrimaryKey(userId);
        long oldVersion = userAccount.getVersion();
        // 更新
        boolean success = accountMapper.updateBalance(amount, new Date(), userId, oldVersion) > 0;
        if (success) {
            return true;
        } else {
            attemptNumber++;
            retryable = attemptNumber < 5;
            if (attemptNumber == 5) {
                log.error("超过最大重试次数");
                break;
            }
            try {
                Thread.sleep(300);
            } catch (InterruptedException e) {
                log.error(e);
            }
        }
    } while (retryable);
    return false;
}
```

```sql
UPDATE user_account SET balance = balance - #{amount,jdbcType=INTEGER}, update_time = #{updateTime,jdbcType=TIMESTAMP}, version = #{version,jdbcType=BIGINT} + 1 WHERE balance > #{amount,jdbcType=INTEGER} AND user_id = #{userId,jdbcType=BIGINT} AND version = #{version,jdbcType=BIGINT};
```

在并发更新时，报异常：Lock wait timeout exceeded=

### 分析：

根据日志分析出：

线程a、b几乎同时到达

线程a查询版本号：856

线程a更新数据库：成功

数据库当前版本号：857

线程b查询到的版本号：856（实际已不是最新）

线程b更新数据库：失败

线程b重试，查询版本号：856

线程b更新数据库：失败

。。。

线程b超过重试次数，退出

线程b重试的过程中，又有其他线程到来，比如c，d，e

线程c查询版本号：857

线程c更新数据库：阻塞，因为b拿到锁一直在重试

线程d查询版本号：857

线程d更新数据库：阻塞，因为b拿到锁一直在重试

线程b超次数退出后，c，d，e争抢锁

d拿到锁，更新数据库：成功

数据库当前版本号：858

线程c查询到的版本号：857（实际已不是最新）

线程c更新数据库：失败

线程c重试，查询版本号：857

线程c更新数据库：失败

。。。

线程c超过重试次数，退出

某个事务对应的线程一直抢不到执行的机会，就一直等待。

最后因事务执行时间超过mysql默认的锁等待时间（50s），就会报出：Lock wait timeout exceeded

为什么线程读不到最新的版本号呢？原来是用到了事务，且mysql默认事务隔离级别Repeatable Read，

把隔离级别改为READ_COMMITTED，问题解决。

@Transactional(rollbackFor = Exception.class, isolation = Isolation.READ_COMMITTED)

分析了这么多，解决问题其实只需要一行代码。

**分析一：为什么事务隔离级别Repeatable Read会导致读不到最新版本号呢？**

先来看这样一段话：

consistent read （一致性读），InnoDB用多版本来提供查询数据库在某个时间点的快照。

如果隔离级别是REPEATABLE READ，那么在同一个事务中的所有一致性读 都读的是 事务中第一个这样的读 读到的快照

即：快照读；

如果是READ COMMITTED，那么一个事务中的每一个一致性读 都会读到它自己刷新的快照版本，即：当前读。

这段话就解释清楚了为什么线程B第一次读到版本号856，后面重试时读到的版本号仍然是856。

首先，线程A和B几乎同时到达，都读到了当前数据库版本号856；

线程A抢到了更新MySQL的行锁，将版本号加1更新为857；

线程B在线程A更新数据库的同时，也没闲着，它一直在重试，尝试读到最新版本号，可是直到线程A成功更新完数据库，它也没拿到最新版本号。

原因就在于当前事务隔离级别为REPEATABLE READ。

这个隔离级别会让程序在同一事务中，多次读到的都是相同的数据，也就是保证可重复读。

所以，只要还在这个事务里，无论B怎么重试，它都读不到最新数据。

可以设想一下，如果B重试过程中读到了最新版本号呢？

也就是B一开始读到版本号856，后面重试时读到线程A更新入库的最新版本号857，那么就会导致一个问题——不可重复读。

而这正是REPEATABLE READ要解决的问题。

对于本业务场景来说，READ_COMMITTED虽然会导致不可重复读，但是这里恰好利用了这个特性，可以让线程在事务里不断重试过程中读到其它线程更新的最新的版本号。

这样就避免了线程反复重试，占有CPU资源，以及争抢数据库锁。

**分析二：为什么会Lock wait timeout exceeded异常？**

因为是每个线程到来后，都各自起一个事务。

假设，某个线程C读到的是旧版本号，拿着旧版本号去更新数据库，发现版本号不匹配，更新失败；

然后，进入重试阶段，正常逻辑是 再次尝试读取新版本号，然后再去更新数据库；

然而，实际情况却不是这样，在C再次去更新数据库时被挂起等待，因为此时有其它线程在执行update语句；

不幸的是，其它线程也是反复重试，时间在流逝，终于轮到C执行update，结果仍然由于版本号是旧的，更新失败；

C准备继续重试，因为还没有超过重试最大次数；

不幸又来了，C准备update时，又有其它线程插进来执行update语句；

就这样，C所在的事务消耗的时间越来越久，终于到达了MySQL的极限——崩了！
