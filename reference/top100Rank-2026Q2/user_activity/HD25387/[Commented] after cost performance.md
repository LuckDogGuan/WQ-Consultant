# after cost performance

- **链接**: [Commented] after cost performance.md
- **作者**: JK98819
- **发布时间/热度**: 1年前, 得票: 14

## 帖子正文

how to improve after-cost performance ??

---

## 讨论与评论 (6)

### 评论 #1 (作者: MG13458, 时间: 1年前)

To improve  **after-cost performance**  of your alphas , you should focus on strategies that reduce  **turnover**  and  **slippage** , while maintaining or enhancing  **alpha signal strength** . Here are actionable approaches:

### 1.  **Reduce Turnover**

High turnover leads to higher transaction costs. Use these operators:

- **`hump(x, hump=...)`** : Smooths small changes in alpha values, avoiding unnecessary trades.
- **`hump_decay(x, p=..., relative=True)`** : Ignores minor movements unless they exceed a threshold.
- **`trade_when(triggerTradeExp, alphaExp, triggerExitExp)`** : Triggers trades conditionally and holds positions otherwise.

**Tip** : Use  `trade_when`  to filter trades based on liquidity or volatility criteria, e.g.:

`trade_when(volume > adv20, alpha, abs(returns) > 0.1)
`

### 2.  **Control Alpha Magnitudes**

Large position sizes can cause high impact cost:

- **`scale(x, scale=...)`** : Controls portfolio exposure.
- **`truncate(x, maxPercent=...)`** : Caps position sizes.
- **`normalize(x, useStd=true, limit=...)`** : Ensures bounded outputs, limiting overexposure.

### 3.  **Neutralize Unwanted Exposures**

Prevent cost due to market or sector exposure:

- **`group_neutralize(x, group)`** : Removes sector/industry bias.
- **`regression_neut(Y, X)`** : Neutralize to market beta or other risk factors.

### 4.  **Use More Stable Predictors**

- Favor time-series smoothed metrics like  `ts_mean` ,  `ts_rank` ,  `ts_decay_exp_window` .
- Avoid overly reactive variables unless justified.

---

### 评论 #2 (作者: NS94943, 时间: 1年前)

Hi,

The best tool to check whether your alpha is likely to perform well after cost is the max trade setting. If the alpha's performance does not degrade too much when using this setting, it is very likely that it will have good after cost performance too, if not overfitted.

---

### 评论 #3 (作者: HD25387, 时间: 1年前)

Great question! To improve after-cost performance, start by  **managing turnover carefully**  — avoid sharp spikes by using operators like  `ts_target_tvr_delta_limit`  or  `tradewhen` . Also, focus on  **signal robustness across liquid stocks** , and try to maintain  **balanced exposure**  across capitalization sizes. Use the Max Trade setting (especially in ASI) to filter out unrealistic trades in low-liquidity names. Finally, monitor sub-universe Sharpe and avoid overly complex alphas that perform well only in narrow slices of the market. Small adjustments can make a big difference post-cost.

---

### 评论 #4 (作者: SM36732, 时间: 1年前)

```
always keep max trade on, it will help
```

---

### 评论 #5 (作者: AK98027, 时间: 1年前)

Improving after-cost performance often comes down to managing turnover and transaction costs effectively. Try designing smoother signals with lower trading frequency and focus on robustness rather than chasing sharp intraday moves. Also, using decay operators and incorporating TVR (Turnover-to-Volatility Ratio) can help reduce unnecessary churn. Optimizing for stability can often lead to better real-world results.

---

### 评论 #6 (作者: LM22798, 时间: 1年前)

Great point! The max trade setting is indeed a powerful tool for evaluating an alpha’s robustness after accounting for costs. If the performance remains relatively stable under this constraint, it’s a strong indicator that the alpha is not overly sensitive or overfitted. This kind of stress test adds confidence that the strategy can hold up in real trading environments.

---

