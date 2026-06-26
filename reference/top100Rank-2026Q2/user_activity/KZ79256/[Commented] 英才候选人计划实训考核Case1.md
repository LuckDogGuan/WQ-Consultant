# 英才候选人计划实训考核（Case1）

- **链接**: [Commented] 英才候选人计划实训考核Case1.md
- **作者**: WL13229
- **发布时间/热度**: 2年前, 得票: 3

## 帖子正文

**必做1: 阅读 [【Alpha灵感】论文/研报合集 – WorldQuant BRAIN](/hc/en-us/community/posts/19348865150743--Alpha%E7%81%B5%E6%84%9F-%E8%AE%BA%E6%96%87-%E7%A0%94%E6%8A%A5%E5%90%88%E9%9B%86) 或者  [Research Papers for Consultants – WorldQuant BRAIN，](/hc/en-us/community/topics/12997688420247-Research-Papers-for-Consultants) 选择一个你感兴趣的Alpha作为模板,并实现对该模板的1000次以上回测。例如**

```
 Ts_Rank(rank(x), 20)
```

参考路线图(您可以使用 **[BRAIN API可以实现的功能 – WorldQuant BRAIN](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD)** 进行路线图的实现）：

- Step1: 登录账号
- Step2: 思考合适的数据字段和参数。以该模板为例，可能基本面的model data也是不错的，但时间参数可能需要至少月度以上。如果是量价数据，可能需要更短的时间周期。
- Step3: 使用 [Data Explorer](https://platform.worldquantbrain.com/data)  手动尝试几个不同类型(category)的数据集，再次深入反思该模板提取的是什么层面的信息。
- Step4: 使用代码获取该类型的所有数据集和大部分数据字段（datafield)
- Step5: 对数据进行初步处理（例如vector data需要先使用vector operator降维）
- Step6: 将数据字段插入模板，批量生成Alpha表达式。
- Step7: 将Alpha表达式附上simulation setting （这一阶段可以使用比较常见的setting，无需过度调参）
- Step8: 将Alpha发送至服务器进行simulation。常见错误debug👉 [BRAIN API及日常回测时常见的报错 – WorldQuant BRAIN](/hc/en-us/community/posts/19446834004503-BRAIN-API%E5%8F%8A%E6%97%A5%E5%B8%B8%E5%9B%9E%E6%B5%8B%E6%97%B6%E5%B8%B8%E8%A7%81%E7%9A%84%E6%8A%A5%E9%94%99)
- Step9: 获取到所有Alpha的结果，每个Alpha至少获取到performance_comparison结果
- Step10:总结反思（代码效率、debug经历、模板适合的数据类型、模板的改进方向等）

**必做2:** 阅读👉 [量化研究推荐论文 – WorldQuant BRAIN](/hc/en-us/community/posts/21004691882135-%E9%87%8F%E5%8C%96%E7%A0%94%E7%A9%B6%E6%8E%A8%E8%8D%90%E8%AE%BA%E6%96%87) 中的任意一篇论文，或者自行寻找其他材料（如研报、论文），总结论文的核心思路和Alpha Idea **(注意不要和本帖子或论坛中已被发布的重复）** .

需提交的内容如下置顶评论所示：

---

## 讨论与评论 (138)

### 评论 #1 (作者: WL13229, 时间: 2年前)

**必做1：**

1.最近的截图（需包括时间） ![图片](images/img_a5c523f455.png)

2.下周二前的截图（需显示时间）

![图片](images/img_7c3791a14f.png)

3.截图显示你的code **连续不停（不可中断，代码需能handle各类报错）** 提交了1000个simulation。请自行考虑，如何print合适的信息，证明已经提交了1000个Alpha.这种技能会使得你的code更加易读，也能帮助你在代码运行时了解其状态。

4. 总结反思，需包含至少四个方面的反思：代码效率、debug经历、模板适合的数据类型、模板的改进方向。多写不限，字数不少于300字。

**必做2：**

**我阅读的文章是option13：**  [Testing for Asset Price Bubbles using Options Data](../CC40930/[Commented] Research Paper 72 Testing for Asset Price Bubbles using Options Data.md)

该文章使用看涨和看跌期权之间的定价差异来估计是否出现了资产泡沫。方法论上讲，价格泡沫的产生是因为买家通常购买资产不是为了永久持有并获取其永久现金流，而是为了在未来某个时候以更高的价格将其卖出。因此，泡沫的存在与投资者对资产价格未来演变的预期密切相关。因此，期权，由于其本身具有前瞻性特质，是估计和测试其标的资产泡沫存在的天然工具。进一步来看：

论文使用看跌期权数据来估计资产的基本价值，然后利用看涨期权的市场价格与基本价值之间的差异来估计泡沫。具体步骤如下：

- 我们首先选定一个灵活的参数模型（如G-SVJD模型）来描述资产价格的演变过程。
- 接下来，我们将看跌期权的数据输入进G-SVJD模型，对股票的实际价值进行估值，原因是该论文认为：使用看跌期权计算出来的股票估值是不含“泡沫”的。
- 最后，我们将看涨期权的数据输入进G-SVJD模型，作为对股票市场价值的估计。将看涨期权计算出来的估计值和看跌期权计算出来的估计值进行相减。这个差值越大，标的股票的泡沫越大。
- 使用统计学的方法，我们可以设定出“泡沫”的门槛。例如，当“泡沫”的值超过了标的资产价格的一定比例时，我们就认为该股票出现了明显的泡沫。

Alpha Idea：使用论文提示的方法，选取合适的模型计算并识别资产泡沫。在泡沫的初期可以跟随做动量策略，后期可以做反转策略。

---

### 评论 #2 (作者: YL93001, 时间: 2年前)

1、此时simulation数目为1078 ![图片](images/img_6a13cddc52.png)

2、此时simulation数目为2579

![图片](images/img_093712d43e.png)

3、每个线程10次simulation，连续跑完158个线程

![图片](images/img_2af04779e3.png)

4、在代码效率方面，生成所有选取的datafield之后对vector数据先进行统一处理再与matrix类型数据合并，从而实现统一插入alpha表达式，再利用ace代码的框架进行多线程回测，该多线程回测效率较高。

在debug方面，注意到若同时替换alpha表达式中的两个datafield，循环生成expression list时可能会产生两个同样的alpha表达式，后期合并result时若用alpha_id做索引要先去重；以及提取数据与回测时最好把setting的参数都写在里面，更容易查看数据是否统一。

模板本身分析的是一致预期相关的数据，均属于分析师数据大类，于是我们选取一些coverage大于0.5，alphaCount小于1000的analyst类型数据来获取里面的全部datafield，回测之后发现，还是模板原来使用的分析师数据效果最好。

模板可能还有以下的改进方向：对alpha进一步做中性化或先筛选出一部分股票，再进行该alpha的交易，设置一些交易条件。

---

### 评论 #3 (作者: YW93864, 时间: 2年前)

大家好，以下是我本周交付的内容。

1.

![图片](images/img_9b304b9d9e.png)

2. 实际上应该模拟了3000+，暂时不确定因为什么会丢失了剩余的1700个，已经设置了sleep防止访问次数过多，以及观察status_code看是否报错；可能需要将sleep时间设置更长

![图片](images/img_6f0e53825f.png)

![图片](images/img_1f46d8abb0.png)

3. 本周心得

本周，我主要做了工程上的工作，以及对我想用的因子模板进行了适当调整。本周的宗旨是Work first, better next.

工程上，我将一些函数打包成库，方便调用，例如登录函数、获取datasets和datafields以及将alpha表现转化为dataframe面板进行可视化，整体上还是比较高效、连贯的。登录函数、获取数据函数在上次Meet up的时候，就有现成的，无需重新造轮子；我主要开发了generate_alpha和get_result函数，generate_alpha是用来生成alpha表达式的，只要将simulation_data字典放入函数，输入对应参数即可；而get_result比较复杂，一方面数据结构比较复杂，字典里面嵌套了多层的字典，另一方面返回的绩效较多，而实际上筛选alpha时无需事无巨细地将每一个指标都罗列出来，当machine alpha跑到2000+，5000+，根本无法考察每一个alpha的每一个绩效。因此我需要对指标进行筛选，首先我会考虑统计出现fail的次数，这些测试是alpha提交的基本条件，我会先观察都pass或者只出现较少fail的alpha，这样在如果有可以提交的那么直接提交，如果有fail的可以再观察其他指标进行手动优化或优化模板，示例如下；接着，我更喜欢fitness较高的alpha，再是收益较高的alpha，其他常见指标再加入考虑，最后分别按sort_value函数对合成好的dataframe进行排序。

```
#pythoncheck['result'].values.to_list().count('FAIL')
```

除此之外，我还将alpha_id考虑进来，方便在必要时候手动查看alpha表现，最后的面板如下

![图片](images/img_9739d64a7a.png)

在工程上仍有需要改进的点：1）SLOW+FAST的参数代码不知道，缺少一个参数，尽管在CHN市场大概率是会使alpha表现变差的，但我仍然想尝试该参数，2）模板工程需要更加灵活，目前可能出现的问题是，当我1000次甚至更多次去simulate时，无法得知“是数据本身使模板从reversal变成了momentum，还是数据在该模板下无效”，如果是后者，那么目前的模板没有问题，但如果是前者，我需要在模拟1000次之后，将模板转换方向，重新测试部分的alpha；也许可以在使用构建表达式字符串时直接设置正负交替的alpha，但这样无法确定模板的属性是动量还是反转，这会导致alpha的可解释性变差；3）还需要进一步设计获取相关性corr接口，因为在目前返回的checks参数里，corr检测仍然是pending，需要额外的指令才可执行。

在模板选择方面，我使用了之前meet up介绍的模板，即“股票收益是球队还是硬币”，其中里面的第一个alpha“波动翻转”是个很好的模板，因为它主要是运算符，而并非像“换手反转”一样有换手率这样的数据去限定判断条件，相对来说第一个模板可玩性更高。

使用这个数据集，我目前觉得还是量价指标或技术指标更合适，因此我选用了model175数据集进行不断的simulation，这个数据我手动测试了一些，确实是有信号的。选用CHN市场，一方面是因为该模板已经在CHN市场取得了一些效果，另一方面是因为CHN独有的技术指标数据集非常丰富，如果深挖，很有可能出现相关性较低但同样有效果的alpha，还有就是方便完成第一周的任务（joke）。该模板原始设定是希望找到波动低于市场截面水平的股票，这些股票的确定性更高，而通常确定性高的股票可能因为过度关注出现超买，确定性较低类似，除了从收益角度去刻画这个现象以外，是否别的技术指标也能内蕴这样的关系？在逻辑上这看上去是说的通的。当我直接使用模板进行simulation时，会发现跑出来的结果一是不好，二是出现某些时刻平坦的曲线，说明该时刻不具备选股能力。

![图片](images/img_0cd9fcee10.png)

我做了适当调整，技术指标在量价数据上进行处理后得到的，相当于已经构造了一次类似returns的部分，如果再次去求技术指标的变化，很有可能丢失信息，因此我将原先计算returns的部分替换为数据本身，再simulate几个，发现略有好转

![图片](images/img_a9c506d264.png)

但发现仍然跟大盘走势接近，因此我再neutral掉beta。最后，确实出现了一根比较好看的净值曲线

![图片](images/img_f376637084.png)

尽管这个未达到入库标准，但该模板看上去要比之前好很多。

模板的改进思路：1）尽管已经“巧妙”地调整了一些运算符使alpha效果更好，但我观察了我自己的result_dataframe，发现只有若干个alpha效果好，而且其中大部分是在同一个datafield上调参调出来的，即该datafiled本身适用这个模板，而不是模板使用dataset，因此模板还需要更加精密地设计以便于使其能更适应整个dataset，在适应dataset之后，再去做进一步调参，优化alpha表现，可能才是有意义的

---

### 评论 #4 (作者: MM46273, 时间: 2年前)

想问一下，最近这周四门考试，下周三门考试，作业如果提交不上来怎么办？

---

### 评论 #5 (作者: YH69102, 时间: 2年前)

![图片](images/img_5eccb754be.png)

![图片](images/img_b452938cfd.png)

![图片](images/img_fcf9ac4067.png)

总结反思：

1.代码效率：

考虑到brain平台最大可同时进行10个simulation,将开始的循环改为了并行运算大幅减少了运行时间。

2.debug经历：

requests进行登陆操作时偶尔会遇到失败的情况，构建函数在遇到某些情况的时候重新登陆。

所有用户每4个小时or提交过多错误simulation会被强制登出。所以每完成一定量的simulation后重新登陆，避免这一问题。

**Expression cannot be empty**表达式不能为空，该问题是忘加最后的表达式引发的。

3.选用模版以及适用的数据类型

参考模版为【Alpha灵感】通过期权隐含价格与股票市场价格的差异寻找投资机会

rank(ts_rank(mdl169_backfill_cpl - close, 22))

其中mdl169_backfill_cpl为隐含价格 可以用get_datafields(s,universe='ILLIQUID_MINVOL1M',search='Technical and Fundamental ranking model')

中的数据代替 其中的close 可以用一些表示价格的数据带入 由于此alpha turnover过高 ts_rank的时间 在[21,42,63] 中选择

4.后续改进思路

发现可以通过把 mdl169_backfill_cpl - close 改为 mdl169_backfill_cpl / close 大幅减少turnover 代价是减少了sharpe

想到 【Alpha灵感】分析师建议和回报率 这篇文章中提到的思路 用分析师预测价格对return回归 ， 想到可以用隐含价格对 close回归后 考虑beta值的大小

然后也可以在其他universe里进行尝试 比如GLB,寻找低相关的因子。

---

### 评论 #6 (作者: WL13229, 时间: 2年前)

[MM46273](/hc/en-us/profiles/14030346587927-MM46273)

同学您好，如果之后无法提交作业，您可能会在某个阶段被移除，需要下一期重新申请。对于下一次重新申请的同学，不建议使用完全同样的申请材料，因为我们会有更高的期待，例如期待您完成本次的作业。

---

### 评论 #7 (作者: WL13229, 时间: 2年前)

[YH69102](/hc/en-us/profiles/18490343218711-YH69102)

同学您好，感谢细心地完成了实践。根据经验，即便用户在一定量的simulation后重登录，系统依然会在你最远的一次登录4小时后登出。因此，这个解决方案可能还不够完善。您可以等待Http错误出现后，再持续地重复登录，直至成功。

---

### 评论 #8 (作者: ZC80223, 时间: 2年前)

2023.12.14

![图片](images/img_89da5fb084.png)

2023.12.18

![图片](images/img_159126e64e.png)

关于确保提交不中断的机制：

1、表达式生成、simulation提交采用线程的方式

![图片](images/img_26ce3ebca2.png)

2、主函数内增加断线重连的函数

![图片](images/img_d9ed9a00fe.png)

3、在表达式生成和simulation的线程中增加监听

![图片](images/img_c2e05e5e6f.png) 4、控制台输出

![图片](images/img_62453537a1.png)

感想：

首先看到这个控制台输出，比较无奈，目前程序还有至少2个bug：

- 目标队列应该限制了1000个simulation，实际上依次程序跑完居然simulate 1700+个，进一步需要排查门限失效原因
- 整个simulation和表达式生成做完了，程序没有自动结束，所以没有打印结果，一直处于活跃状态，需要做进程释放程序刹停，目前不知道问题出在哪，得花时间改。

关于遇到的困难和解决办法：

1、发现生成表达式虽然快，但检索datafield比较花时间，所以做了个异步，一边检索，一边就开始喂入simulation了，解决表达式列表在异步状态的去重是比较低效的。

2、api的吞吐量得测，不然会出现大量的提交不进去，有点忘了课上是怎么判定alpha已经出结果了，目前用了201、429做了response判定，约定出现429不再提交，转而提交等待队列的几个429，直到全部消化完等待队列，再提交新的。

3、单次跑下来实在有点久，可测的机会其实不是很多，所以先提交一个满足作业要求的版本，后续继续看改进。

4、关于alpha结果提取相关的逻辑都没写，关于如果遇到vector型怎么办，也没测。后面再补吧

---

### 评论 #9 (作者: WL13229, 时间: 2年前)

[YH69102](/hc/en-us/profiles/18490343218711-YH69102)

感谢您的详尽回答。通过您的回复，我总结了如下几个您提出的问题，希望有帮助。

***“回测应该回测了3000多个实例，但由于某种原因，丢失了1700个实例。已经设置了一个sleep函数，以防止访问次数过多，并一直在监视status_code以查找错误。但依然出现此问题，如何解决？”***

答：simulation_response.status_code为201并不代表你的Alpha运行没有问题，运行有问题的Alpha就是会被丢失的。您可以运行一下下列代码，体会一下错误的来源：

```
simulation_data = {    'type': 'REGULAR',    'settings': {        'instrumentType': 'EQUITY',        'region': 'USA',        'universe': 'TOP3000',        'delay': 1,        'decay': 15,        'neutralization': 'SUBINDUSTRY',        'truncation': 0.08,        'pasteurization': 'ON',        'unitHandling': 'VERIFY',        'nanHandling': 'OFF',        'language': 'FASTEXPR',        'visualization': False,    },    'regular': 'high-close+dfd'}simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=simulation_data)print(simulation_response.status_code)print(s.get(simulation_response.headers['Location']).json())print(f'status: {s.get(simulation_response.headers["Location"]).json()["status"]}')
```

***"在处理 `get_result` 函数时遇到了困难，因为它的复杂性。数据结构复杂，有许多嵌套的字典，并且返回了许多性能指标。在选择指标和对dataframe排序时遇到了麻烦"***

答：嵌套的字典不应该成为一个很大的问题，可以思考如何存储字典类数据。或者摘取重要的指标，如Sharpe, Fitness等先进行存储。对于返回的嵌套的字典，你需要仔细阅读它能提供的信息，做到心中有一个基本的印象，这对以后研究和绩效分析将会有帮助。

***“遇到了一个问题，不确定是数据本身在模拟过程中使模板从反转变为动量，还是数据在模板下无效。这使得确定模板的属性变得困难。”***

答：模板本身如果是动量，那么就应该是动量。如果在替换数据字段的过程中，performance发生了反转，然后你再加一个负号上去，那么说明你已经偏离了模板本身，有走向overfitting的危险。

***“不确定SLOW+FAST参数的代码，并且缺少一个参数。”***

答：SLOW_AND_FAST

***"需要进一步设计获取相关性（corr）的接口，因为当前的corr检查仍然处于待处理状态，需要额外的指令才能执行。"***

答：检查相关性的API的使用方式已经在这个帖子提出👉 [BRAIN API可以实现的功能 – WorldQuant BRAIN](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD) ，欢迎参考。

***”当使用模板进行模拟时，结果不好，有些时间点显示出平坦的曲线，表明该模型在那些时间没有股票选择能力。“***

答：请手动找到这个Alpha进行查看。在网页浏览器输入“ [https://platform.worldquantbrain.com/alpha/AlphaID”,即可以看到它的表现。一般这种Alpha的出现是因为使用Alpha前的数据处理工作还不够好。这个我们会在未来的课程中提到，并给出一些指导建议。](https://platform.worldquantbrain.com/alpha/AlphaID%E2%80%9D,%E5%8D%B3%E5%8F%AF%E4%BB%A5%E7%9C%8B%E5%88%B0%E5%AE%83%E7%9A%84%E8%A1%A8%E7%8E%B0%E3%80%82%E4%B8%80%E8%88%AC%E8%BF%99%E7%A7%8DAlpha%E7%9A%84%E5%87%BA%E7%8E%B0%E6%98%AF%E5%9B%A0%E4%B8%BA%E4%BD%BF%E7%94%A8Alpha%E5%89%8D%E7%9A%84%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E5%B7%A5%E4%BD%9C%E8%BF%98%E4%B8%8D%E5%A4%9F%E5%A5%BD%E3%80%82%E8%BF%99%E4%B8%AA%E6%88%91%E4%BB%AC%E4%BC%9A%E5%9C%A8%E6%9C%AA%E6%9D%A5%E7%9A%84%E8%AF%BE%E7%A8%8B%E4%B8%AD%E6%8F%90%E5%88%B0%EF%BC%8C%E5%B9%B6%E7%BB%99%E5%87%BA%E4%B8%80%E4%BA%9B%E6%8C%87%E5%AF%BC%E5%BB%BA%E8%AE%AE%E3%80%82)

***”在做出调整和中和beta后，净值曲线也接近市场趋势。“***

答：这个观察不错，说明您已经开始思考，如何提升template。

---

### 评论 #10 (作者: WL13229, 时间: 2年前)

[ZC80223](/hc/en-us/profiles/16412175793303-ZC80223)

同学您好，

simulation_response.status_code为201并不代表你的Alpha运行没有问题，运行有问题的Alpha就是会被丢失的。status_code为201仅代表着，目前并不处于too many simulation的状态。查看alpha是否在正常simulate，您需要查看s.get(simulation_response.headers['Location']).json()这个代码中的‘status’字段

---

### 评论 #11 (作者: WL13229, 时间: 2年前)

[YL93001](/hc/en-us/profiles/18134743066519-YL93001)

谢谢您完成此次case。注意到您的代码还普遍使用ACE比赛提供的代码，个人建议您使用 [BRAIN API可以实现的功能 – WorldQuant BRAIN](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD)  API的原生功能重写。否则到后面内容越来越多时，您可能难以修改源代码。

---

### 评论 #12 (作者: JL23162, 时间: 2年前)

1与2的任务

![图片](images/img_3faa023b33.png)

![图片](images/img_b7f5f8ce60.png)

3.运行代码截图

![图片](images/img_9b83480818.png)  ![图片](images/img_cd8faeb95a.png)

4.总结反思：
当前代码效率应该是达到服务器上限的了 由于上限是10个 提交10个的同时检测是否在10个中回测完毕的 再继续添加 使得总回测队列始终保持10个
debug上 当前代码会因为网络问题断开链接 导致后续回测不了 我昨晚跑的 早上起来看只测了700个 剩下300个是今天早上补的

当前模板数据类型支持martix和vector 我的vector处理直接加入了vec avg，其他的如group数据就会直接drop掉
当前的改进方向应该是如何继续拓展迭代 使得其能够自动跑，并且检验提交，还有自动重启（不论是网络问题 还是长时间 login in的问题）当前只能指定数据字段 按照指定单个模板回测 ，还应该加入多个模板 ，以及判断通过条件数量 按照某一方向继续修改的功能

---

### 评论 #13 (作者: WL13229, 时间: 2年前)

[JL23162](/hc/en-us/profiles/18456131969431-JL23162)

很高兴看到您的代码至少已经实现了断点查找的功能，即您可以清楚地知道代码是从哪个Alpha断开的，然后继续重联。至于如何解决断线（断点）问题，您可以参考该链接👉 [BRAIN API可以实现的功能 – WorldQuant BRAIN](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD) 的更新内容之《 **一种解决超时登出的解决方案》**

---

### 评论 #14 (作者: EH13432, 时间: 2年前)

**任务提交：**

![图片](images/img_7f5c1ee439.jpeg)  ![图片](images/img_f26d9a4a4a.jpeg)

出现链接错误，自动重连

**![图片](images/img_7c7fd61310.png)**

单独实施1000次回测可以成功提交977次simulation

![图片](images/img_e8ace02c4b.png)

**想法记录**

本周的任务主要还是在搭建上，我构造了一些函数，如多重模拟函数——给每个可调整参数传递一个列表或值，函数可以自动组合构建alpha进行回测。最终返回alpha的id列表，以及输入id列表，可以生产is和performance corr的dataframe等等。

![图片](images/img_e07113b021.png)

![图片](images/img_8c5e72705a.png)

**关于登出情况的调整：**

我一开始只是简单的构造try except函数，在出现http error时候重新登陆，但后来发现登出时候的报错更为复杂，又增加了一些except再重新登陆的条件。目前运行4小时以上不会报错了，但自己也没搞明白自己的代码逻辑到底对不对。或许还是应该从状态码是否等于201来判断

**关于模版选取**

模版上，选用了新闻动量篇的思路，因为我觉得该篇在思路上本质就是情绪和交易量对回报率的回归，模版比较有行为金融学意义，且比较可以复制，故对情绪相关数据进行了一下简单的处理就代入进去了。事实上，大部分的sentiment都可以获得一个比较理想的alpha

![图片](images/img_977bbdb01c.png)

**改进**

开始时候我没有写明白同时提交10个alpha的函数逻辑，导致生成速度很慢，一测测一天，且电脑一出现问题就容易前功尽弃。一开始想的是，打包10个alpha进一个组，再用多重模拟进行回测，现在改用多线程来处理，大大加快了测试速度。

**问题**

目前我的代码在运行1000次成功回测的时间大概是2个小时到2个半小时之间，这是一个正常的速度吗？还是可以再进行优化？

我生成dataframe的函数在alpha id列表一长就很容易报错，同样的输入有时候可以成功，有时候会报json decode error，不明白是为什么。本人没有经过系统学习过代码，不是很明白，恳请大家帮我看看。并且有什么改进的办法吗？

![图片](images/img_bfec6c898c.png)

---

### 评论 #15 (作者: WL13229, 时间: 2年前)

[EH13432](/hc/en-us/profiles/13837178860951-EH13432)

非常完整的作业，令人感动。

***"目前我的代码在运行1000次成功回测的时间大概是2个小时到2个半小时之间，这是一个正常的速度吗？"***

答：速度是正常的。看到您也获得了一个新可提交的Alpha,从效率上看，大约1000次simulation获得一个Alpha也是正常的效率，这个说明您的模板选择和数据选择都比较合适。另外一个检测自己速度是否合适的方法就是，回到网页界面，尝试手动simulate一下Alpha,如果会报错“too many simulation at a time”，这就说明代码正在全力工作，占用完了十个线程，算是高效了。

***“我生成dataframe的函数在alpha id列表一长就很容易报错，同样的输入有时候可以成功，有时候会报json decode error”***

答：初步猜想，这个的原因是因为你尝试解析一些提交失败或者没有获得simulation结果的Alpha导致的。我建议你使用try方法，确定json可以解析后再放入dataframe.或者，你可以创建一个csv文件，在确定json可解析后，把json结果append到csv文件的最新一行。

---

### 评论 #16 (作者: BX78946, 时间: 2年前)

首先是上周的截图 ![图片](images/img_0303c5a7c2.png)

然后是今天的截图

![图片](images/img_aee777fe1a.png)

最后附上连续提交1000个alpha的输出：

![图片](images/img_6ed5e09cc7.png)

代码方面主要是用了这个链接里的代码 [https://support.worldquantbrain.com/hc/en-us/community/posts/19831456877463-BRAIN-API可以实现的功能](https://support.worldquantbrain.com/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD)  以及之前mee tup的内容，然后根据老师上课的建议内容，可以将输出的alpha的结果保存到一个csv文件中，方便进一步操作。

![图片](images/img_06b870182d.png)

同时我也保存了整个performance_comparison的结果进一个csv文件。虽然都没有进行进一步的操作，主要是尝试一下。然后我总是在第一次登录的时候会遇到提示"connection down, trying to login again”，这个过程有时候持续很久才会显示Response [201]登陆成功，不知道是为啥，虽然每次最后都登录进去了。

Debug经历主要还是感谢gpt等大模型工具，可以通过他们实现很多想法。

我的模版是参考的 [https://support.worldquantbrain.com/hc/en-us/community/posts/19507603510039--Alpha灵感-偏斜性偏好和市场异象](https://support.worldquantbrain.com/hc/en-us/community/posts/19507603510039--Alpha%E7%81%B5%E6%84%9F-%E5%81%8F%E6%96%9C%E6%80%A7%E5%81%8F%E5%A5%BD%E5%92%8C%E5%B8%82%E5%9C%BA%E5%BC%82%E8%B1%A1)  这篇文章，通过这位consultant 的想法首先构造出来

```
-rank(vec_avg(oth41_s_tech_skewness))*rank(mdl175_revs10)
```

这个alpha，然后在这个基础上加上对市值进行中心化处理，其实就已经得到了一个可以通过除了prod_corr以外所有测试的alpha了。然后对于oth41_s_tech_skewness和mdl175_revs10，我通过搜索他们的dataset，并且分别搜索了“skewness”和“return”这两个关键词，用api筛选了很多datafields，然后用这些datafields遍历组合，最后可以得到很多通过测试的alpha，但是都没有通过prod_corr相关性的检测。

后续的改进：可能是由于我筛选用了关键词搜索以后，能通过测试的alpha之间相关性都很高，所以没有办法通过prod_corr的测试。我感觉从我自身的经历来讲，想得到一个表现还可以的alpha其实没有那么难，难的是怎么能够通过所有的相关性的检验，还是需要多想多看，得到一些新的idea才可以。有可能通过暴力调参能够让检验都通过，但感觉对自身的提升也没什么帮助，希望能通过这个课程有更多的提升。

---

### 评论 #17 (作者: WL13229, 时间: 2年前)

[BX78946](/hc/en-us/profiles/16297370627607-BX78946)

您的思考非常深入。没有通过production测试的原因，主要是因为核心在于使用了下列这个为主信号的Alpha

```
rank(mdl175_revs10)
```

确实如您所说，后续您的筛选方式，大多获得的是同样的idea。其实解决此类问题，我们需要思考一下，这个template的本质是什么？当你使用两个rank相乘时，其实它的本质就变成了两个排序的交叉验证（注意，与加号不同）。且这里前面有个负号，说明这个模板在捕捉的信息是：“如果一个股票同时满足A和B，我就做空”。
因此，该模板其实泛化能力还是比较强的，只专注于return和skewness就会造成correlation高的问题。

但是需要注意的是，一昧的泛化和尝试不同数据集，或“暴力调参”，可能会使得过拟合。因此，我们在寻找A和B时，最好保证它们是在相同维度，或者是同类数据集里的。

最后多说一句，这种泛化能力强的模板，往往效率不高，尤其在面对coverage不高的数据集时，效率会大打折扣。

---

### 评论 #18 (作者: YT14523, 时间: 2年前)

1、 ![图片](images/img_470ab0ab77.png)

2、 ![图片](images/img_18d6a4c61a.png)

3、 ![图片](images/img_74e2774c50.png)

3、反思：

整个代码在原来的基础上，在simulation的循环中加入了每simulate成功除了输出successfully，再加上是第几次simulation，整体上是能成功模拟1000次以上的，但是只是将所有的dataframe呈现出来并挑选的拥有超过1000个数据字段的dataset来模拟。并且使用的数据集是A股基本面数据，从1000次simulation的结果来看这个数据并不是很适用，sharpe，return及其他指标表现都不好且不会有很大的变化，从使用的alpha表达式上看应选择与价格和成交量相关性高的数据，尝试其他数据集的效果都不是很好，因此想尝试让代码遍历所有dataset，将每一个dataset都进行模拟来寻找一个合适的数据集并进行不间断地不同数据集的模拟，但模拟需要很长时间。

![图片](images/img_b1fea2a930.png)

并且在模拟到一半的时候出现了几种报错，表达式没有问题，也并没有超时登录

![图片](images/img_918de2379f.png)

效率问题上只进行换数据集的模拟还是很慢的，思考改进方法：如果要找到合适的数据并能减少不必要的模拟来提高效率，可能可以加入对alpha performance 的判断，遍历所有的dataset，如果simulate一定数量后alpha表现并不好且sharpe或return变化很小甚至为负值时，就换下一个dataset进行模拟，如果模拟的前几个表现有提升的迹象，那么就继续使用这个dataset里的数据字段。

---

### 评论 #19 (作者: YW54232, 时间: 2年前)

![图片](images/img_deef5a6af1.png)

![图片](images/img_5e147d8efc.png)

模拟了约2500个alpha

![图片](images/img_1ffa00815c.png) 可以通过直接count output里的语句得到simulation的数量。

![图片](images/img_5c6ea5c666.png)

使用多线程来模拟，可以调整线程数量。

![图片](images/img_1b0d534c3e.png)

能够保存模拟结果较优的alpha到json文件，进行进一步的研究和提交。

想法：

在之前的测试中，用8线程模拟2500个因子后，网络会有中断的风险，所以用2小时模拟2500因子作为一个批次是我现在的选择。

之前已经参加过线下见面会，回去之后进行了自我探索，所以可见已经进行了10k+的因子模拟，甚至于把整个datafields都跑了一遍。之前的模拟中发现了一些不能用原有模板解释，但是依然有较好效力，甚至corr并不高的因子，可以作为未来研究和进一步探索的基础。但同时也要意识到仅仅通过“遍历”去搜索因子的效率并不高，目前也只有5个左右达到提交要求并corr不高的因子。模板的选择，因子库的构建和批量回测是可以并行进行的事情。而Generation Algorithm更多是提供一个新的视角或者帮助你找到隐藏的关系，而不能指望其中的独创性。

---

### 评论 #20 (作者: WL13229, 时间: 2年前)

@ [YT14523](/hc/en-us/profiles/17370777323031-YT14523)

这个报错似乎还是session被退出的问题。尝试handle并重连，应该可以解决问题

---

### 评论 #21 (作者: WL13229, 时间: 2年前)

[YW54232](/hc/en-us/profiles/13837011976855-YW54232)

网络中断可以进行重连，我们会在下次课介绍一个可行的办法。

关于您对Alpha的思考，是正确的。这正是我们作为Human需要不断给代码赋能的地方。寻找到合适的template，是human research很重要的一部分。

---

### 评论 #22 (作者: HW97336, 时间: 2年前)

**任务提交**

![图片](images/img_87ab2e4c38.png)

![图片](images/img_4f44f50e27.png)

![图片](images/img_05dc0c9f24.png)

![图片](images/img_7e811ad639.png)

**主要函数：**

实现对simulation_data_list里的所有simulation_data同时simulate，得到alpha_id_list和alpha_list

![图片](images/img_3a423414a9.png)

获取performance comparison和summary信息，解决登出问题

![图片](images/img_b8afe5484f.png)

最终的函数，将所有datafield套入表达式，按照10个一组simulate，得到all_alpha_id_list、all_alpha_list、all_pc_list、all_summary_df

![图片](images/img_3d2fae2ba1.png)

**代码效率**

Simulate 1200个Alpha，其中每次都是同时simulate 10 个Alpha，总用时2小时31分钟，不过我将获取performance comparison和summary的数据也写在了函数中，所以使得实际运行时间偏大。如果只simulate，不实时记录数据，而是在全部simulate结束后，从列表获取这些Alpha，再依次统计数据，可能用时会更短。

**debug经历**

- 登录失败：后来发现是因为自己之前用谷歌浏览器挂了VPN，关掉就好了。
- simulation_response.headers['Location']报错：应该是如果表达式出现问题，post后simulation_response.headers里没有’Location’这一指标，因此加入if else条件语句，如果’Location’在simulation_response.headers中，就正常运行代码，如果不在就跳过该表达式，这样就可以避免个别表达式错误导致代码中断。
- 在循环中直接采用simulation_data[’regular’]=new_expression的方式生成新的simulation_data，然后走正常流程，把得到的alpha_id添加进列表，结果发现运行完后list里全是最后一个Alpha，这个问题困扰了我很久，分步print都觉得没问题，后来采用另设一个变量，不直接替换原来的，问题得到解决。
- 解决登出问题：使用try except语句，把要实际运行的代码封装成函数，try这个函数，如果登出了必然会报错，那么运行except，重新sign in()直至response为201，然后再运行上述函数，保证代码不中断。

**模板选择**

模板为：

f"ehat=ts_regression(returns,{datafields_list[n*epoch+j]},120);group_zscore(ts_zscore(-ehat,60),subindustry)"

其中datafields_list[n*epoch+j]就是我们要填入的数据，自己提前在datafields_list中存储了1200种数据，n=10表示10个Alpha为一组，epoch则表示已经simulate多少组，j是每组中的索引

数据类型使用了News、Sentment以及Social Media的数据，通过搜索先得到category，再得到数据集的id，对于Vector都采用vec_sum的方式处理，Matrix则不处理

因为之前对新闻动量有过思考，这次想要在所有相关数据上都试一试，模板主要的意思是计算当前returns的偏离，将这个偏差在时间维度上zscore，然后再在行业维度上zscore，可以得到一个信息比较丰富的指标，根据它来决定多空仓位大小

在结果中看到的确有1个能提交的Alpha，但表现只能说刚刚及格，而且提交后会较低我的performance

![图片](images/img_ac483b2827.png)

![图片](images/img_c021d6fd44.png)

模板的改进方向：直接采用decay=20的方式虽然大幅降低了换手率，但会让其他指标也变差许多，以及对于这种反转策略如果用ts_mean这样的手段很容易降低表现，未来的改进方向可能有：1、加入合适的“进入条件”，这对于降低换手率应该是最重要的；2、可以对多个变量回归；3、将该变量与其他变量正交化，剔除其他变量的影响；4、对数据本身处理，比如可以替换为变化率等等；5、和其他alpha结合，强化表现

---

### 评论 #23 (作者: WL13229, 时间: 2年前)

[HW97336](/hc/en-us/profiles/18134895192087-HW97336)

一个非常完善的流程。同样的，这个是一个比较容易泛化的Alpha。它考量了A和B的残差。其实，returns也是可以换的。换掉returns后，在同个数据集进行操作，也会获得有趣的信息。

---

### 评论 #24 (作者: ZL89083, 时间: 2年前)

![图片](images/img_367c4987ec.png)

![图片](images/img_ac26c3d138.png)

我用tqdm库显示回测进度

![图片](images/img_f3a04eea30.png)

我没有遇到太多bug,由于最近考试多，我就测试了一个比较简单，回测快的表达式：rank(ts_mean(alpha,20)),

然后数据选取的话，主要还是选取能与表达式结合表达一定因子逻辑的数据集，我主要选取了几个fundamental的数据集，有几个因子表现还不错，但我没有截图。

我是将alpha表现的json表达式提取出来放到一个df里面 ![图片](images/img_afeab6e8ff.png)

---

### 评论 #25 (作者: FP65798, 时间: 2年前)

一.simulation增加情况
 ![图片](images/img_e3a7d6ba56.png) 
二.code运行情况(连续不停1000个simulation)
 ![图片](images/img_cba5851ef9.png) 
三.总结反思

1. 代码效率：
   根据之前的运行经验发现，每次提交500个simulation报错的几率比较小，因为一次跑得过多容易出现“connection aborted”的情况。目前我的策略是将要跑的数据按500个一份分组，若无报错，则跑完一份后立刻提交下一份；若中途报错，就获取错误信息显示出来，接着等30分钟（因为我发现程序这边报错平台那边似乎不会立刻刹车，马上重新提交的话会导致“simulation_limit_exceeded”，所以需要等待一段时间），再重新跑一下s = ace.start_session()，再重新提交这一份的500个数据从头跑。从上面第二部分code运行情况的截图来看，这样还是比较顺畅的，每个线程也是顶满10个simulation。在此方式以及模板（见下第3小节）下，对CHN TOP3000的1051个数据，无报错跑完的时间为33.6分钟。
2. debug经历：
   在跑下面这段代码想查看simulation返回的结果时，会遇到以下报错。原因是结果里有重复项。
   目前想到的办法是在result后面加[0:100]这样的区间避开重复项。不知有没更好的办法？
   ![图片](images/img_2bc4092402.png)
3. 模板适合的数据类型：
   参考模板为 [【Alpha灵感】通过期权隐含价格与股票市场价格的差异寻找投资机会](/hc/en-us/community/posts/19140570265367--Alpha%E7%81%B5%E6%84%9F-%E9%80%9A%E8%BF%87%E6%9C%9F%E6%9D%83%E9%9A%90%E5%90%AB%E4%BB%B7%E6%A0%BC%E4%B8%8E%E8%82%A1%E7%A5%A8%E5%B8%82%E5%9C%BA%E4%BB%B7%E6%A0%BC%E7%9A%84%E5%B7%AE%E5%BC%82%E5%AF%BB%E6%89%BE%E6%8A%95%E8%B5%84%E6%9C%BA%E4%BC%9A)
   ```
   ts_backfill(group_rank(ts_rank({x}-close, 60), industry), 20)
   ```
   适合的数据类型: 价格数据（期权隐含股价，加权股价，机器学习预测股价等）
   直接通过search price获得数据
   ```
   datafields_df=hf.get_datafields(s, region='EUR', universe='ILLIQUID_MINVOL1M', delay=1, search='price')
   ```
4. 模板的改进方向：
   此模板在CHN TOP3000看起来有以下不错的表现
   ![图片](images/img_d1942efcd2.png)  ![图片](images/img_01664d495e.png)
   但由于IS ladder Sharpe Fail以及部分turnover比较高使得其无法通过。
   见下图IS ladder Sharpe Fail可能是因为18年后alpha失效了？暂不知有什么改进办法。 ![图片](images/img_34c39e79f4.png) Turnover比较高的改进思路：利用Trade_when设置合适的进场时机，具体是什么条件还需要研究；
   根据运行经验，选择合适的group_neutralize可以对alpha有比较大的提升（可能可以有效降低回撤），可以利用机器再跑下最优group_neutralize。
5. 代码改进方向
   改成断点续跑，而不是现在的报错则从每份数据组的开头重新跑。

---

### 评论 #26 (作者: WL13229, 时间: 2年前)

[ZL89083](/hc/en-us/profiles/13837026594199-ZL89083)

已经算是比较成型的作品了，虽不是最经验，但重在代码bug少

---

### 评论 #27 (作者: WL13229, 时间: 2年前)

[FP65798](/hc/en-us/profiles/17259858019735-FP65798)

非常impressive的回测次数。关于您提到的“改成断点续跑，而不是现在的报错则从每份数据组的开头重新跑。”，这个也是我非常建议的方向。可以看出您已经有相对成熟的框架，我建议将ACE代码重写，这样您可以更加清晰地进行debug，包括show result的部分。

---

### 评论 #28 (作者: WX16829, 时间: 2年前)

**作业提交**

1.程序运行前后截图

![图片](images/img_fb3de5e3a8.jpeg)

2.本次通过程序一共运行提交了1137个因子。研究发现每个因子运行完成后json中Date Modified字段可显示因子的运行时间。运行完成后，将此字段及主要的结果输出至CSV文件保存，运行用时一共约1小时15分钟。

![图片](images/img_d0277b0be5.jpeg)

3.总结反思：

（1）代码效率方面，主要使用了上节课提供的模板，先将因子全部提交至平台运行，完成后再获取结果。由于平台上并行线程的限制，当发现无法提交时等待一段时间重试，总体上效率比较高。

![图片](images/img_4c5a0a90f7.png)

（2）Debug方面，主要考虑初步建立一个简单的dataset探索的框架程序，使用rank(ts_rank({datafield},20))作为模板对dataset other432进行探索，simulation过程中使用的函数主要都是上节课提供的函数。为了后续研究和改进的方便，将数据整理数据输出至csv文件，同时每个因子包含时间标签以方便检查是否为当前程序所测试的因子。

（3）改进方向：主要有两方面：一是程序的容错性和断点续跑需要完善。在测试过程中发现先一次提交全部因子再获取结果的方法有少量因子（1-2个）提交成功，但最后获取结果时发现丢失了。因无法在提交后第一时间获得因子的alpha id,完成后手工检查比较费力，后续考虑程序中能够自动检查和重跑。（2）调参的自动化程度需要提升。目前该模板仅能支持对一个简单因子模板（包含一个可变datafield）的探索，另外setting下的decay、neutralization等设置仍然需要手动调整，这些手动调参的重复性工作后续可以考虑通过程序实现。

---

### 评论 #29 (作者: YJ78324, 时间: 2年前)

一、本次任务前后的Alpha数量截图

本次任务在代码测试和运行后提交了约2000多个Alpha

![图片](images/img_958a34dd95.png)

![图片](images/img_6ea5f5d091.png)

二、代码连续运行情况

代码针对给定数据集共生成了1252个Alpha，这1252个Alpha使用多线程在大约在1小时内提交完成

![图片](images/img_019b252867.png)

![图片](images/img_c4e5dd4ee0.png)

三、总结反思

3.1 代码效率

我将整体的代码分解为三个功能模块，方便后续功能的扩展：（1）WorldQuantClient：用于处理网络请求，如：登录、提交Alpha、查询Alpha等功能；（2）AlphaExpressionGenerator：根据指定的模板与规则生成Alpha表达式，其中也包括了对于Vector类型数据的处理；（3）TaskManager：通过调用前两个模块完成任务的批量提交和结果的记录

批量提交方面为了提升代码的运行效率，我这里采用了ThreadPoolExecutor线程池对于生成的Alpha表达式进行并发提交，最大线程数为WorldQuant的最大模拟次数10。在提交任务后对于所有成功的Alpha集体做一次查询，并保存结果。

3.2 调试经历

整体开发过程中遇到最多的问题还是网络请求中出现 connection aborted。针对这一情况，我对网络请求做了进一步的封装，设置重试次数与间隔时间，每次请求失败后都会重新登陆，再次尝试网络请求。

3.3 Alpha回测

本次选择的测试模板如下：

`rank(group_neutralize(x - last_diff_value(x, 5), bucket(rank(cap), range="0.1, 1, 0.1")))`

根据基本面数据的差异，按照市值进行分组中性化并进行排名，测试范围为CHN TOP3000，用于生成表达式的Data Fields来自 A-shares Fundamental Data 数据集中的1252个字段。其中针对Vector数据都采用了vec_avg方法进行聚合。

整体测试结果如图：

![图片](images/img_6337dc532a.png)

这里选择其中比较高Sharpe的Alpha表达式查看了结果

![图片](images/img_75e54f125d.png)

![图片](images/img_6d6c0b0136.png)

![图片](images/img_d919043ed3.png) 可以看到，这几个Alpha在2020年后都出现了失效的情况，具体原因与优化方向还需要进一步分析。

3.4 改进方向

- 代码方面实现配置化，讲一些可变的参数放入YAML文件中，进一步提升自动化效率；
- 添加结果分析模块，可以针对pnl信息做进一步分析处理；
- 参考论坛中的他人经验，尝试构建Alpha模板库

---

### 评论 #30 (作者: WL13229, 时间: 2年前)

@ [WX16829](/hc/en-us/profiles/8702256081943-WX16829)

代码效率挺好的，这也是推荐的做法。至于您遇到的问题“在测试过程中发现先一次提交全部因子再获取结果的方法有少量因子（1-2个）提交成功，但最后获取结果时发现丢失了。”，您可以在获取到

```
s.get(simulation_response.headers["Location"]).json()["status"].upper() != 'ERROR'
```

之后，再提交下一个。基本到这里，你就已经能获得ID了。
关于模板的自由度提升问题，我们会在接下来的内容覆盖。

---

### 评论 #31 (作者: WL13229, 时间: 2年前)

[YJ78324](/hc/en-us/profiles/12940496308759-YJ78324)

很好的反思，这也是未来我们授课中想不断给大家提升的方向。

一些comment：

```
 last_diff_value(x, 5)
```

1. 如果是用在基本面数据集，上述的参数时间可以从5换到20、60等更长时间，因为基本面数据变动频率低。

2. 关于Alpha信号失效，尝试换个市场做一下

---

### 评论 #32 (作者: OA92025, 时间: 2年前)

1. 此时是12/18/2023 的 15:44，total alphas == 1658.

![图片](images/img_68e79f255b.png)

1. 实现过程：

其实，实质就是通过爬虫实现对brain平台数据的爬取。并且通过python在brain平台上实现simulation。

- Simulate并获取单个alpha的表现，实现断线重连。

F12获取网页代码，找到请求头headers，以及json查询参数（在payload中）

![图片](images/img_ea044c5d82.png)

![图片](images/img_646078e9d7.png)

这些是我们需要的参数。复制粘贴到本地python代码中，稍作修改，就可以实现多个alpha的爬取。

- 获取在IS中的alpha_list列表(unsubmitted)

查看list的详情，list中是1627个alpha的dictionary，包含alpha的id、regular（表达式）、setting详情、表现等数据。

![图片](images/img_e65c2de93c.png)

![图片](images/img_463d53dcba.png)

可是太慢了，现在还没有跑完，ddl快到了，就先交了，之后再补上结果。。。

![图片](images/img_536c4c6a3e.png)

3.问题反思：一直没有弄明白，为什么我能够获取alpha列表、simulate每个alpha、获取每个alpha的表现，但是却没有真正simulate成功？也就是我的alpha提交次数还是不变，没有增加？

---

### 评论 #33 (作者: FL11741, 时间: 2年前)

![图片](images/img_28d9caa66b.png)

![图片](images/img_01582f8414.png)

因为我自己没什么基础，本着一步一个脚印的精神，这次Case1我主要把重心放在程序框架的构建上，大概有了一个整体的思路，一些细节可以之后再作补充和调整。

模版方面选择了最简单的rank(ts_backfill(x,20))，主要起到试跑程序的作用。

程序方面我主要分为三个方面：效率、功能、稳定性。首先讨论效率。效率方面在我们没有做类似于大数据量的相关性实验这些的前提下，很明显时间成本主要都在brain平台的simulation功能上，因此在效率设计方面核心应当是让平台simulation尽量保持满载状态。因此这里选择队列+多线程，alpha list进alpha id出，效果类似下载器，保持10个simulate满载。(截图选用的GLB的数据，实测跑的比CHN慢了3倍多）

![图片](images/img_44ee1de5d7.png)

![图片](images/img_53cae7d978.png)

功能上，由于simulation和后续result研究的分离，并且get函数获取结果数据不会影响simulation进行（我猜），我们有充裕的时间在simulate过程中用alpha id再去获取数据以及做一些基本的处理。因此这一方面灵活度是比较高的。例如我这里做了几个定时刷新的表格，上面的截图提示simulate进度，下面的提示最近完成得到的结果，以及按照fitness排序得到实时排名最高的5个alpha。（忘记截图了，跑了一点点别的作示例）

![图片](images/img_d195774777.png)

稳定性上，要保持程序稳定运行下去，需要程序很强的处理异常能力。这里我还没有做深入研究，暂时简单将所有异常一并等待，重试，跳过处理。

目前遇到的两个主要问题和对未来改进方向的想法：一个是对异常的处理比较粗糙，网页端的错误信息（simulation_limit_exceeded）目前没有拉起异常，不能打断线程进行。另一个问题就是multi-simulation的上限问题，我在文档中没有找到明确说明multi个数*child个数的上限，自己手动试测了一下，结果simulate权限被屏蔽了近两个小时:-) ，因此我目前暂时用的是跑满10个single simulation的方法。如果能确切知道multi上限，可能可以大幅度提升效率。在程序上还有一个比较重要的功能可以添加，就是像下载器那样不但可以满载运行，还可以在程序运行时实时调整队列顺序，比如将临时想测的alpha插入队列最前端等等。其他功能方面主要还是服务于ideas，暂时没有必要过多深入。

---

### 评论 #34 (作者: ZZ51944, 时间: 2年前)

### 数量截图

![图片](images/img_2287c98464.png)

（今天没跑完，明早跑完了补充一个结果）

![图片](images/img_f53f11df93.png)

一次性实现截图：

（今天没跑完，明天跑完了补充一个结果）

### ![图片](images/img_0b0771eb2d.png)

### 

### 总结：

- 代码效率：

1. 最大化模拟，10个同时模拟
2. 常规操作：使用并行计算、向量化操作和优化算法来提高代码的执行效率。
3. 但是，好的思路比暴力算法更有用

- Debug经历：

1. 查文档
2. 虽然有ACE框架，但是自己重写函数熟悉度更高，也不容易出bug，同时还可以更完全高效的表达思想
3. 可以用GPT-4 + Brain文档协助Debug和编写函数
4. ```
   报错RemoteDisconnected：网络原因导致的报错，有可能是因为刷新了Brain页面，还有可能因为VPN不稳定
   ```

- 模板适合的数据类型：

```
ts_skewness(vec_avg({x}),120
```

![图片](images/img_e34f4b8ca6.png)

使用偏度处理新闻数据具有解释性。这可能意味着负偏态表征新闻预示着不好的情况，而正偏态则反应市场欣欣向荣。

- 模板的改进方向：
  - 添加信号：可以将个人常用信号放在一个列表中，使用循环尝试能否改进alpha的表现
  - 尝试将该模板作为一个信号，预示着某种市场情绪
  - 将不同数据字段进行数学运算后进行测试

---

### 评论 #35 (作者: WL13229, 时间: 2年前)

[OA92025](/hc/en-us/profiles/18197007430167-OA92025)

请使用相应的Alpha运行如下代码

s.get(simulation_response.headers['Location']).json()并阅读信息。里面的message应该会告诉你。大概率是你用了不合适的数据。

---

### 评论 #36 (作者: WL13229, 时间: 2年前)

[FL11741](/hc/en-us/profiles/18515544005527-FL11741)

很好的思考！特别是使用队列和插队的管理思路，将很多工作和simulation分开，非常聪明。一个multi最多有5个child

---

### 评论 #37 (作者: OA92025, 时间: 2年前)

您好老师，我是用了这个代码的，也能成功获取所有信息和表现，但是我的alpha提交次数却始终没有更新

---

### 评论 #38 (作者: TG50517, 时间: 2年前)

一、上周四晚上的截图

![图片](images/img_5c229018b6.png)

二、本周一晚上的截图

![图片](images/img_51aaec623f.png)

三、在周一上午提交了1277个Alpha进行回测，把它们分为10个一组，共计128组，每次提交一组，并打印其序号(序号从0开始)，这样当序号为127的组回测完成以后，表明全部回测完成，以下是部分截图。

![图片](images/img_f41d26fc7b.png)

上面是分组的代码

![图片](images/img_a6907a3a38.png)

上面是回测时程序打印出来的序号，以及最终得到的回测结果的个数

这里强调一下重点。为了测试程序的稳定性，在回测进行到第3组(打印出序号2)的时候，故意拔掉网线，自然这时候出现了错误，打印出“Error”，然后又插上网线，这时会打印出“Resume”，并从之前中断的那组开始重新simulate。

为了验证这个功能得到结果的正确性，回测了10个简单的Alpha，1次1个，第一次完整回测，第二次中间故意拔掉网线，然后又恢复，发现这两次得到的alpha_id完全一样，表明这个功能是可靠的。

![图片](images/img_b6e9696ad3.png)

第一次正常回测

![图片](images/img_1228e0638d.png)

第二次中间拔掉网线，然后又恢复

![图片](images/img_a747168698.png)

这两次得到的alpha_id完全一样

四、总结反思

代码效率：这里大部分程序是我自己写的，10个Alpha为一组，一组整体提交，回测完一组并保存结果后再提交下一组，没有用到多线程，所以没有ace库里面的simulate_alpha_list_multi函数效率高，下面的改进方向就是尽可能提高代码的执行效率。

debug经历：之前没有太多的Python编程经验，所以try…except什么的都是上午边学边写。尤其是需要考虑到程序运行时可能会遇到不止一次错误，每次遇到错误都需要从断点继续运行，刚开始写的代码遇到了死循环，经过不断修改最终实现了自己想要的功能。

模板适合的数据类型：我用的模版和老师举的例子非常相似，也是最常见的ts_rank和rank等operator的组合，所以比较适合那些自身就包含公司排名信息的数据，我也是这样搜寻数据的。虽然模版很简单，经过优化以后，也能得到可以提交的Alpha，并完成提交，如下图所示。

![图片](images/img_b6e3c3d019.png)

![图片](images/img_e1b1f66667.png)

![图片](images/img_829f681949.png)

![图片](images/img_db8ea32d48.png)

改进方向：现在遇到的问题是可以提交的Alpha太多，需要从这些Alpha里面筛选出好的Alpha，怎样判断Alpha的好坏需要一定的经验积累。另外需要把常用的程序段写为函数的形式，用到时就直接引用，这样就不需要重复造轮子。

---

### 评论 #39 (作者: OL40142, 时间: 2年前)

1. 原始

![图片](images/img_ce711a8091.png)

2. simulate结束之后

![图片](images/img_2b3f29989d.png)

程序内确实做了1000次simulation，但是为什么这儿没有效果？是因为alpha在simulation时出现错误了嘛？程序也没有报错？存储下来的simulation结果也正常

![图片](images/img_828fef8ae5.png)

3. simulate方式：

（1）取数据集：取USA股票D1数据集

（2）取fileds：在每个数据集中，取coverage>0.5且为matrix类型的的fields

![图片](images/img_eb51a58223.png)

（3）定义操作符

（4）生成alpha表达式

（5）并行回测，每次10个simulation

![图片](images/img_026ac16255.png)

4. 一些进一步的思考：

现在的操作都比较简单，单个运算符、单句回测、单个datafield，只是为了尝试回测框架，很难产生有效产出

（1）operators复杂化，进行组合，实现操作

（2）datafields组合进行操作

5. 一些问题：

（1）我的alpha表达式应该没有出错，数据集也正常，且只有在s.get(simulation_response.headers["Location"]).json()["status"]==‘COMPLETED’的时候才会计数，那问题可能出在哪里？

（2）在取数据集的时候，有些fields好像没有coverage、type等参数，这些是正常的嘛？

---

### 评论 #40 (作者: WL13229, 时间: 2年前)

@ [OA92025](/hc/en-us/profiles/18197007430167-OA92025)

同学您好，simulated和submit不是一个概念，submit没有增加是正常的。只有在s.get(simulation_response.headers["Location"]).json()["status"]==‘COMPLETED’的时候才会计数。另外如果您说simulated词数没有增加的话，可能你一直都在重复simulate以前的一个Alpha。另外请通过alpha id获取表现，才能看到是否有bug。Alpha id要和performance一一对应。检查一下你的Alpha id.最好提供截图，谢谢。

---

### 评论 #41 (作者: WL13229, 时间: 2年前)

@ [OL40142](/hc/en-us/profiles/16271500817559-OL40142)

你的观察是正确的。确实只有在s.get(simulation_response.headers["Location"]).json()["status"]==‘COMPLETED’的时候才会计数。这也是为什么要大家去截图的原因。不complete的情况很多，有些是达到了最高的simulate词数，你排队没有排上，有的Alpha没有被回测。有些是你的数据点在该模板的运算下会出现很多异常值。这些都是量化研究需要考虑到的事情。我们会在第二期导航课做展示。

---

### 评论 #42 (作者: WL13229, 时间: 2年前)

@ [TG50517](/hc/en-us/profiles/8166101444887-TG50517)

非常robust的代码！！

如何挑选出适合提交的Alpha，我们在后续课程也会有专门的设计提到。敬请期待。

---

### 评论 #43 (作者: QL10983, 时间: 2年前)

这是周一时的simulation数量：

![图片](images/img_7ae2451be1.png)

这是周二的simulation数量：

![图片](images/img_4a0c08b370.jpeg)

这个是代码日志截图：

![图片](images/img_134c3c04aa.png)

思考：

我将Brain平台的网络接口封装了几个函数来供调用，最开始会遇到效率问题，主要是循环1000次速度太慢，而且我在第一次跑的时候忘记修改参数导致所有的simulation都是一样的。后来将10次模拟进行并发，将response全部发送出去并且将报头存起来，发送完成后再以此进行结果查询从而极大提升了模拟的效率。

由于使用了平台给的结果查询示例代码进行每次查询后的等待，基本没有遇见网络问题和代码中断的问题。为了保险起见还是进行了异常捕获以防止代码异常中断。

测试过程使用了之前我发布过的文章中的思想结合ROE和PB，每次测试修改不同的时间段前的系数进行测试。因为最近时间有限，截止周二完成了1000次提交但是还未细致分析结果以及不同参数间的关系，将在后续课程进行中继续深入分析。

---

### 评论 #44 (作者: XC63878, 时间: 2年前)

1. 截图一

![图片](images/img_a536223b79.png)

1. 截图二

![图片](images/img_9e0d31e302.png)

1. 连续1000个simulation

![图片](images/img_b97c12d283.png)

这一块完成的不太好。由于自己的代码中没有使用多线程，效率特别慢，基本上跑完一个Alpha要半分钟，所以要跑完1000次回测肯定会遇到登录超时的问题（如上图所示）。需要在代码中增加异常检测和断点续传的功能。

如果登录超时，报错的情况不太一致。根据观察，有时是simulation_progress_url = simulation_response.headers['Location']报错KeyError:'location';有时是报错ConnectionError: ('Connection aborted.', TimeoutError)。所以异常情况需要考虑的比较全。

为了提高处理效率，自己想到的解决方案是 **同时打开多个任务窗口** ，同时跑一样的代码（仅数据起始点不同），变相地实现并发回测Alpha。虽然也跑完了1000个回测，但实际中应该不能这么做。

1. **问题**

（1）由于“先导课”没有听，估计是自己遗漏了一些API的相关信息，比如每次登录时长限制4个小时、brain平台可同时进行10个simulation等。通过看其他同学的帖子，掌握了一些优化的方向。

（2）其他同学的回测的时长，有一个多小时的，也有两个多小时的。如果都是在同时提交10个simulation这种情况下，回测性能还与哪些因素相关呢？是Brain平台的忙闲吗？

（3）有个疑问：当前我们实现的内容，应该只是Alpha的回测，即使在1000次回测中发现了可以提交的Alpha，系统也不会自动给submit，应该还需要手动submit吧？

1. **改进方向**

（1）当前的代码效率太低，看到其他同学有用“多线程”的，对这块不是太懂，目前还在学习优化这部分程序中。

（2）模板数据类型：自己使用的模版是【Alpha灵感】A股换手率类因子，因为原表达式中有cap这个数据字段，所以是对cap进行替换。比较好的数据集应该是price volume data，但这个数据集中筛选出的cap数据太少，不到1000个。所以是在All categories中筛选的cap数据字段，这估计会影响Alpha的表现。此外，为了尽快完成作业，仅使用了matrix类型的数据，后续可以考虑使用vector数据。

（3）当前Alpha表达式的替换，仅实现了单个数据字段的替换，后续可以实现多个数据字段或者operator的替换，感觉这样应该更能够找到低correlation的Alpha。

（4）将回测结果保存为文件，便于后续再次使用。

---

### 评论 #45 (作者: WD77850, 时间: 2年前)

1 前后对比

![图片](images/img_7f36294eda.png)

![图片](images/img_d794b4e162.png)

2 证明连续提交 ![图片](images/img_b3c8d5026e.png)

- 如图我修改了 get alpha的方法 并使用一个变量来计算alpha的数量 最后结果显示1000个 ![图片](images/img_208bb691b7.png)
- 最后一个抓取的alpha也确实是该data set 内最后一个 ![图片](images/img_430976aa1b.png)

3 反思

我选择了【Alpha灵感】The option to stock volume ratio and future returns期权和股票成交量比率和未来回报率 作为alpha模板 并对其中opt4_secpr_volume这个字段进行替换优化。由于该数据字段于期权的价格数据有关， 所以我认为可以通过遍历一个期权价格的data set 来寻找最优数据字段。于是我选择了data set: Implied Volatility and Pricing for Equity options。 这个data set 里面的数据字段大部分与期权价格相关，数量正好有1196个。检查alpha的模拟结果，发现了Sharpe最优的数据字段 opt4_30_call_dis_delta55，这个数据表示的30天看涨期权的价差，用价差代替了原来的期权价格数据。我猜测是因为期权价差增大时同样指示了期权市场热度增大，投资者更加趋向于用期权对冲风险的现象，也符合O/S比原理的设定。该结果相较于之前选择的opt4_secpr_volume 有了较大的提升。关于代码效率的问题，我认为可以减少sleep的时间来提高。关于模板的后续改进方向，我认为可以通过加入止损条件，设置多个分组等方式进行优化。（抱歉因为最近一直在进行期末考试，没有足够的时间深入研究，下次会进行改善） ![图片](images/img_f01a806bbc.png)

---

### 评论 #46 (作者: WL13229, 时间: 2年前)

[WD77850](/hc/en-us/profiles/17370721245207-WD77850)

最后的Alpha没法提交吗

---

### 评论 #47 (作者: WD77850, 时间: 2年前)

本来想着比赛的时候再交的，结果刚才重新测prod correlation全变成0.9了,有人抢先交了hh

---

### 评论 #48 (作者: DZ54968, 时间: 2年前)

1、回测1000+Simulation截图

![图片](images/img_db1bc48619.png)

![图片](images/img_9dbbe2b793.png)

2、尝试保证code连续性代码截图

![图片](images/img_f23f9675c4.png)

这个代码片段将会对每个id发送一个请求，并在请求失败时（例如由于服务器断开连接）等待20秒后重试。

3、总结反思

代码效率：（1）可以在使用machine前提前思考ALPHA表达式的逻辑对哪类数据比较敏感，提前思考可能会用到哪些datafeild；（2）使用多线程优化代码如下

![图片](images/img_3ea6a8c32f.png)

模版适合的数据类型：理解我的表达式适合的数据类型需要在brain平台上多次手动尝试。例如other+number类型的数据有多种，最初表达式使用的数据集是oth41_s_tech_skewness，起初只尝试了other41中的datafield，后经过尝试方向model类数据集中也有适合的datafield。

模版的改进方向：基于Sharpe选出改进后的表达式，发现换手率有一定提高，可以进一步设置过滤条件降低换手率。

![图片](images/img_51c0425c11.png)

---

### 评论 #49 (作者: JT89676, 时间: 2年前)

1、提交结果

![图片](images/img_768e4f17f4.png)

![图片](images/img_02662ac3c7.png)

2、代码效率

simulation提交时由于网络拥堵可能暂时提交失败，可先sleep一段时间再进行重试，若采用单线程提交，那么sleep期间不能提交其他simulation，效率低下，因此可考虑多进程（multi-process）提交，由于此处为I/O密集型操作，不是CPU密集型操作，因此采用多线程（multi-thread）提交速度也不会差太多。（需要考虑电脑CPU的物理核心数）。

![图片](images/img_0fd8f3d3f3.png)

![图片](images/img_903b8322de.png)

3、debug经历：

某些simulation提交一直失败，重试次数太多会触发BRAIN平台/simulations接口的最大重试次数超出的错误，因此可以暂时保存提交失败的simulation。

4、模板：本次尝试的alpha为历史分位数因子，

```
ts_rank(mdl175_netprofitttm/mdl175_mktvalue, 180)
```

该因子考虑EP在过去一段历史区间中所处的分位数点，是常用的时间序列分析方法。我考虑使用数据集China Fundamentals and Technicals Model的字段进行替换，并使用[60, 90, 120, 180]的不同历史区间，分别为2、3、4、6个季度（实际按每个月的交易日来算更合理一些）。最后获取alpha的相关模拟信息，将'turnover', 'returns', 'drawdown', 'dateCreated' 等保存到csv中方便后续分析，其中valid字段根据alpha is阶段的各项check得到，若所有check均通过则check为True。

![图片](images/img_a1cc32aa7e.png)

![图片](images/img_39c63a0e3f.png)

---

### 评论 #50 (作者: HJ98329, 时间: 2年前)

参考之前文章 [https://support.worldquantbrain.com/hc/en-us/community/posts/19524432578967--Alpha%E7%81%B5%E6%84%9F-%E4%BB%8EICIR%E8%A7%92%E5%BA%A6%E6%8E%A2%E8%AE%A8%E9%A3%8E%E6%A0%BC%E5%9B%A0%E5%AD%90%E7%9A%84%E5%9D%87%E5%80%BC%E5%9B%9E%E5%A4%8D%E6%80%A7](https://support.worldquantbrain.com/hc/en-us/community/posts/19524432578967--Alpha%E7%81%B5%E6%84%9F-%E4%BB%8EICIR%E8%A7%92%E5%BA%A6%E6%8E%A2%E8%AE%A8%E9%A3%8E%E6%A0%BC%E5%9B%A0%E5%AD%90%E7%9A%84%E5%9D%87%E5%80%BC%E5%9B%9E%E5%A4%8D%E6%80%A7)  
的思路，决定仿照传统的因子筛选方法，即主要考虑ICIR值，来筛选出表现较佳的因子，提供的因子模板如下：

```
returns > -0.1 ? (ts_ir(ts_corr(ts_returns(vwap, 30), ts_delay(group_neutralize((data field), market), 30), 90), 90)) : -1
```

首先获取符合以下setting的数据集，而后再获取数据集下的所有字段，为简单起见，仅考虑数据类型为MATRIX的字段。

![图片](images/img_536b697c98.png)

利用得到的字段，插入到模板中，并结合setting，打包成包含simulation data的迭代器。

利用thread库，对循环进行（十）多线程处理的方式。由于此为IO密集型任务，理论上应该没有很大的速度差异。并且规避了在不借助其他库的情况下，multiprocessing库中的目标函数中不能包含复杂对象的问题。

![图片](images/img_fc803186d4.png)

![图片](images/img_dfa7706ee8.png)

![图片](images/img_14bffaf4ab.png)

由于此次是第一次运行程序，仅用了比较简略的方式捕获异常，未对异常进行处理。猜测正是由于这个原因，理论上应该得到5500个左右的回测结果，实际上，只有2500左右的alpha被上传到了brain。后续会继续细化异常处理模块，找出其中的原因，并储存下来以作参考。

总结与反思：

1. 如上，接下来继续完善异常处理模块，能够捕捉从很多个易出错的session.get()处出现的错误，从而知晓每个因子的运行情况；

2. 接下来继续完善结果查询代码，初步思路为，回测完成后，先按照回测时间判断是否为今日(最近)回测完的因子，并取出保存，再批量获取结果以及FAIL信息。对于表现较好的，再采取相关性检测；

3. 本帖回测此思路仅为示意，并不是一个很好的idea，没有结合任何主观的判断之类的东西。这方面还需日后在课上学习一下思路。

---

### 评论 #51 (作者: WL13229, 时间: 2年前)

@ [DZ54968](/hc/en-us/profiles/18130763917463-DZ54968)

请问您选择的模板是什么意思？很好奇

---

### 评论 #52 (作者: WL13229, 时间: 2年前)

[HJ98329](/hc/en-us/profiles/13955136965015-HJ98329)

这个模板似乎不错，请问最后效果如何？有没有一些比较有潜力的？

---

### 评论 #53 (作者: ZZ51944, 时间: 2年前)

补充：完成1000个alpha的截图：

![图片](images/img_0966ff25d1.png)

![图片](images/img_eaa761deb7.png)

问题1：切换网络位置总是会出现Remote Disconnected问题，怎么解决？

问题2：1000个总共跑了2个多小时，好像比其他人慢一些，可能的原因是什么？

---

### 评论 #54 (作者: HJ98329, 时间: 2年前)

[WL13229](/hc/en-us/profiles/12285040305687-WL13229)

刚刚又看了一眼表达式，发现写错了，应该是

```
returns > -0.1 ? (ts_ir(ts_corr(ts_returns(vwap, 1), ts_delay(group_neutralize((data field), market), 30), 90), 90)) : -1
```

由于我check results相关的代码还暂未完善，需要稍微改进一下。改进完成后会把结果发到这里的，谢谢

---

### 评论 #55 (作者: YH87923, 时间: 2年前)

很抱歉第一个任务并未完成，由于从来没有学习过任何的编程语言，所以以下呈现的编程均是由chat GPT写成，我真心希望能够尽快跟上大家的进度，请大家给予我一些学习的建议

1．任务截图

截图1：

![图片](images/img_22876278d6.png)

截图2：

![图片](images/img_7d1dee1ac2.png)

这次的任务中我的问题出现在step456，

- Step4: 使用代码获取该类型的所有数据集和大部分数据字段（datafield)
- Step5: 对数据进行初步处理（例如vector data需要先使用vector operator降维）
- Step6: 将数据字段插入模板，批量生成Alpha表达式。

具体截图如下：

Step4:

![图片](images/img_77f4b7942f.png)

虽然能连续不断地输出alpha，但是并不能simulate，而且查询了发现都是同一个alpha_id

![图片](images/img_91df653f0c.png)

并且运行的时间也很长

![图片](images/img_6c1e87574a.png)

Step6的代码：

尝试1：chat推荐的并行结构

![图片](images/img_39728e33c3.png)

尝试2：

Chat推荐的异步编程框架asyncio

![图片](images/img_b074b910d3.png)

Chat解释：代码的含义是通过使用异步编程框架asyncio来提高代码的效率和并发性能。首先，我们创建一个异步函数 submit_alpha_simulation 来模拟提交alpha simulation的过程，并使用 asyncio.sleep() 来模拟alpha simulation的耗时。然后，在主函数中使用异步函数 submit_alpha_simulation 来构建任务列表，并使用 asyncio.gather() 来同时运行多个任务。最后，我们通过分批次提交alpha simulations的方式来提高并发性能，并使用 alpha_id_count_list 列表来存储alpha_id和其运行次数。预计运行时间会明显缩短，取决于alpha simulation的耗时以及平台的响应速度。

请问有哪里可以改进吗，或者说对于python零基础的人来说，需要怎么询问chat GPT能够快速地达到改进代码效率，并且还能真正用进自己的想法。

2.学习到的内容:

（1）学会了存储alpha信息

![图片](images/img_2c830a6634.png)

（2）知道了这次中用到的代码的编程知识：

Python的HTTP请求库和处理响应的方法。
Python的数据结构和处理方法，例如列表、字典等，以及如何定义和传递参数。
Python操作数据，可以使用Pandas库进行数据处理和分析。
使用API进行数据获取，使用Pandas进行数据处理。
Python的数据处理库进行数据处理。
Python进行字符串处理，以及如何使用模板引擎来生成动态表达式。
Python的字符串处理和API调用，以及如何处理参数和设置。
Python的网络请求库，例如requests库，以及如何处理API的请求和响应。
如何解析JSON数据，以及如何提取所需信息。
Python的日志库进行日志记录。

3.Debug经历：

每一环节都有，没一个没有的。登录花了一天时间，Simulate成功第一个alpha花了两天时间，寻找批量生成的代码花了一天时间

在与大家有较大差距的情况下，希望能够跟上大家的脚步，也希望能够得到大家的指导与建议

---

### 评论 #56 (作者: WL13229, 时间: 2年前)

@ [ZZ51944](/hc/en-us/profiles/18187109975191-ZZ51944)

1. 不断尝试重连即可。最好不要用VPN

2. 不同人的Alpha长度、模板不同，计算时间自然是不同的

---

### 评论 #57 (作者: ML15895, 时间: 2年前)

1. 上周 ![图片](images/img_c42a52f30d.png)

2. 这周 ![图片](images/img_944d34374d.png)

3. 成功连续发送1000个alpha expression
 ![图片](images/img_b46cbc2724.png)

4. 总结反思，基本上根据 [BRAIN API可以实现的功能这个帖子](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD) 和之前workshop的经验成功运行并获取到Performance Comparison的结果。

- **代码效率** ：代码主要实现的功能是成功提交alpha expression，通过simulation_response.status_code是否等于201判断，如果不等于，等待之后再提交同一个alpha，避免字段被遗漏，等成功提交完之后过一段时间再统一获取alpha结果。后续会考虑添加检查每个alpha expression是否运行成功。个人感觉代码效率一般，运行时间较长。看大家评论可以用多线程或者并行，后续可以尝试加入。
- **debug经历** ：获取Performance Comparison是会遇到错误，多试几次之后错误消失，具体机制不是太了解，对Performance Comparison网站界面中，前后的结果以及红色绿色上升下降箭头部分的计算不是很清楚，希望李老师课上能够简单介绍一下。
- **模版适合的数据类型** ：使用了这个帖子中的模版
  ```
  ts_rank(rank(datafields), 20)
  ```
  开始选择了Global Fundamental Data，因为它的fieldCount在（CHN，delay=1，TOP3000）中有1054个字段，所以先试了这个，结果看到基本Sharpe和Returns都是负数，后来看描述发现这个数据库是基本上都是annual或者quarterly的数据，应该是使用该模版对年度数据不合适。后来使用alphaCount的数量对数据库排序，选择排名前五的数据库，Price Volume Data for Equity， China Fundamentals and Technicals Model， Company Fundamental Data for Equity， Analyst Revisions， Quant Model Data，回测结果发现model175（China Fundamentals and Technicals Model）和model26（ Analyst Revisions）中有部分关于基本面的字段能在该模版下获得大于2.07的Sharpe，所以正如李老师这个帖子所说，这个模版适用于基本面数据，后续还需要更加深入的分析。这一部分的分析主要通过观察网站的alphas list，但是这样效率低，后续希望能够写成代码，通过排序和获取字段描述实现自动化。
- **模版的改进方向** ：一些初步的想法：
  1. 通过对比两个数据库，analyst revisions能获取Sharpe>2.07的比例高，所以使用该模版之前，可考虑对数据字段做一些预处理。
  2. 通过调整ts_rank频率，扩大可用字段范围。
  3. 将这个模版变成一个signal，然后再利用其他operator处理这个signal。
  这些想法还有待进一步尝试，如果纯用代码方式，第二个是比较好修改，但是第一个和第三个想法没有那么直接，目前反而觉得从网站中打开一个simulation然后一点点试会更直接。后续希望自己的代码能够更加灵活的变动alpha，继续加油，向大家学习。

---

### 评论 #58 (作者: WL13229, 时间: 2年前)

[YH87923](/hc/en-us/profiles/16858167567639-YH87923)

可以看出，您的学习曲线还是非常陡峭的。了解了一些Python的知识。如果是Python零基础，建议看一些视频补一下Python知识→ **[Python零基础](https://www.bilibili.com/video/BV1uY411b75q?p=1&vd_source=d8812fb45dfb16ea5c50d5afa12af977)** 。

我们在明天的导航课会现场演示一个代码框架，可以参考。

---

### 评论 #59 (作者: WH24469, 时间: 2年前)

- ### 1000次提交前

![图片](images/img_8652a1f0d6.png)

- ### 1000次提交后

![图片](images/img_8dcb55c175.png)

- ### 已连续提交1000个alpha（这里我提交的不止1000个）

![图片](images/img_a313025d3f.png)

- ### 反思

**代码效率** ：

在获取datasets和datafields时都是使用for循环，导致效率非常低，此时想到用多进程提高效率，但发现多进程的情况下找不到location，可能是由于网站不允许多进程。

**Debug经历** ：

首先是当要连续提交1000个alpha时，可能由于运行时间过长网站重启，或者过程断网了，导致出现如下error，过程中保证网络通常及限制simulation的数量就不会报错了。

![图片](images/img_9e905a5c9f.png)

其次是获取数据字段的df时有时会获取到空的df，导致找不到‘id’这一列，添加一个判断df是否为空的条件，若df为空，则进行下一数据字段的获取，若df不为空，则正常运行，问题解决。

![图片](images/img_d623a481b9.png)

![图片](images/img_5f15d1eed3.png)

最后是1000个alpha中有个很奇怪的alpha，前面很长一段时间都没有交易信号，有了交易信号后pnl跑的飞快：

![图片](images/img_e677c6ca83.png)

适合的数据类型：

按目前回测的alpha来看，暂时还未发现适合的数据类型，但US市场的TOP3000是比TOP1000要好的。

改进方向：

现在运用的还是从第一个数据集的第一个数据字段开始从始至终逐一带入formula，所以效率较低，且需要人工记录进行到那个字段了，无法让程序自动记录并在下一次重新启动程序时继续后面的字段，所以这方面需要改进。其次是现在还只是修改了一个参数，未来可能需要进行更多种多样化的参数组合，所以还需要探索更加智能化、自动化的调参模块，实现真正的睡觉也能挖alpha，另外如果添加某些筛选阈值来记录比较优良的参数组合或formula并将其保存到一个文件中用于分析会更加易于观察alpha的特征。

---

### 评论 #60 (作者: SL57524, 时间: 2年前)

模版思路：

我选用这篇文章进行复现

1. [【Alpha灵感】股票收益是球队还是硬币？](/hc/en-us/community/posts/19137620283415--Alpha%E7%81%B5%E6%84%9F-%E8%82%A1%E7%A5%A8%E6%94%B6%E7%9B%8A%E6%98%AF%E7%90%83%E9%98%9F%E8%BF%98%E6%98%AF%E7%A1%AC%E5%B8%81-)

基本思路和该Alpha灵感中相似，但略有不同

Moskowitz（2021）论述了当人们抛一枚硬币时，如果上次抛出

了正面，人们倾向于猜测下次会是反面，这是因为人们对抛硬

币这件活动本身比较了解，因此会以“反转”的眼光来看待“抛

硬币”；而当一个新赛季开始时，如果猜测哪只球队会夺冠，

由于人们对新赛季的球队成员和磨合等不是很了解，因此只能

以这些球队的历史成绩来考察它们，此时人们会猜测上赛季的

冠军，依旧将在本赛季夺冠，即人们会以“动量”的眼光来判

断“谁会夺冠”。

然而上述理论应用于股票时，却总是事与愿违。由于投资者对

动量和反转的预期，会导致其在提前采取行动时反应过度，从

而使预期发生“动量”的股票实际可能发生反转，预期发生

“反转”的股票实际可能发生动量。我们据此逻辑构造了“球

队硬币”因子。

#具体而言，我们认为波动率和换手率的变化量可以代表一支股票表现的“可知性”，即更像硬币还是更像球队。

#每月月底计算最近 20 天的日间收益率的标准差，作为当月的日间波动率,比较每只股票的日间波动率与市场截面均值的大小关系，将日间波动率小于市场均值的股票，视为“硬币”型股票

bodong = ts_std_dev(returns,20);

bodong_market = group_mean (bodong,1,market);

#计算每支股票 t 日换手率与 t-1 日换手率的差值，作为 t 日换手率的变化量。

#将每只股票的换手率变化量与当日全市场的换手率变化量的均值做比较，我们认为换手率变化量高于市场均值的股票为“球队”型股票，其未来将大概率发生反转效应；换手率变化量低于市场均值的，为“硬币”股票，未来将大概率发生动量效应。

huanshou = ts_delta(volume/ sharesout,1);

huanshou_market = group_mean (huanshou,1,market);

#找一个原本被认为是reverse的因子，然后对个股分别用这两种判断是否为“硬币”的方式进行判断，如果是硬币，未来发生动量效应的概率更大，把这些股票的Reverse因子前面加负号，对于球队类型的股票，这些因子不做处理。

但在本次作业中，为了简化，下文表达式中的name就是我想要寻找1000次的某个数据集，这个数据集应当是一个原本被认为是reverse的因子，此处仅用波动率作为判别是否是“硬币”的标准（相比研报简化）：

bodong = ts_std_dev(returns,20);bodong_market = group_mean (bodong,1,market);factor = ts_mean({},20);- if_else((bodong < bodong_market), -factor, factor)'.format(name)

【此处有待探究：如果根据原文，用两种判别硬币的方法结合起来可以达到更好效果】

紧接着我选取数据字段（即适用于作为某个反转因子的数据字段，此处可以再严格加以限制，通过预先的simulation以一定标准筛选出有作为反转因子潜力的数据字段：

![图片](images/img_527599c00f.png)

然后在最简单的情况下进行1000次实验，可以看出，和评论区其他同学进行的相似，10次完成的simulation大概需要5分钟，那么1000次要超过500分钟才能完成（此处我没有继续进行1000次）：

针对于中断连接问题，我是选择在检测到异常状态之后重新登陆。我自己实验的过程中仅出现一次status 为400的情况。但根据评论区同学描述，可能还存在其他异常状态，此处可能并不完善。

针对多线程的问题，由于我之前没有学过相关内容，因此尝试复现评论区
DZ54968同学的观点，学习了thread的应用

![图片](images/img_1c15ad1527.png)

但出现一系列问题，目前尚在思考

---

### 评论 #61 (作者: AZ81686, 时间: 2年前)

![图片](images/img_93695bf4c6.jpeg)  ![图片](images/img_1d1d493659.jpeg)  ![图片](images/img_2048b07c14.jpeg)

总结反思:

代码功能：代码特点是将ACE help func和“BRAIN API可以实现的功能”融合，实现多线程回测和connection aborted问题解决；楼上有同学提到多线程问题，其实实测BRAIN最多可以同时simulate 50个regular alphas，不仅是10个

改进方向：断点续跑的解决方案(那其实就还涉及本地数据的管理)，alpha expression错误及其他问题的自动化handle

思考：在什么样的场景下才需要用到像这样一次性1000次simulate的功能，楼上同学好像是用简单的模版搜dataset，猜可能是来评估datafield的效用；那如果是要来优化已有的逻辑往深了做呢？如果只是改参数，似乎有"overfit"的嫌疑；如果是搜operators，那是不是就意味着需要对operators进行分组，（就像是在同一个dataset中搜相似含义的datafields) 在相似作用的operator group中搜operators；上面考虑的是operator的替换，那operator之间的嵌套逻辑应该怎么样? 还没想清楚

ps: 可以看到在代码通过[expression] * 1000生成1千个相同的表达式进行simulate后，IS alpha数没变，检查后发现系统其实会检测simulate的alpha是否和已有alpha的内容相同，如果相同就不会重新sim和创建新alpha id，而是返回旧结果（及id）

---

### 评论 #62 (作者: DZ54968, 时间: 2年前)

@ [WL13229](/hc/en-us/profiles/12285040305687-WL13229)

抱歉评论里的模版截图是另一个正在做的alpha表达式中。关于本次case中使用的alpha模版是关于市场偏斜度的group_neutralize(rank(-mdl175_revs10)+rank(-vec_avg(oth41_s_tech_skewness)), bucket(rank(cap), range='0.5, 1, 0.1'))。通过查询相关datafield更换mdl175_revs10和oth41_s_tech_skewness两类数据，寻找最优组合

---

### 评论 #63 (作者: WL13229, 时间: 2年前)

[DZ54968](/hc/en-us/profiles/18130763917463-DZ54968)

谢谢您的回答，nice!

---

### 评论 #64 (作者: WL13229, 时间: 2年前)

@ [WH24469](/hc/en-us/profiles/13991511763607-WH24469)   [SL57524](/hc/en-us/profiles/18074114880791-SL57524)

希望今天第二期导航课上，其他同学的分享能对各位的研究有所启发。我们周四还有Office Hour，即面向所有顾问的答疑时间，欢迎大家来。

---

### 评论 #65 (作者: YL37225, 时间: 2年前)

1.simulation超过1000次

![图片](images/img_5787cb4299.png) 2.连续提交simulation
 ![图片](images/img_2577c3c51b.png) 3.总结反思
·设置sleep似乎并不会比并行计算慢太多，自己不太擅长编程，就使用了较为简单的time.sleep(6)，不过参数的设置是经过了几次尝试得到的，更换成其他alpha或者修改simulation的设置可能会需要修改参数。

·获取到的数据字段比想象中多许多，未来完成作业我只对其中一部分进行了分析，之后可以尝试对得到的数据字段设置更加精细的筛选。
·为了解决超时登出问题所使用的while ture函数似乎导致所有的simulation模拟完之后又重新模拟第一个，这个问题我还正在解决。

---

### 评论 #66 (作者: XZ75239, 时间: 2年前)

提交作业，参考【Alpha灵感】分析师的真知灼见。考虑刻画出未提前反应在股价中的分析师信息，使用

dataset_id为"analyst14"的数据集，有数据的股票不多，大约是一个比较受分析师关注的股票池。。。

表达式粗糙地尝试了四种：

"rank(abs(ts_delta("+x+",250))/ts_delta(close,250))-0.5"

"rank(-ts_delta(close,250)/abs(ts_delta("+x+",250)))-0.5"

"rank(regression_neut(ts_delta("+x+",250),ts_delta(close,250)))-0.5"

"rank(-regression_neut(ts_delta(close,250),ts_delta("+x+",250)))-0.5"

1、截图1

![图片](images/img_3ff96611be.png)

2、截图2

![图片](images/img_97acc64b61.png)

3、代码截图

![图片](images/img_40050ad4dd.png)

代码能力比较弱，遇到中断只好多次使用try和except，有惊无险无间断地跑完了1000次。。。

考虑改进：1、学习多线程争取跑快点；2、找到还行的夏普比后，也许可以在某个范围内调整参数和表达式直到结果更好。

小白第一次批量跑因子，感到很新奇。。感谢平台的慷慨授课，期待后续的课程~

---

### 评论 #67 (作者: QC95604, 时间: 2年前)

作业提交：

![图片](images/img_0a02d0208a.jpeg)

![图片](images/img_c58ae91923.jpeg)

总结：

初次尝试使用API，确实比网页版的高效。多进程方式无法使用，但可以使用多线程，多线程的方式比for快5~6倍。

代码参考： **[BRAIN API可以实现的功能 – WorldQuant BRAIN](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD)**

**模板参考：** Research Paper 68: An Augmented q-Factor Model with Expected Growth

代码实现过程中遇到一些问题：

1、 ![图片](images/img_7bf767003f.jpeg)

解决方案：加入 try 和 except

2、 ![图片](images/img_bbdc50dc17.jpeg)

尝试使用  **[BRAIN API可以实现的功能 – WorldQuant BRAIN](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD) 中所提及的“一种解决超时登出的解决方案”，但会重复运行，如下：**

**![图片](images/img_8a0e5c2072.jpeg)**

**为防止报错时可继续执行，在except中加入 return None，这样在运行获取报告时只有当返回不是None才加入列表**

```
def simulation_alphas(datafields):    # alpha code    s = sign_in()     # 每次函数被调用时都会执行，不知道会不会造成过度登录？先将就吧    try:        # simlation code        return alpha    except Exception as e:        print(f"Error processing: {e}")         return None  # 返回一个特殊的值表示错误
```

使用Python的`concurrent.futures`库来并行处理`simulation_alphas`函数：

```
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:    results = []    for result in tqdm.tqdm(executor.map(simulation_alphas, datafields), total=len(datafields)):        if result is not None:  # 检查结果是否是特殊的值            results.append(result)
```

最终结果耗时约50分钟：

![图片](images/img_24059a8c8c.jpeg)

![图片](images/img_0e5b326767.jpeg)

---

### 评论 #68 (作者: WL13229, 时间: 2年前)

[QC95604](/hc/en-us/profiles/19798287001111-QC95604)

谢谢提交。看到有个Alpha表现还不错，可以提交吗？

---

### 评论 #69 (作者: ZC69109, 时间: 2年前)

```
问题1:在运行四个小时后api会断开解决：通过创建re-authenticate function每200次simulation后会重新登录问题2：遇到无法simulate的datafield时simulation断开解决：error handling，try-except-continue, 并且记录下不适用datafield问题3：当程序断开重新启动时，会重复run已经run过的datafield还未解决，不过可以通过记录datafield_df来实现问题4:  generated alpha < simulations还未解决，需要进一步阅读api使用文章
```

---

### 评论 #70 (作者: WL13229, 时间: 2年前)

[ZC69109](/hc/en-us/profiles/16836600918551-ZC69109)

请参考本帖子其他同学的作业继续精进。否则后续课程会有非常大的困难。另外每200次重新登录，并不会解决超时登出的问题。目前没有看到您连续完成1000次的证明。

---

### 评论 #71 (作者: ZF71008, 时间: 2年前)

非常感谢老师和大家的论坛分享！小白一枚，非计算机非金融背景，先来领一张第一节课的入场券。。。目前基本完成作业要求，后续有改进再更。。。

1.周四的截图 ![图片](images/img_40a4265dbb.png)

2.周五的截图

![图片](images/img_0f428c98b3.png)

1. 结果

我参考的是这个模板：【Alpha灵感】 看不见的负担

主要搜索'Relationship Data for Equity'相关的datafield以替代pv13_h2_sector

设置发起1000 次Simulation，成功提交994个

![图片](images/img_21e96f2797.png)

目前只是在运行过程打印了epoch信息以显示进度

其他信息作为返回值存在了列表里，需要查看再打印，如performance comparison中的部分关键信息：

![图片](images/img_e1b96c3c90.png)

偶尔遇到不匹配的数据就跳过

![图片](images/img_ed0d3817a2.png)

测试时候遇到计算时间太久的也跳过

![图片](images/img_e123ed6990.png)

1. 反思

4.1 代码效率

目前只是按照最简单的逻辑写出来了最基本的功能，不太懂线程和进程的概念。。。

写了一个循环每10个绑为一组进行处理，回到平台试图增加新的任务，error显示似乎已经达到上限 ![图片](images/img_a0b420477a.png)

并且为了缩短测试时间，设置了一个时间阈值，超过30s的alpha就先过掉了

4.2 debug经历

有时候被 KeyError: 'alpha' 中断（运行这个语句：alpha_id = progress.json()["alpha"]）；

参考论坛这篇文章《BRAIN API及日常回测时常见的报错》，老师的回答：有些Alpha虽然有location，但是不一定能返回json.当您的代码获取到location后，您需要使用get方法获取location的信息，如有返回，才能解析出json. 这意味着，有时候它的返回是None, 或者里面没有信息。

随后写了一个try except 把返回值为None的url就抛弃了。

有时候遇到很长时间的simulation（有的15分钟左右，可能是计算超时最终中断报错，返回的simulation_progress里没有“alpha“ header），大概率是因为datafield中vector的没有处理直接喂进模板导致simulation时间过长。这1000次模拟非常漫长，结果也只有40个alpha成功提交。

随后写了一个try except，把sleep30s以上的就跳过了。并且暂时先仅输入matrix类型的数据。

4.3模板适合的数据类型

当前模板数据类型仅支持martix，在预处理的时候仅检索’MATIRX’, 把vector和group都舍弃了

4.4模板的改进方向

代码的优化和效率的提升，对于我来说还有非常大的改进空间，暂且搁置。在功能方面，希望下一步可以先解决：当前模板数据类型仅支持martix，需要考虑怎么处理vector和group类型的datafield；

需要一段代码，帮助检验相关性等筛选可以提交的alpha

---

### 评论 #72 (作者: EC34309, 时间: 2年前)

**(I apologize in advance for writing this in mostly English, I understand chinese perfectly but I can't type it out efficiently.) ![图片](images/img_8b49beb511.png)  ![图片](images/img_9c11bd4f81.png)**

**Step2: 思考合適的資料欄位和參數。以此範本為例，可能基本面的model data也是不錯的，但時間參數可能需要至少月以上。如果是量價數據，可能需要更短的時間週期。**

我选择了 “【Alpha靈感】A股市場擁擠度因子”.

**Step3: 使用**  [**Data Explorer**](https://platform.worldquantbrain.com/data)  **手動嘗試幾個不同類型(category)的資料集，再次深入反思該範本提取的是什麼層面的資訊。/** 模板適合的資料類型

The original paper suggests a surge of volume, might imply a concentration of capital and bubbles in certain subsets of assets.

A sudden surge of volume is defined as following:

Let “2nd volume” be the mean volume of this week and “1st volume” be the mean volume of last week.

If one of the three conditions is satisfied, the current day is a score of 1, otherwise 0:

1. mean volume of this week > mean volume of last week + predefined volume
2. (mean volume of this week) / (mean volume of last week) > 2
3. mean volume of this week > mean volume of last week + predefined volume AND being the top P% in ratio (mean volume of this week) / (mean volume of last week) in a cross-section.

By searching volume on Data Explorer, the results can be divided into these broad category:

Daily volume:

- Interval volume
- Sentiment volume
- Put/call volume
- Average daily volume

The most obvious data fields, which are used in the original post.

- Relative sentiment volume

Similar logic as trade volume.

模板的改進方向:

Price Metrics/Fundamentals:

- Volume weighted average price
- Daily open/close/high/low price
- Dividend
- Stock split ratio

A surge in prices relative to fundamentals could potentially detect bubbles.

Market Share Metrics:

- Anonymous market share
- Industry/Tier 1 market share
- Concentration metrics like summation of squared market shares

A surge in retail traders can also imply bubbles.

**Step4: 使用代碼取得該類型的所有資料集和大部分資料欄位（datafield)**

**Step5: 將資料初步處理（例如vector data需要先使用vector operator降維）**

For some reason, vector and group data all use too many resources, causing a failure to simulation (for instance, vec_avg(scl12_cubealltype_buzzvec)).

Is this because I have an overseas account or is it the same for everyone?

Regardless, I wrote the appropriate if else statement to apply a vector / group operator if such data types are detected.

**Step6: 將資料欄位插入模板，批次產生Alpha表達式。**

**Step7: 將Alpha表達式附上simulation setting （這一階段可以使用比較常見的setting，無需過度調參）**

To ensure the degree of freedom in terms of simulation data, I allowed the changes on the entire simulation data instead of just the data fields, which motivated me to write a generator to prevent excessive memory usage.

![图片](images/img_144b0f5d28.png)

**截圖顯示你的code連續不停（不可中斷，代碼需能handle各類報錯）**

I used multi-threading on the “simulate” function, which returns alpha id if simulation proceeds successfully. If syntax error / time-out occurs, no id would be returned.

In the multithreading function, I set up a limiter to manage workers so that it keeps the simulation number constantly on 10 (the limits). Alpha-id is recorded and returned as a list.

![图片](images/img_7fbe99a374.png) A dataframe of performance can be generated via get_test_all.

![图片](images/img_50e5c6a772.png) A plot on sharpe of simulated ratio can be obtained:

![图片](images/img_698511f542.png)

Unfortunately, I can't re-login continuously as an overseas account requires biometric-authentication.

總結反思，需包含至少四個面向的反思：程式碼效率、debug經驗、模板適合的資料類型、模板的改進方向。多寫不限，字數不少於300字。

“代碼效率”:

Generator on simulation_data_list greatly improves memory complexity,

I did think of writing a recursive generator as if we allow more freedom on the simulation settings, purely written nested for loport is not the best approach, but it is not that importantops at this stage.

“Debug經驗” :

I didn't encounter any significant bugs, the api is very well-written.

I did need to request the biometric authentication link and then re-login again to receive <201> response, which is the closest obstacle I encountered.

「範本適合的資料類型,範本的改進方向」: already discussed in  **Step3**

However, I wish to elaborate on the problem on the current template,

As most of the data-fields can't even reach a sharpe of 2, across different universes of CHN and USA, strongly suggest against the logic of this template.

There could be several reasons for this phenomenon:

1. Bubble/ concentration of capital detection is correct, but the momentum of the bubble carries significant risks
2. Bubble/ concentration of capital detection is incorrect, meaning volume related data can't effectively detect bubbles via the current rule.

Possible improvement could be:

1. Stricter bubble detection for more sensitive data, such that we only short when the stock is at nearly high points.
2. More relaxed detection for less sensitive data, preventing strategy with nearly one-off trade.
3. Time decay on counting “score”, as we are using ts_sum currently which has the same weight for current day and let's say the past kth day.

---

### 评论 #73 (作者: WL13229, 时间: 2年前)

[ZF71008](/hc/en-us/profiles/20098272506775-ZF71008)

看到这位同学在回测期间成功还提交了一个Alpha,祝贺！

---

### 评论 #74 (作者: WL13229, 时间: 2年前)

[EC34309](/hc/en-us/profiles/13557080755991-EC34309)

这位同学展示出了出色的代码能力和金融能力，相信后面的课程一定能给你更多启发。让我们下节课再见。

---

### 评论 #75 (作者: OD35570, 时间: 2年前)

1、

总共simulate了1000个左右的alpha，在模型意义上还有所欠缺，可能导致回测出来的结果欠佳

simulation前

![图片](images/img_39767ffd97.png)

simulation后

![图片](images/img_41bb8e8a3e.png)

2、模板的选择 ： 【alpha灵感】单因子测试之财务质量因子

```
my_group = bucket(rank(cap), range="0.1, 1, 0.1");group_neutralize(rank(mdl175_roediluted+mdl175_cashrateofsales), my_group)
```

我们考虑替换的数据字段是用相关的基本面数据作为因子来替换，从而选定了数据集fundamental28，然后选取其中的数据字段进行替换，从而组成我们等待回测的alpha字段。

3、回测具体的步骤

根据上一期同学的经验，我们考虑最大线程数为10的线程池进行回测，一次提交10个alpha进行回测，本次操作和后面的操作中貌似都没有出现bug，所以我仅仅用设置了一个try 来实现断线重连。

![图片](images/img_1661de05fe.png)

此外为了验证alpha的质量，我仅仅选取了 ['SHARPE','FITNESS','TURNOVER'] 这几个数据来进行导出，并且储存到Excel中方便查看。 ![图片](images/img_bbf3d84a21.png)

4、不足与反思

- 感觉在所挖掘的alpha在经济意义上不强，回测效果较差，仅仅有2-3个勉强sharpe达到要求，可能需要后续学习如何针对性的进行提升。
- 觉得通过大模型api的接口可以省却很多理解研报的时间，后续会往这方面多学习

---

### 评论 #76 (作者: YT47842, 时间: 2年前)

我下午提交了1200次，但是由于开始提交的时候忘记截图了，所以傍晚用同样的代码又提交。但是发现这个报错 ![图片](images/img_e5c431366d.png)

请问有同学遇到过类似的问题吗？
具体报错信息：ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

以下是下午提交1200次后的结果： ![图片](images/img_941867d49b.png)

这里是提交的用时
 ![图片](images/img_b0843a524c.png) 这里是提交的alpha的模拟结果
 ![图片](images/img_e94589a020.png) 思考：
使用的alpha表达式：

'ehat=ts_regression(returns, {datafields_list[n*epoch+j]}, 60);group_zscore(ts_zscore(-ehat, 60), subindustry)'

代码效率：
使用了10个一组的测试方法，但是感觉使用并发后代码效率会更高
debug经历：
同样遇到了simulation_progress.json()['alpha']找不到对象的问题。在报错中看出是表达式的书写有拼写错误，改正拼写错误后该错误消失；
遇到过在提交过程中有VPN被禁止的问，关掉VPN后恢复正常（但是由于之后需要使用GPT类的工具所以代理也是必须的，希望下次能够改进这个）
模版适合的数据类型：
我选用的是price volume的数据，对于vector使用vec_sum对于matrix则不做处理
模版改进的方向：
该模版由于是从论文研报合集中取得所以prod_corr比较高，后期需要从其他数据源的论文中获取一些灵感

---

### 评论 #77 (作者: QZ41342, 时间: 2年前)

1.开始提交前

共1190次

![图片](images/img_c7e4242e2d.png)

2.提交完成后

共2214次

![图片](images/img_fbacce88cc.png)

1. 代码连续运行情况

连续完成提交1000次，后续可能考虑多进程等方法加快速度

![图片](images/img_921ebc700b.png)

4.总结与反思

本次我参考遗传规划的方法：

（1）首先在python定义brain平台支持的运算符为python函数，使用传入数据名称，输出因子表达式；前期共定义了包括ts_mean，ts_regression等十余个函数

例如：

```
def ts_corr(x,y):    return f'ts_corr({x},{y},10)'
```

（2）在一次循环中，随机选择使用运算符的个数（设置最大个数为4以避免过拟合），然后根据算符的个数随机抽取运算符，然后根据运算符所需的数据个数随机抽取数据种类

（3）对抽取的运算符和数据进行拼接，形成完整的因子表达式

（4）对因子表达式进行检验，使用因子检验通过条件的比例作为目标函数

效果如下：

![图片](images/img_70d536b55b.png)

这样的方法能够快速组合出大量的因子表达式并进行检验，但由于brain是提供表达式进行检验，无法调用常规的遗传规划库进行优化，本次的简单尝试中也没有加入优化算法的思维，导致无法快速找到较好的因子，可能会作为一个以后尝试的方向。

---

### 评论 #78 (作者: WL13229, 时间: 2年前)

[YT47842](/hc/en-us/profiles/19897065331095-YT47842)

您好，这个报错就是超时登出的错误。需要反复重连直至连通

---

### 评论 #79 (作者: SM56169, 时间: 2年前)

1.最近的截图（需包括时间）

![图片](images/img_5afe4446a5.png)

2.下周二前的截图（需显示时间）

![图片](images/img_3ed81e0a48.png)

3.截图显示你的code **连续不停（不可中断，代码需能handle各类报错）** 提交了1000个simulation。

![图片](images/img_4c0cccc6a7.png)

4.总结反思，需包含至少四个方面的反思：代码效率、debug经历、模板适合的数据类型、模板的改进方向。多写不限，字数不少于300字。

代码效率：可以通过多线程提交测试任务成倍缩短总的回测时间。在连接断开的情况下，可以增加一些异常处理机制，确保测试任务能够在连接恢复后继续执行。可以考虑将测试失败的alpha信息记录下来，以便后续分析和修复。

debug经历：在回测未完成时，会提示Location字段不存在的错误，加入了检验Location字段是否存在的判断条件。

模板适合的数据类型：正向信号的基本面数据，机构调研数据，对已有的因子的结果做平滑。

模板的改进方向：模板的改进方向可以包括对不同数据选择不同的时间区间，以适应不同市场环境的变化。在显示回测结果方面，可以设计更结构化、直观的报告，包括性能指标、风险分析、交易历史等信息，提供全面的策略评估信息。此外，记录合格的alpha的相关信息，可以包括因子参数、调优结果等，有助于更深入地理解策略的表现。

---

### 评论 #80 (作者: YT47842, 时间: 2年前)

补充重跑之后的截图

提交之前 ![图片](images/img_205a95c4e5.png) 这里是提交1080次之后的结果 ![图片](images/img_c733ca46c5.png)

---

### 评论 #81 (作者: YW27566, 时间: 2年前)

（1）开始simulation前的截图

```

```

（2）simulation后的截图，完成1000+

![图片](images/img_c935700388.jpeg) （3）在跑代码的过程中，每次测试都会计数来显示代码完成的进度，中间连接中断会自动重新登录账号，重新连接并且重新进行模拟测试并显示retry alpha simulation

![图片](images/img_f6560f3b3e.jpeg)

![图片](images/img_52b24b7163.jpeg)

（4）总结

在代码效率提升方面，采用了multiprocessing多进程的方式同时跑多个进程来提高运行效率。通过共享内存变量来同步不同进程使用的公共计数变量和记录如果没跑通发生错误的变量list。debug方面，如果alpha没跑通就执行alpha_id = simulation_progress.json()["alpha"]会报错，所以在执行这个语句之前加入了状态查看，status=simulation_progress.json()['status']，如果显示fail就会记录错误并跳过。通过get_alpha_perform_rst函数记录下每个alpha的表现便于最后查看结果。

![图片](images/img_9862f49036.jpeg)

在模板使用上，只单纯用了rank函数为了测试跑通整个框架。直接用esg数据和eraning forecast数据表现不佳，forecast数据略好，之后可以尝试用不止用截面上的函数表达式，可以尝试时间序列上的函数如ts_rank，并尝试和其他信息结合构造出新的alpha提升效果。

---

### 评论 #82 (作者: FZ15092, 时间: 2年前)

在本次完成本次作业的调试与实际运行过程中共提交了约1500次测试

1. 代码测试与运行前

![图片](images/img_19dbc90868.png)

2. 测试与运行后：

![图片](images/img_ba470f3484.png)

3. 代码截图

由于我的个人原因这次作业完成的较为仓促，在基本跑通代码后我优先对1000次simulate的任务进行了实现，以免剩余时间不足以及可能出现的其他报错处理，在最多线程为10的参数设置下，1000次测试任务的完成时间约40分钟。在完成了测试任务后我又对代码的信息输出部分进行了优化以体现提交进度与报错信息，优化后输出效果如下：（以一次18次的测试为例）

![图片](images/img_a5f4eb0773.png)

4. 总结反思

在代码效率方面，Alpha提交的效率在多线程运作下已经相对较快，但我尚未对参数进行更多尝试寻找实现最优运作效率的参数，此方面也许仍有提升空间

在debug的过程中，我通过程序报错发现一个dataset的id可能对应几个不同的dataset，而在网页端搜索只能搜索到其中的一条，希望老师能够帮助解释一下这个问题

![图片](images/img_2330efe0c6.png)

因子模板方面，我使用了一个反转Alpha作为模板：

```
-(close-ts_delay(close,5))/close
```

，来自于文章《【Alpha灵感】新闻动量文章启发的反转策略实现》老师的评论区回复，老师称之为一个经典的反转策略想法。在老师题目区的想法启发下我选择了基本面数据集来套用此模板，并相应将时间参数拉长至20天（1个月），观测结果后在某些datafield上发现了一些可能存在信号的Alpha，但距离提交仍有一定差距，后续我会尝试进一步进行筛选与优化

![图片](images/img_6d98921614.png)

目前在实现Alpha提交以后我还未完成Alpha的测试结果统计与筛选等功能的代码，这方面是我亟待完成的部分，希望老师和同学们多多批评指教

---

### 评论 #83 (作者: JS48146, 时间: 2年前)

运行前后截图和对比：

![图片](images/img_89eb9fdb9e.png)

![图片](images/img_8c0303dbb4.png)

阅读了【Alpha灵感】分析师的真知灼见。使用的dataset为Estimations of Key Fundamentals，共包含870个datafields。

遇到问题和设计：

1. Location问题，参考老师在【BRAIN API及日常回测时常见的报错】中的回答，使用if解决。
2. 使用多线程进行simulation，参考之前同学的经验使用了10个线程。在代码中包含这一行，表示对某一个alpha完成了simulation：
3. ![图片](images/img_a692d086ad.png)
4. 因为想要使用一个总的dataframe储存所有的alpha的表现，因此使用lock防止不同线程写冲突。
5. 连续运行后的结果:
6. ![图片](images/img_6dec844805.png)

仍存在的问题：

实际simulation并且能够得到表现的alpha有1600+个，但是在alpha平台上看到的结果只增加了1000个，这是为什么呢。

---

### 评论 #84 (作者: PF41122, 时间: 2年前)

1. 最近的截图： ![图片](images/img_6db95d801d.png)
2. Simulation后截图： ![图片](images/img_5c61035b7f.png)
3. 连续simulate 1000+截图： ![图片](images/img_386aa8a043.png)
4. 实现功能：除了基本的寻找datafield，multisimulation， check，comparison等functions外，还收集了所有simulations的结果数据，方便后期手动筛选或分析。并且simulation的结果和对应的时间会实时更新，方便追踪进度以及前期debug。
5. 代码效率：因为加了一些额外的功能，所以跑10个alpha/组的时间大概在1分半，跑1000个alpha大概在2个多小时。
6. debug经历：发现有些datafield会报错，目前的处理方法是，先simulate一遍选好的datafield，把不会报错的做成alpha expression。当然还发现中途如果电脑进入屏幕保护状态，connection会断开，并一直尝试重连，重新进入界面之后会重新连接，继续开始simulation，所以之后就取消了屏幕保护。
7. 模板适合的数据类型：模型取自 [alpha idea 看不见的负担](/hc/en-us/community/posts/19137319051671--Alpha%E7%81%B5%E6%84%9F-%E7%9C%8B%E4%B8%8D%E8%A7%81%E7%9A%84%E8%B4%9F%E6%8B%85) 。先通过pv13_h2_sector进行分组，然后通过goodwill和sales的比值构建alpha。目前的做法就是将goodwill和sales相关的能用的datafield进行组合来simulate，但还有疑问的就是vector或者matrix等不同的数据类型对simulation结果的影响，或者是否需要做单独的处理呢？因为是fundamental的数据，目前时间节点有按quarter设置，但尚不明确每个datafield数据的frequency以及最早的availability，应该也会影响simulation的结果。

1. 模板的改进方向：观察simulation的结果发现，ts_mean的时间取一年以内能获得更好的表现，所以下一步simulation可以将时间范围缩小到一年内。并且加入一些短期的数据是会有利于提高sharpe的，idea原文中有提到close，或许vwap，volume等也是可以尝试的。

---

### 评论 #85 (作者: KZ79256, 时间: 2年前)

1.最近的截图（需包括时间）

![图片](images/img_0040aa7054.png)

2.下周二前的截图（需显示时间）

![图片](images/img_24d60f2788.png)

3.截图显示你的code **连续不停（不可中断，代码需能handle各类报错）** 提交了1000个simulation。请自行考虑，如何print合适的信息，证明已经提交了1000个Alpha.这种技能会使得你的code更加易读，也能帮助你在代码运行时了解其状态。

![图片](images/img_ee408018fc.png)

4. 总结反思，需包含至少四个方面的反思：代码效率、debug经历、模板适合的数据类型、模板的改进方向。多写不限，字数不少于300字。

- 代码效率: 10线程并行，1.5h模拟了1k+, 由于没有获取FAIL的performance，所以速度上可能比较快
- debug经历: 由于之前用过api调过参，所以直接改的，bug比较少
- 模板：使用的是 【Alpha灵感】基于量价信息的可靠投资信号 里面的模板

```
    m_minus = ts_mean({tmp_1}, 30) - ts_mean({tmp_1}, 10);    delta = (ts_max(m_minus,10)-m_minus)/(ts_max(m_minus,10)-ts_min(m_minus,10));    PCY = 0.2*delta+0.8*ts_delay(delta,1);    signal = -close/vwap;    trade_when(PCY>ts_delay(PCY,1), signal, -1);
```

通过get_datafields(s, instrument_type='EQUITY', region='USA', delay=1, universe='TOP3000', search='price')获取和price相关的数据，然后注意替换里面的tmp_1。由于没有调参，使得部分测试部分指标不达标
 ![图片](images/img_e28139d5c9.png)

- 模板的改进方向

可以通过该方法快速确定，部分适宜的字段。然后调整里面的部分参数，使得整体结果走向更好

可以修改signal的组成方式

---

### 评论 #86 (作者: WL13229, 时间: 2年前)

[JS48146](/hc/en-us/profiles/16529616166551-JS48146)

如果一个Alpha之前被你simulated过，它就不会在面板上增加次数了

---

### 评论 #87 (作者: EH13432, 时间: 2年前)

作业提交：

由于期末考试的原因，上次训练营只参加了先导课内容。任务已经在上次中提交，这里放一个结果，其他不再重复

![图片](images/img_a8384b8400.png)

本次主要是进行了一些修补工作——首先改进了一下我的多重模拟函数，主要在传递参数上，我把每一个可能输入的部分全部用列表形式表达。函数中会自动遍历所有参数组合后的alpha。

另外还是在解决上次任务留下来的一些遗留问题。比如在生成is评价表和self- performance评价表时会出现jsondecodeerror：老师提供的想法很有帮助——使用try except确保json的解析可以规避问题

![图片](images/img_6c7e8710f5.png)

这是目前实现的结果，希望多多指教

---

### 评论 #88 (作者: SK24143, 时间: 2年前)

感谢worldquant平台的课程！

由于代码还没有跑完，先放个运行截图，后续补上

![图片](images/img_3b3ed41e72.png)

![图片](images/img_40e36ea6f2.png)

由于自己是计算机小白，所以在代码方面向其他同学有所借鉴。使用的是多线程concurrent.futures，maxworker=10.

使用的模板是最近提交的一个因子的模板，想看一下有没有更多这样的关系，当然表达式是很简单的zscore(ts_regression({id},fnd27_s_fa_eps_diluted_valueadj,30,rettype=2))，这里选取的数据集是fundamental27的matrix类型的数据。本次进行1200次的模拟，使用的CHN市场，delay=1.

思考与总结：目前只是使用一个数据字段，而没有很多的数据同时输入，所以模型较为简单，也主要起到一个测试的作用。这个模板应该是泛化能力还可以的，但是可能单独这个模板达不到平台提交的标准，之后可以尝试更复杂的模型。要更多地总结论文研报以及其他同学的思路，以及可以恰当的使用大语言模型进行研究。

补充结果，用时80分钟，由于选取的模板不是太好，导致基本没有很好的因子，今后会在模板构建上下功夫，以下为simulate1200次之后的截图。

![图片](images/img_439cc99ea3.png)

---

### 评论 #89 (作者: YZ64617, 时间: 2年前)

模拟前

![图片](images/img_c86957e2b3.png)

模拟后，

![图片](images/img_18d6742673.png)

这次一共模拟了5300多个alpha，耗时6小时

![图片](images/img_78fed6c4ac.png)

### 编程方面

我的步骤是

1. 抓取datafield，写了一个针对settings和dataset.id的函数，并将结果保存成csv格式
2. 使用template批量生成alpha。
3. 批量simulate所有alpha。这个过程，会处理token过期和错误。同时，将成功和失败的都记录成log，保存。
4. simulation过程，是没有alpha ID的，但是会有simulation ID。simulation ID都在第3步记录下来，生成一个URL。GET 这些url，获得alpha id/、。【遇到的问题】simulationID似乎超过一定时间就会不存在，所以，simulate了6个小时，早晨起来，进行后续的时候，alpha id很多已经无法获取了。但是，如果是短时间simulate，这个方法是没有问题的。
5. 使用alpha id，读取alpha的表现。

### 关于token过期和意外链接失效的问题的处理：

- token有效期4小时，14400秒。所以，在每simulate一个alpha的时候，检查一下是否超过一个值（例如，14000秒），如果超过，则重新生成token。
- 对于一些异常，使用try处理。

![图片](images/img_9b10c0d154.png) 我写了一个simulate单个alpha的函数和一个批量simulate的函数。批量simulate函数中，加入了token过期和异常处理。

我的token方式和Brain API的不同。这个是很早很早之前写的，所以就保留了下来。后期，考虑结合Brain API的session方式，对代码进行调整。

### 遇到的问题和思考

1. simluation ID的失效问题。

针对这个解决方法是， [https://api.worldquantbrain.com/users/self/alphas](https://api.worldquantbrain.com/users/self/alphas) ? ➕时间filter条，直接抓起alpha的信息。

除此之外，还可以通过Brain 平台的个人alpha页面进行filter。 [https://platform.worldquantbrain.com/alphas/unsubmitted](https://platform.worldquantbrain.com/alphas/unsubmitted)

但是，似乎Brain 平台有bug或者限制。在网页端，我无法通过performance筛选，也无法把performace显示出来。如图

![图片](images/img_8158599051.png)

由于遇到这几个特殊情况，目前还无法看到所有的5300个alpha的表现，需要对代码进行再加工。

2. 数据集和模版

我这次使用的是 model122， CHN Vector数据，D1。公式模版是单参数的，所以，并不抱很大希望有可以提交的。公式模版如下

![图片](images/img_00bbea1958.png)

计划任务

- 程序方面，需要再优化。例如，simulate+alpha结果这个过程，alpha结果的后续处理等。
- alpha模版方面：需要针对不同类型的dataset/datafield，使用对应的更有效的模版。这就涉及到，dataset的探索
- 每一个datafield都有它自身的各种特点。考虑将论坛的提到的6种方法加进去。也考虑做一个本地dataset的保存，方便自己打标签和快速读取。

---

### 评论 #90 (作者: DZ54968, 时间: 2年前)

1 最近的截图

![图片](images/img_26ae9cb78f.png)

2 回测1000+次后截图

![图片](images/img_531d440e43.png)

3 连续提交1000+Alpha截图

![图片](images/img_e4691266e9.png)

![图片](images/img_0b633f1ff1.png)

4 总结反思

代码效率：选取datafield的数据进行挖掘时可以先关注原策略表达式本身数据具有什么特征，通过category等先进行预筛选，避免测试许多无用数据字段。

debug经历：使用API测试Alpha的过程中注意表达式换行空格等问题出现的报错

模版适合的数据类型：本次选取的是ALPHA灵感中凸显理性因子STR，在进行API挖掘时，手动在brain平台中精炼表达式对后续machine挖掘alpha具有重要作用。在测试原策略表达式时，对于用于计算的核心字段returns，先手动替换为volume、turnover（volume/sharesout）等量价层面相关的字段进行测试，观察相关类型数据字段的回测结果。再考虑使用fundamental等其他类型的字段进行测试。观察各类型测试结果后再在使用api时提取对应的datafield进行测试，能够对所做策略具有更深的理解并提高alpha挖掘效率

模版的改进方向：在数据字段替换层面，可以考虑使用双循环或多循环替换不同位置的数据字段，找出最优组合

---

### 评论 #91 (作者: DK85731, 时间: 2年前)

2401 作业提交 （网络问题提交延迟）

![图片](images/img_0a6418992b.png)

![图片](images/img_658c705a30.png)

![图片](images/img_048180a806.png)

1. 总结反思，需包含至少四个方面的反思：代码效率、debug经历、模板适合的数据类型、模板的改进方向。多写不限，字数不少于300字。

代码效率：由于multiprocessing与ipynb兼容性较差，thread与windows兼容性较差，暂时采用单线程模式代替方案，设置长度为10的队列，循环检测接口可用性，待有空余时将该消息pop并simulate新factor。之后将用py进行改写以实现多线程效率提升。

Debug 经历：主要处理多线程相关问题，主要问题包括无输出不自动停止运行，且使用multiprocess出现不自动停止的bug时需restart kernel以重启，建议选取已有多线程模式进行修改，或者改用除python外的编程语言

模板合适数据类型：选取 [【Alpha灵感】振幅因子的切割]([Commented] 【Alpha灵感】振幅因子的切割.md)  作为模板来源，检验参数约束条件，确定参数迭代方向进行grid test

总结模板的改进方向：经过1000次simulation，发现同一idea下sharpe浮动空间在-1与1之间，但选取同类factor有可能改善回报与相关性，之后应该将同类因子放进同一框架进行测试

---

### 评论 #92 (作者: JH86905, 时间: 2年前)

1.开始截图

![图片](images/img_f97e36a79c.jpeg)

2.API提交后的截图

![图片](images/img_e1c378db33.jpeg)

3. 连续不断提交Alpha的截图

![图片](images/img_867ed71ec5.jpeg)

4. 参考的论文：基于价量互动的选股因子，实现方式比较简单。先分别计算换手率和单日最高最低价差的滑动均值，再计算差分，之后通过其（负）相关性的程度作为Alpha信号。

5.过程记录

a)代码效率: 修改了ACE比赛的模板，使得可以同时simulate 10个Alpha，1000组左右Alpha可以在少于1小时内运行完。目前实现的功能还较为简单，只包括对于各个时序数据所选取时间的搜寻，即在人为确定适合的datafield后再进行数值搜索。目前正在加上GA功能，利用sharpe或fitness的反馈来优化搜索方向。

b)debug经历。一开始出现了链接中断导致代码运行失败的情况，后通过修改，为多线程simulate的方法加上断线重连的功能，在10秒内如果出现timeout就保存断点并再次重连。

c)模板适合的数据类型。目前的模板仅仅支持matrix数据，后续会增加对于vector数据的支持。

d)模板的改进方向。1）利用GA进行数值方面的优化。2）尝试采用不同的数据集，加大搜寻的范围。

---

### 评论 #93 (作者: YT47842, 时间: 2年前)

虽然昨天已经完成了1000次提交，但是今天修改了代码，并使用了新的alpha Expression思路。感觉比昨天有了一定的改进

这个是提交前的alpha计数
 ![图片](images/img_9a4648523d.png)

这个是完成1200次模拟后的alpha记录 ![图片](images/img_ce93ce1a5f.png)

注意到提交了1200次但是只有1130次成功了，下次需要再在函数中打印出提交失败的simulate任务看看咋回事。

这个是提交用时 ![图片](images/img_53b4d71e4a.png)

这个是1200个alpha的performance

![图片](images/img_b80dcba193.png)

这次的模拟还获得了一个可以提交的alpha

![图片](images/img_04a4ea05ed.png)

但是后来发现这个prod_cor过高 >_<

思考：
使用的alpha因子：

"""vhat=ts_regression(scale({datafields_list[n*epoch+j]}),ts_delay(scale(snt_buzz),1),500);ehat=ts_regression(scale(returns),vhat,500);alpha=group_neutralize(-ehat*ts_rank({datafields_list[n*epoch+j]},5),bucket(rank(cap),range='0,1,0.1'));trade_when(abs(returns)<0.08,alpha,abs(returns)>0.1)"""

代码效率：
对代码做了工程上的改进，使用多线程并发，将模拟时间缩短了25%以上
debug经历：
由于昨天已经做了相关的模拟，所以今天的模拟中没有发生bug
模版适合的数据类型：
今天的因子同样选用的是price volume的数据，对于vector使用vec_sum对于matrix则不做处理
模版改进的方向：
还是prod_cor过高，感觉需要继续挖掘新的因子才能解决这个问题

---

### 评论 #94 (作者: WL13229, 时间: 2年前)

[YZ64617](/hc/en-us/profiles/4527497709335-YZ64617)

您好，查看不到performance可能有两个原因。

1。网页缩放问题，调整一下网页缩放的大小（按住control键+鼠标上下滚轮）试一试能不能显示。

2. 过往的Alpha太久了。尝试多simulate一些过第二天看看。

如果尝试上面两个还无法解决，请与我们联系。

---

### 评论 #95 (作者: YZ64617, 时间: 2年前)

[WL13229](/hc/en-us/profiles/12285040305687-WL13229)

谢谢，现在可以再页面上看到performance了。

更新一下alpha结果，有很多sharp比较高的结果，但是，基本都有一个IS Ladder Sharp不通过的问题。

![图片](images/img_90bd14a269.png)

![图片](images/img_750f4dfb5b.png)

对于这个问题，不知道如何入手解决，求建议。

---

### 评论 #96 (作者: YL37225, 时间: 2年前)

**1.alpha提交多次

 ![图片](images/img_c8944f8d96.png)  ![图片](images/img_f14ad34825.png) 

2.alpha的连续提交**  ![图片](images/img_cdea237c12.png) 
 **3.总结反思** ·批量生成alpha的过程中遇到vector数据需特殊调整，这一部分我设计的代码还不具有普适性。
·不太擅长编程，使用了较为简单的time.sleep( )而没有进行多线程的设计，后续可以进行调整。更换alpha或者修改simulation的设置可能会需要修改time.sleep( )函数的参数。·获取到的数据字段比想象中多许多，因为时间关系只对其中一部分进行了分析。
·目前我的代码中如果想，解决超时登出问题而使用while ture函数就会导致所有的simulation模拟完之后又重新模拟第一个。
·每次进行一次大规模simulation时需要耗费的时间较多，应当设计代码记录当前进度，我的代码目前还是每次又重新从第一组数据开始尝试simulation，效率很低。

---

### 评论 #97 (作者: DL55804, 时间: 2年前)

1. 开始截图，此时simulation的数目是1608 ![图片](images/img_186ebd94b0.png)
2. API提交后截图，此时simulation的数目是 ![图片](images/img_b2d1ccbf72.png)
3. 连续不断提交alpha的截图 ![图片](images/img_b2747b3e5d.png)
4. 反思总结——代码效率
   1. 代码的效率大约是1小时能跑1000个左右，目前的做法是使用多线程同时进行10次simulation，simulation结束后，获取alpha的表现 ![图片](images/img_3d7555c876.png)
   2. 解决长时间运行会自动断开的问题。在simulation中，如果回测的alpha有问题，就会发生alpha_check=False，如果是连接断开，就会重新连接，因为使用的是多线程，所以考虑一旦某一个线程断开，其他线程也会断开，所以用一个reconnect_status来表示某一个线程已经再进行重新登录，其他线程只需要等待连接即可。While True确保了断开之后能重复尝试连接 ![图片](images/img_44ef7d792e.png)

1. 具体的代码流程：产生需要回测的参数列表、登录、回测、获取表现、保存simulate的结果到csv中 ![图片](images/img_965d7b13e0.png)
2. 默认的setting为下左图所示。我认为除了region universe delay需要通过setting来进行调整，其他的部分都可以通过在alpha的表达式里，自己进行decay或者中性化，所以通常自己simulate的时候只修改三个部分，也就是下右图所示在表达式里可以自行定义，自由度更高。 ![图片](images/img_9d33b0fae0.png)

1. Simiulate的模板是：【Alpha灵感】凸显理论（Salience Theory）

个人感觉研报的核心应该是提出的那个凸显性，尝试使用换手率构造凸显性，其中可以用来构造凸显性的数据应该很多，包括收益率、换手率，现在感觉甚至是一些情绪指标、基本面指标都可以用来构造。 ![图片](images/img_ee351215bc.png)

1. 参数调整 ![图片](images/img_c5a655d9e7.png)

Window1是取一段时间signal的平均值

Theta是求凸显性的参数

Direction是信号的方向

percent可以让我们可以只交易两端的信号，

skip是考虑到像动量效应会有一些短期的反转，所以可以考虑delay一段时间的信号

hold是类似于decay的天数 ![图片](images/img_53ca3bf404.png)  ![图片](images/img_9b438f5fba.png)  ![图片](images/img_df0ae6fad1.png)

1. 模板的改进思路： 首先是尝试很多类似成交量、换手率、成交额的数据。2. 尝试一些其他的凸显性，类似于基本面的凸显性。3. 使用一些operator让alpha更稳健，例如ts_zscore、ts_rank。
2. Debug的一些反思：由于用了相当多的try，导致debug的过程异常的艰难，现在想来每一次post或者get都应该查看status，如果报错了，根据错误信息进行debug效果应该会更好。2. 还没有想清楚如何更好地可视化performance，以提供更多地信息，方便改进alpha
3. 回测的performance存在csv中 ![图片](images/img_ccb9e0e707.png)

回测的performance存在csv中

---

### 评论 #98 (作者: SW14484, 时间: 2年前)

第一部分：

1. 不间断连续运行1064次

起始数量：530

![图片](images/img_0caf895833.png)

截止数量：1594

![图片](images/img_3778c12173.png)

共花费时间：

![图片](images/img_532498f5dc.png)

步骤详细说明：

（1）单次API成功提交的实现

- 确定API接口参数：首先，需要了解API的具体要求，包括需要的参数、请求方式（GET、POST等）以及任何特定的请求头。
- 编写代码：基于API的要求，编写相应的代码以构建请求。这可能包括设置请求头、构建请求体、以及处理任何必要的身份验证步骤。
- 测试提交：在开发环境中测试API提交，确保所有参数都正确设置，并且能够成功获得预期的响应。
- 记录日志：为每次API提交创建日志记录，以便跟踪问题和性能。

（2）分析API提交的时间间隔和单线程提交的局限性

- 确定时间间隔：发现API有20秒的时间间隔限制，这意味着每次提交后至少需要等待20秒才能进行下一次提交。
- 计算单线程提交时间：考虑到这个限制，如果使用单线程提交1000次，每次等待20秒，加上提交本身的时间，总时间将非常长，至少需要5.5小时。

（3）引入多线程解决方案并处理相关问题

- 确定线程数量：为了加速提交过程，决定使用多线程。通过实验，发现开启10个线程可以达到较好的性能和稳定性。
- 解决多线程访问共享数据的问题：当多个线程需要访问或修改同一数据时，可能会出现死锁或数据不一致的问题。为了解决这个问题，引入了线程锁或其他同步机制，确保每次只有一个线程可以访问或修改数据。
- 调试与优化：在引入多线程后，可能会遇到各种预料之外的问题，如线程冲突、资源竞争等。通过不断地调试和代码优化，最终解决了这些问题。

（4）最终的提交效果

- 性能提升：通过使用多线程，显著提高了API的提交速度。从原来的5.5小时减少到了大约64分钟，大大提高了工作效率。
- 总结与反思：回顾整个优化过程，不仅解决了API提交的问题，还学到了很多关于多线程编程和性能优化的知识。同时，也意识到在引入多线程时，需要特别注意数据同步和线程冲突的问题。

第二部分：

我阅读的是：抢跑者的脚步声，基于价量互动的选股因子这篇研报

在投资领域，我们常常会遇到这样一个现象：当面临重要事件或消息时，投资者往往会加大筹码，试图通过买卖股票来获取更大的收益。这种现象在得到内幕消息时尤为明显，知情交易者（informed trader）通常会急于抛售或买入股票，以期在股价变动前获得利益。然而，作为普通投资者，我们往往无法获取这些内幕消息。那么，如何在不知道内幕消息的情况下，合理规避风险，抓住投资机会呢？

这篇研报为我们提供了一种解决方案：通过异常信号来识别知情交易者的行动。研报作者发现，成交量是泄露知情交易者行动的重要信息源。具体来说，换手率与第二天股价的波动呈现出正相关关系。这意味着，在股票大跌前，知情交易者会大量抛售股票，急于离场，导致换手率上升；而在大涨前，知情交易者会大量购买股票，急于进场，同样会导致换手率上升。这种换手率与股价波动的正相关关系，暗示了信息泄露程度的高低。当这种关系越强时，说明信息泄露程度越高，我们在该类股票上的博弈可能陷入劣势。

为了衡量股票未公开信息的泄露程度，研报提出了一个名为抢跑因子（Front Running, FR）的指标。这个指标通过计算T日换手率与T+1日涨跌幅的关系来评估信息泄露的程度。为了公平比较，研报在计算抢跑因子时剔除了常规因子如市值、动量、换手率、波动率和行业等因素的影响。

纯净的抢跑因子:FR=𝛽1𝑙𝑜𝑔(𝐹𝐴𝑀𝐶)+𝛽220𝐷𝑀𝑜𝑚+𝛽3𝑇𝑢𝑟𝑛+𝛽460𝐷𝑉𝑜𝑙+∑𝛽5𝑖∗𝐶𝑖𝑡𝑖𝑐𝐼𝑛𝑑𝑖+𝜀其中𝐹𝐴𝑀𝐶是股票自由流通市值，20DMom是20日动量，Turn是换手率，60DVol是60日波动率，𝐶𝑖𝑡𝑖𝑐𝐼𝑛𝑑是中信一级行业哑变量，ε是残差。

作者通过回测，得到以下结论：

首先，作者发现：当月因子值越小，次月收益越高。所以，投资者可以关注那些因子值较小的股票，因为它们可能在未来一个月内带来更高的收益。这种策略的实施，无疑增加了投资的灵活性和多样性，为投资者提供了更多的选择。

其次，研报还揭示了知情交易者在好消息和坏消息上的泄露程度存在差异。具体来说，坏消息的信息泄露现象更为显著。这意味着，在面临负面消息时，知情交易者可能更倾向于迅速采取行动，导致换手率上升。这一现象可能与投资者的心理反应有关。面对坏消息，投资者往往感到恐慌和不安，急于抛售股票以避免进一步的损失。因此，投资者在制定策略时，应充分考虑这一因素，避免在负面消息的影响下做出过激的反应。

此外，研报还探讨了上涨和下跌时𝐹𝑅0因子的预测能力差异。结果表明，下跌时的预测能力最强，整体强于上涨。这一发现为我们提供了关于市场行为的深刻洞察。在下跌时，由于投资者对损失的敏感性增加，他们可能更加关注股票的价格变动和相关信息。因此，在这种情况下，𝐹𝑅0因子能够更有效地预测股票的未来表现。

为了增强原始𝐹𝑅0因子的预测能力，研报提出了两种简单的方法。首先，可以使用𝐹𝑅𝑑因子替代𝐹𝑅0因子，即只使用下跌端的数据而不使用上涨端的数据。这种方法基于上述发现，即下跌时的预测能力最强。通过专注于下跌数据，我们可以更准确地捕捉市场行为的变化并做出更明智的投资决策。

其次，另一种方法是将上涨和下跌数据以一定比率结合起来。这种方法旨在平衡两者之间的预测能力差异，并充分利用两方面的信息。通过合理调整比率，我们可以找到最佳的平衡点，使因子在上涨和下跌时都能发挥出色的预测效果。

---

### 评论 #99 (作者: WL13229, 时间: 2年前)

[SW14484](/hc/en-us/profiles/20580045390871-SW14484)

非常完整的作业，完成速度令人赞叹。下节课我们的作业是要求将一篇论文/研报写成模板，看到你已经对该研报做了认真分析。可以着手开始尝试了。让我们下节课再见

---

### 评论 #100 (作者: BC25356, 时间: 2年前)

@ [HW97336](/hc/en-us/profiles/18134895192087-HW97336)

您好，看了您的代码，收益颇多。
可以分享下datafield_list这部分的代码吗？对于这部分，还是有疑惑的（具体怎么得到这个list的）。

---

### 评论 #101 (作者: IC51680, 时间: 2年前)

Screen Captures:

初始alpha:179

![图片](images/img_323b306cac.png)

ace library挺好用的

現有alpha 1224

![图片](images/img_9f19519beb.png)

使用ace library multi simulation, 預設是 三綫程 344 x 3 = 1032

用時 ~2hr

![图片](images/img_2dd767e435.png)

用jupyter notebook 和 acelibrary 輔助, 使用三綫程 所有代碼(generaete alpha list, simulation, return result as dataframe) 不到60 多行

debug经历: 主要是拿result的是后 ace lib prettify result會把dataframe變成style , 之後slice不了dataframem,但改改就沒事了

我閲讀了【Alpha灵感】隔夜“拉锯战”和渔利因子

這文章解釋了如何利用隔夜交易者和盆中交易者的交易模式不同所導致的mispricing來獲利,一般來說，相對專業的機構投資者和職業投資者傾向於在盤中進行交易，而隔夜交易者中，短線交易的投資者比例較高.

在價格校正的過程中，機構投資者可能會出現過度校正的情況，錯誤地將部分隔夜有效交易歸因於由噪音引起的定價錯誤。過度校正可能導致股票定價存在偏差，並在未來呈現回歸的趨勢。

RET_OC = Intraday price change
RET_CO = Overnight price change
NR = Number of intraday reversals in the opposite direction in a month / Number of actual trading days in that month
PR = Number of intraday reversals in the same direction in a month / Number of actual trading days in that month

```
ret_oc = close/open-1; days = 66ret_co = open/ts_delay(close,1)-1;NR = ts_sum(ret_co>0&&ret_oc<0?1:0,66)/days ;PR = ts_sum(ret_co<0&&ret_oc>0?1:0,66)/days ;group = bucket(rank(cap),range='0,1,0.1');group_neutralize(rank(NR)+rank(-PR),group)
```

我在回測時使用了不同neutralization setting (Market sector subindustry...) 還更改了 days

模板的改进思路: 我覺得可以增加其他factor加進去(violatitly,volume,sentiment...)

---

### 评论 #102 (作者: YZ72310, 时间: 2年前)

一、任务前后alpha截图

![图片](images/img_6333a712b1.png)

![图片](images/img_2b79e98ca3.png)

二、连续运行能力和handle重连的能力

![图片](images/img_b4f474ef89.png)

![图片](images/img_2d3daf4320.png)

三、总结反思以及需要改进的点

代码效率尚可，大约3分半钟可以完成10个alpha的提交以及结果获取。由于现在我采用的代码只是简单的调用了multisimulation的方法，并没有做进一步的优化，因此实际还是在串行，在之后需要采用多线程的方式不断检查是否有空余的simulation机会，并进行单个提交。debug经历其实不多，在看懂官方给出的文档后仅花费不多的时间就能调试成功，属于复杂但不困难。但现在的代码仅处于可以运行，还并不能算elegant，之后的想法是改为.py脚本文件从而方便后台运行和参数的添加，也能提高效率。

本次使用的模版是最基础的120天的ts_mean，适用性比较广泛，任何时序的数据类型都可以直接使用，本次操作中，是先获取一定数量的datafield，然后将数据都处理成为可以放入模版的类型再进行simulation，在此后也可以考虑边处理数据边进行simulation的方式。总体来说，这个模版由于过于简单，获得的alpha合格率不是特别高，主要都是sharpe比较低，当然也有return尚可的一些例子，但年际差异较大，无法实际使用。

对于这个模版改进的方向其实主要是增加他的复杂度，因为实际上大部分指标直接取时序平均并没有很直接的意思，可能在其中叠加横截面rank，以及标准差等运算符能够带来更多的信息。总体来说还是需要从一些基本的逻辑出发来进行改进。

![图片](images/img_521f79b3fc.png)

四、论文阅读

我阅读的是 [https://support.worldquantbrain.com/hc/en-us/community/posts/15238260154007-Research-Paper-36-Quantitative-Fundamentals-Application-of-Piotroski-F-Score-on-Non-U-S-Markets](https://support.worldquantbrain.com/hc/en-us/community/posts/15238260154007-Research-Paper-36-Quantitative-Fundamentals-Application-of-Piotroski-F-Score-on-Non-U-S-Markets)

总结和体会：这篇文章主要通过应用Piotroski F-Score方法来分析非美国市场（BRIC、英国、德国），以确定该方法对产生Alpha的效果。结论是在非美国市场，具有高F-Score的公司在股票表现上较好，相较于对应市场指数表现，平均可实现8.2%的正收益（做多仓位）。相反，具有低F-Score的公司表现非常差，相较于对应市场指数表现，平均损失25.3%（做空仓位）。通过以上分析展示了Piotroski方法在非美国市场的适用性，能够通过买入持有交易策略产生Alpha。

构造alpha的idea：使用Piotroski F-Score来对非美国市场的股票进行筛选和投资，特别是在BRIC、英国和德国等市场。通过识别具有高F-Score的公司，并在长期持有的情况下，可以获得超额收益。因此，构建alpha的关键在于执行基于F-Score的投资策略，即长期持有高F-Score公司的股票，同时做空低F-Score公司的股票，以实现市场超额收益。

---

### 评论 #103 (作者: WL13229, 时间: 2年前)

[BC25356](/hc/en-us/profiles/13921805253911-BC25356)

这个帖子有一些关于获取datafield的代码，可以查看：

[https://support.worldquantbrain.com/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD](/hc/en-us/community/posts/19831456877463-BRAIN-API%E5%8F%AF%E4%BB%A5%E5%AE%9E%E7%8E%B0%E7%9A%84%E5%8A%9F%E8%83%BD)

希望对你有帮助

---

### 评论 #104 (作者: WL13229, 时间: 2年前)

@ [IC51680](/hc/en-us/profiles/20023801895447-IC51680)

依然建议尽量从头搭建框架，即便模仿ACE library也会比直接使用得要好。因为在后续课程不断增加内容的过程中，你可能会发现debug的难度在增加。

---

### 评论 #105 (作者: DL92496, 时间: 2年前)

第一部分：

![图片](images/img_0385d606a9.png)

Total Alphas如上图。

这次测试使用的模版是ts_skewness(vec_avg({x}), {y})作为测试基础，x为数据集变量，y为时间变量，生成Alpha List，最后调用ace lib里面的simulate_alpha_list_multi仿真。关键代码如下图。

![图片](images/img_cedcbe8a35.png)

下图为仿真的状态，正在仿真，已经不间断运行超过1000次。

![图片](images/img_e002023322.png)

第二部分：

阅读文献：

Healy, Brian and O'Sullivan, Conall, Dividend Capture Returns: Anomaly or Risk Premium? Evidence from the Equity Options Markets (February 8, 2019). Michael J. Brennan Irish Finance Working Paper Series Research Paper No. 19-2, Available at SSRN:  [https://ssrn.com/abstract=3337964](https://ssrn.com/abstract=3337964)  or  [http://dx.doi.org/10.2139/ssrn.3337964](http://dx.doi.org/10.2139/ssrn.3337964)

总结如下：

这篇文章研究如何利用期权市场的信息来预测除息日当天的预期回报。研究发现，对于交易难度较大、风险较高或股息较少的股票，除息日的回报可能会更高。论文使用Option Metrics 的数据库中的数据，该数据库包含期权价格及其相关股票的信息，但论文只研究了个股的期权，而不是股票组或其他类型的期权。

交易难度较大通常指的是缺少流动性的股票，缺少流动性意味着很难买入或卖出；风险的判断有两个指标，一个是观察个股有没有与市场无关的价格变化，另外一个是透过Beta系数，Beta系数越高意味着股票价格对市场变化更加敏感；股息较少的股票的衡量标准是观察股息是否低于市场水平。文章中主要使用个股数据不包括ETF和ADR。使用的指标包括每天开盘和收盘价格，文章只关注现金分红而忽略其他其他派息事件。文章也关注每天收盘的期权价格、隐含波动率、Delta、Vega和Gamma。

---

### 评论 #106 (作者: ZY25767, 时间: 2年前)

我有一个问题，就是如果setting不变，改变alpha的生成规则，会被算作同样的alpha嘛？

---

### 评论 #107 (作者: WL13229, 时间: 2年前)

[ZY25767](/hc/en-us/profiles/17488901499543-ZY25767)

本次作业不要求改变setting，仅改变Alpha表达式即可。不同表达式，就是不同的Alpha，不会算作同样的。

---

### 评论 #108 (作者: YJ78324, 时间: 2年前)

**必做1：**

1. 批量提交前的截图

![图片](images/img_d049a93531.png)

1. 批量提交后的截图

![图片](images/img_35ceeda38b.png)

1. Alpha提交输出截图

![图片](images/img_0b50d4e788.png)

1. 总结

年前参加了第一次的英才候选人计划，当时因为时间原因没能完成最后一次的作业。此次重新参加这期活动，一方面是补上之前的课程，一方面也想进一步巩固一下之前学到的知识。模板自动化提交方面，我这周也进行了简单的优化，可以通过配置更加方便的对多个搜索字段进行填充，另外也在异常处理方面做了一些优化，现在可以稳定连续的进行Alpha提交了。

**必做2：**

本次我阅读的研报是来自太平洋证券的 **《基于交易异常的广义反转因子》**  ，这篇研报主要研究了基于交易异常的广义反转因子在A股市场的表现。研报中通过多种指标来刻画交易异常，包括收益分布的时间刻画（如隔夜-日内收益角力）、收益分布的离散度刻画（如强弱信息系数）、收益分布本身的刻画（如修正偏度）以及交易行为异常的刻画（如非流动性、异常成交量等）。

在多种因子中我选择了Attention因子进行了分析。Attention因子是用来衡量股票收益分布的异常性，特别是极端日度收益对投资者关注度的影响。这个因子基于行为金融学中的前景理论，该理论认为投资者在决策时会对小概率事件给予更高的权重，从而高估这些事件发生的概率。这种行为偏好可能导致投资者对某些股票的反应过度，从而产生预期收益率的反转效应。

具体来说，"Attention"因子的计算方法如下：

![图片](images/img_e99e5f49e8.png)

这个因子的核心思想是，极端的日度收益（无论是正的还是负的）容易吸引投资者的注意，从而影响他们的交易行为。在收益率分布上，这种关注度与收益率之间呈现出U形的曲线关系。通过这个因子，研究者试图捕捉这种关注度变化对股票未来表现的影响。

下图给出了搜索到最高夏普率的PnL

![图片](images/img_42871ecd3b.png)

---

### 评论 #109 (作者: YZ31807, 时间: 2年前)

1.
 ![图片](images/img_4d2089e2bc.png)  ![图片](images/img_3ef74c5a0e.jpeg)

本次1000次回测中我的alpha来源于【alpha灵感】单因子测试之财务质量因子。财务质量因子是一类比较重要的风格因子，可以反映企业过去的经营状况和未来的持续盈利能力，这些信息能够在一定程度上影响股票的价格。而由于财务信息具有一定的滞后性，财务因子也需要与其他因子进行结合。

rank(mdl175_roediluted*mdl175_cashrateofsales)。这个是文章中基本模型，考虑到大小盘的财务质量差异，利用group_neutralize进行处理，得到了group_neutralize(rank(mdl175_roediluted+mdl175_cashrateofsales), my_group)。在我的100次回测中，我利用get_datafields分别获取roe和cashrateofsale的数据，进行两两随机组合构建了不同的alpha进行回测。

总结与反思：

代码效率：一次性跑了1200次回测，共历时1h30min左右

Debug经历：在第一次的回测中出现了“强迫关闭现有连接”的问题，但过一会儿重新运行这段请求代码发现一切正常，目前没有太明白为什么出现这个情况，希望老师可以解答一下。 ![图片](images/img_39d44d1f4f.png)

Alpha改进思路：目前考虑除了将财务数据与cashrateofsale结合外，考虑将其与其他基本面数据结合或者添加其他的财务质量数据如现金流动比率等，提高alpha整体的稳定性。

2.

我阅读了 [Bid and Ask Prices of Index Put Options: Which Predicts the Underlying Stock Returns?](/hc/en-us/community/posts/15233936157847-Research-Paper-26-Bid-and-Ask-Prices-of-Index-Put-Options-Which-Predicts-the-Underlying-Stock-Returns) ，这篇文章分析了期权在看跌时期买入价与卖出价的波动率对未来股票超额收益的关系以及预测能力的比较。考虑到经济衰退期间和中间资本风险不断增加，以及其关于未来市场方差风险溢价的信息更丰富，卖出价更可能具有较强的预测能力。通过对 S&P500 指数深度价外（OTM）看跌期权买入价和卖出价的隐含波动率的估算，得到了卖出价的隐含波动率比买入价的隐含波动率对股票收益的预测能力更强。本篇文章的研究方法如下：

1. 引入Intermediary Asset Pricing Model用于解释买入卖出价与未来回报的关系
2. 利用线性回归检验买入价与卖出价的波动率与预期收益的关系
3. 采用employ Newey and West t-statistics进行假设检验
4. 通过回归分析与假设检验，卖出价的变化了在对于未来收益的预测显著性水平为5%。这反映了该指标与Intermediary Asset Pricing Model模型的吻合，是一个优秀的预测手段

Alpha idea：根据论文的数据集构建方式，可以建立在看跌期期权卖出价格的波动率的计算模型，以此构建alpha。

---

### 评论 #110 (作者: ZY25767, 时间: 2年前)

这次作业整体收获还是很大的，主要是懂得了API的使用方法，但感觉很希望可以参考研究员后续比较完全健全的框架，来提升速度。

这是最开始的：

![图片](images/img_84fab64541.png)

这是现在最新的

![图片](images/img_1d897ccef9.jpeg)

1. 自动登出的问题：解决办法就是每一次回测前sign in一下

2. 建议有一个官方的API文档可以说明rate的个数。现在我发现还是很慢。我对多线程还是不够了解，只是将notebook多开几个来不断的去跑。的确发现速度不够。

3. 希望有一个online server可以使用。

第二部分：

我阅读的论文是

# Research Paper 73: Uncertainty Resolution Before Earnings Announcements

![图片](images/img_5f775dd99b.png)

![图片](images/img_9fc416a908.png)

总结如下：

这篇论文讲的是根据Earnings Announcements构建的一个因子。我仔细阅读了前半部分，发现他的研究方式像是event study的感觉。

抛开理论的部分：我感觉这个文章提到了一个构建因子的方法；也就是收集 公告日 前10到后10天到[-10, +10] 收益并且用这个收益变化减去平时到收益变化绝对值，得到一个BETA表明这个股票对于 公告日来临这个时间点敏感程度。（这里可以用历史数据来进行分析）。然后根据论文的说法，这里有一个positive skewness in the announcement premium.意味着越敏感（因子值越大的股票），在这段时间的超额收益就越高。

然后我们根据这个因子值多空组合，看看表现如何。

存在的疑问：

如何将不好的研报结果的负收益情况隔离开来？我的想法是第一种可以区间放到【-10，-1】或者，通过对冲抵消这个影响。

---

### 评论 #111 (作者: WL13229, 时间: 2年前)

[ZY25767](/hc/en-us/profiles/17488901499543-ZY25767)

很好的思考，您提出的问题，我们将在后续课程中给出解答。也欢迎您在课程中与我们一同讨论。

---

### 评论 #112 (作者: WL13229, 时间: 2年前)

[YZ31807](/hc/en-us/profiles/18243220367511-YZ31807)

这是正常的报错，无论你是否在每次simulate前都sign_in，都逃脱不了这个4小时的强制断连。解决的办法是，使用try except方法，当报错时重新登录，直到成功即可。

我们会在下节课给出展示demo。欢迎你现在就进行尝试。

---

### 评论 #113 (作者: WL13229, 时间: 2年前)

[YJ78324](/hc/en-us/profiles/12940496308759-YJ78324)

欢迎回来，我对您有印象。似乎是在GA课程之前就没有看到您继续了。不知道上次GA的课您上了吗？相信这一次，你一定能找到更多的Alpha

---

### 评论 #114 (作者: WL13229, 时间: 2年前)

[ZY25767](/hc/en-us/profiles/17488901499543-ZY25767)

一个简单的思考是，如果您认为某个部分会亏钱，那么反着做，不就赚钱了吗？不过话说回来，如果想隔离，那么可以在最后赋值的时候，使用if_else，把它们变成nan即可。从文章的意思看，似乎您有一个performance的图片没有上传。

---

### 评论 #115 (作者: WM13885, 时间: 2年前)

**Task 1**

![图片](images/img_6d4f2116b4.png)  ![图片](images/img_25dcf1b163.png)

一个小时左右跑完1000个，使用的template用于测试程序，并不复杂。用rank对analyst15跑了前1000个数据字段。因为担心漏跑几个alpha所以之后又补了个对simulation的追踪。 ![图片](images/img_528d4ff84d.png)

对于代码效率这块，用的都是论坛上导师post的api使用方法和流程的代码稍微加工，也通过在跑代码的过程中在网站上尝试simulation得到simulate too many times error确认10个回测同时占用率。过程中的bug也通过自查+gpt比较顺利的解决。

下一阶段的目标就是用更复杂的template以及数据字段做更具economic sense的回测，筛选并提交有效alpha。

**Task 2**

选择的文章是【Alpha灵感】A股换手率类因子 Post by KJ42842。以下是12个换手率因子，自己也尝试用fast expression复现些：

 ![图片](images/img_b3f3057781.png) 
 ![图片](images/img_b41ae94425.png) 

这篇帖子给了我很多启发，尤其是关于优化和提高Alpha模型鲁棒性的部分。虽然原始的换手率因子在Fast Expression中复现并不困难，但作者的重点在于如何结合研报内容对其进行优化。

在分析为何原Alpha未达到Robust Universe Return标准时，作者认为这可能与A股市场的特性有关。作者假设主要问题在于原Alpha过度做空了很多换手率较小的小市值股票以获取大部分收益，而这部分收益在真实交易中无法实现。为了验证这一假设，作者重新阅读了关于换手率的研究部分（及各行业换手率均值差异）

 ![图片](images/img_4df409846e.png)

并进一步利用经济常识验证了小市值股票换手率通常较高的情况。为了证实观点，作者采用了power rank的方法，放大了个股换手率的差异，从而优化了原Alpha模型，使新Alpha能够更集中地做空换手率较高、市值较小的企业。随后，由于换手率因子在大盘股中效果较差而在中小盘股中效果较好，为进一步提高IS ladder sharpe的表现，作者采用了right_tail operator来剔除换手率较低的大盘股（噪音），最终使模型达标。

除了以上关于如何提高Robust Universe Return和剔除噪音的方法，作者对Alpha中性化处理以及选择短周期（如5天和22天）来增强Alpha信号的讨论也对我深入理解因子复现过程有很大帮助。可惜复刻后20-22年的表现达不到可以提交的标准，我也暂时没有想到提高IS ladder sharpe的方法，但还是强烈推荐这篇帖子给其他研究者阅读。

---

### 评论 #116 (作者: XH12546, 时间: 2年前)

**Task:1**

![图片](images/img_8be01d61db.png)  ![图片](images/img_7ab31d2909.png)

存在的问题：虽然使用了多线程进行数据获取，但模拟的发送仍然是按顺序进行的，未充分利用并行性能。

总结：1.通过随机洗牌DataFrame，增加了模拟发送的随机性;2.使用了函数封装和模块化设计，提高了可读性和可维护性;3.通过异常处理和延时机制，增加了代码的鲁棒性，使其能够更好地应对可能出现的问题。

**Task2:**

我阅读的论文题目是：Duration-Driven Returns久期驱动型回报

[Duration-Driven Returns by Niels Joachim Gormsen, Eben Lazarus :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3359027)

在这篇论文中，作者提出了一个基于久期的解释，旨在揭示主要股票因子（包括价值、盈利能力、投资、低风险和支付因子）溢价背后的谜题。文章通过投资于近期内获得大部分现金流的公司来解释这些因子的表现，并认为这或许是由于对近期现金流的溢价所致。

首先，作者明确了股票因子（价值、盈利能力、投资、低风险和支付因子）投资于在近期内获得大部分现金流的公司的特性。这种特性可能引发对近期现金流的溢价，从而影响这些因子的回报。通过对单一股票股利期货数据的分析，作者发现，在公司内部，个别现金流的预期CAPM阿尔法随着久期的缩短而减小。这一结果有力地支持了他们的基于久期的解释框架，表明投资于近期现金流的公司可能获得更高的回报。

在更为具体的分析中，作者通过估计CAPM betas，将月度回报对市场回报进行回归，并考虑市场滞后项，来验证他们的观点。为了简化模型，他们强制规定了最后三个滞后项具有相同的斜率参数。研究结果显示，阿尔法与公司的其他特征（如价值、盈利能力、投资、低风险和支付）无关，而与久期有关。这进一步强调了久期在解释股票因子溢价中的重要性，排除了其他特征的影响。

此外，作者详细介绍了他们对到期收益率beta的计算方法，使用了平均beta来衡量给定条带剩余寿命的期望阿尔法。这一方法使得他们能够更精确地理解股票因子溢价与久期之间的关系。

总结：这篇论文为投资者和金融从业者提供了一种新的视角，揭示了久期对主要股票因子溢价的影响。通过对股利期货数据的独特运用，成功解开了股票市场中一个重要而复杂的谜题，为未来的投资策略和市场理解提供了有价值的参考。

---

### 评论 #117 (作者: WH24469, 时间: 2年前)

**必做1：**

1.提交前：

![图片](images/img_9f2b5c5a9e.png)

2.提交后

![图片](images/img_cad4d8bc28.png)

3.连续不断提交：

![图片](images/img_3e8c7f4817.png)

目前采用方法为使用for循环从始至终将全部数据都遍历并带入表达式中，如果提交失败就跳过，并显示fail；如果遍历程序中断，也可以从中断的index重新开始，但对于与表达式适配的数据类型的判断还需进一步完善，现在还无法直接提取适配的datasets。第二个问题就是遍历速度较慢，由于没有使用多线程，将全部数据遍历完所需时间较长，而网站在4hour后会自动断开，代码需要构建实时判断连接状态模块，并在断开时自动重连。

4.总结与反思：

（a）对于代码效率，由于采用for循环的方法，效率较低，采用多线程将节省更多的时间，对于数据的选取没有针对性，全部数据都遍历一遍虽然利于研究哪些数据更适合表达式，但花费的时间较多。

（b）Debug_1，当限制总的提交数量total_wanna_sim_num时，程序设定的是当sim_n 到达这个数字时，程序停止，但真正运行时，sim_n超过了total_wanna_sim_num程序仍然在运行。

![图片](images/img_cebb455e41.png)

修改后代码结果如下图：

![图片](images/img_b3195b51d0.png)

成功解决问题并能获取到程序停止时的datafields名字。

（c）Debug_2，原先的框架并没有获取出每个datafields的is_result的DataFrame，调整框架后，结果如下：

![图片](images/img_5c4e8dd1db.png)

可以看到anl11_2_2e这个datafields的is_result_df。

（d）模板适配的数据类型：

由于模型较简单，且原模型是用于衡量市盈率的，所以适配的数据多属于anl14及anl15类的数据，如下图：

![图片](images/img_a031da5cff.png)

![图片](images/img_a73fae5d62.png)

![图片](images/img_112ccc5b8f.png)

![图片](images/img_f05e87b2f8.png)

（d）模板改进方向：

![图片](images/img_048b244a33.png)

![图片](images/img_d7e5dd4871.png)

目前的模板过于简单，只是求出现值与两年前的值的差值后进行平滑，Sharpe和Fitness都不符合要求，模板基本思想是偏向于基本面类的，那么是否可以考虑融合其他模型，例如CAPM模型等进行优化。

**必做2：**

我阅读的文章是： [【方正金工】显著效应、极端收益扭曲决策权重和“草木皆兵”因子——多因子选股系列研究之八 - 研报 - 一起量化 17quant.com](https://www.17quant.com/post/%E3%80%90%E6%96%B9%E6%AD%A3%E9%87%91%E5%B7%A5%E3%80%91%E6%98%BE%E8%91%97%E6%95%88%E5%BA%94%E3%80%81%E6%9E%81%E7%AB%AF%E6%94%B6%E7%9B%8A%E6%89%AD%E6%9B%B2%E5%86%B3%E7%AD%96%E6%9D%83%E9%87%8D%E5%92%8C%E2%80%9C%E8%8D%89%E6%9C%A8%E7%9A%86%E5%85%B5%E2%80%9D%E5%9B%A0%E5%AD%90%E2%80%94%E2%80%94%E5%A4%9A%E5%9B%A0%E5%AD%90%E9%80%89%E8%82%A1%E7%B3%BB%E5%88%97%E7%A0%94%E7%A9%B6%E4%B9%8B%E5%85%AB.html)

此篇文章首先考虑一个常见的月度反转策略，即常用的20日收益率alpha，该传统反转alpha的逻辑认为，过去20天里，收益率相对较高的股票，其未来表现会相对较弱，而收益率相对较低的股票，其未来表现相对较好。因此如果采用20日收益率的传统反转因子来进行选股，投资者会买入过去一个月收益较低的股票，类似于反转alpha，但是这一思想会使投资者将相邻两个交易日的alpha赋予相同的权重，这有悖于最初逻辑，所以“原始惊恐度”alpha作为对传统alpha的优化，同时也衡量市场对这个标的价格的过度反应程度，其放大了常用的20日收益率alpha的时间颗粒度，考虑每个交易日交易者的过度反应程度。

文章首先计算“惊恐度”alpha，基于“惊恐度”构建多样的加权决策分，利用决策分的移动均值和标准差的等权求和来衡量每个交易日过度反应程度：

- 将每日股票收益率（今收/昨收-1）直接作为当日股票的决策分。
- 将每日的“惊恐度”与每日的收益率相乘，得到加权调整后的决策分，简称“加权决策分”。
- 每月月底，分别计算过去20个交易日的“加权决策分”的均值和标准差，分别作为对“20日收益率因子”和“20日波动率因子”的改进，分别记为“惊恐收益”因子和“惊恐波动”因子，并将二者等权合成为“原始惊恐”因子。

Alpha Idea：文章中的原始惊恐度利用的是收益率数据，而决定收益率的一个重要因素包括成交额，且成交额中包含丰富的信息，这些信息收益率是无法单独体现的，所以考虑将收益率换成成交额，构建一个新的衡量市场情绪的alpha。文章周期统一采用20个交易日，属于中短期alpha，而对于反转，有大周期和小周期的反转，参数飘逸无法把握，是否能剔除该参数带来的不稳健性。

---

### 评论 #118 (作者: BL43673, 时间: 2年前)

TASK1

![图片](images/img_90241e882a.png)

![图片](images/img_538dee3196.png)

主要是参考了【Alpha灵感】新闻动量文章启发的反转策略实现这篇文章的模板，尝试了sentiment相关的不同datafield，找到效果最好的几个然后调整了一下中性化的方法，最终得到了一个可以提交的alpha。 ![图片](images/img_03e772778a.png) 一开始是用的每次回测十个alpha的方法，结果回测2000次花费了五个多小时，后面询问chatgpt+查看论坛之后学习使用了多线程，现在2h10min就能完成2000次测试。中间遇到过一些多线程中tqdm卡住无法继续以及缺少限制使代码进入死循环无法结束等问题，但都通过各种方法解决了。

之后希望能继续精进一下我的回测框架，争取把网页上能做的操作都用api实现一遍。

TASK2

我看的文章是开源金工组的《大小单重定标与资金流因子改进》 [大小单重定标与资金流因子改进 | 开源金工 (qq.com)](https://mp.weixin.qq.com/s/0FRlMiZkJXihzGi9LaTofw)

最基本的资金流因子构造方法如下：

![图片](images/img_bafdae96e8.png)

我自己也在brain平台尝试了最基本的NIR，但我可能对英文的datafield理解存在一些偏差，我并不知道我使用的datafield是不是对的......

![图片](images/img_27dbf2a109.png)

不过确实是有效果，但Sub_Universe_Sharpe无法满足要求。

研报中还介绍了如何用MOD方法去净化资金流，消除alpha中的反转效应，通过用当日ret对ln(B/S)回归得到的残差重新分配买卖的比例，来完成MOD方法。

![图片](images/img_8aaddf5ab6.png)

目前因为时间原因还没有尝试使用该方法，如果有效的话可能就可以获得一个可以提交的alpha了。

但在这里我有疑问：这样子使用残差重新分配买卖单为什么就能排除掉alpha中的反转因素呢？文章中好像也没特别阐明。

另外，文章中还提出重新划分大小单，文章中认为以2万为界限划分大小单是最有效的。但是我目前在平台的数据中好像没有找到相关的数据，等有空再去翻找一下。

---

### 评论 #119 (作者: WL13229, 时间: 2年前)

[BL43673](/hc/en-us/profiles/18478216550679-BL43673)

我尝试将您的问题和原文输给GPT，得到了如下的答案

> 文章提到的使用残差重新分配买卖单以排除Alpha中的反转因素，实际上是基于一种统计方法来分离和剥离因子中的特定成分。这里的主要思想是利用截面回归模型来识别并分离出资金流向数据与股票未来涨跌幅之间的关系，尤其是去除那部分因为市场反转趋势而产生的Alpha效应。
> 简而言之，通过回归分析，文章尝试将资金流向的影响分解为两部分：
> 1. 与股票未来涨跌无直接关系的部分，即所谓的“纯净”Alpha部分，反映了主力资金流向本身对股票未来价格的预测能力；
> 2. 与股票未来涨跌有关的部分，主要是市场的反转因素，比如说因为股票价格短期内涨得过快而可能面临的回调压力。
> 通过回归分析，可以用来预测股票涨跌的独立变量（比如资金流向指标）与股票实际涨跌幅之间的关系被量化和识别。回归模型的残差部分（即实际观察值与模型预测值之间的差异）被认为是剥离了已知影响因素（比如反转趋势）之后的纯净效应。因此，将基于残差调整的买卖单数据用于进一步的分析和因子构建，理论上可以得到一个更为净化的、专注于捕捉主力资金流动性影响的Alpha因子。

---

### 评论 #120 (作者: YW65260, 时间: 2年前)

**必做1：**

截图1： ![图片](images/img_847092c49f.png)

截图2：

![图片](images/img_337546d018.png)

（由于截图1 忘记从一开始算的时候截了，所以这个差值少了些）

体会：在课程之前对于python还有点生疏很多语句都是现学现用，结合老师们上课的分享以及评论区很多的优秀作业和ChatGPT的帮助，完成了代码的学习、debug和提交。由于时间仓促，目前我做的只是完成了流程，包括评论区说的各种优化和多线程的处理方式我还要继续改进。这里我选取的alpha模板是“ts_mean(rank(x),20)”

**必做2：**

我阅读的论文是：量化研究推荐论文中的“ESG Preference, Institutional Trading, and Stock Return Patterns”

背景：ESG评价体系可以帮助投资者和企业更全面地评估企业的绩效和价值观。这里ESG分为3个模块分别是环境E、社会责任S、管理G。所以ESG报告并不仅仅是财报，同样也是评价企业对社会可持续发展的概览，可以形成了对公司更全面的评价。

主要内容：本文探讨了ESG偏好对机构交易和股票收益模式的影响，发现ESG偏好能显著提高机构交易者的收益，研究SR机构持股与股票对收益公告反应不足的关系，使用标准化意外收益(SUE)和复合定量信号(SYY)作为关键指标。结果显示，SR机构持股越高，股票越倾向于对收益公告反应不足。

方法：使用ESG、SR_IO和SYY评分进行股票分类和排序，首先，根据SR_IO（社会责任投资机构持股比例，反映某只股票被社会责任投资机构看好的程度）评分对股票进行排序，将股票分为三个ESG组：低ESG组、中ESG组和高ESG组。对于高SR_IO股票，低估股票的表现优于高估股票，且高ESG组的表现最为显著。而在低SR_IO股票中，未发现误定价信号与回报之间的显著关系。这些发现支持了SR_IO作为SR投资者评估股票吸引力的更有效指标的观点。

其中 stock’s weekly returns：

![图片](images/img_b3ebff98e1.png)

---

### 评论 #121 (作者: BC25356, 时间: 2年前)

**必做1: 阅读 [【Alpha灵感】论文/研报合集 – WorldQuant BRAIN](/hc/en-us/community/posts/19348865150743--Alpha%E7%81%B5%E6%84%9F-%E8%AE%BA%E6%96%87-%E7%A0%94%E6%8A%A5%E5%90%88%E9%9B%86) 或者  [Research Papers for Consultants – WorldQuant BRAIN，](/hc/en-us/community/topics/12997688420247-Research-Papers-for-Consultants) 选择一个你感兴趣的Alpha作为模板,并实现对该模板的1000次以上回测。**

**模版：**

```
group_rank(datafield, industry)
```

**前：**

```

```

**后：**

```

```

**连续性（不中断）：**

```

```

**必做2:** 阅读👉 [量化研究推荐论文 – WorldQuant BRAIN](/hc/en-us/community/posts/21004691882135-%E9%87%8F%E5%8C%96%E7%A0%94%E7%A9%B6%E6%8E%A8%E8%8D%90%E8%AE%BA%E6%96%87) 中的任意一篇论文，或者自行寻找其他材料（如研报、论文），总结论文的核心思路和Alpha Idea **(注意不要和本帖子或论坛中已被发布的重复）**

```
Paper Title：The Rewards to Meeting or Beating Earnings ExpectationsRUL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=247435Abstract:这篇文章研究的是公司未来表现和营收预期的关系，且有两个核心结论。首先，如果公司在上季度实际营收达到或超越预计营收，这些公司会比没有做到的公司有3%的Returns（季度）提升。其次，这些公司也展现自己出色的营收管理和预期管理。Main Context：研报提出了一个概念Market Premium，它被定义成“真实市场表现”与“分析师预测表现或市场预期”之间的差值。如果这个值是正的，就叫做Earnning Surprise。其需要被捕捉，因为它可以帮助投资去找到那些未来可能高价的股票和获取回报。Data：研报使用的数据是在1983年至1997年，来自75000个公司150000个季度盈利数据。但是文中并没有提及，公司的所在国，市值，行业。所以我们在Brain上可以需要用Global Universe。Main Idea: 买入上个季度实际达到或超越预计营收的公司股票，但是我们发现如果按照研报的数据只有3%的提升，没有显著变化。所以我们进一步考虑公司的研发投入，进一步强化“未来好”的信号。思考：1. 对于没有公布Earning Performance的公司怎么办？2. 对于已经公布的是不是有做假行为？如果用多维度去衡量？3. 公布的频次如果是一年一次怎么办？4. 是不是有更多指标可以参与进来，去找到“未来好”的公司？
```

---

### 评论 #122 (作者: BC25356, 时间: 2年前)

[WL13229](/hc/en-us/profiles/12285040305687-WL13229)

您好

> Step4: 使用代码获取该类型的所有数据集和大部分数据字段（datafield)

> Step5:  **对数据进行初步处理（例如vector data需要先使用vector operator降维）** Step6 **:** 将数据字段插入模板，批量生成Alpha表达式。

对于这个vector data我有两个处理办法

法一：在datafield筛选里面只选matrix数据，直接avoid vecto数据，但是这样并不是降维处理。

法二：

- **在获得数据时处理** ：我可以在获取datafield result那一步，直接把所有vector数据进行降维处理，把其字段直接替换成统一的降维数据(vec_avg(vector data))。

- **在simulate这一步处理** ：在进行simulate之前，也就是把datafield放入regular前，对数据进行判断，如果是是vector数据，则进行降维 (Example: vec_avg(vector data))。 ****因为我是直接用API获取所有数据字段 (e.g. ern1_revenue)****  **，所以如何在simulate这一步的时候，对数据进行判断？然后通过if语句进行编写？**

我更想在simulate这一步进行判断，有代码案例吗？

---

### 评论 #123 (作者: XL87358, 时间: 2年前)

**必做1：**

1.最近的截图

![图片](images/img_794f283f1e.png)

2.simulation后的截图

![图片](images/img_00797bc2d5.png)

3.代码连续运行情况：

使用了参考模板

```
 Ts_Rank(rank(x), 20)
```

，选择基本面类型数据共计1278条datafields，回测时以10个Alpha表达式为一组，连续运行2个小时未中断并完成回测。

![图片](images/img_6168f644c8.png)

4. 总结反思：

代码效率上未使用多线程进行回测，运行效率可能还没有达到最佳，暂时还不满意，会在后续边实践边修改代码。

主要遇到了如下的bug，首先是使用alpha_id = simulation_progress.json()["alpha"]在尝试获得id的时候返回Keyerror，但单独检查alpha表达式后发现可以正常回测，经排查发现是因为账号异常登出。使用try except语句在发生错误，重新sign in()再运行回测函数，保证代码不中断。

此外，还遇到一个很有趣的bug，即使用get_datasets(s, settings)函数获取的datasets的id有重名的现象，如出现两个‘fundamental13’，我通过list做切片的方法得到需要的datasets，但因为重名创造了一些重复的Alpha表达式，因此实际系统显示的Alpha数目小于程序模拟的1200多次。（可以看到get_datasets得到的重名数据集实际上是不同的，这些数据集有什么区别呢？此外使用API get_datafields(s, dataset_id='fundamental13')无法选择重名数据集）

![图片](images/img_ac7fc0b42f.png)

调试代码的时候还参考了如下文章做了尝试：

1. [【Alpha灵感】新闻动量文章启发的反转策略实现](/hc/en-us/community/posts/19353819839639--Alpha%E7%81%B5%E6%84%9F-%E6%96%B0%E9%97%BB%E5%8A%A8%E9%87%8F%E6%96%87%E7%AB%A0%E5%90%AF%E5%8F%91%E7%9A%84%E5%8F%8D%E8%BD%AC%E7%AD%96%E7%95%A5%E5%AE%9E%E7%8E%B0)

ehat=ts_regression(returns,ts_delay({datafield},1),120);alpha=group_neutralize(-ehat,bucket(rank(cap),range='0,1,0.1'));alpha

数据类型采用了'news',  'sentiment', 'socialmedia'三种类型的数据。得到了少量高夏普的alpha，但数据字段的coverage不够，无法通过 [IS ladder Shar](/hc/en-us/articles/6726865162903) pe测试。

**必做2：**

**我阅读的文章是发表在JFE上的论文：《Good and Bad Uncertainty: Macroeconomic and Financial Market Implications》**

该文章认为宏观经济的不确定性可以分解为“好”和“坏”两种波动性成分，并将其与总增长和资产价格相关联。好的不确定性预示着未来经济活动的增加，如消费、产出和投资，并与估值比率呈正相关，而坏的不确定性预示着经济增长的下降，并压低资产价格。文章以90年代美国科技股泡沫和08年金融危机中雷曼公司倒闭为例，在第一种情况下，一个普遍的观点是，互联网将提供许多积极的增长机会，从而促进经济发展，但究竟有多少是未知的。这种情况称为“好的”不确定性。另一方面，第二个案例标志着全球金融危机的开始，随着随后出现的许多破产案例，人们知道经济状况正在恶化——然而，还是不清楚恶化了多少?这种情况是“糟糕”不确定性的上升。论文基于美国宏观消费数据，采用Long Run Risks model of Bansal and Yaron (2004)将消费数据的冲击拆解为好与坏两部分。

论文主要涉及的数据：宏观数据部分包括消费和产出数据，R&D投入、存量数据，工业生产数据（supplement the annual data on these macroeconomic measures with the monthly data on industrial production from the Federal Reserve Bank of St. Louis.）

“好”与“坏”的计算方法：y代表宏观变量（e.g., industrial production, earnings, consumption）∆y 代表 demeaned growth rate in y（zero-mean之后的growth rate）

![图片](images/img_7f749d6324.png)

Alpha Idea：我查看了brain平台的宏观数据集，似乎并没有与上述相关的数据字段。但可以借用论文的思想，即不确定性可以以好与坏相区别，在“好”的情况下，波动性越大，股票的预期收益可能就会越高；相对的，在“坏”的情况下，波动性的上升可能意味着股票正在进入一个坏局面。

使用平台简单实践一下：假如把good = ts_mean(returns, 2) < ts_median(returns, 20); 定义为一个好事件（某种反转信号？）那么采用good? rank(ts_std_dev(returns, 20)): -rank(ts_std_dev(returns, 20))

可以看到结果并不理想，换手率相对过高，可能相对于论文的成果，在概念定义、条件设置上过于简单，还有很多可改进空间。后续会继续沿着对不确定性内部结构进行分解的思路继续改进。

![图片](images/img_de231c5147.png)

---

### 评论 #124 (作者: WL13229, 时间: 2年前)

[JK19915](/hc/en-us/profiles/9476915930519-JK19915)

您好，请将作业发布至本评论区，无需另开新帖。我已为您复制粘贴以下您内容。

“

**我阅读的文章是：**  **ESG Preference, Institutional Trading, and Stock Return Patterns**

这篇论文探讨了社会责任投资机构（Socially Responsible，简称SR）持股对股票价格效率及市场信息反应延迟的影响，尤其是当市场环境中的资金流动性较低时，由这些机构大量持有的股票在应对市场信息变化时表现出更大的价格延迟。

具体来看，研究首先构建了一个模型来衡量股票回报受滞后市场回报影响的程度，即Price Delay（价格延迟），并采用每周回报数据计算每家公司在历年内的这一指标。结果表明，社会负责任投资机构所持股份越多的公司，在后期样本期间（2004年至2016年）对市场信息的响应速度较慢，表现为Price Delay增大；而在早期的安慰剂期则没有观察到类似效应。

进一步分析发现，当将样本细分为高SR持股与低SR持股两类时，在资金流动性较低的时期，SR持股对Price Delay的影响更为显著。这意味着在资金流动性受限的情况下，SR机构持有股份较多的公司其股价对市场新信息的调整更迟缓。

此外，论文还基于不同的评分体系如SUE和SYY等对公司进行排序，并对比不同SR持股水平的股票组合的风险调整后收益（Alpha）。结果显示，对于高SR持股的股票，基于SUE或SYY评分形成的多空投资组合具有显著的Alpha值，这反映了这些股票存在可预测的定价偏差，而低SR持股股票的Alpha值则不显著。这种差异可能源自于SR机构持股比例较高的股票由于潜在的卖空限制而导致定价失衡未能及时纠正。

**A**  **lpha idea:** 根据SUE或SYY等量化指标对公司进行排序，构建一个多空投资组合，长仓持有那些SR机构持股比例高且评分良好的公司股票，同时短仓持有同等数量的SR持股低但评分较差的公司股票。由于高SR持股公司的定价偏差可能导致市场对其价值评估存在延后，这样的策略有可能在一段时间内获取Alpha收益，特别是在市场条件不利于快速价格发现的时候。”

---

### 评论 #125 (作者: WL13229, 时间: 2年前)

[BC25356](/hc/en-us/profiles/13921805253911-BC25356)

您好，您关于论文的描述过于简短，请提供更多的细节。量化慢工出细活，欲速则不达。

关于您对代码的问题。我们在API帖子中关于datafield的获取代码，返回的dataframe中，是涵盖了数据类型（如vector，matrix等）的，建议通过此进行判断。

---

### 评论 #126 (作者: WL13229, 时间: 2年前)

[XL87358](/hc/en-us/profiles/20580060743447-XL87358)

可否进一步阐述该论文涉及到的数据？

---

### 评论 #127 (作者: JZ65525, 时间: 2年前)

大家好，这是我Case1的内容：

在simulation 1000 次之前我的状态是这样的：

![图片](images/img_c38da00279.png)

Simulation1000次后: ![图片](images/img_55b25b45a6.png)

以下是连续不断simulation 1000次的状态：

![图片](images/img_289ce6ba33.png)

总结反思：

首先，关于 **代码效率** ，我们尝试通过并发执行的方式来提高模拟运行的速度。通过使用 `concurrent.futures` 模块中的 `ThreadPoolExecutor` ，能够在多个线程中并行发送HTTP请求，这大大提高了执行模拟的速度。然而，并发也引入了复杂性，特别是在管理HTTP会话和处理异常时。在这个过程中，理解每个任务如何独立运行以及如何有效地同步和管理这些任务的结果变得至关重要。

其次，我的 **debug经历** 强调了仔细检查错误消息的重要性。例如，当遇到 `SSLError` 时，初步可能只是简单地认为是网络问题。然而，通过细致地检查错误类型和消息，可以发现是SSL协议或证书方面的问题。这要求对底层网络协议有一定的理解，并知道如何调整请求以满足特定服务器的安全要求。

关于 **模板适合的数据类型** ，当前的模板设计主要针对的是处理网络请求和响应的场景，特别是与REST API交互时。这适用于数据类型为JSON的场景，因为这是Web API最常用的数据交换格式。对于需要处理大量网络请求和期望异步处理这些请求的任务，这个模板特别合适。

最后，考虑到 **模板的改进方向** ，虽然当前的实现提高了任务执行的效率，但仍有改进空间。例如，错误处理可以更加细化，以便更好地处理和重试失败的网络请求。此外，当前模板在处理TLS/SSL配置方面比较静态，引入更灵活的配置选项可以让模板更加通用。进一步地，引入更高级的并发控制机制，如异步IO（ `asyncio` ），可能会进一步提高效率，尤其是在IO密集型任务中。

通过这次经历，我深刻认识到在设计和实现并发网络请求处理时，既需要关注效率和速度，也不能忽视安全性和错误处理的重要性。未来，继续探索更高效的并发模式和更精细的错误处理机制将是提升代码质量和性能的关键方向。

---

### 评论 #128 (作者: JZ65525, 时间: 2年前)

大家好，这是我Case2的内容：

我阅读了文章《Online reviews can predict long-term returns of stocks》。本文通过分析机构投资者的决策型交易，探讨了机构投资者的信息优势对股票价格效率的影响。研究发现，具有未来收益相关信息的投资者会利用这些信息来策略性地调整过去的决策，进一步将机构交易分为决策型交易和隐含交易。决策型交易能够正向预测未来的股票收益和盈余惊喜，而隐含交易则负向预测收益。此外，机构投资者进行决策型交易的倾向以及决策型交易的表现在顶部20%的机构中具有很高的持续性。

通过使用1980至2017年间的季度13F申报数据，研究发现决策型交易在跨机构到股票层面均强烈预测未来的股票收益，顶层分位数的决策型交易股票在接下来的三个月内表现超越底层分位数股票2.59%（年化10.77%）。相比之下，隐含交易负向预测未来股票收益。进一步分析显示，决策型交易对未来盈余惊喜有强预测能力，表明股票基本面的价格发现是机构投资者信息优势的重要来源。

研究还考察了机构投资者信息优势的持续性，发现具有信息优势的机构能够持续利用这一优势。通过分析决策型交易在机构层面的持续性，以及决策型交易的表现在未来几个季度的持续性，结果表明一部分机构投资者能够持续获得信息优势，并专门从事有信息量的交易。

本文的发现不仅揭示了机构投资者在资本市场中的信息角色，还对理解信息如何被纳入股票价格提供了见解。尤其是在机构投资者之间竞争加剧的更近期时段，研究强调了在竞争环境中持续获得信息优势的重要性，为未来关于机构投资者决策型交易的更多研究提供了有价值的洞察。

Alpha Idea:

根据论文的发现和分析方法，可以构造几个量化因子来捕捉机构投资者的信息优势和交易行为对股票价格的影响： 1. 决策交易因子： 描述：这个因子通过计算每个股票在特定时期内所有机构投资者的决策型交易的累积值来衡量。正值表示积极的决策型交易，可能预示着未来股价上涨，而负值则可能预示着未来股价下跌。  计算方法：对于每只股票，将所有机构的决策型交易累加，然后根据其值进行排名或分组。  2. 信息优势持续性因子： 描述：这个因子旨在捕捉那些在决策型交易中表现出持续优势的机构投资者的行为。机构在过去几个季度内表现出强决策型交易能力的股票可能持续表现良好。  计算方法：基于机构过去的决策型交易表现（如过去四个季度的平均决策型交易表现）对股票进行排名或分组。  3. 未来收益预测因子： 描述：考虑到决策型交易对未来盈余惊喜具有预测能力，这个因子基于机构的决策型交易来预测股票的未来盈利能力。  计算方法：利用机构的决策型交易强度和方向来估计每只股票的未来盈利能力，然后根据预测的盈利能力对股票进行排名或分组。

---

### 评论 #129 (作者: BH42089, 时间: 2年前)

Task1:

1. ![图片](images/img_b3ec04fbfa.png)

2. ![图片](images/img_ecf578b3fc.png)

3. ![图片](images/img_fdbbb857ac.png)  ![图片](images/img_bcbd2502a1.png)

1. 以前在ACE比赛中搓过一个简单的world quant brain平台SessionManager，所以就在此基础上继续开发和debug了。

代码效率方面，经过我在本地的测试，从提交一个Alpha到可以收到测试结果大概需要15-30s时间。为了提高回测效率，代码中采用了线程池，从而并行测试Alpha，并且任务之间异步，不需要等待一个批次的Alpha测试完成后才测试下一批。为了尽可能提高回测效率，代码中直接将线程数设置为10（brain平台最大同时回测数量）。

为了程序可以长时间运行，用于发送测试数据并获取结果的函数采用重试机制并加入大量异常捕获代码。通过配置logger的handler可以将错误信息和运行情况信息写入log文件。

代码在小批量测试时可以正常运行，但是在连续测试2000个Alpha时，出现了一致没有办法定位和解决的bug。我首先采用” 【Alpha灵感】新闻动量文章启发的反转策略实现”的因子作为模板

通过替换`snt_buzz_ret`，`vhat`，`cap`以及时间窗口长度，构建出了2000个因子表达式。替换值可选参数的筛选方法为：1.`region=’USA’, universe=’TOP3000’, delay=1, search=f”{variable_name}”`，2.相同数据类型(`type=’Matrix’`)，3.因子数量（’alphaCount’）最多的前10个。通过筛选出的三组长度为10的可选字段，以及时间窗口d的可选值为[60, 120]，我们可以通过`itertools.product`构建出2000个不重复的因子。

接下来将因子表达式结合测试参数生成测试数据，并使用前面提到的代码回测
。然而在测试完这一批因子后，平台上显示我只测试了四百多个新因子。最终我发现问题出现在发送的因子表达式与获得的测试结果中的表达式不一样。

以下发送测试数据并获得测试结果的代码片段

![图片](images/img_611175d502.png)

在经过两天debug仍没有没有修复。我猜测问题可能出现在因子上，于是我随手写了个简单因子模板，采用相同的数据字段生成2000个因子表达式。这批因子的测试正常，可以正常地跑完2000个因子。由于接近ddl，所以就没有为第二批因子精心挑选模板和字段。

![图片](images/img_0e927b1917.png)

Task2：

**我阅读的文章是PV1：**  [Overnight Returns, Daytime Reversals, and Future Stock Returns](/hc/en-us/community/posts/14830168587287-Research-Paper-22-Overnight-Returns-Daytime-Reversals-and-Future-Stock-Returns)

这篇论文研究股票市场中的隔夜回报率日渐回报率反转现象，正向的夜间回报率紧随其后的是负向的日间回报率反转，论文将根据这一现象搭建因子预测股票回报率。当一个月内出现较高频率的正向夜间回报率后紧跟着负向日间回报率反转时，表明投资者之间存在比平时更激烈的对抗，其中夜间交易者可能是噪声交易者，而日间交易者则是套利者。研究结果表明，这种日常对抗的强度预测了跨部分的更高未来回报。论文构建了衡量这种日常对抗强度的因子，并且发现这些因子可以用于预测股票收益。

论文研究的数据集是美股1993/05到2017/12的价格数据和对应公司的财务数据。

论文的日内收益为(open-close)，日间收益为(close-close)收益。通过计算每个月内正向夜间回报后紧接的负向日间回报的频率，可以衡量投资者间日常对抗的强度，进而预测股票的未来回报。

---

### 评论 #130 (作者: SW49904, 时间: 2年前)

**Task 1**

*模拟前*

![图片](images/img_ecfdbc3be4.png)

*模拟后*

*![图片](images/img_039b9fb96a.png)*

具体工作如下：

- Step 1-4，我按照平台提供的API进行了函数封装以便于后续的运行，构造了 *log_in ()，check_alpha (id, s)，get_datafields ()* 这样的函数，为后续simulation做准备。这里我直接用的Equity的例子，因为数据集和字段太多所有没有什么探索思路，希望得到一些启发。此外想问总共有哪些instrument_type，这个如何查看？
- Step 5，这里我的操作比较简单，只是按照type对数据集进行了切分(matrix, vector, group)这三类，后续针对这三种类型选择不同的operators。我这里分别对matrix和vector各跑了前1000个字段数据。
- Step 6-9，首先按照示例我构造了 *simulate_alpha(express,s)* 的函数，这里主要是对simulation模板的优化

*添加一个防止API连接中断的部分->*

```
while True:        simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=simulation_data)        if simulation_response.status_code == 201:            #print("Sucessful")            break        elif simulation_response.status_code == 400:            print('Died')            return None        elif simulation_response.status_code == 401:            s = log_in ()            print("Re-log in")        else:            print(f"Sleeping for 20 seconds due to status code: {simulation_response.status_code}")            sleep(20)
```

*比如登陆超时，从运行记录上看是是这样的->*  ![图片](images/img_46ef70d492.png)

*添加了一个防止由于计算错误引起模拟中断的熔断代码，大部分是由于数据字段和计算公式不匹配或冲突引起的，一般数据经过分类后出现的比较少，所以我选择对于计算错误的alpha直接跳过->*

```
try:    alpha_id = simulation_progress.json()["alpha"]    return alpha_id,sexcept KeyError as e:    print("Error:", e)    print("Skipping alpha simulation.")    return None,s
```

*从运行记录上看是是这样的->*  ![图片](images/img_1eea77f678.png)

*最后模拟部分是一个简单的循环->*

```
for alpha in tqdm(vector_alpha_list):  alpha_id,s = simulate_alpha(alpha,s)
```

*从运行记录上看是是这样的->*  ![图片](images/img_d452e81f02.png)

**额外部分**

我根据checks的信息构造了一个筛选潜力因子的函数，函数首先计算每个检查项的限制差异，并将结果存储在一个新的列中。然后，它计算失败检查的数量。接着，函数检查每个检查项的限制差异是否都小于容忍度因子的限制差异，并在满足条件时将 alpha 的 ID 和失败检查的数量添加到结果 DataFrame 中作为潜力因子。

```
def wether_potential (id, checks_df, CI, potential_df):  checks_df['limit_diff'] = CI * checks_df['limit']  checks_df['diff'] = abs(checks_df['limit'] - checks_df['value'])  num_fail = checks_df[checks_df['result'] == 'FAIL'].shape[0]  if (checks_df['diff'] < checks_df['limit_diff']).all():    print(f"{id} has the potential")    potential_df = potential_df.append({'id': id, 'FALL': num_fail}, ignore_index=True)  return potential_df
```

**反思部分**

我发现我跑的1000次模拟的字段表现都很差，也并没有表现能通过我潜力因子的函数。如果没有一个好的表达式模板，我认为暴力的测试太低效了，希望得到更多的建议，如何有一个好的挖掘因子的思路？此外，我想知道我挖掘潜力因子的思路是否正确，即使我把容错区间调整到CI=0.5，在这次任务的2000次模拟中我也没有筛选出来有潜力的因子。

**Task 2**

我选择的论文： [https://support.worldquantbrain.com/hc/en-us/community/posts/15238244743447-Research-Paper-35-Profitability-R-D-Investments-and-the-Cross-Section-of-Stock-Returns](/hc/en-us/community/posts/15238244743447-Research-Paper-35-Profitability-R-D-Investments-and-the-Cross-Section-of-Stock-Returns)

总结如下：

- 研发强度与股票收益关系探究：使用交叉截面回归分析，研究了研发支出（rd_expense）、毛利率（mdl175_grossprofit）、以及研发与市值比（R&D-to-market value，简称RDM）等因素对随后股票收益的影响。
- 毛利率对预测能力的影响：发现毛利率和研发支出水平（R&D-to-gross profits）会削弱RDM变量的预测能力。当以研发/资产比（R&D-to-assets）作为研发强度的代理时，毛利率仍然主导了研发支出水平的影响。
- 盈利动能的作用：引入盈利动能变量（SUE和CAR3），发现它们会降低研发强度的预测能力，但不影响毛利率的预测能力。盈利动能是未来盈利能力的早期信号，但并非驱动这一结果的因素。
- 市值的影响：报告季度盈利的公司和报告非零研发支出的公司在市值上存在差异，对于报告非零研发支出的大型公司，预测能力下降。
- 统计结果：在控制了R&D-to-assets和R&D-to-gross profits的情况下，大型公司的高毛利率会带来更高的平均收益，而R&D-to-market value变量似乎捕捉到了过去表现较差股票的影响。

---

### 评论 #131 (作者: RW67501, 时间: 2年前)

1. 刚开始simulation数目为559

![图片](images/img_7399d6ce55.jpeg)

2. 后来的simulation数目为770个

这里有bug未解决，我其实设置的代码里是跑了1290次，最后在网页端统计的Alpha数量只增加了约200个，并且有8个Decommissioned alpha。这种情况我在评论区也看到过别的用户出现过，我怀疑是有的Alpha虽然没有报错，但是这些Alpha丢失了。后续debug我会查看Alpha的具体状态

![图片](images/img_120b989a22.jpeg)

3. 每个线程10次simulation，连续跑完129个线程

![图片](images/img_e68b37b36e.jpeg)

4. 反思

本周我参考的模板来自  [https://support.worldquantbrain.com/hc/en-us/community/posts/19353819839639--Alpha%E7%81%B5%E6%84%9F-%E6%96%B0%E9%97%BB%E5%8A%A8%E9%87%8F%E6%96%87%E7%AB%A0%E5%90%AF%E5%8F%91%E7%9A%84%E5%8F%8D%E8%BD%AC%E7%AD%96%E7%95%A5%E5%AE%9E%E7%8E%B0](https://support.worldquantbrain.com/hc/en-us/community/posts/19353819839639--Alpha%E7%81%B5%E6%84%9F-%E6%96%B0%E9%97%BB%E5%8A%A8%E9%87%8F%E6%96%87%E7%AB%A0%E5%90%AF%E5%8F%91%E7%9A%84%E5%8F%8D%E8%BD%AC%E7%AD%96%E7%95%A5%E5%AE%9E%E7%8E%B0)  “【Alpha灵感】新闻动量文章启发的反转策略实现”，表达式为：

```
ehat=ts_regression(returns,ts_delay(snt_buzz_ret,1),120);alpha=group_neutralize(-ehat,bucket(rank(cap),range='0,1,0.1'));alpha
```

因此我选用的category为News data，根据Brain论坛上提供的代码模板，我先拿到New data下所有的dataset对应的id，然后通过id拿到所有datafield的数据。这样操作会得到一些完全重复的data id，通过去重复后共有1299个不同的data id，之后即可代入模板中替换snt_buzz_ret重复simulation。

开始没有对vector数据做操作，直接代入模板中报错。后来对数据类型为vector的数据先进行vec_avg()操作，就可以解决刚刚的bug。

另外运行中有时候存在账户登出的问题，需要try-except防止登出造成运行中断，实测1290次simulation的时候还没有登出。

使用multi-simulation的方法可以大大提高代码运行效率，可以同时跑10个simulation，大概跑完10个simulation需要50s，最终跑完1290个用了2个小时。

最终获得Alphalist，为multi-simulation中children的结果即为单个Alpha的Location。后续可以通过该list获取每个Alpha的id。

![图片](images/img_69cde1e749.jpeg)

5. 改进

首先要解决消失的Alpha的问题，然后对于Alpha的后处理，performance比较进一步完善相关代码，增加代码可读性和运行速度。

6. 文献阅读

我阅读的因子日历中一个因子的索引研报，“高子剑，2020，高频价量相关性，意想不到的选股因子，东吴证券”。这里虽然是高频因子，但是我觉得在日频数据中应该也有效。

表达式为

```
pv_corr=corr(close,volume);alpha=std(pv_corr)
```

该因子考虑价量相关性波动性因子，从价格和成交量的相关性角度来提取有用的信号，而不是只考虑单一的价格和成交量。该因子也可以加入时序信息做平均和对市值做中性化处理。

---

### 评论 #132 (作者: WL13229, 时间: 2年前)

[RW67501](/hc/en-us/profiles/13836987458967-RW67501)

"我其实设置的代码里是跑了1290次，最后在网页端统计的Alpha数量只增加了约200个"

关于所谓"Alpha丢失了“的猜测是不准确的，您需要检查您Alpha的排队逻辑。如果有多个Alpha同时在跑，您需要等其他的跑完再提交。

---

### 评论 #133 (作者: MJ31525, 时间: 2年前)

![图片](images/img_e6636266bd.png)  ![图片](images/img_acc2a5fc14.png)

python simulation流程：1、获取所有的data，以data减去data行业均值为模板后取行业中性，构造alpha快速表达式；2、提交simulation后，根据返回结果，筛选具有潜力的alpha；3、调整alpha表达式根据市值，成交量等调整输出最优alpha。缺点是：只有最后大批量输出使用并行sim，效率较低；模板适应性一般，挖掘效率低；最优结果的筛选机制还不成熟。

我阅读的文章是option4：Research Paper 26: Bid and Ask Prices of Index Put Options: Which Predicts the Underlying Stock Returns?

文章以标普500虚值认沽期权为样本，发现ask价格波动率和股票未来回报的相关性比bid更强，且资产下行风险加剧时更加显著，理解的是市场下行风险增加时，做市商会卖出downside侧认沽期权后，需要卖出股票来对冲，在快速下跌的过程中，做市商卖出股票的冲击成本更高，因此需要以更高的溢价来定价downside的虚值合约。因此ask的定价一定程度反应做市商对未来的预期，使用线性模型预测后根据预测值构建alpha。

---

### 评论 #134 (作者: WL13229, 时间: 2年前)

帮 [ZL70229](/hc/en-us/profiles/17108134190999-ZL70229) 发布作业

**必做（一）**

**![图片](images/img_6406d37a1b.png)**

**![图片](images/img_28b44735aa.png)**

**![图片](images/img_177b21b0df.png)**

**一、代码效率**

**（一）操作的优化**

**命令发送时间：比起单纯手工操作，命令的发送快了n倍，且此套模板可以复用。**

**调参速度：一键修改n次模拟的参数。**

**（二）理论层面的优化**

**因子挖掘指导：可短时间根据因子在不同数据或参数下的大样本结果比较，迭代指导性更强。**

- **模拟结果**

**受限于网站的服务器访问频次，依然需要等待一段时间才能看到模拟结果。但模拟只是中途停歇，并没有中途停止，所以访问频次的限制只是增加了模拟的时长，并没有提高操作的复杂度。**

- **debug经历**

**仅出现中途输错参数及账号密码没有加引号时出现了异常。但不知道是何原因，在进行了第一次的不间断模拟后，后续每次不间断模拟在WQ brain平台只能看到一个alpha记录。**

- **模板适合的类型**

**模板提高的事输入效率，更适用于包含更多datafield的dataset的模型以及表达式更简洁的策略。**

**四、模板改进的方向**

**可以优化代码，对每个参数的进行for循环进一步增加模拟次数。**

**必做（二）**

**我阅读的文章是**  [Research Paper 04: Strategic Rebalancing](/hc/en-us/community/posts/13304175062807-Research-Paper-04-Strategic-Rebalancing)

该文章通过对60-40（股票债券投资比）资产配置方法的“买入并持有”策略与“机械再平衡”策略进行对比，认为“机械再平衡”策略相较于买入存在负凸性，相当于卖出了straddle期权组合。卖出straddle会在资产存在较大上升或下降时遭受亏损，会在资产价格仅在微小区间内变动时由于收到对手方的期权费而盈利。并进一步比较“趋势再平衡”策略，认为该策略与“机械再平衡”相反，相对于“买入并持有”策略具有正的凸性。

该论文通过两阶段的资产配置模型与实证数据分析，得到了以上结论。该论文同样指出应当注意对“买入并持有”策略在市场价格存在持续性动量时会导致风险过度集中，以及简要说明了其他几个模型。

Alpha Idea：“趋势再平衡”策略可以达到做动量策略的效果，“机械再平衡”可以达到做反转策略的效果。

---

### 评论 #135 (作者: HY95587, 时间: 2年前)

![图片](images/img_37fcd8655d.png) 从代码效率来看，应该还可以，一小时能模拟完成。但是由于运行开始时间较晚，可能无法在 9 点之前完成模拟。先上传过程中的图片。 ![图片](images/img_98a77be507.png)

![图片](images/img_9fac78220e.png)

代码效率、debug经历、模板适合的数据类型、模板的改进方向：

代码效率大概 950 alphas/h。感觉不是很理想，因为按理来说可以 10 线程 * 10 multi-sim。

debug 发现 multi-sim 不允许传刚好一个 alpha 的模拟。以及一开始拼写错误中性化项目的单词，导致整个程序卡死。之后对 400 error 的报错报文，都进行了处理和输出，从而及时找到错误。

目前使用的是 ts_rank(rank(x), t) 的模板。我枚举了中性化、delay、decay、USA TOP ??? 这几种设置，x 目前使用了 close, open, vwap；此外调整了时间 t，以及 ts_rank 可能调整为 ts_zscore。

之前在 alpha example 见过类似的因子？好像是比较适合量价数据类型。ts_rank 对时间变化很敏感，不适合基本面的一些变化很慢的数据，以及新闻之类大部分时候为 0 但少部分时候很多的数据。

模版可以考虑稍微复杂一点。现在的模版只能用单一的数据集，可以考虑多个数据集的 ts_regression 或者投影之类的，这样可以删除掉数据的一些 beta 成分，生成更有效的 alpha。

**我阅读的是 option62: Testing for Asset Price Bubbles using Options Data"**

这篇文章提出了一种使用期权数据来评估资产价格泡沫的方法：

文章的目标是利用期权的前瞻性质来探测资产价格泡沫。通过分析看涨期权和看跌期权之间的价格差异，来作为是否存在资产价格泡沫的指标。

- **基本思路** ：期权作为一种衍生金融工具，其价格反映了市场对于未来资产价格走势的预期。理论上，如果资产存在价格泡沫，那么这种预期会在期权定价中表现出来，尤其是看涨期权和看跌期权价格的差异。
- **具体方法** ：
  1. **模型选择** ：选择一个灵活的参数模型（例如G-SVJD模型）来模拟资产价格的演变。
  2. **数据输入** ：使用看跌期权的数据来评估资产的基本价值。文章认为看跌期权的定价较为接近资产的真实基本价值，因为它们通常包含较少的投机性预期。
  3. **泡沫估计** ：将看涨期权的市场价格与从看跌期权得出的基本价值进行比较。价格差异较大时，可能表明存在资产价格泡沫。

- **Alpha Idea** ：根据文章提出的模型和方法，可以设计投资策略来应对资产价格泡沫。在泡沫初期，可以采取跟随市场动量的策略进行投资；当预测到泡沫即将破裂时，转而采取反向策略，以期获得收益。

---

### 评论 #136 (作者: HY95587, 时间: 2年前)

![图片](images/img_0cfbe48cd3.png)  ![图片](images/img_660b1edbbf.png)

---

### 评论 #137 (作者: JC15033, 时间: 2年前)

您好，这段代码的报错一直是如下：

```
Failed to submit alpha: 405 Client Error: Method Not Allowed for url: https://api.worldquantbrain.com/alphas
```

请问要怎么修复？

import requests
import pandas as pd
import json
import time

username = "XXX"
password = "XXX“

# Function to handle authentication and maintain session
def sign_in():
    s = requests.Session()
    s.auth = (username, password)

while True:
        try:
            response = s.post(' [https://api.worldquantbrain.com/authentication](https://api.worldquantbrain.com/authentication) ')
            response.raise_for_status()
            print("Successfully signed in")
            break
        except requests.exceptions.RequestException as e:
            print(f"Failed to sign in: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

return s

# Function to generate an alpha
def generate_alpha(expression: str, universe: str = 'TOP3000', region: str = 'USA'):
    return {
        'expression': expression,
        'settings': {
            'universe': universe,
            'region': region
        }
    }

# Function to submit an alpha
def submit_alpha(session, alpha_data):
    url = ' [https://api.worldquantbrain.com/alphas](https://api.worldquantbrain.com/alphas) '
    try:
        response = session.post(url, json=alpha_data)
        response.raise_for_status()
        alpha_id = response.json()['id']
        print(f"Alpha submitted successfully. Alpha ID: {alpha_id}")
        return alpha_id
    except requests.exceptions.RequestException as e:
        print(f"Failed to submit alpha: {e}")
        return None

# Example alpha expression
alpha_expression = "1-rank(high/low)"

# Example usage:
session = sign_in()
if session:
    alpha_data = generate_alpha(alpha_expression)
    alpha_id = submit_alpha(session, alpha_data)
    if alpha_id:
        # Simulate alpha
        simulation_data = {
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY',
                'region': 'USA',
                'universe': 'TOP3000',
                'delay': 1,
                'decay': 15,
                'neutralization': 'SUBINDUSTRY',
                'truncation': 0.08,
                'pasteurization': 'ON',
                'unitHandling': 'VERIFY',
                'nanHandling': 'OFF',
                'language': 'FASTEXPR',
                'visualization': False,
            },
            'regular': 'close'
        }
        simulation_response = session.post(' [https://api.worldquantbrain.com/simulations](https://api.worldquantbrain.com/simulations) ', json=simulation_data)

if simulation_response.status_code == 202:
            simulation_progress_url = simulation_response.headers['Location']
            print("Simulation in progress...")
            while True:
                simulation_progress = session.get(simulation_progress_url)
                if simulation_progress.status_code == 200:
                    simulation_status = simulation_progress.json().get('status')
                    if simulation_status == 'SUCCESS':
                        print("Alpha simulation successful")
                        break
                    elif simulation_status == 'FAILED':
                        print("Alpha simulation failed")
                        break
                    else:
                        print(f"Simulation status: {simulation_status}")
                        retry_after = simulation_progress.headers.get("Retry-After")
                        if retry_after:
                            print(f"Sleeping for {retry_after} seconds...")
                            time.sleep(float(retry_after))
                        else:
                            print("Waiting for simulation to complete...")
                            time.sleep(10)
                else:
                    print(f"Error fetching simulation status: {simulation_progress.status_code}")
                    break
        else:
            print(f"Failed to start simulation: {simulation_response.status_code}")

---

### 评论 #138 (作者: WL13229, 时间: 2年前)

[JC15033](/hc/en-us/profiles/18243328791959-JC15033)

这个alpha还没有到submit的阶段所以使用

```
https://api.worldquantbrain.com/alphas
```

不正确。我有个建议是使用大语言模型帮助功能实现+参考ACE代码框架👉

1. ACE： [Alpha Creation Engine](/hc/en-us/articles/20786107171351-Alpha-Creation-Engine)

---

