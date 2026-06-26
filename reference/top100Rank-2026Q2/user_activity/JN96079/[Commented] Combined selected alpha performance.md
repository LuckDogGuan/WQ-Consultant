# Combined selected alpha performance

- **链接**: [Commented] Combined selected alpha performance.md
- **作者**: TP19085
- **发布时间/热度**: 10个月前, 得票: 51

## 帖子正文

Could you please explain how to increase Combined Selected Alpha Performance? I noticed that my Combined Alpha Performance is > 2, but Combined Selected Alpha Performance is still < 0 — how can that happen?

---

## 讨论与评论 (6)

### 评论 #1 (作者: TP85668, 时间: 10个月前)

This can happen because Combined Alpha Performance (CAP) measures the performance of  *all*  your alphas, while Combined Selected Alpha Performance (CSAP) only measures the subset you’ve actively selected. If your selection contains underperforming alphas — even if your overall library is strong — CSAP can be negative. To improve it, review and prune low-performing selections, monitor OS stability, and control correlation so that your chosen set is both high-quality and complementary.

---

### 评论 #2 (作者: NN29533, 时间: 10个月前)

Hi friend, this situation can occur because Combined Alpha Performance (CAP) reflects the overall performance of your entire alpha library, whereas Combined Selected Alpha Performance (CSAP) focuses only on the specific subset of alphas you have actively deployed. As a result, even if your complete library performs well, CSAP can still turn negative if the chosen subset includes underperforming alphas. This typically means that selection quality, rather than total alpha quality, is the issue. To address this, it’s important to regularly review your selected alphas, prune those with weak or inconsistent performance, and ensure that the remaining ones maintain strong out-of-sample (OS) stability. Additionally, pay close attention to correlation management — excessive overlap among alphas can dilute returns, even if each alpha looks good individually. By focusing on both quality and complementarity in your selection, you can improve CSAP and maintain consistent performance over time.

---

### 评论 #3 (作者: LB76673, 时间: 10个月前)

The Combined Selected Alpha Performance (CSAP) on the WorldQuant BRAIN platform reflects the aggregated performance of your top-performing alphas selected for their contribution to a portfolio, emphasizing low correlation and high fitness. A CSAP < 0 despite a Combined Alpha Performance (CAP) > 2 suggests that while your overall alpha portfolio is strong (high CAP), the selected alphas may have high correlations, low stability, or insufficient diversification, leading to poor collective performance. To boost CSAP, focus on submitting alphas with Sharpe ratios > 1.4, low turnover (<25%), and diverse data fields (e.g., price, fundamentals, news) to reduce correlation. Use neutralization (e.g., subindustry) and operators like rank or zscore for robustness. Regularly backtest and prune correlated alphas, leveraging resources like the “101 Formulaic Alphas” paper for inspiration. Monitor correlation reports to ensure uniqueness, enhancing your CSAP over time.

---

### 评论 #4 (作者: JN96079, 时间: 10个月前)

Hey  [TP85668](/hc/en-us/profiles/14806393292439-TP85668) , you mean those tagged alpha signals count for CSAP? Meaning if I choose the best, I will have a great CSAP, and if I tag all my signals in my entire alpha pool, I will have a similar CSAP?

I would like to know this situation so that I can also try to increase the value of my CSAP, as I am having the same problem. In fact, I have a negative CSAP value, and it isn't very pleasant.

I could really use some insights,  [TP85668](/hc/en-us/profiles/14806393292439-TP85668) , kindly and any other member who would like to mention some particulars.

Thanks, all!

---

### 评论 #5 (作者: ML46209, 时间: 10个月前)

CSAP only reflects the  **alphas you’ve actively selected** , so it can be negative even if CAP is high. To improve CSAP,  **prune underperforming selections** , ensure strong  **OS stability** , and keep correlations low so your chosen alphas complement each other.

---

### 评论 #6 (作者: NS62681, 时间: 10个月前)

CAP tracks the performance of your entire alpha library, while CSAP only looks at the ones you’ve actively selected. If your chosen alphas underperform, CSAP can go negative even when CAP is strong. To improve, focus on pruning weaker signals, checking OS stability, and managing correlation so your selected set is both strong and complementary.

---

