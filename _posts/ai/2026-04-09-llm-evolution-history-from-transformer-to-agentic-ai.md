---
layout: post
title: LLM 发展历程：从 Transformer 到 Agent 化时代
author: deathwhispers
date: 2026-04-09
slug: llm-evolution-history-from-transformer-to-agentic-ai
categories:
- AI
- General
tags:
- AI
- LLM
status: published
---

这几年，LLM（大语言模型）几乎重塑了 AI 应用形态。

但如果只看近两年的爆发，很容易误以为 LLM 是"突然出现的新物种"。实际上，它是自然语言处理（NLP）几十年技术累积后的一次集中跃迁。

本文按时间线梳理 LLM 的关键发展阶段，帮助你快速建立一张完整的技术地图。

## 一、在 LLM 之前：NLP 的"特征工程时代"

在 2010 年代中期之前，NLP 的主流范式大致是：

1. 人工设计特征（词袋、n-gram、规则模板）。
2. 训练传统模型（SVM、CRF、朴素贝叶斯等）。
3. 为不同任务单独建模。

这一阶段的瓶颈很明显：

- 模型对上下文理解浅。
- 泛化能力差，迁移成本高。
- 新任务通常要从头设计特征。

## 二、2013-2017：深度学习打地基

这几年是"从离散特征到连续表示"的关键过渡期。

### 1. 词向量与分布式表示

Word2Vec、GloVe 等方法让"词"变成稠密向量，开启了语义表示学习。

### 2. 序列模型兴起

RNN、LSTM、GRU 成为主力，Seq2Seq 在机器翻译等任务中取得突破。

### 3. Attention 机制与 Transformer

2017 年，Transformer 提出后，NLP 的核心架构开始从"循环网络"转向"自注意力网络"。

这是 LLM 时代真正的起点，因为它提供了：

- 更好的并行训练能力。
- 更强的长程依赖建模。
- 可扩展到更大数据和更大参数量的架构基础。

## 三、2018-2020：预训练大模型范式确立

这一阶段最重要的变化是：

**先在海量文本上做通用预训练，再面向具体任务微调（Pretrain + Finetune）。**

典型里程碑：

- 2018：ELMo、BERT、GPT-1
- 2019：GPT-2
- 2020：T5、GPT-3

这几年的核心成果不是某个单点任务 SOTA，而是范式迁移：

- 模型从"任务特定模型"走向"通用语言基座"。
- 参数规模、数据规模、算力规模共同驱动性能提升。
- Scaling Law 思想开始成为行业共识。

## 四、2021-2022：从"会补全"到"会对话"

如果说 2018-2020 奠定了"能力上限"，那 2021-2022 解决的是"可用性问题"。

关键变化：

1. Instruction Tuning：模型更会"听指令"。
2. RLHF：输出更贴近人类偏好与安全要求。
3. Prompt Engineering 与 CoT 推理技巧被系统化。

2022 年 11 月，ChatGPT 的发布让 LLM 从研究圈走向大众与产业，成为历史拐点。

## 五、2023：开源生态与应用框架爆发

2023 年可以称为 LLM 工程化元年。

### 1. 开源模型与社区加速

LLaMA 系列带动开源社区快速追赶，模型训练、微调、部署门槛持续下降。

### 2. RAG 成为企业落地主线

企业普遍采用"LLM + 检索增强生成（RAG）"路线，缓解幻觉与知识时效问题。

### 3. 工具化与平台化

Function Calling、工作流编排、向量数据库、模型网关、评测平台逐渐标准化。

## 六、2024-2026：多模态、推理强化与 Agent 化

进入 2024 年后，LLM 进入"能力融合期"，几个趋势非常明显：

### 1. 多模态成为默认能力

文本、图像、音频、视频逐步在同一模型或同一系统内协同。

### 2. 推理能力与长上下文持续增强

模型不再只追求"流畅回答"，而是更强调复杂任务中的分解、规划与验证。

### 3. Agent 化成为应用主战场

系统目标从"问答助手"升级为"可执行任务的智能体"：

- 能调用工具（Function Call / MCP）
- 能分工协作（Subagent）
- 能流程编排（Workflow）
- 能持续评测（Harness / Evals）

换句话说，LLM 正从"模型能力竞争"走向"系统能力竞争"。

## 七、一张时间线速览

| 阶段 | 时间 | 关键关键词 | 本质变化 |
| --- | --- | --- | --- |
| 特征工程时代 | ~2016 | n-gram、SVM、CRF | 任务特定，迁移困难 |
| 深度学习过渡期 | 2013-2017 | Word2Vec、LSTM、Attention、Transformer | 表示学习与架构革新 |
| 预训练范式确立 | 2018-2020 | BERT、GPT-2/3、T5、Scaling Law | 通用语言基座形成 |
| 指令与对齐阶段 | 2021-2022 | Instruction Tuning、RLHF、ChatGPT | 可用性大幅提升 |
| 工程化爆发 | 2023 | 开源模型、RAG、工具链 | 应用落地与平台化 |
| 系统能力竞争 | 2024-2026 | 多模态、推理、Agent、MCP | 从"会说"到"会做" |

## 八、为什么说 LLM 还在早期？

虽然 LLM 已经非常强，但工程上仍有明显挑战：

- 事实可靠性与可验证性。
- 成本、延迟与稳定性平衡。
- 安全、合规与可控性。
- 评测体系与真实业务指标对齐。

这也是为什么今天的重点不再是"只换更大模型"，而是"构建更完整的 AI 系统工程"。

## 九、对开发者的启示

如果你准备长期投入这个方向，建议把能力结构拆成三层：

1. 模型层：Transformer、预训练、微调、对齐。
2. 系统层：RAG、工具调用、Workflow、Agent。
3. 工程层：评测、观测、守护、成本优化。

真正有竞争力的团队，往往不是只懂模型，而是能把三层打通。

## 十、总结

LLM 发展历程可以概括为三句话：

1. 从"人工特征"走向"端到端表示学习"。
2. 从"任务模型"走向"通用基础模型"。
3. 从"会生成文本"走向"能完成任务的智能系统"。

接下来几年，行业竞争焦点大概率会继续从"参数规模"转向"系统闭环能力"：谁能更稳定、更低成本、更可控地交付业务价值，谁就更有优势。

## 参考资料

1. Vaswani et al., *Attention Is All You Need* (2017)
   [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
2. Devlin et al., *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding* (2018)
   [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)
3. Brown et al., *Language Models are Few-Shot Learners (GPT-3)* (2020)
   [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
4. Kaplan et al., *Scaling Laws for Neural Language Models* (2020)
   [https://arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361)
5. Ouyang et al., *Training language models to follow instructions with human feedback (InstructGPT)* (2022)
   [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)
6. OpenAI, *Introducing ChatGPT* (2022-11-30)
   [https://openai.com/index/chatgpt/](https://openai.com/index/chatgpt/)
7. Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (2020)
   [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
