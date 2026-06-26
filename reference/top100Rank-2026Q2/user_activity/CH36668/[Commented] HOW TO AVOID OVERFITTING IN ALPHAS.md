# HOW TO AVOID OVERFITTING IN ALPHAS

- **链接**: [Commented] HOW TO AVOID OVERFITTING IN ALPHAS.md
- **作者**: CN44201
- **发布时间/热度**: 1年前, 得票: 9

## 帖子正文

**Avoiding Overfitting in Alpha Models:**

In quantitative finance and machine learning,  **overfitting**  occurs when a model is too closely fitted to historical data, capturing noise or random fluctuations that don't reflect the true underlying patterns. This results in a model that performs well on past data but fails to generalize to future data or real-world conditions. This is especially critical when trying to develop  **alpha models**  (models that aim to generate returns above the market average).

Here are some detailed strategies to avoid overfitting in alpha models:

### 1.  **Use Cross-Validation**

Cross-validation is a key technique to evaluate how your model will perform on unseen data. It involves splitting your data into multiple subsets (or folds) and training the model on some of them while testing it on the remaining ones. This ensures that the model isn’t simply memorizing the data and is able to generalize.

- **K-Fold Cross-Validation** : This technique splits the data into K folds, using K-1 for training and 1 for testing. The process is repeated K times, with each fold serving as the test set once.
- **Time-Series Cross-Validation** : In finance, cross-validation methods should respect the temporal nature of data. For time-series data, avoid using future data points to predict past data points. Instead, use walk-forward validation (train on past data and test on the future).

Cross-validation helps ensure your model’s robustness and performance beyond just the training dataset.

### 2.  **Feature Selection and Dimensionality Reduction**

Overfitting can occur if the model has too many features, especially if some of them don’t have a meaningful impact on predicting returns or market movements. The more features you add, the greater the chance of capturing noise.

- **Regularization**  (L1/L2): L1 (Lasso) regularization can help eliminate irrelevant features by setting their coefficients to zero. L2 (Ridge) regularization can shrink the coefficients of less important features. These techniques penalize overly complex models and prevent overfitting by reducing the importance of irrelevant features.
- **Principal Component Analysis (PCA)** : PCA reduces the number of features by transforming them into a smaller set of uncorrelated variables, keeping the most important information while reducing the risk of overfitting.
- **Feature Engineering** : Carefully select features that have real economic or financial significance, rather than adding more features to increase complexity. Over-reliance on too many technical indicators, for instance, can make the model prone to overfitting.

### 3.  **Regularization**

**Regularization**  techniques are critical for controlling model complexity. Regularization adds a penalty to the model’s complexity, ensuring that it does not fit the noise in the data.

- **Ridge Regression (L2 Regularization)** : Ridge regression adds a penalty equal to the square of the magnitude of coefficients, which discourages large coefficients that could lead to overfitting.
- **Lasso (L1 Regularization)** : Lasso adds a penalty equal to the absolute value of coefficients, encouraging sparsity in the model (i.e., setting some coefficients to zero). This is useful for feature selection and reducing complexity.
- **Elastic Net** : This method combines L1 and L2 regularization, balancing both feature selection and shrinking coefficients. It’s a good choice when you have many correlated features.

**Regularization**  prevents the model from "over-learning" the details in the training data, forcing it to focus on the most meaningful relationships.

### 4.  **Use More Data**

A model that is trained on a limited dataset is more likely to overfit because it may capture noise or patterns that are specific to that small set of data.

- **More Historical Data** : Using a longer time series or more data points can help ensure the model captures genuine patterns, reducing the risk of overfitting.
- **Diversified Data** : Including data from different market environments (e.g., bull vs. bear markets, different economic conditions) can make the model more robust and prevent it from fitting only to one specific market regime.

However, simply adding more data is not a cure-all—ensure the data is relevant, and avoid adding irrelevant or noisy data.

### 5.  **Avoid Complex Models**

While more complex models may capture more intricate patterns, they also tend to be more prone to overfitting. Instead of using highly complex algorithms, consider:

- **Simple Models First** : Start with simpler models (e.g., linear regression, decision trees) and only increase complexity if necessary. Even sophisticated methods like neural networks or deep learning should be used cautiously, especially with limited data.
- **Tree-based Models** : Random Forests and Gradient Boosting Machines (GBMs) can be prone to overfitting, especially when too many trees or too deep trees are used. You can control overfitting by limiting the depth of trees, using early stopping, or tuning hyperparameters like  `max_depth`  or  `min_samples_split` .

### 6.  **Early Stopping**

**Early stopping**  is particularly important when training deep learning models or complex algorithms. It involves monitoring the performance of your model on the validation set during training, and stopping the training process when the validation performance starts to degrade, even if training performance is improving. This prevents the model from overfitting to the training data.

- **Monitoring Validation Loss** : During training, track the model's error on a separate validation set. If the error starts to increase, halt the training process even if performance on the training data continues to improve.

### 7.  **Ensemble Methods**

**Ensemble methods**  combine multiple models to improve predictive performance and reduce the likelihood of overfitting. By aggregating predictions from multiple models, ensemble methods reduce the variance (or overfitting) and bias in predictions.

- **Bagging** : Techniques like Random Forest are based on bagging (Bootstrap Aggregating), where multiple models are trained on different subsets of data. The final prediction is the average or majority vote across these models, reducing overfitting.
- **Boosting** : Methods like Gradient Boosting (XGBoost, LightGBM) build models sequentially, where each model attempts to correct the errors of the previous one. While boosting is more prone to overfitting than bagging, careful regularization and parameter tuning can mitigate this risk.

### 8.  **Out-of-Sample Testing**

Always test your model on out-of-sample data (data it has not seen during training) to assess how well it generalizes to unseen data. The out-of-sample test provides a more realistic measure of how the model will perform in live markets or real-world applications.

- **Holdout Sample** : Keep a portion of the data aside during model training to act as a "test set." This is crucial for ensuring the model doesn’t just memorize the training data.
- **Real-Time Paper Trading** : If possible, simulate your model in real-time markets (paper trading) to see how it performs with live data, without risking real capital. This helps ensure that the model doesn't overfit to historical data.

### 9.  **Avoid Over-Tuning Hyperparameters**

Hyperparameter tuning can help improve model performance, but excessive tuning on the training data can lead to overfitting.

- **Use a Validation Set for Tuning** : Tune your hyperparameters using a validation set rather than the training set to prevent tailoring the model too closely to the training data.
- **Random Search vs Grid Search** : Instead of exhaustively searching through all hyperparameters, consider using  **random search**  to explore the hyperparameter space. Random search is less likely to overfit compared to grid search, especially for models with many hyperparameters.

### 10.  **Incorporate Domain Knowledge**

While data-driven models are powerful, combining them with domain expertise (e.g., economic theory, financial principles) can provide better insights and prevent overfitting to spurious patterns. Theories and models based on economic fundamentals are less likely to overfit compared to pure data-driven approaches.

### Key Takeaways:

1. **Cross-validation** : Use techniques like K-fold or time-series cross-validation to evaluate performance on unseen data.
2. **Regularization** : Apply L1 or L2 regularization to prevent the model from becoming overly complex.
3. **Simpler Models** : Start with simple models and only increase complexity when necessary.
4. **Ensemble Methods** : Combine multiple models to reduce variance and overfitting.
5. **Out-of-Sample Testing** : Ensure your model performs well on data it hasn’t seen before.
6. **Avoid Over-Tuning** : Excessive fine-tuning can lead to models that only perform well on the training data.

By combining these strategies, you can reduce the risk of overfitting and develop more robust alpha models that generalize well to future market conditions.

---

## 讨论与评论 (40)

### 评论 #1 (作者: HN20653, 时间: 1年前)

Overfitting is one of the biggest challenges when developing alpha models, and this article offers a series of very useful strategies! Using regularization, cross-validation, and out-of-sample testing helps ensure that the model is not just “rote learning” historical data but can generalize better to real market conditions.

---

### 评论 #2 (作者: JB26214, 时间: 1年前)

Overfitting is a major issue in alpha models; use regularization, cross-validation, and out-of-sample testing to improve generalization.

---

### 评论 #3 (作者: TP85668, 时间: 1年前)

The article provides a comprehensive guide to mitigating overfitting in alpha models, covering essential techniques such as cross-validation, regularization, and ensemble methods. It effectively balances theoretical concepts with practical applications, making it valuable for both quantitative finance professionals and machine learning practitioners. However, a deeper discussion on regime shifts in financial markets and their impact on model robustness could further enhance its applicability in real-world scenarios.

---

### 评论 #4 (作者: AN83376, 时间: 1年前)

I completely agree with your approach to preventing overfitting in alpha models. The strategies outlined, such as using regularization, cross-validation, and out-of-sample testing, are essential for ensuring models generalize well beyond historical data.

Given the evolving nature of financial markets, how do you adjust your models to account for regime shifts, and do you use any specific techniques to improve model robustness in such conditions?

---

### 评论 #5 (作者: AK40989, 时间: 1年前)

The strategies outlined for avoiding overfitting in alpha models highlight the importance of balancing complexity with generalization. While techniques like regularization and cross-validation are essential, the role of domain knowledge in feature selection cannot be overstated.

---

### 评论 #6 (作者: NM12321, 时间: 1年前)

In my personal opinion, overfitting in alpha is when you combine too much alpha to make the is good, but the os is bad. To avoid overfitting, in addition to using the test period available on the platform, you can change the universe of alpha and synthesize to get the final result.

---

### 评论 #7 (作者: JL20361, 时间: 1年前)

Does anyone know that whether we can use machine learning technique in API to do alpha research?

---

### 评论 #8 (作者: CH36668, 时间: 1年前)

The strategies discussed—regularization, cross-validation, and out-of-sample testing—are crucial for building models that generalize effectively beyond historical data.

---

### 评论 #9 (作者: DV64461, 时间: 1年前)

Thank you! In summerize, avoiding overfitting in alpha models is crucial to ensuring robust performance in live markets. Here are key strategies:

1. **Out-of-Sample Testing**  – Always validate alphas on unseen data, avoiding excessive optimization on historical datasets. Use  **walk-forward testing**  to mimic real-time performance.
2. **Avoid Data Mining Bias**  – Running too many backtests leads to spurious results. Use  **statistical significance tests**  (e.g., t-tests, p-values) to ensure findings are not due to randomness.
3. **Feature Selection**  – Focus on  **economically sound factors**  rather than adding numerous data points that may not generalize. Avoid excessive use of technical indicators without clear rationale.
4. **Regularization & Simplicity**  – Avoid over-complicated models with too many parameters. Simple, interpretable alphas tend to generalize better than highly complex ones.
5. **Diversification of Alphas**  – Instead of relying on a single alpha signal, combine  **uncorrelated alphas**  to create a more stable and resilient strategy.
6. **Decay Analysis**  – Track the persistence of alpha signals over time. If performance deteriorates quickly, it may be overfitted to past market conditions.
7. **Market Regime Awareness**  – Ensure alphas work across different market environments rather than excelling only in specific conditions.
8. **Transaction Cost Modeling**  – Include realistic execution costs and slippage in backtests to prevent over-optimistic results.

A good alpha must be  **persistent, scalable, and robust** —not just optimized for historical performance. What’s your approach to balancing alpha complexity and generalizability?

---

### 评论 #10 (作者: AK44462, 时间: 1年前)

Financial markets evolve, so adjusting models for regime shifts is crucial. I use adaptive learning, rolling window analysis, and feature selection techniques to enhance robustness and ensure models remain effective across changing conditions.

---

### 评论 #11 (作者: SK90981, 时间: 1年前)

Alpha models that are overfitted may become unreliable and perform poorly in the actual world.  Generalization is enhanced by the use of regularization, cross-validation, and simpler models.  Robustness is further reinforced by out-of-sample testing and ensemble approaches.

---

### 评论 #12 (作者: SM35412, 时间: 1年前)

When considering model complexity in Alpha research, how do you determine the balance between simplicity and the need for more intricate models? Specifically, do you think simpler models like linear regression or decision trees can capture enough patterns in financial data, or is there a point where more complex models like neural networks become necessary? Additionally, how do you manage the risk of overfitting when using tree-based models like Random Forests or Gradient Boosting Machines, especially with limited data? What techniques do you find most effective in controlling overfitting while maintaining model performance?

---

### 评论 #13 (作者: DD24306, 时间: 1年前)

To avoid overfitting in alpha models, focus on cross-validation, regularization, feature selection, and robust testing. Use time-series cross-validation (walk-forward validation) instead of standard K-fold to respect market chronology. Apply L1/L2 regularization to control model complexity and eliminate noise. Limit features through PCA or feature importance ranking, ensuring only relevant signals are used. Start with simpler models before increasing complexity, and prevent over-tuning by balancing hyperparameter optimization with generalizability. Use ensemble methods (bagging, boosting) to reduce variance and improve stability. Always conduct out-of-sample testing and paper trading to validate real-world performance. Lastly, incorporate domain knowledge to ensure models align with fundamental market principles, reducing reliance on data-mined patterns.

---

### 评论 #14 (作者: MB13430, 时间: 1年前)

The best way to avoid overfitting is to keep the idea as simple as possible. To improve performance, try implementing it with different operators.

---

### 评论 #15 (作者: CM45657, 时间: 1年前)

### **How to Avoid Overfitting in Alphas**

Overfitting happens when an alpha strategy  **performs well in backtests but fails in live trading**  due to being overly tuned to past data. Here’s a structured approach to  **detect, prevent, and fix overfitting**  in quantitative strategies.

## **1. Signs of Overfitting in Alphas**

If your alpha:
 Performs exceptionally well in backtests but fails out-of-sample.
Has  **too many parameters**  fine-tuned to past data.
Shows a  **Sharpe ratio above 3.0**  — often unrealistic.
 **Loses predictive power**  when slightly modifying inputs (e.g., 10-day vs. 11-day moving average). **Fails in different market conditions**  (e.g., only works in bull markets).

---

### 评论 #16 (作者: CM45657, 时间: 1年前)

overfitting can also be avoided by increasing decay to smoothen the alpha idea

---

### 评论 #17 (作者: SP39437, 时间: 1年前)

Thank you for the insightful article on avoiding overfitting in alpha models. The strategies you outlined, such as cross-validation, regularization, feature selection, and ensemble methods, are all crucial in ensuring that alpha models generalize well to unseen data. I particularly appreciate the emphasis on time-series cross-validation, which is especially relevant in financial modeling. Additionally, your explanation of using simpler models before moving on to more complex ones, and the importance of avoiding over-tuning hyperparameters, is highly practical. These tips will definitely help in creating more robust and reliable models. Your advice on integrating domain knowledge to complement machine learning models also stands out as an essential factor in developing effective alpha strategies.

How do you recommend balancing the use of alternative data, like sentiment analysis, with traditional financial metrics to avoid overfitting?

---

### 评论 #18 (作者: SP39437, 时间: 1年前)

The article provides a thorough guide to mitigating overfitting in alpha models, covering key techniques like cross-validation, regularization, and ensemble methods. It successfully balances theory with practical application, making it useful for both quantitative finance professionals and machine learning practitioners. However, a deeper discussion on the impact of regime shifts in financial markets on model robustness would further enhance its relevance to real-world scenarios. The strategies for avoiding overfitting underscore the importance of balancing model complexity with generalization. While regularization and cross-validation are essential, the role of domain knowledge in feature selection is also critical. I completely agree with your approach to preventing overfitting. Techniques like regularization, cross-validation, and out-of-sample testing are key to ensuring models perform well on unseen data, avoiding the pitfalls of overfitting. How do you incorporate market regime shifts when designing models to ensure they remain robust in different market conditions?

---

### 评论 #19 (作者: HD25387, 时间: 1年前)

Overfitting is a major challenge in developing  **robust alpha models** , as it can lead to poor generalization in real-world trading. Using  **cross-validation techniques** , such as  **time-series validation** , helps ensure models are not overly reliant on historical patterns.  **Feature selection and regularization**  reduce noise by eliminating irrelevant variables and penalizing complexity. Keeping models  **simpler** , leveraging  **ensemble methods** , and conducting  **out-of-sample testing**  further enhance reliability. Have you experimented with  **adaptive model retraining**  to maintain performance across changing market regimes?

---

### 评论 #20 (作者: MA46706, 时间: 1年前)

This article provides an excellent overview of strategies to mitigate overfitting in alpha models! Cross-validation, regularization, and out-of-sample testing are crucial techniques to ensure models generalize well beyond historical data. Additionally, considering regime shifts and changing market conditions is essential for maintaining model robustness. Has anyone experimented with adaptive learning techniques or reinforcement learning to dynamically adjust alpha models based on evolving market conditions?

---

### 评论 #21 (作者: PT27687, 时间: 1年前)

The insights provided on avoiding overfitting in alpha models are quite comprehensive. It's fascinating how various techniques like cross-validation and regularization can significantly enhance model performance. I'm particularly interested in how combining domain knowledge with data-driven methods can lead to better predictive accuracy. Have you found any specific instances where this combination yielded notable results?

---

### 评论 #22 (作者: NP65801, 时间: 1年前)

To avoid overfitting in Alpha models (often referring to machine learning models, particularly in the context of financial forecasting or quantitative analysis).

---

### 评论 #23 (作者: MR74538, 时间: 1年前)

To handle regime shifts, I incorporate rolling window validation, regime detection algorithms, and adaptive weighting methods. These techniques help maintain model robustness, ensuring adaptability to evolving financial market conditions.

---

### 评论 #24 (作者: TP19085, 时间: 1年前)

The discussion effectively covers essential strategies to prevent overfitting in alpha models, including cross-validation, regularization, and ensemble methods. It strikes a solid balance between theoretical foundations and practical applications, making it relevant for both quantitative finance and machine learning practitioners. However, addressing market regime shifts—sudden structural changes in financial markets—could further enhance model robustness.

While regularization and cross-validation ensure generalization, integrating domain expertise in feature selection is equally vital. Adaptive models, such as reinforcement learning or Bayesian methods, might help adjust to evolving market conditions. Additionally, stress testing across different market phases can validate a model’s resilience.

How do you incorporate market regime shifts into your modeling framework? Have you found specific indicators effective in detecting such transitions in real time?

---

### 评论 #25 (作者: HD25387, 时间: 1年前)

Avoiding  **overfitting in alpha models**  requires a balance between  **model complexity and generalization** . Using  **time-series cross-validation**  ensures robustness, while  **regularization techniques (L1/L2)**  help control complexity.  **Feature selection and dimensionality reduction**  improve signal relevance, and  **out-of-sample testing**  ensures real-world viability. Combining  **simpler models with ensemble methods**  reduces noise, while  **limiting hyperparameter tuning**  prevents excessive curve fitting. Have you explored  **adaptive weighting strategies**  to maintain performance across different market regimes?

---

### 评论 #26 (作者: TP19085, 时间: 1年前)

The article offers a comprehensive guide to mitigating overfitting in alpha models, highlighting key techniques such as cross-validation, regularization, and ensemble methods. It balances theoretical insights with practical applications, making it valuable for both quantitative finance and machine learning practitioners. However, a deeper exploration of market regime shifts—sudden structural changes in financial markets—would further enhance model robustness in real-world scenarios. While techniques like regularization and cross-validation improve generalization, incorporating domain knowledge in feature selection is equally crucial. Additionally, adaptive models like reinforcement learning or Bayesian methods, combined with stress testing across various market phases, can strengthen resilience. How do you integrate regime shifts into your modeling framework to maintain robustness across changing market conditions?

---

### 评论 #27 (作者: NN89351, 时间: 1年前)

I fully align with your approach to mitigating overfitting in alpha models. Techniques like regularization, cross-validation, and out-of-sample testing play a crucial role in ensuring models remain effective beyond historical data.  Considering the constantly shifting landscape of financial markets, how do you adapt your models to detect and respond to regime changes?

---

### 评论 #28 (作者: SD92473, 时间: 1年前)

This post provides an excellent roadmap for avoiding the pitfalls of overfitting in alpha models. I particularly value the emphasis on time-series cross-validation, which is often overlooked but critical in financial modeling. The structured approach to feature selection and dimensionality reduction offers practical guidance that can be immediately implemented. The section on ensemble methods effectively highlights how combining multiple models can create more robust predictions than any single model approach. The reminder to incorporate domain knowledge alongside data-driven techniques is especially important - quantitative finance is ultimately about real-world economic relationships, not just statistical patterns. This comprehensive guide strikes a perfect balance between technical depth and practical application, making it valuable for both beginners and experienced quants looking to build more resilient alpha models.

---

### 评论 #29 (作者: LN92324, 时间: 1年前)

Hi. A quick way I think you can try is to change the universe or neutralization in Settings to see if the alpha results fluctuate much. If the results fluctuate a lot, it's likely that your alpha has been overfitted according to that universe and neutralization. In addition, constantly testing new ideas will also help diversify the list of alphas you submit and can help you accurately evaluate the os performance after each system update.

---

### 评论 #30 (作者: TP19085, 时间: 1年前)

This discussion presents a solid framework for mitigating overfitting in alpha models, combining cross-validation, regularization, and ensemble methods—balancing theory and practical application for both quant finance and machine learning practitioners. While these techniques improve generalization, enhancing model robustness against market regime shifts—sudden structural changes—remains critical for real-world performance.

Integrating domain knowledge into feature selection is equally vital, helping avoid reliance on spurious patterns. Adaptive models like reinforcement learning or Bayesian approaches, paired with stress testing across market phases, further strengthen resilience.

A deeper exploration of regime detection—using indicators like volatility spikes, macroeconomic triggers, or structural break tests—could improve adaptability. Have you tested specific methods for identifying regime shifts in real-time? Balancing adaptability and stability is key to building robust alphas that perform consistently across changing market conditions. Curious to hear how others approach this challenge!

---

### 评论 #31 (作者: DK20528, 时间: 1年前)

When using  **ensemble methods**  like boosting, do you find that early stopping alone is sufficient to prevent overfitting, or do you also apply dropout techniques or additional noise injection methods?

---

### 评论 #32 (作者: KS69567, 时间: 1年前)

To build robust alpha models that generalize effectively, it's crucial to balance model complexity and data fitting. Techniques like cross-validation (K-fold or time-series) assess performance on unseen data, while regularization methods (L1 or L2) prevent overfitting by penalizing excessive complexity. Starting with simpler models and gradually increasing complexity helps maintain interpretability. Ensemble methods reduce variance, while out-of-sample testing ensures real-world reliability. Avoid excessive fine-tuning to minimize the risk of overfitting. By combining these approaches, you can create resilient alpha models that adapt well to future market conditions, maintaining accuracy and stability in volatile environments.

---

### 评论 #33 (作者: AR10676, 时间: 1年前)

Overfitting is a significant challenge when developing alpha factors in quantitative finance, but using the right tools and methodologies can help mitigate its impact. By implementing right strategies, you can enhance the generalization ability of your alpha factors and improve their performance in live trading scenarios.

---

### 评论 #34 (作者: RB90992, 时间: 1年前)

To avoid overfitting in alphas, use simpler models with regularization, perform cross-validation or walk-forward validation, and focus on economic intuition when selecting features. Avoid excessive hyperparameter tuning and test models on out-of-sample data. Regularization techniques like Ridge or Lasso help control complexity, while ensemble methods like bagging or boosting can improve robustness. Always assess model performance on data from different periods to ensure generalization and prevent overfitting to historical noise or specific market conditions.

---

### 评论 #35 (作者: KG26767, 时间: 1年前)

To avoid overfitting in alpha models, it’s essential to balance model complexity with the ability to generalize to new, unseen data. By implementing strategies such as out-of-sample testing, regularization, cross-validation, model simplification, and using robust metrics, you can create more reliable, generalizable models that are less likely to be overfit.

---

### 评论 #36 (作者: HH85779, 时间: 1年前)

This is a thorough and well-structured guide on preventing overfitting in alpha models — a must-read for anyone working in quantitative finance. Each strategy you’ve laid out is both practical and deeply relevant to real-world modeling, especially in data-rich but noisy environments like financial markets.

Thanks for this high-quality breakdown — it’s not only educational but also a great checklist to revisit throughout the model development lifecycle.

---

### 评论 #37 (作者: MA97359, 时间: 1年前)

Avoid overfitting in alpha models with cross-validation, feature selection, regularization, more data, simpler models, early stopping, ensembles, out-of-sample testing, and careful hyperparameter tuning.

---

### 评论 #38 (作者: DK30003, 时间: 1年前)

The strategies discussed—regularization, cross-validation, and out-of-sample testing—are crucial for building models that generalize effectively beyond historical data.

---

### 评论 #39 (作者: NT84064, 时间: 1年前)

This is a comprehensive and well-structured overview of overfitting in alpha models. One additional consideration is the role of stationarity in financial time series data. Many models overfit because they fail to account for non-stationarity—where the statistical properties of the data change over time. Methods like differencing, log transformations, and rolling-window analysis can help improve generalization. Additionally, integrating regime-switching models (e.g., Markov regime-switching) allows models to adapt to changing market conditions rather than fitting to a single market regime. Have you explored using Bayesian inference or probabilistic programming for more robust alpha discovery?

---

### 评论 #40 (作者: MM73790, 时间: 11个月前)

This is a great and detailed way of avoiding overfitting.

---

