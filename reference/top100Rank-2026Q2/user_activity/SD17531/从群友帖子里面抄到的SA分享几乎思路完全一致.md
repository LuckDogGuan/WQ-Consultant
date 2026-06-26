# 从群友帖子里面抄到的SA分享,几乎思路完全一致

- **链接**: 从群友帖子里面抄到的SA分享几乎思路完全一致.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 25

## 帖子正文

SELECTION:bool = (not (own) &&in(competitions,"HCAC2025")&&# (neutralization == 'FAST')&&datacategory_count<=3 &&short_count+long_count > 2000 &&(( prod_correlation >0.4) || (prod_correlation <0.35 ||prod_correlation >0.25)||(prod_correlation <0.2) ));weight = (1*((long_count+ short_count)/ universe_size(universe))*if_else(prod_correlation > 0.7, 2, 1.5)*(1 - self_correlation));bool * weightCOMBO:stats = generate_stats(alpha);w1 = (1+ts_mean(stats.returns,20))/(1+ts_mean(stats.returns,252));W2 = ts_ir(stats.returns,63)/reduce_powersum(self_corr(stats.returns,252),constant=2);scale(w1)+ scale(w2)

---

## 讨论与评论 (0)

