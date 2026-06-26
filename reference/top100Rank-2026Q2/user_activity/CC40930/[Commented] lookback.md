# lookback

- **链接**: [Commented] lookback.md
- **作者**: AS76594
- **发布时间/热度**: 2年前, 得票: 2

## 帖子正文

what is look back period?

how to set(or change) look back period ?

---

## 讨论与评论 (6)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi!

Check out  [Time Series Operators](https://platform.worldquantbrain.com/learn/data-and-operators/operators#time-series-operators)

Example:

last_diff_value(x, d)

Returns last x value not equal to current x value from last d days

d here is a lookback period (look back days parameter)

---

### 评论 #2 (作者: DP11917, 时间: 1年前)

I would like to ask in the documentation, the operator section mentions that lookback should not be set > 502, why is that? Will a lookback that is too long seriously degrade the signal? I hope to get an answer.

---

### 评论 #3 (作者: QG16026, 时间: 1年前)

I realize some insights and lookbacks, it is related to the frequency of the data, for example fundamental data should have a lookback of 60 or more because financial reports are usually updated quarterly, not daily.

---

### 评论 #4 (作者: CC40930, 时间: 1年前)

The "look-back period" refers to the historical time frame used to analyze or measure a particular data point or financial metric. In the context of quantitative trading or financial analysis, it's often used to calculate moving averages, volatility, returns, or other technical indicators.

---

### 评论 #5 (作者: TP14664, 时间: 1年前)

It seems you're looking into  **Time Series Operators** , which are commonly used in time series analysis, particularly in the context of financial data, to perform operations on time-indexed data.

---

### 评论 #6 (作者: ND68030, 时间: 1年前)

A  **look back period**  is a specific timeframe used to analyze past data to make informed decisions or predictions about future events. The concept of a look back period is applied across various fields, including finance, trading, statistics, and software development. Understanding and appropriately setting the look back period is crucial for accurate analysis and effective decision-making.

---

