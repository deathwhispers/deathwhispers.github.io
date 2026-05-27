---
layout: post
title: Spring @Value 注入 map 和 list
slug: spring-value-inject-map-list
type:
- note
date: 2019-02-28
week: 2019-W09
status: draft
tags:
- Spring
- SpringBoot
author: deathwhispers
created: 2019-02-28 09:57
updated: 2019-02-28 09:57
categories:
- Learning
- Spring
---

**EL表达式+JSON写法**

```java
@Value("#{'${scio.cloud.list}'.split(',')}")private List<String> list;@Value("#{${scio.cloud.maps}}")
private Map<String,String> maps;
```

yml文件

```yaml
scio.cloud.list: topic1,topic2,topic3scio.cloud.maps: "{key1: 'value1', key2: 'value2'}"
```

---

- *

**

**yml常规写法**

配置类

```java
@EnableConfigurationProperties@Configuration@ConfigurationProperties(prefix = "scio.cloud")publci class ScioCloudConfig{    private List<String> list;    private Map<String,String> maps;    public void setList(List<String> list){        this.list = list;    }    public void setMaps(Map<String,String> maps){        this.maps = maps;    }}
```

yml常规

```yaml
scio:  cloud    list:      - topic1      - topic2      - topic3scio:  cloud:    maps:      key1: 'value1'      key2: 'value2'
```
