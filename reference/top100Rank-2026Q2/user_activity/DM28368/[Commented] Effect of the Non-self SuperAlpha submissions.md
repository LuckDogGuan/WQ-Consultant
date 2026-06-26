# Effect of the "Non-self SuperAlpha submissions".

- **链接**: [Commented] Effect of the Non-self SuperAlpha submissions.md
- **作者**: HD26227
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

Please let me know about the effect of "Non-self SuperAlpha submissions" on Combine Performance assessment and Dairly payment. Thanks!

---

## 讨论与评论 (21)

### 评论 #1 (作者: DM28368, 时间: 1年前)

Non-self SuperAlpha is equivalent to regular superalpha, it has the same Combine Performance. But in terms of Dairly payment I see it has lower income.

---

### 评论 #2 (作者: DD24306, 时间: 1年前)

if your alpha is "Non-self SuperAlpha submissions" there will be two cases:
- alpha in good selection expression -> high payment, combine per
- alpha in bad selection expression -> low payment, combine per
however the above two cases are just general, it also needs to consider IS performance of your alpha, superalpha -> you need to control the number of selected alpha and write a tight combo expression to combine alpha selection for the highest possible performance -> check IS -> check corr -> check submit -> if alpha selection is not good you can add "* own" in selection expression to select alpha in your alpha pool -> add good signal from pool to improve per superalpha -> good then submit

---

### 评论 #3 (作者: KK81152, 时间: 1年前)

To effectively leverage Non-self SuperAlpha submissions, prioritize alphas with low correlation to your existing signals to enhance diversity. Backtest each alpha independently, assessing Sharpe ratio, turnover, and stability

---

### 评论 #4 (作者: VA36844, 时间: 1年前)

I believe that daily payment depends on the quality of the super alpha, which is influenced by the alphas you choose during the selection process. Therefore, leveraging component alphas with low correlation and low turnover can help improve super alpha performance.

---

### 评论 #5 (作者: SG76464, 时间: 1年前)

Choosing a high-quality alpha will ensure that there are no adverse effects from non-self super alpha. However, if you opt for subpar alpha, it could negatively impact your payment and the value factor.

---

### 评论 #6 (作者: SR82953, 时间: 1年前)

There have only been two updates in the combine alpha performance since the introduction of the non-super alpha feature, so it's difficult to draw a definitive conclusion at this stage. However, so far, I have observed non-super alpha possess positive impact on both the combine ability performance and daily payouts, particularly with non-super alphas having decent fitness and margins with lower drawdown value.

---

### 评论 #7 (作者: JC84638, 时间: 1年前)

Sorry to bother you guys — may I ask if there’s any difference in potential rewards between submitting Self Super Alphas and Non-Self Super Alphas, assuming their performance is similar? Also, since they are evaluated separately, do they generally receive higher payouts than regular Alphas?

---

### 评论 #8 (作者: PH82915, 时间: 1年前)

Non-self SuperAlphas use others’ signals. They count toward your Combined Performance (CAP) like regular ones, but daily pay can be lower. Why? Weak shared signals hurt your combo. Fix: Check their IS performance, pick low-correlation signals, add “*own” to focus on your alphas. Mixing good outside signals with yours boosts results. Stay diverse!

---

### 评论 #9 (作者: JC84638, 时间: 1年前)

[PH82915](/hc/en-us/profiles/1532005543462-PH82915)  Wow, thank you so much for your professional advice! 🙏 May I ask — do experienced consultants usually submit a Super Alpha every day?? Also, are Self Regular Alphas considered a valuable resource?

---

### 评论 #10 (作者: PP87148, 时间: 1年前)

"Non-self SuperAlpha" refers to SuperAlphas that you create using alphas from  **other consultants’ pools** , not your own. While these are still considered valid SuperAlphas, they  **do impact your Combine Performance** , just like your own SuperAlphas do.

So, the  **quality of the alphas you select**  matters a lot — choosing well-performing alphas (even if not your own) is key to improving your overall Combine score.

In terms of  **daily payment** , Non-self SuperAlphas are treated the same as any other SuperAlpha. Their contribution is evaluated based on their value factor, and payments are made accordingly.

✅  **Focus on strong alpha selection**  — whether from your pool or others — to maximize performance and earnings.

---

### 评论 #11 (作者: AK40989, 时间: 1年前)

While these submissions are treated similarly to regular SuperAlphas in terms of Combine Performance, their impact on daily payments can vary significantly based on the quality of the selected alphas. High-quality, low-correlation alphas can enhance overall performance and payouts, while subpar selections may lead to diminished returns.

---

### 评论 #12 (作者: SC43474, 时间: 1年前)

One subtle but important point I’ve noticed with Non-self SuperAlpha submissions is how sensitive they are to selection quality — especially when using shared alphas that may already be saturated across multiple combos. Even if the IS performance looks solid, overlap in usage can reduce marginal contribution to performance and daily payouts. I’ve had better results when using "*own" to rebalance toward my internal pool and layering in only a few truly complementary external signals. Worth experimenting with correlation heatmaps before finalizing a combo.

---

### 评论 #13 (作者: RP41479, 时间: 1年前)

Non-self SuperAlphas can suffer from overlap with shared signals, hurting marginal impact despite good IS. Using "*own" helps refocus on internal alphas, adding only a few well-matched externals. Try correlation heatmaps before locking in combos.

---

### 评论 #14 (作者: DT49505, 时间: 1年前)

The impact of Non-self SuperAlpha submissions on Combine performance and daily payments fundamentally hinges on the quality and selection process of component alphas. While Non-self SuperAlpha submissions are treated equivalently to regular SuperAlpha in performance assessment, their actual contribution depends on how well these alphas complement your existing portfolio. The key is to build a robust selection expression that prioritizes low correlation and high information ratio alphas, ensuring diversification and minimizing redundancy. Backtesting each alpha for metrics such as Sharpe ratio, turnover, and stability in the IS (in-sample) period is critical. Furthermore, incorporating a tight combination expression and periodically reviewing the correlation and IS performance helps in maximizing the combined SuperAlpha performance. If your selection leads to poor synergy, consider adding "* own" to your selection expression to focus on your best-performing alphas and improve the overall submission quality. This disciplined alpha selection and combination approach can enhance your Combine ranking and daily earnings.

---

### 评论 #15 (作者: ML46209, 时间: 1年前)

Thanks for the insightful discussion! From what I gather, Non-self SuperAlpha submissions contribute similarly to Combine Performance as Self SuperAlphas, but their daily payments tend to be more sensitive to the quality and correlation of selected alphas. Using too many shared or overlapping signals can dilute performance and reduce payouts.

To optimize, it seems critical to:

- Select low-correlation, high-quality external alphas
- Combine them smartly with your own alphas (using “*own” in expressions)
- Monitor IS performance and overlap via correlation heatmaps
- Control alpha pool size tightly for max marginal contribution

This adaptive approach could help maximize both Combine Performance and daily earnings. Would love to hear others’ experience on balancing internal vs external alphas in combos!

---

### 评论 #16 (作者: NT84064, 时间: 1年前)

This is a great question, and one that highlights an often misunderstood aspect of SuperAlpha dynamics. “Non-self” SuperAlpha submissions—i.e., SuperAlphas constructed using alphas that were not created by the submitting consultant—can still influence Combine Performance, but their effect on Combine-based payments or Value Factor scoring is nuanced. Typically, Combine Performance reflects the collective quality of deployed alphas within the SuperAlpha, regardless of authorship. However, from a payment and recognition standpoint, only the original authors of the individual alphas contribute to the Value Factor and compensation based on performance. If you are submitting non-self SuperAlphas, you're contributing to portfolio construction quality, but unless you're the alpha originator, you may not see a direct boost in your daily base payment. It would be helpful if the platform offered clearer attribution metrics in this area.

---

### 评论 #17 (作者: NT84064, 时间: 1年前)

Thank you for raising this important topic. The effect of non-self SuperAlpha submissions isn’t always clearly documented, so bringing attention to this area helps many of us better understand how to navigate the platform’s compensation and recognition structure. Many consultants might assume that submitting any high-performing SuperAlpha, regardless of alpha ownership, will directly impact their payments or Value Factor—but your question highlights that ownership and authorship remain central. It's also a valuable reminder to be strategic not just in performance, but in how we build and source our alpha content. I really appreciate you opening this discussion and hope WorldQuant provides more transparency around this going forward

---

### 评论 #18 (作者: SK90981, 时间: 1年前)

Selection quality is key! Using own signals and checking correlations can boost uniqueness and payouts. Avoid overused alphas for better results.

---

### 评论 #19 (作者: TP18957, 时间: 1年前)

One of the biggest lessons I’ve learned from working with Non-self SuperAlphas is the importance of  **marginal contribution** . Even if a shared alpha has strong IS metrics, if it’s already widely used across many combos, its  **incremental value**  to your SuperAlpha may be limited. I’ve started using correlation matrices and marginal performance tracking to evaluate how much each alpha is truly adding beyond redundancy. Also, including a strategic mix of  *own alphas*  with selectively chosen external ones seems to balance uniqueness and robustness better. If the non-self combo is well-constructed, it contributes fully to Combine Performance, but for daily payouts, avoid highly correlated, high-turnover signals that erode your Value Factor.

---

### 评论 #20 (作者: RK48711, 时间: 1年前)

Though these submissions are evaluated like regular SuperAlphas in Combine Performance, their  **daily payment impact depends heavily on alpha quality** . Selecting  **high-quality, low-correlation alphas**  can boost both performance and payouts, while weaker choices may reduce returns.

---

### 评论 #21 (作者: ER62933, 时间: 11个月前)

My super alpha is bringing this error how can I solve it:
""

- Non-self SuperAlpha submissions  **0**  reached quota of  **0** .
  """

---

