# [Alpha Inspiration] Short Interest Effect – Long-Short VersionAlpha Idea

- **链接**: [L2] [Alpha Inspiration] Short Interest Effect  Long-Short VersionAlpha Idea.md
- **作者**: DB74207
- **发布时间/热度**: 2年前, 得票: 18

## 帖子正文

**Paper:** Why Do Short Interest Levels Predict Stock Returns?

**Authors:**  Akbas, Boehmer, Erturk, Sorescu

**Link:**   [https://www.researchgate.net/publication/228171330_Why_Do_Short_Interest_Levels_Predict_Stock_Returns](https://www.researchgate.net/publication/228171330_Why_Do_Short_Interest_Levels_Predict_Stock_Returns)

In the past, academic research has shown that stocks with high levels of short interest are connected with a high probability of experiencing  [negative abnormal returns](https://quantpedia.com/strategies/soccer-clubs-stocks-arbitrage/)  subsequently. Therefore, the common sense implies that it should be possible to gain an advantage of the aforementioned stocks. The theory says that shorting stocks with all the constrain (connected with the shorting) is most often made by the informed investors whose activity ultimately helps prices incorporate more information. Moreover, the level of their holdings has predictive power about returns and fundamentals of the stocks. Knowing the short-interest can lead to a strategy that consists of simply joining informed short-sellers. The long-short variation (our screener also includes [the long-only variant](https://quantpedia.com/strategies/short-interest-effect-long-only-version/) ) of this strategy would be performed by the shorting stocks with high short interest and going long stocks with low short interest.
Overall, the academic world support this anomaly, for example, Asquith, Pathak, and Ritter in their work “ [Short Interest, Institutional Ownership, and Stock Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=525623) “, say that “Stocks are short sale constrained when there is a strong demand to sell short and a limited supply of shares to borrow. Using data on both short interest, a proxy for demand, and institutional ownership, a proxy for supply, we find that constrained stocks underperform during 1988-2002 by a significant 215 basis points per month on an EW basis, although by only an insignificant 39 basis points per month on a VW basis. For the overwhelming majority of stocks, short interest and institutional ownership levels make short-selling constraints unlikely.” Additionally, the authors of this paper state that: “The cross-sectional relation between short interest and future stock returns vanishes when controlling for short-sellers’ information about future fundamental news. Thus, short-sellers contribute, in a significant manner, to price discovery about firm fundamentals.” Last but not least, this long-short strategy has a low correlation to the overall market, and therefore, the strategy can be used as a portfolio diversifier.

**Fundamental reason**

The literature offers two popular explanations for this predictability, namely the overvaluation hypothesis and the information hypothesis. The first possible explanation for the short interest effect – the overvaluation hypothesis stems from the work of Miller (1977). His theory says that stocks with high levels of short interest are overvalued because pessimistic investors are unable to establish short positions, leaving only the optimists to participate in the pricing process. In this model, market forces are unable to prevent overpricing in the amount of shorting costs when these costs are high. The greater the shorting costs, the greater the possible overpricing, and therefore, the lower the subsequent stock returns.
The second and probably more valid explanation is the information hypothesis. The information hypothesis builds on a broadening base of empirical research that demonstrates that short sellers are well-informed traders. Those mentioned above could be the reason for the functionality because if one follows the decisions of the short-sale practitioners, who tend to be investors with superior analytical skills (for example, according to the research of Gutfleish and Atzil, 2004). The main idea is simple; the research says, that these investors typically initiate short positions only if they can infer low fundamental valuation from public sources. For example, short-sellers may engage in forensic accounting, looking for high levels of accrual as evidence of hidden bad news. Still, there is a large number of other possibilities than just  [accruals](https://quantpedia.com/strategies/accrual-anomaly/) .

**Idea alpha:**

Stocks are then sorted each month into short-interest deciles based on the ratio of short interest to shares outstanding. The investor then goes long on the decile with the lowest short ratio and short on the decile with the highest short ratio.

**Related dataset:**

**Term**

**Data field**

**Dataset**

shares outstanding

sharesout

                               Price volume data for equity

Short Interest Ratio
                                      mdl77_devnorthamericashortsentimentfactor_tni_ths
                               Analysts' Factor Model

---

## 讨论与评论 (13)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hello!

In order to enhance your alpha idea, taking dividends into account could be a crucial factor, especially for short interest alphas. This is because investors typically close short positions around the time of dividend payments. It's an interesting scenario - although short sellers are obligated to repay the dividend amount, stocks usually dip by the dividend price at the same time. Consequently, this repayment could be offset by the gains made through the short position. It's definitely an aspect worth considering in your analysis.

Keep up the great work!

---

### 评论 #2 (作者: TN67143, 时间: 2年前)

Hi,

Thank you for the great article and comment to incorporate dividends into our Alphas building process.

Dividends may be an interesting phenomenon and tools. May we look at them at the below:

Based on some limited observations, Dividends ( [https://www.investopedia.com/terms/d/dividend.asp](https://www.investopedia.com/terms/d/dividend.asp) ) last rights trading days (the last days in which investors holding the stocks can receive the dividends payments) is a noticable days, and news events covering the company's dividends payments scheme can affect the stocks prices. The dividend-related events may be followed by investors to trade in either short-term or long-term (maybe they can be classified into event-based or news-based trading).

First of all, dividends are the amount of money the company pays its shareholders from its profit. They reflect the financial health of the company. If the company pays dividend regularly and in good amount, it can show their sustainable and reliable performance. Therefore, on the long term, it shows that the company can makes sustainable values for its shareholders.

From this reason, company with reliable and good dividends payment schemes tend to attract investors to invest. This also motivate investors to purchase the company's stock before its dividends last days to receive the dividends. This has help the stock prices before that dividends days to rise.

But, after that day, the stock prices are adjusted according to the dividend payments amount. For example, If the stock prices before the dividends last day are $39, and the dividends payments are $2/shares, then the stock prices afterwards would be adjusted to $39-$2 = $37. Moreover, the dividends payments amount can be subject to contemporary taxes, leading to a potential decrease in total investors' assets. Therefore, the value of the investors may decrease due to dividends payments.

After the dividends payment days, after some increases influenced by dividends payments announcement, and the adjusted decrease in prices, if the stocks are not frequently traded or valued by the investors, this can create a momentum for stock prices to fall due to short-term investors cutting loss for fear of future decrease. On the other hand, if the company fundamental are good, the stocks are quality and the investors expect the stock to steadily increase, then the stocks could increase back and even cross the before dividends last day prices. In this case, the investors benefits both from the dividends payments and stock prices increase.

The price movement around dividends-related events can be analyzed by the investors to make suitable investment decisions.

Due to my limited knowledge of this financial terms, there can be incomplete analysis in the above writings.

What do you think about how we can incorporate dividends-related analysis to create good Alphas?

Thank you.

---

### 评论 #3 (作者: AG20578, 时间: 2年前)

Absolutely, utilizing dividends in alpha can bring additional insights. Here are a few:

- **Dividend to Price Ratio.** Use dividend/close to create an indicator that measures the return an investor could expect from dividends alone. Remember to backfill the dividend field to handle missing values effectively.
- **Dividend Growth.**  Use `ts_delta(dividend, n)` to capture how much the dividend has grown over 'n' periods. This can indicate a company's increasing profitability.
- **Dividend Change as a groupping.** You can use the days from the last dividend change to create groups, like `floor(days_from_last_change(dividend)/10)`. This can serve as an effective grouping for neutralization, helping to account for differences in dividend strategies between groups.

These are just starting points. Feel free to tweak these ideas or come up with your own unique approaches to incorporate dividends in your alpha creation process. But remember, every time you make an enhancement, don't forget to use the test period feature to ensure that the changes are actually improving the performance and not just fitting the past data. Keep exploring!

---

### 评论 #4 (作者: AT56452, 时间: 2年前)

Hi, how do we represent going long on a stock and going short on a stock in an expression based form? Thanks!

---

### 评论 #5 (作者: TN67143, 时间: 2年前)

Hi,

In my limited knowledge, BRAIN suggests us use the sign (+, -) to indicate the long, short position.

For example, upon developing an Alpha formulas, we have calculated weights vector that specifies how much weights to allocate to each instrument in the stock universe.

If we wish to long the stock with that weight, then we might let the sign of the weight is +.

Otherwise, if we wish to short the stock with that weight, then we might let the sign of the weight is -, indicating that we short the stocks with the same weight.

Hope that could help further clarify..

---

### 评论 #6 (作者: XL31477, 时间: 1年前)

Hey, that's an interesting alpha idea! The long-short strategy based on short interest deciles makes sense. Sorting stocks monthly by the short interest to shares outstanding ratio is a good approach. The fundamental reasons behind, like the overvaluation and information hypotheses, give it solid theoretical support. And having related datasets like sharesout and that specific sentiment factor dataset is handy for implementing and testing it. Just make sure to do thorough backtesting to assess its real-world performance.

---

### 评论 #7 (作者: XD81759, 时间: 1年前)

Hey! This alpha idea's pretty interesting, guys. The long-short strategy here makes sense as it capitalizes on the short interest anomaly. Sorting stocks into deciles based on short interest ratio is a common approach. By going long on the lowest ratio decile and short on the highest, we aim to benefit from the differences in returns predicted by short interest levels. The key's in using the right datasets like "sharesout" and that sentiment factor one. And the info hypothesis gives solid reasoning behind it all. Just make sure to backtest thoroughly before applying it in real trades.

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

This paper offers valuable insights into how short interest can predict stock returns, with both the overvaluation and information hypotheses providing different perspectives on this anomaly. The strategy of going long on low short-interest stocks while shorting high short-interest ones is a smart way to leverage this predictive power, especially considering its low correlation with the broader market. It's fascinating to see how well-informed short-sellers can contribute to price discovery, and this strategy offers a great tool for portfolio diversification.

---

### 评论 #9 (作者: AT56452, 时间: 1年前)

Yes, the rank operator can be effectively used to balance the long and short sides of an alpha, as it normalizes the values into a uniform distribution, ensuring both sides are evenly represented. This helps prevent any extreme divergence between the long and short positions, which can exaggerate future risk.

---

### 评论 #10 (作者: KS69567, 时间: 1年前)

Thank you for the insightful article and comment on incorporating dividends into the alpha-building process. Integrating dividends can add a valuable dimension to strategies, enhancing risk-adjusted returns and capturing additional market signals.

---

### 评论 #11 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #12 (作者: AK98027, 时间: 1年前)

This paper offers valuable insights into how short interest can predict stock returns, with both the overvaluation and information hypotheses providing different perspectives on this anomaly. The strategy of going long on low short-interest stocks while shorting high short-interest ones is a smart way to leverage this predictive power, especially considering its low correlation with the broader market. It's fascinating to see how well-informed short-sellers can contribute to price discovery, and this strategy offers a great tool for portfolio diversification.

---

### 评论 #13 (作者: CC40930, 时间: 1年前)

This strategy capitalizes on the short-interest anomaly by identifying stocks with high and low short-interest ratios. By going long on stocks with low short interest and shorting stocks with high short interest, investors aim to benefit from the predictive power of short interest. The information hypothesis provides a solid explanation for why this strategy works, as short-sellers often possess superior information about a company’s fundamentals. This strategy is also appealing for portfolio diversification due to its low correlation with broader market movements. It will be interesting to explore further refinements like sector-specific adjustments or liquidity filters.

---

