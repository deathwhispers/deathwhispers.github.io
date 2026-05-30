---
layout: post
title: 删除一个StringBuilder的最后一个字符
author: deathwhispers
date: 2018-07-25
slug: delete-last-character-of-stringbuilder
categories:
- Java
tags:
- Java
type: note
status: draft
created: 2018-07-25 22:07
updated: 2018-07-25 22:07
week: 2025-W48
---

When you have to loop through a [collection](https://so.csdn.net/so/search?q=collection&spm=1001.2101.3001.7020) and make a string of each data separated by a delimiter, you always end up with an extra delimiter at the end, e.g.

```java
for (String serverId : serverIds) {
    sb.append(serverId);
    sb.append(",");
}
```

Gives something like : serverId_1, serverId_2, serverId_3,

I would like to delete the last character in the StringBuilder (without converting it because I still need it after this loop).

Others have pointed out the deleteCharAt method, but here’s another alternative approach:

```java
String prefix = "";
for (String serverId : serverIds) {
    sb.append(prefix);
    prefix = ",";
    sb.append(serverId);
}
```

Alternatively, use the Joiner class from Guava :)

As of Java 8, StringJoiner is part of the standard JRE.

Another simple solution is:

```plain text
sb.setLength(sb.length() - 1);
```

A more complicated solution:

The above solution assumes that sb.length() > 0 … i.e. there is a “last character” to remove. If you can’t make that assumption, and/or you can’t deal with the exception that would ensue if the assumption is incorrect, then check the StringBuilder’s length first; e.g.

```java
// Readable version
if (sb.length() > 0) {
    sb.setLength(sb.length() - 1);
}
```

or

```java
// Concise but harder-to-read version of the above
sb.setLength(Math.max(sb.length() - 1, 0));
```

```java
sb.deleteCharAt(sb.length()-1)
```

In this case,

```java
sb.setLength(sb.length() - 1);
```

is preferable as it just assign the last value to ‘\0’ whereas deleting last character does System.arraycopy

As of Java 8, there’s a new StringJoiner class built in.

```java
StringJoiner sj = new StringJoiner(", ");
for (String serverId : serverIds) {
    sj.add(serverId);
}
```

2016年09月25日25分09秒

Another alternative

```java
for (String serverId : serverIds) {
    sb.append(",");
    sb.append(serverId);
}
sb.deleteCharAt(0);
```

Alternatively,

```java
StringBuilder result = new StringBuilder();
for (String string : collection) {
    result.append(string);
    result.append(",");
}
return result.substring(0, result.length() - 1);
```

```java
StringBuilder sb = new StringBuilder();
sb.append("abcdef");
sb.deleteCharAt(sb.length() - 1);
assertEquals("abcde", sb.toString());  // true
```

Just get the position of the last character occurrence.

```java
for (String serverId : serverIds) {
    sb.append(serverId);
    sb.append(",");
}
sb.deleteCharAt(sb.lastIndexOf(","));
```

Since lastIndexOf will perform a reverse search, and you know that it will find at the first try, performance won’t be an issue here.

Yet another alternative:

```java
public String join(Collection<String> collection, String seperator) {;
if (collection.isEmpty()) return "";

Iterator<String> iter = collection.iterator();
StringBuilder sb = new StringBuilder(iter.next());

while (iter.hasNext()) {
    sb.append(seperator);
    sb.append(iter.next());
}
return sb.toString();
}


```

I am doing something like this:

```java
StringBuilder stringBuilder = new StringBuilder();
for (int i = 0;
i < value.length;
i++) {
    stringBuilder.append(values[i]);
    if (i < value.length - 1) {
        stringBuilder.append(", ");
    }
}

```

With Java-8 you can use static method of String class,

String#join(CharSequence delimiter,Iterable

```java
public class Test {
    public static void main(String[] args) {;
    List<String> names = new ArrayList<>();
    names.add("James");
    names.add("Harry");
    names.add("Roy");
    System.out.println(String.join(",", names));
}
}

```

OUTPUT

```plain text
James,Harry,Roy
```

To avoid reinit(affect performance) of prefix use TextUtils.isEmpty:

```java
String prefix = "";
for (String item : list) {
    sb.append(prefix);
    if (TextUtils.isEmpty(prefix))
    prefix = ",";
    sb.append(item);
}

```

Yet another solution similar to the “prefix” solution above avoids multiple prefix assignments in the loop. i.e. Just in case the optimizer does not unroll the first loop iteration.

```java
StringBuilder sb = new StringBuilder();
boolean firstEntry = true;

for (String serverId : serverIds) {
    if (firstEntry)
    firstEntry = false;
    else
    sb.append(",");
    sb.append(serverId);
}

```

You can use:

```java
string finalString=sb.Remove(sb.Length - 1, 1).ToString();
```
