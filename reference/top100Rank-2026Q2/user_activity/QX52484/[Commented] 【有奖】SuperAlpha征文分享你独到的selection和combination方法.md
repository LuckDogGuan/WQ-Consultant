# 【有奖】SuperAlpha征文：分享你独到的selection和combination方法！

- **链接**: [Commented] 【有奖】SuperAlpha征文分享你独到的selection和combination方法.md
- **作者**: WL13229
- **发布时间/热度**: 1 year ago, 得票: 67

## 帖子正文

一句话总结该活动：直接在评论区评论，分享高质量selection或者combo。

> ```
> 被审核通过者将获得BRAIN纪念品一份优秀分享更有机会将获得50USD的一次性津贴。
> ```

活动时间：即日起至6.14日23：59（以服务器时间为准）

活动要求：参赛同学可发布多个idea参赛，可以是selection idea或者combo idea；必须展示setting。同一人可发布多条评论参赛，一个评论仅能放1个idea。同一人不可领多份奖励，但被发出的评论越多会更容易获得较多点赞。

![图片](images/img_6046a81d99.jpeg)

> 纪念品图

再次强调🎇

**被审核通过者将获得BRAIN纪念品一份
优秀分享更有机会将获得50USD的一次性津贴。**

---

## 讨论与评论 (49)

### 评论 #1 (作者: WL13229, 时间: 1 year ago)

**获得纪念品的名单： [LA79055](/hc/en-us/profiles/28845324426135-LA79055) ， [JB71859](/hc/en-us/profiles/26720563911063-JB71859) ， [PW58059](/hc/en-us/profiles/25878520088087-PW58059) ， [PZ64174](/hc/en-us/profiles/28846373031959-PZ64174) ， [WP88606](/hc/en-us/profiles/27032592505751-WP88606) ， [MY27687](/hc/en-us/profiles/28843046087063-MY27687) ， [ZL35633](/hc/en-us/profiles/28828582941975-ZL35633) ， [WH24469](/hc/en-us/profiles/13991511763607-WH24469) ， [JL40454](/hc/en-us/profiles/28831795834263-JL40454) ， [LW49759](/hc/en-us/profiles/26717472313751-LW49759) ， [CH62432](/hc/en-us/profiles/28879407938455-CH62432) ，LZ14530， [LX31898](/hc/en-us/profiles/30215090251159-LX31898) ，KL64183， [YX23928](/hc/en-us/profiles/27479819504663-YX23928) ， [KZ79256](/hc/en-us/profiles/13609593802263-KZ79256) ， [LH44620](/hc/en-us/profiles/26717918976919-LH44620) ，MZ54236， [JR23144](/hc/en-us/profiles/28844048981143-JR23144) ， [HW93328](/hc/en-us/profiles/28771941793815-HW93328) ，XY91783， [XC66172](/hc/en-us/profiles/28880767093655-XC66172) ， [CL88457](/hc/en-us/profiles/25846674784919-CL88457)**

**获得优胜奖名单： [ZL29184](/hc/en-us/profiles/22955594228503-ZL29184) ， [ZS59763，](/hc/en-us/profiles/26858512793111-ZS59763)  [YB49779，](/hc/en-us/profiles/26716038151319-YB49779)  [KD86036，](/hc/en-us/profiles/27031622119831-KD86036)  [AK76468](/hc/en-us/profiles/28846915371031-AK76468) ， [YW93864](/hc/en-us/profiles/14096946892439-YW93864)**

**相关链接地址将发送至您邮箱。**

**SuperAlpha是一个很好地弥补自身组合缺点的方式，请一定要识别本身组合需提升的方面。**

**示例Idea:将自己高流动性的Alpha与池中进行组合**

**类别：selection**

![图片](images/img_3666081085.png)

> 注意：selection数量为30仅为展示，不建议将该数量设置过低。

```
# 选择一部分自己池中流动性较好的,并给较大权重，保证自己的都先被选上self_set = (own&&universe_size(universe)<=1000)*2; # 选择池中低换手,高流动性股票池的新顾问的Alpha,他们可能会带入一些新想法# 且如果该Alpha的作者相关性越低，就越容易选到这个alphapool_set = (!own && author_turnover<0.1 && author_tenure <100 && universe_size(universe)<=500) *author_self_correlation ; # 将两个分数相加，请注意，我们使得只要满足self_set的Alpha一定可以获得高分，保证了自己的都先被选上self_set+pool_set
```

---

### 评论 #2 (作者: ZL29184, 时间: 1 year ago)

**Idea:选取一个较大集合中不相交的子集**

**类别：selection**

**![图片](images/img_3ee4df4fe2.png)**

我个人倾向选取40个以上的。

```
not(own) && #选择别人的alpha保证有足够的alpha(universe =='TOP3000')&& #选择同一个universe的，这个可以后续调整(neutralization =='SECTOR')&&#选择同一个neutralization的，这个可以后续调整(dataset_count ==1 )&&#选择dataset_count ==1的，也就是atom alpha，1这个参数可以后续调整in(datasets, "fundamental6")#选择某一个数据集的alpha，可以选单个，也可以选多个数据集
```

本质上是做出可以组合的拼图，选出一些互相不相交的alpha集合，并且保证它们有相对一致的特征。关于这个不相交，你可以设置不同的参数阈值，使得在固定的维度，你的alpha集合被分为若干个不相交的子集。上面只是一个例子，最后在USA TOP3000选出来了6个alpha，你也可以适当放宽条件以选取更多。

你也可以自由删减这些特征，也可以把若干个加起来。
根据我的实践，这个selection思想足够帮你做出很多相关性很低，能提高组合表现的sa。

祝各位在sa的比赛中有好成绩！

2025/05/30

于广州

---

### 评论 #3 (作者: ZS59763, 时间: 1 year ago)

类别：SELECTIONN

表达式：

(

not(own)&&

#选择不是自己的因子

((turnover<0.07&&turnover>0.05)||

(turnover<0.15&&turnover>0.13)||

(turnover<0.12&&turnover>0.09))

#按照turnover进行分层，每次选取不同的范围以保证每次选到的因子不同，提升多样性

&&(operator_count<8)  &&(dataset_count<=2)

#限制op和pyramid个数，降低过拟合的概率

&&(prod_correlation<0.5&&prod_correlation>0.1)

#按照prodcor筛选，0.5可以保证充分的分散化，0.1则是保证不选到奇奇怪怪的东西（一些厂或者极端的pnl）

#以上为组合部分，以下为权重分配

)

/(turnover*s_log_1p(turnover)

#按照turnover进行加权

*sigmoid(self_correlation)

*sigmoid(prod_correlation)

#按照prodcor进行加权，为了防止权重变化过大，比如0.5和0.1权重差五倍，容易集中到一个因子上去

*abs(long_count-short_count))

#按照多空进行加权，对于多空平衡的因子赋予更高权重，可以避免选到偏多或者偏空因子

其他参数： ![图片](images/img_d459dc8acc.png)

最终结果：

![图片](images/img_05e9dee6f9.png)

---

### 评论 #4 (作者: LA79055, 时间: 1 year ago)

分段条件判断和乘法组合

默认设置：

![图片](images/img_8c7c81724e.png)

类别1：Selection

```
"multiplier = if_else(category == 'FUNDAMENTAL', 1.3, 1.1);\n""adjustment = if_else(decay < 2.0, 1.5, 1);\n""base = sqrt(universe_size(universe));\n""score = multiplier * adjustment * base;\n""if_else(turnover > 0.33, nan, score)",
```

- **类别权重（multiplier）**  – 使用  `if_else`  检查  `category`  是否为  `"FUNDAMENTAL"` 。如果是，则赋值 1.3，否则为 1.1。这说明在该策略体系中，与基本面（FUNDAMENTAL）相关的 α 被认为更有价值，所以获得更高的加权因子。
- **衰减调整（adjustment）**  – 根据  `decay` （衰减）参数是否小于 2.0，赋予 1.5 或 1。通常，较低的衰减可能表明信号稳定性更高，从而给予一个额外加成。
- **基础规模（base）**  – 计算  `universe_size(universe)`  的平方根。这里的 universe_size 可能返回样本（比如股票池）的大小，取平方根起到平滑放大规模效应的作用，使得评分不会随着股票数目线性放大，而是适度调整。
- **综合得分（score）**  – 将上面三个因子相乘，以获得一个初步评分。
- **换手率过滤**  – 最后利用  `if_else(turnover > 0.33, nan, score)`  筛选：如果换手率超过 33%（可能代表交易过于频繁或信号风险较大），则不返回评分，而是返回 NaN，将该 α 排除在候选外。

类别2：Selection

```
"vol_factor = 1 / (abs(prod_correlation) + 0.001);\n""activity_bonus = if_else(author_activity >= 0.85, 1.3, 1);\n""score = vol_factor * activity_bonus * operator_count;\n""if_else(turnover >= 0.34, nan, score)",
```

- **波动性因子（vol_factor）**  – 这里利用反比关系：1 除以（绝对值的  `prod_correlation`  加上一个小常数 0.001）。当 α 与其他信号的相关性较低（绝对值较小）时，vol_factor 较大。这种设计鼓励低相关性、分散化的策略，同时加上一个极小的偏移值避免除零错误。
- **活跃度奖励（activity_bonus）**  – 根据作者的活跃度  `author_activity`  是否达到或超过 0.85，加一个 1.3 的系数，否则为 1。较高的提交频率或活跃度可能被视为对策略构造的持续优化与稳定性保证，因此给予额外奖励。
- **评分计算**  – 得分等于上述两个因子乘以  `operator_count` 。这里的  `operator_count`  反映了策略表达式中操作符的数量，通常用来衡量方法“复杂度”或包含的经济逻辑的丰富性。
- **换手率约束**  – 如果换手率大于或等于 34%，则返回 NaN，排除高换手率的策略，以控制交易成本和策略不稳定风险。

类别3：Selection

```
"bonus = if_else(author_sharpe >= 2.5 && author_sharpe <= 3.5, 1.2, 1);\n""score = operator_count * bonus;\n""if_else(turnover >= 0.35, nan, score)",
```

- **夏普比率奖励（bonus）**  – 利用  `if_else`  判断作者的夏普比率  `author_sharpe`  是否处于 2.5 到 3.5 的理想区间。如果在这个区间，则奖励系数为 1.2，否则系数为 1。通过这样的设计，平台鼓励构造在风险调整后收益表现最佳的策略。
- **评分计算**  – 得分直接是  `operator_count`  与 bonus 的乘积。这意味着策略在符合理想风险收益范围时，其复杂度（操作符数量）得以提升，从而在筛选时可能更受青睐。
- **换手率过滤**  – 设置换手率门槛 35%，超过这一门槛的策略将被视为风险或成本过高而被过滤掉。

类别4：Selection

```
"news_factor    = if_else(in(datacategories, 'news'), 1.4, 1);\n""neutral_factor = if_else(neutralization == 'SUBINDUSTRY', 1.2, 1);\n""bonus = if_else(author_sharpe >= 2.5 && author_sharpe <= 3.5, 1.2, 1);\n""score = news_factor * neutral_factor * bonus * operator_count;\n""if_else(turnover > 0.30, nan, score)",
```

- **新闻因子（news_factor）**  – 如果数据类别  `datacategories`  中包含  `'news'` ，则赋值 1.4，否则为 1。这暗示平台认为融入新闻信息的 α 可能抓住突发事件或市场情绪，从而赋予更高权重。
- **中性化因子（neutral_factor）**  – 判断是否采用了子行业（SUBINDUSTRY）水平的中性化。如果是，则给予 1.2 的加权，否则为 1。这样的处理有助于降低行业、板块效应，表明该策略风险管理更精细。
- **夏普奖励（bonus）**  – 同前面的表达式，如果作者的夏普比率处在 2.5 到 3.5 之间，则奖励 1.2，否则为 1。
- **综合评分计算**  – 将上述三个因子与  `operator_count` （表达式复杂度）相乘，得到最终得分。
- **换手率过滤**  – 当换手率大于 30%时，输出 NaN，从而排除换手过高、可能存在过多交易成本风险的策略。

类别5：Selection

```
"simplicity  = 1 / (operator_count + 1);\n""decay_bonus = if_else(decay < 1.5, 1.3, 1);\n""bonus = if_else(author_sharpe >= 2.5 && author_sharpe <= 3.5, 1.2, 1);\n""score = simplicity * decay_bonus * bonus;\n""if_else(turnover >= 0.30, nan, score)",
```

- **简洁度因子（simplicity）**  – 采用 1/(operator_count+1) 的方式，直接将表达式所用操作符数量转化为“简洁度分数”。操作符越少，即表达式越简洁，分数越高；这里的“+1”用于防止除零。简单往往意味着更容易解释和更低的过拟合风险。
- **衰减奖励（decay_bonus）**  – 根据  `decay`  值，如果小于 1.5则给予 1.3 的加乘，否则为 1。衰减较低可能代表信号持续性更好或噪音较少，这是积极的一面。
- **夏普比率奖励（bonus）**  – 同样地，如果作者的夏普比率位于最佳区间（2.5～3.5），则额外奖励 1.2，否则保持 1。
- **综合评分计算**  – 得分为上述三个因素的乘积，强调了“简洁性”与“信号稳定性”（衰减）以及风险调整后收益水平（夏普）的联合作用。
- **换手率过滤**  – 同样，如果换手率达到或超过 30%，则认为该 α 可能交易过于频繁，从而返回 NaN筛除之。

---

### 评论 #5 (作者: WL13229, 时间: 1 year ago)

楼上虽然AI味比较浓重，但还是有一定启发性，遂通过

---

### 评论 #6 (作者: JB71859, 时间: 1 year ago)

**Idea : 高质量低相关策略**

**Selection Expression:**

(self_correlation <= 0.5) * (prod_correlation < 0.4) * (turnover >= 0.1) * (turnover <= 0.3) * (long_count + short_count)

setting：

![图片](images/img_630564c892.png) 
最终结果： ![图片](images/img_41776ce032.png)

**解释** : 选择自相关性和生产相关性都较低，换手率适中，覆盖度高的Alpha。

---

### 评论 #7 (作者: PW58059, 时间: 1 year ago)

**Idea:观察自己表现好的regular alphas特性，选取对应特性的regular alphas并叠加生产相关性低的alphas获得多样性增益**

**类别：selection**

注意：selection数量仅为展示，具体数值应该视你所选特性alphas的数量而定，但不建议将该数量设置过低。

![图片](images/img_f5a7494045.png)

```
# 比如我自己的GLB regular alphas中，risk70这个数据集在TOP3000这个universe中表现都比较好：(in(datasets, "risk70") && universe=="TOP3000") # 如果想只选取自己的alphas做增益的化，也可以提前将alphas标好颜色，然后直接选取对应颜色，比如：color=="YELLOW" # 之后添加一些生产相关性低的alphas获取多样性增益，整体selection expression如下：(in(datasets, "risk70") && universe=="TOP3000") || (prod_correlation<0.4 && universe=="TOP3000" && turnover<0.15)  && not(own)
```

---

### 评论 #8 (作者: YB49779, 时间: 1 year ago)

**这是我SAC比赛提交的第一个因子**

**Idea:选择尽可能稳定的换手率区间内的优质因子**

**类别：selection**

**Setting： ![图片](images/img_ac719b5d41.png)**

**由于我是第一次在GM的池子中组SA，数量很多，所以我希望尽可能缩小搜索空间，示例中的区间仅为示例，我认为这个区间内的换手率较为稳定。**

# 我是G2组的只能选择simple alphas
# 操作符数小的，且被作者favorite相对更加稳定
# 低decay只是为了刨除那些为了过相关性测试盲目提高decay的劣质因子
# 最后由于我在TOP2500中做sa所以希望来自大的universe的因子占到更高权重
select:(!own&&in(classifications,'SIMPLE')&&turnover>0.08&&turnover<0.15&&operator_count<7&&favorite&&decay<6)*universe_size(universe)
combo:combo_a(alpha)

 ![图片](images/img_d96363f54f.png)  ![图片](images/img_467cc94a0c.png) 
 ![图片](images/img_bb8c0bf907.png) 解释：在提交时prod为0.43，最终base有55，帖子是在一天后写的，此时prod提升到了0.44

---

### 评论 #9 (作者: WL13229, 时间: 1 year ago)

[YB49779](/hc/en-us/profiles/26716038151319-YB49779)  能想到favorite这个idea是真的妙啊

---

### 评论 #10 (作者: PZ64174, 时间: 1 year ago)

**类别：selection**

*in(classifications, "SIMPLE") && not(own)&&(datafield_count<2)&&(operator_count<5)&&(datacategory_count<2)&&(neutralization=='COUNTRY')&&(long_count>500)&&(short_count>500)&&turnover<0.15*

**in(classifications, "SIMPLE")**  *#G2第一周selection池子*

**not(own)**  *#选择非自己的*

**datafield_count<2**  *#限制数据字段个数*

***operator_count<5***  *#限制ops个数，防止出现混信号以及复杂因子*

***datacategory_count<2***  *#限制data类型个数*  *，防止出现混信号以及复杂因子*

**neutralization=='COUNTRY'**  *#因为做的是ASI的，所以选的这个中性化（此中性化在多国家region有比较好的表现，eur也可以选用）*

**(long_count>500)&&(short_count>500)**  *#防止缺少数据的不稳定alpha*

***turnover<0.15***  *#限制换手率*

*注意：selection数量仅为展示，具体数值应该视你所选特性alphas的数量而定，但不建议将该数量设置过低。*

*******（不知道为啥我评论的时候没法放图片，只好口述下selection settings，region：ASI,***  *Selection Handling:Non-Nan,***  *Selection Limit:300***  ***）***

Sharpe 5.33 Turnover 7.97% Fitness 5.53  Returns 13.48% Drawdown 1.50% Margin 33.82‱

**Combo Expression**

**combo_a(alpha)**

---

### 评论 #11 (作者: WP88606, 时间: 1 year ago)

一种随机生成SuperAlpha，进行机器回测的方式，之前发的，可以混个笔记本吗？

[../FZ60707/[Commented] 一种随机生成 SuperAlpha进行机器回测的方式代码优化.md](../FZ60707/[Commented] 一种随机生成 SuperAlpha进行机器回测的方式代码优化.md)

---

### 评论 #12 (作者: MY27687, 时间: 1 year ago)

**类别：selection**

**Selection Expression：**

```
in(classifications, "SIMPLE")&& not(own)&&(in(datasets,'analyst4')+in(datasets,'analyst69')+in(datasets,'model110'))&&turnover<0.02
```

**setting： ![图片](images/img_351c656a11.png)**

**Idea:**

成为顾问后一直在做EUR，后来转战ASI 发现有些数据集信号在不同 Universe下 依然信号很好，所以用来super alpha的 **Selection Expression** 选取换手率turnover<0.02 ，analyst4 analyst69 以及model110的alpha进行组合，由于分配到了G2所以选取的alpha质量并不高。

结论：

![图片](images/img_7db99bfa52.png)

![图片](images/img_f121dbd628.png)

信号还可以，但是PC有点高

![图片](images/img_692cf66990.png)

---

### 评论 #13 (作者: KD86036, 时间: 1 year ago)

**类别：combo**

**idea:将市净率、市盈率等有经济学意义的概念迁移至SUPERALPHA 。**

**setting:和楼上大佬一样评论区加载不了图片，只好口述参数设置** EUR,TOP2500,DECAY:12,Neutralization:RAM,Selection Limit:100

**Combo Expression:**

**step1：基于alpha statistic生成有经济学意义的特征**

stats = generate_stats(alpha);  # 生成a各类lpha statistic

book_value=stats.pnl/stats.returns; #账面规模

cap=stats.trade_value+stats.hold_value; #市值

eps=stats.pnl/(stats.trade_shares+stats.hold_shares);#每股收益

price=cap/(stats.trade_shares+stats.hold_shares); #价格

book_value_per_share=book_value/(stats.trade_shares+stats.hold_shares);#每股账面价值

**step2：基于以上特征进一步构建PB、PE等有经济学意义的表达式**

PE(市盈率)=price/eps

PB(市净率)=price/book_value_per_share

**step3：将上述特征结合时间序列操作符进行回测会产生很不错的效果。**

注意：不要局限于常规时间序列操作符，可以与协方差，偏度，回归等时序操作符结合使用

Example：ts_co_skewness(eps,ts_delay(eps,20) , 252)>0

Result：Sharpe 5.51 Turnover 8.62% Fitness 6.56  Returns 17.74% Drawdown 3.69% Margin 41.16‱

self corr:0.5637,prod corr:0.5637

此处selection仅为参考，欢迎大家拓展：not(own)*(1-self_correlation)*(1-turnover)

---

### 评论 #14 (作者: ZL35633, 时间: 1 year ago)

分享一个selection表达式的格式：

每行写一个表达式，调试的时候可以注释整行不影响执行。

```
# 做bool判断的表达式写在这里，用来筛选需要的alphabool = (    not (own) &&    in(classifications, "POWER_POOL") &&    ( turnover>0.04 && turnover<0.30 ) &&    datacategory_count<=3 &&    short_count+long_count > 1000 &&    1);# 计算权重的表达式写在这里weight = (    1    *(prod_correlation)    *abs(self_correlation-0.5)    *(1-turnover));bool * weight
```

在PPAC中，pc值大的可能是顾问挑选的历史表现好的alpha

![图片](images/img_7014d1a605.png)

![图片](images/img_bb756636a0.png)

---

### 评论 #15 (作者: WL13229, 时间: 1 year ago)

[【SuperAlpha灵感】因子择时模型 – WorldQuant BRAIN](../JL16510/[Commented] 【SuperAlpha灵感】因子择时模型Alpha Template.md)   [YW93864](/hc/en-us/profiles/14096946892439-YW93864)

---

### 评论 #16 (作者: WH24469, 时间: 1 year ago)

类别：SELECTION

（无法上传图片）

settings：GLB，1， positive， 50

Idea:

1.有color或者有category的alpha，说明alpha有其特殊之处，要不很好要不很差，从中选出好的。

2.添加一个prod corr范围来限制过拟合的alpha。

3.os_start_date比较新的说明alpha没有面临失效风险的（这一part也考虑过最近几年performance的，有兴趣的朋友可以自行探索）。

```
in(classifications, "POWER_POOL") &&prod_correlation < 0.5 && prod_correlation > 0.1 &&color != "NONE" &&category != "NONE" &&os_start_date >= "2022-01-01"
```

IS performance:

sharpe : 8.01

turnover : 10.32%

fitness7.28

returns : 10.32%

drawdown : 0.80%

margin : 20.01

已经提交了一个SA了，所以PC会比较高。

补充说明：pc > 0.1是因为power pool中有些author会提交很差的alpha，这些alpha呈现厂或者只有近几年的数据，但凡整体走势是向上的都会导致指标非常好看，pc也比较低，所以我想剔除掉这些“要不很差”的alpha。

另外就是本来有color和有category且2022年后开始os的alpha个人认为已经比较“稀有”了，且现在consultant越来越多，造出来pc低于0.1的且优秀的alpha难度比较大，所以我选择规避掉这部分风险。

最主要还是剔除尾部风险

---

### 评论 #17 (作者: WL13229, 时间: 1 year ago)

[WH24469](/hc/en-us/profiles/13991511763607-WH24469)  请补充阐述 以下选择的原因

```
prod_correlation > 0.1
```

---

### 评论 #18 (作者: WH24469, 时间: 1 year ago)

pc > 0.1是因为power pool中有些author会提交很差的alpha，这些alpha呈现厂或者只有近几年的数据，但凡整体走势是向上的都会导致指标非常好看，pc也比较低，所以我想剔除掉这些“要不很差”的alpha。

另外就是本来有color和有category且2022年后开始os的alpha个人认为已经比较“稀有”了，且现在consultant越来越多，造出来pc低于0.1的且优秀的alpha难度比较大，所以我选择规避掉这部分风险。

最主要还是剔除尾部风险

---

### 评论 #19 (作者: JL40454, 时间: 1 year ago)

User-selected-ntr思路:

Selection的结构简而言之为条件+评分, 在此只阐述条件思路.

选取提交者心中特殊的alpha, 比如颜色, 星标, tag等, 通过对规定域中的人工标签选出被特殊关照的alpha:

- color ==/!= <COLOR>: 颜色筛选;
- favorite/not(favorite): 是否星标;
- tag ==/!= <TAG>: 不太好选, 建议使用AI创建tag池进行选取测试;
- neutralization ==/!= <NEUTRALIZATION>: 剔除不经思考的machine alpha，如果他的neutralization不是machine alpha的默认设置，默认他经过了鲁棒性检测，也属于被用户特殊关照的一类，但是有可能默认设置的值不一定是NONE，或许常用的一些其他neutralization选项也可以加入不等于的条件;
- category ==/!= <CATEGORY>: 是否选择类别;

示例如下, score可随意修改:

> is_special = favorite || color!= "NONE" || neutralization != "NONE" || category != "NONE";
> other_condition = os_start_date > "2024-01-01" && operator_count<7 && dataset_count ==1;
> condition = is_special && other_condition;
> score =(1-prod_correlation)*(1-self_correlation)/turnover;
> if_else(condition, score, nan)

设置:

> "settings":{
> "nanHandling":"OFF",
> "instrumentType":"EQUITY",
> "delay": 1,
> "universe": "TOP3000",
> "truncation": 0.01,
> "unitHandling":"VERIFY",
> "selectionLimit": 250,
> "selectionHandling": "POSITIVE",
> "pasteurization":"ON",
> "region": "USA",
> "language":"FASTEXPR",
> "decay": 5,
> "neutralization": "NONE",
> "visualization": False,
> "testPeriod":"P0Y",
> 'maxTrade': "ON"
> }

---

### 评论 #20 (作者: WL13229, 时间: 1 year ago)

[JL40454](/hc/en-us/profiles/28831795834263-JL40454)

neutralization != "NONE"

这个估计不太好，可以考虑删除，您觉得呢

---

### 评论 #21 (作者: LW49759, 时间: 1 year ago)

### 类别：selection

### 表达式：

```
(not(own)&&(in(classifications,'POWER_POOL'))&&((turnover<0.29&&turnover>0.27)||(turnover<0.25&&turnover>0.23)||(turnover<0.20&&turnover>0.17)||(turnover<0.14&&turnover>0.11)||(turnover<0.09&&turnover>0.05)||(turnover<0.04&&turnover>0.02))&&(operator_count<8)&&(prod_correlation<0.6&&prod_correlation>0.2)&&(dataset_count<=2)&&(long_count>300)&&((neutralization=='SLOW')||(neutralization=='FAST')||(neutralization=='SLOW_AND_FAST')))/(turnover*tanh(turnover)*sigmoid(self_correlation)*sigmoid(prod_correlation))
```

### idea：

选取SLOW，FAST和SLOW_AND_FAST的Neutralization，settings选择SLOW_AND_FAST，记得之前老师说过风险中性化的表现会更加稳健，在此基础上再使用风险中性化，可能会提高稳健性，除了上面三个还可以选择CROWDING，STATISTICAL等分别尝试

selection其他说明：

- turnover分片选择使得每次选到的alpha尽可能不一样
- operator_count和dataset_count使得信号尽量纯粹
- prod_correlation>0.2可以规避一些pnl很奇怪的因子
- 除法后面的权重计算是参考的游戏王的帖子，按照turnover进行加权，按照correlation进行加权，sigmoid是为了防止权重变化过大

### settings：

![图片](images/img_a4ea6d1240.png)

（实际选到了97个）

### 表现：

![图片](images/img_db0b3b39e4.png)

![图片](images/img_f6cdd687cb.png)

![图片](images/img_15fd0d0344.png)

---

### 评论 #22 (作者: CH62432, 时间: 1 year ago)

**类别:Selection;**

**Idea:**

> **中心思想是优先挑选 **信号方向性强且表达式简洁的alpha;****
> ****其余的操作 :数据类型、换手率的限制等等...,通过这些操作来强化中心思想选中alpha****

**Selection Expresson:**

```
abs_score = if_else(abs(long_count - short_count) > 1000, 1.5, 0.5);op_score = if_else(operator_count <= 5, 1.5, 0.5);final_score = (abs_score * op_score) * (in(classifications, 'POWER_POOL') && !own) * (in(datacategories, "analyst") + in(datacategories, "socialmedia") + in(datacategories, "sentiment")) *(turnover < 0.2);final_score;
```

Settings:

![图片](images/img_0d652060f8.png)

**表现**

![图片](images/img_953766092e.png)

![图片](images/img_d4e808cd0c.png)

---

### 评论 #23 (作者: LZ14530, 时间: 1 year ago)

Idea: 在G4组power pool，对上面的SELECTION Idea做了许多尝试，发现选择的alpha中，returns的高低跟alpha质量高低有一定的正相关，期望基于年波动率，给returns高的alpha做高权重

类别：Combo

（无法上传图片）

Setting:

> Region: USA, Delay: 1, Positive: 40;
> Universe: TOP3000,  Neutralization: Subindustry,  Decay: 6,  Truncation: 0.08,  Pasteurization: ON,  Unit Handling: Verify,  Nan Handling: ON,  MaxTrade: OFF

Combo Expression:

```
stats=generate_stats(alpha);ts_std_dev(stats.returns,252)/1
```

测试了多个selection，此combo在margin上优于equal weight

---

### 评论 #24 (作者: WL13229, 时间: 1 year ago)

[LW49759](/hc/en-us/profiles/26717472313751-LW49759)

可否阐释一下tanh和sigmoid的作用，以及它们对Alpha筛选分的影响

---

### 评论 #25 (作者: WX84677, 时间: 1 year ago)

【思路】：基于os 表现好 regular alpha (以下简称 ra) 的特征，构建 select 表达式。

已知满足以下条件的 ra , os 表现大概率较好：

1. returns > turnover;
2. returns > drawndown;
3. PNL 数据完整
4. long_count 与 short_count 接近（多空平衡）
5. long_count、short_count 较大（覆盖面广）
6. 表达式简单，字段较少（避免过拟合，例如 PPA、ATOM）
7. turnover 低于 10% （防止计算交易手续费后亏钱）
8. alpha 在不同 neutralization

第3~7点基本可以通过 select 语句表达，第8点通过同表达式回测所有 neutralizition 来判断（不同 neutralizition PNL 走势及 sa 的六维参数相近）

select 表达式如下：

```
#  sac 主题池，属于主题的得分 1，否则得分 0.theme_score = in(classifications, "POWER_POOL");# dataset_count 挑出 dataset_count 小于等于 2 的，dataset_count 越小得分约高dataset_score = (dataset_count <= 2)*-dataset_count;# turnover 挑选 [2%~10%] 的tvr_score = (turnover >= 0.02 && turnover <= 0.1);# pnlpnl_score = (long_count >= 1000 && short_count >= 1000) * -abs(long_count-short_count) * (long_count+short_count);select_score = theme_score*dataset_score*tvr_score*pc_score*pnl_score;select_score
```

希望对各位有帮助，祝大家在 sac 中取得好成绩。

---

### 评论 #26 (作者: AK76468, 时间: 1 year ago)

![图片](images/img_b9e35158ef.png)

## 假设：

- SIMPLE POOL中的alpha是去除噪音的alpha，每个alpha只保留其有价值的部分。
- 在SIMPLE池中，如果一个alpha的运算符和字段数量超出常规，那么认为这个alpha是作者带有目的实现的Human alpha，具有经济学含义。
- 在SIMPLE池中，如果一个alpha仅有一个运算符和字段，那么认为这个字段本身就具有极强的经济学含义。

## 发现：

> 池内绝大部分的alpha的op数量在 [ 1, 8 ]，绝大部分的alpha的datafield数量在[ 1, 3 ]

## **idea：将极简alpha和复杂alpha组合**

### 类别：Selection

```
(in(classifications,'SIMPLE')&&operator_count<30&&operator_count>10&&//选取运算符介于[10,30]的alphadatafield_count>4&&//选取使用字段大于4的alpha(universe_size(universe)*0.3<long_count&&universe_size(universe)*0.3<short_count)&&//选取多空平衡的alpha，增强可信度os_start_date<"2023-07-01")//选取一定的OS范围，增强可信度+(in(classifications,'SIMPLE')&&operator_count==1&&dataset_count==1&&//选取极简alpha(universe_size(universe)*0.3<long_count&&universe_size(universe)*0.3<short_count)&&os_start_date<"2023-07-01")
```

> *alpha数量=78*

#### combo

> 减弱极简alpha中的相似性，按照相关性分配权重

```
stats =generate_stats(alpha);innerCorr =self_corr(stats.returns,500);ic =if_else(innerCorr >0.8, nan, innerCorr);maxCorr =reduce_max(ic);1 - maxCorr
```

![图片](images/img_5aeb989106.png)

---

### 评论 #27 (作者: WL13229, 时间: 1 year ago)

[AK76468](/hc/en-us/profiles/28846915371031-AK76468)

请阐述一下设置os start date的原因及具体参数由来

---

### 评论 #28 (作者: AK76468, 时间: 1 year ago)

设置os start date可以选取特定时间范围的alpha，我了解到在2023年第三季度时有ACE的比赛，这时顾问们开始广泛使用接口machine alpha。那么假设在此之前，human alpha的占比会比现在多，手工混信号要比机器混信号成本更高，所以op数量多的alpha更可能是有经验顾问手搓出来的，而不是machine混信号出来的，就增大了selection的可信度

> 如果一个alpha的运算符和字段数量超出常规，那么认为这个alpha是作者带有目的实现的Human alpha，具有经济学含义。

---

### 评论 #29 (作者: LX31898, 时间: 1 year ago)

KD86036

有关公式ts_co_skewness(eps , ts_delay(eps , 20) , 252)>0：

我是刚解锁superalpha的有条件顾问，然而在复现大佬的idea过程中发现我并没有ts_co_skewness这个操作符。问了一下deepseek有什么替代的表达式，它给了如下两种替换方法，数学功底好的大佬帮我看看这么替换有没有道理：

方法1：用协方差和矩操作符组合实现
协偏度本质是联合三阶矩，可通过以下操作符组合实现：
X = (eps - ts_mean(eps, 252)) ** 2;  # X的平方偏差
Y = ts_delay(eps, 20) - ts_mean(ts_delay(eps, 20), 252);  # Y的中心化
co_skew = ts_covariance(X, Y, 252);  # 协方差代替联合矩
co_skew > 0

方法2：用回归残差实现（更稳定）
通过线性回归分离非线性依赖，捕捉偏度特征：
# 步骤1: 对Y = ts_delay(eps, 20) 做线性回归
residual = ts_residual(Y, X_linear, 252);  # 残差包含非线性信息
# 步骤2: 计算残差与X平方的协方差
co_skew = ts_covariance(X ** 2, residual, 252);
co_skew > 0
其中 X_linear 可包含线性因子如：
X_linear = ts_mean(eps, 252) || ts_delta(eps, 1) || ... ;  # 拼接线性特征

(ts_residual可用ts_regression替代)

---

### 评论 #30 (作者: KL64183, 时间: 1 year ago)

```
d1 = if_else(color != "NONE", 1, 0);d2 = if_else(category != "NONE", 1, 0);d3 = if_else(!in(datacategories, "model"), if_else(!in(datacategories, "fundamental"), 1, 0.5),0);d4  = if_else(turnover >= 0.5, 0.5, if_else(turnover >= 0.3, 1, if_else(turnover >= 0.1, 0.5, 1)));f1 = sigmoid(turnover/datafield_count);f2 = sigmoid(turnover/operator_count+1);f3 = sigmoid(1/log(abs(long_count-short_count)/universe_size(universe)));in(classifications, "SIMPLE")*(3*(f1+f2)+6*f3+(d1+d2+d3+d4))/16
```

1. **離散指標 (d1 ~ d4)**
   - **d1** ：檢查  `color`  是否為 “NONE”，若不是則 d1=1，否則為 0。
   > 目的：篩選出使用者標註的顏色特徵(alpha)，代表作者在該 alpha 構建上投入較多心力。
   - **d2** ：檢查  `category`  是否為 “NONE”，若不是則 d2=1，否則為 0。
   > 目的：同上述，確保納入使用者手動標籤的分類標籤(alpha)。
   - **d3** ：根據  `datacategories`  給予權重：
   - 若不屬於 “model” 也不屬於 “fundamental”，d3=1（最高權重）；
   - 若屬於 “fundamental” 且不屬於 “model”，d3=0.5（中等權重）；
   - 若屬於 “model”，d3=0（最低權重）。
   > 目的：減少純模型資料的比重、避免基本面資料過度集中，提升資料類別多樣性。
   - **d4** ：根據  `turnover` （換手率）的區間進行分段賦值：
   - ≥ 0.5 → 0.5（高換手率降低利潤率）；
   - [0.3, 0.5) → 1（中度穩定區間）；
   - [0.1, 0.3) → 0.5；
   - [0, 0.1) → 1（低換手率也納入多樣性考量）。
   > 目的：在不同換手率區間中平衡選取高、中、低換手率的 alpha 池。
2. **連續函數 (f1 ~ f3)**
   - **f1 = sigmoid(turnover / datafield_count)**
   > 衡量每個資料欄位平均帶來的換手率大小，高值代表該欄位資訊量較豐富。
   - **f2 = sigmoid(turnover / (operator_count + 1))**
   > 衡量所用運算子效率，運算子越多則分母越大，相對降低效果。
   - **f3 = sigmoid( 1 / log( |long_count − short_count| / universe_size ) )**
   > 評估多空部位分佈的均衡程度；以對數降低敏感度，再取倒數並映射至 (0,1)。
3. **最終分數組合**
   ```
   score =
   in(classifications, "SIMPLE")
   * ( 3*(f1 + f2) + 6*f3 + (d1 + d2 + d3 + d4) ) / 16
   ```
   - 只有當  `classifications`  包含  `"SIMPLE"`  時才計算分數。
   - 將 f1、f2 的合計乘以 3，f3 乘以 6，離散指標之和與之相加後，以 16 為總權重正規化。
   - 選擇 f3 加權 6（優於 3）顯示多空均衡的 alpha 效果更佳；整體採用等權正規化以保持簡潔。

透過上述設計，該邏輯旨在：

- 優先篩選出經作者精心標註的 alpha；
- 平衡不同資料類別與換手率特性；
- 強調多空部位均衡性；
- 並在「SIMPLE」分類下統合所有指標，生成最終分數。

![图片](images/img_61a858becc.png)

![图片](images/img_bc4e7f65b7.png)

![图片](images/img_816e0ee57e.png)

---

### 评论 #31 (作者: WL13229, 时间: 1 year ago)

[LW49759](/hc/en-us/profiles/26717472313751-LW49759)

```
((turnover<0.29&&turnover>0.27)||(turnover<0.25&&turnover>0.23)||(turnover<0.20&&turnover>0.17)||(turnover<0.14&&turnover>0.11)||(turnover<0.09&&turnover>0.05)||(turnover<0.04&&turnover>0.02))
```

请思考一下这个条件，如果你分得再细一些，基本可能所有turnover的Alpha都会被选中，是不是跟删掉它差不多呢

---

### 评论 #32 (作者: YX23928, 时间: 1 year ago)

由于无法上传图片的原因，setting/selection/combo均以文字形式展示：

SETTING：

Region:EUR,Universe:TOP2500,Decay:0,Neutralization:RAM,Max Trade:Off

Selected Alphas：300

#选择新的Neutralization，避免高相关性问题

Selection Expression:

(!own&&in(classifications,'SIMPLE')&&turnover>0.05&&turnover<0.10&&operator_count<8&&decay<10)*universe_size(universe)*(long_count + short_count)

#选择低turnover，低operator_count且(long_count + short_count)较多的alpha

Combo :

stats = generate_stats(alpha);std = ts_std_dev(stats.returns,60);std_crowd = std /ts_delay(std,60);ts_rank(-std_crowd ,500)

#选用YW93864大佬因子择时模型，可减缓因等权选取因子衰减问题

Sharpe:6.48;Turnover:14.89%;Fitness:6.78;Returns:16.29%;Drawdown:1.94%;Margin:21.87‱;

prod correlation:0.64

---

### 评论 #33 (作者: KZ79256, 时间: 1 year ago)

SETTING：

![图片](images/img_7832439340.png)

SELCTIONS:

(in(classifications, "SIMPLE"))*(in(datacategories, "pv"))

上限设的1000，只有764个因子符合

COMBO:

w1 = combo_a(alpha, nlength = 40, mode = 'algo1');

w2 = combo_a(alpha, nlength = 160, mode = 'algo1');

w3 = combo_a(alpha, nlength = 252, mode = 'algo1');

scale(w1) + scale(w2) + scale(w3)

----

selection的原因，本身selection比较长，之后由于选不到1000个因子，就等效于上述selection

主要是为了选择和量价相关的因子

combo的方法设计的原理用于考虑短时combo_a的权重和长时combo_a的组合，借鉴了两个方面

- 之前SA培训的时候把不同的algo进行综合的方式
- 机器学习提取特征时通常会考虑不同时长的特征，来捕捉相应的信息

如果直接用combo_a(alpha, nlength = 250, mode = 'algo1')的结果如下

![图片](images/img_1edb57ab15.png)

用考虑了短时combo_a的权重和长时combo_a的组合的结果如下（0.89是因为我交了一个在此基础上降corr的因子导致的，原始应为0.53左右

![图片](images/img_37b394fb95.png)

我在此基础上用了signed_power(scale(w1) + scale(w2) + scale(w3),2)，来降低corr，降到了0.47

看来新combo比原来只有一点点提升，区别不大2333 =_=!!, 应该是eur数据的simple类的因子本身是基于eur Top1200, 放在了TOP2500导致的

---

### 评论 #34 (作者: LH44620, 时间: 1 year ago)

分享几个combination，经过我回测了各种各样的池子，表现较好的。

1.

```
combo_a(alpha, nlength = 255, mode = 'algo1')+Neutralization选择Statistical
```

虽然combo_a操作符是大家常用的组合superAlpha的选择。可是经过一些回测，我发现combo_a配合上Statistical会有更好的表现。我的池子是g2的simple，所以指标可能没有那么高。这个选择我测试了多个地区，感觉都是成立的。并且corr也较低。

![图片](images/img_8dd6230c0a.png)  ![图片](images/img_26e1455eca.png)

2.

```
combo_a(normalize(alpha), nlength =250, mode = 'algo1')
```

在combo_A的基础上加上normalize(x)操作符。这种用法是在看到wq的sa英文课程时，看到了类似的用法。于是我就想能不能先标准化一下再进行combo_A呢？结果还不错。corr也比较低。池子依然是g2的simple。这个选择我测试了多个地区，感觉也都是成立的。
 ![图片](images/img_f1ba620ac5.png)

![图片](images/img_58b32ecdc9.png)

![图片](images/img_3629eee563.png) 可以看到后期pnl表现超过等权了。

3.

```
x = generate_stats(alpha);ts_co_kurtosis(x.drawdown, x.returns, 215)
```

目的是看极端回撤和极端收益是否共振，判断收益波动性风险。 若cokurtosis很高，说明策略在回撤时也容易出现极端收益波动（高风险区域）。池子是g2的simple。选了200个的GLB，corr较低。这个选择我测试了多个地区，感觉也都是成立的。

![图片](images/img_f58514d66f.png)

![图片](images/img_bb30f71ebe.png)

![图片](images/img_144594e5c0.png)

---

### 评论 #35 (作者: YW93864, 时间: 1 year ago)

本周的SAC暂告一小节，share一下我这周在比赛中做的一些工作，可能有启发意义。后文中，我们假设我们筛选和组成的SA是最大化margin的。需要注意的是，本文用到了一些统计手段，所得出来的结论是模型依赖的，意味着有过拟合的风险，我们在最大化margin和过拟合中做权衡，tradeoff。

**1. 首先是selection，要设定一个基础的筛选标准**

```
cond = (in(classifications,"SIMPLE")&&operator_count<=8&&turnover<=0.5&&datacategory_count<=2&&abs(long_count-short_count)<=500&&not(own));
```

**以下是每一行的逻辑：**

1. 第一行代表我在G2
2. 第二行代表我希望operator_count<=8，不希望太长的operator。太长的很容易没逻辑，选到overfitting的alpha概率就提升了
3. 第三行是对turnover的限制，高turnover低turnover都需要有，所以不能限制太低的turnover，不然大部分alpha可能都是fundamental/analyst或者其他更新频率很低的类型；同时我不希望turnover太高，虽然平时的提交标准是70%，但我们可以适当把阈值拉紧一些。
4. datacategory<=2是希望不要混信号
5. abs(long_count-short_count)<=500，是希望alpha的两头在合理的范围内平衡，允许有一点差异
6. not(own)加不加都可以

**2. 通过统计的方法筛选出哪些datacategory的alpha可能本身就很有用。**

具体来说，我对四个region，将每一个datacategory下的alpha提取出来，为了简单起见，我们就先使用1/ turnover在每一类alpha中选出得分最高的1000个（换手率最小的1000个alpha）。具体的代码可以中群里面或者自己F12调试网页找到。

接着，我们做一些统计。一方面观测各个类型的数据集之间，哪一类数据集的margin更高；一方面观测特定类型的数据集中，哪些变量对margin最有影响，比如turnover，operatorCount，universe_size等等。实际上从select这一步能提取出来的alpha也有限，获取到的信息也很少，仅限turnover，operatorCount，long，short四个信息（我在G2，有一些信息比如neutralization，就无法有效使用）。

**首先展示某个region我能拉到的alpha的绩效（很奇怪，api拉出来的和网页端数量不一致，部分差的蛮多，可能是我的程序有bug，但不影响思路）**

**![图片](images/img_a34c282a04.png)**

假设我们这里拉出来的alpha数量都是正确的。我们想要maximize margin，最简单那我们可以选某个margin以上的类别用来组SA，我们这里假设就选用初analyst以外的alpha。

**接着，我们优中选优，假设我们希望在400个alpha中选200个。一个方法是对这400个alpha用一个大一统的指标去筛选，另一个方法是每一类中，单独选出效果最好的n个alpha组合。**

那我们很容易想到对每一类的alpha做一些统计，寻找什么变量对margin影响最高，对每一类alpha设计一个独特的指标进行筛选。

![图片](images/img_344043115f.png)

比如这里就是某个region某个datacategory的分析图。可以发现这里三类指标都和margin有一定线性关系，那我们可以从这三个角度上设计一些独特指标，在每一类alpha中单独打分。 **需要注意的是该分数要能拉开区分度，不同指标之间需要保持量纲差异较小，这样才能做到可比性和筛选性。**

**3. 指标设计**

我们这里就先设计一个大一统的指标。这里给出一个demo，参考群里面老师的思路：怎样选出不是拉大decay降低turnover的alpha，我的思路是1. 高turnover高decay这样的双高alpha肯定要惩罚的；2. 双低的alpha，说明这样的alpha天然就很低turnover；3. 适中的turnover with 适中的decay，这些可以适中的获取。以下是我设计的v1.0函数

![图片](images/img_cb4bf8d890.png)

具体公式是：(1-sigmoid(T/tau))*(1+tanh(D-decay)/s),tau=0.1,D=10,s=3，tau是默认换手率，认为多少的换手率可以作为一个基准值，高了就惩罚，低了就奖励；D是默认decay，逻辑和前面基本一致；s是敏感性系数，是一个可以调的超参数，这个可以控制decay给多少惩罚。最后这个函数值在0-1之间

**后续优化思路：1. 还可以加入operatorCount作为第三个参数去model；2. 这个函数如果是decay和turnover都适中得分最高，应该更优，因为过双低alpha也可能是字段本身带来的，单独的字段更容易导致alpha表现衰减，所以后续加入更多参数应该会得到更好的alpha**

**4. combo**

这里参考 [KZ79256](/hc/en-us/profiles/13609593802263-KZ79256) 大佬的combo，其实是随机森林的思想，把弱学习器集成起来，得到更稳健的效果。

![图片](images/img_27f4f7d3d5.png)

---

### 评论 #36 (作者: MZ54236, 时间: 1 year ago)

对于G2，这种抵抗性挑选，算不算过拟合呢。

我的想法是既然别人的alpha看不到，那就参考自己的alpha，找sharpe衰减不严重的alpha，整体pnl没有大drawdown的alpha。

挑选范围可以稍微大一点，包括不同universe，不同中性化。找到这些自己的alpha以后，再用其数据集和相关指标做select筛选条件。

select筛选的时候适当的放大条件，避免反反复复就挑到那么几个。

```
md125 = (not(own) && in(classifications, "SIMPLE") && decay <= 10&& (turnover > 0.03 && turnover < 0.07) && in(datasets,'model25'));risk70 =(not(own)&&in(classifications,"SIMPLE")&& decay <= 15 && (turnover > 0.09 && turnover < 0.21) && in(datasets,'risk70'));analyst4 = (not(own) && in(classifications, "SIMPLE") && decay <= 15&& (turnover > 0.07 && turnover < 0.18) && in(datasets,'analyst4')) ;analyst7 = (not(own) && in(classifications, "SIMPLE") && decay <= 6&& (turnover > 0.08 && turnover < 0.11) && in(datasets,'analyst7'));pv13 =(not(own)&&in(classifications,"SIMPLE")&& decay <= 10 && ( turnover < 0.2) && in(datasets,'pv13'));(md125 + risk70 + analyst4 + analyst7 + pv13)*universe_size(universe)
```

以上就是我挑选的几个数据集例子。

Setting，region我选的是USA，因为EUR只能选到Top1200，表现一般，

唯一需要注意的是 Selection Limit，你需要测试每个data set能获得的alpha数量，然后设置一个大于所选总量alpha的limit，避免一个data就把选择池占满。

其余按照操作RA的方式适当调整即可。

---

### 评论 #37 (作者: JR23144, 时间: 1 year ago)

这是我提交的第一个可以参加 SA 比赛的alpha
Idea核心思想： **“精粹非基本面 & 极致内部异质性”加权策略** 
本策略首先通过Selection明确排除基本面（Fundamental）类别的Alpha，专注于挖掘其他类型的信号源，并初步筛选出自身相关性较低的Alpha。随后，在Combo阶段，并非采用简单的等权重或基于生产相关性（prod_correlation）的加权，而是通过计算已选Alpha池内部两两收益率的相关性，动态地为那些与池内其他Alpha“最不相似”（即与最相似那个Alpha的相关性也依然较低）的Alpha赋予更高权重，以追求极致的内部异质性和分散效果。

Selection Expression

```
not(in(datacategories, "fundamental")) * (1-self_correlation)
```

明确剔除所有数据类别包含 "fundamental" 的Alpha。这可能是为了避免某些拥挤的基本面因子，或者专注于挖掘市场微观结构、量价、另类数据等其他来源的Alpha。对剩余Alpha进行打分，self_correlation 越低的Alpha得分越高，意味着优先选择那些自身历史表现不那么“内部一致”（可能代表信号更稳定或适应性更强，而非依赖单一短期模式）的Alpha

Combo Expression

```
stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr
```

1. stats = generate_stats(alpha): 获取Selection阶段选出的所有Alpha的详细统计数据。
2. innerCorr = self_corr(stats.returns, 500): 计算这些已选Alpha的日收益率（stats.returns）之间，过去500个交易日的两两相关系数矩阵。
3. ic = if_else(innerCorr == 1.0, nan, innerCorr): 在相关系数矩阵中，每个Alpha自身与自身的相关性为1.0。为了在下一步正确找到与其他Alpha的最大相关性，将这些对角线上的1.0替换为nan (Not a Number)，使其在reduce_max中被忽略。
4. maxCorr = reduce_max(ic): 对于每一个Alpha，在处理过的相关性矩阵（ic）的对应行/列中，找到它与其他所有Alpha收益率相关性的最大值。这个maxCorr代表了该Alpha与它在当前已选池中“最相似的那个伙伴”的相似程度。
5. 1 - maxCorr: 这是最终的权重分配逻辑。一个Alpha的maxCorr值越低（意味着它即便与池中最相似的Alpha相比，其相似度依然不高），那么1 - maxCorr的值就越大，该Alpha获得的权重也就越高。本质上是 **奖励那些在当前组合中最具独特性的Alpha** 。
   ![图片](images/img_7094f5e330.png)  ![图片](images/img_426f1d41b1.png)

![图片](images/img_283a6402e5.png)

这种策略旨在构建一个不仅整体表现优异，而且内部各个组成部分之间也高度分散的SuperAlpha。理论上，这能带来更强的鲁棒性，尤其是在市场发生结构性变化或某些共性因子失效时，组合的整体回撤有望得到更好的控制，从而可能实现更高的风险调整后收益.

---

### 评论 #38 (作者: HW93328, 时间: 1 year ago)

在社区投稿了一篇用代码自动回测super alpha的帖子，功能包括随机生成selection表达式，与自定义combo表达式组合进行不间断的super alpha回测，可自定义limit、地区、中心化等选项。希望对各位有帮助。

[Super alpha全自动回测代码--开箱即用！ – WorldQuant BRAIN](../JX79797/[Commented] Super alpha全自动回测代码--开箱即用代码优化.md)

---

### 评论 #39 (作者: XY91783, 时间: 1 year ago)

## **idea：使用datacategories来选取分散的alpha，同时依据dataset的质量进行select分数的加权**

### 类别：Selection

在选取alpha时，我主要考虑的是alpha的分散性，即alpha之间的corr尽可能低。

为了实现这个目的，通过选择不同数据集的alpha来保证alpha的分散性，同时由于不同数据集产生的alpha质量参差不齐，所以在分散性原则的基础上，尽量选择质量好的alpha。

在我的理解中基本面的数据质量最高，所以在分配权重时，按照了下面的原则：

```
Fundamental  > Analyst > News > PV > Model
```

在权重考量时，参考了之前有同学分享的具有 favorite 属性的alpha质量更高，所以加入了这个部分

```
bool = (    in(competitions, "HCAC2025") &&            prod_correlation > 0.1  &&    os_start_date >= "2022-01-01");category_fund = in(datacategories, "fundamental") * 0.5;category_anal = in(datacategories, "analyst") * 0.4;category_news = in(datacategories, "news") * 0.3;category_pv = in(datacategories, "pv") * 0.2;category_model = in(datacategories, "model") * 0.1;weight = (    1        * if_else(favorite, 2, 1));first = bool * weight;first*category_anal + first*category_fund + first*category_news + first*category_model + first*category_pv
```

参数设置

 ![图片](images/img_2a2396e506.png)

参数设置时，要注意Selection Limit的设置，数值太大会导致选取的alpha和selection的代码关联太小（全都选了，就没有select的意义了），数值太小的话可能会导致performance低，我一般选择是在100~200之间，根据能选择的alpha数量上限来调整

performance的表现

![图片](images/img_d3bba76118.png)

![图片](images/img_eca241974a.png)

---

### 评论 #40 (作者: WL13229, 时间: 1 year ago)

[XY91783](/hc/en-us/profiles/30270229238807-XY91783)

请注意计算，有时候这样打分只是一厢情愿。如果fundamental的alpha很多，那么就会有很多alpha都有高分，例如有100个fundamental alpha都有高分，那么你的limit低于100，就无法选到其他的categories

---

### 评论 #41 (作者: MG88592, 时间: 1 year ago)

**为了让相关性更低可以使用以下这些参数分成不同的层级，去筛选完全不一样的因子。** 
 **也可以取部分交集，自我微调。选择其中的一个叠加相同的条件就可以筛选出完全不一样的因子，在遍历neut 找到最低的pc 然后继续微调。**

- **selection：**
- 0.01<turnover<0.05
- 0.05<turnover<0.1
- 0.1<turnover<0.15
- ....
- 0.1<prod_corr<0.4
- 0.4<prod_corr<0.45
- 0.45<prod_corr<0.5
- ...
- ....
- op_count<3
- 3<op_count<5
- 5<op_count<8
- ....

---

### 评论 #42 (作者: XC66172, 时间: 1 year ago)

**Idea:** 我是用代码跑super alpha，首先先通过run selection确认哪些字段会选出不一样的alpha(有些字段例如说author_sharpe在simple alpha就不起作用）,在代码方面写出多种组合。例如对所有SA, **(in(datacategories, "xxx")** 都是有效的，写出不同数量的多种组合 **(in(datacategories, "xxx")||in(datacategories, "xxx").** 同理，其他字段也可以设置不同的阈值，((long_count+short_count)>(universe_size(universe)*xx))

**注意事项：** 因为最终的combination太多，必须要用random来随机跑，按顺序跑就会出来结果都高度雷同的。

**类别：Selection:**

```
not(own) && ((neutralization == "SLOW") || (neutralization == "SLOW_AND_FAST") || (neutralization == "CROWDING") || (neutralization == "STATISTICAL") || (neutralization == "REVERSION_AND_MOMENTUM")) && (1-prod_correlation) && (in(datacategories, "macro")||in(datacategories, "news")||in(datacategories, "sentiment")||in(datacategories, "socialmedia")) && ((long_count+short_count)>(universe_size(universe)*0.8))
```

![图片](images/img_9cd5704f0e.png)

![图片](images/img_dd89097df3.png)

我是四个区混在一起随机跑的，一共需要跑3500万次回测，所以必须要随机跑。如果放在云主机上跑，因为只有两核有时候还会有memory issue,这时候只能降低变体数量从而降低总体回测数。

---

### 评论 #43 (作者: WL13229, 时间: 1 year ago)

[XC66172](/hc/en-us/profiles/28880767093655-XC66172)  这个搜索空间太大了，不太合理

---

### 评论 #44 (作者: XC66172, 时间: 1 year ago)

[WL13229](/hc/en-us/profiles/12285040305687-WL13229)

1. 搜索空间确实太大了。原因是这个是初始设置，各个参数累乘，地区再相加的结果；在后面迭代中可以减小搜索空间。例如category combo里我现在是9个类别选四个组合，这样就会有126种组合，再加上其他参数也有多种组合，最终搜索空间会很大。

2.可以通过以下两种方式减小搜索空间：

（a) 回测了一定数量后（例如说500次），可以看一下质量好alphas(sharpe >5 fitness >5)和质量不好alphas的各参数。例如说如果category news没有出现在里面但出现在质量不好的alphas里，那我就把news剔除不再拿来作为参数组合。其他参数同理，可以剔除掉表现不好的neutralizaiton等等。

（b) 质量好的alphas可以使用遗传算法的思维来进行再组合。例如优质alphas A是turnover <0.2 neutralization:SLOW; alphas B是author_sharpe >1.5, neutralization:RAM, 则可以再组合成C:turnover<0.2,neutralization:RAM,D:author_sharpe >1.5,neutralization:SLOW. 看一下表现如何。

---

### 评论 #45 (作者: JR23144, 时间: 1 year ago)

**在社区投稿了一篇用代码的帖子，功能包括随机生成selection表达式，与自定义combo表达式组合进行不间断的super alpha回测，可自定义limit、地区、中心化等选项。使用 了 MySQL 数据库实现的自动生成super alpha ,并多线程回测super alpha的方案，并且这个方案具备“断点续传”的能力，无惧程序中途宕机** 。

[Super-Alpha-自动生成-多线程自动回测-mysql-版本-无惧程序宕机-断点续传](../JR23144/Super Alpha 自动生成多线程自动回测 mysql 版本 无惧程序宕机断点续传代码优化.md)

---

### 评论 #46 (作者: LH44620, 时间: 1 year ago)

在量化小组沟通，发现sa确实大部分的combo 表现都差于等权。那么在sa比赛中，如果交其他combo的话，表现肯定不如全交等权的，不论是is还是os。那么是不是在比赛中交sa的策略可以调整为：尽量只交prod corr合格的等权sa呢？除非有表现好于等权的combo。那么努力的方向就变成在如何selection上了。

---

### 评论 #47 (作者: CL88457, 时间: 1 year ago)

数据区域ASI

```
selection:
```

not(own)&&

((turnover<0.12&&turnover>0.09)||(turnover<0.15&&turnover>0.13)||(turnover<0.19&&turnover>0.16))

&&(operator_count<8)&&(prod_correlation<0.5&&prod_correlation>0.0)

```
combo:
```

```
stats = generate_stats(alpha);ic = self_corr(stats.returns,20);
```

inneric = if_else(ic==1,nan,ic);

```
ts_rank(-reduce_min(inneric),120)表现图片无法上传：sharp7.01 turnover8.00% fitness9.86 returns24.75% drawdown2.02% margin61.91
```

---

### 评论 #48 (作者: QX52484, 时间: 1 year ago)

```
weight = (    1    *(prod_correlation)    *abs(self_correlation-0.5)    *(1-turnover));bool * weight 各位老师，我想请教一下像这样改变权重是如何影响到选取alpha的？ 是得到一个具体数值，而后在Selection Handling为nan的规则下，数值越高则从因子池中优先选取吗？
```

---

### 评论 #49 (作者: MM27120, 时间: 20 days ago)

以前还不懂selection和comb什么意思，如何选择，读了这篇文章感觉有那么一点明白了

还得继续看看帖子中的大神的经验

------------------------------------------------

---

