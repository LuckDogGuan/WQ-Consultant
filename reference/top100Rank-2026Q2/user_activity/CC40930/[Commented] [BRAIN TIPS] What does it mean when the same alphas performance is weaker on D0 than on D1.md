# [BRAIN TIPS] What does it mean when the same alpha’s performance is weaker on D0 than on D1?

- **链接**: [Commented] [BRAIN TIPS] What does it mean when the same alphas performance is weaker on D0 than on D1.md
- **作者**: KA64574
- **发布时间/热度**: 3年前, 得票: 3

## 帖子正文

D1 alphas trade in the morning using data from the previous day; D0 alphas trade in the evening using data from the same day. In practice, if an alpha idea makes sense, often it will have better results in D0 because the alpha is reacting to the most recent market information.

However, using the latest information can also lead to overreaction, which could hurt performance. Also, there are datasets that are delayed by nature such as fundamental and analyst data — in those cases D0 does not have a significant information advantage and hence the performance could be worse.

Of course, what we’ve described above applies only for true alpha signals — if the input is not a true alpha signal, the chance of D0 being better or worse than D1 is 50/50.

If the D1 performance of your alpha is better than the D0 performance, it is likely that your D0 version is not a true D0 alpha or that your initial D1 idea is not a true alpha. So please double check if you see that happen.

---

## 讨论与评论 (6)

### 评论 #1 (作者: TT55495, 时间: 1年前)

I would like to ask why the backtest pass requirement of alpha D0 is much higher than alpha D1 (eg sharpe > 2.69 for USA)

---

### 评论 #2 (作者: AC63290, 时间: 1年前)

I would like to ask why many regions do not have alpha D0 (for example ASI, GLB, KOR,...) Or only big markets like USA, CHN, EUR allow creating alpha D0. Hope to get an answer

---

### 评论 #3 (作者: PH82915, 时间: 1年前)

D0 alphas trade in the evening using the latest same-day data, allowing them to react quickly to recent market information.
D1 alphas trade the next morning using data from the previous day, potentially offering a more measured response.

D0 Advantages:
Access to the most recent market information gives D0 alphas an edge in responding to timely opportunities.
Particularly effective for signals based on intraday or high-frequency data.

D0 Risks:
Overreaction to short-term noise can lead to diminished performance.
Datasets with natural delays (e.g., fundamentals, analyst updates) reduce the value of same-day trading, making D1 performance comparable or even better.

D1 Advantages:
Beneficial when trading on datasets that inherently have lagging updates or slower market incorporation, such as fundamentals.
May avoid the pitfalls of overreacting to noisy data, offering smoother and more reliable performance.

---

### 评论 #4 (作者: HH28380, 时间: 1年前)

thank you  [PH82915](/hc/en-us/profiles/1532005543462-PH82915) , verry clearly to understand

---

### 评论 #5 (作者: ND68030, 时间: 1年前)

The distinction between  **D1**  and  **D0 alphas**  is an important consideration when analyzing the timing of trading strategies, and it plays a significant role in determining the performance of your alpha. Let's break down the key aspects of each and understand why  **D1 alphas**  may outperform  **D0 alphas**  or vice versa, and what it means for the quality of your alpha signal.

---

### 评论 #6 (作者: CC40930, 时间: 1年前)

Thank you for sharing! This explanation highlights the importance of evaluating alpha signals in both D0 and D1 contexts. It’s crucial to ensure the signal's validity and avoid overfitting to recent data, which can distort performance.

---

