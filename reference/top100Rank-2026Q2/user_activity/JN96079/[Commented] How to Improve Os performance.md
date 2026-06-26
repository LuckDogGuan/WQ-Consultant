# How to Improve Os performance?

- **链接**: [Commented] How to Improve Os performance.md
- **作者**: JK98819
- **发布时间/热度**: 9个月前, 得票: 27

## 帖子正文

What should one check before submitting an alpha ???

---

## 讨论与评论 (12)

### 评论 #1 (作者: BO66171, 时间: 9个月前)

General alpha performance!

---

### 评论 #2 (作者: JN96079, 时间: 9个月前)

Mostly, you should check these three main features;

**1. Sharpe ratio;**  should be at least the required minimum threshold. In most cases, the Delay 1 for regions other than China is 1.58, the minimum threshold. Otherwise, the value should be higher than that to reflect the higher performance of your signal.

**2. Fitness;**  should have a considerable value, but the minimum threshold required is 1. Also, for this case, a higher value of fitness showcases the power and good performance of your alpha.

**3. Returns to Drawdown ratio;**  while the two metrics, i.e., returns and drawdown, have no minimum threshold to be passed by your alpha, they have general performance whereby as long as your alpha has better performance in regards to Sharpe ratio and fitness, the returns and drawdowns are often at best. However, you should avoid cases where drawdowns are higher than returns. In simple terms, aim for a returns/drawdown ratio of 1.5 or higher. As always, higher values indicate better performance of your alpha.

Other metrics you can consider are the  ***turnover*** , which needs to be between 1% and 70%. But a lower value, <30% is better.

---

### 评论 #3 (作者: JO81736, 时间: 9个月前)

so you mean drawdown should be half the returns or more less

---

### 评论 #4 (作者: JN96079, 时间: 9个月前)

[JO81736](/hc/en-us/profiles/28500907754391-JO81736) , I mean,  ***returns should be higher than the drawdowns*** . Way higher if possible, and if you understand. You should not have drawdowns with values higher than returns!

---

### 评论 #5 (作者: AS77213, 时间: 9个月前)

thanks everyone for sharing this useful  informatation ................

---

### 评论 #6 (作者: TP85668, 时间: 9个月前)

This is a good and practical question. To improve OS performance before submission, one should check robustness across universes and time periods, ensure the alpha is not overly dependent on a few stocks, and control correlation with existing signals. It’s also important to confirm that the logic behind the alpha makes sense economically, not just statistically.

---

### 评论 #7 (作者: AS13853, 时间: 9个月前)

hi as per my side below mentioned parameters should be checked before any alpha submission

**return and drawdown ration**  should be 1:2 for better performance

**turnover**  should be between 15 to 30%

**sharp and fitness**  should be as per universe standard and for better results fitness should be around 1.9 to 2

overall different dataset showing different result over different operator with different Neutralization

to avoid self and production co-relation we need to use specific dataset and if possible kindly avoid repetition of data-field

thanks

---

### 评论 #8 (作者: SD92473, 时间: 9个月前)

Before submitting an alpha, check that it passes robustness tests (stable IS/OS performance and reasonable Sharpe). Make sure turnover and max trade are within acceptable limits and not driven by noise. Verify that the signal isn’t overly correlated with your existing pool and works across regions or universes. Finally, confirm the logic is meaningful and not just an artifact of overfitting.

---

### 评论 #9 (作者: RP41479, 时间: 9个月前)

To boost OS performance, check robustness across universes and time, avoid reliance on a few stocks, and control correlation with existing signals. Ensure the alpha’s logic makes economic sense, not just statistical.

---

### 评论 #10 (作者: TT72336, 时间: 9个月前)

This is a thoughtful and practical question. To boost out-of-sample (OS) performance before submission, it's important to test robustness across different universes and time frames, ensure the alpha isn’t overly reliant on a handful of stocks, and check for low correlation with existing signals. Just as crucial is making sure the alpha logic has sound economic intuition—not just statistical appeal—to enhance its chances of holding up in real-world conditions.

---

### 评论 #11 (作者: ZX39768, 时间: 1个月前)

thanks

---

### 评论 #12 (作者: JM47610, 时间: 1个月前)

Thank you all for sharing.

---

