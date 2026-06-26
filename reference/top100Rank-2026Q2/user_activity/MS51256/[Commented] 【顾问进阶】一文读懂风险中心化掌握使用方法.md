# 【顾问进阶】一文读懂风险中心化，掌握使用方法

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwgXTPlUsyA6D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAfpodHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzU5NTQ1OTY4NTg5MDMtLSVFOSVBMSVCRSVFOSU5NyVBRSVFOCVCRiU5QiVFOSU5OCVCNi0lRTQlQjglODAlRTYlOTYlODclRTglQUYlQkIlRTYlODclODIlRTklQTMlOEUlRTklOTklQTklRTQlQjglQUQlRTUlQkYlODMlRTUlOEMlOTYtJUU2JThFJThDJUU2JThGJUExJUU0JUJEJUJGJUU3JTk0JUE4JUU2JTk2JUI5JUU2JUIzJTk1BjsIVDoOc2VhcmNoX2lkSSIpNmU4OTczZDgtMDg4YS00NTVhLWFhNzItMzgzNWZjNTcxYTliBjsIRjoJcmFua2kLOgtsb2NhbGVJIgp6aC1jbgY7CFQ6CnF1ZXJ5SSIMTVM1MTI1NgY7CFQ6EnJlc3VsdHNfY291bnRpLQ%3D%3D--f82996e5fa1f163cc69b0758eb8c67e0fd607518
- **作者**: MH33574
- **发布时间/热度**: 7个月前, 得票: 54

## 帖子正文

今天早上收到公告通知11月起，PowerPool将仅接受风险中性化的因子，顾问仍然可以使用其他的非风险中性化（MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY) 回测，但只有符合RA标准的才可以提交。很多新顾问可能还不太熟悉风险中性化这个概念，希望这篇文章对你有帮助1. 什么是风险中性化？定义：“风口来了猪都可以飞上天”，风险中性化就是在去除已知的“风”。 风险中性化是一种通过消除特定风险因子对Alpha影响的技术，使Alpha的表现更加纯粹，专注于捕捉市场异常。通过风险中性化，可以剔除市场、行业或风格因子等已知风险对Alpha收益的干扰，从而更准确地评估Alpha的独立性和有效性。理论背景：风险因子是影响资产收益的主要驱动因素，例如市场风险、行业风险、动量因子等。经典理论：Fama-French三因子模型（市场、规模、价值）和套利定价理论（APT）为风险因子模型奠定了基础。2. 为什么要做风险中性化？消除已知风险因子的干扰：如果Alpha的收益完全由已知风险因子解释，则其价值有限，因为这些因子可以通过简单的模型复制。风险中性化可以帮助研究者专注于Alpha捕捉的独特市场异常。降低风险：减少因风险因子回撤或波动性导致的潜在损失。提高Alpha在不同市场条件下的稳健性。提升Alpha性能：通过剔除不必要的风险因子，提高Alpha的Sharpe比率，减少回撤，并优化换手率与交易成本之间的平衡。3. 风险中性化的好处更高的Alpha独立性：通过剔除风险因子，Alpha表现更独立，能够更好地反映其捕捉市场异常的能力。降低拥挤交易风险：减少因市场中大量投资者持有相似头寸而导致的价格剧烈波动。增强多样性：通过不同的风险中性化方法，生成多样化的信号，丰富Alpha池。优化长期表现：在保留Alpha收益的同时显著降低风险，提供更稳定、可靠的长期表现。4. 如何使用风险中性化？界面操作：在BRAIN平台的回测界面中，进入模拟设置（Simulation Settings），在Neutralization选项中选择对应的风险中性化方法，BRAIN平台内置了六种风险中性：FAST, SLOW, SLOW_AND_FAST, CROWDING, STATISTICAL, REVERSION_AND_MOMENTUM (RAM)API操作：在API中，通过调整代码中的neutralization参数实现。例如{"instrumentType": "EQUITY","region": "USA","universe": "TOP3000","delay": 1,"decay": 0,"neutralization": "FAST",  // 替换为上述对应的风险中性化方法"truncation": 0.1,"pasteurization": "ON","unitHandling": "VERIFY","nanHandling": "ON","language": "FASTEXPR","visualization": false}5. 不同的风险中性化方法及其使用场景以下是平台支持的六种风险中性化方法的详细介绍：5.1 FAST定义：快速因子（Fast Factors）包括市场和行业风格因子，和高换手率的风格因子，例如反转因子。适用场景：高换手率信号。需要捕捉短期市场趋势的Alpha。注意事项：使用FAST中性化可能会增加Alpha的换手率。5.2 SLOW定义：慢速因子（Slow Factors）包括低换手率的风格因子，例如价值因子。适用场景：低换手率信号。更关注长期趋势的Alpha。注意事项：SLOW因子适合稳健型投资策略。5.3 SLOW_AND_FAST定义：结合了慢速因子和快速因子的综合模型。适用场景：需要同时考虑短期和长期趋势的Alpha。适合多样化的投资策略。注意事项：可能会增加换手率，但能更全面地中性化风险。5.4 RAM（Reversion and Momentum）反转因子（REVERSION）：捕捉短期均值回归现象（如5天内的价格回调）。定义：市场通常会对短期事件过度反应，导致暂时性错误定价。随着这些市场效率的修正，超卖的股票价格恢复，超买的股票价格回落。短期反转因子捕捉股票价格的均值回归现象，即近期表现不佳的股票往往在未来获得更高的回报，而近期表现较好的股票可能会出现回调。动量因子（MOMENTUM）：捕捉长期价格趋势（如12个月内的价格趋势）。动量因子识别股票价格的持续趋势，即近期表现较好的股票往往继续上涨，而表现较差的股票则可能继续下跌。基于趋势跟随原则，已建立的价格趋势更可能延续而非逆转适用场景：需要对冲短期均值回归和长期动量趋势的Alpha。注意事项：RAM中性化适用于多空平衡的Alpha。建议结合Alpha的特性，评估其是否容易受到反转或动量因子的影响。5.5 CROWDING定义：拥挤风险中性化，控制因市场中大量投资者持有相似头寸而导致的风险。随着更多投资者进入相同的头寸，交易的盈利能力可能下降。虽然价格在初期可能上涨，但随后可能变得脆弱，容易出现大幅下跌。适用场景：需要减少拥挤交易风险的Alpha。当过多投资者同时试图卖出相同的头寸时，价格可能迅速下跌，导致更大的损失。适合在动量趋势强烈的市场中使用。注意事项：拥挤风险中性化适用于多空平衡的Alpha。需要结合Alpha的特性，评估其是否容易受到拥挤交易的影响。5.6 STATISTICAL定义：因子模型的两大类别：基本面因子模型（Fundamental Factor Models）和基于统计因子模型（Statistical Factor Models），其中第二种使用统计技术（如主成分分析PCA或聚类分析）分析证券收益，识别市场数据中的模式和关系。依赖历史收益数据，通过统计方法预测未来表现或优化投资组合风险。经典案例比如：Roll和Ross的《套利定价理论的实证研究》（APT），强调使用统计方法提取影响资产收益的多个因子。适用场景：捕捉复杂非线性关系的Alpha，生成在特定收益空间中表现良好的信号。注意事项：统计风险中性化依赖于历史数据，可能对数据质量较为敏感。建议结合Alpha的特性，评估其是否适合统计模型的应用。6. 总结风险中性化的核心价值：通过剔除已知风险因子，优化Alpha表现，降低风险。选择合适的方法：根据Alpha的特点（如换手率、风险敞口）选择合适的风险中性化方法。个人建议：在Simulation中先抽样一部分，尝试不同的风险中性化设置，评估其对Alpha表现的影响，选择最合适的再进行全量的回测英文原版文档阅读：Getting Started: Risk Neutralized Alphas | WorldQuant BRAINGetting Started with Risk Neutralized Metrics | WorldQuant BRAINGetting Started with Crowding Risk-Neutralized Alphas | WorldQuant BRAINGetting Started with Statistical Risk-Neutralized Alphas | WorldQuant BRAINGetting Started with RAM Risk-Neutralized Alphas | WorldQuant BRAIN

---

## 讨论与评论 (22)

### 评论 #1 (作者: SX13432, 时间: 7个月前)

大佬的总结真是及时又全面，点赞！~感觉以后风险中性化要成为趋势~五大区所有中性化API代码如下，包括六个风险中性化。经常看到有人在群里问，也贴出来共享~===================更多ATOM，分析数据、多样性、稳健性===================RegionDelayNeutralizationUSA1['NONE', 'REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'COUNTRY','FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']USA0['NONE', 'REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'COUNTRY','FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']GLB1['NONE', 'REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'COUNTRY','FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']EUR1['NONE', 'REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'COUNTRY','FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']EUR0['NONE', 'REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'COUNTRY', 'FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']CHN1['NONE', 'REVERSION_AND_MOMENTUM', 'CROWDING', 'FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']CHN0['NONE', 'REVERSION_AND_MOMENTUM', 'CROWDING', 'FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']ASI1['NONE', 'REVERSION_AND_MOMENTUM', 'STATISTICAL', 'CROWDING', 'COUNTRY','FAST', 'SLOW', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY', 'SLOW_AND_FAST']

---

### 评论 #2 (作者: JW44543, 时间: 7个月前)

写的非常清晰明白，刚刚成为顾问两天也能看的懂，感谢大佬分享！

---

### 评论 #3 (作者: WD55783, 时间: 7个月前)

回测中使用风险中性化设置能剥离市场、行业、风格这些系统性风险因子的干扰，让 alpha更聚焦于自身的特质，不会因为依赖某类风格的阶段性行情。是否可以推导出，日常提交的alpha大量采用风险中性化设置，可以减小过拟合的概率，进而让提交的alpha在未来有更好的表现

---

### 评论 #4 (作者: SZ20589, 时间: 7个月前)

PowerPool将仅接受风险中性化的因子，顾问仍然可以使用其他的非风险中性化（MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY) 回测，但只有符合RA标准的才可以提交。之前交的ppa和atom以及regular alpha从来没有试过风险中心化。这次正好可以试试了。减小过拟合的概率，进而让提交的alpha在未来有更好的表现

---

### 评论 #5 (作者: RM49262, 时间: 7个月前)

=====================================评论区=========================================感谢大佬分享！各类Risk-neutralization的适用因子写的很清楚，这样就可以有的放矢地针对性的选择适合的中性化类型了！===================================================================================

---

### 评论 #6 (作者: CL86067, 时间: 7个月前)

感谢大佬的分享，太有帮助了，最近几周都是风险中性化主题，所以也算试着用了这些这些风险中性化设置，但是完全不懂各种的区别，大佬的分享科普真的及时，顺便问一下会不会不同数据集或者不同区域可能适合不同的风险中性化呢？

---

### 评论 #7 (作者: KH94146, 时间: 7个月前)

CL86067和数据集无关，羊肉可以爆炒，可以涮锅，可以葱爆，可以孜然

---

### 评论 #8 (作者: YQ76635, 时间: 7个月前)

嗯，作者真的很厉害，我也知道自己的差距了。而且写的非常清晰，我对各项中性化的选项也更加清晰了。

---

### 评论 #9 (作者: YX86102, 时间: 7个月前)

非常感谢大佬的分享，对分享中性化的理解程度又更加提高了！！！风险中性化可以帮助研究者专注于Alpha捕捉的独特市场异常。减少因风险因子回撤或波动性导致的潜在损失。提高Alpha在不同市场条件下的稳健性。通过剔除不必要的风险因子，提高Alpha的Sharpe比率，减少回撤，并优化换手率与交易成本之间的平衡。看来是很有必要的！===========================================================================努力~加油~超越~ ！！！===========================================================================

---

### 评论 #10 (作者: HJ70296, 时间: 7个月前)

=====================================评论区=========================================十分感谢大佬分享！收到仅可提交中性化的PPA的邮件后很是困扰，之前参加主题都是随机挑选进行风险中性化，看了大佬的分享后，感觉有点思路了，真是太感谢了！！！===================================================================================

---

### 评论 #11 (作者: JX14975, 时间: 7个月前)

大佬能分享一下slow、fast、slow_and_fast 这三种中性化目前在GLB区域的成功率（不至于因为running too long 或者 take too much sources 而失败的概率）吗？我记得GLB比赛时单槽回测 fast 或 sliow 也会失败，现在情况如何，有什么优化的巧思吗？

---

### 评论 #12 (作者: MY82844, 时间: 7个月前)

风险中性化，一般对于return和margin会有啥影响？

---

### 评论 #13 (作者: HX88270, 时间: 7个月前)

大家都开始测了没，选哪个指标更优秀

---

### 评论 #14 (作者: GY56717, 时间: 7个月前)

学习了， 原来如此， 我之前一直没懂我要如何改变我的simulation，谢谢大神

---

### 评论 #15 (作者: QW78773, 时间: 7个月前)

非常好的总结，让我的理解又深了一步

---

### 评论 #16 (作者: YH87796, 时间: 7个月前)

===================================================================================太感谢大佬的分享了，PPAC该规则之后还不知道风险中性化到底是什么意思，今天读了这篇文章终于搞懂了。后面得开始实操尝试了==============================================================================

---

### 评论 #17 (作者: BW14163, 时间: 7个月前)

非常有价值的分享，讲解了WQ风险中性化的核心概念与实操方法，极大的节约了user需要上网查资料的时间。风险中性化通过剔除市场、行业、风格等已知风险因子，提升Alpha的独立性与稳健性。WQ提供FAST、SLOW、RAM等六种方法，应根据因子换手率、周期特性选择适配中性化方式，并通过小样本测试筛选最优方案，避免盲目全量回测。**********************************紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。每当遇到一个RA时，不要忘了在ppac中捡垃圾的日子。**********************************

---

### 评论 #18 (作者: DH50144, 时间: 7个月前)

有完整的check PPAC的代码不，一个API模块感觉没法串接

---

### 评论 #19 (作者: XL98962, 时间: 7个月前)

学习了， 感谢分享， 让我有了新的角度***************************************************紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。每当遇到一个RA时，不要忘了在ppac中捡垃圾的日子。***************************************************

---

### 评论 #20 (作者: XW90844, 时间: 7个月前)

官方文档的介绍As a rule of thumb,we recommend adopting the Slow Factors for low-turnover signals and Fast Factors or Slow + Fast factors for high-turnover signals. The Slow + Fast Factors incorporates both of the above factors together.但在实际回测中发现并非如此。我现在做法是对每个alpha的核心信号，把6各种风险中性化方式都试一下，找表现最好的一种然后再在此基础上大规模回测。不知道还有没有更好的方法，或者具体选择的建议。However, there is no universal rule as to which alpha should apply certain risk factors. We recommend giving them a try and finding the most suitable risk factors for your needs.

---

### 评论 #21 (作者: MS51256, 时间: 6个月前)

===============================MS51256的评论===============================感谢大佬的科普，写的非常详细，选好neut 不仅可以有效的提升alpha 的表现还可以降低pc以获取更丰厚的base，此外中性化不应该集中于某几个，要多用多种不同的中性化，不能只会三板斧。================================Do your best ================================

---

### 评论 #22 (作者: ZZ26913, 时间: 6个月前)

感谢对于官方原文的总结，节省了大量的阅读时间，这下对于风险因子的中性化便有了较为清晰的理解。

---

