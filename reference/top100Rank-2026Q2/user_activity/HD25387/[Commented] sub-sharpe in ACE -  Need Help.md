# sub-sharpe in ACE -  Need Help

- **链接**: [Commented] sub-sharpe in ACE -  Need Help.md
- **作者**: AK40989
- **发布时间/热度**: 10个月前, 得票: 31

## 帖子正文

I’ve been trying to figure out how to properly calculate and apply the subuniverse Sharpe test using the ACE API library. I know that for robust alpha selection, the subuniverse Sharpe should be at least 70% of the overall Sharpe, but I’m not sure how to extract these values from the simulation output or set up the logic to verify if subuniverse Sharpe is at least 70% of the overall Sharpe.

---

## 讨论与评论 (7)

### 评论 #1 (作者: DT49505, 时间: 10个月前)

Hi. that's great question! In ACE, you can pull subuniverse Sharpe values from the simulation results, usually in the  `sub_sharpes`  field. Then compare each value to 70% of the overall Sharpe. For example, if your overall Sharpe is 0.8, subuniverse Sharpe should be ≥ 0.56. A quick loop can handle this check. It’s a great way to ensure your alpha isn’t overfitting to just one part of the universe.

---

### 评论 #2 (作者: AG14039, 时间: 10个月前)

In ACE, sub-universe Sharpe values are available in the  `sub_sharpes`  field from your simulation results. To check consistency, ensure each sub-universe Sharpe is at least 70% of your total Sharpe—for instance, if the overall Sharpe is 0.8, each sub-universe should be ≥ 0.56. You can easily automate this with a small loop. This method helps verify that your alpha performs robustly across the entire universe rather than relying on a single segment.

---

### 评论 #3 (作者: HD25387, 时间: 10个月前)

Thanks, that helps a lot! I wasn’t sure where to find the  `sub_sharpes`  field in the results, but I’ll dig into that. Do you typically run this check across multiple time periods, or just on the full sample?

---

### 评论 #4 (作者: TP85668, 时间: 10个月前)

Great question! 👍 You can calculate sub-universe Sharpe by rebuilding daily returns for the subset (using weights or equal-weight), then applying the annualized Sharpe formula. Finally, check if  `sub_sharpe >= 0.7 * overall_sharpe` . This ensures your alpha remains robust across different subsets.

---

### 评论 #5 (作者: SK72105, 时间: 10个月前)

subuniverse_sharpe >= 0.75 * sqrt(subuniverse_size / alpha_universe_size) * alpha_sharpe

more details can be found here:

[https://platform.worldquantbrain.com/learn/documentation/consultant-information/consultant-submission-tests#sub-universe](https://platform.worldquantbrain.com/learn/documentation/consultant-information/consultant-submission-tests#sub-universe)

---

### 评论 #6 (作者: TP18957, 时间: 10个月前)

Great question—and you’re on the right track with the “≥ 70% of overall Sharpe” robustness check. In ACE, you can usually grab the overall Sharpe from the sim summary and each sub-universe Sharpe from a  `sub_sharpes`  (or similarly named) field in the results payload. A simple pattern is:

res = ace.simulate(alpha_id=aid, settings=sim_settings)
overall = res["metrics"]["sharpe"]          # e.g., annualized Sharpe
subs    = res["metrics"]["sub_sharpes"]     # dict: {"AMER":0.62,"EMEA":0.55,...}

thresh_fixed = 0.70 * overall
flags = {k: (v >= thresh_fixed) for k, v in subs.items()}

Two refinements I’ve found helpful:

**Size-adjusted threshold**  (as SK72105 noted):

![图片](images/img_b6983b560c.png)

If your results expose  `sub_counts`  and  `universe_count` , you can compute this per sub.

**Stability across time** : run the same check on rolling windows (e.g.,  `P1Y`  slides) to avoid a one-off pass/fail.

Common pitfalls: make sure you’re comparing  **annualized**  Sharpe to annualized Sharpe; handle NaNs/low-count subs (set a minimum coverage/active-days filter); and keep sim settings (delay/decay/neutralization/costs) identical between overall and sub runs. Finally, log both the raw sub Sharpe and the margin above threshold—this helps triage which subs need parameter tweaks (e.g., slightly longer lookbacks or added  `hump()`  to tame turnover noise).

---

### 评论 #7 (作者: RP41479, 时间: 9个月前)

Compute sub-universe Sharpe by generating daily returns for that subset (weighted or equal-weighted), annualize using the Sharpe formula, and verify that sub_sharpe ≥ 0.7 × overall_sharpe to ensure alpha robustness.

---

