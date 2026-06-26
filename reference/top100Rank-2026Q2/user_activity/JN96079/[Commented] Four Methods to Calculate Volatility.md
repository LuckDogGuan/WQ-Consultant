# Four Methods to Calculate Volatility

- **链接**: [Commented] Four Methods to Calculate Volatility.md
- **作者**: NT84064
- **发布时间/热度**: 10个月前, 得票: 52

## 帖子正文

**Introduction** 
Understanding volatility is fundamental to  **risk management**  and  **alpha development** . Volatility not only measures the risk level of an asset but also provides insights into potential trading signals. Let’s explore four popular methods of volatility estimation, from the simplest to more advanced ones.

### **Method 1: Standard Deviation of Daily Returns**

The most straightforward approach calculates the standard deviation of returns over a given window.

**Formula:**

`ts_stddev(returns, d)
`

Example:  `d=21`  for a 21-day (~1 month) volatility.

👉 Pros: Simple, intuitive.
👉 Cons: Treats all days equally, ignores recency effects.

### **Method 2: Exponentially Weighted Moving Standard Deviation (EWMA)**

This method assigns greater weight to recent observations, capturing the market’s “short memory.”

**Formula:**

`sqrt(ts_decay_exp_window(x^2, d, factor=f) - ts_decay_exp_window(x, d, factor=f)^2)
`

👉 Pros: More responsive to recent changes.
👉 Cons: Sensitive to decay parameter choice, more volatile estimates.

### **Method 3: Parkinson’s Volatility**

Proposed by Parkinson (1980), it uses  **high and low prices**  instead of closes, providing a more robust intraday measure.

**Formula:**

`sqrt(1/(4*log(2)) * ts_mean((log(high/low))^2, d))
`

👉 Pros: Captures full intraday range.
👉 Cons: Ignores overnight gaps.

### **Method 4: Garman–Klass Volatility**

An improvement over Parkinson, Garman–Klass (1980) incorporates  **open, high, low, close (OHLC)** , making it especially useful during events like earnings announcements.

**Formula:**

`sqrt((1/(2*window_length)) *
     ts_sum((log(high/low))^2 - ((2*log(2)-1)*(log(close/open))^2), d))
`

👉 Pros: More efficient use of OHLC data.
👉 Cons: Still subject to distortions from after-hours volatility.

### **Applications in Alpha Research**

- **Risk-adjusted signals:**  normalize returns with volatility ( `return/vol` ).
- **Anomaly detection:**  volatility spikes may indicate information asymmetry.
- **Factor combination:**  blend volatility with momentum or volume for multi-dimensional alphas.

**Conclusion** 
There is no “one-size-fits-all” volatility measure. The choice depends on:

- Available data (close-only vs. full OHLC).
- Investment horizon (short-term vs. long-term).
- Alpha objective (risk normalization vs. anomaly detection).

---

## 讨论与评论 (13)

### 评论 #1 (作者: TP85668, 时间: 10个月前)

This is an excellent summary of the four main approaches to volatility estimation, ranging from simple to more sophisticated models. I particularly like how you compared the pros and cons of each method, which makes it easier for practitioners to choose the right one depending on their data and strategy. The applications section is also very practical, showing how volatility can be directly integrated into alpha construction.

---

### 评论 #2 (作者: DJ40095, 时间: 10个月前)

Great summary of volatility estimation techniques! It's especially helpful how you've layered the methods from basic to more advanced, and tied each to its practical pros and cons. I appreciate the emphasis on aligning the method with the alpha objective and data availability too often that's overlooked. Would be interesting to see how these measures perform side by side in stress periods or high-volatility regimes.

---

### 评论 #3 (作者: AC75253, 时间: 10个月前)

great breakdown.. thanks for sharing such good information

---

### 评论 #4 (作者: ZK79798, 时间: 10个月前)

Thanks for sharing! The overview of different volatility measures is really helpful. I’ll try applying them, and it’s very inspiring for my recent research.

---

### 评论 #5 (作者: DT49505, 时间: 10个月前)

Thanks for sharing this clear and detailed explanation — very insightful!

---

### 评论 #6 (作者: JN96079, 时间: 10个月前)

The information shared here is very insightful!

---

### 评论 #7 (作者: AC75253, 时间: 10个月前)

Great overview of volatility measures. The progression from simple (std dev) to advanced (Garman–Klass) is clear and practical. EWMA’s responsiveness is useful but sensitive to parameter choice — maybe worth noting tuning strategies. Also, Parkinson and Garman–Klass miss overnight moves, which can be key in news-driven markets. Loved the alpha applications — especially using vol spikes for anomaly detection. Would be interesting to see how these perform across market regimes.

---

### 评论 #8 (作者: JC84638, 时间: 10个月前)

That’s an interesting share—gave you a like. (jzc

---

### 评论 #9 (作者: TP18957, 时间: 9个月前)

This is an excellent overview of volatility estimation techniques, and I really like how you structured it from the most basic (ts_stddev) to more advanced estimators like Parkinson and Garman–Klass. One nuance I’d add is that the choice of volatility measure often interacts with the rebalance frequency of the alpha. For example, standard deviation or EWMA works well for daily-to-weekly horizons, but Parkinson and Garman–Klass really shine in intraday-sensitive contexts where the high–low range carries more signal. On the flip side, their limitation with overnight jumps can distort risk estimates in news-driven markets, so sometimes blending close-to-close vol with intraday-based estimators yields a more balanced measure. I’ve also found it useful to normalize momentum signals by EWMA vol rather than simple stddev, since it reacts quicker to regime shifts without overreacting as much as realized variance. Would love to see a side-by-side stress test of these methods during crisis periods — that tends to expose their real strengths and weaknesses.

---

### 评论 #10 (作者: TP18957, 时间: 9个月前)

Thanks for sharing such a clear and structured breakdown of volatility measures! I especially appreciate how you didn’t just list the formulas but also explained the pros and cons of each, along with practical alpha applications. The point about choosing the right estimator depending on whether you have only close data or full OHLC was really helpful — that’s something I often overlook. The applications section (risk-adjusted signals, anomaly detection, factor blending) was also a great takeaway and gave me new ideas to test. This post really makes volatility feel less abstract and more directly usable in signal design. Much appreciated!

---

### 评论 #11 (作者: NT34170, 时间: 9个月前)

This piece highlights the relative strengths and tradeoffs of common volatility calculation approaches and situates them well within a broader quantitative framework—suited for better-modelled pricing and sizing of predictive signals.

---

### 评论 #12 (作者: YQ51506, 时间: 8个月前)

这篇文章对波动率计算方法的梳理很全面，从基础的日收益率标准差到更复杂的Garman-Klass方法都覆盖了。作为在WorldQuant Brain平台上做回测的量化研究员，我觉得这些方法在alpha因子挖掘中确实很有实用价值。特别是文章提到的风险调整信号应用，用波动率对收益率进行标准化处理，这个思路在构建稳健因子时很关键。不过在实际回测中，不同波动率估计方法对参数选择比较敏感，比如EWMA的衰减因子设置就需要仔细调优。Parkinson方法虽然能捕捉日内波动，但确实如文章所说忽略了隔夜跳空，这在某些市场环境下可能会影响因子表现。总的来说，这篇文章为波动率相关的因子开发提供了很好的技术参考。

---

### 评论 #13 (作者: IU48204, 时间: 7个月前)

These are very wonderful four points shared and they are really efficient

---

