# Selection expression and combo expression

- **链接**: [Commented] Selection expression and combo expression.md
- **作者**: DN28451
- **发布时间/热度**: 10个月前, 得票: 12

## 帖子正文

When making super alphas I have always limited my selection expression to short count, decay. Long count. Self correlation, prod correlation, author self correlation, author sharpe, etc. These I choose from the drop down list. For combo expression I always put 1. Are there other ways of coming up with different selection expression and combo expression other than those from the drop down list? Give examples please. Eg Selection expression "Decay", Combo expression "1"

---

## 讨论与评论 (15)

### 评论 #1 (作者: DT49505, 时间: 10个月前)

I’ve also been curious about this and still trying to fully understand how flexible we can be when defining selection and combo expressions. So far, I’ve mostly relied on the drop-down options like you mentioned (short count, decay, self correlation, etc.), since they seem like the “safe” choices. But I wonder whether limiting myself only to those defaults might cause me to miss out on more creative or diverse super alphas. For example, could we incorporate transformations of existing signals into the selection expression, or does that break the intended structure? And for combo expression, I’ve only ever put “1” as well, but I’m not sure if adjusting that weight across multiple signals could lead to better balance. Would love to hear how others experiment here—especially whether it’s common practice to try non-standard expressions or if most people stick to the recommended list.

---

### 评论 #2 (作者: DL51264, 时间: 10个月前)

Totally agree, the nice part is it smooths things out without biasing too much toward extremes. By leaning on sector or industry context you’re still preserving relative structure, which is often what matters most in fundamentals. It’s a small tweak but really adds resilience when signals are built on patchy fields.

---

### 评论 #3 (作者: AG14039, 时间: 10个月前)

Absolutely, I agree! The best part is that it smooths values without overemphasizing extremes. By incorporating sector or industry context, it maintains the relative structure that’s crucial in fundamental analysis. It’s a subtle adjustment, but it significantly improves the robustness of signals, especially when working with incomplete or patchy data.

---

### 评论 #4 (作者: HD25387, 时间: 10个月前)

Great question! For selection expressions, I’ve sometimes combined multiple metrics using simple math like  `Decay * ProdCorrelation`  or  `Sharpe / SelfCorrelation`  to better rank robust alphas. As for combo expressions, using weights like  `0.7`  or  `rank_metric1 + 0.3 * rank_metric2`  can help fine-tune blends. Curious to hear what others are trying too.

---

### 评论 #5 (作者: TP85668, 时间: 10个月前)

Good question! 👍 The dropdown options are the most common metrics, but you can design selection expressions creatively. For example, instead of just  `decay` , you could use combinations like  `decay * author_sharpe`  or  `prod_corr / self_corr`  to emphasize both stability and originality. Similarly, for combo expressions, using values like  `rank` ,  `log` , or even weighting schemes (e.g.,  `author_sharpe * 0.5 + self_corr * 0.5` ) can diversify how alphas are blended, instead of always “1”.

---

### 评论 #6 (作者: TP18957, 时间: 10个月前)

This is a great question, because selection expression and combo expression are often treated as “set it and forget it” parameters, but there’s actually more flexibility than just the dropdown defaults. The dropdown gives you safe, pre-validated metrics (decay, sharpe, self_corr, prod_corr, etc.), but you can also construct composite expressions that better reflect your design goals. For example, instead of ranking purely on decay, you could define a selection expression like  `decay * author_sharpe`  to prioritize both persistence and proven performance. Another option is  `prod_corr / self_corr` , which emphasizes orthogonality relative to existing pools. For combo expressions, “1” means equal weighting, but you can experiment with blends like  `0.7 * rank(decay) + 0.3 * rank(author_sharpe)` , or even apply nonlinear transforms such as  `log(1 + sharpe)`  if you want diminishing sensitivity to extreme values. These variations allow you to better shape the diversity and robustness of your super alpha rather than relying only on uniform weights.

---

### 评论 #7 (作者: TP18957, 时间: 10个月前)

Thanks for raising this topic—selection and combo expressions often don’t get much attention, yet they have a subtle but important impact on super alpha construction. I appreciate that you listed the common dropdown metrics, since that’s where most of us start, but the discussion here highlights that it doesn’t have to stop there. Community members have suggested interesting variations like multiplying or dividing different metrics (e.g., decay * sharpe or prod_corr / self_corr) or using weighted combinations rather than a flat “1” for combo expressions. Personally, I’ve found these kinds of tweaks can add resilience and balance, especially when building diverse portfolios of alphas. Your question has definitely motivated me to experiment more with non-standard configurations instead of sticking to the defaults. Thanks again for opening up this conversation—it’s a small detail, but one that can make a real difference in long-term performance.

---

### 评论 #8 (作者: NS62681, 时间: 9个月前)

Using sector or industry context to smooth missing or noisy data helps avoid bias toward extremes while still preserving relative structure. This small adjustment is especially valuable for fundamental fields, where patchy coverage can otherwise distort signals, ultimately making models more resilient.

---

### 评论 #9 (作者: AG14039, 时间: 9个月前)

Incorporating sector or industry context to smooth missing or noisy data helps prevent bias toward extremes while maintaining relative relationships. This subtle adjustment is particularly useful for fundamental fields, where incomplete coverage can otherwise skew signals, enhancing the overall robustness and resilience of models.

---

### 评论 #10 (作者: AG14039, 时间: 9个月前)

Thanks for bringing up this topic—selection and combo expressions often get overlooked, but they play a subtle yet significant role in Super Alpha construction. I appreciate your rundown of the common dropdown metrics, which is a helpful starting point, but this discussion shows there’s room to go further. Community members have explored variations like multiplying or dividing metrics (e.g., decay × Sharpe or prod\_corr ÷ self\_corr) and using weighted combinations instead of a flat “1” for combo expressions. I’ve found these tweaks can enhance resilience and balance, particularly when managing diverse alpha portfolios. Your post has inspired me to experiment more with non-standard configurations rather than relying on defaults. It’s a small detail, but one that can meaningfully impact long-term performance.

---

### 评论 #11 (作者: RP41479, 时间: 9个月前)

Exactly—using sector or industry context to fill or smooth missing data preserves relative rankings, avoids skew from extremes, and strengthens robustness, especially for fundamental datasets with uneven coverage or sparse observations.

---

### 评论 #12 (作者: HT71201, 时间: 9个月前)

In my view, applying sector or industry context to handle missing or noisy data reduces extreme bias while keeping relative structure. This is especially useful for fundamentals, where gaps could otherwise distort signals and weaken model resilience.

---

### 评论 #13 (作者: AA66051, 时间: 8个月前)

There are indeed a diverse range of ways to create both. Please visit learn section under super alpha and get more help from there.

---

### 评论 #14 (作者: IU48204, 时间: 7个月前)

I totally agree

---

### 评论 #15 (作者: MM27120, 时间: 1个月前)

good

---

