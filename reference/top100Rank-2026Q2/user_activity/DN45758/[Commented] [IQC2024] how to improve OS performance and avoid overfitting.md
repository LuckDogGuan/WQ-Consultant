# [IQC2024] how to improve OS performance and avoid overfitting

- **链接**: [Commented] [IQC2024] how to improve OS performance and avoid overfitting.md
- **作者**: ML65849
- **发布时间/热度**: 2年前, 得票: 9

## 帖子正文

Hello, I'm Minki Lee, a researcher from the BRAIN team at WorldQuant Korea.

IQC's Stage 2.1 is nearing its end. Just like in Stage 1, the OS score plays a significant role in Stage 2 as well. Therefore, I recommend that you take some time to review your alpha pool and work on improving your OS score.

**What is the OS score?**

On the BRAIN platform, we have been providing simulations with a total of five years of data from early 2017 to early 2022 to users at the User level. Therefore, most users will strive to find alphas that generate profits during this In-Sample period. However, while trying to improve performance during this period, it is possible to unintentionally create overfitting that makes it appear as if the alpha is performing well, by taking long positions in companies that performed well in the stock market during this period, and short positions in companies that declined.

However, what is more important than the performance during this period is whether the alpha can generate signals in the future. Therefore, it is necessary to evaluate the performance from early 2022 to the present (Out-Sample period) and determine if the performance during this period is also good. In particular, in IQC2024, a higher weight is given to the OS score than the IS (In-Sample) score, and teams that submit alphas that are not overfit or underfit are evaluated more favorably.

**Methods to improve the OS score**

However, it is not easy to determine which alpha is overfitting since we cannot accurately predict the future. We only have a period of about five years, and we can only observe that period, so overfitting occurs more frequently than we think.

Just like evaluating the performance of alphas with Sharpe ratio, the performance of OS can also be evaluated with Sharpe ratio. However, it is known that the OS Sharpe ratio of alphas submitted by consultants generally falls short of the IS Sharpe ratio. The figure below shows the result of combining 30 randomly selected alphas from the In-Sample period until mid-2020 into a super alpha with equal weight. (You can also create such a super alpha once you switch to a consultant.) You can see that the performance of the combined alpha deteriorates as soon as the Out-Sample period begins. Despite the fact that these alphas were created by consultants with more experience than common users and were subjected to more strict criteria, the fact that such results occur implies that it is easy to fall into the trap of overfitting in alpha research more than you thought.

![图片](images/img_8fba1f091c.png)

However, it is not easy to determine whether your alpha is overfitting or not. An alpha can either accurately reflect signals or not. Therefore, we can consider and express the future performance of alphas as follows:

![图片](images/img_fa4b9f76e9.png)

If an alpha effectively captures signals, it can show good performance in the OS. Even if the signals temporarily show poor performance, they can recover their profitability in the long term. However, if an alpha is overfit and lacks signals, it will randomly fluctuate around a return of 0 in the OS. Considering these factors together, for an alpha that is potentially overfit and uncertain, we can expect its future performance to be lower on average than the IS but still higher than 0.

In such a situation, what can be done to improve the OS performance of a merged alpha? One good approach is to include alphas in your alpha pool that reflect various risks, aiming to make the overall performance as close to the average as possible. As the alphas encompass diverse risks with low correlation, the standard deviation will decrease, resulting in OS returns closer to the average (positive) and a lower standard deviation, leading to a higher OS Sharpe ratio.

In addition, good alphas that are not overfit are known to have the following characteristics:

- They have simple and concise ideas with underlying economic insights.
- They are not sensitive to small changes in data or parameters.
- They work well across multiple universes.
- They work well across different regions.

**Practices that can have a negative impact on OS performance**

Using a single formula repeatedly across multiple alphas can have a detrimental effect on OS performance. Let's consider an example. The following alpha was created for the In-Sample period from 2016 to 2021. It was a fairly strong alpha with a Sharpe ratio of 2.07 and a fitness of 1.70.

![图片](images/img_7e385b1932.png)

The performance of this alpha during the out-of-sample period would have been poor. Although this is an extreme example, this alpha exhibited very poor OS performance with a Sharpe ratio of -3.22 and a fitness of -5.77 during the OS period.

![图片](images/img_7d27722127.png)

Although the OS performance is not good, discovering this signal and observing its strong performance during the IS period can incentivize participants in the IQC competition to create alphas by simply mixing this signal with other signals. Here is an example of another alpha created by mixing this signal with other signals:

![图片](images/img_bc8e17b4a2.png)

This alpha visually appears to be exposed to a similar level of risk as some of the leading alphas. However, the correlation between these two alphas is 0.59, which is below the threshold of 0.7. Therefore, it can be submitted separately. Additionally, considering that the IS performance of this alpha is not bad, users may want to submit it.

However, when two similar alphas are submitted together, the negative signal in this alpha will have a higher weight in the merged alpha, resulting in a more detrimental impact on the OS performance.

Of course, this alpha highlights the negative effects of signal mixing because its OS performance is particularly poor. However, even if an alpha has good OS performance, if it has a high correlation with other alphas in the alpha pool, it can increase the standard deviation of the merged alpha and consequently have a negative impact on the OS performance.

In this post, we explored more practical ways to improve the OS score in IQC. If you have any questions or would like to know more, please leave a comment, and I will be happy to respond.

---

## 讨论与评论 (11)

### 评论 #1 (作者: AT56452, 时间: 1年前)

Great post! Can you please mention some practical tips in which we can determine if an alpha will generate good OS performance while making an alpha? Thanks!

---

### 评论 #2 (作者: TN48752, 时间: 1年前)

Hello, here are some ways you can ensure alpha's os:
Here are some suggestions that can improve the OS performance of your alphas:

Focus on simple, but robustly-implemented ideas. Simplify the implementation of an alpha idea and remove unnecessary elements: i.e., parts that do not make sense or do not drive performance.
Take care of missing or abnormal data.
Do not combine multiple uncorrelated alphas in a single alpha. This could lead to an exaggeration of common risks across the combined alphas and cancel out the unique nature of individual alphas. ValueFactor evaluation combines your single-idea alphas in an optimal way, observing pairwise uniqueness and recent performance of each individual alpha, but can only do so if alphas are not pre-mixed.
Out of 10 years in-sample years visible on platform, you can voluntarily set aside 2 years as an evaluation period for yourself. Then, select alphas on the remaining 8 year in-sample training period, and explore practices through which you are able to preserve performance on the 2-year period
Verify that performance of your alpha is (to some extent) preserved even when you change operators, fields, constants, region, universe and simulation settings.
Do not hesitate to increase turnover to 30% or more when needed to exhaustively manifest Sharpe of an alpha idea.

---

### 评论 #3 (作者: DK20528, 时间: 1年前)

Thank you for the detailed explanation, Minki! It's great to have such a thorough understanding of how the OS (Out-Sample) score plays a critical role in the IQC competition.

From your explanation, the key takeaway seems to be the importance of avoiding overfitting by focusing on alphas that exhibit true signals rather than just fitting the data of the in-sample period. The strategies you've outlined for improving the OS score are insightful, especially the suggestion of diversifying the alpha pool to reduce risk and avoid overfitting.

Here are a few points and suggestions I would like to ask or discuss further:

### 1.  **Alpha Diversification** :

- You mentioned that combining alphas with low correlation is beneficial. Could you share more on how to measure the correlation between different alphas effectively? For example, is there a particular method or tool on the BRAIN platform for analyzing the correlation between alphas across different universes and regions?

### 2.  **Simple Ideas with Economic Insights** :

- Could you elaborate on examples of "simple and concise ideas" that have worked well in the past and why they are less likely to overfit? Sometimes, alphas with complex strategies perform better in the short term but may struggle out-of-sample due to their sensitivity to data noise. What do you think are the best practices for balancing complexity and robustness in alpha development?

### 3.  **Testing Across Universes and Regions** :

- I understand that alphas should perform well across multiple universes and regions. Do you have any recommendations for how to test alphas across different regions effectively, and what are the challenges in ensuring that an alpha is not region-specific or data-sensitive?

### 4.  **Impact of Overfitting on the Merged Alpha** :

- You provided an example of how mixing alphas can impact OS performance when one of them has poor OS performance. If we have an alpha that works well in IS but poorly in OS, is there a way to "weight" these alphas more cautiously when combining them? Perhaps using a weighted average based on their IS performance or using different weighting schemes based on robustness?

### 5.  **Handling Negative Signals** :

- You noted that negative signals can have a detrimental effect when mixed with other alphas, especially if their correlation is high. How do you suggest handling these negative signals when they arise—should they be discarded, or is there a strategy for integrating them into the pool in a more controlled way?

These points would help further refine strategies for improving OS performance while keeping the overall alpha pool diverse and robust. Thanks again for sharing such useful insights!

---

### 评论 #4 (作者: AM60509, 时间: 1年前)

Use simple ideas using only single data set to avoid overfitting and improve OS Performance. Avoid fine tuning parameters like lookback period,powers etc.

---

### 评论 #5 (作者: DN45758, 时间: 1年前)

[ML65849](/hc/en-us/profiles/16237811130135-ML65849)

Focus on simple, robust ideas, removing unnecessary elements. Handle missing or abnormal data properly. Avoid combining uncorrelated alphas, as it can cancel out unique signals. Use 8 years for training and 2 for evaluation. Test alpha performance across different settings. Increase turnover above 30% if needed to improve Sharpe.

---

### 评论 #6 (作者: LK29993, 时间: 1年前)

Hi DK20528!

1) To check internal correlation among your own alphas:  [Can I check correlation among my own Alphas? – WorldQuant BRAIN](/hc/en-us/articles/5973552723735-Can-I-check-correlation-among-my-own-Alphas)

2) Simple and concise ideas refer to Alphas that use smaller number of data fields and operators. Best practices to avoid overfitting include: avoid hyper-optimizing your parameters and having a validation process such as using the Test Period feature on BRAIN:  [Test Period | WorldQuant BRAIN](https://platform.worldquantbrain.com/learn/documentation/create-alphas/test-period)

3) To test alpha across universes and regions, simulate the alpha using during universe and region setting and check whether the alpha still has positive sharpe.

4) For your current merged performance in the Performance Comparison section on the BRAIN simulation results page, it is fixed as equal weighted for each alpha. You can explore this concept of weighting Alphas differently when you work with SuperAlphas in future though.

5) The negative signals in Minki's article only arise in the OS. You will not be able to detect these negative OS performances during your research. The best way to avoid having many of these negative signals is to avoid submitting similar Alpha ideas.

---

### 评论 #7 (作者: CC40930, 时间: 1年前)

Thank you for your insightful post about improving the OS score in IQC. I appreciate the clarity in explaining how overfitting can impact alpha performance out-of-sample and the importance of diversifying alphas to improve their future performance.

---

### 评论 #8 (作者: TP14664, 时间: 1年前)

In the context of the BRAIN platform and IQC2024, it is crucial to consider the  **Out-Sample (OS) performance**  of alphas, as this is weighted more heavily than the  **In-Sample (IS) performance** . While alphas may perform well during the IS period, it is possible that they are overfitted, meaning that their performance is tailored too closely to the historical data and may not generalize well to future data. Thus, evaluating alphas on their ability to generate future signals and performance is essential.

---

### 评论 #9 (作者: AC63290, 时间: 1年前)

The  **OS score**  (Out-Sample score) is a metric used to evaluate the performance of an alpha (a trading strategy or signal) based on its ability to generate profitable signals in  **future periods** , specifically in data outside the original training or "In-Sample" period. This score is important because it assesses the  **real-world performance**  of the alpha when applied to  **unseen**  data, rather than simply its ability to perform well on the historical data it was trained on.

---

### 评论 #10 (作者: ND68030, 时间: 1年前)

The challenge of  **avoiding overfitting**  and improving  **Out-of-Sample (OS) performance**  is crucial in quantitative trading and competitions like IQC. From your explanation, it’s clear that while a model or alpha might perform well in the  **In-Sample (IS) period** , there's always the risk that it could be overfitting, meaning it is too tailored to the past data and may not generalize well to future data.

---

### 评论 #11 (作者: deleted user, 时间: 1年前)

To begin using the BRAIN API in your alpha research, download our  **ACE library**  and  **Demo notebook** . You can also check out our  **ACE Library documentation**  and  **API documentation**  for more details.

---

