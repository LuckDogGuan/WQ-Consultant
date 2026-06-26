# 【AIAC】激情燃烧的5天及未来展望

- **链接**: [Commented] 【AIAC】激情燃烧的5天及未来展望.md
- **作者**: WF37935
- **发布时间/热度**: 7个月前, 得票: 14

## 帖子正文

首先看3张图，解释一下标题。

![图片](images/img_fc9c73bb5a.png)

![图片](images/img_5630e5937c.png)

![图片](images/img_221b33ddeb.png)

5天时间，勉强提交够了10个SA，满足了AIAC比赛的最低要求。最大的收获，是切身感受到了AI的可能性。之前虽然也一直用AI、MCP，但是总感觉差点什么，不能够很好的满足我的要求，最大的作用就是给我写description。在这个比赛中，AI确实做出来了很多东西，给了我很大的惊喜。
下面分享下我比赛代码的思路，官方给了一个框架，里面有两个主要的方法，generate_alpha_description和generate_new_alphas。generate_alpha_description没太多好说的，就是让AI根据你提供的alpha的表达式做一个解释。而generate_new_alphas，是根据上一步的解释，使用brain的字段和操作符生成表达式。由于我用的是免费的心流api，在实践中迭代了几次后，对任务进行了拆分，保证每次更大可能生成有效的输出。首先是根据alpha description提炼出几个关键词，然后使用关键词去brain平台查询对应的字段，对这些字段按照数据集分组，每一组调用一次AI生成alpha表达式，循环执行。同时，根据每组对应的数据字段的个数，设置生成的alpha表达式的个数，字段数越多，生成的表达式越多，上限设置15-20个。如果设置太多的话，很难跑的完，而且相关性估计也比较高。在官方的这两步做完后，开始回测，这是第一次回测。对于回测结果，把sharpe<-0.6的表达式添加一个负号，进行第二次回测，把负的alpha变成正的。再把所有回测结果中，sharpe>0.6的，调用AI进行一次增强，让AI增删操作符、替换操作符，然后进行第三次回测。最后从所有的回测结果中，挑选一些进行提交。
对后续的展望：虽然比赛要求parent alpha必须是已提交的，但是比赛结束了，可以拓展下思路。比如我看到了一些好的表达式，那我可以手动回测下，然后把回测的alpha作为parent alpha。或者我有一些pc高的alpha，但是我觉得这个idea很好，那我可以把它作为parent alpha，让AI生成一些不同的实现方式，说不定pc就低了。当然，这只是个人的猜想，有待实践。

由于代码太长了，我只分享一下我的两个prompt，第一个是生成表达式的，第二个是优化表达式的，里面包含了一些变量，仅供参考，不能直接使用。

```
    prompt = f"""    You are an alpha expression generator for the WorldQuant BRAIN platform. Your primary task is to create valid, economically meaningful alpha expressions that comply with platform specifications.    **Core Generation Principles:**    1. **Platform Compliance**    - Use only operators and data fields that exist in the platform's official documentation    - Ensure all function names, parameters, and syntax match supported specifications    - **CRITICAL SYNTAX FIXES**:        - When using `ts_decay_linear(x, d, dense = false)`, you MUST include the equals sign and write it as `dense = false`. NEVER write just `dense false` as this will cause syntax errors.        - When using `kth_element(x, d, k)`, you MUST provide values for all three parameters and use named parameter syntax for k: `kth_element(x, d, k = value)`.             - **k VALUE CONSTRAINT**: The k parameter MUST be a positive integer (k ≥ 1). NEVER use k = 0 or negative values.            - **SYNTAX REQUIREMENT**: Always use named parameter syntax `k = value`. NEVER use positional arguments like `kth_element(x, d, 1)`.    2. **Economic Significance**    - Create expressions with clear financial or economic rationale    - Focus on signals that represent genuine market relationships or behavioral patterns    - Avoid purely mathematical combinations without economic justification    3. **Type Safety Rules**    - **VECTOR OPERATIONS PRECEDENCE**: When working with vector-type data fields, you MUST apply vector operators FIRST before any other operations    - **PROHIBITED DIRECT OPERATIONS**: Never use vector fields directly in regular mathematical functions without proper vector operator conversion    - **CORRECT SEQUENCE**: Always convert vectors to matrices using appropriate vector operators BEFORE using in time-series, group, or other matrix operations    - **VALIDATION CHECK**: Before generating any expression, verify that all vector fields are processed through vector operators first in the operation sequence    - **CRITICAL: NEVER apply vector operators to MATRIX-type fields** - Vector operators are exclusively for VECTOR-type data fields only    4. **Expression Requirements**    - Number of total operators ≤ (including repeat operators)    - **CRITICAL FIELD DIVERSITY CONSTRAINT**:        - **Field Usage Limit**: Each unique data field (excluding grouping fields) can appear in AT MOST 3 different expressions        - **Distribution Strategy**: You MUST distribute field usage evenly across all available data fields        - **Avoid Repetition**: Do NOT repeatedly use the same few popular fields across multiple expressions    5. **Group Field Usage**    - **Permitted group fields**: `country`, `industry`, `subindustry`, `currency`, `market`, `sector`, `exchange` (use exactly as specified)    - **GROUP FIELD RESTRICTIONS**:        - Group fields can ONLY be used within group operators for categorization purposes        - Never use group fields as direct numerical inputs in calculations        - In operators like `group_neutralize(x, group)`, `group` parameter MUST be a group datafield, while `x` MUST be a matrix-type field        - **Special Note:** `group_cartesian_product` operator specifically requires exactly two group datafields as input parameters. You must NEVER use non-group type datafields as parameters for this operator    6. **Expression Quality**    - Generate expressions with proper mathematical structure and function nesting    - Ensure parameter counts match operator requirements    - Create diversified signals across different data types and time horizons    **CRITICAL REMINDERS**:     - Always apply vector operators as the first step when processing vector-type data fields.    - STRICTLY enforce field usage limits: maximum 3 expressions per unique data field    - Ensure FIELD USAGE DIVERSITY across all available data fields    - **NAMED PARAMETER REQUIREMENT**: For functions with named parameters (winsorize, kth_element, ts_decay_linear, etc.), you MUST use named parameter syntax: `function(x, param_name = value)`    - **GROUP FIELD PLACEMENT**: In group operators, group datafields can ONLY be used in the group parameter position (g, g1, g2, group, etc.), NEVER as the main input (x parameter)    Your goal is to produce sophisticated, platform-compliant alpha expressions that demonstrate both technical correctness, economic insight, and FIELD USAGE DIVERSITY.    Based on the following description: '{alpha_description}', generate {num_alphas} new alpha expressions using the provided operators and data.    Operators: {operators[operators['scope']=='REGULAR'].to_json()}, data {data_fields.to_json()} where id is data field name    **TYPE USAGE RULES:**    - **MATRIX fields**: Can be used directly in Arithmetic, Cross Sectional, Time Series operators, With Logical and Transformational operators, As group in Group operators, with bucket()    - **VECTOR fields**: CANNOT be used by itself. Must be wrapped in category=Vector operator FIRST, then treated as MATRIX field    - **GROUP fields**: CANNOT be used by itself. Must be used as "group" parameter in Group operator only    - **NEVER use vector operators on MATRIX-type data fields** - vector operators are strictly for VECTOR-type fields only    **FIELD DIVERSITY REQUIREMENT**:     You MUST ensure that the {num_alphas} expressions use a VARIETY of different data fields. Do NOT concentrate on the same fields repeatedly. Spread usage across all available fields in this dataset.    **PARAMETER PASSING RULE**:     When a function requires named parameters (e.g., `winsorize(x, std=4)`, `kth_element(x, d, k=1)`, `ts_decay_linear(x, d, dense=false)`), you MUST use named parameter syntax and CANNOT use positional arguments.    Provide only {num_alphas} alpha expressions in a json format, they should not be the same.    Return a JSON array where each element has these properties:    - "expression": The alpha expression you provide    - "description": the economically meaning of the alpha expression    """
```

```
    prompt = f"""    You are an alpha expression optimizer for the WorldQuant BRAIN platform. Your task is to optimize multiple existing alpha expressions while maintaining platform compliance and economic significance.    **Core Optimization Principles:**    1. **Platform Compliance**    - Use only operators and data fields that exist in the platform's official documentation    - Ensure all function names, parameters, and syntax match supported specifications    2. **Optimization Strategies**    For EACH input expression, provide THREE optimized versions using these approaches:    - **Add operators**: Enhance signal quality by adding relevant operators (noise reduction, smoothing, normalization)    - **Reduce operators**: Simplify complexity while preserving core signal (remove redundant operations)    - **Replace operators**: Substitute with more appropriate operators for better performance or interpretation    3. **Performance-Driven Optimization Priorities**    Focus on modifications that most significantly improve:    - **Signal-to-noise ratio**: Add smoothing (ts_mean, ts_decay), outlier handling (rank, scale), or volatility adjustment    - **Robustness**: Incorporate multiple time horizons, cross-validation mechanisms, or group normalization    - **Economic intuition**: Strengthen the financial rationale behind the signal    - **Computational efficiency**: Remove redundant operations while preserving alpha essence    - **Risk management**: Add neutralization (group_neutralize), scaling, or bounding operations    4. **Type Safety Rules**    - **VECTOR OPERATIONS PRECEDENCE**: When working with vector-type data fields, you MUST apply vector operators FIRST before any other operations    - **PROHIBITED DIRECT OPERATIONS**: Never use vector fields directly in regular mathematical functions without proper vector operator conversion    - **VALIDATION CHECK**: Verify that all vector fields are processed through vector operators first in the operation sequence    - **CRITICAL**: NEVER apply vector operators to MATRIX-type fields    5. **Expression Requirements**    - Maintain or improve economic rationale    - Ensure mathematical validity and platform compatibility    - Optimize for signal clarity and robustness    - **PARAMETER PASSING RULE**: When a function requires named parameters (e.g., `winsorize(x, std=4)`), you MUST use named parameter syntax and CANNOT use positional arguments. If the original expression uses positional arguments for such functions, you MUST convert them to named parameters.    **Available Operators:** {operators[operators['scope']=='REGULAR'].to_json()}    **Optimization Task:**    You will optimize the following {len(expression_list)} alpha expressions:    EXPRESSIONS TO OPTIMIZE:    {chr(10).join([f"{i+1}. {expr}" for i, expr in enumerate(expression_list)])}    For EACH expression in the list above, provide THREE optimized versions. You can add operators, replace operators, or reduce operators. Focus on making the MOST MEANINGFUL and PERFORMANCE-ENHANCING modifications that will significantly improve:    - Predictive power and signal quality    - Robustness across market regimes      - Risk-adjusted returns    - Economic interpretability    - Computational efficiency    **Return Format:**    Provide a JSON object where:    - Keys are the original expression strings    - Values are arrays of exactly 3 optimization objects, each containing:    - "optimized_expression": The improved alpha expression    Ensure that for each original expression, you provide three distinct and meaningfully different optimized versions.    """
```

---

## 讨论与评论 (11)

### 评论 #1 (作者: LZ25854, 时间: 7个月前)

谢谢楼主的详细分享！作为新人顾问，我这次并没有参加 AIAC 比赛，主要还是因为对 AI 生成因子的技术栈不够熟练，很多流程都还在尝试中。不过读完你这篇实战总结，感觉自己一下子把之前不明白的部分串起来了，特别是你把 generate_alpha_description、generate_new_alphas 的拆解逻辑讲得很清楚，让我学习到了很多。

你提到的关键词提取、按数据集分组调用 AI、控制表达式数量，以及三轮回测（负号反转、增强、再筛选）这些思路，对我这种还没开始大规模实践的新手来说非常有价值。我之前完全没想到可以通过这种“分解任务 + 控制输出规模”的方式提升有效率，也谢谢你提供的prompt。

特别是你后面讲的思路拓展，比如把手动回测好的 alpha 当 parent alpha，或者用 AI 去改写一些 PC 高但逻辑好的因子，这些都是我之前没意识到的方向，感觉未来真的可以多尝试。

感谢分享你的 prompt 思路，对我这种正在摸索 AI 辅助建模的人非常有启发。

---

### 评论 #2 (作者: BW14163, 时间: 7个月前)

感谢分享，好诱人的base，一看佬vf0.96，再加上主题加成，这么高的base就感觉很平常了。
根据alpha描述，通过ai提炼关键词，再生成15-20个表达式，这一路径，感觉可以在明年的方案调整中很好的应用，很有参考的价值。
就是因此产生的alpha，自相关过高，比较麻烦。

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
Prioritize diversity, strong margin, low correlation, stable diversification; strictly control costs and overfitting.
**********************************

---

### 评论 #3 (作者: CC21336, 时间: 6个月前)

对于我这个点塔困难户，官方文档中的那两个接口感觉帮助巨大。用DeepSeek找到很多意想不到的ALpha

---

### 评论 #4 (作者: YH25030, 时间: 6个月前)

太燃了！ 谢谢您的分享。 您的prompt启发了我的思路，准备改进一下自己的模板。

---

### 评论 #5 (作者: ZS61081, 时间: 6个月前)

用的是哪个模型啊？

---

### 评论 #6 (作者: WF37935, 时间: 6个月前)

[ZS61081](/hc/en-us/profiles/26947351890327-ZS61081)   用的glm4.6。心流的模型我都用了一遍，就这个用在我的代码里不怎么报错，效果也好点

---

### 评论 #7 (作者: WF37935, 时间: 6个月前)

[BW14163](/hc/en-us/profiles/28900537669399-BW14163)  你说的很对，但是有一点，就是用一个parent生成的十几个child alpha，组成一个sa，这个sa很可能是sharpe 2 fitness 2 prod 0.6几这种情况。在主题的加持下，却能够比35的base高不少。还有就是如果是通过关键词搜字段的话，如果这个idea不是特别窄的话，一般会搜到多个数据集的字段，自相关还是有可能低一点的。

---

### 评论 #8 (作者: ZY88181, 时间: 6个月前)

刚看到这个帖子，写的太好了，学习一下。

---

### 评论 #9 (作者: LY85808, 时间: 6个月前)

感谢分享，来学习学习

---

### 评论 #10 (作者: CC21336, 时间: 6个月前)

我的提示词可能不够规范，经常产生幻觉生成异常表达式。准备试一试大佬的这个提示词。

---

### 评论 #11 (作者: MZ45384, 时间: 4个月前)

大佬的prompt非常地详细，学习了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

