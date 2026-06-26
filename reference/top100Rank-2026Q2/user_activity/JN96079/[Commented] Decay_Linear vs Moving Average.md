# Decay_Linear vs Moving Average

- **链接**: [Commented] Decay_Linear vs Moving Average.md
- **作者**: SK14400
- **发布时间/热度**: 9个月前, 得票: 12

## 帖子正文

What’s your experience using  `decay_linear`  instead of a simple  `ts_mean` ?
Does the linear decay really improve responsiveness for short-term momentum signals, or does it just add noise?

---

## 讨论与评论 (4)

### 评论 #1 (作者: TP85668, 时间: 9个月前)

In my experience,  `decay_linear`  can make signals more responsive to recent moves, which helps in short-term momentum, but it also risks adding noise if the window is too small.  `ts_mean`  is smoother and more stable—so I usually compare both and choose depending on volatility regime.

---

### 评论 #2 (作者: JN96079, 时间: 9个月前)

That’s a good question. The trade-off between a linear decay (or linearly weighted average, through  *decay_linear* ) vs. a simple (uniform) mean( *ts_mean* ) is subtle — you’re trading bias vs variance, and responsiveness vs stability. I’ve used both in quant strategies, and here’s a breakdown of my experience, and how I think about it;

- ***ts_mean(x, d)*** is just the simple moving average over the past  *d*  days: each day gets weight = 1/d (ignoring NaNs or special sparse handling). It is maximally “flat” and smooth, but gives no extra emphasis to more recent data within the window.
- ***ts_decay_linear(x, d)*** (i.e., a linear weighted scheme) gives higher weight to more recent observations and decays linearly down to zero (or some base) at the oldest point. In effect, it’s akin to a triangular window, where more recent days count more.

Thus, the linear decay shifts more “mass” toward the tail (recent) part of the window, making the estimate more responsive to recent changes (while still using historical data, but with diminishing influence).

---

### 评论 #3 (作者: DT49505, 时间: 9个月前)

I’ve been testing decay_linear vs ts_mean as well, and I keep running into the responsiveness vs stability trade-off. Linear decay feels great when trends are sharp, but sometimes it just amplifies noise in choppier markets. I’m still exploring whether it makes sense to switch dynamically based on volatility regime, or just stick with one consistently. Do you usually treat decay choice as fixed, or adjust it depending on market conditions?

---

### 评论 #4 (作者: AG14039, 时间: 9个月前)

I’ve been experimenting with decay_linear versus ts_mean too, and it really highlights the responsiveness versus stability trade-off. Decay_linear reacts well to sharp trends but can amplify noise in choppy markets, while ts_mean smooths things out at the cost of lag. I’m still debating whether to switch dynamically based on volatility regimes or keep one approach consistent—do you usually fix your decay method, or adjust it according to market conditions?

---

