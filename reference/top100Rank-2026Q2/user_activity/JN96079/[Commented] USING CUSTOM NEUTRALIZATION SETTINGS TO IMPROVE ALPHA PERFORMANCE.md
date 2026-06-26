# USING CUSTOM NEUTRALIZATION SETTINGS TO IMPROVE ALPHA PERFORMANCE

- **链接**: [Commented] USING CUSTOM NEUTRALIZATION SETTINGS TO IMPROVE ALPHA PERFORMANCE.md
- **作者**: FM59649
- **发布时间/热度**: 5个月前, 得票: 25

## 帖子正文

### What is Neutralization?

Neutralization is a technique used to reduce risk in alpha signals. It works by distributing capital evenly across long and short positions to offset event-driven effects on stock prices within a chosen group. For a deeper dive into how neutralization works, check out this post.

**Typical Neutralization**

We generally discourage unneutralized alphas. By default, options like  `"MARKET"` ,  `"SECTOR"` ,  `"INDUSTRY"` , and  `"SUBINDUSTRY"`  automatically neutralize your alpha against these broad risk factors.

### Custom Neutralization

Beyond the standard options, you can create  **custom groups**  for neutralization using the  `group_neutralize()`  operator.

**Example:**

```
CUSTOM_GROUP = floor(rank(cap) * 4.99);
group_neutralize(alpha, CUSTOM_GROUP)

```

**How it works:**

1. Scale the  `rank(cap)`  vector from 0 to 1.
2. Multiply by 4.99 to expand the scale to 0–4.99.
3. Use  `floor()`  to divide stocks into 5 buckets (0–4).

This effectively creates  **quantiles based on market capitalization** , assuming that companies of similar size share similar risks. Neutralizing within these groups helps remove market-cap-related risk from your alpha.

### Double Neutralization

Sometimes, you may want to neutralize against  **multiple risk factors**  simultaneously. This is known as  **double neutralization** .

**Example:**

```
NEW_GROUP = bucket(rank(rel_num_comp), range="0.1,1,0.1");
CUSTOM_GROUP = (INDUSTRY + 1) * 1000 + NEW_GROUP;
group_neutralize(alpha, densify(CUSTOM_GROUP))

```

**Explanation:**

1. Create a new group based on  `rel_num_comp`  (number of competitors). Stocks with the same number of competitors get the same value.
2. Multiply the  `INDUSTRY`  value by a large constant and add  `NEW_GROUP` . Now, only stocks in the same industry  **and**  with similar competitors are grouped together.
3. Neutralization is applied within these fine-grained groups, effectively accounting for both  **industry risk**  and  **competitive risk** .

> Note:  `densify()`  is used here for faster computation. More on that in this post.

### Best Practices

- Experiment with different grouping methods to see which best suits your alpha.
- Common grouping ideas include:
  - Country
  - Exchange
  - Relationship data
  - Statistical groupings

- You can also create your own custom groups using the  `bucket`  operator.

---

## 讨论与评论 (6)

### 评论 #1 (作者: GK78216, 时间: 5个月前)

Great insight👌👌

---

### 评论 #2 (作者: JN96079, 时间: 5个月前)

Such a great explanation!

^^JN

---

### 评论 #3 (作者: BC83045, 时间: 5个月前)

Thank you for shairing. Besides, it’s often useful to check how group size distributions look after densify(), especially in narrower universes, to avoid over-neutralizing the signal.

---

### 评论 #4 (作者: FO28036, 时间: 3个月前)

Great

---

### 评论 #5 (作者: CJ92671, 时间: 3个月前)

wow,,,detailed and well thought of...

---

### 评论 #6 (作者: MB96681, 时间: 2个月前)

I like how your work is detailed and the display is amazing

---

