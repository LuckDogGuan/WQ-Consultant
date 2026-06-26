# 【Alpha灵感】Stock Market's reaction to liquidity shocksAlpha Template

- **链接**: [Commented] 【Alpha灵感】Stock Markets reaction to liquidity shocksAlpha Template.md
- **作者**: TK60163
- **发布时间/热度**: 1年前, 得票: 19

## 帖子正文

**这篇论文在撰写过程中出现了一个随机的错误，结果意外地产生了一个表现良好的 alpha。（如果你能找出这个 alpha 为什么有效，将不胜感激）**

研究论文： [https://www.econstor.eu/bitstream/10419/108624/1/erf_wp_1304.pdf](https://www.econstor.eu/bitstream/10419/108624/1/erf_wp_1304.pdf) 
讲义资料： [https://ba-odegaard.no/teach/notes/liquidity_estimators/amihud_estimator/amihud_lectures.pdf](https://ba-odegaard.no/teach/notes/liquidity_estimators/amihud_estimator/amihud_lectures.pdf)

**摘要：**

This paper investigates how the stock market reacts to firm level liquidity shocks. We find that negative and persistent liquidity shocks not only lead to lower contemporaneous returns, but also predict negative returns for up to six months in the future. Long-short portfolios sorted on past liquidity shocks generate a raw and risk-adjusted return of more than 1% per month. This economically and statistically significant relation is robust across alternative measures of liquidity shocks, different sample periods, and after controlling for various risk factors and firm characteristics. Furthermore, the documented effect is stronger for small stocks, stocks with low analyst coverage and institutional holdings, and for less liquid stocks. Our evidence suggests that the stock market underreacts
to firm level liquidity shocks, and that this underreaction can be driven by investor inattention as well as illiquidity.

**我们的灵感来自 PDF 第13页第1段：**

> *The significantly positive correlation between liquidity shocks and future stock returns suggests that negative liquidity shocks (reductions in liquidity) are related to lower cross-sectional stock returns. In this section, we perform formal analysis, and show that the pricing effect documented in this paper cannot be explained by other risk factors and firm characteristics that are known to predict future stock returns in the cross-section.*

**现在让我们使用流动性冲击与股票回报之间的相关性来构建 alpha。**

**但是等等，我们该如何衡量流动性冲击？**

**让我们看看第4页第1段：**

> The main liquidity shock variable we employ is constructed as the standardized innovation of the negative Amihud’s (Amihud (2002)) illiquidity measure, demeaned (using the past 12-month illiquidity as the mean) and divided by its past 12-month standard deviation.

由于它使用了 **Amihud illiquidity measure** ，我们尝试再找一篇有关该公式的论文：

![图片](images/img_c0471df28f.png)

在拥有所有所需条件后，我们开始构建 alpha：

```
amihud = (10^6)*(1/252)*ts_sum(abs(returns)/volume,252);illiquidity = ts_mean(amihud,252)/ts_std_dev(amihud,252);-ts_corr(illiquidity,returns,63)
```

这个 alpha 确实表现出了一些信号，但依旧较弱。

![图片](images/img_35a3c95d36.png)

经过对数值和操作符的一些调整，我偶然发现了一个表现相当不错的 alpha：

![图片](images/img_feb8298c2a.png)

Expression:

```
amihud = (10^6)*(1/252)*ts_sum(abs(returns)/volume,252);illiquidity = normalize(amihud,useStd=false);-ts_corr(illiquidity,amihud,42)
```

![图片](images/img_c21be26331.png)

使用标准化 amihud 与 amihud 本身在两个月内的时间序列相关性，这样就能创建一个可以独立提交的 alpha。

在此发现后，我尝试进一步优化表达式以获得最佳性能用于提交。以下是最终版本：

```
amihud = (10^6)*(1/252)*ts_sum(abs(returns)/volume,252);illiquidity = normalize(amihud,useStd=false);-hump(group_neutralize(ts_corr(illiquidity,amihud,42),bucket(rank(mdl77_valuemomemtummodel_reportedearningsmomentummodule),range="0,1,0.2")),hump=0.0005)
```

New data introduced: mdl77_valuemomemtummodel_reportedearningsmomentummodule

新增数据： `mdl77_valuemomemtummodel_reportedearningsmomentummodule` 
定义：已公布收益动量模块（Reported Earnings Momentum module）

我选择这个因子用于中性化的原因是，我认为高收益公告的股票已经吸引了许多投资者/分析师的注意，因此投资者/分析师不会对流动性冲击反应不足，因为他们已投入该股票。

**结果：**

![图片](images/img_7ac3da2a4e.png)

**我想请教以下几个问题：**

1）这个 alpha 是基于我使用论文中提到的变量构建的新想法，但我整个表达式都和原文不同。这样的 alpha 是否值得推荐？

2）这个 alpha 的回报略有下降。我给你看一下在哪个地方：

![图片](images/img_d1f1ecf487.png)

虽然最后一年交易期回报下降，我仍然相信它在 OS 表现会很好，因为在5年回测期间没有出现大幅亏损。这种情况下是否还推荐提交这个 alpha？

3）对于观看我帖子的顾问们，你们可以尝试将这个 alpha 应用于不同地区/中性化方法/股票池吗？我目前还是一名 conditional consultant，但我非常好奇这个 alpha 在其他国家以及不同慢因子中性化和股票池中是否表现更好。

感谢你阅读我的帖子！

---

## 讨论与评论 (13)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

推荐提交的

平台数据跟论文使用数据不一定完全相同，计算方式，逻辑等底层架构也未必相同。基于相同思路进行衍生是一个很好的方法！

至于因子为什么有效，这个需要进行额外研究了，粗略看下来是关注了amihud和2月前的amihud变化，推测是买入一些流动性相比之前更好的标的？毕竟amihud是个 反向指标，指标越大流动性越差。

另：表达式里面的数值参数可以删除，大家都乘等于大家都不乘。

（个人拙见，欢迎讨论）

---

### 评论 #2 (作者: XX42289, 时间: 1年前)

非常优秀的新人，流动性指标一直是在全世界任何市场都有效的因子，近期的失效其实没太关系，只需要你的策略pool里有足够的其他类型的因子即可。你可以看到2018和2019年的表现其实也很差，说明他是一个市场风险较大的因子，或许你可以通过regression_neut这类操作符去除掉风险。

---

### 评论 #3 (作者: YW93864, 时间: 1年前)

[TK60163](/hc/en-us/profiles/31451865057303-TK60163)

```
illiquidity = normalize(amihud,useStd=false);
```

您在这一步中使用了截面的信息。

您可以通过大语言模型获得一些其实，比如您可以询问他：为什么使用截面归一化后的amihud和绝对值amihud的相关性对未来收益有预测能力？
回答：

- 截面标准化后的  `illiquidity`  反映的是股票在横截面上的相对流动性，而原始  `amihud`  反映绝对流动性水平。
- 当两者相关性降低时，表明股票的流动性变化与市场整体背离，可能隐含错误定价（如恐慌性抛售导致的流动性暂时枯竭）。

---

### 评论 #4 (作者: LL87164, 时间: 1年前)

@  [YW93864](/hc/en-us/profiles/14096946892439-YW93864)

另一个解开这个“新想法”的办法。学到了。多谢分享。

关于横截面标准化，我理解它还有另外一层作用：去掉量纲的影响。即消除amihud计算时用的volume的量纲（units of currency）

@ Tan Kang(TK60163)

个人认为是否完全和论文一致不重要，背后的支撑和经济学基础才是要点，即最后中性化因子的选用。如果说上面大模型解释的是主信号是什么，那最后主信号落实在什么地方更重要，也是要学习和提升的地方。希望能在这方面多谈谈当时的想法和经验。

论文转模版时，大部分都停留在将论文的公式做简单的模版化上了。“偶然”里有必然，希望能看到更多的这种“偶然”。多谢分享！

---

### 评论 #5 (作者: QP72475, 时间: 1年前)

感谢分享，最近正在学习自己组建alpha。

---

### 评论 #6 (作者: YX23928, 时间: 1年前)

你好，我在顾问权限下，回测十年数据，2013年-2018年的sharpe及fitness均小于1，2019年-2023年sharpe/finess在2左右，根据is pnl显示，这个alpha有under fitting的嫌疑，建议增加tarde when操作符，使得pnl变得平滑。

另表达式中数值参数无效，建议删除，减少operator数量，因为在后续的alpha研究中，operator per指标是影响genius定级。

---

### 评论 #7 (作者: MZ54236, 时间: 1年前)

好厉害的新人，非常有启发的构建alpha经历。

个人认为，图上的pnl表现，和传统 “厂” 字型因子区别还是挺大的，最后还保持了可观的上升趋势。

---

### 评论 #8 (作者: LL87164, 时间: 1年前)

[Tan Kang(TK60163)](/hc/en-us/profiles/31451865057303-Tan-Kang-TK60163)

再论“ *这个模版为什么有效* ”：

如果说第一个模板是对论文的 **一次“失败”的模仿** 。那第二个模板则是在模仿失败后， **一次成功的创新** 。

Alpha 1中的  `illiquidity = ts_mean(amihud, 252)/ts_std_dev(amihud, 252)`  计算的是 **时间序列均值除以时间序列标准差** 。它衡量的是数据的相对离散程度， **不是论文所定义的“冲击”** 。它没有捕捉到当前流动性水平相对于其自身历史的“意外变化”。

Alpha 2中关键步骤是  `illiquidity = normalize(amihud, useStd=false)`  。原始论文的“冲击”定义：与“过去的自己”比较（时间序列），而Alpha 2的“冲击”定义：与“现在的别人”比较（横截面）。这是不是这个模版有效的原因先不说，但是 **创新** 是确定的。原始论文研究的是 **个股自身流动性的时间序列意外** ，Alpha 2构建的是 **个股流动性的横截面背离。**

直接照搬学术公式往往效果不佳，而理解其背后的经济学直觉，并结合平台特有的工具（如 `normalize` ）进行改造和创新，这才是可取之处。

---

### 评论 #9 (作者: SM63503, 时间: 1年前)

大佬好强，之前以为和别人相比只能用group操作符，没想到还有这种新思路

---

### 评论 #10 (作者: SZ83096, 时间: 1年前)

大佬，请教下："使用标准化 amihud 与 amihud 本身在两个月内的时间序列相关性，这样就能创建一个可以独立提交的 alpha。” 这个是基于什么考虑的呢？是论文中提到的还是？我不是很理解您是怎么想到这个数据处理的方法的？

======================================================================

---

### 评论 #11 (作者: PX70901, 时间: 1年前)

大佬可以多谢文章吗？看你很多帖子 学到很多

---

### 评论 #12 (作者: FL39657, 时间: 1年前)

很棒的想法，期待大佬多发文章

---

### 评论 #13 (作者: LL49894, 时间: 1年前)

```
ts_corr(illiquidity,amihud,42)
```

ts_corr计算了的是自身变换值的相关性，也就是amihud与normalize(amihud)的相关性，不知道是否符合逻辑。

---

