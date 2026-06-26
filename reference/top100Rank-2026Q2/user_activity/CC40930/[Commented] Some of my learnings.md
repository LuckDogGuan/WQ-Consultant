# Some of my learnings

- **链接**: [Commented] Some of my learnings.md
- **作者**: RP25658
- **发布时间/热度**: 2年前, 得票: 66

## 帖子正文

I have been using BRAIN platform from last 10 to 15 days now, I would like to share some of my learnings which might help newly joined users to start creating profitable alphas.

- After achieving min sharpe and fitness, improve returns

- consider using rank, ts_rank, zscore and ts_zscore to remove outliers

- Momentum Alphas
    - BRAIN platform are set to long-short neutral setting, makes it harder to capture momentum signal compared to long-only alphas
    - Use trade_when() or conditional operators
    - Set neutralization to "None"
    - Less volatile stocks perform well in momentum Alphas
    - Use liquid universe like TOP500
    - Volatility can be captured when using datasets from “Systematic Risk Metrics”

- Using hump operation
    - Each instrument could have a variable threshold based on liquidity/market-cap/volatility of the stock
    - Can use single threshold value for a group (subindustry/sector/custom group).
    - Increasing the threshold values either uniformly or not uniformly after ranking the instruments on the basis of a few factors (market-cap/volatility) can help.

- Evaluating new datasets
    - Simulate the below expression in “None” neutralization and decay 0 setting
    - datafield

- Weight Test Failure
    - Test is ought to fail when number of stocks is < 10
    - Use rank(), group_rank(), zscore, scale to handle the outliers
    - Use ts_backfill() or group_backfill() to increase the number of tradable stocks

- Alpha Development Cycle
    - Alpha idea → Finding operators and data → Simulate → Revise

- Working on News Dataset
    - trade_when(ed, alpha, exit)
    - ed: event detection, identify the day on which news related to that stock is occurring (by checking NaN)
    - alpha: position can be taken based on percent change after news
    - holding: can hold for remaining days
    - Example: news_tot_ticks, news_pct_5_min,-1, news_tot_ticks is non-NaN when news has occurred
    - NOTE: There are different ways for event detection, alpha and exit (like decaying alpha or setting threshold)

- Setting predetermined Stop loss
    - Exiting at 10% profit or loss
    - close_at_event = trade_when(event, close, -1);
    - alpha = trade_when(event, signal, abs(close - close_at_event) / close > .1);
    - alpha

- How to increase returns?
    - increase volatility of your alpha
    - work with smaller universe
    - increase turnover
    - try using news and analyst datasets

- Alpha signal smoothing
    - smoothing means lessen effects of extreme values
    - Transformational Operators: arc_tan, tanh, log, s_log_1p, sigmoid
    - Cross sectional Operators: zscore, rank
    - Time series Operators: ts_mean(alpha, N), ts_decay_linear...

- Move out of COMFORT ZONE
    - Working with the same data fields will not get you value adding alphas
    - Explore new datasets

- Creating Delay-0 Alphas
    - Use D0 data fields when using news or sentiment dataset
    - D0 works good for smaller universe (TOP500)
    - D0 works well for low turnover alphas; using fundamental or analyst dataset

- Reduce correlation
    - Use different operators
    - Use different grouping
    - Use alternative operators like high/open/low instead of close

- How to get Higher Sharpe?
    - Increase returns
    - Reduce volatility

- Day count
    - 22 is one month
    - 66 is one quarter
    - 264 is one year

- Trading top or bottom quintile/decile improves performance
    - rank(alpha) >= 0.8 ? 1 : (rank(alpha) <= 0.2 ? -1 : 0)
    - Buy top 20% and sell bottom 20%
    - You may have to increase the universe to pass the "Weight Test"

- Trading volume (liquidity) is average turnover
    - turnover = volume / sharesout

- Use ts_mean() or ts_sum() to reduce turnover when using a volatile data field

- To increase turnover you can add below expression depending on the situation
    > rank(mdf_pgn) or 
    > rank(-mdf_pgn)

- When not able to pass sharpe or fitness test due to marginal difference
    > Use ts_mean instead of ts_sum and vice versa

*This would be a developing list, will keep this updated as I learn more from this platform*

---

## 讨论与评论 (17)

### 评论 #1 (作者: SD87674, 时间: 2年前)

Are none neutralisation alphas allowed becuase in the documentation is written that we should use none only when there is group neutralise in our alpha.

---

### 评论 #2 (作者: AG20578, 时间: 2年前)

Hi! check out this article  [Why is it not recommended to submit "Neutralization = None" alphas?](/hc/en-us/articles/13306223024151-Why-is-it-not-recommended-to-submit-Neutralization-None-alphas-)

Even if your alpha has group_neutralize - submit it with 'market'. 'Market' neutralization in settings should not make your group_neutralize alpha unsubmittable.

---

### 评论 #3 (作者: TT24714, 时间: 2年前)

are these two "event" the same event? or it means event 1 and event 2?

- Setting predetermined Stop loss
    - Exiting at 10% profit or loss
    - close_at_event = trade_when(event, close, -1);
    - alpha = trade_when(event, signal, abs(close - close_at_event) / close > .1);
    - alpha

---

### 评论 #4 (作者: AG20578, 时间: 2年前)

Hi! Yes, it is the same event.

---

### 评论 #5 (作者: HK83363, 时间: 2年前)

👍🤝🥂

---

### 评论 #6 (作者: TS90367, 时间: 2年前)

Hi whats the code for exiting "Exiting at 10% profit or loss"?

---

### 评论 #7 (作者: AT56452, 时间: 1年前)

You shouldn't use none neutralisation at all. It hurts your OS performance even if it does alright in IS. Risk neutralised alphas always do better. There are many articles on this in the learn section and on the forum. Go through those to understand the mechanics better.

---

### 评论 #8 (作者: BA51127, 时间: 1年前)

It's great to see your proactive approach to experimenting with different strategies and techniques to enhance alpha performance.

Regarding the question from TS90367 about the code for exiting at a 10% profit or loss, here's a simplified explanation of how you might set that up:

plaintext

```
close_at_event = trade_when(event, close, -1);
alpha = trade_when(event, signal, abs(close - close_at_event) / close > 0.1);
alpha
```

In this code snippet,  `event`  is a condition that triggers a trade,  `close`  is the closing price, and  `signal`  is your alpha signal. The  `trade_when`  function is used to generate trades based on the event condition. When the price moves more than 10% from the  `close_at_event` , the trade is executed.

---

### 评论 #9 (作者: AM60509, 时间: 1年前)

In my opinion, it is easier to create alphas in lesser known regions like China, Taiwan, Korea as compared to USA due to correlation factor. So I suggest start with fundamental datasets like price volume, model, fundamental metric in these regions.

---

### 评论 #10 (作者: DK20528, 时间: 1年前)

This is an insightful and well-organized list of learnings that can be extremely helpful for beginners in alpha development on the BRAIN platform. You've covered a wide range of strategies and tips, from using smoothing operators to handling news data and volatility.

A few points I'd like to clarify:

1. Could you elaborate on how to handle "news_tot_ticks" in event detection for different stock types or industries?
2. When using "trade_when()" with news datasets, how do you decide the appropriate exit strategy after the news event?
3. In the context of reducing correlation, how do you suggest managing the trade-off between reducing correlation and maintaining sufficient alpha strength?

Looking forward to your updates and further insights!

---

### 评论 #11 (作者: RK48711, 时间: 1年前)

1. This comprehensive guide is invaluable for beginners in alpha development on the BRAIN platform, covering key strategies like smoothing operators, news data handling, and volatility. Clarifications: managing "news_tot_ticks" across stocks, determining exit strategies with "trade_when()", and balancing reduced correlation with alpha strength. Looking forward to more insights!

---

### 评论 #12 (作者: AM60509, 时间: 1年前)

[DK20528](/hc/en-us/profiles/24602396283031-DK20528)

Use operators which can substitute each other without decreasing performance. zscore, quantile, rank, scale can be used interchangeably with minor changes to performance but drastic reduction of correlation drastically. Use of different grouping fields can also reduce correlation

---

### 评论 #13 (作者: XL31477, 时间: 1年前)

**Hey  [DK20528](/hc/en-us/profiles/24602396283031-DK20528) , for handling "news_tot_ticks" in event detection, you can check its NaN values to spot news occurrence days for different stocks. When using "trade_when()" with news datasets, exit strategies can vary like setting a fixed time or based on price changes. For managing the correlation-alpha strength trade-off, use different operators like zscore, rank etc. interchangeably and different grouping fields. That helps reduce correlation while keeping alpha's power to an extent.**

---

### 评论 #14 (作者: DN45758, 时间: 1年前)

[AG20578](/hc/en-us/profiles/12243980162327-AG20578)   Thank you!

The recommendation to avoid submitting "Neutralization = None" alphas is primarily rooted in maintaining the robustness and reliability of alphas on the WorldQuant platform. Here’s why this is crucial and how it interacts with the platform's expectations.

---

### 评论 #15 (作者: MK58212, 时间: 1年前)

This is a well-organized guide for beginners in alpha development on the BRAIN platform, covering essential strategies like smoothing, news data handling, and managing volatility. A few clarifications:

1. How do you handle "news_tot_ticks" for different stocks or industries in event detection?
2. When using "trade_when()" with news datasets, what’s your approach for exit strategies post-event?
3. How do you balance reducing correlation with maintaining alpha strength?

Looking forward to your updates!

---

### 评论 #16 (作者: CC40930, 时间: 1年前)

Overall, your list is a  **comprehensive and well-rounded guide**  for users of the BRAIN platform, especially those looking to develop profitable alphas. Keep up the great work, and thank you for sharing your learnings—this will definitely help others who are getting started or are in the early stages of their alpha development journey!

---

### 评论 #17 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

