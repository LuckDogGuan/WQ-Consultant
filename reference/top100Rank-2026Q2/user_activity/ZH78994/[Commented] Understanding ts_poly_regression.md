# Understanding ts_poly_regression

- **链接**: [Commented] Understanding ts_poly_regression.md
- **作者**: MI59300
- **发布时间/热度**: 2年前, 得票: 3

## 帖子正文

Based on the description of ts_poly_regression, the function returns y-Ey.

If y = close, then the (finite difference) second derivative of the quadratic poly regression would be

> quad_diff = ts_poly_regression(close, ts_step(1), 42, k=2);
> Ey = -(quad_diff-close); ## Since quad_diff = y-Ey
> d2close = (Ey - 2*ts_delay(Ey, 42) + ts_delay(Ey, 84)) / 1764;

Is my understanding of obtaining the regression equation (Ey) correct? Is it possible to do this with ts_regression where I can obtain the coefficients?

---

## 讨论与评论 (12)

### 评论 #1 (作者: AG20578, 时间: 2年前)

Yes, your formula for second derivative is correct.

Yes, it is possible to use ts_regression to get Ey:

[https://platform.worldquantbrain.com/learn/data-and-operators/detailed-operator-descriptions#ts_regressiony-x-d-lag-0-rettype-0](https://platform.worldquantbrain.com/learn/data-and-operators/detailed-operator-descriptions#ts_regressiony-x-d-lag-0-rettype-0)

```
ts_regression(close, step(1), 42, lag = 0, rettype = 3)
```

---

### 评论 #2 (作者: DK20528, 时间: 1年前)

Your understanding is close, but let's break it down and clarify the steps to ensure everything makes sense. You're trying to compute the second derivative of the  `close`  price using quadratic polynomial regression, and you're working with the function  `ts_poly_regression` . Here’s a step-by-step explanation:

### 1.  **What  `ts_poly_regression`  returns** :

The function  `ts_poly_regression(close, ts_step(1), 42, k=2)`  performs a quadratic polynomial regression over the data. According to your description, this function returns the difference between the original values ( `y` ) and the estimated values ( `Ey` ), where  `Ey`  is the estimated value from the polynomial regression.

Thus, the formula is:

\text{quad_diff} = y - Ey

Where  `y = close`  and  `Ey`  is the estimated value of  `y`  based on the quadratic regression.

### 2.  **Computing the second derivative** :

To compute the second derivative of the  `close`  price, you're using finite differences. The formula you provided for  `d2close`  is trying to approximate the second derivative of  `Ey` , which is the estimated value of  `close`  based on the regression.

The formula for  `d2close`  in your example:

\text{d2close} = \frac{Ey - 2 \cdot \text{ts_delay}(Ey, 42) + \text{ts_delay}(Ey, 84)}{1764}

is essentially using a finite difference method to approximate the second derivative. The denominator  `1764`  comes from the scaling factor, which is related to the time step  `1`  and the spacing between  `42`  and  `84` .

### 3.  **Your formula** :

From your explanation, you are attempting to approximate the second derivative of  `Ey`  (the estimated value from the polynomial regression) with respect to time. The finite difference formula approximates the second derivative, and it looks correct in terms of structure.

Here's a breakdown of your formula:

- `Ey`  is the estimated value based on quadratic regression.
- `ts_delay(Ey, 42)`  shifts  `Ey`  by 42 time steps backward (this gives you the previous value of  `Ey` ).
- `ts_delay(Ey, 84)`  shifts  `Ey`  by 84 time steps backward.
- The finite difference formula is then applied, and the denominator  `1764`  is the square of  `42` , reflecting the step size squared.

### Conclusion:

Yes, your understanding is correct. You are computing the second derivative of the estimated value ( `Ey` ) from the quadratic polynomial regression using a finite difference method, and your formula for  `d2close`  is a valid way to approximate the second derivative of  `Ey`  based on the delays. The logic behind the finite difference formula is sound, and the use of  `1764`  is also consistent with the step size used in the finite difference approximation.

---

### 评论 #3 (作者: SJ17125, 时间: 1年前)

You're using  `ts_poly_regression`  to perform quadratic polynomial regression on the close price, where the function returns the difference between actual and estimated values (y - Ey). To approximate the second derivative of the estimated close (Ey), you apply a finite difference formula:

\text{d2close} = \frac{Ey - 2 \cdot \text{ts_delay}(Ey, 42) + \text{ts_delay}(Ey, 84)}{1764}

The denominator, 1764, represents the square of the step size (42), aligning with finite difference methods. This approach effectively computes the second derivative of Ey with respect to time, capturing price concavity trends. Your formula is mathematically sound and well-structured for this purpose.

---

### 评论 #4 (作者: MK58212, 时间: 1年前)

Thank you for sharing this valuable insight

---

### 评论 #5 (作者: RK48711, 时间: 1年前)

Thank you for clarifying! This breakdown makes sense and aligns with my understanding. Here's my interpretation based on your explanation:

1. **Understanding  `ts_poly_regression` :**
   The function returns the difference between the actual values ( `y` , i.e.,  `close` ) and the estimated values ( `Ey` ) obtained through quadratic regression. This clarified distinction between  `y`  and  `Ey`  is helpful.
2. **Second Derivative Calculation:**
   The finite difference formula indeed approximates the second derivative of  `Ey`  (not  `y` ), and the denominator, 1764, reflects the squared time step size. The structure of the formula looks consistent with the principles of finite differences.
3. **Conclusion:**
   It seems my approach to compute the second derivative of the estimated values ( `Ey` ) is correct. I'll ensure I focus on  `Ey`  instead of  `y`  when applying this logic.

Thanks again for your detailed explanation—it clarified a few nuances I might have overlooked!

---

### 评论 #6 (作者: XL31477, 时间: 1年前)

**Hey, your understanding is indeed correct. You've got the right idea about using ts_poly_regression and computing the second derivative with that finite difference formula. And yep, you can use ts_regression to get the coefficients too. Just make sure you follow the steps clearly when working with these functions in your quant strategies. Keep it up!**

---

### 评论 #7 (作者: BA51127, 时间: 1年前)

**Function Explanation** :  `ts_poly_regression`  performs a polynomial regression on the data and returns the difference between the original values (y) and the estimated values (Ey) from the regression. This is crucial for understanding how the function operates and what output it provides.
 **Second Derivative Calculation** : The conversation clarifies how to compute the second derivative of the estimated values (Ey) using a finite difference method. The formula provided approximates the second derivative and is mathematically sound, with the denominator (1764) being the square of the time step size (42), which aligns with finite difference methods.
 **Using ts_regression for Coefficients** : It is confirmed that  `ts_regression`  can also be used to obtain the coefficients of the regression equation, which is another way to work with regression in quantitative strategies.

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

- Your understanding of obtaining  **Ey**  using  `ts_poly_regression`  is correct. You are computing the residuals (difference between actual and fitted values) and then applying finite differences to approximate the second derivative.
- **`ts_regression`**  is more for linear regression and wouldn't directly provide you with polynomial coefficients or a straightforward method to get a quadratic fit. For quadratic regression,  **`ts_poly_regression`**  is the more appropriate operator.

---

### 评论 #9 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #10 (作者: NH84459, 时间: 1年前)

Yes, you're absolutely correct! The  `ts_regression`  operator can indeed be used to compute the regression of a time series like  `close`  on a lagged series or step function, with the appropriate parameters. In this case:

- `close`  represents the time series you're working with (e.g., stock closing prices).
- `step(1)`  represents the independent variable, potentially indicating a time step or another series you wish to regress against.
- `42`  could be the number of periods (e.g., lookback window or number of observations).
- `lag = 0`  specifies that the regression should be calculated with no lag between the dependent and independent variables.
- `rettype = 3`  specifies that you want to retrieve the  *y*  values of the regression, which gives you the fitted values for the dependent variable.

---

### 评论 #11 (作者: LY88401, 时间: 1年前)

"Thank you for sharing your outstanding work with us! Your writing not only highlights your incredible talent but also provides valuable insights and inspiration. I truly admire the effort and thoughtfulness you’ve put into creating something so impactful. Your storytelling skills are exceptional, leaving a lasting impression on readers. Please continue to share your amazing creations—I’m eagerly anticipating your next piece! Thank you once again for your generosity and dedication."

---

### 评论 #12 (作者: RB20756, 时间: 1年前)

ts_poly_regression estimates residuals as the difference between actual values (y) and quadratic regression outputs (Ey). The second derivative uses finite differences on Ey, with a denominator reflecting the time step size. ts_regression suits linear fits, not quadratic.

---

