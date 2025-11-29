---
layout: post
title: JetLinks 响应式编程
slug: jetlinks-reactive-programming
type:
  - note
date: 2023-05-25
status: draft
tags:
  - JetLinks
categories:
  - IoT
mood:
weather:
author: deathwhispers
created: 2023-05-25 11:45
updated: 2023-05-25 18:33
---


# 响应式

JetLinks使用[Project Reactor](https://github.com/reactor)作为响应式编程框架,从网络层(webflux,vert.x)到持久层(r2dbc,elastic)全部 封装为非阻塞,响应式调用.

响应式可以理解为观察者模式,通过订阅和发布数据流中的数据对数据进行处理. Project Reactor提供了强大的API,简化多线程和异步编程开发,降低了对数据各种处理方式的复杂度,如果你已经大量使用了java8 stream api,使用reactor将很容易上手.

注意

响应式与传统编程最大的区别是:

响应式中的方法调用是在构造一个流以及处理流中数据的逻辑,当流中产生了数据(发布,订阅),才会执行构造好的逻辑.

传统编程则是直接执行逻辑获取结果.

## 优点

非阻塞,大大简化多线程异步编程. 集成netty等框架可实现更高的网络并发处理能力. API丰富,实现很多复杂的功能只需要几行代码,例如:

1. 前端展示实时数据处理进度.
2. 请求撤销,可获取到连接断开事件.
3. 定时(
interval
),延迟(
delay
),超时(
timout
),以及细粒度的流量控制(
limitRate
).
4. 分组(
groupBy
),聚合(
collect
,
reduce
)操作等

## 缺点

调试不易,异常栈难跟踪,对开发人员有更高的要求.

此问题可以通过优化代码结构来解决,比如: 避免在响应式操作符中直接业务逻辑, 正确的做法是将业务逻辑抽离为独立的函数(方法),然后使用响应式来进行组合.

注意

响应式只是一个编程模型,并不能直接提高系统的并发处理能力. 通常与netty(reactor-netty)等框架配合,从上(网络)到下(持久化)全套实现非阻塞,响应式才有意义.

## 选择合适的操作符

系统中大量使用到了reactor,其核心类只有2个Flux(0-n个数据的流),Mono(0-1个数据的流). 摒弃传统编程的思想,熟悉Flux,Mono操作符(API),就可以很好的使用响应式编程了.

常用操作符:

5. map
: 转换流中的元素:
flux.map(UserEntity::getId)
6. mapNotNull
: 转换流中的元素,并忽略null值.(
reactor 3.4
提供)
7. flatMap
: 转换流中的元素为新的流:
flux.flatMap(this::findById)
8. flatMapMany
: 转换Mono中的元素为Flux(1个转多个):
mono.flatMapMany(this::findChildren)
9. concat
: 将多个流连接在一起组成一个流(按顺序订阅) :
Flux.concat(header,body)
10. merge
: 将多个流合并在一起,同时订阅流:
Flux.merge(save(info),saveDetail(detail))
11. zip
: 压缩多个流中的元素:
Mono.zip(getData(id),getDetail(id),UserInfo::of)
12. then
: 上游流完成后执行其他的操作.
13. doOnNext
: 流中产生数据时执行.
14. doOnError
: 发送错误时执行.
15. doOnCancel
: 流被取消时执行.如: http未响应前,客户端断开了连接.
16. onErrorContinue
: 流发生错误时,继续处理数据而不是终止整个流.
17. defaultIfEmpty
: 当流为空时,使用默认值.
18. switchIfEmpty
: 当流为空时,切换为另外一个流.
19. as
: 将流作为参数,转为另外一个结果:
flux.as(this::save)

完整文档请查看[官方文档](https://projectreactor.io/docs/core/release/reference/#which-operator)

## 代码格式化

使用reactor时,应该注意代码尽量以.换行并做好相应到缩进.例如:

```plain text
//错误
return paramMono.map(param->param.getString("id")).flatMap(this::findById);

//建议
return paramMono
            .map(param->param.getString("id"))
            .flatMap(this::findById);
```

## lamdba

避免在一个lambda中编写大量的逻辑代码,推荐参考领域模型,将具体当逻辑放到对应到实体或者领域对象中.例如:

```plain text
//错误
return devicePropertyMono
        .map(prop->{
            Map<String,Object> map = new HashMap<>();
            map.put("property",prop.getProperty());
            ....
            return map;
        })
        .flatMap(this::doSomeThing)

//建议
//在DeviceProperty中编写toMap方法实现上面lambda中到逻辑.
return devicePropertyMono
        .map(DeviceProperty::toMap)
        .flatMap(this::doSomeThing)
```

## null处理

数据流中到元素不允许为null,因此在进行数据转换到时候要注意null处理.例如:

```plain text
//存在缺陷
return this.findById(id)
           .map(UserEntity::getDescription); //getDescription可能返回null,为null时会抛出空指针,
```

在reactor 3.4后可以使用以下方式来处理可能存在null的map操作

```plain text
return this.findById(id)
           .mapNotNull(UserEntity::getDescription);
```

## 非阻塞与阻塞

默认情况下,reactor的调度器由数据的生产者(Publisher)决定,在WebFlux中则是netty的工作线程, 为了防止工作线程被阻塞导致服务崩溃,在一个请求的流中,禁止执行存在阻塞(如执行JDBC)可能的操作的,如果无法避免阻塞操作,应该指定调度器如:

```plain text
paramMono
  .publishOn(Schedulers.elastic()) //指定调度器去执行下面的操作
  .map(param-> jdbcService.select(param))
```

## 上下文

在响应式中,大部分情况是禁止使用ThreadLocal的(可能造成内存泄漏).因此基于ThreadLocal的功能都无法使用,reactor中引入了上下文,在一个流中,可共享此上下文 ,通过上下文进行变量共享以例如:事务,权限等功能.例如:

```plain text
//从上下文中获取
@GetMapping
public Mono<UserInfo> getCurrentUser(){
    return Mono.subscriberContext()
            .map(ctx->userService.findById(ctx.getOrEmpty("userId").orElseThrow(IllegalArgumentException::new));
}

//定义过滤器设置数据到上下文中
class MyFilter implements WebFilter{
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain){
        return chain.filter(exchange)
            .subscriberContext(Context.of("userId",...))
    }
}
```

注意

在开发中应该将多个流组合为一个流,而不是分别处理.例如:

```plain text
//错误
return flux.doOnNext(data->this.save(data).subscribe());

//正确
return flux.flatMap(this::save);

//错误,没有将流组合在一起
request.flatMap(this::save);
Mono<Void> result = this.notifySaveSuccess();
return result;

//正确
return request
    .flatMap(this::save)
    .then(this.notifySaveSuccess());
```

## FAQ: 我写的操作看上去是正确的,但是没有执行.

有3种可能: 上游流为空,多个流未组合在一起,在不支持响应式的地方使用了响应式

上游流为空:

例:

```plain text
public Mono<Response> handleRequest(Request request){

 return this
      .findOldData(request)
      .flatMap(old -> {
            //这里为什么不执行?
            return ....
      })

}
```

说明

当findOldData返回的流为空时,下游的flatMap等需要操作流中元素的操作符是不会执行的. 可以通过switchIfEmpty操作符来处理空流的情况. 例如:

```plain text
return this
      .findOldData(request)
      //处理没获取到数据的情况
      .switchIfEmpty(Mono.error(()->new NotFoundException("error.data_not_found")))
      .flatMap(old -> {
            return ....
      })
```

如果flatMap和switchIfEmpty中的逻辑都没执行,那可能是下面一种情况.

多个流未组合在一起

例:

```plain text
public Result handleRequest(Request request){

     //处理请求
     service.handleRequest(request);

     return ok;

}
```

注意

20. 只要方法返回值是
Mono
或者
Flux
,都不能单独行动.
21. 只要方法中调用了任何响应式操作.那这个方法也应该是响应式.(返回Mono或者Flux)

因此正确的写法是:

```plain text
public Mono<Result> handleRequest(Request request){
 return service
         //处理请求
         .handleRequest(request)
         //记录日志
         .then(saveLog(request))
         //返回结果
         .thenReturn(ok);
}
```

在不支持响应式的地方使用响应式

```plain text
public Mono<Result> handleRequest(Request request){

return service
         //处理请求
         .handleRequest(request)
         //记录日志 此为错误的用法
         .doOnNext(response-> saveLog(request,response) )
         //返回结果
         .thenReturn(ok);
}
```

说明

从doOnNext方法的语义以及参数Consumer可知,此方法是不支持响应式的（Consumer只有参数没有返回值）,因此不能在此方法中使用响应式操作.

正确的写法:

```plain text
return service
         //处理请求
         .handleRequest(request)
         //记录日志 此为错误的用法
         .flatMap(response-> saveLog(request,response) )
         //返回结果
         .thenReturn(ok);
```

## FAQ: 我想获取流中的元素怎么办

不要试图从流中获取数据出来,而是先思考需要对流中元素做什么, 需要对流中的数据进行操作时,都应该使用操作符来处理,根据Flux或者Mono提供的操作符API进行组合操作.比如:

传统:

```plain text
public List<Book> getAllBooks(){
    List<BookEntity> bookEntities = repository.findAll();

    List<Book> books = new ArrayList(bookEntities.size());

    for(BookEntity entity : bookEntities){
        Book book = entity.copyTo(new Book());
        books.add(book);
    }

    return books;
}
```

响应式:

```plain text
public Flux<Book> getAllBooks(){
return repository
        .findAll()
        .map(entity-> entity.copyTo(new Book()))
}
```

## FAQ: 我需要在非响应式方法中使用响应式怎么办

如果需要阻塞获取结果,可以使用flux.block(timeout).

如果需要异步获取结果,可以使用flux.subscribe(data->{ },error->{ })

如:

```plain text
public void handleRequest(Request request){

  //logService.saveLog(request).block()

  logService
    .saveLog(request)
    .subscribe(
        result->{
            log.debug("保存成功 {}",request)
        },
        error->{
            log.warn("保存失败 {}",request,error);
        }
    )
}
```

## 相关资料

22. [reactive-streams](http://www.reactive-streams.org/)
23. [project-reactor](https://projectreactor.io/)
24. [使用 Reactor 进行反应式编程](https://www.ibm.com/developerworks/cn/java/j-cn-with-reactor-response-encode/index.html?lnk=hmhm)

%23%20%E5%93%8D%E5%BA%94%E5%BC%8F%0A%0A%5Btoc%5D%0A%0AJetLinks%E4%BD%BF%E7%94%A8%5BProject%20Reactor%5D(https%3A%2F%2Fgithub.com%2Freactor)%E4%BD%9C%E4%B8%BA%E5%93%8D%E5%BA%94%E5%BC%8F%E7%BC%96%E7%A8%8B%E6%A1%86%E6%9E%B6%2C%E4%BB%8E%E7%BD%91%E7%BB%9C%E5%B1%82(%60webflux%60%2C%60vert.x%60)%E5%88%B0%E6%8C%81%E4%B9%85%E5%B1%82(%60r2dbc%60%2C%60elastic%60)%E5%85%A8%E9%83%A8%20%E5%B0%81%E8%A3%85%E4%B8%BA%60%E9%9D%9E%E9%98%BB%E5%A1%9E%60%2C%60%E5%93%8D%E5%BA%94%E5%BC%8F%60%E8%B0%83%E7%94%A8.%0A%0A%E5%93%8D%E5%BA%94%E5%BC%8F%E5%8F%AF%E4%BB%A5%E7%90%86%E8%A7%A3%E4%B8%BA%60%E8%A7%82%E5%AF%9F%E8%80%85%E6%A8%A1%E5%BC%8F%60%2C%E9%80%9A%E8%BF%87%60%E8%AE%A2%E9%98%85%60%E5%92%8C%60%E5%8F%91%E5%B8%83%60%E6%95%B0%E6%8D%AE%E6%B5%81%E4%B8%AD%E7%9A%84%E6%95%B0%E6%8D%AE%E5%AF%B9%E6%95%B0%E6%8D%AE%E8%BF%9B%E8%A1%8C%E5%A4%84%E7%90%86.%20%60Project%20Reactor%60%E6%8F%90%E4%BE%9B%E4%BA%86%E5%BC%BA%E5%A4%A7%E7%9A%84API%2C%E7%AE%80%E5%8C%96%E5%A4%9A%E7%BA%BF%E7%A8%8B%E5%92%8C%E5%BC%82%E6%AD%A5%E7%BC%96%E7%A8%8B%E5%BC%80%E5%8F%91%2C%E9%99%8D%E4%BD%8E%E4%BA%86%E5%AF%B9%E6%95%B0%E6%8D%AE%E5%90%84%E7%A7%8D%E5%A4%84%E7%90%86%E6%96%B9%E5%BC%8F%E7%9A%84%E5%A4%8D%E6%9D%82%E5%BA%A6%2C%E5%A6%82%E6%9E%9C%E4%BD%A0%E5%B7%B2%E7%BB%8F%E5%A4%A7%E9%87%8F%E4%BD%BF%E7%94%A8%E4%BA%86%60java8%20stream%20api%60%2C%E4%BD%BF%E7%94%A8%60reactor%60%E5%B0%86%E5%BE%88%E5%AE%B9%E6%98%93%E4%B8%8A%E6%89%8B.%0A%0A%E6%B3%A8%E6%84%8F%0A%0A%60%E5%93%8D%E5%BA%94%E5%BC%8F%60%E4%B8%8E%60%E4%BC%A0%E7%BB%9F%E7%BC%96%E7%A8%8B%60%E6%9C%80%E5%A4%A7%E7%9A%84%E5%8C%BA%E5%88%AB%E6%98%AF%3A%0A%0A%60%E5%93%8D%E5%BA%94%E5%BC%8F%60%E4%B8%AD%E7%9A%84%E6%96%B9%E6%B3%95%E8%B0%83%E7%94%A8%E6%98%AF%E5%9C%A8%60%E6%9E%84%E9%80%A0%60%E4%B8%80%E4%B8%AA%E6%B5%81%E4%BB%A5%E5%8F%8A%60%E5%A4%84%E7%90%86%E6%B5%81%E4%B8%AD%E6%95%B0%E6%8D%AE%60%E7%9A%84%E9%80%BB%E8%BE%91%2C%E5%BD%93%60%E6%B5%81%60%E4%B8%AD%E4%BA%A7%E7%94%9F%E4%BA%86%E6%95%B0%E6%8D%AE(%60%E5%8F%91%E5%B8%83%2C%E8%AE%A2%E9%98%85%60)%2C%E6%89%8D%E4%BC%9A%E6%89%A7%E8%A1%8C%E6%9E%84%E9%80%A0%E5%A5%BD%E7%9A%84%E9%80%BB%E8%BE%91.%0A%0A%60%E4%BC%A0%E7%BB%9F%E7%BC%96%E7%A8%8B%60%E5%88%99%E6%98%AF%E7%9B%B4%E6%8E%A5%E6%89%A7%E8%A1%8C%E9%80%BB%E8%BE%91%E8%8E%B7%E5%8F%96%E7%BB%93%E6%9E%9C.%0A%0A%23%23%20%E4%BC%98%E7%82%B9%0A%0A%E9%9D%9E%E9%98%BB%E5%A1%9E%2C%E5%A4%A7%E5%A4%A7%E7%AE%80%E5%8C%96%E5%A4%9A%E7%BA%BF%E7%A8%8B%E5%BC%82%E6%AD%A5%E7%BC%96%E7%A8%8B.%20%E9%9B%86%E6%88%90%60netty%60%E7%AD%89%E6%A1%86%E6%9E%B6%E5%8F%AF%E5%AE%9E%E7%8E%B0%E6%9B%B4%E9%AB%98%E7%9A%84%E7%BD%91%E7%BB%9C%E5%B9%B6%E5%8F%91%E5%A4%84%E7%90%86%E8%83%BD%E5%8A%9B.%20API%E4%B8%B0%E5%AF%8C%2C%E5%AE%9E%E7%8E%B0%E5%BE%88%E5%A4%9A%E5%A4%8D%E6%9D%82%E7%9A%84%E5%8A%9F%E8%83%BD%E5%8F%AA%E9%9C%80%E8%A6%81%E5%87%A0%E8%A1%8C%E4%BB%A3%E7%A0%81%2C%E4%BE%8B%E5%A6%82%3A%0A%0A1.%20%E5%89%8D%E7%AB%AF%E5%B1%95%E7%A4%BA%E5%AE%9E%E6%97%B6%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E8%BF%9B%E5%BA%A6.%0A2.%20%E8%AF%B7%E6%B1%82%E6%92%A4%E9%94%80%2C%E5%8F%AF%E8%8E%B7%E5%8F%96%E5%88%B0%E8%BF%9E%E6%8E%A5%E6%96%AD%E5%BC%80%E4%BA%8B%E4%BB%B6.%0A3.%20%E5%AE%9A%E6%97%B6(%60interval%60)%2C%E5%BB%B6%E8%BF%9F(%60delay%60)%2C%E8%B6%85%E6%97%B6(%60timout%60)%2C%E4%BB%A5%E5%8F%8A%E7%BB%86%E7%B2%92%E5%BA%A6%E7%9A%84%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6(%60limitRate%60).%0A4.%20%E5%88%86%E7%BB%84(%60groupBy%60)%2C%E8%81%9A%E5%90%88(%60collect%60%2C%60reduce%60)%E6%93%8D%E4%BD%9C%E7%AD%89%0A%0A%23%23%20%E7%BC%BA%E7%82%B9%0A%0A%E8%B0%83%E8%AF%95%E4%B8%8D%E6%98%93%2C%E5%BC%82%E5%B8%B8%E6%A0%88%E9%9A%BE%E8%B7%9F%E8%B8%AA%2C%E5%AF%B9%E5%BC%80%E5%8F%91%E4%BA%BA%E5%91%98%E6%9C%89%E6%9B%B4%E9%AB%98%E7%9A%84%E8%A6%81%E6%B1%82.%0A%0A%E6%AD%A4%E9%97%AE%E9%A2%98%E5%8F%AF%E4%BB%A5%E9%80%9A%E8%BF%87%E4%BC%98%E5%8C%96%E4%BB%A3%E7%A0%81%E7%BB%93%E6%9E%84%E6%9D%A5%E8%A7%A3%E5%86%B3%2C%E6%AF%94%E5%A6%82%3A%20%E9%81%BF%E5%85%8D%E5%9C%A8%E5%93%8D%E5%BA%94%E5%BC%8F%E6%93%8D%E4%BD%9C%E7%AC%A6%E4%B8%AD%E7%9B%B4%E6%8E%A5%E4%B8%9A%E5%8A%A1%E9%80%BB%E8%BE%91%2C%20%E6%AD%A3%E7%A1%AE%E7%9A%84%E5%81%9A%E6%B3%95%E6%98%AF%E5%B0%86%E4%B8%9A%E5%8A%A1%E9%80%BB%E8%BE%91%E6%8A%BD%E7%A6%BB%E4%B8%BA%E7%8B%AC%E7%AB%8B%E7%9A%84%E5%87%BD%E6%95%B0(%E6%96%B9%E6%B3%95)%2C%E7%84%B6%E5%90%8E%E4%BD%BF%E7%94%A8%E5%93%8D%E5%BA%94%E5%BC%8F%E6%9D%A5%E8%BF%9B%E8%A1%8C%E7%BB%84%E5%90%88.%0A%0A%E6%B3%A8%E6%84%8F%0A%0A%E5%93%8D%E5%BA%94%E5%BC%8F%E5%8F%AA%E6%98%AF%E4%B8%80%E4%B8%AA%E7%BC%96%E7%A8%8B%E6%A8%A1%E5%9E%8B%2C%E5%B9%B6%E4%B8%8D%E8%83%BD%E7%9B%B4%E6%8E%A5%E6%8F%90%E9%AB%98%E7%B3%BB%E7%BB%9F%E7%9A%84%E5%B9%B6%E5%8F%91%E5%A4%84%E7%90%86%E8%83%BD%E5%8A%9B.%20%E9%80%9A%E5%B8%B8%E4%B8%8Enetty(%60reactor-netty%60)%E7%AD%89%E6%A1%86%E6%9E%B6%E9%85%8D%E5%90%88%2C%E4%BB%8E%E4%B8%8A(%60%E7%BD%91%E7%BB%9C%60)%E5%88%B0%E4%B8%8B(%60%E6%8C%81%E4%B9%85%E5%8C%96%60)%E5%85%A8%E5%A5%97%E5%AE%9E%E7%8E%B0%60%E9%9D%9E%E9%98%BB%E5%A1%9E%60%2C%60%E5%93%8D%E5%BA%94%E5%BC%8F%60%E6%89%8D%E6%9C%89%E6%84%8F%E4%B9%89.%0A%0A%23%23%20%E9%80%89%E6%8B%A9%E5%90%88%E9%80%82%E7%9A%84%E6%93%8D%E4%BD%9C%E7%AC%A6%0A%0A%E7%B3%BB%E7%BB%9F%E4%B8%AD%E5%A4%A7%E9%87%8F%E4%BD%BF%E7%94%A8%E5%88%B0%E4%BA%86%60reactor%60%2C%E5%85%B6%E6%A0%B8%E5%BF%83%E7%B1%BB%E5%8F%AA%E6%9C%892%E4%B8%AA%60Flux%60(0-n%E4%B8%AA%E6%95%B0%E6%8D%AE%E7%9A%84%E6%B5%81)%2C%60Mono%60(0-1%E4%B8%AA%E6%95%B0%E6%8D%AE%E7%9A%84%E6%B5%81).%20%E6%91%92%E5%BC%83%60%E4%BC%A0%E7%BB%9F%E7%BC%96%E7%A8%8B%60%E7%9A%84%E6%80%9D%E6%83%B3%2C%E7%86%9F%E6%82%89%60Flux%60%2C%60Mono%60%E6%93%8D%E4%BD%9C%E7%AC%A6(API)%2C%E5%B0%B1%E5%8F%AF%E4%BB%A5%E5%BE%88%E5%A5%BD%E7%9A%84%E4%BD%BF%E7%94%A8%E5%93%8D%E5%BA%94%E5%BC%8F%E7%BC%96%E7%A8%8B%E4%BA%86.%0A%0A%E5%B8%B8%E7%94%A8%E6%93%8D%E4%BD%9C%E7%AC%A6%3A%0A%0A1.%20%60map%60%3A%20%E8%BD%AC%E6%8D%A2%E6%B5%81%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0%3A%20%60flux.map(UserEntity%3A%3AgetId)%60%0A2.%20%60mapNotNull%60%3A%20%E8%BD%AC%E6%8D%A2%E6%B5%81%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0%2C%E5%B9%B6%E5%BF%BD%E7%95%A5null%E5%80%BC.(%60reactor%203.4%60%E6%8F%90%E4%BE%9B)%0A3.%20%60flatMap%60%3A%20%E8%BD%AC%E6%8D%A2%E6%B5%81%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0%E4%B8%BA%E6%96%B0%E7%9A%84%E6%B5%81%3A%20%60flux.flatMap(this%3A%3AfindById)%60%0A4.%20%60flatMapMany%60%3A%20%E8%BD%AC%E6%8D%A2Mono%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0%E4%B8%BAFlux(1%E4%B8%AA%E8%BD%AC%E5%A4%9A%E4%B8%AA)%3A%20%60mono.flatMapMany(this%3A%3AfindChildren)%60%0A5.%20%60concat%60%3A%20%E5%B0%86%E5%A4%9A%E4%B8%AA%E6%B5%81%E8%BF%9E%E6%8E%A5%E5%9C%A8%E4%B8%80%E8%B5%B7%E7%BB%84%E6%88%90%E4%B8%80%E4%B8%AA%E6%B5%81(%E6%8C%89%E9%A1%BA%E5%BA%8F%E8%AE%A2%E9%98%85)%20%3A%20%60Flux.concat(header%2Cbody)%60%0A6.%20%60merge%60%3A%20%E5%B0%86%E5%A4%9A%E4%B8%AA%E6%B5%81%E5%90%88%E5%B9%B6%E5%9C%A8%E4%B8%80%E8%B5%B7%2C%E5%90%8C%E6%97%B6%E8%AE%A2%E9%98%85%E6%B5%81%3A%20%60Flux.merge(save(info)%2CsaveDetail(detail))%60%0A7.%20%60zip%60%3A%20%E5%8E%8B%E7%BC%A9%E5%A4%9A%E4%B8%AA%E6%B5%81%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0%3A%20%60Mono.zip(getData(id)%2CgetDetail(id)%2CUserInfo%3A%3Aof)%60%0A8.%20%60then%60%3A%20%E4%B8%8A%E6%B8%B8%E6%B5%81%E5%AE%8C%E6%88%90%E5%90%8E%E6%89%A7%E8%A1%8C%E5%85%B6%E4%BB%96%E7%9A%84%E6%93%8D%E4%BD%9C.%0A9.%20%60doOnNext%60%3A%20%E6%B5%81%E4%B8%AD%E4%BA%A7%E7%94%9F%E6%95%B0%E6%8D%AE%E6%97%B6%E6%89%A7%E8%A1%8C.%0A10.%20%60doOnError%60%3A%20%E5%8F%91%E9%80%81%E9%94%99%E8%AF%AF%E6%97%B6%E6%89%A7%E8%A1%8C.%0A11.%20%60doOnCancel%60%3A%20%E6%B5%81%E8%A2%AB%E5%8F%96%E6%B6%88%E6%97%B6%E6%89%A7%E8%A1%8C.%E5%A6%82%3A%20http%E6%9C%AA%E5%93%8D%E5%BA%94%E5%89%8D%2C%E5%AE%A2%E6%88%B7%E7%AB%AF%E6%96%AD%E5%BC%80%E4%BA%86%E8%BF%9E%E6%8E%A5.%0A12.%20%60onErrorContinue%60%3A%20%E6%B5%81%E5%8F%91%E7%94%9F%E9%94%99%E8%AF%AF%E6%97%B6%2C%E7%BB%A7%E7%BB%AD%E5%A4%84%E7%90%86%E6%95%B0%E6%8D%AE%E8%80%8C%E4%B8%8D%E6%98%AF%E7%BB%88%E6%AD%A2%E6%95%B4%E4%B8%AA%E6%B5%81.%0A13.%20%60defaultIfEmpty%60%3A%20%E5%BD%93%E6%B5%81%E4%B8%BA%E7%A9%BA%E6%97%B6%2C%E4%BD%BF%E7%94%A8%E9%BB%98%E8%AE%A4%E5%80%BC.%0A14.%20%60switchIfEmpty%60%3A%20%E5%BD%93%E6%B5%81%E4%B8%BA%E7%A9%BA%E6%97%B6%2C%E5%88%87%E6%8D%A2%E4%B8%BA%E5%8F%A6%E5%A4%96%E4%B8%80%E4%B8%AA%E6%B5%81.%0A15.%20%60as%60%3A%20%E5%B0%86%E6%B5%81%E4%BD%9C%E4%B8%BA%E5%8F%82%E6%95%B0%2C%E8%BD%AC%E4%B8%BA%E5%8F%A6%E5%A4%96%E4%B8%80%E4%B8%AA%E7%BB%93%E6%9E%9C%3A%60flux.as(this%3A%3Asave)%60%0A%0A%E5%AE%8C%E6%95%B4%E6%96%87%E6%A1%A3%E8%AF%B7%E6%9F%A5%E7%9C%8B%5B%E5%AE%98%E6%96%B9%E6%96%87%E6%A1%A3%5D(https%3A%2F%2Fprojectreactor.io%2Fdocs%2Fcore%2Frelease%2Freference%2F%23which-operator)%0A%0A%23%23%20%E4%BB%A3%E7%A0%81%E6%A0%BC%E5%BC%8F%E5%8C%96%0A%0A%E4%BD%BF%E7%94%A8%60reactor%60%E6%97%B6%2C%E5%BA%94%E8%AF%A5%E6%B3%A8%E6%84%8F%E4%BB%A3%E7%A0%81%E5%B0%BD%E9%87%8F%E4%BB%A5%60.%60%E6%8D%A2%E8%A1%8C%E5%B9%B6%E5%81%9A%E5%A5%BD%E7%9B%B8%E5%BA%94%E5%88%B0%E7%BC%A9%E8%BF%9B.%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%0A%2F%2F%E9%94%99%E8%AF%AF%0Areturn%20paramMono.map(param-%3Eparam.getString(%22id%22)).flatMap(this%3A%3AfindById)%3B%0A%0A%2F%2F%E5%BB%BA%E8%AE%AE%0Areturn%20paramMono%0A%20%20%20%20%20%20%20%20%20%20%20%20.map(param-%3Eparam.getString(%22id%22))%20%0A%20%20%20%20%20%20%20%20%20%20%20%20.flatMap(this%3A%3AfindById)%3B%0A%0A%60%60%60%0A%0A%23%23%20lamdba%0A%0A%E9%81%BF%E5%85%8D%E5%9C%A8%E4%B8%80%E4%B8%AA%60lambda%60%E4%B8%AD%E7%BC%96%E5%86%99%E5%A4%A7%E9%87%8F%E7%9A%84%E9%80%BB%E8%BE%91%E4%BB%A3%E7%A0%81%2C%E6%8E%A8%E8%8D%90%E5%8F%82%E8%80%83%60%E9%A2%86%E5%9F%9F%E6%A8%A1%E5%9E%8B%60%2C%E5%B0%86%E5%85%B7%E4%BD%93%E5%BD%93%E9%80%BB%E8%BE%91%E6%94%BE%E5%88%B0%E5%AF%B9%E5%BA%94%E5%88%B0%60%E5%AE%9E%E4%BD%93%60%E6%88%96%E8%80%85%60%E9%A2%86%E5%9F%9F%E5%AF%B9%E8%B1%A1%60%E4%B8%AD.%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%0A%2F%2F%E9%94%99%E8%AF%AF%0Areturn%20devicePropertyMono%0A%20%20%20%20%20%20%20%20.map(prop-%3E%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20Map%3CString%2CObject%3E%20map%20%3D%20new%20HashMap%3C%3E()%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20map.put(%22property%22%2Cprop.getProperty())%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20….%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20map%3B%0A%20%20%20%20%20%20%20%20%7D)%0A%20%20%20%20%20%20%20%20.flatMap(this%3A%3AdoSomeThing)%0A%0A%2F%2F%E5%BB%BA%E8%AE%AE%0A%2F%2F%E5%9C%A8DeviceProperty%E4%B8%AD%E7%BC%96%E5%86%99toMap%E6%96%B9%E6%B3%95%E5%AE%9E%E7%8E%B0%E4%B8%8A%E9%9D%A2lambda%E4%B8%AD%E5%88%B0%E9%80%BB%E8%BE%91.%0Areturn%20devicePropertyMono%0A%20%20%20%20%20%20%20%20.map(DeviceProperty%3A%3AtoMap)%0A%20%20%20%20%20%20%20%20.flatMap(this%3A%3AdoSomeThing)%0A%0A%60%60%60%0A%0A%23%23%20null%E5%A4%84%E7%90%86%0A%0A%E6%95%B0%E6%8D%AE%E6%B5%81%E4%B8%AD%E5%88%B0%E5%85%83%E7%B4%A0%E4%B8%8D%E5%85%81%E8%AE%B8%E4%B8%BA%60null%60%2C%E5%9B%A0%E6%AD%A4%E5%9C%A8%E8%BF%9B%E8%A1%8C%E6%95%B0%E6%8D%AE%E8%BD%AC%E6%8D%A2%E5%88%B0%E6%97%B6%E5%80%99%E8%A6%81%E6%B3%A8%E6%84%8F%60null%60%E5%A4%84%E7%90%86.%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%0A%2F%2F%E5%AD%98%E5%9C%A8%E7%BC%BA%E9%99%B7%0Areturn%20this.findById(id)%0A%20%20%20%20%20%20%20%20%20%20%20.map(UserEntity%3A%3AgetDescription)%3B%20%2F%2FgetDescription%E5%8F%AF%E8%83%BD%E8%BF%94%E5%9B%9Enull%2C%E4%B8%BAnull%E6%97%B6%E4%BC%9A%E6%8A%9B%E5%87%BA%E7%A9%BA%E6%8C%87%E9%92%88%2C%0A%0A%60%60%60%0A%0A%E5%9C%A8%60reactor%203.4%60%E5%90%8E%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E4%BB%A5%E4%B8%8B%E6%96%B9%E5%BC%8F%E6%9D%A5%E5%A4%84%E7%90%86%E5%8F%AF%E8%83%BD%E5%AD%98%E5%9C%A8null%E7%9A%84map%E6%93%8D%E4%BD%9C%0A%0A%60%60%60java%0Areturn%20this.findById(id)%0A%20%20%20%20%20%20%20%20%20%20%20.mapNotNull(UserEntity%3A%3AgetDescription)%3B%20%0A%60%60%60%0A%0A%23%23%20%E9%9D%9E%E9%98%BB%E5%A1%9E%E4%B8%8E%E9%98%BB%E5%A1%9E%0A%0A%E9%BB%98%E8%AE%A4%E6%83%85%E5%86%B5%E4%B8%8B%2C%60reactor%60%E7%9A%84%E8%B0%83%E5%BA%A6%E5%99%A8%E7%94%B1%E6%95%B0%E6%8D%AE%E7%9A%84%E7%94%9F%E4%BA%A7%E8%80%85(%60Publisher%60)%E5%86%B3%E5%AE%9A%2C%E5%9C%A8%60WebFlux%60%E4%B8%AD%E5%88%99%E6%98%AF%60netty%60%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%BA%BF%E7%A8%8B%2C%20%E4%B8%BA%E4%BA%86%E9%98%B2%E6%AD%A2%E5%B7%A5%E4%BD%9C%E7%BA%BF%E7%A8%8B%E8%A2%AB%E9%98%BB%E5%A1%9E%E5%AF%BC%E8%87%B4%E6%9C%8D%E5%8A%A1%E5%B4%A9%E6%BA%83%2C%E5%9C%A8%E4%B8%80%E4%B8%AA%E8%AF%B7%E6%B1%82%E7%9A%84%E6%B5%81%E4%B8%AD%2C%E7%A6%81%E6%AD%A2%E6%89%A7%E8%A1%8C%E5%AD%98%E5%9C%A8%E9%98%BB%E5%A1%9E(%E5%A6%82%E6%89%A7%E8%A1%8C%60JDBC%60)%E5%8F%AF%E8%83%BD%E7%9A%84%E6%93%8D%E4%BD%9C%E7%9A%84%2C%E5%A6%82%E6%9E%9C%E6%97%A0%E6%B3%95%E9%81%BF%E5%85%8D%E9%98%BB%E5%A1%9E%E6%93%8D%E4%BD%9C%2C%E5%BA%94%E8%AF%A5%E6%8C%87%E5%AE%9A%E8%B0%83%E5%BA%A6%E5%99%A8%E5%A6%82%3A%0A%0A%60%60%60java%0AparamMono%0A%20%20.publishOn(Schedulers.elastic())%20%2F%2F%E6%8C%87%E5%AE%9A%E8%B0%83%E5%BA%A6%E5%99%A8%E5%8E%BB%E6%89%A7%E8%A1%8C%E4%B8%8B%E9%9D%A2%E7%9A%84%E6%93%8D%E4%BD%9C%0A%20%20.map(param-%3E%20jdbcService.select(param))%0A%60%60%60%0A%0A%23%23%20%E4%B8%8A%E4%B8%8B%E6%96%87%0A%0A%E5%9C%A8%E5%93%8D%E5%BA%94%E5%BC%8F%E4%B8%AD%2C%E5%A4%A7%E9%83%A8%E5%88%86%E6%83%85%E5%86%B5%E6%98%AF%E7%A6%81%E6%AD%A2%E4%BD%BF%E7%94%A8%60ThreadLocal%60%E7%9A%84(%E5%8F%AF%E8%83%BD%E9%80%A0%E6%88%90%E5%86%85%E5%AD%98%E6%B3%84%E6%BC%8F).%E5%9B%A0%E6%AD%A4%E5%9F%BA%E4%BA%8E%60ThreadLocal%60%E7%9A%84%E5%8A%9F%E8%83%BD%E9%83%BD%E6%97%A0%E6%B3%95%E4%BD%BF%E7%94%A8%2Creactor%E4%B8%AD%E5%BC%95%E5%85%A5%E4%BA%86%E4%B8%8A%E4%B8%8B%E6%96%87%2C%E5%9C%A8%E4%B8%80%E4%B8%AA%E6%B5%81%E4%B8%AD%2C%E5%8F%AF%E5%85%B1%E4%BA%AB%E6%AD%A4%E4%B8%8A%E4%B8%8B%E6%96%87%20%2C%E9%80%9A%E8%BF%87%E4%B8%8A%E4%B8%8B%E6%96%87%E8%BF%9B%E8%A1%8C%E5%8F%98%E9%87%8F%E5%85%B1%E4%BA%AB%E4%BB%A5%E4%BE%8B%E5%A6%82%3A%60%E4%BA%8B%E5%8A%A1%60%2C%60%E6%9D%83%E9%99%90%60%E7%AD%89%E5%8A%9F%E8%83%BD.%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%0A%2F%2F%E4%BB%8E%E4%B8%8A%E4%B8%8B%E6%96%87%E4%B8%AD%E8%8E%B7%E5%8F%96%0A%40GetMapping%0Apublic%20Mono%3CUserInfo%3E%20getCurrentUser()%7B%0A%20%20%20%20return%20Mono.subscriberContext()%0A%20%20%20%20%20%20%20%20%20%20%20%20.map(ctx-%3EuserService.findById(ctx.getOrEmpty(%22userId%22).orElseThrow(IllegalArgumentException%3A%3Anew))%3B%0A%7D%0A%0A%2F%2F%E5%AE%9A%E4%B9%89%E8%BF%87%E6%BB%A4%E5%99%A8%E8%AE%BE%E7%BD%AE%E6%95%B0%E6%8D%AE%E5%88%B0%E4%B8%8A%E4%B8%8B%E6%96%87%E4%B8%AD%0Aclass%20MyFilter%20implements%20WebFilter%7B%0A%20%20%20%20public%20Mono%3CVoid%3E%20filter(ServerWebExchange%20exchange%2C%20WebFilterChain%20chain)%7B%0A%20%20%20%20%20%20%20%20return%20chain.filter(exchange)%0A%20%20%20%20%20%20%20%20%20%20%20%20.subscriberContext(Context.of(%22userId%22%2C…))%0A%20%20%20%20%7D%0A%7D%0A%0A%60%60%60%0A%0A%E6%B3%A8%E6%84%8F%0A%0A%E5%9C%A8%E5%BC%80%E5%8F%91%E4%B8%AD%E5%BA%94%E8%AF%A5%E5%B0%86%E5%A4%9A%E4%B8%AA%E6%B5%81%E7%BB%84%E5%90%88%E4%B8%BA%E4%B8%80%E4%B8%AA%E6%B5%81%2C%E8%80%8C%E4%B8%8D%E6%98%AF%E5%88%86%E5%88%AB%E5%A4%84%E7%90%86.%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%2F%2F%E9%94%99%E8%AF%AF%0Areturn%20flux.doOnNext(data-%3Ethis.save(data).subscribe())%3B%0A%0A%2F%2F%E6%AD%A3%E7%A1%AE%0Areturn%20flux.flatMap(this%3A%3Asave)%3B%0A%0A%2F%2F%E9%94%99%E8%AF%AF%2C%E6%B2%A1%E6%9C%89%E5%B0%86%E6%B5%81%E7%BB%84%E5%90%88%E5%9C%A8%E4%B8%80%E8%B5%B7%0Arequest.flatMap(this%3A%3Asave)%3B%0AMono%3CVoid%3E%20result%20%3D%20this.notifySaveSuccess()%3B%0Areturn%20result%3B%0A%0A%2F%2F%E6%AD%A3%E7%A1%AE%0Areturn%20request%0A%20%20%20%20.flatMap(this%3A%3Asave)%0A%20%20%20%20.then(this.notifySaveSuccess())%3B%0A%0A%60%60%60%0A%0A%23%23%20FAQ%3A%20%E6%88%91%E5%86%99%E7%9A%84%E6%93%8D%E4%BD%9C%E7%9C%8B%E4%B8%8A%E5%8E%BB%E6%98%AF%E6%AD%A3%E7%A1%AE%E7%9A%84%2C%E4%BD%86%E6%98%AF%E6%B2%A1%E6%9C%89%E6%89%A7%E8%A1%8C.%0A%0A%E6%9C%893%E7%A7%8D%E5%8F%AF%E8%83%BD%3A%20%60%E4%B8%8A%E6%B8%B8%E6%B5%81%E4%B8%BA%E7%A9%BA%60%2C%60%E5%A4%9A%E4%B8%AA%E6%B5%81%E6%9C%AA%E7%BB%84%E5%90%88%E5%9C%A8%E4%B8%80%E8%B5%B7%60%2C%60%E5%9C%A8%E4%B8%8D%E6%94%AF%E6%8C%81%E5%93%8D%E5%BA%94%E5%BC%8F%E7%9A%84%E5%9C%B0%E6%96%B9%E4%BD%BF%E7%94%A8%E4%BA%86%E5%93%8D%E5%BA%94%E5%BC%8F%60%0A%0A%E4%B8%8A%E6%B8%B8%E6%B5%81%E4%B8%BA%E7%A9%BA%3A%0A%0A%E4%BE%8B%3A%0A%0A%0A%60%60%60java%0Apublic%20Mono%3CResponse%3E%20handleRequest(Request%20request)%7B%0A%20%20%20%0A%20return%20this%0A%20%20%20%20%20%20.findOldData(request)%0A%20%20%20%20%20%20.flatMap(old%20-%3E%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%2F%2F%E8%BF%99%E9%87%8C%E4%B8%BA%E4%BB%80%E4%B9%88%E4%B8%8D%E6%89%A7%E8%A1%8C%3F%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20….%0A%20%20%20%20%20%20%7D)%0A%20%0A%7D%0A%0A%60%60%60%0A%0A%E8%AF%B4%E6%98%8E%0A%0A%E5%BD%93%60findOldData%60%E8%BF%94%E5%9B%9E%E7%9A%84%E6%B5%81%E4%B8%BA%E7%A9%BA%E6%97%B6%2C%E4%B8%8B%E6%B8%B8%E7%9A%84%60flatMap%60%E7%AD%89%E9%9C%80%E8%A6%81%60%E6%93%8D%E4%BD%9C%E6%B5%81%E4%B8%AD%E5%85%83%E7%B4%A0%E7%9A%84%E6%93%8D%E4%BD%9C%E7%AC%A6%60%E6%98%AF%E4%B8%8D%E4%BC%9A%E6%89%A7%E8%A1%8C%E7%9A%84.%20%E5%8F%AF%E4%BB%A5%E9%80%9A%E8%BF%87%60switchIfEmpty%60%E6%93%8D%E4%BD%9C%E7%AC%A6%E6%9D%A5%E5%A4%84%E7%90%86%E7%A9%BA%E6%B5%81%E7%9A%84%E6%83%85%E5%86%B5.%20%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%20return%20this%0A%20%20%20%20%20%20.findOldData(request)%0A%20%20%20%20%20%20%2F%2F%E5%A4%84%E7%90%86%E6%B2%A1%E8%8E%B7%E5%8F%96%E5%88%B0%E6%95%B0%E6%8D%AE%E7%9A%84%E6%83%85%E5%86%B5%0A%20%20%20%20%20%20.switchIfEmpty(Mono.error(()-%3Enew%20NotFoundException(%22error.data_not_found%22)))%0A%20%20%20%20%20%20.flatMap(old%20-%3E%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20….%0A%20%20%20%20%20%20%7D)%0A%60%60%60%0A%0A%E5%A6%82%E6%9E%9C%60flatMap%60%E5%92%8C%60switchIfEmpty%60%E4%B8%AD%E7%9A%84%E9%80%BB%E8%BE%91%E9%83%BD%E6%B2%A1%E6%89%A7%E8%A1%8C%2C%E9%82%A3%E5%8F%AF%E8%83%BD%E6%98%AF%E4%B8%8B%E9%9D%A2%E4%B8%80%E7%A7%8D%E6%83%85%E5%86%B5.%0A%0A%E5%A4%9A%E4%B8%AA%E6%B5%81%E6%9C%AA%E7%BB%84%E5%90%88%E5%9C%A8%E4%B8%80%E8%B5%B7%0A%0A%E4%BE%8B%3A%0A%0A%60%60%60java%0A%0Apublic%20Result%20handleRequest(Request%20request)%7B%0A%20%0A%20%20%20%20%20%2F%2F%E5%A4%84%E7%90%86%E8%AF%B7%E6%B1%82%0A%20%20%20%20%20service.handleRequest(request)%3B%0A%0A%20%20%20%20%20return%20ok%3B%0A%0A%7D%0A%0A%60%60%60%0A%0A%E6%B3%A8%E6%84%8F%0A%0A1.%20%E5%8F%AA%E8%A6%81%E6%96%B9%E6%B3%95%E8%BF%94%E5%9B%9E%E5%80%BC%E6%98%AF%60Mono%60%E6%88%96%E8%80%85%60Flux%60%2C%E9%83%BD%E4%B8%8D%E8%83%BD%E5%8D%95%E7%8B%AC%E8%A1%8C%E5%8A%A8.%0A2.%20%E5%8F%AA%E8%A6%81%E6%96%B9%E6%B3%95%E4%B8%AD%E8%B0%83%E7%94%A8%E4%BA%86%E4%BB%BB%E4%BD%95%E5%93%8D%E5%BA%94%E5%BC%8F%E6%93%8D%E4%BD%9C.%E9%82%A3%E8%BF%99%E4%B8%AA%E6%96%B9%E6%B3%95%E4%B9%9F%E5%BA%94%E8%AF%A5%E6%98%AF%E5%93%8D%E5%BA%94%E5%BC%8F.(%E8%BF%94%E5%9B%9EMono%E6%88%96%E8%80%85Flux)%0A%0A%E5%9B%A0%E6%AD%A4%E6%AD%A3%E7%A1%AE%E7%9A%84%E5%86%99%E6%B3%95%E6%98%AF%3A%0A%0A%60%60%60java%0Apublic%20Mono%3CResult%3E%20handleRequest(Request%20request)%7B%0A%20return%20service%0A%20%20%20%20%20%20%20%20%20%2F%2F%E5%A4%84%E7%90%86%E8%AF%B7%E6%B1%82%0A%20%20%20%20%20%20%20%20%20.handleRequest(request)%0A%20%20%20%20%20%20%20%20%20%2F%2F%E8%AE%B0%E5%BD%95%E6%97%A5%E5%BF%97%0A%20%20%20%20%20%20%20%20%20.then(saveLog(request))%0A%20%20%20%20%20%20%20%20%20%2F%2F%E8%BF%94%E5%9B%9E%E7%BB%93%E6%9E%9C%0A%20%20%20%20%20%20%20%20%20.thenReturn(ok)%3B%0A%7D%0A%60%60%60%0A%0A%E5%9C%A8%E4%B8%8D%E6%94%AF%E6%8C%81%E5%93%8D%E5%BA%94%E5%BC%8F%E7%9A%84%E5%9C%B0%E6%96%B9%E4%BD%BF%E7%94%A8%E5%93%8D%E5%BA%94%E5%BC%8F%0A%0A%0A%60%60%60java%0Apublic%20Mono%3CResult%3E%20handleRequest(Request%20request)%7B%0A%0Areturn%20service%0A%20%20%20%20%20%20%20%20%20%2F%2F%E5%A4%84%E7%90%86%E8%AF%B7%E6%B1%82%0A%20%20%20%20%20%20%20%20%20.handleRequest(request)%0A%20%20%20%20%20%20%20%20%20%2F%2F%E8%AE%B0%E5%BD%95%E6%97%A5%E5%BF%97%20%E6%AD%A4%E4%B8%BA%E9%94%99%E8%AF%AF%E7%9A%84%E7%94%A8%E6%B3%95%0A%20%20%20%20%20%20%20%20%20.doOnNext(response-%3E%20saveLog(request%2Cresponse)%20)%0A%20%20%20%20%20%20%20%20%20%2F%2F%E8%BF%94%E5%9B%9E%E7%BB%93%E6%9E%9C%0A%20%20%20%20%20%20%20%20%20.thenReturn(ok)%3B%0A%7D%0A%60%60%60%0A%0A%E8%AF%B4%E6%98%8E%0A%0A%E4%BB%8E%60doOnNext%60%E6%96%B9%E6%B3%95%E7%9A%84%E8%AF%AD%E4%B9%89%E4%BB%A5%E5%8F%8A%E5%8F%82%E6%95%B0%60Consumer%3CT%3E%60%E5%8F%AF%E7%9F%A5%2C%E6%AD%A4%E6%96%B9%E6%B3%95%E6%98%AF%E4%B8%8D%E6%94%AF%E6%8C%81%E5%93%8D%E5%BA%94%E5%BC%8F%E7%9A%84%EF%BC%88%60Consumer%3CT%3E%E5%8F%AA%E6%9C%89%E5%8F%82%E6%95%B0%E6%B2%A1%E6%9C%89%E8%BF%94%E5%9B%9E%E5%80%BC%60%EF%BC%89%2C%E5%9B%A0%E6%AD%A4%E4%B8%8D%E8%83%BD%E5%9C%A8%E6%AD%A4%E6%96%B9%E6%B3%95%E4%B8%AD%E4%BD%BF%E7%94%A8%E5%93%8D%E5%BA%94%E5%BC%8F%E6%93%8D%E4%BD%9C.%0A%0A%E6%AD%A3%E7%A1%AE%E7%9A%84%E5%86%99%E6%B3%95%3A%0A%0A%60%60%60java%0Areturn%20service%0A%20%20%20%20%20%20%20%20%20%2F%2F%E5%A4%84%E7%90%86%E8%AF%B7%E6%B1%82%0A%20%20%20%20%20%20%20%20%20.handleRequest(request)%0A%20%20%20%20%20%20%20%20%20%2F%2F%E8%AE%B0%E5%BD%95%E6%97%A5%E5%BF%97%20%E6%AD%A4%E4%B8%BA%E9%94%99%E8%AF%AF%E7%9A%84%E7%94%A8%E6%B3%95%0A%20%20%20%20%20%20%20%20%20.flatMap(response-%3E%20saveLog(request%2Cresponse)%20)%0A%20%20%20%20%20%20%20%20%20%2F%2F%E8%BF%94%E5%9B%9E%E7%BB%93%E6%9E%9C%0A%20%20%20%20%20%20%20%20%20.thenReturn(ok)%3B%0A%60%60%60%0A%0A%23%23%20FAQ%3A%20%E6%88%91%E6%83%B3%E8%8E%B7%E5%8F%96%E6%B5%81%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0%E6%80%8E%E4%B9%88%E5%8A%9E%0A%0A%E4%B8%8D%E8%A6%81%E8%AF%95%E5%9B%BE%E4%BB%8E%E6%B5%81%E4%B8%AD%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E5%87%BA%E6%9D%A5%2C%E8%80%8C%E6%98%AF%E5%85%88%E6%80%9D%E8%80%83%E9%9C%80%E8%A6%81%E5%AF%B9%E6%B5%81%E4%B8%AD%E5%85%83%E7%B4%A0%E5%81%9A%E4%BB%80%E4%B9%88%2C%20%E9%9C%80%E8%A6%81%E5%AF%B9%E6%B5%81%E4%B8%AD%E7%9A%84%E6%95%B0%E6%8D%AE%E8%BF%9B%E8%A1%8C%E6%93%8D%E4%BD%9C%E6%97%B6%2C%E9%83%BD%E5%BA%94%E8%AF%A5%E4%BD%BF%E7%94%A8%E6%93%8D%E4%BD%9C%E7%AC%A6%E6%9D%A5%E5%A4%84%E7%90%86%2C%E6%A0%B9%E6%8D%AE%60Flux%E6%88%96%E8%80%85Mono%60%E6%8F%90%E4%BE%9B%E7%9A%84%E6%93%8D%E4%BD%9C%E7%AC%A6API%E8%BF%9B%E8%A1%8C%E7%BB%84%E5%90%88%E6%93%8D%E4%BD%9C.%E6%AF%94%E5%A6%82%3A%0A%0A%E4%BC%A0%E7%BB%9F%3A%0A%0A%60%60%60java%0A%0Apublic%20List%3CBook%3E%20getAllBooks()%7B%0A%20%20%20%20List%3CBookEntity%3E%20bookEntities%20%3D%20repository.findAll()%3B%0A%0A%20%20%20%20List%3CBook%3E%20books%20%3D%20new%20ArrayList(bookEntities.size())%3B%0A%0A%20%20%20%20for(BookEntity%20entity%20%3A%20bookEntities)%7B%0A%20%20%20%20%20%20%20%20Book%20book%20%3D%20entity.copyTo(new%20Book())%3B%0A%20%20%20%20%20%20%20%20books.add(book)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20return%20books%3B%0A%7D%0A%60%60%60%0A%0A%E5%93%8D%E5%BA%94%E5%BC%8F%3A%0A%0A%60%60%60java%0Apublic%20Flux%3CBook%3E%20getAllBooks()%7B%0Areturn%20repository%0A%20%20%20%20%20%20%20%20.findAll()%0A%20%20%20%20%20%20%20%20.map(entity-%3E%20entity.copyTo(new%20Book()))%0A%7D%0A%0A%60%60%60%0A%0A%23%23%20FAQ%3A%20%E6%88%91%E9%9C%80%E8%A6%81%E5%9C%A8%E9%9D%9E%E5%93%8D%E5%BA%94%E5%BC%8F%E6%96%B9%E6%B3%95%E4%B8%AD%E4%BD%BF%E7%94%A8%E5%93%8D%E5%BA%94%E5%BC%8F%E6%80%8E%E4%B9%88%E5%8A%9E%0A%0A%E5%A6%82%E6%9E%9C%E9%9C%80%E8%A6%81%E9%98%BB%E5%A1%9E%E8%8E%B7%E5%8F%96%E7%BB%93%E6%9E%9C%2C%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%60flux.block(timeout)%60.%0A%0A%E5%A6%82%E6%9E%9C%E9%9C%80%E8%A6%81%E5%BC%82%E6%AD%A5%E8%8E%B7%E5%8F%96%E7%BB%93%E6%9E%9C%2C%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%60flux.subscribe(data-%3E%7B%20%7D%2Cerror-%3E%7B%20%7D)%60%0A%0A%E5%A6%82%3A%0A%0A%60%60%60java%0Apublic%20void%20handleRequest(Request%20request)%7B%0A%0A%20%20%2F%2FlogService.saveLog(request).block()%0A%20%20%20%20%0A%20%20logService%0A%20%20%20%20.saveLog(request)%0A%20%20%20%20.subscribe(%0A%20%20%20%20%20%20%20%20result-%3E%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20log.debug(%22%E4%BF%9D%E5%AD%98%E6%88%90%E5%8A%9F%20%7B%7D%22%2Crequest)%0A%20%20%20%20%20%20%20%20%7D%2C%0A%20%20%20%20%20%20%20%20error-%3E%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20log.warn(%22%E4%BF%9D%E5%AD%98%E5%A4%B1%E8%B4%A5%20%7B%7D%22%2Crequest%2Cerror)%3B%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20)%0A%7D%0A%60%60%60%0A%0A%23%23%20%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99%0A%0A1.%20%5Breactive-streams%5D(http%3A%2F%2Fwww.reactive-streams.org%2F)%0A2.%20%5Bproject-reactor%5D(https%3A%2F%2Fprojectreactor.io%2F)%0A3.%20%5B%E4%BD%BF%E7%94%A8%20Reactor%20%E8%BF%9B%E8%A1%8C%E5%8F%8D%E5%BA%94%E5%BC%8F%E7%BC%96%E7%A8%8B%5D(https%3A%2F%2Fwww.ibm.com%2Fdeveloperworks%2Fcn%2Fjava%2Fj-cn-with-reactor-response-encode%2Findex.html%3Flnk%3Dhmhm)