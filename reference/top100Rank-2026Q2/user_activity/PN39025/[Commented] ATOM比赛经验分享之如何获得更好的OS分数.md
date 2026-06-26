# ATOM比赛经验分享之如何获得更好的OS分数

- **链接**: [Commented] ATOM比赛经验分享之如何获得更好的OS分数.md
- **作者**: TL87739
- **发布时间/热度**: 1年前, 得票: 30

## 帖子正文

这次很荣幸在ATOM获得了全球总分第一名，其中我的IS分数是全球总分第二，OS分数是全球总分第一。在这里分享一些我获得高的OS分数的心得，也希望能帮助大家打接下来的比赛。即使不打比赛，这些经验对于平时提升value factor，或者merged os performance，也应当会有所帮助。

OS分数即组合的样本外表现，既取决于单个alpha的质量，也取决于alphas等权组合的整体效果。因此这篇文章也将从组合整体与单个alpha两个角度出发去阐释这个问题。

组合整体：

1. IS分数高的，OS分数也高。

如果把组合优化看成训练一个模型，那么IS分数可以说是样本内的拟合程度。如果一个模型本身欠拟合，我们只能期待他在样本外的表现与样本内波动小，但无法期待它样本外的表现能有多好。 **比赛的IS分数，本质上是在引导参赛者提交高sharpe，低turnover，高margin，低drawdown，以及最关键的，低self-correlation的alphas。** 这里的低self-correlation不仅仅指的是与组合里最高的alpha的self-correlation，而是跟组合里所有的alphas的self-correlation。

就个人经验而言，哪怕一个alpha它的max self-correlation并不高，可能0.38左右，但是组合里面有大量与之在0.2~0.3之间的self-correlation的alphas，那么这个alpha是很难加分的。

关于这其中的原理，可以参考 [ZL29184](/hc/en-us/profiles/22955594228503-ZL29184)  的文章：

[为什么要尽量交低相关的Alpha?Why similar alpha fails: intuition from Markowitz portfolio management theory – WorldQuant BRAIN]([Commented] 为什么要尽量交低相关的AlphaWhy similar alpha fails  intuition from Markowitz portfolio management theory.md)

![图片](images/img_a997aa7822.png)

把ATOM榜单按照IS降序排名，发现IS高分的多数OS也高分。

因此，如果想要提高OS分数但又不知从何入手，把IS分数往上打，是一个简单而又好用的思路。

2. alphas数量多的，OS表现好。

![图片](images/img_7a255bcc9a.png)

将ATOM比赛榜单按数量降序可以看出，提交数量多的人之中，绝大多数的OS都好于IS，尤其是IS分数在2w~4w分的段位上。

提交更多的，稳健的，相关性低的alphas，也就是更diverse的，对于一个好的OS是至关重要的，这也符合组合优化的基本原理。

个人九月份交的alphas少，所以最新一期的value factor从0.88骤减到0.13，也是这个观点的作证...

3. 优化组合

这个问题既是整体问题，也涉及到单个alpha该怎么提交的问题。总的来说，在提交单一alpha的时候，除了关注alpha本身的稳健性和pnl，我们还格外需要关注这个alpha放入组合之后对组合带来的变化。

展示一下ATOM在中后期的时候我截图的一个alpha，放入组合之后的表现：

![图片](images/img_cc8cf214b5.png)

这个alpha本身是一个不错的alpha，也可以加分，但是提交后会进一步降低组合在2020年的sharpe。我的组合本来在2020年的sharpe就比较低了，这意味着组合面对2020年的市场条件下，预测能力有所减弱。一个比较好的组合，我们是希望他在每一年的sharpe差异比较小的，也就意味着它在不同的年份，即不同的市场条件下，都有稳定的预测能力。因此这个alpha我并没有立刻提交，而是留了一段时间。

在比较后期我的组合pnl截图：

![图片](images/img_9fce91d071.png)

从单个alpha的角度：

1. 对于不同中性化设置稳健的alpha。

在各种研报和论文之中，作者往往会把自己实证的factor对各类风格因子进行中性化，目的就是检验这个factor不能被这些风格因子所解释部分的预测能力。如果一个alpha，切换中性化后效果大打折扣，那么很可能它的收益是暴露在这个分组之上的。这种alpha能给组合带来的信息增益是有限的。

2. pnl表现稳健的alpha

这个原理是类同于整体pnl的，也就是单个alpha我们希望它能在不同市场条件下都有稳定的预测能力。比起短期的回撤，我会更在乎出现一年及以上的平缓期或者回撤。尤其不希望在近一年decay。

好的pnl示例：

![图片](images/img_3a0c304384.png)

不好的pnl示例：

![图片](images/img_5bdd39865d.png)

上图2的alpha，从2016年一路回撤到了2018年夏天，这种长达2年的回撤是足以让人质疑这个alpha的稳健性的。

尽管pnl分析法会认为图1更稳定，但是取决于OS的时间段，图2alpha的OS表现不一定就弱于图1，或者说有些alpha就是风格暴露、行业暴露，但是正好暴露在了OS时间赚钱的风格/行业上，它OS就是容易好。

因此从打比赛的角度考虑，图二这样的alpha也不是不能交，但是需要建立在已经有大量稳健优质的alpha、图二的alpha要与组合有低的相关性，以及能够优化组合的一些指标，的前提之上。

3. 指标好看的alpha

![图片](images/img_c078747a62.png)

一般做alpha的时候，注意力往往会集中在sharpe和fitness上，但是margin同样也是十分重要的，这意味着这个alpha在扣除手续费之后到底能不能赚到钱。有一些比赛，会测试扣除手续费之后的os，那么组合里如果都是margin低的alphas，可想而知会有更低的分数。

---

## 讨论与评论 (5)

### 评论 #1 (作者: UG81605, 时间: 1年前)

Brilliant summary and congrats on winning the competition. From my limited findings, turnover is the key, less turnover leads to higher margins and vice versa. So in initial stages of competitions i try to submit higher turnover alphas and then go on finding lower turnover alphas. This strategy I follow as it doesn't penalizes me on the points/ IS scores.

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

感谢您的精彩分享，也许在接下来的比赛中我可以有更多的想法来实现，以加快我的成绩。恭喜你，收入逐渐减少是你的秘密

---

### 评论 #3 (作者: LN92324, 时间: 1年前)

First of all, congratulations on winning the contest. I attended a webinar and they said that turnover and margin are two important metrics for a good alpha. I was too focused on Sharpe and ignored the rest. Your sharing is really helpful and I will try it out.

---

### 评论 #4 (作者: CT68712, 时间: 1年前)

感谢您的精彩分享！文章内容非常详细且具有指导性，特别是关于低相关性 Alpha 和组合优化的部分让我印象深刻。我之前也遇到过类似的问题，比如如何平衡 Alpha 的数量和质量，避免过度拟合的同时提升 OS 表现。

想请教一下，您提到的一些指标（例如 self-correlation 和 margin）在实际筛选 Alpha 时，是否有具体的阈值或者标准？另外，对于像您提到的长期回撤的 Alpha，您是否会尝试通过参数调整或者重新中性化来优化呢？期待您的进一步分享！

---

### 评论 #5 (作者: TL87739, 时间: 1年前)

[CT68712](/hc/en-us/profiles/15219840701719-CT68712)

感谢你的回复。

关于您提及的阈值，首先self-correlation，这个是没有一个通用的标准的，你可以根据你自己的经验设定，但也可以根据具体情景灵活变通。我个人是控制在0.4以下，但如果组合里只存在一个高度相关，并且这个alpha远远好于该alpha时，也可以提交。

关于margin，这个在不同的region各不相同，据我了解比较通用的是控制在15以上。

关于您提到的优化alpha的问题，答案是：会。

---

