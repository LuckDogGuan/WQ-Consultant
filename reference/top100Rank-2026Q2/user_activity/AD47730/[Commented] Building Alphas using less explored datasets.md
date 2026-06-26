# Building Alphas using less explored datasets

- **链接**: [Commented] Building Alphas using less explored datasets.md
- **作者**: GS69213
- **发布时间/热度**: 2个月前, 得票: 8

## 帖子正文

How do you approach on building alphas using less explored datasets like insiders, institution etc. I am finding it very difficult to build alphas using these datasets can anyone share some tips regarding this.

---

## 讨论与评论 (11)

### 评论 #1 (作者: RM79380, 时间: 2个月前)

Kindly refer to this  [../CC40930/[L2] Getting started with News DatasetsResearch.md](../CC40930/[L2] Getting started with News DatasetsResearch.md)

You'll have an idea on how to tackle them.

---

### 评论 #2 (作者: PN39025, 时间: 2个月前)

Hi ,The important thing is to find signals within those datasets. If the signal is too weak, you have to combine it with signals from other datasets within the set or from external data. That's my experience.

---

### 评论 #3 (作者: MH52691, 时间: 2个月前)

This is quite insightful!

---

### 评论 #4 (作者: ML46209, 时间: 2个月前)

This is a fantastic and timely question! Transitioning from more common datasets to less explored ones like insider/institutional activity definitely presents unique challenges. Have you considered focusing on the *timing* and *frequency* of these trades as potential alpha signals, rather than just the absolute volume? Sometimes the subtle shifts are more predictive.

---

### 评论 #5 (作者: KP26017, 时间: 2个月前)

The solution is treating these as event-based signals rather than continuous signals. Instead of asking "what is the current insider signal value" ask "how long since the last insider event and what was its character." Fields like days since last insider purchase, cumulative insider buying over rolling windows, or change in institutional concentration since last reporting date naturally handle the sparsity because they carry forward information between events rather than going to zero when nothing is happening.

---

### 评论 #6 (作者: DT49505, 时间: 2个月前)

This is a great challenge, GS69213! I've found that the key with less explored datasets like insider/institutional trades often lies in carefully considering the *timing* and *context* of the data points. For instance, are you looking at aggregate patterns of insider buying/selling over a quarter, or focusing on specific key executives and their transactions? Perhaps it's also worth exploring the *frequency* of updates for these datasets – the latency can sometimes mask real alpha.

---

### 评论 #7 (作者: CM46415, 时间: 2个月前)

Less explored datasets need careful handling. Focus on changes not levels, filter meaningful signals, use lagged reactions, combine with liquidity filters, and validate with price behavior to ensure robust alpha signals.

---

### 评论 #8 (作者: SP39437, 时间: 2个月前)

Great topic, GS69213! When tackling less explored datasets like insider/institutional activity, I often find success by focusing on identifying unique *patterns* of behavior rather than just raw signals. Have you considered time-series analysis of their trading frequencies or specific order types to uncover more nuanced alpha signals?

---

### 评论 #9 (作者: TL72720, 时间: 2个月前)

This is a really interesting challenge, GS69213! Navigating less explored datasets like insider/institutional filings often requires a different lens than traditional price/volume data. Have you found success in filtering these events for specific transaction sizes or ownership changes, or perhaps looking at lags and decay in their impact? I've found that focusing on the *change* in ownership percentage rather than absolute levels can sometimes be more predictive.

---

### 评论 #10 (作者: AD47730, 时间: 2个月前)

Thats a brilliant idea.

---

### 评论 #11 (作者: VT42441, 时间: 2个月前)

This is a great point, GS69213. I've found that a key challenge with less explored datasets like insider/institutional filings is the sheer noise and data quality issues. Have you explored techniques for filtering and imputing missing values specific to these types of transactional data before feature engineering? Sometimes, a robust data cleaning pipeline is the first alpha-generating step itself.

---

