# Setting MAX TRADE in Region

- **链接**: Setting MAX TRADE in Region.md
- **作者**: DM28368
- **发布时间/热度**: 9个月前, 得票: 10

## 帖子正文

Hello everyone, when simulating Alpha (not in the ASIA region) with Max Trade set to OFF, my alpha typically performs better compared to when Max Trade is set to ON. However, when Max Trade is ON, there are constraints on the scale and trading volume for less liquid stocks. So, does setting Max Trade to ON always lead to better Alpha results on OS? Please share your opinions.Thanks all.

---

## 讨论与评论 (5)

### 评论 #1 (作者: SG91420, 时间: 9个月前)

Since the model isn't penalized for trading expenses or liquidity restrictions, MaxTrade is OFF, allowing your alpha to take huge positions in illiquid stocks without any restrictions. This might artificially inflate performance metrics. As a result, there may be signals that appear powerful but are actually not scalable.Conversely, MaxTrade ON limits exposure to less liquid equities and minimizes excessive turnover by enforcing volume and liquidity restraints. This usually results in more stable, investable alphas that perform better in live markets and out-of-sample testing, even though it frequently lowers raw performance measures.  That's my opinion.

---

### 评论 #2 (作者: JC84638, 时间: 9个月前)

In fact, it depends on your objective. If you want to play it safe with a single alpha, using ON more often makes sense. But if you’re looking at the entire portfolio, it’s not always the case. Please refer to:[Discussion] MaxTrade ON vs. OFF: A Useful Contrast, but Handle with Care ☕︎(jzc

---

### 评论 #3 (作者: JN96079, 时间: 9个月前)

The results you get while dealing with Max Trade depend on your idea and the alpha implementation. However, withMax Trade ON, you limit either the size of trades, the amount of capital allocated per trade, or trading volume per stock. Maybe this also imposes constraints based on liquidity, risk, or similar.Also, with it ON, raw return may decline, but risk-adjusted (e.g., alpha per unit risk or volatility) may improve.Otherwise, with your question, "Does 'Max Trade ON' always lead to better alpha?" No. It depends heavily on:Signal strength: If your alpha signals are extremely strong, well supported by fundamental/liquidity analysis, then OFF might yield higher yields.Liquidity of the names: In very liquid stocks, Max Trade constraints may not bind strongly; OFF vs ON won't look very different. In illiquid names, constraints bite more.Market conditions: In volatile markets or when liquidity dries up, having constraints (Max Trade ON) can protect you; in calm and liquid times, being aggressive (OFF) may benefit more.Transaction costs, slippage, etc.If these are properly modeled, ON tends to help; if they are ignored, OFF will look artificially good.Scale/capital size of your strategy: Small capital can move more freely; as capital grows, constraints matter more.In my opinion, and how I deal with theMax Tradefeature, take the following notes;If your goal is picking out what signalscoulddo in an ideal setting (for research), OFF is fine.If your goal is to deploy a strategy with real money and sustaining performance, ON is necessary.Probably best is to run both: use OFF during signal discovery/alpha generation, then test with ON to see how much of the alpha survives when realistic constraints are in place. The difference between OFF and ON is kind of your “capacity” or “scaling” risk.Possibly, you should tune the Max Trade constraint: set it so that in realistic worst-case liquidity, you still could execute; maybe adapt it dynamically (i.e., allow larger trades in more liquid names, smaller in illiquid ones), rather than a one-size-fits-all constraint.

---

### 评论 #4 (作者: RP41479, 时间: 9个月前)

Max Trade ON limits trade size, capital per trade, or stock volume, often improving risk-adjusted returns but sometimes lowering raw returns. Its impact depends on signal strength, liquidity, market conditions, transaction costs, and strategy scale. Use OFF for research and discovery, then test ON to assess realistic alpha survival. Dynamic tuning based on liquidity is ideal.

---

### 评论 #5 (作者: BK35905, 时间: 5个月前)

I’ve noticed the same—turning Max Trade OFF often boosts performance, while ON limits scale for illiquid stocks.

---

