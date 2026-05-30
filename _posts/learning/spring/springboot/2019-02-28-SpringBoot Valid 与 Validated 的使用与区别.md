---
layout: post
title: SpringBoot @Valid 与 @Validated 的使用与区别
author: deathwhispers
date: 2019-02-28
slug: valid-validated-difference
categories:
- Spring
tags:
- Spring
- SpringBoot
type: note
status: draft
created: 2019-02-28 09:57
updated: 2019-02-28 09:57
week: 2019-W09
---

### @Valid：

@Valid注解用于校验，所属包为：javax.validation.Valid。

首先需要在实体类的相应字段上添加用于充当校验条件的注解，如：@Min,如下代码（age属于Girl类中的属性）：

```java
@Min(value = 18,message = "未成年禁止入内")
private Integer age;
```

其次在controller层的方法的要校验的参数上添加@Valid注解，并且需要传入BindingResult对象，用于获取校验失败情况下的反馈信息，如下代码：

```java
@PostMapping("/girls")
public Girl addGirl(@Valid Girl girl, BindingResult bindingResult) {
    if(bindingResult.hasErrors()){
        System.out.println(bindingResult.getFieldError().getDefaultMessage());
        return null;
    }
    return girlResposity.save(girl);
}
```

注: 通常不在这里处理异常, 由统一的exceptioin全局异常处理

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ResponseBody
    @ExceptionHandler(value = MethodArgumentNotValidException.class)
    public JsonResult violationException(MethodArgumentNotValidException exception) {
        // 不带任何参数访问接口,会抛出 BindException
        // 因此，我们只需捕获这个异常，并返回我们设置的 message 即可
        String message = exception.getBindingResult().getAllErrors().get(0).getDefaultMessage();
        return JsonResult.fail(message);
    }
}
```

### @Validated：

@Valid是javax.validation里的。

@Validated是@Valid 的一次封装，是Spring提供的校验机制使用。

### 两者的区别

1. @Valid
：标准JSR-303规范的标记型注解，用来标记验证属性和方法返回值，进行级联和递归校验
2. @Validated
：
Spring
的注解，是标准
JSR-303
的一个变种（补充），提供了一个分组功能，可以在入参验证时，根据不同的分组采用不同的验证机制
3. 在
Controller
中校验方法参数时，使用@Valid和@Validated并无特殊差异（若不需要分组校验的话）
4. @Validated**级联校验**
注解可以用于类级别，用于支持Spring进行方法级别的参数校验。
@Valid
可以用在属性级别约束，用来表示
。
5. @Validated
只能用在类、方法和参数上，而
@Valid
可用于方法、字段、构造器和参数上

最后提示一点：Spring Boot的Web Starter已经加入了Bean Validation以及实现的依赖，可以直接使用。但若是纯Spring MVC环境，请自行导入~

在检验Controller的入参是否符合规范时，使用@Validated或者@Valid在基本验证功能上没有太多区别。但是在**分组**、**注解地方**、**嵌套验证**等功能上两个有所不同：

### 分组

@Valid 作为标准JSR-303规范，还没有吸收分组的功能。

@Validated Spring’s JSR-303规范，是标准JSR-303的一个变种, 提供了一个分组功能，可以在入参验证时，根据不同的分组采用不同的验证机制。

### 注解地方

@Valid：可以用在方法、构造函数、方法参数和成员属性（字段）上

@Validated：可以用在类型、方法和方法参数上。但是不能用在成员属性（字段）上

两者是否能用于成员属性（字段）上直接影响能否提供嵌套验证的功能。

## JSR303定义的校验类型

```plain text
// 空检查
@Null           // 验证对象是否为null
@NotNull        // 验证对象是否不为null, 无法查检长度为0的字符串
@NotBlank       // 检查约束字符串是不是Null还有被Trim的长度是否大于0,只对字符串,且会去掉前后空格.
@NotEmpty       // 检查约束元素是否为NULL或者是EMPTY.

// Booelan检查
@AssertTrue     // 验证 Boolean 对象是否为 true
@AssertFalse    // 验证 Boolean 对象是否为 false

// 长度检查
@Size(min=, max=)       // 验证对象（Array,Collection,Map,String）长度是否在给定的范围之内
@Length(min=, max=)     // 验证注解的元素值长度在min和max区间内

// 日期检查
@Past       // 验证 Date 和 Calendar 对象是否在当前时间之前
@Future     // 验证 Date 和 Calendar 对象是否在当前时间之后
@Pattern    // 验证 String 对象是否符合正则表达式的规则

// 数值检查，建议使用在Stirng,Integer类型，不建议使用在int类型上，因为表单值为“”时无法转换为int，但可以转换为Stirng为"",Integer为null
@Min            // 验证 Number 和 String 对象是否大等于指定的值
@Max            // 验证 Number 和 String 对象是否小等于指定的值
@DecimalMax     // 被标注的值必须不大于约束中指定的最大值. 这个约束的参数是一个通过BigDecimal定义的最大值的字符串表示.小数存在精度
@DecimalMin     // 被标注的值必须不小于约束中指定的最小值. 这个约束的参数是一个通过BigDecimal定义的最小值的字符串表示.小数存在精度
@Digits         // 验证 Number 和 String 的构成是否合法
@Digits(integer=,fraction=)     // 验证字符串是否是符合指定格式的数字，interger指定整数精度，fraction指定小数精度。

@Range(min=, max=)  // 验证注解的元素值在最小值和最大值之间
@Range(min=10000,max=50000,message="range.bean.wage")
private BigDecimal wage;

@Valid // 递归的对关联对象进行校验, 如果关联对象是个集合或者数组,那么对其中的元素进行递归校验,如果是一个map,则对其中的值部分进行校验.(是否进行递归验证)
@CreditCardNumber// 信用卡验证
@Email  // 验证是否是邮件地址，如果为null,不进行验证，算通过验证。
@ScriptAssert(lang= ,script=, alias=)
@URL(protocol=,host=, port=,regexp=, flags=)
```
