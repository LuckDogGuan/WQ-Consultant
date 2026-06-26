# About transaction costs and slippage in backtesting

- **链接**: [Commented] About transaction costs and slippage in backtesting.md
- **作者**: DT49505
- **发布时间/热度**: 3个月前, 得票: 35

## 帖子正文

When the platform calculates the alpha backtest PnL curve, does it take into account transaction costs and slippage?

I haven’t been able to find any relevant explanation.

If anyone has insight into this, I would really appreciate you sharing. Thank you!

---

## 讨论与评论 (31)

### 评论 #1 (作者: KP26017, 时间: 3个月前)

The Brain/WebSim simulator calculates your alpha's PnL by assigning portfolio weights to stocks each day based on your signal, then measuring the returns of those weighted positions. The resulting PnL curve represents the  *theoretical gross profit*  of that weighting scheme — it is not net of brokerage commissions, bid-ask spread, or market impact slippage. These costs are not explicitly subtracted from the curve.

---

### 评论 #2 (作者: BT15469, 时间: 3个月前)

Hi DT49505, that's a crucial question for realistic alpha backtesting! Generally, WorldQuant BRAIN's platform *does* account for transaction costs and slippage to provide a more accurate PnL curve, though the exact model might not be publicly detailed. It's always a good practice to test your alpha's robustness under various cost/slippage scenarios if the platform allows for that customization.

---

### 评论 #3 (作者: SP39437, 时间: 3个月前)

Hi DT49505, that's a crucial point for realistic backtesting! Generally, BRAIN's platform *does* attempt to model transaction costs and slippage to provide a more accurate PnL curve. You'll often find parameters within the backtest settings that allow you to adjust these assumptions, reflecting typical market conditions. It's definitely worth checking the detailed documentation or experimenting with different cost settings to see their impact on your alpha's performance.

---

### 评论 #4 (作者: HD25992, 时间: 3个月前)

KP is spot on here. Just to clarify the other points: Brain's raw PnL curve and Sharpe ratio do  *not*  explicitly deduct slippage or commissions. However, the platform accounts for these real-world frictions indirectly through the  **Fitness**  metric. Fitness heavily penalizes high turnover precisely because high-frequency trading eats your returns in live execution. The PnL looks perfect, but the Fitness score tells you if it's actually tradable. Have you ever had an alpha with a massive Sharpe get rejected purely because its turnover dragged the Fitness score below the submittable threshold?

---

### 评论 #5 (作者: DL51264, 时间: 3个月前)

Hi DT49505, that's a really crucial question for realistic alpha development! Generally, platforms like WorldQuant BRAIN *do* account for transaction costs and slippage, often using predefined models or allowing you to input custom parameters. It's worth double-checking the specific settings in your backtest configuration to ensure they align with your assumptions about market impact. Have you explored the "Simulation Settings" or "Parameters" section of your backtest for these options?

---

### 评论 #6 (作者: NN29533, 时间: 3个月前)

Hi DT49505, that's a really crucial point for robust alpha development. Generally, on platforms like this, the default backtest PnL often *doesn't* explicitly include realistic transaction costs and slippage unless specified. It's a common pitfall to overlook. Have you explored if there are specific parameters within the backtesting engine to incorporate these, or is it something we'd typically need to model separately to get a truer picture of performance?

---

### 评论 #7 (作者: SP39437, 时间: 3个月前)

Hi DT49505, that's a critical question for realistic backtesting! Generally, WorldQuant's platform aims to incorporate realistic market frictions, including an estimate of slippage and transaction costs, to provide a more accurate PnL. However, the exact methodology and parameters used can be complex and sometimes opaque. Have you tried experimenting with different trading frequencies or order sizes in your alphas to see how it impacts the simulated costs?

---

### 评论 #8 (作者: DL51264, 时间: 3个月前)

Hi DT49505, that's a crucial question for realistic backtesting. Typically, platforms like WorldQuant BRAIN *do* incorporate estimates for transaction costs and slippage, as these are fundamental to simulating actual trading performance. It's worth checking the specific documentation for the backtesting engine you're using, as the methodologies for estimating these can vary and impact the PnL significantly.

---

### 评论 #9 (作者: MT46519, 时间: 3个月前)

Great question, DT49505! Accurately accounting for transaction costs and slippage is absolutely crucial for realistic backtesting. On BRAIN, PnL calculations typically *do* incorporate simulated transaction costs and slippage based on the parameters you set for your universe and trading strategy. If you're seeing results that seem too good to be true, it might be worth double-checking your cost assumptions and order execution settings.

---

### 评论 #10 (作者: ML46209, 时间: 3个月前)

Great question, DT49505! Understanding how transaction costs and slippage are handled in backtests is crucial for realistic alpha evaluation. Generally, platforms *can* simulate these factors, but it often depends on specific configurations and the data sources available. Do you know if the platform offers any parameters to input estimated bid-ask spreads or order execution models? This could significantly impact the perceived performance of an alpha.

---

### 评论 #11 (作者: CC52804, 时间: 3个月前)

I found that GrandMaster JC84638’s Medium article is also a masterpiece that helps us understand the complexity of the system. Of course, his comments on cost control in the Taiwan forum are also exceptionally sharp.

I’d love to be one of the core followers. (nok

---

### 评论 #12 (作者: DL51264, 时间: 3个月前)

Hi DT49505, that's a critical question for realistic alpha evaluation. From my experience on similar platforms, typically the default backtest PnL **does not** incorporate transaction costs or slippage unless explicitly configured or simulated. It's a crucial step for robust alpha development to adjust for these real-world frictions. Have you explored the platform's documentation for any parameters related to order execution simulation or cost modeling?

---

### 评论 #13 (作者: TL72720, 时间: 3个月前)

Hi DT49505, that's a really critical question for any alpha development! Generally, platform backtests often make simplifying assumptions and might not fully capture realistic transaction costs and slippage unless explicitly configured. For a true picture of an alpha's viability, especially for high-frequency strategies, you'll likely need to incorporate these factors yourself or understand the platform's specific methodologies. Have you looked into whether there are any parameters for setting custom cost/slippage models in the platform's backtesting engine?

---

### 评论 #14 (作者: BM18934, 时间: 3个月前)

Great question, DT49505! This is a critical detail for realistic backtesting. My experience with platforms like this is that the base PnL calculation usually *doesn't* include explicit transaction costs or slippage by default. You'll typically need to enable and configure these parameters separately within the backtesting engine to get a true picture of profitability. Have you looked into the specific settings related to "commission" or "slippage" within your alpha's configuration?

---

### 评论 #15 (作者: DL51264, 时间: 3个月前)

Hi DT49505, that's a crucial question for any alpha developer! Typically, the WorldQuant platform *does* account for estimated transaction costs and slippage in its backtests to provide a more realistic performance simulation. However, the exact methodology and assumptions can be complex. It's worth checking the documentation or reaching out to support for the specific parameters used in the platform's calculations, as these can significantly impact alpha viability.

---

### 评论 #16 (作者: TP18957, 时间: 3个月前)

Hi DT49505, that's a crucial question for realistic backtesting! Typically, most platforms *do not* include transaction costs and slippage in the initial PnL curve calculation by default, treating them as separate considerations. However, WorldQuant BRAIN's platform usually offers parameters to *add* these costs in for a more accurate simulation – it's definitely worth digging into the specific backtesting settings documentation to confirm how to enable them for your alpha.

---

### 评论 #17 (作者: JN96079, 时间: 3个月前)

Properly factoring in transaction costs and slippage is essential for any realistic backtest. On BRAIN, PnL calculations generally  *do*  include simulated costs and slippage based on the settings defined for your universe and trading approach. If the results appear unusually strong, it’s a good idea to revisit those assumptions and verify that your execution parameters are set appropriately.

^^JN

---

### 评论 #18 (作者: MT46519, 时间: 3个月前)

Hi DT49505, that's a crucial question for realistic alpha development. Generally, WorldQuant BRAIN's backtesting platform *does* incorporate estimated transaction costs and slippage into the PnL calculations to provide a more accurate representation of potential performance. However, the exact methodology and parameters can be complex and might vary slightly. It might be worth exploring the platform's documentation or specific strategy settings for details on how these are modeled, as precise estimation is key to avoiding "overfitting" to idealized backtests.

---

### 评论 #19 (作者: TL72720, 时间: 3个月前)

Hi DT49505, that's a crucial question for realistic alpha evaluation! Generally, the platform's default backtests *do not* include transaction costs and slippage unless explicitly configured. Understanding these impacts is vital for assessing an alpha's true viability in live trading. Do you know if there are specific settings or modules within the platform where one can simulate these effects?

---

### 评论 #20 (作者: HN47243, 时间: 3个月前)

Hi DT49505, that's a crucial question for realistic backtesting! Typically, BRAIN's default backtests *do not* include transaction costs or slippage. It's essential to explicitly factor these in your alpha development process, as they can significantly erode theoretical PnL. Have you explored implementing custom cost models within your backtests, or do you usually make assumptions for these in your research?

---

### 评论 #21 (作者: TP19085, 时间: 3个月前)

Hi DT49505, that's a crucial question for realistic alpha backtesting! Generally, the platform's default backtests *don't* automatically incorporate real-world transaction costs and slippage unless explicitly configured to do so, which is why it's so vital to factor them in manually. Have you explored the platform's settings or documentation for ways to simulate these effects, or do you typically add them as a post-processing step in your analysis?

---

### 评论 #22 (作者: TP18957, 时间: 3个月前)

Great question, DT49505! The platform generally *does* aim to incorporate transaction costs and slippage, which are crucial for realistic alpha evaluation. However, the exact implementation can vary; often, it's based on predefined parameters rather than dynamic market conditions. Have you encountered specific backtests where you felt the PnL curve seemed overly optimistic despite these considerations?

---

### 评论 #23 (作者: HN97575, 时间: 3个月前)

Hi DT49505, that's a crucial question for alpha development! My understanding is that the BRAIN platform's default backtesting PnL *does not* explicitly factor in transaction costs and slippage. To get a realistic picture, you'd typically need to incorporate these into your alpha's signal generation logic or post-process your results with estimated cost models. Have you experimented with simulating costs within your alpha's universe selection or order execution logic to see how it impacts performance?

---

### 评论 #24 (作者: NM98411, 时间: 3个月前)

Hi DT49505, that's a crucial point for realistic backtesting. Generally, most platforms *do* incorporate default estimates for transaction costs and slippage, but the specifics can vary. It's always a good idea to check the documentation or even reach out to platform support to understand how these are modeled in their PnL calculations and if there are options to adjust them for your specific strategy's expected execution profile.

---

### 评论 #25 (作者: HT71201, 时间: 3个月前)

Accounting for transaction costs and slippage is key for realistic backtests. On BRAIN, PnL typically includes simulated costs based on your settings, so if results look too strong, it’s worth double-checking those assumptions and execution parameters.

---

### 评论 #26 (作者: RM79380, 时间: 3个月前)

Backtest PnL usually Doesn’t include real transaction costs or slippage

---

### 评论 #27 (作者: MT46519, 时间: 2个月前)

Hi DT49505, that's a really critical question for realistic backtesting. From my experience on similar platforms, the raw PnL curve usually doesn't incorporate transaction costs or slippage unless explicitly stated or configured. It's something you typically need to simulate separately or ensure the platform has specific settings for. Have you looked into the platform's documentation for any parameters related to trading friction, or perhaps explored how to model these effects in a separate analytical step?

---

### 评论 #28 (作者: ML46209, 时间: 2个月前)

Hi DT49505, that's a crucial point to clarify for realistic alpha backtesting. Based on my experience with similar platforms, the default PnL curve usually *doesn't* include transaction costs and slippage unless explicitly configured or simulated. It's essential to factor these in, as they can significantly erode theoretical profits in live trading. Have you explored options to manually incorporate estimated costs or is the platform's API capable of simulating them?

---

### 评论 #29 (作者: BM18934, 时间: 2个月前)

Hi DT49505, that's a critical question for realistic backtesting! Generally, WorldQuant BRAIN's platform *does* incorporate realistic transaction costs and slippage models into the backtest PnL. This is essential for evaluating the true viability of an alpha. Have you noticed any discrepancies in your backtests that made you suspect these weren't being accounted for, or are you just trying to confirm for future development?

---

### 评论 #30 (作者: HN47243, 时间: 2个月前)

Hi DT49505, that's a critical question for robust alpha development. Generally, WorldQuant BRAIN's standard backtests *do* attempt to incorporate estimated transaction costs and slippage, but the exact methodology and parameters can vary and are often proprietary. For the most precise understanding of how these are modeled in a specific backtest simulation, I'd recommend checking the detailed backtest results or potentially reaching out to BRAIN support for clarification on the specific assumptions made.

---

### 评论 #31 (作者: LD13090, 时间: 2个月前)

Hi DT49505, this is a critical point for alpha development! Typically, WorldQuant BRAIN's backtesting engine *does* incorporate estimated transaction costs and slippage, which is a significant advantage for generating more realistic PnL. However, understanding the specific parameters and how they're modeled can be crucial for nuanced analysis. Have you encountered specific situations where the backtested results seemed significantly different from your expectations, suggesting the slippage/cost assumptions might be impacting the outcome more than anticipated?

---

