# Question about using reduce operators

- **链接**: Question about using reduce operators.md
- **作者**: PN39025
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

Hi guys I am learning about how to use reduce_ operators but there is no example of how to use. Can anyone give me a full example of how to use these operators?reduce_normreduce_sumreduce_maxreduce_minreduce_avgreduce_choosereduce_rangereduce_percentagereduce_stddevreduce_irreduce_skewnessreduce_kurtosisreduce_powersumreduce_count

---

## 讨论与评论 (7)

### 评论 #1 (作者: KS24487, 时间: 1年前)

I'd also like to learn more about these operators. The documentation is, well, to be honest not great at all on these. What does "reduce" mean here? Especially now that it's clear these operators are all available even for the GOLD level, they must be quite useful.

---

### 评论 #2 (作者: PP87148, 时间: 1年前)

Hi,Please find link of the community post where an alpha researcher explained the use of one of these reduce operator in combo expression.https://support.worldquantbrain.com/hc/en-us/community/posts/27626167187607-How-to-control-Alpha-selection-in-Super-Alpha

---

### 评论 #3 (作者: TD17989, 时间: 1年前)

A couple of additional ideas you could consider for further exploration:Moving Averages: Try using moving averages of the delta (e.g.,ma(ts_delta(close, 1), 5)) to smooth out noise and focus on the broader trend.Volume-based signals: Integrating volume data into your signals (e.g., looking at price change relative to volume) can help confirm the strength of a trend.Volatility-adjusted signals: For example, combining price changes with volatility (using indicators like the Average True Range or Bollinger Bands) can help account for market noise.

---

### 评论 #4 (作者: AG20578, 时间: 1年前)

HiPN39025andKS24487!reduce_operators should be used together with self_corr operator in combo expression of superalpha .Example:stats = generate_stats(alpha);innerCorr = self_corr(stats.returns, 500);ic = if_else(innerCorr == 1.0, nan, innerCorr);maxCorr = reduce_max(ic);1 - maxCorrHere innerCorr - is correlation of selected alphas with each other. Dimension of innerCorr (which is output of self_corr operator) is Days * Alpha * Alpha. But to simulate SuperAlpha we need as output Days * Alpha. That is why the use of reduce_operator is needed - to reduce the dimension of self_corr output.Ideas that you can explore further:* instead of calculating self_corr based on returns, you can calculate it based on drawdown, or other stats parameters of an alpha.* you can use different reduce_operators on top of self_corr, just remember that if you use self_corr, reduce_ operator is a must!* Please check out all articles on SuperAlpha indocumentation

---

### 评论 #5 (作者: BS20926, 时间: 1年前)

Hi AG20578 thanks for the explanation. I'd also like to learn more  about these operators.

---

### 评论 #6 (作者: RG93974, 时间: 1年前)

HiiiPN39025You can use the reduce operator only in a Super Alpha Combo Expression not for regular alpha submissions. If you are submitting a super alpha, you will then have access to use reduce operators within your combo expressions.For Example:stats = generate_stats(alpha);ic = reduce_norm(self_corr(stats.returns, 120));1/(1+ic)

---

### 评论 #7 (作者: PT27687, 时间: 1年前)

It’s great that you’re diving into reduce operators! These functions are really useful for various data manipulations. For instance, the `reduce_sum` operator can be used to calculate the sum of all elements in a dataset. If you’re looking for a comprehensive example, I can help create one that incorporates these operators in a real-world scenario, perhaps with some sample data. Would that be helpful?

---

