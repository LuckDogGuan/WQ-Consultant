# [BRAIN TIPS] Using Ts_regression Operator

- **链接**: [Commented] [BRAIN TIPS] Using Ts_regression Operator.md
- **作者**: KA64574
- **发布时间/热度**: 3年前, 得票: 11

## 帖子正文

Regression analysis is a statistical method used in finance to study the linear relationship between two or more variables. As an example, we will apply regression analysis to study the relationship between close price and volume weighted average price (VWAP).

VWAP is a measure of the average price of a stock traded throughout the day, taking into account both the price and volume of shares trades. In other words, VWAP gives more weight to trades that occur at higher volumes as they tend to be more significant in terms of market impact.

**Alpha Idea**

A regression analysis between the close price and VWAP of a stock can provide insight into the relationship between the variables. Suppose our hypothesis is that a positive relationship between close price and VWAP suggests that stock is in strong demand, as VWAP is rising along with close price. While a negative relationship may suggest that the stock is in weaker demand, as the VWAP is declining as the close price rises. We can use ts_regression operator to estimate the  [beta coefficient](https://corporatefinanceinstitute.com/resources/data-science/beta-coefficient/)  between close and VWAP, taking 5 variables as inputs: (dependent variable, independent variable, time window, lag, and rettype).

Following the above steps an alpha could be:  **ts_regression(close, vwap, 4, lag = 0, rettype = 2)**

Close price is the dependent variable that we want to predict, VWAP is the independent variable, 4 days is the time window for which we want to run the regression, and 0 means that there is no lag in the VWAP to predict the close price, lastly rettype = 2 means that we want the beta coefficient (β) as the output.

**Other Rettype Values**

If we seek to get other parameters as the output, we can use these “rettype” argument values :

-        0 corresponds to the error term,

-        1 corresponds to the y-intercept (α),

-        2 corresponds to the beta coefficient (β)

-        3 corresponds to the estimate of the dependent variable.

-        4 corresponds to the sum of squares of error (SSE)

-        5 corresponds to the sum of squares of total (SST)

-        6 corresponds to the R-Square

-        7 corresponds to the mean square error (MSE)

-        8 corresponds to the standard error term of the beta coefficient (β)

-        9 corresponds to the standard error of the y-intercept (α)

**Graphical Representation of Rettype Values**

**![图片](images/img_ebfc617e0f.png)**

---

## 讨论与评论 (8)

### 评论 #1 (作者: ZY79068, 时间: 3年前)

Good visual summary! Thanks!

---

### 评论 #2 (作者: MI59300, 时间: 2年前)

Can we perform polynomial regression with ts_regression, such that we are able to return the coefficients? (ts_poly_regression only returns y-Ey) If possible how so?

---

### 评论 #3 (作者: SH71033, 时间: 2年前)

Right now, ts_poly_regression only supports y- Ey, unlike multiple rettypes under the ts_regression operator.

---

### 评论 #4 (作者: HV77283, 时间: 1年前)

Thank you so much for sharing such a great n wonderful information  . Your points and explanations help us to improve our work quality.Great tips.

---

### 评论 #5 (作者: SK72105, 时间: 1年前)

Great breakdown of the ts_regression operator! In the example given in the article we output beta. How can we use this value to create an alpha?

---

### 评论 #6 (作者: TT55495, 时间: 1年前)

When testing the beta coefficient from a regression (rettype = 2), how can you apply this value to create more sophisticated alpha models, such as those that predict stock momentum or reversals?

---

### 评论 #7 (作者: TD17989, 时间: 1年前)

Hi, I saw Brain updated the multi regression operator, however I found it not working as efficiently as ts_regression

---

### 评论 #8 (作者: CC40930, 时间: 1年前)

Regression analysis in finance helps study the relationship between variables like close price and VWAP. By using the  `ts_regression`  operator, you can analyze the dependency of close price on VWAP. For instance, using  `ts_regression(close, vwap, 4, lag = 0, rettype = 2)`  estimates the beta coefficient. You can also retrieve other regression parameters, such as error term, y-intercept, or R-Square, by adjusting the  `rettype`  argument to get more insights into the relationship and performance of the stock.

---

