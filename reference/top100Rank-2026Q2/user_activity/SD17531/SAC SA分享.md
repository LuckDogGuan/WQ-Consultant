# SAC SA分享

- **链接**: SAC SA分享.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 28

## 帖子正文

曾经因为太懒,导致前几周完全没有参加SAC,现在才知道落后了群友一大截.今天开始交SA,希望能够看到群友的尾气.我是G2组,现在是HCAC主题,今天交的因子是参考游戏王大佬的分层写出来的SA.selection:(in(competitions, "HCAC2025")&&not(own)&&((turnover<0.03&&turnover>0.01)||(turnover<0.05&&turnover>0.04)||(turnover<0.12&&turnover>0.08))&&(operator_count<8)  &&(dataset_count<=2)&&(prod_correlation<0.5&&prod_correlation>0.1))/(turnover*s_log_1p(turnover)*sigmoid(self_correlation)*sigmoid(prod_correlation)*abs(long_count-short_count))combo:stats = generate_stats(alpha);std = ts_std_dev(stats.returns,60);std_crowd = std /ts_delay(std,60);ts_rank(-std_crowd ,500)GLB的SA,我感觉还过得去.

---

## 讨论与评论 (1)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

赞！生活就像海洋，只有意志坚强的人才能到达彼岸

---

