# 英才候选人计划实训考核（Case2）_总第三期

- **链接**: [Commented] 英才候选人计划实训考核Case2_总第三期.md
- **作者**: WL13229
- **发布时间/热度**: 2年前, 得票: 3

## 帖子正文

1. Performance面板截图，选择相关方向的文章

2.找到论文\研报，发布新的一篇《Alpha灵感》文章在 **中文论坛（注意不是顾问论坛）** ，附链接，且 **严禁抄袭，勿与已发布在 [《Alpha灵感》合集中的选题](/hc/en-us/community/posts/19348865150743--Alpha%E7%81%B5%E6%84%9F-%E8%AE%BA%E6%96%87-%E7%A0%94%E6%8A%A5%E5%90%88%E9%9B%86) 重复。**

《Alpha灵感》文章中必须包含的内容

- 核心交易idea是什么？
- 是否找到数据：
- 是否找到Universe: 例如TOP 200, （一般金融论文都会明确说出其适用的股票类型）
- 是否找到Neutralization: Sector (Smart Search)
- 使用什么operator
- 核心Alpha的Expression（可选）
- 绩效（需保证Sharpe至少大于1.3，Fitness至少大于0.6，Turnover低于45%，高于5%；通过PROD相关性测试）

3. Template分析，阐述其抽象后可以提取什么信息，不同条件下的搜索空间可能有多大，有什么独特的操作，适用什么universe,周期等。

4.  **本次作业硬性要求至少成功提交一个Alpha** ，请提供截图。

5. 总结反思（代码较上次有什么功能提升、debug经历、模板适合的数据类型、模板的改进方向等）

---

## 讨论与评论 (75)

### 评论 #1 (作者: WL13229, 时间: 2年前)

**示例：**

1.可以看出，期权数据和分析师数据都用得较少，我选择阅读 [Research paper 53: Textual Sentiment, Option Characteristics, and Stock Return Predictability](../CC40930/[Commented] Research Paper 53 Textual Sentiment Option Characteristics and Stock Return Predictability.md)  ![图片](images/img_aa574d50bd.png)

2.《Alpha灵感》文章（仅供示例）： [【Alpha灵感】A股换手率类因子 – WorldQuant BRAIN](../WX84677/[Commented] 【Alpha灵感】A股换手率类因子.md)

3. Template分析

```
residual_of_A = ts_regression(A,B,750);group_rank(-ts_regression(C,residual_of_A,750),densify(pv13_r2_liquid_min5_sector))
```

抽象来看，该模板用B对A进行提纯，将被提纯的部分拿来对C进一步提纯，并在分组排序。该模板认为，最后提纯出来的事情可以对股价有预测效应。该Alpha在长周期中尝试出现了效果，独特的分组可能会提升表现。

4.  ![图片](images/img_32bba36a3c.png)

5.总结反思

---

### 评论 #2 (作者: KJ42842, 时间: 2年前)

每周四晚8pm-9pm设有与课程相配套的Office Hour，欢迎对课上以及作业内容有疑问的同学参加，注册 [链接](https://worldquant.zoom.us/meeting/register/tJctcu-pqjwuGNcf2F-ukY3hUqWrliPiKhZc)

Note: Office Hour不要求全程参加，解答完问题的同学根据自己时间安排自行下线即可。

---

### 评论 #3 (作者: YW93864, 时间: 2年前)

大家好，这是我本周的交付内容，本周提交3个alpha，复现并优化得到两个，抽象化得到一个。

**1. Performance面板**  ![图片](images/img_bc2ed86460.png)

![图片](images/img_366e5ee6fb.png)

我的alpha在USA比较多，而CHN非常少。因此本周我还是以CHN为主。考虑到之前所有量化相关经历，都没有做过分析师相关的alpha，所以本周以分析师alpha为主。

**2. 【Alpha灵感】**

**链接为： [【Alpha灵感】分析师的“真知灼见” – WorldQuant BRAIN](/hc/en-us/community/posts/20089517507735--Alpha%E7%81%B5%E6%84%9F-%E5%88%86%E6%9E%90%E5%B8%88%E7%9A%84-%E7%9C%9F%E7%9F%A5%E7%81%BC%E8%A7%81-)**

**3. Template抽象化**

首先简述一下，具象复现出来的因子：大致逻辑是从分析师预期中，剥离动量因素的影响，这个因素是来自于内幕交易的，既有长期也有短期。主要是先选取一种分析师数据，再定义长期动量和短期动量因子，分别做截面回归进行剥离，从而发现那些预期变化大而涨跌幅小（没有被提前内幕交易）的股票。

一级抽象：将原有的一致预期净利润替换为相同数据集下的预期数据，此处是other41。Brain还有好多CHN分析师数据，还在尝试。在使用api不断simulate后，发现该数据集也只有净利润相关的三个字段比较好，说明模板具有一定特异性。这里我先后提交了两个，一个是PAFR，另一个是预期惯性因子，详情可移步前文链接，这一部分的绩效在该文章中有展示，两个因子虽然隶属同一数据源且构造算法90%相似，但最后相关性较低。

二级抽象：核心思路是假设分析师的一致预期准确，现在有一家A公司的预期层面有重大变化，但有可能被内幕交易消化掉，因此我们需要找到那些有预期层面有明显变化的，而内幕交易者关注不到的股票。 **防止微观变动影响到中观层面判断。** 微观层面可以进一步用技术指标刻画，除了截面上剥离它，还可以从时序上剥离。

1）那么我这里做的处理是找了另一个有分析师数据的数据集，求算过去一段时间内的均值，再对一些技术指标进行时序回归取残差，效果非常好。当然model216的分析师数据本身就有非常明显的信号，只是容易出现robust universe检测不达标的情况，不过大部分只差一点，在不断simulation后，有两个可以直接提交的，有几个在微调参数后，也能提交，但参数比较极端。总之，整体上还是有稳健的。

![图片](images/img_91b25e9ea4.png)

![图片](images/img_0aa08d2a2f.png)

prod corr高可能是技术指标用的比较多导致的，但处于0.6-0.7之间，最后也通过了测试。

**4. 提交截图**

![图片](images/img_56de8bcefc.png)

**5. 反思**

工程上：本周找了先前提交的simulation丢失现象，发现是因为同一个表达式重复回测的问题。然后平台似乎会先查找有没有测过这个alpha，如果测过完全一样的，则返回之前的alpha_id，如果没有，再开始回测。另外。本周把requests的status_code了解了一下，优化了提交错误表达式无法向我报错的问题。

研究上：本周主要挖掘了分析师alpha，但分析师alpha其实在样本外2021年后至今，有因为市场风格切换的失效问题。我觉得后续优化思路是，1）再尝试分析师数据和不同的数据的组合，依靠其他数据的稳健性叠加分析师数据的强信号；2）寻找不同的分组，剥离市场风格的影响，我这次提交的一个因子还是会受到2015年的影响，暂时没有找到处理这个问题地良好方法，但也不想过拟合2015年，所以提交了，但后续还需要进一步思考如何避免风格切换的风险

问题：1）我在本次测试中获得了很多有潜力的因子，部分只是相差及格标准0.01-0.05不等因而不能提交，部分是因为提交了一个，导致其余相关性变高无法提交。请问老师或者同学对于这些剩余的因子有没有好的处理方法，如何进一步利用它们？

---

### 评论 #4 (作者: YH69102, 时间: 2年前)

1.可以看出，Price volume data和 analysis data都用的较少。选择阅读：东方证券-因子选股系列之九十四：UMR2.0，风险溢价视角下的动量反转统一框架再升级。

![图片](images/img_6079ceb110.png)

2.《Alpha灵感》文章： [https://support.worldquantbrain.com/hc/en-us/community/posts/20088908680087--Alpha%E7%81%B5%E6%84%9F-UMR2-0-%E9%A3%8E%E9%99%A9%E6%BA%A2%E4%BB%B7%E8%A7%86%E8%A7%92%E4%B8%8B%E7%9A%84%E5%8A%A8%E9%87%8F%E5%8F%8D%E8%BD%AC%E7%BB%9F%E4%B8%80%E6%A1%86%E6%9E%B6?page=1#community_comment_20089744914199](https://support.worldquantbrain.com/hc/en-us/community/posts/20088908680087--Alpha%E7%81%B5%E6%84%9F-UMR2-0-%E9%A3%8E%E9%99%A9%E6%BA%A2%E4%BB%B7%E8%A7%86%E8%A7%92%E4%B8%8B%E7%9A%84%E5%8A%A8%E9%87%8F%E5%8F%8D%E8%BD%AC%E7%BB%9F%E4%B8%80%E6%A1%86%E6%9E%B6?page=1#community_comment_20089744914199)

3.3. Template分析：

```
risk = ts_mean(R,20) - R;f = ts_sum(risk * A,20);
```

抽象来看本文旨在通过寻求一种风险的度量手段R,来描述当日的风险水平。进而通过一个统一的公式自动选择动量还是反转。R 的可选范围有turnover,volatility of volume or price.

A则是对股票收益的估计(原文中使用 returns - index_returns),可以替换为其他内容。

用rank(f) 或者 -ts_regression(returns,f,d)作为最终的alpha.

4.

在不同的市场下测试，发现在CHN和GLB都能找到alpha ![图片](images/img_94833c289c.png)

5. 总结反思（代码较上次有什么功能提升、debug经历、模板适合的数据类型、模板的改进方向等）

代码：

把原来需要一次做完所有simulation后再返回结果的，改为了每隔一定次数将所用datafields、alpha_id保存至excel文件，方便于之后的筛选。

模版适合的数据集:

主要考虑固定A后，筛选R。在GLB下将search设置为volatility、coverage>80%。发现有近3000个数据集且分散在很多种dataset中. 然后发现直接搜risk可以缩小很多范围。

模版改进方向：

可以将ts_sum改为ts_decay_exp_window 或者 在计算Risk时 考虑引入论文中提到的特殊日子（在CHN上没提升，说不定其他市场适用）。

---

### 评论 #5 (作者: YL93001, 时间: 2年前)

1、我的面板中各类数据的alpha都比较少，我选择了东吴金工的《 **信息分布均匀度，基于高频波动率的选股因子** 》

![图片](images/img_8e760425bc.png)

2、文章链接： [【Alpha灵感】信息分布均匀度，基于高频波动率的选股因子 – WorldQuant BRAIN](/hc/en-us/community/posts/20073476508055--Alpha%E7%81%B5%E6%84%9F-%E4%BF%A1%E6%81%AF%E5%88%86%E5%B8%83%E5%9D%87%E5%8C%80%E5%BA%A6-%E5%9F%BA%E4%BA%8E%E9%AB%98%E9%A2%91%E6%B3%A2%E5%8A%A8%E7%8E%87%E7%9A%84%E9%80%89%E8%82%A1%E5%9B%A0%E5%AD%90?page=1#community_comment_20100077495191)

3、模板本质上提取了一个数据的标准差除以一个数据的均值，我们可以称之为某个数据的均匀度，对于波动率的信息，经过试验在短周期的效果比较好，我试验了波动率的大约5000个数据，可以提交的alpha数量在20-30个左右；对于其他类型的数据，可以根据数据的特性选择相应的周期，对数据作上述的均匀化处理，可能也会有比较好的效果。

4、alpha提交截图

![图片](images/img_5d75afce1c.png)

5、总结反思：本次我对ace的代码进行了重构与重写，简化了许多步骤，也使自己的代码结构更清晰。在代码效率方面来讲，相比于一次跑5000个simulate，个人认为像在需要短时间内产出结果的project中，1000个左右跑一次可能效率更高一些，一方面simulate时间变短，得到1000个结果后就可以对其中的结果进行分析，同时电脑再跑下1000个alpha。关于本次的均匀度模板，我认为对量价类数据都可以进行尝试，可能会得到一些不错的结果。

---

### 评论 #6 (作者: JL23162, 时间: 2年前)

1.我的面板情况如下

![图片](images/img_1363c01d40.png)

![图片](images/img_0afd1eaf6b.png)

因此选择GLB方面的MODEL data算是涉及一个全新的领域

2.文章链接 [https://support.worldquantbrain.com/hc/en-us/community/posts/20101484394903--Alpha%E7%81%B5%E6%84%9F-%E5%9F%BA%E4%BA%8E%E8%8D%89%E6%9C%A8%E7%9A%86%E5%85%B5%E9%80%BB%E8%BE%91%E6%9E%84%E5%BB%BAalpha](https://support.worldquantbrain.com/hc/en-us/community/posts/20101484394903--Alpha%E7%81%B5%E6%84%9F-%E5%9F%BA%E4%BA%8E%E8%8D%89%E6%9C%A8%E7%9A%86%E5%85%B5%E9%80%BB%E8%BE%91%E6%9E%84%E5%BB%BAalpha)

3.使用的模板在alpha灵感中 继续修改了均值与异常值的定义标准 使用了新的operator

随后在仅57个（精心挑选）的数据中挖出了5个alpha

4.alpha提交截图

![图片](images/img_544831b734.png)

5.总结反思

总的来讲 一个优秀的模板 远比大批量的回测方便，如果有优秀的先验知识，那么产出的alpha也会比较容易，上面这里的57个数据 实际上是归属于同一个数据集Growth Valuation Model 在代码方面现在比较依赖先验知识的输入 现在做的确实是human+machine 但是不能纯挂机，我个人是比较偏向于做GA那种可以挂在服务器上每天挖4个因子的，总的来说，课程帮助很大，不仅是对于worldquant这个平台的因子挖掘，实际上在实盘操作中，这些知识也是可以迁移使用的，不过对于alpha的报酬我仍有疑问，我这里一天提交了4个alpha并且是GLB的乘五倍积分，实际上，只收获了4.11u，感觉收益较低

---

### 评论 #7 (作者: WL13229, 时间: 2年前)

[JL23162](/hc/en-us/profiles/18456131969431-JL23162)

这位同学的作业做得很漂亮。有几点感受可以跟您分享。

1. 纯挂机的，我们未来会有课程继续分享，欢迎您持续参与本计划。

2. 您提到知识的迁移使用，这个确实是非常重要的，这个也会是同学们参与此计划的主要收获之一。

3. 关于收入，我看到您的Alpha总数并不多。收入会在您有一个季度的持续表现（即20个不同自然日都有Alpha提交）之后有明显改变。届时，如果您可以获得比0.5更高的value factor score，相信您的收入会比目前明显增加。总而言之，BRAIN系统需要您有一定活跃的历史，才能给您合理地计算并赋值。另外，可以参考这篇文章👉 **[如何提高研究顾问收入](/hc/en-us/community/posts/19382864029079-%E5%A6%82%E4%BD%95%E6%8F%90%E9%AB%98%E7%A0%94%E7%A9%B6%E9%A1%BE%E9%97%AE%E6%94%B6%E5%85%A5)**

---

### 评论 #8 (作者: BX78946, 时间: 2年前)

1. Performance面板截图 ![Pasted Graphic.png](images/img_36853c7e96.png)

红色部分是USA的news data和fundamental data，这次我选择了CHN市场的price volume data。

2. alpha灵感帖子链接 [https://support.worldquantbrain.com/hc/en-us/community/posts/20090584979479--Alpha灵感-上下影线-蜡烛好还是威廉好-](https://support.worldquantbrain.com/hc/en-us/community/posts/20090584979479--Alpha%E7%81%B5%E6%84%9F-%E4%B8%8A%E4%B8%8B%E5%BD%B1%E7%BA%BF-%E8%9C%A1%E7%83%9B%E5%A5%BD%E8%BF%98%E6%98%AF%E5%A8%81%E5%BB%89%E5%A5%BD-)

3. 这个template原本的含义是通过分析市场参与者的心理状态来找到投资策略，例如如果股票在某段上涨行情中出现了较长的上影线，则我们往往认为该股当前的卖压较大，空头势力占优，上涨行情即将结束。而所提到的蜡烛和威廉的区别只在于衡量的标准是开盘价和收盘价的极值还是只看收盘价。这个策略也算是一个典型的reversion的策略。最后ubl用的zscore我感觉是为了标准化蜡烛上影线和威廉下影线，使得他们是同一个量纲，可以直接进行加法的操作，用其他的cross sectional operator应该也是可以的。原本我以为这个用了很经典的量价的datafield是通不过prod_corr测试的，没想到只是复现了原本研报的idea的alpha就可以直接提交。

![Pasted Graphic 2.png](images/img_835f21caac.png)

这是提交后的corr的测试，提交之前忘了截图了

![Pasted Graphic 3.png](images/img_bb29bb195c.png)

这里原本的蜡烛上影线和威廉下影线的定义是：

```
candle_up = high - max(open, close); William_down = close - low;
```

抽象来看的话，主要是先得到一个变化度，再对这个变化度进行reversion操作。这里的变量很多，我的选择是舍弃掉了open 和 close，把这两个影线都规定成 (high - low)/2，然后分别对high，low进行搜索，要是遇到了vector的话，high就用vec_max，low就用vec_min。但是这样的话其实和原本的影线的定义不是特别相符。当然也可以固定住high，low，然后搜索open，close。这里我纠结的一点就是，原本的这四个data filed都是针对与股票的，相互加减都有意义。要是我固定某两个值，去搜索其他的，很大可能他们之间互相的加减没有经济学的含义。不知道有没有什么方法可以解决这个问题。

4. 后来根据上面的抽象后的模版用api进行模拟，这次还是只得到了很多过不了correlation的alpha。感觉可能是因为，尽管这个idea的表达式看起来很多，但是核心思想还只是得到高位和低位之间的变化度，这个idea的泛化性太强了，导致类似的idea很多。还有可能就是我这种搜索并没有用到很好的先验知识，感觉盲目的直接搜索还是不太好。

![Pasted Graphic 4.png](images/img_78b9d964ba.png)

5. 本来这次我是想选择一篇论文从头开始自己找alpha，但是尝试了一段时间以后没找到表现特别好的就放弃了，还是找了一篇研报进行复现。还是希望自己以后能够多尝试从论文找alpha，这样的话idea的创新性可能会好很多，能过correlation测试的alpha也会多一些。在跑代码的过程中，获取prod_corr的时候有时候会出现“Error while decoding prod_corr JSON for alpha XXXXXXX: Invalid or empty JSON”，还没有解决这个问题。还有一次性太多次请求prod_corr的时候，会出现“Error while fetching prod_corr for alpha XXXXXX: 429 Client Error: Too Many Requests for url:”，不知道有没有好的解决方法。

---

### 评论 #9 (作者: WL13229, 时间: 2年前)

[BX78946](/hc/en-us/profiles/16297370627607-BX78946)

您好，请不要对每个Alpha都请求corr.每小时的请求总数在千次级别。

对于第三个问题，我建议您可以把high open close low全部换掉，放到option data数据集去搜。因为option data也是一种价量数据。然后随机抽取四个不同的东西。或者你先根据option的各类数据先分四个组。

---

### 评论 #10 (作者: ZC80223, 时间: 2年前)

1.我的面板情况如下

![图片](images/img_e4ecb5de0d.png)

2、alpha灵感帖子链接： [https://support.worldquantbrain.com/hc/en-us/community/posts/20051302553879--Alpha%E7%81%B5%E6%84%9F-%E5%9F%BA%E4%BA%8E%E5%8F%8D%E4%BA%8B%E5%AE%9E%E6%A8%A1%E6%8B%9F%E7%9A%84%E4%B8%AD%E5%9B%BD%E8%82%A1%E5%B8%82%E6%B6%A8%E8%B7%8C%E5%81%9C%E6%9D%BF%E7%A3%81%E5%90%B8%E6%95%88%E5%BA%94%E7%A0%94%E7%A9%B6](/hc/en-us/community/posts/20051302553879--Alpha%E7%81%B5%E6%84%9F-%E5%9F%BA%E4%BA%8E%E5%8F%8D%E4%BA%8B%E5%AE%9E%E6%A8%A1%E6%8B%9F%E7%9A%84%E4%B8%AD%E5%9B%BD%E8%82%A1%E5%B8%82%E6%B6%A8%E8%B7%8C%E5%81%9C%E6%9D%BF%E7%A3%81%E5%90%B8%E6%95%88%E5%BA%94%E7%A0%94%E7%A9%B6)

3、

av = vec_avg{x};#vector数据降维
        bv = vec_avg{y};#vector数据降维

signal = (shrt5_limit_down_price - vec_min(pv27_s_dq_low)) < (shrt5_limit_up_price - vec_max(pv27_s_dq_high)) ? -1 : 1;   #构造磁吸方向信号

Prob_trade = 1 / (1 + exp(-(-0.13 + 1.6 * 0.697 + 0.1 * bv + -0.15 * signal)));#构造基于交易活跃度信号的磁吸概率
        Prob_estimate = 1 / (1 + exp(-(-0.08 + 1.6 * 0.697 + 0.013 * av + -0.15 * signal)));#构造基于估值难度信号的磁吸概率
        trade_when(or((shrt5_limit_down_price - vec_min(pv27_s_dq_low)) <0.1,(shrt5_limit_up_price - vec_max(pv27_s_dq_high))<0.1),-rank(Prob_estimate + Prob_trade),-1) #根据文中对于研究对象的定义是股票涨跌停价9%左右样本，个人认为磁吸是反转策略，标志着非理性行为。对于高概率的上涨股票应该做空，下跌股票应该做多。

4、alpha结果，目前还在跑，首次遇到了生成expression高达58w的窘境，采用评论区留言的pv27作为重点生成对象，目前表达式降至19740个。有没有进一步减少范围的小tips？挖出了1个可用的但没过prod corr

![图片](images/img_52ea23ba2d.jpeg)

![图片](images/img_8eb9effd28.jpeg)

补充下，虽然这个idea没找到prod corr过的alpha，但其他idea有通过的。

![图片](images/img_2dc88a0eb2.png)

5、感想

如果有2个以上的datafield，组合的可能性实在太多了，目前仍在摸索技巧中。关于template的有效性有了比较真实的感悟，如果一个template对该数据集无效，那么会出现大量的alpha结果是负值，1000个结果也找不到任何一个形态看上去合理的alpha。这时候需要思考策略是否是理解错了，需要进一步理解。

---

### 评论 #11 (作者: OA92025, 时间: 2年前)

老师，您好~我还是没有解决上周的问题。我的alpha在API提交了simulation之后，查询到‘Location’，打开后status是“complete”，而且也能查询并返回alpha的pnl表现等详情。但是在alpha列表仍然不会显示。排除了您说的1. alpha表达式错误（否则status会是 Error， 而我的是complete）2. sign in不成功（我的是201，是成功了的）这是为什么啊。。。

---

### 评论 #12 (作者: WL13229, 时间: 2年前)

[OA92025](/hc/en-us/profiles/18197007430167-OA92025)

1. 请使用print打印一下你每次simulate的Alpha表达式。

2.如果这个Alpha在之前simulate过，是不会更新数字的。

---

### 评论 #13 (作者: WL13229, 时间: 2年前)

[ZC80223](/hc/en-us/profiles/16412175793303-ZC80223)

请在Alpha灵感帖子或者您的回帖评论中增加Alpha绩效的截图

关于搜索空间过大的问题，这个是一个量化研究中面临的非常真实的问题。我觉得您对自己模板抽象后的理解还不够深入，请继续从数学角度，思考您的模板可以提取什么信息。欢迎跟帖讨论

---

### 评论 #14 (作者: YJ78324, 时间: 2年前)

**【Performance面板】**

![图片](images/img_dd78823dee.png)

本次选取的研报是：东方证券因子选股系列之九十四：UMR2.0—风险溢价视角下的动量反转统一框架再升级

今天才发现，这篇研报选取的跟  YH69102 同学是一样，不过我也在其基础上提交了Alpha，也是CHN上的第一个Alpha。

**【Alpha灵感】**

分享链接： [【Alpha灵感】UMR2.0——风险溢价视角下的动量反转统一框架 – WorldQuant BRAIN](/hc/en-us/community/posts/20101783750167--Alpha%E7%81%B5%E6%84%9F-UMR2-0-%E9%A3%8E%E9%99%A9%E6%BA%A2%E4%BB%B7%E8%A7%86%E8%A7%92%E4%B8%8B%E7%9A%84%E5%8A%A8%E9%87%8F%E5%8F%8D%E8%BD%AC%E7%BB%9F%E4%B8%80%E6%A1%86%E6%9E%B6)

**【Template构建与优化】**

本篇文章的核心在于以时序均值调整后的风险指标来加权个股每日的溢价，并以此构建统一的动量反转因子。

由此可以构建模板，其中天数60由研报中推荐给出，mkt的计算可以参考 [BRAIN小贴士(这里有你想要的硬核内容！持续周更中） – WorldQuant BRAIN](/hc/en-us/community/posts/15152019662487-BRAIN%E5%B0%8F%E8%B4%B4%E5%A3%AB-%E8%BF%99%E9%87%8C%E6%9C%89%E4%BD%A0%E6%83%B3%E8%A6%81%E7%9A%84%E7%A1%AC%E6%A0%B8%E5%86%85%E5%AE%B9-%E6%8C%81%E7%BB%AD%E5%91%A8%E6%9B%B4%E4%B8%AD-)  中沪深300指标的计算：

```
R = {risk} / close;Risk = ts_mean(R, 60) - R;f = ts_decay_linear(Risk * (returns - mkt), 60);rank(f)
```

之后我对比了一下上式中f的计算，发现不计算超额收益时的效果会更好，所以修改模板为：

```
 f = ts_decay_linear(Risk * returns, 60);
```

在这里，我们搜索以volatility作为关键词进行搜索，以其作为每日风险指标，可以得到最佳结果如下：

![图片](images/img_8adea41468.png)

![图片](images/img_e6e4d3537d.png)

可以看到因子的表现不错，可惜并不能通过prod相关性测试。

这里我考虑对因子进行融合，考虑到这个是利用量价数据的因子，所以考虑添加基本面因子进行融合。

这里的基本面因子我采用第一周的模板进行搜索：

```
rank(group_neutralize({field} - last_diff_value({field}, 5), bucket(rank(cap), range="0.1, 1, 0.1")));
```

参考上周结果，最佳的因子在回测最近的两年表现稍差没能通过测试，而此次的量价因子在这个周期表现较好，考虑将两个因子融合：

```
power(alpha_1, 2) + power(alpha_2, 2)
```

最终我们拿到了一个可以提交的Alpha

![图片](images/img_183858bb31.png)

![图片](images/img_1120290dfb.png)

![图片](images/img_df2cee5836.png)

【总结】

通过本周的任务，一方面进一步优化了代码的易用性，可以通过配置文件完成自动化搜索。

![图片](images/img_d4293f5e90.png) 另一方面我也在思考，对于单一一个因子没法满足要求时，可以考虑与其他大类的因子进行融合。进一步，可以将有潜力的因子PNL拿到，之后对自相关性不高的因子进行组合，尝试出可以通过的融合因子。

---

### 评论 #15 (作者: YW54232, 时间: 2年前)

【Performance面板】
 ![图片](images/img_8aafbf2cc2.png) 【Alpha灵感】

[https://support.worldquantbrain.com/hc/en-us/community/posts/20108973243671--Alpha%E7%81%B5%E6%84%9F-%E9%AB%98-%E4%BD%8E%E4%BD%8D%E6%94%BE%E9%87%8F%E5%9B%A0%E5%AD%90](https://support.worldquantbrain.com/hc/en-us/community/posts/20108973243671--Alpha%E7%81%B5%E6%84%9F-%E9%AB%98-%E4%BD%8E%E4%BD%8D%E6%94%BE%E9%87%8F%E5%9B%A0%E5%AD%90)

【Template分析】

alpha = low_event * vol_event == 1 ? -expression : 0;

因子背后的逻辑是在low和volatility事件都触发时进行交易和调仓，那么调仓的权重就是可以搜索的点。我思考的是在低位放量时，什么权重对这个事件而言是一个利好，因此可以在公司基本面数据中进行搜索。搜索中发现net profit能很好的契合我们的需求，所以作为expression信号的核心。

但是因为这个因子和volatility有着强相关性，所以不可避免在2015年A股股灾时有着很差的表现。我花费了两天事件去思考如何“规避”股灾，用了tips15进行尝试，但是发现结果是不robust的，也通不过universe robust测试。

我在此之间其实花费的大量时间去寻找一些能规避2015股灾的因子，但其实效果都不显著。所以要从底层逻辑进行思考，是不是我们这个因子本身并不robust。volatility本质也是和动量相关的，如果混合一些动量相关的判别会不会有好的改善。

于是我对alpha里加入一小部分close price相关的动量因子

ts_rank( (vec_avg(mdl14_2_d1_close_price) - close ),60)

的权重，顺利通过了测试！连2015的回撤也小了很多。结果也是非常的robust。

![图片](images/img_7b0be90bf6.png)

![图片](images/img_23991ecc17.png)

![图片](images/img_90f2c2bde7.png)

【总结反思】

这个alpha的创建过程让我想到一句话：不识庐山真面目，只缘身在此山中。我们不能为了改善因子的test而去改变，这样往往是很低效的，我也为此付出了大量的时间，结果找到方法后很快就改进成功了。关注因子本身和市场的逻辑，往往比只去关注PNL图那一点回撤和缺陷更有用。但是Tips 15对股灾的规避依然是很不错的方法，虽然这次没有完全使用上，但我也尝试了比如股灾中使用更强化的表达式等方法，确实对回撤有所改善。

---

### 评论 #16 (作者: WL13229, 时间: 2年前)

[YW54232](/hc/en-us/profiles/13837011976855-YW54232)

您的思考是非常深入的。很高兴看到您有所收获。确实如此，在股灾中直接平仓，这种方法是饮鸩止渴的。如果把策略换成在股灾中切换成其他的Alpha。可能会有不错的收获

---

### 评论 #17 (作者: FP65798, 时间: 2年前)

1.Performance面板截图
 ![图片](images/img_55df7825bb.png)

Option因子还比较少，故我选择option相关的研报进行研究。

2.新发布【Alpha灵感】
 [【Alpha灵感】关于未来的股票回报，个股期权波动率Smirk告诉了我们什么？](/hc/en-us/community/posts/20163362610711--Alpha%E7%81%B5%E6%84%9F-%E5%85%B3%E4%BA%8E%E6%9C%AA%E6%9D%A5%E7%9A%84%E8%82%A1%E7%A5%A8%E5%9B%9E%E6%8A%A5-%E4%B8%AA%E8%82%A1%E6%9C%9F%E6%9D%83%E6%B3%A2%E5%8A%A8%E7%8E%87Smirk%E5%91%8A%E8%AF%89%E4%BA%86%E6%88%91%E4%BB%AC%E4%BB%80%E4%B9%88-) 
参考文献： [Research Paper 20](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1107464)  : What Does Individual Option Volatility Smirk Tell Us About Future Equity Returns?

3.Template分析

```
diff = {x1} - {x2}
```

![图片](images/img_dc5d0bab23.png) Template是很简单的两数据做差，原因子是call和put期权隐含波动率做差，可以推广为两种波动率数据做差，甚至是两种同一单位的数据做差，都有可能蕴含有价值的信息。

如果限制在期权空间，前项固定，后项变化，则数据量为1509。进一步限制，后项我们只用opt4_put_vola_{x1}d， opt4_{x2}_put_vola_delta{x3}这样名称的数据，数据量缩减为1040。
 ![图片](images/img_34a85a40c0.png)

4.成功提交Alpha截图 ![图片](images/img_7c26d554e1.png)  ![图片](images/img_0ab0f16f82.png) 最终使用Machine挖掘成功提交一个alpha，在做【Alpha灵感】过程中利用纯Human方式成功提交一个alpha。

5.总结反思
代码新增data id字段筛选模块，已初步掌握Human+Machine发掘因子流程，期待进一步的学习。

---

### 评论 #18 (作者: JT89676, 时间: 2年前)

**1. Performance**  **面板** 
 **![图片](images/img_e038852a23.png)**

之前的alpha主要集中在USA地区，本次选择CHN利用基本面数据实现一个可以提交的alpha，并根据抽象的模版用machine搜索其它有提交潜力的alpha。

**2.【**  **Alpha**  **灵感】**

**链接为：**  **[https://support.worldquantbrain.com/hc/en-us/community/posts/20235808598423--Alpha%E7%81%B5%E6%84%9F-%E4%BB%8E%E5%B8%83%E6%9E%97%E5%B8%A6%E5%88%B0%E4%BC%B0%E5%80%BC%E5%BC%82%E5%B8%B8%E5%9B%A0%E5%AD%90](/hc/en-us/community/posts/20235808598423--Alpha%E7%81%B5%E6%84%9F-%E4%BB%8E%E5%B8%83%E6%9E%97%E5%B8%A6%E5%88%B0%E4%BC%B0%E5%80%BC%E5%BC%82%E5%B8%B8%E5%9B%A0%E5%AD%90)**

**3. Template**  **分析**

```
a = ts_zscore(D, 252);a1 = group_neutralize(a, bucket(rank(cap), range="0.1,1,0.1"));a2 = group_neutralize(a1, subindustry);b = ts_zscore(cap, 252);b1 = group_neutralize(b, subindustry);regression_neut(a2, b1)
```

文章的原始alpha选择的D为PE（BRAIN平台对应选取的数据字段为fnd72_s_pit_or_is_q_spe_si），主要逻辑是股票的估值PE具有均值回复特性，可以仿照经典均值回复布林带的构造方法，构造估值布林带模型，如果某股票的估值处于异常区间且其基本面不发生大的变化，未来的EP有很大概率回归正常区间。此外，为了剔除行业层面估值逻辑改变的影响，用到了行业市值中性化处理，并在横截面上作regression，复现的alpha可以提交。Machine搜索阶段使用Earnings Quality数据集和Comprehensive Fundamental Data数据集中的字段对D进行填充并测试，找到一些可以通过IS测试的字段，但是Self Correlation和Prod Correlation都比较高，如下图所示，这样的alpha有32个（其中有些字段本来就是一个系列的，如mdl25_is_41v和mdl25_is_9v），使用的字段为 mdl25_is_41v、mdl25_rd_9v、mdl25_73v、fnd72_s_pit_or_is_q_net_income_bef_mi等。

![图片](images/img_5143905182.png)

![图片](images/img_2a69331458.png)

**4. 提交截图**

**![图片](images/img_f916534037.png)**

**5. 反思**

本次使用的模版还是比较简单，Machine搜索时产生的alpha的Self Correlation和Prod Correlation都比较高。本次还优化了自动化提交脚本，统一了模版字段替换函数的调用过程。

---

### 评论 #19 (作者: WL13229, 时间: 2年前)

[JT89676](/hc/en-us/profiles/18490343365399-JT89676)

有点好奇，corr高的情况如何克服的。最后是通过什么改进进行了提交。另外就是，可以考虑分析师的数据

---

### 评论 #20 (作者: TG50517, 时间: 2年前)

1. 本人的Performance面板截图，选择Fundamental data的文章“New Evidence on the Relation Between the Enterprise Multiple and Average Stock Returns”。

![图片](images/img_391d581848.png)

2. 新的《Alpha灵感》文章链接：

[https://support.worldquantbrain.com/hc/en-us/community/posts/20240820051607](/hc/en-us/community/posts/20240820051607)

3. 核心思路很简单，构造“Enterprise Multiple”，然后数值低的做多，数值高的做空。而

```
Enterprise Multiple = Enterprise Value / EBITDA
```

所以只需要搜索“Enterprise Value”的Datafields {A}，以及“EBITDA”的Datafields {B}，从而

```
Signal = group_rank(ts_rank(-rank(A)/rank(B),5),industry)
```

然而，搜索到的{A}含有242个Datafield，{B}含有680个Datafield，二者有超过16万种组合，空间太大，不值得全部回测。

![图片](images/img_1a71ab09ed.png)

![图片](images/img_6b2c08c8ab.png)

这时发现，有些数据同时包含“ev”和“ebitda”，也就是把“Enterprise Multiple”算好了，这样就可以直接拿来用。不过使用的时候需要注意，有的数据计算的是“ev/ebitda”，有的是“ebitda/ev”，在表达式中加上适当的处理就可以套用同一个模板。
适用的Universe和Neutralization在《Alpha灵感》文章中已有讨论，不再赘述。

4. 成功提交的Alpha截图如下。

![图片](images/img_53a4037f83.png)

![图片](images/img_fc093902d5.png)

![图片](images/img_f8753d9934.png)

![图片](images/img_0b1944abbe.png)

5. 总结反思。

首先，本人的量化研究理念是从一个比较简单，蕴含明确经济学逻辑的Idea出发，然后再一步步优化，在优化的过程中也要保证逻辑的清晰可靠，这样可有效避免Overfitting，所以选择的论文Idea往往比较简单。今后也要尝试更加复杂的论文。

然后，在代码方面，本人在上次作业的基础上，把相关代码写进了一个Python Library中，这样用到哪个函数就可以直接调用，更加方便。

---

### 评论 #21 (作者: OA92025, 时间: 2年前)

paper：华泰单因子测试之换手率类因子（林晓明）

idea：计算每日换手率，以其过去一个月（22个交易日）的移动平均作为因子，再做“市值cap”分组的中性化处理（利用bucket）

1.python暴力循环：

利用循环设置decay、universe和neutral的方式，寻找最大的fitness。如果当前的fitness更大，就把setting记录下来。（很缓慢，而且有的提交不上去，需要用异常捕获，防止中断）

![图片](images/img_b341a4b513.png)

![图片](images/img_901ac01806.png)

2.最终的最优结果：（相关性也可提交）

![图片](images/img_4174931bb8.png)

![图片](images/img_9c310b5c56.png) 3.反思：

太慢了太慢了！！！（4个半小时，提交了约500次）

![图片](images/img_ebb094062f.png)

其实后来想到：

a. 可以先再brain上面模拟一下，得出大致的区间范围，可以减少循环。

b. 也不用每次记录fitness，不用每次查询结果（每次查询都要耗时很多），只需要又submission的记录，然后最后在alpha list里面，按照fitness和sharpe来排序，选最高的提交就行了。

![图片](images/img_a2bc3ff7ab.png)

---

### 评论 #22 (作者: ZL89083, 时间: 2年前)

1,这是我的performance面板

![图片](images/img_9dc01e65b5.png)

我选择用fundamental方面的文章

2，论文链接：  [**https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3292675**](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3292675)

3，寻找template

论文的大概意思就是由于商誉容易被投资者忽视，且不可评估，商誉/销售额这个指标虽然包含了公司价值的信息，但是股市对这些信息反应不足，这个指标其实是一个reversal的指标。但是由于并购行为周期比较长，因此论文里提出了结合量价信息与商誉销售比结合的方式构造因子。所以这个template其实是一种将基本面与量价信息结合的方法。其好处有二：1，提高因子的turnover 2,用量价信息加强并验证基本面的信息。我继续寻找有关setting的信息。并在论文里找到了industry分组的信息，推断股票池为Top500，这让我确定了setting。另外，文章提及了使用排序的方法构建组合，所以operater是以rank为基础。我依照文章构建了一个alpha,表现如下： ![图片](images/img_a2b8ebf0db.png)  ![图片](images/img_ba7dbae99f.png)

sharpe大于1.3，fitness高于0.6，turnover也低于45%，但是correlation为0.8，所以我改变了一下分组方式，改成了pv13_com_page_rank，这降低了相关性，而且适当提高了fitness。

4，template分析。

这个template基本上确定是用两个基本面的数据作为自由度，固定量价的指标，否则搜素强度太大，我就用search法搜索了fundamental的数据，然后用随机抽样的方式抽取了两次，每次50个，一共搜索2500次。在machine的过程中，我发现提交的alpha基本是正的收益，说明这个template是比较不错的，最后搜集的alpha表现如下。

![图片](images/img_071e6b4b83.png)

差不多fitness在0.95以上的我都human式的跑了一下，基本都可以提交，最终改进了相关性和fitness后提交了三个，后续还可以继续搜索

![图片](images/img_596a8198e7.png)

![图片](images/img_333968ff87.png)

![图片](images/img_911dd5682d.png)

说明还是比较成功的，虽然fitness都不算高

---

### 评论 #23 (作者: ZZ51944, 时间: 2年前)

## Performance面板截图

![图片](images/img_a7f6952d2c.png)

对于USA和CHN市场探索较多，多为量价和基本面数据。

选择的文章：做学术研究时总结的常用技术指标

## 《Alpha灵感》链接

[【Alpha灵感】常见技术指标在A股测试 – WorldQuant BRAIN](/hc/en-us/community/posts/20247158390295--Alpha%E7%81%B5%E6%84%9F-%E5%B8%B8%E8%A7%81%E6%8A%80%E6%9C%AF%E6%8C%87%E6%A0%87%E5%9C%A8A%E8%82%A1%E6%B5%8B%E8%AF%95)

## Template分析

生成了 [国家，股票池，中性化] 的三元组，其他使用默认参数，对于已经计算好的10个技术指标（实际上有13个值），以及其不同的数学计算直接进行暴力搜索。

全部的搜索空间 8*5*8*13*6=4000，但是因为股票池并不那么重要，所以先舍去了这个条件，对于表现较好的组合再进行股票池以及其他参数的调优。

## 提交Alpha截图

## ![图片](images/img_4de5638562.png) 
 总结反思

这次主要是学习了如何提高代码的鲁棒性，自动解决一些跳过的问题。

模板改进方向：

横向的改进：加入更多技术指标和技术指标信息提取的数学表达式；

纵向：尝试技术指标调优；

---

### 评论 #24 (作者: WX16829, 时间: 2年前)

作业提交

1.Performance面板：可以看出在USA delay 1中基本面数据和其他类数据相对用得较少，我选择阅读Research paper 18 : Earnings Volatility, Ambiguity, and Crisis-Period Stock Returns

![图片](images/img_cb305d7f37.png)

2.《Alpha灵感》文章：市场危机下盈利波动、不确定性与股价回报

[https://support.worldquantbrain.com/hc/en-us/community/posts/20103734605591--Alpha%E7%81%B5%E6%84%9F-%E5%B8%82%E5%9C%BA%E5%8D%B1%E6%9C%BA%E4%B8%8B%E7%9B%88%E5%88%A9%E6%B3%A2%E5%8A%A8-%E4%B8%8D%E7%A1%AE%E5%AE%9A%E6%80%A7%E4%B8%8E%E8%82%A1%E4%BB%B7%E5%9B%9E%E6%8A%A5?page=1#community_comment_20230670783767](https://support.worldquantbrain.com/hc/en-us/community/posts/20103734605591--Alpha%E7%81%B5%E6%84%9F-%E5%B8%82%E5%9C%BA%E5%8D%B1%E6%9C%BA%E4%B8%8B%E7%9B%88%E5%88%A9%E6%B3%A2%E5%8A%A8-%E4%B8%8D%E7%A1%AE%E5%AE%9A%E6%80%A7%E4%B8%8E%E8%82%A1%E4%BB%B7%E5%9B%9E%E6%8A%A5?page=1#community_comment_20230670783767)

3.Template分析：从文章中所提示的数据特征已可直接构造出一个可提交的alpha，并比较容易地抽象得到以下模板：

crisis_ind==FALSE ? normal_factor : ts_delay(crisis_factor,days)

该模板的含义是：当股价处在正常水平时，使用一般的基本面因子进行预测和交易；当股价进入危机时刻后，使用危机前能够预测危机中股价变动的因子进行交易。

从以上模板中可以看出，因子的泛化可以从三个维度考虑：

- normal_factor：这类因子的选择比较多，感觉上一般表现不错的基本面因子均可以考虑，最简单的方法就是将论文提供的Fundamental28中的特征（一共有超过2000个）进行尝试，其他fundamental dataset或analyst dataset中的特征因子也可考虑。
- crisis_factor：文章中给出oth401_game_eps_vol这个特征构造crisis factor,其核心是认为公司危机前经营上面的波动与危机中的股价变化存在较强的关联性，在other401这个数据集中除了盈利波动外，其他与经营相关的波动特征（例如gross margin vol,Cash Flow Variability,SG&A Volatility等）均可考虑放入模板中测试。
- crisis_ind:这部分目前还没有想到相对固定的模板进行泛化，但除了股价波动这个方法外，违约距离（default distance）、CDS违约特征等均对于危机的判断有比较密切的关联，在平台上也可以找到相关的数据特征进行尝试。

总体上，该模板的泛化能力还是比较强的，可以进行尝试的方向和数据集比较多。该模板的使用的数据以基本面特征数据为主，因子换手率一般相对比较低，同时基本面的特征对同一行业内的公司具有较高的可比性，因此做neutralization或分组时多倾向考虑选择INDUSTRY或SUBINDUSTRY等行业相关的分组类型。

4.提交截图：提交了两个因子，一个是通过人工得到的，另一个是通过模板泛化后找到的。

![图片](images/img_3d8f38f8e5.png)

5.总结反思

在研究方面，主要是花时间研究了通过论文的核心思想如何构造合适的模板，一开始的时候研究方面有偏差，花了不少时间在如何提前判断危机的来临，这个难度确实比较大。后面改为判断是否已出现危机为条件，难度大幅下降了，模板很快地确定下来，第一个因子也较为顺利的提交。因此，判断和选择合适的方向对于因子的研究是十分重要的。

在代码方面，基本沿用了上次的模板，使用Fundamental28的特征逐个放入模板尝试不同的normal_factor，从结果上看不少也可达到可提交的标准，且有一些因子的绩效较第一个因子有明显的提升。对于crisis_factor和crisis_ind初步人工尝试了一下，也能找到一些可提交的因子。如果同时变动三个维度，搜索空间会很大（Fundamental28里面已经有2000多特征），所以后续考虑的方向是如何降低搜索范围，可考虑的方向是先找到绩效较好的normal_factor,过滤后再尝试与不同的crisis_factor和crisis_ind进行组合（这两个维度相对的搜索空间会小一些），看一下最后能否得到其他的有效因子。

另外，在灵感文章后所提的意见中关于不同类型alpha直接连接的问题，这个确实在设计时没有意识到，但目前所使用的normal_factor和crisis_factor外层都是使用了rank这个operator,算是有点歪打正着吧，后续在泛化的过程中这个问题确实需要注意。

对于robust的问题，这个也是一个很好的需改进方向，目前在设计因子中对这方面考虑的并不多，后续这个方向还需要在进一步改进。

---

### 评论 #25 (作者: WD77850, 时间: 2年前)

- 1.Performance 截图
  - 这是我的performance截图，因为量价因子提交较少，故选择量价因子进行研究。 ![图片](images/img_e820473654.png)
- 2. alpha 灵感 湘财证券-多因子量化选股系列之四：新技术因子的研究与测试
  - [Alpha 灵感 湘财证券-多因子量化选股系列之四：新技术因子的研究与测试 – WorldQuant BRAIN](/hc/en-us/community/posts/20251795571351-Alpha-%E7%81%B5%E6%84%9F-%E6%B9%98%E8%B4%A2%E8%AF%81%E5%88%B8-%E5%A4%9A%E5%9B%A0%E5%AD%90%E9%87%8F%E5%8C%96%E9%80%89%E8%82%A1%E7%B3%BB%E5%88%97%E4%B9%8B%E5%9B%9B-%E6%96%B0%E6%8A%80%E6%9C%AF%E5%9B%A0%E5%AD%90%E7%9A%84%E7%A0%94%E7%A9%B6%E4%B8%8E%E6%B5%8B%E8%AF%95)
- 3. Template 分析
  - 抽象得到以下模板（由于因子衡量非流动性，故选择非流动性池，并选择行业中性化。基于检测中出现的集中性问题，加入winsorize控制集中性）
  - group_backfill(winsorize(-ts_mean(A,30)/ts_mean(B,30),std = 4.0), industry, 20, std = 4.0)
  - 原模板已经可以得到一个可提交的因子。抽象的模板表示了B因子在一段时期内的信息对A因子在一段时间内的影响变化，刻画了非流动性指标。很容易得到B一般是与股票日交易额相关的数据，A则一般是与收益率相关的数据。选择多个相关data set进行遍历，替换为oth143_sell_tier1_volume获得了更好的因子表现。经改进后因子通过了测试可以提交 ![图片](images/img_d95476c5c1.png)  ![图片](images/img_0ed5c4665b.png)
- 总结反思：本次作业出现了一些设备问题导致平台操作出现了一些问题，幸好后续找到了替代办法。本次作业试了4篇研报才终于得到一个可以提交的因子。我认为有以下两点教训：1.尽量不要试图在平台上构建以分钟为维度或使用较多日详细交易订单数据的高频因子，特别是出现多个数据段的时候迁移到低频的方法效果也不佳。2.原本template效果较差的时候替换相似数据大概率效果也不佳，反而会浪费大量时间模拟。代码效率：API使用过程中发现在get dataset结果中找到需要的data set 的id比较困难，于是添加了根据名字找id的方法简化了流程。 ![图片](images/img_de3aef9c63.png)
- 后续可能改进方向：研报提到了可以通过市值对数中性化和五组分层进行多空组合。本人不太了解如何使用operator进行这些操作，尝试过使用对logcap 进行bucket分组再group中性化，但是效果不佳。欢迎大家指导。

---

### 评论 #26 (作者: HW97336, 时间: 2年前)

1、performance面板

这是在美国市场上的Alpha，在中国市场上只提交过一个Alpha，所以这次尝试在构建中国市场上的量价Alpha

![图片](images/img_2ec0bba975.png)

2、新的《Alpha灵感》文章链接：

[【Alpha灵感】隔夜“拉锯战”和渔利因子](http://support.worldquantbrain.com/hc/en-us/community/posts/20251308691735--Alpha%E7%81%B5%E6%84%9F-%E9%9A%94%E5%A4%9C-%E6%8B%89%E9%94%AF%E6%88%98-%E5%92%8C%E6%B8%94%E5%88%A9%E5%9B%A0%E5%AD%90)

3、寻找template

首先对于这种量价Alpha提取模板有些困难，一方面是这个Alpha的思路是隔夜和盘中的价格矫正过程，因此似乎不能放弃“隔夜”和“盘中”这两个概念，而隔夜涨跌和盘中涨跌只对于可交易金融资产有效，另一方面是数据集可替换性不大，基本上是开盘和收盘的某个指标，我归纳的template如下：

```
ret_oc = C/O-1;ret_co = O/ts_delay(C)-1;NR = ts_sum(ret_co>0&&ret_oc<0?1:0,22)/22;PR = ts_sum(ret_co<0&&ret_oc>0?1:0,22)/22;group = bucket(rank(cap),range='0,1,0.1');group_neutralize(rank(NR)+rank(-PR),group)
```

其中C表示收盘指标，O表示开盘指标，原文主要思想是隔夜投资者和盘中投资者的对抗，盘中投资者倾向于过度矫正“错误定价”，之后会出现回归现象，NR衡量了盘中投资者过度压低价格的比例，回归意味着涨，因此是正向因子，PR衡量了盘中投资者过度抬高价格的比例，回归意味着跌，因此是负向因子

我先在A股市场复现了研报，成功提交，之后通过搜索“open”和“close”，发现了一些适用于美国的option和news方面的数据，但并不多（中国几乎没有），而且不能两两随意组合，否则没有意义，所以手动配对了数据，最终试了10组，都无法提交，有两组有明显信号，都是价格数据，但是需要手动优化，这个模板不好扩展，也许像开盘收盘的期权隐含波动率或者期货的价格可以一试，但是并没有找到数据。

4、这是中国市场上成功提交的Alpha

![图片](images/img_33ff9ad4b5.png)  ![图片](images/img_930deba765.jpeg)

![图片](images/img_96383df645.jpeg)  ![图片](images/img_70024ee944.jpeg)

5、总结

本周规范了自己的代码库，单独写了一个模板生成的函数，添加了检测是否能提交的函数，以及把提取alpha的信息和模拟alpha分离开

对于模板前面也已经提到了一些想法，我想知道这种模板能不能突破隔夜和盘中的概念，改成其他可扩展的形式呢？以及这次的模板不能直接机械地排列组合，效率太低，一些无意义的组合（比如期权价格收盘价和开盘新闻情绪值的组合）大概率不会有好的表现，因此还是需要人为地组合同一类的open和close，显得有点笨拙，不知道有没有什么好的建议

---

### 评论 #27 (作者: XC63878, 时间: 2年前)

**1.Performance**  **面板截图**

**![图片](images/img_f13b749e64.png)**

**2.Alpha**  **灵感**

链接： [【Alpha灵感】将隔夜涨跌变为有效的选股因子](/hc/en-us/community/posts/20252684454295--Alpha%E7%81%B5%E6%84%9F-%E5%B0%86%E9%9A%94%E5%A4%9C%E6%B6%A8%E8%B7%8C%E5%8F%98%E4%B8%BA%E6%9C%89%E6%95%88%E7%9A%84%E9%80%89%E8%82%A1%E5%9B%A0%E5%AD%90)

idea：在隔夜涨跌幅的基础上，利用成交量的信息，计算隔夜涨跌幅与昨日换手率的相关系数。通过两者的相关性来衡量知情交易者和市场有效性的强弱。

数据：open、close、pv27_turnover_d

Universe: CHN TOP3000

Neutralization：subindustry

**3.Template**  **分析**

corr = ts_corr(A,B,20);

group_neutralize(corr, bucket(rank(cap), range="0, 1, 0.1"));

该模版考虑两个变量之间的相关性，通过这种相关性来反应市场的某种性质或者某一类股票的性质。

**4.**  **成功提交的Alpha**

**![图片](images/img_7076cf5e44.png)**

**5.**  **总结**

本次作业尝试了好几篇论文/研报，存在以下问题

（1）论文/研报本身的灵感很好，但难以在BRAIN平台上找到所需要的数据集，导致无法复现；

（2）论文/研报本身的灵感很好，也能较好地复现，但很难通过prod_corr检测；

（3）论文/研报本身的灵感很好，但复现的效果并不理想。

大多数是第（2）种情况，对于这种情况，如果只是利用machine替换相关变量，仍然还是无法通过prod_corr检测，可能对运算符进行替换的效果更好一点。对于第（1）种情况，可以通过替代变量去构造所需要的数据，但能满足的还是少数。而且自己对Fields确实不太熟悉，有些Fields的Description很笼统。对于第（3）种情况，可能是论文/研报中的某些细节没有写出来，导致无法精确的复现，但论文/研报所表达的经济学原理和逻辑也是很有价值的。

---

### 评论 #28 (作者: SL57524, 时间: 2年前)

1. Performance面板截图，选择相关方向的文章

![图片](images/img_8365e8bcca.png)

2.《Alpha灵感》文章

[【Alpha灵感】Research Paper 22 Overnight returns, daytime rev...](/hc/en-us/community/posts/20239918193303--Alpha%E7%81%B5%E6%84%9F-Research-Paper-22-Overnight-returns-daytime-reversals-and-future-stock-returns)

[【Alpha灵感】 计数启发法](/hc/en-us/community/posts/20237862981399--Alpha%E7%81%B5%E6%84%9F-%E8%AE%A1%E6%95%B0%E5%90%AF%E5%8F%91%E6%B3%95)

[【Alpha灵感】东吴证券的几种换手率因子](/hc/en-us/community/posts/20255074372375--Alpha%E7%81%B5%E6%84%9F-%E4%B8%9C%E5%90%B4%E8%AF%81%E5%88%B8%E7%9A%84%E5%87%A0%E7%A7%8D%E6%8D%A2%E6%89%8B%E7%8E%87%E5%9B%A0%E5%AD%90)

3. Template分析，阐述其抽象后可以提取什么信息，不同条件下的搜索空间可能有多大，有什么独特的操作，适用什么universe,周期等。

我尝试的这3篇文章可以提取到2个Template：

第一个来源于 [【Alpha灵感】Research Paper 22 Overnight returns, daytime rev...](/hc/en-us/community/posts/20239918193303--Alpha%E7%81%B5%E6%84%9F-Research-Paper-22-Overnight-returns-daytime-reversals-and-future-stock-returns) ：

找到某种可以代表“异常”的指标，异常是由于两种状态的连续所体现，对于这种异常分别在月的层次进行计数，用年的层面作为基准值进行比较。

第二个来源于 [【Alpha灵感】 计数启发法](/hc/en-us/community/posts/20237862981399--Alpha%E7%81%B5%E6%84%9F-%E8%AE%A1%E6%95%B0%E5%90%AF%E5%8F%91%E6%B3%95) ，就是针对投资者可能会关注的某个指标，当这个指标相比整体表现超过一定阈值的时候加入计数，在过往的时间段里总和这些技术，加权时注重权重的衰减。这个template可以提取一些股民/机构可以直观/比较经常关注的信息。除了原文的量价指标，目前认为在“新闻”方面这个template可以发挥用处，目前正在用machine对新闻进行搜索，其他量价数据没有搜到可以通过检验的。

关于计数启发法，帖子底下有一些老师同学的留言，我会重新向这些方面尝试优化。

这两个Alpha灵感有相似之处，但是我觉得我所提取的东西并不够抽象化，我感觉找到一个能用的（高成功率）的抽象化模版并不容易，比如老师课上所言的“2次提纯”，这个东西看起来既一定实际意义，又感觉很玄学。

现在我能做的用Machine辅助自己 只能是有明确数据方向的尝试，更像是一种调参，而不是一种Template。

4. Alpha截图

![图片](images/img_ac0d17a6a3.png)

这个alpha来自 [【Alpha灵感】Research Paper 22 Overnight returns, daytime rev...](/hc/en-us/community/posts/20239918193303--Alpha%E7%81%B5%E6%84%9F-Research-Paper-22-Overnight-returns-daytime-reversals-and-future-stock-returns) ，但无论如何改进都无法通过correlation，不知道能不能算勉强完成本次作业。

5. 总结反思

最大的反思在于为什么无法找到可以提交的Alpha

（1）

我发现在USA市场，从论坛的research paper中找到论文，有一些被大家做过的比较多，有一些比如和ESG相关的 ，只在最近几年效果比较好。如果在SSRN上找JFE和J F的这种论文，不知道到底该如何搜索，很多搜出来的论文并不是论坛那种数据鲜明的实证资产定价文章，又有很多论文用的数据都是创新性难以复现的。

在CHN市场，研报方面，Wind等找到的研报很多都是高频的，这些“分钟”数据我尝试迁移到低频但是基本做不出来（希望未来老师可以提供一些迁移的策略、例子），剩下的研报除了那种“N个相似类的因子效果检测”，大多数做出来都是correlation很高的。当然我也看到评论区很多同学都能做出来很好的结果，我认为还有以下几条的原因。

（2）对Fast Expression 和 dataset 不够熟悉。除了阅读论文，我尝试过程中大多数时间花在了如何写fast expression 上，而且常常写出来的表达式无法准确表达文章观点。也因为这个原因，我对Alpha的改进不能得心应手，无法完整的根据一种猜想——验证的逻辑 去细节上、符号上挖掘alpha的本质表现，比如像在 [【Alpha灵感】A股换手率类因子](../WX84677/[Commented] 【Alpha灵感】A股换手率类因子.md) 中老师所示范的那样。我近期会对所有Fast Expression操作符系统学习一下，借Office Hour的机会攻克这一部分问题。

（3）

近期通过《因子投资 方法与实践》这本书对整个因子投资有一定全貌的认知，包括这些天找论文、研报，对常见的分组排序，Fama Macbeth 回归检验， 提纯之后纯净因子表现，正交化等有一定的认知，知道这类论文、研报的论证思路和方式。

希望老师课上可以讲述一些 关于我们的Alpha提交之后，在Protfolio Manager那边如何组合的一些介绍，以及这种组合和SuperAlpha的相似点，从而完善对于因子投资的全貌了解。

---

### 评论 #29 (作者: FL11741, 时间: 2年前)

1.如图，这次在option，analyst和sentiment方向都有尝试 ![图片](images/img_c1ebf6e2e9.png)

2. [【Alpha灵感】 Implied Volatility Skew – WorldQuant BRAIN](/hc/en-us/community/posts/20255825146647--Alpha%E7%81%B5%E6%84%9F-Implied-Volatility-Skew)

Template分析：

仅就这篇post的template而言，还是比较浅显死板的：

(put_vola-call_vola)/(put_vola+call_vola) 将其中put_vola和call_vola换成不同的时间段和strike level，没有抽象化的提升。我只想到根据相关研报尝试不同表达式，例如Put Call Ratio等。

另外根据另一篇研报，得到了一个抽象的不错的模版：

λ = ESG ratings， sentiment ∈ [ -1 , 1 ]

（1 + λ * sentiment）*（1 + λ * negative sentiment）

做了一些尝试，结果发现我跑的ESG ratings数据字段有信号的都在疫情期间栽倒了LoL，所以没有采用那一篇，其他ESG相关的不是打分类型的数据的暂时没有进一步尝试。

4. Post的correlation过高了，暂时没有进一步降低的计划，不过我另起炉灶交了几个 ![图片](images/img_149788ae81.png)

5. 总结与反思：

在case2中遇到的主要问题：

1. 时效性：研报策略在疫情期间失效，甚至有巨大回撤。
2. 数据集与策略复杂性：一些研报的策略公式非常复杂，相应对数据集要求也非常苛刻。例如在实现分析师预测分歧中蕴含的alpha时，按照研报策略需要对同一分析师的基本面数据预测做追踪得到时序数据，再在分析师之间做随机森林回归，但这些可能在平台上较难实现。我选用了分析师预期标准差作为简单替代，有一定信号，但不足达到以提交标准。
3. 对自己不常用的数据方向的不熟悉：缺少对其他方向的基本逻辑和知识的整体认知给我在读研报以及尝试实现带来了很大阻力，希望在期末过后能够投入更多时间精力去学习了解。

关于程序实现上的进展：

上次pre中提到的simulation单独做成程序已经实现，核心思路是将simulation和get result放在两组子进程中，主进程用于用户交互。交互方面可以实现读取新数据进行插队或者正常排队，simulation和get result的开始、暂停、停止功能，以及实时进度的手动刷新。能够满足包括断网，自动登出，计算机睡眠等断点续接情况，意外关闭会丢失前50个待测simulation data和alpha id（可以规避但考虑到潜在的运行效率问题就不做实现了），并将目前我还未知的异常情况写入错误报告中并将simulation data分类为错误表达式或未知错误并返还。总之，现在已经能满足simulation高效率连续运行超过一天。已知问题：get result除了correlation一小时上限150次以外，在加了进程锁和sleep延时后依然偶尔会得到status code 429，在跑universe较小的simulation时，可能导致get result速率追不上simulation。

---

### 评论 #30 (作者: WL13229, 时间: 2年前)

[FL11741](/hc/en-us/profiles/18515544005527-FL11741)

同学您好，看到您写道“由于数据集缺失不同strike level下的成交量及open interest数据，并不能够还原”。

建议您多多尝试，在BRAIN平台有着非常多的option数据，尤其美国区域中option4和option6这一数据集是非常全面的。您说的数据，我本人都有做过，建议多多探索。

---

### 评论 #31 (作者: AZ81686, 时间: 2年前)

1. Performance面板: 可以看出，期权数据，我选择阅读期权方面的论文 ![图片](images/img_185eef8376.png) 2.《Alpha灵感》文章: 【Alpha灵感】Volatility Spreads and Expected Stock Returns

3. 核心template

```
spread = x_of_A - x_of_B
```

抽象来看，A和B可以是两种方向相反的东西，在论文中是call和put；或者也可以是有lead-lag关系的东西，如realized volatility和implied volatility; 这里面x需要相同是保证比较的是同一个东西，如波动率，才有“经济学含义”

4.成功提交 ![图片](images/img_a8bbb4329c.png)

5. 反思疑惑：在尝试过程中发现market / sector中性化的结果比industry/subindustry的表现要好；在可视化分析中可以看到一些行业的pnl表现突出，一些行业的avg size稍大；意味着因子对行业存在暴露；这种暴露是应该坚决消除的？还是可以作为一种smart择"行业"的方案？ ![图片](images/img_bea57d47ef.png)  ![图片](images/img_cb4f160957.png)

---

### 评论 #32 (作者: WL13229, 时间: 2年前)

[AZ81686](/hc/en-us/profiles/14380385958679-AZ81686)

这样的思考非常深入，是我们乐于见到的。我们不妨从另外一个角度来看看这个问题。

1. 在尝试过程中发现market / sector中性化的结果比industry/subindustry的表现要好。

这个观察，我认为和图片相印证后，应该可以得出一个推论：在neutralization之后，你的Alpha目前可能将仓位更多地集中到了某些行业。你可以使用一个group_rank，会得到类似的验证。

2.进一步的思考。

```
spread = x_of_A - x_of_B
```

如果你不加任何平滑的话，这个值可能在某些行业就是会很高的。例如如果我们在全市场的角度讨论资产负债率，那么银行业的整体资产负债率就是很高的。可能全市场资产负债率最高的100家里，有70家都是银行业的公司。那么当你在使用Market Neu的时候，实际上你只是选择了做多某些行业，然后做空某些行业指数。当然，需要点赞的是，这个Alpha也对其精选出来的行业做了合理的资本权重分配，否则不会有很好的IS表现。

这当然也是一种投资的方式，这种方式也是无可厚非的。但是，你需要考虑的是，这是不是你想通过本Alpha实现的目的？如果您只想拥有一个获得好的IS回报的Alpha，那么恭喜你，你已经实现了这个目标。如果你是想通过spread，在每个行业中都识别出“好股票”和“坏股票”，那么这个任务是还没有完成的，还有工作要做。

总结来说，并没有说“这种暴露是应该坚决消除的”。而应该是，我们去了解了这个Alpha在做什么，怎么赚钱，它的特性是什么。这样我们才可以在后续做SuperAlpha的时候，取得预期的效果。

毕竟，我们所作的所有工作，都是为了获得一个“近似于或者好于IS表现的OS”

---

### 评论 #33 (作者: ML15895, 时间: 2年前)

1.  **Performance面板截图** ：比较空白，所以没有限制什么方向。

![图片](images/img_4467d77e0d.png)

2.  **[[Alpha灵感]凸显理论](../MQ62208/[L2] 【Alpha灵感】凸显理论Salience Theory.md)** ，浏览了Brain平台上的alpha灵感合集，再结合网上随机搜索，随机找到了这几篇研报，平台上类似思想的Alpha灵感是 [这篇](/hc/en-us/community/posts/19298826598423--Alpha%E7%81%B5%E6%84%9F-%E6%A0%B9%E6%8D%AE-%E8%8D%89%E6%9C%A8%E7%9A%86%E5%85%B5-%E5%9B%A0%E5%AD%90%E7%9A%84%E6%96%87%E5%AD%97%E6%8F%8F%E8%BF%B0%E8%BF%9B%E8%A1%8C%E9%87%8F%E5%8C%96%E5%AE%9E%E7%8E%B0)  （估计也是prod corr高的来源）

3. T **emplate**  **分析及探索：**

- 从Alpha灵感中的初步实现的结果分析，可以看到STT2效果最好，于是选取这一模式，我理解的是凸显理论可以抽象理解成寻找因子偏离均值的异常值，再根据这些异常值权重和因子的协方差进行多头和空头的选取 template的表达式为：
  ```
  delta=0.7;theta=0.1;factor={datafield}; market_factor = group_mean(factor, 1, market);sigma = abs(factor - market_factor) / (abs(factor) + abs(market_factor) + theta);days = 22;k = ts_rank(-sigma, days)*days;k_1 = if_else(k==0, 1, k);weight = power(delta, ts_rank(k_1, days)) / ts_mean(power(delta, ts_rank(k_1, days)), days);ST = ts_covariance(weight, factor, days);signal = group_neutralize(zscore(-ST), bucket(rank(cap), range="0, 1, 0.1"));signal
  ```
  其中{datafield}为datafield，主要用到category==pv的价量数据，也尝试使用了analyst数据，如果是vector，先使用vec_sum进行降维。
- Template更新历史：
  1) 初步的Template通过IS的测试的不多，只有一个，是价量数据，所以简化模版再尝试，首先想到简化凸显性排序的计算，不改为整数，直接取[0,1]+1，这样的结果是测试速度加快，通过IS测试的个数增加。暂时放弃分析analyst数据，主要针对价量数据。
  2) 顺着这个方向将weight计算和最后的标准化排序调换顺序，进一步简化操作，同时发现vec_vag会更有效一点，所以改用这个操作符进行降维。
  3) 由于初始模版是月频调仓，不知道怎么在Brain平台上实现，所以在计算因子凸显性的时候直接选取截面rank，得到这个模版之后，可以通过IS测试的数量增加到十个左右，但是由于这个alpha主要用到价量数据，可提交的数据字段主要和成交量和换手率有关，prod corr均超过0.75。
  这个版本下的模版是
  ```
  delta=0.7;factor = {datafield}; weight = power(delta, rank(factor)) / ts_mean(power(delta, rank(factor)), 22);ST = ts_covariance(weight, sigma, 22);signal = group_neutralize(zscore(-ST), bucket(rank(cap), range="0, 1, 0.1"));signal
  ```
  可以得到如下结果，可惜还差一点就可以提交，而且corr>0.7， alpha表达式和结果如下
  ![图片](images/img_53da7c46b9.png)  ![图片](images/img_f2dc5afad3.png) 4) 根据sharpe排序找了上面这个结果之后，感觉这个信号真的还不错，感觉放弃有点可惜。所以这两周没有放弃一直在尝试，之前主要是在TOP3000选股，然后试了一下2000也有差不多的信号，突然想到如果是小市值的股票，凸显性有没有可能会更明显。于是使用trade_when 通过rank(cap)选取小市值股票，然后修改group_neutralize的group最终获取一个可以提交的alpha，表现截图如下:
  ![图片](images/img_4110b9a177.png)  ![图片](images/img_6627b209bc.png)

4.  **提交截图** ： ![图片](images/img_ca59a4fbc7.png)

5.  **总结反思** ：

- 功能提升：增加批量获取alpha中通过IS以及corr测试的expression
- 模版适合的数据类型以及改进方向：目前看来是用于价量数据，同时看到评论区有同学是用ts_corr(A,B,d)的模版更抽象，考虑直接抽象成ts_covariance(A,B,d)，不过目前还没有尝试，同时考虑替换group_neutralize的group字段
- 反思总结：
  1）对于template的抽象还需要努力，经验不足导致不知道该怎么抽象，所以template比较复杂。
  2）没有实现两个或者多个datafields组合，搜索空间有限。思考：如何进行group字段的提取。
  3）看到有信号但是prod corr高，甚至产生>0.9的prod corr，我想这说明这是一个实现简单，并且比较有效的因子，作为初学者可以积累一些这方面的素材，所以还是决定死磕这篇研报，最终也找到可以提交的因子还是比较高兴的。缺点就是时间花费太多，可能会错过一些机会。Brain平台上也有提到reduce prod corr的 [帖子](../PN39025/[L2] [BRAIN TIPS] How do you reduce correlation of a good alpha.md) 。希望自己能够继续努力，与君共勉。

---

### 评论 #34 (作者: WL13229, 时间: 2年前)

@ [OA92025](/hc/en-us/profiles/18197007430167-OA92025)

同学您好，本次课程的要求是。发一篇新的idea post。您没有在本次作业的时候发新的post,请关注此问题。

---

### 评论 #35 (作者: AZ81686, 时间: 2年前)

[WL13229](/hc/en-us/profiles/12285040305687-WL13229)

关于“

```
spread = x_of_A - x_of_B
```

如果你不加任何平滑的话，这个值可能在某些行业就是会很高的。”

进一步发展，可以想象，如果我们是想用spread = call的隐含波动率 - put的隐含波动率来作为“情绪方向”的话，会有有个问题就是波动率均值大的股票/行业，计算得到的spread也是相对较大；那么从收益来源的角度，其实这个spread不仅赚的是情绪方向判定的钱，还take了大波动率本身的risk (进而risk premium)

---

### 评论 #36 (作者: WL13229, 时间: 2年前)

[AZ81686](/hc/en-us/profiles/14380385958679-AZ81686)

确实如此，所以在visualization的界面就看到了对某些行业的结果。看看有没有提供capital by sector的图像。或许会有更多启发

---

### 评论 #37 (作者: KZ79256, 时间: 2年前)

1. Performance面板截图，目前我的因子在CHN里面很少

![图片](images/img_6604d7372d.png)

2.找到论文\研报，发布新的一篇《Alpha灵感》文章在 **中文论坛（注意不是顾问论坛）** ， [【Alpha灵感】球队硬币因子构建.md](【Alpha灵感】球队硬币因子构建.md)

（si，写完才发现和alpha灵感里的重了=.=!!!）

3. Template分析

我用了两个template

第一个是在原始的球队硬币因子的基础上更改输入字段，和mean的时间

第二个是将收益率替换为任意信号（如101因子等），通过波动率和换手率反转部分信号

```
day_yield = {signal}day_yield_mean = ts_mean(day_yield, time); # 日间收益率day_yield_std = ts_std_dev(day_yield, time); # 日间波动率factor1 = if_else(normalize(day_yield_std, useStd = false)>0, -day_yield_mean, day_yield_mean);# “日间反转-换手翻转”因子factor2 = if_else(normalize(turnover_rate_delta, useStd = false)>0, -day_yield_mean, day_yield_mean);factor1+factor2
```

4.  **本次作业硬性要求至少成功提交一个Alpha** ，请提供截图。

![图片](images/img_7774cf833c.png)

5. 总结反思（代码较上次有什么功能提升、debug经历、模板适合的数据类型、模板的改进方向等）

- 代码较上次有什么功能提升：将构造和测试分离，插队和sql存储，之后需要将multi模拟加入进去，进一步加速模拟速度。
- 模板的改进方向：第2个模板还没搜到合适的

---

### 评论 #38 (作者: WL13229, 时间: 2年前)

[KZ79256](/hc/en-us/profiles/13609593802263-KZ79256)

看得出来做了有用的工作，才把corr降下来的。值得学习交流。均值加上标准差，即得到一个标准差之后的值。这个Alpha的本质似乎是对某个特征，基于某个条件，进行大小的调整。

---

### 评论 #39 (作者: YW27566, 时间: 2年前)

1.Performance面板中基本面数据较多，尝试使用其他方向的较另类数据  ![图片](images/img_8e1483f1af.png)

2. 发布的alpha灵感链接： [https://support.worldquantbrain.com/hc/en-us/community/posts/21110734836887--Alpha%E7%81%B5%E6%84%9F-Option-Implied-Volatility-Measures-and-Stock-Return-Predictability](/hc/en-us/community/posts/21110734836887--Alpha%E7%81%B5%E6%84%9F-Option-Implied-Volatility-Measures-and-Stock-Return-Predictability)

skew=opt4_273_call_vola_delta25-opt4_273_put_vola_delta50，遍历得出较长的期限，otm call和atm put的组合方式效果更好

3.template: alpha=zscore(A-B);regression_neut(alpha,log(cap));regression_neut(alpha,log(volume))

4. 提交截图：

![图片](images/img_2b601553df.png)

5. 总结反思：对因子进行提纯，标准化，中性化设置等操作后有助于改进alpha，需要针对alpha特点多进行尝试。不合适的提纯，分组方式会削弱alpha表现

---

### 评论 #40 (作者: WL13229, 时间: 2年前)

[YW27566](/hc/en-us/profiles/18162425397783-YW27566)

谢谢分享。请问Template是这样吗

> alpha=zscore(A-B);regression_neut(alpha,log(cap));regression_neut(alpha,log(volume))

如果是这样的话，中间对于cap的提纯是没用上的，因为它的结果没有被一个变量承接。最后您的Alpha和下面这个是一样的。

```
alpha=zscore(A-B);regression_neut(alpha,log(volume))
```

---

### 评论 #41 (作者: ZF71008, 时间: 2年前)

1. Performance 截图 ![图片](images/img_5abb9a54bf.png)

新手上路，目前我提交的alpha很少，下一个策略的选择空间很大，但是model data相对较少，因此这篇笔记从这里下手搜索相关research paper。

开始的时候在平台dataset相关说明里找model相关data，主要检索了cash flow相关的几篇文献，但是其中有一篇提到一句（也有可能是误解了） cash flow相关因子可靠性有争议，自己也没能总结出什么有价值的表达式，就放弃了这个方向。正巧论坛新post了《量化研究推荐论文》这个版块，真的是非常便捷。花了些时间阅读了Research Paper 52: Skewness Preference and Market Anomalies。有些因子测试无法通过corr测试，后来发现论坛此文已经被挖掘过了。为了避免重复，最后选择了这篇文献提到的一篇引用，其中涉及了一种衡量异常的方法：JACKPOT.

引用文献如下：

Conrad, Jennifer, Nishad Kapadia, and Yuhang Xing, 2014, Death and jackpot: Why do individual investors hold overpriced stocks?, Journal of Financial Economics 113, 455–475.

1. 提交：

《Alpha灵感》JACKPOT因子

[https://support.worldquantbrain.com/hc/en-us/community/posts/21119177808663--Alpha%E7%81%B5%E6%84%9F-JACKPOT%E5%9B%A0%E5%AD%90](https://support.worldquantbrain.com/hc/en-us/community/posts/21119177808663--Alpha%E7%81%B5%E6%84%9F-JACKPOT%E5%9B%A0%E5%AD%90)

1. Template分析：

我目前的理解，JACKPOT因子实际上是构建alpha的一部分，可以和很多其他因素一同构建为一个完整的模板。比如上面提到的Research Paper 52: Skewness Preference and Market Anomalies中，可以构建 MIS * JACKPOT 模板。所以搜索空间还是还是很大的，后续我会继续在USA market/D1 尝试挖掘。

1. 成功提交一个alpha，在《Alpha灵感》JACKPOT因子中有部分截图

![图片](images/img_e88f69f88b.png)

![图片](images/img_3b6ce41914.png) 之前的截图：

![图片](images/img_24570e72b8.png)

1. 总结反思：

从文献中总结表达式的能力还很欠缺，需要熟悉对operator以及dataset的使用。接下来准备尝试训练一下chatgpt来辅助总结研报的能力。

---

### 评论 #42 (作者: WL13229, 时间: 2年前)

[ZF71008](/hc/en-us/profiles/20098272506775-ZF71008)

谢谢这位同学的分享。可以分享一下您的《Alpha灵感》JACKPOT因子的链接吗？这会帮助我们尽快Approve这篇帖子。

---

### 评论 #43 (作者: DK85731, 时间: 2年前)

- Performance 截图
- ![图片](images/img_cc33b9889d.png)
- Alpha灵感:  [https://support.worldquantbrain.com/hc/en-us/community/posts/21120326355479--Alpha%E7%81%B5%E6%84%9F-Attention-Implied-Volatility-Spreads-and-Stock-Return](https://support.worldquantbrain.com/hc/en-us/community/posts/21120326355479--Alpha%E7%81%B5%E6%84%9F-Attention-Implied-Volatility-Spreads-and-Stock-Return)
- 模板分析与表现见于 Alpha 灵感文中
- 反思：在撰写本篇评论时无意间发现上期有同学使用了类似的题目 :【Alpha灵感】Volatility Spreads and Expected Stock Returns , 预计前篇同学提交的alpha为同一赛道，导致我有很多因子被一个alpha卡在了0.7的corr ：(。 但细细看来内容也不尽相同，我选取的论文为在之前 Volatility Spreads and Expected Stock Returns 的基础上，运用其他信息进一步优化  。但与此同时，我也发现即使主要因子类似，但在通过其他有效因子进行filter之后，corr也会出现显著降低，故在一些常用因子的基础上使用不常使用的data field进行优化应该也是一个值得尝试的方向。

---

### 评论 #44 (作者: SK24143, 时间: 2年前)

1.performance面板截图

![图片](images/img_6433066de1.png)

由于是新手小白，提交的不多，CHN提交的相对较少，最终选择了东吴证券的一篇研报

2.《Alpha灵感》新价量相关性RPV因子  [《Alpha灵感》新价量相关性RPV因子 – WorldQuant BRAIN](/hc/en-us/community/posts/21120825510551--Alpha%E7%81%B5%E6%84%9F-%E6%96%B0%E4%BB%B7%E9%87%8F%E7%9B%B8%E5%85%B3%E6%80%A7RPV%E5%9B%A0%E5%AD%90)

3. 这个template感觉并不太好进行泛化，因为它考虑的是日内和夜间的一个共同作用，但是我还是试了一下抽象化，试图找到一些与夜间收益率相关的量，其中主要是volume相关的，但试了感觉不太好。

change = open-ts_delay(close,1);

a = ts_corr(change,volume_datafield,60);group_neutralize(a,bucket(rank(cap),range='0,1,0.1'))

4.alpha截图

![图片](images/img_5cb8475788.png)

5.总结与反思

代码方面加上了转化vector的一个函数。在模板方面从研报中得出的太过具体，感觉不好泛化，以后要进一步提高抽取模板的能力。在找论文的时候发现有些观点很难实现，所以感觉找好论文和研报也很关键。下一步准备寻找更多的论文和研报进行尝试，进一步加强实现各种复杂的fast expression的能力，以及提高模板提取能力。

---

### 评论 #45 (作者: YZ64617, 时间: 2年前)

Peformance截图

在开始作业之前，没有 alpha。

现在的

![图片](images/img_f530ab4547.png)

alpha灵感： [【Alpha灵感】Non-Linear Factor Returns in the U.S. Equity Market – WorldQuant BRAIN](/hc/en-us/community/posts/21126691730839--Alpha%E7%81%B5%E6%84%9F-Non-Linear-Factor-Returns-in-the-U-S-Equity-Market)

这篇论文的非线性公式，可以适用于5类factor，我目前只实验了P/E和PM，另外3种完全没有时间去尝试。

公式模板就是按照论文创建创建一个factor，然后使用这个factor，创建3个纬度的变量；之后，将3个变量权重相加。【注意】权重可能是负数，所以，我是通过尝试，确定了第3项是负的。

```
a = 1/PE类datafield；（倒数，构成factor。price momentum则是log）根据论文公式，创建出s1，s2，s3（有完整版，有简化版）signal = s1 + s1 - s3
```

如果需要，可以使用grouping。我使用了下面这种

```
group = bucket(rank(cap), range="0, 1, 0.1");s = group_neutralize(a, group);
```

我通过datafield搜索PE和PM的所有相关数据，获得

- PE-Matrix数据：4147
- PE-Vector：1259
- PM-Vector：541
- PM-Matrix：1541

经过测试universe=Slow Factors表现会更好。USA TOP3000 （ILLIQ效果也不错）。

基于上面这些datafield，一共生成了14968个alpha，截止目前，完成了8900个，耗时21小时，还在跑。也许是因为alpha略微复杂了一点，速度明显比之前刷了1万次模拟慢了很多很多。

目前有100左右通过IS Testing，但是，死在了self corr上，因为我已经提交了2个alpha。对于PE数据，Product Corr和Self Corr是两大难题。不过已经满足，每一个dataset中的PEdatafields是相关度很高的，所以也造成了这样的结果。不过，等所有alpha都跑完，其他dataset的alpha应该还会有几个可以提交。

这周，提交了3个alpha

![图片](images/img_b74ac96c8d.png)

### 

### 思考和一些感想

需求越来越多，所以，考虑整理和优化一下python的函数功能。例如，根据settings或/和search词找dataset和datafield；当大批量simulation的时候，定时或者人工触发从IS alpha中找到alpha的结果，尤其是通过IS testing的；Check simulation和检查corr的函数（没想明白这些返回值应该处理到什么程度）

在手工调试alpha的时候，一点点摸索出了一些思路。对于模版的通用书写规则，感觉需要固定。例如，alpha可以写出不同层级，初级版a1=一个信号，如果表现不好，升级到第二版：a1=***；a2=function(a1)，之后还可以升级为第三版，还可以添加grouping，而grouping方法还可以有不同的版本。这样，可以编出一套逻辑，通过通用的模版，挖掘alpha。

读论文，收获很大，不知不觉领会了一些技巧。其实，灵感论文是我读的第3篇。第一篇读的是“A Fibonacci Heap based Ensemble Model for Stock Price Prediction”，论坛推荐的论文，同时还推荐的dataset。但是，最后也没有搞明白如何去ensemble dataset.id=mdl122的datafield。mdl122就是一个坑，通过descroption无法获得任何有价值的信息，我试探的跑了9000多个simulation，最高的sharpe是1.5，只能放弃。很好奇其他大神是怎么试探出来的。ensemble有对应的brain的operator可以组合出来吗？

关于alpha的优化，我的这个论文总结出来的公式，还有3类factor我可以尝试。那它的模版，也许套用到其他factor上也会有效。另外，还是对于一些operators理解不深，敏锐度不够。

---

### 评论 #46 (作者: XZ75239, 时间: 2年前)

![图片](images/img_ebad87711a.png)

之前提交中国市场基本面相关的因子比较少，于是读了这篇论文《SmallMinusBig Predicts BettingAgainstBeta: Implications for
International Equity Allocation and Market Timing》并在中国市场实践，论文大意是如果前段时间小市值表现得好，那么市场流动性会增加从而导致BAB策略更加奏效？

我在中国市场试了一下做多低beta，做空高beta的策略，并没有奏效，做多高beta反而有信号。然后我加上了前段时间小市值表现得好的条件，然而也并没有奏效。。。

但是我没放弃，联想到最近国内市场，2024经历了2023年的小市值狂欢后开局惨淡，只有国家队拉住的大市值股票让中小值股票既亏alpha又亏beta，很多因子都失效了，本周一还迎来了千股跌停的奇观。我还是很想知道小市值狂欢后，资金去哪儿了，什么策略还能奏效呢？

于是我的template是：returns_c=-group_mean(returns,rank(cap)>0.8?1:0,market)+group_mean(returns,rank(cap)<0.2?1:0,market);

ts_sum(returns_c,5)>0?factor1:factor2

然后试了一系列因子，提交了两个

![图片](images/img_bd1cc343c3.png)

思考：也许可以再试试当交易集中度过高/市场全面大跌等等情况下因子如何切换能够避过大回撤，同时考虑到中国无法卖空，可以手动构造买股票卖空指数的策略看看真实效果。。

这是我发的帖子。。。

【alpha灵感】小市值狂欢之后什么策略有效？

[https://support.worldquantbrain.com/hc/en-us/community/posts/21145402272663--alpha%E7%81%B5%E6%84%9F-%E5%B0%8F%E5%B8%82%E5%80%BC%E7%8B%82%E6%AC%A2%E4%B9%8B%E5%90%8E%E4%BB%80%E4%B9%88%E7%AD%96%E7%95%A5%E6%9C%89%E6%95%88](https://support.worldquantbrain.com/hc/en-us/community/posts/21145402272663--alpha%E7%81%B5%E6%84%9F-%E5%B0%8F%E5%B8%82%E5%80%BC%E7%8B%82%E6%AC%A2%E4%B9%8B%E5%90%8E%E4%BB%80%E4%B9%88%E7%AD%96%E7%95%A5%E6%9C%89%E6%95%88)

---

### 评论 #47 (作者: WL13229, 时间: 2年前)

[XZ75239](/hc/en-us/profiles/13987002908183-XZ75239)

不用担心，可以就分享你读的那篇文章，或者尝试了哪些factor。另外，其实自己的idea就已经是一个很好的帖子了，你已经是一个创作人。相信很多同学都会想看到你的分享。

---

### 评论 #48 (作者: WL13229, 时间: 2年前)

[YZ64617](/hc/en-us/profiles/4527497709335-YZ64617)

很高兴你已经逐渐领悟到了一种搜索的方向及尝试通用的搜索方式。这就是Template的进阶版。不过这类的实施，需要在大回测资源和对数据有更多理解的时候，效率更高。

---

### 评论 #49 (作者: EC34309, 时间: 2年前)

1. Performance面板截圖，選擇相關方向的文章

For some reason I couldn't find the original screenshot, but my alpha distribution was lacking CHN market alpha, so I chose a paper focusing on CHN.

1. 【华泰金工林晓明团队】基于遗传规划的一致预期因子挖掘

[https://support.worldquantbrain.com/hc/en-us/community/posts/21146151322519--Alpha%E7%81%B5%E6%84%9F-%E5%8D%8E%E6%B3%B0%E9%87%91%E5%B7%A5%E6%9E%97%E6%99%93%E6%98%8E%E5%9B%A2%E9%98%9F-%E5%9F%BA%E4%BA%8E%E9%81%97%E4%BC%A0%E8%A7%84%E5%88%92%E7%9A%84%E4%B8%80%E8%87%B4%E9%A2%84%E6%9C%9F%E5%9B%A0%E5%AD%90%E6%8C%96%E6%8E%98](https://support.worldquantbrain.com/hc/en-us/community/posts/21146151322519--Alpha%E7%81%B5%E6%84%9F-%E5%8D%8E%E6%B3%B0%E9%87%91%E5%B7%A5%E6%9E%97%E6%99%93%E6%98%8E%E5%9B%A2%E9%98%9F-%E5%9F%BA%E4%BA%8E%E9%81%97%E4%BC%A0%E8%A7%84%E5%88%92%E7%9A%84%E4%B8%80%E8%87%B4%E9%A2%84%E6%9C%9F%E5%9B%A0%E5%AD%90%E6%8C%96%E6%8E%98)

核心交易idea是什麼？

The change of EPS estimate by analysts positively correlates returns.

是否找到數據：

mdl26_ep_yield_smartestimate_fy1

是否找到Universe: 例如TOP 200, （一般金融論文都會明確說出其適用的股票類型）

All A shares.

是否找到Neutralization: Sector (Smart Search)

Market

使用什麼operator

group_rank

績效（需保證Sharpe至少大於1.3，Fitness至少大於0.6，Turnover低於45%，高於5%；透過PROD相關性測試） ![图片](images/img_dd3ee543a4.png)

Insufficient, 3 additional hypotheses are suggested.

1.Combining smart estimate growth with the growth next yr sector percentile earnings provides a view of expected growth against current valuation.

2.A high earnings yield alongside expected sector-leading growth for the next year could signal potential for returns.

3.Changes in Mean of Estimations of Returns on Equity - upcoming 2 years could correlate with return.

Final result:

![图片](images/img_bc1f07377a.png)

![图片](images/img_a2e107d5bd.png)  ![图片](images/img_af966a5714.png)

1. Template分析，闡述其抽象後可以提取什麼信息，不同條件下的搜索空間可能有多大，有什麼獨特的操作，適用什麼universe,週期等。

1. analyst EPS estimate:

A consistent opinion on a prediction by the analyst correlates with return.

Increasing the search space to any analyst prediction.

1. Compounding analyst estimates
2. Compounding estimates with robust fundamentals

It is worth mentioning I originally wish to come up with a complementary alpha to stabilize this alpha using sentimental data, but it seems that it is not easy to come up with a sentiment alpha in CHN that is profitable enough, perhaps suggesting the relative lack of impact in social media compared to other markets.

4.本次作業硬性要求至少成功提交一個Alpha，請提供截圖。

screenshot provided above.

1. 總結反思（程式碼較上次有什麼功能提升、debug經驗、模板適合的資料類型、模板的改進方向等）

Summary of my workflow:

1. Generate alpha ideas from papers and generative AI.
2. Implement those ideas
3. Superimpose alphas with weak correlations

I wasted a lot of them on generating those ideas. I believe this could be improved by solely focusing on the passage that talks about the variables related to returns.

Questions:

1. I believe I still lack the skill to effectively use fast expression, as I still use a limited set of operators. I would very much appreciate any tricks to smooth the curves (ideally lots of them).
2. I also struggle to interpret using residual/vector neutralization, is it correct to interpret that if the residual/unexplainable return implies the stock has excess return which is more than enough to compensate for the risk? Then why not just long the residual instead, but the implementation for the factor model seems to be different.

market_ret = ts_product(1+group_mean(returns,1,market),250)-1;

rfr = vec_avg(fnd6_newqeventv110_optrfrq);

expected_return = rfr+beta_last_360_days_spy*(market_ret-rfr);

actual_return = ts_product(returns+1,250)-1;

actual_return-expected_return

From “Alpha Examples for Silver Users”

I couldn’t understand why this is the correct implementation, I would be very grateful if anyone could give me a detailed explanation.

---

### 评论 #50 (作者: YL37225, 时间: 2年前)

大家好，我本周尝试复现一篇论文的alpha，但是还没有得到可提交的alpha
1.performance面板

![图片](images/img_9480ce1313.png)

之前提交过的alpha并不多。
2.选择阅读的论文

site:  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2472571](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2472571) 
Are Cash Flows Better Stock Return Predictors than Profits?
3.论文主要说明直接现金流法得到的 Net Cash Flows from Operations after Financing Activities除以total asset，能比较好地预测股票收益。
我的template形式如下：

#data fields

x1=sales;

x2=fnd65_allcap_sedol_salerec;

x3=revenue;

x4=cash;

x5=vec_avg(fnd6_cogss);

x6=vec_avg(fnd6_newqeventv110_xsgaq);

x7=fnd23_intfvm_bpao;

x8=fnd72_s_pit_or_cf_q_cf_change_in_inventories;

x9=fnd3_A_int_exp;

x10=vec_avg(fnd72_pit_or_is_q_is_inc_tax_exp_other_comp_inc);

x11=vec_avg(fnd72_pit_or_bs_a_bs_tot_asset);

#fast expression

y=x1+x2+x3+x4+x5+x6+x7+x8+x9+x10;

z=y/x11;

# z=(cashflow_op + cashflow_fin) / mdf_tas;

# 首先，使用quantile运算符对x进行分位数排名

z_quantile = quantile(z, driver = uniform);

# 定义两个阈值，用于识别前10%和后10%

lower_bound = 0.1;

upper_bound = 0.9;

# 为排名前10%的股票分配正权重，排名后10%的股票分配负权重

# 使用条件表达式，其余保持为0（不投资）

weights = if_else(z_quantile <= lower_bound, -z, if_else(z_quantile >= upper_bound, z, 0));

# 输出加权后的Alpha值

weights;

4.目前的结果如下：
 ![图片](images/img_1184af59e5.png)  ![图片](images/img_ec3ea81b8d.png)

![图片](images/img_62a738a4c6.png)

有一些指标似乎表现还挺好，但是我还不太明白前面为什么曲线是平的？可能我对平台的一些理解还不对，请大家指证。

---

### 评论 #51 (作者: WL13229, 时间: 2年前)

@ [YL37225](/hc/en-us/profiles/17548796152983-YL37225)

还烦请将阅读的论文分享成一篇文档发送至中文论坛

---

### 评论 #52 (作者: WL13229, 时间: 2年前)

[EC34309](/hc/en-us/profiles/13557080755991-EC34309)

您好。看到您使用了GPT的帮助，这是非常好的，它会很有效地帮助你。

1. 关于Alpha Example. 它是基于CAPM模型进行的。它认为由CAPM模型计算出来的return应该为股票的“真实价值return”。但是如果股票的market return高于CAPM模型算出的return，则说明市场给了该股票更高的溢价，它会有momentum的趋势继续上涨。希望这样的解释能给您帮助。

2.

> I wasted a lot of them on generating those ideas. I believe this could be improved by solely focusing on the passage that talks about the variables related to returns.

我猜想您说的是，您希望复现这篇研报的工作流程。它确实是有难度的，先从简单的做起，一步步来。

3. 以下是一些通用的residual概念：在回归中，如果将变量A做为因变量Y，变量B作为自变量X。将A和B做个回归，那么residual就代表了，A的变动中，无法被B解释的那一部分。

---

### 评论 #53 (作者: DZ54968, 时间: 2年前)

1.由于刚成为顾问，各板块Alpha都比较少，由于Model类相关Alpha最少，因此我选择阅读Research Paper 27: Earnings Uncertainty and Attention

2.《Alpha灵感》文章：【Alpha灵感】盈利不确定性和公司关注度

3. Template分析

a = group_rank(ts_regression(zscore(ts_mean(-A,T)), zscore(B), T, lag=63, rettype=2), densify(market));

b = group_neutralize(a, bucket(rank(cap), range='0.1,1,0.1'));

trade_when(C>ts_mean(C, 21), b, abs(returns)>0.1)

该模板对预处理后的两变量进行相关性分析，后采用group和trade_when进行过滤，以预测价格飘移趋势。

4.Alpha提交

虽然本周已尽力尝试，但未能得到可提交Alpha。表现相对较好的Alpha截图如下：

![图片](images/img_431dc5d7a9.png)

5.总结反思

由于对平台运算符和数据不够熟悉，手工构建的模板可能并不足以挖掘有效Alpha。即使尝试了无数种datafield和参数组合，仍然无法获得有效Alpha。总结反思失败教训，一方面认为对于论文的理解不够，没有从中提炼出较好的策略模板，导致纯靠机器暴力挖掘也无法得到可以提交的Alpha；另一方面对于平台使用的熟练度不够，对于数学运算符和数据集的理解不够深入，导致难以复现论文思路或者实现自己对于策略的一些想法。之后的改进方向将从多读论文体会不同论文的策略思想，并多亲手实践，尽可能快地构建自己的alpha模板

---

### 评论 #54 (作者: WL13229, 时间: 2年前)

[DZ54968](/hc/en-us/profiles/18130763917463-DZ54968)

烦请附上《Alpha灵感》的链接，便于我们快速审核

---

### 评论 #55 (作者: DZ54968, 时间: 2年前)

补充【Alpha灵感】链接： [【Alpha灵感】盈利不确定性和公司关注度 – WorldQuant BRAIN](/hc/en-us/community/posts/21149732774039--Alpha%E7%81%B5%E6%84%9F-%E7%9B%88%E5%88%A9%E4%B8%8D%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%92%8C%E5%85%AC%E5%8F%B8%E5%85%B3%E6%B3%A8%E5%BA%A6)

---

### 评论 #56 (作者: WL13229, 时间: 2年前)

[DZ54968](/hc/en-us/profiles/18130763917463-DZ54968)

辛苦在原评论或灵感文章中，分享一些关于check list的内容。例如

《Alpha灵感》文章中必须包含的内容

- 核心交易idea是什么？
- 是否找到数据：
- 是否找到Universe: 例如TOP 200, （一般金融论文都会明确说出其适用的股票类型）
- 是否找到Neutralization: Sector (Smart Search)
- 使用什么operator
- 核心Alpha的Expression（可选）
- 绩效

---

### 评论 #57 (作者: QH29412, 时间: 2年前)

1. Performance面板截图。选择了USA，TOP3000 ![图片](images/img_8f417fafc2.png)
2. 《Alpha灵感》文章- [Back to Fundamentals: The Accrual-Cash Flow Correlation, the Inverted-U Pattern, and Stock Returns](/hc/en-us/community/posts/16412726318231-Research-Raper-22-Back-to-Fundamentals-The-Accrual-Cash-Flow-Correlation-the-Inverted-U-Pattern-and-Stock-Returns)
3. Template分析，文章中说accruals 和employment growth rate，accrual 和 CFO 的负相关性, 都对returns 有很强的预测能力。所以同时满足横截面分析和时间序列分析操作，ts_regression 和regression_neut 都有效果。
4. ![图片](images/img_fd880af184.png)  ![图片](images/img_1ae43439b5.png)
5. 目前alpha还在优化中，turnover 略高，Prod correlation 0.8353 is above cutoff of 0.7 and Sharpe not better by 10.0% or more.
6. 我是用postman 做自动化，个人觉得程序提交simulation比较适合去降低prod corr，搜索范围比较小。前期还在构建框架的时候，搜索范围太大。

fnd6_idit

---

### 评论 #58 (作者: WL13229, 时间: 2年前)

@ [QH29412](/hc/en-us/profiles/18659551926295-QH29412)

烦请发布一篇《Alpha灵感》的文章，阐述一下研究过程。

《Alpha灵感》文章中必须包含的内容

- 核心交易idea是什么？
- 是否找到数据：
- 是否找到Universe: 例如TOP 200, （一般金融论文都会明确说出其适用的股票类型）
- 是否找到Neutralization: Sector (Smart Search)
- 使用什么operator
- 核心Alpha的Expression（可选）
- 绩效（需保证Sharpe至少大于1.3，Fitness至少大于0.6，Turnover低于45%，高于5%；通过PROD相关性测试）

---

### 评论 #59 (作者: SW14484, 时间: 2年前)

1. Performance面板截图 ![图片](images/img_b9dd377878.png)

不难发现，我的Alpha分布主要是在USA分区，所以我这次选择CHN分区

1. 我找的是一篇研报：A 股反转之力的微观来源

并发布在了中文论坛里的【Alpha 灵感】：

[https://support.worldquantbrain.com/hc/en-us/community/posts/22071441537303--Alpha%E7%81%B5%E6%84%9F-A-%E8%82%A1%E5%8F%8D%E8%BD%AC%E4%B9%8B%E5%8A%9B%E7%9A%84%E5%BE%AE%E8%A7%82%E6%9D%A5%E6%BA%90](/hc/en-us/community/posts/22071441537303--Alpha%E7%81%B5%E6%84%9F-A-%E8%82%A1%E5%8F%8D%E8%BD%AC%E4%B9%8B%E5%8A%9B%E7%9A%84%E5%BE%AE%E8%A7%82%E6%9D%A5%E6%BA%90)

1. Template分析：

我的抽象Alpha Template如下：

x = vec_sum(A)  

# 计算x的某个百分比值  
y1 = ts_percentage(x, window_size, percentage=percentage1)  
y2 = ts_percentage(x, window_size, percentage=percentage2)  

# 根据条件计算加权和  
M_high = ts_sum(if_else(x > y1, B, 0), window_size)  
M_low = ts_sum(if_else(x < y2, B, 0), window_size)  

# 计算Alpha值  
Alpha = M_high - M_low  

# 返回Alpha的相反数  
return -Alpha

这里的核心的Template其实就是根据论文里的Idea，按照不同的分位数得到两个次一级的Alpha: A和B，而这两个Alpha衡量的是相反的信息，所以通过计算A-B，得到反转的Alpha因子。

![图片](images/img_e73621937f.png)

![图片](images/img_06bf8132f4.png)

1. 成功提交的Alpha:

![图片](images/img_8eabcbc403.png)

5.总结和反思

1）之前急于开始用machine进行搜索，但是没有深入研究template，最后浪费了许多时间，还是应该多花时间在template背后的经济学原理，而不是大力出奇迹上。有一个疑问是如何提升特定日期的 [IS ladder Sharpe](/hc/en-us/articles/6726865162903)  ，有几个Alpha因为这个原因 过不了。

2）代码提升：进行了提取相关信息包括sharpe等信息，但是有个问题是如何提取IS Testing Status部分的信息，因为它每次运行的输出其实不是确定的。

---

### 评论 #60 (作者: WL13229, 时间: 2年前)

[SW14484](/hc/en-us/profiles/20580045390871-SW14484)

其实IS Ladder不通过，是一个很强的提示，即其在最近一段时间内表现不佳。因此我还是建议从idea出发去修改它。首先我建议使用visualization的功能，查看近几年表现不佳是某些市值层面的失效的还是行业的失效。之后尝试使用vector neutral去中和这个特点。另外的思路是，这个本质是一个反转的策略，不妨和其他反转策略的思路结合起来。

---

### 评论 #61 (作者: WL13229, 时间: 2年前)

[BC25356](/hc/en-us/profiles/13921805253911-BC25356)

关于疑问一，self corr和prod corr往往需要额外触发，才能得到结果。其实理论上，对于每个Alpha,即便你不进行任何IS的checks，你都可以写代码发送提交请求，只是服务器会拒绝而已。

关于疑问二，返回location即等于网站上点击simulate后出现了进度条，使用for 函数在出现了进度条后即进行下一个，并不需要等待Alpha运行结束，这样并不会慢。再次表达我的个人意见，我认为在发送Alpha这个阶段使用多线程是没有必要的。

---

### 评论 #62 (作者: BC25356, 时间: 2年前)

[WL13229](/hc/en-us/profiles/12285040305687-WL13229)

谢谢您的解答。

关于疑问一：我这样理解，并不能通过check里面对应的值来判断，是否可以提交alpha。因为self corr和prod corr往往需要额外触发，所以他们一定是Fail的。但是我们可以判断一些指标，如果这些指标都通过了，我们把这些alpha选出来，在网页是确认提交。是否正确？

关于疑问二：请您看下，我修改前的代码。因为在修改前，我一个小时只能跑120个alphas左右。一个小时为3600秒，而我从发送reques，并等到.json["alpha]的结果，才会进行下一个。从发送到得到结果，需要25～35秒。所以一个小时大致会有120个alpha被发送，并得到alpha id。当代码在跑，我打开网页还可以继续开8~9个simulations，所以我觉得是我代码的问题，请老师帮我看下。

---

### 评论 #63 (作者: WL13229, 时间: 2年前)

[BC25356](/hc/en-us/profiles/13921805253911-BC25356)

您说的大致正确。

关于疑问一，并非“一定是Fail”，而是大部分时候可能是空值（在不触发前），确实也在技术效果上跟fail没有什么差别。手动提交是可以的。查看API的相关帖子，你可以看到修改Alpha颜色的code,你可以把这种有高潜力的Alpha标记颜色，方便后续手动检查。

关于疑问二，你可以参考我们在课上提供过的一个解决方案。即您不需要等待.json["alpha"]的结果出来，您只需要在运行下面这一行不报错的情况下，就应该发送下一个Alpha了。不需要使用while true去等.json["alpha"]的结果出来。

![图片](images/img_8ba150c2d8.png)

后面再从IS列表批量取得Alpha performance

---

### 评论 #64 (作者: YZ31807, 时间: 2年前)

1.Alpha面板

![图片](images/img_6fd3022cc8.png) 可见在CHN较少，于是本周尝试了CHN地区的alpha

2.Alpha灵感文章

[https://support.worldquantbrain.com/hc/en-us/community/posts/22130841774359--Alpha%E7%81%B5%E6%84%9F-%E4%BC%B0%E5%80%BC%E5%9B%A0%E5%AD%90](https://support.worldquantbrain.com/hc/en-us/community/posts/22130841774359--Alpha%E7%81%B5%E6%84%9F-%E4%BC%B0%E5%80%BC%E5%9B%A0%E5%AD%90)

3.template分析

D=RANK(A)*ts_rank(B*C)

group_neutralize(D，mygroup)

其中A是基本面相关Alpha，B与C是根据研报引入的估值类因子BP和SP的实现。

随后，利用上周使用的模板进行大批量回测。在筛选数据时，主要针对BP/SP因子中的组成进行组合筛选，在约500个样本中得到了可以提交的alpha。

4.提交截图

![图片](images/img_fd09113d7b.png)

5.总结反思

在本周我优化了我的上周的模板，使得在筛选alpha中能自动保存alpha的list。在进行alpha构建时，采用了中性化以及与基本面因子结合的办法提高了alpha表现。对于API有一个小小的疑问，可以直接使用API筛选出合格的alpha并且直接提交吗？

---

### 评论 #65 (作者: BC25356, 时间: 2年前)

1. 因为刚开始做研究，所以都是蓝海，选择了最近特别感兴趣，高估值与成长性的话题，所以我选择了

[https://support.worldquantbrain.com/hc/en-us/community/posts/14983690885911-Research-Paper-23-Overvalued-Equity-and-Financing-Decisions](/hc/en-us/community/posts/14983690885911-Research-Paper-23-Overvalued-Equity-and-Financing-Decisions)

![图片](images/img_244e03fd25.png)

2.【Alpha灵感】高估值与融资决策

[https://support.worldquantbrain.com/hc/en-us/community/posts/22155076343831--Alpha%E7%81%B5%E6%84%9F-%E9%AB%98%E4%BC%B0%E5%80%BC%E4%B8%8E%E8%9E%8D%E8%B5%84%E5%86%B3%E7%AD%96](/hc/en-us/community/posts/22155076343831--Alpha%E7%81%B5%E6%84%9F-%E9%AB%98%E4%BC%B0%E5%80%BC%E4%B8%8E%E8%9E%8D%E8%B5%84%E5%86%B3%E7%AD%96)

3. Template分析

```
condition = rank(A);trade_when(condition > 0.8, group_rank(B, group), -1)
```

**抽象** ：通过A进行选股，根据B，进行做空。

**适用Universe** ：因为文章中多次提到small size和High tech innovation company，所以我选择TOP3000

4.  ![图片](images/img_3a829ff47c.png)

5.

- **代码改进：** 从一个小时跑120个到900个Alpha的突破（其实就是一个循环的改变）；并返回alpha结果时候，自动标记可以提交的alpha
- **debug经历：** 卡在获取Location上，一直报proxyerror，最后通过continue很快解决
- **Template改进** ：1. 我想继续深挖论文研究Momentum方向；2. 对于现在的Reversal模版，我觉得可以在对B数据进行深度研究

---

### 评论 #66 (作者: WL13229, 时间: 2年前)

[YZ31807](/hc/en-us/profiles/18243220367511-YZ31807)

一个很完整的作业。是可以用API筛选并提交的，但是我建议在研究的初期，还是通过手动提交比较好，可以人为最后做一次检查和思考。另外，如果担心Alpha淹没在列表中，可以对pass IS Test的Alpha进行颜色的修改，很快就能筛选出来了。

---

### 评论 #67 (作者: WM13885, 时间: 2年前)

**1. alpha 面板截图（作业完成后）：**

![图片](images/img_800558f95d.png)

结论：什么alpha都缺
 **2. post**

【Alpha灵感】换手率因子tps_turbo：如何用纯净化GTR因子增强传统换手率因子

[https://support.worldquantbrain.com/hc/en-us/community/posts/22162473785623--Alpha%E7%81%B5%E6%84%9F-%E6%8D%A2%E6%89%8B%E7%8E%87%E5%9B%A0%E5%AD%90tps-turbo-%E5%A6%82%E4%BD%95%E7%94%A8%E7%BA%AF%E5%87%80%E5%8C%96GTR%E5%9B%A0%E5%AD%90%E5%A2%9E%E5%BC%BA%E4%BC%A0%E7%BB%9F%E6%8D%A2%E6%89%8B%E7%8E%87%E5%9B%A0%E5%AD%90](https://support.worldquantbrain.com/hc/en-us/community/posts/22162473785623--Alpha%E7%81%B5%E6%84%9F-%E6%8D%A2%E6%89%8B%E7%8E%87%E5%9B%A0%E5%AD%90tps-turbo-%E5%A6%82%E4%BD%95%E7%94%A8%E7%BA%AF%E5%87%80%E5%8C%96GTR%E5%9B%A0%E5%AD%90%E5%A2%9E%E5%BC%BA%E4%BC%A0%E7%BB%9F%E6%8D%A2%E6%89%8B%E7%8E%87%E5%9B%A0%E5%AD%90)

**3.template分析：** 
因为参考的文章对同样的template做不同的operator下的处理，如均值，标准差，市值提纯，中性化的处理等，所以核心template还是:
a = {volume_element}/sharesout
目前感觉换手率因子的可代替的数据字段或者template本身无法做到特别抽象，也想过做booster，比如拿基本面因子做一个b =（1+rank（{fundamental}））然后去做a*b组合，但试着跑了500个，并不是很理想。

**4. alpha提交截图：**

![图片](images/img_bb1bf27a1b.png)

**5.总结：** 
这周代码上面做了很多优化，做了模块化提高了效率，多了上面提到的可以做数据字段组合的功能。同时，做了把表现结果导入cvs的功能，尤其是在我筛选IS_Ladder_Shape value 的时候很省时间。但发现如果在跑simulation的时候去拿结果返还的id和数据会导致回测变慢，并且10个回测额占不满，多线程是否能解决这个问题？而在simulation跑完后去fetch is alpha performance似乎不能拿到所有实时的数据？导出来的并不是刚跑完的数据，而是前段时间的。

可以改进的方向：
对代码和理解论文/研报，template的构建做更深的研究，是否能在不同settings（universe）下多次回测？同时做一个更多指标的可视化，导入csv或者能够直接对value做筛选的功能。

---

### 评论 #68 (作者: WH24469, 时间: 2年前)

**1．Performance面板**

目前提交的alpha较少，所以没有数据偏向，选择阅读：Overnight returns, daytime reversals, and future stock returns

**2．Alpha灵感**

链接为： [【Alpha灵感】隔夜与日内拉锯战暗藏的信息 – WorldQuant BRAIN](/hc/en-us/community/posts/22174527569303--Alpha%E7%81%B5%E6%84%9F-%E9%9A%94%E5%A4%9C%E4%B8%8E%E6%97%A5%E5%86%85%E6%8B%89%E9%94%AF%E6%88%98%E6%9A%97%E8%97%8F%E7%9A%84%E4%BF%A1%E6%81%AF)

1. **Template分析**

首先是将数据抽象化，将close替换为（close+vwap）/2，一方面降低数据的prodC，一方面又将volume的信息融合进来。

其次是对回归的抽象化，文章中采用将AB_NR、AB_PR等指标对各项公司的相关基本面指标进行回归，但本人采用将收益率剔除这部分情绪波动的信息，再剔除风险类信息，得到最终指标，意在筛选出那些不受市场情绪影响的，能带来稳定收益的标的。

抽象化后，不近价格会受到隔夜回报的影响，同时成交量中的信息也会对价格造成印象，此外，情绪波动造成的价格波动在市场中带来的影响并不会长期存在，经过纠正后便会回到正常水平。

**4．提交截图**

目前prodC还未达标，且turnover处于65%左右，还在进一步优化，不知道是否是有其他consultant已经提交过这篇论文的alpha了，但论坛并未搜索到相关帖子。

**5.反思**

此次复现过程中，有遇到数据不知道怎么找，表达式不知道怎么用的情况，对brain平台的使用还不够熟练。此外，复现过程中使用无人挖掘的数据较少，更多的使用的是常规使用的数据及operators，导致总是面临prodC不达标的情况，后期需要提升自己使用新operators和datasets的能力。

---

### 评论 #69 (作者: WL13229, 时间: 2年前)

[WM13885](/hc/en-us/profiles/20518086330647-WM13885)

感觉做得有点急躁了，template过于简单，可能大概率无法过滤出有效的信息。还需要更多努力.

"也想过做booster，比如拿基本面因子做一个b =（1+rank（{fundamental}））然后去做a*b组合，"

我认为这样的做法并不是什么booster，相反，这似乎有不小的overfitting风险

---

### 评论 #70 (作者: WL13229, 时间: 2年前)

[WH24469](/hc/en-us/profiles/13991511763607-WH24469)

可以使用trade when的方式，仅在某些情况，例如市场波动大的时候再交易，可以显著降低turnover。

---

### 评论 #71 (作者: SW49904, 时间: 2年前)

抱歉有些超出DDL提交，我的灵感来自于文章： [https://www.damray.com/FileUpload/OfficeFile/76df04556ba547f8a84d062e2b4dfb19.pdf](https://www.damray.com/FileUpload/OfficeFile/76df04556ba547f8a84d062e2b4dfb19.pdf)  ，主要基于六种常见的股票投资策略，包括KDJ指标、蜡烛图和蜡烛图形态等。

我希望通过多因子模型结合不同的技术指标，以提高对股票价格走势的预测能力。KDJ指标可以帮助确定股票的超买和超卖位置，蜡烛图可以帮助识别市场的趋势和反转点，蜡烛图形态可以进一步增强对价格趋势的判断。例如，在KDJ指标显示股票处于超买状态时，如果出现了反转型的蜡烛图形态，如倒锤子或射击之星，那么这可能是一个更可靠的卖出信号。

我构造的Alpha主要形态如下：

*W1* *-(close-low)/(high-low)+ *W2* *-(high-open)/close+ *W3* *ts_mean(-(close-low)/(high-low), 10)，其中前两项我经过消融测试发现在sharpe和fitness的表现上是1+1>2的，而第三项主要是用来降低turnover的。

![图片](images/img_dc34f1a702.png)

对于universe我主要对比了中美市场，经过多次对于Alpha表达式以及Neutralization的调整，我发现该Alpha在CHN中似乎无法避免2015年的股灾，因此我最终选择了USA，并通过循环搜索来找到合适的Nrutralization（Subindustry）和Universe （TOP3000）。

从上述checks中我们可以发现，现在的自相关性非常高，这是令我很头疼的，我没有太好的解决办法，只能通过加入一个自由项到这个多因子模型中，类似于 *W1* *-(close-low)/(high-low)+ *W2* *-(high-open)/close+ *W3* *ts_mean(-(close-low)/(high-low), 10)+0.1*epsilon，而后我通过暴力搜素可以使得Alpha通关的epsilon最终得到提交如下：

![图片](images/img_7967ad21fe.png)  ![图片](images/img_acd96672fb.png)

反思：我觉得自己用的方法非常笨，其中我也尝试了其他方向的文章比如舆情等，但是构造出因子的表现并没有达到预期，甚至没有什么优化空间，这让我非常头疼。而对于量价数据相关的文章，构造出了很多在IS阶段通过测试的因子，再最终的test却总有不同的指标无法通过筛选，目前除了用一些暴力和简单的方法，自己并没有太多思路，还很迷茫。

---

### 评论 #72 (作者: ZY25767, 时间: 2年前)

大家好，这是我本周的交付内容，本周提交了很多实验的alpha，但是没有得到一个好的alpha，因为不太知道怎么把python转换成fast expression

1. Performance面板截图，选择相关方向的文章

![图片](images/img_4d5c416bad.png)

2.《Alpha灵感》文章

Cranes among chickens: The general-attention-grabbing effect of daily price limits in China’s stock market

[https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4073997](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4073997)

This paper examines the general-attention-grabbing effect of daily price limits in China’s stock market. We calculate the proportion of stocks that hit daily price limits and use it to construct a proxy of absolute price limits beta to measure the sensitivity of stock returns to daily price limits. We find that stocks with higher absolute price limits beta attract more investors’ attention and have lower future returns. We show that the predictive power of absolute price limits beta cannot be explained by other stock characteristics. The general-attention-grabbing effect is stronger among stocks that are heavily invested by retail investors.

**Keywords:**  Chinese Stock Market, Daily Price Limits, General-Attention-Grabbing Effect

```
ZT = (stock_close - stock_open) / stock_open
```

```
number_of_stocks = ZT.T.count()ZT = abs(ZT) >= 0.09number_of_stocks_toomuch = ZT.T.sum()factor = number_of_stocks_toomuch / number_of_stocksfactor.replace(np.nan, 0, inplace = True)
```

说白了。

一个指标ZT：涨跌停股票占比。

因子值：股票对ZT的敏感程度（用回归系数来衡量）

```
model = sm.OLS(Y_subset, X_with_const)regression_results = model.fit()results[end_date] = regression_resultsprint(regression_results.params)
```

总结与反思：

对Fast Expression 和 dataset 不够熟悉。除了阅读论文，我尝试过程中大多数时间花在了如何写fast expression 上，而且常常写出来的表达式无法准确表达文章观点。希望可以等我有了我的consultant之后可以更加好的去请教。

---

### 评论 #73 (作者: DL92496, 时间: 2年前)

![图片](images/img_86a3f46f8c.png)

1. Performance 面板截图，选择期权相关的文章

2.文章题目：The Information Content of Option Demand（ [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2005763](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2005763) ）

3. Template分析

rank(-ts_regression(returns, ts_delta(opt6_ioc,day_decay),y)-ts_regression(returns, power(ts_delta(opt6_ioc,day_decay),2) , y))

文章中提出了Total call option interest 因子的变化率和收益呈现负向关趋势，因此建立上述Alpha Template，并使用python扫描不同的回归天数y。

![图片](images/img_1c43fbab23.png)

扫描后依然无法满足Prod correlation的结果。

4.失败原因分析

可能需要引入交易条件，正在探索交易条件判断的因子。

---

### 评论 #74 (作者: WL13229, 时间: 2年前)

[DL92496](/hc/en-us/profiles/13716888353687-DL92496)

请发送一篇《Alpha灵感》文章

---

### 评论 #75 (作者: DL55804, 时间: 2年前)

1、我的面板如下，我选择论文《Limit Order Clustering and Stock Price Movements》 **限价订单聚集对股票价格的影响。**

![图片](images/img_04883381b9.png)

2、【Alpha灵感】限价订单聚集对股票价格的影响

文章链接： [../PN39025/[Commented] 【Alpha灵感】限价订单聚集对股票价格的影响.md](../PN39025/[Commented] 【Alpha灵感】限价订单聚集对股票价格的影响.md)

3、

价格聚集效应：投资者的限价订单倾向于在整数价格点（如X.0）及其附近聚集。这些聚集的限价订单形成了价格支撑或压力，使得股票价格在这些点附近表现出特定的波动模式。

价格波动效应：当股票价格略高于整数价格点时（如收盘价为X.1），次日股票价格更有可能上涨；而当股票价格略低于整数价格点时（如收盘价为X.9），次日股票价格更有可能下跌。这是由于整数价格点附近的限价订单对价格形成了支撑或压制。

策略：在收盘价略高于价格点时（如X.5），买入该股票并持有至次日，预期股票价格将会上涨。在收盘价略低于价格点时（如X.5），卖出该股票并持有至次日，预期股票价格将会下跌。

4、alpha提交截图

![图片](images/img_0b4ff481f2.png)

5、总结反思：

反思与总结：

1. 剔除极端的信号。
2. 剔除价格较大和较小的股票，价格较小的股票，本身的数值就很重要了，价格较大的股票，小数点后的数值没那么重要。
3. back_fill降低换手率。
4. 使用信号过去的标准差，增强信号，交易信号过去波动大的信号，波动大的信号更容易可能是更有效的信号。

---

