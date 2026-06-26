# A Delay-0 Checklist for  WorldQuant Submissions

- **链接**: A Delay-0 Checklist for  WorldQuant Submissions.md
- **作者**: BM29781
- **发布时间/热度**: 5个月前, 得票: 10

## 帖子正文

Use this checklist to ensure your alpha is  **truly delay-0** , structurally sound, and not accidentally behaving like delay-1.

### 1. Data Timing Check (Most Important)

- ✅ All fields are  **known on the same trading day**
- ❌ No fundamentals with reporting or revision lag
- ❌ No fields updated after market close

**Quick test:**

> *Could this value be known before today’s trading decision?*

### 2. Same-Day Logic Only

- ✅ Uses same-bar information (open, high, low, close, volume)
- ❌ Avoids operators that implicitly rely on yesterday’s close

**Good:**

`close - open
`

**Risky:**

`ts_delta(close, 1)
`

### 3. Cross-Sectional First, Time-Series Second

- ✅ Uses  `rank()`  or cross-sectional comparisons
- ❌ Avoids long confirmation windows

**Preferred:**

`rank(df)
`

**Slower:**

`ts_rank(return, 20)
`

### 4. Window Discipline

- ✅ Short, intentional windows (≤ 5–10)
- ❌ Long smoothing windows that introduce lag

**Delay-0 safe:**

`ts_mean(volume, 5)
`

### 5. Conditioning Over Smoothing

- ✅ Filters  *when*  to trade instead of heavily smoothing signals
- ❌ Avoids heavy decay that delays reaction

**Good:**

`trade_when(volume > ts_mean(volume, 20), alpha, 0)
`

### 6. Neutralization Is Mandatory

- ✅ Neutralized by industry / country unless explicitly macro
- ❌ No hidden market or sector drift

**Example:**

`neutralize(alpha, industry)
`

### 7. Extreme Value Control

- ✅ Caps or ranks signals to control noise
- ❌ No raw spikes

**Example:**

`clamp(rank(alpha), -2, 2)
`

### 8. Turnover & Stability Check

- ✅ Reasonable turnover
- ❌ No violent day-to-day flips

**Light smoothing only:**

`decay_linear(alpha, 3)
`

### 9. Delay Sanity Test

- Run the alpha at  **delay-1** :
  - If performance improves materially → it wasn’t delay-0
  - If performance degrades or stays similar → likely true delay-0

### 10. Canonical Delay-0 Template (Safe Baseline)

`trade_when(
  volume > ts_mean(volume, 20),
  decay_linear(
    neutralize(rank(close - open), industry),
    3
  ),
  0
)
`

## Final Rule of Thumb

> **If your alpha needs yesterday to explain today, it is not delay-0.**

True delay-0 alphas are  **aligned in data, logic, and execution timing** .

---

## 讨论与评论 (0)

