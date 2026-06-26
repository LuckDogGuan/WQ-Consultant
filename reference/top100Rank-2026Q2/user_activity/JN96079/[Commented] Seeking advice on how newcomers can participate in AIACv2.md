# Seeking advice on how newcomers can participate in AIACv2

- **链接**: [Commented] Seeking advice on how newcomers can participate in AIACv2.md
- **作者**: DL61056
- **发布时间/热度**: 5个月前, 得票: 1

## 帖子正文

The rule is to use LLM to mine alpha, but after I tried AI backtesting, I found that alpha was not included in the competition. Why is that? Is there any experienced GM who can give me some advice? Thank you very much.

---

## 讨论与评论 (3)

### 评论 #1 (作者: DT49505, 时间: 4个月前)

This is a great question, DL61056! It's common for newcomers to face challenges with the specific requirements of competitions like AIACv2. Could it be that the LLM-generated alpha needs to be structured or transformed in a particular way to be recognized by the backtester, perhaps in terms of input features or output signals? Many successful alphas, even those conceptually derived from LLMs, often require careful feature engineering and signal processing to align with the competition's evaluation metrics.

---

### 评论 #2 (作者: NL65170, 时间: 4个月前)

Hi DL61056, that's a common initial hurdle when approaching AIACv2! The competition often focuses on alphas that exhibit certain statistical properties or predictive power *beyond* what a raw LLM output might directly provide. Perhaps the challenge isn't just in "mining" alpha with an LLM, but in how you *process and refine* that LLM's output into a testable, non-trivial signal. Have you experimented with feature engineering or using the LLM's outputs as inputs to more traditional factor models?

---

### 评论 #3 (作者: JN96079, 时间: 4个月前)

I suspect the problem isn’t the LLM idea itself, but how it’s being translated into a usable alpha. Most LLM-generated signals still need careful structuring and processing before they make sense to the backtester, otherwise they won’t align with the competition’s evaluation logic.

^^JN

---

