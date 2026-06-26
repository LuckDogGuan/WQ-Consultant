# PPAC比赛score的疑问

- **链接**: [Commented] PPAC比赛score的疑问.md
- **作者**: QP72475
- **发布时间/热度**: 1年前, 得票: 50

## 帖子正文

我每次提交PPAC因子的时候查看的score都是增加的，但更新后IS是降下来了，导致排名也降下来了，大家遇到过这个问题吗？那提交PPAC因子的时候如果不看score，那怎么确保提交上去的因子是对比赛有正向作用的呢。大家平常在PPAC比赛中，是怎么选择因子提交的？

![图片](images/img_c53448467b.png)

---

## 讨论与评论 (2)

### 评论 #1 (作者: YX23928, 时间: 1年前)

分数是根据sharpe和fitness来判断的，提交的时候可以看看Performance Comparison，如果对自己的组合有增益，是可以提交的

---

### 评论 #2 (作者: LL87164, 时间: 1年前)

[https://support.worldquantbrain.com/hc/en-us/articles/30787348743447-Do-I-need-to-run-merged-performance-comparison-feature-before-submitting-an-Alpha-in-the-competition](https://support.worldquantbrain.com/hc/en-us/articles/30787348743447-Do-I-need-to-run-merged-performance-comparison-feature-before-submitting-an-Alpha-in-the-competition)

[https://support.worldquantbrain.com/hc/en-us/articles/30788092457623-What-is-the-scoring-criteria-for-Power-Pool-Alpha-Competition](https://support.worldquantbrain.com/hc/en-us/articles/30788092457623-What-is-the-scoring-criteria-for-Power-Pool-Alpha-Competition)

Score不是基于Merged PnL来计算的：“ *The scoring in the Power Pool competition is based on the Sharpe of a smart combination of your selected power pool eligible Alphas (based on returns and variability of the Alphas). Scoring is not based on merged performance.* ”

Summary: It is the sum of Before-cost Information Ratio(IR) and After-cost Information Ratio. Both metrics are normalized and adjusted for alpha count, across In-sample and Out-sample.

个人理解是：IS可以从回测结果看alpha表现的稳健和波动。OS靠感觉和信念。

---

