# [BRAIN TIPS] Demystifying Simulation Settings: Truncation

- **链接**: [Commented] [BRAIN TIPS] Demystifying Simulation Settings Truncation.md
- **作者**: NL41370
- **发布时间/热度**: 2年前, 得票: 6

## 帖子正文

**What is Truncation?**

Truncation is the maximum weight of each stock in the total portfolio. It's calculated by the ratio of the amount invested in the stock to half the book size.

**How to adjust Truncation on BRAIN?**

Hit the "Settings" button on the simulation page's top left. Find the "TRUNCATION" section in the third line. Adjust to a value between 0 and 1. Set to 0 for no truncation limit.

**Why Truncate?**

Truncation is used to limit outlier impacts. For example, in the expression cap / income, income can have positive, negative, or near-zero values. Close-to-zero income (the denominator) can result in huge values, leading to a portfolio overly concentrated on a few assets. Truncation can avoid this, particularly in small universes like the Top200.

**Tips for Success**

Besides truncation, you can control outlier impacts using methods like:

- Ranking (with the rank operator)
- Z-score (with the zscore operator)
- Winsorizing (with the winsorize operator)

Remember: the neutralization step occurs after truncation, so stock weight may exceed your truncation threshold post-neutralization.

---

## 讨论与评论 (8)

### 评论 #1 (作者: IS67473, 时间: 1年前)

Truncation can be utilized in limiting weight on a particular instrument to a reasonable number.

Since truncation step precedes the neutralization step while applying settings - for liquid universes you should ensure a reasonable weight distribution via the alpha expression itself.

---

### 评论 #2 (作者: YX15005, 时间: 2年前)

You said "It's calculated by the ratio of the amount invested in the stock to half the book size." in the " **What is Truncation?** " section. But in my understanding, if you get the weight of each stock, you are in the last step. Why did you say "the neutralization step occurs after truncation"? Do you mean the neutralization step will be taken twice?

---

### 评论 #3 (作者: ME73372, 时间: 2年前)

Interesting! Why the need to divide the book size in half? If truncation is 0.1, does it mean the limit is 5% of the book size? book size is the size of the portfolio?

---

### 评论 #4 (作者: AC82775, 时间: 2年前)

Adding on to YX15005 Comment's and referencing back to the " [How BRAIN platform works](https://platform.worldquantbrain.com/learn/documentation/create-alphas/how-brain-platform-works) ", I have a few ideas on how truncation works. Please correct me if I am wrong.

![图片](images/img_bc16cc05a0.png)

From the excel sheets we can see that neutralization happens after we get the alpha vector of rank(-returns) on column D. We subtract the mean of the market in this case, which mean we start the neutralization process. So when are we doing the truncation? In this example we are using rank operator, thus we will get a result of 1 at max, will it be truncated immediately?

From what I see, I believe the neutralization are done multiple time with truncation in between them. Though I am not sure how many time will the iteration goes. So the step will be:

Alpha vector -> Neutralization -> Truncation -> Neutralization

Thus with this technique, we can properly do the truncation and then neutralize it again thus "the neutralization step occurs after truncation" rule was held true.

---

### 评论 #5 (作者: SH71033, 时间: 2年前)

Hi  [AC82775](/hc/en-us/profiles/17140568810775-AC82775) ,

Yes, that is true.
Great job explaining the truncation settings.

---

### 评论 #6 (作者: PL15523, 时间: 1年前)

Hello, I would like to ask the following case:
eg alpha as follows: rank(close) + rank(open)

When I set the coefficients equal as above, the alpha weight is half of the truncation set in the setting, right?

---

### 评论 #7 (作者: TT55495, 时间: 1年前)

How can truncation be effectively used in combination with other techniques, like ranking, Z-score, or Winsorizing, to control outlier impacts and improve portfolio diversification? What are some potential challenges when using truncation in smaller universes, and how can these challenges be addressed to ensure better risk management?

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

Truncation is used to limit the maximum weight of each stock in a portfolio to prevent outliers from distorting the results. It helps maintain balance and avoid overconcentration in stocks with extreme values, especially in smaller universes. You can adjust truncation settings within BRAIN's simulation settings, ensuring the portfolio remains diversified while minimizing the risk of excessive concentration.

---

