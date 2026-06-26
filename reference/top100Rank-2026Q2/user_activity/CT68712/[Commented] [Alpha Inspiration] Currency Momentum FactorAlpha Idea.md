# [Alpha Inspiration] Currency Momentum FactorAlpha Idea

- **链接**: [Commented] [Alpha Inspiration] Currency Momentum FactorAlpha Idea.md
- **作者**: NH84459
- **发布时间/热度**: 2年前, 得票: 23

## 帖子正文

**Paper:**  db Currency Returns

**Author:**  Deutsche Bank

**Link** :  [http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf](http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf)

Initially discovered in equity markets, momentum strategy is a well-known, well-researched, and, most importantly, a robust anomaly. Moreover, it has been documented in various asset classes across the world and by many academics and is considered as a powerful anomaly. Momentum is a  [trend-following strategy](https://quantpedia.com/strategies/asset-class-trend-following/) , where the strategy buys the assets which have performed well in the past and sells the assets which have performed bad. No surprise, the momentum anomaly is present also in the currencies. In the currency market, momentum is a widely observed feature that many exchange rates trend on a multi-year basis. Therefore, a strategy that follows the trend typically makes positive returns over time.
The financial literature about the anomaly is consistent, and the academics agree that the momentum anomaly has its place in the FX market, for example, Menkhoff, Sarno, Schmeling, and Schrimpf in the  [Currency Momentum Strategies](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1809776) , tested the momentum strategy during the period from 1976 to 2010, with an investment universe consisting of more than 40 currencies. They have found a large and significant cross-sectional spread in excess returns of up to 10% p.a. between a past winner and past loser currencies, i.e., currencies with recent high returns continue to outperform currencies with recent low returns by a significant margin.
Interestingly, Grobys and Heinonen have even found that there is a robust link between the returns of the momentum anomaly implemented in currency markets and global economic risk, measured by the currency return dispersion (RD). They have found that the spread of the zero-cost momentum strategy is significantly larger in high RD states (worldwide crisis state) compared to low RD states.

**Main ideas:** 
The primary reason why does the momentum anomaly work is simple; academics explain this anomaly by the irrationality of investors. More precisely, their underreaction to the new information, failing to incorporate news in the prices. Menkhoff, Sarno, Schmeling, and Schrimpf add: “Moreover, currency momentum is mostly driven by return continuation in spot rates (and not interest rate differentials) and has very different properties from the widely studied  [carry trade](https://quantpedia.com/strategies/fx-carry-trade/) .”
Another possible explanation is that momentum investors are exploiting behavioral shortcomings in other investors, such as investor herding, investor over- and under-reaction, and confirmation bias. Concentrating on the FX momentum, the segmentation of the currency market where some participants act quickly on the news while others respond more slowly is one reason why trends emerge and can be protracted. Additionally, Bae and Elkamhi in “ [Global Equity Correlation in Carry and Momentum Trades](https://www-2.rotman.utoronto.ca/facbios/file/Global%20Equity%20Correlation%20in%20Carry%20and%20Momentum%20Trades%20(Bae%20and%20Elkamhi).pdf) ” have provided a risk-based explanation for the excess returns of two widely-known currency speculation strategies: carry and momentum trades. They have constructed a global equity correlation factor and showed that it explains the variation in average excess returns of both these strategies, where the global correlation factor has a robust negative price of beta risk in the FX market. Moreover, Filippou, Gozluklu, and Taylor have shown that the global political environment affects all currencies and investors following  [momentum strategies](https://quantpedia.com/screener/?FilterKeywords=momentum)  are compensated for the exposure to the global political risk of those currencies they hold, i.e., the past winners, while past losers provide a natural hedge.

**Alpha implementation:** 
Go long three currencies with the highest 12-month momentum against USD and go short three currencies with the lowest 12-month momentum against USD. Cash not used as margin invest on overnight rates. Rebalance monthly.

![图片](images/img_998338ae32.png)

![图片](images/img_6514283864.png)

It can be seen that the long - short count ratio is unbalanced. Is there any way to balance long and short while still maintaining the signal? Besides, the indexes decreased in 2017 and 2020. I am still thinking about ways to improve. Looking forward to everyone discussing. Thank you.

---

## 讨论与评论 (12)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hi!

First of all, great job on the work you've put into understanding and implementing the currency momentum in alpha.

As for balancing long and short count - if your alpha is passing the weight concentration test, then the unbalanced count may not pose a problem.

However, if there's a weight test failure, please refer to the  [Weight Coverage common issues and advice](/hc/en-us/articles/19248385997719-Weight-Coverage-common-issues-and-advice)  - Alpha magnitude distribution. for guidance. Have you considered implementing the rank() function on your alpha? This could potentially help in addressing your concern. Keep experimenting, learning, and improving 😃

---

### 评论 #2 (作者: NH84459, 时间: 2年前)

Hi.

I 've tried nesting cross sectional functions like rank or quantile, but the signal was clearly degraded, alpha could not be submitted, even though long count and short were balanced after using those functions.

---

### 评论 #3 (作者: AG20578, 时间: 2年前)

Understood, additional information about alpha implementation would certainly be beneficial. It would be greatly helpful if you could share which data fields you've used.

Looking at the statistics, I'm guessing your alpha does not include neutralization in its settings; correct me if I'm wrong. If that's the case, certain operations like rank might deviate from your initial idea of "Go long three currencies with the highest 12-month momentum against USD and go short three currencies with the lowest 12-month momentum against USD."

One suggestion I have for you is to use the inst_pnl() operator to identify which stocks align well with your idea and which do not. You could use the underperforming stocks as a "hedge" by assigning them a negative weight, regardless of the signal direction. My suspicion is that there may be some stocks in the Long count that don't contribute positively to your idea, adding only noise. Therefore, by assigning a negative weight to these stocks, you could maintain balance in the long-short configuration without losing the signal. Here's an example of how you could implement this:

```
rank(ts_ir(inst_pnl(scale(alpha)), n_days)) < 0.5 ? alpha : -1
```

Let me know the result 😊

---

### 评论 #4 (作者: XD81759, 时间: 1年前)

Hey NH84459, I feel your pain with the long-short balance issue. Since rank() didn't work well for you, another option could be using a normalization method like z-score normalization on your momentum values before making the long and short decisions. This might help in keeping the signal intact while achieving a better balance. Also, about the index drops in 2017 and 2020, you could consider adding some risk management factors, like volatility filters, to avoid bad periods. Hope these ideas work for you.

---

### 评论 #5 (作者: CC40930, 时间: 1年前)

The momentum anomaly in currency markets is a fascinating concept, and the research presented in this paper offers valuable insights into how currency trends can be capitalized on over time. It's especially interesting to see the link between currency momentum and global economic risk, with higher momentum spreads during times of crisis. The idea that irrational investor behavior, such as underreaction to new information or herding, plays a role in driving this anomaly makes sense, and it’s intriguing to think about how this could be used in trading strategies. Thanks for sharing this paper; it provides great context for understanding how momentum strategies can be effectively applied in the FX market.

---

### 评论 #6 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #7 (作者: PL15523, 时间: 1年前)

The momentum anomaly in financial markets, particularly in foreign exchange (FX), is widely believed to be driven by investor behavior, specifically their irrational reactions to new information. Academics argue that investors often underreact to news, failing to incorporate relevant information into asset prices quickly, which allows for momentum trends to persist.

The research of Menkhoff, Sarno, Schmeling, and Schrimpf emphasizes that currency momentum is driven by the continuation of returns in spot rates rather than by interest rate differentials, differentiating it from the carry trade strategy. This finding suggests that momentum in FX markets is distinct from other commonly studied trading strategies, such as the carry trade, which focuses on interest rate differentials.

---

### 评论 #8 (作者: KS69567, 时间: 1年前)

Currency markets' momentum anomaly does, in fact, offer a convincing viewpoint on how patterns in currency performance can both reflect and take advantage of underlying market dynamics. The correlation between risk aversion and investor behaviour is shown by the finding that momentum spreads typically increase during times of global economic instability or crises. This correlation underscores the ability of currency momentum techniques to forecast outcomes and their usefulness as instruments for managing unstable economic environments.

### Implementing Currency Momentum Strategies :

1. **Identify Momentum** : Track past performance (3-12 months).
2. **Adjust for Risk** : Factor in global risk indicators (e.g., VIX, credit spreads) during crises.
3. **Time Frame** : Use longer horizons (6-12 months) for more reliable momentum signals. Rebalance monthly or quarterly.
4. **Portfolio Construction** : Diversify across currencies. Adjust position sizes based on momentum strength and market volatility.
5. **Crisis Strategy** : During global crises, momentum trends become more pronounced. Capitalize on market shifts early with event-driven trading.

### Portfolio Management:

- **Diversify** : Add currency momentum to complement equities/bonds and improve returns.
- **Risk Management** : Use stop-loss orders or hedging strategies to protect against sudden reversals.
- **Market Timing** : Track macro indicators for signs of trend shifts and adjust positions accordingly.

In short, momentum strategies capitalize on persistent currency trends, especially during times of economic crisis. Adjust risk and diversify to optimize returns.

---

### 评论 #9 (作者: QG16026, 时间: 1年前)

The momentum anomaly in currency markets shows how trends persist, especially during economic crises, reflecting investor behavior and risk aversion. To implement, track 6-12 months of performance, adjust for global risk, diversify positions, and rebalance regularly.

---

### 评论 #10 (作者: AK98027, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #11 (作者: CC40930, 时间: 1年前)

This is an interesting take on momentum strategies in the FX market, especially regarding the robust link to global economic risk. Balancing the long-short ratio while maintaining the momentum signal could potentially be addressed by adjusting the weighting scheme or exploring other risk management techniques. It's great to see the ongoing discussion on improving strategies for better stability during periods of market volatility. Thanks for sharing!

---

### 评论 #12 (作者: CT68712, 时间: 1年前)

The momentum anomaly in currency markets is super intriguing! As a tech-savvy dude who's dabbled in algorithmic trading, I'm fascinated by how these trends can persist due to investor behavior. The idea that people often underreact to new info makes total sense. I appreciate the insights shared here, particularly about the ties between economic risk and momentum strategies. For us quant folks, utilizing a systematic approach to identify these patterns could enhance our portfolios significantly. I’d love to discuss more on how techniques like z-score normalization might help maintain signal strength while balancing longs and shorts. Let's keep exploring the world of FX together!

---

