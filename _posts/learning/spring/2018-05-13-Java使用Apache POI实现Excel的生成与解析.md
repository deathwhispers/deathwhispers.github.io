---
layout: post
title: Java使用Apache POI实现Excel的生成与解析
author: deathwhispers
date: 2018-05-13
slug: java-poi-excel-generation-parsing
categories:
- Spring
tags:
- Java
- Spring
type: note
week: 2018-W20
description: 本笔记介绍了如何使用 Apache POI 库在 Java 中快速生成和解析 Excel（.xls）文件，包含创建工作簿、工作表、单元格以及读取数据的核心代码示例。
keywords: Java, Apache POI, Excel, HSSFWorkbook, XSSFWorkbook, Excel导出, Excel解析
---

Apache POI 是一个非常流行的 Java 库，专门用于处理 Microsoft Office 格式的文件，尤其是 Excel。本笔记将通过简单的代码示例，展示如何使用 POI 快速生成和解析一个 Excel 文件。

## 1. 添加 Maven 依赖

要使用 Apache POI，首先需要在 `pom.xml` 文件中添加相应的依赖。

```xml
<!-- 用于处理 .xls 格式 (Excel 97-2003) -->
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.3</version> <!-- 建议使用最新稳定版 -->
</dependency>

<!-- 用于处理 .xlsx 格式 (Excel 2007+) -->
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.3</version>
</dependency>
```

> **注意**
> *   `poi` 模块提供了 `HSSFWorkbook` 类，用于操作 `.xls` 文件。
> *   `poi-ooxml` 模块提供了 `XSSFWorkbook` 类，用于操作 `.xlsx` 文件。

## 2. 生成 Excel 文件

以下代码演示了如何创建一个包含表头和一行数据的 `.xls` 文件。

```java
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.*;
import java.io.FileOutputStream;
import java.io.IOException;

public class ExcelGenerator
{

    public static void generateExcel()
    {
        // 1. 创建一个新的工作簿 (Workbook)，HSSFWorkbook 对应 .xls 文件
        try (Workbook wb = new HSSFWorkbook();
        FileOutputStream fileOut = new FileOutputStream("D:\\tmp\\workbook.xls"))
        {

            // 2. 在工作簿中创建一个新的工作表 (Sheet)
            Sheet sheet = wb.createSheet("用户信息");

            // 3. 创建表头行 (Row)
            Row headerRow = sheet.createRow(0);

            // 4. 创建单元格 (Cell) 并设置表头值
            headerRow.createCell(0).setCellValue("姓名");
            headerRow.createCell(1).setCellValue("年龄");
            headerRow.createCell(2).setCellValue("手机");

            // 5. 创建数据行并填充数据
            Row dataRow = sheet.createRow(1);
            dataRow.createCell(0).setCellValue("张三");
            dataRow.createCell(1).setCellValue(18); // POI 会自动处理数字类型
            dataRow.createCell(2).setCellValue("18888888888");

            // 6. 将工作簿内容写入文件
            wb.write(fileOut);

            System.out.println("Excel 文件生成成功！");

        } catch (IOException e) {
            // 在实际项目中，应使用日志库记录异常，而不是简单地忽略
            e.printStackTrace();
        }
    }
}



```

## 3. 解析 Excel 文件

以下代码演示了如何读取刚刚生成的 Excel 文件并打印其内容。

```java
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.*;
import java.io.FileInputStream;
import java.io.IOException;

public class ExcelParser
{

    public static void parseExcel()
    {
        // 1. 使用 FileInputStream 加载 Excel 文件
        try (FileInputStream fileIn = new FileInputStream("D:\\tmp\\workbook.xls");
        Workbook wb = new HSSFWorkbook(fileIn))
        {

            // 2. 获取第一个工作表
            Sheet sheet = wb.getSheetAt(0);

            // 3. 遍历工作表的每一行 (通常跳过表头，所以从 i = 1 开始)
            // getLastRowNum() 返回最后一行的索引 (从0开始)
            for (int i = 1;
            i <= sheet.getLastRowNum();
            i++)
            {
                Row row = sheet.getRow(i);
                if (row == null) continue; // 避免空行导致 NullPointerException

                // 4. 读取每个单元格的内容
                String name = row.getCell(0).getStringCellValue();
                // 数字类型建议使用 getNumericCellValue()，避免类型转换异常
                double age = row.getCell(1).getNumericCellValue();
                // 如果手机号是纯数字，Excel 可能将其存为数字格式，需要做相应处理
                row.getCell(2).setCellType(CellType.STRING);
                String phone = row.getCell(2).getStringCellValue();

                System.out.println("姓名：" + name + "，年龄：" + (int)age + "，手机：" + phone);
            }

        } catch (IOException e) {
            // 在实际项目中，应使用日志库记录异常
            e.printStackTrace();
        }
    }
}



```

> **提示**
> *   **处理 `.xlsx` 文件**：只需将代码中的 `HSSFWorkbook` 全部替换为 `XSSFWorkbook` 即可。
> *   **Web 应用集成**：在 Spring 等 Web 框架中，通常会将文件流写入 `HttpServletResponse` 的 `getOutputStream()`，从而实现文件下载功能，而不是直接写入服务器的本地磁盘。
> *   **资源管理**：始终使用 `try-with-resources` 语句或在 `finally` 块中确保关闭所有的 I/O 流，以防止资源泄漏。
