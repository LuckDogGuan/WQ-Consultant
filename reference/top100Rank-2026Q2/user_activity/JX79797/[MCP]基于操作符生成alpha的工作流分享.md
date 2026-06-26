# [MCP]基于操作符生成alpha的工作流分享

- **链接**: [MCP]基于操作符生成alpha的工作流分享.md
- **作者**: JX79797
- **发布时间/热度**: 8个月前, 得票: 105

## 帖子正文

使用的工具链参考：  [https://support.worldquantbrain.com/hc/zh-cn/community/posts/34505447952407](/hc/zh-cn/community/posts/34505447952407)

本工作流的主要目的是，不让一个操作符流落在外，达到每个操作符都有提交。

**使用推荐： 稀有操作符 + 常见数据集， 也可以试试小数据集碰碰运气能不能暴击**

**流程图：**

**![图片](images/img_bb2a9e5fbe.png)**

1. 定义参数与学习：设置配置参数并从`data/gold_operators.csv`学习操作符定义

2. 加载数据集元数据：从`data/datasets/`加载并筛选相关数据集

3. 加载并筛选字段：从`data/fields/`加载字段并识别其类型(matrix/vector)

4. AI理解、组合与验证：智能生成表达式，应用正确的操作符，并进行严格验证

5. 保存表达式：将生成的有效表达式保存到指定输出文件

**示例：**

**Cine交互输入框输入：**

```
使用 intelligent_alpha_generation_workflow.md工作流，使用ts_covariance操作符以及region eur delay 1 universe TOP2500 instrumentType Equity, 使用socialmedia category里的字段生成30个alpha表达式，不超过两个操作符，不超过两个字段
```

**生成表达式列表：**

```
expressions = ["ts_covariance(scl12_sentiment, scl12_buzz, 10)","-ts_covariance(scl12_sentiment, scl12_buzz, 20)","ts_covariance(vec_avg(scl15_d1_risk_score), vec_avg(scl15_d1_conflict), 10)","-ts_covariance(vec_avg(scl15_d1_risk_score), vec_avg(scl15_d1_conflict), 20)","ts_covariance(vec_avg(scl15_d1_trust), vec_avg(scl15_d1_fundamentalstrength), 10)","-ts_covariance(vec_avg(scl15_d1_trust), vec_avg(scl15_d1_fundamentalstrength), 20)","ts_covariance(vec_avg(scl15_d1_pricedirection), vec_avg(scl15_d1_buzz), 10)","-ts_covariance(vec_avg(scl15_d1_pricedirection), vec_avg(scl15_d1_buzz), 20)","ts_covariance(vec_avg(scl15_d1_optimism), vec_avg(scl15_d1_sentiment), 10)","-ts_covariance(vec_avg(scl15_d1_optimism), vec_avg(scl15_d1_sentiment), 20)","ts_covariance(vec_avg(scl15_d1_longshort), vec_avg(scl15_d1_stress), 10)","-ts_covariance(vec_avg(scl15_d1_longshort), vec_avg(scl15_d1_stress), 20)"...]
```

**得到可提交alpha：**

![图片](images/img_e2d106116a.png)

**工作流内容**

```
# AI-Driven, Semantically-Aware Alpha Generation Workflow (Local)This document outlines an advanced, robust workflow for generating financial alpha expressions. The process is driven by an AI assistant, operates entirely on local data, and focuses on creating semantically meaningful and syntactically correct alphas.## Workflow Diagram```mermaidgraph TDsubgraph "输入与学习 (Input & Learning)"A[1. 定义参数与学习<br>Define Parameters & Learn<br><br><b>用户输入:</b><br>- Region, Universe, Delay, Category, Operator<br><br><b>AI学习 (关键):</b><br>- <b>必须</b>从 `data/gold_operators.csv` 学习操作符定义、参数和用法。]endsubgraph "本地数据检索 (Local Data Retrieval)"B[2. 加载数据集元数据<br>Load Dataset Metadata<br><br><b>路径 (本地):</b><br>`data/datasets/EQUITY_{REGION}_{DELAY}_{UNIVERSE}.csv`<br><b>动作:</b><br>读取并解析CSV，根据`Category`筛选数据集ID。]C[3. 加载并筛选字段<br>Load & Filter Fields<br><br><b>路径 (本地):</b><br>`data/fields/EQUITY_{REGION}_{DELAY}_{UNIVERSE}.csv`<br><b>动作:</b><br>1. 加载所有字段。<br>2. 根据数据集ID筛选出`Category`相关字段。<br>3. 识别每个字段的类型 (matrix vs. vector)。]endsubgraph "AI智能生成与验证 (AI-Powered Generation & Verification)"D[4. AI理解、组合与验证<br>AI Understands, Combines & Verifies<br><br><b>过程:</b><br>- <b>处理Vector:</b> 对vector类型字段使用`vec_avg`等聚合。<br>- <b>组合字段:</b> 寻找经济学上合理的组合。<br>- <b>应用操作符:</b> 使用正确语法和分组关键字。<br>- <b>最终验证 (强制):</b> 重新检查每个表达式中所有字段的类型。]endsubgraph "输出 (Output)"E[5. 保存表达式<br>Save Expressions<br><br><b>工具:</b> `write_to_file`<br><b>内容:</b> 生成的、经过验证的、语法正确的表达式列表。]endA --> B;B --> C;C --> D;D --> E;```## Detailed Steps### 1. Define Parameters & Learn- **User Input**: The user specifies the target parameters for the generation task: `Region`, `Universe`, `Delay`, `Category`, `Operator`.- **AI Learning (Crucial Step)**: The AI **must** retrieve and analyze the operator's definition, parameters, and correct syntax from the local file: `data/gold_operators.csv`.### 2. Load Dataset Metadata (Local)- **Action**: The AI reads the appropriate dataset metadata file from the `data/datasets/` directory (e.g., `data/datasets/EQUITY_EUR_1_TOP2500.csv`).- **Parsing**: It extracts `dataset_id`s that match the specified `Category`.### 3. Load & Filter Field Metadata (Local)- **Action**: The AI reads the comprehensive field metadata file from the `data/fields/` directory (e.g., `data/fields/EQUITY_EUR_1_TOP2500.csv`).- **Parsing and Filtering**:1.**Load All Fields**: Ingest the entire list of available data fields.2.**Identify Field Types**: Note whether each field is a `matrix` (scalar) or `vector` (event). This is a critical piece of information for each field.3.**Filter by Category**: Retain only the fields relevant to the specified `Category`.### 4. AI Understands, Combines & VerifiesThis is the central, multi-stage intelligence step.1. **Handle Vector Fields**: **Crucially**, if a field is of type `vector`, it **must** be aggregated into a scalar value before being used in operators that expect scalar inputs (like arithmetic or group operators). Use `vec_avg()`, `vec_sum()`, or `vec_count()` for this purpose.2. **Find Meaningful Combinations**: The AI analyzes the `description` of scalar fields and *aggregated* vector fields to identify opportunities for economically sound combinations.3. **Construct Expressions**: The AI constructs expressions by strictly adhering to the operator syntax and using valid grouping keywords.-**Valid Grouping Keywords**: `subindustry`, `industry`, `sector`, `country`, `exchange`. These are platform-native keywords, not field names.4. **Final Verification (Mandatory)**:- Before outputting the final list, the AI **must** perform a final check on every generated expression.- For **every single field** within an expression, its type must be re-verified against the `fields.csv` file.- Any expression containing a raw `vector` field in a scalar context (e.g., direct arithmetic) **must be corrected or discarded**. This step is non-negotiable and prevents `event inputs` errors.-**Correct Example**: `group_median(snt21_2pos_mean_96 - vec_avg(snt12_lst_trgt_price), country)` (scalar minus an aggregated vector is valid).-**Incorrect Example**: `group_median(snt21_2pos_mean_96 - snt12_lst_trgt_price, country)` (This will fail because `snt12_lst_trgt_price` is a vector).### 5. Save Verified Expressions- **Action**: The AI takes the final, fully verified list of alpha expressions.- **Output**: Using the `write_to_file` tool, it saves this Python list into a specified output file, ready for simulation.
```

```

```

---

## 讨论与评论 (8)

### 评论 #1 (作者: JX28185, 时间: 8个月前)

看了一下兄台对  Vector Operator  的使用，感觉很牛气，继续学习

---

### 评论 #2 (作者: MY82844, 时间: 8个月前)

是说AI可以通过理解，从全遍历集合里面筛选掉一些不太合理的，从而缩减计算量吗？

---

### 评论 #3 (作者: DX67257, 时间: 8个月前)

感谢大佬，分享

另辟蹊径

---

### 评论 #4 (作者: FF56620, 时间: 8个月前)

佬这个工作流效果好啊，我之前也尝试让ai生成表达式，但是比较难的是处理幻觉，一方面他可能自创字段和operator，另一方面是operator的参数可能会瞎搞，造成一堆测试错误，不知道大佬是怎么解决这些问题的

--------------------------------------

“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）

--------------------------------------

---

### 评论 #5 (作者: JW85895, 时间: 8个月前)

非常有用，最近刚好在用mcp试试跑这个流程，就有大佬整理出来了，感谢

---

### 评论 #6 (作者: AH18340, 时间: 8个月前)

给定操作符，和字段，让大模型生成alpha表达式，真棒

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #7 (作者: KX44437, 时间: 7个月前)

[FF56620](/hc/en-us/profiles/29176848908951-FF56620) 
我一般新对话开始之前先让他学一下我可以用的所有操作符，基本就不会出操作符方面的幻觉了，和人差不多，学过看过才会，不然就是根据经验猜了

---

### 评论 #8 (作者: FF65210, 时间: 5个月前)

感谢大佬的经验分享，我的工作流又多了一种研究方式，祝大佬早日GM，VF1.0，步步高升

---

