# 可解释谣言检测系统,请老师务必完整阅读完



课程：人工智能导论大作业2026


---

## 1.项目简介

本项目实现了一个可解释谣言检测系统（Explainable Rumor Detection System），用于检测社交媒体推文是否为谣言，并生成可理解的解释文本。


## 2.系统整体流程

推文

&#x20; ↓

文本预处理

&#x20; ↓

BERTweet 分类器

&#x20; ↓

预测标签 + 置信度

&#x20; ↓

SJTU DeepSeek 大模型

&#x20; ↓

生成解释文本



## 3.项目结构

Rumor\_Detection/

├── README.md

├── requirements.txt

├── .env.example

├── data/

│   ├── train.csv

│   └── val.csv

├── checkpoints/

│   └── best\_model/

└── src/

&#x20;   ├── preprocess.py

&#x20;   ├── dataset.py

&#x20;   ├── model.py

&#x20;   ├── train.py

&#x20;   ├── evaluate.py

&#x20;   ├── infer.py

&#x20;   └── explain.py



## 4.环境配置

运行前需要执行 pip install torch pandas numpy scikit-learn requests transformers emoji ,详情见requirements.txt

！！！重要：
本项目使用了 vinai/bertweet-base 预训练模型。如果在国内网络环境下运行，初次下载模型权重极易超时卡死。
请在运行 train.py 前，务必在终端执行以下命令开启国内镜像加速：
export HF_ENDPOINT=https://hf-mirror.com



## 5.API配置

在交我办申请，获得api-key，在src/explain.py中输入自己的apikey


## 6.使用数据

数据集包含 “train.csv” 和 “val.csv”

数据量训练集约 3000 条，验证集约 500 条



## 7.模型结构

分类器：`vinai/bertweet-base`

输出：二分类

损失函数：CrossEntropyLoss

解释模块：SJTU DeepSeek 大模型



## 8.模型训练

保存在checkpoints/best\_model/bertweet.pth



## 9.项目亮点

使用 BERTweet 微调分类器保证分类精度

调用 SJTU 大模型生成可解释文本



