# Getting Started with Price Volume Data: Tips for Beginners

- **链接**: [Commented] Getting Started with Price Volume Data Tips for Beginners.md
- **作者**: TN74933
- **发布时间/热度**: 1年前, 得票: 9

## 帖子正文

Hi everyone,

After spending time researching and engaging with the community, I’ve learned a lot about building good signals using price-volume data. For beginners who aren’t sure where to start, here’s a straightforward approach that worked for me:

### Start with Simple Ideas in Price Reversion:

- `ts_delta(close, 1)`
- `ts_delta(close, 3)`

These are great starting points for understanding how price changes over time.

### Move on to More Complex Ideas:

As you get comfortable, you can experiment with ideas like:

- `(-1 * rank(Ts_Rank(close, 5)) * rank(close / open))`

This builds on the basics and opens the door to more robust signals for your models.

Hope these examples help you on your journey. Don’t hesitate to share your thoughts or any variations you come up with!

Good luck! 🚀

---

## 讨论与评论 (19)

### 评论 #1 (作者: LI36776, 时间: 1年前)

You give the example of  `(-1 * rank(Ts_Rank(close, 5)) * rank(close / open))`

What does this alpha mean?

---

### 评论 #2 (作者: PP87148, 时间: 1年前)

[TN74933](/hc/en-us/profiles/21997837037719-TN74933) ,

Great example to start with alpha research for the beginners. Keep helping the community to grow with you.

---

### 评论 #3 (作者: VP21767, 时间: 1年前)

Thank you for putting together and sharing such an insightful piece of content! Your effort to provide clarity and value to readers like me is greatly appreciated. This has helped me gain a new perspective and has inspired me to explore further. It’s always a pleasure to learn from someone so knowledgeable and passionate. I’m looking forward to seeing more of your thoughtful work in the future!

---

### 评论 #4 (作者: TW77745, 时间: 1年前)

Starting with price-volume data can be a rewarding journey! Begin with simple metrics like  `ts_delta(close, 1)`  or  `ts_delta(close, 3)`  to understand price changes. Gradually, explore more complex signals like  `(-1 * rank(ts_rank(close, 5)) * rank(close / open))` , which combines ranking and momentum for deeper insights. Experiment and refine these ideas to create robust signals. Good luck!

---

### 评论 #5 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #6 (作者: LY88401, 时间: 1年前)

Thank you for sharing your outstanding work with us! Your writing beautifully highlights your talent while providing meaningful insights and inspiration. I deeply value the time and effort you’ve invested in crafting something so impactful and thoughtful. Your storytelling skills are truly exceptional and have left a lasting impression on me. Please continue sharing your amazing creations—I can’t wait to see what you produce next! Thank you again for your generosity and commitment.

---

### 评论 #7 (作者: PN39025, 时间: 1年前)

Hi ,

Analyst estimates provide the expected earnings per share (EPS) as predicted by market analysts, serving as a benchmark for market expectations. Actual earnings, on the other hand, represent the EPS that a company reports in its financial statements. The difference between these two figures is referred to as  **earnings surprises** , which can significantly impact stock prices depending on whether the actual earnings exceed or fall short of expectations. Additionally,  **earnings timings**  indicate the scheduled dates for companies to release their earnings reports, a critical factor for investors tracking financial performance. Complementing this are  **corporate events** , which include key updates such as earnings calls, guidance revisions, and other significant company announcements that provide deeper insights into a company’s outlook and strategies. Together, these elements play a crucial role in shaping market sentiment and investment decisions.

---

### 评论 #8 (作者: CT68712, 时间: 1年前)

Thanks for sharing your insights on using price-volume data! As someone who's just starting my journey in quantitative trading, I find your approach of beginning with simple metrics like ts_delta incredibly helpful. It's a great way to grasp how prices move over time. I'm particularly intrigued by the more complex signal you mentioned, (-1 * rank(ts_rank(close, 5)) * rank(close / open)), as it seems to incorporate both momentum and ranking, which could really enhance my trading strategies. I appreciate you encouraging everyone to experiment; it motivates me to dive deeper into this fascinating field. Looking forward to learning more from the community! Keep it up!

---

### 评论 #9 (作者: TN48752, 时间: 1年前)

**Factor Neutralization** : Use statistical techniques like regression or principal component analysis (PCA) to remove the influence of market factors (e.g., market beta, industry factors, or macroeconomic variables) from your alpha signals.

---

### 评论 #10 (作者: PL15523, 时间: 1年前)

It sounds like you've made great progress in exploring price-volume data and have found a solid approach to building signals. Your strategy seems to incorporate some essential elements of technical analysis, which is a great starting point for anyone looking to dive deeper.

---

### 评论 #11 (作者: TD17989, 时间: 1年前)

It’s great that you’re sharing your insights and experiences with building signals using price-volume data! These are foundational steps that can really help newcomers grasp the concept of analyzing price movements.

---

### 评论 #12 (作者: AC63290, 时间: 1年前)

Your progression from basic to more advanced ideas really shows how you can gradually improve your models. It also provides a good base for those looking to adapt their strategies as they grow more comfortable with these concepts.

---

### 评论 #13 (作者: TP14664, 时间: 1年前)

`ts_delta(close, 1)`  and  `ts_delta(close, 3)`  — These are fantastic starting points for understanding short-term price changes. They track the price change over a specific period, helping to spot trends or reversals.

---

### 评论 #14 (作者: DP11917, 时间: 1年前)

- **Matrix Data Selection** : Use appropriate libraries (like Pandas or NumPy) to load and select the matrix data.
- **Specific Line Execution** : Run the code to select the matrix data right after loading the dataset, and ensure you're correctly indexing the matrix columns or keys in the case of JSON.

---

### 评论 #15 (作者: AC63290, 时间: 1年前)

**Starting with simple ideas**  like  `ts_delta(close, 1)`  and  `ts_delta(close, 3)`  is excellent because it helps you focus on how price moves over time, and it's easy to understand for beginners. The simplicity allows you to get familiar with the dynamics of price changes, which is fundamental when building more complex models later.

---

### 评论 #16 (作者: TT55495, 时间: 1年前)

Analyst estimates predict a company’s expected earnings per share (EPS), while actual earnings are the reported EPS. The difference between these figures, known as earnings surprises, can affect stock prices. Earnings timings and corporate events, such as earnings calls and guidance updates, provide additional insights that influence market sentiment and investment decisions.

---

### 评论 #17 (作者: PT27687, 时间: 1年前)

This post offers valuable insights for beginners looking to harness price-volume data effectively. The step-by-step approach you shared makes complex concepts more digestible. I'm curious, have you found any specific indicators that complement these starting points? Exploring those might enhance the strategies even further!

---

### 评论 #18 (作者: TN41146, 时间: 1年前)

awesome, It’s wonderful that you're sharing your insights and experiences on building signals using price-volume data! These foundational steps are incredibly helpful for newcomers in understanding how to analyze price movements.

---

### 评论 #19 (作者: LN82138, 时间: 1年前)

with price volume, I think you can try vwap (Volume-weighted average price) this is useful data field explain the average price based on the size of trades, for example vwap/close

---

