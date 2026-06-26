# 3 simple ways to improve after cost performance

- **链接**: 3 simple ways to improve after cost performance.md
- **作者**: AM60509
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

3 ways to improve after cost performance are:-

1.Reduce turnover.

Lesser is the turnover ,better is the after cost performance

Ideal turnover should be less than 15% expect for news datasets for which turnover around 25% is fine

2.Improve Sub Universe Sharpe

Better is the sub universe sharpe ,better is the after cost performance

3.Use Investability Constrained Metric

Better and higher is the performance as shown by the investability constrained metric better will be the after cost performance

---

## 讨论与评论 (15)

### 评论 #1 (作者: NL99431, 时间: 1年前)

good

---

### 评论 #2 (作者: NT84064, 时间: 1年前)

Great summary — these three points are spot on! 🔍

To add a bit more detail:

**Reducing turnover**  not only helps with cost but also with stability. Applying  `decay_linear`  and avoiding overly reactive alphas can help control this.

**Improving Sub-Universe Sharpe**  often comes from better feature selection or filtering out noisy signals — I’ve found that combining  `group_neut`  with  `zscore`  improves cross-sectional stability a lot.

**Investability constraints**  are crucial. It helps to track metrics like  `adv20` ,  `market_cap` , or float-adjusted liquidity, and ensure your signal maintains performance on the investable universe.

Thanks for sharing this — a great reminder to balance signal quality  *and*  execution realism!

---

### 评论 #3 (作者: TP85668, 时间: 1年前)

Thanks for sharing! These three methods are clear and practical. Especially, managing turnover and enhancing Sub-universe Sharpe are key aspects that are often overlooked.

---

### 评论 #4 (作者: KS69567, 时间: 1年前)

To enhance after-cost performance, focus on building efficient and realistic models. Keeping  **turnover low**  reduces trading costs, aiming for under  **15%**  (or  **25%**  for news datasets). Maximizing  **Sub-Universe Sharpe**  ensures stronger risk-adjusted returns, and relying on  **Investability-Constrained Metrics**  ensures your strategies are practical and scalable. Together, these three approaches help optimize real-world performance and long-term success.

---

### 评论 #5 (作者: LB76673, 时间: 1年前)

Thank you for sharing these practical and concise strategies for improving after-cost performance. Each of the three points offers clear guidance for optimizing quantitative models in a real-world trading context. Reducing turnover is particularly impactful, as it directly limits transaction costs that can erode returns. I also appreciate the emphasis on sub-universe Sharpe, which provides a more focused measure of strategy robustness within a specific investable set. Lastly, incorporating investability-constrained metrics helps ensure that signals remain realistic and actionable, especially in large-scale deployments. Posts like this are extremely valuable for refining performance metrics in production settings.

---

### 评论 #6 (作者: HT71201, 时间: 1年前)

Thanks for sharing these clear, practical tips for boosting after-cost performance. Reducing turnover is especially key, as it cuts transaction costs. The focus on sub-universe Sharpe and investability-constrained metrics is also spot-on for keeping strategies realistic and scalable. Posts like this are great for refining production-level models.

---

### 评论 #7 (作者: AC63290, 时间: 1年前)

To improve after cost performance, reduce turnover ideally below 15%, or 25% for new datasets. Enhance Sub Universe Sharpe, as a higher Sharpe indicates stronger risk-adjusted returns. Finally, focus on the Investability Constrained Metric—better performance here signals higher real-world investability and contributes to improved after cost outcomes.

---

### 评论 #8 (作者: SK90981, 时间: 1年前)

Focus on reducing turnover, boosting sub-universe Sharpe, and leveraging investability-constrained metrics to significantly enhance after-cost performance.

---

### 评论 #9 (作者: AG14039, 时间: 1年前)

To improve after-cost performance, prioritize creating efficient and realistic models. Maintain low turnover—ideally below 15%, or 25% when using news datasets—to minimize trading expenses. Focus on maximizing Sub-Universe Sharpe for better risk-adjusted returns, and use Investability-Constrained Metrics to ensure your strategies are practical and scalable. Combining these three methods will help optimize performance in real-world conditions and support long-term success.

---

### 评论 #10 (作者: AG14039, 时间: 1年前)

Thanks for sharing these clear and practical tips! Their simplicity makes them easy to remember and implement. I’ve personally noticed how lowering turnover significantly reduces costs and boosts net returns. Emphasizing Sub Universe Sharpe and investability constraints is a great reminder to keep strategies realistic and scalable. Posts like this are incredibly helpful for both beginners and seasoned quants, offering valuable insights to enhance our models. I really appreciate you taking the time to put this together!

---

### 评论 #11 (作者: TP19085, 时间: 1年前)

Thank you for sharing these clear, concise, and highly actionable strategies for improving after-cost performance. Each point serves as a valuable reminder of how to align quantitative models with real-world trading constraints. Reducing turnover is especially impactful—it directly lowers transaction costs and boosts net returns, making it one of the most effective levers for improving alpha efficiency. Emphasizing  **Sub-Universe Sharpe**  adds a practical lens on robustness, helping ensure that strategies hold up within an investable subset rather than just the broader universe. Additionally, incorporating  **investability-constrained metrics**  ensures that alphas are scalable and executable, particularly in large-scale or institutional settings. These tips are easy to remember, yet powerful in guiding both new and seasoned quants toward production-ready models. Posts like this help refine our thinking and bring greater discipline to strategy development. Truly appreciate you taking the time to share this—it’s a great resource for the entire community.

---

### 评论 #12 (作者: TP19085, 时间: 1年前)

Thank you for sharing these clear, concise, and actionable tips for improving after-cost performance. The simplicity of your framework makes it easy to remember, yet each point offers powerful guidance. Reducing turnover has a direct and significant impact on cutting transaction costs and improving net returns—something I’ve experienced firsthand. Emphasizing Sub-Universe Sharpe brings a more practical lens to robustness, helping ensure strategies are effective within an investable subset, not just in theory. The focus on investability constraints is equally important, as it keeps our models realistic, scalable, and ready for institutional deployment. These insights serve as valuable reminders for both new and experienced quants looking to refine their models and align them with real-world execution. Posts like this elevate the quality of our research and reinforce the importance of disciplined strategy development. Truly appreciate you taking the time to share—it’s a great resource for the entire community.

---

### 评论 #13 (作者: PY38056, 时间: 1年前)

Thanks for sharing this which is helpful in making realistic alphas ,realistic alpha thrives on efficiency, not frequency

---

### 评论 #14 (作者: YZ51589, 时间: 6个月前)

Reading this really reinforces something I’ve learned the hard way: most alphas don’t fail because the idea is bad, but because costs quietly eat them alive. Early on, I used to focus almost entirely on Sharpe and headline performance, and only later realized how much turnover and investability matter once you look at net results.

What resonates with me here is how these points all push toward the same mindset — designing alphas that  *behave well* , not just look good. Lower turnover, decent sub-universe Sharpe, and solid investability metrics usually show up together when a signal is truly robust. Whenever one of them is weak, after-cost performance almost always suffers.

It’s a good reminder that real alpha is about efficiency and discipline, not constant trading or complexity.

---

### 评论 #15 (作者: AK36870, 时间: 1个月前)

thanks, was really helpful

---

