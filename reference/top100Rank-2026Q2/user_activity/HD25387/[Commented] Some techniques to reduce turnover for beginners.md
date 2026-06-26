# Some techniques to reduce turnover for beginners

- **链接**: [Commented] Some techniques to reduce turnover for beginners.md
- **作者**: TP19085
- **发布时间/热度**: 5个月前, 得票: 33

## 帖子正文

Hello everyone! To reduce  **turnover**  (high turnover means higher transaction costs), you can apply some of the following techniques:

- Use operators such as  **`hump`**  and  **`trade_when`**
- Enable  **Max-trade**
- Increase the time window in  **time-series operators**
- Simulate alphas on  **larger universe sizes**

I hope this post is helpful to you.

---

## 讨论与评论 (5)

### 评论 #1 (作者: MY82844, 时间: 5个月前)

Thanks for the tips! Could you share some detailed examples from a master-level perspective? That would be very helpful!

---

### 评论 #2 (作者: TP85668, 时间: 5个月前)

These are very practical tips for beginners. I’d add that using  **rank-based signals instead of raw values** , applying  **moderate decay** , and  **stress-testing turnover across nearby windows/decays**  can help ensure the reduction is structural rather than configuration-specific. In practice, the most robust turnover reduction comes from clear economic logic, not just additional constraints.

---

### 评论 #3 (作者: JC84638, 时间: 5个月前)

Yeah, sometimes these things are quite useful. (jzc

---

### 评论 #4 (作者: HD25387, 时间: 5个月前)

Great starter list. I’d also emphasize that turnover reduction works best when it’s embedded in the signal logic itself—using rank-based constructions, sensible decay, and slightly longer horizons—rather than relying only on hard constraints. That way, the lower turnover tends to be more stable across regimes.

---

### 评论 #5 (作者: ZK79798, 时间: 3个月前)

Helpful tips. Using hump and trade_when, enabling Max-Trade, extending lookback windows, and testing on larger universes are all effective ways to control turnover. Lower turnover not only reduces costs but also improves stability and scalability of alphas. Great practical guidance for beginners.

---

