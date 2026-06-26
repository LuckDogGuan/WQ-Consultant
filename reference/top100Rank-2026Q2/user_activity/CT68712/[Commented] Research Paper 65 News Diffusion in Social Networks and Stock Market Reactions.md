# Research Paper 65: News Diffusion in Social Networks and Stock Market Reactions

- **链接**: [Commented] Research Paper 65 News Diffusion in Social Networks and Stock Market Reactions.md
- **作者**: KA64574
- **发布时间/热度**: 2年前, 得票: 12

## 帖子正文

We study how the social transmission of public news influences investors' beliefs and securities markets. Using data on investor social networks, we find that earnings announcements from firms in higher-centrality locations generate stronger immediate price, volatility, and trading volume reactions. Post announcement, such firms experience weaker price drift and faster volatility decay but higher and more persistent volume. This evidence suggests that greater social connectedness promotes timely incorporation of news into prices, but also opinion divergence and excessive trading. We propose the social churning hypothesis and present supporting evidence with granular data from StockTwits messages and household trading records.

Author : David A. Hirshleifer, Lin Peng, Qiguang Wang

Year : 2021

Link :  **[https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3824022](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3824022)**

**Key ideas and Comments from WorldQuant:**

- Page 5 paragraph 3
- Page 6 paragraph 3
- Page 24 paragraph 2
- Page 34 paragraph 4

**Term**

**Data field**

**Dataset**

Tweet volume

snt_social_volume

[**socialmedia8**](https://platform.worldquantbrain.com/data/data-sets/socialmedia8?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

Sentiment Z score

snt_social_value

[**socialmedia8**](https://platform.worldquantbrain.com/data/data-sets/socialmedia8?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

Sentiment volume

scl12_alltype_buzzvec

[**socialmedia12**](https://platform.worldquantbrain.com/data/data-sets/socialmedia12?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

---

## 讨论与评论 (50)

### 评论 #1 (作者: TN67143, 时间: 2年前)

Hi, can I summarize the paper in the following way:

1. Research question:

The author tried to study the causal relation between [social transmision of public news](cause) and [investors' beliefs] and [securities markets](effect).

2. Research data:

The author look at data on investor social networks to answer this question.

3. Research finding:

Firms in higher-centrality locations (characteristics)
generate stronger immediate price, volatility and trading volume reactions (trading results)

If we take the announcements time as a threshold, the such firms experience the following phenomenon:
a. weaker price drift
b. faster volatility decay
c. higher and more persistent volume.

Those phenomenon suggests the following causal relations:
greater social connectness promotes timely incorporation of news into three phenomenon:
a. prices
b. opinion divergence
c. excessive trading.

Based on the above evidence, the author propose
the social churning hypothesis
and presenting supporting evidences analyzed from
Stocktwits messages and household trading records.

What do you think of my summary?

Best regards,

---

### 评论 #2 (作者: AG20578, 时间: 2年前)

Hi!

Thank you for the summary, it is very well-structured.

Have you attempted to extract some idea from it to incorporate into the alpha?

---

### 评论 #3 (作者: TN67143, 时间: 2年前)

Great!

Thank you for your suggestion. I am trying to do so!

It would be great if we can find a way to translate the causal relation in this paper into concrete Alphas ideas! Can the following process work?

Firstly, the cause is social transmission of public news and social connectedness, which could be measured and represented by how much the stocks are discussed on social media, that may be captured by looking at Tweet volume (snt_social_value).

Secondly, the effect are prices, opinion divergence and excessive trading. Here, I am trying to find data fields that are on theme social media or news, therefore, we could look at sentiment Z score(snt_social_value) and sentiment volume (snt12_alltype_buzzvec) that tell us how the stocks is evaluated on social media using sentiment score.

Thirdly, to capture the causal relation, we may use operator that reflect the correlation or causal relationship such as ts_corr or ts_regression,...

Can you help me look at the above process? Thanks!

Best regards.

---

### 评论 #4 (作者: AG20578, 时间: 2年前)

Yes, the process sounds good 👍. You could consider incorporating geographic data available in the data explorer, such as zip codes or county codes. Grouping by these fields could further represent 'connectivity'. Additionally, you might want to consider the potential delay between cause and effect. The paper suggests that news are incorporated into prices in a timely manner, but you may want to experiment with different time lags.

---

### 评论 #5 (作者: BA51127, 时间: 1年前)

the process sounds good 👍. BUT, here's my take on the process you've outlined:

1. **Social Transmission Measurement** : You're correct that social media activity, particularly tweet volume and sentiment, can serve as a proxy for social transmission of public news. The data fields you've identified, such as  `snt_social_volume`  and  `snt_social_value` , are indeed relevant for capturing the volume and sentiment of stock discussions on platforms like StockTwits.
2. **Effect Variables** : The effects you've highlighted—price movement, opinion divergence, and trading volume—are well-aligned with the paper's findings. The data fields  `snt_social_value`  for sentiment Z-score and  `scl12_alltype_buzzvec`  for sentiment volume are good choices for gauging market sentiment on social media.
3. **Causal Relationship Operators** : Using operators like  `ts_corr`  or  `ts_regression`  to establish correlations or causal relationships is a strategic approach. These can help you quantify how changes in social media sentiment and volume precede or coincide with changes in stock prices and trading volumes.

---

### 评论 #6 (作者: DK20528, 时间: 1年前)

This article provides an insightful exploration of how news dissemination through social networks influences stock market behavior. By linking information diffusion with investor reactions, the authors contribute to the understanding of market efficiency and behavioral finance.

**Strengths:**

1. **Interdisciplinary Approach** : The study bridges social network theory and financial markets, shedding light on how the structure and dynamics of information flow impact stock prices.
2. **Behavioral Insights** : It highlights the role of investor psychology and collective behavior in amplifying or muting the effects of news on market movements.
3. **Practical Relevance** : Understanding how news spreads and influences asset prices is crucial for traders, policymakers, and regulators in managing risks associated with misinformation or herd behavior.

**Potential Areas for Further Development:**

1. **Empirical Validation** : Incorporating case studies or historical events (e.g., viral news stories) to demonstrate the relationship between news diffusion and market reactions would strengthen the study’s empirical basis.
2. **Network Analysis Details** : Providing more detail on the types of social networks analyzed (e.g., social media platforms, professional networks) and their characteristics could offer greater clarity and specificity.
3. **Impact of Misinformation** : Exploring how the spread of false or misleading news affects investor behavior and market efficiency would add depth to the analysis.
4. **Policy Implications** : Discussing how regulators could address challenges arising from rapid news diffusion, such as market manipulation or flash crashes, could enhance the practical value of the study.

This research makes a significant contribution to the growing field of information-driven finance, offering valuable insights into the interplay between social networks, news dissemination, and market dynamics.

---

### 评论 #7 (作者: SG76464, 时间: 1年前)

Thanks for the suggestion

---

### 评论 #8 (作者: XL31477, 时间: 1年前)

Your approach has merit. Using tweet volume and sentiment scores to represent social transmission and its effects is reasonable. However, as others pointed out, considering time lags is crucial as there's often a delay between cause and effect. Also, exploring more network details like different social media platforms used could make the analysis more precise. And don't forget to test various lag settings when using those operators for correlations. Overall, it's a good start but needs refinement for better alpha generation.

---

### 评论 #9 (作者: SJ17125, 时间: 1年前)

Hiii,

Thank you for your thoughtful and insightful comment. We greatly appreciate your recognition of the relevance and importance of this research.

---

### 评论 #10 (作者: RK48711, 时间: 1年前)

Thank you for your thoughtful and insightful comment. We appreciate your recognition of the relevance of this research, especially as ESG investing grows. Your suggestions for further development—such as clarifying stakeholder-friendly investments, comparing ESG and non-ESG funds, and exploring geographic/sectoral variations—are valuable. We also agree that studying the long-term impact of ESG investments would offer crucial insights. Your feedback is invaluable, and we will consider it as we continue exploring the effectiveness of ESG-driven investing. Thank you again for your engagement.

---

### 评论 #11 (作者: XD81759, 时间: 1年前)

The paper by Hirshleifer, Peng, and Wang (2021) studies how public news in social networks affects investors and markets. They find that earnings announcements from more central firms have stronger immediate impacts. Key data fields include tweet volume (snt_social_volume), sentiment Z score (snt_social_value), and sentiment volume (scl12_alltype_buzzvec). This research shows the importance of social connectedness in news diffusion and its effects on stock market reactions. It could be useful for understanding market dynamics and potentially for factor construction related to news sentiment and social media activity.

---

### 评论 #12 (作者: SJ17125, 时间: 1年前)

Hello everyone ,

thanks for your valuable comments and suggestions. it helped me a lot to built some quality alphas. thanks a lot again

---

### 评论 #13 (作者: HY45205, 时间: 1年前)

Thank you for taking the time to share your thoughts and insights. It's always valuable to see different perspectives and learn from the experiences of others in the community. Your contribution not only adds depth to the discussion but also inspires others to engage and share their ideas as well. This kind of knowledge exchange is what makes a community thrive and grow stronger. Whether it's an innovative approach, a thoughtful question, or simply an observation, each piece of input helps build a richer understanding for everyone involved. I truly appreciate the effort you’ve put into crafting your post—it’s clear that a lot of thought and expertise went into it. Please keep sharing your ideas and discoveries, as they are incredibly helpful for others who may be exploring similar topics. Once again, thank you for being an active and thoughtful member of the community!

---

### 评论 #14 (作者: AT56452, 时间: 1年前)

The study examines how the dissemination of public news through social networks affects investor behavior and securities markets. It finds that firms situated in regions with higher social network centrality experience more pronounced immediate reactions in stock price, volatility, and trading volume following earnings announcements. Subsequently, these firms exhibit reduced price drift, quicker volatility reduction, but sustained elevated trading volumes. This suggests that increased social connectedness facilitates prompt assimilation of news into stock prices, yet also leads to differing opinions and heightened trading activity. The researchers introduce the "social churning hypothesis," supported by detailed data from StockTwits messages and individual trading records.

---

### 评论 #15 (作者: AT56452, 时间: 1年前)

The study highlights the significant role of social networks in shaping investor reactions to public news, particularly earnings announcements. Investors connected through these networks tend to respond more swiftly and intensely to such news, affecting market dynamics.

---

### 评论 #16 (作者: AT56452, 时间: 1年前)

Firms located in areas with higher social network centrality witness stronger immediate market reactions—evident in price changes, volatility, and trading volumes—following earnings announcements. This underscores the importance of social connectedness in financial markets.

---

### 评论 #17 (作者: AT56452, 时间: 1年前)

After the initial reaction to earnings announcements, firms in highly connected regions experience a quicker stabilization of volatility and less price drift. However, they also face sustained higher trading volumes, indicating prolonged investor engagement.

---

### 评论 #18 (作者: AT56452, 时间: 1年前)

The researchers propose the "social churning hypothesis," suggesting that while social networks aid in the rapid incorporation of news into stock prices, they also foster opinion divergence among investors, leading to increased trading activity.

---

### 评论 #19 (作者: AT56452, 时间: 1年前)

Data from StockTwits, a platform for investors to share opinions, was analyzed to understand how social media influences trading behavior. The findings indicate that sentiments expressed on such platforms can predict market movements and investor actions.

---

### 评论 #20 (作者: AT56452, 时间: 1年前)

By examining individual trading records, the study provides evidence that social networks contribute to excessive trading. Investors embedded in dense social networks are more likely to trade frequently, influenced by the opinions and actions of their peers.

---

### 评论 #21 (作者: AT56452, 时间: 1年前)

The research suggests that social connectedness enhances the speed at which public news is reflected in stock prices, reducing informational inefficiencies in the market. This rapid assimilation benefits investors seeking to capitalize on new information.

---

### 评论 #22 (作者: AT56452, 时间: 1年前)

Despite the benefits of quick information dissemination, increased social connectedness can lead to varying interpretations of news, causing opinion divergence. This divergence is a driving factor behind the observed excessive trading volumes.

---

### 评论 #23 (作者: AT56452, 时间: 1年前)

The study finds that while initial volatility spikes post-announcement are more pronounced in highly connected regions, the subsequent decay in volatility is faster. This pattern suggests that social networks play a complex role in influencing market stability.

---

### 评论 #24 (作者: AT56452, 时间: 1年前)

The correlation between social connectedness and excessive trading raises questions about market efficiency. While rapid information dissemination is beneficial, the resulting overtrading may lead to increased transaction costs and potential market distortions.

---

### 评论 #25 (作者: HD25387, 时间: 1年前)

Hi!

Thank you for the summary, it is very well-structured.

---

### 评论 #26 (作者: CC40930, 时间: 1年前)

This paper investigates how the social transmission of public news, particularly through investor social networks, affects investor beliefs and securities markets. The study finds that earnings announcements from firms located in higher-centrality positions within social networks lead to stronger immediate reactions in price, volatility, and trading volume. After the announcement, such firms exhibit weaker price drift and faster volatility decay, but experience higher and more persistent trading volume. The findings suggest that greater social connectedness facilitates the timely incorporation of news into market prices, but also fosters opinion divergence and excessive trading. The authors introduce the "social churning hypothesis" and provide evidence using granular data from platforms like StockTwits and household trading records.

---

### 评论 #27 (作者: HD25387, 时间: 1年前)

The findings that firms in higher-centrality locations experience stronger immediate reactions to earnings announcements highlight the role of social networks in market dynamics. Using data like  `snt_social_volume`  could help identify stocks with heightened social attention, providing opportunities for Alpha generation around earnings announcements.

---

### 评论 #28 (作者: HD25387, 时间: 1年前)

The evidence supporting the social churning hypothesis is particularly compelling. The combination of faster volatility decay and persistent trading volume post-announcement suggests potential inefficiencies. Leveraging  `snt_social_value`  as a sentiment indicator might offer insights into opinion divergence and trading patterns.

---

### 评论 #29 (作者: HD25387, 时间: 1年前)

The granular data from StockTwits and household trading records underline the importance of social media in shaping market behavior. Incorporating  `scl12_alltype_buzzvec`  into predictive models could enhance the understanding of how sentiment diffusion impacts stock price and volume reactions, especially in the short term.

---

### 评论 #30 (作者: VP21767, 时间: 1年前)

This study explores how social networks influence investor behavior and stock market reactions. It finds that firms with higher social network centrality generate stronger price and volatility reactions to earnings announcements, accompanied by persistent trading volume. Post-announcement, these firms exhibit less price drift and faster volatility decay. The findings highlight the role of social connectedness in incorporating news into prices while driving opinion divergence and excessive trading, supported by granular data from StockTwits and household trading records.

---

### 评论 #31 (作者: RA30956, 时间: 1年前)

**Role of Social Connectivity in Market Efficiency** : The study underscores the dual role of social networks in financial markets—enhancing the speed of price adjustments while fostering opinion divergence and excessive trading. Investigating the trade-offs between these effects across different market conditions could provide a more nuanced understanding of social networks' impact on market efficiency.

---

### 评论 #32 (作者: MA70307, 时间: 1年前)

**Granular Analysis and Predictive Applications** : The integration of StockTwits messages and household trading records offers valuable granular insights. Expanding this approach to include other social platforms or regional investor behaviors could help refine predictive models for trading volume, sentiment shifts, and post-announcement price drifts.

---

### 评论 #33 (作者: RK48711, 时间: 1年前)

Thank you for sharing the summary and key insights from this study! The findings on the role of social transmission in shaping investor beliefs and market behavior are truly intriguing.

The concept of higher-centrality firms driving stronger market reactions, followed by faster price and volatility adjustments but persistent trading volume, underscores the dual impact of social connectedness—enhancing information dissemination while fostering opinion divergence and trading activity. The "social churning hypothesis" seems like a valuable addition to our understanding of behavioral finance.

I’m particularly interested in how the granular data (e.g., StockTwits messages and household trading records) supports this hypothesis. It would be great to dive deeper into the specific metrics like tweet volume, sentiment Z scores, and sentiment volume.

---

### 评论 #34 (作者: AK98027, 时间: 1年前)

Certainly! Here's a very short summary of the article:

This article explores how social networks influence stock market behavior. Key strengths include its interdisciplinary approach and focus on investor psychology. Areas for improvement include more empirical evidence and a deeper dive into the impact of misinformation.

This summary focuses on the core aspects of the article and its potential for further development.

---

### 评论 #35 (作者: CT68712, 时间: 1年前)

Hey, great insights on the paper! As a high-frequency trader, I really appreciate how you highlighted the role of social connectedness in influencing immediate market reactions. The idea that earnings announcements from firms in more central locations lead to stronger price movements is fascinating. I think incorporating sentiment analysis from social media, like using sentiment Z-scores and tweet volume, could definitely enhance our alpha strategies. Additionally, understanding the lag between news diffusion and market reactions will be crucial for executing trades efficiently. Let's explore how we can utilize these findings in our trading models to capture those rapid fluctuations in price!

---

### 评论 #36 (作者: CT68712, 时间: 1年前)

Hey, I found your insights on the social transmission of public news really interesting! As a tech enthusiast diving into quantitative trading, the idea that social networks have such a strong impact on stock reactions resonates with me. It's fascinating how higher-centrality firms see more immediate price fluctuations and trading volumes. I'm curious about implementing this in my trading strategies. For instance, using tweet volumes and sentiment metrics could provide us an edge in understanding market behavior. Have you considered exploring machine learning techniques to capture these relationships further? I'd love to hear more of your thoughts on that!

---

### 评论 #37 (作者: KS69567, 时间: 1年前)

This study examines how the social transmission of public news impacts investors' beliefs and securities markets. By analyzing investor social networks, the research reveals that earnings announcements from firms in higher-centrality network positions lead to stronger immediate reactions in price, volatility, and trading volume. After the announcement, these firms experience weaker price drift, faster volatility decay, but more persistent and higher trading volume. This suggests that increased social connectedness facilitates quicker news incorporation into prices but also contributes to opinion divergence and excessive trading. The study introduces the "social churning hypothesis" and provides supporting evidence using granular data from StockTwits and household trading records.

---

### 评论 #38 (作者: KS69567, 时间: 1年前)

That’s a great approach! Leveraging sentiment analysis from social media platforms like StockTwits or Twitter can provide real-time insights into market sentiment, allowing you to capture rapid market movements. Here are a few strategies you could explore:

1. **Sentiment Z-Scores** : By calculating sentiment Z-scores for relevant tweets or posts, you can identify unusually high or low sentiment that could signal a potential market reaction.
2. **Tweet Volume and Event Detection** : Track tweet volume around earnings announcements or major news releases. A spike in volume, especially with strong sentiment, could indicate a shift in investor behavior.
3. **Lag Analysis** : Study the time lag between sentiment changes and price movements. By understanding this lag, you can optimize entry and exit points, making your trades more timely.
4. **Social Network Centrality** : Incorporate data on social network centrality, focusing on high-centrality influencers whose opinions may lead to faster diffusion of news and stronger market reactions.

By integrating these factors into your high-frequency trading models, you’ll be able to better capture those rapid price movements and adjust your strategies for maximum profitability. Let me know if you'd like to dive deeper into any of these ideas!

---

### 评论 #39 (作者: KS69567, 时间: 1年前)

Thank you for sharing the study's main findings and summary! The research on how social transmission influences investor attitudes and market behaviour is quite fascinating.

---

### 评论 #40 (作者: AK98027, 时间: 1年前)

The study offers compelling evidence that social network centrality significantly enhances market efficiency by accelerating the diffusion of earnings news. High-centrality firms see quicker price adjustments and less post-announcement drift, underlining the critical role of social connections in reducing informational inefficiencies.

---

### 评论 #41 (作者: AK98027, 时间: 1年前)

The introduction of the social churning hypothesis is a highlight of the paper. It provides a nuanced explanation for the divergence in return volatility and trading volume dynamics, suggesting that persistent trading stems from fluctuating investor beliefs triggered by social interactions.

---

### 评论 #42 (作者: AK98027, 时间: 1年前)

The use of Facebook’s Social Connectedness Index (SCI) as a proxy for real-world social networks is innovative. This approach provides a comprehensive measure of social ties, highlighting how geographic and network centrality influence the flow of market information.

---

### 评论 #43 (作者: AK98027, 时间: 1年前)

The granular data from StockTwits adds depth to the research. It reveals that high-centrality announcements lead to more persistent discussions and disagreements among investors, which supports the idea that social interactions perpetuate attention to financial news over time.

---

### 评论 #44 (作者: AK98027, 时间: 1年前)

The findings on the persistence of investor disagreement are particularly intriguing. High-centrality announcements not only generate more immediate reactions but also sustain prolonged debates, highlighting how social networks shape not just the speed but also the complexity of news interpretation.

---

### 评论 #45 (作者: AK98027, 时间: 1年前)

The paper’s contrast between the fast decay of return volatility and the persistence of trading volume is thought-provoking. It challenges traditional market models and suggests that social dynamics, rather than new information, drive excessive trading activity post-announcement.

---

### 评论 #46 (作者: AK98027, 时间: 1年前)

The observation that high-centrality firms disproportionately attract retail investor activity raises questions about potential biases and inefficiencies introduced by social trading. Retail investors might overtrade based on beliefs propagated through social networks, often incurring higher losses.

---

### 评论 #47 (作者: AK98027, 时间: 1年前)

- By linking social connectedness to economic outcomes like trading volume and price adjustments, the paper extends its relevance beyond finance. It emphasizes the interconnected nature of social behavior and economic decision-making, with implications for other areas like policy design and corporate strategy.

---

### 评论 #48 (作者: AK98027, 时间: 1年前)

While the research is robust, it’s worth exploring whether the findings apply to international markets with different social and cultural dynamics. Additionally, studying other types of news, like macroeconomic announcements, could validate and extend the framework.

---

### 评论 #49 (作者: AK98027, 时间: 1年前)

This research provides actionable insights for market participants. For instance, traders and portfolio managers could use centrality metrics to anticipate market reactions, while policymakers might reconsider how social networks contribute to market inefficiencies.

---

### 评论 #50 (作者: AK98027, 时间: 1年前)

The paper’s distinction between geographic proximity and social network centrality is a crucial contribution. It demonstrates that the flow of information depends more on social connections than mere physical closeness, reshaping how we think about local bias in investing.

---

