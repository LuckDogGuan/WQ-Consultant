# Alpha打分方式-抛砖引玉

- **链接**: Alpha打分方式-抛砖引玉.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 26

## 帖子正文

请问各位友友, 对于一个Alpha, 你是怎么考量他的质量呢?一个常见的场景: robust test滞后可能会有几十上百个非常类似的因子可以提交,但是提交一个以后其他因子会因为相关性过不去.那么,大家是如何考量应该提交哪个因子呢?先说一下个人打分的见解,目前尚未运用到代码中.1.sharpe score = (sharpe - 1) *102.fitness score = (fitness- 1)*103.margin score  = (margin - threshold) *2, us,eur,asi,glb的threshold分别是7,10,15,15.4. return score = (return - drawdown) *35.risk neut +10, 多国家地区 neut market/country +76.maxTrade ON + 10感觉上最好是获取year status去进行挨个计算再相加会更好一点, 然后前8年的分值权重是1,2021,2022权重是3.2023目前暂不做计算.目前初步想法就是这样,不知道友友们有没有更科学的方式?

---

## 讨论与评论 (1)

### 评论 #1 (作者: XC66172, 时间: 1年前)

每个人对ALPHA的打分方式都不太一样。我的除了对于基本指标（sharpe,margin,return,fitness)给予一定权重，也会获取Performance Comparison里的数据（提交该因子后对指标是改善还是更不好），以及self-correlation，product-correlation (我一般是1/SC*系数）这样来算；最后再把它们都加总。你说的NEUT, MaxTrade ON加分也是很好的建议~~=================每天睡醒就搓搓因子，总有一个是好的==================

---

