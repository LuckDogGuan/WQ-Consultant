# Self Correlation in SAC 2025

- **链接**: [Commented] Self Correlation in SAC 2025.md
- **作者**: AK40989
- **发布时间/热度**: 1年前, 得票: 28

## 帖子正文

I’m trying to understand the exact role of the self_correlation expression in the Super Alpha selection process, especially in the "SIMPLE" category of the SAC Competition.

From what I understand, self_correlation generally refers to the highest correlation among the selected Alphas within the pool. But I’ve also seen people say it represents the self-correlation at the time of submission, with the author's existing pool of Alphas.

If it’s the former, then why is it undefined for the SIMPLE classification? And if it’s the latter, I’d like to understand how to calculate the self-correlation among the selected Alpha pool.

The more I think about it, the more confused I get. If it’s the self-correlation among selected Alphas, how is the initial Alpha for the pool chosen? I feel like if the first Alpha changes, the entire pool would also change.

Thanks for coming to my rant, hopefully someone understands why I’m so confused and can help me out.

---

## 讨论与评论 (5)

### 评论 #1 (作者: UG81605, 时间: 1年前)

Self_corr and prod_corr are snapshots at time of submission of a user, i remember WQ team saying this in some webinar. While author_self_corr and author_prod_corr is overall mean of authors all submitted alphas, this metric you can see on consultant leaderboard.

So idea behind self_cor is to select those alphas where the user has some unique signal at time of submitting ( you can use prod corr for more unique signals). While the other metric, author_self _corr will give all alpha pool of the author who has mean self corr less than lets say 0.4.

I hope i did not confuse you again with this.

---

### 评论 #2 (作者: RS70387, 时间: 1年前)

[AK40989](/hc/en-us/profiles/26422151767703-AK40989)  From what I understand, the reason self_correlation often shows up as undefined for the SIMPLE category is that WorldQuant internally breaks down submitted Alphas into smaller components. These smaller building blocks, classified as SIMPLE Alphas, aren’t treated as part of a broader pool, so there's no meaningful correlation to compute. Since they don’t represent full standalone Alphas with a history of related submissions, the self_correlation metric simply doesn’t apply.

---

### 评论 #3 (作者: SK13215, 时间: 1年前)

Yes.

- self-correlation is used—but  *only*  as part of the alpha-aggregation process when teams merge pre-lock date.
- Its purpose:  **remove duplicate signals**  to maintain diversity in a team's alpha library.
- It is  **not**  used as a tie-breaker during scoring phases.

---

### 评论 #4 (作者: HD25387, 时间: 1年前)

I completely understand your confusion — this is a very reasonable question.

In the SAC "SIMPLE" category, self_correlation is usually not defined because the system evaluates each Alpha individually, without combining them into a SuperAlpha at submission time. That’s why it shows as "undefined".

In contrast, when you're building a SuperAlpha manually or in COMPLEX categories, self_correlation refers to the highest pairwise correlation among the selected Alphas in the pool. It helps ensure the signals aren't too redundant.

You're also right that changing the first Alpha (or the selection order) can change the whole pool. This happens because the system uses a greedy selection process.

Hope this clears it up — many of us were confused by this at first too

---

### 评论 #5 (作者: LB76673, 时间: 9个月前)

In Super Alphas, self\_correlation measures the maximum pairwise correlation among all alphas included in that Super Alpha, helping detect redundancy within the pool. For the SIMPLE category, it’s undefined because there is only a single alpha, so no cross-correlation can be calculated. The confusion often comes from mixing this with production correlation to an author’s broader pool, but they are different: self\_correlation only reflects correlations among the selected alphas in that Super Alpha, not against your entire submission history. In practice, the platform gathers all alphas that meet your selection expression, computes their correlation matrix, and reports the maximum correlation as self\_correlation.

---

