# Anyone here experimenting with combo expressions?

- **链接**: [Commented] Anyone here experimenting with combo expressions.md
- **作者**: SP14747
- **发布时间/热度**: 9个月前, 得票: 19

## 帖子正文

I’m testing ways to combine multiple Alphas into a single SuperAlpha. Curious — do you use combos more for  **robustness**  or for  **performance boosts** ? And how do you pick which Alphas to include?

---

## 讨论与评论 (7)

### 评论 #1 (作者: TD40899, 时间: 9个月前)

I have the same concern as the author of this post. From my perspective, creating a solid combo expression is quite difficult and requires a lot of practice. I would be very thankful if someone could share more details, examples, or personal experiences on how to approach this challenge, so that I can learn and improve my own skills. Any guidance or explanation would be greatly appreciated. Thanks in advance for your support and for taking the time to help.

---

### 评论 #2 (作者: ZK79798, 时间: 9个月前)

That’s a great point. Personally, I lean toward using mainstream dataset alphas when building SuperAlphas, since they tend to be more reliable. For combining, I’ve often found equal-weighting works better in many cases—it avoids overfitting to any single alpha and keeps the SuperAlpha more stable across regimes. I see combos as a balance: robustness first, but if they also deliver a performance boost, that’s a nice bonus.

---

### 评论 #3 (作者: JN96079, 时间: 9个月前)

#### **Robustness**

When you merge several alphas, you’re diversifying across signals that might be based on different drivers—say, momentum, mean reversion, fundamentals, or price-volume relationships. This diversification helps:

- Reduce the impact of any single alpha failing in certain market conditions.
- Smooth out returns across changing environments.

#### **Use the following ways to combine alphas to get a super super alpha:**

#### **> Low Correlation**

Ideally, composite alphas should not be highly correlated with one another. Empirical analysis shows that  **pair-wise correlations are not strongly determined by turnover** , suggesting that many alphas with differing characteristics can coexist without undue redundancy.

#### **> Complementary Signal Types**

You’d want to mix alphas that derive from distinct data inputs—technical (price/volume), fundamentals, macro, news sentiment, etc.—to avoid overfitting and improve generalization.

#### **> Backtested Performance & Stability**

Each alpha should be evaluated in-sample and out-of-sample. Choose those that demonstrate consistent predictive power across periods, reducing the risk of overfitting.

#### **> Turnover & Cost Considerations**

While combining, keep an eye on turnover. Even though turnover per se doesn't strongly influence correlation, high turnover can increase trading costs. You may prefer some lower-turnover alphas to stabilize costs.

Thanks!

---

### 评论 #4 (作者: TP85668, 时间: 9个月前)

I find combo expressions valuable for both robustness and performance. The key is selecting low-correlation alphas to minimize overlap and enhance stability.

---

### 评论 #5 (作者: AG14039, 时间: 9个月前)

Exactly—that’s a solid approach. I also prefer using mainstream dataset alphas for SuperAlphas because they’re generally more reliable. In my experience, equal-weighting often works best for combining them, as it prevents overfitting to any single alpha and maintains stability across different regimes. I treat combos as a balance: prioritize robustness first, and consider performance gains as an added benefit.

---

### 评论 #6 (作者: JK98819, 时间: 9个月前)

Yes, I agree. I also use common dataset alphas for SuperAlphas since they’re more reliable. Equal-weighting works well because it avoids overfitting and keeps things stable. For me, the main goal is stability, and extra performance is just a bonus

---

### 评论 #7 (作者: RP41479, 时间: 9个月前)

I find combo expressions useful for boosting both robustness and performance. The key is choosing low-correlation alphas to reduce overlap and improve stability.

---

