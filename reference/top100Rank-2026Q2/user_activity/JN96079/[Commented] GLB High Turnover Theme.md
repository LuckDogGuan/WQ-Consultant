# GLB High Turnover Theme

- **链接**: [Commented] GLB High Turnover Theme.md
- **作者**: AK40989
- **发布时间/热度**: 1年前, 得票: 38

## 帖子正文

I noticed a new high-turnover theme is starting soon for the GLB region, and I’m still quite new to working in this universe. To prepare, I’d really appreciate some guidance from the community.

Are there any datasets you’ve found that tend to produce naturally high-turnover signals? Any specific fields or dataset types that are worth exploring for this theme would be super helpful.

Would really appreciate any insights you can share!

---

## 讨论与评论 (21)

### 评论 #1 (作者: PN39025, 时间: 1年前)

In my experience, if you create a price dataset, you are more likely to achieve the high revenue topic of GLB. Good luck.

---

### 评论 #2 (作者: NB52711, 时间: 1年前)

good

---

### 评论 #3 (作者: DN41247, 时间: 1年前)

This universe TOPDIV3000 is specialized for high turnover Alphas, so you should try every dataset you can to produce diverse of Alphas. As I try, model category can also get turnover of 40% and match theme.

---

### 评论 #4 (作者: KS69567, 时间: 1年前)

In my knowledge , if you can create a Price & Volume Data set and News & Sentiment data set, these dataset help to generate fast-acting signals ideal for high-turnover themes.

---

### 评论 #5 (作者: IK32530, 时间: 1年前)

Also Short-Interest Dataset can help you to make alpha

---

### 评论 #6 (作者: AY28568, 时间: 0年前)

You can try using datasets like price and volume & analyst updates or social media sentiment. These change fast and are good for high-turnover strategies. Also, look at short term signals or news events. Use ideas that react quickly to market moves. Hope this helps you get started.

---

### 评论 #7 (作者: HY24380, 时间: 11个月前)

I have submitted alphas in the GLB high turnover theme. However, this time, I found that it does not align with the theme, despite having a turnover of  **94.44%** .

Below is a screenshot. Let me know if why it is not matching GLB high turnover theme.

```

```

---

### 评论 #8 (作者: VO69741, 时间: 11个月前)

reduce trancation and decay. That code will fit to the theme !

---

### 评论 #9 (作者: JN96079, 时间: 11个月前)

Have you used the TOPDIV3000 universe?

---

### 评论 #10 (作者: HY24380, 时间: 11个月前)

[JN96079](/hc/en-us/profiles/25468856195607-JN96079)

Yes it is TOPDIV3000, GLB

---

### 评论 #11 (作者: HT92336, 时间: 10个月前)

Hi  [HY24380](/hc/en-us/profiles/5266969470615-HY24380) , according to the latest announcement, you need to adjust alpha so that Alphas must pass the IS ladder test to qualify for this theme. Tunover from 40,01-100%, Region"GLB", Universe"TOPDIV3000" . Good luck ![图片](images/img_d437100f9e.png)

---

### 评论 #12 (作者: LR13671, 时间: 10个月前)

Which datasets have consistently produced naturally high-turnover signals for GLB—especially beyond standard price/volume? Have you found event-driven sources (e.g., news sentiment, analyst revisions, short interest) to add meaningful diversity?

---

### 评论 #13 (作者: HY24380, 时间: 10个月前)

Hi  [LR13671](/hc/en-us/profiles/4516642748055-LR13671)

You can use news20 to get high turnover consistently.

---

### 评论 #14 (作者: LT94151, 时间: 10个月前)

Hi HY24380, I’m in the same situation as you — I had done it in TOPDIV3000 on the GLB market with turnover > 40%, but starting from August it no longer worked. I also don’t understand why.

---

### 评论 #15 (作者: TP19085, 时间: 10个月前)

Hi HY24380, I’m facing the same issue—my strategy worked well in TOPDIV3000 on the GLB market with turnover over 40%, but since August it stopped performing, and I’m not sure why. You might want to explore datasets like price, volume, analyst updates, or social media sentiment, as these change rapidly and suit high-turnover strategies. Focusing on short-term signals or news-driven events can help capture quick market moves. Have you identified any datasets beyond the usual price and volume that consistently generate naturally high-turnover signals for GLB? Also, do event-driven sources like news sentiment, analyst revisions, or short interest add meaningful diversity to your models? Sharing your experience could be really helpful!

---

### 评论 #16 (作者: NT84064, 时间: 10个月前)

For the GLB high-turnover theme, the most promising datasets are those with short-lived predictive effects, often tied to market microstructure or rapidly changing sentiment. Fields related to short-term volume surges, order book imbalance, bid-ask spread changes, and short interest updates can naturally lead to frequent portfolio turnover without artificially forcing it. Short-horizon price-based features such as intraday volatility, high–low range ratios, or small-window  `ts_rank()`  on returns also tend to decay quickly, aligning with the theme’s goal. You can also consider combining orthogonal datasets, such as pairing a fast-reacting sentiment signal with a liquidity constraint, to control slippage in high-turnover execution. Since the GLB region includes a diverse set of markets, cross-country validation is key — a signal that looks high-turnover in one region might behave differently in another due to trading calendar differences and liquidity conditions.

---

### 评论 #17 (作者: NT84064, 时间: 10个月前)

Thanks for starting this discussion — it’s exactly the kind of forward-looking preparation that helps everyone make the most of a new theme. I appreciate that you’re not just asking for general tips, but specifically for datasets that produce  *naturally*  high-turnover signals, because forcing turnover through artificial decay often weakens predictive power. Your question will likely encourage experienced consultants to share specific dataset types or fields that have worked well for them in the GLB region, which is a huge time-saver for those new to the universe. By opening this conversation early, you’ve created a valuable space for knowledge sharing before the theme officially begins.

---

### 评论 #18 (作者: HY24380, 时间: 10个月前)

Hi  [TP19085](/hc/en-us/profiles/7969854259351-TP19085)

There are many, but News20 is very consistent.

---

### 评论 #19 (作者: HY24380, 时间: 10个月前)

[LT94151](/hc/en-us/profiles/1918888836445-LT94151)

I think it is because of the fitness test. Now, to be eligible for the GLB high turnover theme, fitness must be >1.

Let me know if it looks correct.

---

### 评论 #20 (作者: LB76673, 时间: 9个月前)

For GLB high-turnover themes, datasets tied to  **short-horizon market activity**  often provide the richest ground. Things like intraday or daily  **liquidity and volume measures** ,  **short interest updates** , and  **analyst revision signals**  tend to move quickly and naturally generate higher turnover. In practice, even basic fields like rolling changes in volume, bid-ask spreads, or short interest ratios can yield signals with strong short-term dynamics. You might also find that news- or sentiment-driven fields, especially when smoothed lightly, add the volatility needed for fast rotation. Since GLB covers a broad set of markets, it helps to combine these with neutralization (region or industry) to avoid signals being dominated by a single area.

---

### 评论 #21 (作者: MH52691, 时间: 1个月前)

Thanks to everyone for their contributions. I'm very eager to research Alphas in this theme. However, I have been struggling with dataset selection.

---

