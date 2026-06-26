# High capacity Alpha Completion 2025

- **链接**: [Commented] High capacity Alpha Completion 2025.md
- **作者**: SS59313
- **发布时间/热度**: 1年前, 得票: 2

## 帖子正文

Hello,

Can anyone suggest that how the score are depend on alpha?

---

## 讨论与评论 (19)

### 评论 #1 (作者: MB13430, 时间: 1年前)

Hi

You can read  [this post](/hc/en-us/articles/26743191705879-What-is-the-scoring-criteria-for-High-Capacity-Alphas-Competition)

**IS Score:**

**Turnover in range 0-5%**

- If Sharpe < 1.75 — Score 0,
- If Sharpe >= 1.75 and Sharpe < 2.0 — Score 1,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 2,
- If Sharpe >= 2.25 — Score 3,

**Turnover in range 5-10%**

- If Sharpe < 2.0 — Score 0,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 1,
- If Sharpe >= 2.25 and Sharpe < 2.5 — Score 2,
- If Sharpe >= 2.5 — Score 3,

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

Hi , this is how the contest is scored :

**IS Score:**

**Turnover in range 0-5%**

- If Sharpe < 1.75 — Score 0,
- If Sharpe >= 1.75 and Sharpe < 2.0 — Score 1,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 2,
- If Sharpe >= 2.25 — Score 3,

**Turnover in range 5-10%**

- If Sharpe < 2.0 — Score 0,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 1,
- If Sharpe >= 2.25 and Sharpe < 2.5 — Score 2,
- If Sharpe >= 2.5 — Score 3,

Total IS Score will be  **(sum of all alphas' score) / sqrt(count of alphas)** . OS score follows a similar scheme, specific thresholds for OS Sharpe will not be shared.

Final Score will be  **0.25 * IS Score + 0.75 * OS Score**

---

### 评论 #3 (作者: PP87148, 时间: 1年前)

Thanks  [PN39025](/hc/en-us/profiles/1532011933942-PN39025)  for the details, these will be really helpful.

My question is If I have submitted an alpha with low turnover (< 10%), but in the OS the turnover increased from 10% , will this alpha be considered eligible for this competition?

---

### 评论 #4 (作者: RP41479, 时间: 1年前)

**Contest Scoring:**

- **IS Score:**
  - **Turnover 0-5%:**
  - Sharpe < 1.75 →  **0**
  - 1.75 ≤ Sharpe < 2.0 →  **1**
  - 2.0 ≤ Sharpe < 2.25 →  **2**
  - Sharpe ≥ 2.25 →  **3**
  - **Turnover 5-10%:**
  - Sharpe < 2.0 →  **0**
  - 2.0 ≤ Sharpe < 2.25 →  **1**
  - 2.25 ≤ Sharpe < 2.5 →  **2**
  - Sharpe ≥ 2.5 →  **3**
  - **Total IS Score:**  Sum of all alpha scores / sqrt(count of alphas).
- **OS Score:**  Follows a similar structure; specific thresholds are undisclosed.
- **Final Score:**   **0.25 × IS Score + 0.75 × OS Score.**

---

### 评论 #5 (作者: TN48752, 时间: 1年前)

The post you provided outlines a scoring system for evaluating performance based on  **Turnover**  and  **Sharpe ratio** . The scoring system is structured into two distinct ranges for  **Turnover** , and each range has different scoring criteria based on  **Sharpe ratio**  values.

---

### 评论 #6 (作者: DK30003, 时间: 1年前)

**IS Score:**

**Turnover in range 0-5%**

- If Sharpe < 1.75 — Score 0,
- If Sharpe >= 1.75 and Sharpe < 2.0 — Score 1,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 2,
- If Sharpe >= 2.25 — Score 3,

**Turnover in range 5-10%**

- If Sharpe < 2.0 — Score 0,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 1,
- If Sharpe >= 2.25 and Sharpe < 2.5 — Score 2,
- If Sharpe >= 2.5 — Score 3,

---

### 评论 #7 (作者: TD84322, 时间: 1年前)

Check out this link to learn how the scoring works:  [High Capacity Alphas Competition Scoring](/hc/en-us/articles/26743191705879-What-is-the-scoring-criteria-for-High-Capacity-Alphas-Competition) .  [https://support.worldquantbrain.com/hc/en-us/articles/26743191705879-What-is-the-scoring-criteria-for-High-Capacity-Alphas-Competition](https://support.worldquantbrain.com/hc/en-us/articles/26743191705879-What-is-the-scoring-criteria-for-High-Capacity-Alphas-Competition%C2%A0)

---

### 评论 #8 (作者: NP85445, 时间: 1年前)

Thanks for laying out the scoring criteria! One question that comes to mind: if an alpha is submitted with low turnover but later exceeds the 10% threshold in the OS phase, does that affect its eligibility?

---

### 评论 #9 (作者: KK61864, 时间: 1年前)

Each submitted alpha will be scored on the basis of the following:

**IS Score:**

**Turnover in range 0-5%**

- If Sharpe < 1.75 — Score 0,
- If Sharpe >= 1.75 and Sharpe < 2.0 — Score 1,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 2,
- If Sharpe >= 2.25 — Score 3,

**Turnover in range 5-10%**

- If Sharpe < 2.0 — Score 0,
- If Sharpe >= 2.0 and Sharpe < 2.25 — Score 1,
- If Sharpe >= 2.25 and Sharpe < 2.5 — Score 2,
- If Sharpe >= 2.5 — Score 3,

Total IS Score will be  **(sum of all alphas' score) / sqrt(count of alphas)** . OS score follows a similar scheme, specific thresholds for OS Sharpe will not be shared.

Final Score will be  **0.25 * IS Score + 0.75 * OS Score**

---

### 评论 #10 (作者: QN91570, 时间: 1年前)

- **IS Score:**
  **Turnover in range 0-5%**
  - If Sharpe < 1.75 — Score 0,
  - If Sharpe >= 1.75 and Sharpe < 2.0 — Score 1,
  - If Sharpe >= 2.0 and Sharpe < 2.25 — Score 2,
  - If Sharpe >= 2.25 — Score 3,
  **Turnover in range 5-10%**
  - If Sharpe < 2.0 — Score 0,
  - If Sharpe >= 2.0 and Sharpe < 2.25 — Score 1,
  - If Sharpe >= 2.25 and Sharpe < 2.5 — Score 2,
  - If Sharpe >= 2.5 — Score 3,
  2
- [PN39025](/hc/en-us/profiles/1532011933942-PN39025)
  - 1年前
  - Edited
  Hi , this is how the contest is scored :
  **IS Score:**
  **Turnover in range 0-5%**
  - If Sharpe < 1.75 — Score 0,
  - If Sharpe >= 1.75 and Sharpe < 2.0 — Score 1,
  - If Sharpe >= 2.0 and Sharpe < 2.25 — Score 2,
  - If Sharpe >= 2.25 — Score 3,
  **Turnover in range 5-10%**
  - If Sharpe < 2.0 — Score 0,
  - If Sharpe >= 2.0 and Sharpe < 2.25 — Score 1,
  - If Sharpe >= 2.25 and Sharpe < 2.5 — Score 2,
  - If Sharpe >= 2.5 — Score 3,
  Total IS Score will be  **(sum of all alphas' score) / sqrt(count of alphas)** . OS score follows a similar scheme, specific thresholds for OS Sharpe will not be shared.
  Final Score will be  **0.25 * IS Score + 0.75 * OS Score**

---

### 评论 #11 (作者: DK30003, 时间: 1年前)

The post you provided outlines a scoring system for evaluating performance based on  **Turnover**  and  **Sharpe ratio** . The scoring system is structured into two distinct ranges for  **Turnover** , and each range has different scoring criteria based on  **Sharpe ratio**  value

---

### 评论 #12 (作者: AG20578, 时间: 1年前)

Hi  [PP87148](/hc/en-us/profiles/11771952650775-PP87148) !

> My question is If I have submitted an alpha with low turnover (< 10%), but in the OS the turnover increased from 10% , will this alpha be considered eligible for this competition?

According to the  [competition guidelines](https://platform.worldquantbrain.com/competition/HCAC2025) :

Alphas are considered for scoring only if they meet all of the following criteria: (i) are in the USA or GLOBAL universe(s); (ii) use Delay 1; and (iii)  **have turnover less than 10% during the in-sample period** .

---

### 评论 #13 (作者: PP87148, 时间: 1年前)

Hi  [AG20578](/hc/en-us/profiles/12243980162327-AG20578) ,

Your response clarifies the eligibility criteria regarding turnover during the in-sample period. It's good to know that the competition evaluates turnover based solely on the in-sample period, even if it changes in OS. This is helpful, especially when assessing alpha submissions. Appreciate your input!

---

### 评论 #14 (作者: NH84459, 时间: 1年前)

A strategy that involves four options contracts with different strike prices but the same expiration date. It aims to profit from a low-volatility environment where the underlying asset’s price remains within a certain range.

---

### 评论 #15 (作者: PT27687, 时间: 1年前)

That's an interesting question about the relationship between alpha and scores! I believe that alpha can significantly influence outcomes by impacting various factors such as performance metrics or risk management criteria. It would be great to hear more about how you see this connection in your specific context. Could you provide more details?

---

### 评论 #16 (作者: PT27687, 时间: 1年前)

The relationship between scores and alpha can be quite complex. Generally, alpha indicates how much of the data set is being utilized effectively. It would be interesting to explore how different alpha values might impact score outcomes across various scenarios. Have you looked into specific examples or case studies that highlight this dependency?

---

### 评论 #17 (作者: AK40989, 时间: 1年前)

The scoring system for alphas based on Sharpe ratios and turnover is quite intricate, and it raises an important question about the implications of turnover changes during the OS phase. If an alpha initially qualifies under the low turnover criteria but later exceeds the threshold, how does that impact its overall score and eligibility in the competition

---

### 评论 #18 (作者: DK30003, 时间: 1年前)

That's an interesting question about the relationship between alpha and scores! I believe that alpha can significantly influence outcomes by impacting various factors such as performance metrics or risk management criteria.

---

### 评论 #19 (作者: PT27687, 时间: 1年前)

It's an interesting question you're raising about the correlation between alpha and scores. Some might argue that a higher alpha indicates better performance, but it could also depend on the strategies being used. Have you considered how different alpha values might affect various performance metrics? I'd love to hear more about your insights!

---

