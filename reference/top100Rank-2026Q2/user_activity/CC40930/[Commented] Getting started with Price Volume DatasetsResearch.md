# Getting started with Price Volume DatasetsResearch

- **链接**: [Commented] Getting started with Price Volume DatasetsResearch.md
- **作者**: Di Sheng Tan
- **发布时间/热度**: 1年前, 得票: 8

## 帖子正文

https://www.youtube.com/embed/40JActnyhkM?start=90&end=287

**Price-Volume Data Definitions:**

- Stock Price is the current price at which a stock can be bought or sold.
  - If there’s high demand for a company’s shares due to favorable factors, the price may increase.
- Opening Price: The price at which a security trades at the opening of an exchange on a given trading day
- Closing Price:  The final price at which a security trades on a given trading day.
- Today's Low:  The lowest price at which a stock trades over the course of the day.
- Today's High: The highest price at which a stock trades over the course of the day.
- Total daily return: Calculated based on the change in a stock’s price from the close of one trading day to the close of the next trading day.
- Volume: Number of shares traded over a period. The Volume-Weighted Average Price (VWAP) is calculated by dividing the total traded value by the total traded shares for the day.
- Daily outstanding shares: total shares held by all shareholders, including institutional investors and company insiders.
- Daily market capitalization: The total dollar market value of a company’s outstanding shares.Dividend: A distribution of a portion of a company’s earnings, decided by the board of directors, paid to a class of its shareholders.

**Some ideas using  [price-volume](https://platform.worldquantbrain.com/data/data-sets?category=pv)  data:**

1. Momentum
   - Following price trend
   - To participate in momentum investing, one would take a long position in an asset that has shown an upward-trending price, or short-sell a security that has been in a downtrend.
   - The basic idea is that once a trend is established, it is more likely to continue in that direction than to move against the trend.
2. Reversal or reversion
   - A reversal is a change in the direction of a price trend, which can be a positive or negative change against the prevailing trend.
   - On a price chart, reversals undergo a recognizable change in the price structure. A reversal is also referred to as a “trend reversal” or a “correction.”
3. Breakout & Volume spike
   - Using technical indicators to predict whether the upcoming trend is whether momentum or reversal.
   - Breakout: Buy a stock when its price moves above a resistance level, or sell when it falls below a support level, with the expectation that the price will continue moving in that direction.
   - Volume Spike: Monitor for significant increases in trading volume, as these spikes can indicate the beginning of a new trend or a potential reversal.

**Recommended Datasets:**

- [Price Volume Data for Equity](https://platform.worldquantbrain.com/data/data-sets/pv1)
- [Market Microstructure Data](https://platform.worldquantbrain.com/data/data-sets/pv104)
- [VWAP Tick Data](https://platform.worldquantbrain.com/data/data-sets/pv141)
- [Aggregated dataset](https://platform.worldquantbrain.com/data/data-sets/pv87)

---

## 讨论与评论 (17)

### 评论 #1 (作者: JO65057, 时间: 1年前)

yes the price volume must be consider within the company

---

### 评论 #2 (作者: CC40930, 时间: 1年前)

This post provides an excellent overview of how price and volume data can be used to develop trading strategies based on momentum, reversals, and breakouts. The definitions of stock price metrics like opening/closing price, low/high, and volume give a solid foundation for understanding market movements.

---

### 评论 #3 (作者: TN48752, 时间: 1年前)

You can refer to paper 101 formal alpha, which suggests many templates that use data pv effectively, but you need to pay attention to reducing turnover.

---

### 评论 #4 (作者: deleted user, 时间: 1年前)

- **Definition** : The  **current price**  at which a stock can be bought or sold. It fluctuates based on market demand and supply.
- **Significance** : This is the most basic and widely followed metric. It reflects the  **market's perception**  of the value of the company and can be used to track  **price trends**  and identify  **buy or sell signals** .
- **Application** : Used in momentum or mean reversion models,  **price signals**  can indicate the direction of future price movements.

---

### 评论 #5 (作者: CC40930, 时间: 1年前)

Great overview of price-volume data and how it can be applied to various strategies like momentum, reversals, and breakouts! I’m particularly interested in using volume spikes and VWAP to help confirm potential trend changes. These strategies sound like they could lead to some really insightful alpha generation. I'll be sure to experiment with these datasets!

---

### 评论 #6 (作者: TN48752, 时间: 1年前)

VWAP is the average price a stock has traded at throughout the day, weighted by volume. It helps traders understand the average price based on the size of trades, making it a useful measure for assessing trends.

---

### 评论 #7 (作者: CS12450, 时间: 1年前)

To get started with Price-Volume Datasets, focus on understanding key price and volume metrics, such as opening/closing prices, daily highs/lows, total returns, and trading volume. These can be used to analyze trends and predict market behavior. Key strategies include:

- **Momentum** : Follow stocks with an upward price trend or short-sell those in a downtrend.
- **Reversal** : Identify price changes that signal a shift in trend direction.
- **Breakouts & Volume Spikes** : Use technical indicators to predict whether a trend will continue or reverse. Look for volume spikes to spot new trends.

Recommended datasets include Price-Volume Data, Market Microstructure Data, VWAP Tick Data, and Aggregated datasets to enhance analysis.

---

### 评论 #8 (作者: NT63388, 时间: 1年前)

A comprehensive post for beginners.

Previously, with the PV set, I usually focused on PV1. 
I will try it on the three datasets pv104, pv141, and pv87.

---

### 评论 #9 (作者: NH84459, 时间: 1年前)

The strategy is simple:  **buy assets in uptrends**  (long positions) and  **short-sell assets in downtrends** . The expectation is that trends have momentum and, therefore, the prices will continue to move in the same direction.

---

### 评论 #10 (作者: TP14664, 时间: 1年前)

**Reversal**  refers to a change in the direction of a price trend. It can be either positive (bullish) or negative (bearish) and goes against the prevailing trend. A reversal is a significant shift in market sentiment, often after a prolonged uptrend or downtrend. On a price chart, it manifests as a recognizable pattern, such as a price moving from an uptrend to a downtrend or vice versa. Reversals can be seen as corrections or trend reversals, and they might indicate the end of a prevailing trend.

---

### 评论 #11 (作者: PL15523, 时间: 1年前)

The combination of breakout and volume spikes is a powerful strategy! Both rely on the idea that significant price movements, especially when accompanied by increased volume, are likely to lead to a continuation of the trend or, in some cases, a reversal.

---

### 评论 #12 (作者: SC43474, 时间: 1年前)

This is an insightful overview of leveraging price-volume datasets for trading strategies. A key addition to these ideas could be analyzing the relationship between price gaps (open-to-close or close-to-open) and volume spikes, which often signal market sentiment shifts. Combining this with intraday VWAP deviations can provide actionable insights for identifying potential breakout or reversal scenarios. Exploring these patterns in datasets like PV1 or VWAP Tick Data could reveal nuanced opportunities for alpha generation.

---

### 评论 #13 (作者: SG25281, 时间: 1年前)

Volume-Weighted Average Price helps traders understand the average price based on the size of trades, making it a useful measure for assessing trends. A reversal is a significant shift in market sentiment, often after a prolonged uptrend or downtrend.

---

### 评论 #14 (作者: SG25281, 时间: 1年前)

Reversals can be seen as corrections or trend reversals, and they can signal the end of a prevailing trend. This is a practical overview of leveraging price-volume datasets for trading strategies. I will definitely be experimenting with these datasets!

---

### 评论 #15 (作者: PT27687, 时间: 1年前)

This post provides a clear introduction to understanding price-volume datasets and their implications in trading strategies. The differentiation between terms like opening and closing prices brings clarity for beginners. I'm curious about your thoughts on how the average investor could effectively use the VWAP in daily trading decisions. Could you share any practical examples?

---

### 评论 #16 (作者: RB98150, 时间: 1年前)

This is a solid breakdown of price-volume data and its applications in trading strategies!

If you're refining  **Alphas**  using PV data, consider:

- **Momentum** : Use rolling returns, VWAP trends, or price breakout confirmations.
- **Mean Reversion** : Apply Z-score normalization, Bollinger Bands, or VWAP deviations.
- **Volume Analysis** : High relative volume spikes may confirm breakouts or reversals.

---

### 评论 #17 (作者: SD14148, 时间: 7个月前)

学到了
价格 - 交易量数据涵盖股票价格、开盘价、收盘价、高低价、每日总回报、交易量、VWAP、每日流通股数、每日市值及股息等定义。利用这些数据有以下投资思路：动量投资，跟随价格走势，对上升趋势资产持多头，下降趋势证券卖空；逆转或回归，关注价格趋势方向变化；突破和成交量飙升，借助技术指标预测趋势，突破阻力位买入、跌破支撑位卖出，监控成交量飙升以判断新趋势或逆转。

感谢大佬

---

