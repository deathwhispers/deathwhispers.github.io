---
layout: post
title: JetLinks ReactorQL
slug: jetlinks-reactorql
type:
- note
date: 2023-05-28
status: draft
tags:
- IoT
- JetLinks
categories:
- IoT
- JetLinks
mood: null
weather: null
author: deathwhispers
created: 2023-05-28 11:45
updated: 2023-05-28 18:33
---

# ReactorQL

# ReactorQL

- <u>ReactorQL</u>
    - <u>场景</u>
    - <u>SQL例子</u>
    - <u>SQL支持列表</u>
    - <u>拓展函数</u>
        - <u>device.properties</u>
        - <u>device.properties.history</u>
        - <u>device.properties.latest</u>
        - <u>device.tags</u>
        - <u>device.selector</u>
        - <u>mqtt.client.publish</u>
        - <u>mqtt.client.subscribe</u>
        - <u>http.request</u>
        - <u>message.subscribe</u>
        - <u>message.publish</u>

JetLinks封装了一套使用SQL来进行实时数据处理的工具包[查看源代码 (opens new window)](https://github.com/jetlinks/reactor-ql)。 通过将SQL翻译为[reactor (opens new window)](https://projectreactor.io/)来进行数据处理。 规则引擎中的数据转发以及可视化规则中的ReactorQL节点均使用此工具包实现。 默认情况下,SQL中的表名就是事件总线中的topic,如: select * from “/device/*/*/message/property/*“*, 表示订阅/device//*/message/property/*下的实时消息.

## 场景

1. 处理实时数据
2. 聚合计算实时数据
3. 跨数据源联合数据处理

## SQL例子

TIP

聚合处理实时数据时,必须使用interval函数或者_window函数.

当温度大于40度时,将数据转发到下一步.

```plain text
select
this.properties.temperature temperature,
this.deviceId deviceId
from
"/device/*/*/message/property/**" -- 订阅所有设备的所有属性消息
where this.properties.temperature > 40
```

处理指定多个型号的设备数据

```plain text
select * from (
    select
        this.properties.temperature temperature,
        this.deviceId deviceId
    from
        "/device/T0001/*/message/property/**" -- 订阅T0001型号下的所有设备消息
    where this.properties.temperature > 40
union all   -- 实时数据只能使用 union all
    select
        this.properties.temperature temperature,
        this.deviceId deviceId
    from
        "/device/T0002/*/message/property/**" -- 订阅T0002型号下的所有设备消息
    where this.properties.temperature > 42
)
```

计算每5分钟的温度平均值,当平均温度大于40度时,将数据转发到下一步.

```plain text
select
avg(this.properties.temperature) temperature
from
"/device/*/*/message/property/**" -- 订阅所有设备的所有属性消息
group by interval('5m')
having temperature > 40 --having 必须使用别名.
```

计算每10条数据为一个窗口,每2条数据滚动的平均值.

```plain text
[1,2,3,4,5,6,7,8,9,10]  第一组
[3,4,5,6,7,8,9,10,11,12] 第二组
[5,6,7,8,9,10,11,12,13,14] 第三组
```

```plain text
select
avg(this.properties.temperature) temperature
from
"/device/*/*/message/property/**" -- 订阅所有设备的所有属性消息
group by _window(10,2)
having temperature > 40 --having 必须使用别名.
```

聚合统计平均值,并且提取聚合结果中的数据.

```plain text
select
rows_to_array(idList) deviceIdList, --将[{deviceId:1},{deviceId:2}] 转为[1,2]
avgTemp,
from
(
   select
   collect_list((select this.deviceId deviceId)) idList, --聚合结果里的
   avg(temperature)                   avgTemp ,
   from "/device/*/*/message/property/**" ,
   group by interval('1m') having avgTemp > 40
)
```

5分钟之内只取第一次。

```plain text
select *
from "/device/*/*/message/event/fire_alarm"
_window('5m'),take(1) -- -1为取最后一次
```

限流: 10秒内超过2次则获取最后一条数据

```plain text
select * from
( select * from "/device/demo-device/device001/message/event/alarm" )
group by
_window('10s') --时间窗口
,trace() -- 跟踪分组内行号信息
,take(-1) --取最后一条数据
having
  row.index > 2  -- 跟踪分组内的行号
and
  row.elapsed>1000 -- 距离上一行的时间
```

注意

SQL中的this表示主表当前的数据,如果存在嵌套属性的时候,必须指定this或者以表别名开头. 如: this.properties.temperature ,写成: properties.temperature是无法获取到值到.

## SQL支持列表

| 函数/表达式 | 用途 | 示例 | 说明 |
| --- | --- | --- | --- |
| + | 加法运算 | temp+10 | 对应函数: math.plus(temp,10) |
| - | 减法运算 | temp-10 | 对应函数: math.sub(temp,10) |
| * | 乘法运算 | temp*10 | 对应函数: math.mul(temp,10) |
| / | 除法运算 | temp/10 | 对应函数: math.divi(temp,10) |
| % | 取模运算 | temp%2 | 对应函数: math.mod(temp,2) |
| & | 位与运算 | val&3 | 对应函数: bit_and(val,3) |
|   |   | 位或运算 | val |
| ^ | 异或运算 | val^3 | 对应函数: bit_mutex(val,3) |
| << | 位左移运算 | val<<2 | 对应函数: bit_left_shift(val,2) |
| >> | 位右移运算 | val>>2 | 对应函数: bit_right_shift(val,2) |
|   |   |   | 字符拼接 |
| avg | 平均值 | avg(val) | 聚合函数,平均值 |
| sum | 合计值 | sum(val) | 聚合函数,合计值 |
| count | 总数 | count(1) | 聚合函数,计数 |
| max | 最大值 | max(val) | 聚合函数,最大值 |
| min | 最小值 | min(val) | 聚合函数,最小值 |
| take | 取指定数量数据 | take(5,-1) –取5个中的最后一个 | 通常配合分组函数_window使用 |
| > | 大于 | val > 10 |   |
| < | 小于 | val < 10 |   |
| = | 等于 | val = 10 |   |
| != | 不等于 | val !=10 | 等同于: <> ,如: val <> 10 |
| >= | 大于等于 | val>=10 |   |
| <= | 小于等于 | val<=10 |   |
| in | 在..之中 | val in (1,2,3) |   |
| not in | 不在..之中 | val not in (1,2,3) |   |
| like | 模糊匹配 | name like ‘a%’ | not like 同理 |
| between | 在之间 | val between 1 and 10 |   |
| now | 当前时间 | now() | 默认返回时间戳,可传入格式化参数. |
| date_format | 格式化日期 | date_format(now(),‘yyyy-MM-dd’) |   |
| cast | 转换类型 | cast(val as boolean) | 支持类型: string,boolean,int,double,float,date,decimal,long |
| interval | 时间分组 | interval(‘10s’) | 分组函数,按时间分组 |
| _window | 窗口分组 | _window(10) | 窗口,支持按数量和时间窗口 |
| collect_list | 聚合结果转为list | collect_list((select deviceId)) | 把聚合的的结果转为list |
| rows_to_array | 将结果集转为单元素数组 | rows_to_array(idList) | 把只有一个属性的结果集中的属性转为集合 |
| new_map | 创建一个map | new_map(‘k1’,v1,‘k2’,v2) |   |
| new_array | 创建一个集合 | new_array(1,2,3,4) |   |
| math.ceil | 向上取整 | math.ceil(val) |   |
| math.floor | 向下取整 | math.floor(val) |   |
| math.round | 四舍五入 | math.round(val) |   |
| math.log | log运算 | math.log(val) |   |
| math.sin | 正弦 | math.sin(val) |   |
| math.asin | 反正弦 | math.asin(val) |   |
| math.sinh | 双曲正弦 | math.sinh(val) |   |
| math.cos | 余弦 | math.cos(val) |   |
| math.acos | 反余弦 | math.acos(val) |   |
| math.cosh | 双曲余弦 | math.cosh(val) |   |
| math.tan | 正切 | math.tan(val) |   |
| math.atan | 反正切 | math.atan(val) |   |
| math.tanh | 双曲正切 | math.tanh(val) |   |
| if | 条件取值 | if(a<1,‘when true’,‘when false’) |   |
| range | 范围判断,等同于between and | range(val,1,10) |   |
| median | 中位数 | median(val) | 中位数 (Pro) |
| skewness | 偏度特征值 | skewness(val) | 偏度特征值聚合函数 (Pro) |
| kurtosis | 峰度特征值 | kurtosis(val) | 峰度特征值聚合函数 (Pro) |
| variance | 方差 | variance(val) | 方差聚合函数 (Pro) |
| geo_mean | 几何平均数 | geo_mean(val) | 几何平均数聚合函数 (Pro) |
| sum_of_squ | 平方和 | sum_of_squ(val) | 平方和聚合函数 (Pro) |
| std_dev | 标准差 | std_dev(val) | 标准差聚合函数 (Pro) |
| slope | 斜度 | slope(val) | 使用最小二乘回归模型计算斜度,大于0为向上,小于0为向下 (Pro) |
| time | 转换时间 | time(‘now-1d’) | 使用表达式来转换时间,返回毫秒时间戳(Pro) |
| jsonata | jsonata表达式 | jsonata(‘$abs(val)’) | 使用jsonata表达式来提取行数据(Pro) |
| spel | spel表达式 | spel(‘#val’) | 使用spel表达式来提取行数据(Pro) |
| env | 获取配置信息 | env(‘key’,‘默认值’) | 获取系统配置信息(Pro) |
| _window_until | 打开窗口直到满足条件 | _window_until(this.success) | 打开窗口直到满足条件(Pro) |
| _window_until_change | 打开窗口直到值变更 | _window_until_change(this.state) | 打开窗口直到值变更(Pro) |

## 拓展函数

TIP

以下功能只在企业版中支持

### device.properties

获取设备已保存的全部最新属性,(注意: 由于使用es存储设备数据,此数据并不是完全实时的)

```plain text
select
device.properties(this.deviceId) props,
this.properties reports
from "/device/*/*/message/property/report"
```

TIP

device.properties(this.deviceId,‘property1’,‘property2’)还可以通过参数获取指定的属性，如果未设置则获取全部属性。

### device.properties.history

查询设备历史数据

```plain text
--聚合查询
select * from device.properties.history(
   select avg(temperature) avgVal
   from "deviceId" -- from 支持: 按设备ID查询: "deviceId", 查询多个设备: device('1','2') 按产品查询: product('id')
   where timestamp between now()-86400000 and now()
)
```

```plain text
--按时间分组
select * from device.properties.history(
    select avg(temperature) avgVal
    from "deviceId"
    where timestamp between now()-86400000 and now()
    group by interval('1d')
)
```

```plain text
-- 订阅实时数据,然后查询对应设备的历史数据
select
(
select maxVal,avgVal from
    device.properties.history(
        select
        max(temp3) maxVal,
        avg(temp3) avgVal
        from device(t.deviceId)
        -- 前一天的数据
        where timestamp between time('now-1d') and t.timestamp
    )
) $this,
t.properties.temp3 temp3
from "/device/*/*/message/property/**" t
```

### device.properties.latest

TIP

此功能需要开启[设备最新数据存储](http://doc.jetlinks.cn/best-practices/start.html#%E8%AE%B0%E5%BD%95%E8%AE%BE%E5%A4%87%E6%9C%80%E6%96%B0%E6%95%B0%E6%8D%AE%E5%88%B0%E6%95%B0%E6%8D%AE%E5%BA%93)

查询设备最新的数据

```plain text
select * from device.properties.latest(
    select
    temperature
    from "productId" --表名为产品ID
    where id = 'deviceId' -- id则为设备ID
)
```

聚合查询

```plain text
select * from device.properties.latest(
    select
    avg(temperature) temperature
    from "productId" --表名为产品ID
)
```

### device.tags

获取设备标签信息

```plain text
select device.tags(this.deviceId) from "/device/*/*/message/property/report"
```

TIP

device.tags(this.deviceId,‘tag1’,‘tag2’)还可以通过参数获取指定的标签，如果未设置则获取全部标签。

### device.selector

选择设备,如：

```plain text
select dev.deviceId from "/device/*/*/message/property/report" t
-- 获取和上报属性在同一个分组里，并且产品id为light-product的设备
left join (
            select this.id deviceId from
            device.selector(same_group(t.deviceId),product('light-product'))
          ) dev
```

支持参数:

4. in_gourp(‘groupId’) 在指定的设备分组中
5. in_group_tree(‘groupId’) 在指定分组中（包含下级分组）
6. same_group(‘deviceId’) 在指定设备的相同分组中
7. product(‘productId’) 指定产品ID对应的设备
8. tag(‘tag1Key’,‘tag1Value’,‘tag2Key’,‘tag2Value’) 按指定的标签获取
9. state(‘online’) 按指定的状态获取
10. in_tenant(‘租户ID’) 在指定租户中的设备
11. org(‘机构ID’) 在指定机构中

### mqtt.client.publish

推送消息到mqtt客户端.

```plain text
select
mqtt.client.publish(
   'networkId' -- 第一个参数: 网络组件中mqtt客户端的ID
   ,'topic' -- 第二个参数: topic
   ,'JSON'  -- 第三个参数: 消息类型: JSON,STRING,BINARY,HEX
   ,this  -- 消息体,会根据消息类型转为不同格式的消息
   ) publishSuccess -- 返回推送结果 true false
from "/rule-engine/device/alarm/sensor-1/**"
```

### mqtt.client.subscribe

从mqtt客户端订阅消息

```plain text
select
t.did deviceId,
t.l location,
t.v value
from mqtt.client.subscribe(
   'networkId' -- 第一个参数: 网络组件中mqtt客户端的ID
   ,'JSON' -- 第二个参数: 消息类型: JSON,STRING,BINARY,HEX
   ,'topic' -- topic
   ,'topic2' -- topic2
) t
where t.v > 30 -- 过滤条件
```

### http.request

发起http请求

```plain text
select

http.request(
   'networkId' -- 第一个参数: 网络组件中http客户端的ID
   -- 下面的参数两两对应组成键值对,注意: 使用逗号(,)分割.
   ,'url','https://www.baidu.com'
   ,'method','POST'
   ,'contentType','application/json'
   -- 请求头
   ,'headers',new_map('key1','value1','key2','value2')
   -- body参数在contentType为application/json时生效
   ,'body',new_map('key1','value1','key2','value2')
   -- requestParam参数在contentType不为json时生效,相当于:application/x-www-form-urlencoded的处理方式
   ,'requestParam',new_map('key1','value1','key2','value2')
   -- 直接拼接到url上的参数 https://www.baidu.com?key1=value1&key2=value2
   ,'queryParameters',new_map('key1','value1','key2','value2')

) response

from dual
```

### message.subscribe

订阅消息网关中的消息

```plain text
select
t.topic topic,
t.message.deviceId deviceId,
t.message.headers.productId productId,
t.message.timestamp ts
from message.subscribe(
   'false' -- 是否订阅来自集群的消息(可选参数,默认为false)
   ,'/device/*/*/online'
   )  t
```

### message.publish

推送消息到消息网关

```plain text
select

message.publish(
   '/device-online/'||t.message.deviceId -- 推送到此topic
   ,t.message -- 消息内容
   ) subscribeNumber -- 返回有多少订阅者收到了消息

from message.subscribe('/device/*/*/online')  t
```

%23%20ReactorQL%0A%0A%5Btoc%5D%0A%0AJetLinks%E5%B0%81%E8%A3%85%E4%BA%86%E4%B8%80%E5%A5%97%E4%BD%BF%E7%94%A8SQL%E6%9D%A5%E8%BF%9B%E8%A1%8C%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E7%9A%84%E5%B7%A5%E5%85%B7%E5%8C%85%5B%E6%9F%A5%E7%9C%8B%E6%BA%90%E4%BB%A3%E7%A0%81%20(opens%20new%20window)%5D(https%3A%2F%2Fgithub.com%2Fjetlinks%2Freactor-ql)%E3%80%82%20%E9%80%9A%E8%BF%87%E5%B0%86SQL%E7%BF%BB%E8%AF%91%E4%B8%BA%5Breactor%20(opens%20new%20window)%5D(https%3A%2F%2Fprojectreactor.io%2F)%E6%9D%A5%E8%BF%9B%E8%A1%8C%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E3%80%82%20%E8%A7%84%E5%88%99%E5%BC%95%E6%93%8E%E4%B8%AD%E7%9A%84%60%E6%95%B0%E6%8D%AE%E8%BD%AC%E5%8F%91%60%E4%BB%A5%E5%8F%8A%E5%8F%AF%E8%A7%86%E5%8C%96%E8%A7%84%E5%88%99%E4%B8%AD%E7%9A%84%60ReactorQL%E8%8A%82%E7%82%B9%60%E5%9D%87%E4%BD%BF%E7%94%A8%E6%AD%A4%E5%B7%A5%E5%85%B7%E5%8C%85%E5%AE%9E%E7%8E%B0%E3%80%82%20%E9%BB%98%E8%AE%A4%E6%83%85%E5%86%B5%E4%B8%8B%2CSQL%E4%B8%AD%E7%9A%84%E8%A1%A8%E5%90%8D%E5%B0%B1%E6%98%AF%E4%BA%8B%E4%BB%B6%E6%80%BB%E7%BA%BF%E4%B8%AD%E7%9A%84%60topic%60%2C%E5%A6%82%3A%20%60select%20*%20from%20%22%2Fdevice%2F*%2F*%2Fmessage%2Fproperty%2F*%22%60%2C%20%E8%A1%A8%E7%A4%BA%E8%AE%A2%E9%98%85%60%2Fdevice%2F*%2F*%2Fmessage%2Fproperty%2F*%60%E4%B8%8B%E7%9A%84%E5%AE%9E%E6%97%B6%E6%B6%88%E6%81%AF.%0A%0A%23%23%20%E5%9C%BA%E6%99%AF%0A%0A1.%20%E5%A4%84%E7%90%86%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE%0A2.%20%E8%81%9A%E5%90%88%E8%AE%A1%E7%AE%97%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE%0A3.%20%E8%B7%A8%E6%95%B0%E6%8D%AE%E6%BA%90%E8%81%94%E5%90%88%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%0A%0A%23%23%20SQL%E4%BE%8B%E5%AD%90%0A%0ATIP%0A%0A%E8%81%9A%E5%90%88%E5%A4%84%E7%90%86%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE%E6%97%B6%2C%E5%BF%85%E9%A1%BB%E4%BD%BF%E7%94%A8%60interval%60%E5%87%BD%E6%95%B0%E6%88%96%E8%80%85%60_window%60%E5%87%BD%E6%95%B0.%0A%0A%E5%BD%93%E6%B8%A9%E5%BA%A6%E5%A4%A7%E4%BA%8E40%E5%BA%A6%E6%97%B6%2C%E5%B0%86%E6%95%B0%E6%8D%AE%E8%BD%AC%E5%8F%91%E5%88%B0%E4%B8%8B%E4%B8%80%E6%AD%A5.%0A%0A%60%60%60sql%0Aselect%20%0Athis.properties.temperature%20temperature%2C%0Athis.deviceId%20deviceId%0Afrom%0A%22%2Fdevice%2F*%2F*%2Fmessage%2Fproperty%2F****%22%20–%20%E8%AE%A2%E9%98%85%E6%89%80%E6%9C%89%E8%AE%BE%E5%A4%87%E7%9A%84%E6%89%80%E6%9C%89%E5%B1%9E%E6%80%A7%E6%B6%88%E6%81%AF%0Awhere%20this.properties.temperature%20%3E%2040%0A%60%60%60%0A%0A%E5%A4%84%E7%90%86%E6%8C%87%E5%AE%9A%E5%A4%9A%E4%B8%AA%E5%9E%8B%E5%8F%B7%E7%9A%84%E8%AE%BE%E5%A4%87%E6%95%B0%E6%8D%AE%0A%0A%60%60%60sql%0Aselect%20%20from%20(%0A%20%20%20%20select%20%0A%20%20%20%20%20%20%20%20this.properties.temperature%20temperature%2C%0A%20%20%20%20%20%20%20%20this.deviceId%20deviceId%0A%20%20%20%20from%0A%20%20%20%20%20%20%20%20%22%2Fdevice%2FT0001%2F%2Fmessage%2Fproperty%2F****%22%20–%20%E8%AE%A2%E9%98%85T0001%E5%9E%8B%E5%8F%B7%E4%B8%8B%E7%9A%84%E6%89%80%E6%9C%89%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%0A%20%20%20%20where%20this.properties.temperature%20%3E%2040%0Aunion%20all%20%20%20–%20%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE%E5%8F%AA%E8%83%BD%E4%BD%BF%E7%94%A8%20union%20all%0A%20%20%20%20select%20%0A%20%20%20%20%20%20%20%20this.properties.temperature%20temperature%2C%0A%20%20%20%20%20%20%20%20this.deviceId%20deviceId%0A%20%20%20%20from%0A%20%20%20%20%20%20%20%20%22%2Fdevice%2FT0002%2F*%2Fmessage%2Fproperty%2F**%22%20–%20%E8%AE%A2%E9%98%85T0002%E5%9E%8B%E5%8F%B7%E4%B8%8B%E7%9A%84%E6%89%80%E6%9C%89%E8%AE%BE%E5%A4%87%E6%B6%88%E6%81%AF%0A%20%20%20%20where%20this.properties.temperature%20%3E%2042%0A)%0A%60%60%60%0A%0A%E8%AE%A1%E7%AE%97%E6%AF%8F5%E5%88%86%E9%92%9F%E7%9A%84%E6%B8%A9%E5%BA%A6%E5%B9%B3%E5%9D%87%E5%80%BC%2C%E5%BD%93%E5%B9%B3%E5%9D%87%E6%B8%A9%E5%BA%A6%E5%A4%A7%E4%BA%8E40%E5%BA%A6%E6%97%B6%2C%E5%B0%86%E6%95%B0%E6%8D%AE%E8%BD%AC%E5%8F%91%E5%88%B0%E4%B8%8B%E4%B8%80%E6%AD%A5.%0A%0A%60%60%60sql%0Aselect%0Aavg(this.properties.temperature)%20temperature%0Afrom%0A%22%2Fdevice%2F*****%2F*****%2Fmessage%2Fproperty%2F**%22%20–%20%E8%AE%A2%E9%98%85%E6%89%80%E6%9C%89%E8%AE%BE%E5%A4%87%E7%9A%84%E6%89%80%E6%9C%89%E5%B1%9E%E6%80%A7%E6%B6%88%E6%81%AF%0Agroup%20by%20interval(‘5m’)%0Ahaving%20temperature%20%3E%2040%20–having%20%E5%BF%85%E9%A1%BB%E4%BD%BF%E7%94%A8%E5%88%AB%E5%90%8D.%0A%60%60%60%0A%0A%E8%AE%A1%E7%AE%97%E6%AF%8F10%E6%9D%A1%E6%95%B0%E6%8D%AE%E4%B8%BA%E4%B8%80%E4%B8%AA%E7%AA%97%E5%8F%A3%2C%E6%AF%8F2%E6%9D%A1%E6%95%B0%E6%8D%AE%E6%BB%9A%E5%8A%A8%E7%9A%84%E5%B9%B3%E5%9D%87%E5%80%BC.%0A%0A%60%60%60tex%0A%5B1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%5D%20%20%E7%AC%AC%E4%B8%80%E7%BB%84%0A%5B3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%5D%20%E7%AC%AC%E4%BA%8C%E7%BB%84%0A%5B5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%5D%20%E7%AC%AC%E4%B8%89%E7%BB%84%0A%60%60%60%0A%0A%60%60%60sql%0Aselect%20%0Aavg(this.properties.temperature)%20temperature%0Afrom%0A%22%2Fdevice%2F*%2F*%2Fmessage%2Fproperty%2F**%22%20–%20%E8%AE%A2%E9%98%85%E6%89%80%E6%9C%89%E8%AE%BE%E5%A4%87%E7%9A%84%E6%89%80%E6%9C%89%E5%B1%9E%E6%80%A7%E6%B6%88%E6%81%AF%0Agroup%20by%20_window(10%2C2)%0Ahaving%20temperature%20%3E%2040%20–having%20%E5%BF%85%E9%A1%BB%E4%BD%BF%E7%94%A8%E5%88%AB%E5%90%8D.%0A%60%60%60%0A%0A%E8%81%9A%E5%90%88%E7%BB%9F%E8%AE%A1%E5%B9%B3%E5%9D%87%E5%80%BC%2C%E5%B9%B6%E4%B8%94%E6%8F%90%E5%8F%96%E8%81%9A%E5%90%88%E7%BB%93%E6%9E%9C%E4%B8%AD%E7%9A%84%E6%95%B0%E6%8D%AE.%0A%0A%60%60%60sql%0Aselect%20%0Arows_to_array(idList)%20deviceIdList%2C%20–%E5%B0%86%5B%7BdeviceId%3A1%7D%2C%7BdeviceId%3A2%7D%5D%20%E8%BD%AC%E4%B8%BA%5B1%2C2%5D%0AavgTemp%2C%0Afrom%0A(%0A%20%20%20select%0A%20%20%20collect_list((select%20this.deviceId%20deviceId))%20idList%2C%20–%E8%81%9A%E5%90%88%E7%BB%93%E6%9E%9C%E9%87%8C%E7%9A%84%0A%20%20%20avg(temperature)%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20avgTemp%20%2C%0A%20%20%20from%20%22%2Fdevice%2F*****%2F*****%2Fmessage%2Fproperty%2F**%22%20%2C%0A%20%20%20group%20by%20interval(‘1m’)%20having%20avgTemp%20%3E%2040%0A)%0A%0A%60%60%60%0A%0A5%E5%88%86%E9%92%9F%E4%B9%8B%E5%86%85%E5%8F%AA%E5%8F%96%E7%AC%AC%E4%B8%80%E6%AC%A1%E3%80%82%0A%0A%60%60%60sql%0A%0Aselect%20*%20%0Afrom%20%22%2Fdevice%2F*%2F*%2Fmessage%2Fevent%2Ffire_alarm%22%0A_window(‘5m’)%2Ctake(1)%20–%20-1%E4%B8%BA%E5%8F%96%E6%9C%80%E5%90%8E%E4%B8%80%E6%AC%A1%0A%0A%60%60%60%0A%0A%E9%99%90%E6%B5%81%3A%2010%E7%A7%92%E5%86%85%E8%B6%85%E8%BF%872%E6%AC%A1%E5%88%99%E8%8E%B7%E5%8F%96%E6%9C%80%E5%90%8E%E4%B8%80%E6%9D%A1%E6%95%B0%E6%8D%AE%0A%0A%60%60%60sql%0Aselect%20*%20from%20%0A(%20select%20*%20from%20%22%2Fdevice%2Fdemo-device%2Fdevice001%2Fmessage%2Fevent%2Falarm%22%20)%0Agroup%20by%0A_window(‘10s’)%20–%E6%97%B6%E9%97%B4%E7%AA%97%E5%8F%A3%0A%2Ctrace()%20–%20%E8%B7%9F%E8%B8%AA%E5%88%86%E7%BB%84%E5%86%85%E8%A1%8C%E5%8F%B7%E4%BF%A1%E6%81%AF%0A%2Ctake(-1)%20–%E5%8F%96%E6%9C%80%E5%90%8E%E4%B8%80%E6%9D%A1%E6%95%B0%E6%8D%AE%0Ahaving%20%0A%20%20row.index%20%3E%202%20%20–%20%E8%B7%9F%E8%B8%AA%E5%88%86%E7%BB%84%E5%86%85%E7%9A%84%E8%A1%8C%E5%8F%B7%0Aand%20%0A%20%20row.elapsed%3E1000%20–%20%E8%B7%9D%E7%A6%BB%E4%B8%8A%E4%B8%80%E8%A1%8C%E7%9A%84%E6%97%B6%E9%97%B4%0A%60%60%60%0A%0A%E6%B3%A8%E6%84%8F%0A%0ASQL%E4%B8%AD%E7%9A%84%60this%60%E8%A1%A8%E7%A4%BA%E4%B8%BB%E8%A1%A8%E5%BD%93%E5%89%8D%E7%9A%84%E6%95%B0%E6%8D%AE%2C%E5%A6%82%E6%9E%9C%E5%AD%98%E5%9C%A8%E5%B5%8C%E5%A5%97%E5%B1%9E%E6%80%A7%E7%9A%84%E6%97%B6%E5%80%99%2C%E5%BF%85%E9%A1%BB%E6%8C%87%E5%AE%9A%60this%60%E6%88%96%E8%80%85%E4%BB%A5%E8%A1%A8%E5%88%AB%E5%90%8D%E5%BC%80%E5%A4%B4.%20%E5%A6%82%3A%20%60this.properties.temperature%60%20%2C%E5%86%99%E6%88%90%3A%20%60properties.temperature%60%E6%98%AF%E6%97%A0%E6%B3%95%E8%8E%B7%E5%8F%96%E5%88%B0%E5%80%BC%E5%88%B0.%0A%0A%23%23%20SQL%E6%94%AF%E6%8C%81%E5%88%97%E8%A1%A8%0A%0A%7C%20%E5%87%BD%E6%95%B0%2F%E8%A1%A8%E8%BE%BE%E5%BC%8F%20%7C%20%E7%94%A8%E9%80%94%20%7C%20%E7%A4%BA%E4%BE%8B%20%7C%20%E8%AF%B4%E6%98%8E%20%7C%0A%7C%20—%20%7C%20—%20%7C%20—%20%7C%20—%20%7C%0A%7C%20%2B%20%7C%20%E5%8A%A0%E6%B3%95%E8%BF%90%E7%AE%97%20%7C%20temp%2B10%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20math.plus(temp%2C10)%20%7C%0A%7C%20%5C-%20%7C%20%E5%87%8F%E6%B3%95%E8%BF%90%E7%AE%97%20%7C%20temp-10%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20math.sub(temp%2C10)%20%7C%0A%7C%20%5C*%20%7C%20%E4%B9%98%E6%B3%95%E8%BF%90%E7%AE%97%20%7C%20temp%5C*10%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20math.mul(temp%2C10)%20%7C%0A%7C%20%2F%20%7C%20%E9%99%A4%E6%B3%95%E8%BF%90%E7%AE%97%20%7C%20temp%2F10%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20math.divi(temp%2C10)%20%7C%0A%7C%20%25%20%7C%20%E5%8F%96%E6%A8%A1%E8%BF%90%E7%AE%97%20%7C%20temp%252%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20math.mod(temp%2C2)%20%7C%0A%7C%20%26%20%7C%20%E4%BD%8D%E4%B8%8E%E8%BF%90%E7%AE%97%20%7C%20val%263%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20bit%5C_and(val%2C3)%20%7C%0A%7C%20%7C%20%7C%20%E4%BD%8D%E6%88%96%E8%BF%90%E7%AE%97%20%7C%20val%7C3%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20bit%5C_or(val%2C3)%20%7C%0A%7C%20%5E%20%7C%20%E5%BC%82%E6%88%96%E8%BF%90%E7%AE%97%20%7C%20val%5E3%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20bit%5C_mutex(val%2C3)%20%7C%0A%7C%20%3C%3C%20%7C%20%E4%BD%8D%E5%B7%A6%E7%A7%BB%E8%BF%90%E7%AE%97%20%7C%20val%3C%3C2%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20bit%5C_left%5C_shift(val%2C2)%20%7C%0A%7C%20%5C%3E%3E%20%7C%20%E4%BD%8D%E5%8F%B3%E7%A7%BB%E8%BF%90%E7%AE%97%20%7C%20val%3E%3E2%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20bit%5C_right%5C_shift(val%2C2)%20%7C%0A%7C%20%7C%7C%20%7C%20%E5%AD%97%E7%AC%A6%E6%8B%BC%E6%8E%A5%20%7C%20val%7C%7C’%E5%BA%A6’%20%7C%20%E5%AF%B9%E5%BA%94%E5%87%BD%E6%95%B0%3A%20concat(val%2C’%E5%BA%A6’)%20%7C%0A%7C%20avg%20%7C%20%E5%B9%B3%E5%9D%87%E5%80%BC%20%7C%20avg(val)%20%7C%20%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%2C%E5%B9%B3%E5%9D%87%E5%80%BC%20%7C%0A%7C%20sum%20%7C%20%E5%90%88%E8%AE%A1%E5%80%BC%20%7C%20sum(val)%20%7C%20%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%2C%E5%90%88%E8%AE%A1%E5%80%BC%20%7C%0A%7C%20count%20%7C%20%E6%80%BB%E6%95%B0%20%7C%20count(1)%20%7C%20%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%2C%E8%AE%A1%E6%95%B0%20%7C%0A%7C%20max%20%7C%20%E6%9C%80%E5%A4%A7%E5%80%BC%20%7C%20max(val)%20%7C%20%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%2C%E6%9C%80%E5%A4%A7%E5%80%BC%20%7C%0A%7C%20min%20%7C%20%E6%9C%80%E5%B0%8F%E5%80%BC%20%7C%20min(val)%20%7C%20%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%2C%E6%9C%80%E5%B0%8F%E5%80%BC%20%7C%0A%7C%20take%20%7C%20%E5%8F%96%E6%8C%87%E5%AE%9A%E6%95%B0%E9%87%8F%E6%95%B0%E6%8D%AE%20%7C%20take(5%2C-1)%20–%E5%8F%965%E4%B8%AA%E4%B8%AD%E7%9A%84%E6%9C%80%E5%90%8E%E4%B8%80%E4%B8%AA%20%7C%20%E9%80%9A%E5%B8%B8%E9%85%8D%E5%90%88%E5%88%86%E7%BB%84%E5%87%BD%E6%95%B0%5C_window%E4%BD%BF%E7%94%A8%20%7C%0A%7C%20%5C%3E%20%7C%20%E5%A4%A7%E4%BA%8E%20%7C%20val%20%3E%2010%20%7C%20%20%7C%0A%7C%20%3C%20%7C%20%E5%B0%8F%E4%BA%8E%20%7C%20val%20%3C%2010%20%7C%20%20%7C%0A%7C%20%5C%3D%20%7C%20%E7%AD%89%E4%BA%8E%20%7C%20val%20%3D%2010%20%7C%20%20%7C%0A%7C%20!%3D%20%7C%20%E4%B8%8D%E7%AD%89%E4%BA%8E%20%7C%20val%20!%3D10%20%7C%20%E7%AD%89%E5%90%8C%E4%BA%8E%3A%20%3C%3E%20%2C%E5%A6%82%3A%20val%20%3C%3E%2010%20%7C%0A%7C%20%5C%3E%3D%20%7C%20%E5%A4%A7%E4%BA%8E%E7%AD%89%E4%BA%8E%20%7C%20val%3E%3D10%20%7C%20%20%7C%0A%7C%20%3C%3D%20%7C%20%E5%B0%8F%E4%BA%8E%E7%AD%89%E4%BA%8E%20%7C%20val%3C%3D10%20%7C%20%20%7C%0A%7C%20in%20%7C%20%E5%9C%A8..%E4%B9%8B%E4%B8%AD%20%7C%20val%20in%20(1%2C2%2C3)%20%7C%20%20%7C%0A%7C%20not%20in%20%7C%20%E4%B8%8D%E5%9C%A8..%E4%B9%8B%E4%B8%AD%20%7C%20val%20not%20in%20(1%2C2%2C3)%20%7C%20%20%7C%0A%7C%20like%20%7C%20%E6%A8%A1%E7%B3%8A%E5%8C%B9%E9%85%8D%20%7C%20name%20like%20’a%25’%20%7C%20not%20like%20%E5%90%8C%E7%90%86%20%7C%0A%7C%20between%20%7C%20%E5%9C%A8%E4%B9%8B%E9%97%B4%20%7C%20val%20between%201%20and%2010%20%7C%20%20%7C%0A%7C%20now%20%7C%20%E5%BD%93%E5%89%8D%E6%97%B6%E9%97%B4%20%7C%20now()%20%7C%20%E9%BB%98%E8%AE%A4%E8%BF%94%E5%9B%9E%E6%97%B6%E9%97%B4%E6%88%B3%2C%E5%8F%AF%E4%BC%A0%E5%85%A5%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%8F%82%E6%95%B0.%20%7C%0A%7C%20date%5C_format%20%7C%20%E6%A0%BC%E5%BC%8F%E5%8C%96%E6%97%A5%E6%9C%9F%20%7C%20date%5C_format(now()%2C’yyyy-MM-dd’)%20%7C%20%20%7C%0A%7C%20cast%20%7C%20%E8%BD%AC%E6%8D%A2%E7%B1%BB%E5%9E%8B%20%7C%20cast(val%20as%20boolean)%20%7C%20%E6%94%AF%E6%8C%81%E7%B1%BB%E5%9E%8B%3A%20string%2Cboolean%2Cint%2Cdouble%2Cfloat%2Cdate%2Cdecimal%2Clong%20%7C%0A%7C%20interval%20%7C%20%E6%97%B6%E9%97%B4%E5%88%86%E7%BB%84%20%7C%20interval(‘10s’)%20%7C%20%E5%88%86%E7%BB%84%E5%87%BD%E6%95%B0%2C%E6%8C%89%E6%97%B6%E9%97%B4%E5%88%86%E7%BB%84%20%7C%0A%7C%20%5C_window%20%7C%20%E7%AA%97%E5%8F%A3%E5%88%86%E7%BB%84%20%7C%20%5C_window(10)%20%7C%20%E7%AA%97%E5%8F%A3%2C%E6%94%AF%E6%8C%81%E6%8C%89%E6%95%B0%E9%87%8F%E5%92%8C%E6%97%B6%E9%97%B4%E7%AA%97%E5%8F%A3%20%7C%0A%7C%20collect%5C_list%20%7C%20%E8%81%9A%E5%90%88%E7%BB%93%E6%9E%9C%E8%BD%AC%E4%B8%BAlist%20%7C%20collect%5C_list((select%20deviceId))%20%7C%20%E6%8A%8A%E8%81%9A%E5%90%88%E7%9A%84%E7%9A%84%E7%BB%93%E6%9E%9C%E8%BD%AC%E4%B8%BAlist%20%7C%0A%7C%20rows%5C_to%5C_array%20%7C%20%E5%B0%86%E7%BB%93%E6%9E%9C%E9%9B%86%E8%BD%AC%E4%B8%BA%E5%8D%95%E5%85%83%E7%B4%A0%E6%95%B0%E7%BB%84%20%7C%20rows%5C_to%5C_array(idList)%20%7C%20%E6%8A%8A%E5%8F%AA%E6%9C%89%E4%B8%80%E4%B8%AA%E5%B1%9E%E6%80%A7%E7%9A%84%E7%BB%93%E6%9E%9C%E9%9B%86%E4%B8%AD%E7%9A%84%E5%B1%9E%E6%80%A7%E8%BD%AC%E4%B8%BA%E9%9B%86%E5%90%88%20%7C%0A%7C%20new%5C_map%20%7C%20%E5%88%9B%E5%BB%BA%E4%B8%80%E4%B8%AAmap%20%7C%20new%5C_map(‘k1’%2Cv1%2C’k2’%2Cv2)%20%7C%20%20%7C%0A%7C%20new%5C_array%20%7C%20%E5%88%9B%E5%BB%BA%E4%B8%80%E4%B8%AA%E9%9B%86%E5%90%88%20%7C%20new%5C_array(1%2C2%2C3%2C4)%20%7C%20%20%7C%0A%7C%20math.ceil%20%7C%20%E5%90%91%E4%B8%8A%E5%8F%96%E6%95%B4%20%7C%20math.ceil(val)%20%7C%20%20%7C%0A%7C%20math.floor%20%7C%20%E5%90%91%E4%B8%8B%E5%8F%96%E6%95%B4%20%7C%20math.floor(val)%20%7C%20%20%7C%0A%7C%20math.round%20%7C%20%E5%9B%9B%E8%88%8D%E4%BA%94%E5%85%A5%20%7C%20math.round(val)%20%7C%20%20%7C%0A%7C%20math.log%20%7C%20log%E8%BF%90%E7%AE%97%20%7C%20math.log(val)%20%7C%20%20%7C%0A%7C%20math.sin%20%7C%20%E6%AD%A3%E5%BC%A6%20%7C%20math.sin(val)%20%7C%20%20%7C%0A%7C%20math.asin%20%7C%20%E5%8F%8D%E6%AD%A3%E5%BC%A6%20%7C%20math.asin(val)%20%7C%20%20%7C%0A%7C%20math.sinh%20%7C%20%E5%8F%8C%E6%9B%B2%E6%AD%A3%E5%BC%A6%20%7C%20math.sinh(val)%20%7C%20%20%7C%0A%7C%20math.cos%20%7C%20%E4%BD%99%E5%BC%A6%20%7C%20math.cos(val)%20%7C%20%20%7C%0A%7C%20math.acos%20%7C%20%E5%8F%8D%E4%BD%99%E5%BC%A6%20%7C%20math.acos(val)%20%7C%20%20%7C%0A%7C%20math.cosh%20%7C%20%E5%8F%8C%E6%9B%B2%E4%BD%99%E5%BC%A6%20%7C%20math.cosh(val)%20%7C%20%20%7C%0A%7C%20math.tan%20%7C%20%E6%AD%A3%E5%88%87%20%7C%20math.tan(val)%20%7C%20%20%7C%0A%7C%20math.atan%20%7C%20%E5%8F%8D%E6%AD%A3%E5%88%87%20%7C%20math.atan(val)%20%7C%20%20%7C%0A%7C%20math.tanh%20%7C%20%E5%8F%8C%E6%9B%B2%E6%AD%A3%E5%88%87%20%7C%20math.tanh(val)%20%7C%20%20%7C%0A%7C%20if%20%7C%20%E6%9D%A1%E4%BB%B6%E5%8F%96%E5%80%BC%20%7C%20if(a%3C1%2C’when%20true’%2C’when%20false’)%20%7C%20%20%7C%0A%7C%20range%20%7C%20%E8%8C%83%E5%9B%B4%E5%88%A4%E6%96%AD%2C%E7%AD%89%E5%90%8C%E4%BA%8Ebetween%20and%20%7C%20range(val%2C1%2C10)%20%7C%20%20%7C%0A%7C%20median%20%7C%20%E4%B8%AD%E4%BD%8D%E6%95%B0%20%7C%20median(val)%20%7C%20%E4%B8%AD%E4%BD%8D%E6%95%B0%20(Pro)%20%7C%0A%7C%20skewness%20%7C%20%E5%81%8F%E5%BA%A6%E7%89%B9%E5%BE%81%E5%80%BC%20%7C%20skewness(val)%20%7C%20%E5%81%8F%E5%BA%A6%E7%89%B9%E5%BE%81%E5%80%BC%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%20(Pro)%20%7C%0A%7C%20kurtosis%20%7C%20%E5%B3%B0%E5%BA%A6%E7%89%B9%E5%BE%81%E5%80%BC%20%7C%20kurtosis(val)%20%7C%20%E5%B3%B0%E5%BA%A6%E7%89%B9%E5%BE%81%E5%80%BC%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%20(Pro)%20%7C%0A%7C%20variance%20%7C%20%E6%96%B9%E5%B7%AE%20%7C%20variance(val)%20%7C%20%E6%96%B9%E5%B7%AE%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%20(Pro)%20%7C%0A%7C%20geo%5C_mean%20%7C%20%E5%87%A0%E4%BD%95%E5%B9%B3%E5%9D%87%E6%95%B0%20%7C%20geo%5C_mean(val)%20%7C%20%E5%87%A0%E4%BD%95%E5%B9%B3%E5%9D%87%E6%95%B0%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%20(Pro)%20%7C%0A%7C%20sum%5C_of%5C_squ%20%7C%20%E5%B9%B3%E6%96%B9%E5%92%8C%20%7C%20sum%5C_of%5C_squ(val)%20%7C%20%E5%B9%B3%E6%96%B9%E5%92%8C%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%20(Pro)%20%7C%0A%7C%20std%5C_dev%20%7C%20%E6%A0%87%E5%87%86%E5%B7%AE%20%7C%20std%5C_dev(val)%20%7C%20%E6%A0%87%E5%87%86%E5%B7%AE%E8%81%9A%E5%90%88%E5%87%BD%E6%95%B0%20(Pro)%20%7C%0A%7C%20slope%20%7C%20%E6%96%9C%E5%BA%A6%20%7C%20slope(val)%20%7C%20%E4%BD%BF%E7%94%A8%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E5%9B%9E%E5%BD%92%E6%A8%A1%E5%9E%8B%E8%AE%A1%E7%AE%97%E6%96%9C%E5%BA%A6%2C%E5%A4%A7%E4%BA%8E0%E4%B8%BA%E5%90%91%E4%B8%8A%2C%E5%B0%8F%E4%BA%8E0%E4%B8%BA%E5%90%91%E4%B8%8B%20(Pro)%20%7C%0A%7C%20time%20%7C%20%E8%BD%AC%E6%8D%A2%E6%97%B6%E9%97%B4%20%7C%20time(‘now-1d’)%20%7C%20%E4%BD%BF%E7%94%A8%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%9D%A5%E8%BD%AC%E6%8D%A2%E6%97%B6%E9%97%B4%2C%E8%BF%94%E5%9B%9E%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4%E6%88%B3(Pro)%20%7C%0A%7C%20jsonata%20%7C%20jsonata%E8%A1%A8%E8%BE%BE%E5%BC%8F%20%7C%20jsonata(‘%24abs(val)’)%20%7C%20%E4%BD%BF%E7%94%A8jsonata%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%9D%A5%E6%8F%90%E5%8F%96%E8%A1%8C%E6%95%B0%E6%8D%AE(Pro)%20%7C%0A%7C%20spel%20%7C%20spel%E8%A1%A8%E8%BE%BE%E5%BC%8F%20%7C%20spel(‘%23val’)%20%7C%20%E4%BD%BF%E7%94%A8spel%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%9D%A5%E6%8F%90%E5%8F%96%E8%A1%8C%E6%95%B0%E6%8D%AE(Pro)%20%7C%0A%7C%20env%20%7C%20%E8%8E%B7%E5%8F%96%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF%20%7C%20env(‘key’%2C’%E9%BB%98%E8%AE%A4%E5%80%BC’)%20%7C%20%E8%8E%B7%E5%8F%96%E7%B3%BB%E7%BB%9F%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF(Pro)%20%7C%0A%7C%20%5C_window%5C_until%20%7C%20%E6%89%93%E5%BC%80%E7%AA%97%E5%8F%A3%E7%9B%B4%E5%88%B0%E6%BB%A1%E8%B6%B3%E6%9D%A1%E4%BB%B6%20%7C%20%5C_window%5C_until(this.success)%20%7C%20%E6%89%93%E5%BC%80%E7%AA%97%E5%8F%A3%E7%9B%B4%E5%88%B0%E6%BB%A1%E8%B6%B3%E6%9D%A1%E4%BB%B6(Pro)%20%7C%0A%7C%20%5C_window%5C_until%5C_change%20%7C%20%E6%89%93%E5%BC%80%E7%AA%97%E5%8F%A3%E7%9B%B4%E5%88%B0%E5%80%BC%E5%8F%98%E6%9B%B4%20%7C%20%5C_window%5C_until%5C_change(this.state)%20%7C%20%E6%89%93%E5%BC%80%E7%AA%97%E5%8F%A3%E7%9B%B4%E5%88%B0%E5%80%BC%E5%8F%98%E6%9B%B4(Pro)%20%7C%0A%0A%23%23%20%E6%8B%93%E5%B1%95%E5%87%BD%E6%95%B0%0A%0ATIP%0A%0A%E4%BB%A5%E4%B8%8B%E5%8A%9F%E8%83%BD%E5%8F%AA%E5%9C%A8%E4%BC%81%E4%B8%9A%E7%89%88%E4%B8%AD%E6%94%AF%E6%8C%81%0A%0A%23%23%23%20device.properties%0A%0A%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B7%B2%E4%BF%9D%E5%AD%98%E7%9A%84%E5%85%A8%E9%83%A8%E6%9C%80%E6%96%B0%E5%B1%9E%E6%80%A7%2C(%E6%B3%A8%E6%84%8F%3A%20%E7%94%B1%E4%BA%8E%E4%BD%BF%E7%94%A8es%E5%AD%98%E5%82%A8%E8%AE%BE%E5%A4%87%E6%95%B0%E6%8D%AE%2C%E6%AD%A4%E6%95%B0%E6%8D%AE%E5%B9%B6%E4%B8%8D%E6%98%AF%E5%AE%8C%E5%85%A8%E5%AE%9E%E6%97%B6%E7%9A%84)%0A%0A%60%60%60sql%0Aselect%20%0Adevice.properties(this.deviceId)%20props%2C%0Athis.properties%20reports%0Afrom%20%22%2Fdevice%2F*%2F*%2Fmessage%2Fproperty%2Freport%22%0A%60%60%60%0A%0ATIP%0A%0A%60device.properties(this.deviceId%2C’property1’%2C’property2’)%60%E8%BF%98%E5%8F%AF%E4%BB%A5%E9%80%9A%E8%BF%87%E5%8F%82%E6%95%B0%E8%8E%B7%E5%8F%96%E6%8C%87%E5%AE%9A%E7%9A%84%E5%B1%9E%E6%80%A7%EF%BC%8C%E5%A6%82%E6%9E%9C%E6%9C%AA%E8%AE%BE%E7%BD%AE%E5%88%99%E8%8E%B7%E5%8F%96%E5%85%A8%E9%83%A8%E5%B1%9E%E6%80%A7%E3%80%82%0A%0A%23%23%23%20device.properties.history%0A%0A%E6%9F%A5%E8%AF%A2%E8%AE%BE%E5%A4%87%E5%8E%86%E5%8F%B2%E6%95%B0%E6%8D%AE%0A%0A%60%60%60sql%0A–%E8%81%9A%E5%90%88%E6%9F%A5%E8%AF%A2%0Aselect%20*%20from%20device.properties.history(%0A%20%20%20select%20avg(temperature)%20avgVal%20%0A%20%20%20from%20%22deviceId%22%20–%20from%20%E6%94%AF%E6%8C%81%3A%20%E6%8C%89%E8%AE%BE%E5%A4%87ID%E6%9F%A5%E8%AF%A2%3A%20%22deviceId%22%2C%20%E6%9F%A5%E8%AF%A2%E5%A4%9A%E4%B8%AA%E8%AE%BE%E5%A4%87%3A%20device(‘1’%2C’2’)%20%E6%8C%89%E4%BA%A7%E5%93%81%E6%9F%A5%E8%AF%A2%3A%20product(‘id’)%0A%20%20%20where%20timestamp%20between%20now()-86400000%20and%20now()%0A)%0A%60%60%60%0A%0A%60%60%60sql%0A%20–%E6%8C%89%E6%97%B6%E9%97%B4%E5%88%86%E7%BB%84%0Aselect%20*%20from%20device.properties.history(%0A%20%20%20%20select%20avg(temperature)%20avgVal%20%0A%20%20%20%20from%20%22deviceId%22%0A%20%20%20%20where%20timestamp%20between%20now()-86400000%20and%20now()%0A%20%20%20%20group%20by%20interval(‘1d’)%0A)%0A%60%60%60%0A%0A%60%60%60sql%0A–%20%E8%AE%A2%E9%98%85%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE%2C%E7%84%B6%E5%90%8E%E6%9F%A5%E8%AF%A2%E5%AF%B9%E5%BA%94%E8%AE%BE%E5%A4%87%E7%9A%84%E5%8E%86%E5%8F%B2%E6%95%B0%E6%8D%AE%0Aselect%20%0A(%0Aselect%20maxVal%2CavgVal%20from%20%0A%20%20%20%20device.properties.history(%0A%20%20%20%20%20%20%20%20select%20%0A%20%20%20%20%20%20%20%20max(temp3)%20maxVal%2C%0A%20%20%20%20%20%20%20%20avg(temp3)%20avgVal%0A%20%20%20%20%20%20%20%20from%20device(t.deviceId)%0A%20%20%20%20%20%20%20%20–%20%E5%89%8D%E4%B8%80%E5%A4%A9%E7%9A%84%E6%95%B0%E6%8D%AE%0A%20%20%20%20%20%20%20%20where%20timestamp%20between%20time(‘now-1d’)%20and%20t.timestamp%0A%20%20%20%20)%0A)%20%24this%2C%0At.properties.temp3%20temp3%0Afrom%20%22%2Fdevice%2F*%2F*%2Fmessage%2Fproperty%2F****%22%20t%0A%60%60%60%0A%0A%23%23%23%20device.properties.latest%0A%0ATIP%0A%0A%E6%AD%A4%E5%8A%9F%E8%83%BD%E9%9C%80%E8%A6%81%E5%BC%80%E5%90%AF%5B%E8%AE%BE%E5%A4%87%E6%9C%80%E6%96%B0%E6%95%B0%E6%8D%AE%E5%AD%98%E5%82%A8%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Fbest-practices%2Fstart.html%23%25E8%25AE%25B0%25E5%25BD%2595%25E8%25AE%25BE%25E5%25A4%2587%25E6%259C%2580%25E6%2596%25B0%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%25B0%25E6%2595%25B0%25E6%258D%25AE%25E5%25BA%2593)%0A%0A%E6%9F%A5%E8%AF%A2%E8%AE%BE%E5%A4%87%E6%9C%80%E6%96%B0%E7%9A%84%E6%95%B0%E6%8D%AE%0A%0A%60%60%60sql%0Aselect%20%20from%20device.properties.latest(%0A%20%20%20%20select%20%0A%20%20%20%20temperature%0A%20%20%20%20from%20%22productId%22%20–%E8%A1%A8%E5%90%8D%E4%B8%BA%E4%BA%A7%E5%93%81ID%0A%20%20%20%20where%20id%20%3D%20’deviceId’%20–%20id%E5%88%99%E4%B8%BA%E8%AE%BE%E5%A4%87ID%0A)%0A%60%60%60%0A%0A%E8%81%9A%E5%90%88%E6%9F%A5%E8%AF%A2%0A%0A%60%60%60sql%0Aselect%20%20from%20device.properties.latest(%0A%20%20%20%20select%20%0A%20%20%20%20avg(temperature)%20temperature%0A%20%20%20%20from%20%22productId%22%20–%E8%A1%A8%E5%90%8D%E4%B8%BA%E4%BA%A7%E5%93%81ID%0A)%0A%60%60%60%0A%0A%23%23%23%20device.tags%0A%0A%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87%E6%A0%87%E7%AD%BE%E4%BF%A1%E6%81%AF%0A%0A%60%60%60sql%0Aselect%20device.tags(this.deviceId)%20from%20%22%2Fdevice%2F%2F%2Fmessage%2Fproperty%2Freport%22%0A%60%60%60%0A%0ATIP%0A%0A%60device.tags(this.deviceId%2C’tag1’%2C’tag2’)%60%E8%BF%98%E5%8F%AF%E4%BB%A5%E9%80%9A%E8%BF%87%E5%8F%82%E6%95%B0%E8%8E%B7%E5%8F%96%E6%8C%87%E5%AE%9A%E7%9A%84%E6%A0%87%E7%AD%BE%EF%BC%8C%E5%A6%82%E6%9E%9C%E6%9C%AA%E8%AE%BE%E7%BD%AE%E5%88%99%E8%8E%B7%E5%8F%96%E5%85%A8%E9%83%A8%E6%A0%87%E7%AD%BE%E3%80%82%0A%0A%23%23%23%20device.selector%0A%0A%E9%80%89%E6%8B%A9%E8%AE%BE%E5%A4%87%2C%E5%A6%82%EF%BC%9A%0A%0A%60%60%60sql%0Aselect%20dev.deviceId%20from%20%22%2Fdevice%2F%2F%2Fmessage%2Fproperty%2Freport%22%20t%0A–%20%E8%8E%B7%E5%8F%96%E5%92%8C%E4%B8%8A%E6%8A%A5%E5%B1%9E%E6%80%A7%E5%9C%A8%E5%90%8C%E4%B8%80%E4%B8%AA%E5%88%86%E7%BB%84%E9%87%8C%EF%BC%8C%E5%B9%B6%E4%B8%94%E4%BA%A7%E5%93%81id%E4%B8%BAlight-product%E7%9A%84%E8%AE%BE%E5%A4%87%0Aleft%20join%20(%20%0A%20%20%20%20%20%20%20%20%20%20%20%20select%20this.id%20deviceId%20from%20%0A%20%20%20%20%20%20%20%20%20%20%20%20device.selector(same_group(t.deviceId)%2Cproduct(‘light-product’))%0A%20%20%20%20%20%20%20%20%20%20)%20dev%0A%60%60%60%0A%0A%E6%94%AF%E6%8C%81%E5%8F%82%E6%95%B0%3A%0A%0A1.%20in%5C_gourp(‘groupId’)%20%E5%9C%A8%E6%8C%87%E5%AE%9A%E7%9A%84%E8%AE%BE%E5%A4%87%E5%88%86%E7%BB%84%E4%B8%AD%0A2.%20in%5C_group%5C_tree(‘groupId’)%20%E5%9C%A8%E6%8C%87%E5%AE%9A%E5%88%86%E7%BB%84%E4%B8%AD%EF%BC%88%E5%8C%85%E5%90%AB%E4%B8%8B%E7%BA%A7%E5%88%86%E7%BB%84%EF%BC%89%0A3.%20same%5C_group(‘deviceId’)%20%E5%9C%A8%E6%8C%87%E5%AE%9A%E8%AE%BE%E5%A4%87%E7%9A%84%E7%9B%B8%E5%90%8C%E5%88%86%E7%BB%84%E4%B8%AD%0A4.%20product(‘productId’)%20%E6%8C%87%E5%AE%9A%E4%BA%A7%E5%93%81ID%E5%AF%B9%E5%BA%94%E7%9A%84%E8%AE%BE%E5%A4%87%0A5.%20tag(‘tag1Key’%2C’tag1Value’%2C’tag2Key’%2C’tag2Value’)%20%E6%8C%89%E6%8C%87%E5%AE%9A%E7%9A%84%E6%A0%87%E7%AD%BE%E8%8E%B7%E5%8F%96%0A6.%20state(‘online’)%20%E6%8C%89%E6%8C%87%E5%AE%9A%E7%9A%84%E7%8A%B6%E6%80%81%E8%8E%B7%E5%8F%96%0A7.%20in%5C_tenant(‘%E7%A7%9F%E6%88%B7ID’)%20%E5%9C%A8%E6%8C%87%E5%AE%9A%E7%A7%9F%E6%88%B7%E4%B8%AD%E7%9A%84%E8%AE%BE%E5%A4%87%0A8.%20org(‘%E6%9C%BA%E6%9E%84ID’)%20%E5%9C%A8%E6%8C%87%E5%AE%9A%E6%9C%BA%E6%9E%84%E4%B8%AD%0A%0A%23%23%23%20mqtt.client.publish%0A%0A%E6%8E%A8%E9%80%81%E6%B6%88%E6%81%AF%E5%88%B0mqtt%E5%AE%A2%E6%88%B7%E7%AB%AF.%0A%0A%60%60%60sql%0A%0Aselect%20%0Amqtt.client.publish(%0A%20%20%20’networkId’%20–%20%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%8F%82%E6%95%B0%3A%20%E7%BD%91%E7%BB%9C%E7%BB%84%E4%BB%B6%E4%B8%ADmqtt%E5%AE%A2%E6%88%B7%E7%AB%AF%E7%9A%84ID%0A%20%20%20%2C’topic’%20–%20%E7%AC%AC%E4%BA%8C%E4%B8%AA%E5%8F%82%E6%95%B0%3A%20topic%0A%20%20%20%2C’JSON’%20%20–%20%E7%AC%AC%E4%B8%89%E4%B8%AA%E5%8F%82%E6%95%B0%3A%20%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%3A%20JSON%2CSTRING%2CBINARY%2CHEX%0A%20%20%20%2Cthis%20%20–%20%E6%B6%88%E6%81%AF%E4%BD%93%2C%E4%BC%9A%E6%A0%B9%E6%8D%AE%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E8%BD%AC%E4%B8%BA%E4%B8%8D%E5%90%8C%E6%A0%BC%E5%BC%8F%E7%9A%84%E6%B6%88%E6%81%AF%0A%20%20%20)%20publishSuccess%20–%20%E8%BF%94%E5%9B%9E%E6%8E%A8%E9%80%81%E7%BB%93%E6%9E%9C%20true%20false%0Afrom%20%22%2Frule-engine%2Fdevice%2Falarm%2Fsensor-1%2F****%22%0A%0A%60%60%60%0A%0A%23%23%23%20mqtt.client.subscribe%0A%0A%E4%BB%8Emqtt%E5%AE%A2%E6%88%B7%E7%AB%AF%E8%AE%A2%E9%98%85%E6%B6%88%E6%81%AF%0A%0A%60%60%60sql%0A%0Aselect%20%0At.did%20deviceId%2C%0At.l%20location%2C%0At.v%20value%0Afrom%20mqtt.client.subscribe(%0A%20%20%20’networkId’%20–%20%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%8F%82%E6%95%B0%3A%20%E7%BD%91%E7%BB%9C%E7%BB%84%E4%BB%B6%E4%B8%ADmqtt%E5%AE%A2%E6%88%B7%E7%AB%AF%E7%9A%84ID%0A%20%20%20%2C’JSON’%20–%20%E7%AC%AC%E4%BA%8C%E4%B8%AA%E5%8F%82%E6%95%B0%3A%20%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%3A%20JSON%2CSTRING%2CBINARY%2CHEX%0A%20%20%20%2C’topic’%20–%20topic%0A%20%20%20%2C’topic2’%20–%20topic2%0A)%20t%0Awhere%20t.v%20%3E%2030%20–%20%E8%BF%87%E6%BB%A4%E6%9D%A1%E4%BB%B6%0A%0A%60%60%60%0A%0A%23%23%23%20http.request%0A%0A%E5%8F%91%E8%B5%B7http%E8%AF%B7%E6%B1%82%0A%0A%60%60%60sql%0A%0Aselect%0A%0Ahttp.request(%0A%20%20%20’networkId’%20–%20%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%8F%82%E6%95%B0%3A%20%E7%BD%91%E7%BB%9C%E7%BB%84%E4%BB%B6%E4%B8%ADhttp%E5%AE%A2%E6%88%B7%E7%AB%AF%E7%9A%84ID%0A%20%20%20–%20%E4%B8%8B%E9%9D%A2%E7%9A%84%E5%8F%82%E6%95%B0%E4%B8%A4%E4%B8%A4%E5%AF%B9%E5%BA%94%E7%BB%84%E6%88%90%E9%94%AE%E5%80%BC%E5%AF%B9%2C%E6%B3%A8%E6%84%8F%3A%20%E4%BD%BF%E7%94%A8%E9%80%97%E5%8F%B7(%2C)%E5%88%86%E5%89%B2.%0A%20%20%20%2C’url’%2C’https%3A%2F%2Fwww.baidu.com’%0A%20%20%20%2C’method’%2C’POST’%0A%20%20%20%2C’contentType’%2C’application%2Fjson’%0A%20%20%20–%20%E8%AF%B7%E6%B1%82%E5%A4%B4%0A%20%20%20%2C’headers’%2Cnew_map(‘key1’%2C’value1’%2C’key2’%2C’value2’)%0A%20%20%20–%20body%E5%8F%82%E6%95%B0%E5%9C%A8contentType%E4%B8%BAapplication%2Fjson%E6%97%B6%E7%94%9F%E6%95%88%0A%20%20%20%2C’body’%2Cnew_map(‘key1’%2C’value1’%2C’key2’%2C’value2’)%0A%20%20%20–%20requestParam%E5%8F%82%E6%95%B0%E5%9C%A8contentType%E4%B8%8D%E4%B8%BAjson%E6%97%B6%E7%94%9F%E6%95%88%2C%E7%9B%B8%E5%BD%93%E4%BA%8E%3Aapplication%2Fx-www-form-urlencoded%E7%9A%84%E5%A4%84%E7%90%86%E6%96%B9%E5%BC%8F%0A%20%20%20%2C’requestParam’%2Cnew_map(‘key1’%2C’value1’%2C’key2’%2C’value2’)%0A%20%20%20–%20%E7%9B%B4%E6%8E%A5%E6%8B%BC%E6%8E%A5%E5%88%B0url%E4%B8%8A%E7%9A%84%E5%8F%82%E6%95%B0%20https%3A%2F%2Fwww.baidu.com%3Fkey1%3Dvalue1%26key2%3Dvalue2%0A%20%20%20%2C’queryParameters’%2Cnew_map(‘key1’%2C’value1’%2C’key2’%2C’value2’)%0A%0A)%20response%0A%0Afrom%20dual%0A%0A%60%60%60%0A%0A%23%23%23%20message.subscribe%0A%0A%E8%AE%A2%E9%98%85%E6%B6%88%E6%81%AF%E7%BD%91%E5%85%B3%E4%B8%AD%E7%9A%84%E6%B6%88%E6%81%AF%0A%0A%60%60%60sql%0A%0Aselect%20%0At.topic%20topic%2C%0At.message.deviceId%20deviceId%2C%0At.message.headers.productId%20productId%2C%0At.message.timestamp%20ts%0Afrom%20message.subscribe(%0A%20%20%20’false’%20–%20%E6%98%AF%E5%90%A6%E8%AE%A2%E9%98%85%E6%9D%A5%E8%87%AA%E9%9B%86%E7%BE%A4%E7%9A%84%E6%B6%88%E6%81%AF(%E5%8F%AF%E9%80%89%E5%8F%82%E6%95%B0%2C%E9%BB%98%E8%AE%A4%E4%B8%BAfalse)%0A%20%20%20%2C’%2Fdevice%2F*%2F*%2Fonline’%0A%20%20%20)%20%20t%0A%0A%60%60%60%0A%0A%23%23%23%20message.publish%0A%0A%E6%8E%A8%E9%80%81%E6%B6%88%E6%81%AF%E5%88%B0%E6%B6%88%E6%81%AF%E7%BD%91%E5%85%B3%0A%0A%60%60%60sql%0A%0Aselect%0A%0Amessage.publish(%0A%20%20%20’%2Fdevice-online%2F’%7C%7Ct.message.deviceId%20–%20%E6%8E%A8%E9%80%81%E5%88%B0%E6%AD%A4topic%0A%20%20%20%2Ct.message%20–%20%E6%B6%88%E6%81%AF%E5%86%85%E5%AE%B9%0A%20%20%20)%20subscribeNumber%20–%20%E8%BF%94%E5%9B%9E%E6%9C%89%E5%A4%9A%E5%B0%91%E8%AE%A2%E9%98%85%E8%80%85%E6%94%B6%E5%88%B0%E4%BA%86%E6%B6%88%E6%81%AF%0A%0Afrom%20message.subscribe(‘%2Fdevice%2F*%2F*%2Fonline’)%20%20t%0A%60%60%60
