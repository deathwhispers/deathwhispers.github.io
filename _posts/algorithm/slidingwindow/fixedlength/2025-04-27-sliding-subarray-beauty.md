---
layout: post 
title: "滑动子数组的美丽值"
date: 2025-04-25
tags: [滑动窗口, 数组, 哈希表]
comments: true 
author: deathwhispers
---

## 描述
给你一个长度为 n 的整数数组 nums ，请你求出每个长度为 k 的子数组的 美丽值 。

一个子数组的 美丽值 定义为：如果子数组中第 x 小整数 是 负数 ，那么美丽值为第 x 小的数，否则美丽值为 0 。

请你返回一个包含 n - k + 1 个整数的数组，依次 表示数组中从第一个下标开始，每个长度为 k 的子数组的 美丽值 。

子数组指的是数组中一段连续 非空 的元素序列。

## 解题思路

## 代码实现
```java
public int[] getSubarrayBeauty(int[] nums, int k, int x) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    // 遍历每个长度为k的子数组
    for (int i = 0; i <= n - k; i++) {
        // 计数排序数组，假设值域较小，我们可以预设一个合理的范围
        int[] count = new int[201];  // 设定值域为[-100, 100] -> 范围大小为201
        // 统计当前子数组的每个数
        for (int j = i; j < i + k; j++) {
            count[nums[j] + 100]++;  // 偏移+100，处理负数
        }
        // 遍历负数，找到第x小的负数
        int negativeCount = 0;
        int beautyValue = 0;
        for (int j = 0; j < 100; j++) {  // 负数在[-100, -1]之间
            negativeCount += count[j];
            if (negativeCount >= x) {
                beautyValue = j - 100;  // 恢复为原始的负数
                break;
            }
        }
        // 如果没有找到第x小的负数，返回0
        if (negativeCount < x) {
            beautyValue = 0;
        }
        result[i] = beautyValue;
    }
    return result;
}
```

```java
public int[] getSubarrayBeauty2(int[] nums, int k, int x) {
    final int BIAS = 50;
    int[] cnt = new int[BIAS * 2 + 1];
    for (int i = 0; i < k - 1; i++) { // 先往窗口内添加 k-1 个数
        cnt[nums[i] + BIAS]++;
    }

    int n = nums.length;
    int[] ans = new int[n - k + 1];
    for (int i = k - 1; i < n; i++) {
        cnt[nums[i] + BIAS]++; // 进入窗口（保证窗口有恰好 k 个数）
        int left = x;
        for (int j = 0; j < BIAS; j++) { // 暴力枚举负数范围 [-50,-1]
            left -= cnt[j];
            if (left <= 0) { // 找到美丽值
                ans[i - k + 1] = j - BIAS;
                break;
            }
        }
        cnt[nums[i - k + 1] + BIAS]--; // 离开窗口
    }
    return ans;
}
```

https://leetcode.cn/problems/sliding-subarray-beauty/description/

