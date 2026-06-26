# How Many Inputs Are Too Many?

- **链接**: [Commented] How Many Inputs Are Too Many.md
- **作者**: SP14747
- **发布时间/热度**: 5个月前, 得票: 12

## 帖子正文

Does adding more data actually improve signal quality?
Or just add noise and correlation?

---

## 讨论与评论 (8)

### 评论 #1 (作者: LJ85703, 时间: 5个月前)

This is a good question. I hope someone capable can provide an answer.

---

### 评论 #2 (作者: MY82844, 时间: 5个月前)

I think we could get some observation from the average fields per alpha from Grand Master and Master consultants, which could be a reasonable benchmark.

---

### 评论 #3 (作者: SK13215, 时间: 5个月前)

good question.I appreciate...

---

### 评论 #4 (作者: LB76673, 时间: 5个月前)

It depends on whether the data adds independent information or just repackages existing signals. I've found that more data often increases overfitting risk unless you're disciplined about validation. The key test is whether new data improves OOS performance, not just IS Sharpe. In practice, combining correlated data sources (like multiple price-based features) usually adds noise, while truly orthogonal data (like alternative datasets with different update frequencies) can help. What's your approach to measuring whether new data is genuinely additive versus redundant?

---

### 评论 #5 (作者: TP85668, 时间: 5个月前)

More inputs don’t automatically mean a better signal. In practice, adding too many fields often increases noise and hidden correlation, leading to good IS but weak OS. A better approach is to start with  **one or two core signals with clear economic intuition** , and only add new inputs if they  **materially change the alpha’s behavior** —for example by improving stability, reducing drawdowns, or lowering correlation. If an extra input only boosts Sharpe marginally but adds fragility, it’s usually not worth it.

---

### 评论 #6 (作者: JN96079, 时间: 5个月前)

I think it would be insightful to look at the average number of fields used per alpha by Grand Master and Master consultants, as that could serve as a useful benchmark.

^^JN

---

### 评论 #7 (作者: HT71201, 时间: 5个月前)

New data is only useful if it offers independent information. Correlated features usually add noise, whereas orthogonal datasets can enhance out-of-sample performance. Validation is key to avoid overfitting.

---

### 评论 #8 (作者: HD25387, 时间: 5个月前)

I think the limit is less about count and more about  *independence* . A small number of inputs with clear, orthogonal information often outperform large bundles of correlated features. If a new input doesn’t materially change signal behavior (stability, drawdown, correlation) beyond a small Sharpe bump, it’s probably adding noise rather than edge.

---

