# 🎉 Migrating Alphas to the New Universes: Initial Thoughts on MINVOL10M and USA TOP2000

- **链接**: [Commented] Migrating Alphas to the New Universes Initial Thoughts on MINVOL10M and USA TOP2000.md
- **作者**: CM46415
- **发布时间/热度**: 2个月前, 得票: 33

## 帖子正文

Hi everyone,

🎉 Exciting news regarding the newly onboarded universes! With the addition of  **USA TOP2000** ,  **ASI TOP500** ,  **ASI MINVOL10M** , and  **GLB MINVOL10M** , I’m curious to see how everyone is adapting their research workflows. These open up some great opportunities, but also bring new challenges for signal durability.

Here is what I am currently testing as I port my existing alphas over:

**1. The Built-in Liquidity Filter (MINVOL10M)**  For the  `GLB MINVOL10M`  and  `ASI MINVOL10M`  universes, having a strict 10 million minimum volume constraint baked in is a huge time-saver. In the past, applying complex mean-reversion signals to global datasets often resulted in great In-Sample scores that instantly collapsed Out-of-Sample (OS) due to illiquid micro-caps skewing the results. I'm finding that I can relax some of my manual  `adv20`  filters when building for these universes, allowing the model to breathe a bit more.

**2. Rethinking Neutralization for USA TOP2000**  Expanding into the  `USA TOP2000`  provides a much wider playground than the Top 500, but it introduces a lot of mid-cap volatility. I'm noticing that my standard risk-neutralization techniques (which worked fine on mega-caps) are struggling slightly here. To maintain OS performance, I'm having to apply much stricter  `group_neutralize`  functions specifically targeting Sub-Industries rather than just broad Sectors.

**3. Cross-Regional Signal Robustness**  I'm currently running an experiment: taking alphas that show strong, risk-neutralized OS performance in the US and running them directly on  `ASI TOP500`  without changing the core expression. The decay rates are vastly different, suggesting that alpha half-lives in the Asian markets require different  `decay_linear`  parameters.

I’d love to hear your initial findings:

- Have you found that your Sharpe ratios naturally improve in the  `MINVOL10M`  universes due to the exclusion of low-liquidity noise?
- Are you building entirely new expressions for  `USA TOP2000` , or just adjusting the risk/decay parameters of your existing signals?

Looking forward to the discussion!

---

## 讨论与评论 (7)

### 评论 #1 (作者: HC86622, 时间: 2个月前)

New universe will releave the challenge of prod correlationship

---

### 评论 #2 (作者: HO41126, 时间: 2个月前)

New universe will help with prod correlation and also balancing tier breaker

---

### 评论 #3 (作者: EM39360, 时间: 2个月前)

solid insights, this will really help to counter production correlation especially in USA region.

---

### 评论 #4 (作者: JM48331, 时间: 2个月前)

**We are on it**

---

### 评论 #5 (作者: MR43525, 时间: 2个月前)

Much educative

---

### 评论 #6 (作者: KP26017, 时间: 2个月前)

Minimum volatility universe construction is fundamentally different from liquidity-based construction and opens genuinely distinct research territory. MINVOL10M selects for low volatility names with minimum liquidity threshold — which creates a universe with different factor exposure characteristics, different return distribution properties, and different crowding dynamics than standard liquidity-ranked universes.

---

### 评论 #7 (作者: SE19816, 时间: 2个月前)

Yes, expanding to USA TOP2000 helps reduce prod correlation. I also found that sub-industry  `group_neutralize`  is necessary to handle the added mid-cap volatility

---

