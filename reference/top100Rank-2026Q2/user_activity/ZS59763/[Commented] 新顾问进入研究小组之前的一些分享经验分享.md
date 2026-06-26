# 新顾问进入研究小组之前的一些分享经验分享

- **链接**: [Commented] 新顾问进入研究小组之前的一些分享经验分享.md
- **作者**: YL92635
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

新顾问进入研究小组之前的一些分享

最开始有个很牛的顾问分享，说这个量化就像玩游戏，还是挺感同身受的，打怪升级，每晋升一级，就会有更多的装备（数据集，操作符，并行度，顾问交流，激励，等级等），每次想要放弃的时候，没有思路的时候，就因为自己稍微再往前走了一步，WQ顾问团也在适当的时候进行培训来协助你进入下一阶段，有种团队作战的感觉！

接下来自己简单回顾了这次alpha之旅，希望对还未进入研究小组的顾问有所帮助哈！也欢迎有经验的顾问大牛提宝贵建议哈！

关键时间节点：

1月2日 自学以前的课程链接，开始提交用户alpha

1月8日 每天提交1-2个达到1万分，提交上传问卷

1月13日-23日参加《零基础学量化》，

1月26日顾问申请表被退回需要修改（户口地址错写成了户籍），

2月27日获得条件顾问，

3月1日参加第一次线下顾问培训

3月5日提交第一个顾问alpha，

3月30日 日均回测1万左右，已提交 30个 Signals（最后5天需连续提交），覆盖8个 Pyramids

3月31日  邀请加入量化研究小组，一起探索更多的可能！

经验分享：

1、笨鸟先飞：可以提前自主学习之前学员分享的视频课程，不一定非得等线上相关培训，因为培训过程中发现参加的人多了，提交问卷的标准也水涨船高，因为我先人一步，之后的进度相对能快些；

2、三阶段模版：三阶段模版对于提交顾问alpha还是有挺大帮助的，提交的顾问alpha基本都来自该模版，要清楚该模版原理并进行简单的改造

3、region选择：看论坛有人分享简单程度：ASI > USA > TWN > EUR > GLB > JPN = CHN = HKG > KOR > AMR （都是delay 1的），所以刚开始选择的ASI，结果时运不济，没挖出可提交的alpha，估计ASI挖的差不多了，TWN感觉region有点小，就尝试了EUR，结果EUR挖掘出了不少alpha，于是就主攻EUR；所以他人的分享可参考，但需要注意这些经验的时效性，过一段时间很可能就不适用了；就像dataset里的 news 类型的，对股价影响就非常有时效性；

4、提前关注Genius各项指标：刚开始以为20个signals 就可以GOLD升级为 EXPERT，季度奖就可以从100-200USD 升级到 200-2000USD了，结果还需Pyramids满足10个，于是转战其他category、region，快达到的时候，可能需要挑灯夜战了，还好找有经验的顾问事先咨询确认了下，发现即便Pyramids 满足10个，由于combined 没有更新，所以只靠3月份是无法升级到EXPERT，只能下个季度继续努力啦。

5、避免check限流：check的时候，如果有大量的自相关度很高的alpha，check会进入限流，变慢，大概10分钟才一个，如果要提升回测效率，这个点确实需要优化下。

工程上的一些优化：

1、记录回测过的field：

Get alpha之后，random之后，记得持久化一份，如果第一个批次回测发现这个dataset存在 potential（生产相关性<0.75） 或者 successful alpha，可进行第二个批次，避免重复回测相同的field

2、get_alphas的时间细化到分钟级别：

培训教学的模版只到天级别，如果一天跑多个批次，不好筛选对应批次的alpha进入下一阶段，所以需要继续记录上一阶段回测的开始时间和结束时间，作为下一阶段的alpha的查询条件；

3、添加margin过滤：

自己只加了 margin 大于 0.0004，优先保证alpha数量，所以设置的低了些

参考如下即可： [https://support.worldquantbrain.com/hc/en-us/articles/4672184130455-How-can-you-earn-more-Base-payment ，同时关注提交因子的performance](/hc/en-us/articles/4672184130455-How-can-you-earn-more-Base-payment%C2%A0%EF%BC%8C%E5%90%8C%E6%97%B6%E5%85%B3%E6%B3%A8%E6%8F%90%E4%BA%A4%E5%9B%A0%E5%AD%90%E7%9A%84performance)  comparison，Sharpe和fitness可以提高你pool的表现，turnover和drawdown要降低，margin和return要提高。

4、动态添加批量回测的任务：

Configs.csv 文件内容如下：

dataset_id,prefix,universe,region,neutralization,first_phrase_max,first_multi_simu,second_multi_simu,third_multi_simu,status,status_start,status_end,first_phrase_start

model32,mdl32,MINVOL1M,ASI,SUBINDUSTRY,1000,10,10,10,check-finished,2025-03-22T21:11:59-05:00,2025-03-23T00:21:06-05:00,

news50,nws50,TOP2500,EUR,SUBINDUSTRY,2329,10,10,10,finished,,,1000

fundamental28,fnd28,MINVOL1M,ASI,SUBINDUSTRY,3000,10,10,10,ready,,,4000

将回测过程中的一些关键变量提取出来，便于动态添加回测任务；

first_phrase_max：第一阶段回测的数量

first_multi_simu,第一阶段的并行度

second_multi_simu,第二阶段的并行度

third_multi_simu,第三阶段的并行度

status,任务状态 ready/finished/check 等

status_start, 需要check的alpha的开始时间

status_end, 需要check的alpha的结束时间，可以对任意阶段的alpha进行回测；

first_phrase_start，刚开始生成的alpha random之后，持久化为数组，当多次回测的时候，方便从数组指定位置开始回测，比如 有23万个，刚开始跑1000个，觉得不错，就可以继续跑2000个等；

目前的困惑：

目前还没有达到alpha自由的阶段，提交的alpha质量也不是很高，再接再励吧！

---

## 讨论与评论 (1)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

针对批次的问题，我的建议是可以增加每一批的数目，使得至少要跑1天，然后用天来区分就可以了。其实还有其他方法，你提到的按照时间论坛里面有人写过代码，或者可以按照颜色，一阶二阶分别打个颜色，筛选

---

