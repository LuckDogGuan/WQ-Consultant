# How to perform polynomial regression?

- **链接**: [Commented] How to perform polynomial regression.md
- **作者**: MI59300
- **发布时间/热度**: 2年前, 得票: 75

## 帖子正文

I would like to determine whether historical prices are either concave up or down. To do this I would like to perform a polynomial regression, meaning x = time and y = close for example. I know there is the ts_poly_regression operator, however

1. Im not sure how to represent the x input as 'time'. Would ts_step work?

2. The ts_poly_regression operator returns y-Ex. How can i obtain the coefficients, or in my case, the sign of the coefficients? (something like rettype in ts_regression)

Thanks

---

## 讨论与评论 (15)

### 评论 #1 (作者: UG81605, 时间: 2年前)

Use ts_regression and for time use ts_step(1). example- ts_regression(data,ts_step(1),.....)

---

### 评论 #2 (作者: MI59300, 时间: 2年前)

How do you use ts_regression to fit a quadratic model?

---

### 评论 #3 (作者: SH71033, 时间: 2年前)

Hi,
Please refer to ts_poly_regression(y, x, d, k = 1) for polynomial regression. with degree 2 for the quadratic regression.

---

### 评论 #4 (作者: DK20528, 时间: 1年前)

To determine whether historical prices are concave up or down using polynomial regression, let's break down the two key aspects you’re asking about:

### 1.  **Representing 'Time' (x) as the Input for Polynomial Regression**

For polynomial regression using  `ts_poly_regression` , you want  `x`  to represent the time, and  `y`  to represent the historical prices (e.g.,  `close`  prices). In this case, you are correct in considering  `ts_step` , as it provides a way to represent the time variable.

- **`ts_step(1)`** : This gives you the time steps, with each time period incremented by 1. So if you apply  `ts_step(1)`  as the  `x`  input, it will increment by 1 at each step, corresponding to each data point in the series.
- **`ts_step`  for Time** : Yes, using  `ts_step(1)`  as the input  `x`  is a valid approach because it gives you a consistent time series from 1 to n (where n is the number of data points), allowing you to perform regression on the historical prices. Each value of  `x`  corresponds to a particular time point.

### 2.  **Obtaining the Coefficients or the Sign of the Coefficients**

You're right that  `ts_poly_regression`  returns  `y - Ex` , where  `Ex`  is the estimated value from the polynomial regression. However, the operator does not directly return the coefficients of the polynomial regression.

To retrieve the coefficients (which you need to determine concavity by inspecting the second derivative), you can use the following approach:

- **Alternative: Use  `ts_regression`** : The  `ts_regression`  operator will return the coefficients of a linear regression (or polynomial if you specify a higher degree). The sign of the second-degree coefficient will give you the information about concavity:
  - **Concave Up** : If the second-degree coefficient is positive, the curve is concave up.
  - **Concave Down** : If the second-degree coefficient is negative, the curve is concave down.

Here's how you can apply  `ts_regression`  for polynomial regression:

#### Steps to Get the Polynomial Coefficients (for a Quadratic Polynomial):

1. **Apply  `ts_regression`  with degree 2** :
   python
   Copy code
   `reg_result = ts_regression(close, ts_step(1), 2)
   `
   This will return a structure where the coefficients of the polynomial (e.g.,  `a` ,  `b` , and  `c`  for a quadratic model y=ax2+bx+cy = ax^2 + bx + cy=ax2+bx+c) are stored.
2. **Check the Sign of the Coefficient** :
   - **Quadratic Term (Second Degree Coefficient)** : The sign of the second-degree coefficient will tell you about the concavity:
   - Positive → Concave up.
   - Negative → Concave down.
   To extract and check the second coefficient:
   python
   Copy code
   `quadratic_coefficient = reg_result[2]  # Index 2 corresponds to the quadratic term
   if quadratic_coefficient > 0:
   print("Concave up")
   elif quadratic_coefficient < 0:
   print("Concave down")
   else:
   print("Linear (no concavity)")
   `

### Summary:

- **To represent 'time' as  `x`** : You can use  `ts_step(1)`  to create a simple time variable, where each step corresponds to a time period.
- **To obtain the coefficients (and their signs)** : Instead of using  `ts_poly_regression` , use  `ts_regression`  with a polynomial degree of 2 to get the coefficients directly. The second-degree coefficient will indicate whether the curve is concave up or down based on its sign.

This approach should help you analyze the concavity of historical prices effectively.

---

### 评论 #5 (作者: RK48711, 时间: 1年前)

Thank you for the detailed explanation! Using  `ts_step(1)`  to represent time as  `x`  and  `ts_regression`  for obtaining the polynomial coefficients makes a lot of sense. I appreciate the clarity on how to interpret the second-degree coefficient to determine concavity. This approach seems both straightforward and effective for analyzing historical price trends. Thanks again for your insights!

---

### 评论 #6 (作者: SJ17125, 时间: 1年前)

Hi  [DK20528](/hc/en-us/profiles/24602396283031-DK20528)

Thank you for the clear and detailed explanation! Using  `ts_step(1)`  to represent time as x and  `ts_regression`  to extract polynomial coefficients is both logical and highly effective. The insight on interpreting the second-degree coefficient for concavity adds a new layer of precision to trend analysis. Combining this approach with additional signals, like volatility or momentum, could further enhance its predictive power. This method is a great tool for exploring historical price dynamics—thank you for sharing such valuable knowledge!

---

### 评论 #7 (作者: MK58212, 时间: 1年前)

The explanation provides a clear method for determining concavity in historical prices using polynomial regression. It suggests using  `ts_step(1)`  to represent time and  `ts_regression`  with a degree of 2 to obtain polynomial coefficients. The sign of the second-degree coefficient effectively indicates concavity: positive for concave up, negative for concave down.

---

### 评论 #8 (作者: XL31477, 时间: 1年前)

**Hey!  [DK20528](/hc/en-us/profiles/24602396283031-DK20528) 's explanation is really on point. To sum it up simply, for representing 'time' as x in polynomial regression, ts_step(1) works well as it gives a proper time series. And to get the coefficients and check concavity, use ts_regression with degree 2. The sign of the second-degree coefficient tells if it's concave up (positive) or down (negative). It's a handy way to analyze historical price trends indeed.**

---

### 评论 #9 (作者: BA51127, 时间: 1年前)

To perform polynomial regression and determine the concavity of historical prices, you can use the  `ts_regression`  operator with a degree of 2. Here's a step-by-step guide:

**Representing Time (x) as Input** : Use  `ts_step(1)`  to create a time variable where each step corresponds to a time period. This will give you a consistent time series from 1 to n, where n is the number of data points.

**Obtaining the Coefficients** : Apply  `ts_regression`  with degree 2 to get the coefficients of the polynomial regression. The second-degree coefficient will indicate the concavity:

- Positive second-degree coefficient: Concave up.
- Negative second-degree coefficient: Concave down.

Here's how you can implement it:

python

```
reg_result = ts_regression(close, ts_step(1), 2)
quadratic_coefficient = reg_result[2]  # Index 2 corresponds to the quadratic term

if quadratic_coefficient > 0:
    print("Concave up")
elif quadratic_coefficient < 0:
    print("Concave down")
else:
    print("Linear (no concavity)")
```

This approach allows you to effectively analyze the concavity of historical price trends.

---

### 评论 #10 (作者: AT56452, 时间: 1年前)

Incorporating the second derivative's insights on concavity with volatility and momentum indicators enriches trend analysis. This comprehensive approach enhances the precision of predictions concerning historical price dynamics, offering valuable tools for financial analysis and strategy development.

---

### 评论 #11 (作者: HD25387, 时间: 1年前)

**Great question! Here are some suggestions to address your points:**

1. **Using  `time`  as  `x` :**
   - Yes,  `ts_step`  is a good option for representing  `time`  as the  `x`  input. It provides a sequence of integers (e.g., 1, 2, 3, ...) that can serve as time steps in your polynomial regression.
2. **Obtaining Coefficients or Their Sign:**
   - Unfortunately,  `ts_poly_regression`  directly outputs the residuals ( `y - Ex` ) rather than the coefficients. To get the sign of the coefficients:
   - You can compare the trend by calculating the slope over segments of the data (e.g.,  `ts_slope(close, window)` ).
   - Alternatively, you might need to use custom logic or pair  `ts_poly_regression`  with other operators to infer the curvature indirectly.
   - If you specifically need coefficients, you may need to approximate them using regression-like functions such as  `ts_regression`  or external processing tools to manually compute the polynomial fit.

**Workaround Idea:**

- You could approximate the curvature by comparing  `y`  values at different time intervals and analyzing the change in the residuals from  `ts_poly_regression` .

Hope this helps! Let me know if you’d like further clarification or alternative approaches! 😊

---

### 评论 #12 (作者: CC40930, 时间: 1年前)

- **`ts_step(1)`**  works well to represent time as the independent variable  `x`  in the polynomial regression.
- **`ts_poly_regression`**  returns residuals, but it does not provide the coefficients.
- To obtain the coefficients or the sign of the coefficients, you can use  **`ts_regression`**  with  `x`  and  `x^2`  to fit a quadratic model and extract the sign of the quadratic term to determine the concavity of the price curve.

---

### 评论 #13 (作者: LY88401, 时间: 1年前)

Your article is excellently written! The ideas are clear, engaging, and well-organized. You have a remarkable ability to present complex topics in a simple, accessible way. It’s an insightful and thought-provoking read that reflects your deep understanding and expertise.

---

### 评论 #14 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #15 (作者: PP87148, 时间: 1年前)

Thank you for the detailed explanation! Using  `ts_step(1)`  to represent time as  `x`  and  `ts_regression`  for obtaining the polynomial coefficients makes a lot of sense. This approach seems both straightforward and effective for analyzing historical price trends.

---

