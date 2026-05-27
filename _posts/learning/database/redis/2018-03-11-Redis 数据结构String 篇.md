---
layout: post
title: Redis 数据结构：String 篇
slug: redis-string-deep-dive
type:
- note
date: 2018-03-11
tags:
- Redis
- Database
categories:
- Learning
- Database
author: deathwhispers
created: 2019-05-11 11:45
updated: 2023-10-28 22:17
---

Redis 的 String 是最基础的数据类型，也是最常用的类型之一。本文将深入探讨 String 类型的常用命令和应用场景。

> 注意：Redis 命令本身不区分大小写，但 Key 和 Value 是区分大小写的。

### 一、写操作

#### 1. `SET`：设置键值

`SET` 是最基础的写命令，用于将字符串值 `value` 关联到 `key`。

```redis
SET key value [EX seconds] [PX milliseconds] [NX|XX]
```

- 如果 `key` 已存在，`SET` 会覆盖旧值。
- 如果 `key` 不存在，则创建新的键值对。

**可选参数：**

- `EX seconds`：设置键的过期时间（秒）。
- `PX milliseconds`：设置键的过期时间（毫秒）。
- `NX`：仅在键不存在时，才对键进行设置操作。
- `XX`：仅在键已存在时，才对键进行设置操作。

**应用场景：**

- **验证码**：利用 `EX` 设置验证码的有效时间。
  ```redis
  SET phone_number:13800138000 "123456" EX 600
  ```
- **分布式锁**：利用 `NX` 实现“不存在则设置”的原子操作，是实现分布式锁的基础。
  ```redis
  SET lock_key "request_id" NX EX 60
  ```

**示例：**

```redis
redis> SET name "miaoerduo"
OK
redis> GET name
"miaoerduo"

redis> SET name "miao"
OK
redis> GET name
"miao"

redis> SET name "miaoerduo" EX 10
OK
redis> GET name
"miaoerduo"
(等10秒后)
redis> GET name
(nil)

redis> SET name "miaoerduo" NX
(nil)
redis> SET name "new_user" NX
OK
```

#### 2. `MSET` / `MSETNX`：批量设置

- `MSET`：一次性设置多个键值对，如果键已存在则覆盖。此操作是原子的。
- `MSETNX`：一次性设置多个键值对，但仅当所有给定的键都不存在时才执行。此操作也是原子的。

**示例：**

```redis
redis> MSET name1 "miaoerduo" name2 "miao"
OK
redis> GET name1
"miaoerduo"

redis> MSETNX name2 "new_value" name3 "love"
(integer) 0
redis> GET name3
(nil)
```

#### 3. `SETRANGE`：覆盖字符串的一部分

从指定的 `offset` 开始，用 `value` 覆盖 `key` 所储存的字符串值。

```redis
SETRANGE key offset value
```

- 如果 `offset` 超出原字符串长度，会自动用空字节 (`\x00`) 填充。

**示例：**

```redis
redis> SET str "hello world"
OK
redis> SETRANGE str 6 "redis"
(integer) 11
redis> GET str
"hello redis"

redis> SETRANGE str 15 "aha"
(integer) 18
redis> GET str
"hello redis\x00\x00\x00\x00aha"
```

#### 4. `APPEND`：追加值

如果 `key` 已经存在并且是一个字符串，`APPEND` 命令将 `value` 追加到 `key` 原来的值的末尾。

**示例：**

```redis
redis> SET str "hello"
OK
redis> APPEND str " world"
(integer) 11
redis> GET str
"hello world"
```

### 二、读操作

#### 1. `GET`：获取键值

获取指定 `key` 的值。如果 `key` 不存在，返回 `nil`。如果 `key` 储存的值不是字符串类型，返回一个错误。

#### 2. `MGET`：批量获取

一次性获取多个 `key` 的值。如果某个 `key` 不存在，则对应的返回值为 `nil`。`MGET` 是一个原子操作，且能有效减少网络开销。

**示例：**

```redis
redis> MSET key1 "a" key2 "b"
OK
redis> MGET key1 key2 key3
1) "a"
2) "b"
3) (nil)
```

#### 3. `GETRANGE`：获取子字符串

获取 `key` 所储存的字符串值的子字符串。`start` 和 `end` 是以 0 为基础的下标，支持负数（-1 表示最后一个字符）。

**示例：**

```redis
redis> SET str "hello world"
OK
redis> GETRANGE str 0 4
"hello"
redis> GETRANGE str 6 -1
"world"
```

#### 4. `GETSET`：设置新值并返回旧值

将 `key` 的值设为 `value` ，并返回 `key` 的旧值。这是一个原子操作。

**应用场景：**

- **重置计数器**：与 `INCR` 配合，可以原子地获取并重置计数器。
  ```redis
  GETSET my_counter 0
  ```

**示例：**

```redis
redis> SET str "hello"
OK
redis> GETSET str "world"
"hello"
redis> GET str
"world"
```

#### 5. `STRLEN`：获取字符串长度

返回 `key` 所储存的字符串值的长度。如果 `key` 不存在，返回 0。

### 三、数值操作（原子）

Redis 的 `INCR` 系列命令支持对字符串表示的整数和浮点数进行原子性的增减操作。

#### 1. `INCR` / `DECR`：加一/减一

- `INCR key`：将 `key` 中储存的数字值增一。
- `DECR key`：将 `key` 中储存的数字值减一。

如果 `key` 不存在，那么 `key` 的值会先被初始化为 `0`，然后再执行操作。

**应用场景：**

- **原子计数器**：网站的访问量、文章的点赞数等。

**示例：**

```redis
redis> SET count 10
OK
redis> INCR count
(integer) 11
redis> DECR count
(integer) 10
```

#### 2. `INCRBY` / `DECRBY`：增加/减少指定整数

- `INCRBY key increment`：将 `key` 所储存的值加上给定的增量 `increment`。
- `DECRBY key decrement`：将 `key` 所储存的值减去给定的减量 `decrement`。

#### 3. `INCRBYFLOAT`：增加指定浮点数

将 `key` 所储存的值加上给定的浮点数增量。要实现减法，只需传入一个负数。

**示例：**

```redis
redis> SET a 1.5
OK
redis> INCRBYFLOAT a 10.1
"11.6"
redis> INCRBYFLOAT a -1.5
"10.1"
```

### 四、位操作

位操作允许将字符串看作一个位数组，并对位进行操作。

#### 1. `SETBIT` / `GETBIT`：设置/获取位

- `SETBIT key offset value`：对 `key` 所储存的字符串值，设置或清除指定偏移量上的位 (`value` 只能是 0 或 1)。
- `GETBIT key offset`：获取指定偏移量上的位。

**应用场景：**

- **用户在线状态**：用一个位表示一个用户ID，`1` 为在线，`0` 为离线。
- **用户签到统计**：用一个月的天数作为位数，记录用户每天是否签到。

**示例：**

```redis
redis> SETBIT user:online:2023-10-28 10086 1
(integer) 0
redis> GETBIT user:online:2023-10-28 10086
(integer) 1
```

#### 2. `BITCOUNT`：统计置位的数量

计算给定字符串中，被设置为 `1` 的比特位的数量。

**示例：**

```redis
redis> SET mykey "foobar"
OK
redis> BITCOUNT mykey
(integer) 26
```

#### 3. `BITOP`：位运算

对一个或多个保存二进制位的字符串 `key` 进行位元操作，并将结果保存到 `destkey`。

```redis
BITOP operation destkey key [key ...]
```

- `operation` 可以是 `AND`、`OR`、`XOR`、`NOT`。

**应用场景：**

- **计算活跃用户**：对每天的用户在线记录进行 `OR` 运算，可以得到某段时间内的总活跃用户数。

#### 4. `BITPOS`：查找第一个置位/未置位

返回字符串中第一个被设置为 `0` 或 `1` 的比特位的位置。

**示例：**

```redis
redis> SET bits "\xff\xf0\x00"
OK
redis> BITPOS bits 0
(integer) 12

![](assets/images/learning/database/redis/redis-string-deep-dive/copycode.gif)

1 redis> set count 02OK

3 redis> incr count

4 (integer) 15 redis> incr count

6 (integer) 27 redis> del count

8 (integer) 19 redis> getcount

10(nil)

11 redis> incr count

12 (integer) 113 redis> incr count

14 (integer) 2

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

值得注意的是，该操作是原子操作，即使有多个请求传输到Redis，count执行的结果都不会错误，所以我们可以大胆放心的用这个功能实现多线程的计数功能。

**4，DECR key**

Decrement the integer value of a key by one

对存储在key的整数值进行原子的减1操作。

注意事项和INCR一样。

**5，INCRBY key increment**

Increment the integer value of a key by the given amount

对存储在key的整数值进行原子的加操作，加increment。

如果key不存在，操作之前，key就会被置为0。如果key的value类型错误或者是个不能表示成数字的字符串，就返回错误。这个操作最多支持64位有符号的整型数字。基本上和INCR一样。

**6，DECRBY key decrement**

Decrement the integer value of a key by the given number

对存储在key的整数值进行原子的减操作，减increment。

其他和INCR一样。

**7，INCRBYFLOAT key increment**

Increment the float value of a key by the given amount

对存储造key中的浮点数进行原子的加操作，加increment。

如果key不存在，操作之前，key就会被置为0。如果key的value类型错误或者是个不能表示成浮点数的字符串，就返回错误。

我们并没有DECRBYFLOAT这个操作，因此想要实现减操作，只需要把increment设成负的就可以。

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

1 redis> set a 1.52OK

3 redis> incrbyfloat a 10.14“11.6”5 redis> incrbyfloat a 10.16“21.7”7 redis> incrbyfloat a -10.18“11.6”9 redis> incrbyfloat a -1.5e210“-138.39999999999999999”

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

浮点数可以用一般的小数和科学计数法表示。

### **四、二进制操作**

**1，SETBIT key offset value**

Sets or clears the bit at offset in the string value stored at key

设置或者清空key的value(字符串)在offset处的bit值。这里将string看成由bit组成的数组。

指定位置的bit可以被设置，或者被清空，这个由value（只能是0或者1）来决定。当key不存在的时候，就创建一个新的字符串value。要确保这个字符串足够长到在offset处有bit值。参数offset需要大于等于0，并且小于2^32(限制bitmap大小为512)。当key对应的字符串增大的时候，新增的部分bit值都是设置为0。

该操作返回value原来的offset位置的bit值。

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

1 redis> setbit a 012 (integer) 03 redis> setbit a 114 (integer) 05 redis> setbit a 216 (integer) 07 redis> setbit a 318 (integer) 09 redis> geta

10“”

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

a最开始不存在，使用setbit操作，将a的前4位都设置成1。最终就得到了，这是16进制表示的结果，前4位都是1，其他都是0。

**2，GETBIT key offset**

Returns the bit value at offset in the string value stored at key

获取key对应的string在offset处的bit值。当offset超出了字符串长度的时候，这个字符串就被假定为由0比特填充的连续空间。当key不存在的时候，它就认为是一个空字符串，所以offset总是超出范围，然后value也被认为是由0比特填充的连续空间。

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

1redis> setbit a712(integer)03redis> getbit a04(integer)05redis> getbit a76(integer)17redis> getbit a1008(integer)0

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

**3，BITCOUNT key [start end]**

Count set bits in a string

统计key的string的二进制中1的个数。

start和end分别表示string的起始和结束位置，含义和GETRANGE中一样。

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

1 redis> setbit mykey 012 (integer) 03 redis> setbit mykey 1014 (integer) 05 redis> setbit mykey 516 (integer) 07 redis> bitcount mykey

8 (integer) 3

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

**4，BITOP operation destkey key [key …]**

Perform bitwise operations between strings

对string进行bit级别的操作。具体操作有4种。AND，OR，XOR，NOT。

用法如下：

BITOP AND destkey srckey1 srckey2 srckey3 … srckeyN

BITOP OR destkey srckey1 srckey2 srckey3 … srckeyN

BITOP XOR destkey srckey1 srckey2 srckey3 … srckeyN

BITOP NOT destkey srckey

NOT操作后面只有一个目标key和srckey，是因为NOT操作是一元的。

对于AND，OR和XOR操作，Redis会将srckey1，srckey2，…，srckeyN这些字符串对位进行相关操作，之后将结果存入destkey中。

如果srckey的length不相等的话，Redis内部会将短的字符串补齐，并填充上0。

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

1 redis> set key1 “”2OK

3 redis> set key2 “0f0f”4OK

5 redis> set key3 “”6OK

7 redis> bitop and destkey key1 key2 key3

8 (integer) 29 redis> getdestkey

10“”11 redis> bitop or destkey key1 key2 key3

12 (integer) 213 redis> getdestkey

14“”15 redis> bitop xor destkey key1 key2 key3

16 (integer) 217 redis> getdestkey

18“”19 redis> bitop not destkey key1

20 (integer) 221 redis> getdestkey

22“0f0f”

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

**5，BITPOS key bit [start] [end]**

Find first bit set or clear in a string

返回string的二进制中第一个0或1的位置。

这里将string看成一个有许多bit组成的数组。其中start和end表示string的一个间隔，如果指定了start和end，则BITPOS只会查询这个区间。注意，start和end表示的字符的位置，不是bit的位置。

即使指定了start和end，BITPOS这个操作也只会这个目标bit的绝对地址。

有几点需要注意：

在没有指定查询区间或只指定start的时候，查询bit位为0的位置时，如果string中没有该位，则会返回string的bit位的总数。比如在0的位置，Redis默认该字符串后面都是0，因此，返回的结果就是12（下标从0开始数的）。

如果指定了查询区间，无论查询0或是1，在没查询到的时候只会返回-1。

在没有指定查询区间时，查询bit位为1的位置时，如果string中没有该位，则会返回-1，表示未查询到。

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

redis> set bits “”

OK

redis> strlen bits

(integer)4

redis> bitpos bits 0

(integer)0

redis> bitpos bits 1

(integer)8

redis> bitpos bits 01

(integer)16

redis> bitpos bits 01 -1

(integer)16

redis> bitpos bits 11 -1

(integer)8

redis> bitpos bits 03

(integer)32

redis> bitpos bits 033

(integer) -1

![](assets/images/learning/database/redis/redis-String篇/copycode.gif)

看上面的例子，bits的初始设置的二进制表示为：

00000000 11111111 00000000 11111111

直接获取0（bitpos bits 0）的位置为0，获取1（bitpos bits 1）的位置为8。

指定开始位置为1（start = 1）的时候，0第一次出现（bitpos bits 1）的位置为16。

指定起始位置为3（start = 3）的时候，0第一次出现（bitpos bits 0 3）的位置为32。这是因为Redis在查询字符串的时候查询到了字符串的末尾，之后默认末尾的后面都是0，因此得到了32这的个位置。

最后，当指定必须在第3个字节（从0开始数）查询0的时候，由于查不到0，因此只返回了-1。

这篇博客的内容，小喵自己也感觉有点多，每个指令小喵都是参考了官方的文档，然后都自己动手做了实验，再加入了自己的一点理解。可能有些地方，小喵没有理解的很好，这时就需要大家多多指教了。
