# Research Paper 70: Day trading and illiquidity premia: Evidence from China

- **链接**: [Commented] Research Paper 70 Day trading and illiquidity premia Evidence from China.md
- **作者**: KA64574
- **发布时间/热度**: 2年前, 得票: 4

## 帖子正文

**Abstract**

Compared to US stocks, Chinese stocks earn most of the returns during the day. We argue this reflects a shifted illiquidity premium caused by the day trading ban in 1995. We estimate difference-in-differences regressions comparing affected Chinese A-class stocks.

to unaffected Chinese B-class stocks and propensity-score matched Japanese stocks around that ban. We find an increase in day returns (especially, for previously liquid stocks), a decrease in night returns, and unchanged 24-hour returns. Using data from 1993 to 2014, we exclude a risk-based explanation and provide evidence indicating that the time-series illiquidity premium shifts from night to day, while the cross-sectional illiquidity premium diminishes.

Authors : Chaoqun Maa, Ru Xiaoa, and Dominik Röschyb

Year : 2021

Link:  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3838211](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3838211)

**Key ideas and Comments from WorldQuant:**

Page 17 para 2

Page 21 para 2

**Term**

**Datafield**

**Link**

chinese a-class stock

mdl265_dvm_china_composite

[**Model265**](https://platform.worldquantbrain.com/data/data-sets/model265?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&universe=TOP2000U)

illiquidity

pv27_as_dq_turn

**[pv27](https://platform.worldquantbrain.com/data/data-sets/pv27?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&universe=TOP2000U)**

bear indicator

mdl175_bearpower

[**Model175**](https://platform.worldquantbrain.com/data/data-sets/model175?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&universe=TOP2000U)

---

## 讨论与评论 (39)

### 评论 #1 (作者: DK20528, 时间: 1年前)

The paper,  **"Day Trading and Illiquidity Premia: Evidence from China"**   provides an intriguing exploration of the relationship between day trading and illiquidity premia in the unique context of the Chinese market. This research addresses a vital topic given the growing prominence of retail investors and the distinctive market structure in China. Below are some comments and questions:

1. **Day Trading Impact:**  Could you clarify the primary channels through which day trading activity influences illiquidity premia? For instance, does the study emphasize the role of volatility, order flow imbalance, or behavioral biases?
2. **Market Structure Specificity:**  The Chinese market has distinct characteristics, such as high retail investor participation and trading restrictions like T+1 rules for stocks. How do these factors affect the generalizability of the findings to other markets?
3. **Measurement of Illiquidity Premia:**  What specific proxies or models were used to quantify illiquidity premia in this study? How do these measures account for the dynamic nature of day trading and intraday liquidity?
4. **Regulatory Implications:**  Does the paper discuss any implications for policymakers or regulators, particularly concerning trading restrictions or measures to enhance market liquidity?
5. **Time Period and Data:**  What time periods and datasets were utilized for the analysis? Were there significant events (e.g., market reforms, policy changes) that might have influenced the results?
6. **Risk-Adjusted Returns:**  Does the study explore whether day trading strategies provide risk-adjusted excess returns, and how these might vary across high- and low-liquidity stocks?
7. **Behavioral Considerations:**  Were any behavioral patterns of day traders, such as herding or overreaction, considered as contributing factors to illiquidity premia?

This paper offers valuable insights into the interplay between day trading and market liquidity, particularly in an emerging market context. Addressing these questions could further clarify the mechanisms and enhance the paper's contribution to the field.

---

### 评论 #2 (作者: LN78195, 时间: 1年前)

It would be interesting to explore how the findings could be generalized to other emerging markets with high retail participation and whether similar patterns are observable under different trading restrictions. How might these insights influence the design of trading strategies or regulatory frameworks in comparable markets?

---

### 评论 #3 (作者: TN48752, 时间: 1年前)

High retail participation often leads to lower liquidity and potentially inefficient price discovery. This could be generalized to other emerging markets where retail investors dominate, especially if institutional involvement is limited.

---

### 评论 #4 (作者: XL31477, 时间: 1年前)

[DK20528](/hc/en-us/profiles/24602396283031-DK20528) , great questions! For the day trading impact, it might involve volatility as more trades can change price swings. Order flow imbalance could also play a part as day trading affects supply & demand. Regarding market structure, the T+1 rule limits quick trading, so findings' generalizability might vary. Illiquidity premia were likely measured using models like pv27_as_dq_turn. For regulatory implications, the paper could've touched on easing trading restrictions to boost liquidity. Time period was 1993 - 2014. Risk-adjusted returns might vary by liquidity level. Behavioral aspects like herding could contribute but need more study.

---

### 评论 #5 (作者: SJ17125, 时间: 1年前)

The paper "Day Trading and Illiquidity Premia: Evidence from China" explores the relationship between day trading and illiquidity premia, focusing on China's unique market structure. Key questions include how day trading influences illiquidity premia (via volatility, order flow, or behavioral biases), and whether the findings can be generalized to other markets with different structures. It would also be valuable to understand the specific proxies used to measure illiquidity premia and the regulatory implications for policymakers. Additionally, investigating whether day trading strategies generate risk-adjusted returns and considering behavioral patterns like herding could enhance the paper's insights.

---

### 评论 #6 (作者: BA51127, 时间: 1年前)

This is a fascinating area of study, particularly given the unique market regulations and the significant role of retail investors in China.

Now, about your curiosity on how day trading influences illiquidity premia, it likely involves a mix of factors such as volatility, order flow imbalances, and perhaps even behavioral biases. The Chinese market's structure, with its distinctive characteristics like the T+1 rule, could indeed affect the generalizability of these findings to other markets.

As for the specifics of measuring illiquidity premia, the paper might use models or proxies that capture intraday liquidity changes. And regarding regulatory implications, there could be insights for policymakers on how to adjust trading restrictions or implement measures to enhance market liquidity.

---

### 评论 #7 (作者: XD81759, 时间: 1年前)

Hey! The key idea here is about the shift in illiquidity premium from night to day for Chinese A-class stocks due to the day trading ban in 1995. They used difference-in-differences regressions. For quant factors, we could consider using "pv27_as_dq_turn" related to illiquidity. And "mdl175_bearpower" as a bear indicator might help in adjusting strategies based on market trends. It's interesting how these elements interact in the context of the study's findings.

---

### 评论 #8 (作者: AT56452, 时间: 1年前)

The 1995 implementation of the T+1 trading rule in China's stock market, which prohibited same-day buying and selling of stocks, significantly influenced return patterns. This policy led to a shift in the illiquidity premium from nighttime to daytime trading sessions.

---

### 评论 #9 (作者: AT56452, 时间: 1年前)

A difference-in-differences analysis comparing Chinese A-class stocks (subject to the T+1 rule) with B-class stocks (initially unaffected) and matched Japanese stocks revealed notable changes. Post-1995, there was an increase in daytime returns, particularly for stocks that were previously more liquid. Conversely, nighttime returns decreased, while overall 24-hour returns remained unchanged.

---

### 评论 #10 (作者: AT56452, 时间: 1年前)

The T+1 trading rule aimed to curb speculative intraday trading and enhance market stability. By restricting rapid buy-sell actions within the same day, it reduced excessive volatility and speculative behaviors that could destabilize the market.

---

### 评论 #11 (作者: AT56452, 时间: 1年前)

The shift in the illiquidity premium from night to day suggests that investors began demanding higher returns for daytime trading, compensating for reduced liquidity due to the trading restrictions. This adjustment reflects the market's adaptation to the new trading environment imposed by the T+1 rule.

---

### 评论 #12 (作者: AT56452, 时间: 1年前)

The cross-sectional illiquidity premium's diminishment indicates a narrowing gap in returns between liquid and illiquid stocks. This change suggests that the T+1 rule may have leveled the playing field, reducing the advantage previously held by more liquid stocks in terms of return premiums.

---

### 评论 #13 (作者: AT56452, 时间: 1年前)

The unchanged 24-hour returns imply that while the distribution of returns between day and night sessions shifted, the overall daily performance of the market remained stable. This stability indicates that the T+1 rule did not adversely affect the market's total return, despite altering intraday dynamics.

---

### 评论 #14 (作者: AT56452, 时间: 1年前)

The policy's impact was more pronounced on previously liquid stocks, which experienced a significant increase in daytime returns. This outcome suggests that the T+1 rule had a differential effect based on a stock's prior liquidity, potentially altering investor behavior towards these securities.

---

### 评论 #15 (作者: AT56452, 时间: 1年前)

The decrease in nighttime returns following the T+1 rule's implementation indicates a reallocation of returns to the daytime. This shift may reflect changes in investor strategies, with a focus on daytime trading when liquidity and trading opportunities were perceived to be higher.

---

### 评论 #16 (作者: AT56452, 时间: 1年前)

The study's findings, based on data from 1993 to 2014, provide robust evidence against a risk-based explanation for the observed return patterns. Instead, they highlight the significant role of market liquidity and trading regulations in shaping return distributions.

---

### 评论 #17 (作者: AT56452, 时间: 1年前)

Overall, the 1995 day trading ban in China led to a redistribution of returns between day and night sessions, influenced by changes in market liquidity and investor behavior. These findings underscore the importance of trading regulations in determining market dynamics and return patterns.

---

### 评论 #18 (作者: CC40930, 时间: 1年前)

This paper explores the impact of China's 1995 day trading ban on stock returns, highlighting a shift in the illiquidity premium. The study finds that compared to U.S. stocks, Chinese stocks earn most of their returns during the day. By using difference-in-differences regressions, the paper compares affected Chinese A-class stocks with unaffected Chinese B-class stocks and Japanese stocks. The findings indicate that, post-ban, day returns increased (especially for previously liquid stocks), while night returns decreased, with overall 24-hour returns remaining unchanged. The paper argues that this shift reflects a time-series illiquidity premium, while the cross-sectional illiquidity premium decreased.

---

### 评论 #19 (作者: AK98027, 时间: 1年前)

**Key Takeaways & Further Considerations:**

- **Day Trading Impact:**  Increased volatility and order flow imbalances are likely consequences of active day trading.
- **Market Structure Influence:**  The T+1 settlement rule likely constrained the study's findings.
- **Liquidity Measurement:**  The paper probably utilized models like pv27_as_dq_turn to estimate illiquidity premia.
- **Regulatory Implications:**  The research could have explored potential benefits of easing trading restrictions to enhance liquidity.
- **Time Period:**  The study covered 1993-2014, which might not fully capture the impact of recent market changes.
- **Risk-Adjusted Returns:**  The relationship between liquidity and risk-adjusted returns may vary across different liquidity levels.
- **Behavioral Factors:**  Herding behavior could potentially influence liquidity premia, but further research is needed to confirm this.

---

### 评论 #20 (作者: RA30956, 时间: 1年前)

The research sheds light on the unique behavior of Chinese stocks, highlighting the dominance of day returns over night returns. This deviation from the norm seen in markets like the US presents a fascinating area for understanding market-specific anomalies and trading patterns.

---

### 评论 #21 (作者: RA30956, 时间: 1年前)

The study attributes the shifted illiquidity premium to the 1995 day trading ban, providing an intriguing example of how regulatory interventions can have long-term effects on market dynamics. The use of a natural experiment to analyze this shift is methodologically robust and enhances the credibility of the findings.

---

### 评论 #22 (作者: RA30956, 时间: 1年前)

The use of difference-in-differences regressions to compare Chinese A-class stocks with B-class stocks and matched Japanese stocks strengthens the analysis. This approach ensures that the findings are not limited to the Chinese market and allows for a broader understanding of how regulatory changes impact illiquidity premiums.

---

### 评论 #23 (作者: RA30956, 时间: 1年前)

The observation that previously liquid stocks experience a significant increase in day returns highlights the disproportionate impact of the day trading ban on certain segments of the market. This finding could be critical for investors who focus on liquidity-sensitive trading strategies.

---

### 评论 #24 (作者: RA30956, 时间: 1年前)

The unchanged 24-hour returns despite the observed shifts in day and night returns is an essential result. It suggests that the overall return profile of the stocks remains stable, even as the distribution of returns across time changes. This stability could have implications for long-term investment strategies.

---

### 评论 #25 (作者: RA30956, 时间: 1年前)

The cross-sectional illiquidity premium diminishes while the time-series illiquidity premium shifts to the day. This nuanced differentiation between time-series and cross-sectional premiums offers a richer understanding of the interaction between liquidity and returns over different time horizons.

---

### 评论 #26 (作者: RA30956, 时间: 1年前)

The study excludes risk-based explanations for the observed changes, suggesting that the results are not merely artifacts of market risk adjustments. This strengthens the argument that the changes are directly tied to the day trading ban and not other external factors.

---

### 评论 #27 (作者: RA30956, 时间: 1年前)

The comparison with propensity-score matched Japanese stocks introduces an additional layer of robustness to the study. By using a control group from a different regulatory environment, the authors ensure that the findings are not unique to the Chinese market but may have parallels elsewhere.

---

### 评论 #28 (作者: RA30956, 时间: 1年前)

The study emphasizes the importance of liquidity in driving stock returns, particularly in the context of regulatory constraints. This insight could be valuable for policymakers aiming to design regulations that balance liquidity concerns with market stability.

---

### 评论 #29 (作者: RA30956, 时间: 1年前)

The observation that night returns decrease post-ban suggests a potential reallocation of trading activity and investor focus to the daytime. This shift in trading behavior could have implications for market microstructure and the design of trading systems.

---

### 评论 #30 (作者: MA70307, 时间: 1年前)

The paper provides valuable insights for investors and fund managers who focus on Chinese stocks. Understanding the shifted illiquidity premium could help refine trading strategies and improve the timing of trades to maximize returns.

---

### 评论 #31 (作者: MA70307, 时间: 1年前)

The analysis of data spanning over two decades (1993–2014) ensures that the findings are not driven by short-term market fluctuations or temporary trends. This long-term perspective enhances the reliability of the conclusions drawn from the study.

---

### 评论 #32 (作者: MA70307, 时间: 1年前)

The study indirectly highlights the role of institutional investors and their trading patterns in influencing market behavior. The regulatory ban may have affected retail investors disproportionately, leading to a redistribution of trading volumes and liquidity provision.

---

### 评论 #33 (作者: MA70307, 时间: 1年前)

The findings have implications for understanding market efficiency. The shift in illiquidity premiums suggests that market inefficiencies introduced by regulations can persist over time and influence return patterns.

---

### 评论 #34 (作者: MA70307, 时间: 1年前)

The differentiation between A-class and B-class stocks provides a valuable perspective on how regulations can create disparities within the same market. This highlights the importance of considering stock classifications when analyzing market dynamics.

---

### 评论 #35 (作者: MA70307, 时间: 1年前)

The study’s findings could inform future regulatory decisions in emerging markets. Understanding the long-term impacts of trading restrictions can help policymakers design interventions that minimize adverse effects on liquidity and return profiles.

---

### 评论 #36 (作者: MA70307, 时间: 1年前)

The methodological rigor, including the use of multiple datasets and control groups, ensures that the study’s conclusions are well-supported. This robustness makes the paper a valuable resource for both academics and practitioners interested in market microstructure.

---

### 评论 #37 (作者: MA70307, 时间: 1年前)

The decrease in night returns following the day trading ban provides an opportunity to explore investor behavior during after-hours trading. This aspect of the market remains under-researched and could offer additional insights into how trading activity shifts in response to regulatory changes.

---

### 评论 #38 (作者: MA70307, 时间: 1年前)

The study’s findings contribute to the broader literature on illiquidity premiums and their role in asset pricing. By examining the Chinese market, the paper provides a unique perspective that complements research conducted in more developed markets.

---

### 评论 #39 (作者: MA70307, 时间: 1年前)

The shifted illiquidity premium observed in the study could have implications for the pricing of derivatives and other financial instruments linked to Chinese stocks. Understanding this shift could help market participants better manage risk and design more effective hedging strategies.

---

