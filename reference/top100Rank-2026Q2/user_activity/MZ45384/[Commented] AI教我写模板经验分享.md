# AI教我写模板经验分享

- **链接**: [Commented] AI教我写模板经验分享.md
- **作者**: HC68689
- **发布时间/热度**: 3个月前, 得票: 15

## 帖子正文

# 1. 如何理解模板

先说下个人背景，程序员，金融小白。去年9月底成为顾问，vf经历三次更新，0.5->0.17->0.47->0.77, 算是刚脱坑的新手。之前的工作流程主要是两块：

- 1.给一些模板(来自论坛)和特定数据集，让AI帮我推荐字段。
- 2.给数据集，直接让AI帮我给出模板。

虽然能勉强出货了，总感觉自己对模板缺乏理解，不知道如何独立写一个模板，就花时间向AI学习了一段时间，整理下自己的理解，希望能帮助到和我一样没有任何金融背景的小白，大佬可以跳过了。

对模板的理解，简单点就是一个可验证的金融直觉(经济学逻辑)，它有两个特点：一是能影响股票走势，二是市场参与者比较认可； 比如这个直觉：挣钱多(净利润高)且稳定的公司股票可能上涨，第一点投资人都会关注公司财务报表中的净利润，它是影响股票的走势，第二点从常识出发，大家也都认可这个观念。具体到我们的工作中，这就是一个模板了：rank(datafield)/ts_std_dev(datafield, 504)， 然后就是去fundmental数据集中去找和净利润相关的数据字段。

但是模板也有好坏了，那这个模板是不是好模板呢？个人理解就是看这个金融直觉是否有漏洞(或者说值不值得推敲)，很明显我们认真理解这句话就会有疑问：

- 1.大公司挣100万和小公司挣100万是不是不能直接相比？
- 1. 不同行业的公司赚钱速度难易不一样，能直接比较吗？
- 3.挣钱多的公司股票已经涨上天了,是不是还得考虑下估值？
- 1. 挣钱稳定到底是多久，一年还是五年？

有了这些疑问，我们就可以继续改进模板了，对于第1.2点就是加group操作，进行cap/industry分组； 对于第3点就是估值低的时候才合理；对于第4点就是504这个时间可以进行调整了；改进后的模板如下：

```
if_else(rank(pb)<0.7, group_neutrizalize(rank(datafield)/ts_std_dev(datafield, 504/1024/2048), bucket(rank(cap), '0.1,1.0,0.1')), -1)。
```

现在回想培训课上老师说的寻找论文里面的alpha idea，其实就是这里说的经济学逻辑，采用brain平台的alpha表达式实现这个逻辑就是在构建模板的过程。alpha表达式越通用，适配的数据字段越多，就越符合模板本身的字面概念了。

至于去那里寻找这些经济学逻辑，一部分是常见的经济学逻辑，靠个人补充金融知识学习，一方面就是新的论文和研报里面学习。

下面是AI给的常见经济学逻辑（例如：动量、反转、价值、质量、成长、情绪等）映射到具体的操作符组合。例如：

- 动量：过去一段时间收益率（使用ts_delay, ts_delta等）
- 反转：过去一段时间收益率的负值
- 价值：市净率的倒数（使用divide, power等）
- 质量：ROE等财务指标
- 情绪：分析师评级变化、新闻情绪等

扯了这么多废话，理解模板的概念就行了，总结下AI给我的模板实战环节流程：

1. 拿到一个数据集，让AI分析里面的字段含义和分类，挑选出经典字段
2. 根据字段含义，让AI推荐常见的经济学逻辑，选一个经济学逻辑
3. 自己阅读和理解这个经济学逻辑，思考下是否合理，提出漏洞
4. 最后让AI修补漏洞后，写出模板，填充字段

# 2. 如何写一个模板

这是我发给AI的数据集，ai总结的三个经济学逻辑

```
这是一个risk类型数据集中的所有数据集，分析下这些字段的含义，给出几个和这些字段相关的经济学逻辑**数据集所有字段：**：vec_avg(rsk59_bid_rate):Market composite lending fee earned for existing shares on loan by long holders (in percent format).vec_avg(rsk59_crowded_score):Multi-factor model which ranks the short side crowdedness of a security based on its short interest, float, stock loan liquidity, and trading liquidity.vec_avg(rsk59_daystocover10day):Real-time Short Interest / 10-day ADTV (average daily trading volume)vec_avg(rsk59_daystocover30day):Real-time Short Interest / 30-day ADTV (average daily trading volume)vec_avg(rsk59_daystocover90day):Real-time Short Interest / 90-day ADTV (average daily trading volume)vec_avg(rsk59_dtcdailychg):Day-over-day percentage change in number of days to cover all short positionsvec_avg(rsk59_dtcweeklychg):Week-over-week percentage change in the number of days to cover all short positions.vec_avg(rsk59_indicativeavailability):Projected available lendable quantityvec_avg(rsk59_last_rate):Market composite lending fee earned for incremental shares loaned on that date (Spot Rate) (in percent format).vec_avg(rsk59_offer_rate):Market composite financing fee paid for existing short positions (in Percent Format)vec_avg(rsk59_short_interest):Real-time short interest expressed in number of sharesvec_avg(rsk59_short_momentum):The momentum indicator measures daily shorting and covering events relative to the market float.vec_avg(rsk59_shortinterestnotional):Real-time Short Interest * Security Price (USD)vec_avg(rsk59_shortinterestpct):Real-time Short Interest expressed as a Percentage ofequity float (Multiply by 100 to see in percent)vec_avg(rsk59_squeeze_risk):Multi-factor model which ranks the potential short squeezability of a security based on its short interest, float, stock loan liquidity, trading liquidity, and mark-to-market profitability.
```

这是AI给出的经济学逻辑

```
1. 轧空风险模板 (SqueezeRiskTemplate)经济学逻辑轧空（Short Squeeze）• 是指当股票价格开始上涨，卖空者被迫平仓（买入股票）从而进一步推高股价的现象。这通常发生在卖空比例很高、借贷成本上升、且股价开始上涨的情况下。核心逻辑：卖空者看跌股票，借入股票卖出，期望未来以更低价格买回归还。但如果股价上涨，卖空者面临亏损，可能被迫买入股票平仓，从而推动股价进一步上涨。因此，具有高轧空风险的股票（卖空比例高、借贷成本高、流动性差等）在未来可能出现上涨。为什么可能有效：行为金融学：卖空者面临风险，当股价上涨时，他们可能恐慌性平仓，导致股价超调。市场微观结构：高卖空比例意味着未来有大量潜在买盘（平仓需求），一旦价格上涨，可能触发连锁反应。信息不对称：卖空者可能掌握负面信息，但如果正面信息出现，卖空者可能措手不及，被迫平仓。关键指标：轧空风险评分（squeeze_risk）：综合了卖空比例、流动性、借贷成本等因素。卖空比例（short_interest_pct）：卖空股数占流通股的比例，比例越高，轧空风险越大。平仓天数（days_to_cover）：卖空股数除以平均交易量，表示平仓所需天数，天数越多，轧空风险越大。2. 卖空拥挤度反转模板 (CrowdingReversalTemplate)经济学逻辑卖空拥挤• 指过多投资者卖空同一只股票，导致卖空交易过度拥挤。当卖空拥挤度达到极端水平时，股票可能被过度做空，任何正面消息或市场情绪转变都可能引发大幅反弹。核心逻辑：过度拥挤的卖空交易可能导致股票价格被过度压低，脱离其基本面价值。当市场情绪转变或出现正面消息时，卖空者可能同时平仓，导致价格快速反弹。因此，卖空拥挤度高的股票在未来可能出现反转上涨。为什么可能有效：行为金融学：投资者情绪和羊群行为导致过度反应，随后出现反转。市场微观结构：拥挤的卖空交易可能导致流动性不足，加剧价格波动。风险溢价：卖空拥挤的股票可能承担额外的风险，投资者要求更高的预期收益，但实际可能因反转而获得高收益。关键指标：卖空拥挤度评分（crowded_score）：综合了卖空比例、流动性、换手率等。卖空比例变化（dtc_daily_chg）：平仓天数的日变化，反映卖空活动的变化速度。3. 借贷成本模板 (BorrowingCostTemplate)经济学逻辑股票借贷成本• 是卖空者借入股票所需支付的费用。借贷成本高通常反映股票借入困难（供给少）或卖空需求大。高借贷成本会侵蚀卖空者的利润，从而抑制卖空活动。核心逻辑：高借贷成本意味着卖空该股票的成本很高，这会减少卖空活动，从而减少卖压。同时，高借贷成本也可能反映市场对该股票的悲观情绪，但过高的成本可能使得卖空者望而却步，甚至促使现有卖空者平仓。因此，借贷成本高的股票未来可能表现较好（因为卖压减少）或表现较差（因为市场悲观），但通常我们关注的是前者，即高借贷成本可能预示股价上涨。为什么可能有效：市场微观结构：借贷成本是卖空交易的重要成本，影响卖空者的决策。信息传递：高借贷成本可能表明股票借入困难，可能是由于大股东不愿出借（看涨）或卖空需求过大。但过高的借贷成本可能意味着卖空过度，容易出现轧空。供需关系：股票借贷市场的供需失衡会影响借贷成本，进而影响卖空活动。关键指标：借贷费率（bid_rate）：多头出借股票获得的费率，即卖空者支付的费率。可用数量（indicative_availability）：可借股票数量，数量少则借贷成本高。总结这三个模板都基于卖空交易的相关数据，从不同角度捕捉卖空行为对股价的影响。它们有效的共同前提是市场并非完全有效，卖空者行为会受到影响，并且可能产生连锁反应。然而，这些因子的有效性也取决于市场环境、投资者结构和制度因素。因此，在实际应用中，需要结合具体市场进行测试和调整。值得注意的是，这些因子可能在某些市场环境下表现较好（如市场上涨时，轧空风险因子可能表现好），而在另一些环境下表现较差。因此，我们可以通过条件模板来根据市场状态选择因子，提高因子的适应性。在构建因子时，我们还需要注意风险控制，比如行业中性化、市值中性化等，以避免因子暴露于某些行业或风格。同时，通过衰减平滑因子信号，可以降低换手率，提高因子的实际可行性。最后，回测和实盘可能存在差异，因此需要谨慎评估因子的稳定性和持续性。建议在样本外数据和实盘中进一步验证因子的有效性
```

这是我在另外一个AI的帮助下，提出的五个疑问：

```
❓ 疑问1：流动性陷阱问题：如果股票本身流动性差，即使有轧空风险，也无法形成有效交易应对：加入volume过滤条件​❓ 疑问2：基本面恶化问题：高卖空可能反映公司真的有问题，不是错杀应对：结合基本面指标（如盈利能力）双重验证​❓ 疑问3：行业特征问题：某些行业（如新能源）天然高卖空，与其他行业不可比应对：行业中性化处理​❓ 疑问4：信号衰减问题：轧空是突发事件，信号可能快速失效应对：短期持有 + 时间衰减​❓ 疑问5：市场环境依赖问题：熊市中轧空效应可能失效（整体下行压力大）应对：可选的市场环境过滤（进阶版）
```

和AI讨论后，AI给出的几个模板：

```
#### 版本1：最简版，太粗糙，未考虑任何风险rank(vec_avg(rsk59_squeeze_risk))​#### 版本2：加入流动性过滤​if_else(    volume > ts_mean(volume, 20) * 0.5,    rank(vec_avg(rsk59_squeeze_risk)),    NaN)​#### 版本3：加入行业中性化 （行业内部比较，避免行业偏差）if_else(    volume > ts_mean(volume, 20) * 0.5,    group_neutralize(        rank(vec_avg(rsk59_squeeze_risk)),        sector    ),    NaN)​#### 版本4：加入时间衰减（最终版， 信号平滑，降低换手率）if_else(    volume > ts_mean(volume, 20) * 0.5,    ts_decay_linear(        group_neutralize(            rank(vec_avg(rsk59_squeeze_risk)),            sector        ),        5    ),    NaN)​​#### 版本5：进阶版（可选， 加入基本面保护，只在ROA较好的公司中应用）if_else(    (volume > ts_mean(volume, 20) * 0.5) & (rank(roa) > 0.3),  # 流动性 + 基本面    ts_decay_linear(        group_neutralize(            rank(vec_avg(rsk59_squeeze_risk)),            sector        ),        5    ),    NaN)
```

这是最终AI写的模板和推荐字段：

```
### 最终模板template_base = """if_else(    volume > ts_mean(volume, {window}) * {threshold},    ts_decay_linear(        group_neutralize(            rank(vec_avg({field})),            sector        ),        {decay}    ),    NaN)"""​### 可替换字段列表​| 原始字段 | 替代字段1 | 替代字段2 | 适用场景 ||---------|----------|----------|---------|| `squeeze_risk` | `crowded_score` | `shortinterestpct` | 不同卖空维度 || `sector` | `bucket(rank(cap), ...)` | `industry_group` | 不同分组方式 || `volume` | `turnover` | `dollar_volume` | 不同流动性指标 |
```

# 3. 总结

最会总结下，上述几步中，理解经济学逻辑，提出质疑这一步对个人成长最关键，尽量别偷懒了。为了更好的理解经济学逻辑，还是得补充经济学知识。 附上AI给我制定的学习计划(每天一小时)：

```
"第1-2周：夯实基础": [    "1. 精读《Active Portfolio Management》第1-4章",    "2. 理解夏普比率、信息比率、最大回撤等核心指标",    "3. 掌握10个最常用的操作符：rank, ts_delta, ts_mean, ts_std_dev, group_neutralize等",    "4. 实现5个经典因子：动量、反转、价值、质量、规模",],​"第3-4周：中级技巧": [    "1. 学习《Advances in Financial Machine Learning》前5章",    "2. 掌握特征工程：滞后、差分、标准化、非线性变换",    "3. 学习组合优化：多因子组合、风险平价、Black-Litterman",    "4. 实现行业中性化、市值中性化、贝塔中性化",],​"第5-6周：高级策略": [    "1. 学习市场状态识别：趋势市、震荡市、恐慌市",    "2. 掌握条件因子：不同市场环境用不同因子",    "3. 学习风险管理：VaR、CVaR、最大回撤控制",    "4. 实现自适应Alpha：根据市场波动率调整因子权重",],
```

---

## 讨论与评论 (8)

### 评论 #1 (作者: QL88701, 时间: 3个月前)

能不能给一些这个模板跑下来的实际例子，因为现在模板太多了，特别是有了ai之后。

=================================================== 每日谨记：提交因子不能抱侥幸心理！！坚持一定会有结果！！===================================================

---

### 评论 #2 (作者: XB37939, 时间: 3个月前)

思路不错 但是可能成果不是很大，还是要根据不同的数据类型设置不同的模板才行

#========= WORLDQUANT BRAIN CONSULTANT ========== #
#每天进步一点点，加油
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%

# sys.setrecursionlimit(α∞)

# PnL = ∑(Robustness * Creativity)

#无限探索、鲁棒性优先，创新性增值

#=================加油每一天=======================#

---

### 评论 #3 (作者: LY52969, 时间: 3个月前)

感谢分享，深受启发，看来我AI用的还是太盲目了

---

### 评论 #4 (作者: WT26072, 时间: 3个月前)

这个流程说的好详细啊，给了我一些动力，感觉还是得学习下金融知识。而且下面的佬有说要按照数据集去分类模板，给了我一些想法。感谢🙏不知道佬用的什么ai呢

---

### 评论 #5 (作者: MZ45384, 时间: 3个月前)

太优秀了！整篇看下来，大佬有着一定的量化投资知识，因此可以跟AI进行更有效更高质量的互动交流，以大佬的耐心，想做出大量且diverse的优秀模板并不困难。加油！！！

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #6 (作者: CZ39633, 时间: 3个月前)

====================================================================================
大佬的分析很到位，让我认识到alpha的构建还是要对自己进行进一步对金融知识的学习

================================自信人生两百年，会当水击三千里==========================

---

### 评论 #7 (作者: ST61360, 时间: 3个月前)

文档写很详细，收获良多，结尾还送了一个模版，谢谢分享。

---

### 评论 #8 (作者: DQ66419, 时间: 2个月前)

感谢大佬分享，提供了一些思路，祝大佬多多出货。

======日日精进，步步为营，积蓄力量，静待花开。Strive daily, advance step by step, gather strength, and wait for the flowers to bloom.======

---

