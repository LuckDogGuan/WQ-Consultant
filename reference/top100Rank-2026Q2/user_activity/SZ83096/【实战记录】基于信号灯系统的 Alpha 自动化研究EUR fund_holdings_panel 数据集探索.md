# 【实战记录】基于信号灯系统的 Alpha 自动化研究——EUR fund_holdings_panel 数据集探索

- **链接**: 【实战记录】基于信号灯系统的 Alpha 自动化研究EUR fund_holdings_panel 数据集探索.md
- **作者**: SZ83096
- **发布时间/热度**: 17天前, 得票: 21

## 帖子正文

### 前言

本文记录了使用"信号灯系统"进行 Alpha 研究的完整实战过程。该系统源自社区帖子《用AI 跑了几百次回测还找不到优质信号》，核心思路是用统计学方法指导 AI 的探索方向。

**原帖链接** :  [[L2] 【经验分享】用AI 跑了几百次回测还找不到优质信号到底是池塘没鱼还是鱼饵不对燃烧token给 AI 装上导航置顶的论坛精选.md]([L2] 【经验分享】用AI 跑了几百次回测还找不到优质信号到底是池塘没鱼还是鱼饵不对燃烧token给 AI 装上导航置顶的论坛精选.md)

### 一、研究背景

**数据集** : EUR/TOP2500/fund_holdings_panel（30个字段）

#### 信号灯系统简介

- 🟢 GREEN: 方向有信号，加码深挖
- 🟡 YELLOW: 有潜力但证据不足，谨慎继续
- 🔴 RED: 信号弱，做结构性改动
- ⚫ DEAD: 及时止损，换方向

### 二、研究过程

#### 第一轮：广泛探索（27个表达式）

均值 Sharpe: -0.24，最高: 0.64

 **信号灯: 🔴 RED → 行动: 结构性改动**

字段分析发现 holder_account_total 最差(Sharpe=-0.88)，应放弃

#### 第二轮：聚焦潜力字段（28个表达式）

均值 Sharpe: 0.27，最高: 0.97

 **关键发现** : stable_boundary_trade_count_21d 字段有显著信号

#### 第三轮：深度优化（20个表达式）

通过 2Y_SHARPE 检查: 9个

#### 第四轮：参数微调

最高 Sharpe: 0.93，2Y_SHARPE: 2.28

### 三、最终成果

**最佳表达式** :

```
ts_decay_linear(group_zscore(vec_avg(stable_boundary_trade_count_21d), sector), 20)
```

Sharpe=0.93, 2Y_SHARPE=2.28, Fitness=0.48

#### 高潜力表达式列表

表达式
Sharpe
2Y_SHARPE

ts_decay_linear(group_zscore(...), 20)
0.93
2.28

group_zscore(ts_decay_linear(..., 20), sector)
0.93
2.27

group_zscore(ts_decay_linear(..., 60), sector)
0.92
2.27

ts_mean(group_zscore(...), 20)
0.91
2.27

ts_decay_linear(group_zscore(...), 60)
0.91
2.44

### 四、信号灯系统验证

轮次
均值Sharpe
信号灯
行动

第一轮
-0.24
🔴 RED
结构性改动

第二轮
0.27
🟡 YELLOW
继续深挖

第三轮
0.39
🟡 YELLOW
参数优化

第四轮
0.84
🟢 GREEN
完成

### 五、关键发现

1. 有效信号字段: stable_boundary_trade_count_21d（稳定边界交易计数）
2. 最佳算子组合: ts_decay_linear + group_zscore
3. 经济学解释: 该字段代表基金的持久性仓位变化，反映机构投资者信息优势

### 六、信号灯系统价值

- 避免盲目探索，明确指导方向调整
- 区分"数据没信号"和"表达式没写对"
- 防误杀护栏，不过早放弃有潜力方向

### 七、致谢

感谢原帖作者分享的信号灯系统思路！

**原帖链接** :  [点击查看原帖]([L2] 【经验分享】用AI 跑了几百次回测还找不到优质信号到底是池塘没鱼还是鱼饵不对燃烧token给 AI 装上导航置顶的论坛精选.md)

---

## 讨论与评论 (1)

### 评论 #1 (作者: JR57542, 时间: 14天前)

感谢完整的实战记录，四轮迭代的信号灯变化过程非常清晰（RED → YELLOW → YELLOW → GREEN），很好地展示了信号灯系统如何避免盲目探索。

关于最终的 stable_boundary_trade_count_21d 字段发现：ts_decay_linear + group_zscore 这个算子组合确实是处理交易计数类字段的经典选择。我在 USA 上也发现类似规律——对于基金持仓面板数据，先做 group_zscore 去除行业效应，再用 ts_decay_linear 做时序平滑，通常比反过来（先时序后截面）效果更好。

补充一个细节：你提到第二轮最高 Sharpe=0.97 但信号灯仍判 RED。我在 EUR 区域也遇到过类似情况——EUR 的 Sharpe 天花板天然比 USA 低，如果用统一的 Sharpe≥1.0 作为 pass_rate 阈值，EUR 方向很容易被误判为无信号。建议对 EUR 单独降低阈值到 0.7-0.8。

---

