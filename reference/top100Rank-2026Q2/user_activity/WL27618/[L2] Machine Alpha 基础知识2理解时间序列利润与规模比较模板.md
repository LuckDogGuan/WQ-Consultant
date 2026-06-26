# Machine Alpha 基础知识2：理解时间序列利润与规模比较模板

- **链接**: [L2] Machine Alpha 基础知识2理解时间序列利润与规模比较模板.md
- **作者**: WL13229
- **发布时间/热度**: 1 year ago, 得票: 32

## 帖子正文

以下是一个简单的模板实现，用来比较一家公司的盈利能力与其资本化水平。

该模板后面隐含的假设是，如果一家公司的基本面绩效比率与之前相比有所增加，其股价可能会上涨。

> *time_series_operator* (<profit_field>/<size_field>, <days>)

实现方式：

使用时间序列运算符和两个基本指标的比率 profit_field是代表收入/盈余/利润的任何字段 size_field是代表公司规模的任何字段。

days需要使用合理的天数参数，例如周（5天）、月（20天）、季（60天）或年（250天） ✨你能想到扩展这个模板的不同方式吗？在下方评论分享你的想法吧！

---

## 讨论与评论 (20)

### 评论 #1 (作者: HZ76661, 时间: 1 year ago)

ts_rank(<profit_field>/<size_field>, 252)
假如有10家公司，对每家公司的一年的 基本面绩效比率 进行排序，
然后根据每一天10家公司的基本面绩效比率计算投资权重，
不知道回答的对不对，请指正

但貌似没有包含，某家公司的比率比N多天这家公司的比率增加 这个概念

---

### 评论 #2 (作者: HZ76661, 时间: 1 year ago)

ts_delay(<profit_field>/<size_field>, <days>)
days 需要便利尝试，因为无法准确获知，公司基本面绩效比率增加的时间

---

### 评论 #3 (作者: JL97920, 时间: 1 year ago)

这个模板展现了时间维度上的公司排名，但是各行业绩效水平不同，下一步应该是用group在各个维度上进行遍历

---

### 评论 #4 (作者: TS96358, 时间: 1 year ago)

ts_zscore((<profit_field>/<size_field>,250))
可以用来衡量一年内盈利/规模的异常程度，也就是现在相对与过去的值是高还是低

---

### 评论 #5 (作者: YH82809, 时间: 1 year ago)

这个模版在时间序列上盈利水平，再结合子行业的排名，来反应公司未来股价的上涨空间。以此可以展开的是，公司员工的状况，员工的平均工资的状况，销售额的变化，现金流持续变化，债务的变化等方面来反应公司未来的盈利能力，从而判断公司股价的未来上升空间。我这样理解对吗

---

### 评论 #6 (作者: WS48176, 时间: 1 year ago)

公司分短期盈利价值和中长期盈利价值，短期盈利价值按季度来体现，因为公司每季度会公布一次业绩报表，中期盈利价值按年度来体现，因为每年度会公布一次年度业绩报表，长期盈利价值可以把这两年或近几年的业绩进行对比，评价它的投资潜力

---

### 评论 #7 (作者: WS48176, 时间: 1 year ago)

32169702556439

---

### 评论 #8 (作者: TC20311, 时间: 1 year ago)

感觉拿bucket(rank(<size_field>), range="0.1,1,0.1")做个分组会稳当一点？
甚至想要双重分组
group_neutralize(
    group_neutralize(
        time_series_operator(profit_field/size_field, days),
        industry
    ),
    size_bucket) 哈哈

)

---

### 评论 #9 (作者: HX40615, 时间: 1 year ago)

[TC20311](/hc/en-us/profiles/31484220422423-TC20311)

可以看看group_cartesian_product，可以满足两层分组需求。

group_cartesian_product ：Merge two groups into one group. If originally there are len_1 and len_2 group indices in g1 and g2, there will be len_1 * len_2 indices in the new group.

---

### 评论 #10 (作者: RY94687, 时间: 11 months ago)

借用ts96358兄弟的盈利异常程度的思路：

group_mean(ts_zscore(profit_field/cap,125),industy)

减少盈利异常计算时间至半年，因为异常时间一年未免有点长了，加入industy消除行业的对结果的影响

---

### 评论 #11 (作者: KL35691, 时间: 10 months ago)

新人弱弱的问一句这个“基本面绩效比率与之前相比有所增加” 中计算的基本面绩效比率 <profit_field>/<size_field> 一定会是线性的吗？有没有可能是非线性的？比如<profit_field>随<size_field>增加越难以线性增加？所以也可能是 *time_series_operator* (<profit_field>/transform_operator(<size_field>), <days>). 请老师指点

---

### 评论 #12 (作者: ZW59625, 时间: 10 months ago)

days需要遍历不同的情况吧，以遍从短中期来判断

---

### 评论 #13 (作者: LL84811, 时间: 10 months ago)

profit_field/size_field是 **一个**  **绝对比率，从静止到动态** ，可 **扩展为**  **比率的变化率或趋势** ，更直接反映         "基本面绩效是否改善"：​

- #### 计算「当前比率」与「过去 n 天平均比率」的差值或比值：​

```
       time_series_operator((current(profit/size) - mean(profit/size, days)) / mean(profit/size, days), days)​       意义：衡量比率的相对增长幅度，避免绝对值受行业基准差异的影响。​
```

- #### 加入比率的一阶导数（变化速度）

```
      time_series_operator(Δ(profit/size)/Δt, days)​      意义：捕捉比率上升 / 下降的速度，速度越快可能预示股价反应越强烈。
```

---

### 评论 #14 (作者: JC31003, 时间: 7 months ago)

小白跟着老师学习到这里了，收货量多

---

### 评论 #15 (作者: XW23690, 时间: 7 months ago)

看了评论同学给了相对变化率以及一阶差分的拓展，我接着再拓展一些：

- 比率的二阶差分（加速度）

比如速度从 0.2%/ 天升到 0.5%/ 天，加速度为正，说明改善在 “加速”；速度从 0.5%/ 天降到 0.3%/ 天，加速度为负，说明改善在 “减速”。​

```
speed=Δ(profit/size)/Δt;accel_speed=Δ(speed)/Δt
```

- 比率变化的稳定性

比率涨了但波动大（比如今天涨 3%、明天跌 2%），说明改善不稳定；波动小则说明改善可靠。用 “变异系数量化波动性，结合变化率判断 “改善的质量”。

```
 CV=ts_mean(Δ(profit/size),days)/ts_std_dev(Δ(profit/size),days)
```

---

### 评论 #16 (作者: YW71867, 时间: 7 months ago)

ts_rank(<profit_field>/<size_field>, <days>)
相对于过去利润有上升趋势的股票
ts_zscore(<profit_field>/<size_field>, <days>)
相对于过去利润有上升趋势的股票，且上升越高投资权重越大

<group_operator/>(<ts_operator>(<profit_field>/<size_field>,<days>),industry)
在同行业内，相对于过去利润有上升趋势的股票（行业利润不一样）

---

### 评论 #17 (作者: CC21336, 时间: 6 months ago)

接触WQ快一年了，回头看这个 “利润/规模” 的用法的确是个出货率非常高的模版。

可以 fnd ; 可以 anl 等等 都可试着去除一个规模相关的字段，往往有意想不到的惊喜。

---

### 评论 #18 (作者: GG53278, 时间: 2 months ago)

那就举个相反的例子，假如负债比上规模之类的字段，也是一个alpha模板，值相比上个周期变小说明单位资产对应的负债越来越少，公司越来越好。time_series_operator(<liabilities_field>/<size_field>, <days>)

---

### 评论 #19 (作者: JM87824, 时间: 2 months ago)

这个因子的本质是用动态的目光来看公司的基本面因子，也就是看它的趋势，而不是只看某一个节点上熟知的绝对大小，对于参数的选择也不是单纯上的参数遍历，而是不同的时间窗口对应了不同的逻辑：短周期（5-20天）：对应事件驱动；中周期（60天）：对应经营周期；长周期（250天）：对应战略转型或宏观周期
一些想法：1.不同的行业profit/size差异比较大，所以我们应该先在行业内做标准化，解决跨行业可比问题
2.一阶变化也就是比率本身波动可能比较大，我们可以通过计算比率的变化率ts_delta(profit/size, 5) / ts_mean(profit/size, 5)，也就是看“盈利效率的增长速度”是不是在加快

---

### 评论 #20 (作者: AQ66932, 时间: 1 month ago)

模板假设：一家公司的基本面绩效比率与之前相比有所增加，其股价可能会上涨。

1、可以扩展这个假设：一家公司的基本面绩效比率与之前相比有所增加同时这家公式的估值低于同行业平均水平，然后根据这个假设提出新的模板
time_series_operator(<profit_field>/<size_field>, <days>)*valuation_discount_factor

2、也可以针对该模板进行细化，比如增加判断项，<profit_field>的变化大于0

---

