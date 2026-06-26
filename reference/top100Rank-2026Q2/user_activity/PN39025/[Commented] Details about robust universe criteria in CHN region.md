# Details about "robust universe" criteria in CHN region

- **链接**: [Commented] Details about robust universe criteria in CHN region.md
- **作者**: AP86495
- **发布时间/热度**: 3年前, 得票: 13

## 帖子正文

Hello. Please clarify what are the "robust universe sharpe" and "robust universe returns" in the CHN region. How are these calculated?

---

## 讨论与评论 (12)

### 评论 #1 (作者: WL13229, 时间: 3年前)

Thanks for the question.

Robust universe is a universe constructed based on the specificities of Chinese market and robust universe test is an additional test for the specificities, such as the constrains of short-selling mechanisms and price limit system. Robust universe test simulates alphas in an environment that is closer to the real time trading and evaluate your alpha performance more realistically.

For robust test, you need to keep at least 40% performance when compared with your original Alpha. In terms of how to improve your Alpha, we can start from the fact that the smaller the capital or the less liquid an instrument is, the more difficult to trade it on the Chinese market. If your Alpha trade more liquid or larger capital instruments, it's less likely to be affected in the robust universe test.  Imagine if your Alpha makes profit on shorting the stocks that can't not be shorted in the real market, it's naturally the performance will degrade on the robust universe. Different datasets have different adaption towards the mechanism of Chinese market, for example fundamental datasets tends to make profit by positioning weights on a lower turnover, which may mitigate the effects of shorting constrain comparing to price-volume datasets.

---

### 评论 #2 (作者: PP31783, 时间: 3年前)

Please elaborate with an example. It is the theoretical solution. Please provide some practical insight.

---

### 评论 #3 (作者: WL13229, 时间: 3年前)

To take care of the special trading rules in CHN Region, you could take account into the market restriction in your Alpha. For example, for price limit policy, you can use if_else() operator to modify your Alpha.

Example:

```
if_else(abs(returns)<0.1,alpha,nan)
```

---

### 评论 #4 (作者: GL74043, 时间: 3年前)

How can I check trading day's returns if I set delay==1?

If I use abs(returns) < 0.1, I actually check the price limit of the day before the trading day, which can't prevent trading stocks that reach price limits during the backtesting.

---

### 评论 #5 (作者: WL13229, 时间: 3年前)

Thanks for this following up question. In this case, try out some Vector data to calculate the return at the market open time. For example  [pv27_as_dq_preclose](https://platform.worldquantbrain.com/data/data-sets/pv27/data-fields/pv27_as_dq_preclose)  (it refers to the preclose price of the stock.) and  [pv27_as_dq_open](https://platform.worldquantbrain.com/data/data-sets/pv27/data-fields/pv27_as_dq_open)  (it refers to the open price of the stock.)

---

### 评论 #6 (作者: PP55193, 时间: 2年前)

can we have a look on the shape of dataframe ?

---

### 评论 #7 (作者: XL31477, 时间: 1年前)

**Hey,  [PP55193](/hc/en-us/profiles/23422193000343-PP55193) . To check the shape of a dataframe, it usually depends on the programming language or platform you're using. In Python with libraries like pandas, you can use the 'shape' attribute. For example, if your dataframe is named 'df', then 'df.shape' will give you a tuple showing the number of rows and columns. In Brain platform, there might be specific functions or ways in the data exploration section to view its structure. Hope this helps you get an idea about the dataframe shape.**

---

### 评论 #8 (作者: DK20528, 时间: 1年前)

Robust Universe Sharpe" and "Robust Universe Returns" are performance metrics used to assess the effectiveness of alpha strategies in the financial markets, including in the CHN region. Here's a breakdown of what these terms typically refer to and how they are calculated:

### 1.  **Robust Universe Sharpe**

- **Definition** : The "Robust Universe Sharpe" is a modified version of the Sharpe ratio that applies to a broader universe of assets or stocks in a given region (e.g., CHN region). It aims to measure the risk-adjusted returns of a strategy while ensuring that the calculation is robust, meaning it accounts for potential outliers or extreme values that might distort the typical Sharpe ratio calculation.
- **Calculation** :
  - **Sharpe Ratio**  is calculated as the ratio of the excess return (the return above a risk-free rate) to the standard deviation (volatility) of those returns: Sharpe Ratio=Rportfolio−Rrisk-freeσportfolio\text{Sharpe Ratio} = \frac{R_{\text{portfolio}} - R_{\text{risk-free}}}{\sigma_{\text{portfolio}}}Sharpe Ratio=σportfolio​Rportfolio​−Rrisk-free​​
  - **Robust Universe Sharpe**  might modify this formula by using a more stable measure of volatility (e.g., using trimmed means or other robust estimators to handle extreme outliers) or adjusting for various market conditions, such as those specific to the CHN region. This ensures that the Sharpe ratio doesn't overestimate the risk-adjusted returns in cases where extreme values or outliers skew the calculation.

### 2.  **Robust Universe Returns**

- **Definition** : "Robust Universe Returns" refer to the returns of a broad set of assets in the CHN region, typically representing a large pool of stocks or financial instruments. The term "robust" implies that the returns are calculated in a way that minimizes the impact of extreme market movements or outliers, ensuring a more stable and realistic measure of returns over time.
- **Calculation** :
  - **Returns Calculation** : This can be the simple average or cumulative returns across the universe of assets, considering factors like price changes, dividends, and other relevant financial metrics.
  - **Robust Calculation Method** : Similar to the robust Sharpe, robust universe returns may use methods like median-based or trimmed mean calculations to avoid the influence of extreme data points or market shocks. This could be useful in markets like China, where volatility can sometimes cause skewed data points.

### Key Differences:

- **Traditional Sharpe/Returns** : In typical calculations, the Sharpe ratio and returns would be based on raw data (i.e., simple average returns and standard deviation of those returns).
- **Robust Versions** : The "robust" versions of these metrics apply adjustments to reduce the impact of outliers and market anomalies, providing a more reliable measure of the strategy’s performance, especially in volatile or non-linear markets such as those in the CHN region.

### Example:

Let’s say you are calculating the "Robust Universe Sharpe" for a set of Chinese stocks in your universe:

1. **Calculate Excess Returns** : Subtract the risk-free rate (e.g., 10-year Chinese government bond yield) from each stock's return.
2. **Adjust for Outliers** : Instead of using the raw standard deviation, apply a robust volatility measure, like median absolute deviation (MAD), to account for any extreme market movements (for example, sudden regulatory changes or geopolitical events).
3. **Compute Sharpe Ratio** : Use the adjusted volatility in the Sharpe formula to compute a more stable risk-adjusted return.

### Why It’s Important in CHN Region:

- The Chinese stock market can be subject to higher volatility and government-driven changes compared to Western markets, so using robust metrics helps prevent overestimating the effectiveness of strategies that may be sensitive to those outliers or sharp market shifts.
- This method provides a clearer picture of performance by smoothing out the noise caused by extraordinary events or non-normal price distributions.

In summary, the "Robust Universe Sharpe" and "Robust Universe Returns" metrics help improve the stability and reliability of performance evaluations by adjusting for outliers and extreme data points, which is especially useful when working with more volatile and unpredictable markets like the CHN region.

---

### 评论 #9 (作者: RK48711, 时间: 1年前)

Thank you for the thorough breakdown of 'Robust Universe Sharpe' and 'Robust Universe Returns'! It’s insightful to see how these metrics address the unique challenges posed by the CHN region's market conditions. The use of robust measures to minimize the impact of outliers and extreme values makes these metrics particularly valuable in volatile environments.

I appreciate the clarity on their calculation and the emphasis on adjustments like trimmed means and MAD. This nuanced approach seems essential for deriving realistic performance assessments, especially in markets prone to non-linear dynamics and regulatory influences.

Would you be open to sharing any specific examples or datasets where these metrics have been successfully applied? It’d be interesting to see their practical impact in real-world scenarios

---

### 评论 #10 (作者: MK58212, 时间: 1年前)

This explanation effectively highlights the importance of robust metrics like "Robust Universe Sharpe" and "Robust Universe Returns" for evaluating performance in volatile markets, such as the CHN region. By accounting for outliers and extreme market movements, these metrics provide more reliable, risk-adjusted insights into strategy effectiveness, addressing the unique challenges of such markets.

---

### 评论 #11 (作者: BA51127, 时间: 1年前)

**Understanding Robust Universe** : The robust universe is a tailored universe that considers the unique aspects of the Chinese market, such as trading constraints and price limits. It aims to simulate a more realistic trading environment to evaluate alpha performance.
 **Performance in Robust Universe** : To pass a robust universe test, an alpha must maintain at least 40% of its original performance. This test is crucial for identifying strategies that may perform well in backtesting but fail to account for real-market constraints, such as the inability to short certain stocks.
 **Practical Implementation and Improvements** : Practical advice includes considering market restrictions within alpha models. For instance, using the  `if_else()`  operator to account for price limits can help alphas perform more realistically under robust universe conditions. Additionally, understanding the impact of different datasets on the Chinese market's mechanisms can help mitigate the effects of shorting constraints.

---

### 评论 #12 (作者: PN39025, 时间: 1年前)

In a robust universe test, your alpha should retain at least 40% of its original performance. To improve your alpha’s robustness, consider the fact that trading less liquid instruments or those with smaller capital in the Chinese market is more challenging. For example, if your alpha relies on shorting stocks that cannot be shorted due to market restrictions, it will naturally underperform in a robust universe.

---

