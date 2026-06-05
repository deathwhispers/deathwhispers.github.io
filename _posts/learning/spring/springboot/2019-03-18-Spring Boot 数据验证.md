---
layout: post
title: Spring Boot 数据验证
author: deathwhispers
date: 2019-03-18
slug: spring-boot-data-validation
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2019-03-18 09:57
updated: 2019-03-18 09:57
week: 2019-W14
---

## JSR-303 注释介绍

这里只列举了 javax.validation 包下的注解，同理在 spring-boot-starter-web 包中也存在 hibernate-validator 验证包，里面包含了一些 javax.validation 没有的注解，有兴趣的可以看看

| **注解** | **说明** |
| --- | --- |
| @NotNull | **限制必须不为null** |
| @NotEmpty | **验证注解的元素值不为 null 且不为空（字符串长度不为0、集合大小不为0）** |
| @NotBlank | **验证注解的元素值不为空（不为null、去除首位空格后长度为0），不同于@NotEmpty，@NotBlank只应用于字符串且在比较时会去除字符串的空格** |
| @Pattern(value) | **限制必须符合指定的正则表达式** |
| @Size(max,min) | **限制字符长度必须在 min 到 max 之间（也可以用在集合上）** |
| @Email | **验证注解的元素值是Email，也可以通过正则表达式和flag指定自定义的email格式** |
| @Max(value) | **限制必须为一个不大于指定值的数字** |
| @Min(value) | **限制必须为一个不小于指定值的数字** |
| @DecimalMax(value) | **限制必须为一个不大于指定值的数字** |
| @DecimalMin(value) | **限制必须为一个不小于指定值的数字** |
| @Null | **限制只能为null（很少用）** |
| @AssertFalse | **限制必须为false （很少用）** |
| @AssertTrue | **限制必须为true （很少用）** |
| @Past | **限制必须是一个过去的日期** |
| @Future | **限制必须是一个将来的日期** |
| @Digits(integer,fraction) | **限制必须为一个小数，且整数部分的位数不能超过 integer，小数部分的位数不能超过 fraction （很少用）** |

# 自定义 Validator 注解

## 为何要自定义

javax.validation 包与 hibernate-validator 包中存在的注解几乎可以满足大部分的要求，又拥有基于正则表达式的@Pattern，为什么还需要自己去定义呢？

原因如下

- 正则效率不高
- 正则可读性不好
- 正则门槛较高，很多开发者并不会编写正则表达式

## 自定义注解

这里定义了一个 @DateTime 注解，在该注解上标注了 @Constraint 注解，它的作用就是指定一个具体的校验器类

关键字段（强制性）

- **message：** 验证失败提示的消息内容
- **groups：** 为约束指定验证组（非常不错的一个功能，下一章介绍）
- **payload：** 不太清楚（欢迎留言交流）

```java
package com.battcn.annotation;

import com.battcn.validator.DateTimeValidator;
import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.FIELD;
import static java.lang.annotation.ElementType.PARAMETER;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

/**
 * @author Levin
 * @since 2018/6/6 0006
 */
@Target({FIELD, PARAMETER})
@Retention(RUNTIME)
@Constraint(validatedBy = DateTimeValidator.class)
public @interface DateTime {
    String message() default "格式错误";
    String format() default "yyyy-MM-dd";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

## 具体验证

定义校验器类 DateTimeValidator 实现 ConstraintValidator 接口，实现接口后需要实现它里面的 initialize： 与 isValid： 方法。

方法介绍

- **initialize：** 主要用于初始化，它可以获得当前注解的所有属性
- **isValid：** 进行约束验证的主体方法，其中 value 就是验证参数的具体实例，context 代表约束执行的上下文环境。

这里的验证方式虽然简单，但职责明确；**为空验证可以使用 @NotBlank、@NotNull、@NotEmpty 等注解来进行控制，而不是在一个注解中做各种各样的规则判断，应该职责分离**

```java
package com.battcn.validator;

import com.battcn.annotation.DateTime;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.text.ParseException;
import java.text.SimpleDateFormat;

/**
 * 日期格式验证
 *
 * @author Levin
 * @version 1.0.0
 * @since 2018-06-06
 */
public class DateTimeValidator implements ConstraintValidator<DateTime, String> {
    private DateTime dateTime;

    @Override
    public void initialize(DateTime dateTime) {
        this.dateTime = dateTime;
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        // 如果 value 为空则不进行格式验证，为空验证可以使用 @NotBlank @NotNull @NotEmpty 等注解来进行控制，职责分离
        if (value == null) {
            return true;
        }
        String format = dateTime.format();
        if (value.length() != format.length()) {
            return false;
        }
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat(format);
        try {
            simpleDateFormat.parse(value);
        } catch (ParseException e) {
            return false;
        }
        return true;
    }
}
```

## 控制层

```java
package com.battcn.controller;

import com.battcn.annotation.DateTime;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 参数校验
 *
 * @author Levin
 * @since 2018/6/04 0031
 */
@Validated
@RestController
public class ValidateController {
    @GetMapping("/test")
    public String test(@DateTime(message = "您输入的格式错误，正确的格式为：{format}", format = "yyyy-MM-dd HH:mm") String date) {
        return "success";
    }
}
```

# 分组验证

有的时候，我们对一个实体类需要有多中验证方式，在不同的情况下使用不同验证方式，比如说对于一个实体类来的 id 来说，新增的时候是不需要的，对于更新时是必须的，这个时候你是选择写一个实体类呢还是写两个呢？

在[自定有数据有效性校验注解](http://www.iocoder.cn/Spring-Boot/battcn/v2-other-validate2/)中介绍到注解需要有一个 groups 属性，这个属性的作用又是什么呢？

接下来就让我们看看如何用一个验证类实现多个接口之间不同规则的验证…

## 分组验证器

定义一个验证组，里面写上不同的空接口类即可

```java
package com.battcn.groups;

/**
 * 验证组
 *
 * @author Levin
 * @since 2018/6/7 0007
 */
public class Groups {
    public interface Update {}
    public interface Default {}
}
```

## 实体类

**groups 属性的作用就让 @Validated 注解只验证与自身 value 属性相匹配的字段，可多个，只要满足就会去纳入验证范围；**我们都知道针对新增的数据我们并不需要验证 ID 是否存在，我们只在做修改操作的时候需要用到，因此这里将 ID 字段归纳到 Groups.Update.class 中去，而其它字段是不论新增还是修改都需要用到所以归纳到 Groups.Default.class 中…

```java
package com.battcn.pojo;

import com.battcn.groups.Groups;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.math.BigDecimal;

/**
 * @author Levin
 * @since 2018/6/7 0005
 */
public class Book {
    @NotNull(message = "id 不能为空", groups = Groups.Update.class)
    private Integer id;
    @NotBlank(message = "name 不允许为空", groups = Groups.Default.class)
    private String name;
    @NotNull(message = "price 不允许为空", groups = Groups.Default.class)
    private BigDecimal price;
    // 省略 GET SET …
}
```

## 控制层

创建一个 ValidateController 类，然后定义好 insert、update 俩个方法，比由于 insert 方法并不关心 ID 字段，所以这里 @Validated 的 value 属性写成 Groups.Default.class 就可以了；而 update 方法需要去验证 ID 是否为空，所以此处 @Validated 注解的 value 属性值就要写成 Groups.Default.class, Groups.Update.class；代表只要是这分组下的都需要进行数据有效性校验操作…

```java
package com.battcn.controller;

import com.battcn.groups.Groups;
import com.battcn.pojo.Book;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 参数校验
 *
 * @author Levin
 * @since 2018/6/06 0031
 */
@RestController
public class ValidateController {
    @GetMapping("/insert")
    public String insert(@Validated(value = Groups.Default.class) Book book) {
        return "insert";
    }

    @GetMapping("/update")
    public String update(@Validated(value = {Groups.Default.class, Groups.Update.class}) Book book) {
        return "update";
    }
}
```
