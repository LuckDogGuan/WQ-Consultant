# Combined selected alpha performance

- **链接**: [Commented] Combined selected alpha performance.md
- **作者**: LS84247
- **发布时间/热度**: 1年前, 得票: 10

## 帖子正文

Someone to explain to me what is considered to improve combined selected alpha performance please.

---

## 讨论与评论 (12)

### 评论 #1 (作者: JC84638, 时间: 1年前)

That’s a great question!
I’m still relatively new to WQ, but from what I’ve seen, having strong  **Combined Alpha Performance**  usually leads to solid  **Combined Selected Alpha Performance**  — mine is currently 1.98 / 2.13.

Lowering correlation can also make a big difference. You might also want to look at how some users with Combined Selected Alpha above 3 are building their strategies.

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

I think you should diversify in many different datasets, it can neutralize risk and volatility.

---

### 评论 #3 (作者: AK40989, 时间: 1年前)

To enhance Combined Selected Alpha Performance, it's essential to implement several key strategies. First, ensure that your alphas meet the necessary eligibility criteria for inclusion. Continuously optimize your trading strategies to improve their effectiveness, and regularly review performance metrics to identify areas for enhancement. Effective risk management techniques should be employed to safeguard against potential losses, while diversifying your alpha sources can lead to better overall results. By focusing on these aspects, you can significantly improve your Combined Selected Alpha Performance and achieve more consistent outcomes.

---

### 评论 #4 (作者: TD84322, 时间: 1年前)

To be honest, I’m not completely sure how to achieve a very high combined performance. But from what I understand, the key factors are having low correlation between alphas and maintaining a high Sharpe ratio. That seems to be the main idea behind the formula.

---

### 评论 #5 (作者: PP87148, 时间: 1年前)

Hi,

Combined selected Alpha Performance is a subset of Combined Alpha Performance, If your CSAP is lower than your CAP suggests the Alphas selected by WQ have weaker performance than your complete Alpha pool and vice versa.

So you should focus on increasing CAP, to increase CAP follow the below techniques.

- **Control Turnover:**
  - Monitor both average and max daily turnover.
  - Use turnover plots to find and reduce peaks.
  - Try:  `tradewhen` ,  `hump` ,  `ts_target_tvr_delta_limit` ,  `ts_delta_limit` .
- **Balance Alpha Weights:**
  - Ensure weights are well-distributed across capitalization sizes.
  - Use visuals to check for even or large-cap skewed exposure.
- **Maintain High Coverage:**
  - Aim for long + short count to cover at least half the universe.
  - Focus on liquid stocks.
  - Avoid excessive short bias (shorts ≫ longs).
- **Check Sub-Universe Performance:**
  - Don’t rely on alphas that barely pass sub-universe tests.
  - Build custom sub-universe tests using Universe dataset fields.

---

### 评论 #6 (作者: AC63290, 时间: 1年前)

Improving combined alpha performance requires diversifying signals, minimizing correlation, controlling turnover, optimizing weights, ensuring robust backtesting, and integrating feedback from real trading conditions for better risk-adjusted returns.

---

### 评论 #7 (作者: ML46209, 时间: 1年前)

Improving Combined Selected Alpha Performance really comes down to balancing diversity and quality. Focus on reducing correlation between alphas while maintaining strong individual performance. Also, managing turnover and ensuring good coverage across liquid stocks help keep the overall strategy stable and effective.

---

### 评论 #8 (作者: SP39437, 时间: 1年前)

To improve Combined Selected Alpha Performance (CSAP), you should focus on optimizing your overall Combined Alpha Performance (CAP), since CSAP is derived from the alphas selected by WorldQuant based on your broader alpha pool. If your CSAP is lower than your CAP, it often means the selected alphas underperform compared to your total submission.

Key strategies include controlling turnover—both average and max daily. Use tools like  `tradewhen` ,  `hump` , and  `ts_target_tvr_delta_limit`  to smooth spikes. Balance your alpha weights across different market caps to avoid large-cap concentration. Aim for high coverage: a good rule is to have your long and short positions span at least half the universe. Stay focused on liquid stocks and avoid excessive short-only biases. Also, always validate alpha performance across sub-universes using Universe dataset fields, ensuring robustness.

What techniques have you found most effective in boosting CSAP without increasing correlation or turnover too much?

---

### 评论 #9 (作者: TP18957, 时间: 1年前)

Improving  **Combined Selected Alpha Performance (CSAP)**  is all about enhancing both the  **quality**  and  **diversity**  of your alpha pool. Since CSAP reflects the performance of alphas  **selected by WQ from your submissions** , a good starting point is to consistently submit  **low-correlated, high-performing alphas**  with stable Sharpe ratios.

You should also aim to:

- **Reduce correlation**  between your alphas to increase marginal value.
- **Control turnover** , using tools like  `tradewhen`  and  `ts_delta_limit` , to avoid instability.
- **Balance exposure**  across different market caps and sectors.
- **Ensure high coverage**  with both long and short positions across a broad universe.
- Run  **sub-universe tests**  to confirm your alpha performance generalizes well.

Focus on improving  **Combined Alpha Performance (CAP)**  first, because CSAP is ultimately a subset. If you maintain CAP > 2.0 with low correlation, your CSAP will likely follow suit.

---

### 评论 #10 (作者: TP18957, 时间: 1年前)

Thanks so much LS84247 for asking this—it’s a question I think many of us have as we aim to grow within the WQ platform. I really appreciated all the insightful responses here, especially from consultants who’ve achieved strong performance metrics. It’s encouraging to know that improving CSAP isn’t just about chasing numbers, but about developing thoughtful, well-rounded strategies—diversifying datasets, managing turnover, and constantly iterating. The idea that CSAP reflects the best from your alpha pool really motivates me to focus more on correlation and robustness. Thanks again for opening this discussion—it’s definitely given me new ideas for what to try next!

---

### 评论 #11 (作者: TP19085, 时间: 1年前)

To raise your  **Combined Selected Alpha Performance (CSAP)** , the most effective starting point is improving your  **Combined Alpha Performance (CAP)** . Since CSAP reflects the subset of your alphas chosen by WorldQuant, a low CSAP relative to CAP often signals that selected alphas are underperforming your broader pool.

Key tactics include managing both  **average and max daily turnover** . Use operators like  `tradewhen` ,  `hump` , or  `ts_target_tvr_delta_limit`  to limit volatility and reduce unnecessary rebalancing. Ensure your alpha exposures are  **evenly distributed across market caps**  to avoid over-concentration in large-cap names. Also, aim for  **broad coverage** —long and short positions should ideally span at least 50% of the universe.

Stick to  **liquid stocks**  and avoid overly short-heavy exposures. Additionally, test for robustness by validating performance across  **sub-universes**  using fields from the Universe dataset.

—What techniques have helped you boost CSAP while keeping correlation and turnover in check?

---

### 评论 #12 (作者: MA14841, 时间: 9个月前)

Why I can't see my Combined Selected Alpha Performance- It is showing "No matching Alphas", i am new to WQ and have created more than 150 Alphas but still i can't see this score.

---

