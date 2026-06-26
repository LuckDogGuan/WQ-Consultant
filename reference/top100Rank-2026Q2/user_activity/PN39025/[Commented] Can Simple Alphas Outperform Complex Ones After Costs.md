# Can Simple Alphas Outperform Complex Ones After Costs?

- **链接**: [Commented] Can Simple Alphas Outperform Complex Ones After Costs.md
- **作者**: CM46415
- **发布时间/热度**: 2个月前, 得票: 13

## 帖子正文

In the pursuit of higher performance, it’s common to build increasingly complex alphas by stacking multiple transformations, filters, and signals. While this often improves in-sample metrics, I’ve noticed that simpler alphas sometimes exhibit better robustness once transaction costs, slippage, and turnover are taken into account.

Complex alphas tend to introduce higher turnover and sensitivity to noise, which can erode returns after costs. On the other hand, simpler structures may capture more stable effects, even if their raw performance appears lower.

I’m interested in understanding this trade-off more clearly:

- Have you observed simpler alphas outperforming complex ones after accounting for costs?
- How do you evaluate whether added complexity genuinely improves net performance?
- Are there specific metrics (e.g., turnover-adjusted Sharpe) you rely on when comparing alphas?
- At what point does additional complexity stop adding value?

Looking forward to hearing how others balance simplicity and performance in alpha design.

---

## 讨论与评论 (2)

### 评论 #1 (作者: CM46415, 时间: 2个月前)

Simple alphas often outperform after costs due to lower turnover and stronger robustness. Complexity helps only when it adds stable predictive power, not when it merely fits in-sample noise.

---

### 评论 #2 (作者: PN39025, 时间: 2个月前)

I agree, but if it's too simple, many people will figure it out, leading to a high correlation. So I usually opt for a more complex structure instead of a simple one.

---

