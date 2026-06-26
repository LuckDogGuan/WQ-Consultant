# Filtering Super Alpha Own Pool vs Expanded Alpha Pool

- **链接**: [Commented] Filtering Super Alpha Own Pool vs Expanded Alpha Pool.md
- **作者**: PP87148
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

For each SuperAlpha a consultant submits from their own pool of Alphas, they will be permitted an equivalent allocation to select whether to submit a SuperAlpha using the expanded Alpha pool (based on their then-current Genius level) as their SuperAlpha submission on a subsequent day.

For this purpose you can use below selection expression if you want to select the alpha from your own pool only.

***(Selection Expression) * OWN***

---

## 讨论与评论 (25)

### 评论 #1 (作者: UG81605, 时间: 1年前)

For own pool alpha i give them colors. And in the selection expression filter out using code, color=="GREEN" .
Also one shld give proper tags to the alphas, so that you can combine several data categories alphas, example fundamental + analyst alphas and make a superalpha. This also ensures less correlation from pools as your own alphas will be unique to consultant pool

---

### 评论 #2 (作者: CC40930, 时间: 1年前)

To filter out own pool and expanded pool alphas for SuperAlpha submission, you can tag each alpha based on its origin (own pool or expanded pool). For own pool alphas, filter based on the consultant's unique ID or submission source. For expanded pool alphas, filter based on the consultant's current Genius level. This allows you to separate the two types and ensure proper selection when submitting a SuperAlpha

---

### 评论 #3 (作者: PP87148, 时间: 1年前)

To focus solely on your own alpha in the Super Alpha selection, use the following selection expression:

## ***(Selection Expression) * OWN***

---

### 评论 #4 (作者: NS94943, 时间: 1年前)

Hi  [PP87148](/hc/en-us/profiles/11771952650775-PP87148) ,

Thank you for this update. Frankly I didn't know about this OWN operator! This will make things easier to segregate self pool and consultant pool alphas.

---

### 评论 #5 (作者: DP11917, 时间: 1年前)

Hi, to select alpha in your pool, filter by color or alpha id, this is the easiest way. Or you can also set by tag or type category

---

### 评论 #6 (作者: TL60820, 时间: 1年前)

Hi  [PP87148](/hc/en-us/profiles/11771952650775-PP87148)

Thank you for shedding light on this for me; I really appreciate your help in clarifying the details. I wanted to ask if there is any detailed documentation or reference material available for "OWN" on the platform. If so, could you kindly point me in the right direction to access it?

Thanks again for your guidance!

---

### 评论 #7 (作者: TW77745, 时间: 1年前)

When submitting SuperAlphas, consultants can choose between their  **own pool**  or the  **expanded Alpha pool** , depending on their Genius level. If you prefer using your  **own pool** , the selection expression  `(Selection Expression) * OWN`  ensures only your own Alphas are considered for the SuperAlpha submission. This approach maintains focus on your developed signals while allowing flexibility to leverage the expanded pool on other days.

---

### 评论 #8 (作者: PP87148, 时间: 1年前)

Hi  [DP11917](/hc/en-us/profiles/18243546243735-DP11917) ,

You can select alphas based on color or any given tag, but this doesn't guarantee that you will select alphas only from your own pool, as other consultants may use the same tag or color.

The best way to ensure you select your own alphas is to use the following expression:

## ***(Selection Expression) * OWN***

---

### 评论 #9 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #10 (作者: ND68030, 时间: 1年前)

The Genius level of consultants is an important factor that determines their authority when selecting Alpha from the Expanded Alpha Pool. Using the Genius level as a criterion helps classify and distribute privileges fairly, based on each individual’s capabilities and practical experience. This creates a dynamic system where those with better skills and performance can access a wider range of choices, encouraging personal development while simultaneously optimizing the quality of decisions made.

---

### 评论 #11 (作者: PN39025, 时间: 1年前)

We can use various methods to filter regular alpha, but I believe the most effective approach is to combine  **multiplication operations**  with additional conditions to enhance accuracy and avoid unwanted correlations.

Using multiplication allows us to capture nonlinear relationships between factors, which can help identify stronger alpha signals

---

### 评论 #12 (作者: CC40930, 时间: 1年前)

Great approach to managing your SuperAlpha submissions! By using the "OWN" expression, you ensure that your alpha is selected solely from your personal pool, which can help streamline the process and maintain consistency in your submissions. It's always beneficial to have a clear strategy for how to allocate your alphas, especially as you scale up and explore expanded pools based on your Genius level.

---

### 评论 #13 (作者: CT68712, 时间: 1年前)

我覺得使用 OWN 表達式來過濾自己池中的 Alpha 是一個超棒的想法！這樣不僅能讓我們專注於自己開發的信號，還能有效地管理 SuperAlpha 的提交過程。對於我們這些剛開始進入量化交易的菜鳥來說，了解如何利用這些工具真的是一項重要的技能。希望能看到更多人分享他們的實踐經驗，這樣我們大家都能一起進步！加油！

---

### 评论 #14 (作者: NT63388, 时间: 1年前)

When using COLOR or tags to select Alpha from my pool, I'm getting inconsistent results. I've had more success with NAME.

And to make sure only the correct Alphas are returned, the SELECTION HANDLING must be "Positive."

---

### 评论 #15 (作者: TD84322, 时间: 1年前)

Nice strategy for managing your SuperAlpha submissions! The "OWN" expression keeps your alpha consistent and efficient. It’s smart to plan how you allocate alphas, especially as you grow with your Genius level.

---

### 评论 #16 (作者: AB15407, 时间: 1年前)

The fact that OWN allows selecting Alphas only from my own pool is a very welcome improvement to the platform. 
I look forward to further platform enhancements for Super, such as greater flexibility by allowing selection based on Country, University, and even the ability to select or exclude individual Alphas (not in my pool).

---

### 评论 #17 (作者: MY83791, 时间: 1年前)

A really effective approach for making superalpha is as follow:

```
own*(in(datasets, "datasetname")*long_count / sqrt(universe_size(universe)) * (turnover < 0.20))
```

---

### 评论 #18 (作者: CT68712, 时间: 1年前)

Hi PP87148, I really appreciate your insights on using the OWN expression for filtering alphas from our own pool! As a newbie in quantitative trading, this is super helpful for me to streamline my SuperAlpha submissions. I love how this allows us to maintain focus on our unique signals while also giving us the flexibility to explore the expanded pool. I’m excited to put this technique into practice and hope to learn more from others in the community. Keep up the great work everyone!

---

### 评论 #19 (作者: CC40930, 时间: 1年前)

This approach of submitting a SuperAlpha from one's own pool while allowing the option to use the expanded Alpha pool based on Genius level is a great way to encourage users to leverage their unique insights while also pushing them to explore a broader set of strategies. By offering the flexibility to choose between using the own pool or the expanded pool, it allows for a balance of personal strategy and the opportunity for growth through a larger variety of alphas.

Using the selection expression  `(Selection Expression) * OWN`  for selecting only from their own pool ensures that users can focus on their personalized alphas, which is a smart way to maintain control over their submissions while adhering to the rules.

This process promotes a deeper engagement with the alphas they’ve created and allows consultants to feel more connected to their own work, while also offering them an incentive to step up and expand their strategy pool as they progress through the Genius levels. It creates a fun and motivational loop! 🎯

---

### 评论 #20 (作者: NP85445, 时间: 1年前)

Using the OWN expression really simplifies filtering for your own pool, keeping your SuperAlpha submissions unique and consistent. Combining it with proper tagging (or even filtering by name) seems to be a smart approach to avoid picking up unwanted signals from the expanded pool. Anyone found other tricks to further refine the selection?

---

### 评论 #21 (作者: QG16026, 时间: 1年前)

Fowing users to submit a SuperAlpha from their own pool while also providing access to the expanded Alpha pool based on their Genius level is a great way to encourage both individual insights and broader strategy exploration. This flexibility enables users to balance their personal strategies with opportunities for growth by incorporating a wider range of alphas

---

### 评论 #22 (作者: AS16039, 时间: 1年前)

Use  **(Selection Expression) * OWN**  to ensure SuperAlpha selection from your own pool. Tagging, naming, or color filtering can help but may introduce inconsistencies. Expanded Alpha pool access depends on  **Genius level** , allowing flexibility.

---

### 评论 #23 (作者: PT27687, 时间: 1年前)

This is an intriguing concept regarding the use of Super Alpha submissions! I'm curious about how the Genius level influences the effectiveness of selecting Alphas from the expanded pool. Could you explain how this integration might enhance overall strategy and outcomes? It seems like there’s a lot of potential here!

---

### 评论 #24 (作者: RB98150, 时间: 1年前)

Use  **(Selection Expression) * OWN**  to submit a SuperAlpha only from your own pool, ensuring controlled selection.

---

### 评论 #25 (作者: AK40989, 时间: 1年前)

The distinction between using your own alpha pool versus the expanded alpha pool for SuperAlpha submissions is crucial for optimizing performance. Tagging and filtering alphas based on their origin not only helps in maintaining uniqueness but also enhances the potential for lower correlation among submitted alphas. Have you found that certain tagging strategies lead to better performance outcomes, or is it more about the diversity of the alphas themselves?

---

