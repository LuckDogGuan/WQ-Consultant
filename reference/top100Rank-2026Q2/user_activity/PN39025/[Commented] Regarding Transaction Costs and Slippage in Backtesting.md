# Regarding Transaction Costs and Slippage in Backtesting

- **链接**: [Commented] Regarding Transaction Costs and Slippage in Backtesting.md
- **作者**: DT49505
- **发布时间/热度**: 11个月前, 得票: 51

## 帖子正文

Hi everyone,

When the platform calculates the backtest PnL curve for an alpha, does it take into account transaction costs and slippage?

If anyone has insights or experience with this, I’d greatly appreciate it if you could share. Thank you! Have a good day

---

## 讨论与评论 (9)

### 评论 #1 (作者: PN39025, 时间: 11个月前)

Hello, currently the pnl line has an IC index to calculate pnl through transaction costs. Please pay attention to the IC index to be more certain about after cost in OS.

---

### 评论 #2 (作者: HD25387, 时间: 11个月前)

Yes, most backtesting platforms, including this one, typically incorporate transaction costs and slippage when calculating the backtest PnL curve. Transaction costs account for the cost of executing trades (like commissions or fees), and slippage reflects the difference between the expected price and the actual execution price, which can occur due to market conditions or liquidity.

To ensure more realistic backtesting, make sure to include transaction cost parameters in the platform’s settings. This can give you a better understanding of how your strategy would perform in live conditions.

Looking forward to hearing others’ experiences!

---

### 评论 #3 (作者: JN96079, 时间: 11个月前)

True, it  *does automatically include realistic transaction costs or slippage* . Furthermore, its simulation focuses on a daily‑rebalanced portfolio with normalisations, neutralisations, and other operations.

---

### 评论 #4 (作者: AM71073, 时间: 10个月前)

Great question!

✅  **Yes** , the BRAIN platform  **does incorporate transaction costs and slippage**  when generating the  **After-Cost PnL curve**  during backtesting.

Here’s how it works:

🔹  **Two PnL Curves:**

- **Pre-Cost PnL** : Assumes perfect execution, no costs.
- **After-Cost PnL** : Adjusts for  **transaction costs** ,  **slippage** , and  **capacity constraints**  — this is the more realistic performance metric.

🔹  **Transaction Costs Include:**

- **Commission**
- **Bid-ask spread**
- **Market impact (especially in illiquid or high-turnover alphas)**

🔹  **Why It Matters:**

- A high  **Pre-Cost Sharpe**  with poor  **After-Cost Sharpe**  often signals  **excessive turnover**  or reliance on illiquid trades.
- Always monitor both  **Sharpe**  and  **Fitness**  (adjusted Sharpe) to assess true performance.

🔹  **Tips to Improve After-Cost Performance:**

- Reduce turnover (aim <0.2)
- Use smoothers like  `ts_mean` ,  `ts_decay_exp_window` ,  `ts_backfill`
- Ensure good  **coverage in liquid stocks**
- Set  **Max Trade**  ON (especially for ASI region alphas)

---

### 评论 #5 (作者: AK98027, 时间: 10个月前)

Great question! Yes, the backtest PnL curves do include both transaction costs and slippage in the calculations. This gives you a more realistic view of actual performance rather than just theoretical gross returns. It's one of the reasons why low-turnover alphas often perform better in live trading - the cost drag is already baked into what you're seeing in backtests.

---

### 评论 #6 (作者: ML46209, 时间: 10个月前)

Good to know! Including realistic transaction costs and slippage is essential for backtests to reflect live performance accurately

---

### 评论 #7 (作者: NT84064, 时间: 10个月前)

In most quant research environments, including those designed for alpha evaluation, the raw backtest PnL curve typically does  **not**  automatically incorporate explicit transaction costs or slippage unless the platform specifies a built-in execution cost model. This means that while the historical price series and simulated trades can show “ideal” returns, the actual implementable performance could be lower once real-world frictions are applied. For more realistic results, it’s advisable to manually adjust for costs—either by applying fixed basis point deductions per trade or modeling slippage as a function of trade size relative to average daily volume (ADV) and bid–ask spread. Some practitioners use functions like turnover penalties in fitness metrics to indirectly reflect costs. Ultimately, if the platform doesn’t natively apply cost adjustments, you should simulate them in your own workflow to better align backtest results with expected live performance.

---

### 评论 #8 (作者: NS62681, 时间: 10个月前)

Transaction costs represent the expenses of executing trades, such as commissions or fees, while slippage captures the gap between the expected price and the actual execution price, which can arise from market conditions or liquidity constraints.

---

### 评论 #9 (作者: LB76673, 时间: 10个月前)

In WQB simulations, the  **PnL curve you see is gross of trading costs**  — it does  **not**  automatically include transaction costs or slippage. The platform assumes frictionless trading when generating IS/OS curves so you can focus on the raw predictive power of the signal.

That said, turnover is tracked because  **higher turnover implies higher implicit costs** . When evaluating alphas, metrics like  **turnover, holding period, and stability**  are used as proxies for cost impact. In practice, WorldQuant applies cost models at later portfolio-construction stages (beyond the alpha simulation itself).

---

