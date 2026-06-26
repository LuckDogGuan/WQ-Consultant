# More on Operators and Matching datafields

- **链接**: [Commented] More on Operators and Matching datafields.md
- **作者**: JO96892
- **发布时间/热度**: 1年前, 得票: 11

## 帖子正文

On many occassions several researchers just introduce operators to an expression without considering compatibility. Maybe tips on making sure that the operators you're using matches the data fields in your expression.

---

## 讨论与评论 (2)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Hi  [JO96892](/hc/en-us/profiles/27901982608407-JO96892)  ,I will consider two factors: whether the operator is suitable for the idea I am using and whether it can neutralize large fluctuations in the future. Is the trade-off between risk neutralization and temporary performance in IS big or not?

---

### 评论 #2 (作者: SK13215, 时间: 1年前)

- Try using (low-correlation) datafields for better generalization.
- using multiple versions of the same signal ( `open` ,  `close` ,  `adj_close` ) might not help.
- Optimize for field coverage vs.alpha **uniqueness** .

---

