# Turnover Clustering — The Hidden Risk

- **链接**: [Commented] Turnover Clustering  The Hidden Risk.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 34

## 帖子正文

Even when average turnover looks fine (~15–20%), clustering matters. I’ve seen alphas where  **turnover is concentrated in a few bursts** , causing large rebalances that increase implementation risk.
Using  `ts_decay`  helped spread trades more evenly, but not perfectly. Another trick is to  **cap per-stock contributions**  ( `truncate` ) so one rebalance doesn’t dominate.

I’ve started tracking not just average turnover, but also  **turnover variance over time**  as a robustness metric.

👉 Question: Do you evaluate turnover distribution (clustering), or only track overall averages when designing alphas?

---

## 讨论与评论 (2)

### 评论 #1 (作者: HD25387, 时间: 8个月前)

That’s a great point. Average turnover alone can be misleading if most of it comes in bursts. I’ve found it useful to track turnover variance and use smoothing techniques to avoid concentrated rebalances, since implementation risk often hides in those clusters.

---

### 评论 #2 (作者: ZK79798, 时间: 8个月前)

Good point—average TVR can hide clustering risks. I also monitor turnover variance and distribution across time, since smoother trade flow often improves OS stability and reduces hidden implementation costs.

---

