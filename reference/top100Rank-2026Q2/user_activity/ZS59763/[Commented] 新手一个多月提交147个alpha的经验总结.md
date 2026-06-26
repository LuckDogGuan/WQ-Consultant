# 新手一个多月提交147个alpha的经验总结

- **链接**: [Commented] 新手一个多月提交147个alpha的经验总结.md
- **作者**: RP76828
- **发布时间/热度**: 1年前, 得票: 14

## 帖子正文

本人python熟练，无金融背景知识，去年12月底拿到顾问权限，12月31日正式提交第一个顾问alpha。由于之前错过了顾问培训课程，刚拿到顾问权限时挺迷茫，不知道怎么入手，只能从自己擅长的工程着手，试着构建一套系统，第一步先确保每天能提交足够的alpha。截至今天提交了147个，但还是没能做到每天能挖出足够可提交的alpha，现在等待参加今年的顾问培训课程，提升技能。我把这一月多一点的操作经验跟大家分享下，错误的地方欢迎前辈指正。

首先是系统搭建：

1、我把所有区的dataset都下载到本地，每个dataset一个文件，比如datasets/USA-1-TOP3000/analyst11

2、构建三个python进程，分别对应一阶，二阶，三阶，一阶提交的alpha全部以step1_开头，二阶以step2_开头，三阶以step3_开头。

一阶代码的实现是随机从任意dataset中取任意几个field，最多10个，最少2个，再随机从+，-，*，/中取operator，构建alpha，比如可以是两个field，一个operator，例子是field1 / field2，也可以是七个field，六个operator，例子是field1 - field2 + field3 +field4 +field5 +field6 +field7。

二阶代码的实现是定时轮询，取当前名字为step1_开头的，sharp大于1.2，fitness大于0.5的alpha，并存储到redis中，以防止下次轮询重复获取。

三阶代码的实现是定时轮询，取当前名字为step2_开头的，sharp大于1.4，fitness大于0.7的alpha，并存储到redis中，以防止下次轮询重复获取。

1月份前七天还比较顺利，这套系统每天能提交4个alpha，当时也还没有super alpha权限，算是满额提交。结果1月8日突然只能用部分field和operator，有些措手不及，因为忙，也没时间改造代码，差不多七八天没法提交一个alpha。

后来代码改造成适配部分field和operator，每天可提交的alpha有时候2个，有时候只有1个，甚至没有，这段时间我就找那些check submission只有一个FAIL的alpha，想手动把它改成可提交的alpha。

重点是处理IS_LADDER_SHARPE这个错误，我第一步是调时间，比如ts_mean(a, 240)，我会试着把240改成120，或者66，20， 10或者5。如果还不行，就参考community里搜到的一篇文章讲到的，把a改成a/(1.7-a)，或者改成a*(1+a)，我记得还改过一个，把a改成a*(1+a)*(2+a)*(3+a)后，变成能提交了，也试过把a改成log(rank(a*(1+a)))后，变成能提交的。还有一两次差一点点，我改了setting里的 **TRUNCATION** ，变成能提交的，也尝试换分组方式，变成能提交的。如果 [IS ladder Sharpe](/hc/en-us/articles/6726865162903?_gl=1*qjnlik*_gcl_au*NzI5ODQ4MzEuMTczODM3MDQyMQ..*_ga*MTczODM3MDQxODMxMWU5YTY1NjczZDEwZA..*_ga_9RN6WVT1K1*MTczOTE5OTE3MS43Mi4xLjE3MzkxOTkyNjMuNjAuMC4w)  等于或者小于零，我就直接放弃，因为之前调过几次，不管怎么调，也过不了。CONCENTRATED_WEIGHT错误，目前我只会调decay，增加decay，通过了几个，CONCENTRATED_WEIGHT超过50，我就放弃调，也是因为之前怎么调，也调不过。

还有一个意外发现是三阶脚本执行后，挑选出一些觉得接近提交的，把step3_改成step1_前缀的名字，重新送给二阶三阶脚本执行，反复嵌套，结果会产生不少可提交的alpha。比如最近提交的一个alpha的模版是group_neutralize(trade_when(ts_corr(close, volume, 20) < 0, -ts_target_tvr_hump(trade_when(group_rank(ts_std_dev(returns,60), sector) > 0.7, a, 22), abs(returns) > 0.1),lambda_min=0, lambda_max=1, target_tvr=0.1), abs(returns) > 0.1),densify(bucket(rank(close*volume),range = '0.1, 1, 0.1’)))，类似这种三阶之后又嵌套二阶的。

目前最大的问题是，虽然提交了147个alpha，30个pyramid，但是combined Alpha Performance是-0.78。我自己可能是犯了如下错误：

1、为了过 [IS ladder Sharpe](/hc/en-us/articles/6726865162903?_gl=1*qjnlik*_gcl_au*NzI5ODQ4MzEuMTczODM3MDQyMQ..*_ga*MTczODM3MDQxODMxMWU5YTY1NjczZDEwZA..*_ga_9RN6WVT1K1*MTczOTE5OTE3MS43Mi4xLjE3MzkxOTkyNjMuNjAuMC4w)  ，我有几个提交的alpha把时间从120改成类似113这种没有意义的数字

2、提交了大量相关性强的alpha，基本上一个alpha通过后，这个alpha再通过二阶，三阶脚本反复执行，能产生五六个可以提交的alpha，我基本都提交了。

---

## 讨论与评论 (14)

### 评论 #1 (作者: LS51569, 时间: 1年前)

随机挑选alpha做加减乘除操作不合适吧，这种alpha可能不具备经济学意义，提交了效果也很差🤔

---

### 评论 #2 (作者: ZS59763, 时间: 1年前)

有个小问题需要注意一下， op用的太多了，在genius那边，单个alpha平均op可能不占优势

---

### 评论 #3 (作者: RX97746, 时间: 1年前)

是的，其实二阶group operator连续嵌套也会出现可以提交的，但不知道对combined Alpha Performance影响如何

---

### 评论 #4 (作者: CP28898, 时间: 1年前)

我很早之前combined 2.x时候，很少调参数  最近参数调多了，os确实会下降。

---

### 评论 #5 (作者: MG88592, 时间: 1年前)

如果一直交一些质量不高的因子 那payment好像会很低，请问楼主目前basepay是多少，valuefactor是多少。

---

### 评论 #6 (作者: RP76828, 时间: 1年前)

就我提交的alpha，大部分就是反复嵌套的，比例至少占全部提交的50%以上，有一些在没有嵌套时有

**PROD** _CORRELATION是0.8以上的，结果反复嵌套过一天后，这个alpha变成可提交的了，更多情况是没有嵌套前会有一两个fail，反复嵌套后就可以通过了。有一些反复嵌套后，sharpe，fitness，turnover和margin这些指标也提升了，所以我不清楚什么情况会是overfitting。

一个alpha很多ops和fields，不清楚有什么副作用，但确实可以快速覆盖更多的pyramid，有一次找到一个覆盖6个category的alpha，再加上反复二阶三阶嵌套，产生了三个可提交的alpha，这三个alpha就覆盖了6个pyramid。

因为我12月31日才提交alpha，我现在的base payment和value factor是初始值，没有更新的。Q1的提交情况得到Q2才能看到影响吧？

---

### 评论 #7 (作者: XX42289, 时间: 1年前)

1. **过度调整参数** ：为了通过IS_LADDER_SHARPE检查，作者将时间参数调整为无意义的数值（如113），这可能降低了alpha的实际有效性。
2. **提交相关性强的alpha** ：作者通过嵌套筛选策略生成了大量相关性强的alpha，导致组合多样性不足，影响了整体表现。

作者这两个错误还是萌新阶段经常遇到的，为了交因子而交因子，导致交了很多过拟合的因子。

套一二三阶段反复套，这个我在新手时期就是这么干的，然后prod corr就降低了，我成功交了因子。但是我也知道这不对。因为这么干可能以后就是1美元了，就不能高value factor了。所以还是不能这样做，还是要多交1，2阶段的因子

---

### 评论 #8 (作者: RP76828, 时间: 1年前)

一二阶就能提交的alpha，对于新手来说，是不是比较难找到，这一个多月来能在一二阶找到的alpha很少，还得多跟前辈请教经验才行。

---

### 评论 #9 (作者: JB71859, 时间: 1年前)

你虽然提交了很多但这样搞质量太低了，和group套group是一样的，VF会爆炸的

---

### 评论 #10 (作者: DZ31817, 时间: 1年前)

我的理解是，如果一个alpha通过微调一下参数就能从不可提交变成可提交，说明这个alpha鲁棒性不强，可能不是一个好alpha。

同理，之前老师有说过建议对alpha进行鲁棒性测试，找到可提交的alpha后，遍历微调下参数，如果结果变化很大，说明alpha不健壮，不建议提交。

---

### 评论 #11 (作者: ZX52486, 时间: 1年前)

非常感谢XX42289的分享经验，作为新手应该尽可能保持alph的质量，同时保证数量，尽可能保证alpha的经济学意义，交之前应该应该多做健壮性测试，以保证os表现和vf

---

### 评论 #12 (作者: ZR63005, 时间: 1年前)

[RP76828](/hc/en-us/profiles/26661185670551-RP76828) 
您好，感谢您的分享！因为我其实也有这类想法，希望写一串代码挂着24小时不停跑，因此想要询问一下，您通过这样的方式挖掘alpha，alpha的平均sharpe与fitness能达到多少呢？以及您目前的vf是多少呢？如果您愿意回答，我会非常感激！

---

### 评论 #13 (作者: RP76828, 时间: 1年前)

我没有计算alpha的平均sharpe，fitness，其实我当时发完这个帖子，因为工作也忙，就基本放弃了，靠着之前提交的alpha，每天自动提交一个super alpha，regular alpha有就提交，没有就不提交，有很长一段时间基本没交，直到ppac降低了难度，才持续每天4个满额提交下去。我vf很低，从0.5-0.2-0.3-0.4，目前是0.4，意外的是我的combined都可以，都过了2。

---

### 评论 #14 (作者: YY27006, 时间: 1个月前)

感谢分享，受益匪浅

---

