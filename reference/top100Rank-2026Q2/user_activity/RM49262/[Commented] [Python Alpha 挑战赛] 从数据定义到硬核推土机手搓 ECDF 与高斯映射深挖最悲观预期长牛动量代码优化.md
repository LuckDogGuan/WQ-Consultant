# [Python Alpha 挑战赛] 从数据定义到硬核推土机：手搓 ECDF 与高斯映射，深挖“最悲观预期”长牛动量代码优化

- **链接**: [Commented] [Python Alpha 挑战赛] 从数据定义到硬核推土机手搓 ECDF 与高斯映射深挖最悲观预期长牛动量代码优化.md
- **作者**: DZ94835
- **发布时间/热度**: 27天前, 得票: 16

## 帖子正文

**1, Idea：**

**起因与发现：**  最近在翻 Data 淘金，重点盯上了  `anl4_qfv4_eps_low`  这个冷门字段。看了一下官方的具体字段含义，它代表的是 **分析师对远期（Forward）EPS 给出的最低预期值** 。

这个金融逻辑其实非常性感：市场上的一致预期（均值/中位数）往往非常拥挤且滞后，但我只盯“最悲观的那个声音”。当全市场砸盘砸得最狠、给出最低预测的分析师，都开始默默上调远期 EPS 时，这往往意味着基本面真正意义上的“利空出尽”，是绝佳的长牛反转信号。

为了看清底细，我专门去  **Lab**  里拉了一下这个字段的真实数据状态。从覆盖率来看，它的时序连续性其实非常好（如下图所示），并不是那种零星残缺的数据。

**![图片](images/img_32a517ffe2.png)**

**![图片](images/img_99c40a743e.png)**

但盯着它的分布图（Distribution），我发现了两个致命的硬伤：

1. **绝对值尺度无法横向对比** ：EPS 是个绝对面值，百元股和几毛钱的股票，其 EPS 的绝对变化量根本不在一个量级。如果直接算 Delta，整个因子的信号会被高价股彻底绑架。
2. **分布偏斜与高密度的“平局粘性”** ：最悲观的预测往往有很强的粘性，数据里存在大量连续多日完全相同的数值（Ties），且整体分布呈现显著的非正态长尾特征。

**Fast Expression 的局限：**  如果用老平台的表达式，直接用  `ts_delta`  做差分，出来的信号全是毛刺，完全没法用。如果加一层  `ts_quantile(..., 180)`  来做分位数平滑，又会遇到一个黑盒坑：分析师预期这玩意儿“平局（Tie）”太多了，经常连续几个月数值趴着不动，底层 Rank 机制处理极其粗糙，且输出只是均匀分布，把尾部基本面修复的力度差异全给抹平了。

**思路破局：干脆自己造轮子**  既然现在放开了 Python Alpha，干脆彻底抛弃黑盒。我的方案是：

1. **先做无未来前向填充 (ffill)** ，把分析师研报空窗期的缺失值补齐。
2. **手写经验累积分布 (ECDF)** ，精细化处理相同值的权重（平局给一半权重），算出真实的相对历史水位。
3. **引入  `scipy.special.ndtri`  做高斯逆映射** ，把均匀分布强行拉成标准正态分布，从根源上把长尾极值和阶跃噪音“正态化”。
4. 最后，再对这套正态化后的水位算 300 天的超长线 Delta。

**2, 实现：**

**核心代码说明：**  因为要算  `delta(..., 300)`  还要往前看 180 天的分布，历史视距拉得很长。为了防止 Python 里写  `for`  循环大横截面直接跑到超时，我把状态存储（store）给扬了，全靠  `numpy`  矩阵切片和掩码（Mask）来硬扛，速度飞快。

下面是完整代码，可以直接拿去跑：

```
from brain.alphas import alphaimport numpy as npimport numpy.typing as nptfrom scipy.special import ndtriimport warningsdef np_ffill(arr):    """    自己糊的一个极速 2D 前向填充。    模拟 FastExpr 处理低频数据的默认 nanHandling，    靠 index 累加避开了循环，处理几百天的长周期空值只有几毫秒。    """    mask = np.isnan(arr)    idx = np.where(~mask, np.arange(mask.shape[0])[:, None], 0)    np.maximum.accumulate(idx, axis=0, out=idx)    return arr[idx, np.arange(idx.shape[1])]@alpha(    data=["anl4_qfv4_eps_low"],    store=[], # 靠拉长 lookback 一次性喂饱数据，不要 store)def ts_delta_quantile_alpha(data, store) -> npt.NDArray[np.float32]:    # 一口气切出过去 480 天的数据 (300的delta跨度 + 180的分布窗口)    x_raw = data.anl4_qfv4_eps_low[-480:].astype(np.float64)        with warnings.catch_warnings():        warnings.simplefilter("ignore")        # 先把日常的 NaN 坑给填上        x = np_ffill(x_raw)                # ==========================================        # 算【今天】的 180 天分布水位        # ==========================================        W_curr = x[-180:]        v_curr = W_curr[-1]                N_curr = np.sum(~np.isnan(W_curr), axis=0)        less_curr = np.nansum(W_curr < v_curr, axis=0)        eq_curr = np.nansum(W_curr == v_curr, axis=0)                # 手搓 ECDF：小于的算全额，等于的算一半，彻底解决 Tie 太多导致的信号扭曲        R_curr = (less_curr + eq_curr / 2.0) / np.where(N_curr > 0, N_curr, np.nan)        R_curr = np.where(np.isnan(v_curr), np.nan, R_curr)        # 上科技：正态分布映射        Q_curr = ndtri(R_curr)                # ==========================================        # 算【300 天前】的 180 天分布水位        # ==========================================        # 矩阵切片大法好：直接切 -480 到 -300 的那一段，刚好 180 天        W_past = x[-480:-300]        v_past = W_past[-1]                N_past = np.sum(~np.isnan(W_past), axis=0)        less_past = np.nansum(W_past < v_past, axis=0)        eq_past = np.nansum(W_past == v_past, axis=0)                R_past = (less_past + eq_past / 2.0) / np.where(N_past > 0, N_past, np.nan)        R_past = np.where(np.isnan(v_past), np.nan, R_past)        Q_past = ndtri(R_past)                # ==========================================        # 算最终的 Long-term Delta        # ==========================================        result = Q_curr - Q_past        result = np.where(np.isinf(result), np.nan, result)            return result.astype(np.float32)
```

3, 提交的页面展示：

![图片](images/img_1f91589480.png)

**配置项 Payload 避坑指南：**  实测下来，高斯化之后再做长周期 delta，彻底洗掉了基本面的阶跃噪音，在 IND 市场 Top500 跑出来的曲线非常稳，抗回撤能力比原版表达式强了一大截。

```
lookback
```

抛砖引玉，希望能给同样在弄基本面长线因子的大佬们提供点灵感！

---

## 讨论与评论 (6)

### 评论 #1 (作者: RM49262, 时间: 23天前)

=====================================评论区====================================

感谢大佬分享  这个思路学到了 准备自己也去试试看

祝大佬比赛取得好成绩

=============================================================================

---

### 评论 #2 (作者: LJ12230, 时间: 23天前)

感谢大佬分享！日积月累，日进一步......................终至山顶。

---

### 评论 #3 (作者: MY21251, 时间: 22天前)

从"最悲观预期"切入这个角度太精妙了！一致预期确实太拥挤，但盯着最悲观的声音变化，这个信号的信噪比应该会高很多。当连最看空的人都改口时，基本面反转的确定性确实强。这是一个典型的逆向投资思维应用：不从共识中找机会，而是关注市场中最悲观的声音，捕捉其边际改善带来的反转信号。适合追求稳健、长周期的 Alpha 策略。

---

### 评论 #4 (作者: LA79055, 时间: 22天前)

这个思路很有启发，尤其是把分析师最低 EPS 预期里的尺度差异、平局值和长尾分布先拆开处理，再用 ECDF 与高斯映射重构信号。官方 Python Alpha 文档也提到数据数组、dtype 和历史窗口要自己管理，这篇把这些工程细节和经济逻辑结合得很清楚。

---

### 评论 #5 (作者: LL81909, 时间: 22天前)

复制 - 粘贴 改SETTINGS,然后回测。。。。什么都没发生 只显示Simulate an alpha to view the results here.

---

### 评论 #6 (作者: XY20037, 时间: 20天前)

逻辑强 → 信号稳 → 写法快 → 避坑全 → 适合 Osmosis + 长期收益。

已经收藏，准备直接跑多区域版本，补充长线低相关 Alpha 库！

---

