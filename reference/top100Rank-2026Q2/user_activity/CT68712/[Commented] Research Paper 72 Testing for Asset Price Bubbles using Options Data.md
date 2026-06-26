# Research Paper 72: Testing for Asset Price Bubbles using Options Data

- **链接**: [Commented] Research Paper 72 Testing for Asset Price Bubbles using Options Data.md
- **作者**: KA64574
- **发布时间/热度**: 2年前, 得票: 4

## 帖子正文

**Abstract**

We present a new approach to identifying asset price bubbles based on options data. We estimate asset bubbles by exploiting the differential pricing between put and call options. We apply our methodology to two stock market indexes, the S&P 500 and the Nasdaq-100, and two technology stocks, Amazon and Facebook, over the 2014-2018 sample period. We find that, while indexes do not exhibit significant bubbles, Amazon and Facebook show frequent and significant bubbles. The estimated bubbles tend to be associated with high trading volume and earning announcement days. Since our approach can be implemented in real time, it is useful to both policy-makers and investors. As an illustration we consider two case studies: the Nasdaq dot-com bubble (between 1999 to 2002) and GameStop (between December 2020 and January 2021). In both cases we identify significant and persistent bubbles.

Author: Nicola Fusari, Robert Jarrow, Sujan Lamichhane

Year: 2020

Link:  [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3670999](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3670999)

Key ideas and Comments from WorldQuant:

- Page 11 Paragraph 2
- Page 22 Paragraph 2,3
- Page 25 Paragraph 1
- Page 28 Paragraph 2

**Term**

**Data field**

**Dataset**

option

fnd6_optgr

[Company Fundamental Data for Equity](https://platform.worldquantbrain.com/data/data-sets/fundamental6)

call option

call_breakeven_10

[Options Analytics](https://platform.worldquantbrain.com/data/data-sets/option9)

---

## 讨论与评论 (29)

### 评论 #1 (作者: TN67143, 时间: 2年前)

Hi,

Can we look at this paper in the following ways?

1. In the first sentence of the abstract, the author wrote: We present a new approach to identifying asset price bubbles based on options data.

Here, the topic of interest is how to identify asset price bubbles. From my limited understanding, asset price bubbles is a quite important issue to identify in risk management.

Maybe due to some irregular, rare occurence or unsustainable cause, the price of an asset or good may increase significantly, beyond their actual demands and valuation. Those type of event could be a recent hype in new area that attract human capitals, funds and investors to allocate a significant proportion of their resources into that-area-related assets; whereas in fact, the real demand and needs for such area have yet developed and being in line with the expectations that the investors and the public have in them. This may lead to over-investment in them, maybe sooner than their actual time of development. This may lead to rapid growth in the industry, stock prices and relatied phenomenon, followed by rapid declines in stock prices, causing investors some challenges to reallocate their capital.

Another examples could be due to some unoccasional events or some irregular natural occurence, the demand for some types of goods increases significantly, leading to a rapid increase in their prices, attracting resources to invest in them. But after that types of events pass, the demand and prices of those goods adjusted accordingly back to their normal equilibrium prices, leaving a lot of those goods that have yet to be consumed, making the supply of goods larger than the actual demand, potentially leading to a not-so-potential outlook. The rapid increase and decrease of such types of goods may be reflected in the volatile movements of the respective stocks market prices. Those types of unsustainable cause may lead to the highly volatile movements in the stock markets.

During a recent financial crisis, based on some signal, some hedge funds have been able to identify the asset price bubbles and upcoming decrease in the prices, leading to their suitable careful long and short positions. Good identification of signals of asset prices bubbles can help investors to manage their risks more effectively.and make suitable investment decisions.

To identify the asset price bubbles, the author look at a highly volatile derivative instrument: options.

---

### 评论 #2 (作者: TN67143, 时间: 2年前)

2. In the second sentence of the abstract, the authors wrote: We estimate asset bubbles by exploiting the differential pricing between put and call options.

There could be multiple reasons why the authors choose options instruments as a measure to identify asset bubbles.

One potential reason could options price tend to fluctuate at high magnitude, sometimes at multiple times the base stock prices. For example, if the base stock prices may change at 1-2% per day, then the respective options could change in the same directions at 2 times the change of the base stocks. This may lead to the options market may experience magnified effects of the original stock markets: The factors that affect the stock markets could have a more significant effect on the respective options price. This high volatility characteristics could make the options market more sensitive and absorb informations and signals quicker than the original stock markets.

Moreover, since the options prices change quickly, and could reach zero upon certain conditions (such as when the options  expire, or predicted price of the options may be above reach and the probability of the actual stock prices reaching the predicted stock prices at expiration dates are low), the investors may need to follow the market more frequently, trading more frequently, leading to their more aware reaction to the time's market conditions. This makes the changes or signals in the stock market zoom out and magnify the effect in the options market.

The options' price movement also reflect how realistic the outlook and expectation of the stock prices of companies at the time of the options IPO. If the expectations of the prices may be higher than the market reacted prices, then the options may react accordingly, showing a potential overvaluation of the stock prices. This overvaluation and the resulting options market movements may be some sign of asset price bubbles. Combining with the magnified effects on options market, the signal of potential asset price bubbles may be clearer upon following the price movements of options markets.

The authors stated that they estimate the price bubbles by examining the difference of call and put options price. To learn more about those 2 types of options, we can look at an articles of JPMorgan Chase's:  [https://www.chase.com/personal/investments/learning-and-insights/article/what-are-puts-and-calls#:~:text=A%20put%20option%20gives%20the,prior%20to%20its%20expiration%20date](https://www.chase.com/personal/investments/learning-and-insights/article/what-are-puts-and-calls#:~:text=A%20put%20option%20gives%20the,prior%20to%20its%20expiration%20date) .

To put it simple,

the call options is quite similar to long positions, that allow the investors to buy assets that are expected to rise in values in a period of time. This may reflect the optimistic outlook of the market, the investors may increase their assets by the increase in their instruments' prices. The call options could represent how optimistic the current institutions are about stocks at a time in the future.

and the put opions is quite similar to short positions, that allow the investors to sell the assets that are expected to decrease in values in a period of time. This may reflect the less optimistic outlook of the market, the investors may need to be more careful to protect their assets upon potential decrease in their instruments' prices. The put options could represent how careful the current institutions are about stocks at a time in the future.

The authors may estimate the pricing bubbles by the difference between put options and call options. It may mean: the smaller the difference, the closer the two estimates are, the more realistic the market and investors are about the future expectation of the stock prices, resulting in lower probability of asset prices bubbles; the lower volatility, the lower chances of the bubbles, and the higher the volatility, the higher chances of the bubbles.

3. In the third sentence of the abstract, the author wrote: We apply our methodology to two stock market indexes, the S&P 500 and the Nasdaq-100, and two technology stocks, Amazon and Facebook, over the 2014-2018 sample period.

Here, the authors apply their methodology to examine the price bubbles of 4 data points (S&P500 (SPX), Nasdaq-100 (NDX), Amazon stock (AMZN), and Facebook (FB)) over the time from 2014 to 2018.

If we visualize the stock prices over the period from 2014 to 2018 as a 2-dimensional graph, then we also have the similar graph for S&P500 and Nasdaq-100. Then, we can treat those two indexes as an asset to examine the price bubbles.

4. In the fourth and fifth paragraph, the authors wrote: We find that, while indexes do not exhibit significant bubbles, Amazon and Facebook show frequent and significant bubbles. The estimated bubbles tend to be associated with high trading volume and earning announcement days.

Here, the authors illustrate that the prices bubbles exists in Amazon (AMZN) and Facebook (FB), and tend to be associated with high trading volume and earning announcement days.

This may help us to associate two other supporting/associating factors into our Alphas formulas: high trading volume and earning announcement days.

It is interesting to see those potentially positive characteristics could be associated with price bubbles. It could result from a momentum of overly positive expectation outlook: when the signal are positive, investors tend to overvalue the stocks, leading to a potential price bubbles.

5. In the sixth paragraph, the authors wrote: Since our approach can be implemented in real time, it is useful to both policy-makers and investors.

They shall suggest the prospective users that may be benefited from this research paper.

6. Then, to reaffirm and prove their proposed methodology, the further examined 2 cases of price bubbles:

As an illustration we consider two case studies: the Nasdaq dot-com bubble (between 1999 to 2002) and GameStop (between December 2020 and January 2021). In both cases we identify significant and persistent bubbles.

7. To sum up, the authors has helped us to find some initial ways to build quality Alphas as follows:
a. First, calculate the difference between options put prices and options call prices. (Since we may wish to long the stocks with the lowest call-put-difference options, this put-call-difference can help us).
b. Then, associate further with volume and earning announcement characteristics.

This may be realized by:
a. (put_breakeven_n - call_breakeven_n)
b. *volume, *earning_announcements (or conditioned on volume, earnings announcements, or correlation with volume, earnings_announcements).

What do you think about the above approach?

Thank you.

---

### 评论 #3 (作者: DK20528, 时间: 1年前)

The paper, "Testing for Asset Price Bubbles using Options Data"  addresses an important and complex area in financial markets. Using options data to detect and analyze asset price bubbles is a novel and interesting approach. Here are some comments and questions regarding the study:

1. **Methodology:**  Could you elaborate on the specific models or frameworks employed to test for bubbles using options data? How does the approach compare to traditional bubble detection methods, such as unit root tests or log-periodic power-law models?
2. **Options Market Insights:**  Since options pricing incorporates expectations of future volatility and risk, how do you isolate the components of the options data that specifically reflect bubble characteristics as opposed to general market uncertainty?
3. **Empirical Validation:**  What datasets and time periods were analyzed to validate the proposed method? Were there any notable historical bubbles that were used as case studies (e.g., dot-com bubble, housing crisis)?
4. **Practical Applications:**  How might market participants, such as institutional investors or regulators, use the findings of this paper to make better decisions? For example, could the method provide early warning signals for emerging bubbles?
5. **Assumptions:**  What are the key assumptions underlying the models used? Are there scenarios or market conditions where the proposed method might fail or produce false positives?
6. **Market Depth and Liquidity:**  How does the depth and liquidity of the options market influence the reliability of bubble detection? Could the method be applied equally well across less liquid markets or for assets with sparse options trading?

This work has the potential to contribute significantly to both academic research and practical risk management. Additional insights on these points would be valuable in understanding the robustness and applicability of the proposed approach.

---

### 评论 #4 (作者: MK58212, 时间: 1年前)

Thank you for your insightful and constructive comment. We truly appreciate your recognition of the innovative nature of our work, particularly the inclusion of expected growth as an additional factor in the q-factor model. Your suggestions for further development, such as clarifying the measurement of expected growth, conducting a comparative analysis with other asset pricing models, and exploring the interactions between factors, are all excellent avenues for strengthening the model's robustness and applicability. We agree that empirical validation and cross-model comparisons will be key to establishing the practical relevance of this approach. Your feedback is incredibly valuable, and we will take it into consideration as we continue to refine and expand upon our research. Thank you again for your thoughtful contribution!

---

### 评论 #5 (作者: BA51127, 时间: 1年前)

It's fascinating how the research leverages the differential pricing between put and call options to identify such anomalies.

Building on DK20528's inquiry about the methodology, I'd like to ask: Could the authors provide more details on how they process and analyze the options data to distinguish bubble signals from other market dynamics? Specifically, how do they account for changes in implied volatility and other factors that might influence option prices, which could potentially mask or mimic bubble indicators? Additionally, what measures are taken to ensure that the detected bubbles are not just temporary market fluctuations but indeed indicative of a sustained overvaluation? Understanding these nuances could further enhance the application of this method in live trading and risk assessment strategies.

---

### 评论 #6 (作者: HV77283, 时间: 1年前)

This approach to identifying asset price bubbles using options data is a valuable contribution, especially with its real-time applicability for policy-makers and investors. The findings on Amazon and Facebook exhibiting significant bubbles provide insightful market dynamics. The case studies, particularly the GameStop example, highlight the practical use of this methodology in identifying persistent bubbles.

---

### 评论 #7 (作者: XL31477, 时间: 1年前)

Hey! You've got some good points there. Identifying asset price bubbles is indeed crucial in risk management. As the paper mentions, using options data is a novel way. Options are volatile derivatives and their pricing differences between puts and calls can give clues about bubbles. When there's a bubble, the options' behavior might deviate from normal. For example, unusual call or put volumes or price spreads could indicate something abnormal in the underlying asset's price. So, yeah, it's a smart approach to dig into options for spotting those bubbles.

---

### 评论 #8 (作者: XD81759, 时间: 1年前)

Hey! That research paper's quite interesting. The key idea of using options data to identify asset price bubbles is cool. Looking at the differential pricing between put and call options makes sense. For the data fields like "call_breakeven_10", it can help in estimating those bubbles. Maybe we could build a factor based on these option analytics data to spot stocks with potential bubbles in real time, just like what they did for Amazon and Facebook. That'd be useful for our strategies.

---

### 评论 #9 (作者: SJ17125, 时间: 1年前)

The paper on using options data to detect asset price bubbles offers a novel approach to this complex issue. Key questions include the models used for bubble detection and how they compare to traditional methods like unit root tests. It would be interesting to understand how the authors isolate bubble characteristics from general market uncertainty and which historical bubbles were analyzed. Additionally, insights into practical applications for investors and regulators, as well as the impact of market liquidity, would be valuable for evaluating the method's robustness. Clarifying the assumptions behind the approach could further strengthen its practical relevance.

---

### 评论 #10 (作者: HY45205, 时间: 1年前)

Thank you for taking the time to share your thoughts and insights. It's always valuable to see different perspectives and learn from the experiences of others in the community. Your contribution not only adds depth to the discussion but also inspires others to engage and share their ideas as well. This kind of knowledge exchange is what makes a community thrive and grow stronger. Whether it's an innovative approach, a thoughtful question, or simply an observation, each piece of input helps build a richer understanding for everyone involved. I truly appreciate the effort you’ve put into crafting your post—it’s clear that a lot of thought and expertise went into it. Please keep sharing your ideas and discoveries, as they are incredibly helpful for others who may be exploring similar topics. Once again, thank you for being an active and thoughtful member of the community!

---

### 评论 #11 (作者: AT56452, 时间: 1年前)

The study introduces an innovative method for detecting asset price bubbles by analyzing options data, specifically focusing on the pricing disparities between put and call options. This approach leverages the differential pricing to estimate the presence and magnitude of bubbles in the underlying assets.

---

### 评论 #12 (作者: AT56452, 时间: 1年前)

Applying this methodology to major stock market indices, such as the S&P 500 and the Nasdaq-100, over the period from 2014 to 2018, the study finds no significant evidence of bubbles. This suggests that, during this timeframe, these indices were priced in alignment with their fundamental values, indicating market stability at the index level.

---

### 评论 #13 (作者: AT56452, 时间: 1年前)

In contrast, when examining individual technology stocks like Amazon and Facebook within the same period, the study identifies frequent and significant bubbles. These findings imply that, despite the overall market stability, certain tech stocks experienced price deviations from their fundamental values, reflecting localized speculative behaviors.

---

### 评论 #14 (作者: AT56452, 时间: 1年前)

The detected bubbles in Amazon and Facebook stocks are often associated with periods of high trading volumes and coincide with earnings announcement days. This correlation suggests that investor reactions to new information and heightened trading activity may contribute to the formation of price bubbles in these stocks.

---

### 评论 #15 (作者: AT56452, 时间: 1年前)

A notable advantage of this options-based approach is its real-time applicability. By utilizing current options data, policymakers and investors can detect and monitor asset price bubbles as they develop, enabling more timely and informed decision-making to mitigate potential financial risks.

---

### 评论 #16 (作者: AT56452, 时间: 1年前)

The study further validates its methodology through historical case studies, including the Nasdaq dot-com bubble from 1999 to 2002. The analysis reveals significant and persistent bubbles during this period, demonstrating the method's effectiveness in identifying historical asset price anomalies.

---

### 评论 #17 (作者: AT56452, 时间: 1年前)

Another case study focuses on the GameStop episode between December 2020 and January 2021. The methodology successfully identifies substantial bubbles during this timeframe, highlighting its capability to detect rapid price escalations driven by speculative trading behaviors in real-world scenarios.

---

### 评论 #18 (作者: AT56452, 时间: 1年前)

This options-based bubble detection method offers a valuable tool for financial market analysis, providing insights into asset price dynamics that are not readily observable through traditional price analysis alone. By focusing on options data, it captures market expectations and sentiments, enhancing the understanding of bubble formations.

---

### 评论 #19 (作者: AT56452, 时间: 1年前)

The findings emphasize the importance of monitoring individual stocks, particularly in the technology sector, for signs of speculative bubbles, even when broader market indices appear stable. This targeted surveillance can help in identifying and addressing potential risks associated with asset price inflation in specific market segments.

---

### 评论 #20 (作者: AT56452, 时间: 1年前)

Overall, the study contributes to the field of financial economics by presenting a practical and timely approach to bubble detection, utilizing options data to enhance market surveillance and inform investment strategies. Its real-time applicability and focus on differential options pricing make it a significant advancement in understanding and identifying asset price bubbles.

---

### 评论 #21 (作者: CC40930, 时间: 1年前)

This study introduces a novel method for identifying asset price bubbles using options data, focusing on the differential pricing of put and call options. Applying this approach to indices like the S&P 500 and Nasdaq-100, as well as stocks like Amazon and Facebook, the research finds that significant bubbles are present in the latter. Notably, these bubbles often coincide with high trading volume and earnings announcement days. The methodology's real-time applicability makes it a valuable tool for both investors and policymakers, with case studies of the Nasdaq dot-com bubble and GameStop providing practical illustrations.

---

### 评论 #22 (作者: HD25387, 时间: 1年前)

**Thank you for sharing this intriguing paper!**

The approach of using the differential pricing between put and call options to identify asset price bubbles is innovative. The findings that Amazon and Facebook exhibited frequent bubbles, especially during high trading volume or earning announcement days, suggest actionable insights for Alpha strategies. It would be interesting to explore if this methodology could be extended to other sectors or regions with similar trading patterns.

---

### 评论 #23 (作者: HD25387, 时间: 1年前)

**Moreover, the real-time applicability of this approach is highly practical.**

Identifying bubbles during significant market events, like the Nasdaq dot-com bubble or the GameStop surge, demonstrates its relevance to both policymakers and investors. Has anyone experimented with integrating these insights using datasets like  `fnd6_optgr`  or  `call_breakeven_10`  into Alpha generation for predictive purposes?

---

### 评论 #24 (作者: VP21767, 时间: 1年前)

This study introduces a methodology to identify asset price bubbles using options data, focusing on the pricing differences between put and call options. Applied to major indices (S&P 500, Nasdaq-100) and stocks (Amazon, Facebook) from 2014 to 2018, the findings reveal significant bubbles in individual stocks, often linked to high trading volumes and earnings announcements. Case studies, including the Nasdaq dot-com bubble (1999-2002) and GameStop (2020-2021), validate the approach's ability to detect persistent bubbles, making it valuable for policymakers and investors.

---

### 评论 #25 (作者: SV11672, 时间: 1年前)

"Fascinating approach to detecting asset price bubbles using options data! By exploiting the differential pricing between put and call options, you're able to estimate bubbles in a more nuanced way. The results are intriguing, particularly the finding that Amazon and Facebook exhibited frequent and significant bubbles during the 2014-2018 period. The association between estimated bubbles and high trading volume/earning announcement days is also insightful. I appreciate the case studies on the Nasdaq dot-com bubble and GameStop, which demonstrate the potential of your approach in identifying significant and persistent bubbles. This research has important implications for policymakers and investors seeking to mitigate the risks associated with asset price bubbles."

---

### 评论 #26 (作者: SV11672, 时间: 1年前)

"This research has the potential to be a game-changer in the field of finance. The ability to detect asset price bubbles in real-time using options data is incredibly valuable for investors, policymakers, and regulators. I'm impressed by the rigor and thoroughness of the analysis, and I'm excited to see how this research will be built upon and applied in practice. Kudos to the authors for their innovative and impactful work!"

---

### 评论 #27 (作者: AK98027, 时间: 1年前)

Thank you for your valuable contributions. Your insights are insightful and add significant value to this community. Your thoughtful perspectives inspire others to share their own ideas, fostering a rich exchange of knowledge. We appreciate the time and effort you put into your contributions. Please continue to share your valuable insights with the community

---

### 评论 #28 (作者: CT68712, 时间: 1年前)

This research paper on detecting asset price bubbles through options data is really engaging! I'm particularly fascinated by the use of differential pricing between put and call options. It's interesting to see how this methodology highlighted bubbles in Amazon and Facebook during 2014-2018. Using these bubbles to inform our trading strategies could yield great Alpha! The correlation with high trading volume and earnings announcements makes it all the more relevant. I wonder if anyone's tried applying similar methods to other sectors or if there's data to validate these signals in real-time trading. This approach definitely paves the way for more sophisticated risk management techniques in our quantitative strategies!

---

### 评论 #29 (作者: KS69567, 时间: 1年前)

Thank you for your thoughtful and helpful feedback. We really appreciate your acknowledgement of the inventiveness of our work, especially the addition of predicted growth to the q-factor model.

---

