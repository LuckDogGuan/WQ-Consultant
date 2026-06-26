# [Alpha Inspiration] Combining Fundamental FSCORE and Equity Short-Term ReversalsAlpha Idea

- **链接**: [L2] [Alpha Inspiration] Combining Fundamental FSCORE and Equity Short-Term ReversalsAlpha Idea.md
- **作者**: TN48752
- **发布时间/热度**: 2年前, 得票: 24

## 帖子正文

**Paper:**  Noise Trading, Slow Diffusion of Information, and Short-Term Reversals: A Fundamental Analysis Approach

**Authors:** Zhu, Zhaobo and Sun, Licheng and Chen, Min

**Link:**  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3097420](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3097420)

**FSCORE:**

![图片](images/img_21643fe5ae.png)

There are three reasons to use FSCORE. Firstly, FSCORE is a comprehensive metric of a firm’s fundamental strength, because this score synthesizes information from nine signals along three dimensions of a firm’s financial performance (profitability, change in financial leverage and liquidity, and change in operational efficiency). Secondly, the fundamental information is gathered directly from the financial statements, which obviates the measurement error problem. And lastly, FSCORE is a nonparametric measure, compared with a parametric approach, FSCORE is more robust and helps to reduce concerns over potential estimation biases. Results support the hypothesis that short-term reversals are influenced by both noise trading and investor underreaction to fundamental information. Also results from regression analysis suggest that both noise trading and fundamental information significantly influence stock returns on the short horizon. No doubt, there is a conclusion that investor underreaction to fundamental information coupled with noise trading can explain the observed empirical patterns in short-term reversals. Moreover, results indicate that the bid-ask spread cannot be the main source of the profitability for short-term reversals, and the results are not particularly sensitive to alternative definitions of fundamental strength. Last but not least, simple short-term reversal and industry-adjusted reversal strategies fail to be profitable in the presence of transaction costs; however, fundamental anchored reversal strategies are economically profitable even in the presence of transaction costs.

**Alpha idea:**

The range of FSCORE is from zero to nine points. Each signal is equal to one (zero) point if the signal indicates a positive (negative) financial performance. A firm scores one point if it has realized a positive return-on-assets (ROA), positive cash flow from operations, a positive change in ROA, a positive difference between net income from operations (Accrual), a decrease in the ratio of long-term debt to total assets, a positive change in the current ratio, no-issuance of new common equity, a positive change in gross margin ratio and lastly a positive change in asset turnover ratio. Firstly, construct a quarterly FSCORE using the most recently available quarterly financial statement information.

![图片](images/img_4a2d434b3b.png)

Monthly reversal data are matched each month with a most recently available quarterly FSCORE. The firm is classified as a fundamentally strong firm if the firm’s FSCORE is greater than or equal to seven (7-9), fundamentally middle firm (4-6) and fundamentally weak firm (0-3). Secondly, identify the large stocks subset – those in the top 40% of all sample stocks in terms of market capitalization at the end of formation month t. After that, stocks are sorted on the past 1-month returns and firm’s most recently available quarterly FSCORE. Take a long position in past losers with favourable fundamentals (7-9) and simultaneously a short position in past winners with unfavourable fundamentals (0-3). The strategy is equally weighted and rebalanced monthly.

**Datafields:**

Fscore: fscore_total

return on assets: return_assets

Cash Flow From Operations - mean of estimations: anl4_cfo_mean

net income: income

debt: debt

assets: assets

current_ratio: current_ratio

gross margin: rsk62_beta_5_100_margin

**Equation** : F = Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9

**Improvement Hint:** Use scale or normalize to combine factors, removing outliers via winstorize()

---

## 讨论与评论 (11)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi!

Thank you for sharing! Have you checked, if any from Q1...Q9 an alpha itself?

---

### 评论 #2 (作者: TN48752, 时间: 2年前)

Thank you for asking. I tested each Q and found that there are some that can give a clear signal when placed individually. For example assets

![图片](images/img_041c9de354.png)

I've also found that it's a good idea to try each Q individually before using a linear function that combines the Qs.

---

### 评论 #3 (作者: AG20578, 时间: 2年前)

This is great to hear!

Also, instead of using linear combination, you can try and combine these alphas inside of SuperAlpha with some combo expression

---

### 评论 #4 (作者: PN39025, 时间: 1年前)

Let me ask you, seeing that your last 2 years of Sharpe were quite low, will this be a good alpha in the future? Thank you very much for sharing.

---

### 评论 #5 (作者: XD81759, 时间: 1年前)

Hey! That's an interesting alpha idea. Using FSCORE combined with short-term reversals makes sense. The way you construct the quarterly FSCORE based on those financial signals is solid. Sorting stocks by past 1-month returns and FSCORE for long and short positions is a good strategy. And the tip on using scale or normalize to combine factors and deal with outliers by winzorize is great. Just make sure the data accuracy for those datafields like fscore_total, return_assets etc. is high during backtesting.

---

### 评论 #6 (作者: XL31477, 时间: 1年前)

**Hey! Thanks for all the comments here. Regarding the concern about the low Sharpe ratio in the past two years, it might not mean it won't be good in the future. Sometimes, market conditions change. We could further optimize the strategy by maybe adjusting the time period for calculating FSCORE or the sorting criteria a bit. Also, keep refining the data cleaning process to enhance data accuracy for better performance. That might help improve its potential in the future.**

---

### 评论 #7 (作者: DN45758, 时间: 1年前)

This paper provides a groundbreaking approach by integrating FSCORE into reversal strategies, offering actionable insights on exploiting noise trading and investor underreaction for robust, transaction-cost-resistant profitability.

---

### 评论 #8 (作者: BA51127, 时间: 1年前)

**FSCORE as a Fundamental Metric** : FSCORE is a comprehensive, nonparametric measure of a firm's financial health, derived from nine signals across profitability, financial leverage, liquidity, and operational efficiency. It's seen as robust and less prone to estimation biases.
 **Strategy Implementation** : The strategy involves constructing a quarterly FSCORE and classifying firms as strong, medium, or weak based on their scores. Stocks are then sorted by past 1-month returns and FSCORE, with long positions taken in past losers with high FSCOREs and short positions in past winners with low FSCOREs.
 **Data Accuracy and Refinement** : Ensuring high data accuracy for fields like fscore_total and return_assets is crucial during backtesting. The use of scaling, normalization, and winsorizing to handle outliers is recommended to improve the strategy's robustness.

---

### 评论 #9 (作者: CC40930, 时间: 1年前)

This alpha strategy leveraging FSCORE to combine fundamental analysis with short-term reversal strategies is quite insightful. By using FSCORE, you are systematically incorporating a wide range of financial performance metrics, making the strategy robust and less prone to biases that can arise from more traditional methods. The approach of sorting stocks based on past returns and fundamental strength offers a clear framework to capture reversals while maintaining a strong link to financial health. Additionally, targeting large-cap stocks improves liquidity and stability in the strategy. Rebalancing monthly helps in managing risk and adjusting positions based on the most recent fundamental data. This seems like a promising approach that balances both fundamentals and price momentum effectively.

---

### 评论 #10 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #11 (作者: CS12450, 时间: 1年前)

### [Alpha Inspiration] Combining Fundamental FSCORE and Equity Short-Term Reversals

**Title and Author of the Article:**

- *The Value of Financial Statement Analysis*  by Piotroski (2000)

**Alpha Inspiration Description:**

- The FSCORE, introduced by Piotroski, is a fundamental score that evaluates a company's financial strength based on key ratios (such as profitability, leverage, and efficiency). Stocks with high FSCORE tend to outperform low FSCORE stocks, as they are deemed financially healthier and more likely to achieve superior returns.
- The concept of equity short-term reversals suggests that stocks that have performed poorly in the short term (e.g., over the past 1 to 3 months) tend to reverse and show positive returns, while stocks that have recently performed well tend to underperform in the near term.
- The idea is to combine these two concepts by selecting stocks with a high FSCORE (strong fundamentals) but that have experienced short-term underperformance (e.g., negative returns over the past 1-3 months). These stocks may represent good opportunities for a short-term reversal, offering a potential profit when they return to their long-term fundamentals.

**Related Dataset:**

- **Piotroski FSCORE dataset**  or  **Fundamentals Dataset** : Data fields related to profitability, leverage, and efficiency ratios (ROA, current ratio, gross margin, etc.).
- **Equity Returns Data** : Daily, weekly, or monthly price data to calculate short-term returns for the reversal strategy.

**(Optional) Current Performance of P&L or Matrix:**

- Backtest the strategy by identifying stocks with high FSCORE and negative short-term returns, then track their performance in the subsequent 1-3 months.
- Assess the strategy's performance using key metrics like cumulative returns, Sharpe ratio, and maximum drawdown.

**Questions and Improvement Ideas:**

- Would incorporating technical indicators, such as moving averages, enhance the accuracy of short-term reversal signals?
- How might incorporating macroeconomic factors (e.g., interest rates, GDP growth) impact the performance of this combined strategy?
- Could a more granular screening process (e.g., looking at different sectors or industries) improve the alpha generation?

**Tag:**  Alpha Idea

This idea is a combination of two well-known strategies: using fundamental analysis (FSCORE) to select strong companies and using short-term price momentum to capture reversals. It should generate interesting results when backtested and could be refined further through risk management or factor diversification

---

