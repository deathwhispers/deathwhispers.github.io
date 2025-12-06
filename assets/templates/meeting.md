---
Title: 会议：{{title}}
Type:
  - Meeting
meeting-time: <% tp.date.now("YYYY-MM-DD HH:mm") %>
duration: 60
status: processed
tags:
  - meeting
host:
participants: []
project-name:
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
updated: <% tp.file.last_modified_date("YYYY-MM-DD HH:mm") %>
---

# 会议 · {{title}}

时间：{{date}} {{meeting_time}}（{{duration}}分钟）  
项目：{{project_code}}  
参会人：{{participants}}

## 会议目标

## 关键讨论

## 决策事项

## 行动项
{{action_items}}

## 附件/录音