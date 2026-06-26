# Incorporating Volatility into Chinese Market Trades

- **链接**: [Commented] Incorporating Volatility into Chinese Market Trades.md
- **作者**: SA89201
- **发布时间/热度**: 2年前, 得票: 9

## 帖子正文

One of the bronze alpha ideas involved going long on the stocks with low volume in the Chinese market and short on those with high volume. One of the suggestions for improving the alpha suggested incorporating volatility, but I'm not sure which datasets tell us about volatility in the Chinese market (all the obvious volatility ones seem to only exist for the US market). Any help here would be appreciated!

---

## 讨论与评论 (11)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi!

There is an interesting post on the forum about the trade_when operator, please check it out:  [Using trade_when for Event Alphas and Low Turnover Alphas](/hc/en-us/community/posts/8360363631127) 
Additionally, volatility is often measured as: ts_stddev(returns, d).
You can try using ts_rank(ts_stddev(returns, d1), d2)>0.5 as a condition in trade_when to capture periods of high volatility.

Hope it helps!

---

### 评论 #2 (作者: QG16026, 时间: 1年前)

Hi, I don't quite understand why the CHN market needs robust universe return and sharpe backtests? Is there any way to improve these 2 indicators?

---

### 评论 #3 (作者: AC63290, 时间: 1年前)

To incorporate volatility into your Alpha for the Chinese market, consider constructing a proxy for volatility using available datasets. For example:

1. **Price Range:**  Use the daily high-low price range or the difference between the daily open and close as a measure of volatility.
2. **Rolling Standard Deviation:**  Compute the rolling standard deviation of daily returns over a fixed period (e.g., 5 or 10 days) to capture recent volatility trends.
3. **Volume Implied Volatility:**  Analyze the relationship between changes in trading volume and price movements as an indirect indicator of volatility.

These methods can help you approximate volatility even when explicit datasets are unavailable.

---

### 评论 #4 (作者: ND68030, 时间: 1年前)

The Chinese stock market has options trading, such as the  **China Financial Futures Exchange (CFFEX)** , where you can find implied volatility for Chinese stocks and indices. If available, implied volatility from these options can serve as a good proxy for market expectations of volatility.

---

### 评论 #5 (作者: LN78195, 时间: 1年前)

To incorporate volatility into Chinese market trades, consider constructing proxies such as rolling standard deviation of returns, daily high-low price range, or volume-implied volatility. Additionally, explore implied volatility from options on platforms like CFFEX for a more direct measure tailored to the Chinese market. Which approach do you think aligns best with your alpha's objectives?

---

### 评论 #6 (作者: HV77283, 时间: 1年前)

Interesting alpha idea of going long on low-volume stocks and short on high-volume ones in the Chinese market! For volatility data, you might explore local sources or financial platforms specific to China, as many US-focused datasets may not cover it. Any suggestions on regional volatility data would be helpful!

---

### 评论 #7 (作者: AM60509, 时间: 1年前)

In order to introduce volatility into the alpha ,multiply the alpha by rank(ts_stddev(returns,25) or rank (ts_stddev(alpha1,lookback period) where alpha1 is the alpha expression

---

### 评论 #8 (作者: TT55495, 时间: 1年前)

Can you explain why it's essential to focus on robust universe returns and Sharpe ratio backtests in the CHN market? Also, what are some methods to improve the reliability and performance of these indicators in this context?

---

### 评论 #9 (作者: NH84459, 时间: 1年前)

Incorporating  **volatility**  into your alpha strategy for the  **Chinese market**  can be a great improvement, but you're right that most readily available datasets tend to focus on  **US markets** . However, there are  **several datasets and approaches**  specific to the  **Chinese market**  that you can explore.

---

### 评论 #10 (作者: CC40930, 时间: 1年前)

To incorporate volatility in your alpha for the Chinese market, you can calculate it from historical price data using standard deviation or use proxies like price dispersion or moving averages. You might also find volatility data for Chinese indices like the Shanghai Composite or CSI 300 to help.

---

### 评论 #11 (作者: AK52014, 时间: 1年前)

To incorporate volatility into your Chinese market Alpha, use proxies like daily price ranges, rolling standard deviations of returns over periods (e.g., 5–10 days), or volume-price relationships as indirect volatility indicators when explicit datasets are unavailable.

---

