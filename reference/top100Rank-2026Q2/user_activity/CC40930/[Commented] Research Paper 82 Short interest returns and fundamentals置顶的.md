# Research Paper 82: Short interest, returns, and fundamentals置顶的

- **链接**: [Commented] Research Paper 82 Short interest returns and fundamentals置顶的.md
- **作者**: NL41370
- **发布时间/热度**: 1年前, 得票: 18

## 帖子正文

Abstract:

We show that short interest predicts future bad news, negative earnings surprises, and

downward revisions in analyst earnings forecasts. Moreover, short interest is a better

predictor of changes in firm fundamentals for stocks that are harder to short and short

sellers appear to have information about these events several months before they become

public. Most importantly, the well-known cross-sectional relation between short interest

and future stock returns vanishes after controlling for short sellers’ information about

future fundamental news. Thus, short sellers contribute in a significant manner to price

discovery about firm fundamentals.

Author: Ferhat Akbas, Ekkehart Boehmer , Bilal Erturk, and Sorin Sorescu

Year: 2013

Link:  [Short Interest, Returns, and Fundamentals by Ferhat Akbas, Ekkehart Boehmer, Bilal Erturk, Sorin M. Sorescu :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2216919)

Key ideas and comments from WorldQuant:

Page 17 Paragraph 2

Page 19 Paragraph 3

**Term**

**Data field**

**Dataset**

short interest

mdl77_devpacificshortsentimentfactor_tni_ths

[Analysts’ factor model](https://platform.worldquantbrain.com/data/data-sets/model77?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

firm fundamental

mdl77_surpriseanalystmodel_qsa_efficiency

[Analysts’ factor model](https://platform.worldquantbrain.com/data/data-sets/model77?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

information

mdl175_informationratio120

[China Fundamentals and Technicals Model](https://platform.worldquantbrain.com/data/data-sets/model175?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=CHN&universe=TOP2000U)

---

## 讨论与评论 (104)

### 评论 #1 (作者: AT56452, 时间: 1年前)

[NL41370](/hc/en-us/profiles/11433604068887-NL41370)  - Quite insightful! To apply the insights given in this paper, we can use other data fields too other than those mentioned in the post right?

---

### 评论 #2 (作者: SK95162, 时间: 1年前)

"An outstanding analysis highlighting the predictive power of short interest on firm fundamentals, showcasing its critical role in price discovery and market efficiency!"

---

### 评论 #3 (作者: TN48752, 时间: 1年前)

I don't quite understand how to implement using the above datasets, because mdl175 is only available in CHN region and mdl77 is not available in CHN.

---

### 评论 #4 (作者: SC43474, 时间: 1年前)

An insightful paper revealing the role of short sellers in anticipating fundamental news and contributing significantly to price discovery. It highlights the interplay between market efficiency and informational asymmetry.

---

### 评论 #5 (作者: AT56452, 时间: 1年前)

[TN48752](/hc/en-us/profiles/13714359745431-TN48752)  - You can probably find datafields in china that correspond to mdl77. That will help you in creating an alpha using this theory. Search using the data explorer.

---

### 评论 #6 (作者: LN78195, 时间: 1年前)

Thank you for sharing the paper! It provides great insights into how short interest can predict negative earnings surprises and downward analyst revisions. I look forward to exploring more research like this in the future.

---

### 评论 #7 (作者: LR13671, 时间: 1年前)

"How do the findings on short sellers’ ability to predict negative firm fundamentals several months in advance inform the regulatory perspective on short-selling restrictions for hard-to-short stocks?"

---

### 评论 #8 (作者: MA70307, 时间: 1年前)

This paper provides compelling evidence on the predictive power of short interest regarding future bad news, negative earnings surprises, and analyst forecast revisions. The insights on  **Page 17 Paragraph 2**  and  **Page 19 Paragraph 3**  reinforce the role of short sellers in price discovery and their access to critical information months ahead of public release. I find it intriguing how controlling for short sellers’ knowledge of fundamental news nullifies the cross-sectional relationship between short interest and stock returns, emphasizing the informational efficiency they bring to markets. The datasets, such as mdl77_devpacificshortsentimentfactor_tni_ths and mdl77_surpriseanalystmodel_qsa_efficiency, seem to effectively capture these dynamics, providing valuable tools for analyzing the link between short interest, firm fundamentals, and market behavior.

---

### 评论 #9 (作者: DK20528, 时间: 1年前)

Thank you for sharing this insightful paper! It offers valuable perspectives on the predictive power of short interest for negative earnings surprises and downward analyst revisions. I look forward to delving deeper into this topic and exploring more research in this area.

---

### 评论 #10 (作者: TD84322, 时间: 1年前)

Thanks for sharing the paper, NL41370! This research offers valuable insights into how short interest predicts negative earnings surprises and downward analyst revisions, and how short sellers contribute to price discovery. It's interesting that short sellers seem to have information about firm fundamentals months before the public.

---

### 评论 #11 (作者: SJ17125, 时间: 1年前)

Thanks for sharing This research which highlights the predictive power of short interest in forecasting negative earnings surprises and downward revisions in earnings forecasts. It reveals that short sellers have access to crucial firm-specific information ahead of public disclosure, particularly for stocks that are harder to short. The study challenges the conventional wisdom linking short interest with stock returns by demonstrating that the relation dissipates once short sellers’ information is factored in, emphasizing their critical role in price discovery and reflecting a deeper understanding of firm fundamentals.

---

### 评论 #12 (作者: HV77283, 时间: 1年前)

Thanks for sharing NL41370! This research sheds light on how short interest predicts negative earnings surprises, analyst downgrades, and highlights short sellers' early insights into firm fundamentals.

---

### 评论 #13 (作者: XL31477, 时间: 1年前)

Hey guys! Regarding implementing with the mentioned datasets when some are region-limited like mdl175 in CHN region only and mdl77 not available in CHN, as  [AT56452](/hc/en-us/profiles/16716798553111-AT56452)  said, try finding corresponding datafields in China for mdl77 via the data explorer. And for the regulatory perspective on short-selling restrictions for hard-to-short stocks as  [LR13671](/hc/en-us/profiles/4516642748055-LR13671)  asked, it depends on how authorities weigh short sellers' predictive power and market impacts. We need more studies on that.

---

### 评论 #14 (作者: BA51127, 时间: 1年前)

**The discussion on Research Paper 83, which delves into the impact of investor emotions on commodity market returns, is indeed a fascinating exploration of the psychological aspects of trading. It's intriguing how this study uses a proprietary dataset of commodity-specific market emotions derived from textual analysis to predict short-term commodity returns.**

**Building on the comments, particularly  [LR13671](/hc/en-us/profiles/4516642748055-LR13671) 's point about the interplay between emotions and cross-commodity relationships, a compelling question arises: How might the framework of this study be extended to assess the spillover effects of emotions across different commodities? For instance, could a surge in optimism about crude oil potentially influence investor sentiment and returns in gold, and vice versa? Understanding these dynamics could provide a more holistic view of how emotions drive market movements and contribute to a more sophisticated predictive model for commodity trading strategies.**

---

### 评论 #15 (作者: AK98027, 时间: 1年前)

Key finding: Short sellers successfully predict negative company events (bad news, earnings misses, and downward forecast revisions) months before they become public. Their influence on stock returns is primarily through this fundamental information discovery rather than speculative trading.

---

### 评论 #16 (作者: SG76464, 时间: 1年前)

Thanks for sharing this useful paper that shed light on short interest predicts negative earnings

---

### 评论 #17 (作者: AC63290, 时间: 1年前)

The study highlights the predictive power of short interest on future bad news, negative earnings surprises, and analyst forecast revisions. Short sellers demonstrate foresight into firm fundamentals months ahead of public disclosure. Importantly, the correlation between short interest and future returns diminishes when accounting for short sellers' informational advantage. Key data fields for replication include  `mdl77_devpacificshortsentimentfactor_tni_ths`  (short interest),  `mdl77_surpriseanalystmodel_qsa_efficiency`  (firm fundamentals), and  `mdl175_informationratio120`  (information). These datasets, especially from analysts' factor models, provide valuable insights into short sellers' role in price discovery and their ability to anticipate fundamental changes in stocks, further emphasizing their significant contribution to market efficiency.

---

### 评论 #18 (作者: XD81759, 时间: 1年前)

Hey, this research paper's quite interesting. It shows short interest can predict future bad news and more. When it comes to the data fields like "short interest" and "firm fundamental", we could potentially use them as factors in our quant models. For example, we might build a factor based on short interest to see if it correlates with stock returns in our datasets. And with the Analysts’ factor model, we could combine different factors to dig deeper into price discovery related to firm fundamentals. Just some thoughts for discussion.

---

### 评论 #19 (作者: SJ17125, 时间: 1年前)

Hiii,

thanks to every one for sharing valueable insights from the research paper. it really helped me to understand the topic.

---

### 评论 #20 (作者: DN45758, 时间: 1年前)

Thanks for sharing the paper, NL41370! This research offers valuable insights into how short interest predicts negative earnings surprises and downward analyst revisions, and how short sellers contribute to price discovery. It's interesting that short sellers seem to have information about firm fundamentals months before the public.

---

### 评论 #21 (作者: CC40930, 时间: 1年前)

In summary, this study provides evidence that short interest is not just a measure of market sentiment but also an early signal of upcoming negative news about a company's fundamentals. By incorporating this information into your alpha models, you may improve your ability to anticipate stock price movements and construct more effective trading strategies.

---

### 评论 #22 (作者: LY88401, 时间: 1年前)

Your article is excellently written! The ideas are clear, engaging, and well-organized. You have a remarkable ability to present complex topics in a simple, accessible way. It’s an insightful and thought-provoking read that reflects your deep understanding and expertise.

---

### 评论 #23 (作者: PN39025, 时间: 1年前)

Thank you for sharing this insightful analysis on the predictive power of short interest in financial markets. Your work highlights the nuanced role of short sellers in anticipating future fundamental news, which is critical to understanding market dynamics and price discovery. The rigorous connection drawn between short interest and future bad news, negative earnings surprises, and analyst forecast revisions offers a powerful lens through which investors can better comprehend market be

The example you provided is especially compelling:

- Short interest not only anticipates bad news but does so particularly for stocks that ar
- The fact that short sellers possess actionable insights several months ahead of public disclosures underscores the sophistication of their strategies and the depth of
- Moreover, the finding that the cross-sectional relationship between short interest and future returns vanishes when accounting for short sellers’ information suggests that their activities are fundamental to aligning stock prices with underlying

### Practical Example:

Consider a scenario where a stock has an unusually high short interest ratio, despite no immediate adverse news. Months later, the company reports a substantial earnings miss, and analysts revise their forecasts downward. The price plummets in response. Your findings suggest that short sellers had already factored in this outcome, possibly due to deep analysis of supply chain issues, declining demand, or industry headwinds.

The ability of short sellers to identify such trends early makes them vital contributors to price efficiency. Their actions serve as a form of market oversight, ensuring that prices better reflect firm fun

---

### 评论 #24 (作者: TT55495, 时间: 1年前)

Thank you for sharing this insightful abstract on the predictive power of short interest regarding future firm fundamentals. The findings regarding short sellers' role in price discovery are quite thought-provoking and offer valuable implications for risk management and return prediction.

---

### 评论 #25 (作者: SV11672, 时间: 1年前)

"Fascinating study on the predictive power of short interest! The findings that short interest predicts future bad news, negative earnings surprises, and downward revisions in analyst earnings forecasts are compelling. The fact that short interest is a better predictor for stocks that are harder to short suggests that short sellers have access to valuable information. The most interesting result, however, is that the relationship between short interest and future stock returns disappears once you control for short sellers' information about future fundamental news. This suggests that short sellers play a crucial role in price discovery, and their activities help to incorporate information about firm fundamentals into stock prices."

---

### 评论 #26 (作者: SV11672, 时间: 1年前)

"Great contribution to the literature on short selling and price discovery! The study's findings have important implications for our understanding of the role of short sellers in the market. By showing that short sellers have access to valuable information about future fundamental news, the study highlights the importance of short selling in facilitating price discovery. The results also suggest that regulators and investors should be cautious when interpreting the relationship between short interest and future stock returns, as it may be driven by short sellers' information advantage rather than manipulation or other factors."

---

### 评论 #27 (作者: AT56452, 时间: 1年前)

Short interest—the volume of shares sold short but not yet covered or closed—serves as a significant indicator in financial markets, offering insights into investor sentiment and potential future stock performance.

---

### 评论 #28 (作者: AT56452, 时间: 1年前)

Elevated short interest often signals investors' anticipation of a company's declining performance. Research indicates that high short interest correlates with future negative news releases, suggesting that short sellers possess foresight into impending adverse developments.

---

### 评论 #29 (作者: AT56452, 时间: 1年前)

Companies with substantial short interest are more prone to report earnings below analyst expectations. This trend implies that short sellers may detect discrepancies or weaknesses in financial health before such information becomes public, highlighting their role in identifying overvalued stocks.

---

### 评论 #30 (作者: AT56452, 时间: 1年前)

High short interest levels can precede downward revisions in analyst earnings forecasts. This pattern suggests that short sellers' activities might influence or predict analysts' reassessments of a company's future profitability, reflecting a deeper understanding of underlying business challenges.

---

### 评论 #31 (作者: AT56452, 时间: 1年前)

Short sellers often exhibit an information advantage, enabling them to act on negative fundamentals before they become public knowledge. This advantage underscores the sophisticated research and analysis employed by short sellers in market assessments.

---

### 评论 #32 (作者: AT56452, 时间: 1年前)

The relationship between short interest and future stock returns is nuanced. While high short interest can indicate anticipated declines, this correlation diminishes when accounting for short sellers' insights into future fundamental news, suggesting that their information is a significant factor in price movements.

---

### 评论 #33 (作者: AT56452, 时间: 1年前)

Short sellers contribute significantly to price discovery by integrating their information about firm fundamentals into stock prices. Their trading activities help correct overvaluations, leading to more accurate stock valuations that reflect a company's true financial state.

---

### 评论 #34 (作者: AT56452, 时间: 1年前)

Stocks that are difficult to short due to limited availability or high borrowing costs often see more pronounced predictive signals from short interest. In such cases, short sellers' commitment indicates strong conviction about anticipated negative performance, despite the higher costs and risks involved.

---

### 评论 #35 (作者: AT56452, 时间: 1年前)

Short sellers appear to act on information several months before it becomes public. This early action reflects their proactive research and ability to identify issues ahead of broader market awareness, allowing them to capitalize on forthcoming stock price declines.

---

### 评论 #36 (作者: AT56452, 时间: 1年前)

Investors and analysts monitor short interest levels to gauge market sentiment. Rising short interest may indicate growing bearishness among informed investors, serving as a cautionary signal to the market about potential declines.

---

### 评论 #37 (作者: AT56452, 时间: 1年前)

Understanding the dynamics of short interest can inform investment strategies. Investors might exercise increased diligence when investing in stocks with high short interest, recognizing the potential for underlying issues that could impact future performance.

---

### 评论 #38 (作者: AT56452, 时间: 1年前)

Short selling remains a legal and regulated practice, viewed as essential for market efficiency and liquidity. Regulators acknowledge that, despite controversies, short selling contributes to price discovery and helps prevent overinflated stock valuations.

---

### 评论 #39 (作者: AT56452, 时间: 1年前)

By identifying and acting on overvalued stocks, short sellers enhance market efficiency. Their activities help align stock prices more closely with intrinsic values, reducing the likelihood of bubbles and promoting healthier market conditions.

---

### 评论 #40 (作者: AT56452, 时间: 1年前)

While high short interest can indicate anticipated declines, it also poses risks such as short squeezes. In a short squeeze, unexpected positive news can drive stock prices up, forcing short sellers to cover positions at a loss, which can further accelerate price increases.

---

### 评论 #41 (作者: AT56452, 时间: 1年前)

Significant short interest has been observed in market anomalies, such as the "meme stock" phenomenon, where stocks with high short interest experienced extreme volatility due to coordinated buying by retail investors, leading to substantial losses for short sellers.

---

### 评论 #42 (作者: AT56452, 时间: 1年前)

Short selling is often viewed with skepticism, with critics arguing it can exacerbate market declines. However, proponents assert that it plays a crucial role in identifying overvalued stocks and fraudulent practices, thereby contributing to overall market health and transparency.

---

### 评论 #43 (作者: KS69567, 时间: 1年前)

This observation highlights two critical insights about short interest as a predictor:

1. **Short Sellers' Informational Advantage** : The predictive power of short interest is stronger for stocks that are harder to short, indicating that short sellers often act on valuable, non-public information or superior analyses. The cost and difficulty of shorting such stocks may deter uninformed traders, leaving a higher concentration of informed short sellers.
2. **Impact of Fundamental News** : The relationship between short interest and future stock returns vanishes when adjusting for short sellers' insights into future fundamental news. This suggests that much of the predictive power of short interest stems from short sellers’ ability to anticipate fundamental changes, such as earnings surprises or financial distress, rather than being an independent signal.

These findings imply that short interest is a proxy for informed trading rather than a standalone predictor, emphasizing the importance of understanding the context and information underlying such signals.

---

### 评论 #44 (作者: KS69567, 时间: 1年前)

The study emphasises how important short sellers are to price discovery since they have access to important data regarding future fundamentals. Because short interest's predictive power comes from smart trading rather than manipulation, it warns investors and authorities to read it cautiously.

---

### 评论 #45 (作者: SK78969, 时间: 1年前)

This research provides fascinating insights into the predictive power of short interest and its role in price discovery. It's particularly interesting how short sellers seem to anticipate bad news and fundamental changes months before they become public, especially for stocks that are harder to short. The finding that the cross-sectional relation between short interest and future returns vanishes when controlling for information on fundamentals underscores the importance of understanding the role of short sellers in the market. It highlights their contribution to efficient pricing and market transparency.

---

### 评论 #46 (作者: CT68712, 时间: 1年前)

這篇研究真的是讓我驚艷！作為一名剛入門的量化交易新手，看到短期賣空（short interest）能預測未來的負面消息，對我來說是個大啟發。短賣空者竟然能在公開發布前幾個月就預測出負面盈餘驚喜和分析師預測修正，這真的是市場效率的一個有趣面向。雖然目前我還在努力理解具體實施的操作，但我覺得結合這些數據在我的交易策略中會很有幫助！希望能和大家一起探討更多這方面的知識！

---

### 评论 #47 (作者: AK98027, 时间: 1年前)

Thank you for sharing this insightful abstract on the predictive power of short interest regarding future firm fundamentals. The findings regarding short sellers' role in price discovery are quite thought-provoking and offer valuable implications for risk management and return prediction.

---

### 评论 #48 (作者: AK98027, 时间: 1年前)

Short selling is often viewed with skepticism, with critics arguing it can exacerbate market declines. However, proponents assert that it plays a crucial role in identifying overvalued stocks and fraudulent practices, thereby contributing to overall market health and transparency.

---

### 评论 #49 (作者: AK98027, 时间: 1年前)

The relationship between short interest and future stock returns is nuanced. While high short interest can indicate anticipated declines, this correlation diminishes when accounting for short sellers' insights into future fundamental news, suggesting that their information is a significant factor in price movements.

---

### 评论 #50 (作者: AK98027, 时间: 1年前)

Stocks that are difficult to short due to limited availability or high borrowing costs often see more pronounced predictive signals from short interest. In such cases, short sellers' commitment indicates strong conviction about anticipated negative performance, despite the higher costs and risks involved.

---

### 评论 #51 (作者: PN39025, 时间: 1年前)

What key insights can be drawn from the neural network structure proposed for extracting trading signals, and how might these insights be adapted for practical implementation despite replication challenges on platforms like BRAIN?

---

### 评论 #52 (作者: MA70307, 时间: 1年前)

This research explores the relationship between short interest, stock returns, and firm fundamentals, highlighting how short interest can serve as a predictor of negative future events for a company. Specifically, short interest is shown to be a leading indicator of bad news, negative earnings surprises, and downward revisions in analyst earnings forecasts. Short sellers, who typically have a bearish outlook on a stock, may possess advanced information about these events, sometimes several months before they become publicly available. This provides valuable insight into how short interest can signal upcoming changes in a firm’s fundamentals, even before official announcements are made.

---

### 评论 #53 (作者: MA70307, 时间: 1年前)

Furthermore, the research reveals that short interest is a more effective predictor of fundamental changes for stocks that are harder to short. These stocks tend to have less liquidity or higher borrowing costs, making it more difficult for investors to take short positions. The fact that short sellers can still uncover negative information about these companies suggests they play a crucial role in price discovery. The research also challenges the common belief that short interest directly correlates with stock returns. Once short sellers' informational advantages are taken into account, the previously observed relationship between short interest and future returns diminishes. This indicates that short sellers' actions are not just about betting against stocks but also about incorporating future information about firm fundamentals into stock prices.

---

### 评论 #54 (作者: MA70307, 时间: 1年前)

The study’s findings emphasize the importance of short sellers in the process of price discovery, as they appear to have access to information about future negative events before they are known to the broader market. This ability gives short sellers an edge in predicting which companies are likely to experience deteriorating fundamentals, which in turn affects stock prices. By examining short interest and its predictive power, investors and analysts can gain a better understanding of future market movements, particularly those driven by fundamental shifts in the underlying companies.

---

### 评论 #55 (作者: MA70307, 时间: 1年前)

Moreover, the research provides valuable insights into how different data fields are utilized in analyzing short interest and firm fundamentals. For instance, the mdl77_devpacificshortsentimentfactor_tni_ths dataset tracks short interest and sentiment, while the mdl77_surpriseanalystmodel_qsa_efficiency dataset measures the accuracy of analysts’ predictions, offering a comprehensive view of how short interest correlates with analyst expectations. The mdl175_informationratio120 dataset further enhances the understanding of how information, including that related to short interest, influences stock prices, particularly in markets with different levels of information efficiency.

---

### 评论 #56 (作者: MA70307, 时间: 1年前)

In conclusion, short interest serves as a powerful tool for predicting future events related to firm fundamentals, and its relationship with stock returns should be viewed through the lens of short sellers' informational advantages. While short interest alone may not provide a complete picture, it remains a crucial component in forecasting negative news, earnings surprises, and analyst downgrades. This research underscores the importance of integrating various data sources to better understand the dynamics between short interest, stock returns, and firm fundamentals.

---

### 评论 #57 (作者: SC43474, 时间: 1年前)

The finding that short interest is most predictive for stocks with higher shorting costs adds a fascinating layer to the discussion. In such cases, short sellers’ willingness to bear additional costs signals their high conviction in anticipated declines. This dynamic suggests that short interest in these stocks serves as a stronger signal of negative fundamentals, offering valuable insights for investors and analysts. It also reinforces the idea that short sellers are highly selective and informed, acting only when their analysis strongly supports the likelihood of future declines.

---

### 评论 #58 (作者: SC43474, 时间: 1年前)

Short sellers’ trading patterns, as described in the study, reveal a disciplined approach to risk and information management. The gradual increase in short interest leading up to negative announcements, followed by a reduction after the news becomes public, reflects their methodical strategy. This behavior demonstrates their focus on aligning stock prices with fundamental realities while minimizing unnecessary market disruptions, further solidifying their role as informed participants rather than speculative gamblers.

---

### 评论 #59 (作者: SC43474, 时间: 1年前)

The study’s method of isolating the impact of news sentiment from firm size is a crucial step in ensuring the accuracy of its findings. Larger firms often receive more media attention, which could skew analyses of news impact. By controlling for size effects, the research provides a clearer view of how sentiment and short interest interact. This methodology not only enhances the study’s credibility but also offers a blueprint for future research on the interplay between market sentiment and trading behavior.

---

### 评论 #60 (作者: SC43474, 时间: 1年前)

Short sellers’ ability to predict bad news months in advance is a unique skill set that differentiates them from other market participants. Their success lies in their proactive approach to research, which involves identifying red flags such as weak earnings quality, industry headwinds, or operational inefficiencies. By acting on these insights, they preemptively adjust stock prices, reducing the risk of sudden, market-disrupting corrections. This anticipatory role underscores their importance in maintaining stability and fairness in financial markets.

---

### 评论 #61 (作者: SC43474, 时间: 1年前)

The study’s findings challenge the widespread regulatory criticism of short selling. Contrary to the view that short sellers destabilize markets or cause unwarranted price declines, the research shows that their trades are based on informed predictions of fundamental changes. This evidence supports the argument that short selling plays a constructive role in preventing overvaluations and identifying financial distress early. Policymakers might need to reconsider restrictions on short selling, recognizing its value as a mechanism for enhancing price discovery and market efficiency.

---

### 评论 #62 (作者: SC43474, 时间: 1年前)

The relationship between short interest and downward analyst forecast revisions is a testament to short sellers’ foresight and their ability to detect fundamental issues before they are widely recognized. The study shows that stocks with the highest short interest often experience the most significant negative revisions in analyst forecasts. This suggests that short sellers act as an early warning system for market participants, identifying risks that may not yet be apparent in publicly available data. This dynamic also challenges the traditional role of analysts as primary information providers, highlighting the complementary role of short sellers in market analysis.

---

### 评论 #63 (作者: SC43474, 时间: 1年前)

By demonstrating that the predictive power of short interest diminishes when controlling for short sellers’ insights into firm fundamentals, the study provides strong evidence that short sellers are informed traders. Their trades are not driven by speculation or market manipulation but by a deep understanding of the underlying business conditions. This finding has significant implications for regulators and market participants alike, suggesting that short sellers’ activities should be seen as enhancing market transparency and efficiency rather than as a source of volatility or instability.

---

### 评论 #64 (作者: SC43474, 时间: 1年前)

The robustness of the study’s findings across different datasets strengthens its conclusions. For instance, the use of both RavenPack and Chan’s Dow Jones-based news data ensures that the results are not specific to one source or methodology. This consistency indicates that the relationship between short interest and future fundamental changes is a generalizable phenomenon rather than an artifact of specific data quirks. Such robustness adds credibility to the study’s claim that short sellers play a vital role in predicting and incorporating negative news into stock prices, regardless of the news dataset used.

---

### 评论 #65 (作者: SC43474, 时间: 1年前)

A critical insight from the study is the relationship between short interest and future analyst forecast revisions. The research reveals that short sellers often anticipate downward revisions in earnings estimates months before analysts adjust their forecasts. This predictive power suggests that short sellers have access to more refined analytical tools or are quicker to interpret fundamental signals than traditional analysts. By incorporating short interest data into their forecasting models, analysts could potentially improve their predictions and offer better guidance to investors, creating a feedback loop that enhances overall market efficiency.

---

### 评论 #66 (作者: SC43474, 时间: 1年前)

The study’s findings that short sellers tend to avoid stocks with positive future news further emphasize their precision and strategic focus. Rather than indiscriminately targeting stocks, short sellers selectively choose companies where they anticipate fundamental weaknesses. This behavior reflects their reliance on robust, evidence-based research rather than speculative trading. It also highlights how their trades contribute to efficient price discovery by discouraging overvaluation in the market. These insights portray short sellers not as market disruptors but as disciplined analysts who identify and act on meaningful risks.

---

### 评论 #67 (作者: SC43474, 时间: 1年前)

One of the most revealing aspects of the study is the time horizon of short sellers’ predictive power. Contrary to the perception that short sellers focus on short-term price fluctuations, the research shows that short interest begins to build up months before negative news is announced. This long-term horizon, sometimes lasting up to a year, suggests that short sellers rely on deep, fundamental research rather than reacting to immediate market signals. Their methodical approach to identifying overvalued stocks and companies with hidden vulnerabilities positions them as important players in maintaining market discipline and efficiency over extended periods.

---

### 评论 #68 (作者: SC43474, 时间: 1年前)

Short sellers’ ability to predict earnings surprises underscores their deep expertise in analyzing company fundamentals. The study reveals that short sellers often act well in advance of quarterly earnings announcements, positioning themselves in anticipation of bad news. This likely involves detailed forensic accounting, supply chain analysis, and insights into broader industry trends. For instance, the cumulative abnormal return (CAR) and standardized unexpected earnings (SUE) metrics used in the study highlight how short sellers consistently anticipate disappointing earnings outcomes, providing a clear advantage over other market participants. This predictive power not only reflects their skill but also highlights the gaps in traditional market analysis.

---

### 评论 #69 (作者: SC43474, 时间: 1年前)

The use of RavenPack’s Event Sentiment Score (ESS) to quantify public news sentiment is a key innovation in this study. By providing a systematic way to classify news as positive, negative, or neutral, the authors reveal a clear connection between news sentiment and short sellers’ trading behavior. For example, the study demonstrates that stocks with high short interest often experience negative sentiment news in the subsequent months. This integration of quantitative news analysis with short interest data offers a new perspective for understanding how market sentiment drives informed trading and could be a valuable tool for both academic research and practical investment strategies.

---

### 评论 #70 (作者: SC43474, 时间: 1年前)

One of the most striking conclusions of the study is that the well-known relationship between short interest and future stock returns vanishes after accounting for short sellers’ knowledge of firm fundamentals. This finding challenges the traditional narrative that short interest directly drives stock price declines. Instead, it highlights how short sellers’ activities are fundamentally linked to their ability to anticipate significant changes in firm performance, such as earnings surprises or forecast revisions. This reframes short sellers as informed market participants whose trades align stock prices more closely with their intrinsic value, rather than as speculative forces disrupting the market.

---

### 评论 #71 (作者: SC43474, 时间: 1年前)

The study provides compelling evidence that short interest is a strong predictor of future negative news about a company, including bad earnings reports and downward revisions in analyst forecasts. This relationship is particularly pronounced for stocks that are harder to short, where high borrowing costs or limited availability of shares filter out less-informed traders. This suggests that short sellers operating in these markets are highly informed and confident in their analysis, as they are willing to incur greater costs to act on their insights. Their actions significantly enhance market efficiency by integrating early signals of deteriorating fundamentals into stock prices.

---

### 评论 #72 (作者: TL60820, 时间: 1年前)

I have a question—how are short sellers gaining this informational advantage? Do the authors discuss any specific data sources, signals, or market patterns they might be using to predict bad news and fundamental changes before they become public? Also, I’m curious about how market conditions, like liquidity constraints or volatility, impact this predictive power. For example, does this relationship weaken in highly liquid stocks or during certain market cycles?

---

### 评论 #73 (作者: RG93974, 时间: 1年前)

It highlights the interplay between market efficiency and informational asymmetry.It offers valuable perspectives on the predictive power of short interest for negative earnings surprises and downward analyst revisions.

---

### 评论 #74 (作者: RG93974, 时间: 1年前)

Short sellers successfully predict negative company events months before they become public.Their important role in pricing was emphasized and reflected a deep understanding of the fundamentals of the firm.I look forward to exploring more research like this in the future.

---

### 评论 #75 (作者: RG93974, 时间: 1年前)

This reframes short sellers as informed market participants whose trades align stock prices more closely with their intrinsic value.This research underscores the importance of integrating various data sources to better understand the dynamics between short interest, stock returns, and firm fundamentals.

---

### 评论 #76 (作者: VK91272, 时间: 1年前)

**Short interest**  refers to the total number of shares of a stock that have been sold short but not yet covered or closed out. When investors short a stock, they are betting that the stock’s price will decline, and they will profit if the stock price falls.

- **High short interest**  indicates that many investors are betting against the stock.
- **Low short interest**  means fewer investors are betting against the stock.

---

### 评论 #77 (作者: VK91272, 时间: 1年前)

While  **short interest**  can be a useful signal of investor sentiment, it’s important to understand that short positions are a form of risk. If a stock's price begins to rise, short sellers can face substantial losses, sometimes forcing them to  **cover**  their short positions, which can drive the stock price even higher in a phenomenon known as a  **short squeeze** .

###

---

### 评论 #78 (作者: VK91272, 时间: 1年前)

**Returns**  simply refer to the profit or loss made on an investment, typically expressed as a percentage of the initial investment. In this context, we’re likely talking about the  **future returns**  of a stock after observing its short interest and considering its fundamentals.

- **Positive returns**  indicate that the stock price has risen.
- **Negative returns**  indicate that the stock price has fallen.

---

### 评论 #79 (作者: VK91272, 时间: 1年前)

Returns can be driven by multiple factors, including investor sentiment (which could be partially reflected in short interest) and the stock’s underlying  **fundamentals**  (such as earnings growth, cash flow, or valuation).

---

### 评论 #80 (作者: VK91272, 时间: 1年前)

Strong fundamentals typically suggest that a company is performing well and may have good growth potential, while weak fundamentals can signal a struggling company. Investors often look at fundamentals to gauge the long-term viability and growth prospects of a stock.

---

### 评论 #81 (作者: VK91272, 时间: 1年前)

**High Short Interest** : When there is  **high short interest** , it can signal that a lot of investors are betting against the stock, possibly because they believe the company’s fundamentals are weak, or they expect the stock’s price to decline. If the  **fundamentals**  of the company are indeed poor (e.g., declining earnings, high debt), this is often a valid signal that the stock may underperform.

---

### 评论 #82 (作者: VK91272, 时间: 1年前)

**Low Short Interest** : On the other hand,  **low short interest**  suggests that investors generally expect the stock to do well, or they don't have strong concerns about its downside risk. In this case,  **solid fundamentals**  would reinforce the idea that the stock is likely to continue performing well.

---

### 评论 #83 (作者: VK91272, 时间: 1年前)

**Positive Returns & High Short Interest** : If a stock with  **high short interest**  begins to post  **strong returns**  (e.g., a surprising earnings beat or a positive news event), short sellers may rush to cover their positions, driving the stock price even higher. This is what’s known as a  **short squeeze** , and it can lead to  **excessive returns**  in the short term.

---

### 评论 #84 (作者: VK91272, 时间: 1年前)

**Negative Returns & High Short Interest** : Conversely, if a stock with high short interest experiences  **negative returns**  (such as disappointing earnings or worsening fundamentals), it will likely confirm the bearish sentiment of short sellers. In this case, returns will typically reflect the negative outlook, and the high short interest could  **intensify the downward pressure**  on the stock price.

---

### 评论 #85 (作者: VK91272, 时间: 1年前)

**Returns & Fundamentals** : If the fundamentals are strong and improving, the stock is likely to post  **positive returns**  regardless of short interest. If the fundamentals are weak or deteriorating, even a low short interest could lead to negative returns as the market responds to poor performance.

---

### 评论 #86 (作者: VK91272, 时间: 1年前)

**Positive Fundamentals, High Short Interest** : If a company’s  **fundamentals are strong**  (e.g., rising earnings, robust cash flow, solid balance sheet), but there is  **high short interest** , this could indicate that the market is  **overly pessimistic** . In this case, the company’s good fundamentals might lead to  **outperformance**  and positive returns. The shorts may have to cover, driving the price even higher.

---

### 评论 #87 (作者: VK91272, 时间: 1年前)

**Negative Fundamentals, High Short Interest** : Conversely, if a company has  **weak fundamentals**  (e.g., declining earnings, high debt, low margins) and high short interest, the market is likely to be bearish, and further  **negative returns**  could occur as the company struggles to meet expectations. Short sellers may profit, and the stock may continue to underperform.

---

### 评论 #88 (作者: VK91272, 时间: 1年前)

Investors can use  **high short interest**  as a contrarian signal. If a stock has a lot of short interest but  **solid fundamentals**  or an upcoming catalyst (e.g., a product launch or earnings surprise), it could be an opportunity for potential  **price appreciation** . The  **short squeeze**  scenario could lead to outsized returns in the short term.

---

### 评论 #89 (作者: RG93974, 时间: 1年前)

If a stock's price begins to rise, short sellers can face heavy losses, sometimes forcing them to cover their short positions, which can cause the stock price to rise even more. This relationship is particularly evident for stocks that are hard to short, where high borrowing costs or limited availability of shares shuts out less-informed traders.

---

### 评论 #90 (作者: SG25281, 时间: 1年前)

It offers valuable perspectives on the predictive power of short interest for negative earnings surprises and downward analyst revisions.Their influence on stock returns is primarily through this fundamental information discovery rather than speculative trading.The findings regarding short sellers' role in price discovery are quite thought-provoking.

---

### 评论 #91 (作者: AK62822, 时间: 1年前)

Consider a scenario where a stock has an unusually high short interest ratio, despite no immediate adverse news. Months later, the company reports a substantial earnings miss, and analysts revise their forecasts downward. The price plummets in response. Your findings suggest that short sellers had already factored in this outcome, possibly due to deep analysis of supply chain issues, declining demand, or industry headwinds.

---

### 评论 #92 (作者: RB98150, 时间: 1年前)

"Short Interest as a Predictor of Negative Fundamentals and Price Discovery"

- **Short Interest Predicts** :
  - Negative earnings surprises.
  - Downward revisions in analyst earnings forecasts.
  - Changes in firm fundamentals, especially for hard-to-short stocks.
- **Short Sellers' Information** :
  - Short sellers appear to have access to information several months before it becomes public.
  - They contribute significantly to price discovery regarding firm fundamentals.
- **Impact on Stock Returns** :
  - The cross-sectional relation between short interest and future stock returns vanishes when accounting for short sellers' information about fundamentals.
- **Key Insights** :
  - Hard-to-short stocks see stronger predictive power from short interest.
  - Short sellers use information about fundamentals to influence stock prices before news is public.

---

### 评论 #93 (作者: NG78013, 时间: 1年前)

Short sellers’ ability to predict earnings surprises underscores their deep expertise in analyzing company fundamentals. The study reveals that short sellers often act well in advance of quarterly earnings announcements, positioning themselves in anticipation of bad news.

---

### 评论 #94 (作者: NG78013, 时间: 1年前)

It highlights the interplay between market efficiency and informational asymmetry.It offers valuable perspectives on the predictive power of short interest for negative earnings surprises and downward analyst revisions

---

### 评论 #95 (作者: PT55616, 时间: 1年前)

Companies with substantial short interest are more prone to report earnings below analyst expectations, in addition, high short interest levels can precede downward in profit and return.

---

### 评论 #96 (作者: AK40989, 时间: 1年前)

The findings from this paper underscore the significant role short interest plays in predicting negative firm fundamentals and enhancing price discovery. It's fascinating how short sellers seem to possess information well ahead of public announcements, particularly for stocks that are harder to short. Given this, how might we leverage alternative datasets to refine our understanding of short interest dynamics and improve our predictive models for stock performance?

---

### 评论 #97 (作者: RS70387, 时间: 1年前)

Interesting how short sellers' insights into firm fundamentals eliminate the cross-sectional return effect.  [LR13671](/hc/en-us/profiles/4516642748055-LR13671) ’s point on regulatory perspectives raises a key question, should short-selling restrictions account for their role in price discovery?

---

### 评论 #98 (作者: HT59568, 时间: 1年前)

What is the relationship between short interest and downward revisions in analyst earnings forecasts?

---

### 评论 #99 (作者: SC43474, 时间: 1年前)

Short interest serves as a strong indicator of deteriorating firm fundamentals and plays a crucial role in price discovery. The research highlights how stocks with high short interest often experience negative earnings surprises and analyst forecast downgrades, particularly those that are difficult to short.

A key takeaway is that short sellers seem to anticipate these fundamental shifts months before they become public knowledge, suggesting they leverage deep analytical insights into company performance, industry trends, and macroeconomic conditions. Interestingly, the usual link between short interest and future stock returns disappears when accounting for the informational edge short sellers possess. This reinforces their role in shaping market efficiency by pricing in negative news well ahead of official disclosures.

---

### 评论 #100 (作者: UN28170, 时间: 1年前)

The study explores how emotions in news and social media impact commodity market returns. Using the Thomson Reuters MarketPsych Indices, the authors analyze 14 years of data with time-series models (TGARCH, VAR). Results show that emotions like optimism, fear, and joy influence crude oil and gold prices but have no significant effect on the broader commodity index. The research highlights both sentimental and appraisal effects, revealing that emotional responses affect short-term commodity price movements. These findings emphasize the role of investor psychology in market behavior. How can traders leverage emotion-based signals while mitigating risks associated with sentiment-driven volatility?

---

### 评论 #101 (作者: HD25387, 时间: 1年前)

This paper shows that  **short interest predicts negative future fundamentals** , such as bad earnings and analyst downgrades. Short sellers often act  **months before**  this information becomes public. Interestingly, once you control for this info, short interest  **no longer predicts returns** , meaning it's the  **fundamental insight** , not the shorting itself, that matters.

👉 For Alpha research, combine short interest ( `mdl77_devpacificshortsentimentfactor_tni_ths` ) with earnings surprise or analyst efficiency ( `mdl77_surpriseanalystmodel_qsa_efficiency` ). This helps isolate  **informed shorting**  from noise.

📌 Idea: Focus on stocks with  **high short interest**  and  **poor fundamentals**  — likely to underperform.

---

### 评论 #102 (作者: EC76681, 时间: 10个月前)

This is a clear and insightful explanation of the role of short interest in predicting firm fundamentals. I especially like how it highlights the contribution of short sellers to price discovery in a concise yet comprehensive way.

---

### 评论 #103 (作者: LR13671, 时间: 9个月前)

How can researchers systematically incorporate short interest into alpha models in a way that separates pure sentiment or liquidity effects from genuine informational signals about fundamentals? For example, can combining short interest with analyst revision datasets or alternative earnings sentiment factors yield more robust predictive power?

---

### 评论 #104 (作者: AF65023, 时间: 8个月前)

How can short interest be systematically incorporated into alpha models to separate pure sentiment or liquidity effects from genuine fundamental signals? Could combining it with analyst revisions or alternative earnings sentiment improve predictive power?

---

