# Use of Normalized operator

- **链接**: [Commented] Use of Normalized operator.md
- **作者**: JK98819
- **发布时间/热度**: 1年前, 得票: 11

## 帖子正文

How to use normalize for data standarization for quantitative analysis?

---

## 讨论与评论 (2)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Hi, there are standardized operators that you can use. If you want to use them effectively, read the examples of those operators, which are explained in great detail.

---

### 评论 #2 (作者: AK98027, 时间: 1年前)

Normalization is key for making features comparable in quantitative analysis. You can use  `normalize(x)`  to scale a signal between 0 and 1 across the cross-section, which helps remove magnitude bias and improve comparability. It’s especially useful when combining different signals or ensuring neutrality. Just be mindful of the context—sometimes  `zscore`  or  `rank`  may be better depending on your goal.

---

