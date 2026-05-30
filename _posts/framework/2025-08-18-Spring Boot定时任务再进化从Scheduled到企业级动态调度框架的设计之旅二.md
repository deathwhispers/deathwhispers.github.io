---
layout: post
title: Spring Boot定时任务再进化：从@Scheduled到企业级动态调度框架的设计之旅（二）
slug: from-scheduled-to-enterprise-level-dynamic-scheduling-framework-design-tour-2
date: 2025-08-18
tags:
- Spring
categories:
- Framework
- Backend
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---

## 引言

> 上一章咱们把`@Scheduled`在复杂业务里的“四个坑”都数了一遍。既然发现了问题，咱做开发的，本能就是想解决它。面对这么个“黑盒”，最直接的想法就是：**“既然管不了它本身，那咱就造个‘遥控器’，用遥控器来管它！”** 这思路听着特合理，所以我第一次尝试就照着这个来。

> 这一章，咱就好好复盘下：这个一开始看着挺完美的方案，是怎么从一张设计图，变成一堵跨不过去的“墙”的。咱们还会扒一扒Spring Bean的生命周期，用一张图让大家看明白——那个经典的“魔鬼”（循环依赖），是怎么把一个挺有希望的设计，直接拖进死胡同的。

## 最初的蓝图：搞个中心化的`TaskManager`

我第一个想法特别简单：弄个叫`TaskManager`的“总指挥”。所有定时任务都归它管，不管是任务注册、存起来，还是启动、停止，全由它负责。

这个`TaskManager`的核心活儿就这么几件：

1.  **任务注册**：应用启动后，自动扫所有带咱们自定义注解（咱叫它`@EnhanceScheduled`）的方法，把这些方法包装成能管的任务对象（`ManagedTask`）。
2.  **运行时存任务**：内部搞个线程安全的`Map`（比如`ConcurrentHashMap`），key是任务的唯一ID，value就是对应的`ManagedTask`实例。
3.  **控制生命周期**：对外提供`start(taskId)`、`stop(taskId)`、`triggerOnce(taskId)`这些方法，通过操作Spring底层的`ThreadPoolTaskScheduler`，精准控制任务。

1.  **`EnhanceScheduled`注解**：它就是`@Scheduled`的“加强版”，除了保留`cron`这些原生属性，还加了`id`、`description`这些方便管理的信息。
2.  **Bean扫描器**：要么实现Spring的`ApplicationRunner`，要么用`@PostConstruct`注解，等所有Bean都初始化完了，就去扫容器里带`@EnhanceScheduled`注解的方法。
3.  **TaskManager**：作为核心管理器，它得把Spring Boot自动配好的`ThreadPoolTaskScheduler`注进来。扫描器一发现任务，就调用`TaskManager.register()`方法。`TaskManager`会创建`ManagedTask`实例，用注进来的`scheduler`调度任务，还会把返回的`ScheduledFuture`句柄存在`ManagedTask`里，方便后面取消任务。
4.  **Controller**：提供RESTful接口，接收外面的管理指令，再调用`TaskManager`对应的方法。

这方案逻辑上能自圆其说，所有任务都归到一个地方管。于是我信心满满地开始把这张图写成代码。

## 迎头撞墙：循环依赖的“幽灵”冒出来了

等我开始写代码，想把这些组件在Spring容器里拼起来的时候，问题来了——还是个特别经典、特别棘手的问题：**循环依赖**。

想搞懂这问题的根源，得先简单唠唠Spring的调度体系是怎么初始化的。如果应用里开了`@EnableScheduling`，大致流程是这样的：

Spring Boot会先创建`ThreadPoolTaskScheduler`这个Bean。然后有个叫`ScheduledAnnotationBeanPostProcessor`的后置处理器，会去扫所有Bean，找出带`@Scheduled`的方法，把这些方法注册到`ScheduledTaskRegistrar`（注册器）里。最后等所有Bean都初始化完，这些注册好的任务才会交给`TaskScheduler`去执行。

现在，咱们把我设计的`TaskManager`塞到这个流程里，看看会出啥幺蛾子。

我的`TaskManager`要控制任务调度，所以它**必须依赖**`ThreadPoolTaskScheduler`。

```java
// TaskManagerImpl.java (第一版设想)
public class TaskManagerImpl implements TaskManager
{
    private final ThreadPoolTaskScheduler taskScheduler;

    // 构造器里注入taskScheduler
    public TaskManagerImpl(ThreadPoolTaskScheduler taskScheduler)
    {
        this.taskScheduler = taskScheduler;
    }
// ... 其他方法
}

```

但我的目标是接管所有`@Scheduled`任务啊！上一章咱也分析过，我不想自己写复杂的Bean扫描逻辑，最省事的就是用Spring自己扫出来的结果。而能拿到这个结果的，就是前面提过的`SchedulingConfigurer`接口。

所以我自然而然就想：让我写的`HadokenSchedulerConfigurer`依赖`TaskManager`。在`configureTasks`方法里，从`taskRegistrar`拿到Spring扫到的任务，再转手交给`TaskManager`处理。

```java
// HadokenSchedulerConfigurer.java (第一版设想)
public class HadokenSchedulerConfigurer implements SchedulingConfigurer
{
    private final TaskManager taskManager;

    // 构造器里注入TaskManager
    public HadokenSchedulerConfigurer(TaskManager taskManager)
    {
        this.taskManager = taskManager;
    }

@Override
public void configureTasks(ScheduledTaskRegistrar taskRegistrar)
{
    // 拿到Spring扫好的任务，交给taskManager处理...
}
}

```

现在把这些依赖关系串起来，那个藏着的“幽灵”就现身了：

咱们来掰扯下这里的逻辑：

1. Spring容器要创建`TaskManager`这个Bean。
2. 创建`TaskManager`的时候，发现它依赖`ThreadPoolTaskScheduler`。于是Spring说：“行，那我先去创建`ThreadPoolTaskScheduler`。”
3. `ThreadPoolTaskScheduler`创建本身没问题，但别忘了，Spring的调度体系还需要`SchedulingConfigurer`来完成最后的配置。
4. 所以Spring接着去创建`HadokenSchedulerConfigurer`这个Bean。
5. 创建`HadokenSchedulerConfigurer`的时候，又发现它依赖`TaskManager`。
6. 这时候Spring就卡壳了，陷入一个死循环：
    * “我要创建`TaskManager`，得先有`TaskScheduler`；但`TaskScheduler`要配置好，得先有`Configurer`。”
    * “可创建`Configurer`，又得先有`TaskManager`。”
    * “……所以，为了造`TaskManager`，我得先有个已经造好的`TaskManager`？”

Spring容器直接抛出`BeanCurrentlyInCreationException`异常，宣告这套设计凉了。这就是典型的“构造器注入循环依赖”——Spring也没法解决这问题。

## 第二个“陷阱”：改不了的注册器

就算咱暂时不管循环依赖，假设能用点技巧（比如加`@Lazy`注解）绕过去，这方案还有第二个坑等着。

我本来计划在`configureTasks`方法里，对`taskRegistrar`里的任务“偷梁换柱”——把原生的`Runnable`换成咱自己包装的、带监控和控制逻辑的`Runnable`。

可等我试着操作`taskRegistrar.getTriggerTaskList()`返回的列表时，发现这列表是**不可修改的**（Unmodifiable Collection）。Spring在这做了保护：它把扫描结果给你，是让你“看”或者“加新任务”，不是让你“改”它已经找好的东西。

这就意味着，咱没法在Spring的体系里，对已经扫出来的任务“原地改造”。我想在下游改已经成型的东西，但Spring根本不给这个机会。

## 结语

我第一次尝试，从一个清晰的思路开始，最后却一头撞上两堵“硬墙”。**循环依赖**暴露了我对Spring Bean生命周期的理解不够深；**改不了的注册器**则说明，我想改造框架的时机和位置都错了。

这次“推倒重来”虽然失败了，但价值真不小。它让我彻底明白：**想扩展一个成熟的框架，千万别用“外部控制”的思路硬扭它的流程。反而得像个“内部插件”一样，找框架预留的扩展点，在它设计好的生命周期里，找个最合适的位置，优雅地把咱的逻辑嵌进去。**

这次失败，也让我的思路从“怎么管已经存在的任务”，转变成“怎么参与任务的创建过程”。也正是这个转变，让我最后发现了`SchedulingConfigurer`接口真正的威力——它不是个简单的配置回调，而是咱掌控Spring调度的“关键入口”。

这一章把第一次改造的踩坑经历讲得比较细致，下一章可以继续聊怎么利用`SchedulingConfigurer`破局，或者你希望重点突出某个技术点（比如Bean生命周期细节、扩展点实战），都可以跟我说，我调整内容侧重点。
