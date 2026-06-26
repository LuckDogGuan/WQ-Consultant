# Propose a Combined Alpha Idea but need to be refined, Open to Discussion

- **链接**: [Commented] Propose a Combined Alpha Idea but need to be refined Open to Discussion.md
- **作者**: YZ44505
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

**Propose an alpha idea but need to be refined :)**

**Alpha Idea:**  trade based on momentum with volume and volatility filters. This alpha strategy aims to identify securities that are showing strong momentum with supporting volume, which can act as a confirmation of the trend. The idea is that an increase in price accompanied by higher volume is a stronger signal of continued momentum compared to price movements on low volume.

MoS= (close - ts_delay(close, 20)) / ts_delay(close, 20)

VoS = volume / adv20 - 1

Alpha = MoS * VoS

**Momentum Score (MoS)** : Calculate the momentum as the percentage change in closing price over the past 20 days.

**Volume Score (VoS)** :Normalize the current volume against the 20-day average volume to see if recent activity is higher than usual.

**Combined Alpha Score** :Multiply the momentum score by the volume score to integrate both price change and trading volume into the alpha. The rationale here is that significant price changes on high volume are more indicative of sustainable movements.

**Reversed Edition of this Alpha and Rationale:**  securities that are showing strong momentum with supporting volume, might experience decrease in price with lower momentum due to market-neutral forces.

MoS= (close - ts_delay(close, 20)) / ts_delay(close, 20)

VoS = volume / adv20 - 1

Alpha = -MoS * VoS        // here I add negative sign to reverse the trade

---

## 讨论与评论 (13)

### 评论 #1 (作者: CC40930, 时间: 1年前)

This is a solid alpha idea that effectively combines momentum with volume, a proven method to capture strong price moves with validation from trading activity. I like the inclusion of the reversed edition to account for mean reversion. To refine this further, you might consider applying additional filters like volatility or adjusting the weights between MoS and VoS for more fine-tuned control. Additionally, a risk-neutralization approach might help ensure the alpha performs well in different market conditions. Overall, great concept!

---

### 评论 #2 (作者: TD17989, 时间: 1年前)

Hi, I noticed you can replace MoS= (close - ts_delay(close, 20)) / ts_delay(close, 20) with return or mean return in 20 days, which will save data and op used for tie break

---

### 评论 #3 (作者: ND68030, 时间: 1年前)

Hi, I think your current alpha is too simple, which will lead to very high prod corr, you can neutralize with factors like option or risk to reduce corr

---

### 评论 #4 (作者: QG16026, 时间: 1年前)

Combining momentum with volume is a solid strategy, and the reversed version offers an interesting twist for mean reversion. To refine this further, you might want to add a volatility filter to capture extreme price movements and prevent false signals in low-volatility environments.

---

### 评论 #5 (作者: TT55495, 时间: 1年前)

Your alpha idea combining momentum with volume and volatility filters is solid, as both momentum and volume are key drivers of market trends. The Momentum Score (MoS) using the 20-day price change is effective, but consider smoothing it with an exponential moving average (EMA) or adjusting the window to reduce noise. The Volume Score (VoS), which normalizes current volume against the 20-day average, works well, but you could enhance it by using the Z-score to capture extreme volume changes more effectively. Combining MoS and VoS is a good approach, but setting thresholds for both scores could filter out weak signals and improve performance. The reversed alpha (negative sign) to capture mean-reversion, you should backtest it to avoid excessive whipsaws. Additionally, considering market conditions and adding a trend strength or volatility filter would help refine the strategy.

---

### 评论 #6 (作者: NH84459, 时间: 1年前)

The idea is to capture  **price momentum**  over the last 20 days. You calculate momentum by comparing the current price to the price 20 days ago. However, to make it more effective, consider adding a  **rate of change (ROC)**  in the MoS, to adjust for the magnitude of the price movement.

---

### 评论 #7 (作者: TN48752, 时间: 1年前)

Hi, you should not use combine alpha but use robust raw signal, because the combine part has super alpha as the work.

---

### 评论 #8 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #9 (作者: CT68712, 时间: 1年前)

Hey, I love your alpha idea focusing on momentum with volume and volatility filters! It's a solid approach given how strong momentum can signal future price movements, especially when confirmed by volume. The combination you've proposed makes a lot of sense for quant traders like us, aiming to capitalize on significant price changes. Integrating a reversed strategy is particularly clever for exploring mean reversion opportunities. Just a thought, maybe consider adding a volatility filter or adjusting the weights between MoS and VoS for fine-tuning. Make sure to backtest it thoroughly to see how it performs across various market conditions. Keep up the great work!

---

### 评论 #10 (作者: AC63290, 时间: 1年前)

Let me first fix the code error, then provide feedback on the alpha idea:

### Code Error Fix

```
alpha_list = [ace.generate_alpha(x, 
    region="GLB",
    universe="MINVOL",
    neutralization="STATISTICAL",
    decay=0,
    test_period="P2Y") for x in alpha_list]

```

Key corrections:

- Fixed function name and parameters
- Corrected "testperied" to "test_period"
- Fixed syntax and spelling errors

### Alpha Strategy Analysis & Refinement

Your momentum-volume alpha idea has potential, but here's how we can refine it:

1. **Enhanced Momentum Score (MoS)**

```
# Add volatility adjustment
vol_adj = ts_std(returns, 20)
MoS = (close - ts_delay(close, 20)) / (ts_delay(close, 20) * vol_adj)

# Or use multiple timeframes
MoS = (
    0.5 * (close - ts_delay(close, 10)) / ts_delay(close, 10) +
    0.3 * (close - ts_delay(close, 20)) / ts_delay(close, 20) +
    0.2 * (close - ts_delay(close, 30)) / ts_delay(close, 30)
)

```

1. **Improved Volume Score (VoS)**

```
# Add volume trend
vol_trend = ts_mean(volume, 5) / ts_mean(volume, 20)
VoS = (volume / adv20 - 1) * vol_trend

# Or use volume acceleration
VoS = ts_delta(volume / adv20, 5)

```

1. **Enhanced Final Alpha**

```
# Add risk filters
volatility_filter = ts_std(returns, 20) < ts_mean(ts_std(returns, 20), 60)
volume_filter = volume > ts_mean(volume, 20)

Alpha = MoS * VoS * volatility_filter * volume_filter

```

#### Key Improvements:

1. **Risk Management**

- Volatility adjustment
- Multiple timeframe analysis
- Volume trend confirmation

1. **Signal Quality**

- Reduced noise through filters
- Better trend confirmation
- More robust volume analysis

1. **Turnover Control**

- Smoother signals
- Better position sizing
- Reduced false signals

#### Additional Considerations:

1. Add sector neutralization
2. Consider market cap weighting
3. Implement decay functions
4. Test different lookback periods
5. Add correlation filters

Remember to:

- Test across different market conditions
- Monitor turnover and capacity
- Consider transaction costs
- Validate statistical significance

The reversed strategy could work in mean-reversion scenarios, but consider market conditions and proper risk management.

---

### 评论 #11 (作者: PL15523, 时间: 1年前)

Thanks for sharing this idea! I’d be interested to hear how backtesting with these adjustments impacts the results.

---

### 评论 #12 (作者: RB98150, 时间: 1年前)

This alpha idea effectively combines momentum with volume to capture strong trends. The reversed edition adds an interesting twist. Refinement could include incorporating volatility filters (e.g.,  `ts_volatility` ) and neutralizing by sector ( `group_neutralize` ) for better diversification and risk-adjusted returns.

---

### 评论 #13 (作者: PT27687, 时间: 1年前)

This alpha strategy seems quite intriguing! The integration of both momentum and volume filters could provide a robust edge, especially in fast-moving markets. I'd be curious about how you plan to backtest this approach and the types of securities you think would be best suited for it. Have you considered incorporating additional technical indicators to further refine the signals?

---

