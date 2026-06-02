---
layout: post
title: Spring 中 @Valid 注解的使用
author: deathwhispers
date: 2021-12-07
slug: valid-annotation-usage
categories:
- Java
tags:
- Java
type: note
status: draft
created: 2021-12-07 12:00
updated: 2021-12-07 12:00
week: 2025-W48
---

# @Valid 注解的使用

@Valid是java自带的参数校验注解，在**javax.validation包下**

![javax.validation包结构](/assets/images/learning/java/valid注解的使用/0b35db080830181482d6d4022ba09302.png)

**javax.validation.constraints中校验参数的注解**

| 注解 | 说明 |
| --- | --- |
| 空检查 |   |
| @NotNull | 验证对象是否不为null，无法检查空字符串 |
| @NotEmpty | 检查约束元素是否为null或者EMPTY，不会trim空格 |
| @NotBlank | 验证对象是否为空，只对字符串校验，且会trim调前后空格 |
| @Null | 验证对象是否为null，只允许null值 |
|   |   |
| Boolean检查 |   |
| @AssertTrue | 验证Boolean对象是否为true |
| @AssertFalse | 验证Boolean对象是否为false |
|   |   |
| 长度检查 |   |
| @Size(min=,max=) | 验证对象长度是否在指定范围内（主要针对集合对象：Array、Collection、Map和String） |
| @Length(min=,max= ) | 判断String长度是否在指定范围内 |
|   |   |
| 数值检查 | 建议使用String，Integer类型，而不是int类型 |
| @Min | 验证Number、String对象是否大于等于指定的值 |
| @Max | 验证Number、String对象是否小于等于指定的值 |
| @DecimalMin | 被标注的值必须不小于约束中指定的最小值. 这个约束的参数是一个通过BigDecimal定义的最小值的字符串表示.小数存在精度 |
| @DecimalMax | 被标注的值必须不大于约束中指定的最大值. 这个约束的参数是一个通过BigDecimal定义的最大值的字符串表示.小数存在精度 |
| @Digits | 验证 Number 和 String 的构成是否合法 |
| @Digits(integer=,fraction=) | 验证字符串是否是符合指定格式的数字，interger指定整数精度，fraction指定小数精度。 |
| @Positive | 验证是否为正数 |
| @PositiveOrZero | 验证是否为正数或0 |
| @Negative | 验证是否为负数 |
| @NegativeOrZero | 验证是否为负数或0 |
|   |   |
| 日期检查 | 支持的时间对象java.util.Datejava.util.Calendarjava.time.Instantjava.time.LocalDatejava.time.LocalDateTimejava.time.LocalTimejava.time.MonthDayjava.time.OffsetDateTimejava.time.OffsetTimejava.time.Yearjava.time.YearMonthjava.time.ZonedDateTimejava.time.chrono.HijrahDatejava.time.chrono.JapaneseDatejava.time.chrono.MinguoDatejava.time.chrono.ThaiBuddhistDate |
| @Past | 验证是否为过去的一个日期 |
| @PastOrPresent | 验证是否为过去或现在的一个日期 |
| @Future | 验证是否为将来的一个日期 |
| @FutureOrPresent | 验证是否为将来或现在的一个日期 |
| @Pattern | 验证 String 对象是否符合正则表达式的规则 |
|   |   |
| @Email | 验证是否是邮件地址，如果为null,不进行验证，算通过验证。 |
