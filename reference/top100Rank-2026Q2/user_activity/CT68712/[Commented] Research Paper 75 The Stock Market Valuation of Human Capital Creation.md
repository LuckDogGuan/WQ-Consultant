# Research Paper 75: The Stock Market Valuation of Human Capital Creation

- **链接**: [Commented] Research Paper 75 The Stock Market Valuation of Human Capital Creation.md
- **作者**: NL41370
- **发布时间/热度**: 2年前, 得票: 7

## 帖子正文

**Abstract:**

We develop measures of firm-level human capital creation from publicly disclosed personnel expenses (PE) and examine the stock market valuation of these characteristics. Separately measuring human capital creation efficacy and opportunity, we first show that efficacy is positively associated with characteristics of human-capital-intensive firms and employee productivity growth. Next, we find that efficacy has a positive pricing coefficient, implying that the market recognizes some of its variation. In our main analysis, long-short portfolios based on the human capital creation efficacy (opportunity) produce annualized abnormal returns of 4.0 to 5.4% (6.0 to 7.5%). Portfolios formed on the combination of efficacy and opportunities produce the strongest abnormal returns of 6.3 to 9.3% in annualized terms. Our results provide evidence of the importance to valuation of accurate human capital measurement.

Author: Matthias Regier, Ethan Rouen

Year: 2020

Link:  [The Stock Market Valuation of Human Capital Creation by Matthias Regier, Ethan Rouen :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3703948)

Key ideas and Comments from WorldQuant:

*Page 5 Paragraph 2*

*Page 19 Paragraph 1*

**Term**

**Data field**

**Dataset**

productivity growth

mcr27_bucket_daily_jobscreated

[Job records from job posting](https://platform.worldquantbrain.com/data/data-sets/macro27?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=GLB&universe=TOP3000)

future value

fnd23_intfv_value

[Fundamental point in time data](https://platform.worldquantbrain.com/data/data-sets/fundamental23?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=GLB&universe=TOP3000)

investment

fnd30_521cr

[Japan fundament data by sectors](https://platform.worldquantbrain.com/data/data-sets/fundamental30?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=ASI&universe=MINVOL1M)

---

## 讨论与评论 (34)

### 评论 #1 (作者: TN67143, 时间: 2年前)

Hi,

Can we look at this abstract paper in the following way?

1. From the 2 sentences (2 and 3) of the abstract, the author wrote: Separately measuring human capital creation efficacy and opportunity, we first show that efficacy is positively associated with characteristics of human-capital-intensive firms and employee productivity growth. Next, we find that efficacy has a positive pricing coefficient, implying that the market recognizes some of its variation.

Does this mean that we have efficacy is positively associated with employee productivity growth (in sentence 2) and efficacy has a positive pricing coefficient (in sentence 3) - meaning that they are at least somehow positively correlated with the stock prices? When we combine these two evidence, we can imply that productivity growth is positively associated with stocks returns (since they are both positively associated with efficacy).

2. The investment in human capital is a form of investment. Can they somewhat suggest that the investment factor is also positively correlated with the stock return?

3. The datafield of investment suggested above is from Japan fundament data by sectors, which is available on some regions like (ASI, JPN,...). Can we also use this investment factors by using the search function to search for suitable investment datafield in other regions (like GLB,...)?

Thank you.

---

### 评论 #2 (作者: DK20528, 时间: 1年前)

This paper  presents an intriguing perspective on how markets assess and quantify the creation of human capital within organizations. The study is particularly compelling because it ties the abstract concept of human capital to tangible financial metrics, offering insights into how investors might respond to corporate investments in employee skills, education, and training. The methodology and use of empirical data strengthen its claims, and the implications for corporate strategy and investor relations are significant. However, more detail on the potential causality between human capital investments and stock market performance would add depth to the discussion.

**Doubts/Questions:**

1. How do the authors differentiate between the valuation of human capital creation and general labor costs in their analysis?
2. Are there specific industries where human capital creation has a more pronounced impact on stock valuation?
3. What measures of human capital creation did the authors prioritize, and how were these metrics sourced or quantified?
4. Could external factors, such as macroeconomic trends or industry-specific disruptions, skew the relationship between human capital creation and stock performance?
5. Were any biases observed in the stock market's valuation based on the demographic composition of the workforce being developed (e.g., age, gender, educational background)?

---

### 评论 #3 (作者: MK58212, 时间: 1年前)

Thank you for your thoughtful and insightful comments on our paper. We truly appreciate your detailed observations, which highlight important aspects of our analysis. Your questions about the differentiation between human capital creation and general labor costs, as well as the potential industry-specific effects, are especially valuable and provide an opportunity to deepen the discussion of our findings. We also agree that exploring the potential causality between human capital investments and stock market performance would add significant depth to the analysis, and we will certainly consider this in future revisions.

Your inquiries into the specific metrics used to quantify human capital creation, as well as the potential influence of external factors such as macroeconomic trends, are critical for understanding the robustness of the relationship between human capital and stock performance. Additionally, your point regarding demographic composition and its potential impact on market valuation is an important consideration that could further refine our interpretation of the results.

We greatly appreciate your engagement with the paper and look forward to addressing these questions as we continue to develop our analysis. Thank you again for your valuable input!

---

### 评论 #4 (作者: TN48752, 时间: 1年前)

Hi, I find these 2 fundamental data fields work quite well in the JPN market, especially the fund23 field, which can give signals without having to nest too many operators.

---

### 评论 #5 (作者: HV77283, 时间: 1年前)

Thank you for the insightful paper! Could you clarify the methodology for calculating human capital efficacy and opportunity? Also, how did you control for industry-specific effects in the analysis?

---

### 评论 #6 (作者: LN78195, 时间: 1年前)

The nuanced distinction between human capital efficacy and opportunity is particularly intriguing. To deepen understanding, could you share more details on how efficacy and opportunity were operationalized, and how industry-specific effects were factored into the analysis?

---

### 评论 #7 (作者: XL31477, 时间: 1年前)

**Hey guys! Regarding the correlation questions,  [TN48752](/hc/en-us/profiles/13714359745431-TN48752) , it's reasonable to think productivity growth might be linked to stock returns as both relate to efficacy. But we need more tests to confirm. For using investment factor in other regions, worth a try but might vary due to different market traits.**

**[HV77283](/hc/en-us/profiles/23521701737751-HV77283) , the paper likely had specific ways to calculate human capital efficacy and opportunity, maybe based on disclosed personnel expenses and related metrics. Controlling for industry effects probably involved sector classifications and adjustments in the analysis.**

---

### 评论 #8 (作者: SK95162, 时间: 1年前)

Thanks for sharing this fundamental dataset; it offers strong alpha potential and valuable insights for enhancing investment strategies.

---

### 评论 #9 (作者: SJ17125, 时间: 1年前)

Thank you for your insightful comments on our paper. Your questions on differentiating human capital creation from labor costs and the industry-specific effects are valuable, and we'll consider these points in future revisions. We agree that exploring the causality between human capital investments and stock market performance would enrich our analysis. Additionally, your observations on external factors, such as macroeconomic trends and demographic composition, are critical for refining our interpretation. We truly appreciate your engagement and will address these questions as we continue developing our analysis.

---

### 评论 #10 (作者: DN45758, 时间: 1年前)

[TN48752](/hc/en-us/profiles/13714359745431-TN48752)    Thanks for sharing this fundamental dataset; it offers strong alpha potential and valuable insights for enhancing investment strategies

---

### 评论 #11 (作者: BA51127, 时间: 1年前)

For those looking to apply momentum ideas to alpha in websim, consider focusing on regions with high liquidity and trading volumes. Select stocks from sectors that are known to exhibit strong momentum characteristics. Use a combination of short-term and long-term momentum indicators to capture different market trends. Adjusting weights based on volatility can also help refine your strategy. Remember, the key is to find a balance between value and momentum to capitalize on global risks and market dynamics effectively.

---

### 评论 #12 (作者: XD81759, 时间: 1年前)

Hey, the paper's pretty interesting. It focuses on firm-level human capital creation and its stock market valuation. Key points are measuring efficacy and opportunity of it. The abnormal returns from long-short portfolios based on these aspects are quite notable. Data fields like productivity growth, job records, etc. are important. Maybe we could think about incorporating related factors into our quant models, like using productivity growth as a factor to predict stock performance.

---

### 评论 #13 (作者: SJ17125, 时间: 1年前)

[DK20528](/hc/en-us/profiles/24602396283031-DK20528)  The study likely explores industries where human capital creation, such as workforce development, talent acquisition, and employee training, has a more significant impact on stock valuation. Industries like technology, healthcare, and finance, where innovation and specialized skills are crucial, may see a more pronounced effect on stock prices. The authors may have prioritized metrics like employee retention rates, training investments, and talent quality, sourced from company reports or labor market data. However, external factors, including macroeconomic trends or industry-specific disruptions (like economic downturns or technological breakthroughs), could potentially skew the relationship between human capital creation and stock performance.

---

### 评论 #14 (作者: HY45205, 时间: 1年前)

Thank you for taking the time to share your thoughts and insights. It's always valuable to see different perspectives and learn from the experiences of others in the community. Your contribution not only adds depth to the discussion but also inspires others to engage and share their ideas as well. This kind of knowledge exchange is what makes a community thrive and grow stronger. Whether it's an innovative approach, a thoughtful question, or simply an observation, each piece of input helps build a richer understanding for everyone involved. I truly appreciate the effort you’ve put into crafting your post—it’s clear that a lot of thought and expertise went into it. Please keep sharing your ideas and discoveries, as they are incredibly helpful for others who may be exploring similar topics. Once again, thank you for being an active and thoughtful member of the community!

---

### 评论 #15 (作者: AT56452, 时间: 1年前)

This study introduces metrics for evaluating firm-level human capital creation using publicly disclosed personnel expenses. By independently analyzing efficacy and opportunity, it identifies a positive link between efficacy, human-capital-intensive firms, and productivity growth. Efficacy exhibits a favorable pricing coefficient, reflecting partial market recognition. Long-short portfolios based on efficacy or opportunity yield annual abnormal returns of 4.0-5.4% and 6.0-7.5%, respectively. Combined metrics outperform, delivering 6.3-9.3% returns. These findings underscore the significance of precise human capital evaluation in enhancing stock market valuation.

---

### 评论 #16 (作者: AT56452, 时间: 1年前)

The mention of a positive pricing coefficient indicates market recognition. Adding specific examples or context for this variation could make the implications clearer.

---

### 评论 #17 (作者: AT56452, 时间: 1年前)

The paragraph provides compelling evidence of portfolio performance. Including additional details on the methodology for forming these portfolios would add depth.

---

### 评论 #18 (作者: AT56452, 时间: 1年前)

Presenting annual abnormal returns for different scenarios is valuable. Including confidence intervals or standard deviations could enhance the statistical robustness.

---

### 评论 #19 (作者: AT56452, 时间: 1年前)

The strong performance of combined metrics is intriguing. Explaining why the combination yields better results could provide deeper insights.

---

### 评论 #20 (作者: AT56452, 时间: 1年前)

The conclusion about human capital measurement's importance to valuation is compelling. Elaborating on its broader implications could emphasize its practical utility.

---

### 评论 #21 (作者: CC40930, 时间: 1年前)

This paper offers an insightful analysis of firm-level human capital creation and its impact on stock market valuation. The distinction between efficacy and opportunity, along with their associations with employee productivity and firm characteristics, adds depth to the discussion. The reported abnormal returns from portfolios formed on these measures highlight the market's underpricing of human capital factors. The findings underscore the significance of precise human capital measurement in driving value and open avenues for integrating these metrics into investment strategies. A thought-provoking read for those interested in ESG and human capital analytics!

---

### 评论 #22 (作者: VP21767, 时间: 1年前)

This study examines firm-level human capital creation using publicly disclosed personnel expenses, focusing on efficacy and opportunity measures. It finds that efficacy is positively linked to characteristics like human-capital-intensive firms and employee productivity growth. Efficacy also has a positive pricing coefficient, indicating market recognition. Portfolios based on human capital creation produce annual abnormal returns of 6.3% to 9.3%. These findings highlight the critical role of accurate human capital measurement in stock market valuation.

---

### 评论 #23 (作者: SV11672, 时间: 1年前)

"Interesting study on the relationship between firm-level human capital creation and stock market valuation! The development of measures for human capital creation efficacy and opportunity from publicly disclosed personnel expenses is a significant contribution. The findings that efficacy is positively associated with human-capital-intensive firms and employee productivity growth, and that it has a positive pricing coefficient, suggest that the market values human capital creation. The results from the long-short portfolios are striking, with abnormal returns ranging from 4.0% to 9.3% per annum. These findings highlight the importance of accurate human capital measurement in valuation."

---

### 评论 #24 (作者: SV11672, 时间: 1年前)

"The study's focus on the measurement of human capital creation efficacy and opportunity is particularly noteworthy. By developing a more nuanced understanding of human capital creation, the authors are able to demonstrate its significant impact on firm valuation. The findings also suggest that investors who incorporate human capital metrics into their investment decisions may be able to generate excess returns.

---

### 评论 #25 (作者: SV11672, 时间: 1年前)

"The study's results underscore the importance of considering human capital as a key driver of firm value. By quantifying the impact of human capital creation on valuation, the authors provide a valuable framework for investors and corporate managers to make more informed decisions. It would be interesting to explore how these findings can be extended to other areas, such as talent management and organizational development."

---

### 评论 #26 (作者: SV11672, 时间: 1年前)

"This study shines a light on the critical role human capital plays in driving firm value, and provides a compelling framework for investors and corporate managers to prioritize talent development and management. The findings have significant implications for investment strategies, and underscore the need for a more nuanced understanding of the intangible drivers of business success."

---

### 评论 #27 (作者: VP21767, 时间: 1年前)

The study analyzes firm-level human capital creation using disclosed personnel expenses, linking efficacy to productivity and stock valuation. It highlights portfolios leveraging human capital opportunities, yielding 6.3-9.3% returns, emphasizing the value of accurate human capital measurement.

---

### 评论 #28 (作者: VP21767, 时间: 1年前)

This research examines firm-level human capital creation through disclosed personnel expenses, connecting efficacy with productivity and stock valuation. Portfolios utilizing human capital opportunities achieve 6.3-9.3% returns, underscoring the importance of precise human capital evaluation.

---

### 评论 #29 (作者: VP21767, 时间: 1年前)

The study explores how disclosed personnel expenses reflect human capital creation, linking efficacy to firm productivity and valuation. Combined portfolios yield 6.3-9.3% annual returns, emphasizing accurate human capital measurement's market significance.

---

### 评论 #30 (作者: VP21767, 时间: 1年前)

Researchers link firm-level human capital creation to productivity growth and stock valuation. Portfolios leveraging efficacy and opportunities achieve 6.3-9.3% returns, demonstrating the role of precise human capital metrics in market outcomes.

---

### 评论 #31 (作者: VP21767, 时间: 1年前)

This paper evaluates human capital creation via personnel expenses, showing its impact on firm productivity and valuation. Portfolios using these metrics generate up to 9.3% annual returns, highlighting the value of robust human capital measurement.

---

### 评论 #32 (作者: AK98027, 时间: 1年前)

When implementing momentum strategies in websim, consider these core principles:

- Focus on highly liquid regions and stocks with substantial trading volumes
- Target sectors with proven momentum behavior
- Blend short and long-term momentum signals to capture diverse market trends
- Implement volatility-based position sizing
- Balance momentum with value factors to better manage global risk exposure

---

### 评论 #33 (作者: CT68712, 时间: 1年前)

This paper presents some intriguing insights! The positive correlation between human capital efficacy and employee productivity growth really highlights how crucial effective talent management can be in driving firm value. The fact that long-short portfolios based on these metrics yield annualized abnormal returns of up to 9.3% is significant for those of us diving into quant strategies. It makes me wonder about integrating such factors into our trading models to capture alpha in the stock market. Additionally, I'm curious to see how these findings could vary across different regions or sectors when applying this approach. Let's keep sharing knowledge and refining our strategies!

---

### 评论 #34 (作者: KS69567, 时间: 1年前)

We appreciate your valuable and perceptive feedback on our article. Your thorough insights, which draw attention to significant facets of our investigation, are much appreciated. Your enquiries on the distinction between general labour costs and the building of human capital, as well as any possible industry-specific impacts, are very insightful and offer a chance to expand on the conversation surrounding our results. We absolutely concur that investigating the possible causal relationship between stock market performance and investments in human capital will greatly deepen the study, and we will undoubtedly take this into account in subsequent updates.

---

