# [GLB Theme] On Dealing With FX In Multi-Currency Regions

- **链接**: [Commented] [GLB Theme] On Dealing With FX In Multi-Currency Regions.md
- **作者**: Di Sheng Tan
- **发布时间/热度**: 2年前, 得票: 17

## 帖子正文

# Introduction

With the launch of GLB, we have yet another region with multiple currencies across the instruments within the same region. Other such regions include EUR and ASI.

When dealing with such regions, we need to be aware of the effects of the different currencies on our Alphas.

There are two main effects that arise from differing currencies: 1) differing range in currencies, 2) differing volatility in currencies.

# Recipes For Mitigating Effects From Different Currencies

Suppose we have a simple hypothesis, our belief is that stocks that have higher revenue than their peers should have their prices appreciate relative to their peers, and vice versa.

We implement that Alpha with  **revenue** .

- **Effect:** Differing Ranges In Currencies
  - **Mitigating Recipe:**  Time Series Operators
  - **Example Implementation:** ts_rank(revenue, d)
  - **Implementation Effect:** Transform range of the raw currency data field into the same range by doing temporal comparison across the same currency (and instrument)
  - **Mitigating Recipe:**  Cross Sectional Operators
  - **Example Implementation:** groups = (exchange + 1)*1000 + industry; group_scale(revenue, densify(groups))
  - **Implementation Effect:** Transform range of the raw currency data field into the same range by doing cross-sectional comparison across the same currency (and instrument).
  - **Notes:** We can create custom groupings of double or even triple sorts by shifting the indices of the groups. This allows us to first group stocks of the same currency into the same group and then further group them into sector/industry/subindustry groupings that can aid our cross-sectional Alpha. The trick here is to add 1 to the 0 index in the exchange group, so that we can scale the exchange group indices by 1000. The scaling constant is arbitrary, but has to be larger than the number of the second group (industry in this case). When we add the transformed exchange group indices to the industry group indices, we get every unique combination of (exchange, industry) grouping. We can extend this idea to any arbitrary N sorting of groups.
  - **Mitigating Recipe:**  Divide fields of the same currency
  - **Example Implementation:** revenue / close
  - **Implementation Effect:** Transforms the raw currency data field into a unitless data field that can be compared fairly across the instruments.
  - **Mitigating Recipe:**  Approximate currency conversions
  - **Example Implementation:** currency_conversion_field = mdl25_cbv421_7v / mdl25_cbv421_6v; revenue_USD = revenue*currency_conversion_field; revenue_USD
  - **Implementation Effect:** By creating our own estimates of a currency conversion field. We can transform any local currency denominated field into a USD denominated field for fair comparison across the instruments.
  - **Notes:** We can find fields in every multi-currency region that have a local currency representation of the field, and a USD representation of that field. For example, in GLB, we have mdl25_cbv421_6v, which the market cap in local currency with 100% coverage. We also have mdl25_cbv421_7v, which is the market cap in USD with 100% coverage. We can approximate a currency conversion field by dividing the USD denominated field by the local denominated field.
  - **Effect:** Differing Volatility In Currencies
  - **Mitigating Recipe:**  Gross Returns Volatility Scaling
  - **Example Implementation:** gross_volatility = ts_std_dev(ts_returns(mdl25_cbv421_6v, 2), d); revenue_gross_scaled = revenue / gross_volatility; revenue_gross_scaled
  - **Implementation Effect:** Mitigate weights changing drastically due the currency volatility effects. In this case, we are also reducing weights relative to the volatility of the underlying instrument movement.
  - **Notes:**  This volatility is going to be a combination of two effects: the volatility of the underlying stock, and the volatility of the local currency. If we divide each data field by the volatility, we can mitigate the volatility of the currency, although this is likely inefficient and a roundabout way of mitigating the currency volatility effect. In most cases, the volatility of the stock prices will also dominate the volatility of the currency. This method should be used when your intention is to scale by volatility, and want to include the currency effects in your volatility scaling.
  - **Mitigating Recipe:**  Currency Returns Volatility Scaling
  - **Example Implementation:** gross_volatility = ts_std_dev(ts_returns(mdl25_cbv421_6v, 2), d); revenue_gross_scaled = revenue / gross_volatility; revenue_gross_scaled
  - **Implementation Effect:** Mitigate weights changing drastically due the currency volatility effects.

# Elaboration: Effects of Differing Range In Currencies

This effect will show whenever we deal with fields that are denominated in different currencies. Examples of such fields include: open, high, low, close, and fields with descriptions that include "price" or "dollars" without being divided, normalized or converted.

Suppose we have a simple hypothesis, our belief is that stocks that have higher revenue than their peers should have their prices appreciate relative to their peers, and vice versa.

We implement that Alpha with  **revenue** .

We can observe the effect of differing range in currencies as follows:

**Instrument**

**Revenue**

**Revenue (USD)**

**Data Field Value**

**Weight**

**Data Field Value**

**Weight**

**Amazon (USA)**

**(USD) 150B**

**0.015**

**(USD) 150B**

**0.667**

**Toyota (JPN)**

**(JPY) 10T**

**0.982**

**(USD) 70B**

**0.311**

**Moutai (CHN)**

**(CNY) 35B**

**0.003**

**(USD) 4.9B**

**0.02**

The effect goes as follows:

1. We have revenue from 3 securities, each from a different country, denominated by a different currency. These securities are Amazon from USA, Toyota from JPN and Moutai from CHN.
2. When we convert their revenue into weights, we get a staggering concentration in Toyota, this is because the JPY currency is dominating the other currencies in range.
3. This unconverted revenue Alpha is also wrong, as Toyota does not actually have more revenue than Amazon, and does thus the weights do not reflect our original hypothesis.
4. If we convert the revenue into USD, at an exchange rate of 0.007USD/JPY and 0.14USD/CHN, our USD-denominated revenue will be (USD150B, USD70B, USD4.9B).
5. Our  **revenue** Alpha will now produce weights of (0.667, 0.311, 0.022), which reflect the original hypothesis.

Hence, we need methods that allow us to deal with the different scale in currencies. As seen above, we can take 4 main methods.

1. Use time-series operators such as  **ts_rank** and  **ts_scale**  to transform the data fields with differing currencies into the same range.
2. Use cross-sectional operators that can normalize/standardize field values among stocks with the same currencies. An example of this include:  **group_neutralize(x, country)** .
3. We can also transform fields that are denominated in currencies into unitless fields by dividing them by other fields that are denominated in currencies. An example of this is  **revenue/close** .
4. If we can find a field that is denominated in the original currency (e.g. market_cap), and another field that has been converted into USD (e.g. market_cap_usd), then we can approximate the currency conversion by taking  **market_cap_usd / market_cap.** We can then use the approximate currency conversion to perform conversions to other fields not denominated in USD.

# Elaboration: Effects of Differing Volatilities In Currencies

This effect will show whenever we deal with fields that contain stocks with different prices, regardless of whether or not we have converted them into the same currency, normalized them, or transformed them into unitless ratios.

Continuing from our previous hypothesis, let's consider the same securities: AMZN from USA, 7203 (Toyota) from JPY, and 600519 (Moutai) from CHN. This time, however, we will focus on the volatility of their respective currencies.

The volatility of a currency can significantly impact the value of a security. For instance, if the JPY experiences high volatility, it could lead to drastic changes in the value of 7203 (Toyota), even if the company's fundamentals remain the same. This volatility can distort the true performance of the security when compared to its peers.

Let's illustrate this with an example. Suppose the USD/JPY exchange rate is highly volatile, fluctuating between 0.007USD/JPY and 0.009USD/JPY within a short period. If we convert the revenue of 7203 (Toyota) into USD during this period, the USD-denominated revenue could range from USD70B to USD90B.

Note that with a 0.007USD/JPY conversion rate, the weights of our  **revenue** Alpha will be (0.667, 0.311, 0.022), but with a 0.009USD/JPY conversion rate, the weights of our revenue Alpha will now be (0.613 , 0.367, 0.020).

This wide range led to significant changes in the weights of our portfolio, even through the fundamentals of the company has not changed, and according to original hypothesis, the weights should not have changed.

One method of mitigating the effects of different volatilities in currencies is to perform volatility scaling. Two methods have been provided above.

# Conclusion

Currencies have a profound effect on our Alphas when we are dealing with multi-currency regions. Knowing how to deal with the effects of the range and volatility of differing currencies will allow you to create Alphas with fields denominated in different currencies that have more fundamental sense.

---

## 讨论与评论 (9)

### 评论 #1 (作者: XL31477, 时间: 1年前)

Hey, great analysis here, mate! When dealing with multi-currency regions indeed, those methods for mitigating effects of different ranges and volatilities in currencies are crucial. For range issues, like using time-series or cross-sectional operators makes sense to standardize data. And for volatility, volatility scaling helps stabilize weights. Just gotta pick the right approach based on the specific situation of our Alphas to make them more reliable and reflect our hypotheses well.

---

### 评论 #2 (作者: TP14664, 时间: 1年前)

Hi, I hope in the coming weeks there will be more themes to improve daily payment. Thanks a lot everyone

---

### 评论 #3 (作者: CC40930, 时间: 1年前)

This post provides a detailed guide on how to mitigate the effects of differing currencies when constructing Alpha strategies. The two main challenges highlighted are the differing ranges and volatilities across currencies. The proposed solutions, such as using time-series operators like  `ts_rank`  and  `ts_scale` , cross-sectional operators like  `group_scale` , and dividing fields by denominated currencies (e.g., revenue/close), offer valuable techniques to normalize and scale data appropriately. Additionally, the methods for addressing currency volatility, including gross returns volatility scaling, provide a solid foundation for reducing the impact of fluctuating exchange rates on Alpha performance. By incorporating these strategies, you can improve the robustness and fairness of multi-currency Alpha models, ensuring they are more aligned with the fundamentals of the assets being analyzed.

---

### 评论 #4 (作者: PL15523, 时间: 1年前)

- **Range** : Normalize with time-series ( `ts_rank` ), cross-sectional operators, or by dividing currency fields (e.g., revenue/close).
- **Volatility** : Scale by volatility using  `gross_volatility`  or  `currency_returns_volatility`  to reduce distortions in alpha weights.

---

### 评论 #5 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #6 (作者: ND68030, 时间: 1年前)

When dealing with regions that have multiple currencies across different instruments, such as  **GLB** ,  **EUR** , and  **ASI** , it’s important to understand how the  **differing currencies**  can impact the performance of your  **Alphas** . The presence of multiple currencies introduces two key effects that can influence the returns, risks, and overall performance of your strategies:

---

### 评论 #7 (作者: QG16026, 时间: 1年前)

The two main factors at play are differing currency ranges and volatility, each influencing the performance of your models. By utilizing techniques like time-series operators, cross-sectional adjustments, and volatility scaling, you can better handle these effects, ensuring more reliable and accurate Alpha results across different currencies

---

### 评论 #8 (作者: AK98027, 时间: 1年前)

When dealing with regions that have multiple currencies across different instruments, such as  **GLB** ,  **EUR** , and  **ASI** , it’s important to understand how the  **differing currencies**  can impact the performance of your  **Alphas** . The presence of multiple currencies introduces two key effects that can influence the returns, risks, and overall performance of your strategies.

---

### 评论 #9 (作者: KS24487, 时间: 1年前)

> This post provides a detailed guide on how to mitigate the effects of differing currencies when constructing Alpha strategies. The two main challenges highlighted are the differing ranges and volat...

Interesting.

---

