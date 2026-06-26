# [Alpha Inspiration] 12 Month Cycle in Cross-Section of Stocks ReturnsAlpha Idea

- **链接**: [L2] [Alpha Inspiration] 12 Month Cycle in Cross-Section of Stocks ReturnsAlpha Idea.md
- **作者**: TD17989
- **发布时间/热度**: 2年前, 得票: 21

## 帖子正文

**Paper:** Seasonality in the Cross-Section of Expected Stock Returns

**Author:** Heston, Sadka

**Link:**  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=687022](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=687022)

The best known seasonal effect in stocks is the  [January effect](https://quantpedia.com/strategies/january-effect-in-stocks/)  that says that stocks perform exceptionally well in the first month of the year. But let’s take a better look inside this anomaly. We may realize that stocks that performed very well in last year’s January will perform well also in this year’s January. Academic research shows this effect is not confined only to January (although the first month of the year is the strongest month for this new anomaly). Still, it also holds for other months of the year – stocks with high historical returns in a particular calendar month tend to have high future returns in that same calendar month.

This seasonal effect is independent of, and its power is comparable to other known effects like  [momentum](https://quantpedia.com/strategies/january-effect-in-stocks/) , mean reversion,  [the earnings announcement effect](https://quantpedia.com/strategies/post-earnings-announcement-effect/) , or  [value effect](https://quantpedia.com/strategies/net-current-asset-value-effect/) . The effect holds well not only in the US but also in other countries. It is strong in each size group, but we present results for the large-cap stocks (as a real-world implementation of every anomaly is always easier with larger companies).

**Fundamental reason**

Academic research shows that the seasonal pattern of liquidity may help explain part of the expected returns. Other explanations attribute returns to compensation for systematic risk or to behavioral theories of investing.

**Alpha implementation**

Every month, stocks are grouped into ten portfolios (with an equal number of stocks in each portfolio) according to their performance in one month one year ago. Investors go long in stocks from the winner decile and shorts stocks from the loser decile. The portfolio is equally weighted and rebalanced every month.

**Related dataset:**

daily return - returns

![图片](images/img_3b6fbd0d92.png)

![图片](images/img_3683bc167c.png)

---

## 讨论与评论 (18)

### 评论 #1 (作者: YW42946, 时间: 2年前)

Hi  [TD17989](/hc/en-us/profiles/13680660215831-TD17989)

I'm Youlin, Brain Researcher from Taiwan office. Nice post on the classical January effect. One thing to note is that in your current implementation, you mentioned that you will long the first decile, and short the loser decile. However, based on the long count and short count number, it suggested that it trades nearly all stocks in the universe (suppose you are working in USA D1 Top3000).

Overall, it is a good idea and brilliant implementation, another future room for testing is how do you define outperform in previous year's month. Is it simple the return of the stocks, or the something more delicate. For example, stocks returns that remove peer's average return..etc.

---

### 评论 #2 (作者: TD17989, 时间: 2年前)

Thank you for your advice. I will remove the conditions and let alpha trade in all stocks

---

### 评论 #3 (作者: TK85978, 时间: 2年前)

Hi Hi  [TD17989](/hc/en-us/profiles/13680660215831-TD17989) ,

I'm Taegyum Kim from South Korea, First, let me say that I am very impressed with your alpha idea. So we would like to implement it in alpha like you, can you help us? My email address is ' [ergh123@postech.ac.kr](mailto:ergh123@postech.ac.kr) ' . We have a lot of questions, like what operator did you use, did you do it in the US or China, etc. Any help would be greatly appreciated.

Best regards.

---

### 评论 #4 (作者: NG20776, 时间: 2年前)

Hi Taegyum Kim - are you speaking with your advisor to help?

---

### 评论 #5 (作者: TK85978, 时间: 2年前)

First of all, thank you for your response. We are in the middle of an IQC competition and don't have an advisor, so I reached out to get some ideas and hints for our alpha.

---

### 评论 #6 (作者: SB17086, 时间: 1年前)

thank you for this advice.

---

### 评论 #7 (作者: XL31477, 时间: 1年前)

Hey  [YW42946](/hc/en-us/profiles/12485882527255-YW42946) , thanks for your insightful comment. You're right about the trading of nearly all stocks, that's something to consider further indeed. Regarding defining outperform, just using simple stock return might be a bit rough. Considering removing peer's average return could make it more refined as it filters out the general market influence and focuses more on the stock's individual performance relative to its peers. It's worth testing both ways to see which works better for this alpha implementation.

---

### 评论 #8 (作者: XD81759, 时间: 1年前)

Hey YW42946, great points there, man! You're right about the trading scope issue. Maybe we could consider narrowing it down a bit to make it more manageable. And regarding defining "outperform", it's indeed crucial. Just using simple stock returns might be a bit rough. Using something like excess return over the peer average, as you mentioned, could be a better way. It'd filter out the market-wide or sector-wide influences and might make the factor more refined and effective for our strategy.

---

### 评论 #9 (作者: CC40930, 时间: 1年前)

The paper by Heston and Sadka delves into the seasonal effects on stock returns, specifically the persistence of high returns for stocks that performed well in a given month, especially January. Their findings highlight that this seasonal pattern extends beyond January, indicating a broader, more predictable anomaly across various months of the year. The research also emphasizes that this effect is comparable in strength to other known market anomalies like momentum or mean reversion. Importantly, the paper suggests liquidity factors and behavioral theories as possible drivers behind these predictable returns. The strategy to implement this alpha involves portfolio rebalancing every month based on past performance, with long positions in the top performers and short positions in the bottom performers. This anomaly offers an interesting opportunity for investors, especially in large-cap stocks, to exploit consistent monthly patterns in stock returns.

---

### 评论 #10 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #11 (作者: AK98027, 时间: 1年前)

Hey YW42946, great points there, man! You're right about the trading scope issue. Maybe we could consider narrowing it down a bit to make it more manageable. And regarding defining "outperform", it's indeed crucial. Just using simple stock returns might be a bit rough. Using something like excess return over the peer average, as you mentioned, could be a better way. It'd filter out the market-wide or sector-wide influences and might make the factor more refined and effective for our strategy.

---

### 评论 #12 (作者: CC40930, 时间: 1年前)

This paper on seasonality in stock returns presents an interesting and robust anomaly, showing that stocks that performed well in a specific month tend to repeat that performance the following year. It is fascinating how such patterns align with liquidity cycles and could be a strong consideration for developing seasonal-based strategies. The implementation approach of grouping stocks into deciles based on prior-year performance and then going long on winners and short on losers could offer a promising strategy to exploit this effect. Thanks for sharing! I’ll definitely look into the paper.

---

### 评论 #13 (作者: AK40989, 时间: 1年前)

By grouping stocks into deciles based on past monthly performance, investors can go long on the winner decile and short the loser decile. This strategy leverages established concepts like momentum and mean reversion, particularly in large-cap stocks where implementation is easier. Rebalancing the portfolio monthly allows investors to capitalize on these seasonal patterns, potentially leading to an increase in alpha performance.

---

### 评论 #14 (作者: LY88401, 时间: 1年前)

Heston and Sadka's paper explores the seasonal effects on stock returns, focusing on the persistence of strong performance for stocks that excelled in a particular month, notably January. Their findings reveal that this seasonal anomaly is not limited to January but occurs across various months, making it a broader and more predictable pattern. The study compares this effect's significance to other well-known anomalies like momentum and mean reversion. Liquidity factors and behavioral theories are proposed as potential explanations for these consistent returns. The suggested strategy involves monthly portfolio rebalancing, taking long positions in top-performing stocks and short positions in underperformers. This anomaly presents an intriguing opportunity for investors, particularly in large-cap stocks, to leverage recurring monthly patterns for potential gains.

---

### 评论 #15 (作者: NT63388, 时间: 1年前)

Could you share which region this idea was implemented on?

Looking at the IS Summary values, I'd guess it was implemented on the ASI region.

Also, I'm quite interested in whether this performance can be achieved well out-of-sample (OS). Do you have any basis for the out-of-sample quality?

---

### 评论 #16 (作者: NT63388, 时间: 1年前)

It seems you are a new consultant. I'm quite impressed that you've already managed to build an Alpha from the article - something that's not easy even for experienced consultants.

I hope you continue to maintain this enthusiasm and curiosity, as I think it will help you achieve sustainable success in finding high-quality Alphas.

---

### 评论 #17 (作者: PN39025, 时间: 1年前)

Thank you for the insightful tips on building a database for Alpha performance! The approach to 12 Month Cycle in Cross-Section of Stocks Returns results is incredibly helpful for refining research and improving submissions.

---

### 评论 #18 (作者: AB15407, 时间: 1年前)

This paper highlights a robust seasonal effect in stock returns beyond the well-known January effect. It demonstrates that past monthly performance predicts future performance in the same month, independent of other established factors like momentum or value. The proposed alpha implementation is a simple long-short strategy based on decile ranking by prior year's monthly returns. Worth investigating given its persistence and potential link to liquidity patterns. Key data is daily returns for calculating monthly performance.

---

