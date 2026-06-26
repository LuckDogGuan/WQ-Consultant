# [BRAIN TIPS] Momentum Alphas

- **链接**: [Commented] [BRAIN TIPS] Momentum Alphas.md
- **作者**: NL41370
- **发布时间/热度**: 3年前, 得票: 5

## 帖子正文

Momentum alpha captures short-term consistent trends and exits your position when there is a momentum shift. As a reminder, if there is bullish sentiment around the overall market, the majority of stocks will show good performances and if there is bearish sentiment overall, the opposite is true.

The alphas we build on the BRAIN platform are set to long-short neutral setting. It is harder to capture momentum signals in this setting compared to long-only alphas because if all the stocks are doing well, chances are you will take losses in the long-short neutral setting as you will be shorting some stocks.

Here are some examples of the same momentum alpha’s IS summaries with/without neutralization settings.

![image](images/img_9340d70733.png)

###### 

However, there are still ways to capture momentum signals.

In order to do that, sophisticated risk controls must be taken into account. This implies that momentum alphas perform well when the stock is less volatile.

Try initiating with trade_when operator or conditional operator to create an expression to specify entry expression or conditional expression to capture the momentum in your alphas. High volatility represents fluctuation on the stock price and thus fits more on reversion alphas.

As for the recommendation on datasets, market volatility can be captured when using datasets from “Systematic Risk Metrics”. News dataset and sentiment datasets can also be some excellent ways to capture momentum shift.

Lastly, try liquid universe like TOP500 when building your momentum alphas. Evidence shows that there is negative correlation between liquidity risk and momentum strategies  *(Asness, 2009)* .

---

## 讨论与评论 (8)

### 评论 #1 (作者: AS24040, 时间: 2年前)

Can you please tell the alpha for which this result has happened

---

### 评论 #2 (作者: NL41370, 时间: 2年前)

Hi,

Please refer to some of Alpha examples here, including "Momentum after news" Alphas  [⭐ Alpha Examples for Beginners | WorldQuant BRAIN](https://platform.worldquantbrain.com/learn/documentation/create-alphas/19-alpha-examples)

---

### 评论 #3 (作者: AM60509, 时间: 1年前)

In order to introduce momentum factor into the alpha expression,add alpha=alpha+ts_delta(alpha,lookbackperiod) into the model

---

### 评论 #4 (作者: CC40930, 时间: 1年前)

Momentum alphas are designed to capture short-term trends and exit positions when momentum shifts occur. In a long-short neutral setting, these alphas can be challenging, as shorting some stocks during a bullish market can lead to losses. To improve momentum capture, consider using risk controls and conditional operators like trade_when to specify entry points. High volatility often aligns with reversion strategies, while lower volatility suits momentum. Utilizing datasets like “Systematic Risk Metrics,” news, and sentiment data can further capture momentum shifts. Focusing on liquid universes like TOP500 can also enhance performance, given the negative correlation between liquidity risk and momentum strategies.

---

### 评论 #5 (作者: TD17989, 时间: 1年前)

In a  **long-only**  setting, you would be long on stocks that show strong momentum, meaning you're betting that the stocks will continue to rise. This is the typical momentum strategy that works well in a  **bullish**  market where most stocks are expected to perform well.

---

### 评论 #6 (作者: TT55495, 时间: 1年前)

Thank you for sharing this insightful explanation on capturing momentum trends. I appreciate the emphasis on using sophisticated risk controls and the tips for dataset selection. Your insights on market volatility and liquidity risk are especially valuable.

---

### 评论 #7 (作者: PN39025, 时间: 1年前)

Momentum Alpha is a strategy that follows short-term price trends, profiting from upward or downward movements, and exits when momentum reverses. It works well in trending markets but faces challenges in capturing signals when market sentiment is unclear.

On the BRAIN platform, alphas use a long-short neutral approach, balancing buy and sell positions to stay market-neutral. While this reduces market risk, it makes momentum harder to capture—especially in bullish markets where short positions can lead to losses as most stocks rise.

Thanks to everyone who contributed to researching this! 😊

---

### 评论 #8 (作者: QG16026, 时间: 1年前)

I appreciate the emphasis on using sophisticated risk controls and the recommendations for selecting appropriate datasets. Your points about market volatility, liquidity risk, and the challenges of capturing momentum in a long-short neutral setting are especially valuable. This is a great guide for building momentum alphas in different market conditions. Thank you

---

