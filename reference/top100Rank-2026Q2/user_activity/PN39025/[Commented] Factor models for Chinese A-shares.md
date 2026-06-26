# Factor models for Chinese A-shares

- **链接**: [Commented] Factor models for Chinese A-shares.md
- **作者**: TN51777
- **发布时间/热度**: 1年前, 得票: 48

## 帖子正文

Hi everyone, last week I posted a forum post for 5 factors Fama model, it's interesting that many people care about how to implement idea and using knowledge to improve alpha.

So I would like to introduce other paper, which focus on China market. From my point of view, each market having its characteristic, so value which can apply in US might not working in other regions.

Abstract: The paper evaluates common asset pricing models for the Chinese A-shares market. The q-factor model, while strong among U.S.-originated models, is outperformed by models specifically tailored to the Chinese market, including a modified six-factor model and a four-factor model designed for A-shares. The research also applies a data-driven method, resulting in a seven-factor model. Interestingly, when transaction costs are accounted for, the model ranking shifts, and a simpler three-factor model (market, size, and earnings-based value) becomes the preferred option.

Data using: almost data in CHN, but focus on value risk factor data (Fundamental/Analyst/Model)

In last post, I saw many questions about how data in the paper being process, or detail formula in the paper, so I will summary highlight note in each part in my comments

---

## 讨论与评论 (46)

### 评论 #1 (作者: TN51777, 时间: 1年前)

Link paper: Factor models for Chinese A-shares by Matthias X. Hanauer a b ,  Maarten Jansen b ,  Laurens Swinkels b c ,  Weili Zhou b

[https://www.sciencedirect.com/science/article/pii/S105752192300491X](https://www.sciencedirect.com/science/article/pii/S105752192300491X%C2%A0)

---

### 评论 #2 (作者: TN51777, 时间: 1年前)

Introduction: China, the world’s second-largest economy, saw its GDP grow from 36% of the U.S.'s in 2000 to 116% in 2020. Its equity market has become the second-largest globally in terms of capitalization and trading volume, yet Chinese A-shares remain segmented from international markets.

---

### 评论 #3 (作者: TN51777, 时间: 1年前)

Unique Market Characteristics: The A-share market has distinct corporate governance and agency problems compared to global markets, making it a prime testing ground for determining the factors influencing stock returns. Studies on such markets are critical since they may reveal unique patterns not found in integrated financial markets.

---

### 评论 #4 (作者: TN51777, 时间: 1年前)

Challenges in Factor Models: The rise of numerous asset pricing factors, often seen as "spurious," has prompted research to examine their validity in less financially integrated markets like China. This is crucial to distinguish real factors from statistical anomalies and refine asset pricing models beyond traditional frameworks like CAPM and the Fama-French three-factor model.

---

### 评论 #5 (作者: TN51777, 时间: 1年前)

Existing Models: Several asset pricing models have been proposed, such as the five- and six-factor models by Fama and French (2015, 2018), the q-factor model by Hou et al. (2015), and the mispricing model by Stambaugh and Yuan (2017). Comparisons of these models are abundant in the context of U.S. stock returns, with studies like Barillas & Shanken (2018) and Hou et al. (2019) offering insights into their performance.

---

### 评论 #6 (作者: TN51777, 时间: 1年前)

Five-Factor Model Performance: Research indicates that the five-factor model (Fama and French, 2015), particularly its inclusion of the profitability factor, outperforms the three-factor model in the Chinese market. However, the investment factor appears to have a lesser impact. This paper aims to provide a more comprehensive comparison of various models for the Chinese A-shares market, filling an important gap in current research.

---

### 评论 #7 (作者: TN51777, 时间: 1年前)

Keys finding:

Model Performance: The traditional three- and five-factor models (Fama & French, 1993, 2015) poorly price Chinese stock returns. The introduction of a momentum factor and replacing book-to-market and profitability factors with updated book-to-market and return-on-equity factors significantly improves the model’s performance.

---

### 评论 #8 (作者: TN51777, 时间: 1年前)

Tailored Four-Factor Model: A four-factor model specifically designed for the Chinese A-shares market outperforms the U.S.-based models, showing the importance of tailoring asset pricing models to local markets. Additionally, a seven-factor model derived from a data-driven Bayesian approach achieves the highest Sharpe ratio, indicating its superior predictive power.

---

### 评论 #9 (作者: TN51777, 时间: 1年前)

Impact of Transaction Costs: Accounting for transaction costs reveals that models with high turnover and large gross alphas may not be profitably traded in practice. After adjusting for transaction costs, a simplified three-factor model with market, size, and updated earnings-based value factors is preferred, showing the practical relevance of transaction costs in model selection.

---

### 评论 #10 (作者: TN51777, 时间: 1年前)

Value Factor's Importance: Despite recent poor performance in U.S. markets, the value factor remains important in the Chinese A-shares market. The paper suggests that dismissing value factors based on their underperformance elsewhere may be premature, emphasizing their continued relevance in this context.

---

### 评论 #11 (作者: TN51777, 时间: 1年前)

Take aways:

Value Premium Discussion: The paper contributes to the ongoing debate on the existence of the value premium in asset pricing models. While recent studies, including Fama and French (2015), argue that the value premium may be redundant for U.S. markets, this study challenges that notion in the context of Chinese A-shares, where the value factor still shows predictive power.

---

### 评论 #12 (作者: TN51777, 时间: 1年前)

Redundancy of Value Premium: The paper suggests that the value factor should not be dismissed outright, even though its performance has been questioned in other markets, particularly in the U.S. The findings indicate that value remains a relevant and non-redundant factor for pricing stock returns in the Chinese A-shares market.

---

### 评论 #13 (作者: TN51777, 时间: 1年前)

Current Debate on Value Factors: The discussion around whether the value premium will persist or if the value factors as currently defined are outdated is central to current asset pricing debates. The study argues that, at least in the case of China, value factors remain significant, pointing to the need for region-specific analysis when considering the role of value in asset pricing.

---

### 评论 #14 (作者: TN51777, 时间: 1年前)

Hopefully my summary is helpful for you, if you have any more questions, such as how data is processing, or how variable is contructing, or how parameter is determining, I will provide more summary, and some ideas how apply them in WQBrain

---

### 评论 #15 (作者: CD94009, 时间: 1年前)

Hi, thanks for sharing your insights and for introducing this interesting paper on asset pricing models in the Chinese A-shares market. I completely agree with your point that markets have unique characteristics, and a model that works well in the U.S. may not necessarily be effective elsewhere

---

### 评论 #16 (作者: CD94009, 时间: 1年前)

Regarding the paper you shared, I have a few questions:

How does the modified six-factor model differ from the original q-factor model?

---

### 评论 #17 (作者: CD94009, 时间: 1年前)

Can you elaborate on the data-driven method that resulted in the seven-factor model? Specifically, how were the factors identified

---

### 评论 #18 (作者: CD94009, 时间: 1年前)

When discussing transaction costs and their impact on model preference, how were these costs measured or estimated

---

### 评论 #19 (作者: CD94009, 时间: 1年前)

Additionally, I noticed that you plan to summarize the key notes in your comments. I think this will be incredibly helpful, especially for those of us who are curious about the data processing techniques and formulas but might not have the time to dive into the full paper. Looking forward to your summary!

Great topic, and I’m excited to see the discussion it sparks!

---

### 评论 #20 (作者: PN39025, 时间: 1年前)

Thank you for introducing this paper and for your valuable contribution to the community. The focus on tailoring asset pricing models specifically for the Chinese A-shares market is insightful, especially considering the limitations of U.S.-based models in different regions. The introduction of a data-driven seven-factor model and the preference for a simpler three-factor model when accounting for transaction costs are particularly interesting points.

We appreciate your detailed notes and summary of key aspects, including data processing and formulas. I will definitely look into this approach and evaluate its performance further. Thanks again for sharing!

---

### 评论 #21 (作者: AK98027, 时间: 1年前)

China's economic ascent has been remarkable. Its GDP surged from 36% of the U.S.'s in 2000 to a commanding 116% in 2020, solidifying its position as the world's second-largest economy. This economic growth has fueled the expansion of its equity market, making it a global powerhouse in terms of capitalization and trading volume. However, Chinese A-shares, those traded domestically, remain largely inaccessible to international investors.

---

### 评论 #22 (作者: AK98027, 时间: 1年前)

The A-share market presents a unique research opportunity due to its distinct corporate governance and agency issues compared to more established global markets. These idiosyncrasies offer a valuable testing ground for identifying the factors that drive stock returns. By studying this unique market environment, researchers can potentially uncover novel patterns in stock price behavior that may not be evident in more integrated financial systems

---

### 评论 #23 (作者: AK98027, 时间: 1年前)

The proliferation of asset pricing factors, many of which may be spurious, has spurred research to investigate their validity in less integrated markets such as China. This scrutiny is essential to differentiate genuine risk factors from statistical artifacts. By examining factor performance in this unique market environment, researchers can refine existing asset pricing models, such as the CAPM and the Fama-French three-factor model, and potentially uncover new insights into the drivers of stock returns.

---

### 评论 #24 (作者: AK98027, 时间: 1年前)

Several asset pricing models have been proposed, including the five- and six-factor models by Fama and French (2015, 2018), the q-factor model by Hou et al. (2015), and the mispricing model by Stambaugh and Yuan (2017). Extensive research, such as the work of Barillas & Shanken (2018) and Hou et al. (2019), has compared these models extensively in the context of U.S. stock returns, providing valuable insights into their relative performance and predictive power.

---

### 评论 #25 (作者: AK98027, 时间: 1年前)

Research suggests that the five-factor model (Fama and French, 2015), particularly its inclusion of the profitability factor, exhibits superior explanatory power compared to the three-factor model in the Chinese market. However, the investment factor appears to have a weaker influence on stock returns in this context. This paper aims to bridge this gap in the literature by conducting a more comprehensive comparison of various asset pricing models, including the five-factor model, in the context of the Chinese A-shares market.

---

### 评论 #26 (作者: AK98027, 时间: 1年前)

Traditional asset pricing models, such as the three- and five-factor models of Fama and French (1993, 2015), exhibit limited success in explaining stock returns within the Chinese market. However, model performance can be significantly enhanced by incorporating a momentum factor and revising the traditional book-to-market and profitability factors with updated measures of book-to-market ratio and return on equity.

---

### 评论 #27 (作者: AK98027, 时间: 1年前)

A four-factor model specifically tailored to the characteristics of the Chinese A-shares market demonstrates superior performance compared to U.S.-based models, highlighting the critical importance of market-specific factors in asset pricing. Furthermore, a seven-factor model derived through a data-driven Bayesian approach achieves the highest Sharpe ratio, suggesting its superior predictive power in capturing the unique risk premia within the Chinese market.

---

### 评论 #28 (作者: AK98027, 时间: 1年前)

The impact of transaction costs significantly alters the practical viability of asset pricing models. Models characterized by high portfolio turnover and substantial gross alphas may generate significant returns in theory, but these returns can be eroded by transaction costs, rendering them unprofitable in practice. After incorporating transaction costs into the analysis, a simplified three-factor model incorporating market, size, and updated earnings-based value factors emerges as the preferred model, highlighting the critical role of transaction costs in selecting practically relevant asset pricing models.

---

### 评论 #29 (作者: AK98027, 时间: 1年前)

Despite recent challenges in U.S. markets, the value factor continues to exhibit significant influence within the Chinese A-shares market. This finding suggests that prematurely dismissing the importance of value factors based on their performance in other markets may be misguided. This research highlights the continued relevance of value investing principles within the unique context of the Chinese market.

---

### 评论 #30 (作者: AK98027, 时间: 1年前)

This paper contributes to the ongoing debate regarding the existence and persistence of the value premium in asset pricing models. Recent research, including the work of Fama and French (2015), has suggested that the value premium may be less pronounced or even redundant in the U.S. market. However, this study challenges this perspective by demonstrating the continued significance of the value factor in explaining stock returns within the Chinese A-shares market.

---

### 评论 #31 (作者: AK98027, 时间: 1年前)

Redundancy of Value Premium: The paper suggests that the value factor should not be dismissed outright, even though its performance has been questioned in other markets, particularly in the U.S. The findings indicate that value remains a relevant and non-redundant factor for pricing stock returns in the Chinese A-shares market.

---

### 评论 #32 (作者: AK98027, 时间: 1年前)

A central debate in current asset pricing research revolves around the persistence of the value premium and the continued relevance of traditional value factors. This study contributes to this discussion by demonstrating the continued significance of value factors in the Chinese A-shares market. These findings underscore the importance of conducting region-specific analyses when evaluating the role of value in asset pricing, as its importance may vary across different market contexts.

---

### 评论 #33 (作者: AK98027, 时间: 1年前)

I am Hoping that this  summary is helpful for you, if you have any more questions, such as how data is processing, or how variable is contructing, or how parameter is determining, I will provide more summary, and some ideas how apply them in WQBrain platform.

Thanking You

---

### 评论 #34 (作者: TN10210, 时间: 1年前)

How do you think the findings from the study on China's A-shares market can influence asset pricing models in other emerging markets with different economic structures and regulations?  [TN51777](/hc/en-us/profiles/17875512568599-TN51777)

---

### 评论 #35 (作者: VK91272, 时间: 1年前)

This paper contributes to the ongoing debate regarding the existence and persistence of the value premium in asset pricing models.

---

### 评论 #36 (作者: TN51777, 时间: 1年前)

[CD94009](/hc/en-us/profiles/6059930277783-CD94009) : "How does the modified six-factor model differ from the original q-factor model?"

The modified six-factor model includes additional factors tailored to the Chinese A-shares market, which are more relevant to its unique characteristics. Unlike the q-factor model, which is U.S.-centric, the six-factor model adjusts for local factors such as earnings-based value, market conditions, and investor behavior specific to China.

---

### 评论 #37 (作者: TN51777, 时间: 1年前)

[TN10210](/hc/en-us/profiles/21908956565655-TN10210)

The findings from the study on China’s A-shares market suggest that asset pricing models need to be tailored to local market conditions. For emerging markets with different economic structures and regulations, this means relying on custom models rather than universal ones. The study shows that factors like government intervention, market structure, and transaction costs can significantly influence model performance. For instance, higher transaction costs in emerging markets may make simpler models (e.g., market, size, earnings-based value) more effective.

---

### 评论 #38 (作者: TN51777, 时间: 1年前)

Additionally, regulatory factors and data limitations may require emerging markets to develop pricing models using local data and advanced techniques, such as machine learning, to capture market-specific dynamics. Overall, this study highlights the importance of adapting models to the unique characteristics of each emerging market.

---

### 评论 #39 (作者: PT82759, 时间: 1年前)

Thank you for sharing this very insightful paper! I completely agree that models need to be adjusted to suit the specific characteristics of each market.

May I ask you this: Could you clarify how you calculated transaction costs and how they affected the choice of the model?

---

### 评论 #40 (作者: PT55616, 时间: 1年前)

Which country you applied this strategy? is it work more in which country? USA or EUR? with me momentum data work more in ASI country such as HKG, TWN but I don't know how to apply in others

---

### 评论 #41 (作者: UN28170, 时间: 1年前)

The paper  *"Factor Models for Chinese A-Shares"*  examines the effectiveness of various asset pricing models in China’s segmented equity market. The study finds that U.S.-developed models, such as the Fama-French three- and five-factor models, fail to adequately explain Chinese stock returns. Instead, a tailored four-factor model, incorporating a market, size, and earnings-based value factor, outperforms conventional models. A Bayesian approach suggests a seven-factor model, but transaction cost adjustments favor a simpler three-factor model. The findings highlight the importance of localized factor models in emerging markets, challenging assumptions that global pricing models apply universally

---

### 评论 #42 (作者: DK30003, 时间: 1年前)

- Challenges in Factor Models: The rise of numerous asset pricing factors, often seen as "spurious," has prompted research to examine their validity in less financially integrated markets like China. This is crucial to distinguish real factors from statistical anomalies and refine asset pricing models beyond traditional frameworks like CAPM and the Fama-French three-factor model.
  10

---

### 评论 #43 (作者: XD81759, 时间: 1年前)

Hey TN51777, sounds great you're sharing insights on Chinese A - shares factor models. You're spot - on that each market has its own quirks. When it comes to these models, the tailored ones for China seem to outperform US - originated ones. For the data - driven seven - factor model, it's crucial to understand how the data is processed. Looking forward to your summary of key points. It'll surely help us better grasp the implementation and improve our alpha for Chinese A - shares.

---

### 评论 #44 (作者: HT59568, 时间: 1年前)

How do transaction costs in China’s market (e.g., stamp duty, circuit breakers) flip the ranking of asset pricing models and Can the  `trade_when()`  operator mitigate turnover issues in CHN Alphas targeting earnings-based value factors?

---

### 评论 #45 (作者: HT59568, 时间: 1年前)

How do short-selling restrictions in China impact the effectiveness of long-short neutralized Alphas?

---

### 评论 #46 (作者: IW96661, 时间: 1年前)

I had a problem submitting analyzing China market but now i have an idea. It seemed so tricky until this was explained.

---

