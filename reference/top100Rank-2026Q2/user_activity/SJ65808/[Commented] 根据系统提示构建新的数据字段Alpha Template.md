# 根据系统提示构建新的数据字段Alpha Template

- **链接**: [Commented] 根据系统提示构建新的数据字段Alpha Template.md
- **作者**: YJ83444
- **发布时间/热度**: 1年前, 得票: 11

## 帖子正文

在Alpha灵感匮竭之时，收到系统发送的提示：

PE ratio can be a good measurement to generate Alphas. Calculate estimated PE ratio using EPS estimates of  [EPS Estimate Model Dataset](https://platform.worldquantbrain.com/data/data-sets/model30?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)  and price fields of basedata ( [Price Volume Data for Equity](https://platform.worldquantbrain.com/data/data-sets/pv1?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000) )

系统提示可以使用EPS估值和价格字段构建新的PE比率数据字段。

第一步先看看什么是PE比率数据字段。

PE ratio，即 市盈率（Price-to-Earnings Ratio），是股票估值中最常用的指标之一。它反映了投资者愿意为每单位盈利支付的价格，是衡量股票相对价值的重要工具。

计算公式为：PE Ratio = 股票价格（Price）/ 每股收益（Earnings Per Share, EPS）
其中：

- 股票价格（Price）：当前股票的市场价格。
- 每股收益（EPS）：公司每股股票的盈利，通常使用过去12个月的盈利（Trailing EPS）或未来12个月的预测盈利（Forward EPS）。

PE比率可以用来：
1、衡量股票的估值水平：

- 市盈率越高，说明投资者愿意为每单位盈利支付更高的价格，可能意味着股票被高估。
- 市盈率越低，说明股票相对便宜，可能意味着股票被低估。

2、比较较同一行业中不同公司的估值水平。

3、判断市场情绪：

- 高市盈率可能反映市场对公司未来增长的高预期。
- 低市盈率可能反映市场对公司未来增长的悲观预期。

然后，从  **pv1**  数据集中获取价格字段，从  **model30**  数据集中获取EPS估值字段，构成 Price/EPS 组合字段。

为了消除极端值的影响，提高信号的可比性，将组合字段rank后，再放入一二三阶中生成Alpha。

目前跑了EUR TOP2500 D1，可以产生可提交的Alpha。

**思考：**

可以通过类似于PE比率的方式构建其他的数据字段组合，比如：

1、PEG Ratio（市盈率相对盈利增长比率）
PEG Ratio 是市盈率（PE Ratio）与盈利增长率（Earnings Growth Rate）的比值，用于衡量股票的估值是否合理，同时考虑公司的成长性。

公式为：PEG Ratio = PE Ratio / Earnings Growth Rate

其中：

- Earnings Growth Rate：盈利增长率，通常使用未来几年的预期盈利增长率。

意义为：

- PEG Ratio < 1：表示股票可能被低估，因为市盈率低于盈利增长率。
- PEG Ratio = 1：表示股票估值合理。
- PEG Ratio > 1：表示股票可能被高估，因为市盈率高于盈利增长率。

2、PB Ratio（市净率）
PB Ratio 是股票价格与每股净资产（Book Value per Share）的比值，用于衡量股票的市场价值与其账面价值的关系。

公式为：

PB Ratio = 股票价格 / 每股净资产
其中：

- 股票价格：当前股票的市场价格。
- 每股净资产：公司的净资产除以总股本，反映公司每股的账面价值。

意义为：

- PB Ratio < 1：表示股票的市场价格低于其账面价值，可能被低估。
- PB Ratio = 1：表示股票的市场价格等于其账面价值。
- PB Ratio > 1：表示股票的市场价格高于其账面价值，可能被高估。

---

## 讨论与评论 (6)

### 评论 #1 (作者: AK76468, 时间: 1年前)

感谢你的投稿，我从中获得了灵感！！

---

### 评论 #2 (作者: OB53521, 时间: 1年前)

首先非常感谢你的投稿，尝试系统给出的建议是一个非常不错的选择，并且你从系统给的建议中得到了你自己对于这个比喻的理解，而认为对于新人顾问是非常有帮助的。其次这篇帖子非常详细的介绍了PE和P B以及其中蕴含的意义，对于构建表达式用处非常大。希望以后能够更加活跃在论坛中，分享你的经验！

---

### 评论 #3 (作者: ZS59763, 时间: 1年前)

感谢你的帖子，很有帮助的内容，点赞！

---

### 评论 #4 (作者: JB53978, 时间: 10个月前)

我在搞d0的alpha，没灵感看到你的这个贴子中的股票价格 / 每股净资产眼前一亮，想到了一个模板，在回测目前最高的Sharpe是1.8，fit是1.32，在跑几个小时我想应该就有了，感谢你分享的内容，点赞

---

### 评论 #5 (作者: SJ65808, 时间: 3个月前)

感谢分享，之前都没怎么注意这些系统提示

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #6 (作者: SL35215, 时间: 2个月前)

感谢分享，很有帮助！

---

