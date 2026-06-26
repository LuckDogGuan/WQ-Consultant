# IND感想Alpha Template

- **链接**: [Commented] IND感想Alpha Template.md
- **作者**: ZX52486
- **发布时间/热度**: 7个月前, 得票: 37

## 帖子正文

1.通过线性回归拿到close与数据的残差，如果拟合得越好，则表明股价有可能在未来会下跌

data = ts_regression(ts_delta(close,1),ts_backfill(vec_avg(mdl138_qpdi3_sale_empl),66),200);

2.通过regression_proj剔除市值的影响，当市值相同时，看谁拟合更好，那么就做空，

re = data -regression_proj(data,rank(cap));

3.最后通过rank(-re)平滑权重，避免权重过于集中，当然也可以使用sigmoid(-re)

4可以延展到fnd和anl有实际意义的组合字段等

5：改进方向：能否在降低换手率的同时尽可能保持performance？

实战如下：

![图片](images/img_f1a9d0483f.png)

![图片](images/img_83ee91c1a8.png)

![图片](images/img_c970ba3aa0.png)

---

## 讨论与评论 (23)

### 评论 #1 (作者: CY96125, 时间: 7个月前)

这个模板和思路应该也能应用在其他region

---

### 评论 #2 (作者: MY82844, 时间: 7个月前)

感谢分享，感觉可能是universe比较小的缘故，performance和pc对参数变化还比较敏感

regression_proj说不定也开始试下risk factor loading

---

### 评论 #3 (作者: YH25030, 时间: 7个月前)

谢谢您的分享。想问一下，ts_regression的回测时间长吗？以前再其他其他区用过ts_regression，感觉回测时间特别长。

---

### 评论 #4 (作者: CL86067, 时间: 7个月前)

学到了，感谢大佬分享模板，感觉IND区域还是蛮不一样的，原来模板跑出好多都是robust universe sharp 不符合要求，似乎和部分股票无法做空有关系，看之前CHN区域是这样的，不知道您的这个操作，用regression_proj剔除市值的影响，是不是有助于解决这个问题呢？

---

### 评论 #5 (作者: XW23690, 时间: 7个月前)

感谢分享，思路很好：“股价与基本面过度拟合→未来回归下跌”。高换手可能是日频股价变化：ts_delta(close,1)，解决方法我暂时有以下想法，第一种是平滑滚动信号：re = ts_mean(ts_rank(-re, day), day)；第二种是加入group分组做中性化处理，我自己也测试过IND区域几乎都会降低turnover并且不丢失表现，针对longcount和shortcount较少的alpha，group_backfill(x,sector,day,std=4)很适用；第三种则是用ts_target_tvr_decay以及ts_target_tvr_hump来调整，不过容易丢失performance

---

### 评论 #6 (作者: DS48533, 时间: 7个月前)

这就是手搓党嘛，完全不懂金融的我，看着干着急，又学不会。不过尝试把你的表达式整理为参考模版，给AI作为参考好咯～

---

### 评论 #7 (作者: QY56710, 时间: 7个月前)

感谢分享.有一个小tip：Robust Sharpe较低时可以适当降低decay的值

---

### 评论 #8 (作者: ZX52486, 时间: 7个月前)

从基本面出发也能拿到一个不错的表现，但是换手率依旧很高，但同时return也高达20%

![图片](images/img_b2ed6bbff0.png)

而且可以明显发现在subindustry中和条件下，alpha的性能更好，使用线性衰减平滑时，性能并未明显降低

![图片](images/img_45b5eb8d33.png)

---

### 评论 #9 (作者: CH92851, 时间: 7个月前)

regression_proj 可惜这个我用不了。

---

### 评论 #10 (作者: HL16690, 时间: 7个月前)

regression_proj(） 显示没有这个方法

---

### 评论 #11 (作者: BJ65592, 时间: 7个月前)

感谢大佬的分享，从邮件里看到了这篇帖子，一开始没有很看懂，仔细研究了regression操作符后大概能理解了
通过使用历史长期的数据，试图找到某个数据与股票走势相关的函数，并返回当前股价波动与函数预估出来的股价波动的差值
如果股价波动高于预估值，则说明股价被高估，应该做空，反之亦然
是一个经典的反转因子，学到了一招，再次感谢大佬！

---

### 评论 #12 (作者: HL81191, 时间: 7个月前)

非常感谢，这个模板让我第一次成功提交IND的alpha，两个星期以来我自己在IND尝试的模板总是有Robust universe Sharpe或Weight等等其他条件无法通过。而这个模板在不用上二阶三阶的情况下就能出很多指标很好的alpha，我今天直接点塔了

---

### 评论 #13 (作者: MZ45384, 时间: 7个月前)

data = ts_regression(ts_delta(close,1),ts_backfill(<vec/>(<filed/>),<d1/>),200);  
re = data -regression_proj(data,rank(cap));   
rank(-re)

新模板累积中，不过我没有regression_proj和regression_neut，有其他代替吗。

==================================================================================

知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值
==================================================================================

---

### 评论 #14 (作者: ZX52486, 时间: 7个月前)

您好，一组任务的时间大概是500到600秒

---

### 评论 #15 (作者: ZX52486, 时间: 7个月前)

关于robust的问题也有这方面的考虑，CHN由于涨跌幅的限制难以做空拿到在模拟盘的收益，而IND也有相似之处，在此之前，您可以参考之前CHN的那篇帖子

---

### 评论 #16 (作者: ZX52486, 时间: 7个月前)

关于没有regression_proj和regression_neut的问题，暂时没有对策

---

### 评论 #17 (作者: HZ10678, 时间: 7个月前)

感谢分享，同样遇到不能用regression_proj的问题，在某些情况下使用regression_neut也可以优化alpha。

或者直接使用前面的代码：

data = ts_regression(ts_delta(close,1),ts_backfill(vec_avg(XXX),66),200);

很多时候也已经够用。

尝试过以下变形

data = ts_regression(ts_delta(close,1),ts_scale(ts_backfill(vec_avg(XXX),66), 252),200);

亦能减少相关性或者提高性能

---

### 评论 #18 (作者: XG98059, 时间: 7个月前)

Alpha expression includes a reversion component so we may not accept these alphas in the future, try working on different alpha ideas。想法很好，但是会有这个warining

---

### 评论 #19 (作者: HZ99685, 时间: 6个月前)

小白不理解，为什么拟合的越好未来股价可能会下跌？也有可能上涨啊？

---

### 评论 #20 (作者: WW36313, 时间: 6个月前)

您好，我想请问一下为了避免权重过于集中还有什么比较好的优化思路呢？

---

### 评论 #21 (作者: SJ65808, 时间: 5个月前)

和模板大师里面的模板比较类似

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #22 (作者: MY82844, 时间: 5个月前)

[XG98059](/hc/en-us/profiles/34425600380695-XG98059)  应该是delta(close,1)这个片段被识别成a reversion component了

---

### 评论 #23 (作者: LJ12230, 时间: 1个月前)

感谢大佬分享!

---

