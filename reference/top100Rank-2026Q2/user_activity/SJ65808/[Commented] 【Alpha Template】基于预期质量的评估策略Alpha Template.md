# 【Alpha Template】基于预期质量的评估策略Alpha Template

- **链接**: [Commented] 【Alpha Template】基于预期质量的评估策略Alpha Template.md
- **作者**: JS30938
- **发布时间/热度**: 7个月前, 得票: 2

## 帖子正文

一、Alpha模板

```
if_else(greater(act_q_bps_surprisenum, 5),ts_scale(act_q_ebi_surprisestd, 60),0)
```

数据字段

```
{    id: 'act_q_bps_surprisenum',    description: 'Number of estimates used for surprise calculation of actual book value per share regarding the last quarter',    dataset: { name: 'Broker Estimates' }  }    {    id: 'act_q_ebi_surprisestd',    description: 'Standard deviation of surprise (actual - estimate) of actual EBIT regarding the last quarter',    dataset: { name: 'Broker Estimates' }  }
```

二、核心逻辑

只在有足够分析师关注的股票中（>5个估计），根据其预期分歧度的时间序列模式生成交易信号。

三、经济学意义

> 在分析师关注度的股票中，通过寻找符合预期分歧度，自然排除低关注度股票，进而获得相对流动性好，信息质量高的股票

关注度：
筛选出 **每股账面价值有超过5个分析师估计** 的股票
对于有更多个分析师的预测，信息更可靠，代表市场关注度更高，高关注的股票流动性更好

分歧度：
对过去60天内 **每股账面价值意外标准差** 进行时间序列标准化
基于实际分析师行为，非价格数据，标准化处理确保跨股票可比性

四、优化
1. 5个分析师是否最优？是否可扩大范围，如可测试3-10的范围
2. 60天是否最佳？是否可测试30-90天范围
3. 时间序列ts_scale是否最适合？可尝试其他标准化

五、总结

尝试搜索其他不同region，不同universe的dataset.name:Broker Estimates类型的字段
此模板通过对数量值字段(act_q_bps_surprisenum)的大小判断来获取信号，可查找类型场景的数据字段，适配此策略

---

## 讨论与评论 (1)

### 评论 #1 (作者: SJ65808, 时间: 5个月前)

为啥是5，这个模板又该如何拓展么，有效果展示吗

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

