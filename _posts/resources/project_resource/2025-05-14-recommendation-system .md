---
layout: post
title: "推荐系统"
date: 2025-05-14
tags: 
  - RecommendationSystem
categories: 
  - resource
comments: true
author: deathwhispers
---



## 推荐系统算法库与列表

* [shenweichen/DeepCTR](https://github.com/shenweichen/DeepCTR) 易于使用、模块化和可扩展的基于深度学习的 CTR 模型包，用于搜索和推荐。

* [hongleizhang/RSPapers](https://github.com/hongleizhang/RSPapers) 推荐系统必读论文精选列表。

* [YuyangZhangFTD/awesome-RecSys-papers](https://github.com/YuyangZhangFTD/awesome-RecSys-papers) 推荐系统中的经典论文

* [ChenglongChen/tensorflow-DeepFM](https://github.com/ChenglongChen/tensorflow-DeepFM)

* [twitter/the-algorithm](https://github.com/twitter/the-algorithm) Twitter 的推荐算法是一组服务和作业，负责在所有 Twitter 产品表面（例如，为你时间线、搜索、探索）提供推文和其他内容的提要。有关算法工作原理的介绍，请参阅我们的工程博客。

* [alibaba/DeepRec](https://github.com/alibaba/DeepRec) 基于 TensorFlow 的推荐引擎。具有超大规模分布式训练能力，支持万亿样本的模型训练和千亿的Embedding Processing。针对稀疏模型场景，在CPU和GPU平台上进行了深度的性能优化。

* [cheungdaven/DeepRec](https://github.com/cheungdaven/DeepRec) 基于 TensorFlow 的深度学习推荐的开源工具包。

* [lyst/lightfm](https://github.com/lyst/lightfm)  LightFM 的 Python 实现，一种混合推荐算法。

* [tensorflow/recommenders](https://github.com/tensorflow/recommenders) 使用 TensorFlow 构建推荐系统模型的库。

* [RUCAIBox/RecBole](https://github.com/RUCAIBox/RecBole) 统一，全面，高效的推荐库，包括：

  - AFM,AutoInt,DCN,DeepFM,DSSM,FFM,FM,FNN,FwFM,LR,NFM,PNN,WideDeep,xDeepFM,BPR,ConvNCF,DGCF,DMF,FISM,GCMC,ItemKNN,LightGCN,NAIS,NeuMF,NGCF,Pop,SpectralCF,CFKG,
  - CKE（Collaborative Knowledge base Embedding 发自16年KDD，将KG与CF融合做联合训练）
  - KGAT Knowledge Graph Attention Network for Recommendation 用KG做增强，捕捉这种高阶交互式特征，做推荐预测。
  - KGCN,KGNNLS,
  - KTUP Unifying Knowledge Graph Learning and Recommendation:Towards a Better Understanding of User Preferences 一方面利用KG可以帮助更好的理解用户偏好。另一方面，用户-物品的交互可以补全KG，增强KG中缺少的事实。最终使两个部分都得到加强。
  - MKR(Multi-task Learning for KG enhanced Recommendation 融合KG和RC) 左边是推荐任务。用户和物品的特征表示作为输入，预测点击率y 右边是知识图谱任务。三元组的头结点h和关系r表示作为输入，预测的尾节点t 两者的交互由一个cross-feature-sharing units完成。由于物品向量和实体向量实际上是对同一个对象的两种描述，他们之间的信息交叉共享可以让两者都获得来自对方的额外信息，从而弥补了自身的信息稀疏性的不足。
  - ippleNet,BERT4Rec,Caser,DIN,FDSA,FPMC,GCSAN,GRU4Rec,GRU4RecF,GRU4RecKG,KSR,NARM,NextItNet,S3Rec,SASRec,SASRecF,SRGNN,STAMP,TransRec

* [Coder-Yu/QRec](https://github.com/Coder-Yu/QRec) QRec：快速实现推荐系统的 Python 框架（基于 TensorFlow）

* [Transformers4Rec](https://github.com/NVIDIA-Merlin/Transformers4Rec/) Transformers4Rec 是一个灵活且高效的库，用于顺序和基于会话的推荐，可用于 PyTorch 和 Tensorflow。

* [datawhalechina/torch-rechub](https://github.com/datawhalechina/torch-rechub) 用于推荐模型的轻量级Pytorch 框架，易于使用且易于扩展。scikit-learn风格易用的API。模型训练与模型定义解耦，易拓展，可针对不同类型的模型设置不同的训练机制。接受pandas的DataFrame、Dict数据输入，上手成本低。高度模块化，容易调用组装成新模型 LR、MLP、FM、FFM、CIN、target-attention、self-attention、transformer。支持常见排序模型 WideDeep、DeepFM、DIN、DCN、xDeepFM等。支持常见召回模型 DSSM、YoutubeDNN、YoutubeDSSM、FacebookEBR、MIND等。多任务学习支持SharedBottom、ESMM、MMOE、PLE、AITM等模型。 GradNorm、UWL、MetaBanlance等动态loss加权机制。

* [shenweichen/DeepMatch](https://github.com/shenweichen/DeepMatch) 用于推荐和广告的深度匹配模型库。训练模型和导出用户和项目的表示向量非常容易，可用于ANN搜索。

* [PaddlePaddle/PaddleRec](https://github.com/PaddlePaddle/PaddleRec) 大规模推荐算法库，包含推荐系统经典及最新算法LR、Wide&Deep、DSSM、TDM、MIND、Word2Vec、Bert4Rec、DeepWalk、SSR、AITM，DSIN，SIGN，IPREC、GRU4Rec、Youtube_dnn、NCF、GNN、FM、FFM、DeepFM、DCN、DIN、DIEN、DLRM、MMOE、PLE、ESMM、ESCMM, MAML、xDeepFM、DeepFEFM、NFM、AFM、RALM、DMR、GateNet、NAML、DIFM、Deep Crossing、PNN、BST、AutoInt、FGCNN、FLEN、Fibinet、ListWise、DeepRec、ENSFM，TiSAS，AutoFIS等，包含经典推荐系统数据集criteo 、movielens等

* [wangshusen/RecommenderSystem](https://github.com/wangshusen/RecommenderSystem) 结合小红书的业务场景和内部实践，讲解主流的工业界推荐系统技术。

* [ZiyaoGeng/Recommender-System-with-TF2.0](https://github.com/ZiyaoGeng/Recommender-System-with-TF2.0) CTR预言论文进行复现，包括传统模型（MF，FM，FFM等），神经网络（WDL，DCN等）以及序列模型（DIN）。

* [THUwangcy/ReChorus](https://github.com/THUwangcy/ReChorus) 用于Top-K推荐的通用PyTorch框架，具有隐式反馈，尤其是用于研究目的。BPR NCF Tensor GRU4Rec NARM SASRec TiSASRec CFKG SLRC Chorus

* [NVIDIA/NVTabular](https://github.com/NVIDIA/NVTabular) 为特征工程、前处理提供了更快的迭代速度，同时利用异步批量加载的方法有效提高了GPU的利用率，提供更快的加载速率。Merlin推荐系统框架的模块。

* [NVIDIA/HugeCTR](https://github.com/NVIDIA/HugeCTR) a high efficiency GPU framework designed for Click-Through-Rate (CTR) estimating training ，在Embedding lookup上做了很多优化，可以轻易的通过数据和模型并行的方式将模型扩展到TB级别，在大规模参数的背景下，这给挖掘模型能力提供了更多的想象力。同时更快的训练速度也让算法工程师能够尝试更多的网络结构，挖掘最适合所研究问题的模型。

* [microsoft/recommenders](https://github.com/microsoft/recommenders) 推荐系统上的最佳实践。包括多个模型：ALS A2SVD BPR Caser DKN xDeepFM FAST LightFM/Hybrid Matrix Factorization LightGBM/Gradient Boosting Tree* LightGCN GeoIMC GRU4Rec Multinomial VAE LSTUR NAML NCF NPA NRMS NextItNet RBM RLRMC SAR SLi-Rec SUM Standard VAE SVD TF-IDF Vowpal Wabbit (VW)* Wide and Deep FM&FFM

* [AmazingDD/daisyRec](https://github.com/AmazingDD/daisyRec) 在 pytorch 中开发的推荐系统。算法：KNN、LFM、SLIM、NeuMF、FM、DeepFM、VAE 等，旨在公平比较推荐系统基准

* [wubinzzu/NeuRec](https://github.com/wubinzzu/NeuRec) 全面且灵活的 Python 库，用于推荐系统，其中包括大量最先进的神经推荐模型。该库旨在解决一般、社交和顺序（下一项）推荐任务，使用Tensorflow库提供 33 个开箱即用的模型。

* [guoguibing/librec](https://github.com/guoguibing/librec) 一个用于推荐系统的 Java 库（需要 Java 版本 1.7 或更高版本）。它实现了一套最先进的推荐算法，旨在解决两个经典的推荐任务：**评分预测**和**项目排名**。

* [facebookresearch/torchrec](https://github.com/facebookresearch/torchrec) 推荐系统的 Pytorch库,旨在提供大型推荐系统 (RecSys) 所需的通用稀疏性和并行性原语。它允许作者使用跨多个 GPU 分片的大型嵌入表来训练模型。

* [huawei-noah/FuxiCTR](https://github.com/huawei-noah/benchmark/tree/main/FuxiCTR) FuxiCTR 为 CTR 预测提供了一个开源库，在可配置性、可调整性和可重复性方面具有惊人的功能。模型包括：LR FM CCPM FFM YoutubeDNN Wide&Deep IPNN DeepCross HOFM DeepFM NFM AFM DCN FwFM xDeepFM DIN FiGNN AutoInt/AutoInt+ FiBiNET FGCNN HFM/HFM+ ONN AFN/AFN+ LorentzFM FLEN FmFM

* [openbenchmark/BARS](https://github.com/openbenchmark/BARS) 迈向推荐系统的开放基准测试。 BARS 基准目前涵盖以下两项任务:点击率预测\候选项目匹配

* [PersiaML/PERSIA](https://github.com/persiaml/persia) 基于 PyTorch 训练深度学习推荐模型的高性能分布式框架。它能够训练具有多达 100 万亿个参数的推荐模型。对公共数据集的实证研究表明，PERSIA 在推荐方面优于其他系统。它的效率和稳健性也得到了快手1亿级DAU的多个应用程序的验证。

* [alibaba/EasyRec](https://github.com/alibaba/EasyRec) 大规模推荐算法的框架。实现了用于常见推荐任务的最先进的深度学习模型：候选生成（匹配）、评分（排名）和多任务学习。它通过简单的配置和超参数调整（HPO）提高了生成高性能模型的效率。

* [pytorch/torchrec](https://github.com/pytorch/torchrec) 推荐系统的 Pytorch 域库

* [PKU-DAIR/GNN-in-RS](https://github.com/PKU-DAIR/GNN-in-RS) 推荐系统中的 GNN（ACM 计算调查 2022）

* [NicolasHug/Surprise](https://github.com/NicolasHug/Surprise) 用于构建和分析推荐系统的 Python scikit

* [caserec/CaseRecommender](https://github.com/caserec/CaseRecommender) 案例推荐器：用于推荐系统的灵活且可扩展的 Py框架

* [grahamjenson/list_of_recommender_systems](https://github.com/grahamjenson/list_of_recommender_systems) 推荐系统和资源列表

* [mengfeizhang820/Paperlist-for-Recommender-Systems](https://github.com/mengfeizhang820/Paperlist-for-Recommender-Systems) 推荐系统论文列表

* [caserec/CaseRecommender](https://github.com/caserec/CaseRecommender) 案例推荐器：用于推荐系统的灵活且可扩展的 Python 框架

## 其他_推荐系统

[imsheridan/DeepRec](https://github.com/imsheridan/DeepRec) 推荐、广告工业界经典以及最前沿的论文、资料集合

[laekov/fastmoe](https://github.com/laekov/fastmoe) 一个易用且高效的基于 PyTorch 的 MoE 模型训练系统.

[oywtece/dstn](https://github.com/oywtece/dstn)

https://github.com/shenweichen/DSIN

[facebookresearch/dlrm](https://github.com/facebookresearch/dlrm) 深度学习推荐模型（DLRM）的实现

[vze92/DMR](https://github.com/vze92/DMR) Deep Match to Rank Model for Personalized Click-Through Rate Prediction DMR：Matching和Ranking相结合的点击率预估模型

[kang205/SASRec](https://github.com/kang205/SASRec) 源于Transformer的基于自注意力的序列推荐模型

[shichence/AutoInt](https://github.com/shichence/AutoInt) 使用Multi-Head self-Attention进行自动的特征提取

https://github.com/xiangwang1223/neural_graph_collaborative_filtering 神经图协同过滤

https://github.com/UIC-Paper/MIMN 点击率预测的长序列用户行为建模的实践

https://github.com/motefly/DeepGBM 结合了GBDT 和神经网络的优点，在有效保留在线更新能力的同时，还能充分利用类别特征和数值特征。由两大块组成，CatNN 主要侧重于利用 Embedding 技术将高维稀疏特征转为低维稠密特征，而 GBDT2NN 则利用树模型筛选出的特征作为神经网络的输入，并通过逼近树结构来进行知识蒸馏。

https://github.com/LeeeeoLiu/ESRM-KG 关键词生成的基于电商会话的推荐模型

https://github.com/zhuchenxv/AutoFIS 自动特征交互选择的点击率预测模型

https://github.com/pangolulu/exact-k-recommendation 解决推荐中带约束的Top-K优化问题

https://github.com/Scagin/NeuralLogicReasoning 神经协同推理,提出了一种新的神经逻辑推荐（NLR）框架，能够将逻辑结构和神经网络相结合，将推荐任务转化为一个逻辑推理任务。

https://github.com/allenjack/HGN 用矩阵分解的形式捕捉用户的长期兴趣，同时将短期兴趣进行拆分，分为group-level以及instance-level的，通过Hierarchical Gating来处理group-level的信息,item-item的乘积来捕捉商品之间的关系。

https://github.com/RUCAIBox/CIKM2020-S3Rec 自我推荐学习，用于具有互信息最大化的顺序推荐

https://github.com/chenchongthu/SAMN 社交注意力记忆网络在推荐系统中的应用

https://github.com/Lancelot39/KGSF 基于知识图谱语义融合改进会话推荐系统
Improving Conversational Recommender Systems via Knowledge Graph based Semantic Fusion

https://github.com/DeepGraphLearning/RecommenderSystems 顺序推荐 基于维度的推荐 社交推荐

https://github.com/FeiSun/BERT4Rec 基于BERT的顺序推荐

https://github.com/ChuanyuXue/CIKM-2019-AnalytiCup 2019-CIKM挑战赛，超大规模推荐之用户兴趣高效检索赛道 冠军解决方案 ,召回阶段基于 Item CF 相似性做召回( item-item 相似性),排序阶段,最终使用了 Catboost 和 Lightgbm 建模。

https://github.com/zyli93/InterHAt 通过分层注意力预测可解释的点击率。

https://github.com/SSE-PT/SSE-PT 基于Transformer的模型,但是和SASRec类似, 效果不错,但是缺少个性化,而且没有加入基于个性化的用户embedding。为了克服这种问题,本文提出来一种个性化的Transformer(SSE-PT),该方法相较于之前的方案提升了5%。

https://github.com/triton-inference-server/server 面向高吞吐低延时的生产环境的框架，通过Triton做线上推理，将TensorRT作为执行后端，能够有效降低Latency，并最大化地利用GPU资源。相比于一个纯CPU的方案，两者的结合使用能够使Latency达到原先的1/18，数据吞吐量达到原先的17.6倍。

https://github.com/lqfarmer/GraphTR 采用了GraphSAGE+FM+Transformer多种手段，粒度上从粗到细，交叉、聚合来自不同领域的异构消息，相比于mean/max pooling、浅层FC等传统聚合方式，极大提升了模型的表达能力

https://github.com/guyulongcs/CIKM2020_DMT 将兴趣建模、多任务学习、偏置学习等几部分进行融合，提出了DMT模型（Deep Multifaceted Transformers）

https://github.com/hwwang55/DKN DKN，将知识图表示融入到新闻推荐中。DKN是一种基于内容的用于点击率预估的深度推荐框架。DKN的主要部分是一个多通道、单词实体对齐的知识感知卷积神经网络，KCNN，其中融入了新闻在语意层面和知识层面的表示。KCNN将单词和实体作为多通道，在卷积过程中明确保留他们之间的对齐关系。

https://github.com/yusanshi/NewsRecommendation NRMS NAML LSTUR DKN Hi-Fi Ark TANR

https://github.com/johnny12150/GCE-GNN 提出了一种全局上下文增强(global-context enhanced)的GNN网络，称为GCE-GNN。能够从两种层次来学习物品的表征，包括global-level：从所有session构成的图上进行全局的表征；以及session-level：从单个session局部item转移图上进行局部的表征；最后融合二者，并通过注意力机制形成最终的序列表征，用于序列推荐任务。

https://github.com/BinbinJin/SD-GAR 第一篇将生成式对抗网络（GAN）框架应用于信息检索（包括推荐系统）的研究工作。在该工作中，IRGAN 训练了一个生成器和一个判别器，其中生成器用来自适应地生成合适的负样本以帮助判别器训练；而判别器则是用来判断样本是来自用户真实的反馈还是生成器生成的样本。通过两者交替式对抗性地训练达到互相提升效果的目的。

https://github.com/twchen/lessr 将会话记录构建成图来建模商品之间的跳转关系的图神经网络

https://github.com/NLPWM-WHU/AGNN 区分了推荐系统中的一般冷启动和严格冷启动，并提出了属性图神经网络方法有效应对严格冷启动的场景。

https://github.com/CRIPAC-DIG/SR-GNN 会话序列推荐的图应用 直接将会话序列建模为图结构数据，并使用图神经网络捕获复杂的项目物品item间转换，每一个会话利用注意力机制将整体偏好与当前偏好结合进行表示。同时这种方式也就不依赖用户的表示了，完全只基于会话内部的潜在向量获得Embedding，然后预测下一个点击。

https://github.com/uctoronto/SHAN Sequential Recommender System based on Hierarchical Attention Network 分层注意力网络SHAN用于序列推荐 。提出新颖的两层分层注意力网络，将上述特性考虑进来，用于推荐可能感兴趣的下一个商品。第一层注意力网络基于用户的历史购买商品的表示来学习用户的长期偏好，第二层通过将用户的长期和短期偏好结合起来，输出最终的用户表示。

https://github.com/chenghuige/mind MIND新闻推荐冠军分享细节揭秘

https://github.com/WayneDW/DeepLight_Deep-Lightweight-Feature-Interactions 轻量级特征交互算法deeplight 大幅加速ctr预估在线服务。 一，通过在浅层结构中精确搜索信息量更大的特征交互来加速模型推理，二，在深层结构中，从层内和层间对冗余的层和冗余的参数进行剪枝，三，促使embedding层的稀疏性，进而保持最有判别性的信息。为了解决预测延迟问题，我们通过结构修剪来加速预测，最终以46倍的速度提高而不会牺牲Criteo数据集上的最新性能。

https://github.com/JiachengLi1995/TiSASRec Time Interval Aware Self-Attention for Sequential Recommendation 时间间隔自注意力模型用于序列推荐。 基于序列模型框架对行为的时间戳进行建模，在下一个商品预测中探索不同时间间隔的影响。

https://github.com/wuch15/IJCAI2019-NAML 多视图学习新闻推荐系统Neural News Recommendation with Attentive Multi-View Learning 可以通过利用不同种类的新闻信息来学习用户和新闻的特征表示。

https://github.com/guoday/Tencent2020_Rank1st  广告受众基础属性预估 2020 Tencent College Algorithm Contest, and the online result ranks 1st.

https://github.com/yuduo93/THIGE 基于时序异质交互图表示学习的商品推荐 将复杂异质的动态交互行为构建为时序异质交互图（Temporal Heterogeneous Interaction Graph, 简称为THIG）进而同时学习用户兴趣和商品表示用于商品推荐。本文提出了一种时序异质图上的表示学习方法，称之为THIGE，充分建模交互行为的异质性，刻画不同类型的兴趣偏好，并融合长、短期兴趣构建用户、商品表示。最后，在3个真实数据集上验证模型的有效性。

https://github.com/guyulongcs/CIKM2020_DMT 大型电子商务推荐系统中多目标排名的深层多面Transformers模型

https://github.com/weiyinwei/MMGCN 多模态图神经网络解决短视频推荐难题

https://github.com/wujcan/SGL 基于图自监督学习的推荐系统。应用于「用户-物品二分图推荐系统」的「图自监督学习」框架。

https://github.com/wangjiachun0426/StackRec 通过迭代堆叠实现推荐系统的高效训练。采用对一个浅层序列推荐模型进行多次层堆叠（Layer Stacking），从而得到一个深层序列推荐模型。具体来说，训练过程包含以下步骤：1）预训练一个浅层序列推荐模型；2）对该模型进行层堆叠，得到一个两倍深度的模型；3）微调这个深层模型；4）将深层模型作为一个新的浅层模型，重复1）至3）直到满足业务需求。

[xiangwang1223/neural_graph_collaborative_filtering](https://github.com/xiangwang1223/neural_graph_collaborative_filtering) 神经图协同过滤（NGCF）是一种基于图神经网络的新推荐框架，通过执行嵌入传播，在用户项二部图中以高阶连通性的形式对协同信号进行显式编码。

https://github.com/johnnyjana730/MVIN 提出multi-view item network (MVIN) ，从user和item来学习多个视角下的商品表示，进而进行商品推荐。在实体视图中，项目表示由KG中连接到它的实体来定义的。

https://github.com/weberrr/CKAN Collaborative Knowledge-aware Attentive Network for Recommender Systems 协作知识感知的注意力网络推荐系统

https://github.com/danyang-liu/KRED KRED：基于知识感知的文档表示应用于新闻推荐。首先是用KGAT来表示每个实体，然后使用用实体的位置 实体出现频率 实体的类别等信息。再用Transformer来优化表征。最后做多任务：包括个性化推荐，项目到项目推荐、新闻流行预测、新类别预测和本地新闻检测等等。

https://github.com/CRIPAC-DIG/DGCF 动态图协同过滤算法，利用动态图来同时捕捉用户和商品之间的协同和序列关系的框架。提出三种更新机制： 零阶继承，一阶传播，二阶聚合，来表示新的交互发生时，该交互对用户或者商品的影响。基于这三种机制，交互发生时同时更新用户和商品的embedding，并且利用最新的embedding来给出推荐。

https://github.com/QYQ-bot/CLEA 运用对比学习解决购物篮推荐场景。（下一个购物篮推荐，也就是根据用户的历史购物篮序列，来推荐用户在下一次可能购买的商品集合。）

https://github.com/huangtinglin/MixGCF 基于多层嵌入合成负例用于推荐，相对NGCF 提高 26%, LightGCN 提高 22%

https://github.com/DyGRec/ASReP  反向预训练Transformer 增广序列推荐系统.解决序列推荐系统中的冷启动（cold-start）问题。为了解决该问题，我们提出需要对冷启动对应的短序列（short sequence）进行增广（Augmentation），从而能够补全信息而避免冷启动的问题。

https://github.com/NLPWM-WHU/EDUA 多样性推荐的 EDUA 模型。其采用双边分支网络作为双目标优化的主要架构，该架构既保持传统学习分支的准确性，又提高自适应学习分支的多样性。

[gluver/KG4Rec_Paperlist](https://github.com/gluver/KG4Rec_Paperlist) 这是关于基于知识图谱的推荐的顶级论文列表。

[xidongbo/AITM](https://github.com/xidongbo/AITM) 自适应信息传输多任务 (AITM) 框架的 TensorFlow 实现。 提交给 KDD21 的论文代码：使用多任务学习为客户获取建模受众多步转换之间的顺序依赖性。应用场景：联名卡获客，从曝光（Impression）、点击（Click）、申请（Application）、核卡（Approval）、激活（Activation）。另外，使用公开的[Ali-CCP阿里巴巴点击和转化预测数据集](https://tianchi.aliyun.com/datalab/dataSet.html?dataId=408)。[pytorch实现](https://github.com/adtalos/AITM-torch)

[newlei/LR-GCCF](https://github.com/newlei/LR-GCCF) 重温基于图的协同过滤：一种线性残差图卷积网络方法，AAAI2020 本文提出了一种使用非线性特征传播和残差结构的GCN网络LR-GCCF用于基于CF的推荐系统，在模型表型上和时间效率上有了一定的提高。

[wangzhegeek/EGES](https://github.com/wangzhegeek/EGES) 阿里巴巴论文的实施：阿里巴巴[电子商务推荐的十亿级商品嵌入](https://arxiv.org/abs/1803.02349)

[YushanZhu/K3M](https://github.com/YushanZhu/K3M) 电子商务中的知识感知多模态预训练

[tsinghua-fib-lab/GNN-Recommender-Systems](https://github.com/tsinghua-fib-lab/GNN-Recommender-Systems) 基于图神经网络的推荐算法索引。

[oywtece/deepmcp](https://github.com/oywtece/deepmcp) 点击率 (CTR) 预测模型。大多数现有方法主要对特征-CTR 关系进行建模，并且存在数据稀疏问题。相比之下，DeepMCP 对其他类型的关系进行建模，以学习更多信息和统计上可靠的特征表示，从而提高 CTR 预测的性能。DeepMCP 包含三部分：匹配子网、关联子网和预测子网。这些子网分别为用户-广告、广告-广告和功能-点击率关系建模。当这些子网在目标标签的监督下联合优化时，学习到的特征表示既具有良好的预测能力，又具有良好的表示能力。

[rener1199/deep_memory](https://github.com/rener1199/deep_memory) 用户记忆网络的点击率预测

[xiaxin1998/DHCN](https://github.com/xiaxin1998/DHCN) 用于基于会话的推荐的自超图卷积网络

[maenzhier/GRecX](https://github.com/maenzhier/GRecX) 基于 GNN 的推荐的高效统一基准。

[RUCAIBox/Awesome-Privacy-Preserving-RS-Paper](https://github.com/RUCAIBox/Awesome-Privacy-Preserving-RS-Paper) 本知识库收集了 2018 年后隐私保护推荐系统的最新研究进展。

[github.com/THUDM/ComiRec](https://github.com/THUDM/ComiRec) KDD 2020 论文《Controllable Multi-Interest Framework for Recommendation》的源代码和数据集 可控的多兴趣推荐框架

[microsoft/tutel](https://github.com/microsoft/tutel) Tutel MoE：优化的专家组合实施

[Jhy1993/Awesome-GNN-Recommendation](https://github.com/Jhy1993/Awesome-GNN-Recommendation) GNN-推荐相关资源

[sisinflab/elliot](https://github.com/sisinflab/elliot) 用于可重现推荐系统评估的全面而严谨的框架

[sumitsidana/recsys_challenge_2020](https://github.com/sumitsidana/recsys_challenge_2020) 此存储库包含 2020 年 RecSys 挑战赛方法的第四名解决方案的代码。该挑战侧重于在动态环境中进行推文参与度预测的现实任务。目标是根据异构输入数据预测目标用户对一组推文的不同类型参与（点赞、回复、转推和转推）的概率。

[ystdo/Codes-for-WSDM-CUP-Music-Rec-1st-place-solution](https://github.com/lystdo/Codes-for-WSDM-CUP-Music-Rec-1st-place-solution)  WSDM CUP 2018 音乐推荐挑战赛第一名解决方案的对应代码。预测 3 月订阅到期的用户中，哪些会流失。为解决该题，阿里巴巴使用了两层 Stacking Model，第一层采用逻辑回归、随机森林、XGBoost 算法，第二层又采用 XGBoost 算法把第一层的结果融合。流失用户预测，对有会员体系的业务场景都可以使用，其中会员付费为主要收入的业务就更为关键，比如像 Apple Music、虾米音乐。多层 Stacking Model 由 AliOS 神灯研发，极大提升了分类预测的准确率，已广泛应用于 AliOS 多项业务中。

[DiligentPanda/Tencent_Ads_Algo_2018](https://github.com/DiligentPanda/Tencent_Ads_Algo_2018) 该仓库维护2018年腾讯广告算法大赛的代码。我们的代码在决赛中排名第三。基于 FFM 的注意力神经网络的平均值。在最终提交中，我们使用了 13 个这样的网络。但是这些网络只是在它们的随机种子上有所不同。 5 个这样的网络将给出几乎相同的结果。Lookalike 相似人群拓展

[ttvand/Santander-Product-Recommendation](https://github.com/ttvand/Santander-Product-Recommendation) Kaggle 竞赛第二名解决方案 - Santander 产品推荐

[Travisgogogo/BAAI-ZHIHU-2019](https://github.com/Travisgogogo/BAAI-ZHIHU-2019) Top3  高效地将用户新提出的问题邀请其他用户进行解答，以及挖掘用户有能力且感兴趣的问题进行邀请下发，优化邀请回答的准确率，提高问题解答率以及回答生产数。

[LogicJake/tuling-video-click-top3](https://github.com/LogicJake/tuling-video-click-top3) 图灵联邦视频点击预测大赛线上第三

[PPshrimpGo/BDCI2018-ChinauUicom-1st-solution](https://github.com/PPshrimpGo/BDCI2018-ChinauUicom-1st-solution) CCF BDCI 2018的面向电信领域的个性化套餐匹配第一名解决方案

[hydantess/TianChi_zhilianzhaopin:](https://github.com/hydantess/TianChi_zhilianzhaopin) 智联招聘人岗智能匹配 根据智联招聘抽样的经过脱敏的求职者标签数据、职位信息、及部分求职者行为信息、用人单位反馈信息，训练排序模型，对求职者的职位候选集进行排序，尽可能使得双端都满意的职位（求职者满意以及用人单位满意）优先推荐。

[RainFung/Tianchi-AntaiCup-International-E-commerce-Artificial-Intelligence-Challenge](https://github.com/RainFung/Tianchi-AntaiCup-International-E-commerce-Artificial-Intelligence-Challenge) 天池-安泰杯跨境电商智能算法大赛 冠军。 通过海量数据挖掘用户下一个可能交互商品，选手们可以提交预测的TOP30商品列表，排序越靠前命中得分越高。

[fuxiAIlab/RL4RS](https://github.com/fuxiAIlab/RL4RS) 基于强化学习的推荐系统的真实世界基准

[NVIDIA-Merlin/competitions](https://github.com/NVIDIA-Merlin/competitions) 推荐系统竞赛的解决方案 RecSys2019_Challenge, RecSys2020_Challenge,RecSys2021_Challenge,SIGIR_eCommerce_Challenge_2021,WSDM_WebTour2021_Challenge

[rosetta-ai/rosetta_recsys2019](https://github.com/rosetta-ai/rosetta_recsys2019) RosettaAI 团队在 2019 年 ACM Recsys 挑战赛中获得第四名的解决方案

[kupuSs/CIKM-CUP-2019-track2-rank10](https://github.com/kupuSs/CIKM-CUP-2019-track2-rank10) CIKM 2019 E-Commerce AI Challenge - 超大规模推荐之用户兴趣高效检索

[miziha-zp/KDD2020_mutilmodalities](https://github.com/miziha-zp/KDD2020_mutilmodalities) top8 KDD Cup 2020 Challenges for Modern E-Commerce Platform: Multimodalities Recall

[steven95421/KDD_WinnieTheBest](https://github.com/steven95421/KDD_WinnieTheBest) KDD Cup 2020 现代电商平台挑战：Multi-modalities Recall 第一名。数据来自移动电商平台的真实场景多模态数据。数据集由搜索查询和产品图像特征组成，是一个基于查询的多模式检索任务。实现了根据候选产品的图像特征对它们的集合进行排名。这些查询中的大多数是搜索具有特定特征的产品的名词短语。候选商品图片由卖家提供的照片，通过黑盒功能转化为2048维特征。与查询最相关的候选产品被视为查询的基本事实。

[aister2020/KDDCUP_2020_Debiasing_1st_Place](https://github.com/aister2020/KDDCUP_2020_Debiasing_1st_Place) 去偏Debiasing中获得第一名。侧重于暴露的复杂性，即如何推荐过去很少暴露的项目，以对抗推荐系统中经常遇到的马太效应。特别是，在对点击数据进行训练时减少偏差对于此任务的成功至关重要。就像现代推荐系统中记录的点击数据和实际在线环境之间存在差距一样，训练数据和测试数据之间也会存在差距，主要是在趋势和项目的流行度方面。

[RUCAIBox/FMLP-Rec](https://github.com/RUCAIBox/FMLP-Rec) 堆叠多个过滤器增强块以生成用于推荐的顺序用户偏好的表示。我们的方法与 SASRec 的主要区别在于用一种新颖的过滤器结构（傅里叶变换MLP）替换了 Transformer 中的多头自注意力结构。

[RUCAIBox/NCL](https://github.com/RUCAIBox/NCL) 通过邻域丰富的对比学习改进图协同过滤。

[alibaba/HybridBackend](https://github.com/alibaba/HybridBackend) 用于在异构集群上训练广泛和深度推荐系统的高性能框架

[CAN-Paper/Co-Action-Network](https://github.com/CAN-Paper/Co-Action-Network) CAN的实现：重新审视点击率预测的特征协同作用

[tsinghua-fib-lab/CLSR](https://github.com/tsinghua-fib-lab/CLSR) 解开推荐的长期和短期利益

[easezyc/Multitask-Recommendation-Library](https://github.com/easezyc/Multitask-Recommendation-Library) 提供了多任务推荐模型和通用数据集的 PyTorch 实现。

[awarebayes/RecNN](https://github.com/awarebayes/RecNN) 围绕 pytorch构建的强化学习推荐工具包

[Tencent/embedx](https://github.com/Tencent/embedx) 基于 c++ 开发的、完全自研的分布式 embedding 训练和推理框架。它目前支持 图模型、深度排序、召回模型和图与排序、图与召回的联合训练模型等

[bytedance/LargeBatchCTR](https://github.com/bytedance/LargeBatchCTR) 基于 DeepCTR 和 CowClip 的 CTR 模型的大批量训练。

[xiangwang1223/disentangled_graph_collaborative_filtering](https://github.com/xiangwang1223/disentangled_graph_collaborative_filtering) 解缠结图协同过滤 一个可解释的推荐框架，它配备了 (1) 胶囊网络的动态路由机制，以细化意图感知图中用户-项目交互的强度，(2) 图的嵌入传播机制神经网络，从高阶连通性中提取相关信息，以及（3）独立建模的距离相关性，以确保意图之间的独立性。因此，我们明确地解开了用户在表示学习中的隐藏意图。

[gusye1234/LightGCN-PyTorch](https://github.com/gusye1234/LightGCN-PyTorch) 旨在简化 GCN 的设计，使其更简洁，更适合推荐。提出了名为 LightGCN 的新模型，仅包含 GCN 中最重要的组件—邻域聚合—用于协同过滤

[muhanzhang/IGMC](https://github.com/muhanzhang/IGMC) 基于图神经网络的归纳矩阵补全模型，不使用任何边信息。 传统的矩阵分解方法将（评级）矩阵分解为行（用户）和列（项目）的低维潜在嵌入的乘积，这是转导的，因为学习的嵌入不能推广到看不见的新矩阵。为了使矩阵完成归纳，必须事先使用内容（辅助信息），如年龄或电影的类型。然而，高质量内容并不总是可用，而且很难提取。IGMC 通过训练一个GNN来实现，该网络完全基于从评分矩阵形成的二分图中提取的（用户、项目）对周围的局部子图，并将子图映射到其相应的评分。它不依赖于特定评分矩阵或任务的任何全局信息，也不学习特定于观察到的用户/项目的嵌入。因此，它是一个完全归纳模型，它可泛化到训练时看不见的用户/项目（假设交互存在），甚至可以迁移到新任务，从 MovieLens训练出来的模型可以直接用于预测豆瓣电影评分，并且效果出奇的好。

[jennyzhang0215/STAR-GCN](https://github.com/jennyzhang0215/STAR-GCN) 用于推荐系统的堆叠和重构图卷积网络

[wenqifan03/GraphRec-WWW19](https://github.com/wenqifan03/GraphRec-WWW19) 用于社交推荐的图神经网络

[PeiJieSun/diffnet](https://github.com/PeiJieSun/diffnet) 基于图神经网络的社交推荐模型。SIGIR2019。

[hwwang55/KGCN](https://github.com/hwwang55/KGCN) 用于推荐系统的知识图卷积网络，它使用图卷积网络（GCN）技术来处理知识图谱以达到推荐的目的。

[huangtinglin/Knowledge_Graph_based_Intent_Network](https://github.com/huangtinglin/Knowledge_Graph_based_Intent_Network) 与推荐知识图交互背后的学习意图，WWW2021

[amzn/pecos](https://github.com/amzn/pecos) 巨大和相关空间的预测 。用于对具有大输出空间的问题进行快速学习和推理，例如极端多标签排序 (XMR) 和大规模检索。

[summmeer/session-based-news-recommendation](https://github.com/summmeer/session-based-news-recommendation) 通过利用不同类型的隐式反馈，我们减轻了精度和多样性与冷启动问题之间的权衡，这对于实际应用是有效的。命名为 TCAR（时间和内容感知推荐系统）

[ahmedrashed-ml/CARCA](https://github.com/ahmedrashed-ml/CARCA) 通过交叉注意的上下文和属性感知顺序推荐，RecSys 2022

[Coder-Yu/SELFRec](https://github.com/Coder-Yu/SELFRec) 一个用于自我监督推荐 (SSR) 的 Python 框架，它集成了常用的数据集和指标，并实现了许多最先进的 SSR 模型。 SELFRec 具有轻量级架构并提供用户友好的界面。 它可以促进模型的实施和评估。
