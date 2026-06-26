# 多图解析USA最新3x High Turnover Theme国区提交现况

- **链接**: 多图解析USA最新3x High Turnover Theme国区提交现况.md
- **作者**: RM49262
- **发布时间/热度**: 2个月前, 得票: 15

## 帖子正文

如果你还不知道目前USA地区3x theme的标准是什么，这里就先带你回顾一下：基础标准（必须符合）：换手率 > 20%High Turnover returns ratio > 0.75 OR Pnl realization < 20 (这两个都是针对3x theme的新检测，其中前者多重回测就能看见是否符合，后者需要单独回测才能看见结果)此外，还有四个子主题，每两周轮换一次(每个人顺序不同，具体参考小铃铛中通知的顺序)，在符合基础标准的前提下，需要在对应的时间内符合下述一个子主题的标准即可：RAM中性化高换手(Orthogonal HTVR Theme)：使用RAM作为中性化即可可投资性高换手(Investable HTVR Theme)：(Max Trade Sharpe > 2.0 且 Max Trade turnover > 20%)  或者  (Max Position Sharpe > 2.0 且 Max Position turnover > 20%)费后sharpe高换手(After Cost HTVR Theme) ：After cost Sharpe > 1.0 (新检测会自动计算)高流动性高换手(Liquid HTVR Theme) ：必须通过 Liquid High Turnover tests:(TOP200 Sharpe > 1) 以及 (TOP500 and TOP200 Sharpe ratio > 0.7)目前这个高换手主题已经进入了第三周，我在SA中进行了以下筛选(in(classifications,"HIGH_TURNOVER:AFTER_COST") ||in(classifications,"HIGH_TURNOVER:INVESTABLE") ||in(classifications,"HIGH_TURNOVER:ORTHOGONAL") ||in(classifications,"HIGH_TURNOVER:LIQUID"))&& in(classifications,"REGULAR")对目前国区已经提交的Theme RA进行了简单的分析，这里分享给大家。首先是难度，根据提交情况来看，截止0417，国区 D1一共提交了96个theme RA，其中：Liquid High Turnover (14)Investable High Turnover (22)Orthogonal High Turnover (40)After Cost High Turnover (65)注：同一个RA可能同时符合多个theme而在D0，theme RA的数量则更少，只有8个，其中：Liquid High Turnover (3)After Cost High Turnover (6)Investable High Turnover (7)上述提交数量大致反映了各个子主题的难度。因此，当轮到较难的主题时，可以适当考虑跳过，毕竟难度还是有的。而在使用的数据大类方面，D1 theme RA的主要构成是：Price Volume (38)Fundamental (25)Analyst (17)Risk (13)Model (11)Social Media (6)Sentiment (5)Earnings (4)Macro (4)Option (4)Other (4)Imbalance (2)Insiders (2)Institutions (2)Short Interest (2)News (1)注：同一个RA可能同时属于多个category/dataset数据集方面，D1 theme RA使用数量排名靠前的主要是以下数据集：pv1 (33)analyst69 (11)fundamental6 (11)socialmedia12 (6)fundamental17 (5)analyst10 (4)model77 (4)risk70 (4)analyst16 (3)analyst4 (3)earnings27 (3)other551 (3)analyst15 (2)analyst82 (2)analyst9 (2)fundamental23 (2)fundamental94 (2)imbalance5 (2)insiders3 (2)model109 (2)model165 (2)model230 (2)option23 (2)pv103 (2)pv47 (2)pv87 (2)risk60 (2)risk71 (2)risk72 (2)sentiment26 (2)sentiment27 (2)short_interest_pred (2)...针对那些使用较多的数据集，大家可以多探索探索。至于其余数据集，基本是大家八仙过海，各显神通。这些D1 theme RA的is 数据分布如下图：之前weijie老师也提到过，可以把个人换手率分成10组，来评估换手的提升是否稳定带来了return的提升，斜率高的话，最总体表现增益更好。这里我们借用类似的概念，来看一下国区theme RA的收益率随着换手提升的变化情况。总的来说，可以看到线性趋势，但斜率不是很高。因此，吃theme 的base固然爽，但也不要忘记注意return/margin的情况。后面再贴一下d0 RA 的相关数据供大家参考

---

## 讨论与评论 (5)

### 评论 #1 (作者: JR57542, 时间: 2个月前)

太可怕了这个主题，可以看得出比较高质量的数据集都是pv1analyst69fundamental6 ，这几个。楼主做的可视化展示确实不错，能直观的看到总体情况

---

### 评论 #2 (作者: XC66172, 时间: 2个月前)

使用SA来倒推哪个数据集容易出theme ra. 学到了~~==========================================FIGHTING LABUBU!==========================================

---

### 评论 #3 (作者: MY82844, 时间: 2个月前)

大佬做结合SA的功能做主题，太强了，思路打开in(classifications,"HIGH_TURNOVER:AFTER_COST") ||in(classifications,"HIGH_TURNOVER:INVESTABLE") ||in(classifications,"HIGH_TURNOVER:ORTHOGONAL") ||in(classifications,"HIGH_TURNOVER:LIQUID")==============================================================================Reflection + Pain = Progress==============================================================================

---

### 评论 #4 (作者: AK76468, 时间: 2个月前)

====================================================================================这个筛选方式真是学到了，以前还在想Theme应该怎么去筛选，原来是在Classification里筛选。官方文档好像确实没有针对性的说明，在大佬这里学到了。====================================================================================

---

### 评论 #5 (作者: MY82844, 时间: 1个月前)

在pv20, pv87跑出一些可以过test的，但是after cost sharpe很多是负数，怎么破?==============================================================================Reflection + Pain = Progress==============================================================================

---

