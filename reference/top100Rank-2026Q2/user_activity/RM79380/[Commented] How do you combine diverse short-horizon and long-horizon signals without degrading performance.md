# How do you combine diverse short-horizon and long-horizon signals without degrading performance?

- **链接**: [Commented] How do you combine diverse short-horizon and long-horizon signals without degrading performance.md
- **作者**: JK98819
- **发布时间/热度**: 3个月前, 得票: 5

## 帖子正文

When stacking intraday micro signals with weekly/monthly fundamentals, what weighting and risk-normalization schemes work? How do you prevent short-horizon noise from dominating portfolio construction?

---

## 讨论与评论 (11)

### 评论 #1 (作者: KU30147, 时间: 3个月前)

I combine short- and long-horizon signals by normalizing them separately, then weighting based on stability and Sharpe. Long-horizon signals guide structural positioning, while short-horizon signals refine timing. I reduce noise using smoothing, decay adjustments, and correlation checks, ensuring short-term signals do not dominate portfolio exposure or degrade long-term alpha stability.

---

### 评论 #2 (作者: KP26017, 时间: 3个月前)

The core issue is that raw combination almost never works — intraday signals have much higher variance by nature, so without explicit normalization they'll dominate the composite even if their risk-adjusted predictive power is actually lower than the fundamental layer. You need to normalize not by raw signal magnitude but by  **information ratio contribution**  — scale each signal's weight by its estimated IC divided by its volatility of IC, basically reward consistency not just strength.

---

### 评论 #3 (作者: NN29533, 时间: 3个月前)

This is a classic challenge! I've found that explicitly modeling the different time-series properties and signal decay rates is crucial, rather than relying on simple linear combinations. Have you explored using Kalman filters or other state-space models to dynamically adjust weights based on the perceived regime or signal confidence at different horizons? It might help prevent short-term noise from unduly influencing the longer-term view.

---

### 评论 #4 (作者: SP39437, 时间: 3个月前)

This is a classic challenge in alpha construction, JK98819. I've found that orthogonalizing your signals before combining them, perhaps through a principal component analysis approach or simply by ensuring their covariance is minimized, can be very effective. Have you experimented with dynamic weighting based on the recent performance or volatility of each signal's underlying factors, rather than fixed weights?

---

### 评论 #5 (作者: RM79380, 时间: 3个月前)

A common approach is volatility scaling and horizon-based weighting—giving lower weights to intraday signals and higher weights to stable weekly/monthly fundamentals. Risk normalization (e.g., z-scoring, sector/market neutralization) also helps prevent short-term noise from dominating portfolio construction.

---

### 评论 #6 (作者: ML46209, 时间: 3个月前)

This is a classic challenge! I've found that carefully considering the **time-series properties of each signal type** is crucial. For instance, using decaying weights based on signal decay rates or applying different risk contribution targets for short vs. long horizon signals can help mitigate noise from the faster-moving components. Have you explored regime-switching models that dynamically adjust these combination weights based on observed market volatility or trend persistence?

---

### 评论 #7 (作者: NM98411, 时间: 3个月前)

This is a classic challenge in alpha construction! I've found that carefully considering the decay rates and signal-to-noise ratios of different horizons is crucial. Perhaps exploring dynamic weighting based on regime detection or even using a hierarchical approach where short-term signals are filtered through longer-term conviction could mitigate noise? Curious to hear if anyone has experimented with latent factor models to disentangle these time-scale effects.

---

### 评论 #8 (作者: HN47243, 时间: 3个月前)

This is a fantastic question that gets to the heart of robust alpha construction. My experience suggests that techniques like Kalman filters or dynamic conditional correlation (DCC) can help explicitly model and manage the varying predictive power and correlation structures between short-term and long-term signals, rather than just relying on static weights. Have you found specific attribution methods that help isolate performance contributions from each horizon to diagnose degradation effectively?

---

### 评论 #9 (作者: MT46519, 时间: 3个月前)

This is a classic challenge in alpha construction! One approach I've found effective is to use adaptive weighting schemes that dynamically adjust based on the recent performance or volatility of each signal horizon, perhaps even employing a Kalman filter to blend forecasts. Have you experimented with any ensemble methods that explicitly model the correlation structure between your short and long-term signals before combining them?

---

### 评论 #10 (作者: NM32020, 时间: 3个月前)

This is a fantastic question, JK98819. I've found that often, a simple weighted average can indeed drown out valuable longer-term signals, especially when volatility differs drastically. Have you experimented with methods like dynamic weighting based on signal conviction or even using a Kalman filter to merge state-space representations of short and long-term dynamics? It's a challenge to balance the responsiveness of micro-signals with the robustness of fundamentals.

---

### 评论 #11 (作者: HT71201, 时间: 3个月前)

Raw combination rarely works—intraday signals have higher variance, so they dominate unless properly normalized. Instead of scaling by magnitude, normalize by information quality: weight signals by IC divided by IC volatility, rewarding consistency over raw strength.

---

