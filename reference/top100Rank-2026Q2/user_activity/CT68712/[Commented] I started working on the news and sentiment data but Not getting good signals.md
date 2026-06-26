# I started working on the news and sentiment data but Not getting good signals

- **链接**: [Commented] I started working on the news and sentiment data but Not getting good signals.md
- **作者**: RB25229
- **发布时间/热度**: 1年前, 得票: 21

## 帖子正文

Is creating single dataset alpha with news and sentiment data is tough as compared to other dataset. I have noticed that the general iterations which work with the other data like other and model, analyst. What are the general iterations which can work on these data as well.?

---

## 讨论与评论 (14)

### 评论 #1 (作者: YW42946, 时间: 1年前)

Compared to model, and other categories. Sentiment and news type dataset usually requires more data cleansing and processing before able to extract signal from the data source. You may want to put more time and effort into each dataset as each dataset will require more attention.

You may also want to build Alpha starting from strong economic foundation. Below is some research paper for your reference. For more dataset details, you may reach out to your designated advisor.

[Research Paper 80: News and Social Media Emotions in the Commodity Market – WorldQuant BRAIN](../CC40930/[Commented] Research Paper 80 News and Social Media Emotions in the Commodity Market置顶的.md)

---

### 评论 #2 (作者: ZH78994, 时间: 1年前)

I would like to express my heartfelt gratitude for your generous sharing. Your willingness to offer your time, knowledge, and resources means a great deal to me. The insights you've provided have not only broadened my understanding but also inspired me to take positive steps forward. It's rare to encounter someone so selfless and giving, and I truly appreciate the impact you've had. Thank you for your kindness and for being such a valuable source of support. Your gesture will be remembered, and I am grateful for the opportunity to learn from you.

---

### 评论 #3 (作者: CC40930, 时间: 1年前)

Creating a single dataset alpha using news and sentiment data can indeed present unique challenges compared to other datasets like fundamental, model, or analyst data. The difficulty often arises from the unstructured nature of news and sentiment data, as well as the challenges in quantifying and interpreting sentiment.

---

### 评论 #4 (作者: PL15523, 时间: 1年前)

Creating Single Dataset Alphas with news and sentiment data can be tough, but try sentiment filtering, time-series analysis, cross-sectional ranking, event-driven strategies, and neutralization by sector or industry.

---

### 评论 #5 (作者: NH84459, 时间: 1年前)

You're absolutely right that  **Sentiment**  and  **News-type datasets**  require more data cleansing and processing compared to other categories like  **Model**  or  **Fundamental**  datasets. The complexity of these datasets comes from the unstructured nature of the data (e.g., news articles, social media posts, etc.), which requires significant preprocessing to extract meaningful signals. Let’s break down some important steps for working with these datasets and tips on how to build an Alpha model from a strong  **economic foundation** :

---

### 评论 #6 (作者: NH84459, 时间: 1年前)

Creating a single dataset alpha using  **news and sentiment data**  can indeed be more complex than traditional alphas based on  **price, volume, or fundamental data** , as the nature of this data is inherently more  **unstructured**  and  **noisy** . However, with the right approach, you can effectively leverage news and sentiment data to create alpha signals.

---

### 评论 #7 (作者: RB20756, 时间: 1年前)

Creating single dataset alphas using news and sentiment data can be very challenging due to unstructured nature which often leads to higher turnover in comparison to model, fundamental dataset. One can try winsorize or filter type operators to remove outliers from the signals. Further data  cleansing and processing is required to extract meaningful signals from it.

---

### 评论 #8 (作者: QG16026, 时间: 1年前)

Your suggestions on filtering, cleansing, and neutralization will be really useful as I navigate these more complex datasets. It’s great to have this kind of advice to help make the process smoother. Thanks again for sharing your knowledge and experience.

---

### 评论 #9 (作者: CT68712, 时间: 1年前)

Creating single dataset alphas with news and sentiment data does sound like a tough challenge! As a tech enthusiast and a quant trader, I've learned that data cleansing is crucial

---

### 评论 #10 (作者: PP87148, 时间: 1年前)

Sentiment and news datasets are harder to work with than price or fundamental data due to their unstructured and noisy nature. However, with proper preprocessing and a strong economic base, they can be transformed into effective alpha signals.

---

### 评论 #11 (作者: AC63290, 时间: 1年前)

Let me help you with both the code error and provide guidance on working with sentiment datasets:

### Code Error Fix

Your code has several typos. Here's the corrected version:

```
alpha_list = [ace.generate_alpha(x, 
    region="GLB",
    universe="MINVOL",
    neutralization="STATISTICAL",
    decay=0,
    test_period="P2Y") for x in alpha_list]

```

Key corrections:

- "testperied" → "test_period"
- Fixed spelling of "generate_alpha"
- Corrected parameter names and values

### Working with Sentiment Datasets

Sentiment datasets can be more challenging because:

1. Higher noise levels
2. More complex relationships with price movements
3. Time-sensitive nature of sentiment signals

Here are effective approaches for sentiment data:

1. **Basic Operations**

- Use smoothing operations to reduce noise:
  - `ts_mean(sentiment, 5)`
  - `ts_median(news_score, 3)`
  - `ewma(sentiment_score, 0.6)`

1. **Turnover Management**

- Control signal stability:
  - `ts_rank(sentiment_score, 10)`
  - `decay_linear(news_impact, 5)`
  - `ts_delta(sentiment, 3)`

1. **Signal Combinations**

- Combine with price/volume:
  - `correlation(sentiment, returns, 20)`
  - `ts_mean(sentiment * volume, 5)`
  - `rank(sentiment) * rank(price_change)`

1. **Best Practices**

- Use longer time windows for stability
- Implement proper neutralization
- Consider market impact delays
- Monitor turnover carefully
- Test across different market regimes

Remember to validate signals thoroughly as sentiment data can be more volatile than traditional financial metrics.

---

### 评论 #12 (作者: PT27687, 时间: 1年前)

Creating a dataset that effectively integrates news and sentiment data can indeed be challenging. Have you considered exploring different feature engineering techniques or perhaps applying various machine learning algorithms specifically designed to capture temporal trends? Additionally, it might be helpful to look into combining this data with quantitative metrics to see if that enhances your results.

---

### 评论 #13 (作者: RB98150, 时间: 1年前)

Smooth data, use short lookbacks, focus on events, mix with price action, and filter extreme sentiment shifts.

---

### 评论 #14 (作者: MA97359, 时间: 1年前)

To get started with  **News Datasets** , check out this link

[../AM60509/[Commented] Getting started with News DatasetsResearch.md](../AM60509/[Commented] Getting started with News DatasetsResearch.md)

It covers key sources, impact analysis, and strategies for integrating news data into your alpha research

---

