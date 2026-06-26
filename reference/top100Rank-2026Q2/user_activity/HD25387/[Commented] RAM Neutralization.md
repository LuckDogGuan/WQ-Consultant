# RAM Neutralization

- **链接**: [Commented] RAM Neutralization.md
- **作者**: JK98819
- **发布时间/热度**: 1年前, 得票: 15

## 帖子正文

how to simulate alphas that can be submittable using RAM neutralization settings

---

## 讨论与评论 (9)

### 评论 #1 (作者: LA79055, 时间: 1年前)

You can set the neutralization in alpha when setting：

```
for alpha in alpha_list:    alpha['settings']['neutralization'] = "REVERSION_AND_MOMENTUM"
```

Other similar neutralization：

```
neutralizations = ["SUBINDUSTRY", "SECTOR", "MARKET", "INDUSTRY",                   "FAST", "CROWDING", "STATISTICAL", "SLOW_AND_FAST", "SLOW", "COUNTRY",                   "REVERSION_AND_MOMENTUM"]
```

Hope this is helpful to you.

————————————————————LA————————————————————

---

### 评论 #2 (作者: MG13458, 时间: 1年前)

OfCourse its's helpful

---

### 评论 #3 (作者: NS94943, 时间: 1年前)

Hi,

In addition to what LA79055 has said, the RAM neutralization setting neutralizes the alpha's reversion and momentum components, if any. So any alphas not having reversion or momentum components will not be affected as much by the RAM setting. Avoiding reversion and momentum alphas with the RAM setting is the safer approach.

Cheers!

---

### 评论 #4 (作者: TP85668, 时间: 1年前)

To simulate submittable alphas using  **RAM neutralization** , make sure to choose the  **"RAM" setting**  under the  *neutralization*  option before running your simulation. Then, construct alphas using datasets that align well with  **Reversion**  and  **Momentum**  patterns — such as  **price-volume** ,  **analyst revisions** , or  **short-term sentiment** . Focus on minimizing overfitting and ensuring turnover is reasonable (<0.3) for better acceptance.

---

### 评论 #5 (作者: HD25387, 时间: 1年前)

Thanks for the tips — super helpful! I’ve found that using  **short-horizon price-volume and analyst revision signals**  works best under RAM neutralization, especially when paired with simple transformations like  `ts_zscore`  or  `quantile` . It’s also important to  **keep expressions clean and turnover low**  to avoid rejection. One mistake I made early on was mixing RAM-sensitive and neutral signals — now I try to stick with either reversion or momentum, not both. Appreciate the examples — they really clarify what works in this setting.

---

### 评论 #6 (作者: SM36732, 时间: 1年前)

agree with  [NS94943](/hc/en-us/profiles/4557122515863-NS94943)

---

### 评论 #7 (作者: AK98027, 时间: 1年前)

Thanks for sharing your experience—really helpful insights! I agree that sticking to a clear signal type, like either reversion or momentum, helps maintain consistency, especially under RAM neutralization. Using clean expressions with simple transformations and low turnover definitely improves acceptance rates. Your point about avoiding signal mix-ups is a great reminder. These practical tips make a big difference!

---

### 评论 #8 (作者: SK13215, 时间: 1年前)

Thank you JK98819.

For giving such important information ..its helps a lot for consultants

---

### 评论 #9 (作者: LM22798, 时间: 1年前)

Thanks for sharing your experience—those are really valuable takeaways! I completely agree that focusing on a single signal type, like momentum or reversion, brings clarity and consistency, especially when dealing with RAM constraints. Keeping expressions clean and transformations minimal not only boosts acceptance rates but also enhances interpretability. Your reminder to avoid mixing signal behaviors is spot on and very helpful for anyone refining their alpha strategies.

---

