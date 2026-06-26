# [Alpha Inspiration] Overnight Trading Sentiment and Arbitrage

- **链接**: [Commented] [Alpha Inspiration] Overnight Trading Sentiment and Arbitrage.md
- **作者**: YJ28691
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

#### 

#### Idea

Overnight Trading Sentiment and Arbitrage

#### Overview

There may be a clear distinction between investors who lead overnight trading and those who lead daytime trading. Generally, relatively professional institutional investors and experts prefer to trade during the daytime. In contrast, a higher proportion of short-term traders is seen during overnight trading. There can also be significant differences in the efficiency between overnight and daytime trading.

According to some new research, many stocks and investment portfolios exhibit certain trading patterns during daily cycles. Two entirely different investor groups dominate overnight and daytime trading, and the trading logic of these two groups can be characterized as "sentiment trading."

During the price correction process, institutional investors may over-adjust. In other words, some efficient trades overnight may be distorted due to mispricing noise caused by excessive adjustments. Such mispricing may lead to errors in stock prices, but these tend to recover in the future.

#### Factors

The research report proposes four factors: NR, PR, ABNR, and ABPR.

- **RET_OC** : Daytime increase
- **RET_CO** : Overnight increase
- **NR** : The number of times there is an opposing direction during the daytime within the month / The actual number of trading days in the month
- **PR** : The number of times there is a reversal in the same direction within the month / The actual number of trading days in the month
- **ABNR** : The NR average of the month / The NR average of the past n months
- **ABPR** : The PR of the month / The PR average of the past n months

Daytime reversals in the opposite direction are cases where  **RET_OC > 0**  and  **RET_CO < 0** , while overnight reversals in the opposite direction are cases where  **RET_OC < 0**  and  **RET_CO > 0** .

I combined two factors,  **NR**  (reversal factor) and  **PR**  (momentum factor), to test them on the  **CHN Top3000** . Initially, a one-month time window (22 days) was used in the research. However, by using a four-month event window (90 days), I found that the performance of the factors improved.

#### Alpha Expression

ret_oc = close/open-1;

ret_co = open/ts_delay(close, 1) -1;

NR = ts_sum(ret_co>0 && ret_oc<0?1:0,90)/90;

PR = ts_sum(ret_co<0 && ret_oc>0?1:0,90)/90;

group = bucket(rank(cap), range='0,1,0.1');

group_neutralize(rank(NR) +rank(-PR),densify( group))

![图片](images/img_80ce1d8aef.png)

---

## 讨论与评论 (21)

### 评论 #1 (作者: AG20578, 时间: 1年前)

Hi YJ28691!

Thank you for sharing, this is most helpful!

---

### 评论 #2 (作者: YJ28691, 时间: 1年前)

YJ28691, I submitted my first alpha reading your article! Thank you!

---

### 评论 #3 (作者: CH36668, 时间: 1年前)

Thank you for sharing this insightful and innovative idea! The thoughtful use of NR and PR factors, along with the extended event window, provides a fresh perspective on trading dynamics. This framework is a valuable contribution to understanding and leveraging sentiment-driven patterns—much appreciated!

---

### 评论 #4 (作者: AM71073, 时间: 1年前)

This is a fascinating idea! The concept of  **overnight vs. daytime trading sentiment**  and the impact of institutional versus short-term traders is something I've been thinking about too. The four factors you've proposed— **NR** ,  **PR** ,  **ABNR** , and  **ABPR** —are great at capturing the dynamics between market corrections and price recovery.

I like how you've tested the  **NR and PR factors**  on the CHN Top3000 with a longer 90-day window, which seems to capture the effect better than just using the 22-day window. This makes sense because market sentiment can sometimes take longer to play out.

Also, your  **alpha expression**  looks like a solid approach to detect the relationship between overnight and daytime price changes. Using  **group_neutralize**  with the  **rank(NR) + rank(-PR)**  combination could really help in controlling for sector or market group effects.

It would be interesting to see if the  **performance of this alpha**  holds across different market cycles or regions. Looking forward to hearing about your results, and would love to hear if you run any further tests on this!

---

### 评论 #5 (作者: SS63636, 时间: 1年前)

This is an insightful exploration of the dynamics between overnight and daytime trading behaviors, and I find the distinction between sentiment-driven overnight trading and institution-dominated daytime trading particularly compelling.

The combination of the NR (reversal factor) and PR (momentum factor) in your analysis is intriguing, especially with the observed performance improvement when shifting to a longer event window (90 days). It suggests that extending the observation period might capture more nuanced patterns, potentially smoothing out noise and emphasizing reliable alpha signals.

The methodology you've shared—utilizing metrics like RET_OC, RET_CO, and group-neutralized factors—provides a robust framework for understanding mispricing opportunities. It also aligns well with the notion that sentiment-induced inefficiencies may recover over time, presenting arbitrage potential.

A couple of thoughts:

1. Have you tested the sensitivity of your alpha to different bucket ranges or neutralization techniques?
2. It might be interesting to layer additional factors like sector-specific behavior or volatility to further refine the alpha expression.

Overall, this is a thought-provoking approach to leveraging time series dynamics for alpha generation. Thanks for sharing!

---

### 评论 #6 (作者: PM26052, 时间: 1年前)

This is an interesting approach to exploring the dynamics of overnight trading sentiment and its relationship with arbitrage opportunities. The idea of differentiating between institutional investors who dominate daytime trading and short-term traders who are more active during overnight sessions makes sense, especially when you consider the role of sentiment and trading patterns in each session.

One thing to consider is whether this strategy might benefit from additional filtering or refinement based on liquidity or volatility measures, as arbitrage opportunities can sometimes be more pronounced in certain market conditions.

Overall, this looks like a promising avenue to explore further, and I would be interested to see how the model performs with different regional datasets or across different market conditions. Would love to hear more about your findings as you continue refining the strategy!

---

### 评论 #7 (作者: PN39025, 时间: 1年前)

Thanks for your post I think this is an interesting idea. There are events that cause the psychology of overnight traders to fluctuate quite a bit

---

### 评论 #8 (作者: SK14400, 时间: 1年前)

This idea captures the inefficiencies that arise from sentiment and over-adjustments, especially during the transitions between overnight and daytime trading. It’s fascinating to see how factors like NR (reversal) and PR (momentum) can quantify these behaviors, paving the way for more targeted alpha strategies. Such models could be especially impactful when combined with sectoral or regional variations, as mispricing might exhibit unique patterns across markets.

The alpha expression you've provided adds a strong quantitative element to the discussion, making it actionable and testable.

**Question for Further Exploration:** 
How could combining sentiment data from alternative sources (e.g., news or social media) enhance the predictive power of these reversal and momentum factors?

---

### 评论 #9 (作者: NS94943, 时间: 1年前)

Thank you  [YJ28691](/hc/en-us/profiles/17412068778135-YJ28691)  for this great post on using PV data for overnight trading and arbitrage. Will certainly try your approach in CHN region!

---

### 评论 #10 (作者: SC43474, 时间: 1年前)

This is a very thought-provoking approach to leveraging the differences between overnight and daytime trading behaviors. The use of NR and PR factors to capture sentiment-driven patterns is quite innovative, especially with the extended 90-day window for a better understanding of market cycles. I agree that the distinction between institutional versus short-term trader influence is crucial in identifying potential mispricing opportunities.

It would be interesting to explore how the approach performs during extreme market conditions, like market crashes or rapid rebounds. Additionally, incorporating real-time sentiment data from news or social media could offer additional predictive power for these trading patterns. Looking forward to seeing more results and refinements from your strategy!

---

### 评论 #11 (作者: TN48752, 时间: 1年前)

Thanks for sharing your alpha idea. May I ask why you added -1 to RET_OC and RET_CO. Also why do you need /90, it seems like removing /90 doesn't affect the alpha result.

---

### 评论 #12 (作者: PN39025, 时间: 1年前)

Yesterday I read your article and got the same idea as your implementation I have done alpha with sharpe 2.0 performance in CHN market.

---

### 评论 #13 (作者: DN41247, 时间: 1年前)

Thank you for sharing this fascinating insight! The idea of distinguishing between overnight and daytime trading sentiment is compelling, and the use of NR and PR factors adds a unique perspective. I appreciate the detailed explanation and your testing approach with extended event windows—very inspiring!

---

### 评论 #14 (作者: AS34048, 时间: 1年前)

Overnight trading and arbitrage opportunities arise from price movements and sentiment-driven market dynamics occurring when major exchanges are closed. Understanding and exploiting these phenomena requires analyzing sentiment, global news, and market inefficiencies. **Overnight sentiment**  refers to market expectations shaped by events and information released after regular trading hours. It impacts the opening prices of assets and intraday volatility.

---

### 评论 #15 (作者: VS18359, 时间: 1年前)

Hi,
Overnight trading sentiment reflects the market’s mood or reaction to events that happen outside regular trading hours, like news, earnings, or global developments, which can influence how markets open the next day. Arbitrage is when traders profit from price differences for the same asset in different markets, like buying a stock cheaper in one market and selling it higher in another, helping balance prices across markets.

---

### 评论 #16 (作者: TD84322, 时间: 1年前)

Thank you, everyone, for your thoughtful comments and valuable insights! I truly appreciate the time and effort you all put into analyzing and discussing this idea. Your feedback and suggestions have given me new perspectives and exciting directions to explore further. It’s inspiring to see how this concept resonates with so many of you, and I look forward to sharing updates as I continue refining this strategy. Thanks again for the support!

---

### 评论 #17 (作者: LK29993, 时间: 1年前)

Hi TN48752!

The -1 is used to shift the expression value to zero when close = open for ret_oc, or when open = ts_delay(close,1) for ret_co. This is so that the expression value will only be positive if there is a daytime or overnight increase. 

We divide by 90 to get the average value after summing up the values for the past 90 days using the ts_sum operator. We will end up with a ratio rather than an absolute number, making it more comparable.

---

### 评论 #18 (作者: YC82708, 时间: 1年前)

This article presents an intriguing approach to understanding the dynamics of overnight trading sentiment and arbitrage. The distinction between institutional investors and short-term traders leading different parts of the trading day is insightful. The research suggests that the "sentiment trading" logic of these two groups leads to inefficiencies, particularly during price corrections.

The factors introduced—NR (Reversal factor) and PR (Momentum factor)—are useful for capturing the dynamics between daytime and overnight trading. The adjustment to a four-month event window instead of just one month, which improved factor performance, emphasizes the importance of testing over longer time periods for more reliable results. The alpha expression presented shows a combination of momentum and reversal signals and their neutralization using a grouping method, making it a solid framework for constructing trading strategies based on these factors.

This strategy could be particularly beneficial for developing models that capitalize on the inefficiencies in overnight pricing, helping to identify opportunities where the market may correct itself during the day.

---

### 评论 #19 (作者: CC40930, 时间: 1年前)

This is an intriguing concept! The distinction between overnight and daytime trading sentiment highlights unique opportunities for arbitrage and mispricing correction. The idea that overnight trading may introduce "sentiment-driven noise" due to mispricing by short-term traders contrasts well with the more calculated strategies of daytime institutional investors. Incorporating signals derived from overnight price adjustments and their subsequent corrections could lead to actionable Alpha insights. Exploring patterns like overnight returns relative to intraday recovery could further refine strategies. Have you considered specific operators or datasets that align with this approach? Would love to hear more!

---

### 评论 #20 (作者: PT27687, 时间: 1年前)

This analysis brings forward an intriguing perspective on the dynamics of overnight versus daytime trading, especially with the sentiment-driven approach you've outlined. I find the differentiation between institutional and short-term traders quite compelling. Could you elaborate on how these trading patterns influence overall market behavior? It's fascinating to think about the implications of such insights on trading strategies!

---

### 评论 #21 (作者: DK30003, 时间: 1年前)

One thing to consider is whether this strategy might benefit from additional filtering or refinement based on liquidity or volatility measures, as arbitrage opportunities can sometimes be more pronounced in certain market conditions.

---

