# 【WorldQuant新手攻略】经验分享和常见问题解答

- **链接**: [Commented] 【WorldQuant新手攻略】经验分享和常见问题解答.md
- **作者**: WS55742
- **发布时间/热度**: 1年前, 得票: 73

## 帖子正文

## 经验分享

### 数据处理：

处理覆盖率低的数据：ts_backfill

处理波动性大的数据：winsorize

### 新手推荐的模板：

商誉对销售额比率：

【Alpha灵感】 看不见的负担

【Alpha灵感】GTS Factor

【Alpha Idea】商誉、过度自信与股票回报

这三篇都讲的是同一个主信号，很容易出alpha，也可以三篇对照着一起看，然后自己做尝试，能做出很多alpha。

其他推荐：

【Alpha灵感】A股恐慌度因子在美股的应用

【Alpha灵感】新闻动量文章启发的反转策略实现

因为这几篇较为简单，所以更适合新手阅读，合集中其他文章也都值得一读。

### 交更多 alpha 的技巧：

交alpha：对于同一个模板，先交低sharp，再交高于10%的，如此可以交很多Self-correlation高于0.7的。(当然这是因为用户阶段的质量是不计入顾问阶段的且Self-correlation检测不严格，所以交的越多越好，然而获得顾问权限后应尽量避免使用此技巧。)

## 改进 alpha 的技巧：

### 降低 turnover

1. 增加 decay（但是太大的衰减值将削弱信号）

2. 使用 trade_when 或 hump

3. 和 turnover 低的alpha结合

4. 使用流动性低的universes，如TOP3000

5. 使用更长的时间，如252

### 降低 Weight concentration

1. 添加范围归一化函数（例如 rank ）

2. 减小 truncation

3. 使用 ts_backfill

### 提高Sharpe

1. 增加return

2. 降低波动性

可尝试使用  [neutralization](https://platform.worldquantbrain.com/learn/documentation/advanced-topics/neut-cons)

使用trade_when，winsorize

### 使 PnL 曲线更平滑

1. 减小 truncation

2. 进行数据处理

### 增加 returns

1. 提高 turnover

2. 减小 decay

3. 使用流动性低的universes

### 降低 correlation

1. 替换不同的数据字段和operators

2. 替换不同的分组方式，即修改group

（注：上面的改进技巧全部来自论坛其他帖子而非原创）

## 常见问题解答

【注意：以下内容为官方材料结合个人经验，不构成权威解答】

### 我是新手，应该从哪开始？

推荐先把文档读完  [https://platform.worldquantbrain.com/learn/documentation](https://platform.worldquantbrain.com/learn/documentation)

公开课《零基础学量化》，上课并完成作业。

[中文论坛](/hc/en-us/community/topics/12913416465431-%E4%B8%AD%E6%96%87%E8%AE%BA%E5%9D%9B) 有丰富的资源，置顶都是很精彩的文章，值得精读，也有很多分享，可以泛读，community中也有很多其他资源，例如  [BRAIN TIPS](/hc/en-us/community/topics/18068926798871-BRAIN-TIPS) 。

### 有问题应该去哪里提问？

- 直播课结束老师一般会答疑。

- 在论坛帖子的评论区。

（有问题可以在此文评论区提出，我知道的话一定会回答的。）

如果对平台有疑问或申请过程遇到困难可以邮件至中国区官邮  [mainlandchina@worldquantbrain.com](mailto:mainlandchina@worldquantbrain.com)  询问。

### 我已经达到10000分，等待阶段可以做什么？

1. 交够100个alpha，因为用户阶段的alpha数量和顾问alpha一起计数，到100个可以解锁superalpha权限，且对用户而言交alpha更简单，所以交够100对进入顾问的长远发展有帮助。

2. 积累自己的模板，通过阅读论坛的资料总结笔记。

3.分享自己的经验，发布在论坛。

### 怎么找/使用模板和Alpha灵感？

对于 [【Alpha灵感启示录】合集（持续更新收录中） – WorldQuant BRAIN](../PN39025/[Commented] 【Alpha灵感启示录】合集持续更新收录中置顶的被推荐的.md) 主要看 USA-D1 。

- 其中有些文章给出了表达式，可以先根据给出的思路自己尝试写alpha然后和作者对比，思考哪里写的不够好；
- 有些只给出了思路，可以尝试自己写，然后向ai提问，可以看 [【学习资料】BRAIN小贴士(这里有你想要的硬核内容！持续周更中） – WorldQuant BRAIN](/hc/en-us/community/posts/15152019662487--%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99-BRAIN%E5%B0%8F%E8%B4%B4%E5%A3%AB-%E8%BF%99%E9%87%8C%E6%9C%89%E4%BD%A0%E6%83%B3%E8%A6%81%E7%9A%84%E7%A1%AC%E6%A0%B8%E5%86%85%E5%AE%B9-%E6%8C%81%E7%BB%AD%E5%91%A8%E6%9B%B4%E4%B8%AD)  见 小贴士20：使用GPT从研究论文中生成有洞见的思路 。

对于  [可以尝试使用的Alpha模板](../CT68712/[Commented] 可以尝试使用的Alpha模板置顶的.md) 可以直接发给ai，让ai解释模板的思路和使用方法。

在learn- Documentation-

[⭐ Alpha Examples for Beginners](https://platform.worldquantbrain.com/learn/documentation/create-alphas/19-alpha-examples)

[⭐ Alpha Examples for Bronze Users 🥉](https://platform.worldquantbrain.com/learn/documentation/create-alphas/sample-alpha-concepts)

[⭐ Alpha Examples for Silver Users🥈](https://platform.worldquantbrain.com/learn/documentation/create-alphas/example-expression-alphas) 中也有很多例子，可以根据文章的提示改进alpha，也可以将其作为模板。

### 为什么我的settings中没有CHN地区

目前所有 BRAIN 平台用户都可以使用的区域是美国（USA）市场。其他区域仅适用于顾问。

### “group_neutralize(x, group)”和“回测设置中的中性化”是否可以互换使用？

是的，例如：

alpha = -ts_returns(close,5)，在回测中设置Neutralization为industry与

alpha = group_neutralize(-ts_returns(close,5),industry)，设置Neutralization为“None”相同。

区别是group_neutralize可以在内部使用，更灵活。

### 《零基础学量化》公开课怎么报名？

- 直播：每次开课都会有邮件通知，留意邮箱。

### 使用代码回测，报错“no location”？

表达式或settings出错，复制相应表达式和settings到网页端回测找问题。

### 为什么报错“You have reached the limit of concurrent simulation”或“SIMULATION_LIMIT_EXCEEDED ”？

用户使用simulate最多可以同时回测3个alpha。

出现报错说明已经达到可以同时simulate的最多数量，只有等前面simulate的alpha的回测完成（即location达到100%）才能继续回测。

### 为什么会出现黄色提示“Incompatible unit for input at index 0…”？

这是单位警告，表面在算术运算中使用了单位不一致的字段。不过仅作为参考，并不会阻止提交。如果认为 Alpha 能够正确处理数据单位，可以放心忽略此警告。

#### 1. 什么情况下会出现此警告？

当您尝试对单位不同的字段进行算术运算时，系统会触发此警告。例如，在表达式 `close + adv20` 中：

`close` 是以美元（$）为单位的价格数据；

`adv20` 是以股份数为单位的成交量数据。

由于两者的单位不同（美元 vs. 股数），直接相加会导致单位不匹配，类似于尝试将“5秒”和“5摄氏度”相加，这在逻辑上是不合理的。

#### 2. 如何消除此警告？

可以尝试通过 `zscore` 等标准化方法处理数据，使其变为无量纲的值。例如，`zscore(close) + zscore(adv20)`。或者使用rank将字段转换为排名值后再进行运算。

### 如何通过sub-universe测试？

#### 1. 选择更大的 universe

#### 2. 避免在 Alpha 中使用与公司规模相关的乘数

例如 rank(-assets)、1–rank(cap)等（- rank(-assets)：倾向于给小市值公司更高的权重。1–rank(cap)：倾向于给大市值公司更低的权重。）。这些乘数可能会显著改变 Alpha 权重的分布，使其偏向更活跃或较不活跃的一侧，从而影响子宇宙的表现。

#### 3. 分别衰减信号的流动和非流动部分

**原因：**

流动性不同的股票对信号的响应可能不同。通过分别处理流动性和非流动性部分，可以更好地控制信号的表现。

方法：

使用流动性代理：例如市值（cap）或成交金额（volume\*close）。

分别衰减：对流动性和非流动性部分应用不同的衰减因子。

**示例：**

原始信号衰减：

`ts_decay_linear(signal, 10)`

改进后的信号衰减：

`ts_decay_linear(signal, 5) * rank(volume*close) + ts_decay_linear(signal, 10) * (1 – rank(volume*close))`

**解释：**

`ts_decay_linear(signal, 5) * rank(volume*close)`：对流动性较高的部分`（rank(volume*close) `较大）应用较短的衰减窗口（5）。

`ts_decay_linear(signal, 10) * (1 – rank(volume*close))`：对流动性较低的部分`（rank(volume*close) `较小）应用较长的衰减窗口（10）。

### vector类型的数据如何使用？

需要用vec_sum或vec_avg降维，详情见[ [Vector Data Fields 🥉 | WorldQuant BRAIN](https://platform.worldquantbrain.com/learn/documentation/understanding-data/vector-datafields)

### 为什么我的 alpha 回测这么慢？

回测速度取决于表达式的复杂程度及settings设置，回测在 Brain 平台的服务器进行，不取决于电脑配置，耐心等待即可。

### 怎么通过 alpha_id 找到对应 alpha？

随便打开一个alpha，在网址最后替换id
或者在  [https://platform.worldquantbrain.com/alpha/](https://platform.worldquantbrain.com/alpha/) 最后加上id

## 结语

这篇文章大部分是各方信息的总结，原创的并不多，感谢大家在论坛的分享，感谢老师的课程讲解，希望可以继续和大家一起进步！

分享到这就结束了，感谢你能看到这里，如果对你有帮助就点个赞吧，有任何问题欢迎在下方评论区留言，再次感谢观看。

---

## 讨论与评论 (8)

### 评论 #1 (作者: DM28368, 时间: 1年前)

ts_backfill and winsorize are two easy-to-use and relatively powerful join operators. Newcomers to WQ should use them! This also means it will help your referral accounts.

---

### 评论 #2 (作者: XD81759, 时间: 1年前)

感谢作者的分享，写得很详细

---

### 评论 #3 (作者: WT73952, 时间: 1年前)

多交alpha的小技巧非常实用！

---

### 评论 #4 (作者: WT73952, 时间: 1年前)

最近测试发现 low-sub-universe-sharpe 可以通过调整开仓和清仓条件去改善

---

### 评论 #5 (作者: BW14163, 时间: 1年前)

感谢分享，讲的非常细致。

---

### 评论 #6 (作者: ZZ37826, 时间: 9个月前)

======================感谢分享========================
真心感谢这篇干货，特别适合刚上BRAIN的新手，我现在是有条件顾问，但也学到了很多。

总结要点：
1、入门路径清晰：先系统读文档与公开课，再用论坛精华与合集搭建个人模板库。
2、数据处理有抓手：覆盖/缺失用ts_backfill，极值用winsorize，必要时做中性化以稳住波动。
3、灵感来源丰富：围绕商誉相关思路、恐慌度、新闻动量等，先按思路复现再对比优化。
4、交alpha有节奏：同一模板先交低夏再提升，利用用户阶段规则提高提交数量与自相关要求，顾问阶段再收敛质量。
5、优化维度明确：从换手、权重集中度、Sharpe、相关性四条线各有具体手段（decay、trade_when、rank、truncation、分组替换等）。
6、实操小技巧到位：子宇宙测试避开规模乘子影响，并发回测有上限，单位警告可通过标准化或rank化处理。
7、细节易忽略：group_neutralize与回测中性化效果可等价，USA为默认可用区域，alpha_id定位有简便路径。

我学到并准备这样做：
1、写表达式尽量先做rank或zscore处理，减少单位问题并提升稳健性。
2、在USA-D1上以“高低流动性分层衰减”的思路做一次完整实验，观察换手与收益的权衡。
3、用较小decay配合trade_when控制换手，再用合理truncation与数据处理让曲线更顺滑。
4、每次迭代都替换数据字段与分组，主动拉低与旧alpha的相关性，扩展组合多样性。

再次感谢你的分享，对我这种在BRAIN打基础的人非常有用，也欢迎继续更新更多细节实践。

================励志学习每一个优质帖子=================

---

### 评论 #7 (作者: CC85858, 时间: 9个月前)

======================------------========================----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

感谢帖子和评论区的分享，很受用。学到了处理单位不统一的处理方法：rank，zscore都可以

---

### 评论 #8 (作者: DZ67590, 时间: 8个月前)

感谢作者，基本上文章中解答的的每一个小点都是我遇到过的问题，所以一直在反复地阅读作者整理的这些内容，这些知识和技巧对于新手来说非常实用。

最近在大规模回测的过程中发现在选取好数据集并查看其特征之后，用文章最初给出的ts_backfill，winsorize这两个operator对数据集进行预处理对于因子的挖掘是非常有好处的。

---

