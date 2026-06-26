# 【Alpha灵感】Cash Flow over Enterprise Value ratio and Investor CautionAlpha Template

- **链接**: [Commented] 【Alpha灵感】Cash Flow over Enterprise Value ratio and Investor CautionAlpha Template.md
- **作者**: TK60163
- **发布时间/热度**: 1年前, 得票: 11

## 帖子正文

研究课题：Free Cash Flow, Enterprise Value, and Investor Caution

链接： [https://www.researchgate.net/publication/228319760_Free_Cash_Flow_Enterprise_Value_and_Investor_Caution](https://www.researchgate.net/publication/228319760_Free_Cash_Flow_Enterprise_Value_and_Investor_Caution)

**Abstract:** 
 *By analyzing actual cash flows in comparison with enterprise values (market capitalization plus debt minus cash) we document that the market dramatically undervalues firms. The findings suggest that the equity market has an extraordinarily high discount rate which negates future earnings in the calculus of firm value. That is, the discount rate is so high that the vast majority of future cash flows are virtually ignored.*

我们从这个简单且知名的 alpha 表达式开始：

```
ts_zscore(cashflow_op/enterprise_value,63)
```

### Alpha 想法：

我们将使用另一个变量替代 operating cashflow over enterprise value 的比率：

```
mdl77_2400_vefcomtt
```

定义（来自 WorldQuant Brain）：

**TTM Operating Cash Flow-to-Enterprise Value** ：被定义为股票的过去 12 个月运营现金流每股值除以每股企业价值。

#### Alpha 表达式：

```
-ts_zscore(mdl77_2400_vefcomtt,63)
```

![图片](images/img_46a428a762.png)

![图片](images/img_079daf54dd.png)

该信号比直接使用  `(cashflow_op/enterprise value)`  更加清晰。
但还可以进一步优化，因为该表达式太简单。
我考虑过更改运算符与回溯期（lookback days），因为 63 天对于 TTM（12 个月）来说过短。

#### 表达式：

```
-ts_quantile(mdl77_2400_vefcomtt,1008)
```

结果：

![图片](images/img_48f9c6639d.png)

### 这是一个可以提交的 alpha，但需要注意的一点是：

![图片](images/img_bc26eaff24.png)

该 alpha 的 PnL 曲线波动过大（spiky）。

### 我认为可能有两个原因：

1. 有很多噪音干扰了信号
2. 信号本身可能不够稳健

### 优化方向：

我们尝试使用  `group_neutralize()`  函数来剔除风险，并使用  `ts_decay_linear()` （或添加额外的 decay）来平滑信号：

```
-group_neutralize(group_neutralize(ts_decay_linear(ts_quantile(mdl77_2400_vefcomtt,1260,driver="cauchy"),5),bucket(rank(capex/sales),range="0,1,0.1")),bucket(rank(debt/enterprise_value),range="0,1,0.2"))
```

其中 neutralize 方法受到 ChatGPT 的启发。

### ChatGPT 表示：

> **5. Leverage (Debt/Equity or Debt/EV)**
> 原因：Enterprise Value 包含债务，因此高杠杆的公司可能会扭曲比率。
> 做法：按照杠杆率进行分组中性化，以减少债务影响。
> **6. Capital Intensity (Capex / Sales, or Fixed Assets / Assets)**
> 原因：资本密集型公司即便运营现金流强，仍可能拥有较低自由现金流。
> 做法：在资产密集型和轻资产企业之间中性化。

### 结果：

![图片](images/img_8fdd3dff1a.png)

![图片](images/img_842696a4e8.png)

### 后续改进方向：

1. 如何降低此 alpha 的换手率（turnover）？
2. 是否可以在保持较低收益标准差的同时提高回报？
3. 如何提高该 alpha 的利润率（margin）？
4. 如何提高子股票池（sub-universe）的夏普比率？（增加 decay 会使 alpha 无法提交）

### 我希望得到以下问题的答案：

1. 是否对 alpha 的进一步改进会导致  **过拟合（overfitting）** ？
2. 如何将研究论文中提出的更多变量（如 CCF 和 EEV）整合进来？
3. 作为一名访问受限的  **consultant** ，我该如何使用仅限 consultant 的操作符替代？（例如，用  `ts_linear_decay`  代替  `ts_exp_window_decay` ）

---

## 讨论与评论 (10)

### 评论 #1 (作者: WS14257, 时间: 1年前)

Thank you guys, nice idea!

---

### 评论 #2 (作者: YH82809, 时间: 1年前)

非常感谢你的分享。

这已经非常好了，我也在担心进一步改进会导致过拟合。如果再把更多的变量整合进去，也许会得到更好的表现，也许会变得更复杂，合乎经济逻辑的我想一定会有好的表现。

---

### 评论 #3 (作者: DM28368, 时间: 1年前)

这是一个非常强大且有价值的数据集，我在量化模型中曾通过它获得了非常高的价值因子（Value Factor）。当将其与 Z-Score 标准化处理和排序（Rank）等技术相结合时，模型所生成的 Alpha 指标会有显著提升。这个数据集非常适合用于挖掘具有预测能力的投资信号。

---

### 评论 #4 (作者: YW93864, 时间: 1年前)

[TK60163](/hc/en-us/profiles/31451865057303-TK60163)

> 1. 是否对 alpha 的进一步改进会导致  **过拟合（overfitting）** ？

看着不错，目前的修改是在没有修改alpha逻辑的情况下，适当调整了alpha的数值，比如使用ts_decay_linear平滑alpha值，用group_neutralize得到更纯净的信号，使用这两个group看上去很有逻辑，很符合基本面量化的一般做法

> 1. 如何将研究论文中提出的更多变量（如 CCF 和 EEV）整合进来？

在这一步中，需要考虑它是否在叠加，一般论文将不同的变量add在一起，并没有特殊的操作。所以我建议可以将不同的指标分开测试，再考虑是否要加入现有的alpha上

> 1. 作为一名访问受限的  **consultant** ，我该如何使用仅限 consultant 的操作符替代？

尝试使用含义近似的operator替换尝试，这个做法也能同时检测alpha idea是否稳健。

---

### 评论 #5 (作者: YW93864, 时间: 1年前)

1. 如何降低此 alpha 的换手率（turnover）？

调试setting中的decay，使用ts_operator中相近的算子；调整alpha值的大小，例如使用sqrt(alpha)

1. 是否可以在保持较低收益标准差的同时提高回报？

这个在alpha idea不变的情况下很难取得显著的成效，因为盈亏同源，当你把稳定性提升时，势必要失去一些收益向上波动的机会

1. 如何提高该 alpha 的利润率（margin）？

margin是pnl除以trade dollars，一方面可以提高pnl，一方面可以降低turnover，前者可以用新的idea优化它，后者可以用操作符或者setting降低它

1. 如何提高子股票池（sub-universe）的夏普比率？（增加 decay 会使 alpha 无法提交）

建议多加测试不同参数的decay，观察是否稳健。如果不同参数下sub-universe有一致性，变化不大，那么可以考虑选择能够提交的那组参数

---

### 评论 #6 (作者: QD44113, 时间: 1年前)

Good idea! Thats helpful

---

### 评论 #7 (作者: FL39657, 时间: 1年前)

It has great reference value for me and has improved my understanding of alpha. Thank you for sharing

---

### 评论 #8 (作者: YW10763, 时间: 9个月前)

看明白了 感谢分享

---

### 评论 #9 (作者: MY82844, 时间: 7个月前)

很有启发，有个细节，理论上来说enterprise_value可以是负值，这样需要特殊处理分母是负值的情形吗？

---

### 评论 #10 (作者: JQ70858, 时间: 7个月前)

很有启发的思考过程演绎，对于我这种小白很有帮助，谢谢楼主分享。

但是sub-universe sharpe的问题还是没得到很好的答案，最近总是遇到这个指标差一点的情况，希望能有人拿出来讨论一下。

---

