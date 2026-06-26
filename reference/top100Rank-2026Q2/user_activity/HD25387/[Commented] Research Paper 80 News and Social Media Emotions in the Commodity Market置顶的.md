# Research Paper 80: News and Social Media Emotions in the Commodity Market置顶的

- **链接**: [Commented] Research Paper 80 News and Social Media Emotions in the Commodity Market置顶的.md
- **作者**: NL41370
- **发布时间/热度**: 1年前, 得票: 16

## 帖子正文

Abstract:

Emotion plays a significant role in both institutional and individual investors’ decision-making process. However, there is a lack of empirical evidence available that addresses how investors’ emotions affect commodity market returns. This study examines the short-term predictive power of media-based emotion indices on the following five days’ commodity returns. The research adopts a proprietary dataset of commodity specific market emotions, which is computed based on a comprehensive textual analysis of sources from newswires, Internet news sources, and social media. Time series econometrics models (Threshold-GARCH and VAR) are employed to analyze fourteen years (01/1998-12/2011) of daily observations of the CRB commodity market index, crude oil and gold returns, and the market-level sentiment and emotions (optimism, fear, and joy).

The empirical results suggest that the commodity specific emotions (optimism, fear, and joy) have significant influence on individual commodity returns, but not on commodity market index returns. Additionally, the research findings support the short-term predictability of the commodity specific emotions on the following five days’ individual commodity returns. Compared to the previous studies of news sentiment on commodity returns (Borovkova, 2011; Borovkova and Mahakena, 2015; Smales, 2014), our research provides further evidence of the effects of news and social media based emotions (optimism, fear and joy) in the commodity market. Additionally, we propose that market emotion incorporates both a sentimental effect and appraisal effect on commodity returns. Empirical results are shown to support both the sentimental effect and appraisal effect when market sentiment is controlled in crude oil and gold spot markets.

Author: Jiancheng Shen, Mohammad Najand, Wu He, Feng Dong

Year: 2017

Link:  [News and Social Media Emotions in the Commodity Market by Jiancheng Shen, Mohammad Najand, Feng Dong, Wu He :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2964301)

Key ideas and Comments from WorldQuant:

Page 9 Paragraph 1

Page 19 Paragraph 1

**Term**

**Data field**

**Dataset**

optimism

fnd90_game_optimism_sale

[Governance, Accounting, Management, and Equality](https://platform.worldquantbrain.com/data/data-sets/fundamental90?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

fear

nws3_scores_fearnormscr

[Dow Jones News Analytics Data](https://platform.worldquantbrain.com/data/data-sets/news3?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

---

## 讨论与评论 (67)

### 评论 #1 (作者: TT55495, 时间: 1年前)

Hello. I have a question and would like to ask for your advice. I find that in order to convert from paper idea to alpha, the signal is often not very good, and when optimizing, it is likely to lead to overfitting. On the contrary, when looking directly at the data on Brain and combining operators without going through the idea paper, I find that the signal is better and less overfitting. Could you please advise me on which direction to take for alpha?

---

### 评论 #2 (作者: RA30956, 时间: 1年前)

This study highlights the predictive power of media-based emotions like optimism, fear, and joy on individual commodity returns, particularly for crude oil and gold. Insights on  **Page 9 Paragraph 1**  and  **Page 19 Paragraph 1**  emphasize the role of sentimental and appraisal effects, supported by datasets like fnd90_game_optimism_sale and nws3_scores_fearnormscr. It’s a valuable contribution to understanding emotion-driven market dynamics.

---

### 评论 #3 (作者: RA30956, 时间: 1年前)

The insights on  **Page 9 Paragraph 1**  and  **Page 19 Paragraph 1**  provide a strong basis for understanding how sentimental and appraisal effects influence short-term commodity returns, particularly for crude oil and gold. Could you elaborate further on how these findings align with the predictive power of media-based emotion indices over the five-day horizon?

---

### 评论 #4 (作者: DK20528, 时间: 1年前)

This paper, presents a fascinating perspective on the role of emotional sentiment in influencing commodity market movements. The integration of textual analysis from news and social media to quantify emotions and their impact on market dynamics is particularly intriguing, as it bridges behavioral finance with computational techniques.

However, I had a couple of doubts:

1. How are the emotional scores from social media and news quantified in this study? Did the methodology distinguish between different sources (e.g., professional news outlets vs. individual social media users), and were there differences in their predictive power?
2. Was there any consideration of the temporal decay of emotional impact? For instance, do emotions derived from news/social media have a short-term influence, or do they also correlate with longer-term trends in the commodity market?

Looking forward to understanding these aspects better.

---

### 评论 #5 (作者: SJ17125, 时间: 1年前)

The study emphasizes the combined sentimental and appraisal effects of market emotions, adding to previous research on sentiment and its impact on commodity markets. These insights provide a more nuanced understanding of investor behavior and market movements influenced by emotional factors.

Thanks for sharing 🙏

---

### 评论 #6 (作者: HV77283, 时间: 1年前)

This study highlights the combined sentimental and appraisal effects of market emotions, expanding on prior research on sentiment’s impact on commodity markets. These insights offer a deeper understanding of how emotional factors influence investor behavior and market movements. Thanks for sharing!

---

### 评论 #7 (作者: XL31477, 时间: 1年前)

**Hey,  [TT55495](/hc/en-us/profiles/13132630342807-TT55495) . Both ways have their merits. Going from paper ideas might face overfitting issues during optimization, but it's based on solid theories. While directly working with data on Brain and combining operators can give good signals sometimes. I'd say you could try combining them. Use the paper ideas as a base, understand the concepts like sentimental and appraisal effects well. Then, when working on Brain, use those ideas to guide your operator combinations and data exploration. That way, you might get good alphas with less overfitting.**

---

### 评论 #8 (作者: AK98027, 时间: 1年前)

The study emphasizes the combined sentimental and appraisal effects of market emotions, adding to previous research on sentiment and its impact on commodity markets.

Thanks for your valuable insights

---

### 评论 #9 (作者: AC63290, 时间: 1年前)

The study explores the role of media-based emotions (optimism, fear, and joy) in predicting short-term commodity returns. Using a proprietary dataset and models like Threshold-GARCH and VAR, the research demonstrates the significant impact of these emotions on individual commodities like crude oil and gold, though not on broader market indices. WorldQuant highlights data fields  `fnd90_game_optimism_sale`  (optimism) and  `nws3_scores_fearnormscr`  (fear) for replicating insights. Results emphasize the sentimental and appraisal effects of market emotions, advancing prior studies by showing their predictive power over five-day returns. These findings offer actionable strategies for leveraging emotional metrics in commodity market investments.

---

### 评论 #10 (作者: XD81759, 时间: 1年前)

Hey, that's an interesting research paper! It shows how emotions from news and social media can impact commodity returns. The key is those specific emotions like optimism, fear, and joy matter for individual commodity returns. When building quant factors related to this, we could consider using these emotion indices as inputs. For example, maybe a factor based on the difference between optimism and fear levels to predict future returns. But gotta make sure the data fields like fnd90_game_optimism_sale and nws3_scores_fearnormscr are properly utilized and analyzed.

---

### 评论 #11 (作者: BA51127, 时间: 1年前)

The discussion on Research Paper 80, "News and Social Media Emotions in the Commodity Market," sheds light on the influential role of investor emotions derived from news and social media on commodity market returns.

For those looking to translate these findings into alpha generation, consider these points:

1. **Emotional Metrics as Inputs** : Use emotional indices, such as optimism and fear levels, as inputs for your alpha models. These metrics can provide insights into market sentiment that traditional financial data might not capture.
2. **Sentiment Analysis** : Analyze the sentiment behind news and social media posts to predict short-term commodity price movements. This approach can offer a unique perspective on market dynamics.
3. **Combining Theoretical and Empirical Approaches** : While theoretical insights from papers provide a solid foundation, combining them with empirical data exploration can lead to more robust alpha strategies.
4. **Data Field Utilization** : Properly utilize and analyze data fields like  `fnd90_game_optimism_sale`  for optimism and  `nws3_scores_fearnormscr`  for fear to enhance your alpha's predictive power.

By integrating emotional sentiment analysis with traditional quantitative methods, you can potentially develop alpha strategies that better capture the nuances of market movements driven by investor emotions.

---

### 评论 #12 (作者: LR13671, 时间: 1年前)

This research provides a compelling look at how media-based emotions, such as optimism, fear, and joy, influence short-term commodity returns, particularly for crude oil and gold. The use of proprietary datasets like fnd90_game_optimism_sale (optimism) and nws3_scores_fearnormscr (fear) adds depth to the analysis.

For those seeking to leverage these insights, consider:

1. **Emotional Sentiment Metrics:**  Integrate emotional indices into alpha models to capture non-traditional drivers of commodity returns.
2. **Temporal Analysis:**  Explore the decay rates of emotional impacts—how long emotions from news and social media influence market trends.
3. **Dataset Optimization:**  Ensure a nuanced approach when analyzing data fields to mitigate overfitting risks, balancing theoretical frameworks with empirical data exploration.

These findings bridge behavioral finance and computational analytics, offering a robust foundation for designing predictive models in commodity markets.

---

### 评论 #13 (作者: DN45758, 时间: 1年前)

Thank you for sharing this insightful paper! The integration of emotional sentiment analysis with commodity markets is fascinating. Exploring how emotions are quantified, differentiated by source, and their temporal effects adds depth to understanding market dynamics. I appreciate this innovative perspective and look forward to further discussions on this topic.

---

### 评论 #14 (作者: SJ17125, 时间: 1年前)

Hiii  [DK20528](/hc/en-us/profiles/24602396283031-DK20528)

In the context of financial markets, the study likely quantifies emotional scores from social media and news using  **natural language processing (NLP)**  techniques tailored to financial sentiment analysis. These methods evaluate the sentiment and emotional tone (e.g., optimism, fear, uncertainty) of text data. Tools such as  **VADER** ,  **Loughran-McDonald sentiment dictionaries** , or advanced models like  **FinBERT**  may have been used to extract sentiment scores specific to financial language.

I hope it helps.

---

### 评论 #15 (作者: PN39025, 时间: 1年前)

Thank you for sharing such a comprehensive and actionable guide—it’s a treasure trove of ideas for consultants looking to explore new avenues in Alpha creation. The combination of readability and sentiment data opens up exciting possibilities for creating innovative Alphas. Great work.

---

### 评论 #16 (作者: CC40930, 时间: 1年前)

The study reinforces the importance of  **investor emotions**  in predicting  **commodity returns** , particularly in the short term. It suggests that a  **sentiment-based approach**  could be a valuable addition to a broader  **quantitative alpha generation strategy** , especially by focusing on emotion-driven price movements in individual commodities like  **crude oil**  and  **gold** . By incorporating  **social media and news sentiment**  into alpha models, investors may gain a more nuanced understanding of the market's psychological state, which can lead to improved prediction and potentially higher returns.

---

### 评论 #17 (作者: VP21767, 时间: 1年前)

This research investigates the influence of media-driven emotions (optimism, fear, and joy) on commodity market returns, using a proprietary dataset and time series models over 14 years. It finds that emotions significantly affect individual commodity returns like crude oil and gold, but not overall market indices. The study underscores the short-term predictability of emotions, highlighting both sentimental and appraisal effects, and provides deeper insights into the relationship between market sentiment and commodity performance.

---

### 评论 #18 (作者: HD25387, 时间: 1年前)

**Thanks for sharing this fascinating research!**

The role of emotions like optimism, fear, and joy in predicting commodity returns is intriguing. A few thoughts and questions:

1. **Short-Term Predictability:**
   - The study highlights short-term predictability for individual commodity returns over five days. Has anyone tested similar emotion-based signals in equity or FX markets?
2. **Emotions and Volatility:**
   - Using models like Threshold-GARCH, how effectively can emotions like fear predict spikes in volatility, especially in commodities like crude oil?
3. **Sentiment Dynamics:**
   - Combining sentiment scores with volume or price momentum data might enhance signal robustness. Has anyone explored such hybrid models?

Looking forward to hearing how others are leveraging sentiment-driven strategies in their Alpha development. Thanks again for sharing this valuable paper! 🚀

---

### 评论 #19 (作者: LY88401, 时间: 1年前)

Your article is excellently written! The ideas are clear, engaging, and well-organized. You have a remarkable ability to present complex topics in a simple, accessible way. It’s an insightful and thought-provoking read that reflects your deep understanding and expertise.

---

### 评论 #20 (作者: TT55495, 时间: 1年前)

Thank you for sharing this interesting research on the role of emotions in commodity market returns. The findings on the influence of optimism, fear, and joy provide significant insight into the emotional dynamics that affect commodity-specific returns. I look forward to exploring more about how emotions are integrated into predictive models for market behavior.

---

### 评论 #21 (作者: KS69567, 时间: 1年前)

The study highlights the intricate interplay between sentimental and appraisal effects of market emotions, offering deeper insights into how emotional factors shape investor behavior and influence commodity market dynamics. These findings enhance our understanding of the role of emotions in financial decision-making, building on prior research to provide a more comprehensive perspective on market movements.

---

### 评论 #22 (作者: SV11672, 时间: 1年前)

"Excellent study on the impact of emotions on commodity market returns! The use of media-based emotion indices and textual analysis of news and social media sources provides a unique perspective on the role of emotions in investor decision-making. The findings that commodity-specific emotions (optimism, fear, and joy) have a significant influence on individual commodity returns, but not on commodity market index returns, are particularly interesting. The study's contribution to the literature on the effects of news and social media-based emotions on commodity returns is significant, and the proposal that market emotion incorporates both sentimental and appraisal effects is a valuable addition to the field."

---

### 评论 #23 (作者: SV11672, 时间: 1年前)

"Very insightful analysis of the emotional drivers of commodity market returns! The study's use of advanced econometric models and a comprehensive dataset adds credibility to the findings. The distinction between sentimental and appraisal effects of market emotion is particularly useful, and the results suggest that both effects play a significant role in shaping commodity returns. The study's implications for investors and policymakers are significant, highlighting the need to consider the emotional aspects of market behavior when making decisions."

---

### 评论 #24 (作者: AT56452, 时间: 1年前)

The study investigates the influence of investor emotions—specifically optimism, fear, and joy—on commodity market returns, focusing on individual commodities like crude oil and gold, as well as the broader CRB commodity market index. By analyzing data from January 1998 to December 2011, the research employs time series econometric models, including Threshold-GARCH and VAR, to assess the predictive power of media-based emotion indices over subsequent five-day commodity returns.

---

### 评论 #25 (作者: AT56452, 时间: 1年前)

Investor emotions significantly impact decision-making processes in financial markets. Emotions such as optimism, fear, and joy can drive investment choices, influencing market dynamics and asset pricing. Understanding these emotional drivers is crucial for comprehending market behavior, as they can lead to phenomena like bubbles or crashes when collective sentiments shift. This study delves into how such emotions, as reflected in media sources, affect commodity returns, highlighting the importance of psychological factors in financial decision-making.

---

### 评论 #26 (作者: AT56452, 时间: 1年前)

Media-based emotion indices are quantitative measures derived from textual analysis of news articles, social media posts, and other online content. These indices capture the prevailing sentiments—optimism, fear, joy—expressed in media sources. By aggregating and analyzing these sentiments, researchers can gauge the market's emotional state, providing insights into potential market movements. In this study, such indices are used to predict short-term commodity returns, demonstrating their utility in financial analysis.

---

### 评论 #27 (作者: AT56452, 时间: 1年前)

The study utilizes advanced econometric models to analyze the data. The Threshold Generalized Autoregressive Conditional Heteroskedasticity (Threshold-GARCH) model captures volatility clustering and asymmetries in financial time series, accounting for different responses to positive and negative shocks. The Vector Autoregression (VAR) model analyzes the interdependencies among multiple time series, allowing for the examination of how changes in one variable affect others over time. These models are instrumental in understanding the dynamic relationship between media-based emotions and commodity returns.

---

### 评论 #28 (作者: AT56452, 时间: 1年前)

The research analyzes daily observations spanning fourteen years, from January 1998 to December 2011. It focuses on the CRB commodity market index, crude oil, and gold returns. This extensive dataset enables a comprehensive examination of long-term trends and patterns, providing robust insights into how media-based emotions influence commodity markets over time.

---

### 评论 #29 (作者: AT56452, 时间: 1年前)

Empirical results indicate that commodity-specific emotions—optimism, fear, and joy—significantly influence individual commodity returns, particularly for crude oil and gold. Positive emotions like optimism and joy can drive prices up, while negative emotions such as fear may lead to price declines. This underscores the sensitivity of individual commodities to market emotions, suggesting that investors' sentiments, as reflected in media, play a crucial role in price determination.

---

### 评论 #30 (作者: AT56452, 时间: 1年前)

Interestingly, the study finds that these emotions do not significantly affect the broader CRB commodity market index returns. This may be due to the diversification within the index, which includes a variety of commodities whose individual emotional influences may offset each other. As a result, the aggregate effect of emotions on the index is diminished, highlighting the complexity of predicting market-wide movements based on sentiment analysis.

---

### 评论 #31 (作者: AT56452, 时间: 1年前)

The research supports the short-term predictability of commodity-specific emotions on subsequent five-day individual commodity returns. By analyzing media-based emotion indices, investors and analysts can anticipate short-term price movements, potentially enhancing trading strategies. This finding emphasizes the value of incorporating sentiment analysis into market analysis, particularly for short-term investment horizons.

---

### 评论 #32 (作者: AT56452, 时间: 1年前)

This study builds upon previous research by Borovkova (2011), Borovkova and Mahakena (2015), and Smales (2014), which examined news sentiment's impact on commodity returns. By focusing specifically on emotions like optimism, fear, and joy, and utilizing a proprietary dataset, this research provides further evidence of the nuanced effects of media-based emotions in the commodity market, offering a more detailed understanding of sentiment's role in financial markets.

---

### 评论 #33 (作者: AT56452, 时间: 1年前)

The study proposes that market emotion incorporates both sentimental and appraisal effects on commodity returns. The sentimental effect refers to the direct impact of emotions on market behavior, while the appraisal effect involves the cognitive evaluation of information that influences emotional responses. Empirical results support both effects, suggesting that emotions and their underlying cognitive appraisals play a role in shaping commodity market dynamics.

---

### 评论 #34 (作者: AT56452, 时间: 1年前)

When controlling for overall market sentiment, the study finds that both sentimental and appraisal effects remain significant in crude oil and gold spot markets. This indicates that individual commodity returns are influenced by specific emotions beyond general market sentiment, highlighting the importance of analyzing commodity-specific emotions for more accurate predictions.

---

### 评论 #35 (作者: AT56452, 时间: 1年前)

The proprietary dataset used in the study is computed based on comprehensive textual analysis of sources from newswires, internet news sources, and social media. This approach allows for the extraction of nuanced emotional content from a wide range of media, providing a more accurate representation of market emotions. The use of advanced text mining techniques enables the quantification of emotions, facilitating their incorporation into econometric models.

---

### 评论 #36 (作者: AT56452, 时间: 1年前)

Understanding the influence of media-based emotions on commodity returns can aid investors in making more informed decisions.

---

### 评论 #37 (作者: HT59568, 时间: 1年前)

How do optimism, fear, and joy influence individual commodity returns differently from commodity market index returns and what evidence supports the short-term predictive power of media-based emotion indices on five days' commodity returns?

---

### 评论 #38 (作者: HT59568, 时间: 1年前)

## **Proprietary dataset application**

How does the proprietary dataset of market emotions improve our understanding of the relationship between emotions and commodity returns?

---

### 评论 #39 (作者: HT59568, 时间: 1年前)

## **Impact of news and social media**

What unique insights does this study offer about the influence of news and social media emotions compared to earlier studies?

---

### 评论 #40 (作者: HT59568, 时间: 1年前)

## **Sentimental and appraisal effects**

How do sentimental and appraisal effects differ in their impact on crude oil and gold returns?

---

### 评论 #41 (作者: HT59568, 时间: 1年前)

## **Threshold-GARCH and VAR models**

Why are Threshold-GARCH and VAR models particularly suitable for analyzing the influence of emotions on commodity returns?

---

### 评论 #42 (作者: HT59568, 时间: 1年前)

## **Crude oil and gold market sentiment**

How does controlling for market sentiment validate the sentimental and appraisal effects in crude oil and gold spot markets?

---

### 评论 #43 (作者: HT59568, 时间: 1年前)

## **Media-based emotion indices**

How do media-based emotion indices differ from traditional market sentiment measures in predicting commodity returns?

---

### 评论 #44 (作者: HT59568, 时间: 1年前)

## **Temporal dynamics of emotions**

What temporal patterns in emotions (optimism, fear, and joy) are significant for understanding commodity price movements?

---

### 评论 #45 (作者: HT59568, 时间: 1年前)

## **Commodity-specific vs. market-level emotions**

Why do commodity-specific emotions have a stronger impact on individual commodity returns than on the commodity market index?

---

### 评论 #46 (作者: AK98027, 时间: 1年前)

The study emphasizes the combined sentimental and appraisal effects of market emotions, adding to previous research on sentiment and its impact on commodity markets. These insights provide a more nuanced understanding of investor behavior and market movements influenced by emotional factors.
Thanks for sharing 🙏

---

### 评论 #47 (作者: AK98027, 时间: 1年前)

This research investigates the influence of investor emotions, specifically optimism, fear, and joy, on commodity market returns. Focusing on individual commodities like crude oil and gold, as well as the broader CRB commodity market index, the study analyzes data from 1998 to 2011. Employing time series econometric models such as Threshold-GARCH and VAR, the research aims to determine whether media-based emotion indices can predict subsequent five-day commodity returns.

---

### 评论 #48 (作者: AK98027, 时间: 1年前)

By examining the relationship between investor emotions and commodity price movements, the study seeks to understand potential emotional contagion effects, volatility dynamics, and the potential for developing improved investment strategies and risk management techniques in the commodity market.

---

### 评论 #49 (作者: AK98027, 时间: 1年前)

Sentimental and appraisal effects likely differ in their impact on crude oil and gold returns due to their distinct characteristics as commodities.

- **Crude Oil:**
  - **Supply and Demand:**  Crude oil prices are heavily influenced by global economic growth, geopolitical events  and OPEC production decisions.
  - **Sentiment:**  Sentimental effects, driven by fear or optimism about the global economy, may have a stronger impact on crude oil. For example, fear of a recession could lead to decreased demand for oil, driving prices down. Conversely, optimism about economic growth could increase demand and push prices higher.
  - **Appraisal Effects:**  Appraisal effects, related to the perceived value or attractiveness of the commodity, might play a lesser role.
- **Gold:**
  - **Safe-Haven Asset:**  Gold is often considered a safe-haven asset during times of economic uncertainty, geopolitical turmoil, and inflation.
  - **Sentiment:**  Fear and uncertainty, driven by geopolitical events or economic downturns, can significantly increase demand for gold as investors seek a safe haven for their assets.
  - **Appraisal Effects:**  Appraisal effects might be more pronounced for gold. For example, if investors perceive gold as undervalued or believe its price will rise due to increased inflation, they may increase demand, driving prices higher.

---

### 评论 #50 (作者: AK98027, 时间: 1年前)

Threshold-GARCH and VAR models are particularly suitable for analyzing the influence of emotions on commodity returns due to their specific characteristics that align with the complexities of this research:

- **Threshold-GARCH:**
  - **Captures Volatility Clustering:**  Commodity markets exhibit periods of high volatility interspersed with periods of relative calm. Threshold-GARCH models are well-suited to capture this volatility clustering behavior, allowing for the identification of regimes (e.g., high volatility vs. low volatility) and how investor emotions might influence these regimes.
  - **Asymmetric Effects:**  Emotions like fear can have asymmetric effects on volatility. For instance, bad news may lead to a larger increase in volatility than good news of the same magnitude. Threshold-GARCH models can capture these asymmetries, providing a more nuanced understanding of the impact of emotions on price fluctuations.
- **VAR (Vector Autoregression):**
  - **Dynamic Interrelationships:**  VAR models can effectively capture the dynamic interrelationships between multiple variables, including commodity returns, investor emotions (optimism, fear, joy), and potentially other relevant factors (e.g., economic indicators, geopolitical events). This allows for a comprehensive analysis of how emotions interact with other variables to influence commodity prices.
  - **Forecasting:**  VAR models can be used to generate forecasts of future commodity returns based on current and past values of emotions and other relevant variables. This forecasting capability is valuable for investors and market participants

---

### 评论 #51 (作者: LY88401, 时间: 1年前)

The study highlights that market emotions influence commodity returns through two key mechanisms: the sentimental effect and the appraisal effect. The sentimental effect captures the direct influence of emotions on market behavior, while the appraisal effect reflects how cognitive evaluations of information shape emotional reactions. 📊🧠 Empirical findings confirm the significance of both effects, demonstrating that emotions and their cognitive underpinnings are integral to understanding commodity market dynamics. 🌟📈

---

### 评论 #52 (作者: LR13671, 时间: 1年前)

The study's nuanced approach to incorporating both sentimental and appraisal effects in understanding commodity returns is noteworthy. The proprietary datasets and focus on short-term predictability add depth to the analysis. It would be interesting to see how temporal decay or the varying reliability of news versus social media sources impact the robustness of these findings.

---

### 评论 #53 (作者: KK81152, 时间: 1年前)

this study suggests that the emotions expressed in media—such as optimism, fear, and joy—can help predict short-term price movements in individual commodities like crude oil and gold. Traders and investors could use emotion-based indicators derived from news and social media to anticipate price changes in the following days. However, these emotions don't seem to affect the broader commodity market index. This insight can be useful for developing trading strategies that leverage market sentiment for more accurate short-term forecasts.

---

### 评论 #54 (作者: LY88401, 时间: 1年前)

This study highlights how emotions in the media—like optimism, fear, and joy—can serve as predictors for short-term price shifts in individual commodities such as crude oil and gold. 📉📈 Traders and investors might leverage emotion-based signals from news and social media to forecast price changes in the days ahead. However, these emotional cues don’t appear to influence broader commodity market indices. 🌐 This finding opens doors to crafting trading strategies that harness market sentiment for sharper short-term predictions. 🚀

---

### 评论 #55 (作者: PN39025, 时间: 1年前)

I have done alpha related to News and Social Media data but there is one point that makes me quite confused when submitting, which is using the test period of the years, I see that it changes quite a lot. Sometimes in 2019, Sharpe was positive 4 but in 2020 it dropped to -5 and in 2021 it went up to 3. Is there any way to neutralize high performance and still maintain stability?

---

### 评论 #56 (作者: SK78969, 时间: 1年前)

This research offers fascinating insights into the influence of emotions on commodity returns, highlighting the predictive power of optimism, fear, and joy in the short term. The distinction between the sentimental and appraisal effects is particularly intriguing—this layered approach adds depth to understanding emotion-driven market dynamics.

How do you think advancements in real-time sentiment analysis and AI could further refine emotion-based models? Could incorporating more granular data sources, like live social media feeds, enhance the accuracy of predictions for commodities like crude oil and gold?

---

### 评论 #57 (作者: SV11672, 时间: 1年前)

"Overall, a well-designed and informative study that sheds new light on the complex relationship between emotions and commodity markets!"

---

### 评论 #58 (作者: PP87148, 时间: 1年前)

### **Emotion Carryover Effect**

**Hypothesis** : Emotions from the past three days predict current crude oil returns.
 **Expression** :  `rank(ts_sum(fear_index, 3) + ts_sum(optimism_index, 3))`

---

### 评论 #59 (作者: AK62822, 时间: 1年前)

This research provides a compelling look at how media-based emotions, such as optimism, fear, and joy, influence short-term commodity returns, particularly for crude oil and gold. The use of proprietary datasets like fnd90_game_optimism_sale (optimism) and nws3_scores_fearnormscr (fear) adds depth to the analysis.

---

### 评论 #60 (作者: DK30003, 时间: 1年前)

This adaptive approach could lead to better risk management and more stable returns over time. Additionally, the emphasis on accounting for transaction costs and liquidity is a crucial reminder of real-world trading challenges. Looking forward to diving deeper into these concepts for refining my own strategies!

---

### 评论 #61 (作者: PT55616, 时间: 1年前)

New data normally have high turnover, such as more than 80%, which cannot apply normally to produce alpha. could you share some technique how can you reduce your turnover?

---

### 评论 #62 (作者: AK40989, 时间: 1年前)

The interplay between media-based emotions and commodity returns is indeed a game-changer for understanding market dynamics. It’s interesting to see how the study differentiates between individual commodities and the overall market index, suggesting that emotional sentiment might have a more pronounced effect on specific assets like crude oil and gold. How might we further refine our models to account for the varying impacts of different emotional sources, especially considering the potential differences in influence between professional news outlets and social media?

---

### 评论 #63 (作者: DK30003, 时间: 1年前)

**Page 19 Paragraph 1**  emphasize the role of sentimental and appraisal effects, supported by datasets like fnd90_game_optimism_sale and nws3_scores_fearnormscr. It’s a valuable contribution to understanding emotion-driven market dynamics.

---

### 评论 #64 (作者: RS70387, 时间: 1年前)

The study’s findings on short-term predictability raise an interesting question, do these emotion-based signals represent inefficiencies that can be systematically exploited, or do they decay quickly? Additionally, how might sentimental and appraisal effects vary across market conditions, and could AI-driven real-time sentiment analysis enhance predictive power?

---

### 评论 #65 (作者: SD92473, 时间: 1年前)

This research effectively demonstrates how media-derived emotions (optimism, fear, joy) can predict individual commodity returns but not broader indices. By distinguishing between sentimental and appraisal effects, it advances our understanding beyond simple sentiment analysis, offering potential applications for trading strategies.

---

### 评论 #66 (作者: UN28170, 时间: 1年前)

This study examines the influence of investor emotions—optimism, fear, and joy—on commodity market returns using a proprietary dataset from Thomson Reuters MarketPsych Indices. Analyzing 14 years of data (1998–2011) with time-series econometric models (Threshold-GARCH and VAR), the research finds that these emotions significantly impact individual commodities like crude oil and gold but not the overall commodity index. Additionally, emotions demonstrate short-term predictive power for commodity returns. The study highlights the dual role of emotions: a sentimental effect influencing noise trading and an appraisal effect shaping rational investment decisions. The findings provide insights for risk management and trading strategies.

---

### 评论 #67 (作者: GO84876, 时间: 1年前)

*This paper provides strong empirical support for integrating emotion-based signals from media into short-term commodity return prediction, especially for crude oil and gold. The authors effectively differentiate between market-level and commodity-specific emotional impacts using a robust 14-year dataset and econometric modeling. Their findings on the sentimental and appraisal effects are especially noteworthy and open up alpha generation possibilities using emotion indices such as  `fnd90_game_optimism_sale`  and  `nws3_scores_fearnormscr`  in a short-horizon framework. This work also validates the unique predictive power of commodity-specific emotions, an angle less explored in previous sentiment literature.*

---

