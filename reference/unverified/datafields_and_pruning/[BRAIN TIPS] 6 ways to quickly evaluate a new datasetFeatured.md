# [BRAIN TIPS] 6 ways to quickly evaluate a new datasetFeatured

- **链接**: https://support.worldquantbrain.com/hc/en-us/community/posts/11807866133911--BRAIN-TIPS-6-ways-to-quickly-evaluate-a-new-dataset
- **作者**: KA64574
- **发布时间/热度**: 3 years ago, 得票: 188

## 帖子正文

WorldQuant BRAIN has thousands of datafields for you to create alphas. But how do you quickly understand a new datafield? Here are 6 ways. Simulate the below expressions in “None” neutralization and decay 0 setting. And obtains insights of specific parameters using the Long Count and Short Count in the IS Summary section of the results.Sr. NoExpressionInsight1datafield%coverage, would approximately be ratio of (Long Count + Short Count in the IS Summary )/ (Universe Size in the settings)2datafield != 0 ? 1 : 0Coverage. Long Count indicates average non-zero values on a daily basis3ts_std_dev(datafield,N) != 0 ? 1 : 0Frequencyofuniquedata (daily, weekly, monthly etc.).Some datasets have data backfilled for missing values, while some do not. The given expression can be used to find the frequency of unique datafield updates by varying N (no. of days).Datafields with a quarterly unique data frequency would see a Long Count + Short Count value close to its actual coverage when N = 66 (quarter). When N = 22 (month) Long Count + Short Count would be lower (approx. 1/3rdof coverage) and when N = 5 (week), Long Count + Short Count would be even lower.4abs(datafield) > XBoundsof the datafield. Vary the values of X and see the Long Count. For example, X=1 will indicate if the field is normalized to values between -1 and +1?5ts_median(datafield, 1000) > XMedianof the datafield over 5 years. Vary the values of X and see the Long Count. Similar process can be applied to check the mean of the datafield.6X < scale_down(datafield) && scale_down(datafield) < YDistributionof the datafield. scale_down acts as a MinMaxScaler that can preserve the original distribution of the data. X and Y are values that vary between 0 and 1 that allow us to check how the datafield distribute across its range.For example, if you simulate [close <= 0], You will see Long and Short Counts as 0. This implies that closing price always has a positive value (as expected!)

---

## 讨论与评论 (15)

### 评论 #1 (作者: RP25658, 时间: 2 years ago)

Please give an example of this expressionts_std_dev(datafield,N) != 0 ? 1 : 0How to interpret the results?

---

### 评论 #2 (作者: AG20578, 时间: 2 years ago)

Try to simulatets_std_dev(datafield,N) != 0 ? 1 : 0where datafield = close, sales, cashflow, and N = 20, 65, 250These three datafields have different frequency - daily, quarterly and annual. The result will be different for each N.Knowing that standard deviation of a constant equals 0, you can make a conclusion about datafield frequency.

---

### 评论 #3 (作者: ZZ17713, 时间: 1 year ago)

How do I view the return value?

---

### 评论 #4 (作者: LO60550, 时间: 1 year ago)

interesting insight

---

### 评论 #5 (作者: VK91272, 时间: 1 year ago)

this is insightful tip.

---

### 评论 #6 (作者: NH84459, 时间: 1 year ago)

You can convert dataset evaluation expressions into code to run automatically, and can also evaluate the skewness and kurtosis of the dataset.

---

### 评论 #7 (作者: AC63290, 时间: 1 year ago)

Understanding datafields in WorldQuant BRAIN involves simulations to analyze coverage, frequency, bounds, median, and distribution. Expressions likedatafield != 0 ? 1 : 0assess non-zero coverage, while scaling and statistical measures reveal frequency and value ranges. Adjust parameters to uncover insights, ensuring optimized Alpha creation with informed data exploration.

---

### 评论 #8 (作者: TT55495, 时间: 1 year ago)

Thank you for the detailed guide on understanding new datafields. The six methods you've outlined for simulating expressions and obtaining insights are extremely helpful.

---

### 评论 #9 (作者: CC40930, 时间: 1 year ago)

By simulating these expressions in a "None" neutralization and decay 0 setting, you can effectively evaluate:Coverage: Availability of data.Update Frequency: How often the data is refreshed.Range and Distribution: Insights into the data's numerical bounds and spread.Central Tendency: Median values over a longer period.These methods help build an intuitive understanding of any new datafield, enabling better alpha design.

---

### 评论 #10 (作者: WC77208, 时间: 1 year ago)

为什么 datafield != 0 ? 1 : 0 用这个且设置了中性化，会导致 long 和 short 都是 0 呢，按理说只是减去平均值，难道是因为字段里不存在为 0 的值吗

---

### 评论 #11 (作者: YZ84314, 时间: 1 year ago)

I am confused by "datafield", the alpha can get insight of coverage by(long count + short count) / universe sizebut:1. i get the datafield "fscore_total", it's description show it's coverage in US-TOP 3000 is "30%"2. i run a simulation, but it's coverage is far less from 30%54 / 3000 = 1.8%Can Someone can help me with my confuse ?

---

### 评论 #12 (作者: WS55742, 时间: 1 year ago)

datafield != 0 ? 1 : 0 如果设置Neutralization不是None，可能会导致 long 和 short 都是 0，因为datafield 可能全是正数，datafield != 0 ? 1 : 0 得到的全为1，[1,1,1,1...]再中心化自然得到全为0，根据 long 和 short 计算方法，自然得到 0 。

---

### 评论 #13 (作者: LY72046, 时间: 1 year ago)

必做1：long-count 指多头，当alpha值为正时做多股票的数量short-count 指空头，当alpha值为负时做空股票的数量必做2：直接输出，可以分析出1100-1300家公司有这个数据以（5,22,66,252）四个常用维度进行回测ts_std_dev(anl4_cff_flag,N)N=5时，可可以分析出大多数公司的值是不变的，所以不是按周更新N=22时，可可以分析出一两百家公司发生变化，其他大多数公司的值是不变的，所以不是按月更新N=66时，400-800家公司发生改变N=252时，几乎所有公司发生改变所以推测是按照年度更新。类似的数据集还有年收入等。必做3：Trade_When (x=triggerTradeExp, y=AlphaExp, z=triggerExitExp)triggerExitExp是退出条件，即不进行交易（或全部平仓）AlphaExp是alpha表达式triggerTradeExp是买入条件，即进行买入trade_when(alpha>1,alpha,-1)可以等价于什么？等价于当alpha>1，表达式值为alpha,当alpha<=1时，表达式为previousAlpha,即之前的alpha：Ifalpha>1, Alpha =alpha.else, Alpha = previousAlphatrade_when(alpha>1,alpha,alpha<-1)可以等价于什么？等价于当alpha>1，表达式值为alpha,当alpha<=1且alpha>=-1时，表达式为previousAlpha,当alpha<-1时，为NaN：Ifalpha>1, Alpha =alpha.Else ifalpha<-1, Alpha = Nan;else, Alpha = previousAlpha必做4：必做5：

---

### 评论 #14 (作者: ML65849, 时间: 1 year ago)

HiYZ84314, if you apply the backfill operators like "ts_backfill", you can see the sum of long-short is around 1000, which is around 30% as data description says. It seems the long and short count indicates the average count of each day in that year.WC77208, yes it may not have the value 0 so all the instrument has the same value 1, so after neutralize it doesn't return any pnl.

---

### 评论 #15 (作者: SK72105, 时间: 1 year ago)

YZ84314Hello ! You should always use the visualization feature to check for coverage. Sometimes data fields mentioned as 100% coverage also can have no values for particular dataset/fields on a single day or more. You can use some method to fill the NANs like that mentioned byML65849. For the particular datafield that you mentioned the coverage is ~30% as mentioned in the "field description"

---

