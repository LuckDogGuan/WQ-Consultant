# 【课代表📕】关于2阶段的改进，字段方向Alpha Template

- **链接**: [L2] 【课代表】关于2阶段的改进字段方向Alpha Template.md
- **作者**: XX42289
- **发布时间/热度**: 1年前, 得票: 112

## 帖子正文

在这里推荐大家可以加入更多新颖的bucket，这里以split为例

bucket(rank(split), range='0.1, 1, 0.1')

![图片](images/img_8e7a816b94.png)

“Stock split ratio” 就是 “股票分割比率”

我猜测不同分割比率的股票可能会有相似性，就需要去做组内的中性化。

这是我用这个group做出来的某个因子，三条线都非常稳健，大家可以尝试加入自己的二阶段！

![图片](images/img_5ac2dfe2ae.png)

![图片](images/img_40e246a71c.png)

![图片](images/img_e2ca443a77.png)

---

## 讨论与评论 (8)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

很有用的帖子，点赞。

按照这个思路推下去，感觉能造出更多的分组

---

### 评论 #2 (作者: YB15978, 时间: 1年前)

感谢分享，能问下有什么办法获取所有region和所有delay都存在的datafield吗

---

### 评论 #3 (作者: PZ64174, 时间: 1年前)

非常感谢课代表分享！在最近的二阶段回测中，加入了课代表的思路，把pv1数据集内的字段拿来做bucket(rank({pv1}), range='0.1, 1, 0.1')分组，其中country，currency，exchange，industry，market，sector，subindustry，这几个数据字段是不适用于这个分组用法的，其他的确实都有比较好的表现。再次感谢课代表的分享！

---

### 评论 #4 (作者: MY82844, 时间: 9个月前)

power pool alpha里面可以用bucket()吗？ 看到有一条 group fields: country, industry, subindustry, currency, market, sector, exchange

---

### 评论 #5 (作者: JQ70858, 时间: 8个月前)

每日学习，立即去实践，有结果来反馈。

感谢分享！

---

### 评论 #6 (作者: YM14905, 时间: 7个月前)

感谢分享，但关于您找出来的alpha我有点疑问，这里多空数量不是很均衡而且2023年的Sharpe是负数，且整体回撤较大以及换手率较低，这种alpha提交后能对VF和Combined performance有正向影响吗？我刚获得顾问权限，遇到了好几个这种alpha，不知道是否应该提交？感谢大佬解答

---

### 评论 #7 (作者: SC16582, 时间: 6个月前)

太棒了！

---

### 评论 #8 (作者: SC16582, 时间: 6个月前)

gemini分析后说这是一个巨大的风险隐患，split（拆股比例）在TOP3000股票里面在绝大多数时间里并没有发生拆股，对于多数数据点，split的值都是1.0或NaN,rank(split)的结果是多数都接近0.5或者均匀随机分布，并没有把股票按照任何有效的经济学逻辑分开，这是一个巨大的风险隐患。

---

