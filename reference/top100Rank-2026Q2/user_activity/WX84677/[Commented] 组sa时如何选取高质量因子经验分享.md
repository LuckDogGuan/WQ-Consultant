# 组sa时如何选取高质量因子？经验分享

- **链接**: [Commented] 组sa时如何选取高质量因子经验分享.md
- **作者**: ZS59763
- **发布时间/热度**: 1年前, 得票: 119

## 帖子正文

如题，在顾问群中发现很多刚开始组sa的顾问，不清楚select的具体选择方式。本帖给出对应规则以及一些例子。

对于expert及以上顾问来说，筛选因子的第一步是用自己的因子，还是组别人的。这个可以通过own和not(own）进行筛选。

第二步，降低选到的因子是过拟合的，或者混信号的概率，可以通过operator_count限制op数量，dataset_count限制数据集数量。

（第二点五步，如果想要选取特定category，特定color或者特定tag的因子，也可以进行筛选。研究小组中有大佬提出过利用color和tag对于因子进行分组，从而按组select的方式）

第三步，选低相关因子：从分散化角度来说,我们自然希望选出的因子相关性较低,这个可以从prod_correlation参数进行控制（selfcor也可以，但是这个是小于等于prod的，不够准确）

第四步，选老顾问/组合表现较好顾问的因子：平台提供了许多因子owner的相关数据参数，可以根据参数进行筛选，主要包括成为顾问的时长，顾问地区，该顾问的sharpe，fit等等

第五步，按照表现选因子。出于防止过拟合和刻意筛选的角度，我们不能够直接选高sharpe，高fit的好（not for sure）因子，平台提供了几个字段帮助我们筛选因子，包括turnover，truncation，long和short count等等，按照每个字段的范围进行分组选因子可以大幅降低重复筛选的概率，从而降低相关性。

前边几步是筛选的过程，对于筛选的权重我们也可以进行调整。

例如：我们可以按照turnover的大小进行赋权，对于turnover较高的因子赋予更小的 权重（在select表达式后加上/turnover即可），此步需要根据个人需求进行修改。

总结：

以上几步是我在筛选中的思考流程，更为详细具体的可以参考 [Selection Expression | WorldQuant BRAIN](https://platform.worldquantbrain.com/learn/documentation/superalpha/selection-expression) ，针对因子选择的流程需要发挥主观能动性，多想多试，才能选出最适合的因子。以下几个案例是我在研究小组发过的select表达式总结，可以基于这三类，对于参数与权重进行调整，从而实现更好的组合。在自动化跑sa的时候，也可以按照不同的“模块”进行组装（但要注意条件不能太苛刻，至少得选出10个因子才能开始跑。）

(own&& ( (turnover>0.03&&turnover<0.05)||(turnover<0.13&&turnover>0.1)||(turnover<0.17&&turnover>0.15) || ((turnover>0.17&&turnover<0.20)))&&(operator_count<18)&&prod_correlation<0.7)/(sigmoid(turnover)*sigmoid(prod_correlation)*log(long_count))

(
not(own)&& 
((turnover<0.12&&turnover>0.09)||(turnover<0.15&&turnover>0.13)||(turnover<0.19&&turnover>0.16))
&&(operator_count<8)
&&(prod_correlation<0.4&&prod_correlation>0.0)
&&(dataset_count<=2)
) 
/(turnover*tanh(turnover)*sigmoid(self_correlation)*sigmoid(prod_correlation)*abs(long_count-short_count))

(own&&(turnover<0.07||(turnover<0.25&&turnover>0.2)))/(sigmoid(turnover)*sigmoid(prod_correlation))

---

## 讨论与评论 (24)

### 评论 #1 (作者: YB15978, 时间: 1年前)

感谢贴主这么好的文章，对应我这样准备进入sa的新手来说，帮助太大了，请问这些选择操作符号如owner not之类可以在哪里查询呢，对于新手都不知道可以用那些关键字和操作符，不知道如果下手哦

---

### 评论 #2 (作者: BL59663, 时间: 1年前)

游戏王不是浪得虚名的

---

### 评论 #3 (作者: WX84677, 时间: 1年前)

感谢游戏王哥的分享，期待下一篇~

---

### 评论 #4 (作者: ZZ44620, 时间: 1年前)

又来看一遍，谢谢游戏王哥，我刚才想法是设定几个strict cond和mild cond然后胡乱匹配，这个strict cond就是比较严格筛选条件，一个expr组多了就会选不到那种，mild就是可以组多点，准备实现一下

---

### 评论 #5 (作者: YB15978, 时间: 1年前)

感谢游戏王，正是需要的时候，例如这样的例子

not(own)&& 

((turnover<0.12&&turnover>0.09)||(turnover<0.15&&turnover>0.13)||(turnover<0.19&&turnover>0.16))

&&(operator_count<8)

&&(prod_correlation<0.4&&prod_correlation>0.0)

&&(dataset_count<=2)

) 

选出了turnover在某一范围的，是否还有办法选出更离散的呢

---

### 评论 #6 (作者: KZ55390, 时间: 1年前)

回复  [YB15978](/hc/en-us/profiles/28855468991639-YB15978) ：

在平台 Learn - Documentation 里右下角有 SuperAlpha 的版块

其中 “SuperAlpha Operators” 有支持的操作符列表（ [https://platform.worldquantbrain.com/learn/documentation/superalpha/appendix-operators](https://platform.worldquantbrain.com/learn/documentation/superalpha/appendix-operators)  ）

“Getting Started with non-Self SuperAlphas” 有提到 “own” 操作符的信息（ [https://platform.worldquantbrain.com/learn/documentation/superalpha/getting-started-non-self-superalphas](https://platform.worldquantbrain.com/learn/documentation/superalpha/getting-started-non-self-superalphas)  ）

“Selection Expression” 有筛选可用数据字段的列表，其中包括 alpha owner 的相关 datafields（ [https://platform.worldquantbrain.com/learn/documentation/superalpha/selection-expression](https://platform.worldquantbrain.com/learn/documentation/superalpha/selection-expression)  ）

---

### 评论 #7 (作者: ZS59763, 时间: 1年前)

可以在learn里面对应文档查询。

---

### 评论 #8 (作者: BJ10003, 时间: 1年前)

现在参与SAC的过程中，收集到了许多模板，共享出来大家一起学习

'(in(classifications, "POWER_POOL") && signed_power(turnover,1)&&long_count/universe_size(universe)<0.25 && short_count/universe_size(universe)<0.25 && not(own)) && (category == "NONE")',

#这一个是选择自己所在组的且优先不是自己的alpha，然后运用long_count去除部分厂型alpha，signed用于降低pro

'(in(classifications, "POWER_POOL")&& signed_power(turnover,1)&&long_count/universe_size(universe)<0.25 && short_count/universe_size(universe)<0.25 && not(own)) && (color == "GREEN")',

---

### 评论 #9 (作者: PB36509, 时间: 1年前)

感谢分享，总结得很好，新手很有启发！一直有个疑惑：如果已经有turnover，truncation，long和short count等指标的严格筛选，not own还有意义吗？

---

### 评论 #10 (作者: ZS59763, 时间: 11个月前)

[PB36509](/hc/en-us/profiles/29029620176023-PB36509)

sorry for late reply，这个条件主要是支持expert及以上顾问拿他人ra组sa用的。理论上来说，几十万个因子池选到自己的并不容易，这边的初心是与用自己ra组sa的own条件对应。

---

### 评论 #11 (作者: XW38100, 时间: 10个月前)

thank  you

---

### 评论 #12 (作者: LX71036, 时间: 10个月前)

感谢游戏王哥，刚看完有关sa的入门课，逛论坛发现游戏王哥的贴子，感觉你的贴子内容对我这种萌新是更加友好，大体上也理解了select的一个作用，就是turnover较高的因子赋予更小的权重，这里不太懂要怎么去理解，是换手率太高就是不太稳定，所以要给到一个更小的权重嘛？

---

### 评论 #13 (作者: HW54322, 时间: 10个月前)

superAlpha，能看懂的第1篇，点赞

---

### 评论 #14 (作者: JT77454, 时间: 9个月前)

感谢游戏王哥的分享，启发很多

---

### 评论 #15 (作者: YS42224, 时间: 9个月前)

感谢分享，非常有帮助

---

### 评论 #16 (作者: LR93609, 时间: 8个月前)

感谢分享，满满干货，学到了。

1. 选取not own的流程；

2. 高质量因子特征；

3. 高质量顾问特征。

-----------------------------------------------------------------------
  凡是发生，皆利于我；愿我所愿，尽是美好
  没有顺风，没有坦途，不去经历，无法到达
-----------------------------------------------------------------------

---

### 评论 #17 (作者: KJ35210, 时间: 8个月前)

感谢博主的分享，步骤很清晰，同时也为我指明了SA操作符的链接，正在研究如何组SA，期待自己的第一个三五，祝好，感谢

---

### 评论 #18 (作者: YQ84572, 时间: 6个月前)

这篇SA选因子指南太实用了！我按步骤优化筛选：先用 `own && operator_count<10` 控复杂度，再用 `prod_correlation<0.5` 和 `author_fitness>2` 提质量。关键是把turnover分段，比如 `(turnover>0.1 && turnover<0.15)` ，避免过拟合。感谢游戏王的分享

---

### 评论 #19 (作者: WX84677, 时间: 6个月前)

我之前 VF 一直不搞，对 SuperAlpha 提不起太大兴趣。最近 VF 更新，小有起色，因此开始研究如何组 SA。

群里对游戏王的帖子推崇备至，今日一看，果然名不虚传，牛！

感谢游戏王大佬的分享，祝大佬 VF 一直 0.9+

============================ 积跬步，至千里 ===========================

---

### 评论 #20 (作者: CW49566, 时间: 5个月前)

学习到了，感谢游戏王分享。

---

### 评论 #21 (作者: YN79403, 时间: 5个月前)

感谢分享，刚刚组了一个SA，pc0.55  sc0.44，效果看着还不错，希望能多分享

---

### 评论 #22 (作者: MZ45384, 时间: 5个月前)

终于有了not own权限和资源，这几天赶紧把游戏王大佬的帖子回来看看，开始手搓（受挫， 如下图）：

not(own)

&&in(classifications, "ATOM")

&&(universe!='ILLIQUID_MINVOL1M')

&&((neutralization == 'SLOW') || (neutralization == 'FAST') || (neutralization == 'SLOW_AND_FAST') || (neutralization == 'CROWDING') || (neutralization == 'STATISTICAL') || (neutralization == 'REVERSION_AND_MOMENTUM'))

&&(in(datacategories, "fundamental")||in(datacategories, "analyst")||in(datacategories, "news")||in(datacategories, "other")||in(datacategories, "risk")||in(datacategories, "pv"))

&&(turnover<0.1&&turnover>0.05)

&&(long_count>1000&&long_count<1200)

&&(prod_correlation<0.6&&prod_correlation>0.3)

&&(self_correlation<0.5&&self_correlation>0.05)

&&(operator_count<=8)&&(operator_count>=3)&&(datafield_count<=2)

&&(decay<=5)&&(truncation<=0.1)

/(sigmoid(turnover)*sigmoid(prod_correlation)*log(long_count))

路漫漫其修远兮，吾将上下而求索。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.
======================================================================================

---

### 评论 #23 (作者: JM34387, 时间: 5个月前)

感谢楼主游戏王的分享，这可谓是刚升级expert的一份大礼。

---

### 评论 #24 (作者: FF65210, 时间: 16天前)

组SA选因子的三步法很清晰：指标筛选、颜色分组、低相关选择。prod_correlation控制相关性这块确实是关键，我之前组SA时忽略了这个，结果几个高相关因子一起回撤。按颜色和标签分组这个技巧也很实用。

---

