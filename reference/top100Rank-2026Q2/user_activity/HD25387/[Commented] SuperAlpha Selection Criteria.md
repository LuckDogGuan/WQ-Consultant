# SuperAlpha Selection Criteria

- **链接**: [Commented] SuperAlpha Selection Criteria.md
- **作者**: HN45379
- **发布时间/热度**: 8个月前, 得票: 37

## 帖子正文

When combining alphas into a SuperAlpha, filtering matters as much as weighting. I usually filter by turnover and margin before combining, which often improves OS stability.
👉 What filters do you apply when selecting components for SuperAlpha construction?

---

## 讨论与评论 (9)

### 评论 #1 (作者: TP85668, 时间: 8个月前)

Great point! Besides turnover and margin, I often filter by correlation (to reduce redundancy) and long/short balance, which helps improve out-of-sample stability.

---

### 评论 #2 (作者: PP31783, 时间: 8个月前)

1)  **Competition Filter** : ["ATOM","POWER_POOL","HCAC2025","ACE2023"]

2)  **datafield_count filter**  : For selecting Alphas with less noise.

3)  **Correlation Filter** : prod_correlation and seld_correlation, I usually keep them around 0.3,0.4,0.5.

4)  **Neutralization Filter** : ["SLOW","FAST","SLOW_AND_FAST","CROWDING", "STATISTICAL", "REVERSION_AND_MOMENTUM"]

5)  **Data Classification Filter :**  For example mode, analyst or news specific.

Start with these combinations and do use python script to generate robust Alpha template based on your requirment. Hope it helps.

If you want help for python code ask me.

thanks.

---

### 评论 #3 (作者: AC75253, 时间: 8个月前)

Hi  [PP31783](/hc/en-us/profiles/11718713490711-PP31783)  thanks for sharing such a detailed and insightful breakdown of your SuperAlpha filtering process — really helpful!

You mentioned using a Python script to generate robust Alpha templates based on custom filter combinations. I'd love to learn more about that. Could you please share a basic structure or example of how you approach this in Python?

Looking forward to your guidance — much appreciated!

---

### 评论 #4 (作者: PP31783, 时间: 8个月前)

Hi AC75253, really appreciate that you loved my article.

Here is the breakdown of a sample code or python script for particular template.

dataset_categories = datasets_df["category_id"].unique().tolist()

dataset_categories = [x for x in dataset_categories if x not in ["fundamental"]]

range_turnover_l = [i / 100 for i in range(2, 10)]
range_turnover_r = [j / 100 for j in range(11, 30)]

import itertools
import random
combinations = list(itertools.combinations(dataset_categories, 3))
print(f'All the combination is : {len(combinations)}')
combinations=random.sample(combinations, 50)

import random 
my_list=["SLOW","FAST","SLOW_AND_FAST","CROWDING", "STATISTICAL", "REVERSION_AND_MOMENTUM"]
 **selection_expression_list** = [
    f'({ " || ".join([f"in(datacategories, \"{cat}\")" for cat in categories]) }) &&'
    f'({ " || ".join([f"(neutralization ==\"{cat}\")" for cat in random.sample(my_list, 3)]) }) &&'
    f'in(classifications, "{CL}") &&'
    f'datafield_count <= {dc} && turnover >= {turnover_l} && turnover < {turnover_r} && '
    f'os_start_date > "2020-01-01" && prod_correlation < {p} && self_correlation < {s}'
    for dc in [1,2,3,4]
    for CL in ["ATOM","POWER_POOL","HCAC2025","ACE2023"]
    for p in [0.2, 0.3, 0.4, 0.5]
    for s in [0.3, 0.4, 0.1, 0.2,0.5]
    for turnover_l, turnover_r in zip(range_turnover_l, range_turnover_r)
    for categories in combinations  # where each item is a tuple/list of category strings
]
print(f"Length of Selection Expression : {len(selection_expression_list)}")
 **selection_expression_list** =random.sample(selection_expression_list, 500).

Its just one example.

---

### 评论 #5 (作者: HD25387, 时间: 8个月前)

Really interesting comparison 🔎. I’ve also noticed that vec_sum gives stability but can wash out sharper edges, while vec_max uncovers hidden bursts of alpha at the cost of turnover.
I think the choice often depends on the target use-case — smoother portfolio vs. hunting niche edges. Curious to hear more community takes on this! 🚀

---

### 评论 #6 (作者: AG14039, 时间: 6个月前)

I’ve seen the same pattern — vec_sum delivers smoother, more stable behavior but can dilute sharper edges, while vec_max tends to reveal concentrated bursts of alpha, though usually with higher turnover. The better choice often depends on the objective: building a steadier portfolio or targeting more specialized opportunities. Would love to hear how others approach this trade-off!

---

### 评论 #7 (作者: SP39437, 时间: 6个月前)

Really interesting comparison 🔎. I’ve observed something similar:  **vec_sum**  tends to provide smoother, more stable signals, but it can sometimes dilute sharper alpha edges, while  **vec_max**  often surfaces concentrated bursts of alpha at the cost of higher turnover. In practice, the choice really depends on the objective—whether you’re aiming for portfolio stability or targeting niche, high-conviction opportunities. I’d be curious to hear how others in the community think about this trade-off.

When building robust alpha templates, I usually start with a structured filtering framework:

1. **Competition filter** :  `["ATOM", "POWER_POOL", "HCAC2025", "ACE2023"]`
2. **Datafield count filter** : helps reduce noise and over-complexity
3. **Correlation filter** : controlling both prod and self correlation, typically around 0.3–0.5
4. **Neutralization filter** :  `["SLOW", "FAST", "SLOW_AND_FAST", "CROWDING", "STATISTICAL", "REVERSION_AND_MOMENTUM"]`
5. **Data classification filter** : e.g. model-based, analyst-driven, or news-specific data

From there, using Python to systematically generate and test alpha templates based on these constraints can significantly improve robustness and efficiency. Hope this helps.

---

### 评论 #8 (作者: TP19085, 时间: 6个月前)

I really like this comparison, and I’ve noticed a similar pattern in practice. Using vec_sum usually results in smoother and more stable signals, though it can sometimes soften stronger alpha effects. In contrast, vec_max tends to highlight more concentrated alpha spikes, but this often comes with increased turnover and volatility. Ultimately, the right choice depends on the goal—whether the focus is on long-term portfolio stability or on capturing narrower, high-conviction opportunities.

When designing durable alpha templates, I typically begin with a clear filtering structure. This includes competition filters to avoid overlap, limits on datafield count to control complexity, and correlation thresholds to manage both production and self-correlation, usually in the 0.3–0.5 range. I also apply neutralization filters across different horizons and behaviors, along with data classification filters based on source type. Leveraging Python to systematically generate and evaluate templates within these constraints has proven highly effective for improving robustness and research efficiency.

---

### 评论 #9 (作者: JN96079, 时间: 5个月前)

You have a great comparison. Furthermore, I have experienced and seen the same behavior in practice. Using  **vec_sum**  generally produces smoother, more stable signals, although it can dilute some of the strongest alpha contributions.  **vec_max** , on the other hand, tends to surface sharper, more concentrated signals, but often at the cost of higher turnover and greater volatility. In the end, the better choice depends on the objective—whether the priority is long-term portfolio stability or targeting narrower, high-conviction opportunities.

^^JN

---

