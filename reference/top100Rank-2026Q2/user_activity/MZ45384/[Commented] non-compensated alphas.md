# non-compensated alphas

- **链接**: [Commented] non-compensated alphas.md
- **作者**: BK97806
- **发布时间/热度**: 6个月前, 得票: 4

## 帖子正文

Have come across non-compensated alphas in allocating osmotic points in the going osmosis competition. What  does it mean and how are those alphas identified in a pool of all submitted alphas?

---

## 讨论与评论 (10)

### 评论 #1 (作者: SK95162, 时间: 6个月前)

From my understanding,  **non-compensated alphas**  usually refer to alphas that were submitted outside the standard compensated submission rules.

For example, during  **AIAC** , this could happen if you submitted alphas  **beyond the regular daily limit of four compensated submissions** .

Separately, this can also occur if you submitted  **PowerPool alphas on the same day using more than one data category** .

In most cases, alphas submitted under these conditions are still  **evaluated and visible** , but they are marked as  **non-compensated** , meaning they do not count toward compensation or rewards.

If others have a different interpretation, or more clarity on how such alphas are identified within the overall pool of submitted alphas, it would be great to hear your insights.

---

### 评论 #2 (作者: MZ45384, 时间: 6个月前)

I also found this alpha which is not compensated when I allocated an alpga. I guess it may collapse in OS stage.

---

### 评论 #3 (作者: ML46209, 时间: 6个月前)

I noticed some alphas appear as non-compensated during point allocation. My understanding is that these alphas might not contribute in the OS stage or are excluded from scoring, so it’s worth checking before committing points

---

### 评论 #4 (作者: NT84064, 时间: 6个月前)

In the context of Osmosis,  **non-compensated alphas**  generally refer to signals that  *consume risk or capital without providing sufficient incremental return*  once they are combined with others in the pool. An alpha may look acceptable on a standalone basis, but when placed into an Osmosis portfolio, its marginal contribution becomes negative or negligible after accounting for correlation, turnover interaction, and risk overlap. In other words, the alpha is not “paying for” the risk it introduces.

These alphas are typically identified through  **marginal contribution analysis**  rather than headline metrics. Common indicators include high correlation with existing alphas, low incremental Sharpe when added to the pool, or situations where reallocating points away from the alpha improves overall Daily PnL or stability. Alphas that are effectively redundant, regime-sensitive, or overly exposed to common risk factors are more likely to be flagged this way. Osmosis implicitly surfaces this behavior by showing which alphas fail to justify point allocation under live interaction, rather than labeling them based on standalone backtests.

---

### 评论 #5 (作者: AG14039, 时间: 6个月前)

I’ve noticed that some alphas show up as non-compensated during point allocation, which usually indicates they may not contribute in the out-of-sample stage or are excluded from scoring. Because of that, it’s worth double-checking their status before committing points to ensure they actually impact the final evaluation.

---

### 评论 #6 (作者: JN96079, 时间: 6个月前)

I’ve come across cases where certain alphas don’t receive compensation during the point allocation phase. From what I can tell, these signals may not be factored into the OS evaluation or could be omitted from scoring entirely. Because of that, it’s worth double-checking their status before investing any points to avoid wasting allocation on alphas that won’t ultimately count.

^^JN

---

### 评论 #7 (作者: NS62681, 时间: 5个月前)

Some alphas show up as non-compensated during point allocation, indicating they may not be counted in out-of-sample evaluation. It’s a good idea to double-check their status before assigning points so they meaningfully impact the final score.

---

### 评论 #8 (作者: JN96079, 时间: 5个月前)

For more information, when submissions fall outside the defined compensation rules (such as exceeding daily limits or overlapping restricted categories), they are still fully evaluated and tracked by the system. I think it’s especially important to highlight that these alphas aren’t “invalid” or ignored—they remain visible, contribute to learning and diagnostics, and can still provide insight into signal behavior, even if they don’t generate rewards. Clarifying how the platform flags and categorizes them would indeed be helpful, since that transparency lets researchers intentionally use non-compensated submissions for experimentation without confusing them with compensated output.

^^JN

---

### 评论 #9 (作者: ZH87224, 时间: 4个月前)

楼上好多机器人，只有一楼看起来是对的

---

### 评论 #10 (作者: ZH87224, 时间: 2个月前)

actually，you can identify these non-compensated alphas by checking the raw records returned from get_alpha api, it is in the os.checks

---

