# Machine Alpha 基础知识3：继续理解时间序列模板，以情绪类数据为例

- **链接**: [L2] Machine Alpha 基础知识3继续理解时间序列模板以情绪类数据为例.md
- **作者**: WL13229
- **发布时间/热度**: 1 year ago, 得票: 32

## 帖子正文

以下是一个与情绪相关数据的模板：

> < [time_series_operator/>](https://platform.worldquantbrain.com/learn/data-and-operators/operators#time-series-operators) (<positive_sentiment/> - <negative_sentiment/>, <days/>)

隐含假设：如果与之前相比，一家公司的净情绪是正面的，那么股价可能会上升。

具体实现:

- 直接对净情绪值进行时间序列运算。 使用合理的天数参数，例如周（5天）、月（20天）、季（60天）或年（250天）。
- [Sentiment Model](https://platform.worldquantbrain.com/data/data-sets?category=sentiment&delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)  and  [Neutralization](https://platform.worldquantbrain.com/learn/documentation/create-alphas/neut-cons) to improve Alpha.
- 除了这个简单的实现，您可能想要将其扩展为更复杂的格式，例如:

> positive_sentiment = rank(<backfill_op/>(<positive_sentiment/>, days));
> negative_sentiment = rank(<backfill_op/>(<negative_sentiment/>, days));
> sentiment_difference = <compare_op/>(positive_sentiment, negative_sentiment):
> <time_series_operator/>(sentiment_difference, days)

具体细节:

- <backfill_op/>: 由于情绪数据通常覆盖度较低，因此使用ts_backfill或to_nan进行数据回填以实现更高的覆盖度是更好的选择。 排名：此模板在回填情绪上使用Rank排名运算符，这确保了数据分布处于可控的范围内。这一步骤还从原始数据中去除了一些噪音。

- <compare_op/>: 除了原始的减法运算符，您还可以从其他比较运算符中进行选择。 通过在模板中更改数据字段、运算符和参数，您可以有效地生成多样化的可提交Alpha，特别是通过 [BRAIN API](/hc/en-us/articles/20786107171351) .

继续尝试这个模板吧。 请在下面评论中分享您对这个模板的发现与拓展！

---

## 讨论与评论 (12)

### 评论 #1 (作者: ZZ88928, 时间: 1 year ago)

请问老师 positive_sentiment和negative_sentiment 可以使用哪些数据集

---

### 评论 #2 (作者: WL13229, 时间: 1 year ago)

[ZZ88928](/hc/en-us/profiles/28828734017303-ZZ88928)

可以使用data工具进行搜索👉 [WorldQuant BRAIN](https://platform.worldquantbrain.com/data)

---

### 评论 #3 (作者: JS34795, 时间: 1 year ago)

这里的rank是和其他的股票想比较吗

---

### 评论 #4 (作者: HX40615, 时间: 1 year ago)

翻回来再看，对模板又有更深入的理解了

```
positive_sentiment = rank(<backfill_op>(<positive_sentiment, days))
```

rank这里是起到数据标准化的作用，是不是也可以扩展到grouping的op

---

### 评论 #5 (作者: WL13229, 时间: 1 year ago)

[HX40615](/hc/en-us/profiles/31695973667607-HX40615)

没错

---

### 评论 #6 (作者: TY67822, 时间: 9 months ago)

sentiment_difference = compare_op(positive_sentiment, negative_sentiment)
compare不止用减法，可以用其他运算方法，更灵活的衡量情绪偏向

---

### 评论 #7 (作者: CS14313, 时间: 9 months ago)

学习了

---

### 评论 #8 (作者: ZJ47021, 时间: 9 months ago)

挺好的

---

### 评论 #9 (作者: KY99488, 时间: 8 months ago)

`positive_sentiment` 表示获取积极情绪的原始数据，相较于其他的数据集，情绪数据覆盖率低，采用ts_back回填确实是个好方法。使用Rank排名运算符框定合理范围内的数据，但是这一操作是如何实现去除原始数据中的噪音的？
按照 250 天的时间范围进行数据回填处理，是否是要考虑整体波动情况，若有较大落差，可以延长或缩短days。
一年内金融交易日大约为250天。
感谢帖主，学到的很多。
===============================行百里者半九十=======================================

---

### 评论 #10 (作者: ZZ26913, 时间: 6 months ago)

这是英文社区中介绍的那个情绪类的Alpha模板！我正在尝试用这类非传统的数据构建信号，这个结构较为清晰。可把compare_op换成ts_corr看看情绪差和未来收益的相关性，也考虑加入其他行业中性化处理。

---

### 评论 #11 (作者: LR70512, 时间: 5 months ago)

还是小白一个，在这里学习到了<backfill_op/>操作符，学习到了数据回填的含义，目前扩展只会再增加一层group操作，如

<group_op/>(< [time_series_operator/>](https://platform.worldquantbrain.com/learn/data-and-operators/operators#time-series-operators) (<positive_sentiment/> - <negative_sentiment/>, <days/>), group)

---

### 评论 #12 (作者: QM70930, 时间: 4 months ago)

我用了这个模板，就是有一个现象是PNL的趋势还可以，但是sharpe这些数据都不是很好，我看PNL曲线的平滑性很差，对于这一类alpha有什么优化的建议吗？

---

