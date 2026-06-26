# Securing Vietnam's sole championship in 2024 - The journey of crafting my fundamental alpha

- **链接**: [Commented] Securing Vietnams sole championship in 2024 - The journey of crafting my fundamental alpha.md
- **作者**: NM98411
- **发布时间/热度**: 1年前, 得票: 60

## 帖子正文

Creating an alpha is a long and persistent process, requiring consultants to have basic programming skills and a certain level of financial knowledge. Here, I will share how to build an alpha from scratch based on the experience I used to compete for the championship.

1. How to find data for alpha development
There are two basic ways to start finding and utilizing data from scratch. The first method is to leverage your existing financial knowledge, identify financial models, and use the pre-available data fields provided by WorldQuant to create your alpha. The second method involves optimizing data usage by analyzing the frequency of data used in other alphas, allowing you to identify common and suitable variables for your own work.

![图片](images/img_52f58b0b7b.png)

As shown in the image above, I accessed the link:
 [https://platform.worldquantbrain.com/data/data-fields?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000](https://platform.worldquantbrain.com/data/data-fields?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000) 
I then ranked the data fields based on the frequency of their usage in alphas. This approach makes it easier to identify which data fields are most commonly used, allowing you to select data that aligns well with your idea.

2. How to use functions to build alpha
Consider mathematical and analytical functions that are appropriate for the data you are using. Focus on data processing functions such as zscore, rank, scale, ts_mean, or transformation functions like ts_delta or ts_decay_exp_window. These functions help transform raw data into potential alpha signals.

If your alpha fails basic tests like weight failure, sub-universe Sharpe, or self-correlation, consider nesting functions repeatedly rather than combining the alpha with additional data fields. This approach can help prevent issues like NaN errors causing weight failure or excessive correlation.

3. Setting
You should prioritize using a universe that fits your purpose. For instance, using the top 3000 most liquid stocks will take longer to run compared to the top 200, so using the top 200 can optimize alpha computation time. However, the top 3000 offers a larger pool of stocks, allowing your code to better reflect its economic meaning.

Neutralization is another crucial setting for alpha creation. If you neutralize to the market, the alpha will be neutralized against the entire market, isolating it from broader market trends. Conversely, using subindustry neutralization will neutralize the smallest industry groups, focusing the alpha on the smallest differences between stocks.

4. Choosing an alpha to submit
Choosing which alpha to submit is critical when you have multiple viable alphas. The current trend to rank highly in the consultant leaderboard is to optimize for using as little data and as few operators as possible for each individual alpha, while ensuring the total amount of data and operators across all alphas is large enough to achieve a high score.

This balance is almost impossible to achieve without compromising alpha performance. This means you must trade off between data field scores and alpha performance. For example, in the competition, I used very few data fields and operators, which resulted in my alpha performance ranking only at the top 7. However, my data field score was exceptionally high, allowing me to secure the world championship.

Depending on your goal, if you aim for high alpha performance and quality, you should use more data and operators. Conversely, if your priority is optimizing data usage, you may need to sacrifice some performance.

Thank you for reading my article! If you enjoyed it and want to learn more, I’ll write another article about building algorithms focused on the USA, which helped me achieve a 1.0 value factor.

---

## 讨论与评论 (12)

### 评论 #1 (作者: LI36776, 时间: 1年前)

woah, 1.0 value factor is seriously impressive

---

### 评论 #2 (作者: KS24487, 时间: 1年前)

As someone who is pretty new here, the idea of optimizing for lower operator and data field counts is especially appealing. I've had a lot of success in the last few weeks just focusing on individual fields with a high existing alpha count as you mentioned. Still, I've found I often needed to combine several of these fields to get lots of alphas for submission. I've been watching the stats for the top performers and I'm blown away with seeing so many alphas being submitted with even just 1-2 operators and fields on average. I can find a few like that, but would love some additional insight on how folks are able to achieve this in bulk. You also mention using a smaller universe, and focusing on USA, and I've had a tough time finding lots of alphas for something like USA/TOPSP500, especially with low operators/fields. Really look forward to additional insights you might have there. 🙏

---

### 评论 #3 (作者: ND68030, 时间: 1年前)

Hi, I would like to ask if this strategy will help your value factor stay at 1? Or just in the month after you take the MAPC. Thanks a lot.

---

### 评论 #4 (作者: DN41247, 时间: 1年前)

Thank you  [NM98411](/hc/en-us/profiles/5646822985623-NM98411)  for sharing your detailed and practical experience in alpha creation! Your step-by-step breakdown, from data selection to optimization and submission strategies, is incredibly insightful and useful for anyone working in quantitative finance.

I particularly appreciate the focus on leveraging existing financial knowledge and optimizing data field usage by analyzing their frequency. Your explanation of function usage, such as zscore and ts_mean, provides great guidance for transforming raw data into meaningful signals.

The discussion on universe settings and neutralization adds depth, emphasizing the trade-offs between computation efficiency and the economic meaning of alphas. Your strategy for balancing data field scores with alpha performance is inspiring, especially how you turned it into a competitive advantage to win the championship.

Looking forward to reading more of your articles, especially about building algorithms with a focus on the USA. Thank you for generously sharing your expertise!

---

### 评论 #5 (作者: TD84322, 时间: 1年前)

Thank you, NM98411, for sharing your practical experience in alpha creation! Your step-by-step guide, from data selection to optimization and submission, is incredibly helpful for anyone in quantitative finance.

I especially value your tips on using financial knowledge, analyzing data field frequency, and applying functions like zscore and ts_mean to create meaningful signals.

Your insights on universe settings and neutralization highlight important trade-offs between efficiency and alpha quality. The way you balanced data field scores with alpha performance to win the championship is truly inspiring.

I’m excited to read more of your articles, especially on building algorithms focused on the USA. Thank you for sharing your expertise!

---

### 评论 #6 (作者: TL60820, 时间: 1年前)

In the process of creating an alpha, how do you balance the trade-off between optimizing data usage and maximizing alpha performance, particularly in competitive environments where both data field score and alpha performance are critical for ranking? When aiming to minimize the number of data fields and operators, how do you ensure that the resulting alpha signal remains both robust and high-quality? What specific techniques or strategies do you employ to maintain strong alpha performance while optimizing for data efficiency, and how do you assess the impact of these trade-offs on both the overall performance and scalability of your alpha?

---

### 评论 #7 (作者: ZH78994, 时间: 1年前)

Creating an alpha is a multi-faceted process that involves both leveraging financial intuition and data analysis. You can start by:

Using your financial knowledge to identify potential factors and utilize pre-available data.

Optimizing data usage by analyzing how successful alphas leverage different data frequencies and variables.

Iteratively refining your model through backtesting, risk-adjusted metrics, and real-time testing.

By combining existing knowledge with data-driven optimization, you can develop a unique and profitable alpha strategy that is both robust and scalable.

---

### 评论 #8 (作者: SK72105, 时间: 1年前)

[NM98411](/hc/en-us/profiles/5646822985623-NM98411)  Congratulations! I have observed that you have an impressive IS and OS score even with a low amount of alphas in both ATOM, and MAPC. Thank you for sharing your approach - it is indeed methodical and practical. Looking forward to the USA article!

---

### 评论 #9 (作者: TL16324, 时间: 1年前)

@NM98411 Well done! Could you please share your tips for high IS score and value factor?

---

### 评论 #10 (作者: CC40930, 时间: 1年前)

This is a fantastic guide on building alpha strategies from scratch! Your approach of leveraging existing financial knowledge and identifying the most commonly used data fields is an effective way to start the process. It’s interesting how you emphasize using data frequency to select variables that align with your alpha, making it much easier to identify important factors for your strategy.

---

### 评论 #11 (作者: ND68030, 时间: 1年前)

In the article, NM98411 points out that if the alpha fails basic tests such as weight failure, sub-universe Sharpe, or autocorrelation, adjusting functions or reorganizing operations can help resolve these issues. This emphasizes the importance of thoroughly testing the alpha through multiple channels and making flexible adjustments to ensure that it not only performs well but also remains stable and sustainable in the long term.

---

### 评论 #12 (作者: PT27687, 时间: 1年前)

The journey you describe in developing an alpha is fascinating and certainly showcases the blend of skill and strategy involved. Your method of optimizing data usage while balancing performance is insightful and seems important for anyone looking to enhance their success in competitions. What specific challenges did you face while ranking the data fields, and how did you overcome them? This could offer valuable lessons for others in the community.

---

