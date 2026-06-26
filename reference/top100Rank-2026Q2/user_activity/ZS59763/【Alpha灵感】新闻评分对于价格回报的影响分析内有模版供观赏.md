# 【Alpha灵感】新闻评分对于价格回报的影响分析（内有模版供观赏）

- **链接**: 【Alpha灵感】新闻评分对于价格回报的影响分析内有模版供观赏.md
- **作者**: ZS59763
- **发布时间/热度**: 1年前, 得票: 36

## 帖子正文

### **Sketch of Poster：**

本帖是参加《带你读论文》系列活动课后征文竞赛所发。

数据和表达式均是在分级之前就做好的，复现难度较大（至少得master才能用全表达式+数据），可以当做思路参考。

提供了一个手搓小模板（出了3个alpha，还没跑其他的就被ban掉了），原始特性是turnover偏高会影响fitness，在改进模版中已经加入ts_target_tvr_delta_limit运算符，有兴（权）趣（限）的读者可以试试使用trade_when（group_count(alpha,market)>数字,alpha,0）代替最外层ts_target_tvr_delta_limit。

### 

### **下边进入正文：**

Alpha核心思路：基于字段的新闻评分可以反应指数价格的变化，通过计算特定指标，并与指数价格进行回归可以得到较高准确性。

### Alpha setting：

![图片](images/img_b129adc192.png)

### **初始版本alpha：**

![图片](images/img_b2a11f40cf.png)

### 初始版本alpha表现：

![图片](images/img_343ca23f60.png)

![图片](images/img_f83a56d604.png)

### 

### **提升方法：**

研究发现在流动性较差的ILLIQUID_MINVOL1M范围内能够实现较好的预测效果，推测是因为大公司的舆情管理影响，以及大公司相对价值与新闻报道关联不大的原因。表现：TOP500<TOP1000<TOP3000<ILLIQUID_MINVOL1M。改用ILLIQUID_MINVOL1M后表现明显提升。此外，引入了target_turnover运算符降低整体turnover。

### **提升后的alpha setting：**

![图片](images/img_973f41b7c1.png)

提升后的alpha效果：

![图片](images/img_bafc947d76.png)

（turnover还是较高，这是因为我ts_target_tvr_delta_limit设置较为保守的原因（0.6，不高才怪了），在模版里面我们调整了设置） ![图片](images/img_6e21570169.png)

### 抽象出的模版：

> ```
> ts_target_tvr_delta_limit(  s_log_1p(    {group运算符}(      -ts_regression(        {ts运算符}({推荐使用pv1，至少return会有很好的信号},3),          ts_zscore(            ts_mean(              winsorize(ts_backfill(winsorize(ts_backfill({新闻字段，新闻数据集}, 120), std=4), 120), std=4),3),30),30)                ,market))                  ,{跟上边一样的pv}                    ,target_tvr={这边建议是0.4,0.2,0.1三个试一试，因为参数调整过大会影响整体表现})
> ```

搜索空间大小因为看不到数据集具体字段数也没法数，我保持所有的操作符不变，pv1那边选return，新闻字段选了三个新闻数据集出来跑，如果有大excel表存所有字段的，可以试试用：sentiment，score，news三个描述筛选。

### **能提交的alpha效果：**

趁着分级之前跑出三个alpha并提交，具体参数表现如下（ILLIQUID_MINVOL1M的就是）：

![图片](images/img_fa48306a5b.png)

![图片](images/img_0f729f654a.png)

![图片](images/img_2ab1ee26eb.png)

![图片](images/img_7793e549ed.png)

### **稳定性检查&其他地区的表现：**

被限制了，没法做。。。但之前的研究发现，同样的字段在GLB地区也有一定信号（但不是这么强烈），模版可以在集中于流动性差，或者宽指universe中进行试验

### 

### **遇到的困难与踩过的坑：**

首先要说的是找论文，现在很多论文都是靠着ml，dl和ai方法来做的，这个在第二节课上也有说过可以ai辅助找。其次是对于表达式的不熟导致不得不重新学习所有表达式的具体用法。至于遇到的坑，有些论文的想法思路（特别是早期发的论文），放到现在可能不太适用，信号消失，这个要从发布时间和稳定性方面做考虑。

---

## 讨论与评论 (1)

### 评论 #1 (作者: XX42289, 时间: 1年前)

关于开头的：【trade_when（group_count(alpha,market)>数字,alpha,0）代替最外层ts_target_tvr_delta_limit。】

提一点小小的建议：

trade_when（group_count(alpha,market)>数字,alpha,0）用于解决concentration的问题，也就是单日的持仓太过于集中。

而ts_target_tvr_delta_limit，这个是用于降低turnover的，和你说的意思一样。

这里给出一个没有ops，但是降低turn的方案：

```
hump(rank(x), hump=0.01)
```

---

