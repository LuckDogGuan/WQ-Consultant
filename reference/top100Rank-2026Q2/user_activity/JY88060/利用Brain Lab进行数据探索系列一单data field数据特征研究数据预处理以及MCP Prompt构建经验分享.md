# 利用Brain Lab进行数据探索系列一：单data field数据特征研究、数据预处理，以及MCP Prompt构建经验分享

- **链接**: 利用Brain Lab进行数据探索系列一单data field数据特征研究数据预处理以及MCP Prompt构建经验分享.md
- **作者**: JY88060
- **发布时间/热度**: 10个月前, 得票: 33

## 帖子正文

概览：一、为什么要进行数据特征研究及数据预处理？二、结合Brain lab分析可能存在的数据问题，以及如何进行数据预处理三、需要关注的数据特征四、数据预处理整体流程梳理五、构建MCP prompt对数据进行预处理正文：一、为什么要进行数据特征研究及数据预处理？“因子”是基于Ross的APT理论，Fama和French通过三因子模型所开创的领域，是属于实证金融而非理论金融的范畴。实证金融的基础是统计学，具体到因子分析上，构成因子的每个金融工具特征在截面上的同质性和因子在时间序列上的平稳性是重要假设前提。具体到Brain平台上的Alpha generation，数据预处理的目的有二：1.通过数据预处理保证数据的同质及平稳，可以更大程度保障IS及OS的一致性，使我们对OS表现更有信心。2.对于涉及多个数据字段的alpha，我们需要保证多个字段的可比性。需要注意的问题是，原始数据的平稳性与因子平稳性是不一样的。我们更关注的是因子的平稳性。举个例子，news数据通常是脉冲式的，随机出现的，因此news数据段一般是不平稳的。但是，如果我们基于news数据构建一个事件驱动因子，我们对每一个新闻执行同样的交易策略，那我们的因子数据的事件空间就是所有的有新闻的时间，而非整个交易时间段，那么因子数据就很可能是平稳的。二、结合Brain lab分析可能存在的数据问题，以及如何进行数据预处理首先，要理解原始数据是一个面板，从数据每个截面上看是不同的金融工具在同一日期的不同特征表现；从每个时间序列上看是同一金融工具在不同日期的特征表现。 因此，在横截面上和时间序列上都需要对数据可能出现的问题进行研究和处理。进一步，考虑数据可能出现的、对同质性和平稳性有影响的问题。基于Brain lab给出的案例，数据可能出现的问题有如下几类：缺失数据(missing data)。在cross section和time series上都可能出现该问题，如果缺失数据比例较大，则因子的统计有效性是存疑的。另外，缺失数据可能被命名为-1或者99，如果不处理会扭曲真实数据情况。周期性数据(cyclical data)。如果数据在time series上出现周期性特征，则数据是不平稳的，可能存在自相关，那么得出的统计量是不可靠的。极值(outlier)。会扭曲数据的真实分布，使得统计量不可靠。非正态分布(non normal distribution)。非正态分布一般不会产生重大问题。平台关注的统计量基本都是参数估计，但如果数据本身是非正态分布的，那么很多经典的参数检验都是无效的，对判断统计量的有效性产生一定难度。还有一些虽然不影响因子有效性，但处理数据时应当小心的问题：向量数据(vector data)。应该了解vector data原始数据的状态，再进一步考虑如何使用具体vector operator进行处理。非可比数据(non-comparable data)。如果涉及两个或两个以上字段进行分析，那么这些字段只有在单位上可比才能联合分析。以下均使用USA, Delay1, TOP3000, dividend数据字段做示例。1.通过数据可视化初步判断数据可能出现的问题缺失数据：通过分布图和数据覆盖图判断是否有缺失值，缺失值是否应该处理，以及应该如何处理情况一：大量、无规律缺失。处理方式：首先判断数据是否可有用于构建事件驱动策略，如可能，则不处理；如果不能，则放弃该字段。情况二：大量、有规律缺失。处理方式：方法一：构建事件驱动策略因子；方法二：通过自回归、周期加总使数据平稳；方法三：简单缺失值回填。情况三少量缺失：处理方式：方法一：简单缺失值回填；方法二：不处理。示例：通过Visualize Field查看数据分布以及覆盖从覆盖图上可以看出，数据90%以上为0，没有nan数据。这时候我们需要注意，这个0数据到底是缺失值被回填为0了，还是它本来就是0？我们放大数据可以看出，覆盖数据在时间上具有一定周期性。再看turnover数据，周期性非常明显。再结合这个字段是股利数据，那么，我们可以大胆判断，这个数据的缺失属于情况二，大量、有规律缺失。（类似的字段还有财务报表的原始数据）我们可以再结合个股数据再次验证。再看频率分布图，大量的数据集中在0，对y轴采用log，可以看出数据有少量的非零数据，非零数据具有尖峰厚尾的统计特征。另外我们注意到，数据并没有把缺失值表示为-1, 999之类。极值通过统计量判断是否存在极值，极值应到如何处理情况一：与策略相关，如捕捉异常财务数据，因为亏损、会计调整等等出现财务指标出现异常数据，那么要么不处理，要么捕捉这些异常后再进行处理。情况二：去极值，使数据同质、平稳。示例：根据统计量分布图查看百分位数的分布从统计量分布图可以看出max值相对于75分位值有scale上的差异，因此这个数据集的极值是会扭曲数据分布的，因为dividend的数据本来就少，所以预计基于异常值很难组成有效因子，所以对于这个字段最好的处理方式就是去极值。非正态分布通过频率分布图查看数据是否属于正态分布。从之前的分布图可以看出数据明显左偏，也就是出现极值的概率大于正态分布。自变量不一定需要调整成正态分布，主要还是看使用数据的目的。比如担心极值会扭曲数据关系，或者希望数据预测更加稳健，可以将数据调整成正态分布。数据可比性通过频率分布图对相关数据进行单位及分布进行判断，调整数据使相关数据字段可比。2.可以采用的数据预处理方式以下是一些示例，采用mcp后会提供更多的数据预处理方式缺失数据：将数值转化为nan：pasteurize, purify, to_nan, nan_out回填nan数据：nan_mask, ts_backfill, kth_element极值：去极值：winsorize, truncate非正态分布：分布调整：log, sigmoid, tanh三、需要关注的数据特征连续还是离散缺失值类型及比例数据频率数据单位和分布四、数据预处理整体流程梳理第一步：点击Visualize Field初步查看数据特征，了解缺失值、异常值和分布数据覆盖图+turnover图+个股数据图判断数据频率、周期性及数据分布数据覆盖图+频率分布图查看缺失值统计特征图查看极值第二步：建立关键统计量定律描述数据概况（利用Brain lab进行分析）1.零值和nan值比例2.数据频率及周期。3.关键统计量分别计算原始非零数据的关键统计量和去极值后的数据的关键统计量。第三步：构建MCP数据分析的prompt，进行数据预处理。五、prompt模板Before we start the alpha generation, we need to preprocess the raw data to improve the quality of the alpha data.Each data field in the Brain Platform database is panel data, i.e., it contains aggregated time-series data of all the financial instruments in the universe in interest.The following is the statistical summary of the data field. After you digesting the data info, you will generate content I later ask you to provide.Data Summary:1. data field{“delay”: 1,“universe”: “USA”,“data set id”: “pv1”,“data field id”: “dividend”}2.measurement scaleThe value in the data field is continuous, not discrete.3. data coverageFrom the time series perspective, the proportion of zero values is{"mean": 0.9920,"min": 0.9455,"25%": 0.9906,"50%": 0.9943,"75%": 0.9968,"max": 1, }.The proportion of nan values in the time series is 0.4. data frequencyThe data has pulse-like periodicity for each instrument in the time series perspective.For each financial instrument, calculate the average days between adjacent non-zero values in its time series, and then conduct statistical analysis on all financial instruments, with the conclusions: {"mean": 87,"min": 1.5,"25%": 1.5,"50%": 91,"75%": 91,"max": 1650}5. data distributionStatistical analysis on all non-zero data shows:{"mean": 0.3541,"min": 0.000003,"25%": 0.12,"50%": 0.23,"75%": 0.4025,"max": 103.75,"skewness": 49.54,"kurtosis": 5101.7}After cross-sectional data winsorization applying the IQR rule, the statistical analysis results are: {"mean": 0.2993,"min": 0.000003,"25%": 0.12,"50%": 0.23,"75%": 0.40,"max": 6.5,"skewness": 1.89,"kurtosis": 10.16}.Now please provide multiple data preprocessing expressions based on your understanding of the operators in the Brain Platform:Step 1. Handling missing data.Step 2. Handling outliers.Optional step. Adjust data distribution for better statistical results.Additional requirement:1. Employ as many as possible operators in the platform以下是分析结果示例：这是单数据字段的分析示例，可以进一步改进prompt，了解数据单位和分布特征后，数据预处理可以实现多个数据字段的对齐，使之可比，是alpha质量更高。另：也在此提问，怎么去理解lab字段分析中的turnover？我理解是abs（单日数据-长期平均值之间差异）/长期平均值，不知道理解是否正确

---

## 讨论与评论 (9)

### 评论 #1 (作者: XW61573, 时间: 10个月前)

学习，还是看得一头雾水

---

### 评论 #2 (作者: FD69320, 时间: 10个月前)

手动点赞，谢谢大佬的分享。========================================================================================================================================================================

---

### 评论 #3 (作者: DX58146, 时间: 9个月前)

有深度，有帮助，期待更多优秀分享

---

### 评论 #4 (作者: ZH87224, 时间: 9个月前)

turnover 的计算：diff(1).abs().sum() / abs().sum()

---

### 评论 #5 (作者: JX28185, 时间: 9个月前)

MCP提示词的数据，用lab公式获取后，是手动输入的，还是有其他自动化方案，请大佬给指点一下。

---

### 评论 #6 (作者: MZ35432, 时间: 6个月前)

根据图形看不太懂当前字段属于哪种形式的数据 需要哪种方式处理呢

---

### 评论 #7 (作者: KH21822, 时间: 3个月前)

手动点赞，谢谢大佬的分享。========================================================================================================================================================================

---

### 评论 #8 (作者: KH21822, 时间: 3个月前)

====================================================================================点赞，谢谢大佬分享====================================================================================

---

### 评论 #9 (作者: RT69601, 时间: 3个月前)

同一个DataSet下，数据字段的分布和缺失不一定相同，分析单独某个字段可能无法构建出有效alpha，但如果在lab中把该DataSet下所有字段都查一遍效率又太低了，请问大佬有没有性价比高的办法分析这些字段呢？

---

