---
layout: post
title: IntelliJ IDEA 如何重构源代码
slug: intellij-idea-refactoring-source-code
type:
- note
status: published
date: 2019-08-13
tags:
- Tooling
author: deathwhispers
categories:
- Other
- General
---

IntelliJ IDEA 提供了各种各样的代码重构，它们可以自动跟踪和更正受影响的代码引用。

要执行重构，请按照以下一般步骤操作：

1. 选择（或悬停在插入符号上）符号或代码片段以重构。可用重构的集合取决于您的选择。您可以在以下 IntelliJ IDEA 组件中选择符号：
    - 项目视图
    - 结构工具窗口
    - 编辑
    - UML 类图
2. 执行以下操作之一：
    - 在主 Refactor（重构）菜单或选择的上下文菜单上，选择所需的重构或按相应的键盘快捷键（如果有）。
    - 在主菜单上选择：重构| 重构此选项，或按 Ctrl+Shift+Alt+T，然后从弹出窗口中选择所需的重构。
3. 在打开的对话框中，指定重构选项。
4. 要立即应用更改，具体取决于重构类型，单击 “重构” 或 “确定”。
5. 对于某些重构，有一个可以在实际执行重构之前预览更改的选项。在这种情况下， “预览” 按钮在相应的对话框中可用。
要预览潜在的更改并进行必要的调整，请单击“预览”。IntelliJ IDEA 显示将在 “查找工具” 窗口的专用选项卡上进行的更改。
此步骤中的一个可能的操作是从重构中排除某些项。为此，请在列表中选择所需的条目，然后按 Delete。
如果在重构后预期出现冲突，IntelliJ IDEA 将显示一个对话框，并简要介绍遇到的问题。如果是这种情况，请执行以下操作之一：
    - 单击 “继续” 按钮可忽略冲突，重构将被执行，但这可能会导致错误的结果。
    - 通过单击 “在视图中显示” 按钮预览冲突。IntelliJ IDEA 显示 “查找工具” 窗口中 “冲突” 选项卡上的所有冲突条目，使您能够导航到有问题的代码行并进行必要的修复。
    - 取消重构并返回编辑器。
6. 当您对建议的结果感到满意时，单击 “执行重构” 以应用更改。

[https://www.w3cschool.cn/intellij_idea_doc/intellij_idea_doc-gu4l2fjc.html](https://www.w3cschool.cn/intellij_idea_doc/intellij_idea_doc-gu4l2fjc.html)
