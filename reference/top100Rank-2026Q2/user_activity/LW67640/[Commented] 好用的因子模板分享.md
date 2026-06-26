# 好用的因子模板分享

- **链接**: [Commented] 好用的因子模板分享.md
- **作者**: XL31477
- **发布时间/热度**: 1年前, 得票: 29

## 帖子正文

```
[    {        "因子模板": "rank(ts_weighted_decay(ts_delta({field1}, 5), k=0.7)) * ts_corr(ts_min_diff({field2}, 10), ts_max({field3}, 15), 20)",        "模板idea": "计算字段在过去5个交易日的变化率，并应用加权衰减函数对其进行排名；然后计算两个字段在过去10个交易日最小差异和另一个字段在过去15个交易日的最大值之间的相关性。此因子结合了短期因子动量和中期相对强弱。",        "适用数据集": {            "field1": {                "analyst": ["analyst11"],                "earnings": ["earnings3"],                "fundamental": ["fundamental13"],                "model": ["model21"],                "imbalance": ["imbalance1"],                "insiders": ["insiders1"],                "institutions": ["institutions6"],                "macro": ["macro17"],                "other": ["other110"],                "news": ["news12"],                "option": ["option1"],                "socialmedia": ["socialmedia4"],                "sentiment": ["sentiment1"],                "risk": ["risk59"],                "pv": ["pv1"],                "shortinterest": ["shortinterest2"]            },            "field2": {                "analyst": ["analyst12"],                "earnings": ["earnings4"],                "fundamental": ["fundamental28"],                "model": ["model20"],                "imbalance": ["imbalance1"],                "insiders": ["insiders4"],                "institutions": ["institutions4"],                "macro": ["macro10"],                "other": ["other128"],                "news": ["news20"],                "option": ["option6"],                "socialmedia": ["socialmedia3"],                "sentiment": ["sentiment1"],                "risk": ["risk71"],                "pv": ["pv103"],                "shortinterest": ["shortinterest14"]            },            "field3": {                "analyst": ["analyst14"],                "earnings": ["earnings9"],                "fundamental": ["fundamental31"],                "model": ["model31"],                "imbalance": ["imbalance1"],                "insiders": ["insiders1"],                "institutions": ["institutions13"],                "macro": ["macro4"],                "other": ["other159"],                "news": ["news22"],                "option": ["option13"],                "socialmedia": ["socialmedia5"],                "sentiment": ["sentiment27"],                "risk": ["risk62"],                "pv": ["pv3"],                "shortinterest": ["shortinterest17"]            }        }}]
```

**解释：** 
1. rank(ts_weighted_decay(ts_delta({field1}, 5), k=0.7)):
   - ts_delta({field1}, 5): 计算字段1（{field1}）在最近5个交易日的变化率（差值）。
   - ts_weighted_decay(..., k=0.7): 对上述变化率应用一个加权衰减函数，其中k=0.7是衰减系数，表示越近期的数据权重越高。
   - rank(...): 对加权衰减后的结果进行排名，生成一个排名值。

1. ts_corr(ts_min_diff({field2}, 10), ts_max({field3}, 15), 20):
   - ts_min_diff({field2}, 10): 计算字段2（{field2}）在最近10个交易日的最小差异（可能是最小波动或最小变化）。
   - ts_max({field3}, 15): 计算字段3（{field3}）在最近15个交易日的最大值。
   - ts_corr(..., 20): 计算上述两个时间序列在过去20个交易日的相关性。
2. 整体因子: 将排名值与相关性值相乘，生成最终的因子值。

**模板idea (Template Idea)** 
- 短期动量: 通过计算字段1在过去5个交易日的变化率，并应用加权衰减函数进行排名，捕捉短期动量效应。
- 中期相对强弱: 通过计算字段2和字段3之间的相关性，其中字段2是过去10个交易日的最小差异，字段3是过去15个交易日的最大值，来衡量中期的相对强弱。

**适用场景** 
这个因子模板适用于那些需要结合短期动量和中期相对强弱的数据字段。通过结合排名和相关性分析，可以识别出具有潜在投资价值的股票。

---

## 讨论与评论 (6)

### 评论 #1 (作者: SY90356, 时间: 1年前)

感谢您的分享，请问从您使用的经验来看，在哪个region下这套模板表现较好？或者是否给region表现做一个大概排序，谢谢！

---

### 评论 #2 (作者: LW67640, 时间: 1年前)

感谢分享。我随便尝试了3个字段，有明显的信号。

---

### 评论 #3 (作者: BL59663, 时间: 1年前)

感谢分享，我问下是不是3个字段要一一对应，比如我用了field1的analyst，后面两个是不是也是analyst数据。还是说可以交叉遍历的。

---

### 评论 #4 (作者: ZL42615, 时间: 1年前)

感谢分享，试试效果！~~

---

### 评论 #5 (作者: LJ12230, 时间: 1个月前)

感谢分享！

---

### 评论 #6 (作者: FF65210, 时间: 16天前)

因子模板分享太贴心了！短中期相对强弱的组合逻辑很清晰，而且适用数据集的建议也很实用。模板化思维确实能降低开发复杂度，不然每次从零开始太耗时间。收藏了，下批回测就用这套模板。

---

