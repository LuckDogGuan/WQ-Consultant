# Overfitting check

- **链接**: Overfitting check.md
- **作者**: RM79380
- **发布时间/热度**: 4个月前, 得票: 17

## 帖子正文

What are some of the ways one can use to check if an alpha is overfitted?

---

## 讨论与评论 (5)

### 评论 #1 (作者: HO41126, 时间: 2个月前)

Generally if it has those weirdly big sharpe

---

### 评论 #2 (作者: JM47610, 时间: 2个月前)

This is something everyone struggles with during Alpha creation.

A few practical ways that I check are:

- Train vs Test consistency: If performance drops a lot from train to test, that’s a red flag.
- IS vs OS behavior: Big gap = likely overfitting. Solid alphas degrade slightly, not collapse.
- Parameter sensitivity: If small changes (lookbacks, weights) break the alpha, it’s fragile.
- Simplicity check: If the logic is too complex to explain clearly, it’s probably curve-fit.
- Correlation with similar ideas: If it only works when combined with very similar alphas, it’s not robust.
- Regime stability: Check if it works across different market conditions, not just one period.

something you should note is that, If it only works  *perfectly*  in-sample, it probably won’t survive in reality.

---

### 评论 #3 (作者: HC86622, 时间: 2个月前)

Check investibility and risk performance

---

### 评论 #4 (作者: CM46415, 时间: 2个月前)

Overfitting shows up when an alpha performs well in-sample but fails out-of-sample. Key checks include Train/Test/OS consistency, parameter sensitivity, stable turnover, weak self-correlation, and robust performance across time periods and small input changes.

---

### 评论 #5 (作者: MK55614, 时间: 1个月前)

If performance collapses outside the training period, that’s a warning sign.

A robust alpha should behave consistently across windows, Simple alphas are usually more robust.

Check the economic intuition of the alpha, ask why should this alpha work in real markets.

Test different universes-if ut survives different universe it means it is a robust signal.

---

