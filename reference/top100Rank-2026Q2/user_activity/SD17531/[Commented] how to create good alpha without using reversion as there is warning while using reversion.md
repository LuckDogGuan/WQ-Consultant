# how to create good alpha without using reversion as there is warning while using reversion.

- **链接**: [Commented] how to create good alpha without using reversion as there is warning while using reversion.md
- **作者**: BS20926
- **发布时间/热度**: 1年前, 得票: 2

## 帖子正文

What should I use in place of the Reversion rank(-ts_delta(close,2)) to avoid the warning of non-acceptance of alpha includes reversion?

---

## 讨论与评论 (31)

### 评论 #1 (作者: TN48752, 时间: 1年前)

If you want to replace  `Reversion(rank(-ts_delta(close,2)))`  to avoid the warning about non-acceptance of alpha that includes reversion, you need to modify your factor so that it does not explicitly involve reversion-based logic.

---

### 评论 #2 (作者: ND68030, 时间: 1年前)

Define the event window around the earnings announcement to capture short-term post-announcement price movements. A typical window might include several days before and after the earnings announcement, such as (-5 days to +30 days).

---

### 评论 #3 (作者: SM14025, 时间: 1年前)

You should avoid using Reversion rank(-ts_delta(close,2)) because it is quite easy to make alpha using Reversion components .And if you are using this you will only ensure daily payout you will not get  good weight .

---

### 评论 #4 (作者: AJ93287, 时间: 1年前)

I think this was introduced to dissuade users from adding a reversion component to their alphas in order to make them pass the various submission tests.  The trouble with such an approach is that it concentrates the risk of the overall portfolio with respect to the short-term reversion risk factor.  If the performance of that factor is poor, all the alphas that were boosted will perform badly at the same time.

---

### 评论 #5 (作者: GS53807, 时间: 1年前)

This is an interesting discussion! It seems like the key issue with reversion-based alphas is that they might artificially pass validation tests but fail in real trading due to high correlation with short-term mean reversion risks. A good way to replace reversion logic is to use factors like trend strength, breakout strategies, or volume-based signals. For example, a simple moving average crossover strategy (where you compare short-term and long-term moving averages) could be a solid alternative.

---

### 评论 #6 (作者: NP85445, 时间: 1年前)

shift your focus to momentum and trend-based signals. For instance, rather than using rank(-ts_delta(close,2)), consider a moving average crossover—comparing short-term and long-term averages—to capture genuine trend shifts. Complement this with volume filters to ensure liquidity and reduce noise. This approach avoids the pitfalls of reversion logic while aiming for robust, sustainable OS performance.

---

### 评论 #7 (作者: WX16829, 时间: 1年前)

you can try to Incorporate Additional Factors

- **Fundamental Data** : Combine price data with fundamental metrics such as earnings growth, cash flow, or other financial ratios. For example,  `ts_rank(earnings_growth * ts_delta(close, 2), 250)`  can provide a more comprehensive signal.
- **Technical Indicators** : Use technical indicators like moving averages, RSI (Relative Strength Index), or MACD (Moving Average Convergence Divergence) to enhance the signal. For example,  `ts_rank(ts_ma(close, 250) - close, 250)`  can capture mean-reversion without direct ranking reversal.

---

### 评论 #8 (作者: SD17531, 时间: 1年前)

Hello brother,

I saw your Q4 alpha submissions and simulations records on other posts. I am really curious—how do you manage to generate one submittable alpha for every roughly 120 simulations ? Could you please share in detail how you discover alphas? 

Thank you.

---

### 评论 #9 (作者: AG20578, 时间: 1年前)

Hi  [BS20926](/hc/en-us/profiles/13099795770903-BS20926) !

This is just a warning, it still allows you to submit alphas with reversion component.

I just want to note, that it is not necessary to use rank(-ts_delta(close,2)) or close or returns in alphas to find a submittable alpha.

On the webinars and advisory sessions you can find new ideas to explore. Do not hesitate to connect with your advisor.

---

### 评论 #10 (作者: TN48752, 时间: 1年前)

**K-means** : This would allow you to group alphas into clusters based on similarity, then compute pairwise correlations within each cluster to understand the internal relationship of the alphas in each group.

---

### 评论 #11 (作者: TD17989, 时间: 1年前)

- **Exponential Decay Weighting:**  Instead of sharp weight adjustments, gradually decay positions over time.
- **Adaptive Holding Periods:**  Use dynamic holding periods based on liquidity and volatility to avoid unnecessary rebalancing.
- **Trade Cost Optimization:**  Incorporate trade cost constraints into your optimizer to prioritize high-return trades with minimal cost.

---

### 评论 #12 (作者: ND68030, 时间: 1年前)

- **Quickly Identify Profitable Factors**
  - Use  `sharpe>0`  to find factors that are consistently profitable.
  - Rank factors by Sharpe ratio to prioritize the strongest ones.
- **Detect and Remove Losing Factors**
  - Apply  `sharpe<0`  to identify underperforming factors that may be hurting your portfolio.
  - Investigate why these factors are failing—bad data, overfitting, or poor market conditions?

---

### 评论 #13 (作者: MA97359, 时间: 1年前)

Hi  [BS20926](/hc/en-us/profiles/13099795770903-BS20926) ,

It seems that you've been relying heavily on reversion-based factors in your Alphas. While reversion strategies can deliver strong performance, they are not the only way to build high-performing Alphas. To enhance your strategy and reduce over-reliance on a single approach, start exploring other datasets and methodologies.

Consider building Alphas based on:

- **Fundamentals**  (e.g., valuation ratios, earnings quality)
- **Earnings & Event-Driven Factors**  (e.g., earnings surprises, corporate actions)
- **News & Sentiment-Based Alphas**  (e.g., media sentiment, analyst reports)
- **Momentum-Driven Signals**  (e.g., trend-following, relative strength)

Diversifying your approach will not only reduce strategy correlation but also open new opportunities for generating unique and resilient Alphas. Keep experimenting and refining!

---

### 评论 #14 (作者: NH84459, 时间: 1年前)

**Choose Variables for Alpha Creation:**  For D0 decay, you should look at  **short-term**  data or events that have an immediate and fast impact on market movements. Examples include  **earnings announcements, sudden market movements, or significant changes in regulatory policies** .

---

### 评论 #15 (作者: PP87148, 时间: 1年前)

Avoid direct ranking of -ts_delta(close, N), as it explicitly signals reversion, in place of this momentum, relative strength, volume confirmation, or volatility-based signals.

---

### 评论 #16 (作者: AC63290, 时间: 1年前)

Here are some alternative approaches to replace the reversion signal rank(-ts_delta(close,2)) while avoiding the reversion warning:

1. Use momentum-based signals:

```
rank(ts_returns(close, 2))  # Forward-looking momentum

```

1. Try volume-weighted approaches:

```
rank(ts_corr(volume, close, 10))  # Volume-price correlation

```

1. Use more complex transformations:

```
rank(ts_std(close, 10) / ts_mean(close, 10))  # Volatility-adjusted signal

```

These alternatives maintain signal quality while avoiding direct reversion patterns that might trigger warnings.

---

### 评论 #17 (作者: QG16026, 时间: 1年前)

Your input is incredibly valuable as I work on refining my strategy and ensuring my alphas remain robust without triggering the reversion alert. I’m excited to test these alternatives and see how they perform in live conditions. Thanks again for your guidance and support

---

### 评论 #18 (作者: GN51437, 时间: 1年前)

I think this was meant to discourage adding a reversion component to alphas just to pass tests. The issue is it increases short-term reversion risk, so if that factor underperforms, all boosted alphas will perform poorly together.

---

### 评论 #19 (作者: CT68712, 时间: 1年前)

Hey there! I totally get your concern about avoiding reversion in your alpha strategies. As a former professional athlete turned quant trader, I've learned the hard way how risky relying on mean reversion can be, especially when it comes to real-market conditions. Have you considered focusing on momentum-based signals instead? For instance, implementing strategies like moving average crossovers or correlating volume with price movements might pave the way for robust, non-reversion dependent signals. This could help you steer clear of those pesky warnings while enhancing your alpha's performance. Keep experimenting and refining your approach; it sounds like you're on an exciting path!

---

### 评论 #20 (作者: CT68712, 时间: 1年前)

Hey BS20926! I'm also trying to navigate the challenges of alpha creation without incorporating reversion. As a tech enthusiast diving into quantitative trading, I can relate! Instead of relying on rank(-ts_delta(close,2)), have you considered using metrics based on momentum or breakout strategies? For example, implementing moving average crossovers could lead to more consistent performance while minimizing risk associated with reversion. By analyzing trend strength and volume indicators, we might find surprisingly effective alternatives. Let's keep exploring and sharing ideas in the community—it's super exciting to see what insights we can gather!

---

### 评论 #21 (作者: BS20926, 时间: 1年前)

HI AC63290

thanks for sharing the alternative approaches to replace the reversion signal rank(-ts_delta(close,2)) while avoiding the reversion warning.

---

### 评论 #22 (作者: HN71281, 时间: 1年前)

- To avoid reversion-based logic, consider momentum, trend-following, or liquidity-based factors. Signals like moving average crossovers, volume surges, or order book imbalances can help generate strong alphas.

---

### 评论 #23 (作者: AS16039, 时间: 1年前)

To avoid reversion-based signals like  `rank(-ts_delta(close,2))` , consider momentum-based alternatives:

1. **Trend-Following** :  `rank(ts_returns(close, 2))`  for short-term momentum.
2. **Breakout Detection** :  `rank(ts_max(close, 20) - close)`  to capture new highs.
3. **Volume Confirmation** :  `rank(ts_corr(close, volume, 10))`  to validate trends.
4. **Volatility-Based** :  `rank(ts_std(close, 10) / ts_mean(close, 10))`  for regime shifts.

---

### 评论 #24 (作者: NS94943, 时间: 1年前)

Hi  [BS20926](/hc/en-us/profiles/13099795770903-BS20926) ,

I agree with  [AJ93287](/hc/en-us/profiles/7940329062423-AJ93287) .

It is quite easy to make any alpha submittable by adding a reversion component to it, so in the past too many such signals have been submitted, leading to reversion and crowding risks. It is advisable to submit only a small percentage of reversion signals every quarter to minimize such risks. Also, using expressions like   *rank(-ts_delta(close,2))*  increases turnover significantly, which is not required to make the alpha submittable. Like others have suggested, use other types of signal like momentum.

Thanks!

---

### 评论 #25 (作者: LK29993, 时间: 1年前)

Hi  [BS20926](/hc/en-us/profiles/13099795770903-BS20926) !

The warning for reversion alphas will not stop you from submitting the alpha. However, it is highly recommended that you submit alphas that do not include the reversion factor. You can find other new ideas by reading research papers, exploring datasets on BRAIN, and visiting the community forum! Some best practices are:

- Avoid submitting alphas based on widely-known factors
- Avoid combining multiple signals into a single alpha

---

### 评论 #26 (作者: PT27687, 时间: 1年前)

It sounds like you're facing some challenges with your alpha strategy. Have you considered exploring trend-following indicators or momentum-based metrics as alternatives to reversion? They could potentially provide you with the results you're looking for without the warnings. Would love to hear your thoughts on this!

---

### 评论 #27 (作者: TP19085, 时间: 1年前)

This change likely discourages users from adding reversion components just to pass submission tests. The issue is that such an approach increases exposure to short-term reversion risk—if that factor underperforms, all boosted alphas suffer simultaneously.

A better alternative is shifting towards  **momentum and trend-based signals**  instead of relying on reversion logic. Strategies like  **trend strength, breakout signals, or volume-based indicators**  can provide more sustainable performance. For example, using a  **moving average crossover** —comparing short-term and long-term moving averages—helps capture real trend shifts.

Instead of  **rank(-ts_delta(close,2))** , consider a moving average crossover, complemented with  **volume filters**  to ensure liquidity and reduce noise. This method enhances robustness while avoiding the pitfalls of reversion-based alphas.

---

### 评论 #28 (作者: VN28696, 时间: 1年前)

To avoid reversion warnings, try  **momentum-based signals**  like  `ts_rank(ts_delta(close, 5))` ,  **volatility-adjusted signals**  using  `ts_zscore` , or  **sector-relative rankings**  with  `group_rank(ts_mean(close, 10), sector)` . Mixing fundamentals can also help.

---

### 评论 #29 (作者: NA18223, 时间: 1年前)

seems like the key issue with reversion-based alphas is that they might artificially pass validation tests but fail in real trading due to high correlation with short-term mean reversion risks. A good way to replace reversion logic is to use factors like trend strength, breakout strategies, or volume-based signals.

---

### 评论 #30 (作者: AK40989, 时间: 1年前)

To create a robust alpha without relying on reversion-based logic, consider focusing on momentum and trend-following signals. For instance, using a moving average crossover strategy can effectively capture genuine trend shifts without triggering reversion warnings. Additionally, incorporating volume-based indicators or breakout detection can enhance your alpha's performance.

---

### 评论 #31 (作者: DK30003, 时间: 1年前)

It seems that you've been relying heavily on reversion-based factors in your Alphas. While reversion strategies can deliver strong performance, they are not the only way to build high-performing Alphas. To enhance your strategy and reduce over-reliance on a single approach, start exploring other datasets and methodologies.

---

