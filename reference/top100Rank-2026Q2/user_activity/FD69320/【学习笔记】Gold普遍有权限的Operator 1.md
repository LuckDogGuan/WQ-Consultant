# 【学习笔记】Gold普遍有权限的Operator 1

- **链接**: 【学习笔记】Gold普遍有权限的Operator 1.md
- **作者**: FD69320
- **发布时间/热度**: 1年前, 得票: 33

## 帖子正文

## 1. ts_zscore

***功能说明*** ：计算时间序列的Z-score标准化值。
 ***参数说明*** ：

- - x: 输入数据
- - d: 回看天数

Z-score定义：Z-score(标准分)是一个统计学概念，表示一个观测值与平均值的偏离程度，以标准差为单位。

Z-score = (原始值 - 均值) / 标准差

假设我们有一只股票最近5天的收盘价：100,102,101,103,99

1. 均值 = (100 + 102 + 101 + 103 + 99) / 5 = 101元
2. 差值平方：(100-101)² + (102-101)² + (101-101)² + (103-101)² + (99-101)²
       = 1 + 1 + 0 + 4 + 4 = 10
3. 标准差 = √(10/5) ≈ 1.414元

- z-score为负表示低于平均水平
- z-score为正表示高于平均水平
- |z-score| 越大表示偏离程度越大

***使用示例：***

```
# 基于均值回归的反转策略-ts_zscore(returns, 5)  # 短期超涨/超跌反转# 均值回归策略-ts_zscore(close/ts_delay(close,1) - 1, 5)  # 短期收益率均值回归
```

## 2. ts_rank

***功能说明*** ：计算时间序列中当前值的历史百分位排名。
 ***参数说明：***

- - x: 输入数据
- - d: 回看天数

***使用示例：***

```
# ts_zscore和ts_rank的区别# ts_zscore关注偏离程度ts_zscore(returns, 20)  # 收益偏离标准差# ts_rank关注相对位置ts_rank(returns, 20)    # 收益历史分位
```

## 3. group_neutralize

***功能说明*** ：按组别对数据进行中性化处理。

> group_neutralize(x, group) = x - group_mean(x, 1, group)

***参数说明：***

- - x: 输入数据
- - group: 分组变量

***实际应用场景：***

```
# 1. 消除行业效应 # 当我们想要获得行业中性的纯因子暴露时：# 获取行业中性的ROE因子pure_roe = group_neutralize(fnd23_roe, industry)# 获取行业中性的动量因子pure_momentum = group_neutralize(ts_rank(returns, 20), industry)# 2. 消除规模效应# 当我们想要消除大小市值的系统性影响：# 按市值五分组进行中性化size_neutral = group_neutralize(alpha_signal,    bucket(rank(market_cap), range="0,1,0.2")  # 市值五分组)
```

## 4. bucket

***功能说明*** ：将连续变量转换为用户指定的分组索引。这个operator将浮点值转换为可以传递给group操作符的分组值。
 ***参数说明：***

- - x: 输入值，通常是rank后的连续变量
- - range="start, end, step": 指定等距分组
- - start: 起始值
- - end: 结束值
- - step: 步长
- - buckets="num_1,num_2,...,num_N": 指定自定义分组边界

- - skipBegin: 是否移除(-inf, start]的默认分组
- - skipEnd: 是否移除[end, +inf)的默认分组
- - skipBoth: 同时设置skipBegin和skipEnd为true
- - NANGroup: 是否将NAN值分到单独的组（索引值将是最后一个bucket之后的值）
- 使用示例：

***使用示例：***

```
# 示例1: 使用range参数进行等距分成5组bucket(rank(market_cap), range="0,1,0.2")# 示例2: 使用buckets参数进行自定义分成5组，去掉极值bucket(rank(fnd23_pe), buckets="0.2,0.4,0.6,0.8",    skipBoth=True  # 去除两端极值)# 示例3: 处理NaN值bucket(rank(market_cap), range="0,1,0.25",    NANGroup=True  # NaN值单独分组)
```

## 5. trade_when

***功能说明*** ：条件性交易操作符。当条件满足时执行交易信号，不满足时返回0。用于设置交易条件或过滤交易信号。

***参数说明：***

- - x=triggerTradeExp: 交易触发条件
- - y=AlphaExp: Alpha表达式
- - z=triggerExitExp: 退出触发条件（可选）

***执行逻辑：***

- - 如果 triggerExitExp > 0，则 Alpha = NaN
- - 否则，如果 triggerTradeExp > 0，则 Alpha = AlphaExp
- - 否则，Alpha = previousAlpha（保持前一天仓位）

***使用示例：***

```
# 示例1: 基本使用 - 成交量条件trade_when(    volume >= ts_mean(volume, 5),  # 交易触发条件    rank(-returns)                 # Alpha表达式-1   # 无退出条件（因为-1永远不>0）)  # 示例2: 带退出条件trade_when(    volume >= ts_mean(volume, 5),  # 交易触发条件    rank(-returns),                # Alpha表达式    abs(returns) > 0.1             # 退出条件：收益率绝对值大于10%)# 示例3: 使用5日均量作为条件trade_when(    volume >= ts_mean(volume, 5),   # 当日成交量大于5日均量    rank(-returns),                 # Alpha表达式    -1                              # 永不退出（因为-1永远不>0）)
```

## 6. if_else

***功能说明*** ：条件执行操作符。如果条件为真返回Alpha_expression_1，为假返回Alpha_expression_2。

***参数说明：***

- - event_condition: 条件表达式
- - Alpha_expression_1: 条件为真时的Alpha表达式
- - Alpha_expression_2: 条件为假时的Alpha表达式

***使用示例***

```
# 假设：# 1. 如果股票过去2天价格上涨，未来可能下跌# 2. 如果当前成交量高于月均量，回归效应可能更强# 实现方案if_else(    volume > ts_mean(volume, 20),          # 当前成交量高于20日均量    ts_delta(close, 3) * (-2),             # 强化反转信号（2倍）    ts_delta(close, 3) * (-1)              # 普通反转信号)
```

```
# 使用if_else等价替换trade_when# trade_when版本trade_when(    volume > ts_mean(volume, 5),    alpha_signal)# if_else版本if_else(    volume > ts_mean(volume, 5),    alpha_signal,    ts_delay(alpha_signal, 1))
```

## 7. ts_delay

***功能说明*** ：返回x在d天前的值。
 ***参数说明* ：**

- - x: 输入值
- - d: 回看的天数

> ts_delta(x, d) = x - ts_delay(x, d)

> ts_delay(x, d) = x - ts_delta(x, d)

***使用示例***

```
# 示例1: 获取前一天的收盘价ts_delay(close, 1)  # 等同于close - ts_delta(close, 1)# 示例2: 获取5天前的成交量ts_delay(volume, 5)  # 等同于volume - ts_delta(volume, 5)# 示例3: 计算与历史值的差值close - ts_delay(close, 1)  # 等同于ts_delta(close, 1)
```

## 8. ts_quantile

***功能说明*** ：计算时间序列的分位数，并应用指定分布的反累积密度函数。

***参数说明：***

- - x: 输入值
- - d: 时间窗口
- - driver: 分布类型（可选）

> - "gaussian": 高斯分布（默认）- "uniform": 均匀分布- "cauchy": 柯西分布

***使用示例***

```
# 当波动率处于高分位时退出，成交量处于高分位时交易trade_when(    ts_quantile(volume, 20, "gaussian") > 0.8,        # 成交量在20天内处于前20%时交易    alpha_signal,                                     # 原始信号    ts_quantile(volatility, 60, "gaussian") > 0.9     # 波动率在60天内处于前10%时退出)
```

## 9. hump

***功能说明*** ：限制输入值的变化频率和幅度，从而减少换手率（turnover）。

***工作原理：***

- - 如果今天的值相比昨天的变化很小（不超过阈值hump），输出保持与昨天相同
- - 如果变化超过阈值，输出为昨天的值加上或减去阈值（根据变化方向）

> 今天的值 vs 昨天的值
> ↓
> 变化是否超过阈值hump？
> ↓
> 是 → 昨天的值 ± hump（根据变化方向）
> 否 → 保持昨天的值

***使用示例：***

```
# 示例1：限制alpha信号的变化hump(alpha_signal, 0.01)  # 限制信号变化在1%以内# 示例2：结合trade_when使用trade_when(    volume > ts_mean(volume, 20),    hump(alpha_signal, 0.02),  # 高成交量时允许2%的变化    hump(alpha_signal, 0.005)  # 低成交量时只允许0.5%的变化)
```

## 10. ts_target_tvr_hump

***功能说明：*** 自动调整hump参数，使信号的换手率（turnover）达到目标值。这是一个自适应版本的hump。

***参数说明：***

- - x: 输入信号（必需）需要控制换手率的原始信号
- - lambda_min: 最小hump阈值（可选）允许的最小变化限制
- - lambda_max: 最大hump阈值（可选）允许的最大变化限制
- - target_tvr: 目标换手率（可选）期望达到的换手率水平

***使用示例：***

```
# 示例1：使用默认参数ts_target_tvr_hump(alpha_signal)  # 目标10%换手率# 示例2：指定目标换手率ts_target_tvr_hump(alpha_signal, target_tvr=0.05)  # 目标5%换手率# 示例3：完整参数设置ts_target_tvr_hump(    alpha_signal,    lambda_min=0.001,  # 最小变化限制0.1%    lambda_max=0.05,   # 最大变化限制5%    target_tvr=0.15    # 目标15%换手率)
```

---

## 讨论与评论 (3)

### 评论 #1 (作者: ST61360, 时间: 1年前)

非常好的内容输出，收藏了。谢谢分享。

---

### 评论 #2 (作者: SQ98290, 时间: 7个月前)

真是宝藏内容，这么好的文章还有四篇，非常感谢楼主的分享

这种运用具体数学例子的方式让我更加了解了该操作符到底是在做什么的操作机理

之前的认识最多就到官方提供的例子和这个操作符的中文翻译内容

所以我对具体到每支股票的操作是完全懵的状态

这些内容也将启发我以后使用操作符的使用，从具体的运算方式去思考

而不再是简单的堆砌使用

祝你继续gm，vf月月1.0

---

### 评论 #3 (作者: MM27120, 时间: 5个月前)

分享的内容很有料

关注一波

真的是能帮助到现在的我

感谢

---

