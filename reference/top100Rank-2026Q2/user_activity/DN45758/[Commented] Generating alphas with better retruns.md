# Generating alphas with better retruns.

- **链接**: [Commented] Generating alphas with better retruns.md
- **作者**: LS84247
- **发布时间/热度**: 1年前, 得票: 1

## 帖子正文

How can someone generate alphas with higher returns but lower turnover?

---

## 讨论与评论 (22)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Hi, there are some operators that will make return increase and tunover decrease, for example, the operator ts_target_tvr_delta_limit(x, y, lambda_min=0, lambda_max=1, target_tvr=0.1) helps you do that easily. More importantly, the formula for calculating tunover and return is inversely proportional, so it's quite easy.

---

### 评论 #2 (作者: SD99406, 时间: 1年前)

PN39025

Hey, this very nice explanation,

---

### 评论 #3 (作者: AK40989, 时间: 1年前)

Optimizing for both return and low turnover can feel like walking a tightrope. I’ve found that using smoothing operators like  `decay_linear` ,  `ts_mean` , or  `ts_lag`  can help reduce excessive rebalancing while preserving signal strength. Also, being selective with universes and neutralizations (like avoiding overly volatile or illiquid subsets) can make a big difference.

Would love to hear if others have discovered specific operator combos or structures that consistently lower TVR without hurting performance.

---

### 评论 #4 (作者: AC63290, 时间: 1年前)

I also cope with this problem. how to solve it

---

### 评论 #5 (作者: NH84459, 时间: 1年前)

- Use  **medium- to long-horizon signals**  (e.g., 10–90 day signals) instead of daily ones.
- Favor  **rank-based**  signals over raw-value ones, which are often more robust across time and markets.

---

### 评论 #6 (作者: SG91420, 时间: 1年前)

Make use of basic elements such as quality measurements, dividend yield, earnings growth, macroeconomic indicators, and valuation (P/E). These promote lesser turnover and change gradually.
To create portfolios that are less likely to balance and are risk-efficient, use risk models.

---

### 评论 #7 (作者: NS23220, 时间: 1年前)

you can try increasing the decay or using operators like hump_decay() or ts_target_tvr_delta_limit(x, y, lambda_min=0, lambda_max=1, target_tvr=0.1)  to make alphas

---

### 评论 #8 (作者: HD25387, 时间: 1年前)

Thanks for the great tips! I’ve also found that using smoother signals — like rolling averages or smoothed momentum — helps reduce turnover while still capturing strong returns. Combining medium-term signals with turnover-limiting operators like  `ts_target_tvr_delta_limit`  can create more stable Alphas. It also helps to backtest in multiple regions to ensure signal consistency. Has anyone tried incorporating macroeconomic features or sector-based filters to enhance return while maintaining low turnover?

---

### 评论 #9 (作者: DT49505, 时间: 1年前)

This thread brings up some insightful strategies for balancing higher returns with lower turnover. I’d like to add that incorporating signal smoothing techniques—such as exponential moving averages or Kalman filters—can further stabilize alpha signals and reduce noise-induced trading. Additionally, layering in volatility scaling can enhance risk-adjusted returns without necessarily increasing turnover. Sector-neutral or industry-relative features can also improve signal robustness. It's important to consider the interaction between features and constraints like turnover limits during optimization. Has anyone experimented with cross-sectional residuals after regressing out macro or sector exposures to isolate purer alpha signals while keeping churn low?

---

### 评论 #10 (作者: NV31424, 时间: 1年前)

–  **Smooth signals** : lengthen your decay half-life or use longer look-back z-scores/moving averages to dampen noise.
–  **Thresholded trading** : only rebalance when your signal change exceeds a set threshold, or rebalance less often (e.g. every 5 days).

---

### 评论 #11 (作者: LM22798, 时间: 1年前)

Certain operators are specifically designed to help increase returns while simultaneously reducing turnover. For instance, the  `ts_target_tvr_delta_limit(x, y, lambda_min=0, lambda_max=1, target_tvr=0.1)`  operator is a practical tool for achieving this balance. It simplifies the process of optimizing for higher returns without incurring excessive portfolio turnover. This is particularly effective because, in many cases, the formulas for calculating return and turnover are inversely related—meaning that a well-tuned adjustment can enhance one while reducing the other.

---

### 评论 #12 (作者: ML46209, 时间: 1年前)

In my experience, one effective way to generate alphas with high returns and low turnover is to combine medium-term signals with stable filters like weighted moving averages. Instead of relying solely on  `ts_target_tvr_delta_limit` , I often add minimum holding period constraints (e.g., holding positions for at least 5 days) to avoid unnecessary trades. I've also experimented with incorporating macroeconomic variables like PMI or expected inflation — when integrated properly, they can enhance returns without significantly increasing turnover.

---

### 评论 #13 (作者: LB76673, 时间: 1年前)

Some operators are specifically built to boost returns while lowering turnover at the same time. For example, the ts\_target\_tvr\_delta\_limit(x, y, lambda\_min=0, lambda\_max=1, target\_tvr=0.1) operator is a useful tool for striking this balance. It makes it easier to optimize for higher returns without causing too much portfolio turnover. This works well because, in many situations, the calculations for return and turnover tend to move in opposite directions—so a carefully adjusted setting can improve returns while cutting turnover.

---

### 评论 #14 (作者: JB26214, 时间: 1年前)

Generate alphas with better returns by combining alternative data, machine learning models, robust backtesting, risk management, and continuous model refinement.

---

### 评论 #15 (作者: NS62681, 时间: 1年前)

Balancing return optimization with low turnover can be a delicate act. In my experience, applying smoothing functions such as  `decay_linear` ,  `ts_mean` , or  `ts_lag`  helps curb unnecessary rebalancing while maintaining the integrity of the signal.

---

### 评论 #16 (作者: SC43474, 时间: 1年前)

A key to balancing higher returns with lower turnover lies in blending signal horizons and carefully selecting operators. Medium- to long-term signals reduce noise and unnecessary rebalancing, while operators like ts_target_tvr_delta_limit provide direct control over turnover targets without sacrificing performance. Combining this with universe filtering—focusing on stable, liquid stocks—and applying smoothing functions like decay_linear or ts_mean can create more robust, efficient alphas. It’s about thoughtful layering: signal design, operator tuning, and universe choice working together rather than relying on a single fix.

---

### 评论 #17 (作者: AC63290, 时间: 1年前)

To generate alphas with higher returns and lower turnover, focus on selecting stable, long-term predictive factors rather than short-term signals. Use techniques like smoothing or longer holding periods, minimize frequent trading triggers, and incorporate robust risk management to reduce unnecessary trades while maintaining strong performance and return consistency.

---

### 评论 #18 (作者: AG14039, 时间: 1年前)

Hi! Some operators are designed to help increase return while reducing turnover—one example is  `ts_target_tvr_delta_limit(x, y, lambda_min=0, lambda_max=1, target_tvr=0.1)` , which makes this balance easier to achieve. More importantly, since the formulas for return and turnover are inversely related, optimizing for one can often positively influence the other.

---

### 评论 #19 (作者: AG14039, 时间: 1年前)

Incorporate fundamental factors like quality metrics, dividend yield, earnings growth, macro indicators, and valuation ratios (like P/E), as these typically result in lower turnover due to their gradual shifts. To build more stable and risk-efficient portfolios, consider applying risk models to guide your construction process.

---

### 评论 #20 (作者: SD92473, 时间: 1年前)

When constructing trading signals, prioritizing medium- to long-horizon timeframes typically yields more stable and reliable results than short-term approaches. Signals spanning 10 to 90 days allow sufficient time for fundamental market dynamics to unfold while filtering out much of the noise inherent in daily price movements. This extended timeframe helps capture meaningful trends and patterns that reflect underlying economic forces rather than temporary market fluctuations or random volatility that can dominate shorter periods.

---

### 评论 #21 (作者: PY74849, 时间: 1年前)

Generating alphas with better returns involves systematically identifying and exploiting predictable patterns in asset prices to produce excess returns (alpha) over a benchmark. Here's how you can approach it, depending on your goals (quantitative, discretionary, or hybrid):

---

### 评论 #22 (作者: DN45758, 时间: 1年前)

Absolutely, balancing return and low turnover is tricky! Smoothing operators like  `decay_linear` ,  `ts_mean` , and  `ts_lag`  are great for taming turnover without losing signal punch. Selective universe choices and thoughtful neutralization definitely help too. Others often use combos like  `ts_decay`  with  `group_rank`  or  `ts_smooth`  paired with  `delay` —have you tried those? Curious what operator mixes others swear by to keep turnover down while maintaining strong performance!

---

