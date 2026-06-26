# [BRAIN TIPS] Improve your alphas with the right settings

- **链接**: [Commented] [BRAIN TIPS] Improve your alphas with the right settings.md
- **作者**: NL41370
- **发布时间/热度**: 2年前, 得票: 12

## 帖子正文

**What are the current available simulation settings in BRAIN?**

You can check the following link for more detailed documentation:  [settings](https://platform.worldquantbrain.com/learn/documentation/create-alphas/simulation-settings) . Some particular configurations which will have great impact on your alphas’ performance are “Delay”, “Decay”, “Truncation”, “Neutralization”.

**How each simulation settings effect alpha performance?**

Let’s implement an alpha idea where we weight the stocks by its company dividend yield for a month:

*ts_zscore(mdf_yld,20)*

With settings:

![image](images/img_cb51474a32.png)

We have the following performance metrics:

![image](images/img_31f79f9bd8.png)

Here we will experiment with some different settings to see how the performance metrics is effected:

![图片](images/img_a9a1599e95.png)

*Green: mean the metric becomes better, Red: mean the metric becomes worse, Blue: mean the metric doesn’t change much.

Please note that the above results served as a suggestion, it is not meant to be a strict guideline on how you should choose your simulation settings. Because each alpha idea will have a different suitable settings.

Even though, simulation settings rely on how you implement alpha ideas.  [A general rule of thumb is neutralizing your alpha into a smaller bucket generally improves your Sharpe ratio](https://platform.worldquantbrain.com/learn/documentation/create-alphas/neut-cons) , which in turn improves the fitness score. Increasing decay is generally good at lowering your alpha’s turnover, which also affect the fitness score.  Drawdown and Margin is more dependent on your original alpha ideas, and your alpha’s universe.

---

## 讨论与评论 (7)

### 评论 #1 (作者: IS67473, 时间: 1年前)

It is better to have lower values for decay. To reduce turnover, try utilizing operators within your alpha expression, like trade_when instead of increasing decay. Delay isn't a setting that is to be used for optimization. Delay 1 and Delay 0 research has fundamental differences.

It is advisable to not overfit your alpha on specific metrics. It is okay to optimize an alpha for a lower correlation as long as you aren't deteriorating the performance significantly.

---

### 评论 #2 (作者: NH84459, 时间: 1年前)

Hello, I would like to ask, for example, I set truncation in the setting to 0.01, but my alpha is nested in the truncation function to 0.1, so how will the total truncation of that alpha be calculated in the end?

---

### 评论 #3 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #4 (作者: TT55495, 时间: 1年前)

If you were to test the performance of an alpha using different simulation settings, how would you prioritize settings like delay and decay to optimize the alpha's performance for specific market conditions?

---

### 评论 #5 (作者: NH84459, 时间: 1年前)

Hi, I would like to ask if it is advisable to use settings that make the alpha worse but reduce the correlation?

---

### 评论 #6 (作者: CC40930, 时间: 1年前)

Simulation settings in BRAIN, such as Delay, Decay, Truncation, and Neutralization, can have a significant impact on alpha performance. These settings are used to experiment and adjust various factors that influence the overall results of your alpha ideas. For example, in an alpha idea where you weight stocks by their dividend yield (using  `ts_zscore(mdf_yld,20)` ), different simulation settings can affect performance metrics like Sharpe ratio, turnover, and drawdown.

---

### 评论 #7 (作者: KJ42842, 时间: 1年前)

[TT55495](/hc/en-us/profiles/13132630342807-TT55495)

Setting can be prioritized based on alpha idea, update frequency of datasets and so on.

---

