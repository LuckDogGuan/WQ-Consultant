# Methods For Enhancing After-Cost Performance

- **链接**: [Commented] Methods For Enhancing After-Cost Performance.md
- **作者**: CB60351
- **发布时间/热度**: 1个月前, 得票: 29

## 帖子正文

Improving After Cost Performance is important in improving  *Combined Alpha Performance.*  In this post, we'll discuss some tips on how to do better on After-cost  *Sharpe ratio.*

***1.**  **Manage Turnover*** : Average daily turnover and maximum daily turnover. Use turnover plots to find peaks in turnover daily. If average daily turnover is already low, work to decrease high peaks, if possible. Set up turnover control with tradewhen, hump, ts_target_tvr_delta_limit, and ts_delta_limit operators.

***2. Optimize Alpha Weights Distribution:***  Balance the distribution of Alpha weights in capitalization. Verify the size using visualization tools, making sure it's even or leaning towards high-capitalization stocks.

***3. Keep a High Coverage:***  Emphasize on maintaining good coverage, particularly in the liquid part of universe. At least 50% of the coverage should be in liquid stocks, and should be at least half of the universe. There is no need to have a large difference between the short and long counts.

***4. Review Sub-Universe Performance:***  Review sub-universe test scores and do not submit. Alphas just passing the Sub-universe Sharpe test. Any fields from the Universe dataset can be used to create your own sub-universe tests to test performance in all sub-universes.

***5. Enable Max Trade for Alphas in ASI region:***  Make sure that Max Trade is set to ON for all Alphas in the ASI region. This setting maximizes ASI Alphas and enhances 'after cost' performance at the combo level.

---

## 讨论与评论 (13)

### 评论 #1 (作者: BK74354, 时间: 1个月前)

Well stated.Thank you!!

---

### 评论 #2 (作者: JO96892, 时间: 1个月前)

Well put. Thank you and happy research!

---

### 评论 #3 (作者: AM35708, 时间: 1个月前)

Thank you for this input

---

### 评论 #4 (作者: JM47610, 时间: 1个月前)

This is interesting, well explained. Let me put this into action.

---

### 评论 #5 (作者: DN85880, 时间: 1个月前)

Thank youuu!!!

---

### 评论 #6 (作者: MO52425, 时间: 1个月前)

Thank you for this

---

### 评论 #7 (作者: VK29840, 时间: 1个月前)

this is very informative

---

### 评论 #8 (作者: VK30714, 时间: 1个月前)

Thank you for this

---

### 评论 #9 (作者: JM47610, 时间: 1个月前)

Great, This explanation is very clear, Well put.

---

### 评论 #10 (作者: MY82844, 时间: 1个月前)

Good summary! By the way, do you have any comments about Max Trade v.s. Max Position? From the simulation results, it seems that... they could both change the after cost performance a lot.

*========================================================*

*Pain + Reflection = Progress*

*========================================================*

---

### 评论 #11 (作者: KU30147, 时间: 1个月前)

Improve after-cost alpha performance by reducing turnover spikes, balancing alpha weights toward liquid/high-cap stocks, maintaining strong universe coverage, testing performance across sub-universes, and enabling Max Trade for ASI-region alphas. Focus on stable trading behavior, liquidity, and robust Sharpe ratios across different market segments.

---

### 评论 #12 (作者: AD47730, 时间: 1个月前)

I was looking for that nicely explained.

---

### 评论 #13 (作者: KP26017, 时间: 21天前)

Really practical checklist and the after-cost focus is exactly the right optimization target for Combined Alpha Performance — gross Sharpe improvements that don't survive cost adjustment don't translate into real pool contribution.

---

