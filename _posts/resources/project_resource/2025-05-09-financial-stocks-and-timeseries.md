---
layout: post
title: "金融股票与时间序列"
date: 2025-05-09
tags: 
  - Financial Stocks
  - TimeSeries
categories: 
  - Resource
comments: true
author: deathwhispers
---



## 金融股票

https://github.com/microsoft/qlib Qlib是一个面向AI的量化投资平台，旨在实现潜力，增强研究能力并创造AI技术在量化投资中的价值。包括多个模型。

https://github.com/QUANTAXIS/QUANTAXIS 量化金融策略框架

https://github.com/ricequant/rqalpha 从数据获取、算法交易、回测引擎，实盘模拟，实盘交易到数据分析，为程序化交易者提供了全套解决方案

https://github.com/cedricporter/funcat 将同花顺、通达信、文华财经麦语言等的公式写法移植到了 Python

https://github.com/georgezouq/awesome-deep-reinforcement-learning-in-finance 金融市场上使用的那些AI（RL/DL/SL/进化/遗传算法）的集合

https://github.com/wangshub/RL-Stock 如何用深度强化学习自动炒股。

https://github.com/tensortrade-org/tensortrade 一个开源强化学习框架，用于训练，评估和部署强大的交易程序。

[OpenBB-finance/OpenBBTerminal](https://github.com/OpenBB-finance/OpenBBTerminal) 适合每个人、任何地方的投资研究。OpenBB致力于通过专注于每个人都可以访问的开源基础架构来构建投资研究的未来。

https://github.com/bsolomon1124/pyfinance 为投资管理和证券收益分析而构建的Python分析包。主要是对面向定量金融的现有包进行补充，如pyfolio和pandas-datareader等。pyfinance包含六个模块，它们分别是：datasets.py ：金融数据下载，基于request进行数据爬虫；general.py：通用财务计算，例如主动份额计算，收益分配近似值和跟踪误差优化；ols.py：回归分析，支持pandas滚动窗口回归；options.py：期权衍生品计算和策略分析；returns.py：通过CAPM框架对财务时间序列进行统计分析，旨在模拟FactSet Research Systems和Zephyr等软件的功能，并提高了速度和灵活性；utils.py：基础架构。

https://github.com/quantopian/alphalens Python量化分析库，量化网站quantopian开发维护的量化三件套之一，用于股票因子(alpha)的性能分析。alphalens与zipline以及pyfolio常常一同使用，其中，pyfolio提供财务组合的性能和风险分析，zipline用于量化策略回测。alphalens的主要功能包括对一个alpha因子进行统计和绘图，包括：因子收益分析、因子信息系数分析、换手率分析以及分组分析。

https://github.com/quantopian/pyfolio 用于金融投资组合的性能和风险分析。它可以很好地与Zipline回测库一起工作。

https://github.com/quantopian/zipline 美国著名的量化策略平台quantopian开发和维护的量化交易库，并且quantopian量化平台的回测引擎也是基于zipline的，除此之外，像国内比较有名的三大矿聚宽(JointQuant)、米筐(RiceQuant)、优矿的回测引擎也是基于此。另外，由于quantopian平台多年的使用，zipline的专业性是可以保证的，并且zipline在github中的代码也在保持不断更新和改进。zipline是一种事件驱动（event-driven）的回测框架，有完整的文档和社区，如果你是对国外美股交易感兴趣，那么zipline将比较合适；但是对于国内像A股的数据则无法支持，只能通过本地化的数据进行回测。

https://github.com/gbeced/pyalgotrade 一个事件驱动的回测框架，虽然不如zipline的名气大，但是同样也具有完善的社区和详细的文档。据说pyalgotrade的运行速度和灵活度要比zipline强，但是缺点是不支持pandas。

https://github.com/mementum/backtrader 一个功能强大的量化策略回测平台。backtrader允许你专注于编写可重用的交易策略、指标和分析工具，而不是花时间构建基础设施。

https://github.com/enigmampc/catalyst 对于虚拟货币交易的量化回测平台。Catalyst是一个底层基于zipline的算法交易框架，目前比较成熟，并且可以支持策略的回测与实盘（ 目前支持四家交易所 Binance, Bitfinex, Bittrex, Poloniex) 。

https://github.com/vnpy/vnpy 国内由陈晓优团队开发量化交易框架，它目前在github上star和fork的数量已经超过了zipline，目前是全球开源量化框架的首位。vn.py主要侧重于实盘交易，同样支持通过历史数据进行回测，包括数据的可视化、收益结果、参数调优等，除此之外，它还具备一些常用的CTA策略、SpreadTrading价差交易、行情录制等功能，并且它还具备完善的社区以及教程。新手在使用时，可以通过它的GUI环境VN Station进行使用，同时也可以基于它的策略模版进行自定义的策略开发。

https://github.com/waditu/tushare 拥有丰富的数据内容，如股票、基金、期货、数字货币等行情数据，公司财务、基金经理等基本面数据。其SDK开发包支持语言，同时提供HTTP Restful接口，最大程度方便不同人群的使用。并且，它提供多种数据储存方式，如Oracle、MySQL，MongoDB、HDF5、CSV等，为数据获取提供了性能保证。

https://github.com/jindaxiang/akshare 基于 Py 的财经数据接口库, 目的是实现对股票、期货、期权、基金、外汇、债券、指数、加密货币等金融产品的基本面数据、实时和历史行情数据、衍生数据从数据采集、数据清洗到数据落地的一套工具, 主要用于学术研究目的。特点是获取的是相对权威的财经数据网站公布的原始数据, 通过利用原始数据进行各数据源之间的交叉验证, 进而再加工, 从而得出科学的结论。

[AI4Finance-LLC/FinRL-Library](https://github.com/AI4Finance-LLC/FinRL-Library) 哥大开源“FinRL”: 一个用于量化金融自动交易的深度强化学习库

[Heerozh/spectre](https://github.com/Heerozh/spectre) GPU 加速的因子分析库和回测工具。

[midas-research/sthan-sr-aaai](https://github.com/midas-research/sthan-sr-aaai) 通过时空超图注意力网络进行股票选择：一种学习排名方法

[yumoxu/stocknet-dataset](https://github.com/yumoxu/stocknet-dataset) 从推文和历史股价预测股票走势的综合数据集。

[goiter/CoCPC](https://github.com/goiter/CoCPC) 基于 Copula 的对比预测编码 (Co-CPC)。通过考虑与宏观经济指标的耦合来发布股票走势预测的代码和数据。

[hkgsas/LOB](https://github.com/hkgsas/LOB) 中国市场限价订单短期市场预测基准数据集。

[jrothschild33/learn_backtrader: ](https://github.com/jrothschild33/learn_backtrader) BackTrader中文教程笔记，系统性介绍Bactrader的特性、策略构建、数据结构、回测交易等，彻底掌握量化神器的使用方法。章节：介绍篇、数据篇、指标篇、交易篇、策略篇、可视化篇…

[AI4Finance-Foundation/FinRL-Meta](https://github.com/AI4Finance-Foundation/FinRL-Meta) 数据驱动金融强化学习的市场环境和基准

[AI4Finance-Foundation/FinRL-Live-Trading](https://github.com/AI4Finance-Foundation/FinRL-Live-Trading) 自动股票交易的深度强化学习：一种集成策略。ICAIF 2020。

[AI4Finance-Foundation/DQN-DDPG_Stock_Trading](https://github.com/AI4Finance-Foundation/DQN-DDPG_Stock_Trading) 使用 DQN/DDPG 进行股票交易。Xiong, Z.、Liu, XY、Zhong, S.、Yang, H. 和 Walid, A.，2018 年。股票交易的实用深度强化学习方法，NeurIPS 2018 AI in Finance Workshop。

[AI4Finance-Foundation/FinRL_Podracer](https://github.com/AI4Finance-Foundation/FinRL_Podracer) 一个优雅（轻量级、高效且稳定）的 FinRL 库，允许研究人员和量化交易者轻松开发算法策略。

[tkfy920/qstock](https://github.com/tkfy920/qstock) 打造成个人量化投研分析包，目前包括数据获取（data）、可视化(plot)、选股(stock)和量化回测（策略backtest）模块。 qstock将为用户提供简洁的数据接口和规整化后的金融市场数据。可视化模块为用户提供基于web的交互图形的简单接口； 选股模块提供了同花顺的选股数据和自定义选股，包括RPS、MM趋势、财务指标、资金流模型等； 回测模块为大家提供向量化（基于pandas）和基于事件驱动的基本框架和模型。

[je-suis-tm/quant-trading](https://github.com/je-suis-tm/quant-trading) Python 量化交易策略，包括 VIX 计算器、模式识别、商品交易顾问、蒙特卡洛、期权跨式、射击之星、伦敦突破、Heikin-Ashi、配对交易、RSI、布林带、抛物线 SAR、双推力、真棒、MACD

[AlgoTraders/stock-analysis-engine](https://github.com/AlgoTraders/stock-analysis-engine) 回测 1000 种每分钟交易算法，使用来自 IEX、Tradier 和 FinViz 的自动定价数据训练 AI。数据集和交易表现自动发布到 S3，用于构建 AI 训练数据集，以教授 DNN 如何交易。在 Kubernetes 和 docker-compose 上运行。

[amor71/LiuAlgoTrader](https://github.com/amor71/LiuAlgoTrader) 一个可扩展的、多进程的 ML 就绪框架，用于有效的算法交易。该框架简化了开发、测试、部署、分析和训练算法交易策略。该框架自动分析交易会话、超参数优化，分析可用于训练预测模型。

## 时间序列

[thuml/Autoformer](https://github.com/thuml/Autoformer) 用于长期序列预测的具有自相关性的分解变压器。Autoformer超越了Transformer系列，首次实现了串联。在六个基准上进行实验，涵盖五个主流应用程序。我们将我们的模型与十个基线进行比较，包括 Informer、N-BEATS 等。通常，对于长期预测设置，Autoformer 实现了 SOTA，相对于之前的基线有38% 的相对改进。

[alan-turing-institute/sktime](https://github.com/alan-turing-institute/sktime) 时间序列的机器学习统一框架 。包括时间序列分类、回归、聚类、注释和预测。

[jdb78/pytorch-forecasting](https://github.com/jdb78/pytorch-forecasting) pytorch的时间系列预测库，模型包括：RecurrentNetwork、DecoderMLP、NBeats 、DeepAR 、TemporalFusionTransformer。

[qingsongedu/time-series-transformers-review](https://github.com/qingsongedu/time-series-transformers-review) 专业策划的关于时间序列的变压器的很棒的资源（论文、代码、数据等）列表。

[arrigonialberto86/deepar](https://github.com/arrigonialberto86/deepar) Amazon于2017年提出的基于深度学习的时间序列预测方法

[fjxmlzn/DoppelGANger](https://github.com/fjxmlzn/DoppelGANger) 使用GAN共享网络时间序列数据：挑战，初步承诺和未解决的问题，IMC 2020（最佳论文入围）

[AIStream-Peelout/flow-forecast](https://github.com/AIStream-Peelout/flow-forecast) 一个开源的深度学习时间序列预测库。包括模型：Vanilla LSTM、Full transformer、Simple Multi-Head Attention、Transformer w/a linear decoder、DA-RNN (CPU only for now)。

[tslearn-team/tslearn](https://github.com/tslearn-team/tslearn) 时间序列机器学习python工具包，其中包括了一些基本的时间序列预测或者分类模型，如多层感知机，SVR，KNN以及基本的数据预处理工具和数据集的生成与加载模块。

[blue-yonder/tsfresh](https://github.com/blue-yonder/tsfresh) 时间序列特征提取python工具包，它会自动计算出大量的时间序列特征。此外，该工具包还包含了一些方法，用于评估回归或分类任务中这些特征的解释能力和重要性。

[johannfaouzi/pyts](https://github.com/johannfaouzi/pyts) 时间序列分类工具包。提供预处理工具及若干种时间序列分类算法。

[PaddlePaddle/PaddleTS](https://github.com/PaddlePaddle/PaddleTS) 基于PaddlePaddle的易于使用的深度时间序列建模，包括TSDataset，分析，转换，模型，AutoTS和Ensemble等综合功能模块，支持时间序列预测，表示学习和异常检测等多功能任务。

[linkedin/greykite](https://github.com/linkedin/greykite) Greykite 库通过其旗舰算法 Silverkite 提供灵活、直观和快速的预测。Silverkite 算法适用于大多数时间序列，尤其适用于趋势或季节性变化点、事件/假日效应和时间依赖性的那些。它是可解释的，因此对于值得信赖的决策和洞察力很有用。

[zhouhaoyi/Informer2020](https://github.com/zhouhaoyi/Informer2020) 效果远超Transformer的长序列预测，提出了ProbSparse self-attention机制来高效的替换常规的self-attention并且获得了的O（LlogL)时间复杂度以及O(LlogL)的内存使用率,提出了self-attention distilling操作，它大幅降低了所需的总空间复杂度O((2-e)LlogL)；我们提出了生成式的Decoder来获取长序列的输出，这只需要一步，避免了在inference阶段的累计误差传播；

[deeptime-ml/deeptime](https://github.com/deeptime-ml/deeptime) 用于分析时间序列数据，包括降维，聚类和马尔可夫模型估计

[unit8co/darts](https://github.com/unit8co/darts) python 库，用于对时间序列进行用户友好的预测和异常检测。

[bashtage/arch](https://github.com/bashtage/arch) 自回归条件异方差 (ARCH) 和其他金融计量经济学工具，用 Python 编写（使用 Cython 和/或 Numba 来提高性能）

https://github.com/nnzhan/MTGNN 通用的图神经网络框架 MTGNN，通过图学习模块融合外部知识和变量之间的单向关系，再使用 mix-hop 传播层和膨胀 inception 捕获空间和时序依赖。

https://github.com/VachelHU/EvoNet Time-Series Event Prediction with Evolutionary State Graph 将时间序列转化为动态图进行表示的方法。该方法成功在阿里云 ·SLS 商业化，作为一项智能巡检服务，可以对大规模时间序列进行异常检测与分析。

https://github.com/microsoft/StemGNN 基于图谱分解的时间序列预测。进一步提高多元时间序列预测的准确性。StemGNN 在spectral domain中捕获系列间(inter-series)相关性和时间依赖性(temporal dependencies)。它结合了图傅立叶变换 (GFT) 和离散傅立叶变换 (DFT)，GFT对序列间(inter-series)相关性进行建模，而离散傅立叶变换 (DFT) 则对端到端框架中的时间依赖性(temporal dependencies)进行建模。通过 GFT 和 DFT 后，谱表示具有清晰的模式，可以通过卷积和序列学习模块进行有效预测。

[fulifeng/Temporal_Relational_Stock_Ranking](https://github.com/fulifeng/Temporal_Relational_Stock_Ranking) 基于图神经网络、图谱型数据的收益预测模型

https://github.com/emadeldeen24/TS-TCC 一个无监督的时间序列表示学习框架，通过时间和上下文对比。

https://github.com/nnzhan/MTGNN 基于图神经网络的多变量时间序列预测模型

[adarnn](https://github.com/jindongwang/transferlearning/tree/master/code/deep/adarnn) 提出自适应的RNN模型，使得其可以更好地泛化。由时序相似性量化和时序分布匹配算法组成，前者用于表征时序中的分布信息，后者通过分布匹配构建广义RNN模型。

https://github.com/facebookresearch/Kats 用于分析时间系列数据的工具包，轻量级、易于使用、通用和可扩展的框架，用于执行时间系列分析，从了解关键统计数据和特征、检测变化点和异常，到预测未来趋势。

https://github.com/slaypni/fastdtw 近似动态时间规整算法，提供与 O（N）时间和内存复杂性的最佳或接近最佳对齐。

https://github.com/ourownstory/neural_prophet 基于神经网络的时间系列模型，灵感来自 Facebook Prophet 和 AR-Net，建立在 PyTorch 之上。

https://github.com/jsyoon0823/TimeGAN 时间序列生成对抗网络

[lucidrains/perceiver-pytorch](https://github.com/lucidrains/perceiver-pytorch) 具有迭代注意的通用感知器,利用非对称注意力机制将输入迭代地提取到一个紧密的潜在空间中，使其能够扩展以处理非常大的输入。

[alasdairtran/radflow](https://github.com/alasdairtran/radflow) [TheWebConf 2021] Radflow：时间序列网络的循环、聚合和可分解模型

[https://github.com/eBay/RANSynCoders](https://github.com/eBay/RANSynCoders) 一种无监督的深度学习架构，用于在大型多元时间序列中进行实时异常检测和定位。

[gzerveas/mvts_transformer](https://github.com/gzerveas/mvts_transformer) 多元时间序列转换器框架

[zhhlee/InterFusion](https://github.com/zhhlee/InterFusion) KDD 2021：使用分层度量间和时间嵌入的多变量时间序列异常检测和解释

[NSIBF/NSIBF](https://github.com/NSIBF/NSIBF) 通过神经系统识别和贝叶斯过滤对网络物理系统进行时间序列异常检测

[winedarksea/AutoTS](https://github.com/winedarksea/AutoTS) AutoTS 是 Python 的时间序列包，旨在快速大规模部署高精度预测。

[facebookresearch/transformer-sequential](https://github.com/facebookresearch/transformer-sequential) 两篇论文的代码：Feedback Transformer 和 Expire-Span。用于使用类似 Transformer 的架构进行长序列建模。

[angus924/minirocket](https://github.com/angus924/minirocket) MINIROCKET：用于时间序列分类的非常快速（几乎）确定性转换

[EvilPsyCHo/Deep-Time-Series-Prediction](https://github.com/EvilPsyCHo/Deep-Time-Series-Prediction) Seq2Seq、Bert、Transformer、WaveNet 用于时间序列预测。

[locuslab/TCN](https://github.com/locuslab/TCN) 序列建模基准和时间卷积网络

[jambo6/neuralRDEs](https://github.com/jambo6/neuralRDEs) 长时间序列的神经粗糙微分方程

[sktime/sktime-dl](https://github.com/sktime/sktime-dl) 基于TensorFlow的深度学习sktime配套包

[jiwidi/time-series-forecasting-with-python](https://github.com/jiwidi/time-series-forecasting-with-python) 使用 python 进行时间序列预测的以用例为中心的教程

[timeseriesAI/tsai](https://github.com/timeseriesAI/tsai) 时间序列 Timeseries 深度学习 机器学习 Pytorch fastai | Pytorch / fastai 中用于时间序列和序列的最先进的深度学习库

[Alro10/deep-learning-time-series](https://github.com/Alro10/deep-learning-time-series) 使用深度学习进行时间序列预测的论文、代码和实验列表

[ElementAI/N-BEATS](https://github.com/ElementAI/N-BEATS) 基于神经网络的单变量时间序列预测模型

[yuezhihan/ts2vec](https://github.com/yuezhihan/ts2vec) 一个通用的时间序列表示学习框架

[firmai/atspy](https://github.com/firmai/atspy) Python 中的自动化时间序列模型

[cesium-ml/cesium](https://github.com/cesium-ml/cesium) 用于时间序列推理的开源平台。从原始时间序列数据中提取特征，构建机器学习模型，为新数据生成预测。

[zhengqi98/Hefei_ECG_TOP1](https://github.com/zhengqi98/Hefei_ECG_TOP1) “合肥高新杯”心电人机智能大赛 —— 心电异常事件预测 TOP1 Solution,依据心电图机8导联的数据和年龄、性别特征，预测心电异常事件

[thuml/Anomaly-Transformer](https://github.com/thuml/Anomaly-Transformer) 基于关联偏差的时间序列异常检测

[thuml/Nonstationary_Transformers](https://github.com/thuml/Nonstationary_Transformers) 非平稳时间序列的通用预测框架。非平稳的时序数据具有更复杂且难以捕捉的时序依赖，以及随着时间不断变化的数据分布，以往的研究旨在利用平稳化技术消除数据在时间维度上的分布差异，以提高数据本身的可预测性。然而在平稳化后的数据上进行模型训练会限制Transformer建模时序依赖的能力，导致模型仅能学到不易区分的注意力图与较弱的时序依赖，从而产生平稳性过高的预测输出与较大的预测误差，我们称之为过平稳现象（Over-stationarization）。针对非平稳时序预测问题，提出了Non-stationary Transformers，其包含一对相辅相成的序列平稳化（Series Stationarization）和去平稳化注意力（De-stationary Attention）模块，能够广泛应用于Transformer以及变体，一致提升其在非平稳时序数据上的预测效果。

[microprediction/timemachines](https://github.com/microprediction/timemachines) 利用流行的python时间序列包的功能，如river，pydlm，tbats，pmdarima，statsmodels.tsa，neuralprophet，Facebook Prophet，Uber的orbit，Facebook的greykitite等。

