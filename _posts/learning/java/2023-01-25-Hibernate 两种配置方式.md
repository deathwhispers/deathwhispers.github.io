---
layout: post
title: Hibernate 两种配置方式
slug: hibernate-two-configuration-methods
type:
- note
date: 2023-01-25
week: 2025-W48
status: draft
tags:
- Java
author: deathwhispers
created: 2023-01-25 10:47
updated: 2023-01-25 10:47
categories:
- Learning
- Java
---

## Hibernate 两种配置方式

hibernate有两种配置方式，分别是[*.hbm.xml 配置方式](https://how2j.cn/k/hibernate/hibernate-tutorial/31.html#step66) 和[注解方式](https://how2j.cn/k/hibernate/hibernate-annotation/1052.html#step4010)。 虽然方式不一样，但是都是用于解决如下问题：1. 当前类是否实体类2. 对应的表名称3. 主键对应哪个属性， 自增长策略是什么，对应字段名称是什么4. 非主键属性对应字段名称是什么

接下来，我会做一套仿hibernate的注解，并且在一个实体类Hero上运用这些注解，并通过反射解析这些注解信息，来解决上述的问题

## 自定义 Hibernate 注解

参考hibernate的 [注解配置方式](https://how2j.cn/k/hibernate/hibernate-annotation/1052.html#step4010) ，自定义5个注解，分别对应hibernate中用到的注解：

- hibernate_annotation.MyEntity 对应 javax.persistence.Entity
- hibernate_annotation.MyTable 对应 javax.persistence.Table
- hibernate_annotation.MyId 对应 javax.persistence.Id
- hibernate_annotation.MyGeneratedValue 对应 javax.persistence.GeneratedValue
- hibernate_annotation.MyColumn 对应 javax.persistence.Column

[MyEntity.java](https://how2j.cn/k/annotation/annotation-like-hibernate/1058.html#nowhere)

```java
package hibernate_annotation;import java.lang.annotation.ElementType;import java.lang.annotation.Retention;import java.lang.annotation.RetentionPolicy;import java.lang.annotation.Target;@Target(ElementType.TYPE)@Retention(RetentionPolicy.RUNTIME)public @interface MyEntity {}
```

[MyTable.java](https://how2j.cn/k/annotation/annotation-like-hibernate/1058.html#nowhere)

```java
package hibernate_annotation;import java.lang.annotation.ElementType;import java.lang.annotation.Retention;import java.lang.annotation.RetentionPolicy;import java.lang.annotation.Target;@Target(ElementType.TYPE)@Retention(RetentionPolicy.RUNTIME)public @interface MyTable {    String name();}
```

[MyId.java](https://how2j.cn/k/annotation/annotation-like-hibernate/1058.html#nowhere)

```java
package hibernate_annotation;import java.lang.annotation.ElementType;import java.lang.annotation.Retention;import java.lang.annotation.RetentionPolicy;import java.lang.annotation.Target;@Target(ElementType.METHOD)@Retention(RetentionPolicy.RUNTIME)public @interface MyId {}
```

[MyGeneratedValue.java](https://how2j.cn/k/annotation/annotation-like-hibernate/1058.html#nowhere)

```plain text
package hibernate_annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface MyGeneratedValue {
    String strategy();
}
```

[MyColumn.java](https://how2j.cn/k/annotation/annotation-like-hibernate/1058.html#nowhere)

```java
package hibernate_annotation;import java.lang.annotation.ElementType;import java.lang.annotation.Retention;import java.lang.annotation.RetentionPolicy;import java.lang.annotation.Target;@Target(ElementType.METHOD)@Retention(RetentionPolicy.RUNTIME)public @interface MyColumn {    String value();}
```

## 运用在Hero对象上

像[以注解方式配置Product类](https://how2j.cn/k/hibernate/hibernate-annotation/1052.html#step4010) 那样，在Hero类上运用这些自定义注解：当注解的方法是value的时候，给这个注解赋值时，本来应该是：@MyColumn(value=“name_”)

现在可以简略一点，写为@MyColumn(“name_”)

只有当名称是value的时候可以这样，其他名称如name,stratgy等不行

## 解析注解

创建一个解析类ParseHibernateAnnotation ，获取Hero类上配置的注解信息，其运行结果如图所示。思路如下：

1. 首先获取Hero.class类对象
2. 判断本类是否进行了MyEntity 注解
3. 获取注解 MyTable
4. 遍历所有的方法，如果某个方法有MyId注解，那么就记录为主键方法primaryKeyMethod
5. 把主键方法的自增长策略注解MyGeneratedValue和对应的字段注解MyColumn 取出来，并打印
6. 遍历所有非主键方法，并且有MyColumn注解的方法，打印属性名称和字段名称的对应关系。

```java
package test;import java.lang.reflect.Method;import hibernate_annotation.MyColumn;import hibernate_annotation.MyEntity;import hibernate_annotation.MyGeneratedValue;import hibernate_annotation.MyId;import hibernate_annotation.MyTable;import pojo.Hero;public class ParseHibernateAnnotation {    public static void main(String[] args) {        Class<Hero> clazz = Hero.class;        MyEntity myEntity = (MyEntity) clazz.getAnnotation(MyEntity.class);        if (null == myEntity) {            System.out.println("Hero类不是实体类");        } else {            System.out.println("Hero类是实体类");            MyTable myTable= (MyTable) clazz.getAnnotation(MyTable.class);            String tableName = myTable.name();            System.out.println("其对应的表名是:" + tableName);            Method[] methods =clazz.getMethods();            Method primaryKeyMethod = null;            for (Method m: methods) {                MyId myId = m.getAnnotation(MyId.class);                if(null!=myId){                    primaryKeyMethod = m;                    break;                }            }            if(null!=primaryKeyMethod){                System.out.println("找到主键：" + method2attribute( primaryKeyMethod.getName() ));                MyGeneratedValue myGeneratedValue =                primaryKeyMethod.getAnnotation(MyGeneratedValue.class);                System.out.println("其自增长策略是：" +myGeneratedValue.strategy());                MyColumn myColumn = primaryKeyMethod.getAnnotation(MyColumn.class);                System.out.println("对应数据库中的字段是：" +myColumn.value());            }            System.out.println("其他非主键属性分别对应的数据库字段如下：");            for (Method m: methods) {                if(m==primaryKeyMethod){                    continue;                }                MyColumn myColumn = m.getAnnotation(MyColumn.class);                //那些setter方法上是没有MyColumn注解的                if(null==myColumn)                    continue;                System.out.format("属性： %s\t对应的数据库字段是:%s%n",method2attribute(m.getName()),myColumn.value());            }        }    }    private static String method2attribute(String methodName) {        String result = methodName; ;        result = result.replaceFirst("get", "");        result = result.replaceFirst("is", "");        if(result.length()<=1){            return result.toLowerCase();        }        else{            return result.substring(0,1).toLowerCase() + result.substring(1,result.length());        }    }}
```

## 可运行项目

因为本知识点涉及到的自定义类型比较多，为了保证大家顺利看到运行结果，把本项目打包后在右上角下载
