---
layout: post
title: JetLinks 使用hsweb-easyorm (opens new window)实现响应式的ORM.
slug: jetlinks-using-hsweb-easyorm-for-reactive-orm
type:
  - note
date: 2023-05-26
status: draft
tags:
  - JetLinks
categories:
  - IoT
mood:
weather:
author: deathwhispers
created: 2023-05-26 11:45
updated: 2023-05-26 18:33
---


# JetLinks 使用hsweb-easyorm (opens new window)实现响应式的ORM.

JetLinks 使用[hsweb-easyorm (opens new window)](https://github.com/hs-web/hsweb-easy-orm)实现响应式的ORM.

## DAO

easyorm封装了r2dbc实现了动态DDL,DSL动态条件等便捷操作.实现一个增删改查只需要2步.

创建实体类,使用jpa注解描述映射关系.

```plain text
@Data
@Table(name="s_test")
public class TestEntity extends GenericEntity<String> {

    @Column
    private String name;

    @Column
    @EnumCodec  //使用枚举进行编解码
    @ColumnType(javaType = String.class)//指定数据库数据类型
    @DefaultValue("disabled")//默认值
    private TestEnum state;

    @Column
    @JsonCodec //json编解码
    @ColumnType(jdbcType = JDBCType.CLOB, javaType = String.class)
    private Map<String,Object> configuration;
}
```

在需要使用crud的地方直接注入ReactiveRepository<TestEntity,String>即可,如:

```plain text
@Autowired
ReactiveRepository<TestEntity,String> testRepository;
```

TIP

启动类上需要注解: @EnableEasyormRepository(“实体类所在包,如: org.jetlinks.community.**.entity”).

### 自定义通用查询条件

## Service

### CRUD Service

hsweb提供了GenericReactiveCrudService,使用ReactiveRepository实现通用增删该查.例如:

```plain text
public class TestService extends GenericReactiveCrudService<TestEntity,String>{
}
```

### 支持缓存的Service

GenericReactiveCacheSupportCrudService

```plain text
@Service
public class TestService extends GenericReactiveCacheSupportCrudService<TestEntity, String> {

    @Override
    public String getCacheName() {
        return "test-entity-cache";
    }
}
```

### 支持树结构实体的Service

GenericReactiveTreeSupportCrudService,提供了对树结构数据对一些通用处理,如List与树结构互转.

```plain text
@Service
public class TestService extends GenericReactiveTreeSupportCrudService<TestEntity, String> {

}
```

TIP

树结构实体需要实现: TreeSortSupportEntity接口,或者继承GenericTreeSortSupportEntity

## Web

hsweb和jetlinks都使用注解式来声明web映射,方式与spring-mvc类似.

### Web Crud

增删改查与Service类似,实现接口:ReactiveCrudController(基于ReactiveRepository),或者ReactiveServiceCrudController基于(ReactiveCrudService)即可.树结构实体还可以实现:ReactiveTreeServiceQueryController接口.

具体的接口内容请查看对应源代码.

## 动态查询

平台的Controller和Service均支持动态查询,查询参数说明[请看这里](http://doc.jetlinks.cn/interface-guide/query-param.html).

## 权限控制

hsweb提供来一套统一的权限控制API,方便进行细粒度的权限控制.

### 注解式

常用注解:

1. @Resource
: 用于定义资源,通常注解在类上.
2. @ResourceAction
: 定义对资源对操作,通常注解在方法上.
3. @QueryAction
: 继承自
@ResourceAction(, name = “查询”)
4. @SaveAction
: 继承自
@ResourceAction(, name = “保存”)
5. @DeleteAction
: 继承自
@ResourceAction(, name = “删除”)
6. @Authorze
: 声明权限控制,注解在类或者方法上,可通过注解属性配置控制权限方式.
7. @EnableAopAuthorize
: 注解在启动类上,开启权限控制.

TIP

@ResourceAction通常使用注解继承的方式来使用,可以更好的管理操作定义.详细使用方法可参照:@QueryAction

### 编程式

在有的场景需要编程方式获取当前用户权限信息,例如:

```plain text
@GetMapping("/user/detaul/current")
public Mono<UserDetail> getCurrentUserDetail(){
    return Authentication
            .currentReactive()
            .switchIfEmpty(Mono.error(UnAuthorizedException::new))//如果没有用户信息则抛出异常
            .map(autz->service.getUserDetail(autz.getUser().getId()))
}
```

### 权限维度

hsweb抽象来一个权限维度的概念,例如 用户,角色,公司是维度类型,那么具体的一个用户,角色或者人员就是维度信息. 在Authentication中,没有角色这些固有概念,只有维度,维度是可拓展的.不同的系统,可能维度不同,但是权限控制使用同一套API.

权限控制:

```plain text
//注解式,推荐使用注解继承方式来自定义注解.
    @RequiresRoles("admin")//继承自: @Dimension(type="role",)
    public Mono<UserDetail> getData(String id){
       //...
    }

    //编程式
    //用户是否在id为admin中role维度中.相当于判断用户是否是admin角色.
    autz.hasDimension(DefaultDimensionType.role,"admin").
```

### 自定义维度

实现接口:DimensionProvider,然后注入到spring即可.例如:

```plain text
@Component
public class CompanyDimensionProvider implements DimensionProvider {

    @Autowired
    private CompanyService service;

    @Override
    public Flux<DimensionType> getAllType() {
        //建议使用枚举来实现DimensionType
        return Flux.just(CustomDimensionType.company);
    }

    @Override
    public Flux<Dimension> getDimensionByUserId(String userId) {
        //根据userId获取维度
        return service
                .findByUserId(userId)
                .map(CompanyEntity::toDimension);
    }

    @Override
    public Mono<? extends Dimension> getDimensionById(DimensionType type, String id) {
        //根据维度id获取维度
        return service.findById(id)
                      .map(CompanyEntity::toDimension);
    }

    @Override
    public Flux<String> getUserIdByDimensionId(String dimensionId) {
        //根据维度ID获取所有用户ID
        return service.findUserBind(dimensionId)
                .map(CompanyUserBindEntity::getUserId);
    }
}
```

JetLinks%20%E4%BD%BF%E7%94%A8%5Bhsweb-easyorm%20(opens%20new%20window)%5D(https%3A%2F%2Fgithub.com%2Fhs-web%2Fhsweb-easy-orm)%E5%AE%9E%E7%8E%B0%E5%93%8D%E5%BA%94%E5%BC%8F%E7%9A%84ORM.%0A%0A%23%23%20DAO%0A%0A%60easyorm%60%E5%B0%81%E8%A3%85%E4%BA%86%60r2dbc%60%E5%AE%9E%E7%8E%B0%E4%BA%86%E5%8A%A8%E6%80%81DDL%2CDSL%E5%8A%A8%E6%80%81%E6%9D%A1%E4%BB%B6%E7%AD%89%E4%BE%BF%E6%8D%B7%E6%93%8D%E4%BD%9C.%E5%AE%9E%E7%8E%B0%E4%B8%80%E4%B8%AA%E5%A2%9E%E5%88%A0%E6%94%B9%E6%9F%A5%E5%8F%AA%E9%9C%80%E8%A6%812%E6%AD%A5.%0A%0A%E5%88%9B%E5%BB%BA%E5%AE%9E%E4%BD%93%E7%B1%BB%2C%E4%BD%BF%E7%94%A8jpa%E6%B3%A8%E8%A7%A3%E6%8F%8F%E8%BF%B0%E6%98%A0%E5%B0%84%E5%85%B3%E7%B3%BB.%0A%0A%60%60%60java%0A%0A%40Data%0A%40Table(name%3D%22s_test%22)%0Apublic%20class%20TestEntity%20extends%20GenericEntity%3CString%3E%20%7B%0A%0A%20%20%20%20%40Column%0A%20%20%20%20private%20String%20name%3B%0A%0A%20%20%20%20%40Column%0A%20%20%20%20%40EnumCodec%20%20%2F%2F%E4%BD%BF%E7%94%A8%E6%9E%9A%E4%B8%BE%E8%BF%9B%E8%A1%8C%E7%BC%96%E8%A7%A3%E7%A0%81%0A%20%20%20%20%40ColumnType(javaType%20%3D%20String.class)%2F%2F%E6%8C%87%E5%AE%9A%E6%95%B0%E6%8D%AE%E5%BA%93%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%0A%20%20%20%20%40DefaultValue(%22disabled%22)%2F%2F%E9%BB%98%E8%AE%A4%E5%80%BC%0A%20%20%20%20private%20TestEnum%20state%3B%0A%0A%20%20%20%20%40Column%0A%20%20%20%20%40JsonCodec%20%2F%2Fjson%E7%BC%96%E8%A7%A3%E7%A0%81%0A%20%20%20%20%40ColumnType(jdbcType%20%3D%20JDBCType.CLOB%2C%20javaType%20%3D%20String.class)%0A%20%20%20%20private%20Map%3CString%2CObject%3E%20configuration%3B%0A%7D%0A%0A%60%60%60%0A%0A%E5%9C%A8%E9%9C%80%E8%A6%81%E4%BD%BF%E7%94%A8crud%E7%9A%84%E5%9C%B0%E6%96%B9%E7%9B%B4%E6%8E%A5%E6%B3%A8%E5%85%A5%60ReactiveRepository%3CTestEntity%2CString%3E%60%E5%8D%B3%E5%8F%AF%2C%E5%A6%82%3A%0A%0A%60%60%60java%0A%0A%40Autowired%0AReactiveRepository%3CTestEntity%2CString%3E%20testRepository%3B%0A%0A%60%60%60%0A%0ATIP%0A%0A%E5%90%AF%E5%8A%A8%E7%B1%BB%E4%B8%8A%E9%9C%80%E8%A6%81%E6%B3%A8%E8%A7%A3%3A%20%60%40EnableEasyormRepository(%22%E5%AE%9E%E4%BD%93%E7%B1%BB%E6%89%80%E5%9C%A8%E5%8C%85%2C%E5%A6%82%3A%20org.jetlinks.community.**.entity%22)%60.%0A%0A%23%23%23%20%E8%87%AA%E5%AE%9A%E4%B9%89%E9%80%9A%E7%94%A8%E6%9F%A5%E8%AF%A2%E6%9D%A1%E4%BB%B6%0A%0A%23%23%20Service%0A%0A%23%23%23%20CRUD%20Service%0A%0Ahsweb%E6%8F%90%E4%BE%9B%E4%BA%86%60GenericReactiveCrudService%60%2C%E4%BD%BF%E7%94%A8%60ReactiveRepository%60%E5%AE%9E%E7%8E%B0%E9%80%9A%E7%94%A8%E5%A2%9E%E5%88%A0%E8%AF%A5%E6%9F%A5.%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%0Apublic%20class%20TestService%20extends%20GenericReactiveCrudService%3CTestEntity%2CString%3E%7B%0A%7D%0A%0A%60%60%60%0A%0A%23%23%23%20%E6%94%AF%E6%8C%81%E7%BC%93%E5%AD%98%E7%9A%84Service%0A%0A%60GenericReactiveCacheSupportCrudService%60%0A%0A%60%60%60java%0A%40Service%0Apublic%20class%20TestService%20extends%20GenericReactiveCacheSupportCrudService%3CTestEntity%2C%20String%3E%20%7B%0A%0A%20%20%20%20%40Override%0A%20%20%20%20public%20String%20getCacheName()%20%7B%0A%20%20%20%20%20%20%20%20return%20%22test-entity-cache%22%3B%0A%20%20%20%20%7D%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%94%AF%E6%8C%81%E6%A0%91%E7%BB%93%E6%9E%84%E5%AE%9E%E4%BD%93%E7%9A%84Service%0A%0A%60GenericReactiveTreeSupportCrudService%60%2C%E6%8F%90%E4%BE%9B%E4%BA%86%E5%AF%B9%E6%A0%91%E7%BB%93%E6%9E%84%E6%95%B0%E6%8D%AE%E5%AF%B9%E4%B8%80%E4%BA%9B%E9%80%9A%E7%94%A8%E5%A4%84%E7%90%86%2C%E5%A6%82%60List%60%E4%B8%8E%60%E6%A0%91%E7%BB%93%E6%9E%84%60%E4%BA%92%E8%BD%AC.%0A%0A%60%60%60java%0A%40Service%0Apublic%20class%20TestService%20extends%20GenericReactiveTreeSupportCrudService%3CTestEntity%2C%20String%3E%20%7B%0A%0A%7D%0A%60%60%60%0A%0ATIP%0A%0A%E6%A0%91%E7%BB%93%E6%9E%84%E5%AE%9E%E4%BD%93%E9%9C%80%E8%A6%81%E5%AE%9E%E7%8E%B0%3A%20%60TreeSortSupportEntity%60%E6%8E%A5%E5%8F%A3%2C%E6%88%96%E8%80%85%E7%BB%A7%E6%89%BF%60GenericTreeSortSupportEntity%60%0A%0A%23%23%20Web%0A%0Ahsweb%E5%92%8Cjetlinks%E9%83%BD%E4%BD%BF%E7%94%A8%60%E6%B3%A8%E8%A7%A3%E5%BC%8F%60%E6%9D%A5%E5%A3%B0%E6%98%8Eweb%E6%98%A0%E5%B0%84%2C%E6%96%B9%E5%BC%8F%E4%B8%8E%60spring-mvc%60%E7%B1%BB%E4%BC%BC.%0A%0A%23%23%23%20Web%20Crud%0A%0A%E5%A2%9E%E5%88%A0%E6%94%B9%E6%9F%A5%E4%B8%8E%60Service%60%E7%B1%BB%E4%BC%BC%2C%E5%AE%9E%E7%8E%B0%E6%8E%A5%E5%8F%A3%3A%60ReactiveCrudController%60(%E5%9F%BA%E4%BA%8E%60ReactiveRepository%60)%2C%E6%88%96%E8%80%85%60ReactiveServiceCrudController%60%E5%9F%BA%E4%BA%8E(%60ReactiveCrudService%60)%E5%8D%B3%E5%8F%AF.%E6%A0%91%E7%BB%93%E6%9E%84%E5%AE%9E%E4%BD%93%E8%BF%98%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%3A%60ReactiveTreeServiceQueryController%60%E6%8E%A5%E5%8F%A3.%0A%0A%E5%85%B7%E4%BD%93%E7%9A%84%E6%8E%A5%E5%8F%A3%E5%86%85%E5%AE%B9%E8%AF%B7%E6%9F%A5%E7%9C%8B%E5%AF%B9%E5%BA%94%E6%BA%90%E4%BB%A3%E7%A0%81.%0A%0A%23%23%20%E5%8A%A8%E6%80%81%E6%9F%A5%E8%AF%A2%0A%0A%E5%B9%B3%E5%8F%B0%E7%9A%84Controller%E5%92%8CService%E5%9D%87%E6%94%AF%E6%8C%81%E5%8A%A8%E6%80%81%E6%9F%A5%E8%AF%A2%2C%E6%9F%A5%E8%AF%A2%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E%5B%E8%AF%B7%E7%9C%8B%E8%BF%99%E9%87%8C%5D(http%3A%2F%2Fdoc.jetlinks.cn%2Finterface-guide%2Fquery-param.html).%0A%0A%23%23%20%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6%0A%0Ahsweb%E6%8F%90%E4%BE%9B%E6%9D%A5%E4%B8%80%E5%A5%97%E7%BB%9F%E4%B8%80%E7%9A%84%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6API%2C%E6%96%B9%E4%BE%BF%E8%BF%9B%E8%A1%8C%E7%BB%86%E7%B2%92%E5%BA%A6%E7%9A%84%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6.%0A%0A%23%23%23%20%E6%B3%A8%E8%A7%A3%E5%BC%8F%0A%0A%E5%B8%B8%E7%94%A8%E6%B3%A8%E8%A7%A3%3A%0A%0A1.%20%60%40Resource%60%3A%20%E7%94%A8%E4%BA%8E%E5%AE%9A%E4%B9%89%E8%B5%84%E6%BA%90%2C%E9%80%9A%E5%B8%B8%E6%B3%A8%E8%A7%A3%E5%9C%A8%E7%B1%BB%E4%B8%8A.%0A2.%20%60%40ResourceAction%60%3A%20%E5%AE%9A%E4%B9%89%E5%AF%B9%E8%B5%84%E6%BA%90%E5%AF%B9%E6%93%8D%E4%BD%9C%2C%E9%80%9A%E5%B8%B8%E6%B3%A8%E8%A7%A3%E5%9C%A8%E6%96%B9%E6%B3%95%E4%B8%8A.%0A3.%20%60%40QueryAction%60%3A%20%E7%BB%A7%E6%89%BF%E8%87%AA%60%40ResourceAction(id%20%3D%20%22query%22%2C%20name%20%3D%20%22%E6%9F%A5%E8%AF%A2%22)%60%0A4.%20%60%40SaveAction%60%3A%20%E7%BB%A7%E6%89%BF%E8%87%AA%60%40ResourceAction(id%20%3D%20%22save%22%2C%20name%20%3D%20%22%E4%BF%9D%E5%AD%98%22)%60%0A5.%20%60%40DeleteAction%60%3A%20%E7%BB%A7%E6%89%BF%E8%87%AA%60%40ResourceAction(id%20%3D%20%22delete%22%2C%20name%20%3D%20%22%E5%88%A0%E9%99%A4%22)%60%0A6.%20%60%40Authorze%60%3A%20%E5%A3%B0%E6%98%8E%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6%2C%E6%B3%A8%E8%A7%A3%E5%9C%A8%E7%B1%BB%E6%88%96%E8%80%85%E6%96%B9%E6%B3%95%E4%B8%8A%2C%E5%8F%AF%E9%80%9A%E8%BF%87%E6%B3%A8%E8%A7%A3%E5%B1%9E%E6%80%A7%E9%85%8D%E7%BD%AE%E6%8E%A7%E5%88%B6%E6%9D%83%E9%99%90%E6%96%B9%E5%BC%8F.%0A7.%20%60%40EnableAopAuthorize%60%3A%20%E6%B3%A8%E8%A7%A3%E5%9C%A8%E5%90%AF%E5%8A%A8%E7%B1%BB%E4%B8%8A%2C%E5%BC%80%E5%90%AF%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6.%0A%0ATIP%0A%0A%60%40ResourceAction%60%E9%80%9A%E5%B8%B8%E4%BD%BF%E7%94%A8%E6%B3%A8%E8%A7%A3%E7%BB%A7%E6%89%BF%E7%9A%84%E6%96%B9%E5%BC%8F%E6%9D%A5%E4%BD%BF%E7%94%A8%2C%E5%8F%AF%E4%BB%A5%E6%9B%B4%E5%A5%BD%E7%9A%84%E7%AE%A1%E7%90%86%E6%93%8D%E4%BD%9C%E5%AE%9A%E4%B9%89.%E8%AF%A6%E7%BB%86%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95%E5%8F%AF%E5%8F%82%E7%85%A7%3A%60%40QueryAction%60%0A%0A%23%23%23%20%E7%BC%96%E7%A8%8B%E5%BC%8F%0A%0A%E5%9C%A8%E6%9C%89%E7%9A%84%E5%9C%BA%E6%99%AF%E9%9C%80%E8%A6%81%E7%BC%96%E7%A8%8B%E6%96%B9%E5%BC%8F%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E6%9D%83%E9%99%90%E4%BF%A1%E6%81%AF%2C%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%40GetMapping(%22%2Fuser%2Fdetaul%2Fcurrent%22)%0Apublic%20Mono%3CUserDetail%3E%20getCurrentUserDetail()%7B%0A%20%20%20%20return%20Authentication%0A%20%20%20%20%20%20%20%20%20%20%20%20.currentReactive()%0A%20%20%20%20%20%20%20%20%20%20%20%20.switchIfEmpty(Mono.error(UnAuthorizedException%3A%3Anew))%2F%2F%E5%A6%82%E6%9E%9C%E6%B2%A1%E6%9C%89%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E5%88%99%E6%8A%9B%E5%87%BA%E5%BC%82%E5%B8%B8%0A%20%20%20%20%20%20%20%20%20%20%20%20.map(autz-%3Eservice.getUserDetail(autz.getUser().getId()))%0A%7D%0A%60%60%60%0A%0A%23%23%23%20%E6%9D%83%E9%99%90%E7%BB%B4%E5%BA%A6%0A%0Ahsweb%E6%8A%BD%E8%B1%A1%E6%9D%A5%E4%B8%80%E4%B8%AA%E6%9D%83%E9%99%90%E7%BB%B4%E5%BA%A6%E7%9A%84%E6%A6%82%E5%BF%B5%2C%E4%BE%8B%E5%A6%82%20%60%E7%94%A8%E6%88%B7%60%2C%60%E8%A7%92%E8%89%B2%60%2C%60%E5%85%AC%E5%8F%B8%60%E6%98%AF%E7%BB%B4%E5%BA%A6%E7%B1%BB%E5%9E%8B%2C%E9%82%A3%E4%B9%88%60%E5%85%B7%E4%BD%93%60%E7%9A%84%E4%B8%80%E4%B8%AA%60%E7%94%A8%E6%88%B7%60%2C%60%E8%A7%92%E8%89%B2%60%E6%88%96%E8%80%85%60%E4%BA%BA%E5%91%98%60%E5%B0%B1%E6%98%AF%E7%BB%B4%E5%BA%A6%E4%BF%A1%E6%81%AF.%20%E5%9C%A8%60Authentication%60%E4%B8%AD%2C%E6%B2%A1%E6%9C%89%E8%A7%92%E8%89%B2%E8%BF%99%E4%BA%9B%E5%9B%BA%E6%9C%89%E6%A6%82%E5%BF%B5%2C%E5%8F%AA%E6%9C%89%E7%BB%B4%E5%BA%A6%2C%E7%BB%B4%E5%BA%A6%E6%98%AF%E5%8F%AF%E6%8B%93%E5%B1%95%E7%9A%84.%E4%B8%8D%E5%90%8C%E7%9A%84%E7%B3%BB%E7%BB%9F%2C%E5%8F%AF%E8%83%BD%E7%BB%B4%E5%BA%A6%E4%B8%8D%E5%90%8C%2C%E4%BD%86%E6%98%AF%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6%E4%BD%BF%E7%94%A8%E5%90%8C%E4%B8%80%E5%A5%97API.%0A%0A%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6%3A%0A%0A%60%60%60java%0A%20%20%20%20%2F%2F%E6%B3%A8%E8%A7%A3%E5%BC%8F%2C%E6%8E%A8%E8%8D%90%E4%BD%BF%E7%94%A8%E6%B3%A8%E8%A7%A3%E7%BB%A7%E6%89%BF%E6%96%B9%E5%BC%8F%E6%9D%A5%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B3%A8%E8%A7%A3.%0A%20%20%20%20%40RequiresRoles(%22admin%22)%2F%2F%E7%BB%A7%E6%89%BF%E8%87%AA%3A%20%40Dimension(type%3D%22role%22%2Cid%3D%22admin%22)%0A%20%20%20%20public%20Mono%3CUserDetail%3E%20getData(String%20id)%7B%0A%20%20%20%20%20%20%20%2F%2F…%0A%20%20%20%20%7D%0A%0A%20%20%20%20%2F%2F%E7%BC%96%E7%A8%8B%E5%BC%8F%0A%20%20%20%20%2F%2F%E7%94%A8%E6%88%B7%E6%98%AF%E5%90%A6%E5%9C%A8id%E4%B8%BAadmin%E4%B8%ADrole%E7%BB%B4%E5%BA%A6%E4%B8%AD.%E7%9B%B8%E5%BD%93%E4%BA%8E%E5%88%A4%E6%96%AD%E7%94%A8%E6%88%B7%E6%98%AF%E5%90%A6%E6%98%AFadmin%E8%A7%92%E8%89%B2.%0A%20%20%20%20autz.hasDimension(DefaultDimensionType.role%2C%22admin%22).%0A%60%60%60%0A%0A%23%23%23%20%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6%0A%0A%E5%AE%9E%E7%8E%B0%E6%8E%A5%E5%8F%A3%3A%60DimensionProvider%60%2C%E7%84%B6%E5%90%8E%E6%B3%A8%E5%85%A5%E5%88%B0%60spring%60%E5%8D%B3%E5%8F%AF.%E4%BE%8B%E5%A6%82%3A%0A%0A%60%60%60java%0A%40Component%0Apublic%20class%20CompanyDimensionProvider%20implements%20DimensionProvider%20%7B%0A%0A%20%20%20%20%40Autowired%0A%20%20%20%20private%20CompanyService%20service%3B%0A%0A%20%20%20%20%40Override%0A%20%20%20%20public%20Flux%3CDimensionType%3E%20getAllType()%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%E5%BB%BA%E8%AE%AE%E4%BD%BF%E7%94%A8%E6%9E%9A%E4%B8%BE%E6%9D%A5%E5%AE%9E%E7%8E%B0DimensionType%0A%20%20%20%20%20%20%20%20return%20Flux.just(CustomDimensionType.company)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20%40Override%0A%20%20%20%20public%20Flux%3CDimension%3E%20getDimensionByUserId(String%20userId)%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%E6%A0%B9%E6%8D%AEuserId%E8%8E%B7%E5%8F%96%E7%BB%B4%E5%BA%A6%0A%20%20%20%20%20%20%20%20return%20service%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.findByUserId(userId)%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.map(CompanyEntity%3A%3AtoDimension)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20%40Override%0A%20%20%20%20public%20Mono%3C%3F%20extends%20Dimension%3E%20getDimensionById(DimensionType%20type%2C%20String%20id)%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%E6%A0%B9%E6%8D%AE%E7%BB%B4%E5%BA%A6id%E8%8E%B7%E5%8F%96%E7%BB%B4%E5%BA%A6%0A%20%20%20%20%20%20%20%20return%20service.findById(id)%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.map(CompanyEntity%3A%3AtoDimension)%3B%0A%20%20%20%20%7D%0A%0A%20%20%20%20%40Override%0A%20%20%20%20public%20Flux%3CString%3E%20getUserIdByDimensionId(String%20dimensionId)%20%7B%0A%20%20%20%20%20%20%20%20%2F%2F%E6%A0%B9%E6%8D%AE%E7%BB%B4%E5%BA%A6ID%E8%8E%B7%E5%8F%96%E6%89%80%E6%9C%89%E7%94%A8%E6%88%B7ID%0A%20%20%20%20%20%20%20%20return%20service.findUserBind(dimensionId)%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.map(CompanyUserBindEntity%3A%3AgetUserId)%3B%0A%20%20%20%20%7D%0A%7D%0A%60%60%60