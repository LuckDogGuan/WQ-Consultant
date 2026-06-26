# How to reach 10,000 points-Tips for new consultants

- **链接**: [Commented] How to reach 10000 points-Tips for new consultants.md
- **作者**: Emma Kagendo(EK97682)
- **发布时间/热度**: 8个月前, 得票: 2

## 帖子正文

Hello everyone,  
I wanted to share a few things that helped me hit the 10,000-point mark as a consultant on BRAIN — in case it helps anyone still getting started.

✅ Start Simple: Use popular datasets like pv1, model26, and risk70. These have good coverage and lots of alphas built from them.

✅ Play With Operators: Try rank, ts_rank, zscore, and ts_decay_linear. They work well when layered properly.

✅ Boost Your Signal: Once your

signal is stable, add a second dataset or neutralize to sector/industry using vector_neut.

✅ Backfill Where Needed: If you're getting low coverage, ts_backfill and days_from_last_change can help.

✅ Track Performance: Use the "My Alphas" tab daily to learn what’s working. Reuse successful patterns.

---

## 讨论与评论 (3)

### 评论 #1 (作者: Emma Kagendo(EK97682), 时间: 8个月前)

If you have more suggestions feel free to drop your thoughts

---

### 评论 #2 (作者: ME83843, 时间: 8个月前)

Excellent summary. Combining rank-based transformations with  `ts_decay_linear`  has improved my stability as well. I’d add that testing different decay windows can really fine-tune results.

---

### 评论 #3 (作者: Emma Kagendo(EK97682), 时间: 8个月前)

Exactly,you can share more ideas

---

