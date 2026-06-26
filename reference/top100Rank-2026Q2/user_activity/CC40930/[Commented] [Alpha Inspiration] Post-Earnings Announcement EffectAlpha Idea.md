# [Alpha Inspiration] Post-Earnings Announcement EffectAlpha Idea

- **链接**: [Commented] [Alpha Inspiration] Post-Earnings Announcement EffectAlpha Idea.md
- **作者**: DV65657
- **发布时间/热度**: 2年前, 得票: 17

## 帖子正文

**Paper:** Earnings Announcements are Full of Surprises

**Authors:** Brandt, Kishore, Santa-Clara, Venkatachalam

**Link:**  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=909563](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=909563)

Post-earnings announcement drift or PEAD is the tendency for a stock’s cumulative abnormal returns to drift for several weeks (even several months) following the positive earnings announcement. It is an academically well-documented anomaly first discovered by Ball and Brown in 1968 (we present links to several related academic research papers). Since then, it has been studied and confirmed by countless academics in many international markets. There are a number of ways to define an earnings surprise (or ways to filter stocks with the positive response to earnings) – earnings higher than analysts estimates, earnings higher than some average earnings or stock’s price appreciation during earnings announcement period higher than expected. Each factor shows a strong prediction ability for the stock’s future returns, and it is good to use some combination of factors to enhance the PEAD effect. We present one such strategy from the source paper related to this anomaly. This strategy is presented in its long-short form, but most of the returns come from the long side, so it is not a problem to implement it as long-only. Research also shows that the main performance contributors are small-capitalization stocks; therefore, caution is recommended during the strategy’s implementation.

**Fundamental reason**

This phenomenon can be explained with several hypotheses. The most widely accepted explanation for this effect is investors’  [under-reaction to earnings announcements](https://quantpedia.com/strategies/reversal-in-post-earnings-announcement-drift/) . It is also widely believed that there is a strong connection between earnings momentum and price momentum.

Several studies also show earnings momentum could be explained by liquidity risk as the Post-Earnings Announcement Effect appears to be strong in small-cap stocks.

**Main idea**

Two factors are used: EAR (Earnings Announcement Return) and SUE (Standardized Unexpected Earnings). SUE is constructed by dividing the earnings surprise (calculated as actual earnings minus expected earnings; expected earnings are computed using a seasonal random walk model with drift) by the standard deviation of earnings surprises. EAR is the abnormal return for firms recorded over a three-day window centered on the last announcement date, in excess of the return of a portfolio of firms with similar risk exposures.
Stocks are sorted into quintiles based on the EAR and SUE. To avoid look-ahead bias, data from the previous quarter are used to sort stocks. Stocks are weighted equally in each quintile. The investor goes long stocks from the intersection of top SUE and EAR quintiles and goes short stocks from the intersection of the bottom SUE and EAR quintiles the second day after the actual earnings announcement and holds the portfolio one quarter (or 60 working days). The portfolio is rebalanced every quarter.

**Related dataset:**

earnings surprise

fmdl17_est_z_earningssurprise

             Research Analyst Estimate Factors

Abnormal Return   
       mdl77_opricemomentumfactor_rba
             Analysts' Factor Model

![图片](images/img_9ea4648811.png)

![图片](images/img_e59f27c10f.png)

---

## 讨论与评论 (13)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hello!

That's a brilliant find with the mdl77_opricemomentumfactor_rba field! You're onto something really exciting. Here are some suggestions that might help you take your idea even further:

1. Consider implementing this field yourself using the group_mean and trade_when operators. This way, you could find the market-adjusted price return not only from two days before to one day after its quarterly earnings announcement, but also over a longer period. And instead of using the S&P 500 return as a market proxy, you might try using sector-specific returns.
2. Take long or short positions based on your condition, and then gradually exit the positions - you can use the days_from_last_change operator and the event earning announcement as inputs.

These tweaks might just enhance your Alpha and bring about better results.

Remember, every little adjustment you make is a step towards refining your Alpha and uncovering new insights. Keep exploring, keep experimenting, and most importantly, keep going! You're doing a fantastic job 😊

---

### 评论 #2 (作者: JS86713, 时间: 2年前)

I am nor able to find this field.
please help me to find.

---

### 评论 #3 (作者: AG20578, 时间: 2年前)

Hi  [JS86713](/hc/en-us/profiles/22373948554903-JS86713) !

This field can be found in DataExplorer  [https://platform.worldquantbrain.com/data/data-sets/model77/data-fields/mdl77_opricemomentumfactor_rba?delay=1&instrumentType=EQUITY&region=USA&universe=TOP3000](https://platform.worldquantbrain.com/data/data-sets/model77/data-fields/mdl77_opricemomentumfactor_rba?delay=1&instrumentType=EQUITY&region=USA&universe=TOP3000)

This field is available for consultants, learn more about consultant program:  [https://platform.worldquantbrain.com/consultant-program/](https://platform.worldquantbrain.com/consultant-program/)

---

### 评论 #4 (作者: XD81759, 时间: 1年前)

Hey, that's a really interesting post about the Post-Earnings Announcement Effect. Using EAR and SUE as factors makes sense as they capture different aspects of earnings surprise and abnormal return. Sorting stocks into quintiles helps in identifying the extremes. Rebalancing quarterly keeps the portfolio updated. Just be careful with small-cap stocks as they contribute much to performance but also bring liquidity risks. Overall, it's a solid strategy to explore and potentially enhance the PEAD effect.

---

### 评论 #5 (作者: CC40930, 时间: 1年前)

The Post-Earnings Announcement Drift (PEAD) phenomenon remains a fascinating and well-documented market anomaly, with significant implications for stock returns following earnings announcements. The strategy highlighted in the paper—sorting stocks based on Earnings Announcement Return (EAR) and Standardized Unexpected Earnings (SUE)—provides a robust framework for capitalizing on this anomaly. By combining these factors, investors can predict the continuation of stock momentum, especially in small-cap stocks, where the effect tends to be stronger. This long-short strategy allows investors to potentially benefit from the drift in stock prices after earnings surprises, but it’s essential to consider the liquidity risks, especially with smaller stocks. Additionally, rebalancing portfolios quarterly is an important practice to manage risk and capture the sustained impact of earnings surprises.

---

### 评论 #6 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #7 (作者: AK98027, 时间: 1年前)

Hey, that's a really interesting post about the Post-Earnings Announcement Effect. Using EAR and SUE as factors makes sense as they capture different aspects of earnings surprise and abnormal return. Sorting stocks into quintiles helps in identifying the extremes. Rebalancing quarterly keeps the portfolio updated. Just be careful with small-cap stocks as they contribute much to performance but also bring liquidity risks. Overall, it's a solid strategy to explore and potentially enhance the PEAD effect.

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

This post presents a robust strategy based on the Post-Earnings Announcement Drift (PEAD) anomaly, effectively using Earnings Announcement Return (EAR) and Standardized Unexpected Earnings (SUE) to identify stocks that are likely to continue moving in the direction of their earnings surprise. By sorting stocks into quintiles and constructing long-short portfolios, this approach takes advantage of under-reactions to earnings news. A well-structured strategy with good academic backing! To improve, you might consider adjusting for volatility or incorporating sector-specific factors to refine stock selection further. Looking forward to more discussions on how to enhance its effectiveness.

---

### 评论 #9 (作者: TP14664, 时间: 1年前)

Post-Earnings Announcement Drift (PEAD) is an interesting and well-documented anomaly in financial markets, where stocks tend to experience cumulative abnormal returns over a period of time (often several weeks or months) following a positive earnings announcement. This phenomenon was first discovered by Ball and Brown in 1968 and has since been widely studied and confirmed by numerous researchers in various global markets. The basic premise is that investors' reactions to earnings reports, especially those that exceed expectations, may be slow to fully adjust, creating a persistent drift in stock prices.

---

### 评论 #10 (作者: PN39025, 时间: 1年前)

Thanks for sharing this valuable insight!

Two factors are central to the analysis:

1. **EAR (Earnings Announcement Return)** : The abnormal return over a three-day window centered on the last earnings announcement, adjusted for firms with similar risk exposures.
2. **SUE (Standardized Unexpected Earnings)** : Calculated by dividing the earnings surprise (actual earnings minus expected earnings, derived using a seasonal random walk model with drift) by the standard deviation of earnings surprises.

**Strategy** :

- Stocks are sorted into quintiles based on EAR and SUE using data from the previous quarter.
- The strategy involves going long on stocks in the intersection of the top EAR and SUE quintiles, and short on stocks in the intersection of the bottom quintiles. Positions are initiated the second day after the earnings announcement and held for one quarter (60 working days), with quarterly rebalancing.

How do EAR and SUE interact to affect returns, and could other factors like sector trends or macroeconomic events enhance the model's robustness?

---

### 评论 #11 (作者: TD17989, 时间: 1年前)

**Earnings Surprise Definition** : The surprise is typically calculated as the difference between the reported earnings and analysts' expectations. A positive surprise occurs when the reported earnings exceed expectations, and a negative surprise happens when earnings fall short of predictions.

---

### 评论 #12 (作者: NT63388, 时间: 1年前)

This post highlights the well-known Post-Earnings Announcement Drift (PEAD) anomaly. It suggests combining Earnings Announcement Return (EAR) and Standardized Unexpected Earnings (SUE) to identify stocks that will drift upwards after an earnings announcement. 
The proposed implementation is a long-short strategy, long the top quintile intersection and short the bottom, held for one quarter. The note also correctly mentions that the effect is stronger in small-cap stocks. 
Key takeaway: Combine SUE and EAR to exploit under-reaction to earnings news. Remember the small-cap bias.

---

### 评论 #13 (作者: AB15407, 时间: 1年前)

The paper "Earnings Announcements are Full of Surprises" explores the PEAD anomaly, a persistent effect where stock prices continue to move in the direction of an earnings surprise for weeks or even months. The strategy combines EAR and SUE to identify under-reacting stocks. The suggested long-short implementation highlights potential alpha generation, especially in small-cap stocks. However, be aware of potential liquidity risk and challenges in accurately estimating expected earnings for SUE calculation. A good starting point for exploring earnings-based strategies.

---

