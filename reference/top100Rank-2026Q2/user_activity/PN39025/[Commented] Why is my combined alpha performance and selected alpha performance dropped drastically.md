# Why is my combined alpha performance and selected alpha performance dropped drastically?

- **链接**: [Commented] Why is my combined alpha performance and selected alpha performance dropped drastically.md
- **作者**: CM45657
- **发布时间/热度**: 1年前, 得票: 25

## 帖子正文

After the update of today my combined alpha performance and sellected alpha performance has dropped drastically. I don't understand why  but what am sure of is that i have been submitting alphas consistently atleast four alphas for the past one month. The combined alpha performance has dropped  from 2.79 to 0.85 and the sellected alpha performance hass dropped from 0.06 to -0.35 this might even affect my requirement of reaching the master or the grandmaster level .Give me tips that one may use to increase them. Any tip will be much appreciated. Are they really considered when the genius levels. And if they affect the gineous levels how weighted are they?. I would be very greatful if you provide me the information requested. Thanks in advance.

---

## 讨论与评论 (36)

### 评论 #1 (作者: SK72105, 时间: 1年前)

Hey  [CM45657](/hc/en-us/profiles/26410069297303-CM45657) ! I think almost everyone would have seen some fall in the Combined performance metrics in the most recent update because now the after-cost Sharpe is displayed! However, I think another reason of your alpha performance going down drastically could be submitting too many similar alphas (in terms of ideas) or too many correlated alphas in a few regions - this could've led to a large drawdown in Dec 2024(that could be a possibility). You can overcome this by:

1. Submitting lesser correlated alphas, and don't submit too many similar alphas. Always check the "Performance Comparison" tab!

2. Diversifying over regions - Try submitting more alphas in regions that have lesser amount of alphas in your alpha pool

3. Refine existing alphas - Try improving your existing alpha ideas (especially those that gave you a high Value factor earlier) and aim for lower turnover while maintaining a good sharpe and fitness

February is the last month in which you can improve your combined performance for the Genius levels for the next quarter! So utilize it well! All the best!

---

### 评论 #2 (作者: TD28355, 时间: 1年前)

How is the turnover of the alphas you submitted? Have the alphas achieved sufficient diversity? The combined score includes the after-cost factor, meaning transaction costs are deducted. Therefore, if your alpha has a high score but also high turnover, this could be the reason for the low combined score.

---

### 评论 #3 (作者: DN51664, 时间: 1年前)

I think that the high correlation between alphas and high turnover is the reason for the decline in combined alpha performance because, according to the latest update, this score now includes the after-cost factor.

---

### 评论 #4 (作者: TT55495, 时间: 1年前)

The drop in Combined performance may be due to after-cost Sharpe or highly correlated alphas in certain regions. To improve, submit diverse, low-correlation alphas, refine existing ones, and reduce turnover. February is the last chance to qualify for next quarter’s Genius levels.

---

### 评论 #5 (作者: PL15523, 时间: 1年前)

- **Downside Protection** : The long positions (stocks expected to increase in value) and short positions (stocks expected to decrease in value) balance each other, protecting against market downturns.
- **Attractive Risk-Adjusted Returns** : By balancing both long and short positions, the strategy seeks to achieve better returns considering the level of risk taken.

---

### 评论 #6 (作者: AC63290, 时间: 1年前)

**Market Regimes** : The performance of an alpha model can be influenced by the market regime (bull, bear, sideways). Understanding how the model behaves under different market conditions helps in predicting its future success.

---

### 评论 #7 (作者: ND68030, 时间: 1年前)

It ensures that everyone is working with datasets appropriate for their level of expertise, helping maintain fairness and consistency across different levels of analysis.

---

### 评论 #8 (作者: RG93974, 时间: 1年前)

Thank you for starting this insightful discussion on combined alpha performance and selected alpha performance strategies.Submitting less correlation alphas and don't use  too many similar alphas and reduce turnover.Try submitting more alphas in regions that have lesser amount of alphas in your alpha pool.

---

### 评论 #9 (作者: RP41479, 时间: 1年前)

The drop in Combined performance may stem from after-cost Sharpe or regional alpha correlation. Improve by submitting diverse, low-correlation alphas, refining existing ones, and lowering turnover.

---

### 评论 #10 (作者: VP21767, 时间: 1年前)

### Understanding Alpha Performance Drop and Potential Solutions

#### **Why Did Your Alpha Performance Drop?**

Alpha performance fluctuations are common in quantitative trading due to various factors such as market conditions, selection criteria, and correlation with other alphas in the system. Here are some possible reasons for the sudden decline:

1. **Market Regime Shift**
   - If the market conditions have changed (e.g., increased volatility, macroeconomic shifts), previously effective signals may temporarily underperform.
   - Certain alpha signals perform well in trending markets but fail in mean-reverting environments.
2. **Selection and Weighting Adjustments**
   - The WorldQuant BRAIN platform constantly updates its weighting system for alphas.
   - If many participants submit similar alphas, their individual impact on the overall combined alpha score decreases.
   - Newer, more predictive alphas from others may have taken priority, leading to lower weighting for your alphas.
3. **Alpha Redundancy and Correlation Issues**
   - If your submitted alphas are highly correlated with each other, their uniqueness score might be reduced.
   - Correlation with other existing high-performing alphas can also affect selection and impact.
4. **Decay in Predictive Power**
   - Some alpha signals naturally degrade over time, especially if they rely on short-term anomalies.
   - A high Sharpe ratio alpha may gradually lose its edge as the market adapts.

#### **How to Improve Your Alpha Performance?**

Here are some steps to enhance the robustness and longevity of your alpha signals:

1. **Increase Alpha Diversity**
   - Ensure that your submitted alphas are independent of each other.
   - Avoid excessive reliance on common factors like momentum or mean reversion.
2. **Use Robust Feature Selection**
   - Consider alternative data sources such as volume trends, earnings data, and macroeconomic indicators.
   - Implement factor neutralization techniques to minimize exposure to broad market trends.
3. **Optimize Alpha Parameters**
   - Experiment with different decay periods and time horizons to optimize predictive power.
   - Adjust weighting methods and normalization techniques.
4. **Monitor Selection Criteria**
   - Regularly check how your alphas are ranked in comparison to others.
   - Use out-of-sample testing to validate the stability of new alphas.

By continuously refining your approach, you can mitigate performance drops and improve your chances of reaching higher consultant levels on the platform. 🚀

---

### 评论 #11 (作者: TD17989, 时间: 1年前)

- - **`ts_sum`** : Used to calculate the sum over a specified period, which can help in smoothing the data or aggregating features over time.
  - **`group_neutralize`** : Neutralizes the alpha relative to specific groupings like sector or industry. This ensures that the alpha is not biased toward particular groups.
  - **Improvement** : Using  `ts_sum`  helps in smoothing out any volatile data, while  `group_neutralize`  allows you to ensure your alpha is not overfitted to specific sectors or industries.

---

### 评论 #12 (作者: EY94293, 时间: 1年前)

the drop of the combined perfomance may be due to submiting highly corelated aplhas

---

### 评论 #13 (作者: GN67910, 时间: 1年前)

submit alphas with low turnover

---

### 评论 #14 (作者: SK84434, 时间: 1年前)

Your concern is completely valid. Performance drops after updates can be frustrating, especially when you're consistent with alpha submissions. First, it’s important to know that  **combined and selected alpha performances**   *do*  factor into Genius level progression, though they are just part of the broader evaluation (alongside metrics like simulation count, diversity, and backtest stability).

Here are a few tips to help boost performance:

- **Focus on robustness:**  Try using normalization techniques (z-scoring, group-neutralization) to make your alphas more stable across regions and time.
- **Reduce overfitting:**  Avoid overly complex operator chains; test simpler variations of your best-performing alphas.
- **Diversify signal types:**  Mix momentum, reversal, and volatility-style alphas.
- **Track feedback:**  Use the  *simulation diagnostics*  to identify where your alphas are underperforming.
- **Resubmit strong performers:**  Re-upload slightly tweaked versions of past high-performers.

Performance fluctuations are common, keep iterating and you’ll rebound stronger. You're clearly committed, so stay consistent.

---

### 评论 #15 (作者: JM24243, 时间: 1年前)

- **Turnover**
  - High turnover alphas often suffer from excessive trading costs, reducing net performance.
  - Check if your signals require frequent rebalancing—consider optimizing for lower turnover.
- **Diversity of Alphas**
  - If your alphas are highly correlated, their combined impact diminishes.
  - Try adding alphas with different styles (e.g., mean-reversion, momentum, liquidity-based).
- **Market Regime Changes**
  - The market environment may have shifted, making previously successful alphas less effective.
  - Backtest your alphas across different market conditions and adjust accordingly.
- **After-Cost Adjustments**
  - The combined score factors in costs—if your gross alpha score is high but the net score is low, costs are likely an issue.
  - Consider execution-aware alphas that minimize slippage.

---

### 评论 #16 (作者: CK48468, 时间: 1年前)

### **1. Reduce After-Cost Impact**

- Check the  **after-cost Sharpe ratio** —high turnover alphas suffer from slippage and transaction costs.
- Optimize execution: consider  **VWAP-based trading** , spread-aware signals, or volume-adjusted scaling.

### **2. Improve Alpha Diversity**

- If your alphas are highly correlated, they contribute little to the combined score.
- Submit  **uncorrelated alphas**  across different styles (e.g., momentum vs. mean-reversion, volume-based vs. price-based).
- Use  **orthogonalization techniques**  to reduce redundancy.

### **3. Region-Specific Adjustments**

- If your alphas are concentrated in certain markets, their effectiveness may be diluted.
- Diversify into  **multiple regions** , considering unique market structures (e.g., order flow for US, liquidity shifts for EUR, momentum for ASI).

### 

- **Refine existing alphas** : Improve signal stability and reduce noise.
- **Prioritize low-turnover, execution-efficient alphas**  to maximize post-cost returns.
- **Monitor correlations**  and rebalance your submissions accordingly.

---

### 评论 #17 (作者: MG13458, 时间: 1年前)

### **Reduce Alpha Correlation**

- **Diversify your alphas**  by using different styles (momentum, mean-reversion, liquidity-based).
- Submit  **orthogonalized**  alphas—remove overlapping signals by regressing them against existing ones.

---

### 评论 #18 (作者: TM41976, 时间: 1年前)

### **Expand to Underrepresented Regions**

- Submit more alphas in  **regions where you have fewer alphas** , as this can improve diversity.
- Tailor signals to regional differences (e.g.,  **order flow in the USA, liquidity shifts in EUR, momentum in ASI** ).
- Monitor the  **regional alpha contribution**  in your performance breakdown.

---

### 评论 #19 (作者: AK44377, 时间: 1年前)

### **Improve Downside Protection**

- Use  **sector-neutral**  and  **market-neutral**  strategies to reduce exposure to broad market movements.
- Optimize the  **hedging ratio**  between long and short positions based on volatility and beta.

---

### 评论 #20 (作者: TD84322, 时间: 1年前)

The key factors affecting your combined alpha performance and selected alpha performance are Sharpe ratio, correlation, and trading costs. With the recent update, trading costs now impact alpha performance more significantly. To improve your scores, focus on reducing correlation, increasing your Sharpe ratio, and minimizing trading costs.

---

### 评论 #21 (作者: QN91570, 时间: 1年前)

It ensures that everyone is working with datasets appropriate for their level of expertise, helping maintain fairness and consistency across different levels of analysis.

---

### 评论 #22 (作者: PP87148, 时间: 1年前)

![图片](images/img_8b5b56ea91.jpeg)

The updated  **after-cost combined alpha performance**  has been broken down by Genius levels, as shown in the table. Here's what the data reveals:

### **1. Negative Impact**

A significant number of users in each tier experienced a decline in performance, with the severity of the drop categorized by percentage:

- **Expert Level**  (289 users):
  - 275 users (95%) saw a negative impact.
  - Among these,  **139 users**  faced a performance drop of over 50%, the highest proportion for this level.
- **Gold Level**  (1,004 users):
  - 537 users (53.5%) were negatively impacted.
  - A substantial  **319 users**  faced a drop of over 50%.
- **Grandmaster Level**  (31 users):
  - 31 users (100%) were negatively impacted.
  - Most declines were between 20–50%.
- **Master Level**  (117 users):
  - 112 users (95.7%) saw negative changes, with  **53 users**  facing over 50% drops.

### **2. No Change**

Stability was limited to only the  **Gold Level** , where  **279 users (27.8%)**  retained their pre-cost performance, while the other levels showed almost no cases of stability.

### **3. Positive Impact**

Users who gained from the after-cost update are as follows:

- **Expert Level:**  Only 9 users (3.1%) saw positive changes, with  **4 of them**  improving by over 50%.
- **Gold Level:**  188 users (18.7%) benefited, making this group the largest beneficiary.  **164 users**  saw performance gains exceeding 50%.
- **Grandmaster Level:**  Only 5 users (16.1%) experienced positive changes, mostly modest improvements.
- **Master Level:**  Only 5 users (4.3%) benefited, with no gains exceeding 30%.

### **Key Observations**

1. **Gold Level Users Were the Most Affected:**
   - With the largest population, Gold Level saw both the highest number of negatively impacted users and the largest share of positively impacted ones.
2. **Expert and Master Levels Were Most Vulnerable:**
   - Expert-level users faced significant performance drops (95% negative impact).
3. **Grandmaster Level Was Uniformly Negative:**
   - Every Grandmaster saw a decline, though most avoided the steepest drops.
4. **Cost Efficiency Rewarded:**
   - Users in the Gold Level who focused on cost-efficient strategies were rewarded with significant performance boosts.

### **Steps to Counter After-Cost Impact**

To adapt to the new after-cost ranking system, users can take the following actions:

1. **Analyze Cost Drivers in Existing Alphas:**
   - Identify factors contributing to high transaction costs, such as excessive turnover, slippage, or spread sensitivity.
2. **Focus on Cost-Efficient Alpha Design:**
   - Develop strategies with lower turnover or higher signal-to-noise ratios, which reduce trading frequency without compromising performance.
3. **Blend Alphas for Balance:**
   - Combine high-performance, high-cost alphas with lower-cost alphas to improve the overall after-cost performance.

---

### 评论 #23 (作者: GN51437, 时间: 1年前)

The decline in Combined performance could be attributed to after-cost Sharpe or highly correlated alphas in specific regions. To improve, submit a variety of low-correlation alphas, fine-tune existing ones, and lower turnover. February is the final opportunity to qualify for next quarter’s Genius levels.

---

### 评论 #24 (作者: KS24487, 时间: 1年前)

It's apparently the inclusion of costs responsible for the big change. Their tips are here:  [../BK35905/[Commented] How to Improve After Cost Performance置顶的.md](../BK35905/[Commented] How to Improve After Cost Performance置顶的.md)

You are definitely not alone. I'm also quite disappointed to see I'm at 0.59 after 2 months of daily max submissions and careful attention to tie breakers. Looking at the board before and after this update, there was a massive drop for everyone and even most current grandmasters are no longer eligible. This update may make tie breaker criteria obsolete. Logically, it seems those who run this contest are sadists to keep pulling the rug 💀.

That said, at least this is related to alpha performance. Of course I want to reach grandmaster, but to be honest the #1 reason I'm here is to improve my alphas. I don't want to lose sight of that. So, at least the effort to improve this metric aligns with that goal.

I do wish we had a bit more information though. I see some folks with 0 submissions and over 2.00 combined performance. That leads me to think this is another metric measured over the entire lifetime of one's account, but I'm not sure. It would also be nice to know exactly how to calculate after-cost sharpe (or at least include it in the simulation metrics). Similarly, how are the "selected" alphas selected? There's also an element of luck to this -- if you just take a distribution of random alphas there will be winners and losers -- the luck we make helps but only goes so far.

---

### 评论 #25 (作者: PN39025, 时间: 1年前)

When evaluating your submitted alphas, consider both their turnover and diversity. High turnover can significantly impact performance due to increased transaction costs, which are deducted in the combined score. Even if an alpha achieves a high raw score, excessive turnover may result in a much lower combined score. Ensuring sufficient diversity and cost efficiency is crucial for optimizing overall performance.

---

### 评论 #26 (作者: SK72105, 时间: 1年前)

[KS24487](/hc/en-us/profiles/25338264452119-KS24487)  The combined alpha performance (CAP) is updated only till Dec 2024 OS period. So if you have submitted plenty of high performing alphas in Jan 2025 it's likely your sharpe will increase - especially if you are diversifying over regions, and data categories.

Secondly, the CAP, and Selected CAP is calculated for ALL consultant alphas (since beginning of their journey as a Consultant) not just a quarter. So someone with 0 alphas in the quarter can have a CAP > 2.

Selected CAP in my opinion is just alphas that are combined taking into consideration their OS performance and correlation with each other. However, I am unsure of how it works.

---

### 评论 #27 (作者: NH16784, 时间: 1年前)

[CM45657](/hc/en-us/profiles/26410069297303-CM45657)  Hello, the change in CAP is due to the addition of transaction costs. Therefore, the following indicators should be noted to increase CAP:
1. Turnover.
2. Return
3. Margin

---

### 评论 #28 (作者: RW93893, 时间: 1年前)

It’s tough to see such a drastic drop in performance despite consistent submissions. Staying adaptable to updated evaluation criteria must be a challenge. Have you noticed any patterns in which types of Alphas are performing better after the update?

---

### 评论 #29 (作者: NP85445, 时间: 1年前)

Hey, I totally understand your concern about the sudden drop in combined and selected alpha performance. With the recent update, after-cost Sharpe ratios are now factored in more rigorously, so if your alphas have high turnover or are too similar, their net impact can take a hit. I’d recommend checking your turnover levels—small adjustments in decay settings or conditional trading logic (like using trade_when) can help reduce unnecessary trades. Also, consider diversifying your submissions with less correlated strategies across different regions to stabilize your overall performance.

---

### 评论 #30 (作者: NS62681, 时间: 1年前)

The key factors in optimizing alpha performance are the Sharpe ratio and correlation. With the latest update, trading costs have also become a crucial consideration. To enhance your combined alpha, prioritize reducing correlation, improving the Sharpe ratio, and minimizing trading costs. Submitting high-quality alphas with strong predictive power will lead to better long-term performance.

---

### 评论 #31 (作者: AS77213, 时间: 1年前)

**CAN ANYONE PLEASE TELL ME HOW CAN I  IMPROVE MY AFTER COST PERFORMANCE??**

---

### 评论 #32 (作者: DK30003, 时间: 1年前)

I think that the high correlation between alphas and high turnover is the reason for the decline in combined alpha performance because, according to the latest update, this score now includes the after-cost factor.

---

### 评论 #33 (作者: TP19085, 时间: 1年前)

The recent decline in Combined Performance metrics, especially with after-cost Sharpe now displayed, highlights key challenges. Submitting too many correlated alphas or concentrating them in specific regions may have led to larger drawdowns, particularly in December 2024. To improve performance, diversify across regions, reduce correlation, and refine high-value alphas while controlling turnover. Market regime shifts, selection criteria changes, and alpha redundancy also contribute to fluctuations. Enhancing feature selection, optimizing decay periods, and validating stability through out-of-sample testing can mitigate performance drops. Addressing turnover issues, adjusting for market conditions, and minimizing trading costs ensure sustained alpha strength. With February being crucial for Genius-level qualifications, strategic adjustments can maximize potential. Best of luck! 🚀

---

### 评论 #34 (作者: DD24306, 时间: 1年前)

Regarding your question about how the  **combined alpha performance**  and  **selected alpha performance**  are weighted for the Genius levels, these metrics are generally important as part of the evaluation process for your level progress. The weight they carry might depend on various factors like consistency, risk-adjusted returns, and the overall robustness of the alphas you submit.

---

### 评论 #35 (作者: AK40989, 时间: 1年前)

A significant drop in combined and selected alpha performance can often be attributed to changes in the evaluation metrics, such as the introduction of after-cost Sharpe ratios, which can reveal the true impact of transaction costs on your strategies. Additionally, have you considered the correlation between your submitted alphas? High correlation can lead to compounded drawdowns, especially in volatile market conditions. Diversifying your alpha submissions and refining existing strategies to reduce turnover while maintaining performance metrics could be key to improving your scores.

---

### 评论 #36 (作者: DK30003, 时间: 1年前)

How is the turnover of the alphas you submitted? Have the alphas achieved sufficient diversity? The combined score includes the after-cost factor, meaning transaction costs are deducted. Therefore, if your alpha has a high score but also high turnover, this could be the reason for the low combined score.

---

