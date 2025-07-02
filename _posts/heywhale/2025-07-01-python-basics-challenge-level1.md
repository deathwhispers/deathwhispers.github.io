---
layout: post 
title: "Python基础_基础用法"
date: 2025-07-01 
tags: [Python,heywhale,Python 基础]
comments: true 
author: deathwhispers
mathjax: true
---

本项目来源于和鲸社区，使用转载需要标注来源
* 作者: 和鲸社区
* 来源: 和鲸社区

<!-- more -->

# 1. Python基础_基础用法 

## 练习
### 练习1：华氏温度转换为摄氏温度。

> 提示：华氏温度到摄氏温度的转换公式为
> 
> $$ C=(F - 32) \div 1.8 $$

```python
F = int(input("请输入一个华氏温度："))
C = (F - 32) / 1.8
print("华氏温度:%d, 摄氏温度:%d" % (F, C))
```

### 练习2：输入圆的半径计算计算周长和面积
```python
import math
R = float(input("请输入一个圆的半径："))
L = 2 * math.pi * R
S = math.pi * R**2
print("圆的半径:%.1f, 周长:%.2f, 面积:%.2f" % (R,L,S))
```

### 练习3：输入年份判断是不是闰年。
> suggestion：比较运算符会产生布尔值，而逻辑运算符and和or会对这些布尔值进行组合，最终也是得到一个布尔值，闰年输出True，平年输出False。

```python
year = int(input("请输入一个年份:"))
if((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
    print("{}年是闰年!".format(year))
else:
    print("{}年不是闰年!".format(year))
```

### 练习4：英制单位英寸与公制单位厘米互换。
> 英制单位英寸与公制单位厘米互换:
> 
> 1 厘米 = 0.39英寸；
> 
> 1 英寸 = 2.54厘米；

```python
length = float(input("请输入长度:"))
unit = input("请输入单位(英寸/厘米、in/cm)):")
if unit == 'in' or unit == '英寸':
    length_limi = length * 2.54 # 1 英寸 = 2.54厘米
    print('%.2f英寸 = %.2f厘米' % (length, length_limi))
elif unit == 'cm' or unit == '厘米':
    length_yingcun = length * 0.39
    print('%.2f厘米 = %.2f英寸' % (length, length_yingcun))
else:
    print('对不起，您输入有误，请重新输入！')
```

### 练习5：百分制成绩转换为等级制成绩。
> 要求：如果输入的成绩在90分以上（含90分）输出A；80分-90分（不含90分）输出B；70分-80分（不含80分）输出C；60分-70分（不含70分）输出D；60分以下输出E。

```python
score = int(input("请输入您的成绩"))
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'E'
print('根据您提供的成绩分数，最终评分等级为:%s' % grade)
```

### 练习6：输入三条边长，如果能构成三角形就计算周长和面积。
* 三角形边长就等于其三边之和：a + b + c；
* 已知三边，求三角形面积，根据海伦公式：

$$ p = (a+b+c)/2 $$
$$ area = \sqrt { p * (p - a) * (p - b) * (p-c) } $$

```python
a = float(input("请输入三角形第一条边长"))
b = float(input("请输入三角形第二条边长"))
c = float(input("请输入三角形第三条边长"))
if(a + b > c and a + c > b and b + c > a):
    perimeter = a + b + c
    p = (a + b + c) / 2
    area = (p*(p-a)*(p-b)*(p-c))**0.5
    print("根据您输入的三条边长，构成的三角形周长为: %.2f, 面积为: %.2f ;" % (perimeter, area))
else:
    print("您输入的三条边长不符合三角形性质，请重新输入！")
```

## 作业

### Q1：给定a=8, b=3，根据如下公式计算x1，并**保留两位小数**

$$ x = \sqrt { (a + b) * (a - b) / (a^2 + b^2) } $$

```
x1 = 0.8680003787638843
```

```python
a=8
b=3
x1=((a+b)*(a-b)/(a**2 + b**2)) **0.5
x1=round(x1,2)
print(x1)
```


### Q2：将x1代入下列分段函数，计算结果赋值给x2
$$
f(x) = \begin{cases} 
3x-5   & (x > 1)\\
x + 2  & (-1 \leq x  \leq 1) \\
5x + 3 & (x \leq -1) \\
\end{cases}
$$

>Tips: markdown 中可以使用两对 "$$" 来包裹公式代码块
> 
> 其中，分段函数需要使用 \begin{cases} 和 \end{cases} 成对来描述，
> 每一行用 "\\" 进行分隔，公式和条件之间可以通过 “&” 符号进行对齐。
>

```
x2 = 2.868000378763884
```

```python
a=8
b=3
x1=((a+b)*(a-b)/(a**2 + b**2)) **0.5
x1=round(x1,2)
print(x1)

x = x1
if x > 1:
	x2 = 3 * x - 5
elif x >= -1:
	x2 = x +2
else:
	x2 = 5 * x + 3
print(x2)
```

### Q3：计算x1*100所对应的成绩等级，赋值给y

90分以上（含90分）输出A；80分-90分（不含90分）输出B；70分-80分（不含80分）输出C；60分-70分（不含70分）输出D；60分以下输出E。

```
y = B
```

```python
a=8
b=3
x1=((a+b)*(a-b)/(a**2 + b**2)) **0.5
x1=round(x1,2)
print(x1)

x = x1
if x > 1:
	x2 = 3 * x - 5
elif x >= -1:
	x2 = x +2
else:
	x2 = 5 * x + 3
print(x2)

grade = x1 * 100
if grade >= 90:
	y = "A"
elif grade >= 80:
	y = "B"
elif grade >= 70:
	y = "C"
elif grade >= 60:
	y = "D"
else:
	y = "E"
print(y)
```

