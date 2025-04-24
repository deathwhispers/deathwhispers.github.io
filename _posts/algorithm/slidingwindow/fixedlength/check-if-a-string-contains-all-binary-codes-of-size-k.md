---
layout: post 
title: "检查一个字符串是否包含所有长度为 K 的二进制子串"
date: 2025-04-24 
tags: [滑动窗口,位运算,哈希表,字符串,滚动哈希]
comments: true 
author: deathwhispers
---
# [检查一个字符串是否包含所有长度为 K 的二进制子串](https://leetcode.cn/problems/check-if-a-string-contains-all-binary-codes-of-size-k/description)
给你一个二进制字符串 s 和一个整数 k 。如果所有长度为 k 的二进制字符串都是 s 的子串，请返回 true ，否则请返回 false 。

## 思路一
1. **初始化存储结构**：创建一个用于存储子串的集合（如HashSet或set）。
2. **提取子串**：按顺序从字符串中提取长度为 k 的所有子串。
3. **存入集合**：将每个提取到的子串存入集合中。
4. **判断结果**：检查集合中元素个数是否不少于 \(2^k\)，得出是否包含所有对应长度子串的结论。

### Java 实现
```java
public boolean hasAllCodes(String s, int k) {
    HashSet<String> hashSet = new HashSet<>();
    for (int i = 0; i + k <= s.length(); i++) {
        hashSet.add(s.substring(i, i + k));
    }
    return hashSet.size() >= Math.pow(2, k);
}
```
### Python 实现
```python
class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        seen = set()
        for i in range(len(s) - k + 1):
            sub_str = s[i:i + k]
            seen.add(sub_str)
        return len(seen) >= 2 ** k
```
### 代码解释：
1. **函数声明及初始化**：`has_all_binary_substrings` 函数接受两个参数，字符串 `s` 和子串长度 `K`。 `total_substrings` 计算出长度为 `K` 的所有可能二进制子串的数量。`seen` 是一个集合，用于保存已经出现过的子串。
2. **遍历字符串提取子串**： 使用 `for` 循环遍历字符串 `s`，每次循环提取长度为 `K` 的子串。
3. **检查子串并判断结果**：如果子串不在 `seen` 集合中，将其添加进去，当 `seen` 集合中的子串数量等于总的可能子串数量时，返回 `True`。如果循环结束没有达到这个数量，返回 `False`。

## 思路二
1. **初始化构建工具**：创建一个用于构建子串的工具（如StringBuilder或列表）。
2. **子串构建与处理**：逐个扫描字符串中的字符，将其加入构建工具。当构建的子串长度达到 k 时，存入集合并移除构建工具的第一个字符。
3. **判断结果**：和第一种方法一样，通过集合元素个数是否不小于 \(2^k\) 判断结果。
### Java 实现
```java
public boolean hasAllCodes2(String s, int k) {
    StringBuilder builder = new StringBuilder();
    char[] cs = s.toCharArray();
    int n = cs.length;
    HashSet<String> hashSet = new HashSet<>();
    for (int i = 0; i < n; i++) {
        builder.append(cs[i]);
        if (i < k - 1) {
            continue;
        }
        hashSet.add(builder.toString());
        builder.deleteCharAt(0);
    }
    return hashSet.size() >= Math.pow(2, k);
}
```
### Python 实现
```python
class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        seen = set()
        builder = []
        for i, char in enumerate(s):
            builder.append(char)    
            if i < k - 1:
                continue
            sub_str = ''.join(builder)
            seen.add(sub_str)
            builder.pop(0)
        return len(seen) >= 2 ** k
```
## 总结
两种思路核心都是处理和统计长度为 k 的子串，步骤类似但子串生成方式有别。
