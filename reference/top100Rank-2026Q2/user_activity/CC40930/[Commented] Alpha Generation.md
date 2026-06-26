# Alpha Generation

- **链接**: [Commented] Alpha Generation.md
- **作者**: PW79735
- **发布时间/热度**: 2年前, 得票: 3

## 帖子正文

Any help will be appreciated! I'm trying to build my first alpha, but nothing has worked until now. Here are some of the current ideas that I came up with:

signal = abs(ts_mean(close, 10)/ ts_mean(close, 200) - 1); -signal * sign(returns);

I need to improve two IS testing Status: 

- [Fitness](/hc/en-us/articles/20251386376471)  of  **0,48**  is below cutoff of  **1** .
- [Turnover](/hc/en-us/articles/20251419309719)  of  **85,59%**  is above cutoff of  **70%** .
  And have a pending one too:
  - Self-correlation check pending.

---

## 讨论与评论 (14)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hello there!

Let's tackle these errors one at a time, starting with turnover 😊. As you can see from this formula: Fitness = Sharpe * sqrt(abs(Returns) / Max(Turnover, 0.125)), reducing turnover might help you increase fitness.

Here are a couple of strategies that could help:

1. You could try reducing turnover by using the trade_when operator. For example:
   ```
   trade_when(rank(ts_mean(returns, 20)) > 0.5, -signal * sign(returns), -1)
   ```
2. Consider using an aggregate instead of daily returns. For example:
   ```
   -signal * sign(ts_decay_linear(returns, 20))
   ```

The message "Self-correlation check pending" indicates that this check hasn't been performed yet, as the alpha fails other checks (Fitness and Turnover).

Give it a shot and let me know how it goes!

---

### 评论 #2 (作者: PW79735, 时间: 2年前)

Thanks for the reply! And sorry for seeing this, just now. I will try your suggestions. Where can I find more documentation about Fast Expression Language and Alpha Generation?

---

### 评论 #3 (作者: XL31477, 时间: 1年前)

Hey , for more documentation on Fast Expression Language and Alpha Generation, you can check the official WorldQuant Brain platform docs. Usually, there are detailed guides on functions, operators and how to build alphas there. Also, search in the platform's help section or community forum archives. Some experienced users might've shared useful insights before. Hope these tips work for you and good luck with improving your alpha!

---

### 评论 #4 (作者: CC40930, 时间: 1年前)

Great start with your alpha strategy! For improving the fitness, you might want to consider adjusting the time periods or incorporating additional indicators like volatility or momentum to refine your signal. Regarding turnover, reducing trade frequency by using longer time periods for moving averages could help. Also, keep an eye on self-correlation – detrending the signal or introducing lagged features might assist with that. Keep testing and iterating; the key is fine-tuning until the results align with your criteria.

---

### 评论 #5 (作者: NH84459, 时间: 1年前)

It sounds like you're working on building a trading  **alpha**  based on certain signal calculations, but you're encountering challenges with your  **in-sample (IS) testing**  metrics, such as  **fitness**  and  **turnover** . I'll break down your current approach and provide suggestions for improving the  **fitness**  and  **turnover** , as well as address the  **pending self-correlation check** .

###

---

### 评论 #6 (作者: KS69567, 时间: 1年前)

Your alpha approach is off to a strong start! Refine your signal by adjusting the time periods or adding other indicators like momentum or volatility to increase its fitness. Reducing the frequency of trades by choosing longer moving average periods may help manage turnover. Robustness may be enhanced by detrending the signal or adding lag characteristics to address self-correlation. Adjust the parameters and keep a careful eye on the outcomes to make sure the approach is meeting your performance goals. Iteration and continuous testing are crucial. Keep improving since doing so will get you closer to a more dependable and successful strategy.

---

### 评论 #7 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #8 (作者: AK98027, 时间: 1年前)

Your alpha approach is off to a strong start! Refine your signal by adjusting the time periods or adding other indicators like momentum or volatility to increase its fitness. Reducing the frequency of trades by choosing longer moving average periods may help manage turnover. Robustness may be enhanced by detrending the signal or adding lag characteristics to address self-correlation. Adjust the parameters and keep a careful eye on the outcomes to make sure the approach is meeting your performance goals.

---

### 评论 #9 (作者: CC40930, 时间: 1年前)

"Building your first alpha can be tricky, but you're on the right track by experimenting with different ideas! For your signal, the use of  `ts_mean`  is a good start for smoothing the data, but improving fitness and reducing turnover might require refining your strategy. Consider adding additional filters or adjusting the window lengths to reduce the frequency of trades. Also, check if there's any seasonality or volatility in the market that might affect your signal’s performance.

For the self-correlation issue, try adjusting your model to include a lag component in your signal to reduce overfitting. Lastly, don't forget to review transaction costs and slippage that could contribute to your turnover. Keep refining your approach and testing different variations—you'll get there!"

---

### 评论 #10 (作者: TN48752, 时间: 1年前)

- Your formula for Fitness suggests that turnover plays a significant role in determining the overall performance. If turnover is too high, it could negatively affect your fitness. As you mentioned, reducing turnover could potentially help you improve this metric.
- The first suggestion you made using  `trade_when(rank(ts_mean(returns, 20)) > 0.5, -signal * sign(returns), -1)`  looks like a solid attempt to reduce trading frequency. By adjusting when you trade based on the rank of the moving average of returns, you're essentially filtering out trades that might be too volatile or too frequent. This should help in reducing turnover while still allowing for significant market signals.

---

### 评论 #11 (作者: PN39025, 时间: 1年前)

There are many operators to reduce tunover you can use ts_sum,ts_mean,hump it is very good and retains moderate performance but you have to accept lower sharpe

---

### 评论 #12 (作者: TP14664, 时间: 1年前)

- On the flip side, firms with  **low turnover ratios**  align more with  **value characteristics** . These companies may not be as heavily traded or speculated upon, but they are likely to be undervalued relative to their intrinsic worth.
- The study shows that these firms  **earn higher future returns** . This supports the idea that value stocks—those that are less actively traded and might be overlooked by the market—offer better returns over the long term.

---

### 评论 #13 (作者: NT63388, 时间: 1年前)

To increase Sharpe/Fitness and decrease Turnover, you can increase Setting > Decay.

There are also many operators that help achieve the same result, for example, a particularly good one is: ts_mean(alpha, 60) (where alpha is your Alpha, and 60 is the time period you want to MEAN - this can be replaced with other values like 5, 20, 90, 180, 240, ...).

---

### 评论 #14 (作者: AB15407, 时间: 1年前)

Besides the trade_when operator, you can use if_else.
Here's a suggested alpha: if_else(ts_mean(close, {day1})/ts_mean(close, {day2}) > 1, -returns, -1)
You can replace {day1} and {day2} with different pairs of days, for example: 10-200, 10-20, 10-40, 20-40, ...

---

