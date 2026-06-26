# Operator大师-用基础的operator实现复杂功能

- **链接**: [Commented] Operator大师-用基础的operator实现复杂功能.md
- **作者**: WL13229
- **发布时间/热度**: 1年前, 得票: 59

## 帖子正文

集思广益，在目前自己已有的operator权限下，提出组合的尝试，延申目前已有operator的边界。评论请附上用例. [运算符和函数手册中文版 – WorldQuant BRAIN](/hc/en-us/community/posts/32340683206423-%E8%BF%90%E7%AE%97%E7%AC%A6%E5%92%8C%E5%87%BD%E6%95%B0%E6%89%8B%E5%86%8C%E4%B8%AD%E6%96%87%E7%89%88)

例如

group_zscore

```
group_zscore = (alpha - group_mean(alpha, market)) / group_std_dev(alpha, market)
```

有的人没有std,可以

```
group_zscore = (alpha - group_mean(alpha, market)) / power(power(alpha - group_mean(alpha, market), 2), 0.5)
```

---

## 讨论与评论 (42)

### 评论 #1 (作者: PN39025, 时间: 1年前)

尝试： 将  **ts_zscore**  和  **ts_partial_corr**  结合，先对时间序列标准化处理，再计算其与其他变量的部分相关性，消除数值尺度的影响。
用例： 在研究 **石油价格** 对 **航空股** 的影响时，使用  **ts_zscore**  标准化航空股和石油价格时间序列数据，然后用  **ts_partial_corr**  控制市场指数的影响，得出石油价格对航空股的净影响。

我有以下这个 **提议** ，希望大家可以参考或补充意见！

---

### 评论 #2 (作者: YB15978, 时间: 1年前)

请问是网页更新了吗，昨天还能查看很多的operator, 今天看不到了

---

### 评论 #3 (作者: KS24487, 时间: 1年前)

Here is an implementation of ts_regression:

```
n=group_count(x, market); b = (n * ts_sum(x*y,lookback) - ts_sum(x,lookback) * ts_sum(y,lookback)) / (n * ts_sum(x^2,lookback) - ts_sum(x,lookback)^2);
```

However, some people (including me) don't have group_count any more, so you might need to manually specify n as the number of instruments in the universe for each alpha, ie 3000 for USA/TOP3000. 

The resulting b is the beta measure and should equal this:

```
b = ts_regression(y, x, lookback, lag=0, rettype=2);
```

---

### 评论 #4 (作者: WP88606, 时间: 1年前)

less = not(A>=B)

没有log却有s_log_1p，这个好像更复杂

---

### 评论 #5 (作者: OS30886, 时间: 1年前)

计算ts_corr:

a= close;

b = open;

p = 5;

c = ts_mean(ts_av_diff(a,p)*ts_av_diff(b,p),p);

c/ts_std_dev(a,p)/ts_std_dev(b,p)

不过没理解错的话我觉得是有一点出入的，因为这里的ts_av计算的是每天值减去每天的均值，而非p天内固定的均值

---

### 评论 #6 (作者: ZW48988, 时间: 1年前)

这题我会，我的sqrt(x)被禁了，我换成了power(x,0.5)…

---

### 评论 #7 (作者: TL72031, 时间: 1年前)

[YB15978](/hc/en-us/profiles/28855468991639-YB15978) 
是啊，他们根据我们的Genius level 限制我们看到的operators和data

---

### 评论 #8 (作者: YC92090, 时间: 1年前)

根据  [https://support.worldquantbrain.com/hc/en-us/community/posts/9672576065943--BRAIN-TIPS-How-does-regression-neut-work](https://support.worldquantbrain.com/hc/en-us/community/posts/9672576065943--BRAIN-TIPS-How-does-regression-neut-work)  这篇文提到的regression_neut(Y, X)定义，尝试：

# Step 1: 计算横截面均值

mean_Y = vec_avg(Y);

mean_X = vec_avg(X);

# Step 2: 计算协方差和方差

cov_YX = vec_avg(multiply(subtract(Y, mean_Y), subtract(X, mean_X)));

var_X = vec_avg(power(subtract(X, mean_X), 2));

# Step 3: 计算回归系数 a 和 b

b = divide(cov_YX, var_X);

a = subtract(mean_Y, multiply(b, mean_X));

# Step 4: 计算回归估计值

Y_estimation = add(a, multiply(b, X));

# Step 5: 计算中性化结果

Y_neutralized = subtract(Y, Y_estimation);

但是执行时会遇到以下错误，想请问是否哪里撰写的不正确
WorldQuant BRAIN is experiencing some difficulties. Please contact support if this problem persists.

---

### 评论 #9 (作者: WP88606, 时间: 1年前)

ts_min(x, 20) = min(ts_delay(x, 1), ts_delay(x, 2), ts_delay(x, 3), ts_delay(x, 4), ts_delay(x, 5), ts_delay(x, 6), ts_delay(x, 7), ts_delay(x, 8), ts_delay(x, 9), ts_delay(x, 10), ts_delay(x, 11), ts_delay(x, 12), ts_delay(x, 13), ts_delay(x, 14), ts_delay(x, 15), ts_delay(x, 16), ts_delay(x, 17), ts_delay(x, 18), ts_delay(x, 19), ts_delay(x, 20))

---

### 评论 #10 (作者: WP88606, 时间: 1年前)

log_diff(x) = ts_delta(log(x), 1)

---

### 评论 #11 (作者: DN41247, 时间: 1年前)

Thank you, it's such a great explanation, hence I can custom `group_zscore` by using `group_median`, ... and increase operators used in Genius!

---

### 评论 #12 (作者: KJ42842, 时间: 1年前)

[YC92090](/hc/en-us/profiles/28073763357335-YC92090)

vec_avg 是对 vector类型数据字段的操作，横截面的均值可以用group_mean(x, market)。

---

### 评论 #13 (作者: TL72031, 时间: 1年前)

s_log_1p(x) = if_else(sign(x)==-1,-log(1+abs(x)),log(1+abs(x)))

---

### 评论 #14 (作者: XJ47364, 时间: 1年前)

这个思维训练很有意义，但是现在看不到被禁用的运算符名称和说明，凭删内容之前有限的一点记忆很难参加这个活动。老师要是能针对用户权限出几道题就好了。

---

### 评论 #15 (作者: PZ64174, 时间: 1年前)

ts_decay_linear(-fraction(winsorize(ts_backfill(anl4_adjusted_netincome_ft,115),std=4)),10)

fraction无法使用之后我换成了

ts_decay_linear(-densify(zscore(winsorize(ts_backfill(anl4_adjusted_netincome_ft,115),std=4))),10)

但是会有个 WARNING ：Incompatible unit for input of "densify" at index 0, expected "Unit[Group:1]", found "Unit[]"

---

### 评论 #16 (作者: AN57408, 时间: 1年前)

exp(x) equal to e^x = 2.71828182846^x

you can use the following operators with similar functionality:

> exp(x) = signed_power(2.7182, x)

---

### 评论 #17 (作者: AN57408, 时间: 1年前)

To replace 's_log_1p', you can use the following operators with similar functionality:

> s_log_1p(x) = sign(x) * (log( 1 + abs(x)))

---

### 评论 #18 (作者: BY50972, 时间: 1年前)

Thank you,

good explanation group_mean increase operators used in Genius level

---

### 评论 #19 (作者: RP41479, 时间: 1年前)

Thanks! I can customize  `group_zscore`  with  `group_median`  and expand operator usage in Genius!

---

### 评论 #20 (作者: HN71281, 时间: 1年前)

这是一个很好的思路，利用已有 operator 组合出更复杂的功能，突破单一 operator 的局限性。特别是  `ts_zscore`  与  `ts_partial_corr`  的结合，有助于消除尺度影响并控制市场指数，提升相关性分析的准确性。或许可以进一步探索滚动窗口、非线性相关性（如  `rank_corr` ），或者引入更多控制变量，以提升分析的稳健性.

---

### 评论 #21 (作者: DM28368, 时间: 1年前)

group operators are quite difficult for me. I have read the explanation of these operators but I have not been able to implement them effectively. Are these operators not powerful enough or am I doing it wrong?

---

### 评论 #22 (作者: WL27618, 时间: 1年前)

```
{data}-ts_max_diff({data},{d}) #ts_max
```

```
(({data}-ts_max_diff({data},{d}))*ts_scale({data},{d})-{data})/(ts_scale({data},{d})-1)  #ts_min
```

---

### 评论 #23 (作者: PX70901, 时间: 1年前)

vector_ne这个怎样弄

---

### 评论 #24 (作者: TD37298, 时间: 1年前)

该公式是否适用于非正态分布的组？如果数据不服从正态分布，是否有标准差的替代方法？

---

### 评论 #25 (作者: WL27618, 时间: 1年前)

```
weight = {d}+ts_step(0);ts_sum({data}*weight,{d})/ts_sum(weight,{d}) #ts_decay_linear
```

虽然linear decay大家都有, 其他filter都可以这么制作, 改weight就可以. 我等级低也没法验证是否完全一致

---

### 评论 #26 (作者: HH63454, 时间: 10个月前)

很受启发！我尝试在  `group_zscore`  的思路上，用  `median`  替代  `mean` ，在小样本或非正态分布下可能更稳健：
 `group_zscore_median = (alpha - group_median(alpha, market)) / power(power(alpha - group_median(alpha, market), 2), 0.5)`

另外，如果想进一步降低极端值影响，可以先做 winsorize 再计算，这样组合 operator 的思路会更灵活，也方便在权限受限的情况下拓展功能。

---

### 评论 #27 (作者: BL59154, 时间: 10个月前)

ts_min可以用以下表达式替代：（ts_max同理）

```
ts_min({datafield}, {days}) = ts_backfill(if_else(ts_arg_min({datafield}, {days})==0, {datafield}, nan), 120)
```

---

### 评论 #28 (作者: SG46247, 时间: 10个月前)

ts_backfill(quantile(ts_mean({data_field}, 40)), {decay})

持续性趋势过滤：40日均值的分位数变换加回填机制，中期均值平滑短期波动，回填减少频繁调仓。

ts_mean(ts_rank({data_field}, {decay}), {decay})

三重平滑信号:n日排名的n日均值平滑,双重平滑机制大幅降低信号噪声和换手率。

ts_mean(ts_rank({data_field}, {decay}), {decay1})/ts_mean(ts_rank({data_field}, {decay}), {decay2})

decay1 与decay2  一个长期如（5，20，60）一个短期如（60，120，250）

---

### 评论 #29 (作者: SF42622, 时间: 10个月前)

建议给新人也有ts_min 和 ts_max 函数的权限吧，这两个很普通也很重要，缺这两个，很多因子实现不了

---

### 评论 #30 (作者: SF42622, 时间: 10个月前)

[BL59154](/hc/en-us/profiles/29675125860631-BL59154)

你的公式确定吗？感觉不太对啊

```
ts_min({datafield}, {days}) = ts_backfill(if_else(ts_arg_min({datafield}, {days})==0, {datafield}, nan), 120)
```

---

### 评论 #31 (作者: WL27618, 时间: 10个月前)

```
group_normalize({data},{group}) = {data}/(group_sum(abs({data}),{group}))
```

===============================================================================

---

### 评论 #32 (作者: FZ85649, 时间: 9个月前)

老师还有operator中文手册了吗？这个文章中文手册链接失效了。谢谢

---

### 评论 #33 (作者: CC85858, 时间: 9个月前)

signed_power(alpha,a)，当a为奇数的时候signed_power(alpha,a)和power(alpha,a)是等价的

当a为偶数时，signed_power(alpha, a)等价于                                                                                                    if_else ( alpha > 0, power (alpha , a ), - power ( alpha , a ))

---

### 评论 #34 (作者: BZ88812, 时间: 9个月前)

下面这个公式是对的吗，跟我印象中的中性化不一样group_normalize({data},{group}) = {data}/(group_sum(abs({data}),{group}))

---

### 评论 #35 (作者: CC85858, 时间: 9个月前)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

FZ85649                                                                                                                                                                 网站的平台导航栏learn下有一个operator，里面有操作符的详细解释

---

### 评论 #36 (作者: CC85858, 时间: 9个月前)

BZ88812                                                                                                                                                              你是不是将group_normalize和group_neutralize操作符弄混了

---

### 评论 #37 (作者: SQ98290, 时间: 8个月前)

没想到还能这样组合，即使成为了顾问也还是有很多没懂的地方，看来多学习是正确的

---

### 评论 #38 (作者: BZ88812, 时间: 8个月前)

[CC85858](/hc/en-us/profiles/29142660537879-CC85858)    谢谢，是的

---

### 评论 #39 (作者: DL74068, 时间: 8个月前)

ts_max(x,d)=ts_delay(x,ts_arg_max(x,d));

---

### 评论 #40 (作者: JQ70858, 时间: 8个月前)

感谢老师的指点，用可用的现有的操作符实现现阶段没有的操作符的功能，既能解决想要到达理想运算的效果，有时候也能提供一些新的思路，一举两得。

---

### 评论 #41 (作者: RZ39578, 时间: 7个月前)

计算当天事件数量： vec_sum(datafiled)/vec_avg(datafield). 感觉蛮有用的，如果是新闻数据可以用来看当天热度。

---

### 评论 #42 (作者: MY65447, 时间: 2个月前)

读了这篇文章，很有收获，深受启发，发现要学的还很多。感谢大佬分享！

==============================================================

Keep going every day, and you will surely reap greater rewards

==============================================================

---

