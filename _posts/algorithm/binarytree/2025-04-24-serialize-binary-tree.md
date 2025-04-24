---
layout: post 
title: "序列化二叉树"
date: 2025-04-24 
tags: [二叉树]
comments: true 
author: deathwhispers
---



```java
package com.dw.algorithm.binarytree;

import com.dw.common.TreeNode;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * 序列化二叉树
 *
 * @author yanggj
 * @version 1.0.0
 * @date 2023/2/16 16:11
 */
public class SerializeBinaryTree {

    TreeNode empty = new TreeNode(Integer.MIN_VALUE);

    // Encodes a tree to a single string.
    public String serialize(TreeNode root) {
        if (root == null) {
            return "";
        }
        StringBuilder builder = new StringBuilder();
        Deque<TreeNode> deque = new ArrayDeque<>();
        deque.addLast(root);
        while (!deque.isEmpty()) {
            TreeNode poll = deque.pollFirst();
            builder.append(poll.val).append(",");
            if (!poll.equals(empty)) {
                // 节点不为空时，添加左右节点
                TreeNode left = poll.left;
                if (left == null) {
                    left = empty;
                }
                TreeNode right = poll.right;
                if (right == null) {
                    right = empty;
                }
                deque.addLast(left);
                deque.addLast(right);
            }
        }
        return builder.toString();
    }

    // Decodes your encoded data to tree.
    public TreeNode deserialize(String data) {
        if (data.isEmpty()) return null;
        String[] split = data.split(",");
        int n = split.length;
        TreeNode root = new TreeNode(Integer.parseInt(split[0]));
        Deque<TreeNode> deque = new ArrayDeque<>();
        deque.addLast(root);
        for (int i = 1; i < n; i += 2) {
            // 取出root节点
            TreeNode first = deque.pollFirst();
            int left = Integer.parseInt(split[i]);
            int right = Integer.parseInt(split[i + 1]);
            if (left != Integer.MIN_VALUE) {
                // 左子节点不为空
                first.left = new TreeNode(left);
                deque.addLast(first.left);
            }
            if (right!=Integer.MIN_VALUE){
                // 右子节点不为空
                first.right = new TreeNode(right);
                deque.addLast(first.right);
            }
        }
        return root;
    }
}


```