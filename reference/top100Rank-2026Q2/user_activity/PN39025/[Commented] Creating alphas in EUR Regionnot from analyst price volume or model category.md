# Creating alphas in EUR Region(not from analyst, price volume or model category)

- **链接**: [Commented] Creating alphas in EUR Regionnot from analyst price volume or model category.md
- **作者**: SV70703
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

Can someone guide me on how to make alphas in the EUR region? I am unable to crack any alphas in categories other than model, analyst and price volume.

---

## 讨论与评论 (17)

### 评论 #1 (作者: PL15523, 时间: 1年前)

Hi, you can simulate the alphas on the USA price volume market and simulate on the EUR market. Usually the os performance of the EUR market is not very good, so be careful of overfitting

---

### 评论 #2 (作者: NH84459, 时间: 1年前)

You can study options on the EUR market. I find that EUR option data usually has good out samples. Please combine with data price volume

---

### 评论 #3 (作者: SK72105, 时间: 1年前)

risk88, and risk70 datafields work well, however they are somewhat similar to some model datasets! If you haven't tried fundamental data, I would encourage you to try "Global Fundamental Data", and "Aggregated Fundamental Data" Datasets

---

### 评论 #4 (作者: AC63290, 时间: 1年前)

You can read paper 101 formulic alphas, then deploy these alphas on the EUR market. I see many alphas giving very positive signals, however need to pay attention to reduce turnover

---

### 评论 #5 (作者: TD84322, 时间: 1年前)

Try working with the option dataset; there are some useful templates available in the community. It’s not overly difficult, but be cautious when handling missing data, ensuring sufficient coverage, and managing high turnover. These aspects are important to get accurate and reliable results.

---

### 评论 #6 (作者: DN41247, 时间: 1年前)

Here are some tips for creating alphas in the EUR region:

1. **Simulate on USA First** : Test alphas on the USA price-volume market and simulate them on EUR. Be mindful of overfitting as EUR market out-of-sample (OS) performance can be less reliable.
2. **Options Data** : EUR options data often provides good OS results. Combine it with price-volume data, ensuring proper handling of missing data and managing turnover.
3. **Risk and Fundamental Datasets** : Use  `risk88`  and  `risk70`  fields, or diversify with  **Global Fundamental Data**  and  **Aggregated Fundamental Data**  for broader insights.
4. **Leverage Research** : Apply ideas from  *101 Formulic Alphas*  and focus on strategies with low turnover to reduce costs.
5. **Community Templates** : Start with shared templates for EUR options and datasets, adapting them to the region’s dynamics.

Experiment, monitor results, and refine for better performance! 🚀

---

### 评论 #7 (作者: PN39025, 时间: 1年前)

Most of the alpha I do is in EURO and I find if you don't have much experience in EURO region you should try using fundamental dataset and Analyst the performance of those datasets is quite good

---

### 评论 #8 (作者: TD84322, 时间: 1年前)

Creating alphas outside model, analyst, and price-volume categories is tough. Try revisiting model or analyst-based approaches while ensuring good coverage and balanced long/short counts. Stay patient and keep experimenting!

---

### 评论 #9 (作者: TN74933, 时间: 1年前)

I think you can try using the risk dataset; I usually combine it with the model dataset for better results, goodluck

---

### 评论 #10 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #11 (作者: CT68712, 时间: 1年前)

Hi, everyone! As a tech enthusiast, I'm diving into the world of quantitative trading, and I've been exploring ways to create alpha in the EUR region. It's fascinating yet challenging! I've noticed that using fundamental datasets and options data can yield interesting insights.

Recently, I came across advice about experimenting with models and ensuring you have good coverage to avoid overfitting. I'm all about the data-driven approach, so I'm excited to see how combining the risk datasets with the options can enhance results.

If anyone has templates or further tips on navigating the intricacies of the EUR market, please share! Let's connect and learn from each other's experiences. Happy trading!

---

### 评论 #12 (作者: RB20756, 时间: 1年前)

Your insights into EUR alpha creation are incredibly valuable! Exploring fundamental and options datasets while balancing risk factors is a smart approach. Testing on the USA market first and leveraging community templates can further refine strategies. Looking forward to more shared discoveries—happy trading! 🚀

---

### 评论 #13 (作者: NP85445, 时间: 1年前)

Fundamental datasets, especially  **Global Fundamental Data**  and  **Aggregated Fundamental Data** , often provide stable signals if combined with well-structured ranking functions. Additionally,  **risk datasets like risk88 and risk70**  can enhance robustness, though they might share similarities with model-based data.

---

### 评论 #14 (作者: ML46209, 时间: 1年前)

If you want to create alphas in the EUR region without relying on model, analyst, or price-volume data, you could try combining options data with risk datasets like risk88 and risk70. These datasets can provide more stable signals, especially when integrated with fundamental data such as "Global Fundamental Data" or "Aggregated Fundamental Data."

Additionally, experimenting with low-turnover strategies can help reduce transaction costs and minimize overfitting. Another approach is to first test your alphas in the US market, then fine-tune and apply them to the EUR region for better out-of-sample performance evaluation. Good luck!

---

### 评论 #15 (作者: RB98150, 时间: 1年前)

Try alphas from sentiment (news, social media), macr and market patterns

---

### 评论 #16 (作者: MA97359, 时间: 1年前)

Use news datasets with  `tradewhen`  to detect events and trade accordingly. Risk datasets are also well-covered and can generate strong alpha signals.

---

### 评论 #17 (作者: PT27687, 时间: 1年前)

Exploring alternative methods to create alphas is an interesting challenge! Have you considered looking into macroeconomic factors or regional news events that might affect market sentiment? Diving into behavioral finance or sentiment analysis could potentially lead to unique insights as well. What other strategies have you tried so far?

---

