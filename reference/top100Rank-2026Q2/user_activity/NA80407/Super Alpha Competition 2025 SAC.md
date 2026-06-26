# Super Alpha Competition 2025 (SAC)

- **链接**: Super Alpha Competition 2025 SAC.md
- **作者**: NA80407
- **发布时间/热度**: 1年前, 得票: 16

## 帖子正文

WorldQuant is currently organizing the Super Alpha Competition 2025. As this is my first time participating in SAC, I don’t have much experience and I’m not fully clear on how Super Alpha scores are calculated.I would greatly appreciate it if experienced consultants who have previously taken part in SAC could share their knowledge and insights. Practical advice and shared experiences would be extremely helpful for me—and other newcomers—to better understand the competition and prepare effectively.

---

## 讨论与评论 (24)

### 评论 #1 (作者: IK32530, 时间: 1年前)

This is my first experience participating in a super alpha competition, but based on tips from other consultants, trying to lower self_correlation and prod_correlation is considered useful advice for improving competition results. Using the operator combo_a appears to deliver good results with respect to correlation. Although equal_weight leads to favorable outcomes on the PNL chart, today’s performance comparison showed that it performs significantly worse in terms of scoring compared to using combo_a.

---

### 评论 #2 (作者: JM52201, 时间: 1年前)

Hi @NA80407,Key factors that influence the score include:Sharpe Ratio– The higher, the better. It reflects the risk-adjusted return of your alpha.Turnover– Lower turnover is generally preferred unless your alpha is highly profitable.Correlation to existing alphas– Novelty matters. Alphas too similar to existing ones may be penalized.IC (Information Coefficient)– This shows how well your alpha predicts future returns.

---

### 评论 #3 (作者: KK61864, 时间: 1年前)

SuperAlphas that meet all the following criteria are eligible for the competition:-are in USA/ASI/EUR/ GLB region, Delay 1use component Alphas from only one category assigned to the participant in the respective week.The metrics that impact the SAC 2025 Score are:-Sharpeof the merged performance series: The larger the Sharpe is, the better the score would be with all other parameters being the same.Returns to drawdown ratioof the merged performance series: The larger this ratio is, the better the score would be with all other parameters being the same.Turnoverof the merged performance series: The larger this parameter is, the worse the score would be with all other parameters being the same.25%of the SAC 2025 Score is based on the performance during the In-sample period.75%of the SAC 2025 score is based on the performance during Out-sample period.Final_score = 0.25*(scaled_is_score) + 0.75*(scaled_os_score)To improve OS performance:-focus on idea and implementation quality, not just on performance numbers and metrics: a clear idea and robust implementation would generally remain strong during the OS period, while performance numbers may change.

---

### 评论 #4 (作者: RS70387, 时间: 1年前)

NA80407, Great to see your interest in SAC, it’s a fantastic opportunity to learn and compete.In addition to the helpful points already shared byJM52201, I'd recommend checking out theSAC 2025 FAQ. It breaks down the competition structure, scoring mechanics, and best practices in detail.One important point from the FAQ is howyour SAC score is actually calculated. It's based on metrics derived from yourmerged performance series, which is an equal-weighted combination of your submitted SuperAlphas (i.e., as if the same dollar amount were invested in each). This makes the quality of your whole SuperAlpha set and how well they work together extremely important.The metrics that influence your score are:Sharpe Ratioof the merged performance: Higher is better.Return to Drawdown Ratio: Again, higher is better.Turnover: Lower turnover is preferred, unless your returns strongly justify it.Scoring is weighted heavily toward theOut-of-Sample (OS)performance:25% of the final score is based on In-Sample (IS)75% is based on Out-of-Sample (OS)Final Score = 0.25 × (scaled IS score) + 0.75 × (scaled OS score)This means your OS performance matters most. A good takeaway here is that strong scores often come fromwell-thought-out ideas with robust implementations, not just tuning numbers to look good. Signals that are clear, logical, and resilient tend to hold up better in OS.Good luck in SAC 2025 and don’t hesitate to experiment and learn along the way.

---

### 评论 #5 (作者: AM54671, 时间: 1年前)

How can one make a strong super alpha true the designated fields

---

### 评论 #6 (作者: TN48242, 时间: 1年前)

Hi, I recently joined SAC as well, so I totally understand how you feel starting out. One of the unique aspects of SAC is that participants gain access to the global alpha pool, which contains many strong Alphas from other consultants. This is a great opportunity to experiment and learn, as you can try different combination (combo_expression) and selection (selection_expression) strategies to understand how a Super Alpha is evaluated.When building a Super Alpha, make sure to focus on:Combined performance: how well the Alphas work together;Novelty and correlation: avoid overlap and increase diversity among Alphas;Neutralization and universe selection: thoughtful choices here can significantly improve your results.Also, I highly recommend checking out the "Super Alpha" section in the Learn tab on the platform. It explains what a Super Alpha is and how the evaluation process works in detail.Wishing you all the best as you explore and experiment in SAC 2025!

---

### 评论 #7 (作者: AM54671, 时间: 1年前)

Thanks for the ideology

---

### 评论 #8 (作者: TP18957, 时间: 1年前)

Great question about how Super Alpha scores are computed! The scoring framework primarily balances risk-adjusted returns (Sharpe Ratio), turnover, and predictive power (Information Coefficient). Importantly, the competition rewards novelty — alphas that are highly correlated with existing ones may face penalties, encouraging innovation and diversity in signals. Another key factor is universe selection and neutralization techniques, which can greatly affect alpha performance by controlling for sector, market, or other risk exposures. For newcomers, a practical tip is to experiment extensively with combining alphas using combo expressions and adjusting selection expressions to fine-tune contributions. Reviewing historical winning strategies and the platform’s “Super Alpha” tutorial is invaluable for mastering these aspects.

---

### 评论 #9 (作者: AG14039, 时间: 1年前)

Hi! I recently joined SAC as well, so I understand how starting out feels. One of the great things about SAC is access to the global alpha pool, which contains many strong Alphas from other consultants—offering a valuable chance to experiment with different combination (combo_expression) and selection (selection_expression) strategies to learn how a Super Alpha is evaluated. When building a Super Alpha, focus on combined performance to ensure the Alphas work well together, prioritize novelty and low correlation to increase diversity, and make thoughtful choices about neutralization and universe selection to improve results. I also recommend checking out the "Super Alpha" section in the Learn tab on the platform for a detailed explanation of the evaluation process. Best of luck as you explore and experiment in SAC 2025!

---

### 评论 #10 (作者: AK40989, 时间: 1年前)

I’m curious about practical tips on crafting strongselection_expressionandcombo_expressionstrategies that balance performance and novelty. How do you approach combining Alphas to optimize Sharpe ratio while keeping correlations low?

---

### 评论 #11 (作者: RK48711, 时间: 1年前)

Thanks for the tips! I'm exploring the global alpha pool now—do you have any advice on evaluating Alpha combinations or handling novelty and correlation? Also curious how you approach neutralization and universe selection.

---

### 评论 #12 (作者: LW67640, 时间: 1年前)

Welcome to SAC! I joined not too long ago too, so I totally get how overwhelming it can feel at first. Here’s what I’ve picked up about scoring and building Super Alphas:Key things that affect your score:Sharpe Ratio: Higher is better. Basically shows how much bang you get for your risk buck.Turnover: Lower is usually preferred (less trading costs), unless your alpha’s crazy profitable.Correlation to existing alphas: Super important! If your alpha’s too similar to others, it might get penalized. Novelty wins.IC (Information Coefficient): Tells you how well your alpha predicts future returns – accuracy matters.For building good Super Alphas:Play with the global alpha pool: Seriously, this is SAC’s best feature. Test different combo_expression and selection_expression setups using proven alphas from others. Hands-on tweaking is the fastest way to learn what scores well.Focus on team chemistry: Don’t just chase shiny individual alphas. See how they work together in a combo – sometimes meh alphas pair up into something awesome.Hunt for uniqueness: Mix in low-correlation, offbeat alphas. Makes your whole strategy more resilient and less "me-too."Tweak your settings: Don’t sleep on neutralization and universe selection (neutralization & universe selection). Small adjustments here can seriously boost performance.Oh, and definitely check out the "Super Alpha" guide under the Learn tab – it breaks down the whole evaluation process in plain English. Super handy when you’re starting out.Stick with it! The first few weeks are trial-and-error, but you’ll start seeing patterns. Happy tinkering in SAC 2025 – hope you uncover some gems!

---

### 评论 #13 (作者: ZV96737, 时间: 1年前)

Since this competition allows sourcing alphas globally, implementing ahigher Selection Limit (700-1000 range)could deliver significant advantages. Increasing the candidate pool size enhancesdiversity,  improving the chances of discovering uncorrelated and unique signals. Moreover, this expanded selection scope naturally promotes greaterstability, as larger alpha pools inherentlyreduce overfitting risksthat often plague smaller, more limited selections. For context, while a 500-alpha limit might constrain optimization opportunities,expanding to 1000 candidateswould enable testing combinations across more factors, potentially yielding moreconsistent and robust results.

---

### 评论 #14 (作者: SP39437, 时间: 1年前)

Hi there! I recently joined SAC too, so I completely understand the experience of getting started. One of the best parts of SAC is having access to the global alpha pool—it's filled with high-quality Alphas from other consultants, giving you a great opportunity to test different strategies usingcombo_expressionandselection_expression. This allows you to learn how Super Alphas are built and evaluated in practice.When creating a Super Alpha, it’s key to focus on how well your selected Alphas work together (combined performance), ensure there's enough novelty and low correlation to keep the signal diverse, and apply thoughtful neutralization and universe choices to improve robustness. Don’t forget to explore the“Super Alpha”section in theLearntab—it’s packed with helpful information on the evaluation framework and strategy building. What’s been the most surprising thing you’ve learned so far while exploring the global alpha pool in SAC?

---

### 评论 #15 (作者: JK98819, 时间: 1年前)

Try to choose alphas that don’t behave the same way. It helps improve your overall performance.Use combo_expression and selection_expression wisely– These control how you blend and filter your alphas. Small tweaks can make a big difference

---

### 评论 #16 (作者: AK52014, 时间: 1年前)

Welcome to SAC—I recently joined too, so I get the learning curve! Take advantage of the global alpha pool to explore combo and selection strategies. Focus on performance, novelty, and neutralization. The Learn tab’s Super Alpha guide is invaluable!

---

### 评论 #17 (作者: SK90981, 时间: 1年前)

Excited to join SAC 2025! Would love to hear tips from experienced participants to better understand scoring and improve our strategies.

---

### 评论 #18 (作者: AG14039, 时间: 1年前)

Welcome to SAC! I joined recently as well, so I understand the learning curve. Be sure to explore the global alpha pool—it’s a great resource for testing combo and selection strategies. Prioritize performance, novelty, and proper neutralization, and don’t miss the Super Alpha guide in the Learn tab—it’s incredibly helpful!

---

### 评论 #19 (作者: RP41479, 时间: 1年前)

Thanks for the tips! I'm exploring the global alpha pool—any quick advice on combining alphas, managing novelty and correlation, and handling neutralization and universe selection!

---

### 评论 #20 (作者: SP39437, 时间: 1年前)

Welcome to SAC! I joined not too long ago myself, so I completely understand how overwhelming it can feel at first. Here are a few things I’ve learned about how Super Alpha scoring works and how to build better submissions:Scoring BasicsSharpe Ratio: The higher, the better — it reflects return vs. risk.Turnover: Lower turnover helps, unless your alpha performs exceptionally well.Correlation: Keep it low with other alphas — uniqueness really matters.IC (Information Coefficient): Measures predictive power — higher is better.Tips for Building Super AlphasUse theglobal alpha poolto test combo strategies — it’s the best way to learn.Think aboutteam synergy, not just individual alpha performance.Addlow-correlationor unconventional alphas to boost diversification.Don’t overlookneutralization or universe settings— small tweaks make a big difference.Also, check out theSuper Alpha guideunder the Learn tab — it’s a great starter. Stick with it, and good luck in SAC 2025!

---

### 评论 #21 (作者: TP19085, 时间: 1年前)

Hi there! I recently joined SAC as well, so I can definitely relate to the learning curve early on. One of the most exciting features is access to the global alpha pool—it’s a rich resource full of high-performing Alphas contributed by other consultants. It gives you the chance to experiment withcombo_expressionandselection_expression, helping you understand how Super Alphas are constructed and evaluated in real-world scenarios.When building a Super Alpha, it’s important to focus on overall synergy between selected alphas. Aim for strong combined performance, low correlation among signals, and enough novelty to avoid redundancy. Applying proper neutralization and choosing a stable universe can greatly enhance signal robustness. Also, be sure to check out the “Super Alpha” section under the Learn tab—it offers great insight into evaluation methods and strategy design.What’s been the most unexpected insight or pattern you’ve come across while exploring SAC’s global alpha pool?

---

### 评论 #22 (作者: TP19085, 时间: 10个月前)

Hey, welcome to SAC! It’s great to hear you’re diving into the global alpha pool — that’s definitely one of the best ways to get hands-on experience with real alphas and see how combo_expression and selection_expression shape Super Alphas.One insight that surprised me early on was how critical low correlation between alphas is for building a strong Super Alpha. Even a couple of alphas with similar signals can drag down overall performance and Sharpe. So, prioritizing diversity — not just raw returns — really helps stability. Also, applying proper neutralization (country, sector) and sticking to a stable universe often makes a bigger difference than tweaking the combo logic itself.Have you found any particular alpha types or patterns in the pool that consistently add value or boost diversification? It’s always fascinating to hear how others spot hidden gems or unexpected synergies!

---

### 评论 #23 (作者: TP19085, 时间: 10个月前)

That’s a solid welcome package — and you’ve hit on some of the most overlooked points in SAC.A lot of newcomers focus on picking the “top” alphas by Sharpe or IC, but the real magic often comes fromsynergy and low correlation, as you mentioned. Two high-performing but similar alphas can sink a Super Alpha’s risk-adjusted metrics, whereas a mix of moderate performers with orthogonal signals can deliver far better stability.I’ve also noticed thatneutralization(especially country or sector) anduniverse stabilitycan quietly make a huge difference — sometimes more than tinkering endlessly withcombo_expression. And in the global alpha pool, it’s often worth experimenting with “odd” or niche alphas that don’t shine alone but plug important gaps in your correlation matrix.If you’d like, I can share a quick framework I use to screen for those hidden gems before testing combos.

---

### 评论 #24 (作者: TP19085, 时间: 6个月前)

Welcome to SAC—it’s great to have you onboard. The initial learning curve can feel steep, but access to the global alpha pool makes the process both practical and rewarding. Exploring this pool allows you to experiment with combo and selection expressions, offering hands-on insight into how Super Alphas are built and evaluated in realistic settings. When constructing a Super Alpha, the key is focusing on how signals work together rather than on individual strength alone. Strong combined performance, low correlation, and genuine diversity help avoid redundancy and improve robustness. Thoughtful neutralization choices and a stable universe further strengthen results. Reviewing the Super Alpha materials in the Learn section is also highly recommended, as they clarify scoring metrics and design principles. Overall, careful exploration and iteration quickly turn the alpha pool into a powerful learning tool.

---

