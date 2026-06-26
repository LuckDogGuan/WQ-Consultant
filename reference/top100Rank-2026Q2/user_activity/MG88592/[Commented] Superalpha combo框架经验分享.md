# Superalpha combo框架经验分享

- **链接**: [Commented] Superalpha combo框架经验分享.md
- **作者**: JX14975
- **发布时间/热度**: 10个月前, 得票: 57

## 帖子正文

最近，在社群中发现很多刚开始组sa的顾问，不清楚combo的具体选择方式，楼主在sac比赛期间与weijie老师交流了一下combo的思路，因此发出来抛砖引玉。

首先，我理解的combo思路分两个部分：先是筛选，然后才是组合。

第一步：筛选是为了过滤掉一些狭义的厂（即：数据只有几个月甚至几天的因子），不建议用来过滤其它alpha指标：毕竟只看pnl过去的表现与未来没有统计相关性。

过滤狭义的厂的combo是：stats=generate_stats(alpha);if_else(ts_std_dev(stats.returns,250)>0,[your_combo],0)。部分用户也希望能够过滤广义的厂（后期pnl变平的alpha）：stats=generate_stats(alpha);if_else(rank(ts_std_dev(stats.returns,250))>0.5,[your_combo],0)，0.5是一个任意的取值，可以自行修改。

第二步，即上述combo中【yourcombo】的部分，比较常见的1（等权）和combo_a。combo_a是wq提供的基于机器学习算法的组合方式，分为algo1\algo2\algo3三种，默认algo1。有人（我）猜测它们能够依次对应3种比较常见的多因子组合方式：最小相关性组合、等风险贡献组合、最小波动率组合，但没有证据（因为weijie老师说他从来不用combo_a），欢迎大家一起考证。

有大佬提出：参考随机森林的优化方法，将3种算法的结果归一化（scale）然后组合（加）起来，能够增加优化效果，同时采用不同的nlength，能够捕捉alpha不同周期层面的特征。如：scale(combo_a(alpha,mode=’algo1’,nlength=40))+ scale(combo_a(alpha,mode=’algo1’,nlength=160))+ scale(combo_a(alpha,mode=’algo1’,nlength=250))

根据数学原理，1（等权）是机会最大的组合。意思就是：从sharpe和fitness表现来看，大多数combo都是花里胡哨不如等权的（要么就是与等权差不多）。因此推荐大家优先使用等权组合（划重点！）。

除了等权以外，如combo_a等组合方式都是用alpha过去的表现预测未来（没有经济学意义支撑的预测），因此其稳健性自然大多数时候不如等权——这还只是在使用相关性与波动率的情况下，如果用sharpe或者收益率直接筛选，过拟合必然更加严重。基于相关性与波动率的组合方式除了combo_a，还有1/ts_std_dev(stats.returns,252)（风险平价组合），1/reduce_powersum(stats,returns,constant=2)（相关性平方和倒数）：

```
    ["combo_a(alpha)",    'combo_a(alpha,mode=\'algo2\')',   'combo_a(alpha,mode=\'algo3\')','stats = generate_stats(alpha); 1/ts_std_dev(stats.returns,252)',‘1/reduce_powersum(stats,returns,constant=2)’]
```

最后，组合时务必注意：非chn市场不建议做空任何wq因子。最好能确保你的combo表达式在任何情况下都不会给alpha一个负权重。

附录：遍历combo_a的组合方式

```
def combo_a_combined(mode1,othermods,mode1day):    ls=[]    days=[20,40,160,250]    days=[day for day in days if day<mode1day]    allmods=['algo1','algo2','algo3']    for day in days:        for mod in othermods:            ls.attend(f'(scale(combo_a(alpha,mode={mode1},nlength={mode1day}))+scale(combo_a(alpha,mode={mod},nlength={day})))')            if day>63 and len(othermods)>1:                days1=[day1 for day1 in days if day1<day]                mode3=[mode for mode in allmods if (mode !=mode1 and mode!=mod)][0]                for day1 in days1:                    ls.attend(f'(scale(combo_a(alpha,mode={mode1},nlength={mode1day}))+scale(combo_a(alpha,mode={mod},nlength={day}))+scale(combo_a(alpha,mode={mode3},nlength={day1}))')    return ls
```

```
for combo in combo_a_combined('algo3',['algo2','algo1'],250):
```

---

## 讨论与评论 (5)

### 评论 #1 (作者: CW99271, 时间: 10个月前)

我一开始也是不懂怎么组SA

---

### 评论 #2 (作者: DS48533, 时间: 9个月前)

感谢分享，尤其是慷慨的给了代码，另外，如果你能看到的话，想问下，如何在帖子中，像你这样插入带有正确缩紧的代码片段啊

---

### 评论 #3 (作者: MG88592, 时间: 5个月前)

感谢分享，目前论坛对select的帖子已经较为完备，对于combo的帖子比较稀缺，感谢分享。
希望有更多的人可以提出自己的combo idea 。
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #4 (作者: HM97321, 时间: 5个月前)

感谢

---

### 评论 #5 (作者: FF56620, 时间: 1个月前)

感谢分享，最近发现own的alpha，都组不出来了，来论坛找找灵感，找到这个帖子，很多还没用过，试试效果。

----------------------------------------------------------------------------------------------------------------------------------------------------

---

