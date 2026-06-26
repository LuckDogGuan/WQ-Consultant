# 【Alpha灵感】理想振幅因子

- **链接**: [Commented] 【Alpha灵感】理想振幅因子.md
- **作者**: XD81759
- **发布时间/热度**: 1年前, 得票: 27

## 帖子正文

本月中旬（2024/12/09-2024/12/19），我参加了因子日历研究项目，收获颇丰，实现了15个Alpha Idea（在不同的Region产生了约60个信号），并尝试总结了一些Template，最近会整理成帖子分享给大家。本文是该系列的第1篇，Idea如下：

![图片](images/img_9054fdfcc1.png)

在Brain平台的初步实现表达式如下：

```
# Step 1: 计算每日振幅amplitude = high / low - 1;# Step 2: 定义高收盘价和低收盘价的过滤条件high_threshold = ts_percentage(close, 20, percentage=0.5);low_threshold = ts_percentage(close, 20, percentage=0.5);# Step 3: 筛选高收盘价和低收盘价对应的有效交易日V_high = ts_mean(if_else(close > high_threshold, amplitude, NAN), 20);V_low = ts_mean(if_else(close < low_threshold, amplitude, NAN), 20);# Step 4: 计算理想振幅因子ideal_amplitude_factor = V_high - V_low;-ideal_amplitude_factor
```

该Alpha在USA和GLB均产生了较强信号，经简单优化后即可submit。下图分别是该Alpha在USA和GLB的Performance。

![图片](images/img_c4d7a31abc.png)  ![图片](images/img_a0e83f3375.png)  ![图片](images/img_858e8f45b2.png)  ![图片](images/img_d8e8ccda8e.png)

（如果以上内容对您有帮助，请点点赞，谢谢）

（本帖之后会在评论区继续更新，内容包括但不限于：①Alpha Idea-理想换手率因子；②受此启发得到的一个降cor且可能提升Performance的alpha优化方法；③Template-理想因子。感兴趣的小伙伴别忘了Follow喔~）

---

## 讨论与评论 (13)

### 评论 #1 (作者: PL15523, 时间: 1年前)

您好，感谢您分享阿尔法想法。我发现当使用 ts_percentage（一个很少使用的运算符）时，这种 alpha 创造力已经达到了阈值。然而，这种alpha材质使用了很多算子，这会让抢七天才处于劣势。是否可以减少一些不必要的操作符？希望您能给我更多建议

---

### 评论 #2 (作者: WP88606, 时间: 1年前)

新手可以问一下简单优化是指什么？

---

### 评论 #3 (作者: YW93864, 时间: 1年前)

[PL15523](/hc/en-us/profiles/13159798571671-PL15523)

> *然而，这种alpha材质使用了很多算子*

并非使用过多算子就不好，而是要确保使用了这些算子后，Alpha依然有经济意义。我们不能因为运算符过多而丢弃这些有价值的Alpha，我们的目的是submit有效的Alpha。这里操作的本质是对原始的数据序列进行筛选，使用ts_percentage是在构建摘选阈值，使用if_else是进行筛选，使用ts_mean是对筛选后的序列进行描述性统计，从而达到构建Alpha的目的。如果您想要减少操作符，您可以尝试只筛选一个数据序列的数据，比如只构建V_high，因为最后的V_high减去V_low做对比类似于多因子合成

---

### 评论 #4 (作者: YW93864, 时间: 1年前)

[WP88606](/hc/en-us/profiles/27032592505751-WP88606)

一般来说简单的优化是进行不同的中性化操作，例如在面板里选择Sector, Subindustry, Slow Factors等，您也可以考虑自定义中性化运算，比如group_neutralize(<alpha>, densify(Group))，只需在data里找到您想要的Group即可。

更高阶的优化，则可以尝试在计算出ideal_amplitude_factor后，对其进行衍生的运算操作。如果您对线性回归熟悉，可以看到减法实际上是特殊的回归，因此您可以通过regression_neut对其取残差；或者使用时序运算符在ideal_amplitude_factor外部进行优化，比如ts_rank(ideal_amplitude_factor,20)等

---

### 评论 #5 (作者: XD81759, 时间: 1年前)

【Alpha灵感】1.2 理想因子（换手率）

前文已经实现了理想因子（振幅），那不由得要问：是否有其他的理想因子呢？答案是肯定的。开源证券《振幅因子的隐藏结构》提到，“振幅和换手率都是反映股票成交活跃程度的指标……高价换手率和低价换手率所蕴含的信息同样存在结构性差异，价格较高处换手率具有更强的负向选股能力。从回测结果上看，理想换手率因子的选股能力要优于原始换手率因子（图14），可以视为原始换手率因子的一个有效改进方案。”

![图片](images/img_abbdb48162.png)

在Brain平台的初步实现表达式如下（构造框架和步骤与上一篇“理想振幅因子”基本一致，只是将振幅替换为换手率）：

![图片](images/img_8f24e39703.png)

该Alpha在USA和GLB均产生了较强信号，经简单优化后即可submit。下图分别是该Alpha在USA和GLB的Performance。

![图片](images/img_e5685173be.png)  ![图片](images/img_a335d78b3a.png)  ![图片](images/img_0da09ffdf2.png)  ![图片](images/img_c288124ebc.png)

（如果以上内容对您有帮助，请点点赞，谢谢）

（本帖之后会在评论区继续更新。内容包括但不限于：Template-理想因子-实例&变式。感兴趣的小伙伴别忘了Follow喔~）

---

### 评论 #6 (作者: XD81759, 时间: 1年前)

【Alpha灵感】1.3 理想因子（其他）：Template

众所周知，因子的泛化能有效提高挖因子的效率。泛化也有很多种，如：①泛化到不同的region/universe，只要因子足够robust，这种泛化是比较平凡的；②泛化到不同的dataset/datafield，这种泛化是正是Template的主要功能；③通过修改Template，形成新的、不同的Template（变式），这是另一个维度的泛化，这种泛化对Template的延展性提出了更高的要求。本文重点讨论“理想因子”后两种泛化的情况。

一个高度抽象的模板可能长这样：

```
# Step 1: 计算每日数据data = f_1({field});# Step 2: 定义过滤条件cond_1 = ccc1;cond_2 = ccc2;...cond_n = cccn;# Step 3: 计算有效交易日原始因子值d = ddd;V_1 = f_2(data, ts_operator(if_else(cond_1 data, NAN), d));V_2 = f_2(data, ts_operator(if_else(cond_2, data, NAN), d));...V_2 = f_2(data, ts_operator(if_else(cond_n, data, NAN), d));# Step 4: 计算理想因子ideal_factor = f_3(V_1, V_2, ..., V_n);# Step 5: 利用理想因子，构建最终因子f_4(ideal_factor)
```

其中，f_1是对datafield的预处理（可以不做），如ts_backfill，也可以是rank、group_normalize等；f_2是通过对data、ts_operator（及其他operator）的组合，实现的原始因子（详见以下示例）；f_3是理想因子的构建方式，包括但不限于V_1-V_2；f_4是将理想因子当作datafield后，按照其他因子构建方式，构建的最终因子（此处可用二阶、三阶、或其他Template）。

为帮助大家理解，在此给出4个简单常用的模板：

```
模板一：# Step 1: 计算每日数据data = {datafield};# Step 2: 定义过滤条件d = 63;high_threshold = ts_percentage(close, d, percentage=0.5);low_threshold = ts_percentage(close, d, percentage=0.5);# Step 3: 计算有效交易日原始因子值V_high = data*ts_std_dev(if_else(close > high_threshold, data, NAN), d);V_low = data*ts_std_dev(if_else(close < low_threshold, data, NAN), d);# Step 4: 计算理想因子ideal_factor = V_high - V_low;# Step 5: 利用理想因子，构建最终因子-ideal_factor
```

```
模板二：# Step 1: 计算每日数据data = {datafield};# Step 2: 定义过滤条件d = 63;high_threshold = ts_percentage(close, d, percentage=0.5);low_threshold = ts_percentage(close, d, percentage=0.5);# Step 3: 计算有效交易日原始因子值V_high = data*ts_std_dev(if_else(close > high_threshold, data, NAN), d);V_low = data*ts_std_dev(if_else(close < low_threshold, data, NAN), d);# Step 4: 计算理想因子ideal_factor = 2*V_high - V_low;# Step 5: 利用理想因子，构建最终因子-ideal_factor
```

```
模板三：# Step 1: 计算每日数据data = {datafield};# Step 2: 定义过滤条件d = 5;high_threshold = ts_percentage(close, d, percentage=0.5);low_threshold = ts_percentage(close, d, percentage=0.5);# Step 3: 计算有效交易日原始因子值V_high = ts_mean(if_else(close > high_threshold, data, NAN), d);V_low = ts_mean(if_else(close > high_threshold, data, NAN), d);# Step 4: 计算理想因子ideal_factor = V_high - V_low;# Step 5: 利用理想因子，构建最终因子-ideal_factor
```

```
模板四：# Step 1: 计算每日数据data = {datafield};# Step 2: 定义过滤条件d = 5;high_threshold = ts_percentage(close, d, percentage=0.5);low_threshold = ts_percentage(close, d, percentage=0.5);# Step 3: 计算有效交易日原始因子值V_high = ts_mean(if_else(close > high_threshold, data, NAN), d);V_low = ts_mean(if_else(close > high_threshold, data, NAN), d);# Step 4: 计算理想因子ideal_factor = 5*V_high - V_low;# Step 5: 利用理想因子，构建最终因子-ideal_factor
```

（如果以上内容对您有帮助，请点点赞，谢谢）

（本帖之后会在评论区继续更新。接下来几篇是在ASI-MINVOL1M-D1不同dataset上的泛化实例，有助于理解以上Template泛化方式、效果及后续调优方法等。感兴趣的小伙伴别忘了Follow喔~）

---

### 评论 #7 (作者: LH44620, 时间: 1年前)

大佬，没有ts_percentage（）操作符，有没有什么替代的办法😍

---

### 评论 #8 (作者: SD17531, 时间: 1年前)

ts_percentage这个操作符新人没有权限,有没有其他类似操作符可以实现?谢谢

```
high_threshold = ts_percentage(close, d, percentage=0.5);low_threshold = ts_percentage(close, d, percentage=0.5);
```

---

### 评论 #9 (作者: LH44620, 时间: 1年前)

大佬，没有ts_percentage（）操作符，有没有什么替代的办法

---

### 评论 #10 (作者: CZ10093, 时间: 1年前)

想请教一下您是使用了什么样的simulation setting。

下图是从您在研究小组中的ppt中的截图，可以看到sharpe和fitness都达标，也挺高。

![图片](images/img_7ed75dafae.png)

而下图是我想复现您的alpha。 **可以看到除了nan的大小写问题和没有comment，和您的代码一模一样** ，但是sharpe和fitness非常低，根本不达标。

![图片](images/img_633ecad4b3.png)

当然这个差异有可能是由于simulation setting造成的，我的simulation setting使用的如下settings。

![图片](images/img_db82b3d411.png)

**然后我尝试了多种我能够想到的simulation settings，修改了neutralization、decay和truncate，但是我仿真得到的sharpe & fitness从没有超过1 ！！**

我很好奇您采用的是一个什么样的simulation setting，能够将在表达式相同的情况下，将sharpe & fitness提升那么多。希望得到您的回答，非常感谢！

---

### 评论 #11 (作者: XD81759, 时间: 1年前)

有一些朋友可能因为操作符权限问题，无法使用ts_percentage，在此本人提供一种替代方法：

```
 # Step 1: 计算每日数据data = ts_backfill(mdl26_rank,63);# Step 2: 定义过滤条件d = 63;cond_high = (ts_rank(close, d) > 0.9);cond_low = (ts_rank(close, d) < 0.1);# Step 3: 筛选有效交易日V_high = data*ts_std_dev(if_else(cond_high, data, NAN), d);V_low = data*ts_std_dev(if_else(cond_low, data, NAN), d);# Step 4: 计算理想因子ideal_factor = 10*V_high - V_low;group_normalize(ideal_factor,country)
```

效果如下：

![图片](images/img_d418249c7f.jpeg)  ![图片](images/img_a52a13f895.jpeg)

大家在使用模板的时候，可以充分发挥主观能动性，修修改改，找到最适合自己的！

---

### 评论 #12 (作者: XD81759, 时间: 1年前)

感谢 [CZ10093](/hc/en-us/profiles/26965592415639-CZ10093) 的提问

关于设置问题，第一次跑的时候我一般设置decay=0，中性化=country。

---

### 评论 #13 (作者: YK42677, 时间: 1年前)

其实如果没有上面的这些operator，也可以用ts_mean来算出close的均值，然后用close对均值乘以一个系数去做大小比较，也能跑出来，我的理解是排序或者百分比函数选取出来的数据并不一定要是一个固定的比例，用我的方法去操作的话，反而可能能够获取数据的多样性，从而可能出现更加好的alpha。

---

