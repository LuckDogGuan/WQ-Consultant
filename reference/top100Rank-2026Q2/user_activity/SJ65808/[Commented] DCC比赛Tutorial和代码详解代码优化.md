# DCC比赛Tutorial和代码详解代码优化

- **链接**: [Commented] DCC比赛Tutorial和代码详解代码优化.md
- **作者**: YZ64617
- **发布时间/热度**: 4个月前, 得票: 36

## 帖子正文

## 写在前面的废话

DCC比赛之后，官方发布了3个版本的代码。第一版是Bigdata在github上的tutorial修改而来。之后的2个版本分别增加了 **Workflow_multi_theme_sentiment** 和 **Competition_Full_Workflow_Demo** 。新增的这2个文件夹是一个相对完整的针对这次比赛的例子。

比赛代码会用到bigdata-research-tools 和bigdata-client包。bigdata有详细的文档和代码例子。

- [Bigdata官方文档](https://docs.bigdata.com/getting-started/quickstart_guide_workflows)
- [Bigdata Cookbook](https://github.com/Bigdata-com/bigdata-cookbook/blob/main/README.md) ：它们的github中，还有不少资源可以借鉴。

**个人的一些理解和可能的坑** ：

- LLM不是必须的，但我感觉使用LLM会增加数据量化的准确性
- Brain给出的2个完整的例子并没有使用LLM
- 包含LLM使用的例子在Workflow_example中，源头来自Bigdata的cookbook
- Bigdata依赖包是支持自定义openai兼容接口的模型的
- 在这里定义  *`from bigdata_research_tools.llm.base import LLMConfig* ` （可以让AI帮你写）
- LLM调用在代码中，默认10线程并行，大家注意。根据自用的模型进行设定。token消耗量，会是比较大的，且运行时间会长。
- 有可能，在notebook中运行LLM相关功能时，代码会报错。大概是涉及到异步的问题。经过CC的多次尝试，不修改依赖包 *bigdata_research_tools.llm* 下的文件似乎是无法解决的。所以，CC最后把项目文件夹内的venv内的依赖包给改了。如果大家遇到这个情况，请根据自身情况来决定。猜测，可能和notebook中运行代码有关。

下面的正文是我多次与CC对话和修改代码的过程中生成的。希望对大家有帮助。里面有一些小瑕疵。

## 目录

- 第一章：背景知识——你需要先理解这些
  - 1.1 这是什么比赛
  - 1.2 什么是量化信号
  - 1.3 NLP与新闻数据在金融中的应用
  - 1.4 关键术语表
- 第二章：环境搭建
  - 2.1 安装 Python 和 uv
  - 2.2 创建虚拟环境并安装依赖
  - 2.3 配置凭据
  - 2.4 启动 Jupyter Notebook
- 第三章：项目整体架构
  - 3.1 文件夹结构总览
  - 3.2 核心管线流程图
  - 3.3 外部依赖库说明
- 第四章：四大API详解
  - 4.1 认证机制——BrainSession
  - 4.2 Search API——语义搜索
  - 4.3 Volume API——聚合计数
  - 4.4 CoMentions API——共现发现
  - 4.5 Knowledge Graph API——知识图谱
- 第五章：Smart Batching——大规模高效搜索
  - 5.1 为什么需要批量搜索
  - 5.2 SmartBatchingPlanner 工作原理
  - 5.3 搜索执行与限速
  - 5.4 关键函数一览
- 第六章：Workflow_example——LLM辅助端到端工作流
  - 6.1 Step 1：主题思维导图生成
  - 6.2 Step 2：搜索规划与执行
  - 6.3 Step 3：实体提取与过滤
  - 6.4 Step 4：公司名称掩码
  - 6.5 Step 5：LLM标注与验证
  - 6.6 Step 6：滚动信号构建
  - 6.7 最终输出解读
- 第六点五章：Workflow_multi_theme_sentiment——多主题情感+BRAIN上传
  - 6.5.1 这个模块有什么不同？
  - 6.5.2 工作流六步走
  - 6.5.3 主题定义——正交主题设计
  - 6.5.4 实体归因机制
  - 6.5.5 复合信号构建
  - 6.5.6 数据质量验证
  - 6.5.7 上传到BRAIN
- 第六点七五章：Competition_Full_Workflow_Demo——比赛完整工作流演示
  - 6.75.1 这个模块的定位
  - 6.75.2 工作流五步走
  - 6.75.3 评分机制
  - 6.75.4 MATRIX vs VECTOR 上传
  - 6.75.5 三套工作流对比
- 第七章：经济学与金融逻辑
  - 7.1 新闻情感与股价的关系
  - 7.2 主题选择的策略思考
  - 7.3 信号质量评估
- 第八章：比赛实战指南
  - 8.1 比赛流程
  - 8.2 学习路径建议
  - 8.3 进阶优化方向
- 附录：所有函数速查表

# 第一章：背景知识——你需要先理解这些

## 1.1 这是什么比赛

**Bigdata.com & WorldQuant Data Creation Challenge 2026**  (简称 DCC2026) 是一个量化研究比赛。

**比赛要求你做的事** ：

1. 利用 Bigdata.com 提供的新闻数据API，挖掘新闻中的信息
2. 构建"量化信号"——一组数字，代表每家公司每天受某个主题影响的程度
3. 将信号上传到 WorldQuant Brain 平台，进行模拟回测（simulation）
4. 系统根据信号的预测能力给你打分

**通俗理解** ：想象你是一个基金经理的助手。每天有海量新闻，你需要从中提炼出"哪些公司因为某个主题（比如AI芯片短缺）受到了正面或负面影响"，然后把这个判断量化为一个数字信号。

## 1.2 什么是量化信号

量化信号（Quantitative Signal）是一个时间序列数据，格式如下：

公司名称
日期
信号值

Apple Inc.
2021-01-15
0.75

Apple Inc.
2021-01-16
0.62

Tesla Inc.
2021-01-15
-0.30

- **正值** ：表示该公司在这个主题下收到了正面影响（好消息多）
- **负值** ：表示负面影响（坏消息多）
- **接近零** ：表示中性或无明显影响

在本项目中，最终输出的信号是  `signal_7d` （7天滚动均值）和  `signal_30d` （30天滚动均值）。

## 1.3 NLP与新闻数据在金融中的应用

**为什么新闻数据有价值？**

传统量化投资依赖价格、成交量等数字数据。但新闻包含了市场参与者的预期、事件发展、政策变化等"软信息"。通过自然语言处理（NLP）技术，可以从海量文本中提取情感、主题、影响力等信息。

**核心思路** ：

```
新闻报道 → NLP分析 → 情感/影响判断 → 量化信号 → 交易决策

```

**例子** ：

- 新闻："芯片短缺导致汽车制造商减产" → 对汽车公司是 **负面** 消息
- 新闻："苹果公司发布创新AR眼镜，市场反响热烈" → 对Apple是 **正面** 消息

## 1.4 关键术语表

术语
英文
含义

chunk
Chunk
文档中的一个文本片段，是搜索API返回的基本单位

实体
Entity
新闻中提到的公司、人物、地点等，每个有唯一ID

实体宇宙
Entity Universe
你关注的公司集合（本项目用美国前3000家公司）

语义搜索
Semantic Search
基于含义（而非关键词匹配）的搜索

共现
Co-mention
两个实体在同一段文本中被同时提到

思维导图
MindMap
将一个大主题拆分成若干子主题的树形结构

滚动窗口
Rolling Window
用过去N天的数据计算的统计值（如7天平均值）

前瞻偏差
Look-ahead Bias
在回测中使用了未来才能知道的信息——必须避免

时间点一致
Point-in-time
只使用当时已知的信息，不偷看未来

LLM
Large Language Model
大语言模型，如GPT-4o-mini，用于理解和标注文本

basket
Basket
一组公司的集合，打包在一起发送搜索请求

# 第二章：环境搭建

## 2.1 安装 Python 和 uv

**Python** ：需要 Python 3.10 或更高版本。到  [python.org](https://www.python.org/downloads/)  下载安装。

**uv** ：一个极快的 Python 包管理器（替代 pip），安装方式：

```
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或者用 pip 安装
pip install uv

```

## 2.2 创建虚拟环境并安装依赖

```
# 进入项目根目录
cd DCC2026_v1

# 创建虚拟环境
uv venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 安装所有依赖（使用根目录下的整合版 requirements.txt）
uv pip install -r requirements.txt

```

安装完成后，你应该能看到类似 "Installed 137 packages" 的信息。

## 2.3 配置凭据

每个模块文件夹下都有一个  `.env.example`  文件。你需要：

```
# 复制模板文件
cp .env.example .env

# 编辑 .env 文件，填入你的凭据
BRAIN_EMAIL=你的注册邮箱
BRAIN_PASSWORD=你的密码

```

**如何获取凭据** ：到  [WorldQuant Brain](https://www.worldquantbrain.com/)  注册账号。比赛参与者会获得API访问权限。

**Workflow_example 额外需要** （可选）：

```
OPENAI_API_KEY=你的OpenAI密钥

```

这是用于LLM标注步骤的。如果没有，可以跳过LLM验证步骤。

> **重要** ：每个模块文件夹（Search_API、Volume_API 等）都需要各自配置  `.env` ，因为它们是独立运行的。

## 2.4 启动 Jupyter Notebook

```
# 确保虚拟环境已激活
jupyter notebook

```

浏览器会自动打开，你可以导航到任何模块文件夹打开对应的  `.ipynb`  文件。

# 第三章：项目整体架构

## 3.1 文件夹结构总览

```
DCC2026_v1/
│
├── Search_API/                   # 模块1：语义搜索教程
│   ├── Search_API_Tutorial.ipynb # Jupyter教程notebook
│   ├── session.py                # 认证会话类
│   ├── api_helpers.py            # API调用辅助函数
│   ├── print_helpers.py          # 结果打印辅助函数
│   ├── .env.example              # 环境变量模板
│   └── requirements.txt          # 本模块依赖
│
├── Volume_API/                   # 模块2：聚合计数教程
│   ├── Volume_API_Tutorial.ipynb
│   ├── session.py
│   ├── api_helpers.py
│   ├── print_helpers.py
│   └── ...
│
├── CoMentions_API/               # 模块3：共现发现教程
│   ├── CoMentions_API_Tutorial.ipynb
│   └── ...
│
├── Knowledge_Graph_API/          # 模块4：知识图谱教程
│   ├── Knowledge_Graph_API_Tutorial.ipynb
│   └── ...
│
├── Smart_Batching/               # 模块5：大规模批量搜索
│   ├── test_smart_batching.ipynb
│   ├── session.py
│   ├── src/
│   │   ├── smart_batching.py     # 分批规划器（1366行核心代码）
│   │   ├── search_function.py    # 搜索执行器（1032行核心代码）
│   │   ├── smart_batching_config.py  # 配置常量
│   │   └── output_converter.py   # 输出格式转换
│   └── id_name_mapping_us_top_3000.csv  # 实体宇宙数据
│
├── Workflow_example/             # 模块6：LLM辅助端到端工作流
│   ├── Workflow_example.ipynb    # 完整工作流教程
│   ├── session.py
│   ├── df_rolling_signal.csv     # 示例信号输出
│   ├── id_name_mapping_us_top_3000.csv
│   └── src/
│       ├── helper.py             # 通用辅助函数（实体处理、信号构建、可视化）
│       ├── search_function.py    # 搜索执行（带限速和并发控制）
│       ├── smart_batching.py     # 分批规划
│       ├── smart_batching_config.py
│       ├── output_converter.py
│       ├── processing_results.py # 搜索结果处理
│       ├── mindmap/
│       │   ├── mindmap.py        # MindMap数据结构
│       │   ├── mindmap_generator.py  # 思维导图生成器
│       │   └── mindmap_utils.py  # 提示词模板和工具
│       ├── labeler/
│       │   └── screener_labeler.py  # LLM标注器
│       └── prompts/
│           └── labeler.py        # 所有提示词模板
│
├── Workflow_multi_theme_sentiment/  # 模块7：多主题情感 + BRAIN上传
│   ├── Workflow_multi_theme_sentiment.ipynb  # 完整多主题工作流
│   ├── session.py               # 增强版认证（支持2FA）
│   ├── universe.json            # 3435个实体ID
│   └── .env.example             # 环境变量模板
│
├── Competition_Full_Workflow_Demo/  # 模块8：比赛完整工作流演示（★新增）
│   ├── DataCreationCompetition_workflow.ipynb  # 精简比赛工作流
│   ├── session.py               # 增强版认证（支持2FA）
│   ├── universe.json            # ~3000个实体ID
│   ├── requirements.txt         # 模块依赖
│   ├── .env.example             # 环境变量模板
│   └── README.md                # 模块说明
│
└── tutorial/                     # 本教程文件夹
    └── step_by_step_guide.md     # 你正在读的这个文件

```

## 3.2 核心管线流程图

整个项目要做的事情，用一张图概括：

```
┌─────────────────────────────────────────────────────────────┐
│                    第一阶段：数据获取                         │
│                                                             │
│  选择主题 ──→ 生成思维导图 ──→ 拆分为子主题                    │
│  (你的创意)   (LLM生成)        (如"AI芯片 → 供应链、研发...")  │
│                                                             │
│       ↓                                                     │
│  智能分批规划 ──→ 语义搜索执行 ──→ 获取新闻chunk               │
│  (优化API调用)   (并行+限速)      (文本片段+情感分数)          │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                    第二阶段：数据处理                         │
│                                                             │
│  实体提取 ──→ 公司过滤 ──→ 名称掩码 ──→ LLM标注              │
│  (从chunk中)  (只留宇宙内)  (防偏见)    (判断正面/负面)        │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                    第三阶段：信号构建                         │
│                                                             │
│  影响评分 ──→ 日度聚合 ──→ 滚动均值 ──→ 信号表               │
│  (+1/-1/0)   (每公司每天)  (7天/30天)    (最终输出)           │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                    第四阶段：比赛提交                         │
│                                                             │
│  路径A (Workflow_example):                                   │
│  信号表 ──→ 格式转换 ──→ 上传Brain平台 ──→ Simulation评分     │
│  (代码产出)  (你需自己写)   (平台操作)      (系统自动)         │
│                                                             │
│  路径B (Workflow_multi_theme_sentiment): ★推荐★              │
│  MATRIX数据 ──→ Parquet打包 ──→ 自动上传BRAIN ──→ Simulation │
│  (代码自动)     (代码自动)       (代码自动)        (系统自动)  │
│                                                             │
│  路径C (Competition_Full_Workflow_Demo): ★最简单★            │
│  日度抓取 ──→ 评分 ──→ MATRIX+VECTOR上传 ──→ Simulation      │
│  (代码自动)  (代码自动)  (代码自动)            (系统自动)      │
└─────────────────────────────────────────────────────────────┘

```

> **注意** ：
> - **路径A** （Workflow_example）：代码覆盖前三个阶段，第四阶段的格式转换和上传需要你自行实现。
> - **路径B** （Workflow_multi_theme_sentiment）：代码覆盖 **全部四个阶段** ，包括自动上传到BRAIN！适合想要深度定制主题和信号的参赛者。
> - **路径C** （Competition_Full_Workflow_Demo）： **最精简的端到端路径** ，不需要定义主题、不需要滚动信号，直接日度抓取评分上传。 **新手推荐先用这条路径跑通完整流程！**

## 3.3 外部依赖库说明

库名
用途
你需要了解的

 `requests` 
HTTP请求库
所有API调用的底层实现

 `pandas` 
数据处理框架
DataFrame是贯穿全项目的核心数据结构

 `numpy` 
数值计算
数组操作、数学运算

 `scipy` 
科学计算
统计分析（信号处理中可能用到）

 `plotly` 
交互式可视化
生成漂亮的图表（网络图、仪表盘等）

 `matplotlib` 
静态可视化
折线图、柱状图等

 `python-dotenv` 
环境变量管理
从  `.env`  文件读取凭据

 `bigdata-research-tools` 
BigData高层封装
LLM引擎、标注器基类、搜索函数

 `bigdata-client` 
BigData底层API
查询组件（Entity、Keyword等）

 `openai` 
OpenAI API客户端
调用GPT模型进行标注

 `graphviz` 
图形可视化
思维导图的图形渲染

 `json-repair` 
JSON修复
修复LLM返回的不规范JSON

 `pyarrow` 
Parquet格式
用于MATRIX数据打包和上传到BRAIN（Workflow_multi_theme_sentiment）

# 第四章：四大API详解

所有API都通过同一个认证机制访问。理解这四个API是使用项目的基础。

## 4.1 认证机制——BrainSession

**文件** ：每个模块的  `session.py`

**它是什么** ： `BrainSession`  是一个自定义的 HTTP 会话类，继承自 Python 的  `requests.Session` 。它帮你处理登录认证。

**工作原理** ：

```
from session import BrainSession

session = BrainSession(
    email="你的邮箱",
    password="你的密码",
    api_base_url="https://api.worldquantbrain.com"
)
# 之后所有API调用都通过 session 发送
# session 会自动处理登录token

```

**底层流程** ：

1. 发送用户名+密码到  `/authentication`  端点
2. 获取 JWT token
3. 之后每次请求自动在Header中附带token
4. Token过期会自动重新认证

> **注意** ：项目中有两种 BrainSession：
> - **标准版** （大部分模块）：简单 HTTP Basic Auth
> - **增强版** （Workflow_multi_theme_sentiment）：支持  **Persona 2FA** （生物识别认证），有token过期追踪机制

## 4.2 Search API——语义搜索

**对应文件夹** ： `Search_API/` 
 **教程Notebook** ： `Search_API_Tutorial.ipynb`

### 做什么的？

语义搜索是整个项目的 **数据来源核心** 。它不是简单的关键词匹配，而是理解你查询的 **含义** ，返回语义相关的新闻文档片段（chunk）。

### 请求结构

```
payload = {
    "query": {
        "text": "artificial intelligence chip shortage",  # 搜索语义
        "filters": {
            "timestamp": {
                "start": "2021-01-01T00:00:00Z",
                "end": "2022-12-31T23:59:59Z"
            },
            "entity": {
                "any_of": ["00067A", "003W2R"],  # 实体ID过滤
                "search_in": "BODY"
            }
        },
        "max_chunks": 100,          # 最大返回chunk数
        "reranker": True,           # 是否使用重排序器
        "relevance_threshold": 0.5, # 相关性阈值
        "freshness_boost": 0,       # 新鲜度加权（比赛要求设为0）
    }
}
response = session.post("/bigdata/v1/search", json=payload)

```

### 返回数据结构

```
{
    "results": {
        "documents": [
            {
                "id": "doc_123",
                "headline": "Intel Reports Chip Shortage...",
                "timestamp": "2021-06-15T10:30:00Z",
                "source": {"id": "src_1", "name": "Reuters", "rank": 1},
                "url": "https://...",
                "chunks": [
                    {
                        "cnum": 0,          # chunk编号
                        "text": "Intel reported severe chip shortages...",
                        "relevance": 0.85,  # 语义相关性分数（0-1）
                        "sentiment": -0.6,  # 情感分数（-1到0之间）
                        "detections": [     # 检测到的实体
                            {"id": "001A3F", "type": "entity", "start": 0, "end": 5}
                        ]
                    }
                ]
            }
        ]
    }
}

```

### 关键参数说明

参数
说明
建议值

 `max_chunks` 
单次请求返回的最大chunk数
100-1000

 `reranker` 
二次排序，提高相关性但增加延迟
True（质量优先）或 False（速度优先）

 `relevance_threshold` 
过滤掉低于此阈值的结果
0.3-0.7

 `freshness_boost` 
偏向新文档的程度
 **比赛要求设为 0** 

 `source_boost` 
偏向高排名来源
根据需要调整

### 关键辅助函数

**文件** ： `Search_API/api_helpers.py`

函数
用途

 `semantic_search(session, query, filters, ...)` 
执行单次语义搜索

 `search_with_reranker(session, query, ...)` 
带重排序器的搜索

 `plot_relevance_distribution(results)` 
绘制相关性分布图

 `compare_with_without_reranker(...)` 
对比开关reranker的效果

## 4.3 Volume API——聚合计数

**对应文件夹** ： `Volume_API/` 
 **教程Notebook** ： `Volume_API_Tutorial.ipynb`

### 做什么的？

Volume API 返回的是 **计数** 而不是实际文档。它告诉你"对于这个查询，每天有多少条相关新闻"。

### 为什么有用？

- **评估覆盖范围** ：在做正式搜索前，先看看某个主题有多少数据
- **情感趋势** ：按天统计正面/负面新闻数量
- **决策依据** ：数据太少的主题或时间段，信号不可靠

### 请求示例

```
payload = {
    "query": {
        "text": "AI chip shortage",
        "filters": {
            "timestamp": {"start": "2021-01-01T00:00:00Z", "end": "2022-12-31T23:59:59Z"}
        },
        "granularity": "day"  # 按天统计
    }
}
response = session.post("/bigdata/v1/search/volume", json=payload)

```

### 返回数据

```
{
    "results": [
        {"date": "2021-01-15", "document_count": 42, "chunk_count": 156},
        {"date": "2021-01-16", "document_count": 38, "chunk_count": 132},
        ...
    ]
}

```

## 4.4 CoMentions API——共现发现

**对应文件夹** ： `CoMentions_API/` 
 **教程Notebook** ： `CoMentions_API_Tutorial.ipynb`

### 做什么的？

发现哪些实体（公司、人物、地点等）经常和你的搜索主题 **一起被提到** 。

### 为什么有用？

- **发现相关公司** ：搜"芯片短缺"，发现 Intel、TSMC、NVIDIA 被频繁提及
- **构建主题篮子** ：找出一组受同一主题影响的公司
- **网络分析** ：理解实体之间的关联关系

### 请求示例

```
payload = {
    "query": {
        "text": "semiconductor shortage",
        "filters": {
            "timestamp": {"start": "...", "end": "..."},
            "entity": {
                "any_of": ["公司ID列表"],  # 在这些公司中查找
                "search_in": "BODY"
            }
        },
        "limit": 1000
    }
}
response = session.post("/bigdata/v1/search/co-mentions/entities", json=payload)

```

### 在项目中的实际用途

Smart Batching 系统用 CoMentions API 来 **预估每个公司的新闻量** （chunk数），从而优化搜索策略。这是整个分批系统的第一步。

## 4.5 Knowledge Graph API——知识图谱

**对应文件夹** ： `Knowledge_Graph_API/` 
 **教程Notebook** ： `Knowledge_Graph_API_Tutorial.ipynb`

### 做什么的？

实体名称和ID之间的 **双向解析** 。

### 核心操作

操作
说明
例子

名称 → ID
根据公司名找到唯一ID
"Apple" → "00F26A"

ID → 名称
根据ID查公司名和元数据
"00F26A" → "Apple Inc."

来源查询
查找新闻来源信息
查看某来源的排名和类别

### 为什么重要？

所有API的实体过滤都用 **ID** 而非名称。你必须先通过知识图谱把公司名转成ID，才能精确搜索。

```
# 查找Apple公司的ID
response = session.get("/bigdata/v1/knowledge-graph/entities", params={"name": "Apple"})
# 返回: [{"id": "00F26A", "name": "Apple Inc.", "type": "company", ...}]

```

# 第五章：Smart Batching——大规模高效搜索

## 5.1 为什么需要批量搜索

**问题** ：你要搜索的实体宇宙有3000+家公司，如果逐一搜索：

- 3000家 × 每家1次请求 = 3000次API调用
- API限速100次/分钟 → 需要30分钟
- 如果时间跨度大，每家公司需要多次请求 → 更久

**Smart Batching 的解决方案** ：

- 把公司按新闻量分组，打包成"basket"
- 每个basket一次请求搜索多家公司
- 自动切分时间窗口，确保每次请求不超过1000 chunks
- 结果： **减少 67-99% 的API调用**

## 5.2 SmartBatchingPlanner 工作原理

**文件** ： `Workflow_example/src/smart_batching.py`  中的  `SmartBatchingPlanner`  类

### 两阶段流程

**阶段1：量发现** （Phase 1）

```
输入：公司列表 + 搜索主题 + 时间范围
   ↓
调用 CoMentions API 获取每家公司的chunk数量
   ↓
输出：{公司ID: chunk数量} 的字典

```

**阶段2：分批规划** （Phase 2）

```
输入：每家公司的chunk数量
   ↓
按量分桶：high(500+), medium(100-500), low(1-100), very_low(0)
   ↓
创建basket：确保每个basket总chunk ≤ 1000，实体数 ≤ 500
   ↓
自适应时间切分：高量公司用更细粒度（月/周）
   ↓
输出：搜索计划（哪些公司在什么时间段搜索）

```

### 关键配置（smart_batching_config.py）

```
MAX_ENTITIES_IN_ANY_OF = 500   # 每次请求最多500个实体
MAX_CHUNKS_PER_BASKET = 1000   # 每个basket最多1000个chunk
START_DATE = "2021-01-01"       # 默认起始日期
END_DATE = "2022-12-31"         # 默认结束日期

```

## 5.3 搜索执行与限速

**文件** ： `Workflow_example/src/search_function.py`

### SlidingWindowRateLimiter

搜索执行器内置了一个滑动窗口限速器，确保不超过API速率限制：

```
限速规则：
- 每分钟最多 100 个请求
- 连续请求间至少间隔 5 秒（防突发）
- 线程安全（支持并行搜索）

```

### 两种搜索模式

模式
函数
说明

Smart搜索
 `execute_search(plan, chunk_percentage)` 
按计划执行，按比例采样chunk

全网格搜索
 `execute_full_grid_search(...)` 
简单遍历所有basket，不做比例采样

**chunk_percentage**  参数：控制每个basket实际请求的chunk比例。设为0.5表示只取50%的chunk（加快速度，牺牲覆盖度）。

## 5.4 关键函数一览

函数
文件
用途

 `SmartBatchingPlanner.plan_all_periods()` 
smart_batching.py
生成完整搜索计划

 `SmartBatchingPlanner.load_universe()` 
smart_batching.py
从CSV加载实体列表

 `SmartBatchingPlanner.get_comention_volumes()` 
smart_batching.py
三遍模式查询公司chunk量

 `SmartBatchingPlanner.get_comention_volumes_iterative()` 
smart_batching.py
迭代模式查询（更高效）

 `SmartBatchingPlanner.create_baskets()` 
smart_batching.py
创建公司分组basket

 `SmartBatchingPlanner.export_to_csvs()` 
smart_batching.py
导出计划到CSV

 `execute_search()` 
search_function.py
执行Smart搜索

 `execute_full_grid_search()` 
search_function.py
执行全网格搜索

 `deduplicate_documents()` 
search_function.py
合并重复文档

 `convert_to_dataframe()` 
output_converter.py
原始结果转DataFrame

# 第六章：Workflow_example——LLM辅助端到端工作流

这是LLM辅助的端到端工作流模块，展示了从主题到信号的完整流程。对应  `Workflow_example/Workflow_example.ipynb` 。

## 6.1 Step 1：主题思维导图生成

**文件** ： `src/mindmap/mindmap.py` ,  `src/mindmap/mindmap_generator.py`

### 做什么？

把一个大主题（如"AI芯片短缺"）用LLM自动拆分成若干子主题，形成树形结构。

### 为什么要拆分？

一个大主题直接搜索，可能覆盖不全。拆成子主题后，可以：

- 提高搜索的 **召回率** （recall）：每个子主题捕获不同角度的新闻
- 更精确的 **标注** ：子主题更具体，LLM判断更准确

### 示例

```
AI芯片短缺                          ← 根节点（主题）
├── 供应链中断风险                    ← 子主题
│   ├── 晶圆制造瓶颈                 ← 叶子节点（最终搜索目标）
│   ├── 物流运输延迟
│   └── 原材料供应紧张
├── 企业成本风险
│   ├── 芯片采购成本上升
│   ├── 产品延迟发布
│   └── 研发替代方案投入
└── 市场竞争风险
    ├── 客户转向竞争对手
    └── 市场份额变化

```

### 核心代码

```
from src.mindmap.mindmap import generate_theme_tree

# 一次性生成
tree = generate_theme_tree(
    main_theme="AI chip shortage",
    focus="impact on semiconductor companies",
    llm_model_config="openai::gpt-4o-mini"
)

# 查看结果
tree.print()  # 打印树形结构
tree.get_terminal_labels()  # 获取所有叶子节点标签
tree.get_terminal_label_summaries()  # 获取叶子节点的标签+摘要
tree.save_json("my_mindmap.json")  # 保存为JSON

```

### MindMap 类核心方法

方法
用途

 `MindMap.from_dict(dict)` 
从字典创建MindMap

 `.print()` 
打印树形结构

 `.visualize(engine="graphviz")` 
生成可视化图（支持graphviz/plotly/matplotlib）

 `.get_terminal_labels()` 
获取所有叶子节点的标签列表

 `.get_terminal_label_summaries()` 
获取叶子节点{标签: 摘要}字典

 `.get_label_to_parent_mapping()` 
获取叶子→父节点的映射

 `.to_dataframe()` 
转为DataFrame

 `.to_json()` 
转为JSON字符串

 `.save_json(filepath)` 
保存为JSON文件

### MindMapGenerator 高级模式

`MindMapGenerator`  类提供了三种生成模式：

模式
方法
说明

一次性
 `generate_oneshot()` 
LLM直接生成，最快

精炼
 `generate_refined()` 
LLM生成 → 搜索验证 → 调整优化，质量更高

动态
 `generate_dynamic()` 
按月/季度分段生成，适应随时间变化的主题

## 6.2 Step 2：搜索规划与执行

### 规划

```
from src.smart_batching import SmartBatchingPlanner

planner = SmartBatchingPlanner(session=session)

# 生成搜索计划
plan = planner.plan_all_periods(
    topic="AI chip shortage",
    start_date="2021-01-01",
    end_date="2022-12-31",
    volume_query_mode="iterative",  # 推荐迭代模式
)

# 查看计划报告
print(planner.generate_report(plan))

```

### 执行

```
from src.search_function import execute_search

# 执行搜索（chunk_percentage控制采样比例）
results = execute_search(
    session=session,
    plan=plan,
    topic="AI chip shortage",
    chunk_percentage=1.0,  # 1.0 = 100%完整搜索
)

```

### 结果转DataFrame

```
from src.output_converter import convert_to_dataframe

df_chunks = convert_to_dataframe(results)
# 每行是一个chunk，包含：
# date, doc_id, headline, chunk_text, chunk_relevance,
# chunk_sentiment, entity_ids, detections, ...

```

## 6.3 Step 3：实体提取与过滤

**文件** ： `src/helper.py`

### 为什么要过滤？

搜索返回的chunk中可能包含各种实体（公司、人物、地点等）。我们只关心"实体宇宙"中的公司。

### 流程

```
from src.helper import load_universe_entities, explode_to_dataframe

# 加载实体宇宙
entity_ids, id_to_name = load_universe_entities("id_name_mapping_us_top_3000.csv")
# entity_ids: {"00067A", "003W2R", ...}（4732个ID的集合）
# id_to_name: {"00067A": "Humana Inc.", ...}

# 按实体展开（一个chunk可能包含多个公司 → 拆成多行）
df_exploded = explode_to_dataframe(
    df_chunks,
    universe_csv="id_name_mapping_us_top_3000.csv"
)
# 现在每行是一个 (chunk, 实体) 组合
# 新增列：entity_id, entity_name

```

### 关键概念：展开（Explode）

一条新闻中可能提到3家公司。展开操作会把这条新闻变成3行，每行对应一家公司：

```
原始chunk：
  "Apple and Microsoft are competing for AI chip supply from NVIDIA"
  detections: [Apple, Microsoft, NVIDIA]

展开后：
  行1: entity=Apple,     chunk_text="Apple and Microsoft..."
  行2: entity=Microsoft, chunk_text="Apple and Microsoft..."
  行3: entity=NVIDIA,    chunk_text="Apple and Microsoft..."

```

## 6.4 Step 4：公司名称掩码

**文件** ： `src/helper.py`  中的  `mask_companies_in_df()`

### 为什么要掩码？

发送文本给LLM标注时，如果文本中出现"Apple"，LLM可能因为自己对Apple的"印象"而产生偏见。掩码就是把公司名替换成中性占位符：

```
原文：
  "Apple reported strong earnings while Microsoft faced regulatory challenges"

掩码后（假设目标公司是Apple）：
  "Target_Company reported strong earnings while Other_Company_1 faced regulatory challenges"

```

### 代码

```
from src.helper import mask_companies_in_df

df_masked = mask_companies_in_df(
    df_exploded,
    text_column="chunk_text",
    detection_column="companies_detection",
    target_entity_id_column="entity_id"
)
# 新增列：masked_text, other_entities_map

```

## 6.5 Step 5：LLM标注与验证

**文件** ： `src/labeler/screener_labeler.py`

### 做什么？

用LLM（如GPT-4o-mini）阅读每段掩码后的文本，判断：

1. **是否与主题相关** （is_theme_related: True/False）
2. **影响方向** （impact: Positive/Negative/Neutral/Unclear）

### 两种标注模式

模式
方法
说明

基础标注
 `get_labels()` 
一步判断影响方向

验证标注
 `get_validation_labels()` 
两步：先判相关性，再判影响

### 代码示例

```
from src.labeler.screener_labeler import ScreenerLabeler

labeler = ScreenerLabeler(
    llm_config="openai::gpt-4o-mini",
    theme="AI chip shortage",
    sub_themes=tree.get_terminal_label_summaries()
)

# 两步验证标注
df_labeled = labeler.get_validation_labels(df_masked)
# 新增列：is_theme_related, impact, motivation

```

### ThemeValidationResult 模型

```
class ThemeValidationResult(BaseModel):
    is_theme_related: bool    # 是否与主题相关
    impact: ImpactType        # "Positive" | "Negative" | "Neutral" | "Unclear"
    motivation: str           # LLM的判断理由

```

### 提示词模板

所有发送给LLM的提示词模板在  `src/prompts/labeler.py`  中定义。主要模板：

模板
用途

 `screener_system_prompt_template` 
基础主题标注

 `theme_validation_prompt_template` 
两步验证：相关性+影响

 `risk_system_prompt_template` 
风险场景评估

## 6.6 Step 6：滚动信号构建

**文件** ： `src/helper.py`  中的  `build_rolling_impact_signal()`

### 核心逻辑

```
影响评分映射：
  Positive  → +1
  Negative  → -1
  Neutral   → 0
  Unclear   → 0

日度聚合：
  每家公司每天的 daily_score = 当天所有chunk评分的平均值

滚动均值：
  signal_7d  = daily_score 的过去7天滚动平均
  signal_30d = daily_score 的过去30天滚动平均

```

### 代码

```
from src.helper import build_rolling_impact_signal

df_signal = build_rolling_impact_signal(
    df_labeled,
    entity_col="entity_name",
    date_col="date",
    impact_col="impact",
    is_theme_related_col="is_theme_related",
    window_7d=7,
    window_30d=30,
    rolling_agg="mean"  # 使用均值（还可以用 "sum"）
)

```

### 可视化

```
from src.helper import plot_top_entities_rolling_signal

# 画出新闻量最多的5家公司的信号趋势
plot_top_entities_rolling_signal(
    df_signal,
    signal_col="signal_30d",  # 或 "signal_7d"
    top_n=5
)

```

## 6.7 最终输出解读

`df_rolling_signal.csv`  的每一行代表 **一家公司在一天的信号** ：

列名
含义
取值范围

 `entity_name` 
公司名称
如 "Apple Inc."

 `date` 
日期
2021-01-01 ~ 2022-12-31

 `daily_score` 
当天影响均值
-1 到 +1

 `n_positive` 
当天正面新闻数
0, 1, 2, ...

 `n_negative` 
当天负面新闻数
0, 1, 2, ...

 `n_neutral` 
当天中性新闻数
0, 1, 2, ...

 `n_unclear` 
当天不明确新闻数
0, 1, 2, ...

 `volume` 
当天总新闻数
0, 1, 2, ...

 `signal_7d` 
7天滚动信号
-1 到 +1

 `signal_30d` 
30天滚动信号
-1 到 +1

 `volume_7d` 
7天滚动新闻量
0, 1, 2, ...

 `volume_30d` 
30天滚动新闻量
0, 1, 2, ...

**如何解读** ：

- `signal_30d = 0.8` ：过去30天该公司在此主题下以正面新闻为主（做多信号）
- `signal_30d = -0.6` ：过去30天以负面新闻为主（做空信号或风险预警）
- `signal_30d ≈ 0` ：中性或数据不足

# 第六点五章：Workflow_multi_theme_sentiment——多主题情感+BRAIN上传

这是项目新增的 **最完整模块** ，展示了从主题定义到BRAIN平台上传的全流程。对应  `Workflow_multi_theme_sentiment/Workflow_multi_theme_sentiment.ipynb` 。

> **★ 新手推荐先看这个模块！**  因为它不需要LLM（省掉OpenAI费用），而且包含了完整的BRAIN上传代码。

## 6.5.1 这个模块有什么不同？

特性
Workflow_example
Workflow_multi_theme_sentiment

需要LLM？
是（OpenAI）
 **否** 

如何判断情感？
LLM标注
 **API内置sentiment过滤器** 

主题数量
单一主题拆分
 **多个正交主题** 

是否上传BRAIN？
❌ 需自行实现
 **✅ 代码自动完成** 

信号格式
CSV（长格式）
 **MATRIX Parquet（宽格式）** 

实体列表
CSV（含名称）
JSON（纯ID）

核心优势
LLM精度高
无需LLM、完整提交流程

**核心思路** ：用多个 **正交主题** （互相独立的角度），每个主题有明确的 **正/负方向** ，利用API的sentiment过滤器直接获取正面或负面新闻，然后加权合成复合信号。

## 6.5.2 工作流六步走

```
步骤1: 实体宇宙 + 主题定义
  ↓ 加载3435个实体ID，定义正面/负面主题
步骤2: 批量搜索执行
  ↓ 500实体/批 × 月份 × 主题，带API层面sentiment过滤
步骤3: 实体归因 + 情感评分
  ↓ 把搜索结果归因到具体公司，计算加权情感分
步骤4: 滚动信号构建
  ↓ 7天/30天滚动均值 → 方向加权合成 → 截面去均值
步骤5: 数据质量QA验证
  ↓ 6项自动检查确保数据没问题
步骤6: 上传到BRAIN
  ↓ 打包成Parquet格式，自动上传MATRIX数据字段

```

## 6.5.3 主题定义——正交主题设计

**什么是正交主题？**  就是从不同的、互相独立的角度来捕捉新闻情感。比如：

- "财报正面新闻"（方向：+1）——捕捉盈利增长
- "供应链负面新闻"（方向：-1）——捕捉供应链风险

```
THEMES = {
    "earnings_positive": {
        "text": "the company reports strong earnings growth revenue beat expectations",
        "description": "Clearly positive earnings news only",
        "sentiment_filter": {"min": 0.3, "max": 1.0},  # 只要正面情感的新闻
        "direction": 1.0,  # 正面方向
    },
    "supply_chain_negative": {
        "text": "supply chain disruption shortage delays logistics bottleneck",
        "description": "Clearly negative supply chain news only",
        "sentiment_filter": {"min": -1.0, "max": -0.3},  # 只要负面情感的新闻
        "direction": -1.0,  # 负面方向
    },
}

```

**关键参数** ：

- `text` : 搜索查询文本（语义搜索用）
- `sentiment_filter` : API层面的情感过滤（ `min` / `max`  范围是 -1 到 1）
- `direction` : 合成复合信号时的方向权重

> **进阶提示** ：示例展示了5个金融主题。你可以进一步扩展到8-10个正交维度，覆盖更多角度（如"并购活动"、"产品创新"等）。主题越多、越正交，复合信号越稳健。

## 6.5.4 实体归因机制

搜索返回的新闻中可能提到多家公司。系统用以下逻辑将新闻归因到具体实体：

归因类型
条件
权重

 **直接归因** 
实体在chunk中被检测到  **且**  在查询的batch中
100%

 **共提及归因** 
实体在chunk中被检测到，在实体宇宙中，但 **不在** 查询batch中
50%

 **丢弃** 
chunk中没有检测到任何实体宇宙中的实体
0%

**评分公式** ：

```
文档加权情感 = Σ(相关性 × 情感) / Σ(相关性)
平均相关性 = mean(各chunk相关性)

```

## 6.5.5 复合信号构建

### 步骤1：每主题滚动均值

把每个主题的日度评分做 7天 和 30天 的 **回溯滚动均值** （只看过去，不看未来，确保时间点一致）。

### 步骤2：方向加权合成

```
composite = Σ(主题矩阵 × 方向权重 × 0.5)

```

比如：earnings_positive 的矩阵 × (+1) × 0.5 + supply_chain_negative 的矩阵 × (-1) × 0.5

### 步骤3：截面去均值

每天对所有有信号的公司做 **去均值** 处理（减去当日均值）。这确保信号是 **相对的** ——相对于同日其他公司的表现。

```
# 每天的截面去均值
for date in all_dates:
    nonzero = composite.loc[date] != 0
    if nonzero.sum() > 1:
        composite.loc[date, nonzero] -= composite.loc[date, nonzero].mean()

```

## 6.5.6 数据质量验证

Notebook内置了6项自动QA检查：

检查项
内容
通过条件

QA-1 日期范围
矩阵覆盖完整日期
起止日期正确

QA-2 实体覆盖
有信号的实体占比
>5% 通过, >1% 警告

QA-3 NaN/Inf
数据中无异常值
无NaN且无Inf

QA-4 值域范围
信号值合理
[-1.5, +1.5] 范围内

QA-5 复合平衡
正负信号比例
20%-80% 且均值接近0

QA-6 平滑度
30天滚动比原始更平滑
30d标准差 ≤ raw标准差

## 6.5.7 上传到BRAIN

这是整个比赛最关键的一步——将信号上传到WorldQuant BRAIN进行alpha模拟！

### 上传数据格式

属性
值

类型
 `MATRIX` 

格式
Parquet + GZIP 压缩

矩阵形状
日期行 × 实体ID列

值
信号值 × 100（放大100倍）

字段ID
 `{USER_ID}_{主题缩写}_{窗口}`

### 上传代码核心

```
# 准备上传
field_meta = json.dumps({
    'id': field_id,          # 如 "12345_earnings_pos_7d"
    'type': 'MATRIX',
    'source': 'BigData',
    'data': [{'region': 'USA', 'delay': 1}]
})

# 发送到BRAIN
response = session.post(
    "/users/self/data-fields",      # 上传端点
    data={'field': field_meta},     # 元数据
    files={'data': parquet_buffer}, # Parquet文件
    timeout=120
)

```

### 上传字段示例

字段ID
说明

 `{USER_ID}_earnings_pos_7d` 
7天滚动正面财报情感

 `{USER_ID}_earnings_pos_30d` 
30天滚动正面财报情感

 `{USER_ID}_supply_neg_7d` 
7天滚动负面供应链情感

 `{USER_ID}_supply_neg_30d` 
30天滚动负面供应链情感

> **成功上传后** ，你就可以在BRAIN平台上使用这些数据字段来构建alpha表达式并运行Simulation了！

# 第六点七五章：Competition_Full_Workflow_Demo——比赛完整工作流演示

这是项目新增的 **最精简模块** ，展示了从实体ID到BRAIN平台上传的最短路径。对应  `Competition_Full_Workflow_Demo/DataCreationCompetition_workflow.ipynb` 。

> **★ 绝对新手推荐先看这个模块！**  不需要LLM，不需要BRT库，不需要定义主题，代码最少，流程最直接。

## 6.75.1 这个模块的定位

特性
Workflow_example
Workflow_multi_theme_sentiment
Competition_Full_Workflow_Demo

需要LLM？
是
否
 **否** 

需要BRT库？
是
否
 **否** 

需要定义主题？
是
是
 **否** 

上传类型
需自行实现
MATRIX
 **MATRIX + VECTOR** 

代码复杂度
高
中
 **低（最简单）** 

API端点
生产环境
生产环境
 **开发环境** 

核心优势
LLM精度
多主题复合信号
 **最短路径跑通全流程**

**核心思路** ：每天批量获取新闻文档 → 用每个chunk的  `相关性 × 情感`  计算评分 → 汇总为每个实体每天的分数 → 同时上传MATRIX（均值）和VECTOR（列表）到BRAIN。

## 6.75.2 工作流五步走

```
步骤1: 实体宇宙加载
  ↓ 从 universe.json 加载 ~3000 个实体ID
步骤2: 日度文档获取
  ↓ 每天 → 分批500个ID → 调Search API → 带指数退避重试
步骤3: 情感评分计算
  ↓ 每篇文章: avg(相关性 × 情感) × 100 → 归因到文章中提到的实体
步骤4: DataFrame构建
  ↓ 行=日期, 列=实体ID, 值=评分列表 → 保存Parquet
步骤5: 上传到BRAIN
  ↓ MATRIX（均值float）+ VECTOR（评分列表）同时上传

```

### 关键代码结构

```
# 主执行函数
all_entity_data = run_workflow(
    start_date_input="2021-01-01",
    end_date_input="2021-01-07",
    universe_ids=top3000      # ~3000个实体ID
)
# 返回: {entity_id: {date_str: [scores]}}

# 构建DataFrame
df = create_dataframe(all_entity_data, "2021-01-01", "2021-01-07", top3000)
# shape: (7天, ~3000列)

# 上传MATRIX（每个单元格一个float）
df_matrix = df.applymap(lambda x: mean(x) if x else 0.0)
create_data_field(f"{USER_ID}_sentiment_matrix", df_matrix, 'USA', 1, 'MATRIX', 'BigData')

# 上传VECTOR（每个单元格一个float列表）
df_vector = df.applymap(lambda x: list(x) if x else [])
create_data_field(f"{USER_ID}_sentiment_vector", df_vector, 'USA', 1, 'VECTOR', 'BigData')

```

## 6.75.3 评分机制

这个模块的评分逻辑非常直接：

### 文档级评分

```
对每篇文章：
  1. 遍历所有chunk
  2. chunk_score = relevance × sentiment
     - relevance: 语义相关性 (0~1)
     - sentiment: 情感分数 (-1~+1)
  3. article_score = mean(所有chunk_score) × 100

最终：
  - 正分 = 相关且正面的文章（如：高相关性的利好新闻）
  - 负分 = 相关且负面的文章
  - 接近零 = 不太相关或情感中性

```

### 实体归因

每篇文章的分数会被分配给文章中提到的 **所有在实体宇宙中的实体** ：

```
for chunk in article['chunks']:
    for detection in chunk['detections']:
        if detection['type'] == 'entity' and detection['id'] in universe_set:
            # 这个实体获得这篇文章的分数
            entity_scores[detection['id']].append(article_score)

```

> **注意** ：与 Workflow_multi_theme_sentiment 的区别——这里没有"直接归因 vs 共提及归因"的区分，所有在文章中检测到的实体都获得相同权重的分数。

## 6.75.4 MATRIX vs VECTOR 上传

这个模块同时演示了两种BRAIN数据字段类型：

类型
每个单元格的值
用途

 **MATRIX** 
单个float（多篇文章取均值）
简单的日度情感均值

 **VECTOR** 
float列表（保留所有文章分数）
保留完整信息，可在BRAIN端做更复杂处理

```
# MATRIX示例（某实体某天）：
# 3篇文章评分: [25.5, -10.2, 8.0]
# MATRIX值 = mean([25.5, -10.2, 8.0]) = 7.77

# VECTOR示例（同样的实体同天）：
# VECTOR值 = [25.5, -10.2, 8.0]  ← 保留原始列表

```

### 上传格式

属性
MATRIX
VECTOR

类型名
 `MATRIX` 
 `VECTOR` 

格式
Parquet + GZIP
Parquet + GZIP

矩阵形状
日期行 × 实体ID列
日期行 × 实体ID列

单元格值
float
list[float]

字段ID
 `{USER_ID}_sentiment_scores_matrix` 
 `{USER_ID}_sentiment_scores_vector`

## 6.75.5 三套工作流对比

维度
Workflow_example
Workflow_multi_theme_sentiment
Competition_Full_Workflow_Demo

 **复杂度** 
★★★★★
★★★☆☆
★☆☆☆☆

 **信号质量** 
最高（LLM精度）
高（多主题正交）
基础（原始评分）

 **成本** 
需要LLM API费用
免费
免费

 **完整度** 
缺BRAIN上传
完整
完整

 **适用场景** 
深度研究
正式比赛
快速入门/原型验证

> **建议路径** ：先用 Competition_Full_Workflow_Demo 跑通全流程 → 再用 Workflow_multi_theme_sentiment 提升信号质量 → 最后用 Workflow_example 追求极致精度。

# 第七章：经济学与金融逻辑

## 7.1 新闻情感与股价的关系

**学术基础** ：行为金融学研究表明，新闻情感可以预测短期股价走势。原因包括：

1. **信息传播延迟** ：并非所有投资者同时看到并消化新闻
2. **注意力有限** ：投资者不可能关注所有公司的所有新闻
3. **情感反应** ：负面新闻往往引发过度反应，正面新闻可能反应不足

**本项目的逻辑链** ：

```
新闻发布 → NLP提取情感 → 构建信号 → 假设信号能预测未来价格变动

```

**注意** ：这只是一个假设。信号好不好用，要靠 **回测验证** 。

## 7.2 主题选择的策略思考

主题选择是整个管线中 **最重要的创意环节** 。好的主题应该：

特征
好的主题
差的主题

影响范围
影响多家公司，但不是所有公司
要么只影响1-2家，要么影响所有公司

可量化
有明确的正面/负面影响
模糊不清，难以判断正负

时效性
在目标时间段有持续新闻
只是一两天的新闻

差异化
不同公司受影响程度不同
所有公司影响一样（无alpha）

独特性
别人不太可能想到
太通用（如"经济衰退"）

**主题示例** ：

- ✅ "芯片短缺对汽车行业的影响"——具体、可量化、差异化
- ✅ "新冠疫苗研发进展对医药公司的影响"——时效性强
- ❌ "全球经济增长"——太宽泛
- ❌ "某CEO言论"——太窄、一次性

## 7.3 信号质量评估

在把信号提交到Brain平台之前，你可以自己初步评估：

### 覆盖度

```
有信号的公司数 / 实体宇宙总数

```

太低说明主题覆盖不够，太高说明可能不够精确。

### 信号分布

好的信号应该有合理的正负分布，不应该全是正面或全是负面。

### 时间稳定性

`signal_30d`  不应该剧烈跳动（除非有重大事件）。如果信号噪声太大，考虑加大滚动窗口或增加过滤条件。

### 新闻量支撑

`volume_30d`  很低的公司信号不可靠。可以设阈值过滤掉低量公司。

# 第八章：比赛实战指南

## 8.1 比赛流程

### 路径A：Workflow_example（LLM辅助，需自行上传）

```
1. 注册 WorldQuant Brain 账号
2. 获取 API 凭据（BRAIN_EMAIL, BRAIN_PASSWORD）+ OpenAI API Key
3. 选择研究主题
4. 运行 Workflow_example 管线生成信号CSV
5. 将信号CSV转换为 Brain 平台的 MATRIX 格式（需自行实现）
6. 上传到 Brain 平台
7. 运行 Simulation
8. 查看评分和排名

```

### 路径B：Workflow_multi_theme_sentiment（完整流程，多主题复合信号）

```
1. 注册 WorldQuant Brain 账号
2. 获取 API 凭据（BRAIN_EMAIL, BRAIN_PASSWORD）
3. 定义多个正交金融主题
4. 运行 Workflow_multi_theme_sentiment notebook
5. 代码自动搜索、评分、构建MATRIX、上传到BRAIN ← 全自动！
6. 在BRAIN平台构建alpha表达式
7. 运行 Simulation
8. 查看评分和排名

```

### 路径C：Competition_Full_Workflow_Demo（★新手首选，最简单★）

```
1. 注册 WorldQuant Brain 账号
2. 获取 API 凭据（BRAIN_EMAIL, BRAIN_PASSWORD）
3. 运行 DataCreationCompetition_workflow.ipynb
4. 代码自动日度抓取、评分、上传MATRIX+VECTOR到BRAIN ← 全自动！
5. 在BRAIN平台构建alpha表达式
6. 运行 Simulation
7. 查看评分和排名

```

> **绝对新手推荐路径C** ：最少的代码、最少的配置、最短的路径跑通全流程。跑通之后再切换到路径B提升信号质量。

## 8.2 学习路径建议

### 第1周：基础

1. 配好环境，跑通所有  `.env`  配置
2. 按顺序运行4个API Tutorial Notebook：
   - `Search_API_Tutorial.ipynb` （最重要，理解chunk概念）
   - `Volume_API_Tutorial.ipynb`
   - `Knowledge_Graph_API_Tutorial.ipynb`
   - `CoMentions_API_Tutorial.ipynb`
3. 每个Notebook的每个cell都运行一遍，理解输入输出

### 第2周：进阶

1. **★ 运行  `Competition_Full_Workflow_Demo/DataCreationCompetition_workflow.ipynb`**
2. 理解最简单的"抓取→评分→上传"全流程（新手必须先跑通这个！）
3. 运行  `Smart_Batching/test_smart_batching.ipynb`
4. 理解分批原理，尝试修改参数
5. 运行  `Workflow_multi_theme_sentiment/Workflow_multi_theme_sentiment.ipynb`
6. 理解多主题 + BRAIN上传的完整流程
7. 运行  `Workflow_example/Workflow_example.ipynb` （需要OpenAI API Key）
8. 对比三种工作流的不同

### 第3周：实战

1. 设计自己的正交主题组合（参考 THEMES 字典格式）
2. 修改 Workflow_multi_theme_sentiment 的主题、时间范围、批次大小
3. 运行完整管线并上传到BRAIN
4. 在BRAIN平台构建alpha表达式，运行Simulation
5. 分析QA检查结果和Simulation评分

### 第4周：迭代优化

1. 增加更多正交主题（扩展到5-10个）
2. 调整sentiment_filter的阈值范围
3. 尝试 Workflow_example 的LLM标注方案，对比效果
4. 优化滚动窗口参数、归因权重
5. 提交最佳信号，冲刺排名

## 8.3 进阶优化方向

当你跑通基础流程后，以下方向可以帮你在比赛中脱颖而出：

### 信号构建优化

方向
说明

衰减加权
越近的新闻权重越高（指数衰减）

z-score标准化
跨公司横截面标准化，消除量级差异

行业中性化
减去行业平均信号，提取公司特有信号

多主题合成
综合多个主题的信号（等权或优化权重）— Workflow_multi_theme_sentiment 已实现基础版

异常量检测
新闻量突增时加大信号权重（事件驱动）

归因权重优化
调整共提及归因的0.5×折扣系数，可按距离或频率动态调整

截面去均值改进
可尝试按行业分组去均值，而非全市场去均值

### 搜索质量优化

方向
说明

调整 relevance_threshold
提高阈值减少噪声，降低阈值增加覆盖

reranker开关
开=质量高但慢，关=速度快但噪声多

来源过滤
只用高排名来源（source_rank）减少噪声

精炼MindMap
用refined模式生成更好的子主题

### LLM标注优化

方向
说明

改进prompt
让LLM判断更准确（最具性价比的优化）

换模型
试试更强大的模型（如 gpt-4o）

验证模式
使用两步验证（先判相关性再判影响）

置信度过滤
只保留LLM高置信度的判断

# 附录：所有函数速查表

## 认证（session.py）

函数/类
说明

 `BrainSession(email, password, api_base_url)` 
创建标准认证会话（大部分模块）

 `BrainSession(base_url, email, password, refresh_margin)` 
创建增强版认证会话（Workflow_multi_theme_sentiment，支持2FA）

## 思维导图（mindmap/mindmap.py）

函数/方法
说明

 `generate_theme_tree(main_theme, focus, llm_model_config)` 
生成主题思维导图

 `generate_risk_tree(main_theme, focus, llm_model_config)` 
生成风险思维导图

 `MindMap.from_dict(dict)` 
从字典创建

 `MindMap.print()` 
打印树结构

 `MindMap.visualize(engine)` 
可视化（graphviz/plotly/matplotlib）

 `MindMap.get_terminal_labels()` 
获取叶子节点标签

 `MindMap.get_terminal_label_summaries()` 
获取叶子节点{标签:摘要}

 `MindMap.get_label_summaries()` 
获取所有节点{标签:摘要}

 `MindMap.get_label_to_parent_mapping()` 
叶子→父节点映射

 `MindMap.to_dataframe(leaves_only)` 
转DataFrame

 `MindMap.to_json()` 
转JSON字符串

 `MindMap.save_json(filepath)` 
保存JSON文件

## 思维导图生成器（mindmap/mindmap_generator.py）

方法
说明

 `MindMapGenerator.generate_oneshot()` 
一次性生成

 `MindMapGenerator.generate_refined()` 
精炼生成

 `MindMapGenerator.generate_dynamic(intervals)` 
动态时间段生成

 `MindMapGenerator.bootstrap_refined(n)` 
并行生成n棵精炼树

## 分批规划（smart_batching.py）

方法
说明

 `SmartBatchingPlanner.plan_all_periods(topic, ...)` 
生成完整搜索计划

 `SmartBatchingPlanner.load_universe(csv_path)` 
加载实体宇宙

 `SmartBatchingPlanner.get_comention_volumes(companies, topic, ...)` 
三遍模式查询chunk量

 `SmartBatchingPlanner.get_comention_volumes_iterative(...)` 
迭代模式查询

 `SmartBatchingPlanner.create_baskets(company_volumes, max_chunks)` 
创建分组basket

 `SmartBatchingPlanner.split_period(start, end, period_type)` 
按粒度切分时间

 `SmartBatchingPlanner.generate_report(report)` 
生成人类可读报告

 `SmartBatchingPlanner.export_to_csvs(report, ...)` 
导出CSV

## 搜索执行（search_function.py）

函数
说明

 `execute_search(session, plan, topic, chunk_percentage)` 
Smart搜索执行

 `execute_full_grid_search(session, companies, topic, ...)` 
全网格搜索

 `deduplicate_documents(results)` 
文档去重

## 数据处理（helper.py）

函数
说明

 `load_universe_entities(csv_path)` 
加载实体宇宙（返回set和dict）

 `explode_by_entity(results, valid_ids, id_to_name)` 
按实体展开原始结果

 `explode_to_dataframe(data, universe_csv)` 
展开为DataFrame

 `mask_companies_in_df(df, ...)` 
公司名称掩码

 `entity_statistics(df)` 
实体统计（文档数、情感均值等）

 `prepare_sentiment_dataframe(df)` 
准备情感分析DataFrame

 `get_top_entities_by_volume(df, n)` 
获取新闻量Top N实体

 `build_rolling_impact_signal(df, ...)` 
构建滚动影响信号

 `plot_top_entities_rolling_signal(df, ...)` 
绘制Top实体信号趋势图

 `display_sentiment_volume(df, entity)` 
显示单个实体情感+新闻量图

 `display_top_entities_dashboard(df, daily_sentiment, n)` 
显示Top实体仪表盘

## 结果处理（output_converter.py）

函数
说明

 `convert_to_dataframe(raw_results)` 
原始API结果 → 按chunk展开的DataFrame

## 实体处理（processing_results.py）

函数
说明

 `aggregate_results_by_chunk(results)` 
按chunk聚合搜索结果

 `get_unknown_entities_from_df_column(df, known_entities)` 
找出未知实体

 `extract_companies_from_entity_list(entity_ids, session)` 
从KG API提取公司信息

 `process_entities_and_filter_companies(df, session, universe_csv)` 
处理实体并过滤公司

## 标注器（labeler/screener_labeler.py）

方法
说明

 `ScreenerLabeler.get_labels(df)` 
基础主题标注

 `ScreenerLabeler.get_validation_labels(df)` 
两步验证标注

 `ScreenerLabeler.post_process_dataframe(df)` 
后处理格式化

## 思维导图工具（mindmap/mindmap_utils.py）

函数/变量
说明

 `prompts_dict` 
主题/风险树的提示词模板字典

 `format_mindmap_to_dataframe(text)` 
文本格式思维导图转DataFrame

 `save_results_to_file(results, dir, filename)` 
保存结果到JSON

 `load_results_from_file(dir, filename)` 
从JSON加载结果

## 多主题情感管线（Workflow_multi_theme_sentiment notebook内函数）

函数/类
说明

 `RateLimiter(max_requests_per_minute)` 
线程安全限速器（默认30 req/min）

 `api_request(endpoint, payload, max_retries)` 
带重试和限速的API请求

 `monthly_buckets(start, end)` 
生成月度时间桶列表

 `build_rolling_matrices(long_df, windows)` 
构建滚动矩阵（raw/7d/30d）

 `upload_matrix(field_id, matrix_df, scale, ...)` 
上传MATRIX数据字段到BRAIN

## 比赛演示管线（Competition_Full_Workflow_Demo notebook内函数）

函数/类
说明

 `get_daily_documents(target_date_str, company_ids)` 
按日期获取新闻文档，500/批，带指数退避重试

 `calculate_scores_for_day(documents, valid_ids_set)` 
计算当日所有文档的实体评分，返回  `{entity_id: [scores]}` 

 `run_workflow(start_date, end_date, universe_ids)` 
主执行入口：按日迭代→获取→评分→聚合

 `create_dataframe(entity_data, start, end, universe_ids)` 
将嵌套字典转为DataFrame，保存Parquet

 `create_data_field(data_field_id, data_frame, region, delay, type_name, source)` 
上传MATRIX或VECTOR数据字段到BRAIN

 `calc_average(scores)` 
将评分列表取均值（用于MATRIX）

 `parse_keep_as_list(scores)` 
保持评分列表格式（用于VECTOR）

> **最后的话** ：这个项目看起来复杂，但核心逻辑其实很清晰——就是"搜新闻 → 判好坏 → 算分数 → 上传BRAIN"。建议新手先跑通  `Competition_Full_Workflow_Demo` （最简单，5步搞定），再进阶到  `Workflow_multi_theme_sentiment` （多主题正交信号），最后研究  `Workflow_example`  的LLM高精度方案。三条路径递进互补，选最适合你当前阶段的！祝你比赛顺利

---

## 讨论与评论 (15)

### 评论 #1 (作者: YZ64617, 时间: 3个月前)

补充一下：

- 有效的 date range: **(2021-01-01, 2022-12-31)。** 超过这个区间，无法上传到Brain平台。
- alpha不需要提交，只需要 tagged 为" **DCC2026** "。需要自己记住上传的datafield id是什么，直接simulation就可以了。感觉满意的，打个 **DCC2026。**
- 单个alpha的分值，可以通过performance查看。但是，组合就只能看榜单了。我感觉，可以自己抓取PnL，组合算一下大概的分数。

OS测试：

OS占75%的分数，可以OS数据来自于哪里呢？IS是完整的2021-2022年的数，OS估计只能是这2年的截取。所以，PnL的稳定我个人感觉很重要。那岂不是用training data去test？

**上传了好多datafields，忘记了具体有哪些怎么办？使用下面的API，GET请求**

[api.worldquantbrain.com/users/self/data-fields](https://api.worldquantbrain.com/users/self/data-fields)

---

### 评论 #2 (作者: YZ29225, 时间: 3个月前)

太棒了 感谢大佬

---

### 评论 #3 (作者: MS51256, 时间: 3个月前)

感谢分享，祝您发财
=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #4 (作者: YL96068, 时间: 3个月前)

大佬NB，介绍很清晰，非常感谢。可以去跑多主题模板试试了。

---

### 评论 #5 (作者: BW14163, 时间: 3个月前)

好详细，非常认真，先收藏起来，该天抽时间看一下，刚才刚看了一个关于DCC的帖子，他主要讲了规则层面上DCC的要求，这个帖子从程序应用开始讲解，讲了如何正常运行相关代码，非常不错。

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
Prioritize diversity, strong margin, low correlation, stable diversification; strictly control costs and overfitting.
**********************************

---

### 评论 #6 (作者: XY20037, 时间: 3个月前)

太感谢大佬这份堪称「天花板级」的 DCC 比赛教程了！从背景知识、环境搭建到三大工作流的完整拆解，再到经济学逻辑和实战优化，每一部分都讲得深入浅出、细节拉满。尤其是对三套工作流的对比分析（新手先跑 Competition_Full_Workflow_Demo，进阶用 Workflow_multi_theme_sentiment，高阶试 Workflow_example），直接给新手指明了清晰的学习路径，还补充了日期范围、OS 评分、datafield 查询 API 这些关键踩坑点，实用性拉满！已经收藏反复研读，跟着这套教程走，完全能从零跑通比赛全流程，再次感谢大佬的无私分享！

---

### 评论 #7 (作者: WX84677, 时间: 3个月前)

这教程太硬核了！从环境搭建到三套工作流对比，从API详解到Smart Batching原理，把DCC比赛全流程扒得明明白白。特别是"新手路径C→进阶B→高精A"的递进设计，还有LLM异步坑、token消耗这些细节提醒，都是踩过坑才能写出来的干货。附录函数速查表更是贴心，直接当文档查。感谢整理，省了我至少一周摸索时间！

---

### 评论 #8 (作者: XW23690, 时间: 3个月前)

感谢分享，非常详细，DCC还有很多细节我还没搞懂。

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #9 (作者: WZ33694, 时间: 3个月前)

中文剖析很全面，听了2次课程，都是英文，一知半解。下载了文档，遇到openai_key，测试失败。

一直在找，有没有可能替换openai_key，用其他模型来替代的。

感谢分享！！！

---

### 评论 #10 (作者: SJ65808, 时间: 3个月前)

很详细的分享，感谢大佬的研究

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #11 (作者: MY49971, 时间: 3个月前)

真是手把手教程了，感谢大佬无私奉献

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #12 (作者: ZV96737, 时间: 3个月前)

超级好的帖子，原本自己探索感觉还有点困难，没想到有大佬总结出了这么详细的攻略文档

=================================

measure with data，trade with discipline

=================================

---

### 评论 #13 (作者: YY44020, 时间: 3个月前)

感谢大佬

---

### 评论 #14 (作者: KH21822, 时间: 3个月前)

感谢分享！！！

===================================================================================
===================

=================================

measure with data，trade with discipline!

---

### 评论 #15 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬对于DCC比赛的解释和代码通过。                                                                                      ================================自信人生两百年，会当水击三千里==========================

---

