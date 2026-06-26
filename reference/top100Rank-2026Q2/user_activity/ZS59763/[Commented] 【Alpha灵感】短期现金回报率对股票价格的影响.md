# 【Alpha灵感】短期现金回报率对股票价格的影响

- **链接**: [Commented] 【Alpha灵感】短期现金回报率对股票价格的影响.md
- **作者**: YZ92137
- **发布时间/热度**: 1年前, 得票: 8

## 帖子正文

灵感来源： [《PRODUCTIVITY OF SHORT TERM ASSETS AS A SIGNAL OF FUTURE STOCK](https://arxiv.org/pdf/2412.13311)  [PERFORMANCE 》](https://arxiv.org/pdf/2412.13311)

- Alpha 核心思路

短期的现金回报率有超额收益

- Alpha关键公式

![图片](images/img_c9c15422ce.png)

![图片](images/img_7c83de2d2e.png)

- Alpha实现思路

1 因为文中多次提到以月为单位（点题短期），所以Alpha的时间周期基本就是d=20

2 从公式看到实际是要回归短期的股票回报率和现金之间的关系，股票回报率通过20天跨度的close进行计算得到

3 因为里面提到了是选择了的标的，排除了金融行业的股票，简单来说就是进行了分组，尝试了sector，industry和subindustry，industry效果相对较好，可能是里面有金融大类的划分？

4 因为是短期的数据，但是很多cash等财报类的数据的从逻辑上考虑就是季度更新，所以要进行填值操作，有没有对nan的处理，效果差别相当大

5 因为原文写了要用现金回报率进行排序，那我就选了group_rank，另外在S&P500上效果最好，我就选了用cap分组

- Alpha setting

![图片](images/img_f20f7c23a8.png)

- Alpha performance, Sharpe>1.3, turnover<50%, return>8%, fitness>0.7, pro-corr<0.65
- 增强Alpha的信号，以及其他不同的探索与尝试
- 可提交的版本

d = 20;

M = ts_delay(cap,d);

r = ts_delta(close,d);

y1 = power(ts_delta(cashflow, d),2)/ts_delay(M, d);

alpha = ts_regression(r,y1,600);

group_rank(-alpha, bucket(rank(cap),range="0,1,0.1"))

![图片](images/img_c9d0a782fa.png)

![图片](images/img_aa23e46c93.png)

- Alpha的模板

```
    for d in days:        for group_ops in group_ops_list:            for group in groups:                alpha = f"""d = {d};M = ts_delay(cap,d);r = ts_delta(close,d);y1 = power(ts_delta(cashflow, d),2)/ts_delay(M, d);alpha = ts_regression(r,y1,750);{group_ops}(-alpha, densify({group}))"""
```

- **Alpha模板的产能**

**搜索了2万个大概，产生了2个alpha，后面想再改个模板试试，已经没权限了。。。。**

- **Alpha的稳健性检查**

**d=10,20,30均有尝试，都有信号，随着时间增加递减，为了在其他region中方便尝试，都尽量用了比较通用的字段，发现其他region很多也有信号。**

- Alpha在其他region的表现

在ASI，GLB，EUR，CHN都有信号，但是普遍比USA的弱，没有简单找到alpha，现在没权限了，可能要换个路试试。

- 探索该Alpha遇到的困难

实际上这篇论文还有一部分公式和内容如下，逻辑上讲这篇文章主要说把股票的回报分为现金汇报和非现金汇报，上面我理解只是找到了现金回报的部分，还要再去掉非现金汇报的部分，才完美，不过我根据下面的公式做了一些尝试，效果没有很好，可能是我哪里搞错了。希望大家能完善。

![图片](images/img_d7bb10b636.png)  ![图片](images/img_1ee8bb6c7a.png)

附原文代码参考：

def calculate_b_it(company):
    data = company.copy()
    data['market_cap_t_minus_1'] = data['market_cap'].shift() # paper uses M_{t-1} for the denoms
    data['leverage'] = data['total_debt'] / (data['total_debt'] + data['market_cap'])

    # Y VALUES
    data['r_minus_R'] = data['stock_return'] - data['rf_rate']

# REGRESSION VARIABLES
    data['gamma_1'] = (data['cash_holdings'].diff()) / data['market_cap_t_minus_1']
    data['gamma_2'] = (data['earnings'].diff()) / data['market_cap_t_minus_1']
    data['gamma_3'] = ((data['total_assets'] - data['cash_holdings']).diff()) / data['market_cap_t_minus_1']
    data['gamma_4'] = (data['rd_expense'].diff()) / data['market_cap_t_minus_1']
    data['gamma_5'] = (data['interest_expense'].diff()) / data['market_cap_t_minus_1']
    data['gamma_6'] = (data['dividends_paid'].diff()) / data['market_cap_t_minus_1']
    data['gamma_7']= data['cash_holdings_t_minus_1'] / data['market_cap_t_minus_1']
    data['gamma_8'] = data['leverage']
    data['gamma_9'] = (data['total_debt'].diff() + data['market_cap_t_minus_1'].diff()) / (data['total_debt'].shift() + data['market_cap_t_minus_1'].shift())
    data['gamma_10'] = (data['market_cap_t_minus_1'] * (data['cash_holdings'].diff())) / (data['market_cap'] ** 2)
    data['gamma_11'] = (data['leverage'] * (data['cash_holdings'].diff())) / data['market_cap']

    data = data.dropna()

    y = data['r_minus_R']
    X = data[['gamma_1', 'gamma_2', 'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6', 'gamma_7', 'gamma_8', 'gamma_9', 'gamma_10', 'gamma_11']]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    data['marginal_cash_value'] = (
        model.params.iloc[0] +
        (model.params.iloc[10] * (data['cash_holdings_t_minus_1'] / data['market_cap_t_minus_1'])) +
        (model.params.iloc[11] * data['leverage'])
    )

    data['average_cash_value'] = data['marginal_cash_value'] * data['cash_holdings']

    company['b_it'] = data['average_cash_value'].pct_change()  # monthly cash return

---

## 讨论与评论 (7)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

很好的帖子，点赞！

此外，想问一下，你有没有尝试过用其他描述财务状况或者基本面状况的字段代替cashflow？我看你的模版核心就是不同的operator轮换，换cashflow字段或许是个办法？我不太确定

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

**搜索了2万个大概，产生了2个alpha，后面想再改个模板试试，已经没权限了。。。。感同身受啊**

---

### 评论 #3 (作者: YZ92137, 时间: 1年前)

[ZS59763](/hc/en-us/profiles/26858512793111-ZS59763)

没办法，权限变了，我就没再尝试了，本来想周末再改下的， cashflow在其他几个region里面我用了几个cashflow per share的字段*shares 替代，效果差不多。

---

### 评论 #4 (作者: YZ92137, 时间: 1年前)

好像很多ops又能用了，换了模板又在找了。。。等好了再发上来

---

### 评论 #5 (作者: YW93864, 时间: 1年前)

这个帖子很有趣，我有一些不同的见解。

1. 快速的看了一下原文和您整理的内容，我觉得这篇论文实际上是想传达ΔCash对短期超额收益的预测能力，而γ2-γ6是控制变量，意思是把这些变量加入回归后，考察ΔCash对短期超额收益是否还具备预测能力。因此本文真实的预测变量--alpha，应该是ΔCash，如果您在剥离ΔCash后发现该alpha仍然可以预测收益，那说明可能在捕捉其他信息，比如是否有ΔCash变动较高但没有被交易的公司，从而捕捉未被关注的那一部分收益（如果我理解错误，请随时指正我）

2. 对于您提出的困难，从统计角度简单的猜测是：gamma7-gamma11这几个变量和您要被回归的变量相关性过低或者过高，相关性过低会导致y和残差几乎没差异，过高会导致残差中都是噪声。需要考虑它们之间的关系。

*Kindly remind: USA市场有明显的动量效应，当您使用ts_delta/ts_returns(close, d)作为regression中的y时，需要考虑它的收益来源是否和您的idea一致，不然可能只是对momentum因子进行优化，当这种优化不够稳健的时候，alpha在样本外容易失效

---

### 评论 #6 (作者: YZ92137, 时间: 1年前)

[YW93864]([Commented] 【Alpha灵感】短期现金回报率对股票价格的影响.md/comments/29174992475031)

1 这篇论文我的确没有读的特别细，我主要看了他的代码部分，我是这么理解的

y = data['r_minus_R']
 X = data[['gamma_1', 'gamma_2', 'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6', 'gamma_7', 'gamma_8', 'gamma_9', 'gamma_10', 'gamma_11']]
 X = sm.add_constant(X)
 model = sm.OLS(y, X).fit()

这里我看他用了model.params.iloc[0]来计算data['marginal_cash_value']并最终得到了company['b_it']，bit就是作者用来排序的因子，化繁为简，就可以认为截距是bit，我认为这个marginal_cash_value的marginal可能就是排除掉其他cash因子得到的东西。。。当然我是连蒙带猜的，这块东西看的的确头大。

2 有时间我再试试

3 ts_delta(close, d) 是完全按照他论文的说法写的，不知道你是不是这个意思。。。抱歉，其实有点没看明白你的意思。

---

### 评论 #7 (作者: YQ76635, 时间: 1年前)

感谢作者的分享，我把作者前半部分的研报核心摘录，主要是公式的部分，用alpha表达式实现出来，参考了作者alpha 表达式idea。

下面是alpha表达式的实现，已经通过交易，可以提交

d=5;

M=ts_delay(cap,d);

r=ts_delta(close,d);

y=power(ts_delta(winsorize(ts_backfill(cash,d),std=4),d),2)/ts_delay(M,d);

y1=power(ts_delta(winsorize(ts_backfill(retained_earnings,d),std=4),d),2)/ts_delay(M,d);

y2=power(ts_delta(winsorize(ts_backfill(assets-cash,d),std=4),d),2)/ts_delay(M,d);

y3=power(ts_delta(winsorize(ts_backfill(rd_expense,d),std=4),d),2)/ts_delay(M,d);

y4=power(ts_delta(winsorize(ts_backfill(dividend,d),std=4),d),2)/ts_delay(M,d);

alpha=ts_regression(r,y+y1+y2-y3-y4,252);

d的值我设置的是5，其他值我尝试了回测，d=5表现最好，而且基本带有ts_delta(close,d)的，也是如此。

turnover过大，微调设置 decay=15 。其他参数设置参考作者。

---

