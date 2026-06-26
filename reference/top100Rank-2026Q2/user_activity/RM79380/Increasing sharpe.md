# Increasing sharpe

- **链接**: Increasing sharpe.md
- **作者**: RM79380
- **发布时间/热度**: 4个月前, 得票: 10

## 帖子正文

Is there a way of increasing sharpe without overfitting?

---

## 讨论与评论 (3)

### 评论 #1 (作者: ME83843, 时间: 3个月前)

Yes — but the key is  **improving signal quality, not “tuning” it** .

Here are practical ways to increase Sharpe  **without overfitting** :

**1. Reduce noise, don’t add complexity**

- Use light smoothing (e.g., reasonable lookbacks)
- Remove redundant operators
- Cleaner signal → better risk-adjusted returns

**2. Improve signal intuition**

- Make sure the alpha has a clear economic reason
- Strong intuition usually translates to more stable Sharpe

**3. Control turnover**

- High turnover often inflates noise and costs
- Use decay or slightly longer horizons to stabilize returns

**4. Combine orthogonal signals**

- Blend low-correlated alphas
- Diversification improves Sharpe more reliably than tweaking one signal

**5. Neutralize properly**

- Remove unintended exposures (sector, market)
- Helps isolate true alpha → cleaner performance

**6. Focus on consistency, not peaks**

- Stable IS across periods > one strong backtest
- Consistency naturally improves Sharpe over time

---

### 评论 #2 (作者: FM47631, 时间: 3个月前)

Sharpe improvements that survive OOS usually come from reducing noise, not adding signal. Think orthogonality, turnover control, and better universe conditioning rather than more complex expressions.

---

### 评论 #3 (作者: GK10904, 时间: 3个月前)

YES

---

