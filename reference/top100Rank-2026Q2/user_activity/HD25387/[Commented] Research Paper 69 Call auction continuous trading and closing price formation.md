# Research Paper 69: Call auction, continuous trading and closing price formation

- **链接**: [Commented] Research Paper 69 Call auction continuous trading and closing price formation.md
- **作者**: KA64574
- **发布时间/热度**: 2年前, 得票: 4

## 帖子正文

**Abstract:**

The Shanghai Stock Exchange changed its trading mechanism of the preceding three minutes to closing from continuous trading to call auction on August 20, 2018, while Shenzhen had already changed this in 2006. Taking all A-shared stocks’ data from 2017 to 2019 as our sample, we construct difference-in-difference models and find significant trading volume shifts from closing call to preceding continuous trading. We also see a significant increase in volatility in call preceding continuous trading, but a significant decrease in closing price deviation in a closing call. Market efficiency is found to be improved by these changes, perhaps due to less liquidity noise in the closing price. Our conclusions remain robust in various robustness checks. It suggests that the introduction of closing call auction would reduce manipulation and liquidity noise in the closing price, thus improving market efficiency in China.

Author : Jiayi Li, Sumei Luo & Guangyou Zhou

Year : 2021

Link :  **[https://www.tandfonline.com/doi/full/10.1080/14697688.2020.1849782](https://www.tandfonline.com/doi/full/10.1080/14697688.2020.1849782)**

**Key ideas and Comments from WorldQuant:**

Page 3 para 2

Page 4 para 3

Page 9 para 5

Term

Datafield

Link

continuous trading

pv27_s_strange_volume

[**pv27**](https://platform.worldquantbrain.com/data/data-sets/pv27?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&universe=TOP3000)

auction

pv27_open_moneyflow_pct_volume

[**pv27**](https://platform.worldquantbrain.com/data/data-sets/pv27?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&universe=TOP3000)

volatility

pv27_ashare_volume_w

[**pv27**](https://platform.worldquantbrain.com/data/data-sets/pv27?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&universe=TOP3000)

---

## 讨论与评论 (63)

### 评论 #1 (作者: DK20528, 时间: 1年前)

This article presents an intriguing analysis of market microstructure, particularly focusing on auction mechanisms, continuous trading, and the dynamics of closing price formation. The authors offer a comprehensive investigation into how these components interact to impact liquidity, price efficiency, and market stability.

**Strengths:**

1. The integration of auction theory with continuous trading dynamics is a unique contribution, highlighting the transitional mechanisms between pre-market, intraday, and post-market phases.
2. Empirical methods or theoretical frameworks (if included) appear robust for dissecting price formation mechanisms, particularly in closing auctions.
3. The study has practical relevance for policymakers, market regulators, and practitioners in understanding how auction designs influence market outcomes.

**Potential Areas for Further Development:**

1. Expanding the scope of the analysis to include cross-market comparisons could enhance the generalizability of the findings, particularly across different regulatory environments.
2. If empirical data is used, incorporating more diverse datasets or a broader time frame might offer deeper insights into temporal changes in price formation processes.
3. Exploring the behavioral aspects of participants in auction and continuous trading could add an additional layer of depth to the analysis.

Overall, this study sheds valuable light on the nuanced interactions between auction mechanisms and trading dynamics, a topic of critical importance for the efficient functioning of modern financial markets.

---

### 评论 #2 (作者: TD17989, 时间: 1年前)

Hi, I think we can regress vwap or return on pv27 dependent variables. I tried it and got some good results

---

### 评论 #3 (作者: XL31477, 时间: 1年前)

Hey TD17989's idea of regressing vwap or return on pv27 dependent variables sounds interesting. It could potentially reveal useful relationships in the market data. But we should also consider if there are other factors that might affect the results, like market conditions or specific stock characteristics. Maybe we can do more robustness checks to make sure those good results hold up. Just my two cents.

---

### 评论 #4 (作者: SJ17125, 时间: 1年前)

This article provides a thorough analysis of market microstructure, focusing on auction mechanisms, continuous trading, and closing price formation. The integration of auction theory with continuous trading dynamics is a unique contribution, offering valuable insights into market liquidity and efficiency. Expanding the analysis to include cross-market comparisons and broader datasets could further enhance its applicability. Additionally, exploring the behavioral aspects of market participants in these contexts would deepen the understanding of price formation. Overall, the study offers important insights for policymakers and market practitioners on the influence of auction designs on market outcomes.

---

### 评论 #5 (作者: BA51127, 时间: 1年前)

The discussion on Research Paper 69 highlights the impact of auction mechanisms on market dynamics, particularly in the context of the Shanghai Stock Exchange's transition to a call auction system for closing prices. The findings suggest that this change reduced manipulation and liquidity noise in closing prices, improving market efficiency. For further exploration, it would be interesting to see how these results compare with other markets that have different trading mechanisms, especially regarding the behavior of different types of investors during auctions and continuous trading sessions.

---

### 评论 #6 (作者: AT56452, 时间: 1年前)

Shanghai Stock Exchange - A mention of this is a pretty good tell to simulate the alpha made using this paper in the China region as the logic in this paper would do best in China then.

---

### 评论 #7 (作者: XD81759, 时间: 1年前)

There's an issue with the provided link. It seems the page couldn't be parsed. But from the abstract, we know the study focused on the trading mechanism change in Shanghai and Shenzhen exchanges. They used difference-in-difference models with A-share data from 2017 - 2019. The key findings were volume shifts, volatility changes, and improved market efficiency. For more details, we need to access the full paper properly.

---

### 评论 #8 (作者: AT56452, 时间: 1年前)

The Shanghai Stock Exchange (SSE) transitioned its closing mechanism from continuous trading to a call auction on August 20, 2018, aligning with the Shenzhen Stock Exchange's earlier adoption in 2006. This strategic shift aimed to enhance market efficiency and integrity.

---

### 评论 #9 (作者: AT56452, 时间: 1年前)

Post-implementation, a notable redistribution of trading volumes was observed. Specifically, there was a significant reduction in trading activity during the closing call auction, accompanied by an increase in the minutes preceding it. This suggests that traders adjusted their strategies to align with the new mechanism, potentially to mitigate risks associated with order execution during the call auction period.

---

### 评论 #10 (作者: AT56452, 时间: 1年前)

The introduction of the closing call auction led to a discernible increase in volatility during the continuous trading period immediately before the auction. Conversely, volatility during the closing call auction itself decreased. This indicates that while the call auction stabilized end-of-day prices, it may have shifted some price fluctuations to the preceding continuous trading period.

---

### 评论 #11 (作者: AT56452, 时间: 1年前)

A significant decrease in closing price deviations was recorded following the adoption of the call auction. This improvement suggests that the mechanism contributed to more accurate price discovery at the market close, reducing discrepancies between closing prices and intrinsic stock values.

---

### 评论 #12 (作者: AT56452, 时间: 1年前)

The shift to a closing call auction has been associated with improved market efficiency. By consolidating orders and reducing the potential for price manipulation, the auction mechanism fosters a trading environment where prices more accurately reflect available information.

---

### 评论 #13 (作者: AT56452, 时间: 1年前)

The call auction's introduction appears to have curtailed opportunities for closing price manipulation. By aggregating orders and determining a single closing price, the mechanism makes it more challenging for traders to influence prices through large, strategic trades at the close.

---

### 评论 #14 (作者: AT56452, 时间: 1年前)

Implementing the closing call auction has contributed to a reduction in liquidity noise at the market close. This reduction enhances the reliability of closing prices as benchmarks for valuation and performance assessment.

---

### 评论 #15 (作者: AT56452, 时间: 1年前)

The SSE's adoption of the closing call auction brought its practices in line with the Shenzhen Stock Exchange, which had implemented a similar mechanism in 2006. This harmonization may facilitate more consistent trading behaviors and expectations across China's major stock exchanges.

---

### 评论 #16 (作者: AT56452, 时间: 1年前)

Research indicates that the introduction of the closing call auction has helped reduce the risk associated with small-cap stocks, improving the continuity of price formation and contributing to a more stable trading environment for these securities.

---

### 评论 #17 (作者: AT56452, 时间: 1年前)

The change in trading mechanism prompted investors to modify their trading strategies, particularly concerning order placements and timing, to adapt to the new closing procedures. This behavioral shift reflects the market's responsiveness to structural changes aimed at enhancing efficiency.

---

### 评论 #18 (作者: AT56452, 时间: 1年前)

The transition to a closing call auction has been associated with improvements in overall market quality, including better price discovery, reduced volatility at the close, and enhanced protection against manipulative trading practices. These developments contribute to a more robust and reliable market infrastructure.

---

### 评论 #19 (作者: AT56452, 时间: 1年前)

In summary, the SSE's implementation of a closing call auction has yielded several benefits, including improved market efficiency, reduced price manipulation, and enhanced price discovery, aligning with global best practices in stock exchange operations.

---

### 评论 #20 (作者: AT56452, 时间: 1年前)

On August 20, 2018, the Shanghai Stock Exchange (SSE) implemented a significant change in its trading mechanism by introducing a closing call auction session. This adjustment altered the trading hours, reducing the afternoon continuous auction from 13:00–15:00 to 13:00–14:57, with the new closing call auction session running from 14:57 to 15:00.

---

### 评论 #21 (作者: AT56452, 时间: 1年前)

Prior to this change, the Shenzhen Stock Exchange had already adopted a similar closing call auction mechanism in 2006. This earlier adoption provided a comparative framework for assessing the impact of such trading mechanisms on market dynamics.

---

### 评论 #22 (作者: AT56452, 时间: 1年前)

To evaluate the effects of the closing call auction, researchers constructed difference-in-difference models using data from all A-shared stocks between 2017 and 2019. This approach allowed for a robust analysis of the trading volume shifts and volatility changes associated with the new trading mechanism.

---

### 评论 #23 (作者: AT56452, 时间: 1年前)

The study found a significant shift in trading volume from the closing call auction to the preceding continuous trading session. This indicates that investors adjusted their trading behaviors in response to the new mechanism, potentially seeking to capitalize on the continuous trading environment rather than the call auction.

---

### 评论 #24 (作者: AT56452, 时间: 1年前)

An increase in volatility was observed during the pre-closing continuous trading session. This heightened volatility suggests that the transition to a closing call auction may have influenced investor behavior, leading to more pronounced price fluctuations in the final minutes of continuous trading.

---

### 评论 #25 (作者: AT56452, 时间: 1年前)

Conversely, the introduction of the closing call auction led to a significant decrease in closing price deviation. This improvement in price accuracy suggests that the call auction mechanism enhanced the reliability of closing prices, reducing discrepancies that could arise from end-of-day trading activities.

---

### 评论 #26 (作者: CC40930, 时间: 1年前)

This paper examines the impact of the Shanghai Stock Exchange's transition from continuous trading to a call auction mechanism for the three minutes leading up to the market close, which occurred on August 20, 2018. The study analyzes data from 2017 to 2019 for all A-shared stocks and employs difference-in-difference models. The results show significant shifts in trading volume from closing call auctions to the preceding continuous trading period, as well as a rise in volatility during the call auction period. However, there was a decrease in closing price deviation, suggesting improved market efficiency due to reduced liquidity noise. The findings support the idea that closing call auctions help reduce manipulation and enhance market efficiency in China.

---

### 评论 #27 (作者: VP21767, 时间: 1年前)

This study analyzes the Shanghai Stock Exchange's shift from continuous trading to a call auction for closing prices. Using data from 2017 to 2019, it highlights a significant reduction in closing price deviation and liquidity noise, improving market efficiency. However, it notes increased volatility before the call auction. These findings suggest that call auctions can minimize manipulation and stabilize the closing price formation process, enhancing overall market functionality in China.

---

### 评论 #28 (作者: VP21767, 时间: 1年前)

[DK20528](/hc/en-us/profiles/24602396283031-DK20528)  This article provides a detailed examination of market microstructure, emphasizing auction mechanisms, continuous trading, and the formation of closing prices. Key strengths include integrating auction theory with trading dynamics, offering insights into transitional phases, and its practical relevance for policymakers and regulators. Areas for improvement could involve cross-market comparisons, broader datasets, and behavioral analyses of participants. Overall, the study contributes valuable insights into market efficiency and liquidity, highlighting the impact of auction designs on modern financial markets.

---

### 评论 #29 (作者: HD25387, 时间: 1年前)

The transition from continuous trading to a call auction mechanism in the Shanghai Stock Exchange highlights an important shift in market dynamics. It’s interesting to see how this change led to reduced closing price deviations and improved market efficiency. Exploring similar mechanisms in other markets might yield insightful comparisons.

---

### 评论 #30 (作者: HD25387, 时间: 1年前)

The study's focus on the significant trading volume shift and volatility changes provides a valuable perspective on liquidity management. Using the  **pv27_s_strange_volume**  field for analyzing continuous trading impacts could reveal more nuanced effects of these mechanisms.

---

### 评论 #31 (作者: HD25387, 时间: 1年前)

I find the reduction in liquidity noise in closing prices particularly fascinating. It suggests that the call auction system could be a more robust way to handle price discovery near market close. This could be worth exploring in regions or stocks with high manipulation concerns.

---

### 评论 #32 (作者: HD25387, 时间: 1年前)

Improved market efficiency through structural changes like this is a great takeaway. Leveraging  **pv27_open_moneyflow_pct_volume**  to assess auction effectiveness might provide deeper insights into optimizing trading mechanisms in other markets.

---

### 评论 #33 (作者: AK98027, 时间: 1年前)

I appreciate you taking the time to share your thoughts and insights. This article effectively integrates auction theory with continuous trading dynamics, providing a novel perspective on market microstructure. The study employs robust methods to analyze price formation, particularly in closing auctions. The findings have valuable implications for policymakers and market participants in optimizing market design and enhancing market efficiency. Further research should explore cross-market comparisons, utilize diverse datasets, and incorporate behavioral aspects of market participants to further enrich our understanding of these complex market phenomena.

---

### 评论 #34 (作者: HT59568, 时间: 1年前)

**Impact of trading mechanism change:**  How did the shift from continuous trading to call auction on the Shanghai Stock Exchange affect trading volume and price volatility?

---

### 评论 #35 (作者: HT59568, 时间: 1年前)

**Difference-in-difference model findings:**  What were the key insights derived from the difference-in-difference models regarding trading volume shifts and price deviations?

---

### 评论 #36 (作者: HT59568, 时间: 1年前)

**Volatility in call preceding continuous trading:**  Why did the transition result in a significant increase in volatility during the call preceding continuous trading?

---

### 评论 #37 (作者: HT59568, 时间: 1年前)

**Reduction in closing price deviation:**  How does the introduction of the closing call auction contribute to reducing closing price deviations?

---

### 评论 #38 (作者: HT59568, 时间: 1年前)

**Market efficiency improvements:**  What factors suggest that market efficiency improved following the adoption of the closing call auction?

---

### 评论 #39 (作者: HT59568, 时间: 1年前)

**Manipulation and liquidity noise:**  In what ways does the closing call auction reduce manipulation and liquidity noise in the closing price?

---

### 评论 #40 (作者: HT59568, 时间: 1年前)

**Comparison with Shenzhen Stock Exchange:**  How does the Shanghai Stock Exchange’s transition compare to the Shenzhen Stock Exchange, which implemented similar changes in 2006?

---

### 评论 #41 (作者: HT59568, 时间: 1年前)

**Data robustness checks:**  What methods were used to ensure the robustness of the study’s conclusions, and what were the outcomes?

---

### 评论 #42 (作者: HT59568, 时间: 1年前)

**Role of auction-related metrics:**  How do metrics like pv27_open_moneyflow_pct_volume and pv27_ashare_volume_w help analyze the impact of the closing call auction?

---

### 评论 #43 (作者: HT59568, 时间: 1年前)

**Broader implications for market design:**  What are the broader implications of the study’s findings for improving market efficiency through trading mechanism changes?

---

### 评论 #44 (作者: MA70307, 时间: 1年前)

The research paper highlights a significant evolution in the trading mechanism of Chinese stock exchanges, specifically the introduction of a call auction system during the closing minutes of trading. This change, implemented by the Shanghai Stock Exchange in 2018, brings its operations in line with the Shenzhen Stock Exchange, which adopted this mechanism earlier in 2006. The study effectively captures the impact of this transition on trading volume, volatility, and closing price formation, presenting a detailed analysis of how these changes influence market behavior and efficiency. The authors’ use of difference-in-difference models and extensive data sets spanning three years adds empirical rigor, allowing for robust conclusions about the implications of the new system.

---

### 评论 #45 (作者: MA70307, 时间: 1年前)

One of the standout findings is the observed shift in trading volume from the closing call auction to the preceding continuous trading session. This shift underscores the behavioral adjustments traders make when a call auction system is introduced, as they seek to optimize their positions in light of new market conditions. The study also identifies an increase in volatility during the continuous trading period that precedes the call auction. This finding provides valuable insights into how market participants adjust their strategies in response to changes in trading mechanisms, particularly when anticipating the final call auction.

---

### 评论 #46 (作者: MA70307, 时间: 1年前)

Another important aspect of the study is the observed reduction in closing price deviation as a result of the call auction. This suggests that the mechanism introduces greater price stability by reducing noise and manipulation, thereby leading to more accurate price discovery. The reduction in liquidity noise, specifically, highlights the benefits of the call auction system for enhancing market efficiency. This finding is particularly relevant for regulators and policymakers aiming to ensure fair and efficient trading environments while minimizing opportunities for price manipulation.

---

### 评论 #47 (作者: MA70307, 时间: 1年前)

The paper’s emphasis on market efficiency offers a compelling argument for the broader adoption of closing call auctions, particularly in markets that currently rely solely on continuous trading. By demonstrating how the call auction reduces noise in the closing price, the study supports the notion that trading mechanisms can be designed to optimize liquidity and transparency. The implications for international markets are significant, as the findings may inspire similar reforms in other regions seeking to improve their market structures.

---

### 评论 #48 (作者: MA70307, 时间: 1年前)

The authors’ methodological approach is another strength of the paper. Their use of difference-in-difference models allows them to isolate the effects of the call auction from other factors influencing market behavior. Additionally, the robustness checks conducted reinforce the credibility of the findings, ensuring that the conclusions are not the result of data biases or methodological errors. This analytical rigor enhances the paper’s contribution to the literature on market microstructure.

---

### 评论 #49 (作者: MA70307, 时间: 1年前)

While the paper provides valuable insights, there are opportunities for further development. One such area is the inclusion of cross-market comparisons to assess the generalizability of the findings. By examining markets with different regulatory frameworks and trading practices, the authors could provide a more comprehensive understanding of how call auctions function across diverse environments. This would also help identify best practices and potential challenges in implementing similar mechanisms globally.

---

### 评论 #50 (作者: MA70307, 时间: 1年前)

The behavioral aspects of market participants in response to the call auction mechanism also warrant further exploration. Understanding the motivations and strategies of traders, particularly institutional investors, could add depth to the analysis. This behavioral perspective would complement the empirical findings and provide a more holistic view of the impact of the call auction system on market dynamics.

---

### 评论 #51 (作者: MA70307, 时间: 1年前)

The temporal dimension of the study, while adequate for the scope of the paper, could be extended to include a longer time frame. Analyzing data over a more extended period would capture the long-term effects of the call auction system, particularly as market participants adjust their strategies over time. This would also allow for a deeper exploration of any lagging impacts on market efficiency and stability.

---

### 评论 #52 (作者: MA70307, 时间: 1年前)

The practical implications of the findings make this study particularly relevant for policymakers and regulators. The reduction in closing price manipulation and liquidity noise underscores the value of carefully designed trading mechanisms. The authors’ conclusions provide a strong case for revisiting and refining trading systems to enhance market integrity and efficiency. As markets continue to evolve, the insights from this study could serve as a foundation for future reforms and innovations in trading practices.

---

### 评论 #53 (作者: MA70307, 时间: 1年前)

Overall, this paper contributes significantly to the understanding of market microstructure and the interplay between auction mechanisms and continuous trading. Its findings have practical relevance for improving trading systems, and the study provides a robust foundation for future research in this area. By addressing the areas for further development, such as cross-market comparisons and behavioral analysis, the authors could build on this work to provide even greater insights into the complexities of market dynamics.

---

### 评论 #54 (作者: RA30956, 时间: 1年前)

The study effectively bridges the gap between auction theory and practical market dynamics, highlighting how theoretical models can be applied to real-world trading systems to improve efficiency and stability. This connection underscores the practical importance of academic research in shaping financial market reforms.

---

### 评论 #55 (作者: RA30956, 时间: 1年前)

By focusing on both the Shanghai and Shenzhen Stock Exchanges, the paper offers a comparative perspective on the impact of the call auction system, demonstrating its consistency in improving market efficiency across different timelines and market structures.

---

### 评论 #56 (作者: RA30956, 时间: 1年前)

The reduction in closing price manipulation observed in the study is a critical finding, as it aligns with the broader goal of enhancing transparency and fairness in financial markets. This highlights the potential of call auctions as a tool for fostering investor confidence.

---

### 评论 #57 (作者: RA30956, 时间: 1年前)

The significant shift in trading volume from the call auction to preceding continuous trading sessions reflects the adaptability of market participants. It also indicates that the timing and structure of trading mechanisms can directly influence trading behavior.

---

### 评论 #58 (作者: RA30956, 时间: 1年前)

The study’s focus on volatility during the continuous trading session preceding the call auction sheds light on a potential trade-off between price stability and participant activity. This nuanced understanding can guide future adjustments in trading system designs.

---

### 评论 #59 (作者: RA30956, 时间: 1年前)

Market efficiency, as improved through the call auction mechanism, is shown to benefit from reduced liquidity noise. This finding emphasizes the importance of reducing extraneous factors that distort price discovery, which is crucial for maintaining market integrity.

---

### 评论 #60 (作者: RA30956, 时间: 1年前)

The paper highlights the dynamic nature of financial markets, where changes in trading mechanisms can have cascading effects on market behavior. This adaptability necessitates ongoing evaluation and refinement of trading systems to ensure optimal performance.

---

### 评论 #61 (作者: RA30956, 时间: 1年前)

The robustness checks conducted in the study provide a critical safeguard against potential biases or inaccuracies. This methodological rigor strengthens the credibility of the conclusions and serves as a benchmark for future research in similar areas.

---

### 评论 #62 (作者: RA30956, 时间: 1年前)

The empirical findings underscore the need for a balance between continuous trading and auction mechanisms. While both have distinct advantages, the combination appears to offer a more holistic approach to achieving market stability and efficiency.

---

### 评论 #63 (作者: RA30956, 时间: 1年前)

The study’s implications extend beyond the Chinese market, offering insights for global markets considering similar reforms. By showcasing the benefits of the call auction system, the paper serves as a valuable resource for understanding how trading mechanism changes can optimize market outcomes.

---

