---
layout: post
title: "Python基础_综合练习 2"
date: 2025-07-05
tags:
  - Python
  - heywhale
  - Python 基础
categories:
  - Python 基础学习
comments: true
author: deathwhispers
---

本项目来源于和鲸社区，使用转载需要标注来源

* 作者: 和鲸社区
* 来源: 和鲸社区

<!-- more -->

# Python 综合练习 2

## 第一题

题目：有40个人围成一圈，顺序排号。从第一个人开始报数（只报123这三个数），凡报到数字为3的人退出圈子，问最后留下的是原来第几号的那位。

**约瑟夫环问题**

### 方法一：模拟法（推荐，适合理解）

* 使用一个列表保存所有人的编号 [1, 2, ..., 40]
* 使用一个计数器 count，每轮加1
* 当 count % 3 == 0 时，移除当前人
* 循环直到只剩一人

```python
def last_remaining(n=40):
    people = list(range(1, n + 1))  # 创建人员编号列表
    index = 0                       # 当前报数的人的索引
    count = 0                       # 报数计数器

    while len(people) > 1:
        count += 1
        if count % 3 == 0:
            people.pop(index)       # 报到3的人出局
        else:
            index += 1              # 不是3，跳到下一个人

        # 索引循环处理（因为是一个圈）
        index %= len(people)

    return people[0]

# 调用函数
result = last_remaining()

# 输出结果
print("最后留下的人是原来的第", result, "号")
```

```text
L1 = [28]
```

# 第二题

题目：编写一个程序，提取以逗号分割的字符串中的所有数字，并将数字重新组合成一个数组；要求输入'34岁,67年,55岁,33岁,12日,98年'这一个字符串，提取出['34'， '67'， '55'， '33'， '12'， '98']，注意数字用字符串来表示，结果保存到L2中；

```python
import re

# 输入字符串
s = '34岁,67年,55岁,33岁,12日,98年'

# 按逗号分割字符串
parts = s.split(',')

# 提取每个部分中的数字
L2 = []
for part in parts:
    # 使用正则提取该片段中的连续数字
    numbers = re.findall(r'\d+', part)
    if numbers:
        # 添加到结果列表中
        L2.extend(numbers)

# 输出结果（可选）
print("提取出的数字列表为：", L2)
```

```text
L2 = ['34', '67', '55', '33', '12', '98']
```


# 第三题

题目：编写一个程序，根据给定的公式计算并打印值:$Q=\sqrt{[(2*C*D)/H]}$。其中，假定C=50。H=30。D是一个变量，它的值应该以逗号分隔的序列输入到程序中。

要求输入：'100,150,180'这一字符串，依次按逗号分隔出每个数字，并带入公式中计算，计算结果保存到L3数组中【注意：计算出的数字用字符串表示】；

```python
import math

# 给定常量
C = 50
H = 30

# 输入字符串
input_str = '100,150,180'

# 分割字符串得到 D 的列表
D_list = input_str.split(',')

# 初始化结果列表 L3
L3 = []

# 遍历每个 D 值，代入公式计算，并将结果转为字符串
for d_str in D_list:
    D = float(d_str)
    Q = math.sqrt((2 * C * D) / H)
    # 四舍五入保留整数或转换为整数（如果小数部分为0）
    Q_rounded = round(Q)
    # 转换为字符串后添加进 L3
    L3.append(str(Q_rounded))

# 输出结果（可选）
print("计算结果保存在 L3 中：", L3)
```

```text
L3 = ['18', '22', '24']
```

# 第四题

题目：编写一个程序，X,Y作为输入数值，根据两个数值会生成一个二维数组，数组的第i行和第j列的元素值等于i×j。注意：i和j都是从0开始计；
要求输入'3, 5'这一字符串，则程序输出为：[[0,0,0,0,0],[0,1,2,3,4],[0,2,4,6,8]]；将二维数组转化为一维数组，保存到L4数组中；

```python
# 输入字符串
input_str = '3,5'

# 解析输入，得到 X（行数）和 Y（列数）
X, Y = map(int, input_str.split(','))

# 初始化二维数组
matrix = []

# 构建二维数组
for i in range(X):
    row = []
    for j in range(Y):
        row.append(i * j)
    matrix.append(row)

# 将二维数组转换为一维数组，并保存到 L4
L4 = [element for row in matrix for element in row]
```

```text
L4 = [0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 0, 2, 4, 6, 8]
```

> PS: 一行写法，代码更加简洁，但晦涩难懂

```python
X, Y = map(int, '3,5'.split(','))
L4 = [i * j for i in range(X) for j in range(Y)]
print(L4)
```


# 第五题

题目：编写一个程序，以逗号分隔的单词序列作为输入，按照字母顺序对每个单词进行排序，并通过逗号分隔的序列来打印单词。要求输入'without,hello,bag,world'这一字符串，则输出为：['bag', 'hello', 'without', 'world']；将结果保存到数组L5中；

**字符串处理 + 排序问题**

```python
# 输入字符串
input_str = 'without,hello,bag,world'

# 分割字符串为单词列表
words = input_str.split(',')

# 对单词进行排序（按字母顺序）
sorted_words = sorted(words)

# 保存结果到 L5
L5 = sorted_words

print("排序后的结果：", L5)
```

```text
L5 = ['bag', 'hello', 'without', 'world']
```

# 第六题

题目：编写一个程序，接收一行序列作为输入，并在将句子中的所有字符大写后打印出来。

要求输入'Practice makes perfect'，并将每个单词大写后的结果保存到数组L6中；

**字符串处理 + 格式转换**

```python
# 输入字符串
input_str = 'Practice makes perfect'

# 分割字符串为单词列表，并将每个单词转为大写
L6 = [word.upper() for word in input_str.split()]

# 输出结果（可选）
print("转换后的结果：", L6)
```

```python
input_str = 'Practice makes perfect'
words = input_str.split()
L6 = []

for word in words:
    L6.append(word.upper())

print(L6)
```

```text
L6 = ['PRACTICE', 'MAKES', 'PERFECT']
```


# 第七题

题目：编写一个程序，以一系列空格分隔的单词作为输入，并在删除所有重复的单词后，按字母顺序排序后打印这些单词。
要求输入'hello world and practice makes perfect and hello world again'这一字符串，将最终结果保存到L7数组中；

```python
# 输入字符串
input_str = "hello world and practice makes perfect and hello world again"

# 分割字符串为单词列表，并去重（使用 set）
unique_words = set(input_str.split())

# 按字母顺序排序，并保存到 L7
L7 = sorted(unique_words)

# 输出结果（可选）
print("去重并排序后的结果：", L7)
```

```text
L7 = ['again', 'and', 'hello', 'makes', 'perfect', 'practice', 'world']
```

> 扩展：一行写法
```python
L7 = sorted(set("hello world and practice makes perfect and hello world again".split()))
print(L7)
```


# 第八题

题目：编写一个程序，接收一系列以逗号分隔的4位二进制数作为输入，然后检查它们是否可被5整除， 可被5整除的数字将以逗号分隔的顺序打印。
要求输入'0100,0011,1010,1000'这一字符串，将输出结果保存到L8数组中；

```python
# 输入字符串
input_str = '0100,0011,1010,1000'

# 分割字符串为列表
binary_numbers = input_str.split(',')

# 初始化结果列表 L8
L8 = []

# 遍历每个二进制数
for binary in binary_numbers:
    # 将二进制字符串转换为十进制整数
    decimal = int(binary, 2)
    
    # 判断是否能被5整除
    if decimal % 5 == 0:
        L8.append(binary)

# 输出结果（可选）
print("能被5整除的二进制数：", L8)
```

```text
L8 = ['1010']
```

# 第九题

题目：编写一个程序，找到1000到3000之间并且所有位数均为偶数的所有数字，比如2000，2002等，将最终结果保存到L9中；

```python
# 初始化结果列表
L9 = []

# 遍历 1000 到 3000 的所有数字
for num in range(1000, 3001):
    # 将数字转为字符串，检查每一位是否都是偶数
    if all(int(digit) % 2 == 0 for digit in str(num)):
        L9.append(num)

# 输出结果（可选）
print("符合条件的数字有：", L9)
```

```python
L9 = [num for num in range(1000, 3001) if all(int(d) % 2 == 0 for d in str(num))]
```

# 第十题

题目：编写一个输入英文句并计算该句子中共有多少字母和数字的程序。
要求输入'Hello world! 123'，将该字符串中字母和数字的个数保存到L10中；【注意：这题答案是用数字来表示】

```python
# 输入字符串
s = 'Hello world! 123'

# 初始化计数器
letters = 0
digits = 0

# 遍历每个字符
for char in s:
    if char.isalpha():
        letters += 1
    elif char.isdigit():
        digits += 1

# 将结果保存到 L10
L10 = [letters, digits]

print("L10 =", L10)
```

```python
s = 'Hello world! 123'
L10 = [sum(1 for c in s if c.isalpha()), sum(1 for c in s if c.isdigit())]
print(L10)
```

```text
L10 = [10, 3]
```

# 第十一题

题目：编写一个输入英文句子并计算该句子中大写字母和小写字母数量的程序。
要求输入'Hello world!'，将大写字母和小写字母的个数存到数组L11中；


```python
# 输入字符串
s = 'Hello world!'

# 初始化计数器
upper_count = 0
lower_count = 0

# 遍历每个字符
for char in s:
    if char.isupper():
        upper_count += 1
    elif char.islower():
        lower_count += 1

# 保存结果到 L11
L11 = [upper_count, lower_count]

print("L11 =", L11)
```

```python
s = 'Hello world!'
L11 = [sum(1 for c in s if c.isupper()), sum(1 for c in s if c.islower())]
```

```text
L11 = [1, 9]
```

# 第十二题

题目：网站要求用户输入用户名和密码进行注册。编写程序以检查用户输入的密码有效性。
以下是检查密码的标准：
1. [a-z]之间至少有1个字母
   2. [0-9]之间至少有1个数字
   3. [A-Z]之间至少有一个字母
   4. [$＃@]中至少有1个字符 
   5. 最短交易密码长度：6 
   6. 交易密码的最大长度：12

您的程序接收一系列逗号分隔的密码，并将根据上述标准进行检查，将打印符合条件的密码，每个密码用逗号分隔。

要求输入'ABd1234@1,a F1#,2w3E*,2We3345'，将输出结果保存到L12中；

**密码验证与筛选**

```python
import re

# 输入字符串
passwords = 'ABd1234@1,a F1#,2w3E*,2We3345'

# 分割成密码列表
password_list = passwords.split(',')

# 初始化结果列表
L12 = []

# 定义正则表达式模式
pattern = re.compile(r"""
    ^                      # 开始匹配
    (?=.*[a-z])            # 至少一个小写字母
    (?=.*\d)               # 至少一个数字
    (?=.*[A-Z])            # 至少一个大写字母
    (?=.*[$#@])            # 至少一个特殊字符 $ # @
    [A-Za-z0-9$#@]{6,12}   # 只能是这些字符，长度在6~12之间
    $                      # 结束匹配
""", re.VERBOSE)

# 遍历每个密码，检查是否符合规则
for pwd in password_list:
    if pattern.fullmatch(pwd):
        L12.append(pwd)

# 输出结果（可选）
print("符合条件的密码：", L12)
```

```text
L12 = ['ABd1234@1']
```

# 第十三题

数组1：[49, 38, 65, 97, 76, 13, 27, 49, 55, 4] ，排序方法：冒泡排序

将排序后的结果保存到L13中；

```python
# 原始数组
arr = [49, 38, 65, 97, 76, 13, 27, 49, 55, 4]

# 冒泡排序实现
n = len(arr)
for i in range(n):
    # 提前退出优化：如果某一轮没有发生交换，说明已经有序
    swapped = False
    for j in range(0, n - i - 1):
        if arr[j] > arr[j+1]:
            # 交换位置
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            swapped = True
    if not swapped:
        break

# 将排序结果保存到 L13
L13 = arr

# 输出结果（可选）
print("排序后的数组：", L13)
```

```text
L13 = [4, 13, 27, 38, 49, 49, 55, 65, 76, 97]
```


# 第十四题

题目：机器人从原点（0,0）开始在平面中移动，机器人可以通过给定的步骤向上，向下，向左和向右移动。

机器人运动的痕迹如下所示：

UP 5；DOWN 3；LEFT 3；RIGHT 2；方向之后的数字是步骤。

请编写一个程序，计算一系列运动和原点之后距当前位置的距离。如果距离是浮点数，则只打印最接近的整数。

要求输入'UP 5；DOWN 3；LEFT 3；RIGHT 2'这一字符串，将最终结果保存到L14中；

**坐标模拟 + 距离计算**

```python
import math

# 输入字符串
input_str = 'UP 5；DOWN 3；LEFT 3；RIGHT 2'

# 初始化坐标
x, y = 0, 0

# 分割每个指令
instructions = input_str.split('；')

# 处理每个指令
for inst in instructions:
    if not inst.strip():
        continue
    direction, step = inst.strip().split()
    step = int(step)
    
    if direction == 'UP':
        y += step
    elif direction == 'DOWN':
        y -= step
    elif direction == 'LEFT':
        x -= step
    elif direction == 'RIGHT':
        x += step

# 计算欧几里得距离
distance = round(math.hypot(x, y))

# 保存结果到 L14
L14 = [distance]

# 输出结果（可选）
print("机器人最后的位置：", (x, y))
print("距原点的距离：", distance)
print("L14 =", L14)
```

```text
L14 = [2]
```

# 第十五题

题目：假定我们数农场里的鸡和兔子中有35个头和94条腿。问我们有多少只鸡和多少只兔子？将最终结果保存到数组L15中；

**鸡兔同笼问题**


### 方法一：数学求解
```python
# 头和腿的总数
heads = 35
legs = 94

# 解方程
# 设鸡为 x，兔子为 y
# x + y = heads
# 2x + 4y = legs

# 解得：
x = (4 * heads - legs) // 2  # 鸡的数量
y = heads - x                # 兔子数量

# 保存结果到 L15
L15 = [x, y]

# 输出结果（可选）
print("鸡的数量：", x)
print("兔子数量：", y)
print("L15 =", L15)
```

### 方法二：暴力枚举

 * 鸡的数量从 0 到 heads
 * 兔子数量 = heads - x
 * 检查：2x + 4y == legs ?

```python
heads = 35
legs = 94

for x in range(heads + 1):
    y = heads - x
    if 2 * x + 4 * y == legs:
        L15 = [x, y]
        print("找到解：鸡 =", x, "只，兔子 =", y, "只")
        break
```

### 方法三：假设法
 * 假设全部是鸡 → 那么总腿数应该是：35 × 2 = 70 条腿
 * 实际有 94 条腿，比鸡多出 94 - 70 = 24 条腿
 * 每把一只鸡换成兔子，腿数增加 2
 * 所以换了 24 ÷ 2 = 12 次 → 有 12 只兔子，其余是鸡

```python
heads = 35
legs = 94

# 假设全是鸡
extra_legs = legs - 2 * heads
rabbits = extra_legs // 2
chickens = heads - rabbits

L15 = [chickens, rabbits]

print("鸡的数量：", chickens)
print("兔子数量：", rabbits)
print("L15 =", L15)
```

```text
L15 = [23, 12]
```

# 解题思路

## 第一题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E4%B8%80%E9%A2%98)

题目：有40个人围成一圈，顺序排号。从第一个人开始报数（只报123这三个数），凡报到数字为3的人退出圈子，问最后留下的是原来第几号的那位。

**步骤：**

1.  创建一个列表 `people`，包含40个元素，每个元素表示一个人，用整数1到40表示。
2.  使用一个循环来模拟报数的过程，每次从第一个人开始，按顺序报数，当报数为3时，将该人从列表中移除。
3.  重复步骤2，直到列表中只剩下一个人为止，输出该人的编号，即为最后留下的人。

**关键点提示：**

1.  这题与第三节的第一题相同，是一个约瑟夫环问题，同样可以套用前面关键点提示的模板。
2.  为了解决这个问题，我们可以使用循环和列表来模拟40个人围成一圈的过程。每次从第一个人开始，按顺序报数，当报到数字为3时，将该人移出圈子。重复这个过程直到只剩下一个人为止，那个人就是最后留下的人。

* * *

## 第二题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E4%BA%8C%E9%A2%98)

题目：编写一个程序，提取以逗号分割的字符串中的所有数字，并将数字重新组合成一个数组；要求输入'34岁,67年,55岁,33岁,12日,98年'这一个字符串，提取出\['34'， '67'， '55'， '33'， '12'， '98'\]，注意数字用字符串来表示，结果保存到L2中；

**步骤：**

1.  定义一个空列表 `numbers`，用于保存提取出的数字。
2.  使用字符串的 `split()` 方法将给定的字符串按逗号进行分割，得到一个字符串列表。
3.  遍历分割后的字符串列表，使用 `replace` 方法对每个字符串中的 `岁`、`年`、`日` 进行替换处理，并添加到 `numbers` 列表中。
4.  输出最终的 `numbers` 列表。

**关键点提示：**

1.  为了解决这个问题，我们可以使用字符串的分割 `spilt` 方法和以及字符串的替换 `replace` 方法来提取以逗号分割的字符串中的所有数字，并将其重新组合成一个数组。
2.  如果小伙伴对正则表达式比较熟悉的话，同样可以使用正则表达式相关方法 `re.findall(r'\d+', string)` 匹配字符串来完成更快捷的操作。

* * *

## 第三题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E4%B8%89%E9%A2%98)

题目：编写一个程序，根据给定的公式计算并打印值: $Q=[(2∗C∗D)/H]$。其中，假定C=50。H=30。D是一个变量，它的值应该**以逗号分隔的序列**输入到程序中。  
要求输入：'100,150,180'这一字符串，依次按逗号分隔出每个数字，并带入公式中计算，计算结果保存到L3数组中【注意：计算出的数字用字符串表示】；

**步骤：**

1.  定义常量 C 和 H 的值。
2.  从输入中获取逗号分隔的序列，然后将其拆分成数字列表。
3.  对于每个数字，按照公式进行计算，将计算结果保存到结果列表中。

**关键点提示：**

1.  `split` 方法可以将某个字符当作分隔符并返回分隔后的字符串列表。

* * *

## 第四题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%9B%9B%E9%A2%98)

题目：编写一个程序，X,Y作为输入数值，根据两个数值会生成一个二维数组，**数组的第i行和第j列的元素值等于i×j**。注意：i和j都是从0开始计；  
要求输入'3, 5'这一字符串，则程序输出为：\[\[0,0,0,0,0\],\[0,1,2,3,4\],\[0,2,4,6,8\]\]；将二维数组转化为一维数组，保存到L4数组中；

**步骤：**

1.  从输入中获取 X 和 Y 的值。
2.  创建一个二维数组，并根据给定的规则进行填充。
3.  将二维数组转换为一维数组。

**关键点提示：**

1.  将二维数组转化为一维数组，主要的思路是依次遍历二维数组中的每一项中的每一个数字，并将其添加到一维数组中。

* * *

## 第五题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E4%BA%94%E9%A2%98)

题目：编写一个程序，以逗号分隔的单词序列作为输入，按照字母顺序对每个单词进行排序，并通过逗号分隔的序列来打印单词。要求输入'without,hello,bag,world'这一字符串，则输出为：\['bag', 'hello', 'without', 'world'\]；将结果保存到数组L5中；

**步骤：**

1.  从输入中获取逗号分隔的单词序列，并将其拆分成单词列表。
2.  对每个单词进行排序。
3.  将排序后的单词列表转换为以逗号分隔的字符串，并保存到结果数组中。

**关键点提示：**

1.  `split` 方法可以将某个字符当作分隔符并返回分隔后的字符串列表。
2.  `sorted` 方法对字符串也可以排序哦，该方法会返回字符串中的字符按照字母顺序排序后的结果。

* * *

## 第六题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%85%AD%E9%A2%98)

题目：编写一个程序，接收一行序列作为输入，并在将句子中的所有字符大写后打印出来。  
要求输入'Practice makes perfect'，并将每个单词大写后的结果保存到数组L6中；

**步骤：**

1.  从输入中获取一行序列，使用 `split` 方法将其分割成单词列表。
2.  对每个单词使用 `upper` 方法进行大写转换。
3.  将大写转换后的单词保存到结果数组中。

**关键点提示：**

1.  将小写字母转换成大写字母可以使用 `upper` 方法进行转换。
2.  `split` 方法可以将某个字符当作分隔符并返回分隔后的字符串列表。

* * *

## 第七题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E4%B8%83%E9%A2%98)

题目：编写一个程序，以一系列空格分隔的单词作为输入，并在删除所有重复的单词后，按字母顺序排序后打印这些单词。  
要求输入'hello world and practice makes perfect and hello world again'这一字符串，将最终结果保存到L7数组中；

**步骤：**

1.  从输入中获取一系列空格分隔的单词，并将其拆分成单词列表。
2.  使用集合（set）来删除所有重复的单词。
3.  将集合中的单词按字母顺序排序，并将结果保存到结果数组中。

**关键点提示：**

1.  集合（set）具有无序性和唯一性的的特点，所以将数据存储在集合中可以很容易的达到去重的目的，但不要忽略集合的无序性，这意味着我们不能够使用下标来访问集合中的元素。

* * *

## 第八题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%85%AB%E9%A2%98)

题目：编写一个程序，接收一系列以逗号分隔的4位二进制数作为输入，然后检查它们是否可被5整除， 可被5整除的数字将以逗号分隔的顺序打印。  
要求输入'0100,0011,1010,1000'这一字符串，将输出结果保存到L8数组中；

**步骤：**

1.  从输入中获取一系列以逗号分隔的4位二进制数，并将它们拆分成一个列表。
2.  遍历列表中的每个二进制数，并将其转换为十进制数。
3.  检查每个十进制数是否可被5整除，如果是，则将其转换为二进制数加入结果数组中。

**关键点提示：**

1.  想要将十进制数转换为二进制数，我们可以使用 `bin` 方法；而将二进制数转换为十进制数，我们可以使用 `int` 方法再将其强制转换回来。

* * *

## 第九题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E4%B9%9D%E9%A2%98)

题目：编写一个程序，找到1000到3000之间并且所有位数均为偶数的所有数字，比如2000，2002等，将最终结果保存到L9中；

**步骤：**

1.  初始化一个空列表 `result`，用于保存满足条件的数字。
2.  使用一个循环遍历1000到3000之间的所有数字。
3.  对于每个数字，将其转换为字符串，便于遍历每位数字。
4.  遍历每位数字，检查是否都为偶数，如果有任何一位数字不是偶数，则跳过当前数字，继续下一个数字的检查。
5.  如果所有位数都为偶数，则将该数字添加到列表 `result` 中。
6.  循环结束后，输出列表 `result`，即包含所有满足条件的数字的列表。

**关键点提示：**

1.  注意本题所要找的数字的所有位数都是偶数，需将各位的数字拆开讨论。

* * *

## 第十题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%8D%81%E9%A2%98)

题目：编写一个输入英文句并计算该句子中共有多少字母和数字的程序。  
要求输入'Hello world! 123'，将该字符串中字母和数字的个数保存到L10中；【注意：这题答案是用数字来表示】

**步骤：**

1.  初始化变量 `letter_count` 和 `digit_count`，用于计算字母和数字的个数，初始值都为0。
2.  初始化变量 `sentence` 存储句子。
3.  遍历句子中的每个字符。
4.  使用 `isalpha()` 方法判断字符是否为字母，如果是，则将 `letter_count` 值加1。
5.  使用 `isdigit()` 方法判断字符是否为数字，如果是，则将 `digit_count` 值加1。
6.  将 `letter_count` 和 `digit_count` 存储在 `result` 列表中。

**关键点提示：**

1.  判断字符是否为字母可以通过 `isalpha` 方法来判断
2.  判断字符是否为数字可以通过 `isdigit` 方法来判断。

* * *

## 第十一题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%8D%81%E4%B8%80%E9%A2%98)

题目：编写一个输入英文句子并计算该句子中大写字母和小写字母数量的程序。  
要求输入'Hello world!'，将大写字母和小写字母的个数存到数组L11中；

**步骤：**

1.  初始化两个变量 `upper_count` 和 `lower_count` 分别用于统计大写字母和小写字母的数量，初始值均为0。
2.  初始化变量 `sentence` 存储英文句子
3.  遍历句子中的每个字符。
4.  判断字符种类，如果是大写字母，则 `upper_count` 加1；如果是小写字母，则 `lower_count` 加1。
5.  将 `upper_count` 和 `lower_count` 存储到数组 `result` 中。

**关键点提示：**

1.  判断字符是否为大写可以通过 `isupper` 方法来判断，判断字符是否为小写可以通过 `islower` 方法来判断。

* * *

## 第十二题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%8D%81%E4%BA%8C%E9%A2%98)

题目：网站要求用户输入用户名和密码进行注册。编写程序以检查用户输入的密码有效性。  
以下是检查密码的标准：  
1 \[a-z\]之间至少有1个字母  
2 \[0-9\]之间至少有1个数字  
3 \[A-Z\]之间至少有一个字母  
4 \[$＃@\]中至少有1个字符  
5 最短交易密码长度：6  
6 交易密码的最大长度：12  
您的程序接收一系列逗号分隔的密码，并将根据上述标准进行检查，将打印符合条件的密码，每个密码用逗号分隔。

要求输入'ABd1234@1,a F1#,2w3E\*,2We3345'，将输出结果保存到L12中；

**步骤：**

1.  初始化一个空列表 `result` 用于存储符合条件的密码。
2.  初始化变量 passwords 用于保存一系列逗号分隔的密码。
3.  使用 `split` 方法将密码按逗号分隔成单个密码。
4.  遍历每个密码，使用 if 语句检查是否符合上述标准。
5.  如果密码符合所有条件，则将其添加到 `result` 列表中。
6.  输出符合条件的密码列表 `result`。

**关键点提示：**

1.  本题主要是使用了 `split` 方法将各段密码进行了分开后 ，使用多级 if-else 语句对密码进行筛选。

* * *

## 第十三题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%8D%81%E4%B8%89%E9%A2%98)

数组1：\[49, 38, 65, 97, 76, 13, 27, 49, 55, 4\] ，排序方法：冒泡排序

将排序后的结果保存到L13中；

**步骤：**

以下是使用冒泡排序算法对数组进行排序的步骤：

1.  定义一个包含待排序元素的数组 `arr1 = [49, 38, 65, 97, 76, 13, 27, 49, 55, 4]`。
2.  创建一个函数 `bubble_sort`，用于实现冒泡排序。
3.  在 `bubble_sort` 函数中，获取数组的长度 `n`，以确定需要进行多少轮遍历。
4.  使用两层嵌套循环，在外层循环中进行 `n` 轮遍历，表示需要比较的次数。
5.  在内层循环中，比较相邻的元素，若前一个元素大于后一个元素，则交换它们的位置，将较大的元素向后移动。
6.  在每一轮遍历后，将最大的元素移到数组末尾。
7.  在外层循环的每一轮遍历中，通过一个标志 `swapped` 来标记是否有元素交换，若一轮遍历中没有交换，则表示数组已经有序，可以提前结束循环。
8.  返回排序后的数组。
9.  调用 `bubble_sort` 函数，并将数组 `arr1` 作为参数传递进去，得到排序后的数组 `sorted_arr`。
10.  将排序后的数组 `sorted_arr` 保存到变量 `result` 中。
11.  输出排序后的结果，即 `result` 数组。

**关键点提示：**

1.  冒泡排序是一种简单的排序算法，它重复地遍历待排序的元素，每次比较相邻的两个元素，并交换它们的位置，直到整个数组变得有序。冒泡排序的基本思想是通过不断地比较相邻元素，将较大（或较小）的元素交换到数组的尾部，从而逐步形成有序序列。
2.  冒泡排序的时间复杂度为O(n^2)，其中n是数组的长度。在最坏的情况下，需要进行n\*(n-1)/2次比较和交换操作。

* * *

## 第十四题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%8D%81%E5%9B%9B%E9%A2%98)

题目：机器人从原点（0,0）开始在平面中移动，机器人可以通过给定的步骤向上，向下，向左和向右移动。  
机器人运动的痕迹如下所示：  
UP 5；DOWN 3；LEFT 3；RIGHT 2；方向之后的数字是步骤。

请编写一个程序，计算一系列运动和原点之后距当前位置的距离。如果距离是浮点数，则只打印最接近的整数。  
要求输入'UP 5；DOWN 3；LEFT 3；RIGHT 2'这一字符串，将最终结果保存到L14中；

**步骤：**

1.  初始化机器人的当前位置为原点，即(x, y) = (0, 0)。
2.  根据输入的字符串，逐步模拟机器人的运动。遍历每个步骤，并根据步骤的方向和数字进行相应的移动。向上移动将y坐标增加，向下移动将y坐标减少，向左移动将x坐标减少，向右移动将x坐标增加。
3.  计算最终位置与原点的距离。使用欧几里得距离公式计算两点之间的距离：distance = sqrt((x - 0)^2 + (y - 0)^2)。
4.  将计算得到的距离取整，保存到result中。

**关键点提示：**

1.  本题最难想到的地方可能是如何把机器人的方向和位移分开。通过分号，我们可以使用 `split` 方法将对机器人的操作分开，形成一个列表 `[UP 5, DOWN 3, LEFT 3, RIGHT 2]`，然后再通过循环，使用 `split` 方法隔开空格两端的方向与位移，并记录到公共属性上即可。

* * *

## 第十五题[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E7%AC%AC%E5%8D%81%E4%BA%94%E9%A2%98)

题目：假定我们数农场里的鸡和兔子中有35个头和94条腿。问我们有多少只兔子和多少只鸡？将最终结果保存到数组L15中；

### 解法 1：暴力枚举法[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E8%A7%A3%E6%B3%95-1%EF%BC%9A%E6%9A%B4%E5%8A%9B%E6%9E%9A%E4%B8%BE%E6%B3%95)

**步骤：**

1.  定义一个函数`calculate_chicken_and_rabbit`，该函数接受两个参数`heads`和`legs`，分别表示头的数量和腿的数量。函数的目标是找出可能的鸡和兔子数量组合。
2.  在函数内部，使用一个循环枚举所有可能的鸡的数量。假设鸡的数量为x，那么兔子的数量就是`heads - x`。
3.  验证当前的鸡和兔子数量组合是否满足给定的腿的数量。根据题目中鸡和兔子的腿数分别为2和4，可以得到方程`2 * x + 4 * y = legs`，其中y表示兔子的数量。
4.  如果找到满足条件的鸡和兔子数量组合，将它们保存到一个结果数组中，并返回结果数组。
5.  在主程序中，输入头的数量和腿的数量，并调用`calculate_chicken_and_rabbit`函数计算鸡和兔子的数量。最后，将结果保存到数组 `result` 中，并打印输出。

**关键点提示：**

1.  该方法是比较容易想到与实现的方法，通过暴力枚举鸡的数量，并让其符合相应的等式，我们可以很容易的获取鸡兔同笼问题的答案。

### 解法 2：矩阵求解法[¶](https://www.heywhale.com/api/notebooks/64c86d9a3cbcbda8f58557a0/RenderedContent?embed_doc=true&layout=normal&jwtToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE1YTg0OTVjZDE3NDAwMTc0MjlmNDkiLCJpYXQiOjE3NTE1MTEyOTIsImV4cCI6MTc1MTU5NzY5Mn0.8EGF7pVlyunNw7q0N2ok3O63IUCqGX1XeEpeIZr1Vho&cellcomment=1&cellbookmark=1#%E8%A7%A3%E6%B3%95-2%EF%BC%9A%E7%9F%A9%E9%98%B5%E6%B1%82%E8%A7%A3%E6%B3%95)

要解决这个问题，我们可以使用代数方程组的方法来计算鸡和兔子的数量，这种方法可能更符合我们平时计算的情况。

设鸡的数量为x，兔子的数量为y。根据题目条件，我们可以得到以下两个方程：

1.  x + y = 35（头的数量）
2.  2x + 4y = 94（腿的数量）

现在我们可以解这个方程组，求出x和y的值。

**步骤：**

1.  定义一个函数，接收头的数量和腿的数量作为输入，并计算鸡和兔子的数量。
2.  在函数内部，使用代数方程组的解法来计算x和y的值。可以使用Python的解方程组函数，也可以手动解方程组。
3.  将计算得到的鸡和兔子的数量保存到result数组中。

**关键点提示：**

1.  `np.linalg.solve`是NumPy库中用于求解线性方程组的函数。它可以在给定系数矩阵和常数向量的情况下，求解线性方程组的解。对于本题，可以将问题转化为一个线性方程组，其中x表示鸡的数量，y表示兔子的数量。

2.  首先，我们有两个方程：

    鸡的头数兔子的头数总头数鸡的头数+兔子的头数\=总头数  
    鸡的腿数兔子的腿数总腿数鸡的腿数+兔子的腿数\=总腿数

    将其转化为线性方程组的形式：  
    x+y\=heads  
    2x+4y\=legs

    转换成系数矩阵的形式后，就可以使用`np.linalg.solve`来求解这个线性方程组，得到鸡和兔子的数量。




