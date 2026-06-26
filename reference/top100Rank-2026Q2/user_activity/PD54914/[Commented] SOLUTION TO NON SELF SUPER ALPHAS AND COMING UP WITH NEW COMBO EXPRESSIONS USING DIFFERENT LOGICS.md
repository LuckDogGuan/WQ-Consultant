# SOLUTION TO NON SELF SUPER ALPHAS AND COMING UP WITH NEW COMBO EXPRESSIONS USING DIFFERENT LOGICS

- **链接**: [Commented] SOLUTION TO NON SELF SUPER ALPHAS AND COMING UP WITH NEW COMBO EXPRESSIONS USING DIFFERENT LOGICS.md
- **作者**: DO97304
- **发布时间/热度**: 7个月前, 得票: 29

## 帖子正文

Creating and Simulating a Super Alpha in WorldQuant BRAIN
Step 1: Select Alphas
Choose 20 high-performing alphas from the same region (e.g., USA) to ensure consistency in
universe coverage and performance behavior.
Step 2: Assign a Custom Code Name
After selecting the 20 alphas, assign a unique code name to your group. Example: 321. This code
will be used to reference your selection in simulation.
Step 3: Navigate to the Simulation Section
Go to the Simulate tab from the top menu to begin building your Super Alpha.
Step 4: Configure Simulation Settings
In the simulation settings panel:
- Set the Region to match the one used in your alpha selections (e.g., USA).
- Adjust additional settings as required (e.g., rebalance frequency, neutralization options).
Step 5: Define Selection Expression
In the Selection Expression box, input the following code:
name == '321'
This ensures that the simulator only combines alphas tagged with your chosen code.
Step 6: Define Combo Expression
In the Combo Expression section, use the following:
1
This applies a uniform weight to all selected alphas in the group.
Step 7: Start Simulation
Click Start to run the simulation.
Review performance metrics like Sharpe Ratio, Return, Turnover, and Drawdown to evaluate
effectiveness.

---

## 讨论与评论 (16)

### 评论 #1 (作者: PD54914, 时间: 7个月前)

Random selection helps reduce correlation, provided the alpha pool is large and contains diversified signals.

---

### 评论 #2 (作者: BK74354, 时间: 7个月前)

Diversity in selecting the regular alphas for the super alpha is key in ensuring quality

---

### 评论 #3 (作者: JG69762, 时间: 7个月前)

Cool

---

### 评论 #4 (作者: GM63928, 时间: 7个月前)

Good note 

But did  you consider correlations

---

### 评论 #5 (作者: SN66028, 时间: 7个月前)

Cool

---

### 评论 #6 (作者: CN36144, 时间: 7个月前)

Nice summary, it’s concise, accurate, and easy to follow.

---

### 评论 #7 (作者: MK25243, 时间: 7个月前)

Thanks for sharing! Grouping alphas using a code name like this is really convenient. I’ve tested this approach and the Sharpe improved quite noticeably when the group has enough logical diversity.

---

### 评论 #8 (作者: FM66022, 时间: 7个月前)

Thanks for enlighting, I did not think of assigning a custom name to group my alphas I need to build a Super Alpha your post has really solved my case!

---

### 评论 #9 (作者: AK40989, 时间: 7个月前)

i like how title is just clickbait and have nothing to do with the post body

---

### 评论 #10 (作者: AG14039, 时间: 6个月前)

Thanks for sharing! Grouping alphas under a common code name is indeed very convenient, and in my experience, the Sharpe can improve significantly when the grouped alphas bring enough logical diversity to the mix.

---

### 评论 #11 (作者: PA75047, 时间: 6个月前)

A simple way to build a strong combo or super alpha in Brain when your normal combo signals are not working is to first pick a set of individually strong alphas from the same region so their behavior is consistent, then assign them a custom tag so you can group them together inside the simulator, and after that you use the simulate tab to build a combined expression that only pulls from the alphas with that tag, and this trick gives you full control over which ideas enter the combo and allows you to mix different logics like momentum, reversal, volatility or spread based signals without the system accidentally adding unwanted alphas, and by experimenting with weights or mathematical expressions inside the combo field you can discover new combinations that behave better than a normal auto selected super alpha.

---

### 评论 #12 (作者: TP18957, 时间: 5个月前)

This is a very practical walkthrough of building a Super Alpha manually, and it highlights an approach that many researchers overlook when they struggle with non-self Super Alphas or unintuitive auto-combinations. Tagging alphas with a custom code name and explicitly controlling the selection expression ( `name == '321'` ) gives you deterministic control over which signals enter the combo, which is critical for managing correlation and logical diversity. One important extension to this workflow is to go beyond a flat combo expression of  `1` . While equal weighting is a good baseline, experimenting with alternative combo logics—such as volatility-scaled weights, inverse-correlation weighting, or regime-conditioned weights—can materially improve robustness and drawdown behavior. Additionally, before grouping, it helps to pre-screen the 20 alphas not only for individual Sharpe but also for pairwise correlation and factor exposure overlap. This method effectively turns Super Alpha construction into a portfolio optimization problem rather than a black-box aggregation, which is exactly how advanced researchers should approach scaling signals on BRAIN.

---

### 评论 #13 (作者: JN96079, 时间: 5个月前)

You have a great insight! I hadn’t considered assigning custom names to organize my alphas when building a Super Alpha, and your post completely cleared that up for me.

^^JN

---

### 评论 #14 (作者: CA42779, 时间: 4个月前)

This is a good start for new users.

---

### 评论 #15 (作者: VG27700, 时间: 2个月前)

this is very helpful info

---

### 评论 #16 (作者: JO53930, 时间: 2个月前)

Super resourceful. Thanks for this

---

