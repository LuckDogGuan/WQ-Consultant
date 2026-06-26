# [BRAIN TIPS] Getting Started with Technical Indicators

- **链接**: [Commented] [BRAIN TIPS] Getting Started with Technical Indicators.md
- **作者**: KA64574
- **发布时间/热度**: 3年前, 得票: 28

## 帖子正文

https://www.youtube.com/embed/40JActnyhkM?start=90&end=287

Technical indicators are heuristic or pattern-based signals based on the price/volume of a financial asset. They can help us make better trading decisions by identifying trends, momentum, support and resistance levels, and other important market signals. Common examples of technical indicators include moving average, Bollinger bands, and relative strength index (RSI).

**What you need to build Technical Indicators**

Recommended Data fields

![图片](images/img_0ea2c72c9b.png)

The data fields are mainly price data (open, close, high, low and vwap) as well as volume data.

![图片](images/img_d422232794.png)

How is VWAP Calculated?

Let’s say for example that during the course of the sessions, 40 stocks are purchased at a price of $118.00, 10 were purchased at $119, 10 at $120, and another 10 at $121 as seen in the table below.

To calculate VWAP, simply multiple the volume and price of each order together and divide it by the volume total.

![图片](images/img_961e3c0214.png)

Recommended Operators

Most of the operators required are arithmetic and time-series operators. For example, a moving average may be calculated using ts_mean. Check out the  [Operators page](https://platform.worldquantbrain.com/learn/data-and-operators/operators)  to learn about their functionalities.

![图片](images/img_09dddcff3c.png)

**Sources of Ideas**

Investopedia is a good place to begin, with a series of 9 articles covering technical indicators. You can check out the first article  [here](https://www.investopedia.com/terms/t/technicalindicator.asp) .

Afterwards, you can check out  [Elearnmarkets](https://www.elearnmarkets.com/blog/best-25-technical-indicators/#17-volume-at-price) , which provides 25 commonly used technical indicators.

Lastly, for more advanced learning, you can visit  [Stockcharts’ ChartSchool](https://school.stockcharts.com/doku.php?id=technical_indicators:moving_averages) , comprising a very comprehensive collection of technical indicators.

**Tips for Technical Indicator Alphas**

Customization: Technical indicators can be customized with different time periods to suit specific trading strategies and objectives. For example, the moving average indicator can be divided into short, medium, long term indicators based on the time period 10 days, 50 days, and 200 days respectively.

Simulation Settings: Using different neutralizations and decay settings can improve the signal of technical indicators through reduction of turnover or increase in returns. Try out each variation and see which is the most effective.

Dealing with Outliers: Outliers represent a fundamental challenge in alpha research, the effect being that weight becomes highly concentrated on a few stocks. If you see the message “Weight is too strongly concentrated” in your IS test results, consider using  **rank** ,  **ts_rank** ,  **zscore**  and  **ts_zscore**  to remove such outliers.

---

## 讨论与评论 (7)

### 评论 #1 (作者: TN48752, 时间: 1年前)

You can integrate commonly used technical indicators such as MA, MACD, RSI into the trade when or if else conditions to enhance the signal.

---

### 评论 #2 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #3 (作者: SK72105, 时间: 1年前)

I would like to add that time-series operators like ts_max_diff, and ts_scale also work well with technical indicators; and often have low correlation

---

### 评论 #4 (作者: TT55495, 时间: 1年前)

I appreciate the detailed explanation of technical indicators and the valuable resources you shared. Your breakdown of VWAP calculation and tips for customization and dealing with outliers will definitely enhance my understanding and approach to trading strategies. I look forward to exploring the suggested sources for deeper learning. Thanks for your contribution!

---

### 评论 #5 (作者: CC40930, 时间: 1年前)

Technical indicators are used to analyze the price and volume of financial assets to identify trends, momentum, support, resistance levels, and other market signals. To build effective technical indicators, you'll need price data (open, close, high, low, and VWAP) and volume data, along with appropriate operators.

---

### 评论 #6 (作者: TD17989, 时间: 1年前)

Technical indicators play a crucial role in technical analysis, helping traders and investors identify potential trends, market conditions, and entry or exit points. These indicators are based on  **price**  and  **volume**  data and can reveal a lot about market sentiment and potential future price movements.

---

### 评论 #7 (作者: CT68712, 时间: 1年前)

Great insights on technical indicators! As a newbie in this space, I find the breakdown of VWAP and its components super helpful. Understanding how volume and price interplay through indicators like moving averages and RSI seems vital for trading strategies. I’m curious about how to effectively customize these indicators for my own trading style. The resources you shared, especially from Investopedia and Stockcharts, will definitely aid my learning process. Looking forward to experimenting with these tools and seeing their impact on my trading outcomes. Appreciate the valuable information!

---

