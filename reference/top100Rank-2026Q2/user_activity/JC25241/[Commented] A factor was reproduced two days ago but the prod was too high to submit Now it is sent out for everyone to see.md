# A factor was reproduced two days ago, but the prod was too high to submit. Now it is sent out for everyone to see.

- **链接**: [Commented] A factor was reproduced two days ago but the prod was too high to submit Now it is sent out for everyone to see.md
- **作者**: YK42677
- **发布时间/热度**: 1年前, 得票: 26

## 帖子正文

The basic idea is：

Volatility, IC absolute value close to 0.1

For volatility, there are many ways to calculate it, such as directly calculating the standard deviation (or variance) of the past N days' return, and averaging (or summing) the square of the past N days' return (similar to thinking that the mean of the return is 0 and then calculating the variance). There are also exponent-weighted summations of the squared returns of the past N days (the volatility factor in Barra CNE6). Here, we take the second approach and sum the squared returns of the last N days.

My expression：

![图片](images/img_001f3a7b35.png)

The setting is:

![图片](images/img_89c94e7e38.png)

The result is:

![图片](images/img_7ef70ad816.png)

![图片](images/img_7afa917f9b.png)

Add a word: actually quite surprised that such a simple expression can have a good effect!!

---

## 讨论与评论 (27)

### 评论 #1 (作者: NS94943, 时间: 1年前)

Interesting and simple alpha expression. Gives good performance, but I think the linear decay of 512 is too much and changes the original signal. You could try taking the mean values, use trading conditions or other operators to reduce turnover. Cheers!

---

### 评论 #2 (作者: UG81605, 时间: 1年前)

This is a simple reversion alpha. I can see that you took decay as 512 days, this comes in overfitting of the alpha. Such alphas can pass IS tests but will definitely fail in OS tests.

---

### 评论 #3 (作者: NT84064, 时间: 1年前)

Your approach to constructing a volatility-based factor is interesting, especially given its simplicity and effectiveness. The choice to sum the squared returns over a rolling window instead of using direct standard deviation calculations aligns with methodologies like GARCH models and EWMA volatility estimations, which place greater emphasis on recent price movements. One question that comes to mind is how sensitive this factor is to the choice of N (lookback period). Have you tested different values of N to see how stability and predictive power change? Additionally, given that IC absolute value is around 0.1, have you considered incorporating a normalization step or combining it with another factor (such as volume-based metrics) to enhance its robustness? Would love to hear more about any refinements you've explored!

---

### 评论 #4 (作者: NT84064, 时间: 1年前)

Thank you for sharing this factor and your thought process behind it! It’s always fascinating to see how even simple expressions can yield strong results when grounded in solid market intuition. Your post is a great reminder that complexity isn't always necessary—sometimes, straightforward and well-structured ideas perform just as well or even better. Also, your transparency in sharing this with the community is truly appreciated, as it encourages discussion and further improvements. Looking forward to more of your insights and any follow-ups on how this factor performs across different market conditions!

---

### 评论 #5 (作者: PW58059, 时间: 1年前)

Great job on this factor reproduction. I'm curious about the limitations of this volatility factor. Are there any market conditions or asset classes where you think it might not perform as well? And if so, how do you plan to address those limitations in the future?

---

### 评论 #6 (作者: SR82953, 时间: 1年前)

"Interesting approach! Summing the squared returns of the last N days can be a solid way to measure volatility, but as you mentioned, using a large decay value on price-volume data could create an artificially strong signal that might not hold up in live trading. It’s always valuable to explore diverse methodologies, but ensuring real-world applicability is key. Have you tested how this factor performs across different market regimes?"

---

### 评论 #7 (作者: KY24675, 时间: 1年前)

The decision to send out the factor now suggests that it’s been reviewed or adjusted to meet necessary standards. The initial hesitation to submit the high value likely reflected concerns about its accuracy or suitability. Moving forward, clear communication about the review process, any changes made, and the rationale behind sending it out now will help maintain credibility and ensure the stakeholders understand why it’s now considered appropriate to share.

---

### 评论 #8 (作者: NA80407, 时间: 1年前)

This is a straightforward mean reversion alpha. I noticed you used a decay of 512 days, which leans towards overfitting. While such alphas might perform well in IS tests, they are likely to struggle in OS tests

---

### 评论 #9 (作者: HQ17963, 时间: 1年前)

Good try! This expression assigns negative weight to stocks with larger absolute returns, which likes a reversal trading strategy. At the same time, you use a large decay(512) to reduce turnover.
I think the alpha can be improved by considering the positive and negative returns, because negative returns and positive returns obviously have different effects on prices. You can try to replace pow with  **signed_power** to achieve this. Let's keep passion!!

---

### 评论 #10 (作者: SC73595, 时间: 1年前)

Your approach to constructing a volatility-based factor is quite interesting, particularly in its balance of simplicity and effectiveness. Using the sum of squared returns over a rolling window instead of direct standard deviation calculations aligns well with methodologies like GARCH models and EWMA volatility, which prioritize recent price movements.

One aspect I’m curious about is the sensitivity of the factor to the choice of N (lookback period). Have you tested different values to assess how stability and predictive power vary? Additionally, with the IC absolute value around 0.1, have you considered incorporating a normalization step or integrating it with another factor—perhaps volume-based metrics—to enhance robustness?

Would love to hear more about any refinements you’ve explored!

---

### 评论 #11 (作者: HD25387, 时间: 1年前)

That's a great insight! Sometimes the most elegant alphas come from simple yet powerful ideas, especially when backed by solid statistical reasoning like volatility clustering. Even if the prod correlation was high this time, it’s still a valuable concept — perhaps tweaking the normalization or conditioning could help reduce correlation while preserving signal strength. Keep experimenting! 🚀

---

### 评论 #12 (作者: CH36668, 时间: 1年前)

Interesting and straightforward alpha expression! It delivers solid performance, but the linear decay of 512 might be too aggressive, potentially distorting the original signal. You could experiment with taking mean values, incorporating trading conditions, or applying different operators to help reduce turnover.

---

### 评论 #13 (作者: NT84064, 时间: 1年前)

This is an interesting approach to capturing volatility! The use of exponent-weighted summations provides a more adaptive measure of recent price fluctuations compared to simple rolling variance. Given that your IC absolute value is close to 0.1, it suggests some predictive power—have you tested different decay rates for the weighting to see if certain values improve stability? Additionally, considering the factor’s high production cost, have you explored normalization techniques or alternative parameter tuning to enhance efficiency? It would be fascinating to see how this factor performs in different market conditions or when combined with other risk-adjusted signals.

---

### 评论 #14 (作者: DP14281, 时间: 1年前)

The decay you have set up is 512, which will completely change the original signal. Generally it is a good practice that you should keep your decay in setting below 10.

---

### 评论 #15 (作者: MA97359, 时间: 1年前)

Using higher decay to generate signals might not always be ideal. Instead, focus on  **effective operators**  and consider the  **mean of data fields**  to extract more robust signals.

---

### 评论 #16 (作者: SV78590, 时间: 1年前)

Your approach to building a volatility-based factor is intriguing—simple yet highly effective. Summing squared returns over a rolling window instead of using direct standard deviation calculations aligns well with methodologies like GARCH models and EWMA volatility estimates, which emphasize recent price movements.

One question that comes to mind:  **How sensitive is this factor to the choice of N (lookback period)?**  Have you tested different values of N to analyze its impact on stability and predictive power?

Also, with an IC absolute value of around 0.1, have you considered  **normalization**  or combining it with another factor (e.g., volume-based metrics) to improve robustness? Would love to hear more about any refinements you've explored!

---

### 评论 #17 (作者: AK40989, 时间: 1年前)

It's interesting to see how a straightforward approach to calculating volatility can yield effective results. The use of squared returns for volatility measurement seems to capture essential market dynamics without overcomplicating the model.

---

### 评论 #18 (作者: HD25387, 时间: 1年前)

That's really interesting! Sometimes the simplest expressions reveal powerful insights, especially with volatility-based factors. Curious to see how it performs across different regions or when adjusted with a decay or normalization layer.

---

### 评论 #19 (作者: RK48711, 时间: 1年前)

It’s fascinating how a simple method for calculating volatility can produce impactful outcomes. Using squared returns to measure volatility effectively captures key market behaviors without adding unnecessary complexity to the model.

---

### 评论 #20 (作者: RC82292, 时间: 1年前)

It’s always valuable to explore diverse methodologies, but ensuring real-world applicability is key.  The initial hesitation to submit the high value likely reflected concerns about its accuracy or suitability.I think the alpha can be improved by considering the positive and negative returns, because negative returns and positive returns obviously have different effects on prices.

---

### 评论 #21 (作者: DK30003, 时间: 1年前)

Good try! This expression assigns negative weight to stocks with larger absolute returns, which likes a reversal trading strategy. At the same time, you use a large decay(512) to reduce turnover.
I think the alpha can be improved by considering the positive and negative returns, because negative returns and positive returns obviously have different effects on prices.

---

### 评论 #22 (作者: JC25241, 时间: 1年前)

Your volatility factor is simple and effective, similar to GARCH and EWMA models. How does it perform with different values of N (lookback period)? Have you considered normalizing it or combining it with other factors like volume to improve robustness?

Thanks for sharing! Simple methods based on solid intuition can be powerful. I look forward to hearing more about its performance in different market conditions.

The approach is solid, but large decay values may create overly strong signals in live trading. Have you tested it across different market regimes?

---

### 评论 #23 (作者: AY46244, 时间: 1年前)

That's a great insight! Sometimes the most elegant alphas come from simple yet powerful ideas, especially when backed by solid statistical reasoning like volatility clustering.

---

### 评论 #24 (作者: HD25387, 时间: 1年前)

Impressive how such a basic volatility formulation still holds predictive power. Sometimes simplicity captures structural inefficiencies better than complex constructions. Curious how it behaves across different universes—especially in low-liquidity segments. Thanks for sharing!

---

### 评论 #25 (作者: NT84064, 时间: 1年前)

It's always exciting to see a simple factor achieve strong results. The approach you're using to calculate volatility by summing the squared returns of the past N days is a straightforward yet effective method to capture market fluctuations. It’s interesting that you’re not just focusing on the traditional standard deviation, but on an exponentially weighted sum, which can help emphasize more recent price changes. This technique is likely to be more responsive to recent market conditions, allowing for better reflection of short-term volatility. The fact that such a simple expression has had a good effect just goes to show that sometimes less is more in factor modeling—keeping things straightforward can sometimes yield impressive results without overcomplicating the model.

---

### 评论 #26 (作者: NT84064, 时间: 1年前)

Fascinating approach to volatility calculation! The second method of summing the squared returns of the past N days, especially with exponent-weighting, is an interesting way to capture short-term volatility trends without overcomplicating the calculation. The volatility factor's sensitivity to the choice of N days is always a key consideration, and it’s great to see how it’s been tuned for this model. The simplicity of the expression is indeed a pleasant surprise, but as you mentioned, simplicity often leads to robustness, particularly when combined with effective risk measures like IC. It would be interesting to see how this compares when tested across different market regimes.

---

### 评论 #27 (作者: SK90981, 时间: 1年前)

Surprising how a simple volatility expression using squared returns can yield such solid results—sometimes simplicity really works!

---

