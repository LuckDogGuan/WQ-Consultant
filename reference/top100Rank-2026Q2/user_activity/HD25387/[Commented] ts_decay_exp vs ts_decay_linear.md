# ts_decay_exp vs ts_decay_linear

- **链接**: [Commented] ts_decay_exp vs ts_decay_linear.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 35

## 帖子正文

Decay functions weight past observations differently. Linear decay decreases steadily, while exponential emphasizes the most recent values.
For momentum signals, exponential decay can sharpen responsiveness, but may cause turnover spikes. Linear decay smooths transitions and can be more stable.
👉 Question: Do you systematically compare both decays in backtests, or default to one type depending on dataset?

---

## 讨论与评论 (3)

### 评论 #1 (作者: HD25387, 时间: 8个月前)

I usually compare both decays during testing since their impact on turnover and stability can be quite different. Exponential decay often works better for short-horizon momentum, while linear is more robust for smoother, longer-term effects. Defaulting to one risks missing dynamics that only show up under the other weighting.

---

### 评论 #2 (作者: AG14039, 时间: 6个月前)

I usually test both decay types because they can have very different effects on turnover and stability. Exponential decay tends to suit short-horizon momentum signals, while linear decay is often more robust for smoother, longer-term effects. Relying on just one by default can mean missing dynamics that only emerge under the alternative weighting.

---

### 评论 #3 (作者: SP39437, 时间: 6个月前)

Decay functions determine how much weight past observations receive in a signal. Linear decay reduces weights gradually over time, while exponential decay places much greater emphasis on the most recent data points. This difference can meaningfully affect both responsiveness and stability in alpha behavior.

For momentum-style signals, exponential decay often sharpens responsiveness and helps capture short-term moves more quickly, but it can also lead to higher turnover and sensitivity to noise. Linear decay, by contrast, produces smoother transitions and is generally more stable, making it better suited for longer-horizon effects or signals tied to slower economic processes.

Because these decay types can lead to very different outcomes, I usually test both rather than relying on one by default. Some dynamics only emerge under alternative weighting schemes, and testing both helps reveal whether performance is driven by genuine signal structure or by sensitivity to recent fluctuations. Comparing turnover, Sharpe stability, and out-of-sample behavior under each decay provides valuable insight into the signal’s true robustness.

How do you decide when a signal’s responsiveness justifies the added turnover risk from exponential decay?

---

