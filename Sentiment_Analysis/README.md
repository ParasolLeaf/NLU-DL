# 评论情感分析系统

基于百度文心大模型 ERNIE 的评论情感分析系统，可以批量分析评论文本的情感倾向（积极、消极、中立），并生成可视化统计结果。

## 情感分析任务介绍

情感分析（Sentiment Analysis）是自然语言处理（NLP）中的重要任务之一，旨在从文本中识别和提取主观信息。它可以：

- 自动判断文本的情感倾向（积极、消极、中立）
- 帮助企业了解用户对产品或服务的态度
- 为决策制定提供数据支持
- 实现舆情监控和分析

本项目使用百度文心ERNIE大模型进行情感分析，相比传统机器学习方法具有以下优势：
- 更好的语义理解能力
- 更强的上下文把握能力
- 对新词和复杂表达的适应性更强
- 无需手动特征工程

## 数据集说明

本项目使用 ChnSentiCorp_htl_all 数据集进行评论情感分析。该数据集是中文情感分析领域的经典数据集之一：

- 来源：携程网酒店评论
- 规模：7000+ 条中文酒店评论数据
- 标注：二分类（正面/负面）人工标注
- 特点：
  - 真实用户评论，语言表达自然
  - 覆盖多种情感表达方式
  - 包含口语化表达和网络用语
  - 评论长度适中，信息量充足

## 功能特点

- 支持批量处理 CSV 格式的评论数据
- 自动处理多种文件编码（UTF-8、GBK、GB2312、GB18030）
- 生成直观的情感分布可视化图表
- 导出详细的分析结果
- 实时显示处理进度

## 环境要求

- Python 3.7+
- 百度文心大模型 API 密钥（Access Key 和 Secret Key）

## 安装步骤

1. 克隆或下载项目代码

2. 安装依赖包：
```bash
pip install -r requirements.txt
```

3. 配置 API 密钥：
   - 创建一个config.py，在 `config.py` 文件中设置您的百度文心 API 密钥以及其他相关参数：
   ```python
   # ERNIE API配置
   QIANFAN_ACCESS_KEY = "your_iak_key"
   QIANFAN_SECRET_KEY = "your_isk_key"

   # 文件路径配置
   # INPUT_CSV = './data/ChnSentiCorp_htl_all.csv'
   INPUT_CSV = './data/ChnSentiCorp_htl_short.csv'
   OUTPUT_CSV = './output/sentiment_analysis_results.csv'
   OUTPUT_PLOT = './output/sentiment_analysis_results.png'

   # 模型配置
   MODEL_NAME = "ERNIE-Speed-128K"
   ```

## 使用方法

1. 准备数据：
   - 将需要分析的评论数据保存为 CSV 文件
   - CSV 文件必须包含 `review` 列
   - 默认文件名为 `./data/ChnSentiCorp_htl_all.csv`（可在 config.py 中根据实际路径修改）

2. 运行分析：
```bash
python sentiment_analysis.py
```

3. 查看结果：
   - 情感分析结果将保存在 `./output/sentiment_analysis_results.csv`
   - 可视化图表将保存为 `./output/sentiment_analysis_results.png`
   - 控制台会实时显示处理进度和统计结果

## 文件结构

- `sentiment_analysis.py`: 主程序入口
- `sentiment_analyzer.py`: 情感分析核心类
- `config.py`: 配置文件
- `utils.py`: 工具函数
- `requirements.txt`: 依赖包列表
- `README.md`: 项目说明文档

## 输出示例

1. CSV 结果文件包含以下列：
   - review: 原始评论文本
   - sentiment: 情感分析结果（积极/消极/中立）

2. 可视化结果：
   - 柱状图显示三种情感类别的数量分布
   - 包含具体数值标签
   - 使用不同颜色区分情感类别

