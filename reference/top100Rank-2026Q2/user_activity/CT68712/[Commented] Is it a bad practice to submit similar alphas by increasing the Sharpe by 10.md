# Is it a bad practice to submit similar alphas by increasing the Sharpe by 10% ?

- **链接**: [Commented] Is it a bad practice to submit similar alphas by increasing the Sharpe by 10.md
- **作者**: SK26283
- **发布时间/热度**: 1年前, 得票: 3

## 帖子正文

Does it cause any negative effect on the value factor as it increases both self and production correlation?

---

## 讨论与评论 (28)

### 评论 #1 (作者: PN39025, 时间: 1年前)

Hi , It is not a bad habit to increase Sharpe by 10% since you are refining the alpha. However, the value factor depends on multiple factors. Regions cannot be directly correlated with the value factor, as it is based on the OS performance of your most recently submitted alphas during the applicable calendar quarter. To improve your chances of achieving a high value factor, consider diversifying regions and incorporating different datasets

---

### 评论 #2 (作者: NT63388, 时间: 1年前)

Personally, I think it's correct.

Increasing the Sharpe by 10% just to cross the threshold, only so you can submit the Alpha. If it's a truly novel idea, then you could do that once or twice.

I'm afraid you're just trying to increase the Sharpe enough to submit, and that it's happening repeatedly.

This will have a negative impact on the diversity of your Alphas, not just simply increasing correlation.

Focus on finding strong Alphas to achieve a high VF (Validation Factor), and diversify to prevent the VF from decreasing.

---

### 评论 #3 (作者: SM58724, 时间: 1年前)

Hi  [SK26283](/hc/en-us/profiles/26394131301271-SK26283) , Increasing Sharpe by 10% to cross the threshold isn’t necessarily bad, but repeatedly doing so may harm the diversity of your Alphas. While refining Alphas is good, the value factor depends on multiple factors, including OS performance. Instead of just boosting Sharpe, focus on finding strong, diverse Alphas across regions and datasets to improve VF and avoid negative effects from high correlation.

---

### 评论 #4 (作者: PP87148, 时间: 1年前)

Hi,

You should calculate the correlation between these two alphas as well and then if these are not much correlated < 60%. Then you can submit the alpha, else you should avoid this.

---

### 评论 #5 (作者: DL53864, 时间: 1年前)

I think this could negatively impact your combined alpha performance. Typically, if the alpha pool is diverse, the combination can yield higher performance compared to combining alphas with high correlation to each other.

---

### 评论 #6 (作者: deleted user, 时间: 1年前)

- **R** : Especially useful for statistical analysis and handling time-series data. Packages like  **xts** ,  **quantmod** , and  **TTR**  are powerful tools in financial data analysis.
- **SQL** : Since financial data is often stored in databases, understanding SQL is crucial for querying and extracting data efficiently.

###

---

### 评论 #7 (作者: PL15523, 时间: 1年前)

By focusing on the  **TOP200** , you're limiting your opportunities to the most well-established and frequently traded stocks. The  **alpha potential**  might be lower compared to the broader universe, especially for  **small-cap**  stocks, which tend to have higher growth potential.

---

### 评论 #8 (作者: CT68712, 时间: 1年前)

It’s interesting to see the discussions around Sharpe ratios and alpha submissions! As someone venturing into quant trading, I understand how tempting it might be to tweak that Sharpe value just to meet submission thresholds. But I agree with NT63388—if you repeatedly adjust just to hit a number, you could be risking the diversity of your strategies. Diversifying alphas and focusing on unique ideas should be the priority. Strengthening the underlying algorithms is crucial for long-term success. Keep pushing those boundaries, everyone!

---

### 评论 #9 (作者: SK72105, 时间: 1年前)

[SK26283](/hc/en-us/profiles/26394131301271-SK26283)  Hello! I think it is better to submit alphas with lower correlation using different datafields, and operators. This will not only help you achieve a better combined alpha performance but is also likely to improve your Value Factor, and help in Genius level tie-breaker. Also, if you keep submitting the same alpha it will concentrate the risk factors of your combined performance and this will increase the chances of a sharp drawdown in the OS period. So in my opinion, it is not a good practice.

---

### 评论 #10 (作者: NH16784, 时间: 1年前)

[SK26283](/hc/en-us/profiles/26394131301271-SK26283)  hi, you should not submit alphas with self corr > 0.7 because i did that in the past, and the value factor was around 0.3, after i changed it, my vf is now 0.98

---

### 评论 #11 (作者: CT68712, 时间: 1年前)

Hi everyone! As a tech enthusiast diving into quant trading, I find the discussions on Sharpe ratios and alpha submissions fascinating. I totally get the urge to push that Sharpe value up by 10%, but NT63388 makes a good point about the risk of losing diversity in your alphas. It’s all about balance! Don’t just chase the numbers—finding distinct and strong alphas across various datasets is key. The real success comes from innovative strategies rather than merely tweaking the stats to fit submission requirements. Let’s keep our alphas diverse and aim for long-term growth! Keep up the great work!

---

### 评论 #12 (作者: deleted user, 时间: 1年前)

: If your strategy is volatile, consider methods to reduce volatility while maintaining returns. This can include smoothing out the returns or adjusting for outlier events (such as market crashes) that cause large drawdowns.

---

### 评论 #13 (作者: RP41479, 时间: 1年前)

Sharpe ratio tweaks can be tempting, but over-adjusting risks strategy diversity. I agree with NT63388—focus on unique alphas and strong algorithms for long-term success. Keep innovating!

---

### 评论 #14 (作者: MA97359, 时间: 1年前)

Hi  [SK26283](/hc/en-us/profiles/26394131301271-SK26283) , Here's my take on your question,
 Submitting correlated alphas can be beneficial if you are confident in their strong out-of-sample (OS) performance potential. However, submitting multiple alphas with similar construction without real OS strength can increase mean self-correlation and production correlation, potentially hurting overall performance. To avoid this, ensure that any correlated alphas you submit have been rigorously tested and demonstrate genuine robustness before submission.

---

### 评论 #15 (作者: TD84322, 时间: 1年前)

I think it's correct. Raising Sharpe by 10% just to submit is fine for a novel idea once or twice, but doing it repeatedly hurts diversity. Focus on strong Alphas and diversify to keep VF high.

---

### 评论 #16 (作者: QN91570, 时间: 1年前)

It’s interesting to see the discussions around Sharpe ratios and alpha submissions! As someone venturing into quant trading, I understand how tempting it might be to tweak that Sharpe value just to meet submission thresholds.

---

### 评论 #17 (作者: PP87148, 时间: 1年前)

Submitting similar alphas occasionally isn’t inherently bad, but consistently doing so may dilute the overall value of your portfolio. Instead, prioritize innovation and diversity to maximize your contributions.

---

### 评论 #18 (作者: NP85445, 时间: 1年前)

It's okay to tweak your alpha once in a while to cross the Sharpe threshold, but doing it repeatedly with similar strategies can hurt diversity. Over-adjustment may increase correlation among your alphas, diluting the overall value factor. Focus on developing genuinely novel ideas to maintain a robust, diversified portfolio.

---

### 评论 #19 (作者: DK30003, 时间: 1年前)

I think this could negatively impact your combined alpha performance. Typically, if the alpha pool is diverse, the combination can yield higher performance compared to combining alphas with high correlation to each other

---

### 评论 #20 (作者: TN48752, 时间: 1年前)

**Actionable Insight** : Combining these three variables will give a clear picture of how much the company has exceeded expectations and how robust the financial performance is. Positive surprises backed by strong earnings and revenue growth could signal a higher chance of continued momentum.

---

### 评论 #21 (作者: QG16026, 时间: 1年前)

Hi, i wondering what strategies can be implemented to boost the Sharpe ratio without compromising the diversity of your alphas, and how can diversification across different regions and datasets help maintain a robust value factor while minimizing high correlation risks?

---

### 评论 #22 (作者: RB98150, 时间: 1年前)

Increasing the correlation between self and production of alphas could lead to less diversification, which may reduce the  effectiveness in generating alpha. When correlations rise, the alpha may become more sensitive to market movements or specific sector performance, potentially diminishing its ability to capture undervalued opportunities. This may result in increased risk and reduced returns, Balancing correlation is key for maintaining effectiveness.

---

### 评论 #23 (作者: NS62681, 时间: 1年前)

Increasing the Sharpe ratio by 10% is a reasonable approach to refining an alpha. However, the value factor is influenced by multiple elements. Regions do not have a direct correlation with the value factor, as it is determined by the out-of-sample performance of your most recently submitted alphas during the applicable calendar quarter.

---

### 评论 #24 (作者: PT27687, 时间: 1年前)

Your question touches on an interesting aspect of model development. Enhancing the Sharpe ratio by a small percentage may seem beneficial at first, but, as you mentioned, it could lead to increased correlation and potentially self-similarity among alphas. This might result in overfitting in certain scenarios. How do you plan to balance this trade-off while aiming for robustness in your models?

---

### 评论 #25 (作者: VN28696, 时间: 1年前)

It’s not necessarily a bad practice, but it comes with risks.

If your new alpha is too similar to an existing one, it will likely have  **high self and production correlation** , which can  **reduce its value factor** . A small Sharpe increase (like 10%) might not justify submitting a near-duplicate, especially if it doesn’t generalize well out of sample.

Instead of minor tweaks, try  **improving the core logic**  or  **diversifying the approach**  to make the alpha more robust and unique.

---

### 评论 #26 (作者: NA18223, 时间: 1年前)

As someone venturing into quant trading, I understand how tempting it might be to tweak that Sharpe value just to meet submission thresholds. But I agree with NT63388—if you repeatedly adjust just to hit a number, you could be risking the diversity of your strategies.

---

### 评论 #27 (作者: LN92324, 时间: 1年前)

Hi. Because the system only allows submitting a maximum of 4 regular alphas per day, you can select the best alphas of that day to submit. In my opinion, you should not submit alphas that are too similar to each other because it will affect the correlation criterion - an important criterion to evaluate the quality of your alphas. Because there are only a maximum of 4 regular alphas, you should choose alphas with low correlations, then optimize their performance.

---

### 评论 #28 (作者: DK30003, 时间: 1年前)

Consider methods to reduce volatility while maintaining returns. This can include smoothing out the returns or adjusting for outlier events (such as market crashes) that cause large drawdowns.

---

