---
layout: post
title: "白话 DeepSeek 01｜从函数到神经网络"
date: 2025-10-05
tags:
  - DeepSeek
  - 神经网络
categories:
  - DeepSeek
  - 白话 DeepSeek 系列
comments: true
math: true
mermaid: true
author: deathwhispers
---

# 从函数到神经网络：技术演进与核心关联解析

## 摘要

神经网络是当前人工智能领域的核心技术之一，但其本质是对“函数”这一基础数学概念的复杂延伸与组合。从早期人工智能符号主义（追求精确函数）到现代联结主义（追求函数近似），技术路线的转变揭示了神经网络的本质：通过层级嵌套和参数优化，构造一个能够逼近任意复杂映射关系的复合函数。本文将从函数定义出发，逐层剖析感知机、多层网络的构建逻辑，最终揭示函数与神经网络的内在关联。

## 第一章 函数基础：神经网络的数学基石

函数是描述输入与输出之间映射关系的工具，即给定输入值（自变量 x ），通过特定规则计算得到唯一的输出值（因变量 y ）。通用表达式为 y=f(x)。

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/4e04986a-d4f4-4c1b-a2d8-44980c6471ef/d59e3775-f271-4ede-9d47-d058ab0b28cd/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SKZMH324%2F20251016%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251016T030510Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAGER6U0Vg6PjEDWGfefl3AMGii2kVbl7aILZ5Un5AQ5AiEAocAcDDnjcH%2F%2BapmsMnFmjLzF%2FBwSghOrHDvPFCtqLyoqiAQIg%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDNk5pCCgi1g%2Fl0H7OircA5qDFu3ccSZBlJ4jpRX6ZcLLlR2Kczpu%2BXAkqO3VtH9u8cW93woeBPO20lD%2BnGwkCCA64L%2BiEf0m4eIAkC7VPUDW%2BjRU4TXd9p2i5NVGK1ZwVRUYmPKx7kU8tTRk6517%2BP%2F%2BHZzX%2BqF0NL4NiudeovvA9eKkLSujKNEHQQcDzi0z61jQfiKAC9r8Vfd0a0BcDgQbnlj8Q4xPIPnirfR3x0BhZLAJcWnfgpUCx%2FYdsy9qiGX%2BBK7xXKLrAf69G27Nk6oy6qhrkvfmAjWBFg2hmMYJhsnIb1y5vIP4vmkaRS%2BTCGHtnP7CBYuaalcYCij9ldPsZd5i6kQhDuwJKC%2B0UpfX0z0PT6UVWFT2yTIiFD7fBGI05Aa1csqTWXqEhyeJkFyXPlLf5sN%2BPC6eDwdI%2FxDNccLdjXAesdDOCiF8itfVlK8G853bHD3LkSLL7IhMGnaOVp60eiPhJsRPd11ib0a8UR2VmffYebqQEAgPCBu8uUEF1SB43IcGXAfWegYq4eJ611JfnOhByNYb7ozVoHCqrx4iemrjXb9hLRGiBzd5ZMu6k3p3CKvAzXJP%2Bc5aV5A1eBrxvaD4eqBCyXAoJoZ6wKR8Ff9%2F7NunaYKQxB6390591Uihns74G6WlMN2ewccGOqUB3mAOWySU9VPmAWVpdz%2FU09WEOxqVjOWD9J4M6TNzBqlyPDiMlHyuR05krLs00oDwGdeQXtThebZGbRTH80vjhLmlSIb16OXd%2F3wdXJBLzc4iHH8jzDOLojvT9yzLuCSBuWqICvIOzK%2B1dlpfQz8g5wraWrRcxlzXl65XnzyYrPKaW390ghjEAirx595ZVOzmvpZlLiQEf%2FSSlq5C5jrsBPuXJS67&X-Amz-Signature=ffcf54904f1e39eaec4cd95e03add952d766c77d6f65bfbea809add684b5403d&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![](data:,)

![](data:,)

![](data:,)



### 1.1 从“精确解”到“近似解”：联结主义的引入

早期人工智能的符号主义试图为每一个问题找到一个精确的数学函数来表示。但但是很多时候，我们没办法找到一个精确的函数来描述某个关系，退而求其次选择一个近似解也不错，也就是说函数没必要精确的通过每一个点，它只需要最接近结果就好了，这就是联结主义。

联结主义的引入，则转变了思路：既然无法找到精确函数，不如退而求其次，找到一个可以无限逼近真实关系的“近似函数”。这一思想是神经网络诞生的根本驱动力。

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/4e04986a-d4f4-4c1b-a2d8-44980c6471ef/ab8dd484-ea4f-4a77-9123-823986f7a3bc/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SKZMH324%2F20251016%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251016T030510Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAGER6U0Vg6PjEDWGfefl3AMGii2kVbl7aILZ5Un5AQ5AiEAocAcDDnjcH%2F%2BapmsMnFmjLzF%2FBwSghOrHDvPFCtqLyoqiAQIg%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDNk5pCCgi1g%2Fl0H7OircA5qDFu3ccSZBlJ4jpRX6ZcLLlR2Kczpu%2BXAkqO3VtH9u8cW93woeBPO20lD%2BnGwkCCA64L%2BiEf0m4eIAkC7VPUDW%2BjRU4TXd9p2i5NVGK1ZwVRUYmPKx7kU8tTRk6517%2BP%2F%2BHZzX%2BqF0NL4NiudeovvA9eKkLSujKNEHQQcDzi0z61jQfiKAC9r8Vfd0a0BcDgQbnlj8Q4xPIPnirfR3x0BhZLAJcWnfgpUCx%2FYdsy9qiGX%2BBK7xXKLrAf69G27Nk6oy6qhrkvfmAjWBFg2hmMYJhsnIb1y5vIP4vmkaRS%2BTCGHtnP7CBYuaalcYCij9ldPsZd5i6kQhDuwJKC%2B0UpfX0z0PT6UVWFT2yTIiFD7fBGI05Aa1csqTWXqEhyeJkFyXPlLf5sN%2BPC6eDwdI%2FxDNccLdjXAesdDOCiF8itfVlK8G853bHD3LkSLL7IhMGnaOVp60eiPhJsRPd11ib0a8UR2VmffYebqQEAgPCBu8uUEF1SB43IcGXAfWegYq4eJ611JfnOhByNYb7ozVoHCqrx4iemrjXb9hLRGiBzd5ZMu6k3p3CKvAzXJP%2Bc5aV5A1eBrxvaD4eqBCyXAoJoZ6wKR8Ff9%2F7NunaYKQxB6390591Uihns74G6WlMN2ewccGOqUB3mAOWySU9VPmAWVpdz%2FU09WEOxqVjOWD9J4M6TNzBqlyPDiMlHyuR05krLs00oDwGdeQXtThebZGbRTH80vjhLmlSIb16OXd%2F3wdXJBLzc4iHH8jzDOLojvT9yzLuCSBuWqICvIOzK%2B1dlpfQz8g5wraWrRcxlzXl65XnzyYrPKaW390ghjEAirx595ZVOzmvpZlLiQEf%2FSSlq5C5jrsBPuXJS67&X-Amz-Signature=2f17cd5f93ac6b7931a008611cc96ac8ac30012802fc2b0f510d83ace3d6b0d5&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



### 1.2 多输入函数的扩展与线性变换

现实问题中输入往往是多维的（如图片的像素、文本的特征），此时函数扩展为多变量形式 y=f(x_1,x_2,…,x_n)。

其线性形式可表示为：

![](data:,)

$z=w_1x_1+w_2x_2+⋯+w_nx_n+b=
\sum_{i=1}^n(w_ix_i)+b$

![](data:,)

其中，w_1∼w_n 为权重（Weights），b 为偏置（Bias）。这一加权求和（线性变换）正是神经网络神经元的核心计算逻辑。权重 w_i 代表了不同输入对输出影响的程度。



但是当数据稍微变化一下，出现曲线的时候，简单的线性函数就没办法解决这个问题了。那我们的目标就是将线性函数转为非线性函数，这可以通过套一个非线性函数来做到，比如平方、正弦函数、指数函数。这就是激活函数。





![](https://prod-files-secure.s3.us-west-2.amazonaws.com/4e04986a-d4f4-4c1b-a2d8-44980c6471ef/60d5ce59-9f70-4160-844b-04d9fed3503b/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SKZMH324%2F20251016%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251016T030510Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAGER6U0Vg6PjEDWGfefl3AMGii2kVbl7aILZ5Un5AQ5AiEAocAcDDnjcH%2F%2BapmsMnFmjLzF%2FBwSghOrHDvPFCtqLyoqiAQIg%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDNk5pCCgi1g%2Fl0H7OircA5qDFu3ccSZBlJ4jpRX6ZcLLlR2Kczpu%2BXAkqO3VtH9u8cW93woeBPO20lD%2BnGwkCCA64L%2BiEf0m4eIAkC7VPUDW%2BjRU4TXd9p2i5NVGK1ZwVRUYmPKx7kU8tTRk6517%2BP%2F%2BHZzX%2BqF0NL4NiudeovvA9eKkLSujKNEHQQcDzi0z61jQfiKAC9r8Vfd0a0BcDgQbnlj8Q4xPIPnirfR3x0BhZLAJcWnfgpUCx%2FYdsy9qiGX%2BBK7xXKLrAf69G27Nk6oy6qhrkvfmAjWBFg2hmMYJhsnIb1y5vIP4vmkaRS%2BTCGHtnP7CBYuaalcYCij9ldPsZd5i6kQhDuwJKC%2B0UpfX0z0PT6UVWFT2yTIiFD7fBGI05Aa1csqTWXqEhyeJkFyXPlLf5sN%2BPC6eDwdI%2FxDNccLdjXAesdDOCiF8itfVlK8G853bHD3LkSLL7IhMGnaOVp60eiPhJsRPd11ib0a8UR2VmffYebqQEAgPCBu8uUEF1SB43IcGXAfWegYq4eJ611JfnOhByNYb7ozVoHCqrx4iemrjXb9hLRGiBzd5ZMu6k3p3CKvAzXJP%2Bc5aV5A1eBrxvaD4eqBCyXAoJoZ6wKR8Ff9%2F7NunaYKQxB6390591Uihns74G6WlMN2ewccGOqUB3mAOWySU9VPmAWVpdz%2FU09WEOxqVjOWD9J4M6TNzBqlyPDiMlHyuR05krLs00oDwGdeQXtThebZGbRTH80vjhLmlSIb16OXd%2F3wdXJBLzc4iHH8jzDOLojvT9yzLuCSBuWqICvIOzK%2B1dlpfQz8g5wraWrRcxlzXl65XnzyYrPKaW390ghjEAirx595ZVOzmvpZlLiQEf%2FSSlq5C5jrsBPuXJS67&X-Amz-Signature=8c16b17febd286c7e4c2afb532b1748d479010d642b4bdb3682b33c7a6510f49&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![](data:,)

![](data:,)

![](data:,)

## 第二章 从多输入函数到感知机：神经网络的基本单元

感知机（Perceptron）是神经网络的“最小单元”，其本质是“线性函数 + 非线性激活函数”的组合体。

### 2.1 感知机的结构与函数映射

一个感知机对应一个完整的函数映射过程：

1. 线性加权求和（输入层的线性函数）：对输入 X 和权重 W 进行点积运算并加偏置 b。

1. 非线性激活（引入非线性函数）：将线性输出 z 代入非线性激活函数 σ(⋅)。

激活函数 σ(⋅) 使得感知机能够解决线性不可分的问题（如曲线分类），是打破线性关系、实现复杂函数近似的关键。

![](data:,)

### 2.2 神经元的图形化理解

在神经网络的图示中，一个神经元（小圆圈）就代表了一个完整的感知机（即一个多输入非线性函数）。信号从左侧输入，在神经元内进行加权求和和激活变换，最终从右侧输出。

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/4e04986a-d4f4-4c1b-a2d8-44980c6471ef/59ac66bd-a459-480d-9b7e-ee8db2ffe311/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SKZMH324%2F20251016%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251016T030510Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAGER6U0Vg6PjEDWGfefl3AMGii2kVbl7aILZ5Un5AQ5AiEAocAcDDnjcH%2F%2BapmsMnFmjLzF%2FBwSghOrHDvPFCtqLyoqiAQIg%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDNk5pCCgi1g%2Fl0H7OircA5qDFu3ccSZBlJ4jpRX6ZcLLlR2Kczpu%2BXAkqO3VtH9u8cW93woeBPO20lD%2BnGwkCCA64L%2BiEf0m4eIAkC7VPUDW%2BjRU4TXd9p2i5NVGK1ZwVRUYmPKx7kU8tTRk6517%2BP%2F%2BHZzX%2BqF0NL4NiudeovvA9eKkLSujKNEHQQcDzi0z61jQfiKAC9r8Vfd0a0BcDgQbnlj8Q4xPIPnirfR3x0BhZLAJcWnfgpUCx%2FYdsy9qiGX%2BBK7xXKLrAf69G27Nk6oy6qhrkvfmAjWBFg2hmMYJhsnIb1y5vIP4vmkaRS%2BTCGHtnP7CBYuaalcYCij9ldPsZd5i6kQhDuwJKC%2B0UpfX0z0PT6UVWFT2yTIiFD7fBGI05Aa1csqTWXqEhyeJkFyXPlLf5sN%2BPC6eDwdI%2FxDNccLdjXAesdDOCiF8itfVlK8G853bHD3LkSLL7IhMGnaOVp60eiPhJsRPd11ib0a8UR2VmffYebqQEAgPCBu8uUEF1SB43IcGXAfWegYq4eJ611JfnOhByNYb7ozVoHCqrx4iemrjXb9hLRGiBzd5ZMu6k3p3CKvAzXJP%2Bc5aV5A1eBrxvaD4eqBCyXAoJoZ6wKR8Ff9%2F7NunaYKQxB6390591Uihns74G6WlMN2ewccGOqUB3mAOWySU9VPmAWVpdz%2FU09WEOxqVjOWD9J4M6TNzBqlyPDiMlHyuR05krLs00oDwGdeQXtThebZGbRTH80vjhLmlSIb16OXd%2F3wdXJBLzc4iHH8jzDOLojvT9yzLuCSBuWqICvIOzK%2B1dlpfQz8g5wraWrRcxlzXl65XnzyYrPKaW390ghjEAirx595ZVOzmvpZlLiQEf%2FSSlq5C5jrsBPuXJS67&X-Amz-Signature=cf9a4cfb07cc8e9b743abe388058471c60b66dc582f3090d4dd9f78a6687a371&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



## 第三章 多层组合：从感知机到神经网络

单个感知机无法处理异或（XOR）等更复杂的任务。通过将多个感知机按层级连接，利用函数的函数（Function of a Function）实现更复杂的映射，便构成了多层感知机（Multi-Layer Perceptron, MLP），即神经网络。

### 3.1 神经网络的层级结构与函数链

神经网络通过“输入层→隐藏层→输出层”的结构，实现从原始输入到目标输出的复杂函数映射。

1. 隐藏层（Hidden Layer）：由多个感知机构成。每一层的输出 H^k 都是上一层输出 H^{k−1} 的输入，形成函数嵌套关系。

![](data:,)

![](data:,)

$H^k=σ(W^k⋅H^{k−1}+b^k)$

![](data:,)

隐藏层的主要作用是对输入数据进行复杂的特征提取和变换。

1. 网络整体映射：整个神经网络的函数映射是一个深度嵌套的复合函数：

$Y=f_{out}(…f_2(f_1(X))…)$

![](data:,)

其中 f_i 代表第 i 层的函数映射。网络的深度（隐藏层数量）和宽度（每层神经元数量）决定了其函数拟合能力的复杂程度。

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/4e04986a-d4f4-4c1b-a2d8-44980c6471ef/4b0cbea1-ab56-4046-82e2-58ce064feab6/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SKZMH324%2F20251016%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251016T030510Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAGER6U0Vg6PjEDWGfefl3AMGii2kVbl7aILZ5Un5AQ5AiEAocAcDDnjcH%2F%2BapmsMnFmjLzF%2FBwSghOrHDvPFCtqLyoqiAQIg%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDNk5pCCgi1g%2Fl0H7OircA5qDFu3ccSZBlJ4jpRX6ZcLLlR2Kczpu%2BXAkqO3VtH9u8cW93woeBPO20lD%2BnGwkCCA64L%2BiEf0m4eIAkC7VPUDW%2BjRU4TXd9p2i5NVGK1ZwVRUYmPKx7kU8tTRk6517%2BP%2F%2BHZzX%2BqF0NL4NiudeovvA9eKkLSujKNEHQQcDzi0z61jQfiKAC9r8Vfd0a0BcDgQbnlj8Q4xPIPnirfR3x0BhZLAJcWnfgpUCx%2FYdsy9qiGX%2BBK7xXKLrAf69G27Nk6oy6qhrkvfmAjWBFg2hmMYJhsnIb1y5vIP4vmkaRS%2BTCGHtnP7CBYuaalcYCij9ldPsZd5i6kQhDuwJKC%2B0UpfX0z0PT6UVWFT2yTIiFD7fBGI05Aa1csqTWXqEhyeJkFyXPlLf5sN%2BPC6eDwdI%2FxDNccLdjXAesdDOCiF8itfVlK8G853bHD3LkSLL7IhMGnaOVp60eiPhJsRPd11ib0a8UR2VmffYebqQEAgPCBu8uUEF1SB43IcGXAfWegYq4eJ611JfnOhByNYb7ozVoHCqrx4iemrjXb9hLRGiBzd5ZMu6k3p3CKvAzXJP%2Bc5aV5A1eBrxvaD4eqBCyXAoJoZ6wKR8Ff9%2F7NunaYKQxB6390591Uihns74G6WlMN2ewccGOqUB3mAOWySU9VPmAWVpdz%2FU09WEOxqVjOWD9J4M6TNzBqlyPDiMlHyuR05krLs00oDwGdeQXtThebZGbRTH80vjhLmlSIb16OXd%2F3wdXJBLzc4iHH8jzDOLojvT9yzLuCSBuWqICvIOzK%2B1dlpfQz8g5wraWrRcxlzXl65XnzyYrPKaW390ghjEAirx595ZVOzmvpZlLiQEf%2FSSlq5C5jrsBPuXJS67&X-Amz-Signature=afd268976e711b6bed95b2a319d81ae3c347257a763dea281c424f4e20d4bb18&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



### 3.2 神经网络的“学习”本质：函数参数优化

神经网络的训练过程，本质是通过优化网络中的所有参数（权重和偏置），使网络的输出尽可能接近真实标签。

这一过程可理解为：

1. 定义函数空间：网络的结构（层数、神经元数）定义了一个“所有可能的复合函数”的空间。

1. 搜索最优解：通过反向传播算法和梯度下降，在上述函数空间中，找到最接近“真实映射函数”的那一个，即找到最优的 W 和 b 组合。



因此，神经网络的“学习”过程，就是寻找最优函数参数，以实现复杂函数近似的过程。

## 第四章 核心关联与演进逻辑总结

从函数到神经网络的演进逻辑，是数学原理与计算需求的完美结合：

1. 基础单元：单输入函数 → 多输入函数，为神经元的加权求和提供数学基础。

1. 非线性突破：线性函数 + 激活函数 → 感知机，通过非线性激活函数实现简单非线性映射。

1. 复杂映射：感知机多层堆叠 → 神经网络，通过复合函数（函数嵌套）实现任意复杂输入输出关系。

1. 自适应优化：联结主义思想 + 反向传播算法 → 动态调整函数参数，使网络“学会”最优的函数逼近。



简言之，神经网络并非脱离数学基础的“黑盒”，而是以函数为核心，通过层级组合与参数优化形成的强大计算模型。 理解这一演进脉络，是掌握神经网络原理与应用的关键。

![](data:,)

![](data:,)

![](data:,)

![](data:,)

![](data:,)

![](data:,)

![](data:,)

![](data:,)

![](data:,)

![](data:,)

