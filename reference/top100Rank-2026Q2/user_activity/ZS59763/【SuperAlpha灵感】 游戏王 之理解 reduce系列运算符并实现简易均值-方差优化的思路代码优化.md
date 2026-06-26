# 【SuperAlpha灵感】 <游戏王> 之《理解 reduce系列运算符并实现简易均值-方差优化的思路》代码优化

- **链接**: 【SuperAlpha灵感】 游戏王 之理解 reduce系列运算符并实现简易均值-方差优化的思路代码优化.md
- **作者**: ZS59763
- **发布时间/热度**: 1年前, 得票: 85

## 帖子正文

如题，sac比赛催生出了很多很多好用的select和combo。但注意到在combo中，reduce系列的运算符并未被广泛提及，本文介绍reduce系列运算符的具体用法，给出简单的例子加以佐证，最后利用reduce系列实现简易的均值-方差优化实现思路以及初步实验结果。

Acknowledgments：

- 使用kimi进行辅助；
- 复现灵感来自于《因子投资：方法与实践》一书；
- 后续会尝试复现书中更有意义的combo；
- 感谢AK哥（AK76468）的帮助。

Warning：

- 鉴于能力有限，本文部分内容难免 **存在错误** ，对于均值-方差优化的推导严谨度严重缺乏。 **非文责自负，仅供观赏** 。

***什么是reduce？***

归约（reduction）操作，用于对输入矩阵的最后一个维度进行计算（从sa的角度来说，是对新一日的数据进行计算，后进行权重分配并进行投资）。

***如何理解reduce？***

我们以reduce_avg为例，按照定义解释如下：

- **作用** ：对输入矩阵的最后一个维度（即最后一轴）上的元素求平均值。
- **忽略 NaN 值** ：在计算平均值时，会自动跳过  `NaN` （非数字）值。
- **支持维度** ：
  - 如果输入是  **2D 矩阵**   `(D x N)` ，输出是  `(D x 1)` 。
  - 如果输入是  **3D 矩阵**   `(D x N x N)` ，输出是  `(D x N x 1)` 。
- **threshold 参数** ：用于设置 **最少需要多少个非 NaN 值** 才能计算平均值，否则返回 NaN。

***参数说明：*** input` 输入的 2D 或 3D 矩阵
threshold`最少需要的非 NaN 值数量（默认是 0，表示不限制

***举例：*** 2D 输入矩阵  `(D x N)`

```
input = [[1.0, 2.0, NaN],
         [3.0, NaN, 5.0]]
```

- 对每一行（最后一个维度）求平均值，忽略 NaN：
  - 第一行： `[1.0, 2.0]`  → 平均值 =  `(1 + 2) / 2 = 1.5`
  - 第二行： `[3.0, 5.0]`  → 平均值 =  `(3 + 5) / 2 = 4.0`
- 输出： `[[1.5], [4.0]]`  → 形状为  `(2 x 1)`

#### ***举例*** ：threshold = 2

```
input = [[1.0, NaN, NaN],
         [3.0, 4.0, NaN]]
```

- 第一行只有一个有效值，不满足 threshold=2 → 输出 NaN
- 第二行有两个有效值，满足 threshold → 平均值 =  `(3 + 4) / 2 = 3.5`
- 输出： `[[NaN], [3.5]]`

***其他操作符的含义：***

 `reduce_choose(input, nth, ignoreNan=true)` 

选择每行（或每层）中第  `nth`  个元素（排序后）， `ignoreNan`  控制是否忽略 NaN。

 `reduce_count(input, threshold)` 
统计每行中 **大于 threshold**  的元素个数。

 `reduce_ir(input)` 
计算每行中值的 **信息比率（Information Ratio）** 。

 `reduce_kurtosis(input)` 
计算每行中值的 **峰度（Kurtosis）** ，衡量分布的尖峭程度。

 `reduce_max(input)` 
返回每行中的 **最大值** 。

 `reduce_min(input)` 
返回每行中的 **最小值** 。

 `reduce_norm(input)` 
返回每行中元素的 **绝对值之和** （L1 范数）。

 `reduce_percentage(input, percentage=0.5)` 
返回每行中排序后的 **百分位数** （默认是中位数）。

 `reduce_powersum(input, constant=2, precise=false)` 
返回每行中元素的 **常数次幂之和** ，默认是平方和。

 `reduce_range(input)` 
返回每行中值的 **范围（最大值 - 最小值）** 。

 `reduce_skewness(input)` 
计算每行中值的 **偏度（Skewness）** ，衡量分布的不对称性。

 `reduce_stddev(input, threshold=0)` 
计算每行中值的 **标准差** ，可设置最小有效值比例。

 `reduce_sum(input)` 

返回每行中所有元素的 **和** 。

***均值方差优化***

均值-方差优化（Mean-Variance Optimization, MVO）是一种投资组合优化方法，由哈里·马科维茨（Harry Markowitz）在1952年提出，是现代投资组合理论（Modern Portfolio Theory, MPT）的核心。其目标是在给定风险水平下最大化预期收益，或在给定收益水平下最小化风险。

### **核心概念**

1. **均值（Mean）**
   指投资组合中各资产的 **预期收益率** 的加权平均值，反映收益潜力。
2. **方差（Variance）**
   衡量资产收益率的波动程度（风险），方差越大，风险越高。投资组合的方差不仅取决于单个资产的方差，还受资产间 **协方差** （相关性）影响。
3. **有效前沿（Efficient Frontier）**
   在风险-收益坐标系中，所有最优组合构成的曲线。曲线上的组合满足：
   - 相同风险下收益最高，或
   - 相同收益下风险最低。

简易版均值-方差优化实现思路（这里没有加入权重，推测权重可以通过回归运算符获得）

stats=generate_stats(alpha);

expected_returns = reduce_avg(self_corr(stats.returns,252), threshold=0);

demeaned_returns = stats.returns - expected_returns;

covariance_matrix = reduce_sum(self_corr(demeaned_returns* demeaned_returns ,252));

portfolio_return = reduce_sum(self_corr(expected_returns,252));

portfolio_variance = reduce_sum( (self_corr(covariance_matrix ,252)));

portfolio_return/sqrt(portfolio_variance)

实验结果（权重按1计算，本人因子，默认统计中性化）:

![图片](images/img_a9451aa653.png)

![图片](images/img_18897efcd4.png)

![图片](images/img_b2f362fbaf.png)

副产物：按照sharpe比率对于因子进行加权的combo：

stats=generate_stats(alpha);

portfolio_return = ts_sum(stats.returns,252);

portfolio_stddev = ts_std_dev(stats.returns,252);

portfolio_return / portfolio_stddev

实践结论：在本人因子中，usa，eur比等权表现较好，asi打平，glb跑输，或有实用性。

![图片](images/img_6fea430485.png)

![图片](images/img_98937c43f7.png)

![图片](images/img_75aa1767f0.png)

![图片](images/img_3528b66319.png)

---

## 讨论与评论 (5)

### 评论 #1 (作者: YW93864, 时间: 1年前)

```
expected_returns = reduce_avg(self_corr(stats.returns,252), threshold=0);
```

这个算出来的不应该是self_corr么，所以接着当你计算

demeaned_returns = stats.returns - expected_returns;

会出现量纲不一致的情况？是这样么

---

### 评论 #2 (作者: JX14975, 时间: 11个月前)

```
expected_returns = reduce_avg(self_corr(stats.returns,252), threshold=0);
```

这段是在算self_corr吧
建议修改为：
expected_returns=normalize(stats.returns)，这才是在算减去平均值后的值。
另外，对reduce运算符的解析非常清晰，很有用

---

### 评论 #3 (作者: AH18340, 时间: 11个月前)

感谢游戏王分享，用起来

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #4 (作者: XC66172, 时间: 11个月前)

【在本人因子中，usa，eur比等权表现较好，asi打平，glb跑输，或有实用性】看到这个突然眼前一亮，目前我还没有跑过combo exp是比等权表现好的（官方推荐的stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr）偶尔能，但和等权走势很雷同。

一般combo exp我都是用来降PC的.. 赶紧试一下游戏王推荐的这两个combo

---

### 评论 #5 (作者: AL13375, 时间: 9个月前)

实测了这个：

```
按照sharpe比率对于因子进行加权的combo：stats=generate_stats(alpha);portfolio_return = ts_sum(stats.returns,252);portfolio_stddev = ts_std_dev(stats.returns,252);portfolio_return / portfolio_stddev实践结论：在本人因子中，usa，eur比等权表现较好，asi打平，glb跑输，或有实用性。
```

有用！！！

本来我就是主做USA的，这个combo真的很不错，相比等权可以有一定程度的优化，还能降低prod！

感谢游戏王大佬！

=*=*=*=*=*=*=路漫漫其修远兮，吾将上下而求索=*=*=*=*=*=*=

---

