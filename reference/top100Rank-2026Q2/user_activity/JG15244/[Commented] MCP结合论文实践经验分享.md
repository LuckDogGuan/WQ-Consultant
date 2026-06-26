# MCP结合论文实践经验分享

- **链接**: [Commented] MCP结合论文实践经验分享.md
- **作者**: YZ13693
- **发布时间/热度**: 7个月前, 得票: 20

## 帖子正文

官方推荐的论文

Research Paper: Overvalued Equity and Financing Decisions

[https://support.worldquantbrain.com/hc/en-us/community/posts/14983690885911-Research-Paper-Overvalued-Equity-and-Financing-Decisions](/hc/en-us/community/posts/14983690885911-Research-Paper-Overvalued-Equity-and-Financing-Decisions)

根据MCP工具里面的APP, 提取论文的方程 和表达式
 ![图片](images/img_6c955c7ae7.png) 
 ![图片](images/img_ea0ee3fc51.png) 导出分析结果
根据论文提供的 数据字段 mdl23_bk_net_equity_financ 利用ai  对起进行分析，

分析结果如下：

## 原始表达式（已回测）

**Alpha ID**: `rK3edZVd`

**表达式**:

```

group_neutralize(ts_rank(ts_mean(mdl23_bk_net_equity_financ, 20), 60) + ts_rank(ts_mean(pv87_stock_tvrwgthold, 20), 60), densify(sector))

```

**回测结果**:

- IS Sharpe: 0.61 (FAIL - 低于1.58阈值)

- IS Fitness: 0.22 (FAIL - 低于1.0阈值)

- Turnover: 0.0651 (PASS)

- Sub-universe Sharpe: 0.19 (FAIL)

**逻辑**: 高股权融资 + 高换手率 = 更强的市场时机信号

---

## 优化表达式（待测试）

### 方向1：改为减法组合（反转逻辑）

**逻辑**: 高股权融资 + 高换手率 = 做空信号（利用高估时机）

```

group_neutralize(ts_rank(ts_mean(mdl23_bk_net_equity_financ, 20), 60) - ts_rank(ts_mean(pv87_stock_tvrwgthold, 20), 60), densify(sector))

```

**参数建议**:

- region: USA

- universe: TOP3000

- delay: 1

- decay: 6

- neutralization: SECTOR

- truncation: 0.02

---

### 方向2：增强平滑与去噪

**逻辑**: 增加平滑窗口，收紧限尾，减少噪声

```

group_neutralize(ts_rank(ts_mean(winsorize(ts_mean(mdl23_bk_net_equity_financ, 20), std=3), 10), 60) + ts_rank(ts_mean(winsorize(ts_mean(pv87_stock_tvrwgthold, 20), std=3), 10), 60), densify(sector))

```

**参数建议**:

- region: USA

- universe: TOP3000

- delay: 1

- decay: 6-8

- neutralization: SECTOR

- truncation: 0.02-0.03

---

### 方向3：单一信号测试（股权融资）

**逻辑**: 先测试单一信号强度，确认基础信号质量

```

group_neutralize(ts_rank(ts_mean(mdl23_bk_net_equity_financ, 20), 60), densify(sector))

```

**参数建议**:

- region: USA

- universe: TOP3000

- delay: 1

- decay: 6

- neutralization: SECTOR

- truncation: 0.02

---

### 方向4：调整窗口参数

**逻辑**: 缩短平滑窗口，延长排名窗口，提高信号敏感性

```

group_neutralize(ts_rank(ts_mean(mdl23_bk_net_equity_financ, 10), 120) + ts_rank(ts_mean(pv87_stock_tvrwgthold, 10), 120), densify(sector))

```

**参数建议**:

- region: USA

- universe: TOP3000

- delay: 1

- decay: 6

- neutralization: SECTOR

- truncation: 0.02

---

### 方向5：股权融资 + 估值组合（论文核心逻辑）

**逻辑**: 高股权融资 + 低估值 = 可能被高估，未来表现较差

```

group_neutralize(ts_rank(ts_mean(mdl23_bk_net_equity_financ, 20), 60) - ts_rank(ts_mean(mdl23_valuation, 20), 60), densify(sector))

```

**参数建议**:

- region: USA

- universe: TOP3000

- delay: 1

- decay: 6

- neutralization: SECTOR

- truncation: 0.02

---

### 方向6：股权融资 + 模型评分

**逻辑**: 高股权融资 + 低模型评分 = 融资时机不佳

```

group_neutralize(ts_rank(ts_mean(mdl23_bk_net_equity_financ, 20), 60) - ts_rank(ts_mean(mdl23_bk_mdl_score, 20), 60), densify(sector))

```

**参数建议**:

- region: USA

- universe: TOP3000

- delay: 1

- decay: 6

- neutralization: SECTOR

- truncation: 0.02

---

### 方向7：股权融资变化率（市场时机）

**逻辑**: 股权融资快速增加 = 利用高估时机

```

group_neutralize(ts_rank(ts_delta(mdl23_bk_net_equity_financ, 5), 60), densify(sector))

```

**参数建议**:

- region: USA

- universe: TOP3000

- delay: 1

- decay: 6

- neutralization: SECTOR

- truncation: 0.02

---

## 数据字段说明

### 核心字段

- **mdl23_bk_net_equity_financ**: 股权融资水平（高分表示更高的股权发行水平）

- 数据集: model23 (Scorings Data)

- 覆盖率: 65.89%

- 使用情况: 36用户，151个alpha

- **pv87_stock_tvrwgthold**: 换手率加权持仓

- 数据集: pv87 (Aggregated dataset)

- 覆盖率: 96.51%

- 使用情况: 104用户，1229个alpha

### 辅助字段

- **mdl23_valuation**: 估值（自由现金流/企业价值）

- **mdl23_bk_mdl_score**: 总体模型评分

- **mdl23_bk_mdl_score_chg**: 模型评分变化

---

## 论文核心发现（参考）

1. **误定价驱动融资**: 股权高估时，权益发行增加（仅在被高估股票中成立）

2. **条件效应**:

- 成长机会：低B/P、高R&D、小公司对误定价更敏感

- 换手率：高换手率放大误定价对发行的效应

- 内部人交易：内部人净卖出越多，权益发行对高估越敏感

3. **关键指标**: V/P（误定价）、EI（权益发行）、Tobin's q（增长机会）

---

## 测试优先级

1. **优先测试**: 方向3（单一信号）- 确认基础信号强度

2. **其次测试**: 方向5（股权融资+估值）- 符合论文核心逻辑

3. **并行测试**: 方向1、方向2、方向4 - 不同优化策略

4. **后续测试**: 方向6、方向7 - 其他组合方式

---

## 注意事项

- 所有表达式使用 USA/TOP3000/D1 设置

- 建议 decay=6-8，truncation=0.02-0.03

- 中性化建议使用 SECTOR（已测试）或 INDUSTRY

- 需要关注 robust universe Sharpe ≥ 1.0

---

得到一条 不错的Pnl,曲线
 ![图片](images/img_06a9878ebc.png)

补充：

alpha表达式

ts_delta(group_neutralize(ts_rank(ts_mean(mdl23_bk_net_equity_financ, 10), 120) + ts_rank(ts_mean(pv87_stock_tvrwgthold, 10), 120), densify(sector)), 240)

setting 配置如图

![图片](images/img_82594490fa.png)

---

## 讨论与评论 (7)

### 评论 #1 (作者: JG15244, 时间: 7个月前)

看最后的pnl图线，是一个非常好的alpha！

有几个疑问，我看文中提到的示例alpha表达式中，还存在pv类型的字段，这个字段是怎么来的呢？

贴主，是否分享一下提问的具体呀。

---

### 评论 #2 (作者: WL13229, 时间: 7个月前)

[JG15244](/hc/en-us/profiles/26966744854807-JG15244)

博主已分享了表达式 欢迎查看

---

### 评论 #3 (作者: SD14148, 时间: 7个月前)

============================================================================

感谢大佬分享

============================================================================

有学到了个知识点

---

### 评论 #4 (作者: AH18340, 时间: 7个月前)

感谢大佬分享，这么多op会不会过拟合

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #5 (作者: FF56620, 时间: 7个月前)

感谢分享，我在尝试使用AI处理论文的时候，也是一样，最终生成的表达式太多operator和field了，且存在不同dataset和category的field的混用，不知道会不会过拟合

---
Pursue scalable, repeatable opportunities rooted in probability.

---

### 评论 #6 (作者: JC25837, 时间: 6个月前)

确实，MCP给小白们太多的建议了，但是发现它只会套公式上去。

---

### 评论 #7 (作者: YQ84572, 时间: 6个月前)

感谢分享，很清晰的分享了mcp结合论文的实践经验
=============================================================================================================================================================================

---

