# 【Super Alpha】SIMPLE和HCAC主题获奖的sa经验分享经验分享

- **链接**: [Commented] 【Super Alpha】SIMPLE和HCAC主题获奖的sa经验分享经验分享.md
- **作者**: ZZ44620
- **发布时间/热度**: 1年前, 得票: 42

## 帖子正文

## 所有这两周SA概览

### SIMPLE

![图片](images/img_9fed098fbd.png)

### HCAC

![图片](images/img_524fd70d89.png)

## 准备工作

我是采用非手搓先随机生成的方法，参考（copy）自 [JL16510](/hc/en-us/profiles/25889743296151-JL16510)  的 [多线程遍历回测super alpha – WorldQuant BRAIN](../JL16510/多线程遍历回测super alpha代码优化.md) 与 [HW93328](/hc/en-us/profiles/28771941793815-HW93328)  的 [Super alpha全自动回测代码--开箱即用！](../JX79797/[Commented] Super alpha全自动回测代码--开箱即用代码优化.md)

## 基本想法

HW大佬的想法随机生成类似的，首先是做一些 **单位条件** ，类似于`turnover<0.1`
再去生成条件表达式 **硬筛选+权重排序** 和带selectlimit的select表达式，去在wq平台查看是否满足数量

```
not own && week theme && 条件1 && 条件2 * 权重去排序
```

若满足数量条件，则随机从combo列表选择一个combo表达式后面去回测。这里你可以自定义的
- 单位条件的范围`(turnover<0.1)`；
- 选择权重排序`1/operator`，我当时问ai说我就要给`operator==5`的最高分，大于或小于都给低分（>0），然后ai也会给你一个公式；
- combo表达式，从其他大佬分享帖子和sac会议上积累的；
- select limit，之前一直感觉大数量会表现好，看到ACE第二他的分享是小数量（50个）出来的货也能很好。

## 遍历回测--多样性

> 低相关可能我从这个比赛才开始交SA

可以随便跑，我一开始只是遍历各个region和universe只为了找到能过pd的，一直过不去pd，第一天没交上。第一周后面听到群里JG佬说 **model过拟合** ，那我在所有前面都加了`not(model)`（这里简写），

假设是 **之前听说model很多都过拟合，我就基本不碰** ，

然后基于这个假设，生成随机去回测，并看看这批跑的表现。
我的理解是，如果你不基于任何假设的话，你生成的sa其实都来自一个 **很大的分布上** ，然后你去 **提前限制** 就在 **大分布** 上找一个 **小分布** ，希望这个小分布生成出来的表现好。

> 如果想假设一些有意义的，可以看看每个周的主题比赛里面的alpha大概是什么样子的？

所以后面几周我都是先带一些假设（偏见）去生成，比如HCAC，太容易组出来厂，听weijie老师说用pnl的标准差去判断，然后我让ai去生成了类似的combo，然后这样去组的alpha：

```
stats = generate_stats(alpha);chang = ts_std_dev(stats.pnl, 252);<defs...>  # 可为空scale((<last_expr>) * rank(chang))
```

想法就是最后乘个chang，或者之前游戏王说的`if_else(rank(chang)>0.5, alpha,0)`。但这样假设最后的效果并不好，因为我感觉假如选择的ra有三种，

- 一种好的向上的；
- 一种平的；
- 一种更坏的向下的。

感觉上面`rank(chang)`只能过滤掉中间那个，然后内部还是说第一种和第二种相抵消，最后sa出来还是一个厂，除了上面分析拿图举例，蓝绿是不带rankchang的；红色是带的，其实感觉没啥区别

![图片](images/img_69c38efd29.png)

对此我并没有什么好的方法，但是感觉ACE第二大佬，他一个combo可能会比上面更好

```
stats = generate_stats(alpha); a = stats.pnl; ts_mean(a,252)/ts_std_dev(a,252)
```

最后是，我遍历去回测然后图打出来看看哪个设置会更好，然后可能会更多的去跑这个区域，可以去调整这个顺序`["ILLIQUID_MINVOL1M","TOP3000"]`。除了图我还有一些平均值之类的计算，这里不再列出了

![图片](images/img_405b6fc218.png)

![图片](images/img_0e6c6036b4.png)

## 

## 

## 筛选法与加权法battle？

严格去定义这两种思路，不混到一块用的话：

- **筛选法 (Screening)** ，&&人&&挤&&人&&，符合就选进来，不符合就拒之门外；
- **加权/稀释法 (Weighting)** ，就是每个条件只是对选进来的给一个分（我没搞懂是先对整个ra库算出来分再排序选择还是什么），又称if else大法？

下面是Ai的回答
这是一个非常精彩的提问，触及了Super Alpha构建中两种核心哲学思想的对比：“ **筛选法 (Screening)** ” vs “ **加权/稀释法 (Weighting/Dilution)** ”。

现在，我们来对比你之前的“筛选法”和这种“加权法”。

![图片](images/img_7f48c2f398.png)

**结论** : 它们不是互相替代的关系，而是 **互为补充** 的。

所以我现在随机生成的模板是“ **多筛选单一加权** ”，sa论坛分享中有人用if else打分我没用过，感觉塞不进来这个生成的代码中。

另外我现在没想明白 **打分分层** 与 **筛选分层** 之间的区别？比如

- `if_else(turnover >= 0.15 && turnover <= 0.20, 1.5, 1) * if_else(turnover >= 0.30 && turnover <= 0.35, 1.5, 1)`
- ((turnover<0.07&&turnover>0.05)||(turnover<0.15&&turnover>0.13)||
  (turnover<0.12&&turnover>0.09)) ，与游戏王的turnover分层的区别？

## 筛选条件--只设置了正整数

- 正整数
- 非零
- 非nan

我感觉在上面生成模式下，都可以转换成正整数的selecthandling，除非if else设置零，否则我不知道改这个参数有什么用处，还有nan也是，我看到的例子都是if else进行设置的，感觉没有天然的nan和zero去过滤，你需要人为指定条件。

## 多样性与分层

- **Region**  -- 基本上如果有region我都跑跑
- **Universe**  -- 第一次我会跑很多，后面就是每个region单一跑了
- **中性化** -- 现在是stat用的多了，但是pnl真的很低
- **Selectlimit -** - 我感觉还是从小到大都去看看效果
- **Author**  -- 防止一直选一个作者的
- **数据集种类**  -- 橘子姐采取的思路

关于最后一点，数据集没必要，每个地区重合的数据集不一样，如果选到该地区没有的数据集老报错。

另外我有个思路是可以让ai去给出数据类别组合， **假设是这几个数据ra的性质上互补或者这对种类ra相加表现好？**

但是有个问题， **你怎么知道你选到的ra既有种类A也有种类B的** ，除非你自己手搓，比如设置150数量，然后先限制A和其他条件，使得选到数量降到150以下，然后再添B，但是这样代码层面不太好实现以我现在能力，所以我没试过：

```
not own && week theme && 互补数据类别 && 普通条件1 && 普通条件2 * 权重表达式
```

另外一开始我没关注到author，主要后面听到weijie老师说的“ **最好的情况你这个ra来自不同dataset和不同的author** ”

> 来源越分散，抗风险能力通常越好，这在量化投资中被称为“免费的午餐” -- AI

但是前者有的选，后者真的不太好控制，尤其前几周稍微上author都选不到ra，但是ACE中能用author不会过度的过滤掉很多ra，所以我尝试在代码中添加author的单位条件（learn里面那种），然后随机生成变成

```
not own && week theme && 作者条件 && 普通条件1 && 普通条件2 * 普通权重* 作者权重
```

## 怎么去调整挑选到的raw sa

首先 **我最基本假设是你不要去大改，每个地方全都修改。**

因为我当时比如说又在后面乘了很多权重表达式，效果并不好；亦或者去添加很多很多条件，有可能更差，但是在SAC会议上主持人尝试很多条件然后如果表现差去 **反转** 。

只在你挑到那个sa进行整容 **微调** ，从论坛的经验来看有下面这么几种

1. 相关性，operator，turnover就简单的添加上去选的更少的或者选择更低相关，假设这样做会增强表现；
2. AK小猫哥的想法：将极简alpha和复杂alpha组合，尝试把sa select写出一个复杂版本？引出下面思路
3. **针对性对冲：**

我的理解是，举个栗子，你挑到的随机生成的长这样（一般是过pd，近几年表现好，要不你干嘛费劲？）

```
not(own)&&in(competitions, "ACE2023")&&(datafield_count<=3)&& (category == "NONE") * ((1 / (log(turnover + 1) * power(decay, 2))) * (author_sharpe / (author_turnover + 0.05)))
```

然后注意到 **权重是关于turnover的式子** ，以及含有datafield筛选
第一步尝试

```
not(own)&&in(competitions, "ACE2023")&&(datafield_count<=3|| datafield>=6)&&  # <---(turnover<=0.1)&&                # <---(category == "NONE") * ((1 / (log(turnover + 1) * power(decay, 2))) * (author_sharpe / (author_turnover + 0.05)))
```

如果表现还不好，我就是对turnover对冲，因为我的权重是关于turnover的， **所以我假设限制或者对冲turnover可能有好的表现**

```
not(own)&&in(competitions, "ACE2023")&&(datafield_count<=3||datafield_count>=6)&&(turnover<=0.1|| (turnover>0.2&&turnover<0.3))&& # <---(prod_correlation < 0.3) * (category == "NONE") * ((1 / (log(turnover + 1) * power(decay, 2))) * (author_sharpe / (author_turnover + 0.05)))
```

> 注：我只是这样想的，但真实上说会不会更好不太清楚，至少对我来说能过pd或者提升IS表现了，另外也可以 **尝试作者条件对冲？没试过**

1. 最后一个我试过的方法： **修改combo** ，除了换combo我还有几个都加一块，你可以想象猫和老鼠那集Tom调制药水什么都掺点，最直接的是

```
stats = generate_stats(alpha);w1 = combo_a(alpha, nlength = 40, mode = "algo1");w2 = combo_a(alpha, nlength = 160, mode = "algo1"); w3 = combo_a(alpha, nlength = 252, mode = "algo1");w4 = (ts_mean(stats.returns, 126) / ts_std_dev(stats.returns, 126))/reduce_powersum(self_corr(stats.returns, 252), constant = 2);scale(w4) + scale(w2) + scale(w3) + scale(w1)
```

其中w1 w2 w3 是华子哥降sa的pd，w4是sac第二次会议上主持人写的，然后我就掺进来，原本代码combo list是这样

```
w1 = combo_a(alpha, nlength = 40, mode = "algo1");w2 = combo_a(alpha, nlength = 160, mode = "algo1");w3 = combo_a(alpha, nlength = 252, mode = "algo1");signed_power(scale(w1) + scale(w2) + scale(w3),2)
```

这个估计来自第一次SAC会议上主持人写的combo

```
w1 = combo_a(alpha, nlength = 250, mode = "algo1");w2 = combo_a(alpha, nlength = 250, mode = "algo2");w3 = combo_a(alpha, nlength = 250, mode = "algo3");scale(w1) + scale(w2) + scale(w3)
```

后面收集到一些其他的也可以掺进来

```
stats = generate_stats(alpha); a = stats.pnl; ts_mean(a,252)/ts_std_dev(a,252)
```

我最多就是尝试4个w，没试过更多的，有这个必要吗，因为感觉越多越混乱，我不知道这个combo再计算什么了？

> 当我们掺combo时，我们在计算什么？

另外reduce的combo我没很明白怎么玩的，所以没试过。

### 什么时候停止调整--sa 也有过拟合？

我朴素想法是无论select和combo写的如何复杂，sa好像没有过拟合这一说法。但是weijie老师说，一个idea被修改十次就差不多了，再改就危险了。我自己在调某个sa时候，一直调整selectlimit和decay，脑子在想的是“166吉利数字啊，说不定会更好？”，这种我感觉就往overfitting路上走了。

## 其他碎碎话

- MAX TRADE: ON，就是我怎么生成怎么组，都很难组出来pnl到20M的，我不知道为啥，基本就说11M-16M之间；
- && 和*是一样的？有时候我把*变成&&就选不到了；
- ai推荐数据集组合我在老虎模板试过然后vf爆掉了，我感觉是ASI的问题，但是也谨慎对待AI的回答。

## **附录**

这天太累了，就不列各个大佬关于sa的经验了，我把自己用到的sa某些可能有用代码放在这里，下面包含AI生成谨慎使用

base_list意思是，比如你选了一个combo，可以类似于`combo*rank(chang)`这种叠加其他操作，但我现在没用过了

```
    # ---------------- 原始 combo 列表 ----------------    base_list = [        # '1',        # 在ACE中几乎无效的        'stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr',        'stats = generate_stats(alpha); mom =  ts_mean(stats.returns, 60) / ts_std_dev(stats.returns, 60); ts_rank(mom,252)',        'stats = generate_stats(alpha); tv = ts_mean(stats.trade_value,60); tv_crowd = tv/ts_delay(tv,60); ts_rank(-tv_crowd,252)',        'stats = generate_stats(alpha); std = ts_std_dev(stats.returns,60); std_crowd = std /ts_delay(std,60); ts_rank(-std_crowd ,252)',        'stats = generate_stats(alpha); ic = self_corr(stats.returns,60); inneric = if_else(ic==1,nan,ic); ts_rank(-reduce_min(inneric),252)',        'stats =generate_stats(alpha);covariance_matrix=ts_covariance(stats.returns, stats.returns, 126);covariance_matrix',        'stats = generate_stats(alpha); a = stats.pnl; ts_mean(a,252)/ts_std_dev(a,252)',        # 自己写        # 'stats = generate_stats(alpha);w_stable = -ts_max(stats.drawdown, 63);ts_rank(w_stable, 126)',        # AI 生成        # 'stats = generate_stats(alpha); ir = ts_mean(stats.returns, 250) / ts_std_dev(stats.returns, 250); dd_pen  = 1 - abs(stats.drawdown); ir * dd_pen',        # 'stats = generate_stats(alpha); mom60 = ts_sum(stats.returns, 60); market_on = ts_rank(ts_mean(mom60, 120), 250) > 0.6; w = if_else(market_on, ts_rank(mom60, 500), 1); w',        # 'stats = generate_stats(alpha); ir = ts_mean(stats.returns, 125) / ts_std_dev(stats.returns, 125); vol = ts_std_dev(stats.returns, 125); w = ir / (vol + 0.001); ts_rank(w, 500)',        'stats = generate_stats(alpha);pos = ts_sum( if_else(stats.returns>0,  stats.returns, 0), 60);neg = ts_sum( if_else(stats.returns<0, -stats.returns, 0), 60);ts_rank( pos / (1 + neg), 500 )',        # 降 corr 专用        'w1 = combo_a(alpha, nlength = 250, mode = "algo1");w2 = combo_a(alpha, nlength = 250, mode = "algo2");w3 = combo_a(alpha, nlength = 250, mode = "algo3");scale(w1) + scale(w2) + scale(w3)',        'w1 = combo_a(alpha, nlength = 40, mode = "algo1");w2 = combo_a(alpha, nlength = 160, mode = "algo1");w3 = combo_a(alpha, nlength = 252, mode = "algo1");signed_power(scale(w1) + scale(w2) + scale(w3),2)',        'w1 = combo_a(alpha, nlength = 40, mode = "algo2");w2 = combo_a(alpha, nlength = 160, mode = "algo2");w3 = combo_a(alpha, nlength = 252, mode = "algo2");signed_power(scale(w1) + scale(w2) + scale(w3),2)',        'w1 = combo_a(alpha, nlength = 40, mode = "algo3");w2 = combo_a(alpha, nlength = 160, mode = "algo3");w3 = combo_a(alpha, nlength = 252, mode = "algo3");signed_power(scale(w1) + scale(w2) + scale(w3),2)'    ]    for day in [125,252]:        for algo in ['algo1']:  # , 'algo2' , 'algo2', 'algo3'            base_list.append(f"combo_a(alpha, nlength = {day}, mode = '{algo}')")
```

权重：

```

```

```
    # ---------- 1. 普通维度权重 ----------    ordinary_weights = [        # ———— 交易成本导向 ————        '1 / (turnover + 0.02)',               # 换手率越低 → 交易成本越低，权重越大        '1 / (log(turnover + 1) * power(decay, 2))',   # 同时惩罚高换手与高 decay，鼓励稳健低成本信号        # ———— 覆盖率 / 有效度 ————        '1 / ((long_count + short_count + 1)*abs(long_count - short_count))',   # 多空均衡度，越均衡越小，分子越小 → 权重越小（惩罚失衡）        'log(long_count + short_count + 1) / log(universe_size(universe))', # 绝对覆盖率：覆盖股票数越多越好        # ———— 拥挤度 & 自相关性 ————        '1/ (sigmoid(prod_correlation)+0.01)',      # ProdCorr 越小越好，降低市场拥挤        '(1 - sigmoid(prod_correlation)) * (1 - sigmoid(self_correlation)) / (turnover + 0.02)', # 少拥挤、少自相关且低换手        # ———— 复杂度惩罚 ————        '1 / (operator_count + 1)',                 # 运算符越多，表达式越复杂，潜在过拟合 → 权重降低        '(100 - decay) / (operator_count + 1)',     # 偏好低 decay + 简洁表达式        '1 / (dataset_count * datafield_count + 1)',# 数据源 & 字段越少，简单易解释且不过拟合        # ———— 其他稳健性度量 ————        '(1 - truncation) * (1 - turnover)',        # 低截断 + 低换手 → 稳定且低成本        '(long_count + short_count)', # 覆盖率（多空合计 / Universe）        '(prod_correlation) * abs(self_correlation-0.5)', # 多空相关性越小越好    ]    # ---------- 2. 作者维度权重 ----------    author_weights = [        '1',        # ———— 作者产出效率 & 活跃度 ————        # 'sigmoid(author_yield_rate)',              # 历史提交产出率高 → 经验证有效性强        # 'sigmoid(author_quarter_yield_rate)',      # 近 90 天活跃产出率        # ———— 作者稳健性 ————        '(1 - author_prod_correlation) * (1 - author_self_correlation)', # 作者整体信号相关性低 → 多样化        # 'author_returns_to_drawdown',              # 作者收益回撤比，高于 1 越好        # # ———— 作者风险收益与成本 ————        # 'author_sharpe / (author_turnover + 0.05)',# 高 Sharpe & 低换手 → 风险收益优秀且成本低        # ———— 作者多样性维度 ————        '1 / (author_distinct_count_regions + 1)', # 地区越多可能风格分散，惩罚过分分散        # '1 / (author_distinct_count_dataset + 1)', # 数据集越少 → 简洁可解释，减少过拟合        # '1 / (author_distinct_count_operator + 1)',# 运算符种类越少 → 简洁、稳定    ]    # 综合权重示例：高产出 & 低相关 / 低换手    # author_weights.append('sigmoid(author_yield_rate) * (1 - author_prod_correlation) / (author_turnover + 0.05)')
```

---

## 讨论与评论 (21)

### 评论 #1 (作者: KH94146, 时间: 1年前)

限时置顶一周，并已收录至SA经验合集置顶中

---

### 评论 #2 (作者: LL87164, 时间: 1年前)

[ZZ44620](/hc/en-us/profiles/28856702901527-ZZ44620)

刚刚开始 SA 的旅程， 这篇文章真是及时雨。点赞！👍

想和大家探讨的是：

1. 既有种类 A 也有种类 B，用 in(datacategories, "A") && in(datacategories, "B") 实现不就可以吗

2. 关于“ ***&& 和*是一样的？*** ”，我的理解是：&& 是 [1,0] 的判断，即是否被选中（假设 selection handling 为 positive 的话）；而 * 只是在前一个的结果基础上加个权重。

3. 关于下面这个表达式：

- `if_else(turnover >= 0.15 && turnover <= 0.20, 1.5, 1) * if_else(turnover >= 0.30 && turnover <= 0.35, 1.5, 1)`

假设 selection handling 为 positive，上面这个相当于满足 turnover >= 0.15 && turnover <= 0.20 或 turnover >= 0.30 && turnover <= 0.35 的为 1.5，其余的都是 1，然后排序按 limit 数选出所有 Alpha，包括不满足这个两个条件的也有可能选出来。

而 (turnover >= 0.15 && turnover <= 0.20, 1.5, 1) || (turnover >= 0.30 && turnover <= 0.35, 1.5, 1) 相当于只选出来满足这两个条件的，其他的一律不选。

最后，想问博主的是：与 AI 协作时，都“喂“什么给它？所有 Selection 和 Combo 能用到的操作符和相关说明吗？

---

### 评论 #3 (作者: SZ83096, 时间: 1年前)

好强的大佬啊，这么多独特的combo，真是学到了啊。

select 里面好多我没有尝试过的参数啊，接下来有时间了会尝试下效果的。

感谢大佬的分享，祝大佬vf 月月保持高水平。

======================================================

---

### 评论 #4 (作者: ZY77039, 时间: 1年前)

感谢分享，weight花样非常多，学到了，你说的收益比较低，没有超过20M，又何尝不是一种恰到好处的fitting。

---

### 评论 #5 (作者: JL76306, 时间: 1年前)

非常感谢楼主大大的分享，为已经手动制作了五六个礼拜的我来说注入了新的想法和力量！

SAC比赛一路以来受到很多贴主开源精神的强力帮助，至此也有幸获得过SAC周奖。借楼主之贴，我也将我的一点小小的观察想法分享给大家：

在制作SA的时候，我对learn里面的op操作符进行了再次的学习，其中特别的注意到了combo专用符栏目，至此，我开始了这方面的尝试和学习。

其中以下几款reduce类combo在一些条件下产生的SA效果更为显著，大家可以搭载试试看：

```
combo 1：
```

stats = generate_stats(signed_power(alpha,2));

ic =reduce_ir(self_corr(stats.returns, 120));

1/(1+ic)

```
combo 2:
```

stats = generate_stats(signed_power(alpha,2));

ic =reduce_norm(self_corr(stats.returns, 120));

1/(1+ic)

```
combo 3:
```

stats = generate_stats(signed_power(alpha,2));

ic =reduce_max(self_corr(stats.returns, 120));

1/(1+ic)

以上表达式是我在使用reduce combo表达式中最经常发现优质SA 的表达式，但不乏有些reduce操作符在特定的university和select下会有更好的表现，当然也有许多时候等权的combo（alpha）会更好，这都需要大家在使用时进行实际调试。

最后，再次感谢伟大的开源精神，感谢各位的帮助和友好的社区氛围！

---

### 评论 #6 (作者: XC66172, 时间: 1年前)

必须手动点赞，感谢大佬在群里分享的文档~~ 里面的combo表达式很有用，今天试用了一个PC立马就降了一些 （终于提交上了一个PC <0.5的 虽然fitness <5) 且还和equal weight的表现差不多

=================================================

FIGHITNG LABUBU

=================================================

---

### 评论 #7 (作者: ZZ44620, 时间: 1年前)

[LL87164](/hc/en-us/profiles/28834270391959-LL87164)

1. 不是要选到既有种类 A 也有种类 B的ra，而是要选到 **只在种类A** 和 **只在种类B** 的ra，这样可能更纯净一些，然后假设这两数据类别做出来的ra会在某种程度上去互补；
2. 但是比如*(operator == 2)这种，我之前理解成也是如果operator==2，就相当于乘1，否则相当于乘0？

```
not(own)&&in(classifications, "ATOM")&&(turnover<0.1)&&((prod_correlation<0.4)&&(prod_correlation>0.1))&&((self_correlation<0.2)&&(self_correlation>0.1))&&(operator_count<4)&& (datafield_count==1) * (1/operator_count)
```

但我上面这个例子只能选到3个，把前面的&&换成*就可以选到很多个

我喂ai除了learn里面的super alpha的selection文档和combo文档以及论坛里面的经验和具体有用的combo或者select表达式

---

### 评论 #8 (作者: AK76468, 时间: 1年前)

感谢ZZ佬的无私分享！我从中学习到了很多SELCETION和COMBO的idea和tech！希望您在SAC比赛中取得好成绩！！

我有一些问题，您平时是如何从可以提交的sa中抉择出最终提交的sa呢？Comparison这个功能您是如何使用的？如果要给Corr、基础指标、Comparison按照重要程度排序，您会更看重什么？

---

### 评论 #9 (作者: LL87164, 时间: 1年前)

[ZZ44620](/hc/zh-cn/profiles/28856702901527-ZZ44620)

RE:  **只在种类A** 和 **只在种类B，** 用下面这个表达式怎么样

```
 (in(datacategories, "A") && (datacategory_count=1)) || (in(datacategories, "B") && (datacategory_count=1))
```

---

### 评论 #10 (作者: XW61573, 时间: 1年前)

感谢大佬的分享，我们也在努力的学习中，期待能够学习到更多，获取更多的SA

---

### 评论 #11 (作者: ZZ44620, 时间: 1年前)

[AK76468](/hc/en-us/profiles/28846915371031-AK76468)

我一开始只是为了过pd，后面的话听了游戏王的建议比较看重近几年comparison指标。我一般步骤

1. 淘到一个好的，近几年指标加分，但是整体分数不要扣太多，比如扣1000分一内，并且过pd；
2. 然后我再去微调，看看这几个地方会不会更好：1) 近几年表现，2) 整体指标，3) 少扣点分；
3. 自相关这个真的可能因为我交的sa比较少，所以没怎么关注过，也比较低。

第一步中，因为我随机生成，其实每批生成70个，然后一晚上跑几个中性化，比如某个sa在这几个中性化都不错就会收藏，或者单纯近几年好的，看完之后一般不会超过4-5个吧。另外我会把这些一个一个放到alpha lists和已经交过的对比，以及他们之间的对比（主要是Pnl吧）

---

### 评论 #12 (作者: JR23144, 时间: 1年前)

感谢大佬的无私分享，不过我发现赛选条件特多，像EUR 这样的区域 就不会得到匹配条件能上的regular alpha,匹配不到那么多的alpha ，表现感觉就会差一些

===================================VF 1.0 =======================================

---

### 评论 #13 (作者: YH25030, 时间: 1年前)

谢谢您的分享。下面那个搜索条件给我很大启发。

not own && week theme && 条件1 && 条件2 * 权重去排序

刚才我尝试着用dataset_count,datacategory_count和 author_prod_correlation<0.3的权重去排序。在ATOM里面得到不错的结果，Product Corr小于0.5.

![图片](images/img_f9d81bfe97.png)

---

### 评论 #14 (作者: JR23144, 时间: 1年前)

```
not own && week theme && 条件1 && 条件2 * 权重去排序
```

感谢ZZ 佬， 用了这个之后匹配到的alpha 更多了，非常的不错，并且 Prod Correlation 也都是很低，博主写的用心了，特地回来反馈一下，不过还是有些疑问，有些alpha 之间自相关性都比较高，怎么用排除法，去除某些相关性的问题，保证可以提交最多的super alpha 。

---

### 评论 #15 (作者: ML42552, 时间: 1年前)

感谢ZZ佬的分享，阅读完本贴感觉收获良多，再对super alpha 的selection 理解更加深刻的同时，了解到了更多的combo模板，目前我也是用 自 [JL16510](/hc/en-us/profiles/25889743296151-JL16510)  的 [多线程遍历回测super alpha – WorldQuant BRAIN](../JL16510/多线程遍历回测super alpha代码优化.md) 与 [HW93328](/hc/en-us/profiles/28771941793815-HW93328)  的 [Super alpha全自动回测代码--开箱即用！](../JX79797/[Commented] Super alpha全自动回测代码--开箱即用代码优化.md) 的结合，非常好用！感谢大佬们的无私奉献。

最后祝愿大佬25年sa大赛能够获得全球第一！！！

----------------------------------------------------------------------------------------------------

---

### 评论 #16 (作者: YQ51506, 时间: 1年前)

感谢大佬的无私分享，对于selection和combo的思考很有深度，向你学习

---

### 评论 #17 (作者: TY59174, 时间: 1年前)

对SA还没有什么认识,正好从大佬的这篇分享中学习,感觉这是值得反复阅读几次的

---

### 评论 #18 (作者: ZV96737, 时间: 1年前)

拜读了您的分享，感觉收获了很多。从随机生成策略到筛选与加权法的实践，再到 combo 组合的创新思路，都让我对 Super Alpha 的构建有了新认知。特别是多维度权重设计和避免过拟合的提醒，解决了我不少实操困惑。感谢无私分享，启发良多！祝大佬每天60刀拿满

---

### 评论 #19 (作者: MY27687, 时间: 11个月前)

==================================MY27687===========================================
感谢大佬分享的sa经验帖，确实有自己的独特idea，也感谢大佬无私分享了这么多Combo Expression，最近刚好在寻找这方面的comb，太感谢大佬了，希望大佬base多多，vf高高！！！！

====================================================================================

---

### 评论 #20 (作者: DT40395, 时间: 9个月前)

通篇认真读完，真的是涨太多知识了，感谢大佬的SA经验分享，combo表达式太需要了。也祝大佬VF0.9+

---

### 评论 #21 (作者: WX84677, 时间: 6个月前)

这篇 SA 教程从思路到实践案例非常丰富且有理论体系，总结出筛选法、权重法两大流派，且对比分析了两者的差异和优势劣势。最绝是结尾竟然还附赠的一堆表达式案例！感谢大佬无私分享！！

祝大佬：
vf 常1，Base 拉满，定级 GM，wf 疯涨！

---

