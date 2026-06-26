# High-Correlation Alphas with Higher Sharpe: Safe to Submit or Long-Term Risk?

- **链接**: [Commented] High-Correlation Alphas with Higher Sharpe Safe to Submit or Long-Term Risk.md
- **作者**: FM47631
- **发布时间/热度**: 10个月前, 得票: 8

## 帖子正文

In WQB, it’s technically acceptable to submit alphas with  **production correlation above the stated threshold**  to other consultant alphas  **if the new alpha’s Sharpe is 10% higher or more** .

From a  **long-term performance and credit perspective** , will repeatedly submitting such highly correlated but slightly superior alphas:

1. **Negatively impact my evaluation or future model contribution** ,
2. Or is this considered fully acceptable practice given the Sharpe uplift?

I’m curious how others approach the trade-off between  **Sharpe improvement**  vs.  **correlation-driven redundancy**  when prioritizing alpha submissions.

---

## 讨论与评论 (11)

### 评论 #1 (作者: JN96079, 时间: 10个月前)

It is true what you have stated, i.e., acceptable to submit the same alpha but with higher Sharpe the second or third time of submission. However, it's not advisable since in the long run, it will not be adding value at all to the pool of alphas. So, from my point of view, doing that one time is okay if you have run out of ideas, but do not do that the second time, just try to make a new idea, a new signal to add value and diversity to the signal pool.

---

### 评论 #2 (作者: JC84638, 时间: 10个月前)

Sometimes, I submit Alphas that perform about 10% better, but only for the stronger ones. When maximizing submission volume, it’s crucial to avoid using too many weak Alphas.

**If possible, you should be able to submit Alphas with +20% sharpe or more.**

**(Remember to keep the turnover from getting too high.)**

If u have any other questions, feel free to ask me~

---

### 评论 #3 (作者: AM71073, 时间: 10个月前)

Great question—this is a subtle trade-off many of us face. While the platform allows submission of correlated alphas with ≥10% Sharpe improvement, relying heavily on such submissions might raise concerns over  **true innovation**  and  **long-term portfolio diversification** .

In my experience, it's best to treat these as  **tactical enhancements**  rather than core strategy—use them selectively when the improvement is meaningful and the signal behavior is clearly refined. For long-term credit strength and model inclusion,  **uniqueness and orthogonality**  still matter a lot. I try to balance both by maintaining a base of low-correlated signals while iteratively improving strong families with modest overlap. Curious how others are thinking about this trade-off too!

---

### 评论 #4 (作者: PT23235, 时间: 10个月前)

Hi  [JC84638](/hc/en-us/profiles/28348489344151-JC84638) 
I am a newbie so sometimes I can't handle data well.
Do you mind if I ask how to handle/combine News/Sentiment datasets? Please share your experience with alpha processing or strategies with me, I would appreciate it.

---

### 评论 #5 (作者: ML46209, 时间: 10个月前)

It’s technically fine to submit highly correlated alphas if the Sharpe is meaningfully higher, but  **long-term value comes from diversity** , not small improvements. One-time submission of a stronger correlated alpha can be okay, but repeatedly submitting similar signals risks redundancy and won’t add real contribution to the pool.

A practical approach is to focus on  **new ideas or orthogonal signals** —or only submit correlated alphas if the Sharpe uplift is substantial (e.g., +20%) and turnover remains reasonable. Balancing Sharpe improvement with pool diversity usually yields better long-term performance and evaluation.v

---

### 评论 #6 (作者: JC84638, 时间: 10个月前)

[PT23235](/hc/en-us/profiles/27841870878743-PT23235)  Just like you would process fnd, mdl, anl data, but you may need to pay attention to the update frequency and value range.  **nws**  and  **snt**  often have highly discrete distributions, which means you should consider applying  **winsorize** ,  **log(data + k)** ,  **s_log_1p** ,  **tanh** ,  **rank** , etc., to compress them. (jzc

---

### 评论 #7 (作者: LB76673, 时间: 10个月前)

From what I’ve seen, submitting alphas that clear the Sharpe uplift rule (≥10% higher even with correlation above the threshold) is fully within the platform’s rules and won’t get flagged as “incorrect” behavior. However, the long-term credit and contribution picture tends to favor diversity.

If most of your submissions are highly correlated with each other (even if Sharpe is a bit higher), then over time your pool of alphas might not add as much incremental value to the global model. This can indirectly limit your credit impact, since credits scale with unique contribution and robustness. On the other hand, consistently offering uncorrelated alphas with stable performance usually compounds better in the long run.

A good middle ground is to keep some high-Sharpe “upgrades” for existing logic (to show signal refinement), but balance them with exploratory submissions in new universes, horizons, or operator structures that drive correlation down. That way you’re delivering both quality improvements and differentiated signals.

---

### 评论 #8 (作者: NS62681, 时间: 10个月前)

Submitting correlated alphas is acceptable if the Sharpe gain is significant, but true long-term value comes from diversity. A one-time stronger correlated alpha may be fine, but repeated similar signals add little. It’s better to focus on new or orthogonal ideas, or only submit correlated alphas when the Sharpe uplift is substantial with reasonable turnover. Balancing Sharpe and diversity ensures stronger long-term performance.

---

### 评论 #9 (作者: AG14039, 时间: 9个月前)

Yes, it’s true that you can resubmit the same alpha with a higher Sharpe on a second or third attempt. That said, it’s generally not recommended, since over time it doesn’t really contribute new value to the alpha pool. In my view, doing it once is fine if you’re short on ideas, but repeating it isn’t worthwhile—better to focus on creating fresh signals that bring diversity and add meaningful value.

---

### 评论 #10 (作者: AG14039, 时间: 9个月前)

Submitting correlated alphas can be fine if they deliver a meaningful Sharpe improvement, but lasting value comes from diversity. A single strong correlated alpha may be worth it, but repeatedly submitting similar signals adds little benefit. It’s generally better to prioritize novel or orthogonal ideas, or only include correlated ones when the Sharpe gain is substantial and turnover stays manageable. Striking the right balance between Sharpe and diversity leads to stronger, more sustainable performance.

---

### 评论 #11 (作者: HY90970, 时间: 9个月前)

High prod correlated alphas with higher sharpe can be submitted technically and are fine to submit if:

- self correlation between your such alphas is low or moderate.

- you are not submitting similar alpha by increasing sharpe by 10% each time.  like 2 ->2.3 -> 2.7 and so on.

---

