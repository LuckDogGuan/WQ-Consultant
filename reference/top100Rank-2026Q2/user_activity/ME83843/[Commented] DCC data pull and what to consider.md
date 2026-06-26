# DCC data pull and what to consider

- **链接**: [Commented] DCC data pull and what to consider.md
- **作者**: EM11875
- **发布时间/热度**: 3个月前, 得票: 17

## 帖子正文

Hi , I am pulling data in batches for the 2yr period , i..e 2021 and whole of 2022, if it normal when simulating the data to partly lack some values on some of the months ,, yet it is a competitive company selection.

What consideration should I have to ensure I don't have a data  gap, I have simulated the field also by trying to backfill 1 month trading period but still missing out on something,

---

## 讨论与评论 (4)

### 评论 #1 (作者: JN96079, 时间: 3个月前)

Try to fill the nans by winsorizing. That way, you can get better-structured, more competent data that will boost alpha performance!

^^JN

---

### 评论 #2 (作者: EM11875, 时间: 3个月前)

This worked, Thanks  [JN96079](/hc/en-us/profiles/25468856195607-JN96079) 

Especially backfilling the data point created in your alpha considering it's a 2yr range, while using NAN handling  techniques that handles part of this data gaps.

---

### 评论 #3 (作者: JN96079, 时间: 3个月前)

Great. Happy learning!

^^JN

---

### 评论 #4 (作者: ME83843, 时间: 3个月前)

Yeah, this can happen and it’s fairly common depending on the dataset. Even with good coverage, some fields have reporting delays, gaps, or irregular updates—especially fundamentals or less liquid names.

A few things you can check:
•  **Coverage consistency**  – some fields drop coverage in certain months or regions
•  **Update frequency**  – quarterly data will naturally look sparse in daily sims
•  **Backfill window**  – 1 month might be too short; sometimes extending it helps if the data is slow-moving
•  **Universe changes**  – stock additions/removals can create apparent gaps

Also worth checking if the signal still behaves well after handling missing values, rather than trying to force full coverage. Curious if others have found better ways to deal with this too.

---

