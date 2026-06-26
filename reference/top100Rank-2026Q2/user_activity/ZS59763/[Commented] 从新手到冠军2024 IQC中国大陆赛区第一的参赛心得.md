# 从新手到冠军：2024 IQC中国大陆赛区第一的参赛心得

- **链接**: [Commented] 从新手到冠军2024 IQC中国大陆赛区第一的参赛心得.md
- **作者**: WD90077
- **发布时间/热度**: 1年前, 得票: 64

## 帖子正文

在文章 [《2024 IQC中国大陆赛区第一的参赛收获分享》](../RM49262/[L2] 2024 IQC中国大陆赛区第一的参赛收获分享.md) 提到了自己通过参加国际量化挑战赛（International Quant Championship，IQC）成为BRAIN顾问经历及收获。我的专业背景并非STEM领域，而是经济学和商科，从业经历也与量化无关。第一次接触BRAIN，就是通过IQC。本文将进一步分享作为新手，面临开发alpha的问题。

首先，IQC是含金量高但非常新手友好的一个比赛。

含金量高是在于其因为是公开赛，理论上任何人都可以参加，规模之大，名声之大。而BRAIN的其他比赛例如MAPC都是内部赛，仅限BRAIN顾问参加。但又因为不限背景参加，所以在IQC在很多方面的设置，都体现出对新手高度友好，主要体现在：

1.允许组队，每支队伍允许同校的1-4人参加，并且同校不仅是同校的在校生，同校的老师﹑校友等也可以参加，这在一定程度上克服了单人成队的劣势。

2.比赛时间长，整个IQC长达数月，让各个队伍都有充足的时间去发挥“后发优势”，即使在前期没有提到足够多的alpha，也可以通过持久战，慢慢追赶，调整策略，去逆风翻盘的，即使是纯小白，也有充裕的时间去学习。不像其他的内部赛，只有大概一个半月的时间，可能前几天落后了，后期就比较难追赶。

3.alpha提交标准的相对宽松，例如在alpha的相关性方面仅看Self Correlation，不看Prod Correlation，所以可以参考甚至模仿一些公开的或已知的alpha（或alpha模板），无需担心从0到1去做alpha。

4.可用的dataset相对顾问的较少，但都是容易出信号的dataset，并且这些dataset里datafield含义都是相对容易理解的，避免了新手在庞大数据中迷失方向。

5.BRAIN提供的三件套课程：《零基础学量化》《带你读论文》及线下短训营，以及老师们的指导﹑社区的分享﹑研究小组的交流等，是可以为新手提供足够的入门甚至进阶支撑的。

其次，需要考虑两个关键问题：alpha的数量和质量。

一﹑关于数量问题，我自己当时参赛alpha的来源主要是以下两个：

1.BRAIN提供的alpha example，例如Learn里面的Documentation，有不少alpha example，并且会有指导如何提升该alpha表现的方法，这些example都是非常有经济学含义的，而且根据指导的方向去调整，难度不大。还有，从BRAIN的官方讲座﹑课程中学习alpha。这是我建议优先去学习的渠道，因为在能够在一定程度摸索出官方所偏好的alpha的样式，也是在一定程度可以防止overfitting，例如避免过多的op堆叠使用，又例如倾向使用single dataset等。

2.通过官方提供的论文及参考的datafield，结合论坛中各个帖子，去学习如何从0到1做出有经济学意义的alpha，并逐步尝试独立开发alpha。

二﹑关于质量问题，考虑OS表现。

从历年IQC的比赛评分标准来看，OS是越来越重要的，从以往更关注IS，都IS和OS各占50%，到了2024年是IS和OS分别占25%和75%。这使得我们不得不高度重视，因为有不少参赛的选手，也是靠OS追赶上排名的。

OS表现不佳，分为underfitting和overfitting两种情形。前者可能来源于追求“简洁”而对datafiled的处理不足。后者可能来源于datafield或op的堆叠﹑过度调参﹑混信号等。在实际中，我们可能需要更多地关注后者，因为在比赛时，新手通常会出现以下一些行为：例如聚焦在IS Preformance的加分，为了加分，可能会不断调整settings和表达式中的各个参数。又例如把不同的几个regular alpha，简单地进行线性运算，例如通过rank()，把不同的datafield相加起来等。再例如，在调整表达式使得分数不断增加的同时，alpha可能已经偏离了原来的经济学含义。

所以，可以构建一个 **Robustness Test** 的框架，例如包含：

1. **参数敏感性测试** ：对settings和alpha表达式的参数进行调整时，观察对alpha performance变化的影响。

2. **数据字段相似性替换测试** ：如果表达式中使用了多个datafield，对其中的单个datafield进行相似性变换，例如mdl175_beta120替换为mdl175_beta60，观察对alpha performance变化的影响，如果有，是否该表达式过度依赖于或仅取决于某个datafield。

3. **集中度测试** ：使用rank，sign，power(rank(),2)等，并设定相应的阈值，分别对拟提交alpha进行测试。

例如观察rank(alpha)的sharp是否仍然≥ alpha sharp的50%；

sign(alpha)的sharp是否仍然≥ alpha sharp的40%；

power(rank(alpha)，2)的sharp是否仍然≥ alpha sharp的80%等。

如果收益指标不足某个阈值，或者风险指标大约某个阈值（例如出现turnover大幅上升）则可能需要进一步考虑该alpha是否存在影响OS的一些因素，例如该alpha的表现可能对于某些标的的配置特别敏感，头寸过度集中在少数标的上。

4. **Universe扩展测试** ：观察拟提交alpha 在super universe和sub universe的表现是否仍有一定程度的信号。例如如果alpha的universe是TOP1000的，则可以把universe调整为TOP3000和TOP500，观察sharp是否仍然保持大于等于某个阈值。

5. **SEMI-OS分析** ：调整TEST PERIOD，观察Performance的各项指标在不同SEMI-OS下是否有较大差异。

6. **相关性分析** ：借助Self Correlation和“Alpha Distribution”去尽可能diverse所以提交的alpha。

如果alpha OS不错，那么在之后的National/Regional Round和Global Finals都会有比较大的优势。例如在National/Regional Round可能需要选取3个具有代表性的alpha进行展示。“代表性”不一定是IS Sharp最高的，但可能需要考虑idea具有一定的独特性，且OS很大可能能够保持稳健的，因为这两者结合能在很大程度上反映出自己在开发alpha的方法论和执行框架。

最后，在BRAIN体系下，每个人都有走上冠军之路的可能。加油！

*声明*

*本文所述内容仅为个人经验分享，所涉及的过往比赛信息仅供参考，具体以BRAIN官方公布为准。*

---

## 讨论与评论 (18)

### 评论 #1 (作者: SZ83096, 时间: 1年前)

写的真好，特别是对新手如何构建 **Robustness Test** 的框架非常实用，谢谢分享

---

### 评论 #2 (作者: MY56787, 时间: 1年前)

感谢楼主分享如此详尽的参赛经验和心得！Robustness Test框架给我很大启发，除了第一点是自己平时会做的，其他几点都没有考虑过，让我重新思考了如何平衡IS和OS的表现。

---

### 评论 #3 (作者: ZS59763, 时间: 1年前)

很详尽的参赛经验，可以让我推荐的几个用户好好学学了，点赞

---

### 评论 #4 (作者: BS20926, 时间: 1年前)

Thank you for sharing your experience and insights. Elaboration on the robustness Test framework helps alot.

---

### 评论 #5 (作者: RB98150, 时间: 1年前)

Your breakdown of the IQC experience is both insightful and thorough—like a well-optimized alpha with minimal overfitting! The emphasis on OS robustness is particularly crucial, given how easily one can fall into the trap of parameter tweaking and false signal confidence. The robustness tests you outlined are like a financial warrior’s training regimen—stress-testing every angle before battle. Also, the reminder that rank(alpha) sharpness should still hold up under transformations? Chef’s kiss. More traders should appreciate that a fragile alpha is like a bad haircut—it looks fine in one light but collapses under real scrutiny. Keep up the great work, and may your alphas stay resilient and uncorrelated!

---

### 评论 #6 (作者: YF61435, 时间: 1年前)

做alpha还没有稳健性测试的意识，对我有很大启发，打算也慢慢摸索自己的框架。

---

### 评论 #7 (作者: RZ54685, 时间: 1年前)

我已经交了不少alpha，但还是从数量上满足一万分，以后的方向应该是做质量高的alpha，这个给我启发很大，希望能有更多的交流！

---

### 评论 #8 (作者: XD81759, 时间: 1年前)

学到了，不愧是IQC 2024中国区第一

---

### 评论 #9 (作者: YL39207, 时间: 1年前)

很大启发，非常赞！我的理解是增加了稳健的可能性，但实际上OS的底层复杂性和市场动态性可能导致理论优势被稀释。例如，训练数据与真实场景的分布偏移、不可预见的协变量干扰，都可能成为稳健性提升的实际瓶颈。所以还是不能单纯地依赖训练集上的策略优化。

---

### 评论 #10 (作者: liangzhuoan(RL73053), 时间: 1年前)

感谢分享

---

### 评论 #11 (作者: CL50482, 时间: 11个月前)

感谢分享 **Robustness Test** 的框架！

---

### 评论 #12 (作者: WL83640, 时间: 10个月前)

现在刚从用户转为有条件顾问，在做alpha上有更高要求，感觉难度更大，这个框架启发很大！

---

### 评论 #13 (作者: MS79222, 时间: 10个月前)

谢谢大佬分享！这个Robustness Test框架很赞！错过了IQC，我现在正在等待成为顾问，这个框架还是要好好研究，对今后的研究有帮助！

---

### 评论 #14 (作者: YH75978, 时间: 10个月前)

感谢分享，很有启发！希望可以多发帖分享更多干货！

---

### 评论 #15 (作者: SK10818, 时间: 10个月前)

感谢大佬分享，一直困惑与如何判断alpha的质量，感谢大佬给了一个参考的标准

---

### 评论 #16 (作者: PX22637, 时间: 9个月前)

感谢大佬分享,  **Robustness Test** 框架是及时雨

---

### 评论 #17 (作者: HM24686, 时间: 9个月前)

感谢大佬的分享，每次看都有新的收获！

---

### 评论 #18 (作者: CC85858, 时间: 9个月前)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------感谢分享，原来还有这种检查方式：power(rank(alpha)，2)的sharp是否仍然≥ alpha sharp的80%

---

