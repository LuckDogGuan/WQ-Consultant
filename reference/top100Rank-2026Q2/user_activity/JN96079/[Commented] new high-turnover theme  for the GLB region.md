# new high-turnover theme  for the GLB region,

- **链接**: [Commented] new high-turnover theme  for the GLB region.md
- **作者**: RS19747
- **发布时间/热度**: 11个月前, 得票: 8

## 帖子正文

I  new high-turnover theme is started for the GLB region, and I’m still quite new to working in this universe. To prepare, I’d really appreciate some guidance from the community.  Are there any datasets you’ve found that tend to produce naturally high-turnover signals? Any specific fields or dataset types that are worth exploring for this theme would be super helpful.

---

## 讨论与评论 (15)

### 评论 #1 (作者: PN39025, 时间: 11个月前)

Hello, for high revenue, the dataset always meets the need, which is price volume, it will bring high sharpe and tuning to satisfy the theme.

---

### 评论 #2 (作者: NT63388, 时间: 11个月前)

In a recent webinar, I and several other consultants also had a Q&A session about this question.
The webinar host suggested working based on the PV or News categories.
Logically, these two categories have a daily or weekly frequency of providing information, which helps enable high trading frequency and thus leads to high turnover, aligning with the Theme topic.
However, it is necessary to manage this carefully because high turnover can result in high after-costs, which may significantly reduce your Combined score.

---

### 评论 #3 (作者: JN96079, 时间: 11个月前)

While one can generate high turnover alphas to meet the new theme, the key is to maintain a better range of turnover, which in my case I believe between 40 and 55 is better. Otherwise, you can control the turnover using decay settings, while most of analyst and price volume category datasets give high turonver, but still robust signals.

---

### 评论 #4 (作者: IK32530, 时间: 11个月前)

Among the price and volume datasets, I recommend using pv37 because it’s the easiest to create basic signals with.

---

### 评论 #5 (作者: AY28568, 时间: 11个月前)

Thanks for posting this, I’m also trying to learn more about the new high-turnover theme in the GLB region. From what I’ve seen, fields like price-volume, short-term volatility, and intraday returns can help create high-turnover signals. Some people also use news sentiment or very short-term data for quick signals. Using fast changing operators can be useful too. If anyone has tried some good field or operator combinations for this type of alpha in GLB, please share It would be great if we all learn and grow together

---

### 评论 #6 (作者: DJ40095, 时间: 11个月前)

One area I’ve been looking into for high-turnover ideas is short-horizon signals derived from analyst revisions or sentiment shifts, especially from fast-updating datasets like models or options. They tend to react quickly to market events and can naturally drive more frequent rebalancing. Might also be worth exploring alternative data sets that update daily—like certain technical indicators or model momentum fields—as they can help maintain high activity without being overly noisy. Curious to hear if others have had luck combining these with PV signals.

---

### 评论 #7 (作者: DP14281, 时间: 11个月前)

Generally Risk, Price Volume, News are the data categories which tends to higher turnover and good Alphas PnL, you can try these in this theme.

---

### 评论 #8 (作者: PS61132, 时间: 11个月前)

Price-volume, risk and sentiment datasets are reliable for high turnover and typically produce strong Sharpe ratios when properly tuned to the theme

---

### 评论 #9 (作者: LR13671, 时间: 10个月前)

A good turnover range to aim for is  **40–60%** , balancing frequency with after-cost considerations. Over-optimization for turnover can lead to degraded OS performance, so be sure to validate your signals across multiple universes (e.g., GLB, USA).

---

### 评论 #10 (作者: TP19085, 时间: 10个月前)

Lately, I’ve been exploring short-term signals for high-turnover strategies, especially those based on analyst revisions or sentiment changes from quickly updating sources like models or options data. These tend to respond rapidly to market events, naturally encouraging more frequent rebalancing. It might also be helpful to consider alternative daily-updating datasets, such as technical indicators or model momentum fields, which can support active trading without excessive noise. I’m curious if others have successfully combined these with price-volume (PV) signals.

Thanks for sharing this—I'm also learning about high-turnover themes in the GLB region. Fields like price-volume, short-term volatility, and intraday returns appear useful, along with news sentiment and fast-changing data for quick signals. Fast operators add value too. If anyone has good field or operator combos for GLB high-turnover alphas, please share. In a recent webinar, consultants recommended focusing on PV or News categories since their daily or weekly updates enable higher trading frequency. But caution is needed—high turnover can increase costs and reduce overall scores.

---

### 评论 #11 (作者: ML46209, 时间: 10个月前)

For GLB high-turnover alphas, try Price-Volume, News, and short-term momentum fields. Aim for 40–60% turnover, use fast operators, and combine datasets for robust signals.

---

### 评论 #12 (作者: NT84064, 时间: 10个月前)

For the GLB region, building high-turnover signals requires focusing on datasets that capture rapid, short-lived market dynamics. In my experience, intraday or high-frequency derived features—such as short-term volatility spikes, bid-ask spread changes, and order book imbalances—can naturally yield higher turnover alphas. Price-driven datasets with minimal smoothing, like 1–5 day returns or rolling z-scores of volume, also tend to refresh quickly, which supports a higher trading frequency. Additionally, event-based datasets (earnings releases, analyst rating changes, or corporate news sentiment) can create bursts of activity that decay rapidly, pushing turnover higher. Since GLB aggregates multiple regions, ensure that your data is properly synchronized across markets, adjusting for different time zones and trading calendars. Finally, consider that high-turnover themes often come with increased transaction cost impact, so it’s important to backtest net performance with realistic slippage assumptions—especially in less liquid universes within GLB.

---

### 评论 #13 (作者: HH63454, 时间: 10个月前)

For GLB high-turnover themes, short-horizon datasets like price-volume, intraday volatility, and event-driven sentiment tend to work best. Consider using fast-changing operators to keep turnover elevated while targeting the 40–60% range to control costs. Synchronizing data across different markets in GLB is also key for consistent performance.

---

### 评论 #14 (作者: NS62681, 时间: 10个月前)

For GLB high-turnover themes, short-horizon datasets such as price-volume, intraday volatility, and event-driven sentiment often deliver the best results. Using fast-reacting operators can help maintain high turnover while aiming for the 40–60% range to manage costs. It’s also important to synchronize data across GLB markets to ensure stable and consistent performance.

---

### 评论 #15 (作者: LB76673, 时间: 10个月前)

In the GLB region, high-turnover signals usually emerge from datasets that capture fast-changing dynamics rather than slow-moving fundamentals. Market microstructure fields like intraday volume, bid-ask spreads, and short interest shifts often create naturally high-turnover behavior, as do sentiment or analyst estimate revisions since they react quickly to news flow. Some consultants also explore cap- or liquidity-related datasets, which refresh frequently and can amplify short-term ranking changes. My advice is to start by testing microstructure and sentiment-related datasets first, because they tend to align best with the high-turnover theme, and then validate stability with neutralization so the speed doesn’t just reflect noise.

---

