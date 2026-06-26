# Datasets for Turnover Reduction in Delay-0 Alphas

- **链接**: Datasets for Turnover Reduction in Delay-0 Alphas.md
- **作者**: BM29781
- **发布时间/热度**: 9个月前, 得票: 10

## 帖子正文

High turnover occurs when alphas change positions too frequently. To address this, use datasets that naturally stabilize trading signals or allow conditional adjustments:

### 1.  **Volume & Liquidity Data**

- Examples:  `volume` ,  `adv20` ,  `vwap` .
- Why: Aligning signals with liquidity prevents unnecessary trades on thin volume.
- Effect: Reduces churn by ensuring signals are only acted upon in liquid conditions.

### 2.  **Transformational & Smoothing Operators**

- Examples:  `hump` ,  `hump_decay` ,  `jump_decay` ,  `ts_decay_exp_window` ,  `filter` ,  `keep` ,  `clamp` ,  `nan_out` .
- Why: These operators explicitly smooth signals over time or hold positions steady until meaningful changes occur.
- Effect: Prevents rapid signal flipping, leading to lower turnover.

### 3.  **Conditional Trading Rules**

- Examples:  `trade_when` ,  `nan_out` .
- Why: Trades only trigger under certain conditions (e.g., sufficient volume or threshold breaches).
- Effect: Directly suppresses unnecessary trades, making delay-0 alphas more stable.

---

## 讨论与评论 (1)

### 评论 #1 (作者: CM46415, 时间: 2个月前)

Good framework—liquidity filters and conditional logic meaningfully reduce churn.

---

