---
layout: post
title: "Python基础_综合练习 1"
date: 2025-07-04
tags:
  - Python
  - HeyWhale
categories:
  - Python
comments: true
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---

本项目来源于和鲸社区，使用转载需要标注来源

* 作者: 和鲸社区
* 来源: 和鲸社区

:toc
<!-- more -->

# 第一题

题目：有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？

程序分析：可填在百位、十位、个位的数字都是1、2、3、4。组成所有的排列后再去 掉不满足条件的排列。

注：结果保存到L1中，每道题的结果均依次保存到L2，L3，L4......

```python
import itertools

# 可用数字
digits = [1, 2, 3, 4]

# 生成所有3位数的排列（顺序不同视为不同数字）
permutations = itertools.permutations(digits, 3)

# 转换为三位整数，并去重排序
three_digit_numbers = [int(''.join(map(str, p))) for p in permutations]

# 输出结果
print(f"总共有 {len(three_digit_numbers)} 个三位数。")
print("分别是：")
print(sorted(three_digit_numbers))
```

```python
L1 = [123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431,
      432]
```

## 第二题

题目：企业发放的奖金根据利润提成。利润(I)
低于或等于10万元时，奖金可提10%；利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；20万到40万之间时，高于20万元的部分，可提成5%；40万到60万之间时高于40万元的部分，可提成3%；60万到100万之间时，高于60万元的部分，可提成1.5%，高于100万元时，超过100万元的部分按1%提成，从输入利润为120000时，求应发放奖金总数？结果转换成int，保存到L2数组中

程序分析：请利用数轴来分界，定位。

```python
# 定义利润阈值和对应的提成比例（单位：元）
thresholds = [
    (100000, 0.10),  # ≤10万：10%
    (200000, 0.075),  # 10~20万：7.5%
    (400000, 0.05),  # 20~40万：5%
    (600000, 0.03),  # 40~60万：3%
    (1000000, 0.015),  # 60~100万：1.5%
    (float('inf'), 0.01)  # >100万：1%
]

# 输入利润（单位：元）
profit = 120000

# 初始化奖金总额
bonus = 0.0

# 当前累计的利润上限
prev_limit = 0

# 遍历每个奖金区间
for limit, rate in thresholds:
    if profit > prev_limit:
        # 计算当前区间的利润范围
        current_range = min(profit, limit) - prev_limit
        bonus += current_range * rate
        prev_limit = min(limit, profit)
    else:
        break  # 如果已经处理完所有有效区间，跳出循环

# 将奖金转为整数
L2 = [int(bonus)]

# 输出结果
print("应发放奖金总数为：", L2[0], "元")
```

```python
L2 = 11500
```

## 第三题

题目：一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？

**程序分析：**
假设该数为 x。

  1. 则：x + 100 = n2, x + 100 + 168 = m2
  2. 计算等式：m2 - n2 = (m + n)(m - n) = 168
  3. 设置： m + n = i，m - n = j，i * j =168，i 和 j 至少一个是偶数
  4. 可得： m = (i + j) / 2， n = (i - j) / 2，i 和 j 要么都是偶数，要么都是奇数。
  5. 从 3 和 4 推导可知道，i 与 j 均是大于等于 2 的偶数。
  6. 由于 i * j = 168， j>=2，则 1 < i < 168 / 2 + 1。
  7. 接下来将 i 的所有数字循环计算即可。

数学分析：转换成了一个因式分解的问题

```python
import math

# 遍历所有可能的因数对 (d1, d2)，使得 d1 * d2 = 168
results = []

for d1 in range(1, int(math.isqrt(168)) + 1):
    if 168 % d1 == 0:
        d2 = 168 // d1
        
        # 确保 d2 > d1，并且奇偶性相同（才能解出整数 b 和 a）
        if (d2 + d1) % 2 == 0 and (d2 - d1) % 2 == 0:
            b = (d2 + d1) // 2
            a = (d2 - d1) // 2
            
            x = a * a - 100
            if b * b == x + 268:  # 再次验证是否满足条件
                results.append(x)

# 输出结果
print("满足条件的整数 x 有：")
print(results)
```

```python
L3 = 21
```

## 第四题

题目：输入2021-09-30，判断这一天是这一年的第几天？

程序分析：以3月5日为例，应该先把前两个月的加起来，然后再加上5天即本年的第几天，特殊情况，闰年且输入月份大于2时需考虑多加一天：

```python
def is_leap_year(year):
    """
    判断是否为闰年
    能被4整除但不能被100整除，或者能被400整除的年份是闰年
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def day_of_year(date_str):
    """
    输入格式为 'YYYY-MM-DD' 的字符串，返回是当年的第几天
    """
    # 拆分字符串为年、月、日
    year, month, day = map(int, date_str.split('-'))

    # 各月份的天数（默认平年）
    days_in_month = [31, 28, 31, 30, 31, 30,
                     31, 31, 30, 31, 30, 31]

    # 如果是闰年，修改2月为29天
    if is_leap_year(year):
        days_in_month[1] = 29

    # 计算前 month - 1 个月的总天数，然后加上 day
    total_days = sum(days_in_month[:month - 1]) + day
    return total_days

if __name__ == "__main__":
    date_input = "2021-09-30"
    result = day_of_year(date_input)
    print(f"{date_input} 是这一年的第 {result} 天")
```


可以使用 python 自带的 datetime 库来简化代码，
```python
from datetime import datetime

def day_of_year(date_str):
    """
    输入格式为 'YYYY-MM-DD' 的字符串，返回是当年的第几天
    """
    # 将字符串解析为 datetime 对象
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # 获取 struct_time 对象，并从中提取一年中的第几天
    day_of_year = date_obj.timetuple().tm_yday
    
    return day_of_year

if __name__ == "__main__":
    date_input = "2021-09-30"
    result = day_of_year(date_input)
    print(f"{date_input} 是这一年的第 {result} 天")
```

```python
L4 = 273
```

## 第五题

题目：输入三个整数13, 4,20，请把这三个数由小到大输出。

程序分析：我们想办法把最小的数放到x上，先将x与y进行比较，如果x>y则将x与y的值进行交换，然后再用x与z进行比较，如果x>
z则将x与z的值进行交换，这样能使x最小。

排序问题，可以使用冒泡排序思想
```python
# 输入三个整数
x, y, z = 13, 4, 20
# 第一步：比较 x 和 y，如果 x > y，则交换它们
if x > y:
    x, y = y, x
# 第二步：比较 x 和 z，如果 x > z，则交换它们
if x > z:
    x, z = z, x
# 第三步：比较 y 和 z，如果 y > z，则交换它们
if y > z:
    y, z = z, y
# 输出结果
print("从小到大排序的结果为：", x, y, z)
```

使用列表 + sort 函数（推荐用于多数字排序）
```python
nums = [13, 4, 20]
nums.sort()
print("从小到大排序的结果为：", nums)
```

使用 sorted() 函数（不改变原列表）
```python
nums = [13, 4, 20]
sorted_nums = sorted(nums)
print("从小到大排序的结果为：", sorted_nums)
```

```python
L5 = [4, 13, 20]
```

## 第六题

题目：斐波那契数列。

程序分析：斐波那契数列（Fibonacci sequence），又称黄金分割数列，指的是这样一个数列：0、1、1、2、3、5、8、13、21、34、……。输出第10个斐波那契数列

在数学上，费波那契数列是以递归的方法来定义：

```text
F0 = 0(n=0)
F1 = 1(n=1)
Fn = F[n - 1] + F[n - 2](n= > 2)    
```

使用递归法
```python
def fib_recursive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)

print("第10个斐波那契数是：", fib_recursive(10))
```

使用循环
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print("第10个斐波那契数是：", fibonacci(10))
```

使用动态规划的思想
```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    elif n == 1:
        return 1
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print("第10个斐波那契数是：", fib_memo(10))
```

```python
L6 = 55
```

## 第七题

题目：古典问题：有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月后每个月又生一对兔子，假如兔子都不死，问每个月的兔子有多少对？

要求输出从第1个月到第10个月分别有多少对兔子。

程序分析：兔子的规律为数列1,1,2,3,5,8,13,21....

```python
def rabbit_pairs(n):
    a, b = 1, 1  # 第1个月、第2个月都是1对兔子
    print(f"第1个月：{a} 对")
    print(f"第2个月：{b} 对")
    
    for month in range(3, n + 1):
        a, b = b, a + b
        print(f"第{month}个月：{b} 对")

# 示例：输出前10个月的兔子数量
rabbit_pairs(10)
```

```python
L7 = 55
```

## 第八题

题目：将一个正整数分解质因数。要求输入90，打印出90=2*3*3*5，将分解出的质因数保存到L8数组中。

程序分析：对n进行分解质因数，应先找到一个最小的质数k，然后按下述步骤完成：

1. 如果这个质数恰等于n，则说明分解质因数的过程已经结束，打印出即可。
2. 如果n<>k，但n能被k整除，则应打印出k的值，并用n除以k的商,作为新的正整数你n,重复执行第一步。
3. 如果n不能被k整除，则用k+1作为k的值,重复执行第一步。

```python
def prime_factors(n):
    i = 2
    factors = []
    
    while i * i <= n:
        while n % i == 0:
            # 找到一个质因子
            factors.append(i)
            n //= i
        i += 1
    
    if n > 1:
        factors.append(n)
    
    return factors

# 输入数字
num = 90

# 分解质因数
L8 = prime_factors(num)

# 输出格式：90 = 2*3*3*5
print(f"{num} = {'*'.join(map(str, L8))}")

# 打印数组内容（可选）
print("分解出的质因数保存在 L8 数组中：", L8)
```

```python
L8 =  [2, 3, 3, 5]
```

## 第九题

题目：输入'123runoobc kdf235*(dfl)'，分别统计出其中英文字母、空格、数字和其它字符的个数。按照顺序将个数保存到L9;

程序分析：利用 while 或 for 语句,条件为输入的字符不为 '\n'。

```python
def count_characters(s):
    letters = 0
    spaces = 0
    digits = 0
    others = 0

    for char in s:
        if char.isalpha():
            letters += 1
        elif char.isdigit():
            digits += 1
        elif char == ' ':
            spaces += 1
        else:
            others += 1

    return [letters, spaces, digits, others]

# 示例调用
L9 = count_characters('123runoobc kdf235*(dfl)')
print("L9 =", L9)
```

```python
L9 = [13, 1, 5, 4]
```

## 第十题

题目：一个数如果恰好等于它的因子之和，这个数就称为"完数"。例如6=1＋2＋3.编程找出1000以内的所有完数。将结果保存到L10中；

**思路：**
* 遍历从 2 到 1000 的每一个整数 n；
* 对每个 n，找出它的所有 真因子（能整除它且小于它本身的正整数）；
* 求这些因子的和 sum_factors；
* 如果 n == sum_factors，则 n 是一个完数；

```python
def is_perfect_number(n):
    """判断一个数是否为完数"""
    if n < 2:
        return False

    sum_factors = 0
    for i in range(1, n):
        if n % i == 0:
            sum_factors += i

    return sum_factors == n

# 存储结果
L10 = []

# 遍历 1~1000 的所有整数
for num in range(1, 1001):
    if is_perfect_number(num):
        L10.append(num)

# 输出结果（可选）
print("1000 以内的完数有：", L10)
```

```python
L10 = [6, 28, 496]
```



## 第十一题

题目：一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在第10次落地时，共经过多少米？结果保存到L11中；

```python
# 初始高度
height = 100
total_distance = height  # 第一次落地已经走了100米
bounce = height / 2      # 第一次弹起的高度

# 存储结果的列表
L11 = []

# 循环计算第2次到第10次落地的过程
for _ in range(2, 11):  # 第2次到第10次，共9次循环
    total_distance += bounce * 2  # 上升 + 下降
    bounce /= 2                   # 每次弹起高度减半

# 将结果保存到 L11 中
L11.append(round(total_distance, 2))

# 输出结果（可选）
print("第10次落地时，总共经过了 %.2f 米" % total_distance)
print("L11 =", L11)
```

```python
L11 = [299.609375]
```

## 第十二题

题目：猴子吃桃问题：猴子第一天摘下若干个桃子，当即吃了一半，还不瘾，又多吃了一个第二天早上又将剩下的桃子吃掉一半，又多吃了一个。以后每天早上都吃了前一天剩下的一半零一个。到第10天早上想再吃时，见只剩下一个桃子了。求第一天共摘了多少。

程序分析：采取逆向思维的方法，从后往前推断。

我们可以从第10天开始倒着推回去：
第10天早上有 1 个桃子 ,假设前一天（第9天）剩下的桃子数为 x，
则：
$$第9天吃完后剩下 = x - (x // 2 + 1) = 下一天的桃子数$$

反过来就是：
$$ x = (下一天的桃子数 + 1) * 2$$
我们就可以从第10天倒推到第1天。

```python
# 初始化第10天早上的桃子数量
peaches = 1

# 从第9天倒推到第1天
for day in range(9, 0, -1):
    peaches = (peaches + 1) * 2

# 输出结果
print("第一天共摘了", peaches, "个桃子")

# 如果需要保存结果到变量 L12
L12 = [peaches]
print("L12 =", L12)
```

```python
L12 = [1534]
```

## 第十三题

题目：两个乒乓球队进行比赛，各出三人。甲队为a,b,c三人，乙队为x,y,z三人。已抽签决定比赛名单。有人向队员打听比赛的名单。a说他不和x比，c说他不和x,z比，请编程序找出与a对战的是谁？结果保存到L13中；

思考如何用程序的方法来表达这个情况

```python
L13 = z
```

# 第十四题

题目：给出23459，逆序打印出各位数字。并保存到L14中；

程序分析：学会分解出每一位数。

```python
num = 23459
L14 = []

# 使用循环逐位提取数字
n = num
while n > 0:
    digit = n % 10     # 取出最后一位
    L14.append(digit)  # 添加到列表中
    n = n // 10        # 去掉最后一位

# 输出结果
print("原数：", num)
print("逆序各位数字：", L14)
```

```python
num = 23459
L14 = [int(ch) for ch in str(num)][::-1]

print("原数：", num)
print("逆序各位数字：", L14)
```

```python
L14 = [9, 5, 4, 3, 2]
```

## 第十五题

题目：将数组[9,6,5,4,1]逆序输出，结果保存到L15中。

程序分析：用第一个与最后一个交换。

我们可以使用 双指针法 或者 循环交换法 来实现数组逆序：

* 定义两个指针：一个指向开头（i = 0），另一个指向末尾（j = len(arr) - 1）
* 交换这两个位置的元素
* i 向右移动，j 向左移动
* 直到 i >= j 为止

```python
# 原始数组
arr = [9, 6, 5, 4, 1]

# 创建一个副本用于操作，避免修改原数组（可选）
L15 = arr.copy()

# 双指针逆序法
i = 0
j = len(L15) - 1

while i < j:
    # 交换第 i 和 第 j 个元素
    L15[i], L15[j] = L15[j], L15[i]
    i += 1
    j -= 1

# 输出结果
print("原始数组：", arr)
print("逆序后数组：", L15)
```

你也可以使用切片方式直接逆序：
```python
L15 = arr[::-1]
```

或者使用 .reverse() 方法：
```python
L15 = arr.copy()
L15.reverse()
```

```python
L15 = [1, 4, 5, 6, 9]
```


