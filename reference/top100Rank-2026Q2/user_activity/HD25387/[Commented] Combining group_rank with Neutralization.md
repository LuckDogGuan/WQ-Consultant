# Combining group_rank with Neutralization

- **链接**: [Commented] Combining group_rank with Neutralization.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 35

## 帖子正文

`group_rank(x, group)`  normalizes signals within groups. When combined with  `neutralize` , it can both standardize within peer sets and strip global biases.
Example:  `neutralize(group_rank(roic, industry), mkt_cap)`  ensures ROIC is peer-relative and free of size bias. This layered approach often improves robustness in OS.
👉 Question: Do you apply group ranks first then neutralization, or the reverse?

---

## 讨论与评论 (2)

### 评论 #1 (作者: HD25387, 时间: 8个月前)

I usually apply group ranking first, then neutralization. Grouping ensures the signal is meaningful within its peer set, while the subsequent neutralization removes broader biases like size or liquidity. Reversing the order can work, but tends to blur the peer-relative structure of the signal.

---

### 评论 #2 (作者: AG14039, 时间: 6个月前)

I typically rank signals within groups first and then apply neutralization. The grouping step makes sure the signal has relevance within its peer cohort, and the neutralization that follows cleans out broader influences like size or liquidity. Doing it the other way around can still function, but it often weakens the peer-relative structure that the grouping is meant to capture.

---

