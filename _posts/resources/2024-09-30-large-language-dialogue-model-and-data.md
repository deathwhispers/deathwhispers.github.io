---
layout: post
title: "类chatgpt大语言对话模型及数据"
date: 2024-09-30
tags: 
  - LLM
  - Large Language Model
categories: 
  - Resource
comments: true
author: deathwhispers
created: 2025-11-28 09:57
updated: 2025-11-28 09:57
---





## 类ChatGPT大语言对话模型及数据

* [Significant-Gravitas/Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT#auto-gpt-an-autonomous-gpt-4-experiment) 使用GPT4来自动完成目标任务。一个实验性开源应用程序，展示了 GPT-4 语言模型的功能。该程序由 GPT-4 驱动，将 LLM 的“思想”链接在一起，以自主实现您设定的任何目标。作为 GPT-4 完全自主运行的首批示例之一，Auto-GPT 突破了 AI 的可能性界限。

* [AntonOsika/gpt-engineer](https://github.com/AntonOsika/gpt-engineer) GPT 工程师易于调整、扩展，它根据提示生成整个代码库。指定您希望它构建的内容，AI 要求澄清，然后构建它。

* [facebookresearch/llama](https://github.com/facebookresearch/llama) facebook LLaMA 模型的推理代码。最新版本的 Llama 现在可供各种规模的个人、创作者、研究人员和企业访问，以便他们可以负责任地进行实验、创新和扩展他们的想法。

* [THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 开源中英双语对话模型 ChatGLM-6B 的第二代版本，在保留了初代模型对话流畅、部署门槛较低等众多优秀特性的基础之上，引入了如下新特性：`更强大的性能`：全面升级了基座模型。ChatGLM2-6B 使用了 GLM 的混合目标函数，经过了 1.4T 中英标识符的预训练与人类偏好对齐训练，评测结果显示，相比于初代模型，MMLU（+23%）、CEval（+33%）、GSM8K（+571%） 、BBH（+60%）等数据集上的性能取得了大幅度的提升，在同尺寸开源模型中具有较强的竞争力。`更长的上下文`：基于 FlashAttention 技术，我们将基座模型的上下文长度（Context Length）由 ChatGLM-6B 的 2K 扩展到了 32K，并在对话阶段使用 8K 的上下文长度训练。对于更长的上下文，我们发布了 ChatGLM2-6B-32K 模型。LongBench 的测评结果表明，在等量级的开源模型中，32K 有着较为明显的竞争优势。`更高效的推理`：基于 Multi-Query Attention 技术，有更高效的推理速度和更低的显存占用：在官方的模型实现下，推理速度相比初代提升了 42%，INT4 量化下，6G 显存支持的对话长度由 1K 提升到了 8K。`更开放的协议`：权重对学术研究完全开放，在填写问卷进行登记后亦允许免费商业使用。

* [THUDM/ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) 开源的、支持中英双语的对话语言模型，基于 [General Language Model (GLM)](https://github.com/THUDM/GLM) 架构，具有 62 亿参数。结合模型量化技术，用户可以在消费级的显卡上进行本地部署（INT4 量化级别下最低只需 6GB 显存）。 ChatGLM-6B 使用了和 ChatGPT 相似的技术，针对中文问答和对话进行了优化。经过约 1T 标识符的中英双语训练，辅以监督微调、反馈自助、人类反馈强化学习等技术的加持，62 亿参数的 ChatGLM-6B 已经能生成相当符合人类偏好的回答。

* [THUDM/GLM-130B](https://github.com/THUDM/GLM-130B) GLM-130B是一个开放的双语（英汉）双向密集模型，具有1300亿个参数，使用通用语言模型（GLM）算法进行预训练。它旨在支持单个 A100 （40G * 8） 或 V100 （32G * 8） 上具有 130B 参数的推理任务。通过 INT4 量化，硬件可以进一步降低到具有 4 * RTX3090 24G 的单个服务器，几乎没有性能下降。

* [QwenLM/Qwen-7B](https://github.com/QwenLM/Qwen-7B) 由阿里云提出的Qwen-7B（通义千问-7B）聊天和预训练大语言模型的官方存储库。使用高质量的预训练数据进行训练。我们已经在超过2.2万亿个代币的自建大规模高质量数据集上预训练了Qwen-7B。该数据集包括纯文本和代码，涵盖广泛的领域，包括一般领域数据和专业领域数据。更好地支持语言。我们的分词器基于超过 150K 个代币的大词汇表，与其他分词器相比更有效。它对多种语言都很友好，并且有助于用户进一步微调Qwen-7B以扩展对某种语言的理解。支持 8K 上下文长度。Qwen-7B和Qwen-7B-Chat都支持8K的上下文长度，这允许输入长上下文。支持插件。Qwen-7B-Chat 是用插件相关的对齐数据训练的，因此它能够使用工具，包括 API、模型、数据库等，并且能够作为代理进行游戏。

* [imoneoi/openchat](https://github.com/imoneoi/openchat) 使用不完善的数据推进开源语言模型。OpenChat是一系列基于监督微调（SFT）的开源语言模型。我们利用 ~80k ShareGPT 对话与条件反射策略和加权损失，尽管我们的方法很简单，但仍实现了卓越的表现。我们的最终愿景是开发一个高性能、开源和商用的大型语言模型，并且我们正在不断取得进展。

* [lonePatient/awesome-pretrained-chinese-nlp-models](https://github.com/lonePatient/awesome-pretrained-chinese-nlp-models) 高质量中文预训练模型集合。包括：基础大模型、对话大模型、多模态对话大模型、大模型评估基准、开源模型库平台、开源数据集库、中文指令数据集。

* [Vision-CAIR/MiniGPT-4](https://github.com/Vision-CAIR/MiniGPT-4) MiniGPT-4：使用高级大型语言模型增强视觉语言理解 提供与 Vicuna-7B 对齐的预训练 MiniGPT-4！演示 GPU 内存消耗现在可以低至 12GB。
- [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) 纯C/C++中LLaMA模型的CPU推理。2023年FacebookResearch 开源了大规模语言模型LLaMA，包含从 7B 到 65B 的参数范围，训练使用多达 1.4万亿 tokens 语料。LLaMA-13B在大部分基准测评上超过了GPT3-175B，LLaMA可能是目前公开模型权重中效果最好的语言模型。

- [juncongmoo/pyllama](https://github.com/juncongmoo/pyllama) LLaMA - 在单个 4GB GPU 中运行 LLM

- [tatsu-lab/stanford_alpaca](https://github.com/tatsu-lab/stanford_alpaca) 斯坦福大学的LLaMA羊驼模型。用2K数据微调模型，构建和共享一个遵循指令的LLaMA模型。
* [LC1332/Chinese-alpaca-lora](https://github.com/LC1332/Chinese-alpaca-lora) 在LLaMA、斯坦福大学Alpaca、Alpaca LoRA、Cabrita、Japanese-Alpaca-LoRA的基础上，调试了一个中国LLaMA模型。同时使用ChatGPT API将alpaca_data. json翻译为中文，再进行微调。

* [tloen/alpaca-lora](https://github.com/tloen/alpaca-lora) 在消费者硬件上使用指令来微调LLaMA模型。使用低秩自适应（LoRA）重现斯坦福大学Alpaca结果的代码。我们提供了一个与 text-davinci-003质量相似的Instruct模型，可以在Raspberry Pi上运行（用于研究），并且代码很容易扩展到 13b ， 30b 和 65b模型。

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
