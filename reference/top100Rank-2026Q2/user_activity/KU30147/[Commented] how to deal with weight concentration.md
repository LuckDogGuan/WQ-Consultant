# how to deal with weight concentration.

- **链接**: [Commented] how to deal with weight concentration.md
- **作者**: ML44231
- **发布时间/热度**: 5个月前, 得票: 17

## 帖子正文

Weight concentration happens when a few extreme signals dominate portfolio weights.  `kth_element(x, d, k)`  handles this by selecting a  **robust extreme**  over lookback  *d* , which both  **caps weights**  and  **reduces turnover**  by avoiding frequent jumps from outliers.  `ts_backfill(a, d)`  is an alternative that  **reduces weight concentration**  by carrying forward sparse signals

---

## 讨论与评论 (7)

### 评论 #1 (作者: KU30147, 时间: 5个月前)

I was facing this problem.It will be very helpfull.

---

### 评论 #2 (作者: EN41519, 时间: 5个月前)

another one is group_backfill(group,d)

---

### 评论 #3 (作者: MY82844, 时间: 5个月前)

What is the main difference between these two? In the case k=1, they are the same?

---

### 评论 #4 (作者: ML44231, 时间: 5个月前)

kth element is more preferable where turnover is high since it lowers turover and reduces  weight concentration at the same time

---

### 评论 #5 (作者: GK78521, 时间: 5个月前)

very helpful. I have been facing the challenge

---

### 评论 #6 (作者: BC83045, 时间: 4个月前)

Great insights. If I may ask, what lookback period range should be used?

---

### 评论 #7 (作者: JN96079, 时间: 4个月前)

I had been struggling with this exact problem, so this information is very useful.

^^JN

---

