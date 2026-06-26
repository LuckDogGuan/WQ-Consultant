# Suggestions on Powerpool + Regular alphas

- **链接**: [Commented] Suggestions on Powerpool  Regular alphas.md
- **作者**: AT91967
- **发布时间/热度**: 9个月前, 得票: 3

## 帖子正文

How to create a regular + powerpool alpha, like what core idea should be use , because whenever i try to make such alphas it passes the criteria of powerpool but not regular. Some suggestions on how to approach to make such alphas would be great for me.

---

## 讨论与评论 (4)

### 评论 #1 (作者: JN96079, 时间: 9个月前)

Hi,  [AT91967](/hc/en-us/profiles/30888095840023-AT91967) , take these differences in creating alphas in general.

**Powerpool**  alphas are those with 3 data fields and below, and the operators are not more than 8. Regular alphas are general alphas. So to differentiate, your alpha should pass every metric from the Sharpe ratio to the  **Sub-universe Sharpe**  to qualify as regular. Otherwise, if your regular alpha has more than 0.7 product correlation, it becomes a  **PowerPool plus Regular alpha** .

I believe you know  **pure PowerPool**  alphas are those whose metrics pass to be included as the least robust ones, but they may not have passed all the metrics.

If not well understood, please be sure to point out the issue, and I can explain more.

Thanks!

---

### 评论 #2 (作者: AT91967, 时间: 9个月前)

Hey,  [JN96079](/hc/en-us/profiles/25468856195607-JN96079) , i understood the differentiation part, i just want to ask how to make such alphas which are simpler and meet all the regular alphas requirement, the core idea for PP+Regular alpha

---

### 评论 #3 (作者: JN96079, 时间: 9个月前)

In creating alphas, you can come up with simple ideas combining data fields with some favorable operators. For instance, consider the following;

You can start by using simple operators like:

- Moving average (e.g., ts_mean)

- Ranking (rank)
- Linear regression (ts_regression)

Next, consider choosing relevant factors that may cut across:

- Price (close, open, high, low)
- Volume (volume, vwap)
- Financial indicators (earnings, debt-to-equity)

Check the following example of an alpha to get started:

- ts_mean(df, 10) - df: If in this case the df = close or open, then it will indicate undervaluation if the price is below the 10-day average.

---

### 评论 #4 (作者: JM40089, 时间: 4个月前)

[JN96079](/hc/en-us/profiles/25468856195607-JN96079)  I have read your explanation as am facing the same issue.  Despite using datasets within the themes I usually end up with pure power pools. So what are the metrics or minimum requirements for one to submit a power pool alpha. In simple terms what makes a power pool alpha a power pool alpha. If I can hear your own understanding I will appreciate.

---

