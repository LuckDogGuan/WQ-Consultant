# Difference Between self_correlation and author_self_correlation in Selection?

- **链接**: [Commented] Difference Between self_correlation and author_self_correlation in Selection.md
- **作者**: TN48242
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

Hi everyone, I hope you're doing well!

I’ve been reviewing the selection metrics related to correlation and came across four different expressions:

- `self_correlation <= 0.6`
- `prod_correlation < 0.5`
- `author_self_correlation <= 0.6`
- `author_prod_correlation < 0.5`

At first glance, they seem similar, but I’d like to understand the key differences between them.
Do the ones with the  `author_`  prefix represent average correlation values across all of a consultant's Alphas, while the others apply at the individual Alpha level?
If so, does using  `author_self_correlation`  or  `author_prod_correlation`  help filter based on the overall profile of a consultant, rather than the properties of a single Alpha?

Additionally, are there specific scenarios where using  `author_` -prefixed selections is preferred over direct Alpha-based correlation filters?

Appreciate any clarification on this — it would help me apply better filters when building SuperAlphas.

Thanks in advance!

---

## 讨论与评论 (19)

### 评论 #1 (作者: DV64461, 时间: 1年前)

Thank you for your sharing, but I think in case we have own* operator in selection expression, so we just need self_corr and prod_corr. I also wonder whether using author_self_corr and author_prod_corr make our simulation process slower?

---

### 评论 #2 (作者: TP85668, 时间: 1年前)

`self_correlation`  measures how much one Alpha is correlated with your other Alphas.
 `author_self_correlation`  is the average correlation of all your Alphas with each other.
Use  `self_correlation`  for filtering single Alphas, and  `author_self_correlation`  to evaluate your full Alpha portfolio's diversity.

---

### 评论 #3 (作者: DG92378, 时间: 1年前)

Thanks @TP85668 for the clarification 😊

---

### 评论 #4 (作者: JM52201, 时间: 1年前)

Hi @TN48242, great question!

You're spot on — the  **author_** * metrics reflect the  *average correlation across all your submitted Alphas* , while  `self_correlation`  and  `prod_correlation`  apply to a  *single Alpha* .

- Use  `self_correlation`  and  `prod_correlation`  to filter  **individual**  Alphas for robustness and novelty.
- Use  `author_self_correlation`  and  `author_prod_correlation`  to monitor your  **overall Alpha profile**  and avoid redundancy in your submissions.

Author-level filters are especially useful when building a SuperAlpha to ensure your alphas are diverse and not overly similar to production ones.

Hope that clears it up!

---

### 评论 #5 (作者: RS70387, 时间: 1年前)

Hi  [TN48242](/hc/en-us/profiles/28127049223191-TN48242) , Great question! Just to clarify the difference:

- `self_correlation <= 0.5`  means you're directly selecting individual Alphas whose self-correlation is below 0.5,  so each selected Alpha must meet that threshold on its own.
- `author_self_correlation <= 0.5` , on the other hand, selects Alphas from consultants whose  **average self-correlation**  (across all their submitted Alphas) is under 0.5. In this case, the specific Alpha being selected might have a higher self-correlation, but it's coming from a consultant with an overall diverse set.

So basically, one is about the Alpha itself, and the other is about the diversity of the consultant's full portfolio. Both can be useful, depending on what kind of filters you're aiming for in your SuperAlpha.

---

### 评论 #6 (作者: NS62681, 时间: 1年前)

**`self_correlation`**  indicates how strongly a single Alpha is correlated with your other Alphas.
 **`author_self_correlation`**  represents the average correlation among all Alphas in your portfolio.

Use  **`self_correlation`**  to assess the uniqueness of individual Alphas.
Use  **`author_self_correlation`**  to measure the overall diversification of your Alpha portfolio.

---

### 评论 #7 (作者: CT69120, 时间: 1年前)

`self_correlation`  is used to assess how similar a single Alpha is to your other Alphas — it's suitable for filtering individual Alphas.
 `author_self_correlation`  measures the overall diversity of your submitted Alpha portfolio — useful for evaluating your entire strategy.
When building a SuperAlpha, it's best to use both to ensure your Alphas are both independent and diverse.

---

### 评论 #8 (作者: AG14039, 时间: 1年前)

###### ChatGPT said:

Great question! To clarify,  `self_correlation <= 0.5`  means you’re selecting individual Alphas whose own self-correlation is below 0.5, so each Alpha must meet this threshold on its own. In contrast,  `author_self_correlation <= 0.5`  filters Alphas based on their consultants’ average self-correlation across all submitted Alphas—meaning the specific Alpha might have a higher self-correlation, but it comes from a consultant with an overall diverse portfolio. Essentially, one focuses on the Alpha itself, while the other considers the consultant’s broader diversity, and both filters can be valuable depending on your Super Alpha strategy.

---

### 评论 #9 (作者: SP39437, 时间: 1年前)

You're absolutely right — the  `author_*`  metrics help you evaluate the  **overall diversity**  of a consultant's Alpha portfolio, while  `self_correlation`  and  `prod_correlation`  focus on  **individual Alpha-level uniqueness and novelty** .

- **`self_correlation`**  ≤ 0.5 means you’re directly selecting Alphas that are internally diverse and not overly autocorrelated.
- **`prod_correlation`**  helps ensure the Alpha isn’t too similar to existing production Alphas.

In contrast:

- **`author_self_correlation`**  ≤ 0.5 filters by the average self-correlation across  *all*  of a consultant’s submitted Alphas. Even if a particular Alpha has higher self-correlation, it qualifies if the author’s overall set is diverse.

This distinction is especially important when designing  **SuperAlphas** , where maintaining  **diversity and non-redundancy**  across the component Alphas can significantly enhance robustness and avoid signal crowding. When building SuperAlphas, do you prefer using  `self_correlation`  or  `author_self_correlation`  as a primary filter — and why?

---

### 评论 #10 (作者: AK40989, 时间: 1年前)

I understand what these metrics represent, but I’m still struggling to translate that into a concrete idea. What would be an example thought process or selection expression that effectively uses author_self_correlation or author_prod_correlation? How do you typically incorporate these author-level metrics into your filtering strategy?

---

### 评论 #11 (作者: AG14039, 时间: 1年前)

You're absolutely right- `*`  metrics represent the average correlation across all your submitted Alphas, while  `self_correlation`  and  `prod_correlation`  are specific to an individual Alpha. You can use  `self_correlation`  and  `prod_correlation`  to evaluate the robustness and novelty of a single Alpha, while  `author_self_correlation`  and  `author_prod_correlation`  help you monitor your overall submission profile and avoid redundancy. These author-level filters are especially helpful when building a Super Alpha, as they ensure your included Alphas are diverse and not too similar to production ones. Hope that helps clarify things!

---

### 评论 #12 (作者: HD25387, 时间: 1年前)

Great question—this distinction is key when building well-balanced SuperAlphas. You're spot on:  `self_correlation`  and  `prod_correlation`  refer to metrics at the  **individual alpha level** , while  `author_self_correlation`  and  `author_prod_correlation`  reflect  **aggregate values across all alphas from the same consultant** . The  `author_`  metrics are particularly helpful when you want to control correlation across a contributor’s entire portfolio, ensuring diversity in signal sources. I usually apply author-level filters when assembling larger combos to avoid overexposure to a single researcher’s style.

---

### 评论 #13 (作者: AK52014, 时间: 1年前)

Great question, TN48242! self_correlation ≤ 0.5 filters individual Alphas, while author_self_correlation ≤ 0.5 targets consultants with diverse Alpha portfolios. One ensures each Alpha is low-correlation; the other favors authors with overall diversified submissions.

---

### 评论 #14 (作者: SK90981, 时间: 1年前)

Great question! Author-level correlations assess a consultant's overall Alpha diversity, while self/prod focus on individual Alphas. Useful for broader profile filtering!

---

### 评论 #15 (作者: AG14039, 时间: 1年前)

Great question, TN48242! A self_correlation ≤ 0.5 is used to filter individual Alphas with low internal correlation, while author_self_correlation ≤ 0.5 focuses on selecting consultants whose entire Alpha portfolio is well-diversified. One emphasizes the uniqueness of each Alpha, and the other values overall submission diversity.

---

### 评论 #16 (作者: RP41479, 时间: 1年前)

Thanks for raising such a valuable point! Understanding alpha-level vs. author-level correlation is crucial for building strong SuperAlphas. The clear explanations shared here are incredibly helpful—it's this kind of collaborative learning that makes the Brain community so special. Excited to apply these insights and keep growing together!

---

### 评论 #17 (作者: TP19085, 时间: 1年前)

Absolutely—great point. The  `author_*`  metrics give you insight into the  **overall diversity**  of a consultant’s Alpha portfolio, while  `self_correlation`  and  `prod_correlation`  evaluate uniqueness at the  **individual Alpha level** .

A  `self_correlation ≤ 0.5`  ensures that a specific Alpha isn’t overly autocorrelated, promoting internal signal variety.  `prod_correlation` , meanwhile, checks whether the Alpha closely resembles existing production Alphas—low values indicate better novelty.

On the other hand,  `author_self_correlation ≤ 0.5`  measures the  **average self-correlation across all Alphas**  submitted by a consultant. This means an Alpha with higher self-correlation may still qualify if the consultant’s portfolio is broadly diverse.

This distinction becomes especially important when constructing SuperAlphas. Maintaining  **low correlation across components**  helps avoid redundancy and improves out-of-sample robustness.

When you’re selecting Alphas for SuperAlphas, do you find it more effective to prioritize  `self_correlation`  at the individual level or rely on the broader  `author_self_correlation`  as a filter—and why?

---

### 评论 #18 (作者: SG91420, 时间: 1年前)

The stability of a single Alpha over time is gauged by self_correlation.
An indicator of the overall stability of a contributor's signals is author_self_correlation, which is the average self_correlation across all Alphas from that contributor.
In the process of filtering and choosing Alphas for SuperAlpha construction, that distinction makes a great deal of sense. I value your advice; it will undoubtedly help me make wiser choices in the future!

---

### 评论 #19 (作者: MK58212, 时间: 1年前)

Thanks to  **@ [TN48242](/hc/en-us/profiles/28127049223191-TN48242)**  for raising this thoughtful question—it’s a great point of confusion for many! Also, big thanks to the community members who stepped in to clarify the differences between individual alpha-level correlations and the author-level metrics. Really helpful for refining SuperAlpha filtering strategies!

---

