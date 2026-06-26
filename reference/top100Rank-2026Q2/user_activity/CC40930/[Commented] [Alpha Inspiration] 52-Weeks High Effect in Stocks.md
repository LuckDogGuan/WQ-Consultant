# [Alpha Inspiration] 52-Weeks High Effect in Stocks

- **链接**: [Commented] [Alpha Inspiration] 52-Weeks High Effect in Stocks.md
- **作者**: DH18707
- **发布时间/热度**: 2年前, 得票: 5

## 帖子正文

**Paper:**  Industry Information and the 52-Week High Effect

**Authors:**  Hong, Jordan, Liu

**Link** :  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1787378](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1787378)

The “52-week high effect” states that stocks with prices close to the 52-week highs have better subsequent returns than stocks with prices far from the 52-week highs. Investors use the 52-week high as an “anchor” against which they value stocks. When stock prices are near the 52-week high, investors are unwilling to bid the price all the way to the fundamental value. As a result, investors under-react when stock prices approach the 52-week high, and this creates a 52-week high effect.

This effect could be enhanced with a strategy using a narrower investment universe and buying stocks in industries in which stock prices are close to 52-week highs. The strategy is related to  [the momentum effect](https://quantpedia.com/calendar-seasonal-trading-and-momentum-factor/) , but research shows it is independent of it. The strategy should not be implemented in January as it has negative results in this month (like momentum). Most of the gains for  [the long-short version](https://quantpedia.com/strategies/short-interest-effect-long-short-version/)  are from long positions, which makes the “52-week high effect” easier to implement in real-world trading.

Academics speculate that this effect is connected to “adjustment and anchoring bias”. Anchoring is a psychological bias that says that people start with an implicitly suggested reference point (the “anchor” -> 52-week high in our example) and then make incremental adjustments based on additional information. The financial paper says that traders use the 52-week high as a reference point in which they evaluate the potential impact of news. When good news has pushed a stock’s price near or to a new 52-week high, traders are reluctant to bid the price of the stock higher even if the information warrants it. The information eventually prevails, and the price moves up, resulting in a continuation. It works similarly for 52-week lows.

Alpha idea: The ratio between the current price and 52-week high is calculated for each stock at the end of each month (PRILAG i,t = Price i,t / 52-Week High i,t). Every month, the investor then calculates the weighted average of ratios (PRILAG i,t) from all firms in each industry (20 industries are used), where the weight is the market capitalization of the stock at the end of the month t. The winners (losers) are stocks in the six industries with the highest (lowest) weighted averages of PRILAGi,t. The investor buys stocks in the winner portfolio and shorts stocks in the loser portfolio and holds them for three months. Stocks are weighted equally, and the portfolio is rebalanced monthly (which means that 1/3 of the portfolio is rebalanced each month).

**Dataset:**  pv1

---

## 讨论与评论 (7)

### 评论 #1 (作者: TN67143, 时间: 2年前)

Hi,

Thank you for your summary. Very interesting articles.

Can us look at the following interpretation of this ideas in the following ways.

First of all, we have PRILAGi,t = price/ts_max(price, 252), where price can be high, low, open, close or vwap.

Then, we multiply them with cap to achieve element-wise multiplication.

What do you think about this formula?

Let's discuss.

Thank you!

---

### 评论 #2 (作者: AR51656, 时间: 2年前)

Hi, are you getting good results from that formula? I am not getting that good signals

---

### 评论 #3 (作者: TN67143, 时间: 2年前)

Hi,

Great comments!

May be we would need to look at this idea deeper to come up with the suitable process to create a quality Alphas. Could we adjust them in the following way?

1. Key ideas: 
The author find that stock prices near their 52-week high is seen as a positive predictor of future stock returns. Whereas in reality, they are seen by investors as a negative signal (by price reversion assumption). This creates an opportunities to create an Alphas based on this unexplored finding.

2. Key index: 
To capture this finding, the author defines an index: PRILAGi,t = price_i,t/52_week_high(price_i,t). 0 <= PRILAGi,t <= 1. The higher PRILAGi,t, the closer the stock prices are to their 52-week high.

3. Additional information:
The authors then calculate the weighted average of PRILAG, with the weights are their market capitalization, yielding cap*PRILAGi,t

4. Grouping:
The authors use Industry grouping: group_operator(cap*PRILAGi,t) = group_operator(cap*price/ts_max(price, 252)).

5. Rebalance and recalculating in time horizon: 
This is quite difficult to realized by a suitable formula. Let's open for discussion.

6. Long/short position:
Long the stocks with the highest calculated index, and short the stocks with the lowest calculated index. Meaning the sign is +. We shall use the formula: group_operator(cap*price/ts_max(price, 252)).

Let's try it out and discuss!

Thanks!

---

### 评论 #4 (作者: CC40930, 时间: 1年前)

The "52-week high effect" offers an interesting perspective on how investor behavior and psychological biases influence stock price movements. By focusing on industries where stocks are close to their 52-week highs, the strategy effectively captures the delayed reaction to information, as described in the paper. The use of market capitalization-weighted averages of the price-to-52-week high ratio within each industry further refines the strategy, allowing it to capitalize on underreactions while avoiding the pitfalls of general market momentum. Rebalancing monthly and holding positions for three months can potentially generate consistent alpha by exploiting this market inefficiency.

---

### 评论 #5 (作者: NH84459, 时间: 1年前)

- **Buy the Winners** : From the 6 industries with the highest weighted averages of PRILAG, select the stocks and  **buy**  them.
- **Short the Losers** : From the 6 industries with the lowest weighted averages of PRILAG, select the stocks and  **short**  them.
- Stocks within each portfolio (winners and losers) are  **equally weighted** , meaning that each stock in the winner and loser portfolios contributes the same amount to the portfolio, regardless of its market capitalization.

---

### 评论 #6 (作者: TD17989, 时间: 1年前)

The  **"52-week high effect"**  is an intriguing phenomenon observed in the stock market. It suggests that stocks whose prices are close to their 52-week highs tend to have better subsequent returns than stocks that are far from their 52-week highs. The theory behind this effect is based on  **investor behavior**  and how they use the 52-week high as an "anchor" for valuing stocks.

###

---

### 评论 #7 (作者: CC40930, 时间: 1年前)

This is an interesting take on the 52-week high effect, and I really like how it incorporates industry-specific factors. The idea of weighting stocks by market cap and rebalancing monthly seems like a smart way to capture momentum without overexposing to any single stock. Excited to see how this performs in practice!

---

