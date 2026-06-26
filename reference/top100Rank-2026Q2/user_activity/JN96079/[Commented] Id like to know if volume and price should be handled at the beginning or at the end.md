# I'd like to know if volume and price should be handled at the beginning or at the end?

- **链接**: [Commented] Id like to know if volume and price should be handled at the beginning or at the end.md
- **作者**: SQ15289
- **发布时间/热度**: 6个月前, 得票: 51

## 帖子正文

I have two addition methods for the same dataset. I want to know if the two data points have different units, should we first equalize them and then add them, or add them directly? For example, should we use rank(a) + rank(b) or rank(a + b)? Also, I've thought of rank, zscore, and scale as operators for quantity and price. Are there any others?

---

## 讨论与评论 (8)

### 评论 #1 (作者: KG79468, 时间: 6个月前)

Between  `rank(a)+rank(b)`  vs  `rank(a+b)` , I prefer the former. Ranking after summation can hide structure and over-emphasize one component.

---

### 评论 #2 (作者: NT84064, 时间: 5个月前)

This is a classic and very important question in alpha construction, and the answer depends on whether you want  **unit invariance**  or  **economic interaction**  to dominate the signal. On  **WorldQuant** , when price and volume (or any heterogeneous units) are combined, the default  *safer*  approach is usually  **normalize first, then combine** —for example  `rank(a) + rank(b)`  or  `zscore(a) + zscore(b)` . This ensures neither variable mechanically dominates due to scale, and it produces a cleaner cross-sectional signal that’s easier to interpret and more stable across regimes.

In contrast,  `rank(a + b)`  implicitly assumes that the  *raw interaction*  between a and b has meaning before normalization. This can be valid in cases where the combined quantity itself reflects a tradable concept (e.g., dollar volume ≈ price × volume), but it’s riskier when units are unrelated. In practice, rank and zscore are the most robust operators for mixing heterogeneous data, while  `scale`  is useful when you want bounded magnitudes but still preserve relative strength. Beyond those,  `normalize` ,  `winsorize + zscore` , or even time-series normalization (e.g., ts_zscore) can help control distributional distortions before combination. The key is consistency: once you decide whether normalization is part of the  *signal definition*  or just  *post-processing* , apply it deliberately rather than implicitly.

---

### 评论 #3 (作者: NT84064, 时间: 5个月前)

Thank you for asking this—this question goes straight to the heart of why many alphas look reasonable syntactically but behave very differently in practice. The distinction between “normalize first vs. normalize after” isn’t obvious until you’ve seen how unit dominance or operator ordering can completely reshape a signal. Your example with rank(a) + rank(b) versus rank(a + b) is especially helpful because it highlights how subtle implementation choices encode very different assumptions.

I also appreciate that you’re thinking beyond just rank and actively considering operators like zscore and scale. That kind of operator awareness is what separates mechanical experimentation from intentional alpha design. Questions like this encourage people to reflect on the economic meaning of each step instead of relying on trial-and-error optimization. Thanks for bringing this up—it’s the kind of discussion that benefits both newer researchers and experienced consultants refining their intuition.

---

### 评论 #4 (作者: AG14039, 时间: 5个月前)

Between rank(a) + rank(b) and rank(a + b), I prefer the former. Ranking after summation can obscure structure and over-emphasize a single component.

---

### 评论 #5 (作者: JN96079, 时间: 5个月前)

I generally favor  **rank(a) + rank(b)**  over  **rank(a + b)** . Ranking the components separately preserves their individual structure, whereas ranking after aggregation can obscure underlying relationships and allow one input to dominate the combined signal.

^^JN

---

### 评论 #6 (作者: LB76673, 时间: 5个月前)

If two inputs have different units or scales, you should  **normalize first, then combine** . In practice,  `rank(a) + rank(b)`  (or zscore/scale before adding) is usually safer than  `rank(a + b)` , because adding raw values mixes incompatible units and lets one dominate.

---

### 评论 #7 (作者: DL51264, 时间: 5个月前)

In practice, if two inputs have different units like price and volume, it’s almost always better to normalize them first and then combine, so rank(a) + rank(b) is usually safer than rank(a + b). Adding raw values mixes scales and can let one dominate the signal unintentionally. I normally treat normalization (rank, zscore, scale) as an early step, then combine, and only apply smoothing or neutralization later. Besides rank, zscore, and scale, people also use winsorize/truncation and group-based normalization to keep quantities and prices comparable.

---

### 评论 #8 (作者: HT71201, 时间: 5个月前)

For inputs with different units, normalize before combining— `rank(a) + rank(b)`  is safer than  `rank(a + b)` . Apply normalization first, then combine, and use smoothing or neutralization later. Winsorization, truncation, or group-based normalization can also help maintain comparability.

---

