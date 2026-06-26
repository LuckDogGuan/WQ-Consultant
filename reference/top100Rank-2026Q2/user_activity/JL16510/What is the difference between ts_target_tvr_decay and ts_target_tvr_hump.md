# What is the difference between ts_target_tvr_decay and ts_target_tvr_hump?

- **链接**: What is the difference between ts_target_tvr_decay and ts_target_tvr_hump.md
- **作者**: JL16510
- **发布时间/热度**: 9个月前, 得票: 37

## 帖子正文

Hi,everyone.I notice that everything is same in the description of ts_target_tvr_decay and ts_target_tvr_hump, except for the names after tune being different. It indicates that the usage of the two operators is quite similar, but there should still have some differences. I want to know what the subtle differences are.Thank you.

---

## 讨论与评论 (1)

### 评论 #1 (作者: RK65765, 时间: 8个月前)

I think the main difference is in how they shape the turnover path. Withts_target_tvr_decay, turnover tapers off smoothly over time, whilets_target_tvr_humpfollows more of a bell-shaped curve where turnover builds up, peaks, and then falls. Both help control trading costs, but decay is more gradual, and hump is more concentrated in the middle.

---

