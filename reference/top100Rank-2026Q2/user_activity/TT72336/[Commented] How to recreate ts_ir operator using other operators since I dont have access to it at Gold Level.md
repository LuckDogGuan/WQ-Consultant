# How to recreate ts_ir operator using other operators since I don't have access to it at Gold Level

- **链接**: How to recreate ts_ir operator using other operators since I dont have access to it at Gold Level.md
- **作者**: AM60509
- **发布时间/热度**: 1年前, 得票: 6

## 帖子正文

How to recreate ts_ir operator using other operators since I don't have access to it at Gold Level.Please let me know on how to do this

---

## 讨论与评论 (17)

### 评论 #1 (作者: UG81605, 时间: 1年前)

ts_mean()/ts_std_dev, simple

---

### 评论 #2 (作者: MD65015, 时间: 1年前)

You can replace the  `ts_ir`  operator with the following formula using  `ts_mean`  and  `ts_stddev` :

ts_ir(x, day) = ts_mean(x,day)/ts_stddev(x, day)

This formula calculates the Information Ratio (IR) by dividing the mean of the time series  `x`  over the given day by its standard deviation over the same period.

---

### 评论 #3 (作者: HN71281, 时间: 1年前)

You can replicate  **ts_ir**  using  **ts_mean(returns, N) / ts_stddev(returns, N)**  to calculate the rolling information ratio manually. Adjust  **N**  based on your time horizon for better signal stability.

---

### 评论 #4 (作者: RB98150, 时间: 1年前)

`you can try this : ts_mean(ts_delta(signal, days)) / ts_std_dev(ts_delta(signal, days))
`

---

### 评论 #5 (作者: LM22798, 时间: 1年前)

can ts_rank work in that case scenario? I have seen it work when i was creating a superalpha

---

### 评论 #6 (作者: NT29269, 时间: 1年前)

You can indirectly use ts_ir(x, d) through two functions, ts_mean(x, d) and ts_std_dev(x, d), since by definition, ts_ir(x, d) = ts_mean(x, d) / ts_std_dev(x, d). However, the drawback is that it increases the total number of operators you use, which may not be optimal for the genius subcriterion.

---

### 评论 #7 (作者: RB20756, 时间: 1年前)

You can replace  `ts_ir(x, d)`  with  `ts_mean(x, d) / ts_stddev(x, d)` , which calculates the rolling Information Ratio manually. While this provides the same result, it may increase the number of operators used, which could impact optimization under Genius program constraints. Adjust  `d`  for stability.

---

### 评论 #8 (作者: HN20653, 时间: 1年前)

You can use ts_mean / ts_std_dev

---

### 评论 #9 (作者: TT72336, 时间: 1年前)

You can replace  `ts_ir(x, day)`  with: ts_mean(x, day) / ts_stddev(x, day)

---

### 评论 #10 (作者: TP19085, 时间: 1年前)

You can replicate the functionality of  `ts_ir(x, d)`  by using  `ts_mean(x, d)`  and  `ts_std_dev(x, d)` , as it follows the formula:

```
ts_ir(x,d)=ts_std_dev(x,d)/ts_mean(x,d)​​
```

However, this approach comes with a trade-off. Since it requires using two separate functions instead of one, it increases the total number of operators in your expression. This could be problematic if you're optimizing for the genius subcriterion, where efficiency and minimal operator usage are preferred. Therefore, direct usage of  `ts_ir(x, d)`  remains the better option when possible.

---

### 评论 #11 (作者: AS16039, 时间: 1年前)

You can recreate the  **ts_ir**  operator using:

ts_ir(x,d)=ts_mean(x,d)/ts_stddev(x,d)ts\_ir(x, d) = ts\_mean(x, d) / ts\_stddev(x, d)ts_ir(x,d)=ts_mean(x,d)/ts_stddev(x,d)

This computes the rolling  **Information Ratio**  over a window of  **d**  days by dividing the mean by the standard deviation.

**Considerations:**

- Using two separate operators increases the total count, which may impact the  **Genius subcriterion** .
- Adjust  **d**  for signal stability.

---

### 评论 #12 (作者: PT27687, 时间: 1年前)

It's great to see your initiative in exploring alternatives to the ts_ir operator! Have you thought about which specific operators you currently have access to? It might help to outline what you want to achieve with ts_ir, so we can brainstorm some effective combinations of the available operators.

---

### 评论 #13 (作者: ML46209, 时间: 1年前)

You can replicate the  `ts_ir`  operator by using  `ts_mean(returns, N) / ts_stddev(returns, N)`  to manually calculate the rolling information ratio. Adjust the value of N based on your time horizon to improve signal stability

---

### 评论 #14 (作者: NA18223, 时间: 1年前)

it requires using two separate functions instead of one, it increases the total number of operators in your expression. This could be problematic if you're optimizing for the genius subcriterion, where efficiency and minimal operator usage are preferred.

---

### 评论 #15 (作者: AK40989, 时间: 1年前)

To recreate the `ts_ir` operator, you can use the following simple steps:

1. Calculate the excess returns: alpha returns minus benchmark returns.
2. Use `ts_mean()` to find the average of the excess returns.
3. Use `ts_std_dev()` to calculate the standard deviation of the excess returns.
4. Divide the average excess return by the standard deviation to get the Information Ratio.

This method will effectively give you the Information Ratio using basic operators.

---

### 评论 #16 (作者: DK30003, 时间: 1年前)

You can indirectly use ts_ir(x, d) through two functions, ts_mean(x, d) and ts_std_dev(x, d), since by definition, ts_ir(x, d) = ts_mean(x, d) / ts_std_dev(x, d). However, the drawback is that it increases the total number of operators you use, which may not be optimal for the genius subcriterion.

---

### 评论 #17 (作者: NN89351, 时间: 1年前)

Great to see your initiative in finding alternatives to the ts_ir operator! Have you identified which specific operators are available to you? Defining the exact goal you want to achieve with ts_ir could help us explore effective operator combinations.

---

