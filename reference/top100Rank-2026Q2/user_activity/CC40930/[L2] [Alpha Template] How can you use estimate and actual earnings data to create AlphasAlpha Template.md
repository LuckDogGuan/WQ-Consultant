# [Alpha Template] How can you use estimate and actual earnings data to create AlphasAlpha Template

- **链接**: [L2] [Alpha Template] How can you use estimate and actual earnings data to create AlphasAlpha Template.md
- **作者**: YW42946
- **发布时间/热度**: 1年前, 得票: 33

## 帖子正文

Hello everyone, 👋

Today, I'd like to share a template idea that arises from comparing analyst estimates with actual earnings data. This idea builds on the observation that when actual fundamental data releases differ from what analysts seeks to predict, the market may overreact. Expressed in BRAIN Expression, it looks like this:

> group_zscore(subtract(group_zscore(<act_data>, industry), group_zscore(<est_data>, industry)), industry)

This template calculates the difference in group-normalized actual data versus estimated data. You can explore pairs of actual<>estimate data in datasets like  [analyst7](https://platform.worldquantbrain.com/data/data-sets/analyst7?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000) .

Here's a brief breakdown:

- Normalization: The template normalizes both actual financial data and analyst estimates within industries, enabling fair comparisons across companies.
- Discrepancy Identification: It highlights the difference between normalized estimates and actual data to pinpoint where market expectations deviate from reality, suggesting potential overreactions.
- Industry Comparison: A final round of normalization across the industry evaluates these discrepancies to industry standards, identifying companies significantly impacted by earnings surprises.

This template is already quite effective for exploring analyst-related datasets. Share your thoughts on how this template could be further expanded and discuss any interesting findings you have along the way below!

---

## 讨论与评论 (13)

### 评论 #1 (作者: MG97617, 时间: 1年前)

Do you mind sharing the settings you recommend?

---

### 评论 #2 (作者: YL70953, 时间: 1年前)

I tried running the alpha template using analyst7, however all of the simulated alphas has very low short counts and long counts and there is no more positions starting from 2018. May I know is there any reasons for this?

---

### 评论 #3 (作者: DN45758, 时间: 1年前)

[YW42946](/hc/en-us/profiles/12485882527255-YW42946)

This is a well-thought-out template idea that captures the market dynamics between analyst expectations and actual earnings. By normalizing both the actual and estimated data within industries, it helps highlight discrepancies that can signal overreactions. The final normalization ensures a broader market context, making the template versatile for identifying potential mispricing due to earnings surprises. It’s a great starting point for uncovering actionable insights, particularly in volatile market conditions. Thanks for sharing this!

---

### 评论 #4 (作者: deleted user, 时间: 1年前)

Hi, I want to ask if the subtract operator and the - operator are the same in nature but are considered as 2 different operators in tie break?

---

### 评论 #5 (作者: XD81759, 时间: 1年前)

Hey YW42946, that's a really cool template! To further expand it, maybe we could incorporate additional fundamental factors alongside the earnings data, like revenue growth or profit margins. This might give a more comprehensive view of the company's situation. Also, we could test it across different time periods to see if the overreaction patterns vary. And it'd be interesting to combine it with technical factors in a multi-factor model to enhance its predictive power. Looking forward to others' findings too.

---

### 评论 #6 (作者: ZH78994, 时间: 1年前)

I would like to express my heartfelt gratitude for your generous sharing. Your willingness to offer your time, knowledge, and resources means a great deal to me. The insights you've provided have not only broadened my understanding but also inspired me to take positive steps forward. It's rare to encounter someone so selfless and giving, and I truly appreciate the impact you've had. Thank you for your kindness and for being such a valuable source of support. Your gesture will be remembered, and I am grateful for the opportunity to learn from you.

---

### 评论 #7 (作者: XL31477, 时间: 1年前)

**Hey  [YW42946](/hc/en-us/profiles/12485882527255-YW42946)  , your template is really awesome! To further expand it, we could consider adding weights to different industries based on their market importance or volatility. This might make the normalization more refined. Also, exploring different normalization methods other than just group_zscore could bring new perspectives. And for interesting findings, I noticed in some sectors, the discrepancies are more pronounced during earnings seasons. Maybe that's a direction worth digging deeper into.**

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

This is a fantastic template for identifying market overreactions to earnings surprises! The industry-level normalization adds depth, ensuring comparisons are meaningful. Have you explored integrating time-series operators to capture the persistence of these discrepancies over time?

---

### 评论 #9 (作者: KS69567, 时间: 1年前)

Your template is fantastic! An excellent template for spotting market overreactions to earnings shocks is this one! By adding depth, the industry-level normalisation guarantees that comparisons are significant.To broaden it even more, we may think about giving other industries weights according to their volatility or market significance. This might refine the normalisation process.

---

### 评论 #10 (作者: VS18359, 时间: 1年前)

This template enhances the analysis of market sentiment by normalizing both actual earnings and analyst estimates across industries. By doing so, it smooths out industry-specific factors and enables a more accurate comparison of performance versus expectations. The result is a clearer view of potential overreactions or mispricings in the market, allowing investors to identify opportunities where stock prices may not align with underlying fundamentals. This can help distinguish between short-term noise and long-term value discrepancies, improving decision-making in earnings-related market movements.

---

### 评论 #11 (作者: ND68030, 时间: 1年前)

Thanks for sharing! To optimize the Alpha, consider analyzing the impact of earnings surprises on stock prices over time, examining lag effects and price momentum. Additionally, integrating factors like valuation, market sentiment, or sector-based analysis can help refine signals and enhance strategy performance.

---

### 评论 #12 (作者: PT27687, 时间: 1年前)

This template concept certainly offers an intriguing approach to understanding market reactions. I particularly appreciate how it incorporates normalization, which can provide a clearer picture of discrepancies across different sectors. Have you considered potential limitations or other variables that could influence these earnings surprises? Exploring those could deepen our understanding of market behavior even further!

---

### 评论 #13 (作者: LR13671, 时间: 9个月前)

This is an excellent Alpha Template that smartly captures the relationship between analyst estimates and actual earnings data to identify potential market overreactions. The core insight of normalizing both actual and estimated data within industries is key to making fair, apples-to-apples comparisons, especially across companies with very different scales or business models. By using the group_zscore operator twice – first to normalize actual and estimated data, and then to measure the discrepancy – the template removes industry-specific biases and highlights meaningful differences that can drive alpha signals.

---

