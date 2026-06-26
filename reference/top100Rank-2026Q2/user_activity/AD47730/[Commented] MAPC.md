# MAPC

- **链接**: MAPC.md
- **作者**: KU30147
- **发布时间/热度**: 9个月前, 得票: 11

## 帖子正文

When I submitted one alpha my score was 9000,but when I submitted 3 alpha my score reduce to 7000, I just want to know is there any penalty thing .I want to know how to improve my score .

I have used the same data sets with different operators , fitness and return/drawdown ratio was great .

---

## 讨论与评论 (6)

### 评论 #1 (作者: CT48231, 时间: 9个月前)

The score in the Merged Alpha Performance Competition depends both on the quality of your alpha and how it compares with other consultants participating in the competition. Therefore, if you notice your score dropping, it means your alpha is not strong enough yet

---

### 评论 #2 (作者: AG14039, 时间: 9个月前)

In the Merged Alpha Performance Competition, your score reflects both the inherent quality of your alpha and how it ranks against other participating consultants. So, if you see your score decline, it indicates that your alpha hasn’t yet performed strongly enough relative to the competition.

---

### 评论 #3 (作者: SG91420, 时间: 9个月前)

If your 3 alphas are highly correlated with each other (because they use the same dataset and similar operators), they add less incremental value. As a result, the overall score can be lower even if each individual alpha looks strong.

---

### 评论 #4 (作者: NK50559, 时间: 9个月前)

MAPC doesn’t just reward high Sharpe or good return/drawdown — it also rewards contribution of new, uncorrelated signals.

If you submit several alphas that are too similar (high correlation, same dataset, similar operators), their marginal contribution is smaller.

The system avoids “double counting” the same edge, so your overall score can go down when adding overlapping alphas.

---

### 评论 #5 (作者: LB76673, 时间: 9个月前)

There’s no direct penalty for submitting more alphas, but your score depends on how new submissions interact with your existing portfolio. If the new alphas are highly correlated with each other or with your previous ones, the system may reduce their contribution to your overall score, even if their individual stats look good. To improve your score, focus on diversity: vary datasets, operators, regions, and neutralizations to reduce correlation, while maintaining good fitness and Sharpe. Quality plus differentiation usually matters more than just quantity.

---

### 评论 #6 (作者: AD47730, 时间: 5个月前)

Yes, MAPC applies an implicit penalty. Scores drop when multiple alphas are correlated or use the same data, even with good fitness. The first alpha gets a novelty premium; additional ones must add orthogonal information. Improve scores by reducing cross-alpha correlation, changing data families, horizons, decay, and neutralization—not just operators.

---

