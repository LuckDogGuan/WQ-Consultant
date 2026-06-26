# Do we need to consider quantity and price in multiplication and division?

- **链接**: [Commented] Do we need to consider quantity and price in multiplication and division.md
- **作者**: SQ15289
- **发布时间/热度**: 6个月前, 得票: 54

## 帖子正文

In the previous question, I learned that addition and subtraction require units to be the same. Does multiplication and division also require the same? For example, for a/b and a*b, do we need to add rank, zscore, or scale?

---

## 讨论与评论 (14)

### 评论 #1 (作者: EN41519, 时间: 6个月前)

Yes I think so.

---

### 评论 #2 (作者: TP85668, 时间: 6个月前)

For multiplication/division, variables don’t need matching units, but  **normalization (rank, z-score, scaling) is strongly recommended**  to prevent scale dominance and signal distortion. In practice, unnormalized multiplications often look good in-sample but fail out-of-sample due to uncontrolled amplitude effects.

---

### 评论 #3 (作者: MY82844, 时间: 6个月前)

I think as in physics, the units are not required to the same for multiplication  and division, as long as the final output has a real meaning...

---

### 评论 #4 (作者: ML46209, 时间: 6个月前)

For multiplication and division, units don’t need to match like in addition/subtraction, but the result still needs a sensible interpretation. I usually normalize (rank/zscore) to control scale and avoid one input dominating the signal rather than for unit consistency itself.

---

### 评论 #5 (作者: PM26052, 时间: 6个月前)

Good question. Unlike addition and subtraction, multiplication and division do not require the inputs to have the same units. However, from an alpha design perspective, it’s still best practice to normalize (rank, zscore, or scale) inputs to control magnitude and avoid one term dominating the result.

---

### 评论 #6 (作者: KU30147, 时间: 6个月前)

I think no .we can multiply different operators.

---

### 评论 #7 (作者: MK25243, 时间: 6个月前)

Well, in my opinion, standardizing the unit of data chosen before you input them into any models or formulas will help you so much.

---

### 评论 #8 (作者: AY28568, 时间: 6个月前)

For multiplication and division, the values don’t need to have the same units. However, if one value is much bigger than the other, it can dominate the result and make the signal noisy. Using rank, z-score, or scaling helps keep things balanced and more stable. In practice, ranking both inputs is simple and works well for cross-sectional alphas, while z-score is useful when comparing changes over time

---

### 评论 #9 (作者: LB76673, 时间: 6个月前)

Units do not need to match in the strict sense, but scale still matters a lot. If a and b have very different magnitudes or heavy tails, a*b or a/b can be dominated by one term and become unstable. Applying rank, zscore, or scale before multiplying or dividing is usually recommended to control outliers, improve robustness, and make the interaction meaningful. Division in particular benefits from normalization to avoid extreme ratios.

---

### 评论 #10 (作者: HH63454, 时间: 6个月前)

multiplication and division don’t require matching units like addition/subtraction, but they do implicitly combine scales. In alpha design, the real issue is not unit consistency but dominance and stability. If one input has a much wider distribution or heavier tails, it can completely drive the product or ratio and make the signal brittle

that’s why rank/zscore/scale are often applied before a*b or a/b: not for mathematical validity, but to control sensitivity, reduce tail risk, and make the interaction interpretable. I usually ask: do I want relative ordering (rank), standardized surprise (zscore), or raw magnitude? - and normalize accordingly

---

### 评论 #11 (作者: AG14039, 时间: 5个月前)

For multiplication and division, the inputs don’t need to share the same units. However, if one term is much larger than the other, it can dominate the output and introduce noise. Applying rank, z-score, or scaling helps keep the inputs balanced and improves stability. In practice, ranking both inputs is a simple and effective choice for cross-sectional alphas, while z-score is more suitable when analyzing changes over time.

---

### 评论 #12 (作者: SP14747, 时间: 5个月前)

Addition/subtraction require compatible units.  **Multiplication/division don’t**  — but they  *do*  amplify scale differences. In alpha design, rank/zscore/scale isn’t about unit validity, it’s about  **controlling dominance and stability** . If one term sets the magnitude, you’re modeling scale, not interaction. Normalize when you want interaction, skip it only when scale itself carries economic meaning.

---

### 评论 #13 (作者: TP19085, 时间: 5个月前)

Addition and subtraction only make sense when inputs share compatible units, while multiplication and division technically do not—but they can strongly magnify differences in scale. In alpha construction, normalization techniques like rank, z-score, or scaling are not primarily about fixing unit consistency; they are about managing dominance, stability, and balance between components. If one input determines most of the magnitude in a formula, the resulting signal is effectively modeling scale rather than a true interaction between variables. Normalization becomes essential when the goal is to let multiple signals interact on equal footing and contribute comparably to the outcome. Skipping normalization is only justified when absolute scale itself carries clear economic meaning, such as liquidity size or risk exposure. In practice, thoughtful normalization helps prevent fragile alphas driven by a single overpowering term and leads to more stable, interpretable, and robust signal behavior across regimes.

---

### 评论 #14 (作者: HT71201, 时间: 5个月前)

Inputs for multiplication/division needn’t share units, but large differences can dominate and introduce noise. Ranking stabilizes cross-sectional alphas; z-scoring is better for temporal changes.

---

