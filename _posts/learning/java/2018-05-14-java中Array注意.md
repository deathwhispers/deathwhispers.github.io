---
layout: post
title: java中Array注意
author: deathwhispers
date: 2018-05-14
slug: java-array-note
categories:
- Java
tags:
- Java
type: note
status: draft
created: 2018-05-14 22:31
updated: 2018-05-14 22:31
week: 2025-W48
---

# java中Array注意

在使用toArray()方法时,需要注意转型的问题

```java
public static void main(String[] args) {
    List<String> list = new ArrayList<String>();
    list.add("1");
    list.add("2");
    String[] tt = (String[]) list.toArray(new String[0]);
}


```

这段代码是没问题的，但我们看到String[] tt =(String[]) list.toArray(new String[0]) 中的参数很奇怪，然而去掉这个参数new String[0]却在运行时报错.

我们发现toArray()有两个方法,无参的toArray方法会先构造一个Object数组,然后进行数据copy,最后返回的是Object类型的数组,所以就会出现转型错误了

```java
public Object[] toArray() {
    Object[] result = new Object[size];
    System.arraycopy(elementData, 0, result, 0, size);
    return result;
}


```

而带有参数的toArray()方法,则是根据参数数组的类型,构造一个对应类型的,长度与ArrayList一样的一个空数组,之后进行数据copy,虽然方法本身返回的还是Object类型,不过构造数组

```java
public Object[] toArray(Object a[]) {
    if (a.length < size)
    a = (Object[]) java.lang.reflect.Array.newInstance(a.getass().getComponentType(), size);
    System.arraycopy(elementData, 0, a, 0, size);
    if (a.length > size)
    a[size] = null;
    return a;
}
```

因此在使用toArray的时候可以参考以下三种方式

```java
1. Long[] l = new Long[<total size>];
list.toArray(l);
2. Long[] l = (Long[]) list.toArray(new Long[0]);
3. Long[] a = new Long[<total size>];
Long[] l = (Long[]) list.toArray(a);
```
