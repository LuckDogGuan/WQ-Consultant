# 【Alpha灵感】限价订单聚集对股票价格的影响

- **链接**: [Commented] 【Alpha灵感】限价订单聚集对股票价格的影响.md
- **作者**: DL55804
- **发布时间/热度**: 2年前, 得票: 27

## 帖子正文

**标题：** Limit Order Clustering and Stock Price Movements

**作者：** Xiao Zhang

![图片](images/img_2cba1d1749.png)

**概述：**

股票每日的收盘价轻微高于整数的会趋向于上升，比如6.1、7.1、8.1，股票每日收盘价轻微低于整数的会趋向于下降，比如5.9、6.9、7.9。

这是因为大量的限价订单会聚集在整数，比如：如果今天的收盘价达到了6.1，就代表着他吃掉了所有在6元的卖单，并且会有大量的买单聚集在6元，下一个卖单的聚集点可能是7元，所以他吃掉了所有的阻力，并且新增了大量的支撑，并且下一个阻力点在7元，所以有非常大的上升空间。

投资者的限价订单聚集在整数的原因可能是受到某些心理因素的影响，喜欢设置一个整数的价格，X.5可能也是一个很重要的分界点很重要的分界点。

**Alpha Idea:**

价格聚集效应：投资者的限价订单倾向于在整数价格点（如X.0）及其附近聚集。这些聚集的限价订单形成了价格支撑或压力，使得股票价格在这些点附近表现出特定的波动模式。

价格波动效应：当股票价格略高于整数价格点时（如收盘价为X.1），次日股票价格更有可能上涨；而当股票价格略低于整数价格点时（如收盘价为X.9），次日股票价格更有可能下跌。这是由于整数价格点附近的限价订单对价格形成了支撑或压制。

策略：在收盘价略高于价格点时（如X.5），买入该股票并持有至次日，预期股票价格将会上涨。在收盘价略低于价格点时（如X.5），卖出该股票并持有至次日，预期股票价格将会下跌。

alpha表现：

![图片](images/img_10f08387c3.png)

反思与总结：

1. 剔除极端的信号。
2. 剔除价格较大和较小的股票，价格较小的股票，本身的数值就很重要了，价格较大的股票，小数点后的数值没那么重要。
3. back_fill降低换手率。
4. 使用信号过去的标准差，增强信号，交易信号过去波动大的信号，波动大的信号更容易可能是更有效的信号。

---

## 讨论与评论 (12)

### 评论 #1 (作者: TN48752, 时间: 2年前)

你好。感谢您的详细文章。你能分享一下 alpha 表达式吗？谢谢。

---

### 评论 #2 (作者: UG81605, 时间: 2年前)

Interesting strategy. I bet this would have a high turnover. And in the post you mentioned backfill to reduce turnover. But why do we need backfill?

---

### 评论 #3 (作者: DL55804, 时间: 2年前)

![图片](images/img_c49a650d2a.png)

这是alpha的表达式

---

### 评论 #4 (作者: WL13229, 时间: 2年前)

好文章！

---

### 评论 #5 (作者: DL55804, 时间: 1年前)

> Interesting strategy. I bet this would have a high turnover. And in the post you mentioned backfill to reduce turnover. But why do we need backfill?

I use some filter in the expression, including price filter and signal winsor. These filters cause the signal to contain many "nan" and "zero". "nan" and "zero" represent signals that are no strong.Therefore, we use "ts_backfill" operator to replace "nan" and "zero" with a recent strong signal. If the signal change to "zero" or "nan" from a strong signal like -0.4 or 0.4, that means we close all the position. But if we use "ts_backfill" operator, that means we keep the original position unchanged and ultimately reduce the turnover

---

### 评论 #6 (作者: WL13229, 时间: 1年前)

👆漂亮，又一个很好的backfill的案例

---

### 评论 #7 (作者: TS90367, 时间: 1年前)

How can you share whats ur turnover?

---

### 评论 #8 (作者: PN59652, 时间: 1年前)

Hello. Can you please share your setting, this is my setting in USA market:

![图片](images/img_0ce37db78e.png) And this is my expression:

![图片](images/img_01db8344f9.png)

---

### 评论 #9 (作者: DL55804, 时间: 1年前)

> How can you share whats ur turnover?

![图片](images/img_26a8499270.png)

---

### 评论 #10 (作者: DL55804, 时间: 1年前)

> Hello. Can you please share your setting, this is my setting in USA market

this is my setting. Thank you for your expression, which also gave me a lot of inspiration

![图片](images/img_cd85e494ea.png)

---

### 评论 #11 (作者: CE47191, 时间: 1年前)

几点想法

1.这个限价订单影响股票价格的效应，应该会在散户集中的股票上最为明显，在主要由量化进行交易的股票上体现的不明显（绝大多数量化应该不在意整数关口），引入社交媒体数据可能有改进空间。此外在CHN市场上用社交媒体数据，可以考虑避免追高买入龙头概念股

2.在2023年初（刚好位于样本外），A股开始实行价格笼子制度，不知道价格笼子对于这个α有什么影响

---

### 评论 #12 (作者: PN39025, 时间: 1年前)

我认为你实现收盘价和开盘价的想法相当好，但是我想问你这种方法是否可以部署在许多不同的市场中，因为每个市场的特点不同，所以是否有必要将价格相乘。每个市场降低风险的系数？

---

