# 【MCP WorkFlow】一个使用MCP来给Alpha写描述并获取更多启发的工作流

- **链接**: [Commented] 【MCP WorkFlow】一个使用MCP来给Alpha写描述并获取更多启发的工作流.md
- **作者**: WL13229
- **发布时间/热度**: 10个月前, 得票: 86

## 帖子正文

我们都知道，要发挥MCP的功能，就需要把它当作我们的秘书。以下是一个参考工作流，你可以让它照着做，并把Alpha表达式和Region给它，就能给你Alpha进行解释，并给你进一步点塔的启发，和撰写description的台词。

# Alpha Explanation Workflow

This manual provides a step-by-step workflow for analyzing and explaining a WorldQuant BRAIN alpha expression. By following this guide, you can efficiently gather the necessary information to understand the logic and potential strategy behind any alpha.

## Step 1: Deconstruct the Alpha Expression

The first step is to break down the alpha expression into its fundamental components:  **data fields**  and  **operators** .

For example, given the expression  `quantile(ts_regression(oth423_find,group_mean(oth423_find,vec_max(shrt3_bar),country),90))` :

- **Data Fields:**   `oth423_find` ,  `shrt3_bar`
- **Operators:**   `quantile` ,  `ts_regression` ,  `group_mean` ,  `vec_max`

## Step 2: Analyze Data Fields

Use the  `brain-platform-mcp`  tool  `get_datafields`  to get detailed information about each data field.

**Tool Usage:**   `xml <use_mcp_tool> <server_name>brain-platform-mcp</server_name> <tool_name>get_datafields</tool_name> <arguments> { "instrument_type": "EQUITY", "region": "ASI", "delay": 1, "universe": "MINVOL1M", "data_type": "VECTOR", "search": "shrt3_bar" } </arguments> </use_mcp_tool>`

**Tips for effective searching:**

- **Specify Parameters:**  Always provide as much information as you know, including  `instrument_type` ,  `region` ,  `delay` ,  `universe` , and  `data_type`  ( `MATRIX`  or  `VECTOR` ).
- **Iterate:**  If you don't find the data field on your first try, try different combinations of parameters. The  `ASI`  region, for example, has two universes:  `MINVOL1M`  and  `ILLIQUID_MINVOL1M` .
- **Check Data Type:**  Be sure to check if the data is a  `MATRIX`  (one value per stock per day) or a  `VECTOR`  (multiple values per stock per day). This is crucial for understanding how the data is used.

**Example Data Field Information:**

- **`oth423_find`** : A  **matrix**  data field from the "Fundamental Income and Dividend Model" dataset in the ASI region. It represents a "Find score," likely indicating fundamental attractiveness.
- **`shrt3_bar`** : A  **vector**  data field from the "Securities Lending Files Data" dataset in the ASI region. It provides a vector of ratings (1-10) indicating the demand to borrow a stock, which is a proxy for short-selling interest.

## Step 3: Understand the Operators

Use the  `brain-platform-mcp`  tool  `get_operators`  to get a list of all available operators and their descriptions.

**Tool Usage:**   `xml <use_mcp_tool> <server_name>brain-platform-mcp</server_name> <tool_name>get_operators</tool_name> <arguments> {} </arguments> </use_mcp_tool>`  The output of this command contains a wealth of information. For your convenience, a table of the most common operators is included in the Appendix of this manual.

## Step 4: Consult Official Documentation

For more complex topics, the official BRAIN documentation is an invaluable resource. Use the  `get_documentations`  tool to see a list of available documents, and  `get_documentation_page`  to read a specific page.

**Example:**  To understand vector data fields better, I consulted the "Vector Data Fields ðŸ¥‰" document ( `vector-datafields` ). This revealed that vector data contains multiple values per instrument per day and must be aggregated by a vector operator before being used with other operators.

## Step 5: Broaden Understanding with External Research (Optional)

For cutting-edge ideas and inspiration, you can search for academic papers on arXiv using the provided  `arxiv_api.py`  script.

**Workflow:**

1. **Identify Keywords:**  Based on your analysis of the alpha, identify relevant keywords. For our example, these were:  `"short interest"` ,  `"fundamental analysis"` ,  `"relative value"` , and  `"news sentiment"` .
2. **Run the Script:**  Use the  `with-wrappers`  script to avoid SSL errors.
   ```
   python arxiv_api.py "your keywords here" -n 10
   ```

## Step 6: Synthesize and Explain

Once you have gathered all the necessary information, structure your explanation in a clear and concise format. The following template is recommended:

- **Idea:**  A high-level summary of the alpha's strategy.
- **Rationale for data used:**  An explanation of why each data field was chosen and what it represents.
- **Rationale for operators used:**  A step-by-step explanation of how the operators transform the data to generate the final signal.
- **Further Inspiration:**  Ideas for new alphas based on your research.

## Troubleshooting

- **SSL Errors:**  If you encounter a  `CERTIFICATE_VERIFY_FAILED`  error when running python scripts that access the internet, use the  `AI to help you change or make`  script to execute your command.

## Appendix A: Understanding Vector Data

Vector Data is a distinct type of data field where the number of events recorded per day, per instrument, can vary. This is in contrast to standard matrix data, which has a single value for each instrument per day.

For example, news sentiment data is often a vector because a stock can have multiple news articles on a single day. To use this data in most BRAIN operators, it must first be aggregated into a single value using a  **vector operator** .

---

## 讨论与评论 (26)

### 评论 #1 (作者: WL13229, 时间: 10个月前)

撰写类似文章，可以获得更快审批，高价值优秀者可获得礼物。

---

### 评论 #2 (作者: WL13229, 时间: 10个月前)

# 中文版：Alpha 解析工作流程

本手册提供了逐步的工作流程，用于分析和解释 WorldQuant BRAIN alpha 表达式。按照本指南操作，你可以高效地收集所需信息，理解任何 alpha 背后的逻辑和潜在策略。

## 第一步：拆解 Alpha 表达式

第一步是将 alpha 表达式分解为其基本组成部分：数据字段和运算符。

**例如，给定表达式：** 
 `quantile(ts_regression(oth423_find,group_mean(oth423_find,vec_max(shrt3_bar),country),90))`

- **数据字段** ：oth423_find, shrt3_bar
- **运算符** ：quantile, ts_regression, group_mean, vec_max

## 第二步：分析数据字段

使用 brain-platform-mcp 工具的  `get_datafields`  功能，获取每个数据字段的详细信息。

**工具用法：**

```
<use_mcp_tool>
  <server_name>brain-platform-mcp</server_name>
  <tool_name>get_datafields</tool_name>
  <arguments>
    { "instrument_type": "EQUITY", "region": "ASI", "delay": 1, "universe": "MINVOL1M", "data_type": "VECTOR", "search": "shrt3_bar" }
  </arguments>
</use_mcp_tool>
```

**高效搜索技巧：**

- **指定参数** ：尽可能提供已知信息，包括 instrument_type、region、delay、universe 和 data_type（MATRIX 或 VECTOR）。
- **多次尝试** ：如果第一次没有找到数据字段，尝试不同参数组合。例如，ASI 区域有两个 universe：MINVOL1M 和 ILLIQUID_MINVOL1M。
- **检查数据类型** ：务必确认数据是 MATRIX（每只股票每天一个值）还是 VECTOR（每只股票每天多个值）。这对于理解数据的使用方式至关重要。

**示例数据字段信息：**

- **oth423_find** ：来自 ASI 区域“Fundamental Income and Dividend Model”数据集的矩阵型数据字段。代表“Find score”，可能表示基本面吸引力。
- **shrt3_bar** ：来自 ASI 区域“Securities Lending Files Data”数据集的向量型数据字段。提供 1-10 的评级向量，表示借入股票的需求，是做空兴趣的代理指标。

## 第三步：理解运算符

使用 brain-platform-mcp 工具的  `get_operators`  功能，获取所有可用运算符及其说明。

**工具用法：**

```
<use_mcp_tool>
  <server_name>brain-platform-mcp</server_name>
  <tool_name>get_operators</tool_name>
  <arguments>{}</arguments>
</use_mcp_tool>
```

该命令的输出包含大量信息。为方便起见，本手册附录中包含了最常用运算符的表格。

## 第四步：查阅官方文档

对于更复杂的主题，官方 BRAIN 文档是宝贵的资源。使用  `get_documentations`  工具查看可用文档列表，使用  `get_documentation_page`  阅读特定页面。

**示例** ：为了更好地理解向量数据字段，我查阅了“Vector Data Fields”文档（vector-datafields）。了解到向量数据每个标的每天可以有多个值，必须先用向量运算符聚合后才能与其他运算符一起使用。

## 第五步：通过外部研究拓宽理解（可选）

为了获得前沿思路和灵感，可以在论坛搜索他人的相关见解，或使用提供的 arxiv_api.py 脚本在 arXiv 上搜索学术论文。

**工作流程：**

- **确定关键词** ：根据对 alpha 的分析，确定相关关键词。例如本例为：“short interest”、“fundamental analysis”、“relative value”、“news sentiment”。
- **运行脚本** ：使用 with-wrappers 脚本避免 SSL 错误。

```
python arxiv_api.py "your keywords here" -n 10
```

## 第六步：综合并解释

收集所有必要信息后，建议按照以下模板，结构化、简明地撰写解释：

- **思路** ：对 alpha 策略的高层次总结。
- **数据使用理由** ：解释为何选择每个数据字段及其代表含义。
- **运算符使用理由** ：逐步说明运算符如何转换数据以生成最终信号。
- **进一步启发** ：基于你的研究，提出新的 alpha 思路。

## 故障排查

- **SSL 错误** ：如果运行访问互联网的 python 脚本时遇到 CERTIFICATE_VERIFY_FAILED 错误，请使用  `AI创建必要`  脚本执行命令。

## 附录A：理解向量数据

向量数据是一种特殊类型的数据字段，每天每个标的记录的事件数量可以不同。与标准矩阵数据（每天每个标的一个值）不同。

例如，新闻情绪数据通常是向量型，因为一只股票一天可能有多篇新闻。要在大多数 BRAIN 运算符中使用这类数据，必须先用向量运算符将其聚合为单一值。

---

### 评论 #3 (作者: SG46247, 时间: 10个月前)

===================================================================================

先把表达式拆成「数据字段」和「运算符」两大块，就像拆零件一样理清楚基本构成。

接着用 MCP 工具查数据字段：明确股票类型、地区等参数，分清是每天一个值的矩阵数据，还是多个值的向量数据（比如新闻情绪这类），向量数据得先聚合才能用。

然后搞懂运算符：用工具查每个运算符的功能，知道它们是怎么加工数据的。

遇到复杂点的就翻官方文档，还可以搜相关学术论文找灵感。最后把这些信息串起来，说清策略思路、用了啥数据、怎么运算的，就能慢慢入门 Alpha 分析。感谢老师的mcp工作流分享

---

### 评论 #4 (作者: SH67409, 时间: 10个月前)

老师，brain-platform-mcp  在哪里下载呢

---

### 评论 #5 (作者: WL13229, 时间: 10个月前)

[SH67409](/hc/en-us/profiles/29030826126359-SH67409)

已有热心顾问在论坛分享，请查看一些最近的帖子

---

### 评论 #6 (作者: FG26814, 时间: 10个月前)

感谢老师提供的MCP思路， 我之前使用AI进行辅助学习ALpha 表达示的基本版 就是通过简单的提示词来做引导。  
{

你现在是我的Alpha 表达示分析助手  我一般会这样问：

anl69_best_eps_4wk_chg：Dividend per share 4 wk Chg
ts_mean(winsorize(ts_backfill(vec_sum(anl69_best_eps_4wk_chg), 120), std=4), 120)

然后你要按下面的要求回复。

要求：
1. 理念：用一句话概括策略核心思想
2. 数据理由：解释每个数据字段的含义、计算方式和选用原因
3. 运算理由：解释每个运算符的功能和参数设置逻辑
4. 输出格式：
   - 先完整中文分析
   - 后完整英文分析
   - 严格使用```chinese和```english标记代码块
   - english 需要严格的格式
Idea: 
(CONTEXT)
Rationale for data used: 
(CONTEXT)
Rationale for operators used: 
(CONTEXT)
5. 保持简洁，无额外内容
6. 英文内容在100字左右。

如果明白了，请回复，OK，I am ready

}

这次老师给了一个很好的借用大模型的能力来做ALpha 自动化的思路, 可以试试。 

初步思路：
1. 获取一个字段或者多个字段， 或者找到一阶里有信息的字段。
2. 对字段（以及表达示）做拆解，进行解释
3. 对源始字段做不同的特征工程，
4、获得回测的数据进行 剪枝，再回测。 
5. 制定一个弹性的筛选Alpha 的标准，
6. 筛选后的ALpha 列表信息将发送邮件给自己，进行查看。 
试试看这个流程是否能打通。

---

### 评论 #7 (作者: JB53978, 时间: 10个月前)

MCP确实用起来不错，让它写了几个模板跑出来的效果还算不错。这种模板会不会有过拟合的风险，比如：它给我的这个模板：group_neutralize(ts_delta({datafield}, {decay), sector)

---

### 评论 #8 (作者: WL13229, 时间: 10个月前)

[FG26814](/hc/en-us/profiles/28995499404183-FG26814)

不错不错。建议在尝试的时候，先一步步做，看看效果。最后大致满意，就变成一个工作流文档。

---

### 评论 #9 (作者: SL19872, 时间: 10个月前)

可以把operator做成json文件，datasets可以下载到本地，让大模型去读取理解

---

### 评论 #10 (作者: CW99271, 时间: 10个月前)

很不错的想法，希望能有更多人来使用这个功能，并总结出更多经验供大家学习

---

### 评论 #11 (作者: YQ51506, 时间: 10个月前)

感谢各位大佬的分享，集思广益，让大家的MCP更加智能，高效生成alpha

---

### 评论 #12 (作者: BL59663, 时间: 9个月前)

目前还在对MCP的摸索阶段，感谢大佬们的精彩分享，希望能把这些精华都吸收进去，创新出好的模版

---

### 评论 #13 (作者: WL58980, 时间: 2个月前)

感谢大家的分析，受益匪浅！

Learning is endless!!!

=============================================================================

Study hard — quality over quantity, no room for mediocrity. Cherish every learning opportunity, stay focused, and learn from the experts. Keep pushing!

=============================================================================

---

### 评论 #14 (作者: SK10818, 时间: 9个月前)

老师，这个流程有点像是完成的prompt工程，请问这个流程应该怎么使用呢？是放在md里面交个mcp去读取吗？

---

### 评论 #15 (作者: ZL74029, 时间: 9个月前)

通过这个文章和评论让我受益匪浅，也去摸索一下，共勉

---

### 评论 #16 (作者: LN13454, 时间: 9个月前)

这个还是需要有 googel的 gemin cli 才行，因为这个token 确实费钱，alpha没挖到，钱到去了不少，这个分享很有参考意义，谢谢，谢谢

=================================这个值得学习，谢谢分析=========================

哦，谢谢分享

---

### 评论 #17 (作者: SQ89646, 时间: 9个月前)

感谢大佬分享 有mcp很多操作都快了很多 就是token消耗的有点快哈哈

---

### 评论 #18 (作者: CM61969, 时间: 9个月前)

感谢各位大佬的分享,又是在论坛长脑子的一天。

---

### 评论 #19 (作者: JX79797, 时间: 9个月前)

[SK10818](/hc/en-us/profiles/29090704445463-SK10818)

是的，输入框直接输入，使用xxxx.md工作流，为xxxxx(表达式)输出描述

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**

**# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%**

**# sys.setrecursionlimit(α∞)**

**# PnL = ∑(Robustness * Creativity)**

**#无限探索、鲁棒性优先，创新性增值**

**#=================奋进的小徐=======================#**

---

### 评论 #20 (作者: JQ70858, 时间: 9个月前)

看来要学的还很多。。。先mark一下。 T_T

---

### 评论 #21 (作者: GQ89952, 时间: 8个月前)

不错不错

---

### 评论 #22 (作者: SZ20589, 时间: 8个月前)

老师，这个流程是要把它拷贝到MCP哪里呢？是要一步步输入给MCP还是说直接把这个流程文档给MCP它就能工作了？

MCP 工具明确股票类型、地区等参数，分清值的矩阵数据，还是多个值的向量数，向量数据得先聚合才能用，用工具查每个运算符的功能，知道它们是怎么加工数据的。这些方面是挺有用的，感谢老师

=================================感谢老师分享=========================

---

### 评论 #23 (作者: PY58917, 时间: 8个月前)

谢谢weijie老师在国庆假期还为我们组织线上的聊天会，会上也提到了要我们跟上时代的脚步，学习使用ai agent、mcp等应用，时值国庆、中秋佳节，也正好是我们研习mcp的好时机。

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**  **#========= 希望大家都可以解决Alpha挖掘中的探索、语义理解和多样性这三大核心问题========== #**  **#=========知过必改，得能莫忘 ========== #**

---

### 评论 #24 (作者: DZ64073, 时间: 8个月前)

很好很好👍

---

### 评论 #25 (作者: YH87796, 时间: 8个月前)

已经安装好MCP了，但是感觉还是没有使用它的思路，大家平时都是怎么使用MCP来帮助做因子研究的呢

=================================================================================

---

### 评论 #26 (作者: YJ72634, 时间: 8个月前)

SZ20589
我的理解是用那种claude code这类的cli工具，然后把老师给的这一大长段放到给模型预设的参考prompt的readme.md文件里。

---

