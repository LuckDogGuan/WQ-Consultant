# Sharpe ratio, turnover and margin  range for different region

- **链接**: [Commented] Sharpe ratio turnover and margin  range for different region.md
- **作者**: PG24800
- **发布时间/热度**: 2年前, 得票: 4

## 帖子正文

For different region what should be the ranges of sharpe ratio, turnover and margin

Tell about USA ASI CHN GLB TWN HKG

---

## 讨论与评论 (11)

### 评论 #1 (作者: YW42946, 时间: 2年前)

There are no actual ranges. This depends on the data used, the universe, the settings and your hypothesis. A good rule of thumb is trying to aim for > 2 Sharpe, < 20% turnover and > .5% margin.

---

### 评论 #2 (作者: TN48752, 时间: 2年前)

Hi. I want to ask that currently I am making alphas with high turnover (50 - 60%), but sharpe is also high (4 - 6). Are alphas of this type considered good and could this lead to os sharpe after low cost?? I suspect that because this datafield has a high frequency, it leads to high turnover (lots of portfolio changes). Thank you.

![图片](images/img_7e179bd6e5.png)

![图片](images/img_16d0b66759.png)

---

### 评论 #3 (作者: AG20578, 时间: 2年前)

Hi  [TN48752](/hc/en-us/profiles/13714359745431-TN48752) !

Could you please specify the region?

If it's CHN or ASI, there's a high likelihood that the performance, after accounting for costs, will fall below zero.

However, if it's the USA, the margin given this turnover still appears to be low.

It's essential to remember that the objective of each alpha is uniqueness - to discover uncommon market inefficiencies. The goal of an alpha is not necessarily to outperform costs.

---

### 评论 #4 (作者: TN48752, 时间: 2年前)

This alpha was made on region GLB MINVOL1M. I tried to evaluate the frequency of the datafield and saw that it is traded daily. As I understand it, if after cost performance is low, it will lead to a small increase or even a decrease in weight factor, is that correct? According to my understanding, weight factor will increase after at least 6 months of alpha being released to the market. and generate profit, too high turonver will cause the profit from that alpha to be low. Wish to be answered. Thank you so much.

---

### 评论 #5 (作者: AG20578, 时间: 2年前)

No, if alpha is unique and has good performance before costs in OS, then it is enough. There is no direct connection between weight factor and after cost performance.

---

### 评论 #6 (作者: TN48752, 时间: 2年前)

Thank you for responding. As I understand it, I don't need to fit turnover to low but can diversify turnover according to both high - medium and low turnover, right? Thank you.

---

### 评论 #7 (作者: AG20578, 时间: 2年前)

Sounds good - to have alphas across different turnover ranges 😃

---

### 评论 #8 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #9 (作者: CC40930, 时间: 1年前)

It's important to note that these metrics are influenced by various factors, including market conditions, investor sentiment, and regulatory changes. Therefore, while these general trends can provide a starting point, a detailed analysis considering current data and specific market conditions is essential for accurate assessments.

---

### 评论 #10 (作者: PN39025, 时间: 1年前)

I follow a lot of seminars and the 2022 and 2023 sessions have themes that are recommended to tune from 5% to 20%. So I think doing it in that range will give good alpha for both sharpe and OS.

---

### 评论 #11 (作者: SK72105, 时间: 1年前)

My median values for the mentioned regions (for regular alphas):

USA: Sharpe 2.1, Turnover 12.5, Margin 10.5

ASI: Sharpe 2.75, Turnover 20.3, Margin 7

GLB: Sharpe 2.59, Turnover 18.9, Margin 7.2

TWN: Sharpe 2.35-2.4, Turnover 11, Margin 15 (only 15 alphas submitted here)

HKG: Sharpe 2.1, Turnover 14, Margin 16.5 (only 40 alphas in this region)

Hope this is able to give you some clarity over performance in each region! However, in my opinion the median values can vary based on experience, the ideas used, and data category used! A lot of my alphas in USA/ASI also have high turnover because I submitted alphas more in these regions as a newer consultant.

---

