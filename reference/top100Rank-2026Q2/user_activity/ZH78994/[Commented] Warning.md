# Warning

- **链接**: [Commented] Warning.md
- **作者**: AS12128
- **发布时间/热度**: 2年前, 得票: 3

## 帖子正文

- Incompatible unit for input at index 0, expected "Unit[]", found "Unit[CSPrice:1]"
- Incompatible unit for input at index 1, expected "Unit[]", found "Unit[CSPrice:1]"
  how to handle these errors/warnings?

---

## 讨论与评论 (11)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Hello, this warning means that your Alpha expression has a wrong dimension (unit). For example, when you use close+volume, such an error message will appear. Because the unit of the close is "$" and the unit of the volume is "shares count". Performing direct operations on datafields in different units will produce "Incompatible unit error".

But if we change expression to

rank(close)+rank(volume)

, for example, we won't have this warning anymore

---

### 评论 #2 (作者: TN48752, 时间: 1年前)

You should carefully study the field descriptions before applying them together. For example, price fields are calculated in $, while volume is calculated differently.

---

### 评论 #3 (作者: DK20528, 时间: 1年前)

It's important to thoroughly understand the descriptions of each field before combining them. For instance, price-related fields are typically measured in dollars, whereas volume fields are calculated using a different scale or unit.

---

### 评论 #4 (作者: XL31477, 时间: 1年前)

**Hey! These warnings indicate unit mismatch in your input. As the others said, different fields have different units like price in "$" and volume in "shares count". Before using them together in an expression, make sure you understand each field's unit properly. You can either transform them to have compatible units or use functions like rank() on them separately before combining, so that the operations won't trigger such incompatible unit errors.**

---

### 评论 #5 (作者: ND68030, 时间: 1年前)

You will still be able to simulate alpha successfully, but in real markets alpha will not work that way. Try to understand the nature of the data to combine them appropriately.

---

### 评论 #6 (作者: DN45758, 时间: 1年前)

[AG20578](/hc/en-us/profiles/12243980162327-AG20578)  Thank you for addressing this important clarification about unit compatibility in alpha expressions. Your guidance ensures accurate calculations and avoids errors in dimensional consistency.

---

### 评论 #7 (作者: MK58212, 时间: 1年前)

When encountering errors like:

- **Incompatible unit for input at index 0, expected "Unit[]", found "Unit[CSPrice:1]"**
- **Incompatible unit for input at index 1, expected "Unit[]", found "Unit[CSPrice:1]"**

it often indicates a mismatch between the expected and provided input data types or units in your model or function. Here are a few points to clarify:

1. How do you typically handle unit mismatches when integrating price-based metrics (e.g., CSPrice) into a calculation that expects unitless inputs?
2. Are there specific preprocessing steps or conversions recommended to align such inputs with the expected units?
3. If the issue persists, would a custom function to handle unit casting or normalization be a viable approach?

Looking forward to your thoughts!

---

### 评论 #8 (作者: BA51127, 时间: 1年前)

**Understanding  `rank`  and  `-rank`** : The  `rank`  function assigns a value between 0 and 1 to each stock based on a given metric, with 0 being the lowest and 1 being the highest. When the rank is negated, as in  `-rank(ts_delta(close,5))` , the order is flipped, with stocks that have the largest negative changes (drops) in price receiving the highest ranks.
 **Interpretation for Shorting** : Using  `-rank(ts_delta(close,5))`  as a signal means that stocks with the largest negative price changes over the last 5 periods will have the highest ranks, indicating a higher confidence level for shorting these stocks. Conversely, stocks with smaller or positive changes will have lower ranks, suggesting less confidence in shorting them.
 **Application in Alpha Strategies** : This method can be effectively used to target stocks with significant recent negative momentum for short positions and potentially consider long positions for those with positive or small changes, depending on the strategy's design.

---

### 评论 #9 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #10 (作者: NH84459, 时间: 1年前)

However, by using a transformation like  `rank(close) + rank(volume)` , you're essentially removing the units by converting both fields into a dimensionless ranking (or ordinal value) based on their relative position. Since ranks are unitless, the operation can now proceed without any errors.

This approach ensures that you're working with comparable data, allowing you to perform calculations without running into dimensionality issues.

---

### 评论 #11 (作者: LY88401, 时间: 1年前)

"Thank you for sharing your outstanding work with us! Your writing not only highlights your incredible talent but also provides valuable insights and inspiration. I truly admire the effort and thoughtfulness you’ve put into creating something so impactful. Your storytelling skills are exceptional, leaving a lasting impression on readers. Please continue to share your amazing creations—I’m eagerly anticipating your next piece! Thank you once again for your generosity and dedication."

---

