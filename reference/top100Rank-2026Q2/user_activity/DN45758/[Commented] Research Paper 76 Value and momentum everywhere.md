# Research Paper 76: Value and momentum everywhere

- **链接**: [Commented] Research Paper 76 Value and momentum everywhere.md
- **作者**: NL41370
- **发布时间/热度**: 2年前, 得票: 11

## 帖子正文

Abstract:

We find consistent value and momentum return premia across eight diverse markets and asset classes, and a strong common factor structure among their returns. Value and momentum return correlate more strongly across asset classes than passive exposures to the asset classes, but value and momentum are negatively correlated with each other, both within and across asset classes. Our results indicate the presence of common global risks that we characterize with a three-factor model. Global funding liquidity risk is a partial source of these patterns, which are identifiable only when examining value and momentum jointly across markets. Our findings present a challenge to existing behavioral, institutional, and rational asset pricing theories that largely focus on U.S. equities

Author: CLIFFORD S. ASNESS, TOBIAS J. MOSKOWITZ, and LASSE HEJE PEDERSEN

Year: 2013

Link:  [Value and Momentum Everywhere (nyu.edu)](https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf)

Key ideas and Comments from WorldQuant:

Page 11 Paragraph 3

Page 21 Paragraph 1

**Term**

**Data field**

**Dataset**

Earnings announcement

fnd23_intfv_value

[Fundamental Point in time data](https://platform.worldquantbrain.com/data/data-sets/fundamental23?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

Momentum

mdl57_momentum

[Quantitative stock valuation model](https://platform.worldquantbrain.com/data/data-sets/model57?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000)

returns

returns

[**Price Volume Data for Equity**](https://platform.worldquantbrain.com/data/data-sets/pv1)

---

## 讨论与评论 (46)

### 评论 #1 (作者: TN10210, 时间: 1年前)

Thank you for your sharing, the paper is useful.

However from my experience, I think that in WQBrain reversal idea is more easily to brainstorm and building alpha, I think that's nature of market that we want to buy a stock when it drawdown than follow momentum. Can you share some tip to apply momentum idea to alpha in websim (eg: region, universe, some technique?)

---

### 评论 #2 (作者: DK20528, 时间: 1年前)

This paper  offers a groundbreaking contribution to the asset pricing and portfolio management literature. By examining the pervasive nature of value and momentum effects across different asset classes, geographies, and markets, the authors convincingly argue that these phenomena are not confined to equities but are universal.

Their findings challenge the traditional notion that value and momentum are anomalies limited to specific markets or periods. Instead, the study highlights their systematic nature and suggests that these strategies may be rooted in deeper behavioral or risk-based explanations. The empirical approach is rigorous, with an impressive dataset spanning multiple decades and asset classes, including stocks, bonds, currencies, and commodities.

Key strengths of the paper include:

1. **Cross-Asset Analysis:**  The authors’ ability to demonstrate consistency in value and momentum effects across diverse asset classes strengthens the robustness of their findings.
2. **Behavioral and Risk Explanations:**  The discussion of potential drivers—such as overreaction, underreaction, and risk-based explanations—provides a balanced view that invites further exploration.
3. **Portfolio Implications:**  The analysis of how value and momentum strategies interact in a diversified portfolio context is highly relevant for practitioners.

However, there are areas that could benefit from additional discussion:

1. **Market Efficiency:**  The authors touch on the efficiency implications of their findings, but a deeper dive into whether markets can remain inefficient despite the ubiquity of these effects would be valuable.
2. **Implementation Challenges:**  Transaction costs, liquidity constraints, and scalability issues for value and momentum strategies in less liquid markets warrant further examination.
3. **Out-of-Sample Testing:**  As financial markets evolve, exploring how these strategies perform in more recent, potentially algorithm-driven markets would enhance the paper’s applicability.

### Questions Regarding the Paper:

1. **Consistency Across Asset Classes:**  Did the magnitude of the value and momentum effects differ significantly across asset classes (e.g., equities vs. commodities)? Are there any asset classes where these effects are weaker or absent?
2. **Time-Period Sensitivity:**  How stable are the value and momentum effects over time? Have they diminished in more recent years due to increased awareness and exploitation by institutional investors?
3. **Behavioral vs. Risk-Based Explanations:**  The paper discusses both behavioral and risk-based explanations for value and momentum. Do the authors lean toward one explanation as being more plausible, or is the evidence equally split?
4. **Interactions Between Value and Momentum:**  The paper highlights the potential benefits of combining value and momentum strategies. Are there specific conditions or market environments where one strategy consistently outperforms the other?
5. **Data Coverage and Limitations:**  How comprehensive was the dataset used, particularly for non-equity asset classes? Were there any limitations in the data that could bias the results?
6. **Practical Applications:**  What insights does the paper provide for constructing real-world portfolios that balance exposure to value and momentum? How sensitive are the strategies to transaction costs and other implementation frictions?
7. **Impact of Market Microstructure:**  Did the study account for the impact of market microstructure changes, such as the rise of algorithmic trading or changes in liquidity, on value and momentum strategies?

Would you like further assistance with summarizing, critiquing, or exploring specific aspects of the paper?

---

### 评论 #3 (作者: ND68030, 时间: 1年前)

I think the alpha idea would be to vectorize the return neuts according to the mdl57_momentum data to represent momentum, Since I am currently limited fundamental data I cannot test Earnings announcement

---

### 评论 #4 (作者: MK58212, 时间: 1年前)

Thank you for your thoughtful and detailed feedback on our paper. We greatly appreciate your comprehensive analysis of our work, especially your recognition of the cross-asset analysis and the potential behavioral and risk-based explanations for value and momentum effects. Your questions and suggestions for further exploration are incredibly valuable, and we agree that diving deeper into topics like market efficiency, implementation challenges, and the stability of these effects over time would significantly enhance the discussion.

We also appreciate your insightful inquiries regarding the consistency of value and momentum effects across different asset classes, the potential biases in our dataset, and the practical implications for portfolio construction. Your suggestion to explore the impact of market microstructure changes, such as algorithmic trading, is particularly timely and will certainly inform our future work.

Thank you again for your thorough engagement with the paper. Your feedback has provided us with many avenues for further refinement, and we look forward to addressing these important aspects in future revisions.

---

### 评论 #5 (作者: HV77283, 时间: 1年前)

Thank you for your detailed feedback on our paper. We value your analysis, especially on cross-asset insights and behavioral vs. risk-based explanations for value and momentum. Your suggestions on market efficiency, implementation, and algorithmic trading impacts offer valuable directions for future work.

---

### 评论 #6 (作者: XL31477, 时间: 1年前)

**Hey, regarding applying momentum idea to alpha in websim, here are some tips. First, when choosing the region, focus on those with higher trading volumes and liquidity like major stock exchanges. For universe, pick stocks from sectors that historically show strong momentum responses. Technique-wise, you can use a combination of short-term and long-term momentum indicators to capture different trends. Also, consider adjusting the weights based on volatility. Hope these can help you build better alphas.**

---

### 评论 #7 (作者: SK95162, 时间: 1年前)

Thank you for your thoughtful insights. Your contributions on cross-asset analysis, market efficiency, and algorithmic trading are invaluable.

---

### 评论 #8 (作者: SK72105, 时间: 1年前)

I have tried implementing the idea of low correlation between the two factors of momentum and value using risk88 dataset. It works in all regions very well!

---

### 评论 #9 (作者: DN45758, 时间: 1年前)

Thank you for this insightful research, revealing global value and momentum dynamics and their connection to funding liquidity risks.

---

### 评论 #10 (作者: BA51127, 时间: 1年前)

Here's a concise take on how to apply momentum ideas to alpha in websim:

1. **Region Selection** : Opt for regions with higher trading volumes and liquidity, such as major stock exchanges, to capture strong momentum effects.
2. **Universe Filtering** : Choose stocks from sectors that have historically demonstrated significant momentum responses.
3. **Momentum Indicators** : Utilize a mix of short-term and long-term momentum indicators to identify trends across different time frames.
4. **Weight Adjustment** : Consider adjusting the weights of your alpha strategy based on volatility to manage risk effectively.

---

### 评论 #11 (作者: XD81759, 时间: 1年前)

Hey, the paper shows consistent value and momentum return premia across different markets and asset classes. The negative correlation between value and momentum is interesting. When it comes to using these in Brain platform, for value, we can explore fundamental data like fnd23_intfv_value. For momentum, mdl57_momentum could be handy. Also, don't forget to analyze returns data. Combine them properly in your quant strategies and test via backtesting.

---

### 评论 #12 (作者: SJ17125, 时间: 1年前)

[DK20528](/hc/en-us/profiles/24602396283031-DK20528)  The study likely examines the influence of market microstructure changes, such as the rise of algorithmic trading and shifts in liquidity, on the performance of value and momentum strategies. These factors can significantly alter trading costs, execution speed, and market efficiency, potentially impacting the profitability and risk-adjusted returns of these strategies. Addressing such variables would provide a more nuanced understanding of how evolving trading environments influence the effectiveness of traditional investment approaches. I hope it helps.

---

### 评论 #13 (作者: HY45205, 时间: 1年前)

Thank you for taking the time to share your thoughts and insights. It's always valuable to see different perspectives and learn from the experiences of others in the community. Your contribution not only adds depth to the discussion but also inspires others to engage and share their ideas as well. This kind of knowledge exchange is what makes a community thrive and grow stronger. Whether it's an innovative approach, a thoughtful question, or simply an observation, each piece of input helps build a richer understanding for everyone involved. I truly appreciate the effort you’ve put into crafting your post—it’s clear that a lot of thought and expertise went into it. Please keep sharing your ideas and discoveries, as they are incredibly helpful for others who may be exploring similar topics. Once again, thank you for being an active and thoughtful member of the community!

---

### 评论 #14 (作者: AT56452, 时间: 1年前)

The study "Value and Momentum Everywhere" identifies consistent return premia for value and momentum strategies across eight diverse markets and asset classes, revealing a strong common factor structure among their returns. Notably, value and momentum returns exhibit higher correlation across asset classes compared to passive exposures, yet maintain a negative correlation with each other both within and across these classes. The research introduces a three-factor model to characterize these global risks, suggesting that global funding liquidity risk partially explains these patterns. These findings challenge existing asset pricing theories that predominantly focus on U.S. equities.

---

### 评论 #15 (作者: AT56452, 时间: 1年前)

The study's examination of eight diverse markets and asset classes provides a robust analysis of value and momentum strategies, enhancing the generalizability of its findings.

---

### 评论 #16 (作者: AT56452, 时间: 1年前)

Uncovering a strong common factor structure among returns underscores the interconnectedness of global financial markets and the pervasive nature of value and momentum premia.

---

### 评论 #17 (作者: AT56452, 时间: 1年前)

The observation that value and momentum returns correlate more strongly across asset classes than passive exposures suggests that these strategies tap into underlying factors beyond mere market movements.

---

### 评论 #18 (作者: AT56452, 时间: 1年前)

The negative correlation between value and momentum strategies, both within and across asset classes, indicates potential diversification benefits when combining these approaches in investment portfolios.

---

### 评论 #19 (作者: AT56452, 时间: 1年前)

Proposing a three-factor model to characterize global risks offers a new framework for understanding the dynamics influencing value and momentum returns.

---

### 评论 #20 (作者: AT56452, 时间: 1年前)

Identifying global funding liquidity risk as a partial source of the observed patterns highlights the importance of macroeconomic factors in shaping investment strategy outcomes.

---

### 评论 #21 (作者: AT56452, 时间: 1年前)

The findings challenge traditional behavioral, institutional, and rational asset pricing theories, particularly those centered on U.S. equities, prompting a reevaluation of these models in a global context.

---

### 评论 #22 (作者: AT56452, 时间: 1年前)

The negative correlation between value and momentum strategies suggests that investors could achieve better diversification by incorporating both strategies across various asset classes.

---

### 评论 #23 (作者: AT56452, 时间: 1年前)

The study emphasizes that certain risk patterns become identifiable only when value and momentum are examined jointly across markets, indicating the necessity of integrated analysis in financial research.

---

### 评论 #24 (作者: AT56452, 时间: 1年前)

By focusing on multiple markets, the research provides insights that are applicable beyond U.S. equities, offering a more comprehensive understanding of global financial phenomena.

---

### 评论 #25 (作者: CC40930, 时间: 1年前)

This study offers a compelling exploration of value and momentum return premia across diverse markets and asset classes. The identification of a strong common factor structure and the negative correlation between value and momentum, both within and across asset classes, highlights intriguing dynamics. The integration of global funding liquidity risk as a partial explanation enriches the analysis, while the joint examination of value and momentum across markets provides fresh challenges to established asset pricing theories. A fascinating read for anyone interested in cross-asset strategies!

---

### 评论 #26 (作者: VP21767, 时间: 1年前)

This study identifies consistent value and momentum return premia across eight markets and asset classes, with a shared factor structure in their returns. While value and momentum correlate strongly within asset classes, they are negatively correlated with each other. The findings suggest a global risk factor, characterized by a three-factor model, partly driven by global funding liquidity risk. This challenges traditional asset pricing theories that focus predominantly on U.S. equities.

---

### 评论 #27 (作者: SV11672, 时间: 1年前)

The study's emphasis on the importance of considering value and momentum jointly across markets is a key takeaway. By examining these factors in a global context, the authors are able to identify patterns and risks that may not be apparent when focusing on a single market or asset class. The findings also highlight the need for investors to adopt a more nuanced and globally-aware approach to portfolio construction and risk management.

---

### 评论 #28 (作者: SV11672, 时间: 1年前)

"Fascinating study on the consistent value and momentum return premia across diverse markets and asset classes! The findings of a strong common factor structure among their returns and the negative correlation between value and momentum are particularly noteworthy. The identification of global funding liquidity risk as a partial source of these patterns is also insightful. The study's results pose a significant challenge to existing asset pricing theories, highlighting the need for more comprehensive and globally-focused frameworks

---

### 评论 #29 (作者: VP21767, 时间: 1年前)

The paper provides a compelling exploration of value and momentum return premia across diverse markets, emphasizing their negative correlation. The identification of global funding liquidity risk as a common factor is intriguing, challenging traditional asset pricing theories. It would be interesting to further analyze how these dynamics interact during periods of economic volatility or in emerging markets. Could additional factors amplify or mitigate these return premia?

---

### 评论 #30 (作者: VP21767, 时间: 1年前)

This paper provides a comprehensive analysis of value and momentum return premia across diverse markets, emphasizing their negative correlation. The identification of global funding liquidity risk as a shared factor challenges traditional asset pricing models. This research adds depth to the understanding of how value and momentum interact, offering significant insights into global risk factors influencing asset returns.

---

### 评论 #31 (作者: VP21767, 时间: 1年前)

The study explores the dynamics of value and momentum return premia across various markets, highlighting their inverse relationship and shared sensitivity to global funding liquidity risks. By uncovering a common factor structure, the research challenges conventional asset pricing theories, offering fresh perspectives on how these strategies interact and contribute to broader market behaviors. This analysis deepens our understanding of cross-asset risk factors shaping financial returns.

---

### 评论 #32 (作者: VP21767, 时间: 1年前)

The research examines value and momentum return premia across multiple markets, revealing their negative correlation and shared exposure to global liquidity risks. It identifies a common factor structure, challenging traditional asset pricing models and providing insights into how these strategies interact and influence financial returns across diverse asset classes.

---

### 评论 #33 (作者: AK98027, 时间: 1年前)

Thank you for your research illuminating the relationship between funding liquidity risks and their effects on global value and momentum factors. Your analysis provides valuable insights into these market dynamics.

---

### 评论 #34 (作者: CT68712, 时间: 1年前)

Hey大家！我最近讀了一篇關於價值和動量的研究，發現這些回報溢價在不同市場和資產類別之間都有一致性，這真是太酷了！特別是關於全球資金流動性風險的部分，讓我想起了量化交易中建立模型時，風險因素的重要性。我覺得這不僅能幫助我們理解市場的行為，同時也能提升我們的交易策略。如果有玩過類似的量化模型，大家可以分享一下你們的經驗嗎？這樣我也能學習到更多！

---

### 评论 #35 (作者: HT59568, 时间: 1年前)

**Impact of earnings announcements:**  How do earnings announcements (fnd23_intfv_value) interact with value and momentum premia in global markets?

---

### 评论 #36 (作者: HT59568, 时间: 1年前)

**Momentum modeling:**  How does the mdl57_momentum dataset enhance the understanding of momentum effects in global asset classes?

---

### 评论 #37 (作者: HT59568, 时间: 1年前)

**Challenge to asset pricing theories:**  How do the findings challenge existing behavioral, institutional, and rational asset pricing theories focused on U.S. equities?

---

### 评论 #38 (作者: HT59568, 时间: 1年前)

**Joint examination of value and momentum:**  Why is examining value and momentum jointly across markets essential to identifying common global risks?

---

### 评论 #39 (作者: HT59568, 时间: 1年前)

**Global funding liquidity risk:**  In what ways does global funding liquidity risk partially explain the observed patterns in value and momentum premia?

---

### 评论 #40 (作者: HT59568, 时间: 1年前)

**Three-factor model:**  How does the three-factor model characterize the global risks driving value and momentum returns?

---

### 评论 #41 (作者: HT59568, 时间: 1年前)

**Negative correlation between value and momentum:**  What explains the negative correlation between value and momentum returns both within and across asset classes?

---

### 评论 #42 (作者: HT59568, 时间: 1年前)

**Correlation across asset classes:**  Why do value and momentum returns correlate more strongly across asset classes than passive exposures?

---

### 评论 #43 (作者: HT59568, 时间: 1年前)

**Common factor structure:**  What evidence supports the existence of a strong common factor structure among value and momentum returns across asset classes?

---

### 评论 #44 (作者: HT59568, 时间: 1年前)

**Value and momentum premia across markets:**  How do value and momentum return premia consistently manifest across eight diverse markets and asset classes?

---

### 评论 #45 (作者: KS69567, 时间: 1年前)

This paper makes a groundbreaking contribution to  **asset pricing**  and  **portfolio management**  by demonstrating that  **value**  and  **momentum**  effects are pervasive across various asset classes, geographies, and markets. The authors provide compelling evidence that these phenomena are not limited to equities but are universal, influencing a wide range of investment opportunities. This insight broadens the scope of value and momentum strategies, showing their applicability and potential across diverse financial contexts.

---

### 评论 #46 (作者: KS69567, 时间: 1年前)

The study delves into the dynamics of  **value**  and  **momentum return premia**  across various markets, revealing their  **inverse relationship**  and shared sensitivity to  **global funding liquidity risks** . By identifying a common factor structure, the research challenges traditional  **asset pricing theories**  and offers new insights into how these strategies interact, influencing broader market behaviors. This analysis enhances our understanding of the  **cross-asset risk factors**  that shape financial returns, providing a more comprehensive framework for portfolio management and asset pricing strategies.

---

