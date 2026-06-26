# 关于冲Pyramid的一点心得

- **链接**: [Commented] 关于冲Pyramid的一点心得.md
- **作者**: JL11546
- **发布时间/热度**: 1年前, 得票: 15

## 帖子正文

大家好。最后半个月计划冲一下Master试试。这周我用了5天时间获得了10个Pyramid，达到了Master级别。分享一些冲Pyramid的思考，希望能对各位有所帮助。

1. 优先选择一些包含多个catergories的模板。有些模板跑出一个alpha可以获得两个甚至三个categories，这会显著提高我们点亮Pyramid的效率。比如@TL87739同学提供的模板效率就很高：

```
regression_neut(group_zscore(group_neutralize(ts_zscore(ts_backfill({data1},120),120),densify(bucket(rank(ts_backfill({market_cap or enterprise_value or revenue or sales},120)),range='0,1,0.1'))),densify(industry)),group_neutralize(ts_zscore(ts_backfill({{market_cap or enterprise_value or revenue or sales}},120),120),densify(industry)))
```

这个模板选择analyst和model字段可以同时获得fundamental的category，并且这个模板在ASI, CHN, KOR, TWN, HKG这几个region的效率都很不错。

2. 一个模板如果跑了5000个simulations以上还没有信号就尽快更换模板，不要在一个模板上浪费时间。我这5天使用了9个模板，其中只有4个模板挖到了alpha。如果在一个模板上纠结可能会浪费大量的时间

3. 使用多线程进行回测，能显著提升效率，代码我参考的这篇文章。

[使用协程方式提高Multi-simulation效率代码框架分享](/hc/en-us/community/posts/28236334008855-%E4%BD%BF%E7%94%A8%E5%8D%8F%E7%A8%8B%E6%96%B9%E5%BC%8F%E6%8F%90%E9%AB%98Multi-simulation%E6%95%88%E7%8E%87%E4%BB%A3%E7%A0%81%E6%A1%86%E6%9E%B6%E5%88%86%E4%BA%AB)

4. 对因子的调整：

（1）可以使用hump，ts_delta_limit降低turnover；

（2）可以使用signed_power和trade_when降低IS_Ladder和Prod_Corr；

（3）CHN的字段如果各项标准差的不多可以尝试降低Decay，使用Crowding的中性化尝试挽救一下；

5. 放弃一些region和categories。我发现我在Delay0的全部,region Delay1的EUR, JPN, AMR这几个region里面挖到的Alpha数量寥寥无几，所以我放弃了上述的region，并且优先跑了analyst, model, fundamental, pv这些categories。另外sentimen比较意外的好出alpha，值得尝试。

以上就是我的在冲Pyramid中的一点心得，祝各位都能获得自己期望的Genius Level！

---

## 讨论与评论 (8)

### 评论 #1 (作者: WP88606, 时间: 1年前)

请问ts_delta_limit如何设置可以降低turnover？

---

### 评论 #2 (作者: KH94146, 时间: 1年前)

[WP88606](/hc/en-us/profiles/27032592505751-WP88606)

在 learn operator里搜索  可以看到更多的解释，具体的tvr参数就是你目标的turnover

---

### 评论 #3 (作者: WP88606, 时间: 1年前)

感谢分享！找见了。降低turnover补充一点，还可以将settings里的decay设置为0，代码里使用ts_decay_exp_window，对sharpe的影响可能会变小。

---

### 评论 #4 (作者: JL11546, 时间: 1年前)

[WP88606](/hc/en-us/profiles/27032592505751-WP88606)

我理解这个操作符是用于限制 Alpha 的仓位（Position）在两个日期之间的变化幅度，确保因子信号的调整不会导致过大的交易量或风险。比如，ts_delta_limit(x, y, limit_volume=0.1)，x是alpha表达式；y是成交量的表达式比如adv20或者一个常数，例如1000万；limi_volume是y这个参数的比例。合并起来就是这个因子在单日做多/做空的头寸不能超过y这个成交量的10%。

---

### 评论 #5 (作者: XX42289, 时间: 1年前)

现在pyramids是最简单的一个指标了，真正难的是最后的排名，建议看一下。现在达成master的有533人，很难脱颖而出，一定要排名够高才行，名额可能只有95个左右。所以得加油了，除了pyramids，还要关注另外六个指标。

per ops，5～7之间是比较好的
per field 2.5～3.0之间就比较好
ops数量在125比较好（因为越南有一个团队在这里集中占了20个名额）
fields数量要在450以上
activity 50-100以上
referal=1就行
最大连续那个一辈子都不可能超越前面那几个人，不用想了

---

### 评论 #6 (作者: ZS59763, 时间: 1年前)

很好的评论，点赞。

---

### 评论 #7 (作者: YW26515, 时间: 1年前)

很有启发，谢谢前辈的经验分享。
我们现在一天最多交4个，Pyramid则需要3个才可以，前辈如何做到一个alpha跨两个Pyramid的，🙏

---

### 评论 #8 (作者: JL11546, 时间: 1年前)

[YW26515](/hc/en-us/profiles/29331368412951-YW26515)  你好，你可以使用二阶模板，这样就是主信号一个category，分组数据一个category，可以一次点两个Pyramid。不过要注意平台最新规则是一个因子最多只可以点两个Pyramid，如果你的因子可以点超过2个，那么哪个Pyramid都不会被增加。

---

