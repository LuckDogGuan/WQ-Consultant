# question about universe

- **链接**: [Commented] question about universe.md
- **作者**: NN29533
- **发布时间/热度**: 8个月前, 得票: 33

## 帖子正文

I am backtesting a strategy on the Top 200 companies from 2020 to 2023. However, some companies would have exited and new ones entered the Top 200 in 2024.
My key question is: Does the backtesting system dynamically update the constituents along the testing timeline, using the actual, contemporaneous Top 200 for that specific period (daily, quarterly, or annually)? Or does it rigidly stick to a single, static list (e.g., the 2020 list) throughout the entire backtest?
A reliable system must use the historical list to avoid survivorship bias right?

---

## 讨论与评论 (6)

### 评论 #1 (作者: SS35873, 时间: 8个月前)

A reliable backtesting system should dynamically update the Top 200 constituents based on their actual historical rankings at each point in time—daily, monthly, or annually—rather than using a single static list from one year. This ensures that the backtest reflects real-world investability and avoids  **survivorship bias** , which occurs when only companies that survived until the end of the test period are included, artificially inflating performance. In short, accurate backtests must use contemporaneous universes that evolve as they did in reality.

---

### 评论 #2 (作者: AG14039, 时间: 6个月前)

A reliable backtesting system should update the Top 200 constituents dynamically based on their actual historical rankings at each point in time—whether daily, monthly, or annually—instead of relying on one fixed list from a single year. This approach reflects true investability and avoids survivorship bias, which arises when only companies that survived until the end of the period are included, artificially boosting results. In essence, accurate backtests require contemporaneous universes that evolve exactly as they did in real markets.

---

### 评论 #3 (作者: KG79468, 时间: 6个月前)

The constituents are not static. The system recomputes the universe daily/periodically based on the real historical Top 200 at each timestamp, ensuring accuracy.

---

### 评论 #4 (作者: SP39437, 时间: 6个月前)

A robust backtesting framework should always rely on a dynamic universe that updates according to historical rankings at each point in time, rather than using a single static list derived from one reference year. By reconstituting the Top 200 constituents daily, monthly, or annually based on what was actually tradable at that moment, the backtest more accurately reflects real-world investability. This approach is essential for avoiding survivorship bias, which occurs when only stocks that remain in the universe until the end of the sample are included, leading to inflated and misleading performance results. Using contemporaneous universes ensures that strategy behavior is evaluated under the same conditions traders would have faced in reality, including entries, exits, and liquidity changes. Ultimately, realistic universe construction is just as important as signal design when assessing true strategy robustness. How do you decide the optimal rebalancing frequency for updating a dynamic universe in backtests?

---

### 评论 #5 (作者: TP19085, 时间: 6个月前)

A sound backtesting setup should be built on a universe that evolves through time, reflecting historical rankings at each point rather than relying on a fixed list taken from a single year. Rebuilding the Top 200 constituents on a daily, monthly, or yearly basis—based on what was actually tradable then—creates a far more realistic simulation of real market conditions. This is critical for eliminating survivorship bias, where excluding stocks that later drop out of the universe can significantly overstate performance. Using contemporaneous universes ensures the strategy is tested under conditions traders truly faced, including changes in membership, liquidity, and accessibility. In this sense, universe construction plays a role just as important as alpha formulation itself. The credibility of any backtest depends on whether it mirrors real-world constraints rather than idealized assumptions.

---

### 评论 #6 (作者: JN96079, 时间: 5个月前)

A robust backtesting framework should rebuild the Top 200 universe at each point in time based on the rankings that actually existed then—whether updated daily, monthly, or annually—instead of relying on a fixed list from a single year. Doing so better reflects real-world investability and prevents survivorship bias, which arises when only companies that remain at the end of the sample are included, overstating historical performance. In short, credible backtests require time-appropriate universes that change in step with market reality.

^^JN

---

