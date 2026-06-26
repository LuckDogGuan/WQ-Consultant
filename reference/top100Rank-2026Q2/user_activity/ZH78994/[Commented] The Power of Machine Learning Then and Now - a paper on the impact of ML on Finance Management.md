# The Power of Machine Learning: Then and Now - a paper on the impact of ML on Finance Management

- **链接**: [Commented] The Power of Machine Learning Then and Now - a paper on the impact of ML on Finance Management.md
- **作者**: TB57255
- **发布时间/热度**: 2年前, 得票: 7

## 帖子正文

This is a paper I did for the FP&A Trends Group (a multinational professional body) reflecting on how I would have used the latest ML techniques as a Finance Manager had they been available to me then. It may be of interest to some of the community.  [https://fpa-trends.com/article/machine-learning-then-and-now](https://fpa-trends.com/article/machine-learning-then-and-now)   Tom

---

## 讨论与评论 (18)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi Tom!

Great paper, thanks for sharing!

Models that predict sales and earnings have great potential for alpha creation. On the platform, we have ready-to-use predictions from analysts, but we can also build simple models using expression language. Here are three examples:
1. We can implement auto-regression using the ts_regression operator and try to predict future sales using sales values from a quarter ago and a year ago.
2. We can implement cross-sectional auto-regression within a sector or industry using the group_mean operator.
3. We can use 1, 2, 3, 4 point ts_delta to approximate a first-order derivative and use it as a trend.

A combination of all three methods might help to create a model for sales prediction.
Generally, Machine Learning (ML) is a very powerful tool for quantitative researchers, however, implementing it in alphas has its limitations for several reasons. For instance, if we use quarterly or annual data, we don't have many points to train the model and avoid overfitting. Could you please share any additional ideas you might have on the challenges one might encounter while developing ML models on time-series data?

But ML can definitely be helpful for research automation and searching for optimal parameters in alpha expressions. By using the BRAIN API, we can implement a genetic algorithm for alpha expression creation. (there is still a risk of overfitting, so it is essential to split data into training and validation sets).

Anastasia

---

### 评论 #2 (作者: XL31477, 时间: 1年前)

[AG20578](/hc/en-us/profiles/12243980162327-AG20578) Anastasia, you've made really good points there. When developing ML models on time-series data, another challenge is dealing with seasonality. If not properly accounted for, it can mess up the model's predictions. Also, changes in market conditions over time can make historical data less relevant for training. And the choice of features matters a lot too. Picking the wrong ones might lead to poor performance. Regarding overfitting, splitting data into training and validation sets is key indeed. And using cross-validation can further help assess how well the model generalizes.

---

### 评论 #3 (作者: TB57255, 时间: 1年前)

Thanks Anastasia for your kind comments and interesting points and thanks XL31477. I dealt with seasonality by creating a 13 dimensional multiple regression with one variable for time and 12 dummies to represent each month. This turned out to be pretty good for automotive, but hospitality, for example, required another dummy variable for the moveable feast of Easter. Changes in market conditions I dealt with by weighting the more recent data. I look forward to trying out Anastasia’s suggestions in alphas. The challenges are as you suggest making sure we have all the factors in the model and enough data points to do a reasonable regression. Also make sure to do the analysis at the correct level, as summarised data can hide trends. Tom

---

### 评论 #4 (作者: BA51127, 时间: 1年前)

Your approach to handling seasonality with a 13-dimensional multiple regression is quite innovative. However, I'm curious about how you propose to address the limitations of data points when working with quarterly or annual data, as Anastasia mentioned. Could you elaborate on any strategies or techniques you might use to mitigate the risks of overfitting in such scenarios, especially when dealing with limited data sets?

---

### 评论 #5 (作者: CC40930, 时间: 1年前)

This is a great reflection on the evolution of machine learning techniques in finance. It's fascinating to think about how these technologies could have transformed financial management processes when they were not as accessible. The integration of machine learning into financial forecasting and decision-making is now offering powerful new ways to streamline operations and improve accuracy. For anyone in the finance field, especially those in FP&A, this paper provides valuable insights into how emerging tools can reshape traditional approaches. Thanks for sharing, Tom!

---

### 评论 #6 (作者: KS69567, 时间: 1年前)

This is an excellent illustration of how machine learning methods have developed in the financial industry. It is interesting to consider how financial management procedures would have been drastically changed by these sophisticated technology, which were previously less available. Their broad accessibility today has surely changed how the sector makes decisions, manages risks, and develops strategies, opening up new avenues for creativity and efficiency. It's interesting to think about how machine learning will continue to progress and influence the financial industry in the future as its fast breakthroughs continue to push the envelope of what is possible.

---

### 评论 #7 (作者: TB57255, 时间: 1年前)

I used the standard error of the regression to calculate a confidence interval on the forecast. The fewer the data points, or the more irregular the history, or the further into the future the estimate, the wider this was. I could then calculate the likelihood of a forecast by its position within the confidence interval, thus: ‘there is a 40% chance of exceeding $6m but only a 5% chance of exceeding $7m.’ The interval could be determined by monte-carlo methods or by simply assuming a normal distribution. This would automatically correct for the number of data points and avoid over-fitting. Of course, you need a number of points to determine seasonality. From experience I found the minimum to be 1.5 cycles, but obviously, the more the better. Tom

---

### 评论 #8 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #9 (作者: ND68030, 时间: 1年前)

You're right that machine learning (ML) can be a powerful tool for quantitative research, particularly when it comes to developing  **alpha models**  based on historical data. However, as you pointed out, when working with time-series data, there are several  **challenges**  to consider, especially when it comes to  **training models**  and avoiding overfitting. Let's explore some of these challenges in more detail, along with some additional ideas and approaches you might consider.

---

### 评论 #10 (作者: TB57255, 时间: 1年前)

ZH78994 - thank you for your kind comments which have made my day. I have a couple more papers with the FP&A group:  [https://fpa-trends.com/article/british-coal-controlling-last-major-project](https://fpa-trends.com/article/british-coal-controlling-last-major-project)  which discusses the application of modelling techniques including machine learning to a very large project, and

[https://fpa-trends.com/article/systems-thinking-fpa-internal-audit-and-management-excellence-case-study](https://fpa-trends.com/article/systems-thinking-fpa-internal-audit-and-management-excellence-case-study)  which discusses the application of systems thinking and optimisation to the management of internal audit. I hope you enjoy them.

---

### 评论 #11 (作者: AK98027, 时间: 1年前)

You're right that machine learning (ML) can be a powerful tool for quantitative research, particularly when it comes to developing  **alpha models**  based on historical data. However, as you pointed out, when working with time-series data, there are several  **challenges**  to consider, especially when it comes to  **training models**  and avoiding overfitting. Let's explore some of these challenges in more detail, along with some additional ideas and approaches you might consider.

---

### 评论 #12 (作者: CC40930, 时间: 1年前)

That's an interesting read, Tom! It's always insightful to see how modern ML techniques could have impacted decision-making in finance. The evolution from traditional methods to machine learning can open up new possibilities for predictive analysis and more efficient financial management. I'll definitely check out the link! Thanks for sharing.

---

### 评论 #13 (作者: PP87148, 时间: 1年前)

Thanks for sharing this paper Tom, the below are some alpha strategies I understood from your paper

### **Sales Forecasting with Time-Series Models**

- **Alpha Strategy** : Invest in companies that show consistent improvement in their sales forecasting accuracy using advanced time-series models.
- **Implementation** : Use tools to analyze seasonal trends and forecast sales more accurately. Companies that can reduce forecast errors/ surprise (e.g., from 10% to 2%) are likely to have better cash flow management and more precise financial planning, making them strong candidates for outperformance in the market.
  some brain datafields are here :  **star_eps_surprise_prediction_12m**

---

### 评论 #14 (作者: PP87148, 时间: 1年前)

### **Inventory Optimization Using Clustering and Classification**

- **Alpha Strategy** : Identify companies optimizing inventory management through  **clustering**  and  **classification models** .
- **Implementation** : By applying clustering techniques, companies can identify slow-moving or obsolete inventory, optimizing stock levels and reducing waste. Classification models can categorize inventory (A, B, C items) to ensure efficient stock management, improving operational efficiency and profitability. Look for firms excelling in inventory management through AI-driven models to outperform competitors.
  Brain Datafields :  **inventory_turnover**

---

### 评论 #15 (作者: PP87148, 时间: 1年前)

### **Cash Flow and Capital Employed Forecasting**

- **Alpha Strategy** : Focus on companies using ML for advanced forecasting of  **cash flow**  and  **capital employed** .
- **Implementation** : Companies that use AI-driven financial models can predict short-term and long-term cash flows more accurately, ensuring they maintain optimal liquidity and profitability. Look for companies that are improving capital efficiency by using machine learning to forecast and manage their capital employed better.
  Brain Datafields:  **cashflow_op**

---

### 评论 #16 (作者: TB57255, 时间: 1年前)

Fantastic alphas! Very impressive.

---

### 评论 #17 (作者: DP14281, 时间: 1年前)

Your suggestion is helpful to generate high performance alpha

---

### 评论 #18 (作者: PN39025, 时间: 1年前)

Applying machine learning (ML) to time-series data for alpha generation comes with several challenges. Limited data, especially quarterly or yearly, makes training complex models difficult without overfitting. Financial data often exhibits autocorrelation and non-stationarity, which can mislead ML models unless handled with techniques like differencing or hybrid approaches. Overfitting is another risk, as historical patterns may capture noise rather than meaningful signals, making proper time-series cross-validation essential. Interpretability is also a concern, as black-box models lack transparency, highlighting the importance of using interpretable techniques like XGBoost or SHAP. Additionally, data snooping bias can result in poor generalization, requiring careful train-test splitting and out-of-sample testing. Regime changes in financial markets further complicate modeling, emphasizing the need for regime detection. Practical considerations like transaction costs and slippage must be accounted for during backtesting to ensure realistic predictions. Finally, for real-time applications, ML models must be optimized for latency and scalability to handle large datasets effectively. Addressing these challenges requires a balance of domain knowledge, robust techniques, and practical considerations.

---

