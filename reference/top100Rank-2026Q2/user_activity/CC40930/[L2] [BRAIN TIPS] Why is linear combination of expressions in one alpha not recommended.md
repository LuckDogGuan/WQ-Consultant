# [BRAIN TIPS] Why is linear combination of expressions in one alpha not recommended?

- **链接**: [L2] [BRAIN TIPS] Why is linear combination of expressions in one alpha not recommended.md
- **作者**: NL41370
- **发布时间/热度**: 3年前, 得票: 22

## 帖子正文

Linear combination of multiple alphas in one alpha expression may lead to better performance in stat wise (IS performance). However, it is discouraged to do so for 3 reasons:

1. If Linear combination is used just to combine inferior alphas to yield a submittable alpha, this is as good as allocating one's capital to each inferior alpha according to its weight
2. If each expression within the alpha has different scale, it is likely the expression that generate smaller weight magnitude can have trivial impact on the entire signal.

For example, let’s look into the following alpha expression consisting of two sub-expressions:

-ts_delta(close,5)-rank(ts_delta(close,5))

Both sub-expressions are classic ways to implement the idea of reversion. However, the two sub-expressions have different weight magnitude. The first sub-expression's output is change in stock prices which would be much larger than the second sub-expressions output: rank values in range of [0,1]. So the second sub-expression may have a negligible contribution to the alpha.

3. When using linear combination, we cannot check the correlations of the sub-expressions. Therefore, even though it may have improved performance in the IS setting, it could be riskier in out-of-sample because of the possibility of them being highly correlated, leading to sharper drawdowns.

### **Try focusing on making your alpha as simple as possible.**

Implementation of original idea will help solve correlation problem and improve statistical performance. Simple is the best!

---

## 讨论与评论 (6)

### 评论 #1 (作者: TD17989, 时间: 3年前)

Can you explain it in detail? I can only assume that combining alpha with linear model means changing the coefficients of the components in alpha, which in turn can cause overfit -> low os scores. Is this right?

---

### 评论 #2 (作者: BH21731, 时间: 3年前)

I think Brain already has theirs own team to combine alphas together before going to market, so researchers should try to create original signals, and shouldn't add too much noise or combine alpha just to pass backtest or have a good in sample score.

---

### 评论 #3 (作者: LI36776, 时间: 3年前)

If you have to take a linear combination of several terms, and carefully choose each coefficient to maximise the fitness or sharpe ratio, it's probably because each term only has a weak signal and you only get a submittable alpha by overfitting the coefficients to historical data. By choosing each coefficient to maximise the fitness, you're doing something similar to p-hacking, where your alpha "predicts" the in-sample prices closely, but likely fails to predict the out-of-sample prices well. Of course, WorldQuant wants alphas that predict out-of-sample prices well, so there's not much value for them if people submit misleadingly overfitted alphas that perform well only for in-sample data. They'd likely check your alpha's out-of-sample performance first before using it in production, and if your alpha was overfitted, it wouldn't perform well for out-of-sample data. So while using overfitted linear combinations makes it easier for you to submit alphas, you wouldn't learn much from doing this, and the company wouldn't earn money from using overfitted alphas, which is why it isn't recommended.

(Also, I'm not an expert or a WQ employee, this is just my understanding)

---

### 评论 #4 (作者: AC63290, 时间: 1年前)

Linear combinations of Alphas can boost in-sample performance but are discouraged due to scaling disparities, inability to assess sub-expression correlations, and risk of overfitting. Simplifying Alphas and focusing on original ideas ensures better generalization, reduces correlation risks, and enhances robustness for out-of-sample performance, aligning with the principle that simplicity is best.

---

### 评论 #5 (作者: TT55495, 时间: 1年前)

What are some alternative methods to combine multiple alpha expressions without risking overfitting or overcomplicating the model? How can we effectively handle different scales within the expressions to ensure they contribute equally to the final alpha, and what steps can be taken to mitigate the potential risk of high correlation between sub-expressions in the OS period?

---

### 评论 #6 (作者: CC40930, 时间: 1年前)

Using a linear combination of multiple alphas may seem appealing for improving in-sample (IS) performance, but it can lead to issues. First, combining inferior alphas just to create a submittable alpha can be as ineffective as distributing capital across weak alphas. Second, if the alphas have different scales, the one with a smaller magnitude may have a minimal effect. For example, combining a price change with a ranked value could make the ranked value's impact trivial. Finally, combining alphas without checking for correlations can result in riskier out-of-sample performance, as highly correlated expressions can lead to sharper drawdowns. The best approach is to keep your alpha simple and focused on the original idea to improve statistical performance and minimize risks.

---

