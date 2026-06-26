# RELATED TO COMBINED OSMOSIS PERFORMANCE

- **链接**: [Commented] RELATED TO COMBINED OSMOSIS PERFORMANCE.md
- **作者**: SP61833
- **发布时间/热度**: 1个月前, 得票: 11

## 帖子正文

My  **Combined Osmosis Performance** has become negative. I did not made any drastic changes in the osmosis pool so what is the reason for this significant drop. Can anyone suggest how to improve it?

What type of alphas should be tagged to improve combined osmosis performance?

---

## 讨论与评论 (6)

### 评论 #1 (作者: RM79380, 时间: 1个月前)

Try tagging low correlated alphas

---

### 评论 #2 (作者: PD54914, 时间: 1个月前)

I think the two main things to focus on are robustness and after-cost performance.

This post might help for improving after-cost performance:  [How to Improve After-Cost Performance](../DL53864/[L2] How to Improve After Cost Performance置顶的.md?utm_source=chatgpt.com)

I applied some of these ideas and my last 3 Osmosis updates were around 2.72, 3.56, and 3.82.

---

### 评论 #3 (作者: YD84002, 时间: 1个月前)

A common practice is to select 15–20 high-quality Alphas per region.

This experience is informative:

- Around 10: may show strong upward momentum, but with higher volatility.
- 15–25: generally more balanced.
- 30+: more stable, but if quality varies widely, it can dilute the top signals.
- Selecting all: tends to introduce low-quality and highly correlated Alphas.

But the real factor is not the count—it’s the number of  **effectively independent Alphas** .

For example:

- 20 highly correlated Alphas may be equivalent to only a few effective signals.
- 8 low-correlation, high-quality Alphas could outperform 30 homogeneous Alphas.

If the overall quality in a particular region is poor, forcing a target count may be worse than using fewer Alphas or pausing participation.

Therefore, the number should be determined jointly by quality distribution, correlation matrix, and rule constraints.

---

### 评论 #4 (作者: DT49505, 时间: 1个月前)

I think low correlation is definitely an important factor, especially in Osmosis where diversification seems to play a major role in overall stability. From my experience, even a few highly correlated alphas can negatively affect combined performance over time. I also agree that after-cost robustness matters a lot, since some alphas may look strong individually but contribute poorly once combined. Recently, I’ve been trying to focus more on diversification across datasets, holding horizons, and turnover characteristics rather than only optimizing standalone metrics.

---

### 评论 #5 (作者: CW62782, 时间: 1个月前)

This can happen even without big changes. Combined Osmosis is not only about your current pool, but also how those tagged alphas behave recently and how much they still add together.

---

### 评论 #6 (作者: AD47730, 时间: 1个月前)

Uncorelated and simple and orthogonal alpha along with high sharpe and fitness.

---

