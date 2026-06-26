# Max Trade settings in ASI Region

- **链接**: [Commented] Max Trade settings in ASI Region.md
- **作者**: SD92473
- **发布时间/热度**: 1年前, 得票: 24

## 帖子正文

During simulation, I have observed that there is an additional max_trade settings = "ON" specifically for ASI region alpha simulations. How does they impact the OS performance of an Alpha ?

---

## 讨论与评论 (11)

### 评论 #1 (作者: AK40989, 时间: 1年前)

The max_trade setting in the ASI region serves to limit excessive trading volume, which can impact the stability of out-of-sample performance. If your alpha relies heavily on high-frequency signals, you might see degradation when max_trade is enforced, especially if the signal is sensitive to execution constraints.

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

If you turn max trade on, low liquidity stocks will be eliminated for good alpha performance from low liquidity stocks will reduce performance. Currently max trade is a mandatory requirement with ASI.

---

### 评论 #3 (作者: CH62432, 时间: 1年前)

The  `max_trade = "ON"`  setting is specific to certain regions like ASI (Asia), where market liquidity, transaction constraints, and regulatory restrictions may differ significantly from US or EU markets. This setting plays a critical role in how the simulated Alpha translates into realistic out-of-sample (OS) performance.

---

### 评论 #4 (作者: TP85668, 时间: 1年前)

In the ASI region, enabling  `max_trade = "ON"`  improves OS performance realism by limiting exposure to illiquid stocks. While it may reduce returns slightly, it helps maintain execution quality and lowers slippage, making the alpha more robust for deployment.

---

### 评论 #5 (作者: HD25387, 时间: 1年前)

Great question — I’ve also noticed that enabling  `max_trade`  can significantly shift performance profiles, especially for alphas that benefit from small-cap or low-liquidity names. It acts as a  **realism filter** , removing stocks where execution might not be feasible at scale. This can lead to lower but more stable OS performance. I’ve found it useful to stress-test my alphas both with and without  `max_trade`  early in development to avoid surprises. Given that it’s now mandatory in ASI, building with this constraint in mind from the start is key.

---

### 评论 #6 (作者: AK98027, 时间: 1年前)

In my experience, it generally improves Sharpe ratios and reduces drawdowns, but at the cost of absolute returns. The net effect on OS score depends on your alpha's natural trade distribution - if your alpha generates large concentrated positions, max_trade will have a bigger impact. Best to backtest with both settings to see how it affects your specific alpha's risk-return profile.

---

### 评论 #7 (作者: AB64885, 时间: 1年前)

I’ve found that  `max_trade = "ON"`  in ASI is one of those quiet settings that has a huge impact, especially for alphas that lean into small or illiquid names. When I started applying it early in my alpha design process, I noticed fewer surprises in OS performance later. It forces you to think more about scalability and execution, not just backtest returns. A tip that helped me: I run parallel simulations with max_trade ON and OFF during the initial idea stage — it gives a clearer view of which ideas are robust under realistic constraints. Definitely a must-consider for long-term consistency.

---

### 评论 #8 (作者: DN45758, 时间: 1年前)

Using max_trade often improves Sharpe ratios and lowers drawdowns but can reduce absolute returns. Its impact depends on your alpha’s trade concentration. Backtesting with and without max_trade is recommended to understand its effect on your alpha’s risk-return profile and OS score.

---

### 评论 #9 (作者: SK13215, 时间: 1年前)

if u turn on max trade in ASI region is basically it helped me that can reduce absolute re turns when max trade is off .definaltely long term uses of max trade on

---

### 评论 #10 (作者: DK20528, 时间: 1年前)

I’ve noticed that too! When  `max_trade = ON`  is applied in ASI region simulations, it often helps control excessive turnover or outlier trades. This can lead to more stable and realistic OS performance, especially for aggressive alphas. Worth checking how it affects your alpha’s PnL and drawdown.

---

### 评论 #11 (作者: TP19085, 时间: 10个月前)

I’ve found that setting max_trade to "ON" in ASI is a subtle but powerful tweak, especially for alphas focused on small or illiquid stocks. Turning it on early in alpha design helps highlight scalability and execution challenges, not just backtest returns, reducing surprises in out-of-sample (OS) performance. A helpful approach I use is running parallel simulations with max_trade both enabled and disabled during idea development. This comparison reveals which alphas remain robust under realistic trading constraints. Since max_trade is now mandatory in ASI, incorporating it from the start is crucial for building consistent, scalable strategies. It acts like a realism filter by excluding names where execution at scale would be difficult, often lowering OS returns but increasing stability. This practice has been a game changer in my process, improving long-term performance and reducing risk of unexpected issues.

---

