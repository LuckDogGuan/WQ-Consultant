# 【VF 0.9+顾问分享】新人常见误区之Under Fitting （欠拟合）经验分享

- **链接**: [Commented] 【VF 09顾问分享】新人常见误区之Under Fitting 欠拟合经验分享.md
- **作者**: MH33574
- **发布时间/热度**: 1年前, 得票: 39

## 帖子正文

春节期间有些懈怠了，回来收收心继续搬砖，并且给新人分享一些常见容易忽视的地方

一、【Fitting】

在很多培训中老师都有讲过 不要过拟合，Over fitting。在本文中就不在赘述了，总之一句话 when you feels not right, it is not right! 但往往新手顾问找到可以提交的alpha 以后就直接提交了，这也错失了很多提高alpha 表现从而提高value factor的机会

**总结我常见的fitting方式包括：**

**1. 改变天数 Days、Std 等Operator里面的天数**

这部分没有太多的技术含量，通过有意义的天数进行替代，最简单的办法是都试一遍 5、22、60、120、240等。当然有经验的同学可以根据数据特性来进行有针对性的调优，比如季度更新频率的数据在ts backfill 5显然是没有意义的。

**2. 更改Universe, 中性化，decay等setting里的参数**

这里也可以暴力替换，自己维护一个不同region的universe、中性化的表即可。在实操中注意第一步里替换了天数等可以选择2-5个作为表达式进行回测，一方面multi simulation要大于1个alpha才可以。

**3.针对特定情况（比如高换手率）的fitting**

一个很好用但容易被忽视的工具 PnL Visualization, 默认大家可以看到的是PnL的曲线，点击右上角的下拉菜单还可以看到不同时间的换手率，sharpe等数值。

![图片](images/img_8959d62781.png)

尤其有用的是turnover，但你看到在某一个时间这个alpha出现了剧烈的turnover的升高，很有可能是那段时间的数据有误，可以通过以下方式进行规避。（但group count是genius operator 部分人可能没有）

trade_when(group_count(alpha,market)>个数，alpha，0)

另外在手工回测的时候也可以勾选visulization选项（simulate按钮旁）这样也可以在pnl图上获取更多的信息（行业分布、市值分布、国家分布等）

此外降低turnover的常见方法包括  ts_decay_linear 等函数，尤其是平台最新推出的含有关键词tvr的operator，虽然可能会降低Sharpe，但降低tvr后可以提高fitness和margin  找到一个合理的平衡点即可。

需要注意的是这些operator需要配合scale使用，即 Operator（Scale(Alpha), Scale(Volume 如adv20）， 其他参数）

**二、【Fitting与Robust Testing】**

Value Factor本质是看OS的表现，那如果你的alpha可以在不同的universe 不同的中性化条件下都有不错的表现，也侧面证明了这个alpha本身是有很好的意义的，那也可以放心提交。

通过以上的步骤二，可以观察这个alpha在不同setting下的表现，从而进行判断是否提交该alpha

**以下是一些代码供参考**

**#获取alpha的表达式, 用来参考基线，并获取表达式**

```
target_id = 'alpha id'alpha_result = get_simulation_result_json(s,target_id)print('EXPRESSION:',alpha_result['regular']['code'])decay = alpha_result['settings']['decay']neut = alpha_result['settings']['neutralization']uni = alpha_result['settings']['universe']print('SHARPE:',alpha_result['is']['sharpe'])print('FITNESS:',alpha_result['is']['fitness'])print('MARGIN',alpha_result['is']['margin'])
```

#自行维护的对应关系表

```
region = 'ASI'neutralization = ['MARKET','SECTOR','INDUSTRY','SUBINDUSTRY']if region == 'ASI':neutralization.extend(['COUNTRY','CROWDING','FAST','SLOW','SLOW_AND_FAST'])universe= ['MINVOL1M','ILLIQUID_MINVOL1M']elif region == 'JPN':universe= ['TOP1600','TOP1200']print(neutralization)print(universe)
```

**第一步：更换天数等input**

```
days = ['5','22','60','120','240']winsorizes = ['1','2','3','4']
```

```
template = '''Alpha Expression'''expressions = []for day1 in days:forwinsorizeinwinsorizes:forday2indays:expression=template.replace('A', day1).replace('B', winsorize).replace('C',day2)expressions.append(expression)
```

**发送回测（请根据自己的代码做适配调整）**

```
#first round find daysfine_alpha_list=[]for expression in expressions:fine_alpha_list.append((expression, decay))fine_pools = load_task_pool(fine_alpha_list,10,10)print(datetime.now())multi_simulate2(fine_pools, neut, region, uni, 0, 1)print(datetime.now())
```

---

## 讨论与评论 (17)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

很有用的一篇文章，点赞

里面的函数大多可以在machinelib和acelib里面找到，也不乏需要魔改的地方。

我感觉最终形态应该是，输入一个alpha的id，单独留一个槽跑这个id所有可能性遍历（预计不会多，顶多5*10（粗略估计）），在抓取比较，选最号的提交

---

### 评论 #2 (作者: XX42289, 时间: 1年前)

感谢MH（MASTER）大佬的分享，也就是说，一个alpha想要提交，就要先遍历一下全部的天数，遍历全部的中性化，不同的universe吗？如果不是ROBUST的，那就不提交了，如果是ROBUST的，就挑最好的参数去提交！但是这样会消耗掉大量的计算资源------从而降低寻找到有信号的因子的效率-----请问大佬如何平衡呢？

---

### 评论 #3 (作者: CG48008, 时间: 1年前)

感谢分享，我尝试改了winsorize中的std=1，alpha的表现提高了不少，但是我不是很确定，这样会不会过拟合 ![图片](images/img_cdc0ca787e.png)

---

### 评论 #4 (作者: MH33574, 时间: 1年前)

[ZS59763](/hc/en-us/profiles/26858512793111-ZS59763)

是一种思路   这一步我通常是手动做的   直接10*10 跑完所有的入参遍历  剩下的setting 遍历留一个卡槽即可

---

### 评论 #5 (作者: MH33574, 时间: 1年前)

[XX42289](/hc/en-us/profiles/14187300941847-XX42289)

其实很快的，基本在200-300个回测就可以搞定了，第一轮先筛天数来fitting data 第二轮看setting。至于要不要交这个是可以根据自己存量多少以及alpha idea本身是否robust来自己权衡了

---

### 评论 #6 (作者: MH33574, 时间: 1年前)

[CG48008](/hc/en-us/profiles/27705934439703-CG48008)

我认为不太会，因为原来的4本来也就是当时笔者的经验值

---

### 评论 #7 (作者: MZ32639, 时间: 1年前)

确实更细节一些，但是是不是在大规模simulate的时候不能提供太多的帮助，需要一些预筛选？

---

### 评论 #8 (作者: MH33574, 时间: 1年前)

[MZ32639](/hc/en-us/profiles/27031307610263-MZ32639)

这个是用在已经找到了想要交的alpha  然后进行进一步优化时候用的

---

### 评论 #9 (作者: YK42677, 时间: 1年前)

很不错的观点，未来将应用在我的Alpha研究中，感谢分享。

---

### 评论 #10 (作者: BZ93061, 时间: 9个月前)

不错不错，码住

---

### 评论 #11 (作者: CW99271, 时间: 9个月前)

原来value factor分值是这样提高的，学到了，非常感谢，接下来这几天我也试试看，看看能不能学以致用。

---

### 评论 #12 (作者: YQ84572, 时间: 9个月前)

这份指导对于新人顾问很有帮助，从已经有信号的alpha通过简单调整设置得到一个优秀性能的alpha从而提高vf，实际使用效果也很好，使用这个方法我也是终于得到了一些丝滑pnl的alpha，对后续的vf提高有了自信

---

### 评论 #13 (作者: ZJ47021, 时间: 9个月前)

感谢分享

---

### 评论 #14 (作者: WD55783, 时间: 7个月前)

如果找到一个看上去还不错的alpha，通过遍历各种operator和setting的参数往往可以找到性能更好的alpha，之前在实践中主要还是通过手动修改中性化策略来遍历挑选，看完这个帖子决定还是得用代码来处理遍历覆盖更多设置参数

---

### 评论 #15 (作者: LZ25854, 时间: 7个月前)

感谢大佬的分享！让我理解了：不只是让 Alpha 看起来更好，而是要证明它在不同环境下依然合理。

> “一个 Alpha 如果能在不同 Universe、中性化条件下都表现良好，就说明它更具稳健性与经济意义。”
> 这类 Alpha 的 OS 表现更稳定，VF也能相应提高。
> 作为一个新人，看完这份宝贵的经验帖，也有些疑问：虽然调参数确实能提升表现，但如何判断“优化”与“过拟合”的分界？是否有经验性的标准呢？有时降低 turnover 会明显压低 Sharpe，那在提交决策上，是否应更看重 Fitness或者Margin ，而非 Sharpe？

---

### 评论 #16 (作者: QL88701, 时间: 6个月前)

十分感谢，这对新人有很大的帮助！！

---

### 评论 #17 (作者: PP26750, 时间: 5个月前)

大佬分享得太及时了！特别是关于暴力遍历参数的思路，虽然之前也模模糊糊想过，但您讲得这么系统还是第一次见。感觉找到了方向，不像之前那样盲目调参了。代码示例也特别实用，虽然我还得慢慢消化。以后找alpha就得按您说的这么系统地测试，不能找到个差不多的就交了。看来value factor提升还是有方法可循的，不是纯靠运气。必须点赞！好好研究研究您说的这些方法，争取早日把VF提上去。大家一起加油！

---

