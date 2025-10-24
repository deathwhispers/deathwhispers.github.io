---
layout: post
title: "一文学会在Markdown中编辑数学符号与公式"
date: 2025-10-24
tags:
  - Markdown
  - LaTeX
categories:
  []
comments: true
math: true
mermaid: true
author: deathwhispers
---

# 一文学会在Markdown中编辑数学符号与公式

在用Markdown写博客时会涉及到数学符号与公式的编辑，下面进行汇总。随手记录，方便你我他。

- 行内公式：将公式插入到本行内

```bash
$0.98^{365} \approx 0.0006$
```

我的365天：$0.98^{365} \approx 0.0006$

- 单独的公式块：将公式插入到新的一行内，并且居中

```bash
$$
1.02^{365} \approx 1377.4
$$
```

在座各位大佬的365天：

$$
1.02^{365} \approx 1377.4
$$

## 符号

### 上下标、运算符

### 括号

### 三角函数、指数、对数

### 数学符号

### 连线符号

### 高级运算符

### 集合运算

### 希腊字母

### 字体转换

若要对公式的某一部分字符进行字体转换，可以用 {\font {需转换的部分字符}} 命令，其中\font部分可以参照下表选择合适的字体。一般情况下，公式默认为意大利体。

## 公式

### 基本函数公式

- 行内公式：$\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt$

```bash
$\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt$

```

- 行间公式：

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt
$$

```bash
$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt
$$

```

- $y_k=\varphi(u_k+v_k)$

```bash
$y_k=\varphi(u_k+v_k)$

```

- $y(x)=x^3+2x^2+x+1$

```bash
$y(x)=x^3+2x^2+x+1$

```

- $x^{y}=(1+{\rm e}^x)^{-2xy}$

```bash
$x^{y}=(1+{\rm e}^x)^{-2xy}$

```

- $\displaystyle f(n)=\sum_{i=1}^{n}{n*(n+1)}$

```bash
$\displaystyle f(n)=\sum_{i=1}^{n}{n*(n+1)}$

```

### 分段函数#

- 分段函数：

$$
y=\begin{cases}
2x+1, & x \leq0\\
x, & x>0
\end{cases}
$$

```bash
$$
y=\begin{cases}
2x+1, & x \leq0\\
x, & x>0
\end{cases}
$$

```

- 方程组：

$$
\left \{
\begin{array}{c}
a_1x+b_1y+c_1z=d_1 \\
a_2x+b_2y+c_2z=d_2 \\
a_3x+b_3y+c_3z=d_3
\end{array}
\right.
$$

```bash
$$
\left \{
\begin{array}{c}
a_1x+b_1y+c_1z=d_1 \\
a_2x+b_2y+c_2z=d_2 \\
a_3x+b_3y+c_3z=d_3
\end{array}
\right.
$$

```

### 积分#

- 积分书写：

$$
\int_{\theta_1(x)}^{\theta_2(x)}=l
$$

```bash
$$
\int_{\theta_1(x)}^{\theta_2(x)}=l
$$

```

- 二重积分：

$$
\iint dx dy=\sigma
$$

```bash
$$
\iint dx dy=\sigma
$$

```

- 三重积分：

$$
\iiint dx dydz=\nu
$$

```bash
$$
\iiint dx dydz=\nu
$$

```

### 微分和偏微分#

- 一阶微分方程：

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

```bash
$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

```

$$
\left. \frac{{\rm d}y}{{\rm d}x} \right|_{x=0}=3x+1=1
$$

```bash
$$
\left. \frac{{\rm d}y}{{\rm d}x} \right|_{x=0}=3x+1=1
$$

```

- 二阶微分方程：

$$
y''+py'+qy=f(x)
$$

```bash
$$
y''+py'+qy=f(x)
$$

```

$$
\frac{d^2y}{dx^2}+p\frac{dy}{dx}+qy=f(x)
$$

```bash
$$
\frac{d^2y}{dx^2}+p\frac{dy}{dx}+qy=f(x)
$$

```

- 偏微分方程：

$$
\frac{\partial u}{\partial t}= h^2 \left( \frac{\partial^2 u}{\partial x^2} +\frac{\partial^2 u}{\partial y^2}+ \frac{\partial^2 u}{\partial z^2}\right)
$$

```bash
$$
\frac{\partial u}{\partial t}= h^2 \left( \frac{\partial^2 u}{\partial x^2} +\frac{\partial^2 u}{\partial y^2}+ \frac{\partial^2 u}{\partial z^2}\right)
$$

```

### 矩阵和行列式#

起始标记 \begin{matrix} ,结束标记\end{matrix},每一行末尾标记\，行间元素之间以&分隔。在起始、结束标记处用下列词替换matrix。

- pmatrix ：小括号边框

$$
\begin{pmatrix}
1&2\\
3&4\\
\end{pmatrix}
$$

```bash
$$
\begin{pmatrix}
1&2\\
3&4\\
\end{pmatrix}
$$

```

- bmatrix ：中括号边框

$$
\begin{bmatrix}
1&2\\
3&4\\
\end{bmatrix}
$$

```bash
$$
\begin{bmatrix}
1&2\\
3&4\\
\end{bmatrix}
$$

```

- Bmatrix ：大括号边框

$$
\begin{Bmatrix}
1&2\\
3&4\\
\end{Bmatrix}
$$

```bash
$$
\begin{Bmatrix}
1&2\\
3&4\\
\end{Bmatrix}
$$

```

- vmatrix ：单竖线边框

$$
\begin{vmatrix}
1&2\\
3&4\\
\end{vmatrix}
$$

```bash
$$
\begin{vmatrix}
1&2\\
3&4\\
\end{vmatrix}
$$

```

- Vmatrix ：双竖线边框

$$
\begin{Vmatrix}
1&2\\
3&4\\
\end{Vmatrix}
$$

```bash
$$
\begin{Vmatrix}
1&2\\
3&4\\
\end{Vmatrix}
$$

```

- 无框矩阵：

$$
\begin{matrix}
    1 & x & x^2 \\
    1 & y & y^2 \\
    1 & z & z^2 \\
\end{matrix}
$$

```bash
$$
\begin{matrix}
    1 & x & x^2 \\
    1 & y & y^2 \\
    1 & z & z^2 \\
\end{matrix}
$$

```

- 单位矩阵：

$$
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&1\\
\end{bmatrix}
$$

```bash
$$
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&1\\
\end{bmatrix}
$$

```

- m×n矩阵：

$$
A=\begin{bmatrix}
{a_{11}}&{a_{12}}&{\cdots}&{a_{1n}}\\
{a_{21}}&{a_{22}}&{\cdots}&{a_{2n}}\\
{\vdots}&{\vdots}&{\ddots}&{\vdots}\\
{a_{m1}}&{a_{m2}}&{\cdots}&{a_{mn}}\\
\end{bmatrix}
$$