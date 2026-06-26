# Event Windows + Continuous Factors — A Winning Blend

- **链接**: [Commented] Event Windows  Continuous Factors  A Winning Blend.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 36

## 帖子正文

Event-driven signals like earnings, dividends, or news shocks can deliver  **huge but spiky Sharpe** . But on their own, they lack turnover and continuity. My solution was to combine them with continuous baselines:

- Event alpha:  `trade_when(earnings_event, rank(revision), NaN)`
- Continuous alpha:  `ts_rank(price/ts_sma(price,20),60)`
- Final: weighted blend (0.6 × event + 0.4 × continuous)

This hybrid gave stable performance — sharp returns around events, plus smoother exposure in between.

👉 Question: Do you integrate event alphas into continuous portfolios, or let them stand alone?

---

## 讨论与评论 (2)

### 评论 #1 (作者: HD25387, 时间: 8个月前)

Blending event-driven and continuous signals is a smart approach. Event alphas often have precision but low turnover, while continuous factors smooth exposure and improve scalability. I usually integrate them rather than running standalone, since the hybrid tends to balance sharp event returns with consistent background performance.

---

### 评论 #2 (作者: AG14039, 时间: 6个月前)

Combining event-driven and continuous signals is a really effective strategy, since event-based alphas deliver sharp, targeted returns but typically operate with low turnover, while continuous factors provide smoother exposure and better scalability. Instead of running them separately, I usually merge the two because the hybrid structure captures the precision of event signals while maintaining steady baseline performance.

---

