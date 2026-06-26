# Improvement of an alpha using the decay operator on an Analyst Net Income Signal.

- **链接**: [Commented] Improvement of an alpha using the decay operator on an Analyst Net Income Signal.md
- **作者**: SM50208
- **发布时间/热度**: 2个月前, 得票: 4

## 帖子正文

Alpha = ts_decay_linear(anl4_adjusted_netincome_ft, 5)

The logic behind this is that current updates in analysts' forward net income expectations contain valuable information about future stock performance. Applying the decay function gives more weight to the recent information while gradually reducing the effect of the historical data. This yields good results since the alpha reacts faster to the new information.

---

## 讨论与评论 (2)

### 评论 #1 (作者: FZ60707, 时间: 2个月前)

Nice and clean use of linear decay on analyst net income revisions. A couple of suggestions to take it further: (1) test other decay shapes like exponential or hyperbolic to see if they better capture the fading impact of earnings surprises, and (2) consider neutralizing the signal against sector or market factors — analyst expectation changes often have strong common components. Also, have you checked the turnover and whether the decay window of 5 is robust across different market regimes? Thanks for sharing the idea.

---

### 评论 #2 (作者: CM46415, 时间: 2个月前)

Good idea and solid intuition.

Using  `ts_decay_linear`  on analyst forward net income helps capture  **recent revisions more strongly** , which is often where the real predictive edge comes from. It also reduces noise from older, stale estimates and makes the signal more responsive to changing expectations.

Just keep an eye on turnover—decay can increase reactivity, so balancing it with stability checks and correlation filtering will be important for maintaining robustness.

---

