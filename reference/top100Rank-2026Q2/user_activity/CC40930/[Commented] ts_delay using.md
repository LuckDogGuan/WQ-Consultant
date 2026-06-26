# ts_delay using

- **链接**: [Commented] ts_delay using.md
- **作者**: LN14840
- **发布时间/热度**: 3年前, 得票: 3

## 帖子正文

if the settings is delay-1, if we use ts_delay(close,1), we'll get the close price of yesterday or 2 days ago?

---

## 讨论与评论 (8)

### 评论 #1 (作者: SH71033, 时间: 3年前)

Hi,

Yes. For delay 1 taking ts_delay(close ,1 ) will give you the close price of the stock 2 days ago.

---

### 评论 #2 (作者: TP14664, 时间: 1年前)

May I ask why can't I use ts_delay(close,-1)? Is the reason because the wallet limits forward looking bias? Because normally when I train data prediction with python, I often use -1, then use model training to reduce overfit.

---

### 评论 #3 (作者: XL31477, 时间: 1年前)

**Hey,  [TP14664](/hc/en-us/profiles/7143306994583-TP14664) . You can't use ts_delay(close,-1) mainly because it would introduce a forward-looking bias. In quant world, we should base our analysis on historical data only. Unlike in Python training where you might use it for model training purposes and then deal with overfitting later. But here in our context, we gotta follow the rule to avoid getting future info by using such negative delay values. Hope that clears it up for you.**

---

### 评论 #4 (作者: NH84459, 时间: 1年前)

Hi, I would like to ask if the ts operator types are an analogue of derivatives, or is only ts_delta actually a derivative?

---

### 评论 #5 (作者: BA51127, 时间: 1年前)

**Understanding  `ts_delay`** : Using  `ts_delay(close, 1)`  with a delay setting of 1 will indeed provide the close price of the stock from 2 days ago, not 1 day ago. This is an important distinction to understand when working with time series data in the platform.
 **Avoiding Forward-Looking Bias** : The reason  `ts_delay(close, -1)`  is not allowed is to prevent introducing forward-looking bias into the model. In quantitative finance, it's crucial to base analysis solely on historical data to avoid using future information, which could lead to overfitting and unrealistic backtest results.
 **`ts`  Operator Types and Derivatives** : Regarding the question about whether  `ts`  operator types are analogous to derivatives, it seems there might be some confusion.  `ts_delta`  is indeed related to the concept of a derivative, as it calculates the change in a data field over time. Other  `ts`  operators serve different purposes in time series analysis and are not necessarily derivatives.

---

### 评论 #6 (作者: deleted user, 时间: 1年前)

Hi, I would like to ask what is the maximum time period that can be used for ts_delay, and does going back deep have any risk to alpha?

---

### 评论 #7 (作者: CC40930, 时间: 1年前)

When you use  `ts_delay(close, 1)`  with a  **delay-1**  setting, it means you will get the  **close price of yesterday** , i.e., the close price from the previous day.

---

### 评论 #8 (作者: LY88401, 时间: 1年前)

Your article is excellently written! The ideas are clear, engaging, and well-organized. You have a remarkable ability to present complex topics in a simple, accessible way. It’s an insightful and thought-provoking read that reflects your deep understanding and expertise.

---

