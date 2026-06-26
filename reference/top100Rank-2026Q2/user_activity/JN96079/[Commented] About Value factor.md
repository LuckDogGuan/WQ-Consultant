# About Value factor

- **链接**: [Commented] About Value factor.md
- **作者**: AS13853
- **发布时间/热度**: 1年前, 得票: 22

## 帖子正文

How to increase value factor

---

## 讨论与评论 (19)

### 评论 #1 (作者: JC84638, 时间: 11个月前)

Based on my own experience — with my Value Factor going from 0.5→ 0.97 → 0.95 → 0.99 — I’d say we can’t truly rely on IS to predict OS. First, make sure Self Correlation isn’t too high, and that your Alpha isn’t just the result of stacking data fields and operators. Ideally, it should have clear logical meaning.
Try to submit Alphas with  **Turnover under 15%** , and occasionally include a few in the  **15%–50%**  range to help balance the signal. When you add a few higher-turnover Alphas into a low-turnover, high-margin pool, it can actually help  **reduce Drawdown**  even further.
Most importantly, keep tracking over time which types of Alphas tend to perform better in OS.

I'm not saying you should only submit Alphas with high Recent Year Performance — that would be a mistake. In reality, you also need to **include some seemingly average Alphas** , because they often contribute a lot to your portfolio.

By the way, my Combined after-cost OS is 3.56, and Selected OS is 4.52. (May. 2025)

![图片](images/img_7acaf8aa05.png)

Diversify — and then diversify some more. (JZC)

If you have any other questions, feel free to ask me!

---

### 评论 #2 (作者: SK13215, 时间: 1年前)

First of all.....

 **Delay Fundamental Fields----------------------** 
Use  `delay(field, n)`  to avoid look-ahead bias.

 **Filter Outliers---------------------------------------** 
Remove extreme values using  `filter`  or  `clip`  logic.

 **Combine with Momentum or Quality--------** 
Value alone may underperform; hybrid alpha is more robust.

 **Use Log Transform--------------------------------** 

 `log(pe_ratio)`  reduces skewed distribution.

 **Look at Growth-adjusted Value----------------** 
E.g.,  `pe_ratio / earnings_growth`  for PEG-like idea.

if u looking in these steps, that's some point u can understand, it definitely work on increasing the value factor.....

THANK YOU

---

### 评论 #3 (作者: HD25387, 时间: 1年前)

To increase the value factor, focus on improving traditional valuation metrics like earnings yield, book-to-price, or cash flow yield. Look for companies trading below intrinsic value with stable fundamentals. Reduce exposure to overpriced growth stocks. You can also enhance signals by neutralizing sector biases or combining value with quality. Consistent rebalancing improves factor purity.

---

### 评论 #4 (作者: PM97686, 时间: 1年前)

Focus on variables that show low pricing in relation to fundamentals in order to raise the value factor.  Typical techniques consist of:

**Utilize ratios of price to fundamentals:** 
 Include inverse measures such as earnings per price, earnings per PE, or earnings per PB.  Higher value is indicated by lower prices in relation to the fundamentals.

**Scale and rank value signals:**  To make value measurements comparable across industries or nations, use scale(), rank(), or group_zscore().

**Combine several value metrics** : To get a more reliable and varied value signal, combine a number of distinct valuation ratios (such as PE, PB, and EV/EBITDA).

**Group adjust to eliminate bias** : To prevent slanting too much toward value-heavy businesses (such as financials), use group_neutralize() or group_rank() by sector or industry.

---

### 评论 #5 (作者: PN39025, 时间: 1年前)

Hi, there is no fixed formula or experience to improve the value factor. It is run in the OS phase so it is difficult to control and in my opinion you should do alpha with clear ideas and not overfit, then you will improve the ability to get a higher value factor.

---

### 评论 #6 (作者: JO96892, 时间: 1年前)

I think you should focus on submitting quality alphas. Rember qaulity over quantity and always make sure your alphas meet the minimum thresholds of BRAIN Platform in terms of alpha requirements and IS Test. Utilize the notes in the learn section as well and join webinars to stay ahead on matters like this!

---

### 评论 #7 (作者: KS69567, 时间: 1年前)

Long-term success on the BRAIN platform requires concentrating on submitting high-quality alphas. Always put quality before quantity by making sure your submissions pass the IS Test and meet the minimal requirements. Make use of the insightful information in the "Learn" section, and attend webinars frequently to stay current. These tools are intended to help you stay in line with platform requirements and hone your strategy development abilities. You can improve your performance and raise the possibility that your alphas will be accepted and perform well by combining solid research, extensive testing, and ongoing learning. The secret to success is quality and consistency.

---

### 评论 #8 (作者: JN96079, 时间: 1年前)

Inconcur with everyone who has suggested some ways to improve value factor. Moreso  [JO96892](/hc/en-us/profiles/27901982608407-JO96892)  , also I belive the most import starting point of making sure the ends will be great, i.e value factor improvement and all most ever, making sure that all terms of alpha submission are fully met to the threshold is what one should aim first.

---

### 评论 #9 (作者: AY28568, 时间: 1年前)

Hi, improving the value factor isn’t easy since it depends on OS performance, which we can’t directly control. Instead of chasing high value scores, it's better to focus on building solid, logic-based alphas. Avoid overfitting and aim for consistency this will naturally improve your results over time.

---

### 评论 #10 (作者: JZ16161, 时间: 1年前)

It seems also value factor go hand on hand with combine alpha selected

---

### 评论 #11 (作者: TD37298, 时间: 0年前)

I think if you want to achieve a high value factor, first you need to make each of your alpha factors stronger, with a higher coefficient. Next, you should diversify across more regions and improve neutralization.

---

### 评论 #12 (作者: AD89110, 时间: 11个月前)

- It's not 100% clear how value factor increases, but there are some tips which can be helpful.
- Try to work on USA and GLB region more than any other region.
- Use different neutralization to check alpha performance.
- Create good performance alphas.

---

### 评论 #13 (作者: AS13853, 时间: 11个月前)

thanks everyone for such valuable comments

---

### 评论 #14 (作者: SK52405, 时间: 11个月前)

helpful

---

### 评论 #15 (作者: LR13671, 时间: 10个月前)

mproving the  **Value Factor**  isn't just about picking the right ratios — it's about creating  **robust, well-structured alphas**  that align with valuation logic while avoiding overfitting.

---

### 评论 #16 (作者: LR13671, 时间: 10个月前)

Avoid stacking too many operators or fields without logic; instead, each alpha should represent a distinct investment  **hypothesis** . Blend value with  **quality**  or  **momentum**  signals to improve resilience across regimes.

---

### 评论 #17 (作者: TP19085, 时间: 10个月前)

Achieving long-term success on the BRAIN platform hinges on submitting high-quality alphas rather than focusing on quantity. Ensuring your submissions pass the IS Test and meet all minimum requirements is essential. Utilize the valuable resources in the "Learn" section and participate in webinars regularly to stay updated and sharpen your strategy development skills. Combining thorough research, rigorous testing, and continuous learning increases the likelihood that your alphas will be accepted and perform well. Quality and consistency are the keys to success. When targeting value factors, focus on variables that show low prices relative to fundamentals. Common methods include using ratios like earnings-to-price or price-to-book, scaling and ranking value signals to normalize them across industries or countries, and combining multiple valuation metrics such as PE, PB, and EV/EBITDA for robustness. Group adjustments help remove bias toward sectors like financials by neutralizing or ranking within groups.

---

### 评论 #18 (作者: NS62681, 时间: 10个月前)

Improving Value Factor is tricky since it mainly reflects out-of-sample performance, which we can’t directly control. Rather than chasing scores, focus on building solid, logic-driven alphas, avoiding overfitting, and aiming for consistency over time, these practices will naturally lift your VF.

---

### 评论 #19 (作者: LB76673, 时间: 9个月前)

Increasing Value Factor generally comes down to improving both the uniqueness and robustness of your alphas rather than just chasing high Sharpe. One way is to reduce redundancy by diversifying datasets and operators so that each alpha adds incremental information instead of overlapping with others. Lowering production and self-correlation in your PowerPool is key, since highly correlated signals dilute contribution to VF even if their standalone Sharpe is strong. Neutralization also helps because it strips away broad market, sector, or cap biases, letting the true idiosyncratic signal show through. Stability across IS and OS windows matters a lot too, so filtering out alphas with sharp IS/OS decay will generally lift VF over time. Finally, balancing turnover and ensuring that extreme weights or outliers don’t dominate your signals can make the pool more consistent, which is also rewarded in VF.

---

