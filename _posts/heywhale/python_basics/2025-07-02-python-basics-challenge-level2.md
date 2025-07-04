---
layout: post
title: "Python基础_循环函数"
date: 2025-07-02
tags: [Python,heywhale,Python 基础]
categories: [Python 基础学习]
comments: true
author: deathwhispers
---

本项目来源于和鲸社区，使用转载需要标注来源
* 作者: 和鲸社区
* 来源: 和鲸社区

<!-- more -->

* toc
{:toc}

# 2.Python基础_循环函数

**🔖循环分支和函数**

  * 循环结构的应用场景 - 条件 / 缩进 / 代码块 / 流程图
  * while循环 - 基本结构 / break语句 / continue语句
  * for循环 - 基本结构 / range类型 / 循环中的分支结构 / 嵌套的循环 / 提前结束程序
  * 定义函数 - def语句 / 函数名 / 参数列表 / return语句 / 调用自定义函数：
  * 函数的参数 - 默认参数 / 可变参数 / 关键字参数 / 命名关键字参数
  * 函数的返回值 - 没有返回值 / 返回单个值 / 返回多个值
  * 作用域问题 - 局部作用域 / 嵌套作用域 / 全局作用域 / 内置作用域 / 和作用域相关的关键字

## 1. for循环
如果明确的知道循环执行的次数或者要对一个容器进行迭代（后面会讲到），那么我们推荐使用for-in循环，例如下面代码中计算1~100求和的结果。

### 1.1 for语句

for循环可以遍历任何可迭代对象，如一个列表或者一个字符串。

for循环的一般格式如下：

```python
for <variable> in <sequence>:    
    <statements>    
else:    
    <statements>    
```

for 循环实例：
```python
languages = ["C", "C++", "Perl", "Python"] 
for x in languages:
    print (x)
```

### 1.2 break

以下 for 实例中使用了 break 语句，break 语句用于跳出当前循环体：

```python
sites = ["Baidu", "Google","jindong","Taobao"]
for site in sites:
    if site == "jindong":
        print("购物!")
        break
    print("循环数据 " + site)
else:
    print("没有循环数据!")
print("完成循环!")
```

上面的代码中使用了break关键字来提前终止循环，需要注意的是break只能终止它所在的那个循环，
这一点在使用嵌套的循环结构（下面会讲到）需要引起注意。

除了break之外，还有另一个关键字是continue，
它可以用来放弃本次循环后续的代码直接让循环进入下一轮。

和分支结构一样，循环结构也是可以嵌套的，也就是说在循环中还可以构造循环结构。

下面的例子演示了如何通过嵌套的循环来输出一个九九乘法表。

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print('%d*%d=%d' % (i, j, i * j), end='\t')
    print()
```

> range(1,10) 会生成一个数列，左闭右开，从 1 到 9 (不包含 10)

### 1.3 range()函数

如果你需要遍历数字序列，可以使用内置range()函数。它会生成数列，例如:

```python
for i in range(5):
    print(i)
```
```text
0
1
2
3
4
```

利用range（）函数计算1~100和：
```python
sum = 0
for x in range(101):
    sum += x
print(sum)
```
或者
```python
sum = 0
for x in range(1,101):
    sum += x
print(sum)
```

需要说明的是上面代码中的range(1, 101)可以用来构造一个从1到100的范围，
当我们把这样一个范围放到for-in循环中，就可以通过前面的循环变量x依次取出从1到100的整数。
当然，range的用法非常灵活，下面给出了一个例子：

* range(101)：可以用来产生0到100范围的整数，需要注意的是取不到101。
* range(1, 101)：可以用来产生1到100范围的整数，相当于左闭右开
* range(1, 101, 2)：可以用来产生1到100的奇数，其中2是步长，即每次数值递增的值。
* range(100, 0, -2)：可以用来产生100到1的偶数，其中-2是步长，即每次数字递减的值。

知道了这一点，我们可以用下面的代码来实现1~100之间的偶数求和。

```python
sum = 0
for x in range(2, 101, 2):  
    sum += x
print(sum)
```

同样地，我们也可以求奇数和
```python
sum = 0
for x in range(1, 100, 2):  
    print(x)
    sum += x
print(sum)
```

当然，也可以通过在循环中使用分支结构的方式来实现相同的功能，代码如下所示。

```python
sum = 0
for x in range(1, 101):
    if x % 2 == 0:
        sum += x
print(sum)
```

> tips：相较于上面直接跳过奇数的做法，下面这种做法很明显并不是很好的选择。

可以结合range()和len()函数以遍历一个序列的索引,如下所示:

```python
a = ['Google', 'Baidu', 'ModelWhale', 'Taobao', 'QQ']
for i in range(len(a)):
    print(i, a[i])
```

## 2. while循环

如果要构造不知道具体循环次数的循环结构，我们推荐使用while循环。while循环通过一个能够产生或转换出布尔值的表达式来控制循环，表达式的值为True则继续循环；表达式的值为False则结束循环。

### 2.1 while语句
```python
while 判断条件(condition)：    
    执行语句(statements)
    ...
```

使用 while 来计算 1 到 100 的总和
```python
n = 100
sum = 0
counter = 1
while counter <= n:
    sum = sum + counter
    counter += 1
    
print("1 到 %d 之和为: %d" % (n,sum))
```

## 2.2 无限循环
我们可以通过设置条件表达式永远不为 false 来实现无限循环，实例如下：
```python
var = 1
while var == 1 :  # 表达式永远为 true
   num = int(input("输入一个数字  :"))
   print ("你输入的数字是: ", num)

print ("Good bye!")
```

> 无限循环在服务器上客户端的实时请求非常有用。

## 2.3 while 循环使用 else 语句
如果 while 后面的条件语句为 false 时，则执行 else 的语句块。

语法格式如下：
```python
while <expr>:    
    <statement(s)>    
else:
    <additional_statement(s)>
```

写一个猜数字的游戏，游戏的规则如下：

计算机出一个1到100之间的随机数，玩家输入自己猜的数字，计算机给出对应的提示信息（大一点、小一点或猜对了），
如果玩家猜中了数字，计算机提示用户一共猜了多少次，游戏结束，否则游戏继续。

```python
import random

# 随机取1~100之间的一个整数
answer = random.randint(1, 100)
counter = 0
while True:
    counter += 1
    number = int(input('请输入: '))
    if number < answer:
        print('大一点')
    elif number > answer:
        print('小一点')
    else:
        print('恭喜你猜对了!')
        break #猜对即停止while循环
print('你总共猜了%d次' % counter)
if counter > 7:
    print('你真棒')
```

### 2.4 简单语句组
类似if语句的语法，如果你的while循环体中只有一条语句，你可以将该语句与while写在同一行中， 如下所示：



## 3. 函数

函数是组织好的，可重复使用的，用来实现单一，或相关联功能的代码段。

函数能提高应用的模块性，和代码的重复利用率。

你已经知道Python提供了许多内建函数，比如print()。 但你也可以自己创建函数，这被叫做用户自定义函数。

### 3.1 定义一个函数

你可以定义一个由自己想要功能的函数，以下是简单的规则：

* 函数代码块以 def 关键词开头，后接函数标识符名称和圆括号 ()。
* 任何传入参数和自变量必须放在圆括号中间，圆括号之间可以用于定义参数。
* 函数的第一行语句可以选择性地使用文档字符串—用于存放函数说明。
* 函数内容以冒号:起始，并且缩进。
* return [表达式] 结束函数，选择性地返回一个值给调用方，不带表达式的 return 相当于返回 None。

### 3.2 语法
定义函数使用 def 关键字，一般格式如下：

```python
def 函数名（参数列表）:    
    函数体    
```
默认情况下，参数值和参数名称是按函数声明中定义的顺序匹配起来的。

#### 实例1 让我们使用函数来输出"Hello World！"

```python
def hello() :
    print("Hello World!")

hello()
```

更复杂点的应用，函数中带上参数变量:

#### 实例2 比较两个数，并返回较大的数
```python

def max(a, b):
    if a > b:
        return a
    else:
        return b

a = 4
b = 5
print(max(a, b))
```

#### 实例3 计算面积函数
```python
def area(width, height):
    return width * height

w = 4
h = 5
print("width =", w, " height =", h, " area =", area(w, h))
```

### 3.3 函数调用
定义一个函数：给了函数一个名称，指定了函数里包含的参数，和代码块结构。

这个函数的基本结构完成以后，你可以通过另一个函数调用执行，也可以直接从 Python 命令提示符执行。

如下实例调用了 printme() 函数：
```python
# 定义函数
def printme( str ):
    # 打印任何传入的字符串
    print (str)
    return

# 调用函数
printme("我要调用用户自定义函数!")
printme("再次调用同一函数")
```

### 3.4 参数
以下是调用函数时可使用的正式参数类型：

* 必需参数
* 关键字参数
* 默认参数
* 不定长参数

#### 必需参数

必需参数须以正确的顺序传入函数。调用时的数量必须和声明时的一样。

调用 printme() 函数，你必须传入一个参数，不然会出现语法错误：

```python
#可写函数说明
def printme( str ):
    "打印任何传入的字符串"
    print (str)
    return

# 调用 printme 函数，不加参数会报错
printme()
```

#### 关键字参数

关键字参数和函数调用关系紧密，函数调用使用关键字参数来确定传入的参数值。

使用关键字参数允许函数调用时参数的顺序与声明时不一致，因为 Python 解释器能够用参数名匹配参数值。

以下实例在函数 printme() 调用时使用参数名：

```python
#可写函数说明
def printme( str ):
    "打印任何传入的字符串"
    print (str)
    return

#调用printme函数
printme( str = "我爱编程")
```

以下实例中演示了函数参数的使用不需要使用指定顺序：

```python
#可写函数说明
def printinfo( name, age ):
    "打印任何传入的字符串"
    print ("名字: ", name)
    print ("年龄: ", age)
    return

#调用printinfo函数
printinfo( age=50, name="张三" )
```

#### 默认参数

调用函数时，如果没有传递参数，则会使用默认参数。以下实例中如果没有传入 age 参数，则使用默认值：

```python
#可写函数说明
def printinfo( name, age = 35 ):
    "打印任何传入的字符串"
    print ("名字: ", name)
    print ("年龄: ", age)
    return

#调用printinfo函数
printinfo( age=50, name="张三" )
print ("------------------------")
printinfo( name="张三" )
```

#### 不定长参数

你可能需要一个函数能处理比当初声明时更多的参数。这些参数叫做不定长参数，和上述 2 种参数不同，声明时不会命名。基本语法如下

```python
def functionname([formal_args,] *var_args_tuple ):    
    "函数_文档字符串"    
    function_suite    
    return [expression]    
```

加了星号 *的参数会以元组(tuple)的形式导入，存放所有未命名的变量参数。

```python
# 可写函数说明
def printinfo( arg1, *vartuple ):
    "打印任何传入的参数"
    print ("输出: ")
    print (arg1)
    print (vartuple)

# 调用printinfo 函数
printinfo( 70, 60, 50 )
```

### 3.5 return语句

return [表达式] 语句用于退出函数，选择性地向调用方返回一个表达式。不带参数值的return语句返回None。

之前的例子都没有示范如何返回数值，以下实例演示了 return 语句的用法：

```python
# 可写函数说明
def sum( arg1, arg2 ):
    # 返回2个参数的和."
    total = arg1 + arg2
    print ("函数内 : ", total)
    return total

# 调用sum函数
total = sum( 10, 20 )
print ("函数外 : ", total)
```

## 4. 变量的作用域

最后，我们来讨论一下Python中有关变量作用域的问题。

```python
def foo():
    b = 'hello'
    # Python中可以在函数内部再定义函数
    def bar():
        c = True
        print(a)
        print(b)
        print(c)

    bar()
    # print(c)  # NameError: name 'c' is not defined


if __name__ == '__main__':
    a = 100
    # print(b)  # NameError: name 'b' is not defined
    foo()
```

上面的代码能够顺利的执行并且打印出100、hello和True，但我们注意到了，在bar函数的内部并没有定义a和b两个变量，那么a和b是从哪里来的。

我们在上面代码的if分支中定义了一个变量a，这是一个全局变量（global variable），属于全局作用域，因为它没有定义在任何一个函数中。在上面的foo函数中我们定义了变量b，这是一个定义在函数中的局部变量（local variable），属于局部作用域，在foo函数的外部并不能访问到它；但对于foo函数内部的bar函数来说，变量b属于嵌套作用域，在bar函数中我们是可以访问到它的。bar函数中的变量c属于局部作用域，在bar函数之外是无法访问的。
事实上，Python查找一个变量时会按照“局部作用域”、“嵌套作用域”、“全局作用域”和“内置作用域”的顺序进行搜索，前三者我们在上面的代码中已经看到了，所谓的“内置作用域”就是Python内置的那些标识符，我们之前用过的input、print、int等都属于内置作用域。

再看看下面这段代码，我们希望通过函数调用修改全局变量a的值，但实际上下面的代码是做不到的。

```python
def foo():
    a = 200
    print(a)  # 200

if __name__ == '__main__':
    a = 100
    foo()
    print(a)  # 100
```

在调用 foo 函数后，我们发现 a 的值仍然是 100 ，这是因为当我们在函数 foo 中写 a = 200 的时候，是重新定义了一个名字为 a 的局部变量，它跟全局作用域的 a 并不是同一个变量，
因为局部作用域中有了自己的变量 a ，因此 foo 函数不再搜索全局作用域中的 a 。

如果我们希望在foo函数中修改全局作用域中的a，代码如下所示。

```python

def foo():
    global a
    a = 200
    print(a)  # 200

if __name__ == '__main__':
    a = 100
    foo()
    print(a)  # 200
```
我们可以使用 global 关键字来指示 foo 函数中的变量 a 来自于全局作用域，如果全局作用域中没有 a，那么下面一行的代码就会定义变量 a 并将其置于全局作用域。

同理，如果我们希望函数内部的函数能够修改嵌套作用域中的变量，可以使用 nonlocal 关键字来指示变量来自于嵌套作用域，请大家自行试验。


## ✍作业
### 1. 找出10000以内的完美数，保存到列表L1中。

说明：完美数又称为完全数或完备数，它的所有的真因子（即除了自身以外的因子）的和（即因子函数）恰好等于它本身。

例如：$6（6=1+2+3）$ 和 $28（28=1+2+4+7+14）$ 就是完美数。完美数有很多神奇的特性，有兴趣的可以自行了解。

暴力枚举
```python
def sum_of_proper_divisors(n):
    """返回n的所有真因数之和"""
    if n < 2:
        return 0
    divisors_sum = 1  # 1 是所有大于1的数的真因数
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            divisors_sum += i
            if i != n // i and n // i != n:
                divisors_sum += n // i
    return divisors_sum

L1 = []
for num in range(2, 10001):
    if sum_of_proper_divisors(num) == num:
        L1.append(num)

print("10000以内的完美数：", L1)
```

**数学公式**
偶完美数的形式为:
$$ 2 ^ {p-1} (2 ^ p - 1) $$

其中 $ 2 ^ p - 1 $ 是一个梅森素数（Mersenne Prime）。我们枚举一些小的 p 值来生成完美数，并检查是否小于等于 10000

```python
def is_mersenne_prime(p):
    """检查 2^p - 1 是否是素数（即是否产生完美数）"""
    mersenne = (1 << p) - 1  # 计算 2^p - 1
    if mersenne < 2:
        return False
    for i in range(2, int(mersenne ** 0.5) + 1):
        if mersenne % i == 0:
            return False
    return True

L1 = []
p_values = [2, 3, 5, 7, 11, 13]  # 小于 2^13 的结果已超过 10000

for p in p_values:
    if is_mersenne_prime(p):
        perfect_number = (1 << (p - 1)) * ((1 << p) - 1)
        if perfect_number <= 10000:
            L1.append(perfect_number)

print("10000以内的完美数：", L1)
```

```python
L1 = [6, 28, 496, 8128]
```



### 2. 寻找1000内的水仙花数，并保存到列表L2中；

> tips：水仙花数也被称为超完全数字不变数、自恋数、自幂数、阿姆斯特朗数，它是一个3位数，该数字每个位上数字的立方之和正好等于它本身，
> 例如：$$1^3 + 5^3 + 3^3=153$$

```python
def is_narcissistic(num):
    digits = list(map(int, str(num)))
    n = len(digits)
    return sum(digit ** n for digit in digits) == num

L2 = [num for num in range(1, 1000) if is_narcissistic(num)]

print("1000以内的水仙花数：", L2)
``` 

```python
L2 = [153, 370, 371, 407]
```


### 3. 写一个程序查询300到500内的回文素数，并保存到列表L3中；

回文素数（Palindromic Prime） 是指既是回文数，又是素数的数。

* 回文数（Palindrome）：正着读和反着读一样的数字。例如：121、131。
* 素数（Prime）：只能被 1 和它本身整除的大于 1 的自然数。例如：2, 3, 5, 7, 11 等。

```python
def is_palindrome(n):
    return str(n) == str(n)[::-1]

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

L3 = [num for num in range(300, 501) if is_palindrome(num) and is_prime(num)]

print("300到500之间的回文素数：", L3)
```

```python
L3 = [313, 353, 373, 383]
```
