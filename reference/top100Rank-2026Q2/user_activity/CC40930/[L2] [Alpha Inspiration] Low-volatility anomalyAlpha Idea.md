# [Alpha Inspiration] Low-volatility anomalyAlpha Idea

- **链接**: [L2] [Alpha Inspiration] Low-volatility anomalyAlpha Idea.md
- **作者**: TN63138
- **发布时间/热度**: 2年前, 得票: 21

## 帖子正文

**Paper:**  The Volatility Effect: Lower Risk Without Lower Return

**Authors:** Blitz, Vliet

**Link:**  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=980865](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=980865)

**Main idea:**

The Efficient Market Theory has been challenged by the finding that relatively simple anomalies can be utilized to construct trading strategies, that are found to generate statistically significant higher returns than those of the market portfolio. There is also a second possibility where the Market efficiency is also challenged if some simple investment strategy generates a comparable return to that of the market but at a systematically lower level of risk. Well known strategies that challenge efficiency are Momentum, Size, and Value, but a large amount of research has been made about volatility effect in stocks. Low-risk stocks exhibit significantly higher risk-adjusted returns than the market portfolio, while high-risk stocks significantly underperform on a risk-adjusted basis. Authors Clarke, de Silva, and Thorley have found that minimum variance portfolios, based on the 1000 largest U.S. stocks over the years 1968-2005, achieve a volatility reduction of about 25% while delivering comparable or even higher average returns than the benchmark market portfolio. This paper has found that portfolios, which consist of stocks with the lowest historical volatility, are associated with Sharpe ratio improvements, that are even larger than those in the aforementioned minimum variance portfolios. Baker, Bradley, and Wurgler in their work: Benchmarks as Limits to Arbitrage: Understanding the Low Volatility Anomaly, have proved that over the past 41 years, high volatility and high beta stocks have substantially underperformed low volatility and low beta stocks in U.S. markets. Clearly, there is a lot of evidence that the low-volatility effect is an anomaly that works and should be utilized in an investing strategy. Concentrating on long-term volatility, the anomaly can be used by the investor to create decile portfolios that are based on a straightforward ranking of stocks on their historical return volatility. Afterward, the investor would simply long the decile with the stocks with the lowest volatility (moreover, he can short the decile of stocks with the highest volatility). Going long on low-risk stocks and short on high-risk stocks produce a significant volatility spread. However, a long-short portfolio isn’t the only way to exploit this anomaly. A long-only strategy is much easier to implement than a long-short strategy. The investor could go long on low volatility stocks and enjoy the higher Sharpe ratio rather than standard equity indices.

Firstly, to take full advantage of the attractive absolute returns of low-risk stocks, there is a need for leverage. However, in practice, either many investors are not allowed, or they are unwilling to apply leverage, especially the leverage needed for exploiting the volatility effect. This results in the fact that the opportunity, which is presented by low-risk stocks, cannot be easily arbitraged away. Secondly, the volatility effect could be the result of an inefficient and decentralized investment approach. The problem of benchmark driven investing is that asset managers have an incentive to tilt towards high beta or high volatility stocks. This is a relatively simple way for every asset manager to generate returns above the average if he assumes that the CAPM at least partially holds. This results in overpriced high-risk stocks, while low-risk stocks may become under-priced; this is particularly consistent with the return patterns which were documented in this paper. The volatility effect may also be caused by behavioral biases among private investors. Private investors will overpay for risky stocks that are perceived to be similar to lottery tickets because they are in the search for high returns in an as short time as possible. Additionally, Li, Sullivan, and García-Feijóo in their paper, The Low-Volatility Anomaly: Market Evidence on Systematic Risk versus Mispricing, have found out that the anomaly returns associated low-volatility stocks can be attributed to market mispricing or compensation for higher systematic risk. Soe, in “The low-volatility effect: A comprehensive look“, claims that volatility-effect challenges the traditional equilibrium asset pricing theory that an asset’s expected return is directly proportional to its beta or systematic risk, or, in other words, higher-risk securities should be rewarded with higher expected returns while lower-risk assets receive lower expected returns. The evidence seems to be endless. Moreover, the volatility effect is similar in size compared to classic effects (momentum, size, and value) and remains significant after Fama-French adjustments and double sorts. Last but not least, concentrating on long-term, past three years, volatility implies a much lower portfolio turnover.

**Implementation**

At the end of each month, the investor constructs equally weighted decile portfolios by ranking the stocks on the past three-year volatility of weekly returns. The investor goes long stocks in the top decile (stocks with the lowest volatility).

**Related dataset:**

**Term**

**Data field**

**Dataset**

returns

returns

                               Price volume data for equity

20-day volume standard deviation 
                                      mdl175_02dtsv
                               China Fundamentals and Technicals Model

Liquidity-turnover beta                 mdl175_tbot                                     China Fundamentals and Technicals Model

PnL

![图片](images/img_dbb9463508.png)

![图片](images/img_eca5c85149.png)

**Comments and questions:**

In general, the Chinese market has the potential to generate very strong signals, but it is necessary to pay attention to the backtest robust sharpness and returns, as well as high correlation. Is there any way to overcome these situations? Thank you everyone.

---

## 讨论与评论 (13)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi! Thanks for sharing your insights 🌺

It's interesting to see how low-risk stocks can yield higher risk-adjusted returns compared to the market portfolio. The proposed ideas, such as leveraging low-volatility stocks, offer interesting approaches to this.

When it comes to robust universe tests for the CHN Alpha, there might be a few challenges. Here's why:

The Chinese market has limited short-selling mechanisms, making it hard to short most stocks directly. Additionally, China enforces a price limit mechanism. Given these unique aspects of the Chinese market, we've designed a robust universe tests for the CHN Region (similar to the Sub-universe test for the USA Region). Check out the Learn article for more info:  [China Alphas: Understand the market](https://platform.worldquantbrain.com/learn/documentation/advanced-topics/china-region) .

If your Alpha fails this test in the CHN Region, it typically means that a majority of your Alpha's returns (over 60%) originate from stocks that may lack liquidity. Or, it could indicate that the weight is excessively concentrated in certain stocks. Of course, there might be various other factors leading to test failure.

You could potentially improve this by using two main methods. Firstly, try to even out your position weights using operators like rank(), hump(), clamp(), etc. Secondly, consider revisiting your Alpha implementation and modify it to ensure its robustness across various stocks. This could involve revising the size of buckets, changing conditions, and so on. As for the issue of high correlation - it usually surfaces when you overuse the same idea. Try to diversify the fields you use - there's a lot of volatility-related fields available in the  [China Fundamentals and Technicals Model](https://platform.worldquantbrain.com/data/search/data-fields?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&search=volatility&universe=TOP3000)  dataset.

Keep pushing boundaries, exploring new ideas, and refining your Alphas. Remember, every challenge is a stepping stone to success. You're doing a great job! ✨⭐

---

### 评论 #2 (作者: ZY82137, 时间: 2年前)

Hi, I am having trouble computing weekly returns using fast expressions, could you give me a hint on what operators to use?

---

### 评论 #3 (作者: AG20578, 时间: 2年前)

Hi! Daily returns are ts_delta(close, 1) / ts_delay(close, 1). So, to compute weekly returns you can use ts_delta(close, 5) / ts_delay(close, 5).

Another way is to use ts_product(returns+1, 5) - 1 (but it is not recommended for large amount of days).

Or exp(ts_sum(log(returns+1), 5)) - 1.

Also you can use  [ts_returns operator](https://platform.worldquantbrain.com/learn/data-and-operators/detailed-operator-descriptions#ts_returns-x-d-mode-1) .

---

### 评论 #4 (作者: XL31477, 时间: 1年前)

Hey, dude. To overcome those issues in the Chinese market, first, for backtest robust sharpness and returns, increase the sample size of data used in backtesting and consider different market periods. Also, stress test your strategy under various scenarios. Regarding high correlation, diversify your factors or strategies. For example, combine low-volatility with other uncorrelated factors like value or momentum. This might help reduce the impact of high correlation and make the overall performance more stable.

---

### 评论 #5 (作者: XD81759, 时间: 1年前)

Hey! When it comes to the Chinese market's issues you mentioned, for backtest robustness, you can try different time periods and market conditions for testing. As for sharpness and returns, optimizing your factor weights might help. Regarding high correlation, diversifying your factors can reduce it. For example, add some non - volatility - related factors. And it's always good to cross - validate your results with different datasets.

---

### 评论 #6 (作者: CC40930, 时间: 1年前)

The low-volatility effect is a fascinating anomaly that challenges traditional financial theory. As demonstrated, low-risk stocks tend to outperform high-risk ones in terms of risk-adjusted returns, highlighting a potential strategy for enhancing portfolio returns with less volatility. The idea of leveraging this effect, despite the practical challenges of implementing leverage, could be a key strategy for risk-conscious investors. Moreover, the behavioral and market inefficiencies that drive this anomaly are intriguing, offering an opportunity for investors to exploit mispricing. This low-volatility strategy’s potential in reducing risk while maintaining strong returns makes it an essential consideration for long-term investors.

---

### 评论 #7 (作者: KS69567, 时间: 1年前)

The Volatility Effect demonstrates that low-volatility stocks often achieve better risk-adjusted returns than their high-volatility counterparts, defying the conventional risk-return tradeoff principle. Behavioural biases, such as overconfidence and a preference for high-risk "lottery-like" stocks, contribute to the mis pricing of high-volatility assets. Additionally, institutional constraints and speculative trading pressures further reduce the returns of high-risk stocks. By leveraging the Volatility Effect, investors can build portfolios that offer stable and competitive returns with reduced risk. However, this strategy may underperform in bull markets, and its effectiveness varies across market conditions, making it essential to adapt strategies based on prevailing dynamics.

---

### 评论 #8 (作者: PP87148, 时间: 1年前)

It's fascinating to explore how low-risk stocks can generate higher risk-adjusted returns than the market portfolio. Leveraging low-volatility stocks is certainly an intriguing approach worth considering.

However, implementing robust universe tests for CHN Alpha presents unique challenges:

- The Chinese market has limited short-selling options, making it difficult to short most stocks directly.
- A strict price limit mechanism further complicates trading dynamics.

To address this, we've designed robust universe tests specifically for the CHN Region, similar to those for the USA. More details are available in the Learn article:  *China Alphas: Understand the Market.*

If your Alpha fails this test, it often means over 60% of returns stem from illiquid stocks or overly concentrated weights. To improve, try two strategies:

1. Balance position weights using operators like rank(), hump(), or clamp().
2. Refine your Alpha's logic, adjusting bucket sizes, conditions, or diversifying fields to reduce correlation.

---

### 评论 #9 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #10 (作者: TT55495, 时间: 1年前)

Thank you for sharing this detailed summary of the "Volatility Effect: Lower Risk Without Lower Return" paper. How would the low-volatility anomaly work with different risk tolerance profiles, and how can we adjust portfolio weights based on risk preferences?

---

### 评论 #11 (作者: QG16026, 时间: 1年前)

How can strategies leveraging the Volatility Effect be adjusted to suit different risk tolerance profiles, and what methods can be used to rebalance portfolio weights based on investors' risk preferences? Thank you so much for your sharing.

---

### 评论 #12 (作者: AK98027, 时间: 1年前)

The low-volatility effect is a fascinating anomaly that challenges traditional financial theory. As demonstrated, low-risk stocks tend to outperform high-risk ones in terms of risk-adjusted returns, highlighting a potential strategy for enhancing portfolio returns with less volatility. The idea of leveraging this effect, despite the practical challenges of implementing leverage, could be a key strategy for risk-conscious investors. Moreover, the behavioral and market inefficiencies that drive this anomaly are intriguing, offering an opportunity for investors to exploit mispricing. This low-volatility strategy’s potential in reducing risk while maintaining strong returns makes it an essential consideration for long-term investors.

---

### 评论 #13 (作者: KK81152, 时间: 1年前)

### 1.  **Identify Low-Volatility Stocks** :

- **Data Needed** : Use historical  **weekly return data**  for stocks to calculate their  **volatility**  over the past 3 years.
- **Ranking** : At the end of each month, rank all stocks based on their  **volatility** . Stocks with the  **lowest volatility**  (least price fluctuation) should be placed in the  **top decile** .

### 2.  **Construct the Portfolio** :

- **Long Position** : Invest in the  **top decile**  of stocks with the  **lowest volatility** . These are your "low-risk" stocks.
- **Rebalancing** : Every month, repeat the process—rank stocks based on 3-year volatility and adjust your portfolio by going long on the lowest volatility stocks.

### 3.  **Use of Data** :

- **Returns** : Use stock  **price data**  to calculate returns.
- **Volume and Liquidity** : Include  **volume standard deviation**  and  **liquidity-turnover beta**  from datasets (like "China Fundamentals and Technicals Model") to further refine stock selection.

### 4.  **Leverage (Optional)** :

- To enhance returns, you might consider  **leveraging**  your positions in low-volatility stocks. However, this depends on whether leverage is allowed or suitable for your risk tolerance.

### 5.  **Avoid Overcomplication** :

- Instead of a complicated long-short strategy, a  **long-only**  position in low-volatility stocks can deliver strong, risk-adjusted returns.

### Summary:

- **Rank stocks by volatility**  (3-year history) and  **long the least volatile**  ones.
- **Monthly rebalancing**  and simple portfolio management.
- **Leverage**  can be considered, but a long-only strategy is easier to implement.

---

