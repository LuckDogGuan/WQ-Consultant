# How to analyse the OS performance?

- **链接**: [Commented] How to analyse the OS performance.md
- **作者**: HN12949
- **发布时间/热度**: 6个月前, 得票: 4

## 帖子正文

Can someone  **explain** to me what are these **sharpe 60** to  **sharpe 500**  and OS/IS ratio in the submitted alphas. While selecting them in  **osmosis** competitions what  **criteria** should we set using these OS performance matrix??

![图片](images/img_90711f0bf5.png)

---

## 讨论与评论 (6)

### 评论 #1 (作者: ML46209, 时间: 6个月前)

Sharpe 60–500 help check time consistency in OS, not just peak performance. I usually look for all-positive windows with no sharp collapse, and an OS/IS ratio that isn’t too low to avoid overfitting when selecting alphas for Osmosis.

---

### 评论 #2 (作者: LB76673, 时间: 6个月前)

Can someone  **explain** to me what are these **sharpe 60** to  **sharpe 500**  and OS/IS ratio in the submitted alphas. While selecting them in  **osmosis** competitions what  **criteria** should we set using these OS performance matrix??

---

### 评论 #3 (作者: JN96079, 时间: 5个月前)

Looking at Sharpe over the 60–500 range is useful for assessing time consistency out of sample, not just headline peaks. I typically prefer signals that stay positive across all windows without sudden breakdowns, and I  ***pay close attention to the OS/IS ratio***  to avoid selecting overfit alphas when preparing for Osmosis.

^^JN

---

### 评论 #4 (作者: AG14039, 时间: 5个月前)

Sharpe 60–500 helps assess time consistency in OS rather than just peak performance. I typically look for uniformly positive windows without sharp collapses, along with an OS/IS ratio that isn’t too low, to reduce overfitting when selecting alphas for Osmosis.

---

### 评论 #5 (作者: DL51264, 时间: 5个月前)

Sharpe 60 to Sharpe 500 just show how your alpha behaves across different lookback horizons, from short to long term. You don’t want one Sharpe to stand out while others collapse. OS/IS ratio tells you how well performance carries out of sample. For Osmosis, I usually pick alphas with decent Sharpe consistency and OS/IS not too low, rather than chasing the highest single number.

---

### 评论 #6 (作者: HN12949, 时间: 4个月前)

@DL51264 thank you, that was helpful. I will do the same.

---

