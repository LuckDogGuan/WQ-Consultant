# Can I use Trade_when to decease the Turnover?

- **链接**: [Commented] Can I use Trade_when to decease the Turnover.md
- **作者**: TL67839
- **发布时间/热度**: 1年前, 得票: 11

## 帖子正文

In my understanding, The Turnover is too high means the trading frequency is too high. So, I want to set some limitations for my alpha and don't allow it to trade at any time.

For example, my original alpha is:

```
Hello World.
```

And then, my new alpha is:

```
triggerTradeExp = (rank(volume) > 0.5)AlphaExp= Hello World.triggerExitExp = (rank(volume) <= 0.5)trade_when(triggerTradeExp, AlphaExp, triggerExitExp)
```

I thought this would reduce the trading frequency and reduce the Turnover, but it didn't. Sometimes, it even increased the turnover. I don't know what is the problem. Does anyone know this?

---

## 讨论与评论 (24)

### 评论 #1 (作者: PL15523, 时间: 1年前)

Hi, you should try some conditions like volume < adv20 or volume < ts_mean(volume,20), should use volume variations to reduce corr better

---

### 评论 #2 (作者: AA47840, 时间: 1年前)

Turnover refers to how frequently trades occur within a given period. More formally, turnover is a measure of the average daily trading activity relative to the portfolio's holdings. It can be calculated using the formula:

**Turnover = Value Traded / Value Held**

For the above expression:

```

triggerTradeExp = (rank(volume) > 0.5)

AlphaExp = Hello World.

triggerExitExp = (rank(volume) <= 0.5)

trade_when(triggerTradeExp, AlphaExp, triggerExitExp)

```

In this case, a trade is triggered when the rank of the volume is greater than 0.5 ( `triggerTradeExp` ), and it exits when the rank of the volume becomes less than or equal to 0.5 ( `triggerExitExp` ).

This logic could lead to frequent exits, particularly when  `rank(volume)`  hovers around the threshold of 0.5. For instance, if  `rank(volume)`  is slightly above 0.5 on one day but drops just below 0.5 the next, an exit would be triggered. These frequent exits reduce the value held while increasing the value traded, thereby causing the turnover to rise. So it is necessary to choose less volatile variables in triggerTradeExp and triggerExitExp if we wish to reduce turnover.

---

### 评论 #3 (作者: TN48752, 时间: 1年前)

You can add a condition to only trade when the market return has a greater volatility than %, this will effectively reduce turnover

---

### 评论 #4 (作者: TL67839, 时间: 1年前)

Thanks to all of you, you helped me a lot!

---

### 评论 #5 (作者: LN78195, 时间: 1年前)

While adding volatility thresholds or using volume variations like  **adv20**  can help, has anyone experimented with incorporating multi-factor conditions (e.g., combining momentum and liquidity factors) to further refine entry/exit points and stabilize turnover? Would love to hear your experiences

---

### 评论 #6 (作者: AC63290, 时间: 1年前)

You can use variations of the volume found in the data explorer to both reduce turnover and reduce correlation. For example, the volume fields in the opt4 data set

---

### 评论 #7 (作者: DK20528, 时间: 1年前)

It seems you're trying to reduce trading frequency and turnover by introducing a condition based on trading volume (with  `rank(volume) > 0.5`  and  `rank(volume) <= 0.5`  for entry and exit triggers, respectively). However, this approach may not reduce turnover as you expect for a couple of reasons:

### 1.  **Trigger Conditions May Not Be Effective in Reducing Trades:**

- **Trading Frequency vs. Trading Volume** : By using  `rank(volume)` , you're ranking the volume of stocks, but not directly controlling the trading frequency. This means your strategy might still trigger trades on stocks with high rank in volume, regardless of the actual number of trades being executed. High volume does not necessarily imply low turnover or fewer trades.
- **Liquidity of Stocks** : Stocks with high volume are likely to have a lot of liquidity, which could cause your strategy to trigger more often, especially if there are multiple opportunities in a given timeframe for stocks that fit the condition. This can inadvertently lead to more trades, not fewer.

### 2.  **Timing of Entry and Exit (Ranked Volume)** :

- **Exit Conditions** : The exit condition based on  `rank(volume) <= 0.5`  might not effectively reduce trading activity. For example, you might be triggering an exit because a stock's rank drops below 0.5, but if there are many stocks with high turnover, your strategy could still close positions quickly and open new ones frequently. This would still result in high turnover.
- **Entry-Exit Timing** : If your entry condition triggers when the stock’s volume rank is higher than 0.5, but then exits when it drops below 0.5, you may end up with frequent entry-exit cycles, which could increase turnover. The issue is that both conditions ( `rank(volume) > 0.5`  and  `rank(volume) <= 0.5` ) might not necessarily align in a way that reduces trades over time.

### 3.  **Strategy Overfitting to Volume** :

- **Market Movements** : If the volume rank is just one part of the strategy, it might not account for broader market factors influencing stock movements. Even with a volume-based filter, market trends or volatility can still lead to trades that aren’t related to volume rank but to broader market behavior, thus increasing turnover.

### Potential Solutions to Reduce Turnover:

- **Implement Time-Based Filters** : Consider adding a time filter to restrict how often a stock can be traded within a given period. For example, a stock might not be eligible to be traded again until a certain number of days have passed after an exit.
- **Add Additional Filters** : You could incorporate other conditions, such as volatility or price movement thresholds, to better control trading frequency. For example, only allow trades if the stock’s price moves a certain percentage in a given timeframe, or if the market conditions are favorable for trading.
- **Position Size Constraints** : Control turnover by limiting the size of your trades. This reduces the impact of frequent small trades while keeping your strategy in line with market conditions.
- **Lookback Period** : Introduce a lookback period for the volume rank to smooth out any short-term spikes or drops in volume. For example, you could rank average volume over a 5-day or 10-day period to avoid reacting to short-term fluctuations.

### Example of Adjusted Alpha with Additional Conditions:

python

Copy code

`triggerTradeExp = (rank(volume, 5) > 0.5) and (volatility() < 0.02)  # Example: rank over 5 days and volatility threshold
AlphaExp = HelloWorld()
triggerExitExp = (rank(volume, 5) <= 0.5) or (volatility() > 0.02)  # Exit if low volume rank or high volatility
trade_when(triggerTradeExp, AlphaExp, triggerExitExp)
`

This would control trading frequency better by considering both volume rank over a period (instead of just one day) and volatility as additional conditions for trade entry and exit.

In summary, the issue may stem from the interaction between the volume ranking and the trading frequency, leading to more trades instead of fewer. Refining your conditions, adding additional filters, or restricting trade frequency through time-based or volatility-based constraints could help achieve your goal of reducing turnover.

---

### 评论 #8 (作者: AM60509, 时间: 1年前)

Yes, Trade_When can be used to reduce turnover. It only executes if condition is true and in other cases the alpha remains the same,no new assignment occurs.

---

### 评论 #9 (作者: XL31477, 时间: 1年前)

**Hey, I think the main problem is that just relying on rank(volume) conditions might not work well as you expected. Sometimes the rank(volume) hovering around the threshold can cause frequent exits and entries, thus increasing turnover. As others mentioned, adding more factors like volatility, or using time-based filters could be better. Also, considering a lookback period for volume rank can smooth things out. Try to combine these to make your trade_when conditions more effective in reducing turnover.**

---

### 评论 #10 (作者: AY96883, 时间: 1年前)

HELLO

[TL67839](/hc/en-us/profiles/21239286987031-TL67839)

You can also use **HUMP** operator to reduse turnover and its giving good signals.

---

### 评论 #11 (作者: TL67839, 时间: 1年前)

Thanks for everyone's suggestions, but I have one more question. I use some variables (like volume<adv20 or

rank(historical_volatility_20) > 0.3) to draw down the turnover, but I found that the returns also decreased with the turnover. Do you guys have any idea about how to draw down the turnover with returns and sharpe fixed?

---

### 评论 #12 (作者: CC40930, 时间: 1年前)

It seems like the issue with your approach might be that you're setting a condition based on volume ranking, which could lead to frequent switching between the condition being met or not, thus still causing a high turnover.

---

### 评论 #13 (作者: KS69567, 时间: 1年前)

**Trade_When**  is an effective mechanism to reduce turnover in a trading system. By executing trades only when specified conditions are met, it ensures that the alpha remains unchanged when the conditions are not satisfied, avoiding unnecessary assignments or trades. This targeted execution minimizes transactional overhead and supports a more stable and efficient trading strategy or the  **HUMP operator**  is another effective tool for reducing turnover while providing reliable signals. By leveraging its functionality, you can enhance the efficiency of your trading strategy, ensuring minimal unnecessary trades while maintaining high-quality decision-making based on robust signals.

---

### 评论 #14 (作者: KJ42842, 时间: 1年前)

[TL67839](/hc/en-us/profiles/21239286987031-TL67839)

Return decrease at the same time with turnover is quite usual in alpha creation, you can try different events or conditions to find the optimal one.

---

### 评论 #15 (作者: NH84459, 时间: 1年前)

The  **doubling of the return**  (0.5 in the denominator) comes into play because if you had invested the entire capital (including the non-deployed cash), you could have earned more. However, since only half of the capital is actively working, the return is effectively calculated on a "half capital" basis. It’s an adjustment to make the calculation of the returns fairer by considering the uninvested portion.

---

### 评论 #16 (作者: AK52014, 时间: 1年前)

Hey, relying solely on rank(volume) conditions may cause frequent entries and exits, increasing turnover. A lookback period can smooth fluctuations, while adding factors like volatility or time-based filters can improve stability. Combining these can enhance trade_when conditions for better efficiency.

---

### 评论 #17 (作者: TD17989, 时间: 1年前)

**Price + Fundamental Data** : Combine historical price data with fundamental indicators (P/E ratio, Earnings Growth, etc.) to create alphas that predict price movement based on underlying business health.

---

### 评论 #18 (作者: MA97359, 时间: 1年前)

Yes, you can use TradeWhen to control the turnover of the alpha. It helps manage trading frequency and optimize execution based on signal conditions.

---

### 评论 #19 (作者: QG16026, 时间: 1年前)

It makes sense that frequent entry or exit due to volume rank fluctuations can increase turnover rather than reduce it. I'll definitely experiment with multi-factor conditions and a lookback period to refine my approach.

---

### 评论 #20 (作者: PT55616, 时间: 1年前)

Yes you can use the trade_when to reduce turnover, by using price volume/ fundamental as trigger condition and your alpha as weight condition, however it will take time to find best trigger suitable for you

---

### 评论 #21 (作者: NN89351, 时间: 1年前)

Hey, using only rank(volume) conditions might lead to excessive trading, which can drive up turnover. Adding a lookback period can help smooth out short-term noise, while incorporating factors like volatility or time-based filters can make entries more stable. A well-balanced approach to trade_when conditions can improve execution efficiency and reduce unnecessary trades.

---

### 评论 #22 (作者: AK40989, 时间: 1年前)

Using `trade_when` can indeed help manage turnover, but the conditions you set are crucial. Your current setup may lead to frequent trades if the volume rank fluctuates around the 0.5 threshold, causing unnecessary exits and increasing turnover.

---

### 评论 #23 (作者: HD25387, 时间: 1年前)

Using  **trade_when**  can help control trading frequency, but its impact on  **Turnover**  depends on how the conditions interact with market movements. If your entry and exit rules trigger trades frequently, you may still experience high turnover. One possible issue is that  **rank(volume) > 0.5**  may not provide strong enough filtering, leading to frequent rebalancing. You might try  **smoother conditions**  (e.g., a moving average of volume) or  **adding holding period constraints**  to stabilize positions. Also, check how your  **alpha values change between trade decisions** , as excessive fluctuations can force unwanted trades.

---

### 评论 #24 (作者: YQ51506, 时间: 7个月前)

大佬提到的trade_when用法确实值得探讨。从你的描述看，用rank(volume)作为交易触发条件，理论上应该能降低换手率，但实际效果不理想甚至反向。这可能是因为volume的rank值在0.5附近频繁波动，导致交易信号反复触发。我在WorldQuant Brain平台回测时也遇到过类似情况，有时候看似合理的过滤条件反而会增加不必要的交易。建议可以尝试用更稳定的指标作为触发条件，比如用移动平均的volume或者结合其他技术指标。另外，trade_when的触发逻辑需要仔细设计，避免在边界值附近频繁切换。

---

