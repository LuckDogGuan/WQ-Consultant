# 【本地Corr增强版】本地预估Prod Corr最大值的下限代码优化

- **链接**: 【本地Corr增强版】本地预估Prod Corr最大值的下限代码优化.md
- **作者**: KZ79256
- **发布时间/热度**: 1年前, 得票: 67

## 帖子正文

众所周知，Prod Corr请求的越多，限速越严重，一小时Check不了几个。而本地Self Corr有时候又有点局限。
所以我就打起了之前进行过Prod Corr的Pnl曲线，以期望用这些Pnl曲线进一步预估Prod Corr。

首先，从最简单的例子入手，假设已知变量a和变量b的相关系数为x，变量b和变量c的相关系数为y，则变量a与变量c的相关系数z的范围为 xy-sqrt(1-x^2)sqrt(1-y^2)<= z <= xy+sqrt(1-x^2)sqrt(1-y^2)

类比我们的任务，a其实是Prod Pool里面的某条Pnl，b是一个之前进行过Prod Corr的Pnl曲线，c是我们想求的Pnl曲线。

Prod Pool是由无数条类似的a的Pnl曲线构成的A。之前进行过Prod Corr的Pnl曲线也有很多（构成了数据集B）。由于A和B都有很多线，c和A的相关系数范围很大，而且不好计算（我也不会求bushi，以下是deepseek的解答

![图片](images/img_8a11c3ba01.png)

这个范围起始快接近-1到1了。因此这个范围其实没有什么作用

但是我们关注的是Prod Corr的最大值而非他的范围，尤其是Prod Corr>0.7的。

那么其实我们可以将上述范围的左边界，从取最小值改成取最大值。此时就是预估的Prod Corr的下限

举个不太恰当的例子，假设Prod Pool是个水果市场，我们进行过Prod Corr的是一个水果经销商。我们的任务是批量进一点某种苹果，但是我们不知道该去哪。如果我们在水果经销商处找到了相同品种的，而水果经销商又告诉我们他的水果从水果市场的某个摊位上买的，那就意味着我们到这个摊位上买的话大概率有我们要的水果。只要这个概率高于0.7，我们就去那买。而在我们的corr上，如果这个概率高于0.7，我们就不会进行prod corr检测，而这个概率就是通过最开始的不等式确定的。

至于实践上非常简单，当然首先你得有保存下来的进行过Prod corr的曲线和相应的corr，之后借用我之前的 [本地Self Corr计算代码](本地0误差计算自相关性【即插即用版】代码优化.md) ，计算因子和进行过Prod corr的曲线的相关性，通过不等式获取最小值的集合，取最小值集合的最大值作为本地预估Prod Corr最大值的下限。如果这个下限大于0.7，我们不进行Prod Corr检测。用以减少Check的次数。

```
def calc_prod_min_corr(    alpha_id: str,    know_rets: pd.DataFrame | None = None,    know_corr: pd.Series | None = None,    alpha_result: dict | None = None,    alpha_pnls: pd.DataFrame | None = None):    if alpha_result is None:        alpha_result = cfg.sess.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()    if alpha_pnls is not None:        if len(alpha_pnls) == 0:            alpha_pnls = None    if alpha_pnls is None:        _, alpha_pnls = get_alpha_pnls([alpha_result])        alpha_pnls = alpha_pnls[alpha_id]    # alpha_rets = alpha_pnls.pct_change(axis=0, fill_method=None)    alpha_rets = alpha_pnls - alpha_pnls.ffill().shift(1)    alpha_rets = alpha_rets[pd.to_datetime(alpha_rets.index)>pd.to_datetime(alpha_rets.index).max() - pd.DateOffset(years=4)]    y = know_rets.corrwith(alpha_rets)    corr_min = y*know_corr - np.sqrt(1-know_corr**2)*np.sqrt(1-y**2)    corr_max = y*know_corr + np.sqrt(1-know_corr**2)*np.sqrt(1-y**2)    return corr_min.max()
```

这个过程非常像大家用的Corr的剪枝。

当然我这个东西是不是合理还需要讨论（计算速度和剔除的效率上），或者有其他更好的利用方式也欢迎讨论。

或者多人共建一个已交alpha的pnl库可能更有效率🤣

---

## 讨论与评论 (10)

### 评论 #1 (作者: YW93864, 时间: 1年前)

在 [KZ79256](/hc/en-us/profiles/13609593802263-KZ79256) 大佬的基础上，我补充关于相关性推断的一些例子。

这其实是一道非常非常非常经典的量化面试题。长话短说，我只提示关键的思路，我们所需要的只是一些numerical linear algebra的知识：
1. 简单级别，假设有X, Y, Z三个随机变量，ρX,Z和ρY,Z的相关性都为ρ（它是一个常数，更简单的题中，面试官会告诉你这个ρ具体大小，比如0.5），请问ρX,Y的相关性多少？这种情况下，我们只需要将这些ρ放到相关性矩阵上->相关性矩阵是对称半正定的（symmetric positive semi-definitive），此时使用Sylvester criterion的性质，计算该矩阵leading principal minor的行列式并使它们大于0->求解这些不等式组，我们便得到了ρ的区间

2. 中等级别，这里的rho不一样，即有ρ1，ρ2。您也可以通过上面的方式求解，只是计算量稍微大一点；

3. 难度级别，假设您有n个随机变量，它们的相关系数假设都为ρ，请你求解ρ的区间。在这里我们不能用上述方法，因为n有多少个不确定，也很难计算出行列式。我们可以将这个相关性矩阵拆成ρ1 1^t + (1-ρ)E，这里的1是长度为n的列向量，每个元素都为1，而E是单位矩阵只有主对角线为1，其余元素均为0，根据1 1^t和E的特征值，结合相关性矩阵是半正定的，我们很方便可以解出ρ的区间。

上述题目中，1和2与本贴相关，3是衍生。当随机变量个数固定时，我们确实可以轻松推测出ρ的区间。然而，当随机变量个数不固定时，我们很难估计出合理的区间。比如Brain每天都有顾问提交的因子，Prod Corr应该是动态变化的。随机变量的个数不断增加，计算起来比较复杂。这是我的观点

---

### 评论 #2 (作者: LX31898, 时间: 1年前)

试运行了一下题主的代码，但结果并没有跑通。想问下题主：y和know_corr在我这里计算出来都是一个序列，请问know_corr中间需要如何转换能得到计算需要的数值？

---

### 评论 #3 (作者: KZ79256, 时间: 1年前)

[YW93864](/hc/en-us/profiles/14096946892439-YW93864)  感谢Yumin大佬的补充. 确实很难估计出合理的区间, 而且我们也很难知道pool中的相关系数都是什么.

我在这里的核心思想是减少check相近pnl的次数.

极限下两个pnl的相关系数为1, 则只需要check一条曲线即可.

而非极端下可以简单的通过中等级别(2)来计算一个相关系数来排除掉相近的pnl.

---

### 评论 #4 (作者: KZ79256, 时间: 1年前)

[LX31898](/hc/en-us/profiles/30215090251159-LX31898)  这个代码很难一次跑通的,因为已经经过check的pnl和prod corr都需要额外准备.

y和know_corr确实都是个序列, 通过两个序列可以计算得到corr_min,我们取corr_min的最大值.

know_corr是一个pd.Series, 索引是alpha_id,值是prod corr

know_rets是一个pnls的矩阵, 列名是alpha_id, 行是时间(参考本地corr计算的os_rets)

---

### 评论 #5 (作者: LX31898, 时间: 1年前)

问下 [KZ79256](/hc/en-us/profiles/13609593802263-KZ79256) 大佬，已经经过check的pnl和prod corr可以从自己已经测过但是没有达到提交条件的alpha里面选吗，或者是只能从平台上面根据权限或者其他因素找近似符合条件的alpha？

---

### 评论 #6 (作者: KZ79256, 时间: 1年前)

我用的是自己已经测过但是没有达到提交条件的alpha. 这个corr需要自己存下来, 平台上基本没有啥保留

---

### 评论 #7 (作者: QQ68782, 时间: 1年前)

楼上大佬都太专业了, 看不懂

我有个最简单的实践, 效果似乎还行

就是直接相乘就行了

比如: 提交alpha a1失败, prod_corr = 0.8

本地计算a2和a1的相似度是0.9

那么认为a2的prod_corr至少是:0.8*0.9 = 0.72, 直接放弃check

实际用下来的确能增加check的效率

---

### 评论 #8 (作者: KZ79256, 时间: 9个月前)

[QQ68782](/hc/en-us/profiles/27244216042135-QQ68782)

太强了佬，大道至简哇

==================================keep moving=======================================

---

### 评论 #9 (作者: WL63604, 时间: 6个月前)

yyds，今天机缘巧合看到了相关性的传递性定理：
 ![图片](images/img_5f911748c6.png) 假如X是已经计算出PC的alpha，且与池子中的某个A相关性最大，B是待求PC的alpha，且B与X的互相性可以通过PNL计算出来。虽然不知道B是否也是与池子的中某个A也是相关性最大，但至少也可以通过相关性的传递性计算与A的相关性，以排除明确下限大于0.7的因子

---

### 评论 #10 (作者: BJ65592, 时间: 6个月前)

我试了一下一批只精确测试pc一定个数到速度明显变慢为止，然后拿这些精确测试过的pc和剩余没测试的因子做相关性矩阵计算，再乘上刚才的pc列，然后在每行没测试过的因子取最大值，判断是否大于0.7，大于就直接不看了，小于则后续有时间再手动验证pc。

效果不是很理想，原因可能是样本太少，仅限于当天测出来的10几20个的pc，而且这些pc值还普遍不高，毕竟是想要交的因子，经过了层层筛选出来的。拿pc值低的因子做样本效果太差，这样下来目标可能是收集pc尽可能高的因子的pnl，最好是1，感觉可以写个服务，两个接口，一个是输入pnl和pc值入库，可以限制pc值必须大于0.9，问题是无法校验pc值是否真实，全凭自觉；第二个是输入pnl估算pc值或者是全量下载数据用于本地计算

---

