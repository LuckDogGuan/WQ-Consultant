# How to get reduce operators counted as as to increases operator count in Genius Section?

- **链接**: How to get reduce operators counted as as to increases operator count in Genius Section.md
- **作者**: AM60509
- **发布时间/热度**: 1年前, 得票: 3

## 帖子正文

Reduce operators work only in combo expression of super alphas but as per new rules in Q2 2025, superalphas don't affect operator count,so how will we use reduce operators to increase operator count.

I wrote the below alpha in ASI region in MINVOL1M universe with Statistical Neutralization

stats = generate_stats(alpha); innerCorr = self_corr(stats.hold_pnl,680); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic);

(0.5*combo_a(alpha,nlength=1950,mode='algo3')+0.4*(1 - maxCorr))

and submitted it my but operator count due to use of reduce_max operator didnt increase.

Can some one please guide

---

## 讨论与评论 (8)

### 评论 #1 (作者: TP85668, 时间: 1年前)

You're absolutely right — as of Q2 2025,  **Super Alphas no longer contribute to the Genius Operator Count** . So even though you're using  `reduce_max`  in the combo expression, it won’t boost your operator count.

### To increase your operator count:

1. **Avoid using Reduce operators only inside the combo expression of a Super Alpha.**
2. **Use Reduce operators like  `reduce_max`  directly in the main alpha logic**  before combining or outside the combo, and submit that as a regular alpha.
   - Example: apply  `reduce_max`  on some cross-sectional stats or metrics before using any combo logic.
3. If you still use Super Alpha,  **include other unique operators in the core expression (not just combo)**  to make sure they count.

---

### 评论 #2 (作者: KS69567, 时间: 1年前)

As of the Q2 2025 update,  **SuperAlpha expressions no longer impact the operator count** , even if they include complex functions like  `reduce_max` . This means that  **Reduce operators used inside  `combo_a`  or other combo expressions won’t increase your operator count** , as they are confined within the SuperAlpha scope. To make reduce operators contribute to your operator count, you must use them  **outside**  any SuperAlpha or combo expression. In your example, since  `reduce_max`  is embedded within a  `combo_a` , it doesn't count. To increase your operator count, move reduce functions  **outside**  SuperAlpha expressions or use them independently.

---

### 评论 #3 (作者: AC63290, 时间: 1年前)

Reduce operators must be used directly within the combo expression to count toward the operator total. Using them in helper functions or statistical blocks, like  `generate_stats` , won’t increase the count. Move reduce logic into the combo expression to ensure compliance with Q2 2025 rules and gain operator credit.

---

### 评论 #4 (作者: TP18957, 时间: 1年前)

Here’s the key clarification about  **reduce operators and operator count in Genius section under Q2 2025 rules** :

- **Super Alphas no longer add to operator count** , even if you use reduce operators like  `reduce_max`  inside their combo expressions.
- To increase your operator count with reduce operators,  **use reduce operators directly in the main alpha expression of a regular (non-Super) alpha** , not just inside the combo expression of a Super Alpha.
- Avoid placing reduce operators in helper functions or statistical blocks that don’t count towards the main expression.
- If you want to benefit from reduce operators for operator count,  **submit regular alphas with reduce operators in their core logic** , then combine those alphas as needed.

In short:
 **Use reduce operators in normal alphas, not just inside Super Alpha combo expressions, to have them counted toward the Genius operator count.**

---

### 评论 #5 (作者: SP39437, 时间: 1年前)

You're absolutely right — as of Q2 2025, Super Alphas no longer contribute to the Genius Operator Count. This means that even if you're using something like  `reduce_max`  within a Super Alpha’s  `combo`  expression, it won’t add to your operator total.

To effectively increase your operator count:

- Avoid placing Reduce operators solely inside a Super Alpha's combo expression.
- Instead, use Reduce operators (e.g.,  `reduce_max` ) directly in the main logic of a regular alpha — either before applying a combo or outside of any Super Alpha logic.

Example: Apply  `reduce_max`  to a cross-sectional feature or metric in a standalone alpha before any combination step.

If you still choose to use Super Alphas, make sure your core logic includes other unique operators outside of  `combo`  to ensure they count toward your Genius metrics.

---

### 评论 #6 (作者: AG14039, 时间: 1年前)

You're absolutely right—starting Q2 2025, Super Alphas no longer contribute to the Genius Operator Count. This means using operators like  `reduce_max`  solely within a Super Alpha’s combo expression won’t impact your operator total. To effectively increase your count, it's best to apply such Reduce operators directly in the main logic of regular Alphas, outside of any Super Alpha structure. For example, use  `reduce_max`  on a cross-sectional feature in a standalone Alpha before any combination step. If you still build Super Alphas, ensure your core logic includes unique operators outside the combo to maintain Genius metric contributions.

---

### 评论 #7 (作者: TP19085, 时间: 1年前)

You’re exactly right — starting in Q2 2025, Super Alphas no longer contribute to your Genius Operator Count. That means any operators used exclusively inside a Super Alpha’s  `combo`  expression, such as  `reduce_max` , won’t be counted toward your official operator total.

To effectively grow your operator count under the new rules, avoid relying solely on Reduce operators within Super Alpha logic. Instead, apply them directly in the primary structure of a standard alpha. For example, you could use  `reduce_max`  on a cross-sectional metric  *before*  any combo logic or as a standalone element in a regular alpha.

If you’re still using Super Alphas, be sure to include additional operators outside of the  `combo`  to ensure they’re recognized by the system. Building diverse and rich logic into your base alphas is now the most reliable way to improve your Genius metrics.

How are you adjusting your alpha design strategy in light of these changes?

---

### 评论 #8 (作者: NS62681, 时间: 1年前)

Super Alphas no longer contribute to the Genius Operator Count. As a result, using operators like  `reduce_max`  exclusively within a Super Alpha's combination logic will not affect your total operator count. To effectively increase your Genius metrics, it's best to apply such Reduce operators directly within the core logic of regular Alphas, outside of any Super Alpha structure.

---

