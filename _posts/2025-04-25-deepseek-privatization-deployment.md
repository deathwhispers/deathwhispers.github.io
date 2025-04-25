---
layout: post
title: "Deepseek私有化部署"
date: 2025-02-13
tags: [DeepSeek, 私有化部署]
comments: true
author: deathwhispers
---

# Linux 安装 ollama

## 自动安装

1. 进入[官网下载页面](https://ollama.com/download/linux)
2. 一行命令自动下载并安装 `curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh`

<aside>
💡


⚠️需要注意网络问题，直接访问ollama会比较卡，网速很慢，极大可能下载失败。

</aside>

---

## 手动安装

<aside>
💡


如果您正在从先前的版本中升级，则应首先使用`sudo rm -rf /usr/lib/ollama` 删除旧库。

</aside>

### **1. 确认系统要求**

- **操作系统**：支持 Ubuntu、Debian、CentOS 等主流 Linux 发行版。
- **依赖**：确保已安装 `curl` 和 `tar` 工具。

### **2. 下载 Ollama 安装包**

1. 访问 Ollama 的官方网站或 GitHub 仓库，获取最新的 Linux 安装包（如 `.tar.gz` 或 `.deb` 文件）。
2. 使用 `curl` 或 `wget` 下载安装包：

```bash
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
```

<aside>
⚠️


需要注意网络问题，ollama官网下载速度很慢，可以找[**镜像网站**](https://sourceforge.net/projects/ollama.mirror/)去下载，选择与服务器相匹配的版本。

</aside>

### **3. 解压安装包**

1. 使用 `tar` 解压下载的文件：

```bash
sudo tar -C /usr -xzf ollama-linux-amd64.tgz
```

1. 启动 Ollama

```bash
ollama serve
```

1. 新开启一个终端窗口，测试服务是否启动

```bash
ollama -v
```

### **4. 配置为系统服务（可选）**

1. 为 Ollama 创建用户及用户组

```bash
sudo useradd -r -s /bin/false -U -m -d /usr/share/ollama ollama
sudo usermod -a -G ollama $(whoami)
```

1. 创建 systemd 服务文件`/etc/systemd/system/ollama.service`:

```bash
sudo vim /etc/systemd/system/ollama.service
```

1. 添加以下内容：

```bash
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=$PATH"
# 自定义监听的端口，默认为：127.0.0.1:11434
#Environment="OLLAMA_HOST=0.0.0.0:11434” 

[Install]
WantedBy=default.target
```

<aside>
💡


⚠️默认的ollama配置启动后，仅监听127.0.0.1:11434。需要配置监听范围及监听端口Environment="OLLAMA_HOST=0.0.0.0:11434”

</aside>

1. 启用并启动服务：

```bash
sudo systemctl enable ollama

sudo systemctl start ollama
```

1. 启动Ollama并验证运行状态：

```bash
# 启动 ollama
sudo systemctl start ollama
# 查看 ollama 运行状态
sudo systemctl status ollama
```

![image.png](../images/deepseek-privatization-deployment/image.png)

ollama -v 显示：

![image.png](../images/deepseek-privatization-deployment/image%201.png)

<aside>
⚠️


特别注意：当在`/etc/systemd/system/ollama.service` 中**修改了监听端口**后，即使通过systemctl 的方式启动成功，在运行 ollama -v 命令时也会提示无法连接到运行的 ollama 服务上。同时会影响后续下载模型的命令，同样会提示无法连接到 ollama 服务，导致服务下载模型。

</aside>

### 5. 自定义

要自定义Ollama的安装，您可以通过运行来编辑Systemd服务文件或环境变量：

```bash
sudo systemctl edit ollama
```

或者，手动创建一个覆盖文件 `/etc/systemd/system/ollama.service.d/override.conf` ：

```bash
[Service]
Environment="OLLAMA_DEBUG=1"
```

### **6. 更新**

通过再次运行安装脚本来更新Ollama：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

或者，重新下载 Ollama 安装包：

```bash
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
sudo tar -C /usr -xzf ollama-linux-amd64.tgz
```

<aside>
⚠️


需要注意网络问题，ollama官网下载速度很慢，可以找[**镜像网站**](https://sourceforge.net/projects/ollama.mirror/)去下载，选择与服务器相匹配的版本。

</aside>

### 7. 安装特定版本

将Ollama_version环境变量与安装脚本一起安装特定版本的Ollama，包括预释放。

可以从发行版中找到版本号

比如：

```bash
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION=0.5.7 sh
```

### 8. 查看运行日志

```bash
journalctl -e -u ollama
```

### 9. 卸载

卸载 ollama 服务：

```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service
```

从以下bin目录中删除Ollama二进制文件

- /usr/local/bin
- /usr/bin
- /bin

```bash
sudo rm $(which ollama)
```

删除下载的模型和Ollama服务用户和组：

```bash
sudo rm -r /usr/share/ollama
sudo userdel ollama
sudo groupdel ollama
```

删除已安装的库：

```bash
sudo rm -rf /usr/local/lib/ollama
```

# 拉取并安装 DeepSeek

![image.png](../images/deepseek-privatization-deployment/image%202.png)

目前DeepSeek-R1可选的模型有满血版671B，和蒸馏版1.5B、7B、8B、14B、32B、70B：

每个版本及对应的电脑硬件要求：

## **DeepSeek-R1 模型硬件要求**

| **模型版本**         | **CPU 核心数** | **内存** | **存储大小** | **存储类型** | **GPU 显存** | **GPU 型号**                                     | **应用场景**                                                 |
| -------------------- | -------------- | -------- | ------------ | ------------ | ------------ | ------------------------------------------------ | ------------------------------------------------------------ |
| **DeepSeek-R1-671B** | 64 核 +        | 512 GB   | 1 TB +       | SSD          | 256GB+       | 多节点分布式训练（如 8x A100/H100）              | 超大规模 AI 研究、通用人工智能（AGI）探索                    |
| **DeepSeek-R1-1.5B** | 4 核 +         | 8GB +    | 16GB +       | SSD          | 4GB +        | 非必需（纯 CPU 推理），若 GPU 加速可选 4GB+ 显存 | 低资源设备部署，如树莓派、旧款笔记本、嵌入式系统或物联网设备 |
| **DeepSeek-R1-7B**   | 8 核 +         | 16GB +   | 32GB +       | SSD          | 8GB +        | 推荐 8GB+ 显存（如 RTX 3070/4060）               | 中小型企业本地开发测试、中等复杂度 NLP 任务，例如文本摘要、翻译、轻量级多轮对话系统 |
| **DeepSeek-R1-8B**   | 8 核 +         | 16GB +   | 32GB +       | SSD          | 8GB +        | 推荐 8GB+ 显存（如 RTX 3070/4060）               | 需更高精度的轻量级任务（如代码生成、逻辑推理）               |
| **DeepSeek-R1-14B**  | 12 核 +        | 32GB +   | 32GB +       | SSD          | 16GB +       | 16GB+ 显存（如 RTX 4090 或 A5000）               | 企业级复杂任务、长文本理解与生成                             |
| **DeepSeek-R1-32B**  | 16 核 +        | 64GB +   | 64GB +       | SSD          | 24GB +       | 24GB+ 显存（如 A100 40GB 或双卡 RTX 3090）       | 高精度专业领域任务、多模态任务预处理                         |
| **DeepSeek-R1-70B**  | 32 核 +        | 128GB +  | 128GB +      | SSD          | 64GB +       | 多卡并行（如 2x A100 80GB 或 4x RTX 4090）       | 科研机构/大型企业、高复杂度生成任务                          |

### **硬件要求说明**：

- **CPU 核心数**: 每个版本对 CPU 核心数的要求决定了计算处理的能力，核心数越多，系统可以同时处理更多的任务。
- **推荐 CPU 型号**: 根据不同版本的规模和计算需求，推荐的 CPU 型号帮助选择性能合适的处理器。
- **内存**: 用于存储模型的中间结果和大规模数据。模型越大，对内存的需求也就越高。
- **存储类型与大小**: 推荐使用 SSD，尤其是 NVMe SSD，能够提供更快的数据读取和写入速度。存储大小根据模型和数据量的要求而不同。
- **GPU 数量与显卡型号**: GPU 用于加速深度学习模型的训练和推理。GPU 数量决定了计算的并行能力，显卡型号影响性能。
- **GPU 显存**: 显存大小决定了每个 GPU 能处理的模型大小，显存越大，能够处理的模型也就越大。

<aside>
💡


当使用纯CPU推理时，对CPU和内存的要求更高。

</aside>

## 下载模型

运行下面的命令，下载对应的模型

```bash
ollama run deepseek-r1:7B
```

![image.png](../images/deepseek-privatization-deployment/image%203.png)

安装成功后的界面

![image.png](../images/deepseek-privatization-deployment/image%204.png)

可以直接使用了，简单提问试一下：

![image.png](../images/deepseek-privatization-deployment/image%205.png)

### **安装 Page Assist**

安装**Page Assist**

通过 Chrome应用商店安装扩展插件，进入应用市场，搜索Page Assist

![image.png](../images/deepseek-privatization-deployment/image%206.png)

点击扩展插件，就可以看到刚刚加载的插件，点击📌将插件固定到浏览器中，方便以后随时打开使用

![image.png](../images/deepseek-privatization-deployment/image%207.png)

点击插件图标就可以打开UI界面了，和chatGPT的聊天界面类似，可以选择对应的模型开始提问。

![image.png](../images/deepseek-privatization-deployment/image%208.png)

点击模型下拉框，可以查看已经安装的模型，目前已经安装了1.5B和7B的deepseek蒸馏版模型。

![image.png](../images/deepseek-privatization-deployment/image%209.png)

接下来，可以选择一个模型提问试试

![image.png](../images/deepseek-privatization-deployment/image%2010.png)

此时服务器CPU情况，推理速度很慢，且服务器资源占用量很大。

![image.png](../images/deepseek-privatization-deployment/image%2011.png)

点击右上角的齿轮进入设置页面，可以进行一些基础的设置，如语言，语音识别语言等等。

同时可以管理网络搜索，选择搜索引擎，是否默认联网搜索等。

![image.png](../images/deepseek-privatization-deployment/image%2012.png)

![image.png](../images/deepseek-privatization-deployment/image%2013.png)

在“OpenAI 兼容 API”设置项中，会列出所有已添加的服务提供商，

![image.png](../images/deepseek-privatization-deployment/image%2014.png)

点击“添加提供商”可以添加新的大模型服务提供商

![image.png](../images/deepseek-privatization-deployment/image%2015.png)

比如，选择“DeepSeek”，会自动带出提供商名称和基础URL，当然也可以修改；填入对应的API key就可以使用了。

![image.png](../images/deepseek-privatization-deployment/image%2016.png)

添加完成后，点击下载按钮，可以下载对应的模型

![image.png](../images/deepseek-privatization-deployment/image%2017.png)

所有已下载的模型，可以在“管理模型”菜单中的 **Custom Models** 中列出

![image.png](../images/deepseek-privatization-deployment/image%2018.png)

“管理知识”菜单栏，可以添加本地知识库，让DeepSeek更专业。

![image.png](../images/deepseek-privatization-deployment/image%2019.png)

# 参考文档

1. [ollama官方仓库指引](https://github.com/ollama/ollama/blob/main/docs/linux.md)
2. [连接失败的解决方案](https://github.com/n4ze3m/page-assist/blob/main/docs/connection-issue.md)
3. [设置ollama监听在0.0.0.0](https://blog.csdn.net/ethnicitybeta/article/details/136237150)
4. [**如何在个人电脑上私有安装DeepSeek？彻底告别服务器繁忙！**](https://mp.weixin.qq.com/s/iKfE67M42ROWVCMTe6wbFA)
5. [**本地部署「DeepSeek」模型硬件配置要求**](https://xiaoyi.vc/deepseek-specs.html)
6. [**DeepSeek R1、V3的1.5b/7b/32b/70b和671b模型，本地部署硬件要求对应表**](https://aizhinan.cc/217)
7. [**解决DeepSeek通过Ollama本地部署报错问题**](https://blog.csdn.net/m0_73679357/article/details/145432758)
8. [Ollama模型下载地址](https://ollama.com/library)