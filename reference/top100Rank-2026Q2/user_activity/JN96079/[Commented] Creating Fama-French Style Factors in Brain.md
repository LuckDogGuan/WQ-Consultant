# Creating Fama-French Style Factors in Brain

- **链接**: [Commented] Creating Fama-French Style Factors in Brain.md
- **作者**: AK40989
- **发布时间/热度**: 9个月前, 得票: 35

## 帖子正文

I’ve been thinking about whether it’s possible to build something like a Fama-French factor inside Brain. For example, a size factor based on market capitalization, or factors that mimic their cross-sectional return sorting approach. I haven’t seen an operator that directly classifies by market cap, so I’m wondering how close we can get to replicating these kinds of factors on the platform.
Has anyone here tried building Fama-French style factors, and if so, what approaches worked best?

---

## 讨论与评论 (9)

### 评论 #1 (作者: JN96079, 时间: 9个月前)

Hey,  [AK40989](/hc/en-us/profiles/26422151767703-AK40989) , you can build Fama-French–style factors in  BRAIN. The platform exposes cross-sectional ranking, time-series operators, and quantile/scale operators (e.g.  **`rank`** ,  **`ts_rank`** ,  **`quantile`** ,  **`scale`** ,  **`winsorize`** ) and plenty of data fields, so you can reproduce the FF-style sorts (size, value, small-minus-big, high-minus-low) as long as the needed data fields (market  ***cap***  or shares outstanding, book value or bps, etc.) are available for your universe.

---

### 评论 #2 (作者: AF65023, 时间: 9个月前)

Interesting idea! While BRAIN doesn’t have a direct market cap operator, you can approximate Fama-French style factors by ranking  **alphas**  on proxies (e.g., size, value, momentum) and building long-short portfolios across those ranks. Essentially, think in terms of  **factor-mimicking portfolios** —long top-ranked, short bottom-ranked—and let the platform handle construction.

---

### 评论 #3 (作者: SY65468, 时间: 9个月前)

Great question! While Brain doesn’t allow strict Fama-French bucket sorts, you can approximate them with continuous signals. For example, book-to-price can stand in for value, and rolling  `ts_rank`  on returns works for momentum. You can also blend multiple signals (like value + momentum), use  `ts_arg_max/min`  or rolling medians to reduce noise, and experiment with different lookback periods to build smoother, more robust factor tilts.

---

### 评论 #4 (作者: TP85668, 时间: 9个月前)

Interesting question! While Brain doesn’t have a direct “market cap sort” operator, you can approximate Fama-French style factors by using available fields like  `market_cap` , then applying ranking, grouping, or quantile-based operators (e.g.,  `rank` ,  `bucket` ,  `group_neutralize` ). For SMB-like signals, try long small-cap and short large-cap groups. Combining with book-to-market or momentum fields could get you close to the classic 3-factor setup.

---

### 评论 #5 (作者: AG14039, 时间: 9个月前)

Great question! Although Brain doesn’t offer a built-in “market cap sort” operator, you can approximate Fama-French style factors using existing fields like  `market_cap`  combined with ranking, bucketing, or group-based operators (e.g.,  `rank` ,  `bucket` ,  `group_neutralize` ). For an SMB-like approach, you could go long on small-cap groups and short on large-cap groups. Pairing this with book-to-market or momentum variables can help recreate something close to the traditional three-factor model.

---

### 评论 #6 (作者: JO81736, 时间: 9个月前)

In WorldQuant Brain, strict Fama-French bucket sorts aren’t available, but you can approximate factors using continuous signals, rolling ranks, and blended signals to create smoother, more robust style factor tilts.

---

### 评论 #7 (作者: JK98819, 时间: 9个月前)

I’ve also been exploring Fama-French style factors in Brain and found that thinking in terms of  *factor-mimicking signals*  rather than exact bucket sorts works best. Combining fields like  `market_cap`  or  `shares_outstanding`  with  `rank` ,  `quantile` , or  `group_neutralize`  lets you approximate SMB, HML, or momentum tilts fairly closely. Blending multiple ranked signals (e.g., size + value) and testing different lookback windows can produce surprisingly robust factors that behave much like the classic FF factors.

---

### 评论 #8 (作者: LB76673, 时间: 9个月前)

You can approximate Fama-French factors by using available market cap fields and ranking functions like  `ts_rank`  or  `rank`  to split stocks into size buckets. For value or momentum factors, combine fundamentals or price signals and use cross-sectional ranking to mimic the long-short sorting. Applying group-neutralization by sector or industry helps reduce bias. While it’s not a direct replication, careful ranking and weighted exposure can create similar factor-like behavior in Brain.

---

### 评论 #9 (作者: HN45379, 时间: 9个月前)

This is a very relevant point. I agree that Brain doesn’t provide a direct “size sort” operator, but the spirit of Fama-French factors can still be captured. For example, rank(cap) can approximate size-based groupings, while bucket or group operators allow cross-sectional sorting similar to their original framework. Combining these with return-based metrics helps mimic value or momentum tilts. I think your post highlights an important connection: even though Brain isn’t designed around academic factors, many of their principles can be adapted with creativity.

---

