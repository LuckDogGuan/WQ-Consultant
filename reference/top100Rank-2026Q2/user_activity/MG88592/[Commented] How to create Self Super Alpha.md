# How to create Self Super Alpha

- **链接**: [Commented] How to create Self Super Alpha.md
- **作者**: MG52134
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

Hello everyone, I have recently achieved Master level and now I am able to create super alphas using other consultant alphas as well. But how can I only select my own alphas in selection expression so as to generate "Self Super Alpha".

---

## 讨论与评论 (27)

### 评论 #1 (作者: AJ93287, 时间: 1年前)

start your selection expression with:

```
own * 
```

---

### 评论 #2 (作者: ST37368, 时间: 1年前)

As mentioned by  [AJ93287](/hc/en-us/profiles/7940329062423-AJ93287)  you can use {own *} or you can name your alphas and use (name == "xyz") in selection expression. It'll recall all those alphas which named xyz

---

### 评论 #3 (作者: VV63697, 时间: 1年前)

Simply in the selection expression use (own)* whatever is your other selection criterion , if you don't put the brackets it selects from the complete pool according to genius level

---

### 评论 #4 (作者: YS82315, 时间: 1年前)

Just use (own)* in the selection expression.

An example of a selection expression could be:

```
(turnover <= 0.2) + 100 * (own)
```

---

### 评论 #5 (作者: MG88592, 时间: 1年前)

Congratulations on achieving the Master level! I would like to ask if you have any good selection and combination expressions for building super alphas?

---

### 评论 #6 (作者: FM59649, 时间: 1年前)

Hello  [MG52134](/hc/en-us/profiles/4718604640407-MG52134) , congratulations on receiving the master level,to submit self alphas,you can use the selection expression multiplied by own,take for instance the example below,for more information you can check

[https://platform.worldquantbrain.com/learn/documentation/superalpha/getting-started-non-self-superalphas](https://platform.worldquantbrain.com/learn/documentation/superalpha/getting-started-non-self-superalphas)

This is a post on how tou can submit both self and non-self superalphas,you can also find it on the learn page

```
own*(turnover<0.5)
```

---

### 评论 #7 (作者: NH16784, 时间: 1年前)

Hi, you can use own * ... to select only your alpha; (not own) * ,,, to select other people's alpha, and use own * .. + (not own) * ... to combine both. For details, you can refer to the Superalpha section in Learn.

---

### 评论 #8 (作者: SK95162, 时间: 1年前)

Go through the 'Learn' section of WorldQuant Brain — it's very helpful. You'll definitely learn how to create a Super Alpha even from pools that aren't your own.

---

### 评论 #9 (作者: SC43474, 时间: 1年前)

To create a "Self Super Alpha" using only your own alphas, you can use  `own *`  in the selection expression. For example:

scss

CopyEdit

`own * (turnover < 0.5)  
`

This ensures that only your personally created alphas are used. You can also use  `(own)`  in combination with other conditions like Sharpe or turnover limits to refine your selection further.

---

### 评论 #10 (作者: AK40989, 时间: 1年前)

To create a "Self Super Alpha," leveraging the selection expression with "own *" is indeed the right approach, as it ensures that only your alphas are considered. Additionally, combining this with specific criteria, such as performance metrics or risk parameters, can enhance the effectiveness of your super alpha. Experimenting with different combinations, like incorporating conditions for turnover or volatility, can lead to more robust results. Engaging with the community and sharing insights on successful expressions can further refine your strategies.

---

### 评论 #11 (作者: RP41479, 时间: 1年前)

Check out the 'Learn' section of WorldQuant Brain—it’s great for learning how to create a Super Alpha, even from external pools.

---

### 评论 #12 (作者: CM45657, 时间: 1年前)

multiply the selection expression with own operator *own

---

### 评论 #13 (作者: HN20653, 时间: 1年前)

Multiply by the own expression

```
Selection Expression..... * own
```

---

### 评论 #14 (作者: KK81152, 时间: 1年前)

Congratulations on reaching  **Master level** ! That's an impressive milestone, and being able to create  **super alphas**  by combining multiple consultant alphas opens up a whole new level of possibilities. To create a  **"Self Super Alpha"**  using only your own alphas, you'll need to carefully craft your selection expression to ensure that only your alphas are being selected.

---

### 评论 #15 (作者: TD37298, 时间: 1年前)

Hi MG52134,Are there specific criteria or methods to evaluate the 'reliability' or 'independence' of self-created alphas before combining them.

---

### 评论 #16 (作者: KS69567, 时间: 1年前)

To create a Self Super Alpha, start by selecting 15–25 of your top-performing alphas with low pairwise correlation (preferably < 0.6) and strong out-of-sample Sharpe ratios. Ensure diversity across regions (e.g., USA, CHN), delay types (D0, D1), and factor styles (momentum, value, sentiment, etc.). Use smart weighting techniques such as Sharpe-based or volatility-adjusted methods to optimize performance, rather than equal weighting. Backtest the combined alpha to check for improved Sharpe, lower drawdown, and acceptable turnover. Regularly monitor and refresh the component alphas as needed. Finalize and submit your Self Super Alpha via “My Alphas” > Create Super Alpha.

---

### 评论 #17 (作者: RG93974, 时间: 1年前)

Congratulations on achieving the Master level,

Just use (own)* in the selection expression.

An example:-

own * (in(datacategories,'other') && universe == "TOP3000" && turnover < 0.30)

---

### 评论 #18 (作者: DT49505, 时间: 1年前)

This is a very relevant question, especially for those who’ve recently unlocked the ability to build super alphas. To create a "Self Super Alpha", using the  `own *`  prefix in your selection expression is indeed the correct approach, as several consultants have mentioned. You can also combine this with additional filters, such as constraints on turnover, volatility, or other metrics, to fine-tune the selection. For instance,  `(own)*(turnover < 0.3)`  would select only your alphas with turnover below 0.3. Additionally, tagging your alphas with identifiable names and using  `name == "..."`  within the selection expression can give you even finer control. Make sure to test various combinations and monitor backtest results to optimize performance.

---

### 评论 #19 (作者: ML46209, 时间: 1年前)

**How to Create a Self Super Alpha**

- Use the selection expression starting with  `own *`  to ensure only your own alphas are included.
- Example:  `own * (turnover < 0.5)`  selects your alphas with turnover below 0.5.
- You can combine  `own *`  with other conditions like Sharpe ratio, volatility, or universe filters.
- Select 15–25 of your best, low-correlation alphas covering diverse regions, delays, and factor styles.
- Use smart weighting (e.g., Sharpe-based or volatility-adjusted) rather than equal weights.
- Backtest for improved Sharpe, reduced drawdown, and acceptable turnover.
- Submit your Self Super Alpha via the “My Alphas” > “Create Super Alpha” page.
- Refer to WorldQuant Brain’s Learn section for detailed guidance.

---

### 评论 #20 (作者: PP87148, 时间: 1年前)

To focus solely on your own alpha in the Super Alpha selection, use the following selection expression:

***(Selection Expression) * OWN***

---

### 评论 #21 (作者: SK90981, 时间: 1年前)

Congratulations on reaching Master level! Great tip on using (own)* in selection—simple yet powerful for refining universe filters effectively.

---

### 评论 #22 (作者: TP18957, 时间: 1年前)

Great question and equally great responses from the community! To add a bit more nuance, when you're constructing a Self Super Alpha, using the  `own *`  syntax in the selection expression ensures you're filtering only your personally submitted alphas. However, it’s also important to think beyond syntax and consider the  *quality*  and  *diversity*  of the alphas you're combining. Prioritize alphas with strong out-of-sample Sharpe ratios and low pairwise correlation. You can further refine your expression with additional filters like  `turnover < 0.3`  or  `sharpe > 1`  to enhance robustness. Also, don't overlook regional and style diversification (e.g., mixing momentum with value or sentiment). A well-structured self alpha portfolio isn’t just about ownership — it’s about synergy. Good luck!

---

### 评论 #23 (作者: RK48711, 时间: 1年前)

Creating a "Self Super Alpha" using the selection expression * *"own "*  is the correct method to focus solely on your alphas. Enhancing it with filters based on  **performance, risk, turnover, or volatility**  can improve its effectiveness. Testing different combinations and  **collaborating with the community**  to share insights can help refine and strengthen your overall strategy.

---

### 评论 #24 (作者: AT42510, 时间: 1年前)

Congrats on hitting Master level! To build a Self Super Alpha, design your selection expression to include only your own alphas while optimizing for performance and diversity.

---

### 评论 #25 (作者: JK98819, 时间: 1年前)

- Use the selection expression starting with  `own *`  to ensure only your own alphas are included.
- Example:  `own * (turnover < 0.3)`  selects your alphas with turnover below 0.3.

---

### 评论 #26 (作者: SM36732, 时间: 1年前)

use own before selection expression

---

### 评论 #27 (作者: MH52691, 时间: 26天前)

Very brilliant Ideas here!

---

