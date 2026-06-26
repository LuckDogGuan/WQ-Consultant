# [BRAIN TIPS] Finding Alphas: Price Volume Data

- **链接**: [Commented] [BRAIN TIPS] Finding Alphas Price Volume Data.md
- **作者**: NL41370
- **发布时间/热度**: 2年前, 得票: 15

## 帖子正文

In the book “Finding Alphas”, Chapter 18 “Equity Price and Volume” explores characteristics of price volume alphas  **[1]** , while Chapter 7 “Turnover” discusses the impact of price volume alphas on turnover and comparisons with fundamental alphas  **[2]** .

In the dataset  ***Price Volume Data for Equity***  on BRAIN, price can be as at a point in time, such as close or open, or it can also be the maximum  ***high*** , minimum  ***low***  or average  ***vwap***  price for day. Volume can be in terms of total volume for the day, or average volume for the past 20 days  ***adv20*** .

***Turnover***  is a performance metric in our simulation results that measures the simulated daily trading activity.

**Characteristics of price volume alphas**

1. **Trading Frequencies:**  The more often price-volume alphas are traded, the more likely their performance will be statistically significant with higher information ratio (IR), and thus higher  ***Sharpe*** . Once costs are taken into account, however, potential profits from such anomalies decrease. There is a trade-off between higher  ***Sharpe***  and lower  ***turnover*** .
2. **Momentum-Reversion:**  In general, prices tend to revert to the mean over short periods, such as intraday or daily horizons, but they tend to follow the trend over longer horizons of weeks or months.
3. **Psychological Factors:**  Psychological factors can be a source of price-volume alphas. For example, human traders tend to issue buy or sell orders in round numbers. Most people care less about a 1% rise in their holdings than a corresponding 1% loss. People tend to hold their losing positions too long and sell their winning positions too soon.
4. **Other Data:**  Significant movements in price or volume is often a reflection of known or unknown market events. Consider earnings date data, such as  ***ern3_expected_time, News Datasets,***  and  ***Social Media Datasets*** .

**Impact of price volume alphas on turnover**

For price-volume data, changes occur every day but most of those changes are inconsequential. We will likely have a turnover that is higher than ideal, and lose money on average.

**Comparison with fundamental alphas**

In comparison,  ***Fundamental Datasets***  change only a handful of times a year, and have fewer trading opportunities and lower turnover. However, spikes in trading activity may occur during these quarterly changes, suggesting that the alpha may simulate trading into the position very quickly and potentially trading out too soon. This may be suboptimal for fundamental alphas, which usually have longer time horizons.

**Price Volume Data**

**Fundamental Data**

**Turnover**

Higher  ***turnover***  due to highly frequent changes in data (daily)

Lower  ***turnover***  due to less frequent changes in data (quarterly)

**Sharpe**

Higher  ***sharpe***  due to more trading opportunities

Lower ***sharpe*** due to less trading opportunities

The following are examples of  ***Price Volume Data for Equity***  that is provided in BRAIN.

1. Open price ( ***open*** )
2. Close price ( ***close*** )
3. Maximum price ( ***high*** )
4. Minimum price ( ***low*** )
5. Daily returns ( ***returns*** )
6. Market cap ( ***cap*** )
7. Daily traded volume ( ***volume*** )
8. Number of stocks ( ***sharesout*** )

[**[1] Finding Alphas: Chapter 18. Equity Price and Volume**](https://onlinelibrary.wiley.com/doi/10.1002/9781119571278.ch18)

[**[2] Finding Alphas: Chapter 7. Turnover**](https://onlinelibrary.wiley.com/doi/10.1002/9781119571278.ch7)

---

## 讨论与评论 (11)

### 评论 #1 (作者: SK90981, 时间: 1年前)

Thank you for sharing insights on the price volume data which is helpful me to submit more alphas.

---

### 评论 #2 (作者: TT55495, 时间: 1年前)

May I ask why cap is included in price volume? I think market capitalization should be included in fundamental

---

### 评论 #3 (作者: LN78195, 时间: 1年前)

The comparison with fundamental data highlights the unique strengths of each approach. Could you elaborate on how psychological factors like round-number biases can be effectively incorporated into alpha strategies?

---

### 评论 #4 (作者: SK72105, 时间: 1年前)

[TT55495](/hc/en-us/profiles/13132630342807-TT55495)  a lot of datasets have closing price, cap, returns, and many other pv dataset type fields in various data categories. You'll find fields named market cap in some datasets from analyst, fundamental, and model data category too!

---

### 评论 #5 (作者: BA51127, 时间: 1年前)

Your post on "Finding Alphas: Price Volume Data" is quite insightful, especially the discussion on the characteristics of price-volume alphas and their impact on turnover. I'm curious about the role of psychological factors in alpha generation. How can we quantify and integrate these psychological biases, such as round-number orders, into our alpha strategies effectively? Also, could you provide some examples of how these factors have been successfully implemented in the past?

---

### 评论 #6 (作者: TN74933, 时间: 1年前)

here is one example of price volume alpha:  ((-1*rank(Ts_Rank(close, 10))) * rank((close / open)))

---

### 评论 #7 (作者: AC63290, 时间: 1年前)

Thank you for the detailed insights and references from  *Finding Alphas*  regarding price-volume and fundamental alphas, their characteristics, and their impact on turnover and Sharpe ratios. The distinctions between price-volume alphas' high turnover and momentum-reversion traits versus fundamental alphas' low turnover and long-term focus are particularly enlightening. Additionally, the psychological factors influencing price-volume alphas and the emphasis on trading frequency as a trade-off between Sharpe and costs provide a clearer perspective on optimization. The examples of Price Volume Data for Equity in BRAIN are also helpful for practical implementation. Your support in summarizing these concepts is greatly appreciated!

---

### 评论 #8 (作者: HV77283, 时间: 1年前)

The comparison with fundamental data highlights the strengths of both approaches. Could you provide more details on how psychological factors, such as round-number biases, can be effectively integrated into alpha strategies? I'm curious to learn how these behavioral insights can enhance trading signals.

---

### 评论 #9 (作者: CC40930, 时间: 1年前)

Understanding the balance between turnover and Sharpe ratio is crucial when utilizing price-volume alphas, as high turnover can lead to diminishing returns if transaction costs are high.

---

### 评论 #10 (作者: CT68712, 时间: 1年前)

Thanks for sharing this insightful breakdown of price volume data! As a new trader, I find the emphasis on both trading frequency and psychological factors so interesting. The high turnover from price-volume alphas makes sense but also seems to come with the challenge of managing transaction costs effectively. I appreciate your mention of round-number biases; they really do reflect collective trader behavior! I’m eager to explore how I can apply these concepts in my own strategy, particularly in balancing Sharpe ratios with turnover rates. Looking forward to more discussions like this in the community!

---

### 评论 #11 (作者: SP61833, 时间: 1年前)

Thank you so much for sharing insights on the price volume data.The comparison with fundamental data highlights the strengths of both approaches.The examples of Price Volume Data for Equity in BRAIN are also helpful for practical implementation.

---

