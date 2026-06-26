# [BRAIN TIPS] Examples of good stop loss conditions

- **链接**: [Commented] [BRAIN TIPS] Examples of good stop loss conditions.md
- **作者**: NL41370
- **发布时间/热度**: 3年前, 得票: 7

## 帖子正文

A method to avoid potential losses is to create good alphas that have low correlation with your existing alphas. When you have two good alphas with a low correlation, one of them should ideally compensate for the other when it is in a loss condition. Overall, both alphas should perform well over time .

Think about loss first before thinking about stop-loss and the techniques to stop losses. Your alphas often require some condition to work — market environment, time of the year — or simply just depend on some assumption. For example, if you have alpha = - return 5 days, that means you are assuming that every week the price will revert. Can you check that assumption?

When your idea depends on parameters, if the parameters change in the live condition what can you offer? Often, it would be better to define your parameter by a range and then adjust dynamically (regression and correlation operation help here). Or you might consider parameter averaging: In the previous example, alpha = -(return 3 + return 5 + return 8 days) might be a better alternative.

From my experience, it is not a good idea to have a stop-loss technique that applies for all alphas as it creates dependency on the stop loss, limits the creativity and reduces the diversity of the pool, particularly during critical conditions. The technique to make alphas better should depend on the initial alpha idea.

---

## 讨论与评论 (8)

### 评论 #1 (作者: Nguyen Dang Huynh(HN14753), 时间: 2年前)

Hi. I would like to ask "event" in close_at_event = trade_when(event, close, -1); What is the meaning of stop loss? Is it true that event = returns < 0.9*ts_delay(returns,1)? Thank you.

---

### 评论 #2 (作者: HT66349, 时间: 2年前)

Hi,

[By definition](https://www.investopedia.com/articles/stocks/09/use-stop-loss.asp#:~:text=A%20stop%2Dloss%20order%20is%20an%20order%20placed%20with%20a,limit%20your%20loss%20to%2010%25.) , stop loss is a method to limit our losses on securities' positions and in the context of Alpha research, it refers to the technique that closes or exits a position if it has accumulated more than a certain amount of loss.

trade_when is, in my opinion, a good starting point for implementing your stop losses. Continue exploring but do bear in mind that Alphas can also assign negative weights. Therefore, the loss of a position does not necessarily equate to a decrease in stock price (or negative stock returns).

---

### 评论 #3 (作者: TT55495, 时间: 1年前)

How can you dynamically adjust parameters in your alpha models if market conditions or parameters change in real-time, and what role do regression and correlation operations play in this process?

---

### 评论 #4 (作者: CC40930, 时间: 1年前)

To avoid potential losses, it's important to build alphas with low correlation to each other, as one can offset losses from the other. Always consider the assumptions behind your alphas—market conditions, timeframes, and parameters—and be prepared to adjust dynamically based on changes. Instead of applying a universal stop-loss, tailor adjustments to the specific alpha idea to preserve creativity and diversity, especially in critical situations. Techniques like dynamic parameter adjustments or averaging can improve robustness without relying on rigid stop-loss mechanisms.

---

### 评论 #5 (作者: deleted user, 时间: 1年前)

Creating alphas that are not highly correlated with each other reduces the risk of simultaneous losses across your strategies. When one alpha performs poorly, another one may still perform well, balancing the overall performance.

---

### 评论 #6 (作者: KJ42842, 时间: 1年前)

[TT55495](/hc/en-us/profiles/13132630342807-TT55495)

It's exactly since the market change dynamically, so that you can use that market dynamics to get parameter changed accordingly rather than fixed. Regression and correlation are example of ways to switch parameter based on the market condition.

---

### 评论 #7 (作者: CT68712, 时间: 1年前)

Great discussion on stop-loss techniques! As a quantitative trader, I completely agree that having alphas with low correlation is crucial for risk management. It's interesting to consider how parameters can change based on real-time market conditions. I often utilize regression and correlation analysis to dynamically adjust my models, ensuring they remain robust amid volatility. The traditional one-size-fits-all stop-loss isn’t always the best approach. Tailoring each alpha’s stop-loss condition makes a lot of sense, preserving both creativity and diversity in our strategies. Keep pushing the boundaries; it's all about finding that balance in our complex world of trading!

---

### 评论 #8 (作者: RB76778, 时间: 1年前)

Narure is good

---

