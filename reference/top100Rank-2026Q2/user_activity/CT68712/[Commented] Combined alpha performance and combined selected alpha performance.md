# Combined alpha performance and combined selected alpha performance.

- **链接**: [Commented] Combined alpha performance and combined selected alpha performance.md
- **作者**: SC87308
- **发布时间/热度**: 1年前, 得票: 13

## 帖子正文

#### **Hi guys,**

#### Someone, please tell me how to increase combined alpha performance and combined selected alpha performance. Ever since these eligibility criteria have come , they have been going to decrease every time. Please suggest some beneficial tips.

#### Thank you

---

## 讨论与评论 (40)

### 评论 #1 (作者: NM12321, 时间: 1年前)

As far as I know, the two indicators CombinePerformance and CombineSelectedPerformance are similar to value factors, so it will depend a lot on your performance alpha. Therefore you need to submit quality alpha and low corr. The current genius threshold is based on max 2 of these indicators.

---

### 评论 #2 (作者: DN51664, 时间: 1年前)

I have also observed the same as you. Initially, my combined alpha performance score was above 2, but it has been decreasing after multiple updates. Although my value factor remains quite stable, the combined alpha performance score keeps dropping. I'm not sure if there are differences in the calculation methods of these two metrics.

---

### 评论 #3 (作者: TT55495, 时间: 1年前)

CombinePerformance and CombineSelectedPerformance depend on performance alpha, so submit high-quality, low-correlation alpha. The genius threshold allows up to two of these indicators.

---

### 评论 #4 (作者: NH84459, 时间: 1年前)

- **Low Transaction Costs** : Strategies need to account for trading costs like commissions, slippage, and market impact. Excessive transaction costs can erode potential profits.
- **Slippage** : Evaluate slippage, which is the difference between the expected price of a trade and the actual execution price. Minimizing slippage can increase strategy effectiveness.

---

### 评论 #5 (作者: deleted user, 时间: 1年前)

Optimizing models over short timeframes can cause overfitting, as they may be tuned to past market noise that doesn’t reflect future conditions. Using a longer backtesting period tests the model in more diverse market environments, reducing the risk of tailoring a model to a temporary pattern that doesn't hold.

---

### 评论 #6 (作者: QG16026, 时间: 1年前)

- Confirms that the model can maintain strong performance when applied to larger sets of assets (more than 70% of the original Sharpe ratio).
- **Why it matters** : It ensures that the model is not overfitted to a small set of instruments and remains effective when expanded to a broader universe of assets.

---

### 评论 #7 (作者: ND68030, 时间: 1年前)

This helps prevent consultants from using data outside their level's scope, which could lead to suboptimal analysis or overfitting, as more complex datasets may not be appropriate for lower-level analysts.

---

### 评论 #8 (作者: TD17989, 时间: 1年前)

- Some developers unknowingly leak information from the training data into the OS period.
- Example:  *“Ensure that OS testing is conducted on data that was truly unseen during model development—no peeking at OS performance while tweaking parameters!”*

---

### 评论 #9 (作者: PN39025, 时间: 1年前)

Hi , The most effective way to achieve robust sampling is by submitting low-correlation alpha through a diversified portfolio utilizing multiple datasets and submitting across various regions and universes

---

### 评论 #10 (作者: RP41479, 时间: 1年前)

Submit high-quality, low-correlation alphas, as Combine Performance and Combine Selected Performance depend on alpha performance. The genius threshold allows up to two such indicators.

---

### 评论 #11 (作者: VP21767, 时间: 1年前)

I think diversifying the alphas we submit will improve the merge combine index somewhat. For example, we sub different regions in 1 month such as CHN, GLB, ASI, EUR,... Good luck.

---

### 评论 #12 (作者: LB76673, 时间: 1年前)

1. Improve OS Sharpe Ratio of Your Alphas

A higher OS Sharpe directly improves your combined performance.

- Avoid Overfitting: Keep alphas simple, test on different time periods, and avoid excessive parameter tuning.

- Use the Test Period Feature: Ensure alphas perform well in the test set before submission.

- Use Market-Neutral Transformations: Avoid biases that overfit to specific market regimes.

- Ensure Stability: Alphas with consistent Sharpe over time are better for combined performance.

---

2. Reduce Correlation Between Submitted Alphas

Highly correlated alphas don’t contribute much to Combined Alpha Performance.

- Check Correlation Matrices: Before submission, analyze pairwise correlation between your alphas.

- Use Diverse Factors: Instead of just price-based signals, incorporate fundamental, volume, and alternative datasets.

- Apply Different Transformations: Use variations in decay rates, time horizons, or ranking mechanisms.

- Submit Alphas from Different Pyramids: Ensuring alphas come from different sources enhances diversification.

---

3. Optimize Turnover for Better Score Impact

Turnover impacts your score directly:

- Keep Turnover < 10%: High turnover alphas tend to degrade performance.

- Use Low-Turnover Operators: Apply ts_target_tvr_hump, ts_target_tvr_delta_limit, or trade_when.

- Balance Sharpe vs. Turnover: If turnover is high, ensure Sharpe is well above 2.

---

4. Improve Risk Management and Neutralization

Some neutralizations may increase turnover and harm scores.

- Apply Selective Neutralizations: Avoid over-neutralizing factors unless necessary.

- Monitor Exposure to Unwanted Risks: Industry, sector, and macro risks should be controlled efficiently.

- Test Alpha Performance with and Without Neutralization: Sometimes, removing neutralization can improve OS performance.

---

5. Increase the Number of High-Scoring Alphas

- Submit More Alphas with Scores > 0: Your combined score depends on the total number of alphas and their scores.

- Remove Poor Performers: Regularly replace low-scoring alphas with better ones.

- Keep a Balance Between New and Old Submissions: Continuously refreshing your alpha pool ensures adaptability.

---

### 评论 #13 (作者: TD84322, 时间: 1年前)

The two key factors are Sharpe ratio and correlation. With the recent update, trading costs now play a role in alpha performance. To improve your combined alpha performance, focus on lowering correlation, increasing Sharpe ratio, and minimizing trading costs.

---

### 评论 #14 (作者: MA97359, 时间: 1年前)

Hi  [SC87308](/hc/en-us/profiles/16143039569687-SC87308) ,

Improving  **combined alpha performance**  and  **combined selected alpha performance**  is a time-consuming process that requires a  **smart and systematic approach** —it can't be achieved overnight. Here are some key strategies to enhance both:

#### **1. Combined Alpha Performance**

This represents the performance of your entire pool of regularly submitted alphas. To improve it:

- **Diversify Alpha Generation**  – Expand your alpha building across all accessible regions to reduce dependency on a single market.
- **Include Delay-0 Alphas**  – These can contribute positively to overall performance.
- **Focus on Weight-Gaining Alphas**  – Read up on strategies to develop alphas that have a higher chance of gaining weight, such as  **competition alphas**  or  **theme-based alphas** .
- **Daily Submission Strategy**  – Among your daily submitted alphas, ensure that at least  **one alpha is robust** , passing key tests like:
  - **Testing Period**
  - **Margin & Turnover Requirements**
  - **Rank Test**
  - **Sub-Universe Test**
  - **Sign Test**

#### **2. Combined Selected Alpha Performance**

This measures the performance of the alphas you’ve  **chosen**  for building super alphas. To optimize it:

- **Select a Diverse Set of Alphas**  – Avoid over-relying on the same selection expressions.
- **Submit Super Alphas Across Regions**  – Broaden your approach to maximize opportunities.
- **Leverage High-Performing Alphas**  – Tag alphas that already show strong performance and use them strategically to build  **super alphas** .

---

### 评论 #15 (作者: QN91570, 时间: 1年前)

Initially, my combined alpha performance score was above 2, but it has been decreasing after multiple updates. Although my value factor remains quite stable, the combined alpha performance score keeps dropping.

---

### 评论 #16 (作者: RB20756, 时间: 1年前)

To enhance alpha performance, focus on OS Sharpe, diversification, and turnover optimization. Avoid overfitting by testing alphas across varied periods. Reduce correlation with diverse factors and transformations. Keep turnover low for stability. Continuously refine risk management and submit high-scoring, uncorrelated alphas for optimal results. 🚀

---

### 评论 #17 (作者: HN62464, 时间: 1年前)

A key approach to improving combined alpha performance is refining alpha selection and submission strategies. Besides maintaining low correlation and high Sharpe, consider adaptive weighting—giving more weight to consistently strong alphas while phasing out weaker ones dynamically. Also, leverage market regimes by categorizing alphas based on macro conditions and rotating them accordingly.

---

### 评论 #18 (作者: AC63290, 时间: 1年前)

To enhance combined alpha performance, focus on creating diverse, uncorrelated alphas. Key strategies include: exploring different timeframes (intraday vs. multi-day signals), using varied data sources (price, volume, fundamentals), and implementing distinct trading strategies (momentum, mean reversion, sentiment). Ensure proper neutralization across sectors and market factors. Optimize individual alpha weights in the combination based on their correlation matrix and historical performance. Consider market regime detection to dynamically adjust weights. Pay attention to turnover and transaction costs. Most importantly, maintain strict quality control on individual alphas before combining them, as weak components can dilute overall performance.

---

### 评论 #19 (作者: PP87148, 时间: 1年前)

This is a really good question, and it’s something a lot of us are struggling with since the recent inclusion of  **after-cost adjustments**  in the performance metrics. Below is the impact of  **after-cost adjustment**  across all genius levels.
 ![图片](images/img_07230fb62b.jpeg) 

 **Why Your CAP/CSAP Might Be Dropping:**

1. **After-Cost Adjustments** : The new calculations now account for things like slippage, turnover, and trading costs. If your alphas aren’t cost-efficient, their performance will take a hit.
2. **Alpha Decay** : Alphas can lose their edge over time, especially if market dynamics change or others are working on similar ideas.
3. **Overfitting** : If your alphas are too tuned to historical data, they might not perform well in forward tests, leading to penalties.
4. **Selected Alpha Inefficiencies** : If your chosen alphas aren’t contributing well to the portfolio, they’ll pull down your CSAP.

### 

### Tips to Boost Your CAP and CSAP:

#### 1.  **Optimize for After-Cost Performance**

- Keep  **turnover**  low to avoid excessive trading.
- Minimize slippage and impact costs by avoiding signals that generate heavy trades in less liquid stocks.
- Use features that are robust and less noisy—they tend to hold up better after costs are applied.

#### 2.  **Diversify Your Alphas**

- Blend high-cost alphas with low-cost ones to strike a balance.
- If you have access to multiple regions like EUR, USA, ASI, or GLB, spread your alphas across them to reduce concentration risk.

#### 3.  **Focus on Selected Alphas**

- Prioritize alphas with a strong signal-to-noise ratio; they’ll improve CSAP.
- Avoid choosing alphas that are too correlated with each other, as this can dilute their impact on the portfolio.

#### 4.  **Leverage Advanced Tools**

- Use the  **Brain API**  to automate alpha generation and test them for after-cost performance before submitting.
- Experiment with blending techniques to create synergies between alphas for a more stable performance.

### A Few Key Takeaways:

- Focus on  **quality, not quantity** —a smaller, well-balanced set of cost-efficient alphas will outperform a large set of subpar ones.
- Keep an open mind and collaborate with others in the community to pick up new ideas and stay ahead of the curve.

---

### 评论 #20 (作者: GN51437, 时间: 1年前)

CombinePerformance and CombineSelectedPerformance are influenced by performance alpha, so it's important to submit high-quality, low-correlation alphas. The genius threshold permits up to two of these indicators.

---

### 评论 #21 (作者: PN39025, 时间: 1年前)

**Tips to Boost Combined Alpha Performance:**

1. **Develop Diverse Alphas:**  Focus on creating alphas with low self-correlation and low correlation with production alphas. Explore new and less commonly used alpha strategies.
2. **Diversify Across Regions:**  Submit low-correlation alphas in different regions to maximize the number of pyramids and improve overall performance.
3. **Scale Up Signal Generation:**  Increase the total number of alphas to enhance the combined signal strength.
4. **Prioritize High OS Sharpe Ratios:**  Look for alphas with consistently high out-of-sample (OS) Sharpe ratios, as they indicate stronger and more reliable performance.
5. **Use Meaningful Look-back Periods:**  Avoid arbitrary values. Stick to well-tested periods like 5, 20, 60, or 240 days to ensure robust results.

In addition to exploring new data fields across pyramids, consider using  **unconventional operators** not just time-series operators. By pushing these boundaries, you can climb to higher tiers in the  **BRAIN Genius Program** .

---

### 评论 #22 (作者: CT68712, 时间: 1年前)

Hey there! As a fellow quant enthusiast, I totally get your concerns about combined alpha performance. One of the key things I've learned is to diversify your strategies—experiment with combining various factors like momentum, value, and volatility. Also, consider backtesting your models rigorously. Even small tweaks can lead to significant improvements over time. Lastly, keep an eye on market conditions as they can impact your performance metrics. Best of luck, and let's keep pushing to optimize our strategies together!

---

### 评论 #23 (作者: TD28355, 时间: 1年前)

My score has also decreased over time, and I don’t understand the reason why. I sincerely hope the moderators can explain the mechanism for calculating the combined score, including what factors are involved. If this score is calculated based on all submitted alphas, I don’t believe it could change so drastically within just one month.

---

### 评论 #24 (作者: KS69567, 时间: 1年前)

### **To Boost Combined alpha performance and combined selected alpha performance:**

1. **Diversify Alphas:**  Use low-correlation (<0.6) alphas from different regions, data fields, and timeframes.
2. **Enhance OS Performance:**  Test in multiple market environments; apply dynamic risk filters.
3. **Smart Weighting:**  Optimize alpha weights to favor strong performers and reduce weak alpha impact.
4. **Reduce Turnover:**  Use vector/regression neutralization to lower turnover without hurting Sharpe.
5. **Regular Cleanup:**  Remove underperforming alphas and refresh with new, uncorrelated ones.
6. **Focus on Stability:**  Prioritize alphas with consistent performance, not just peak metrics.

---

### 评论 #25 (作者: LM22798, 时间: 1年前)

It highly depends on the quality of your alpha and its uniqueness, try creating alphas from less used datasets.

---

### 评论 #26 (作者: GS53807, 时间: 1年前)

Great discussion! It seems like diversification is key to improving Combined Alpha Performance. Instead of focusing only on a single region like the US or CHN, spreading submissions across multiple markets like GLB, EUR, and ASI could help reduce correlation. Also, testing different ranking methods (quantile vs. z-score vs. rank) might lead to more unique signals. One thing I’m curious about—how much impact does neutralization (e.g., sector or risk factor removal) have on combined performance? Has anyone tested this?

---

### 评论 #27 (作者: NH16784, 时间: 1年前)

[SC87308](/hc/en-us/profiles/16143039569687-SC87308)  Hello, the change in CAP is due to the addition of transaction costs. Therefore, the following indicators should be noted to increase CAP:
1. Turnover.
2. Return
3. Margin

---

### 评论 #28 (作者: HN71281, 时间: 1年前)

To improve Combined Alpha Performance, focus on submitting high-quality, low-correlation alphas. Diversify your alphas to avoid redundancy, monitor risk-adjusted returns, and adapt to changing market conditions. Regularly refine your strategies and test for robustness.

---

### 评论 #29 (作者: BS20926, 时间: 1年前)

I think CombinePerformance and CombineSelectedPerformance are influenced by OS performance alpha, so focus on submitting good alpha with high predictability for future performance.

---

### 评论 #30 (作者: NP85445, 时间: 1年前)

Hey, I totally understand your concern about the sudden drop in combined and selected alpha performance. With the recent update, after-cost Sharpe ratios are now factored in more rigorously, so if your alphas have high turnover or are too similar, their net impact can take a hit. I’d recommend checking your turnover levels—small adjustments in decay settings or conditional trading logic (like using trade_when) can help reduce unnecessary trades. Also, consider diversifying your submissions with less correlated strategies across different regions to stabilize your overall performance.

---

### 评论 #31 (作者: RB90992, 时间: 1年前)

To improve combined alpha performance, you should:

I.     Focus on risk management to protect gains and reduce losses.
II.    Evaluate costs and taxes to ensure you’re keeping more of your returns.
III.   Monitor and adjust your portfolio regularly based on performance and market changes.
IV.   Diversify strategically across sectors and assets.
V.    Stay flexible and adaptive to evolving market conditions, while keeping a long-term perspective.
VI.   Leverage data and analytics to refine strategies and uncover hidden opportunities.
VII.  Continuous refinement and strategic adjustments are key to maintaining strong alpha performance

---

### 评论 #32 (作者: TN74933, 时间: 1年前)

Hi, Combined and Combine Selected Performance depend on performance of your alpha pool, so try to submit low turnover, low self/prof correlation alpha to improve you level. goodluck!!!!!!

---

### 评论 #33 (作者: NS62681, 时间: 1年前)

The key factors in optimizing alpha performance are the Sharpe ratio and correlation. With the latest update, trading costs have also become a crucial consideration. To enhance your combined alpha, prioritize reducing correlation, improving the Sharpe ratio, and minimizing trading costs. Submitting high-quality alphas with strong predictive power will lead to better long-term performance.

---

### 评论 #34 (作者: PT27687, 时间: 1年前)

Improving combined alpha performance can be quite challenging, especially with new eligibility criteria in place. Have you considered analyzing the selection process for your strategies? Sometimes, a thorough review of the underlying algorithms and adjusting parameters can lead to better outcomes. It might also be worth exploring diversification across different strategies. What approaches have you tried so far?

---

### 评论 #35 (作者: TP19085, 时间: 1年前)

Enhancing combined alpha performance requires a strategic approach, ensuring diversity and minimizing correlation. Key strategies include using different timeframes, data sources, and trading styles while neutralizing market and sector biases. Optimizing alpha weights through correlation analysis and market regime detection improves adaptability. Maintaining low turnover and controlling transaction costs preserves returns. High OS Sharpe ratios enhance overall performance—avoiding overfitting, testing across periods, and using market-neutral transformations are essential. Reducing correlation through diverse factors, transformations, and dataset variations increases robustness. Optimizing turnover (<10%) with low-turnover operators improves stability. Effective risk management through selective neutralization prevents unnecessary performance degradation. Regularly refreshing high-scoring alphas while removing weak ones ensures sustained alpha strength and adaptability in evolving market conditions.

---

### 评论 #36 (作者: VN28696, 时间: 1年前)

I've noticed the same trend as well. My combined alpha performance was initially strong, but after several updates, it has been gradually declining. Interestingly, my value factor remains relatively stable, so I'm wondering if there have been changes in how these metrics are calculated. Would be great to hear insights from others who have managed to improve their scores!

---

### 评论 #37 (作者: DD24306, 时间: 1年前)

By optimizing your individual alphas and ensuring proper diversification, you should see an improvement in both the combined alpha performance and selected alpha performance. Focus on consistency and risk management, as these will likely help improve your overall results.

---

### 评论 #38 (作者: AK40989, 时间: 1年前)

To enhance your combined alpha performance and combined selected alpha performance, focusing on the quality and diversity of your submitted alphas is crucial. Submitting high-quality, low-correlation alphas can help mitigate the impact of drawdowns and improve overall performance metrics. Additionally, have you considered the effects of transaction costs and slippage on your strategies? Minimizing these factors can significantly boost your net returns. What strategies are you currently employing to ensure your alphas remain robust across varying market conditions.

---

### 评论 #39 (作者: SK90981, 时间: 1年前)

Provide high-quality, low-correlation alpha since CombinePerformance and CombineSelectedPerformance rely on performance alpha.

---

### 评论 #40 (作者: DK30003, 时间: 1年前)

This helps prevent consultants from using data outside their level's scope, which could lead to suboptimal analysis or overfitting, as more complex datasets may not be appropriate for lower-level analysts.

---

