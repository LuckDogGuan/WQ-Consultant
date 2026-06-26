# Datasets for Noise Suppression in Delay-0 Alphas

- **链接**: Datasets for Noise Suppression in Delay-0 Alphas.md
- **作者**: BM29781
- **发布时间/热度**: 9个月前, 得票: 7

## 帖子正文

Noise in delay-0 alphas comes from reacting too strongly to single-day price changes. To mitigate this, use datasets and features that evolve more smoothly over time:

### 1.  **Fundamental & Ratio-Based Data**

- Examples:  `sales/assets` ,  `est_netprofit` ,  `est_netdebt` .
- Why: Fundamentals are slower-moving and less reactive to daily volatility.
- Effect: Anchors alphas to structural, stable drivers of performance.

### 2.  **Volatility & Statistical Measures**

- Examples:  `ts_stddev` ,  `ts_skewness` ,  `ts_kurtosis` ,  `ts_entropy` , coskewness, cokurtosis.
- Why: Instead of raw price jumps, they capture distributional properties over a window.
- Effect: Suppresses day-to-day noise while highlighting persistent risk and asymmetry.

### 3.  **Cross-Sectional Grouping**

- Examples:  `group_neutralize` ,  `group_normalize` ,  `bucket` .
- Why: Comparing stocks within industries or buckets reduces idiosyncratic shocks.
- Effect: Smooths signals by focusing on relative rather than absolute movements.

---

## 讨论与评论 (1)

### 评论 #1 (作者: CM46415, 时间: 2个月前)

Solid breakdown—this is essentially noise reduction through structure, not just smoothing.

---

