# Why is -(open-close) this not working?

- **链接**: [Commented] Why is -open-close this not working.md
- **作者**: PT60851
- **发布时间/热度**: 2年前, 得票: 2

## 帖子正文

I am new to quantitative finance and i am not much aware what happens behind the scenes after clicking on simulate button although i read the starter pack.
Question:  according to "-(open-close)" if price closes below the open then there is bearish sentiment and returns -ve value (assign negative weights) which will short the stock and if it close above the open then bullish sentiment is there and +ve weight will be assigned so it will buy the stock as per my understanding.
but when i simulate it in my platform it performs bad.Why?

---

## 讨论与评论 (16)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi!

What you are attempting to implement is based on the concept of momentum (close-open) -- the belief that if a stock's price rises, it will continue to rise, and vice versa. Such strategies can potentially be found, but it is challenging. You might want to consider using more time series data, as currently, you're only considering the price difference from one day.

Also, your expression isn't normalized, which means stocks with higher prices have more influence. You could correct this by normalizing your data, perhaps by dividing your values by a time series of closing prices.

The third point to consider is that significant price movements – indicative of a strong, defined trend – are relatively rare in the market. Most of the time, prices remain fairly flat, hence, the (close-open) value is not a sentiment in itself.

Sentiment is better defined by substantial price changes in response to specific events - like corporate actions, dividend announcements, or the publication of analytic forecasts. You might want to use a 'trade_when' operator, to trigger action based on these significant events, and only use the normalized (close-open) value when such events occur. Ideally, these events should act as the start point of a momentum signal.

---

### 评论 #2 (作者: PT60851, 时间: 2年前)

Yeah makes sense, Thanks a lot.

---

### 评论 #3 (作者: Permanently deleted user, 时间: 2年前)

Thanks

---

### 评论 #4 (作者: DK20528, 时间: 1年前)

Your understanding of the strategy based on  **open-close price differences**  is mostly correct: when the closing price is below the opening price, it suggests a bearish sentiment, and when the closing price is above the opening price, it suggests a bullish sentiment. Typically, you'd assign a negative weight to bearish stocks (to short them) and a positive weight to bullish stocks (to go long).

However, if the simulation of your strategy is performing poorly, there could be several reasons for this. Let's explore some possibilities:

### 1.  **Over-Simplified Strategy**

- The approach based solely on  **open-close price differences**  might be too simple. In reality, stock prices can be affected by many other factors like market news, overall market conditions, company fundamentals, etc. A strategy that uses only a single indicator might miss out on important signals.
- **Suggestion** : Try incorporating additional factors such as momentum, volume, or other technical indicators like moving averages, RSI, etc., to improve your strategy.

### 2.  **Market Noise and Overfitting**

- The open-close difference is influenced by short-term market fluctuations, which can be quite noisy. Relying solely on this information may lead to overfitting, where the strategy works well in backtesting but fails in live simulations or real-market conditions due to the inherent randomness and noise in financial markets.
- **Suggestion** : Incorporate a longer-term perspective (e.g., moving averages or trend indicators) to filter out noise and focus on more meaningful signals.

### 3.  **Risk Management and Position Sizing**

- It's possible that the strategy isn't using proper  **risk management** . Even if the signal (open-close price difference) is correct, how much capital you allocate to each trade and when to exit the position are crucial for overall performance.
- **Suggestion** : Introduce position sizing, stop-loss, and take-profit levels to manage risk effectively. This will help in reducing the impact of losing trades and improve overall performance.

### 4.  **Transaction Costs and Slippage**

- In live markets, there are  **transaction costs** , such as commission fees and slippage, which might not have been accounted for during the simulation. These factors can have a significant negative impact on the performance of a strategy, especially if it's trading frequently.
- **Suggestion** : Ensure that your simulation includes realistic assumptions about transaction costs and slippage to reflect real-world trading conditions.

### 5.  **Market Regimes and Data Periods**

- The strategy might be performing poorly because it doesn't account for changing market conditions (e.g., bull markets, bear markets, or sideways markets). A strategy that works in one type of market may fail in another.
- **Suggestion** : Consider testing your strategy across different market conditions and incorporating adaptive models that can adjust to varying market environments.

### 6.  **Signal Frequency and Timing**

- If the strategy generates a signal to buy or sell every day or too frequently, the frequency of trades may lead to lower profitability due to high transaction costs or suboptimal timing.
- **Suggestion** : Limit the frequency of trades or use filters to only trigger trades when there is a strong signal (e.g., combining open-close with a momentum indicator or using longer time horizons).

### 7.  **Backtest Bias**

- There could be issues with  **data mining**  or backtest bias. If you're working with a limited dataset or are over-optimizing the model, it could lead to a scenario where the strategy looks good in backtesting but doesn't generalize well to unseen data (out-of-sample).
- **Suggestion** : Ensure you're using an  **out-of-sample**  validation set to test the strategy's robustness and prevent overfitting to historical data.

### Next Steps:

- Try refining the strategy by adding other features or filters.
- Focus on improving  **risk management**  and adjust  **position sizing** .
- Consider testing the strategy over different market conditions and data periods to see how it performs in varying environments.
- Incorporate transaction costs and slippage to simulate more realistic trading conditions.

By addressing these aspects, you should be able to improve your strategy and its performance in simulations. Let me know if you'd like to dive deeper into any specific aspect of your strategy!

---

### 评论 #5 (作者: MK58212, 时间: 1年前)

Thanks

---

### 评论 #6 (作者: RK48711, 时间: 1年前)

Your strategy based on open-close price differences is generally sound, but its poor performance may stem from factors like oversimplification, market noise, and lack of proper risk management. To improve, consider adding more indicators, accounting for transaction costs and slippage, testing across different market conditions, and reducing trade frequency. Ensure proper position sizing and use out-of-sample testing to avoid overfitting. Refining these aspects should enhance the strategy's performance.

---

### 评论 #7 (作者: XL31477, 时间: 1年前)

Hey! The reason it performs bad could be multiple things. Firstly, it might be too simple just relying on (open-close). You should add more factors like momentum or volume. Secondly, market noise can mess it up and cause overfitting. Thirdly, proper risk management like position sizing and stop-loss might be lacking. Also, don't forget about transaction costs and slippage which matter in real trading. Try working on these aspects to improve its performance.

---

### 评论 #8 (作者: SJ17125, 时间: 1年前)

Hii,

What you’re implementing aligns with momentum strategies based on (close - open), but it has some limitations. Using more time-series data instead of single-day differences could enhance your approach. Normalize your values, perhaps by dividing by closing prices, to prevent high-priced stocks from dominating. Significant price movements that reflect strong trends are rare, so (close - open) alone might not represent sentiment effectively. Instead, combine it with event-based triggers like corporate actions or forecasts using a  `trade_when`  operator to capture meaningful momentum signals at key moments.

---

### 评论 #9 (作者: BA51127, 时间: 1年前)

The concept of using the difference between the open and close prices to infer market sentiment is a straightforward approach to gauging short-term price action. However, as you've noticed, simply using -(open-close) as an alpha strategy may not yield good performance. Here are a few reasons why this might be the case and some suggestions for improvement:

1. **Market Noise** : Financial markets are subject to a great deal of noise on a day-to-day basis. The difference between the open and close prices can be influenced by random fluctuations that do not necessarily indicate a sustained trend or sentiment.
2. **Lack of Context** : A single day's price action may not provide enough context to determine a trend. It could be more effective to look at the change over a longer period or in conjunction with other indicators.
3. **Oversimplification** : Relying on a single metric for decision-making can be limiting. You might want to incorporate additional factors such as volume, volatility, or other technical indicators that could provide a more comprehensive view of market sentiment.
4. **Normalization** : As AG20578 pointed out, your expression isn't normalized. This means that stocks with higher prices can disproportionately affect the strategy's performance. Normalizing the data, perhaps by dividing the (close-open) value by the closing price or a moving average, could help to equalize the influence of different stocks.
5. **Event-Driven Trading** : Price movements often occur in response to specific events. Using a 'trade_when' operator to trigger trades based on significant events, in conjunction with the (close-open) value, could help to identify more meaningful signals.
6. **Risk Management** : A poorly performing strategy could also be a result of inadequate risk management. Incorporating proper position sizing, stop-loss orders, and taking profit at appropriate levels can help protect against large drawdowns and enhance overall performance.
7. **Market Conditions** : Different market conditions can significantly affect the performance of a strategy. It's important to test your strategy across various market environments to ensure it's robust and not just performing well in a specific type of market.
8. **Transaction Costs** : In live trading, transaction costs such as commissions and slippage can eat into profits. Make sure to account for these in your simulation to get a more accurate picture of how the strategy will perform in real trading.

To improve your strategy, consider testing it with additional factors, over different time frames, and across various market conditions. Also, ensure that you're using proper risk management techniques and accounting for transaction costs. By refining your approach in these areas, you may be able to improve the performance of your alpha strategy.

---

### 评论 #10 (作者: XL31477, 时间: 1年前)

**Hey! There are several possible reasons for its poor performance. Firstly, it might be too simple relying just on (open - close). Adding more factors like momentum or volume could help. Secondly, market noise can impact it and lead to overfitting. Also, proper risk management like position sizing and stop-loss is important. Don't forget about transaction costs and slippage which matter in real trading. Consider working on these aspects to boost its performance.**

---

### 评论 #11 (作者: DN45758, 时间: 1年前)

[AG20578](/hc/en-us/profiles/12243980162327-AG20578)

The momentum strategy based on (close-open) can be improved by using more time series data and normalizing the values, as price differences alone may not capture true sentiment. Consider incorporating event-based triggers like corporate actions and earnings announcements for more reliable momentum signals.

Thank you for sharing these valuable insights!

---

### 评论 #12 (作者: CC40930, 时间: 1年前)

While the expression  `-(open - close)`  correctly captures the sentiment direction based on daily price movement, it might be too simplistic and susceptible to noise or market conditions. To improve the performance, it's essential to refine your alpha strategy by adding more sophisticated features, implementing risk management techniques, and testing across different market conditions. Don't be discouraged by early performance—quantitative finance requires iterative testing and learning.

---

### 评论 #13 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #14 (作者: SV11672, 时间: 1年前)

Hi,BA51127

"Great points to consider when refining an alpha strategy! Protecting against large drawdowns and enhancing overall performance are crucial."

---

### 评论 #15 (作者: PP87148, 时间: 1年前)

The strategy you're working with looks at stock price movements, assuming a rise means it will continue. However, using just one day's price change can be misleading. It's better to use more data and focus on big events, like company news, that drive real momentum.

---

### 评论 #16 (作者: DP14281, 时间: 1年前)

Great ideas about price momentum

---

