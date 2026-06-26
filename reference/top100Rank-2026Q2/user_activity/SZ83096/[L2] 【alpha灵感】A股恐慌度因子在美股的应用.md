# 【alpha灵感】A股恐慌度因子在美股的应用

- **链接**: [L2] 【alpha灵感】A股恐慌度因子在美股的应用.md
- **作者**: XX42289
- **发布时间/热度**: 1 year ago, 得票: 87

## 帖子正文

📈【A股恐慌度因子在美股的应用】💡

大家好！今天我要分享一个超有趣的因子——恐慌度因子
这个因子是可以直接提交的哦，并且具有非常强的经济学意义。

m_ret = group_mean(returns, rank(ts_mean(cap, 20)), market);

horro = abs(returns - m_ret) / (abs(returns)+abs(m_ret)+0.1);

horro_day = ts_mean(horro, 22);

ret_std = ts_std_dev(returns, 22);

adj_ret = horro_day * ret_std * returns;

adj_ret_mean = ts_mean(adj_ret, 22);

adj_ret_std = ts_std_dev(adj_ret, 22);

horro_std_bonus = zscore(adj_ret_mean) + zscore(adj_ret_std);

-horro_std_bonus

🔍  **因子构成解析** ：

1. **m_ret** ：计算股票收益的组内均值，基于市值排名和市场的平均收益。
2. **horro** ：衡量个股收益与组内均值的偏离程度，反映恐慌情绪。
3. **horro_day** ：对恐慌情绪进行22天的移动平均，平滑数据。
4. **ret_std** ：计算22天的收益标准差，衡量波动性。
5. **adj_ret** ：结合恐慌情绪和波动性，调整收益。
6. **adj_ret_mean**  和  **adj_ret_std** ：分别计算调整后收益的均值和标准差。
7. **horro_std_bonus** ：将调整后收益的均值和标准差进行标准化，并相加，得到最终的因子值。

💡  **为什么这个因子能赚钱？**

- **做多因子值越大** ：意味着恐慌情绪较低，收益稳定，适合做多。
- **做空因子值越小** ：意味着恐慌情绪较高，收益波动大，适合做空。

因子表现：
 ![图片](images/img_fb003f908d.png)

![图片](images/img_599f4b23d5.png)

![图片](images/img_d1f8cbf042.png)

---

## 讨论与评论 (17)

### 评论 #1 (作者: PN39025, 时间: 1 year ago)

你好，我觉得你的想法很有趣，但是似乎方向有些偏了，所以α的效率太低了。你是否已经尝试过一些结合的方法来提高效率，更清晰地表达想法呢？

---

### 评论 #2 (作者: XX42289, 时间: 1 year ago)

[PN39025](/hc/en-us/profiles/1532011933942-PN39025)

您好，您可以具体说一下是哪个方向偏了呢？

效率具体是哪个方面的效率呢？

这个因子在美股的表现确实略逊色，但是在其他地区还是很可以的，不过由于用户只能获取到USA，所以针对性地做了这个因子作为示范。

这当然不是一个完美的因子，或许可以有一点启发吧。

---

### 评论 #3 (作者: SB24011, 时间: 1 year ago)

This is a really interesting factor! Even though I don’t know much Chinese, I can still get the gist of it. It seems like the "fear factor" is designed to measure how much a stock’s return deviates from the average of its group, which reflects the level of panic or stress in the market. By combining this with volatility and smoothing the data with a 22-day moving average, it looks like you can identify stocks that are either more stable (good for going long) or more volatile (good for shorting).

The way this factor combines returns, volatility, and market sentiment into one value is pretty clever, and it seems like it could be really useful for making decisions in both long and short strategies. I’m definitely interested in testing this out in my own models....

---

### 评论 #4 (作者: NW35998, 时间: 1 year ago)

请问有没有相关文献推荐呢？

---

### 评论 #5 (作者: WW78643, 时间: 1 year ago)

用了 表现非常好

---

### 评论 #6 (作者: YY58435, 时间: 1 year ago)

**现在提交的时候提示说：Weight concentration 11.53% is above cutoff of 10% on 11/21/2022。**

**我给ts_backfill了一下，通过了，只是损失了一点sharpe值**

---

### 评论 #7 (作者: YL29925, 时间: 1 year ago)

加上這個ts_backfill(-horro_std_bonus,252)可以提升到Spectacular

---

### 评论 #8 (作者: YQ76635, 时间: 1 year ago)

我也用了，不过等我的 **Weight concentration更高，超过了30%；我用了winsorize，损失的sharp有点大，然后trade_when 找补回来点，总算是good**

---

### 评论 #9 (作者: OR93845, 时间: 1 year ago)

直接用，就是Spectacular，太棒了

---

### 评论 #10 (作者: TK60163, 时间: 1 year ago)

我知道我只是一个刚入门的新手，但请花一点时间看看我的评论。（由 GPT-3.5 翻译成中文）

**根据你提供的例子：**

![图片](images/img_07a70b30ec.png)

一切看起来都还好，但是……

![图片](images/img_47ec96c331.png)

提交这个 alpha 会导致我在 IQC 2025 比赛中的得分下降。因此，我现在要寻找一些方法来改进这个 alpha。

**Alpha 改进思路：**

由于这个 alpha 只关注在 panic sentiment（恐慌情绪）上升时，收益不可靠这一点。因此，我再次查看了代码，并发现了一些有趣的地方：

```
mean_returns = group_mean(returns,rank(ts_mean(cap,20)),market);horro = abs(returns-mean_returns)/(abs(returns)+abs(mean_returns)+0.1);horro_day=ts_mean(horro,22);ret_std = ts_std_dev(returns,22);adj_ret = horro_day * ret_std * returns;adj_ret_mean = ts_mean(adj_ret,22);adj_ret_std = ts_std_dev(adj_ret,22);horro_std_bonus = zscore(adj_ret_mean) + zscore(adj_ret_std);-horro_std_bonus
```

**我在想：**

> *“如果交易者处于 panic 状态，他们会在收到信息后立即买入/卖出股票。”*

因此，我提出：代码中的 “returns” 应该具体指向  **intra-day returns** ，因为随着 panic 情绪的增强，overnight returns 的影响较小。

**改进后的代码：**

```
intra_ret = close/open-1;mean_returns = group_mean(intra_ret,rank(ts_mean(cap,20)),market);horro = abs(intra_ret-mean_returns)/(abs(intra_ret)+abs(mean_returns)+0.1);horro_day=ts_mean(horro,22);ret_std = ts_std_dev(intra_ret,22);adj_ret = horro_day * ret_std * intra_ret;adj_ret_mean = ts_mean(adj_ret,22);adj_ret_std = ts_std_dev(adj_ret,22);horro_std_bonus = zscore(adj_ret_mean) + zscore(adj_ret_std);-horro_std_bonus
```

**结果：**

![图片](images/img_f90a9353c9.png)

![图片](images/img_3296ba08ef.png)

我的理论奏效了！Sharpe 增加了 0.5，收益增加了约 20%，fitness 几乎翻倍！

**让我们看看提交后的得分：**

![图片](images/img_ba48e1a480.png)

得分似乎降低了？即使这是一个表现非常好的 alpha，拥有漂亮的数据统计？

**我进一步分析原因，然后构建出这样的解释：**

> *“提交 alpha 后，虽然收益增加了，但因为收益的标准差降低了（图表线性程度不够），没有满足我组合绩效的要求。”*

**问题在于：**

![图片](images/img_2aad28c8c5.png)

图中的这两个部分负面影响了我的组合 PnL，因此我需要再想个办法。

**如何让图表更线性，以产生稳定的收益？**

在调整代码时，我注意到 alpha 的权重分布太分散。将 truncation 设置为 0.01 反而让 alpha 的收益更差。我突然想到一个想法：

> *“如果将信号改为不同的分布，会不会导致更稳定的权重分布，从而使图形更线性”*

**修改后的代码：**

```
intra_ret = close/open-1;mean_returns = group_mean(intra_ret,rank(ts_mean(cap,20)),market);horro = abs(intra_ret-mean_returns)/(abs(intra_ret)+abs(mean_returns)+0.1);horro_day=ts_mean(horro,22);ret_std = ts_std_dev(intra_ret,22);adj_ret = horro_day * ret_std * intra_ret;adj_ret_mean = ts_mean(adj_ret,22);adj_ret_std = ts_std_dev(adj_ret,22);horro_std_bonus = zscore(adj_ret_mean) + zscore(adj_ret_std);-quantile(horro_std_bonus,driver="cauchy")
```

**结果：**

![图片](images/img_a2b5a42879.png)

**组合团队绩效：**

![图片](images/img_5698024081.png)

完美！每个指标（Sharpe、Fitness、Returns、Margin）都得到了提升！

**最后，为了减少 turnover，我们使用 ts_linear_decay()，因为我没有 exponential decay 的运算符:**

![图片](images/img_6218d117ad.png)

我知道可能没有人会看到我的评论，但如果你看到了，请帮我回答以下问题：

1) 我应该提交这个 alpha 吗？换句话说，如果我提交了它，它会在长期对我产生不利影响吗？

2) 我不太理解，为什么在  `ts_mean(cap,20)`  中使用的是 20 天，但在其他 time-series 运算中却是 22 天？

3) 在计算 horro 的时候，为什么要加上 0.1？这个值的作用是什么？

4) 还有其他方法可以改进这个 alpha 吗？例如使用  `trade_when`  运算符或使用更多的数据字段？

5) 我可以把这篇评论发在中文社区论坛上吗？我想让更多人看到我的帖子！如果可以的话，你能提供我这个 alpha 想法背后的研究论文吗？

感谢你看到这里，我对你表示衷心的感谢！

---

### 评论 #11 (作者: HM16508, 时间: 1 year ago)

You can use trade_when here I used it and it improved do volume<adv20

---

### 评论 #12 (作者: ZL15100, 时间: 10 months ago)

horro = abs(returns - m_ret) / (abs(returns)+abs(m_ret)+0.1);

这里面的加0.1是什么意思了

---

### 评论 #13 (作者: ZZ37826, 时间: 9 months ago)

======================感谢分享========================
真心感谢博主的实战分享，思路清晰、逻辑扎实，对在WorldQuant平台上做跨市场迁移很有启发。
我在WorldQuant的理解：平台以公式化表达构建Alpha，强调标准化、分组中性化、风险控制与可解释性，回测以一致的行业、市值、交易成本等框架约束，便利我们快速从想法到可提交Alpha。

- 因子核心先按市值排序做组内收益均值，建立相对比较的基线。
- 以个股收益相对组均的偏离度刻画恐慌，并用22日均线平滑降低噪声。
- 结合22日收益波动率放大显著偏离的权重，形成调整后的收益序列。
- 对调整后序列分别取均值与标准差并标准化相加，得到最终打分。
- 信号含义是低恐慌更稳健、分值高侧偏多，高恐慌波动放大一侧更适合做空。

我学到的点与打算进一步尝试：
- 在Brain上可将该思路直接公式化并轻量改造以复用到美股与A股。
- 组内基准可用行业或风格分组替换市值排序，对比稳健性。
- 平滑窗口与波动窗口分开调参，观察收益、回撤与换手的权衡。
- 对打分做分层、去极值与中性化，贴合平台的风险与审核要求。
- 加入交易成本、撮合延迟与停牌过滤，提升提交后的可实现度。

再次感谢博主无私分享，祝大家在WorldQuant多产高质量、可复现实证的Alpha，越做越稳、越做越好！

================励志学习每一个优质帖子=================

---

### 评论 #14 (作者: CC85858, 时间: 9 months ago)

ZL15100                                                                                                                                                                               应该是防止分母为0吧

---

### 评论 #15 (作者: CW99617, 时间: 7 months ago)

Thank you for identifying a version of fear and greed index! While the original alpha and the improved ones mentioned in  [TK60163](/hc/en-us/profiles/31451865057303-TK60163) 's thread above are not submittable on my end mostly because their Sharpe ratios are not significantly above 1.58 and the prod correlations are also not below the 0.7 benchmark, I’ve successfully implemented a submittable alpha after:

1. better accounting for the within-group deviation for a particular stock to capture its fear index;
2. incorporating the  **short- and long-term signals**  into the current model;
3. neutralizing the final trading signals with  **appropriate nonlinear transformations and truncation or smoothing techniques** .

Future alpha ideas based on this delay-1 model might include its extension to a delay-0 counterpart, which require a Sharpe ratio of at least 2.69 and the 2-year Sharpe exceeding the cutoff 2.69 as well.

There are also two  **(hyper)parameters**  that I have to manually tune to achieve the final submissible model.

---

### 评论 #16 (作者: HL64570, 时间: 7 months ago)

adj_ret取名为“调整后收益”，名字起得非常糟糕，因为该名字和含义毫无关系！

adj_ret是horro_day和ret_std的乘积，同时考虑了个股收益率偏离均值的程度和本身的波动性，代表一种综合性风险。

注意是“风险”，不是“收益”！

---

### 评论 #17 (作者: LL27686, 时间: 1 month ago)

[TK60163](/hc/en-us/profiles/31451865057303-TK60163)  really appreciate your thought process. Im also in iqc now searching for ideas, learnt multiple new things just by looking at your comment alone. Hv you found out the reason behind 2? I also noticed multiple alphas shared here have such parameter difference, wonder if that really matters. For 3 you likely alr know, its likely to prevent denominator from been 0 or very small number which might distort the alpha. 4, respect, i tend to just submit the moment i come out with a spectacular besides some minor tweakings.

---

