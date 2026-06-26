# SHARPE VS TURNOVER

- **链接**: [Commented] SHARPE VS TURNOVER.md
- **作者**: DN28451
- **发布时间/热度**: 1年前, 得票: 8

## 帖子正文

Hello team, which consideration has more weight between Sharpe and Turnover when submitting an alpha? Let's say you have 2 alphas; the first alpha has a Sharpe of 2.0 and a Turnover of 40%. The second alpha has a Sharpe of 1.6 and a Turnover of 30%.

---

## 讨论与评论 (12)

### 评论 #1 (作者: SK13215, 时间: 1年前)

If we noticed that Both Sharpe and Turnover ,which we consider the Sharpe should be high ,or we can say that Turnover should be least.with the help of operators which we use in this

---

### 评论 #2 (作者: BW14163, 时间: 1年前)

I think both Sharpe ratio and turnover are important. Excessive turnover can lead to high transaction costs after the OS , while a high Sharpe ratio is often considered an indicator of excellent alpha.

---

### 评论 #3 (作者: IK32530, 时间: 1年前)

I think people will make different choices depending on the values of turnover and Sharpe. In my case, I prefer to lower turnover to increase margin. I like to keep turnover as low as possible, ideally down to 20%, so I would choose an alpha with a Sharpe of 1.6. Of course, I would also consider the shape of the PNL graph when selecting an alpha.

---

### 评论 #4 (作者: DN28451, 时间: 1年前)

I find these as very good insights when making a choice between the two alphas. I will consider checking the PNL graph too. Keeping turnover below twenty percent is also a good idea. More insights are welcome

---

### 评论 #5 (作者: NH16784, 时间: 1年前)

No matter how high the Sharpe ratio of your alphas is, high turnover will significantly reduce your alpha performance in real life after costs. Try to keep turnover below 20% for your alpha to survive after costs. This is my experience from real-life trading.

---

### 评论 #6 (作者: DD24306, 时间: 1年前)

In the above case, I think alpha 2 is better, because turnover around that level will be more suitable and if you can turn on the visualize feature in the simulation, there will be charts to evaluate the overall sharpe, the fluctuating turnover is quite good, it is also possible that case 1 will be better than 2 or vice versa. I still believe in choosing the case of turnover < 25%, a reasonable range for any region.

---

### 评论 #7 (作者: DH50715, 时间: 1年前)

Alpha 1 has a higher Sharpe ratio (2.0 vs. 1.6), which means better risk-adjusted returns. While Alpha 2 has lower turnover (30% vs. 40%), the difference is small and likely doesn't outweigh the Sharpe advantage. Unless trading costs or liquidity are major concerns, Alpha 1 is the better choice.

---

### 评论 #8 (作者: NT84064, 时间: 10个月前)

When comparing Sharpe and turnover, Sharpe is generally the primary indicator of a signal’s predictive strength, while turnover reflects execution cost and trading frequency. In most cases, a higher Sharpe will be preferred, provided turnover remains within the acceptable range for the target universe and theme. In your example, if both alphas meet the platform’s turnover guidelines (and neither exceeds limits for cost assumptions), the alpha with Sharpe 2.0 and 40% turnover is likely more valuable because its higher risk-adjusted return outweighs the modest increase in turnover. However, if the research context emphasizes a specific turnover target — for example, low-turnover theme competitions — then turnover may take priority. The best practice is to optimize for Sharpe first, then refine turnover through smoothing, operator adjustments, or signal blending to hit theme requirements without losing too much predictive power.

---

### 评论 #9 (作者: NT84064, 时间: 10个月前)

Thanks for raising this question — it’s one that almost every alpha developer faces when balancing raw performance against trading frequency. I appreciate that you provided concrete numbers for both Sharpe and turnover, because it makes the discussion more tangible and easier for others to weigh in. Your post encourages the community to share how they prioritize between these metrics depending on the research goal, whether that’s general submission, Power Pool eligibility, or theme-based competitions. By starting this discussion, you’re helping both new and experienced consultants think more critically about the trade-off between signal strength and practical implementation costs.

---

### 评论 #10 (作者: SG46247, 时间: 10个月前)

====================================================================================This post is a good reminder that combining alphas isn’t just about boosting returns—it’s about smoothing volatility, controlling drawdowns, and ensuring that transaction costs remain manageable.Both approaches can be valid it depends on your infrastructure and execution constraints.

---

### 评论 #11 (作者: JN96079, 时间: 10个月前)

From what you have, I would definitely go for the signal with higher Sharpe, since Sharpe as a metric measures an alpha, giving the general performance, and the higher the better.

However, you can consider trying lowering the threshold to have a more efficient signal. Otherwise, always consider a higher Sharpe as long as other metrics are within required values, and another thing,  ***returns to drawdown ratio,***  keep it above 1.

---

### 评论 #12 (作者: LB76673, 时间: 9个月前)

In practice, Sharpe generally carries more weight than turnover when evaluating alpha quality, because a higher Sharpe directly reflects stronger risk-adjusted returns. However, turnover is still an important secondary metric since excessively high turnover can reduce the real-world applicability of a signal and may impact capacity or stability in production. Between your two examples, the alpha with a Sharpe of 2.0 and 40% turnover would usually be considered stronger than the one with a Sharpe of 1.6 and 30% turnover, as the turnover difference is relatively modest while the Sharpe improvement is significant.

---

