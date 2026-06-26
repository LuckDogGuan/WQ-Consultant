# How can I simulate and submit alpha D1 for the JPN region?

- **链接**: How can I simulate and submit alpha D1 for the JPN region.md
- **作者**: DM28368
- **发布时间/热度**: 1年前, 得票: 10

## 帖子正文

Hello everyone, in Q1/2025, I successfully ran and submitted many D1 alphas for the JPN region with relatively good metrics. However, in Q2/2025, when simulating with the required condition of the parameter Max trade = ON, the alpha metrics were poor and could not be submitted. Does anyone have any experience or tips on how to run and submit D1 alphas for the JPN region? Thank you.

---

## 讨论与评论 (2)

### 评论 #1 (作者: NM12321, 时间: 1年前)

I have also submitted quite a lot of JPN alpha, the datasets I usually run are fundamental, model, .... I usually keep the decay low.

---

### 评论 #2 (作者: PY62071, 时间: 1年前)

To simulate and submit aD1 alpha for the JPN regionon a platformWrite aFast-Expression (“ts()”-compatible)single-line or Python-based alpha tailored to Japanese stocks (e.g. TOP 1500 JPN), setdelay=1 (D1), definedecay, truncation, and choose yourneutralization(market or industry) settings. Then run your alpha in the simulator by selectingregion = JPN, choosing your universe and D1 configuration, and clickSimulate. The platform will evaluate metrics such asSharpe,Fitness,turnover, anddrawdown. If it passes quality thresholds (e.g., Sharpe > 2.5 for D1) you can enable theSubmit Alpha.

---

