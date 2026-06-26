# Trade_when vs Daily rebalancing

- **链接**: [Commented] Trade_when vs Daily rebalancing.md
- **作者**: II20648
- **发布时间/热度**: 2个月前, 得票: 2

## 帖子正文

When does trade_when actually outperform a standard daily alpha? I've been using  `trade_when(volume > adv20, positive_days, -1)`  for a momentum strategy and the Sharpe improves, but I'm not sure if that's because of the entry condition or just because I'm holding longer. How do you think about when to use trade_when vs. just adjusting decay

---

## 讨论与评论 (3)

### 评论 #1 (作者: CM46415, 时间: 2个月前)

Great question—this is really about  *execution structure vs signal smoothing* .

`trade_when`  usually outperforms daily rebalancing when your signal is only valid under certain market conditions (like liquidity, volume, volatility regimes). In your case, filtering with  `volume > adv20`  likely improves Sharpe because you’re avoiding noisy or illiquid periods—not just because you’re holding longer.

Decay, on the other hand, smooths the signal continuously. It reduces noise but still trades every day, so it doesn’t change  *when*  you participate—only  *how strongly*  you react.

Rule of thumb:

- Use  **decay**  when the signal is always valid but noisy.
- Use  **trade_when**  when the signal is conditionally valid or you want to avoid bad regimes (liquidity/volatility filters).

So your improvement likely comes from better  *regime filtering* , not just holding period.

---

### 评论 #2 (作者: FZ60707, 时间: 2个月前)

`trade_when`  tends to outperform when your alpha is state‑dependent—e.g., momentum only works during high volume. The condition filters out low‑signal periods, while the longer hold reduces turnover, both boosting Sharpe. Adjusting decay just changes how fast a position fades;  `trade_when`  controls  *if*  you trade at all. So use  `trade_when`  when the signal’s strength depends on a regime, and stick with decay when the signal itself is continuous but mean‑reverting.

---

### 评论 #3 (作者: Eddy Momanyi Nyambane(EM17335), 时间: 2个月前)

Very useful

---

