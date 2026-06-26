# Understanding ts_min_diff and ts_max_diff

- **链接**: [Commented] Understanding ts_min_diff and ts_max_diff.md
- **作者**: MK58212
- **发布时间/热度**: 5个月前, 得票: 12

## 帖子正文

I’ve been using  **`ts_min_diff`**  and  **`ts_max_diff`**  a lot lately, and they’re surprisingly intuitive.

- **`ts_min_diff(x, n)`**  tells you how far the current value is from its recent  *low* . When this is small, the series is sitting near its downside extreme — useful for spotting potential rebounds.
- **`ts_max_diff(x, n)`**  shows how far the current value is from its recent  *high* . A small value here means the series is holding near highs, often a sign of strength.

I like these because they focus on  **extremes rather than averages** , which makes them feel more “real” in noisy markets. Simple operators, but very effective when combined with ranking or volatility filters.

---

## 讨论与评论 (7)

### 评论 #1 (作者: SK52405, 时间: 5个月前)

useful

---

### 评论 #2 (作者: KU30147, 时间: 5个月前)

ts_min_diff and ts_max_diff anchor signals to recent extremes, not averages. They capture proximity to lows or highs, making them robust in noisy markets. Near-lows hint at rebound potential; near-highs signal strength. Simple, intuitive operators that shine when paired with ranking or volatility filters.

---

### 评论 #3 (作者: CS51388, 时间: 5个月前)

Am trying this out mostly with ranking thank you for it

---

### 评论 #4 (作者: HD25387, 时间: 5个月前)

Well put. These operators capture position relative to extremes, which often carries more information than mean-based signals. I’ve also found they work best when combined with ranking or volatility normalization to avoid noisy false signals.

---

### 评论 #5 (作者: KG79468, 时间: 5个月前)

Well said. These operators are powerful because they anchor signals to recent extremes rather than smoothing everything away. They feel especially useful for mean-reversion and strength-confirmation logic.

---

### 评论 #6 (作者: KS81133, 时间: 5个月前)

Refreshing info!

---

### 评论 #7 (作者: CS51388, 时间: 5个月前)

Nice observation — focusing on distance from recent extremes often cuts through noise better than mean-based signals. These operators feel especially useful when paired with ranking or simple filters.

---

