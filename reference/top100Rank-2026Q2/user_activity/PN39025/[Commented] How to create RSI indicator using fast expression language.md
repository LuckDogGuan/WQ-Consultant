# How to create RSI indicator using fast expression language ?

- **链接**: [Commented] How to create RSI indicator using fast expression language.md
- **作者**: AV91162
- **发布时间/热度**: 3年前, 得票: 2

## 帖子正文

Is there any way, we can create and use the RSI indicator for alpha construction?

---

## 讨论与评论 (10)

### 评论 #1 (作者: AS34454, 时间: 3年前)

Yes, try using operators like ts_sum, ts_delta and conditional operators. And data fields like the "close" price.

In my experience, RSI signal has worked with Decay = 0 and Delay = 1 setting

---

### 评论 #2 (作者: AK88691, 时间: 3年前)

have you found the implementation of rsi?

---

### 评论 #3 (作者: SH71033, 时间: 3年前)

Hi,
We have datasets, that have pre calculated indicator values.
Some of these datasets are consultant datasets, available here:  [WorldQuant BRAIN](https://platform.worldquantbrain.com/learn/data-and-operators/model10)

---

### 评论 #4 (作者: RP25658, 时间: 2年前)

RSI Implementation

```
avgGAIN = ts_sum(returns > 0 ? returns : 0, 14) / 14;avgLOSS = ts_sum(returns < 0 ? -returns : 0, 14) / 14;RS = avgGAIN / avgLOSS;RSI = (100 - (100/(1+ RS)));
```

---

### 评论 #5 (作者: XL31477, 时间: 1年前)

**Hey, guys! To create RSI indicator using fast expression language, as  [AS34454](/hc/en-us/profiles/1515337426161-AS34454)  said, you can use operators like ts_sum, ts_delta and conditional ones, with "close" price data.  [RP25658](/hc/en-us/profiles/17195128096279-RP25658)  also gave a good implementation example. First, calculate avgGAIN and avgLOSS over 14 periods. Then get RS by dividing them. Finally, use the formula to work out RSI. It's a useful indicator for alpha construction. Hope this helps!**

---

### 评论 #6 (作者: DK20528, 时间: 1年前)

Yes, you can use the  **Relative Strength Index (RSI)**  indicator for alpha construction. RSI is a momentum oscillator that measures the speed and change of price movements, typically used to identify overbought or oversold conditions in a market.

Here’s how you can integrate the RSI into your alpha construction:

### 1.  **Calculate RSI** :

The RSI is calculated using the formula:

RSI=100−1001+RSRSI = 100 - \frac{100}{1 + RS}RSI=100−1+RS100​

Where:

- **RS**  = Average of  `n`  days' up closes / Average of  `n`  days' down closes.
- **n**  is the number of periods, usually set to 14.

This is a time-series indicator that you can calculate over any period (14 days is standard, but you can experiment with different periods based on your strategy).

### 2.  **Incorporate RSI into Alpha Construction** :

Once you have the RSI values, you can use them in your alpha model. For example:

- **Buy Signal (Long)** : If RSI is below a certain threshold (e.g., 30), indicating that the asset is oversold.
- **Sell Signal (Short)** : If RSI is above a certain threshold (e.g., 70), indicating that the asset is overbought.
- **Neutral Zone** : RSI between 30 and 70, indicating a neutral or consolidating market.

You can use these signals to create an alpha expression. For example, an alpha might look like:

python

Copy code

`rsi_value = RSI(price_data, period=14)
if rsi_value < 30:
    signal = 1 # Buy Signal
elif rsi_value > 70:
    signal = -1 # Sell Signal
else:
    signal = 0 # No action
`

### 3.  **Additional Techniques** :

- **RSI Divergence** : A divergence between price movement and RSI can be a powerful signal. For example, if prices are making new lows, but RSI is making higher lows, it could signal a potential trend reversal.
- **RSI with Moving Averages** : You can use RSI in conjunction with a moving average (e.g., 9-period RSI) to smooth out the signals and reduce noise.
- **RSI with Other Indicators** : Combine RSI with other indicators, like Moving Average Convergence Divergence (MACD), Bollinger Bands, or trend-following strategies for more robust alpha signals.

### 4.  **Considerations** :

- **Lookback Period** : Experiment with different RSI periods (e.g., 10, 14, 21) based on your strategy's time horizon.
- **Risk Management** : Be mindful of how RSI signals interact with your risk controls and market conditions.
- **Market Specificity** : RSI can behave differently across various asset classes (e.g., equities, commodities, currencies), so tailor your model to the specific market you are trading.

By using RSI as part of your alpha construction, you can capture momentum signals and better predict price reversals or continuations, enhancing your alpha strategy.

---

### 评论 #7 (作者: AT56452, 时间: 1年前)

The Relative Strength Index (RSI) is a momentum oscillator developed by J. Welles Wilder in 1978 to evaluate the speed and change of price movements in financial markets. It quantifies the magnitude of recent price changes to assess overbought or oversold conditions, aiding traders in decision-making processes.

---

### 评论 #8 (作者: AT56452, 时间: 1年前)

RSI is computed using the formula: RSI = 100 - [100 / (1 + RS)], where RS (Relative Strength) is the average of 'n' days' up closes divided by the average of 'n' days' down closes. Typically, a 14-day period is used for this calculation. This formula normalizes the indicator to oscillate between 0 and 100, providing a consistent framework for analysis.

---

### 评论 #9 (作者: AT56452, 时间: 1年前)

RSI values range from 0 to 100. Traditionally, an RSI above 70 suggests that a security is overbought, indicating potential for a price reversal or corrective pullback. Conversely, an RSI below 30 indicates that a security is oversold, suggesting a potential upward reversal. These thresholds help traders identify possible entry and exit points.

---

### 评论 #10 (作者: PN39025, 时间: 1年前)

Thank you for sharing this clear and concise explanation of the RSI formula. Your breakdown of the calculation and its practical use is highly insightful and greatly appreciated.

---

