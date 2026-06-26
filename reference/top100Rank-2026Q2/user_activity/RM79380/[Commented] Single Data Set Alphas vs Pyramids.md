# Single Data Set Alphas vs Pyramids

- **链接**: [Commented] Single Data Set Alphas vs Pyramids.md
- **作者**: TB54813
- **发布时间/热度**: 2个月前, 得票: 6

## 帖子正文

Hello guys, how does world quant treat single dataset alphas in terms of pyramids filling. Suppose I have a single dataset alpha with 2 fields. Whats the number that will be shown on the Pyramid alpha distribution page for the specific data category I've submitted to? Looking forward to hearing from you☺. Thanks!

---

## 讨论与评论 (8)

### 评论 #1 (作者: DK28254, 时间: 2个月前)

When you submit a single dataset alpha with 2 fields, the number shown on the Pyramid alpha distribution page for that specific data category is  **1** .

The Pyramid distribution counts the number of  **unique Alphas**  accepted, not the number of datasets or fields utilized within those Alphas. Even if an Alpha contains multiple fields from the same category, it is recorded as a single unit in the pyramid's count for that category.

If an Alpha combines datasets from different categories (e.g., Fundamental and Sentiment), it will typically contribute a count of 1 to each respective category on the distribution page to reflect that a slot in those category-specific pyramids has been filled.

---

### 评论 #2 (作者: RO53473, 时间: 2个月前)

Hello, thank you for the insight on how single dataset alphas are counted on the pyramid!

---

### 评论 #3 (作者: PN39025, 时间: 2个月前)

Hi , If you submit more than 2 categories, it won't count towards the pyramid, so please only use fewer than 2 categories. Note that the inst_pnl operator field is used for pricing, so please check the match pyramid section.

---

### 评论 #4 (作者: RM79380, 时间: 2个月前)

The number shown will be 1 since you submitted one alpha in the same data category.

---

### 评论 #5 (作者: MT46519, 时间: 2个月前)

Hi TB54813, that's a great question about how single-dataset alphas contribute to pyramid filling. Typically, WorldQuant's system will aggregate the signals from your two fields based on their respective data categories. It's worth checking the documentation for your specific data categories to understand if there's any weighting or precedence applied between fields from the same dataset, as that can impact the final pyramid visualization. Have you encountered situations where different fields within a single dataset seemed to have an unequal influence on the pyramid?

---

### 评论 #6 (作者: CM46415, 时间: 2个月前)

In pyramid allocation, WorldQuant doesn’t treat “single dataset vs multi-dataset” as a special rule for counting pyramids.

A single dataset alpha (even with multiple fields) is still evaluated as one alpha and contributes to pyramids based on its  **data category and diversity impact** , not how many fields it uses.

So the number shown in the pyramid distribution depends on:

- The  **data category used**  (e.g., price, fundamental, alternative, etc.)
- The  **unique contribution to diversity**  within that category
- Not the number of fields inside the alpha

In short: 1 dataset + 2 fields = still 1 alpha contribution, and pyramids reflect category-level allocation, not field-level complexity.

---

### 评论 #7 (作者: ND24253, 时间: 2个月前)

Hi TB54813, that's a great question about how single-dataset alphas are treated in the pyramid. My understanding is that the pyramid aggregation aims to provide a consolidated view of an alpha's performance across different data dimensions. For a single-dataset alpha with two fields, WorldQuant typically aggregates the performance based on the primary data category you've assigned. It's not a simple sum of the fields, but rather a weighted contribution to the overall alpha score. Have you observed any specific behaviors in the pyramid that seem to contradict this aggregation logic when you've submitted single-dataset alphas?

---

### 评论 #8 (作者: TL72720, 时间: 2个月前)

Hi TB54813, that's a great question that touches on how WorldQuant BRAIN aggregates alpha signals. For a single-dataset alpha with two fields, the Pyramid distribution page typically displays a consolidated score representing the alpha's overall signal strength and confidence within that specific data category. It's not just a simple average, but rather a sophisticated weighting based on factors like signal robustness, correlation with other data, and historical performance. Have you observed any particular patterns in how these consolidated scores behave for different types of single-dataset alphas you've developed?

---

