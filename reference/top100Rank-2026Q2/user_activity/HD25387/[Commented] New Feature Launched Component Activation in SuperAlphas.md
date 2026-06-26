# New Feature Launched: Component Activation in SuperAlphas

- **链接**: [Commented] New Feature Launched Component Activation in SuperAlphas.md
- **作者**: RS70387
- **发布时间/热度**: 1年前, 得票: 54

## 帖子正文

As shared in the recent opportunity webinar, the  [*Component Activation*](https://platform.worldquantbrain.com/learn/documentation/superalpha/superalpha-overview)  feature is now live on the platform!

This setting lets us control when each Alpha starts contributing to a SuperAlpha, either from its  **In-Sample (IS)**  or  **Out-of-Sample (OS)**  period.

**Why it matters:** 
Using IS Alphas in combos can inflate backtest performance due to overfitting. On the other hand, OS Activation ensures that each Alpha only contributes after its OS start date, giving us a more realistic and reliable picture of SuperAlpha performance on unseen data.

🔴  **IS Activation**  = Longer history, but higher overfitting risk
🟢  **OS Activation**  = Less history, but better for robust OS performance

This is especially handy when our component Alphas have different OS start dates, no need to filter or align them manually anymore.

Give it a try and share how it’s impacting your builds!

---

## 讨论与评论 (5)

### 评论 #1 (作者: DH50715, 时间: 1年前)

Okay, let's go ahead and try this feature together. It might offer something valuable, and it’s worth exploring.

---

### 评论 #2 (作者: JO96892, 时间: 1年前)

This feature is worth exploring, I am so excited to test and optimize my builds.

---

### 评论 #3 (作者: HD25387, 时间: 1年前)

Thanks for the great summary! 🔍 I’ve just started testing OS Activation in some of my SuperAlphas, and it really helps prevent overfitting — especially when combining Alphas with staggered OS periods. It’s also saving time by removing the need for manual alignment. Definitely a solid step toward more realistic and clean combo construction. Looking forward to seeing how others are using it!

---

### 评论 #4 (作者: AG20578, 时间: 1年前)

Hi  [PN39025](/hc/en-us/profiles/1532011933942-PN39025) !

Please check out this article  [SuperAlpha simulation modes](https://platform.worldquantbrain.com/learn/documentation/superalpha/superalpha-overview#superalpha-simulation-modes) .

In OS activation, alpha's performance will be counted from the alpha submission date and further. But in super alpha simulation you'll see performance only until current IS end date

---

### 评论 #5 (作者: AS73530, 时间: 11个月前)

Thanks for sharing this great insight, it's really helpful for preventing overfitting of alphas.

---

