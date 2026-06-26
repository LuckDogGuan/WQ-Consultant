# [Alpha Idea]Is predictability of industry returns after M&A announcement effictive ?

- **链接**: [Commented] [Alpha Idea]Is predictability of industry returns after MA announcement effictive.md
- **作者**: YQ76635
- **发布时间/热度**: 9个月前, 得票: 12

## 帖子正文

最近在根据论文构建alpha的 idea，其中这篇论文论述的核心观点及内容非常典型来用于构建alpha ida。

这篇论文基本信息如下：

- **题目：** Predictability of Industry Returns After M&A Announcement
- **作者：** Christian Funke, Timo Gebken, Lutz Johanning, Gaston Michel

### **论文核心内容概述**

这篇论文研究了 **并购（M&A）公告后，目标公司所在行业的股票回报是否具有可预测性。**

**核心方法：事件研究法 + 投资组合分析**

- **事件研究：** 计算并购公告窗口期（如公告日前后几天）内目标公司所在行业的 **异常回报** （Abnormal Returns, ARs）和 **累计异常回报** （Cumulative Abnormal Returns, CARs）。这用于衡量公告对行业的 **即时冲击** 。
- **投资组合分析：** 这是检验 **可预测性** 的关键。
- **构建行业组合：** 在每个并购公告事件后，根据特定标准（如公告后短期表现、公告本身特征）将目标公司所在行业进行分组（例如，表现最好的行业组合 vs 表现最差的行业组合）。
- **持有期检验：** 在公告后的不同持有期（如1个月、3个月、6个月、1年、2年、3年）内，跟踪这些行业组合的 **买入并持有超额回报** （Buy-and-Hold Abnormal Returns, BHARs）或 **累计超额回报** （Cumulative Abnormal Returns, CARs）。

我根据论文提到的核心方法首先构建了alpha的雏形，数据字段取mws85_sentiment

anl8_bessplitptg_d1_value，snt1_d1_earningssurprise，

其中mws85_sentiment 代表公告发布后的事件反映,anl8_bessplitptg_d1_value 为并购事件中目标公司的价格。异常回报用公式(snt1_d1_earningssurprise*close);

Alpha表达式如下：

a=-ts_regression(vec_avg(mws85_sentiment),vec_avg(anl8_bessplitptg_d1_value),22);#a的值越高，并购公告产生的反应越大，这用于衡量公告对行业的 **即时冲击**

abnomal_return=(snt1_d1_earningssurprise*close);#异常收入，由于公告事件产生的超过平时的收入

b=rank(a)>0.7?ts_mean(abnomal_return,22):nan;# 用rank(a)进行打分，分数大于0.7时，捕捉产生异常收入的股票。

c=group_rank(b,densify(bucket(group_rank(cap, sector),range='0.1, 1, 0.1')));#在行业内进行Cap 分组，并捕捉行业中产生异常收入的股票，对行业中排名高的股票做多。

Alpha 雏形构建完成后进行回测。回测信号处于斜率稍低但稳定上升的曲线状态，曲线表现平稳，并且有信号出现。

- 再研读论文，论文中提到 **横截面回归分析：** 进一步控制其他可能影响行业回报的因素（如行业规模、估值、动量、波动性等），检验并购公告事件本身及其特征（如交易规模、支付方式、行业相关性）对行业未来超额回报的 **预测能力** 。

我将动量和估值这2个影响行业回报的因素引入alpha的表达式。

表达式如

a=-ts_regression(vec_avg(mws85_sentiment),vec_avg(anl8_bessplitptg_d1_value),22);

abnomal_return=(snt1_d1_earningssurprise*close);

b=rank(a)>0.7?ts_mean(abnomal_return,22):nan;

c=group_rank(b,densify(bucket(group_rank(cap, sector),range='0.1, 1, 0.1')));

d=group_zscore(-ts_quantile(cap / high, 22),densify(densify(sta2_top3000_fact3_c50)));

e=-ts_delta(winsorize(ts_backfill(anl4_flag_erbfintax, 120), std=4), 66);

sig=0.5*c+0.3*d+0.2*e;

其中d为动量因子；e为估值因子，字段anl4_flag_erbfintax 含义为Earnings before interest and taxes - forecast type (revision **/**  **new** /...)。

曲线如下：

回测指标如下：

Sharpe

1.94

Turnover

31.55%

Fitness

1.17

Returns

11.39%

Drawdown

8.51%

Margin

7.22‱

这里核心信号权重为0.5；动量权重0.3，估值权重0.2

下一版，我微调权重，核心信号权重为0.5；动量权重0.4，估值权重0.1.

回测指标如下：

Sharpe

2.18

Turnover

37.49%

Fitness

1.08

Returns

9.15%

Drawdown

5.63%

Margin

4.88‱

这里着重说明下，单独剥离每个因子，核心alpha的指标sharp 只有0.75，而动量指标和估值指标的sharp均超过1.25；但权重分配时核心信号也就是主信号权重低于0.5时，整个曲线变形，指标骤减。这就是论文研究的好处，它给你个方向，然后按照这个方向构建而不是盲目的根据单个alpha因子的指标好坏来分配权重构建——我觉得这个因子sharp高，分配多点权重拉下sharp的分值。而是根据论文研究的结果，主信号从核心观点取出，然后根据论文里提供的信息，补益，增强主信号，但不能抢夺主信号，否则会将主信号稀释或混淆。因此构建alpha的时候绝对不能根据单个因子指标的好坏分配权重，而是要根据主信号的形态和需要增强，补充——有时候单个主信号不能充分反映市场的情况。

---

## 讨论与评论 (6)

### 评论 #1 (作者: YQ76635, 时间: 9个月前)

我将该alpha 表达式做成模板，得到另外的alpha，指标如下：

Sharpe

2.48

Turnover

31.17%

Fitness

1.29

Returns

8.47%

Drawdown

4.01%

Margin

5.43‱

该alpha已经提交

---

### 评论 #2 (作者: JX79797, 时间: 9个月前)

权重微调的最后一版，明显不如前一版啊

**#========= WORLDQUANT BRAIN CONSULTANT ========== #**

**# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%**

**# sys.setrecursionlimit(α∞)**

**# PnL = ∑(Robustness * Creativity)**

**#无限探索、鲁棒性优先，创新性增值**

**#=================奋进的小徐=======================#**

---

### 评论 #3 (作者: SC84371, 时间: 9个月前)

不错

---

### 评论 #4 (作者: YQ51506, 时间: 9个月前)

这篇关于并购公告后行业回报可预测性的研究挺有意思的。大佬提到的论文方法和alpha构建思路很清晰，特别是用事件研究法和投资组合分析来捕捉行业层面的异常回报。在WorldQuant Brain上回测时，我也发现单一因子往往表现不稳定，需要结合动量、估值等辅助因子来增强主信号。不过有个小疑问：异常回报计算用snt1_d1_earningssurprise*close是否充分考虑了行业beta和风险调整？可能需要加入行业中性化处理。另外权重分配的逻辑很专业，确实不能单纯看sharp值分配权重，而应该基于因子间的互补性。回测结果看起来不错，sharp从1.94提升到2.18，drawdown也降低了，说明多因子组合有效。

---

### 评论 #5 (作者: LR93609, 时间: 9个月前)

感谢分享，不错的复现案例，个人感觉有几个问题：

**1. 欠拟合：** 如果将532调整为541指标会变好，为何不遍历所有的选项呢？111/235/433/343...

**2. 过拟合：** ts_regression的时候，两个field大概率是不同频的，直接计算，结果可能是过拟合的。

**3. 无意义：** densify为何要连续用两次呢？一次已足矣

--------------------------------------------------------------------------------------------------------------------------

凡事发生，皆利于我；愿我所愿，尽是美好

--------------------------------------------------------------------------------------------------------------------------

---

### 评论 #6 (作者: MS51256, 时间: 9个月前)

感谢大佬的分享，

a=-ts_regression(vec_avg(mws85_sentiment),vec_avg(anl8_bessplitptg_d1_value),22);

abnomal_return=(snt1_d1_earningssurprise*close);

b=rank(a)>0.7?ts_mean(abnomal_return,22):nan;

c=group_rank(b,densify(bucket(group_rank(cap, sector),range='0.1, 1, 0.1')));

d=group_zscore(-ts_quantile(cap / high, 22),densify(densify(sta2_top3000_fact3_c50)));

e=-ts_delta(winsorize(ts_backfill(anl4_flag_erbfintax, 120), std=4), 66);

sig=0.5*c+0.3*d+0.2*e;

这几个表达式对他们取不同的权值得到的结果，敢交吗
且不提过拟合的风险，这个op数量也是极为炸裂

---

