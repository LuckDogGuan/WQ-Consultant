# 【Alpha灵感】“球队硬币”因子构建

- **链接**: 【Alpha灵感】球队硬币因子构建.md
- **作者**: KZ79256
- **发布时间/热度**: 2年前, 得票: 19

## 帖子正文

研报标题：方正证券 - 个股动量效应的识别及“球队硬币”因子 构建——多因子选股系列研究之四

作者：曹春晓，方正金融工程团队

概述：将股票划分为“球队”和“硬币”类股票，进行反转或不反转处理

**1.1 Alpha Idea:**

**背景**

*抛硬币* ：由于人们对抛硬币的概率可知，所以当上一次抛出为正面时，下一次猜测倾向于反面。人们会以“反转”的眼光来看待“抛硬币”

*猜球队夺冠* ：由于新赛季开始且球队磨合情况不了解，所以通常使用历史成绩考察不同球队，倾向于猜测上赛季的冠军，依旧会在本赛季夺冠。人们会以“动量”的眼光来看待“球队夺冠”。

**然而，对于股票来说，为了获得更多的收益，通常会发生过度买卖，使得“硬币”和“球队”的股票结果正好相反，即**

- “球队”股票：最终可能实际发生的是反转效应。
- “硬币”股票：最终可能实际发生的是动量效应。

同时， **认为波动率和换手率的变化量可以代表一支股票表现的“可知性”** ，即更像硬币还是更像球队。即

- 波动率低，表明股价走势相对稳定，投资者对其未来趋势做出判断也更加容易
- 换手率降低，则表示投资者对股票的意见分歧逐渐减少，也是“可知性”提高 的表现。

因此

- 波动率低的股票和换手率下降的股票，“可知性”更高， 属于硬币类型的股票，未来发生动量效应的概率更大
- 波动率高的股票和换手率增长的股票，“可知性”更低，属于球队类型的股票，未来发生反转效应的概率更大。

**1.2 主要数据字段** ：close, open, volume/cap
 **1.3 主要运算符** ：normalize, ts_mean, ts_std_dev
 **1.4 Universe** : CHN TOP3000

**2. 因子构建**

本文介绍的 **“球队硬币”因子** 由三个因子（ **“修正日间反转”因子、“修正日内反转”因子和 “修正隔夜反转”因子** ）构成。每个因子由两类因子（ **波动率处理和换手率处理** ）加和而成。

具体代码如下：

```
turnover_rate = volume/cap;turnover_rate_delta = turnover_rate - ts_delay(turnover_rate, 1);daynei_yield = close/open-1; close_delay = ts_delay(close, 1);night_yield = open/close_delay - 1;day_yield = close/close_delay-1; time = 20;# “修正日间反转”因子# “日间反转-波动翻转”因子day_yield_mean = ts_mean(day_yield, time); # 日间收益率day_yield_std = ts_std_dev(day_yield, time); # 日间波动率factor1 = if_else(normalize(day_yield_std, useStd = false)>0, -day_yield_mean, day_yield_mean);# “日间反转-换手翻转”因子factor2 = if_else(normalize(turnover_rate_delta, useStd = false)>0, -day_yield_mean, day_yield_mean);# “修正日内反转”因子# “日内反转-波动翻转”因子daynei_yield_mean = ts_mean(daynei_yield, time); daynei_yield_std = ts_std_dev(daynei_yield, time); factor3 = if_else(normalize(daynei_yield_std, useStd = false)>0, -daynei_yield_mean, daynei_yield_mean);# “日内反转-换手翻转”因子factor4 = if_else(normalize(turnover_rate_delta, useStd = false)>0, -daynei_yield_mean, daynei_yield_mean);# “修正隔夜反转”因子# “隔夜距离”因子night_dis = abs(normalize(night_yield, useStd = false));night_dis_mean = ts_mean(night_dis, time); night_dis_std = ts_std_dev(night_dis, time); # “隔夜反转-波动翻转”因子factor5 = if_else(normalize(night_dis_std, useStd = false)>0, -night_dis_mean, night_dis_mean);# # “隔夜反转-换手翻转”因子turnover_dis = abs(normalize(ts_delay(turnover_rate, 1) - ts_delay(turnover_rate, 2), useStd = false));factor6 = if_else(normalize(turnover_dis, useStd = false)>0, -night_dis_mean, night_dis_mean);# “球队硬币”因子factor1 + factor2 + factor3 + factor4 + factor5 + factor6
```

经过其他处理后，以下是回测绩效

![图片](images/img_41a47a0ac9.png)

![图片](images/img_d026829964.png)

![图片](images/img_f4902eb9d4.png)

---

## 讨论与评论 (2)

### 评论 #1 (作者: WL13229, 时间: 2年前)

想请问一下。这个文章跟👉

1. [【Alpha灵感】股票收益是球队还是硬币？](/hc/en-us/community/posts/19137620283415--Alpha%E7%81%B5%E6%84%9F-%E8%82%A1%E7%A5%A8%E6%94%B6%E7%9B%8A%E6%98%AF%E7%90%83%E9%98%9F%E8%BF%98%E6%98%AF%E7%A1%AC%E5%B8%81-)

的相关性似乎还可以，请问是做了哪些独特的工作呢。

---

### 评论 #2 (作者: TN48752, 时间: 2年前)

非常优质的文章。 希望同学们近期能有更多的文章

---

