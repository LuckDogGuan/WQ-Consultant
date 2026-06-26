# [Question] Why does Value Factor decrease even when performance increases?

- **链接**: [Commented] [Question] Why does Value Factor decrease even when performance increases.md
- **作者**: LD50548
- **发布时间/热度**: 10个月前, 得票: 51

## 帖子正文

Recently, I noticed that both my Combined Alpha Performance and Combined Selected Alpha Performance have increased significantly, which means the overall alpha performance is improving. However, my Value Factor has decreased compared to previous quarters. I’m not sure if these two metrics are directly related, or if VF is also affected by other factors such as overlap, prod correlation, or sub-universe metrics. I’d like to ask if anyone has experienced a similar situation and how to analyze the reasons in order to keep VF stable.

---

## 讨论与评论 (10)

### 评论 #1 (作者: SG65105, 时间: 10个月前)

Same issue +1

---

### 评论 #2 (作者: TD40899, 时间: 10个月前)

Hi. As I understand it, the current month’s value factor is an aggregate result of alphas from the past three months, while the combined performance metrics are updated up to the most recent month. So it’s natural that these two indicators are not correlated.

---

### 评论 #3 (作者: DT49505, 时间: 10个月前)

This is a really insightful observation. From what I understand, Value Factor (VF) is calculated with its own methodology and time window, which doesn’t always move in sync with combined performance metrics. As TD40899 mentioned, VF tends to reflect a longer horizon (e.g., rolling three months), while combined alpha performance can react much faster to recent improvements. That time lag alone can create divergence between the two metrics. Beyond that, overlap and prod correlation can also influence VF, since heavy concentration in similar alphas can reduce the “quality” assessment even if overall performance is rising. One way to analyze this is to break down contributions from different alpha groups, checking for redundancy or skewed weightings that might be suppressing VF. Monitoring sub-universe performance could also reveal whether recent gains are concentrated in narrower areas, which VF might penalize. I’d be curious if anyone has tried systematically tracking the relationship between VF trends and correlation metrics to pinpoint the exact drivers.

---

### 评论 #4 (作者: HD25387, 时间: 10个月前)

A rise in  **overall alpha performance**  doesn’t always translate into a higher  **Value Factor (VF)** , since VF depends on more than just returns. It can also be affected by:

- **Overlap & redundancy**  – if new alphas improve performance but are highly correlated, VF can fall.
- **Production correlation**  – stronger performance with higher cross-correlation can reduce VF stability.
- **Sub-universe effects**  – changes in coverage, liquidity filters, or weighting schemes may shift VF.

In short, VF measures  **uniqueness and robustness** , not just raw performance. To keep it stable, analyze  **correlation structure, alpha overlap, and sub-universe consistency**  alongside performance.

---

### 评论 #5 (作者: DL51264, 时间: 10个月前)

I’ve seen that happen too. The rise in Combined Alpha and Selected Alpha doesn’t always translate into a stronger Value Factor, since VF also depends a lot on overlap, correlation among your alphas, and how stable they are in different sub-universes. Sometimes a boost in raw performance can actually lower VF if it comes with more redundancy or concentration. A good way to diagnose is to check prod correlation, overlap metrics, and whether a few strong alphas are dominating too much—balancing those tends to keep VF from drifting down even when headline performance improves.

---

### 评论 #6 (作者: AG14039, 时间: 10个月前)

The current month’s value factor reflects the aggregated results of alphas from the past three months, whereas the combined performance metrics are updated through the most recent month. That’s why it’s normal for these two measures to show little correlation.

---

### 评论 #7 (作者: TP85668, 时间: 10个月前)

Good question 👍. It makes sense that Alpha performance can improve while Value Factor decreases, since VF captures more than just raw performance. It’s also influenced by overlap between signals, product correlation, sub-universe coverage, and weighting effects. I’d suggest comparing recent quarters, checking signal correlations, and breaking down contributions by Alpha to see which factors are driving the VF drop.

---

### 评论 #8 (作者: TP18957, 时间: 9个月前)

This is a really important question because it highlights how Value Factor (VF) and Combined Alpha Performance measure different aspects of your inventory. Performance metrics—Combined Alpha and Combined Selected Alpha—capture the raw return quality, but VF is more of a  *structural robustness score* . It aggregates results over a longer horizon (usually ~3 months) and accounts for overlap, product correlation, and breadth across sub-universes. That’s why VF can decrease even when headline performance rises: if your improvements come from a few highly correlated alphas, VF may penalize the lack of diversity. Similarly, if performance gains are concentrated in specific sub-universes, VF will reflect weaker generalizability. A practical approach is to break down correlation matrices, examine redundancy in your portfolio, and ensure strong alphas are not overly dominating. In essence, VF rewards breadth, independence, and stability, not just short-term gains.

---

### 评论 #9 (作者: TP18957, 时间: 9个月前)

Thanks for raising this question—it’s something many of us have probably noticed but not articulated so clearly. I really appreciate how you pointed out the divergence between Combined Performance and Value Factor, because it reminds me that success on the platform isn’t just about boosting returns but also about maintaining balance and diversity across alphas. Reading through the responses, I now understand better that VF captures structural elements like overlap, correlation, and sub-universe stability, rather than just short-term performance. That perspective is very helpful, and I’ll definitely start paying closer attention to redundancy and breadth when evaluating my own signals. Really grateful you sparked this discussion—it’s both practical and eye-opening.

---

### 评论 #10 (作者: RP41479, 时间: 9个月前)

Higher alpha performance doesn’t always boost Value Factor (VF), which reflects uniqueness and robustness. VF can drop due to correlated alphas, production correlation, or sub-universe shifts. Monitoring overlap, correlations, and coverage.

---

