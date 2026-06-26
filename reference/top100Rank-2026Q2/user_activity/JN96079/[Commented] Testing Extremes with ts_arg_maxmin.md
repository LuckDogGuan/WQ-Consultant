# Testing Extremes with ts_arg_max/min

- **链接**: [Commented] Testing Extremes with ts_arg_maxmin.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 38

## 帖子正文

Using ts_arg_max or ts_arg_min shows how recent an extreme occurred, which sometimes matters more than the value itself. In cyclical stocks, it gave me stability boosts.
👉 Have you applied arg_max/min for timing signals, or do you treat them as secondary operators?

---

## 讨论与评论 (4)

### 评论 #1 (作者: TP85668, 时间: 8个月前)

Great point! Using  `ts_arg_max/min`  to measure  *recency of extremes*  is often overlooked but can add strong timing value, especially in cyclical or mean-reverting stocks. I’ve seen it work well when combined with  `ts_decay`  or  `ts_rank`  to smooth out noise. Personally, I treat it as a  **primary operator for timing** , but only after neutralization checks — otherwise, it can amplify sector or market-wide swings. Curious to hear how others integrate it into their alpha design.

---

### 评论 #2 (作者: AG14039, 时间: 6个月前)

Using ts_arg_max/min to capture how recently extremes occurred is an underrated technique that can add meaningful timing value, particularly in cyclical or mean-reverting names. I’ve found it performs even better when paired with ts_decay or ts_rank to control noise. I usually treat it as a timing-focused operator, but only after checking neutralization, since without that step it can unintentionally magnify sector or market-wide moves. I’d be interested to hear how others incorporate it into their alpha construction.

---

### 评论 #3 (作者: SP39437, 时间: 5个月前)

Using ts_arg_max / ts_arg_min to capture the  *recency*  of extreme values is an often underappreciated technique, yet it can add significant timing power when applied correctly. Rather than focusing on the magnitude of a move, these operators highlight  *when*  an extreme last occurred, which is especially useful in cyclical or mean-reverting stocks where timing matters more than direction alone. In my experience, their effectiveness improves notably when combined with stabilizing operators such as ts_decay or ts_rank, which help smooth noise and reduce sensitivity to short-lived spikes. I typically view ts_arg_max/min as a timing-centric building block rather than a standalone signal. Importantly, I only rely on it after running neutralization checks, since without proper controls it can unintentionally amplify broad market or sector-wide swings. When used thoughtfully, it becomes a powerful way to capture regime shifts without excessive turnover.

How do you balance the timing strength of ts_arg_max/min with the risk of amplifying common factor exposures?

---

### 评论 #4 (作者: JN96079, 时间: 5个月前)

Leveraging  **ts_arg_max/min**  to measure how recently a peak or trough occurred is an often overlooked way to add timing information, especially for cyclical or mean-reverting stocks. I’ve seen it work best when combined with  **ts_decay**  or  **ts_rank** , which helps suppress noise and stabilize the signal. I generally use it as a timing-oriented component, but only after applying neutralization—otherwise it can unintentionally amplify sector or market-level effects. I’d be curious to hear how others are using this operator in their own alpha designs.

^^JN

---

