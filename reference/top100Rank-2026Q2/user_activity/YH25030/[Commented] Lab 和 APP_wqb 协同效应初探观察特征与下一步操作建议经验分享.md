# Lab 和 APP_wqb 协同效应初探：观察特征与下一步操作建议经验分享

- **链接**: [Commented] Lab 和 APP_wqb 协同效应初探观察特征与下一步操作建议经验分享.md
- **作者**: LL87164
- **发布时间/热度**: 11个月前, 得票: 52

## 帖子正文

**概述：** 找到某个信号后下一步该怎么操作，是个经常遇到的问题。下面结合一个实例分享一下如何通过Lab 和 APP_wqb 协同，找到答案。

**原始信号模版及表现：**

```
ts_zscore(<compare/>(<oth455_data_1/>, <oth455_data_2/>), 252)
```

**![图片](images/img_81ea389a95.png)**

**1. Lab 里观察数据特征**

![图片](images/img_2714c03870.png)

可以清晰地看到，数据在不同时间段表现出完全不同的“ **状态** ”。以其中一个 Instrument 为例：

- 2015年至2017年底: 信号呈现出非常平滑、规律的缓跌趋势。它的波动很小。
- 2018年前后: 信号突然变得剧烈震荡、毫无规律。它的值在短期内上下跳动，表现出极大的不确定性。
- 2018年中之后: 信号进入了一个新的、相对平稳的平台期。

尽管 ts_zscore 做了标准化，然而，z-score值仍然可能表现出显著的波动性。极端值仍然可能不成比例地影响夏普比率的计算。

**2. 把表达式以及这个数据特征输入 App**

**![图片](images/img_6d7763ce4a.png)**

得到带排名的建议，找到其中一个如下：

*“Applying ts_entropy after ts_zscore(<compare/>(<oth455_data_1/>, <oth455_data_2/>), 252) could meaningfully improve the Sharpe ratio, but the effectiveness depends heavily on the underlying data characteristics. The current expression calculates a z-score of the difference between two principal components (PCA factors) over a 252-day window. This aims to identify periods of unusual deviations in the relationship between these factors. However, it doesn't directly capture the volatility or predictability of these deviations. This is where ts_entropy can add value. By applying ts_entropy to the output of the ts_zscore calculation, we obtain a measure of the randomness or predictability of the z-score time series. A high entropy value suggests a more unpredictable, noisy signal, while a low entropy value suggests a more predictable, potentially trend-following signal. How it improves the strategy: Risk Management: High entropy periods indicate greater uncertainty. During these periods, we can reduce position size or even exit trades entirely, thus mitigating potential losses from unpredictable market movements. This directly contributes to improving the Sharpe ratio by lowering the denominator (risk). Signal Enhancement: Low entropy periods suggest a more predictable pattern in the z-score. This could indicate a stronger, more reliable signal for trading. We can increase position sizes or enter new trades with higher confidence during these periods, potentially increasing returns (numerator of Sharpe ratio). * Synergistic Effect: The combination leverages the strength of both operators. ts_zscore identifies potential trading opportunities based on deviations from the norm, while ts_entropy provides a measure of the reliability of those signals. This allows for dynamic risk management and signal weighting, leading to a more robust and potentially higher Sharpe ratio strategy. Example: Suppose the ts_zscore output shows a consistently high value for several days. A simple strategy based solely on this might lead to large losses if the market suddenly reverses. However, if the ts_entropy of this z-score time series is also high, it suggests this high value is part of a noisy, unpredictable period. The combined strategy would then signal caution, potentially preventing significant losses. Conversely, a consistently low z-score with low entropy would suggest a strong, persistent trend, justifying a more aggressive trading strategy. Limitations: The effectiveness depends on the data. If the z-score time series is inherently random, ts_entropy might not add much value. The choice of the d parameter (number of past days for entropy calculation) in ts_entropy is crucial and requires careful optimization. Overfitting is a potential concern. Despite these limitations, the potential for improved risk management and signal enhancement makes this a good addition, hence the score of 6.”*

将上面的内容再问一下大模型，得到一个总结：

*“该策略的核心思想是，使用  `ts_entropy`  (信息熵) 作为一种**“信号可靠性”的衡量指标**，来动态地调整基于  `ts_zscore`  信号的交易行为。*

*它本身不产生买卖信号，而是像一个“天气预报系统”，告诉我们当前  `ts_zscore`  信号所处的环境是“晴朗可预测”还是“风雨交加、充满不确定性”。”*

这一点和 Lab 中观察到的特征比较吻合。回测看看结果。

**3. 回测结果：**  ![图片](images/img_0d8883cd09.png)

有提升，说明图中的数据特征（状态切换）是“问题”，而  `ts_entropy`  算子是解决这个问题的“工具”。

---

## 讨论与评论 (39)

### 评论 #1 (作者: JG91554, 时间: 10个月前)

*<compare/>(<oth455_data_1/>, <oth455_data_2/>), 这里的compare是指什么，*

---

### 评论 #2 (作者: LL87164, 时间: 10个月前)

[JG91554](/hc/en-us/profiles/30669600255511-JG91554)

基本的加减乘除。重点还是其背后的意义。

---

### 评论 #3 (作者: WL13229, 时间: 10个月前)

这个帖子我非常喜欢，

---

### 评论 #4 (作者: DH36161, 时间: 10个月前)

是我没有这个operator的权限吗？

![图片](images/img_99721da95c.png)

---

### 评论 #5 (作者: WY25891, 时间: 10个月前)

请问APP_wqb中在哪里找到这个界面（quant reseach target)

---

### 评论 #6 (作者: LL87164, 时间: 10个月前)

[DH36161](/hc/en-us/profiles/28900502318615-DH36161)

应该是。APP_wqb 会在有权限的里面进行推荐。

---

### 评论 #7 (作者: LL87164, 时间: 10个月前)

[WY25891](/hc/en-us/profiles/27031621269399-WY25891)

Inspiration House

---

### 评论 #8 (作者: ER48854, 时间: 10个月前)

居然成了lab的导论了，好。

---

### 评论 #9 (作者: ZY88181, 时间: 10个月前)

ts_entropy , to_nan都没权限，咋整？

---

### 评论 #10 (作者: YL20168, 时间: 10个月前)

请问app_wqb能不能发我一份， [956629514@qq.com](mailto:956629514@qq.com) ，非常感谢

---

### 评论 #11 (作者: WL58980, 时间: 10个月前)

太棒了

---

### 评论 #12 (作者: ER48854, 时间: 10个月前)

数据的异常波动还可能与当时的金融市场有关

---

### 评论 #13 (作者: AW52508, 时间: 10个月前)

请问app_wqb能不能发我一份， [cwang_2020@163.com](mailto:cwang_2020@163.com) ，非常感谢

---

### 评论 #14 (作者: LL87164, 时间: 10个月前)

[YL20168](/hc/en-us/profiles/31954206483991-YL20168)   [AW52508](/hc/en-us/profiles/31627201900311-AW52508)

安装最近培训 MCP 时的包里有最新版的 APP，在 ~/site-packages/cnhkmcp/untracked/APP 目录下。

---

### 评论 #15 (作者: JY75067, 时间: 10个月前)

app_wqb帮忙分享我一下， [yujilong_163163@163.com](mailto:yujilong_163163@163.com) 。谢谢

---

### 评论 #16 (作者: ZL42615, 时间: 10个月前)

这篇文章写的好，学习了！

---

### 评论 #17 (作者: XW61573, 时间: 10个月前)

It is  very goog

---

### 评论 #18 (作者: YZ64617, 时间: 9个月前)

请问app_wqb能不能发我一份， [eexzy@hotmail.com](mailto:eexzy@hotmail.com) , 非常感谢!!

---

### 评论 #19 (作者: JB71859, 时间: 9个月前)

这里的 *<oth455_data_1/>, <oth455_data_2/>是什么，same-data* 吗还是什么，但该说不说你的这个工作流确实是不错的，有很多我可以去学习和借鉴的地方，这个模板好像在Alpha模板征文也有。
====================================================================================

---

### 评论 #20 (作者: WH74165, 时间: 9个月前)

感谢分享

---

### 评论 #21 (作者: LM81527, 时间: 9个月前)

这个other是很多模板都可以使用的，看来是一个比较好的方法，app_wqb很多人都没怎么看了，其实有很多模板是可以用的，这个值得学习，和借鉴，加油，多努力，好像发钱了是把， 对，是发了，加油加

===========================生命是一场恩典=========================================================

---

### 评论 #22 (作者: SQ89646, 时间: 9个月前)

APP_wqb能否支持其他大模型，比如gemini

---

### 评论 #23 (作者: LR93609, 时间: 9个月前)

感谢分享，非常不错的分享

我们之前看到的大多数帖子，都是分享idea、模版或者是工具的，

很少有如此详尽的分享pnl曲线优化方法和路径的，非常值得借鉴。

我的很多调试都是基于对setting和operators的理解和认识，

实际上会有很多盲区和不理性的地方，比如

1. decay与turnover的关系，

2. truncation与signed_power以及power的关系

3. NAN HANDLING与ts_backfill之间的关系

4. neut与group_neut之间的关系

希望后续能够借助博主的方式，不断改善。

再次感谢分享，受益颇深

--------------------------------------------------------------------------------------------------

凡事发生，皆利于我；愿我所愿，尽是美好

--------------------------------------------------------------------------------------------------

---

### 评论 #24 (作者: LY85808, 时间: 9个月前)

用这个模版找到了能提交的因子，感谢分享！

---

### 评论 #25 (作者: LY52969, 时间: 9个月前)

请问app_wqb能发我一份么，非常感谢！我的邮箱是  [foxmeder@outlook.com](mailto:foxmeder@outlook.com)

---

### 评论 #26 (作者: LL87164, 时间: 9个月前)

[LY52969](/hc/en-us/profiles/32934254632855-LY52969) ：

pip install cnhkmcp

MCP 安装包里有最新版的 APP，在 ~/site-packages/cnhkmcp/untracked/APP 目录下。

---

### 评论 #27 (作者: YH25030, 时间: 9个月前)

谢谢分享。我在另外一篇帖子里也看到利用ts_entropy找到主信号。说明大佬们多喜欢用这个操作符。我是没有这个操作符。等下个赛季，希望能被分配到这个操作符（笑）。

---

### 评论 #28 (作者: SZ20589, 时间: 9个月前)

这个compare是什么？ts_entropy 没有这个operator啊，要到什么等级才有它呢？有没有等效它的操作符呢？我很多还是不懂。

希望后续能够借助博主的方式，不断改善。

再次感谢分享，受益颇深

--------------------------------------------------------------------------------------------------

加油。

---

### 评论 #29 (作者: QP72475, 时间: 9个月前)

感谢，又学到了新的工作流了。

---

### 评论 #30 (作者: AH18340, 时间: 9个月前)

感谢大佬分享，之前用lab只是看看，感觉自己也不知道怎么改进，只能乱套操作符。现在收到一个启发了，之后会多试试。

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #31 (作者: ZJ47021, 时间: 9个月前)

好多操作符都没有！

---

### 评论 #32 (作者: AM12075, 时间: 9个月前)

在应用 ts_entropy 之后确实能捕捉到信号的“状态切换”，但也引发了一些值得思考的问题。信息熵在多大程度上能够稳定刻画不同市场环境下的可预测性？它是否只是在特定样本阶段有效，而在未来数据中可能失效？其次，熵参数 d 的选择如何在避免过拟合和保持敏感性之间平衡，ts_entropy 更多是一种风险控制工具，是否会因过度抑制信号而牺牲收益端的潜力，如果市场结构变化导致信号特征发生偏移，熵指标是否仍然具备鲁棒性？这些问题都需要在进一步的回测和交叉验证中得到检验。

---

### 评论 #33 (作者: MY49971, 时间: 9个月前)

很不错的分享，现在是AI时代，这些工具必须得学会使用

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #34 (作者: LL83568, 时间: 8个月前)

请问app_wqb能不能发我一份， [a2485933921@qq.com](mailto:a2485933921@qq.com) ，非常感谢

---

### 评论 #35 (作者: DD76063, 时间: 8个月前)

但是这样会不会容易过拟合，因为是提前知道了数据的变化

---

### 评论 #36 (作者: LL87164, 时间: 8个月前)

[DD76063](/hc/en-us/profiles/33194548802327-DD76063)

根据捕获、归纳的数据特征，应用于未来可能出现的同样情况的机会。不算是过拟合。

---

### 评论 #37 (作者: EP71225, 时间: 7个月前)

请问app_wqb能不能发我一份， [echopan1234@hotmail.com](mailto:echopan1234@hotmail.com)   非常感谢!!

---

### 评论 #38 (作者: AA52414, 时间: 7个月前)

请问app_wqb能不能发我一份， [1853705298@qq.com](mailto:echopan1234@hotmail.com)  非常感谢！！

---

### 评论 #39 (作者: CT68230, 时间: 3个月前)

请问app_wqb能不能发我一份， [1009682631@qq.com](mailto:956629514@qq.com) ，非常感谢

---

