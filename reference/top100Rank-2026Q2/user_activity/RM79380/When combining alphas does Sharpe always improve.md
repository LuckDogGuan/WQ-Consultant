# When combining alphas does Sharpe always improve?

- **链接**: When combining alphas does Sharpe always improve.md
- **作者**: RM79380
- **发布时间/热度**: 2个月前, 得票: 32

## 帖子正文

If two alphas both have a Sharpe ratio of 2, will combining them produce a portfolio of Sharpe ratio above 2?

---

## 讨论与评论 (6)

### 评论 #1 (作者: FM47631, 时间: 1个月前)

Mathematically, Sharpe only improves if the alphas have low correlation, which is why Brain strictly limits correlation against the production pool. However, even if the raw Sharpe increases, you have to look at the holistic impact: does combining them spike your Turnover or dilute your Margin, ultimately dropping your overall Fitness score? Furthermore, arbitrarily jamming alphas together just to force a higher In-Sample (IS) Sharpe is a classic recipe for overfitting, meaning your Out-of-Sample (OS) performance will almost certainly degrade.

---

### 评论 #2 (作者: JM47610, 时间: 1个月前)

Not always.Combining two Sharpe 2 alphas only improves portfolio Sharpe if the signals arenot highly correlated.

---

### 评论 #3 (作者: KU30147, 时间: 1个月前)

Not neceserily.

---

### 评论 #4 (作者: CB60351, 时间: 21天前)

Not always like that, but sometimes it does.

---

### 评论 #5 (作者: DY83351, 时间: 20天前)

Not necessarily,it depends on the correlation between the two alphas.

---

### 评论 #6 (作者: SL11054, 时间: 20天前)

If the two alphas are perfectly correlated, you are essentially trading the exact same signal twice. You double your returns, but you also double your risk. The portfolio Sharpe ratio remains exactly 2.

---

