---
layout: post
title: "NLP自然语言处理"
date: 2025-05-13
tags: [学习资源, NLP, 自然语言处理]
comments: true
author: deathwhispers
---


[toc]
# NLP自然语言处理

## Transformer库与优化

* [huggingface/transformers](https://github.com/huggingface/transformers) 支持Pytorch、TensorFlow和JAX的最先进的机器学习Transformers库。提供了数以千计的预训练模型，支持100多种语言的文本分类、信息抽取、问答、摘要、翻译、文本生成。它的宗旨让最先进的 NLP 技术人人易用。

* [jadore801120/attention-is-all-you-need-pytorch](https://github.com/jadore801120/attention-is-all-you-need-pytorch) PyTorch 实现的Transformer模型在“注意力就是你所需要的一切”。

* [adapter-hub/adapter-transformers](https://github.com/adapter-hub/adapter-transformers) HuggingFace 的 Transformers 的友好分支，将适配器添加到 PyTorch 语言模型。可用作 HuggingFace 的直接替代品，并定期同步新的上游更改。

* [microsoft/DeBERTa](https://github.com/microsoft/DeBERTa) 注意力分散的增强解码的BERT，使用了BERT和RoBERTa模型，显着提高了预训练的效率和下游任务的性能。

* [pytorch/fairseq](https://github.com/pytorch/fairseq) Python的Facebook AI Research Sequence-to-Sequence包。

* [ml-jku/hopfield-layers](https://github.com/ml-jku/hopfield-layers) NLP 领域里大热的 Transformer，其网络更新规则其实是和 Hopfield 网络在连续状态下是相同的。Transformer 中的这种注意力机制其实等价于扩展到连续状态的 modern Hopfield 网络中的更新规则。作者来自奥地利林茨大学、挪威奥斯陆大学，与 Jürgen Schmidhuber 合著 LSTM 的 Sepp Hochreiter 也是作者之一。

* [laiguokun/Funnel-Transformer](https://github.com/laiguokun/Funnel-Transformer) Transformer优化，一种新的自我注意模型，可以将隐藏状态的序列逐渐压缩为较短的状态，从而降低了计算成本。

* [mit-han-lab/hardware-aware-transformers](https://github.com/mit-han-lab/hardware-aware-transformers) 用于高效自然语言处理的硬件感知型Transformers.实现高达3倍的加速和3.7倍的较小模型尺寸，不会降低性能。

* [mit-han-lab/lite-transformer](https://github.com/mit-han-lab/lite-transformer) 具有长距离短距离注意的Lite transformer

* [allenai/longformer](https://github.com/allenai/longformer) 用于长文档的类似BERT的模型

* [Tencent/TurboTransformers](https://github.com/Tencent/TurboTransformers) 在 CPU 和 GPU 上进行Transformer推断的快速且用户友好的运行库。

* [idiap/fast-transformers](https://github.com/idiap/fast-transformers) Pytorch实现的快速Transformer库

* [bytedance/lightseq](https://github.com/bytedance/lightseq) 高效的序列处理与生成库，提供 Bert, GPT, Transformer，beam search, diverse beam search, topp/topk sampling

* [google-research/bigbird](https://github.com/google-research/bigbird) 基于稀疏注意力(随机注意力机制+局部注意力机制+全局注意力机制)的transformer，它将基于transformer的模型（例如 BERT）扩展到更长的序列。 由于能够处理更长的上下文，BigBird 极大地提高了各种 NLP 任务（例如问答和摘要）的性能。

* [lucidrains/performer-pytorch](https://github.com/lucidrains/performer-pytorch) 一个高效的线性广义注意力框架（generalized attention framework），允许基于不同相似性度量（核）的一类广泛的注意力机制。该框架通过谷歌的新算法 FAVOR+（Fast Attention Via Positive Orthogonal Random Features）来实现，后者能够提供注意力机制的可扩展低方差、无偏估计，这可以通过随机特征图分解（常规 softmax-attention）来表达。该方法在保持线性空间和时间复杂度的同时准确率也很有保证，也可以应用到独立的softmax运算。此外，还可以和可逆层等其他技术进行互操作。

* [microsoft/fastformers](https://github.com/microsoft/fastformers) 实现Transformers在CPU上223倍的推理加速 它能对基于Transformer的模型在各种NLU任务上实现高效的推理时间性能。论文FastFormers的作者表明，利用知识蒸馏、结构化剪枝和数值优化可以大幅提高推理效率。我们表明，这种改进可以达到200倍的加速，并在22倍的能耗下节省超过200倍的推理成本。

* [mit-han-lab/lite-transformer](https://github.com/mit-han-lab/lite-transformer) 轻量级Transformer，注意力长短搭配 长依赖和短依赖的剥离，并引入卷积来捕捉短依赖，总体思想和Transformer之自适应宽度注意力有点类似。文章中发现低层次上的注意力都比较短，层次越高，注意力的所关注的依赖越长。

* [ThilinaRajapakse/simpletransformers](https://github.com/ThilinaRajapakse/simpletransformers) 用于分类、NER、QA、语言建模、语言生成、T5、多模态和会话AI的transformer

* [cloneofsimo/RealFormer-pytorch](https://github.com/cloneofsimo/RealFormer-pytorch) 通过在Transformer架构上进行改造来提升BERT训练效果，具体为：使用attention残差机制改造Transformer。1、realformer在标签数量较少的分类任务上有一定的提升效果，提升的幅度与数据集和任务难度有关，一般越难的任务提升的幅度越大。2、realformer在标签数量达到一定的数值时，其效果便会大打折扣，在某些数据集上甚至会无法学习。

* [openai/sparse_attention](https://github.com/openai/sparse_attention) 稀疏Attention

* [sacmehta/delight](https://github.com/sacmehta/delight) 提出了一个更深更轻的Transformer，DeLighT，它的性能与Transformer相似，甚至更好，平均少了2到3倍的参数。

* [BSlience/transformer-all-in-one](https://github.com/BSlience/transformer-all-in-one) 记录了学习Transformer过程中的一些疑问和解答，并且实现Transformer的全过程。

* [mlpen/Nystromformer](https://github.com/mlpen/Nystromformer) 利用了 Nyström 方法来近似标准的Attention。

* [xuanqing94/FLOATER](https://github.com/xuanqing94/FLOATER) 基于连续动态系统学习更加灵活的位置编码

* [ELS-RD/transformer-deploy](https://github.com/ELS-RD/transformer-deploy) Hugging Face Transformer 亚毫秒推理和部署到生产环境

* [lucidrains/x-transformers](https://github.com/lucidrains/x-transformers) 一个简单但完整的全注意力转换器，具有来自各种论文的一组有希望的实验特征 Full encoder / decoder 、Decoder-only (GPT-like) 、Encoder-only (BERT-like) 、Image -> caption 。

* [lucidrains/FLASH-pytorch](https://github.com/lucidrains/FLASH-pytorch) 线性时间的Transformer变体

* [NVIDIA/FasterTransformer](https://github.com/NVIDIA/FasterTransformer) Transformer相关优化，包括BERT、GPT 。提供了一个脚本和配方来运行高度优化的基于转换器的编码器和解码器组件，它由 NVIDIA 测试和维护。可以带来性能加速。

* [HazyResearch/flash-attention](https://github.com/HazyResearch/flash-attention) 快速且节省内存的精确注意力

* [NetEase-FuXi/EET](https://github.com/NetEase-FuXi/EET) 针对Transformer-based大模型和长序列场景的高性能pytorch推理插件。高性能：设计高度优化的CUDA内核。灵活：提供包括op api、model api和pipelines应对不同需求。 使用： 几行代码即可完成。适配主流ai框架，包括fairseq和transformers。bert模型整体性能加速1.2x到7.x倍，gpt模型整体性能加速2.x到7.x倍。

* [NVIDIA/transformer-ls](https://github.com/NVIDIA/transformer-ls) 将原始 Transformer 的全部自注意力替换为考虑长期和短期相关性的有效注意力。每个查询都关注分段滑动窗口中的标记以捕获短期相关性，以及动态投影特征以捕获长期相关性。为了对齐原始特征、投影特征向量的范数并提高聚合的效率，使用两组层归一化对原始特征向量和投影特征向量进行归一化。

* [thuml/Flowformer](https://github.com/thuml/Flowformer) 任务通用的线性复杂度Transformer 。在图论中的经典网络流（Flow network）模型中，“守恒”（Conservation）是一个重要现象，即每个节点的流入量等于流出量。受到“固定资源情况下，必定引起竞争”的启发，通过网络流视角重新分析经典注意力机制中的信息流动，并通过守恒性质将竞争引入注意力机制设计，以避免平凡注意力问题。

* [alipay/Pyraformer](https://github.com/alipay/Pyraformer) 用于长期时间序列建模和预测的低复杂度金字塔注意。

* [NVIDIA/Megatron-LM](https://github.com/NVIDIA/Megatron-LM) 由 NVIDIA 的应用DL研究团队开发的大型、强大的transformer。开发了高效、模型并行（张量、序列和流水线）和多节点预训练，基于 Transformer 的模型（例如 GPT、BERT 和 T5）使用混合精度。

* [facebookresearch/bit](https://github.com/facebookresearch/bit) 鲁棒二值化多次蒸馏Transformer

* [Tongjilibo/bert4torch](https://github.com/Tongjilibo/bert4torch) 优雅的pytorch transformers库

## BERT优化

* [google-research/bert](https://github.com/google-research/bert) Bidirectional Encoder Representations from Transformers 来自Transformers的双向编码器表示法

* [google-research/ALBERT](https://github.com/google-research/ALBERT) 用于语言表达自我监督学习的Lite BERT

* [bojone/bert-of-theseus](https://github.com/bojone/bert-of-theseus) BERT 模型压缩方法 ,theseus(忒修斯之船 如果忒修斯的船上的木头被  逐渐替换，直到所有的木头都不是原来的木头，那这艘船还是原来的那艘船吗？),将原始大模型切分为多个大模块，固定大模型权重，训练时随机替换为小模块,充分训练后，将小模型继续微调。

* [brightmart/albert_zh](https://github.com/brightmart/albert_zh) 使用TensorFlow 进行自我监督学习语言表示的Lite Bert的实现预训练的汉语模型

* [bojone/bert4keras](https://github.com/bojone/bert4keras) 更清晰、更轻量级的keras版bert，提供丰富的应用例子。

* [huawei-noah/Pretrained-Language-Model](https://github.com/huawei-noah/Pretrained-Language-Model) 华为诺亚方舟实验室开发的预训练语言模型及其相关优化技术NEZHA是一种经过预训练的中文语言模型，可以在多项中文NLP任务上实现最先进的性能TinyBERT是一种压缩的BERT模型，推理时可缩小7.5倍，加快9.4倍

* [ymcui/MacBERT](https://github.com/ymcui/MacBERT) MacBERT是一种改进的BERT，具有新颖的M LM校正预训练任务，它减轻了预训练和微调的差异。我们建议使用类似的词来进行掩蔽，而不是使用在微调阶段从未出现过的 [MASK] 令牌进行掩蔽。通过使用基于 word2vec (Mikolov et al., 2013) 相似度计算的Synonyms 工具包 (Wang and Hu, 2017)获得相似词。如果选择 N-gram 进行掩码，我们将单独找到相似的单词。在极少数情况下，当没有相似词时，我们会降级为使用随机词替换。

* [Lisennlp/TinyBert](https://github.com/Lisennlp/TinyBert) 基于华为的TinyBert进行修改的，简化了数据读取的过程，方便我们利用自己的数据进行读取操作。

* [epfml/collaborative-attention](https://github.com/epfml/collaborative-attention) 整合多头注意力,任何经过预训练的注意力层重新配置为协作注意力层。

* [ZhuiyiTechnology/WoBERT](https://github.com/ZhuiyiTechnology/WoBERT) 以词为基本单位的中文BERT（Word-based BERT）

* [autoliuweijie/FastBERT](https://github.com/autoliuweijie/FastBERT) 具有自适应推断时间的自蒸馏BERT pip install fastbert

* [alexa/bort](https://github.com/alexa/bort) 论文 Optimal Subarchitecture Extraction for BERT. “ BERT的最佳子体系结构提取”的代码。Bort是用于BERT架构的最佳子集，它是通过对神经架构搜索应用完全多项式时间近似方案（FPTAS）提取的。 Bort的有效（即不计算嵌入层）大小是原始BERT大型体系结构的5.5％，是净大小的16％。它在CPU上也比基于BERT的速度快7.9倍，并且比体系结构的其他压缩变体和某些非压缩变体性能更好。与多个公共自然语言理解（NLU）基准上的BERT-large相比，它的平均性能提高了0.3％至31％。

* [valuesimplex/FinBERT](https://github.com/valuesimplex/FinBERT) 基于 BERT 架构的金融领域预训练语言模型

* [yitu-opensource/ConvBert](https://github.com/yitu-opensource/ConvBert) ConvBERT，通过全新的注意力模块，仅用 1/10 的训练时间和 1/6 的参数就获得了跟 BERT 模型一样的精度。依图研发团队从模型结构本身的冗余出发，提出了一种基于跨度的动态卷积操作，并基于此提出了 ConvBERT 模型。

* [wtma/CharBERT](https://github.com/wtma/CharBERT) 字符敏感的预训练语言模型 通过结合字符级别和词级别的信息实现了更为全面的输入编码，同时，结合 RNN 和 CNN 的优势，基本上 CNN，RNN，Transformer 都使用上了，体现了新老研究成果的结合在一定程度上能进一步提升方法的性能。

* [Sleepychord/CogLTX](https://github.com/Sleepychord/CogLTX) 将BERT应用于长文本CogLTX遵循一种特别简单直观的范式，即抽取关键的句子=>通过BERT得到答案的两步流程。

* [ShannonAI/service-streamer](https://github.com/ShannonAI/service-streamer) 服务流媒体BERT服务,每秒处理1400个句子的BERT服务.

* [Sleepychord/CogLTX](https://github.com/Sleepychord/CogLTX) 可将当前类似BERT的预训练语言模型应用于长文本。使用动态规划算法将长文本划分为文本块集合；使用MemRecall对原长句中的子句进行打分：从而选择出分数最高的子句组成 再进行训练，这样一来的话，COGLTX相当于使用了了两个bert，MemRecall中bert就是负责打分，另一个bert执行原本的NLP任务。

* [bojone/BERT-whitening](https://github.com/bojone/BERT-whitening) 简单的线性变换（白化）操作，就可以达到BERT-flow的效果。

* [thunlp/ERNIE](https://github.com/thunlp/ERNIE) 用知识图谱增强 BERT 的预训练效果

  * 1) 对于抽取并编码的知识信息，研究者首先识别文本中的命名实体，然后将这些提到的实体与知识图谱中的实体进行匹配。研究者并不直接使用 KG 中基于图的事实，相反他们通过知识嵌入算法（例如 TransE）编码 KG 的图结构，并将多信息实体嵌入作为 ERNIE 的输入。基于文本和知识图谱的对齐，ERNIE 将知识模块的实体表征整合到语义模块的隐藏层中。
  * 2) 与BERT类似，采用了带Mask的语言模型，以及预测下一句文本作为预训练目标。除此之外，为了更好地融合文本和知识特征，研究者设计了一种新型预训练目标，即随机 Mask 掉一些对

* [ShannonAI/ChineseBert](https://github.com/ShannonAI/ChineseBert) 融合字形与拼音信息的中文Bert预训练模型

* [alibaba/AliceMind/LatticeBERT](https://github.com/alibaba/AliceMind/tree/main/LatticeBERT) Leveraging Multi-Granularity Representations in Chinese Pre-trained Language Models 利用多粒度的词格信息（word lattice），相对字级别的模型取得了性能提升。

* [Langboat/Mengzi](https://github.com/Langboat/Mengzi) 孟子预训练模型 轻量级但更强大，对部署和工业落地更友好的模型。

* [huawei-noah/DynaBERT](https://github.com/huawei-noah/Pretrained-Language-Model/tree/master/DynaBERT) dynamic BERT 可以通过选择自适应宽度和深度来灵活地调整网络大小，从而得到一个尺寸可变的网络。首先通过知识蒸馏的方法将teacher BERT的知识迁移到有自适应宽度的子网络student  DynaBERTw中，然后再对DynaBERTw进行知识蒸馏得到同时支持深度自适应和宽度自适应的子网络DynaBERT。

* [microsoft/LoRA](https://github.com/microsoft/LoRA) 大型语言模型的低秩适应。 冻结原始权重的同时学习成对的秩分解矩阵来减少可训练参数的数量。降低了适用于特定任务的大型语言模型的存储需求，并在部署期间实现了高效的任务切换，所有这些都不会引入推理延迟。在 GLUE 基准上获得与完全微调相当或更好的结果，同时只训练和存储一小部分参数。

* [guillaume-be/rust-bert](https://github.com/guillaume-be/rust-bert)  Rust-native 最先进的自然语言处理模型和管道。 Hugging Face 的 Transformers 库的端口，使用 tch-rs crate 和 rust-tokenizers 预处理。 支持多线程标记化和GPU推理。 公开了模型基础架构、特定于任务的头和随时可用的管道。

* [volcengine/veGiantModel](https://github.com/volcengine/veGiantModel) 字节跳动应用ML团队的基于torch的高效训练库。 使巨型模型（例如GPT、BERT和T5）训练变得简单高效。 建立在 Megatron 和 DeepSpeed 之上，通过集成高效通信库BytePs并提供定制的管道分区来提高通信效率。

* [extreme-bert/extreme-bert](https://github.com/extreme-bert/extreme-bert)  可加速 BERT 在自定义数据集上的预训练和微调。

## 预训练模型

* [dbiir/UER-py](https://github.com/dbiir/UER-py) 一个用于对通用语料进行预训练并对下游任务进行微调的工具包。提供了非常丰富的模型库。包括：中文RoBERTa、基于词的中文RoBERTa、中文GPT-2预训练模型（通用、古诗词、对联、歌词、文言文）、中文T5预训练模型、中文RoBERTa下游任务微调模型（JD full 情感分类 、JD binary 情感分类 、Dianping 情感分类、Ifeng 新闻主题分类、Chinanews 新闻主题分类 、CLUENER2020 NER 、抽取式问答）等。

* [OpenBMB/BMInf](https://github.com/OpenBMB/BMInf) BMInf (Big Model Inference) 是一个用于大规模预训练语言模型（PLM）推理阶段的低资源工具包。最低支持在NVIDIA GTX 1060单卡运行百亿大模型。在此基础上，使用更好的gpu运行会有更好的性能。模型能力覆盖文本补全、文本生成与对话场景。文本生成能力大幅提高。目前支持下列模型：

  * **CPM2.1**. CPM2.1是CPM2 [[1](https://bminf.readthedocs.io/zh_CN/latest/introduction-zh.html#ref)] 的升级版本。拥有110亿参数的通用中文预训练语言模型。基于CPM2，CPM2.1新增了一个生成式的预训练任务并基于持续学习范式进行训练。CPM2.1比CPM2具有更好的生成能力。
  * **CPM1.** CPM1 [[2](https://bminf.readthedocs.io/zh_CN/latest/introduction-zh.html#ref)] 是拥有26亿参数的生成式中文预训练语言模型。CPM1的模型架构与GPT [[4](https://bminf.readthedocs.io/zh_CN/latest/introduction-zh.html#ref)] 类似，它能够被应用于广泛的自然语言处理任务，如对话、文章生成、完形填空和语言理解。
  * **EVA.** EVA [[3](https://bminf.readthedocs.io/zh_CN/latest/introduction-zh.html#ref)] 是有着28亿参数的中文预训练对话模型。EVA在很多对话任务上表现优异，尤其是在多轮人机交互对话任务上。

* [CyberZHG/keras-xlnet](https://github.com/CyberZHG/keras-xlnet) XLNet的非官方实现。

* [hwchase17/langchain](https://github.com/hwchase17/langchain)  通过可组合性使用大型语言模型构建应用程序  基于 OPENAI 的 GPT3 等大语言模型设计一系列便于集成到实际应用中的接口，降低了在实际场景中部署大语言模型的难度

* [IDEA-CCNL/Fengshenbang-LM](https://github.com/IDEA-CCNL/Fengshenbang-LM) Fengshenbang-LM(封神榜大模型)是IDEA研究院认知计算与自然语言研究中心主导的大模型开源体系，成为中文认知智能的基础设施。包括了自然语言理解(NLU)，自然语言生成(NLG)和自然语言转换(NLT)任务。CHID(成语填空)、TNEWS(新闻分类)超过人类，CHID(成语填空)、CSLDCP(学科文献分类)、OCNLI(自然语言推理)单任务第一，刷新小样本学习记录。

* [ymcui/Chinese-XLNet](https://github.com/ymcui/Chinese-XLNet) 面向中文的XLNet预训练模型

* [microsoft/unilm](https://github.com/microsoft/unilm) UniLM-NLP及更高版本的统一语言模型预训练

  * layoutlm 多模态文档理解预训练模型LayoutLM 2.0，模型首先将文本、图像、布局三种模态的输入转换成向量表示，然后再交给编码器网络，最终输出的表示向量可以供下游任务使用。下游任务：表单理解、票据理解、复杂布局长文档理解、文档图像分类、视觉问答。

* [YunwenTechnology/Unilm](https://github.com/YunwenTechnology/Unilm) UniLM模型既可以应用于自然语言理解（NLU）任务，又可以应用于自然语言生成（NLG）任务。论文来自微软研究院。模型虽然强大，但微软并没有开源中文的预训练模型。因此云问本着开源之前，将我们预训练好的中文unilm_base模型进行开源。

* [ymcui/Chinese-ELECTRA](https://github.com/ymcui/Chinese-ELECTRA) 中文ELECTRA预训练模型 其中ELECTRA-small模型可与BERT-base甚至其他同等规模的模型相媲美，而参数量仅为BERT-base的1/10

* [THUDM/GLM-130B](https://github.com/THUDM/GLM-130B) 开放的双语（英汉）双向密集模型，1300亿参数，使用通用语言模型（GLM）进行预训练。 支持单台A100（40G * 8）或V100（32G * 8）服务器上具有130B参数的推理任务。 通过 INT4 量化，降低到 4 * RTX 3090（24G），而性能几乎没有下降。 截至 2022 -7-3 ，已接受了超过 4000 亿个文本标记（中文和英文各 200B）的训练。

* [alibaba/EasyTransfer](https://github.com/alibaba/EasyTransfer) 自然语言处理的迁移学习工具。主要特性：预训练语言模型工具，丰富且高质量的预训练模型库 BERT, ALBERT, RoBERTa, T5, etc,丰富且易用的NLP应用 如文本匹配、分本分类、机器阅读理解MRC，自动化的知识蒸馏，易用且高效的分布式训练。

* [microsoft/unilm/layoutlm](https://github.com/microsoft/unilm/tree/master/layoutlm) 多模态预训练模型 LayoutLM 2.0，不仅考虑了文本和页面布局信息，还将图像信息融合到了多模态框架内。下游任务微调：表单理解 票据理解 复杂布局长文档理解 文档图像分类 视觉问答

* [google-research/byt5](https://github.com/google-research/byt5) ByT5：通过预先训练的字节到字节模型迈向无令牌的未来.ByT5 是 mT5 模型的无标记器扩展。 我们的 ByT5 模型不像大多数其他预训练语言模型（BERT、XLM-R、T5、GPT-3）那样使用子词词汇表，而是直接在 UTF-8 字节上运行，无需任何文本预处理。 除了降低系统复杂性之外，我们发现参数匹配的 ByT5 模型在一系列任务中与 mT5 具有竞争力，并且在涉及嘈杂文本或对拼写和发音敏感的任务上优于 mT5。 此 repo 可用于重现 ByT5 论文中的实验。

* [sunyilgdx/NSP-BERT](https://github.com/sunyilgdx/NSP-BERT) 利用**句子级别(sentence-level)** 的预训练任务 **NSP (下一句预测，Next Sentence Prediction)** 来实现不同的NLP下游任务, 例如 *单句分类(single sentence classification)*, *双句分类(sentence pair classification)*, *指代消解(coreference resolution)*, *完形填空(cloze-style task)*, *实体链接(entity linking)*, *实体类型识别(entity typing)*.

* [thunlp/OpenPrompt](https://github.com/thunlp/OpenPrompt) Prompt-learning 是将预训练语言模型应用于下游NLP任务的最新范式，它使用文本模板修改输入文本并直接使用 PLM 执行预训练任务。 该库提供了一个标准、灵活和可扩展的框架来部署即时学习管道。 OpenPrompt支持直接从Huggingface Transformer加载PLM。将来，我们还将支持其他库实现的 PLM。

* [google-research/flan](https://github.com/google-research/flan) 微调语言模型是零样本学习器

* [PaddlePaddle/ERNIE](https://github.com/PaddlePaddle/ERNIE) ERNIE 家族各种预训练模型的官方实现，涵盖语言理解与生成、多模态理解与生成等主题。

* [airaria/TextPruner](https://github.com/airaria/TextPruner) 用于预训练语言模型的基于 PyTorch 的模型修剪工具包.它提供了**低成本**和**免训练的**方法，通过去除冗余神经元来减小模型大小并加快模型推理速度。在 TextPruner 中，共有三种剪枝模式：**词汇剪枝**、**变压器剪枝**和**管道剪枝**。

* [Tencent/PatrickStar](https://github.com/Tencent/PatrickStar) 提供更大、更快、更环保的预训练模型，并为所有人普及人工智能。PatrickStar 的内存管理支持将模型的当前计算部分以外的所有内容卸载到 CPU 以节省 GPU。此外，在扩展到多个 GPU 时，基于块的内存管理对于集体通信非常有效。通过**异构训练**（DeepSpeed Zero Stage 3 也使用它），PatrickStar 可以充分利用 CPU 和 GPU 内存，这样您就可以使用更少的 GPU 来训练更大的模型。

* [ymcui/PERT](https://github.com/ymcui/PERT) 提出了一种基于乱序语言模型的预训练模型，在不引入掩码标记[MASK]的情况下自监督地学习文本语义信息。PERT在部分中英文NLU任务上获得性能提升，但也在部分任务上效果较差，请酌情使用。

* [THUDM/P-tuning-v2](https://github.com/THUDM/P-tuning-v2)  P-tuning v2 对预训练变压器的每一层输入应用连续提示。深度提示调整增加了连续提示的容量，并缩小了跨各种设置微调的差距，特别是对于小型模型和艰巨的任务。将文本生成的prefix-tuning技术适配到NLU任务。Prompting技术火爆NLP社区，其将预训练模型从Fine-tuning范式带入Prompt-Engineering时代。Promp最初由人工设计，自然语言提示本身十分脆弱，而且从优化角度无法达到最优。为了解决问题发展出了可学习的Prompt，而P-tuning v2在实际上就是Prefix-tuning，在Prefix部分，每一层transformer的embedding输入需要被tuned。在不同规模大小的LM模型上，P-tuning v2能与精调（Fine-tuning）方法的表现比肩，有时甚至更好。

* [EleutherAI/gpt-neox](https://github.com/EleutherAI/gpt-neox) 基于 DeepSpeed 库的 GPU 上模型并行自回归转换器（autoregressive transformers）的实现。目前基于 NVIDIA 的威震天语言模型，并已通过 DeepSpeed 的技术以及一些新颖的优化进行了增强。希望在此过程中训练和开源 175B 参数 GPT-3 复制。

* [OpenBMB/BMTrain](https://github.com/OpenBMB/BMTrain) 高效的大型模型训练工具包，可用于训练具有数百亿参数的大型模型。 它可以以分布式方式训练模型，同时保持代码像单机训练一样简单。

* [microsoft/CodeBERT](https://github.com/microsoft/CodeBERT) 针对编程语言的预训练模型，在Py、Java、JS、PHP、Ruby、Go的 NL-PL 对上进行预训练的多编程语言模型。

* [clue-ai/PromptCLUE](https://github.com/clue-ai/PromptCLUE) 大规模多任务Prompt预训练中文开源模型。千亿中文token上大规模预训练，累计学习1.5万亿中文token，亿级中文任务数据上完成训练，训练任务超过150+。比base版平均任务提升7个点+；具有更好的理解、生成和抽取能力，并且支持文本改写、纠错、知识图谱问答。

* [BlinkDL/RWKV-LM](https://github.com/BlinkDL/RWKV-LM) 具有 Transformer 级 LLM 性能的 RNN。它可以像 GPT（可并行化）一样直接训练。因此，它结合了 RNN 和 Transformer 的优点——出色的性能、快速推理、节省 VRAM、快速训练、“无限”ctx_len 和自由句子嵌入。

* [FlagOpen/FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) 可以将任何文本映射到低维密集向量，该向量可用于检索、分类、聚类或语义搜索等任务。它也可以用于LLM的矢量数据库。

## 文本分类

* [kk7nc/Text_Classification](https://github.com/kk7nc/Text_Classification) 一项文本分类算法的调查

* [cnn_multilabel_classification](https://github.com/tcxdgit/cnn_multilabel_classification) 基于TextCNN和Attention的多标签分类

* [ilivans/tf-rnn-attention](https://github.com/ilivans/tf-rnn-attention) Tensorflow实现文本分类任务的关注机制。

* [skdjfla/toutiao-text-classfication-dataset](https://github.com/skdjfla/toutiao-text-classfication-dataset) 中文文本分类数据集 共38.2万条，分布于15类中。

* [xiaoqian19940510/text-classification-surveys](https://github.com/xiaoqian19940510/text-classification-surveys) 文本分类资源汇总，包括深度学习文本分类模型，如SpanBERT、ALBERT、RoBerta、Xlnet、MT-DNN、BERT、TextGCN、MGAN、TextCapsule、SGNN、SGM、LEAM、ULMFiT、DGCNN、ELMo、RAM、DeepMoji、IAN、DPCNN、TopicRNN、LSTMN 、Multi-Task、HAN、CharCNN、Tree-LSTM、DAN、TextRCNN、Paragraph-Vec、TextCNN、DCNN、RNTN、MV-RNN、RAE等，浅层学习模型，如LightGBM 、SVM、XGboost、Random Forest、C4.5、CART、KNN、NB、HMM等。介绍文本分类数据集，如MR、SST、MPQA、IMDB、Ye…

* [649453932/Chinese-Text-Classification-Pytorch](https://github.com/649453932/Chinese-Text-Classification-Pytorch) 中文文本分类，TextCNN，TextRNN，FastText，TextRCNN，BiLSTM_Attention，DPCNN，Transformer，基于pytorch，开箱即用。

* [649453932/Bert-Chinese-Text-Classification-Pytorch](https://github.com/649453932/Bert-Chinese-Text-Classification-Pytorch)  使用Bert，ERNIE，进行中文文本分类

* [SanghunYun/UDA_pytorch](https://github.com/SanghunYun/UDA_pytorch) Unsupervised Data Augmentation  with BERT 一种半监督学习方法，可在多种语言和视觉任务上实现SOTA结果。仅用20个标记的示例，UDA的性能就优于之前在25,000个标记的示例上训练的IMDb上的SOTA。

* [TextCNN与ALBERT分类效果的实践](https://zhuanlan.zhihu.com/p/443782891) 详解小样本短文本多分类-对比TextCNN与ALBERT分类效果的实践（附Pytorch代码）

* [GT-SALT/MixText](https://github.com/GT-SALT/MixText) 文本半监督方法MixText 提出一种全新文本增强方式——TMix，在隐式空间插值，生成全新样本。对未标注样本进行低熵预测，并与标注样本混合进行TMix。MixText可以挖掘句子之间的隐式关系，并在学习标注样本的同时利用无标注样本的信息。超越预训练模型和其他半监督方法

* [beyondguo/label_confusion_learning](https://github.com/beyondguo/label_confusion_learning) 利用标签之间的混淆关系，提升文本分类效果。利用标签信息时能够充分考虑标签之间的重叠或者依赖关系。

* [AIRobotZhang/STCKA](https://github.com/AIRobotZhang/STCKA) 基于知识图谱的文本分类.将每个短文本与其在KB中的相关概念相关联，将概念信息作为先验知识整合到深度神经网络中。

* [ShannonAI/Neural-Semi-Supervised-Learning-for-Text-Classification](https://github.com/ShannonAI/Neural-Semi-Supervised-Learning-for-Text-Classification) 在大规模通用领域预训练的前提下，更好地利用大规模领域内无标注语料与标注语料，从而最大限度地提升模型效果.足量的领域内语料U使模型不需要再在通用领域语料上预训练；无论是采用预训练还是自训练的方式，都可以显著提升模型效果，二者结合可以得到最佳结果；当领域内标注数据D较小的时候，在伪平行数据D'上训练、再在D上微调可以提升更多的效果；当D更大的时候，在D和D'上联合训练取得的效果更好。

* [xmu-xiaoma666/External-Attention-pytorch](https://github.com/xmu-xiaoma666/External-Attention-pytorch) 17篇注意力机制 PyTorch 实现

* [DunZhang/LM-MLC](https://github.com/DunZhang/LM-MLC) 基于完型填空(模板)的多标签分类算法.

* [bojone/r-drop](https://github.com/bojone/r-drop) 使用r-drop机制实验了中文文本分类、文本生成任务，有提升。

* [BUPT-GAMMA/CompareNet_FakeNewsDetection](https://github.com/BUPT-GAMMA/CompareNet_FakeNewsDetection) 与知识比较：使用外部知识进行图神经假新闻检测 (ACL 2021)

* [pangwong/pytorch-multi-label-classifier](https://github.com/pangwong/pytorch-multi-label-classifier) pytorch 实现的多标签分类分类器

* [xuyige/BERT4doc-Classification](https://github.com/xuyige/BERT4doc-Classification) 如何微调 BERT 进行文本分类

* [timoschick/pet](https://github.com/timoschick/pet) 该存储库包含“利用小样本文本分类和自然语言推理的完形填空题”的代码.介绍了模式利用训练 (PET)，这是一种半监督训练程序，可将输入示例重新表述为完形填空式短语。在低资源环境中，PET 和 iPET 显着优于常规监督训练、各种半监督基线甚至 GPT-3，尽管需要的参数减少 99.9%。PET 的迭代变体 (iPET) 训练多代模型，甚至可以在没有任何训练数据的情况下使用。

* [YerevaNN/warp](https://github.com/YerevaNN/warp) ACL'2021 论文 WARP Cyclone Word-level Adversarial ReProgramming 的代码。 在 SuperGLUE 少样本文本分类上优于“GPT-3”。提出了一种基于对抗性重编程的替代方法，它是自动扩展提示模板生成的早期工作。而且参数量少了好多个数量级。

* [whatissimondoing/CoG-BART](https://github.com/whatissimondoing/CoG-BART) 对比度和生成使BART成为很好的对话情感识别器

* [hiyouga/Dual-Contrastive-Learning](https://github.com/hiyouga/dual-contrastive-learning) 双重对比学习。 通过在同一空间内同时学习输入样本的特征和分类器的参数，为监督分类任务提出了一种新颖的对比学习框架。

* [thunlp/KnowledgeablePromptTuning](https://github.com/thunlp/KnowledgeablePromptTuning) 将知识整合到 Prompt Verbalizer 中进行文本分类

* [zhouj8553/FlipDA](https://github.com/zhouj8553/FlipDA) 提供了一种基于 T5 和翻转标签自训练的自动数据增强方法。 我们在 FewGLUE 上对其进行评估，并提高其性能。

## 文本摘要

* [xcfcode/Summarization-Papers](https://github.com/xcfcode/Summarization-Papers) 文本摘要论文总结

* [abisee/pointer-generator](https://github.com/abisee/pointer-generator) 使用指针生成器网络进行汇总

* [AIKevin/Pointer_Generator_Summarizer](https://github.com/AIKevin/Pointer_Generator_Summarizer) 指针生成器网络：具有关注，指向和覆盖机制的Seq2Seq，用于抽象性摘要。 tensorflow 2.0

* [kjc6723/seq2seq_Pointer_Generator_Summarizer](https://github.com/kjc6723/seq2seq_Pointer_Generator_Summarizer) 中文会话中生成摘要总结的项目  tensorflow 2.0

* [steph1793/Pointer_Transformer_Generator](https://github.com/steph1793/Pointer_Transformer_Generator) 指针生成器网络 tensorflow 2.0

* [magic282/NeuSum](https://github.com/magic282/NeuSum) 通过共同学习评分和选择句子进行神经文本摘要

* [dmmiller612/bert-extractive-summarizer](https://github.com/dmmiller612/bert-extractive-summarizer) BERT易于使用的提取文本摘要

* [nju-websoft/NEST](https://github.com/nju-websoft/NEST) 输入知识图谱的基于联合编码的弱监督神经实体摘要方法

* [bojone/SPACES](https://github.com/bojone/SPACES) 端到端的长本文摘要模型（法研杯2020司法摘要赛道）

* [xcfcode/Summarization-Papers](https://github.com/xcfcode/Summarization-Papers) 文本摘要论文列表，包括各种主题。

* [yym6472/ms_pointer_network](https://github.com/yym6472/ms_pointer_network) 用多来源Pointer Network的产品标题摘要方法.从两个信息来源：原始商品标题和知识信息knowledge中抽取信息，然后将二者进行综合得到最后的结果。

* [FeiSun/ProductTitleSummarizationCorpus](https://github.com/FeiSun/ProductTitleSummarizationCorpus) Dataset for CIKM 2018 paper "Multi-Source Pointer Network for Product Title Summarization" 用于产品标题摘要的多源指针网络

* [jiacheng-ye/kg_one2set](https://github.com/jiacheng-ye/kg_one2set) 解决关键词生成任务，给一篇源文档（比如论文的摘要），关键词预测任务就是预测出一些表达文档重点信息的关键词，或者更准确的说是关键短语。提出了模型SetTrans，其特点是能够预测更多、更准确而且重复率更低的关键词集合。并行预测，在 inference 效率上是Transfomer的6.44倍。

* [MaartenGr/keyBERT](https://github.com/MaartenGr/keyBERT) 一种最小且易于使用的关键字提取技术，它利用BERT嵌入来创建与文档最相似的关键字和关键字短语。

* [xcfcode/PLM_annotator](https://github.com/xcfcode/PLM_annotator) 探索对话总结的 DialoGPT

* [RowitZou/topic-dialog-summ](https://github.com/RowitZou/topic-dialog-summ) 具有显着性感知主题建模的客户服务的面向主题的口语对话摘要。数据集是从阿里巴巴客户服务中心收集的。所有对话都是在客户和服务代理之间进行的普通话来电。脱敏数据可在 [Google Drive](https://drive.google.com/file/d/1X3-C9vTYfk43T5NIEvRsdRIJkN1RuG7b/view?usp=sharing)或[百度盘](https://pan.baidu.com/s/1AvkGnerKpQHUNbwkz9kO7A)（提取码：t6nx）上获得。

* [maszhongming/MatchSum](https://github.com/maszhongming/MatchSum)  背景: 传统抽取式摘要模型都是基于句子级提取的，即未考虑句子间关系，对所有句子逐个打分，取topN的句子为摘要。主要贡献:考虑句子间的关系，通过候选句间的组合句来抽取摘要;基于摘要与原文档在语义上应该有较大匹配度的考量，本文提出了基于候选句间的组合句与原文档的相似度来判断文档摘要的模型.对六个摘要提取数据集进行分析，验证了句子级得分高的摘要并不是摘要级得分最高的。如果仅以句子级，容易产生pearl-summary, 即虽然句子得分较低，但其实是较好的摘要，作者称为沧海遗珠。

* [nlpyang/PreSumm](https://github.com/nlpyang/PreSumm) 基于BERT的文档级编码器，该编码器能够表达文档的语义，并获得文档的句子表示。并分别提出了抽取式和生成式的摘要模型。

* [nlpyang/BertSum](https://github.com/nlpyang/BertSum) BERT的简单变体 用于抽取式文本摘要，主要是选择性抽取文本中的句子作为最后的摘要。这个任务最大的问题是如何获得每个句子向量，然后把向量用于二分类，判断去留。而 BERT 原模型只能生成单句的句子向量，或者句子对的。（1）将文档中每句话前加 [CLS]后加[SEP]，然后输入 BERT，而每个[CLS]对应的位置就是每句的句向量。（2）为了进一步增加句之间的互动，在 BERT 之上加了一层 Transformer 的 Summarization Layer，只输入每个[CLS]的向量，最后输出预测当前句是否保留，finetune。

* [OpenSUM/CPSUM](https://github.com/OpenSUM/CPSUM) 半监督抽取式摘要的噪声注入一致性训练和熵约束伪标签

* [krystalan/ClidSum](https://github.com/krystalan/ClidSum) 一个跨语言对话摘要的基准数据集

## 文本生成、文本对话

### 类ChatGPT大语言对话模型及数据

* [Significant-Gravitas/Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT#auto-gpt-an-autonomous-gpt-4-experiment) 使用GPT4来自动完成目标任务。一个实验性开源应用程序，展示了 GPT-4 语言模型的功能。该程序由 GPT-4 驱动，将 LLM 的“思想”链接在一起，以自主实现您设定的任何目标。作为 GPT-4 完全自主运行的首批示例之一，Auto-GPT 突破了 AI 的可能性界限。

* [AntonOsika/gpt-engineer](https://github.com/AntonOsika/gpt-engineer) GPT 工程师易于调整、扩展，它根据提示生成整个代码库。指定您希望它构建的内容，AI 要求澄清，然后构建它。

* [facebookresearch/llama](https://github.com/facebookresearch/llama) facebook LLaMA 模型的推理代码。最新版本的 Llama 现在可供各种规模的个人、创作者、研究人员和企业访问，以便他们可以负责任地进行实验、创新和扩展他们的想法。

* [THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 开源中英双语对话模型 ChatGLM-6B 的第二代版本，在保留了初代模型对话流畅、部署门槛较低等众多优秀特性的基础之上，引入了如下新特性：`更强大的性能`：全面升级了基座模型。ChatGLM2-6B 使用了 GLM 的混合目标函数，经过了 1.4T 中英标识符的预训练与人类偏好对齐训练，评测结果显示，相比于初代模型，MMLU（+23%）、CEval（+33%）、GSM8K（+571%） 、BBH（+60%）等数据集上的性能取得了大幅度的提升，在同尺寸开源模型中具有较强的竞争力。`更长的上下文`：基于 FlashAttention 技术，我们将基座模型的上下文长度（Context Length）由 ChatGLM-6B 的 2K 扩展到了 32K，并在对话阶段使用 8K 的上下文长度训练。对于更长的上下文，我们发布了 ChatGLM2-6B-32K 模型。LongBench 的测评结果表明，在等量级的开源模型中，32K 有着较为明显的竞争优势。`更高效的推理`：基于 Multi-Query Attention 技术，有更高效的推理速度和更低的显存占用：在官方的模型实现下，推理速度相比初代提升了 42%，INT4 量化下，6G 显存支持的对话长度由 1K 提升到了 8K。`更开放的协议`：权重对学术研究完全开放，在填写问卷进行登记后亦允许免费商业使用。

* [THUDM/ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) 开源的、支持中英双语的对话语言模型，基于 [General Language Model (GLM)](https://github.com/THUDM/GLM) 架构，具有 62 亿参数。结合模型量化技术，用户可以在消费级的显卡上进行本地部署（INT4 量化级别下最低只需 6GB 显存）。 ChatGLM-6B 使用了和 ChatGPT 相似的技术，针对中文问答和对话进行了优化。经过约 1T 标识符的中英双语训练，辅以监督微调、反馈自助、人类反馈强化学习等技术的加持，62 亿参数的 ChatGLM-6B 已经能生成相当符合人类偏好的回答。

* [THUDM/GLM-130B](https://github.com/THUDM/GLM-130B) GLM-130B是一个开放的双语（英汉）双向密集模型，具有1300亿个参数，使用通用语言模型（GLM）算法进行预训练。它旨在支持单个 A100 （40G * 8） 或 V100 （32G * 8） 上具有 130B 参数的推理任务。通过 INT4 量化，硬件可以进一步降低到具有 4 * RTX3090 24G 的单个服务器，几乎没有性能下降。

* [QwenLM/Qwen-7B](https://github.com/QwenLM/Qwen-7B) 由阿里云提出的Qwen-7B（通义千问-7B）聊天和预训练大语言模型的官方存储库。使用高质量的预训练数据进行训练。我们已经在超过2.2万亿个代币的自建大规模高质量数据集上预训练了Qwen-7B。该数据集包括纯文本和代码，涵盖广泛的领域，包括一般领域数据和专业领域数据。更好地支持语言。我们的分词器基于超过 150K 个代币的大词汇表，与其他分词器相比更有效。它对多种语言都很友好，并且有助于用户进一步微调Qwen-7B以扩展对某种语言的理解。支持 8K 上下文长度。Qwen-7B和Qwen-7B-Chat都支持8K的上下文长度，这允许输入长上下文。支持插件。Qwen-7B-Chat 是用插件相关的对齐数据训练的，因此它能够使用工具，包括 API、模型、数据库等，并且能够作为代理进行游戏。

* [imoneoi/openchat](https://github.com/imoneoi/openchat) 使用不完善的数据推进开源语言模型。OpenChat是一系列基于监督微调（SFT）的开源语言模型。我们利用 ~80k ShareGPT 对话与条件反射策略和加权损失，尽管我们的方法很简单，但仍实现了卓越的表现。我们的最终愿景是开发一个高性能、开源和商用的大型语言模型，并且我们正在不断取得进展。

* [lonePatient/awesome-pretrained-chinese-nlp-models](https://github.com/lonePatient/awesome-pretrained-chinese-nlp-models) 高质量中文预训练模型集合。包括：基础大模型、对话大模型、多模态对话大模型、大模型评估基准、开源模型库平台、开源数据集库、中文指令数据集。

* [Vision-CAIR/MiniGPT-4](https://github.com/Vision-CAIR/MiniGPT-4) MiniGPT-4：使用高级大型语言模型增强视觉语言理解 提供与 Vicuna-7B 对齐的预训练 MiniGPT-4！演示 GPU 内存消耗现在可以低至 12GB。
- [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) 纯C/C++中LLaMA模型的CPU推理。2023年FacebookResearch 开源了大规模语言模型LLaMA，包含从 7B 到 65B 的参数范围，训练使用多达 1.4万亿 tokens 语料。LLaMA-13B在大部分基准测评上超过了GPT3-175B，LLaMA可能是目前公开模型权重中效果最好的语言模型。

- [juncongmoo/pyllama](https://github.com/juncongmoo/pyllama) LLaMA - 在单个 4GB GPU 中运行 LLM

- [tatsu-lab/stanford_alpaca](https://github.com/tatsu-lab/stanford_alpaca) 斯坦福大学的LLaMA羊驼模型。用2K数据微调模型，构建和共享一个遵循指令的LLaMA模型。
* [LC1332/Chinese-alpaca-lora](https://github.com/LC1332/Chinese-alpaca-lora) 在LLaMA、斯坦福大学Alpaca、Alpaca LoRA、Cabrita、Japanese-Alpaca-LoRA的基础上，调试了一个中国LLaMA模型。同时使用ChatGPT API将alpaca_data. json翻译为中文，再进行微调。

* [tloen/alpaca-lora](https://github.com/tloen/alpaca-lora) 在消费者硬件上使用指令来微调LLaMA模型。使用低秩自适应（LoRA）重现斯坦福大学Alpaca结果的代码。我们提供了一个与 text-davinci-003质量相似的Instruct模型，可以在Raspberry Pi上运行（用于研究），并且代码很容易扩展到 13b ， 30b 和 65b模型。

* [mymusise/ChatGLM-Tuning](https://github.com/mymusise/ChatGLM-Tuning) 平价的chatgpt实现方案, 基于ChatGLM-6B + LoRA

* [OpenLMLab/MOSS](https://github.com/OpenLMLab/MOSS) 支持中英双语和多种插件的开源对话语言模型，moss-moon系列模型具有160亿参数。开源数据: moss-002-sft-data: 多轮对话数据，覆盖有用性、忠实性、无害性三个层面，包含由text-davinci-003生成的约57万条英文对话和59万条中文对话。moss-003-sft-data: 多轮对话数据，基于MOSS-002内测阶段采集的约10万用户输入数据和gpt-3.5-turbo构造而成，更加符合真实用户意图分布，包含更细粒度的有用性类别标记、更广泛的无害性数据和更长对话轮数，约含110万条对话数据。moss-003-sft-plugin-data: 插件增强的多轮对话数据，包含支持搜索引擎、文生图、计算器、解方程等四个插件在内的约30万条多轮对话数据。moss-003-pm-data: 偏好数据，包含在约18万额外对话上下文数据及使用moss-moon-003-sft所产生的回复数据上构造得到的偏好对比数据。

* [baichuan-inc/baichuan-7B](https://github.com/baichuan-inc/baichuan-7B) 百川公司开发的大规模7B预训练语言模型。一个开源可商用的大规模预训练语言模型。基于 Transformer 结构，在大约 1.2 万亿 tokens 上训练的 70 亿参数模型，支持中英双语，上下文窗口长度为 4096。在标准的中文和英文 benchmark（C-Eval/MMLU）上均取得同尺寸最好的效果。

* [clue-ai/ChatYuan](https://github.com/clue-ai/ChatYuan) 用于问答、结合上下文做对话、做各种生成任务，包括创意性写作，也能回答一些像法律、新冠等领域问题。它基于PromptCLUE-large结合数亿条功能对话多轮对话数据进一步训练得到。

* [lm-sys/FastChat](https://github.com/lm-sys/FastChat) 令人印象深刻的 GPT-4 开放式聊天机器人 Vicuna：一个以 90% ChatGPT 质量的开源聊天机器人。

* [project-baize/baize-chatbot](https://github.com/project-baize/baize-chatbot) 使用 LoRA 训练的开源聊天模型.它使用通过让 ChatGPT 与自己聊天生成的 100k 对话。还使用羊驼的数据来提高其性能。已发布了 7B、13B 和 30B 模型。

* [AI4Finance-Foundation/FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) 以数据为中心的 FinGPT。开源开放金融！革新

* [EleutherAI/gpt-neox](https://github.com/EleutherAI/gpt-neox) 在GPU上训练大规模语言模型。基于 NVIDIA 的威震天语言模型，并已通过 DeepSpeed 的技术以及一些新颖的优化进行了增强。目标是使这个存储库成为一个集中且可访问的地方，以收集用于训练大规模自回归语言模型的技术，并加速对大规模训练的研究。

* [visual-openllm/visual-openllm](https://github.com/visual-openllm/visual-openllm) 文心一言的开源版，基于 ChatGLM + Visual ChatGPT + Stable Diffusion

* [hikariming/alpaca_chinese_dataset](https://github.com/hikariming/alpaca_chinese_dataset) 人工精调的中文对话数据集和一段chatglm的微调代码

* [ymcui/Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) 中文LLaMA模型和经过指令精调的Alpaca大模型。这些模型在原版LLaMA的基础上扩充了中文词表并使用了中文数据进行二次预训练，进一步提升了中文基础语义理解能力。同时，在中文LLaMA的基础上，本项目使用了中文指令数据进行指令精调，显著提升了模型对指令的理解和执行能力。

* [Facico/Chinese-Vicuna](https://github.com/Facico/Chinese-Vicuna) 一个中文低资源的llama+lora方案，结构参考alpaca

* [lucidrains/PaLM-rlhf-pytorch](https://github.com/lucidrains/PaLM-rlhf-pytorch) 在PaLM架构上实现RLHF（人工反馈强化学习）,类似ChatGPT

* [liltom-eth/llama2-webui](https://github.com/liltom-eth/llama2-webui) 从任何地方（Linux/Windows/Mac）在GPU或CPU上本地运行任何Llama 2。使用“llama2-wrapper”作为生成代理/应用程序的本地llama2后端。

* [togethercomputer/OpenChatKit](https://github.com/togethercomputer/OpenChatKit) 一个强大的开源基础，可以为各种应用程序创建专用和通用聊天机器人。该工具包包括一个指令调优的语言模型，一个审核模型，和一个可扩展的检索系统，用于包括来自自定义存储库的最新响应。

* [LianjiaTech/BELLE](https://github.com/LianjiaTech/BELLE) 开源中文对话大模型，现阶段基于开源预训练大语言模型（如BLOOM），针对中文做了优化，模型调优仅使用由ChatGPT生产的数据（不包含任何其他数据）。开放了数据集：Stanford Alpaca 生成的中文数据集1M + 0.5M；0.25M数学指令数据集和0.8M多轮任务对话数据集。

* [carbonz0/alpaca-chinese-dataset](https://github.com/carbonz0/alpaca-chinese-dataset) alpaca中文指令微调数据集

* [cryscan/multilingual-share](https://huggingface.co/datasets/cryscan/multilingual-share) 为了推进中文AI的发展，促进AI技术公开化、国际化，我们成立了 ShareGPT-90k 项目，希望借助大家的力量推进数据清洗与对齐工作。可能与各位想象的有所不同，GPT模型主要通过预训练数据集赋能，语料的质量对模型最终性能至关重要。然而，百度知道、CSDN、知乎等平台软文过多；小木虫等高质量平台语料过少；个人博客内容质量参差不齐。OpenAI完成数据集的收集花费了巨大成本，以至于需要从微软集资。我们无力承担如此巨大的开销，于是需要各位有志于筹建开放获取语料，并有一定外语基础的网友们献上自己的力量。[RWKV-Wiki/MultilingualShareGPT](https://github.com/RWKV-Wiki/MultilingualShareGPT)

* [TigerResearch/TigerBot](https://github.com/TigerResearch/TigerBot) 多语言多任务LLM，在 BLOOM 基础上的模型：TigerBot-7B, TigerBot-7B-base，TigerBot-180B。数据：预训练 100G，从 2TB 过滤后的数据中经过去噪去重清洗而得；监督微调 1G 或 100 万条数据，按比例涵盖用户指令常见的 10 大类 120 小类任务。

  * [中文开源预训练集 - 55G，包含中文书籍、中文互联网、中文百科](https://huggingface.co/datasets/TigerResearch/pretrain_zh)

  * [英文开源预训练集 - 51G，包含英文书籍、英文互联网、英文百科](https://huggingface.co/datasets/TigerResearch/pretrain_en)
  - [中文-微调指令集-合集 - 53W 条 - 下载 [hugging face]](https://huggingface.co/datasets/TigerResearch/sft_zh)

  - [英文-微调指令集-合集 - 67W 条 - 下载 [hugging face]](https://huggingface.co/datasets/TigerResearch/sft_en)

* [masa3141/japanese-alpaca-lora](https://github.com/masa3141/japanese-alpaca-lora) 日文指令来微调LLaMA模型

* [22-hours/cabrita](https://github.com/22-hours/cabrita) 葡萄牙语微调指令LLaMA

* [Stability-AI/StableLM](https://github.com/Stability-AI/StableLM) 稳定性AI语言模型。使用 Stanford Alpaca 的程序对模型进行了微调，结合了五个最近的对话代理数据集：Stanford 的 Alpaca 、Nomic-AI 的 gpt4all 、RyokoAI 的 ShareGPT52K 数据集、Databricks的 Dolly 和 HH 。以 StableLM-Tuned-Alpha 的形式发布这些模型。

* [LC1332/Luotuo-Chinese-LLM](https://github.com/LC1332/Luotuo-Chinese-LLM) 中文大语言模型开源项目，包含了一系列语言模型。Luotuo-Vanilla是骆驼项目的第一个github仓库, 它是在LLaMA-7B上进行微调的。骆驼项目的初始目标，是研究使用跨语言数据在进行微调时，大语言模型发生的相关现象。

* [FreedomIntelligence/LLMZoo](https://github.com/FreedomIntelligence/LLMZoo) 一个为大型语言模型提供数据，模型和评估基准的项目。发布基于BLOOMZ的凤凰Phoenix7B模型、Chimera奇美拉模型。Phoenix-inst-chat-7b  达到85.2% 的ChatGPT效果。

* [openai/evals](https://github.com/openai/evals) 一个评估LLM和LLM系统的框架，也是一个开源的基准测试表。

* [pengxiao-song/LaWGPT](https://github.com/pengxiao-song/LaWGPT) 基于中文法律知识的大语言模型

* [MediaBrain-SJTU/MedicalGPT-zh](https://github.com/MediaBrain-SJTU/MedicalGPT-zh) 基于ChatGLM的在高质量指令数据集微调的中文医疗对话语言模型

* [mlfoundations/open_flamingo](https://github.com/mlfoundations/open_flamingo) 用于训练大型多模态模型的开源框架。DeepMind Flamingo 模型的开源版本。提供了用于训练和评估模型的 PyTorch 实现。还提供了在新的多模式 C4 数据集上训练的初始 OpenFlamingo 9B 模型。

* [dandelionsllm/pandallm](https://github.com/dandelionsllm/pandallm) 海外中文开源大语言模型，基于 Llama-7B, -13B, -33B, -65B 进行中文领域上的持续预训练。

* [OptimalScale/LMFlow](https://github.com/OptimalScale/LMFlow) 一个可扩展、方便和高效的工具箱，用于微调大型机器学习模型。我们的目标是开发一套用户友好、快速可靠，并对整个社区开放的全流程微调代码库。

* [yangjianxin1/Firefly](https://github.com/yangjianxin1/Firefly)  Firefly(流萤): 中文对话式大语言模型，包括高质量的包含1.1M中文多任务[指令微调数据集](https://huggingface.co/datasets/YeungNLP/firefly-train-1.1M)，包含23种常见的中文NLP任务的指令数据。对于每个任务，由人工书写若干指令模板，保证数据的高质量与丰富度。权重分享：在bloom-1b4-zh 和bloom-2b6-zh 的基础上，进行指令微调，获得如下中文模型：firefly-1b4 、firefly-2b6 、firefly-2b6-v2。开源QLoRA训练流程和模型权重

* [PlexPt/awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) ChatGPT 中文调教指南。各种场景使用指南。学习怎么让它听你的话。

* [dalinvip/Awesome-ChatGPT](https://github.com/dalinvip/Awesome-ChatGPT) ChatGPT资料汇总学习

* [rockbenben/ChatGPT-Shortcut](https://github.com/rockbenben/ChatGPT-Shortcut) 让生产力加倍的 ChatGPT 快捷指令，按照领域和功能分区，可对提示词进行标签筛选、关键词搜索和一键复制。

* [PhoebusSi/Alpaca-CoT](https://github.com/PhoebusSi/Alpaca-CoT) 将CoT数据扩展到Alpaca以提高其推理能力，同时我们将不断收集更多的instruction-tuning数据集,并在我们框架下集成进更多的LLM，打造一个通用的LLM-IFT平台。[Alpaca-CoT · Datasets](https://huggingface.co/datasets/QingyiSi/Alpaca-CoT)

* [sahil280114/codealpaca](https://github.com/sahil280114/codealpaca)  在代码生成指令上训练的 Instruction-following LLaMA Model。包括用于微调模型的 20K 数据。

* [unit-mesh/unit-minions](https://github.com/unit-mesh/unit-minions) 《AI 研发提效研究：自己动手训练 LoRA》，包含 Llama （Alpaca LoRA）模型、ChatGLM （ChatGLM Tuning）相关 Lora 的训练。训练内容：用户故事生成、测试代码生成、代码辅助生成、文本转 SQL、文本生成

* [microsoft/JARVIS](https://github.com/microsoft/JARVIS) 一个将LLM与ML社区联系起来的系统。该系统由LLM作为控制器和众多专家模型作为协作执行者（来自HuggingFace Hub）组成。我们系统的工作流程包括四个阶段：任务规划：使用ChatGPT分析用户的请求以了解他们的意图，并将其分解成可能解决的任务。模型选择：为了解决计划的任务，ChatGPT 根据他们的描述选择托管在拥抱脸上的专家模型。任务执行：调用并执行每个选定的模型，并将结果返回给 ChatGPT。响应生成：最后，使用 ChatGPT 集成所有模型的预测，并生成响应。

* [mlc-ai/mlc-llm](https://github.com/mlc-ai/mlc-llm) 使每个人都能在每个人的设备上本地开发、优化和部署 AI 模型。解决方案的基石是机器学习编译（MLC），我们利用它来有效地部署AI模型。我们建立在开源生态系统的肩膀上，包括来自Hugging Face和Google的令牌化器，以及Llama，Vicuna，Dolly，MOSS，RWKV等开源LLM。我们的主要工作流程基于 Apache TVM Unity。

* [mlc-ai/web-llm](https://github.com/mlc-ai/web-llm) 将大语言模型和聊天引入 Web 浏览器。一切都在浏览器中运行，没有服务器支持。WebLLM是MLC LLM的姊妹项目。它重用了模型工件并构建了MLC LLM的流程。

* [wangzhaode/ChatGLM-MNN](https://github.com/wangzhaode/ChatGLM-MNN) 纯C++，易于部署的ChatGLM-6B。

* [vllm-project/vllm](https://github.com/vllm-project/vllm) 适用于 LLM 的高吞吐量和内存效率推理和服务引擎。在吞吐量方面，vLLM 的性能比拥抱面转换器 （HF） 高出 24 倍，文本生成推理 （TGI） 高出 3.5 倍。使用**PagedAttention**分页注意力高效管理注意力键和值存储器。

* [adams549659584/go-proxy-bingai](https://github.com/adams549659584/go-proxy-bingai)用 Vue3 和 Go 搭建的微软 New Bing 演示站点，拥有一致的 UI 体验，支持 ChatGPT 提示词，国内可用。

* [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) 包含 ChatGPT 提示，以更好地使用 ChatGPT

* [humanloop/awesome-chatgpt](https://github.com/humanloop/awesome-chatgpt) ChatGPT和GPT-3的惊人工具、演示和文档

* [encx/ChatGPT](https://github.com/lencx/ChatGPT) ChatGPT 桌面应用程序(Mac、Windows 和 Linux)

* [xtekky/chatgpt-clone](https://github.com/xtekky/chatgpt-clone) 具有更好用户界面的聊天GPT界面

* [wong2/chatgpt-google-extension](https://github.com/wong2/chatgpt-google-extension) 浏览器扩展，用ChatGPT增强搜索引擎效果

* [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT) 逆向工程 ChatGPT 的API

* [ddiu8081/chatgpt-demo](https://github.com/ddiu8081/chatgpt-demo) 基于 OpenAI GPT-3.5 Turbo API 的 demo。

* [LAION-AI/Open-Assistant](https://github.com/LAION-AI/Open-Assistant) 基于聊天的助理，它理解任务，可以与第三方系统互动，并能动态地检索信息。将提供基于RLHF的大型语言模型，并公开训练数据。

* [acheong08/EdgeGPT](https://github.com/acheong08/EdgeGPT) 微软必应聊天的逆向工程API

* [yoheinakajima/babyagi](https://github.com/yoheinakajima/babyagi) 使用GPT3/4来自动完成任务。一个 AI 支持的任务管理系统示例. 该系统使用 OpenAI 和 Pinecone API 创建, 优先级排序和执行任务. 该系统背后的主要思想是基于先前任务的结果和预定义的目标创建任务. 脚本然后使用 OpenAI 的自然语言处理（NLP）能力根据目标创建新任务, 并使用 Pinecone 存储和检索任务结果以获得上下文. 这是原始的[任务驱动的自驱代理](https://twitter.com/yoheinakajima/status/1640934493489070080?s=20)的简化版本.

* [TransformerOptimus/SuperAGI](https://github.com/TransformerOptimus/SuperAGI) SuperAGI - 开发优先的开源自主 AI 代理框架。使开发人员能够快速可靠地构建、管理和运行有用的自主代理。

* [StanGirard/quivr](https://github.com/StanGirard/quivr) 将所有文件和想法转储到您的生成式AI（如chatgpt）的第二大脑中并与之聊天。旨在轻松存储和检索非结构化信息。

* [transitive-bullshit/chatgpt-api](https://github.com/transitive-bullshit/chatgpt-api) OpenAI提供的ChatGPT的Node.js包装器。

* [zhayujie/chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat) 用ChatGPT搭建微信聊天机器人

* [openai/openai-python](https://github.com/openai/openai-python) OpenAI Python库提供了从用Python语言编写的应用程序对OpenAI API的方便访问。

* [chenking2020/FindTheChatGPTer](https://github.com/chenking2020/FindTheChatGPTer) ChatGPT/GPT4开源“平替”汇总，持续更新

* [madawei2699/myGPTReader](https://github.com/madawei2699/myGPTReader) 由chatGPT提供支持,Slack上的一个机器人，可以阅读和总结任何网页，包括电子书在内的文档，甚至是YouTube上的视频。它可以通过语音和你交流。

* [JosephusCheung/GuanacoDataset](https://huggingface.co/datasets/JosephusCheung/GuanacoDataset) Guanaco 模型的数据集旨在增强多语言能力并解决各种语言任务。以 Alpaca 模型的 175个任务为基础，提供了用不同语言重写的种子任务，并添加了专门为英语语法分析、自然语言理解、跨语言自我意识和显式内容识别设计的新任务。数据集总共包含53万个条目，以6k美元的低成本生成。英语\中文\日语。

* [thunlp/UltraChat](https://github.com/thunlp/UltraChat) 大规模、信息丰富、多样化的多轮聊天数据（和模型）

* [ziliwangnlp/RefGPT](https://github.com/ziliwangnlp/RefGPT) 包含5万对中文多轮对话数据。用如下方法自动生成数据。采集优质的事实型文档，reference，来源是电子书、维基百科、优质垂类网站。文档需要涵盖尽量多的主题。利用已有LLM生成多轮对话。输入是一篇reference，prompt类似“请根据这篇文章生成多轮问答”。API输出一段多轮对话（dialogue）。这种方法将原本只适合预训练的文档转化成可供微调的多轮对话。收集到大量的reference-dialogue二元组。将reference和prompt作为输入，dialogue作为目标，微调一个GPT模型。称作Reference-to-Dialogue GPT，缩写RefGPT。有了RefGPT，即可基于reference生成多轮对话，获得海量的数据。需要关注2个要点。Reference的质量、广度。Reference内容质量必须高，比如医疗等优质垂类网站的页面、维基百科上非生僻的词条，且需要对网页做清洗。Reference的广度应当大，不能限制在单个垂类或网站。调用已有LLM时需要写prompt，需要仔细尝试各种prompt，使得LLM生成的多轮对话符合预期。

* [gururise/AlpacaDataCleaned](https://github.com/gururise/AlpacaDataCleaned) 经过清理和整理的斯坦福的羊驼数据集

* [wangrui6/Zhihu-KOL](https://huggingface.co/datasets/wangrui6/Zhihu-KOL) 知乎对话数据，parquet格式400多MB的大小

* [BAAI/COIG](https://huggingface.co/datasets/BAAI/COIG) 中文开放教学通才 (COIG) 项目，以维护一套无害、有用且多样化的中文对话语料库。具体包括：人工验证的翻译指令 (67798) 、考试指令 (63532) 、人类价值对齐指令 (34471) 、反事实修正多轮聊天（13653）、Leetcode 指令 (11737)

* [nomic-ai/pyllamacpp](https://github.com/nomic-ai/pyllamacpp) 支持 llama.cpp + gpt4all 的 Python 绑定

* [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) llama.cpp 的 Python 绑定

* [BlinkDL/ChatRWKV](https://github.com/BlinkDL/ChatRWKV) 使用RWKV语言模型（100%RNN）的类ChatGPT开源聊天模型。

* [rawandahmad698/PyChatGPT](https://github.com/rawandahmad698/PyChatGPT) 非官方 ChatGPT API 的 Python 客户端，具有自动令牌重新生成、对话跟踪、代理支持等功能。

* [qunash/chatgpt-advanced](https://github.com/qunash/chatgpt-advanced) 一种浏览器扩展，可通过网络结果增强您的 ChatGPT 提示。

* [mpociot/chatgpt-vscode](https://github.com/mpociot/chatgpt-vscode) 允许您使用 ChatGPT 的 VSCode 扩展

* [liady/ChatGPT-pdf](https://github.com/liady/ChatGPT-pdf) 用于将 ChatGPT 历史下载为 PNG、PDF 或创建可共享链接的 Chrome 扩展

* [imartinez/privateGPT](https://github.com/imartinez/privateGPT) 使用 LLM 的强大功能，无需互联网连接就可以对您的文档提出问题。 100% 私有，任何时候都没有数据离开您的执行环境。您可以在没有互联网连接的情况下提取文档和提问！

* [xtekky/gpt4free](https://github.com/xtekky/gpt4free) 免费使用GPT4模型 [typescript版本](https://github.com/xiangsx/gpt4free-ts)

* [saharmor/awesome-chatgpt](https://github.com/saharmor/awesome-chatgpt) 精选的 ChatGPT 演示、工具、文章等

* [JushBJJ/Mr.-Ranedeer-AI-Tutor](https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor) GPT-4 AI 导师提示，用于可定制的个性化学习体验。

* [binary-husky/chatgpt_academic](https://github.com/binary-husky/chatgpt_academic) 科研工作专用ChatGPT/GLM拓展，特别优化学术Paper润色体验，模块化设计支持自定义快捷按钮&函数插件，支持代码块表格显示，Tex公式双显示，新增Python和C++项目剖析&自译解功能，PDF/LaTex论文翻译&总结功能，支持并行问询多种LLM模型，支持gpt-3.5/gpt-4/chatglm

* [AetherCortex/Llama-X](https://github.com/AetherCortex/Llama-X) 关于将LLaMA提高到SOTA LLM的开放学术研究

* [WangRongsheng/ChatGenTitle](https://github.com/WangRongsheng/ChatGenTitle) 使用百万arXiv论文信息在LLaMA模型上进行微调的论文题目生成模型

* [nishiwen1214/ChatReviewer](https://github.com/nishiwen1214/ChatReviewer) 使用ChatGPT分析论文优缺点，提出改进建议

* [bhaskatripathi/pdfGPT](https://github.com/bhaskatripathi/pdfGPT) 允许您使用 GPT 功能与 PDF 文件的内容聊天。在聊天机器人中转换您的 pdf 文件的唯一开源解决方案

* [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) 全流程加速科研，利用chatgpt进行论文总结+润色+审稿+审稿回复

* [eimenhmdt/autoresearcher](https://github.com/eimenhmdt/autoresearcher) 使用 GPT 自动化科学工作流程

* [gragland/chatgpt-chrome-extension](https://github.com/gragland/chatgpt-chrome-extension) ChatGPT Chrome 扩展。将 ChatGPT 集成到互联网上的每个文本框中。

* [vincelwt/chatgpt-mac](https://github.com/vincelwt/chatgpt-mac) Mac 版 ChatGPT，就在您的菜单栏中。

* [GaiZhenbiao/ChuanhuChatGPT](https://github.com/GaiZhenbiao/ChuanhuChatGPT) 为ChatGPT ChatGLM LLaMA StableLM MOSS等多种LLM提供了一个轻快好用的Web图形界面

* [SCIR-HI/Med-ChatGLM](https://github.com/SCIR-HI/Med-ChatGLM) 基于中文医学知识的ChatGLM指令微调

* [xionghonglin/DoctorGLM](https://github.com/xionghonglin/DoctorGLM) 基于ChatGLM-6B的中文问诊模型

* [WangRongsheng/MedQA-ChatGLM](https://github.com/WangRongsheng/MedQA-ChatGLM) 基于真实医疗对话数据在ChatGLM上进行LoRA、P-Tuning V2、Freeze、RLHF等微调

* [Toyhom/Chinese-medical-dialogue-data](https://github.com/Toyhom/Chinese-medical-dialogue-data) 中文医疗对话数据集，:<Andriatria_男科> 94596个问答对 <IM_内科> 220606个问答对 <OAGD_妇产科> 183751个问答对 <Oncology_肿瘤科> 75553个问答对 <Pediatric_儿科> 101602个问答对 <Surgical_外科> 115991个问答对 总计 792099个问答对

* [sonnylazuardi/chat-ai-desktop](https://github.com/sonnylazuardi/chat-ai-desktop) 使用 Tauri 和 Rust 的 Mac 和 Windows 菜单栏的非官方 ChatGPT 桌面应用程序

* [xx025/carrot](https://github.com/xx025/carrot) 准备了众多免费好用的ChatGPT镜像站点，当前100+站点

* [LiLittleCat/awesome-free-chatgpt](https://github.com/LiLittleCat/awesome-free-chatgpt) 免费的 ChatGPT 镜像网站列表，持续更新。

* [yzfly/awesome-chatgpt-zh](https://github.com/yzfly/awesome-chatgpt-zh) ChatGPT 中文指南，ChatGPT 中文调教指南，指令指南，精选资源清单，更好的使用 chatGPT 让你的生产力

* [terry3041/pyChatGPT](https://github.com/terry3041/pyChatGPT) OpenAI的ChatGPT API的非官方Python包装器

* [platelminto/chatgpt-conversation](https://github.com/platelminto/chatgpt-conversation) 用你的声音与 ChatGPT 对话，让它回话。

* [202252197/ChatGPT_JCM](https://github.com/202252197/ChatGPT_JCM) OpenAI管理界面，聚合OpenAI的所有接口进行界面操作(所有模型、图片、音频、微调、文件)等，支持Markdown格式(公式、图表，表格)等

* [memochou1993/gpt-ai-assistant](https://github.com/memochou1993/gpt-ai-assistant) 使用 OpenAI API 和 LINE 消息传递 API 实现的应用程序。通过安装过程，您可以使用LINE移动应用程序开始与自己的AI助手聊天。

* [cesarhuret/docGPT](https://github.com/cesarhuret/docGPT) ChatGPT 直接在 Google Docs 中作为编辑器的插件

* [ConnectAI-E/Feishu-OpenAI](https://github.com/ConnectAI-E/Feishu-OpenAI) 飞书 ×（GPT-3.5 + DALL·E + Whisper）= 飞一般的工作体验 rocket 语音对话、角色扮演、多话题讨论、图片创作、表格分析、文档导出

* [terror/chatgpt.nvim](https://github.com/terror/chatgpt.nvim) 在 Neovim 中查询 ChatGPT

* [clmnin/summarize.site](https://github.com/clmnin/summarize.site) 浏览器扩展使用ChatGPT总结网页内容

* [shobrook/stackexplain](https://github.com/shobrook/stackexplain) 用 ChatGPT 解释您编程中的错误消息

* [Zero6992/chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot) 将 ChatGPT 集成到您自己的discord机器人中

* [m1guelpf/chatgpt-telegram](https://github.com/m1guelpf/chatgpt-telegram) 运行您自己的GPT电报机器人，只需一个命令

* [transitive-bullshit/chatgpt-twitter-bot](https://github.com/transitive-bullshit/chatgpt-twitter-bot) ChatGPT API支持的Twitter机器人

* [kxxt/chatgpt-action](https://github.com/kxxt/chatgpt-action) 让 ChatGPT 为您审查 PR 拉取请求

* [RomanHotsiy/commitgpt](https://github.com/RomanHotsiy/commitgpt) 使用 ChatGPT 自动生成git提交消息

* [oceanlvr/ChatGPT-ProBot](https://github.com/oceanlvr/ChatGPT-ProBot) 基于 ChatGPT 的 GitHub APP，键入 /chatgpt 与机器人 robot 聊天。

* [kazuki-sf/ChatGPT_Extension](https://github.com/kazuki-sf/ChatGPT_Extension) 非常简单的Chrome扩展（v3），您可以从网络上的任何地方访问OpenAI的ChatGPT。

* [abielzulio/chatgpt-raycast](https://github.com/abielzulio/chatgpt-raycast) ChatGPT raycast(Mac的快捷启动器) 扩展

* [bupticybee/ChineseAiDungeonChatGPT](https://github.com/bupticybee/ChineseAiDungeonChatGPT)  中文版的ai地牢，直接使用的openai的ChatGPT api作为讲故事的模型。

* [domeccleston/sharegpt](https://github.com/domeccleston/sharegpt) 轻松与您的朋友分享 ChatGPT 对话的永久链接

* [Yidadaa/ChatGPT-Next-Web](https://github.com/Yidadaa/ChatGPT-Next-Web) 一键拥有你自己的 ChatGPT 网页服务。

* [pengzhile/pandora](https://github.com/pengzhile/pandora) 实现了网页版 ChatGPT 的主要操作。后端优化，绕过 Cloudflare，速度喜人。

* [Chanzhaoyu/chatgpt-web](https://github.com/Chanzhaoyu/chatgpt-web)  用Express和Vue3搭建的 ChatGPT 演示网页

* [elyase/awesome-gpt3](https://github.com/elyase/awesome-gpt3) 关于 OpenAI GPT-3 API 的演示和文章的集合。

* [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) 提示工程是一门相对较新的学科，用于开发和优化提示以有效地将语言模型 (LM) 用于各种应用程序和研究主题。即时的工程技能有助于更好地理解大型语言模型 (LLM) 的功能和局限性。研究人员使用提示工程来提高 LLM 在广泛的常见和复杂任务（例如问题回答和算术推理）上的能力。开发人员使用提示工程来设计与 LLM 和其他工具交互的强大且有效的提示技术。

* [reworkd/AgentGPT](https://github.com/reworkd/AgentGPT) 在浏览器中组装、配置和部署自治 AI 代理。为您自己的自定义 AI 命名，让它开始任何可以想象的目标。它将尝试通过思考要完成的任务、执行它们并从结果中学习来达到目标。

* [openai/chatgpt-retrieval-plugin](https://github.com/openai/chatgpt-retrieval-plugin)  ChatGPT 检索插件可让您通过自然语言提问来轻松查找个人或工作文档。

* [kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference](https://github.com/kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference) 在本地CPU推理上运行Llama 2和其他开源LLM，用于文档问答

* [Bin-Huang/chatbox](https://github.com/Bin-Huang/chatbox) 开源的 ChatGPT API (OpenAI API) 桌面客户端，Prompt 的调试与管理工具，支持 Windows、Mac 和 Linux

* [openai/openai-cookbook](https://github.com/openai/openai-cookbook) 使用 OpenAI API 的示例和指南

* [smol-ai/developer](https://github.com/smol-ai/developer) 随着Anthropic Claude的100k 上下文窗口的出现，现在每个开发人员都可以拥有自己的辅助开发助手

* [e2b-dev/e2b](https://github.com/e2b-dev/e2b) 允​​许您创建和部署虚拟软件开发人员。这些虚拟开发人员由专门的 AI 代理提供支持，这些代理可以根据您的指令构建软件并可以使用工具。

* [csunny/DB-GPT](https://github.com/csunny/DB-GPT) 使用本地 GPT 与您的数据和环境交互，无数据泄漏，100% 私密，100% 安全 目前支持Vicuna(7b, 13b), ChatGLM-6b(int4, int8)

* [acheong08/Bard](https://github.com/acheong08/Bard) Google 的 Bard 聊天机器人 API 的逆向工程

* [jtsang4/claude-to-chatgpt](https://github.com/jtsang4/claude-to-chatgpt) 将 Anthropic 的 Claude 模型的 API 转换为 OpenAI Chat API 格式。

* [databrickslabs/dolly](https://github.com/databrickslabs/dolly) dolly-v2-12b是由Databricks创建的120亿参数因果语言模型，该模型源自EleutherAI的Pythia-12b，并在Databricks员工生成的~15K记录指令语料库上进行微调，并在宽松许可证（CC-BY-SA）下发布

* [openlm-research/open_llama](https://github.com/openlm-research/open_llama) 一个在RedPajama数据集上训练的Meta AI的LLaMA 7B的许可开源复制品。

* [mbzuai-nlp/LaMini-LM](https://github.com/mbzuai-nlp/LaMini-LM) 来自大规模指令的多样化蒸馏模型群。从ChatGPT提炼出来的小型高效语言模型的集合，并在2.58M指令的大规模数据集上进行训练。我们通过执行句子/离线提炼从大型语言模型中提取知识。我们基于几个现有的提示资源，使用 gpt-3.5-turbo 生成总共 2.58M 对指令和响应。

* [microsoft/TaskMatrix](https://github.com/microsoft/TaskMatrix) 连接了ChatGPT和一系列Visual Foundation模型，以便在聊天期间发送和接收图像。

* [huggingface/peft](https://github.com/huggingface/peft) 最先进的参数高效微调 （PEFT） 方法，LoRA、Prefix Tuning、P-Tuning、Prompt Tuning、AdaLoRA。参数高效微调 （PEFT） 方法能够将预训练的语言模型 （PLM） 有效地适应各种下游应用程序，而无需微调模型的所有参数。微调大型 PLM 的成本通常高得令人望而却步。在这方面，PEFT方法仅微调少量（额外）模型参数，从而大大降低了计算和存储成本。最近最先进的PEFT技术实现了与完全微调相当的性能。

* [artidoro/qlora](https://github.com/artidoro/qlora) 量化LLM的有效微调。QLoRA使用bitsandbytes进行量化。QLoRA是一种高效的微调方法，可减少内存使用量，足以在单个 48GB GPU 上微调 65B 模型，同时保留完整的 16 位微调任务性能。QLoRA 通过冻结的 4 位量化预训练LM将梯度反向传播到低秩适配器 （LoRA） 中。我们最好的模型 Guanaco，在 Vicuna 基准测试中优于之前所有公开的模型，达到了 ChatGPT 性能水平的 99.3%，而只需在单个 GPU 上进行 24 小时的微调。QLoRA 引入了许多创新，以在不牺牲性能的情况下节省内存：（a） 4 位 NormalFloat （NF4），一种理论上最适合正态分布权重的新数据类型 （b） 双重量化，通过量化常量来减少平均内存占用，以及 （c） 分页优化器来管理内存峰值。我们使用QLoRA对1k个模型进行微调，对 8 个指令数据集、多种模型（LLaMA、T5）和模型规模（如33B和65B参数）的指令遵循和聊天机器人性能进行详细分析。结果表明，QLoRA在小型高质量数据集上进行微调可以产生最先进的结果，即使用比以前的SoTA更小的模型也是如此。GPT4评估是人类评估的廉价且合理的替代方案。当前的聊天机器人基准测试不值得信赖，无法准确评估聊天机器人的性能水平。我们发布了所有模型和代码，包括用于 4 位训练的 CUDA 内核。

* [hiyouga/ChatGLM-Efficient-Tuning](https://github.com/hiyouga/ChatGLM-Efficient-Tuning) 基于 PEFT 的高效 ChatGLM 微调

* [ZrrSkywalker/LLaMA-Adapter](https://github.com/ZrrSkywalker/LLaMA-Adapter) 在1小时内遵循指令微调LLaMA , 1.2M参数

* [Instruction-Tuning-with-GPT-4/GPT-4-LLM](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM) 共享 GPT-4 生成的数据，用于构建具有监督学习和强化学习的指令遵循 LLM。存储库包含：

  - 英语教学 - 遵循数据由 GPT-4 使用 Alpaca 提示进行微调 LLM。
  - 由 GPT-4 使用由 ChatGPT 从羊驼翻译的中文提示生成的中文指令跟踪数据。
  - 按 GPT-4 排名以训练奖励模型的比较数据。
  - 关于非自然指令的答案 来自 GPT-4 的数据，用于大规模量化 GPT-4 和指令调整模型之间的差距。

* [lxe/simple-llm-finetuner](https://github.com/lxe/simple-llm-finetuner) 初学者友好的界面，旨在通过商用NVIDIA GPU上的PEFT库，使用LoRA方法微调各种语言模型。使用较小的数据集和 256 的样本长度，您甚至可以在常规的 Colab Tesla T4 实例上运行它。

* [Jittor/JittorLLMs](https://github.com/Jittor/JittorLLMs) 计图大模型推理库，具有高性能、配置要求低、中文支持好、可移植等特点。成本低：相比同类框架，本库可大幅降低硬件配置要求（减少80%），没有显卡，2G内存就能跑大模型；支持广：目前支持了4种大模型：[ChatGLM大模型](https://github.com/THUDM/ChatGLM-6B)、鹏程[盘古大模型](https://openi.org.cn/pangu/)、BlinkDL的[ChatRWKV](https://github.com/BlinkDL/ChatRWKV)、国外Meta的[LLaMA大模型](https://github.com/facebookresearch/llama)等；可移植：用户不需要修改任何代码，只需要安装Jittor版torch(JTorch)；速度快：大模型加载速度慢，Jittor框架通过零拷贝技术，大模型加载开销降低40%，同时，通过元算子自动编译优化，计算性能相比同类框架提升20%以上。

* [RUCAIBox/LLMSurvey](https://github.com/RUCAIBox/LLMSurvey) 与大型语言模型相关的论文和资源集合。

* [Lunabot](https://cn.lunabot.ai/zh/) 在任何网页为你服务的AI助理，通过快捷指令释放AI工作潜力，无需KEY和ChatGPT账号

* [jerryjliu/llama_index](https://github.com/jerryjliu/llama_index) 您的 LLM 应用程序的数据框架。高级 API 允许初学者使用 LlamaIndex 在 5 行代码中摄取和查询他们的数据。我们的低级 API 允许高级用户自定义和扩展任何模块（数据连接器、索引、检索器、查询引擎、重新排名模块）以满足他们的需求。

* [amazon-science/mm-cot](https://github.com/amazon-science/mm-cot) 语言模型中的多模式思维链推理。包括两个训练阶段：(i) 基本原理生成和 (ii) 答案推理。这两个阶段共享相同的模型架构，但输入和输出不同。

* [haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA) 面向多模态 GPT-4 级别功能构建的大型语言和视觉助手。

* [BradyFU/Awesome-Multimodal-Large-Language-Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) 多模态大型语言模型的最新论文和数据集

* [THUDM/VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B) 多模态中英双语对话语言模型

* [LC1332/Luotuo-Silk-Road](https://github.com/LC1332/Luotuo-Silk-Road) 中文大语言模型的数据。对话与指令数据集：Luotuo-Chinese-Alpaca 骆驼-中国-羊驼、Chinese-Dolly 中国多莉、Chinese-WizardLM 中国巫师LM、阅读理解数据 Chinese-CoQA 、Luotuo-QA-B、图文跨模态数据 Chinese-MMC4-130k 中文-MMC4-130k、Chinese-Coco-Captioning 中文-可可-字幕、Embedding蒸馏数据 CNewSum-Embedding

* [logspace-ai/langflow](https://github.com/logspace-ai/langflow) LangChain（大语言模型链式开发工具，强大的框架，可以简化构建高级语言模型应用程序的过程。） 的 UI，采用反应流设计，提供一种轻松的方式来实验和原型流。

* [YeungNLP/firefly-train-1.1M](https://huggingface.co/datasets/YeungNLP/firefly-train-1.1M) 收集了23个常见的中文数据集，对于每个任务，由人工书写若干种指令模板，保证数据的高质量与丰富度，数据量为115万 。

* [togethercomputer/RedPajama-Data](https://github.com/togethercomputer/RedPajama-Data) 包含用于准备大型数据集以训练大型语言模型的代码。重现LLaMA训练数据集的开源配方。Commoncrawl、C4、GitHub、Books、ArXiv、Wikipedia、StackExchange。合计1.2万亿令牌

* [Voine/ChatWaifu_Mobile](https://github.com/Voine/ChatWaifu_Mobile) 移动版二次元 AI 老婆聊天器 语言大模型来自 GhatGPT\语音推理为客户端本地 VITS - ncnn\图形渲染基于 Native Live2D\语音输入识别为客户端本地 Sherpa - ncnn

* [yizhongw/self-instruct](https://github.com/yizhongw/self-instruct) 将预训练的语言模型与自身生成的指令数据对齐。自我指导是一个框架，可帮助语言模型提高其遵循自然语言指令的能力。它通过使用模型自己的代数来创建大量教学数据来实现此目的。通过自导，可以提高语言模型的指令遵循功能，而无需依赖大量的手动注释。自指令过程是一种迭代引导算法，它从一组手动编写的指令种子开始，并使用它们来提示语言模型生成新指令和相应的输入输出实例。然后对这些世代进行过滤以删除低质量或类似的代数，并将生成的数据添加回任务池。此过程可以重复多次，从而产生大量教学数据，可用于微调语言模型以更有效地遵循说明。

* [Timothyxxx/Chain-of-ThoughtsPapers](https://github.com/Timothyxxx/Chain-of-ThoughtsPapers) 大型语言模型中的思维链促使引出推理。思想链论文集合

* [zilliztech/GPTCache](https://github.com/zilliztech/GPTCache) LLM 的语义缓存。 与 LangChain 和 llama_index 完全集成。

* [pashpashpash/vault-ai](https://github.com/pashpashpash/vault-ai) 使用 OP Stack（OpenAI + Pinecone Vector Database）为 ChatGPT 提供长期记忆。使用简单的 React 前端上传您自己的自定义知识库文件（PDF、txt、epub 等）。

* [jerry1993-tech/Cornucopia-LLaMA-Fin-Chinese](https://github.com/jerry1993-tech/Cornucopia-LLaMA-Fin-Chinese) 聚宝盆(Cornucopia): 基于中文金融知识的LLaMA微调模型；涉及SFT、RLHF、GPU训练部署等

* [THUDM/WebGLM](https://github.com/THUDM/WebGLM) 迈向具有人类偏好的高效网络增强问答系统。WebGLM希望使用100亿参数的GLM，提供高效且具有成本效益的Web增强问答系统。它旨在通过将 Web 搜索和检索功能集成到预先训练的语言模型中来改进实际应用程序部署。

* [FreedomIntelligence/HuatuoGPT](https://github.com/FreedomIntelligence/HuatuoGPT) 华佗GPT，迈向驯服语言模型成为医生。在庞大的中国医学语料库上训练的大型语言模型（LLM）。我们与华拓GPT的目标是为医疗咨询场景构建更专业的“ChatGPT”。[demo](https://www.huatuogpt.cn/)

* [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) 拖放UI以构建自定义LLM流程

* [xcanwin/KeepChatGPT](https://github.com/xcanwin/KeepChatGPT) ChatGPT的畅聊与增强插件。开源免费。不仅能解决所有报错不再刷新，还有保持活跃、取消审计、克隆对话、净化首页、展示大屏、展示全屏、言无不尽、拦截跟踪、日新月异等多个高级功能。让我们的AI体验无比顺畅、丝滑、高效、简洁。

* [ShishirPatil/gorilla](https://github.com/ShishirPatil/gorilla) LLM的API商店 。使 LLM 能够通过调用 API 来使用工具。给定一个自然语言查询，Gorilla 会提出语义和语法上正确的 API 来调用。通过Gorilla，我们是第一个演示如何使用LLM准确调用1，600+（并且不断增长的）API调用，同时减少幻觉的人。

* [microsoft/guidance](https://github.com/microsoft/guidance) 指南使你能够比传统的提示或链接更有效、更高效地控制新式语言模型。指导程序允许您将生成、提示和逻辑控制交错到单个连续流中，以匹配语言模型实际处理文本的方式。简单的输出结构，如思维链及其许多变体（例如，ART，Auto-CoT等）已被证明可以提高LLM的性能。像 GPT-4 这样更强大的 LLM 的出现允许更丰富的结构，而 guidance 使该结构更容易、更便宜。

* [fuergaosi233/wechat-chatgpt](https://github.com/fuergaosi233/wechat-chatgpt) 通过微信在微信上使用ChatGPT

* [fauxpilot/fauxpilot](https://github.com/fauxpilot/fauxpilot) GitHub Copilot服务器的开源替代品。构建GitHub Copilot的本地托管替代方案的尝试。它在NVIDIA的Triton Inference Server中使用SalesForce CodeGen模型和FasterTransformer后端。

* [Instruction-Tuning-with-GPT-4/GPT-4-LLM](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM) 旨在共享 GPT-4 生成的数据，用于构建具有监督学习和强化学习的指令遵循 LLM。

* [akoksal/LongForm](https://github.com/akoksal/LongForm) 使用语料库提取生成长文本的指令调优数据集和模型。通过利用英语语料库示例和增强指令创建的。从现有的语料库（如C4和维基百科）中选择一组多样化的人类编写的文档，并通过LLM为给定的文档生成指令。然后，用结构化的语料库示例（如Stack Exchange和WikiHow）和任务示例（如问答，电子邮件写作，语法错误更正，故事/诗歌生成和文本摘要）来扩展这些示例。

* [BelleGroup/train_3.5M_CN](https://huggingface.co/datasets/BelleGroup/train_3.5M_CN) 约350万条由BELLE项目生成的中文指令数据。

* [BelleGroup/train_2M_CN](https://huggingface.co/datasets/BelleGroup/train_2M_CN) 约200万条由BELLE项目生成的中文指令数据。

* [BelleGroup/train_1M_CN](https://huggingface.co/datasets/BelleGroup/train_1M_CN) 约100万条由BELLE项目生成的中文指令数据。

* [BelleGroup/train_0.5M_CN](https://huggingface.co/datasets/BelleGroup/train_0.5M_CN) 约50万条由BELLE项目生成的中文指令数据。

* [BelleGroup/generated_chat_0.4M](https://huggingface.co/datasets/BelleGroup/generated_chat_0.4M) 包含约40万条由BELLE项目生成的个性化角色对话数据，包含角色介绍。

* [BelleGroup/school_math_0.25M](https://huggingface.co/datasets/BelleGroup/school_math_0.25M) 包含约25万条由BELLE项目生成的中文数学题数据，包含解题过程。

* [juletxara/mgsm](https://huggingface.co/datasets/juletxara/mgsm) 多语言小学数学基准（MGSM）是小学数学问题的基准。8.5K高质量语言多样化的小学数学单词问题的数据集。创建该数据集是为了支持对需要多步骤推理的基本数学问题进行问答的任务。

* [XueFuzhao/InstructionWild](https://github.com/XueFuzhao/InstructionWild)  InstructWild v2，其中包括超过 110K 个基于用户的高质量指令。我们没有使用自导来生成任何指令。我们还用指令类型和特殊标签标记这些指令的子集。

* [sunzeyeah/chinese_chatgpt_corpus](https://huggingface.co/datasets/sunzeyeah/chinese_chatgpt_corpus) 该存储库收集了用于监督微调（SFT）和来自人类反馈的强化学习（RLHF）的中文语料库。

* [PlexPt/chatgpt-corpus](https://github.com/PlexPt/chatgpt-corpus) ChatGPT 中文语料库 对话语料 小说语料 客服语料 用于训练大模型

* [zxbsmk/webnovel_cn](https://huggingface.co/datasets/zxbsmk/webnovel_cn) 从12560本网文提取的约21.7M条可用于训练小说生成的中文指令数据

* [QingyiSi/Alpaca-CoT](https://huggingface.co/datasets/QingyiSi/Alpaca-CoT) 该存储库将不断收集各种指令调优数据集。并且我们将不同的数据集标准化为相同的格式，可以直接通过羊驼模型的代码加载。

* [datasets/BAAI/COIG](https://huggingface.co/datasets/BAAI/COIG) 中文开放教学通才（COIG）项目来维护一套无害、有用和多样化的中文教学语料库。[BAAI-Zlab/COIG](https://github.com/BAAI-Zlab/COIG)

* [CLUEbenchmark/pCLUE](https://github.com/CLUEbenchmark/pCLUE) 基于提示的大规模预训练数据集，用于多任务学习和零样本学习，120万训练数据。

* [FreedomIntelligence/Huatuo-26M](https://github.com/FreedomIntelligence/Huatuo-26M) 规模最大的中国医学质量保证数据集：包含 26，000，000 个问答对。

* [liyucheng/zhihu_rlhf_3k](https://huggingface.co/datasets/liyucheng/zhihu_rlhf_3k) 知乎3000个用于RLHF（Reinforcement Learning from Human Feedback 基于人类反馈的强化学习）的数据

* [X-PLUG/CValues](https://github.com/X-PLUG/CValues) 面向中文大模型价值观的评估与对齐研究。邀请中国知名专家学者，每位专家提出100个诱导偏见、歧视回答的刁钻问题，并对大模型的回答进行标注。项目吸引了环境科学、心理学、法理学等多个领域专家参与，并召开了专家研讨会，会后发布业内首个大语言模型治理开源中文数据集100PoisonMpts，包含专家提出的问题、专家自己撰写或认可的答案。

* [DA-southampton/RedGPT](https://github.com/DA-southampton/RedGPT)  提出一种自动生成事实型对话的方法，并公开我们的部分数据。我们公开的第一批数据（RedGPT-Dataset-V1-CN）共包含5万条中文多轮对话。目标是自动生成海量、高质量、事实型多轮对话，用于训练GPT，提升GPT的事实正确性。我们采用如下方法自动生成数据。1. 采集优质的事实型文档，我们称之为reference，其来源可以是电子书、维基百科、优质垂类网站。文档需要涵盖尽量多的主题，包括但不限于人物、机构、科技、医疗、法律、人文、经济、家居、汽车、出行、美食、时尚、体育、教育、宠物。2. 利用已有的LLM（例如付费API）生成多轮对话。输入是一篇reference，prompt类似“请根据这篇文章生成多轮问答”。API会输出一段多轮对话（dialogue）。这种方法将原本只适合预训练的文档转化成可供微调的多轮对话。3. 第2步收集到大量的reference-dialogue二元组。将reference和prompt作为输入，dialogue作为目标，微调一个GPT模型（可以基于LLaMA或BLOOM的预训练基座）。我们将微调出的模型称作Reference-Enlightened-Dialogue GPT，缩写RedGPT。有了RedGPT，即可基于reference生成多轮对话，获得海量的数据。

* [X-PLUG/ChatPLUG](https://github.com/X-PLUG/ChatPLUG) 旨在建立和共享一个中文开放域对话系统。在推理过程中集成外部知识是灵活的，这是一个可选的输入。您可以利用 获取最新信息或使用本地知识库获取 search engine 领域知识。通过设置 bot profiles 或使用 role-paly instructions 来自定义对话和字符的样式很容易。它通过多轮对话展示了其在开放领域对话方面的熟练程度，同时也在广泛的 NLP 任务上表现出色 multi-task abilities 。

* [chathub-dev/chathub](https://github.com/chathub-dev/chathub) 多合一的聊天机器人客户端。在一个应用程序中使用不同的聊天机器人，目前支持ChatGPT，新的Bing Chat，Google Bard，Claude和10 +开源模型，包括Alpaca，Vicuna，ChatGLM等。

* [go-skynet/LocalAI](https://github.com/go-skynet/LocalAI) 自托管、社区驱动、本地 OpenAI 兼容 API。在消费级硬件上运行LLM的OpenAI的直接替代品。免费的开源OpenAI替代品。LocalAI是一个运行ggml兼容模型的API：llama，gpt4all，rwkv，whisper，vicuna，koala，gpt4all-j，cerebras，falcon，dolly，starcoder和许多其他

* [sunner/ChatALL](https://github.com/sunner/ChatALL) 同时与ChatGPT，Bing Chat，Bard，Alpaca，Vicuna，Claude，ChatGLM，MOSS，讯飞星火，文心一言等聊天，发现最佳答案

* [li-plus/chatglm.cpp](https://github.com/li-plus/chatglm.cpp) C++实现ChatGLM-6B和ChatGLM2-6B，以便在MacBook上进行实时聊天。

* [ztxz16/fastllm](https://github.com/ztxz16/fastllm/) 纯c++的全平台llm加速库，支持python调用，chatglm-6B级模型单卡可达10000+token / s，支持glm, llama, moss基座，手机端流畅运行

* [gventuri/pandas-ai](https://github.com/gventuri/pandas-ai) Python库，它将生成人工智能功能集成到Pandas中，使数据帧成为对话式的。为流行的数据分析和操作工具pandas添加了生成AI功能。

* [howl-anderson/unlocking-the-power-of-llms](https://github.com/howl-anderson/unlocking-the-power-of-llms) 使用 Prompts 和 Chains 让 ChatGPT 成为神奇的生产力工具

* [eugeneyan/open-llms](https://github.com/eugeneyan/open-llms) 可用于商业用途的开放LLM列表。

* [Mooler0410/LLMsPracticalGuide](https://github.com/Mooler0410/LLMsPracticalGuide) LLM实用指南资源的精选列表。它基于我们的调查论文：在实践中利用LLM的力量：关于ChatGPT及其他的调查。该调查部分基于本博客的后半部分。我们还构建了现代大型语言模型（LLM）的进化树，以追踪近年来语言模型的发展，并重点介绍一些最著名的模型。

* [imaurer/awesome-decentralized-llm](https://github.com/imaurer/awesome-decentralized-llm) LLM资源的集合，可用于构建您可以“拥有”的产品或进行可重复的研究。

* [Open LLM Leaderboard ](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) 开放LLM排行榜旨在跟踪，排名和评估LLM和聊天机器人的发布。

* [botpress/botpress](https://github.com/botpress/botpress) 由 OpenAI 提供支持的下一代聊天机器人和助手的终极平台。开始以闪电般的速度为您的项目或业务构建令人难以置信的助手。

* [dice2o/BingGPT](https://github.com/dice2o/BingGPT) 新必应AI聊天的桌面应用程序（Windows，macOS和Linux）

* [josStorer/chatGPTBox](https://github.com/josStorer/chatGPTBox) 将 ChatGPT 深度集成到您的浏览器中，您需要的一切都在这里

* [lss233/chatgpt-mirai-qq-bot](https://github.com/lss233/chatgpt-mirai-qq-bot) 一键部署！真正的 AI 聊天机器人！支持ChatGPT、文心一言、讯飞星火、Bing、Bard、ChatGLM、POE，多账号，人设调教，虚拟女仆、图片渲染、语音发送 | 支持 QQ、Telegram、Discord、微信 等平台

* [promptslab/Promptify](https://github.com/promptslab/Promptify) 使用 LLM 解决 NLP 问题，并使用 Promptify 轻松为流行的生成模型（如 GPT、PaLM 等）生成不同的 NLP 任务提示

* [salesforce/CodeT5](https://github.com/salesforce/CodeT5) CodeT5的主页：用于代码理解和生成的开放代码LLM

* [enricoros/big-agi](https://github.com/enricoros/big-agi) 由 GPT-4 及更高版本提供支持的个人 AI 应用程序，具有 AI 角色、AGI 功能、文本到图像、语音、响应流、代码突出显示和执行、PDF 导入、开发人员预设等等。使用Next.js，React，Joy。

* [jaymody/picoGPT](https://github.com/jaymody/picoGPT) NumPy实现的一个不必要的微小的GPT-2。40 行代码。

* [zurawiki/gptcommit](https://github.com/zurawiki/gptcommit) 一个 git prepare-commit-msg 钩子，用于使用 GPT-3 创作提交消息。使用此工具，您可以轻松生成清晰、全面和描述性的提交消息，让您专注于编写代码。

* [bentoml/OpenLLM](https://github.com/bentoml/OpenLLM) 用于在生产中操作大型语言模型 （LLM） 的开放平台。轻松微调、服务、部署和监控任何 LLM。

* [karpathy/llama2.c](https://github.com/karpathy/llama2.c) 在一个纯 C 文件中推理Llama 2大型语言模型

* [geekan/MetaGPT](https://github.com/geekan/MetaGPT)  多代理框架：给定一行需求，返回 PRD、设计、任务、存储库。为 GPT 分配不同的角色，以形成用于复杂任务的协作软件实体。

* [ModelTC/lightllm](https://github.com/ModelTC/lightllm) 基于Python的LLM（大型语言模型）推理和服务框架，以其轻量级设计，易于扩展和高速性能而著称。LightLLM利用了许多备受推崇的开源实现的优势，包括但不限于FasterTransformer，TGI，vLLM和FlashAttention。

* [PanQiWei/AutoGPTQ](https://github.com/PanQiWei/AutoGPTQ) 一个易于使用的LLM量化包，带有用户友好的API，基于GPTQ算法。

* [princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm) 正式实现“思想之树：用大语言模型刻意解决问题”

* [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) 快速轻松地将尖端的LLM技术集成到您的应用程序中。将OpenAI，Azure OpenAI和Hugging Face等大型语言模型（LLM）与C#，Python和Java等传统编程语言集成在一起。语义内核通过允许您定义可以在几行代码中链接在一起的插件来实现这一点。

* [thomas-yanxin/LangChain-ChatGLM-Webui](https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui) 基于LangChain和ChatGLM-6B等系列LLM的针对本地知识库的自动问答

* [ssbuild/chatglm_finetuning](https://github.com/ssbuild/chatglm_finetuning) Chatglm 6b微调和羊驼微调

* [liucongg/ChatGLM-Finetuning](https://github.com/liucongg/ChatGLM-Finetuning) 基于ChatGLM-6B、ChatGLM2-6B模型，进行下游具体任务微调，涉及Freeze、Lora、P-tuning、全参微调等

* [HqWu-HITCS/Awesome-Chinese-LLM](https://github.com/HqWu-HITCS/Awesome-Chinese-LLM) 整理开源的中文大语言模型，以规模较小、可私有化部署、训练成本较低的模型为主，包括底座模型，垂直领域微调及应用，数据集与教程等。

* [ OpenGVLab/Ask-Anything](https://github.com/OpenGVLab/Ask-Anything) [视频聊天GPT]聊天GPT与视频理解！还有更多支持的LM，如miniGPT4，StableLM和MOSS。

* [OpenMotionLab/MotionGPT](https://github.com/OpenMotionLab/MotionGPT) 一个统一且用户友好的运动语言模型，用于学习两种模态的语义耦合，并在多个运动任务上生成高质量的运动和文本描述。

* [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) 大型语言模型（LLM）已经席卷了NLP社区AI社区的整个世界。以下是关于大型语言模型的精选论文列表，尤其是与 ChatGPT 相关的论文。它还包含LLM培训框架，部署LLM的工具，有关LLM的课程和教程以及所有公开可用的LLM检查点和API。

* [DSXiangLi/DecryptPrompt](https://github.com/DSXiangLi/DecryptPrompt) 总结Prompt&LLM论文，开源数据&模型，AIGC应用

* [catqaq/ChatPiXiu](https://github.com/catqaq/ChatPiXiu) 开源chatgpt替代方案/实现的调查，复制和领域/任务适应。

* [DAMO-NLP-SG/LLM-Zoo](https://github.com/DAMO-NLP-SG/LLM-Zoo) 本项目收集了以下各种开源和闭源LLM的信息

* [wgwang/LLMs-In-China](https://github.com/wgwang/LLMs-In-China) 旨在记录中国大模型发展情况

* [OpenBMB/BMList](https://github.com/OpenBMB/BMList) 希望使用此列表来显示大模型的最新趋势。

* [nichtdax/awesome-totally-open-chatgpt](https://github.com/nichtdax/awesome-totally-open-chatgpt) ChatGPT 的完全开放的替代品列表

* [ikaijua/Awesome-AITools](https://github.com/ikaijua/Awesome-AITools) 收藏AI相关的实用工具，大型语言模型

* [mckaywrigley/ai-code-translator](https://github.com/mckaywrigley/ai-code-translator) 使用 AI 将代码从一种语言翻译成另一种语言。

* [datawhalechina/prompt-engineering-for-developers](https://github.com/datawhalechina/prompt-engineering-for-developers) 面向开发者的 LLM 入门教程，吴恩达大模型系列课程中文版

* [datawhalechina/hugging-llm](https://github.com/datawhalechina/hugging-llm) 拥抱LLM，拥抱未来。介绍 ChatGPT 原理、使用和应用，降低使用门槛，让更多感兴趣的非NLP或算法专业人士能够无障碍使用LLM创造价值。

* [promptingguide.ai/zh](https://www.promptingguide.ai/zh) 提示工程（Prompt Engineering）是一门较新的学科，关注提示词开发和优化，帮助用户将大语言模型（Large Language Model, LLM）用于各场景和研究领域。 掌握了提示工程相关技能将有助于用户更好地了解大型语言模型的能力和局限性。基于对大语言模型的浓厚兴趣，我们编写了这份全新的提示工程指南，介绍了大语言模型相关的论文研究、学习指南、模型、讲座、参考资料、大语言模型能力以及与其他与提示工程相关的工具。

* [phodal/aigc](https://github.com/phodal/aigc) 《构筑大语言模型应用：应用开发与架构设计》一本关于 LLM 在真实世界应用的开源电子书，介绍了大语言模型的基础知识和应用，以及如何构建自己的模型。其中包括Prompt的编写、开发和管理，探索最好的大语言模型能带来什么，以及LLM应用开发的模式和架构设计。

* [km1994/LLMsNineStoryDemonTower](https://github.com/km1994/LLMsNineStoryDemonTower) 分享 LLMs在自然语言处理（ChatGLM、Chinese-LLaMA-Alpaca、小羊驼 Vicuna、LLaMA、GPT4ALL等）、信息检索（langchain）、语言合成、语言识别、多模态等领域（Stable Diffusion、MiniGPT-4、VisualGLM-6B、Ziya-Visual等）等 实战与经验。

* [iguodongiot/llm-action](https://github.com/liguodongiot/llm-action) 本项目旨在分享大模型相关技术原理以及实战经验。

* [hiyouga/LLaMA-Efficient-Tuning](https://github.com/hiyouga/LLaMA-Efficient-Tuning) 易于使用的LLM微调框架（LLaMA-2，BLOOM，Falcon，Baichuan，Qwen，ChatGLM2）

* [FlagOpen/FlagEval](https://github.com/FlagOpen/FlagEval) AI大型基础模型的评估工具包。我们的目标是探索和整合科学、公平、开放的基础模型评估基准、方法和工具。FlagEval将在未来支持在不同模态（如NLP，音频，CV和多模态）中/跨基础模型的多维评估（如准确性，效率，鲁棒性等）。我们希望通过对基础模型的评估，加深对基础模型的理解，促进相关的技术创新和产业化应用。

* [InternLM/opencompass](https://github.com/InternLM/opencompass) LLM评估平台，支持超过50 +数据集的各种模型（LLaMA，LLaMa2，ChatGLM2，ChatGPT，Claude等）。

* [OpenLMLab/GAOKAO-Bench](https://github.com/OpenLMLab/GAOKAO-Bench) 一个评估框架，利用高考问题作为数据集来评估大型语言模型。

* [mikegu721/xiezhibenchmark](https://github.com/mikegu721/xiezhibenchmark) 獬豸是语言模型（LMs）的综合评估套件。它由249587道多项选择题组成，涵盖 516 个不同的学科和四个难度级别。希望可以帮助开发人员跟踪进度并分析其LM的重要优势/缺点。

* [haonan-li/CMMLU](https://github.com/haonan-li/CMMLU) 综合性的中文评估基准，专门用于评估语言模型在中文语境下的知识和推理能力。CMMLU涵盖了从基础学科到高级专业水平的67个主题。它包括：需要计算和推理的自然科学，需要知识的人文科学和社会科学,以及需要生活常识的中国驾驶规则等。此外，CMMLU中的许多任务具有中国特定的答案，可能在其他地区或语言中并不普遍适用。因此是一个完全中国化的中文测试基准。

* [Felixgithub2017/MMCU](https://github.com/Felixgithub2017/MMCU) 本评测只是对大模型语义理解能力的测试，并不能代表模型的全面能力评测，评测结果仅供参考。整个评测方式、评测数据集、评测记录都公开，确保可以复现。

* [jeinlee1991/chinese-llm-benchmark](https://github.com/jeinlee1991/chinese-llm-benchmark) 中文大模型能力评测榜单：覆盖文心一言、chatgpt、通义千问、讯飞星火、belle / chatglm 等开源大模型，多维度能力评测。不仅提供能力评分排行榜，也提供所有模型的原始输出结果！

* [thu-coai/Safety-Prompts](https://github.com/thu-coai/Safety-Prompts) 中文安全prompts，评估和提升大模型的安全性。

* [SCIR-HI/Huatuo-Llama-Med-Chinese](https://github.com/SCIR-HI/Huatuo-Llama-Med-Chinese) 本草（原名：华驼）模型仓库，基于中文医学知识的大语言模型指令微调

* [michael-wzhu/PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE) 面向医学领域多任务少样本学习的中文大规模指令调优数据集

* [UCSD-AI4H/Medical-Dialogue-System](https://github.com/UCSD-AI4H/Medical-Dialogue-System) 包含医生和患者之间的对话（中文）。它有 110 万次对话和 400 万条话语。数据在不断增长，并将添加更多对话。原始对话来自 haodf.com。数据的所有版权均属于 haodf.com。

* [lemuria-wchen/imcs21](https://github.com/lemuria-wchen/imcs21)  IMCS-21 的新语料库基准，用于自动医疗咨询系统

* [中文医疗信息处理评测基准CBLUE_数据集-阿里云天池](https://tianchi.aliyun.com/dataset/95414) 中国中文信息学会医疗健康与生物信息处理专业委员会在合法开放共享的理念下发起，由阿里云天池平台承办，并由医渡云、腾讯天衍、平安医疗、阿里夸克、北京、郑州、鹏城实验室、哈工大(深圳）、同济、中山、复旦、华东师范等开展智慧医疗研究的单位共同协办，旨在推动中文医学NLP技术和社区的发展。

* [shibing624/MedicalGPT](https://github.com/shibing624/MedicalGPT) 训练医疗大模型，实现包括二次预训练、有监督微调、奖励建模、强化学习训练。

* [WangRongsheng/XrayGLM](https://github.com/WangRongsheng/XrayGLM) 首个会看胸部X光片的中文多模态医学大模型

* [WangRongsheng/CareLlama](https://github.com/WangRongsheng/CareLlama) 医疗大语言模型，同时它集合了数十个公开可用的医疗微调数据集和开放可用的医疗大语言模型以促进医疗LLM快速发展。

* [michael-wzhu/ChatMed](https://github.com/michael-wzhu/ChatMed) 中文医疗大模型，善于在线回答患者/用户的日常医疗相关问题

* [michael-wzhu/ShenNong-TCM-LLM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) “神农”大模型，首个中医药中文大模型.

* [michaelwzhu/ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset) 中医药指令数据集

* [michaelwzhu/ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset) 来自于互联网上的医疗问诊问题(11W)，反映了真实世界的不同用户/患者的医疗问诊需求。目前response都是由OpenAI GPT-3.5引擎回答的。后续会对互联网上的医生回答与患者回答进行筛选甄别，择优选择，构建质量更优的数据集。

* [CMKRG/QiZhenGPT](https://github.com/CMKRG/QiZhenGPT) 利用[启真医学知识库](http://www.mk-base.com/)构建的中文医学指令数据集，并基于此在Chinese-LLaMA-Plus-7B、CaMA-13B、ChatGLM-6B模型上进行指令精调，大幅提高了模型在中文医疗场景下效果，首先针对药品知识问答发布了评测数据集，后续计划优化疾病、手术、检验等方面的问答效果，并针对医患问答、病历自动生成等应用展开拓展。

* [scutcyr/BianQue](https://github.com/scutcyr/BianQue) 中文医疗对话模型扁鹊(BianQue)。实际的医生与用户交谈往往会存在“医生根据用户当前的描述进行持续多轮的询问”。并且医生在最后根据用户提供的信息综合给出建议，如下图所示。我们把医生不断问询的过程定义为 询问链（CoQ, Chain of Questioning） ，当模型处于询问链阶段，其下一个问题通常由对话上下文历史决定。结合当前开源的中文医疗问答数据集（MedDialog-CN、IMCS-V2、CHIP-MDCFNPC、MedDG、cMedQA2、Chinese-medical-dialogue-data），分析其中的单轮/多轮特性以及医生问询特性，结合实验室长期自建的生活空间健康对话大数据，构建了千万级别规模的扁鹊健康大数据BianQueCorpus。对话数据通过“病人：xxx\n医生：xxx\n病人：xxx\n医生：”的形式统一为一种指令格式，训练数据当中混合了大量target文本为医生问询的内容而非直接的建议，这将有助于提升AI模型的问询能力。基于扁鹊健康大数据BianQueCorpus，我们选择了 ChatGLM-6B 作为初始化模型，经过全量参数的指令微调训练得到了新一代BianQue2.0。扩充了药品说明书指令、医学百科知识指令以及ChatGPT蒸馏指令等数据，强化了模型的建议与知识查询能力。[BianQue - a Hugging Face Space by scutcyr](https://huggingface.co/spaces/scutcyr/BianQue)

* [liaokongVFX/LangChain-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)  LangChain 的中文入门教程

* [thomas-yanxin/Sunsimiao](https://github.com/thomas-yanxin/Sunsimiao)  孙思邈中文医疗大模型 ：提供安全、可靠、普惠的中文医疗大模型

* [scutcyr/SoulChat](https://github.com/scutcyr/SoulChat) 中文领域心理健康对话大模型

* [lyogavin/Anima](https://github.com/lyogavin/Anima) 第一个开源的基于QLoRA的33B中文大语言模型。基于QLoRA开源的33B guanaco训练了10000 steps。训练使用一个H100 GPU。

* [PKU-YuanGroup/ChatLaw](https://github.com/PKU-YuanGroup/ChatLaw) 中文法律大模型。目前开源的仅供学术参考的版本底座为姜子牙-13B、Anima-33B，我们使用大量法律新闻、法律论坛、法条、司法解释、法律咨询、法考题、判决文书等原始文本来构造对话数据。

* [AndrewZhe/lawyer-llama](https://github.com/AndrewZhe/lawyer-llama)  中文法律LLaMA，在大规模法律语料上进行了continual pretraining，让它系统的学习中国的法律知识体系。 在此基础上，我们借助ChatGPT收集了一批对中国国家统一法律职业资格考试客观题（以下简称法考）的分析和对法律咨询的回答，利用收集到的数据对模型进行指令微调，让模型习得将法律知识应用到具体场景中的能力。

* [CSHaitao/LexiLaw](https://github.com/CSHaitao/LexiLaw) 经过微调的中文法律大模型，它基于 ChatGLM-6B 架构，通过在法律领域的数据集上进行微调，使其在提供法律咨询和支持方面具备更高的性能和专业性。

* [LiuHC0428/LAW-GPT](https://github.com/LiuHC0428/LAW-GPT) 中文法律对话语言模型，由ChatGLM-6B LoRA 16-bit指令微调得到。数据集包括现有的法律问答数据集和基于法条和真实案例指导的self-Instruct构建的高质量法律文本问答，提高了通用语言大模型在法律领域的表现，提高了模型回答的可靠性和专业程度。

* [siat-nlp/HanFei](https://github.com/siat-nlp/HanFei) 国内首个全参数训练的法律大模型 HanFei-1.0 韩非

* [davidpig/lychee_law](https://github.com/davidpig/lychee_law) 律知, 法律咨询大模型，Law-GLM-10B: 基于 GLM-10B 模型, 在 30GB 中文法律数据上进行指令微调.

* [HIT-SCIR-SC/QiaoBan](https://github.com/HIT-SCIR-SC/QiaoBan) 中文儿童情感陪伴大模型“巧板”。基于通用大模型，使用了通用域人机对话数据、单轮指令数据以及儿童情感陪伴对话数据进行指令微调，训练得到，是通用大语言模型迁移至儿童情感陪伴领域的一次成功实践。三大特点：首先，基于情绪辅导理论构建的儿童情感陪伴对话数据，能够更有效地守护孩子的心理健康。其次，具有儿童心理学背景的志愿者与专家参与完成高质量对话数据的收集。使得能够更加准确地理解和回应儿童的需求，真正与他们建立深入的情感连接。最后，模型与儿童的交互方式更加贴心，让他们能够感受到温暖和认同，成为他们坚实成长道路上的得力伙伴。

* [gmftbyGMFTBY/science-llm](https://github.com/gmftbyGMFTBY/science-llm) 科学领域的大规模语言模型，在redpajama arXiv上训练

* [IMOSR/MediaGPT](https://github.com/IMOSR/MediaGPT) 中文的自媒体大语言模型MediaGPT(曾用名Media LLaMA)

* [THUDM/CodeGeeX](https://github.com/THUDM/CodeGeeX)  一个具有130亿个参数的大型多语言代码生成模型，在20多种语言的大型代码语料库上进行了预训练。

* [ymcui/Chinese-LLaMA-Alpaca-2](https://github.com/ymcui/Chinese-LLaMA-Alpaca-2)  中文 LLaMA-2 & Alpaca-2 大模型二期项目 + 本地CPU/GPU训练部署 (Chinese LLaMA-2 & Alpaca-2 LLMs)

* [FlagAlpha/Llama2-Chinese](https://github.com/FlagAlpha/Llama2-Chinese) Llama中文社区，最好的中文Llama大模型，完全开源可商用

* [CVI-SZU/Linly](https://github.com/CVI-SZU/Linly) 提供中文对话模型 Linly-ChatFlow 、中文基础模型 Chinese-LLaMA (1-2)、Chinese-Falcon 及其训练数据。中文基础模型以 LLaMA 和 Falcon 为底座，使用中文和中英平行语料进行增量预训练，将其在英文上的语言能力扩展到中文上。公开的多语言指令数据，对中文模型进行大规模指令跟随训练，实现了 Linly-ChatFlow。此外，本项目开源了从头训练的 Linly-OpenLLaMA 模型，包含 3B、7B、13B 规模，在 1TB 中英文语料上进行预训练，针对中文优化了字词结合tokenizer。

* [OpenBMB/CPM-Bee](https://github.com/OpenBMB/CPM-Bee) 一个完全开源、允许商用的百亿参数中英文基座模型，也是CPM-Live训练的第二个里程碑。它采用Transformer自回归架构（auto-regressive），在超万亿（trillion）高质量语料上进行预训练，拥有强大的基础能力。开发者和研究者可以在CPM-Bee基座模型的基础上在各类场景进行适配来以创建特定领域的应用模型。

* [OpenBMB/VisCPM](https://github.com/OpenBMB/VisCPM) 基于CPM基础模型的中英双语多模态大模型系列。支持面向图像进行中英双语多模态对话。该模型使用Muffin视觉编码架构，使用CPM-Bee（10B）作为语言基座模型，并通过语言建模训练目标融合视觉和语言模型。模型训练包括预训练和指令精调两阶段：`1.预训练`：我们使用约100M高质量英文图文对数据对VisCPM-Chat进行了预训练，数据包括CC3M、CC12M、COCO、Visual Genome、Laion等。在预训练阶段，语言模型参数保持固定，仅更新视觉编码器的参数，以支持大规模视觉-语言表示的高效对齐。`2.指令精调`：采用LLaVA-150K英文指令精调数据，并混合相应翻译后的中文数据对模型进行指令精调，以对齐模型多模态基础能力和用户使用意图。在指令精调阶段，更新全部模型参数，以提升指令精调数据的利用效率。有趣的是，发现即使仅采用英文指令数据进行指令精调，模型也可以理解中文问题，但仅能用英文回答。表明模型的多语言多模态能力已得到良好泛化。在指令精调阶段进一步加入少量中文翻译数据，可以将模型回复语言和用户问题语言对齐。

* [zjunlp/KnowLM](https://github.com/zjunlp/KnowLM) 一个开源的知识渊博的大型语言模型框架。以知识和大模型为中心，利用构建的中英文预训练语料库，对LLaMA等大型模型进行全面预训练。基于KG2Instructions的技术，优化了包括NER、RE和IE在内的知识提取任务，可以使用人工指令完成。

* [zjunlp/KnowLM-IE · Datasets at Hugging Face](https://huggingface.co/datasets/zjunlp/KnowLM-IE) 基于知识图谱构建的，提取实体关系三元组的指令数据集

* [ictnlp/BayLing](https://github.com/ictnlp/BayLing) “百聆”是基于LLaMA的对齐增强的英语/中文大语言模型，具有优越的中英文能力，在多语言和通用任务等测试中取得ChatGPT 90%的性能。

* [AtomEcho/AtomGPT](https://github.com/AtomEcho/AtomGPT) 基于LLaMA的模型架构，从0开始训练，希望能在训练的过程中，将模型能力得到提升的进化过程展示出来，感受到模型学习的过程。

* [FMInference/FlexGen](https://github.com/FMInference/FlexGen) 在单个 GPU 上运行大型语言模型，以实现面向吞吐量的方案。

* [bigscience-workshop/petals](https://github.com/bigscience-workshop/petals) 在家运行LLM，BitTorrent风格。微调和推理速度比卸载快10 倍。Petals协作运行像Llama和BLOOM这样的大型语言模型 - 你加载模型的一小部分，然后加入为其他部分提供服务的人来运行推理或微调。

### 文本生成、文本对话

* [Awesome-TOD-NLG-Survey](https://github.com/yizhen20133868/Awesome-TOD-NLG-Survey) 面向任务的对话系统 (TOD) 中自然语言生成的调查：最新进展和新前沿

* [openai/gpt-2](https://github.com/openai/gpt-2) 论文“语言模型是无监督的多任务学习者”中的代码和模型。

* [karpathy/minGPT](https://github.com/karpathy/minGPT) OpenAI GPT（生成预训练转换器）训练的最小 PyTorch 重新实现

* [XiangLi1999/PrefixTuning](https://github.com/XiangLi1999/PrefixTuning)  前缀微调：优化文本生成的连续提示模板。提出一种更好的微调方法，通过加入前缀实现统一模型在不同任务上的微调，实现小样本学习，极大地减少了参数量。目前对于前缀的构造，大致可以分为本文的连续前缀和离散前缀（自动生成或手动设计），对于在摘要任务上加入离散前缀，有点类似于从对话中提取特征或结构，但这种方法的优势就在于它不需要大量的样本，而传统的融入结构的方法仍然需要很多样本。

* [RUCAIBox/TextBox](https://github.com/RUCAIBox/TextBox) 基于Python和PyTorch开发的，用于在一个统一的、全面的、高效的框架中复现和开发文本生成算法，主要面向研究者使用。我们的库包括16种文本生成算法，涵盖了两个主要任务：无条件（无输入）生成、序列到序列（Seq2Seq）生成，包括机器翻译和摘要生成。模型 无条件：LSTMVAE    (Bowman et al., 2016)、CNNVAE (Yang et al., 2017)、HybridVAE    (Semeniuta et al., 2017)、SeqGAN    (Yu et al., 2017)、TextGAN (Zhang et al., 2017)、RankGAN    (Lin et al., 2017)、MaliGAN (Che et al., 2017)、LeakGAN (Guo et al., 2018)、MaskGAN    (Fedus et al., 2018)。序列到序列 RNN (Sutskever et al., 2014)、Transformer    (Vaswani et al., 2017b)、GPT-2 (Radford et al.)、XLNet (Yang et al., 2019)、BERT2BERT (Rothe et al., 2020)、BART（Lewis et al。，2020）

* [BART](https://github.com/pytorch/fairseq/tree/master/examples/bart) Bidirectional and Auto-Regressive Transformers 是以去噪为预训练目标训练的序列间模型， 一种符合生成任务的预训练方法。我们证明了这种预训练目标更为通用，并且证明了我们可以在SQuAD和GLUE上匹配RoBERTa的结果，并在摘要（XSum，CNN数据集）、长形式生成性问答（ELI5）和对话-反应生成（ConvAI2）上获得最新的结果。在生成任务上显著高于BERT, UniLM, XLNet, RoBERTa等模型

* [fastnlp/CPT](https://github.com/fastnlp/CPT) 中文预训练非平衡转换器 (CPT) ，它是一种非平衡 Transformer 编码器-解码器，联合 MLM 和 DAE 进行预训练。用于汉语理解和生成的预训练.

* [songhaoyu/BoB](https://github.com/songhaoyu/BoB) BERTOverBERT用于从有限的个性化数据训练基于角色的对话模型。分解为了两个子任务，从有限的角色化对话数据中进行学习。

* [YunwenTechnology/QueryGeneration](https://github.com/YunwenTechnology/QueryGeneration) 智能扩充机器人的“标准问”库之Query生成

* [beyondguo/genius](https://github.com/beyondguo/genius) 强大的有条件文本生成模型，以草稿为输入，在给定的草稿(文本范围、短语或单词的关键信息)中填充缺失的上下文，在大规模文本语料库上进行预训练，用一种极端和选择性的掩蔽策略从草稿目标进行新的重建，使它能够生成给定素描的多样化和高质量的文本。

* [imcaspar/gpt2-ml](https://github.com/imcaspar/gpt2-ml) GPT2 多语言支持, 15亿参数中文预训练模型

* [EleutherAI/gpt-neo](https://github.com/EleutherAI/gpt-neo) 模型并行GPT2和类似GPT3的模型的实现，能够使用mesh-tensorflow库扩展到完整的GPT3尺寸（甚至可能更多！）。

* [rikdz/GraphWriter](https://github.com/rikdz/GraphWriter) 基于图Transformer从知识图谱中生成文本

* [liucongg/GPT2-NewsTitle](https://github.com/liucongg/GPT2-NewsTitle) GPT2.带有超级详细注释的中文GPT2新闻标题生成项目。

* [ZhuiyiTechnology/t5-pegasus](https://github.com/ZhuiyiTechnology/t5-pegasus) 中文生成式预训练模型，以mT5为基础架构和初始权重，通过类似PEGASUS的方式进行预训练。

* [google-research/text-to-text-transfer-transformer](https://github.com/google-research/text-to-text-transfer-transformer) T5的理念就是“万事皆可 Seq2Seq”，它使用了标准的 Encoder-Decoder 模型，并且构建了无监督/有监督的文本生成预训练任务，最终将效果推向了一个新高度。

* [google-research/multilingual-t5](https://github.com/google-research/multilingual-t5) T5 的多国语言版

* [Morizeyao/GPT2-Chinese](https://github.com/Morizeyao/GPT2-Chinese) GPT2中文文生模型，包括散文、诗词、对联、通用中文、中文歌词、文言文

* [bojone/t5_in_bert4keras](https://github.com/bojone/t5_in_bert4keras) 在keras中使用T5模型 ,用mT5 small版本finetune出来的 CSL 标题生成模型，BLEU 指标能持平基于 WoBERT 的 UniLM 模型，并且解码速度快 130%；而用 mT5  base 版本 finetune 出来的 CSL 标题生成模型，指标能超过基于 WoBERT 的 UniLM 模型 1% 以上，并且解码速度也能快 60%。

* [PENS-Personalized-News-Headline-Generation](https://github.com/LLluoling/PENS-Personalized-News-Headline-Generation) 新闻头条生成数据集和通用框架

* [Aristotle609/Medium-Title-Generator](https://github.com/Aristotle609/Medium-Title-Generator) 生成数据科学文章标题的模型

* [yangjianxin1/GPT2-chitchat](https://github.com/yangjianxin1/GPT2-chitchat) 用于中文闲聊的GPT2文本对话模型

* [RUCAIBox/MVP](https://github.com/RUCAIBox/MVP) 自然语言生成的多任务监督预训练。遵循标准的转换器编码器-解码器架构。使用标记数据集进行监督预训练。还具有特定于任务的软提示，以刺激模型执行特定任务的能力。专为自然语言生成而设计，可以适应各种生成任务。我们的模型也可以适应自然语言理解任务。收集了7种代表性生成任务的45个有标签数据集，共计3200千万条样本（23GB），来作为预训练语料。第一阶段，使用这些语料训练一个标准的Transformer，即MVP；第二阶段，冻结住MVP，利用每个任务的数据训练任务特定的连续型提示（即7组提示）。

* [RUCAIBox/Context-Tuning](https://github.com/RUCAIBox/Context-Tuning) 上下文调优：学习上下文提示用于自然语言生成

* [samueldobbie/markup](https://github.com/samueldobbie/markup) 基于Web的文档注释工具，由GPT-3  提供支持

* [deeppavlov/DeepPavlov](https://github.com/deeppavlov/DeepPavlov) 用于深度学习端到端对话系统和聊天机器人的开源库。

## 文本匹配 文本相似度

* [princeton-nlp/SimCSE](https://github.com/princeton-nlp/SimCSE) SimCSE：句子嵌入的简单对比学习 。提供无监督或有监督的对比学习。是目前文本相似度更好的方法。

* [UKPLab/sentence-transformers](https://github.com/UKPLab/sentence-transformers) 句子转换器：使用BERT RoBERTa XLM-RoBERTa＆Co.和PyTorch的多语言句子嵌入

* [bojone/CoSENT](https://github.com/bojone/CoSENT) 比Sentence-BERT更有效的句向量方案.优化cos值的新方案**CoSENT**（Cosine Sentence）。[实验显示](https://kexue.fm/archives/8847)，CoSENT在收敛速度和最终效果上普遍都比InferSent和Sentence-BERT要好。

* [shawroad/CoSENT](https://github.com/shawroad/CoSENT_Pytorch) 比Sentence-BERT更有效的句向量方案 Pytorch版

* [shuxinyin/SimCSE-Pytorch](https://github.com/shuxinyin/SimCSE-Pytorch) 中文SimCSE+ESimCSE的无监督 + 有监督实现

* [wangyuxinwhy/uniem](https://github.com/wangyuxinwhy/uniem) 统一嵌入模型，目标是创建中文最好的通用文本嵌入模型。202306发布 [M3E models](https://huggingface.co/moka-ai/m3e-base) ，在中文文本分类和文本检索上均优于 openai text-embedding-ada-002。

* [thunlp/OpenMatch](https://github.com/thunlp/OpenMatch) 总体架构包括两大部分：一是相关文档检索，即根据用户检索词，从大规模文档集合中返回最相关的Top-K(K通常为100或1000)文档。二是文档重排序，即将各神经网络模型和非神经网络模型的排序特征整合，对Top-K文档重排序，进一步提升排序效果。OpenMatch提供了融合外部知识图谱信息的知识增强模型，和筛选大规模数据的数据增强模型。

* [NTMC-Community/MatchZoo-py](https://github.com/NTMC-Community/MatchZoo-py) 通用的文本匹配工具包，旨在方便大家快速的实现、比较、以及分享最新的深度文本匹配模型。MatchZoo 的 PyTorch 版本。

* [voidism/DiffCSE](https://github.com/voidism/DiffCSE) 用于学习句子嵌入的无监督对比学习框架。DiffCSE学习对原始句子和编辑句子之间的差异敏感的句子嵌入，其中编辑的句子是通过随机屏蔽原始句子，然后从屏蔽语言模型中采样来获得的。我们表明 DiffSCE 是等变对比学习的一个实例（Dangovski 等人，2021 年），它概括了对比学习并学习对某些类型的增强不敏感而对其他“有害”类型的增强敏感的表征。我们的实验表明，DiffCSE在无监督句子表示学习方法中取得了最先进的结果，在语义文本相似性任务上比SimCSE高出2.3个绝对点。

* [shibing624/text2vec](https://github.com/shibing624/text2vec) 文本向量表征工具，把文本转化为向量矩阵，实现了Word2Vec、RankBM25、Sentence-BERT、CoSENT等文本表征、文本相似度计算模型，开箱即用。

* [terrifyzhao/text_matching](https://github.com/terrifyzhao/text_matching) 常用文本匹配模型tf版本，数据集为QA_corpus模型:DSSM ConvNet ESIM ABCNN BiMPM DIIN DRCN

* [Brokenwind/BertSimilarity](https://github.com/Brokenwind/BertSimilarity) 基于Google的BERT模型来进行语义相似度计算。

* [bohanli/BERT-flow](https://github.com/bohanli/BERT-flow) 基于流式生成模型，将BERT的表示可逆地映射到一个均匀的空间，文本表示、语义文本相似性任务的SOTA。

* [DataTerminatorX/Keyword-BERT](https://github.com/DataTerminatorX/Keyword-BERT) 带关键词的BERT语义匹配

* [bojone/BERT-whitening](https://github.com/bojone/BERT-whitening) 简单的向量白化改善句向量质量，可以媲美甚至超过BERT-flow的效果。

* [autoliuweijie/BERT-whitening-pytorch](https://github.com/autoliuweijie/BERT-whitening-pytorch) Pytorch version of BERT-whitening

* [nilboy/gaic_track3_pair_sim](https://github.com/nilboy/gaic_track3_pair_sim) 短文本语义匹配，2021年全球人工智能技术创新大赛-赛道三-冠军方案

* [yym6472/ConSERT](https://github.com/yym6472/ConSERT) 基于对比学习的句子语义表示迁移框架。包含三部分，数据增强，BERT 编码层，对比损失层。

* [amazon-research/sccl](https://github.com/amazon-research/sccl) 利用对比学习促进更好地基于距离的短文本聚类实现。

* [ZhuiyiTechnology/roformer-sim](https://github.com/ZhuiyiTechnology/roformer-sim) 融合检索和生成的RoFormer-Sim模型.应用于相似句生成、相似句扩增、语义相似度问题。

* [allenai/macaw](https://github.com/allenai/macaw) Macaw（Multi-angle c(q)uestion answering 多角度 c(q) 问题回答）是一种即用型模型，能够进行一般问题回答，在训练的领域之外表现出稳健性。 它以“多角度”方式进行了训练，这意味着它可以处理一组灵活的输入和输出“槽”（如问题、答案、解释）。Macaw 建立在 T5 之上，有不同的尺寸：macaw-11b、macaw-3b 和 macaw-large，以及各种排行榜上的以答案为重点的版本：macaw-answer-11b。

* [Decem-Y/sohu_text_matching_Rank2](https://github.com/Decem-Y/sohu_text_matching_Rank2) 2021搜狐校园文本匹配算法大赛Top2。使用了预训练模型（如NEZHA、MacBert、ROBERTA、ERNIE等），设计了选择了两种技术路线（通过[SEP]拼接source与target作为输入、类似SBERT的句子向量编码比较），并尝试多种上分策略（在给定语料上继续mlm预训练、focal loss损失函数、不同的pooling策略、加入TextCNN、fgm对抗训练、数据增强等）。选取多组差异较大的模型的输出，通过投票的方式进行集成，得到最好成绩。

* [shuxinyin/SimCSE-Pytorch](https://github.com/shuxinyin/SimCSE-Pytorch) 中文数据集下SimCSE+ESimCSE的实现

* [wakafengfan/simcse-pytorch](https://github.com/wakafengfan/simcse-pytorch) pytorch版simcse无监督语义相似模型

* [bojone/SimCSE](https://github.com/bojone/SimCSE) SimCSE在中文任务上的简单实验

* [yangjianxin1/SimCSE](https://github.com/yangjianxin1/SimCSE) SimCSE有监督与无监督实验复现 一种简单但是很巧妙的NLP对比学习方法，创新性地引入Dropout的方式，对样本添加噪声，从而达到对正样本增强的目的。 该框架的训练目的为：对于batch中的每个样本，拉近其与正样本之间的距离，拉远其与负样本之间的距离，使得模型能够在大规模无监督语料（也可以使用有监督的语料）中学习到文本相似关系。

* [vdogmcgee/SimCSE-Chinese-Pytorch](https://github.com/vdogmcgee/SimCSE-Chinese-Pytorch) SimCSE在中文上的复现，有监督+无监督

* [GeekDream-x/SemEval2022-Task8-TonyX](https://github.com/GeekDream-x/SemEval2022-Task8-TonyX)  在 Semeval-2022 Task8 —— Multilingual News Article Similarity 中提供了我们获胜系统的实现。这是一项关于评估多语言和跨语言新闻文章相似性的竞赛，涵盖 18 个语言对。

* [JohnGiorgi/DeCLUTR](https://github.com/JohnGiorgi/DeCLUTR)  无监督文本表示的深度对比学习

* [huggingface/setfit](https://github.com/huggingface/setfit) 使用 Sentence Transformers 进行高效的少样本学习. 高效且无提示的框架，用于对句子转换器进行少量微调。 它用很少的标记数据实现了高精度，特点：没有提示或语言表达器：当前的少量微调技术需要手工提示或语言表达器将示例转换为适合底层语言模型的格式。 SetFit 通过直接从文本示例生成丰富的嵌入来完全免除提示。训练速度快、多语言。

* [epidemic-sentence-pair](https://github.com/zzy99/epidemic-sentence-pair) 新冠疫情相似句对判定大赛 线上第一名方案。BERT模型融合、数据对称扩充、数据传递扩充、对抗训练、伪标签。

* [KKenny0/sohu2021](https://github.com/KKenny0/sohu2021) 2021搜狐校园文本匹配算法大赛方案，基于BERT的交互模型，通过BERT来得到source-target pair的向量表示。任务：短短、短长和长长文本匹配。

## 机器阅读理解

* [imClumsyPanda/langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM) 利用 [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) + [langchain](https://github.com/hwchase17/langchain) 实现的基于本地知识的 ChatGLM 应用。建立了全部基于开源模型实现的本地知识问答应用。

* [l15y/wenda](https://github.com/l15y/wenda) 闻达：一个LLM调用平台。目前支持chatGLM-6B、chatRWKV、chatYuan和chatGLM-6B模型下自建知识库查找。

* [GanymedeNil/document.ai](https://github.com/GanymedeNil/document.ai) 基于向量数据库与GPT3.5的通用本地知识库方案

* [basketballandlearn/MRC_Competition_Dureader](https://github.com/basketballandlearn/MRC_Competition_Dureader) 基于大规模MRC数据再训练的机器阅读理解预训练模型（包括roberta-wwm-large、macbert-large），可以使用[transformers库](https://huggingface.co/luhua/chinese_pretrain_mrc_roberta_wwm_ext_large)。

* [wptoux/albert-chinese-large-webqa](https://github.com/wptoux/albert-chinese-large-webqa) 基于百度webqa与dureader数据集训练的Albert Large QA模型

* [bojone/dgcnn_for_reading_comprehension](https://github.com/bojone/dgcnn_for_reading_comprehension) 基于膨胀门卷积的阅读理解式问答模型（Keras实现）

* [cooelf/AwesomeMRC](https://github.com/cooelf/AwesomeMRC) 对MRC的研究摘要和参考资料

* [nlpdata/c3](https://github.com/nlpdata/c3) 中文机器阅读理解数据集 multiple-Choice Chinese machine reading Comprehension dataset.

* [qiufengyuyi/event_extraction](https://github.com/qiufengyuyi/event_extraction) 百度aistudio事件抽取比赛 使用机器阅读理解来尝试解决。

* [liuhuanyong/MiningZhiDaoQACorpus](https://github.com/liuhuanyong/MiningZhiDaoQACorpus) 百度知道问答语料库，包括超过580万的问题，938万的答案，5800个分类标签。基于该问答语料库，可支持多种应用，如闲聊问答，逻辑挖掘。

* [xv44586/ccf_2020_qa_match](https://github.com/xv44586/ccf_2020_qa_match) CCF2020问答匹配比赛 任务是：给定IM交流片段，片段包含一个客户问题以及随后的经纪人若干IM消息，从随后的经纪人消息中找出一个是对客户问题的回答。

* [lgw863/LogiQA-dataset](https://github.com/lgw863/LogiQA-dataset) 数据集包含8,678个QA实例

* [HIT-SCIR/Molweni](https://github.com/HIT-SCIR/Molweni) 提出了构建于多人对话的英文机器阅读理解（MRC）数据集—Molweni，并覆盖了对话语篇结构。Molweni源自于Ubuntu聊天语料库，包括10,000个对话，共计88,303条话语（utterance）。我们共标注了30,066个问题，包括可回答和不可回答的问题。Molweni独特地为其多人对话提供了语篇结构信息，共标注了78,245个语篇关系实例，为多人对话语篇结构分析（Discourse  parsing）贡献了大规模数据。

* [danqi/acl2020-openqa-tutorial](https://github.com/danqi/acl2020-openqa-tutorial) 本教程对开放域问答 (QA) 的前沿研究进行了概述，QA 是使用大量不同主题的文档来回答问题的任务。首先简要介绍历史背景，讨论研究问题的基本设置和核心技术挑战，然后描述具有通用评估指标和基准的现代数据集。然后，是在开放域QA中提出的前沿模型，包括两阶段检索器-阅读器方法、密集检索器和端到端训练以及无检索器方法。最后，介绍使用文本和大型知识库的混合方法，并以重要的开放性问题结束本教程。

* [zhoujx4/DuReader-Checklist-BASELINE](https://github.com/zhoujx4/DuReader-Checklist-BASELINE) 百度2021年语言与智能技术竞赛机器阅读理解torch版baseline

* [google-research/tapas](https://github.com/google-research/tapas) 端到端的神经表格文本理解模型。表格 QA 模型。

* [PaddlePaddle/RocketQA](https://github.com/PaddlePaddle/RocketQA) 信息检索和问答的密集检索，包括中英文最先进的模型。

## 知识图谱问答KBQA、多跳推理

* [RUCAIBox/KBQAPapers](https://github.com/RUCAIBox/KBQAPapers) 知识图谱问答KBQA论文集

* [shijx12/TransferNet](https://github.com/shijx12/TransferNet) An Effective and Transparent Framework for Multi-hop Question Answering over Relation Graph 多跳问题解答关系图的有效透明框架，通过每一跳都预测当前关系得分，并更新实体得分，直到最大跳数。预测该问题的跳数，按跳数的概率加权每一跳得分作为实体的最终得分。

* [malllabiisc/EmbedKGQA](https://github.com/malllabiisc/EmbedKGQA) 基于知识图谱嵌入的链路预测处理多跳问答。首先训练实体嵌入，随后利用实体嵌入学习问题嵌入，预测时对所有实体，构建(head entity, question)并评分，并选择评分最高的头实体作为答案。能很好地处理知识图谱中的不完整和稀疏的问题。

* [BDBC-KG-NLP/QA-Survey](https://github.com/BDBC-KG-NLP/QA-Survey) 北航大数据高精尖中心研究张日崇团队对问答系统的总结。包括基于知识图谱的问答（KBQA），基于文本的问答系统（TextQA），基于表格的问答系统（TabletQA）和基于视觉的问答系统（VisualQA），每类系统分别对学术界和工业界进行总结。

* [xianghuisun/Chinese_KGQA](https://github.com/xianghuisun/Chinese_KGQA) 实现基于知识图谱的中文问答系统

* https://github.com/cdjhz/multigen Language Generation with Multi-hop Reasoning on Commonsense Knowledge Graph 基于常识知识图的多跳推理语言生成 本研究关注一类条件文本生成任务，即给定输入源文本X，目标是生成一段目标文本 Y。研究员们额外增加了一个知识图谱 G=(V,E) 的输入为模型在生成时提供常识知识的信息。

* https://github.com/INK-USC/MHGRN 基于知识库的多跳关系推理 本篇文章提出了multi-hop relational reasoning module（多跳关系推理模型）叫做MHGRN多跳推理网络。该模型在额外的多跳知识图谱中抽取的子网络中进行推理。本文提出的方法将已有的基于路径的常识推理以及GCN融合在了一起，并在CommonsenseQA和OpenbookQA上取得了良好的效果。

* https://github.com/lanyunshi/Multi-hopComplexKBQA 查询图生成，用于回答知识库中的多跳复杂问题.提出了一种改进的分阶段查询图生成方法，该方法具有更灵活的生成查询图的方式。在查询图生成的每一步，包含三种预定义的操作：扩展、连接、聚合。

* https://github.com/nju-websoft/SPARQA 基于知识库的问题解答,提出了一种新颖的骨架语法来表示一个复杂问题的高级结构。骨架语法本质上是依赖语法的一个选定子集，用于专门表示复杂问题的高级结构。这种专用的粗粒度表示形式由于其简单性而可能具有准确的解析算法，有助于提高下游细粒度语义解析的准确性。

* https://github.com/mori97/JKNet-dgl 跳跃知识网络的dgl实现

* https://github.com/THUDM/CogQA 基于认知图谱实现多跳阅读.从人类的认知过程中受到启发。双过程理论认为，我们的大脑思考过程由两套系统构成: System1 和 System 2。System 1: 我们的大脑首先通过System 1隐式的、无意识的和凭借直觉的过程来检索相关信息。System 2: 在System 1过程的基础上，再进行一个显式的、有意识的、可控的推理过程，即System 2。作者使用BERT模型构建System 1，使用GNN模型构建System 2。

* https://github.com/michiyasunaga/qagnn GNN 在融合 QA 上下文与 KG 的一个尝试，在问答任务上相比现有的预训练语言模型、以及预训练 +KG 模型，都有不小的提升。同时，使用 attention-base GNN，能够可视化知识图谱中节点之间的注意力关系，有助于提高 QA 可解释性和结构化推理的能力。

* https://github.com/WenRichard/KBQA-BERT 基于知识图谱的问答系统，BERT做命名实体识别和句子相似度，分为online和outline模式

* https://github.com/RichardHGL/WSDM2021_NSM KBQA 的神经状态机器 ComplexWebQuestions

* [UKPLab/coling2018-graph-neural-networks-question-answering](https://github.com/UKPLab/coling2018-graph-neural-networks-question-answering) 用门图形神经网络建模语义，用于知识库问题解答

* [https://github.com/THU-KEG/KoPL](https://github.com/THU-KEG/KoPL) KoPL全称 Knowledge oriented Programing Language, 是一个为复杂推理问答而设计的编程语言。可以将自然语言问题表示为由基本函数组合而成的KoPL程序，程序运行的结果就是问题的答案。目前，KoPL的27个基本函数覆盖对多种知识元素（如概念、实体、关系、属性、修饰符等）的操作，并支持多种问题类型（如计数、事实验证、比较等）的查询。KoPL提供透明的复杂问题推理过程，易于理解和使用。KoPL面向知识库、文本等不同形式的知识资源，可扩展性强。

* [PaddlePaddle/PGL/erniesage](https://github.com/PaddlePaddle/PGL/tree/static_stable/examples/erniesage) 使用PGL实现ERNIESage。在很多工业应用中，往往出现如下图所示的一种特殊的图：Text Graph。顾名思义，图的节点属性由文本构成，而边的构建提供了结构信息。如搜索场景下的Text Graph，节点可由搜索词、网页标题、网页正文来表达，用户反馈和超链信息则可构成边关系。ERNIESage 由PGL团队提出，是ERNIE SAmple aggreGatE的简称，该模型可以同时建模文本语义与图结构信息，有效提升 Text Graph 的应用效果。其中 ERNIE 是百度推出的基于知识增强的持续学习语义理解框架。ERNIESage 是 ERNIE 与 GraphSAGE 碰撞的结果，是 ERNIE SAmple aggreGatE 的简称，它的结构如下图所示，主要思想是通过 ERNIE 作为聚合函数（Aggregators），建模自身和邻居节点的语义与结构关系。ERNIESage 对于文本的建模是构建在邻居聚合的阶段，中心节点文本会与所有邻居节点文本进行拼接；然后通过预训练的 ERNIE 模型进行消息汇聚，捕捉中心节点以及邻居节点之间的相互关系；最后使用 ERNIESage 搭配独特的邻居互相看不见的 Attention Mask 和独立的 Position Embedding 体系，就可以轻松构建TextGraph中句子之间以及词之间的关系。使用ID特征的GraphSAGE只能够建模图的结构信息，而单独的ERNIE只能处理文本信息。通过PGL搭建的图与文本的桥梁，ERNIESage能很简单的把GraphSAGE以及ERNIE的优点结合一起。TextGraph场景，效果能够比单独的ERNIE以及GraphSAGE都要好。

* [BshoterJ/awesome-kgqa](https://github.com/BshoterJ/awesome-kgqa) 知识图谱问答部分资料合集

* [RUCKBReasoning/SubgraphRetrievalKBQA](https://github.com/RUCKBReasoning/SubgraphRetrievalKBQA) 多跳知识库问答子图检索增强模型的pytorch实现 WebQuestionSP CWQ

* [google-research/smore](https://github.com/google-research/smore) 多功能的框架，它可以在KG上扩展多跳查询嵌入。SMORE可以轻松地在Freebase KG上训练查询嵌入，在一台机器上拥有超过8600万个节点和33800万条边。

## 知识图谱

* [CLUEbenchmark/KgCLUE](https://github.com/CLUEbenchmark/KgCLUE) KgCLUE: 大规模中文开源知识图谱问答数据集。实体数量 3121457，关系数量 245838，高频关系(>100) 3833，三元组数量 20559652，知识库来源于百科类数据，由百科类搜索的事实性三元组构成。

* [autoliuweijie/K-BERT](https://github.com/autoliuweijie/K-BERT) Enabling Language Representation with Knowledge Graph ，已被AAAI2020所录取，是较早的考虑将知识图谱中的边关系引入预训练模型的论文。主要通过修改Transformer中的attention机制，通过特殊的mask方法将知识图谱中的相关边考虑到编码过程中，进而增强预训练模型的效果。

* [npubird/KnowledgeGraphCourse](https://github.com/npubird/KnowledgeGraphCourse) 东南大学《知识图谱》研究生课程

* [AutoML-Research/AutoSF](https://github.com/AutoML-Research/AutoSF) 用于知识图谱学习的双线性评分函数（SFs）搜索。知识图(KG)是一种以实体为节点、以关系为边的特殊图结构，对数据挖掘和机器学习都很重要，并启发了各种下游应用，如结构化搜索、问答、推荐。在KGs中，每条边都被表示为一个具有形式(头实体、关系、尾实体)的三元组，表示为(h, r, t)，一个基本问题是如何量化三元组(h, r, t)s的合理性。KG嵌入(KGE)是近年来出现并发展起来的一种很有前途的方法。基本上，给定一组观察到的三元组，KGE试图学习实体和关系的低维向量表示，以便三元组的可信性能够被量化。得分函数(SF)根据嵌入值返回(h, r, t)的分数，用于度量可信性。SF一般是人为设计和选择的，对嵌入的质量有显著影响。

* [THU-KEG/KEPLER](https://github.com/THU-KEG/KEPLER) 主要通过添加类似于TransE的预训练机制来增强对应文本的表示，进而增强预训练模型在一些知识图谱有关任务的效果。

* [txsun1997/CoLAKE](https://github.com/txsun1997/CoLAKE) 使用知识图谱以增强预训练模型的效果 首先将上下文看作全连接图，并根据句子中的实体在KG上抽取子图，通过两个图中共现的实体将全连接图和KG子图融合起来；最终本文将文本上下文和知识上下文一起用MLM进行预训练，将mask的范围推广到word、entity和relation；为训练该模型，本文采用cpu-gpu混合训练策略结合负采样机制减少训练时间；最终本文提出的方法在知识图谱补全和若干NLP任务上均带来了增益。然后本文将该图转化为序列，使用Transformer进行预训练，并在训练时采用特殊的type embedding来表示实体、词语与其他子图信息

* [JanKalo/KnowlyBERT](https://github.com/JanKalo/KnowlyBERT) 提出了一种混合的语言知识模型查询系统，该系统使用语言模型来应对现实世界中知识图谱的不完整性问题。作为KnowlyBERT的输入，用户可以向系统提出以实体为中心的SPARQL查询。首先，查询语言模型（a）；然后，对不完整的知识图谱进行查询，并获得结果（b）；另外SPARQL查询被翻译成多种自然语言语句，这些语言语句在“关系模板生成”步骤中由语言模型完成；语言模型返回多个单词列表以及每个单词（c）的置信度值；然后将这些列表合并为一个列表（d），并根据知识图谱类型信息（e）使用我们的语义过滤步骤进行过滤。此外，执行阈值处理，削减不相关的结果（f）；将语言模型和知识图谱的结果合并（g）并返回给用户。

* [yeliu918/KG-BART](https://github.com/yeliu918/KG-BART) 知识图谱增强的预训练模型的生成式常识推理.可利用图上的注意力来聚集丰富的概念语义，从而增强对看不见的概念集的模型泛化。

* [bernhard2202/intkb](https://github.com/bernhard2202/intkb) 一种交互式知识图谱补全框架

* [husthuke/awesome-knowledge-graph](https://github.com/husthuke/awesome-knowledge-graph) 整理知识图谱相关学习资料

* [wangbo9719/StAR_KGC](https://github.com/wangbo9719/StAR_KGC) Structure-Augmented Text Representation Learning for Efficient Knowledge Graph Completion 结构增强文本表示学习，实现高效知识图完成.知识图谱补全

* [Everglow123/MAKG](https://github.com/Everglow123/MAKG)  移动app知识图谱

* [openconcept](http://openkg.cn/dataset/openconcept) 基于自动化知识抽取算法的大规模中文概念图谱。440万概念核心实体，以及5万概念和1200万实体-概念三元组。数据包括了常见的人物、地点等通用实体。

* [ OpenKG-ORG/OpenEA](https://github.com/openkg-org/OpenEA) 基于知识图谱嵌入的开源实体融合工具。本体匹配、实体对齐、真值验证、冲突消解。

* [seukgcode/MELBench.](https://github.com/seukgcode/MELBench) 多模态实体链接 (MEL) 旨在利用多模态信息将提及项映射到知识库中定义的相应实体。 我们发布了三个 MEL 数据集：Weibo-MEL、Wikidata-MEL 和 Richpedia-MEL，分别包含来自社交媒体、百科全书和多模态知识图谱的 25,602、18,880 和 17,806 个样本。

* [OpenKG-ORG/OpenRichpedia](https://github.com/OpenKG-ORG/OpenRichpedia) 东南大学多模态知识图谱-OpenRichpedia工程文件

* [csdqa](http://openkg.cn/dataset/csdqa)  计算机科学领域示意图问答数据集

* [HKUST-KnowComp/FKGE](https://github.com/HKUST-KnowComp/FKGE) 差异私有联合知识图嵌入

* [totogo/awesome-knowledge-graph](https://github.com/totogo/awesome-knowledge-graph) 知识图相关学习材料、数据库、工具和其他资源的精选列表

* [BrambleXu/knowledge-graph-learning](https://github.com/BrambleXu/knowledge-graph-learning) 精选的知识图谱教程、项目社区列表。

* [liuhuanyong/PersonGraphDataSet](https://github.com/liuhuanyong/PersonGraphDataSet) 人物图谱数据集，近十万的人物关系图谱事实数据库，通过人物关系抽取算法抽取+人工整理得出，可用于人物关系搜索、查询、人物关系多跳问答，以及人物关系推理等场景提供基础数据。

* [husthuke/awesome-knowledge-graph](https://github.com/husthuke/awesome-knowledge-graph) 整理知识图谱相关学习资料

* [ownthink/KnowledgeGraph](https://github.com/ownthink/KnowledgeGraph) 史上最大规模1.4亿知识图谱数据免费下载，知识图谱，通用知识图谱，融合了两千五百多万实体，拥有亿级别的实体属性关系。

* [liuhuanyong/AbstractKnowledgeGraph](https://github.com/liuhuanyong/AbstractKnowledgeGraph) 抽象知识图谱，目前规模50万，支持名词性实体、状态性描述、事件性动作进行抽象。目标于抽象知识，包括抽象实体，抽象动作，抽象事件。基于该知识图谱，可以进行不同层级的实体抽象和动作抽象，这与人类真实高度概括的认知是一致的。

* [songjiang0909/awesome-knowledge-graph-construction](https://github.com/songjiang0909/awesome-knowledge-graph-construction) 很棒的知识图构建

* [ZihengZZH/awesome-multimodal-knowledge-graph](https://github.com/ZihengZZH/awesome-multimodal-knowledge-graph) 多模态知识图谱的精彩阅读列表或其他资源（数据集、教程等）。

* [thunlp/KB2E](https://github.com/thunlp/KB2E) 知识图谱嵌入，包括 TransE、TransH、TransR 和 PTransE

* [powerycy/DeepKg: Knowledge Graph](https://github.com/powerycy/DeepKg) 知识图谱的构建 实体识别\语义标准化\向量召回

* [zjunlp/deepke](https://github.com/zjunlp/deepke) 基于深度学习的开源中文知识图谱抽取框架，支持cnSchema、低资源、长篇章、多模态的知识抽取工具，可以基于PyTorch实现命名实体识别、关系抽取和属性抽取功能。

* [面向事件时序因果关系识别的17类开源标注数据集总结](https://mp.weixin.qq.com/s/uz3IfX4CyxtJjJl-HRkMaA)

* [iuhuanyong/TextGrapher](https://github.com/liuhuanyong/TextGrapher) 输入一篇文档，将文档进行关键信息提取，进行结构化，并最终组织成图谱组织形式，形成对文章语义信息的图谱化展示。 采用了高频词，关键词，命名实体识别，主谓宾短语识别等抽取方式，并尝试将三类信息进行图谱组织表示，这种表示方式是一种尝试。

* [liuhuanyong/ChainKnowledgeGraph](https://github.com/liuhuanyong/ChainKnowledgeGraph) 产业链知识图谱包括A股上市公司、行业和产品共3类实体，包括上市公司所属行业关系、行业上级关系、产品上游原材料关系、产品下游产品关系、公司主营产品、产品小类共6大类。 上市公司4,654家，行业511个，产品95,559条、上游材料56,824条，上级行业480条，下游产品390条，产品小类52,937条，所属行业3,946条。

* [zjukg/NeuralKG](https://github.com/zjukg/NeuralKG) 支持多种知识图谱表示学习/知识图谱嵌入（Knowledge Graph Embedding）模型的Python工具包，其中实现了多种传统知识图谱嵌入、基于图神经网络的知识图谱嵌入以及基于规则的知识图谱嵌入方法。

* [zjunlp/DeepKE](https://github.com/zjunlp/DeepKE/blob/main/README_CN.md) 开源知识图谱抽取与构建工具，支持cnSchema、低资源、长篇章、多模态的知识抽取工具，基于PyTorch实现命名实体识别、关系抽取和属性抽取功能。

* [migalkin/NodePiece](https://github.com/migalkin/NodePiece) 大型知识图谱的复合和参数高效表示 （ICLR'22）。NodePiece是一个“分词器”，用于减少知识图中的实体词汇量。不是将每个节点浅层嵌入到向量中，而是首先在其关系上下文中通过 K 个锚节点和 M 关系类型“标记”每个节点。然后，通过任何注入函数（例如MLP或Transformer）对生成的哈希序列进行编码。NodePiece可以使用相同的锚点和关系词汇表标记附加到所见图的看不见的节点，这允许NodePiece在归纳设置中使用经典KG完成中的所有众所周知的评分函数（如TransE或RotatE）开箱即用。NodePiece在OGB WikiKG 2排行榜上名列前茅，以大幅降低的参数预算（7M与500-1500M）为模型提供动力。当前配置只需要 20K 个锚节点，而不是学习 2.5M 实体嵌入。关系预测\节点分类\样本外链路预测

* [liuhuanyong/ChineseSemanticKB](https://github.com/liuhuanyong/ChineseSemanticKB) 面向中文处理的12类、百万规模的语义常用词典，包括34万抽象语义库、34万反义语义库、43万同义语义库等，可支持句子扩展、转写、事件抽象与泛化等多种应用场景。

* [lemonhu/stock-knowledge-graph](https://github.com/lemonhu/stock-knowledge-graph) 利用网络公开数据构建一个小型证券知识图谱

* [OpenBGBenchmark/OpenBG](https://github.com/OpenBGBenchmark/OpenBG) 大规模开放业务知识图谱.开放的商业知识图，它使用统一的Schema覆盖大规模的多模态数据集，包含了浙江大学ZJUKG实验室和阿里巴巴知识引擎团队提供的数百万个产品和消费者需求。

* [DeqingYang/CKBC](https://github.com/DeqingYang/CKBC) 使用关系图注意力网络和预训练语言模型完成常识知识库。常识在各种语料库中很少被明确表达，但对于机器理解自然语言非常有用。与传统的知识库（KG）不同，常识库（CKG）中的节点通常由自由格式的文本表示，并且比传统的 KG 规模更大，更稀疏。因此，这对传统的知识库补全（KBC）方法造成了挑战。

* [JavaStudenttwo/ccks_kg](https://github.com/JavaStudenttwo/ccks_kg) ccks2020基于本体的金融知识图谱自动化构建技术评测第五名方法总结

## NLP语料和数据集

* [thu-coai/CrossWOZ](https://github.com/thu-coai/CrossWOZ) 中文跨域任务导向对话数据集.它包含5个领域的6K对话会话和102K语音，包括酒店，餐厅，景点，地铁和出租车。

* [goto456/stopwords](https://github.com/goto456/stopwords) 中文常用停用词表

* [chatopera/Synonyms](https://github.com/chatopera/Synonyms) 用于自然语言处理和理解的中文同义词。

* [RUCAIBox/TG-ReDial](https://github.com/RUCAIBox/TG-ReDial) 电影领域的对话推荐数据集TG-ReDial (Recommendation through Topic-Guided Dialog)。包含1万个完整对话和近13万条语句，加入了话题线索以实现将用户引导至推荐场景这一语义的自然转移，并采用半自动的方式构建，保留了用户真实的个性化信息（如交互历史，偏好主题），使得人工标注过程更加合理可控。

* [fighting41love/funNLP](https://github.com/fighting41love/funNLP) NLP民工的乐园: 中英文敏感词、语言检测、中外手机/电话归属/运营商查询、名字推断性别、手机号抽取、身份证抽取、邮箱抽取、中日文人名库、中文缩写库、拆字词典、词汇情感值、停用词、反动词表、暴恐词表、繁简转换、英文模拟中文发音、汪峰歌词生成器、职业名称词库、同义词库、反义词库、否定词库、汽车品牌词库、汽车零件、连续英文切割、各种中文词向量、公司大全、古诗、IT、财经、成语、地名、历史名人、诗词、医学、饮食、法律、汽车、动物词库、中文聊天语料、中文谣言数据、百度中文问答数据集、句子相似度、bert资源、文本生成&摘要相关工具、cocoNLP信息抽取、国内电话号码正则匹配、清华中英文跨语言百科知识图谱

* [brightmart/nlp_chinese_corpus](https://github.com/brightmart/nlp_chinese_corpus) 大规模中文自然语言处理语料 维基百科json版(wiki2019zh) 新闻语料json版(news2016zh) 百科类问答json版(baike2018qa) 社区问答json版(webtext2019zh) ：大规模高质量数据集 翻译语料(translation2019zh)

* [msra-nlc/ChineseKBQA](https://github.com/msra-nlc/ChineseKBQA) NLPCC-ICCPOL 2016 Shared Task: Open Domain Chinese Question Answering [开放域中文问答数据集](http://tcci.ccf.org.cn/conference/2016/pages/page05_evadata.html)

* [jkszw2014/bert-kbqa-NLPCC2017](https://github.com/jkszw2014/bert-kbqa-NLPCC2017) A trial of kbqa based on bert for NLPCC2016/2017 Task 5 (基于BERT的中文知识库问答实践）

* [wavewangyue/NLPCC-MH](https://github.com/wavewangyue/NLPCC-MH)  中文多跳问答数据集 基于 NLPCC 所包含的单跳问题，通过扩充问句内容的方式，构建了专注多跳问题的中文 KBQA 数据集

* [BERT-CCPoem](https://thunlp.oss-cn-qingdao.aliyuncs.com/BERT_CCPoem_v1.zip) 是完全基于一个囊括了几乎所有中国古典诗词的语料库CCPC-Full v1.0训练而成的，该语料库共计926,024首诗词及8,933,162个诗词句子。[THUNLP-AIPoet/BERT-CCPoem](https://github.com/THUNLP-AIPoet/BERT-CCPoem) 中国古典诗词预训练模型

* [liucongg/NLPDataSet](https://github.com/liucongg/NLPDataSet) 数据集包括：DRCD、cmrc2018、chinese-squad、中医数据集、法研杯2019、莱斯杯机器阅读理解、疫情QA、WebQA、Dureader等9个数据集。

* [C-Eval 数据集](https://cevalbenchmark.com/index.html)是一个全面的中文基础模型评测数据集，涵盖了 52 个学科和四个难度的级别。

* [Gaokao](https://github.com/OpenLMLab/GAOKAO-Bench) 是一个以中国高考题作为评测大语言模型能力的数据集，用以评估模型的语言能力和逻辑推理能力。 我们只保留了其中的单项选择题，随机划分后对所有模型进行统一 `5-shot` 测试。

* [MMLU](https://arxiv.org/abs/2009.03300) 是包含 57 个多选任务的英文评测数据集，涵盖了初等数学、美国历史、计算机科学、法律等，难度覆盖高中水平到专家水平，是目前主流的LLM评测数据集。

* [microsoft/AGIEval](https://github.com/microsoft/AGIEval) 以人为本的基准，专门用于评估基础模型在与人类认知和解决问题相关的任务中的一般能力。该基准源自 20 项针对普通人类考生的官方、公共和高标准入学和资格考试，例如普通大学入学考试（例如，中国高考（高考）和美国 SAT）、法学院入学考试、数学竞赛、律师资格考试和国家公务员考试。

* [thunlp/Few-NERD](https://github.com/thunlp/Few-NERD) 一个大规模的人工标注的用于少样本命名实体识别任务的数据集。该数据集包含8种粗粒度和66种细粒度实体类型，每个实体标签均为粗粒度+细粒度的层级结构，共有18万维基百科句子，460万个词，每个词都被注释为上下文（context）或一个实体类型的一部分。

* [CLUEbenchmark/CLUECorpus2020](https://github.com/CLUEbenchmark/CLUECorpus2020) 通过对[Common Crawl](http://commoncrawl.org)的中文部分进行语料清洗，最终得到100GB的高质量中文预训练语料。实验产出的模型见：[高质量中文预训练模型，大号、超小和相似度预训练模型。](https://github.com/CLUEbenchmark/CLUEPretrainedModels)

* [esbatmop/MNBVC](https://github.com/esbatmop/MNBVC) Massive Never-ending BT Vast Chinese corpus超大规模中文语料集。对标chatGPT训练的40T数据。MNBVC数据集不但包括主流文化，也包括各个小众文化甚至火星文的数据。MNBVC数据集包括新闻、作文、小说、书籍、杂志、论文、台词、帖子、wiki、古诗、歌词、商品介绍、笑话、糗事、聊天记录等一切形式的纯文本中文数据。

* [oscar-corpus/OSCAR-2201](https://huggingface.co/datasets/oscar-corpus/OSCAR-2201)  通过使用 unoliant 架构对通用爬网语料库进行语言分类和过滤而获得的一个巨大的多语言语料库。数据以原始形式和重复数据删除形式按语言分发。

* [festvox/datasets-CMU_DoG](https://github.com/festvox/datasets-CMU_DoG) CMU 文档基础对话数据集 该数据集包含 4112 个对话，每个对话平均 21.43 轮。这使该数据集可以在生成响应的同时提供相关的聊天历史记录。

* [doc2dial/sharedtask-dialdoc2021](https://github.com/doc2dial/sharedtask-dialdoc2021) doc2dial是IBM发布的基于文档的对话数据集，包含两个任务：1）从文档中检索和问题相关的句子(information-seeking)；2）基于上一步结果生成合理答复(response generation) 数据集共有4个不同领域的480篇文档，4800个多轮对话，每个对话平均有14次交互。

* [chin-gyou/MovieChats](https://github.com/chin-gyou/MovieChats) MovieChats：在封闭域中像人类一样聊天，电影内容的聊天对话数据集

* [projects/personachat](https://github.com/facebookresearch/ParlAI/tree/master/projects/personachat)  Persona-Chat 数据集人物聊天对话数据

* [krystalan/SGSum](https://github.com/krystalan/SGSum) 一个面向体育赛事摘要的人工标注数据集

* [IceFlameWorm/NLP_Datasets](https://github.com/IceFlameWorm/NLP_Datasets)  中文NLP数据集，ATEC语义相似度学习赛数据集、CCKS 2018 微众银行智能客服问句匹配大赛数据集、ATEC + CCKS 2018 组合数据集（互金客服场景）、哈工大BQ_corpus数据集（语义相似度）、哈工大LCQMC数据集（语义相似度）。

* [nlpcc2018](http://tcci.ccf.org.cn/conference/2018/taskdata.php) 选择task7 Open Domain Question Answering，即可下载数据集。数据集包含知识图谱和问答数据

* [pkumod/CKBQA](https://github.com/pkumod/CKBQA)  ccks2018 ccks2019 包含简单问题和复杂问题的中文 KBQA 数据集。对于每个中文问题，我们都提供了黄金答案和黄金 SPARQL 查询，因此该数据集也可以应用于语义解析任务。

* [Marsan-Ma-zz/chat_corpus](https://github.com/Marsan-Ma-zz/chat_corpus) 来自各种开源的聊天语料库集合  open_subtitles
  英文电影字幕解析， movie_subtitles_cn 康奈尔电影对话语料库， 歌词_zh
  来自 PTT 论坛的歌词，witter_en 来自 twitter 的语料库（700k 行），twitter_en big更大尺寸的 twitter 语料库（5M 行）

* [rkadlec/ubuntu-ranking-dataset-creator](https://github.com/rkadlec/ubuntu-ranking-dataset-creator) 从 Ubuntu 语料库对话框中为排名任务创建训练、有效和测试数据集的脚本。

* [codemayq/chinese_chatbot_corpus](https://github.com/codemayq/chinese_chatbot_corpus) 对目前市面上已有的开源中文聊天语料的搜集和系统化整理工作。包含chatterbot、豆瓣多轮、PTT八卦语料、青云语料、电视剧对白语料、贴吧论坛回帖语料、微博语料、小黄鸡语料，共8个公开闲聊常用语料和短信，白鹭时代问答等语料。

* [NiuTrans/Classical-Modern](https://github.com/NiuTrans/Classical-Modern) 非常全的文言文（古文）-现代文平行语料

* [CLUEbenchmark/SimCLUE](https://github.com/CLUEbenchmark/SimCLUE) 大规模语义理解与匹配数据集。可用于无监督对比学习、半监督学习等构建中文领域效果最好的预训练模型。可用于语义理解、语义相似度、召回与排序等检索场景等。整合了以上9个数据集：哈工大 LCQMC 数据集、AFQMC 蚂蚁金融语义相似度数据集、OPPO 小布对话文本语义匹配数据集、北大中文文本复述数据集 PKU-Paraphrase-Bank、Chinese-STS-B 数据集、Chinese-MNLI 自然语言推理数据集、Chinese-SNLI 自然语言推理数据集、
  OCNLI 中文原版自然语言推理数据集、CINLID 成语语义推理数据集

* [GuocaiL/nlp_corpus](https://github.com/GuocaiL/nlp_corpus)  open_ner_data网上开放的ner数据集、boson数据集、clue细粒度实体识别数据集、微软实体识别数据集、人民网实体识别数据集（98年）、中药说明书实体识别数据集（“万创杯”中医药天池大数据竞赛）、视频_音乐_图书数据集、微博数据集

* [zejunwang1/CSTS:](https://github.com/zejunwang1/CSTS) 中文自然语言推理与语义相似度数据集

  - 哈工大 LCQMC 数据集
  - AFQMC 蚂蚁金融语义相似度数据集
  - OPPO 小布对话文本语义匹配数据集
  - 谷歌 PAWS-X 数据集
  - 北大中文文本复述数据集 PKU-Paraphrase-Bank
  - Chinese-STS-B 数据集
  - Chinese-MNLI 自然语言推理数据集
  - Chinese-SNLI 自然语言推理数据集
  - OCNLI 中文原版自然语言推理数据集
  - CINLID 中文成语语义推理数据集

* [sailxuOvO/CC-Riddle](https://github.com/sailxuOvO/CC-Riddle) 汉字谜语问答数据集

* [CLUEbenchmark/DataCLUE](https://github.com/CLUEbenchmark/DataCLUE) 数据为中心的NLP基准和工具包。以数据为中心（Data-centric）的AI，是一种新型的AI探索方向。它的核心问题是如何通过系统化的改造你的数据（无论是输入或者标签）来提高最终效果。 传统的AI是以模型为中心（Model-centric）的，主要考虑的问题是如何通过改造或优化模型来提高最终效果，它通常建立在一个比较固定的数据集上。 最新的数据显示超过90%的论文都是以模型为中心的，通过模型创新或学习方法改进提高效果，即使不少改进影响可能效果并不是特别明显。有些人认为当前的人工智能领域， 无论是自然语言处理（如BERT） 或计算机视觉(ResNet)， 已经存在很多成熟高效模型，并且模型可以很容易从开源网站如github获得；而与此同时，工业界实际落地 过程中可能有80%的时间用于 清洗数据、构建高质量数据集，或在迭代过程中获得更多数据，从而提升模型效果。正是看到了这种巨大的差别，在吴恩达等人的推动下这种 以数据为中心 （Data-centric）的AI进一步的系统化，并成为一个有具有巨大实用价值方法论。

* [ydli-ai/CSL](https://github.com/ydli-ai/CSL) 首个中文科学文献数据集（CSL），包含 396,209 篇中文核心期刊论文元信息 （标题、摘要、关键词、学科、门类）。CSL 数据集可以作为预训练语料，也可以构建许多NLP任务，例如文本摘要（标题预测）、 关键词生成和文本分类等。取自 [国家科技资源共享服务工程技术研究中心](https://nstr.escience.net.cn/)， 包含 2010-2020 年发表的期刊论文元信息（标题、摘要和关键词）。根据中文核心期刊目录进行筛选， 并标注学科和门类标签，分为 13 个门类（一级标签）和 67 个学科（二级标签）。 数据总量为 396,209 条。

* [pluto-junzeng/CNSD](https://github.com/pluto-junzeng/CNSD) 中文自然语言推理数据集（A large-scale Chinese Nature language inference and Semantic similarity calculation Dataset） 本数据及通过翻译加部分人工修正的方法，从英文原数据集生成，可以一定程度缓解中文自然语言推理和语义相似度计算数据集不够的问题。

* [victorsungo/MMDialog](https://github.com/victorsungo/MMDialog) 面向多模态开放域会话的大规模多轮对话数据集。

* [lupantech/ScienceQA](https://github.com/lupantech/ScienceQA) 通过思维链进行多模态推理的科学问题回答。提出了科学问答（ScienceQA），这是一个新的基准，包括21,208个多模态多项选择题，有一套不同的科学主题和注释，他们的答案与相应的讲座和解释。讲座和解释分别提供了一般的外部知识和具体的原因，以获得正确的答案。拥有更丰富的领域多样性：自然科学语言科学社会科学。ScienceQA包含26个主题、127个类别和379个技能，涵盖了广泛的领域。我们进一步设计语言模型，学习生成演讲和解释作为思维链（CoT），以模拟回答ScienceQA问题时的多跳推理过程。ScienceQA证明了CoT在语言模型中的实用性，CoT在少样例GPT-3中将问题回答性能提高了1.20%，在微调的UnifiedQA中将问题回答性能提高了3.99%。

* [benywon/ChiQA](https://github.com/benywon/ChiQA) 用于多模态理解的大规模基于图像的真实世界问答数据集。ChiQA中的问题是向搜索引擎发出的开放域用户查询。ChiQA中的图像也是从搜索引擎中收集的真实世界图像，与问题相关但不一定能回答问题。我们的数据众包包括两个阶段的主动学习过程。在第一阶段，我们从网络上随机收集样本。在第二阶段中，我们首先基于来自第一阶段的数据训练模型，然后使用训练好的模型在剩余数据上选择硬示例并继续标记。这两个阶段的设置使得数据更具挑战性，并且从本质上消除了对数据中某些属性或语言模式的不合理偏爱。

* [qkaren/Counterfactual-StoryRW](https://github.com/qkaren/Counterfactual-StoryRW) “虚构故事推理和生成”的数据集和代码

* [eecrazy/CausalBank](https://github.com/eecrazy/CausalBank) 非常大规模、开放的领域、句子级、平行的因果语料库。按照句子中出现的因果顺序分为两部分：because_mode（结果，然后是原因）和therefore_mode（原因，然后是结果）。使用预处理的英语通用爬网语料库 （5.14 TB） 中的细粒度因果模板匹配获得的，完全自动，无需任何人工注释。里面或多或少有噪音。

* [InsaneLife/ChineseNLPCorpus](https://github.com/InsaneLife/ChineseNLPCorpus) 中文自然语言处理数据集，阅读理解、任务型对话数据、文本分类、实体识别&词性标注&分词、句法&语义解析、推荐系统、百科数据、指代消歧、预训练：（词向量or模型）、中文完形填空数据集、中华古诗词数据库、保险行业语料库、汉语拆字字典。

* [pengxiao-song/awesome-chinese-legal-resources](https://github.com/pengxiao-song/awesome-chinese-legal-resources) 中国法律数据集和相关资源的精彩集合。致力于收集全面的中文法律数据源

* [xglue](https://huggingface.co/datasets/xglue) 由11个任务组成，跨越19种语言。对于每个任务，训练数据仅以英语提供。这意味着要在XGLUE上取得成功，模型必须具有强大的零镜头跨语言迁移能力，以从特定任务的英语数据中学习并将其学到的内容转移到其他语言中。与其并发工作XTREME相比，XGLUE有两个特点：首先，它同时包含跨语言NLU和跨语言NLG任务;其次，除了包括5个现有的跨语言任务（即NER，POS，MLQA，PAWS-X和XNLI）之外，XGLUE还从Bing场景中选择了6个新任务，包括新闻分类，查询广告匹配，网页排名，QA匹配，问题生成和新闻标题生成。语言、任务和任务来源的这种多样性为量化跨语言自然语言理解和生成的预训练模型的质量提供了全面的基准。

* [yhavinga/ccmatrix](https://huggingface.co/datasets/yhavinga/ccmatrix) 该语料库是使用 [CCMatrix](https://github.com/facebookresearch/LASER/tree/master/tasks/CCMatrix) 中所述的基于边缘的双文本挖掘技术从网络爬虫中提取的语言对。

* [ywjawmw/TCM_KG](https://github.com/ywjawmw/TCM_KG) 中医TCM-neo4j 知识图谱

* [ydli-ai/CSL](https://github.com/ydli-ai/CSL) 首个中文科学文献数据集（CSL），包含 396,209 篇中文核心期刊论文元信息 （标题、摘要、关键词、学科、门类）。CSL 数据集可以作为预训练语料，也可以构建许多NLP任务，例如文本摘要（标题预测）、 关键词生成和文本分类等。

## 关系抽取、信息抽取

* [roomylee/awesome-relation-extraction](https://github.com/roomylee/awesome-relation-extraction)  专门用于关系提取的精选资源列表，关系提取是自然语言处理 (NLP) 中最重要的任务之一。

* [weizhepei/CasRel](https://github.com/weizhepei/CasRel) 用于关系三重提取的新颖级联二进制标记关系抽取框架.

* [loujie0822/DeepIE](https://github.com/loujie0822/DeepIE) 基于深度学习的信息抽取技术,实体抽取\实体关系联合抽取\属性抽取\实体链接/标准化\事件抽取\摘要抽取

* [OpenKG-ORG/OpenUE](https://github.com/openkg-org/openue) 一个从文本中通用提取的开放工具包

* [universal-ie/UIE](https://github.com/universal-ie/UIE) 统一的文本到结构生成框架UIE，它可以对不同的IE任务进行统一建模，自适应地生成目标结构，并且可以从不同的知识源中学习通用的IE能力。实验结果表明，UIE在有监督和低资源环境下都取得了非常有竞争力的性能，验证了其通用性、有效性和可转移性。

* [131250208/TPlinker-joint-extraction](https://github.com/131250208/TPlinker-joint-extraction) 联合抽取模型 实体关系联合抽取标注关系抽取方案

* [bojone/GPLinker](https://github.com/bojone/GPLinker) 基于GlobalPointer的实体/关系/事件抽取

* [xhw205/GPLinker_torch](https://github.com/xhw205/GPLinker_torch) CMeIE/CBLUE/CHIP/实体关系抽取/SPO抽取

* [TanyaZhao/MRC4ERE_plus](https://github.com/TanyaZhao/MRC4ERE_plus) 基于机器阅读理解的联合实体关系提取框架

* [cuhksz-nlp/RE-TaMM](https://github.com/cuhksz-nlp/RE-TaMM) 于词依存信息类型映射记忆神经网络的关系抽取

* [PaddleNLP/DuIE](https://github.com/PaddlePaddle/PaddleNLP/tree/develop/examples/information_extraction/DuIE) LIC2021 DuIE 关系抽取基线 .信息抽取旨在从非结构化自然语言文本中提取结构化知识，如实体、关系、事件等。关系抽取的目标是对于给定的自然语言句子，根据预先定义的schema集合，抽取出所有满足schema约束的SPO三元组。schema定义了关系P以及其对应的主体S和客体O的类别。 本基线系统基于预训练语言模型ERNIE设计了结构化的标注策略，可以实现多条、交叠的SPO抽取。

* [princeton-nlp/PURE](https://github.com/princeton-nlp/PURE) PURE：从文本中提取实体和关系，包含 PURE（普林斯顿大学关系提取系统）的 (PyTorch) 代码和预训练模型，如论文所述：一种令人沮丧的实体和关系提取的简便方法。

* [xiaoqian19940510/Event-Extraction](https://github.com/xiaoqian19940510/Event-Extraction) 近年来事件抽取方法总结，包括中文事件抽取、开放域事件抽取、事件数据生成、跨语言事件抽取、小样本事件抽取、零样本事件抽取等类型，DMCNN、FramNet、DLRNN、DBRNN、GCN、DAG-GRU、JMEE、PLMEE等方法

* [231sm/Reasoning_In_EE](https://github.com/231sm/Reasoning_In_EE) 利用本体表示学习实现低资源的事件抽取

* [zjunlp/openue](https://github.com/zjunlp/openue) 开源的通用文本信息抽取工具 三元组抽取 事件抽取 槽填充和意图检测

* [thunlp/OpenNRE](https://github.com/thunlp/OpenNRE) 开源的神经网络关系抽取工具包，包括了多款常用的关系抽取模型，CNN、BERT、bag-level PCNN-ATT。

* [thunlp/NREPapers](https://github.com/thunlp/NREPapers) 神经网络关系抽取必读论文列表，覆盖了较为经典的神经网络关系抽取领域的已发表论文、综述等。

* [zjunlp/DocED](https://github.com/zjunlp/DocED) 跨句事件抽取旨在研究如何同时识别篇章内多个事件。提出多层双向网络Multi-Layer Bidirectional Network融合跨句语义和关联事件信息，从而增强内各事件提及的判别。

* [cuhksz-nlp/RE-AGCN](https://github.com/cuhksz-nlp/RE-AGCN) 使用注意力图卷积网络的依赖驱动关系提取的实现。

* [XueFuzhao/GDPNet](https://github.com/XueFuzhao/GDPNet) 构建一个潜在的多视图图来捕获令牌之间的各种可能关系。然后细化这个图来选择重要的词进行关系预测。最后，将细化图的表示和基于 BERT 的序列表示连接起来以进行关系提取。提出的 GDPNet（高斯动态时间扭曲池化网络）中，利用高斯图生成器 (GGG) 来生成多视图图的边。然后通过动态时间扭曲池 (DTWPool) 对图形进行细化。在 DialogRE 和TACRED上，表明在对话级 RE 上实现了最佳性能，并且在句子级 RE 上与最先进的性能相当。

* [dair-iitd/OpenIE-standalone](https://github.com/dair-iitd/OpenIE-standalone) 华盛顿大学 (UW) 和德里印度理工学院 (IIT 德里) 的主要开放信息提取 (Open IE) 系统。一个开放的系统提取文本中的关系。

* [zjunlp/KnowPrompt](https://github.com/zjunlp/KnowPrompt) 把关系标签之间的知识整合到关系提取的prompt-tuning中，并提出了一种使用协同优化的Knowledge-aware Prompt-tuning方法。

* [yao8839836/kg-bert](https://github.com/yao8839836/kg-bert) 知识库补全的工作，结合BERT可以将更丰富的上下文表示结合进模型中，在三元组分类、链接预测以及关系预测中达到了SOTA。

* [dolphin-zs/Doc2EDAG](https://github.com/dolphin-zs/Doc2EDAG) 中国金融事件提取的端到端文档级框架 。基于实体的有向无环图（EDAG）, 以自回归方式生成一个 EDAG。这样，一个硬表填充任务被分解为几个更易于处理的路径扩展子任务。

* [liuhuanyong/EventTriplesExtraction](https://github.com/liuhuanyong/EventTriplesExtraction) 基于依存句法与语义角色标注的事件三元组抽取，可用于文本理解如文档主题链，事件线等应用。

* [percent4/knowledge_graph_demo](https://github.com/percent4/knowledge_graph_demo) 展示三元组抽取后形成的知识图谱，包括几本小说的实体关系

* [lemonhu/open-entity-relation-extraction](https://github.com/lemonhu/open-entity-relation-extraction) 基于依存句法分析，实现面向开放域文本的知识三元组抽取（实体和关系抽取）及知识库构建。

* [lancopku/Chinese-Literature-NER-RE-Dataset](https://github.com/lancopku/Chinese-Literature-NER-RE-Dataset) 中文文学文本语篇级命名实体识别与关系抽取数据集

* [tonytan48/Re-DocRED](https://github.com/tonytan48/Re-DocRED) 广泛使用的文档级关系抽取基准。然而，DocRED数据集包含很大比例的假阴性示例（注释不完整）。我们修订了DocRED数据集中的4，053个文档并解决了其问题。

## 实体识别NER、意图识别、槽位填充

* [LeeSureman/Flat-Lattice-Transformer](https://github.com/LeeSureman/Flat-Lattice-Transformer) 中文NER 基于Transformer设计了一种巧妙position encoding来融合Lattice结构，可以无损的引入词汇信息。基于Transformer融合了词汇信息的动态结构，支持并行化计算，可以大幅提升推断速度。

* [ljynlp/W2NER](https://github.com/ljynlp/W2NER) 通过将统一的 NER 建模为词-词关系分类，提出了一种新颖的替代方案。该架构通过有效地建模实体词与 Next-Neighboring-Word (NNW) 和 Tail-Head-Word-* (THW-*) 关系之间的相邻关系，解决了统一 NER 的内核瓶颈。在 14 个广泛使用的基准数据集上针对平坦、重叠和不连续的 NER（8 个英语和 6 个中文数据集）进行了广泛的实验，击败了所有当前表现最好的基线，推动了最先进的表现统一的NER。

* [MiuLab/SlotGated-SLU](https://github.com/MiuLab/SlotGated-SLU) 意图识别和槽位填充（slot filling）联合模型，提出槽位门控机制（slot-gated mechanism）来解决没有明确建立槽位和意图之间联系的缺陷，达到较好的效果。

* [monologg/JointBERT](https://github.com/monologg/JointBERT) 意图识别和槽位填充（slot filling）联合训练模型，使用了BERT来进行语义编码，然后做序列标注任务和多分类任务的联合训练。

* [z814081807/DeepNER](https://github.com/z814081807/DeepNER) 天池中药说明书实体识别挑战冠军方案；中文命名实体识别；NER; BERT-CRF & BERT-SPAN & BERT-MRC；Pytorch

* [liuwei1206/LEBERT](https://github.com/liuwei1206/LEBERT) Lexicon Enhanced BERT模型来解决中文序列标注NER任务。相比于 FLAT，Lattice LSTM 等方法，它把词汇信息融入到了 BERT 底层的编码过程中。相比于 Lex-BERT，它无需包含词汇类型信息的词典，只需要普通的词向量即可。

* [kangbrilliant/DCA-Net](https://github.com/kangbrilliant/DCA-Net) 用于插槽填充和意图检测的协同互感器。数据集ATIS上，意向Acc 97.7 插槽填充F1 95.9 。

* [yizhen20133868/Awesome-SLU-Survey](https://github.com/yizhen20133868/Awesome-SLU-Survey) 口语语言理解（Spoken Language Understanding，SLU）作为任务型对话系统的核心组件，目的是为了获取用户询问语句的框架语义表示（semantics frame）信息，进而将这些信息为对话状态追踪模块（DST）以及自然语言生成模块（NLG）所使用。SLU任务通常包含以下两个任务：意图识别（intent detection）和槽位填充（slot filling）。

* [wuba/qa_match](https://github.com/wuba/qa_match) 58同城推出的一款基于深度学习的轻量级问答匹配工具，它融合领域识别与意图识别，对问答意图进行精确理解。

* [qiufengyuyi/sequence_tagging](https://github.com/qiufengyuyi/sequence_tagging) 用bilstm-crf，bert等方法进行序列标记任务

* [panchunguang/ccks_baidu_entity_link](https://github.com/panchunguang/ccks_baidu_entity_link) CCKS&百度 2019中文短文本的实体链指 第一名解决方案

* [ShannonAI/mrc-for-flat-nested-ner](https://github.com/ShannonAI/mrc-for-flat-nested-ner) 命名实体识别的统一 MRC 框架

* [AdvPicker](https://github.com/microsoft/vert-papers/tree/master/papers/AdvPicker) 通过对抗性判别器有效利用未标记数据进行跨语言 NER

* [jiesutd/LatticeLSTM](https://github.com/jiesutd/LatticeLSTM) 使用 Lattice LSTM 的中文 NER。ACL2018论文的代码。

* [Lynten/stanford-corenlp](https://github.com/Lynten/stanford-corenlp) 为文本处理任务提供了一个简单的 API，例如标记化、部分语音标记、命名实体识别、选区解析、依赖解析等。

* [thunlp/PL-Marker](https://github.com/thunlp/PL-Marker) 用于实体和关系提取的打包悬浮标记。提出了一种新的跨度表示方法，称为 Packed Levitated Markers，通过在编码器中策略性地打包标记来考虑跨度（对）之间的依赖关系。

* [v-mipeng/LexiconAugmentedNER](https://github.com/v-mipeng/LexiconAugmentedNER) 拒绝为中文 NER 合并词典的复杂操作。在中文 NER 中加入词典可以非常简单，同时也很有效。

* [lonePatient/BERT-NER-Pytorch](https://github.com/lonePatient/BERT-NER-Pytorch) Chinese NER(Named Entity Recognition) using BERT(Softmax, CRF, Span)

* [gaohongkui/GlobalPointer_pytorch](https://github.com/gaohongkui/GlobalPointer_pytorch) 全局指针统一处理嵌套与非嵌套NER的Pytorch实现

## 其他_NLP自然语言处理

[nltk/nltk](https://github.com/nltk/nltk) 支持自然语言处理研究和开发的开源 Python 模块、数据集和教程。

[keon/awesome-nlp](https://github.com/keon/awesome-nlp) 专用于自然语言处理 （NLP） 的资源精选列表

[stanfordnlp/stanza](https://github.com/stanfordnlp/stanza) Stanford NLP Group 的官方 Python NLP 库。 它支持在 60 多种语言上运行各种准确的自然语言处理工具。

[huseinzol05/NLP-Models-Tensorflow](https://github.com/huseinzol05/NLP-Models-Tensorflow) 抽象总结 聊天机器人依赖解析器 实体标记 提取摘要 发电机 语言检测 神经机器翻译 光学字符识别 POS标签 问题答案 句子对 语音转文字 拼写校正 小队问题答案 抽干 文字扩充 文字分类 文字相似度 文字转语音 主题生成器 主题建模 无监督提取摘要 矢量化器 老少少的声码器 可视化 注意Attention

[CLUEbenchmark/FewCLUE](https://github.com/CLUEbenchmark/FewCLUE) FewCLUE 小样本学习测评基准，中文版 小样本学习（Few-shot Learning）正是解决这类在极少数据情况下的机器学习问题。结合预训练语言模型通用和强大的泛化能力基础上，探索小样本学习最佳模型和中文上的实践，是本课题的目标。FewCLUE：中文小样本学习测评基准，基于CLUE的积累和经验，并结合少样本学习的特点和近期的发展趋势，精心设计了该测评，希望可以促进中文领域上少样本学习领域更多的研究、应用和发展。模型有5种不同的方式做任务，分别是使用预训练模型直接做下游任务微调、PET\RoBERTa为基础的Ptuning方式、GPT类模型为基础的Ptuning方式、使用RoBERTa或GPT做零样本学习。

[deepset-ai/haystack](https://github.com/deepset-ai/haystack) 开源的NLP框架，可以使用Transformer模型和LLM（GPT-3等）与数据交互。Haystack提供了生产就绪的工具来快速构建类似ChatGPT的问题回答、语义搜索、文本生成等。

[sebastianruder/NLP-progress](https://github.com/sebastianruder/NLP-progress) 它旨在涵盖传统和核心NLP任务，如依赖解析和词性标记，以及最近的任务，如阅读理解和自然语言推理。主要目的是为读者提供基准数据集的快速概述以及他们感兴趣的任务的最新技术，这是进一步研究的垫脚石。为此，如果有一个地方已经发布并定期维护任务的结果，例如公共排行榜。

[PKU-TANGENT/nlp-tutorial](https://github.com/PKU-TANGENT/nlp-tutorial) NLP新手入门教程

[yuanzhoulvpi2017/zero_nlp](https://github.com/yuanzhoulvpi2017/zero_nlp) 中文nlp解决方案(大模型、数据、模型、训练、推理)

[bojone/attention](https://github.com/bojone/attention)  Attention机制的实现tensorflow/keras

[425776024/nlpcda](https://github.com/425776024/nlpcda) 中文数据增强工具,随机实体替换\近义词\近义近音字替换\随机字删除\NER类 BIO 数据增强\随机置换邻近的字\百度中英翻译互转\中文等价字替换

[wac81/textda](https://github.com/wac81/textda) Python3中文文本的数据增强

[zhanlaoban/EDA_NLP_for_Chinese](https://github.com/zhanlaoban/EDA_NLP_for_Chinese) 适合中文语料的数据增强EDA的实现

[akkarimi/aeda_nlp](https://github.com/akkarimi/aeda_nlp) 一种更简单的文本分类数据增强技术.插入符号。

[rz-zhang/SeqMix](https://github.com/rz-zhang/SeqMix) 数据增强⽅法,通过序列混合增强活动序列标记。

[clovaai/ssmix](https://github.com/clovaai/ssmix) 数据增强⽅法,SSMix⽅法在⽂本input上通过巧妙的⽅法进⾏mixup，⽽不像前⾯⼤部分使⽤在 hidden层上。该⽅法在保留⼤部分重要token的前提下基于⼀些信息替换⼀个新的 span进来。

[ShomyLiu/Neu-Review-Rec](https://github.com/ShomyLiu/Neu-Review-Rec) Pytorch的基于评论文本的深度推荐系统模型库。DeepCoNN(WSDM'17)、D-Attn(RecSys'17)、ANR(CIKM'18)、NARRE(WWW'18)、MPCN(KDD'18)、TARMF(WWW'18)、CARL(TOIS'19)、CARP(SIGIR'19)、DAML(KDD'19)

[squareRoot3/Target-Guided-Conversation](https://github.com/squareRoot3/Target-Guided-Conversation) 目标指导的开放域对话,开放域聊天中目标引导.

[flairNLP/flair](https://github.com/flairNLP/flair) 最先进的NLP框架。由柏林洪堡大学开发。将先进的NLP模型应用于文本，如NER、词性标记 （PoS）、对生物医学的特殊支持、感知消歧和分类。Flair具有简单的界面，允许不同的单词和文档嵌入，包括Flair嵌入，BERT嵌入和ELMo嵌入。

[NVIDIA/NeMo](https://github.com/NVIDIA/NeMo) 对话式 AI 工具包，专为从事ASR\TTS\语言模型和NLP的研究人员而构建。NeMo的主要目标是帮助来自工业界和学术界的研究人员重用以前的工作（代码和预训练模型），并更轻松地创建新的对话AI模型。所有 NeMo 模型都使用 Lightning 进行训练，训练可自动扩展到 1000 多个 GPU。此外，NeMo 威震天 LLM 模型可以使用张量和管道模型并行性训练多达 1 万亿个参数。NeMo 模型可以针对推理进行优化，并使用 NVIDIA Riva 针对生产用例进行部署。

[lancopku/pkuseg-python](https://github.com/lancopku/pkuseg-python) 多领域中文分词工具

https://github.com/JasonForJoy/MPC-BERT 一种预训练的多方会话理解语言模型.多方会话（MPC）的各种神经模型在收件人识别、说话人识别和反应预测等方面取得了显著的进展。

https://github.com/airaria/TextBrewer 基于PyTorch的NLP任务知识蒸馏工具包，适用于多种模型结构，支持自由组合各种蒸馏策略，并且在文本分类、阅读理解、序列标注等典型NLP任务上均能获得满意的效果。

https://github.com/czhang99/SynonymNet 基于多个上下文双向匹配的同义实体发现

PRADO 用于文档分类的投影注意网络 性能媲美BERT，但参数量仅为1/300 tensorflow/models/tree/master/research/sequence_projection

https://github.com/stanford-futuredata/ColBERT ColBERT: 基于上下文（contextualized）的后期交互的排序模型 Efficient and Effective Passage Search via Contextualized Late Interaction over BERT 兼顾匹配的效率和doc中的上下文信息

https://github.com/salesforce/pytorch-qrnn 准循环神经网络Quasi-Recurrent Neural Network,基于使用实例可以比高度优化的 NVIDIA cuDNN LSTM 实现2到17倍快

https://github.com/ChenghaoMou/pytorch-pQRNN pQRNN 结合一个简单的映射和一个quasi-RNN编码器来进行快速并行处理。pQRNN模型表明这种新的体系结构几乎可以达到BERT级的性能，尽管只使用1/300的参数量和有监督的数据。

https://github.com/RUCAIBox/TG_CRS_Code TG-ReDial相应的推荐、回复生成、主题预测功能实现。

https://github.com/Qznan/QizNLP 快速运行分类、序列标注、匹配、生成等NLP任务的Tensorflow框架 (中文 NLP 支持分布式）

[salesforce/WikiSQL](https://github.com/salesforce/WikiSQL)  用于为关系数据库开发NLP界面的大型众包数据集。 WikiSQL 是与Seq2SQL 一起发布的数据集。使用强化学习从自然语言生成结构化查询。

https://github.com/toizzy/tilt-transfer 运行TILT迁移学习实验的代码 让语言模型先在乐谱上进行训练，再在自然语言上训练可以有效的提升语言模型的性能。

[XiaoMi/MiNLP/minlp-tokenizer](https://github.com/XiaoMi/MiNLP/tree/main/minlp-tokenizer) 小米 AI NLP 团队的平台 MiNLP 开源了中文分词功能

https://github.com/explosion/spaCy 工业级强度的NLP工具包，被称为最快的工业级自然语言处理工具。支持多种自然语言处理的基本功能，主要功能包括分词、词性标注、词干化、命名实体识别、名词短语提取等。

https://github.com/RUCAIBox/CRSLab 用于构建会话推荐系统（Conversational Recommender System CRS）的开源工具包。 对话推荐任务主要拆分成三个任务：推荐任务（生成推荐的商品），对话任务（生成对话的回复）和策略任务（规划对话推荐的策略）。模型 CRS 模型 ReDial、KBRD、KGSF、TG-ReDial、推荐模型 Popularity、GRU4Rec、SASRec、TextCNN、R-GCN、BERT、对话模型 HERD、Transformer、GPT-2 策略模型 PMI、MGCG、Conv-BERT、Topic-BERT、Profile-BERT

https://github.com/RUCAIBox/CRSPapers 选取了近年来基于深度学习的对话推荐系统相关论文（共 62 篇），并根据工作的类型进行分类，以供参考。

https://github.com/nlp-uoregon/trankit 用于多语言自然语言处理的基于轻型变压器的Python工具包 支持以下任务：句子分割。标记化。多字令牌扩展。词性标记。形态特征标记。依赖性解析。命名实体识别。

https://github.com/yizhen20133868/NLP-Conferences-Code 记录NLP相关顶会(如ACL、EMNLP、NAACL、COLING、AAAI、IJCAI)的论文开源项目合集

https://github.com/cuhksz-nlp/DGSA 基于方向建模图卷积网络的联合方面提取和情感分析.输入:由句子生成的依存句法分析树得到的图;句子（词序列）.输出表示为一个标签序列.可用于序列标注、ER 和情感分析。

https://github.com/FedML-AI/FedNLP FedNLP：自然语言处理中的联合学习研究平台

Graph4nlp是一个易于使用的NLP图形神经网络库。应用：文本分类、神经机器翻译、摘要、KG补全：预测konwledge图中两个现有实体之间的缺失关系。数学问题解决：自动解决数学习题，用易懂的语言提供问题的背景信息。名称实体识别、问题生成。

[PaddlePaddle/PaddleNLP](https://github.com/PaddlePaddle/PaddleNLP) 简单易用且易于开发的强大功能。开发的简单易用的自然覆盖处理模型并提供开发者的简单易用的自然覆盖处理模型，并提供NLP 多场景的语言库供灵活使用的需求。

[huybery/r2sql](https://github.com/huybery/r2sql) Dynamic Hybrid Relation Network for Cross-Domain Context-Dependent Semantic Parsing 跨域上下文相关语义分析的动态混合关系网络 应用于：多轮text-to-SQL 任务（通过多轮对话的方式生成最终的查询语句， Text-to-SQL 任务：给定一个自然语言查询和数据库的作为输入，产生一个SQL语句作为输出。）

https://github.com/facebookresearch/GENRE 首创生成式实体检索，通过seq2seq方法(BART)生成有意义的实体名称从而实现实体链接，而且还可以取得SOTA结果。

https://github.com/sebastian-hofstaetter/intra-document-cascade IDCM模型: 文档内部级联选择段落服务于文档排序。采用文档内部级联策略，在运行复杂并且高效果的排序模型（ETM，Effective Teacher Model）之前，使用高效率的模型（ESM，Efficient Student Model）进行候选文档中多余段落的删除。相比bert，具有基本相同的效果，而且查询延迟降低400%以上。

https://github.com/jingtaozhan/DRhard 通过难负例优化稠密向量文档检索模型训练，利用动态难负例抽样提高模型效果，以及将随机抽样结合静态难负例抽样提高模型稳定性。

https://github.com/yechens/NL2SQL Text2SQL 语义解析数据集、解决方案、paper资源整合项。Text to SQL( 以下简称Text2SQL)，是将自然语言文本（Text）转换成结构化查询语言SQL的过程，属于自然语言处理-语义分析（Semantic Parsing）领域中的子任务。

https://github.com/destwang/CTCResources 中文文本纠错（Chinese Text Correction, CTC）相关论文、数据集。

https://github.com/fushengwuyu/chinese_spelling_correction 中文文本纠错模型：bert语言模型+字音字形相似度 、MLM、seq2seq

https://github.com/grammarly/gector ”GECToR – Grammatical Error Correction: Tag, Not Rewrite”，使用给序列打标签来替代主流的Seq2Seq模型。本文采取了一种迭代的方法，也就是通过多次(其实最多也就两三次)序列打标签。

https://github.com/destwang/CTC2021 本赛题主要选择互联网上中文母语写作者撰写的网络文本作为校对评测数据，从拼写错误、语法错误、语病错误等多个方面考察机器的认知智能能力。

https://github.com/Jingjing-NLP/VOLT 借鉴边际效用通过最优转移学习词表。

https://github.com/thunlp/OpenAttack 文本对抗攻击工具包，可以用于文本对抗攻击的全过程，包括文本预处理、受害模型访问、对抗样本生成、对抗攻击评测以及对抗训练等。

https://github.com/thunlp/TAADpapers 文本对抗攻击和防御必读论文列表。

https://github.com/lupantech/InterGPS 基于符号推理的几何数学题求解器。建立了一个新的大规模基准数据集，称为 Geometry3K。这些数据从两本中学教材收集，涵盖了北美 6 到 12 年级的几何知识。每道题收集了 LaTeX 格式的问题文本、几何图形、四个选项和正确答案。为了模型的精细评估，每个数据标注了问题目标和几何图形的类型。Inter-GPS 将几何关系集 R 和定理集 KB 作为输入，应用定理预测器预测适用的定理序列，逐步对关系集进行符号推理，从而输出问题目标的答案。

https://github.com/Helsinki-NLP/Tatoeba-Challenge 这是一个机器翻译的挑战集，包含 29G 翻译单元在 3，708 位ext 覆盖 557 种语言。该包包括从涵盖 134 种语言的 Tatoeba.org 衍生的 631 套测试集的版本。此包提供以多种语言进行机器翻译的数据集，并提供从 Tatoeba 获取的测试数据。

https://github.com/princeton-nlp/LM-BFF 更好的Few-shot小样本微调语言模型.包括：1.基于提示（prompt）进行微调，关键是如何自动化生成提示模板；
2.将样本示例以上下文的形式添加到每个输入中，关键是如何对示例进行采样.

https://github.com/thunlp/PromptPapers 关于基于提示的预先训练语言模型的必读论文。

[linzehui/mRASP](https://github.com/linzehui/mRASP) 通过利用对齐信息预训练多语言神经机器翻译. 代表多语言随机对齐替换预训练，是一种预训练的多语言神经机器翻译模型。 它在包含 32 个语言对的大规模多语言语料库上进行了预训练。 获得的模型可以在下游语言对上进一步微调。 为了有效地使具有相似含义的单词和短语在多种语言的表示中更接近，我们引入了随机对齐替换 (RAS) 技术。

[soft-prompt-tuning](https://github.com/kipgparker/soft-prompt-tuning) The Power of Scale for Parameter-Efficient Prompt Tuning 用于参数高效的即时调整的规模的力量

[facebookresearch/ParlAI](https://github.com/facebookresearch/ParlAI) 在各种公开可用的对话数据集上训练和评估 AI 模型的框架。

[CAMTL/CA-MTL](https://github.com/CAMTL/CA-MTL) 条件自适应多任务学习：使用更少的参数和更少的数据改进 NLP 中的迁移学习

[thunlp/WantWords](https://github.com/thunlp/WantWords) 一个开源的在线反向词典。

[pcyin/tranX](https://github.com/pcyin/tranX) 用于将自然语言查询映射到机器可执行代码的通用神经语义解析器

[hooman650/SupCL-Seq](https://github.com/hooman650/SupCL-Seq) 下游优化序列表示的监督对比学习

[openai/grade-school-math](https://github.com/openai/grade-school-math) 包含 8.5K 高质量语言多样化小学数学单词问题的数据集。对于每个测试问题，我们提供从 6B 微调、6B 验证、175B 微调和 175B 验证生成的解决方案。

[makcedward/nlpaug](https://github.com/makcedward/nlpaug) NLP 的数据增强

[hankcs/pyhanlp](https://github.com/hankcs/pyhanlp) 中文分词、依存句法分析

[shibing624/pycorrector](https://github.com/shibing624/pycorrector) 中文文本纠错工具。支持中文音似、形似、语法错误纠正。实现了Kenlm、ConvSeq2Seq、BERT、MacBERT、ELECTRA、ERNIE、Transformer等多种模型的文本纠错，并在SigHAN数据集评估各模型的效果。

[HillZhang1999/MuCGEC](https://github.com/HillZhang1999/MuCGEC) MuCGEC中文纠错数据集及文本纠错SOTA模型开源

[PengheLiu/Cn_Speck_Checker](https://github.com/PengheLiu/Cn_Speck_Checker) 通过统计方法对中文单词进行自动纠错

[taozhijiang/chinese_correct_wsd](https://github.com/taozhijiang/chinese_correct_wsd) 简易中文纠错消歧 用户输入语句的同音自动纠错.

[beyondacm/Autochecker4Chinese](https://github.com/beyondacm/Autochecker4Chinese) 中文文本错别字检测以及自动纠错

[iqiyi/FASPell](https://github.com/iqiyi/FASPell)  2019-SOTA简繁中文拼写检查工具：FASPell Chinese Spell Checker ( 中文拼写检错 / 中文拼写纠错 / 中文拼写检查)

[hiyoung123/SoftMaskedBert](https://github.com/hiyoung123/SoftMaskedBert) 中文文本纠错模型。使用两个网络模型，一个用于错误检测；另一个基于BERT进行纠错。

[ACL2020SpellGCN/SpellGCN](https://github.com/ACL2020SpellGCN/SpellGCN) 将语音学和视觉相似性结合到汉语拼写检查\文本纠错

[MuCGEC/scorers/ChERRANT](https://github.com/HillZhang1999/MuCGEC/tree/main/scorers/ChERRANT) 借鉴了英文上主流的GEC(Grammatical Error Correction 语法纠错)评估工具[ERRANT](https://github.com/chrisjbryant/errant)，搭建了中文GEC评估工具ChERRANT（Chinese ERRANT）。ChERRANT的主要功能是通过对比预测编辑和标准编辑，计算预测结果的精确度、召回度、F值指标，从而评估语法纠错模型的性能。应用:搜索query纠错、语音纠错、舆情文本纠错

[liushulinle/CRASpell](https://github.com/liushulinle/CRASpell) 使用复制机制改进中文拼写纠正的上下文错字稳健方法

[thunlp/OpenBackdoor](https://github.com/thunlp/OpenBackdoor) 文本后门攻防开源工具包（NeurIPS 2022 D&B）

[xueyouluo/ccks2021-track2-code](https://github.com/xueyouluo/ccks2021-track2-code) “英特尔创新大师杯”深度学习挑战赛 赛道2：CCKS2021中文NLP地址要素解析 。基于BERT的Biaffine结构，直接预测文本构成的所有span的类别。相比单纯基于span预测和基于MRC的预测，Biaffine的结构可以同时考虑所有span之间的关系，从而提高预测的准确率。

[kpu/kenlm](https://github.com/kpu/kenlm) 高效统计语言模型kenlm：新词发现、分词、智能纠错

[ryanzhumich/Contrastive-Learning-NLP-Papers](https://github.com/ryanzhumich/Contrastive-Learning-NLP-Papers) NLP 对比学习是一种学习嵌入空间的技术，使得相似的数据样本对具有接近的表示，而不同的样本彼此相距很远。 它可以在有监督或无监督的设置中使用，使用不同的损失函数来生成特定于任务或通用的表示。 在各种 NLP 任务中提供了有希望的性能改进，而且还提供了所需的特性，例如与任务无关的句子表示、忠实的文本生成、零样本和少样本设置中的数据高效学习、可解释性和可解释性 .

[textstat/textstat](https://github.com/textstat/textstat) 用于计算文本对象（段落、句子、文章）的可读性统计数据。

[nonebot/nonebot2](https://github.com/nonebot/nonebot2) 跨平台 Python 异步聊天机器人框架

[mit-han-lab/smoothquant](https://github.com/mit-han-lab/smoothquant) 对大语言模型的准确和高效的训练后量化

[causaltext/causal-text-papers](https://github.com/causaltext/causal-text-papers) 因果推理和自然语言处理的交叉研究。

[zhijing-jin/Causality4NLP_Papers](https://github.com/zhijing-jin/Causality4NLP_Papers) 关于自然语言处理因果关系的论文阅读列表

[DaDaMrX/ReaLiSe](https://github.com/DaDaMrX/ReaLiSe) 多模态模型中文拼写检查器。包括：文字语义、文字发音、文字图形。

[dbohdan/structured-text-tools](https://github.com/dbohdan/structured-text-tools) 用于操作结构化文本数据的命令行工具列表

[huggingface/tokenizers](https://github.com/huggingface/tokenizers) 提供当今最常用的分词器的实现，重点关注性能和多功能性。

[jessevig/bertviz](https://github.com/jessevig/bertviz) 在NLP模型中可视化注意力（BERT，GPT2，BART等）

[lutzroeder/netron](https://github.com/lutzroeder/netron) 用于神经网络、深度学习和机器学习模型的可视化工具

[sebastianruder/NLP-progress](https://github.com/sebastianruder/NLP-progress) 用于跟踪自然语言处理 (NLP) 进展的存储库，包括数据集和最常见 NLP 任务的最新技术水平。

[DengBoCong/nlp-paper](https://github.com/DengBoCong/nlp-paper) 自然语言处理领域下的相关论文（附阅读笔记），复现模型以及数据处理等

[ssut/py-googletrans](https://github.com/ssut/py-googletrans) （非官方）Googletrans：免费且无限制的 Google 翻译 API for Python。翻译完全免费。

[https://github.com/jgm/pandoc](https://github.com/jgm/pandoc) 通用标记转换器。一个Haskell库，用于从一种标记格式转换为另一种标记格式，以及使用该库的命令行工具。
