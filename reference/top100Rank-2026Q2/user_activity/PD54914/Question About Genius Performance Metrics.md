# Question About Genius Performance Metrics

- **链接**: Question About Genius Performance Metrics.md
- **作者**: PD54914
- **发布时间/热度**: 7个月前, 得票: 3

## 帖子正文

I’m trying to better understand the performance metrics shown in Genius, specifically:Combined Alpha PerformanceCombined Selected Alpha PerformanceCombined Power Pool Alpha PerformanceWhat exactly do these metrics represent, how are they calculated, and what steps can help improve them?Thanks in advance!

---

## 讨论与评论 (3)

### 评论 #1 (作者: TP85668, 时间: 7个月前)

Here’s a simple breakdown of the three Genius performance metrics:1. Combined Alpha PerformanceThis is thecombined out-of-sample performance of all alphas you’ve submitted. Every alpha you publish contributes—good or bad—so consistently submitting strong, stable signals helps improve this score.2. Combined Selected Alpha PerformanceThis reflects theout-of-sample performance of only the alphas that WQ selectsfrom your submissions. Since selection is based on quality, stability, and uniqueness, this metric tells you how well yourbestideas (as validated by WQ) perform.3. Combined Power Pool Alpha PerformanceThis measures theout-of-sample performance of the Power Pool alphas you’ve submitted. Because Power Pool has stricter filters, this score often highlights your most robust signals.How to improve them:Build alphas withlow correlationto each other and to existing signals.Focus onrobustness(works across delays, universes, and time periods).Reduceoverfittingby using simple, clean logic.Improveselection chancesby submitting fewer but higher-quality alphas.Aim forstable OS performancerather than high IS spikes.

---

### 评论 #2 (作者: AY28568, 时间: 6个月前)

These Genius performance metrics can seem confusing, but they are very helpful once you understand them.Combined Alpha Performanceshows how all your Alphas are doing together.Combined Selected Alpha Performanceshows the performance of only those Alphas chosen by WQ.Combined Power Pool Alpha Performancecompares your signals with the Power Pool. To improve these metrics, try creating stable Alphas with good Robust Sharpe, low turnover, and consistent performance over longer periods. Hope this gives some clarity!

---

### 评论 #3 (作者: NT84064, 时间: 5个月前)

This is an important question because the Genius performance metrics are designed to measureportfolio-level contributionrather than individual alpha quality. Combined Alpha Performance reflects the out-of-sample behavior of all alphas you’ve submitted, aggregated in a normalized way so that no single high-volatility signal dominates. Combined Selected Alpha Performance narrows this to only those alphas chosen by WorldQuant, effectively adding an additional quality and robustness filter on top of raw submission. Combined Power Pool Alpha Performance focuses on alphas optimized for low correlation and synergy, which is why improving this metric often depends more on diversification discipline than on maximizing Sharpe. To improve these metrics, focusing on recent OS stability, reducing correlation across datasets and operator families, and pruning decayed signals is usually more effective than increasing submission volume. Thinking in terms of marginal contribution and long-term durability aligns closely with how these metrics behave.

---

