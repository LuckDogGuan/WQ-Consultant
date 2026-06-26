# Reducing correlation of alphas

- **链接**: [L2] Reducing correlation of alphas.md
- **作者**: AT56452
- **发布时间/热度**: 1年前, 得票: 15

## 帖子正文

Some tips to reduce correlation for your alphas -

1) Use uncommon operators like vector_neut, vector_proj, regression _neut and regression proj while making your alphas.

2) Use group operators with custom neutralisations using different kinds of data. Eg. Group_coalesce, group_cartesian_product, etc. work extremely well.

3) While building alphas filter datasets based on the number of alphas it has and spend time on understanding the dataset that has the least number of alphas, read some literature on it and then think which operator would work the best with that kind of data. You'll mostly come up with a submittable alpha with less self and prod corr if you follow this.

I'll keep adding more ideas to this thread. Let me know if it helped you!

---

## 讨论与评论 (74)

### 评论 #1 (作者: SK95162, 时间: 1年前)

Thank you for sharing these insights! Could you provide specific examples of how you’ve applied operators like  `vector_neut` ,  `vector_proj` , and the  `group`  variants using different datasets? It would be fascinating to see how these techniques come together to enhance signal generation or optimize portfolio construction!

---

### 评论 #2 (作者: AK98027, 时间: 1年前)

This is an excellent post with highly actionable strategies! I am also sharing my thoughts on this-

1. **Uncommon Operators ( `vector_neut` ,  `vector_proj` ,  `regression_neut` ,  `regression_proj` )** :
   - **Impact:**  Reduce correlation, improve Sharpe ratios, and enhance alpha specificity by isolating unique signals.
   - **Best Use:**  Effective with structured data like price-volume or fundamental datasets. Example: neutralizing against benchmarks or sector trends.
2. **Group Operators ( `group_coalesce` ,  `group_cartesian_product` )** :
   - **Impact:**  Enhance fitness and stability by creating diverse signals through custom neutralizations and unique data combinations.
   - **Best Use:**  Ideal for hierarchical datasets (e.g., industries, regions, ESG metrics).
3. **Underutilized Datasets** :
   - **Impact:**  Generate novel alphas with high Sharpe ratios and unique return profiles by analyzing niche datasets.
   - **Best Use:**  Alternative data (e.g., satellite, credit card data) or specialized macro datasets.

**Overall:**  These strategies reduce correlation and improve alpha performance by uncovering unique signals and optimizing data relationships. A great framework for advancing alpha research.

---

### 评论 #3 (作者: CA42779, 时间: 1年前)

Thanks for the insights the operators are working well.

---

### 评论 #4 (作者: AT56452, 时间: 1年前)

A tip to make submittable alphas - Keep a repository of booster alphas that you can use to make submittable alphas. You can use booster alphas with alphas that are near the threshold required for submitting alphas. For example, required sharpe is 1.58 and your alpha has a sharpe of 1.50. In this case just add the booster alpha to the main idea to make the main alpha submittable. But make sure to keep the corr low as the over usage of booster alphas increase self and prod corr which impacts the portfolio of your alphas.

---

### 评论 #5 (作者: YW42946, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)

Please be aware that this sort of behavior may be close to ensemble Alphas.
The booster Alphas you believed may be having drawdowns or flat lines in out-sample -> which will impact all your submissions that use this method. Please note that correlation can easily be cheesed, low correlation may not imply no concentration on certain idea.

We call this "research bias", and it is dangerous if your "research bias" to prone to only a few factors.

---

### 评论 #6 (作者: AT56452, 时间: 1年前)

[YW42946](/hc/en-us/profiles/12485882527255-YW42946)  - Thank you for pointing this out! I wasn't aware.

---

### 评论 #7 (作者: VV63697, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)  can you elaborate more on the second point like how one can actually build an intuition as to what groupings to actually use with the data plus whenever i try the group_cartesian product my correlation is still high enough .

---

### 评论 #8 (作者: AT56452, 时间: 1年前)

[SK95162](/hc/en-us/profiles/23496019416727-SK95162)

So, one helpful tip is - If you find a relationship between two kinds of data, say between news and sentiment or price, you can use vector_neut, vector_proj, regression_neut, regression_proj, ts_covariance, group coalesce, group_cartesian_product instead of ts_corr. Try this and let me know if it helped you!

---

### 评论 #9 (作者: AT56452, 时间: 1年前)

[SK95162](/hc/en-us/profiles/23496019416727-SK95162)

Also, while applying this, use data that has either zero or very a smaller number of alphas. If you're just starting, you can experiment with data that has a greater number of alphas, so that you know how the data works and how these operators work.

---

### 评论 #10 (作者: AT56452, 时间: 1年前)

A tip to make submittable alphas - The getting started series of articles on the community forum are extremely helpful for making alphas with pretty less correlation. Just spend an hour or so on each article and apply the things mentioned in the articles. In a couple of hours, you will surely find pretty good alphas.

---

### 评论 #11 (作者: AT56452, 时间: 1年前)

A tip to make submittable alphas - Make a repository of alpha templates and note them down in a document. Make a table that has the template and the data with which it works well. Noting down what works and what doesn't work helps you especially on days when you're struggling to build submittable alphas, re out of ideas and have spent considerable time on making one and you still aren't done. Also, you can try using these templates with data other than the data with which the template usually works well.

---

### 评论 #12 (作者: AM71073, 时间: 1年前)

Great tips! I really like the emphasis on using  **uncommon operators**  like  `vector_neut`  and  `regression_proj` —they can be very effective at reducing correlation by introducing more complexity and variation to the alpha construction. I would also add that it's helpful to experiment with  **different lookback periods**  for certain operators, as they can sometimes reveal signals that aren't immediately obvious with shorter periods.

Regarding the  **group operators** , using  **custom neutralizations**  with data that has fewer alphas can be a game changer, especially when you apply it to less commonly explored datasets. These datasets might reveal unique insights that can help create more independent alphas.

A suggestion: when filtering datasets, make sure to  **validate**  the stability and robustness of the alphas over time. Even if a dataset has fewer alphas, it’s important to test how these alphas perform across different market conditions to ensure the correlation stays low.

Looking forward to more of your ideas, this is really helpful!

---

### 评论 #13 (作者: AT56452, 时间: 1年前)

[VV63697](/hc/en-us/profiles/22631087402903-VV63697)  - For developing an intuition, I would suggest three things that have worked for me -

1) Spend time on the platform. There's no alternative to this one. You start getting a sense of what works and what doesn't after spending considerable time on the platform.

2) On days when you have some time, spend time reading the research papers recommended on the platform and try to make alphas using those. It'll seem difficult/impossible at times but it works. You start understanding the practical applications of the data available.

3) Try using different operators available on the platform and see which one works best with which kind of data. Attending the advisory sessions regularly helps a ton as you get to see live how to think while building alphas. Try new operators and ask questions about those operators during the advisory sessions/webinars.

---

### 评论 #14 (作者: AT56452, 时间: 1年前)

[VV63697](/hc/en-us/profiles/22631087402903-VV63697)  - You might be getting a high correlation because you're using sector, industry, country, etc as groups for max alphas you're making. Use other kinds of data fields as groups too. Using different kinds of data especially in group_cartesian_product yields uncorrelated alphas.

---

### 评论 #15 (作者: AT56452, 时间: 1年前)

Tip for making good alphas -

1) Test your alpha across universes to ensure it's robust.

2) Use neutralisations like crowding factors, fast factors, slow factors, slow and fast factors more than the usual ones.

---

### 评论 #16 (作者: AT56452, 时间: 1年前)

Tip to make good alphas - For alphas that have low coverage use ts_backfill. As ts_backfill is used a lot, you can also use kth element or group_backfill instead to reduce correlation. These work fine. For eg. this tip will come in handy when making alphas using news data.

---

### 评论 #17 (作者: AT56452, 时间: 1年前)

Tip to make good alphas - Instead of increasing the decay value in the settings use ts_decay_linear, ts_decay_exp_window, hump, hump decay, jump decay, etc.

---

### 评论 #18 (作者: AT56452, 时间: 1年前)

Tip to make good alphas - Use winsorize if you have large drawdowns in your pnl chart. ALso, make sure you test the robustness of this alpha even after using winsorize.

Drawdowns are the extreme dips you see in your pnl chart.

---

### 评论 #19 (作者: LN78195, 时间: 1年前)

Thank you for the detailed insights on reducing alpha correlation! What custom groupings have you found most effective for  `group_cartesian_product` , particularly with niche datasets or non-standard fields? Lastly, when leveraging uncommon operators like  `regression_proj` , are there specific datasets or scenarios where they consistently perform best? Looking forward to more practical examples to refine these strategies further!

---

### 评论 #20 (作者: VV63697, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)  yes actually i used industry , subindustry , others for grouping but the thing is for the other grouping data like the oth455 dataset we have those fields that use N2V or PCA to denoise or reduce the less important stuff from the data and using k-means algorithm to like make clusters . Now in principle i know how to use those unsupervised learning algorithms for data that i have and can visualize but here i don't understand how do they work with the data like when used with group operators are the above algorithms applied on the data or it's just a datafield which has data like others , how do we use it into grouping operators as to get a good signal because technically i don't see what i am doing here with them. This is assuming that i did not misunderstand the datafields and what they intend to do . For the other grouping datafields i cannot get what exactly are they doing like what is C20 split in that case how should i go about custom groupings and how should i learn to use them cause i can't just randomly apply groupings to see what works good right.

Thanks

---

### 评论 #21 (作者: AT56452, 时间: 1年前)

[VV63697](/hc/en-us/profiles/22631087402903-VV63697)  - Correct. Maybe create a post and copy this comment/problem there, pose a question, and tag an advisor. They'll be able to explain better. Also, to get an idea, read the research papers about the application of ML given on the platform. Those papers have helped me a ton. They might help you, too!

---

### 评论 #22 (作者: PM26052, 时间: 1年前)

Great tips, AT56452! I completely agree with the importance of using unconventional operators and understanding your dataset to reduce correlation. In addition to the operators you mentioned, experimenting with time-series operators like  `ts_decay_exp_window` ,  `ts_delta` , or  `ts_mean`  can help capture different temporal patterns in the data and often reduce correlations between alphas built on the same dataset.

Thanks for sharing these tips, and I look forward to more insights from you!

---

### 评论 #23 (作者: PN39025, 时间: 1年前)

I think we can use new regions that will have less alpha then the corr will be improved.Thanks for sharing another great tip that can be applied to your research process to improve it even more. I hope you will share more in the future

---

### 评论 #24 (作者: NT63388, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)  I just read your post today. I also carefully reviewed every suggestion in your comments, and they really made me reflect on my current methods.
I also noticed that you have a Value Factor (VF) of 0.95, so I think you’re my role model!

For a long time, my VF has been stuck at around 0.1x or 0.2x, so I’d like to ask you the following questions to improve my research approach.

**Your criteria when submitting Alphas** 
Do you have specific criteria that help you maintain a high VF and achieve nearly perfect tie-breaker scores in Genius? For example:

- Priority #1: Ensuring the Alpha has strong and concise signals (e.g., a low number of operators per Alpha, such as 5-8).
- Priority #2: Ensuring the Alpha passes Robustness Tests (e.g., rank(alpha), sign(alpha), sub-universe checks, 2-year test periods, etc.). Or do you not prioritize these tests much?
- Considering "IS Summary" metrics: Do you set specific thresholds like Sharpe >2.0 (or just 1.58 to meet the baseline), Drawdown <5%, Margin >10‱, Turnover <25%, and Returns/Drawdown >1? I’ve noticed diverse opinions on the importance of these benchmarks.
- Sharpe in the last two years: Do you aim for a Sharpe ratio of >=2.0 (or at least ensure it remains positive)?

Looking forward to learning from your insights! 🙏

---

### 评论 #25 (作者: NS94943, 时间: 1年前)

Great post,  [AT56452!](/hc/en-us/profiles/16716798553111-AT56452)

As has been rightly pointed out by others, trying the highest value datasets with your existing frameworks is the simplest approach to getting lower correlations. Also, since single dataset alphas (ATOMs) will be much more important from now on, finding statistical relationships between fields of the same dataset will be very useful in this regard.

---

### 评论 #26 (作者: NG78013, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #27 (作者: AT56452, 时间: 1年前)

Tip for reducing correlation, especially for GENIUS - Make alphas in lesser explored regions like Japan, Korea, Taiwan, China, America, etc. As these regions have a really small number of alphas it'll be easy to submit alphas in this region. Plus point is you can submit alphas easily in these regions by replicating the alpha ideas you already have in other regions like GLB, EUR, Asia, and the USA.

---

### 评论 #28 (作者: AT56452, 时间: 1年前)

Making alphas in unexplored regions will help you in increasing pyramid count and breaching the pyramid count for the Grandmaster level in Genius. After breaching the pyramid count, you can start submitting alphas with new ideas in regions like GLB, EUR, US and Asia because alphas from these regions are given more weight than the lesser explored regions. This strategy helps you in diversifying alphas, regions and reducing correlation.

---

### 评论 #29 (作者: AT56452, 时间: 1年前)

Most alphas you make in GLB can be replicated and submitted in all the other regions. So, a good strategy is to start building alphas in GLB and then moving on to submit the same alpha in other regions. DOing the opposite might not have the same effect as this strategy. Alpha submission on the platform and then gaining weight and value doesn't't only require consistent submissions and research for new ideas, it also requires one to be strategic in one's actions. So, you should have a plan for accomplishing certain goals according to the 1) areas you're lacking at and 2) the concurrent competition.

---

### 评论 #30 (作者: AT56452, 时间: 1年前)

Almost after every competition you have some time until the next competition is announced. In that cooling period of sorts, you should analyse your existing alphas and the strategy you're following and make required changes based on your performance. You should be able to understand and improvise in the areas you lacked in the last competition you participated in to improve in the next one. In this cooling period only, you should improve your research methodology and experiment with new datasets and operators to understand which work well or which are the datasets you're able to understand well and focus on being good with those datasets. These are some strategic actions you can do to improve your work and get better while doing it. I do it quite often and I think it helps me a ton at getting better at what I do.

---

### 评论 #31 (作者: AT56452, 时间: 1年前)

A good template for beginners would be using a group operator then a time series operator then rank/scale/score/winsorize and then one less explored data field to build a good alpha. Characteristics like coverage, frequency, etc. of the kind of data field you're using should be taken into account when choosing the groups, number of days, etc.

---

### 评论 #32 (作者: AT56452, 时间: 1年前)

Astutely understanding the operators in terms of the math and the logic behind them is essential for using them appropriately with data-fields. This understanding helps you visualise how will the data-field interact with the operator and what will the outcome be before you get the simulation results and this helps a ton in building good alphas. Building this logic in your head also helps you decipher the research papers and make alphas using them because while reading the research paper, from its language you know which operation should be used.

---

### 评论 #33 (作者: AS34048, 时间: 1年前)

Using the unexplored datafields and operators will bring diversity in alphas and eventually reduce the correlation .

---

### 评论 #34 (作者: NT63388, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)  
Thank you so much for your helpful sharing.

Can you share more about your perspective on my previous question? [[L2] Reducing correlation of alphas.md/comments/28613251833751]([L2] Reducing correlation of alphas.md/comments/28613251833751)

---

### 评论 #35 (作者: AT56452, 时间: 1年前)

[NT63388](/hc/en-us/profiles/6348096761239-NT63388)

Hey! Thanks for such nice comments and questions!

The GENIUS tiebreaker scores - The strategies I'm using I'm already adding them as comments under this post pretty honestly.

Priority 1 - Yes. I try to keep my alpha as simple as possible. I like it to have a solid logical base. I try to use the least number of data fields/operators as much as it is possible.

Priority 2 - Sometimes I check my alphas using these tests sometimes I don't. Depends on how much time I have that day. But usually, you'll see if your alpha is logical it'll automatically pass these tests. Also, even if the shape and fitness are just passing the submission criteria, the OS performance of these alphas will be good if the alphas has a solid logic.

Priority 3 -  So, I am not very picky about the sharpe and fitness of an alpha. It should be good enough/submittable. But I do care about the drawdowns, returns/drawdown, and margins. Also, drawdowns, returns/drawdown, and margins have different ideal numbers based on the region you're building alphas in. You can ask your advisor about it. They'll guide you better in this respect. I try to diversify turnover values. I don't think it's ever a good idea to just stick to 25% or 10% or whatever. See, I think every question you ask about the characteristics of an alpha I believe diversity is the key. The more diverse your alphas are in every aspect possible, the better your overall portfolio value would be.

Priority 4 - Sharpe in the last two years - I don't excessively focus on this. This is because sometimes when we think about these criteria having a certain value we tend to overfit. Overfitted alphas don't work well in OS. So, overall if I see that the alpha is doing well in most years, it's a good to go for me.

I hope this was helpful for you! Keep the questions coming! Also, I wanted to know how long has it been since you've been a consultant?

---

### 评论 #36 (作者: NT63388, 时间: 1年前)

@ [AT56452](/hc/en-us/profiles/16716798553111-AT56452)

First of all, thank you so much for your feedback.
It has truly helped clear my mind quite a bit.
I’ve spent too much time thinking about the conditions under which an Alpha would be good enough. I even calculated the similarity with poorly rated Alphas from the past. And as you mentioned, that made the Alpha overfit.
However, without any conditions for selecting Alphas, I worry that the probability of picking a bad Alpha would be higher (since finding a good Alpha is usually much harder than creating a bad one).

I’ve been a Consultant for nearly two years now. Since my VF is usually not high, Alpha hasn’t brought me much financial value, but it has provided me with a research environment and the opportunity to meet friends like you.
I deeply appreciate that.

---

### 评论 #37 (作者: AT56452, 时间: 1年前)

Tip - Try and submit alphas that are risk neutralised. So, your neutralisation settings should be crowding factors, slow factors, fast factors, and slow and fast factors mostly because these shield you from macro risks and market risk in general. Also, the OS performance is pretty reliable when you use these and similar to what you see in IS, or at least is good enough in the OS.

---

### 评论 #38 (作者: AT56452, 时间: 1年前)

I've been facing many issues with the total number of operators and I'm currently at 177. The total is supposedly 181 as that's the highest number on the genius leaderboard. So, I'm mentioning the operators I've used below. Hope this helps you guys.

---

### 评论 #39 (作者: AT56452, 时间: 1年前)

Below mentioned are all the reduce_ operators -

- reduce_norm
- reduce_sum
- reduce_max
- reduce_min
- reduce_avg
- reduce_choose
- reduce_range
- reduce_percentage
- reduce_stddev
- reduce_ir
- reduce_skewness
- reduce_kurtosis
- reduce_powersum
- reduce_count

---

### 评论 #40 (作者: AT56452, 时间: 1年前)

- abs
- and
- arc_cos
- arc_sin
- arc_tan
- bucket
- ceiling
- clamp
- combo_weight
- convert dollar2share
- count
- days_from_last_change
- equal
- exp
- filter

---

### 评论 #41 (作者: AT56452, 时间: 1年前)

- floor
- generate_stats
- group_backfill
- group_count
- group_extra
- group_max
- group_mean
- group_median
- group_min
- group_neutralize
- group_normalize
- group_percentage
- group_rank

---

### 评论 #42 (作者: AT56452, 时间: 1年前)

- group_scale
- group_std_dev
- group_sum
- group_vector_neut
- group_vector_proj
- group_zscore
- hump
- hump_decay
- if_else
- inst_pnl
- inst_tvr

---

### 评论 #43 (作者: AT56452, 时间: 1年前)

- is_finite
- is_nan
- is_not_finite
- is_not_nan
- keep
- kth_element
- last_diff_value
- left_tail
- less
- log
- log_diff

---

### 评论 #44 (作者: AT56452, 时间: 1年前)

- max
- min
- nan_mask
- nan_out
- negate
- normalize
- not
- one_side
- or
- pasteurize
- position_safeguard
- power
- purify
- quantile
- rank

---

### 评论 #45 (作者: AT56452, 时间: 1年前)

- rank_by_side
- rank_gmean_amean_diff
- regression_neut
- replace
- reverse
- right_tail
- round
- round_down
- s_log_1p
- scale
- self_corr
- sigmoid
- sign
- signed_power
- sqrt

---

### 评论 #46 (作者: AT56452, 时间: 1年前)

- tail
- tanh
- to_nan
- trade_when
- truncate
- ts_arg_max
- ts_arg_min
- ts_av_diff
- ts_backfill
- ts_co_kurtosis
- ts_co_skewness
- ts_corr
- ts_count_nans
- ts_decay_linear
- ts_delay
- ts_delta
- ts_entropy

---

### 评论 #47 (作者: AT56452, 时间: 1年前)

- ts_ir
- ts_kurtosis
- ts_max_diff
- ts_mean
- ts_median
- ts_min
- ts_min_diff
- ts_min_max_cps
- ts_min_max_diff
- ts_moment
- ts_partial_corr
- ts_percentage
- ts_poly_regression
- ts_product
- ts_quantile
- ts_rank

---

### 评论 #48 (作者: AT56452, 时间: 1年前)

- ts_rank_gmean_amean_diff
- ts_regression
- ts_returns
- ts_scale
- ts_skewness
- ts_std_dev
- ts_step
- ts_sum
- ts_theilsen
- ts_triple_corr
- ts_vector_neut
- ts_vector_proj
- ts_weighted_decay
- ts_zscore
- unit
- universe_size
- vector_neut

---

### 评论 #49 (作者: AT56452, 时间: 1年前)

- winsorize
- zscore
- Arithmetic operators: subtract, add, divide, multipl, power
- <,  >, >=, <=, !=
- cond ? expr1 : expr2
- add(x, y, filter = false), x + y
- divide(x, y), x / y
- fraction(x)
- inverse(x)
- multiply(x ,y, ... , filter=false), x * y
- subtract(x, y, filter=false), x - y
- jump_decay(x, d, sensitivity=0.5, force=0.1)
- ts_delta_limit(x, y, limit_volume=0.1)
- ts_target_tvr_delta_limit(x, y, lambda_min=0, lambda_max=1, target_tvr=0.1)

---

### 评论 #50 (作者: AT56452, 时间: 1年前)

- ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)
- rank(x, rate=2)
- generalized_rank(open, m=1)
- regression_proj(y, x)
- scale_down(x,constant=0)
- vector_proj(x, y)
- vec_avg(x)
- vec_choose(x,nth=k)
- vec_count(x)
- vec_ir(x)
- vec_kurtosis(x)
- vec_max(x)
- vec_min(x)
- vec_norm(x)
- vec_percentage(x,percentage=0.5)
- vec_powersum(x,constant=2)

---

### 评论 #51 (作者: AT56452, 时间: 1年前)

- vec_range(x)
- vec_skewness(x)
- vec_stddev(x)
- vec_sum(x)
- vec_filter(vec, value=nan)
- group_coalesce(original_group, group2, group3,…)
- group_rank(x, group)
- group_cartesian_product(g1, g2)

---

### 评论 #52 (作者: VV63697, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)  Thanks for the list of operators , i wanted to know what arguments do position safeguard and combo weight operators take .

---

### 评论 #53 (作者: TD84322, 时间: 1年前)

Thanks for sharing these insightful tips! They are super helpful for building robust and less correlated alphas. I'll try these out, especially using custom neutralizations and exploring lesser-used datasets and operators. Looking forward to more ideas in this thread!

---

### 评论 #54 (作者: DN41247, 时间: 1年前)

Thank you  [AT56452](/hc/en-us/profiles/16716798553111-AT56452)  for the helpful tip! Neutralizing risk factors like crowding, slow, and fast ones is a great strategy for reducing macro risks and ensuring reliable OS performance. Much appreciated!

---

### 评论 #55 (作者: DK30003, 时间: 1年前)

A tip to make submittable alphas - Keep a repository of booster alphas that you can use to make submittable alphas. You can use booster alphas with alphas that are near the threshold required for submitting alphas. For example, required sharpe is 1.58 and your alpha has a sharpe of 1.50. In this case just add the booster alpha to the main idea to make the main alpha submittable. But make sure to keep the corr low as the over usage of booster alphas increase self and prod corr which impacts the portfolio of your alphas.

---

### 评论 #56 (作者: PN39025, 时间: 1年前)

[AT56452](/hc/en-us/profiles/16716798553111-AT56452)  Hi, can you share your experience in choosing alpha to submit based on performance criteria? Thank you.

---

### 评论 #57 (作者: AT56452, 时间: 1年前)

[PN39025](/hc/en-us/profiles/1532011933942-PN39025)  - More than choosing which alpha to submit, I research beforehand, find a good idea and improve it enough to be able to submit it. So, the settings and operators and everything else is based on that logic only. For eg. if an alpha shows better performance using the industry neutralisation but according to the idea and the economic logic my initial plan was to use subindustry neutralisation, then I submit the alpha in subindustry only because that makes more sense to me than just chasing the numbers.

---

### 评论 #58 (作者: PN39025, 时间: 1年前)

Xin chào  [AT56452](/hc/en-us/profiles/16716798553111-AT56452) , bạn có thể hướng dẫn tôi cách sử dụng 3 toán tử universe_size, position_safeguard, combo_weight không? Tôi không thấy nó trên nền tảng. Cảm ơn bạn.

---

### 评论 #59 (作者: XN41151, 时间: 1年前)

I appreciate the thorough explanation on managing alpha correlation! Could you share which custom groupings work best when using group_cartesian_product/group_coalesce, especially with unique datasets or unconventional fields? Additionally, are there particular datasets or situations where lesser-used operators like regression_proj tend to deliver reliable results? Excited to hear more practical use cases to enhance these approaches!

---

### 评论 #60 (作者: SK14400, 时间: 1年前)

Thank you for sharing these insightful tips on reducing alpha correlation! The practical strategies like using unique operators, leveraging group functions, and focusing on underutilized datasets are incredibly helpful for refining approaches. Looking forward to more ideas in this thread!

---

### 评论 #61 (作者: ZH78994, 时间: 1年前)

By following these tips, you can create a SuperAlpha that is less prone to overfitting, more diversified, and ultimately better positioned to perform in out-of-sample testing. The key is to focus on building diverse, independent signals that capture different facets of market behavior, avoiding redundancy and ensuring long-term robustness.

Let me know if you’d like more specific examples or further elaboration on any of these strategies!

---

### 评论 #62 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #63 (作者: YC82708, 时间: 1年前)

This article provides some useful strategies to reduce correlation in alpha models. I found the suggestion to use uncommon operators like  `vector_neut` ,  `vector_proj` , and  `regression_neut`  particularly insightful. These operators can introduce variability in the way alphas interact with the data, which helps in avoiding redundancy and overfitting. The idea of using group operators with custom neutralizations (e.g.,  `group_coalesce`  and  `group_cartesian_product` ) is also a great way to increase the diversity of the alphas while maintaining their relevance to the dataset. Additionally, the recommendation to filter datasets based on the number of alphas it contains and then tailor the alpha model to the dataset’s characteristics is a smart approach. This method not only helps in reducing correlations but also improves the overall understanding of the data, which can lead to the creation of more robust and submittable alphas. The practical, hands-on nature of these tips is valuable for anyone looking to fine-tune their alpha strategies.

---

### 评论 #64 (作者: CC40930, 时间: 1年前)

These tips are really insightful and practical! Focusing on lesser-used operators and exploring underutilized datasets is a great approach to innovate while reducing correlation. I especially appreciate the emphasis on understanding datasets deeply before applying operators—that's a step often overlooked but crucial for generating unique alphas. Looking forward to seeing more ideas in this thread! Keep them coming! 🚀

---

### 评论 #65 (作者: ND68030, 时间: 1年前)

Another important factor in reducing correlation between alphas is diversity in input factors. By using different data sources, such as price data, macroeconomic data, and market behavior, you can reduce the correlation between alphas. This way, the alphas will be less influenced by the same set of factors and can operate more independently, improving their ability to diversify and reduce overlap in trading strategies

---

### 评论 #66 (作者: KP26017, 时间: 1年前)

You can try unlinear-combination, such as using if/else combination. It will be best if you can filter some condition with logic back ground. Eg: if price_volume is high correlation alpha, you want to combine with social media is low correlation alpha:

If(arg_max(close,5) <1  (date with near the peak of alpha)

then social media data (near peak mean more favor on social media)

else reversal idea (keep price-volume high correlation idea)

---

### 评论 #67 (作者: KP26017, 时间: 1年前)

You could attempt to reduce correlation by combining fields from different categories, but it is important to test this strategy to ensure it doesn’t degrade model performance. Alphas from different categories can provide more independent signals, potentially improving overall model performance.Make sure to test the model’s performance after making these changes and consider any computational overhead on the system.

---

### 评论 #68 (作者: NT63388, 时间: 1年前)

[ZH78994](/hc/en-us/profiles/22396335369111-ZH78994)

> you can create a SuperAlpha that is less prone to overfitting, more diversified, and ultimately better positioned to perform in out-of-sample testing.

I don't really understand your point. The operators vector_neut, vector_proj, regression_neut, and regression_proj are aimed at creating Regular Alpha with low correlation.

Are you also applying them to build Super-Alpha (within a "Combo Expression")?

If you can achieve that while maintaining Alpha quality, that would be fantastic. Please share how you do it.

---

### 评论 #69 (作者: AK40989, 时间: 1年前)

Reducing alpha correlation is crucial for effective model performance. I'm curious about how you determine the effectiveness of custom groupings when using operators like group_cartesian_product. What specific metrics or tests do you apply to evaluate their impact on alpha performance?

---

### 评论 #70 (作者: KK81152, 时间: 1年前)

### **Use Uncommon Operators**

- **Operators like  `vector_neut` ,  `vector_proj` ,  `regression_neut` , and  `regression_proj`**  are excellent for minimizing correlation because they neutralize common factors or project signals into independent spaces, making your alphas more unique.
- **Benefit** : These operators help to make your alphas more diverse, reducing overlap in signals and improving the overall performance when combined.

---

### 评论 #71 (作者: AS16039, 时间: 1年前)

These are great insights on reducing alpha correlation! Using uncommon operators like  `vector_neut` ,  `vector_proj` , and  `group_cartesian_product`  can significantly enhance signal uniqueness. Exploring underutilized datasets and custom groupings also helps. Applying these techniques strategically across different regions could further optimize alpha diversity.

---

### 评论 #72 (作者: PT27687, 时间: 1年前)

Your insights on reducing alpha correlation are highly valuable, especially the emphasis on using uncommon operators and understanding unique datasets. I find it interesting how different operators can lead to more innovative approaches. Have you encountered any specific datasets that particularly benefited from your suggested methods? I'd love to hear more about those cases!

---

### 评论 #73 (作者: JK98819, 时间: 1年前)

Really helpful insights — especially the emphasis on exploring  **underutilised datasets**  and using  **less common operators**  like  `vector_proj`  and  `regression_neut`  to diversify alpha construction. That’s a practical strategy for both originality and lower correlation.

---

### 评论 #74 (作者: HY24380, 时间: 11个月前)

**Interesting Finding: Neutralization Level Impact on Production Correlation**

I encountered an interesting result regarding neutralization granularity and its effect on production correlation metrics.

**Issue:**  Despite extensive efforts to bring production correlation below the required threshold, including experimenting with various operators and similar data fields, the correlation remained persistently high.

**Solution:**  The breakthrough occurred when I adjusted the neutralization level from a subindustry to an industry classification. This single change brought the production correlation within acceptable thresholds without compromising other key performance metrics such as the Sharpe ratio or fitness scores.

**Key Observation:**  The broader industry-level neutralization effectively reduced unwanted factor exposures while maintaining alpha generation capability, suggesting that the subindustry-level neutralization may have been too granular for this particular alpha expression.

**Request for Community Input:**

- Has anyone experienced similar issues where neutralization granularity significantly impacted correlation metrics?
- Are there illustrative examples or best practices for determining optimal neutralization levels?
- What frameworks do you use to balance neutralization effectiveness with alpha preservation?

Any insights or experiences from the community would be highly valuable for understanding this relationship between neutralization scope and factor exposures.

---

