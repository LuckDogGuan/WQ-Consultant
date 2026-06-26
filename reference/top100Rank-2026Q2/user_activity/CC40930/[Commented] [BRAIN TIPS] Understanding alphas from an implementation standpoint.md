# [BRAIN TIPS] Understanding alphas from an implementation standpoint

- **链接**: [Commented] [BRAIN TIPS] Understanding alphas from an implementation standpoint.md
- **作者**: KA64574
- **发布时间/热度**: 3年前, 得票: 9

## 帖子正文

As you know, alpha values are evaluated each day and positions are rebalanced daily. This daily rebalancing of positions doesn’t involve closing and taking new positions each day; instead we take only incremental positions to decrease transaction costs. For instance, if on day 1, your alpha went long $2,000 of AAPL and the next day it is long $3,000 of AAPL, we don’t close out the first day’s position and then go long another $3,000 of AAPL. Instead we add $1,000 of AAPL to the next day’s position. You can assume the transactions are done using the volume-weighted average price (VWAP) of AAPL shares traded that day.

---

## 讨论与评论 (6)

### 评论 #1 (作者: TT55495, 时间: 1年前)

I would like to ask if the example you gave is about the idea of ​​momentum? When the price is going up, should we continue to buy in that trend?

---

### 评论 #2 (作者: LN78195, 时间: 1年前)

Regarding the example, it does seem to align with momentum principles—continuing to increase positions as the price trend strengthens. Could you clarify if this strategy also adapts to scenarios where contrarian or mean-reversion signals are present?

---

### 评论 #3 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #4 (作者: deleted user, 时间: 1年前)

Now I understand the context better. You're describing  **daily rebalancing**  with  **incremental adjustments**  to positions based on the alpha signal, rather than fully closing and reopening positions each day. This approach reduces  **transaction costs**  and avoids unnecessary turnover in the portfolio.

---

### 评论 #5 (作者: QG16026, 时间: 1年前)

Thank you for the clarification! The incremental adjustment approach makes a lot of sense for reducing transaction costs while maintaining the alpha signal. Really insightful.

---

### 评论 #6 (作者: CC40930, 时间: 1年前)

The transactions are typically executed at the  **volume-weighted average price (VWAP)**  of the stock for that day, ensuring the trade reflects the average price considering the volume of shares traded.

This strategy reduces trading frequency and slippage, helping to optimize costs while maintaining alignment with the alpha's recommendations.

---

